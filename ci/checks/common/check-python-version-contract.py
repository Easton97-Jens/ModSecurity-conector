#!/usr/bin/env python3
"""Statically enforce the Parent's Python workflow-selection contract.

This parses workflow YAML into ``yaml.BaseLoader`` semantic nodes to inspect
the same job and step structure GitHub Actions receives; it never executes
workflow content.  Unsupported or ambiguous mappings, shell indirection, and
non-POSIX shell selectors fail closed.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import json
from pathlib import Path
import re
import stat
import sys
import textwrap
from typing import Iterable, Sequence

import yaml
from yaml.nodes import MappingNode, Node, ScalarNode, SequenceNode
from yaml.tokens import (
    AliasToken,
    AnchorToken,
    FlowMappingStartToken,
    FlowSequenceStartToken,
    TagToken,
)


CANONICAL_VERSION_FILE = ".python-version"
SETUP_PYTHON_ACTION = "actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97"
SETUP_PYTHON_RELEASE_COMMENT = "# v7.0.0"
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
UPDATE_PYTHON_VERSION_WORKFLOW = "update-python-version.yml"
SECURITY_TOOL_LOCK = Path("ci/tooling/security-tools.lock.yml")
_ACTIVE_SETUP_PYTHON_REFERENCE: str | None = None


@dataclass(frozen=True, order=True)
class JobIdentity:
    """A stable workflow filename/job-ID pair used by the inventory contract."""

    workflow: str
    job: str

    def display(self) -> str:
        return f"{self.workflow}:{self.job}"


def semantic_mapping_items(node: MappingNode, *, context: str) -> dict[str, Node]:
    """Decode a YAML mapping with duplicate and merge keys rejected."""

    result: dict[str, Node] = {}
    for key, value in node.value:
        if not isinstance(key, ScalarNode):
            raise ContractInputError(f"{context} has a non-scalar mapping key")
        if key.value == "<<":
            raise ContractInputError(f"{context} uses an unsupported YAML merge key")
        if key.value in result:
            raise ContractInputError(f"{context} has a duplicate mapping key {key.value!r}")
        result[key.value] = value
    return result


def scalar_environment_values(
    fields: dict[str, Node], *, context: str
) -> dict[str, str]:
    """Return scalar GitHub Actions environment values at one scope.

    A non-scalar environment value cannot be safely reasoned about for
    interpreter selection, so it is rejected before shell validation.
    """

    environment = fields.get("env")
    if environment is None:
        return {}
    if not isinstance(environment, MappingNode):
        raise ContractInputError(f"{context}.env is not a mapping")
    values: dict[str, str] = {}
    for key, value in semantic_mapping_items(
        environment, context=f"{context}.env"
    ).items():
        if not isinstance(value, ScalarNode):
            raise ContractInputError(f"{context}.env.{key} is not a scalar")
        values[key] = value.value
    return values


def setup_python_reference_from_lock(root: Path, *, require_lock: bool) -> str:
    """Bind setup-python provenance to the updater-owned action lock.

    The generic action updater intentionally changes the immutable setup-python
    SHA and release comment.  Reading the same checked-in lock avoids a stale
    hardcoded checker pin while retaining strict tag/commit shape validation.
    Isolated unit fixtures may opt out only when they intentionally omit the
    production lock; the public CLI always requires it.
    """

    lock_path = root / SECURITY_TOOL_LOCK
    if not lock_path.is_file():
        if require_lock:
            raise ContractInputError(f"security tool lock is missing: {lock_path}")
        return SETUP_PYTHON_REFERENCE
    try:
        document = yaml.compose(lock_path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
    except (OSError, RecursionError, yaml.YAMLError) as error:
        raise ContractInputError(f"cannot parse security tool lock {lock_path}: {error}") from error
    if not isinstance(document, MappingNode):
        raise ContractInputError(f"security tool lock is not a mapping: {lock_path}")
    lock = semantic_mapping_items(document, context="security tool lock")
    actions = lock.get("pinned_actions")
    if not isinstance(actions, MappingNode):
        raise ContractInputError("security tool lock has no pinned_actions mapping")
    record = semantic_mapping_items(actions, context="security tool lock.pinned_actions").get(
        "actions/setup-python"
    )
    if not isinstance(record, MappingNode):
        raise ContractInputError("security tool lock has no actions/setup-python record")
    values = semantic_mapping_items(record, context="security tool lock.actions/setup-python")
    version = values.get("version")
    commit = values.get("commit_sha")
    if not isinstance(version, ScalarNode) or not re.fullmatch(r"v[1-9][0-9]*(?:\.[0-9]+){0,2}", version.value):
        raise ContractInputError("actions/setup-python lock version is invalid")
    if not isinstance(commit, ScalarNode) or not re.fullmatch(r"[a-f0-9]{40}", commit.value):
        raise ContractInputError("actions/setup-python lock commit_sha is invalid")
    return f"actions/setup-python@{commit.value} # {version.value}"


def active_setup_python_reference() -> str:
    return _ACTIVE_SETUP_PYTHON_REFERENCE or SETUP_PYTHON_REFERENCE


def active_setup_python_action() -> str:
    return active_setup_python_reference().split(" # ", 1)[0]


# These are the final Parent-native Python jobs, including the read-only and
# publisher stages for the Python and CI-tool updaters.  The one candidate job
# below is deliberately separate because it must validate a prospective patch
# before the canonical .python-version file is changed.
EXPECTED_NORMAL_PYTHON_JOBS = frozenset(
    {
        JobIdentity("all-connectors-no-crs.yml", "aggregate"),
        JobIdentity("all-connectors-no-crs.yml", "no-crs"),
        JobIdentity("check-actions-versions.yml", "check-ci-tool-updates"),
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
        JobIdentity("update-actions-versions.yml", "create-ci-tool-update-pr"),
        JobIdentity("update-actions-versions.yml", "resolve-ci-tool-updates"),
        JobIdentity("update-actions-versions.yml", "validate-ci-tool-updates"),
        JobIdentity("update-go-version.yml", "create-go-update-pr"),
        JobIdentity("update-go-version.yml", "resolve-go-patch"),
        JobIdentity("update-go-version.yml", "validate-go-patch"),
        JobIdentity(UPDATE_PYTHON_VERSION_WORKFLOW, "create-python-update-pr"),
        JobIdentity(UPDATE_PYTHON_VERSION_WORKFLOW, "resolve-python-patch"),
        JobIdentity("update-submodules.yml", "validate-submodule-update"),
        JobIdentity("verified-report-governance.yml", "report-governance"),
    }
)

# This is intentionally an exact pair, not a filename/job-name pattern.  It
# does not permit ambient Python: the candidate version and setup-python path
# are both checked by the stricter verifier shape below.
CANDIDATE_VALIDATION_JOB = JobIdentity(
    UPDATE_PYTHON_VERSION_WORKFLOW, "validate-python-patch"
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

# Executable basenames are recognized structurally below rather than with a
# regular expression.  The scanner does not search arbitrary substrings:
# comments and here-document bodies are excluded.  A standalone literal
# interpreter *token*, however, is conservatively contract-relevant even in
# an unknown command's argument list: arbitrary launchers can execute such a
# token, and maintaining a launcher allowlist would be bypassable.
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
NON_POSIX_WORKFLOW_SHELLS = frozenset({"pwsh", "powershell", "cmd"})
SHELL_INDIRECTION_BUILTINS = frozenset({"alias", "eval"})
# These commands cannot execute an argument as a program.  Their data tokens
# are deliberately excluded from the generic launcher scan so that
# ``echo python3`` remains text rather than a false execution finding.  Every
# other command is conservatively treated as a possible launcher; this is a
# closed list of data-only semantics, not an open-ended launcher allowlist.
NON_EXECUTING_ARGUMENT_COMMANDS = frozenset(
    {
        ":",
        "basename",
        "cat",
        "cd",
        "chmod",
        "chown",
        "cmp",
        "cp",
        "cut",
        "date",
        "dirname",
        "echo",
        "exit",
        "export",
        "false",
        "git",
        "grep",
        "head",
        "ln",
        "local",
        "ls",
        "make",
        "mkdir",
        "mv",
        "printf",
        "pwd",
        "read",
        "rm",
        "return",
        "sed",
        "set",
        "sha256sum",
        "sort",
        "test",
        "touch",
        "tr",
        "true",
        "uname",
        "uniq",
        "unset",
        "wc",
        "[",
        "[[",
    }
)
# Dynamic arguments are allowed only for commands whose argument grammar is
# audited not to choose an executable.  Any unknown command remains fail
# closed, which catches arbitrary launchers without keeping an allowlist of
# launchers.  Shell-local functions are added separately only when their
# declaration is present in the same static run block.
DYNAMIC_ARGUMENT_SAFE_COMMANDS = NON_EXECUTING_ARGUMENT_COMMANDS | frozenset(
    {
        "actionlint",
        "gh",
        "gitleaks",
        "mktemp",
        "nginx_protocol_profile_configure_flags",
        "nginx_protocol_profile_valid",
        "tar",
        "tee",
        "zizmor",
    }
)
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
UNSAFE_INTERPRETER_ENV_KEYS = frozenset(
    {"PATH", "BASH_ENV", "ENV", "PYTHONHOME", "PYTHONEXECUTABLE", "VIRTUAL_ENV"}
)
UNSAFE_INTERPRETER_ENV_ASSIGNMENT = re.compile(
    r"(?<![A-Za-z0-9_])"
    r"(?:PATH|BASH_ENV|ENV|PYTHONHOME|PYTHONEXECUTABLE|VIRTUAL_ENV)"
    r"(?:\+?=|<<)"
)
GITHUB_ENV_REDIRECT = re.compile(
    r'>>?\s*(?:"\$GITHUB_ENV"|\$\{GITHUB_ENV\}|\$GITHUB_ENV)'
    r"\s*(?:#.*)?$"
)
STATIC_GITHUB_ENV_ECHO = re.compile(
    r'^\s*echo\s+"(?P<key>[A-Za-z_][A-Za-z0-9_]*)=[^"\n]*"\s*$'
)
STATIC_GITHUB_ENV_PRINTF = re.compile(
    r"^\s*printf\s+'(?P<key>[A-Za-z_][A-Za-z0-9_]*)=%s\\n'\s+\"[^\"\n]*\"\s*$"
)
# A Python-contract job may persist only this deliberately small set of
# non-interpreter state.  The source grammar below requires the assignment key
# itself to be literal, so a shell expression cannot splice together PATH (or
# another interpreter-selection key) for a later step.
ALLOWED_GITHUB_ENV_KEYS = frozenset(
    {
        "BUILD_ROOT",
        "CANDIDATE_PATH",
        "CONNECTOR_COMPONENT_CACHE",
        "EVIDENCE_ROOT",
        "LOG_ROOT",
        "MODSECURITY_SOURCE_DIR",
        "MODSECURITY_V3_SOURCE_DIR",
        "NGINX_HARNESS_PARENT",
        "NGINX_PHASE4_MODE",
        "NO_CRS_EVIDENCE_ROOT",
        "NO_CRS_RUN_ID",
        "PYTHONPATH",
        "PYTHONPYCACHEPREFIX",
        "RUNTIME_REPORT_OUTPUT_ROOT",
        "SOURCE_ROOT",
        "TMP_ROOT",
        "VERIFIED_RUN_ROOT",
        "XDG_STATE_HOME",
    }
)
SIMPLE_REDIRECT_PATH_VALUE = re.compile(
    r"(?:"
    r"(?:\$RUNNER_TEMP|\$GITHUB_WORKSPACE)(?:/[A-Za-z0-9._/-]+)*"
    r"|[A-Za-z0-9][A-Za-z0-9._/-]*"
    r")"
)
SIMPLE_REDIRECT_PATH_ASSIGNMENT = re.compile(
    r"(?m)^\s*(?:local\s+)?(?P<name>[A-Za-z_][A-Za-z0-9_]*)"
    r"\s*=\s*(?P<value>[^#\n]+?)\s*(?:#.*)?$"
)
DYNAMIC_OUTPUT_REDIRECT_VARIABLE = re.compile(
    r"^\$(?P<name>[A-Za-z_][A-Za-z0-9_]*)(?:/[A-Za-z0-9._/-]+)*$"
)


class ContractInputError(ValueError):
    """Raised for invalid command input or an unusable canonical version file."""


@dataclass
class Step:
    index: int
    start_line: int
    indent: int
    lines: list[tuple[int, str]]
    node: MappingNode | None = None
    source: str = ""
    default_shell: str | None = None

    def semantic_fields(self) -> dict[str, Node]:
        if self.node is None:
            return {}
        return semantic_mapping_items(self.node, context="workflow step")

    def semantic_entry(self, key: str) -> tuple[ScalarNode, Node] | None:
        if self.node is None:
            return None
        for key_node, value in self.node.value:
            if isinstance(key_node, ScalarNode) and key_node.value == key:
                return key_node, value
        return None

    def scalar(self, key: str) -> str | None:
        if self.node is not None:
            value = self.semantic_fields().get(key)
            return value.value if isinstance(value, ScalarNode) else None
        for _, _, entry in direct_step_entries(self.lines, self.indent):
            if entry[0] == key:
                return clean_scalar(entry[1])
        return None

    def raw_scalar(self, key: str) -> str | None:
        """Return the unnormalized scalar text for a direct step mapping key.

        The setup-python provenance comment is part of this contract, so it
        must be checked before `clean_scalar()` removes a YAML comment.
        """

        if self.node is not None:
            entry = self.semantic_entry(key)
            if entry is None:
                return None
            key_node, value = entry
            line = self.source.splitlines()[key_node.start_mark.line]
            separator = line.find(":", key_node.end_mark.column)
            return line[separator + 1 :].strip() if separator >= 0 else None
        for _, _, entry in direct_step_entries(self.lines, self.indent):
            if entry[0] == key:
                return entry[1].strip()
        return None

    def nested_mapping(self, key: str) -> dict[str, str]:
        if self.node is not None:
            value = self.semantic_fields().get(key)
            if not isinstance(value, MappingNode):
                return {}
            return {
                child_key: child_value.value
                for child_key, child_value in semantic_mapping_items(
                    value, context=f"workflow step.{key}"
                ).items()
                if isinstance(child_value, ScalarNode)
            }
        for position, parent_indent, entry in direct_step_entries(
            self.lines, self.indent
        ):
            if entry[0] == key:
                return direct_child_mapping(self.lines[position + 1 :], parent_indent)
        return {}

    def run(self) -> str:
        if self.node is not None:
            value = self.semantic_fields().get("run")
            return value.value if isinstance(value, ScalarNode) else ""
        for position, parent_indent, entry in direct_step_entries(
            self.lines, self.indent
        ):
            if entry[0] == "run":
                return step_run_value(
                    entry[1], self.lines[position + 1 :], parent_indent
                )
        return ""


@dataclass
class Job:
    identity: JobIdentity
    indent: int
    lines: list[tuple[int, str]]
    node: MappingNode | None = None
    source: str = ""
    default_shell: str | None = None
    inherited_environment: dict[str, str] = field(default_factory=dict)

    def semantic_fields(self) -> dict[str, Node]:
        if self.node is None:
            return {}
        return semantic_mapping_items(self.node, context=f"workflow job {self.identity.display()}")

    def scalar(self, key: str) -> str | None:
        """Return a direct job-level scalar without descending into steps."""

        if self.node is not None:
            value = self.semantic_fields().get(key)
            return value.value if isinstance(value, ScalarNode) else None

        for _, line in self.lines[1:]:
            indent = indentation(line)
            if indent != self.indent + 2:
                continue
            entry = mapping_entry(line[indent:])
            if entry is not None and entry[0] == key:
                return clean_scalar(entry[1])
        return None

    def steps(self) -> list[Step]:
        if self.node is not None:
            steps = self.semantic_fields().get("steps")
            if not isinstance(steps, SequenceNode):
                return []
            result: list[Step] = []
            source_lines = self.source.splitlines()
            for index, step in enumerate(steps.value):
                if not isinstance(step, MappingNode):
                    continue
                start = step.start_mark.line
                end = step.end_mark.line + 1
                result.append(
                    Step(
                        index,
                        start + 1,
                        step.start_mark.column,
                        [(line_number + 1, line) for line_number, line in enumerate(source_lines[start:end], start=start)],
                        step,
                        self.source,
                        self.default_shell,
                    )
                )
            return result
        steps_line = steps_mapping_index(self.lines, self.indent)
        if steps_line is None:
            return []
        return build_steps(self.lines[steps_line + 1 :], self.indent)


def indentation(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def step_mapping_tail(
    line: str, position: int, step_indent: int, line_indent: int
) -> str | None:
    """Return a direct step-mapping tail in the supported YAML subset."""

    tail = line[line_indent:]
    if position == 0 and line_indent == step_indent and tail.startswith("- "):
        return tail[2:]
    if line_indent == step_indent + 2:
        return tail
    return None


def direct_step_entries(
    lines: Sequence[tuple[int, str]], step_indent: int
) -> Iterable[tuple[int, int, tuple[str, str]]]:
    """Yield direct mapping entries from one workflow step."""

    for position, (_, line) in enumerate(lines):
        line_indent = indentation(line)
        tail = step_mapping_tail(line, position, step_indent, line_indent)
        if tail is None:
            continue
        entry = mapping_entry(tail)
        if entry is not None:
            yield position, line_indent, entry


def direct_child_mapping(
    lines: Sequence[tuple[int, str]], parent_indent: int
) -> dict[str, str]:
    """Collect direct scalar children until the parent mapping ends."""

    result: dict[str, str] = {}
    for _, child_line in lines:
        child_indent = indentation(child_line)
        if child_line.strip() and child_indent <= parent_indent:
            break
        if child_indent != parent_indent + 2:
            continue
        child_entry = mapping_entry(child_line[child_indent:])
        if child_entry is not None:
            result[child_entry[0]] = clean_scalar(child_entry[1])
    return result


def step_run_value(
    value: str, following_lines: Sequence[tuple[int, str]], parent_indent: int
) -> str:
    """Return a supported inline or block ``run`` value."""

    scalar = clean_scalar(value)
    if not scalar.startswith(("|", ">")):
        return scalar
    return textwrap.dedent("\n".join(block_lines(following_lines, parent_indent))).strip()


def block_lines(
    lines: Sequence[tuple[int, str]], parent_indent: int
) -> list[str]:
    """Return a YAML block body without crossing its parent indentation."""

    result: list[str] = []
    for _, line in lines:
        if line.strip() and indentation(line) <= parent_indent:
            break
        result.append(line)
    return result


def steps_mapping_index(lines: Sequence[tuple[int, str]], job_indent: int) -> int | None:
    """Locate the direct ``steps:`` mapping in a parsed job."""

    for position, (_, line) in enumerate(lines):
        if indentation(line) == job_indent + 2 and line.strip() == "steps:":
            return position
    return None


def append_step(
    result: list[Step],
    lines: list[tuple[int, str]] | None,
    start_line: int,
    step_indent: int,
) -> None:
    """Append one accumulated workflow step when one is available."""

    if lines is not None:
        result.append(Step(len(result), start_line, step_indent, lines))


def build_steps(lines: Sequence[tuple[int, str]], job_indent: int) -> list[Step]:
    """Split the bounded YAML ``steps:`` body into individual steps."""

    step_indent = job_indent + 4
    result: list[Step] = []
    current: list[tuple[int, str]] | None = None
    current_start = 0
    for line_number, line in lines:
        line_indent = indentation(line)
        if line.strip() and line_indent <= job_indent + 2:
            break
        if line_indent == step_indent and line[line_indent:].startswith("- "):
            append_step(result, current, current_start, step_indent)
            current = [(line_number, line)]
            current_start = line_number
            continue
        if current is not None:
            current.append((line_number, line))
    append_step(result, current, current_start, step_indent)
    return result


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


def is_ascii_decimal(value: str) -> bool:
    """Return whether *value* contains one or more ASCII decimal digits."""

    return bool(value) and all("0" <= character <= "9" for character in value)


def is_exact_python_313_version(value: str) -> bool:
    """Return whether *value* is the accepted ``3.13.N`` version shape."""

    prefix = "3.13."
    if not value.startswith(prefix):
        return False
    patch = value.removeprefix(prefix)
    return patch == "0" or (
        bool(patch) and patch[0] != "0" and is_ascii_decimal(patch)
    )


def parse_exact_version(value: str, source: str) -> str:
    if not is_exact_python_313_version(value):
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


def read_workflow_lines(path: Path) -> tuple[list[str] | None, list[str]]:
    """Read a workflow as text without broadening the parser boundary."""

    try:
        return path.read_text(encoding="utf-8").splitlines(), []
    except UnicodeDecodeError as exc:
        return None, [f"cannot decode workflow {path.name}: {exc}"]
    except OSError as exc:
        return None, [f"cannot read workflow {path.name}: {exc}"]


def jobs_mapping_index(lines: Sequence[str]) -> int | None:
    """Locate the top-level ``jobs:`` mapping when it exists."""

    for index, line in enumerate(lines):
        if indentation(line) == 0 and line.strip() == "jobs:":
            return index
    return None


def starts_top_level_section(line: str) -> bool:
    """Return whether a nonblank line ends the current ``jobs:`` section."""

    return bool(line.strip()) and indentation(line) == 0


def job_block_transition(
    line: str, current_indent: int | None
) -> tuple[int | None, str | None]:
    """Return the selected job indentation and any new job header."""

    line_indent = indentation(line)
    header = job_header(line[line_indent:])
    if header is None:
        return current_indent, None
    if current_indent is None:
        return line_indent, header
    if line_indent == current_indent:
        return current_indent, header
    return current_indent, None


def workflow_job_blocks(
    path: Path, lines: Sequence[str], jobs_start: int
) -> Iterable[tuple[JobIdentity, int, list[tuple[int, str]]]]:
    """Yield the narrow, indentation-delimited jobs below ``jobs:``."""

    job_indent: int | None = None
    current_identity: JobIdentity | None = None
    current_lines: list[tuple[int, str]] = []
    for line_number, line in enumerate(lines[jobs_start + 1 :], start=jobs_start + 2):
        if starts_top_level_section(line):
            break
        job_indent, header = job_block_transition(line, job_indent)
        if header is not None:
            if current_identity is not None:
                assert job_indent is not None
                yield current_identity, job_indent, current_lines
            current_identity = JobIdentity(path.name, header)
            current_lines = [(line_number, line)]
            continue
        if current_identity is not None:
            current_lines.append((line_number, line))
    if current_identity is not None:
        assert job_indent is not None
        yield current_identity, job_indent, current_lines


def semantic_job_header_violations(path: Path, text: str) -> tuple[set[str], list[str]]:
    """Return canonical semantic job IDs or fail closed on YAML indirection.

    The source-level job/step parser below intentionally stays narrow because
    it also records exact shell source.  It must never silently omit a YAML
    job that GitHub can execute, though.  Parse the *job inventory* with
    PyYAML's node tree first, then accept only the canonical block mapping
    syntax that the narrow parser understands.  Quoted/escaped, explicit,
    alias/merge, duplicate, and flow-style job declarations are rejected
    instead of being invisible to the Python-use inventory.
    """

    try:
        for token in yaml.scan(text, Loader=yaml.BaseLoader):
            if isinstance(token, (AliasToken, AnchorToken)):
                return set(), [
                    f"workflow must not use YAML anchors or aliases: {path.name}"
                ]
            if isinstance(token, (FlowMappingStartToken, FlowSequenceStartToken)):
                return set(), [
                    f"workflow must not use YAML flow collections: {path.name}"
                ]
            if isinstance(token, TagToken):
                return set(), [f"workflow must not use YAML tags: {path.name}"]
        document = yaml.compose(text, Loader=yaml.BaseLoader)
    except (RecursionError, yaml.YAMLError) as error:
        return set(), [f"workflow is not valid YAML: {path.name}: {error}"]
    if not isinstance(document, MappingNode):
        return set(), [f"workflow root is not a mapping: {path.name}"]

    lines = text.splitlines()
    shape_violations: list[str] = []
    visited: set[int] = set()

    def visit(node: Node, *, context: str) -> None:
        identity = id(node)
        if identity in visited:
            return
        visited.add(identity)
        if isinstance(node, MappingNode):
            if node.flow_style:
                shape_violations.append(
                    f"workflow must not use YAML flow collections: {path.name}"
                )
                return
            keys: set[str] = set()
            for key, value in node.value:
                if not isinstance(key, ScalarNode):
                    shape_violations.append(
                        f"workflow has a non-scalar mapping key: {path.name}"
                    )
                    continue
                try:
                    source_line = lines[key.start_mark.line]
                except IndexError:
                    shape_violations.append(
                        f"workflow key has an invalid source mark: {path.name}"
                    )
                    continue
                if (
                    key.style is not None
                    or key.value == "<<"
                    or key.value in keys
                    or source_line.lstrip().startswith("?")
                ):
                    shape_violations.append(
                        f"workflow must use canonical unquoted mapping keys: {path.name}"
                    )
                    continue
                keys.add(key.value)
                visit(value, context=f"{context}.{key.value}")
            return
        if isinstance(node, SequenceNode):
            if node.flow_style:
                shape_violations.append(
                    f"workflow must not use YAML flow collections: {path.name}"
                )
                return
            for index, value in enumerate(node.value):
                visit(value, context=f"{context}[{index}]")
            return
        if isinstance(node, ScalarNode):
            source = text[node.start_mark.index : node.end_mark.index]
            if node.style == '"' and "\\" in source:
                shape_violations.append(
                    f"workflow must not use escaped double-quoted scalars: {path.name}"
                )
            return
        shape_violations.append(f"workflow has an unsupported YAML node: {path.name}")

    visit(document, context="workflow")
    if shape_violations:
        return set(), sorted(set(shape_violations))

    top_level: dict[str, Node] = {}
    for key, value in document.value:
        if not isinstance(key, ScalarNode):
            return set(), [f"workflow has a non-scalar top-level key: {path.name}"]
        if key.value == "<<":
            return set(), [f"workflow uses an unsupported top-level merge key: {path.name}"]
        if key.value in top_level:
            return set(), [f"workflow has a duplicate top-level key {key.value!r}: {path.name}"]
        top_level[key.value] = value

    jobs = top_level.get("jobs")
    if jobs is None:
        return set(), []
    if not isinstance(jobs, MappingNode) or jobs.flow_style:
        return set(), [f"workflow jobs must use a canonical block mapping: {path.name}"]

    identities: set[str] = set()
    violations: list[str] = []
    for key, value in jobs.value:
        if not isinstance(key, ScalarNode):
            violations.append(f"workflow job key is not a scalar: {path.name}")
            continue
        name = key.value
        if (
            key.style is not None
            or not is_mapping_key(name)
            or not isinstance(value, MappingNode)
            or value.flow_style
        ):
            violations.append(
                f"workflow job must use a canonical unquoted block header: {path.name}:{name!r}"
            )
            continue
        if name in identities:
            violations.append(f"duplicate workflow job: {path.name}:{name}")
            continue
        try:
            source_line = lines[key.start_mark.line]
        except IndexError:
            violations.append(f"workflow job has an invalid source mark: {path.name}:{name}")
            continue
        expected_header = re.compile(rf"^  {re.escape(name)}:\s*(?:#.*)?$")
        if expected_header.fullmatch(source_line) is None:
            violations.append(
                f"workflow job must use a canonical unquoted block header: {path.name}:{name!r}"
            )
            continue
        identities.add(name)
    return identities, violations


def add_job_block(
    result: dict[JobIdentity, Job],
    violations: list[str],
    identity: JobIdentity,
    job_indent: int,
    lines: list[tuple[int, str]],
) -> None:
    """Record one workflow job or retain the existing duplicate diagnostic."""

    if identity in result:
        violations.append(f"duplicate workflow job: {identity.display()}")
        return
    result[identity] = Job(identity, job_indent, list(lines))


def semantic_workflow_jobs(
    path: Path, source: str
) -> tuple[
    list[tuple[str, ScalarNode, MappingNode, str | None, dict[str, str]]],
    list[str],
]:
    """Return every executable job from the YAML node tree.

    The contract needs exact shell source for a few provenance checks, but its
    job/step inventory must use the same decoded YAML structure GitHub sees.
    This accepts valid aliases, comments, quoted keys, and flow collections
    while rejecting only ambiguous duplicate/merge mappings and malformed job
    structures.  ``Job``/``Step`` then consume these semantic nodes directly.
    """

    try:
        document = yaml.compose(source, Loader=yaml.BaseLoader)
    except (RecursionError, yaml.YAMLError) as error:
        return [], [f"workflow is not valid YAML: {path.name}: {error}"]
    if not isinstance(document, MappingNode):
        return [], [f"workflow root is not a mapping: {path.name}"]

    active: set[int] = set()
    checked: set[int] = set()

    def validate(node: Node, *, context: str) -> None:
        identity = id(node)
        if identity in active:
            raise ContractInputError(f"{context} has a recursive YAML alias")
        if identity in checked:
            return
        active.add(identity)
        if isinstance(node, MappingNode):
            for key, value in semantic_mapping_items(node, context=context).items():
                validate(value, context=f"{context}.{key}")
        elif isinstance(node, SequenceNode):
            for index, value in enumerate(node.value):
                validate(value, context=f"{context}[{index}]")
        elif not isinstance(node, ScalarNode):
            raise ContractInputError(f"{context} has an unsupported YAML node")
        active.remove(identity)
        checked.add(identity)

    try:
        validate(document, context=f"workflow {path.name}")
        top_level = semantic_mapping_items(document, context=f"workflow {path.name}")
    except ContractInputError as error:
        return [], [str(error)]

    def default_run_shell(
        fields: dict[str, Node], *, context: str
    ) -> str | None:
        defaults = fields.get("defaults")
        if defaults is None:
            return None
        if not isinstance(defaults, MappingNode):
            raise ContractInputError(f"{context}.defaults is not a mapping")
        run = semantic_mapping_items(defaults, context=f"{context}.defaults").get("run")
        if run is None:
            return None
        if not isinstance(run, MappingNode):
            raise ContractInputError(f"{context}.defaults.run is not a mapping")
        run_defaults = semantic_mapping_items(run, context=f"{context}.defaults.run")
        if "working-directory" in run_defaults:
            raise ContractInputError(
                f"{context}.defaults.run must not set working-directory"
            )
        shell = run_defaults.get("shell")
        if shell is None:
            return None
        if not isinstance(shell, ScalarNode):
            raise ContractInputError(f"{context}.defaults.run.shell is not a scalar")
        return shell.value

    try:
        workflow_default_shell = default_run_shell(
            top_level, context=f"workflow {path.name}"
        )
        workflow_environment = scalar_environment_values(
            top_level, context=f"workflow {path.name}"
        )
    except ContractInputError as error:
        return [], [str(error)]
    jobs = top_level.get("jobs")
    if jobs is None:
        return [], []
    if not isinstance(jobs, MappingNode):
        return [], [f"workflow jobs is not a mapping: {path.name}"]

    result: list[tuple[str, ScalarNode, MappingNode, str | None, dict[str, str]]] = []
    try:
        semantic_mapping_items(jobs, context=f"workflow jobs {path.name}")
        for key_node, value in jobs.value:
            if not isinstance(key_node, ScalarNode):
                return [], [f"workflow job key is not a scalar: {path.name}"]
            name = key_node.value
            if not is_mapping_key(name):
                return [], [f"workflow job has an invalid identifier {name!r}: {path.name}"]
            if not isinstance(value, MappingNode):
                return [], [f"workflow job is not a mapping: {path.name}:{name}"]
            fields = semantic_mapping_items(
                value, context=f"workflow job {path.name}:{name}"
            )
            job_default_shell = default_run_shell(
                fields, context=f"workflow job {path.name}:{name}"
            )
            environment = dict(workflow_environment)
            environment.update(
                scalar_environment_values(
                    fields, context=f"workflow job {path.name}:{name}"
                )
            )
            steps = fields.get("steps")
            if steps is not None:
                if not isinstance(steps, SequenceNode):
                    return [], [f"workflow job steps is not a sequence: {path.name}:{name}"]
                if any(not isinstance(step, MappingNode) for step in steps.value):
                    return [], [
                        f"workflow job step is not a mapping: {path.name}:{name}"
                    ]
            result.append(
                (
                    name,
                    key_node,
                    value,
                    job_default_shell or workflow_default_shell,
                    environment,
                )
            )
    except ContractInputError as error:
        return [], [f"cannot decode workflow jobs {path.name}: {error}"]
    return result, []


def parse_jobs(path: Path) -> tuple[dict[JobIdentity, Job], list[str]]:
    lines, read_errors = read_workflow_lines(path)
    if lines is None:
        return {}, read_errors

    source = "\n".join(lines)
    semantic_jobs, semantic_violations = semantic_workflow_jobs(path, source)
    if semantic_violations:
        return {}, semantic_violations
    result: dict[JobIdentity, Job] = {}
    violations: list[str] = []
    for name, key, node, default_shell, inherited_environment in semantic_jobs:
        identity = JobIdentity(path.name, name)
        if identity in result:
            violations.append(f"duplicate workflow job: {identity.display()}")
            continue
        start = key.start_mark.line
        end = node.end_mark.line + 1
        job_lines = [
            (line_number + 1, line)
            for line_number, line in enumerate(lines[start:end], start=start)
        ]
        result[identity] = Job(
            identity,
            key.start_mark.column,
            job_lines,
            node,
            source,
            default_shell,
            inherited_environment,
        )
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
    redirection_operator: str | None = None


@dataclass(frozen=True)
class ShellCommand:
    command: ShellWord
    arguments: tuple[ShellWord, ...]
    prefix: tuple[ShellWord, ...] = ()


@dataclass(frozen=True)
class ShellAnalysis:
    commands: tuple[ShellCommand, ...]
    errors: tuple[str, ...]
    words: tuple[ShellWord, ...]


@dataclass
class ShellScanState:
    """Mutable state for one bounded linear shell scan."""

    cursor: int
    words: list[ShellWord]
    redirection_operator: str | None = None


@dataclass
class ShellWordReadState:
    """Mutable state while consuming one source-only shell word."""

    characters: list[str]
    dynamic: bool = False
    quote: str | None = None
    stopped: bool = False


def command_basename(command: str) -> str:
    return command.rsplit("/", 1)[-1]


def static_command_basename(word: ShellWord) -> str | None:
    """Return a statically known executable basename, if one is available."""

    basename = command_basename(word.value)
    if word.dynamic and "$" in basename:
        return None
    return basename


def is_dotted_ascii_decimal(value: str) -> bool:
    """Return whether *value* is one or more dotted ASCII decimal components."""

    return all(is_ascii_decimal(component) for component in value.split("."))


def is_versioned_command_name(command: str, prefix: str) -> bool:
    """Recognize an unversioned or dotted-ASCII-version executable name."""

    if not command.startswith(prefix):
        return False
    suffix = command.removeprefix(prefix)
    return not suffix or is_dotted_ascii_decimal(suffix)


def is_python_or_pip_command(command: str) -> bool:
    basename = command_basename(command)
    return any(
        is_versioned_command_name(basename, prefix) for prefix in ("python", "pip")
    )


def is_bare_pip_command(command: str) -> bool:
    return is_versioned_command_name(command_basename(command), "pip")


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


def advance_heredoc_quote(
    line: str, cursor: int, quote: str
) -> tuple[int, str | None]:
    """Advance one quoted character while looking only for heredoc openings."""

    character = line[cursor]
    if character == "\\" and quote == '"':
        return cursor + 2, quote
    if character == quote:
        return cursor + 1, None
    return cursor + 1, quote


def shell_comment_starts(line: str, cursor: int) -> bool:
    """Return whether ``#`` begins a supported shell comment."""

    if line[cursor] != "#":
        return False
    return cursor == 0 or line[cursor - 1].isspace() or line[cursor - 1] in ";|&"


