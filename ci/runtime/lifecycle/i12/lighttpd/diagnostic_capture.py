#!/usr/bin/env python3
"""Physical stock-native P1/config diagnostics; no body-lifecycle qualification.

Run as the existing controller's admitted nonroot identity. No identity,
namespace, sandbox, or product capability is modified here.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import socket
import signal
import stat
import subprocess
import time


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fresh_output(path):
    path = Path(path).absolute()
    if path.resolve() != path or path.exists():
        raise ValueError("Fresh physical output directory without symlink ancestors required")
    path.mkdir(parents=True, mode=0o700)
    if stat.S_IMODE(path.stat().st_mode) != 0o700:
        raise ValueError("Output directory must be private")
    return path


def controls_match(receipt):
    codes = [row["exitcode"] for row in receipt["configuration_probes"]]
    return (len(codes) == 8 and codes[0] == 0 and all(code > 0 for code in codes[1:])
            and [row["status"] for row in receipt["clients"]] == [200, 403, 200])


def request(port, marker=False):
    data = b"OPTIONS * HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n"
    if marker:
        data += b"X-Modsec-Smoke: block\r\n"
    data += b"\r\n"
    with socket.create_connection(("127.0.0.1", port), timeout=3) as client:
        client.sendall(data)
        chunks = []
        while True:
            chunk = client.recv(65536)
            if not chunk:
                break
            chunks.append(chunk)
            if sum(map(len, chunks)) > 131072:
                raise ValueError("Diagnostic response exceeds 128 KiB limit")
    return data, b"".join(chunks)


def capture(output, host, module, rules, port=18951):
    output = fresh_output(output)
    os.umask(0o077)
    document = output / "document-root"
    document.mkdir()
    (document / "index.html").write_text("diagnostic stock native\n")
    cases = [
        ("valid_rules_file", None, None),
        ("missing_rules_file", "rules_file", str(output / "absent-rules.conf")),
        ("invalid_rule_syntax", "rules_file", str(output / "invalid-rules.conf")),
        ("unknown_config_key", "invented_unknown_key", "on"),
        ("invalid_boolean", "enabled", "invalid"),
        ("invalid_status", "default_error_status", "12"),
        ("invalid_size", "max_header_count", "NaN"),
        ("unsafe_event_path", "event_path", str(output / "missing-parent/events.jsonl")),
    ]
    (output / "invalid-rules.conf").write_text("NotAValidModSecurityDirective\n")
    records = []
    for name, key, value in cases:
        directory = output / name
        directory.mkdir()
        settings = {"enabled": "on", "rules_file": str(rules),
                    "request_body_mode": "none", "response_body_mode": "none",
                    "default_block_status": "403", "default_error_status": "500",
                    "event_path": str(directory / "events.jsonl")}
        if key:
            settings[key] = value
        runtime = directory / "runtime.conf"
        runtime.write_text("".join(f"{k}={v}\n" for k, v in settings.items()))
        config = directory / "lighttpd.conf"
        config.write_text(
            'server.compat-module-load = "disable"\n'
            'server.modules = ( "mod_msconnector" )\n'
            f'server.document-root = "{document}"\n'
            'server.bind = "127.0.0.1"\n'
            f'server.port = {port}\n'
            f'server.errorlog = "{directory / "error.log"}"\n'
            'msconnector.enabled = "enable"\n'
            f'msconnector.config-file = "{runtime}"\n')
        argv = ["rtk", "proxy", str(host), "-m", str(module.parent), "-tt", "-f", str(config)]
        parsed = subprocess.run(argv, capture_output=True, timeout=15)
        (directory / "config.stdout").write_bytes(parsed.stdout)
        (directory / "config.stderr").write_bytes(parsed.stderr)
        records.append({"case_id": name, "argv": argv, "exitcode": parsed.returncode,
                        "runtime_sha256": sha(runtime), "host_config_sha256": sha(config),
                        "physical_stderr_sha256": sha(directory / "config.stderr"),
                        "qualification_scope": "configuration_parser_only",
                        "original_status_changed": False})
    valid = output / "valid_rules_file"
    host_argv = ["rtk", "proxy", str(host), "-D", "-m", str(module.parent), "-f", str(valid / "lighttpd.conf")]
    clients = []
    stopped = None
    actual = None
    with (output / "host.stdout").open("xb") as stdout, (output / "host.stderr").open("xb") as stderr:
        process = subprocess.Popen(host_argv, stdout=stdout, stderr=stderr)
        try:
            deadline = time.monotonic() + 5
            while time.monotonic() < deadline:
                if process.poll() is not None:
                    raise RuntimeError(f"Host exited before request: {process.returncode}")
                # Find the actual lighttpd child of the RTK wrapper.
                matches = []
                for proc in Path("/proc").iterdir():
                    if proc.name.isdigit():
                        try:
                            if os.readlink(proc / "exe") == str(host):
                                matches.append(proc)
                        except (FileNotFoundError, PermissionError, ProcessLookupError):
                            pass
                if matches:
                    actual = matches[0]
                    (output / "host.status").write_bytes((actual / "status").read_bytes())
                    (output / "host.maps").write_bytes((actual / "maps").read_bytes())
                    try:
                        sent, received = request(port)
                        break
                    except ConnectionRefusedError:
                        pass
                time.sleep(0.05)
            else:
                raise RuntimeError("Host readiness timeout")
            for name, marker in [("p1-allow", False), ("p1-deny", True), ("p1-neighbor", False)]:
                sent, received = request(port, marker)
                (output / f"{name}-request.http").write_bytes(sent)
                (output / f"{name}-response.http").write_bytes(received)
                clients.append({"name": name, "status": int(received.split(b" ", 2)[1]),
                                "physical_response_bytes": len(received),
                                "physical_response_sha256": hashlib.sha256(received).hexdigest(),
                                "peer_eof_observed": True})
        finally:
            if actual is not None:
                try:
                    os.kill(int(actual.name), signal.SIGTERM)
                except ProcessLookupError:
                    pass
            else:
                process.terminate()
            try:
                stopped = process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                stopped = process.wait(timeout=5)
    receipt = {"schema": "lighttpd-stock-native-diagnostic-v1", "route": "lighttpd-stock-native-control",
               "uid": os.getuid(), "gid": os.getgid(), "host_argv": host_argv,
               "host_sha256": sha(host), "module_sha256": sha(module), "rules_sha256": sha(rules),
               "configuration_probes": records, "clients": clients,
               "host_wrapper_exitcode": stopped, "host_wrapper_reaped": process.poll() is not None,
               "body_modes": {"request": "none", "response": "none"},
               "backend": {"applicable": False, "reason": "OPTIONS-star served by host; no upstream configured."},
               "finish_free_observation": None,
               "finish_free_missing_reason": "Stock product module is uninstrumented; no physical API capture was supplied.",
               "full_lifecycle_qualified": False, "original_status_changed": False}
    (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("output", "host", "module", "rules"):
        parser.add_argument("--" + name, required=True, type=Path)
    args = parser.parse_args()
    receipt = capture(args.output, args.host, args.module, args.rules)
    print(json.dumps(receipt, indent=2))
    return 0 if controls_match(receipt) else 1


if __name__ == "__main__":
    raise SystemExit(main())
