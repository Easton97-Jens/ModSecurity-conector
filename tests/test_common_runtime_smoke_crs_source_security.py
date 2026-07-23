from __future__ import annotations

import argparse
import importlib.util
import os
import stat
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "common_runtime_smoke_crs_source_security",
    ROOT / "common/scripts/run_local_runtime_smoke.py",
)
assert SPEC is not None and SPEC.loader is not None
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


class CommonRuntimeSmokeCrsSourceSecurityTest(unittest.TestCase):
    @staticmethod
    def make_args(
        *,
        crs_source_dir: Path | str = "",
        runtime_lookup_root: list[Path | str] | None = None,
        evidence_root: Path | None = None,
    ) -> argparse.Namespace:
        return argparse.Namespace(
            crs_source_dir=str(crs_source_dir),
            runtime_lookup_root=[str(path) for path in runtime_lookup_root or []],
            evidence_root=str(evidence_root) if evidence_root is not None else "",
            crs_smoke_case="minimal",
            crs_git_ref="",
        )

    @staticmethod
    def make_crs_source(path: Path) -> Path:
        path.mkdir(parents=True, mode=0o700)
        path.chmod(0o700)
        setup = path / "crs-setup.conf.example"
        setup.write_text("SecRuleEngine On\n", encoding="utf-8")
        setup.chmod(stat.S_IRUSR | stat.S_IWUSR)
        rules_dir = path / "rules"
        rules_dir.mkdir(mode=0o700)
        rules_dir.chmod(0o700)
        rule = rules_dir / "REQUEST-901-INITIALIZATION.conf"
        rule.write_text('SecRule ARGS "@contains safe" "id:901001,pass,nolog"\n', encoding="utf-8")
        rule.chmod(stat.S_IRUSR | stat.S_IWUSR)
        return path

    def test_shared_temporary_environment_is_not_an_implicit_crs_candidate(self) -> None:
        with tempfile.TemporaryDirectory(prefix="common-crs-source-") as temporary:
            temporary_root = Path(temporary)
            self.make_crs_source(
                temporary_root / "ModSecurity-conector-verified/src/coreruleset"
            )
            args = self.make_args()
            with mock.patch.dict(
                os.environ,
                {"RUNNER_TEMP": str(temporary_root), "TMPDIR": str(temporary_root)},
                clear=False,
            ):
                self.assertEqual([], RUNNER.crs_source_candidate_roots(args))
                with self.assertRaisesRegex(RUNNER.SmokeBlocked, "missing CRS_SOURCE_DIR"):
                    RUNNER.resolve_crs_source_dir(args)

    def test_trusted_explicit_crs_source_generates_smoke_config(self) -> None:
        with tempfile.TemporaryDirectory(prefix="common-crs-source-") as temporary:
            temporary_root = Path(temporary)
            source_dir = self.make_crs_source(temporary_root / "crs-source")
            evidence_root = temporary_root / "evidence"
            evidence_root.mkdir(mode=0o700)
            evidence_root.chmod(0o700)
            (evidence_root / "crs-smoke").mkdir(mode=0o700)
            (evidence_root / "crs-smoke").chmod(0o700)
            log_dir = temporary_root / "logs"
            log_dir.mkdir(mode=0o700)
            args = self.make_args(crs_source_dir=source_dir, evidence_root=evidence_root)

            resolved = RUNNER.resolve_crs_source_dir(args)
            rule_file, runtime_dir, _version = RUNNER.prepare_crs_smoke_config(
                args, log_dir
            )

            self.assertEqual(source_dir, resolved)
            self.assertEqual(evidence_root / "crs-smoke", runtime_dir)
            self.assertIn(str(source_dir / "rules"), rule_file.read_text(encoding="utf-8"))

    def test_trusted_runtime_lookup_root_candidate_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory(prefix="common-crs-source-") as temporary:
            temporary_root = Path(temporary)
            lookup_root = temporary_root / "runtime-root"
            lookup_root.mkdir(mode=0o700)
            lookup_root.chmod(0o700)
            source_dir = self.make_crs_source(lookup_root / "sources/coreruleset")
            args = self.make_args(runtime_lookup_root=[lookup_root])

            self.assertEqual(source_dir, RUNNER.resolve_crs_source_dir(args))

    def test_symlinked_crs_source_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="common-crs-source-") as temporary:
            temporary_root = Path(temporary)
            source_dir = self.make_crs_source(temporary_root / "crs-source")
            alias = temporary_root / "crs-alias"
            alias.symlink_to(source_dir, target_is_directory=True)
            args = self.make_args(crs_source_dir=alias)

            with self.assertRaisesRegex(RUNNER.SmokeBlocked, "must not contain a symlink"):
                RUNNER.resolve_crs_source_dir(args)

    def test_group_or_world_writable_rules_directory_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="common-crs-source-") as temporary:
            source_dir = self.make_crs_source(Path(temporary) / "crs-source")
            rules_dir = source_dir / "rules"
            rules_dir.chmod(stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            args = self.make_args(crs_source_dir=source_dir)

            with self.assertRaisesRegex(RUNNER.SmokeBlocked, "must not be group or world writable"):
                RUNNER.resolve_crs_source_dir(args)

    def test_group_or_world_writable_rule_file_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="common-crs-source-") as temporary:
            source_dir = self.make_crs_source(Path(temporary) / "crs-source")
            rule_file = source_dir / "rules/REQUEST-901-INITIALIZATION.conf"
            rule_file.chmod(stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            args = self.make_args(crs_source_dir=source_dir)

            with self.assertRaisesRegex(RUNNER.SmokeBlocked, "must not be group or world writable"):
                RUNNER.resolve_crs_source_dir(args)

    def test_group_or_world_writable_included_plugin_file_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="common-crs-source-") as temporary:
            source_dir = self.make_crs_source(Path(temporary) / "crs-source")
            plugins_dir = source_dir / "plugins"
            plugins_dir.mkdir(mode=0o700)
            plugins_dir.chmod(0o700)
            plugin_file = plugins_dir / "local-before.conf"
            plugin_file.write_text(
                'SecRule ARGS "@contains safe" "id:901002,pass,nolog"\n', encoding="utf-8"
            )
            plugin_file.chmod(stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            args = self.make_args(crs_source_dir=source_dir)

            with self.assertRaisesRegex(RUNNER.SmokeBlocked, "must not be group or world writable"):
                RUNNER.resolve_crs_source_dir(args)

    def test_sticky_parent_must_also_be_trusted(self) -> None:
        sticky_parent = SimpleNamespace(
            st_mode=stat.S_IFDIR | stat.S_ISVTX | stat.S_IWGRP
        )
        runner_owned_child = SimpleNamespace(st_mode=stat.S_IFDIR | stat.S_IRWXU)

        with mock.patch.object(
            RUNNER, "is_trusted_crs_owner", side_effect=[False, True]
        ):
            self.assertFalse(
                RUNNER.crs_directory_entry_is_protected(
                    sticky_parent, runner_owned_child
                )
            )
        with mock.patch.object(
            RUNNER, "is_trusted_crs_owner", side_effect=[True, True]
        ):
            self.assertTrue(
                RUNNER.crs_directory_entry_is_protected(
                    sticky_parent, runner_owned_child
                )
            )

    def test_group_or_world_writable_evidence_root_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="common-crs-source-") as temporary:
            temporary_root = Path(temporary)
            source_dir = self.make_crs_source(temporary_root / "crs-source")
            evidence_root = temporary_root / "evidence"
            evidence_root.mkdir(mode=0o700)
            evidence_root.chmod(stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            log_dir = temporary_root / "logs"
            log_dir.mkdir(mode=0o700)
            args = self.make_args(crs_source_dir=source_dir, evidence_root=evidence_root)

            with self.assertRaisesRegex(
                RUNNER.SmokeBlocked,
                "CRS evidence root must not be group or world writable",
            ):
                RUNNER.prepare_crs_smoke_config(args, log_dir)

    def test_group_or_world_writable_runtime_directory_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="common-crs-source-") as temporary:
            temporary_root = Path(temporary)
            source_dir = self.make_crs_source(temporary_root / "crs-source")
            evidence_root = temporary_root / "evidence"
            evidence_root.mkdir(mode=0o700)
            evidence_root.chmod(0o700)
            runtime_dir = evidence_root / "crs-smoke"
            runtime_dir.mkdir(mode=0o700)
            runtime_dir.chmod(stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            log_dir = temporary_root / "logs"
            log_dir.mkdir(mode=0o700)
            args = self.make_args(crs_source_dir=source_dir, evidence_root=evidence_root)

            with self.assertRaisesRegex(
                RUNNER.SmokeBlocked,
                "CRS smoke runtime directory must not be group or world writable",
            ):
                RUNNER.prepare_crs_smoke_config(args, log_dir)

    def test_symlinked_runtime_directory_is_rejected_before_generated_write(self) -> None:
        with tempfile.TemporaryDirectory(prefix="common-crs-source-") as temporary:
            temporary_root = Path(temporary)
            source_dir = self.make_crs_source(temporary_root / "crs-source")
            evidence_root = temporary_root / "evidence"
            evidence_root.mkdir(mode=0o700)
            evidence_root.chmod(0o700)
            target_dir = temporary_root / "target"
            target_dir.mkdir(mode=0o700)
            (evidence_root / "crs-smoke").symlink_to(target_dir, target_is_directory=True)
            log_dir = temporary_root / "logs"
            log_dir.mkdir(mode=0o700)
            args = self.make_args(crs_source_dir=source_dir, evidence_root=evidence_root)

            with self.assertRaisesRegex(RUNNER.SmokeBlocked, "must not contain a symlink"):
                RUNNER.prepare_crs_smoke_config(args, log_dir)

    def test_symlinked_generated_setup_file_is_rejected_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory(prefix="common-crs-source-") as temporary:
            temporary_root = Path(temporary)
            source_dir = self.make_crs_source(temporary_root / "crs-source")
            evidence_root = temporary_root / "evidence"
            runtime_dir = evidence_root / "crs-smoke"
            runtime_dir.mkdir(parents=True, mode=0o700)
            evidence_root.chmod(0o700)
            runtime_dir.chmod(0o700)
            protected_target = temporary_root / "protected-setup"
            protected_target.write_text("keep\n", encoding="utf-8")
            protected_target.chmod(0o600)
            (runtime_dir / "crs-setup.conf").symlink_to(protected_target)
            log_dir = temporary_root / "logs"
            log_dir.mkdir(mode=0o700)
            args = self.make_args(crs_source_dir=source_dir, evidence_root=evidence_root)

            with self.assertRaisesRegex(
                RUNNER.SmokeBlocked,
                "generated CRS setup file must not contain a symlink",
            ):
                RUNNER.prepare_crs_smoke_config(args, log_dir)
            self.assertEqual("keep\n", protected_target.read_text(encoding="utf-8"))

    def test_symlinked_generated_rule_file_is_rejected_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory(prefix="common-crs-source-") as temporary:
            temporary_root = Path(temporary)
            source_dir = self.make_crs_source(temporary_root / "crs-source")
            evidence_root = temporary_root / "evidence"
            runtime_dir = evidence_root / "crs-smoke"
            runtime_dir.mkdir(parents=True, mode=0o700)
            evidence_root.chmod(0o700)
            runtime_dir.chmod(0o700)
            protected_target = temporary_root / "protected-rule"
            protected_target.write_text("keep\n", encoding="utf-8")
            protected_target.chmod(0o600)
            (runtime_dir / "modsecurity-crs-smoke.conf").symlink_to(protected_target)
            log_dir = temporary_root / "logs"
            log_dir.mkdir(mode=0o700)
            args = self.make_args(crs_source_dir=source_dir, evidence_root=evidence_root)

            with self.assertRaisesRegex(
                RUNNER.SmokeBlocked,
                "generated CRS smoke rule must not contain a symlink",
            ):
                RUNNER.prepare_crs_smoke_config(args, log_dir)
            self.assertEqual("keep\n", protected_target.read_text(encoding="utf-8"))

    def test_group_or_world_writable_audit_log_directory_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="common-crs-source-") as temporary:
            temporary_root = Path(temporary)
            source_dir = self.make_crs_source(temporary_root / "crs-source")
            evidence_root = temporary_root / "evidence"
            evidence_root.mkdir(mode=0o700)
            evidence_root.chmod(0o700)
            log_dir = temporary_root / "logs"
            log_dir.mkdir(mode=0o700)
            log_dir.chmod(stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            args = self.make_args(crs_source_dir=source_dir, evidence_root=evidence_root)

            with self.assertRaisesRegex(
                RUNNER.SmokeBlocked,
                "CRS audit-log directory must not be group or world writable",
            ):
                RUNNER.prepare_crs_smoke_config(args, log_dir)

    def test_symlinked_audit_log_is_rejected_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory(prefix="common-crs-source-") as temporary:
            temporary_root = Path(temporary)
            source_dir = self.make_crs_source(temporary_root / "crs-source")
            evidence_root = temporary_root / "evidence"
            evidence_root.mkdir(mode=0o700)
            evidence_root.chmod(0o700)
            log_dir = temporary_root / "logs"
            log_dir.mkdir(mode=0o700)
            protected_target = temporary_root / "protected-audit"
            protected_target.write_text("keep\n", encoding="utf-8")
            protected_target.chmod(0o600)
            (log_dir / "crs-audit.log").symlink_to(protected_target)
            args = self.make_args(crs_source_dir=source_dir, evidence_root=evidence_root)

            with self.assertRaisesRegex(
                RUNNER.SmokeBlocked,
                "generated CRS audit log must not contain a symlink",
            ):
                RUNNER.prepare_crs_smoke_config(args, log_dir)
            self.assertEqual("keep\n", protected_target.read_text(encoding="utf-8"))

    def test_quoted_source_path_is_rejected_before_config_generation(self) -> None:
        with tempfile.TemporaryDirectory(prefix="common-crs-source-") as temporary:
            temporary_root = Path(temporary)
            source_dir = self.make_crs_source(temporary_root / 'crs"source')
            evidence_root = temporary_root / "evidence"
            evidence_root.mkdir(mode=0o700)
            evidence_root.chmod(0o700)
            log_dir = temporary_root / "logs"
            log_dir.mkdir(mode=0o700)
            args = self.make_args(crs_source_dir=source_dir, evidence_root=evidence_root)

            with self.assertRaisesRegex(
                RUNNER.SmokeBlocked, "unsupported characters for a ModSecurity directive"
            ):
                RUNNER.prepare_crs_smoke_config(args, log_dir)

    def test_globbed_source_path_is_rejected_before_config_generation(self) -> None:
        with tempfile.TemporaryDirectory(prefix="common-crs-source-") as temporary:
            temporary_root = Path(temporary)
            source_dir = self.make_crs_source(temporary_root / "crs*source")
            evidence_root = temporary_root / "evidence"
            evidence_root.mkdir(mode=0o700)
            evidence_root.chmod(0o700)
            log_dir = temporary_root / "logs"
            log_dir.mkdir(mode=0o700)
            args = self.make_args(crs_source_dir=source_dir, evidence_root=evidence_root)

            with self.assertRaisesRegex(
                RUNNER.SmokeBlocked, "unsupported characters for a ModSecurity directive"
            ):
                RUNNER.prepare_crs_smoke_config(args, log_dir)


if __name__ == "__main__":
    unittest.main()
