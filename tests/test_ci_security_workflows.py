"""Focused static contracts for the repository's CI-security workflows."""

from __future__ import annotations

import os
import re
import subprocess
import unittest
from pathlib import Path

import yaml
from yaml.tokens import AliasToken, AnchorToken, KeyToken, ScalarToken, TagToken


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
WORKFLOW_PATTERNS = ("*.yml", "*.yaml")
PERMISSION_FIXTURES = ROOT / "ci" / "fixtures" / "workflow-permission-contract"
SHA_PIN = re.compile(r"^[a-z\d_.-]+(?:/[a-z\d_.-]+)+@[a-f\d]{40}\s+# v\d", re.MULTILINE)
JOB_HEADER = re.compile(r"^ {2}(?P<name>[A-Za-z0-9_-]+):\s*$")
STEP_HEADER = re.compile(r"^(?P<indent>\s*)-\s")
GO_MODULE_REQUIREMENT = re.compile(
    r"^(?P<module>[A-Za-z0-9][A-Za-z0-9._/-]*)\s+v"
    r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?:\s+//.*)?$"
)
PCRE2_SHA256 = "47fe8c99461250d42f89e6e8fdaeba9da057855d06eb7fc08d9ca03fd08d7bc7"
PROTECTED_NGINX_BROKER_CALLER_WORKFLOW = "run-protected-nginx-root-broker.yml"
PROTECTED_NGINX_BROKER_REUSABLE_REFERENCE = (
    "Easton97-Jens/ModSecurity-conector/.github/workflows/nginx-root-broker.yml@"
    "e06254ea9622d214a9030b9ba786756560ace417"
)
PROTECTED_NGINX_BROKER_CALLER_MASTER_GATE_TERMS = frozenset(
    {
        "github.event_name == 'workflow_dispatch'",
        "github.repository == 'Easton97-Jens/ModSecurity-conector'",
        "github.event.repository.fork == false",
        "github.ref == 'refs/heads/master'",
        "github.event.repository.default_branch == 'master'",
    }
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
    ("update-actions-versions.yml", "update-actions-versions"): {
        "contents": "write",
        "pull-requests": "write",
        "actions": "write",
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


def mapping_after(lines: list[str], index: int, indent: int) -> dict[str, str]:
    """Return the scalar mapping immediately below a known indentation level."""

    mapping: dict[str, str] = {}
    child_prefix = " " * (indent + 2)
    for line in lines[index + 1 :]:
        if not line.strip():
            continue
        if not line.startswith(child_prefix):
            break
        match = re.match(rf"^{re.escape(child_prefix)}(?P<key>[A-Za-z0-9_-]+):\s*(?P<value>[^\s#]+)", line)
        if match is None:
            continue
        mapping[match.group("key")] = match.group("value")
    return mapping


def top_level_permissions(text: str) -> dict[str, str]:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line == "permissions:":
            return mapping_after(lines, index, 0)
    raise AssertionError("workflow has no top-level permissions mapping")


def job_blocks(text: str) -> dict[str, str]:
    """Split the top-level jobs mapping without adding a YAML dependency."""

    lines = text.splitlines()
    blocks: dict[str, list[str]] = {}
    current: str | None = None
    in_jobs = False
    for line in lines:
        if line == "jobs:":
            in_jobs = True
            continue
        if not in_jobs:
            continue
        if line and not line.startswith(" "):
            break
        match = JOB_HEADER.match(line)
        if match:
            current = match.group("name")
            blocks[current] = [line]
        elif current is not None:
            blocks[current].append(line)
    return {name: "\n".join(block) for name, block in blocks.items()}


def job_permissions(job: str) -> dict[str, str]:
    lines = job.splitlines()
    for index, line in enumerate(lines):
        if line == "    permissions:":
            return mapping_after(lines, index, 4)
    return {}


def job_if_expression(job: str) -> str | None:
    """Return the unique job-level ``if`` expression without YAML evaluation."""

    lines = job.splitlines()
    expressions: list[str] = []
    for index, line in enumerate(lines):
        if not line.startswith("    if:"):
            continue
        value = line.removeprefix("    if:").strip()
        if value in {">", ">-", "|", "|-"}:
            continuation: list[str] = []
            for candidate in lines[index + 1 :]:
                if candidate.startswith("      "):
                    continuation.append(candidate.strip())
                    continue
                if candidate.strip():
                    break
            value = " ".join(continuation)
        expressions.append(value)
    if len(expressions) != 1:
        return None
    expression = expressions[0]
    if expression.startswith("${{") and expression.endswith("}}"):
        expression = expression.removeprefix("${{").removesuffix("}}").strip()
    return " ".join(expression.split())


def has_exact_master_only_gate(job: str, extra_terms: set[str]) -> bool:
    """Require a conjunction of the fixed master gate and approved job clauses."""

    expression = job_if_expression(job)
    if expression is None:
        return False
    terms = {term.strip() for term in expression.split("&&")}
    return terms == PROTECTED_NGINX_BROKER_CALLER_MASTER_GATE_TERMS | extra_terms


def job_direct_key_count(job: str, key: str) -> int:
    """Count direct job mapping keys, including malformed duplicate keys."""

    return sum(line.startswith(f"    {key}:") for line in job.splitlines())


def job_with_keys(job: str) -> list[str] | None:
    """Return direct ``with`` keys only when the job has one such mapping."""

    lines = job.splitlines()
    with_indexes = [index for index, line in enumerate(lines) if line.startswith("    with:")]
    if len(with_indexes) != 1:
        return None
    keys: list[str] = []
    for line in lines[with_indexes[0] + 1 :]:
        if not line.strip():
            continue
        if len(line) - len(line.lstrip()) <= 4:
            break
        match = re.match(r"^      (?P<key>[A-Za-z_][A-Za-z0-9_-]*):", line)
        if match is not None:
            keys.append(match.group("key"))
    return keys


def checkout_step_blocks(text: str) -> list[str]:
    """Return each checkout step through the next step at the same indent."""

    lines = text.splitlines()
    blocks: list[str] = []
    for index, line in enumerate(lines):
        if "uses: actions/checkout@" not in line:
            continue
        start = index
        while start > 0 and STEP_HEADER.match(lines[start]) is None:
            start -= 1
        step_match = STEP_HEADER.match(lines[start])
        if step_match is None:
            raise AssertionError(f"checkout is not in a workflow step: {line}")
        step_indent = len(step_match.group("indent"))
        end = len(lines)
        for candidate in range(start + 1, len(lines)):
            candidate_match = STEP_HEADER.match(lines[candidate])
            if candidate_match and len(candidate_match.group("indent")) <= step_indent:
                end = candidate
                break
        blocks.append("\n".join(lines[start:end]))
    return blocks


def fixture_violations(text: str) -> set[str]:
    """Model the policy boundary exercised by the safe/unsafe fixtures."""

    violations: set[str] = set()
    if "pull_request_target:" in text:
        violations.add("pull_request_target")
    if top_level_permissions(text) != {"contents": "read"}:
        violations.add("top_level_permissions")
    if "secrets." in text:
        violations.add("secret_reference")
    for job in job_blocks(text).values():
        permissions = job_permissions(job)
        checkout_steps = checkout_step_blocks(job)
        if any("persist-credentials: false" not in step for step in checkout_steps):
            violations.add("persisted_credentials")
        if (
            any(value == "write" for value in permissions.values())
            and "submodules: recursive" in job
            and "make quick-check" in job
        ):
            violations.add("privileged_submodule_execution")
    return violations


def yaml_security_errors(text: str) -> list[str]:
    """Reject YAML indirection without treating block-scalar code as YAML."""

    errors: list[str] = []
    key_token_seen = False
    try:
        for token in yaml.scan(text):
            line_number = token.start_mark.line + 1
            if isinstance(token, KeyToken):
                key_token_seen = True
                continue
            if isinstance(token, AnchorToken):
                errors.append(f"line {line_number}: anchor")
            elif isinstance(token, AliasToken):
                errors.append(f"line {line_number}: alias")
            elif isinstance(token, TagToken):
                errors.append(f"line {line_number}: tag")
            elif (
                key_token_seen
                and isinstance(token, ScalarToken)
                and token.style is None
                and token.value == "<<"
            ):
                errors.append(f"line {line_number}: merge key")
            if not isinstance(token, KeyToken):
                key_token_seen = False
    except yaml.YAMLError as exc:
        line_number = getattr(getattr(exc, "problem_mark", None), "line", 0) + 1
        errors.append(f"line {line_number}: malformed YAML")
    return errors


def protected_nginx_broker_caller_errors(text: str) -> list[str]:
    """Return exact trust-contract violations for the protected dispatch caller."""

    errors: list[str] = []
    if not text.startswith("name: Protected NGINX Root Broker Lifecycle\n"):
        errors.append("caller workflow name")
    trigger_match = re.search(r"(?ms)^on:\n(?P<body>.*?)(?=^permissions:\n)", text)
    if trigger_match is None:
        errors.append("caller trigger section")
        trigger_body = ""
    else:
        trigger_body = trigger_match.group("body")
        triggers = re.findall(r"(?m)^  ([A-Za-z_][A-Za-z0-9_-]*):", trigger_body)
        if triggers != ["workflow_dispatch"]:
            errors.append("caller must have only workflow_dispatch")
        inputs = re.findall(r"(?m)^      ([A-Za-z_][A-Za-z0-9_-]*):", trigger_body)
        if inputs != ["parent_head_sha"]:
            errors.append("caller must expose only parent_head_sha")
        if "        required: true" not in trigger_body or "        type: string" not in trigger_body:
            errors.append("caller parent_head_sha must be required string")
    for forbidden in (
        "pull_request:",
        "pull_request_target:",
        "push:",
        "workflow_call:",
        "repository_dispatch:",
        "workflow_run:",
    ):
        if forbidden in text:
            errors.append(f"forbidden trigger {forbidden}")
    try:
        if top_level_permissions(text) != {"contents": "read"}:
            errors.append("caller top-level permissions")
    except AssertionError:
        errors.append("caller top-level permissions")
    if (
        "  group: protected-nginx-root-broker-caller" not in text
        or "  cancel-in-progress: false" not in text
    ):
        errors.append("caller non-cancelling concurrency")
    expected_jobs = {
        "prepare-manifests",
        "run-no-crs-broker",
        "run-with-crs-broker",
        "verify-evidence",
        "result",
    }
    jobs = job_blocks(text)
    if set(jobs) != expected_jobs:
        errors.append("caller job inventory")
    expected_gate_extras = {
        "prepare-manifests": set(),
        "run-no-crs-broker": {"needs.prepare-manifests.result == 'success'"},
        "run-with-crs-broker": {"needs.prepare-manifests.result == 'success'"},
        "verify-evidence": {
            "always()",
            "needs.prepare-manifests.result == 'success'",
            "needs.run-no-crs-broker.result == 'success'",
            "needs.run-with-crs-broker.result == 'success'",
        },
        "result": {"always()"},
    }
    for name, job in jobs.items():
        if job_permissions(job) != {"contents": "read"}:
            errors.append(f"caller job permissions {name}")
        if not has_exact_master_only_gate(job, expected_gate_extras.get(name, set())):
            errors.append(f"caller master-only gate {name}")
    if "matrix:" in text or "strategy:" in text:
        errors.append("caller must not use a dynamic matrix")
    protected_calls = [
        line.strip()
        for line in text.splitlines()
        if line.strip().startswith("uses: Easton97-Jens/ModSecurity-conector/.github/workflows/")
    ]
    if protected_calls != [
        f"uses: {PROTECTED_NGINX_BROKER_REUSABLE_REFERENCE}",
        f"uses: {PROTECTED_NGINX_BROKER_REUSABLE_REFERENCE}",
    ]:
        errors.append("caller immutable protected broker reference")
    required_no_crs = (
        "      caller_manifest_artifact: protected-nginx-caller-${{ github.run_id }}-${{ github.run_attempt }}-no-crs",
        "      parent_head_sha: ${{ inputs.parent_head_sha }}",
        "      framework_sha: c71e15db7b7517b237add9fa09b3493e7bc93627",
        "      protected_broker_sha: e06254ea9622d214a9030b9ba786756560ace417",
        "      matrix_variant: no-crs",
        "      run_id: protected-nginx-root-${{ github.run_id }}-${{ github.run_attempt }}-no-crs",
    )
    required_with_crs = tuple(item.replace("no-crs", "with-crs") for item in required_no_crs)
    required_with_crs = tuple(
        item.replace("matrix_variant: with-crs", "matrix_variant: with-crs")
        for item in required_with_crs
    )
    expected_broker_input_keys = [
        "caller_manifest_artifact",
        "parent_head_sha",
        "framework_sha",
        "protected_broker_sha",
        "matrix_variant",
        "run_id",
    ]
    for job_name, requirements in (
        ("run-no-crs-broker", required_no_crs),
        ("run-with-crs-broker", required_with_crs),
    ):
        job = jobs.get(job_name, "")
        if job_direct_key_count(job, "uses") != 1:
            errors.append(f"caller immutable protected broker reference {job_name}")
        if job_direct_key_count(job, "with") != 1 or job_with_keys(job) != expected_broker_input_keys:
            errors.append(f"caller exact broker input keys {job_name}")
        for required in requirements:
            if required not in job:
                errors.append(f"caller fixed broker input {job_name} {required}")
    if "policy_profile:" in trigger_body or "matrix_variant:" in trigger_body:
        errors.append("caller exposes a dynamic profile or variant")
    prepare = jobs.get("prepare-manifests", "")
    if "create-manifests" not in prepare or '--target-sha "$TARGET_PARENT_SHA"' not in prepare:
        errors.append("caller manifest preparation")
    if "--output-root" in prepare:
        errors.append("caller manifest path must be derived from the trusted runner temporary directory")
    if prepare.count("caller-manifest.json") != 2:
        errors.append("caller must upload exactly two single-file manifests")
    if any(
        pattern in text
        for pattern in (
            "uses: ./",
            "@master",
            "@fix/",
            "secrets.",
            "${{ secrets.",
            "sudo",
            "git checkout \"$TARGET_PARENT_SHA\"",
            "git checkout '${TARGET_PARENT_SHA}'",
            "ref: ${{ inputs.parent_head_sha }}",
            "python3 \"$TARGET_PARENT_SHA\"",
            "source \"$TARGET_PARENT_SHA\"",
            "make $TARGET_PARENT_SHA",
        )
    ):
        errors.append("caller target-code or privilege boundary")
    evidence = jobs.get("verify-evidence", "")
    if (
        "verify-evidence" not in evidence
        or "Download no-CRS broker evidence" not in evidence
        or "Download OWASP CRS broker evidence" not in evidence
    ):
        errors.append("caller evidence readback")
    if "--no-crs-directory" in evidence or "--with-crs-directory" in evidence:
        errors.append("caller evidence paths must be derived from the trusted runner temporary directory")
    result = jobs.get("result", "")
    for required in (
        "always()",
        '"$PREPARE_RESULT" != success',
        '"$NO_CRS_RESULT" != success',
        '"$WITH_CRS_RESULT" != success',
        '"$EVIDENCE_RESULT" != success',
        "exit 1",
    ):
        if required not in result:
            errors.append("caller fail-closed result")
            break
    return errors


def go_module_requirements(text: str) -> dict[str, tuple[int, int, int]]:
    """Return stable semantic versions declared in Go require directives."""

    requirements: dict[str, tuple[int, int, int]] = {}
    in_require_block = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line == "require (":
            in_require_block = True
            continue
        if in_require_block and line == ")":
            in_require_block = False
            continue
        if in_require_block:
            candidate = line
        elif line.startswith("require "):
            candidate = line.removeprefix("require ").strip()
        else:
            continue
        match = GO_MODULE_REQUIREMENT.fullmatch(candidate)
        if match is None:
            continue
        requirements[match.group("module")] = tuple(
            int(match.group(part)) for part in ("major", "minor", "patch")
        )
    return requirements


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
                if reference.startswith(
                    "Easton97-Jens/ModSecurity-conector/.github/workflows/"
                ):
                    self.assertEqual(path.name, PROTECTED_NGINX_BROKER_CALLER_WORKFLOW)
                    self.assertEqual(reference, PROTECTED_NGINX_BROKER_REUSABLE_REFERENCE)
                    continue
                self.assertRegex(reference, SHA_PIN, f"{path}: {line}")
                self.assertIn(reference.split("@", 1)[1].split()[0], recorded_shas, f"{path}: {line}")

    def test_workflow_and_lock_yaml_reject_forbidden_indirection(self) -> None:
        unsafe = """\
defaults: &unsafe
  run:
    shell: bash
jobs:
  reuse:
    <<: *unsafe
    value: !unsafe value
"""
        self.assertEqual(
            yaml_security_errors(unsafe),
            ["line 1: anchor", "line 6: merge key", "line 6: alias", "line 7: tag"],
        )
        checked_paths = [*self.workflow_paths(), ROOT / "ci/tooling/security-tools.lock.yml"]
        for path in checked_paths:
            with self.subTest(path=path):
                self.assertEqual(yaml_security_errors(path.read_text(encoding="utf-8")), [])

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

    def test_envoy_ext_proc_dependency_floors(self) -> None:
        requirements = go_module_requirements(
            (ROOT / "connectors" / "envoy" / "ext_proc" / "go.mod").read_text(encoding="utf-8")
        )
        security_floors = {
            "google.golang.org/grpc": (1, 82, 1),
            "golang.org/x/net": (0, 56, 0),
            "golang.org/x/sys": (0, 46, 0),
            "golang.org/x/text": (0, 39, 0),
        }
        for module, floor in security_floors.items():
            with self.subTest(module=module):
                self.assertIn(module, requirements)
                self.assertGreaterEqual(requirements[module], floor)

    def test_codeql_uses_central_go_file_and_bounded_cpp_scope(self) -> None:
        text = self.workflow("ci-security-codeql.yml")
        self.assertEqual(text.count("go-version-file: .go-version"), 2)
        self.assertEqual(text.count("check-latest: false"), 2)
        self.assertNotIn("go-version:", text)
        self.assertIn("connectors/envoy/ext_proc", text)
        self.assertIn("connectors/traefik/native_middleware", text)
        self.assertIn("Fuzz Traefik UDS frame parser", text)
        self.assertIn("-fuzz='^FuzzUDSFrameAndResult$'", text)
        self.assertIn("-fuzztime=15s -parallel=1", text)
        self.assertIn("make check-common-helpers-c17", text)
        self.assertIn("Fuzz Common HTTP header parser", text)
        self.assertIn("make check-common-http-header-fuzz", text)

    def test_codeql_components_match_the_central_lock_atomically(self) -> None:
        """Keep every CodeQL component on the one locked release."""

        lock_text = (ROOT / "ci" / "tooling" / "security-tools.lock.yml").read_text(encoding="utf-8")
        lock_entry = re.search(
            r"^  github/codeql-action:\n"
            r"    version: (?P<version>v[^\s]+)\n"
            r"    commit_sha: (?P<sha>[a-f\d]{40})\n"
            r"    upstream: https://github\.com/github/codeql-action$",
            lock_text,
            re.MULTILINE,
        )
        self.assertIsNotNone(lock_entry)
        assert lock_entry is not None
        expected = (lock_entry.group("sha"), lock_entry.group("version"))

        codeql_jobs = 0
        for job_name, job in self.jobs("ci-security-codeql.yml").items():
            init_references = re.findall(r"github/codeql-action/init@([a-f\d]{40})\s+# (v[^\s]+)", job)
            analyze_references = re.findall(r"github/codeql-action/analyze@([a-f\d]{40})\s+# (v[^\s]+)", job)
            if not init_references and not analyze_references:
                continue
            codeql_jobs += 1
            self.assertEqual(init_references, [expected], f"{job_name}: init")
            self.assertEqual(analyze_references, [expected], f"{job_name}: analyze")

        self.assertEqual(codeql_jobs, 4)
        for workflow_name in ("ci-security-osv.yml", "ci-security-scorecard.yml"):
            upload_references = re.findall(
                r"github/codeql-action/upload-sarif@([a-f\d]{40})\s+# (v[^\s]+)",
                self.workflow(workflow_name),
            )
            self.assertEqual(upload_references, [expected], workflow_name)

    def test_development_pyyaml_dependency_is_exact_safe_pin(self) -> None:
        text = (ROOT / "requirements-dev.txt").read_text(encoding="utf-8")
        self.assertIn("PyYAML==6.0.3", text)
        self.assertNotIn("PyYAML>=", text)

    def test_makefile_preserves_the_framework_pcre2_default_boundary(self) -> None:
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        self.assertIn(
            "ifneq ($(origin PCRE2_SHA256),undefined)\nexport PCRE2_SHA256\nendif",
            makefile,
        )
        self.assertNotIn(
            "export PCRE2_VERSION\nexport PCRE2_SOURCE_URL\nexport PCRE2_SHA256\nexport PCRE2_SHA256_URL",
            makefile,
        )
        target = (
            "print-pcre2-export:\n"
            "\t@if printenv PCRE2_SHA256 >/dev/null 2>&1; then "
            "printf 'present:<%s>' \"$$PCRE2_SHA256\"; else printf absent; fi"
        )
        environment = dict(os.environ)
        environment.pop("PCRE2_SHA256", None)
        command = ["make", "-s", f"--eval={target}", "print-pcre2-export"]
        absent = subprocess.run(
            command,
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(absent.stdout, "absent")

        empty_environment = {**environment, "PCRE2_SHA256": ""}
        environment_empty = subprocess.run(
            command,
            cwd=ROOT,
            env=empty_environment,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(environment_empty.stdout, "present:<>")

        explicit_empty = subprocess.run(
            ["make", "-s", "PCRE2_SHA256=", f"--eval={target}", "print-pcre2-export"],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(explicit_empty.stdout, "present:<>")

        explicit_digest = subprocess.run(
            ["make", "-s", f"PCRE2_SHA256={PCRE2_SHA256}", f"--eval={target}", "print-pcre2-export"],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(explicit_digest.stdout, f"present:<{PCRE2_SHA256}>")

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

    def test_verified_report_governance_stays_lightweight(self) -> None:
        """Keep expensive runtime evidence and report production local-only."""

        text = self.workflow("verified-report-governance.yml")
        jobs = self.jobs("verified-report-governance.yml")
        self.assertEqual(set(jobs), {"report-governance"})
        job = jobs["report-governance"]
        self.assertIn("timeout-minutes: 20", job)
        self.assertIn("make report-governance", job)
        for forbidden in (
            "verified-report-run",
            "verified-report-evidence-gate",
            "refresh-all-reports",
            "generate-system-environment-proof",
            "runtime-matrix-all",
            "upload-artifact",
            "ALLOW_RUNTIME_DOWNLOADS",
            "ALLOW_RUNTIME_BUILDS",
        ):
            self.assertNotIn(forbidden, text)

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

    def test_all_checkouts_disable_persisted_credentials(self) -> None:
        for path in self.workflow_paths():
            checkout_steps = checkout_step_blocks(path.read_text(encoding="utf-8"))
            for checkout_step in checkout_steps:
                self.assertIn("persist-credentials: false", checkout_step, path.name)

    def test_trusted_nginx_root_broker_has_no_pr_code_at_root_boundary(self) -> None:
        text = self.workflow("nginx-root-broker.yml")
        self.assertIn("workflow_call:", text)
        self.assertNotIn("pull_request:", text)
        self.assertNotIn("pull_request_target:", text)
        self.assertIn("github.workflow_ref", text)
        self.assertIn('git merge-base --is-ancestor "$BROKER_SHA" FETCH_HEAD', text)
        self.assertIn('git rev-parse "$BROKER_SHA:ci/runtime/broker/nginx_root_broker.py"', text)
        self.assertIn("git hash-object ci/runtime/broker/nginx_root_broker.py", text)
        self.assertIn("prepare-fresh-crs-source.sh", text)
        self.assertIn("prepare-crs-bundle", text)
        self.assertIn("verify-runtime-profile", text)
        self.assertIn("cleanup.json", text)
        self.assertIn("sudo -- /usr/bin/python3 -I ci/runtime/broker/nginx_root_broker.py action", text)
        self.assertNotIn("uses: ./", text)
        for forbidden in (
            "sudo -E",
            "sudo sh -c",
            "sudo bash -c",
            "shell: bash -c",
            "--broker-parent",
            "--staging-root",
            "--runtime-snapshot",
            "sudo python",
        ):
            self.assertNotIn(forbidden, text)

    def test_protected_master_caller_is_exactly_pinned_and_fail_closed(self) -> None:
        text = self.workflow(PROTECTED_NGINX_BROKER_CALLER_WORKFLOW)
        self.assertEqual(protected_nginx_broker_caller_errors(text), [])
        mutations = {
            "broker master ref": (
                PROTECTED_NGINX_BROKER_REUSABLE_REFERENCE,
                PROTECTED_NGINX_BROKER_REUSABLE_REFERENCE.replace(
                    "@e06254ea9622d214a9030b9ba786756560ace417", "@master"
                ),
            ),
            "broker branch ref": (
                PROTECTED_NGINX_BROKER_REUSABLE_REFERENCE,
                PROTECTED_NGINX_BROKER_REUSABLE_REFERENCE.replace(
                    "@e06254ea9622d214a9030b9ba786756560ace417", "@fix/unsafe"
                ),
            ),
            "local reusable workflow": (
                PROTECTED_NGINX_BROKER_REUSABLE_REFERENCE,
                "./.github/workflows/nginx-root-broker.yml",
            ),
            "wrong broker SHA": (
                PROTECTED_NGINX_BROKER_REUSABLE_REFERENCE,
                PROTECTED_NGINX_BROKER_REUSABLE_REFERENCE.replace(
                    "e06254ea9622d214a9030b9ba786756560ace417",
                    "0" * 40,
                ),
            ),
            "duplicate broker reference": (
                f"    uses: {PROTECTED_NGINX_BROKER_REUSABLE_REFERENCE}",
                "\n".join(
                    (
                        f"    uses: {PROTECTED_NGINX_BROKER_REUSABLE_REFERENCE}",
                        f"    uses: {PROTECTED_NGINX_BROKER_REUSABLE_REFERENCE}",
                    )
                ),
            ),
            "mutable Framework SHA": (
                "framework_sha: c71e15db7b7517b237add9fa09b3493e7bc93627",
                "framework_sha: 0" * 40,
            ),
            "duplicate broker input": (
                "      framework_sha: c71e15db7b7517b237add9fa09b3493e7bc93627",
                "\n".join(
                    (
                        "      framework_sha: c71e15db7b7517b237add9fa09b3493e7bc93627",
                        "      framework_sha: c71e15db7b7517b237add9fa09b3493e7bc93627",
                    )
                ),
            ),
            "missing master guard": (
                "github.ref == 'refs/heads/master' &&\n",
                "",
            ),
            "short-circuited master guard": (
                "github.event_name == 'workflow_dispatch'",
                "true || github.event_name == 'workflow_dispatch'",
            ),
            "pull request trigger": (
                "  workflow_dispatch:\n",
                "  pull_request:\n  workflow_dispatch:\n",
            ),
            "pull request target trigger": (
                "  workflow_dispatch:\n",
                "  pull_request_target:\n  workflow_dispatch:\n",
            ),
            "push trigger": (
                "  workflow_dispatch:\n",
                "  push:\n  workflow_dispatch:\n",
            ),
            "additional workflow input": (
                "      parent_head_sha:\n",
                "      policy_profile:\n        required: true\n        type: string\n      parent_head_sha:\n",
            ),
            "dynamic variant input": (
                "      parent_head_sha:\n",
                "      matrix_variant:\n        required: true\n        type: string\n      parent_head_sha:\n",
            ),
            "target checkout": (
                "          ref: ${{ github.sha }}",
                "          ref: ${{ inputs.parent_head_sha }}",
            ),
            "target execution": (
                "          set -euo pipefail",
                "          set -euo pipefail\n          python3 \"$TARGET_PARENT_SHA\"",
            ),
            "caller-selected manifest path": (
                '            --with-crs-run-id "$WITH_CRS_RUN_ID"',
                '            --with-crs-run-id "$WITH_CRS_RUN_ID" \\\n            --output-root "$RUNNER_TEMP/unsafe"',
            ),
            "caller-selected evidence path": (
                "          python3 ci/runtime/broker/protected_nginx_broker_caller.py verify-evidence \\\n",
                "          python3 ci/runtime/broker/protected_nginx_broker_caller.py verify-evidence \\\n"
                '            --no-crs-directory "$RUNNER_TEMP/unsafe" \\\n',
            ),
            "write permission": (
                "permissions:\n  contents: read",
                "permissions:\n  contents: write",
            ),
            "secret reference": (
                "          set -euo pipefail",
                "          set -euo pipefail\n          printf '%s\\n' \"${{ secrets.CALLER_SECRET }}\"",
            ),
            "sudo in caller": (
                "          set -euo pipefail",
                "          set -euo pipefail\n          sudo true",
            ),
            "result masks a failed broker": (
                '"$NO_CRS_RESULT" != success',
                '"$NO_CRS_RESULT" = success',
            ),
        }
        for name, (original, replacement) in mutations.items():
            with self.subTest(name=name):
                self.assertIn(original, text)
                mutated = text.replace(original, replacement, 1)
                self.assertNotEqual(protected_nginx_broker_caller_errors(mutated), [])

    def test_untrusted_pull_request_model(self) -> None:
        sarif_write_jobs = {
            key for key, value in EXPECTED_WRITE_PERMISSIONS.items() if value.get("security-events") == "write"
        }
        for path in self.workflow_paths():
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("pull_request_target:", text, path.name)
            self.assertNotIn("workflow_run:", text, path.name)
            if not re.search(r"(?m)^\s*pull_request:", text):
                continue
            self.assertNotIn("secrets.", text, path.name)
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
        jobs = self.jobs("update-submodules.yml")
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
        self.assertIn("needs: resolve-submodule-update", jobs["validate-submodule-update"])
        self.assertIn("submodules: recursive", jobs["validate-submodule-update"])
        self.assertIn("make quick-check", jobs["validate-submodule-update"])
        dependency_install = (
            "python3 -m pip install --disable-pip-version-check --only-binary=:all: "
            "--require-hashes --requirement "
            "ci/requirements/update-submodules-validation-linux-x86_64.txt"
        )
        dependency_lock = (
            ROOT / "ci" / "requirements" / "update-submodules-validation-linux-x86_64.txt"
        ).read_text(encoding="utf-8")
        self.assertIn("PyYAML==6.0.3", dependency_lock)
        self.assertIn(
            "--hash=sha256:c458b6d084f9b935061bc36216e8a69a7e293a2f1e68bf956dcd9e6cbcd143f5",
            dependency_lock,
        )
        self.assertNotIn("PyYAML>=", dependency_lock)
        self.assertIn(dependency_install, jobs["validate-submodule-update"])
        self.assertIn(
            f'run: "{dependency_install}"',
            jobs["validate-submodule-update"],
        )
        self.assertLess(
            jobs["validate-submodule-update"].index("Verify Python interpreter contract"),
            jobs["validate-submodule-update"].index(dependency_install),
        )
        self.assertLess(
            jobs["validate-submodule-update"].index(dependency_install),
            jobs["validate-submodule-update"].index("make quick-check"),
        )
        self.assertNotIn("GH_TOKEN", jobs["validate-submodule-update"])
        self.assertNotIn("secrets.", jobs["validate-submodule-update"])

        publisher = jobs["create-submodule-update-pr"]
        self.assertIn("submodules: false", publisher)
        self.assertIn("persist-credentials: false", publisher)
        self.assertIn("git ls-remote --exit-code", publisher)
        self.assertIn("git update-index --add --cacheinfo", publisher)
        self.assertIn("GH_TOKEN: ${{ github.token }}", publisher)
        self.assertNotIn("submodules: recursive", publisher)
        self.assertNotIn("git submodule", publisher)
        self.assertNotIn("make quick-check", publisher)

    def test_manual_actions_updater_uses_a_trusted_default_branch(self) -> None:
        job = self.jobs("update-actions-versions.yml")["update-actions-versions"]
        self.assertIn(
            "if: github.ref == format('refs/heads/{0}', github.event.repository.default_branch)",
            job,
        )
        checkouts = checkout_step_blocks(job)
        self.assertEqual(len(checkouts), 1)
        self.assertIn("ref: ${{ github.event.repository.default_branch }}", checkouts[0])
        self.assertIn("persist-credentials: false", checkouts[0])

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
        self.assertIn("UPDATE_BRANCH: automation/update-python-314", publisher)
        self.assertIn('PR_TITLE: "chore(ci): propose Python 3.14 patch update"', publisher)
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
        self.assertIn('gh api --method GET "repos/$GITHUB_REPOSITORY/pulls/$existing_pr" --jq \'.auto_merge\'', publisher)
        self.assertIn('if [ "$auto_merge" != "null" ]; then', publisher)
        self.assertIn("git fetch --no-tags origin \"$UPDATE_BRANCH\"", publisher)
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
        self.assertEqual(job_permissions(jobs["validate-go-patch"]), {"contents": "read"})
        resolver = jobs["resolve-go-patch"]
        self.assertIn("go-version-file: .go-version", resolver)
        self.assertIn("check-latest: false", resolver)
        self.assertIn("cache: false", resolver)
        self.assertIn("make check-go-version-contract", resolver)
        self.assertIn('scripts/update-go-version.py --check --json', resolver)

        candidate = jobs["validate-go-patch"]
        self.assertIn("go-version: ${{ needs.resolve-go-patch.outputs.version }}", candidate)
        self.assertIn("GOTOOLCHAIN: local", candidate)
        self.assertEqual(candidate.count("go test -mod=readonly ./..."), 2)
        self.assertEqual(candidate.count("go build -mod=readonly ./..."), 2)
        self.assertEqual(candidate.count("go mod verify"), 2)
        self.assertIn('scripts/update-go-version.py --check --expected-version "$CANDIDATE_VERSION" --json', candidate)
        self.assertIn("tests.test_update_go_version", candidate)
        self.assertIn("tests.test_go_version_contract", candidate)

        publisher = jobs["create-go-update-pr"]
        self.assertEqual(
            job_permissions(publisher),
            {"contents": "write", "pull-requests": "write"},
        )
        self.assertNotIn("actions: write", publisher)
        self.assertNotIn("actions/setup-go@", publisher)
        self.assertNotIn("submodules: recursive", publisher)
        self.assertNotIn("git submodule", publisher)
        self.assertNotIn("make ", publisher)
        self.assertNotIn("--force", publisher)
        self.assertNotIn("--force-with-lease", publisher)
        self.assertIn('python3 scripts/update-go-version.py --update --expected-version "$CANDIDATE_VERSION" --json', publisher)
        self.assertIn("UPDATE_BRANCH: automation/update-go-126", publisher)
        self.assertIn('PR_TITLE: "chore(ci): propose Go 1.26 patch update"', publisher)
        self.assertIn("if [ \"$changed_paths\" != \".go-version\" ]; then", publisher)
        self.assertIn('git update-index --add --cacheinfo 100644 "$candidate_blob" .go-version', publisher)
        self.assertIn("git push origin \"$UPDATE_BRANCH\"", publisher)
        self.assertIn("--draft", publisher)
        self.assertIn("gh pr edit \"$existing_pr\"", publisher)
        self.assertIn("scripts/select-python-update-pr.py", publisher)
        self.assertIn("## English", publisher)
        self.assertIn("## Deutsch", publisher)
        self.assertIn("Module directives: unchanged", publisher)

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
