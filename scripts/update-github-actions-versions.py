#!/usr/bin/env python3
"""Safely resolve, validate, and apply Parent CI tool updates.

The updater intentionally has a narrow, fail-closed scope:

* only the checked-in Parent action and security-tool allowlists are eligible;
* GitHub metadata always comes from the fixed public GitHub API endpoint;
* immutable release tags are resolved to full commit IDs before use;
* tool assets must have GitHub's published SHA-256 digest; and
* an apply operation can alter only the Parent workflow files and this lock.

It never follows redirects, accepts an API URL override, writes a submodule,
or performs Git/GitHub delivery.  The workflow separates resolution,
read-only validation, and the narrowly privileged publisher.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Mapping

import yaml
from yaml.nodes import MappingNode, Node, ScalarNode, SequenceNode


CANONICAL_GITHUB_API_URL = "https://api.github.com"
LOCK_RELATIVE_PATH = Path("ci/tooling/security-tools.lock.yml")
WORKFLOWS_RELATIVE_DIRECTORY = Path(".github/workflows")
MAX_METADATA_BYTES = 2 * 1024 * 1024
MAX_CANDIDATE_BYTES = 2 * 1024 * 1024
MAX_TAG_PAGES = 10
MAX_TAG_DEREFERENCES = 4
NETWORK_TIMEOUT_SECONDS = 20
MAX_WORKFLOW_YAML_NODES = 100_000
SHA_RE = re.compile(r"^[a-f0-9]{40}$", re.ASCII)
SHA256_RE = re.compile(r"^[a-f0-9]{64}$", re.ASCII)
VERSION_RE = re.compile(r"^v(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)$", re.ASCII)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$", re.ASCII)
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9_.-]*/[a-z0-9][a-z0-9_.-]*$", re.ASCII)
ASSET_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$", re.ASCII)
EXECUTABLE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$", re.ASCII)
USES_PREFIX = re.compile(r"^\s*(?:-\s*)?uses:\s*", re.ASCII)
REMOTE_USE_RE = re.compile(
    r"^(?P<prefix>\s*(?:-\s*)?uses:\s*)"
    r"(?P<action>[a-z0-9][a-z0-9_.-]*/[a-z0-9][a-z0-9_.-]*(?:/[a-z0-9][a-z0-9_.-]*)*)"
    r"@(?P<sha>[a-f0-9]{40})"
    r"\s+#\s*(?P<version>v(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*))\s*$",
    re.ASCII,
)


class UpdaterError(RuntimeError):
    """The updater cannot safely continue."""


class LockError(UpdaterError):
    """The checked-in lock is malformed or outside the updater allowlist."""


class MetadataError(UpdaterError):
    """Official metadata was malformed, incomplete, redirected, or stale."""


class CandidateError(UpdaterError):
    """A cross-job candidate is malformed or no longer matches provenance."""


class WorkflowContractError(UpdaterError):
    """A workflow action reference is not an exact lock-backed SHA pin."""


@dataclass(frozen=True, order=True)
class Version:
    """An exact stable release tag supported by this updater."""

    major: int
    minor: int
    patch: int

    @classmethod
    def parse(cls, value: object, *, context: str) -> "Version":
        if type(value) is not str:
            raise MetadataError(f"{context} version is not a string")
        match = VERSION_RE.fullmatch(value)
        if match is None:
            raise MetadataError(f"{context} version is not an exact stable vM.m.p tag")
        return cls(int(match.group("major")), int(match.group("minor")), int(match.group("patch")))

    def __str__(self) -> str:
        return f"v{self.major}.{self.minor}.{self.patch}"


@dataclass(frozen=True)
class ActionRecord:
    """One immutable workflow-action record from the allowlisted lock."""

    name: str
    version: str
    commit_sha: str
    upstream: str

    def to_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "version": self.version,
            "commit_sha": self.commit_sha,
            "upstream": self.upstream,
        }


@dataclass(frozen=True)
class ToolRecord:
    """The immutable fields needed to provision one security-tool release."""

    name: str
    version: str
    release_commit: str
    asset: str
    url: str
    sha256: str
    executable: str
    upstream: str

    def to_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "version": self.version,
            "release_commit": self.release_commit,
            "asset": self.asset,
            "url": self.url,
            "sha256": self.sha256,
            "executable": self.executable,
            "upstream": self.upstream,
        }


@dataclass(frozen=True)
class LockState:
    """A validated, narrowly parsed security-tools lock document."""

    text: str
    checked_at: str
    actions: dict[str, ActionRecord]
    tools: dict[str, ToolRecord]


@dataclass(frozen=True)
class ActionResolution:
    """The current and authoritative target identity for one action."""

    current: ActionRecord
    target: ActionRecord

    def to_dict(self) -> dict[str, dict[str, str]]:
        return {"current": self.current.to_dict(), "target": self.target.to_dict()}

    @property
    def changes(self) -> bool:
        return self.current != self.target


@dataclass(frozen=True)
class ToolResolution:
    """The current and authoritative target identity for one tool release."""

    current: ToolRecord
    target: ToolRecord

    def to_dict(self) -> dict[str, dict[str, str]]:
        return {"current": self.current.to_dict(), "target": self.target.to_dict()}

    @property
    def changes(self) -> bool:
        return self.current != self.target


@dataclass(frozen=True)
class Candidate:
    """A cross-job provenance record which is revalidated before writing."""

    resolved_at: str
    actions: tuple[ActionResolution, ...]
    tools: tuple[ToolResolution, ...]

    @property
    def update_available(self) -> bool:
        return any(item.changes for item in (*self.actions, *self.tools))

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "source": CANONICAL_GITHUB_API_URL,
            "resolved_at": self.resolved_at,
            "update_available": self.update_available,
            "actions": [item.to_dict() for item in self.actions],
            "tools": [item.to_dict() for item in self.tools],
        }


@dataclass(frozen=True)
class ToolPolicy:
    """A tool-specific asset contract; generic globbing is deliberately absent."""

    slug: str
    executable: str
    asset_template: str

    def asset_for(self, version: str) -> str:
        return self.asset_template.format(version=version.removeprefix("v"))


TOOL_POLICIES: dict[str, ToolPolicy] = {
    "actionlint": ToolPolicy(
        slug="rhysd/actionlint",
        executable="actionlint",
        asset_template="actionlint_{version}_linux_amd64.tar.gz",
    ),
    "zizmor": ToolPolicy(
        slug="zizmorcore/zizmor",
        executable="zizmor",
        asset_template="zizmor-x86_64-unknown-linux-gnu.tar.gz",
    ),
    "gitleaks": ToolPolicy(
        slug="gitleaks/gitleaks",
        executable="gitleaks",
        asset_template="gitleaks_{version}_linux_x64.tar.gz",
    ),
}
SUPPORTED_ACTIONS = frozenset(
    {
        "actions/checkout",
        "actions/setup-python",
        "actions/setup-go",
        "actions/github-script",
        "actions/upload-artifact",
        "actions/download-artifact",
        "github/codeql-action",
        "google/osv-scanner-action",
        "ossf/scorecard-action",
    }
)
SUPPORTED_TOOLS = frozenset(TOOL_POLICIES)
# Actions are provenance-bound to immutable Git tags, never GitHub's
# ``releases/latest`` endpoint.  In particular github/codeql-action publishes
# bundle releases whose tag names are not workflow-action vM.m.p tags.
ACTION_RESOLUTION_SOURCES = {name: "immutable_git_tags" for name in SUPPORTED_ACTIONS}


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Reject metadata redirects instead of silently trusting another host."""

    def redirect_request(self, request, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        raise MetadataError("redirects are not allowed for GitHub release metadata")


def _required_string(mapping: Mapping[str, object], key: str, context: str) -> str:
    value = mapping.get(key)
    if type(value) is not str or not value:
        raise MetadataError(f"{context}.{key} is missing or invalid")
    return value


def _required_bool(mapping: Mapping[str, object], key: str, context: str) -> bool:
    value = mapping.get(key)
    if type(value) is not bool:
        raise MetadataError(f"{context}.{key} is missing or invalid")
    return value


def _reject_json_constant(value: str) -> object:
    raise ValueError(f"non-standard JSON constant {value!r}")


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise MetadataError("metadata JSON contains duplicate object keys")
        result[key] = value
    return result


def _decode_json(body: bytes, *, context: str) -> object:
    try:
        return json.loads(
            body.decode("utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_json_constant,
        )
    except MetadataError:
        raise
    except (RecursionError, UnicodeDecodeError, ValueError) as error:
        raise MetadataError(f"{context} is not valid JSON") from error


def _response_header(response: object, name: str) -> str | None:
    headers = getattr(response, "headers", None)
    if headers is None:
        return None
    value = headers.get(name) if hasattr(headers, "get") else None
    if value is not None:
        return str(value)
    if hasattr(headers, "items"):
        for key, candidate in headers.items():
            if str(key).casefold() == name.casefold():
                return str(candidate)
    return None


def _read_json_response(response: object, *, expected_url: str, context: str) -> object:
    status = getattr(response, "status", None)
    if status is None and hasattr(response, "getcode"):
        status = response.getcode()
    if status is not None and status != 200:
        raise MetadataError(f"{context} did not return HTTP 200")
    actual_url = response.geturl() if hasattr(response, "geturl") else None
    if actual_url != expected_url:
        raise MetadataError(f"{context} was redirected")
    content_type = _response_header(response, "Content-Type")
    if content_type is None or content_type.split(";", 1)[0].strip().casefold() != "application/json":
        raise MetadataError(f"{context} is not application/json")
    length = _response_header(response, "Content-Length")
    if length is not None:
        if not re.fullmatch(r"\d+", length.strip(), re.ASCII) or int(length) > MAX_METADATA_BYTES:
            raise MetadataError(f"{context} has an invalid Content-Length")
    if not hasattr(response, "read"):
        raise MetadataError(f"{context} cannot be read")
    body = response.read(MAX_METADATA_BYTES + 1)
    if type(body) is not bytes or len(body) > MAX_METADATA_BYTES:
        raise MetadataError(f"{context} exceeds its size limit")
    if length is not None and len(body) != int(length):
        raise MetadataError(f"{context} was truncated")
    return _decode_json(body, context=context)


class OfficialGitHubApi:
    """A small fixed-endpoint client for public GitHub release provenance."""

    def __init__(self, opener: object | None = None) -> None:
        self._opener = opener or urllib.request.build_opener(NoRedirectHandler())

    def _request_json(self, path: str) -> object:
        if not path.startswith("/") or ".." in path or "#" in path:
            raise MetadataError("GitHub API path is invalid")
        url = f"{CANONICAL_GITHUB_API_URL}{path}"
        request = urllib.request.Request(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "Accept-Encoding": "identity",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "modsecurity-conector-ci-tool-updater",
            },
            method="GET",
        )
        response = None
        try:
            if not hasattr(self._opener, "open"):
                raise MetadataError("GitHub metadata opener is invalid")
            response = self._opener.open(request, timeout=NETWORK_TIMEOUT_SECONDS)
            return _read_json_response(response, expected_url=url, context="GitHub API response")
        except MetadataError:
            raise
        except urllib.error.HTTPError as error:
            raise MetadataError(f"GitHub API returned HTTP {error.code}") from error
        except OSError as error:
            raise MetadataError("GitHub API request failed") from error
        finally:
            if response is not None and hasattr(response, "close"):
                response.close()

    @staticmethod
    def _validate_slug(slug: str) -> None:
        if not SLUG_RE.fullmatch(slug):
            raise MetadataError("GitHub repository slug is invalid")

    def stable_tags(self, slug: str) -> list[str]:
        """Return all bounded, exact stable tags found through the official API."""

        self._validate_slug(slug)
        tags: set[str] = set()
        encoded = urllib.parse.quote(slug, safe="/")
        for page in range(1, MAX_TAG_PAGES + 1):
            response = self._request_json(f"/repos/{encoded}/tags?per_page=100&page={page}")
            if type(response) is not list:
                raise MetadataError(f"{slug} tag response is not a list")
            for index, item in enumerate(response):
                if type(item) is not dict:
                    raise MetadataError(f"{slug} tag record {index} is invalid")
                name = _required_string(item, "name", f"{slug} tag record {index}")
                try:
                    Version.parse(name, context=f"{slug} tag")
                except MetadataError:
                    continue
                tags.add(name)
            if len(response) < 100:
                return sorted(tags, key=lambda tag: Version.parse(tag, context=f"{slug} tag"))
        raise MetadataError(f"{slug} tag listing exceeded {MAX_TAG_PAGES} pages")

    def tag_commit(self, slug: str, tag: str) -> str:
        """Resolve a lightweight or annotated tag to one immutable commit SHA."""

        self._validate_slug(slug)
        Version.parse(tag, context=f"{slug} tag")
        encoded_slug = urllib.parse.quote(slug, safe="/")
        encoded_tag = urllib.parse.quote(tag, safe="")
        response = self._request_json(f"/repos/{encoded_slug}/git/ref/tags/{encoded_tag}")
        if type(response) is not dict:
            raise MetadataError(f"{slug} tag reference is invalid")
        current: Mapping[str, object] = response
        for _ in range(MAX_TAG_DEREFERENCES + 1):
            object_record = current.get("object")
            if type(object_record) is not dict:
                raise MetadataError(f"{slug} tag object is invalid")
            kind = _required_string(object_record, "type", f"{slug} tag object")
            sha = _required_string(object_record, "sha", f"{slug} tag object")
            if not SHA_RE.fullmatch(sha):
                raise MetadataError(f"{slug} tag object SHA is invalid")
            if kind == "commit":
                return sha
            if kind != "tag":
                raise MetadataError(f"{slug} tag object has unsupported type {kind!r}")
            tagged = self._request_json(f"/repos/{encoded_slug}/git/tags/{sha}")
            if type(tagged) is not dict:
                raise MetadataError(f"{slug} annotated tag object is invalid")
            current = tagged
        raise MetadataError(f"{slug} tag exceeded nested-tag limit")

    def latest_release(self, slug: str) -> Mapping[str, object]:
        """Return one non-draft/non-prerelease GitHub release record."""

        self._validate_slug(slug)
        encoded = urllib.parse.quote(slug, safe="/")
        response = self._request_json(f"/repos/{encoded}/releases/latest")
        if type(response) is not dict:
            raise MetadataError(f"{slug} latest release is invalid")
        if _required_bool(response, "draft", f"{slug} latest release"):
            raise MetadataError(f"{slug} latest release is a draft")
        if _required_bool(response, "prerelease", f"{slug} latest release"):
            raise MetadataError(f"{slug} latest release is a prerelease")
        return response


def _section_body(text: str, section: str) -> str:
    match = re.search(
        rf"(?ms)^{re.escape(section)}:\n(?P<body>.*?)(?=^[A-Za-z][A-Za-z0-9_-]*:\s*$|\Z)",
        text,
    )
    if match is None:
        raise LockError(f"lock lacks required {section!r} section")
    return match.group("body")


def _parse_section_records(text: str, section: str) -> dict[str, dict[str, str]]:
    body = _section_body(text, section)
    records: dict[str, dict[str, str]] = {}
    pattern = re.compile(
        r"(?m)^  (?P<name>[A-Za-z0-9][A-Za-z0-9_./-]*):\n"
        r"(?P<body>(?:^    [^\n]*(?:\n|$))*)"
    )
    for match in pattern.finditer(body):
        name = match.group("name")
        if name in records:
            raise LockError(f"{section}.{name} is duplicated")
        fields: dict[str, str] = {}
        for field in re.finditer(r"(?m)^    (?P<key>[a-z][a-z0-9_]*): (?P<value>.+)$", match.group("body")):
            key = field.group("key")
            if key in fields:
                raise LockError(f"{section}.{name}.{key} is duplicated")
            fields[key] = field.group("value").strip()
        records[name] = fields
    if not records:
        raise LockError(f"{section} has no records")
    return records


def _lock_version(value: object, *, context: str) -> str:
    try:
        return str(Version.parse(value, context=context))
    except MetadataError as error:
        raise LockError(str(error)) from error


def _lock_sha(value: object, *, context: str, sha256: bool = False) -> str:
    if type(value) is not str or not (SHA256_RE if sha256 else SHA_RE).fullmatch(value):
        algorithm = "SHA-256" if sha256 else "commit SHA"
        raise LockError(f"{context} has an invalid {algorithm}")
    return value


def _exact_upstream(slug: str) -> str:
    return f"https://github.com/{slug}"


def _action_record(name: str, values: Mapping[str, str]) -> ActionRecord:
    required = {"version", "commit_sha", "upstream"}
    missing = required.difference(values)
    if missing:
        raise LockError(f"pinned_actions.{name} lacks {', '.join(sorted(missing))}")
    unexpected = set(values).difference(required)
    if unexpected:
        raise LockError(f"pinned_actions.{name} has unsupported fields: {', '.join(sorted(unexpected))}")
    if name not in SUPPORTED_ACTIONS or not SLUG_RE.fullmatch(name):
        raise LockError(f"pinned_actions.{name} is outside the Parent updater allowlist")
    upstream = values["upstream"]
    if upstream != _exact_upstream(name):
        raise LockError(f"pinned_actions.{name}.upstream is not its exact GitHub repository")
    return ActionRecord(
        name=name,
        version=_lock_version(values["version"], context=f"pinned_actions.{name}"),
        commit_sha=_lock_sha(values["commit_sha"], context=f"pinned_actions.{name}.commit_sha"),
        upstream=upstream,
    )


def _tool_record(name: str, values: Mapping[str, str]) -> ToolRecord:
    required = {"version", "release_commit", "asset", "url", "sha256", "executable", "upstream"}
    missing = required.difference(values)
    if missing:
        raise LockError(f"tools.{name} lacks {', '.join(sorted(missing))}")
    unexpected = set(values).difference(required | {"license", "purpose", "permissions"})
    if unexpected:
        raise LockError(f"tools.{name} has unsupported fields: {', '.join(sorted(unexpected))}")
    policy = TOOL_POLICIES.get(name)
    if policy is None:
        raise LockError(f"tools.{name} is outside the Parent updater allowlist")
    version = _lock_version(values["version"], context=f"tools.{name}")
    asset = values["asset"]
    if not ASSET_RE.fullmatch(asset) or asset != policy.asset_for(version):
        raise LockError(f"tools.{name}.asset does not match the fixed platform asset contract")
    upstream = values["upstream"]
    if upstream != _exact_upstream(policy.slug):
        raise LockError(f"tools.{name}.upstream is not its exact GitHub repository")
    url = values["url"]
    expected_url = f"{upstream}/releases/download/{version}/{asset}"
    if url != expected_url:
        raise LockError(f"tools.{name}.url is not the exact official release-asset URL")
    executable = values["executable"]
    if executable != policy.executable or not EXECUTABLE_RE.fullmatch(executable):
        raise LockError(f"tools.{name}.executable violates its fixed tool policy")
    return ToolRecord(
        name=name,
        version=version,
        release_commit=_lock_sha(values["release_commit"], context=f"tools.{name}.release_commit"),
        asset=asset,
        url=url,
        sha256=_lock_sha(values["sha256"], context=f"tools.{name}.sha256", sha256=True),
        executable=executable,
        upstream=upstream,
    )


def parse_lock_text(text: str) -> LockState:
    """Parse the small checked-in lock without executing YAML features."""

    if "\x00" in text or len(text.encode("utf-8")) > MAX_CANDIDATE_BYTES:
        raise LockError("security-tool lock is malformed or too large")
    if len(re.findall(r"(?m)^schema_version: 1$", text)) != 1:
        raise LockError("security-tool lock must use exactly schema_version 1")
    checked = re.findall(r'(?m)^checked_at: "(?P<date>[^\"]+)"$', text)
    if len(checked) != 1 or not DATE_RE.fullmatch(checked[0]):
        raise LockError("lock checked_at must contain exactly one ISO date")
    action_fields = _parse_section_records(text, "pinned_actions")
    tool_fields = _parse_section_records(text, "tools")
    if set(action_fields) != SUPPORTED_ACTIONS:
        raise LockError("pinned_actions must exactly match the Parent action allowlist")
    if set(tool_fields) != SUPPORTED_TOOLS:
        raise LockError("tools must exactly match the Parent security-tool allowlist")
    actions = {name: _action_record(name, fields) for name, fields in action_fields.items()}
    tools = {name: _tool_record(name, fields) for name, fields in tool_fields.items()}
    return LockState(text=text, checked_at=checked[0], actions=actions, tools=tools)


def _safe_repository_file(root: Path, relative: Path) -> Path:
    if root != root.resolve() or relative.is_absolute() or ".." in relative.parts:
        raise UpdaterError("unsafe repository path")
    path = root / relative
    try:
        metadata = path.lstat()
    except OSError as error:
        raise UpdaterError(f"required repository file is unavailable: {relative}") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise UpdaterError(f"repository target is not a regular file: {relative}")
    try:
        path.resolve(strict=True).relative_to(root)
    except (OSError, ValueError) as error:
        raise UpdaterError(f"repository target escapes the Parent root: {relative}") from error
    return path


def read_lock(root: Path) -> LockState:
    path = _safe_repository_file(root, LOCK_RELATIVE_PATH)
    try:
        return parse_lock_text(path.read_text(encoding="utf-8"))
    except UnicodeDecodeError as error:
        raise LockError("security-tool lock is not UTF-8") from error


@dataclass(frozen=True)
class WorkflowUse:
    path: Path
    line_index: int
    action_path: str
    slug: str
    commit_sha: str
    version: str


def workflow_paths(root: Path) -> list[Path]:
    directory = root / WORKFLOWS_RELATIVE_DIRECTORY
    try:
        metadata = directory.lstat()
    except OSError as error:
        raise WorkflowContractError("Parent workflow directory is unavailable") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise WorkflowContractError("Parent workflow directory is not a real directory")
    paths: list[Path] = []
    for pattern in ("*.yml", "*.yaml"):
        for path in directory.glob(pattern):
            relative = path.relative_to(root)
            _safe_repository_file(root, relative)
            paths.append(path)
    if not paths:
        raise WorkflowContractError("Parent workflow directory has no workflow files")
    return sorted(paths)


def _semantic_uses_key_positions(path: Path, text: str) -> list[tuple[int, int]]:
    """Parse YAML safely and return every semantic ``uses`` mapping-key position.

    The textual pin format is deliberately canonical, but YAML permits quoted
    escapes, tags, explicit keys, and flow maps that can decode to the same
    key.  A node tree gives us the decoded key semantics without evaluating
    arbitrary YAML objects; canonical text is enforced separately below.
    """

    try:
        document = yaml.compose(text, Loader=yaml.BaseLoader)
    except (RecursionError, yaml.YAMLError) as error:
        raise WorkflowContractError(f"{path} is not valid YAML") from error
    if document is None:
        raise WorkflowContractError(f"{path} is empty YAML")

    positions: list[tuple[int, int]] = []
    visited: set[int] = set()
    node_count = 0

    def visit(node: Node) -> None:
        nonlocal node_count
        identity = id(node)
        if identity in visited:
            return
        visited.add(identity)
        node_count += 1
        if node_count > MAX_WORKFLOW_YAML_NODES:
            raise WorkflowContractError(f"{path} exceeds the YAML node limit")
        if isinstance(node, MappingNode):
            for key, value in node.value:
                if not isinstance(key, ScalarNode):
                    raise WorkflowContractError(f"{path}:{key.start_mark.line + 1} has a non-scalar YAML key")
                if key.value == "uses":
                    positions.append((key.start_mark.line + 1, key.start_mark.column + 1))
                visit(value)
            return
        if isinstance(node, SequenceNode):
            for item in node.value:
                visit(item)
            return
        if not isinstance(node, ScalarNode):
            raise WorkflowContractError(f"{path}:{node.start_mark.line + 1} has an unsupported YAML node")

    visit(document)
    return sorted(positions)


def _parse_workflow_uses(path: Path, text: str) -> list[WorkflowUse]:
    uses: list[WorkflowUse] = []
    canonical_key_positions: list[tuple[int, int]] = []
    for line_index, raw_line in enumerate(text.splitlines(keepends=True), start=1):
        line = raw_line[:-1] if raw_line.endswith("\n") else raw_line
        prefix = USES_PREFIX.match(line)
        if prefix is None:
            continue
        canonical_key_positions.append((line_index, line.index("uses:", prefix.start()) + 1))
        value = line[prefix.end() :].split("#", 1)[0].strip().strip("\"'")
        if value.startswith("./") or value.startswith("../"):
            continue
        if value.startswith("docker://") or "${{" in value or "}}" in value:
            raise WorkflowContractError(f"{path}:{line_index} is not an immutable GitHub Action pin")
        match = REMOTE_USE_RE.fullmatch(line)
        if match is None:
            raise WorkflowContractError(f"{path}:{line_index} must use a SHA pin followed by an exact release tag")
        action_path = match.group("action")
        action_parts = action_path.split("/")
        slug = "/".join(action_parts[:2])
        uses.append(
            WorkflowUse(
                path=path,
                line_index=line_index,
                action_path=action_path,
                slug=slug,
                commit_sha=match.group("sha"),
                version=match.group("version"),
            )
        )
    if canonical_key_positions != _semantic_uses_key_positions(path, text):
        raise WorkflowContractError(
            f"{path} has a semantic uses key that is not an exact canonical unquoted block uses: key"
        )
    return uses


def _workflow_texts(root: Path) -> dict[Path, str]:
    texts: dict[Path, str] = {}
    for path in workflow_paths(root):
        try:
            texts[path.relative_to(root)] = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as error:
            raise WorkflowContractError(f"{path} is not UTF-8") from error
    return texts


def assert_workflow_lock(
    root: Path,
    actions: Mapping[str, ActionRecord],
    *,
    texts: Mapping[Path, str] | None = None,
) -> list[WorkflowUse]:
    """Require every remote action use to match its exact lock identity."""

    current_texts = _workflow_texts(root) if texts is None else dict(texts)
    observed: set[str] = set()
    all_uses: list[WorkflowUse] = []
    for relative, text in sorted(current_texts.items(), key=lambda item: item[0].as_posix()):
        path = root / relative
        for use in _parse_workflow_uses(path, text):
            record = actions.get(use.slug)
            if record is None:
                raise WorkflowContractError(f"{relative}:{use.line_index} action {use.slug} lacks a lock record")
            if use.commit_sha != record.commit_sha:
                raise WorkflowContractError(f"{relative}:{use.line_index} SHA does not match pinned_actions.{use.slug}")
            if use.version != record.version:
                raise WorkflowContractError(f"{relative}:{use.line_index} release comment does not match pinned_actions.{use.slug}")
            observed.add(use.slug)
            all_uses.append(use)
    missing = set(actions).difference(observed)
    if missing:
        raise WorkflowContractError(f"lock action records are unused: {', '.join(sorted(missing))}")
    return all_uses


def _latest_tag(tags: Iterable[str], *, current: str, context: str) -> str:
    parsed = [Version.parse(tag, context=context) for tag in tags]
    if not parsed:
        raise MetadataError(f"{context} has no exact stable tags")
    latest = max(parsed)
    current_version = Version.parse(current, context=context)
    if latest < current_version:
        raise MetadataError(f"{context} latest stable tag would downgrade the checked-in lock")
    return str(latest)


def _release_asset(release: Mapping[str, object], *, slug: str, version: str, policy: ToolPolicy) -> tuple[str, str]:
    assets = release.get("assets")
    if type(assets) is not list:
        raise MetadataError(f"{slug} release assets are invalid")
    asset_name = policy.asset_for(version)
    matches: list[Mapping[str, object]] = []
    for index, asset in enumerate(assets):
        if type(asset) is not dict:
            raise MetadataError(f"{slug} release asset {index} is invalid")
        if _required_string(asset, "name", f"{slug} release asset {index}") == asset_name:
            matches.append(asset)
    if len(matches) != 1:
        raise MetadataError(f"{slug} release lacks exactly one supported Linux asset {asset_name}")
    asset = matches[0]
    url = _required_string(asset, "browser_download_url", f"{slug} release asset")
    expected_url = f"https://github.com/{slug}/releases/download/{version}/{asset_name}"
    if url != expected_url:
        raise MetadataError(f"{slug} release asset URL is not the exact official download URL")
    digest = _required_string(asset, "digest", f"{slug} release asset")
    if not digest.startswith("sha256:") or not SHA256_RE.fullmatch(digest.removeprefix("sha256:")):
        raise MetadataError(f"{slug} release asset lacks an exact SHA-256 digest")
    return asset_name, digest.removeprefix("sha256:")


def resolve_candidate(root: Path, api: OfficialGitHubApi) -> Candidate:
    """Resolve all allowlisted release identities from the fixed official APIs."""

    lock = read_lock(root)
    assert_workflow_lock(root, lock.actions)
    action_resolutions: list[ActionResolution] = []
    for name in sorted(lock.actions):
        if ACTION_RESOLUTION_SOURCES.get(name) != "immutable_git_tags":
            raise MetadataError(f"{name} has no approved immutable action-tag resolution policy")
        current = lock.actions[name]
        current_commit = api.tag_commit(name, current.version)
        if current_commit != current.commit_sha:
            raise MetadataError(f"{name} current tag no longer resolves to the locked immutable SHA")
        target_version = _latest_tag(api.stable_tags(name), current=current.version, context=name)
        target_commit = api.tag_commit(name, target_version)
        target = ActionRecord(name=name, version=target_version, commit_sha=target_commit, upstream=current.upstream)
        action_resolutions.append(ActionResolution(current=current, target=target))

    tool_resolutions: list[ToolResolution] = []
    for name in sorted(lock.tools):
        current = lock.tools[name]
        policy = TOOL_POLICIES[name]
        current_commit = api.tag_commit(policy.slug, current.version)
        if current_commit != current.release_commit:
            raise MetadataError(f"{name} current release tag no longer resolves to the locked immutable SHA")
        release = api.latest_release(policy.slug)
        target_version = str(Version.parse(_required_string(release, "tag_name", f"{name} latest release"), context=name))
        if Version.parse(target_version, context=name) < Version.parse(current.version, context=name):
            raise MetadataError(f"{name} latest release would downgrade the checked-in lock")
        asset, digest = _release_asset(release, slug=policy.slug, version=target_version, policy=policy)
        target = ToolRecord(
            name=name,
            version=target_version,
            release_commit=api.tag_commit(policy.slug, target_version),
            asset=asset,
            url=f"https://github.com/{policy.slug}/releases/download/{target_version}/{asset}",
            sha256=digest,
            executable=current.executable,
            upstream=current.upstream,
        )
        tool_resolutions.append(ToolResolution(current=current, target=target))
    return Candidate(
        resolved_at=datetime.now(timezone.utc).date().isoformat(),
        actions=tuple(action_resolutions),
        tools=tuple(tool_resolutions),
    )


def _candidate_mapping(value: object, *, context: str) -> Mapping[str, object]:
    if type(value) is not dict:
        raise CandidateError(f"{context} is not an object")
    return value


def _candidate_action(value: object, *, context: str) -> ActionRecord:
    record = _candidate_mapping(value, context=context)
    allowed = {"name", "version", "commit_sha", "upstream"}
    if set(record) != allowed:
        raise CandidateError(f"{context} has an unexpected action schema")
    try:
        return _action_record(
            _required_candidate_string(record, "name", context),
            {
                "version": _required_candidate_string(record, "version", context),
                "commit_sha": _required_candidate_string(record, "commit_sha", context),
                "upstream": _required_candidate_string(record, "upstream", context),
            },
        )
    except LockError as error:
        raise CandidateError(str(error)) from error


def _candidate_tool(value: object, *, context: str) -> ToolRecord:
    record = _candidate_mapping(value, context=context)
    allowed = {"name", "version", "release_commit", "asset", "url", "sha256", "executable", "upstream"}
    if set(record) != allowed:
        raise CandidateError(f"{context} has an unexpected tool schema")
    try:
        return _tool_record(
            _required_candidate_string(record, "name", context),
            {key: _required_candidate_string(record, key, context) for key in allowed.difference({"name"})},
        )
    except LockError as error:
        raise CandidateError(str(error)) from error


def _required_candidate_string(mapping: Mapping[str, object], key: str, context: str) -> str:
    value = mapping.get(key)
    if type(value) is not str or not value:
        raise CandidateError(f"{context}.{key} is missing or invalid")
    return value


def candidate_from_dict(value: object) -> Candidate:
    """Parse the artifact format strictly before comparing it to fresh metadata."""

    mapping = _candidate_mapping(value, context="candidate")
    allowed = {"schema_version", "source", "resolved_at", "update_available", "actions", "tools"}
    if set(mapping) != allowed or mapping.get("schema_version") != 1:
        raise CandidateError("candidate has an unexpected schema")
    if mapping.get("source") != CANONICAL_GITHUB_API_URL:
        raise CandidateError("candidate does not name the fixed GitHub API source")
    resolved_at = _required_candidate_string(mapping, "resolved_at", "candidate")
    if not DATE_RE.fullmatch(resolved_at):
        raise CandidateError("candidate resolved_at is not an ISO date")
    update_available = mapping.get("update_available")
    if type(update_available) is not bool:
        raise CandidateError("candidate update_available is not boolean")
    actions_value = mapping.get("actions")
    tools_value = mapping.get("tools")
    if type(actions_value) is not list or type(tools_value) is not list:
        raise CandidateError("candidate actions or tools is not a list")
    actions: list[ActionResolution] = []
    for index, item in enumerate(actions_value):
        pair = _candidate_mapping(item, context=f"candidate.actions[{index}]")
        if set(pair) != {"current", "target"}:
            raise CandidateError(f"candidate.actions[{index}] has an unexpected schema")
        actions.append(
            ActionResolution(
                current=_candidate_action(pair["current"], context=f"candidate.actions[{index}].current"),
                target=_candidate_action(pair["target"], context=f"candidate.actions[{index}].target"),
            )
        )
    tools: list[ToolResolution] = []
    for index, item in enumerate(tools_value):
        pair = _candidate_mapping(item, context=f"candidate.tools[{index}]")
        if set(pair) != {"current", "target"}:
            raise CandidateError(f"candidate.tools[{index}] has an unexpected schema")
        tools.append(
            ToolResolution(
                current=_candidate_tool(pair["current"], context=f"candidate.tools[{index}].current"),
                target=_candidate_tool(pair["target"], context=f"candidate.tools[{index}].target"),
            )
        )
    if [item.current.name for item in actions] != sorted(SUPPORTED_ACTIONS):
        raise CandidateError("candidate actions do not exactly match the Parent allowlist")
    if [item.current.name for item in tools] != sorted(SUPPORTED_TOOLS):
        raise CandidateError("candidate tools do not exactly match the Parent allowlist")
    candidate = Candidate(resolved_at=resolved_at, actions=tuple(actions), tools=tuple(tools))
    if candidate.update_available != update_available:
        raise CandidateError("candidate update_available is inconsistent with target identities")
    return candidate


def load_candidate(path: Path) -> Candidate:
    """Read one bounded candidate artifact; it is not trusted until re-resolved."""

    try:
        metadata = path.lstat()
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
            raise CandidateError("candidate is not a regular file")
        raw = path.read_bytes()
    except OSError as error:
        raise CandidateError("candidate cannot be read") from error
    if len(raw) > MAX_CANDIDATE_BYTES:
        raise CandidateError("candidate exceeds its size limit")
    try:
        data = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_json_constant,
        )
    except MetadataError as error:
        raise CandidateError(str(error)) from error
    except (UnicodeDecodeError, RecursionError, ValueError) as error:
        raise CandidateError("candidate is not valid JSON") from error
    return candidate_from_dict(data)


