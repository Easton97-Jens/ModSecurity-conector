#!/usr/bin/env python3
"""Run a real Traefik -> forwardAuth service -> libmodsecurity smoke."""

from __future__ import annotations

import argparse
import contextlib
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


class MissingDependency(RuntimeError):
    """A required local executable is absent before the smoke starts."""


class UpstreamHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        body = b"traefik forwardauth upstream ok\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: object) -> None:
        del fmt, args


def free_port() -> int:
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def require_local_executable(path: Path, label: str) -> Path:
    if not path.is_absolute():
        raise MissingDependency(f"{label} must be an absolute local path: {path}")
    if str(path).startswith(("/usr/", "/bin/", "/sbin/", "/opt/")):
        raise MissingDependency(f"{label} must not use a global system path: {path}")
    if not path.is_file() or not os.access(path, os.X_OK):
        raise MissingDependency(f"{label} is not executable: {path}")
    return path


def consume_no_crs_selected_cases(repo_root: Path) -> None:
    """Require the canonical plan before using the narrow host smoke.

    The shell helper intentionally records no PASS result: evidence finalization
    will retain selected catalog entries with no live case result as
    ``NOT_EXECUTED``.
    """
    if os.environ.get("MSCONNECTOR_NO_CRS_BASELINE", "") != "1":
        return
    consumer = repo_root / "ci" / "consume-no-crs-selected-cases.sh"
    if not consumer.is_file() or not os.access(consumer, os.X_OK):
        raise MissingDependency(f"No-CRS selected-case consumer is missing: {consumer}")
    completed = subprocess.run(
        [str(consumer), "traefik"],
        cwd=repo_root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.stdout:
        print(completed.stdout, end="")
    if completed.returncode != 0:
        detail = completed.stderr.strip() or "selected-case consumer failed"
        raise RuntimeError(detail)


def assert_output_root(path: Path, repo_root: Path) -> None:
    if not path.is_absolute():
        raise MissingDependency(f"runtime smoke output root must be absolute: {path}")
    if path in {Path("/"), Path("/tmp"), Path("/var/tmp")}:
        raise MissingDependency(f"runtime smoke output root is too broad: {path}")
    try:
        path.resolve(strict=False).relative_to(repo_root.resolve())
    except ValueError:
        return
    raise MissingDependency(f"runtime smoke output must be outside the checkout: {path}")


def assert_no_symlink_components(path: Path) -> None:
    absolute = Path(os.path.abspath(path))
    current = Path(absolute.anchor)
    for component in absolute.parts[1:]:
        current /= component
        if current.is_symlink():
            raise MissingDependency(
                f"runtime smoke output path must not contain symlinks: {current}"
            )
        if not current.exists():
            break


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def verify_block_event(path: Path, expected_rule_id: str) -> dict[str, object]:
    if not path.is_file():
        raise RuntimeError(f"Common event JSONL is missing: {path}")
    records: list[dict[str, object]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            value = json.loads(line)
            if not isinstance(value, dict):
                raise RuntimeError("Common event JSONL record is not an object")
            records.append(value)
    for record in records:
        if (
            record.get("connector") == "traefik"
            and record.get("transaction_id") == "traefik-forwardauth-block"
            and record.get("rule_id") == expected_rule_id
            and record.get("status") == "blocked"
            and record.get("http_status") == 403
        ):
            forbidden = {"request_body", "response_body", "body_payload", "body_snippet"}
            if forbidden.intersection(record):
                raise RuntimeError("Common event JSONL contains a forbidden body payload field")
            return record
    raise RuntimeError(
        f"Common event JSONL lacks the expected rule {expected_rule_id} blocked event"
    )


def concrete_service_config(template: Path, destination: Path, rules_file: Path, event_path: Path) -> None:
    lines: list[str] = []
    for line in template.read_text(encoding="utf-8").splitlines():
        if line.startswith("rules_file="):
            line = f"rules_file={rules_file}"
        elif line.startswith("event_path="):
            line = f"event_path={event_path}"
        lines.append(line)
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")


def dynamic_config(upstream_port: int, auth_port: int) -> str:
    return f"""http:
  routers:
    smoke:
      entryPoints:
      - web
      rule: PathPrefix(`/`)
      middlewares:
      - modsecurity-forwardauth
      service: upstream
  middlewares:
    modsecurity-forwardauth:
      forwardAuth:
        address: http://127.0.0.1:{auth_port}/authorize
        trustForwardHeader: false
        authRequestHeaders:
        - X-Modsec-Smoke
        - X-Request-Id
  services:
    upstream:
      loadBalancer:
        servers:
        - url: http://127.0.0.1:{upstream_port}
"""


def http_status(url: str, headers: dict[str, str] | None = None) -> int:
    request = urllib.request.Request(url, headers=headers or {}, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=2) as response:
            response.read()
            return int(response.status)
    except urllib.error.HTTPError as exc:
        exc.read()
        return int(exc.code)


def wait_for_tcp(port: int, process: subprocess.Popen[bytes], label: str) -> None:
    deadline = time.monotonic() + 10
    last_error: OSError | None = None
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"{label} exited early with code {process.returncode}")
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                return
        except OSError as exc:
            last_error = exc
        time.sleep(0.1)
    raise RuntimeError(f"{label} did not listen on port {port}: {last_error}")


def wait_for_traefik(port: int, process: subprocess.Popen[bytes]) -> None:
    deadline = time.monotonic() + 12
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"Traefik exited early with code {process.returncode}")
        try:
            if http_status(f"http://127.0.0.1:{port}/ready") == 200:
                return
        except Exception as exc:  # startup connection failures are retried
            last_error = exc
        time.sleep(0.2)
    raise RuntimeError(f"Traefik did not become ready: {last_error}")


