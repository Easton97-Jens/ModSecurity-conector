"""Offline tests for the narrow CodeQL Go version-contract checker."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "ci" / "checks" / "common" / "check-go-version-contract.py"


def load_checker():
    spec = importlib.util.spec_from_file_location("go_version_contract_checker", CHECKER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {CHECKER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


checker = load_checker()


def go_job(
    name: str,
    *,
    setup_reference: str | None = None,
    selector: str = "file",
    extra_with_lines: tuple[str, ...] = (),
) -> str:
    reference = checker.SETUP_GO_REFERENCE if setup_reference is None else setup_reference
    version_line = (
        "          go-version-file: .go-version"
        if selector == "file"
        else "          go-version: '1.26.5'"
    )
    extra_lines = "".join(f"          {line}\n" for line in extra_with_lines)
    return f'''  {name}:
    runs-on: ubuntu-latest
    steps:
      - uses: {reference}
        with:
{version_line}
{extra_lines}          check-latest: false
'''


class GoVersionContractTests(unittest.TestCase):
    def root_with_workflow(self, root: Path, workflow: str, version: str = "1.26.5") -> Path:
        (root / ".github" / "workflows").mkdir(parents=True)
        (root / ".go-version").write_text(f"{version}\n", encoding="utf-8")
        (root / ".github" / "workflows" / "ci-security-codeql.yml").write_text(workflow, encoding="utf-8")
        return root

    def check_json(self, root: Path) -> tuple[int, dict[str, object]]:
        output = io.StringIO()
        with mock.patch.object(checker, "repository_root", return_value=root), contextlib.redirect_stdout(output):
            status = checker.main(["--json"])
        return status, json.loads(output.getvalue())

    def valid_workflow(self) -> str:
        return "name: CodeQL\n\non:\n  workflow_dispatch:\n\njobs:\n" + go_job("envoy-go") + go_job("traefik-go")

    def test_valid_contract_accepts_two_central_selectors(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            status, result = self.check_json(self.root_with_workflow(Path(temporary), self.valid_workflow()))
        self.assertEqual(0, status)
        self.assertEqual("passed", result["status"])
        self.assertEqual("1.26.5", result["version"])
        self.assertEqual([], result["violations"])

    def test_literal_selector_and_unlisted_go_job_are_rejected(self) -> None:
        workflow = (
            "name: CodeQL\n\non:\n  workflow_dispatch:\n\njobs:\n"
            + go_job("envoy-go", selector="literal")
            + go_job("traefik-go")
            + go_job("other-go")
        )
        with tempfile.TemporaryDirectory() as temporary:
            status, result = self.check_json(self.root_with_workflow(Path(temporary), workflow))
        self.assertEqual(2, status)
        self.assertEqual("failed", result["status"])
        self.assertTrue(any("exact central" in entry for entry in result["violations"]))
        self.assertTrue(any("unlisted" in entry for entry in result["violations"]))

    def test_yaml_equivalent_literal_selector_variants_are_rejected(self) -> None:
        variants = {
            "space_before_colon": ("go-version : '1.26.5'",),
            "single_quoted_key": ("'go-version': '1.26.5'",),
            "double_quoted_key": ('"go-version": "1.26.5"',),
            "explicit_mapping_key": ("? go-version", ": '1.26.5'"),
        }
        for name, extra_with_lines in variants.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                workflow = (
                    "name: CodeQL\n\non:\n  workflow_dispatch:\n\njobs:\n"
                    + go_job("envoy-go", extra_with_lines=extra_with_lines)
                    + go_job("traefik-go")
                )
                status, result = self.check_json(
                    self.root_with_workflow(Path(temporary), workflow)
                )
            self.assertEqual(2, status)
            self.assertEqual("failed", result["status"])
            self.assertTrue(any("exact central" in entry for entry in result["violations"]))

    def test_wrong_action_pin_and_invalid_version_file_fail_closed(self) -> None:
        wrong_reference = "actions/setup-go@main"
        workflow = (
            "name: CodeQL\n\non:\n  workflow_dispatch:\n\njobs:\n"
            + go_job("envoy-go", setup_reference=wrong_reference)
            + go_job("traefik-go")
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = self.root_with_workflow(Path(temporary), workflow)
            status, result = self.check_json(root)
            (root / ".go-version").write_text("1.26.05\n", encoding="utf-8")
            bad_status, bad_result = self.check_json(root)
        self.assertEqual(2, status)
        self.assertTrue(any("actions/setup-go" in entry for entry in result["violations"]))
        self.assertEqual((2, "error"), (bad_status, bad_result["status"]))

    def test_setup_go_step_body_ends_at_the_next_step(self) -> None:
        job = go_job("envoy-go") + "      - name: unrelated\n        run: echo unrelated\n"
        steps = checker.setup_go_blocks(job)
        self.assertEqual(1, len(steps))
        self.assertEqual(checker.SETUP_GO_REFERENCE, steps[0].reference)
        self.assertNotIn("unrelated", steps[0].body)

    def test_symlink_version_file_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            outside = root / "outside"
            outside.write_text("1.26.5\n", encoding="utf-8")
            self.root_with_workflow(root, self.valid_workflow())
            (root / ".go-version").unlink()
            (root / ".go-version").symlink_to(outside)
            status, result = self.check_json(root)
        self.assertEqual((2, "error"), (status, result["status"]))


if __name__ == "__main__":
    unittest.main()
