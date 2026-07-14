from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = ROOT / "ci" / "tooling" / "security-tools.lock.yml"
ALLOWED_STATUSES = {
    "enabled",
    "documented_only",
    "not_applicable",
    "blocked_feature_unavailable",
}
REQUIRED_TOOLS = {
    "actionlint",
    "zizmor",
    "gitleaks_cli",
    "gitleaks_action",
    "codeql",
    "dependency_review",
    "scorecard",
    "osv_scanner",
}
OFFICIAL_UPSTREAMS = {
    ("github", "codeql-action"),
    ("actions", "dependency-review-action"),
    ("ossf", "scorecard-action"),
    ("google", "osv-scanner-action"),
    ("rhysd", "actionlint"),
    ("zizmorcore", "zizmor"),
    ("gitleaks", "gitleaks"),
    ("gitleaks", "gitleaks-action"),
}
SHA = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_RECORD_FIELDS = (
    "display_name",
    "upstream",
    "evaluated_at",
    "security_policy",
    "supported_platforms",
    "public_repository_availability",
    "purpose",
    "license",
    "release",
    "integration",
    "minimal_permissions",
    "secrets",
    "automated_fixes",
    "update_procedure",
    "workflows",
    "status",
)


def load_manifest(path: Path = MANIFEST_PATH) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        value = yaml.safe_load(stream)
    if not isinstance(value, dict):
        raise ValueError("manifest root must be a mapping")
    return value


def check_result_status(outcome: str, feature_available: bool) -> str:
    if not feature_available:
        return "blocked_feature_unavailable"
    if outcome == "passed":
        return "passed"
    return "failed"


def non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value)