def heredoc_starts_at(line: str, cursor: int) -> bool:
    """Return whether the cursor starts a possible here-document operator."""

    return line[cursor] == "<" and cursor + 1 < len(line) and line[cursor + 1] == "<"


def record_heredoc_opening(
    openings: list[tuple[str, bool]],
    errors: list[str],
    delimiter: str | None,
    strip_tabs: bool,
    error: str | None,
) -> None:
    """Retain a valid delimiter or its fail-closed scanner error."""

    if error is not None:
        errors.append(error)
    elif delimiter is not None:
        openings.append((delimiter, strip_tabs))


def heredoc_openings(line: str) -> tuple[list[tuple[str, bool]], list[str]]:
    """Find static here-document openings outside comments and shell quotes."""

    openings: list[tuple[str, bool]] = []
    errors: list[str] = []
    cursor = 0
    quote: str | None = None
    while cursor < len(line):
        character = line[cursor]
        if quote is not None:
            cursor, quote = advance_heredoc_quote(line, cursor, quote)
            continue
        if character in {"'", '"'}:
            quote = character
            cursor += 1
            continue
        if character == "\\":
            cursor += 2
            continue
        if shell_comment_starts(line, cursor):
            break
        if heredoc_starts_at(line, cursor):
            delimiter, strip_tabs, cursor, error = read_heredoc_delimiter(line, cursor)
            record_heredoc_opening(openings, errors, delimiter, strip_tabs, error)
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
        self.words: list[ShellWord] = []

    def scan(self) -> ShellAnalysis:
        limit_error = self._scanner_limit_error()
        if limit_error is not None:
            return ShellAnalysis((), (limit_error,), ())

        state = ShellScanState(0, [])
        while state.cursor < len(self.source):
            self._scan_next(state)
        self._finish_scan(state)
        return ShellAnalysis(
            tuple(self.commands), tuple(self.errors), tuple(self.words)
        )

    def _scanner_limit_error(self) -> str | None:
        if len(self.source) > MAX_SHELL_SOURCE_LENGTH:
            return f"shell source exceeds {MAX_SHELL_SOURCE_LENGTH} byte scanner limit"
        if self.depth > MAX_SHELL_NESTING:
            return f"shell nesting exceeds {MAX_SHELL_NESTING} levels"
        return None

    def _scan_next(self, state: ShellScanState) -> None:
        character = self.source[state.cursor]
        if character in " \t\r":
            state.cursor += 1
            return
        if shell_comment_starts(self.source, state.cursor):
            state.cursor = self._comment_end(state.cursor)
            return
        if character == "\n" or character in ";|&":
            self._consume_command_boundary(state, character)
            return
        redirection_start = self._redirection_start(state.cursor)
        if redirection_start is not None:
            state.cursor, state.redirection_operator = self._consume_redirection(
                redirection_start
            )
            return
        if character in "()":
            self._consume_parenthesis(state, character)
            return
        self._consume_word(state)

    def _comment_end(self, cursor: int) -> int:
        end = self.source.find("\n", cursor)
        return len(self.source) if end < 0 else end

    def _consume_command_boundary(self, state: ShellScanState, character: str) -> None:
        if state.redirection_operator is not None:
            self.errors.append("redirection has no target")
            state.redirection_operator = None
        self._finish_segment(state.words)
        state.words = []
        state.cursor = self._after_command_boundary(state.cursor, character)

    def _after_command_boundary(self, cursor: int, character: str) -> int:
        next_cursor = cursor + 1
        if (
            character in "|&"
            and next_cursor < len(self.source)
            and self.source[next_cursor] == character
        ):
            return next_cursor + 1
        return next_cursor

    def _consume_parenthesis(self, state: ShellScanState, character: str) -> None:
        if character == "(" and self._is_function_declaration(state):
            state.words = []
            state.cursor += 2
            return
        if character == "(":
            if state.redirection_operator is not None:
                state.redirection_operator = None
            self._finish_segment(state.words)
            state.words = []
            state.cursor += 1
            return
        self._finish_segment(state.words)
        state.words = []
        state.cursor += 1

    def _is_function_declaration(self, state: ShellScanState) -> bool:
        cursor = state.cursor
        return (
            cursor + 1 < len(self.source)
            and self.source[cursor + 1] == ")"
            and len(state.words) == 1
            and not state.words[0].dynamic
        )

    def _consume_word(self, state: ShellScanState) -> None:
        word, state.cursor = self._read_word(state.cursor)
        if state.redirection_operator is not None:
            word = ShellWord(
                word.value,
                word.dynamic,
                redirection_target=True,
                redirection_operator=state.redirection_operator,
            )
            state.redirection_operator = None
        state.words.append(word)
        self.words.append(word)

    def _finish_scan(self, state: ShellScanState) -> None:
        if state.redirection_operator is not None:
            self.errors.append("redirection has no target")
        self._finish_segment(state.words)

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

    def _consume_redirection(self, cursor: int) -> tuple[int, str | None]:
        operator = self.source[cursor]
        cursor += 1
        if cursor < len(self.source) and self.source[cursor] == operator:
            cursor += 1
            operator *= 2
        if operator == "<" and cursor < len(self.source) and self.source[cursor] == "-":
            cursor += 1
            operator = "<-"
        if cursor < len(self.source) and self.source[cursor] == "&":
            cursor += 1
            while cursor < len(self.source) and (
                self.source[cursor].isdigit() or self.source[cursor] == "-"
            ):
                cursor += 1
            return cursor, None
        return cursor, operator

    def _read_word(self, cursor: int) -> tuple[ShellWord, int]:
        state = ShellWordReadState([])
        while cursor < len(self.source) and not state.stopped:
            if self._word_boundary(cursor, state.quote):
                break
            cursor = self._consume_word_character(cursor, state)
        if state.quote is not None and not state.stopped:
            self.errors.append("unterminated shell quote")
        return ShellWord("".join(state.characters), state.dynamic), cursor

    def _word_boundary(self, cursor: int, quote: str | None) -> bool:
        return quote is None and self.source[cursor] in " \t\r\n;|&<>()"

    def _consume_word_character(
        self, cursor: int, state: ShellWordReadState
    ) -> int:
        if state.quote is None:
            return self._consume_unquoted_word_character(cursor, state)
        return self._consume_quoted_word_character(cursor, state)

    def _consume_quoted_word_character(
        self, cursor: int, state: ShellWordReadState
    ) -> int:
        quote = state.quote
        assert quote is not None
        character = self.source[cursor]
        if character == quote:
            state.quote = None
            return cursor + 1
        if character == "\\" and quote == '"':
            return self._consume_quoted_escape(cursor, state)
        if character == "$" and quote == '"':
            return self._consume_word_expansion(cursor, state)
        if character == "`" and quote == '"':
            self.errors.append("backtick command substitution is unsupported")
        state.characters.append(character)
        return cursor + 1

    def _consume_quoted_escape(
        self, cursor: int, state: ShellWordReadState
    ) -> int:
        if cursor + 1 >= len(self.source):
            self.errors.append("dangling shell escape")
            state.stopped = True
            return len(self.source)
        state.characters.append(self.source[cursor + 1])
        return cursor + 2

    def _consume_unquoted_word_character(
        self, cursor: int, state: ShellWordReadState
    ) -> int:
        character = self.source[cursor]
        if character in {"'", '"'}:
            state.quote = character
            return cursor + 1
        if character == "\\":
            return self._consume_unquoted_escape(cursor, state)
        if character == "$":
            return self._consume_word_expansion(cursor, state)
        if character == "`":
            self.errors.append("backtick command substitution is unsupported")
        state.characters.append(character)
        return cursor + 1

    def _consume_unquoted_escape(
        self, cursor: int, state: ShellWordReadState
    ) -> int:
        if cursor + 1 >= len(self.source):
            self.errors.append("dangling shell escape")
            state.stopped = True
            return len(self.source)
        if self.source[cursor + 1] != "\n":
            state.characters.append(self.source[cursor + 1])
        return cursor + 2

    def _consume_word_expansion(
        self, cursor: int, state: ShellWordReadState
    ) -> int:
        cursor, expansion_dynamic = self._read_expansion(cursor, state.characters)
        state.dynamic = state.dynamic or expansion_dynamic
        return cursor

    def _read_expansion(self, cursor: int, characters: list[str]) -> tuple[int, bool]:
        if cursor + 1 >= len(self.source):
            characters.append("$")
            return cursor + 1, True
        marker = self.source[cursor + 1]
        if marker == "'":
            return self._read_ansi_c_quoted_string(cursor, characters)
        if marker == "(":
            return self._read_parenthesized_expansion(cursor, characters)
        if marker == "{":
            return self._read_braced_expansion(cursor, characters)
        if marker.isalpha() or marker == "_":
            return self._read_named_expansion(cursor, characters)
        characters.append(self.source[cursor : cursor + 2])
        return cursor + 2, True

    def _read_ansi_c_quoted_string(
        self, cursor: int, characters: list[str]
    ) -> tuple[int, bool]:
        """Consume Bash's static ANSI-C ``$'...'`` quote form.

        It is used for NUL/newline/tab-safe fixed literals in trusted
        workflows.  Treat the contents as a static word rather than letting
        the closing quote start an unrelated shell quote state; dynamic shell
        expansions are not evaluated inside this form.
        """

        position = cursor + 2
        while position < len(self.source):
            character = self.source[position]
            if character == "'":
                return position + 1, False
            if character == "\\":
                if position + 1 >= len(self.source):
                    self.errors.append("dangling ANSI-C shell escape")
                    return len(self.source), False
                characters.append(self.source[position + 1])
                position += 2
                continue
            characters.append(character)
            position += 1
        self.errors.append("unterminated ANSI-C shell quote")
        return len(self.source), False

    def _read_parenthesized_expansion(
        self, cursor: int, characters: list[str]
    ) -> tuple[int, bool]:
        content, end = self._command_substitution(cursor)
        if content is None:
            self.errors.append("unterminated command substitution")
            return len(self.source), True
        self._inspect_parenthesized_expansion(content)
        characters.append("$()")
        return end, True

    def _inspect_parenthesized_expansion(self, content: str) -> None:
        if content.startswith("("):
            self._validate_arithmetic_expansion(content)
            return
        nested = ShellScanner(content, self.depth + 1).scan()
        self.commands.extend(nested.commands)
        self.errors.extend(nested.errors)
        self.words.extend(nested.words)

    def _validate_arithmetic_expansion(self, content: str) -> None:
        """Reject executable substitutions hidden inside arithmetic expansion."""

        if "$(" in content[1:]:
            self.errors.append(
                "arithmetic expansion with command substitution is unsupported"
            )
        if "`" in content:
            self.errors.append(
                "arithmetic expansion with backtick substitution is unsupported"
            )

    def _read_braced_expansion(
        self, cursor: int, characters: list[str]
    ) -> tuple[int, bool]:
        end = self._braced_expansion_end(cursor)
        if end is None:
            self.errors.append("unterminated braced shell expansion")
            return len(self.source), True
        characters.append("${}")
        return end, True

    def _read_named_expansion(
        self, cursor: int, characters: list[str]
    ) -> tuple[int, bool]:
        end = self._named_expansion_end(cursor)
        characters.append(self.source[cursor:end])
        return end, True

    def _named_expansion_end(self, cursor: int) -> int:
        end = cursor + 2
        while end < len(self.source) and (
            self.source[end].isalnum() or self.source[end] == "_"
        ):
            end += 1
        return end

    def _command_substitution(self, start: int) -> tuple[str | None, int]:
        cursor = start + 2
        content_start = cursor
        depth = 1
        quote: str | None = None
        while cursor < len(self.source):
            cursor, depth, quote = self._advance_command_substitution(
                cursor, depth, quote
            )
            if depth == 0:
                return self.source[content_start : cursor - 1], cursor
        return None, len(self.source)

    def _advance_command_substitution(
        self, cursor: int, depth: int, quote: str | None
    ) -> tuple[int, int, str | None]:
        if quote is not None:
            return self._advance_substitution_quote(cursor, depth, quote)
        character = self.source[cursor]
        if character in {"'", '"'}:
            return cursor + 1, depth, character
        if character == "\\":
            return cursor + 2, depth, None
        if character == "(":
            return cursor + 1, depth + 1, None
        if character == ")":
            return cursor + 1, depth - 1, None
        return cursor + 1, depth, None

    def _advance_substitution_quote(
        self, cursor: int, depth: int, quote: str
    ) -> tuple[int, int, str | None]:
        character = self.source[cursor]
        if character == "\\" and quote == '"':
            return cursor + 2, depth, quote
        if character == quote:
            return cursor + 1, depth, None
        return cursor + 1, depth, quote

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
        cursor = self._first_non_assignment_word(usable)
        while cursor < len(usable):
            cursor, command, error, finished = self._command_head_transition(
                usable, cursor
            )
            if error is not None:
                return None, error
            if command is not None:
                return command, None
            if finished:
                return None, None
        return None, None

    def _first_non_assignment_word(self, words: Sequence[ShellWord]) -> int:
        cursor = 0
        while cursor < len(words) and is_shell_assignment(words[cursor]):
            cursor += 1
        return cursor

    def _command_head_transition(
        self, words: list[ShellWord], cursor: int
    ) -> tuple[int, ShellCommand | None, str | None, bool]:
        word = words[cursor]
        value = word.value if not word.dynamic else None
        if value in {"case", "for", "function"}:
            return cursor, None, None, True
        if value in SHELL_INDIRECTION_BUILTINS:
            return (
                cursor,
                None,
                f"shell indirection builtin {value!r} is unsupported",
                True,
            )
        if value in SHELL_CONTROL_WORDS:
            return cursor + 1, None, None, False
        if value == "command":
            return self._command_wrapper_transition(words, cursor)
        if value == "env":
            next_cursor, error = self._skip_env_options(words, cursor + 1)
            return next_cursor, None, error, False
        if value == "sudo":
            next_cursor, error = self._skip_wrapper_options(words, cursor + 1)
            return next_cursor, None, error, False
        basename = static_command_basename(word)
        if basename is None:
            return cursor, None, "dynamic shell command head is unsupported", True
        return (
            cursor,
            ShellCommand(
                word,
                tuple(words[cursor + 1 :]),
                tuple(words[:cursor]),
            ),
            None,
            True,
        )

    def _command_wrapper_transition(
        self, words: list[ShellWord], cursor: int
    ) -> tuple[int, ShellCommand | None, str | None, bool]:
        option_cursor = cursor + 1
        if (
            option_cursor < len(words)
            and words[option_cursor].value in SHELL_COMMAND_OPTION_ONLY
        ):
            return option_cursor, None, None, True
        if (
            option_cursor < len(words)
            and not words[option_cursor].dynamic
            and words[option_cursor].value == "-p"
        ):
            # ``command -p`` changes PATH for the invoked command; it does
            # not consume the following executable as an option value.
            return option_cursor + 1, None, None, False
        next_cursor, error = self._skip_wrapper_options(words, option_cursor)
        return next_cursor, None, error, False

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
            cursor, finished, error = self._env_option_transition(words, cursor)
            if error is not None:
                return cursor, error
            if finished:
                return cursor, None
        return cursor, None

    def _env_option_transition(
        self, words: list[ShellWord], cursor: int
    ) -> tuple[int, bool, str | None]:
        word = words[cursor]
        if word.value == "--" and not word.dynamic:
            return cursor + 1, True, None
        if is_shell_assignment(word):
            return cursor + 1, False, None
        if word.dynamic:
            return cursor, True, "dynamic env command head is unsupported"
        if not word.value.startswith("-") or word.value == "-":
            return cursor, True, None
        next_cursor = cursor + 1
        if word.value not in {"-C", "-u", "--chdir", "--unset"}:
            return next_cursor, False, None
        if next_cursor >= len(words):
            return next_cursor, True, "env option has no value"
        return next_cursor + 1, False, None

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
            self.words.extend(nested.words)
            return


