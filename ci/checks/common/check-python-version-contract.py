#!/usr/bin/env python3
"""Statically enforce the Parent's Python workflow-selection contract.

This intentionally understands only the small, stable YAML shape used by the
checked-in GitHub Actions workflows.  It does not deserialize YAML or execute
workflow content; unsupported/ambiguous contract shapes fail closed.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import re
import stat
import sys
import textwrap
from typing import Iterable, Sequence


EXACT_PYTHON_313 = re.compile(r"3\.13\.(?:0|[1-9][0-9]*)\Z")
CANONICAL_VERSION_FILE = ".python-version"
SETUP_PYTHON_ACTION = "actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1"
SETUP_PYTHON_RELEASE_COMMENT = "# v6.3.0"
SETUP_PYTHON_REFERENCE = f"{SETUP_PYTHON_ACTION} {SETUP_PYTHON_RELEASE_COMMENT}"
VERIFIER_NAME = "Verify Python interpreter contract"
CANDIDATE_VERIFIER_NAME = "Verify Python candidate interpreter contract"
VERIFIER_PATH = "ci/checks/common/check-python-interpreter-contract.py"
SETUP_PYTHON_OUTPUT = "${{ steps.setup-python.outputs.python-path }}"
CANDIDATE_VERSION_OUTPUT = "${{ needs.resolve-python-patch.outputs.version }}"
NORMAL_VERIFIER_COMMAND = (
    f'python3 {VERIFIER_PATH} --version-file .python-version '
    '--expected-python "$EXPECTED_PYTHON"'
)
CANDIDATE_VERIFIER_COMMAND = (
    f'python3 {VERIFIER_PATH} --expected-version "$EXPECTED_VERSION" '
    '--expected-python "$EXPECTED_PYTHON"'
)


@dataclass(frozen=True, order=True)
class JobIdentity:
    """A stable workflow filename/job-ID pair used by the inventory contract."""

    workflow: str
    job: str

    def display(self) -> str:
        return f"{self.workflow}:{self.job}"


# These are the final Parent-native Python jobs: the current 22 jobs plus the
# resolver and publisher in update-python-version.yml.  The one candidate job
# below is deliberately separate because it must validate a prospective patch
# before the canonical .python-version file is changed.
EXPECTED_NORMAL_PYTHON_JOBS = frozenset(
    {
        JobIdentity("all-connectors-no-crs.yml", "aggregate"),
        JobIdentity("all-connectors-no-crs.yml", "no-crs"),
        JobIdentity("check-actions-versions.yml", "check-actions-versions"),
        JobIdentity("ci-security-secrets.yml", "advisory-full-history"),
        JobIdentity("ci-security-secrets.yml", "pull-request-range"),
        JobIdentity("ci-security-workflow-lint.yml", "actionlint"),
        JobIdentity("ci-security-workflow-lint.yml", "zizmor"),
        JobIdentity("lint.yml", "scaffold-lint"),
        JobIdentity("open-connectors-smoke.yml", "open-connectors-smoke"),
        JobIdentity("protocol-contract.yml", "nginx-profile-and-client-preflight"),
        JobIdentity("protocol-contract.yml", "protocol-contract"),
        JobIdentity("quick-framework-check.yml", "quick-check"),
        JobIdentity("test-apache.yml", "apache-structure"),
        JobIdentity("test-common.yml", "common-structure"),
        JobIdentity("test-envoy.yml", "envoy-contract"),
        JobIdentity("test-full-smoke-sequential.yml", "manual-heavy-runtime-validation"),
        JobIdentity("test-lighttpd.yml", "lighttpd-contract"),
        JobIdentity("test-nginx.yml", "nginx-structure"),
        JobIdentity("test-traefik.yml", "traefik-contract"),
        JobIdentity("update-actions-versions.yml", "update-actions-versions"),
        JobIdentity("update-python-version.yml", "create-python-update-pr"),
        JobIdentity("update-python-version.yml", "resolve-python-patch"),
        JobIdentity("update-submodules.yml", "validate-submodule-update"),
        JobIdentity("verified-report-governance.yml", "report-governance"),
    }
)

# This is intentionally an exact pair, not a filename/job-name pattern.  It
# does not permit ambient Python: the candidate version and setup-python path
# are both checked by the stricter verifier shape below.
CANDIDATE_VALIDATION_JOB = JobIdentity(
    "update-python-version.yml", "validate-python-patch"
)

# The list is intentionally explicit.  Broadly classifying every Make target
# as Python-bearing would both create false positives and conceal an inventory
# decision.  Each target here invokes Parent/Framework Python in the current
# workflow contract.
KNOWN_PYTHON_MAKE_TARGETS = frozenset(
    {
        "capabilities-all-connectors-evidence",
        "check-envoy-common-adoption",
        "check-lighttpd-common-adoption",
        "check-remaining-connectors-build-wiring",
        "check-remaining-connectors-claim-policy",
        "check-remaining-connectors-common-adoption",
        "check-remaining-connectors-host-integration",
        "check-remaining-connectors-start-wiring",
        "check-test-matrix",
        "check-traefik-common-adoption",
        "codex-check",
        "generate-test-matrix",
        "install-dev-deps",
        "lint",
        "quick-check",
        "readiness-remaining-connectors",
        "report-governance",
        "setup-dev",
        "test-no-crs",
        "test-protocol-client",
        "test-with-crs",
    }
)

# Match executable basenames after a shell command boundary.  The code below
# deliberately does not search arbitrary shell text: `echo python3`, comments,
# and here-document bodies are not interpreter executions.  Versioned and
# absolute/venv forms remain covered through `is_python_or_pip_command()`.
PYTHON_OR_PIP_BASENAME = re.compile(
    r"(?:python(?:[0-9]+(?:\.[0-9]+)*)?|pip(?:[0-9]+(?:\.[0-9]+)*)?)\Z"
)
MAX_SHELL_SOURCE_LENGTH = 131_072
MAX_SHELL_NESTING = 32
SHELL_CONTROL_WORDS = frozenset(
    {
        "!",
        "{",
        "}",
        "do",
        "done",
        "elif",
        "else",
        "esac",
        "fi",
        "for",
        "function",
        "if",
        "in",
        "then",
        "time",
        "until",
        "while",
    }
)
SHELL_COMMAND_OPTION_ONLY = frozenset({"-v", "-V"})
SHELL_OPTIONS_WITH_VALUE = frozenset(
    {
        "-C",
        "-g",
        "-h",
        "-p",
        "-r",
        "-t",
        "-u",
        "--chdir",
        "--group",
        "--host",
        "--prompt",
        "--role",
        "--user",
    }
)
PYTHON_MATRIX_KEY = re.compile(
    r"^\s*(?:-\s*)?python(?:[-_]?versions?)?\s*:", re.IGNORECASE
)
PYTHON_MATRIX_REFERENCE = re.compile(
    r"\bmatrix\.python(?:[-_]?versions?)?\b", re.IGNORECASE
)
VERIFIER_COMMAND_LINE = re.compile(
    rf"(?m)^\s*python3\s+{re.escape(VERIFIER_PATH)}\b[^\n]*$"
)


class ContractInputError(ValueError):
    """Raised for invalid command input or an unusable canonical version file."""


@dataclass
class Step:
    index: int
    start_line: int
    indent: int
    lines: list[tuple[int, str]]

    def scalar(self, key: str) -> str | None:
        for position, (_, line) in enumerate(self.lines):
            indent = indentation(line)
            tail = line[indent:]
            if position == 0 and indent == self.indent and tail.startswith("- "):
                tail = tail[2:]
            elif indent != self.indent + 2:
                continue
            entry = mapping_entry(tail)
            if entry is not None and entry[0] == key:
                return clean_scalar(entry[1])
        return None

    def raw_scalar(self, key: str) -> str | None:
        """Return the unnormalized scalar text for a direct step mapping key.

        The setup-python provenance comment is part of this contract, so it
        must be checked before `clean_scalar()` removes a YAML comment.
        """

        for position, (_, line) in enumerate(self.lines):
            indent = indentation(line)
            tail = line[indent:]
            if position == 0 and indent == self.indent and tail.startswith("- "):
                tail = tail[2:]
            elif indent != self.indent + 2:
                continue
            entry = mapping_entry(tail)
            if entry is not None and entry[0] == key:
                return entry[1].strip()
        return None

    def nested_mapping(self, key: str) -> dict[str, str]:
        for position, (_, line) in enumerate(self.lines):
            indent = indentation(line)
            tail = line[indent:]
            if position == 0 and indent == self.indent and tail.startswith("- "):
                tail = tail[2:]
            elif indent != self.indent + 2:
                continue
            entry = mapping_entry(tail)
            if entry is None or entry[0] != key:
                continue

            result: dict[str, str] = {}
            for _, child_line in self.lines[position + 1 :]:
                child_indent = indentation(child_line)
                if child_line.strip() and child_indent <= indent:
                    break
                if child_indent != indent + 2:
                    continue
                child_entry = mapping_entry(child_line[child_indent:])
                if child_entry is not None:
                    result[child_entry[0]] = clean_scalar(child_entry[1])
            return result
        return {}

    def run(self) -> str:
        for position, (_, line) in enumerate(self.lines):
            indent = indentation(line)
            tail = line[indent:]
            if position == 0 and indent == self.indent and tail.startswith("- "):
                tail = tail[2:]
            elif indent != self.indent + 2:
                continue
            entry = mapping_entry(tail)
            if entry is None or entry[0] != "run":
                continue
            value = clean_scalar(entry[1])
            if not value.startswith(("|", ">")):
                return value

            body: list[str] = []
            for _, child_line in self.lines[position + 1 :]:
                child_indent = indentation(child_line)
                if child_line.strip() and child_indent <= indent:
                    break
                body.append(child_line)
            return textwrap.dedent("\n".join(body)).strip()
        return ""


@dataclass
class Job:
    identity: JobIdentity
    indent: int
    lines: list[tuple[int, str]]

    def scalar(self, key: str) -> str | None:
        """Return a direct job-level scalar without descending into steps."""

        for _, line in self.lines[1:]:
            indent = indentation(line)
            if indent != self.indent + 2:
                continue
            entry = mapping_entry(line[indent:])
            if entry is not None and entry[0] == key:
                return clean_scalar(entry[1])
        return None

    def steps(self) -> list[Step]:
        steps_line = None
        for position, (_, line) in enumerate(self.lines):
            if indentation(line) == self.indent + 2 and line.strip() == "steps:":
                steps_line = position
                break
        if steps_line is None:
            return []

        step_indent = self.indent + 4
        result: list[Step] = []
        current: list[tuple[int, str]] | None = None
        current_start = 0
        for line_number, line in self.lines[steps_line + 1 :]:
            indent = indentation(line)
            if line.strip() and indent <= self.indent + 2:
                break
            if indent == step_indent and line[indent:].startswith("- "):
                if current is not None:
                    result.append(
                        Step(len(result), current_start, step_indent, current)
                    )
                current = [(line_number, line)]
                current_start = line_number
            elif current is not None:
                current.append((line_number, line))
        if current is not None:
            result.append(Step(len(result), current_start, step_indent, current))
        return result


def indentation(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def is_mapping_key(value: str) -> bool:
    """Return whether *value* is in the deliberately narrow YAML key subset."""

    return bool(value) and all(
        character.isascii() and (character.isalnum() or character in "_-")
        for character in value
    )


def mapping_entry(value: str) -> tuple[str, str] | None:
    """Parse the small ``key: value`` YAML shape used by this checker.

    This deliberately avoids a general YAML parser and regular-expression
    backtracking.  It accepts exactly the former contract's ASCII key subset,
    keeps colons in the value, and leaves scalar normalization to
    :func:`clean_scalar`.
    """

    separator = value.find(":")
    if separator <= 0:
        return None
    key = value[:separator]
    if not is_mapping_key(key):
        return None
    return key, value[separator + 1 :].lstrip()


def job_header(value: str) -> str | None:
    """Return a narrow job key when *value* is a YAML job header."""

    entry = mapping_entry(value)
    if entry is None:
        return None
    key, remainder = entry
    if not remainder or remainder.startswith("#"):
        return key
    return None


def clean_scalar(value: str) -> str:
    """Normalize the scalar forms used by the checked-in workflow contract."""

    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    if " #" in value:
        value = value.split(" #", 1)[0].rstrip()
    return value


def repository_root() -> Path:
    return next(parent for parent in Path(__file__).resolve().parents if (parent / "Makefile").is_file())


def parse_exact_version(value: str, source: str) -> str:
    if not EXACT_PYTHON_313.fullmatch(value):
        raise ContractInputError(
            f"{source} must be an exact Python 3.13.N version; got {value!r}"
        )
    return value


def canonical_version_file(root: Path) -> Path:
    """Return the one regular, non-symlink canonical version file.

    The public CLI intentionally does not accept a user-selected root or
    version-file path.  This helper is kept separate so in-process tests can
    supply an isolated repository root without widening the command boundary.
    """

    candidate = root / CANONICAL_VERSION_FILE
    try:
        metadata = candidate.lstat()
    except OSError as exc:
        raise ContractInputError(
            f"cannot inspect canonical version file {candidate}: {exc}"
        ) from exc
    if stat.S_ISLNK(metadata.st_mode):
        raise ContractInputError(f"canonical version file must not be a symlink: {candidate}")
    if not stat.S_ISREG(metadata.st_mode):
        raise ContractInputError(f"canonical version file must be a regular file: {candidate}")
    return candidate


def read_canonical_version(path: Path) -> str:
    try:
        metadata = path.lstat()
    except OSError as exc:
        raise ContractInputError(f"cannot inspect canonical version file {path}: {exc}") from exc
    if stat.S_ISLNK(metadata.st_mode):
        raise ContractInputError(f"canonical version file must not be a symlink: {path}")
    if not stat.S_ISREG(metadata.st_mode):
        raise ContractInputError(f"canonical version file must be a regular file: {path}")
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ContractInputError(f"cannot read canonical version file {path}: {exc}") from exc
    if content.endswith("\n"):
        content = content[:-1]
    if "\n" in content or "\r" in content:
        raise ContractInputError(
            f"canonical version file {path} must contain one exact version and an optional final newline"
        )
    return parse_exact_version(content, f"canonical version file {path}")


def version_tuple(value: str) -> tuple[int, int, int]:
    major, minor, patch = (int(part) for part in value.split("."))
    return major, minor, patch


def workflow_files(root: Path) -> tuple[list[Path], list[str]]:
    workflows = root / ".github" / "workflows"
    if not workflows.is_dir():
        raise ContractInputError(f"workflow directory is missing: {workflows}")

    paths = sorted({*workflows.glob("*.yml"), *workflows.glob("*.yaml")})
    result: list[Path] = []
    violations: list[str] = []
    for path in paths:
        if path.is_symlink():
            violations.append(f"workflow must not be a symlink: {path.relative_to(root)}")
        elif path.is_file():
            result.append(path)
    return result, violations


def parse_jobs(path: Path) -> tuple[dict[JobIdentity, Job], list[str]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError as exc:
        return {}, [f"cannot decode workflow {path.name}: {exc}"]
    except OSError as exc:
        return {}, [f"cannot read workflow {path.name}: {exc}"]

    jobs_start = None
    for index, line in enumerate(lines):
        if indentation(line) == 0 and line.strip() == "jobs:":
            jobs_start = index
            break
    if jobs_start is None:
        return {}, []

    result: dict[JobIdentity, Job] = {}
    violations: list[str] = []
    job_indent: int | None = None
    current_identity: JobIdentity | None = None
    current_lines: list[tuple[int, str]] = []

    def finish_current() -> None:
        if current_identity is None:
            return
        if current_identity in result:
            violations.append(f"duplicate workflow job: {current_identity.display()}")
            return
        assert job_indent is not None
        result[current_identity] = Job(current_identity, job_indent, list(current_lines))

    for line_number, line in enumerate(lines[jobs_start + 1 :], start=jobs_start + 2):
        if line.strip() and indentation(line) == 0:
            break
        if not line.strip():
            if current_identity is not None:
                current_lines.append((line_number, line))
            continue
        indent = indentation(line)
        if indent <= 0:
            continue
        header = job_header(line[indent:])
        if job_indent is None and header is not None:
            job_indent = indent
        if job_indent is not None and indent == job_indent and header is not None:
            finish_current()
            current_identity = JobIdentity(path.name, header)
            current_lines = [(line_number, line)]
        elif current_identity is not None:
            current_lines.append((line_number, line))
    finish_current()
    return result, violations


def run_without_verifier_command(run: str) -> str:
    return VERIFIER_COMMAND_LINE.sub("", run)


def is_shell_name(value: str) -> bool:
    """Return whether *value* is a POSIX-style variable name."""

    if not value or not (value[0].isalpha() or value[0] == "_"):
        return False
    return all(character.isalnum() or character == "_" for character in value[1:])


def is_shell_assignment(word: "ShellWord") -> bool:
    separator = word.value.find("=")
    return (
        not word.redirection_target
        and separator > 0
        and is_shell_name(word.value[:separator])
    )


@dataclass(frozen=True)
class ShellWord:
    """One bounded, source-only shell word.

    ``dynamic`` means that the word contains a shell expansion.  A static
    basename can still be safely classified (for example
    ``$RUNNER_TEMP/tool/actionlint``); an expansion in the executable basename
    is rejected rather than silently treated as non-Python.
    """

    value: str
    dynamic: bool = False
    redirection_target: bool = False


@dataclass(frozen=True)
class ShellCommand:
    command: ShellWord
    arguments: tuple[ShellWord, ...]


@dataclass(frozen=True)
class ShellAnalysis:
    commands: tuple[ShellCommand, ...]
    errors: tuple[str, ...]


def command_basename(command: str) -> str:
    return command.rsplit("/", 1)[-1]


def static_command_basename(word: ShellWord) -> str | None:
    """Return a statically known executable basename, if one is available."""

    basename = command_basename(word.value)
    if word.dynamic and "$" in basename:
        return None
    return basename


def is_python_or_pip_command(command: str) -> bool:
    return PYTHON_OR_PIP_BASENAME.fullmatch(command_basename(command)) is not None


def is_bare_pip_command(command: str) -> bool:
    return command_basename(command).startswith("pip") and (
        PYTHON_OR_PIP_BASENAME.fullmatch(command_basename(command)) is not None
    )


def read_heredoc_delimiter(
    line: str, start: int
) -> tuple[str | None, bool, int, str | None]:
    """Read a narrow, static here-document delimiter after ``<<``.

    Dynamic and malformed delimiters are not safe to skip: their bodies could
    contain a hidden command.  They are therefore reported as scanner errors.
    """

    cursor = start + 2
    if cursor < len(line) and line[cursor] == "<":
        # ``<<<`` is a here-string, not a here-document.
        return None, False, cursor + 1, None
    strip_tabs = cursor < len(line) and line[cursor] == "-"
    if strip_tabs:
        cursor += 1
    while cursor < len(line) and line[cursor] in " \t":
        cursor += 1
    if cursor >= len(line):
        return None, strip_tabs, cursor, "here-document has no delimiter"

    quote = line[cursor]
    if quote in {"'", '"'}:
        closing = line.find(quote, cursor + 1)
        if closing < 0:
            return None, strip_tabs, len(line), "unterminated here-document delimiter"
        delimiter = line[cursor + 1 : closing]
        cursor = closing + 1
    else:
        delimiter_start = cursor
        while cursor < len(line) and line[cursor] not in " \t;|&<>":
            cursor += 1
        delimiter = line[delimiter_start:cursor]

    if not is_shell_name(delimiter):
        return (
            None,
            strip_tabs,
            cursor,
            "here-document delimiter must be a static shell identifier",
        )
    return delimiter, strip_tabs, cursor, None


def heredoc_openings(line: str) -> tuple[list[tuple[str, bool]], list[str]]:
    """Find static here-document openings outside comments and shell quotes."""

    openings: list[tuple[str, bool]] = []
    errors: list[str] = []
    cursor = 0
    quote: str | None = None
    while cursor < len(line):
        character = line[cursor]
        if quote is not None:
            if character == "\\" and quote == '"':
                cursor += 2
            elif character == quote:
                quote = None
                cursor += 1
            else:
                cursor += 1
            continue
        if character in {"'", '"'}:
            quote = character
            cursor += 1
            continue
        if character == "\\":
            cursor += 2
            continue
        if character == "#" and (
            cursor == 0 or line[cursor - 1].isspace() or line[cursor - 1] in ";|&"
        ):
            break
        if character == "<" and cursor + 1 < len(line) and line[cursor + 1] == "<":
            delimiter, strip_tabs, cursor, error = read_heredoc_delimiter(line, cursor)
            if error is not None:
                errors.append(error)
            elif delimiter is not None:
                openings.append((delimiter, strip_tabs))
            continue
        cursor += 1
    return openings, errors


def shell_source_without_heredoc_bodies(run: str) -> tuple[str, tuple[str, ...]]:
    """Keep command lines while excluding only statically delimited bodies."""

    result: list[str] = []
    pending_delimiters: list[tuple[str, bool]] = []
    errors: list[str] = []
    for line in run.splitlines():
        if pending_delimiters:
            delimiter, strip_tabs = pending_delimiters[0]
            candidate = line.lstrip("\t") if strip_tabs else line
            if candidate.strip() == delimiter:
                pending_delimiters.pop(0)
            continue
        result.append(line)
        openings, line_errors = heredoc_openings(line)
        pending_delimiters.extend(openings)
        errors.extend(line_errors)
    if pending_delimiters:
        errors.append("unterminated here-document body")
    return "\n".join(result), tuple(errors)


class ShellScanner:
    """A bounded linear scanner for the contract's intentionally small shell subset."""

    def __init__(self, source: str, depth: int = 0) -> None:
        self.source = source
        self.depth = depth
        self.commands: list[ShellCommand] = []
        self.errors: list[str] = []

    def scan(self) -> ShellAnalysis:
        if len(self.source) > MAX_SHELL_SOURCE_LENGTH:
            return ShellAnalysis(
                (),
                (
                    f"shell source exceeds {MAX_SHELL_SOURCE_LENGTH} byte scanner limit",
                ),
            )
        if self.depth > MAX_SHELL_NESTING:
            return ShellAnalysis(
                (),
                (f"shell nesting exceeds {MAX_SHELL_NESTING} levels",),
            )

        words: list[ShellWord] = []
        redirection_target = False
        cursor = 0
        while cursor < len(self.source):
            character = self.source[cursor]
            if character in " \t\r":
                cursor += 1
                continue
            if character == "#" and (
                cursor == 0
                or self.source[cursor - 1].isspace()
                or self.source[cursor - 1] in ";|&"
            ):
                while cursor < len(self.source) and self.source[cursor] != "\n":
                    cursor += 1
                continue
            if character == "\n" or character in ";|&":
                if redirection_target:
                    self.errors.append("redirection has no target")
                    redirection_target = False
                self._finish_segment(words)
                words = []
                if character in "|&" and cursor + 1 < len(self.source):
                    if self.source[cursor + 1] == character:
                        cursor += 1
                cursor += 1
                continue
            redirection_start = self._redirection_start(cursor)
            if redirection_start is not None:
                cursor, redirection_target = self._consume_redirection(redirection_start)
                continue
            if character == "(":
                # A function declaration has the narrow ``name()`` form.  It
                # declares a shell function; it is not an invocation of a
                # similarly named executable.  Other parenthesized forms are
                # command lists or process substitutions, whose contents are
                # scanned normally after this structural delimiter.
                if (
                    cursor + 1 < len(self.source)
                    and self.source[cursor + 1] == ")"
                    and len(words) == 1
                    and not words[0].dynamic
                ):
                    words = []
                    cursor += 2
                    continue
                if redirection_target:
                    redirection_target = False
                self._finish_segment(words)
                words = []
                cursor += 1
                continue
            if character == ")":
                # Case-arm terminators and closing command lists both end a
                # segment.  The contained command has already been scanned.
                self._finish_segment(words)
                words = []
                cursor += 1
                continue

            word, cursor = self._read_word(cursor)
            if redirection_target:
                word = ShellWord(word.value, word.dynamic, redirection_target=True)
                redirection_target = False
            words.append(word)

        if redirection_target:
            self.errors.append("redirection has no target")
        self._finish_segment(words)
        return ShellAnalysis(tuple(self.commands), tuple(self.errors))

    def _redirection_start(self, cursor: int) -> int | None:
        character = self.source[cursor]
        if character in "<>":
            return cursor
        if not character.isdigit():
            return None
        end = cursor
        while end < len(self.source) and self.source[end].isdigit():
            end += 1
        return end if end < len(self.source) and self.source[end] in "<>" else None

    def _consume_redirection(self, cursor: int) -> tuple[int, bool]:
        operator = self.source[cursor]
        cursor += 1
        if cursor < len(self.source) and self.source[cursor] == operator:
            cursor += 1
        if operator == "<" and cursor < len(self.source) and self.source[cursor] == "-":
            cursor += 1
        if cursor < len(self.source) and self.source[cursor] == "&":
            cursor += 1
            while cursor < len(self.source) and (
                self.source[cursor].isdigit() or self.source[cursor] == "-"
            ):
                cursor += 1
            return cursor, False
        return cursor, True

    def _read_word(self, cursor: int) -> tuple[ShellWord, int]:
        characters: list[str] = []
        dynamic = False
        quote: str | None = None
        while cursor < len(self.source):
            character = self.source[cursor]
            if quote is None and character in " \t\r\n;|&<>()":
                break
            if quote is not None:
                if character == quote:
                    quote = None
                    cursor += 1
                    continue
                if character == "\\" and quote == '"':
                    if cursor + 1 >= len(self.source):
                        self.errors.append("dangling shell escape")
                        return ShellWord("".join(characters), dynamic), len(self.source)
                    characters.append(self.source[cursor + 1])
                    cursor += 2
                    continue
                if character == "$" and quote == '"':
                    cursor, expansion_dynamic = self._read_expansion(cursor, characters)
                    dynamic = dynamic or expansion_dynamic
                    continue
                if character == "`" and quote == '"':
                    self.errors.append("backtick command substitution is unsupported")
                characters.append(character)
                cursor += 1
                continue

            if character in {"'", '"'}:
                quote = character
                cursor += 1
                continue
            if character == "\\":
                if cursor + 1 >= len(self.source):
                    self.errors.append("dangling shell escape")
                    return ShellWord("".join(characters), dynamic), len(self.source)
                if self.source[cursor + 1] == "\n":
                    cursor += 2
                else:
                    characters.append(self.source[cursor + 1])
                    cursor += 2
                continue
            if character == "$":
                cursor, expansion_dynamic = self._read_expansion(cursor, characters)
                dynamic = dynamic or expansion_dynamic
                continue
            if character == "`":
                self.errors.append("backtick command substitution is unsupported")
            characters.append(character)
            cursor += 1

        if quote is not None:
            self.errors.append("unterminated shell quote")
        return ShellWord("".join(characters), dynamic), cursor

    def _read_expansion(self, cursor: int, characters: list[str]) -> tuple[int, bool]:
        if cursor + 1 >= len(self.source):
            characters.append("$")
            return cursor + 1, True
        marker = self.source[cursor + 1]
        if marker == "(":
            content, end = self._command_substitution(cursor)
            if content is None:
                self.errors.append("unterminated command substitution")
                return len(self.source), True
            if content.startswith("("):
                # ``$((...))`` is a normal non-executing arithmetic expansion.
                # Its only executable nested form is command substitution;
                # reject that form rather than overlooking a hidden Python
                # invocation.  Backticks are rejected for the same reason.
                if "$(" in content[1:]:
                    self.errors.append(
                        "arithmetic expansion with command substitution is unsupported"
                    )
                if "`" in content:
                    self.errors.append(
                        "arithmetic expansion with backtick substitution is unsupported"
                    )
            else:
                nested = ShellScanner(content, self.depth + 1).scan()
                self.commands.extend(nested.commands)
                self.errors.extend(nested.errors)
            characters.append("$()")
            return end, True
        if marker == "{":
            end = self._braced_expansion_end(cursor)
            if end is None:
                self.errors.append("unterminated braced shell expansion")
                return len(self.source), True
            characters.append("${}")
            return end, True
        if marker.isalpha() or marker == "_":
            end = cursor + 2
            while end < len(self.source) and (
                self.source[end].isalnum() or self.source[end] == "_"
            ):
                end += 1
            characters.append(self.source[cursor:end])
            return end, True
        characters.append(self.source[cursor : cursor + 2])
        return cursor + 2, True

    def _command_substitution(self, start: int) -> tuple[str | None, int]:
        cursor = start + 2
        content_start = cursor
        depth = 1
        quote: str | None = None
        while cursor < len(self.source):
            character = self.source[cursor]
            if quote is not None:
                if character == "\\" and quote == '"':
                    cursor += 2
                elif character == quote:
                    quote = None
                    cursor += 1
                else:
                    cursor += 1
                continue
            if character in {"'", '"'}:
                quote = character
                cursor += 1
                continue
            if character == "\\":
                cursor += 2
                continue
            if character == "(":
                depth += 1
            elif character == ")":
                depth -= 1
                if depth == 0:
                    return self.source[content_start:cursor], cursor + 1
            cursor += 1
        return None, len(self.source)

    def _braced_expansion_end(self, start: int) -> int | None:
        cursor = start + 2
        depth = 1
        while cursor < len(self.source):
            character = self.source[cursor]
            if character == "\\":
                cursor += 2
                continue
            if character == "{":
                depth += 1
            elif character == "}":
                depth -= 1
                if depth == 0:
                    return cursor + 1
            cursor += 1
        return None

    def _finish_segment(self, words: list[ShellWord]) -> None:
        command, error = self._command_from_words(words)
        if error is not None:
            self.errors.append(error)
            return
        if command is None:
            return
        self.commands.append(command)
        self._scan_shell_script_argument(command)

    def _command_from_words(
        self, words: list[ShellWord]
    ) -> tuple[ShellCommand | None, str | None]:
        usable = [word for word in words if not word.redirection_target]
        cursor = 0
        while cursor < len(usable) and is_shell_assignment(usable[cursor]):
            cursor += 1
        while cursor < len(usable):
            word = usable[cursor]
            value = word.value if not word.dynamic else None
            if value in {"case", "for", "function"}:
                return None, None
            if value in SHELL_CONTROL_WORDS:
                cursor += 1
                continue
            if value == "command":
                cursor += 1
                if cursor < len(usable) and usable[cursor].value in SHELL_COMMAND_OPTION_ONLY:
                    return None, None
                cursor, error = self._skip_wrapper_options(usable, cursor)
                if error is not None:
                    return None, error
                continue
            if value == "env":
                cursor, error = self._skip_env_options(usable, cursor + 1)
                if error is not None:
                    return None, error
                continue
            if value == "sudo":
                cursor, error = self._skip_wrapper_options(usable, cursor + 1)
                if error is not None:
                    return None, error
                continue
            basename = static_command_basename(word)
            if basename is None:
                return None, "dynamic shell command head is unsupported"
            return ShellCommand(word, tuple(usable[cursor + 1 :])), None
        return None, None

    def _skip_wrapper_options(
        self, words: list[ShellWord], cursor: int
    ) -> tuple[int, str | None]:
        while cursor < len(words):
            word = words[cursor]
            if word.dynamic:
                return cursor, "dynamic shell wrapper option is unsupported"
            if word.value == "--":
                return cursor + 1, None
            if not word.value.startswith("-") or word.value == "-":
                return cursor, None
            cursor += 1
            if word.value in SHELL_OPTIONS_WITH_VALUE:
                if cursor >= len(words):
                    return cursor, "shell wrapper option has no value"
                cursor += 1
        return cursor, None

    def _skip_env_options(
        self, words: list[ShellWord], cursor: int
    ) -> tuple[int, str | None]:
        while cursor < len(words):
            word = words[cursor]
            if word.value == "--" and not word.dynamic:
                return cursor + 1, None
            if is_shell_assignment(word):
                cursor += 1
                continue
            if word.dynamic:
                return cursor, "dynamic env command head is unsupported"
            if not word.value.startswith("-") or word.value == "-":
                return cursor, None
            cursor += 1
            if word.value in {"-C", "-u", "--chdir", "--unset"}:
                if cursor >= len(words):
                    return cursor, "env option has no value"
                cursor += 1
        return cursor, None

    def _scan_shell_script_argument(self, command: ShellCommand) -> None:
        basename = static_command_basename(command.command)
        if basename not in {"bash", "dash", "ksh", "sh", "zsh"}:
            return
        for index, argument in enumerate(command.arguments):
            if argument.value != "-c" or argument.dynamic:
                continue
            if index + 1 >= len(command.arguments):
                self.errors.append("shell -c has no script argument")
                return
            script = command.arguments[index + 1]
            if script.dynamic:
                self.errors.append("dynamic shell -c script is unsupported")
                return
            nested = ShellScanner(script.value, self.depth + 1).scan()
            self.commands.extend(nested.commands)
            self.errors.extend(nested.errors)
            return