def _semantic_candidate(candidate: Candidate) -> tuple[tuple[ActionResolution, ...], tuple[ToolResolution, ...]]:
    return candidate.actions, candidate.tools


def _assert_candidate_current(candidate: Candidate, state: LockState) -> None:
    for resolution in candidate.actions:
        if state.actions.get(resolution.current.name) != resolution.current:
            raise CandidateError(f"candidate action {resolution.current.name} does not start from this lock")
        if resolution.target.name != resolution.current.name or resolution.target.upstream != resolution.current.upstream:
            raise CandidateError(f"candidate action {resolution.current.name} changes its identity outside the allowlist")
        if Version.parse(resolution.target.version, context=resolution.target.name) < Version.parse(
            resolution.current.version, context=resolution.current.name
        ):
            raise CandidateError(f"candidate action {resolution.current.name} downgrades the release")
    for resolution in candidate.tools:
        if state.tools.get(resolution.current.name) != resolution.current:
            raise CandidateError(f"candidate tool {resolution.current.name} does not start from this lock")
        if (
            resolution.target.name != resolution.current.name
            or resolution.target.upstream != resolution.current.upstream
            or resolution.target.executable != resolution.current.executable
        ):
            raise CandidateError(f"candidate tool {resolution.current.name} changes its fixed identity")
        if Version.parse(resolution.target.version, context=resolution.target.name) < Version.parse(
            resolution.current.version, context=resolution.current.name
        ):
            raise CandidateError(f"candidate tool {resolution.current.name} downgrades the release")


