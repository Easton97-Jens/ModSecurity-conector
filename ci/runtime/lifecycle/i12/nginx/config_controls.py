#!/usr/bin/env python3
"""Fresh parser observations for historical NGINX fixture defects; no traffic."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for name in ("nginx-binary", "module", "library-dir", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    if not args.output.is_relative_to(Path("/var/tmp/codex/ModSecurity-conector")) or args.output.exists():
        raise ValueError("fresh task-owned output required")
    args.output.mkdir(mode=0o700)
    cases = [
        ("historical-minimal", "modsecurity_phase4_mode minimal;", 1, "expected off|safe|strict"),
        ("historical-host-mime-gate", 'modsecurity_phase4_content_types_file "' + str(args.output / "scope.txt") + '";', 1,
         'unknown directive "modsecurity_phase4_content_types_file"'),
        ("supported-safe", "modsecurity_phase4_mode safe;", 0, "test is successful"),
        ("supported-strict", "modsecurity_phase4_mode strict;", 0, "test is successful"),
    ]
    (args.output / "scope.txt").write_text("application/json\n")
    environment = {"PATH": "/usr/bin:/bin", "LD_LIBRARY_PATH": str(args.library_dir)}
    rows = []
    for label, directive, expected, diagnostic in cases:
        configuration = args.output / (label + ".conf")
        configuration.write_text(f'load_module "{args.module}";\nuser nobody nogroup;\n'
            + f'pid "{args.output}/{label}.pid";\nerror_log stderr;\nevents {{}}\nhttp {{ {directive} }}\n')
        argv = [str(args.nginx_binary), "-e", "stderr", "-t", "-c", str(configuration), "-p", str(args.output) + "/"]
        child = subprocess.run(argv, env=environment, capture_output=True, timeout=15)
        (args.output / (label + ".stdout")).write_bytes(child.stdout)
        (args.output / (label + ".stderr")).write_bytes(child.stderr)
        rows.append({"label": label, "argv": argv, "actual_exit": child.returncode,
            "signal": -child.returncode if child.returncode < 0 else None,
            "expected_exit": expected, "diagnostic": diagnostic,
            "matched": child.returncode == expected and diagnostic.encode() in child.stderr,
            "configuration_sha256": sha(configuration), "stderr_sha256": sha(args.output / (label + ".stderr")),
            "http_requests_sent": 0, "host_started": False})
    receipt = {"scope": "Native parser only; no HTTP or lifecycle qualification", "rows": rows,
        "module_sha256": sha(args.module), "binary_sha256": sha(args.nginx_binary),
        "rules_scope_file_sha256": sha(args.output / "scope.txt"), "all_expected": all(row["matched"] for row in rows)}
    (args.output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt))
    return 0 if receipt["all_expected"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
