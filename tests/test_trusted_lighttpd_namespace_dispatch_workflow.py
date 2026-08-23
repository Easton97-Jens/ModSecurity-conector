"""Static trust contracts for the protected Lighttpd namespace dispatcher."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/run-trusted-lighttpd-namespace-dispatch.yml"
EXPECTED_REPOSITORY = "Easton97-Jens/ModSecurity-conector"
TRUSTED_ORIGIN = "https://github.com/Easton97-Jens/ModSecurity-conector.git"
RUNTIME_ROOT = "/var/lib/trusted-lighttpd-namespace"
SOURCE_ROOT = f"{RUNTIME_ROOT}/source"
TEMP_ROOT = f"{RUNTIME_ROOT}/tmp"
GIT_TEMPLATE_ROOT = f"{RUNTIME_ROOT}/empty-git-template"
SOURCE_NAMESPACE_RUNNER = f"{RUNTIME_ROOT}/run-source-namespace.sh"
SOURCE_TEST_RUNNER = f"{RUNTIME_ROOT}/run-source-test.sh"


def require_markers(errors: list[str], text: str, label: str, markers: tuple[str, ...]) -> None:
    """Record each missing static control without treating source text as execution."""

    for marker in markers:
        if marker not in text:
            errors.append(f"missing {label}: {marker}")


def require_order(errors: list[str], text: str, label: str, markers: tuple[str, ...]) -> None:
    """Require an ordered fixed sequence inside one trusted workflow slice."""

    if any(marker not in text for marker in markers):
        errors.append(f"missing ordered {label}")
        return
    positions = [text.index(marker) for marker in markers]
    if positions != sorted(positions):
        errors.append(f"invalid {label} order")


def trusted_dispatch_errors(text: str) -> list[str]:
    """Return violations of the protected-master PR-code trust boundary."""

    errors: list[str] = []
    if not text.startswith("name: Trusted Lighttpd Namespace Dispatch\n"):
        errors.append("workflow name")

    trigger_match = re.search(r"(?ms)^on:\n(?P<body>.*?)(?=^permissions:\n)", text)
    if trigger_match is None:
        errors.append("workflow trigger section")
        trigger_body = ""
    else:
        trigger_body = trigger_match.group("body")
        triggers = re.findall(r"(?m)^  ([A-Za-z_][A-Za-z0-9_-]*):", trigger_body)
        if triggers != ["workflow_dispatch"]:
            errors.append("workflow must have only workflow_dispatch")
        inputs = re.findall(r"(?m)^      ([A-Za-z_][A-Za-z0-9_-]*):", trigger_body)
        if inputs != ["target"]:
            errors.append("workflow must expose only target")
        require_markers(
            errors,
            trigger_body,
            "workflow target input contract",
            (
                "Open canonical PR number or its full lowercase 40-character head SHA.",
                "        required: true",
                "        type: string",
            ),
        )

    for forbidden in (
        "pull_request:",
        "pull_request_target:",
        "push:",
        "workflow_call:",
        "workflow_run:",
        "repository_dispatch:",
        "actions/cache",
        "actions/upload-artifact",
        "actions/download-artifact",
        "secrets.",
        "GH_TOKEN",
        "continue-on-error",
        "|| true",
        "exit 0",
        "--unshare-user-try",
        "--privileged",
        "docker run",
        "sysctl",
        "uses: ./",
    ):
        if forbidden in text:
            errors.append(f"forbidden workflow content: {forbidden}")

    if not re.search(r"(?m)^permissions:\n  contents: read\n", text):
        errors.append("top-level contents-read permission")
    if text.count("${{ inputs.target }}") != 1 or "          TARGET: ${{ inputs.target }}" not in text:
        errors.append("target must enter shell only through one environment value")

    require_markers(
        errors,
        text,
        "protected-master boundary",
        (
            "github.event_name == 'workflow_dispatch'",
            f"github.repository == '{EXPECTED_REPOSITORY}'",
            "github.event.repository.fork == false",
            "github.ref == 'refs/heads/master'",
            "github.event.repository.default_branch == 'master'",
            "github.ref_protected == true",
            "github.actor == 'Easton97-Jens'",
            "github.triggering_actor == 'Easton97-Jens'",
            "runs-on: ubuntu-24.04",
            "permissions:\n      contents: read",
            "timeout-minutes: 45",
            "cancel-in-progress: false",
        ),
    )
    require_markers(
        errors,
        text,
        "trusted bootstrap control",
        (
            "for directory in / /usr /usr/bin /usr/sbin /etc /var /var/lib; do",
            "/usr/bin/apt-get update",
            "apparmor-utils bubblewrap jq",
            "kernel/apparmor_restrict_unprivileged_userns",
            'test "$userns_restriction" = 1',
            "profile trusted-lighttpd-ci-userns flags=(unconfined) {",
            "  userns,",
            "/usr/sbin/apparmor_parser --replace /etc/apparmor.d/trusted-lighttpd-ci-userns",
            "/usr/sbin/aa-status --enabled",
            "/usr/bin/sudo -n /usr/bin/aa-exec -p trusted-lighttpd-ci-userns -- ",
            'case "$(/usr/bin/cat /proc/self/attr/current)" in',
            "trusted-lighttpd-ci-userns\\ *)",
            "BLOCKED: trusted AppArmor profile was not entered.",
            "/usr/sbin/useradd --create-home --user-group --home-dir /home/ns-test",
            'test "$(/usr/bin/id -G ns-test)" = "$ns_test_gid"',
            f"{RUNTIME_ROOT}/tmp",
            "-m 0700",
            "--disable-userns",
            "--assert-userns-disabled",
            "/usr/bin/unshare --help | /usr/bin/grep -F -- '--keep-caps' >/dev/null",
        ),
    )
    if "/usr/sbin/aa-status --profiled" in text:
        errors.append("aa-status --profiled cannot prove that the named profile is loaded")
    if "/var/tmp/trusted-lighttpd-namespace" in text:
        errors.append("trusted runtime root must not use the public /var/tmp parent")
    for forbidden_profile_term in (
        "capability,",
        " mount,",
        " umount,",
        " ptrace,",
        " network,",
        "change_profile",
        "/**",
        " ux",
    ):
        if forbidden_profile_term in text:
            errors.append(f"AppArmor profile is broader than userns: {forbidden_profile_term}")

    bootstrap_marker = "      - name: Bootstrap constrained namespace host before any checkout"
    resolve_marker = "      - id: resolve-target"
    test_marker = "      - name: Materialize and run the namespace test only as constrained ns-test"
    report_marker = "  report-trusted-lighttpd-namespace:"
    require_markers(
        errors,
        text,
        "ordered workflow step",
        (bootstrap_marker, resolve_marker, test_marker, report_marker),
    )
    if all(marker in text for marker in (bootstrap_marker, resolve_marker, test_marker, report_marker)):
        require_order(
            errors,
            text,
            "workflow step",
            (bootstrap_marker, resolve_marker, test_marker, report_marker),
        )
        bootstrap_step = text[text.index(bootstrap_marker) : text.index(resolve_marker)]
        require_markers(
            errors,
            bootstrap_step,
            "complete pre-materialization constrained probe",
            (
                "/usr/bin/sudo -n /usr/bin/aa-exec -p trusted-lighttpd-ci-userns -- ",
                'case "$(/usr/bin/cat /proc/self/attr/current)" in',
                "trusted-lighttpd-ci-userns\\ *)",
                "BLOCKED: trusted AppArmor profile was not entered.",
                "# Prove the complete constrained ns-test boundary before checkout.",
                "fail_preflight() {",
                "BLOCKED: preflight.$1",
                "/usr/bin/setpriv",
                "-- /usr/bin/env -i",
                'test "$current_uid" != 0',
                'test "$current_euid" != 0',
                'test "$current_gid" != 0',
                'test "$current_egid" != 0',
                "NoNewPrivs",
                "CapInh CapPrm CapEff CapBnd CapAmb",
                "fail_preflight apparmor_profile",
                "fail_preflight docker_socket",
                "fail_preflight user_mount_pid_namespace",
                "fail_preflight host_mount_leak",
                "fail_preflight bubblewrap_user_pid_namespace",
                "/usr/bin/unshare --user --map-root-user --mount --pid --fork",
                "/usr/bin/mount --make-rprivate /",
                "/usr/bin/bwrap --unshare-user --unshare-pid --disable-userns --assert-userns-disabled",
            ),
        )
        if "/usr/bin/sudo -n /usr/bin/setpriv" in bootstrap_step:
            errors.append("pre-materialization setpriv must enter the named AppArmor profile")
        if any(forbidden in bootstrap_step for forbidden in ("GITHUB_WORKSPACE", "SOURCE_COPY")):
            errors.append("bootstrap must not consume a PR source path")

    require_markers(
        errors,
        text,
        "API-bound exact target control",
        (
            "https://api.github.com/repos/$expected_repository",
            'if [[ "$target" =~ ^[0-9a-f]{40}$ ]]; then',
            'elif [[ "$target" =~ ^[1-9][0-9]*$ ]]; then',
            '"$api_root/commits/$target"',
            '"$api_root/commits/$target/pulls"',
            "commit_sha=\"$(printf '%s' \"$commit_response\" | /usr/bin/jq -er '.sha')\"",
            'test "$commit_sha" = "$target"',
            '"$api_root/pulls/$target"',
            "select(.state == \"open\")",
            "select(.base.ref == \"master\")",
            "select(.base.repo.full_name == $expected_repository)",
            "select(.head.repo.full_name == $expected_repository)",
            "select(.head.sha == $expected_sha)",
            "commit SHA does not bind exactly one open canonical master PR",
            "TARGET_SHA: ${{ steps.resolve-target.outputs.target_sha }}",
        ),
    )
    if "ref: ${{ inputs.target }}" in text or "${{ inputs.target }}" in text.replace(
        "          TARGET: ${{ inputs.target }}", ""
    ):
        errors.append("unvalidated target used outside the resolver environment")

    resolver_match = re.search(
        r"(?ms)^      - id: resolve-target\n(?P<body>.*?)(?=^      - name: Materialize and run the namespace test only as constrained ns-test)",
        text,
    )
    if resolver_match is None:
        errors.append("public API resolver boundary")
        resolver = ""
    else:
        resolver = resolver_match.group("body")
    if re.search(r"--retry 3 --retry-delay 1 --retry-max-time 30(?:\s|$)", resolver) is None:
        errors.append("missing bounded public API retry")
    if "--retry 0" in resolver:
        errors.append("public API resolver must retry bounded transient errors")
    if "--retry-all-errors" in resolver:
        errors.append("public API resolver must not retry non-transient errors")

    trusted_job_match = re.search(
        r"(?ms)^  trusted-lighttpd-namespace:\n(?P<body>.*?)(?=^  report-trusted-lighttpd-namespace:)",
        text,
    )
    if trusted_job_match is None:
        errors.append("trusted test job boundary")
        trusted_job = ""
    else:
        trusted_job = trusted_job_match.group("body")
    source_runner_match = re.search(
        r"(?ms)<<'TRUSTED_SOURCE_RUNNER'\n(?P<body>.*?)^[ \t]*TRUSTED_SOURCE_RUNNER$",
        trusted_job,
    )
    if source_runner_match is None:
        errors.append("root-owned source runner boundary")
        source_runner = ""
    else:
        source_runner = source_runner_match.group("body")
    source_namespace_match = re.search(
        r"(?ms)<<'TRUSTED_SOURCE_NAMESPACE'\n(?P<body>.*?)^[ \t]*TRUSTED_SOURCE_NAMESPACE$",
        trusted_job,
    )
    if source_namespace_match is None:
        errors.append("root-owned source namespace helper boundary")
        source_namespace_runner = ""
    else:
        source_namespace_runner = source_namespace_match.group("body")
    require_markers(
        errors,
        trusted_job,
        "trusted job output",
        ("outputs:\n      target_sha: ${{ steps.resolve-target.outputs.target_sha }}",),
    )
    if "GITHUB_TOKEN" in trusted_job or "github.token" in trusted_job:
        errors.append("trusted PR-code job must not receive a write token")
    if re.search(r"(?m)^      [A-Za-z-]+:\s*write\s*$", trusted_job):
        errors.append("trusted PR-code job must not receive write permissions")
    for forbidden in ("actions/checkout", "GITHUB_WORKSPACE", "SOURCE_COPY"):
        if forbidden in trusted_job:
            errors.append(f"trusted job must not use runner-workspace PR source: {forbidden}")

    report_job_match = re.search(
        r"(?ms)^  report-trusted-lighttpd-namespace:\n(?P<body>.*)\Z",
        text,
    )
    if report_job_match is None:
        errors.append("status reporting job boundary")
        report_job = ""
    else:
        report_job = report_job_match.group("body")
    require_markers(
        errors,
        report_job,
        "isolated status-reporting control",
        (
            "needs: trusted-lighttpd-namespace",
            "always() &&",
            "needs.trusted-lighttpd-namespace.outputs.target_sha != ''",
            "permissions:\n      statuses: write",
            "runs-on: ubuntu-24.04",
            "timeout-minutes: 5",
            "TARGET_SHA: ${{ needs.trusted-lighttpd-namespace.outputs.target_sha }}",
            "TRUSTED_TEST_RESULT: ${{ needs.trusted-lighttpd-namespace.result }}",
            "GITHUB_TOKEN: ${{ github.token }}",
            '[[ ! "$TARGET_SHA" =~ ^[0-9a-f]{40}$ ]]',
            "status_state=success",
            "status_state=failure",
            "status_state=error",
            "context\\\":\\\"trusted-lighttpd-namespace",
            "https://api.github.com/repos/Easton97-Jens/ModSecurity-conector/statuses/$TARGET_SHA",
        ),
    )
    for forbidden in (
        "actions/checkout",
        "sudo",
        "secrets.",
        "inputs.target",
        "GITHUB_WORKSPACE",
        "SOURCE_ROOT",
        "SOURCE_COPY",
        "actions/cache",
        "artifact",
    ):
        if forbidden in report_job:
            errors.append(f"status reporter must not use PR source or privileged content: {forbidden}")
    if re.search(r"(?m)^\s*-\s*uses:", report_job):
        errors.append("status reporter must not load an action")
    if re.search(r"(?m)^      (?!statuses:)[A-Za-z-]+:\s*write\s*$", report_job):
        errors.append("status reporter must have only statuses: write")
    if text.count("--retry 0") != 1:
        errors.append("only the side-effecting status POST may retain retry 0")
    if re.search(r"--retry 0\s*\\\n\s*--request POST", report_job) is None:
        errors.append("status reporter POST must retain retry 0")
    if re.search(r"--retry (?!0(?:\s|\\|$))", report_job):
        errors.append("status reporter POST must not use a nonzero retry policy")

    require_markers(
        errors,
        trusted_job,
        "trusted source helper installation and invocation",
        (
            f"/usr/bin/sudo -n /usr/bin/tee {SOURCE_TEST_RUNNER}",
            "<<'TRUSTED_SOURCE_RUNNER'",
            f"require_trusted_system_file {SOURCE_TEST_RUNNER}",
            f"/usr/bin/sudo -n /usr/bin/tee {SOURCE_NAMESPACE_RUNNER}",
            "<<'TRUSTED_SOURCE_NAMESPACE'",
            f"require_trusted_system_file {SOURCE_NAMESPACE_RUNNER}",
            "/usr/bin/sudo -n /usr/bin/env -i",
            'NS_TEST_UID="$ns_test_uid"',
            'NS_TEST_GID="$ns_test_gid"',
            'TARGET_SHA="$TARGET_SHA"',
            "/usr/bin/aa-exec -p trusted-lighttpd-ci-userns -- ",
            f"/usr/bin/dash -eu {SOURCE_NAMESPACE_RUNNER}",
            "BLOCKED: runtime.source_namespace_execution",
            "BLOCKED: runtime.source_namespace_mount_leak",
            "BLOCKED: runtime.source_namespace_temp_mount_leak",
        ),
    )
    require_markers(
        errors,
        source_runner,
        "restricted direct source materialization",
        (
            "fail_runtime() {",
            "BLOCKED: runtime.$1",
            "NoNewPrivs",
            "CapInh CapPrm CapEff CapBnd CapAmb",
            'test "$current_groups" = "$NS_TEST_GID" || fail_runtime supplemental_groups',
            'test "$(/usr/bin/readlink /proc/self/ns/user)" != "$HOST_USER_NAMESPACE"',
            'test "$(/usr/bin/readlink /proc/self/ns/mnt)" != "$HOST_MOUNT_NAMESPACE"',
            'test "$(/usr/bin/readlink /proc/self/ns/pid)" != "$HOST_PID_NAMESPACE"',
            'test "$$" = 1',
            f"TEMP_ROOT={TEMP_ROOT}",
            'test "$TMPDIR" = "$TEMP_ROOT"',
            'test "$TMP" = "$TEMP_ROOT"',
            'test "$TEMP" = "$TEMP_ROOT"',
            'test "$LIGHTTPD_NAMESPACE_TEST_TEMP_PARENT" = "$TEMP_ROOT"',
            "run_git() {",
            "capture_git() {",
            "/usr/bin/timeout --signal=TERM --kill-after=5s 120s /usr/bin/git",
            'test "$TRUSTED_ORIGIN" = "https://github.com/Easton97-Jens/ModSecurity-conector.git"',
            r'printf "%s\\n" "$TARGET_SHA" | /usr/bin/grep -Eq "^[0-9a-f]{40}$"',
            'run_git init --quiet --template="$GIT_TEMPLATE_ROOT" "$SOURCE_ROOT"',
            'run_git -C "$SOURCE_ROOT" fetch --no-tags --depth=1 --no-recurse-submodules "$TRUSTED_ORIGIN" "$TARGET_SHA"',
            'run_git -C "$SOURCE_ROOT" cat-file -e "${TARGET_SHA}^{commit}"',
            'run_git -C "$SOURCE_ROOT" fsck --strict --connectivity-only',
            'run_git -C "$SOURCE_ROOT" checkout --quiet --detach "$TARGET_SHA"',
            'capture_git -C "$SOURCE_ROOT" rev-parse HEAD',
            r'run_git -C "$SOURCE_ROOT" config --local --get-regexp "^http\\..*\\.extraheader$"',
            'run_git -C "$SOURCE_ROOT" config --local --get-all credential.helper',
            'test -d "$SOURCE_ROOT/.git"',
            'test ! -L "$SOURCE_ROOT/.git"',
            '/usr/bin/rm -rf --one-file-system -- "$SOURCE_ROOT/.git"',
            'test ! -e "$SOURCE_ROOT/.git"',
            'source_symlink="$(/usr/bin/find -P "$SOURCE_ROOT" -type l -print -quit)"',
            'test -z "$source_symlink"',
            'cd "$SOURCE_ROOT"',
            "/usr/bin/python3 -m unittest -v connectors.lighttpd.tests.test_no_crs_fixture_namespace",
            'temporary_entry="$(/usr/bin/find -P "$TEMP_ROOT" -mindepth 1 -maxdepth 1 -print -quit)"',
            'test -z "$temporary_entry"',
            'exit "$test_status"',
        ),
    )
    require_markers(
        errors,
        source_namespace_runner,
        "root-owned private source mount and privilege drop",
        (
            "SOURCE_ROOT=/var/lib/trusted-lighttpd-namespace/source",
            f"TEMP_ROOT={TEMP_ROOT}",
            "GIT_TEMPLATE_ROOT=/var/lib/trusted-lighttpd-namespace/empty-git-template",
            f"TRUSTED_ORIGIN={TRUSTED_ORIGIN}",
            "fail_namespace() {",
            "test \"$(/usr/bin/id -u)\" = 0",
            "source_root_not_empty",
            "/usr/bin/find -P \"$SOURCE_ROOT\" -mindepth 1 -maxdepth 1 -print -quit",
            "temporary_root_not_empty",
            "/usr/bin/find -P \"$TEMP_ROOT\" -mindepth 1 -maxdepth 1 -print -quit",
            "/usr/bin/unshare --mount --pid --fork --kill-child=SIGKILL",
            "/usr/bin/mount --make-rprivate /",
            "uid=$NS_TEST_UID,gid=$NS_TEST_GID,mode=0700,nosuid,nodev,noexec,size=256m",
            "uid=$NS_TEST_UID,gid=$NS_TEST_GID,mode=0700,nosuid,nodev,noexec,size=128m",
            "/usr/bin/grep -F \" $SOURCE_ROOT \" /proc/self/mountinfo | /usr/bin/grep -F \" - tmpfs \"",
            "/usr/bin/grep -F \" $TEMP_ROOT \" /proc/self/mountinfo | /usr/bin/grep -F \" - tmpfs \"",
            "/usr/bin/grep -Eq \"(shared:|master:)\"",
            "exec /usr/bin/setpriv",
            '--reuid="$NS_TEST_UID"',
            '--regid="$NS_TEST_GID"',
            "--clear-groups",
            "--no-new-privs",
            "--inh-caps=-all",
            "--ambient-caps=-all",
            "--bounding-set=-all",
            "/usr/bin/env -i",
            "GIT_ALLOW_PROTOCOL=https",
            "GIT_CONFIG_NOSYSTEM=1",
            "GIT_CONFIG_SYSTEM=/dev/null",
            "GIT_CONFIG_GLOBAL=/dev/null",
            "GIT_CONFIG_KEY_0=core.hooksPath",
            "GIT_CONFIG_VALUE_0=/dev/null",
            "GIT_CONFIG_KEY_1=credential.helper",
            "GIT_CONFIG_VALUE_1=",
            "GIT_CONFIG_KEY_2=protocol.file.allow",
            "GIT_CONFIG_VALUE_2=never",
            "GIT_LFS_SKIP_SMUDGE=1",
            "GIT_TERMINAL_PROMPT=0",
            "LIGHTTPD_REQUIRE_NAMESPACE_INTEGRATION=1",
            "LIGHTTPD_REQUIRE_UNPRIVILEGED_TEST_RUNNER=1",
            f"LIGHTTPD_NAMESPACE_TEST_TEMP_PARENT=\"$TEMP_ROOT\"",
            "/usr/bin/unshare --user --map-current-user --map-group=\"$NS_TEST_GID\" --keep-caps --mount --pid --fork --kill-child=SIGKILL",
            f"/usr/bin/dash -eu {SOURCE_TEST_RUNNER}",
        ),
    )
    require_markers(
        errors,
        source_runner,
        "runtime bounded diagnostics",
        (
            "fail_runtime apparmor_profile",
            "fail_runtime docker_socket",
            "fail_runtime user_namespace",
            "fail_runtime mount_namespace",
            "fail_runtime pid_namespace",
            "fail_runtime source_namespace_mount",
            "fail_runtime source_namespace_propagation",
            "fail_runtime temporary_namespace_mount",
            "fail_runtime temporary_namespace_propagation",
            "fail_runtime target_sha",
            "fail_runtime git_origin",
            "fail_runtime source_root",
            "fail_runtime source_root_symlink",
            "fail_runtime source_root_owner_mode",
            "fail_runtime temporary_root",
            "fail_runtime temporary_root_symlink",
            "fail_runtime temporary_root_owner_mode",
            "fail_runtime temporary_root_environment",
            "fail_runtime temporary_root_not_empty",
            "fail_runtime git_template_root",
            "fail_runtime git_template_root_symlink",
            "fail_runtime git_template_not_empty",
            "fail_runtime git_init",
            "fail_runtime git_fetch",
            "fail_runtime git_object",
            "fail_runtime git_fsck",
            "fail_runtime git_checkout",
            "fail_runtime git_head",
            "fail_runtime git_http_credential_header",
            "fail_runtime git_credential_helper",
            "fail_runtime git_state",
            "fail_runtime git_state_removal",
            "fail_runtime source_symlink",
        ),
    )
    if not re.search(r"(?m)^\s*GIT_CONFIG_VALUE_1=[ \t]*\\$", source_namespace_runner):
        errors.append("credential helper must be set to an explicit empty value")
    require_order(
        errors,
        source_namespace_runner,
        "private mount before non-root source execution",
        (
            "/usr/bin/unshare --mount --pid --fork --kill-child=SIGKILL",
            "/usr/bin/mount --make-rprivate /",
            "uid=$NS_TEST_UID,gid=$NS_TEST_GID,mode=0700,nosuid,nodev,noexec,size=256m",
            "uid=$NS_TEST_UID,gid=$NS_TEST_GID,mode=0700,nosuid,nodev,noexec,size=128m",
            "exec /usr/bin/setpriv",
            "--clear-groups",
            "-- /usr/bin/env -i",
            "/usr/bin/unshare --user --map-current-user --map-group=\"$NS_TEST_GID\" --keep-caps --mount --pid --fork",
            "--keep-groups",
            f"/usr/bin/dash -eu {SOURCE_TEST_RUNNER}",
        ),
    )
    require_order(
        errors,
        source_runner,
        "root-owned source runner",
        (
            'run_git init --quiet --template="$GIT_TEMPLATE_ROOT" "$SOURCE_ROOT"',
            '/usr/bin/rm -rf --one-file-system -- "$SOURCE_ROOT/.git"',
            'cd "$SOURCE_ROOT"',
            "/usr/bin/python3 -m unittest -v connectors.lighttpd.tests.test_no_crs_fixture_namespace",
            "test_status=$?",
            'exit "$test_status"',
        ),
    )
    test_command = "/usr/bin/python3 -m unittest -v connectors.lighttpd.tests.test_no_crs_fixture_namespace"
    if test_command in source_runner:
        post_test_runner = source_runner[source_runner.index(test_command) :]
        require_order(
            errors,
            post_test_runner,
            "temporary-root cleanup attestation",
            (
                test_command,
                "test_status=$?",
                'temporary_entry="$(/usr/bin/find -P "$TEMP_ROOT" -mindepth 1 -maxdepth 1 -print -quit)"',
                'test -z "$temporary_entry"',
                'exit "$test_status"',
            ),
        )
    if "-depth -delete" in trusted_job or "cleanup_source()" in trusted_job:
        errors.append("trusted source teardown must not delete a same-UID writable path")
    if any(marker in source_namespace_runner for marker in ("run_git()", "python3", "rm -rf", "-depth -delete")):
        errors.append("root source namespace helper must not consume PR source")
    if "--keep-caps" in source_runner:
        errors.append("source runner must not retain setup capabilities across exec")
    source_capability_finalizer_pattern = (
        r'/usr/bin/unshare --user --map-current-user --map-group="\$NS_TEST_GID" '
        r'--keep-caps --mount --pid --fork --kill-child=SIGKILL --mount-proc=/proc '
        r'--propagation private[ \t]*\\[ \t]*\n[ \t]*'
        r'/usr/bin/setpriv[ \t]*\\[ \t]*\n[ \t]*'
        r'--reuid="\$NS_TEST_UID"[ \t]*\\[ \t]*\n[ \t]*'
        r'--regid="\$NS_TEST_GID"[ \t]*\\[ \t]*\n[ \t]*'
        r'--keep-groups[ \t]*\\[ \t]*\n[ \t]*'
        r'--no-new-privs[ \t]*\\[ \t]*\n[ \t]*'
        r'--inh-caps=-all[ \t]*\\[ \t]*\n[ \t]*'
        r'--ambient-caps=-all[ \t]*\\[ \t]*\n[ \t]*'
        r'--bounding-set=-all[ \t]*\\[ \t]*\n[ \t]*'
        rf'-- /usr/bin/dash -eu {re.escape(SOURCE_TEST_RUNNER)}'
    )
    if source_namespace_runner.count("--keep-caps") != 1:
        errors.append("source namespace must retain capabilities only for one trusted finalizer transition")
    if re.search(source_capability_finalizer_pattern, source_namespace_runner) is None:
        errors.append("source namespace must drop recreated capabilities before the source runner")
    if text.count("/usr/bin/sudo -n") != 13:
        errors.append("unexpected privileged command inventory")
    if text.count("/usr/bin/sudo -n /usr/bin/aa-exec -p trusted-lighttpd-ci-userns -- ") != 2:
        errors.append("unexpected named-AppArmor launcher inventory")
    if text.count("/usr/bin/timeout --signal=TERM --kill-after=5s 120s /usr/bin/git") != 2:
        errors.append("all Git operations must use the bounded launcher")
    if text.count(TRUSTED_ORIGIN) != 2:
        errors.append("all source-materialization origin uses must remain fixed")
    if text.count("CapInh CapPrm CapEff CapBnd CapAmb") != 2:
        errors.append("every non-root execution boundary must verify all capability sets")
    if text.count('/usr/bin/grep -F " $SOURCE_ROOT " /proc/self/mountinfo | /usr/bin/grep -F " - tmpfs "') != 2:
        errors.append("source tmpfs must be proven inside the private mount and source runner")
    if text.count('/usr/bin/grep -F " $TEMP_ROOT " /proc/self/mountinfo | /usr/bin/grep -F " - tmpfs "') != 2:
        errors.append("temporary tmpfs must be proven inside the private mount and source runner")
    if text.count('/usr/bin/grep -Eq "(shared:|master:)"') != 5:
        errors.append("every namespace probe and private mount must reject shared propagation")
    if len(re.findall(r"(?<![A-Za-z0-9-])--no-new-privs(?![A-Za-z0-9-])", text)) != 3:
        errors.append("every non-root privilege drop, including the user-namespace finalizer, must set no_new_privs")
    if text.count("--clear-groups") != 2:
        errors.append("both pre-user-namespace privilege drops must clear supplemental groups")
    if source_namespace_runner.count("--keep-groups") != 1 or text.count("--keep-groups") != 1:
        errors.append("the user-namespace finalizer must preserve only the already-cleared group state")
    inner_finalizer_start = source_namespace_runner.find(
        '/usr/bin/unshare --user --map-current-user --map-group="$NS_TEST_GID" --keep-caps'
    )
    if inner_finalizer_start < 0 or "--clear-groups" in source_namespace_runner[inner_finalizer_start:]:
        errors.append("the mapped user-namespace finalizer must not call denied setgroups")
    if "--groups=" in source_namespace_runner or "--init-groups" in source_namespace_runner:
        errors.append("the source namespace must not initialize or add supplementary groups")
    for capability_drop in ("--inh-caps=-all", "--ambient-caps=-all", "--bounding-set=-all"):
        if text.count(capability_drop) != 3:
            errors.append(f"every non-root privilege drop, including the user-namespace finalizer, must retain {capability_drop}")
    if text.count("/usr/bin/unshare --user --map-root-user --mount --pid --fork") != 1:
        errors.append("the pre-materialization user/mount/PID probe is required")
    if text.count(
        "/usr/bin/unshare --user --map-current-user --map-group=\"$NS_TEST_GID\" --keep-caps --mount --pid --fork"
    ) != 1:
        errors.append("source execution must enter one same-identity user/mount/PID namespace with a trusted capability finalizer")
    if text.count(
        "/usr/bin/bwrap --unshare-user --unshare-pid --disable-userns --assert-userns-disabled"
    ) != 1:
        errors.append("the pre-materialization Bubblewrap probe is required")
    for forbidden_sudo in ("sudo -E", "sudo bash", "sudo sh", "sudo python", "sudo rm"):
        if forbidden_sudo in text:
            errors.append(f"unsafe privileged form: {forbidden_sudo}")
    if any(
        "/usr/bin/sudo" in line and ("GITHUB_WORKSPACE" in line or "SOURCE_COPY" in line)
        for line in text.splitlines()
    ):
        errors.append("root command may not consume a PR source path")
    return errors


class TrustedLighttpdNamespaceDispatchWorkflowTest(unittest.TestCase):
    def test_dispatcher_preserves_the_complete_trust_contract(self) -> None:
        self.assertEqual(trusted_dispatch_errors(WORKFLOW.read_text(encoding="utf-8")), [])

    def test_representative_boundary_mutations_fail_closed(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        mutations = {
            "PR trigger": ("  workflow_dispatch:\n", "  pull_request:\n  workflow_dispatch:\n"),
            "PR target trigger": (
                "  workflow_dispatch:\n",
                "  pull_request_target:\n  workflow_dispatch:\n",
            ),
            "unprotected ref": ("github.ref_protected == true", "github.ref_protected == false"),
            "untrusted dispatcher actor": (
                "github.actor == 'Easton97-Jens'",
                "github.actor == 'attacker'",
            ),
            "untrusted rerun actor": (
                "github.triggering_actor == 'Easton97-Jens'",
                "github.triggering_actor == 'attacker'",
            ),
            "mutable Git ref": ('"$TRUSTED_ORIGIN" "$TARGET_SHA"', '"$TRUSTED_ORIGIN" master'),
            "raw dispatch input as Git ref": (
                '"$TRUSTED_ORIGIN" "$TARGET_SHA"',
                '"$TRUSTED_ORIGIN" "${{ inputs.target }}"',
            ),
            "public API retry disabled": (
                "--retry 3 --retry-delay 1 --retry-max-time 30",
                "--retry 0",
            ),
            "public API retry bound weakened": (
                "--retry 3 --retry-delay 1 --retry-max-time 30",
                "--retry 3 --retry-delay 1 --retry-max-time 300",
            ),
            "public API retries all errors": (
                "--retry 3 --retry-delay 1 --retry-max-time 30",
                "--retry 3 --retry-delay 1 --retry-max-time 30 --retry-all-errors",
            ),
            "untrusted Git origin": (TRUSTED_ORIGIN, "https://example.invalid/untrusted.git"),
            "protocol restriction removed": ("GIT_ALLOW_PROTOCOL=https", "GIT_ALLOW_PROTOCOL=file"),
            "global Git config restored": ("GIT_CONFIG_NOSYSTEM=1", "GIT_CONFIG_NOSYSTEM=0"),
            "Git hooks enabled": ("GIT_CONFIG_VALUE_0=/dev/null", "GIT_CONFIG_VALUE_0=/tmp/hooks"),
            "credential helper enabled": ("GIT_CONFIG_VALUE_1=", "GIT_CONFIG_VALUE_1=store"),
            "unsafe Git template": (
                f"GIT_TEMPLATE_ROOT={GIT_TEMPLATE_ROOT}",
                "GIT_TEMPLATE_ROOT=/tmp/untrusted-git-template",
            ),
            "unbounded Git command": (
                "/usr/bin/timeout --signal=TERM --kill-after=5s 120s /usr/bin/git",
                "/usr/bin/git",
            ),
            "Git tags allowed": ("fetch --no-tags --depth=1", "fetch --tags --depth=1"),
            "Git history deepened": ("--no-tags --depth=1", "--no-tags --depth=50"),
            "submodule recursion allowed": ("--no-recurse-submodules", "--recurse-submodules"),
            "exact object check removed": (
                'run_git -C "$SOURCE_ROOT" cat-file -e "${TARGET_SHA}^{commit}"',
                "true # exact object check removed",
            ),
            "exact head check removed": (
                'capture_git -C "$SOURCE_ROOT" rev-parse HEAD',
                "true # exact head check removed",
            ),
            "Git state retained": ('test ! -e "$SOURCE_ROOT/.git"', 'test -e "$SOURCE_ROOT/.git"'),
            "source symlink guard removed": ('test -z "$source_symlink"', "true # source symlink guard removed"),
            "identity-preserving source namespace removed": (
                "--map-current-user",
                "--map-root-user",
            ),
            "source namespace capability finalizer moved outside the inner namespace": (
                "exec /usr/bin/unshare --mount --pid --fork --kill-child=SIGKILL",
                "exec /usr/bin/unshare --keep-caps --mount --pid --fork --kill-child=SIGKILL",
            ),
            "private source tmpfs removed": (
                "uid=$NS_TEST_UID,gid=$NS_TEST_GID,mode=0700,nosuid,nodev,noexec,size=256m",
                "mode=0700,nosuid,nodev,noexec,size=4m",
            ),
            "private temporary tmpfs removed": (
                "uid=$NS_TEST_UID,gid=$NS_TEST_GID,mode=0700,nosuid,nodev,noexec,size=128m",
                "mode=0700,nosuid,nodev,noexec,size=4m",
            ),
            "post-mount privilege drop removed": (
                "exec /usr/bin/setpriv",
                "exec /usr/bin/dash -eu",
            ),
            "root source materialization introduced": (
                "exec /usr/bin/setpriv",
                "run_git() { :; }\n            exec /usr/bin/setpriv",
            ),
            "namespace lifecycle teardown proof removed": (
                "--kill-child=SIGKILL",
                "--no-kill-child",
            ),
            "source mount leak guard removed": (
                "BLOCKED: runtime.source_namespace_mount_leak",
                "BLOCKED: runtime.source_mount_leak_disabled",
            ),
            "temporary mount leak guard removed": (
                "BLOCKED: runtime.source_namespace_temp_mount_leak",
                "BLOCKED: runtime.source_temp_mount_leak_disabled",
            ),
            "source mount propagation guard removed": (
                '/usr/bin/grep -Eq "(shared:|master:)"',
                '/usr/bin/grep -Eq "source-propagation-disabled"',
            ),
            "path-based source cleanup introduced": (
                "test -z \"$source_entry\" || fail_namespace source_root_not_empty",
                "test -z \"$source_entry\" || fail_namespace source_root_not_empty\n          /usr/bin/find -P \"$SOURCE_ROOT\" -xdev -mindepth 1 -depth -delete",
            ),
            "workspace reintroduced": (
                f"SOURCE_ROOT={SOURCE_ROOT}",
                'SOURCE_ROOT="$GITHUB_WORKSPACE/pr-source"',
            ),
            "global userns relaxation": (
                'test "$userns_restriction" = 1',
                "sysctl -w kernel.apparmor_restrict_unprivileged_userns=0",
            ),
            "privileged container": (
                "cancel-in-progress: false",
                "cancel-in-progress: false\n    container: --privileged",
            ),
            "unsafe namespace fallback": ("--assert-userns-disabled", "--unshare-user-try"),
            "AppArmor profile extension": ("    userns,", "    userns,\n    capability,"),
            "namespace probe removed": (
                "/usr/bin/unshare --user --map-root-user --mount --pid --fork",
                "/usr/bin/true # namespace probe removed",
            ),
            "legacy AppArmor profile count": (
                "/usr/bin/sudo -n /usr/bin/aa-exec -p trusted-lighttpd-ci-userns -- ",
                "/usr/sbin/aa-status --profiled | /usr/bin/grep -F -- 'trusted-lighttpd-ci-userns' >/dev/null",
            ),
            "wrong AppArmor profile proof": (
                "BLOCKED: trusted AppArmor profile was not entered.",
                "BLOCKED: wrong AppArmor profile was entered.",
            ),
            "pre-materialization AppArmor transition removed": (
                "# Prove the complete constrained ns-test boundary before checkout.\n          /usr/bin/sudo -n /usr/bin/aa-exec -p trusted-lighttpd-ci-userns -- \\",
                "# Prove the complete constrained ns-test boundary before checkout.\n          /usr/bin/sudo -n /usr/bin/setpriv \\",
            ),
            "pre-materialization capability guard removed": (
                "CapInh CapPrm CapEff CapBnd CapAmb",
                "CapInh CapPrm CapEff CapAmb",
            ),
            "pre-materialization Bubblewrap probe removed": (
                "fail_preflight bubblewrap_user_pid_namespace",
                "fail_preflight bwrap_disabled",
            ),
            "runtime diagnostic removed": (
                "fail_runtime source_namespace_mount",
                "fail_runtime namespace_probe_disabled",
            ),
            "public runtime parent": (RUNTIME_ROOT, "/var/tmp/trusted-lighttpd-namespace"),
            "lost privilege drop": ("--no-new-privs", "--drop-no-new-privileges"),
            "outer source namespace group clear removed": (
                "exec /usr/bin/setpriv \\\n              --reuid=\"$NS_TEST_UID\" \\\n              --regid=\"$NS_TEST_GID\" \\\n              --clear-groups",
                "exec /usr/bin/setpriv \\\n              --reuid=\"$NS_TEST_UID\" \\\n              --regid=\"$NS_TEST_GID\" \\\n              --keep-groups",
            ),
            "source-runner group attestation removed": (
                'test "$current_groups" = "$NS_TEST_GID" || fail_runtime supplemental_groups',
                "true # source-runner group attestation removed",
            ),
            "root PR-source command": (
                f"SOURCE_ROOT={SOURCE_ROOT}",
                "SOURCE_ROOT=/tmp/unsafe\n          /usr/bin/sudo -n /usr/bin/rm -rf -- \"$SOURCE_ROOT\"",
            ),
            "untrusted artifact": (
                "cancel-in-progress: false",
                "cancel-in-progress: false\n  cache: actions/cache",
            ),
            "local action": (
                "cancel-in-progress: false",
                "cancel-in-progress: false\n      - uses: ./untrusted-action",
            ),
            "masked failure": (
                "cancel-in-progress: false",
                "cancel-in-progress: false\n    continue-on-error: true",
            ),
            "trusted test gains write permission": (
                "    permissions:\n      contents: read\n    runs-on: ubuntu-24.04",
                "    permissions:\n      statuses: write\n    runs-on: ubuntu-24.04",
            ),
            "write token reaches PR-code job": (
                "    outputs:\n      target_sha: ${{ steps.resolve-target.outputs.target_sha }}",
                "    outputs:\n      target_sha: ${{ steps.resolve-target.outputs.target_sha }}\n    env:\n      GITHUB_TOKEN: ${{ github.token }}",
            ),
            "status reporter checks out source": (
                "    steps:\n      - name: Publish the fixed trusted namespace status without checkout",
                "    steps:\n      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7\n      - name: Publish the fixed trusted namespace status without checkout",
            ),
            "status reporter retries side effect": ("--retry 0", "--retry 3"),
            "status reporter loses trusted output dependency": (
                "    needs: trusted-lighttpd-namespace\n",
                "    needs: []\n",
            ),
        }
        for name, (original, replacement) in mutations.items():
            with self.subTest(name=name):
                self.assertIn(original, text)
                mutated = text.replace(original, replacement, 1)
                self.assertNotEqual(trusted_dispatch_errors(mutated), [])

        inner_finalizer_marker = (
            '--map-group="$NS_TEST_GID" --keep-caps --mount --pid --fork '
            '--kill-child=SIGKILL --mount-proc=/proc --propagation private'
        )
        inner_finalizer_index = text.index(inner_finalizer_marker)
        inner_finalizer = text[inner_finalizer_index:]
        finalizer_mutations = {
            "source namespace capability retention removed": ("--keep-caps --mount", "--mount"),
            "source namespace capability finalizer bypassed": ("/usr/bin/setpriv", "/usr/bin/dash"),
            "source namespace finalizer forces denied setgroups": (
                "--keep-groups",
                "--clear-groups",
            ),
            "source namespace finalizer changes the already-cleared group state": (
                "--keep-groups",
                "--groups=0",
            ),
            "source namespace finalizer loses no_new_privs": ("--no-new-privs", "--no-new-privileges"),
            "source namespace finalizer retains inheritable capabilities": ("--inh-caps=-all", "--inh-caps=+all"),
            "source namespace finalizer retains ambient capabilities": ("--ambient-caps=-all", "--ambient-caps=+all"),
            "source namespace finalizer retains bounding capabilities": ("--bounding-set=-all", "--bounding-set=+all"),
        }
        for name, (original, replacement) in finalizer_mutations.items():
            with self.subTest(name=name):
                self.assertIn(original, inner_finalizer)
                mutated = text[:inner_finalizer_index] + inner_finalizer.replace(original, replacement, 1)
                self.assertNotEqual(trusted_dispatch_errors(mutated), [])