def analyze_shell_source(run: str) -> ShellAnalysis:
    source, heredoc_errors = shell_source_without_heredoc_bodies(run)
    scanned = ShellScanner(source).scan()
    return ShellAnalysis(scanned.commands, heredoc_errors + scanned.errors)


def direct_python_or_pip_command(run: str) -> str | None:
    for shell_command in analyze_shell_source(run).commands:
        command = static_command_basename(shell_command.command)
        if command is not None and is_python_or_pip_command(command):
            return command
    return None


def bare_pip_command(run: str) -> str | None:
    for shell_command in analyze_shell_source(run).commands:
        command = static_command_basename(shell_command.command)
        if command is not None and is_bare_pip_command(command):
            return command
    return None


def python_make_target(run: str) -> str | None:
    for shell_command in analyze_shell_source(run).commands:
        command = static_command_basename(shell_command.command)
        if command != "make":
            continue
        for argument in shell_command.arguments:
            if not argument.dynamic and argument.value in KNOWN_PYTHON_MAKE_TARGETS:
                return argument.value
    return None


def shell_syntax_error(run: str) -> str | None:
    analysis = analyze_shell_source(run)
    return analysis.errors[0] if analysis.errors else None


def actual_python_use(step: Step) -> str | None:
    run = step.run()
    without_verifier = run_without_verifier_command(run)
    if direct_python_or_pip_command(without_verifier) is not None:
        return "direct python/pip command"
    target = python_make_target(without_verifier)
    if target is not None:
        return f"Make target {target}"
    return None


