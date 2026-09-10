from __future__ import annotations

import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from tests.version_updater_test_support import load_updater


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "update-go-components.py"
updater = load_updater("update_go_components", SCRIPT)

BASELINE_SYS = "v0.46.0"
BASELINE_NET = "v0.56.0"
BASELINE_TEXT = "v0.39.0"
TARGET_SYS = "v0.47.0"
TARGET_NET = "v0.58.0"
TARGET_TEXT = "v0.41.0"


def go_mod(
    grpc_version: str,
    *,
    sys_version: str = BASELINE_SYS,
    net_version: str = BASELINE_NET,
    text_version: str = BASELINE_TEXT,
) -> str:
    return f"""module github.com/Easton97-Jens/ModSecurity-conector/connectors/envoy/ext_proc

go 1.26.5

require (
\tgithub.com/envoyproxy/go-control-plane/envoy v1.37.0
\tgolang.org/x/sys {sys_version}
\tgoogle.golang.org/grpc {grpc_version}
\tgoogle.golang.org/protobuf v1.36.11
)

require (
\tgolang.org/x/net {net_version} // indirect
\tgolang.org/x/text {text_version} // indirect
)
"""


def checksum_entries(
    grpc_version: str,
    *,
    sys_version: str,
    net_version: str,
    text_version: str,
) -> str:
    return "".join(
        f"{module} {version}{suffix} {checksum_for(module, version, suffix, token)}\n"
        for module, version, token in (
            ("golang.org/x/net", net_version, "net"),
            ("golang.org/x/sys", sys_version, "sys"),
            ("golang.org/x/text", text_version, "text"),
            ("google.golang.org/grpc", grpc_version, "grpc"),
        )
        for suffix in ("", "/go.mod")
    )


def checksum_for(module: str, version: str, suffix: str, token: str) -> str:
    return updater.TRUSTED_TARGET_GO_SUM_ENTRIES.get(
        (module, version, suffix),
        f"h1:{token}=",
    )


def baseline_go_sum(*, extra: str = "") -> str:
    return (
        "github.com/envoyproxy/go-control-plane/envoy v1.37.0 h1:envoy=\n"
        "google.golang.org/protobuf v1.36.11 h1:protobuf=\n"
        + checksum_entries(
            "v1.83.1",
            sys_version=BASELINE_SYS,
            net_version=BASELINE_NET,
            text_version=BASELINE_TEXT,
        )
        + extra
    )


def candidate_go_sum(
    grpc_version: str = "v1.83.2",
    *,
    sys_version: str = TARGET_SYS,
    net_version: str = TARGET_NET,
    text_version: str = TARGET_TEXT,
    extra: str = "",
) -> str:
    return (
        baseline_go_sum()
        + checksum_entries(
            grpc_version,
            sys_version=sys_version,
            net_version=net_version,
            text_version=text_version,
        )
        + extra
    )


def target_go_mod(grpc_version: str = "v1.83.2") -> str:
    return go_mod(
        grpc_version,
        sys_version=TARGET_SYS,
        net_version=TARGET_NET,
        text_version=TARGET_TEXT,
    )