def analyze_shell_source(run: str) -> ShellAnalysis:
    source, heredoc_errors = shell_source_without_heredoc_bodies(run)
    scanned = ShellScanner(source).scan()
    return ShellAnalysis(scanned.commands, heredoc_errors + scanned.errors, scanned.words)


def static_github_env_writer_key(source: str) -> str | None:
    """Return a literal key from one intentionally narrow env-file writer."""

    match = STATIC_GITHUB_ENV_ECHO.fullmatch(source)
    if match is None:
        match = STATIC_GITHUB_ENV_PRINTF.fullmatch(source)
    return match.group("key") if match is not None else None


def github_env_group_writers(
    lines: list[str], closing_index: int
) -> list[str] | None:
    """Return a simple ``{ echo ...; } >> "$GITHUB_ENV"`` group body.

    Nested or otherwise indirect groups are intentionally outside this small
    grammar: persisting an environment key that cannot be statically named is
    not safe for a job whose subsequent Python executable is path-bound.
    """

    for opening_index in range(closing_index - 1, -1, -1):
        if lines[opening_index].strip() == "{":
            return lines[opening_index + 1 : closing_index]
    return None


def github_env_write_error(run: str) -> str | None:
    """Reject indirect or unapproved writes to GitHub's environment file.

    Matching only ``PATH=`` is not sufficient: shell arguments can assemble
    that key dynamically.  The accepted forms therefore have a literal key in
    source and are limited to an audited non-interpreter allowlist.
    """

    if "GITHUB_ENV" not in run:
        return None
    lines = run.splitlines()
    for line_index, line in enumerate(lines):
        if "GITHUB_ENV" not in line:
            continue
        redirect = GITHUB_ENV_REDIRECT.search(line)
        if redirect is None:
            return "indirect or unsupported GITHUB_ENV write"
        writer = line[: redirect.start()].strip()
        if writer == "}":
            writers = github_env_group_writers(lines, line_index)
            if writers is None:
                return "unsupported GITHUB_ENV writer group"
        else:
            writers = [writer]
        for source in writers:
            stripped = source.strip()
            if not stripped or stripped.startswith("#"):
                continue
            key = static_github_env_writer_key(stripped)
            if key is None:
                return "indirect or unsupported GITHUB_ENV writer"
            if key not in ALLOWED_GITHUB_ENV_KEYS:
                return f"unapproved GITHUB_ENV key {key!r}"
    return None


