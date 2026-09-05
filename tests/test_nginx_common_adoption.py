"""Mutation coverage for NGINX's helper-aware Common-adoption checker."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "ci" / "checks" / "connectors" / "nginx" / "check-nginx-common-adoption.py"
NGINX = ROOT / "connectors" / "nginx"
SOURCES = (
    "ngx_http_modsecurity_common.h",
    "ngx_http_modsecurity_module.c",
    "ngx_http_modsecurity_mapper.h",
    "ngx_http_modsecurity_mapper.c",
    "ngx_http_modsecurity_body_filter.c",
    "ngx_http_modsecurity_access.c",
    "ngx_http_modsecurity_header_filter.c",
    "ngx_http_modsecurity_log.c",
    "ddebug.h",
)


def function_bounds(source: str, signature: str) -> tuple[int, int]:
    """Return exactly one synthetic function definition's source bounds."""
    start = source.index(signature)
    opening = source.index("{", start)
    depth = 0
    for position in range(opening, len(source)):
        if source[position] == "{":
            depth += 1
        elif source[position] == "}":
            depth -= 1
            if depth == 0:
                return start, position + 1
    raise AssertionError(f"unbalanced synthetic function: {signature}")


def replace_in_function(
    path: Path, signature: str, old: str, new: str
) -> None:
    """Replace one source fragment in the selected synthetic function."""
    source = path.read_text(encoding="utf-8")
    start, end = function_bounds(source, signature)
    original = source[start:end]
    if original.count(old) != 1:
        raise AssertionError(f"expected one mutable fragment in {path}: {old!r}")
    path.write_text(
        source[:start] + original.replace(old, new, 1) + source[end:],
        encoding="utf-8",
    )


def insert_before_signature(path: Path, signature: str, directive: str) -> None:
    """Insert one preprocessing directive immediately before a C definition."""
    source = path.read_text(encoding="utf-8")
    start = source.index(signature)
    path.write_text(
        source[:start] + directive + "\n" + source[start:], encoding="utf-8"
    )


def prepend_directive(path: Path, directive: str) -> None:
    """Add one preprocessing directive before a local included header's guard."""
    source = path.read_text(encoding="utf-8")
    path.write_text(directive + "\n" + source, encoding="utf-8")


def inject_inactive_decoy(
    path: Path,
    signature: str,
    old: str,
    new: str,
    opening: str = "#if 0\n",
    closing: str = "#endif\n",
) -> None:
    """Hide a safe twin in an inactive branch while corrupting the live one."""
    source = path.read_text(encoding="utf-8")
    start, end = function_bounds(source, signature)
    original = source[start:end]
    if original.count(old) != 1:
        raise AssertionError(f"expected one mutable fragment in {path}: {old!r}")
    malformed = original.replace(old, new, 1)
    path.write_text(
        source[:start] + opening + original + "\n" + closing + malformed + source[end:],
        encoding="utf-8",
    )


def inject_outer_guard_else_decoy(
    path: Path, signature: str, old: str, new: str
) -> None:
    """Put a safe twin in the outer include guard's inactive else branch."""
    source = path.read_text(encoding="utf-8")
    start, end = function_bounds(source, signature)
    original = source[start:end]
    if original.count(old) != 1:
        raise AssertionError(f"expected one mutable fragment in {path}: {old!r}")
    terminal_endif = source.rfind("#endif")
    if terminal_endif < end:
        raise AssertionError(f"expected outer include guard in {path}")
    malformed = original.replace(old, new, 1)
    path.write_text(
        source[:start]
        + malformed
        + source[end:terminal_endif]
        + "#else\n"
        + original
        + "\n"
        + source[terminal_endif:],
        encoding="utf-8",
    )


