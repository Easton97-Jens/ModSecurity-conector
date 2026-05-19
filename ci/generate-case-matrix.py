#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
IMPORT_STATUS = ROOT / "tests/import-status.json"
OUT = ROOT / "docs/testing/generated"

RULE_RE = re.compile(r'^\s*SecRule\s+([^\s]+)\s+"(@[^\s"]+)')
PHASE_RE = re.compile(r"phase:(\d)")
TRANS_RE = re.compile(r"t:([A-Za-z0-9_]+)")
GAP_TAG_RE = re.compile(r"(connector[_-]?gap|runtime[_-]?difference|future|experimental|pending|mapped[_-]?only)", re.I)


def warn(message: str) -> None:
    print(f"[matrix-generator] WARN: {message}", file=sys.stderr)


def read_yaml(path: Path) -> dict:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        warn(f"failed to parse YAML {path}: {exc}")
        return {}
    if not isinstance(raw, dict):
        warn(f"YAML root is not an object in {path}; treating as empty")
        return {}
    return raw


def infer_scope(path: Path) -> str:
    s = str(path).replace("\\", "/")
    if "/tests/common/" in s:
        return "common"
    if "/tests/apache/" in s:
        return "apache"
    if "/tests/nginx/" in s:
        return "nginx"
    return "unknown"


def parse_runtime_verified(data: dict) -> str:
    rv = data.get("runtime_verified", data.get("verified"))
    if isinstance(rv, bool):
        return "true" if rv else "false"
    if isinstance(rv, str):
        low = rv.strip().lower()
        if low in {"true", "yes", "pass", "verified"}:
            return "true"
        if low in {"false", "no", "unverified", "pending"}:
            return "false"
    status = str(data.get("status", "unknown")).lower()
    if status in {"pass", "verified"}:
        return "true"
    if status in {"xfail", "pending", "blocked", "unknown"}:
        return "false"
    return "unknown"


def parse_case(path: Path) -> dict:
    data = read_yaml(path)
    rules = str(data.get("rules", "") or "")

    variables: set[str] = set()
    phases: set[int] = set()
    operators: set[str] = set()
    transformations: set[str] = set()

    for line in rules.splitlines():
        m = RULE_RE.search(line)
        if m:
            variables.add(m.group(1))
            operators.add(m.group(2))
        for p in PHASE_RE.findall(line):
            phases.add(int(p))
        for t in TRANS_RE.findall(line):
            transformations.add(t)

    status = str(data.get("status", "unknown") or "unknown").strip().lower()
    category = str(data.get("category", "unknown") or "unknown")
    notes = str(data.get("notes", data.get("note", "")) or "")
    source = data.get("source") or data.get("source_ref") or data.get("provenance") or "unknown"
    caps = data.get("capabilities")
    if not isinstance(caps, dict):
        caps = {}

    tags = set()
    for txt in [path.name, status, category, notes, str(source)]:
        for match in GAP_TAG_RE.findall(txt):
            tags.add(match.lower().replace("_", "-"))

    response_body = bool(caps.get("response_body", False)) or any("RESPONSE_BODY" in v for v in variables)

    if not phases:
        warn(f"no phase metadata found in {path}")

    return {
        "id": str(data.get("name", path.stem) or path.stem),
        "path": str(path.relative_to(ROOT)),
        "scope": infer_scope(path),
        "status": status,
        "category": category,
        "runtime_verified": parse_runtime_verified(data),
        "variables": sorted(variables),
        "operators": sorted(operators),
        "transformations": sorted(transformations),
        "phases": sorted(phases),
        "response_body": response_body,
        "source": str(source),
        "notes": notes if notes else "-",
        "tags": sorted(tags),
    }


def gather_cases() -> list[dict]:
    files = []
    for scope in ["common", "apache", "nginx"]:
        files.extend(sorted((ROOT / "tests" / scope / "cases").rglob("*.yaml")))
    return [parse_case(p) for p in files]


def load_import_status() -> dict:
    try:
        return json.loads(IMPORT_STATUS.read_text(encoding="utf-8"))
    except Exception as exc:
        warn(f"failed to parse {IMPORT_STATUS}: {exc}")
        return {}