def simple_redirect_path_variables(run: str) -> frozenset[str]:
    """Return variables that are assigned only bounded local output paths."""

    assignments: dict[str, bool] = {}
    source, _ = shell_source_without_heredoc_bodies(run)
    for match in SIMPLE_REDIRECT_PATH_ASSIGNMENT.finditer(source):
        name = match.group("name")
        value = match.group("value").strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        is_safe = SIMPLE_REDIRECT_PATH_VALUE.fullmatch(value) is not None
        assignments[name] = assignments.get(name, True) and is_safe
    return frozenset(name for name, is_safe in assignments.items() if is_safe)


def bounded_dynamic_output_target(
    target: str,
    safe_variables: frozenset[str],
    *,
    allowed_github_targets: frozenset[str],
) -> bool:
    """Return whether one dynamic write target has a bounded source form."""

    if target in allowed_github_targets:
        return True
    if target.startswith("$RUNNER_TEMP/") or target.startswith("$GITHUB_WORKSPACE/"):
        return True
    variable = DYNAMIC_OUTPUT_REDIRECT_VARIABLE.fullmatch(target)
    return variable is not None and variable.group("name") in safe_variables


def dynamic_output_redirection_error(run: str) -> str | None:
    """Reject opaque dynamic output paths that could resolve to GitHub files.

    GitHub environment files are process-provided paths.  A workflow must not
    discover one through ``set``, ``grep``, indirection, or another opaque
    shell variable and then redirect output there.  Direct GitHub output files,
    direct runner/workspace paths, and variables with a bounded local path
    assignment are the only accepted dynamic output targets.
    """

    safe_variables = simple_redirect_path_variables(run)
    for word in analyze_shell_source(run).words:
        if (
            not word.redirection_target
            or word.redirection_operator not in {">", ">>"}
            or not word.dynamic
        ):
            continue
        target = word.value
        if bounded_dynamic_output_target(
            target,
            safe_variables,
            allowed_github_targets=frozenset(
                {"$GITHUB_ENV", "$GITHUB_OUTPUT", "$GITHUB_STEP_SUMMARY"}
            ),
        ):
            continue
        return "dynamic output redirection target is unsupported"
    return None


