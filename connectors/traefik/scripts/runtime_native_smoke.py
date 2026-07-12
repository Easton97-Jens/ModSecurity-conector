#!/usr/bin/env python3
"""Exercise the pinned Traefik local-plugin route without capability promotion.

The runner stages the repository-owned local plugin beneath Traefik's
``plugins-local`` workspace, starts the pinned binary with a File Provider,
and sends a body-bearing request through a router that explicitly selects the
plugin. The plugin currently owns only a passthrough Engine seam, so the
result deliberately does not assert Common/libmodsecurity rule evaluation,
Phase-4 enforcement, or no-full-buffering evidence.
"""

from __future__ import annotations

import contextlib
import http.client
import http.server
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


class MissingDependency(RuntimeError):
    """A required local host prerequisite is unavailable before execution."""


REPO_ROOT = Path(__file__).resolve().parents[3]
PLUGIN_SOURCE = REPO_ROOT / "connectors/traefik/native_middleware"
PLUGIN_ID = "modsecurityNative"
REQUEST_BODY = b"native-traefik-request-body"


def assert_no_symlink_components(path: Path) -> None:
    absolute = Path(os.path.abspath(path))
    current = Path(absolute.anchor)
    for component in absolute.parts[1:]:
        current /= component
        if current.is_symlink():
            raise MissingDependency(f"runtime path contains a symlink: {current}")
        if not current.exists():
            break


def assert_runtime_root(path: Path) -> Path:
    resolved = Path(os.path.abspath(path))
    if not resolved.is_absolute():
        raise MissingDependency("native runtime root must be absolute")
    if resolved in {Path("/"), Path("/tmp"), Path("/var"), Path("/var/tmp")}:
        raise MissingDependency(f"native runtime root is too broad: {resolved}")
    try:
        resolved.relative_to(REPO_ROOT)
    except ValueError:
        pass
    else:
        raise MissingDependency(f"native runtime root must be outside checkout: {resolved}")
    assert_no_symlink_components(resolved)
    return resolved


def require_local_executable(path: Path, label: str) -> Path:
    resolved = Path(os.path.abspath(path))
    if not resolved.is_absolute():
        raise MissingDependency(f"{label} must be an absolute local path")
    if str(resolved).startswith(("/usr/", "/bin/", "/sbin/", "/opt/")):
        raise MissingDependency(f"{label} must not use a global system path: {resolved}")
    if not resolved.is_file() or not os.access(resolved, os.X_OK):
        raise MissingDependency(f"{label} is not executable: {resolved}")
    return resolved


def free_port() -> int:
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def read_plugin_module(source: Path) -> str:
    go_mod = source / "go.mod"
    middleware = source / "middleware.go"
    metadata = source / ".traefik.yml"
    if not go_mod.is_file() or not middleware.is_file() or not metadata.is_file():
        raise MissingDependency(f"native plugin source is incomplete: {source}")
    for candidate in source.rglob("*"):
        if candidate.is_symlink():
            raise MissingDependency(f"native plugin source must not contain symlinks: {candidate}")
    module_match = re.search(r"(?m)^module\s+([^\s]+)\s*$", go_mod.read_text(encoding="utf-8"))
    package_match = re.search(
        r"(?m)^package\s+([A-Za-z_][A-Za-z0-9_]*)\s*$",
        middleware.read_text(encoding="utf-8"),
    )
    if module_match is None or package_match is None:
        raise MissingDependency("native plugin must declare a Go module and package")
    module_name = module_match.group(1)
    if module_name.rsplit("/", 1)[-1] != package_match.group(1):
        raise MissingDependency(
            "Traefik local-plugin package must match the final module-path component"
        )
    if f"import: {module_name}" not in metadata.read_text(encoding="utf-8"):
        raise MissingDependency("native plugin metadata import does not match go.mod")
    return module_name


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def wait_for_port(port: int, process: subprocess.Popen[bytes], label: str) -> None:
    deadline = time.monotonic() + 15
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
    raise RuntimeError(f"{label} did not listen on {port}: {last_error}")


def stop_process(process: subprocess.Popen[bytes] | None) -> bool:
    if process is None or process.poll() is not None:
        return True
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)
    return process.poll() is not None


