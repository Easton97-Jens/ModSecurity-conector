#!/usr/bin/env python3
"""Run local Envoy/Traefik runtime smokes without global dependencies."""

from __future__ import annotations

import argparse
import contextlib
import http.client
import http.server
import json
import os
import shutil
import socket
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path


BLOCK_VALUES = {"1", "true", "block", "yes", "on"}


def free_port() -> int:
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


class QuietHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: object) -> None:
        return


class UpstreamHandler(QuietHandler):
    def do_GET(self) -> None:
        body = b"msconnector upstream ok\n"
        self.send_response(200)
        self.send_header("content-type", "text/plain")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class SimpleDecisionBackend:
    decision_backend = "simple"
    modsecurity_backend_verified = False
    modsecurity_rule_loaded = False
    intervention_status: int | None = None
    last_error: str | None = None
    blocked_decision: dict[str, object] | None = None

    def decide(self, headers: http.client.HTTPMessage, path: str) -> dict[str, object]:
        del path
        value = headers.get("x-msconnector-block", "")
        if value.lower() in BLOCK_VALUES:
            return {
                "body": b"blocked by local msconnector decision service\n",
                "status": 403,
            }
        return {
            "body": b"allowed by local msconnector decision service\n",
            "status": 200,
        }


class ModSecurityDecisionBackend:
    decision_backend = "libmodsecurity"

    def __init__(self, helper: Path, rule_file: Path, decision_log_path: Path, env: dict[str, str]) -> None:
        self.helper = helper
        self.rule_file = rule_file
        self.decision_log_path = decision_log_path
        self.env = env
        self.modsecurity_backend_verified = False
        self.modsecurity_rule_loaded = False
        self.intervention_status: int | None = None
        self.last_error: str | None = None
        self.blocked_decision: dict[str, object] | None = None

    def _evaluate(self, header_value: str, path: str) -> dict[str, object]:
        command = [
            str(self.helper),
            "--rule-file",
            str(self.rule_file),
            "--decision-log",
            str(self.decision_log_path),
            "--uri",
            path,
        ]
        if header_value:
            command.extend(["--header-value", header_value])
        completed = subprocess.run(
            command,
            check=False,
            env=self.env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if completed.returncode != 0:
            detail = completed.stderr.strip() or completed.stdout.strip() or f"exit {completed.returncode}"
            raise RuntimeError(f"libmodsecurity targeted evaluator failed: {detail}")
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"libmodsecurity targeted evaluator returned invalid JSON: {completed.stdout}") from exc
        if not payload.get("ok"):
            raise RuntimeError(str(payload.get("error") or "libmodsecurity targeted evaluator failed"))
        return payload

    def decide(self, headers: http.client.HTTPMessage, path: str) -> dict[str, object]:
        header_value = headers.get("x-modsec-smoke", "")
        payload = self._evaluate(header_value, path)
        self.modsecurity_rule_loaded = bool(payload.get("modsecurity_rule_loaded"))
        disruptive = bool(payload.get("intervention_disruptive"))
        status = int(payload.get("intervention_status") or (403 if disruptive else 200))
        self.intervention_status = status
        if header_value == "block":
            self.blocked_decision = payload
            self.modsecurity_backend_verified = (
                self.modsecurity_rule_loaded
                and disruptive
                and status == 403
                and payload.get("modsecurity_rule_id") == "1000001"
            )
        body = (
            b"blocked by libmodsecurity targeted smoke rule\n"
            if disruptive
            else b"allowed by libmodsecurity targeted smoke rule\n"
        )
        return {
            "body": body,
            "status": status if disruptive else 200,
        }