def tee_destination_error(run: str) -> str | None:
    """Restrict ``tee`` targets before its data stream can reach GitHub files.

    ``tee`` is data-only for executable selection, but it is a file writer.
    Its target must consequently use the same bounded path policy as shell
    output redirections.  A direct step-summary target is the sole GitHub
    special file used by the checked-in workflows.
    """

    safe_variables = simple_redirect_path_variables(run)
    for command in analyze_shell_source(run).commands:
        if static_command_basename(command.command) != "tee":
            continue
        parsing_options = True
        for argument in command.arguments:
            if parsing_options and not argument.dynamic and argument.value == "--":
                parsing_options = False
                continue
            if parsing_options and not argument.dynamic and argument.value.startswith("-"):
                continue
            parsing_options = False
            if not argument.dynamic:
                continue
            if bounded_dynamic_output_target(
                argument.value,
                safe_variables,
                allowed_github_targets=frozenset({"$GITHUB_STEP_SUMMARY"}),
            ):
                continue
            return "dynamic tee destination is unsupported"
    return None


def direct_python_or_pip_command(run: str) -> str | None:
    for shell_command in analyze_shell_source(run).commands:
        command = static_command_basename(shell_command.command)
        if command is not None and is_python_or_pip_command(command):
            return command
    return None


