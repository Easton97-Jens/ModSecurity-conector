from __future__ import annotations

import re
import shlex
from pathlib import Path
from typing import Any

SPLIT_SHELL = re.compile(r"(?:;|&&|\|\|)")
BROAD_STAGING_ARGUMENTS = frozenset({"--all", "-A", "."})
FORCE_PUSH_ARGUMENTS = frozenset({"--force-with-lease", "--force", "-f"})
MASTER_DESTINATIONS = frozenset({"master", "refs/heads/master"})


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def _token_segments(command: str) -> list[list[str]] | None:
    try:
        return [shlex.split(segment) for segment in SPLIT_SHELL.split(command)]
    except ValueError:
        return None


def _git_arguments(tokens: list[str], subcommand: str) -> list[str] | None:
    for index in range(len(tokens) - 1):
        if tokens[index : index + 2] == ["git", subcommand]:
            return tokens[index + 2 :]
    return None


def _git_argument_sets(command: str, subcommand: str) -> list[list[str]] | None:
    segments = _token_segments(command)
    if segments is None:
        return None
    return [
        arguments
        for tokens in segments
        if (arguments := _git_arguments(tokens, subcommand)) is not None
    ]


def _has_broad_staging(command: str) -> bool:
    argument_sets = _git_argument_sets(command, "add")
    return argument_sets is None or any(
        BROAD_STAGING_ARGUMENTS.intersection(arguments) for arguments in argument_sets
    )


def _has_hard_reset(command: str) -> bool:
    argument_sets = _git_argument_sets(command, "reset")
    return argument_sets is None or any("--hard" in arguments for arguments in argument_sets)


def _is_force_push_argument(argument: str) -> bool:
    return argument in FORCE_PUSH_ARGUMENTS or argument.startswith(
        ("--force-with-lease=", "--force=")
    )


def _has_force_push(command: str) -> bool:
    argument_sets = _git_argument_sets(command, "push")
    return argument_sets is None or any(
        any(_is_force_push_argument(argument) for argument in arguments)
        for arguments in argument_sets
    )


def _rm_arguments(tokens: list[str]) -> list[str] | None:
    try:
        return tokens[tokens.index("rm") + 1 :]
    except ValueError:
        return None


def _has_recursive_flag(arguments: list[str]) -> bool:
    return any(
        item in {"-r", "-R", "--recursive"}
        or (item.startswith("-") and "r" in item.lower())
        for item in arguments
        if item.startswith("-")
    )


def _is_approved_temp_target(target: str, temp_root: Path) -> bool:
    candidate = Path(target)
    return candidate.is_absolute() and _is_within(candidate, temp_root)


def _has_recursive_remove_outside_temp(command: str, temp_root: Path) -> bool:
    segments = _token_segments(command)
    if segments is None:
        return True
    for tokens in segments:
        arguments = _rm_arguments(tokens)
        if arguments is None or not _has_recursive_flag(arguments):
            continue
        targets = [item for item in arguments if not item.startswith("-")]
        if not targets or any(not _is_approved_temp_target(target, temp_root) for target in targets):
            return True
    return False


def _has_master_destination(argument: str) -> bool:
    destination = argument.rsplit(":", 1)[-1]
    return destination in MASTER_DESTINATIONS


def _pushes_to_master(command: str) -> bool:
    """Recognize explicit Git push refspecs whose destination is master."""
    argument_sets = _git_argument_sets(command, "push")
    return argument_sets is None or any(
        _has_master_destination(argument)
        for arguments in argument_sets
        for argument in arguments
    )


def dangerous_command_reason(command: str, temp_root: Path) -> str | None:
    """Return a non-sensitive policy category for a command that must be denied."""
    checks = (
        (_has_broad_staging(command), "broad_git_staging"),
        (_has_hard_reset(command), "hard_git_reset"),
        (_has_force_push(command), "force_push"),
        (_pushes_to_master(command), "direct_master_push"),
        (_has_recursive_remove_outside_temp(command, temp_root), "recursive_removal_outside_temp_root"),
    )
    return next((reason for matched, reason in checks if matched), None)


def _normalized_staging_path(path: str) -> str:
    normalized = path.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def _is_local_codex_path(normalized: str) -> str | None:
    if normalized in {"AGENTS.md", "AGENTS.override.md", "RTK.md"}:
        return "local_codex_instruction_file"
    if normalized.startswith((".codex/", ".rtk/")):
        return "local_codex_configuration"
    return None


def _is_generated_or_analysis_path(normalized: str) -> bool:
    return normalized.startswith(
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
    )


def _is_possible_secret_file(normalized: str) -> bool:
    name = normalized.rsplit("/", 1)[-1]
    lowered = normalized.lower()
    return (
        name in {".env", "id_rsa", "id_ed25519", ".npmrc"}
        or name.startswith(".env.")
        or name.endswith((".pem", ".key", ".p12", ".pfx", ".jks"))
        or "credential" in lowered
        or "secret" in lowered
    )


def prohibited_staging_path(path: str) -> str | None:
    """Return a non-sensitive category when a path must not be staged."""
    normalized = _normalized_staging_path(path)
    local_category = _is_local_codex_path(normalized)
    if local_category is not None:
        return local_category
    if _is_generated_or_analysis_path(normalized):
        return "local_generated_or_analysis_artifact"
    if _is_possible_secret_file(normalized):
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
