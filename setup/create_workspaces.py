"""Préparer les espaces Fabric de l'atelier ; simulation hors ligne par défaut."""

import argparse
import csv
import os
import re
import sys
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
from uuid import UUID


FABRIC_API = "https://api.fabric.microsoft.com/v1"
GRAPH_API = "https://graph.microsoft.com/v1.0"
JOURNAL_FIELDS = (
    "timestamp_utc", "event", "resource_type", "resource_id",
    "workspace_id", "display_name", "scope", "marker",
)


def guid(value):
    try:
        parsed = UUID(value)
    except (ValueError, TypeError, AttributeError) as error:
        raise ValueError("Un identifiant UUID valide est requis.") from error
    if parsed.int == 0:
        raise ValueError("L'identifiant UUID ne peut pas être nul.")
    return str(parsed)


def slug(value):
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    result = re.sub(r"[^a-z0-9._-]+", "-", normalized.lower()).strip("-._")
    if not result or len(result) > 100:
        raise ValueError("La partie locale de l'adresse doit produire un nom de 1 à 100 caractères.")
    return result


def load_participants(path, prefix):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if not {"email", "first_name"}.issubset(reader.fieldnames or []):
            raise ValueError("Le CSV doit contenir les colonnes email,first_name.")
        participants = []
        emails, names, identifiers = set(), set(), set()
        for row in reader:
            if not any(row.values()):
                continue
            email = (row.get("email") or "").strip().lower()
            if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
                raise ValueError(f"Adresse ou UPN invalide à la ligne {reader.line_num}.")
            name = prefix + slug(email.split("@", 1)[0])
            object_id = guid(row["object_id"].strip()) if (row.get("object_id") or "").strip() else ""
            if email in emails or name in names or (object_id and object_id in identifiers):
                raise ValueError("Doublon d'adresse, d'identifiant ou de nom de workspace ; corrigez le CSV.")
            if len(name) > 256:
                raise ValueError("Nom de workspace trop long.")
            emails.add(email)
            names.add(name)
            identifiers.add(object_id)
            participants.append({"email": email, "name": name, "object_id": object_id})
    if not participants:
        raise ValueError("La liste des participants est vide.")
    return participants


