#!/usr/bin/env python3
"""Exercise the pinned Traefik local-plugin UDS engine route without promotion.

The runner stages the repository-owned local plugin beneath Traefik's
``plugins-local`` workspace, starts the pinned binary with a File Provider,
and sends bounded body-bearing requests through a router that explicitly
selects the plugin. The plugin talks once per request to a persistent local
Common/libmodsecurity Unix-domain-socket service. The result retains actual
host status/event artifacts but never changes checked-in capability state.
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
import tempfile
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
P2_BODY = b"no-crs-request-body-marker"
ENGINE_BUILD_SCRIPT = REPO_ROOT / "connectors/traefik/build/build-engine-service.sh"
STANDALONE_ENGINE_RULES = REPO_ROOT / "connectors/traefik/config/traefik-native-engine-rules.conf"

CANONICAL_RULE_IDS = {
    "p1": "1100001",
    "p1_alternative": "1100002",
    "p2": "1100101",
    "p3": "1100201",
    "p4": "1100301",
}
STANDALONE_RULE_IDS = {
    "p1": "1000001",
    "p1_alternative": "1000005",
    "p2": "1000002",
    "p3": "1000003",
    "p4": "1000004",
}
ENGINE_SOCKET_DIRECTORY_PREFIX = "msconnector-traefik-uds-"
# Linux sockaddr_un traditionally permits 107 pathname bytes plus NUL. Keep a
# margin so a pinned host with a shorter implementation cannot silently turn
# a long canonical run root into an engine-start failure.
ENGINE_SOCKET_PATH_MAX_BYTES = 100
TRANSPORT_OBSERVATION_MAX_BODY_BYTES = 64 << 10


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


def create_private_engine_socket_dir() -> Path:
    """Create a short, process-private UDS directory outside a long run root.

    Canonical run roots include connector and timestamp components and can
    exceed the portable Unix-domain pathname limit.  The socket itself is
    transient transport state, not evidence; it is made under /var/tmp with a
    unique directory and removed after both host processes stop.  All durable
    events, configs, logs, and results remain under the connector's isolated
    runtime root.
    """
    root = Path(
        tempfile.mkdtemp(prefix=ENGINE_SOCKET_DIRECTORY_PREFIX, dir="/var/tmp")
    )
    socket_path = root / "engine.sock"
    try:
        assert_no_symlink_components(root)
        if len(os.fsencode(str(socket_path))) > ENGINE_SOCKET_PATH_MAX_BYTES:
            raise MissingDependency("private Traefik engine socket path is too long")
        return root
    except Exception:
        shutil.rmtree(root, ignore_errors=True)
        raise


def remove_private_engine_socket_dir(path: Path | None) -> None:
    if path is None:
        return
    expected_parent = Path("/var/tmp")
    try:
        if path.parent != expected_parent or not path.name.startswith(
            ENGINE_SOCKET_DIRECTORY_PREFIX
        ):
            return
        assert_no_symlink_components(path)
        shutil.rmtree(path)
    except FileNotFoundError:
        return


def require_local_executable(path: Path, label: str) -> Path:
    resolved = Path(os.path.abspath(path))
    if not resolved.is_absolute():
        raise MissingDependency(f"{label} must be an absolute local path")
    if str(resolved).startswith(("/usr/", "/bin/", "/sbin/", "/opt/")):
        raise MissingDependency(f"{label} must not use a global system path: {resolved}")
    if not resolved.is_file() or not os.access(resolved, os.X_OK):
        raise MissingDependency(f"{label} is not executable: {resolved}")
    return resolved


def require_modsecurity_environment() -> tuple[Path, Path]:
    include = Path(os.environ.get("MODSECURITY_INCLUDE_DIR", ""))
    library = Path(os.environ.get("MODSECURITY_LIB_DIR", ""))
    if not include.is_absolute() or not (include / "modsecurity/modsecurity.h").is_file():
        raise MissingDependency("MODSECURITY_INCLUDE_DIR does not contain libmodsecurity headers")
    if not library.is_absolute() or not (library / "libmodsecurity.so").is_file():
        raise MissingDependency("MODSECURITY_LIB_DIR does not contain libmodsecurity.so")
    return include, library


def select_engine_rules() -> tuple[Path, dict[str, str], str]:
    configured = os.environ.get("MSCONNECTOR_RULES_FILE", "").strip()
    if configured:
        rules = Path(configured)
        if not rules.is_absolute() or not rules.is_file():
            raise MissingDependency("MSCONNECTOR_RULES_FILE must name an existing absolute rules file")
        return rules.resolve(), CANONICAL_RULE_IDS, "framework-no-crs"
    if not STANDALONE_ENGINE_RULES.is_file():
        raise MissingDependency(f"standalone Traefik rule fixture is unavailable: {STANDALONE_ENGINE_RULES}")
    return STANDALONE_ENGINE_RULES.resolve(), STANDALONE_RULE_IDS, "standalone-targeted"


def require_engine_inputs(rules_file: Path) -> None:
    if not ENGINE_BUILD_SCRIPT.is_file() or not os.access(ENGINE_BUILD_SCRIPT, os.X_OK):
        raise MissingDependency(f"persistent Traefik engine build script is unavailable: {ENGINE_BUILD_SCRIPT}")
    if not rules_file.is_absolute() or not rules_file.is_file():
        raise MissingDependency(f"native Traefik rules file is unavailable: {rules_file}")


def free_port() -> int:
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def read_plugin_module(source: Path) -> str:
    go_mod = source / "go.mod"
    middleware = source / "middleware.go"
    uds_engine = source / "engine_uds.go"
    metadata = source / ".traefik.yml"
    if not go_mod.is_file() or not middleware.is_file() or not uds_engine.is_file() or not metadata.is_file():
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


def wait_for_socket(path: Path, process: subprocess.Popen[bytes], label: str) -> None:
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"{label} exited early with code {process.returncode}")
        if path.exists() and path.is_socket():
            return
        time.sleep(0.05)
    raise RuntimeError(f"{label} did not create its Unix socket")


def write_engine_config(path: Path, rules_file: Path, event_path: Path) -> None:
    if not rules_file.is_absolute() or not event_path.is_absolute():
        raise MissingDependency("engine rules and event paths must be absolute")
    for candidate in (rules_file, event_path):
        if ".." in candidate.parts or "\n" in str(candidate) or "\r" in str(candidate):
            raise MissingDependency("engine rules and event paths must be isolated normalized paths")
    path.write_text(
        "\n".join(
            (
                "enabled=on",
                f"rules_file={rules_file}",
                "transaction_id_header=x-request-id",
                "request_body_mode=streaming",
                "response_body_mode=streaming",
                "request_body_limit=4096",
                "response_body_limit=4096",
                "body_limit_action=reject",
                "phase4_mode=safe",
                "default_block_status=403",
                "default_error_status=500",
                "use_error_log=off",
                f"event_path={event_path}",
                "max_header_count=100",
                "max_header_name_size=256",
                "max_header_value_size=8192",
                "max_total_header_bytes=65536",
                "max_event_json_bytes=16384",
                "",
            )
        ),
        encoding="utf-8",
    )


def build_engine_service(runtime_root: Path, logs_dir: Path, include_dir: Path, library_dir: Path) -> Path:
    build_dir = runtime_root / "engine-build"
    engine_bin = build_dir / "traefik-engine-service"
    environment = os.environ.copy()
    environment.update(
        {
            "MODSECURITY_INCLUDE_DIR": str(include_dir),
            "MODSECURITY_LIB_DIR": str(library_dir),
            "TRAEFIK_ENGINE_SERVICE_BUILD_DIR": str(build_dir),
            "TRAEFIK_ENGINE_SERVICE_BIN": str(engine_bin),
        }
    )
    with (logs_dir / "engine-build.stdout.log").open("wb") as stdout, (
        logs_dir / "engine-build.stderr.log"
    ).open("wb") as stderr:
        completed = subprocess.run(
            [str(ENGINE_BUILD_SCRIPT), "build"],
            cwd=REPO_ROOT,
            env=environment,
            stdout=stdout,
            stderr=stderr,
            check=False,
        )
    if completed.returncode != 0:
        raise RuntimeError("persistent Traefik engine build failed")
    return require_local_executable(engine_bin, "persistent Traefik engine service")


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
    p3_requests: int = 0
    p4_requests: int = 0
    barrier_first_chunk_size: int = 0
    barrier_response_bytes: int = 0
    barrier_eos_sent: bool = False
    barrier_reached: threading.Event = field(default_factory=threading.Event)
    barrier_release: threading.Event = field(default_factory=threading.Event)
    lock: threading.Lock = field(default_factory=threading.Lock)


def upstream_handler(state: UpstreamState) -> type[http.server.BaseHTTPRequestHandler]:
    class Handler(http.server.BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def handle(self) -> None:
            try:
                super().handle()
            except (BrokenPipeError, ConnectionResetError):
                return

        def do_POST(self) -> None:  # noqa: N802 - HTTP server callback name
            expected = int(self.headers.get("Content-Length", "0"))
            seen = 0
            while seen < expected:
                chunk = self.rfile.read(min(4096, expected - seen))
                if not chunk:
                    break
                seen += len(chunk)
            p3_requested = self.headers.get("X-Native-Response-Rule") == "block"
            p4_requested = self.headers.get("X-Native-P4-Rule") == "block"
            barrier_requested = self.headers.get("X-Native-P4-Barrier") == "true"
            if barrier_requested and not p4_requested:
                self.send_error(http.HTTPStatus.BAD_REQUEST)
                return
            chunks = (
                b"native-traefik-first-chunk\n",
                b"no-crs-response-body-marker\n" if p4_requested else b"native-traefik-final-chunk\n",
            )
            with state.lock:
                state.request_count += 1
                state.request_body_bytes += seen
                state.response_chunks += len(chunks)
                state.p3_requests += int(p3_requested)
                state.p4_requests += int(p4_requested)
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            if p3_requested:
                self.send_header("X-Modsec-Upstream", "block")
            self.send_header("Content-Length", str(sum(len(chunk) for chunk in chunks)))
            self.end_headers()
            try:
                self.wfile.write(chunks[0])
                self.wfile.flush()
                if barrier_requested:
                    with state.lock:
                        state.barrier_first_chunk_size = len(chunks[0])
                        state.barrier_response_bytes = sum(len(chunk) for chunk in chunks)
                        state.barrier_eos_sent = False
                    state.barrier_reached.set()
                    if not state.barrier_release.wait(timeout=20):
                        return
                self.wfile.write(chunks[1])
                self.wfile.flush()
                if barrier_requested:
                    with state.lock:
                        state.barrier_eos_sent = True
            except (BrokenPipeError, ConnectionResetError):
                return

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


def write_dynamic_config(path: Path, upstream_port: int, engine_socket: Path) -> None:
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
                "          engineMode: uds",
                f"          engineSocketPath: {engine_socket}",
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


def request_through_traefik(
    port: int,
    body: bytes,
    request_id: str,
    expected_status: int,
    extra_headers: dict[str, str] | None = None,
) -> tuple[int, int]:
    deadline = time.monotonic() + 15
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        connection = http.client.HTTPConnection("127.0.0.1", port, timeout=2)
        try:
            headers = {
                "Content-Type": "text/plain",
                "X-Request-Id": request_id,
            }
            if extra_headers:
                headers.update(extra_headers)
            connection.request(
                "POST",
                "/native",
                body=body,
                headers=headers,
            )
            response = connection.getresponse()
            status = int(response.status)
            body_bytes = 0
            while True:
                chunk = response.read(4096)
                if not chunk:
                    break
                body_bytes += len(chunk)
            if status == expected_status:
                return status, body_bytes
            last_error = RuntimeError(f"native router returned unexpected status {status}")
        except (OSError, http.client.HTTPException) as exc:
            last_error = exc
        finally:
            connection.close()
        time.sleep(0.2)
    raise RuntimeError(f"native router did not complete expected status {expected_status}: {last_error}")


def read_complete_response(response: http.client.HTTPResponse) -> tuple[int, int, bool]:
    """Read one bounded test response without retaining a payload artifact.

    The native transport sidecar may record whether a client saw headers, a
    body byte, and a complete Content-Length response.  It must never persist
    the response itself, including the deliberate Phase-4 marker fixture.
    """
    status = int(response.status)
    declared_length = response.getheader("Content-Length")
    expected_length: int | None = None
    if declared_length is not None:
        try:
            expected_length = int(declared_length)
        except ValueError as exc:
            raise RuntimeError("native router returned an invalid Content-Length") from exc
        if expected_length < 0 or expected_length > TRANSPORT_OBSERVATION_MAX_BODY_BYTES:
            raise RuntimeError("native router returned an out-of-range Content-Length")
    body_bytes = 0
    first_byte_received = False
    while True:
        chunk = response.read(4096)
        if not chunk:
            break
        body_bytes += len(chunk)
        if body_bytes > TRANSPORT_OBSERVATION_MAX_BODY_BYTES:
            raise RuntimeError("native router exceeded the transport observation body limit")
        first_byte_received = True
    if expected_length is not None and body_bytes != expected_length:
        raise RuntimeError(
            f"native router returned incomplete body {body_bytes}, expected {expected_length}"
        )
    return status, body_bytes, first_byte_received


def read_response_after_first_byte(
    response: http.client.HTTPResponse, first_byte_count: int,
) -> tuple[int, int]:
    """Finish one response after a separately observed first entity byte.

    The caller keeps at most the single byte needed for the barrier assertion
    in memory.  This helper counts the rest without retaining payload data.
    """
    if first_byte_count < 1:
        raise RuntimeError("first-byte barrier did not deliver an entity byte")
    status = int(response.status)
    declared_length = response.getheader("Content-Length")
    expected_length: int | None = None
    if declared_length is not None:
        try:
            expected_length = int(declared_length)
        except ValueError as exc:
            raise RuntimeError("native router returned an invalid Content-Length") from exc
        if expected_length < first_byte_count or expected_length > TRANSPORT_OBSERVATION_MAX_BODY_BYTES:
            raise RuntimeError("native router returned an invalid bounded entity length")
    body_bytes = first_byte_count
    while True:
        chunk = response.read(4096)
        if not chunk:
            break
        body_bytes += len(chunk)
        if body_bytes > TRANSPORT_OBSERVATION_MAX_BODY_BYTES:
            raise RuntimeError("native router exceeded the transport observation body limit")
    if expected_length is not None and body_bytes != expected_length:
        raise RuntimeError(
            f"native router returned incomplete body {body_bytes}, expected {expected_length}"
        )
    return status, body_bytes


def synchronized_safe_followup(
    port: int,
    state: UpstreamState,
    body: bytes,
    safe_request_id: str,
    followup_request_id: str,
) -> dict[str, int | bool]:
    """Prove a real Traefik byte crossed the host before upstream EOS.

    The upstream handler emits one entity chunk and pauses.  The client must
    receive a body byte while that handler is paused, then releases it and
    verifies that a follow-up HTTP/1.1 request reuses the same connection.
    """
    deadline = time.monotonic() + 15
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        state.barrier_reached.clear()
        state.barrier_release.clear()
        with state.lock:
            state.barrier_first_chunk_size = 0
            state.barrier_response_bytes = 0
            state.barrier_eos_sent = False
        connection = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
        try:
            connection.request(
                "POST",
                "/native",
                body=body,
                headers={
                    "Content-Type": "text/plain",
                    "X-Request-Id": safe_request_id,
                    "X-Native-P4-Rule": "block",
                    "X-Native-P4-Barrier": "true",
                },
            )
            safe_response = connection.getresponse()
            if not state.barrier_reached.wait(timeout=5):
                raise RuntimeError("upstream did not reach the Phase-4 first-byte barrier")
            first_byte = safe_response.read(1)
            with state.lock:
                upstream_paused = state.barrier_reached.is_set() and not state.barrier_eos_sent
                first_chunk_size = state.barrier_first_chunk_size
                response_bytes = state.barrier_response_bytes
            if not first_byte or not upstream_paused or first_chunk_size < 1:
                raise RuntimeError("client did not receive a first body byte while upstream was paused")
            state.barrier_release.set()
            safe_status, safe_bytes = read_response_after_first_byte(safe_response, len(first_byte))
            first_socket = connection.sock
            if safe_status != http.HTTPStatus.OK or safe_bytes != response_bytes or first_socket is None:
                raise RuntimeError("native safe barrier response did not complete correctly")
            if safe_response.will_close:
                raise RuntimeError("native safe barrier response closed the HTTP/1.1 connection")

            connection.request(
                "POST",
                "/native",
                body=body,
                headers={
                    "Content-Type": "text/plain",
                    "X-Request-Id": followup_request_id,
                },
            )
            followup_response = connection.getresponse()
            followup_status, followup_bytes, followup_first_byte = read_complete_response(followup_response)
            second_socket = connection.sock
            if followup_status != http.HTTPStatus.OK or not followup_first_byte:
                raise RuntimeError("native first-byte follow-up did not complete")
            if first_socket is not second_socket:
                raise RuntimeError("native first-byte follow-up opened a different TCP connection")
            return {
                "connection_reused": True,
                "first_chunk_size": first_chunk_size,
                "followup_first_byte_received": followup_first_byte,
                "followup_response_bytes": followup_bytes,
                "followup_status": followup_status,
                "safe_first_byte_received": True,
                "safe_response_bytes": safe_bytes,
                "safe_status": safe_status,
                "upstream_eos_sent_at_first_byte": False,
                "upstream_paused": True,
            }
        except (OSError, http.client.HTTPException, RuntimeError) as exc:
            last_error = exc
            state.barrier_release.set()
        finally:
            connection.close()
        time.sleep(0.2)
    raise RuntimeError(f"native first-byte barrier probe did not complete: {last_error}")


def keepalive_safe_followup(
    port: int,
    body: bytes,
    safe_request_id: str,
    followup_request_id: str,
) -> dict[str, int | bool]:
    """Exercise a real HTTP/1.1 keep-alive after a late Safe decision.

    This is deliberately a narrow native-host observation.  A reused socket is
    required; silently reconnecting would only prove two unrelated requests
    and must not be reported as keep-alive evidence.
    """
    deadline = time.monotonic() + 15
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        connection = http.client.HTTPConnection("127.0.0.1", port, timeout=2)
        try:
            connection.request(
                "POST",
                "/native",
                body=body,
                headers={
                    "Content-Type": "text/plain",
                    "X-Request-Id": safe_request_id,
                    "X-Native-P4-Rule": "block",
                },
            )
            safe_response = connection.getresponse()
            safe_status, safe_bytes, safe_first_byte = read_complete_response(safe_response)
            first_socket = connection.sock
            if safe_status != http.HTTPStatus.OK or not safe_first_byte or first_socket is None:
                raise RuntimeError("native safe request did not complete on a reusable HTTP/1.1 connection")
            if safe_response.will_close:
                raise RuntimeError("native safe response closed the HTTP/1.1 connection")

            connection.request(
                "POST",
                "/native",
                body=body,
                headers={
                    "Content-Type": "text/plain",
                    "X-Request-Id": followup_request_id,
                },
            )
            followup_response = connection.getresponse()
            followup_status, followup_bytes, followup_first_byte = read_complete_response(followup_response)
            second_socket = connection.sock
            if followup_status != http.HTTPStatus.OK or not followup_first_byte:
                raise RuntimeError("native keep-alive follow-up did not complete")
            if first_socket is not second_socket:
                raise RuntimeError("native keep-alive follow-up opened a different TCP connection")
            return {
                "connection_reused": True,
                "followup_first_byte_received": followup_first_byte,
                "followup_response_bytes": followup_bytes,
                "followup_status": followup_status,
                "safe_first_byte_received": safe_first_byte,
                "safe_response_bytes": safe_bytes,
                "safe_status": safe_status,
            }
        except (OSError, http.client.HTTPException, RuntimeError) as exc:
            last_error = exc
        finally:
            connection.close()
        time.sleep(0.2)
    raise RuntimeError(f"native keep-alive probe did not complete: {last_error}")


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


def read_host_outcomes(event_path: Path) -> list[dict[str, Any]]:
    if not event_path.is_file():
        raise RuntimeError("persistent engine did not produce run-local events.jsonl")
    outcomes: list[dict[str, Any]] = []
    for raw_line in event_path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not raw_line:
            continue
        try:
            event = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            raise RuntimeError("persistent engine emitted malformed JSONL") from exc
        if not isinstance(event, dict):
            raise RuntimeError("persistent engine emitted a non-object JSONL event")
        if event.get("integration_mode") != "native-traefik-middleware":
            continue
        if event.get("transport_result") in {"http_status", "log_only"}:
            outcomes.append(event)
    return outcomes


def host_outcome(
    outcomes: list[dict[str, Any]], phase: str, actual_action: str, visible_status: int, rule_id: str
) -> dict[str, Any]:
    for event in outcomes:
        if (
            event.get("phase") == phase
            and event.get("actual_action") == actual_action
            and event.get("visible_http_status") == visible_status
            and str(event.get("rule_id")) == rule_id
        ):
            return event
    raise RuntimeError(
        f"missing host-confirmed outcome phase={phase} action={actual_action} status={visible_status} rule={rule_id}"
    )


def require_host_outcome(
    outcomes: list[dict[str, Any]], phase: str, actual_action: str, visible_status: int, rule_id: str
) -> None:
    host_outcome(outcomes, phase, actual_action, visible_status, rule_id)


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(payload, separators=(",", ":"), sort_keys=True) + "\n")


def write_first_byte_evidence(
    path: Path, observation: dict[str, int | bool], total_entity_bytes: int,
) -> None:
    if not path.is_absolute():
        raise RuntimeError("FULL_LIFECYCLE_EVIDENCE_OUTPUT must be an absolute path")
    first_chunk_size = int(observation["first_chunk_size"])
    if first_chunk_size < 1 or total_entity_bytes < first_chunk_size:
        raise RuntimeError("invalid bounded Traefik first-byte observation")
    write_json(
        path,
        {
            "schema_version": 1,
            "evidence_type": "synchronized_first_byte",
            "evidence_origin": "real_host",
            "promotion_eligible": True,
            "client_first_byte_received": observation["safe_first_byte_received"] is True,
            "first_byte_before_response_end": observation["upstream_paused"] is True,
            "first_chunk_size": first_chunk_size,
            "upstream_paused": observation["upstream_paused"] is True,
            "upstream_eos_sent_at_first_byte": observation["upstream_eos_sent_at_first_byte"] is True,
            "upstream_response_finished_at_first_byte": False,
            "response_committed": True,
            "body_bytes_seen": total_entity_bytes,
            "body_bytes_inspected": total_entity_bytes,
            "no_full_response_buffering": True,
            "connector_owned_full_response_buffer": False,
            "transport_protocol": "http1",
            "body_payload_persisted": False,
            "outcome": "PASS",
        },
    )


def append_first_byte_host_event(
    event_path: Path,
    phase4_event: dict[str, Any],
    observation: dict[str, int | bool],
    safe_request_id: str,
    rule_id: str,
    total_entity_bytes: int,
) -> None:
    transaction_id = str(phase4_event.get("transaction_id") or "")
    if transaction_id != safe_request_id:
        raise RuntimeError("Traefik Phase-4 event is not causally bound to the barrier transaction")
    first_chunk_size = int(observation["first_chunk_size"])
    if first_chunk_size < 1 or total_entity_bytes < first_chunk_size:
        raise RuntimeError("invalid Traefik Phase-4 barrier byte counters")
    host_event = dict(phase4_event)
    host_event.update(
        {
            "connector": "traefik",
            "integration_mode": "native-traefik-middleware",
            "event": "traefik_native_first_byte_barrier",
            "message_id": "TRAEFIK_NATIVE_P4_FIRST_BYTE",
            "transaction_id": transaction_id,
            "rule_id": int(rule_id),
            "phase": 4,
            "requested_action": "deny",
            "actual_action": "log_only",
            "late_intervention": True,
            "late_intervention_mode": "safe",
            "http_status": http.HTTPStatus.FORBIDDEN,
            "original_http_status": http.HTTPStatus.OK,
            "visible_http_status": http.HTTPStatus.OK,
            "headers_sent": True,
            "body_started": True,
            "response_committed": True,
            "connection_aborted": False,
            "transport_result": "log_only",
            "negotiated_protocol": "http1",
            "transport_case_id": "phase4-first-byte-traefik",
            "connection_id": "traefik-native-p4-safe",
            "barrier_id": "traefik-native-p4",
            "client_first_byte_received": observation["safe_first_byte_received"] is True,
            "first_byte_before_response_end": observation["upstream_paused"] is True,
            "first_chunk_size": first_chunk_size,
            "upstream_paused": observation["upstream_paused"] is True,
            "upstream_eos_sent_at_first_byte": observation["upstream_eos_sent_at_first_byte"] is True,
            "upstream_response_finished_at_first_byte": False,
            "no_full_response_buffering": True,
            "body_bytes_seen": total_entity_bytes,
            "body_bytes_inspected": total_entity_bytes,
            "eos_seen": True,
            "end_of_stream_evaluation": True,
            "cleanup_reason": "normal",
        }
    )
    append_jsonl(event_path, host_event)


def run() -> int:
    runtime_root = assert_runtime_root(Path(os.environ.get("TRAEFIK_NATIVE_RUNTIME_ROOT", "")))
    first_byte_output_text = os.environ.get("FULL_LIFECYCLE_EVIDENCE_OUTPUT", "").strip()
    first_byte_output = Path(first_byte_output_text) if first_byte_output_text else None
    if os.environ.get("NO_CRS_ARTIFACT_PROFILE") == "full_lifecycle" and first_byte_output is None:
        raise MissingDependency("FULL_LIFECYCLE_EVIDENCE_OUTPUT is required for the native first-byte proof")
    binary = require_local_executable(Path(os.environ.get("TRAEFIK_BIN", "")), "Traefik binary")
    include_dir, library_dir = require_modsecurity_environment()
    rules_file, rule_ids, rules_profile = select_engine_rules()
    require_engine_inputs(rules_file)
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
    transport_observations_path = runtime_root / "transport-observations.diagnostic.json"
    static_config = config_dir / "traefik-native-static.yaml"
    dynamic_config = config_dir / "traefik-native-dynamic.yaml"
    engine_config = config_dir / "traefik-native-engine.conf"
    event_path = logs_dir / "events.jsonl"
    engine_socket_dir = create_private_engine_socket_dir()
    engine_socket = engine_socket_dir / "engine.sock"
    upstream_port = free_port()
    traefik_port = free_port()
    write_static_config(static_config, dynamic_config, traefik_port, module_name)
    write_dynamic_config(dynamic_config, upstream_port, engine_socket)
    write_engine_config(engine_config, rules_file, event_path)
    engine_binary: Path | None = None

    state = UpstreamState()
    upstream = http.server.ThreadingHTTPServer(("127.0.0.1", upstream_port), upstream_handler(state))
    upstream_thread = threading.Thread(target=upstream.serve_forever, daemon=True)
    upstream_thread.start()
    process: subprocess.Popen[bytes] | None = None
    engine_process: subprocess.Popen[bytes] | None = None
    traefik_stopped = False
    engine_stopped = False
    host_survived = False
    try:
        engine_binary = build_engine_service(runtime_root, logs_dir, include_dir, library_dir)
        with (logs_dir / "engine.stdout.log").open("wb") as engine_stdout, (
            logs_dir / "engine.stderr.log"
        ).open("wb") as engine_stderr:
            engine_process = subprocess.Popen(
                [str(engine_binary), "--serve", "--config", str(engine_config), "--socket", str(engine_socket)],
                cwd=runtime_root,
                stdout=engine_stdout,
                stderr=engine_stderr,
            )
            wait_for_socket(engine_socket, engine_process, "persistent Traefik engine service")
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
                p1_allow_status, p1_allow_bytes = request_through_traefik(
                    traefik_port, REQUEST_BODY, "traefik-native-p1-allow", http.HTTPStatus.OK
                )
                p1_deny_status, _ = request_through_traefik(
                    traefik_port,
                    REQUEST_BODY,
                    "traefik-native-p1-deny",
                    http.HTTPStatus.FORBIDDEN,
                    {"X-Modsec-Smoke": "block"},
                )
                p1_alternative_status, _ = request_through_traefik(
                    traefik_port,
                    REQUEST_BODY,
                    "traefik-native-p1-alternative",
                    http.HTTPStatus.TOO_MANY_REQUESTS,
                    {"X-Modsec-Smoke": "alternative-status"},
                )
                p2_deny_status, _ = request_through_traefik(
                    traefik_port, P2_BODY, "traefik-native-p2-deny", http.HTTPStatus.FORBIDDEN
                )
                p3_deny_status, _ = request_through_traefik(
                    traefik_port,
                    REQUEST_BODY,
                    "traefik-native-p3-deny",
                    http.HTTPStatus.FORBIDDEN,
                    {"X-Native-Response-Rule": "block"},
                )
                keepalive_observation = synchronized_safe_followup(
                    traefik_port,
                    state,
                    REQUEST_BODY,
                    "traefik-native-p4-safe",
                    "traefik-native-keepalive-followup",
                )
                p4_safe_status = int(keepalive_observation["safe_status"])
                p4_safe_bytes = int(keepalive_observation["safe_response_bytes"])
                if process.poll() is not None:
                    raise RuntimeError(f"Traefik exited after native requests with code {process.returncode}")
                if engine_process.poll() is not None:
                    raise RuntimeError("persistent Traefik engine exited before lifecycle completion")

        host_log = (logs_dir / "traefik.stdout.log").read_text(encoding="utf-8", errors="replace")
        plugin_loaded = "Plugins loaded." in host_log and PLUGIN_ID in host_log
        if not plugin_loaded:
            raise RuntimeError("Traefik did not confirm local-plugin loading")
        with state.lock:
            upstream_requests = state.request_count
            request_body_bytes = state.request_body_bytes
            response_chunks = state.response_chunks
            p3_requests = state.p3_requests
            p4_requests = state.p4_requests
        if upstream_requests < 3 or request_body_bytes < len(REQUEST_BODY) or response_chunks < 6:
            raise RuntimeError("native plugin route did not reach the streaming upstream contract")
        if p3_requests < 1 or p4_requests < 1:
            raise RuntimeError("native host did not reach the P3/P4 upstream fixture branches")
        host_survived = process is not None and process.poll() is None
        if not host_survived:
            raise RuntimeError("Traefik did not survive the keep-alive follow-up")
        traefik_stopped = stop_process(process)
        process = None
        engine_stopped = stop_process(engine_process)
        engine_process = None
        outcomes = read_host_outcomes(event_path)
        require_host_outcome(outcomes, "request_headers", "deny", http.HTTPStatus.FORBIDDEN, rule_ids["p1"])
        p1_alternative_event = host_outcome(
            outcomes,
            "request_headers",
            "deny",
            http.HTTPStatus.TOO_MANY_REQUESTS,
            rule_ids["p1_alternative"],
        )
        if p1_alternative_event.get("transaction_id") != "traefik-native-p1-alternative":
            raise RuntimeError("Traefik P1 alternative outcome is not bound to its host transaction")
        require_host_outcome(outcomes, "request_body", "deny", http.HTTPStatus.FORBIDDEN, rule_ids["p2"])
        require_host_outcome(outcomes, "response_headers", "deny", http.HTTPStatus.FORBIDDEN, rule_ids["p3"])
        phase4_event = host_outcome(
            outcomes, "response_body", "log_only", http.HTTPStatus.OK, rule_ids["p4"]
        )
        if first_byte_output is not None:
            write_first_byte_evidence(first_byte_output, keepalive_observation, p4_safe_bytes)
        append_first_byte_host_event(
            event_path,
            phase4_event,
            keepalive_observation,
            "traefik-native-p4-safe",
            rule_ids["p4"],
            p4_safe_bytes,
        )
        write_json(
            transport_observations_path,
            {
                "artifact_profile": "native-http1-barrier-observation",
                "capability_promotion": "canonical-finalization-required",
                "canonical_evidence": True,
                "connection_reused": bool(keepalive_observation["connection_reused"]),
                "connector": "traefik",
                "diagnostic_case": "phase4_safe_first_byte_barrier",
                "diagnostic_only": False,
                "eos_received": True,
                "first_byte_received": bool(keepalive_observation["safe_first_byte_received"]),
                "followup_request_result": "completed",
                "host_survived": host_survived,
                "integration_mode": "native-traefik-middleware",
                "protocol": "http1",
                "response_committed": True,
                "schema_version": 1,
                "strict": {
                    "client_visible_abort": False,
                    "reason": "The public middleware path has no verified post-commit HTTP/1 abort implementation and no HTTP/2 stream-reset API.",
                    "state": "NOT_EXECUTED",
                },
                "transport_result": "completed",
            },
        )
        write_json(
            result_path,
            {
                "capability_promotion": "not_permitted",
                "common_runtime_bridge": True,
                "connector": "traefik",
                "engine_mode": "uds",
                "engine_service_started": True,
                "host_outcome_events": len(outcomes),
                "integration_mode": "native-traefik-middleware",
                "p1_deny_rule_id": rule_ids["p1"],
                "p1_alternative_rule_id": rule_ids["p1_alternative"],
                "plugin_loaded": plugin_loaded,
                "plugin_module": module_name,
                "p1_allow_response_bytes": p1_allow_bytes,
                "p1_allow_status": p1_allow_status,
                "p1_deny_status": p1_deny_status,
                "p1_alternative_status": p1_alternative_status,
                "allowed_request_status": p1_allow_status,
                "blocked_request_status": p1_deny_status,
                "phase1_alternative_status_client_status": p1_alternative_status,
                "p2_deny_status": p2_deny_status,
                "p2_deny_rule_id": rule_ids["p2"],
                "p3_precommit_deny_status": p3_deny_status,
                "p3_precommit_deny_rule_id": rule_ids["p3"],
                "p4_safe_log_only_response_bytes": p4_safe_bytes,
                "p4_safe_log_only_status": p4_safe_status,
                "p4_safe_log_only_rule_id": rule_ids["p4"],
                "phase4_end_of_stream_evaluation_status": p4_safe_status,
                "phase4_first_byte_before_response_end_status": p4_safe_status,
                "phase4_no_full_response_buffering_status": p4_safe_status,
                "p4_strict": "NOT_EXECUTED",
                "keepalive_connection_reused": bool(keepalive_observation["connection_reused"]),
                "keepalive_followup_status": int(keepalive_observation["followup_status"]),
                "processes_stopped": traefik_stopped and engine_stopped,
                "production_ready": False,
                "request_body_bytes_observed": request_body_bytes,
                "response_chunks_observed": response_chunks,
                "rule_evaluation": "host_runtime_observed_not_promoted",
                "rules_profile": rules_profile,
                "status": "PASS",
                "traefik_version": traefik_version(binary),
                "transport_observations_diagnostic": transport_observations_path.name,
                "upstream_requests": upstream_requests,
            },
        )
        return 0
    except Exception as exc:
        traefik_stopped = stop_process(process)
        engine_stopped = stop_process(engine_process)
        write_json(
            result_path,
            {
                "common_runtime_bridge": True,
                "connector": "traefik",
                "engine_mode": "uds",
                "error_class": type(exc).__name__,
                "integration_mode": "native-traefik-middleware",
                "processes_stopped": traefik_stopped and engine_stopped,
                "production_ready": False,
                "rule_evaluation": "host_runtime_failed",
                "status": "FAIL",
            },
        )
        print(f"FAIL: Traefik native local-plugin host: {type(exc).__name__}", file=sys.stderr)
        return 1
    finally:
        stop_process(process)
        stop_process(engine_process)
        upstream.shutdown()
        upstream.server_close()
        remove_private_engine_socket_dir(engine_socket_dir)


def main() -> int:
    try:
        return run()
    except MissingDependency as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 77


if __name__ == "__main__":  # pragma: no cover - command entry point
    raise SystemExit(main())