def first_python_use(steps: Iterable[Step]) -> tuple[Step, str] | None:
    for step in steps:
        use = actual_python_use(step)
        if use is not None:
            return step, use
    return None


def first_shell_syntax_error(steps: Iterable[Step]) -> tuple[Step, str] | None:
    """Return a fail-closed shell-recognition error, if a step has one."""

    for step in steps:
        error = shell_syntax_error(run_without_verifier_command(step.run()))
        if error is not None:
            return step, error
    return None


def has_python_matrix_selector(job: Job) -> bool:
    """Identify Python-bearing matrix axes and matrix-derived selectors."""

    if any(PYTHON_MATRIX_REFERENCE.search(line) for _, line in job.lines):
        return True
    if any("matrix" in line.lower() for line in selector_lines(job)):
        return True

    for position, (_, line) in enumerate(job.lines):
        matrix_indent = indentation(line)
        if line[matrix_indent:].strip() != "matrix:":
            continue
        for _, child_line in job.lines[position + 1 :]:
            child_indent = indentation(child_line)
            if child_line.strip() and child_indent <= matrix_indent:
                break
            if PYTHON_MATRIX_KEY.match(child_line):
                return True
    return False


def python_job_reason(job: Job) -> str | None:
    """Classify every workflow form that can select or invoke Python.

    Reusable workflow calls cannot be proved non-Python from the caller source,
    and a Python matrix can choose a runtime without an inline command.  Both
    are deliberately inventoried rather than silently bypassing this check.
    """

    direct = first_python_use(job.steps())
    if direct is not None:
        return direct[1]
    syntax_error = first_shell_syntax_error(job.steps())
    if syntax_error is not None:
        return f"unsupported/malformed shell syntax: {syntax_error[1]}"
    if job.scalar("uses") is not None:
        return "job-level reusable workflow invocation"
    if has_python_matrix_selector(job):
        return "Python-related matrix selector"
    return None


