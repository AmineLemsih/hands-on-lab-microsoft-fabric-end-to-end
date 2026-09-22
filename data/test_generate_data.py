"""Contrôler les contrats des données synthétiques sans dépendance externe."""

import csv
import io
import re
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal, InvalidOperation
from html.parser import HTMLParser
from pathlib import Path

import generate_data as generator


def numeric_value(text):
    words = {"un": "1", "une": "1", "deux": "2", "trois": "3", "six": "6", "sept": "7"}
    normalized = " ".join(text.split()).lower()
    return Decimal(words.get(normalized, normalized).replace(" ", "").replace(",", "."))


def read_expected_values(markdown):
    table = "\n".join(line for line in markdown.splitlines() if line.startswith("|"))
    rows = list(csv.reader(io.StringIO(table), delimiter="|"))
    return {row[1].strip(): numeric_value(row[2]) for row in rows[2:]}


class WorkshopValues(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []
        self.unmarked = []
        self.current = None
        self.parts = []

    def handle_starttag(self, tag, attrs):
        key = dict(attrs).get("data-expected")
        if key is not None:
            if tag != "span" or self.current is not None:
                raise ValueError("data-expected exige un span non imbriqué")
            self.current = (key, self.getpos()[0])
            self.parts = []
            self.unmarked.append(" ")

    def handle_data(self, data):
        if self.current is None:
            self.unmarked.append(data)
        else:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == "span" and self.current is not None:
            key, line = self.current
            self.references.append((key, "".join(self.parts), line))
            self.current = None
            self.unmarked.append(" ")


def workshop_value_errors(workshop, expected):
    prose = re.sub(r"^---\n.*?\n---\n", lambda match: "\n" * match[0].count("\n"), workshop, count=1, flags=re.DOTALL)
    prose = re.sub(r"```[^\n]*\n.*?```", lambda match: "\n" * match[0].count("\n"), prose, flags=re.DOTALL)
    prose = re.sub(r"`([^`\n]+)`", lambda match: match[1] if re.fullmatch(r"\d[\d ,.]*", match[1]) else "", prose)
    prose = re.sub(r"\]\([^\n)]*\)", "", prose)
    parsed = WorkshopValues()
    parsed.feed(prose)
    parsed.close()
    errors = []
    if not parsed.references or parsed.current is not None:
        errors.append("Valeurs absentes ou balisage data-expected incomplet")
    for key, text, line in parsed.references:
        try:
            actual = numeric_value(text)
        except InvalidOperation:
            errors.append(f"Ligne {line} : {key} n'est pas une valeur numérique : {text!r}")
            continue
        if key not in expected:
            errors.append(f"Ligne {line} : {key} absent de expected_values.md")
        elif actual != expected[key]:
            errors.append(f"Ligne {line} : {key} affiche {text!r}, attendu {expected[key]}")
    unmarked = "".join(parsed.unmarked).replace("*", "")
    quantities = re.compile(
        r"(?<![\w])(?:\d{1,3}(?:[ \u00a0\u202f]\d{3})+(?:[.,]\d+)?"
        r"|\d{5,}"
        r"|\d+,\d+"
        r"|une(?=\s+seule\s+ligne\b)"
        r"|(?:\d+|six|sept|trente)(?=\s+(?:lignes?|observations?|sites?|colonnes?|pics?|régions?|barres?|couples?|kWh|kgCO2e|valeurs?|enregistrements?)\b))",
        re.IGNORECASE,
    )
    for match in quantities.finditer(unmarked):
        errors.append(f"Valeur métier sans data-expected : {match.group()!r}")
    return errors


class DataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.root = Path(cls.temporary.name)
        cls.before = cls.root / "before"
        cls.repeated = cls.root / "repeated"
        cls.after = cls.root / "after"
        script = Path(generator.__file__)
        for folder, state in ((cls.before, "before"), (cls.repeated, "before"), (cls.after, "after")):
            subprocess.run(
                [sys.executable, str(script), "--out", str(folder), "--latest-state", state],
                check=True, capture_output=True,
            )
        cls.sites = generator.read_csv(cls.before / "sites.csv")
        cls.raw = generator.read_csv(cls.before / "consumption_2025.csv")
        cls.cleaned, cls.blanks, cls.errors = generator.clean_rows(cls.raw)

    def test_repeated_generation_is_byte_identical(self):
        expected = {
            "sites.csv", "emission_factors.csv", "consumption_2025.csv",
            "consumption_latest_day.csv", "consumption_latest_day_before.csv",
            "consumption_latest_day_after.csv", "questions_expected_answers.md",
            "expected_values.md",
        }
        self.assertEqual({path.name for path in self.before.iterdir()}, expected)
        for name in expected:
            with self.subTest(file=name):
                self.assertEqual((self.before / name).read_bytes(), (self.repeated / name).read_bytes())

    def test_schema_and_grain(self):
        self.assertEqual(len(self.raw), 10950)
        self.assertEqual((self.blanks, self.errors, len(self.cleaned)), (55, 55, 10840))
        self.assertEqual(set(self.raw[0]), set(generator.FIELDS))
        self.assertEqual(set(self.sites[0]), {"site_id", "site_name", "region", "activity", "area_m2", "opening_date"})
        self.assertEqual(len({(row["site_id"], row["date"]) for row in self.cleaned}), 10840)
        for path in self.before.glob("*.csv"):
            for column in generator.read_csv(path)[0]:
                self.assertIsNotNone(re.fullmatch(r"[a-z][a-z0-9_]*", column))

    def test_expected_values_are_calculated_and_scenario_independent(self):
        expected = (self.before / "expected_values.md").read_text(encoding="utf-8")
        self.assertIn(f"| site_count | {len(self.sites)} |", expected)
        self.assertIn(f"| clean_rows | {len(self.cleaned):,} |".replace(",", " "), expected)
        electricity = sum(Decimal(row["kwh_elec"]) for row in self.cleaned)
        self.assertIn(f"| electricity_kwh | {generator.french_number(electricity)} |", expected)
        self.assertIn("| electricity_factor | 0,055 |", expected)
        self.assertIn("| gas_factor | 0,205 |", expected)
        self.assertEqual(expected, (self.after / "expected_values.md").read_text(encoding="utf-8"))
        committed = Path(generator.__file__).resolve().parent / "csv/expected_values.md"
        self.assertEqual(expected, committed.read_text(encoding="utf-8"), "Régénérer expected_values.md avant de publier")

    def test_workshop_values_match_generated_reference(self):
        workshop = (Path(generator.__file__).resolve().parents[1] / "docs/workshop.md").read_text(encoding="utf-8")
        expected = read_expected_values((self.before / "expected_values.md").read_text(encoding="utf-8"))
        self.assertEqual(workshop_value_errors(workshop, expected), [])

    def test_workshop_guard_rejects_changed_or_unmarked_values(self):
        expected = read_expected_values((self.before / "expected_values.md").read_text(encoding="utf-8"))
        valid = '<span data-expected="site_count">30</span> sites ; <span data-expected="clean_rows">10\u202f840</span> lignes'
        self.assertEqual(workshop_value_errors(valid, expected), [])
        for altered in (
            valid.replace('>30<', '>27<'),
            valid.replace('10\u202f840', '110840'),
            valid.replace('data-expected="site_count"', 'data-expected="unknown_count"'),
            valid + ' ; 10 841 observations',
            valid + ' ; 27 sites',
            valid + ' ; 0,056 kgCO2e par kWh',
            valid + ' ; seuil `10000`',
            valid + ' ; une seule ligne de facteurs',
        ):
            with self.subTest(workshop=altered):
                self.assertTrue(workshop_value_errors(altered, expected))
        changed_generation = dict(expected, site_count=Decimal(31))
        self.assertTrue(workshop_value_errors(valid, changed_generation))

    def test_alert_states_do_not_modify_historical_files(self):
        for name in ("sites.csv", "emission_factors.csv", "consumption_2025.csv",
                     "consumption_latest_day_before.csv", "consumption_latest_day_after.csv"):
            with self.subTest(file=name):
                self.assertEqual((self.before / name).read_bytes(), (self.after / name).read_bytes())
        self.assertEqual((self.before / "consumption_latest_day.csv").read_bytes(),
                         (self.before / "consumption_latest_day_before.csv").read_bytes())
        self.assertEqual((self.after / "consumption_latest_day.csv").read_bytes(),
                         (self.after / "consumption_latest_day_after.csv").read_bytes())

    def test_exactly_one_region_crosses_alert_threshold(self):
        self.assertEqual(generator.ALERT_THRESHOLD_KWH, Decimal("10000"))
        before = generator.regional_energy(generator.read_csv(self.before / "consumption_latest_day.csv"), self.sites)
        after = generator.regional_energy(generator.read_csv(self.after / "consumption_latest_day.csv"), self.sites)
        self.assertTrue(all(value < generator.ALERT_THRESHOLD_KWH for value in before.values()))
        crossed = [region for region, value in after.items() if value > generator.ALERT_THRESHOLD_KWH]
        self.assertEqual(crossed, ["Bretagne"])
        self.assertEqual((before["Bretagne"], after["Bretagne"]), (Decimal("2724.55"), Decimal("36724.55")))

    def test_observed_totals_and_carbon(self):
        electricity = sum(Decimal(row["kwh_elec"]) for row in self.cleaned)
        gas = sum(Decimal(row["kwh_gas"]) for row in self.cleaned)
        self.assertEqual(electricity, Decimal("2896164.51"))
        self.assertEqual(gas, Decimal("1686455.14"))
        carbon = electricity * Decimal("0.055") + gas * Decimal("0.205")
        self.assertEqual(generator.french_number(carbon), "505 012,35")
        by_id = {site["site_id"]: site for site in self.sites}
        monthly_region = {(by_id[row["site_id"]]["region"], row["date"][:7]) for row in self.cleaned}
        self.assertEqual(len(monthly_region), 72)

    def test_peaks_openings_and_answer_questions(self):
        actual_peaks = {(row["site_id"], row["date"]) for row in self.cleaned if generator.energy(row) > 20000}
        self.assertEqual(actual_peaks, generator.PEAKS)
        self.assertEqual(sum(site["opening_date"] <= "2025-01-01" for site in self.sites), 27)
        self.assertEqual({row["year"] for row in self.cleaned}, {"2025"})
        answers = (self.before / "questions_expected_answers.md").read_text(encoding="utf-8")
        for number, question in enumerate(generator.QUESTIONS, start=1):
            self.assertIn(f"## Q{number}. {question}", answers)
        self.assertIn("Impossible à calculer : les données de 2024 sont absentes.", answers)


if __name__ == "__main__":
    unittest.main()