@dataclass
class UpstreamState:
    request_count: int = 0
    request_body_bytes: int = 0
    response_chunks: int = 0
    lock: threading.Lock = field(default_factory=threading.Lock)


def upstream_handler(state: UpstreamState) -> type[http.server.BaseHTTPRequestHandler]:
    class Handler(http.server.BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def do_POST(self) -> None:  # noqa: N802 - HTTP server callback name
            expected = int(self.headers.get("Content-Length", "0"))
            seen = 0
            while seen < expected:
                chunk = self.rfile.read(min(4096, expected - seen))
                if not chunk:
                    break
                seen += len(chunk)
            chunks = (b"native-traefik-first-chunk\n", b"native-traefik-final-chunk\n")
            with state.lock:
                state.request_count += 1
                state.request_body_bytes += seen
                state.response_chunks += len(chunks)
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(sum(len(chunk) for chunk in chunks)))
            self.end_headers()
            for chunk in chunks:
                self.wfile.write(chunk)
                self.wfile.flush()

        def log_message(self, _format: str, *_args: object) -> None:
            # Request paths and body values are not useful evidence.
            return

    return Handler


def write_static_config(path: Path, dynamic_path: Path, port: int, module_name: str) -> None:
    path.write_text(
        "\n".join(
            (
                "entryPoints:",
                "  web:",
                f'    address: "127.0.0.1:{port}"',
                "providers:",
                "  file:",
                f'    filename: "{dynamic_path}"',
                "    watch: false",
                "experimental:",
                "  localPlugins:",
                f"    {PLUGIN_ID}:",
                f"      moduleName: {module_name}",
                "      settings:",
                "        envs: []",
                "global:",
                "  checkNewVersion: false",
                "  sendAnonymousUsage: false",
                "log:",
                "  level: INFO",
                "",
            )
        ),
        encoding="utf-8",
    )


def write_dynamic_config(path: Path, upstream_port: int) -> None:
    path.write_text(
        "\n".join(
            (
                "http:",
                "  routers:",
                "    native:",
                "      entryPoints: [web]",
                '      rule: "PathPrefix(`/`)"',
                "      middlewares: [native]",
                "      service: upstream",
                "  middlewares:",
                "    native:",
                "      plugin:",
                f"        {PLUGIN_ID}:",
                "          maxHeaderCount: 128",
                "          maxHeaderBytes: 65536",
                "          maxRequestChunkBytes: 32768",
                "          maxResponseChunkBytes: 32768",
                "          transactionIDHeader: X-Request-Id",
                "          engineMode: passthrough",
                "  services:",
                "    upstream:",
                "      loadBalancer:",
                "        servers:",
                f"          - url: http://127.0.0.1:{upstream_port}",
                "",
            )
        ),
        encoding="utf-8",
    )


def request_through_traefik(port: int) -> tuple[int, int]:
    deadline = time.monotonic() + 15
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        connection = http.client.HTTPConnection("127.0.0.1", port, timeout=2)
        try:
            connection.request(
                "POST",
                "/native",
                body=REQUEST_BODY,
                headers={"Content-Type": "text/plain", "X-Request-Id": "traefik-native-host"},
            )
            response = connection.getresponse()
            status = int(response.status)
            body_bytes = 0
            while True:
                chunk = response.read(4096)
                if not chunk:
                    break
                body_bytes += len(chunk)
            if status == 200:
                return status, body_bytes
            last_error = RuntimeError(f"native router returned unexpected status {status}")
        except (OSError, http.client.HTTPException) as exc:
            last_error = exc
        finally:
            connection.close()
        time.sleep(0.2)
    raise RuntimeError(f"native router did not complete a 200 request: {last_error}")


