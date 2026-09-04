"""Compiled regression for SPOP self-test metadata cleanup."""

from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "connectors" / "haproxy" / "src" / "haproxy_spop_diagnostic_runtime.c"


class HAProxySPOPSelfTestCleanupContractTests(unittest.TestCase):
    def test_compiled_cleanup_removes_pass_and_idempotent_error_metadata(self) -> None:
        compiler = shutil.which("cc")
        if compiler is None:
            self.skipTest("requires a C compiler")

        harness_source = r'''
#define main haproxy_spop_diagnostic_runtime_program_main
#include "__SOURCE__"
#undef main

#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>

int main(void) {
    const char *ready = "__READY__";
    const char *pid = "__PID__";
    const char *port = "__PORT__";
    FILE *log = fopen("__LOG__", "w");
    assert(log != NULL);
    assert(close(creat(ready, 0600)) == 0);
    assert(close(creat(pid, 0600)) == 0);
    assert(close(creat(port, 0600)) == 0);
    assert(cleanup_self_test_metadata(ready, pid, port,
        SELF_TEST_METADATA_ALL, log) == 0);
    assert(access(ready, F_OK) != 0);
    assert(access(pid, F_OK) != 0);
    assert(access(port, F_OK) != 0);
    assert(cleanup_self_test_metadata(ready, pid, port,
        SELF_TEST_METADATA_ALL, log) == 0);
    assert(fclose(log) == 0);
    return 0;
}
'''

        with tempfile.TemporaryDirectory(
            prefix="haproxy-spop-selftest-cleanup-",
            dir=os.environ.get("TMPDIR"),
        ) as temporary_directory:
            root = Path(temporary_directory)
            paths = {
                "__SOURCE__": SOURCE.as_posix(),
                "__READY__": (root / "spop-diagnostic-runtime.ready").as_posix(),
                "__PID__": (root / "spop-diagnostic-runtime.pid").as_posix(),
                "__PORT__": (root / "spop-diagnostic-runtime.port").as_posix(),
                "__LOG__": (root / "self-test.log").as_posix(),
            }
            for marker, value in paths.items():
                harness_source = harness_source.replace(marker, value)
            harness = root / "cleanup_contract.c"
            binary = root / "cleanup_contract"
            harness.write_text(harness_source, encoding="utf-8")
            compile_result = subprocess.run(
                [
                    compiler,
                    "-std=c17",
                    "-Wall",
                    "-Wextra",
                    "-Werror",
                    "-ffunction-sections",
                    "-fdata-sections",
                    "-I",
                    str(ROOT / "common" / "include"),
                    "-I",
                    str(ROOT / "connectors" / "haproxy" / "src"),
                    str(harness),
                    "-Wl,--gc-sections",
                    "-o",
                    str(binary),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(compile_result.returncode, 0, compile_result.stderr)
            run_result = subprocess.run(
                [str(binary)], cwd=ROOT, check=False, capture_output=True, text=True
            )
            self.assertEqual(run_result.returncode, 0, run_result.stderr)
            self.assertEqual(
                (root / "self-test.log").read_text(encoding="utf-8").count(
                    "self-test metadata cleanup PASS"
                ),
                2,
            )

    def test_metadata_claim_preserves_existing_paths_and_rejects_collision(self) -> None:
        compiler = shutil.which("cc")
        if compiler is None:
            self.skipTest("requires a C compiler")

        harness_source = r'''
#define main haproxy_spop_diagnostic_runtime_program_main
#include "__SOURCE__"
#undef main

#include <assert.h>
static void write_sentinel(const char *path, const char *text) {
    FILE *file = fopen(path, "w");
    assert(file != NULL);
    assert(fputs(text, file) >= 0);
    assert(fclose(file) == 0);
}

static void assert_contents(const char *path, const char *expected) {
    char buffer[64];
    FILE *file = fopen(path, "r");
    assert(file != NULL);
    assert(fgets(buffer, sizeof(buffer), file) != NULL);
    assert(strcmp(buffer, expected) == 0);
    assert(fclose(file) == 0);
}

int main(void) {
    const char *root = "__ROOT__";
    char ready[4096];
    char pid_path[4096];
    char port[4096];
    pid_t child;
    int status;
    int ready_fd;

    assert(mkdir_p(root) == 0);
    snprintf(ready, sizeof(ready), "%s/spop-diagnostic-runtime.ready", root);
    snprintf(pid_path, sizeof(pid_path), "%s/spop-diagnostic-runtime.pid", root);
    snprintf(port, sizeof(port), "%s/spop-diagnostic-runtime.port", root);

    write_sentinel(pid_path, "caller-owned\n");
    ready_fd = claim_self_test_metadata_file(ready);
    assert(ready_fd >= 0);
    assert(claim_self_test_metadata_file(pid_path) < 0);
    assert(close(ready_fd) == 0);
    assert(cleanup_self_test_metadata(ready, pid_path, port,
        SELF_TEST_METADATA_READY, NULL) == 0);
    assert_contents(pid_path, "caller-owned\n");
    assert(access(ready, F_OK) != 0);
    assert(access(port, F_OK) != 0);
    assert(unlink(pid_path) == 0);

    ready_fd = claim_self_test_metadata_file(ready);
    assert(ready_fd >= 0);
    child = fork();
    assert(child >= 0);
    if (child == 0) {
        exit(claim_self_test_metadata_file(ready) < 0 ? 0 : 1);
    }
    assert(waitpid(child, &status, 0) == child);
    assert(WIFEXITED(status) && WEXITSTATUS(status) == 0);
    assert(close(ready_fd) == 0);
    assert(cleanup_self_test_metadata(ready, pid_path, port,
        SELF_TEST_METADATA_READY, NULL) == 0);
    assert(access(ready, F_OK) != 0);
    assert(access(pid_path, F_OK) != 0);
    assert(access(port, F_OK) != 0);
    return 0;
}
'''

        with tempfile.TemporaryDirectory(
            prefix="haproxy-spop-selftest-ownership-",
            dir=os.environ.get("TMPDIR"),
        ) as temporary_directory:
            root = Path(temporary_directory)
            paths = {
                "__SOURCE__": SOURCE.as_posix(),
                "__ROOT__": (root / "shared-tmp").as_posix(),
            }
            for marker, value in paths.items():
                harness_source = harness_source.replace(marker, value)
            harness = root / "selftest_ownership_contract.c"
            binary = root / "selftest_ownership_contract"
            harness.write_text(harness_source, encoding="utf-8")
            compile_result = subprocess.run(
                [
                    compiler,
                    "-std=c17",
                    "-Wall",
                    "-Wextra",
                    "-Werror",
                    "-ffunction-sections",
                    "-fdata-sections",
                    "-I",
                    str(ROOT / "common" / "include"),
                    "-I",
                    str(ROOT / "connectors" / "haproxy" / "src"),
                    str(harness),
                    "-Wl,--gc-sections",
                    "-o",
                    str(binary),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(compile_result.returncode, 0, compile_result.stderr)
            run_result = subprocess.run(
                [str(binary)], cwd=ROOT, check=False, capture_output=True, text=True
            )
            self.assertEqual(run_result.returncode, 0, run_result.stderr)

    def test_run_self_test_has_cleanup_after_child_waits_on_success_and_errors(self) -> None:
        source = SOURCE.read_text(encoding="utf-8")
        run_self_test = source.split("static int run_self_test", 1)[1].split(
            "typedef struct legacy_server_config", 1
        )[0]
        self.assertGreaterEqual(
            run_self_test.count("cleanup_self_test_metadata(ready_path, pid_path, port_path,"),
            6,
        )
        self.assertIn("waitpid(child, &status, 0);\n        (void)cleanup_self_test_metadata", run_self_test)
        self.assertIn("waitpid(child, &status, 0);\n    if (!WIFEXITED", run_self_test)
        self.assertIn("ready_fd = claim_self_test_metadata_file(ready_path);", run_self_test)
        self.assertIn("pid_fd = claim_self_test_metadata_file(pid_path);", run_self_test)
        self.assertIn("port_fd = claim_self_test_metadata_file(port_path);", run_self_test)
        self.assertIn("owned_metadata |= SELF_TEST_METADATA_READY;", run_self_test)
        self.assertIn("owned_metadata |= SELF_TEST_METADATA_PID;", run_self_test)
        self.assertIn("owned_metadata |= SELF_TEST_METADATA_PORT;", run_self_test)


if __name__ == "__main__":
    unittest.main()
