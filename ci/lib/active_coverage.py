"""Collect real line observations for the admitted Parent active inventory.

No test is selected here. The inventory runner supplies exact admitted targets.
Eligible Python children retain real line observations without changing their
isolation flags; extracted native fixtures are not attributed to product files.
"""
from __future__ import annotations

import dis
from functools import lru_cache
import gzip
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shlex
import shutil
import stat
import subprocess
import sys
import trace
import types
import xml.etree.ElementTree as ET

from ci.lib.sonar_source_roles import is_test_source, load_roles

ROOT = Path(__file__).resolve().parents[2]
MAX_REPORT_BYTES = 64 * 1024 * 1024
SHA256 = re.compile(r"[a-f0-9]{64}", re.ASCII)
REVISION = re.compile(r"[a-f0-9]{40}", re.ASCII)
IDENTIFIER = re.compile(r"[a-z][a-z0-9_.-]{0,127}", re.ASCII)


class CoverageError(ValueError):
    """Coverage cannot be attributed to the selected source and execution."""


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def regular_bytes(path: Path, limit: int = MAX_REPORT_BYTES) -> bytes:
    """Read only a bounded ordinary artifact, rejecting symlinks and hardlinks."""
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(descriptor, "rb") as source:
        observed = os.fstat(source.fileno())
        if (not stat.S_ISREG(observed.st_mode) or observed.st_nlink != 1 or
                observed.st_size > limit):
            raise CoverageError("coverage input must be a bounded single-link regular file")
        value = source.read(limit + 1)
    if len(value) > limit:
        raise CoverageError("coverage input exceeds its size limit")
    return value


def safe_relative(value: str) -> PurePosixPath:
    if (not isinstance(value, str) or not value or "\\" in value or
            any(part in {"", ".", ".."} for part in value.split("/"))):
        raise CoverageError("coverage source path must be canonical and repository-relative")
    path = PurePosixPath(value)
    if path.is_absolute():
        raise CoverageError("coverage source path must be repository-relative")
    return path


def source_path(root: Path, relative: str) -> Path:
    path = root / safe_relative(relative)
    current = root
    for part in path.relative_to(root).parts:
        current = current / part
        if current.is_symlink():
            raise CoverageError("coverage source must not traverse symlinks")
    if not path.is_file() or path.resolve(strict=True) != path:
        raise CoverageError("coverage source must be a current regular repository file")
    return path


def external_root(path: Path) -> Path:
    """Require an existing canonical current-user external evidence directory."""
    if not path.is_absolute() or ".." in path.parts or path.resolve(strict=True) != path:
        raise CoverageError("coverage output root must be canonical and absolute")
    if path == ROOT or ROOT in path.parents or path == Path(path.anchor):
        raise CoverageError("coverage output must be outside the source checkout")
    for component in [*reversed(path.parents), path]:
        observed = component.lstat()
        if not stat.S_ISDIR(observed.st_mode) or observed.st_uid not in (0, os.geteuid()):
            raise CoverageError("coverage output ancestry must be trusted non-symlink directories")
        public_ancestor = (component != path and observed.st_uid == 0 and
                           observed.st_mode & stat.S_ISVTX)
        if observed.st_mode & 0o022 and not public_ancestor:
            raise CoverageError("coverage output ancestry must not be replaceable by other users")
    if path.stat().st_uid != os.geteuid():
        raise CoverageError("coverage output must belong to the executing user")
    return path


def execution_directory(output_root: Path, execution_id: str) -> Path:
    if IDENTIFIER.fullmatch(execution_id) is None:
        raise CoverageError("coverage execution ID must be a fixed inventory identifier")
    root = external_root(output_root)
    child = root / execution_id
    child.mkdir(mode=0o700, exist_ok=True)
    external_root(child)
    return child


def python_command(target: str, output_root: Path, execution_id: str,
                   strict_skips: bool = False) -> list[str]:
    del strict_skips  # The inventory parent audits the same child summary.
    directory = execution_directory(output_root, execution_id)
    return [sys.executable, str(ROOT / "ci/tools/collect-active-coverage.py"),
            "trace-python", "--target", target, "--output", str(directory / "python.json")]


