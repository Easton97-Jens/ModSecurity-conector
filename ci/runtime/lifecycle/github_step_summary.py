"""Safely append bounded content to a GitHub Actions step summary file."""

from __future__ import annotations

import argparse
import os
import re
import stat
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path


SUMMARY_DIRECTORY_NAME = "_runner_file_commands"
SUMMARY_FILE_NAME = re.compile(r"^step_summary_[A-Za-z0-9_-]+$", re.ASCII)
UNSAFE_SUMMARY_PATH = "GitHub step summary path is unsafe"
CONNECTORS = frozenset(("apache", "envoy", "haproxy", "lighttpd", "traefik"))
VALID_OUTCOMES = frozenset(("success", "failure", "skipped", "cancelled"))


def _write_summary(descriptor: int, content: str) -> None:
    data = content.encode("utf-8")
    while data:
        written = os.write(descriptor, data)
        if written <= 0:
            raise OSError("cannot append GitHub step summary")
        data = data[written:]


def _safe_open_flags() -> tuple[int, int, int, int]:
    nofollow = getattr(os, "O_NOFOLLOW", None)
    directory = getattr(os, "O_DIRECTORY", None)
    nonblock = getattr(os, "O_NONBLOCK", None)
    if (
        not isinstance(nofollow, int)
        or not isinstance(directory, int)
        or not isinstance(nonblock, int)
    ):
        raise ValueError("GitHub step summary safe-open capability is unavailable")
    return nofollow, directory, nonblock, getattr(os, "O_CLOEXEC", 0)


def _open_directory_without_symlinks(path: Path) -> int:
    if (
        not path.is_absolute()
        or path == Path("/")
        or os.path.normpath(os.fspath(path)) != os.fspath(path)
    ):
        raise ValueError(UNSAFE_SUMMARY_PATH)
    nofollow, directory, _nonblock, close_on_exec = _safe_open_flags()
    descriptor = -1
    try:
        descriptor = os.open(path.anchor, os.O_RDONLY | directory | close_on_exec)
        for component in path.parts[1:]:
            next_descriptor = os.open(
                component,
                os.O_RDONLY | directory | nofollow | close_on_exec,
                dir_fd=descriptor,
            )
            os.close(descriptor)
            descriptor = next_descriptor
    except OSError as error:
        if descriptor >= 0:
            os.close(descriptor)
        raise ValueError(UNSAFE_SUMMARY_PATH) from error
    return descriptor


def _require_trusted_directory(descriptor: int) -> None:
    details = os.fstat(descriptor)
    if (
        not stat.S_ISDIR(details.st_mode)
        or details.st_uid != os.geteuid()
        or details.st_mode & 0o022
    ):
        raise ValueError("GitHub step summary directory is unsafe")


def _open_github_step_summary(environment: Mapping[str, str]) -> int:
    runner_temp_value = environment.get("RUNNER_TEMP", "")
    summary_value = environment.get("GITHUB_STEP_SUMMARY", "")
    runner_temp = Path(runner_temp_value)
    runner_descriptor = -1
    summary_parent_descriptor = -1
    summary_descriptor = -1
    try:
        if not summary_value:
            raise ValueError("GitHub step summary path is unavailable")
        nofollow, directory, nonblock, close_on_exec = _safe_open_flags()
        runner_descriptor = _open_directory_without_symlinks(runner_temp)
        _require_trusted_directory(runner_descriptor)
        summary_path = Path(summary_value)
        if not summary_path.is_absolute() or os.path.normpath(summary_value) != summary_value:
            raise ValueError(UNSAFE_SUMMARY_PATH)
        try:
            relative = summary_path.relative_to(runner_temp)
        except ValueError as error:
            raise ValueError(UNSAFE_SUMMARY_PATH) from error
        if (
            len(relative.parts) != 2
            or relative.parts[0] != SUMMARY_DIRECTORY_NAME
            or not SUMMARY_FILE_NAME.fullmatch(relative.parts[1])
        ):
            raise ValueError(UNSAFE_SUMMARY_PATH)
        summary_parent_descriptor = os.open(
            SUMMARY_DIRECTORY_NAME,
            os.O_RDONLY | directory | nofollow | close_on_exec,
            dir_fd=runner_descriptor,
        )
        _require_trusted_directory(summary_parent_descriptor)
        summary_descriptor = os.open(
            relative.parts[1],
            os.O_WRONLY | os.O_APPEND | nofollow | nonblock | close_on_exec,
            dir_fd=summary_parent_descriptor,
        )
        details = os.fstat(summary_descriptor)
        if (
            not stat.S_ISREG(details.st_mode)
            or details.st_uid != os.geteuid()
            or details.st_mode & 0o022
            or details.st_nlink != 1
        ):
            raise ValueError("GitHub step summary file is unsafe")
        result = summary_descriptor
        summary_descriptor = -1
        return result
    except OSError as error:
        raise ValueError(UNSAFE_SUMMARY_PATH) from error
    finally:
        if runner_descriptor >= 0:
            os.close(runner_descriptor)
        if summary_parent_descriptor >= 0:
            os.close(summary_parent_descriptor)
        if summary_descriptor >= 0:
            os.close(summary_descriptor)


