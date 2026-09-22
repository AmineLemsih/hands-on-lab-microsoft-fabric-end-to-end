"""Lister les images locales et synchroniser leurs références selon leur présence."""

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESERVED = {"00-learning-path.svg", "00-architecture.png", "10-recap.svg"}
IMAGE = re.compile(r"^(?P<indent>\s*)(?P<open><!--\s*)?(?P<image>!\[[^\]]*\]\((?P<path>(?:\./)?assets/[^)\s]+)\))(?P<close>\s*-->)?\s*$")


def synchronize(file_path, write=True):
    with file_path.open(encoding="utf-8", newline="") as stream:
        source = stream.read()
    output, records = [], []
    fence = None
    changes = 0
    assets = (file_path.parent / "assets").resolve()
    for number, line in enumerate(source.splitlines(keepends=True), start=1):
        content = line.rstrip("\r\n")
        ending = line[len(content):]
        stripped = content.lstrip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            fence = None if fence == marker else (marker if fence is None else fence)
        match = IMAGE.fullmatch(content) if fence is None else None
        if not match:
            output.append(line)
            continue
        if bool(match["open"]) != bool(match["close"]):
            raise ValueError(f"Commentaire incomplet : {file_path.name}, ligne {number}")
        target = (file_path.parent / match["path"]).resolve()
        if not target.is_relative_to(assets):
            raise ValueError("Une image ne doit pas sortir du dossier assets.")
        present = target.is_file() and target.stat().st_size > 0
        reserved = target.parent == assets and target.name in RESERVED
        should_comment = not present and not reserved
        commented = bool(match["open"])
        if commented != should_comment:
            changes += 1
            image = match["image"]
            content = match["indent"] + (f"<!-- {image} -->" if should_comment else image)
        output.append(content + ending)
        records.append({"file": str(file_path), "line": number, "image": match["path"],
                        "present": present, "active": not should_comment, "reserved": reserved})
    if write and changes:
        with file_path.open("w", encoding="utf-8", newline="") as stream:
            stream.write("".join(output))
    return records, changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Contrôle seul ; code 1 si des références doivent changer")
    parser.add_argument("--summary", action="store_true", help="Afficher seulement les totaux")
    parser.add_argument("files", nargs="*", type=Path, help="Documents Markdown ; défaut : workshop et notes animateur")
    args = parser.parse_args()
    files = args.files or [ROOT / "docs/workshop.md", ROOT / "docs/facilitator-notes.md"]
    records, changes = [], 0
    for file_path in files:
        current, count = synchronize(file_path, write=not args.check)
        records.extend(current)
        changes += count
    if not args.summary:
        for record in records:
            state = "présente" if record["present"] else "manquante"
            reference = "active" if record["active"] else "commentée"
            print(f"{record['image']} : {state}, référence {reference} (ligne {record['line']})")
    present = sum(record["present"] for record in records)
    print(f"{len(records)} références ; {present} présentes ; {len(records) - present} manquantes ; {changes} modification(s).")
    print("Les trois schémas pédagogiques restent actifs, même absents. Aucun fichier image n'est généré.")
    return 1 if args.check and changes else 0


if __name__ == "__main__":
    raise SystemExit(main())