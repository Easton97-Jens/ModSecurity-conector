#!/usr/bin/env python3
"""Generate, but never apply, the reviewed repair for Actions run 36608694822.

This is a one-time recovery aid, not a new candidate-approval mechanism.
It performs no fetch, checkout, staging, commit, push, or workflow operation.
Candidate shell is read as data from two exact Framework Git objects.
"""

from __future__ import annotations

import argparse
import ast
import difflib
import hashlib
from pathlib import Path
import stat
import subprocess
import sys


BASE_SHA = "d56af0856507eb048987974d3960e301e7c24371"
OLD_FRAMEWORK_SHA = "f9e48b0774b5bdf7aaa8e38ce98eb6c50bf293c8"
NEW_FRAMEWORK_SHA = "0290a979ba4bc63a7abed175a53471367b385553"
OLD_STRUCTURE_SHA256 = "7ad268af3baa17d2c2e9b5857ced2138684fab70e5066ddddd6f3656e8baa6af"
OLD_NGINX_SHA256 = "e951607d534836624bd36b6b45a71dbfb055237deae3738da6bbf3270dada279"
NEW_NGINX_SHA256 = "974ed5298a5e398e008704ed5db284e655fc270c596493dbccada452448fc9f1"
OLD_RUFF_COMMIT = "b5dba861cc38e3f7fb4524c9ceba3e01a474ea13"
NEW_RUFF_COMMIT = "62914c4b9b79a9e5004374a9c482ad2ed69290e1"
MAX_FILE_BYTES = 1024 * 1024
FRAMEWORK_PATH = "modules/ModSecurity-test-Framework"
VERIFIER_PATH = "ci/tools/verify-framework-candidate-contract.py"
VERIFIER_TEST_PATH = "tests/test_verify_framework_candidate_contract.py"

# Exactly the literal common.sh changes in Framework commit 0290a979.
PIN_UPDATES = (
    ("NGINX_RELEASE_TAG", "release-1.31.5", "release-1.31.6"),
    ("NGINX_SHA256", OLD_NGINX_SHA256, NEW_NGINX_SHA256),
    ("AWS_LC_TAG", "v5.5.0", "v5.10.0"),
    ("AWS_LC_COMMIT", "991e67ff4cf04df4dd89e407f8b920c6936cb56a",
     "3fe7e081e62131b6776f0d923312b5e6756907ce"),
    ("GO_FTW_RELEASE_TAG", "v2.5.0", "v2.6.0"),
    ("GO_FTW_APPROVED_COMMIT", "a937cfdf5e724574aa27efd652a91e1ed95ef50f",
     "c35cc8a27c560d92f0b466136473424064a24c28"),
    ("CI_CANONICAL_NODE_VERSION", "26.8.2", "26.9.0"),
    ("CI_ACTION_CODEQL_VERSION", "v4.38.0", "v4.38.1"),
    ("CI_ACTION_CODEQL_COMMIT", "b96794f015dfd88f77b49b1c93e0fa7110f94c63",
     "1c5b675653bb5c22dbe9b12b556ec555138e09fd"),
    ("CI_SECURITY_TOOL_RUFF_VERSION", "0.16.7", "0.16.8"),
    ("CI_SECURITY_TOOL_RUFF_COMMIT", OLD_RUFF_COMMIT, NEW_RUFF_COMMIT),
    ("CI_SECURITY_TOOL_RUFF_SHA256",
     "73894c7b7c9a53fd66ed715eb3a1ec65077f316328e377057a98bdb7fcba0326",
     "c4a8c7c152532bcb7e7ede4bd6ccd440dcacddffcdcdd79b90090ac6021f41c2"),
)