def validate_manifest_header(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if manifest.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if not non_empty_string(manifest.get("checked_at")):
        errors.append("checked_at must be a non-empty string")
    return errors


def validate_upstream(name: str, upstream: Any) -> list[str]:
    if not isinstance(upstream, dict):
        return [f"{name}: upstream must be a mapping"]

    errors: list[str] = []
    owner = upstream.get("owner")
    repository = upstream.get("repository")
    if (owner, repository) not in OFFICIAL_UPSTREAMS:
        errors.append(f"{name}: upstream is not an approved official repository")
    expected_url = f"https://github.com/{owner}/{repository}"
    if upstream.get("url") != expected_url:
        errors.append(f"{name}: upstream URL must identify the official repository")
    return errors


def validate_release(name: str, release: Any) -> list[str]:
    if not isinstance(release, dict):
        return [f"{name}: release must be a mapping"]

    errors: list[str] = []
    if not non_empty_string(release.get("version")):
        errors.append(f"{name}: release version is required")
    if not non_empty_string(release.get("date")):
        errors.append(f"{name}: release date is required")
    if not isinstance(release.get("commit_sha"), str) or not SHA.fullmatch(
        release["commit_sha"]
    ):
        errors.append(f"{name}: release commit SHA must be 40 lowercase hex characters")
    return errors


def validate_security_policy(name: str, policy: Any, upstream: Any) -> list[str]:
    if not non_empty_string(policy):
        return [f"{name}: security-policy disposition is required"]
    if not isinstance(upstream, dict):
        return []
    if policy == "not_published_at_evaluation":
        return []
    if policy == f"{upstream.get('url')}/security/policy":
        return []
    return [f"{name}: security policy must be the official upstream policy URL"]


def validate_platforms(name: str, platforms: Any) -> list[str]:
    if not isinstance(platforms, list) or not platforms:
        return [f"{name}: supported platforms must be a non-empty list"]
    if all(non_empty_string(platform) for platform in platforms):
        return []
    return [f"{name}: supported platforms must be a non-empty list"]


def validate_status_metadata(name: str, record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    status = record.get("status")
    if status not in ALLOWED_STATUSES:
        errors.append(f"{name}: unsupported status")
    automated_fixes = record.get("automated_fixes")
    if not isinstance(automated_fixes, bool):
        errors.append(f"{name}: automated_fixes must be boolean")
    elif automated_fixes:
        errors.append(f"{name}: automatic fixes are not allowed")
    return errors


def validate_list_fields(name: str, record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in ("minimal_permissions", "secrets", "workflows"):
        if not isinstance(record.get(field), list):
            errors.append(f"{name}: {field} must be a list")
    return errors


def validate_non_enabled_reason(name: str, record: dict[str, Any]) -> list[str]:
    if record.get("status") == "enabled" or record.get("reason"):
        return []
    return [f"{name}: non-enabled status needs a reason"]


def validate_downloaded_binary(
    name: str, record: dict[str, Any], upstream: Any
) -> list[str]:
    if record.get("integration") != "downloaded_binary":
        return []

    checksum = record.get("checksum")
    if not isinstance(checksum, dict):
        return [f"{name}: downloaded binary needs checksum metadata"]

    errors: list[str] = []
    if not isinstance(checksum.get("sha256"), str) or not SHA256.fullmatch(
        checksum["sha256"]
    ):
        errors.append(f"{name}: binary SHA-256 must be 64 lowercase hex characters")
    for field, error_message in (
        ("asset", "binary asset is required"),
        ("source", "checksum source is required"),
        ("executable", "executable is required"),
    ):
        if not non_empty_string(checksum.get(field)):
            errors.append(f"{name}: {error_message}")
    if not isinstance(upstream, dict):
        return errors

    expected_prefix = (
        f"https://github.com/{upstream.get('owner')}/"
        f"{upstream.get('repository')}/releases/download/"
    )
    if not isinstance(checksum.get("url"), str) or not checksum["url"].startswith(
        expected_prefix
    ):
        errors.append(f"{name}: download URL must be an official release asset")
    return errors


def validate_tool_record(name: str, record: Any) -> list[str]:
    if not isinstance(record, dict):
        return [f"{name}: record must be a mapping"]

    errors = [
        f"{name}: missing {field}"
        for field in REQUIRED_RECORD_FIELDS
        if field not in record
    ]
    upstream = record.get("upstream")
    errors.extend(validate_upstream(name, upstream))
    errors.extend(validate_release(name, record.get("release")))
    if not non_empty_string(record.get("evaluated_at")):
        errors.append(f"{name}: per-tool evaluation date is required")
    errors.extend(validate_security_policy(name, record.get("security_policy"), upstream))
    errors.extend(validate_platforms(name, record.get("supported_platforms")))
    if not non_empty_string(record.get("public_repository_availability")):
        errors.append(f"{name}: public-repository availability is required")
    errors.extend(validate_status_metadata(name, record))
    errors.extend(validate_list_fields(name, record))
    errors.extend(validate_non_enabled_reason(name, record))
    errors.extend(validate_downloaded_binary(name, record, upstream))
    return errors


def validate_dispositions(manifest: dict[str, Any]) -> list[str]:
    dispositions = manifest.get("dispositions")
    if not isinstance(dispositions, dict):
        return ["dispositions must be a mapping"]

    attestations = dispositions.get("artifact_attestations")
    if not isinstance(attestations, dict):
        return ["artifact_attestations disposition is required"]
    if (
        attestations.get("status") != "not_applicable"
        or attestations.get("reason")
        != "not_applicable_until_release_workflow_exists"
    ):
        return ["artifact attestation disposition must remain explicit"]
    return []


def validate_manifest_data(manifest: dict[str, Any]) -> list[str]:
    errors = validate_manifest_header(manifest)
    tools = manifest.get("tools")
    if not isinstance(tools, dict):
        return errors + ["tools must be a mapping"]
    if set(tools) != REQUIRED_TOOLS:
        errors.append("tools must contain the required security integrations exactly")

    for name, record in tools.items():
        errors.extend(validate_tool_record(name, record))
    errors.extend(validate_dispositions(manifest))
    return errors


def validate_pinned_action_record(action: str, record: Any) -> list[str]:
    if not isinstance(record, dict):
        return [f"{action}: pinned action record must be a mapping"]

    errors: list[str] = []
    if not isinstance(record.get("version"), str) or not record["version"].startswith("v"):
        errors.append(f"{action}: pinned action version must be a stable v-prefixed value")
    if not isinstance(record.get("commit_sha"), str) or not SHA.fullmatch(
        record["commit_sha"]
    ):
        errors.append(f"{action}: pinned action SHA must be 40 lowercase hex characters")
    if record.get("upstream") != f"https://github.com/{action}":
        errors.append(f"{action}: pinned action upstream must be official GitHub URL")
    return errors


def validate_pinned_actions(manifest: dict[str, Any]) -> list[str]:
    pins = manifest.get("pinned_actions")
    if not isinstance(pins, dict) or not pins:
        return ["pinned_actions must be a non-empty mapping"]

    errors: list[str] = []
    for action, record in pins.items():
        if not isinstance(action, str) or action.count("/") != 1:
            errors.append(f"pinned action name is malformed: {action!r}")
            continue
        errors.extend(validate_pinned_action_record(action, record))
    return errors


def pinned_actions_from(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    pins = manifest.get("pinned_actions")
    if not isinstance(pins, dict):
        return {}
    return {
        action: record
        for action, record in pins.items()
        if isinstance(action, str) and isinstance(record, dict)
    }


def parse_uses_line(line: str) -> tuple[str, str | None] | None:
    content = line.lstrip()
    if content.startswith("-"):
        content = content[1:].lstrip()
    if not content.startswith("uses:"):
        return None

    value = content.removeprefix("uses:").lstrip()
    reference, separator, comment = value.partition("#")
    reference = reference.rstrip()
    if not reference or any(character.isspace() for character in reference):
        return None
    if not separator:
        return reference, None

    if not comment:
        return None
    version = comment.lstrip()
    if not version:
        return reference, comment[-1:]
    return reference, version


def workflow_error(label: str, line_number: int, message: str) -> str:
    return f"{label}:{line_number}: {message}"


def parse_action_reference(
    reference: str, label: str, line_number: int, errors: list[str]
) -> tuple[str, str] | None:
    if "@" not in reference:
        errors.append(workflow_error(label, line_number, "action reference lacks a revision"))
        return None
    return reference.rsplit("@", 1)


def validate_action_reference(
    action: str, revision: str, version: str | None, label: str, line_number: int
) -> list[str]:
    errors: list[str] = []
    if len(action.split("/")) < 2:
        errors.append(workflow_error(label, line_number, "action reference is malformed"))
    if not SHA.fullmatch(revision):
        errors.append(
            workflow_error(label, line_number, "action reference is not an immutable SHA")
        )
    if not version or not version.startswith("v"):
        errors.append(
            workflow_error(
                label,
                line_number,
                "immutable action reference lacks a stable-version comment",
            )
        )
    return errors


def validate_pinned_action_reference(
    action: str,
    revision: str,
    version: str | None,
    label: str,
    line_number: int,
    pinned_actions: dict[str, dict[str, Any]],
) -> list[str]:
    upstream = "/".join(action.split("/")[:2])
    expected = pinned_actions.get(upstream)
    if expected is None:
        return [
            workflow_error(
                label,
                line_number,
                f"action is absent from the versioned pin map: {upstream}",
            )
        ]

    errors: list[str] = []
    if revision != expected.get("commit_sha"):
        errors.append(
            workflow_error(
                label,
                line_number,
                f"action SHA does not match the recorded release: {upstream}",
            )
        )
    if version != expected.get("version"):
        errors.append(
            workflow_error(
                label,
                line_number,
                f"action version comment does not match the recorded release: {upstream}",
            )
        )
    return errors


def validate_workflow_text(
    text: str, label: str, pinned_actions: dict[str, dict[str, Any]] | None = None
) -> list[str]:
    errors: list[str] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        parsed_line = parse_uses_line(line)
        if parsed_line is None:
            continue
        reference, version = parsed_line
        if reference.startswith("./"):
            continue
        parsed_reference = parse_action_reference(reference, label, line_number, errors)
        if parsed_reference is None:
            continue
        action, revision = parsed_reference
        errors.extend(validate_action_reference(action, revision, version, label, line_number))
        if pinned_actions is not None:
            errors.extend(
                validate_pinned_action_reference(
                    action,
                    revision,
                    version,
                    label,
                    line_number,
                    pinned_actions,
                )
            )
    return errors


def validate_workflow_pins(
    root: Path = ROOT, pinned_actions: dict[str, dict[str, Any]] | None = None
) -> list[str]:
    errors: list[str] = []
    workflows = root / ".github" / "workflows"
    paths = sorted(set(workflows.rglob("*.yml")) | set(workflows.rglob("*.yaml")))
    for path in paths:
        errors.extend(
            validate_workflow_text(
                path.read_text(encoding="utf-8"),
                str(path.relative_to(root)),
                pinned_actions,
            )
        )
    return errors


def validate(root: Path = ROOT) -> list[str]:
    try:
        manifest = load_manifest(root / "ci" / "tooling" / "security-tools.lock.yml")
    except (OSError, ValueError, yaml.YAMLError) as error:
        return [f"manifest load failed: {error}"]
    return (
        validate_manifest_data(manifest)
        + validate_pinned_actions(manifest)
        + validate_workflow_pins(root, pinned_actions_from(manifest))
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate security-tool metadata and workflow pins.")
    parser.add_argument("--root", type=Path, default=ROOT)
    arguments = parser.parse_args()
    errors = validate(arguments.root.resolve())
    if errors:
        for error in errors:
            print(f"security tooling: {error}", file=sys.stderr)
        return 1
    print("Security tooling manifest and workflow pins: valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