class UpdateGoComponentsTests(unittest.TestCase):
    def root_with_module(
        self,
        root: Path,
        *,
        go_mod_source: str | None = None,
        go_sum_source: str | None = None,
    ) -> Path:
        module = root / "connectors" / "envoy" / "ext_proc"
        module.mkdir(parents=True)
        (module / "go.mod").write_text(go_mod_source or go_mod("v1.83.1"), encoding="utf-8")
        (module / "go.sum").write_text(go_sum_source or baseline_go_sum(), encoding="utf-8")
        return root

    def run_cli(
        self,
        root: Path,
        argv: list[str],
        *,
        baseline_frame: bytes = b"",
    ) -> tuple[int, dict[str, object]]:
        output = io.StringIO()
        status = updater.main(
            argv,
            root=root,
            output=output,
            input_stream=io.BytesIO(baseline_frame),
        )
        return status, json.loads(output.getvalue())

    @staticmethod
    def baseline_frame() -> bytes:
        return (
            go_mod("v1.83.1").encode("utf-8")
            + updater.BASELINE_FRAME_SEPARATOR
            + baseline_go_sum().encode("utf-8")
        )

    def test_resolves_the_only_approved_component_floor(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.root_with_module(Path(temporary))
            status, result = self.run_cli(root, ["--check", "--json"])
        self.assertEqual(status, 0)
        self.assertEqual(result["status"], "update_available")
        self.assertIs(result["update_available"], True)
        self.assertEqual(
            result["components"],
            [
                {
                    "directory": "connectors/envoy/ext_proc",
                    "dependency": "google.golang.org/grpc",
                    "current_version": "v1.83.1",
                    "target_version": "v1.83.2",
                    "update_available": True,
                }
            ],
        )

    def test_current_or_newer_complete_bundle_needs_no_component_update(self) -> None:
        for version in ("v1.83.2", "v1.83.10", "v1.84.0", "v1.100.0"):
            with self.subTest(version=version), tempfile.TemporaryDirectory() as temporary:
                root = self.root_with_module(Path(temporary), go_mod_source=target_go_mod(version))
                status, result = self.run_cli(root, ["--check", "--json"])
            self.assertEqual(status, 0)
            self.assertEqual(result["status"], "current")
            self.assertIs(result["update_available"], False)

    def test_rejects_malformed_partial_or_missing_requirements(self) -> None:
        cases = {
            "prerelease": go_mod("v1.83.2-rc.1"),
            "indirect": go_mod("v1.83.1").replace(
                "\tgoogle.golang.org/grpc v1.83.1\n",
                "\tgoogle.golang.org/grpc v1.83.1 // indirect\n",
            ),
            "missing": go_mod("v1.83.1").replace("\tgoogle.golang.org/grpc v1.83.1\n", ""),
            "partial_baseline": go_mod("v1.83.1", sys_version=TARGET_SYS),
            "partial_target": go_mod("v1.83.2"),
        }
        for name, source in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                root = self.root_with_module(Path(temporary), go_mod_source=source)
                status, result = self.run_cli(root, ["--check", "--json"])
            self.assertEqual((status, result["status"]), (1, "error"))

    def test_rejects_a_symlinked_component_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            module = root / "connectors" / "envoy" / "ext_proc"
            module.mkdir(parents=True)
            outside = root / "outside-go-mod"
            outside.write_text(go_mod("v1.83.1"), encoding="utf-8")
            (module / "go.mod").symlink_to(outside)
            (module / "go.sum").write_text(baseline_go_sum(), encoding="utf-8")
            status, result = self.run_cli(root, ["--check", "--json"])
        self.assertEqual((status, result["status"]), (1, "error"))

    def test_rejects_a_symlinked_component_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            outside_module = root / "outside" / "envoy" / "ext_proc"
            outside_module.mkdir(parents=True)
            (outside_module / "go.mod").write_text(go_mod("v1.83.1"), encoding="utf-8")
            (outside_module / "go.sum").write_text(baseline_go_sum(), encoding="utf-8")
            (root / "connectors").symlink_to(root / "outside", target_is_directory=True)
            status, result = self.run_cli(root, ["--check", "--json"])
        self.assertEqual((status, result["status"]), (1, "error"))

    def test_preflight_rejects_symlinks_without_modifying_their_targets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temporary_path = Path(temporary)
            for filename, source in (("go.mod", go_mod("v1.83.1")), ("go.sum", baseline_go_sum())):
                with self.subTest(filename=filename):
                    root = self.root_with_module(temporary_path / filename)
                    module = root / "connectors" / "envoy" / "ext_proc"
                    target = root / f"outside-{filename}"
                    target.write_text(source, encoding="utf-8")
                    (module / filename).unlink()
                    (module / filename).symlink_to(target)
                    before = target.read_bytes()
                    status, result = self.run_cli(root, ["--validate-component-files", "--json"])
                    self.assertEqual((status, result["status"]), (1, "error"))
                    self.assertEqual(target.read_bytes(), before)

            root = temporary_path / "intermediate-directory"
            outside_module = root / "outside" / "envoy" / "ext_proc"
            outside_module.mkdir(parents=True)
            target_go_mod = outside_module / "go.mod"
            target_go_sum = outside_module / "go.sum"
            target_go_mod.write_text(go_mod("v1.83.1"), encoding="utf-8")
            target_go_sum.write_text(baseline_go_sum(), encoding="utf-8")
            before_go_mod = target_go_mod.read_bytes()
            before_go_sum = target_go_sum.read_bytes()
            (root / "connectors").symlink_to(root / "outside", target_is_directory=True)
            status, result = self.run_cli(root, ["--validate-component-files", "--json"])
            self.assertEqual((status, result["status"]), (1, "error"))
            self.assertEqual(target_go_mod.read_bytes(), before_go_mod)
            self.assertEqual(target_go_sum.read_bytes(), before_go_sum)

    def test_preflight_accepts_real_component_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.root_with_module(Path(temporary))
            status, result = self.run_cli(root, ["--validate-component-files", "--json"])
        self.assertEqual(status, 0)
        self.assertEqual(
            result,
            {
                "status": "valid",
                "directory": "connectors/envoy/ext_proc",
                "files": ["go.mod", "go.sum"],
            },
        )

    def test_candidate_cli_reads_only_static_component_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.root_with_module(
                Path(temporary),
                go_mod_source=target_go_mod(),
                go_sum_source=candidate_go_sum(),
            )
            status, result = self.run_cli(
                root,
                ["--validate-candidate", "--json"],
                baseline_frame=self.baseline_frame(),
            )
        self.assertEqual(status, 0)
        self.assertEqual(result["status"], "valid")

    def test_candidate_cli_rejects_malformed_baseline_frames_and_symlinked_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.root_with_module(
                Path(temporary),
                go_mod_source=target_go_mod(),
                go_sum_source=candidate_go_sum(),
            )
            malformed_frames = {
                "no_separator": self.baseline_frame().replace(updater.BASELINE_FRAME_SEPARATOR, b"", 1),
                "extra_separator": self.baseline_frame() + updater.BASELINE_FRAME_SEPARATOR,
                "oversized": b"x" * (updater.MAX_BASELINE_FRAME_BYTES + 1),
            }
            for name, baseline_frame in malformed_frames.items():
                with self.subTest(name=name):
                    status, result = self.run_cli(
                        root,
                        ["--validate-candidate", "--json"],
                        baseline_frame=baseline_frame,
                    )
                    self.assertEqual((status, result["status"]), (1, "error"))

            module = root / "connectors" / "envoy" / "ext_proc"
            outside = root / "outside-go-mod"
            outside.write_text(target_go_mod(), encoding="utf-8")
            (module / "go.mod").unlink()
            (module / "go.mod").symlink_to(outside)
            before = outside.read_bytes()
            status, result = self.run_cli(
                root,
                ["--validate-candidate", "--json"],
                baseline_frame=self.baseline_frame(),
            )
            self.assertEqual((status, result["status"]), (1, "error"))
            self.assertEqual(outside.read_bytes(), before)

    def test_candidate_validation_accepts_only_the_fixed_bundle_and_checksums(self) -> None:
        baseline_mod = go_mod("v1.83.1").encode("utf-8")
        candidate_mod = target_go_mod().encode("utf-8")
        baseline_sum = baseline_go_sum().encode("utf-8")
        candidate_sum = candidate_go_sum().encode("utf-8")

        result = updater.validate_component_candidate(
            baseline_mod,
            candidate_mod,
            baseline_sum,
            candidate_sum,
        )

        self.assertEqual(result["status"], "valid")
        self.assertEqual(result["baseline_version"], "v1.83.1")
        self.assertEqual(result["target_version"], "v1.83.2")
        self.assertEqual(result["go_mod_sha256"], hashlib.sha256(candidate_mod).hexdigest())
        self.assertEqual(result["go_sum_sha256"], hashlib.sha256(candidate_sum).hexdigest())
        updater.require_expected_candidate_hashes(
            result,
            expected_go_mod_sha256=hashlib.sha256(candidate_mod).hexdigest(),
            expected_go_sum_sha256=hashlib.sha256(candidate_sum).hexdigest(),
        )
        for expected_go_mod_sha256, expected_go_sum_sha256 in (
            ("0" * 64, hashlib.sha256(candidate_sum).hexdigest()),
            ("not-a-digest", hashlib.sha256(candidate_sum).hexdigest()),
            (hashlib.sha256(candidate_mod).hexdigest(), "not-a-digest"),
        ):
            with self.subTest(
                expected_go_mod_sha256=expected_go_mod_sha256,
                expected_go_sum_sha256=expected_go_sum_sha256,
            ):
                with self.assertRaises(updater.ComponentError):
                    updater.require_expected_candidate_hashes(
                        result,
                        expected_go_mod_sha256=expected_go_mod_sha256,
                        expected_go_sum_sha256=expected_go_sum_sha256,
                    )

        tidied_candidate_sum = (
            baseline_go_sum().replace(
                checksum_entries(
                    "v1.83.1",
                    sys_version=BASELINE_SYS,
                    net_version=BASELINE_NET,
                    text_version=BASELINE_TEXT,
                ),
                "",
            )
            + checksum_entries(
                "v1.83.2",
                sys_version=TARGET_SYS,
                net_version=TARGET_NET,
                text_version=TARGET_TEXT,
            )
        ).encode("utf-8")
        self.assertEqual(
            updater.validate_component_candidate(
                baseline_mod,
                candidate_mod,
                baseline_sum,
                tidied_candidate_sum,
            )["status"],
            "valid",
        )

    def test_candidate_validation_rejects_unapproved_manifest_or_checksum_changes(self) -> None:
        baseline_mod = go_mod("v1.83.1").encode("utf-8")
        baseline_sum = baseline_go_sum().encode("utf-8")
        cases = {
            "other_direct_requirement": (
                target_go_mod().replace(
                    "\tgoogle.golang.org/protobuf v1.36.11\n",
                    "\tgoogle.golang.org/protobuf v1.36.12\n",
                ).encode("utf-8"),
                candidate_go_sum().encode("utf-8"),
            ),
            "unrelated_checksum": (
                target_go_mod().encode("utf-8"),
                candidate_go_sum(extra="golang.org/x/crypto v0.56.1 h1:crypto=\n").encode("utf-8"),
            ),
            "altered_target_checksum": (
                target_go_mod().encode("utf-8"),
                candidate_go_sum()
                .replace(
                    "h1:EManeRomTObA0BU7I8vXgg/78uE5MJ9M8B39EX2WscU=",
                    "h1:tampered=",
                )
                .encode("utf-8"),
            ),
            "wrong_target": (
                target_go_mod("v1.83.3").encode("utf-8"),
                candidate_go_sum("v1.83.3").encode("utf-8"),
            ),
        }
        for name, (candidate_mod, candidate_sum) in cases.items():
            with self.subTest(name=name):
                with self.assertRaises(updater.ComponentError):
                    updater.validate_component_candidate(
                        baseline_mod,
                        candidate_mod,
                        baseline_sum,
                        candidate_sum,
                    )

    def test_candidate_validation_rejects_non_update_unapproved_or_missing_target_checksums(self) -> None:
        baseline_mod = go_mod("v1.83.1").encode("utf-8")
        baseline_sum = baseline_go_sum().encode("utf-8")
        target_mod = target_go_mod().encode("utf-8")
        target_sum = candidate_go_sum().encode("utf-8")
        missing_text_target_sum = (
            candidate_go_sum()
            .replace(
                f"golang.org/x/text {TARGET_TEXT} "
                f"{checksum_for('golang.org/x/text', TARGET_TEXT, '', 'text')}\n"
                f"golang.org/x/text {TARGET_TEXT}/go.mod "
                f"{checksum_for('golang.org/x/text', TARGET_TEXT, '/go.mod', 'text')}\n",
                "",
            )
            .encode("utf-8")
        )
        missing_protobuf_target_sum = (
            candidate_go_sum()
            .replace("google.golang.org/protobuf v1.36.11 h1:protobuf=\n", "")
            .encode("utf-8")
        )
        with self.assertRaises(updater.ComponentError):
            updater.validate_component_candidate(target_mod, target_mod, target_sum, target_sum)
        with self.assertRaises(updater.ComponentError):
            updater.validate_component_candidate(
                baseline_mod,
                target_mod,
                baseline_sum,
                missing_text_target_sum,
            )
        with self.assertRaises(updater.ComponentError):
            updater.validate_component_candidate(
                baseline_mod,
                target_mod,
                baseline_sum,
                missing_protobuf_target_sum,
            )


if __name__ == "__main__":
    unittest.main()
