"""Focused static contracts for the repository's CI-security workflows."""

from __future__ import annotations

import os
import re
import subprocess
import tempfile
import textwrap
import unittest
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

import yaml
from yaml.nodes import MappingNode, Node, ScalarNode, SequenceNode


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
WORKFLOW_PATTERNS = ("*.yml", "*.yaml")
PERMISSION_FIXTURES = ROOT / "ci" / "fixtures" / "workflow-permission-contract"
SHA_PIN = re.compile(r"^[a-z\d_.-]+(?:/[a-z\d_.-]+)+@[a-f\d]{40}\s+# v\d", re.MULTILINE)
CANONICAL_USES_KEY = re.compile(r"^\s*(?:-\s*)?uses:\s*", re.ASCII)
SECRET_CONTEXT = re.compile(r"(?<![A-Za-z0-9_-])secrets(?![A-Za-z0-9_-])", re.IGNORECASE)
TOKEN_CONTEXT = re.compile(
    r"(?<![A-Za-z0-9_-])(?:github\s*\.\s*token|(?:GH|GITHUB)_TOKEN)(?![A-Za-z0-9_-])",
    re.IGNORECASE,
)

WRITE_PERMISSION_KEYS = {
    "contents",
    "actions",
    "checks",
    "security-events",
    "pull-requests",
    "issues",
    "packages",
    "id-token",
    "attestations",
}

EXPECTED_WRITE_PERMISSIONS = {
    ("cleanup-artifacts.yml", "cleanup-artifacts"): {"actions": "write"},
    ("test-full-smoke-sequential.yml", "cleanup-artifacts"): {"actions": "write"},
    ("update-actions-versions.yml", "create-ci-tool-update-pr"): {
        "contents": "write",
        "pull-requests": "write",
    },
    ("update-submodules.yml", "create-submodule-update-pr"): {
        "contents": "write",
        "pull-requests": "write",
    },
    ("update-python-version.yml", "create-python-update-pr"): {
        "contents": "write",
        "pull-requests": "write",
    },
    ("update-go-version.yml", "create-go-update-pr"): {
        "contents": "write",
        "pull-requests": "write",
    },
    ("ci-security-codeql.yml", "actions"): {
        "contents": "read",
        "security-events": "write",
    },
    ("ci-security-codeql.yml", "envoy-go"): {
        "contents": "read",
        "security-events": "write",
    },
    ("ci-security-codeql.yml", "traefik-go"): {
        "contents": "read",
        "security-events": "write",
    },
    ("ci-security-codeql.yml", "bounded-c-cpp"): {
        "contents": "read",
        "security-events": "write",
    },
    ("ci-security-osv.yml", "pull-request-diff"): {
        "contents": "read",
        "security-events": "write",
    },
    ("ci-security-scorecard.yml", "default-branch"): {
        "contents": "read",
        "security-events": "write",
    },
}


def workflow_mapping(text: str, *, context: str) -> MappingNode:
    """Parse a workflow structurally, never by a key-shaped text regex.

    YAML permits quoted and escaped keys.  The permission contract must see
    precisely the same job identifiers and permission mappings that the
    workflow parser sees, or a quoted writer job could escape the audit.
    """

    try:
        document = yaml.compose(text, Loader=yaml.BaseLoader)
    except (RecursionError, yaml.YAMLError) as error:
        raise AssertionError(f"{context} is not valid YAML") from error
    if not isinstance(document, MappingNode):
        raise AssertionError(f"{context} is not a YAML mapping")
    return document


def mapping_items(node: MappingNode, *, context: str) -> dict[str, Node]:
    """Return one simple mapping, rejecting duplicate and merge-based keys."""

    values: dict[str, Node] = {}
    for key, value in node.value:
        if not isinstance(key, ScalarNode):
            raise AssertionError(f"{context} has a non-scalar mapping key")
        if key.value == "<<":
            raise AssertionError(f"{context} uses an unsupported YAML merge key")
        if key.value in values:
            raise AssertionError(f"{context} has a duplicate mapping key {key.value!r}")
        values[key.value] = value
    return values


def permissions_mapping(node: Node, *, context: str) -> dict[str, str]:
    """Decode GitHub permission syntax and fail closed for unsupported forms."""

    if isinstance(node, MappingNode):
        permissions: dict[str, str] = {}
        for key, value in mapping_items(node, context=context).items():
            if not isinstance(value, ScalarNode):
                raise AssertionError(f"{context}.{key} is not a scalar permission value")
            permissions[key] = value.value
        return permissions
    if isinstance(node, ScalarNode):
        if node.value == "read-all":
            return {"*": "read"}
        if node.value == "write-all":
            return {"*": "write"}
    raise AssertionError(f"{context} uses an unsupported permission form")


def scalar_mapping(node: Node, *, context: str) -> dict[str, str]:
    """Decode one simple scalar mapping and reject every non-scalar field."""

    if not isinstance(node, MappingNode):
        raise AssertionError(f"{context} is not a mapping")
    result: dict[str, str] = {}
    for key, value in mapping_items(node, context=context).items():
        if not isinstance(value, ScalarNode):
            raise AssertionError(f"{context}.{key} is not a scalar")
        result[key] = value.value
    return result


def top_level_permissions(text: str) -> dict[str, str]:
    document = workflow_mapping(text, context="workflow")
    permissions = mapping_items(document, context="workflow").get("permissions")
    if permissions is None:
        raise AssertionError("workflow has no top-level permissions mapping")
    return permissions_mapping(permissions, context="workflow.permissions")


def workflow_triggers(text: str) -> set[str]:
    """Return decoded GitHub trigger names without accepting YAML indirection."""

    document = workflow_mapping(text, context="workflow")
    trigger_node = mapping_items(document, context="workflow").get("on")
    if trigger_node is None:
        raise AssertionError("workflow has no trigger mapping")
    if isinstance(trigger_node, ScalarNode):
        if not trigger_node.value:
            raise AssertionError("workflow has an empty trigger")
        return {trigger_node.value}
    if isinstance(trigger_node, SequenceNode):
        triggers: set[str] = set()
        for index, item in enumerate(trigger_node.value):
            if not isinstance(item, ScalarNode) or not item.value:
                raise AssertionError(f"workflow.on[{index}] is not a non-empty scalar trigger")
            if item.value in triggers:
                raise AssertionError(f"workflow has duplicate trigger {item.value!r}")
            triggers.add(item.value)
        return triggers
    if isinstance(trigger_node, MappingNode):
        return set(mapping_items(trigger_node, context="workflow.on"))
    raise AssertionError("workflow uses an unsupported trigger form")


def job_blocks(text: str) -> dict[str, str]:
    """Return semantic job IDs paired with their source blocks.

    The raw source is retained for focused shell and checkout assertions, but
    the job inventory comes from PyYAML's decoded node tree so quoted IDs
    cannot be skipped.
    """

    document = workflow_mapping(text, context="workflow")
    jobs = mapping_items(document, context="workflow").get("jobs")
    if not isinstance(jobs, MappingNode):
        raise AssertionError("workflow has no jobs mapping")
    blocks: dict[str, str] = {}
    for key, value in jobs.value:
        if not isinstance(key, ScalarNode):
            raise AssertionError("workflow.jobs has a non-scalar job identifier")
        if key.value == "<<":
            raise AssertionError("workflow.jobs uses an unsupported YAML merge key")
        if not re.fullmatch(r"[A-Za-z0-9_-]+", key.value, re.ASCII):
            raise AssertionError(f"workflow.jobs has an invalid job identifier {key.value!r}")
        if not isinstance(value, MappingNode):
            raise AssertionError(f"workflow.jobs.{key.value} is not a mapping")
        if key.value in blocks:
            raise AssertionError(f"workflow.jobs has duplicate identifier {key.value!r}")
        blocks[key.value] = text[key.start_mark.index : value.end_mark.index]
    return blocks


def job_fields(job: str) -> tuple[str, dict[str, Node]]:
    """Return one semantic job's decoded top-level fields."""

    document = workflow_mapping(job, context="workflow job")
    items = mapping_items(document, context="workflow job")
    if len(items) != 1:
        raise AssertionError("workflow job source does not contain exactly one job")
    job_name, job_node = next(iter(items.items()))
    if not isinstance(job_node, MappingNode):
        raise AssertionError(f"workflow job {job_name!r} is not a mapping")
    return job_name, mapping_items(job_node, context=f"workflow job {job_name}")


def job_scalar_field(job: str, field: str) -> str:
    """Require one decoded scalar job field without comment-based spoofing."""

    job_name, fields = job_fields(job)
    value = fields.get(field)
    if not isinstance(value, ScalarNode):
        raise AssertionError(f"workflow job {job_name}.{field} is not a scalar")
    return value.value


def job_environment(job: str) -> dict[str, str]:
    """Return one job's decoded environment mapping, if it has one."""

    job_name, fields = job_fields(job)
    environment = fields.get("env")
    return {} if environment is None else scalar_mapping(environment, context=f"workflow job {job_name}.env")


def workflow_environment(text: str) -> dict[str, str]:
    """Return the decoded workflow-wide environment mapping, if present."""

    document = workflow_mapping(text, context="workflow")
    environment = mapping_items(document, context="workflow").get("env")
    return {} if environment is None else scalar_mapping(environment, context="workflow.env")


def job_permissions(job: str) -> dict[str, str]:
    job_name, fields = job_fields(job)
    permissions = fields.get("permissions")
    if permissions is None:
        return {}
    return permissions_mapping(permissions, context=f"workflow job {job_name}.permissions")


@dataclass(frozen=True)
class CheckoutStep:
    """One decoded checkout step and its exact decoded with fields."""

    raw: str
    with_values: dict[str, str]


def checkout_steps(text: str) -> list[CheckoutStep]:
    """Find semantic checkout steps, including quoted or escaped YAML keys."""

    document = workflow_mapping(text, context="workflow")
    steps: list[CheckoutStep] = []
    visited: set[int] = set()

    def visit(node: Node, *, context: str) -> None:
        identity = id(node)
        if identity in visited:
            return
        visited.add(identity)
        if isinstance(node, MappingNode):
            values = mapping_items(node, context=context)
            uses = values.get("uses")
            if isinstance(uses, ScalarNode) and uses.value.startswith("actions/checkout@"):
                with_node = values.get("with")
                if with_node is None:
                    with_values: dict[str, str] = {}
                elif isinstance(with_node, MappingNode):
                    with_values = {}
                    for key, value in mapping_items(with_node, context=f"{context}.with").items():
                        if not isinstance(value, ScalarNode):
                            raise AssertionError(f"{context}.with.{key} is not a scalar")
                        with_values[key] = value.value
                else:
                    raise AssertionError(f"{context}.with is not a mapping")
                steps.append(
                    CheckoutStep(
                        raw=text[node.start_mark.index : node.end_mark.index],
                        with_values=with_values,
                    )
                )
            for child in values.values():
                visit(child, context=f"{context}.value")
            return
        if isinstance(node, SequenceNode):
            for index, child in enumerate(node.value):
                visit(child, context=f"{context}[{index}]")
            return
        if not isinstance(node, ScalarNode):
            raise AssertionError(f"{context} has an unsupported YAML node")

    visit(document, context="workflow")
    return steps


