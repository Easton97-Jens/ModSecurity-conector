"""Apply one explicitly selected, source-bound Apache-native oracle correction.

The immutable Framework case and original rendered rules remain evidence. This
Parent host-specific correction does not qualify runtime or lifecycle results.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[3]
REGISTRY = ROOT / "config/testing/i12/apache-native-oracle-overrides.json"
ORIGINAL_RULE = '''SecRule &REQUEST_HEADERS:X-No-Crs-Duplicate "@eq 2" \\
    "id:1100504,phase:1,pass,log,t:none,chain,msg:'no-crs duplicate request header names'"
SecRule REQUEST_HEADERS:X-No-Crs-Duplicate "@streq one" "t:none,chain"
SecRule REQUEST_HEADERS:X-No-Crs-Duplicate "@streq two" "t:none"'''
CORRECTED_RULE = '''SecRule &REQUEST_HEADERS:X-No-Crs-Duplicate "@eq 1" \\
    "id:1100504,phase:1,pass,log,t:none,chain,msg:'no-crs duplicate request header names'"
SecRule REQUEST_HEADERS:X-No-Crs-Duplicate "@streq one, two" "t:none"'''


def digest(path: Path) -> str:
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"proof input must be a regular non-symlink file: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare(selection: str, case: Path, framework: Path, rules: Path,
            identity: Path, receipt: Path) -> dict:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    override = registry["overrides"].get(selection)
    if override is None:
        raise ValueError("unknown Apache oracle override")
    if case.resolve() != (framework / override["case_relative_path"]).resolve():
        raise ValueError("override does not apply to selected case")
    if digest(case) != override["original_case_sha256"]:
        raise ValueError("immutable original case SHA does not match")
    revision = subprocess.run(
        ["rtk", "proxy", "git", "-C", str(framework), "rev-parse", "HEAD"],
        check=True, capture_output=True, text=True, timeout=10,
    ).stdout.strip()
    if revision != override["framework_revision"]:
        raise ValueError("Framework revision does not match scoped correction")
    digest(identity)
    facts = json.loads(identity.read_text(encoding="utf-8"))
    for key in ("profile", "apache_version", "apr_version", "sdk_version"):
        if facts.get(key) != override[key]:
            raise ValueError(f"override identity mismatch: {key}")
    for key in ("apache_binary", "sdk_library"):
        if digest(Path(facts[key])) != override[key + "_sha256"]:
            raise ValueError(f"override artifact mismatch: {key}")
    proofs = facts.get("independent_proofs", [])
    kinds = {proof.get("kind") for proof in proofs}
    if not {"apache_core_merge", "apr_native_sdk_regression"} <= kinds:
        raise ValueError("independent core and real APR/native SDK proofs are required")
    for proof in proofs:
        if digest(Path(proof["path"])) != proof["sha256"]:
            raise ValueError("independent proof SHA mismatch")
        if proof["kind"] == "apache_core_merge" and proof["sha256"] != override["core_merge_proof_sha256"]:
            raise ValueError("core merge proof is outside this source-bound correction")
        if proof["kind"] == "apr_native_sdk_regression":
            observations = dict(line.split("=", 1) for line in
                                Path(proof["path"]).read_text().splitlines())
            expected = {"apr": override["apr_version"], "sdk": "ModSecurity v3.0.14 (Linux)",
                        "count": "1", "header": "X-No-Crs-Duplicate\tone, two", "matched": "1", "status": "451"}
            if any(observations.get(key) != value for key, value in expected.items()):
                raise ValueError("actual APR/native SDK probe does not establish the correction")
            if digest(Path(observations["sdk_image"]).resolve()) != override["sdk_library_sha256"]:
                raise ValueError("actual native probe loaded a different SDK image")
    original_sha = digest(rules)
    text = rules.read_text(encoding="utf-8")
    # Framework rendering preserves this literal rule block. Reject unrelated
    # rules or altered expectations instead of guessing from a rule id alone.
    if text.count(ORIGINAL_RULE) != 1:
        raise ValueError("original rendered rule block does not match")
    archive = rules.with_name(rules.name + ".original-oracle")
    corrected = text.replace(ORIGINAL_RULE, CORRECTED_RULE)
    result = {
        "schema_version": 1, "selection": selection, "correction": override,
        "registry_sha256": digest(REGISTRY), "identity_sha256": digest(identity),
        "independent_proofs": proofs, "original_case": str(case),
        "original_rules": str(archive), "original_rules_sha256": original_sha,
        "corrected_rules": str(rules),
        "corrected_rules_sha256": hashlib.sha256(corrected.encode()).hexdigest(),
        "original_oracle_preserved": True, "runtime_retest": None,
        "lifecycle_qualification": None,
    }
    if receipt.exists() or receipt.is_symlink() or archive.exists() or archive.is_symlink():
        raise ValueError("correction evidence output already exists")
    with archive.open("xb") as stream:
        stream.write(text.encode())
    rules.write_text(corrected, encoding="utf-8")
    with receipt.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write("\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for option in ("selection", "case", "framework", "rules", "identity", "receipt"):
        parser.add_argument("--" + option, required=True)
    args = parser.parse_args()
    try:
        prepare(args.selection, Path(args.case), Path(args.framework),
                Path(args.rules), Path(args.identity), Path(args.receipt))
    except (ValueError, KeyError, OSError, subprocess.SubprocessError) as error:
        parser.exit(77, f"apache oracle override rejected: {error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