def exact_command(run: str, expected: str) -> bool:
    meaningful = [line.strip() for line in run.splitlines() if line.strip() and not line.lstrip().startswith("#")]
    return meaningful == [expected]


def pinned_setup_step(steps: Sequence[Step]) -> tuple[Step | None, list[str]]:
    setup_like = [
        step
        for step in steps
        if (uses := step.scalar("uses")) is not None
        and uses.startswith("actions/setup-python@")
    ]
    matching = [
        step for step in setup_like if step.raw_scalar("uses") == SETUP_PYTHON_REFERENCE
    ]
    errors: list[str] = []
    if len(matching) != 1:
        if setup_like:
            errors.append(
                "actions/setup-python must use exactly "
                f"{SETUP_PYTHON_REFERENCE}; found {len(matching)} exact reference(s)"
            )
        else:
            errors.append(
                "must contain exactly one "
                f"{SETUP_PYTHON_ACTION} setup step; found {len(matching)}"
            )
        return None, errors
    setup = matching[0]
    if setup.scalar("id") != "setup-python":
        errors.append("pinned actions/setup-python step must have id: setup-python")
    return setup, errors


def selector_lines(job: Job) -> list[str]:
    lines: list[str] = []
    for _, line in job.lines:
        if re.match(r"^\s*python-version\s*:", line):
            lines.append(line.strip())
    return lines


