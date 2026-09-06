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


def replace_all_in_function(
    path: Path, signature: str, old: str, new: str, expected_count: int
) -> None:
    """Replace every expected instance of a fragment in one function."""
    source = path.read_text(encoding="utf-8")
    start, end = function_bounds(source, signature)
    original = source[start:end]
    if original.count(old) != expected_count:
        raise AssertionError(
            f"expected {expected_count} mutable fragments in {path}: {old!r}"
        )
    path.write_text(
        source[:start] + original.replace(old, new) + source[end:],
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

    def test_comment_brace_cannot_hide_response_mapper_lifecycle_call(self) -> None:
        def mutate(repository: Path) -> None:
            path = (
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_mapper.c"
            )
            replace_in_function(
                path,
                "void\nngx_http_modsecurity_validate_response_mapper",
                "    ngx_log_error(NGX_LOG_WARN, r->connection->log, 0,\n"
                "        \"modsecurity common response mapper validation skipped: %s\", mapper_error);\n"
                "}",
                "    ngx_log_error(NGX_LOG_WARN, r->connection->log, 0,\n"
                "        \"modsecurity common response mapper validation skipped: %s\", mapper_error);\n"
                "    /* } */\n"
                "    ngx_http_filter_finalize_request(r, &ngx_http_modsecurity_module,\n"
                "        NGX_ERROR);\n"
                "}",
            )

        self._assert_rejected(
            mutate,
            "NGINX response mapper helper excludes caller lifecycle, body, enforcement, filter-chain, and allocation control",
        )

    def test_string_brace_cannot_hide_response_mapper_lifecycle_call(self) -> None:
        def mutate(repository: Path) -> None:
            path = (
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_mapper.c"
            )
            replace_in_function(
                path,
                "void\nngx_http_modsecurity_validate_response_mapper",
                "    ngx_log_error(NGX_LOG_WARN, r->connection->log, 0,\n"
                "        \"modsecurity common response mapper validation skipped: %s\", mapper_error);\n"
                "}",
                "    ngx_log_error(NGX_LOG_WARN, r->connection->log, 0,\n"
                "        \"modsecurity common response mapper validation skipped: %s\", mapper_error);\n"
                "    ngx_log_error(NGX_LOG_WARN, r->connection->log, 0, \"}\");\n"
                "    ngx_http_filter_finalize_request(r, &ngx_http_modsecurity_module,\n"
                "        NGX_ERROR);\n"
                "}",
            )

        self._assert_rejected(
            mutate,
            "NGINX response mapper helper excludes caller lifecycle, body, enforcement, filter-chain, and allocation control",
        )

    def test_comment_brace_cannot_hide_unbounded_response_body_append(self) -> None:
        def mutate(repository: Path) -> None:
            path = (
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_body_filter.c"
            )
            replace_in_function(
                path,
                "static ngx_int_t\nngx_http_modsecurity_append_response_chain_buffer",
                "    return ngx_http_modsecurity_append_response_body_buffer(r, ctx, mcf,\n"
                "        chain->buf);",
                "    /* return ngx_http_modsecurity_append_response_body_buffer(r, ctx, mcf,\n"
                "        chain->buf); */\n"
                "    /* } */\n"
                "    return ngx_http_modsecurity_append_response_body_chunk(ctx,\n"
                "        chain->buf->pos,\n"
                "        (size_t)(chain->buf->last - chain->buf->pos));",
            )

        self._assert_rejected(
            mutate,
            "NGINX records seen bytes through the Common plan only after the in-scope gate",
        )

    def test_inactive_brace_cannot_hide_unbounded_response_body_append(self) -> None:
        def mutate(repository: Path) -> None:
            path = (
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_body_filter.c"
            )
            replace_in_function(
                path,
                "static ngx_int_t\nngx_http_modsecurity_append_response_chain_buffer",
                "    return ngx_http_modsecurity_append_response_body_buffer(r, ctx, mcf,\n"
                "        chain->buf);",
                "#if 0\n"
                "    return ngx_http_modsecurity_append_response_body_buffer(r, ctx, mcf,\n"
                "        chain->buf);\n"
                "}\n"
                "#endif\n"
                "    return ngx_http_modsecurity_append_response_body_chunk(ctx,\n"
                "        chain->buf->pos,\n"
                "        (size_t)(chain->buf->last - chain->buf->pos));",
            )

        self._assert_rejected(
            mutate,
            "NGINX records seen bytes through the Common plan only after the in-scope gate",
        )

    def test_active_conditional_cannot_hide_response_mapper_lifecycle_call(self) -> None:
        def mutate(repository: Path) -> None:
            replace_in_function(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_mapper.c",
                "void\nngx_http_modsecurity_validate_response_mapper",
                "    ngx_log_error(NGX_LOG_WARN, r->connection->log, 0,\n"
                "        \"modsecurity common response mapper validation skipped: %s\", mapper_error);\n"
                "}",
                "    ngx_log_error(NGX_LOG_WARN, r->connection->log, 0,\n"
                "        \"modsecurity common response mapper validation skipped: %s\", mapper_error);\n"
                "#if 1\n"
                "    ngx_http_filter_finalize_request(r, &ngx_http_modsecurity_module, NGX_ERROR);\n"
                "#endif\n"
                "}",
            )

        self._assert_rejected(
            mutate,
            "NGINX response mapper helper excludes caller lifecycle, body, enforcement, filter-chain, and allocation control",
        )

    def test_each_direct_response_body_append_route_before_gate_is_rejected(
        self,
    ) -> None:
        cases = (
            (
                "buffer wrapper",
                "    return ngx_http_modsecurity_append_response_body_buffer(r, ctx, mcf,\n"
                "        chain->buf);\n\n",
            ),
            (
                "limited body wrapper",
                "    return ngx_http_modsecurity_append_limited_response_body(ctx, mcf,\n"
                "        chain->buf->pos,\n"
                "        (size_t)(chain->buf->last - chain->buf->pos));\n\n",
            ),
            (
                "file body wrapper",
                "    return ngx_http_modsecurity_append_file_response_body(r, ctx, mcf,\n"
                "        chain->buf);\n\n",
            ),
            (
                "bounded chunk helper",
                "    return ngx_http_modsecurity_append_response_body_chunk(ctx,\n"
                "        chain->buf->pos,\n"
                "        (size_t)(chain->buf->last - chain->buf->pos));\n\n",
            ),
            (
                "raw ModSecurity append",
                "    return msc_append_response_body(ctx->modsec_transaction,\n"
                "        chain->buf->pos,\n"
                "        (size_t)(chain->buf->last - chain->buf->pos));\n\n",
            ),
        )
        path_name = "ngx_http_modsecurity_body_filter.c"
        signature = (
            "static ngx_int_t\n"
            "ngx_http_modsecurity_append_response_chain_buffer"
        )

        for name, invocation in cases:
            with self.subTest(route=name):
                def mutate(
                    repository: Path,
                    invocation: str = invocation,
                ) -> None:
                    replace_in_function(
                        repository / "connectors" / "nginx" / "src" / path_name,
                        signature,
                        "    if (phase4_in_scope == 0) {",
                        invocation + "    if (phase4_in_scope == 0) {",
                    )

                self._assert_rejected(
                    mutate,
                    "NGINX records seen bytes through the Common plan only after the in-scope gate",
                )

    def test_any_pre_gate_helper_call_is_rejected(self) -> None:
        cases = (
            (
                "response-body helper",
                "    return ngx_http_modsecurity_append_response_body_buffer(r, ctx, mcf,\n"
                "        buffer);\n",
                "ngx_http_modsecurity_pre_gate_helper",
            ),
            (
                "harmless helper",
                "    return NGX_OK;\n",
                "ngx_http_modsecurity_pre_gate_helper",
            ),
            (
                "object macro helper alias",
                "    return NGX_OK;\n",
                "MSCONNECTOR_PRE_GATE_HELPER",
            ),
        )
        path_name = "ngx_http_modsecurity_body_filter.c"
        signature = (
            "static ngx_int_t\n"
            "ngx_http_modsecurity_append_response_chain_buffer"
        )
        helper_signature = (
            "static ngx_int_t\n"
            "ngx_http_modsecurity_pre_gate_helper(ngx_http_request_t *r,\n"
            "    ngx_http_modsecurity_ctx_t *ctx, ngx_http_modsecurity_conf_t *mcf,\n"
            "    ngx_buf_t *buffer)\n"
        )

        for name, helper_body, invocation_name in cases:
            with self.subTest(helper=name):
                def mutate(
                    repository: Path,
                    helper_body: str = helper_body,
                    invocation_name: str = invocation_name,
                ) -> None:
                    path = repository / "connectors" / "nginx" / "src" / path_name
                    insert_before_signature(
                        path,
                        signature,
                        helper_signature + "{\n" + helper_body + "}",
                    )
                    if invocation_name == "MSCONNECTOR_PRE_GATE_HELPER":
                        insert_before_signature(
                            path,
                            signature,
                            "#define MSCONNECTOR_PRE_GATE_HELPER "
                            "ngx_http_modsecurity_pre_gate_helper",
                        )
                    replace_in_function(
                        path,
                        signature,
                        "    if (phase4_in_scope == 0) {",
                        "    return " + invocation_name
                        + "(r, ctx, mcf, chain->buf);\n\n"
                        + "    if (phase4_in_scope == 0) {",
                    )

                self._assert_rejected(
                    mutate,
                    "NGINX records seen bytes through the Common plan only after the in-scope gate",
                )

    def test_active_conditional_direct_response_body_append_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            replace_in_function(
                repository / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_body_filter.c",
                "static ngx_int_t\nngx_http_modsecurity_append_response_chain_buffer",
                "    if (phase4_in_scope == 0) {",
                "#if 1\n"
                "    return ngx_http_modsecurity_append_response_body_chunk(ctx,\n"
                "        chain->buf->pos,\n"
                "        (size_t)(chain->buf->last - chain->buf->pos));\n"
                "#endif\n\n"
                "    if (phase4_in_scope == 0) {",
            )

        self._assert_rejected(
            mutate,
            "NGINX records seen bytes through the Common plan only after the in-scope gate",
        )

    def test_object_macro_alias_of_each_response_mapper_marker_is_rejected(
        self,
    ) -> None:
        default_use = "    MSCONNECTOR_FORBIDDEN_MAPPER_ALIAS;\n"
        cases = (
            ("response validation", "ctx->common_response_validated", default_use),
            ("processed state", "ctx->processed", default_use),
            ("intervention state", "ctx->intervention_triggered", default_use),
            ("phase4 state", "ctx->phase4_processed", default_use),
            ("response-body state", "ctx->response_body_bytes_seen", default_use),
            ("response-commit state", "ctx->response_committed", default_use),
            ("response-header processing", "msc_process_response_headers", default_use),
            ("response-body processing", "msc_process_response_body", default_use),
            ("raw response-header sink", "msc_add_n_response_header", default_use),
            ("next-filter chain", "ngx_http_next_header_filter", default_use),
            (
                "request finalizer",
                "ngx_http_filter_finalize_request",
                "    MSCONNECTOR_FORBIDDEN_MAPPER_ALIAS(r,\n"
                "        &ngx_http_modsecurity_module, 0);\n",
            ),
            ("pool allocation", "ngx_palloc", default_use),
            ("nonzeroing pool allocation", "ngx_pnalloc", default_use),
            ("zeroing pool allocation", "ngx_pcalloc", default_use),
        )
        path_name = "ngx_http_modsecurity_mapper.c"
        signature = "void\nngx_http_modsecurity_validate_response_mapper"
        warning = (
            "    ngx_log_error(NGX_LOG_WARN, r->connection->log, 0,\n"
            "        \"modsecurity common response mapper validation skipped: %s\", mapper_error);\n"
        )

        for name, replacement, use in cases:
            with self.subTest(marker=name):
                def mutate(
                    repository: Path,
                    replacement: str = replacement,
                    use: str = use,
                ) -> None:
                    path = repository / "connectors" / "nginx" / "src" / path_name
                    insert_before_signature(
                        path,
                        signature,
                        "#define MSCONNECTOR_FORBIDDEN_MAPPER_ALIAS " + replacement,
                    )
                    replace_in_function(
                        path,
                        signature,
                        warning,
                        warning + use,
                    )

                self._assert_rejected(
                    mutate,
                    "NGINX critical macro inputs reject aliases of checked lifecycle and response-body controls",
                )

    def test_object_macro_alias_of_each_pre_gate_response_body_append_route_is_rejected(
        self,
    ) -> None:
        cases = (
            (
                "buffer wrapper",
                "ngx_http_modsecurity_append_response_body_buffer",
                "    MSCONNECTOR_FORBIDDEN_BODY_ALIAS(r, ctx, mcf, chain->buf);\n\n",
            ),
            (
                "limited body wrapper",
                "ngx_http_modsecurity_append_limited_response_body",
                "    MSCONNECTOR_FORBIDDEN_BODY_ALIAS(ctx, mcf, chain->buf->pos,\n"
                "        (size_t)(chain->buf->last - chain->buf->pos));\n\n",
            ),
            (
                "file body wrapper",
                "ngx_http_modsecurity_append_file_response_body",
                "    MSCONNECTOR_FORBIDDEN_BODY_ALIAS(r, ctx, mcf, chain->buf);\n\n",
            ),
            (
                "bounded chunk helper",
                "ngx_http_modsecurity_append_response_body_chunk",
                "    MSCONNECTOR_FORBIDDEN_BODY_ALIAS(ctx, chain->buf->pos,\n"
                "        (size_t)(chain->buf->last - chain->buf->pos));\n\n",
            ),
            (
                "raw ModSecurity append",
                "msc_append_response_body",
                "    MSCONNECTOR_FORBIDDEN_BODY_ALIAS(ctx->modsec_transaction,\n"
                "        chain->buf->pos,\n"
                "        (size_t)(chain->buf->last - chain->buf->pos));\n\n",
            ),
        )
        path_name = "ngx_http_modsecurity_body_filter.c"
        signature = (
            "static ngx_int_t\n"
            "ngx_http_modsecurity_append_response_chain_buffer"
        )

        for name, replacement, invocation in cases:
            with self.subTest(marker=name):
                def mutate(
                    repository: Path,
                    replacement: str = replacement,
                    invocation: str = invocation,
                ) -> None:
                    path = repository / "connectors" / "nginx" / "src" / path_name
                    insert_before_signature(
                        path,
                        signature,
                        "#define MSCONNECTOR_FORBIDDEN_BODY_ALIAS " + replacement,
                    )
                    replace_in_function(
                        path,
                        signature,
                        "    if (phase4_in_scope == 0) {",
                        invocation + "    if (phase4_in_scope == 0) {",
                    )

                self._assert_rejected(
                    mutate,
                    "NGINX critical macro inputs reject aliases of checked lifecycle and response-body controls",
                )

    def test_chained_object_macro_alias_to_direct_response_body_append_is_rejected(
        self,
    ) -> None:
        def mutate(repository: Path) -> None:
            path = (
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_body_filter.c"
            )
            signature = (
                "static ngx_int_t\n"
                "ngx_http_modsecurity_append_response_chain_buffer"
            )
            insert_before_signature(
                path,
                signature,
                "#define MSCONNECTOR_FORBIDDEN_BODY_ALIAS "
                "MSCONNECTOR_FORBIDDEN_BODY_TERMINAL\n"
                "#define MSCONNECTOR_FORBIDDEN_BODY_TERMINAL "
                "msc_append_response_body",
            )
            replace_in_function(
                path,
                signature,
                "    if (phase4_in_scope == 0) {",
                "    MSCONNECTOR_FORBIDDEN_BODY_ALIAS(ctx->modsec_transaction,\n"
                "        chain->buf->pos,\n"
                "        (size_t)(chain->buf->last - chain->buf->pos));\n\n"
                "    if (phase4_in_scope == 0) {",
            )

        self._assert_rejected(
            mutate,
            "NGINX critical macro inputs reject aliases of checked lifecycle and response-body controls",
        )

    def test_harmless_object_macro_remains_accepted(self) -> None:
        def mutate(repository: Path) -> None:
            insert_before_signature(
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_mapper.c",
                "void\nngx_http_modsecurity_validate_response_mapper",
                "#define MSCONNECTOR_HARMLESS_ALIAS 1U",
            )

        result = self._run_checker(mutate)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(
            "PASS: NGINX critical macro inputs reject aliases of checked lifecycle and response-body controls",
            result.stdout,
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

    def test_string_literal_phase4_scope_assignment_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            replace_in_function(
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_body_filter.c",
                "static ngx_int_t\nngx_http_modsecurity_process_response_body_chain",
                "    phase4_in_scope = ngx_http_modsecurity_phase4_in_scope(r);\n",
                "    phase4_in_scope = r->main != NULL ? 1 : 0;\n"
                "    (void) \"phase4_in_scope = "
                "ngx_http_modsecurity_phase4_in_scope(r)\";\n",
            )

        self._assert_rejected(
            mutate,
            "NGINX records seen bytes through the Common plan only after the in-scope gate",
        )

    def test_string_literal_body_limit_accounting_is_rejected(self) -> None:
        def mutate(repository: Path) -> None:
            path = (
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_body_filter.c"
            )
            signature = (
                "static ngx_int_t\n"
                "ngx_http_modsecurity_plan_limited_response_body"
            )
            replace_all_in_function(
                path,
                signature,
                "ctx->response_body_bytes_seen = plan.bytes_seen;",
                "ctx->response_body_bytes_seen = 0U;",
                2,
            )
            replace_in_function(
                path,
                signature,
                "    *allowed = plan.append_size;\n",
                "    (void) \"ctx->response_body_bytes_seen = "
                "plan.bytes_seen;\";\n"
                "    *allowed = plan.append_size;\n",
            )

        self._assert_rejected(
            mutate,
            "NGINX records seen bytes through the Common plan only after the in-scope gate",
        )

    def test_unreachable_body_response_mapper_calls_are_rejected(self) -> None:
        call = (
            "    ngx_http_modsecurity_validate_response_mapper(ctx, r,\n"
            "        NGX_HTTP_MODSECURITY_RESPONSE_MAPPER_DIAGNOSTIC_BODY);\n"
        )
        cases = (
            ("braced if zero", "    if (0) {\n" + "    " + call + "    }\n"),
            ("unbraced if zero", "    if (0)\n" + "    " + call),
            ("preprocessor if one", "#if 1\n" + call + "#endif\n"),
        )

        for name, replacement in cases:
            with self.subTest(wrapper=name):
                def mutate(
                    repository: Path, replacement: str = replacement
                ) -> None:
                    replace_in_function(
                        repository
                        / "connectors"
                        / "nginx"
                        / "src"
                        / "ngx_http_modsecurity_body_filter.c",
                        "static ngx_int_t\n"
                        "ngx_http_modsecurity_validate_response_mapper_once",
                        call,
                        replacement,
                    )

                self._assert_rejected(
                    mutate,
                    "NGINX body mapper validation remains once-only, post-guard, and non-fatal",
                )

    def test_unreachable_header_response_mapper_calls_are_rejected(self) -> None:
        call = (
            "    ngx_http_modsecurity_validate_response_mapper(ctx, r,\n"
            "        NGX_HTTP_MODSECURITY_RESPONSE_MAPPER_DIAGNOSTIC_HEADER);\n"
        )
        cases = (
            ("braced if zero", "    if (0) {\n" + "    " + call + "    }\n"),
            ("unbraced if zero", "    if (0)\n" + "    " + call),
            ("preprocessor if one", "#if 1\n" + call + "#endif\n"),
        )

        for name, replacement in cases:
            with self.subTest(wrapper=name):
                def mutate(
                    repository: Path, replacement: str = replacement
                ) -> None:
                    replace_in_function(
                        repository
                        / "connectors"
                        / "nginx"
                        / "src"
                        / "ngx_http_modsecurity_header_filter.c",
                        "ngx_int_t\n"
                        "ngx_http_modsecurity_header_filter(ngx_http_request_t *r)\n{",
                        call,
                        replacement,
                    )

                self._assert_rejected(
                    mutate,
                    "NGINX header mapper validation retains its existing eligibility and ordering without a once gate",
                )

    def test_preprocessor_early_return_before_body_mapper_is_rejected(self) -> None:
        guard = (
            "    if (ctx->common_response_validated) {\n"
            "        return NGX_OK;\n"
            "    }\n\n"
        )

        def mutate(repository: Path) -> None:
            replace_in_function(
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_body_filter.c",
                "static ngx_int_t\n"
                "ngx_http_modsecurity_validate_response_mapper_once",
                guard,
                guard + "#if 1\n    return NGX_OK;\n#endif\n\n",
            )

        self._assert_rejected(
            mutate,
            "NGINX body mapper validation remains once-only, post-guard, and non-fatal",
        )

    def test_early_return_before_header_mapper_is_rejected(self) -> None:
        guard = (
            "    if (ctx->intervention_triggered) {\n"
            "        return ngx_http_next_header_filter(r);\n"
            "    }\n\n"
        )
        cases = (
            (
                "preprocessor",
                "#if 1\n    return ngx_http_next_header_filter(r);\n#endif\n\n",
            ),
            (
                "structured conditional",
                "    if (1) {\n"
                "        return ngx_http_next_header_filter(r);\n"
                "    }\n\n",
            ),
        )

        for name, insertion in cases:
            with self.subTest(wrapper=name):
                def mutate(
                    repository: Path, insertion: str = insertion
                ) -> None:
                    replace_in_function(
                        repository
                        / "connectors"
                        / "nginx"
                        / "src"
                        / "ngx_http_modsecurity_header_filter.c",
                        "ngx_int_t\n"
                        "ngx_http_modsecurity_header_filter(ngx_http_request_t *r)\n{",
                        guard,
                        guard + insertion,
                    )

                self._assert_rejected(
                    mutate,
                    "NGINX header mapper validation retains its existing eligibility and ordering without a once gate",
                )

    def test_pre_guard_header_mapper_bypasses_are_rejected(self) -> None:
        context_acquisition = (
            "    ctx = ngx_http_modsecurity_get_module_ctx(r);\n"
        )
        diagnostic = "    dd(\"header filter, recovering ctx: %p\", ctx);\n"
        anchor = context_acquisition + "\n" + diagnostic
        cases = (
            (
                "direct context lookup state mutation before acquisition",
                "    ngx_http_modsecurity_get_module_ctx(r)->"
                "intervention_triggered = 1;\n"
                + context_acquisition
                + "\n"
                + diagnostic,
            ),
            (
                "diagnostic argument intervention-state mutation",
                context_acquisition
                + "\n"
                + "    dd(\"header filter, recovering ctx: %p\", "
                + "(ctx->intervention_triggered = 1, ctx));\n",
            ),
            (
                "diagnostic argument context null assignment",
                context_acquisition
                + "\n"
                + "    dd(\"header filter, recovering ctx: %p\", "
                + "(ctx = NULL));\n",
            ),
            (
                "intervention-state mutation",
                context_acquisition
                + "    ctx->intervention_triggered = 1;\n\n"
                + diagnostic,
            ),
            (
                "context null assignment",
                context_acquisition + "    ctx = NULL;\n\n" + diagnostic,
            ),
            (
                "compound early return after context acquisition",
                context_acquisition
                + "    {\n"
                + "        return ngx_http_next_header_filter(r);\n"
                + "    }\n\n"
                + diagnostic,
            ),
            (
                "compound early return before context acquisition",
                "    {\n"
                + "        return ngx_http_next_header_filter(r);\n"
                + "    }\n"
                + context_acquisition
                + "\n"
                + diagnostic,
            ),
        )

        for name, replacement in cases:
            with self.subTest(bypass=name):
                def mutate(
                    repository: Path, replacement: str = replacement
                ) -> None:
                    replace_in_function(
                        repository
                        / "connectors"
                        / "nginx"
                        / "src"
                        / "ngx_http_modsecurity_header_filter.c",
                        "ngx_int_t\n"
                        "ngx_http_modsecurity_header_filter(ngx_http_request_t *r)\n{",
                        anchor,
                        replacement,
                    )

                self._assert_rejected(
                    mutate,
                    "NGINX header mapper validation retains its existing eligibility and ordering without a once gate",
                )

    def test_diagnostic_macro_side_effect_is_rejected(self) -> None:
        macro_path_name = "ddebug.h"
        original_macro = (
            "#define dd(...) do { \\\n"
            "    fprintf(stderr, \"modsec *** %s: \", __func__); \\\n"
            "    fprintf(stderr, __VA_ARGS__); \\\n"
            "    fprintf(stderr, \" at %s line %d.\\n\", __FILE__, __LINE__); \\\n"
            "} while (0)"
        )
        replacement_macro = (
            "#define dd(...) do { "
            "msconnector_header_debug_bypass(__VA_ARGS__); "
            "} while (0)"
        )
        object_like_redirect_macro = (
            "#define dd msconnector_header_debug_bypass"
        )
        noncall_side_effect_macro = (
            "#define dd(...) do { \\\n"
            "    *((volatile unsigned char *)0) = 1U; \\\n"
            "    fprintf(stderr, \"modsec *** %s: \", __func__); \\\n"
            "    fprintf(stderr, __VA_ARGS__); \\\n"
            "    fprintf(stderr, \" at %s line %d.\\n\", __FILE__, __LINE__); \\\n"
            "} while (0)"
        )
        helper = (
            "static void\n"
            "msconnector_header_debug_bypass(const char *format,\n"
            "    ngx_http_modsecurity_ctx_t *ctx)\n"
            "{\n"
            "    (void)format;\n"
            "    ctx->intervention_triggered = 1;\n"
            "}\n\n"
        )
        signature = (
            "ngx_int_t\n"
            "ngx_http_modsecurity_header_filter(ngx_http_request_t *r)\n{"
        )

        cases = (
            ("helper call", replacement_macro, helper),
            ("object-like diagnostic redirect", object_like_redirect_macro, helper),
            ("direct non-call side effect", noncall_side_effect_macro, ""),
        )

        for name, replacement, source_helper in cases:
            with self.subTest(side_effect=name):
                def mutate(
                    repository: Path,
                    replacement: str = replacement,
                    source_helper: str = source_helper,
                ) -> None:
                    macro_path = (
                        repository
                        / "connectors"
                        / "nginx"
                        / "src"
                        / macro_path_name
                    )
                    macro_source = macro_path.read_text(encoding="utf-8")
                    if macro_source.count(original_macro) != 1:
                        raise AssertionError(
                            "expected one mutable dd macro definition"
                        )
                    macro_path.write_text(
                        macro_source.replace(original_macro, replacement, 1),
                        encoding="utf-8",
                    )
                    if source_helper:
                        insert_before_signature(
                            repository
                            / "connectors"
                            / "nginx"
                            / "src"
                            / "ngx_http_modsecurity_header_filter.c",
                            signature,
                            source_helper,
                        )

                self._assert_rejected(
                    mutate,
                    "NGINX critical macro inputs reject aliases of checked lifecycle and response-body controls",
                )

    def test_nonvariadic_diagnostic_fallback_side_effect_is_rejected(self) -> None:
        original_fallback = (
            "static void dd(const char *fmt, ...) {\n"
            "    (void)fmt;\n"
            "}"
        )
        mutated_fallback = (
            "static void dd(const char *fmt, ...) {\n"
            "    va_list arguments;\n"
            "    va_start(arguments, fmt);\n"
            "    *(volatile unsigned char *)va_arg(arguments, void *) = 0U;\n"
            "    va_end(arguments);\n"
            "}"
        )

        def mutate(repository: Path) -> None:
            path = repository / "connectors" / "nginx" / "src" / "ddebug.h"
            source = path.read_text(encoding="utf-8")
            if source.count(original_fallback) != 2:
                raise AssertionError("expected two inert static dd fallbacks")
            path.write_text(
                source.replace(original_fallback, mutated_fallback, 1),
                encoding="utf-8",
            )

        self._assert_rejected(
            mutate,
            "NGINX nonvariadic diagnostic fallbacks remain inert and bounded",
        )

    def test_additional_conditional_diagnostic_fallback_is_rejected(self) -> None:
        original_nondebug_fallback = (
            "#if (NGX_HAVE_VARIADIC_MACROS)\n"
            "#define dd(...)\n"
            "#else\n"
            "static void dd(const char *fmt, ...) {\n"
            "    (void)fmt;\n"
            "}\n"
            "#endif"
        )
        alternate_nondebug_fallback = (
            "#if (NGX_HAVE_VARIADIC_MACROS)\n"
            "#define dd(...)\n"
            "#elif 1\n"
            "static void dd(const char *fmt, ...) {\n"
            "    (void)fmt;\n"
            "    *((volatile unsigned char *)0) = 1U;\n"
            "}\n"
            "#else\n"
            "static void dd(const char *fmt, ...) {\n"
            "    (void)fmt;\n"
            "}\n"
            "#endif"
        )

        def mutate(repository: Path) -> None:
            path = repository / "connectors" / "nginx" / "src" / "ddebug.h"
            source = path.read_text(encoding="utf-8")
            if source.count(original_nondebug_fallback) != 1:
                raise AssertionError("expected one mutable nondebug dd fallback")
            path.write_text(
                source.replace(
                    original_nondebug_fallback, alternate_nondebug_fallback, 1
                ),
                encoding="utf-8",
            )

        self._assert_rejected(
            mutate,
            "NGINX nonvariadic diagnostic fallbacks remain inert and bounded",
        )

    def test_object_like_pcre_allocator_macro_is_rejected(self) -> None:
        cases = (
            (
                "init",
                "#define ngx_http_modsecurity_pcre_malloc_init(x) NULL",
                "#define ngx_http_modsecurity_pcre_malloc_init "
                "((ngx_pool_t *(*)(ngx_pool_t *))0)",
            ),
            (
                "done",
                "#define ngx_http_modsecurity_pcre_malloc_done(x) (void)x",
                "#define ngx_http_modsecurity_pcre_malloc_done "
                "((void (*)(ngx_pool_t *))0)",
            ),
        )

        for name, original, replacement in cases:
            with self.subTest(macro=name):
                def mutate(
                    repository: Path,
                    original: str = original,
                    replacement: str = replacement,
                ) -> None:
                    path = (
                        repository
                        / "connectors"
                        / "nginx"
                        / "src"
                        / "ngx_http_modsecurity_common.h"
                    )
                    source = path.read_text(encoding="utf-8")
                    if source.count(original) != 1:
                        raise AssertionError(
                            "expected one mutable PCRE allocator macro"
                        )
                    path.write_text(
                        source.replace(original, replacement, 1),
                        encoding="utf-8",
                    )

                self._assert_rejected(
                    mutate,
                    "NGINX critical macro inputs reject aliases of checked lifecycle and response-body controls",
                )

    def test_response_body_chain_requires_direct_bounded_wrapper(self) -> None:
        wrapper_call = (
            "        ret = ngx_http_modsecurity_append_response_chain_buffer(r, ctx, mcf,\n"
            "            phase4_in_scope, chain);\n"
        )

        def mutate(repository: Path) -> None:
            replace_in_function(
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_body_filter.c",
                "static ngx_int_t\n"
                "ngx_http_modsecurity_process_response_body_chain",
                wrapper_call,
                "        ret = NGX_OK;\n",
            )

        self._assert_rejected(
            mutate,
            "NGINX response-body chain loop directly calls the reviewed bounded wrapper",
        )

    def test_response_body_raw_sink_outside_bounded_helper_is_rejected(self) -> None:
        wrapper_call = (
            "        ret = ngx_http_modsecurity_append_response_chain_buffer(r, ctx, mcf,\n"
            "            phase4_in_scope, chain);\n"
        )
        raw_helper = (
            "static ngx_int_t\n"
            "msconnector_unchecked_response_body(ngx_http_modsecurity_ctx_t *ctx,\n"
            "    const u_char *data, size_t amount)\n"
            "{\n"
            "    return msc_append_response_body(ctx->modsec_transaction, data, amount) < 0\n"
            "        ? NGX_ERROR : NGX_OK;\n"
            "}\n\n"
        )

        def mutate(repository: Path) -> None:
            path = (
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_body_filter.c"
            )
            insert_before_signature(
                path,
                "static ngx_int_t\n"
                "ngx_http_modsecurity_process_response_body_chain",
                raw_helper,
            )
            replace_in_function(
                path,
                "static ngx_int_t\n"
                "ngx_http_modsecurity_process_response_body_chain",
                wrapper_call,
                "        ret = msconnector_unchecked_response_body(ctx,\n"
                "            chain->buf->pos, (size_t)(chain->buf->last - chain->buf->pos));\n",
            )

        self._assert_rejected(
            mutate,
            "NGINX response-body raw sink remains owned by the bounded append helper",
        )

    def test_header_filter_requires_response_header_collection(self) -> None:
        collection_call = (
            "    if (ngx_http_modsecurity_add_response_headers(r, ctx) != NGX_OK) {\n"
        )

        def mutate(repository: Path) -> None:
            replace_in_function(
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_header_filter.c",
                "ngx_int_t\n"
                "ngx_http_modsecurity_header_filter(ngx_http_request_t *r)\n{",
                collection_call,
                "    if (NGX_OK != NGX_OK) {\n",
            )

        self._assert_rejected(
            mutate,
            "NGINX header filter directly collects validated response headers before metadata processing",
        )

    def test_response_header_collection_uses_validated_wrapper(self) -> None:
        wrapper_call = "        if (ngx_http_modsecurity_add_n_response_header(ctx,\n"

        def mutate(repository: Path) -> None:
            replace_in_function(
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_header_filter.c",
                "static ngx_int_t\n"
                "ngx_http_modsecurity_add_response_headers",
                wrapper_call,
                "        if (NGX_OK != NGX_OK) {\n",
            )

        self._assert_rejected(
            mutate,
            "NGINX response-header collection retains the reviewed validated wrapper surface",
        )

    def test_response_header_collection_keeps_synthetic_resolver_loop(self) -> None:
        resolver_loop = (
            "    for (i = 0; ngx_http_modsecurity_headers_out[i].name.len; i++) {\n"
        )

        def mutate(repository: Path) -> None:
            replace_in_function(
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_header_filter.c",
                "static ngx_int_t\n"
                "ngx_http_modsecurity_add_response_headers",
                resolver_loop,
                "    for (i = 0; 0; i++) {\n",
            )

        self._assert_rejected(
            mutate,
            "NGINX response-header collection retains the reviewed synthetic and chained traversal",
        )

    def test_response_header_raw_sink_outside_common_wrapper_is_rejected(self) -> None:
        raw_helper = (
            "static ngx_inline ngx_int_t\n"
            "msconnector_unchecked_response_header(ngx_http_modsecurity_ctx_t *ctx,\n"
            "    const u_char *name, size_t name_len, const u_char *value, size_t value_len)\n"
            "{\n"
            "    return msc_add_n_response_header(ctx->modsec_transaction, name, name_len,\n"
            "        value, value_len);\n"
            "}\n\n"
        )

        def mutate(repository: Path) -> None:
            common_header = (
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_common.h"
            )
            insert_before_signature(
                common_header,
                "static ngx_inline ngx_int_t\n"
                "ngx_http_modsecurity_add_n_response_header",
                raw_helper,
            )
            replace_in_function(
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_header_filter.c",
                "static ngx_int_t\n"
                "ngx_http_modsecurity_add_response_headers",
                "        if (ngx_http_modsecurity_add_n_response_header(ctx,\n",
                "        if (msconnector_unchecked_response_header(ctx,\n",
            )

        self._assert_rejected(
            mutate,
            "NGINX response-header raw sink remains owned by the canonical validated Common wrapper",
        )

    def test_response_body_raw_sink_function_pointer_alias_is_rejected(self) -> None:
        bounded_call = (
            "        ret = ngx_http_modsecurity_append_response_chain_buffer(r, ctx, mcf,\n"
            "            phase4_in_scope, chain);\n"
        )
        error_return = (
            "        if (ret != NGX_OK) {\n"
            "            return ret;\n"
            "        }\n"
        )
        raw_alias = (
            bounded_call
            + error_return
            + "        static int (*const raw_body)(Transaction *, const unsigned char *, size_t) =\n"
            "            msc_append_response_body;\n"
            "        (void) raw_body(ctx->modsec_transaction, chain->buf->pos,\n"
            "            (size_t)(chain->buf->last - chain->buf->pos));\n"
        )

        def mutate(repository: Path) -> None:
            replace_in_function(
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_body_filter.c",
                "static ngx_int_t\n"
                "ngx_http_modsecurity_process_response_body_chain",
                bounded_call + error_return,
                raw_alias,
            )

        self._assert_rejected(
            mutate,
            "NGINX response-body raw sink remains owned by the bounded append helper",
        )

    def test_response_header_raw_sink_function_pointer_alias_is_rejected(self) -> None:
        validator = (
            "    if (ngx_http_modsecurity_validate_header(ctx, name, name_len, value,\n"
            "            value_len, 1) != NGX_OK) {\n"
        )
        raw_alias = (
            "    static int (*const raw_header)(Transaction *, const unsigned char *, size_t,\n"
            "        const unsigned char *, size_t) = &msc_add_n_response_header;\n"
            "    (void) raw_header(ctx->modsec_transaction, name, name_len, value, value_len);\n"
            + validator
        )

        def mutate(repository: Path) -> None:
            replace_in_function(
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_common.h",
                "static ngx_inline ngx_int_t\n"
                "ngx_http_modsecurity_add_n_response_header",
                validator,
                raw_alias,
            )

        self._assert_rejected(
            mutate,
            "NGINX response-header raw sink remains owned by the canonical validated Common wrapper",
        )

    def test_response_body_chain_cannot_return_before_scope_gate(self) -> None:
        assignment = (
            "    mcf = ngx_http_get_module_loc_conf(r, ngx_http_modsecurity_module);\n"
        )

        def mutate(repository: Path) -> None:
            replace_in_function(
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_body_filter.c",
                "static ngx_int_t\n"
                "ngx_http_modsecurity_process_response_body_chain",
                assignment,
                "    if (0) {\n"
                "        return NGX_OK;\n"
                "    }\n"
                + assignment,
            )

        self._assert_rejected(
            mutate,
            "NGINX response-body chain loop directly calls the reviewed bounded wrapper",
        )

    def test_response_header_collection_cannot_neutralize_traversal_state(self) -> None:
        resolver_loop = (
            "    for (i = 0; ngx_http_modsecurity_headers_out[i].name.len; i++) {\n"
        )

        def mutate(repository: Path) -> None:
            replace_in_function(
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_header_filter.c",
                "static ngx_int_t\n"
                "ngx_http_modsecurity_add_response_headers",
                resolver_loop,
                "    ngx_http_modsecurity_headers_out[0].name.len = 0U;\n"
                "    part->nelts = 0U;\n"
                "    part->next = NULL;\n"
                + resolver_loop,
            )

        self._assert_rejected(
            mutate,
            "NGINX response-header collection retains the reviewed synthetic and chained traversal",
        )

    def test_body_filter_cannot_invoke_chunk_before_direct_chain(self) -> None:
        direct_chain = (
            "    return ngx_http_modsecurity_process_response_body_chain(r, in, ctx);\n"
        )
        intermediate_caller = (
            "    static ngx_int_t (*const raw_chunk)(ngx_http_modsecurity_ctx_t *,\n"
            "        u_char *, size_t) = ngx_http_modsecurity_append_response_body_chunk;\n"
            "    (void)raw_chunk(ctx, in->buf->pos,\n"
            "        (size_t)(in->buf->last - in->buf->pos));\n"
            + direct_chain
        )

        def mutate(repository: Path) -> None:
            replace_in_function(
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_body_filter.c",
                "ngx_int_t\nngx_http_modsecurity_body_filter(ngx_http_request_t *r, ngx_chain_t *in)",
                direct_chain,
                intermediate_caller,
            )

        self._assert_rejected(
            mutate,
            "NGINX response-body filter retains only the direct prepared chain path",
        )

    def test_response_body_buffer_requires_limited_memory_path(self) -> None:
        limited_memory_path = (
            "        return ngx_http_modsecurity_append_limited_response_body(ctx, mcf,\n"
            "            data, len);\n"
        )
        direct_chunk = (
            "        return ngx_http_modsecurity_append_response_body_chunk(ctx, data, len);\n"
        )

        def mutate(repository: Path) -> None:
            replace_in_function(
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_body_filter.c",
                "static ngx_int_t\n"
                "ngx_http_modsecurity_append_response_body_buffer",
                limited_memory_path,
                direct_chunk,
            )

        self._assert_rejected(
            mutate,
            "NGINX response-body buffer route retains the bounded memory/file planner paths",
        )

    def test_limited_response_body_cannot_ignore_planned_allowance(self) -> None:
        planned_allowance = (
            "    return ngx_http_modsecurity_append_response_body_chunk(ctx, data, allowed);\n"
        )
        unbounded_length = (
            "    return ngx_http_modsecurity_append_response_body_chunk(ctx, data, len);\n"
        )

        def mutate(repository: Path) -> None:
            replace_in_function(
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_body_filter.c",
                "static ngx_int_t\n"
                "ngx_http_modsecurity_append_limited_response_body",
                planned_allowance,
                unbounded_length,
            )

        self._assert_rejected(
            mutate,
            "NGINX limited response-body helper passes the Common-planned allowance to the raw chunk route",
        )

    def test_phase4_scope_predicate_cannot_be_neutralized(self) -> None:
        declaration = (
            "    ngx_http_modsecurity_conf_t *mcf = ngx_http_get_module_loc_conf(r, ngx_http_modsecurity_module);\n"
        )

        def mutate(repository: Path) -> None:
            replace_in_function(
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_body_filter.c",
                "static ngx_int_t\nngx_http_modsecurity_phase4_in_scope",
                declaration,
                "    return 1;\n" + declaration,
            )

        self._assert_rejected(
            mutate,
            "NGINX Phase4 scope predicate retains the reviewed content-type allowlist",
        )

    def test_synthetic_date_resolver_cannot_return_before_wrapper(self) -> None:
        context_lookup = (
            "    ctx = ngx_http_modsecurity_get_module_ctx(r);\n\n"
        )

        def mutate(repository: Path) -> None:
            replace_in_function(
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_header_filter.c",
                "static ngx_int_t\nngx_http_modsecurity_resolv_header_date",
                context_lookup,
                context_lookup
                + "    if (r != NULL) {\n"
                "        return 1;\n"
                "    }\n\n",
            )

        self._assert_rejected(
            mutate,
            "NGINX synthetic response-header resolver table and Date route retain the validated Common wrapper",
        )

    def test_synthetic_resolver_table_cannot_rebind_date(self) -> None:
        table_path = (
            Path("connectors")
            / "nginx"
            / "src"
            / "ngx_http_modsecurity_header_filter.c"
        )
        old_resolver = "            ngx_http_modsecurity_resolv_header_date },"
        new_resolver = "            ngx_http_modsecurity_resolv_header_server },"

        def mutate(repository: Path) -> None:
            path = repository / table_path
            source = path.read_text(encoding="utf-8")
            if source.count(old_resolver) != 1:
                raise AssertionError("expected exactly one Date resolver table entry")
            path.write_text(
                source.replace(old_resolver, new_resolver, 1),
                encoding="utf-8",
            )

        self._assert_rejected(
            mutate,
            "NGINX synthetic response-header resolver table and Date route retain the validated Common wrapper",
        )

    def test_next_header_cannot_terminate_chained_traversal_early(self) -> None:
        iterator = "    for (;;) {\n"
        terminated_iterator = (
            iterator
            + "        if (part != NULL) {\n"
            "            return NULL;\n"
            "        }\n"
        )

        def mutate(repository: Path) -> None:
            replace_in_function(
                repository
                / "connectors"
                / "nginx"
                / "src"
                / "ngx_http_modsecurity_common.h",
                "static ngx_inline ngx_table_elt_t *\n"
                "ngx_http_modsecurity_next_header",
                iterator,
                terminated_iterator,
            )

        self._assert_rejected(
            mutate,
            "NGINX chained response-header traversal retains the canonical Common iterator",
        )

    def test_post_mapper_header_corridor_bypasses_are_rejected(self) -> None:
        mapper_call = (
            "    ngx_http_modsecurity_validate_response_mapper(ctx, r,\n"
            "        NGX_HTTP_MODSECURITY_RESPONSE_MAPPER_DIAGNOSTIC_HEADER);\n"
        )
        marker = mapper_call + "    ctx->common_response_validated = 1;\n"
        cases = (
            (
                "processed state assignment",
                mapper_call
                + "    ctx->processed = 1;\n"
                + "    ctx->common_response_validated = 1;\n",
            ),
            (
                "conditional early return",
                mapper_call
                + "#if 1\n"
                + "    return NGX_OK;\n"
                + "#endif\n"
                + "    ctx->common_response_validated = 1;\n",
            ),
            (
                "post-validation context null assignment",
                marker + "    ctx = NULL;\n",
            ),
        )

        for name, replacement in cases:
            with self.subTest(bypass=name):
                def mutate(
                    repository: Path, replacement: str = replacement
                ) -> None:
                    replace_in_function(
                        repository
                        / "connectors"
                        / "nginx"
                        / "src"
                        / "ngx_http_modsecurity_header_filter.c",
                        "ngx_int_t\n"
                        "ngx_http_modsecurity_header_filter(ngx_http_request_t *r)\n{",
                        marker,
                        replacement,
                    )

                self._assert_rejected(
                    mutate,
                    "NGINX header mapper validation retains its existing eligibility and ordering without a once gate",
                )

    def test_response_mapper_context_mutations_are_rejected(self) -> None:
        cases = (
            (
                "mapper helper",
                "void\nngx_http_modsecurity_validate_response_mapper",
                "    msconnector_response_mapper_contract_init(&contract);\n",
                "    memset((void *)ctx, 0, sizeof(*ctx));\n"
                "    msconnector_response_mapper_contract_init(&contract);\n",
            ),
            (
                "mapper implementation",
                "int ngx_http_modsecurity_map_response_from_ctx",
                "    (void)ctx;\n",
                "    memset((void *)ctx, 0, sizeof(*ctx));\n",
            ),
        )

        for name, signature, anchor, replacement in cases:
            with self.subTest(mutation=name):
                def mutate(
                    repository: Path,
                    signature: str = signature,
                    anchor: str = anchor,
                    replacement: str = replacement,
                ) -> None:
                    replace_in_function(
                        repository
                        / "connectors"
                        / "nginx"
                        / "src"
                        / "ngx_http_modsecurity_mapper.c",
                        signature,
                        anchor,
                        replacement,
                    )

                self._assert_rejected(
                    mutate,
                    "NGINX response mapper helper excludes caller lifecycle, body, enforcement, filter-chain, and allocation control",
                )

    def test_indirect_calls_are_rejected(self) -> None:
        mapper_cases = (
            (
                "nested cast",
                "",
                "    typedef void (*msconnector_mapper_hook_type)(void);\n"
                "    static msconnector_mapper_hook_type msconnector_mapper_hook;\n"
                "    (*(msconnector_mapper_hook_type)msconnector_mapper_hook)();\n",
            ),
            (
                "indexed function pointer",
                "static void (*msconnector_mapper_hooks[1])(void);\n\n",
                "    msconnector_mapper_hooks[0]();\n",
            ),
            (
                "member function pointer",
                "struct msconnector_mapper_hook_table {\n"
                "    void (*msconnector_response_mapper_contract_init)(void);\n"
                "};\n"
                "static struct msconnector_mapper_hook_table "
                "msconnector_mapper_hooks;\n\n",
                "    msconnector_mapper_hooks."
                "msconnector_response_mapper_contract_init();\n",
            ),
        )

        for name, declaration, indirect_call in mapper_cases:
            with self.subTest(mapper=name):
                def mutate_mapper(
                    repository: Path,
                    declaration: str = declaration,
                    indirect_call: str = indirect_call,
                ) -> None:
                    path = (
                        repository
                        / "connectors"
                        / "nginx"
                        / "src"
                        / "ngx_http_modsecurity_mapper.c"
                    )
                    if declaration:
                        insert_before_signature(
                            path,
                            "void\nngx_http_modsecurity_validate_response_mapper",
                            declaration,
                        )
                    replace_in_function(
                        path,
                        "void\nngx_http_modsecurity_validate_response_mapper",
                        "    msconnector_response_mapper_contract_init(&contract);\n",
                        indirect_call
                        + "    msconnector_response_mapper_contract_init(&contract);\n",
                    )

                self._assert_rejected(
                    mutate_mapper,
                    "NGINX response mapper helper excludes caller lifecycle, body, enforcement, filter-chain, and allocation control",
                )

        nested_indirect_call = mapper_cases[0][2]

        macro_cases = (
            (
                "read",
                "#define dd_check_read_event_handler(r)",
                "\n\n#define dd_check_write_event_handler(r)",
            ),
            (
                "write",
                "#define dd_check_write_event_handler(r)",
                "\n\n#else\n\n#if (NGX_HAVE_VARIADIC_MACROS)",
            ),
        )

        for name, macro_start, macro_end in macro_cases:
            with self.subTest(macro=name):
                def mutate_macro(
                    repository: Path,
                    macro_start: str = macro_start,
                    macro_end: str = macro_end,
                ) -> None:
                    path = (
                        repository
                        / "connectors"
                        / "nginx"
                        / "src"
                        / "ddebug.h"
                    )
                    source = path.read_text(encoding="utf-8")
                    start = source.index(macro_start)
                    end = source.index(macro_end, start)
                    replacement = (
                        macro_start
                        + " do { \\\n"
                        + "    typedef void (*msconnector_mapper_hook_type)(void); \\\n"
                        + "    static msconnector_mapper_hook_type msconnector_mapper_hook; \\\n"
                        + "    (*(msconnector_mapper_hook_type)"
                        + "msconnector_mapper_hook)(); \\\n"
                        + "} while (0)"
                    )
                    path.write_text(
                        source[:start] + replacement + source[end:],
                        encoding="utf-8",
                    )

                self._assert_rejected(
                    mutate_macro,
                    "NGINX critical macro inputs reject aliases of checked lifecycle and response-body controls",
                )

    def test_forbidden_response_mapper_member_access_variants_are_rejected(
        self,
    ) -> None:
        cases = (
            ("whitespace arrow", "ctx -> processed"),
            ("parenthesized arrow", "(ctx) -> processed"),
            ("dereferenced dot", "(*ctx).processed"),
            ("indexed member", "ctx[0].processed"),
            ("parenthesized dereferenced dot", "(*(ctx)).processed"),
        )
        signature = "void\nngx_http_modsecurity_validate_response_mapper"
        anchor = "    msconnector_response_mapper_contract_init(&contract);\n"

        for name, member_access in cases:
            with self.subTest(member_access=name):
                def mutate(
                    repository: Path, member_access: str = member_access
                ) -> None:
                    replace_in_function(
                        repository
                        / "connectors"
                        / "nginx"
                        / "src"
                        / "ngx_http_modsecurity_mapper.c",
                        signature,
                        anchor,
                        "    if (ctx != NULL && " + member_access + ") {\n"
                        "        (void)(" + member_access + ");\n"
                        "    }\n\n"
                        + anchor,
                    )

                self._assert_rejected(
                    mutate,
                    "NGINX response mapper helper excludes caller lifecycle, body, enforcement, filter-chain, and allocation control",
                )

    def test_forbidden_macro_member_access_variants_are_rejected(self) -> None:
        cases = (
            ("whitespace arrow", "ctx -> processed"),
            ("dereferenced dot", "(*ctx).processed"),
            ("indexed member", "ctx[0].processed"),
            ("parenthesized dereferenced dot", "(*(ctx)).processed"),
        )
        signature = "void\nngx_http_modsecurity_validate_response_mapper"

        for name, replacement in cases:
            with self.subTest(member_access=name):
                def mutate(
                    repository: Path, replacement: str = replacement
                ) -> None:
                    insert_before_signature(
                        repository
                        / "connectors"
                        / "nginx"
                        / "src"
                        / "ngx_http_modsecurity_mapper.c",
                        signature,
                        "#define MSCONNECTOR_FORBIDDEN_MEMBER_ACCESS "
                        + replacement,
                    )

                self._assert_rejected(
                    mutate,
                    "NGINX critical macro inputs reject aliases of checked lifecycle and response-body controls",
                )

    def test_forbidden_macro_member_component_aliases_are_rejected(self) -> None:
        cases = (
            (
                "context alias",
                "#define MSCONNECTOR_MAPPER_CONTEXT ctx",
                "MSCONNECTOR_MAPPER_CONTEXT -> processed",
            ),
            (
                "member alias",
                "#define MSCONNECTOR_MAPPER_MEMBER processed",
                "ctx -> MSCONNECTOR_MAPPER_MEMBER",
            ),
        )
        signature = "void\nngx_http_modsecurity_validate_response_mapper"
        anchor = "    msconnector_response_mapper_contract_init(&contract);\n"

        for name, directive, member_access in cases:
            with self.subTest(alias=name):
                def mutate(
                    repository: Path,
                    directive: str = directive,
                    member_access: str = member_access,
                ) -> None:
                    path = (
                        repository
                        / "connectors"
                        / "nginx"
                        / "src"
                        / "ngx_http_modsecurity_mapper.c"
                    )
                    insert_before_signature(path, signature, directive)
                    replace_in_function(
                        path,
                        signature,
                        anchor,
                        "    if (ctx != NULL && " + member_access + ") {\n"
                        "        (void)(" + member_access + ");\n"
                        "    }\n\n"
                        + anchor,
                    )

                self._assert_rejected(
                    mutate,
                    "NGINX critical macro inputs reject aliases of checked lifecycle and response-body controls",
                )


if __name__ == "__main__":
    unittest.main()