def _replace_lock_fields(text: str, section: str, name: str, fields: Mapping[str, str]) -> str:
    """Replace only required scalar fields inside one uniquely parsed lock record."""

    start = re.search(rf"(?m)^{re.escape(section)}:$", text)
    if start is None:
        raise LockError(f"lock lacks {section}")
    section_end = re.search(r"(?m)^[A-Za-z][A-Za-z0-9_-]*:\s*$", text[start.end() :])
    end = start.end() + section_end.start() if section_end is not None else len(text)
    body = text[start.end() : end]
    record = re.search(
        rf"(?ms)^  {re.escape(name)}:\n(?P<body>(?:^    [^\n]*(?:\n|$))*)",
        body,
    )
    if record is None:
        raise LockError(f"lock lacks {section}.{name}")
    record_text = record.group(0)
    for key, value in fields.items():
        field_pattern = re.compile(rf"(?m)^    {re.escape(key)}: .+$")
        if len(field_pattern.findall(record_text)) != 1:
            raise LockError(f"lock lacks unique {section}.{name}.{key}")
        record_text = field_pattern.sub(f"    {key}: {value}", record_text)
    updated_body = body[: record.start()] + record_text + body[record.end() :]
    return text[: start.end()] + updated_body + text[end:]


def _replace_checked_at(text: str, checked_at: str) -> str:
    if not DATE_RE.fullmatch(checked_at):
        raise CandidateError("candidate date is invalid")
    pattern = re.compile(r'(?m)^checked_at: "[^\"]+"$')
    if len(pattern.findall(text)) != 1:
        raise LockError("lock lacks one checked_at field")
    return pattern.sub(f'checked_at: "{checked_at}"', text)


