"""Générer et contrôler les données synthétiques de l'atelier Contoso."""

import argparse
import csv
import math
import random
from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path


SEED = 2025
YEAR = 2025
LAST_DAY = date(YEAR, 12, 31)
ALERT_THRESHOLD_KWH = Decimal("20000")
REGIONS = (
    "Île-de-France",
    "Auvergne-Rhône-Alpes",
    "Hauts-de-France",
    "Nouvelle-Aquitaine",
    "Occitanie",
    "Bretagne",
)
ACTIVITIES = ("office", "warehouse", "factory", "branch")
FIELDS = (
    "site_id", "date", "year", "kwh_elec", "kwh_gas", "avg_temp"
)
PEAKS = {
    ("S003", "2025-01-15"),
    ("S007", "2025-03-12"),
    ("S012", "2025-06-18"),
    ("S018", "2025-08-21"),
    ("S024", "2025-11-14"),
    ("S030", "2025-12-31"),
}
QUESTIONS = (
    "Quelle est la consommation électrique totale observée en 2025, en kWh ?",
    "Quelle région émet le plus de kgCO2e en 2025, électricité et gaz réunis ?",
    "Quel mois de 2025 a la consommation totale la plus élevée, en kWh ?",
    "Quels couples site et jour dépassent 20 000 kWh, électricité et gaz réunis, en 2025 ?",
    "Combien de sites étaient actifs au 1er janvier 2025 ?",
    "De quel pourcentage nos émissions ont-elles baissé entre 2024 et 2025 ?",
)


def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def make_sites(generator):
    sites = []
    openings = {28: "2025-03-15", 29: "2025-07-01", 30: "2025-10-01"}
    for number in range(1, 31):
        activity = ACTIVITIES[(number - 1) % len(ACTIVITIES)]
        surface = generator.randint(700, 4500)
        if activity in ("warehouse", "factory"):
            surface *= 3
        sites.append({
            "site_id": f"S{number:03d}",
            "site_name": f"Contoso site {number:02d}",
            "region": REGIONS[(number - 1) % len(REGIONS)],
            "activity": activity,
            "area_m2": surface,
            "opening_date": openings.get(
                number, date(2012 + number % 12, 1 + number % 12, 1).isoformat()
            ),
        })
    return sites


def make_consumption(sites, generator):
    rows = []
    reference_day = []
    electric_intensity = {"office": 0.055, "warehouse": 0.035, "factory": 0.095, "branch": 0.045}
    for day_offset in range(365):
        current_day = date(YEAR, 1, 1) + timedelta(days=day_offset)
        seasonal_temperature = 12 - 10 * math.cos(2 * math.pi * (day_offset - 15) / 365)
        for site in sites:
            temperature = seasonal_temperature + generator.uniform(-3, 3)
            weekend_factor = 0.62 if current_day.weekday() >= 5 else 1.0
            active = current_day.isoformat() >= site["opening_date"]
            electricity = (
                site["area_m2"] * electric_intensity[site["activity"]]
                * (1 + max(temperature - 22, 0) * 0.04)
                * weekend_factor * generator.uniform(0.88, 1.12)
            ) if active else 0.0
            gas = (
                site["area_m2"] * 0.006 * max(18 - temperature, 0)
                * weekend_factor * generator.uniform(0.90, 1.10)
            ) if active else 0.0
            record = {
                "site_id": site["site_id"],
                "date": current_day.isoformat(),
                "year": str(YEAR),
                "kwh_elec": f"{electricity:.2f}",
                "kwh_gas": f"{gas:.2f}",
                "avg_temp": f"{temperature:.2f}",
            }
            if current_day == LAST_DAY:
                reference_day.append(record.copy())
            if (site["site_id"], current_day.isoformat()) in PEAKS:
                record["kwh_elec"] = f"{electricity + 25000:.2f}"
                record["kwh_gas"] = f"{gas + 9000:.2f}"
            rows.append(record)
    return rows, reference_day


def add_quality_defects(rows, generator):
    eligible = [
        index for index, row in enumerate(rows)
        if (row["site_id"], row["date"]) not in PEAKS
        and row["date"] != LAST_DAY.isoformat()
    ]
    defect_count = round(len(rows) * 0.01)
    for position, index in enumerate(generator.sample(eligible, defect_count)):
        if position < defect_count // 2:
            rows[index] = dict.fromkeys(FIELDS, "")
        else:
            rows[index]["kwh_elec"] = "invalid"


def clean_rows(rows):
    cleaned = []
    blank_count = 0
    invalid_count = 0
    for row in rows:
        if not any(row.values()):
            blank_count += 1
            continue
        try:
            date.fromisoformat(row["date"])
            int(row["year"])
            for field in ("kwh_elec", "kwh_gas", "avg_temp"):
                if not Decimal(row[field]).is_finite():
                    raise ValueError("Valeur non finie")
        except (ValueError, InvalidOperation):
            invalid_count += 1
            continue
        cleaned.append(row)
    return cleaned, blank_count, invalid_count