def _compiler_wrapper(directory: Path, variable: str, default: str) -> Path:
    compiler = shlex.split(os.environ.get(variable, default))
    if not compiler or shutil.which(compiler[0]) is None:
        raise CoverageError("native coverage requires the selected actual compiler")
    wrapper = directory / ("coverage-" + variable.lower())
    text = "#!/bin/sh\nexec " + shlex.join([
        sys.executable, str(ROOT / "ci/tools/collect-active-coverage.py"),
        "compile", "--", *compiler]) + ' "$@"\n'
    if wrapper.exists():
        if regular_bytes(wrapper).decode("utf-8") != text:
            raise CoverageError("coverage compiler wrapper changed during this execution")
    else:
        descriptor = os.open(wrapper, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o700)
        with os.fdopen(descriptor, "w", encoding="utf-8") as output:
            output.write(text)
    return wrapper


def coverage_environment(output_root: Path, execution_id: str) -> dict[str, str]:
    from ci.lib.python_coverage_bootstrap import provision_bootstrap

    directory = execution_directory(output_root, execution_id)
    notes = directory / "gcov-notes"
    data = directory / "gcov-data"
    notes.mkdir(mode=0o700, exist_ok=True)
    data.mkdir(mode=0o700, exist_ok=True)
    cc = _compiler_wrapper(directory, "CC", "cc")
    cxx = _compiler_wrapper(directory, "CXX", "c++")
    environment = {"CC": str(cc), "CXX": str(cxx), "ACTIVE_COVERAGE_NOTES": str(notes),
                   "GCOV_PREFIX": str(data), "GCOV_PREFIX_STRIP": "0",
                   "PYTHONNOUSERSITE": "1", "PYTHONDONTWRITEBYTECODE": "1"}
    environment.update(provision_bootstrap(directory, ROOT, execution_id,
                                           test_patterns=_source_roles().patterns))
    return environment


def go_coverage_arguments(output_root: Path, execution_id: str) -> list[str]:
    directory = execution_directory(output_root, execution_id)
    return ["-covermode=atomic", "-coverpkg=./...",
            "-coverprofile=" + str(directory / "go.out")]


def _compiler_note_paths(arguments: list[str], binary: Path, output_index: int) -> list[Path]:
    # GCC's direct-link auxiliary name is output-name + source-basename.
    # Select exact current inputs, not a directory glob or a prefix: notes for
    # smoke-asan are unrelated when compiling smoke, despite that shared prefix.
    # A compile-only output instead replaces its object suffix with .gcno.
    if "-c" in arguments:
        return [binary.with_suffix(".gcno")]
    source_suffixes = {".c", ".i", ".cc", ".cp", ".cxx", ".cpp", ".CPP", ".c++", ".C", ".ii"}
    return [binary.parent / (binary.name + "-" + Path(argument).stem + ".gcno")
            for position, argument in enumerate(arguments)
            if position != output_index + 1 and not argument.startswith("-")
            and Path(argument).suffix in source_suffixes and Path(argument).is_file()]


def compile_instrumented(arguments: list[str]) -> int:
    if arguments and arguments[0] == "--":
        arguments = arguments[1:]
    if not arguments or "-o" not in arguments:
        raise CoverageError("coverage compiler requires an explicit output file")
    index = arguments.index("-o")
    if index + 1 >= len(arguments):
        raise CoverageError("coverage compiler output file is missing")
    binary = Path(arguments[index + 1]).absolute()
    notes = external_root(Path(os.environ["ACTIVE_COVERAGE_NOTES"]))
    result = subprocess.run([*arguments, "--coverage", "-fprofile-abs-path",
                             "-DMSCONNECTOR_ACTIVE_GCOV=1"], check=False)
    if result.returncode:
        return result.returncode
    # Preserve original path layout to pair only these compiler outputs with
    # their GCOV_PREFIX counters after test-owned temporary directories vanish.
    for candidate in _compiler_note_paths(arguments, binary, index):
        if not candidate.exists():
            continue
        relative = candidate.absolute().relative_to(candidate.anchor)
        destination = notes / relative
        destination.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        data = regular_bytes(candidate)
        if destination.exists() and regular_bytes(destination) != data:
            raise CoverageError("compiler notes collide for different native source builds")
        if not destination.exists():
            destination.write_bytes(data)
    return 0


@lru_cache(maxsize=1)
def _source_roles():
    return load_roles(ROOT)


@lru_cache(maxsize=8192)
def _is_test_source(relative: str, root: Path = ROOT) -> bool:
    return is_test_source(relative, _source_roles(), root=root)


def _is_python_product(relative: str, root: Path = ROOT) -> bool:
    path = PurePosixPath(relative)
    return (path.suffix == ".py" and path.parts[0] not in {"tests", "modules", ".codex"}
            and not _is_test_source(relative, root))


