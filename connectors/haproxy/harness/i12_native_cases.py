#!/usr/bin/env python3
"""Prepare separate native-HTX private-host inputs from the immutable I12 capture.

Preparation never starts a host or qualifies an oracle. Each generated fixture
needs its own sealed controller spec and independent lifecycle review.
"""
import argparse
import hashlib
import json
from pathlib import Path

CAPTURE_HASHES = {
    "launch.py": "033e35075bba6f5138217059b8e92a7c1ac495af261365897fa81523bef577eb",
    "client.py": "d06126fb153f9675f538f48151bcbd7e8f767e4f639baa70c1f5d37f42410e63",
    "backend.py": "1644799f27594796741fc611589abed79eca35d13166938a7012a0779abad85c",
    "openssl.cnf": "31092455fc7e54d448735380895b9bee2097458bcf2ff10233766f66ee18494f",
}
BASE_REQUEST = b"haproxy-lifecycle-main\n"
BASE_RESPONSE = b"haproxy-lifecycle-response\n"
DIAGNOSTIC_CASES = frozenset(("p1-deny", "p2-deny", "p3-deny", "p4-safe"))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def replace_once(text, before, after):
    if text.count(before) != 1:
        raise ValueError("capture boundary changed: " + repr(before))
    return text.replace(before, after)


def cases():
    result = {
        "request-empty": {"request": b""},
        "request-file": {"request_file": True},
        "request-streaming": {"request_streaming": True},
        "request-content-type-missing": {"request_type": None},
        "request-charset-present": {"request_type": "text/plain; charset=utf-8"},
        "request-charset-missing": {},
        "request-csv": {"request_type": "text/csv", "request": b"id,value\n1,marker\n"},
        "request-marker-at-payload-end": {"request": b"a" * 70000 + b"I12_END"},
        "response-empty": {"response": b""},
        "response-single-chunk": {},
        "response-file": {"response_file": True},
        "response-streaming": {"response_streaming": True},
        "response-content-type-present": {},
        "response-content-type-missing": {"response_type": None},
        "response-charset-present": {"response_type": "text/plain; charset=utf-8"},
        "response-charset-missing": {},
        "response-mime-scope-in": {},
        "response-mime-scope-out": {"response_type": "application/octet-stream", "response_inspected": False},
        "response-csv": {"response_type": "text/csv", "response": b"id,value\n1,marker\n", "mime": "text/csv"},
        "response-marker-at-payload-end": {"response": b"a" * 70000 + b"I12_END"},
        "request-reject": {"request_limit": 16, "request_action": "Reject", "expected_status": 403},
        "request-process-partial": {"request_limit": 16, "request_action": "ProcessPartial", "request_inspected": BASE_REQUEST[:16]},
        "response-reject": {"response_limit": 16, "response_action": "Reject", "expected_status": 200, "response_inspected": False},
        "response-process-partial": {"response_limit": 16, "response_action": "ProcessPartial", "response_inspected": BASE_RESPONSE[:16]},
        "p1-deny": {"deny_phase": 1, "expected_status": 403},
        "p2-deny": {"deny_phase": 2, "expected_status": 403},
        "p3-deny": {"deny_phase": 3, "expected_status": 403},
        # Current HTX host contract deliberately fails unsupported redirects
        # closed with503; the native policy still requests302 plus Location.
        "p3-redirect": {"redirect_phase": 3, "expected_status": 503, "native_requested_status": 302},
        "p4-safe": {"deny_phase": 4},
    }
    for value in result.values():
        value.setdefault("request", BASE_REQUEST)
        value.setdefault("response", BASE_RESPONSE)
    return result


def body_probe(variable, body, rule, phase):
    # Independent native transformation proves inspected bytes, including prefix
    # limits, rather than mistaking connector append counters for SDK contents.
    hashed = hashlib.sha1(body).hexdigest()
    return (f'SecRule {variable} "@streq {hashed}" '
            f'"id:{rule},phase:{phase},pass,log,t:sha1,t:hexEncode,msg:\'I12_NATIVE_EXACT_BYTES_{rule}\'"\n')


