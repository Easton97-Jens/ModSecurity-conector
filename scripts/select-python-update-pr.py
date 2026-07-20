#!/usr/bin/env python3
"""Fail closed when selecting the repository-owned Python update pull request."""

from __future__ import annotations

import argparse
import json
import sys
from typing import BinaryIO, TextIO, cast


MAX_RESPONSE_BYTES = 2 * 1024 * 1024
PULL_REQUEST_CONTEXT = "pull request"
PULL_REQUEST_HEAD_CONTEXT = f"{PULL_REQUEST_CONTEXT}.head"
PULL_REQUEST_HEAD_REPOSITORY_CONTEXT = f"{PULL_REQUEST_HEAD_CONTEXT}.repo"
PULL_REQUEST_BASE_CONTEXT = f"{PULL_REQUEST_CONTEXT}.base"
PULL_REQUEST_BASE_REPOSITORY_CONTEXT = f"{PULL_REQUEST_BASE_CONTEXT}.repo"


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


def read_pull_request_list(stream: BinaryIO) -> object:
    """Read one bounded GitHub API response from the trusted workflow pipe."""

    try:
        body = stream.read(MAX_RESPONSE_BYTES + 1)
    except OSError as error:
        raise SelectionError("pull request response cannot be read") from error
    if type(body) is not bytes:
        raise SelectionError("pull request response is not bytes")
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
    except (RecursionError, ValueError) as error:
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
    pull_requests = cast(list[object], response)
    if not pull_requests:
        return None
    if len(pull_requests) != 1:
        raise SelectionError("expected zero or one matching open update pull request")

    pull_request = pull_requests[0]
    if type(pull_request) is not dict:
        raise SelectionError("pull request response item is invalid")
    number = pull_request.get("number")
    if type(number) is not int or number <= 0:
        raise SelectionError("pull request number is invalid")
    draft = pull_request.get("draft")
    if type(draft) is not bool or not draft:
        raise SelectionError("matching update pull request must remain a draft")

    head = _required_mapping(pull_request, "head", PULL_REQUEST_CONTEXT)
    base = _required_mapping(pull_request, "base", PULL_REQUEST_CONTEXT)
    head_repository = _required_mapping(head, "repo", PULL_REQUEST_HEAD_CONTEXT)
    base_repository = _required_mapping(base, "repo", PULL_REQUEST_BASE_CONTEXT)
    head_owner = _required_mapping(
        head_repository,
        "owner",
        PULL_REQUEST_HEAD_REPOSITORY_CONTEXT,
    )

    expected_head_label = f"{owner}:{update_branch}"
    if (
        _required_string(head, "ref", PULL_REQUEST_HEAD_CONTEXT) != update_branch
        or _required_string(head, "label", PULL_REQUEST_HEAD_CONTEXT) != expected_head_label
        or _required_string(
            head_repository,
            "full_name",
            PULL_REQUEST_HEAD_REPOSITORY_CONTEXT,
        ).casefold()
        != repository.casefold()
        or _required_string(
            head_owner,
            "login",
            f"{PULL_REQUEST_HEAD_REPOSITORY_CONTEXT}.owner",
        ).casefold()
        != owner.casefold()
        or _required_string(base, "ref", PULL_REQUEST_BASE_CONTEXT) != base_branch
        or _required_string(
            base_repository,
            "full_name",
            PULL_REQUEST_BASE_REPOSITORY_CONTEXT,
        ).casefold()
        != repository.casefold()
    ):
        raise SelectionError("matching pull request is not the repository-owned default-branch update PR")
    return number


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True, help="trusted owner/repository identity")
    parser.add_argument("--owner", required=True, help="trusted repository owner identity")
    parser.add_argument("--base", required=True, help="trusted default base branch")
    parser.add_argument("--branch", required=True, help="constant repository-owned update branch")
    return parser


def main(
    argv: list[str] | None = None,
    *,
    input_stream: BinaryIO | None = None,
    output: TextIO | None = None,
    error_output: TextIO | None = None,
) -> int:
    """Parse trusted API output and emit a numeric PR identifier only."""

    args = build_arg_parser().parse_args(argv)
    selected_input = sys.stdin.buffer if input_stream is None else input_stream
    selected_output = sys.stdout if output is None else output
    selected_error = sys.stderr if error_output is None else error_output
    try:
        number = select_update_pull_request(
            read_pull_request_list(selected_input),
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