MUTABLE_SOURCE_FIELDS = (
    "ENVOY_VERSION", "LIGHTTPD_SERIES", "LIGHTTPD_RELEASE_ROOT_URL",
    "LIGHTTPD_SERIES_BASE_URL", "LIGHTTPD_VERSION", "LIGHTTPD_SOURCE_URL",
    "LIGHTTPD_ARCHIVE_NAME", "LIGHTTPD_DOWNLOAD_URL", "LIGHTTPD_SHA256",
    "HAPROXY_SERIES", "HAPROXY_RELEASE_ROOT_URL", "HAPROXY_SERIES_BASE_URL",
    "HAPROXY_VERSION", "HAPROXY_ARCHIVE_NAME", "HAPROXY_SOURCE_URL",
    "HAPROXY_SHA256", "HAPROXY_HTX_SERIES", "HAPROXY_HTX_SERIES_BASE_URL",
    "HAPROXY_HTX_VERSION", "HAPROXY_HTX_ARCHIVE_NAME", "HAPROXY_HTX_SOURCE_URL",
    "HAPROXY_HTX_SHA256", "CRS_APPROVED_REPO_URL", "CRS_APPROVED_COMMIT",
    "CRS_RELEASE_TAG",
)

# NGINX remains outside the generic synchronizer. No broker path is writable.
NGINX_PATHS = (
    ".github/workflows/test-nginx-exact-head.yml",
    ".github/workflows/test-full-smoke-sequential.yml",
    "ci/provisioning/components/prepare-runtime-components.py",
    "ci/checks/evidence/check-runtime-producer-readiness.py",
    "tests/run_nginx_body_buffer_fixture.py",
    "tests/test_nginx_body_buffer_fixture.py",
    "tests/test_runtime_component_cache_identity.py",
    VERIFIER_TEST_PATH,
    "tests/test_nginx_exact_head_gate_contract.py",
    "tests/test_report_presentation_literals.py",
    "tests/test_update_framework_versions.py",
    "tests/test_prepare_runtime_components.py",
    "tests/test_runtime_env_snapshot_contract.py",
    "tests/test_runtime_component_cache_contract.py",
    "tests/test_evidence_output_security.py",
    "tests/test_nginx_functional_evidence.py",
)
SHA_PATHS = (
    ".github/workflows/test-connectors-with-crs-no-mrts.yml",
    "tests/test_ci_security_workflows.py",
)
TARGET_PATHS = (*NGINX_PATHS, *SHA_PATHS, VERIFIER_PATH)

REGRESSION_TEST = """\
    def test_checked_out_framework_common_matches_production_review(self) -> None:
        framework_common = ROOT / "modules/ModSecurity-test-Framework/ci/lib/common.sh"
        if not framework_common.is_file():
            self.skipTest("reviewed Framework submodule is not initialized")
        payload = framework_common.read_bytes()
        self.assertEqual(
            VERIFIER._framework_common_structure_sha256(payload),
            self.approved_common_structure_sha256,
        )
        # Exercise the real file, not merely two duplicated digest literals.
        VERIFIER.APPROVED_FRAMEWORK_COMMON_STRUCTURE_SHA256 = (
            self.approved_common_structure_sha256
        )
        self.common.write_bytes(payload)
        before = self.parent_bytes()
        values = VERIFIER.verify_contract(self.root, CANDIDATE_SHA, self.common)
        self.assertEqual(values["release_tag"], "release-1.31.6")
        self.assertEqual(before, self.parent_bytes())

"""


class RepairError(ValueError):
    """The exact reviewed recovery preconditions do not hold."""


def replace_required(text: str, before: str, after: str, label: str,
                     *, count: int | None = None) -> str:
    matches = text.count(before)
    if matches == 0 or (count is not None and matches != count):
        raise RepairError(f"{label}: expected {count or 'at least one'} old value; found {matches}")
    return text.replace(before, after)


def structure_digest(text: str) -> str:
    """Reproduce only the normalizer; this does not replace the real verifier."""
    seen: set[str] = set()
    normalized: list[str] = []
    for line in text.splitlines(keepends=True):
        content = line.rstrip("\r\n")
        ending = line[len(content):]
        for name in MUTABLE_SOURCE_FIELDS:
            prefix = name + "="
            if content.startswith(prefix):
                if name in seen:
                    raise RepairError(f"Duplicate source-data field: {name}")
                seen.add(name)
                normalized.append(prefix + "<PARENT_REVIEWED_SOURCE_DATA>" + ending)
                break
        else:
            normalized.append(line)
    if seen != set(MUTABLE_SOURCE_FIELDS):
        raise RepairError("Incomplete source-data registry")
    return hashlib.sha256("".join(normalized).encode("utf-8")).hexdigest()


