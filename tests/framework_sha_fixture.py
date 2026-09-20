"""Independent static Framework SHA fixtures for temporary test repositories."""

from __future__ import annotations

from pathlib import Path
import re


SOURCE_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = ".github/workflows/test-connectors-with-crs-no-mrts.yml"
FIXTURE_PATH = "tests/test_ci_security_workflows.py"
SLOTS = (
    (WORKFLOW_PATH, r"(?m)^( {6}EXPECTED_FRAMEWORK_SHA:[ \t]*)([0-9a-f]{40})([ \t]*)$", 1),
    (WORKFLOW_PATH, r"(?m)^( {10}FRAMEWORK_SHA:[ \t]*)([0-9a-f]{40})([ \t]*)$", 3),
    (FIXTURE_PATH, r'(?m)^(WITH_CRS_NO_MRTS_FRAMEWORK_SHA[ \t]*=[ \t]*")([0-9a-f]{40})("[ \t]*)$', 1),
)


def set_framework_sha_fixture(root: Path, framework_sha: str) -> None:
    """Reset a copied projection independently of its current repository pin."""
    if root.resolve() == SOURCE_ROOT:
        raise ValueError("Framework SHA fixtures must not modify the source checkout")
    if re.fullmatch(r"[0-9a-f]{40}", framework_sha) is None:
        raise ValueError("test Framework SHA must be 40 lowercase hexadecimal characters")

    original = {
        relative: (root / relative).read_bytes().decode("utf-8")
        for relative in (WORKFLOW_PATH, FIXTURE_PATH)
    }
    observed = set()
    for relative, pattern, count in SLOTS:
        matches = list(re.finditer(pattern, original[relative]))
        if len(matches) != count:
            raise ValueError(f"{relative}: expected {count} static Framework SHA slots")
        observed.update(match.group(2) for match in matches)
    if len(observed) != 1:
        raise ValueError("copied Framework SHA slots are inconsistent")

    # Validate every slot before writing either file. Do not use the production
    # synchronizer to prepare its own test inputs or rewrite dynamic expressions.
    rendered = dict(original)
    for relative, pattern, _count in SLOTS:
        rendered[relative] = re.sub(
            pattern,
            lambda match: match.group(1) + framework_sha + match.group(3),
            rendered[relative],
        )
    for relative, text in rendered.items():
        if text != original[relative]:
            (root / relative).write_bytes(text.encode("utf-8"))
