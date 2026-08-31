"""Static security contracts for the HAProxy evidence upload workflow path."""

from __future__ import annotations

import hashlib
from pathlib import Path
import re
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "test-connectors-with-crs-no-mrts.yml"
UPLOAD_PIN = "actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a # v7.0.1"


class HaproxyEvidenceWorkflowContractTests(unittest.TestCase):
    @staticmethod
    def source() -> str:
        return WORKFLOW.read_text(encoding="utf-8")

    @staticmethod
    def block(source: str, start: str, end: str) -> str:
        return source.split(start, 1)[1].split(end, 1)[0]

    def test_boundary_uses_a_mandatory_namespace_and_never_roots_checkout_python(self) -> None:
        source = self.source()
        boundary = self.block(
            source,
            "      - name: Prepare HAProxy runtime evidence boundary\n",
            "      - name: Run selected real with-CRS no-MRTS runtime\n",
        )
        self.assertIn("id: prepare-haproxy-runtime-evidence", boundary)
        self.assertIn("if: matrix.connector == 'haproxy'", boundary)
        self.assertIn(
            'rev-parse "$PARENT_SHA:ci/runtime/lifecycle/project-haproxy-runtime-evidence.py"',
            boundary,
        )
        self.assertIn('cat-file -e "${projector_blob}^{blob}"', boundary)
        self.assertIn("runner_temp_identity=", boundary)
        self.assertIn("/usr/bin/head", boundary)
        self.assertIn("/usr/bin/sudo", boundary)
        self.assertIn("sudo -n /usr/bin/env -i", boundary)
        self.assertIn("probe_uid=$(", boundary)
        for namespace_flag in (
            "--mount",
            "--pid",
            "--fork",
            "--kill-child=SIGKILL",
            "--mount-proc=/proc",
            "--propagation private",
        ):
            self.assertIn(namespace_flag, boundary)
        for privilege_drop in (
            "/usr/bin/setpriv",
            '--reuid="$runtime_uid"',
            '--regid="$runtime_gid"',
            "--clear-groups",
            "--no-new-privs",
            "--inh-caps=-all",
            "--ambient-caps=-all",
            "--bounding-set=-all",
        ):
            self.assertIn(privilege_drop, boundary)
        self.assertIn('test "$probe_uid" = "$runtime_uid"', boundary)
        self.assertNotIn("seal-helper", boundary)
        self.assertNotIn("SEALED_HELPER", boundary)
        self.assertNotIn("sudo -n /usr/bin/python3", boundary)
        self.assertNotIn("sudo -n sh", boundary)
        self.assertNotIn("find ", boundary)
        self.assertNotIn("cp -", boundary)

    def test_haproxy_privileged_operations_do_not_resolve_sudo_from_path(self) -> None:
        source = self.source()
        self.assertIn("/usr/bin/sudo -n", source)
        self.assertIsNone(re.search(r"(?<!/usr/bin/)sudo -n", source))

    def test_runtime_executes_checkout_only_after_privilege_drop_and_receipts_fail_closed(self) -> None:
        source = self.source()
        runtime = self.block(
            source,
            "      - name: Run selected real with-CRS no-MRTS runtime\n",
            "      - name: Project HAProxy runtime evidence\n",
        )
        runtime_script = runtime.split("        run: |\n", 1)[1]
        self.assertIn(
            "SETUP_PYTHON_PATH: $" + "{{ steps.setup-python.outputs.python-path }}",
            runtime,
        )
        self.assertIn('PYTHON="$SETUP_PYTHON_PATH"', runtime_script)
        for runtime_value in (
            "RUNTIME_UID",
            "RUNTIME_GID",
            "RUNTIME_PARENT_SHA",
            "RUNTIME_FRAMEWORK_SHA",
            "RUNTIME_MRTS_SHA",
        ):
            self.assertIn(f"{runtime_value}: $" + "{{ steps.prepare-haproxy-runtime-evidence.outputs.", runtime)
            self.assertIn(f'"${runtime_value}"', runtime_script)
        self.assertNotIn(
            "$" + "{{ steps.prepare-haproxy-runtime-evidence.outputs.",
            runtime_script,
        )
        self.assertIn("HAPROXY_EVIDENCE_RECEIPT=1", runtime)
        self.assertIn(
            'HAPROXY_EVIDENCE_RECEIPT_PROJECTOR="$GITHUB_WORKSPACE/ci/runtime/lifecycle/project-haproxy-runtime-evidence.py"',
            runtime,
        )
        self.assertIn("EXPECTED_PARENT_SHA=", runtime)
        self.assertIn("EXPECTED_FRAMEWORK_SHA=", runtime)
        self.assertIn("EXPECTED_MRTS_SHA=", runtime)
        self.assertIn("/usr/bin/unshare", runtime)
        self.assertIn("/usr/bin/setpriv", runtime)
        self.assertIn("--no-new-privs", runtime)
        self.assertIn("/usr/bin/make -C \"$GITHUB_WORKSPACE\" verified-haproxy-case", runtime)
        root_launch, dropped_runtime = runtime.split("-- /usr/bin/env -i", 1)
        self.assertNotIn("$GITHUB_WORKSPACE", root_launch)
        self.assertNotIn("GITHUB_ENV", dropped_runtime)
        self.assertNotIn("GITHUB_OUTPUT", dropped_runtime)
        self.assertNotIn("GITHUB_PATH", dropped_runtime)
        self.assertNotIn("GITHUB_STATE", dropped_runtime)
        self.assertLess(runtime.index("/usr/bin/setpriv"), runtime.index("/usr/bin/make"))
        self.assertNotIn("HAPROXY_EVIDENCE_RECEIPT_HELPER", runtime)
        self.assertNotIn("seal-helper", runtime)
        self.assertNotIn("sudo -n /usr/bin/python3", runtime)
        self.assertNotIn("|| true", runtime)
        self.assertNotIn("continue-on-error:", runtime)

    def test_runtime_prepares_a_validated_private_tmp_root_before_privilege_drop(
        self,
    ) -> None:
        source = self.source()
        runtime = self.block(
            source,
            "      - name: Run selected real with-CRS no-MRTS runtime\n",
            "      - name: Project HAProxy runtime evidence\n",
        )
        self.assertIn(
            'expected_verified_root="$expected_cell_root/verified"',
            runtime,
        )
        self.assertIn('expected_tmp_root="$expected_verified_root/tmp"', runtime)
        self.assertIn('test "$VERIFIED_RUN_ROOT" = "$expected_verified_root"', runtime)
        self.assertIn('test "$TMP_ROOT" = "$expected_tmp_root"', runtime)
        self.assertIn('test ! -L "$runtime_path"', runtime)
        self.assertIn('test ! -e "$expected_tmp_root"', runtime)
        self.assertIn('test ! -L "$expected_tmp_root"', runtime)
        self.assertIn('/usr/bin/install -d -m 0700 -- "$expected_tmp_root"', runtime)
        self.assertIn(
            '/usr/bin/chmod 0700 -- "$expected_verified_root" "$expected_tmp_root"',
            runtime,
        )
        self.assertIn(
            'test "$(/usr/bin/stat -Lc \'%u:%g:%a\' -- "$expected_tmp_root")" = "$RUNTIME_UID:$RUNTIME_GID:700"',
            runtime,
        )
        self.assertLess(
            runtime.index("expected_verified_root="),
            runtime.index("sudo -n /usr/bin/env -i"),
        )
        self.assertLess(
            runtime.index(
                '/usr/bin/chmod 0700 -- "$expected_verified_root" "$expected_tmp_root"',
            ),
            runtime.index("sudo -n /usr/bin/env -i"),
        )
        self.assertNotIn("|| true", runtime)
        self.assertNotIn("continue-on-error:", runtime)

    def test_runtime_rederives_all_build_roots_after_checkout_controlled_steps(
        self,
    ) -> None:
        source = self.source()
        boundary = self.block(
            source,
            "      - name: Prepare HAProxy runtime evidence boundary\n",
            "      - name: Run selected real with-CRS no-MRTS runtime\n",
        )
        runtime = self.block(
            source,
            "      - name: Run selected real with-CRS no-MRTS runtime\n",
            "      - name: Project HAProxy runtime evidence\n",
        )
        self.assertIn("TRUSTED_RUNNER_TEMP: $" + "{{ runner.temp }}", boundary)
        self.assertIn(
            "TRUSTED_CRS_RUNTIME_RUN_ID: crs-$"
            + "{{ github.run_id }}-$"
            + "{{ github.run_attempt }}-$"
            + "{{ matrix.connector }}",
            boundary,
        )
        self.assertIn(
            'test "$CRS_RUNTIME_RUN_ID" = "$TRUSTED_CRS_RUNTIME_RUN_ID"',
            boundary,
        )
        self.assertIn("cell_root_identity=", boundary)
        self.assertIn('"cell_root_identity=$cell_root_identity"', boundary)
        self.assertIn('RUNTIME_CELL_ROOT_IDENTITY: $' + "{{", runtime)
        self.assertIn('TRUSTED_CRS_RUNTIME_RUN_ID: $' + "{{", runtime)
        self.assertIn('expected_build_root="$expected_verified_root/build"', runtime)
        self.assertIn('expected_log_root="$expected_verified_root/logs"', runtime)
        self.assertIn('expected_cache_root="$expected_verified_root/cache-v2"', runtime)
        self.assertIn(
            'expected_component_cache="$expected_cache_root/shared"',
            runtime,
        )
        self.assertIn(
            'expected_crs_source_root="$expected_verified_root/crs-fresh-source"',
            runtime,
        )
        self.assertIn(
            'expected_crs_source_dir="$expected_crs_source_root/coreruleset"',
            runtime,
        )
        for environment_check in (
            'test "$RUNNER_TEMP" = "$TRUSTED_RUNNER_TEMP"',
            'test "$CRS_RUNTIME_RUN_ID" = "$TRUSTED_CRS_RUNTIME_RUN_ID"',
            'test "$BUILD_ROOT" = "$expected_build_root"',
            'test "$SOURCE_ROOT" = "$expected_crs_source_root"',
            'test "$CRS_SOURCE_DIR" = "$expected_crs_source_dir"',
            'test "$LOG_ROOT" = "$expected_log_root"',
            'test "$CACHE_ROOT" = "$expected_cache_root"',
            'test "$CONNECTOR_COMPONENT_CACHE" = "$expected_component_cache"',
            'test "$PYTHONPYCACHEPREFIX" = "$expected_pycache_root"',
        ):
            self.assertIn(environment_check, runtime)
        self.assertIn('/usr/bin/realpath -e -- "$runtime_path"', runtime)
        self.assertIn('"$expected_cell_root"', runtime)
        self.assertIn(
            'test "$(/usr/bin/stat -Lc \'%d:%i:%u:%g:%a\' -- "$expected_cell_root")" = "$RUNTIME_CELL_ROOT_IDENTITY"',
            runtime,
        )
        dropped_runtime = runtime.split("-- /usr/bin/env -i", 1)[1]
        for canonical_assignment in (
            'RUNNER_TEMP="$TRUSTED_RUNNER_TEMP"',
            'CRS_RUNTIME_RUN_ID="$TRUSTED_CRS_RUNTIME_RUN_ID"',
            'VERIFIED_RUN_ROOT="$expected_verified_root"',
            'BUILD_ROOT="$expected_build_root"',
            'SOURCE_ROOT="$expected_crs_source_root"',
            'CRS_SOURCE_DIR="$expected_crs_source_dir"',
            'TMP_ROOT="$expected_tmp_root"',
            'LOG_ROOT="$expected_log_root"',
            'CACHE_ROOT="$expected_cache_root"',
            'CONNECTOR_COMPONENT_CACHE="$expected_component_cache"',
            'FRAMEWORK_ROOT="$GITHUB_WORKSPACE/modules/ModSecurity-test-Framework"',
        ):
            self.assertIn(canonical_assignment, dropped_runtime)
        self.assertNotIn('BUILD_ROOT="$BUILD_ROOT"', dropped_runtime)
        self.assertNotIn('SOURCE_ROOT="$SOURCE_ROOT"', dropped_runtime)
        self.assertNotIn('CRS_SOURCE_DIR="$CRS_SOURCE_DIR"', dropped_runtime)

    def test_projection_and_verification_are_unprivileged_and_descriptor_bound(self) -> None:
        source = self.source()
        project = self.block(
            source,
            "      - name: Project HAProxy runtime evidence\n",
            "      - name: Verify HAProxy runtime evidence\n",
        )
        verify = self.block(
            source,
            "      - name: Verify HAProxy runtime evidence\n",
            "      - name: Upload non-HAProxy runtime evidence\n",
        )
        self.assertIn("if: matrix.connector == 'haproxy' && steps.runtime.outcome == 'success'", project)
        self.assertIn("TRUSTED_SOURCE_ROOT", project)
        self.assertIn("TRUSTED_RUNNER_TEMP", project)
        self.assertIn("RUNTIME_GID", project)
        self.assertIn("PROJECTOR_BLOB", project)
        self.assertIn("run_runner_projector()", project)
        self.assertIn("run_evidence_projector()", project)
        self.assertIn('"/usr/bin/git", "--no-pager", "-C", workspace, "cat-file", "blob", blob', project)
        self.assertIn("hashlib.sha1", project)
        self.assertIn("exec(compile(source", project)
        self.assertIn(
            'stage_parent=$(/usr/bin/sudo -n /usr/bin/mktemp -d -- "$TRUSTED_RUNNER_TEMP/haproxy-runtime-evidence-parent.XXXXXXXX")',
            project,
        )
        self.assertIn('stage_root="$stage_parent/package"', project)
        self.assertIn("/usr/bin/sudo -n /usr/bin/mkdir -m 0700", project)
        self.assertIn(
            '/usr/bin/sudo -n /usr/bin/chown --no-dereference "$EVIDENCE_UID:$RUNTIME_GID" -- "$stage_root"',
            project,
        )
        self.assertNotIn(
            '/usr/bin/sudo -n /usr/bin/chown --no-dereference "$EVIDENCE_UID:$EVIDENCE_GID" -- "$stage_root"',
            project,
        )
        self.assertIn("/usr/bin/sudo -n /usr/bin/chmod 0755", project)
        self.assertIn('= "$EVIDENCE_UID:$RUNTIME_GID:700"', project)
        self.assertIn("run_runner_projector export-source-receipt", project)
        self.assertIn("| /usr/bin/head --bytes=16385", project)
        self.assertIn("| run_evidence_projector project-document --source-document-stdin", project)
        self.assertNotIn("source_document=", project)
        self.assertNotIn("--source-document ", project)
        self.assertLess(project.index("run_runner_projector export-source-receipt"), project.index("| /usr/bin/head --bytes=16385"))
        self.assertLess(project.index("| /usr/bin/head --bytes=16385"), project.index("| run_evidence_projector project-document --source-document-stdin"))
        self.assertLess(project.index("stage_parent="), project.index("project-document"))
        self.assertIn('--upload-gid "$RUNTIME_GID"', project)
        self.assertIn(
            "if: matrix.connector == 'haproxy' && steps.project-haproxy-runtime-evidence.outcome == 'success'",
            verify,
        )
        self.assertIn("RUNTIME_GID", verify)
        self.assertIn("EVIDENCE_UID", verify)
        self.assertIn("EVIDENCE_GID", verify)
        self.assertIn("hashlib.sha1", verify)
        self.assertIn("exec(compile(source", verify)
        self.assertIn("run_evidence_projector verify", verify)
        self.assertIn('--upload-gid "$RUNTIME_GID"', verify)
        for block in (project, verify):
            self.assertIn("sudo -n /usr/bin/env -i", block)
            self.assertIn("/usr/bin/unshare", block)
            self.assertIn("/usr/bin/setpriv", block)
            self.assertIn("--no-new-privs", block)
            self.assertIn("--inh-caps=-all", block)
            self.assertIn("--ambient-caps=-all", block)
            self.assertIn("--bounding-set=-all", block)
            self.assertIn('--reuid="$EVIDENCE_UID"', block)
            self.assertIn('--regid="$EVIDENCE_GID"', block)
            self.assertNotIn("sudo -n -u nobody -g nogroup", block)
            self.assertNotIn("seal-helper", block)
            self.assertNotIn("SEALED_HELPER", block)
            self.assertNotIn("sudo -n /usr/bin/python3", block)
            self.assertNotIn("find ", block)
            self.assertNotIn("cp -", block)
            self.assertNotIn("|| true", block)
            self.assertNotIn("continue-on-error:", block)
        self.assertIn('--reuid="$RUNTIME_UID"', project)
        self.assertIn('--regid="$RUNTIME_GID"', project)
        root_launcher, constrained_projector = project.split("-- /usr/bin/env -i", 1)
        self.assertNotIn("$GITHUB_WORKSPACE", root_launcher)
        self.assertNotIn("source_document", root_launcher)
        self.assertLess(
            constrained_projector.index("/usr/bin/python3 -I -c"),
            constrained_projector.index("exec(compile(source"),
        )

    def test_verifier_persists_only_a_bounded_canonical_digest_report(self) -> None:
        source = self.source()
        verify = self.block(
            source,
            "      - name: Verify HAProxy runtime evidence\n",
            "      - name: Upload non-HAProxy runtime evidence\n",
        )
        self.assertIn(
            'digest_report="$STAGE_PARENT/haproxy-runtime-evidence-digests.json"',
            verify,
        )
        self.assertIn(
            '/usr/bin/sudo -n /usr/bin/install -m 0640 -o 0 -g "$RUNTIME_GID" /dev/null "$digest_report"',
            verify,
        )
        self.assertIn("/usr/bin/head --bytes=1025", verify)
        self.assertIn('/usr/bin/sudo -n /usr/bin/tee -- "$digest_report" >/dev/null', verify)
        self.assertIn("os.O_NOFOLLOW", verify)
        self.assertIn("before.st_uid != 0", verify)
        self.assertIn("stat.S_IMODE(before.st_mode) != 0o640", verify)
        self.assertIn("object_pairs_hook=reject_duplicate_keys", verify)
        self.assertIn('"haproxy_runtime_evidence_digests"', verify)
        self.assertIn('type(document["schema_version"]) is not int', verify)
        self.assertIn('output.write("evidence_sha256="', verify)
        self.assertIn('output.write("manifest_sha256="', verify)
        self.assertIn('/usr/bin/sudo -n /usr/bin/rm -f -- "$digest_report"', verify)
        self.assertLess(
            verify.index("run_evidence_projector verify"),
            verify.index('output.write("evidence_sha256="'),
        )
        self.assertLess(
            verify.index('output.write("manifest_sha256="'),
            verify.index('/usr/bin/sudo -n /usr/bin/rm -f -- "$digest_report"'),
        )
        for forbidden in ("|| true", "continue-on-error:", "stage_root=$digest_report"):
            self.assertNotIn(forbidden, verify)

    def test_projector_seals_the_upload_reader_path_without_other_traversal(self) -> None:
        projector = (
            ROOT / "ci" / "runtime" / "lifecycle" / "project-haproxy-runtime-evidence.py"
        ).read_text(encoding="utf-8")
        self.assertIn("os.fchmod(descriptor, 0o550)", projector)
        self.assertNotIn("os.fchmod(descriptor, 0o555)", projector)

    def test_immutable_git_blob_verifiers_use_the_git_nul_delimiter(self) -> None:
        source = self.source()
        verifier = (
            'hashlib.sha1(b"blob " + str(len(source)).encode("ascii") + '
            'b"\\0" + source).hexdigest() != blob'
        )
        malformed_verifier = (
            'hashlib.sha1(b"blob " + str(len(source)).encode("ascii") + '
            'b"\\\\0" + source).hexdigest() != blob'
        )
        self.assertEqual(source.count(verifier), 4)
        self.assertNotIn(malformed_verifier, source)

        path = "ci/runtime/lifecycle/summarize-with-crs-no-mrts-workflow.py"
        blob = subprocess.check_output(
            ["git", "rev-parse", f"HEAD:{path}"], cwd=ROOT, text=True
        ).strip()
        blob_source = subprocess.check_output(["git", "cat-file", "blob", blob], cwd=ROOT)
        git_digest = hashlib.sha1(
            b"blob " + str(len(blob_source)).encode("ascii") + b"\0" + blob_source
        ).hexdigest()
        self.assertEqual(git_digest, blob)

    def test_upload_is_exactly_the_verified_two_file_package(self) -> None:
        source = self.source()
        upload = self.block(
            source,
            "      - name: Upload real runtime evidence\n",
            "      - name: Write connector runtime overview\n",
        )
        self.assertIn(
            "if: matrix.connector == 'haproxy' && steps.verify-haproxy-runtime-evidence.outcome == 'success'",
            upload,
        )
        self.assertIn(UPLOAD_PIN, upload)
        self.assertIn(
            "steps.project-haproxy-runtime-evidence.outputs.stage_root }}/haproxy-runtime-evidence.json",
            upload,
        )
        self.assertIn(
            "steps.project-haproxy-runtime-evidence.outputs.stage_root }}/manifest.json",
            upload,
        )
        self.assertIn("if-no-files-found: error", upload)
        for forbidden in (
            "continue-on-error:",
            "|| true",
            "BUILD_ROOT",
            "VERIFIED_RUN_ROOT",
            "EVIDENCE_ROOT",
            "logs",
            "result.json",
            "source_root",
            "haproxy-runtime-evidence-digests.json",
        ):
            self.assertNotIn(forbidden, upload)

    def test_non_haproxy_upload_and_overview_keep_actual_outcomes_and_order(self) -> None:
        source = self.source()
        non_haproxy_upload = self.block(
            source,
            "      - name: Upload non-HAProxy runtime evidence\n",
            "      - name: Upload real runtime evidence\n",
        )
        overview = source.split("      - name: Write connector runtime overview\n", 1)[1]
        self.assertIn("if: always() && matrix.connector != 'haproxy'", non_haproxy_upload)
        self.assertIn(UPLOAD_PIN, non_haproxy_upload)
        self.assertNotIn("verified-haproxy-case", non_haproxy_upload)
        self.assertIn("UPLOAD_EVIDENCE_OUTCOME:", overview)
        self.assertIn("steps.upload-runtime-evidence.outcome", overview)
        self.assertIn("steps.upload-non-haproxy-runtime-evidence.outcome", overview)
        self.assertLess(
            source.index("      - name: Prepare HAProxy runtime evidence boundary\n"),
            source.index("      - name: Run selected real with-CRS no-MRTS runtime\n"),
        )
        self.assertLess(
            source.index("      - name: Run selected real with-CRS no-MRTS runtime\n"),
            source.index("      - name: Project HAProxy runtime evidence\n"),
        )
        self.assertLess(
            source.index("      - name: Project HAProxy runtime evidence\n"),
            source.index("      - name: Verify HAProxy runtime evidence\n"),
        )
        self.assertLess(
            source.index("      - name: Verify HAProxy runtime evidence\n"),
            source.index("      - name: Upload real runtime evidence\n"),
        )


if __name__ == "__main__":
    unittest.main()