def energy(row):
    return Decimal(row["kwh_elec"]) + Decimal(row["kwh_gas"])


def regional_energy(rows, sites):
    by_id = {site["site_id"]: site for site in sites}
    totals = defaultdict(Decimal)
    for row in rows:
        totals[by_id[row["site_id"]]["region"]] += energy(row)
    return totals


def french_number(value):
    rounded = Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"{rounded:,.2f}".replace(",", " ").replace(".", ",")


def validate_output(output, latest_state="before"):
    sites = read_csv(output / "sites.csv")
    factors = read_csv(output / "emission_factors.csv")
    raw = read_csv(output / "consumption_2025.csv")
    current = read_csv(output / "consumption_latest_day.csv")
    before = read_csv(output / "consumption_latest_day_before.csv")
    after = read_csv(output / "consumption_latest_day_after.csv")
    cleaned, blank_count, invalid_count = clean_rows(raw)
    actual_peaks = {
        (row["site_id"], row["date"]) for row in cleaned if energy(row) > ALERT_THRESHOLD_KWH
    }
    site_ids = {site["site_id"] for site in sites}
    before_totals = regional_energy(before, sites)
    after_totals = regional_energy(after, sites)
    snapshot_valid = lambda snapshot: (
        len(snapshot) == 30
        and {row["site_id"] for row in snapshot} == site_ids
        and all(row["date"] == LAST_DAY.isoformat() for row in snapshot)
        and clean_rows(snapshot)[1:] == (0, 0)
    )
    checks = {
        "30 sites uniques": len(sites) == len(site_ids) == 30,
        "1 ligne de facteurs, 2 énergies": len(factors) == 1 and factors[0]["year"] == "2025",
        "10 950 lignes brutes": len(raw) == 10950,
        "55 lignes vides et 55 erreurs de type": blank_count == invalid_count == 55,
        "10 840 lignes propres": len(cleaned) == 10840,
        "clés site/jour uniques": len({(row["site_id"], row["date"]) for row in cleaned}) == len(cleaned),
        "références de sites valides": all(row["site_id"] in site_ids for row in cleaned),
        "six pics protégés": actual_peaks == PEAKS,
        "trois instantanés de 30 sites au 31 décembre 2025": all(
            snapshot_valid(snapshot) for snapshot in (current, before, after)
        ),
        "toutes les régions sous le seuil avant": all(total < ALERT_THRESHOLD_KWH for total in before_totals.values()),
        "exactement une région au-dessus du seuil après": sum(total > ALERT_THRESHOLD_KWH for total in after_totals.values()) == 1,
        "seul S030 change entre les instantanés": [
            first["site_id"] for first, second in zip(before, after) if first != second
        ] == ["S030"],
        "instantané actif conforme au paramètre": current == (before if latest_state == "before" else after),
        "après identique au dernier jour historique": after == [row for row in cleaned if row["date"] == LAST_DAY.isoformat()],
        "365 jours de 2025 représentés": {row["date"] for row in cleaned} == {
            (date(YEAR, 1, 1) + timedelta(days=offset)).isoformat() for offset in range(365)
        },
        "année cohérente avec les dates": all(row["year"] == row["date"][:4] for row in cleaned),
    }
    for label, passed in checks.items():
        if not passed:
            raise ValueError(f"Contrôle échoué : {label}")
        print(f"OK : {label}")
    return sites, factors[0], cleaned


