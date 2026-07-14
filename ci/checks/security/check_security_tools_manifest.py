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
USES = re.compile(r"^\s*(?:-\s*)?uses:\s*([^\s#]+)(?:\s*#\s*(.+))?\s*$")


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


def validate_manifest_data(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if manifest.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if not isinstance(manifest.get("checked_at"), str) or not manifest["checked_at"]:
        errors.append("checked_at must be a non-empty string")
    tools = manifest.get("tools")
    if not isinstance(tools, dict):
        return errors + ["tools must be a mapping"]
    if set(tools) != REQUIRED_TOOLS:
        errors.append("tools must contain the required security integrations exactly")

    for name, record in tools.items():
        if not isinstance(record, dict):
            errors.append(f"{name}: record must be a mapping")
            continue
        for key in (
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
        ):
            if key not in record:
                errors.append(f"{name}: missing {key}")
        upstream = record.get("upstream")
        if not isinstance(upstream, dict):
            errors.append(f"{name}: upstream must be a mapping")
        else:
            owner = upstream.get("owner")
            repository = upstream.get("repository")
            if (owner, repository) not in OFFICIAL_UPSTREAMS:
                errors.append(f"{name}: upstream is not an approved official repository")
            expected_url = f"https://github.com/{owner}/{repository}"
            if upstream.get("url") != expected_url:
                errors.append(f"{name}: upstream URL must identify the official repository")
        release = record.get("release")
        if not isinstance(release, dict):
            errors.append(f"{name}: release must be a mapping")
        else:
            if not isinstance(release.get("version"), str) or not release["version"]:
                errors.append(f"{name}: release version is required")
            if not isinstance(release.get("date"), str) or not release["date"]:
                errors.append(f"{name}: release date is required")
            if not isinstance(release.get("commit_sha"), str) or not SHA.fullmatch(
                release["commit_sha"]
            ):
                errors.append(f"{name}: release commit SHA must be 40 lowercase hex characters")
        if not isinstance(record.get("evaluated_at"), str) or not record["evaluated_at"]:
            errors.append(f"{name}: per-tool evaluation date is required")
        policy = record.get("security_policy")
        if not isinstance(policy, str) or not policy:
            errors.append(f"{name}: security-policy disposition is required")
        elif (
            isinstance(upstream, dict)
            and policy != "not_published_at_evaluation"
            and policy != f"{upstream.get('url')}/security/policy"
        ):
            errors.append(f"{name}: security policy must be the official upstream policy URL")
        platforms = record.get("supported_platforms")
        if (
            not isinstance(platforms, list)
            or not platforms
            or not all(isinstance(platform, str) and platform for platform in platforms)
        ):
            errors.append(f"{name}: supported platforms must be a non-empty list")
        if (
            not isinstance(record.get("public_repository_availability"), str)
            or not record["public_repository_availability"]
        ):
            errors.append(f"{name}: public-repository availability is required")
        if record.get("status") not in ALLOWED_STATUSES:
            errors.append(f"{name}: unsupported status")
        if not isinstance(record.get("automated_fixes"), bool):
            errors.append(f"{name}: automated_fixes must be boolean")
        elif record["automated_fixes"]:
            errors.append(f"{name}: automatic fixes are not allowed")
        if not isinstance(record.get("minimal_permissions"), list):
            errors.append(f"{name}: minimal_permissions must be a list")
        if not isinstance(record.get("secrets"), list):
            errors.append(f"{name}: secrets must be a list")
        if not isinstance(record.get("workflows"), list):
            errors.append(f"{name}: workflows must be a list")
        if record.get("status") != "enabled" and not record.get("reason"):
            errors.append(f"{name}: non-enabled status needs a reason")
        if record.get("integration") == "downloaded_binary":
            checksum = record.get("checksum")
            if not isinstance(checksum, dict):
                errors.append(f"{name}: downloaded binary needs checksum metadata")
            else:
                if not isinstance(checksum.get("sha256"), str) or not SHA256.fullmatch(
                    checksum["sha256"]
                ):
                    errors.append(f"{name}: binary SHA-256 must be 64 lowercase hex characters")
                if not isinstance(checksum.get("asset"), str) or not checksum["asset"]:
                    errors.append(f"{name}: binary asset is required")
                if not isinstance(checksum.get("source"), str) or not checksum["source"]:
                    errors.append(f"{name}: checksum source is required")
                if not isinstance(checksum.get("executable"), str) or not checksum["executable"]:
                    errors.append(f"{name}: executable is required")
                if isinstance(upstream, dict):
                    expected_prefix = (
                        f"https://github.com/{upstream.get('owner')}/"
                        f"{upstream.get('repository')}/releases/download/"
                    )
                    if not isinstance(checksum.get("url"), str) or not checksum["url"].startswith(
                        expected_prefix
                    ):
                        errors.append(f"{name}: download URL must be an official release asset")
    dispositions = manifest.get("dispositions")
    if not isinstance(dispositions, dict):
        errors.append("dispositions must be a mapping")
    else:
        attestations = dispositions.get("artifact_attestations")
        if not isinstance(attestations, dict):
            errors.append("artifact_attestations disposition is required")
        elif (
            attestations.get("status") != "not_applicable"
            or attestations.get("reason")
            != "not_applicable_until_release_workflow_exists"
        ):
            errors.append("artifact attestation disposition must remain explicit")
    return errors


def validate_pinned_actions(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    pins = manifest.get("pinned_actions")
    if not isinstance(pins, dict) or not pins:
        return ["pinned_actions must be a non-empty mapping"]
    for action, record in pins.items():
        if not isinstance(action, str) or action.count("/") != 1:
            errors.append(f"pinned action name is malformed: {action!r}")
            continue
        if not isinstance(record, dict):
            errors.append(f"{action}: pinned action record must be a mapping")
            continue
        if not isinstance(record.get("version"), str) or not record["version"].startswith("v"):
            errors.append(f"{action}: pinned action version must be a stable v-prefixed value")
        if not isinstance(record.get("commit_sha"), str) or not SHA.fullmatch(
            record["commit_sha"]
        ):
            errors.append(f"{action}: pinned action SHA must be 40 lowercase hex characters")
        if record.get("upstream") != f"https://github.com/{action}":
            errors.append(f"{action}: pinned action upstream must be official GitHub URL")
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


def validate_workflow_text(
    text: str, label: str, pinned_actions: dict[str, dict[str, Any]] | None = None
) -> list[str]:
    errors: list[str] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = USES.match(line)
        if match is None:
            continue
        reference, version = match.groups()
        if reference.startswith("./"):
            continue
        if "@" not in reference:
            errors.append(f"{label}:{line_number}: action reference lacks a revision")
            continue
        action, revision = reference.rsplit("@", 1)
        action_parts = action.split("/")
        if len(action_parts) < 2:
            errors.append(f"{label}:{line_number}: action reference is malformed")
            continue
        if not SHA.fullmatch(revision):
            errors.append(f"{label}:{line_number}: action reference is not an immutable SHA")
        if not version or not version.startswith("v"):
            errors.append(f"{label}:{line_number}: immutable action reference lacks a stable-version comment")
        if pinned_actions is not None:
            upstream = "/".join(action_parts[:2])
            expected = pinned_actions.get(upstream)
            if expected is None:
                errors.append(
                    f"{label}:{line_number}: action is absent from the versioned pin map: {upstream}"
                )
                continue
            if revision != expected.get("commit_sha"):
                errors.append(
                    f"{label}:{line_number}: action SHA does not match the recorded release: {upstream}"
                )
            if version != expected.get("version"):
                errors.append(
                    f"{label}:{line_number}: action version comment does not match the recorded release: {upstream}"
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