def traefik_version(binary: Path) -> str:
    completed = subprocess.run(
        [str(binary), "version"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if completed.returncode != 0:
        raise MissingDependency("could not determine pinned Traefik version")
    return next((line.strip() for line in completed.stdout.splitlines() if line.strip()), "unknown")


def run() -> int:
    runtime_root = assert_runtime_root(Path(os.environ.get("TRAEFIK_NATIVE_RUNTIME_ROOT", "")))
    binary = require_local_executable(Path(os.environ.get("TRAEFIK_BIN", "")), "Traefik binary")
    module_name = read_plugin_module(PLUGIN_SOURCE)
    if runtime_root.exists() and any(runtime_root.iterdir()):
        raise MissingDependency(f"native runtime root must be empty: {runtime_root}")
    runtime_root.mkdir(parents=True, exist_ok=True)
    plugin_destination = runtime_root / "plugins-local/src" / Path(module_name)
    plugin_destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(PLUGIN_SOURCE, plugin_destination)

    config_dir = runtime_root / "effective-config"
    logs_dir = runtime_root / "logs"
    config_dir.mkdir()
    logs_dir.mkdir()
    result_path = runtime_root / "result.json"
    static_config = config_dir / "traefik-native-static.yaml"
    dynamic_config = config_dir / "traefik-native-dynamic.yaml"
    upstream_port = free_port()
    traefik_port = free_port()
    write_static_config(static_config, dynamic_config, traefik_port, module_name)
    write_dynamic_config(dynamic_config, upstream_port)

    state = UpstreamState()
    upstream = http.server.ThreadingHTTPServer(("127.0.0.1", upstream_port), upstream_handler(state))
    upstream_thread = threading.Thread(target=upstream.serve_forever, daemon=True)
    upstream_thread.start()
    process: subprocess.Popen[bytes] | None = None
    stopped = False
    try:
        with (logs_dir / "traefik.stdout.log").open("wb") as stdout, (
            logs_dir / "traefik.stderr.log"
        ).open("wb") as stderr:
            process = subprocess.Popen(
                [str(binary), f"--configFile={static_config}"],
                cwd=runtime_root,
                stdout=stdout,
                stderr=stderr,
            )
            wait_for_port(traefik_port, process, "Traefik native local-plugin host")
            client_status, client_response_bytes = request_through_traefik(traefik_port)
            if process.poll() is not None:
                raise RuntimeError(f"Traefik exited after native request with code {process.returncode}")

        host_log = (logs_dir / "traefik.stdout.log").read_text(encoding="utf-8", errors="replace")
        plugin_loaded = "Plugins loaded." in host_log and PLUGIN_ID in host_log
        if not plugin_loaded:
            raise RuntimeError("Traefik did not confirm local-plugin loading")
        with state.lock:
            upstream_requests = state.request_count
            request_body_bytes = state.request_body_bytes
            response_chunks = state.response_chunks
        if upstream_requests < 1 or request_body_bytes < len(REQUEST_BODY) or response_chunks < 2:
            raise RuntimeError("native plugin route did not reach the streaming upstream contract")
        stopped = stop_process(process)
        process = None
        write_json(
            result_path,
            {
                "capability_promotion": "not_permitted",
                "client_response_bytes": client_response_bytes,
                "client_status": client_status,
                "common_runtime_bridge": False,
                "connector": "traefik",
                "engine_mode": "passthrough",
                "integration_mode": "native-traefik-middleware",
                "plugin_loaded": plugin_loaded,
                "plugin_module": module_name,
                "processes_stopped": stopped,
                "production_ready": False,
                "request_body_bytes_observed": request_body_bytes,
                "response_chunks_observed": response_chunks,
                "rule_evaluation": "not_wired",
                "status": "PASS",
                "traefik_version": traefik_version(binary),
                "upstream_requests": upstream_requests,
            },
        )
        return 0
    except Exception as exc:
        stopped = stop_process(process)
        write_json(
            result_path,
            {
                "common_runtime_bridge": False,
                "connector": "traefik",
                "engine_mode": "passthrough",
                "error_class": type(exc).__name__,
                "integration_mode": "native-traefik-middleware",
                "processes_stopped": stopped,
                "production_ready": False,
                "rule_evaluation": "not_wired",
                "status": "FAIL",
            },
        )
        print(f"FAIL: Traefik native local-plugin host: {type(exc).__name__}", file=sys.stderr)
        return 1
    finally:
        stop_process(process)
        upstream.shutdown()
        upstream.server_close()


def main() -> int:
    try:
        return run()
    except MissingDependency as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 77


if __name__ == "__main__":  # pragma: no cover - command entry point
    raise SystemExit(main())
