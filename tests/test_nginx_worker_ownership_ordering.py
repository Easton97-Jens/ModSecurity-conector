"""Root materialization must precede NGINX worker ownership handoff."""

from __future__ import annotations

import grp
import os
from pathlib import Path
import pwd
import re
import stat
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "connectors/nginx/harness/run_nginx_smoke.sh"
FRAMEWORK = Path(os.environ.get(
    "MSCONNECTOR_TEST_FRAMEWORK_ROOT", ROOT / "modules/ModSecurity-test-Framework"
)).resolve()
CASE = FRAMEWORK / "tests/cases/no-crs-baseline/deny_header_marker_403.yaml"
CASE_CLI = FRAMEWORK / "tests/runners/case_cli.py"


def shell_function(source: str, name: str) -> str:
    start = source.index(f"{name}() {{\n")
    return source[start:source.index("\n}\n", start) + 3]


class NginxWorkerOwnershipOrderingTests(unittest.TestCase):
    def test_materialization_precedes_every_worker_handoff(self) -> None:
        source = HARNESS.read_text(encoding="utf-8")
        handoffs = [match.start() for match in re.finditer(
            r"(?m)^prepare_nginx_worker_paths$", source
        )]
        materialize = source.index('if ! "$PYTHON_BIN" "$CASE_CLI" materialize')
        successful_materialize = source.index("\nfi\n", materialize) + 4
        self.assertTrue(handoffs)
        self.assertGreater(min(handoffs), successful_materialize)
        self.assertLess(successful_materialize, source.index(
            "\nlock_private_runtime_paths\n", successful_materialize
        ))
        self.assertLess(handoffs[0], source.index("\nproject_nginx_worker_docroot\n"))
        self.assertLess(handoffs[-1], source.index("\npreflight_nginx_worker_docroot\n"))
        preparation = source[source.index('ensure_dir_755 "$NGINX_HARNESS_WORK_ROOT"'):
                             source.index(': > "$STATUS_FILE"')]
        self.assertIn('"$NGINX_SERVER_LOG_ROOT/audit"', preparation)
        worker_function = shell_function(source, "prepare_nginx_worker_paths")
        worker_paths = worker_function.split("    for path in \\\n", 1)[1].split("\n    do", 1)[0]
        self.assertEqual(re.findall(r'"([^"\n]+)"', worker_paths), [
            "$NGINX_WORKER_STATE_ROOT",
            *[f"$NGINX_WORKER_STATE_ROOT/{name}" for name in (
                "client_body_temp", "proxy_temp", "fastcgi_temp", "uwsgi_temp", "scgi_temp"
            )],
            "$NGINX_SERVER_LOG_ROOT", "$NGINX_SERVER_LOG_ROOT/audit",
        ])
        for private in ("RUNTIME_ROOT", "LOG_DIR", "RULES_FILE", "CONFIG_FILE",
                        "NGINX_MEMCHECK_EVIDENCE_DIR"):
            self.assertNotIn(f'"${private}"', worker_function)

    @unittest.skipUnless(os.geteuid() == 0, "requires real root/nobody ownership separation")
    def test_real_materializer_and_worker_access_preserve_private_paths(self) -> None:
        runuser = next((path for path in ("/usr/sbin/runuser", "/usr/bin/runuser")
                        if os.access(path, os.X_OK)), None)
        if runuser is None:
            self.skipTest("fixed runuser executable unavailable")
        try:
            worker = pwd.getpwnam("nobody")
            worker_group = grp.getgrnam("nogroup")
        except KeyError:
            self.skipTest("nobody/nogroup accounts unavailable")
        self.assertNotEqual(worker.pw_uid, os.geteuid())
        self.assertTrue(CASE.is_file(), CASE)
        self.assertTrue(CASE_CLI.is_file(), CASE_CLI)
        self.assertIn("@@AUDIT_LOG_DIR@@", CASE.read_text(encoding="utf-8"))
        source = HARNESS.read_text(encoding="utf-8")
        functions = "\n".join(shell_function(source, name) for name in (
            "ensure_dir_755", "ensure_private_dir", "nginx_worker_group",
            "prepare_nginx_worker_paths", "resolve_nginx_worker_identity",
            "write_permission_diagnostics", "lock_private_runtime_paths",
            "validate_nginx_generated_path_authority",
        ))
        preparation = source[source.index('ensure_dir_755 "$NGINX_HARNESS_WORK_ROOT"'):
                             source.index(': > "$STATUS_FILE"')]
        # Choose a task-owned ancestor the real worker can traverse. Never
        # change caller-owned ancestors or fall back to /tmp or /dev/shm.
        temporary_parent = Path(os.environ.get(
            "NGINX_OWNERSHIP_TEST_TEMP_ROOT", tempfile.gettempdir()
        ))
        if any(not stat.S_IMODE(path.stat().st_mode) & stat.S_IXOTH
               for path in (temporary_parent, *temporary_parent.parents)):
            self.skipTest("provide a worker-traversable external test temp root")
        with tempfile.TemporaryDirectory(prefix="nginx-owner-order-", dir=temporary_parent) as directory:
            base = Path(directory)
            base.chmod(0o711)
            verified = base / "verified"
            verified.mkdir(mode=0o711)
            verified.chmod(0o711)
            build = verified / "build"
            harness = build / "nginx-harness"
            runtime = harness / "runtime/deny_header_marker_403"
            logs = harness / "logs/deny_header_marker_403"
            server = harness / "server-logs/deny_header_marker_403"
            state = harness / "worker-state/deny_header_marker_403"
            environment = {
                "PATH": os.defpath, "CURRENT_UID": "0", "PYTHON_BIN": sys.executable,
                "PYTHONDONTWRITEBYTECODE": "1", "BUILD_ROOT": str(build),
                "VERIFIED_RUN_ROOT": str(verified), "NGINX_HARNESS_PARENT": str(build),
                "NGINX_HARNESS_WORK_ROOT": str(harness), "RUNTIME_BASE": str(harness / "runtime"),
                "RUNTIME_ROOT": str(runtime), "LOG_DIR": str(logs),
                "RESULTS_DIR": str(build / "results"), "RUNTIME_PID_FILE": str(runtime / "nginx.pid"),
                "NGINX_WORKER_STATE_ROOT": str(state), "NGINX_SERVER_LOG_ROOT": str(server),
                "NGINX_MEMCHECK_EVIDENCE_DIR": str(logs / "memcheck"),
                "STATUS_FILE": str(logs / "status.txt"), "PERMISSIONS_LOG": str(logs / "permissions.log"),
                "NGINX_WORKER_PREFLIGHT_FILE": str(logs / "preflight.jsonl"),
                "NGINX_PATH_AUTHORITY_VALIDATOR": str(ROOT / "ci/runtime/common/validate-nginx-harness-paths.py"),
                "NGINX_WORKER_USER": "nobody", "NGINX_WORKER_GROUP": "nogroup",
                "NGINX_DOCROOT_PROJECTION": "1", "PRIVATE_DOCROOT": str(runtime / "htdocs"),
                "NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR": "", "FULL_LIFECYCLE_EVIDENCE_OUTPUT": "",
                "MSCONNECTOR_FULL_LIFECYCLE_SYNC": "0", "NGINX_PATHS_VALIDATED": "0",
            }

            def shell(commands: str) -> subprocess.CompletedProcess[str]:
                return subprocess.run(
                    ["sh", "-eu", "-c", 'umask 077\nblocked() { echo "$*" >&2; exit 77; }\n'
                     + functions + "\n" + commands],
                    env=environment, text=True, capture_output=True, check=False,
                )

            initial = shell("validate_nginx_generated_path_authority\n" + preparation)
            self.assertEqual(initial.returncode, 0, initial.stderr)
            for path in (server, server / "audit", runtime, runtime / "conf", logs):
                metadata = path.stat()
                self.assertEqual((metadata.st_uid, metadata.st_gid,
                                  stat.S_IMODE(metadata.st_mode)), (0, 0, 0o700), str(path))

            def materialize() -> subprocess.CompletedProcess[str]:
                return subprocess.run([
                    sys.executable, str(CASE_CLI), "materialize", "--case", str(CASE),
                    "--rules-file", str(runtime / "conf/rules.conf"),
                    "--env-file", str(runtime / "conf/case.env"),
                    "--headers-file", str(runtime / "conf/headers.txt"),
                    "--body-file", str(runtime / "conf/body.bin"),
                    "--docroot", str(runtime / "htdocs"),
                    "--audit-log-file", str(server / "audit.log"),
                    "--audit-log-dir", str(server / "audit"),
                    "--rules-preamble-file", str(FRAMEWORK / "tests/rules/no-crs-baseline.conf"),
                ], env=environment, text=True, capture_output=True, check=False)

            rendered = materialize()
            self.assertEqual(rendered.returncode, 0, rendered.stderr)
            rules = runtime / "conf/rules.conf"
            self.assertEqual(rules.stat().st_uid, 0)
            self.assertIn(str(server / "audit.log"), rules.read_text(encoding="utf-8"))
            handoff = shell("lock_private_runtime_paths\nprepare_nginx_worker_paths")
            self.assertEqual(handoff.returncode, 0, handoff.stderr)
            for path in (server, server / "audit", state, *(state / name for name in (
                    "client_body_temp", "proxy_temp", "fastcgi_temp", "uwsgi_temp", "scgi_temp"))):
                metadata = path.stat()
                self.assertEqual((metadata.st_uid, metadata.st_gid,
                                  stat.S_IMODE(metadata.st_mode)),
                                 (worker.pw_uid, worker_group.gr_gid, 0o700), str(path))
            for path in (runtime, runtime / "conf", runtime / "htdocs", logs, logs / "memcheck"):
                metadata = path.stat()
                self.assertEqual((metadata.st_uid, stat.S_IMODE(metadata.st_mode)), (0, 0o700))

            def worker_command(*command: str) -> subprocess.CompletedProcess[str]:
                return subprocess.run([runuser, "-u", "nobody", "-g", "nogroup", "--", *command],
                                      env={"PATH": os.defpath}, text=True, capture_output=True, check=False)

            for path in (server / "worker-write.log", server / "audit/worker-write.log"):
                written = worker_command("touch", str(path))
                self.assertEqual(written.returncode, 0, written.stderr)
                self.assertEqual(path.stat().st_uid, worker.pw_uid)
            for path, mode in ((rules, "-r"), (runtime / "conf/case.env", "-r"),
                               (runtime / "conf", "-x"), (runtime, "-x"), (logs, "-x")):
                self.assertNotEqual(worker_command("test", mode, str(path)).returncode, 0, str(path))
            # The real Framework guard must still refuse the old sequence.
            rejected = materialize()
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("audit log directory must be owned by the current user", rejected.stderr)


if __name__ == "__main__":
    unittest.main()