def _render_lock(state: LockState, candidate: Candidate) -> str:
    rendered = state.text
    changed = False
    for resolution in candidate.actions:
        if not resolution.changes:
            continue
        rendered = _replace_lock_fields(
            rendered,
            "pinned_actions",
            resolution.current.name,
            {"version": resolution.target.version, "commit_sha": resolution.target.commit_sha},
        )
        changed = True
    for resolution in candidate.tools:
        if not resolution.changes:
            continue
        rendered = _replace_lock_fields(
            rendered,
            "tools",
            resolution.current.name,
            {
                "version": resolution.target.version,
                "release_commit": resolution.target.release_commit,
                "asset": resolution.target.asset,
                "url": resolution.target.url,
                "sha256": resolution.target.sha256,
            },
        )
        changed = True
    return _replace_checked_at(rendered, candidate.resolved_at) if changed else rendered


def _render_workflow(text: str, uses: Iterable[WorkflowUse], targets: Mapping[str, ActionRecord]) -> str:
    lines = text.splitlines(keepends=True)
    for use in uses:
        target = targets.get(use.slug)
        if target is None or target == ActionRecord(use.slug, use.version, use.commit_sha, _exact_upstream(use.slug)):
            continue
        raw = lines[use.line_index - 1]
        newline = "\n" if raw.endswith("\n") else ""
        line = raw[:-1] if newline else raw
        match = REMOTE_USE_RE.fullmatch(line)
        if match is None:
            raise WorkflowContractError(f"{use.path}:{use.line_index} changed while rendering")
        lines[use.line_index - 1] = f"{match.group('prefix')}{use.action_path}@{target.commit_sha} # {target.version}{newline}"
    return "".join(lines)