def stop_process(process: subprocess.Popen[bytes] | None) -> None:
    if process is None or process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def parse_args() -> argparse.Namespace:
    script = Path(__file__).resolve()
    repo_root = script.parents[3]
    build_root = Path(os.environ.get("BUILD_ROOT", "/var/tmp/ModSecurity-conector-verified/build"))
    component_cache = Path(
        os.environ.get(
            "CONNECTOR_COMPONENT_CACHE",
            "/var/tmp/ModSecurity-conector-verified/component-cache",
        )
    )
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--connector-binary",
        type=Path,
        default=Path(
            os.environ.get(
                "TRAEFIK_CONNECTOR_BIN",
                str(build_root / "traefik-connector/traefik-forwardauth"),
            )
        ),
    )
    parser.add_argument(
        "--traefik-binary",
        type=Path,
        default=Path(os.environ.get("TRAEFIK_BIN", str(component_cache / "traefik/bin/traefik"))),
    )
    parser.add_argument(
        "--config-template",
        type=Path,
        default=repo_root / "connectors/traefik/config/traefik-forwardauth.conf",
    )
    parser.add_argument(
        "--result-root",
        type=Path,
        default=Path(
            os.environ.get(
                "TRAEFIK_CONNECTOR_RESULT_ROOT",
                str(build_root / "traefik-connector/runtime-smoke"),
            )
        ),
    )
    return parser.parse_args()


