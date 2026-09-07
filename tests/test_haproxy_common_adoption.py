#!/usr/bin/env python3
"""Mutation coverage for HAProxy's global Common-adoption checker."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHECKER_DIRECTORY = ROOT / "ci" / "checks" / "connectors" / "haproxy"
HAPROXY_DIRECTORY = ROOT / "connectors" / "haproxy"
MAPPER_RELATIVE_PATH = Path("connectors/haproxy/src/haproxy_modsecurity_mapper.c")


def replace_once(path: Path, old: str, new: str) -> None:
    """Replace one expected source fragment or fail the test setup loudly."""
    source = path.read_text(encoding="utf-8")
    if source.count(old) != 1:
        raise AssertionError(f"expected one mutable fragment in {path}: {old!r}")
    path.write_text(source.replace(old, new, 1), encoding="utf-8")


class HaproxyCommonAdoptionCheckerTests(unittest.TestCase):
    """Exercise current mapper controls through isolated checker mutations."""

    def _copy_repository(self, destination: Path) -> Path:
        (destination / "Makefile").write_text(
            "# synthetic checker repository\n", encoding="utf-8"
        )
        checker_destination = destination / "ci" / "checks" / "connectors" / "haproxy"
        checker_destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(CHECKER_DIRECTORY, checker_destination)
        haproxy_destination = destination / "connectors" / "haproxy"
        haproxy_destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(HAPROXY_DIRECTORY, haproxy_destination)
        return destination / MAPPER_RELATIVE_PATH

    def _run_checker(self, mutate=None) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory(prefix="haproxy-common-adoption-") as temporary:
            repository = Path(temporary)
            mapper = self._copy_repository(repository)
            if mutate is not None:
                mutate(mapper)
            environment = os.environ.copy()
            environment["PYTHONDONTWRITEBYTECODE"] = "1"
            return subprocess.run(
                [
                    sys.executable,
                    str(
                        repository
                        / "ci"
                        / "checks"
                        / "connectors"
                        / "haproxy"
                        / "check-haproxy-common-adoption.py"
                    ),
                ],
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

    def test_current_host_contract_is_accepted(self) -> None:
        result = self._run_checker()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_removed_preallocation_host_rejection_is_rejected_despite_decoys(self) -> None:
        def mutate(mapper: Path) -> None:
            replace_once(
                mapper,
                "haproxy_validate_source_headers(src->headers, src->header_count, 1,",
                "haproxy_validate_source_headers(src->headers, src->header_count, 0,",
            )
            with mapper.open("a", encoding="utf-8") as source:
                source.write(
                    "\n/* haproxy_validate_source_headers(src->headers, src->header_count, 1, */\n"
                    "static int foreign_host_validation_decoy(void)\n"
                    "{\n"
                    "    return haproxy_validate_source_headers(0, 0U, 1, 0, 0U);\n"
                    "}\n"
                )

        self._assert_rejected(
            mutate,
            "request mapper validates exactly one Host before owned-header allocation",
        )

    def test_ignored_preallocation_host_rejection_is_rejected_despite_comment(self) -> None:
        def mutate(mapper: Path) -> None:
            guard = (
                "if (haproxy_validate_source_headers(src->headers, src->header_count, 1,\n"
                "            error, error_len) != 1) {\n"
                "        return 0;\n"
                "    }\n"
            )
            replace_once(
                mapper,
                guard,
                "(void)haproxy_validate_source_headers(src->headers, src->header_count, 1,\n"
                "            error, error_len);\n",
            )
            with mapper.open("a", encoding="utf-8") as source:
                source.write(f"\n/* {guard} */\n")

        self._assert_rejected(
            mutate,
            "request mapper validates exactly one Host before owned-header allocation",
        )

    def test_removed_empty_host_cleanup_rejection_is_rejected_despite_comment(self) -> None:
        def mutate(mapper: Path) -> None:
            replace_once(
                mapper,
                "if (host_header == 0 || host_header->value == 0 ||\n"
                "            host_header->value_size == 0U) {\n",
                "if (host_header == 0) {\n",
            )
            with mapper.open("a", encoding="utf-8") as source:
                source.write(
                    "\n/* if (host_header == 0 || host_header->value == 0 ||\n"
                    "            host_header->value_size == 0U) {\n"
                    "        haproxy_modsecurity_mapped_request_cleanup(out);\n"
                    "        return 0;\n"
                    "    } */\n"
                )

        self._assert_rejected(
            mutate,
            "request mapper rejects empty Host and cleans allocated mapper state",
        )

    def test_reintroduced_server_ip_hostname_fallback_is_rejected_despite_decoys(self) -> None:
        def mutate(mapper: Path) -> None:
            replace_once(
                mapper,
                "out->request.hostname = host_header->value;",
                "out->request.hostname = src->server_ip;",
            )
            with mapper.open("a", encoding="utf-8") as source:
                source.write(
                    "\n/* out->request.hostname = host_header->value; */\n"
                    "static void foreign_hostname_decoy(void)\n"
                    "{\n"
                    "    out->request.hostname = host_header->value;\n"
                    "}\n"
                )

        self._assert_rejected(
            mutate,
            "request mapper derives hostname from validated Host and keeps server_ip as server address",
        )

    def test_inverted_common_validation_return_is_rejected_despite_comment(self) -> None:
        def mutate(mapper: Path) -> None:
            replace_once(
                mapper,
                "rc = msconnector_request_mapper_validate_output(contract, &out->request, error, error_len);\n"
                "    if (rc != 1) {",
                "rc = msconnector_request_mapper_validate_output(contract, &out->request, error, error_len);\n"
                "    if (rc == 1) {",
            )
            with mapper.open("a", encoding="utf-8") as source:
                source.write("\n/* if (rc != 1) { return 0; } */\n")

        self._assert_rejected(
            mutate,
            "request mapper evaluates Common validation returns and cleans failures",
        )

    def test_inverted_response_validation_is_rejected_despite_comment_decoy(self) -> None:
        def mutate(mapper: Path) -> None:
            validation = (
                "rc = msconnector_response_mapper_validate_output(contract, &out->response, error, error_len);\n"
                "    if (rc != 1) {\n"
                "        haproxy_modsecurity_mapped_response_cleanup(out);\n"
                "        return 0;\n"
                "    }\n"
            )
            replace_once(
                mapper,
                validation,
                validation.replace("if (rc != 1)", "if (rc == 1)"),
            )
            with mapper.open("a", encoding="utf-8") as source:
                source.write(f"\n/* {validation} */\n")

        self._assert_rejected(
            mutate,
            "response mapper evaluates Common validation returns and cleans failures",
        )

    def test_inverted_config_merge_is_rejected_despite_comment_decoy(self) -> None:
        def mutate(mapper: Path) -> None:
            binding = mapper.parent / "haproxy_modsecurity_binding.c"
            merge_guard = (
                "if (msconnector_config_merge(&created->common_config, &created->common_config,\n"
                "                &config->common_config) != 1 ||\n"
                "                msconnector_config_validate(&created->common_config, config_error,\n"
                "                    sizeof(config_error)) != 1) {\n"
                "            copy_message(decision->log_message, sizeof(decision->log_message),\n"
                "                config_error[0] != '\\0' ? config_error : \"Common config validation failed\");\n"
                "            haproxy_modsecurity_engine_destroy(created);\n"
                "            return 1;\n"
                "        }\n"
            )
            replace_once(
                binding,
                merge_guard,
                merge_guard.replace(
                    "&config->common_config) != 1 ||",
                    "&config->common_config) == 1 ||",
                ),
            )
            with binding.open("a", encoding="utf-8") as source:
                source.write(f"\n/* {merge_guard} */\n")

        self._assert_rejected(
            mutate,
            "engine configuration treats Common merge and validation return 1 as success",
        )


if __name__ == "__main__":
    unittest.main()