def make_decision_handler(decision_backend: SimpleDecisionBackend | ModSecurityDecisionBackend) -> type[QuietHandler]:
    class RuntimeDecisionHandler(QuietHandler):
        def _answer(self) -> None:
            try:
                decision = decision_backend.decide(self.headers, self.path)
                status = int(decision["status"])
                body = decision["body"]
            except Exception as exc:  # noqa: BLE001 - auth backend errors become smoke evidence.
                decision_backend.last_error = str(exc)
                status = 500
                body = f"decision backend error: {exc}\n".encode("utf-8")
            self.send_response(status)
            self.send_header("content-type", "text/plain")
            self.send_header("content-length", str(len(body)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)

        do_GET = _answer
        do_POST = _answer
        do_HEAD = _answer

    return RuntimeDecisionHandler


def start_http_server(handler: type[http.server.BaseHTTPRequestHandler], port: int) -> http.server.ThreadingHTTPServer:
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def http_status(url: str, headers: dict[str, str] | None = None) -> int:
    request = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(request, timeout=2) as response:
            response.read()
            return int(response.status)
    except urllib.error.HTTPError as exc:
        exc.read()
        return int(exc.code)


def wait_for_proxy(url: str, process: subprocess.Popen[object], deadline: float, expected_status: int = 200) -> None:
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"proxy exited early with code {process.returncode}")
        try:
            status = http_status(url)
            if status == expected_status:
                return
            last_error = RuntimeError(f"proxy returned {status}, expected {expected_status}")
        except Exception as exc:  # noqa: BLE001 - startup probes may fail many ways.
            last_error = exc
        time.sleep(0.2)
    raise RuntimeError(f"proxy did not become ready: {last_error}")


def local_library_env(base_env: dict[str, str], lib_dir: Path, runtime_lookup_roots: list[str]) -> dict[str, str]:
    env = dict(base_env)
    paths = [str(lib_dir)]
    for root_text in runtime_lookup_roots:
        root = Path(root_text)
        for candidate in (
            root / "prefix/expat/lib",
            root / "expat/lib",
        ):
            if candidate.is_dir():
                paths.append(str(candidate))
    existing = env.get("LD_LIBRARY_PATH", "")
    if existing:
        paths.append(existing)
    env["LD_LIBRARY_PATH"] = os.pathsep.join(dict.fromkeys(paths))
    return env