def _executable_lines(code: types.CodeType) -> set[int]:
    # Since Python 3.13, dis.findlinestarts() includes None for artificial
    # bytecode with no source line. Such instructions (and line 0 metadata)
    # are not executable source lines and must never become report entries.
    result = {line for _, line in dis.findlinestarts(code)
              if line is not None and line > 0}
    for constant in code.co_consts:
        if isinstance(constant, types.CodeType):
            result.update(_executable_lines(constant))
    return result


def trace_python(target: str, output: Path) -> int:
    # Import only the same exact child entry point used by the inventory runner.
    from ci.lib.active_test_inventory import load_inventory, python_child
    inventory = load_inventory(ROOT)
    execution_id = os.environ.get("ACTIVE_TEST_EXECUTION")
    admitted = [item for item in inventory.executions if item["id"] == execution_id
                and item["selector"] == {"kind": "python", "target": target}]
    if (len(admitted) != 1 or
            os.environ.get("ACTIVE_TEST_INVENTORY_SHA256") != inventory.digest):
        raise CoverageError("traced Python child must match its fully admitted inventory execution")
    external_root(output.parent)
    if output.exists():
        raise CoverageError("Python coverage output must be fresh")
    tracer = trace.Trace(count=True, trace=False, ignoredirs=[sys.base_prefix])
    result = tracer.runfunc(python_child, target)
    observed: dict[str, dict[str, int]] = {}
    for (filename, line), count in tracer.results().counts.items():
        path = Path(filename)
        if not path.is_absolute() or not path.is_relative_to(ROOT):
            continue
        relative = path.relative_to(ROOT).as_posix()
        if _is_python_product(relative) and count > 0:
            source_path(ROOT, relative)
            observed.setdefault(relative, {})[str(line)] = count
    payload = {"schema_version": 1, "target": target, "files": observed}
    output.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
    return result


def add_lines(lines: dict[str, dict[int, int]], path: str, observations: dict[int, int]) -> None:
    target = lines.setdefault(path, {})
    for line, count in observations.items():
        if type(line) is not int or type(count) is not int or line < 1 or count < 0:
            raise CoverageError("coverage observations require positive line numbers and nonnegative counts")
        target[line] = target.get(line, 0) + count


def python_lines(path: Path, root: Path, lines: dict[str, dict[int, int]]) -> None:
    value = json.loads(regular_bytes(path))
    if set(value) != {"schema_version", "target", "files"} or value["schema_version"] != 1:
        raise CoverageError("invalid Python trace report schema")
    for relative, observations in value["files"].items():
        source = source_path(root, relative)
        if not _is_python_product(relative, root):
            raise CoverageError("Python coverage report includes test or external source")
        code = compile(regular_bytes(source), str(source), "exec")
        executable = _executable_lines(code)
        hits = {int(line): count for line, count in observations.items()}
        if not hits.keys() <= executable:
            raise CoverageError("Python trace refers to a non-executable source line")
        add_lines(lines, relative, {line: hits.get(line, 0) for line in executable})


def go_lines(profile: Path, root: Path, module: str,
             lines: dict[str, dict[int, int]]) -> None:
    content = regular_bytes(profile).decode("utf-8").splitlines()
    if not content or content[0] not in {"mode: set", "mode: count", "mode: atomic"}:
        raise CoverageError("invalid Go coverage mode")
    declaration = (root / module / "go.mod").read_text(encoding="utf-8")
    match = re.search(r"^module\s+(\S+)\s*$", declaration, re.MULTILINE)
    if match is None:
        raise CoverageError("Go coverage module has no exact module declaration")
    prefix = match.group(1) + "/"
    for entry in content[1:]:
        block = re.fullmatch(r"(.+):(\d+)\.(\d+),(\d+)\.(\d+) (\d+) (\d+)", entry)
        if block is None or not block.group(1).startswith(prefix):
            raise CoverageError("Go coverage source is outside the selected actual module")
        relative = module + "/" + block.group(1)[len(prefix):]
        source = source_path(root, relative)
        first, end, count = int(block.group(2)), int(block.group(4)), int(block.group(7))
        line_count = len(regular_bytes(source).splitlines())
        if first < 1 or end < first or end > line_count:
            raise CoverageError("Go coverage block exceeds the current source")
        # Native profiles retain the exact block format as raw evidence. Generic
        # line coverage reports the lines spanned by those measured Go blocks.
        add_lines(lines, relative, {line: count for line in range(first, end + 1)})


