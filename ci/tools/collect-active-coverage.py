#!/usr/bin/env python3
"""Run only the admitted coverage group and retain revision-bound real reports."""
from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from ci.lib.active_coverage import (CoverageError, compile_instrumented, digest,
                                    external_root, gcov_lines, go_lines,
                                    make_manifest, python_lines, regular_bytes,
                                    source_path, trace_python, validate_manifest,
                                    write_generic_report)
from ci.lib.active_test_inventory import (execute_selected, load_inventory,
                                         select_executions)

GENERIC_REPORT = "coverage.xml"
MANIFEST_REPORT = "manifest.json"


def git_output(*arguments: str) -> str:
    return subprocess.check_output(["git", *arguments], cwd=ROOT, text=True).strip()


def source_snapshot() -> dict[str, str]:
    raw = subprocess.check_output(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT)
    paths = sorted(set(raw.decode("utf-8").rstrip("\0").split("\0")))
    result = {}
    for name in paths:
        if (Path(name).suffix not in {".py", ".go", ".c", ".h", ".cc", ".cpp", ".sh"}
                and name not in {"config/testing/sonar-source-roles.json", ".sonarcloud.properties",
                                 "sonar-project.properties"}):
            continue
        result[name] = digest(regular_bytes(source_path(ROOT, name)))
    return result


def build_identity(selected: tuple[dict, ...]) -> dict:
    subprocess.run([sys.executable, str(ROOT / "ci/tools/sync-sonar-test-scope.py"), "--check"],
                   cwd=ROOT, check=True)
    result = {"python_version": sys.version, "python_executable": str(Path(sys.executable).resolve()),
              "python_sha256": digest(regular_bytes(Path(sys.executable).resolve())),
              "go_version": subprocess.check_output(["go", "version"], text=True).strip(),
              "modules": {}, "native_compilers": {}, "modsecurity": {},
              "analysis_inputs": {name: digest(regular_bytes(ROOT / name)) for name in
                                 ("config/testing/sonar-source-roles.json", ".sonarcloud.properties",
                                  "sonar-project.properties")}}
    for variable, default in (("CC", "cc"), ("CXX", "c++")):
        arguments = shlex.split(os.environ.get(variable, default))
        actual = shutil.which(arguments[0]) if arguments else None
        if actual is None:
            raise CoverageError("coverage requires an actual selected native compiler")
        binary = Path(actual).resolve(strict=True)
        version = subprocess.check_output([str(binary), "--version"], text=True).splitlines()[0]
        result["native_compilers"][variable] = {"path": str(binary), "sha256": digest(regular_bytes(binary)),
                                               "version": version}
    for item in selected:
        module = item["selector"].get("module")
        if module and module not in result["modules"]:
            result["modules"][module] = {name: (digest(regular_bytes(ROOT / module / name))
                                                  if (ROOT / module / name).exists() else None)
                                         for name in ("go.mod", "go.sum")}
    include = os.environ.get("MODSECURITY_INCLUDE_DIR")
    library = os.environ.get("MODSECURITY_LIB_FILE")
    if not include or not library:
        raise CoverageError("actual C++ coverage requires explicitly selected ModSecurity headers and library")
    for name in ("modsecurity.h", "rules_set.h", "transaction.h"):
        header = Path(include) / "modsecurity" / name
        result["modsecurity"][name] = digest(regular_bytes(header))
    result["modsecurity"]["library"] = str(Path(library).resolve(strict=True))
    result["modsecurity"]["library_sha256"] = digest(regular_bytes(Path(library).resolve(strict=True)))
    return result


def _github_outputs(output: Path, manifest: dict) -> None:
    names = [str(output / name) for name in manifest["reports"] if name.endswith("/go.out")]
    record = {"coverage_root": str(output), "generic_report": str(output / GENERIC_REPORT),
              "go_reports": ",".join(names), "manifest": str(output / MANIFEST_REPORT)}
    target = os.environ.get("GITHUB_OUTPUT")
    if target:
        with open(target, "a", encoding="utf-8") as stream:
            for name, value in record.items():
                if "\n" in value or "\r" in value:
                    raise CoverageError("coverage output path contains a control character")
                stream.write(f"{name}={value}\n")
    print(json.dumps(record, sort_keys=True))


def validate_execution_identity(inventory, selected: tuple[dict, ...], summary: dict,
                                revision: str, before: dict[str, str]) -> None:
    if summary["inventory_sha256"] != inventory.digest or load_inventory(ROOT).digest != inventory.digest:
        raise CoverageError("active inventory changed while coverage tests executed")
    if git_output("rev-parse", "HEAD") != revision or source_snapshot() != before:
        raise CoverageError("source/build identity changed during selected coverage execution")
    if len(summary["results"]) != len(selected) or any(result["status"] != "passed" for result in summary["results"]):
        raise CoverageError("coverage requires terminal successful selected executions")
    if any(result.get("observed", {}).get("skips", 0) for result in summary["results"]):
        raise CoverageError("coverage identity cannot promote skipped selected cases to executed evidence")


def collect_observations(selected: tuple[dict, ...], output: Path,
                         measurement: Path) -> tuple[dict, dict, list[str]]:
    observations: dict[str, dict[int, int]] = {}
    raw_reports = []
    go_sources: dict[str, dict[int, int]] = {}
    for execution in selected:
        directory = measurement / execution["id"]
        selector = execution["selector"]
        if selector["kind"] == "python":
            raw = directory / "python.json"
            python_lines(raw, ROOT, observations)
            raw_reports.append(raw.relative_to(output).as_posix())
        if selector["kind"] == "go":
            raw = directory / "go.out"
            go_lines(raw, ROOT, selector["module"], go_sources)
            raw_reports.append(raw.relative_to(output).as_posix())
        for raw in sorted((directory / "python-subprocess").glob("*.json")):
            record = json.loads(regular_bytes(raw))
            if record.get("target") != execution["id"] + ":subprocess":
                raise CoverageError("Python child record belongs to another execution")
            python_lines(raw, ROOT, observations)
            raw_reports.append(raw.relative_to(output).as_posix())
        for name in gcov_lines(directory, ROOT, observations):
            raw_reports.append((measurement / name).relative_to(output).as_posix())
    return observations, go_sources, raw_reports