def read_journal(path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if tuple(reader.fieldnames or []) != JOURNAL_FIELDS:
            raise ValueError("Journal incompatible ; ne pas le remplacer ni le tronquer.")
        return list(reader)


class Journal:
    def __init__(self, path):
        self.path = path
        self.lock_path = path.with_suffix(path.suffix + ".lock")
        self.rows = []

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.lock_path.open("x").close()
        try:
            self.rows = read_journal(self.path)
        except Exception:
            self.lock_path.unlink()
            raise
        return self

    def __exit__(self, *_args):
        self.lock_path.unlink(missing_ok=True)

    def record(self, event, resource_type, resource_id, workspace_id, name, scope, marker):
        row = dict(zip(JOURNAL_FIELDS, (
            datetime.now(timezone.utc).isoformat(), event, resource_type,
            guid(resource_id), guid(workspace_id), name, scope, marker,
        )))
        new_file = not self.path.exists()
        with self.path.open("a", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=JOURNAL_FIELDS, lineterminator="\n")
            if new_file:
                writer.writeheader()
            writer.writerow(row)
            stream.flush()
            os.fsync(stream.fileno())
        self.rows.append(row)


class Tokens:
    def __init__(self, tenant_id=None, client_id=None):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.credential = None

    def get(self, resource):
        variable = "FABRIC_TOKEN" if resource == "fabric" else "GRAPH_TOKEN"
        token = os.environ.get(variable)
        if token:
            return token.strip()
        if not self.tenant_id or not self.client_id:
            raise ValueError(f"Renseignez {variable} ou --tenant-id et --client-id pour la connexion interactive.")
        if self.credential is None:
            from azure.identity import InteractiveBrowserCredential

            self.credential = InteractiveBrowserCredential(
                tenant_id=guid(self.tenant_id), client_id=guid(self.client_id),
                redirect_uri="http://localhost",
            )
        audience = "https://api.fabric.microsoft.com" if resource == "fabric" else "https://graph.microsoft.com"
        return self.credential.get_token(audience + "/.default").token


class ApiClient:
    def __init__(self, tokens, session=None):
        if session is None:
            import requests

            session = requests.Session()
        self.tokens = tokens
        self.session = session

    def request(self, method, path, payload=None, expected=(200,), params=None, resource="fabric"):
        if not path.startswith("/") or path.startswith("//") or "://" in path:
            raise ValueError("Seuls les chemins relatifs de l'API sont acceptés.")
        base = FABRIC_API if resource == "fabric" else GRAPH_API
        headers = {"Authorization": "Bearer " + self.tokens.get(resource), "Accept": "application/json"}
        for attempt in range(4):
            try:
                response = self.session.request(
                    method, base + path, json=payload, params=params, headers=headers,
                    timeout=(10, 60), allow_redirects=False,
                )
            except Exception as error:
                raise RuntimeError("Transport interrompu. Aucun rejeu automatique ; vérifiez Fabric et le journal avant de relancer.") from error
            if response.status_code == 429 and attempt < 3:
                time.sleep(retry_after(response, 10))
                continue
            if response.status_code not in expected:
                try:
                    body = response.json()
                    code = body.get("errorCode") or body.get("error", {}).get("code", "inconnu")
                except (ValueError, AttributeError):
                    code = "inconnu"
                raise RuntimeError(f"API {resource} : HTTP {response.status_code}, code {code}. Aucun corps ni jeton journalisé.")
            return response
        raise RuntimeError("Limite de tentatives atteinte.")

    def list_all(self, path):
        values, seen = [], set()
        params = None
        while True:
            body = self.request("GET", path, params=params).json()
            values.extend(body["value"])
            token = body.get("continuationToken")
            if not token:
                return values
            if token in seen:
                raise RuntimeError("Jeton de pagination répété ; arrêt de sécurité.")
            seen.add(token)
            params = {"continuationToken": token}


def retry_after(response, default=5):
    seconds = int(response.headers.get("Retry-After", default))
    if not 0 <= seconds <= 120:
        raise RuntimeError("Délai demandé hors de la fenêtre automatique ; relancez plus tard.")
    return seconds


def wait_operation(client, operation_id, delay=0):
    operation_id = guid(operation_id)
    deadline = time.monotonic() + 600
    while time.monotonic() < deadline:
        if delay:
            time.sleep(delay)
        response = client.request("GET", f"/operations/{operation_id}")
        status = response.json().get("status")
        if status == "Succeeded":
            return client.request("GET", f"/operations/{operation_id}/result").json()
        if status in ("Failed", "Cancelled"):
            raise RuntimeError(f"Opération {operation_id} terminée en échec : consultez Fabric avant de relancer.")
        if status not in ("NotStarted", "Running"):
            raise RuntimeError(f"État d'opération non reconnu : {status}.")
        delay = retry_after(response)
    raise RuntimeError(f"Opération {operation_id} encore en cours ; le journal permet de reprendre le suivi.")


def unique_named(items, name):
    matches = [item for item in items if item["displayName"].casefold() == name.casefold()]
    if len(matches) > 1:
        raise ValueError(f"Plusieurs ressources portent le nom {name} ; arrêt sans choix arbitraire.")
    return matches[0] if matches else None


def resolve_participants(client, participants):
    resolved = []
    identifiers = set()
    for participant in participants:
        participant = participant.copy()
        if not participant["object_id"]:
            if participant["email"].startswith("$"):
                raise ValueError("UPN commençant par $ : fournissez la colonne object_id.")
            response = client.request(
                "GET", "/users/" + quote(participant["email"], safe=""),
                params={"$select": "id,userPrincipalName"}, resource="graph",
            )
            participant["object_id"] = guid(response.json()["id"])
        if participant["object_id"] in identifiers:
            raise ValueError("Deux lignes désignent la même identité Entra.")
        identifiers.add(participant["object_id"])
        resolved.append(participant)
    return resolved


def ensure_workspace(client, journal, workspaces, name, scope, marker, capacity_id):
    workspace = unique_named(workspaces, name)
    if workspace:
        workspace_id = guid(workspace["id"])
        workspace = client.request("GET", f"/workspaces/{workspace_id}").json()
        if scope == "participant" and workspace.get("description") != marker:
            raise ValueError(f"{name} ne porte pas le marqueur de cette session et de ce participant ; accès non modifiés.")
        if workspace.get("description") != marker and workspace.get("capacityId") != capacity_id:
            raise ValueError(f"{name} préexiste sur une autre capacité ; déplacement automatique refusé.")
        journal.record("reused", "Workspace", workspace_id, workspace_id, name, scope, marker)
    else:
        workspace = client.request("POST", "/workspaces", {
            "displayName": name, "description": marker, "capacityId": capacity_id,
        }, expected=(201,)).json()
        workspace_id = guid(workspace["id"])
        journal.record("created", "Workspace", workspace_id, workspace_id, name, scope, marker)
        workspaces.append(workspace)
        workspace = client.request("GET", f"/workspaces/{workspace_id}").json()
    if workspace.get("capacityId") != capacity_id:
        client.request("POST", f"/workspaces/{workspace_id}/assignToCapacity", {
            "capacityId": capacity_id,
        }, expected=(202,))
        deadline = time.monotonic() + 300
        while time.monotonic() < deadline:
            workspace = client.request("GET", f"/workspaces/{workspace_id}").json()
            if workspace.get("capacityId") == capacity_id:
                break
            time.sleep(5)
        else:
            raise RuntimeError("Affectation à la capacité encore en cours ; relancez avec le même journal.")
    print(f"Espace prêt : {name}")
    return workspace_id


def ensure_role(client, workspace_id, principal_id, principal_type, role):
    path = f"/workspaces/{workspace_id}/roleAssignments"
    matches = [assignment for assignment in client.list_all(path)
               if assignment["principal"]["id"].lower() == principal_id.lower()]
    if matches:
        if len(matches) != 1 or matches[0]["role"] != role:
            raise ValueError("Rôle direct existant différent : faites valider le changement manuellement.")
        return
    client.request("POST", path, {
        "principal": {"id": principal_id, "type": principal_type}, "role": role,
    }, expected=(201,))


def ensure_lakehouse(client, journal, workspace_id, marker):
    completed = {row["resource_id"] for row in journal.rows if row["event"] == "completed"}
    pending = [row for row in journal.rows if row["event"] == "pending"
               and row["workspace_id"] == workspace_id and row["resource_id"] not in completed]
    for operation in pending:
        lakehouse = wait_operation(client, operation["resource_id"])
        journal.record("created", "Lakehouse", lakehouse["id"], workspace_id, "lh_source", "common", marker)
        journal.record("completed", "Operation", operation["resource_id"], workspace_id, "lh_source", "common", marker)
    path = f"/workspaces/{workspace_id}/lakehouses"
    lakehouse = unique_named(client.list_all(path), "lh_source")
    if lakehouse:
        return lakehouse["id"]
    response = client.request("POST", path, {
        "displayName": "lh_source", "description": marker,
        "creationPayload": {"enableSchemas": True},
    }, expected=(201, 202))
    if response.status_code == 202:
        operation_id = guid(response.headers.get("x-ms-operation-id"))
        journal.record("pending", "Operation", operation_id, workspace_id, "lh_source", "common", marker)
        lakehouse = wait_operation(client, operation_id, retry_after(response))
    else:
        operation_id = None
        lakehouse = response.json()
    journal.record("created", "Lakehouse", lakehouse["id"], workspace_id, "lh_source", "common", marker)
    if operation_id:
        journal.record("completed", "Operation", operation_id, workspace_id, "lh_source", "common", marker)
    return lakehouse["id"]


def authentication_arguments(parser):
    parser.add_argument("--tenant-id", help="Identifiant du tenant pour la connexion interactive")
    parser.add_argument("--client-id", help="Identifiant de l'application publique Entra autorisée")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--participants", type=Path, default=Path("setup/participants.csv"))
    parser.add_argument("--capacity-id", required=True, type=guid)
    parser.add_argument("--participants-group-id", required=True, type=guid)
    parser.add_argument("--role", choices=("Admin", "Member", "Contributor", "Viewer"), default="Member")
    parser.add_argument("--prefix", default="ws-lab-")
    parser.add_argument("--common-name", default="ws-shared")
    parser.add_argument("--session", default="energy-lab")
    parser.add_argument("--journal", type=Path, default=Path("setup/workspaces.csv"))
    parser.add_argument("--clone-report", action="store_true", help="Option réservée, désactivée par défaut ; API de clonage à valider")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="Autoriser les écritures dans Fabric")
    mode.add_argument("--dry-run", action="store_true", help="Simulation hors ligne (défaut)")
    authentication_arguments(parser)
    args = parser.parse_args(argv)
    if not re.fullmatch(r"[a-z0-9-]+", args.session):
        parser.error("--session doit contenir uniquement lettres minuscules, chiffres et tirets.")
    participants = load_participants(args.participants, args.prefix)
    if not args.common_name.strip() or len(args.common_name) > 256:
        parser.error("Nom du workspace commun invalide.")
    if any(person["name"].casefold() == args.common_name.casefold() for person in participants):
        parser.error("Le workspace commun doit être distinct des espaces participants.")
    for participant in participants:
        print(f"Plan : {participant['name']} ; rôle {args.role} ; capacité demandée")
    print(f"Plan : {args.common_name} ; groupe participants Viewer ; lakehouse lh_source")
    if args.clone_report:
        # TODO vérifier : https://learn.microsoft.com/rest/api/power-bi/reports/clone-report-in-group
        message = "Clonage non implémenté : valider l'API Power BI, son jeton, les droits et l'idempotence avant d'activer cette option."
        if args.apply:
            raise ValueError(message + " Aucune écriture distante lancée.")
        print(message)
    if not args.apply:
        print("Simulation hors ligne : aucun appel réseau, aucune connexion, aucun journal écrit. L'existant n'est pas inspecté.")
        return 0
    client = ApiClient(Tokens(args.tenant_id, args.client_id))
    participants = resolve_participants(client, participants)
    workspaces = client.list_all("/workspaces")
    marker = "fabric-labs:energy:" + args.session
    with Journal(args.journal) as journal:
        common_id = ensure_workspace(client, journal, workspaces, args.common_name, "common", marker, args.capacity_id)
        ensure_role(client, common_id, args.participants_group_id, "Group", "Viewer")
        ensure_lakehouse(client, journal, common_id, marker)
        for participant in participants:
            workspace_id = ensure_workspace(
                client, journal, workspaces, participant["name"], "participant",
                marker + ":" + participant["object_id"], args.capacity_id,
            )
            ensure_role(client, workspace_id, participant["object_id"], "User", args.role)
    print("Workspaces prêts. Partagez lh_source avec ReadAll, puis préparez energy_report avec une connexion à identité fixe.")
    print("Le partage ReadAll et les alertes depuis le rapport partagé doivent être validés à J-7 selon le guide animateur.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, RuntimeError) as error:
        print(f"Arrêt : {error}", file=sys.stderr)
        sys.exit(1)