def verifier_step(steps: Sequence[Step], name: str = VERIFIER_NAME) -> Step | None:
    named = [step for step in steps if step.scalar("name") == name]
    return named[0] if len(named) == 1 else None


def validate_order(
    identity: JobIdentity,
    steps: Sequence[Step],
    setup: Step | None,
    verifier: Step | None,
    verifier_name: str = VERIFIER_NAME,
) -> list[str]:
    errors: list[str] = []
    first_use = first_python_use(steps)
    if setup is None:
        if first_use is not None:
            errors.append(
                f"{identity.display()} uses Python via {first_use[1]} before pinned setup-python"
            )
        return errors
    if verifier is None:
        errors.append(f"{identity.display()} lacks exactly one {verifier_name!r} step")
    elif verifier.index <= setup.index:
        errors.append(f"{identity.display()} verifier must run after setup-python")
    if first_use is not None:
        use_step, use_kind = first_use
        if use_step.index <= setup.index:
            errors.append(
                f"{identity.display()} first Python use ({use_kind}) must be after setup-python"
            )
        if verifier is None or verifier.index >= use_step.index:
            errors.append(
                f"{identity.display()} verifier must run before first Python use ({use_kind})"
            )
    return errors


def validate_no_bare_pip(identity: JobIdentity, steps: Iterable[Step]) -> list[str]:
    """Reject PATH-dependent pip aliases even when setup has already run."""

    errors: list[str] = []
    for step in steps:
        command = bare_pip_command(run_without_verifier_command(step.run()))
        if command is not None:
            errors.append(
                f"{identity.display()} must not invoke bare pip command {command!r}; "
                "use python -m pip through the verified interpreter"
            )
    return errors