def executable_words(command: ShellCommand) -> tuple[ShellWord, ...]:
    """Return words that can be executable positions for one shell command."""

    basename = static_command_basename(command.command)
    if (
        basename in NON_EXECUTING_ARGUMENT_COMMANDS
        or (basename is not None and is_python_or_pip_command(basename))
    ):
        return (command.command,)
    return (command.command, *command.arguments)


def python_interpreter_token(run: str) -> str | None:
    """Return a literal interpreter token found anywhere in shell syntax.

    Shell launchers are intentionally not enumerated here.  Any command can
    choose to execute a following argument (for example ``nohup``, ``flock``,
    ``find -exec``, or a future tool), so a static Python/pip executable token
    is inventoried in every potential execution position outside comments,
    here-doc bodies, redirection targets, and arguments of commands proven to
    be data-only.  Dynamic executable construction remains a scanner error
    and is handled by :func:`shell_syntax_error`.
    """

    for shell_command in analyze_shell_source(run).commands:
        for word in executable_words(shell_command):
            if word.redirection_target:
                continue
            command = static_command_basename(word)
            if command is not None and is_python_or_pip_command(command):
                return command
    return None


def bare_pip_command(run: str) -> str | None:
    for shell_command in analyze_shell_source(run).commands:
        for word in executable_words(shell_command):
            if word.redirection_target:
                continue
            command = static_command_basename(word)
            if command is not None and is_bare_pip_command(command):
                return command
    return None