def materialize(capture, output, name, case):
    original = {}
    for filename, expected in CAPTURE_HASHES.items():
        data = (capture / filename).read_bytes()
        if digest(data) != expected:
            raise ValueError("immutable capture hash differs: " + filename)
        original[filename] = data.decode()
    output.mkdir(parents=True)
    request = case["request"]
    response = case["response"]
    launch = original["launch.py"]
    launch = replace_once(launch, "SecRequestBodyLimit 1024", "SecRequestBodyLimit " + str(case.get("request_limit", 1048576)))
    launch = replace_once(launch, "SecRequestBodyNoFilesLimit 1024", "SecRequestBodyNoFilesLimit 1048576")
    launch = replace_once(launch, "SecResponseBodyLimit 1024", "SecResponseBodyLimit " + str(case.get("response_limit", 1048576)))
    launch = replace_once(launch, "SecRequestBodyLimitAction Reject", "SecRequestBodyLimitAction " + case.get("request_action", "Reject"))
    launch = replace_once(launch, "SecResponseBodyLimitAction Reject", "SecResponseBodyLimitAction " + case.get("response_action", "Reject"))
    launch = replace_once(launch, "SecResponseBodyMimeType text/plain", "SecResponseBodyMimeType " + case.get("mime", "text/plain"))
    extra = body_probe("REQUEST_BODY", case.get("request_inspected", request), 1999471, 2)
    inspected_response = case.get("response_inspected", response)
    if inspected_response is not False:
        extra += body_probe("RESPONSE_BODY", inspected_response, 1999472, 4)
    if case.get("deny_phase"):
        phase = case["deny_phase"]
        variable = "REQUEST_URI" if phase < 3 else "RESPONSE_HEADERS:X-I12-Main"
        pattern = "/i12-main" if phase < 3 else "main"
        extra += f'SecRule {variable} "@contains {pattern}" "id:1999473,phase:{phase},deny,status:403,log,msg:\'I12_NATIVE_P{phase}_DENY\'"\n'
    if case.get("redirect_phase"):
        extra += 'SecRule RESPONSE_HEADERS:X-I12-Main "@streq main" "id:1999474,phase:3,redirect:https://haproxy-i12.invalid/redirect-target,status:302,log,msg:\'I12_NATIVE_P3_REDIRECT\'"\n'
    launch = replace_once(launch, "SecAction \"id:1999404,phase:4,pass,log,msg:'I12_HAP_P4'\"\n", "SecAction \"id:1999404,phase:4,pass,log,msg:'I12_HAP_P4'\"\n" + extra)
    diagnostic = name in DIAGNOSTIC_CASES
    selected_id = ("DIAG::haproxy-native-htx::" + name if diagnostic else "I12::haproxy-native-htx::NEED-" + name)
    case_label = ("DIAG-" if diagnostic else "NEED-") + name
    launch = launch.replace("I12::haproxy-native-htx::NEED-request-eos-once", selected_id)
    launch = launch.replace("NEED-request-eos-once", case_label).replace("20261014-haproxy-htx-01", "20261015-htx-" + name)
    # A failed main client is retained and the healthy neighbor still runs.
    # A driver zero exit is explicitly not a full lifecycle qualification.
    launch = replace_once(launch, "if result.returncode:raise RuntimeError(label+' failed')", "if result.returncode and label!='main-client':raise RuntimeError(label+' failed')")
    client = original["client.py"]
    body_expr = "Path('/mnt/fixtures/request-body.bin').read_bytes()" if case.get("request_file") else repr(request)
    client = replace_once(client, "body=('haproxy-lifecycle-'+name+'\\n').encode()", "body=" + body_expr + " if name=='main' else b'neighbor'")
    request_type = case.get("request_type", "text/plain")
    client = replace_once(client, "Content-Type: text/plain\\r\\n", "" if request_type is None else "Content-Type: " + request_type + "\\r\\n")
    if case.get("request_streaming"):
        client = replace_once(client, "connection.sendall(request);", "\n    pieces=[request[:-len(body)],body[:8],body[8:]]\n    for piece in pieces:\n        connection.sendall(piece);time.sleep(.1)\n    ")
    expected = case.get("expected_status", 200)
    client = replace_once(client, "if row['status']!=200", f"if row['status']!=({expected} if name=='main' else 200)")
    backend = original["backend.py"]
    response_expr = "Path('/mnt/fixtures/response-body.bin').read_bytes()" if case.get("response_file") else repr(response)
    backend = replace_once(backend, "response=b'haproxy-lifecycle-response\\n'", "response=" + response_expr + " if self.path=='/i12-main' else b'healthy\\n'")
    backend = replace_once(backend, "self.send_response(200);", "self.send_response(200);self.send_header('X-I12-Main','main' if self.path=='/i12-main' else 'neighbor');")
    content_type = case.get("response_type", "text/plain")
    backend = replace_once(backend, "self.send_header('Content-Type','text/plain');", "" if content_type is None else "self.send_header('Content-Type'," + repr(content_type) + ");")
    if case.get("response_streaming"):
        backend = replace_once(backend, "self.wfile.write(response);self.wfile.flush();", "\n        for chunk in [response[:8],response[8:16],response[16:]]:\n            self.wfile.write(chunk);self.wfile.flush();time.sleep(.1)\n        ")
    for filename, text in {"launch.py": launch, "client.py": client, "backend.py": backend}.items():
        compile(text, filename, "exec")
        (output / filename).write_text(text)
    (output / "openssl.cnf").write_text(original["openssl.cnf"])
    (output / "request-body.bin").write_bytes(request)
    (output / "response-body.bin").write_bytes(response)
    contract = {"schema": "i12-haproxy-native-case-v1", "original_id": None if diagnostic else selected_id,
                "diagnostic_id": selected_id if diagnostic else None,
                "original_obligation_eligible": not diagnostic,
                "capture_variant": "haproxy-direct", "capture_input_hashes": CAPTURE_HASHES,
                "request_bytes": len(request), "request_sha256": digest(request),
                "response_bytes": len(response), "response_sha256": digest(response),
                "expected_native_request_sha1": hashlib.sha1(case.get("request_inspected", request)).hexdigest(),
                "expected_native_response_sha1": None if inspected_response is False else hashlib.sha1(inspected_response).hexdigest(),
                "native_response_probe_applicable": inspected_response is not False,
                "neighbor_request_bytes": 8, "neighbor_response_bytes": 8,
                "settings": {key: value for key, value in case.items() if not isinstance(value, bytes)},
                "native_probe_rules": [1999471] + ([1999472] if inspected_response is not False else []),
                "full_lifecycle_pass": None, "private_host_execution_required": True,
                "native_EOS_not_derived_from_HTTP": True}
    (output / "case-contract.json").write_text(json.dumps(contract, indent=2) + "\n")
    files = {p.name: digest(p.read_bytes()) for p in output.iterdir()}
    for path in output.iterdir():
        path.chmod(0o444)
    output.chmod(0o555)
    ledger = output.with_name(output.name + "-ledger.json")
    ledger.write_text(json.dumps({"files": files, "symlinks": {}}, indent=2, sort_keys=True) + "\n")
    ledger.chmod(0o444)
    return {"name": name, "source": str(output), "ledger": str(ledger), "ledger_sha256": digest(ledger.read_bytes())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--capture", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    authorized = Path("/var/tmp/codex/ModSecurity-conector")
    if not args.output.is_absolute() or not args.output.resolve().is_relative_to(authorized):
        parser.error("output must be under the external Codex storage root")
    args.output.mkdir(parents=True, exist_ok=True)
    records = [materialize(args.capture, args.output / name, name, case) for name, case in cases().items()]
    (args.output / "fixture-index.json").write_text(json.dumps(records, indent=2) + "\n")
    print(json.dumps({"prepared": len(records), "hosts_started": 0}))


if __name__ == "__main__":
    main()