def validate_shell_syntax(identity: JobIdentity, steps: Iterable[Step]) -> list[str]:
    """Reject unsupported shell forms instead of silently missing Python use."""

    errors: list[str] = []
    for step in steps:
        error = shell_syntax_error(run_without_verifier_command(step.run()))
        if error is not None:
            errors.append(
                f"{identity.display()} step at workflow line {step.start_line} "
                f"contains unsupported/malformed shell syntax: {error}"
            )
    return errors


def validate_normal_job(job: Job) -> list[str]:
    steps = job.steps()
    setup, errors = pinned_setup_step(steps)
    if setup is not None:
        with_values = setup.nested_mapping("with")
        if with_values.get("python-version-file") != ".python-version":
            errors.append("setup-python must use python-version-file: '.python-version'")
        if with_values.get("check-latest") != "false":
            errors.append("setup-python must use check-latest: false")
        if "python-version" in with_values:
            errors.append("normal Python jobs must not use python-version selectors")
        if any("3.13" in line or "matrix" in line for line in selector_lines(job)):
            errors.append("normal Python jobs must not use a literal or matrix Python selector")
        if has_python_matrix_selector(job):
            errors.append(
                "normal Python jobs must not declare or reference Python-related matrix selectors"
            )

    verifier = verifier_step(steps)
    if verifier is not None:
        if verifier.nested_mapping("env").get("EXPECTED_PYTHON") != SETUP_PYTHON_OUTPUT:
            errors.append(
                "verifier EXPECTED_PYTHON must be exactly "
                "${{ steps.setup-python.outputs.python-path }}"
            )
        if not exact_command(verifier.run(), NORMAL_VERIFIER_COMMAND):
            errors.append(
                "verifier must invoke the interpreter checker with .python-version and "
                '"$EXPECTED_PYTHON"'
            )
    errors.extend(validate_order(job.identity, steps, setup, verifier))
    prefixed = [f"{job.identity.display()}: {error}" for error in errors]
    return (
        prefixed
        + validate_no_bare_pip(job.identity, steps)
        + validate_shell_syntax(job.identity, steps)
    )