def write_answers(output, sites, factors, cleaned, scenario):
    by_id = {site["site_id"]: site for site in sites}
    region_carbon = defaultdict(Decimal)
    month_energy = defaultdict(Decimal)
    electricity = Decimal(0)
    gas = Decimal(0)
    for row in cleaned:
        elec_value = Decimal(row["kwh_elec"])
        gas_value = Decimal(row["kwh_gas"])
        electricity += elec_value
        gas += gas_value
        region = by_id[row["site_id"]]["region"]
        region_carbon[region] += (
            elec_value * Decimal(factors["elec_kgco2e_per_kwh"])
            + gas_value * Decimal(factors["gas_kgco2e_per_kwh"])
        )
        month_energy[row["date"][:7]] += energy(row)
    top_region = max(region_carbon, key=region_carbon.get)
    top_month = max(month_energy, key=month_energy.get)
    active_sites = sum(site["opening_date"] <= "2025-01-01" for site in sites)
    peaks = sorted(
        (row for row in cleaned if energy(row) > ALERT_THRESHOLD_KWH),
        key=lambda row: (-energy(row), row["site_id"], row["date"]),
    )
    lines = [
        "# Questions et réponses attendues",
        "",
        "Résultats calculés sur les CSV relus après écriture, après suppression des lignes vides et des erreurs.",
        "Aucune imputation. Les 110 observations rejetées sont manquantes, pas égales à zéro.",
        "Les facteurs sont fictifs : aucun bilan réglementaire ne peut être produit avec ces données.",
        "",
        f"Graine : {SEED}. Année civile : {YEAR}. Lignes propres : {len(cleaned)}.",
        f"Dernier jour disponible : {LAST_DAY.isoformat()}. Instantané actif : {scenario}.",
        "Les réponses historiques ne dépendent pas du scénario de l'instantané.",
        "",
        f"## Q1. {QUESTIONS[0]}",
        "",
        f"**{french_number(electricity)} kWh électriques** observés.",
        f"Contrôle : gaz = {french_number(gas)} kWh ; total = {french_number(electricity + gas)} kWh.",
        "",
        f"## Q2. {QUESTIONS[1]}",
        "",
        f"**{top_region} : {french_number(region_carbon[top_region])} kgCO2e**.",
        f"Total toutes régions : {french_number(sum(region_carbon.values()))} kgCO2e.",
        "Calcul par observation : kWh électriques x 0,055 + kWh gaz x 0,205 ; arrondi après la somme.",
        "",
        "| Région | kgCO2e |",
        "| --- | ---: |",
    ]
    lines.extend(
        f"| {region} | {french_number(carbon)} |"
        for region, carbon in sorted(region_carbon.items(), key=lambda item: (-item[1], item[0]))
    )
    lines.extend([
        "", f"## Q3. {QUESTIONS[2]}", "",
        f"**{top_month} : {french_number(month_energy[top_month])} kWh**.",
        "", "| Mois | kWh totaux |", "| --- | ---: |",
    ])
    lines.extend(f"| {month} | {french_number(total)} |" for month, total in sorted(month_energy.items()))
    lines.extend([
        "", f"## Q4. {QUESTIONS[3]}", "", "**Six couples site/jour**, pas six régions.",
        "", "| Site | Date | kWh totaux |", "| --- | --- | ---: |",
    ])
    lines.extend(f"| {row['site_id']} | {row['date']} | {french_number(energy(row))} |" for row in peaks)
    lines.extend([
        "", f"## Q5. {QUESTIONS[4]}", "", f"**{active_sites} sites actifs**.",
        "Un site est actif si sa date de mise en service est antérieure ou égale à la date demandée.",
        "Aucune fermeture n'est modélisée. Il y a 30 sites dans le référentiel, dont trois ouverts pendant 2025.",
        "", f"## Q6. {QUESTIONS[5]}", "",
        "**Impossible à calculer : les données de 2024 sont absentes.** Ne pas inventer de pourcentage ni supposer zéro.",
        "Demander les consommations et les facteurs de 2024, puis vérifier que les périmètres sont comparables.",
        "", "## Contrôle de l'alerte", "",
        "L'instantané est le 31 décembre 2025, pas la date système. Ne pas filtrer le rapport sur AUJOURDHUI().",
        "Le fichier consumption_latest_day_before.csv retire le pic de S030 de l'instantané uniquement ; consumption_latest_day_after.csv le rétablit.",
        "Remplacer le fichier actif consumption_latest_day.csv, recharger la table puis actualiser le modèle sémantique.",
        f"Seuil de démonstration par région : {french_number(ALERT_THRESHOLD_KWH)} kWh, comparaison strictement supérieure.",
        "Ne pas modifier le CSV annuel pendant ce test. Mesurer la latence en répétition, prévoir une capture.",
        "", "| Région | Avant, kWh | Après, kWh |", "| --- | ---: | ---: |",
    ])
    before = regional_energy(read_csv(output / "consumption_latest_day_before.csv"), sites)
    after = regional_energy(read_csv(output / "consumption_latest_day_after.csv"), sites)
    lines.extend(f"| {region} | {french_number(before[region])} | {french_number(after[region])} |" for region in sorted(before))
    lines.extend([
        "",
    ])
    (output / "questions_expected_answers.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent / "out", help="Dossier de sortie")
    parser.add_argument("--latest-state", choices=("before", "after"), default="before", help="État du fichier actif pour l'alerte")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    generator = random.Random(SEED)
    sites = make_sites(generator)
    factors = [{
        "year": str(YEAR),
        "elec_kgco2e_per_kwh": "0.055",
        "gas_kgco2e_per_kwh": "0.205",
        "source": "fictif, ne pas utiliser pour un reporting réel",
    }]
    rows, reference_day = make_consumption(sites, generator)
    latest_day = [
        row.copy() for row in rows if row["date"] == LAST_DAY.isoformat()
    ]
    current = reference_day if args.latest_state == "before" else latest_day
    add_quality_defects(rows, generator)
    write_csv(args.out / "sites.csv", sites, sites[0].keys())
    write_csv(args.out / "emission_factors.csv", factors, factors[0].keys())
    write_csv(args.out / "consumption_2025.csv", rows, FIELDS)
    write_csv(args.out / "consumption_latest_day_before.csv", reference_day, FIELDS)
    write_csv(args.out / "consumption_latest_day_after.csv", latest_day, FIELDS)
    write_csv(args.out / "consumption_latest_day.csv", current, FIELDS)
    loaded_sites, loaded_factors, cleaned = validate_output(args.out, args.latest_state)
    write_answers(args.out, loaded_sites, loaded_factors, cleaned, args.latest_state)
    print(f"Données et six réponses calculées dans {args.out}")


if __name__ == "__main__":
    main()