def checkout_step_blocks(text: str) -> list[str]:
    """Return raw checkout blocks found by the structural checkout parser."""

    return [step.raw for step in checkout_steps(text)]


def action_step_with_values(text: str, *, action_prefix: str) -> list[dict[str, str]]:
    """Return decoded ``with`` mappings for one pinned action family.

    This deliberately traverses parsed YAML instead of looking for raw
    ``uses`` or ``go-version`` text. Quoted, escaped, or flow-style YAML keys
    therefore cannot make a CodeQL setup-go field invisible to the contract.
    """

    document = workflow_mapping(text, context="workflow")
    steps: list[dict[str, str]] = []
    visited: set[int] = set()

    def visit(node: Node, *, context: str) -> None:
        identity = id(node)
        if identity in visited:
            return
        visited.add(identity)
        if isinstance(node, MappingNode):
            values = mapping_items(node, context=context)
            uses = values.get("uses")
            if isinstance(uses, ScalarNode) and uses.value.startswith(action_prefix):
                with_node = values.get("with")
                if with_node is None:
                    raise AssertionError(f"{context}.{action_prefix} has no with mapping")
                steps.append(scalar_mapping(with_node, context=f"{context}.with"))
            for child in values.values():
                visit(child, context=f"{context}.value")
            return
        if isinstance(node, SequenceNode):
            for index, child in enumerate(node.value):
                visit(child, context=f"{context}[{index}]")
            return
        if not isinstance(node, ScalarNode):
            raise AssertionError(f"{context} has an unsupported YAML node")

    visit(document, context="workflow")
    return steps


def step_environment_mappings(job: str) -> list[dict[str, str]]:
    """Return every direct step-level environment mapping in source order."""

    job_name, fields = job_fields(job)
    steps = fields.get("steps")
    if steps is None:
        return []
    if not isinstance(steps, SequenceNode):
        raise AssertionError(f"workflow job {job_name}.steps is not a sequence")
    environments: list[dict[str, str]] = []
    for index, step in enumerate(steps.value):
        if not isinstance(step, MappingNode):
            raise AssertionError(f"workflow job {job_name}.steps[{index}] is not a mapping")
        environment = mapping_items(
            step,
            context=f"workflow job {job_name}.steps[{index}]",
        ).get("env")
        if environment is not None:
            environments.append(
                scalar_mapping(
                    environment,
                    context=f"workflow job {job_name}.steps[{index}].env",
                )
            )
    return environments


def scalar_values(text: str) -> list[str]:
    """Return decoded YAML scalar values while rejecting ambiguous mappings."""

    document = workflow_mapping(text, context="workflow")
    values: list[str] = []
    visited: set[int] = set()

    def visit(node: Node, *, context: str) -> None:
        identity = id(node)
        if identity in visited:
            return
        visited.add(identity)
        if isinstance(node, MappingNode):
            for child in mapping_items(node, context=context).values():
                visit(child, context=f"{context}.value")
            return
        if isinstance(node, SequenceNode):
            for index, child in enumerate(node.value):
                visit(child, context=f"{context}[{index}]")
            return
        if isinstance(node, ScalarNode):
            values.append(node.value)
            return
        raise AssertionError(f"{context} has an unsupported YAML node")

    visit(document, context="workflow")
    return values


def workflow_secret_references(text: str) -> list[str]:
    """Find decoded GitHub secrets-context uses, including bracket access."""

    return [value for value in scalar_values(text) if SECRET_CONTEXT.search(value)]


def workflow_token_references(text: str) -> list[str]:
    """Find decoded token contexts and token-shaped environment keys."""

    document = workflow_mapping(text, context="workflow")
    references: list[str] = []
    visited: set[int] = set()

    def visit(node: Node, *, context: str) -> None:
        identity = id(node)
        if identity in visited:
            return
        visited.add(identity)
        if isinstance(node, MappingNode):
            for key, value in node.value:
                if not isinstance(key, ScalarNode):
                    raise AssertionError(f"{context} has a non-scalar mapping key")
                if TOKEN_CONTEXT.search(key.value):
                    references.append(key.value)
                visit(value, context=f"{context}.{key.value}")
            return
        if isinstance(node, SequenceNode):
            for index, child in enumerate(node.value):
                visit(child, context=f"{context}[{index}]")
            return
        if isinstance(node, ScalarNode):
            if TOKEN_CONTEXT.search(node.value):
                references.append(node.value)
            return
        raise AssertionError(f"{context} has an unsupported YAML node")

    visit(document, context="workflow")
    return references


def workflow_run_scalars(text: str) -> list[str]:
    """Return decoded run scalar bodies for the privileged-execution model."""

    document = workflow_mapping(text, context="workflow")
    runs: list[str] = []
    visited: set[int] = set()

    def visit(node: Node, *, context: str) -> None:
        identity = id(node)
        if identity in visited:
            return
        visited.add(identity)
        if isinstance(node, MappingNode):
            values = mapping_items(node, context=context)
            run = values.get("run")
            if isinstance(run, ScalarNode):
                runs.append(run.value)
            for child in values.values():
                visit(child, context=f"{context}.value")
            return
        if isinstance(node, SequenceNode):
            for index, child in enumerate(node.value):
                visit(child, context=f"{context}[{index}]")
            return
        if not isinstance(node, ScalarNode):
            raise AssertionError(f"{context} has an unsupported YAML node")

    visit(document, context="workflow")
    return runs


def assert_updater_job_boundary(
    job: str,
    *,
    expected_if: str,
    expected_checkout_with: dict[str, str],
) -> None:
    """Require the exact trusted-ref gate and checkout contract for one job."""

    if job_scalar_field(job, "if") != expected_if:
        raise AssertionError("updater job does not use its exact trusted default-branch gate")
    checkouts = checkout_steps(job)
    if len(checkouts) != 1:
        raise AssertionError("updater job must contain exactly one checkout")
    if checkouts[0].with_values != expected_checkout_with:
        raise AssertionError(f"updater checkout has unexpected fields: {checkouts[0].with_values!r}")