def validate_measurements(selected: tuple[dict, ...], observations: dict,
                          go_sources: dict) -> dict:
    measured_python = [name for name in observations if name.endswith(".py")]
    measured_native = [name for name in observations if Path(name).suffix in {".c", ".cc", ".cpp", ".h"}]
    measured_cpp = "common/scripts/modsecurity_targeted_eval.cc" in observations
    if not measured_cpp:
        raise CoverageError("selected coverage must measure the actual C++ evaluator source")
    expected_modules = {item["selector"]["module"] for item in selected
                        if item["selector"]["kind"] == "go"}
    if not measured_python or not measured_native:
        raise CoverageError("selected coverage must produce real Python and native source observations")
    if not expected_modules or any(not any(name.startswith(module + "/") for name in go_sources)
                                   for module in expected_modules):
        raise CoverageError("selected coverage must produce actual profiles for every selected Go module")
    return {"python_sources": len(measured_python), "native_sources": len(measured_native),
            "cpp_evaluator": measured_cpp, "go_modules": sorted(expected_modules)}


def collect(output: Path, strict_skips: bool) -> int:
    inventory = load_inventory(ROOT)
    selected = select_executions(inventory, ("coverage",))
    external_root(output)
    if any(output.iterdir()):
        raise CoverageError("coverage collection requires a fresh empty output directory")
    revision = git_output("rev-parse", "HEAD")
    before = source_snapshot()
    build = build_identity(selected)
    dirty = bool(git_output("status", "--porcelain", "--untracked-files=normal"))
    summary = execute_selected(inventory, selected, output, strict_skips=strict_skips,
                               coverage_root=output)
    validate_execution_identity(inventory, selected, summary, revision, before)
    observations, go_sources, raw_reports = collect_observations(
        selected, output, Path(summary["coverage_directory"]))
    measurements = validate_measurements(selected, observations, go_sources)
    sources = write_generic_report(ROOT, observations, output / GENERIC_REPORT)
    # Go keeps its native statement-block format for Sonar's Go importer. It is
    # not inserted into generic XML as invented line-by-line execution hits.
    for relative in go_sources:
        sources.setdefault(relative, before[relative])
    # Generic report sources and native Go sources have separate importers; the
    # generic source binding remains exact, with additional Go files in metadata.
    generic_sources = dict(sources)
    for relative in go_sources:
        if relative not in observations:
            generic_sources.pop(relative, None)
    selected_cases = summary["selected_case_ids"]
    manifest = make_manifest(ROOT, output, revision, inventory.digest, selected_cases,
                             generic_sources, [GENERIC_REPORT, *raw_reports], dirty=dirty, build_identity=build)
    manifest["go_sources"] = {relative: before[relative] for relative in sorted(go_sources)}
    (output / MANIFEST_REPORT).write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _github_outputs(output, manifest)
    print("COVERAGE_GENERATED: " + json.dumps({"revision": revision,
          "inventory_sha256": inventory.digest, "case_count": len(selected_cases),
          "generic_sources": len(generic_sources), "go_sources": len(go_sources),
          "raw_report_count": len(raw_reports), **measurements,
          "dirty_worktree": dirty}, sort_keys=True))
    return 0


def verify(output: Path) -> int:
    inventory = load_inventory(ROOT)
    selected = select_executions(inventory, ("coverage",))
    value = json.loads(regular_bytes(output / MANIFEST_REPORT))
    go_sources = value.get("go_sources", {})
    if not isinstance(go_sources, dict) or not go_sources:
        raise CoverageError("coverage manifest is missing actual Go source measurements")
    for relative, expected in go_sources.items():
        if digest(regular_bytes(source_path(ROOT, relative))) != expected:
            raise CoverageError("measured Go source changed after its actual test build")
    validate_manifest(value, ROOT, output, git_output("rev-parse", "HEAD"), inventory.digest)
    if bool(git_output("status", "--porcelain", "--untracked-files=normal")):
        raise CoverageError("scanner import requires a clean source checkout")
    expected_cases = [case["id"] for item in selected for case in item["cases"]]
    if value["case_ids"] != expected_cases:
        raise CoverageError("coverage manifest does not bind the complete admitted coverage group")
    if value["build_identity"] != build_identity(selected):
        raise CoverageError("coverage toolchain, SDK or module dependency identity changed before scanner import")
    _github_outputs(output, value)
    print("COVERAGE_IDENTITY_VERIFIED")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("run", "verify"):
        command = commands.add_parser(name)
        command.add_argument("--output-root", type=Path, required=True)
        if name == "run":
            command.add_argument("--strict-skips", action="store_true")
    traced = commands.add_parser("trace-python")
    traced.add_argument("--target", required=True)
    traced.add_argument("--output", type=Path, required=True)
    compiler = commands.add_parser("compile")
    compiler.add_argument("arguments", nargs=argparse.REMAINDER)
    arguments = parser.parse_args()
    try:
        if arguments.command == "compile":
            return compile_instrumented(arguments.arguments)
        if arguments.command == "trace-python":
            return trace_python(arguments.target, arguments.output)
        if arguments.command == "verify":
            return verify(arguments.output_root)
        return collect(arguments.output_root, arguments.strict_skips)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"COVERAGE_REJECTED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
