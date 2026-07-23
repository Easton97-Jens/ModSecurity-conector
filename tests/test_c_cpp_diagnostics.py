#!/usr/bin/env python3
"""Contract tests for the local C17/C++17 diagnostics foundation."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CDB_TOOL = ROOT / "ci/checks/analysis/compile_database.py"
NGINX_CONFIG = ROOT / "connectors/nginx/config"
NGINX_CHECK = ROOT / "ci/checks/connectors/nginx/check-nginx-c-standards.sh"
NGINX_DATABASE_CHECK = ROOT / "ci/checks/analysis/compile-db-nginx-c17.sh"
CPP_DATABASE_CHECK = ROOT / "ci/checks/analysis/compile-db-cpp17.sh"
CPP_EVALUATOR_CHECK = ROOT / "ci/checks/analysis/check-targeted-evaluator-cpp17.sh"
ANALYSIS_TOOLS_CHECK = ROOT / "ci/checks/analysis/check-analysis-tools.sh"


def nginx_config_sources() -> set[Path]:
    sources: set[Path] = set()
    for connector_source, common_source in re.findall(
        r"\$ngx_addon_dir/(src/[A-Za-z0-9_./-]+\.c)|\$MSCONNECTOR_COMMON_SRC/([A-Za-z0-9_./-]+\.c)",
        NGINX_CONFIG.read_text(encoding="utf-8"),
    ):
        if connector_source:
            sources.add((ROOT / "connectors/nginx" / connector_source).resolve())
        else:
            sources.add((ROOT / "common/src" / common_source).resolve())
    return sources


def cdb_entry(source: Path, output_root: Path) -> dict[str, object]:
    relative = source.relative_to(ROOT).as_posix().replace("/", "_")
    if source.suffix == ".c":
        arguments = [
            "/usr/bin/cc",
            "-std=c17",
            "-Wall",
            "-Wextra",
            "-Werror",
            "-c",
            str(source),
            "-o",
            str(output_root / f"{relative}.o"),
        ]
        output = output_root / f"{relative}.o"
    else:
        arguments = [
            "/usr/bin/c++",
            "-std=c++17",
            "-Wall",
            "-Wextra",
            "-Werror",
            str(source),
            "-o",
            str(output_root / "modsecurity_targeted_eval"),
        ]
        output = output_root / "modsecurity_targeted_eval"
    return {
        "directory": str(ROOT),
        "file": str(source),
        "arguments": arguments,
        "output": str(output),
    }


class CAndCppDiagnosticsContractTests(unittest.TestCase):
    maxDiff = None

    def run_cdb_tool(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [sys.executable, str(CDB_TOOL), "--repo-root", str(ROOT), *arguments],
            cwd=ROOT,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_nginx_config_and_c17_check_cover_the_same_real_sources(self) -> None:
        configured = nginx_config_sources()
        checked = {
            (ROOT / source).resolve()
            for source in re.findall(
                r"(?:connectors/nginx|common)/[A-Za-z0-9_./-]+\.c",
                NGINX_CHECK.read_text(encoding="utf-8"),
            )
        }

        self.assertTrue(configured)
        self.assertSetEqual(configured, checked)
        self.assertTrue(all(source.is_file() for source in configured))
        self.assertIn(ROOT / "common/src/late_intervention.c", checked)

    def test_make_targets_keep_analysis_opt_in_and_clangd_non_mutating(self) -> None:
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        for target in (
            "check-analysis-tools",
            "compile-db-nginx-c17",
            "check-targeted-evaluator-cpp17",
            "compile-db-cpp17",
            "check-clangd-c17",
        ):
            self.assertIn(f"{target}:", makefile)
        self.assertIn(
            ".PHONY: check-analysis-tools compile-db-nginx-c17 "
            "check-targeted-evaluator-cpp17 compile-db-cpp17 check-clangd-c17",
            makefile,
        )

        clangd_script = (ROOT / "ci/checks/analysis/check-clangd-c17.sh").read_text(
            encoding="utf-8"
        )
        self.assertIn("--clang-tidy=false", clangd_script)
        self.assertIn("--enable-config=false", clangd_script)
        self.assertIn("--tweaks=", clangd_script)
        self.assertIn("--compile-commands-dir", clangd_script)
        self.assertIn("--log=error", clangd_script)
        evaluator_script = (
            ROOT / "ci/checks/analysis/check-targeted-evaluator-cpp17.sh"
        ).read_text(encoding="utf-8")
        self.assertIn("-isystem \"$MODSECURITY_INCLUDE_DIR\"", evaluator_script)
        self.assertIn("-Wall -Wextra -Werror", evaluator_script)
        self.assertNotIn("check-analysis-tools", makefile[makefile.index("lint:") :])
        self.assertFalse((ROOT / ".clangd").exists())
        self.assertFalse((ROOT / ".clang-tidy").exists())

    def test_checkout_output_requests_are_rejected_before_creating_directories(self) -> None:
        test_root = ROOT / ".c-cpp-diagnostics-output-regression"
        self.assertFalse(test_root.exists())
        self.addCleanup(shutil.rmtree, test_root, ignore_errors=True)

        for script, variable in (
            (NGINX_DATABASE_CHECK, "COMPDB_OUTPUT"),
            (CPP_DATABASE_CHECK, "COMPDB_OUTPUT"),
            (CPP_EVALUATOR_CHECK, "CPP_BUILD_ROOT"),
        ):
            environment = os.environ.copy()
            target = test_root / (
                "compile_commands.json" if variable == "COMPDB_OUTPUT" else "build"
            )
            environment[variable] = str(target)
            result = subprocess.run(
                [str(script)],
                cwd=ROOT,
                env=environment,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("outside the checkout", result.stderr)
            self.assertFalse(test_root.exists())

    def test_external_output_requests_continue_to_dependency_checks(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="c-cpp-diagnostics-external-output-"
        ) as temporary_directory:
            temporary_root = Path(temporary_directory)
            for script, variable, target, tool_variable, expected_message, defaults in (
                (
                    CPP_DATABASE_CHECK,
                    "COMPDB_OUTPUT",
                    temporary_root / "cpp" / "compile_commands.json",
                    "CXX",
                    "BLOCKED: missing C++ compiler",
                    2,
                ),
                (
                    NGINX_DATABASE_CHECK,
                    "COMPDB_OUTPUT",
                    temporary_root / "nginx" / "compile_commands.json",
                    "CC",
                    "BLOCKED: missing C compiler",
                    2,
                ),
                (
                    CPP_EVALUATOR_CHECK,
                    "CPP_BUILD_ROOT",
                    temporary_root / "evaluator",
                    "CXX",
                    "BLOCKED: missing C++ compiler",
                    1,
                ),
            ):
                environment = os.environ.copy()
                environment[variable] = str(target)
                environment[tool_variable] = "codex-missing-compiler-for-contract-test"
                result = subprocess.run(
                    [str(script)],
                    cwd=ROOT,
                    env=environment,
                    check=False,
                    capture_output=True,
                    text=True,
                )
                script_text = script.read_text(encoding="utf-8")
                self.assertEqual(result.returncode, 77, result.stderr)
                self.assertIn(expected_message, result.stderr)
                self.assertNotIn("outside the checkout", result.stderr)
                created_path = target.parent if variable == "COMPDB_OUTPUT" else target
                self.assertTrue(created_path.exists())
                self.assertEqual(script_text.count("*) : ;;"), defaults)

    def test_missing_analysis_tool_returns_documented_blocked_status(self) -> None:
        environment = os.environ.copy()
        environment["CC"] = "codex-missing-c-compiler-for-contract-test"
        result = subprocess.run(
            [str(ANALYSIS_TOOLS_CHECK)],
            cwd=ROOT,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 77, result.stderr)
        self.assertIn("BLOCKED: CC is unavailable", result.stderr)

    def test_compilation_database_filtering_validation_merging_and_atomic_publish(self) -> None:
        temporary_parent = os.environ.get("TMPDIR")
        with tempfile.TemporaryDirectory(
            prefix="c-cpp-diagnostics-", dir=temporary_parent
        ) as temporary_directory:
            temporary_root = Path(temporary_directory)
            output_root = temporary_root / "objects"
            output_root.mkdir()
            database = temporary_root / "compile_commands.json"
            c_sources = sorted(nginx_config_sources(), key=lambda path: path.as_posix())
            cpp_source = (ROOT / "common/scripts/modsecurity_targeted_eval.cc").resolve()
            generated_probe = temporary_root / "generated-probe.c"
            generated_probe.write_text("int generated_probe(void) { return 0; }\n", encoding="utf-8")

            c_capture = temporary_root / "nginx-raw.json"
            c_capture.write_text(
                json.dumps(
                    [cdb_entry(source, output_root) for source in c_sources]
                    + [
                        cdb_entry(c_sources[0], output_root),
                        {
                            "directory": str(ROOT),
                            "file": str(generated_probe),
                            "arguments": [
                                "/usr/bin/cc",
                                "-std=c17",
                                "-Wall",
                                "-Wextra",
                                "-Werror",
                            ],
                            "output": str(output_root / "generated-probe.o"),
                        },
                    ]
                ),
                encoding="utf-8",
            )
            c_result = self.run_cdb_tool(
                "--input",
                str(c_capture),
                "--output",
                str(database),
                "--require",
                "nginx",
            )
            self.assertEqual(c_result.returncode, 0, c_result.stderr)
            self.assertIn("FILTERED: duplicate translation unit", c_result.stdout)
            self.assertIn("FILTERED: entry", c_result.stdout)

            missing_c_capture = temporary_root / "missing-c-raw.json"
            missing_c_capture.write_text(
                json.dumps([cdb_entry(source, output_root) for source in c_sources[1:]]),
                encoding="utf-8",
            )
            missing_c_database = temporary_root / "missing-c-compile_commands.json"
            missing_c_result = self.run_cdb_tool(
                "--input",
                str(missing_c_capture),
                "--output",
                str(missing_c_database),
                "--require",
                "nginx",
            )
            self.assertNotEqual(missing_c_result.returncode, 0)
            self.assertIn("coverage is incomplete", missing_c_result.stderr)
            self.assertIn(
                str(c_sources[0].relative_to(ROOT)), missing_c_result.stderr
            )
            self.assertFalse(missing_c_database.exists())

            missing_cpp_result = self.run_cdb_tool(
                "--output",
                str(database),
                "--verify-only",
                "--require",
                "nginx",
                "--require",
                "cpp",
            )
            self.assertNotEqual(missing_cpp_result.returncode, 0)
            self.assertIn("coverage is incomplete", missing_cpp_result.stderr)
            self.assertIn(
                "common/scripts/modsecurity_targeted_eval.cc", missing_cpp_result.stderr
            )

            cpp_capture = temporary_root / "cpp-raw.json"
            cpp_capture.write_text(
                json.dumps([cdb_entry(cpp_source, output_root)]), encoding="utf-8"
            )
            cpp_result = self.run_cdb_tool(
                "--input",
                str(cpp_capture),
                "--output",
                str(database),
                "--merge-existing",
                "--require",
                "cpp",
            )
            self.assertEqual(cpp_result.returncode, 0, cpp_result.stderr)

            verify_result = self.run_cdb_tool(
                "--output",
                str(database),
                "--verify-only",
                "--require",
                "nginx",
                "--require",
                "cpp",
            )
            self.assertEqual(verify_result.returncode, 0, verify_result.stderr)

            published = json.loads(database.read_text(encoding="utf-8"))
            self.assertIsInstance(published, list)
            published_sources = {Path(entry["file"]).resolve() for entry in published}
            self.assertSetEqual(published_sources, set(c_sources) | {cpp_source})
            self.assertEqual(len(published), len(published_sources))
            self.assertTrue(all(source.is_file() and ROOT in source.parents for source in published_sources))
            self.assertTrue(all(Path(entry["output"]).is_absolute() for entry in published))
            self.assertTrue(all(ROOT not in Path(entry["output"]).resolve().parents for entry in published))
            for entry in published:
                source = Path(entry["file"])
                arguments = entry["arguments"]
                self.assertIn("-Wall", arguments)
                self.assertIn("-Wextra", arguments)
                self.assertIn("-Werror", arguments)
                self.assertIn("-std=c17" if source.suffix == ".c" else "-std=c++17", arguments)

            original_database = database.read_bytes()
            invalid_capture = temporary_root / "invalid-raw.json"
            invalid_capture.write_text(
                json.dumps(
                    [
                        {
                            "directory": str(ROOT),
                            "file": str(temporary_root / "copied-external.c"),
                            "arguments": [
                                "/usr/bin/cc",
                                "-std=c17",
                                "-Wall",
                                "-Wextra",
                                "-Werror",
                            ],
                            "output": str(output_root / "copied-external.o"),
                        }
                    ]
                ),
                encoding="utf-8",
            )
            invalid_result = self.run_cdb_tool(
                "--input",
                str(invalid_capture),
                "--output",
                str(database),
                "--merge-existing",
                "--require",
                "nginx",
            )
            self.assertNotEqual(invalid_result.returncode, 0)
            self.assertEqual(database.read_bytes(), original_database)

            checkout_output_result = self.run_cdb_tool(
                "--input",
                str(c_capture),
                "--output",
                str(ROOT / "compile_commands.json"),
                "--require",
                "nginx",
            )
            self.assertNotEqual(checkout_output_result.returncode, 0)
            self.assertIn("outside the checkout", checkout_output_result.stderr)


if __name__ == "__main__":
    unittest.main()