class NginxCommonAdoptionCheckerTests(unittest.TestCase):
    """Exercise semantic contracts against isolated inactive-branch decoys."""

    def _copy_repository(self, destination: Path) -> Path:
        (destination / "Makefile").write_text(
            "# synthetic checker repository\n", encoding="utf-8"
        )
        checker = destination / "ci" / "checks" / "connectors" / "nginx" / CHECKER.name
        checker.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(CHECKER, checker)
        source_directory = destination / "connectors" / "nginx" / "src"
        source_directory.mkdir(parents=True, exist_ok=True)
        for name in SOURCES:
            shutil.copy2(NGINX / "src" / name, source_directory / name)
        shutil.copy2(
            ROOT / "connectors" / "profile_registry.h",
            destination / "connectors" / "profile_registry.h",
        )
        shutil.copytree(
            ROOT / "common" / "include", destination / "common" / "include"
        )
        shutil.copy2(NGINX / "config", destination / "connectors" / "nginx" / "config")
        return destination

    def _run_checker(self, mutate=None) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory(prefix="nginx-common-adoption-") as temporary:
            repository = self._copy_repository(Path(temporary))
            if mutate is not None:
                mutate(repository)
            environment = os.environ.copy()
            environment["PYTHONDONTWRITEBYTECODE"] = "1"
            return subprocess.run(
                [sys.executable, str(repository / "ci" / "checks" / "connectors" / "nginx" / CHECKER.name)],
                cwd=repository,
                env=environment,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )

    def _assert_rejected(self, mutate, message: str) -> None:
        result = self._run_checker(mutate)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(message, result.stdout + result.stderr)

    def test_current_helper_aware_contract_is_accepted(self) -> None:
        result = self._run_checker()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(
            "PASS: NGINX Server resolver preserves the bounded explicit-length response-header sink",
            result.stdout,
        )

    def test_inactive_mapper_validator_decoy_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            inject_inactive_decoy(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_access.c",
                "static ngx_int_t\nngx_http_modsecurity_validate_common_request_mapper",
                "mapper_error);\n        return NGX_HTTP_BAD_REQUEST;",
                "mapper_error);\n        return NGX_OK;",
            )

        self._assert_rejected(
            mutate,
            "NGINX request mapper validation fails closed before request-header initialization",
        )

    def test_inactive_initializer_propagation_decoy_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            inject_inactive_decoy(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_access.c",
                "static ngx_int_t\nngx_http_modsecurity_initialize_request",
                "ctx->intervention_triggered = 1;\n        return rc;",
                "ctx->intervention_triggered = 1;\n        return NGX_OK;",
            )

        self._assert_rejected(
            mutate,
            "NGINX request mapper validation fails closed before request-header initialization",
        )

    def test_inactive_response_wrapper_decoy_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            inject_inactive_decoy(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_common.h",
                "static ngx_inline ngx_int_t\nngx_http_modsecurity_add_n_response_header",
                "value_len, 1) != NGX_OK) {\n        return NGX_ERROR;",
                "value_len, 1) != NGX_OK) {\n        return NGX_OK;",
            )

        self._assert_rejected(
            mutate,
            "NGINX Server resolver preserves the bounded explicit-length response-header sink",
        )

    def test_active_preprocessor_mapper_early_return_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            replace_in_function(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_access.c",
                "static ngx_int_t\nngx_http_modsecurity_validate_common_request_mapper",
                "    msconnector_request_mapper_contract_init(&contract);\n",
                "#if 1\n"
                "    return NGX_OK;\n"
                "#endif\n\n"
                "    msconnector_request_mapper_contract_init(&contract);\n",
            )

        self._assert_rejected(
            mutate,
            "NGINX request mapper validation fails closed before request-header initialization",
        )

    def test_unconditional_mapper_early_return_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            replace_in_function(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_access.c",
                "static ngx_int_t\nngx_http_modsecurity_validate_common_request_mapper",
                "    msconnector_request_mapper_contract_init(&contract);\n",
                "    return NGX_OK;\n\n"
                "    msconnector_request_mapper_contract_init(&contract);\n",
            )

        self._assert_rejected(
            mutate,
            "NGINX request mapper validation fails closed before request-header initialization",
        )

    def test_permitted_macro_early_return_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            path = (
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_access.c"
            )
            signature = (
                "static ngx_int_t\n"
                "ngx_http_modsecurity_validate_common_request_mapper"
            )
            insert_before_signature(
                path, signature, "#define MSCONNECTOR_EARLY_RETURN return 0"
            )
            replace_in_function(
                path,
                signature,
                "    msconnector_request_mapper_contract_init(&contract);\n",
                "    MSCONNECTOR_EARLY_RETURN;\n"
                "    msconnector_request_mapper_contract_init(&contract);\n",
            )

        self._assert_rejected(
            mutate,
            "NGINX request mapper validation fails closed before request-header initialization",
        )

    def test_ucn_macro_name_early_return_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            path = (
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_access.c"
            )
            signature = (
                "static ngx_int_t\n"
                "ngx_http_modsecurity_validate_common_request_mapper"
            )
            insert_before_signature(
                path, signature, "#define \\u004dSCONNECTOR_EARLY_RETURN return 0"
            )
            replace_in_function(
                path,
                signature,
                "    msconnector_request_mapper_contract_init(&contract);\n",
                "    MSCONNECTOR_EARLY_RETURN;\n"
                "    msconnector_request_mapper_contract_init(&contract);\n",
            )

        self._assert_rejected(
            mutate,
            "NGINX request mapper validation fails closed before request-header initialization",
        )

    def test_permitted_macro_control_flow_capture_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            path = (
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_access.c"
            )
            signature = (
                "static ngx_int_t\n"
                "ngx_http_modsecurity_validate_common_request_mapper"
            )
            insert_before_signature(
                path,
                signature,
                "#define MSCONNECTOR_SKIP_NEXT_STATEMENT if (1) ; else",
            )
            replace_in_function(
                path,
                signature,
                "    msconnector_request_mapper_contract_init(&contract);\n",
                "    MSCONNECTOR_SKIP_NEXT_STATEMENT\n"
                "    msconnector_request_mapper_contract_init(&contract);\n",
            )

        self._assert_rejected(
            mutate,
            "NGINX request mapper validation fails closed before request-header initialization",
        )

    def test_active_preprocessor_response_early_return_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            replace_in_function(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_common.h",
                "static ngx_inline ngx_int_t\nngx_http_modsecurity_add_n_response_header",
                "    if (ngx_http_modsecurity_validate_header(ctx, name, name_len, value,\n",
                "#if 1\n"
                "    return NGX_ERROR;\n"
                "#endif\n\n"
                "    if (ngx_http_modsecurity_validate_header(ctx, name, name_len, value,\n",
            )

        self._assert_rejected(
            mutate,
            "NGINX Server resolver preserves the bounded explicit-length response-header sink",
        )

    def test_line_spliced_inactive_mapper_decoy_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            inject_inactive_decoy(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_access.c",
                "static ngx_int_t\nngx_http_modsecurity_validate_common_request_mapper",
                "mapper_error);\n        return NGX_HTTP_BAD_REQUEST;",
                "mapper_error);\n        return NGX_OK;",
                "#\\\nif 0\n",
                "#\\\nendif\n",
            )

        self._assert_rejected(
            mutate,
            "NGINX request mapper validation fails closed before request-header initialization",
        )

    def test_trigraph_inactive_response_wrapper_decoy_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            inject_inactive_decoy(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_common.h",
                "static ngx_inline ngx_int_t\nngx_http_modsecurity_add_n_response_header",
                "value_len, 1) != NGX_OK) {\n        return NGX_ERROR;",
                "value_len, 1) != NGX_OK) {\n        return NGX_OK;",
                "??=if 0\n",
                "??=endif\n",
            )

        self._assert_rejected(
            mutate,
            "NGINX Server resolver preserves the bounded explicit-length response-header sink",
        )

    def test_digraph_inactive_response_wrapper_decoy_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            inject_inactive_decoy(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_common.h",
                "static ngx_inline ngx_int_t\nngx_http_modsecurity_add_n_response_header",
                "value_len, 1) != NGX_OK) {\n        return NGX_ERROR;",
                "value_len, 1) != NGX_OK) {\n        return NGX_OK;",
                "%:if 0\n",
                "%:endif\n",
            )

        self._assert_rejected(
            mutate,
            "NGINX Server resolver preserves the bounded explicit-length response-header sink",
        )

    def test_outer_include_guard_else_decoy_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            inject_outer_guard_else_decoy(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_common.h",
                "static ngx_inline ngx_int_t\nngx_http_modsecurity_add_n_response_header",
                "value_len, 1) != NGX_OK) {\n        return NGX_ERROR;",
                "value_len, 1) != NGX_OK) {\n        return NGX_OK;",
            )

        self._assert_rejected(
            mutate,
            "NGINX Server resolver preserves the bounded explicit-length response-header sink",
        )

    def test_mapper_rejection_is_bound_to_the_mapper_call(self) -> None:
        def mutate(repository: Path) -> None:
            path = repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_access.c"
            signature = "static ngx_int_t\nngx_http_modsecurity_validate_common_request_mapper"
            replace_in_function(
                path,
                signature,
                "mapper_error);\n        return NGX_HTTP_BAD_REQUEST;",
                "mapper_error);\n        return NGX_OK;",
            )
            replace_in_function(
                path,
                signature,
                "\n    return NGX_OK;\n}",
                "\n    if (r == NULL) {\n"
                "        return NGX_HTTP_BAD_REQUEST;\n"
                "    }\n\n"
                "    return NGX_OK;\n}",
            )

        self._assert_rejected(
            mutate,
            "NGINX request mapper validation fails closed before request-header initialization",
        )

    def test_unbraced_mapper_rejection_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            replace_in_function(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_access.c",
                "static ngx_int_t\nngx_http_modsecurity_validate_common_request_mapper",
                "    if (!ngx_http_modsecurity_map_request(r, &contract, &mapped_request,\n",
                "    if (r != NULL)\n"
                "        if (!ngx_http_modsecurity_map_request(r, &contract, &mapped_request,\n",
            )

        self._assert_rejected(
            mutate,
            "NGINX request mapper validation fails closed before request-header initialization",
        )

    def test_nested_initializer_propagation_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            replace_in_function(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_access.c",
                "static ngx_int_t\nngx_http_modsecurity_initialize_request",
                "    rc = ngx_http_modsecurity_validate_common_request_mapper(r);\n"
                "    if (rc != NGX_OK) {\n"
                "        ctx->intervention_triggered = 1;\n"
                "        return rc;\n"
                "    }",
                "    if (ctx->processed) {\n"
                "        rc = ngx_http_modsecurity_validate_common_request_mapper(r);\n"
                "        if (rc != NGX_OK) {\n"
                "            ctx->intervention_triggered = 1;\n"
                "            return rc;\n"
                "        }\n"
                "    }",
            )

        self._assert_rejected(
            mutate,
            "NGINX request mapper validation fails closed before request-header initialization",
        )

    def test_unbraced_initializer_propagation_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            replace_in_function(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_access.c",
                "static ngx_int_t\nngx_http_modsecurity_initialize_request",
                "    rc = ngx_http_modsecurity_validate_common_request_mapper(r);\n",
                "    if (ctx->processed)\n"
                "        rc = ngx_http_modsecurity_validate_common_request_mapper(r);\n",
            )

        self._assert_rejected(
            mutate,
            "NGINX request mapper validation fails closed before request-header initialization",
        )

    def test_nested_response_validation_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            replace_in_function(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_common.h",
                "static ngx_inline ngx_int_t\nngx_http_modsecurity_add_n_response_header",
                "    if (ngx_http_modsecurity_validate_header(ctx, name, name_len, value,\n"
                "            value_len, 1) != NGX_OK) {\n"
                "        return NGX_ERROR;\n"
                "    }",
                "    if (ctx->response_header_count > 0U) {\n"
                "        if (ngx_http_modsecurity_validate_header(ctx, name, name_len, value,\n"
                "                value_len, 1) != NGX_OK) {\n"
                "            return NGX_ERROR;\n"
                "        }\n"
                "    }",
            )

        self._assert_rejected(
            mutate,
            "NGINX Server resolver preserves the bounded explicit-length response-header sink",
        )

    def test_unbraced_response_validation_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            replace_in_function(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_common.h",
                "static ngx_inline ngx_int_t\nngx_http_modsecurity_add_n_response_header",
                "    if (ngx_http_modsecurity_validate_header(ctx, name, name_len, value,\n"
                "            value_len, 1) != NGX_OK) {\n"
                "        return NGX_ERROR;\n"
                "    }",
                "    if (ctx->response_header_count > 0U)\n"
                "        if (ngx_http_modsecurity_validate_header(ctx, name, name_len, value,\n"
                "                value_len, 1) != NGX_OK) {\n"
                "            return NGX_ERROR;\n"
                "        }",
            )

        self._assert_rejected(
            mutate,
            "NGINX Server resolver preserves the bounded explicit-length response-header sink",
        )

    def _replace_date_wrapper_with_raw_sink(
        self, repository: Path, raw_sink_name: str
    ) -> None:
        replace_in_function(
            repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_header_filter.c",
            "static ngx_int_t\nngx_http_modsecurity_resolv_header_date",
            "    return ngx_http_modsecurity_add_n_response_header(ctx,\n"
            "        (const unsigned char *) name.data,\n"
            "        name.len,\n"
            "        (const unsigned char *) date.data,\n"
            "        date.len);",
            "    return "
            + raw_sink_name
            + "(ctx->modsec_transaction,\n"
            "        (const unsigned char *) name.data,\n"
            "        name.len,\n"
            "        (const unsigned char *) date.data,\n"
            "        date.len) == 1 ? 1 : NGX_ERROR;",
        )

    def test_line_spliced_raw_response_sink_is_rejected(self) -> None:
        self._assert_rejected(
            lambda repository: self._replace_date_wrapper_with_raw_sink(
                repository, "msc_add_n_response_\\\nheader"
            ),
            "NGINX Server resolver preserves the bounded explicit-length response-header sink",
        )

    def test_ucn_raw_response_sink_is_rejected(self) -> None:
        self._assert_rejected(
            lambda repository: self._replace_date_wrapper_with_raw_sink(
                repository, "msc_add_n_response_\\u0068eader"
            ),
            "NGINX Server resolver preserves the bounded explicit-length response-header sink",
        )

    def test_alternate_common_wrapper_raw_sink_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            path = repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_common.h"
            signature = "static ngx_inline ngx_int_t\nngx_http_modsecurity_add_n_response_header"
            raw_return = (
                "    return msc_add_n_response_header(ctx->modsec_transaction, name, name_len,\n"
                "        value, value_len) == 1 ? 1 : NGX_ERROR;"
            )
            replace_in_function(
                path,
                signature,
                raw_return,
                "    if (name_len == 0U) {\n"
                "        return msc_add_n_response_header((ctx)->modsec_transaction, name, name_len,\n"
                "            value, value_len) == 1 ? 1 : NGX_ERROR;\n"
                "    }\n\n"
                + raw_return,
            )

        self._assert_rejected(
            mutate,
            "NGINX Server resolver preserves the bounded explicit-length response-header sink",
        )

    def test_macro_redefined_request_mapper_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            insert_before_signature(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_access.c",
                "static ngx_int_t\nngx_http_modsecurity_validate_common_request_mapper",
                "#define ngx_http_modsecurity_map_request(...) (1)",
            )

        self._assert_rejected(
            mutate,
            "NGINX request mapper validation fails closed before request-header initialization",
        )

    def test_diagnostic_macro_control_flow_mutation_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            path = repository / "connectors" / "nginx" / "src" / "ddebug.h"
            source = path.read_text(encoding="utf-8")
            old = "#define dd(...) do { \\\n"
            new = "#define dd(...) if (1) ; else \\\n"
            if source.count(old) != 1:
                raise AssertionError("expected one mutable diagnostic macro")
            path.write_text(source.replace(old, new, 1), encoding="utf-8")

        self._assert_rejected(
            mutate,
            "NGINX request mapper validation fails closed before request-header initialization",
        )

    def test_unapproved_local_macro_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            replace_in_function(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_access.c",
                "static ngx_int_t\nngx_http_modsecurity_validate_common_request_mapper",
                "    msconnector_request_mapper_contract_init(&contract);\n",
                "    msconnector_request_mapper_contract_init(&contract);\n"
                "#define r ((ngx_http_request_t *) 0)\n",
            )

        self._assert_rejected(
            mutate,
            "NGINX request mapper validation fails closed before request-header initialization",
        )

    def test_macro_redefined_initializer_validator_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            insert_before_signature(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_access.c",
                "static ngx_int_t\nngx_http_modsecurity_initialize_request",
                "#define ngx_http_modsecurity_validate_common_request_mapper(r) NGX_OK",
            )

        self._assert_rejected(
            mutate,
            "NGINX request mapper validation fails closed before request-header initialization",
        )

    def test_macro_redefined_bad_request_status_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            prepend_directive(
                repository / "connectors" / "nginx" / "src" / "ddebug.h",
                "#define NGX_HTTP_BAD_REQUEST NGX_OK",
            )

        self._assert_rejected(
            mutate,
            "NGINX request mapper validation fails closed before request-header initialization",
        )

    def test_macro_redefined_response_validator_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            insert_before_signature(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_common.h",
                "static ngx_inline ngx_int_t\nngx_http_modsecurity_add_n_response_header",
                "#define ngx_http_modsecurity_validate_header(...) NGX_OK",
            )

        self._assert_rejected(
            mutate,
            "NGINX Server resolver preserves the bounded explicit-length response-header sink",
        )

    def test_critical_macro_undefinition_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            insert_before_signature(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_access.c",
                "static ngx_int_t\nngx_http_modsecurity_validate_common_request_mapper",
                "#undef NGX_HTTP_BAD_REQUEST",
            )

        self._assert_rejected(
            mutate,
            "NGINX request mapper validation fails closed before request-header initialization",
        )

    def test_token_pasted_raw_response_sink_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            insert_before_signature(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_header_filter.c",
                "static ngx_int_t\nngx_http_modsecurity_resolv_header_date",
                "#define MSCONNECTOR_RAW_HEADER_SINK msc_add_n_response_ ## header",
            )
            self._replace_date_wrapper_with_raw_sink(
                repository, "MSCONNECTOR_RAW_HEADER_SINK"
            )

        self._assert_rejected(
            mutate,
            "NGINX Server resolver preserves the bounded explicit-length response-header sink",
        )

    def test_permitted_common_macro_raw_response_sink_alias_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            prepend_directive(
                repository / "common" / "include" / "msconnector" / "limits.h",
                "#define MSCONNECTOR_RAW_HEADER_SINK msc_add_n_response_header",
            )
            self._replace_date_wrapper_with_raw_sink(
                repository, "MSCONNECTOR_RAW_HEADER_SINK"
            )

        self._assert_rejected(
            mutate,
            "NGINX Server resolver preserves the bounded explicit-length response-header sink",
        )

    def test_early_macro_return_with_unreachable_raw_sink_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            path = (
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_common.h"
            )
            signature = (
                "static ngx_inline ngx_int_t\n"
                "ngx_http_modsecurity_add_n_response_header"
            )
            raw_return = (
                "    return msc_add_n_response_header(ctx->modsec_transaction, name, name_len,\n"
                "        value, value_len) == 1 ? 1 : NGX_ERROR;"
            )
            insert_before_signature(
                path,
                signature,
                "#define MSCONNECTOR_BYPASS(...) 1",
            )
            replace_in_function(
                path,
                signature,
                raw_return,
                "    return MSCONNECTOR_BYPASS(ctx->modsec_transaction, name, name_len,\n"
                "        value, value_len);\n\n"
                + raw_return,
            )

        self._assert_rejected(
            mutate,
            "NGINX Server resolver preserves the bounded explicit-length response-header sink",
        )

    def test_permitted_macro_parameterized_raw_sink_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            path = (
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_common.h"
            )
            signature = (
                "static ngx_inline ngx_int_t\n"
                "ngx_http_modsecurity_add_n_response_header"
            )
            raw_return = (
                "    return msc_add_n_response_header(ctx->modsec_transaction, name, name_len,\n"
                "        value, value_len) == 1 ? 1 : NGX_ERROR;"
            )
            insert_before_signature(
                path,
                signature,
                "#define MSCONNECTOR_RETURN_APPLIED(fn, args) return fn args",
            )
            replace_in_function(
                path,
                signature,
                raw_return,
                "    MSCONNECTOR_RETURN_APPLIED(msc_add_n_response_header,\n"
                "        (ctx->modsec_transaction, name, name_len, value, value_len));\n\n"
                + raw_return,
            )

        self._assert_rejected(
            mutate,
            "NGINX Server resolver preserves the bounded explicit-length response-header sink",
        )

    def test_permitted_macro_parameterized_prevalidation_sink_is_rejected(
        self,
    ) -> None:
        def mutate(repository: Path) -> None:
            path = (
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_common.h"
            )
            signature = (
                "static ngx_inline ngx_int_t\n"
                "ngx_http_modsecurity_add_n_response_header"
            )
            insert_before_signature(
                path,
                signature,
                "#define MSCONNECTOR_APPLY(fn, args) fn args",
            )
            replace_in_function(
                path,
                signature,
                "    if (ngx_http_modsecurity_validate_header(ctx, name, name_len, value,\n",
                "    MSCONNECTOR_APPLY(msc_add_n_response_header,\n"
                "        (ctx->modsec_transaction, name, name_len, value, value_len));\n\n"
                "    if (ngx_http_modsecurity_validate_header(ctx, name, name_len, value,\n",
            )

        self._assert_rejected(
            mutate,
            "NGINX Server resolver preserves the bounded explicit-length response-header sink",
        )

    def test_unscanned_local_include_extension_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            decoy = repository / "connectors" / "nginx" / "src" / "checker-decoy.inc"
            decoy.write_text(
                "#define r ((ngx_http_request_t *) 0)\n", encoding="utf-8"
            )
            insert_before_signature(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_access.c",
                "static ngx_int_t\nngx_http_modsecurity_validate_common_request_mapper",
                '#include "checker-decoy.inc"',
            )

        self._assert_rejected(
            mutate,
            "NGINX request mapper validation fails closed before request-header initialization",
        )

    def test_traversal_local_include_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            decoy = repository / "connectors" / "nginx" / "checker-decoy.h"
            decoy.write_text(
                "#define r ((ngx_http_request_t *) 0)\n", encoding="utf-8"
            )
            insert_before_signature(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_access.c",
                "static ngx_int_t\nngx_http_modsecurity_validate_common_request_mapper",
                '#include "../checker-decoy.h"',
            )

        self._assert_rejected(
            mutate,
            "NGINX request mapper validation fails closed before request-header initialization",
        )

    def test_unscanned_out_of_root_local_header_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            decoy = repository / "connectors" / "checker-decoy.h"
            decoy.write_text(
                "#define r ((ngx_http_request_t *) 0)\n", encoding="utf-8"
            )
            insert_before_signature(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_access.c",
                "static ngx_int_t\nngx_http_modsecurity_validate_common_request_mapper",
                '#include "connectors/checker-decoy.h"',
            )

        self._assert_rejected(
            mutate,
            "NGINX request mapper validation fails closed before request-header initialization",
        )

    def test_external_quoted_include_local_shadow_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            decoy = repository / "stdio.h"
            decoy.write_text(
                "#define NGX_HTTP_BAD_REQUEST NGX_OK\n", encoding="utf-8"
            )
            insert_before_signature(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_access.c",
                "static ngx_int_t\nngx_http_modsecurity_validate_common_request_mapper",
                '#include "stdio.h"',
            )

        self._assert_rejected(
            mutate,
            "NGINX request mapper validation fails closed before request-header initialization",
        )

    def test_unknown_angle_include_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            decoy = repository / "checker-decoy.inc"
            decoy.write_text(
                "#define NGX_HTTP_BAD_REQUEST NGX_OK\n", encoding="utf-8"
            )
            insert_before_signature(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_access.c",
                "static ngx_int_t\nngx_http_modsecurity_validate_common_request_mapper",
                "#include <checker-decoy.inc>",
            )

        self._assert_rejected(
            mutate,
            "NGINX request mapper validation fails closed before request-header initialization",
        )

    def test_include_next_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            insert_before_signature(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_access.c",
                "static ngx_int_t\nngx_http_modsecurity_validate_common_request_mapper",
                "#include_next <ngx_config.h>",
            )

        self._assert_rejected(
            mutate,
            "NGINX request mapper validation fails closed before request-header initialization",
        )

    def test_import_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            insert_before_signature(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_access.c",
                "static ngx_int_t\nngx_http_modsecurity_validate_common_request_mapper",
                "#import <ngx_config.h>",
            )

        self._assert_rejected(
            mutate,
            "NGINX request mapper validation fails closed before request-header initialization",
        )

    def test_external_angle_include_local_shadow_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            decoy = repository / "ngx_config.h"
            decoy.write_text(
                "#define NGX_HTTP_BAD_REQUEST NGX_OK\n", encoding="utf-8"
            )

        self._assert_rejected(
            mutate,
            "NGINX request mapper validation fails closed before request-header initialization",
        )

    def test_macro_expanded_local_include_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            decoy = repository / "connectors" / "nginx" / "src" / "checker-decoy.inc"
            decoy.write_text(
                "#define r ((ngx_http_request_t *) 0)\n", encoding="utf-8"
            )
            insert_before_signature(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_access.c",
                "static ngx_int_t\nngx_http_modsecurity_validate_common_request_mapper",
                '#define MSCONNECTOR_CHECKER_DECOY "checker-decoy.inc"\n'
                "#include MSCONNECTOR_CHECKER_DECOY",
            )

        self._assert_rejected(
            mutate,
            "NGINX request mapper validation fails closed before request-header initialization",
        )


if __name__ == "__main__":
    unittest.main()
