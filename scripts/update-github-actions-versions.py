#!/usr/bin/env python3
"""Check and update GitHub Actions versions in repository workflows."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


USES_RE = re.compile(
    r"^(?P<prefix>\s*(?:-\s*)?uses:\s*)"
    r"(?P<quote>[\"']?)"
    r"(?P<value>[^\"'\s#]+)"
    r"(?P=quote)"
    r"(?P<suffix>.*)$"
)
USES_PREFIX_RE = re.compile(r"^\s*(?:-\s*)?uses:\s*(?P<rest>.+)$")
SEMVER_RE = re.compile(r"^v(?P<major>\d+)(?:\.(?P<minor>\d+))?(?:\.(?P<patch>\d+))?$")
SHA_RE = re.compile(r"^[0-9a-fA-F]{40,64}$")

MODULE_PATH = Path("modules/ModSecurity-test-Framework")
REPORT_DEFAULT = "actions-update-report.md"
WORKFLOW_GLOBS = (".github/workflows/*.yml", ".github/workflows/*.yaml")


class RateLimitError(RuntimeError):
    """GitHub API rate limit was reached."""


class ActionLookupError(RuntimeError):
    """Action metadata could not be resolved."""


@dataclass(frozen=True)
class SemverRef:
    tag: str
    major: int
    minor: int
    patch: int
    precision: int

    @property
    def key(self) -> tuple[int, int, int, int]:
        return (self.major, self.minor, self.patch, self.precision)


@dataclass
class UsesLine:
    path: Path
    line_number: int
    prefix: str
    quote: str
    value: str
    suffix: str
    newline: str

    @property
    def replacement_prefix(self) -> str:
        return f"{self.prefix}{self.quote}"

    @property
    def replacement_suffix(self) -> str:
        return f"{self.quote}{self.suffix}{self.newline}"


@dataclass
class ReportRow:
    status: str
    path: Path
    line: int
    action: str
    current_ref: str
    new_ref: str
    repository: str
    note: str


def parse_semver_ref(ref: str) -> SemverRef | None:
    match = SEMVER_RE.match(ref)
    if not match:
        return None
    minor = match.group("minor")
    patch = match.group("patch")
    precision = 1
    if minor is not None:
        precision = 2
    if patch is not None:
        precision = 3
    return SemverRef(
        tag=ref,
        major=int(match.group("major")),
        minor=int(minor or 0),
        patch=int(patch or 0),
        precision=precision,
    )


def compare_semver_refs(left: str, right: str) -> int:
    left_ref = parse_semver_ref(left)
    right_ref = parse_semver_ref(right)
    if left_ref is None or right_ref is None:
        raise ValueError(f"Cannot compare non-semver refs: {left!r}, {right!r}")
    left_key = (left_ref.major, left_ref.minor, left_ref.patch)
    right_key = (right_ref.major, right_ref.minor, right_ref.patch)
    return (left_key > right_key) - (left_key < right_key)


def action_repo_slug(action: str) -> str | None:
    parts = action.split("/")
    if len(parts) < 2 or not parts[0] or not parts[1]:
        return None
    return f"{parts[0]}/{parts[1]}"


def is_sha_ref(ref: str) -> bool:
    return bool(SHA_RE.match(ref))


def is_dynamic_uses(value: str) -> bool:
    return "${{" in value or "}}" in value


def is_local_uses(value: str) -> bool:
    return value.startswith(("./", "../"))


def is_docker_uses(value: str) -> bool:
    return value.startswith("docker://")


def split_action_ref(value: str) -> tuple[str, str] | None:
    if "@" not in value:
        return None
    action, ref = value.rsplit("@", 1)
    if not action or not ref:
        return None
    return action, ref


def parse_uses_line(path: Path, line_number: int, line: str) -> UsesLine | None:
    newline = ""
    body = line
    if body.endswith("\n"):
        newline = "\n"
        body = body[:-1]
    match = USES_RE.match(body)
    if match:
        return UsesLine(
            path=path,
            line_number=line_number,
            prefix=match.group("prefix"),
            quote=match.group("quote"),
            value=match.group("value"),
            suffix=match.group("suffix"),
            newline=newline,
        )
    loose = USES_PREFIX_RE.match(body)
    if not loose:
        return None
    rest = loose.group("rest").split("#", 1)[0].strip()
    if len(rest) >= 2 and rest[0] == rest[-1] and rest[0] in {"'", '"'}:
        rest = rest[1:-1]
    if not is_dynamic_uses(rest):
        return None
    return UsesLine(
        path=path,
        line_number=line_number,
        prefix=body[: body.find("uses:") + len("uses:")],
        quote="",
        value=rest,
        suffix="",
        newline=newline,
    )


def workflow_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for pattern in WORKFLOW_GLOBS:
        files.extend(root.glob(pattern))
    module_root = root / MODULE_PATH
    if module_root.exists():
        for pattern in WORKFLOW_GLOBS:
            files.extend(module_root.glob(pattern))
    return sorted(path for path in files if path.is_file())


def path_repository(root: Path, path: Path) -> str:
    rel = path.resolve().relative_to(root.resolve())
    return "module" if rel.parts[: len(MODULE_PATH.parts)] == MODULE_PATH.parts else "main"


def is_module_submodule(root: Path) -> bool:
    module_root = root / MODULE_PATH
    if not module_root.exists():
        return False
    try:
        result = subprocess.run(
            ["git", "submodule", "status", "--", str(MODULE_PATH)],
            cwd=root,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except OSError:
        return False
    return result.returncode == 0 and bool(result.stdout.strip())


def select_latest_ref(current_ref: str, candidate_tags: Iterable[str]) -> str | None:
    current = parse_semver_ref(current_ref)
    if current is None:
        return None
    candidates = [parsed for tag in candidate_tags if (parsed := parse_semver_ref(tag))]
    if not candidates:
        return None
    if current.precision == 1:
        major_aliases = [candidate for candidate in candidates if candidate.precision == 1]
        if major_aliases:
            candidates = major_aliases
    return max(candidates, key=lambda candidate: candidate.key).tag


class GitHubActionResolver:
    def __init__(self, token: str | None = None, api_url: str | None = None) -> None:
        self.token = token
        self.api_url = (api_url or os.environ.get("GITHUB_API_URL") or "https://api.github.com").rstrip("/")
        self.cache: dict[str, tuple[list[str], str]] = {}
        self.rate_limited = False

    def get_semver_refs(self, action: str) -> tuple[list[str], str]:
        slug = action_repo_slug(action)
        if slug is None:
            raise ActionLookupError(f"Cannot determine repository for action {action!r}")
        if slug in self.cache:
            return self.cache[slug]
        releases = self._release_tags(slug)
        if releases:
            result = (releases, "releases")
        else:
            result = (self._tag_refs(slug), "tags")
        self.cache[slug] = result
        return result

    def _request_json(self, path: str) -> tuple[object, dict[str, str]]:
        url = f"{self.api_url}{path}"
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "modsecurity-actions-version-updater",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))
                return data, {key.lower(): value for key, value in response.headers.items()}
        except urllib.error.HTTPError as error:
            body = error.read().decode("utf-8", errors="replace")
            remaining = error.headers.get("X-RateLimit-Remaining")
            if error.code in {403, 429} and (remaining == "0" or "rate limit" in body.lower()):
                self.rate_limited = True
                raise RateLimitError("GitHub API rate limit reached") from error
            raise ActionLookupError(f"GitHub API returned HTTP {error.code}: {body[:200]}") from error
        except (OSError, json.JSONDecodeError) as error:
            raise ActionLookupError(str(error)) from error

    def _paged(self, path: str) -> list[object]:
        items: list[object] = []
        page = 1
        separator = "&" if "?" in path else "?"
        while True:
            data, _headers = self._request_json(f"{path}{separator}per_page=100&page={page}")
            if not isinstance(data, list):
                raise ActionLookupError("GitHub API returned a non-list response")
            items.extend(data)
            if len(data) < 100:
                return items
            page += 1

    def _release_tags(self, slug: str) -> list[str]:
        encoded = urllib.parse.quote(slug, safe="/")
        releases = self._paged(f"/repos/{encoded}/releases")
        stable: list[str] = []
        prerelease: list[str] = []
        for release in releases:
            if not isinstance(release, dict) or release.get("draft"):
                continue
            tag = str(release.get("tag_name") or "")
            if not parse_semver_ref(tag):
                continue
            if release.get("prerelease"):
                prerelease.append(tag)
            else:
                stable.append(tag)
        return stable or prerelease

    def _tag_refs(self, slug: str) -> list[str]:
        encoded = urllib.parse.quote(slug, safe="/")
        tags = self._paged(f"/repos/{encoded}/tags")
        result: list[str] = []
        for tag in tags:
            if isinstance(tag, dict):
                name = str(tag.get("name") or "")
                if parse_semver_ref(name):
                    result.append(name)
        return result


def replacement_line(uses_line: UsesLine, new_ref: str) -> str:
    action_ref = split_action_ref(uses_line.value)
    if action_ref is None:
        return uses_line.prefix + uses_line.quote + uses_line.value + uses_line.replacement_suffix
    action, _old_ref = action_ref
    return f"{uses_line.replacement_prefix}{action}@{new_ref}{uses_line.replacement_suffix}"


def analyze_uses(
    root: Path,
    uses_line: UsesLine,
    resolver: GitHubActionResolver,
    module_is_submodule: bool,
    write: bool,
    allow_submodule_write: bool,
) -> tuple[ReportRow, str | None]:
    repository = path_repository(root, uses_line.path)
    rel_path = uses_line.path.resolve().relative_to(root.resolve())
    value = uses_line.value

    def row(status: str, action: str = value, current: str = "", new: str = "", note: str = "") -> ReportRow:
        return ReportRow(status, rel_path, uses_line.line_number, action, current, new, repository, note)

    if is_dynamic_uses(value):
        return row("Skipped dynamic", note="uses contains a GitHub expression"), None
    if is_local_uses(value):
        return row("Skipped local", note="local action path"), None
    if is_docker_uses(value):
        return row("Skipped docker", note="Docker action reference"), None

    action_ref = split_action_ref(value)
    if action_ref is None:
        return row("Unknown", note="uses entry has no @ref"), None
    action, current_ref = action_ref
    if is_dynamic_uses(action) or is_dynamic_uses(current_ref):
        return row("Skipped dynamic", action, current_ref, note="uses contains a GitHub expression"), None
    if is_sha_ref(current_ref):
        return row("Pinned SHA", action, current_ref, note="SHA-pinned action is not updated automatically"), None

    current_semver = parse_semver_ref(current_ref)
    if current_semver is None:
        return row("Unknown", action, current_ref, note="current ref is not a supported semver tag"), None

    try:
        candidate_refs, source = resolver.get_semver_refs(action)
    except RateLimitError as error:
        return row("Error", action, current_ref, note=str(error)), None
    except ActionLookupError as error:
        return row("Error", action, current_ref, note=str(error)), None

    latest_ref = select_latest_ref(current_ref, candidate_refs)
    if latest_ref is None:
        return row("Unknown", action, current_ref, note=f"no semver refs found from {source}"), None

    latest_semver = parse_semver_ref(latest_ref)
    if latest_semver is None:
        return row("Unknown", action, current_ref, note=f"latest ref is not semver: {latest_ref}"), None

    current_key = (current_semver.major, current_semver.minor, current_semver.patch)
    latest_key = (latest_semver.major, latest_semver.minor, latest_semver.patch)
    if latest_key <= current_key:
        if current_ref not in set(candidate_refs):
            return row(
                "Unknown",
                action,
                current_ref,
                latest_ref,
                f"current ref was not found in {source}; not downgrading",
            ), None
        return row("OK", action, current_ref, latest_ref, f"latest from {source}"), None

    if write and repository == "module" and module_is_submodule and not allow_submodule_write:
        return row(
            "Skipped submodule write",
            action,
            current_ref,
            latest_ref,
            "module is a submodule; set SUBMODULE_UPDATE_TOKEN to write module updates",
        ), None

    return row("Updated", action, current_ref, latest_ref, f"latest from {source}"), latest_ref


def scan_workflows(
    root: Path,
    resolver: GitHubActionResolver,
    write: bool = False,
    allow_submodule_write: bool = False,
) -> tuple[list[ReportRow], bool]:
    root = root.resolve()
    rows: list[ReportRow] = []
    replacements: dict[Path, dict[int, str]] = {}
    module_submodule = is_module_submodule(root)

    for path in workflow_files(root):
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        for index, line in enumerate(lines, start=1):
            uses_line = parse_uses_line(path, index, line)
            if uses_line is None:
                continue
            row, new_ref = analyze_uses(
                root=root,
                uses_line=uses_line,
                resolver=resolver,
                module_is_submodule=module_submodule,
                write=write,
                allow_submodule_write=allow_submodule_write,
            )
            rows.append(row)
            if new_ref and row.status == "Updated":
                replacements.setdefault(path, {})[index] = replacement_line(uses_line, new_ref)

    if write and not resolver.rate_limited:
        for path, line_replacements in replacements.items():
            lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
            for line_number, new_line in line_replacements.items():
                lines[line_number - 1] = new_line
            path.write_text("".join(lines), encoding="utf-8")

    return rows, module_submodule


def markdown_cell(value: object) -> str:
    return str(value if value is not None else "").replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def render_report(rows: list[ReportRow], module_submodule: bool) -> str:
    statuses = [
        "Updated",
        "OK",
        "Pinned SHA",
        "Skipped local",
        "Skipped docker",
        "Skipped dynamic",
        "Skipped submodule write",
        "Unknown",
        "Error",
    ]
    counts = dict.fromkeys(statuses, 0)
    for row in rows:
        counts[row.status] = counts.get(row.status, 0) + 1

    lines = [
        "# GitHub Actions update report",
        "",
        "This report scans `uses:` entries in root workflow files and the vendored framework module.",
        "Local actions, Docker actions, dynamic expressions, and SHA-pinned actions are not updated automatically.",
        "",
        "## Summary",
        "",
        f"- Found `uses:` entries: {len(rows)}",
        f"- Updated entries: {counts.get('Updated', 0)}",
        f"- Already current entries: {counts.get('OK', 0)}",
        f"- SHA-pinned entries: {counts.get('Pinned SHA', 0)}",
        (
            "- Skipped local/Docker/dynamic entries: "
            f"{counts.get('Skipped local', 0) + counts.get('Skipped docker', 0) + counts.get('Skipped dynamic', 0)}"
        ),
        f"- Skipped submodule writes: {counts.get('Skipped submodule write', 0)}",
        f"- Unknown entries: {counts.get('Unknown', 0)}",
        f"- Errors: {counts.get('Error', 0)}",
        f"- Framework module is submodule: {'yes' if module_submodule else 'no'}",
        "",
        "## Entries",
        "",
        "| Status | File | Line | Action | Current ref | New ref | Repository | Note |",
        "| --- | --- | ---: | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row.status),
                    markdown_cell(row.path.as_posix()),
                    markdown_cell(row.line),
                    markdown_cell(row.action),
                    markdown_cell(row.current_ref),
                    markdown_cell(row.new_ref),
                    markdown_cell(row.repository),
                    markdown_cell(row.note),
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def write_report(path: Path, rows: list[ReportRow], module_submodule: bool) -> None:
    path.write_text(render_report(rows, module_submodule), encoding="utf-8")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="fail when updates are available")
    mode.add_argument("--write", action="store_true", help="write available updates to workflow files")
    parser.add_argument("--report", default=REPORT_DEFAULT, help="write a Markdown report to this path")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    root = Path.cwd()
    token = os.environ.get("GITHUB_TOKEN")
    allow_submodule_write = bool(os.environ.get("SUBMODULE_UPDATE_TOKEN"))
    resolver = GitHubActionResolver(token=token)
    rows, module_submodule = scan_workflows(
        root=root,
        resolver=resolver,
        write=args.write,
        allow_submodule_write=allow_submodule_write,
    )
    if args.report:
        write_report(Path(args.report), rows, module_submodule)
    if args.check and any(row.status == "Updated" for row in rows):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
