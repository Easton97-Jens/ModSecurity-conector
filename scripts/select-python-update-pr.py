#!/usr/bin/env python3
"""Fail closed when selecting the repository-owned Python update pull request."""

from __future__ import annotations

import argparse
import json
import os
import stat
import sys
from pathlib import Path
from typing import TextIO


MAX_RESPONSE_BYTES = 2 * 1024 * 1024


class SelectionError(RuntimeError):
    """The GitHub API response cannot safely identify one update pull request."""


def _reject_json_constant(value: str) -> object:
    raise ValueError(f"non-standard JSON constant {value!r}")


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise SelectionError("pull request response contains duplicate object keys")
        result[key] = value
    return result


def _required_string(mapping: dict[str, object], key: str, context: str) -> str:
    value = mapping.get(key)
    if type(value) is not str or not value:
        raise SelectionError(f"{context}.{key} is missing or invalid")
    return value


def _required_mapping(mapping: dict[str, object], key: str, context: str) -> dict[str, object]:
    value = mapping.get(key)
    if type(value) is not dict:
        raise SelectionError(f"{context}.{key} is missing or invalid")
    return value


def read_pull_request_list(path: Path) -> object:
    """Read one bounded, regular, non-symlink GitHub API response."""

    try:
        metadata = os.lstat(path)
    except OSError as error:
        raise SelectionError("pull request response cannot be inspected") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise SelectionError("pull request response must be a regular non-symlink file")
    if metadata.st_size > MAX_RESPONSE_BYTES:
        raise SelectionError("pull request response exceeds the size limit")
    try:
        with path.open("rb") as handle:
            body = handle.read(MAX_RESPONSE_BYTES + 1)
    except OSError as error:
        raise SelectionError("pull request response cannot be read") from error
    if len(body) > MAX_RESPONSE_BYTES:
        raise SelectionError("pull request response exceeds the size limit")
    try:
        return json.loads(
            body.decode("utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_json_constant,
        )
    except SelectionError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError, ValueError) as error:
        raise SelectionError("pull request response is not valid JSON") from error


def select_update_pull_request(
    response: object,
    *,
    repository: str,
    owner: str,
    base_branch: str,
    update_branch: str,
) -> int | None:
    """Return one exact Draft PR number, or none; reject every ambiguity."""

    if not all(type(value) is str and value for value in (repository, owner, base_branch, update_branch)):
        raise SelectionError("expected repository, owner, base, or branch is invalid")
    if type(response) is not list:
        raise SelectionError("pull request response must be a JSON array")
    if not response:
        return None
    if len(response) != 1:
        raise SelectionError("expected zero or one matching open update pull request")

    pull_request = response[0]
    if type(pull_request) is not dict:
        raise SelectionError("pull request response item is invalid")
    number = pull_request.get("number")
    if type(number) is not int or number <= 0:
        raise SelectionError("pull request number is invalid")
    draft = pull_request.get("draft")
    if type(draft) is not bool or not draft:
        raise SelectionError("matching update pull request must remain a draft")

    head = _required_mapping(pull_request, "head", "pull request")
    base = _required_mapping(pull_request, "base", "pull request")
    head_repository = _required_mapping(head, "repo", "pull request.head")
    base_repository = _required_mapping(base, "repo", "pull request.base")
    head_owner = _required_mapping(head_repository, "owner", "pull request.head.repo")

    expected_head_label = f"{owner}:{update_branch}"
    if (
        _required_string(head, "ref", "pull request.head") != update_branch
        or _required_string(head, "label", "pull request.head") != expected_head_label
        or _required_string(head_repository, "full_name", "pull request.head.repo").casefold()
        != repository.casefold()
        or _required_string(head_owner, "login", "pull request.head.repo.owner").casefold()
        != owner.casefold()
        or _required_string(base, "ref", "pull request.base") != base_branch
        or _required_string(base_repository, "full_name", "pull request.base.repo").casefold()
        != repository.casefold()
    ):
        raise SelectionError("matching pull request is not the repository-owned default-branch update PR")
    return number


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="bounded GitHub REST pull-list JSON")
    parser.add_argument("--repository", required=True, help="trusted owner/repository identity")
    parser.add_argument("--owner", required=True, help="trusted repository owner identity")
    parser.add_argument("--base", required=True, help="trusted default base branch")
    parser.add_argument("--branch", required=True, help="constant repository-owned update branch")
    return parser


def main(
    argv: list[str] | None = None,
    *,
    output: TextIO | None = None,
    error_output: TextIO | None = None,
) -> int:
    """Parse trusted API output and emit a numeric PR identifier only."""

    args = build_arg_parser().parse_args(argv)
    selected_output = sys.stdout if output is None else output
    selected_error = sys.stderr if error_output is None else error_output
    try:
        number = select_update_pull_request(
            read_pull_request_list(args.input),
            repository=args.repository,
            owner=args.owner,
            base_branch=args.base,
            update_branch=args.branch,
        )
    except SelectionError as error:
        print(f"python update pull request selection failed: {error}", file=selected_error)
        return 1
    if number is not None:
        print(number, file=selected_output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
