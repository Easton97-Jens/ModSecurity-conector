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
LOCK_PATH = ROOT / "ci" / "tooling" / "security-tools.lock.yml"
LOCKED_ACTION_USE = re.compile(
    r"(?P<prefix>uses:\s+[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)?@)"
    r"(?P<sha>[a-f0-9]{40})(?:\s+#\s*v[^\n]+)?"
)
SUBMODULE_PUBLISHER_NORMALIZED_SHA256 = "486be1c4676f48e035b8f17ca7ec44f9651de539edc9620d83191f1052418bc6"
AUTO_MERGE_DISABLED_QUERY = (
    "--jq 'if (has(\"auto_merge\") and (.auto_merge == null)) then \"null\" "
    "else \"auto-merge-present\" end'"
)
READONLY_SUBMODULE_SANDBOX_CALL = " ".join(
    (
        "python3 ci/tools/prepare-readonly-submodule-validation-sandbox.py",
        '--source-root "$GITHUB_WORKSPACE"',
        '--framework-root "$GITHUB_WORKSPACE/modules/ModSecurity-test-Framework"',
        '--write-root "$VALIDATION_WRITE_ROOT"',
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
READONLY_SUBMODULE_CLEANUP_GATE = (
    "if: ${{ always() && steps.create-readonly-candidate-sandbox-guard.outputs.write_root != '' }}"
)
READONLY_SUBMODULE_CLEANUP_CALL = " ".join(
    (
        "python3 ci/tools/prepare-readonly-submodule-validation-sandbox.py",
        "--cleanup",
        '--source-root "$GITHUB_WORKSPACE"',
        '--framework-root "$GITHUB_WORKSPACE/modules/ModSecurity-test-Framework"',
        '--write-root "$VALIDATION_WRITE_ROOT"',
        '--runner-temp "$RUNNER_TEMP"',
    )
)
SUBMODULE_CANDIDATE_STATE_HELPER = "ci/tools/validate-submodule-candidate-state.py"
SUBMODULE_CANDIDATE_BASELINE_CALL = " ".join(
    (
        f"python3 {SUBMODULE_CANDIDATE_STATE_HELPER}",
        "capture-parent-baseline",
        '--parent-root "$GITHUB_WORKSPACE"',
        '--github-env "$GITHUB_ENV"',
    )
)
SUBMODULE_CANDIDATE_STATE_CALL = " ".join(
    (
        f"python3 {SUBMODULE_CANDIDATE_STATE_HELPER}",
        "validate",
        '--parent-root "$GITHUB_WORKSPACE"',
        '--submodule-path "$SUBMODULE_PATH"',
        '--current-gitlink-sha "$CURRENT_GITLINK_SHA"',
        '--candidate-sha "$CANDIDATE_SHA"',
        '--expected-parent-head "$EXPECTED_PARENT_HEAD"',
        '--expected-parent-hooks-sha256 "$EXPECTED_PARENT_HOOKS_SHA256"',
    )
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
SUBMODULE_VALIDATE_ONLY_RETIRED_PR280_BRANCH = (
    "github.ref == 'refs/heads/agent/framework-apr-util-submodule-validation'"
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
SUBMODULE_LOCAL_GIT_CONTRACT_TESTS = (
    "tests.test_validate_submodule_candidate_state",
    "tests.test_update_submodules_local_git",
    "tests.test_update_framework_versions",
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


def normalize_shell_script(script: str) -> str:
    """Normalize layout for static shell contracts without executing shell."""

    without_continuations = SHELL_CONTINUATION.sub(" ", script)
    return " ".join(without_continuations.split())


def assert_hash_locked_ci_test_dependency_installation(
    testcase: unittest.TestCase,
    validator: str,
    *,
    interpreter_contract_step: str,
    first_test_step: str,
) -> None:
    """Require the locked CI dependency before an import-sensitive workflow test."""

    normalized = normalize_shell_script(validator)
    install_step = "Install hash-locked CI test dependency"
    install_command = (
        "python3 -m pip install --disable-pip-version-check --no-input "
        "--only-binary=:all: --require-hashes -r requirements-ci.lock"
    )
    workflow_test = "tests.test_ci_security_workflows"

    testcase.assertIn(install_step, validator)
    testcase.assertIn(install_command, normalized)
    testcase.assertIn("python3 -m pip check", normalized)
    testcase.assertLess(
        validator.index(interpreter_contract_step),
        validator.index(install_step),
    )
    testcase.assertLess(validator.index(install_step), validator.index(first_test_step))
    testcase.assertLess(normalized.index(install_command), normalized.index("python3 -m pip check"))
    testcase.assertLess(normalized.index(install_command), normalized.index(workflow_test))
    testcase.assertLess(normalized.index("python3 -m pip check"), normalized.index(workflow_test))


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
        "Create private read-only candidate guard",
        "id: create-readonly-candidate-sandbox-guard",
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
        SUBMODULE_CANDIDATE_BASELINE_CALL,
        SUBMODULE_CANDIDATE_STATE_CALL,
        "VALIDATOR SOURCE MUTATION BLOCKED",
        "VALIDATOR WRITE-ROOT CONTRACT BLOCKED",
        "Enforce isolated candidate result after verification",
        "SANDBOX_PREPARE_RESULT: ${{ steps.prepare-readonly-candidate-sandbox.outcome }}",
        "CANDIDATE_RESULT: ${{ steps.run-readonly-candidate-namespace.outcome }}",
        'test "$SANDBOX_PREPARE_RESULT" = success',
        'test "$CANDIDATE_RESULT" = success',
        "git -c core.hooksPath=/dev/null diff --check",
        'git -c core.hooksPath=/dev/null -C "$SUBMODULE_PATH" diff --check',
        "printf 'write_root=%s\\n' \"$write_root\" >> \"$GITHUB_OUTPUT\"",
        "Clean up private read-only candidate guard",
        READONLY_SUBMODULE_CLEANUP_GATE,
        READONLY_SUBMODULE_CLEANUP_CALL,
        "READONLY_SUBMODULE_VALIDATION_SANDBOX_CLEANED",
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
        "git status --porcelain --untracked-files=all",
        "grep -v",
        "git reset --hard",
        "git clean",
        "|| true",
        "sudo -n python3 ci/tools/validate-submodule-candidate-state.py",
        "sudo -n git -c core.hooksPath=/dev/null diff --check",
        'sudo -n git -c core.hooksPath=/dev/null -C "$SUBMODULE_PATH" diff --check',
        "chown -R",
        "chmod -R",
        "$SUDO_USER",
        "$USER",
    )
    for term in forbidden:
        if term in validator:
            errors.append(f"workflow must delegate {term!r} exclusively to the namespace helper")

    namespace_count = normalized.count(READONLY_SUBMODULE_NAMESPACE_CALL)
    if namespace_count != 1:
        errors.append("workflow must invoke the namespace helper exactly once")
    if normalized.count("prepare-readonly-submodule-validation-sandbox.py") != 3:
        errors.append("sandbox helper must prepare, verify, and clean exactly once each")
    if normalized.count("umask 077") != 1:
        errors.append("only private guard creation may set the workflow umask")
    if "GH_TOKEN" in validator or "secrets." in validator or "github.token" in validator:
        errors.append("validator job must not receive credentials")
    if "--namespace-parent /tmp" in validator or "--namespace-parent /var/tmp" in validator:
        errors.append("namespace helper must not use a public namespace parent")
    if normalized.count(SUBMODULE_CANDIDATE_BASELINE_CALL) != 1:
        errors.append("candidate validation must capture exactly one immutable Parent baseline")
    if normalized.count(SUBMODULE_CANDIDATE_STATE_CALL) != 2:
        errors.append("candidate validation must run exactly before and after the namespace")

    verification_step = validator.partition(
        "- name: Verify candidate source inventory and external outputs"
    )[2].partition("- name: Enforce isolated candidate result after verification")[0]
    if READONLY_SUBMODULE_VERIFY_GATE not in verification_step:
        errors.append("physical verification must follow a failed candidate but not failed preparation")

    setup_index = normalized.find(READONLY_SUBMODULE_SANDBOX_CALL)
    namespace_index = normalized.find(READONLY_SUBMODULE_NAMESPACE_CALL)
    verification_index = normalized.find("Verify candidate source inventory and external outputs")
    result_index = normalized.find("Enforce isolated candidate result after verification")
    cleanup_index = normalized.find("Clean up private read-only candidate guard")
    if min(setup_index, namespace_index, verification_index, result_index, cleanup_index) < 0 or not (
        setup_index < namespace_index < verification_index < result_index < cleanup_index
    ):
        errors.append("guard preparation, candidate, verification, result gate, and cleanup must be ordered")
    baseline_index = normalized.find(SUBMODULE_CANDIDATE_BASELINE_CALL)
    checkout_index = normalized.find("checkout --detach")
    first_state_index = normalized.find(SUBMODULE_CANDIDATE_STATE_CALL)
    second_state_index = normalized.find(SUBMODULE_CANDIDATE_STATE_CALL, first_state_index + 1)
    if min(baseline_index, checkout_index, first_state_index, second_state_index) < 0 or not (
        baseline_index < checkout_index < first_state_index < setup_index < second_state_index < result_index
    ):
        errors.append("candidate-state validation must bracket the isolated namespace")
    return errors


def readonly_submodule_sandbox_helper_errors(helper: str) -> list[str]:
    """Return violations of the source-preserving root-side sandbox boundary."""

    errors: list[str] = []
    required = (
        'WRITE_ROOT_PREFIX = "modsecurity-readonly-validation."',
        "def _reject_nested_source_mounts",
        "def _mountinfo_mountpoints",
        "def cleanup_sandbox",
        "def _validate_cleanup_layout",
        "def _open_existing_directory_path",
        "os.O_NOFOLLOW",
        "dir_fd=",
        "source / \".git\"",
        "_reject_mounts_within(write, \"cleanup write root\", include_root=True)",
        "_source_regular_inodes",
        "external output hardlinks a source file",
        "READONLY_SUBMODULE_VALIDATION_SANDBOX_CLEANED",
    )
    for term in required:
        if term not in helper:
            errors.append(f"missing {term}")
    for term in ("_lock_tree", "shutil.", "rmtree", "os.system", "shell=True"):
        if term in helper:
            errors.append(f"source-preserving helper must not use {term!r}")
    try:
        syntax_tree = ast.parse(helper)
    except SyntaxError:
        return [*errors, "source-preserving helper must remain valid Python"]
    function_nodes = {
        node.name: node
        for node in syntax_tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    function_text = {
        name: "\n".join(helper.splitlines()[node.lineno - 1 : node.end_lineno])
        for name, node in function_nodes.items()
        if node.end_lineno is not None
    }
    for name in ("prepare_sandbox", "verify_sandbox"):
        body = function_text.get(name, "")
        if not body:
            errors.append(f"missing {name}")
            continue
        nested_mount_index = body.find("_reject_nested_source_mounts(source)")
        inventory_index = body.find("_source_inventory(source)")
        if min(nested_mount_index, inventory_index) < 0 or nested_mount_index > inventory_index:
            errors.append(f"{name} must reject nested source mounts before inventory use")
        for call in ast.walk(function_nodes[name]):
            if (
                isinstance(call, ast.Call)
                and isinstance(call.func, ast.Attribute)
                and isinstance(call.func.value, ast.Name)
                and call.func.value.id == "os"
                and call.func.attr in {"chown", "chmod", "fchown", "fchmod"}
            ):
                errors.append(f"{name} must not ownership- or mode-mutate the source tree")
    prepare = function_text.get("prepare_sandbox", "")
    if prepare.find("_source_inventory(source)") > prepare.find("_make_external_root(write, identity)"):
        errors.append("prepare must inventory source before creating external output")
    for name, node in function_nodes.items():
        for call in ast.walk(node):
            if not (
                isinstance(call, ast.Call)
                and isinstance(call.func, ast.Attribute)
                and isinstance(call.func.value, ast.Name)
                and call.func.value.id == "os"
                and call.func.attr in {"chown", "chmod"}
            ):
                continue
            if name != "_make_external_root":
                errors.append(f"{call.func.attr} is only allowed for the private external root")
    cleanup = function_text.get("cleanup_sandbox", "")
    if not cleanup or "_open_existing_directory_path(temporary)" not in cleanup:
        errors.append("cleanup must open the trusted temporary parent by descriptor")
    if not cleanup or "_remove_tree_contents(write_descriptor)" not in cleanup:
        errors.append("cleanup must unlink only descriptor-relative private contents")
    return errors


def readonly_namespace_runner_errors(runner: str) -> list[str]:
    """Return violations of the trusted private mount/PID/chroot launcher contract."""

    errors: list[str] = []
    required = (
        'PROCFS_TARGET = Path("/proc")',
        'JAIL_SOURCE = Path("/source")',
        'JAIL_EXTERNAL = Path("/external")',
        'JAIL_GUARD = Path("/guard")',
        'JAIL_DEV = Path("/dev")',
        "JAIL_RUNTIME_DIRECTORIES =",
        'JAIL_HOSTED_PYTHON_ROOT = Path("/opt/hostedtoolcache/Python")',
        'JAIL_HOSTED_PYTHON_ARCHITECTURE = "x64"',
        'JAIL_COMPILER_ROOT = Path("/usr")',
        'JAIL_C_COMPILER = Path("/usr/bin/gcc")',
        'JAIL_CXX_COMPILER = Path("/usr/bin/g++")',
        "JAIL_RUNTIME_ETC_FILES =",
        'JAIL_FORBIDDEN_PATH_COMPONENTS = ("tmp", "var", "home", "root", "run", "sys")',
        "CLONE_NEWNS | CLONE_NEWPID",
        "MS_NOEXEC = 8",
        "def _reject_nested_source_mounts",
        "_reject_nested_source_mounts(source)",
        "/proc/self/mountinfo",
        "source root contains an unexpected active mount",
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
        '_mount("tmpfs", mount_root, MS_NOSUID | MS_NODEV | MS_NOEXEC, "tmpfs")',
        '_mount("tmpfs", dev_view, MS_NOSUID | MS_NOEXEC, "tmpfs")',
        "_create_jail_device(dev_view / \"null\", 1, 3, 0o666)",
        "_create_jail_device(dev_view / \"urandom\", 1, 9, 0o444)",
        "_mount(str(source), source_view, MS_BIND)",
        "MS_BIND | MS_REMOUNT | MS_RDONLY | MS_NOSUID | MS_NODEV",
        "_mount(str(external), external_view, MS_BIND)",
        "MS_BIND | MS_REMOUNT | MS_NOSUID | MS_NODEV",
        "_verify_mount(source_view, readonly=True)",
        "_verify_mount(external_view, readonly=False)",
        "_mount(None, mount_root, MS_REMOUNT | MS_RDONLY | MS_NOSUID | MS_NODEV | MS_NOEXEC)",
        "_verify_mount(mount_root, readonly=True, require_noexec=True)",
        "_hosted_python_runtime_root(python)",
        "_validate_hosted_python_runtime(runtime_root)",
        '_fixed_runtime_executable(JAIL_C_COMPILER, "C compiler")',
        '_fixed_runtime_executable(JAIL_CXX_COMPILER, "C++ compiler")',
        "metadata.st_uid != 0",
        "stat.S_IWGRP | stat.S_IWOTH | stat.S_ISUID | stat.S_ISGID",
        "relative.parts[1] != JAIL_HOSTED_PYTHON_ARCHITECTURE",
        "hosted_python_root.relative_to(JAIL_ROOT).parts",
        "_bind_readonly(hosted_python_root, hosted_python_target)",
        "os.chdir(jail_root)",
        'os.chroot(".")',
        "_close_unapproved_descriptors({0, 1, 2, proc_ready_write})",
        "_replace_standard_input()",
        "_enter_jail(layout.root)",
        "os.setgroups([]); os.setgid(gid); os.setuid(uid); os.chdir(source)",
        "os.execve(\"/bin/bash\"",
        "READONLY_SUBMODULE_VALIDATION_NAMESPACE_COMPLETE",
        "if _mountinfo_for(mount_root) != before:",
        "os.rmdir(path)",
        'test "$PWD" = "$GITHUB_WORKSPACE"',
        'cap_eff=""; no_new_privs=""',
        "done < /proc/self/status",
        "0000000000000000",
        "NoNewPrivs:",
        "for component in JAIL_FORBIDDEN_PATH_COMPONENTS",
        "for target in /tmp /var /home /root /run /sys /dev/shm",
        "test -c /dev/null; test -c /dev/urandom; test ! -w /dev",
        "validator sees an unexpected device",
        'test -e "$descriptor" || continue',
        "validator retained an inherited descriptor",
        'if /usr/bin/mount -o remount,rw "$GITHUB_WORKSPACE"',
        '"HOME": str(root / "home")',
        '"TMPDIR": str(root / "tmp")',
        '"XDG_CACHE_HOME": str(root / "xdg-cache")',
        '"PIP_CACHE_DIR": str(root / "pip-cache")',
        '"PYTHONPYCACHEPREFIX": str(root / "pycache")',
        '"PYTHONUSERBASE": str(root / "python-user-base")',
        '"PYTHONPATH": str(root / "python-packages")',
        '"CC": str(compiler)',
        '"CXX": str(cxx_compiler)',
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
        ".readonly-validator-runtime-write-probe",
        ".readonly-validator-runtime-directory-probe",
        ".readonly-validator-runtime-rename-probe",
        "/dev/.readonly-validator-device-probe",
        "validator obtained sudo",
        'exec make PYTHON="$PYTHON" quick-check',
        '--target "$PYTHONPATH" --requirement "$GITHUB_WORKSPACE/ci/requirements/update-submodules-validation-linux-x86_64.txt"',
    )
    for term in required:
        if term not in runner:
            errors.append(f"missing {term}")
    for term in ("tempfile", "os.chmod(", "os.umask(", "BaseException"):
        if term in runner:
            errors.append(f"namespace runner must not use {term!r}")
    if 'exec make PYTHON="$PYTHON" BUILD_ROOT=' in runner:
        errors.append("namespace runner must pass BUILD_ROOT through the environment")
    if 'Path("/opt"),' in runner:
        errors.append("namespace runner must never expose the broad host /opt tree")
    for term in (
        "MS_REC | MS_BIND",
        "MNT_DETACH",
        "shutil.",
        "rmtree",
        "subprocess",
        "shell=True",
        "os.system",
        "secrets.token_hex",
        "awk ",
    ):
        if term in runner:
            errors.append(f"namespace runner must not use {term}")
    if runner.count("_mount(str(source), source_view, MS_BIND)") != 1:
        errors.append("namespace runner must create exactly one non-recursive source bind")
    if runner.count("_mount(str(external), external_view, MS_BIND)") != 1:
        errors.append("namespace runner must create exactly one non-recursive output bind")
    if runner.count("_teardown_jail_layout(layout)") != 1:
        errors.append("namespace runner must synchronously unmount the complete private jail")
    if runner.count('PROCFS_TARGET = Path("/proc")') != 1:
        errors.append("namespace runner must export one immutable literal candidate procfs target")

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
    configuration = functions.get("_validated_configuration", "")
    jail_builder = functions.get("_build_jail_layout", "")
    descriptor_closer = functions.get("_close_unapproved_descriptors", "")
    if not pid1_candidate:
        errors.append("namespace runner must retain the PID-one candidate helper")
    if not namespace_child:
        errors.append("namespace runner must retain the namespace child launcher")
        return errors
    nested_mount_index = configuration.find("_reject_nested_source_mounts(source)")
    external_index = configuration.find("if external != write_root / \"external\":")
    if not configuration or min(nested_mount_index, external_index) < 0 or nested_mount_index > external_index:
        errors.append("namespace runner must reject nested source mounts before setup")
    if not jail_builder or "_mount(\"tmpfs\", mount_root" not in jail_builder:
        errors.append("namespace runner must construct a private tmpfs jail before candidate execution")
    if (
        "_mount(None, source_view, MS_BIND | MS_REMOUNT | MS_RDONLY | MS_NOSUID | MS_NODEV)"
        not in jail_builder
    ):
        errors.append("namespace runner must remount the source view read-only inside the jail")
    if (
        "_mount(None, external_view, MS_BIND | MS_REMOUNT | MS_NOSUID | MS_NODEV)"
        not in jail_builder
    ):
        errors.append("namespace runner must retain nodev on the sole writable external view")
    if not descriptor_closer or "os.scandir(\"/proc/self/fd\")" not in descriptor_closer:
        errors.append("namespace runner must close unapproved inherited descriptors through fresh procfs")

    proc_mount = re.compile(
        r'''_mount\(\s*["']proc["']\s*,\s*layout\.proc\s*,\s*'''
        r"MS_RDONLY\s*\|\s*MS_NOSUID\s*\|\s*MS_NODEV\s*\|\s*MS_NOEXEC"
        r'''\s*,\s*["']proc["']\s*\)'''
    )
    proc_match = proc_mount.search(pid1_candidate)
    if proc_match is None:
        errors.append("namespace runner must mount a fresh readonly nosuid nodev noexec procfs inside the jail")
        return errors

    fork_index = namespace_child.find("child = os.fork()")
    layout_index = namespace_child.find("layout = _build_jail_layout(")
    helper_call_index = namespace_child.find("_run_pid1_candidate(", fork_index)
    proc_verify_index = pid1_candidate.find("_verify_procfs(layout.proc)")
    jail_index = pid1_candidate.find("_enter_jail(layout.root)")
    stdin_index = pid1_candidate.find("_replace_standard_input()")
    descriptor_index = pid1_candidate.find("_close_unapproved_descriptors({0, 1, 2, proc_ready_write})")
    readiness_write_index = pid1_candidate.find('os.write(proc_ready_write, b"1")')
    no_new_privs_index = pid1_candidate.find("_set_no_new_privs()")
    candidate_entry_index = pid1_candidate.find("candidate_entry(*candidate_arguments)")
    if min(
        fork_index,
        layout_index,
        helper_call_index,
        proc_verify_index,
        jail_index,
        stdin_index,
        descriptor_index,
        readiness_write_index,
        no_new_privs_index,
        candidate_entry_index,
    ) < 0 or not (
        layout_index < fork_index < helper_call_index
        and proc_match.start() < proc_verify_index < jail_index < stdin_index < descriptor_index
        < readiness_write_index < no_new_privs_index < candidate_entry_index
    ):
        errors.append("jail, descriptor closure, readiness, no_new_privs, and candidate order is unsafe")
    wait_index = namespace_child.find("os.waitpid(child, 0)")
    teardown_index = namespace_child.find("_teardown_jail_layout(layout)")
    readiness_read_index = namespace_child.find('proc_ready = os.read(proc_ready_read, 1) == b"1"')
    if min(readiness_read_index, wait_index, teardown_index) < 0 or not (
        readiness_read_index < wait_index < teardown_index
    ):
        errors.append("namespace runner must wait for PID one before tearing down the private jail")
    return errors


EXPECTED_WRITE_PERMISSIONS = {
    ("cleanup-artifacts.yml", "cleanup-artifacts"): {"actions": "write"},
    ("test-full-smoke-sequential.yml", "cleanup-artifacts"): {"actions": "write"},
    ("update-submodules.yml", "create-submodule-update-pr"): {
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
    if text.count(SUBMODULE_VALIDATE_ONLY_BRANCH) != 4:
        errors.append("repair-branch validation admission must have four exact branch checks")
    if SUBMODULE_VALIDATE_ONLY_RETIRED_PR280_BRANCH in text:
        errors.append("retired PR #280 validation-only branch must not be admitted")

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


def locked_action_pins() -> set[str]:
    """Return immutable Action SHAs from the current reviewed lock."""

    raw = yaml.safe_load(LOCK_PATH.read_text(encoding="utf-8"))
    actions = raw.get("pinned_actions", {}) if isinstance(raw, dict) else {}
    if not isinstance(actions, dict):
        raise AssertionError("workflow Action lock has no pinned_actions mapping")
    pins = {
        record.get("commit_sha")
        for record in actions.values()
        if isinstance(record, dict) and isinstance(record.get("commit_sha"), str)
    }
    if not pins or any(not re.fullmatch(r"[a-f0-9]{40}", pin) for pin in pins):
        raise AssertionError("workflow Action lock contains an invalid immutable pin")
    return pins


def locked_action_pin(name: str) -> str:
    """Return one exact Action reference prefix bound to the reviewed lock."""

    raw = yaml.safe_load(LOCK_PATH.read_text(encoding="utf-8"))
    actions = raw.get("pinned_actions", {}) if isinstance(raw, dict) else {}
    record = actions.get(name) if isinstance(actions, dict) else None
    if not isinstance(record, dict) or not isinstance(record.get("commit_sha"), str):
        raise AssertionError(f"workflow Action lock has no immutable pin for {name}")
    return f"{name}@{record['commit_sha']}"


def normalize_locked_action_pins(text: str) -> str:
    """Canonicalize only reviewed Action pins before a structural digest check."""

    pins = locked_action_pins()

    def replace(match: re.Match[str]) -> str:
        if match.group("sha") not in pins:
            return match.group(0)
        return f"{match.group('prefix')}<locked-action> # <locked-version>"

    return LOCKED_ACTION_USE.sub(replace, text)


class CiSecurityWorkflowTest(unittest.TestCase):
    def workflow(self, name: str) -> str:
        return (WORKFLOWS / name).read_text(encoding="utf-8")

    def workflow_paths(self) -> list[Path]:
        return sorted({path for pattern in WORKFLOW_PATTERNS for path in WORKFLOWS.glob(pattern)})

    def jobs(self, name: str) -> dict[str, str]:
        return job_blocks(self.workflow(name))

    def test_all_remote_actions_are_immutable_sha_pins(self) -> None:
        lock_data = yaml.safe_load(LOCK_PATH.read_text(encoding="utf-8"))
        locked_actions = (
            lock_data.get("pinned_actions", {}) if isinstance(lock_data, dict) else {}
        )
        self.assertIsInstance(locked_actions, dict)
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
                action_with_suffix, pinned_sha = reference.split("@", 1)
                action_name = "/".join(action_with_suffix.split("/")[:2])
                record = locked_actions.get(action_name)
                self.assertIsInstance(record, dict, f"{path}: {line}")
                self.assertEqual(
                    pinned_sha.split()[0],
                    record.get("commit_sha"),
                    f"{path}: {line}",
                )

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
        self.assertIn("printf '%s\\n' \"$version\" | awk", text)
        self.assertIn("NR == 1", text)
        self.assertNotIn('[[ ! "$version" =~', text)
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
        self.assertIn("define export_framework_optional_provenance", makefile)
        export_list = makefile.split("FRAMEWORK_OPTIONAL_PROVENANCE_EXPORTS :=", 1)[1]
        export_list = export_list.split("$(foreach", 1)[0]
        self.assertIn("PCRE2_SHA256", export_list)
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

    def test_pr_apr_util_provenance_job_is_unconditional_and_read_only(self) -> None:
        workflow = self.workflow("ci-security-workflow-lint.yml")
        jobs = self.jobs("ci-security-workflow-lint.yml")
        job = jobs["apr-util-provenance"]

        self.assertIn("  pull_request:\n", workflow)
        self.assertNotIn("    branches:", workflow.partition("  pull_request:\n")[2].partition("  push:")[0])
        self.assertNotIn("if:", job)
        self.assertEqual(job_permissions(job), {"contents": "read"})
        self.assertNotIn("secrets.", job)
        self.assertNotIn("github.token", job)
        checkout_steps = checkout_step_blocks(job)
        self.assertEqual(len(checkout_steps), 1)
        self.assertIn(locked_action_pin("actions/checkout"), checkout_steps[0])
        self.assertIn("submodules: recursive", checkout_steps[0])
        self.assertIn("persist-credentials: false", checkout_steps[0])
        self.assertIn(
            "python3 -m unittest -v tests.test_framework_apr_util_provenance tests.test_apr_util_static_contract",
            job,
        )
        self.assertIn(locked_action_pin("actions/setup-python"), job)
        self.assertIn("id: setup-python", job)
        self.assertIn("python-version-file: .python-version", job)
        self.assertIn("check-latest: false", job)
        self.assertIn(
            'python3 ci/checks/common/check-python-interpreter-contract.py --version-file .python-version --expected-python "$EXPECTED_PYTHON"',
            job,
        )
        self.assertNotIn("pip ", job)
        self.assertNotIn("curl ", job)
        self.assertNotIn("wget ", job)

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

    def test_ci_security_contracts_run_the_local_submodule_git_regressions(self) -> None:
        workflow = self.workflow("ci-security-workflow-lint.yml")
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        contract_target = makefile.partition("check-ci-security-contract:")[2].partition(
            "\n\n"
        )[0]
        for module in SUBMODULE_LOCAL_GIT_CONTRACT_TESTS:
            with self.subTest(module=module):
                self.assertIn(module, workflow)
                self.assertIn(module, contract_target)
        self.assertTrue((ROOT / SUBMODULE_CANDIDATE_STATE_HELPER).is_file())

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
        self.assertIn("submodules: false", validator)
        self.assertNotIn("submodules: recursive", validator)
        self.assertIn(READONLY_SUBMODULE_NAMESPACE_CALL, normalize_shell_script(validator))
        self.assertIn("remote get-url origin", validator)
        self.assertIn("merge-base --is-ancestor", validator)
        self.assertIn("checkout --detach", validator)
        self.assertIn(
            'git -c protocol.file.allow=never submodule update --init -- "$SUBMODULE_PATH"',
            validator,
        )
        self.assertNotIn("submodule update --init --recursive", validator)
        self.assertEqual(validator.count("Validate Framework component-pin data contract"), 1)
        self.assertIn("sync-framework-component-versions.py", validator)
        self.assertIn("--validate", validator)
        self.assertIn('"$CANDIDATE_SHA:ci/lib/common.sh"', validator)
        self.assertIn('git -c core.hooksPath=/dev/null -C "$SUBMODULE_PATH" show', validator)
        for forbidden in (
            'source "$framework_common"',
            '. "$framework_common"',
            'bash "$framework_common"',
            'sh "$framework_common"',
            'eval "$framework_common"',
            'python3 "$framework_common"',
        ):
            self.assertNotIn(forbidden, validator)
        component_pin_validator = validator.partition(
            "Prepare dedicated read-only candidate sandbox"
        )[0]
        self.assertNotIn("continue-on-error", component_pin_validator)
        self.assertLess(
            workflow.index("Validate Framework component-pin data contract"),
            workflow.index("Prepare dedicated read-only candidate sandbox"),
        )
        self.assertIn(SUBMODULE_CANDIDATE_BASELINE_CALL, normalize_shell_script(validator))
        self.assertEqual(normalize_shell_script(validator).count(SUBMODULE_CANDIDATE_STATE_CALL), 2)
        self.assertNotIn("status --porcelain", validator)
        self.assertNotIn("grep -v", validator)
        self.assertNotIn("git reset --hard", validator)
        self.assertNotIn("git clean", validator)
        self.assertNotIn("|| true", validator)
        self.assertTrue((ROOT / SUBMODULE_CANDIDATE_STATE_HELPER).is_file())
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
        sandbox_helper = (
            ROOT / "ci" / "tools" / "prepare-readonly-submodule-validation-sandbox.py"
        ).read_text(encoding="utf-8")
        self.assertEqual(readonly_submodule_sandbox_helper_errors(sandbox_helper), [])
        sandbox_helper_mutations = {
            "source locking returns": (
                "def _make_external_root",
                "def _lock_tree(root: Path) -> None:\n"
                "    for path, _relative, metadata in _walk_tree(root):\n"
                "        os.chown(path, 0, 0, follow_symlinks=False)\n"
                "        os.chmod(path, stat.S_IMODE(metadata.st_mode) & ~0o022)\n\n\n"
                "def _make_external_root",
            ),
            "nested source mount rejection removed": (
                "_reject_nested_source_mounts(source)",
                "_nested_source_mounts_not_checked(source)",
            ),
            "cleanup loses descriptor traversal": (
                "_open_existing_directory_path(temporary)",
                "os.open(temporary, os.O_RDONLY | os.O_DIRECTORY)",
            ),
        }
        for name, (original, replacement) in sandbox_helper_mutations.items():
            with self.subTest(sandbox_helper_mutation=name):
                self.assertIn(original, sandbox_helper)
                mutated = sandbox_helper.replace(original, replacement, 1)
                self.assertNotEqual(readonly_submodule_sandbox_helper_errors(mutated), [])

        candidate_state_mutations = {
            "missing immutable Parent baseline": (
                "capture-parent-baseline",
                "capture-parent-baseline-bypassed",
            ),
            "candidate state validated only once": (
                "validate \\\n            --parent-root",
                "validate-bypassed \\\n            --parent-root",
            ),
            "broad Parent status check restored": (
                "git -c core.hooksPath=/dev/null diff --check",
                "git status --porcelain --untracked-files=all\n          git -c core.hooksPath=/dev/null diff --check",
            ),
        }
        for name, (original, replacement) in candidate_state_mutations.items():
            with self.subTest(candidate_state_mutation=name):
                self.assertIn(original, validator)
                mutated = validator.replace(original, replacement, 1)
                self.assertNotEqual(readonly_submodule_validator_errors(mutated), [])

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
            "nested source mounts are accepted": (
                "_reject_nested_source_mounts(source)",
                "_nested_source_mounts_not_checked(source)",
            ),
            "source loses read-only remount": (
                "_mount(None, source_view, MS_BIND | MS_REMOUNT | MS_RDONLY | MS_NOSUID | MS_NODEV)",
                "_mount(None, source_view, MS_BIND | MS_REMOUNT | MS_NOSUID | MS_NODEV)",
            ),
            "output loses device restriction": (
                "_mount(None, external_view, MS_BIND | MS_REMOUNT | MS_NOSUID | MS_NODEV)",
                "_mount(None, external_view, MS_BIND | MS_REMOUNT | MS_NOSUID)",
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
            r'''_mount\(\s*["']proc["']\s*,\s*layout\.proc\s*,\s*'''
            r"MS_RDONLY\s*\|\s*MS_NOSUID\s*\|\s*MS_NODEV\s*\|\s*MS_NOEXEC"
            r'''\s*,\s*["']proc["']\s*\)''',
            namespace_runner,
        )
        self.assertIsNotNone(proc_match)
        assert proc_match is not None
        proc_mount = proc_match.group(0)
        jail_mutations = {
            "private procfs constant is mutable to another target": (
                'PROCFS_TARGET = Path("/proc")',
                'PROCFS_TARGET = Path("/proc-unsafe")',
            ),
            "private procfs is missing": (proc_mount, proc_mount.replace('"proc"', '"none"', 1)),
            "private procfs has executable flags": (proc_mount, proc_mount.replace("| MS_NOEXEC", "", 1)),
            "private jail root is missing": (
                '_mount("tmpfs", mount_root, MS_NOSUID | MS_NODEV | MS_NOEXEC, "tmpfs")',
                "pass",
            ),
            "candidate skips chroot": ('os.chroot(".")', "pass"),
            "candidate keeps inherited descriptors": (
                "_close_unapproved_descriptors({0, 1, 2, proc_ready_write})",
                "pass",
            ),
            "candidate can retain host temp paths": (
                "for target in /tmp /var /home /root /run /sys /dev/shm",
                "for target in /source",
            ),
            "parent skips jail teardown": ("_teardown_jail_layout(layout)", "pass"),
        }
        for name, (original, replacement) in jail_mutations.items():
            with self.subTest(name=name):
                self.assertIn(original, namespace_runner)
                mutated_runner = namespace_runner.replace(original, replacement, 1)
                self.assertNotEqual(readonly_namespace_runner_errors(mutated_runner), [])
        self.assertLess(
            validator.index("Create private read-only candidate guard"),
            validator.index("Prepare dedicated read-only candidate sandbox"),
        )
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
        self.assertLess(
            validator.index("Enforce isolated candidate result after verification"),
            validator.index("Clean up private read-only candidate guard"),
        )
        self.assertIn(READONLY_SUBMODULE_SANDBOX_CALL, normalize_shell_script(validator))
        self.assertIn(READONLY_SUBMODULE_WRITE_ROOT, validator)
        self.assertIn(READONLY_SUBMODULE_EXTERNAL_ROOT, validator)
        self.assertNotIn("setfacl", validator)
        self.assertNotIn("getfacl", validator)
        self.assertNotIn("sudo -n -u modsecurity-validator", validator)
        self.assertNotIn("sudo -n python3 ci/tools/validate-submodule-candidate-state.py", validator)
        self.assertNotIn("sudo -n git -c core.hooksPath=/dev/null diff --check", validator)

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
            "private guard cleanup is no longer unconditional": (
                READONLY_SUBMODULE_CLEANUP_GATE,
                "if: ${{ success() }}",
            ),
            "private guard cleanup is removed": (
                "Clean up private read-only candidate guard",
                "Private guard cleanup removed",
            ),
            "private guard cleanup loses its fixed prefix contract": (
                "--cleanup",
                "--cleanup-disabled",
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
        self.assertEqual(
            sha256(normalize_locked_action_pins(publisher).encode("utf-8")).hexdigest(),
            SUBMODULE_PUBLISHER_NORMALIZED_SHA256,
        )
        self.assertIn("persist-credentials: false", publisher)
        self.assertIn("id: setup-python", publisher)
        self.assertIn(
            "EXPECTED_PYTHON: ${{ steps.setup-python.outputs.python-path }}",
            publisher,
        )
        self.assertIn(
            "python3 ci/checks/common/check-python-interpreter-contract.py "
            "--version-file .python-version --expected-python \"$EXPECTED_PYTHON\"",
            publisher,
        )
        self.assertIn("grep -Fqx", publisher)
        self.assertIn('-e "$SUBMODULE_PATH"', publisher)
        self.assertNotIn('case "$changed_path" in', publisher)
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
        self.assertIn("require_only_allowed_update_paths", publisher)
        self.assertIn("require_expected_update_raw", publisher)
        self.assertIn("git diff --cached --raw --no-abbrev --no-renames", normalized_publisher)
        self.assertIn("CANDIDATE_SHA", publisher)
        self.assertIn("CURRENT_GITLINK_SHA", publisher)
        self.assertIn("MASTER_OLD_SHA", publisher)
        self.assertIn("Parent master Framework gitlink changed after resolution", publisher)
        self.assertIn("PR_MARKER", publisher)
        self.assertIn("--draft", publisher)
        self.assertIn(".auto_merge", publisher)
        self.assertIn(
            "pr_auto_merge=\"$(gh api --method GET "
            "\"repos/$GITHUB_REPOSITORY/pulls/$pr_number\" "
            "--jq 'if (has(\"auto_merge\") and (.auto_merge == null)) then \"null\" "
            "else \"auto-merge-present\" end')\"",
            publisher,
        )
        self.assertIn(AUTO_MERGE_DISABLED_QUERY, publisher)
        self.assertNotIn(".auto_merge //", publisher)
        self.assertIn('has("auto_merge")', publisher)
        self.assertIn('else "auto-merge-present" end', publisher)
        for state_name, payload, expected in (
            ("present JSON null", {"auto_merge": None}, "null"),
            ("boolean false", {"auto_merge": False}, "auto-merge-present"),
            ("string null", {"auto_merge": "null"}, "auto-merge-present"),
            ("enabled object", {"auto_merge": {}}, "auto-merge-present"),
            ("missing field", {}, "auto-merge-present"),
        ):
            with self.subTest(auto_merge_state=state_name):
                normalized = (
                    "null"
                    if "auto_merge" in payload and payload["auto_merge"] is None
                    else "auto-merge-present"
                )
                self.assertEqual(normalized, expected)
        self.assertIn('[ "$pr_auto_merge" = "null" ] && auto_merge_present=false', publisher)
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
        self.assertIn("sync-framework-component-versions.py", publisher)
        self.assertIn("--sync", publisher)
        self.assertIn("--check", publisher)
        self.assertIn("python3 scripts/generate_compiler_guides.py", publisher)
        self.assertIn("docs/build/compilers/lighttpd.de.md", publisher)
        self.assertIn('git -c core.hooksPath=/dev/null add --', publisher)
        self.assertNotIn("git add .", publisher)
        self.assertNotIn("git add -A", publisher)
        self.assertNotIn("|| true", publisher)
        self.assertNotIn("continue-on-error", publisher)
        self.assertNotIn("GH_PAT", publisher)
        self.assertNotIn("PERSONAL_ACCESS_TOKEN", publisher)
        self.assertNotIn("DEPLOY_KEY", publisher)
        self.assertNotIn("submodules: recursive", publisher)
        self.assertIn(
            'git -c protocol.file.allow=never submodule update --init -- "$SUBMODULE_PATH"',
            publisher,
        )
        self.assertNotIn("submodule update --init --recursive", publisher)
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

    def test_workflow_tool_updater_is_the_sole_parent_only_action_maintainer(self) -> None:
        for retired_path in (
            WORKFLOWS / "check-actions-versions.yml",
            WORKFLOWS / "update-actions-versions.yml",
            ROOT / "scripts/check-github-actions-versions.py",
            ROOT / "scripts/update-github-actions-versions.py",
        ):
            self.assertFalse(retired_path.exists(), retired_path)

        dependabot = (ROOT / ".github/dependabot.yml").read_text(encoding="utf-8")
        self.assertNotIn('package-ecosystem: "github-actions"', dependabot)
        self.assertIn('package-ecosystem: "pip"', dependabot)

        workflow_name = "update-workflow-tools.yml"
        workflow = self.workflow(workflow_name)
        jobs = self.jobs(workflow_name)
        self.assertEqual(set(jobs), {"resolver", "validator", "publisher", "outcome"})
        publisher = jobs["publisher"]
        for required_guard in (
            "github.repository == 'Easton97-Jens/ModSecurity-conector'",
            "github.event.repository.fork == false",
            "github.event.repository.default_branch == 'master'",
            "github.ref == 'refs/heads/master'",
        ):
            self.assertIn(required_guard, publisher)
        for job_name in ("resolver", "validator", "publisher"):
            for checkout in checkout_step_blocks(jobs[job_name]):
                self.assertIn("submodules: false", checkout, job_name)
                self.assertNotIn("submodules: recursive", checkout, job_name)
        for forbidden in (
            "SUBMODULE_UPDATE_TOKEN",
            "modules/ModSecurity-test-Framework",
            "git submodule",
            "module_repo",
            "automation/update-github-actions-versions",
        ):
            self.assertNotIn(forbidden, workflow)

    def test_python_patch_updater_separates_trusted_stages_and_writer_scope(self) -> None:
        workflow_name = "update-python-version.yml"
        workflow = self.workflow(workflow_name)
        jobs = self.jobs(workflow_name)
        self.assertEqual(
            set(jobs),
            {
                "resolve-python-patch",
                "validate-python-patch",
                "publish-python-update",
                "report-python-update-outcome",
            },
        )
        self.assertEqual(top_level_permissions(workflow), {"contents": "read"})
        self.assertIn(
            "group: modsecurity-conector-python-version-maintenance-${{ github.repository }}",
            workflow,
        )
        self.assertIn("cancel-in-progress: false", workflow)
        for disallowed_trigger in (
            "push:",
            "pull_request:",
            "pull_request_target:",
            "workflow_run:",
            "repository_dispatch:",
        ):
            self.assertNotIn(f"  {disallowed_trigger}", workflow)
        self.assertIn("- cron: '17 6 * * 1'", workflow)
        self.assertIn("  workflow_dispatch:", workflow)

        canonical_gate_terms = {
            "github.repository == 'Easton97-Jens/ModSecurity-conector'",
            "github.event.repository.fork == false",
            "github.event.repository.default_branch == 'master'",
            "github.ref == 'refs/heads/master'",
            "github.event_name == 'schedule'",
            "github.event_name == 'workflow_dispatch'",
        }
        for job_name in (
            "resolve-python-patch",
            "validate-python-patch",
            "publish-python-update",
        ):
            expression = job_if_expression(jobs[job_name])
            self.assertIsNotNone(expression, job_name)
            for term in canonical_gate_terms:
                self.assertIn(term, expression, job_name)
            checkouts = checkout_step_blocks(jobs[job_name])
            self.assertEqual(len(checkouts), 1, job_name)
            self.assertIn("ref: ${{ github.sha }}", checkouts[0], job_name)
            self.assertIn("fetch-depth: 1", checkouts[0], job_name)
            self.assertIn("submodules: false", checkouts[0], job_name)
            self.assertIn("persist-credentials: false", checkouts[0], job_name)

        self.assertNotIn("secrets.", jobs["resolve-python-patch"])
        self.assertNotIn("secrets.", jobs["validate-python-patch"])

        self.assertEqual(job_permissions(jobs["resolve-python-patch"]), {"contents": "read"})
        self.assertEqual(job_permissions(jobs["validate-python-patch"]), {"contents": "read"})
        publisher = jobs["publish-python-update"]
        self.assertEqual(job_permissions(publisher), {"contents": "read"})
        self.assertIn("needs.resolve-python-patch.outputs.update_available == 'true'", publisher)
        self.assertIn("needs.validate-python-patch.result == 'success'", publisher)
        self.assertIn("WORKFLOW_UPDATER_APP_CLIENT_ID", publisher)
        self.assertIn("WORKFLOW_UPDATER_APP_PRIVATE_KEY", publisher)
        self.assertIn("::error::WORKFLOW_UPDATER_APP_CLIENT_ID", publisher)
        self.assertIn("::error::WORKFLOW_UPDATER_APP_PRIVATE_KEY", publisher)
        self.assertIn(locked_action_pin("actions/create-github-app-token"), publisher)
        self.assertIn("permission-contents: write", publisher)
        self.assertIn("permission-pull-requests: write", publisher)
        self.assertNotIn("permission-workflows:", publisher)
        self.assertNotIn("permission-actions:", publisher)
        self.assertNotIn("permission-issues:", publisher)
        self.assertNotIn("github.token", publisher)
        self.assertNotIn("GH_TOKEN:", publisher)
        for job_name, job in jobs.items():
            if job_name != "publish-python-update":
                self.assertNotIn("WORKFLOW_UPDATER_APP_CLIENT_ID", job, job_name)
                self.assertNotIn("WORKFLOW_UPDATER_APP_PRIVATE_KEY", job, job_name)

        self.assertNotIn("submodules: recursive", publisher)
        self.assertNotIn("git submodule", publisher)
        self.assertNotIn("gh ", publisher)
        self.assertNotIn("scripts/select-python-update-pr.py", publisher)
        self.assertNotIn("grep -Eq", publisher)
        self.assertNotIn("re.compile", publisher)
        publisher_normalized = normalize_shell_script(publisher)
        publisher_install_step = "Install hash-locked CI test dependency"
        publisher_install_command = (
            "python3 -m pip install --disable-pip-version-check --no-input "
            "--only-binary=:all: --require-hashes -r requirements-ci.lock"
        )
        self.assertIn(publisher_install_step, publisher)
        self.assertIn(publisher_install_command, publisher_normalized)
        self.assertIn("python3 -m pip check", publisher_normalized)
        self.assertLess(
            publisher.index("Verify Python interpreter contract"),
            publisher.index(publisher_install_step),
        )
        self.assertLess(
            publisher.index(publisher_install_step),
            publisher.index("Mint repository-limited Python updater App token"),
        )
        self.assertLess(
            publisher.index(publisher_install_step),
            publisher.index("Revalidate current master before modifying it"),
        )
        self.assertLess(
            publisher_normalized.index(publisher_install_command),
            publisher_normalized.index("python3 -m pip check"),
        )
        self.assertLess(
            publisher_normalized.index("python3 -m pip check"),
            publisher_normalized.index("make check-ci-security-contract"),
        )
        self.assertIn(
            'python3 scripts/update-python-version.py --check --expected-version "$CANDIDATE_VERSION" --json',
            publisher,
        )
        self.assertIn(
            'python3 scripts/update-python-version.py --update --expected-version "$CANDIDATE_VERSION" --json',
            publisher,
        )
        self.assertIn("UPDATE_BRANCH: automation/update-python-314", publisher)
        self.assertIn('PR_TITLE: "chore(ci): propose Python 3.14 patch update"', publisher)
        self.assertIn('PR_MARKER: "<!-- modsecurity-conector-python-314-updater -->"', publisher)
        self.assertIn("FRAMEWORK_REFERENCE_SHA: 3cb33609626ff689c54b6dc0f31fb7e9401fe75e", publisher)
        self.assertIn('git fetch --no-tags origin "refs/heads/$DEFAULT_BRANCH:refs/remotes/origin/$DEFAULT_BRANCH"', publisher)
        self.assertIn('git reset --hard "origin/$DEFAULT_BRANCH"', publisher)
        self.assertIn('branch_paths="$(git diff --name-only "$merge_base" "origin/$UPDATE_BRANCH")"', publisher)
        self.assertIn('if [ "$branch_paths" != ".python-version" ]; then', publisher)
        self.assertIn('"--force-with-lease=refs/heads/$UPDATE_BRANCH:$EXPECTED_REMOTE_TIP"', publisher)
        self.assertNotRegex(publisher, r"git push\s+--force(?:\s|$)")
        self.assertNotRegex(publisher, r"git push\s+--force-with-lease(?:\s|$)")
        self.assertNotIn('origin "HEAD:refs/heads/master"', publisher)
        self.assertNotIn("pulls.merge", publisher)
        self.assertNotIn("gh pr merge", publisher)
        self.assertIn("github.rest.git.listMatchingRefs", publisher)
        self.assertIn("github.paginate(github.rest.pulls.list", publisher)
        self.assertIn("pullRequest.head.repo?.full_name !== repository", publisher)
        self.assertIn("pullRequest.base.repo?.full_name !== repository", publisher)
        self.assertIn("pullRequest.auto_merge !== null", publisher)
        self.assertIn("draft: true", publisher)
        self.assertIn("Recheck the matching Draft pull request after publication", publisher)
        self.assertIn("pullRequest.head.sha !== process.env.EXPECTED_HEAD_SHA", publisher)
        self.assertIn('changed_paths="$(git diff --name-only "origin/$DEFAULT_BRANCH" --)"', publisher)
        self.assertIn("if [ \"$changed_paths\" != \".python-version\" ]; then", publisher)
        self.assertIn('git add -- .python-version', publisher)
        self.assertIn('staged_paths="$(git diff --cached --name-only)"', publisher)
        self.assertIn('if [ "$staged_paths" != ".python-version" ]; then', publisher)
        self.assertIn("git diff --cached --check", publisher)
        self.assertNotIn("git add -A", publisher)
        self.assertNotIn("git add .", publisher)
        self.assertIn("UPDATE_CHANGED: ${{ steps.update.outputs.changed }}", publisher)
        self.assertIn('if [ "$UPDATE_CHANGED" != true ]; then', publisher)
        self.assertNotIn('if [ "${{ steps.update.outputs.changed }}" != true ]; then', publisher)
        self.assertIn("## English", publisher)
        self.assertIn("## Deutsch", publisher)
        self.assertIn("Automatic merge remains disabled.", publisher)
        self.assertIn("Automatischer Merge bleibt deaktiviert.", publisher)

        resolver = jobs["resolve-python-patch"]
        self.assertIn("status: ${{ steps.resolve.outputs.status }}", resolver)
        self.assertIn("current_version: ${{ steps.resolve.outputs.current_version }}", resolver)
        self.assertIn("latest_version: ${{ steps.resolve.outputs.latest_version }}", resolver)
        self.assertIn("update_available: ${{ steps.resolve.outputs.update_available }}", resolver)
        self.assertIn('scripts/update-python-version.py --check --json', resolver)
        self.assertNotIn("re.compile", resolver)
        self.assertNotIn("grep -Eq", resolver)

        candidate = jobs["validate-python-patch"]
        assert_hash_locked_ci_test_dependency_installation(
            self,
            candidate,
            interpreter_contract_step="Verify Python candidate interpreter contract",
            first_test_step="Run focused Python version contracts",
        )
        self.assertIn("python-version: ${{ needs.resolve-python-patch.outputs.latest_version }}", candidate)
        self.assertIn("check-latest: false", candidate)
        self.assertIn("python3 -m compileall -q ci scripts tests", candidate)
        self.assertIn("make check-ci-security-contract", candidate)
        self.assertIn(
            'check-python-interpreter-contract.py --expected-version "$EXPECTED_VERSION" --expected-python "$EXPECTED_PYTHON"',
            candidate,
        )
        self.assertIn(
            'scripts/update-python-version.py --check --expected-version "$CANDIDATE_VERSION" --json',
            candidate,
        )

        outcome = jobs["report-python-update-outcome"]
        self.assertEqual(job_permissions(outcome), {})
        self.assertEqual(job_if_expression(outcome), "always()")
        self.assertNotIn("secrets.", outcome)
        self.assertNotIn("publisher_app_token", outcome)
        self.assertIn("case \"$UPDATE_AVAILABLE\" in", outcome)
        self.assertIn("No Python 3.14 patch update is available.", outcome)
        self.assertIn("Kein Python-3.14-Patch-Update ist verfügbar.", outcome)

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
        assert_hash_locked_ci_test_dependency_installation(
            self,
            candidate,
            interpreter_contract_step="Verify Python interpreter contract",
            first_test_step="Run Go version and workflow contracts",
        )
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
        self.assertIn(AUTO_MERGE_DISABLED_QUERY, publisher)
        self.assertIn('if [ "$auto_merge" != "null" ]; then', publisher)
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