def run(args: argparse.Namespace) -> int:
    repo_root = Path(__file__).resolve().parents[3]
    consume_no_crs_selected_cases(repo_root)
    result_root = Path(os.path.abspath(args.result_root))
    assert_no_symlink_components(result_root)
    assert_output_root(result_root, repo_root)
    result_path = result_root / "result.json"
    expected_rule_id = os.environ.get("MSCONNECTOR_EXPECTED_RULE_ID", "1000001")
    connector_binary = require_local_executable(args.connector_binary, "Traefik connector binary")
    traefik_binary = require_local_executable(args.traefik_binary, "Traefik binary")
    template = args.config_template.resolve()
    rules_file = Path(
        os.environ.get(
            "MSCONNECTOR_RULES_FILE",
            str(repo_root / "common/rules/modsecurity_targeted_smoke.conf"),
        )
    ).resolve()
    if not template.is_file():
        raise MissingDependency(f"connector config template is missing: {template}")
    if not rules_file.is_file():
        raise MissingDependency(f"targeted smoke rule is missing: {rules_file}")

    if result_root.exists():
        shutil.rmtree(result_root)
    result_root.mkdir(parents=True, exist_ok=True)
    log_dir = result_root / "logs"
    config_dir = result_root / "config"
    log_dir.mkdir(parents=True, exist_ok=True)
    config_dir.mkdir(parents=True, exist_ok=True)
    service_config = config_dir / "traefik-forwardauth.conf"
    traefik_config = config_dir / "traefik-dynamic.yml"
    event_path = log_dir / "events.jsonl"
    concrete_service_config(template, service_config, rules_file, event_path)

    upstream_port = free_port()
    auth_port = free_port()
    traefik_port = free_port()
    traefik_config.write_text(dynamic_config(upstream_port, auth_port), encoding="utf-8")

    upstream = http.server.ThreadingHTTPServer(("127.0.0.1", upstream_port), UpstreamHandler)
    upstream_thread = threading.Thread(target=upstream.serve_forever, daemon=True)
    upstream_thread.start()
    service_process: subprocess.Popen[bytes] | None = None
    traefik_process: subprocess.Popen[bytes] | None = None
    allowed_status: int | None = None
    blocked_status: int | None = None
    blocked_event: dict[str, object] | None = None

    service_stdout_path = log_dir / "service.stdout.log"
    service_stderr_path = log_dir / "service.stderr.log"
    traefik_stdout_path = log_dir / "traefik.stdout.log"
    traefik_stderr_path = log_dir / "traefik.stderr.log"
    traefik_access_path = log_dir / "traefik-access.log"
    try:
        check = subprocess.run(
            [str(connector_binary), "--check-config", "--config", str(service_config)],
            cwd=repo_root,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        (log_dir / "config-check.stdout.log").write_text(check.stdout, encoding="utf-8")
        (log_dir / "config-check.stderr.log").write_text(check.stderr, encoding="utf-8")
        if check.returncode != 0:
            raise RuntimeError(f"connector config check failed with code {check.returncode}")

        with service_stdout_path.open("wb") as service_stdout, service_stderr_path.open("wb") as service_stderr:
            service_process = subprocess.Popen(
                [
                    str(connector_binary),
                    "--serve",
                    "--config",
                    str(service_config),
                    "--listen",
                    f"127.0.0.1:{auth_port}",
                ],
                cwd=repo_root,
                stdout=service_stdout,
                stderr=service_stderr,
            )
            wait_for_tcp(auth_port, service_process, "Traefik forwardAuth service")

            command = [
                str(traefik_binary),
                f"--entryPoints.web.address=127.0.0.1:{traefik_port}",
                f"--providers.file.filename={traefik_config}",
                "--providers.file.watch=false",
                "--api=false",
                "--log.level=ERROR",
                "--global.sendAnonymousUsage=false",
                "--accesslog=true",
                f"--accesslog.filepath={traefik_access_path}",
            ]
            (config_dir / "traefik-command.txt").write_text(" ".join(command) + "\n", encoding="utf-8")
            with traefik_stdout_path.open("wb") as traefik_stdout, traefik_stderr_path.open("wb") as traefik_stderr:
                traefik_process = subprocess.Popen(
                    command,
                    cwd=repo_root,
                    stdout=traefik_stdout,
                    stderr=traefik_stderr,
                )
                wait_for_traefik(traefik_port, traefik_process)
                allowed_status = http_status(
                    f"http://127.0.0.1:{traefik_port}/allowed",
                    {"X-Request-Id": "traefik-forwardauth-allow"},
                )
                blocked_status = http_status(
                    f"http://127.0.0.1:{traefik_port}/blocked",
                    {
                        "X-Modsec-Smoke": "block",
                        "X-Request-Id": "traefik-forwardauth-block",
                    },
                )

        if allowed_status != 200 or blocked_status != 403:
            raise RuntimeError(
                f"unexpected Traefik statuses: allowed={allowed_status}, blocked={blocked_status}"
            )
        if service_process.poll() is not None:
            raise RuntimeError(f"forwardAuth service exited with code {service_process.returncode}")
        if traefik_process.poll() is not None:
            raise RuntimeError(f"Traefik exited with code {traefik_process.returncode}")
        blocked_event = verify_block_event(event_path, expected_rule_id)

        write_json(
            result_path,
            {
                "allowed_request_status": allowed_status,
                "blocked_request_status": blocked_status,
                "common_runtime_path_verified": True,
                "connector": "traefik",
                "connector_binary": str(connector_binary),
                "crs_complete": False,
                "event_path": str(event_path),
                "full_matrix_ready": False,
                "integration_mode": "forwardAuth",
                "intervention_status": 403,
                "modsecurity_rule_file": str(rules_file),
                "modsecurity_rule_id": str(blocked_event["rule_id"]),
                "modsecurity_rule_loaded": True,
                "production_ready": False,
                "request_body_verified": False,
                "response_body_verified": False,
                "response_processing_supported": False,
                "runtime_verified": True,
                "status": "PASS",
                "traefik_binary": str(traefik_binary),
            },
        )
        print(f"PASS: Traefik forwardAuth runtime smoke (200/403), result={result_path}")
        return 0
    except Exception as exc:
        write_json(
            result_path,
            {
                "allowed_request_status": allowed_status,
                "blocked_request_status": blocked_status,
                "common_runtime_path_verified": False,
                "connector": "traefik",
                "error": str(exc),
                "event_path": str(event_path),
                "integration_mode": "forwardAuth",
                "request_body_verified": False,
                "response_body_verified": False,
                "response_processing_supported": False,
                "runtime_verified": False,
                "status": "FAIL",
            },
        )
        print(f"FAIL: Traefik forwardAuth runtime smoke: {exc}", file=sys.stderr)
        return 1
    finally:
        stop_process(traefik_process)
        stop_process(service_process)
        upstream.shutdown()
        upstream.server_close()


def main() -> int:
    args = parse_args()
    try:
        return run(args)
    except MissingDependency as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 77


if __name__ == "__main__":
    raise SystemExit(main())
