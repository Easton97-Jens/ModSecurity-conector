from __future__ import annotations

import os
import json
from pathlib import Path
import subprocess
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[3]
CONNECTOR = REPO_ROOT / "connectors" / "lighttpd"
PATCH = CONNECTOR / "patches" / "0001-lighttpd-1.4.84-msconnector-stream-hooks.patch"


class PatchedCoreBootstrapTest(unittest.TestCase):
    CORE_BUILDER = CONNECTOR / "build" / "build_patched_core.sh"

    @staticmethod
    def _configure_script() -> str:
        return (
            "#!/bin/sh\n"
            "set -eu\n"
            "printf '%s\\n' '#define LIGHTTPD_TEST_CONFIG 1' > config.h\n"
        )

    @staticmethod
    def _write_script(path: Path, content: str, *, executable: bool = True) -> None:
        path.write_text(content, encoding="utf-8")
        path.chmod(0o755 if executable else 0o644)

    def _fixture(
        self,
        root: Path,
        *,
        configure: bool,
        autogen: str,
        non_executable_configure: bool = False,
    ) -> dict[str, object]:
        source = root / "verified lighttpd source"
        patched_root = root / "patched lighttpd build"
        patched_source = patched_root / "lighttpd-1.4.84"
        core_build = patched_root / "build-1.4.84"
        stage_root = patched_root / "stage"
        tools = root / "test tools"
        trace = root / "autogen trace.txt"

        (source / "src").mkdir(parents=True)
        (source / "src" / "plugin.h").write_text(
            "#define LIGHTTPD_TEST_SOURCE 1\n", encoding="utf-8"
        )
        (source / "configure.ac").write_text(
            "AC_INIT([lighttpd],[1.4.84])\n", encoding="utf-8"
        )
        tools.mkdir()

        self._write_script(tools / "cc", "#!/bin/sh\nexit 0\n")
        self._write_script(
            tools / "patch",
            "#!/bin/sh\n"
            "set -eu\n"
            "target=\n"
            "while [ \"$#\" -gt 0 ]; do\n"
            "    case \"$1\" in\n"
            "        -d) target=$2; shift 2 ;;\n"
            "        *) shift ;;\n"
            "    esac\n"
            "done\n"
            "[ -n \"$target\" ]\n"
            "printf '%s\\n' '#define LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION 1' > \"$target/src/plugin.h\"\n",
        )
        self._write_script(
            tools / "make",
            "#!/bin/sh\n"
            "set -eu\n"
            "install_mode=0\n"
            "for argument in \"$@\"; do\n"
            "    [ \"$argument\" = install ] && install_mode=1\n"
            "done\n"
            "[ \"$install_mode\" -eq 1 ] || exit 0\n"
            "stage=${LIGHTTPD_TEST_STAGE_ROOT:?}\n"
            "mkdir -p \"$stage/bin\"\n"
            "cat > \"$stage/bin/lighttpd\" <<'EOF'\n"
            "#!/bin/sh\n"
            "if [ \"${1:-}\" = -v ]; then\n"
            "    printf '%s\\n' 'lighttpd/1.4.84'\n"
            "fi\n"
            "EOF\n"
            "chmod +x \"$stage/bin/lighttpd\"\n",
        )
        self._write_script(
            tools / "nm",
            "#!/bin/sh\n"
            "printf '%s\\n' '00000000 T plugins_call_handle_request_body'\n"
            "printf '%s\\n' '00000000 T plugins_call_handle_response_body'\n",
        )

        if configure:
            self._write_script(
                source / "configure",
                self._configure_script(),
                executable=not non_executable_configure,
            )

        if autogen != "missing":
            autogen_shebang = (
                "#!/usr/bin/env bash\n"
                if autogen == "unsupported_non_executable"
                else "#!/bin/sh\n"
            )
            autogen_script = f"{autogen_shebang}set -eu\n"
            autogen_script += 'printf "%s\\n" "$PWD" >> "$AUTOGEN_TRACE"\n'
            if autogen == "fails":
                autogen_script += "printf '%s\\n' 'missing bootstrap tool: test-autoreconf' >&2\nexit 41\n"
            elif autogen == "no_configure":
                autogen_script += "exit 0\n"
            elif autogen == "unsupported_non_executable":
                autogen_script += "exit 0\n"
            elif autogen in ("succeeds", "succeeds_non_executable"):
                autogen_script += (
                    "cat > configure <<'EOF'\n"
                    f"{self._configure_script()}"
                    "EOF\n"
                    "chmod +x configure\n"
                )
            elif autogen == "must_not_run":
                autogen_script += "printf '%s\\n' 'autogen should not have run' >&2\nexit 97\n"
            else:
                raise ValueError(f"unsupported autogen fixture: {autogen}")
            self._write_script(
                source / "autogen.sh",
                autogen_script,
                executable=autogen
                not in ("succeeds_non_executable", "unsupported_non_executable"),
            )

        environment = os.environ.copy()
        environment.update(
            {
                "BUILD_ROOT": str(root / "build root"),
                "LIGHTTPD_PATCHED_ROOT": str(patched_root),
                "LIGHTTPD_SOURCE_DIR": str(source),
                "LIGHTTPD_TEST_STAGE_ROOT": str(stage_root),
                "LIGHTTPD_MAKE_JOBS": "1",
                "AUTOGEN_TRACE": str(trace),
                "CC": "cc",
                "MAKE": "make",
                "NM": "nm",
                "PATH": f"{tools}{os.pathsep}{environment['PATH']}",
            }
        )
        return {
            "environment": environment,
            "patched_source": patched_source,
            "core_build": core_build,
            "trace": trace,
        }

    def _run_builder(self, environment: dict[str, str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["sh", str(self.CORE_BUILDER)],
            cwd=REPO_ROOT,
            env=environment,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def test_existing_executable_configure_skips_autogen(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lighttpd-bootstrap-") as temporary:
            fixture = self._fixture(
                Path(temporary) / "path with spaces", configure=True, autogen="must_not_run"
            )
            result = self._run_builder(fixture["environment"])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("mode=build", result.stdout)
            self.assertFalse(fixture["trace"].exists())

    def test_missing_configure_bootstraps_with_posix_non_executable_autogen(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lighttpd-bootstrap-") as temporary:
            fixture = self._fixture(
                Path(temporary) / "path with spaces",
                configure=False,
                autogen="succeeds_non_executable",
            )
            result = self._run_builder(fixture["environment"])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                fixture["trace"].read_text(encoding="utf-8").splitlines(),
                [str(fixture["patched_source"])],
            )
            self.assertTrue((fixture["patched_source"] / "configure").stat().st_mode & 0o111)

    def test_non_executable_configure_bootstraps_in_the_patched_copy(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lighttpd-bootstrap-") as temporary:
            fixture = self._fixture(
                Path(temporary) / "path with spaces",
                configure=True,
                autogen="succeeds",
                non_executable_configure=True,
            )
            result = self._run_builder(fixture["environment"])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                fixture["trace"].read_text(encoding="utf-8").splitlines(),
                [str(fixture["patched_source"])],
            )
            self.assertTrue((fixture["patched_source"] / "configure").stat().st_mode & 0o111)

    def test_missing_configure_and_autogen_blocks_before_build_directory(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lighttpd-bootstrap-") as temporary:
            fixture = self._fixture(
                Path(temporary) / "path with spaces", configure=False, autogen="missing"
            )
            result = self._run_builder(fixture["environment"])
            self.assertEqual(result.returncode, 77)
            self.assertIn("bootstrap script is missing", result.stderr)
            self.assertIn(str(fixture["patched_source"] / "autogen.sh"), result.stderr)
            self.assertFalse(fixture["core_build"].exists())

    def test_failing_autogen_reports_exit_status_and_stops(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lighttpd-bootstrap-") as temporary:
            fixture = self._fixture(
                Path(temporary) / "path with spaces", configure=False, autogen="fails"
            )
            result = self._run_builder(fixture["environment"])
            self.assertEqual(result.returncode, 77)
            self.assertIn("exit status 41", result.stderr)
            self.assertIn("missing bootstrap tool: test-autoreconf", result.stderr)
            self.assertFalse(fixture["core_build"].exists())

    def test_successful_autogen_without_executable_configure_blocks(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lighttpd-bootstrap-") as temporary:
            fixture = self._fixture(
                Path(temporary) / "path with spaces",
                configure=False,
                autogen="no_configure",
            )
            result = self._run_builder(fixture["environment"])
            self.assertEqual(result.returncode, 77)
            self.assertIn("without an executable configure script", result.stderr)
            self.assertFalse(fixture["core_build"].exists())

    def test_non_executable_autogen_with_unsupported_interpreter_blocks(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lighttpd-bootstrap-") as temporary:
            fixture = self._fixture(
                Path(temporary) / "path with spaces",
                configure=False,
                autogen="unsupported_non_executable",
            )
            result = self._run_builder(fixture["environment"])
            self.assertEqual(result.returncode, 77)
            self.assertIn("does not declare a supported POSIX shell", result.stderr)
            self.assertFalse(fixture["core_build"].exists())

    def test_repeat_build_reuses_configure_without_second_autogen(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lighttpd-bootstrap-") as temporary:
            fixture = self._fixture(
                Path(temporary) / "path with spaces", configure=False, autogen="succeeds"
            )
            first = self._run_builder(fixture["environment"])
            second = self._run_builder(fixture["environment"])
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn("mode=reused", second.stdout)
            self.assertEqual(
                fixture["trace"].read_text(encoding="utf-8").splitlines(),
                [str(fixture["patched_source"])],
            )


class PatchedHostContractTest(unittest.TestCase):
    def test_patch_uses_a_file_scope_compile_time_size_check(self) -> None:
        patch = PATCH.read_text(encoding="utf-8")
        self.assertNotIn("ck_static_assert", patch)
        self.assertIn("plugin_fn_request_body_data_must_match_plugin_fn_data", patch)
        self.assertIn("plugin_fn_response_body_data_must_match_plugin_fn_data", patch)

    def test_patched_core_and_host_targets_are_separate_from_no_crs(self) -> None:
        makefile = (CONNECTOR / "Makefile").read_text(encoding="utf-8")
        self.assertIn("build-lighttpd-patched-core", makefile)
        self.assertIn("build-lighttpd-patched-host", makefile)
        self.assertIn("check-lighttpd-patched-host", makefile)
        self.assertIn("runtime-smoke-lighttpd-patched", makefile)

        patched_target = makefile.split("runtime-smoke-lighttpd-patched:", 1)[1].split(
            "\n\n", 1
        )[0]
        self.assertNotIn("MSCONNECTOR_NO_CRS_BASELINE", patched_target)

    def test_patched_build_contract_stages_a_verified_core_and_module(self) -> None:
        core = (CONNECTOR / "build" / "build_patched_core.sh").read_text(encoding="utf-8")
        host = (CONNECTOR / "build" / "build_patched_host.sh").read_text(encoding="utf-8")
        check = (CONNECTOR / "harness" / "check_patched_lifecycle_host.sh").read_text(
            encoding="utf-8"
        )

        for required in (
            "AC_INIT([lighttpd],[1.4.84]",
            "configure",
            '"$MAKE_BIN" -C "$CORE_BUILD_DIR" -j "$MAKE_JOBS"',
            '"$MAKE_BIN" -C "$CORE_BUILD_DIR" install',
            "plugins_call_handle_request_body",
            "plugins_call_handle_response_body",
            "patched-core-build-info.txt",
        ):
            self.assertIn(required, core)
        self.assertIn("LIGHTTPD_MSCONNECTOR_CORE_MODE=patched", host)
        self.assertIn("LIGHTTPD_MODULE_DIR=\"$MODULE_DIR\"", host)
        self.assertIn("patched-host-build-info.txt", host)
        self.assertIn("module_sha256", check)
        self.assertIn("core_binary_sha256", check)
        self.assertIn("PROXY_MODULE_PATH", host)
        self.assertIn("mod_proxy_plugin_init", host)
        self.assertIn("proxy_module_sha256", host)
        self.assertIn("proxy_module_sha256", check)

    def test_patched_config_allows_only_identity_entity_body_input(self) -> None:
        preparer = CONNECTOR / "harness" / "prepare_patched_lifecycle_smoke.sh"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "lighttpd-core-patched" / "lighttpd-1.4.84" / "src"
            source.mkdir(parents=True)
            (source / "plugin.h").write_text(
                "#define LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION 1\n",
                encoding="utf-8",
            )
            environment = os.environ.copy()
            environment.update(
                {
                    "BUILD_ROOT": str(root),
                    "LIGHTTPD_PATCHED_ROOT": str(root / "lighttpd-core-patched"),
                    "LIGHTTPD_PATCHED_RESPONSE_BODY_MODE": "streaming",
                }
            )
            result = subprocess.run(
                ["sh", str(preparer)],
                cwd=REPO_ROOT,
                env=environment,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            config = Path(result.stdout.strip())
            self.assertIn(
                "response_body_mode=streaming",
                (config.parent / "msconnector-runtime.conf").read_text(encoding="utf-8"),
            )

    def test_patched_config_adds_only_the_http1_proxy_routes_for_streaming(self) -> None:
        preparer = CONNECTOR / "harness" / "prepare_patched_lifecycle_smoke.sh"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "lighttpd-core-patched" / "lighttpd-1.4.84" / "src"
            source.mkdir(parents=True)
            (source / "plugin.h").write_text(
                "#define LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION 1\n",
                encoding="utf-8",
            )
            environment = os.environ.copy()
            environment.update(
                {
                    "BUILD_ROOT": str(root),
                    "LIGHTTPD_PATCHED_ROOT": str(root / "lighttpd-core-patched"),
                    "LIGHTTPD_PATCHED_RESPONSE_BODY_MODE": "streaming",
                    "LIGHTTPD_PROXY_BARRIER_PORT": "19001",
                    "LIGHTTPD_PROXY_FIXTURE_PORT": "19002",
                }
            )
            result = subprocess.run(
                ["sh", str(preparer)],
                cwd=REPO_ROOT,
                env=environment,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            config = Path(result.stdout.strip()).read_text(encoding="utf-8")
        self.assertIn('server.modules = ( "mod_proxy", "mod_msconnector" )', config)
        self.assertIn("server.stream-response-body = 1", config)
        self.assertIn('"/p4/barrier/"', config)
        self.assertIn('"/p4/fixture/"', config)
        self.assertNotIn("mod_h2", config)

    def test_patched_config_rejects_unproven_content_encoding(self) -> None:
        preparer = CONNECTOR / "harness" / "prepare_patched_lifecycle_smoke.sh"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "lighttpd-core-patched" / "lighttpd-1.4.84" / "src"
            source.mkdir(parents=True)
            (source / "plugin.h").write_text(
                "#define LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION 1\n",
                encoding="utf-8",
            )
            environment = os.environ.copy()
            environment.update(
                {
                    "BUILD_ROOT": str(root),
                    "LIGHTTPD_PATCHED_ROOT": str(root / "lighttpd-core-patched"),
                    "LIGHTTPD_PATCHED_RESPONSE_BODY_MODE": "streaming",
                    "LIGHTTPD_PATCHED_ENTITY_ENCODING": "gzip",
                }
            )
            result = subprocess.run(
                ["sh", str(preparer)],
                cwd=REPO_ROOT,
                env=environment,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        self.assertEqual(result.returncode, 77)
        self.assertIn("identity entity-body input", result.stderr)

    def test_response_callback_ingests_entity_ranges_and_finishes_at_eos(self) -> None:
        module = (CONNECTOR / "module" / "mod_msconnector.c").read_text(encoding="utf-8")
        callback = module.rsplit("static plugin_body_hook_result mod_msconnector_handle_response_body", 1)[1].split(
            "#endif", 1
        )[0]
        finish = module.rsplit("static plugin_body_hook_result mod_msconnector_finish_response_body", 1)[1].split(
            "static plugin_body_hook_result mod_msconnector_handle_response_body", 1
        )[0]
        self.assertIn("const unsigned char *data", callback)
        self.assertIn("msconnector_runtime_transaction_append_response_body_chunk", callback)
        self.assertIn("msconnector_runtime_transaction_set_response_commit_state", callback)
        self.assertIn("mod_msconnector_finish_response_body", callback)
        self.assertIn("mod_msconnector_handle_response_start(r, p)", callback)
        self.assertNotIn("lighttpd_modsecurity_visit_body_range", callback)
        self.assertIn("msconnector_runtime_transaction_finish_response_body", finish)
        self.assertIn("msconnector_late_intervention_resolve", finish)
        self.assertIn("msconnector_runtime_phase4_mode", finish)
        self.assertIn("NOT EXECUTED", finish)

    def test_safe_phase4_host_action_marks_late_only_after_commit(self) -> None:
        module = (CONNECTOR / "module" / "mod_msconnector.c").read_text(encoding="utf-8")
        finish = module.rsplit("static plugin_body_hook_result mod_msconnector_finish_response_body", 1)[1].split(
            "static plugin_body_hook_result mod_msconnector_handle_response_body", 1
        )[0]
        self.assertIn("MSCONNECTOR_LATE_INTERVENTION_DENY_IF_POSSIBLE", finish)
        self.assertIn("mod_msconnector_apply_decision(r, p, ctx, &decision)", finish)
        self.assertIn("decision.late_intervention = 1;", finish)
        self.assertLess(
            finish.index("decision.late_intervention = 1;"),
            finish.index("msconnector_runtime_transaction_record_host_action"),
        )

    def test_patch_hooks_entity_bytes_before_transfer_encoding_not_socket_write(self) -> None:
        patch = PATCH.read_text(encoding="utf-8")
        self.assertIn("http_chunk_msconnector_entity_body", patch)
        self.assertIn("http_chunk_msconnector_entity_close", patch)
        self.assertIn("resp_body_entity_hook_suppressed", patch)
        self.assertIn("if (r->gw_dechunk->done) {", patch)
        self.assertIn("return http_chunk_msconnector_entity_close(r);", patch)
        self.assertNotIn("msconnector-eos-debug", patch)
        self.assertIn("http1_entity_body_before_transfer_encoding", (
            CONNECTOR / "build" / "build_patched_core.sh"
        ).read_text(encoding="utf-8"))
        self.assertNotIn("--- a/src/connections.c", patch)
        self.assertNotIn("network_write", patch)
        self.assertLess(
            patch.index("http_chunk_msconnector_entity_body(r,"),
            patch.index("if (http_chunk_uses_tempfile(cq, len))"),
        )

    def test_unobserved_response_lifecycle_is_not_synthesized_after_entity_disconnect(self) -> None:
        module = (CONNECTOR / "module" / "mod_msconnector.c").read_text(
            encoding="utf-8"
        )
        response_start = module.split(
            "REQUEST_FUNC(mod_msconnector_handle_response_start)", 1
        )[1].split("REQUEST_FUNC(mod_msconnector_handle_request_reset)", 1)[0]
        request_reset = module.split(
            "REQUEST_FUNC(mod_msconnector_handle_request_reset)", 1
        )[1]
        self.assertNotIn("mod_msconnector_finish_uninspected_response_body", response_start)
        self.assertIn("mod_msconnector_finish_uninspected_response_body(r, ctx)", request_reset)
        self.assertIn("no synthetic Phase-4 finalization", request_reset)
        self.assertIn(
            "msconnector_runtime_transaction_finish_unobserved_response_body",
            module,
        )
        self.assertNotIn(
            "msconnector_runtime_transaction_finish_response_body(r, ctx)", request_reset
        )

    def test_request_body_mapper_uses_an_unsigned_size_bound(self) -> None:
        mapper = (CONNECTOR / "src" / "lighttpd_modsecurity_mapper.c").read_text(
            encoding="utf-8"
        )
        self.assertIn("(uintmax_t)take > (uintmax_t)SIZE_MAX", mapper)
        self.assertNotIn("take > (off_t)SIZE_MAX", mapper)

    def test_disruptive_host_action_is_recorded_after_status_selection(self) -> None:
        module = (CONNECTOR / "module" / "mod_msconnector.c").read_text(
            encoding="utf-8"
        )
        action = module.split("static handler_t mod_msconnector_apply_decision", 1)[1].split(
            "#ifdef LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION", 1
        )[0]
        self.assertIn("result = http_status_set_err(r, status);", action)
        self.assertIn("msconnector_runtime_transaction_record_host_action", action)
        self.assertLess(
            action.index("result = http_status_set_err(r, status);"),
            action.index("msconnector_runtime_transaction_record_host_action"),
        )
        self.assertIn("MSCONNECTOR_DECISION_ACTION_DENY", action)
        self.assertIn('"http_status"', action)

    def test_patched_runtime_labels_raw_events_with_its_selected_host_path(self) -> None:
        module = (CONNECTOR / "module" / "mod_msconnector.c").read_text(
            encoding="utf-8"
        )
        self.assertIn("msconnector_runtime_set_event_integration_mode", module)
        self.assertIn('"patched-native-lighttpd"', module)

    def test_host_transaction_identifier_uses_a_process_local_serial(self) -> None:
        module = (CONNECTOR / "module" / "mod_msconnector.c").read_text(
            encoding="utf-8"
        )
        self.assertIn("unsigned long host_transaction_counter;", module)
        factory = module.split("static handler_ctx *handler_ctx_create", 1)[1].split(
            "static void handler_ctx_destroy", 1
        )[0]
        self.assertIn("++p->host_transaction_counter;", factory)
        self.assertIn('"lighttpd-%ld-%lu"', factory)
        self.assertNotIn('"lighttpd-%ld-%d-%u-%u"', factory)

    def test_full_lifecycle_runner_uses_real_http1_entity_and_barrier_evidence(self) -> None:
        runner = (CONNECTOR / "harness" / "run_patched_full_lifecycle.sh").read_text(
            encoding="utf-8"
        )
        self.assertIn("LIGHTTPD_PATCHED_RESPONSE_BODY_MODE=streaming", runner)
        self.assertIn("lighttpd_http1_entity_fixture_upstream.py", runner)
        self.assertIn('--runtime-output-root "$SMOKE_DIR"', runner)
        self.assertIn("verify_runtime_output_paths", runner)
        self.assertIn("safe_output_path(root, Path(sys.argv[3])", runner)
        self.assertIn("--merge-evidence", runner)
        self.assertIn("FULL_LIFECYCLE_EVIDENCE_OUTPUT", runner)
        self.assertIn("phase4_end_of_stream_evaluation_status", runner)
        self.assertIn("phase4_first_byte_before_response_end_status", runner)
        self.assertIn("phase4_no_full_response_buffering_status", runner)
        self.assertNotIn("wire bytes", runner)
        self.assertIn(': "${NO_CRS_RUN_ID:?NO_CRS_RUN_ID is required}"', runner)

        serve_command = runner.split(
            '"$PYTHON_BIN" "$SYNCHRONIZED_UPSTREAM" --serve', 1
        )[1].split("BARRIER_PID=$!", 1)[0]
        merge_command = runner.split(
            '"$PYTHON_BIN" "$SYNCHRONIZED_UPSTREAM" --merge-evidence', 1
        )[1].split('fail "could not write payload-free synchronized first-byte evidence"', 1)[0]
        self.assertIn('--control-root "$SMOKE_DIR"', serve_command)
        self.assertIn('--control-root "$SMOKE_DIR"', merge_command)
        writer_command = runner.split('"$PYTHON_BIN" "$RESULT_WRITER" \\\n', 1)[1].split(
            "if grep -Fq", 1
        )[0]
        self.assertIn('--run-id "$NO_CRS_RUN_ID"', writer_command)

    def test_parent_routes_lighttpd_first_byte_evidence_through_the_smoke_root(self) -> None:
        lifecycle = (REPO_ROOT / "ci" / "runtime" / "lifecycle" / "run-no-crs-baseline.sh").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "FIRST_BYTE_EVIDENCE=$CONNECTOR_RUN_ROOT/first-byte-evidence.json",
            lifecycle,
        )
        self.assertIn(
            'if [ "$connector" = lighttpd ] && [ "$NO_CRS_ARTIFACT_PROFILE" = full_lifecycle ]; then',
            lifecycle,
        )
        self.assertIn(
            "LIGHTTPD_STAGE_FIRST_BYTE_EVIDENCE=$LIGHTTPD_RUNTIME_ROOT/first-byte-evidence.json",
            lifecycle,
        )
        self.assertIn(
            "FIRST_BYTE_EVIDENCE_SOURCE=$LIGHTTPD_STAGE_FIRST_BYTE_EVIDENCE",
            lifecycle,
        )
        self.assertIn(
            'FULL_LIFECYCLE_EVIDENCE_OUTPUT="$STAGE_FIRST_BYTE_EVIDENCE_OUTPUT"',
            lifecycle,
        )
        self.assertIn(
            'cp "$FIRST_BYTE_EVIDENCE_SOURCE" "$FIRST_BYTE_EVIDENCE"',
            lifecycle,
        )

    def test_full_lifecycle_runner_centralizes_fixed_status_and_diagnostic_literals(self) -> None:
        runner = (CONNECTOR / "harness" / "run_patched_full_lifecycle.sh").read_text(
            encoding="utf-8"
        )
        status_name = "HTTP_STATUS_FORMAT"
        diagnostic_name = "DIAGNOSTIC_LINES"
        status_value = "%{" + "http_code" + "}"
        diagnostic_value = ",".join(("1", "200")) + "p"
        status_declaration = f"{status_name}='{status_value}'"
        diagnostic_declaration = f"{diagnostic_name}='{diagnostic_value}'"
        status_use = f'--write-out "${status_name}"'
        diagnostic_use = f'sed -n "${diagnostic_name}"'

        self.assertEqual(runner.count(status_declaration), 1)
        self.assertEqual(runner.count(diagnostic_declaration), 1)
        self.assertLess(runner.index(status_declaration), runner.index(status_use))
        self.assertLess(runner.index(diagnostic_declaration), runner.index(diagnostic_use))
        self.assertLess(runner.index(status_declaration), runner.index("blocked() {"))
        self.assertLess(runner.index(diagnostic_declaration), runner.index("blocked() {"))
        self.assertEqual(runner.count(status_use), 8)
        self.assertEqual(runner.count(diagnostic_use), 6)

        source_without_declarations = runner.replace(status_declaration, "").replace(
            diagnostic_declaration, ""
        )
        self.assertNotIn(status_value, source_without_declarations)
        self.assertNotIn(diagnostic_value, source_without_declarations)
        self.assertNotIn(f"export {status_name}", runner)
        self.assertNotIn(f"export {diagnostic_name}", runner)

        for control in (
            "set -eu",
            "trap cleanup EXIT HUP INT TERM",
            "trap - EXIT HUP INT TERM",
            'if ! wait "$FIRST_BYTE_CLIENT_PID"; then',
            'if grep -Fq \'"status": "FAIL"\' "$RESULTS_PATH"; then',
        ):
            self.assertIn(control, runner)

        success = "2" + "00"
        denied = "4" + "03"
        alternative = "4" + "29"
        for result_name, expected in (
            ("allow_status", success),
            ("deny_status", denied),
            ("alternative_status", alternative),
            ("request_body_status", denied),
            ("response_header_status", denied),
            ("content_length_status", success),
            ("chunked_status", success),
            ("phase4_safe_status", success),
        ):
            self.assertIn(f'[ "${result_name}" = {expected} ] || fail', runner)

    def test_result_writer_projects_only_bounded_eos_metadata_from_one_safe_event(self) -> None:
        writer = CONNECTOR / "harness" / "write_patched_lifecycle_results.py"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)

            def safe_event(size: int, transaction_id: str) -> dict[str, object]:
                return {
                    "connector": "lighttpd",
                    "integration_mode": "patched-native-lighttpd",
                    "event": "response_blocked",
                    "message_id": "response_blocked",
                    "transaction_id": transaction_id,
                    "rule_id": "1100301",
                    "phase": "response_body",
                    "status": "blocked",
                    "http_status": 403,
                    "original_http_status": 200,
                    "visible_http_status": 200,
                    "requested_action": "deny",
                    "actual_action": "log_only",
                    "late_intervention": True,
                    "late_intervention_mode": "safe",
                    "headers_sent": True,
                    "body_started": True,
                    "response_committed": True,
                    "connection_aborted": False,
                    "transport_result": "log_only",
                    "body_bytes_seen": size,
                    "body_bytes_inspected": size,
                }

            barrier = root / "barrier.jsonl"
            content_length = root / "content-length.jsonl"
            chunked = root / "chunked.jsonl"
            events = root / "events.jsonl"
            for path, event in (
                (barrier, safe_event(31, "tx-barrier")),
                (content_length, safe_event(29, "tx-content-length")),
                (chunked, safe_event(24, "tx-chunked")),
            ):
                path.write_text(json.dumps(event) + "\n", encoding="utf-8")
            events.write_text("", encoding="utf-8")
            fixture = root / "fixture.json"
            fixture.write_text(
                json.dumps(
                    {
                        "evidence_type": "lighttpd_http1_entity_fixture_result",
                        "body_payload_persisted": False,
                        "content_length_requests": 1,
                        "chunked_requests": 1,
                        "content_length_entity_bytes": 29,
                        "chunked_entity_bytes": 24,
                    }
                ),
                encoding="utf-8",
            )
            evidence = root / "first-byte.json"
            evidence.write_text("{}\n", encoding="utf-8")
            output = root / "results.jsonl"
            projection = root / "projection.jsonl"
            summary = root / "summary.json"
            result = subprocess.run(
                [
                    "python3",
                    str(writer),
                    "--events", str(events),
                    "--run-id", "lighttpd-current-run",
                    "--output", str(output),
                    "--selected-case-ids",
                    "phase4_rule_observed phase4_end_of_stream_evaluation "
                    "phase4_deny_after_commit_log_only_safe "
                    "phase4_first_byte_before_response_end "
                    "phase4_no_full_response_buffering",
                    "--allow-status", "200",
                    "--deny-status", "403",
                    "--alternative-status", "429",
                    "--request-body-status", "403",
                    "--response-header-status", "403",
                    "--phase4-safe-events", str(barrier),
                    "--phase4-projected-events-output", str(projection),
                    "--phase4-safe-status", "200",
                    "--phase4-first-byte-evidence", str(evidence),
                    "--content-length-events", str(content_length),
                    "--chunked-events", str(chunked),
                    "--entity-fixture-result", str(fixture),
                    "--phase4-summary-output", str(summary),
                    "--runtime-output-root", str(root),
                ],
                cwd=REPO_ROOT,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            projected = json.loads(projection.read_text(encoding="utf-8"))
            self.assertTrue(projected["eos_seen"])
            self.assertTrue(projected["end_of_stream_evaluation"])
            self.assertEqual(projected["run_id"], "lighttpd-current-run")
            self.assertNotIn("event_hash", projected)
            rows = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]
            self.assertEqual({row["status"] for row in rows}, {"PASS"})
            self.assertTrue(all(row["transaction_ids"] == ["tx-barrier"] for row in rows))
            self.assertEqual(
                {row["first_byte_evidence_path"] for row in rows},
                {str(evidence)},
            )
            summary_value = json.loads(summary.read_text(encoding="utf-8"))
            self.assertEqual(summary_value["phase4_end_of_stream_evaluation_status"], 200)
            self.assertEqual(summary_value["phase4_first_byte_before_response_end_status"], 200)
            self.assertEqual(summary_value["phase4_no_full_response_buffering_status"], 200)


if __name__ == "__main__":
    unittest.main()
