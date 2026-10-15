"""NGINX evidence file boundaries; synthetic tests, never host qualification."""

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "ci/runtime/lifecycle/i12/nginx"
RUN_ROOT = Path("/var/tmp/codex/ModSecurity-conector/runs")


def load(name):
    spec = importlib.util.spec_from_file_location("nginx_boundary_" + name, HARNESS / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BUILD = load("build_capture")
REPORT = load("report")
QUALIFY = load("qualify")
REVIEW = load("review_observations")
CONFIG = load("config_controls")


class EvidenceBoundaryTests(unittest.TestCase):
    def setUp(self):
        # Use the same protected external storage as the harness; /tmp fixtures
        # would hide the real ancestry policy these tests need to exercise.
        RUN_ROOT.mkdir(parents=True, exist_ok=True)
        scratch = tempfile.TemporaryDirectory(prefix="nginx-boundary-", dir=RUN_ROOT)
        self.addCleanup(scratch.cleanup)
        self.scratch = Path(scratch.name)
        self.image = self.scratch / "nginx"
        self.image.write_bytes(b"synthetic pinned native image\n")
        self.image.chmod(0o500)

    def test_fresh_build_output_is_private_and_never_reuses_existing_directory(self):
        target = self.scratch / "build" / "fresh"
        self.assertEqual(BUILD.create_private_output(target), target)
        self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o700)
        self.assertEqual(stat.S_IMODE(target.parent.stat().st_mode), 0o700)
        with self.assertRaises(FileExistsError):
            BUILD.create_private_output(target)
        self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o700)

    def test_build_rejects_escape_links_and_writable_ancestors(self):
        with self.assertRaises(ValueError):
            BUILD.create_private_output(Path("/tmp/nginx-i12-untrusted-output"))
        with self.assertRaises(ValueError):
            BUILD.create_private_output(self.scratch / ".." / "escaped")
        link = self.scratch / "linked"
        link.symlink_to(self.scratch, target_is_directory=True)
        with self.assertRaises((OSError, ValueError)):
            BUILD.create_private_output(link / "fresh")
        writable = self.scratch / "writable"
        writable.mkdir(mode=0o777)
        writable.chmod(0o777)
        with self.assertRaises(ValueError):
            BUILD.create_private_output(writable / "fresh")
        self.assertEqual(stat.S_IMODE(writable.stat().st_mode), 0o777)

    def test_report_and_qualifier_accept_protected_regular_evidence(self):
        evidence = self.scratch / "receipt.json"
        evidence.write_text('{"result":"synthetic"}\n')
        self.assertEqual(REPORT.read(evidence), {"result": "synthetic"})
        reference = REPORT.reference(evidence)
        self.assertEqual(reference["sha256"], hashlib.sha256(evidence.read_bytes()).hexdigest())
        self.assertEqual(reference["bytes"], evidence.stat().st_size)
        self.assertEqual(QUALIFY.evidence_path(evidence), evidence)

    def test_evidence_readers_reject_symlinks_writable_files_and_nonfiles(self):
        link = self.scratch / "linked-image"
        link.symlink_to(self.image)
        for reader in (REPORT.evidence_path, QUALIFY.evidence_path):
            for unsafe in (link, self.scratch, Path("/etc/passwd"), self.scratch / ".." / "escape"):
                with self.subTest(reader=reader.__module__, unsafe=unsafe):
                    with self.assertRaises(ValueError):
                        reader(unsafe)
        self.image.chmod(0o666)
        for reader in (REPORT.evidence_path, QUALIFY.evidence_path):
            with self.assertRaises(ValueError):
                reader(self.image)

    def test_nested_reference_cannot_smuggle_an_external_file(self):
        with self.assertRaises(ValueError):
            QUALIFY.validate_references({"observations": [{"reference": {
                "path": "/etc/passwd", "sha256": "0" * 64}}]})

    def test_report_publication_is_limited_to_its_exact_tracked_destination(self):
        name = "ci/runtime/lifecycle/i12/nginx/evidence-20261015.json"
        self.assertEqual(REPORT.output_path(ROOT / name, name), ROOT / name)
        for destination in (self.scratch / "report.json", ROOT / "docs/unrelated.md",
                            ROOT / "docs/../" / name):
            with self.subTest(destination=destination):
                with self.assertRaises(ValueError):
                    REPORT.output_path(destination, name)

    def test_approved_packet_destination_must_be_fresh_and_protected(self):
        destination = self.scratch / "new" / "approved"
        self.assertEqual(QUALIFY.publication_path(destination), destination)
        with self.assertRaises(ValueError):
            QUALIFY.publication_path(self.scratch)
        with self.assertRaises(ValueError):
            QUALIFY.publication_path(Path("/tmp/nginx-i12-approved"))
        link = self.scratch / "linked"
        link.symlink_to(self.scratch, target_is_directory=True)
        with self.assertRaises(ValueError):
            QUALIFY.publication_path(link / "approved")
        self.scratch.chmod(0o777)
        self.addCleanup(self.scratch.chmod, 0o700)
        with self.assertRaises(ValueError):
            QUALIFY.publication_path(self.scratch / "approved")

    def test_verification_projection_hash_binds_full_inventory_without_exposing_paths(self):
        hashes = {"private/operator/forwardauth.c": "1" * 64, "private/build.c": "2" * 64}
        source = {"checks": [{"name": "native", "status": "PASS"}], "input_sha256": hashes}
        projected = REPORT.public_summary(source)
        self.assertNotIn("input_sha256", projected)
        self.assertNotIn("private/operator", json.dumps(projected))
        self.assertEqual(projected["input_sha256_count"], 2)
        canonical = json.dumps(hashes, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        self.assertEqual(projected["input_sha256_set_sha256"], hashlib.sha256(canonical).hexdigest())
        changed = {**source, "input_sha256": {**hashes, "private/build.c": "3" * 64}}
        self.assertNotEqual(REPORT.public_summary(changed)["input_sha256_set_sha256"],
                            projected["input_sha256_set_sha256"])

    def test_selected_contract_projection_binds_source_inventory_without_exposing_paths(self):
        hashes = {"parent:connectors/traefik/forwardauth.c": "1" * 64}
        source = {"expected_phase": "P2", "original_source_hashes": hashes}
        projected = REPORT.public_selected_requirement(source)
        self.assertEqual(projected["expected_phase"], "P2")
        self.assertNotIn("original_source_hashes", projected)
        self.assertNotIn("forwardauth", json.dumps(projected))
        self.assertEqual(projected["original_source_hashes_count"], 1)
        self.assertEqual(projected["original_source_hashes_set_sha256"], REPORT.canonical_hash(hashes))

    def test_loaded_image_hashes_regular_protected_file_and_rejects_links_and_writable_image(self):
        metadata, digest = REVIEW.protected_image(self.image)
        self.assertEqual(metadata.st_size, self.image.stat().st_size)
        self.assertEqual(digest, hashlib.sha256(self.image.read_bytes()).hexdigest())
        link = self.scratch / "linked"
        link.symlink_to(self.image)
        with self.assertRaises((ValueError, OSError)):
            REVIEW.protected_image(link)
        self.image.chmod(0o666)
        with self.assertRaises(ValueError):
            REVIEW.protected_image(self.image)

    def test_loaded_image_rejects_writable_ancestry_and_fifo_without_blocking(self):
        fifo = self.scratch / "not-an-image"
        os.mkfifo(fifo, mode=0o600)
        with self.assertRaises(ValueError):
            REVIEW.protected_image(fifo)
        self.scratch.chmod(0o777)
        self.addCleanup(self.scratch.chmod, 0o700)
        with self.assertRaises(ValueError):
            REVIEW.protected_image(self.image)

    def test_namespace_worker_and_project_paths_resolve_to_distinct_backing_trees(self):
        admission = {"bindings": [{"target": "/mnt/artifacts", "source": str(self.scratch / "artifacts")},
                                   {"target": "/mnt", "source": str(self.scratch / "generic")}]}
        attempt = self.scratch / "attempt"
        self.assertEqual(REVIEW.physical("/var/tmp/codex/ModSecurity-nginx-i12/nginx-i12-x/payload.txt",
                                        attempt, admission),
                         attempt / "data/nginx-worker-runtime/nginx-i12-x/payload.txt")
        self.assertEqual(REVIEW.physical("/var/tmp/codex/ModSecurity-conector/results/receipt.json",
                                        attempt, admission), attempt / "data/results/receipt.json")
        self.assertEqual(REVIEW.physical("/mnt/artifacts/native/nginx", attempt, admission),
                         self.scratch / "artifacts/native/nginx")
        for invalid in ("/mnt/artifacts/../outside", "relative/image", "/mnt//artifacts/image"):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    REVIEW.physical(invalid, attempt, admission)

    def test_configuration_arguments_must_be_canonical_owned_paths(self):
        self.assertEqual(CONFIG.trusted_path(self.image), self.image)
        self.assertEqual(CONFIG.trusted_path(self.scratch, directory=True), self.scratch)
        self.assertEqual(CONFIG.trusted_path(self.scratch / "fresh", fresh=True), self.scratch / "fresh")
        for unsafe in (str(self.image) + ';daemon on;', str(self.image) + '\nload_module bad;',
                       str(self.image) + "$(id)", "/etc/passwd", self.scratch / ".." / "escape"):
            with self.subTest(unsafe=unsafe):
                with self.assertRaises(ValueError):
                    CONFIG.trusted_path(unsafe)
        link = self.scratch / "linked"
        link.symlink_to(self.image)
        with self.assertRaises(ValueError):
            CONFIG.trusted_path(link)
        self.image.chmod(0o666)
        with self.assertRaises(ValueError):
            CONFIG.trusted_path(self.image)


if __name__ == "__main__":
    unittest.main()