def append_github_step_summary(environment: Mapping[str, str], content: str) -> None:
    descriptor = _open_github_step_summary(environment)
    try:
        _write_summary(descriptor, content)
    finally:
        os.close(descriptor)


def require_connector(value: str, profile: str) -> str:
    if value not in CONNECTORS:
        raise ValueError(f"connector is outside the fixed {profile} runtime set")
    return value


def outcomes_from_environment(
    environment: Mapping[str, str], stages: tuple[tuple[str, str, str], ...]
) -> dict[str, str]:
    outcomes: dict[str, str] = {}
    for key, _label, environment_name in stages:
        value = environment.get(environment_name, "")
        if value not in VALID_OUTCOMES:
            raise ValueError(f"{environment_name} is not a GitHub step outcome")
        outcomes[key] = value
    return outcomes


def validate_outcomes(
    outcomes: Mapping[str, str], stages: tuple[tuple[str, str, str], ...]
) -> None:
    expected_stages = {stage for stage, _label, _environment_name in stages}
    if set(outcomes) != expected_stages:
        raise ValueError("summary outcomes do not match the fixed workflow stage set")
    if any(outcome not in VALID_OUTCOMES for outcome in outcomes.values()):
        raise ValueError("summary outcomes contain an invalid state")


def rendered_outcome(
    connector: str,
    stage: str,
    outcome: str,
    security_skipped_stage: tuple[str, str] | None = None,
) -> str:
    if security_skipped_stage == (connector, stage) and outcome == "skipped":
        return "skipped_by_security_policy"
    return outcome


def outcome_counts(
    connector: str,
    outcomes: Mapping[str, str],
    stages: tuple[tuple[str, str, str], ...],
    security_skipped_stage: tuple[str, str] | None = None,
) -> dict[str, int]:
    counts = {"passed": 0, "failed": 0, "skipped": 0, "cancelled": 0, "security_skipped": 0}
    for stage, _label, _environment_name in stages:
        outcome = outcomes[stage]
        rendered = rendered_outcome(connector, stage, outcome, security_skipped_stage)
        if rendered == "skipped_by_security_policy":
            counts["security_skipped"] += 1
        elif outcome == "success":
            counts["passed"] += 1
        elif outcome == "failure":
            counts["failed"] += 1
        elif outcome == "skipped":
            counts["skipped"] += 1
        else:
            counts["cancelled"] += 1
    return counts


def first_nonpassing_stage(
    connector: str,
    outcomes: Mapping[str, str],
    stages: tuple[tuple[str, str, str], ...],
    security_skipped_stage: tuple[str, str] | None = None,
) -> str:
    for stage, label, _environment_name in stages:
        outcome = rendered_outcome(connector, stage, outcomes[stage], security_skipped_stage)
        if outcome not in ("success", "skipped_by_security_policy"):
            return label
    return "none"


def runtime_bundle_outcome(outcome: str) -> str:
    if outcome == "success":
        return "PASS — real target completed its fail-closed runtime assertions"
    if outcome == "failure":
        return "FAIL — runtime assertions did not complete"
    if outcome == "skipped":
        return "MISSING — runtime target did not run"
    return "CANCELLED — runtime target did not complete"


def render_profile_summary(
    connector: str,
    outcomes: Mapping[str, str],
    stages: tuple[tuple[str, str, str], ...],
    *,
    profile_title: str,
    stage_heading: str,
    runtime_label: str,
    note: str,
    security_skipped_stage: tuple[str, str] | None = None,
) -> str:
    validate_outcomes(outcomes, stages)
    counts = outcome_counts(connector, outcomes, stages, security_skipped_stage)
    rows = [
        f"### {connector} — {profile_title}",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Stages passed | `{counts['passed']}` |",
        f"| Stages failed | `{counts['failed']}` |",
        f"| Stages skipped | `{counts['skipped']}` |",
        f"| Stages cancelled | `{counts['cancelled']}` |",
    ]
    if security_skipped_stage is not None:
        rows.append(f"| Security-policy skips | `{counts['security_skipped']}` |")
    rows.extend(
        (
            f"| First non-passing stage | `{first_nonpassing_stage(connector, outcomes, stages, security_skipped_stage)}` |",
            "",
            f"| {stage_heading} | Actual outcome |",
            "| --- | --- |",
        )
    )
    rows.extend(
        f"| {label} | `{rendered_outcome(connector, stage, outcomes[stage], security_skipped_stage)}` |"
        for stage, label, _environment_name in stages
    )
    rows.extend(
        (
            "",
            "| Real runtime assertion bundle | Outcome |",
            "| --- | --- |",
            f"| {runtime_label} | `{runtime_bundle_outcome(outcomes['runtime'])}` |",
            "",
            note,
            "",
        )
    )
    return "\n".join(rows)


def run_summary(
    arguments: Sequence[str] | None,
    *,
    stages: tuple[tuple[str, str, str], ...],
    render_summary: Callable[[str, Mapping[str, str]], str],
) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector", required=True)
    args = parser.parse_args(arguments)
    try:
        content = render_summary(args.connector, outcomes_from_environment(os.environ, stages))
        append_github_step_summary(os.environ, content)
    except (OSError, ValueError) as error:
        print(f"FAIL: {error}", file=os.sys.stderr)
        return 2
    return 0