def _allowed_changed_path(path: Path) -> bool:
    if path == LOCK_RELATIVE_PATH:
        return True
    return path.parent == WORKFLOWS_RELATIVE_DIRECTORY and path.suffix in {".yml", ".yaml"}


def build_update_plan(root: Path, candidate: Candidate) -> dict[Path, str]:
    """Build a fully validated in-memory change set with a strict Parent allowlist."""

    state = read_lock(root)
    _assert_candidate_current(candidate, state)
    texts = _workflow_texts(root)
    uses = assert_workflow_lock(root, state.actions, texts=texts)
    targets = {item.current.name: item.target for item in candidate.actions if item.changes}
    planned: dict[Path, str] = {}
    rendered_lock = _render_lock(state, candidate)
    if rendered_lock != state.text:
        planned[LOCK_RELATIVE_PATH] = rendered_lock
    uses_by_path: dict[Path, list[WorkflowUse]] = {}
    for use in uses:
        uses_by_path.setdefault(use.path.relative_to(root), []).append(use)
    for relative, text in texts.items():
        rendered = _render_workflow(text, uses_by_path.get(relative, ()), targets)
        if rendered != text:
            planned[relative] = rendered
    if any(not _allowed_changed_path(relative) for relative in planned):
        raise UpdaterError("planned update escapes the Parent CI-tool allowlist")
    if planned:
        rendered_state = parse_lock_text(planned.get(LOCK_RELATIVE_PATH, state.text))
        rendered_texts = dict(texts)
        rendered_texts.update({path: text for path, text in planned.items() if path != LOCK_RELATIVE_PATH})
        assert_workflow_lock(root, rendered_state.actions, texts=rendered_texts)
    return dict(sorted(planned.items(), key=lambda item: item[0].as_posix()))