def python_shell_use(step: Step) -> str | None:
    """Classify an explicit or inherited step shell without executing it."""

    shell = step.scalar("shell") or step.default_shell
    if shell is None:
        return None
    if "$" in shell or "`" in shell:
        return "dynamic shell selector"
    normalized = shell.strip()
    executable = normalized.split(maxsplit=1)[0] if normalized else ""
    if is_python_or_pip_command(executable):
        return "Python shell"
    if normalized in {"bash", "sh"}:
        return None
    if normalized in NON_POSIX_WORKFLOW_SHELLS:
        return "non-POSIX shell selector"
    return "custom shell selector"


def workflow_shell_selector_error(step: Step) -> str | None:
    """Allow only the reviewed default/Bash shell in monitored Python jobs."""

    shell = step.scalar("shell") or step.default_shell
    if shell is None:
        return None
    if "$" in shell or "`" in shell:
        return "dynamic workflow shell selector is unsupported"
    if shell.strip() == "bash":
        return None
    return f"unsupported workflow shell selector {shell.strip()!r}"


def python_make_target(run: str) -> str | None:
    for shell_command in analyze_shell_source(run).commands:
        command = static_command_basename(shell_command.command)
        if command != "make":
            continue
        for argument in shell_command.arguments:
            if not argument.dynamic and argument.value in KNOWN_PYTHON_MAKE_TARGETS:
                return argument.value
    return None


LOCAL_SHELL_FUNCTION = re.compile(
    r"(?m)^\s*(?:function\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*\(\)"
)


def dynamic_executable_position_error(run: str) -> str | None:
    """Reject dynamic words at every potential executable position.

    A launcher has no bounded universal grammar: ``nohup p${X}ython3`` and
    ``nohup "$PYTHON"`` can both execute an interpreter without containing a
    static ``python`` token.  Arguments of commands proven to be data-only,
    and arguments after a direct Python/pip executable, are the only narrow
    exceptions.  This avoids a bypassable launcher allowlist while retaining
    ordinary ``echo``/``printf`` data handling.
    """

    local_functions = frozenset(LOCAL_SHELL_FUNCTION.findall(run))
    for command in analyze_shell_source(run).commands:
        command_name = static_command_basename(command.command)
        if not command_name:
            # The bounded POSIX scanner can retain an empty placeholder around
            # a multiline pipeline continuation; it is not an executable
            # position, and the adjacent command is scanned independently.
            continue
        if (
            command_name in DYNAMIC_ARGUMENT_SAFE_COMMANDS
            or command_name in local_functions
            or (
                command_name is not None
                and is_python_or_pip_command(command_name)
            )
        ):
            words = (command.command,)
        else:
            words = executable_words(command)
        for word in words:
            if word.redirection_target or not word.dynamic:
                continue
            basename = static_command_basename(word)
            if basename is not None and not is_python_or_pip_command(basename):
                # A dynamic directory prefix paired with a fixed non-Python
                # tool name (for example "$RUNNER_TEMP/.../gitleaks") cannot
                # construct a Python executable.  The tool's own integrity
                # contract is checked separately.
                continue
            return "dynamic potential executable position is unsupported"
    return None


def shell_path_reset_error(run: str) -> str | None:
    """Reject wrappers that replace setup-python's PATH search order."""

    for command in analyze_shell_source(run).commands:
        prefix = command.prefix
        if not prefix:
            continue
        wrapper = static_command_basename(prefix[0])
        values = [word.value for word in prefix]
        if wrapper == "command" and "-p" in values[1:]:
            return "command -p replaces the setup-python PATH"
        if wrapper != "env":
            continue
        for index, value in enumerate(values[1:], start=1):
            if value in {"-i", "--ignore-environment"}:
                return "env -i replaces the setup-python PATH"
            if value in {"-u", "--unset"}:
                if index + 1 < len(values) and values[index + 1] == "PATH":
                    return "env unsets the setup-python PATH"
            if value in {"-uPATH", "--unset=PATH"}:
                return "env unsets the setup-python PATH"
    return None


def shell_syntax_error(run: str) -> str | None:
    analysis = analyze_shell_source(run)
    if analysis.errors:
        return analysis.errors[0]
    path_reset = shell_path_reset_error(run)
    if path_reset is not None:
        return path_reset
    tee_error = tee_destination_error(run)
    if tee_error is not None:
        return tee_error
    return dynamic_executable_position_error(run)


def actual_python_use(step: Step) -> str | None:
    shell_use = python_shell_use(step)
    if shell_use is not None:
        return shell_use
    run = step.run()
    without_verifier = run_without_verifier_command(run)
    if direct_python_or_pip_command(without_verifier) is not None:
        return "direct python/pip command"
    if python_interpreter_token(without_verifier) is not None:
        return "literal python/pip interpreter token"
    target = python_make_target(without_verifier)
    if target is not None:
        return f"Make target {target}"
    return None


def step_environment_values(step: Step) -> tuple[dict[str, str], str | None]:
    """Return one step's scalar environment mapping or a fail-closed error."""

    if step.node is None:
        return step.nested_mapping("env"), None
    try:
        return (
            scalar_environment_values(
                step.semantic_fields(),
                context=f"workflow step at line {step.start_line}",
            ),
            None,
        )
    except ContractInputError as error:
        return {}, str(error)


def path_mutation_in_run(run: str) -> str | None:
    """Return interpreter-selection environment mutations in shell source.

    This deliberately scans the original source in addition to lexical shell
    words: a GitHub environment file persists state for later steps, and its
    pathname or assignment key must not be assembled dynamically.
    """

    if "${!" in run:
        return "indirect shell expansion"
    github_env_error = github_env_write_error(run)
    if github_env_error is not None:
        return github_env_error
    dynamic_target_error = dynamic_output_redirection_error(run)
    if dynamic_target_error is not None:
        return dynamic_target_error
    if "GITHUB_PATH" in run:
        return "GITHUB_PATH mutation"
    if UNSAFE_INTERPRETER_ENV_ASSIGNMENT.search(run):
        return "inline interpreter-selection environment assignment"
    return None


def python_words_by_command(run: str) -> tuple[ShellAnalysis, list[tuple[int, ShellWord]]]:
    """Return recognized Python/pip executable words with command ordering."""

    analysis = analyze_shell_source(run)
    words: list[tuple[int, ShellWord]] = []
    for command_index, command in enumerate(analysis.commands):
        for word in executable_words(command):
            if word.redirection_target:
                continue
            basename = static_command_basename(word)
            if basename is not None and is_python_or_pip_command(basename):
                words.append((command_index, word))
    return analysis, words


def validate_python_execution_sources(job: Job, steps: Iterable[Step]) -> list[str]:
    """Bind Python execution to setup-python's unmodified PATH.

    Bare ``python``/``python3`` names remain valid after the verified setup only
    when no workflow, job, step, or inline PATH mutation can replace the
    action-provided executable.  Absolute and alternate executable paths are
    rejected; the checked-in full-smoke workflow uses the verified ``python3``
    name instead of a local virtual-environment path.
    """

    errors: list[str] = []
    inherited_unsafe = sorted(
        UNSAFE_INTERPRETER_ENV_KEYS.intersection(job.inherited_environment)
    )
    if inherited_unsafe:
        errors.append(
            f"{job.identity.display()} must not set interpreter-selection env key(s) "
            f"{', '.join(inherited_unsafe)} via workflow/job env"
        )
    for step in steps:
        environment, environment_error = step_environment_values(step)
        if environment_error is not None:
            errors.append(f"{job.identity.display()} {environment_error}")
        else:
            unsafe_keys = sorted(
                UNSAFE_INTERPRETER_ENV_KEYS.intersection(environment)
            )
            if unsafe_keys:
                errors.append(
                    f"{job.identity.display()} step at workflow line {step.start_line} "
                    "must not set interpreter-selection env key(s) "
                    f"{', '.join(unsafe_keys)} via env"
                )

        run = step.run()
        mutation = path_mutation_in_run(run)
        if mutation is not None:
            errors.append(
                f"{job.identity.display()} step at workflow line {step.start_line} "
                f"must not perform {mutation}"
            )

        _, python_words = python_words_by_command(run)
        for _, word in python_words:
            executable = word.value
            basename = static_command_basename(word)
            if basename is None:
                continue
            if is_bare_pip_command(basename):
                continue
            if executable in {"python", "python3"}:
                continue
            errors.append(
                f"{job.identity.display()} step at workflow line {step.start_line} "
                "must invoke only unqualified 'python' or 'python3' from "
                f"setup-python, not {executable!r}"
            )
    return errors


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

    if job.node is not None:
        if any("matrix" in line.lower() for line in selector_lines(job)):
            return True
        visited: set[int] = set()

        def visit(node: Node, *, in_matrix: bool = False) -> bool:
            identity = id(node)
            if identity in visited:
                return False
            visited.add(identity)
            if isinstance(node, ScalarNode):
                return bool(PYTHON_MATRIX_REFERENCE.search(node.value))
            if isinstance(node, SequenceNode):
                return any(visit(value, in_matrix=in_matrix) for value in node.value)
            if not isinstance(node, MappingNode):
                return False
            for key, value in semantic_mapping_items(
                node, context=f"workflow job {job.identity.display()}"
            ).items():
                if in_matrix and PYTHON_MATRIX_KEY.fullmatch(f"{key}:"):
                    return True
                if visit(value, in_matrix=in_matrix or key == "matrix"):
                    return True
            return False

        return visit(job.node)

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
    expected_reference = active_setup_python_reference()
    expected_action = active_setup_python_action()
    setup_like = [
        step
        for step in steps
        if (uses := step.scalar("uses")) is not None
        and uses.startswith("actions/setup-python@")
    ]
    matching = [
        step for step in setup_like if step.raw_scalar("uses") == expected_reference
    ]
    errors: list[str] = []
    if len(setup_like) != 1 or len(matching) != 1:
        if setup_like:
            errors.append(
                "actions/setup-python must use exactly "
                f"one {expected_reference} step; found {len(setup_like)} "
                f"setup-python step(s) and {len(matching)} exact reference(s)"
            )
        else:
            errors.append(
                "must contain exactly one "
                f"{expected_action} setup step; found {len(matching)}"
            )
        return None, errors
    setup = matching[0]
    if setup.scalar("id") != "setup-python":
        errors.append("pinned actions/setup-python step must have id: setup-python")
    return setup, errors


