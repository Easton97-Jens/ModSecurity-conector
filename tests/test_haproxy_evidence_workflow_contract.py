"""Static security contracts for the HAProxy evidence upload workflow path."""

from __future__ import annotations

from pathlib import Path
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
        self.assertIn('stage_parent=$(sudo -n /usr/bin/mktemp -d -- "$TRUSTED_RUNNER_TEMP/haproxy-runtime-evidence-parent.XXXXXXXX")', project)
        self.assertIn('stage_root="$stage_parent/package"', project)
        self.assertIn("sudo -n /usr/bin/mkdir -m 0700", project)
        self.assertIn(
            'sudo -n /usr/bin/chown --no-dereference "$EVIDENCE_UID:$RUNTIME_GID" -- "$stage_root"',
            project,
        )
        self.assertNotIn(
            'sudo -n /usr/bin/chown --no-dereference "$EVIDENCE_UID:$EVIDENCE_GID" -- "$stage_root"',
            project,
        )
        self.assertIn("sudo -n /usr/bin/chmod 0755", project)
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

    def test_projector_seals_the_upload_reader_path_without_other_traversal(self) -> None:
        projector = (
            ROOT / "ci" / "runtime" / "lifecycle" / "project-haproxy-runtime-evidence.py"
        ).read_text(encoding="utf-8")
        self.assertIn("os.fchmod(descriptor, 0o550)", projector)
        self.assertNotIn("os.fchmod(descriptor, 0o555)", projector)

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
