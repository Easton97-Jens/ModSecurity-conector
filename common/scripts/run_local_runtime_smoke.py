#!/usr/bin/env python3
"""Run local Envoy/Traefik runtime smokes without global dependencies."""

from __future__ import annotations

import argparse
import contextlib
import http.server
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


class DecisionHandler(QuietHandler):
    def _answer(self) -> None:
        value = self.headers.get("x-msconnector-block", "")
        if value.lower() in BLOCK_VALUES:
            body = b"blocked by local msconnector decision service\n"
            self.send_response(403)
            self.send_header("content-type", "text/plain")
            self.send_header("content-length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        body = b"allowed by local msconnector decision service\n"
        self.send_response(200)
        self.send_header("content-type", "text/plain")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    do_GET = _answer
    do_POST = _answer
    do_HEAD = _answer


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


def wait_for_proxy(url: str, process: subprocess.Popen[object], deadline: float) -> None:
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"proxy exited early with code {process.returncode}")
        try:
            http_status(url)
            return
        except Exception as exc:  # noqa: BLE001 - startup probes may fail many ways.
            last_error = exc
            time.sleep(0.2)
    raise RuntimeError(f"proxy did not become ready: {last_error}")


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


def writer_args(args: argparse.Namespace, status: str, exit_code: int, runtime_verified: bool, allowed: int | None, blocked: int | None, skipped_reason: str, missing: list[str]) -> list[str]:
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


def write_result(args: argparse.Namespace, status: str, exit_code: int, runtime_verified: bool, allowed: int | None, blocked: int | None, skipped_reason: str, missing: list[str]) -> None:
    subprocess.run(
        writer_args(args, status, exit_code, runtime_verified, allowed, blocked, skipped_reason, missing),
        check=True,
    )


def run_smoke(args: argparse.Namespace) -> int:
    binary = Path(args.resolved_runtime_binary)
    evidence_root = Path(args.evidence_root)
    work_dir = Path(args.config_root)
    log_dir = Path(args.log_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    upstream_port = args.upstream_port or free_port()
    auth_port = args.authz_port or free_port()
    listen_port = args.listen_port or free_port()
    upstream_server = start_http_server(UpstreamHandler, upstream_port)
    auth_server = start_http_server(DecisionHandler, auth_port)
    stdout_path = log_dir / f"{args.connector}.stdout.log"
    stderr_path = log_dir / f"{args.connector}.stderr.log"
    allowed_status: int | None = None
    blocked_status: int | None = None
    process: subprocess.Popen[object] | None = None

    try:
        command = build_proxy_command(args.connector, binary, work_dir, listen_port, upstream_port, auth_port)
        (work_dir / "proxy-command.txt").write_text(" ".join(command) + "\n", encoding="utf-8")
        with stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
            process = subprocess.Popen(command, stdout=stdout, stderr=stderr)
            wait_for_proxy(f"http://127.0.0.1:{listen_port}/allowed", process, time.monotonic() + 12)
            allowed_status = http_status(f"http://127.0.0.1:{listen_port}/allowed")
            blocked_status = http_status(
                f"http://127.0.0.1:{listen_port}/blocked",
                {"X-Msconnector-Block": "1"},
            )

        if allowed_status == 200 and blocked_status == 403:
            write_result(
                args,
                "PASS",
                0,
                True,
                allowed_status,
                blocked_status,
                "",
                [],
            )
            return 0

        write_result(
            args,
            "BLOCKED",
            77,
            False,
            allowed_status,
            blocked_status,
            f"{args.connector} local runtime smoke did not produce expected 200/403 statuses",
            [args.runtime_binary_name],
        )
        return 77
    except Exception as exc:  # noqa: BLE001 - all runtime startup failures become blocked evidence.
        write_result(
            args,
            "BLOCKED",
            77,
            False,
            allowed_status,
            blocked_status,
            f"{args.connector} local runtime smoke could not be completed: {exc}",
            [args.runtime_binary_name],
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
        upstream_server.shutdown()
        auth_server.shutdown()
        upstream_server.server_close()
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
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return run_smoke(args)


if __name__ == "__main__":
    raise SystemExit(main())
