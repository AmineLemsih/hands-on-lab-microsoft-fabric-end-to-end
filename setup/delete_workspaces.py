"""Supprimer uniquement les workspaces créés dans le journal, après confirmation."""

import argparse
import sys
from pathlib import Path

from create_workspaces import ApiClient, Journal, Tokens, authentication_arguments, guid, read_journal


def deletion_candidates(rows, include_common=False):
    candidates = {}
    for row in rows:
        if row["resource_type"] != "Workspace":
            continue
        resource_id = guid(row["resource_id"])
        if row["event"] == "created":
            if row["scope"] not in ("common", "participant"):
                raise ValueError("Périmètre de journal inconnu.")
            if not row["marker"].startswith("fabric-labs:energy:"):
                raise ValueError("Le journal contient un marqueur non reconnu.")
            if row["workspace_id"] != resource_id:
                raise ValueError("Identifiants incohérents dans le journal.")
            if row["scope"] == "participant" or include_common:
                candidates[resource_id] = row
        elif row["event"] == "deleted":
            candidates.pop(resource_id, None)
    return list(candidates.values())


def delete_candidates(client, journal, candidates):
    checked = []
    for row in candidates:
        response = client.request("GET", f"/workspaces/{row['resource_id']}", expected=(200, 404))
        if response.status_code == 404:
            checked.append((row, False))
            continue
        workspace = response.json()
        if workspace.get("description") != row["marker"] or workspace.get("displayName") != row["display_name"]:
            raise ValueError(f"{row['display_name']} a changé de nom ou de marqueur ; aucune suppression lancée.")
        checked.append((row, True))
    for row, exists in checked:
        if exists:
            client.request("DELETE", f"/workspaces/{row['resource_id']}", expected=(200, 404))
        journal.record("deleted", "Workspace", row["resource_id"], row["workspace_id"],
                       row["display_name"], row["scope"], row["marker"])
        print(f"Supprimé ou déjà absent : {row['display_name']}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--journal", type=Path, default=Path("setup/workspaces.csv"))
    parser.add_argument("--include-common", action="store_true", help="Inclure le workspace commun seulement s'il a été créé par le script")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--dry-run", action="store_true")
    parser.add_argument("--confirm", help="Confirmation littérale : DELETE")
    authentication_arguments(parser)
    args = parser.parse_args(argv)
    if not args.journal.is_file():
        parser.error("Journal absent ; aucune suppression possible.")
    if args.apply and args.confirm != "DELETE":
        parser.error("La suppression exige --apply --confirm DELETE.")
    candidates = deletion_candidates(read_journal(args.journal), args.include_common)
    for row in candidates:
        print(f"Plan de suppression : {row['display_name']} ({row['resource_id']})")
    print(f"{len(candidates)} workspace(s) concerné(s). Les espaces réutilisés sont conservés.")
    if not args.apply or not candidates:
        print("Aucune écriture ni connexion. La capacité et le groupe Entra ne sont jamais supprimés.")
        return 0
    with Journal(args.journal) as journal:
        current = deletion_candidates(journal.rows, args.include_common)
        if current != candidates:
            raise ValueError("Journal modifié depuis le plan ; relancez la simulation.")
        client = ApiClient(Tokens(args.tenant_id, args.client_id))
        delete_candidates(client, journal, candidates)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, RuntimeError) as error:
        print(f"Arrêt : {error}", file=sys.stderr)
        sys.exit(1)