def reviewed_candidate_digest(previous: str, candidate: str) -> str:
    if structure_digest(previous) != OLD_STRUCTURE_SHA256:
        raise RepairError("Baseline common.sh does not reproduce the approved structure digest")
    expected_lines = previous.splitlines(keepends=True)
    for name, before, after in PIN_UPDATES:
        old_line = f'{name}="{before}"\n'
        matches = [index for index, line in enumerate(expected_lines) if line == old_line]
        if len(matches) != 1:
            raise RepairError(f"Unexpected baseline assignment: {name}")
        expected_lines[matches[0]] = f'{name}="{after}"\n'
    if "".join(expected_lines) != candidate:
        raise RepairError("Candidate differs beyond the 12 reviewed literal assignments")
    digest = structure_digest(candidate)
    if digest == OLD_STRUCTURE_SHA256:
        raise RepairError("Candidate must have a distinct structure digest")
    return digest


def build_changes(originals: dict[str, str], digest: str) -> dict[str, str]:
    if set(originals) != set(TARGET_PATHS):
        raise RepairError("The closed target-file inventory is incomplete or widened")
    changed = dict(originals)
    # Preserve an actually different unreviewed-next-release negative control.
    changed[VERIFIER_TEST_PATH] = replace_required(
        changed[VERIFIER_TEST_PATH],
        'CANDIDATE_COMMON.replace("release-1.31.5", "release-1.31.6")',
        'CANDIDATE_COMMON.replace("release-1.31.5", "release-1.31.7")',
        "NGINX negative control", count=1,
    )
    for path in NGINX_PATHS:
        changed[path] = replace_required(changed[path], "1.31.5", "1.31.6", path)
        changed[path] = changed[path].replace(OLD_NGINX_SHA256, NEW_NGINX_SHA256)
    for path in (VERIFIER_PATH, VERIFIER_TEST_PATH):
        changed[path] = replace_required(
            changed[path], OLD_STRUCTURE_SHA256, digest, path, count=1,
        )
    changed[VERIFIER_TEST_PATH] = replace_required(
        changed[VERIFIER_TEST_PATH], OLD_RUFF_COMMIT, NEW_RUFF_COMMIT, "Ruff fixture",
    )
    for path in SHA_PATHS:
        changed[path] = replace_required(
            changed[path], OLD_FRAMEWORK_SHA, NEW_FRAMEWORK_SHA, path,
        )
    needle = "    def test_production_review_digest_matches_the_reviewed_candidate(self) -> None:\n"
    changed[VERIFIER_TEST_PATH] = replace_required(
        changed[VERIFIER_TEST_PATH], needle, REGRESSION_TEST + needle,
        "real Framework regression insertion", count=1,
    )
    for path, text in changed.items():
        if path.endswith(".py"):
            ast.parse(text, filename=path)
    return changed


def render_patch(originals: dict[str, str], changed: dict[str, str]) -> str:
    chunks: list[str] = []
    for path in sorted(changed):
        if changed[path] == originals[path]:
            continue
        chunks.append(f"diff --git a/{path} b/{path}\n")
        for line in difflib.unified_diff(
            originals[path].splitlines(keepends=True),
            changed[path].splitlines(keepends=True),
            fromfile="a/" + path, tofile="b/" + path,
        ):
            chunks.append(line)
            if not line.endswith("\n"):
                chunks.append("\n\\ No newline at end of file\n")
    chunks.append(
        f"diff --git a/{FRAMEWORK_PATH} b/{FRAMEWORK_PATH}\n"
        f"index {OLD_FRAMEWORK_SHA}..{NEW_FRAMEWORK_SHA} 160000\n"
        f"--- a/{FRAMEWORK_PATH}\n"
        f"+++ b/{FRAMEWORK_PATH}\n"
        "@@ -1 +1 @@\n"
        f"-Subproject commit {OLD_FRAMEWORK_SHA}\n"
        f"+Subproject commit {NEW_FRAMEWORK_SHA}\n"
    )
    return "".join(chunks)