def _gcov_source_lines(value: dict, root: Path, lines: dict[str, dict[int, int]]) -> None:
    for measured in value.get("files", []):
        source = Path(measured["file"])
        if not source.is_absolute() or not source.is_relative_to(root):
            continue
        name = source.relative_to(root).as_posix()
        if (source.suffix not in {".c", ".cc", ".cpp", ".h"} or
                name.startswith("modules/") or _is_test_source(name, root)):
            continue
        current = source_path(root, name)
        limit = len(regular_bytes(current).splitlines())
        observed = {item["line_number"]: item["count"] for item in measured["lines"]}
        if any(type(number) is not int or not 1 <= number <= limit for number in observed):
            raise CoverageError("gcov line does not belong to the current actual source")
        add_lines(lines, name, observed)


def _gcov_note_reports(tool: str, note: Path, counter: Path, paired: Path) -> list[Path]:
    paired.mkdir(mode=0o700, exist_ok=True)
    local_note = paired / note.name
    local_note.write_bytes(regular_bytes(note))
    local_note.with_suffix(".gcda").write_bytes(regular_bytes(counter))
    result = subprocess.run([tool, "--json-format", str(local_note)], cwd=paired,
                            capture_output=True, text=True, check=False, timeout=60)
    if result.returncode:
        raise CoverageError("gcov could not read the fresh matching notes and execution counters")
    files = list(paired.glob("*.gcov.json.gz"))
    if not files:
        raise CoverageError("gcov did not emit its documented JSON report")
    return files


def gcov_lines(directory: Path, root: Path,
               lines: dict[str, dict[int, int]]) -> list[str]:
    notes = directory / "gcov-notes"
    if not notes.is_dir():
        return []
    reports = directory / "gcov-json"
    reports.mkdir(mode=0o700, exist_ok=True)
    tool = shutil.which("gcov")
    if tool is None:
        raise CoverageError("native coverage notes exist but gcov is unavailable")
    generated: list[str] = []
    for note in sorted(notes.rglob("*.gcno")):
        relative = note.relative_to(notes)
        counter = directory / "gcov-data" / relative.with_suffix(".gcda")
        if not counter.is_file():
            continue  # Unexecuted alternate fixture is not evidence of a run.
        paired = reports / digest(relative.as_posix().encode("utf-8"))
        for compressed in _gcov_note_reports(tool, note, counter, paired):
            with gzip.open(compressed, "rb") as report:
                raw = report.read(MAX_REPORT_BYTES + 1)
            if len(raw) > MAX_REPORT_BYTES:
                raise CoverageError("gcov JSON exceeds the report limit")
            _gcov_source_lines(json.loads(raw), root, lines)
            generated.append(compressed.relative_to(directory.parent).as_posix())
    return generated


def write_generic_report(root: Path, lines: dict[str, dict[int, int]], destination: Path) -> dict[str, str]:
    report = ET.Element("coverage", {"version": "1"})
    sources: dict[str, str] = {}
    for relative, observations in sorted(lines.items()):
        source = source_path(root, relative)
        raw = regular_bytes(source)
        line_count = len(raw.splitlines())
        if not observations or any(number > line_count for number in observations):
            raise CoverageError("coverage report has missing or out-of-range source observations")
        sources[relative] = digest(raw)
        element = ET.SubElement(report, "file", {"path": relative})
        for number, count in sorted(observations.items()):
            if type(number) is not int or type(count) is not int or number < 1 or count < 0:
                raise CoverageError("invalid actual coverage line observation")
            ET.SubElement(element, "lineToCover", {"lineNumber": str(number),
                                                   "covered": "true" if count > 0 else "false"})
    if not sources:
        raise CoverageError("selected executions produced no measurable production source coverage")
    ET.ElementTree(report).write(destination, encoding="utf-8", xml_declaration=True)
    return sources


