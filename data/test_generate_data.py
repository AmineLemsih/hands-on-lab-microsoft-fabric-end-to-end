"""Contrôler les contrats des données synthétiques sans dépendance externe."""

import re
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

import generate_data as generator


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