def write(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("Generated file — do not edit manually.\n\n" + body.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    cases = gather_cases()
    imp = load_import_status()

    by_scope = Counter(c["scope"] for c in cases)
    by_status = Counter(c["status"] for c in cases)
    by_runtime = Counter(c["runtime_verified"] for c in cases)
    by_phase = Counter(p for c in cases for p in c["phases"])
    by_var = Counter(v for c in cases for v in c["variables"])
    response_body_count = sum(1 for c in cases if c["response_body"])

    matrix = ["# Generated Case Matrix", "", "| case_id | path | scope | phase | variables | operators | transformations | status | runtime_verified | notes |", "|---|---|---|---|---|---|---|---|---|---|"]
    for c in cases:
        matrix.append(f"| {c['id']} | `{c['path']}` | {c['scope']} | {','.join(map(str, c['phases'])) or '-'} | {', '.join(c['variables']) or '-'} | {', '.join(c['operators']) or '-'} | {', '.join(c['transformations']) or '-'} | {c['status']} | {c['runtime_verified']} | {c['notes']} |")
    write(OUT / "case-matrix.generated.md", "\n".join(matrix))

    summary = ["# Generated Coverage Summary", "", f"- Total cases: {len(cases)}", f"- RESPONSE_BODY cases: {response_body_count}", f"- Verified runtime cases: {by_runtime.get('true', 0)}", f"- Non-verified runtime cases: {len(cases) - by_runtime.get('true', 0)}", "", "## By scope"]
    for k in ["common", "apache", "nginx", "unknown"]:
        summary.append(f"- {k}: {by_scope.get(k, 0)}")
    summary += ["", "## By status"] + [f"- {k}: {v}" for k, v in sorted(by_status.items())]
    summary += ["", "## By variable/collection"] + [f"- `{k}`: {v}" for k, v in by_var.most_common()]
    summary += ["", "## By phase"] + [f"- phase {p}: {by_phase.get(p, 0)}" for p in [1, 2, 3, 4]]
    summary += ["", "## Verification note", "- Generated summaries are reporting only and do not replace full runtime evidence from `make smoke-all`.", "- RESPONSE_BODY remains non-verified/non-promoted until stable full-smoke runtime evidence exists."]
    write(OUT / "coverage-summary.generated.md", "\n".join(summary))

    xfail = ["# Generated XFAIL/Pending/Future Summary", "", "| case_id | path | status | phase | variables | notes |", "|---|---|---|---|---|---|"]
    for c in cases:
        if c["status"] in {"xfail", "pending", "future", "experimental"} or any(t in c["tags"] for t in ["future", "experimental", "pending"]):
            xfail.append(f"| {c['id']} | `{c['path']}` | {c['status']} | {','.join(map(str, c['phases'])) or '-'} | {', '.join(c['variables']) or '-'} | {c['notes']} |")
    write(OUT / "xfail-summary.generated.md", "\n".join(xfail))

    gaps = ["# Generated Connector Gap Summary", "", "| case_id | path | status | tags | variables | source/provenance | notes |", "|---|---|---|---|---|---|---|"]
    for c in cases:
        tags = set(c["tags"])
        if "connector-gap" in tags or "runtime-difference" in tags or c["status"] in {"connector-gap", "runtime-difference"}:
            gaps.append(f"| {c['id']} | `{c['path']}` | {c['status']} | {', '.join(c['tags']) or '-'} | {', '.join(c['variables']) or '-'} | {c['source']} | {c['notes']} |")
    for key in ["connector_specific", "mapped_only", "blocked", "xfail"]:
        for e in imp.get(key, []):
            if isinstance(e, dict):
                gaps.append(f"| {e.get('case') or e.get('source') or 'unknown'} | `tests/import-status.json` | {key} | - | - | {e.get('source', 'unknown')} | {e.get('reason', '')} |")
    write(OUT / "connector-gap-summary.generated.md", "\n".join(gaps))

    phase_doc = ["# Generated Phase Coverage", "", "| phase | case_count | top_variables | status_distribution |", "|---|---:|---|---|"]
    for p in [1, 2, 3, 4]:
        pcases = [c for c in cases if p in c["phases"]]
        var_count = Counter(v for c in pcases for v in c["variables"])
        stat_count = Counter(c["status"] for c in pcases)
        top_vars = ", ".join(f"{k}({v})" for k, v in var_count.most_common(5)) or "-"
        stats = ", ".join(f"{k}:{v}" for k, v in sorted(stat_count.items())) or "-"
        phase_doc.append(f"| {p} | {len(pcases)} | {top_vars} | {stats} |")
    write(OUT / "phase-coverage.generated.md", "\n".join(phase_doc))

    overview = [
        "# ModSecurity Connector Test Coverage Overview",
        "",
        "## Kurzzusammenfassung",
        f"- Gesamtzahl Cases: **{len(cases)}**",
        f"- verified/pass count (runtime_verified=true): **{by_runtime.get('true', 0)}**",
        f"- xfail count: **{by_status.get('xfail', 0)}**",
        f"- pending-runtime-verification count: **{by_runtime.get('false', 0)}**",
        f"- connector-gap count: **{sum(1 for c in cases if 'connector-gap' in c['tags'] or c['status']=='connector-gap')}**",
        f"- runtime-difference count: **{sum(1 for c in cases if 'runtime-difference' in c['tags'] or c['status']=='runtime-difference')}**",
        f"- future/experimental count: **{sum(1 for c in cases if 'future' in c['tags'] or 'experimental' in c['tags'] or c['status'] in {'future','experimental'})}**",
        f"- RESPONSE_BODY cases: **{response_body_count}** (weiterhin **nicht verified/promoted**)",
        "",
        "## Coverage nach Variable/Collection",
        "| Variable | Count |",
        "|---|---:|",
    ]
    overview += [f"| `{k}` | {v} |" for k, v in by_var.most_common(20)]
    overview += ["", "## Coverage nach Phase", "| Phase | Count |", "|---|---:|"]
    overview += [f"| {p} | {by_phase.get(p, 0)} |" for p in [1, 2, 3, 4]]
    overview += ["", "## Coverage nach Status", "| Status | Count |", "|---|---:|"]
    overview += [f"| {k} | {v} |" for k, v in sorted(by_status.items())]
    overview += ["", "## Coverage nach Scope", "| Scope | Count |", "|---|---:|"]
    overview += [f"| {k} | {by_scope.get(k, 0)} |" for k in ["common", "apache", "nginx", "unknown"]]
    overview += ["", "## Top offene Gaps", "- Siehe `docs/testing/generated/connector-gap-summary.generated.md` für detaillierte Einträge.", "", "## Verified Runtime Coverage", "- Runtime-verified ist nur das, was als `runtime_verified=true` klassifiziert ist.", "", "## Pending Runtime Verification", "- Fälle mit `runtime_verified=false/unknown` sind nicht als Runtime-PASS zu lesen.", "", "## XFAIL / Known Gap Coverage", "- XFAIL/Pending/Future/Experimental Fälle sind in der XFAIL-Summary gelistet.", "", "## Connector Gap / Runtime Difference Coverage", "- Connector-Gap und Runtime-Difference sind explizit separat ausgewiesen.", "", "## Phase 3/4 Outbound Coverage", "- Phase 3/4 Fälle sind in `phase-coverage.generated.md` und der Matrix enthalten.", "", "## RESPONSE_BODY Status", "- RESPONSE_BODY bleibt nicht verified/promoted.", "", "## Cloud/Quick/Full Smoke Bedeutung", "- Quick/Cloud Checks sind nützlich für frühes Signal, ersetzen aber keine vollständige Runtime-Verifikation.", "- `make smoke-all` bleibt autoritativ für Runtime-Evidenz.", "", "## Generated Artefakte", "- `docs/testing/generated/case-matrix.generated.md`", "- `docs/testing/generated/coverage-summary.generated.md`", "- `docs/testing/generated/xfail-summary.generated.md`", "- `docs/testing/generated/connector-gap-summary.generated.md`", "- `docs/testing/generated/phase-coverage.generated.md`", "", "## Hinweis", "- Generated summaries ersetzen keine Full-Smoke Runtime-Evidenz.", "- Keine RESPONSE_BODY-Promotion ohne stabile Vollbelege."]
    write(ROOT / "docs/testing/test-coverage-overview.md", "\n".join(overview))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