def make_manifest(root: Path, output: Path, revision: str, inventory_digest: str,
                  case_ids: list[str], sources: dict[str, str], reports: list[str],
                  dirty: bool = False, build_identity: dict | None = None) -> dict:
    if REVISION.fullmatch(revision) is None or SHA256.fullmatch(inventory_digest) is None:
        raise CoverageError("coverage identity requires full source revision and inventory digest")
    if not case_ids or len(case_ids) != len(set(case_ids)):
        raise CoverageError("coverage identity requires actual unique selected case IDs")
    artifacts = {name: digest(regular_bytes(output / safe_relative(name))) for name in reports}
    manifest = {"schema_version": 1, "revision": revision,
                "inventory_sha256": inventory_digest, "case_ids": case_ids,
                "dirty_worktree": dirty, "sources": sources, "go_sources": {}, "reports": artifacts, "build_identity": build_identity or {},
                "measurement": {"python": "actual admitted line traces; eligible same-prefix/UID children; isolated, clean-environment and killed children may be unmeasured",
                                "go": "actual selected go test statement-block profiles imported by the native Go importer",
                                "native": "GCC/gcov actual source units only; extracted temporary fixtures are unmeasured",
                                "cpp": "GCC/gcov from the admitted actual targeted evaluator; no host lifecycle claim"}}
    validate_manifest(manifest, root, output, revision, inventory_digest, require_clean=False)
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def _validate_manifest_identity(value: dict, revision: str, inventory_digest: str,
                                require_clean: bool) -> None:
    expected = {"schema_version", "revision", "inventory_sha256", "case_ids",
                "dirty_worktree", "sources", "go_sources", "reports", "build_identity", "measurement"}
    if not isinstance(value, dict) or set(value) != expected or value["schema_version"] != 1:
        raise CoverageError("coverage manifest uses an invalid closed schema")
    if value["revision"] != revision:
        raise CoverageError("coverage report belongs to another source revision")
    if value["inventory_sha256"] != inventory_digest:
        raise CoverageError("coverage report belongs to another active inventory")
    if type(value["dirty_worktree"]) is not bool or require_clean and value["dirty_worktree"]:
        raise CoverageError("scanner import requires the exact clean published source revision")


def _validate_file_observations(element: ET.Element, root: Path) -> None:
    if element.tag != "file" or set(element.attrib) != {"path"}:
        raise CoverageError("generic coverage file has an invalid source identity")
    limit = len(regular_bytes(source_path(root, element.attrib["path"])).splitlines())
    observed = set()
    for line in element:
        if (line.tag != "lineToCover" or set(line.attrib) != {"lineNumber", "covered"}
                or line.attrib["covered"] not in {"true", "false"}):
            raise CoverageError("generic coverage line has an invalid observation")
        number = int(line.attrib["lineNumber"])
        if number in observed or not 1 <= number <= limit:
            raise CoverageError("generic coverage line is duplicated or out of range")
        observed.add(number)
    if not observed:
        raise CoverageError("generic coverage source has no measured executable lines")


def _validate_generic(value: dict, root: Path, output: Path) -> None:
    element = ET.fromstring(regular_bytes(output / "coverage.xml"))
    if element.tag != "coverage" or element.attrib != {"version": "1"}:
        raise CoverageError("scanner coverage report must use generic coverage format version1")
    names = [item.attrib.get("path") for item in element]
    if len(names) != len(set(names)) or set(names) != set(value["sources"]):
        raise CoverageError("coverage report and measured source manifest disagree")
    for source in element:
        _validate_file_observations(source, root)


def _validate_source_bindings(value: dict, root: Path) -> None:
    if not isinstance(value["sources"], dict) or not value["sources"]:
        raise CoverageError("coverage manifest must bind measured actual production sources")
    if not isinstance(value["go_sources"], dict):
        raise CoverageError("Go source binding must be a source digest mapping")
    for name, expected_digest in value["sources"].items():
        if digest(regular_bytes(source_path(root, name))) != expected_digest:
            raise CoverageError("measured source changed after coverage generation")
    for name, expected_digest in value["go_sources"].items():
        if digest(regular_bytes(source_path(root, name))) != expected_digest:
            raise CoverageError("measured Go source changed after coverage generation")


def validate_manifest(value: dict, root: Path, output: Path, revision: str,
                      inventory_digest: str, require_clean: bool = True) -> None:
    _validate_manifest_identity(value, revision, inventory_digest, require_clean)
    _validate_source_bindings(value, root)
    if not isinstance(value["reports"], dict) or "coverage.xml" not in value["reports"]:
        raise CoverageError("coverage manifest must bind its actual scanner report")
    for name, expected_digest in value["reports"].items():
        path = output / safe_relative(name)
        if path.is_symlink() or digest(regular_bytes(path)) != expected_digest:
            raise CoverageError("coverage artifact changed after generation")
    _validate_generic(value, root, output)
