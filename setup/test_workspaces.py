"""Tests hors ligne : aucun appel à Fabric ni à Microsoft Graph."""

import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import create_workspaces as create
import delete_workspaces as delete


WORKSPACE_ID = "11111111-1111-4111-8111-111111111111"
CAPACITY_ID = "22222222-2222-4222-8222-222222222222"
PRINCIPAL_ID = "33333333-3333-4333-8333-333333333333"
OPERATION_ID = "44444444-4444-4444-8444-444444444444"
MARKER = "fabric-labs:energy:test"


def response(status=200, body=None, headers=None):
    result = Mock(status_code=status, headers=headers or {})
    result.json.return_value = body or {}
    return result


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def participants(self, rows):
        path = self.root / "participants.csv"
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(["email", "first_name"])
            writer.writerows(rows)
        return path

    def test_dry_run_does_not_construct_client_or_write_journal(self):
        path = self.participants([("camille@example.invalid", "Camille")])
        journal = self.root / "workspaces.csv"
        with patch.object(create, "ApiClient") as client:
            self.assertEqual(create.main([
                "--participants", str(path), "--capacity-id", CAPACITY_ID,
                "--participants-group-id", PRINCIPAL_ID, "--journal", str(journal),
            ]), 0)
        client.assert_not_called()
        self.assertFalse(journal.exists())

    def test_duplicate_normalized_names_are_rejected(self):
        path = self.participants([("élodie@example.invalid", "Élodie"), ("elodie@other.invalid", "Autre")])
        with self.assertRaisesRegex(ValueError, "Doublon"):
            create.load_participants(path, "ws-lab-")

    def test_names_use_email_not_first_name(self):
        path = self.participants([("camille.martin@example.invalid", "Camille"), ("camille.dupont@example.invalid", "Camille")])
        participants = create.load_participants(path, "ws-lab-")
        self.assertEqual([person["name"] for person in participants], ["ws-lab-camille.martin", "ws-lab-camille.dupont"])

    def test_same_local_part_in_two_domains_is_rejected(self):
        path = self.participants([("samir@example.invalid", "Samir"), ("samir@other.invalid", "Autre")])
        with self.assertRaisesRegex(ValueError, "Doublon"):
            create.load_participants(path, "ws-lab-")

    def test_clone_option_fails_before_any_remote_operation(self):
        path = self.participants([("camille@example.invalid", "Camille")])
        with patch.object(create, "ApiClient") as client:
            with self.assertRaisesRegex(ValueError, "Clonage non implémenté"):
                create.main([
                    "--participants", str(path), "--capacity-id", CAPACITY_ID,
                    "--participants-group-id", PRINCIPAL_ID, "--clone-report", "--apply",
                ])
        client.assert_not_called()

    def test_pagination_keeps_fixed_host(self):
        session = Mock()
        session.request.side_effect = [
            response(body={"value": [{"id": 1}], "continuationToken": "next", "continuationUri": "https://example.invalid/"}),
            response(body={"value": [{"id": 2}]}),
        ]
        client = create.ApiClient(Mock(), session)
        client.tokens.get.return_value = "fake-token"
        self.assertEqual(len(client.list_all("/workspaces")), 2)
        self.assertEqual(session.request.call_args.args[1], create.FABRIC_API + "/workspaces")
        self.assertEqual(session.request.call_args.kwargs["params"], {"continuationToken": "next"})
        self.assertFalse(session.request.call_args.kwargs["allow_redirects"])

    def test_lro_reads_result_only_after_success(self):
        client = Mock()
        client.request.side_effect = [
            response(body={"status": "Running"}), response(body={"status": "Succeeded"}),
            response(body={"id": WORKSPACE_ID}),
        ]
        with patch.object(create.time, "sleep"):
            self.assertEqual(create.wait_operation(client, OPERATION_ID)["id"], WORKSPACE_ID)
        self.assertEqual(client.request.call_args.args, ("GET", f"/operations/{OPERATION_ID}/result"))

    def test_created_workspace_is_journaled_before_later_failure(self):
        client = Mock()
        client.request.side_effect = [response(201, {"id": WORKSPACE_ID}), RuntimeError("panne simulée")]
        path = self.root / "workspaces.csv"
        with create.Journal(path) as journal:
            with self.assertRaises(RuntimeError):
                create.ensure_workspace(client, journal, [], "ws-lab-test", "participant", MARKER, CAPACITY_ID)
        self.assertEqual(create.read_journal(path)[0]["event"], "created")

    def test_existing_workspace_and_role_are_not_recreated(self):
        workspace = {"id": WORKSPACE_ID, "displayName": "ws-lab-test", "description": MARKER, "capacityId": CAPACITY_ID}
        client = Mock()
        client.request.return_value = response(body=workspace)
        client.list_all.return_value = [{"principal": {"id": PRINCIPAL_ID}, "role": "Member"}]
        path = self.root / "workspaces.csv"
        with create.Journal(path) as journal:
            create.ensure_workspace(client, journal, [workspace], workspace["displayName"], "participant", MARKER, CAPACITY_ID)
            create.ensure_role(client, WORKSPACE_ID, PRINCIPAL_ID, "User", "Member")
        self.assertEqual(client.request.call_count, 1)
        self.assertEqual(delete.deletion_candidates(create.read_journal(path)), [])

    def test_unmanaged_participant_workspace_is_refused(self):
        workspace = {"id": WORKSPACE_ID, "displayName": "ws-lab-test", "description": "Autre usage", "capacityId": CAPACITY_ID}
        client = Mock()
        client.request.return_value = response(body=workspace)
        with create.Journal(self.root / "workspaces.csv") as journal:
            with self.assertRaises(ValueError):
                create.ensure_workspace(client, journal, [workspace], workspace["displayName"], "participant", MARKER, CAPACITY_ID)
        self.assertEqual(client.request.call_count, 1)

    def test_common_is_protected_and_reruns_preserve_ownership(self):
        path = self.root / "workspaces.csv"
        with create.Journal(path) as journal:
            journal.record("created", "Workspace", WORKSPACE_ID, WORKSPACE_ID, "ws-shared", "common", MARKER)
            journal.record("reused", "Workspace", WORKSPACE_ID, WORKSPACE_ID, "ws-shared", "common", MARKER)
        self.assertEqual(delete.deletion_candidates(create.read_journal(path)), [])
        self.assertEqual(len(delete.deletion_candidates(create.read_journal(path), True)), 1)

    def test_delete_needs_explicit_confirmation_before_authentication(self):
        path = self.root / "workspaces.csv"
        with create.Journal(path) as journal:
            journal.record("created", "Workspace", WORKSPACE_ID, WORKSPACE_ID, "ws-lab-test", "participant", MARKER)
        with patch.object(delete, "ApiClient") as client:
            with self.assertRaises(SystemExit):
                delete.main(["--journal", str(path), "--apply"])
        client.assert_not_called()

    def test_changed_marker_prevents_all_deletions(self):
        client = Mock()
        client.request.return_value = response(body={"displayName": "ws-lab-test", "description": "Autre usage"})
        with create.Journal(self.root / "workspaces.csv") as journal:
            journal.record("created", "Workspace", WORKSPACE_ID, WORKSPACE_ID, "ws-lab-test", "participant", MARKER)
            with self.assertRaises(ValueError):
                delete.delete_candidates(client, journal, delete.deletion_candidates(journal.rows))
        self.assertEqual(client.request.call_args.args[0], "GET")
        self.assertEqual(client.request.call_count, 1)

    def test_missing_workspace_is_marked_deleted_without_delete_request(self):
        client = Mock()
        client.request.return_value = response(404)
        with create.Journal(self.root / "workspaces.csv") as journal:
            journal.record("created", "Workspace", WORKSPACE_ID, WORKSPACE_ID, "ws-lab-test", "participant", MARKER)
            delete.delete_candidates(client, journal, delete.deletion_candidates(journal.rows))
            self.assertEqual(delete.deletion_candidates(journal.rows), [])
        self.assertEqual(client.request.call_count, 1)

    def test_role_mismatch_is_not_silently_overwritten(self):
        client = Mock()
        client.list_all.return_value = [{"principal": {"id": PRINCIPAL_ID}, "role": "Admin"}]
        with self.assertRaises(ValueError):
            create.ensure_role(client, WORKSPACE_ID, PRINCIPAL_ID, "User", "Member")
        client.request.assert_not_called()

    def test_failed_lro_does_not_read_result(self):
        client = Mock()
        client.request.return_value = response(body={"status": "Failed"})
        with self.assertRaises(RuntimeError):
            create.wait_operation(client, OPERATION_ID)
        self.assertEqual(client.request.call_count, 1)

    def test_throttling_obeys_retry_after(self):
        session = Mock()
        session.request.side_effect = [response(429, headers={"Retry-After": "2"}), response(body={"value": []})]
        tokens = Mock()
        tokens.get.return_value = "fake-token"
        client = create.ApiClient(tokens, session)
        with patch.object(create.time, "sleep") as delay:
            self.assertEqual(client.list_all("/workspaces"), [])
        delay.assert_called_once_with(2)

    def test_unknown_retry_delay_stops(self):
        with self.assertRaises(RuntimeError):
            create.retry_after(response(429, headers={"Retry-After": "600"}))


if __name__ == "__main__":
    unittest.main()