def git_read(root: Path, *arguments: str, stdin: bytes | None = None) -> bytes:
    # No shell, no candidate execution, no network, no external diff/FS-monitor hooks.
    command = [
        "git", "--no-pager", "--no-replace-objects",
        "-c", "core.fsmonitor=false", "-c", "core.hooksPath=/dev/null",
        "-C", str(root), *arguments,
    ]
    result = subprocess.run(command, input=stdin, capture_output=True, timeout=60, check=False)
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace")[:4000]
        raise RepairError(f"Read-only Git check failed: {arguments[0]}\n{detail}")
    if len(result.stdout) > MAX_FILE_BYTES:
        raise RepairError("Git result exceeds the bounded file size")
    return result.stdout


def read_worktree_file(root: Path, relative: str) -> bytes:
    path = root
    for part in Path(relative).parts:
        path = path / part
        if path.is_symlink():
            raise RepairError(f"Symlink in target path: {relative}")
    metadata = path.stat()
    if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > MAX_FILE_BYTES:
        raise RepairError(f"Unsafe target file: {relative}")
    return path.read_bytes()


def prepare_patch(root: Path, framework: Path) -> tuple[str, str]:
    root = root.resolve(strict=True)
    framework = framework.resolve(strict=True)
    if git_read(root, "rev-parse", BASE_SHA + "^{commit}").decode().strip() != BASE_SHA:
        raise RepairError("Required Parent base commit is unavailable")
    gitlink = git_read(root, "ls-tree", BASE_SHA, "--", FRAMEWORK_PATH).decode()
    if gitlink != f"160000 commit {OLD_FRAMEWORK_SHA}\t{FRAMEWORK_PATH}\n":
        raise RepairError("Unexpected baseline Framework gitlink")
    previous = git_read(framework, "show", OLD_FRAMEWORK_SHA + ":ci/lib/common.sh").decode("utf-8")
    candidate = git_read(framework, "show", NEW_FRAMEWORK_SHA + ":ci/lib/common.sh").decode("utf-8")
    digest = reviewed_candidate_digest(previous, candidate)
    originals: dict[str, str] = {}
    for path in TARGET_PATHS:
        payload = git_read(root, "show", BASE_SHA + ":" + path)
        if read_worktree_file(root, path) != payload:
            raise RepairError(f"Target differs from the reviewed baseline: {path}")
        originals[path] = payload.decode("utf-8")
    changed = build_changes(originals, digest)
    patch = render_patch(originals, changed)
    # --check does not apply or stage anything. --index also detects index drift.
    git_read(root, "apply", "--check", "--index", "-", stdin=patch.encode("utf-8"))
    return patch, digest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--framework-repo", type=Path,
                        help="Existing Framework clone containing both exact commits")
    parser.add_argument("--output", type=Path, required=True,
                        help="New patch file; an existing file is never overwritten")
    args = parser.parse_args(argv)
    framework = args.framework_repo or args.repo_root / FRAMEWORK_PATH
    try:
        patch, digest = prepare_patch(args.repo_root, framework)
        with args.output.open("x", encoding="utf-8", newline="") as destination:
            destination.write(patch)
    except (RepairError, OSError, UnicodeError, SyntaxError, subprocess.TimeoutExpired) as error:
        print(f"reviewed Framework repair: {error}", file=sys.stderr)
        return 2
    print(f"Prepared, not applied: {args.output}")
    print(f"Reviewed candidate structure SHA-256: {digest}")
    print(f"Patch scope: {len(TARGET_PATHS)} text files and one Framework gitlink")
    print("Review and apply the patch explicitly; existing contract and runtime checks remain required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