def validate_candidate(root: Path, candidate: Candidate, api: OfficialGitHubApi) -> dict[Path, str]:
    """Re-resolve official provenance and validate the exact in-memory update plan."""

    fresh = resolve_candidate(root, api)
    if candidate.resolved_at != fresh.resolved_at:
        raise CandidateError("candidate date differs from freshly resolved official provenance")
    if _semantic_candidate(candidate) != _semantic_candidate(fresh):
        raise CandidateError("candidate differs from freshly resolved official release provenance")
    return build_update_plan(root, candidate)


def _atomic_write(path: Path, text: str) -> None:
    metadata = path.lstat()
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise UpdaterError(f"refusing to replace non-regular file {path}")
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, stat.S_IMODE(metadata.st_mode))
        os.replace(temporary, path)
    except OSError as error:
        raise UpdaterError(f"cannot atomically update {path}") from error
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def apply_plan(root: Path, plan: Mapping[Path, str]) -> list[str]:
    """Apply a prevalidated plan only to regular Parent CI-tool targets."""

    changed: list[str] = []
    for relative, text in plan.items():
        if not _allowed_changed_path(relative):
            raise UpdaterError("apply request escapes the Parent CI-tool allowlist")
        path = _safe_repository_file(root, relative)
        _atomic_write(path, text)
        changed.append(relative.as_posix())
    return changed