def selector_lines(job: Job) -> list[str]:
    if job.node is not None:
        lines: list[str] = []
        visited: set[int] = set()

        def visit(node: Node) -> None:
            identity = id(node)
            if identity in visited:
                return
            visited.add(identity)
            if isinstance(node, MappingNode):
                for key, value in semantic_mapping_items(
                    node, context=f"workflow job {job.identity.display()}"
                ).items():
                    if key == "python-version":
                        scalar = value.value if isinstance(value, ScalarNode) else ""
                        lines.append(f"{key}: {scalar}")
                    visit(value)
            elif isinstance(node, SequenceNode):
                for value in node.value:
                    visit(value)

        visit(job.node)
        return lines
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


def validate_working_directories(identity: JobIdentity, steps: Iterable[Step]) -> list[str]:
    """Keep relative verifier scripts rooted at the checked-out repository."""

    return [
        f"{identity.display()} must not set a step working-directory"
        for step in steps
        if step.scalar("working-directory") is not None
    ]


def validate_shell_syntax(identity: JobIdentity, steps: Iterable[Step]) -> list[str]:
    """Reject unsupported shell forms instead of silently missing Python use."""

    errors: list[str] = []
    for step in steps:
        selector_error = workflow_shell_selector_error(step)
        if selector_error is not None:
            errors.append(
                f"{identity.display()} step at workflow line {step.start_line} "
                f"contains unsupported shell selector: {selector_error}"
            )
        error = shell_syntax_error(run_without_verifier_command(step.run()))
        if error is not None:
            errors.append(
                f"{identity.display()} step at workflow line {step.start_line} "
                f"contains unsupported/malformed shell syntax: {error}"
            )
    return errors


def normal_setup_violations(job: Job, setup: Step) -> list[str]:
    """Return normal-job setup selector violations in their contract order."""

    errors: list[str] = []
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
    return errors


def normal_verifier_violations(verifier: Step) -> list[str]:
    """Return normal-job verifier-shape violations in contract order."""

    errors: list[str] = []
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
    return errors


def finalize_job_validation(
    job: Job, steps: Sequence[Step], errors: list[str]
) -> list[str]:
    """Prefix structural errors before adding source-level shell violations."""

    identity = job.identity
    prefixed = [f"{identity.display()}: {error}" for error in errors]
    return (
        prefixed
        + validate_no_bare_pip(identity, steps)
        + validate_working_directories(identity, steps)
        + validate_shell_syntax(identity, steps)
        + validate_python_execution_sources(job, steps)
    )


def validate_normal_job(job: Job) -> list[str]:
    steps = job.steps()
    setup, errors = pinned_setup_step(steps)
    if setup is not None:
        errors.extend(normal_setup_violations(job, setup))

    verifier = verifier_step(steps)
    if verifier is not None:
        errors.extend(normal_verifier_violations(verifier))
    errors.extend(validate_order(job.identity, steps, setup, verifier))
    return finalize_job_validation(job, steps, errors)


def candidate_setup_violations(job: Job, setup: Step) -> list[str]:
    """Return candidate-job setup selector violations in contract order."""

    errors: list[str] = []
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
    return errors


def candidate_verifier_violations(verifier: Step) -> list[str]:
    """Return candidate verifier-shape violations in contract order."""

    errors: list[str] = []
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
    return errors


def validate_candidate_job(job: Job) -> list[str]:
    """Validate the one explicit candidate-patch exception without widening it."""

    steps = job.steps()
    setup, errors = pinned_setup_step(steps)
    if setup is not None:
        errors.extend(candidate_setup_violations(job, setup))

    verifier = verifier_step(steps, CANDIDATE_VERIFIER_NAME)
    if verifier is not None:
        errors.extend(candidate_verifier_violations(verifier))
    errors.extend(
        validate_order(
            job.identity,
            steps,
            setup,
            verifier,
            CANDIDATE_VERIFIER_NAME,
        )
    )
    return finalize_job_validation(job, steps, errors)


def downgrade_violations(
    canonical_version: str, previous_version: str | None, allow_downgrade: bool
) -> list[str]:
    """Return the explicit-authorization error for a version downgrade."""

    if previous_version is None:
        return []
    previous = parse_exact_version(previous_version, "--previous-version")
    if version_tuple(canonical_version) >= version_tuple(previous) or allow_downgrade:
        return []
    return [
        f"canonical Python version {canonical_version} is a downgrade from {previous}; "
        "pass --allow-downgrade only with explicit authorization"
    ]


def collect_workflow_jobs(root: Path) -> tuple[dict[JobIdentity, Job], list[str]]:
    """Collect workflow jobs and retain source-file diagnostics in path order."""

    paths, violations = workflow_files(root)
    jobs: dict[JobIdentity, Job] = {}
    for path in paths:
        parsed, parse_violations = parse_jobs(path)
        jobs.update(parsed)
        violations.extend(parse_violations)
    return jobs, violations


def missing_inventory_violations(
    jobs: dict[JobIdentity, Job],
    expected: frozenset[JobIdentity],
    expected_candidate_job: JobIdentity | None,
) -> list[str]:
    """Return required inventory entries that are absent from the workflows."""

    violations = [
        f"expected normal Python job is absent: {identity.display()}"
        for identity in sorted(expected)
        if identity not in jobs
    ]
    if expected_candidate_job is not None and expected_candidate_job not in jobs:
        violations.append(
            f"expected candidate-validation job is absent: {expected_candidate_job.display()}"
        )
    return violations


def detected_python_jobs(jobs: dict[JobIdentity, Job]) -> set[JobIdentity]:
    """Return the inventory of every job that can select or execute Python."""

    return {
        identity for identity, job in jobs.items() if python_job_reason(job) is not None
    }


def expected_normal_job_violations(
    jobs: dict[JobIdentity, Job],
    expected: frozenset[JobIdentity],
    detected: set[JobIdentity],
) -> list[str]:
    """Validate each expected normal job in stable inventory order."""

    violations: list[str] = []
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
    return violations


def candidate_job_violations(
    jobs: dict[JobIdentity, Job],
    candidate_identity: JobIdentity | None,
    detected: set[JobIdentity],
) -> list[str]:
    """Validate the one candidate exception when it is configured and present."""

    if candidate_identity is None:
        return []
    candidate = jobs.get(candidate_identity)
    if candidate is None:
        return []
    violations: list[str] = []
    if candidate_identity not in detected:
        violations.append(
            "candidate-validation job has no detected Python use, known Make use, "
            "reusable invocation, or Python-related matrix selector: "
            f"{candidate_identity.display()}"
        )
    violations.extend(validate_candidate_job(candidate))
    return violations


def unlisted_python_job_violations(
    jobs: dict[JobIdentity, Job],
    expected: frozenset[JobIdentity],
    expected_candidate_job: JobIdentity | None,
    detected: set[JobIdentity],
) -> list[str]:
    """Reject detected Python jobs absent from the explicit inventory."""

    violations: list[str] = []
    for identity in sorted(detected):
        if identity in expected or identity == expected_candidate_job:
            continue
        violations.append(
            f"unlisted Python-related workflow job: {identity.display()} "
            f"({python_job_reason(jobs[identity])})"
        )
        violations.extend(validate_normal_job(jobs[identity]))
    return violations


def evaluate_workflow_contract(
    root: Path,
    version_file: Path,
    previous_version: str | None = None,
    allow_downgrade: bool = False,
    expected_normal_jobs: Iterable[JobIdentity] = EXPECTED_NORMAL_PYTHON_JOBS,
    expected_candidate_job: JobIdentity | None = CANDIDATE_VALIDATION_JOB,
    require_setup_lock: bool = False,
) -> tuple[str, list[str], set[JobIdentity]]:
    """Evaluate source-only workflow policy and return version, violations, inventory."""

    global _ACTIVE_SETUP_PYTHON_REFERENCE
    previous_reference = _ACTIVE_SETUP_PYTHON_REFERENCE
    _ACTIVE_SETUP_PYTHON_REFERENCE = setup_python_reference_from_lock(
        root, require_lock=require_setup_lock
    )
    try:
        canonical_version = read_canonical_version(version_file)
        violations = downgrade_violations(
            canonical_version, previous_version, allow_downgrade
        )
        jobs, workflow_violations = collect_workflow_jobs(root)
        violations.extend(workflow_violations)

        expected = frozenset(expected_normal_jobs)
        violations.extend(
            missing_inventory_violations(jobs, expected, expected_candidate_job)
        )
        detected = detected_python_jobs(jobs)
        violations.extend(expected_normal_job_violations(jobs, expected, detected))
        violations.extend(candidate_job_violations(jobs, expected_candidate_job, detected))
        violations.extend(
            unlisted_python_job_violations(
                jobs, expected, expected_candidate_job, detected
            )
        )
        return canonical_version, violations, detected
    finally:
        _ACTIVE_SETUP_PYTHON_REFERENCE = previous_reference


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
            require_setup_lock=True,
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