def validate_candidate_job(job: Job) -> list[str]:
    """Validate the one explicit candidate-patch exception without widening it."""

    steps = job.steps()
    setup, errors = pinned_setup_step(steps)
    if setup is not None:
        with_values = setup.nested_mapping("with")
        if with_values.get("python-version") != CANDIDATE_VERSION_OUTPUT:
            errors.append(
                "candidate setup-python must use exactly "
                "python-version: ${{ needs.resolve-python-patch.outputs.version }}"
            )
        if "python-version-file" in with_values:
            errors.append("candidate setup-python must not use python-version-file")
        if with_values.get("check-latest") != "false":
            errors.append("candidate setup-python must use check-latest: false")
        if any("3.13" in line or "matrix" in line for line in selector_lines(job)):
            errors.append("candidate job must not use literal or matrix Python selectors")
        if has_python_matrix_selector(job):
            errors.append(
                "candidate job must not declare or reference Python-related matrix selectors"
            )

    verifier = verifier_step(steps, CANDIDATE_VERIFIER_NAME)
    if verifier is not None:
        env = verifier.nested_mapping("env")
        if env.get("EXPECTED_VERSION") != CANDIDATE_VERSION_OUTPUT:
            errors.append(
                "candidate verifier EXPECTED_VERSION must be exactly "
                "${{ needs.resolve-python-patch.outputs.version }}"
            )
        if env.get("EXPECTED_PYTHON") != SETUP_PYTHON_OUTPUT:
            errors.append(
                "candidate verifier EXPECTED_PYTHON must be exactly "
                "${{ steps.setup-python.outputs.python-path }}"
            )
        if not exact_command(verifier.run(), CANDIDATE_VERIFIER_COMMAND):
            errors.append(
                "candidate verifier must invoke the checker with "
                '"$EXPECTED_VERSION" and "$EXPECTED_PYTHON"'
            )
    errors.extend(
        validate_order(
            job.identity,
            steps,
            setup,
            verifier,
            CANDIDATE_VERIFIER_NAME,
        )
    )
    prefixed = [f"{job.identity.display()}: {error}" for error in errors]
    return (
        prefixed
        + validate_no_bare_pip(job.identity, steps)
        + validate_shell_syntax(job.identity, steps)
    )


