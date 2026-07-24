"""Focused static contracts for the repository's CI-security workflows."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


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
                self.assertRegex(reference, SHA_PIN, f"{path}: {line}")
                self.assertIn(reference.split("@", 1)[1].split()[0], recorded_shas, f"{path}: {line}")

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

    def test_all_checkouts_disable_persisted_credentials(self) -> None:
        for path in self.workflow_paths():
            checkout_steps = checkout_step_blocks(path.read_text(encoding="utf-8"))
            for checkout_step in checkout_steps:
                self.assertIn("persist-credentials: false", checkout_step, path.name)

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
