"""Static trust contracts for the protected Lighttpd namespace dispatcher."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/run-trusted-lighttpd-namespace-dispatch.yml"
CHECKOUT_PIN = "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7"
EXPECTED_REPOSITORY = "Easton97-Jens/ModSecurity-conector"


def trusted_dispatch_errors(text: str) -> list[str]:
    """Return violations of the pre-checkout privileged trust boundary."""

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
        for required in (
            "Open canonical PR number or its full lowercase 40-character head SHA.",
            "        required: true",
            "        type: string",
        ):
            if required not in trigger_body:
                errors.append("workflow target input contract")
                break

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

    for required in (
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
    ):
        if required not in text:
            errors.append(f"missing protected-master boundary: {required}")

    for required in (
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
        "test \"$(/usr/bin/id -G ns-test)\" = \"$ns_test_gid\"",
        "/var/lib/trusted-lighttpd-namespace/tmp",
        "-m 0700",
        "--disable-userns",
        "--assert-userns-disabled",
    ):
        if required not in text:
            errors.append(f"missing trusted bootstrap control: {required}")
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
    checkout_marker = "      - name: Check out the validated exact commit without hooks"
    verify_marker = "      - name: Verify exact checkout and remove Git state before PR code"
    test_marker = "      - name: Run the namespace test only as constrained ns-test"
    report_marker = "  report-trusted-lighttpd-namespace:"
    for marker in (bootstrap_marker, checkout_marker, verify_marker, test_marker, report_marker):
        if marker not in text:
            errors.append(f"missing ordered workflow step: {marker}")
    if not errors and not (
        text.index(bootstrap_marker)
        < text.index(checkout_marker)
        < text.index(verify_marker)
        < text.index(test_marker)
    ):
        errors.append("checkout ordering")
    if bootstrap_marker in text and checkout_marker in text:
        bootstrap_step = text[text.index(bootstrap_marker) : text.index(checkout_marker)]
        for required in (
            "/usr/bin/sudo -n /usr/bin/aa-exec -p trusted-lighttpd-ci-userns -- ",
            'case "$(/usr/bin/cat /proc/self/attr/current)" in',
            "trusted-lighttpd-ci-userns\\ *)",
            "BLOCKED: trusted AppArmor profile was not entered.",
        ):
            if required not in bootstrap_step:
                errors.append(f"missing pre-checkout named AppArmor profile proof: {required}")

    for required in (
        "https://api.github.com/repos/$expected_repository",
        'if [[ "$target" =~ ^[0-9a-f]{40}$ ]]; then',
        'elif [[ "$target" =~ ^[1-9][0-9]*$ ]]; then',
        '"$api_root/commits/$target"',
        '"$api_root/commits/$target/pulls"',
        "commit_sha=\"$(printf '%s' \"$commit_response\" | /usr/bin/jq -er '.sha')\"",
        'test "$commit_sha" = "$target"',
        '"$api_root/pulls/$target"',
        'select(.state == "open")',
        'select(.base.ref == "master")',
        'select(.base.repo.full_name == $expected_repository)',
        'select(.head.repo.full_name == $expected_repository)',
        'select(.head.sha == $expected_sha)',
        "commit SHA does not bind exactly one open canonical master PR",
        "ref: ${{ steps.resolve-target.outputs.target_sha }}",
        CHECKOUT_PIN,
        "persist-credentials: false",
        "submodules: false",
        "lfs: false",
        "fetch-depth: 1",
        "GIT_CONFIG_KEY_0: core.hooksPath",
        "GIT_CONFIG_VALUE_0: /dev/null",
        "config --local --get-regexp '^http\\..*\\.extraheader$'",
        "config --local --get-all credential.helper",
        '/usr/bin/rm -rf --one-file-system -- "$source_root/.git"',
        'test ! -e "$source_root/.git"',
    ):
        if required not in text:
            errors.append(f"missing exact-ref checkout control: {required}")
    if "ref: ${{ inputs.target }}" in text:
        errors.append("unvalidated target used as checkout ref")

    trusted_job_match = re.search(
        r"(?ms)^  trusted-lighttpd-namespace:\n(?P<body>.*?)(?=^  report-trusted-lighttpd-namespace:)",
        text,
    )
    if trusted_job_match is None:
        errors.append("trusted test job boundary")
        trusted_job = ""
    else:
        trusted_job = trusted_job_match.group("body")
    if "outputs:\n      target_sha: ${{ steps.resolve-target.outputs.target_sha }}" not in trusted_job:
        errors.append("trusted job must expose only the resolved target SHA")
    if "GITHUB_TOKEN" in trusted_job or "github.token" in trusted_job:
        errors.append("trusted PR-code job must not receive a write token")
    if re.search(r"(?m)^      [A-Za-z-]+:\s*write\s*$", trusted_job):
        errors.append("trusted PR-code job must not receive write permissions")

    report_job_match = re.search(
        r"(?ms)^  report-trusted-lighttpd-namespace:\n(?P<body>.*)\Z",
        text,
    )
    if report_job_match is None:
        errors.append("status reporting job boundary")
        report_job = ""
    else:
        report_job = report_job_match.group("body")
    for required in (
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
    ):
        if required not in report_job:
            errors.append(f"missing isolated status-reporting control: {required}")
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

    for required in (
        "/usr/bin/aa-exec -p trusted-lighttpd-ci-userns -- ",
        "/usr/bin/setpriv",
        "--reuid=\"$ns_test_uid\"",
        "--regid=\"$ns_test_gid\"",
        "--clear-groups",
        "--no-new-privs",
        "--inh-caps=-all",
        "--ambient-caps=-all",
        "--bounding-set=-all",
        "/usr/bin/env -i",
        "LIGHTTPD_REQUIRE_NAMESPACE_INTEGRATION=1",
        "LIGHTTPD_REQUIRE_UNPRIVILEGED_TEST_RUNNER=1",
        "LIGHTTPD_NAMESPACE_TEST_TEMP_PARENT=/var/lib/trusted-lighttpd-namespace/tmp",
        "/usr/bin/unshare --user --map-root-user --mount --pid --fork",
        "--propagation private",
        "/usr/bin/mount --make-rprivate /",
        "/usr/bin/bwrap --unshare-user --unshare-pid --disable-userns --assert-userns-disabled",
        "/usr/bin/python3 -m unittest -v connectors.lighttpd.tests.test_no_crs_fixture_namespace",
    ):
        if required not in text:
            errors.append(f"missing restricted PR-code control: {required}")

    if text.count("/usr/bin/sudo -n") != 11:
        errors.append("unexpected privileged command inventory")
    if len(re.findall(r"(?<![A-Za-z0-9-])--no-new-privs(?![A-Za-z0-9-])", text)) != 2:
        errors.append("both ns-test privilege drops must set no_new_privs")
    if text.count("--clear-groups") != 2:
        errors.append("both ns-test privilege drops must clear supplemental groups")
    for forbidden_sudo in ("sudo -E", "sudo bash", "sudo sh", "sudo python", "sudo rm"):
        if forbidden_sudo in text:
            errors.append(f"unsafe privileged form: {forbidden_sudo}")
    if "cd \"$SOURCE_COPY\"" not in text or "-- /usr/bin/env -i" not in text:
        errors.append("PR source execution boundary")
    else:
        test_step = text.split(test_marker, 1)[1]
        ordered_markers = (
            "/usr/bin/aa-exec -p trusted-lighttpd-ci-userns -- ",
            "-- /usr/bin/env -i",
            "/usr/bin/unshare --user --map-root-user --mount --pid --fork",
            'cd "$SOURCE_COPY"',
            "/usr/bin/python3 -m unittest -v connectors.lighttpd.tests.test_no_crs_fixture_namespace",
        )
        if any(marker not in test_step for marker in ordered_markers):
            errors.append("complete PR source execution order")
        elif sorted(test_step.index(marker) for marker in ordered_markers) != [
            test_step.index(marker) for marker in ordered_markers
        ]:
            errors.append("PR source starts before constrained namespace probes")
    if any(
        "/usr/bin/sudo" in line and ("SOURCE_ROOT" in line or "source_root" in line)
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
            "PR target trigger": ("  workflow_dispatch:\n", "  pull_request_target:\n  workflow_dispatch:\n"),
            "unprotected ref": ("github.ref_protected == true", "github.ref_protected == false"),
            "untrusted dispatcher actor": (
                "github.actor == 'Easton97-Jens'",
                "github.actor == 'attacker'",
            ),
            "untrusted rerun actor": (
                "github.triggering_actor == 'Easton97-Jens'",
                "github.triggering_actor == 'attacker'",
            ),
            "mutable checkout": (
                "ref: ${{ steps.resolve-target.outputs.target_sha }}",
                "ref: master",
            ),
            "checkout raw input": (
                "ref: ${{ steps.resolve-target.outputs.target_sha }}",
                "ref: ${{ inputs.target }}",
            ),
            "credential persistence": ("persist-credentials: false", "persist-credentials: true"),
            "credential removal": ('test ! -e "$source_root/.git"', "test -e \"$source_root/.git\""),
            "global userns relaxation": ("test \"$userns_restriction\" = 1", "sysctl -w kernel.apparmor_restrict_unprivileged_userns=0"),
            "privileged container": ("cancel-in-progress: false", "cancel-in-progress: false\n    container: --privileged"),
            "unsafe namespace fallback": ("--assert-userns-disabled", "--unshare-user-try"),
            "AppArmor profile extension": (
                "    userns,",
                "    userns,\n    capability,",
            ),
            "namespace probe removed": (
                "/usr/bin/unshare --user --map-root-user --mount --pid --fork",
                "/usr/bin/true # namespace probe removed",
            ),
            "legacy AppArmor profile count": (
                "/usr/bin/sudo -n /usr/bin/aa-exec -p trusted-lighttpd-ci-userns -- ",
                "/usr/sbin/aa-status --profiled | /usr/bin/grep -F -- 'trusted-lighttpd-ci-userns' >/dev/null",
            ),
            "wrong AppArmor profile proof": (
                "trusted-lighttpd-ci-userns\\ *)",
                "untrusted-profile\\ *)",
            ),
            "public runtime parent": (
                "/var/lib/trusted-lighttpd-namespace",
                "/var/tmp/trusted-lighttpd-namespace",
            ),
            "lost privilege drop": ("--no-new-privs", "--drop-no-new-privileges"),
            "root PR-source command": (
                "          source_root=\"$GITHUB_WORKSPACE/pr-source\"\n          test -d \"$source_root\"",
                "          /usr/bin/sudo -n /usr/bin/cp -- \"$SOURCE_ROOT\" /tmp/unsafe\n          source_root=\"$GITHUB_WORKSPACE/pr-source\"\n          test -d \"$source_root\"",
            ),
            "untrusted artifact": ("cancel-in-progress: false", "cancel-in-progress: false\n  cache: actions/cache"),
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