def _active_shell_lines(script: str) -> list[str]:
    """Return non-comment shell lines for strict, narrow publisher command checks."""

    return [
        line.strip()
        for line in script.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def publisher_script_digest(job: str) -> str:
    """Provide a stable, deliberate profile boundary for publisher shell code."""

    payload = "\0".join(workflow_run_scalars(job)).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _profile_node(node: Node, *, mapping_key: str | None = None) -> object:
    """Return a canonical semantic publisher profile for one YAML node.

    CI-tool self-updates legitimately rotate immutable ``uses`` SHAs in their
    own publisher job.  Preserve the action identity but redact only the
    40-hex suffix; every other job/step field remains profile-bound.  The
    independent action-lock tests continue to enforce the exact SHA and its
    release comment.
    """

    if isinstance(node, MappingNode):
        entries: list[tuple[object, object]] = []
        for key, value in node.value:
            decoded_key = key.value if isinstance(key, ScalarNode) else None
            entries.append(
                (
                    _profile_node(key),
                    _profile_node(value, mapping_key=decoded_key),
                )
            )
        return {"mapping": entries}
    if isinstance(node, SequenceNode):
        return {"sequence": [_profile_node(item) for item in node.value]}
    if isinstance(node, ScalarNode):
        value = node.value
        if mapping_key == "uses":
            value = re.sub(r"@(?=[a-f0-9]{40}$)[a-f0-9]{40}$", "@<SHA256-PIN>", value)
        return {"scalar": value}
    raise AssertionError("publisher profile contains an unsupported YAML node")


def publisher_job_digest(job: str) -> str:
    """Hash the complete semantic publisher profile except mutable pin SHA values."""

    document = workflow_mapping(job, context="publisher job")
    profile = _profile_node(document)
    encoded = json.dumps(profile, ensure_ascii=True, separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def assert_publisher_command_policy(
    job: str,
    *,
    expected_digest: str,
    expected_job_digest: str,
) -> None:
    """Reject merge, readiness, force, and non-exact branch push variants."""

    scripts = workflow_run_scalars(job)
    if not scripts:
        raise AssertionError("publisher has no shell commands")
    if publisher_script_digest(job) != expected_digest:
        raise AssertionError("publisher shell profile changed without an explicit contract update")
    if publisher_job_digest(job) != expected_job_digest:
        raise AssertionError("publisher job profile changed without an explicit contract update")
    combined = "\n".join(scripts)
    forbidden = (
        r"(?i)(?:^|[\s;])gh\s+pr\s+(?:merge|ready)(?:\s|$)",
        r"(?i)--auto-merge(?:\s|$)",
        r"(?i)--ready-for-review(?:\s|$)",
        r"(?i)--force(?:-with-lease)?(?:\s|$)",
        r"(?m)\bgit\s+(?:-c\s+\S+\s+|\\\s*\n\s*)+push\b",
    )
    for pattern in forbidden:
        if re.search(pattern, combined):
            raise AssertionError(f"publisher contains forbidden command form {pattern!r}")
    push_lines = [
        line
        for script in scripts
        for line in _active_shell_lines(script)
        if re.search(r"\bgit(?:\s+-c\s+\S+)*\s+push\b", line)
    ]
    if not push_lines or any(line != 'git push origin "$UPDATE_BRANCH"' for line in push_lines):
        raise AssertionError(f"publisher has an unexpected Git push command: {push_lines!r}")
    if not re.search(r"(?m)^[ \t]*gh pr create \\\n[ \t]*--draft \\\n", combined):
        raise AssertionError("publisher does not create a Draft pull request")
    if not re.search(r"(?m)^[ \t]*is_draft=\"\$\(gh api --method GET .*--jq '\.draft'\)\"$", combined):
        raise AssertionError("publisher does not obtain the existing PR Draft state")
    if not re.search(r'(?m)^[ \t]*if \[ "\$is_draft" != "true" \]; then$', combined):
        raise AssertionError("publisher does not reject an existing non-Draft PR")
    if not re.search(r"(?m)^[ \t]*auto_merge=\"\$\(gh api --method GET .*--jq '\.auto_merge'\)\"$", combined):
        raise AssertionError("publisher does not obtain the existing PR auto-merge state")
    if not re.search(r'(?m)^[ \t]*if \[ "\$auto_merge" != "null" \]; then$', combined):
        raise AssertionError("publisher does not reject an existing auto-merge state")


def fixture_violations(text: str) -> set[str]:
    """Model the policy boundary exercised by the safe/unsafe fixtures."""

    violations: set[str] = set()
    triggers = workflow_triggers(text)
    if "pull_request_target" in triggers:
        violations.add("pull_request_target")
    if "workflow_run" in triggers:
        violations.add("workflow_run")
    if top_level_permissions(text) != {"contents": "read"}:
        violations.add("top_level_permissions")
    if workflow_secret_references(text):
        violations.add("secret_reference")
    for job in job_blocks(text).values():
        permissions = job_permissions(job)
        job_checkouts = checkout_steps(job)
        if any(step.with_values.get("persist-credentials") != "false" for step in job_checkouts):
            violations.add("persisted_credentials")
        if (
            any(value == "write" for value in permissions.values())
            and any(step.with_values.get("submodules") == "recursive" for step in job_checkouts)
            and any("make quick-check" in run for run in workflow_run_scalars(job))
        ):
            violations.add("privileged_submodule_execution")
    return violations


def semantic_uses_key_positions(text: str) -> list[tuple[int, int]]:
    """Return decoded YAML ``uses`` keys so escaped spellings cannot evade tests."""

    document = yaml.compose(text, Loader=yaml.BaseLoader)
    if document is None:
        return []
    positions: list[tuple[int, int]] = []
    visited: set[int] = set()

    def visit(node: Node) -> None:
        if id(node) in visited:
            return
        visited.add(id(node))
        if isinstance(node, MappingNode):
            for key, value in node.value:
                if isinstance(key, ScalarNode) and key.value == "uses":
                    positions.append((key.start_mark.line + 1, key.start_mark.column + 1))
                visit(value)
        elif isinstance(node, SequenceNode):
            for item in node.value:
                visit(item)

    visit(document)
    return sorted(positions)


class CiSecurityWorkflowTest(unittest.TestCase):
    def workflow(self, name: str) -> str:
        return (WORKFLOWS / name).read_text(encoding="utf-8")

    def workflow_paths(self) -> list[Path]:
        return sorted({path for pattern in WORKFLOW_PATTERNS for path in WORKFLOWS.glob(pattern)})

    def jobs(self, name: str) -> dict[str, str]:
        return job_blocks(self.workflow(name))

    def test_all_remote_actions_are_immutable_sha_pins(self) -> None:
        lock_text = (ROOT / "ci" / "tooling" / "security-tools.lock.yml").read_text(encoding="utf-8")
        recorded_shas = set(re.findall(r"commit_sha: ([a-f\d]{40})", lock_text))
        for path in self.workflow_paths():
            for line in path.read_text(encoding="utf-8").splitlines():
                if "uses:" not in line or "@" not in line or "./" in line:
                    continue
                reference = line.split("uses:", 1)[1].strip()
                self.assertRegex(reference, SHA_PIN, f"{path}: {line}")
                self.assertIn(reference.split("@", 1)[1].split()[0], recorded_shas, f"{path}: {line}")

    def test_workflow_uses_keys_are_canonical_and_unquoted(self) -> None:
        for path in self.workflow_paths():
            text = path.read_text(encoding="utf-8")
            canonical_positions: list[tuple[int, int]] = []
            for line_number, line in enumerate(text.splitlines(), start=1):
                match = CANONICAL_USES_KEY.match(line)
                if match is not None:
                    canonical_positions.append((line_number, line.index("uses:", match.start()) + 1))
            self.assertEqual(
                canonical_positions,
                semantic_uses_key_positions(text),
                f"{path}: every decoded YAML uses key must use canonical unquoted block syntax",
            )

    def test_action_release_comments_exactly_match_the_lock(self) -> None:
        lock_text = (ROOT / "ci" / "tooling" / "security-tools.lock.yml").read_text(encoding="utf-8")
        action_section = lock_text.split("pinned_actions:\n", 1)[1].split("\ntools:\n", 1)[0]
        locked: dict[str, tuple[str, str]] = {}
        for match in re.finditer(
            r"(?ms)^  (?P<name>[a-z0-9_.-]+/[a-z0-9_.-]+):\n(?P<body>.*?)(?=^  [a-z0-9_.-]+/[a-z0-9_.-]+:|\Z)",
            action_section,
        ):
            version = re.search(r"(?m)^    version: (?P<value>v\d+\.\d+\.\d+)$", match.group("body"))
            sha = re.search(r"(?m)^    commit_sha: (?P<value>[a-f\d]{40})$", match.group("body"))
            self.assertIsNotNone(version, match.group("name"))
            self.assertIsNotNone(sha, match.group("name"))
            locked[match.group("name")] = (sha.group("value"), version.group("value"))  # type: ignore[union-attr]
        self.assertEqual(len(locked), 9)
        for path in self.workflow_paths():
            for line in path.read_text(encoding="utf-8").splitlines():
                if "uses:" not in line or "@" not in line or "./" in line:
                    continue
                reference = line.split("uses:", 1)[1].strip()
                action_path, pinned = reference.split("@", 1)
                slug = "/".join(action_path.split("/")[:2])
                sha, comment = pinned.split(" # ", 1)
                self.assertIn(slug, locked, f"{path}: {line}")
                self.assertEqual((sha, comment), locked[slug], f"{path}: {line}")

    def test_secret_scan_uses_exact_pr_range_and_advisory_history(self) -> None:
        text = self.workflow("ci-security-secrets.yml")
        self.assertIn("github.event.pull_request.base.sha", text)
        self.assertIn("github.event.pull_request.head.sha", text)
        self.assertIn('git merge-base "$BASE_SHA" "$HEAD_SHA"', text)
        self.assertIn("--redact=100", text)
        self.assertIn("continue-on-error: true", text)

    def test_osv_uses_the_pr_head_not_merge_sha(self) -> None:
        text = self.workflow("ci-security-osv.yml")
        self.assertIn("OSV_HEAD_SHA: ${{ github.event.pull_request.head.sha }}", text)
        self.assertNotIn("OSV_HEAD_SHA: ${{ github.sha }}", text)
        self.assertIn("old-results.json", text)
        self.assertIn("new-results.json", text)
        self.assertNotIn("fix", text.lower())

    def test_codeql_tracks_module_go_versions_and_bounded_cpp_scope(self) -> None:
        text = self.workflow("ci-security-codeql.yml")
        jobs = self.jobs("ci-security-codeql.yml")
        directive = re.compile(r"(?m)^go (1\.26\.(?:0|[1-9][0-9]*))$")
        module_versions: dict[str, str] = {}
        module_paths = {
            "envoy-go": ROOT / "connectors" / "envoy" / "ext_proc" / "go.mod",
            "traefik-go": ROOT / "connectors" / "traefik" / "native_middleware" / "go.mod",
        }
        for job_name, module_path in module_paths.items():
            module_text = module_path.read_text(encoding="utf-8")
            matches = directive.findall(module_text)
            self.assertEqual(len(matches), 1, module_path)
            self.assertIsNone(re.search(r"(?m)^toolchain[ \t]+", module_text), module_path)
            module_versions[job_name] = matches[0]

        self.assertEqual(len(set(module_versions.values())), 1, "the two Go module directives must be an exact consensus")
        for job_name, expected_version in module_versions.items():
            self.assertEqual(job_environment(jobs[job_name]).get("GOTOOLCHAIN"), "local", job_name)
            setup_go = action_step_with_values(jobs[job_name], action_prefix="actions/setup-go@")
            self.assertEqual(setup_go, [{"go-version": expected_version}], job_name)
        self.assertIn("connectors/envoy/ext_proc", text)
        self.assertIn("connectors/traefik/native_middleware", text)
        self.assertIn("make check-common-helpers-c17", text)

    def test_security_tool_lock_has_provenance_and_digests(self) -> None:
        text = (ROOT / "ci" / "tooling" / "security-tools.lock.yml").read_text(encoding="utf-8")
        for tool in ("actionlint", "zizmor", "gitleaks"):
            self.assertIn(f"  {tool}:", text)
        self.assertGreaterEqual(text.count("sha256:"), 3)
        self.assertIn("full_history_gitleaks: advisory_until_historical_findings_are_triaged", text)

    def test_all_workflows_have_read_only_top_level_default(self) -> None:
        for path in self.workflow_paths():
            self.assertEqual(
                top_level_permissions(path.read_text(encoding="utf-8")),
                {"contents": "read"},
                path.name,
            )

    def test_job_write_permissions_are_exactly_allowlisted(self) -> None:
        observed: dict[tuple[str, str], dict[str, str]] = {}
        for path in self.workflow_paths():
            for job_name, job in job_blocks(path.read_text(encoding="utf-8")).items():
                permissions = job_permissions(job)
                if any(value == "write" for value in permissions.values()):
                    observed[(path.name, job_name)] = permissions
                    for capability in ("checks", "issues", "packages", "id-token", "attestations"):
                        self.assertNotIn(capability, permissions, f"{path.name}:{job_name}")
        self.assertEqual(observed, EXPECTED_WRITE_PERMISSIONS)

    def test_quoted_or_escaped_writer_jobs_cannot_bypass_permission_audits(self) -> None:
        text = textwrap.dedent(
            """\
            name: structural-permission-mutation
            permissions:
              contents: read
            jobs:
              "\\x71uoted-writer":
                permissions:
                  "\\x63ontents": write
                runs-on: ubuntu-latest
                steps: []
              write-all-writer:
                permissions: write-all
                runs-on: ubuntu-latest
                steps: []
            """
        )
        jobs = job_blocks(text)
        self.assertEqual(set(jobs), {"quoted-writer", "write-all-writer"})
        self.assertEqual(job_permissions(jobs["quoted-writer"]), {"contents": "write"})
        self.assertEqual(job_permissions(jobs["write-all-writer"]), {"*": "write"})
        self.assertEqual(top_level_permissions(text), {"contents": "read"})

    def test_quoted_escaped_explicit_and_flow_trigger_keys_are_semantic(self) -> None:
        def workflow_with_trigger(event: str, spelling: str) -> str:
            if spelling == "quoted":
                trigger = f"on:\n  \"{event}\": {{}}"
            elif spelling == "escaped":
                trigger = f"on:\n  \"\\x{ord(event[0]):02x}{event[1:]}\": {{}}"
            elif spelling == "explicit":
                trigger = f"on:\n  ? !!str {event}\n  : {{}}"
            elif spelling == "flow":
                trigger = f"on: {{{event}: {{}}}}"
            else:  # pragma: no cover - local test construction guard
                raise AssertionError(f"unknown trigger spelling {spelling}")
            return (
                "name: semantic-trigger-mutation\n"
                f"{trigger}\n"
                "permissions:\n"
                "  contents: read\n"
                "jobs:\n"
                "  reader:\n"
                "    permissions:\n"
                "      contents: read\n"
                "    runs-on: ubuntu-latest\n"
                "    steps: []\n"
            )

        for event in ("pull_request_target", "workflow_run", "pull_request"):
            for spelling in ("quoted", "escaped", "explicit", "flow"):
                text = workflow_with_trigger(event, spelling)
                self.assertEqual(workflow_triggers(text), {event}, f"{event}:{spelling}")
                violations = fixture_violations(text)
                if event in {"pull_request_target", "workflow_run"}:
                    self.assertIn(event, violations, f"{event}:{spelling}")
                else:
                    self.assertEqual(violations, set(), f"{event}:{spelling}")

        duplicate = textwrap.dedent(
            """\
            name: duplicate-trigger-mutation
            on:
              pull_request: {}
              pull_request: {}
            """
        )
        with self.assertRaises(AssertionError):
            workflow_triggers(duplicate)
        merged = textwrap.dedent(
            """\
            name: merged-trigger-mutation
            trigger-anchor: &trigger_anchor
              pull_request_target: {}
            on:
              <<: *trigger_anchor
            """
        )
        with self.assertRaises(AssertionError):
            workflow_triggers(merged)

    def test_semantic_checkout_fields_reject_comments_and_escaped_values(self) -> None:
        text = textwrap.dedent(
            """\
            name: checkout-mutation
            on: pull_request
            permissions:
              contents: write
            jobs:
              writer:
                permissions:
                  contents: write
                runs-on: ubuntu-latest
                steps:
                  - uses: actions/checkout@0123456789012345678901234567890123456789
                    with:
                      persist-credentials: true # persist-credentials: false
                      submodules: "\\x72ecursive"
                  - run: make quick-check
            """
        )
        steps = checkout_steps(text)
        self.assertEqual(len(steps), 1)
        self.assertEqual(steps[0].with_values["persist-credentials"], "true")
        self.assertEqual(steps[0].with_values["submodules"], "recursive")
        self.assertIn("persisted_credentials", fixture_violations(text))
        self.assertIn("privileged_submodule_execution", fixture_violations(text))

    def test_semantic_secret_scan_detects_escaped_and_bracket_context_access(self) -> None:
        escaped_context = "se" + r"\x63" + "rets"
        expression_open = "$" + "{{"
        escaped = (
            "name: escaped-secret-mutation\n"
            "on: pull_request\n"
            "permissions:\n"
            "  contents: read\n"
            "jobs:\n"
            "  reader:\n"
            "    permissions:\n"
            "      contents: read\n"
            "    runs-on: ubuntu-latest\n"
            "    steps:\n"
            '      - run: "echo '
            + expression_open
            + " "
            + escaped_context
            + '.TOKEN }}"\n'
        )
        bracket = textwrap.dedent(
            """\
            name: bracket-secret-mutation
            on: pull_request
            permissions:
              contents: read
            jobs:
              reader:
                permissions:
                  contents: read
                runs-on: ubuntu-latest
                steps:
                  - run: "echo EXPRESSION"
            """
        ).replace("EXPRESSION", "$" + "{{ secrets['TOKEN'] }}")
        self.assertTrue(workflow_secret_references(escaped))
        self.assertTrue(workflow_secret_references(bracket))
        self.assertIn("secret_reference", fixture_violations(escaped))
        self.assertIn("secret_reference", fixture_violations(bracket))

    def test_all_checkouts_disable_persisted_credentials(self) -> None:
        for path in self.workflow_paths():
            for checkout_step in checkout_steps(path.read_text(encoding="utf-8")):
                self.assertEqual(
                    checkout_step.with_values.get("persist-credentials"),
                    "false",
                    path.name,
                )

    def test_automated_updaters_have_exact_semantic_trust_and_delivery_profiles(self) -> None:
        gate = "github.ref == format('refs/heads/{0}', github.event.repository.default_branch)"
        expression = lambda suffix: "$" + "{{ " + gate + suffix + " }}"
        github_expression = lambda value: "$" + "{{ " + value + " }}"
        default_checkout = {
            "ref": github_expression("github.event.repository.default_branch"),
            "submodules": "false",
            "persist-credentials": "false",
        }
        fetched_checkout = {**default_checkout, "fetch-depth": "0"}
        recursive_checkout = {**fetched_checkout, "submodules": "recursive"}
        expected_python = github_expression("steps.setup-python.outputs.python-path")
        github_token = github_expression("github.token")
        run_url = github_expression(
            "github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id"
        )
        profiles = {
            "update-actions-versions.yml": {
                "resolver": "resolve-ci-tool-updates",
                "validator": "validate-ci-tool-updates",
                "publisher": "create-ci-tool-update-pr",
                "validator_if": expression(" && needs.resolve-ci-tool-updates.outputs.update_available == 'true'"),
                "publisher_if": expression(
                    " && needs.resolve-ci-tool-updates.outputs.update_available == 'true'"
                    " && needs.validate-ci-tool-updates.result == 'success'"
                ),
                "validator_checkout": default_checkout,
                "publisher_env": {
                    "CANDIDATE_SHA256": github_expression(
                        "needs.resolve-ci-tool-updates.outputs.candidate_sha256"
                    ),
                    "DEFAULT_BRANCH": github_expression("github.event.repository.default_branch"),
                    "UPDATE_BRANCH": "automation/update-parent-ci-tooling",
                    "PR_TITLE": "chore(ci): propose Parent CI tooling update",
                    "WORKFLOW_RUN_URL": run_url,
                    "PYTHONDONTWRITEBYTECODE": "1",
                },
                "publisher_steps": [
                    {"EXPECTED_PYTHON": expected_python},
                    {
                        "GH_TOKEN": github_token,
                        "CANDIDATE_BASE_SHA": github_expression("steps.update.outputs.base_sha"),
                    },
                ],
                "script_digest": "0d0d4fd6ae4f47507393046b28c30bfe11af6117e9b02fd1b6acffea2b14aad7",
                "job_digest": "f825e0e05d960d4f6522059e3f5fd721329c5aa8e6d5f4158047658d86057d8c",
            },
            "update-python-version.yml": {
                "resolver": "resolve-python-patch",
                "validator": "validate-python-patch",
                "publisher": "create-python-update-pr",
                "validator_if": expression(" && needs.resolve-python-patch.outputs.update_available == 'true'"),
                "publisher_if": expression(
                    " && needs.resolve-python-patch.outputs.update_available == 'true'"
                    " && needs.validate-python-patch.result == 'success'"
                ),
                "validator_checkout": default_checkout,
                "publisher_env": {
                    "CANDIDATE_VERSION": github_expression("needs.resolve-python-patch.outputs.version"),
                    "CURRENT_VERSION": github_expression("needs.resolve-python-patch.outputs.current_version"),
                    "DEFAULT_BRANCH": github_expression("github.event.repository.default_branch"),
                    "UPDATE_BRANCH": "automation/update-python-313",
                    "PR_TITLE": "chore(ci): propose Python 3.13 patch update",
                    "WORKFLOW_RUN_URL": run_url,
                    "PYTHONDONTWRITEBYTECODE": "1",
                },
                "publisher_steps": [
                    {"EXPECTED_PYTHON": expected_python},
                    {
                        "GH_TOKEN": github_token,
                        "CANDIDATE_BASE_SHA": github_expression("steps.update.outputs.base_sha"),
                    },
                ],
                "script_digest": "81c484127046202e18410d8e553b2b1965af5f289ec25e4109fd5cff5d9a0cd9",
                "job_digest": "2a733cbfbd561461828332f2eef2c606b653b244251faaeba0acbf93df44dfed",
            },
            "update-go-version.yml": {
                "resolver": "resolve-go-patch",
                "validator": "validate-go-patch",
                "publisher": "create-go-update-pr",
                "validator_if": expression(" && needs.resolve-go-patch.outputs.update_available == 'true'"),
                "publisher_if": expression(
                    " && needs.resolve-go-patch.outputs.update_available == 'true'"
                    " && needs.validate-go-patch.result == 'success'"
                ),
                "validator_checkout": default_checkout,
                "publisher_env": {
                    "CANDIDATE_VERSION": github_expression("needs.resolve-go-patch.outputs.version"),
                    "CURRENT_VERSION": github_expression("needs.resolve-go-patch.outputs.current_version"),
                    "DEFAULT_BRANCH": github_expression("github.event.repository.default_branch"),
                    "UPDATE_BRANCH": "automation/update-go-126",
                    "PR_TITLE": "chore(ci): propose Go 1.26 patch update",
                    "WORKFLOW_RUN_URL": run_url,
                    "PYTHONDONTWRITEBYTECODE": "1",
                },
                "publisher_steps": [
                    {"EXPECTED_PYTHON": expected_python},
                    {
                        "GH_TOKEN": github_token,
                        "CANDIDATE_BASE_SHA": github_expression("steps.update.outputs.base_sha"),
                    },
                ],
                "script_digest": "4c7b072c776925de43ab99e53f059d23dbca23d1065e8656cd31e0f6ddfdb7ae",
                "job_digest": "72c23c23c58ec14021fc7e95d0e543bf3ec3e430f80bad49e401cb61038c78c8",
            },
            "update-submodules.yml": {
                "resolver": "resolve-submodule-update",
                "validator": "validate-submodule-update",
                "publisher": "create-submodule-update-pr",
                "validator_if": expression(" && needs.resolve-submodule-update.outputs.changed == 'true'"),
                "publisher_if": expression(
                    " && needs.resolve-submodule-update.outputs.changed == 'true'"
                    " && needs.validate-submodule-update.result == 'success'"
                ),
                "validator_checkout": recursive_checkout,
                "publisher_env": {
                    "CANDIDATE_SHA": github_expression("needs.resolve-submodule-update.outputs.candidate_sha"),
                    "CANDIDATE_BASE_SHA": github_expression("needs.resolve-submodule-update.outputs.base_sha"),
                    "SUBMODULE_REF": github_expression("needs.resolve-submodule-update.outputs.submodule_ref"),
                    "DEFAULT_BRANCH": github_expression("github.event.repository.default_branch"),
                    "UPDATE_BRANCH": "chore/update-submodules",
                    "PR_TITLE": "chore: propose submodule update",
                    "WORKFLOW_RUN_URL": run_url,
                },
                "publisher_steps": [{"GH_TOKEN": github_token}],
                "script_digest": "c28874221a02ae0defccd05ff6522e0d58e0c0815dff0bfec79245f41a1f81f2",
                "job_digest": "74256ed56e07a07a568e84cd58837fbb86a6ae1330ebca9bd50834bd4d3f9d43",
            },
        }
        expected_workflow_env = {
            "update-submodules.yml": {
                "SUBMODULE_PATH": "modules/ModSecurity-test-Framework",
                "SUBMODULE_URL": "https://github.com/Easton97-Jens/ModSecurity-test-Framework.git",
            }
        }
        for workflow_name, profile in profiles.items():
            text = self.workflow(workflow_name)
            self.assertEqual(workflow_triggers(text), {"schedule", "workflow_dispatch"}, workflow_name)
            top_level = mapping_items(workflow_mapping(text, context=workflow_name), context=workflow_name)
            self.assertNotIn("defaults", top_level, workflow_name)
            self.assertEqual(workflow_environment(text), expected_workflow_env.get(workflow_name, {}), workflow_name)
            jobs = job_blocks(text)
            resolver = jobs[profile["resolver"]]
            validator = jobs[profile["validator"]]
            publisher = jobs[profile["publisher"]]
            assert_updater_job_boundary(
                resolver,
                expected_if=gate,
                expected_checkout_with=default_checkout if workflow_name != "update-submodules.yml" else fetched_checkout,
            )
            assert_updater_job_boundary(
                validator,
                expected_if=profile["validator_if"],
                expected_checkout_with=profile["validator_checkout"],
            )
            assert_updater_job_boundary(
                publisher,
                expected_if=profile["publisher_if"],
                expected_checkout_with=fetched_checkout,
            )
            self.assertEqual(job_permissions(publisher), {"contents": "write", "pull-requests": "write"})
            self.assertEqual(job_environment(publisher), profile["publisher_env"], workflow_name)
            self.assertEqual(step_environment_mappings(publisher), profile["publisher_steps"], workflow_name)
            for read_only_job in (resolver, validator):
                self.assertEqual(workflow_secret_references(read_only_job), [], workflow_name)
                self.assertEqual(workflow_token_references(read_only_job), [], workflow_name)
            assert_publisher_command_policy(
                publisher,
                expected_digest=profile["script_digest"],
                expected_job_digest=profile["job_digest"],
            )

    def test_updater_publishers_bind_candidates_to_one_fresh_default_revision(self) -> None:
        """Reject drift both before publishing and after an existing-PR fetch.

        A profile digest makes intentional workflow changes explicit, but it is
        not the semantic guarantee here: a future rehash must not be able to
        remove the default-branch revalidation that keeps a precomputed
        candidate from being applied onto a newer trusted tree.
        """

        github_expression = lambda value: "$" + "{{ " + value + " }}"
        contracts = (
            (
                "update-actions-versions.yml",
                "create-ci-tool-update-pr",
                "create-ci-tool-update-pr",
                github_expression("steps.update.outputs.base_sha"),
                "if ! rebuild_trusted_candidate_index; then",
            ),
            (
                "update-python-version.yml",
                "create-python-update-pr",
                "create-python-update-pr",
                github_expression("steps.update.outputs.base_sha"),
                'git read-tree "origin/$UPDATE_BRANCH"',
            ),
            (
                "update-go-version.yml",
                "create-go-update-pr",
                "create-go-update-pr",
                github_expression("steps.update.outputs.base_sha"),
                'git read-tree "origin/$UPDATE_BRANCH"',
            ),
            (
                "update-submodules.yml",
                "create-submodule-update-pr",
                "resolve-submodule-update",
                github_expression("needs.resolve-submodule-update.outputs.base_sha"),
                'git read-tree "origin/$DEFAULT_BRANCH"',
            ),
        )
        verified_default = (
            'verified_default_sha="$(git rev-parse --verify --quiet '
            '"origin/$DEFAULT_BRANCH^{commit}")"'
        )
        candidate_comparison = 'if [ "$verified_default_sha" != "$CANDIDATE_BASE_SHA" ]; then'
        fresh_branch_head_check = (
            'if [ "$(git rev-parse HEAD)" != '
            '"$(git rev-parse "origin/$DEFAULT_BRANCH")" ]; then'
        )

        def assert_ordered(source: str, *fragments: str) -> None:
            position = -1
            for fragment in fragments:
                next_position = source.find(fragment, position + 1)
                self.assertNotEqual(next_position, -1, fragment)
                position = next_position

        for (
            workflow_name,
            publisher_name,
            candidate_producer_name,
            expected_base_expression,
            reconstruction_marker,
        ) in contracts:
            with self.subTest(workflow=workflow_name):
                workflow = self.workflow(workflow_name)
                jobs = self.jobs(workflow_name)
                publisher = jobs[publisher_name]
                candidate_producer = jobs[candidate_producer_name]
                publisher_environments = [
                    job_environment(publisher),
                    *step_environment_mappings(publisher),
                ]
                self.assertIn(
                    expected_base_expression,
                    [
                        environment["CANDIDATE_BASE_SHA"]
                        for environment in publisher_environments
                        if "CANDIDATE_BASE_SHA" in environment
                    ],
                )
                self.assertIn('candidate_base_sha="$(git rev-parse HEAD)"', candidate_producer)
                self.assertIn(
                    "printf 'base_sha=%s\\n' \"$candidate_base_sha\" >> \"$GITHUB_OUTPUT\"",
                    candidate_producer,
                )
                if workflow_name == "update-submodules.yml":
                    self.assertIn(
                        "base_sha: ${{ steps.resolve.outputs.base_sha }}",
                        workflow,
                    )

                # The candidate must match a freshly fetched default ref
                # before either the existing-PR or new-branch delivery path.
                assert_ordered(
                    publisher,
                    'git fetch --no-tags origin "$DEFAULT_BRANCH"',
                    verified_default,
                    candidate_comparison,
                    "existing_pr=\"$(",
                )

                existing_start = publisher.index('if [ -n "$existing_pr" ]; then')
                fresh_start = publisher.index(
                    'if [ "$remote_branch" = true ]; then', existing_start
                )
                existing_branch = publisher[existing_start:fresh_start]
                # Fetching both refs can move origin/default again.  The
                # second check must happen before any merge-base, index
                # rebuild/read-tree, or commit can consume that ref.
                assert_ordered(
                    existing_branch,
                    'git fetch --no-tags origin "$DEFAULT_BRANCH" "$UPDATE_BRANCH"',
                    verified_default,
                    candidate_comparison,
                    "exit 1",
                    'merge_base="$(git merge-base',
                    reconstruction_marker,
                    'commit="$(git commit-tree',
                )

                fresh_branch = publisher[fresh_start:]
                assert_ordered(
                    fresh_branch,
                    'git switch --no-track -c "$UPDATE_BRANCH" "origin/$DEFAULT_BRANCH"',
                    fresh_branch_head_check,
                    'git push origin "$UPDATE_BRANCH"',
                )

    def test_semantic_updater_profiles_reject_comment_spoofs_and_forced_refspecs(self) -> None:
        gate = "github.ref == format('refs/heads/{0}', github.event.repository.default_branch)"
        comment_spoof = textwrap.dedent(
            """\
            updater:
              if: true # github.ref == format('refs/heads/{0}', github.event.repository.default_branch)
              steps:
                - uses: actions/checkout@0123456789012345678901234567890123456789
                  with:
                    ref: REF_SPOOF
                    submodules: false
                    persist-credentials: false
            """
        ).replace(
            "REF_SPOOF",
            "$" + "{{ github.sha }} # $" + "{{ github.event.repository.default_branch }}",
        )
        with self.assertRaises(AssertionError):
            assert_updater_job_boundary(
                comment_spoof,
                expected_if=gate,
                expected_checkout_with={
                    "ref": "$" + "{{ github.event.repository.default_branch }}",
                    "submodules": "false",
                    "persist-credentials": "false",
                },
            )
        forced_refspec = textwrap.dedent(
            """\
            publisher:
              steps:
                - run: |
                    git push origin +"$UPDATE_BRANCH"
            """
        )
        with self.assertRaises(AssertionError):
            assert_publisher_command_policy(
                forced_refspec,
                expected_digest=publisher_script_digest(forced_refspec),
                expected_job_digest=publisher_job_digest(forced_refspec),
            )

    def test_untrusted_pull_request_model(self) -> None:
        sarif_write_jobs = {
            key for key, value in EXPECTED_WRITE_PERMISSIONS.items() if value.get("security-events") == "write"
        }
        for path in self.workflow_paths():
            text = path.read_text(encoding="utf-8")
            triggers = workflow_triggers(text)
            self.assertNotIn("pull_request_target", triggers, path.name)
            self.assertNotIn("workflow_run", triggers, path.name)
            if "pull_request" not in triggers:
                continue
            self.assertEqual(workflow_secret_references(text), [], path.name)
            for job_name, job in job_blocks(text).items():
                permissions = job_permissions(job)
                if not any(value == "write" for value in permissions.values()):
                    continue
                self.assertIn((path.name, job_name), sarif_write_jobs, f"{path.name}:{job_name}")
                self.assertEqual(
                    permissions,
                    {"contents": "read", "security-events": "write"},
                    f"{path.name}:{job_name}",
                )
                if path.name == "ci-security-scorecard.yml":
                    self.assertIn("github.event_name != 'pull_request'", job)

    def test_cleanup_jobs_do_not_checkout_or_execute_project_code(self) -> None:
        for workflow_name in ("cleanup-artifacts.yml", "test-full-smoke-sequential.yml"):
            job = self.jobs(workflow_name)["cleanup-artifacts"]
            self.assertEqual(job_permissions(job), {"actions": "write"}, workflow_name)
            self.assertEqual(checkout_step_blocks(job), [], workflow_name)
            self.assertNotIn("run:", job, workflow_name)

    def test_update_submodules_separates_validation_from_publishing(self) -> None:
        workflow_name = "update-submodules.yml"
        workflow = self.workflow(workflow_name)
        jobs = self.jobs(workflow_name)
        self.assertEqual(
            set(jobs),
            {
                "resolve-submodule-update",
                "validate-submodule-update",
                "create-submodule-update-pr",
            },
        )
        self.assertEqual(job_permissions(jobs["resolve-submodule-update"]), {"contents": "read"})
        self.assertEqual(job_permissions(jobs["validate-submodule-update"]), {"contents": "read"})
        self.assertEqual(
            job_permissions(jobs["create-submodule-update-pr"]),
            {"contents": "write", "pull-requests": "write"},
        )
        trusted_default_ref = "github.ref == format('refs/heads/{0}', github.event.repository.default_branch)"
        for job_name in ("resolve-submodule-update", "validate-submodule-update", "create-submodule-update-pr"):
            job = jobs[job_name]
            self.assertIn(trusted_default_ref, job, job_name)
            checkouts = checkout_step_blocks(job)
            self.assertEqual(len(checkouts), 1, job_name)
            self.assertIn("ref: ${{ github.event.repository.default_branch }}", checkouts[0], job_name)
            self.assertIn("persist-credentials: false", checkouts[0], job_name)
        self.assertIn("needs: resolve-submodule-update", jobs["validate-submodule-update"])
        self.assertIn("submodules: recursive", jobs["validate-submodule-update"])
        self.assertIn("make quick-check", jobs["validate-submodule-update"])
        self.assertNotIn("GH_TOKEN", jobs["validate-submodule-update"])
        self.assertNotIn("secrets.", jobs["validate-submodule-update"])

        publisher = jobs["create-submodule-update-pr"]
        self.assertIn("submodules: false", publisher)
        self.assertIn("persist-credentials: false", publisher)
        self.assertIn("git ls-remote --exit-code", publisher)
        self.assertIn('git ls-remote --symref --exit-code "$SUBMODULE_URL" HEAD', publisher)
        self.assertIn("git update-index --add --cacheinfo", publisher)
        self.assertIn("GH_TOKEN: ${{ github.token }}", publisher)
        self.assertIn("DEFAULT_BRANCH: ${{ github.event.repository.default_branch }}", publisher)
        self.assertIn("assert_exact_submodule_path", publisher)
        self.assertIn('git diff --name-status -z --no-renames "$merge_base" "origin/$UPDATE_BRANCH"', publisher)
        self.assertIn('git diff --cached --name-status -z --no-renames "origin/$UPDATE_BRANCH"', publisher)
        self.assertIn('git read-tree "origin/$DEFAULT_BRANCH"', publisher)
        self.assertIn('git push origin "$UPDATE_BRANCH"', publisher)
        self.assertIn("--draft", publisher)
        self.assertIn('gh api --method GET "repos/$GITHUB_REPOSITORY/pulls/$existing_pr" --jq \'.draft\'', publisher)
        self.assertIn('if [ "$is_draft" != "true" ]; then', publisher)
        self.assertIn('gh api --method GET "repos/$GITHUB_REPOSITORY/pulls/$existing_pr" --jq \'.auto_merge\'', publisher)
        self.assertIn('if [ "$auto_merge" != "null" ]; then', publisher)
        self.assertIn("## English", publisher)
        self.assertIn("## Deutsch", publisher)
        self.assertIn("no automatic merge", publisher)
        self.assertIn("kein automatischer Merge", publisher)
        self.assertNotIn("master", workflow)
        self.assertNotIn("git checkout -B", publisher)
        self.assertNotIn("--force", publisher)
        self.assertNotIn("--force-with-lease", publisher)
        self.assertNotIn("submodules: recursive", publisher)
        self.assertNotIn("git submodule", publisher)
        self.assertNotIn("make quick-check", publisher)

    def test_submodule_publisher_rejects_rename_delete_and_unallowlisted_statuses(self) -> None:
        publisher = self.jobs("update-submodules.yml")["create-submodule-update-pr"]
        lines = publisher.splitlines()
        start = next(index for index, line in enumerate(lines) if line == "          assert_exact_submodule_path() {")
        end = next(
            index
            for index, line in enumerate(lines[start:], start=start)
            if line == "          existing_pr=\"$("
        )
        helper = textwrap.dedent("\n".join(lines[start:end]))

        def run_statuses(payload: bytes) -> subprocess.CompletedProcess[bytes]:
            with tempfile.NamedTemporaryFile() as status_file:
                status_file.write(payload)
                status_file.flush()
                return subprocess.run(
                    ["bash", "-c", f"{helper}\nassert_exact_submodule_path \"$1\"\n", "bash", status_file.name],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env={**os.environ, "SUBMODULE_PATH": "modules/ModSecurity-test-Framework"},
                    check=False,
                )

        self.assertEqual(run_statuses(b"M\0modules/ModSecurity-test-Framework\0").returncode, 0)
        for payload in (
            b"A\0modules/ModSecurity-test-Framework\0",
            b"D\0modules/ModSecurity-test-Framework\0",
            b"R100\0modules/ModSecurity-test-Framework\0",
            b"M\0.github/workflows/lint.yml\0",
            b"M\0modules/ModSecurity-test-Framework\0M\0.github/workflows/lint.yml\0",
        ):
            self.assertNotEqual(run_statuses(payload).returncode, 0)

    def test_ci_tool_updater_separates_resolution_validation_and_publishing(self) -> None:
        workflow_name = "update-actions-versions.yml"
        jobs = self.jobs(workflow_name)
        self.assertEqual(
            set(jobs),
            {
                "resolve-ci-tool-updates",
                "validate-ci-tool-updates",
                "create-ci-tool-update-pr",
            },
        )
        trusted_default_ref = "github.ref == format('refs/heads/{0}', github.event.repository.default_branch)"
        for job_name in ("resolve-ci-tool-updates", "validate-ci-tool-updates", "create-ci-tool-update-pr"):
            job = jobs[job_name]
            self.assertIn(trusted_default_ref, job, job_name)
            checkouts = checkout_step_blocks(job)
            self.assertEqual(len(checkouts), 1, job_name)
            self.assertIn("ref: ${{ github.event.repository.default_branch }}", checkouts[0], job_name)
            self.assertIn("submodules: false", checkouts[0], job_name)
            self.assertIn("persist-credentials: false", checkouts[0], job_name)
            self.assertIsNone(
                re.search(r"(?<![-A-Za-z0-9_])secrets\.", job),
                job_name,
            )

        resolver = jobs["resolve-ci-tool-updates"]
        validator = jobs["validate-ci-tool-updates"]
        publisher = jobs["create-ci-tool-update-pr"]
        self.assertEqual(job_permissions(resolver), {"contents": "read"})
        self.assertEqual(job_permissions(validator), {"contents": "read"})
        self.assertEqual(
            job_permissions(publisher),
            {"contents": "write", "pull-requests": "write"},
        )
        self.assertIn("--resolve --json", resolver)
        self.assertIn("actions/upload-artifact@", resolver)
        self.assertIn("Install hash-locked YAML parser", resolver)
        self.assertNotIn("GH_TOKEN", resolver)
        self.assertNotIn("git push", resolver)
        self.assertIn("needs: resolve-ci-tool-updates", validator)
        self.assertIn("actions/download-artifact@", validator)
        self.assertNotIn("CANDIDATE_PATH: ${{ runner.temp }}", validator)
        self.assertIn("Set candidate artifact path", validator)
        self.assertIn("--validate --candidate", validator)
        self.assertIn("Validate and checksum-download candidate tool archives before publishing", validator)
        self.assertIn("git archive --format=tar HEAD", validator)
        self.assertIn("ci/checks/common/check-python-version-contract.py", validator)
        self.assertIn("python3 ci/checks/common/check-python-version-contract.py --json", validator)
        self.assertIn("fetch_security_tool.py", validator)
        self.assertIn("for tool in actionlint zizmor gitleaks", validator)
        self.assertIn(
            'timeout 30 "$validation_root/downloaded-tools/actionlint/actionlint" --version',
            validator,
        )
        self.assertIn(
            'timeout 30 "$validation_root/downloaded-tools/zizmor/zizmor" --version',
            validator,
        )
        self.assertIn(
            'timeout 30 "$validation_root/downloaded-tools/gitleaks/gitleaks" version',
            validator,
        )
        self.assertNotIn("GH_TOKEN", validator)
        self.assertNotIn("git push", validator)
        self.assertIn("needs.validate-ci-tool-updates.result == 'success'", publisher)
        self.assertIn("Install hash-locked YAML parser", publisher)
        self.assertIn("--apply --candidate", publisher)
        self.assertIn("--verify --json", publisher)
        self.assertIn("is_explicit_parent_ci_tool_path", publisher)
        self.assertNotIn(".github/workflows/*.yml", publisher)
        self.assertNotIn(".github/workflows/*.yaml", publisher)
        self.assertNotIn("assert_parent_ci_paths", publisher)
        self.assertIn('git diff --name-status -z --no-renames "$merge_base" "origin/$UPDATE_BRANCH"', publisher)
        self.assertIn('git diff --cached --name-status -z --no-renames "origin/$UPDATE_BRANCH"', publisher)
        self.assertIn('if [ "$status" != "M" ]', publisher)
        self.assertIn("Refusing non-modification change status", publisher)
        self.assertIn('git read-tree "origin/$DEFAULT_BRANCH"', publisher)
        self.assertNotIn('git read-tree "origin/$UPDATE_BRANCH"', publisher)
        self.assertIn("Reconstructed index does not exactly match the revalidated trusted candidate worktree.", publisher)
        self.assertIn("if ! git diff --quiet; then", publisher)
        self.assertIn("git diff --cached --check", publisher)
        self.assertIn("git diff --check", publisher)
        self.assertIn("git push origin \"$UPDATE_BRANCH\"", publisher)
        self.assertNotIn("git push origin \"$DEFAULT_BRANCH\"", publisher)
        self.assertNotIn("--force", publisher)
        self.assertNotIn("--force-with-lease", publisher)
        self.assertNotIn("submodules: recursive", publisher)
        self.assertNotIn("git submodule", publisher)
        self.assertNotIn("modules/ModSecurity-test-Framework", publisher)
        self.assertIn("scripts/select-python-update-pr.py", publisher)
        self.assertIn("--jq '.draft'", publisher)
        self.assertIn('if [ "$is_draft" != "true" ]', publisher)
        self.assertIn(".auto_merge", publisher)
        self.assertIn("--draft", publisher)
        self.assertIn("## English", publisher)
        self.assertIn("## Deutsch", publisher)
        self.assertIn("no automatic merge", publisher)
        self.assertIn("kein automatischer Merge", publisher)

    def test_yaml_parser_dependency_is_hash_locked_and_provisioned(self) -> None:
        lock = (ROOT / "ci" / "tooling" / "python-ci-requirements.lock").read_text(encoding="utf-8")
        self.assertIn("PyYAML==6.0.3", lock)
        self.assertRegex(lock, r"(?m)^\s*--hash=sha256:[a-f\d]{64}$")

        parser_jobs = {
            "check-actions-versions.yml": ("check-ci-tool-updates",),
            "update-actions-versions.yml": (
                "resolve-ci-tool-updates",
                "validate-ci-tool-updates",
                "create-ci-tool-update-pr",
            ),
            "update-python-version.yml": ("validate-python-patch",),
            "update-go-version.yml": ("validate-go-patch",),
            "ci-security-workflow-lint.yml": ("actionlint",),
        }
        for workflow_name, names in parser_jobs.items():
            for job_name in names:
                job = self.jobs(workflow_name)[job_name]
                self.assertIn("Install hash-locked YAML parser", job, f"{workflow_name}:{job_name}")
                self.assertIn("--isolated", job, f"{workflow_name}:{job_name}")
                self.assertIn("--require-hashes", job, f"{workflow_name}:{job_name}")
                self.assertIn("--only-binary=:all:", job, f"{workflow_name}:{job_name}")
                self.assertIn("--index-url https://pypi.org/simple", job, f"{workflow_name}:{job_name}")
                self.assertIn("python-ci-requirements.lock", job, f"{workflow_name}:{job_name}")
                self.assertIn("PYTHONPATH=", job, f"{workflow_name}:{job_name}")

    def test_ci_tool_publisher_rejects_rename_delete_and_unallowlisted_statuses(self) -> None:
        """Exercise the actual NUL/status helper embedded in the publisher shell."""

        publisher = self.jobs("update-actions-versions.yml")["create-ci-tool-update-pr"]
        lines = publisher.splitlines()
        start = next(
            index for index, line in enumerate(lines) if line == "          is_explicit_parent_ci_tool_path() {"
        )
        end = next(
            index
            for index, line in enumerate(lines[start:], start=start)
            if line == '          current_status_file="$RUNNER_TEMP/parent-ci-tool-current-status.z"'
        )
        helper = textwrap.dedent("\n".join(lines[start:end]))

        def run_statuses(payload: bytes) -> subprocess.CompletedProcess[bytes]:
            with tempfile.NamedTemporaryFile() as status_file:
                status_file.write(payload)
                status_file.flush()
                return subprocess.run(
                    ["bash", "-c", f"{helper}\nassert_modified_parent_ci_paths \"$1\"\n", "bash", status_file.name],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )

        allowed = b"M\0ci/tooling/security-tools.lock.yml\0"
        self.assertEqual(run_statuses(allowed).returncode, 0)
        rejected = {
            "added": b"A\0ci/tooling/security-tools.lock.yml\0",
            "deleted": b"D\0ci/tooling/security-tools.lock.yml\0",
            "renamed": b"R100\0ci/tooling/security-tools.lock.yml\0.github/workflows/lint.yml\0",
            "unallowlisted": b"M\0scripts/update-github-actions-versions.py\0",
        }
        for name, payload in rejected.items():
            with self.subTest(change=name):
                self.assertNotEqual(run_statuses(payload).returncode, 0)

    def test_ci_tool_publisher_rebuilds_existing_branch_from_trusted_default(self) -> None:
        """An allowlisted malicious old-branch edit must not survive a refresh."""

        publisher = self.jobs("update-actions-versions.yml")["create-ci-tool-update-pr"]
        lines = publisher.splitlines()
        start = next(
            index for index, line in enumerate(lines) if line == "          rebuild_trusted_candidate_index() {"
        )
        end = next(
            index
            for index, line in enumerate(lines[start:], start=start)
            if line == '          current_status_file="$RUNNER_TEMP/parent-ci-tool-current-status.z"'
        )
        helper = textwrap.dedent("\n".join(lines[start:end]))

        with tempfile.TemporaryDirectory() as temporary:
            sandbox = Path(temporary)
            repository = sandbox / "repository"
            remote = sandbox / "origin.git"
            runner_temp = sandbox / "runner-temp"
            repository.mkdir()
            runner_temp.mkdir()

            def git(*arguments: str, output: bool = False) -> subprocess.CompletedProcess[str]:
                return subprocess.run(
                    ["git", *arguments],
                    cwd=repository,
                    text=True,
                    stdout=subprocess.PIPE if output else subprocess.DEVNULL,
                    stderr=subprocess.PIPE,
                    check=True,
                )

            git("init")
            git("config", "user.name", "CI contract test")
            git("config", "user.email", "ci-contract@example.invalid")
            lock = repository / "ci" / "tooling" / "security-tools.lock.yml"
            workflow = repository / ".github" / "workflows" / "lint.yml"
            lock.parent.mkdir(parents=True)
            workflow.parent.mkdir(parents=True)
            lock.write_text("trusted lock\n", encoding="utf-8")
            workflow.write_text("trusted workflow\n", encoding="utf-8")
            git("add", ".")
            git("commit", "-m", "trusted default")
            default_branch = git("branch", "--show-current", output=True).stdout.strip()
            subprocess.run(
                ["git", "init", "--bare", str(remote)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            git("remote", "add", "origin", str(remote))
            git("push", "-u", "origin", f"HEAD:{default_branch}")

            git("switch", "-c", "automation/update-parent-ci-tooling")
            workflow.write_text("malicious old draft content\n", encoding="utf-8")
            git("add", ".github/workflows/lint.yml")
            git("commit", "-m", "malicious allowed-file edit")
            git("push", "origin", "HEAD:automation/update-parent-ci-tooling")

            git("switch", default_branch)
            git("fetch", "origin", default_branch, "automation/update-parent-ci-tooling")
            lock.write_text("revalidated candidate lock\n", encoding="utf-8")
            environment = dict(os.environ)
            environment.update(
                {
                    "DEFAULT_BRANCH": default_branch,
                    "RUNNER_TEMP": str(runner_temp),
                    "changed_paths": "ci/tooling/security-tools.lock.yml",
                }
            )
            result = subprocess.run(
                ["bash", "-c", f"set -euo pipefail\n{helper}\nrebuild_trusted_candidate_index\n"],
                cwd=repository,
                env=environment,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            tree = git("write-tree", output=True).stdout.strip()
            restored_workflow = git("show", f"{tree}:.github/workflows/lint.yml", output=True).stdout
            rebuilt_lock = git("show", f"{tree}:ci/tooling/security-tools.lock.yml", output=True).stdout
            self.assertEqual(restored_workflow, "trusted workflow\n")
            self.assertEqual(rebuilt_lock, "revalidated candidate lock\n")

    def test_go_publisher_rejects_rename_delete_and_unallowlisted_statuses(self) -> None:
        """The Go updater has the same M-only no-renames protection."""

        publisher = self.jobs("update-go-version.yml")["create-go-update-pr"]
        lines = publisher.splitlines()
        start = next(
            index for index, line in enumerate(lines) if line == "          assert_exact_modified_go_paths() {"
        )
        end = next(
            index
            for index, line in enumerate(lines[start:], start=start)
            if line == '          current_status_file="$RUNNER_TEMP/go-update-current-status.z"'
        )
        helper = textwrap.dedent("\n".join(lines[start:end]))

        def run_statuses(payload: bytes) -> subprocess.CompletedProcess[bytes]:
            with tempfile.NamedTemporaryFile() as status_file:
                status_file.write(payload)
                status_file.flush()
                return subprocess.run(
                    [
                        "bash",
                        "-c",
                        f'{helper}\nassert_exact_modified_go_paths "$1"\n',
                        "bash",
                        status_file.name,
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )

        allowed = (
            b"M\0.github/workflows/ci-security-codeql.yml\0"
            b"M\0connectors/envoy/ext_proc/go.mod\0"
            b"M\0connectors/traefik/native_middleware/go.mod\0"
        )
        self.assertEqual(run_statuses(allowed).returncode, 0)
        rejected = {
            "added": b"A\0.github/workflows/ci-security-codeql.yml\0",
            "deleted": b"D\0connectors/envoy/ext_proc/go.mod\0",
            "renamed": b"R100\0connectors/envoy/ext_proc/go.mod\0other/go.mod\0",
            "unallowlisted": b"M\0scripts/update-go-version.py\0",
        }
        for name, payload in rejected.items():
            with self.subTest(change=name):
                self.assertNotEqual(run_statuses(payload).returncode, 0)

    def test_python_patch_updater_separates_trusted_stages_and_writer_scope(self) -> None:
        workflow_name = "update-python-version.yml"
        jobs = self.jobs(workflow_name)
        self.assertEqual(
            set(jobs),
            {
                "resolve-python-patch",
                "validate-python-patch",
                "create-python-update-pr",
            },
        )
        trusted_default_ref = "github.ref == format('refs/heads/{0}', github.event.repository.default_branch)"
        for job_name in ("resolve-python-patch", "validate-python-patch", "create-python-update-pr"):
            self.assertIn(trusted_default_ref, jobs[job_name], job_name)
            checkouts = checkout_step_blocks(jobs[job_name])
            self.assertEqual(len(checkouts), 1, job_name)
            self.assertIn("ref: ${{ github.event.repository.default_branch }}", checkouts[0], job_name)
            self.assertIn("submodules: false", checkouts[0], job_name)
            self.assertIn("persist-credentials: false", checkouts[0], job_name)
            self.assertNotIn("secrets.", jobs[job_name], job_name)

        self.assertEqual(job_permissions(jobs["resolve-python-patch"]), {"contents": "read"})
        self.assertEqual(job_permissions(jobs["validate-python-patch"]), {"contents": "read"})
        publisher = jobs["create-python-update-pr"]
        self.assertEqual(
            job_permissions(publisher),
            {"contents": "write", "pull-requests": "write"},
        )
        self.assertNotIn("actions: write", publisher)
        self.assertNotIn("submodules: recursive", publisher)
        self.assertNotIn("git submodule", publisher)
        self.assertNotIn("make ", publisher)
        self.assertNotIn("--force", publisher)
        self.assertNotIn("--force-with-lease", publisher)
        self.assertIn('python3 scripts/update-python-version.py --update --expected-version "$CANDIDATE_VERSION" --json', publisher)
        self.assertIn("UPDATE_BRANCH: automation/update-python-313", publisher)
        self.assertIn('PR_TITLE: "chore(ci): propose Python 3.13 patch update"', publisher)
        self.assertIn('changed_paths="$(git diff --name-only)"', publisher)
        self.assertIn("if [ \"$changed_paths\" != \".python-version\" ]; then", publisher)
        self.assertIn("git diff --check", publisher)
        self.assertIn("git push origin \"$UPDATE_BRANCH\"", publisher)
        self.assertIn("--draft", publisher)
        self.assertIn("gh pr edit \"$existing_pr\"", publisher)
        self.assertIn('gh api --method GET "repos/$GITHUB_REPOSITORY/pulls"', publisher)
        self.assertIn('-f base="$DEFAULT_BRANCH"', publisher)
        self.assertIn('-f head="${GITHUB_REPOSITORY_OWNER}:$UPDATE_BRANCH"', publisher)
        self.assertIn("set -o pipefail", publisher)
        self.assertIn("scripts/select-python-update-pr.py", publisher)
        self.assertNotIn("--input", publisher)
        self.assertNotIn("gh pr list --head", publisher)
        self.assertIn('gh api --method GET "repos/$GITHUB_REPOSITORY/pulls/$existing_pr" --jq \'.draft\'', publisher)
        self.assertIn('if [ "$is_draft" != "true" ]; then', publisher)
        self.assertIn('gh api --method GET "repos/$GITHUB_REPOSITORY/pulls/$existing_pr" --jq \'.auto_merge\'', publisher)
        self.assertIn('if [ "$auto_merge" != "null" ]; then', publisher)
        self.assertIn(
            "git fetch --no-tags origin \"$DEFAULT_BRANCH\" \"$UPDATE_BRANCH\"",
            publisher,
        )
        self.assertIn("git read-tree \"origin/$UPDATE_BRANCH\"", publisher)
        self.assertIn("git update-index --add --cacheinfo 100644 \"$candidate_blob\" .python-version", publisher)
        self.assertIn("git commit-tree \"$tree\" -p \"origin/$UPDATE_BRANCH\"", publisher)
        self.assertIn("## English", publisher)
        self.assertIn("## Deutsch", publisher)
        self.assertIn("no automatic merge", publisher)
        self.assertIn("kein automatischer Merge", publisher)

        candidate = jobs["validate-python-patch"]
        self.assertIn("python-version: ${{ needs.resolve-python-patch.outputs.version }}", candidate)
        self.assertIn("check-latest: false", candidate)
        self.assertIn("Install hash-locked YAML parser", candidate)
        self.assertIn("python3 -m compileall -q ci scripts tests", candidate)
        self.assertIn(
            'check-python-interpreter-contract.py --expected-version "$EXPECTED_VERSION" --expected-python "$EXPECTED_PYTHON"',
            candidate,
        )
        self.assertIn(
            'scripts/update-python-version.py --check --expected-version "$CANDIDATE_VERSION" --json',
            candidate,
        )

    def test_go_patch_updater_separates_trusted_stages_and_writer_scope(self) -> None:
        workflow_name = "update-go-version.yml"
        jobs = self.jobs(workflow_name)
        self.assertEqual(
            set(jobs),
            {
                "resolve-go-patch",
                "validate-go-patch",
                "create-go-update-pr",
            },
        )
        trusted_default_ref = "github.ref == format('refs/heads/{0}', github.event.repository.default_branch)"
        for job_name in ("resolve-go-patch", "validate-go-patch", "create-go-update-pr"):
            self.assertIn(trusted_default_ref, jobs[job_name], job_name)
            checkouts = checkout_step_blocks(jobs[job_name])
            self.assertEqual(len(checkouts), 1, job_name)
            self.assertIn("ref: ${{ github.event.repository.default_branch }}", checkouts[0], job_name)
            self.assertIn("submodules: false", checkouts[0], job_name)
            self.assertIn("persist-credentials: false", checkouts[0], job_name)
            self.assertNotIn("secrets.", jobs[job_name], job_name)

        self.assertEqual(job_permissions(jobs["resolve-go-patch"]), {"contents": "read"})
        candidate = jobs["validate-go-patch"]
        self.assertEqual(job_permissions(candidate), {"contents": "read"})
        self.assertIn("go-version: ${{ needs.resolve-go-patch.outputs.version }}", candidate)
        self.assertIn("Set up canonical Python for workflow contracts", candidate)
        self.assertIn("Install hash-locked YAML parser", candidate)
        self.assertIn("GOTOOLCHAIN: local", candidate)
        self.assertIn("mktemp -d", candidate)
        self.assertIn('git archive --format=tar HEAD | tar -x -C "$candidate_root"', candidate)
        self.assertIn('cd "$candidate_root"', candidate)
        self.assertIn(
            'scripts/update-go-version.py --update --expected-version "$CANDIDATE_VERSION" --json',
            candidate,
        )
        self.assertIn('if report.get("changed") is not True:', candidate)
        self.assertNotIn('go mod edit -go="$CANDIDATE_VERSION"', candidate)
        self.assertIn("go mod tidy", candidate)
        self.assertIn("cp go.mod go.mod.expected", candidate)
        self.assertIn("assert_no_module_metadata_drift", candidate)
        self.assertIn("cmp -s go.mod go.mod.expected", candidate)
        self.assertIn("go.sum.expected", candidate)
        self.assertIn("go mod verify", candidate)
        self.assertIn("go list -m all >/dev/null", candidate)
        self.assertIn("go list -buildvcs=false -deps ./...", candidate)
        self.assertIn("go test ./...", candidate)
        self.assertIn("go vet ./...", candidate)
        self.assertIn("tests.test_update_go_version", candidate)
        self.assertIn('scripts/update-go-version.py --check --expected-version "$CANDIDATE_VERSION" --json', candidate)

        resolver = jobs["resolve-go-patch"]
        self.assertIn("Set up canonical Python for Go resolution", resolver)
        self.assertIn("Verify Python interpreter contract", resolver)
        self.assertIn('"patch_update_available"', resolver)
        self.assertIn('"newer_minor_available"', resolver)
        self.assertIn("newer_minor_version", resolver)

        publisher = jobs["create-go-update-pr"]
        self.assertEqual(
            job_permissions(publisher),
            {"contents": "write", "pull-requests": "write"},
        )
        self.assertNotIn("actions: write", publisher)
        self.assertNotIn("submodules: recursive", publisher)
        self.assertNotIn("git submodule", publisher)
        self.assertNotIn("make ", publisher)
        self.assertNotIn("--force", publisher)
        self.assertNotIn("--force-with-lease", publisher)
        self.assertIn("Set up canonical Python for Go publication", publisher)
        self.assertIn("Verify Python interpreter contract", publisher)
        self.assertIn('python3 scripts/update-go-version.py --update --expected-version "$CANDIDATE_VERSION" --json', publisher)
        self.assertIn("UPDATE_BRANCH: automation/update-go-126", publisher)
        self.assertIn('PR_TITLE: "chore(ci): propose Go 1.26 patch update"', publisher)
        self.assertIn('changed_paths="$(git diff --name-only)"', publisher)
        self.assertIn("strict Go contract", publisher)
        self.assertIn("git diff --check", publisher)
        self.assertIn("git push origin \"$UPDATE_BRANCH\"", publisher)
        self.assertIn("--draft", publisher)
        self.assertIn("gh pr edit \"$existing_pr\"", publisher)
        self.assertIn('gh api --method GET "repos/$GITHUB_REPOSITORY/pulls"', publisher)
        self.assertIn('-f base="$DEFAULT_BRANCH"', publisher)
        self.assertIn('-f head="$GITHUB_REPOSITORY_OWNER:$UPDATE_BRANCH"', publisher)
        self.assertIn("set -o pipefail", publisher)
        self.assertIn('[ "$UPDATE_BRANCH" != "automation/update-go-126" ]', publisher)
        self.assertIn('[ "$GITHUB_REF" != "refs/heads/$DEFAULT_BRANCH" ]', publisher)
        self.assertIn("scripts/select-python-update-pr.py", publisher)
        self.assertIn('gh api --method GET "repos/$GITHUB_REPOSITORY/pulls/$existing_pr" --jq \'.draft\'', publisher)
        self.assertIn('if [ "$is_draft" != "true" ]; then', publisher)
        self.assertIn('gh api --method GET "repos/$GITHUB_REPOSITORY/pulls/$existing_pr" --jq \'.auto_merge\'', publisher)
        self.assertIn('if [ "$auto_merge" != "null" ]; then', publisher)
        self.assertIn("git fetch --no-tags origin \"$DEFAULT_BRANCH\" \"$UPDATE_BRANCH\"", publisher)
        self.assertIn("assert_exact_modified_go_paths", publisher)
        self.assertIn('git diff --name-status -z --no-renames > "$current_status_file"', publisher)
        self.assertNotIn('done < <("$@")', publisher)
        self.assertIn('git diff --name-status -z --no-renames "$merge_base" "origin/$UPDATE_BRANCH"', publisher)
        self.assertIn('git diff --cached --name-status -z --no-renames "origin/$UPDATE_BRANCH"', publisher)
        self.assertIn('if [ "$status" != "M" ]; then', publisher)
        self.assertIn("git read-tree \"origin/$UPDATE_BRANCH\"", publisher)
        self.assertIn("git update-index --add --cacheinfo 100644 \"$codeql_blob\" .github/workflows/ci-security-codeql.yml", publisher)
        self.assertIn("git commit-tree \"$tree\" -p \"origin/$UPDATE_BRANCH\"", publisher)
        self.assertIn("## English", publisher)
        self.assertIn("## Deutsch", publisher)
        self.assertIn("no automatic merge", publisher)
        self.assertIn("kein automatischer Merge", publisher)

    def test_sarif_upload_permissions_are_scoped(self) -> None:
        codeql = self.workflow("ci-security-codeql.yml")
        for job_name in ("actions", "envoy-go", "traefik-go", "bounded-c-cpp"):
            self.assertEqual(
                job_permissions(self.jobs("ci-security-codeql.yml")[job_name]),
                {"contents": "read", "security-events": "write"},
                job_name,
            )
        self.assertEqual(codeql.count("github/codeql-action/analyze@"), 4)

        osv = self.jobs("ci-security-osv.yml")["pull-request-diff"]
        self.assertEqual(job_permissions(osv), {"contents": "read", "security-events": "write"})
        self.assertIn("submodules: false", osv)
        self.assertIn("github.event.pull_request.base.sha", osv)
        self.assertIn("github.event.pull_request.head.sha", osv)
        self.assertIn("github/codeql-action/upload-sarif@", osv)

        scorecard_jobs = self.jobs("ci-security-scorecard.yml")
        self.assertEqual(job_permissions(scorecard_jobs["same-repository-pull-request"]), {"contents": "read"})
        self.assertIn("github.event.pull_request.head.sha", scorecard_jobs["same-repository-pull-request"])
        self.assertNotIn("upload-sarif", scorecard_jobs["same-repository-pull-request"])
        self.assertEqual(
            job_permissions(scorecard_jobs["default-branch"]),
            {"contents": "read", "security-events": "write"},
        )
        self.assertIn("github/codeql-action/upload-sarif@", scorecard_jobs["default-branch"])

    def test_permission_contract_fixtures_reject_unsafe_and_accept_safe(self) -> None:
        safe = (PERMISSION_FIXTURES / "safe.yml").read_text(encoding="utf-8")
        unsafe = (PERMISSION_FIXTURES / "unsafe.yml").read_text(encoding="utf-8")
        self.assertEqual(fixture_violations(safe), set())
        self.assertEqual(
            fixture_violations(unsafe),
            {
                "pull_request_target",
                "top_level_permissions",
                "secret_reference",
                "persisted_credentials",
                "privileged_submodule_execution",
            },
        )


if __name__ == "__main__":
    unittest.main()