def build_modsecurity_evaluator(args: argparse.Namespace, log_dir: Path) -> tuple[Path, dict[str, str]]:
    include_dir = Path(args.modsecurity_include_dir) if args.modsecurity_include_dir else None
    lib_dir = Path(args.modsecurity_lib_dir) if args.modsecurity_lib_dir else None
    lib_file = Path(args.modsecurity_lib_file) if args.modsecurity_lib_file else None
    rule_file = Path(args.modsecurity_rule_file) if args.modsecurity_rule_file else None
    if include_dir is None or lib_dir is None or lib_file is None or rule_file is None:
        raise RuntimeError("local libmodsecurity include dir, lib dir, lib file, and targeted rule file are required")
    for path, label in (
        (include_dir / "modsecurity/modsecurity.h", "modsecurity.h"),
        (include_dir / "modsecurity/rules_set.h", "rules_set.h"),
        (include_dir / "modsecurity/transaction.h", "transaction.h"),
        (lib_file, "libmodsecurity shared library"),
        (rule_file, "targeted smoke rule"),
    ):
        if not path.exists():
            raise RuntimeError(f"missing {label}: {path}")

    cxx = os.environ.get("CXX") or shutil.which("c++") or shutil.which("g++")
    if not cxx:
        raise RuntimeError("missing C++ compiler for targeted libmodsecurity smoke evaluator")

    source = Path(args.connector_root) / "common/scripts/modsecurity_targeted_eval.cc"
    if not source.is_file():
        raise RuntimeError(f"modsecurity targeted evaluator source missing: {source}")

    build_dir = Path(args.tmp_root) / f"{args.connector}-modsecurity-targeted-smoke"
    build_dir.mkdir(parents=True, exist_ok=True)
    output = build_dir / "modsecurity_targeted_eval"
    command = [
        cxx,
        "-std=c++17",
        "-I",
        str(include_dir),
        str(source),
        "-L",
        str(lib_dir),
        f"-Wl,-rpath,{lib_dir}",
        "-lmodsecurity",
        "-o",
        str(output),
    ]
    (log_dir / "modsecurity-evaluator-build-command.txt").write_text(" ".join(command) + "\n", encoding="utf-8")
    completed = subprocess.run(command, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    (log_dir / "modsecurity-evaluator-build.stdout.log").write_text(completed.stdout, encoding="utf-8")
    (log_dir / "modsecurity-evaluator-build.stderr.log").write_text(completed.stderr, encoding="utf-8")
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip() or f"exit {completed.returncode}"
        raise RuntimeError(f"could not build targeted libmodsecurity evaluator: {detail}")
    output.chmod(0o755)
    env = local_library_env(os.environ, lib_dir, args.runtime_lookup_root)
    return output, env


def envoy_config(listen_port: int, admin_port: int, upstream_port: int, auth_port: int) -> str:
    return f"""static_resources:
  listeners:
  - name: listener_0
    address:
      socket_address:
        address: 127.0.0.1
        port_value: {listen_port}
    filter_chains:
    - filters:
      - name: envoy.filters.network.http_connection_manager
        typed_config:
          "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
          stat_prefix: ingress_http
          route_config:
            name: local_route
            virtual_hosts:
            - name: local_service
              domains: ["*"]
              routes:
              - match:
                  prefix: "/"
                route:
                  cluster: upstream_service
          http_filters:
          - name: envoy.filters.http.ext_authz
            typed_config:
              "@type": type.googleapis.com/envoy.extensions.filters.http.ext_authz.v3.ExtAuthz
              http_service:
                server_uri:
                  uri: http://127.0.0.1:{auth_port}
                  cluster: ext_authz
                  timeout: 0.5s
                path_prefix: /auth
                authorization_request:
                  allowed_headers:
                    patterns:
                    - exact: x-msconnector-block
                    - exact: x-modsec-smoke
          - name: envoy.filters.http.router
            typed_config:
              "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
  clusters:
  - name: upstream_service
    connect_timeout: 0.25s
    type: STRICT_DNS
    lb_policy: ROUND_ROBIN
    load_assignment:
      cluster_name: upstream_service
      endpoints:
      - lb_endpoints:
        - endpoint:
            address:
              socket_address:
                address: 127.0.0.1
                port_value: {upstream_port}
  - name: ext_authz
    connect_timeout: 0.25s
    type: STRICT_DNS
    lb_policy: ROUND_ROBIN
    load_assignment:
      cluster_name: ext_authz
      endpoints:
      - lb_endpoints:
        - endpoint:
            address:
              socket_address:
                address: 127.0.0.1
                port_value: {auth_port}
admin:
  access_log_path: /dev/null
  address:
    socket_address:
      address: 127.0.0.1
      port_value: {admin_port}
"""


def traefik_dynamic_config(upstream_port: int, auth_port: int) -> str:
    return f"""http:
  routers:
    msconnector:
      entryPoints:
      - web
      rule: PathPrefix(`/`)
      middlewares:
      - msconnector-auth
      service: upstream
  middlewares:
    msconnector-auth:
      forwardAuth:
        address: http://127.0.0.1:{auth_port}/auth
        trustForwardHeader: true
        authRequestHeaders:
        - X-Msconnector-Block
        - X-Modsec-Smoke
  services:
    upstream:
      loadBalancer:
        servers:
        - url: http://127.0.0.1:{upstream_port}
"""


def build_proxy_command(connector: str, binary: Path, work_dir: Path, listen_port: int, upstream_port: int, auth_port: int) -> list[str]:
    if connector == "envoy":
        admin_port = free_port()
        config_path = work_dir / "envoy.yaml"
        config_path.write_text(envoy_config(listen_port, admin_port, upstream_port, auth_port), encoding="utf-8")
        return [
            str(binary),
            "-c",
            str(config_path),
            "--base-id",
            str((listen_port + admin_port) % 100000),
            "--disable-hot-restart",
            "--log-level",
            "error",
        ]

    if connector == "traefik":
        dynamic_path = work_dir / "traefik-dynamic.yml"
        dynamic_path.write_text(traefik_dynamic_config(upstream_port, auth_port), encoding="utf-8")
        return [
            str(binary),
            "--entryPoints.web.address=127.0.0.1:%d" % listen_port,
            "--providers.file.filename=%s" % dynamic_path,
            "--providers.file.watch=false",
            "--api=false",
            "--log.level=ERROR",
            "--global.sendAnonymousUsage=false",
        ]

    raise ValueError(f"unsupported connector for local runtime smoke: {connector}")


def writer_args(
    args: argparse.Namespace,
    status: str,
    exit_code: int,
    runtime_verified: bool,
    allowed: int | None,
    blocked: int | None,
    skipped_reason: str,
    missing: list[str],
    modsecurity_backend_verified: bool = False,
    modsecurity_rule_loaded: bool = False,
    intervention_status: int | None = None,
    decision_log_path: str = "",
    audit_log_path: str = "",
) -> list[str]:
    command = [
        sys.executable,
        str(Path(args.connector_root) / "common/scripts/write_smoke_result.py"),
        "--connector",
        args.connector,
        "--integration-mode",
        args.integration_mode,
        "--status",
        status,
        "--exit-code",
        str(exit_code),
        "--runtime-verified",
        "true" if runtime_verified else "false",
        "--response-body-verified",
        "false",
        "--allowed-request-status",
        str(allowed) if allowed is not None else "not-run",
        "--blocked-request-status",
        str(blocked) if blocked is not None else "not-run",
        "--decision-backend",
        args.decision_backend,
        "--modsecurity-backend-verified",
        "true" if modsecurity_backend_verified else "false",
        "--modsecurity-rule-file",
        args.modsecurity_rule_file,
        "--modsecurity-rule-id",
        "1000001" if args.decision_backend == "libmodsecurity" else "",
        "--modsecurity-rule-loaded",
        "true" if modsecurity_rule_loaded else "false",
        "--intervention-status",
        str(intervention_status) if intervention_status is not None else "not-run",
        "--audit-log-path",
        audit_log_path,
        "--decision-log-path",
        decision_log_path,
        "--modsecurity-include-dir",
        args.modsecurity_include_dir,
        "--modsecurity-lib-dir",
        args.modsecurity_lib_dir,
        "--modsecurity-lib-file",
        args.modsecurity_lib_file,
        "--modsecurity-pkg-config-path",
        args.modsecurity_pkg_config_path,
        "--modsecurity-prefix",
        args.modsecurity_prefix,
        "--modsecurity-manifest",
        args.modsecurity_manifest,
        "--evidence-root",
        args.evidence_root,
        "--results-dir",
        args.results_dir,
        "--connector-root",
        args.connector_root,
        "--source-root",
        args.source_root,
        "--build-root",
        args.build_root,
        "--tmp-root",
        args.tmp_root,
        "--log-root",
        args.log_root,
        "--log-dir",
        args.log_dir,
        "--harness-path",
        args.harness_path,
        "--skipped-reason",
        skipped_reason,
        "--resolved-runtime-binary",
        args.resolved_runtime_binary,
        "--runtime-binary-env-var",
        args.runtime_binary_env_var,
        "--runtime-binary-name",
        args.runtime_binary_name,
        "--architecture-decision",
        args.architecture_decision,
    ]
    for dependency in missing:
        command.extend(["--missing-dependency", dependency])
    for root in args.runtime_lookup_root:
        command.extend(["--runtime-lookup-root", root])
    return command


def write_result(
    args: argparse.Namespace,
    status: str,
    exit_code: int,
    runtime_verified: bool,
    allowed: int | None,
    blocked: int | None,
    skipped_reason: str,
    missing: list[str],
    modsecurity_backend_verified: bool = False,
    modsecurity_rule_loaded: bool = False,
    intervention_status: int | None = None,
    decision_log_path: str = "",
    audit_log_path: str = "",
) -> None:
    subprocess.run(
        writer_args(
            args,
            status,
            exit_code,
            runtime_verified,
            allowed,
            blocked,
            skipped_reason,
            missing,
            modsecurity_backend_verified,
            modsecurity_rule_loaded,
            intervention_status,
            decision_log_path,
            audit_log_path,
        ),
        check=True,
    )


def run_smoke(args: argparse.Namespace) -> int:
    binary = Path(args.resolved_runtime_binary)
    work_dir = Path(args.config_root)
    log_dir = Path(args.log_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)
    decision_log_path = log_dir / "modsecurity-decision.log" if args.decision_backend == "libmodsecurity" else None

    try:
        if args.decision_backend == "libmodsecurity":
            helper, helper_env = build_modsecurity_evaluator(args, log_dir)
            decision_backend: SimpleDecisionBackend | ModSecurityDecisionBackend = ModSecurityDecisionBackend(
                helper,
                Path(args.modsecurity_rule_file),
                decision_log_path if decision_log_path is not None else log_dir / "modsecurity-decision.log",
                helper_env,
            )
        else:
            decision_backend = SimpleDecisionBackend()
    except Exception as exc:  # noqa: BLE001 - dependency/build gaps become blocked evidence.
        write_result(
            args,
            "BLOCKED",
            77,
            False,
            None,
            None,
            f"{args.connector} libmodsecurity decision backend could not be prepared: {exc}",
            ["libmodsecurity"],
            False,
            False,
            None,
            str(decision_log_path) if decision_log_path is not None else "",
        )
        return 77

    upstream_port = args.upstream_port or free_port()
    auth_port = args.authz_port or free_port()
    listen_port = args.listen_port or free_port()
    upstream_server: http.server.ThreadingHTTPServer | None = None
    auth_server: http.server.ThreadingHTTPServer | None = None
    stdout_path = log_dir / f"{args.connector}.stdout.log"
    stderr_path = log_dir / f"{args.connector}.stderr.log"
    allowed_status: int | None = None
    blocked_status: int | None = None
    process: subprocess.Popen[object] | None = None

    try:
        upstream_server = start_http_server(UpstreamHandler, upstream_port)
        auth_server = start_http_server(make_decision_handler(decision_backend), auth_port)
        command = build_proxy_command(args.connector, binary, work_dir, listen_port, upstream_port, auth_port)
        (work_dir / "proxy-command.txt").write_text(" ".join(command) + "\n", encoding="utf-8")
        with stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
            process = subprocess.Popen(command, stdout=stdout, stderr=stderr)
            wait_for_proxy(f"http://127.0.0.1:{listen_port}/allowed", process, time.monotonic() + 12)
            allowed_status = http_status(f"http://127.0.0.1:{listen_port}/allowed")
            blocked_headers = (
                {"X-Modsec-Smoke": "block"}
                if args.decision_backend == "libmodsecurity"
                else {"X-Msconnector-Block": "1"}
            )
            blocked_status = http_status(
                f"http://127.0.0.1:{listen_port}/blocked",
                blocked_headers,
            )

        modsecurity_backend_verified = bool(
            getattr(decision_backend, "modsecurity_backend_verified", False)
        )
        modsecurity_rule_loaded = bool(getattr(decision_backend, "modsecurity_rule_loaded", False))
        intervention_status = getattr(decision_backend, "intervention_status", None)
        backend_error = getattr(decision_backend, "last_error", None)
        success = allowed_status == 200 and blocked_status == 403
        if args.decision_backend == "libmodsecurity":
            success = success and modsecurity_backend_verified

        if success:
            write_result(
                args,
                "PASS",
                0,
                True,
                allowed_status,
                blocked_status,
                "",
                [],
                modsecurity_backend_verified,
                modsecurity_rule_loaded,
                intervention_status,
                str(decision_log_path) if decision_log_path is not None else "",
            )
            return 0

        reason = f"{args.connector} local runtime smoke did not produce expected 200/403 statuses"
        missing: list[str] = []
        if args.decision_backend == "libmodsecurity" and not modsecurity_backend_verified:
            reason = (
                f"{args.connector} libmodsecurity targeted smoke did not verify "
                "a rule-backed 403 intervention"
            )
            missing = ["libmodsecurity"] if backend_error else []
        if backend_error:
            reason = f"{reason}: {backend_error}"
        write_result(
            args,
            "BLOCKED",
            77,
            False,
            allowed_status,
            blocked_status,
            reason,
            missing,
            modsecurity_backend_verified,
            modsecurity_rule_loaded,
            intervention_status,
            str(decision_log_path) if decision_log_path is not None else "",
        )
        return 77
    except Exception as exc:  # noqa: BLE001 - all runtime startup failures become blocked evidence.
        modsecurity_backend_verified = bool(
            getattr(decision_backend, "modsecurity_backend_verified", False)
        )
        modsecurity_rule_loaded = bool(getattr(decision_backend, "modsecurity_rule_loaded", False))
        intervention_status = getattr(decision_backend, "intervention_status", None)
        write_result(
            args,
            "BLOCKED",
            77,
            False,
            allowed_status,
            blocked_status,
            f"{args.connector} local runtime smoke could not be completed: {exc}",
            [args.runtime_binary_name],
            modsecurity_backend_verified,
            modsecurity_rule_loaded,
            intervention_status,
            str(decision_log_path) if decision_log_path is not None else "",
        )
        return 77
    finally:
        if process is not None and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
        if upstream_server is not None:
            upstream_server.shutdown()
            upstream_server.server_close()
        if auth_server is not None:
            auth_server.shutdown()
            auth_server.server_close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--connector", required=True, choices=["envoy", "traefik"])
    parser.add_argument("--integration-mode", required=True)
    parser.add_argument("--resolved-runtime-binary", required=True)
    parser.add_argument("--runtime-binary-env-var", required=True)
    parser.add_argument("--runtime-binary-name", required=True)
    parser.add_argument("--runtime-lookup-root", action="append", default=[])
    parser.add_argument("--evidence-root", required=True)
    parser.add_argument("--results-dir", required=True)
    parser.add_argument("--connector-root", required=True)
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--build-root", required=True)
    parser.add_argument("--tmp-root", required=True)
    parser.add_argument("--log-root", required=True)
    parser.add_argument("--log-dir", required=True)
    parser.add_argument("--config-root", required=True)
    parser.add_argument("--listen-port", type=int, default=0)
    parser.add_argument("--upstream-port", type=int, default=0)
    parser.add_argument("--authz-port", type=int, default=0)
    parser.add_argument("--harness-path", required=True)
    parser.add_argument("--architecture-decision", default="")
    parser.add_argument("--decision-backend", choices=["simple", "libmodsecurity"], default="simple")
    parser.add_argument("--modsecurity-rule-file", default="")
    parser.add_argument("--modsecurity-include-dir", default="")
    parser.add_argument("--modsecurity-lib-dir", default="")
    parser.add_argument("--modsecurity-lib-file", default="")
    parser.add_argument("--modsecurity-pkg-config-path", default="")
    parser.add_argument("--modsecurity-prefix", default="")
    parser.add_argument("--modsecurity-manifest", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return run_smoke(args)


if __name__ == "__main__":
    raise SystemExit(main())
