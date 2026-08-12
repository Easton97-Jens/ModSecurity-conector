"""Focused static contracts for the repository's CI-security workflows."""

from __future__ import annotations

import ast
import os
import re
import subprocess
import tempfile
import unittest
from hashlib import sha256
from pathlib import Path

import yaml
from yaml.tokens import AliasToken, AnchorToken, KeyToken, ScalarToken, TagToken


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
WORKFLOW_PATTERNS = ("*.yml", "*.yaml")
PERMISSION_FIXTURES = ROOT / "ci" / "fixtures" / "workflow-permission-contract"
SHA_PIN = re.compile(r"^[a-z\d_.-]+(?:/[a-z\d_.-]+)+@[a-f\d]{40}\s+# v\d", re.MULTILINE)
SHELL_CONTINUATION = re.compile(r"\\\r?\n[ \t]*")
JOB_HEADER = re.compile(r"^ {2}(?P<name>[A-Za-z0-9_-]+):\s*$")
STEP_HEADER = re.compile(r"^(?P<indent>\s*)-\s")
GO_MODULE_REQUIREMENT = re.compile(
    r"^(?P<module>[A-Za-z0-9][A-Za-z0-9._/-]*)\s+v"
    r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?:\s+//.*)?$"
)
PCRE2_SHA256 = "47fe8c99461250d42f89e6e8fdaeba9da057855d06eb7fc08d9ca03fd08d7bc7"
PROTECTED_NGINX_BROKER_CALLER_WORKFLOW = "run-protected-nginx-root-broker.yml"
PROTECTED_NGINX_BROKER_SHA = "49c40779a7b6de9f699391bcd524ea069787df42"
PROTECTED_NGINX_BROKER_FRAMEWORK_SHA = "03880bf66b3905940466ff10b3a431a27ecc6b26"
PROTECTED_NGINX_BROKER_REUSABLE_REFERENCE = (
    "Easton97-Jens/ModSecurity-conector/.github/workflows/nginx-root-broker.yml@"
    + PROTECTED_NGINX_BROKER_SHA
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
SUBMODULE_PUBLISHER_SHA256 = "c1e70a1d4481faafea81e4d33159388beb4471f709fe583fe8f8744be0977508"
READONLY_SUBMODULE_SANDBOX_CALL = " ".join(
    (
        "python3 ci/tools/prepare-readonly-submodule-validation-sandbox.py",
        '--source-root "$GITHUB_WORKSPACE"',
        '--framework-root "$GITHUB_WORKSPACE/modules/ModSecurity-test-Framework"',
        '--write-root "$write_root"',
        '--runner-temp "$RUNNER_TEMP"',
        "--validator-user modsecurity-validator",
        "--validator-group modsecurity-validator",
    )
)
READONLY_SUBMODULE_WRITE_ROOT = "$RUNNER_TEMP/modsecurity-readonly-validation.XXXXXX"
READONLY_SUBMODULE_EXTERNAL_ROOT = "$VALIDATION_WRITE_ROOT/external"
READONLY_SUBMODULE_NAMESPACE_CALL = " ".join(
    (
        "sudo -n python3 ci/tools/run-readonly-submodule-validation-namespace.py",
        '--source-root "$GITHUB_WORKSPACE"',
        '--framework-root "$GITHUB_WORKSPACE/modules/ModSecurity-test-Framework"',
        '--write-root "$VALIDATION_WRITE_ROOT"',
        '--external-root "$VALIDATION_WRITE_ROOT/external"',
        "--validator-user modsecurity-validator",
        "--validator-group modsecurity-validator",
        '--python "$EXPECTED_PYTHON"',
        '--namespace-parent "$namespace_parent"',
    )
)
READONLY_SUBMODULE_SANDBOX_READY = (
    "READONLY_SUBMODULE_VALIDATION_SANDBOX_READY\\ external=*\\ source_inventory_sha256=*"
)
READONLY_SUBMODULE_NAMESPACE_COMPLETE = "READONLY_SUBMODULE_VALIDATION_NAMESPACE_COMPLETE"
READONLY_SUBMODULE_VERIFY_GATE = (
    "if: ${{ always() && steps.prepare-readonly-candidate-sandbox.outcome == 'success' }}"
)
SUBMODULE_VALIDATE_ONLY_INPUT = """\
  workflow_dispatch:
    inputs:
      validate_only:
        description: Run the non-publishing exact-ref validator only.
        required: false
        default: false
        type: boolean
"""
SUBMODULE_VALIDATE_ONLY_EVENT = (
    "github.event_name == 'workflow_dispatch' && "
    "github.event.inputs.validate_only == 'true'"
)
SUBMODULE_VALIDATE_ONLY_REPOSITORY = "github.repository == 'Easton97-Jens/ModSecurity-conector'"
SUBMODULE_VALIDATE_ONLY_BRANCH = (
    "github.ref == 'refs/heads/fix/ci-enforce-readonly-submodule-validation'"
)
SUBMODULE_VALIDATE_ONLY_PROTECTED_FLAG = "github.ref_protected == true"
SUBMODULE_VALIDATE_ONLY_PROTECTED_MASTER = (
    "(github.ref == 'refs/heads/master' && "
    "github.event.repository.default_branch == 'master' && "
    f"{SUBMODULE_VALIDATE_ONLY_PROTECTED_FLAG})"
)
SUBMODULE_VALIDATE_ONLY_REF_ALLOWLIST = (
    f"({SUBMODULE_VALIDATE_ONLY_BRANCH} || {SUBMODULE_VALIDATE_ONLY_PROTECTED_MASTER})"
)
SUBMODULE_VALIDATE_ONLY_MANUAL_PREDICATE = (
    f"{SUBMODULE_VALIDATE_ONLY_EVENT} && "
    f"{SUBMODULE_VALIDATE_ONLY_REPOSITORY} && "
    "github.event.repository.fork == false && "
    f"{SUBMODULE_VALIDATE_ONLY_REF_ALLOWLIST}"
)
SUBMODULE_VALIDATE_ONLY_MASTER_EXCLUSION = (
    "(github.event_name != 'workflow_dispatch' || "
    "github.event.inputs.validate_only != 'true')"
)
SUBMODULE_VALIDATE_ONLY_CHECKOUT_REF = (
    f"ref: ${{{{ {SUBMODULE_VALIDATE_ONLY_MANUAL_PREDICATE} && github.sha || "
    "github.event.repository.default_branch }}"
)
SUBMODULE_RESOLVER_GATE = (
    f"{SUBMODULE_VALIDATE_ONLY_REPOSITORY} && github.event.repository.fork == false && "
    "( ( github.ref == 'refs/heads/master' && "
    "github.event.repository.default_branch == 'master' && "
    f"{SUBMODULE_VALIDATE_ONLY_MASTER_EXCLUSION} ) || "
    f"( {SUBMODULE_VALIDATE_ONLY_EVENT} && "
    f"( {SUBMODULE_VALIDATE_ONLY_BRANCH} || {SUBMODULE_VALIDATE_ONLY_PROTECTED_MASTER} ) ) )"
)
SUBMODULE_VALIDATOR_GATE = (
    "needs.resolve-submodule-update.result == 'success' && "
    "needs.resolve-submodule-update.outputs.changed == 'true'"
)
SUBMODULE_PUBLISHER_GATE = (
    "needs.resolve-submodule-update.result == 'success' && "
    "needs.resolve-submodule-update.outputs.changed == 'true' && "
    "needs.resolve-submodule-update.outputs.validation_only == 'false' && "
    "needs.validate-submodule-update.result == 'success'"
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

CONNECTOR_MODE_WORKFLOWS = {
    "test-connectors-no-crs-no-mrts.yml": {
        "name": "connector-tests-no-crs-no-mrts",
        "crs": "no-crs",
        "mrts": "no-mrts",
        "cells": {
            "apache": "runtime",
            "envoy": "runtime",
            "haproxy": "runtime",
            "lighttpd": "runtime",
            "traefik": "runtime",
        },
    },
    "test-connectors-with-crs-no-mrts.yml": {
        "name": "connector-tests-with-crs-no-mrts",
        "crs": "with-crs",
        "mrts": "no-mrts",
        "cells": {
            "apache": "runtime",
            "envoy": "contract",
            "haproxy": "runtime",
            "lighttpd": "contract",
            "traefik": "contract",
        },
    },
    "test-connectors-no-crs-with-mrts.yml": {
        "name": "connector-tests-no-crs-with-mrts",
        "crs": "no-crs",
        "mrts": "with-mrts",
        "cells": {
            "apache": "runtime",
            "envoy": "expected_unsupported",
            "haproxy": "runtime",
            "lighttpd": "expected_unsupported",
            "traefik": "expected_unsupported",
        },
    },
    "test-connectors-with-crs-with-mrts.yml": {
        "name": "connector-tests-with-crs-with-mrts",
        "crs": "with-crs",
        "mrts": "with-mrts",
        "cells": {
            "apache": "runtime",
            "envoy": "expected_unsupported",
            "haproxy": "runtime",
            "lighttpd": "expected_unsupported",
            "traefik": "expected_unsupported",
        },
    },
}
CONNECTOR_MODE_CONNECTORS = frozenset(
    {"apache", "envoy", "haproxy", "lighttpd", "traefik"}
)
CONNECTOR_MODE_COVERAGE_KINDS = frozenset(
    {"runtime", "contract", "expected_unsupported"}
)
CONNECTOR_MODE_FRAMEWORK_SHA = "209389022c942d83113f6be88bf31d25637352f0"
CONNECTOR_MODE_MRTS_SHA = "615b13bacbd008562c17408246c41ab27dca3104"
CONNECTOR_MODE_TRIGGER_PATHS = frozenset(
    {
        "tests/test_ci_security_workflows.py",
        "tests/test_python_version_contract.py",
        "ci/checks/common/check-python-version-contract.py",
        "ci/runtime/**",
        "connectors/apache/**",
        "connectors/envoy/**",
        "connectors/haproxy/**",
        "connectors/lighttpd/**",
        "connectors/traefik/**",
        "config/**",
        "Makefile",
        ".python-version",
        "modules/ModSecurity-test-Framework",
    }
)


def normalize_shell_script(script: str) -> str:
    """Normalize layout for static shell contracts without executing shell."""

    without_continuations = SHELL_CONTINUATION.sub(" ", script)
    return " ".join(without_continuations.split())


def has_exact_framework_gitlink_staging(script: str) -> bool:
    """Recognize only the narrowly scoped Framework gitlink index update."""

    normalized = normalize_shell_script(script)
    required = (
        'git update-index --add --cacheinfo '
        '"160000,$CANDIDATE_SHA,$SUBMODULE_PATH"'
    )
    return (
        required in normalized
        and "git add ." not in normalized
        and "git add -A" not in normalized
    )


def readonly_submodule_validator_errors(validator: str) -> list[str]:
    """Return violations of the root-side namespace validation boundary."""

    normalized = normalize_shell_script(validator)
    errors: list[str] = []
    required = (
        READONLY_SUBMODULE_SANDBOX_CALL,
        READONLY_SUBMODULE_NAMESPACE_CALL,
        "sudo -n groupadd --system modsecurity-validator",
        "sudo -n useradd --system --no-create-home --shell /usr/sbin/nologin",
        'sudo -n chown root:root "$write_root"',
        'sudo -n chmod 0711 "$write_root"',
        'namespace_parent="$(sudo -n mktemp -d /tmp/modsecurity-readonly-namespace.XXXXXX)"',
        'sudo -n chown root:modsecurity-validator "$namespace_parent"',
        'sudo -n chmod 0750 "$namespace_parent"',
        "trap cleanup_namespace_parent EXIT",
        'sudo -n rmdir -- "$namespace_parent"',
        "sandbox_prepare_output=\"$(sudo -n python3 ci/tools/prepare-readonly-submodule-validation-sandbox.py",
        READONLY_SUBMODULE_SANDBOX_READY,
        "id: prepare-readonly-candidate-sandbox",
        "id: run-readonly-candidate-namespace",
        "continue-on-error: true",
        READONLY_SUBMODULE_NAMESPACE_COMPLETE,
        "Verify candidate source inventory and external outputs",
        READONLY_SUBMODULE_VERIFY_GATE,
        "--verify",
        "VALIDATOR SOURCE MUTATION BLOCKED",
        "VALIDATOR WRITE-ROOT CONTRACT BLOCKED",
        "Enforce isolated candidate result after verification",
        "SANDBOX_PREPARE_RESULT: ${{ steps.prepare-readonly-candidate-sandbox.outcome }}",
        "CANDIDATE_RESULT: ${{ steps.run-readonly-candidate-namespace.outcome }}",
        'test "$SANDBOX_PREPARE_RESULT" = success',
        'test "$CANDIDATE_RESULT" = success',
        "sudo -n git -c core.hooksPath=/dev/null diff --check",
        'sudo -n git -c core.hooksPath=/dev/null -C "$SUBMODULE_PATH" diff --check',
        "printf 'write_root=%s\\n' \"$write_root\" >> \"$GITHUB_OUTPUT\"",
    )
    for term in required:
        if term not in normalized:
            errors.append(f"missing {term}")

    forbidden = (
        "setfacl",
        "getfacl",
        "unshare",
        "mount ",
        "umount",
        "sudo -n -u modsecurity-validator",
        "env -i",
        "bash --noprofile --norc -ceu",
        'make PYTHON="$PYTHON" BUILD_ROOT=',
        "rm -rf",
    )
    for term in forbidden:
        if term in validator:
            errors.append(f"workflow must delegate {term!r} exclusively to the namespace helper")

    namespace_count = normalized.count(READONLY_SUBMODULE_NAMESPACE_CALL)
    if namespace_count != 1:
        errors.append("workflow must invoke the namespace helper exactly once")
    if normalized.count("prepare-readonly-submodule-validation-sandbox.py") != 2:
        errors.append("sandbox helper must prepare and physically verify exactly once each")
    if normalized.count("umask 077") != 1:
        errors.append("only root-side sandbox preparation may set the workflow umask")
    if "GH_TOKEN" in validator or "secrets." in validator or "github.token" in validator:
        errors.append("validator job must not receive credentials")
    if "--namespace-parent /tmp" in validator or "--namespace-parent /var/tmp" in validator:
        errors.append("namespace helper must not use a public namespace parent")

    verification_step = validator.partition(
        "- name: Verify candidate source inventory and external outputs"
    )[2].partition("- name: Enforce isolated candidate result after verification")[0]
    if READONLY_SUBMODULE_VERIFY_GATE not in verification_step:
        errors.append("physical verification must follow a failed candidate but not failed preparation")

    setup_index = normalized.find(READONLY_SUBMODULE_SANDBOX_CALL)
    namespace_index = normalized.find(READONLY_SUBMODULE_NAMESPACE_CALL)
    verification_index = normalized.find("Verify candidate source inventory and external outputs")
    result_index = normalized.find("Enforce isolated candidate result after verification")
    if min(setup_index, namespace_index, verification_index, result_index) < 0 or not (
        setup_index < namespace_index < verification_index < result_index
    ):
        errors.append("root preparation, namespace candidate, physical verification, and result gate must be ordered")
    return errors


def readonly_namespace_runner_errors(runner: str) -> list[str]:
    """Return violations of the trusted private namespace launcher contract."""

    errors: list[str] = []
    required = (
        'PROCFS_TARGET = Path("/proc")',
        "CLONE_NEWNS | CLONE_NEWPID",
        "MS_NOEXEC = 8",
        'parser.add_argument("--namespace-parent", required=True)',
        "_validate_namespace_parent(namespace_parent, gid)",
        "namespace_ancestor = namespace_parent.parent",
        "namespace parent must have a trusted sticky ancestor",
        "namespace parent requires a root-owned sticky ancestor",
        "namespace parent must be root:validator mode 0750",
        "namespace parent must be empty before mount layout creation",
        "mount_root = namespace_parent / \"mount-root\"",
        "os.mkdir(path, mode=0o700)",
        "os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)",
        "metadata = os.fstat(descriptor)",
        "not stat.S_ISDIR(metadata.st_mode) or metadata.st_uid != 0",
        "os.fchown(descriptor, 0, validator_gid)",
        "os.fchmod(descriptor, 0o750)",
        "metadata = os.lstat(path)",
        "(0, validator_gid, 0o750)",
        "PR_SET_NO_NEW_PRIVS = 38",
        "if LIBC.prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) != 0:",
        "_set_no_new_privs()",
        '_mount(None, Path("/"), MS_REC | MS_PRIVATE)',
        "_mount(str(source), source_view, MS_BIND)",
        "MS_BIND | MS_REMOUNT | MS_RDONLY | MS_NOSUID | MS_NODEV",
        "_mount(str(external), external_view, MS_BIND)",
        "MS_BIND | MS_REMOUNT | MS_NOSUID | MS_NODEV",
        "_verify_mount(source_view, readonly=True)",
        "_verify_mount(external_view, readonly=False)",
        "_verify_procfs(PROCFS_TARGET)",
        "os.setgroups([]); os.setgid(gid); os.setuid(uid); os.chdir(source)",
        "os.execve(\"/bin/bash\"",
        "READONLY_SUBMODULE_VALIDATION_NAMESPACE_COMPLETE",
        "if _mountinfo_for(mount_root) != before:",
        "os.rmdir(path)",
        'test "$PWD" = "$GITHUB_WORKSPACE"',
        "/proc/self/status)",
        "0000000000000000",
        "NoNewPrivs:",
        'if /usr/bin/mount -o remount,rw "$GITHUB_WORKSPACE"',
        '"HOME": str(root / "home")',
        '"TMPDIR": str(root / "tmp")',
        '"XDG_CACHE_HOME": str(root / "xdg-cache")',
        '"PIP_CACHE_DIR": str(root / "pip-cache")',
        '"PYTHONPYCACHEPREFIX": str(root / "pycache")',
        '"PYTHONUSERBASE": str(root / "python-user-base")',
        '"PYTHONPATH": str(root / "python-packages")',
        '"GIT_CONFIG_GLOBAL": str(root / "gitconfig")',
        '"GITHUB_ACTIONS": "true"',
        '"BUILD_ROOT": str(root / "build")',
        '"VERIFIED_RUN_ROOT": str(root / "verified-run")',
        '"CACHE_ROOT": str(root / "cache")',
        '"VERIFIED_EVIDENCE_ROOT": str(root / "evidence")',
        '"RUNTIME_RUN_ROOT": str(root / "runtime")',
        '"SOURCE_ROOT": str(root / "source")',
        '"MATRIX_ROOT": str(root / "matrix")',
        ".readonly-validator-write-probe",
        "validator obtained sudo",
        'exec make PYTHON="$PYTHON" quick-check',
        '--target "$PYTHONPATH" --requirement "$GITHUB_WORKSPACE/ci/requirements/update-submodules-validation-linux-x86_64.txt"',
    )
    for term in required:
        if term not in runner:
            errors.append(f"missing {term}")
    for term in ("tempfile", "os.chmod(", 'Path("/tmp")', "os.umask(", "BaseException"):
        if term in runner:
            errors.append(f"namespace runner must not use {term!r}")
    if 'exec make PYTHON="$PYTHON" BUILD_ROOT=' in runner:
        errors.append("namespace runner must pass BUILD_ROOT through the environment")
    forbidden = (
        "MS_REC | MS_BIND",
        "MNT_DETACH",
        "shutil.",
        "rmtree",
        "subprocess",
        "shell=True",
        "os.system",
        "secrets.token_hex",
    )
    for term in forbidden:
        if term in runner:
            errors.append(f"namespace runner must not use {term}")
    if runner.count("_mount(str(source), source_view, MS_BIND)") != 1:
        errors.append("namespace runner must create exactly one non-recursive source bind")
    if runner.count("_mount(str(external), external_view, MS_BIND)") != 1:
        errors.append("namespace runner must create exactly one non-recursive output bind")
    if runner.count("_umount(external_view); _umount(source_view)") != 1:
        errors.append("namespace runner must synchronously unmount both exact views")

    if runner.count('PROCFS_TARGET = Path("/proc")') != 1 or runner.count(
        'Path("/proc")'
    ) != 1:
        errors.append("namespace runner must export one immutable literal procfs target")

    try:
        syntax_tree = ast.parse(runner)
    except SyntaxError:
        errors.append("namespace runner must remain valid Python")
        return errors
    functions = {
        node.name: "\n".join(runner.splitlines()[node.lineno - 1 : node.end_lineno])
        for node in syntax_tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.end_lineno is not None
    }
    pid1_candidate = functions.get("_run_pid1_candidate", "")
    namespace_child = functions.get("_namespace_child", "")
    if not pid1_candidate:
        errors.append("namespace runner must retain the PID-one candidate helper")
    if not namespace_child:
        errors.append("namespace runner must retain the namespace child launcher")
        return errors
    if pid1_candidate.count("ready_acknowledged = False") != 1 or pid1_candidate.count(
        "ready_acknowledged = True"
    ) != 1:
        errors.append("namespace runner must transfer procfs cleanup ownership exactly once")

    proc_mount = re.compile(
        r'''_mount\(\s*["']proc["']\s*,\s*PROCFS_TARGET\s*,\s*'''
        r"MS_RDONLY\s*\|\s*MS_NOSUID\s*\|\s*MS_NODEV\s*\|\s*MS_NOEXEC"
        r'''\s*,\s*["']proc["']\s*\)'''
    )
    proc_match = proc_mount.search(pid1_candidate)
    if proc_match is None:
        errors.append("namespace runner must mount a fresh readonly nosuid nodev noexec procfs at /proc")
        return errors

    fork_index = namespace_child.find("child = os.fork()")
    helper_call_index = namespace_child.find("_run_pid1_candidate(", fork_index)
    verifier_index = pid1_candidate.find("_verify_procfs(PROCFS_TARGET)")
    readiness_write_index = pid1_candidate.find('os.write(proc_ready_write, b"1")')
    readiness_transfer_index = pid1_candidate.find("ready_acknowledged = True")
    no_new_privs_index = pid1_candidate.find("_set_no_new_privs()")
    candidate_entry_index = pid1_candidate.find("candidate_entry(*candidate_arguments)")
    if min(
        fork_index,
        helper_call_index,
        verifier_index,
        readiness_write_index,
        readiness_transfer_index,
        no_new_privs_index,
        candidate_entry_index,
    ) < 0 or not (
        fork_index < helper_call_index
        and proc_match.start()
        < verifier_index
        < readiness_write_index
        < readiness_transfer_index
        < no_new_privs_index
        < candidate_entry_index
    ):
        errors.append("private procfs readiness ownership must transfer before no_new_privs and candidate identity drop")
    if pid1_candidate.count("_umount(PROCFS_TARGET)") != 1 or namespace_child.count(
        "_umount(PROCFS_TARGET)"
    ) != 1:
        errors.append("namespace runner must retain guarded child cleanup and parent procfs restoration")
    child_proc_cleanup = re.search(
        r'''if proc_mounted and not ready_acknowledged:\s+try:\s+_umount\(PROCFS_TARGET\)\s+'''
        r'''if _mountinfo_for\(PROCFS_TARGET\) != before_proc:''',
        pid1_candidate,
    )
    parent_proc_restoration = re.search(
        r'''finally:\s+if proc_mounted:\s+_umount\(PROCFS_TARGET\)\s+'''
        r'''if _mountinfo_for\(PROCFS_TARGET\) != before_proc:''',
        namespace_child,
    )
    if child_proc_cleanup is None:
        errors.append("namespace runner must synchronously clean up procfs if PID-one setup fails")
    if parent_proc_restoration is None:
        errors.append("namespace runner must synchronously restore procfs after the PID child exits")
    wait_index = namespace_child.find("os.waitpid(child, 0)")
    readiness_read_index = namespace_child.find(
        'proc_mounted = os.read(proc_ready_read, 1) == b"1"'
    )
    if parent_proc_restoration is not None and (
        readiness_read_index < 0
        or wait_index < 0
        or not readiness_read_index < wait_index < parent_proc_restoration.start()
    ):
        errors.append("namespace runner must acknowledge readiness and restore /proc only after the PID child exits")
    if "before_proc = _mountinfo_for(PROCFS_TARGET)" not in namespace_child or (
        "if _mountinfo_for(PROCFS_TARGET) != before_proc:" not in namespace_child
        or "if _mountinfo_for(PROCFS_TARGET) != before_proc:" not in pid1_candidate
    ):
        errors.append("namespace runner must verify /proc mount restoration after synchronous cleanup")
    return errors


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


def update_submodule_validate_only_errors(text: str) -> list[str]:
    """Return violations of the manual non-publishing validation contract."""

    errors: list[str] = []
    if text.count(SUBMODULE_VALIDATE_ONLY_INPUT) != 1:
        errors.append("validate_only must be one exact optional-false boolean input")
    if text.count(SUBMODULE_VALIDATE_ONLY_PROTECTED_FLAG) != 4:
        errors.append("protected-master validation must have four exact ref-protection checks")

    jobs = job_blocks(text)
    required_jobs = {
        "resolve-submodule-update",
        "validate-submodule-update",
        "create-submodule-update-pr",
        "report-submodule-update-outcome",
    }
    if not required_jobs.issubset(jobs):
        return errors + ["validate_only contract jobs are missing"]

    resolver = jobs["resolve-submodule-update"]
    validator = jobs["validate-submodule-update"]
    publisher = jobs["create-submodule-update-pr"]
    outcome = jobs["report-submodule-update-outcome"]
    normalized_resolver = normalize_shell_script(resolver)
    normalized_outcome = normalize_shell_script(outcome)

    if job_if_expression(resolver) != SUBMODULE_RESOLVER_GATE:
        errors.append("resolver must allow only same-repository master or manual validate_only")
    if job_if_expression(validator) != SUBMODULE_VALIDATOR_GATE:
        errors.append("validator must retain its successful changed-candidate gate")
    if job_if_expression(publisher) != SUBMODULE_PUBLISHER_GATE:
        errors.append("publisher must be disabled by the resolver-derived validate_only flag")
    if job_if_expression(outcome) != "always()":
        errors.append("outcome reporter must inspect every terminal job state")

    checkout_contracts = (
        ("resolver", resolver, "Checkout Parent metadata"),
        ("validator", validator, "Checkout candidate for read-only validation"),
    )
    for name, job, step_name in checkout_contracts:
        checkout_steps = checkout_step_blocks(job)
        if (
            len(checkout_steps) != 1
            or f"- name: {step_name}" not in checkout_steps[0]
            or checkout_steps[0].count(SUBMODULE_VALIDATE_ONLY_CHECKOUT_REF) != 1
        ):
            errors.append(
                f"{name} named checkout must use the dispatched SHA only for validate_only"
            )
    if SUBMODULE_VALIDATE_ONLY_CHECKOUT_REF in publisher:
        errors.append("publisher must never check out the dispatched validate_only SHA")
    if "ref: ${{ github.event.repository.default_branch }}" not in publisher:
        errors.append("publisher must retain the default-branch checkout")

    activation = (
        "validation_only=false "
        f'if [ "${{{{ {SUBMODULE_VALIDATE_ONLY_MANUAL_PREDICATE} }}}}" = true ]; then '
        "validation_only=true fi"
    )
    force_changed = 'if [ "$validation_only" = true ]; then changed=true fi'
    if activation not in normalized_resolver:
        errors.append("resolver must derive validation_only only from the manual boolean input")
    if normalized_resolver.count(force_changed) != 1:
        errors.append("resolver must force changed exactly once and only inside validation_only")
    if normalized_resolver.count("changed=true") != 2:
        errors.append("changed may be true only for a real update or validate_only")
    if re.findall(r"\bchanged=(?:false|true)\b", normalized_resolver) != [
        "changed=false",
        "changed=true",
        "changed=true",
    ]:
        errors.append("validation_only must be the final changed assignment before outputs")
    if (
        activation in normalized_resolver
        and force_changed in normalized_resolver
        and normalized_resolver.index(activation) >= normalized_resolver.index(force_changed)
    ):
        errors.append("validation_only activation must precede its changed override")
    if resolver.count("validation_only: ${{ steps.resolve.outputs.validation_only }}") != 1:
        errors.append("resolver must expose one validation_only job output")
    if normalized_resolver.count(
        "printf 'validation_only=%s\\n' \"$validation_only\""
    ) != 1:
        errors.append("resolver must publish one validation_only step output")

    if job_permissions(resolver) != {"contents": "read"}:
        errors.append("resolver permissions must remain contents-read only")
    if job_permissions(validator) != {"contents": "read"}:
        errors.append("validator permissions must remain contents-read only")
    if job_permissions(publisher) != {"contents": "write", "pull-requests": "write"}:
        errors.append("publisher permissions changed outside the established boundary")
    if job_permissions(outcome) != {"contents": "read"}:
        errors.append("outcome reporter permissions must remain contents-read only")
    if any(term in resolver or term in validator for term in ("GH_TOKEN", "secrets.", "github.token")):
        errors.append("resolver and validator must not receive publishing credentials")
    if any(term in publisher for term in ("gh pr merge", "--auto", "enablePullRequestAutoMerge")):
        errors.append("publisher must not enable or perform auto-merge")

    validation_only_case = 'case "$VALIDATION_ONLY" in'
    changed_case = 'case "$CHANGED" in'
    validation_only_success = (
        'if [ "$CHANGED" != "true" ] || [ "$VALIDATOR_RESULT" != "success" ] || '
        '[ "$PUBLISHER_RESULT" != "skipped" ]; then'
    )
    normal_update_success = (
        'if [ "$VALIDATOR_RESULT" != "success" ] || '
        '[ "$PUBLISHER_RESULT" != "success" ]; then'
    )
    if outcome.count(
        "VALIDATION_ONLY: ${{ needs.resolve-submodule-update.outputs.validation_only }}"
    ) != 1:
        errors.append("outcome reporter must consume one resolver-derived validation_only output")
    if normalized_outcome.count(validation_only_case) != 1:
        errors.append("outcome reporter must have one validation_only state case")
    if normalized_outcome.count(changed_case) != 1:
        errors.append("outcome reporter must retain one normal changed state case")
    if validation_only_case in normalized_outcome and changed_case in normalized_outcome:
        validation_only_section = normalized_outcome.partition(validation_only_case)[2].partition(
            changed_case
        )[0]
        if validation_only_success not in validation_only_section:
            errors.append("validate_only success requires changed, validator success, and publisher skip")
        if "exit 0" not in validation_only_section:
            errors.append("successful validate_only reporting must exit before normal publishing checks")
        if normalized_outcome.index(validation_only_case) >= normalized_outcome.index(changed_case):
            errors.append("validate_only state must be handled before the normal changed state")
    if normalized_outcome.count(normal_update_success) != 1:
        errors.append("normal changed updates must still require validator and publisher success")
    return errors


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
        f"      framework_sha: {PROTECTED_NGINX_BROKER_FRAMEWORK_SHA}",
        f"      protected_broker_sha: {PROTECTED_NGINX_BROKER_SHA}",
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
    if (
        "ref: ${{ github.sha }}" not in prepare
        or 'test "$(git rev-parse HEAD)" = "$GITHUB_SHA"' not in prepare
        or "persist-credentials: false" not in prepare
    ):
        errors.append("caller checkout identity")
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

    def test_codeql_uses_trusted_base_go_version_and_bounded_cpp_scope(self) -> None:
        text = self.workflow("ci-security-codeql.yml")
        self.assertIn("ref: ${{ github.event.pull_request.base.sha || github.sha }}", text)
        self.assertEqual(
            text.count("go-version: ${{ needs.trusted-go-version.outputs.version }}"),
            2,
        )
        self.assertEqual(text.count("check-latest: false"), 2)
        self.assertNotIn("go-version-file: .go-version", text)
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

    def test_report_governance_and_strict_evidence_lifecycles_are_isolated(self) -> None:
        """Keep fresh-checkout governance separate from materialized runtime evidence."""

        text = self.workflow("verified-report-governance.yml")
        jobs = self.jobs("verified-report-governance.yml")
        self.assertEqual(set(jobs), {"report-governance"})
        job = jobs["report-governance"]
        self.assertIn("timeout-minutes: 20", job)
        self.assertIn("make report-governance", job)
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        lint_body = makefile.split("lint:", 1)[1].split("\nsummary:", 1)[0]
        self.assertIn("$(MAKE) report-governance", lint_body)
        self.assertNotIn("verified-report-evidence-gate", lint_body)
        strict_target = makefile.split("verified-report-evidence-gate:", 1)[1].split("\n\n", 1)[0]
        self.assertIn("check-generated-report-layout", strict_target)
        lifecycle = (ROOT / "ci/runtime/lifecycle/run-verified-report-run.py").read_text(
            encoding="utf-8"
        )
        self.assertIn('["make", "verified-report-evidence-gate"]', lifecycle)

        # Generic CI and maintenance workflows must not invoke the strict gate;
        # only the runtime lifecycle above may do so after its producer/refresh phases.
        for path in self.workflow_paths():
            self.assertNotIn(
                "verified-report-evidence-gate",
                path.read_text(encoding="utf-8"),
                path.name,
            )
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
        self.assertIn("ACTUAL_CALLER_WORKFLOW_REF: ${{ github.workflow_ref }}", text)
        self.assertIn(
            "EXPECTED_CALLER_WORKFLOW_REF: Easton97-Jens/ModSecurity-conector/.github/workflows/run-protected-nginx-root-broker.yml@refs/heads/master",
            text,
        )
        self.assertNotIn("EXPECTED_WORKFLOW_REF:", text)
        self.assertIn("CALLER_SHA: ${{ github.sha }}", text)
        self.assertIn("CALLER_WORKFLOW_SHA: ${{ github.workflow_sha }}", text)
        self.assertIn('git cat-file -e "$CALLER_SHA^{commit}"', text)
        self.assertIn('git merge-base --is-ancestor "$CALLER_SHA" FETCH_HEAD', text)
        self.assertIn("validate-caller-workflow", text)
        self.assertIn('git merge-base --is-ancestor "$BROKER_SHA" FETCH_HEAD', text)
        self.assertIn('git ls-tree "$BROKER_SHA" -- modules/ModSecurity-test-Framework', text)
        self.assertIn("verify_broker_source .github/workflows/nginx-root-broker.yml", text)
        self.assertIn('git rev-parse "$BROKER_SHA:$source_path"', text)
        self.assertIn('git hash-object "$source_path"', text)
        self.assertIn("verify_broker_source ci/runtime/broker/nginx_root_broker.py", text)
        self.assertIn("prepare-fresh-crs-source.sh", text)
        self.assertIn("prepare-crs-bundle", text)
        self.assertEqual(
            text.count(
                "          RUNTIME_COMPONENT_SNAPSHOT_CONTRACT: protected-nginx-broker"
            ),
            1,
        )
        self.assertLess(
            text.index("RUNTIME_COMPONENT_SNAPSHOT_CONTRACT: protected-nginx-broker"),
            text.index("make fetch-deps"),
        )
        self.assertLess(
            text.index("make fetch-deps"),
            text.index("prepare-from-snapshot"),
        )
        self.assertNotIn(
            "RUNTIME_COMPONENT_SNAPSHOT_CONTRACT: ${{", text
        )
        self.assertIn("verify-runtime-profile", text)
        self.assertIn("cleanup.json", text)
        self.assertIn("sudo -- /usr/bin/python3 -I ci/runtime/broker/nginx_root_broker.py action", text)
        self.assertNotIn("uses: ./", text)
        for forbidden in (
            "sudo -E",
            "sudo sh -c",
            "sudo bash -c",
            "shell: bash -c",
            "id-token: write",
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
                    f"@{PROTECTED_NGINX_BROKER_SHA}", "@master"
                ),
            ),
            "broker branch ref": (
                PROTECTED_NGINX_BROKER_REUSABLE_REFERENCE,
                PROTECTED_NGINX_BROKER_REUSABLE_REFERENCE.replace(
                    f"@{PROTECTED_NGINX_BROKER_SHA}", "@fix/unsafe"
                ),
            ),
            "local reusable workflow": (
                PROTECTED_NGINX_BROKER_REUSABLE_REFERENCE,
                "./.github/workflows/nginx-root-broker.yml",
            ),
            "wrong broker SHA": (
                PROTECTED_NGINX_BROKER_REUSABLE_REFERENCE,
                PROTECTED_NGINX_BROKER_REUSABLE_REFERENCE.replace(
                    PROTECTED_NGINX_BROKER_SHA,
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
                f"framework_sha: {PROTECTED_NGINX_BROKER_FRAMEWORK_SHA}",
                "framework_sha: " + "0" * 40,
            ),
            "duplicate broker input": (
                f"      framework_sha: {PROTECTED_NGINX_BROKER_FRAMEWORK_SHA}",
                "\n".join(
                    (
                        f"      framework_sha: {PROTECTED_NGINX_BROKER_FRAMEWORK_SHA}",
                        f"      framework_sha: {PROTECTED_NGINX_BROKER_FRAMEWORK_SHA}",
                    )
                ),
            ),
            "missing master guard": (
                "github.ref == 'refs/heads/master' &&\n",
                "",
            ),
            "wrong repository guard": (
                "github.repository == 'Easton97-Jens/ModSecurity-conector'",
                "github.repository == 'attacker/example'",
            ),
            "missing fork guard": (
                "github.event.repository.fork == false &&\n",
                "",
            ),
            "missing default branch guard": (
                "github.event.repository.default_branch == 'master'",
                "github.event.repository.default_branch == 'main'",
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
            "mutable caller checkout": (
                "          ref: ${{ github.sha }}",
                "          ref: master",
            ),
            "missing caller checkout head assertion": (
                '          test "$(git rev-parse HEAD)" = "$GITHUB_SHA"\n',
                "",
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
        workflow = self.workflow("update-submodules.yml")
        jobs = job_blocks(workflow)
        self.assertEqual(
            set(jobs),
            {
                "resolve-submodule-update",
                "validate-submodule-update",
                "create-submodule-update-pr",
                "report-submodule-update-outcome",
            },
        )
        resolver = jobs["resolve-submodule-update"]
        validator = jobs["validate-submodule-update"]
        publisher = jobs["create-submodule-update-pr"]
        normalized_publisher = normalize_shell_script(publisher)
        outcome = jobs["report-submodule-update-outcome"]

        self.assertEqual(job_permissions(resolver), {"contents": "read"})
        self.assertEqual(job_permissions(validator), {"contents": "read"})
        self.assertEqual(
            job_permissions(publisher),
            {"contents": "write", "pull-requests": "write"},
        )
        self.assertEqual(job_permissions(outcome), {"contents": "read"})
        self.assertEqual(job_if_expression(outcome), "always()")
        self.assertEqual(update_submodule_validate_only_errors(workflow), [])
        self.assertEqual(job_if_expression(resolver), SUBMODULE_RESOLVER_GATE)
        self.assertEqual(resolver.count(SUBMODULE_VALIDATE_ONLY_CHECKOUT_REF), 1)
        self.assertEqual(validator.count(SUBMODULE_VALIDATE_ONLY_CHECKOUT_REF), 1)
        self.assertIn("github.ref == 'refs/heads/master'", resolver)
        self.assertIn("github.event.repository.default_branch == 'master'", resolver)
        self.assertIn("github.event.repository.fork == false", resolver)
        self.assertIn("remote_ref_count", resolver)
        self.assertIn('if [ "$remote_ref_count" != "1" ]; then', resolver)
        self.assertIn('if [ "$candidate_ref" != "$SUBMODULE_REF" ]; then', resolver)
        self.assertIn("Resolved submodule revision is not a full SHA-1", resolver)
        self.assertIn("Current gitlink is not a full SHA-1", resolver)
        self.assertIn('if [ "$candidate_sha" = "$current_sha" ]; then', resolver)
        self.assertIn("changed=false", resolver)
        self.assertIn("changed=true", resolver)
        self.assertIn("Current Parent tree does not contain exactly one submodule entry", resolver)
        self.assertIn("candidate_sha", resolver)
        self.assertIn("current_sha", resolver)
        self.assertIn("resolver_status=resolved", resolver)

        self.assertIn("needs: resolve-submodule-update", validator)
        self.assertEqual(
            job_if_expression(validator),
            SUBMODULE_VALIDATOR_GATE,
        )
        self.assertIn("submodules: recursive", validator)
        self.assertIn(READONLY_SUBMODULE_NAMESPACE_CALL, normalize_shell_script(validator))
        self.assertIn("remote get-url origin", validator)
        self.assertIn("merge-base --is-ancestor", validator)
        self.assertIn("checkout --detach", validator)
        self.assertIn("submodule update --init --recursive", validator)
        self.assertIn("status --porcelain", validator)
        dependency_lock = (
            ROOT / "ci" / "requirements" / "update-submodules-validation-linux-x86_64.txt"
        ).read_text(encoding="utf-8")
        self.assertIn("PyYAML==6.0.3", dependency_lock)
        self.assertIn(
            "--hash=sha256:c458b6d084f9b935061bc36216e8a69a7e293a2f1e68bf956dcd9e6cbcd143f5",
            dependency_lock,
        )
        self.assertNotIn("PyYAML>=", dependency_lock)
        self.assertIn("EXPECTED_PYTHON: ${{ steps.setup-python.outputs.python-path }}", validator)
        self.assertNotIn("GH_TOKEN", validator)
        self.assertNotIn("secrets.", validator)
        self.assertEqual(readonly_submodule_validator_errors(validator), [])

        """Run the exact workflow prelude with a test-local sudo implementation."""
        workflow_payload = yaml.safe_load(self.workflow("update-submodules.yml"))
        steps = workflow_payload["jobs"]["validate-submodule-update"]["steps"]
        candidate_step = next(
            step for step in steps if step["name"] == "Run quick check in the private read-only namespace"
        )
        prelude, separator, _candidate = candidate_step["run"].partition("namespace_output=")
        expected_prelude = """\
set -euo pipefail
namespace_parent=""
cleanup_namespace_parent() {
  namespace_status=$?
  if [ -n "$namespace_parent" ]; then
    sudo -n rmdir -- "$namespace_parent" || {
      echo "Unable to remove readonly namespace parent" >&2
      return 1
    }
  fi
  return "$namespace_status"
}
trap cleanup_namespace_parent EXIT
namespace_parent="$(sudo -n mktemp -d /tmp/modsecurity-readonly-namespace.XXXXXX)"
sudo -n chown root:modsecurity-validator "$namespace_parent"
sudo -n chmod 0750 "$namespace_parent"
"""
        self.assertTrue(separator)
        self.assertEqual(prelude, expected_prelude)
        self.assertNotIn("run-readonly-submodule-validation-namespace.py", prelude)

        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            mock_bin = temporary_root / "bin"; mock_bin.mkdir()
            namespace_root = temporary_root / "namespace-parents"; namespace_root.mkdir()
            sudo_log = temporary_root / "sudo.log"
            created_paths = temporary_root / "created-paths.log"
            mock_sudo = mock_bin / "sudo"
            mock_sudo.write_text(
                "\n".join(
                    (
                        "#!/bin/sh", "set -eu", "printf '%s\\n' \"$*\" >> \"$MOCK_SUDO_LOG\"",
                        "test \"$1\" = -n", "shift", "case \"$1\" in",
                        "  mktemp)",
                        "    path=\"$(/usr/bin/mktemp -d \"$MOCK_NAMESPACE_ROOT/namespace.XXXXXX\")\"",
                        "    printf '%s\\n' \"$path\" >> \"$MOCK_CREATED_PATHS\"",
                        "    printf '%s\\n' \"$path\"", "    ;;",
                        "  chown|chmod) exit 0 ;;", "  rmdir)", "    shift",
                        "    if [ \"${MOCK_RMDIR_FAILURE:-0}\" = 1 ]; then exit 73; fi",
                        "    exec /usr/bin/rmdir \"$@\"", "    ;;",
                        "  *) echo \"unexpected mocked sudo command: $*\" >&2; exit 99 ;;", "esac", "",
                    )
                ),
                encoding="utf-8",
            )
            mock_sudo.chmod(0o700)

            def execute(candidate_status: int, *, rmdir_failure: bool = False) -> tuple[subprocess.CompletedProcess[str], Path]:
                environment = {
                    **os.environ,
                    "PATH": f"{mock_bin}:{os.environ['PATH']}",
                    "MOCK_SUDO_LOG": str(sudo_log),
                    "MOCK_CREATED_PATHS": str(created_paths),
                    "MOCK_NAMESPACE_ROOT": str(namespace_root),
                    "MOCK_RMDIR_FAILURE": "1" if rmdir_failure else "0",
                    "CANDIDATE_STATUS": str(candidate_status),
                }
                environment.pop("BASH_ENV", None)
                result = subprocess.run(
                    ["/bin/bash", "-ceu", "\n".join((expected_prelude, 'exit "$CANDIDATE_STATUS"', ""))],
                    text=True, capture_output=True, env=environment, check=False,
                )
                if not created_paths.exists():
                    self.fail(result.stderr)
                created = Path(created_paths.read_text(encoding="utf-8").splitlines()[-1])
                return result, created

            success, success_parent = execute(0)
            self.assertEqual(success.returncode, 0, success.stderr)
            self.assertFalse(success_parent.exists())

            candidate_failure, failed_parent = execute(47)
            self.assertEqual(candidate_failure.returncode, 47, candidate_failure.stderr)
            self.assertFalse(failed_parent.exists())

            cleanup_failure, retained_parent = execute(0, rmdir_failure=True)
            try:
                self.assertNotEqual(cleanup_failure.returncode, 0)
                self.assertTrue(retained_parent.is_dir())
            finally:
                if retained_parent.exists():
                    retained_parent.rmdir()

            log = sudo_log.read_text(encoding="utf-8")
            self.assertIn(f"rmdir -- {success_parent}", log)
            self.assertIn(f"rmdir -- {failed_parent}", log)
            self.assertIn(f"rmdir -- {retained_parent}", log)
            self.assertNotIn("rm -rf", log)
        namespace_runner = (
            ROOT / "ci" / "tools" / "run-readonly-submodule-validation-namespace.py"
        ).read_text(encoding="utf-8")
        self.assertEqual(readonly_namespace_runner_errors(namespace_runner), [])
        namespace_mutations = {
            "namespace loses PID isolation": (
                "CLONE_NEWNS | CLONE_NEWPID",
                "CLONE_NEWNS",
            ),
            "namespace propagation is not private": (
                '_mount(None, Path("/"), MS_REC | MS_PRIVATE)',
                '_mount(None, Path("/"), MS_REC)',
            ),
            "candidate can gain new privileges": (
                "if LIBC.prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) != 0:",
                "if False:",
            ),
            "candidate does not prove no-new-privileges": (
                "NoNewPrivs:",
                "NoNewPrivileges:",
            ),
            "source is recursively bound": (
                "_mount(str(source), source_view, MS_BIND)",
                "_mount(str(source), source_view, MS_REC | MS_BIND)",
            ),
            "source loses read-only remount": (
                "MS_BIND | MS_REMOUNT | MS_RDONLY | MS_NOSUID | MS_NODEV",
                "MS_BIND | MS_REMOUNT | MS_NOSUID | MS_NODEV",
            ),
            "output loses device restriction": (
                "MS_BIND | MS_REMOUNT | MS_NOSUID | MS_NODEV",
                "MS_BIND | MS_REMOUNT | MS_NOSUID",
            ),
            "candidate retains root identity": (
                "os.setgroups([]); os.setgid(gid); os.setuid(uid); os.chdir(source)",
                "os.chdir(source)",
            ),
            "candidate loses hosted-run classification": (
                '"GITHUB_ACTIONS": "true"',
                '"GITHUB_ACTIONS": "false"',
            ),
            "namespace uses lazy cleanup": (
                "os.rmdir(path)",
                "MNT_DETACH",
            ),
            "namespace accepts a public parent": (
                "namespace parent must be root:validator mode 0750",
                "namespace parent may be public",
            ),
            "namespace mount root loses validator traversal": (
                "os.fchmod(descriptor, 0o750)",
                "os.mkdir(path, mode=0o700)",
            ),
            "namespace restores unsafe Python chmod": (
                "os.fchown(descriptor, 0, validator_gid)",
                "os.fchown(descriptor, 0, validator_gid)\n            os.chmod(path, 0o755)",
            ),
            "namespace hardcodes the public temporary directory": (
                "namespace_ancestor = namespace_parent.parent",
                'namespace_ancestor = Path("/tmp")',
            ),
            "namespace changes the process umask": (
                "os.fchmod(descriptor, 0o750)",
                "os.umask(0)\n            os.fchmod(descriptor, 0o750)",
            ),
            "namespace catches process-control exceptions": (
                "except Exception as error:",
                "except BaseException as error:",
            ),
        }
        for name, (original, replacement) in namespace_mutations.items():
            with self.subTest(name=name):
                self.assertIn(original, namespace_runner)
                mutated_runner = namespace_runner.replace(original, replacement, 1)
                self.assertNotEqual(readonly_namespace_runner_errors(mutated_runner), [])

        proc_match = re.search(
            r'''_mount\(\s*["']proc["']\s*,\s*PROCFS_TARGET\s*,\s*'''
            r"MS_RDONLY\s*\|\s*MS_NOSUID\s*\|\s*MS_NODEV\s*\|\s*MS_NOEXEC"
            r'''\s*,\s*["']proc["']\s*\)''',
            namespace_runner,
        )
        self.assertIsNotNone(proc_match)
        assert proc_match is not None
        proc_mount = proc_match.group(0)
        proc_mutations = {
            "private procfs constant is mutable to another target": (
                'PROCFS_TARGET = Path("/proc")',
                'PROCFS_TARGET = Path("/proc-unsafe")',
            ),
            "private procfs is missing": proc_mount.replace('"proc"', '"none"', 1),
            "private procfs has executable flags": proc_mount.replace("| MS_NOEXEC", "", 1),
            "private procfs has the wrong mount target": proc_mount.replace(
                "PROCFS_TARGET", 'Path("/proc")', 1
            ),
            "private procfs mounts before the PID child fork": "",
            "private procfs verifier is missing": "",
            "private procfs verifier runs after no-new-privileges": "",
            "private procfs readiness ownership transfer is missing": "",
            "private procfs readiness ownership transfers after no-new-privileges": "",
            "private procfs child cleanup remains active after readiness": "",
            "private procfs guarded child cleanup is missing": "",
            "private procfs parent ignores readiness acknowledgement": "",
            "private procfs parent restoration is missing": "",
            "private procfs restoration proof is missing": "before_proc = []",
        }
        for name, replacement in proc_mutations.items():
            with self.subTest(name=name):
                if name == "private procfs constant is mutable to another target":
                    original, mutated = replacement
                    self.assertIn(original, namespace_runner)
                    mutated_runner = namespace_runner.replace(original, mutated, 1)
                elif name == "private procfs mounts before the PID child fork":
                    helper_invocation_match = re.search(
                        r"^        _run_pid1_candidate\(\n(?:^            .*\n)+^        \)$",
                        namespace_runner,
                        re.MULTILINE,
                    )
                    self.assertIsNotNone(helper_invocation_match)
                    assert helper_invocation_match is not None
                    helper_invocation = helper_invocation_match.group(0)
                    relocated_invocation = "\n".join(
                        line[4:] for line in helper_invocation.splitlines()
                    )
                    mutated_runner = namespace_runner.replace(helper_invocation, "", 1).replace(
                        "    child = os.fork()",
                        f"{relocated_invocation}\n    child = os.fork()",
                        1,
                    )
                elif name == "private procfs verifier is missing":
                    mutated_runner = namespace_runner.replace(
                        "_verify_procfs(PROCFS_TARGET)", "", 1
                    )
                elif name == "private procfs verifier runs after no-new-privileges":
                    mutated_runner = namespace_runner.replace(
                        "_verify_procfs(PROCFS_TARGET)", "", 1
                    ).replace(
                        "_set_no_new_privs()",
                        "_set_no_new_privs()\n        _verify_procfs(PROCFS_TARGET)",
                        1,
                    )
                elif name == "private procfs readiness ownership transfer is missing":
                    mutated_runner = namespace_runner.replace(
                        "ready_acknowledged = True", "", 1
                    )
                elif name == "private procfs readiness ownership transfers after no-new-privileges":
                    mutated_runner = namespace_runner.replace(
                        "ready_acknowledged = True", "", 1
                    ).replace(
                        "_set_no_new_privs()",
                        "_set_no_new_privs()\n        ready_acknowledged = True",
                        1,
                    )
                elif name == "private procfs child cleanup remains active after readiness":
                    mutated_runner = namespace_runner.replace(
                        "if proc_mounted and not ready_acknowledged:",
                        "if proc_mounted:",
                        1,
                    )
                elif name == "private procfs guarded child cleanup is missing":
                    mutated_runner = namespace_runner.replace(
                        "if proc_mounted and not ready_acknowledged:\n            try:\n                _umount(PROCFS_TARGET)",
                        "if False:\n            try:\n                _umount(PROCFS_TARGET)",
                        1,
                    )
                elif name == "private procfs parent ignores readiness acknowledgement":
                    mutated_runner = namespace_runner.replace(
                        'proc_mounted = os.read(proc_ready_read, 1) == b"1"',
                        "proc_mounted = True",
                        1,
                    )
                elif name == "private procfs parent restoration is missing":
                    mutated_runner = namespace_runner.replace(
                        "finally:\n        if proc_mounted:\n            _umount(PROCFS_TARGET)",
                        "finally:\n        if False:\n            _umount(PROCFS_TARGET)",
                        1,
                    )
                elif name == "private procfs restoration proof is missing":
                    mutated_runner = namespace_runner.replace(
                        "before_proc = _mountinfo_for(PROCFS_TARGET)", replacement, 1
                    )
                else:
                    mutated_runner = namespace_runner.replace(proc_mount, replacement, 1)
                self.assertNotEqual(readonly_namespace_runner_errors(mutated_runner), [])
        self.assertLess(
            validator.index("Prepare dedicated read-only candidate sandbox"),
            validator.index("Run quick check in the private read-only namespace"),
        )
        self.assertLess(
            validator.index("Run quick check in the private read-only namespace"),
            validator.index("Verify candidate source inventory and external outputs"),
        )
        self.assertLess(
            validator.index("Check out the resolved descendant revision"),
            validator.index("Prepare dedicated read-only candidate sandbox"),
        )
        self.assertIn(READONLY_SUBMODULE_SANDBOX_CALL, normalize_shell_script(validator))
        self.assertIn(READONLY_SUBMODULE_WRITE_ROOT, validator)
        self.assertIn(READONLY_SUBMODULE_EXTERNAL_ROOT, validator)
        self.assertNotIn("setfacl", validator)
        self.assertNotIn("getfacl", validator)
        self.assertNotIn("sudo -n -u modsecurity-validator", validator)

        validator_mutations = {
            "namespace helper removed": (
                "run-readonly-submodule-validation-namespace.py",
                "run-readonly-submodule-validation-namespace.removed.py",
            ),
            "namespace helper loses the physical guard root": (
                '--write-root "$VALIDATION_WRITE_ROOT"',
                '--write-root /tmp/validator-guard',
            ),
            "namespace helper loses the physical external root": (
                '--external-root "$VALIDATION_WRITE_ROOT/external"',
                '--external-root /tmp/validator-output',
            ),
            "namespace helper loses the unprivileged user": (
                "--validator-user modsecurity-validator",
                "--validator-user root",
            ),
            "namespace helper loses its private mount parent": (
                '--namespace-parent "$namespace_parent"',
                "--namespace-parent /tmp",
            ),
            "namespace parent is not trusted root-created storage": (
                'namespace_parent="$(sudo -n mktemp -d /tmp/modsecurity-readonly-namespace.XXXXXX)"',
                'namespace_parent="/tmp/modsecurity-readonly-namespace"',
            ),
            "namespace parent cleanup becomes recursive": (
                'sudo -n rmdir -- "$namespace_parent"',
                'sudo -n rm -rf -- "$namespace_parent"',
            ),
            "namespace completion marker is not required": (
                READONLY_SUBMODULE_NAMESPACE_COMPLETE,
                "READONLY_SUBMODULE_VALIDATION_NAMESPACE_NOT_COMPLETE",
            ),
            "post-candidate source verification removed": (
                "Verify candidate source inventory and external outputs",
                "Candidate verification removed",
            ),
            "inventory verification disabled": (
                "--verify",
                "--inspect",
            ),
            "verification no longer runs after candidate failure": (
                "- name: Verify candidate source inventory and external outputs\n"
                "        " + READONLY_SUBMODULE_VERIFY_GATE,
                "- name: Verify candidate source inventory and external outputs\n"
                "        if: ${{ success() }}",
            ),
            "candidate result is not enforced after verification": (
                'test "$CANDIDATE_RESULT" = success',
                "true",
            ),
            "workflow regains ACL mutation": (
                "printf 'write_root=%s\\n' \"$write_root\" >> \"$GITHUB_OUTPUT\"",
                "printf 'write_root=%s\\n' \"$write_root\" >> \"$GITHUB_OUTPUT\"\n"
                '          sudo -n setfacl -m "u:modsecurity-validator:--x" -- "$RUNNER_TEMP"',
            ),
        }
        for name, (original, replacement) in validator_mutations.items():
            with self.subTest(name=name):
                self.assertIn(original, validator)
                mutated = validator.replace(original, replacement, 1)
                self.assertNotEqual(readonly_submodule_validator_errors(mutated), [])

        namespace_runner_removed = validator.replace(
            "run-readonly-submodule-validation-namespace.py",
            "run-readonly-submodule-validation-namespace.removed.py",
            1,
        )
        self.assertNotEqual(readonly_submodule_validator_errors(namespace_runner_removed), [])

        validate_only_mutations = {
            "input enables validate_only by default": (
                SUBMODULE_VALIDATE_ONLY_INPUT,
                SUBMODULE_VALIDATE_ONLY_INPUT.replace("default: false", "default: true"),
            ),
            "fork gate removed from resolver": (
                "github.event.repository.fork == false &&",
                "github.event.repository.fork == true ||",
            ),
            "canonical repository constraint removed": (
                SUBMODULE_VALIDATE_ONLY_REPOSITORY,
                "true",
            ),
            "canonical repository constraint changed": (
                SUBMODULE_VALIDATE_ONLY_REPOSITORY,
                "github.repository == 'attacker/ModSecurity-conector'",
            ),
            "repair branch constraint removed": (
                SUBMODULE_VALIDATE_ONLY_BRANCH,
                "true",
            ),
            "repair branch constraint changed": (
                SUBMODULE_VALIDATE_ONLY_BRANCH,
                "github.ref == 'refs/heads/arbitrary-validator-branch'",
            ),
            "protected master removed from validate_only allowlist": (
                SUBMODULE_VALIDATE_ONLY_PROTECTED_MASTER,
                "false",
            ),
            "protected master loses default-branch condition": (
                SUBMODULE_VALIDATE_ONLY_PROTECTED_MASTER,
                "(github.ref == 'refs/heads/master')",
            ),
            "protected-ref condition deleted": (
                SUBMODULE_VALIDATE_ONLY_PROTECTED_FLAG,
                "true",
            ),
            "protected-ref condition inverted": (
                SUBMODULE_VALIDATE_ONLY_PROTECTED_FLAG,
                "github.ref_protected != true",
            ),
            "unprotected master explicitly allowed": (
                SUBMODULE_VALIDATE_ONLY_PROTECTED_FLAG,
                "github.ref_protected == false",
            ),
            "master clause admits validate_only dispatch": (
                SUBMODULE_VALIDATE_ONLY_MASTER_EXCLUSION,
                "true",
            ),
            "scheduled run admitted through manual test gate": (
                SUBMODULE_VALIDATE_ONLY_EVENT,
                "github.event_name == 'schedule' && "
                "github.event.inputs.validate_only == 'true'",
            ),
            "resolver validates default branch instead of dispatched SHA": (
                SUBMODULE_VALIDATE_ONLY_CHECKOUT_REF,
                "ref: ${{ github.event.repository.default_branch }}",
            ),
            "resolver activation omits hosted-proof constraints": (
                f'if [ "${{{{ {SUBMODULE_VALIDATE_ONLY_MANUAL_PREDICATE} }}}}" = true ]; then',
                f'if [ "${{{{ {SUBMODULE_VALIDATE_ONLY_EVENT} }}}}" = true ]; then',
            ),
            "validate_only does not force existing gitlink validation": (
                'if [ "$validation_only" = true ]; then\n'
                "            changed=true\n"
                "          fi",
                'if [ "$validation_only" = true ]; then\n'
                "            changed=false\n"
                "          fi",
            ),
            "later resolver assignment cancels validate_only forcing": (
                "          {\n            printf 'candidate_sha=%s\\n'",
                "          changed=false\n          {\n            printf 'candidate_sha=%s\\n'",
            ),
            "publisher admits validate_only": (
                "needs.resolve-submodule-update.outputs.validation_only == 'false' &&",
                "needs.resolve-submodule-update.outputs.validation_only != 'true' &&",
            ),
            "resolver gains write permission": (
                "    permissions:\n      contents: read",
                "    permissions:\n      contents: write",
            ),
            "resolver receives publisher credential": (
                "    runs-on: ubuntu-latest",
                "    env:\n      GH_TOKEN: ${{ github.token }}\n    runs-on: ubuntu-latest",
            ),
            "publisher enables auto-merge": (
                "--draft",
                "--draft --auto",
            ),
            "outcome ignores resolver validation_only output": (
                "VALIDATION_ONLY: ${{ needs.resolve-submodule-update.outputs.validation_only }}",
                "VALIDATION_ONLY: ${{ needs.resolve-submodule-update.outputs.changed }}",
            ),
            "validate_only outcome requires publisher success": (
                'if [ "$CHANGED" != "true" ] || [ "$VALIDATOR_RESULT" != "success" ] || [ "$PUBLISHER_RESULT" != "skipped" ]; then',
                'if [ "$CHANGED" != "true" ] || [ "$VALIDATOR_RESULT" != "success" ] || [ "$PUBLISHER_RESULT" != "success" ]; then',
            ),
            "validate_only outcome falls through to publishing checks": (
                "              exit 0\n              ;;\n            false)",
                "              ;;\n            false)",
            ),
            "normal update accepts skipped publisher": (
                'if [ "$VALIDATOR_RESULT" != "success" ] || [ "$PUBLISHER_RESULT" != "success" ]; then',
                'if [ "$VALIDATOR_RESULT" != "success" ] || [ "$PUBLISHER_RESULT" != "skipped" ]; then',
            ),
        }
        for name, (original, replacement) in validate_only_mutations.items():
            with self.subTest(validate_only_mutation=name):
                self.assertIn(original, workflow)
                mutated = workflow.replace(original, replacement, 1)
                self.assertNotEqual(update_submodule_validate_only_errors(mutated), [])

        self.assertIn("submodules: false", publisher)
        self.assertEqual(sha256(publisher.encode("utf-8")).hexdigest(), SUBMODULE_PUBLISHER_SHA256)
        self.assertIn("persist-credentials: false", publisher)
        self.assertEqual(
            job_if_expression(publisher),
            SUBMODULE_PUBLISHER_GATE,
        )
        self.assertNotIn(SUBMODULE_VALIDATE_ONLY_CHECKOUT_REF, publisher)
        self.assertNotIn("gh pr merge", publisher)
        self.assertNotIn("--auto", publisher)
        self.assertNotIn("enablePullRequestAutoMerge", publisher)
        self.assertIn("git ls-remote --exit-code", publisher)
        self.assertTrue(has_exact_framework_gitlink_staging(publisher))
        self.assertIn("GH_TOKEN: ${{ github.token }}", publisher)
        self.assertIn("git read-tree \"$MASTER_HEAD\"", publisher)
        self.assertIn('git diff --cached --name-only "$MASTER_HEAD"', normalized_publisher)
        self.assertIn("require_only_submodule_path", publisher)
        self.assertIn("git diff --cached --raw --no-abbrev --no-renames", normalized_publisher)
        self.assertIn("CANDIDATE_SHA", publisher)
        self.assertIn("CURRENT_GITLINK_SHA", publisher)
        self.assertIn("MASTER_OLD_SHA", publisher)
        self.assertIn("Parent master Framework gitlink changed after resolution", publisher)
        self.assertIn("PR_MARKER", publisher)
        self.assertIn("--draft", publisher)
        self.assertIn(".auto_merge", publisher)
        self.assertIn("marker_count", publisher)
        self.assertIn("verify_open_pr_identity", publisher)
        self.assertIn("verify_open_draft_pr", publisher)
        self.assertIn("ensure_open_pr_is_draft", publisher)
        self.assertIn('gh pr ready "$pr_number" --repo "$GITHUB_REPOSITORY" --undo', publisher)
        self.assertLess(
            publisher.index('verify_open_pr_identity "$pr_number" "$expected_head"'),
            publisher.index('gh pr ready "$pr_number" --repo "$GITHUB_REPOSITORY" --undo'),
        )
        self.assertIn('[ "$pr_draft" != "true" ]', publisher)
        self.assertIn('[ "$pr_base_repo" != "$GITHUB_REPOSITORY" ]', publisher)
        self.assertIn('[ "$pr_head_repo" != "$GITHUB_REPOSITORY" ]', publisher)
        self.assertIn("verify_merged_pr", publisher)
        self.assertIn("require_single_updater_commit", publisher)
        self.assertIn("git rev-list --reverse", publisher)
        self.assertIn("read_matching_merged_pr", publisher)
        self.assertIn('case "$OPEN_PR_COUNT:$UPDATE_BRANCH_PRESENT" in', publisher)
        self.assertIn("BRANCH_STATE=A", publisher)
        self.assertIn("BRANCH_STATE=B", publisher)
        self.assertIn("BRANCH_STATE=C", publisher)
        self.assertIn("Unsafe maintenance branch/pull-request state", publisher)
        self.assertIn("Maintenance state changed before normal branch creation", publisher)
        self.assertIn("Maintenance branch or pull request changed before lease-bound update", publisher)
        self.assertIn("Maintenance branch or pull request changed before lease-bound reuse", publisher)
        self.assertIn(
            'git push --force-with-lease="refs/heads/$UPDATE_BRANCH:$EXPECTED_REMOTE_HEAD" origin "$NEW_COMMIT:refs/heads/$UPDATE_BRANCH"',
            publisher,
        )
        self.assertIn('git push origin "$NEW_COMMIT:refs/heads/$UPDATE_BRANCH"', publisher)
        self.assertNotIn("git checkout -B", publisher)
        self.assertNotIn("git push --force origin", publisher)
        self.assertNotIn("git push --force-with-lease origin", publisher)
        self.assertNotIn("git add ", publisher)
        self.assertNotIn("|| true", publisher)
        self.assertNotIn("continue-on-error", publisher)
        self.assertNotIn("GH_PAT", publisher)
        self.assertNotIn("PERSONAL_ACCESS_TOKEN", publisher)
        self.assertNotIn("DEPLOY_KEY", publisher)
        self.assertNotIn("submodules: recursive", publisher)
        self.assertNotIn("git submodule", publisher)
        self.assertNotIn("make quick-check", publisher)

        self.assertIn("RESOLVER_RESULT", outcome)
        self.assertIn("VALIDATOR_RESULT", outcome)
        self.assertIn("PUBLISHER_RESULT", outcome)
        self.assertIn("RESOLVER_STATUS", outcome)
        self.assertIn('case "$CHANGED" in', outcome)
        self.assertIn('false)', outcome)
        self.assertIn('"$VALIDATOR_RESULT" != "skipped"', outcome)
        self.assertIn('"$PUBLISHER_RESULT" != "skipped"', outcome)
        self.assertIn('true)', outcome)
        self.assertIn('"$VALIDATOR_RESULT" != "success"', outcome)
        self.assertIn('"$PUBLISHER_RESULT" != "success"', outcome)
        self.assertIn("Submodule resolver output is missing or malformed", outcome)
        self.assertIn("Submodule resolver changed output is missing or unexpected", outcome)
        self.assertIn(
            "The Framework submodule already points to the reviewed current master commit. No branch, commit, or pull request was created or modified.",
            outcome,
        )
        self.assertIn(
            "Das Framework-Submodule zeigt bereits auf den geprüften aktuellen Master-Commit. Es wurde kein Branch, Commit oder Pull Request erstellt oder verändert.",
            outcome,
        )
        self.assertNotIn("GH_TOKEN", outcome)
        self.assertNotIn("secrets.", outcome)
        self.assertNotIn("continue-on-error", outcome)

    def test_framework_gitlink_staging_contract_normalizes_layout_only(self) -> None:
        one_line = (
            'git update-index --add --cacheinfo '
            '"160000,$CANDIDATE_SHA,$SUBMODULE_PATH"'
        )
        continued = (
            "git update-index \\\n"
            "  --add \\\n"
            '  --cacheinfo "160000,$CANDIDATE_SHA,$SUBMODULE_PATH"'
        )
        self.assertTrue(has_exact_framework_gitlink_staging(one_line))
        self.assertTrue(has_exact_framework_gitlink_staging(continued))
        self.assertFalse(
            has_exact_framework_gitlink_staging(
                'git update-index --cacheinfo "160000,$CANDIDATE_SHA,$SUBMODULE_PATH"'
            )
        )
        self.assertFalse(
            has_exact_framework_gitlink_staging(
                'git update-index --add "160000,$CANDIDATE_SHA,$SUBMODULE_PATH"'
            )
        )
        self.assertFalse(
            has_exact_framework_gitlink_staging(
                'git update-index --add --cacheinfo "100644,$CANDIDATE_SHA,$SUBMODULE_PATH"'
            )
        )
        self.assertFalse(
            has_exact_framework_gitlink_staging(
                'git update-index --add --cacheinfo "160000,$CANDIDATE_SHA,$OTHER_PATH"'
            )
        )
        for broad_staging in ("git add .", "git add -A"):
            self.assertFalse(has_exact_framework_gitlink_staging(f"{one_line}\n{broad_staging}"))

    def test_framework_gitlink_raw_diff_contract_is_functional(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)

            def git(*arguments: str, input_text: str | None = None) -> str:
                return subprocess.run(
                    ["git", *arguments],
                    cwd=repository,
                    input=input_text,
                    text=True,
                    check=True,
                    capture_output=True,
                    env={
                        **os.environ,
                        "GIT_AUTHOR_NAME": "test",
                        "GIT_AUTHOR_EMAIL": "test@example.invalid",
                        "GIT_COMMITTER_NAME": "test",
                        "GIT_COMMITTER_EMAIL": "test@example.invalid",
                    },
                ).stdout.strip()

            git("init", "-q")
            empty_tree = git("mktree", input_text="")
            old_gitlink = git("commit-tree", empty_tree, "-m", "old target")
            new_gitlink = git("commit-tree", empty_tree, "-m", "new target")
            self.assertRegex(old_gitlink, r"^[0-9a-f]{40}$")
            self.assertRegex(new_gitlink, r"^[0-9a-f]{40}$")

            framework_path = "modules/ModSecurity-test-Framework"
            git("update-index", "--add", "--cacheinfo", f"160000,{old_gitlink},{framework_path}")
            parent_tree = git("write-tree")
            parent_commit = git("commit-tree", parent_tree, "-m", "parent")
            git("read-tree", parent_commit)
            git("update-index", "--add", "--cacheinfo", f"160000,{new_gitlink},{framework_path}")
            index_entry = git("ls-files", "--stage", "--", framework_path).split()
            self.assertEqual(index_entry[:2], ["160000", new_gitlink])

            raw = git("diff", "--cached", "--raw", "--no-abbrev", "--no-renames", parent_commit)
            records = raw.splitlines()
            expected = re.compile(
                rf"^:160000 160000 {old_gitlink} {new_gitlink} M\t{re.escape(framework_path)}$"
            )
            self.assertEqual(len(records), 1)
            self.assertRegex(records[0], expected)

            extra_blob = git("hash-object", "-w", "--stdin", input_text="extra\n")
            git("update-index", "--add", "--cacheinfo", f"100644,{extra_blob},extra.txt")
            widened_records = git(
                "diff", "--cached", "--raw", "--no-abbrev", "--no-renames", parent_commit
            ).splitlines()
            self.assertEqual(len(widened_records), 2)
            self.assertFalse(len(widened_records) == 1 and bool(expected.fullmatch(widened_records[0])))

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


class ConnectorModeWorkflowContractTest(unittest.TestCase):
    """Keep the static 20-cell connector-mode workflow family fail-closed."""

    @staticmethod
    def workflow_path(filename: str) -> Path:
        return WORKFLOWS / filename

    def load_workflow(self, filename: str) -> tuple[dict[str, object], str]:
        text = self.workflow_path(filename).read_text(encoding="utf-8")
        parsed = yaml.load(text, Loader=yaml.BaseLoader)
        self.assertIsInstance(parsed, dict, filename)
        return parsed, text

    def test_exact_static_topology_and_twenty_cells(self) -> None:
        actual_files = {
            path.name for path in WORKFLOWS.glob("test-connectors-*.yml")
        }
        self.assertEqual(actual_files, set(CONNECTOR_MODE_WORKFLOWS))

        observed_cells: dict[tuple[str, str, str], str] = {}
        for filename, expected in CONNECTOR_MODE_WORKFLOWS.items():
            with self.subTest(filename=filename):
                workflow, _text = self.load_workflow(filename)
                self.assertEqual(
                    set(workflow),
                    {"name", "on", "permissions", "concurrency", "jobs"},
                )
                self.assertEqual(workflow["name"], expected["name"])
                self.assertEqual(workflow["permissions"], {"contents": "read"})
                self.assertEqual(
                    workflow["concurrency"],
                    {"group": expected["name"], "cancel-in-progress": "false"},
                )
                self.assertEqual(set(workflow["jobs"]), {"connector-mode"})
                job = workflow["jobs"]["connector-mode"]
                self.assertNotIn("if", job)
                self.assertEqual(job["runs-on"], "ubuntu-latest")
                self.assertIn("${{ matrix.connector }}", job["name"])
                self.assertIn("${{ matrix.coverage_kind }}", job["name"])
                self.assertEqual(job["strategy"]["fail-fast"], "false")
                self.assertEqual(set(job["strategy"]["matrix"]), {"include"})
                rows = job["strategy"]["matrix"]["include"]
                self.assertEqual(len(rows), 5)
                self.assertEqual(
                    {row["connector"] for row in rows}, CONNECTOR_MODE_CONNECTORS
                )
                self.assertEqual(
                    {row["coverage_kind"] for row in rows}.difference(
                        CONNECTOR_MODE_COVERAGE_KINDS
                    ),
                    set(),
                )
                actual = {
                    row["connector"]: row["coverage_kind"]
                    for row in rows
                }
                self.assertEqual(actual, expected["cells"])
                self.assertEqual({row["crs"] for row in rows}, {expected["crs"]})
                self.assertEqual({row["mrts"] for row in rows}, {expected["mrts"]})
                self.assertEqual(len(actual), 5)
                for connector, coverage_kind in actual.items():
                    key = (connector, expected["crs"], expected["mrts"])
                    self.assertNotIn(key, observed_cells)
                    observed_cells[key] = coverage_kind

        expected_cells = {
            (connector, expected["crs"], expected["mrts"]): coverage_kind
            for expected in CONNECTOR_MODE_WORKFLOWS.values()
            for connector, coverage_kind in expected["cells"].items()
        }
        self.assertEqual(observed_cells, expected_cells)
        self.assertEqual(len(observed_cells), 20)
        self.assertNotIn("nginx", {key[0] for key in observed_cells})
        self.assertNotIn("_template", {key[0] for key in observed_cells})

    def test_no_crs_metadata_stays_equal_to_closed_profile(self) -> None:
        workflow, _text = self.load_workflow("test-connectors-no-crs-no-mrts.yml")
        rows = workflow["jobs"]["connector-mode"]["strategy"]["matrix"]["include"]
        expected_metadata = {
            "apache": (
                "full-lifecycle-low-latency",
                "native-httpd-module",
                "http1",
                "safe",
                "source-wiring-and-baseline-only",
            ),
            "envoy": (
                "request-only-compatibility",
                "http-ext-authz-service",
                "http1",
                "not_applicable",
                "no-response-host-path",
            ),
            "haproxy": (
                "header-compatibility",
                "spoe-spop-agent",
                "http1",
                "not_applicable",
                "no-response-body-host-path",
            ),
            "lighttpd": (
                "header-compatibility",
                "native-lighttpd-plugin",
                "http1",
                "not_applicable",
                "no-native-body-host-path",
            ),
            "traefik": (
                "request-only-compatibility",
                "http-forwardauth-service",
                "http1",
                "not_applicable",
                "no-response-host-path",
            ),
        }
        actual_metadata = {
            row["connector"]: (
                row["connector_profile"],
                row["integration_mode"],
                row["protocol"],
                row["phase4_mode"],
                row["evidence_scope"],
            )
            for row in rows
        }
        self.assertEqual(actual_metadata, expected_metadata)

    def test_triggers_are_pr_scoped_and_cover_shared_test_paths(self) -> None:
        for filename, expected in CONNECTOR_MODE_WORKFLOWS.items():
            with self.subTest(filename=filename):
                workflow, _text = self.load_workflow(filename)
                events = workflow["on"]
                self.assertEqual(set(events), {"pull_request", "workflow_dispatch"})
                pull_request = events["pull_request"]
                self.assertEqual(set(pull_request), {"branches", "paths"})
                self.assertEqual(pull_request["branches"], ["master"])
                paths = set(pull_request["paths"])
                self.assertIn(f".github/workflows/{filename}", paths)
                self.assertTrue(CONNECTOR_MODE_TRIGGER_PATHS.issubset(paths))
                self.assertNotIn("connectors/nginx/**", paths)

    def test_workflows_keep_the_pr_security_boundary_closed(self) -> None:
        for filename in CONNECTOR_MODE_WORKFLOWS:
            with self.subTest(filename=filename):
                workflow, text = self.load_workflow(filename)
                lowered = text.lower()
                self.assertEqual(workflow["permissions"], {"contents": "read"})
                for fragment in (
                    "pull_request_target:",
                    "workflow_run:",
                    "repository_dispatch:",
                    "github.event.inputs",
                    "inputs.",
                    "secrets.",
                    "github.token",
                    "$github_token",
                    "continue-on-error",
                    "|| true",
                    "sudo",
                    "actions/cache",
                    "restore-keys",
                    "upload-artifact@",
                ):
                    self.assertNotIn(fragment, lowered, fragment)
                self.assertNotIn("connector: nginx", lowered)
                self.assertNotIn("connectors/nginx", lowered)
                self.assertNotIn("nginx-root-broker", lowered)
                self.assertNotIn("fromJSON", text)
                self.assertNotIn("needs.", text)
                exact_head = "${{ github.event.pull_request.head.sha || github.sha }}"
                self.assertEqual(text.count(exact_head), 2)
                self.assertIn(f"ref: {exact_head}", text)
                self.assertIn(f"EXPECTED_PARENT_SHA: {exact_head}", text)
                self.assertEqual(
                    re.findall(r"\$\{\{\s*github\.event[^}]*\}\}", text),
                    [exact_head, exact_head],
                )
                self.assertEqual(len(checkout_step_blocks(text)), 1)
                self.assertIn("submodules: recursive", text)
                self.assertIn("persist-credentials: false", text)
                uses = re.findall(r"^\s*uses:\s+([^\s#]+)", text, re.MULTILINE)
                self.assertGreaterEqual(len(uses), 2)
                for action in uses:
                    self.assertRegex(action, r"^[^@]+@[0-9a-f]{40}$")

    def test_runtime_contract_and_negative_paths_have_honest_claims(self) -> None:
        no_crs, no_crs_text = self.load_workflow(
            "test-connectors-no-crs-no-mrts.yml"
        )
        self.assertIn("FIVE_CONNECTOR_PROFILE: no-crs", no_crs_text)
        self.assertIn("--verify-row", no_crs_text)
        self.assertIn('make "runtime-smoke-$CONNECTOR"', no_crs_text)
        self.assertIn('make "evidence-check-$CONNECTOR"', no_crs_text)
        self.assertIn("Check process cleanup", no_crs_text)
        self.assertNotIn("expected_unsupported", no_crs_text)
        self.assertEqual(
            no_crs["jobs"]["connector-mode"]["strategy"]["fail-fast"], "false"
        )

        contract, contract_text = self.load_workflow(
            "test-connectors-with-crs-no-mrts.yml"
        )
        self.assertIn("test-five-connectors-with-crs-no-mrts-contract", contract_text)
        self.assertIn("test-crs-provenance-contract", contract_text)
        self.assertIn("Install hash-locked Framework CI dependency", contract_text)
        self.assertIn(
            "--require-hashes -r modules/ModSecurity-test-Framework/requirements-ci.lock",
            contract_text,
        )
        self.assertIn("python3 -m pip check", contract_text)
        dependency_step = next(
            step
            for step in contract["jobs"]["connector-mode"]["steps"]
            if step["name"] == "Install hash-locked Framework CI dependency"
        )
        framework_revision_step = next(
            step
            for step in contract["jobs"]["connector-mode"]["steps"]
            if step["name"] == "Verify recorded Framework and MRTS revisions"
        )
        steps = contract["jobs"]["connector-mode"]["steps"]
        self.assertLess(
            steps.index(framework_revision_step), steps.index(dependency_step)
        )
        self.assertEqual(dependency_step["if"], "matrix.coverage_kind == 'contract'")
        self.assertEqual(
            dependency_step["run"].splitlines(),
            [
                "set -euo pipefail",
                "python3 -m pip install --disable-pip-version-check --no-input --only-binary=:all: \\",
                "  --require-hashes -r modules/ModSecurity-test-Framework/requirements-ci.lock",
                "python3 -m pip check",
            ],
        )
        self.assertIn("CONTRACT_VALIDATED", contract_text)
        self.assertIn("host_runtime_status=UNATTESTED", contract_text)
        for target in (
            "check-config-envoy",
            "check-config-lighttpd",
            "check-config-traefik",
        ):
            self.assertIn(f"make -n {target}", contract_text)
        self.assertNotIn("five-connectors-with-crs-no-mrts-validate", contract_text)
        self.assertNotIn("five-connectors-with-crs-no-mrts-aggregate", contract_text)
        self.assertNotIn("run-full-matrix-job.py", contract_text)
        self.assertEqual(
            contract["jobs"]["connector-mode"]["strategy"]["fail-fast"], "false"
        )

        for filename in (
            "test-connectors-no-crs-with-mrts.yml",
            "test-connectors-with-crs-with-mrts.yml",
        ):
            with self.subTest(filename=filename):
                _workflow, text = self.load_workflow(filename)
                self.assertIn("Prove current safe full-matrix rejection", text)
                self.assertIn('for candidate in "$CONNECTOR" unknown _template; do', text)
                self.assertIn('if python3 ci/runtime/lifecycle/run-full-matrix-job.py', text)
                self.assertIn('rejection_log="$CELL_ROOT/rejected-$candidate.stderr"', text)
                self.assertIn('if [ "$rc" -ne 2 ]; then', text)
                self.assertIn('"argument --connector: invalid choice:"', text)
                self.assertIn('test ! -e "$rejected_build_root"', text)
                self.assertNotIn("if: false", text)
                self.assertNotIn("exit 0", text)

        for filename in (
            "test-connectors-with-crs-no-mrts.yml",
            "test-connectors-no-crs-with-mrts.yml",
            "test-connectors-with-crs-with-mrts.yml",
        ):
            with self.subTest(filename=filename):
                _workflow, text = self.load_workflow(filename)
                self.assertIn(
                    'make verified-apache-case CASE=action_deny_phase1 CRS="$CRS" MRTS="$MRTS"',
                    text,
                )
                self.assertIn(
                    'make verified-haproxy-case CASE=action_deny_phase1 CRS="$CRS" MRTS="$MRTS"',
                    text,
                )
                self.assertIn("Verify focused runtime cleanup", text)

    def test_full_matrix_allowlist_and_recorded_gitlinks_remain_fixed(self) -> None:
        source = ROOT / "ci" / "runtime" / "lifecycle" / "run-full-matrix-job.py"
        tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
        connectors = None
        for statement in tree.body:
            if not isinstance(statement, ast.Assign):
                continue
            if any(
                isinstance(target, ast.Name) and target.id == "CONNECTORS"
                for target in statement.targets
            ):
                connectors = ast.literal_eval(statement.value)
                break
        self.assertEqual(connectors, {"apache", "haproxy", "nginx"})

        gitlink = subprocess.run(
            ["git", "ls-files", "-s", "--", "modules/ModSecurity-test-Framework"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            encoding="utf-8",
        ).stdout.strip()
        self.assertRegex(
            gitlink,
            rf"^160000 {CONNECTOR_MODE_FRAMEWORK_SHA} 0\tmodules/ModSecurity-test-Framework$",
        )
        for filename in CONNECTOR_MODE_WORKFLOWS:
            with self.subTest(filename=filename):
                _workflow, text = self.load_workflow(filename)
                self.assertIn(
                    f"EXPECTED_FRAMEWORK_SHA: {CONNECTOR_MODE_FRAMEWORK_SHA}", text
                )
                self.assertIn(f"EXPECTED_MRTS_SHA: {CONNECTOR_MODE_MRTS_SHA}", text)
                self.assertIn(
                    'mrts_commit=$(git -C modules/ModSecurity-test-Framework/tools/MRTS rev-parse HEAD)',
                    text,
                )
                self.assertIn('test "$mrts_commit" = "$EXPECTED_MRTS_SHA"', text)

        legacy_caller = (WORKFLOWS / "all-connectors-no-crs.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("workflow_dispatch:", legacy_caller)
        self.assertIn("schedule:", legacy_caller)
        self.assertNotIn("pull_request:", legacy_caller)


if __name__ == "__main__":
    unittest.main()
