from __future__ import annotations

import re
import shlex
from pathlib import Path
from typing import Any

BROAD_STAGING = re.compile(r"(?:^|[;&|]\s*)git\s+add\s+(?:--all|-A|\.)(?=\s|$)")
HARD_RESET = re.compile(r"(?:^|[;&|]\s*)git\s+reset\s+[^\n;&|]*--hard(?:\s|$)")
FORCE_PUSH = re.compile(
    r"(?:^|[;&|]\s*)git\s+push\b[^\n;&|]*(?:--force-with-lease|--force|-f)(?=\s|$)"
)
SPLIT_SHELL = re.compile(r"(?:;|&&|\|\|)")


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def _has_recursive_remove_outside_temp(command: str, temp_root: Path) -> bool:
    for segment in SPLIT_SHELL.split(command):
        try:
            tokens = shlex.split(segment)
        except ValueError:
            return True
        if not tokens:
            continue
        try:
            rm_index = tokens.index("rm")
        except ValueError:
            continue
        arguments = tokens[rm_index + 1 :]
        flags = [item for item in arguments if item.startswith("-")]
        recursive = any(
            item in {"-r", "-R", "--recursive"}
            or (item.startswith("-") and "r" in item.lower())
            for item in flags
        )
        if not recursive:
            continue
        targets = [item for item in arguments if not item.startswith("-")]
        if not targets:
            return True
        for target in targets:
            candidate = Path(target)
            if not candidate.is_absolute() or not _is_within(candidate, temp_root):
                return True
    return False


def _pushes_to_master(command: str) -> bool:
    """Recognize explicit Git push refspecs whose destination is master."""
    for segment in SPLIT_SHELL.split(command):
        try:
            tokens = shlex.split(segment)
        except ValueError:
            return True
        for index in range(len(tokens) - 1):
            if tokens[index : index + 2] != ["git", "push"]:
                continue
            for argument in tokens[index + 2 :]:
                if argument in {"master", "refs/heads/master"}:
                    return True
                if ":" not in argument:
                    continue
                destination = argument.rsplit(":", 1)[1]
                if destination in {"master", "refs/heads/master"}:
                    return True
    return False


def dangerous_command_reason(command: str, temp_root: Path) -> str | None:
    """Return a non-sensitive policy category for a command that must be denied."""
    if BROAD_STAGING.search(command):
        return "broad_git_staging"
    if HARD_RESET.search(command):
        return "hard_git_reset"
    if FORCE_PUSH.search(command):
        return "force_push"
    if _pushes_to_master(command):
        return "direct_master_push"
    if _has_recursive_remove_outside_temp(command, temp_root):
        return "recursive_removal_outside_temp_root"
    return None


def prohibited_staging_path(path: str) -> str | None:
    """Return a non-sensitive category when a path must not be staged."""
    normalized = path.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    lowered = normalized.lower()
    if normalized in {"AGENTS.md", "AGENTS.override.md", "RTK.md"}:
        return "local_codex_instruction_file"
    if normalized.startswith((".codex/", ".rtk/")):
        return "local_codex_configuration"
    if normalized.startswith(
        (
            "build/",
            ".build/",
            "tmp/",
            ".tmp/",
            "cache/",
            ".cache/",
            "analysis/",
            ".analysis/",
        )
    ):
        return "local_generated_or_analysis_artifact"
    name = normalized.rsplit("/", 1)[-1]
    if (
        name in {".env", "id_rsa", "id_ed25519", ".npmrc"}
        or name.startswith(".env.")
        or name.endswith((".pem", ".key", ".p12", ".pfx", ".jks"))
        or "credential" in lowered
        or "secret" in lowered
    ):
        return "possible_secret_file"
    return None


def pre_tool_hook_output(payload: dict[str, Any], temp_root: Path) -> dict[str, Any]:
    tool_input = payload.get("tool_input")
    command = tool_input.get("command", "") if isinstance(tool_input, dict) else ""
    reason = dangerous_command_reason(command, temp_root)
    if reason is None:
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": "Repository command policy allows this command.",
            }
        }
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "Blocked by repository safety policy: "
            + reason
            + ".",
        }
    }


def permission_request_hook_output(
    payload: dict[str, Any], temp_root: Path
) -> dict[str, Any] | None:
    tool_input = payload.get("tool_input")
    command = tool_input.get("command", "") if isinstance(tool_input, dict) else ""
    reason = dangerous_command_reason(command, temp_root)
    if reason is None:
        return None
    return {
        "hookSpecificOutput": {
            "hookEventName": "PermissionRequest",
            "decision": {
                "behavior": "deny",
                "message": "Blocked by repository safety policy: " + reason + ".",
            },
        }
    }