def verify_local_contract(root: Path) -> dict[str, object]:
    """Validate lock/workflow congruence without network or writes."""

    state = read_lock(root)
    uses = assert_workflow_lock(root, state.actions)
    return {
        "status": "valid",
        "actions": len(state.actions),
        "tools": len(state.tools),
        "workflow_uses": len(uses),
    }


def _print_json(value: Mapping[str, object]) -> None:
    print(json.dumps(value, sort_keys=True, separators=(",", ":")))


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--resolve", action="store_true", help="resolve official candidate provenance without writing")
    mode.add_argument("--validate", action="store_true", help="re-resolve and validate a candidate artifact without writing")
    mode.add_argument("--apply", action="store_true", help="re-resolve, validate, and apply a candidate artifact")
    mode.add_argument("--check", action="store_true", help="resolve and exit 1 when an update is available")
    mode.add_argument("--verify", action="store_true", help="verify local lock/workflow congruence without network")
    parser.add_argument("--candidate", type=Path, help="candidate JSON required by --validate or --apply")
    parser.add_argument("--json", action="store_true", help="emit machine-readable result")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    if bool(args.candidate) != bool(args.validate or args.apply):
        raise SystemExit("--candidate is required only with --validate or --apply")
    root = Path.cwd().resolve()
    try:
        if args.verify:
            result = verify_local_contract(root)
            if args.json:
                _print_json(result)
            else:
                print("Parent CI tool lock and workflow pins are congruent.")
            return 0

        api = OfficialGitHubApi()
        if args.resolve or args.check:
            candidate = resolve_candidate(root, api)
            plan = build_update_plan(root, candidate)
        else:
            assert args.candidate is not None
            candidate = load_candidate(args.candidate)
            plan = validate_candidate(root, candidate, api)

        result: dict[str, object] = candidate.to_dict()
        result["changed_paths"] = [path.as_posix() for path in plan]
        if args.apply:
            result["applied_paths"] = apply_plan(root, plan)
            result["status"] = "applied" if plan else "current"
        else:
            result["status"] = "update_available" if candidate.update_available else "current"
        if args.json:
            _print_json(result)
        else:
            print(f"CI tool updater status: {result['status']}")
            for path in result["changed_paths"]:
                print(path)
        return 1 if args.check and candidate.update_available else 0
    except UpdaterError as error:
        print(f"CI tool updater failed safely: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