def evaluate_workflow_contract(
    root: Path,
    version_file: Path,
    previous_version: str | None = None,
    allow_downgrade: bool = False,
    expected_normal_jobs: Iterable[JobIdentity] = EXPECTED_NORMAL_PYTHON_JOBS,
    expected_candidate_job: JobIdentity | None = CANDIDATE_VALIDATION_JOB,
) -> tuple[str, list[str], set[JobIdentity]]:
    """Evaluate source-only workflow policy and return version, violations, inventory."""

    canonical_version = read_canonical_version(version_file)
    violations: list[str] = []
    if previous_version is not None:
        previous = parse_exact_version(previous_version, "--previous-version")
        if version_tuple(canonical_version) < version_tuple(previous) and not allow_downgrade:
            violations.append(
                f"canonical Python version {canonical_version} is a downgrade from {previous}; "
                "pass --allow-downgrade only with explicit authorization"
            )

    paths, file_violations = workflow_files(root)
    violations.extend(file_violations)
    jobs: dict[JobIdentity, Job] = {}
    for path in paths:
        parsed, parse_violations = parse_jobs(path)
        jobs.update(parsed)
        violations.extend(parse_violations)

    expected = frozenset(expected_normal_jobs)
    for identity in sorted(expected):
        if identity not in jobs:
            violations.append(f"expected normal Python job is absent: {identity.display()}")
    if expected_candidate_job is not None and expected_candidate_job not in jobs:
        violations.append(
            f"expected candidate-validation job is absent: {expected_candidate_job.display()}"
        )

    detected: set[JobIdentity] = set()
    for identity, job in jobs.items():
        if python_job_reason(job) is not None:
            detected.add(identity)

    for identity in sorted(expected):
        job = jobs.get(identity)
        if job is None:
            continue
        if identity not in detected:
            violations.append(
                f"expected normal Python job has no detected Python use, known Make use, "
                f"reusable invocation, or Python-related matrix selector: "
                f"{identity.display()}"
            )
        violations.extend(validate_normal_job(job))

    if expected_candidate_job is not None:
        candidate = jobs.get(expected_candidate_job)
        if candidate is not None:
            if expected_candidate_job not in detected:
                violations.append(
                    "candidate-validation job has no detected Python use, known Make use, "
                    "reusable invocation, or Python-related matrix selector: "
                    f"{expected_candidate_job.display()}"
                )
            violations.extend(validate_candidate_job(candidate))

    for identity in sorted(detected):
        if identity in expected or identity == expected_candidate_job:
            continue
        violations.append(
            f"unlisted Python-related workflow job: {identity.display()} "
            f"({python_job_reason(jobs[identity])})"
        )
        violations.extend(validate_normal_job(jobs[identity]))

    return canonical_version, violations, detected


def parser() -> argparse.ArgumentParser:
    argument_parser = argparse.ArgumentParser(
        description="Validate Parent GitHub Actions Python setup and interpreter checks."
    )
    argument_parser.add_argument(
        "--version-file",
        metavar="PATH",
        default=CANONICAL_VERSION_FILE,
        help="must be the literal canonical path .python-version",
    )
    argument_parser.add_argument(
        "--previous-version",
        metavar="3.13.N",
        help="previous canonical version; reject a downgrade unless explicitly allowed",
    )
    argument_parser.add_argument(
        "--allow-downgrade",
        action="store_true",
        help="acknowledge an intentional canonical-version downgrade",
    )
    argument_parser.add_argument("--json", action="store_true", help="emit JSON")
    return argument_parser


def report(
    status: str,
    canonical_version: str | None,
    violations: list[str],
    detected: set[JobIdentity],
    as_json: bool,
) -> None:
    if as_json:
        print(
            json.dumps(
                {
                    "canonical_version": canonical_version,
                    "detected_python_jobs": [item.display() for item in sorted(detected)],
                    "status": status,
                    "violations": violations,
                },
                sort_keys=True,
            )
        )
        return
    if status == "valid":
        print(
            "python-version-contract: valid "
            f"(Python {canonical_version}; {len(detected)} Python-executing workflow jobs)"
        )
        return
    for violation in violations:
        print(f"python-version-contract: {violation}", file=sys.stderr)


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        # Validate the only remaining path-shaped argument before resolving or
        # reading any filesystem path.  The public command has no caller-
        # controlled repository boundary.
        if args.version_file != CANONICAL_VERSION_FILE:
            raise ContractInputError(
                "--version-file must be exactly the literal '.python-version'"
            )
        root = repository_root()
        if not root.is_dir():
            raise ContractInputError(f"repository root is not a directory: {root}")
        version_file = canonical_version_file(root)
        canonical_version, violations, detected = evaluate_workflow_contract(
            root,
            version_file,
            previous_version=args.previous_version,
            allow_downgrade=args.allow_downgrade,
        )
    except ContractInputError as exc:
        report("error", None, [str(exc)], set(), args.json)
        return 2

    if violations:
        report("violations", canonical_version, violations, detected, args.json)
        return 1
    report("valid", canonical_version, [], detected, args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
