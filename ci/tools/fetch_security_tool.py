#!/usr/bin/env python3
"""Download one locked Parent CI security-tool asset without trust expansion."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import stat
import tarfile
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LOCK = ROOT / "ci" / "tooling" / "security-tools.lock.yml"
SHA256 = re.compile(r"^[a-f\d]{64}$", re.ASCII)
SHA1 = re.compile(r"^[a-f\d]{40}$", re.ASCII)
VERSION = re.compile(r"^v(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)$", re.ASCII)
ASSET = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$", re.ASCII)
EXECUTABLE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$", re.ASCII)
MAX_DOWNLOAD_BYTES = 512 * 1024 * 1024
NETWORK_TIMEOUT_SECONDS = 60
MAX_REDIRECTS = 2
# GitHub release downloads currently redirect from github.com to the first
# host below.  The second host is GitHub's legacy release-asset endpoint.  Do
# not widen this to a githubusercontent.com wildcard: the locked origin URL,
# the small explicit host set, and the final SHA-256 are separate controls.
RELEASE_ASSET_HOSTS = frozenset(
    {
        "release-assets.githubusercontent.com",
        "github-releases.githubusercontent.com",
    }
)
TOOL_ASSETS = {
    "actionlint": ("rhysd/actionlint", "actionlint", "actionlint_{version}_linux_amd64.tar.gz"),
    "zizmor": ("zizmorcore/zizmor", "zizmor", "zizmor-x86_64-unknown-linux-gnu.tar.gz"),
    "gitleaks": ("gitleaks/gitleaks", "gitleaks", "gitleaks_{version}_linux_x64.tar.gz"),
}


def _parse_https_url(url: object, *, context: str) -> urllib.parse.SplitResult:
    """Parse a complete direct HTTPS URL and reject ambiguous authorities."""

    if type(url) is not str:
        raise ValueError(f"{context} is not a URL")
    try:
        parsed = urllib.parse.urlsplit(url)
    except ValueError as error:
        raise ValueError(f"{context} is invalid") from error
    if (
        parsed.scheme != "https"
        or parsed.hostname is None
        or parsed.port is not None
        or parsed.username is not None
        or parsed.password is not None
        or not parsed.path.startswith("/")
        or "/../" in parsed.path
        or parsed.fragment
    ):
        raise ValueError(f"{context} is not a direct HTTPS URL")
    return parsed


def _initial_release_url(url: str) -> urllib.parse.SplitResult:
    parsed = _parse_https_url(url, context="security-tool release URL")
    if parsed.hostname != "github.com" or parsed.query:
        raise ValueError("security-tool release URL is not the exact GitHub release origin")
    return parsed


def _release_asset_url(url: object, *, context: str) -> urllib.parse.SplitResult:
    parsed = _parse_https_url(url, context=context)
    if parsed.hostname not in RELEASE_ASSET_HOSTS:
        raise ValueError(f"{context} is not an allowed GitHub release-asset host")
    return parsed


class TrustedReleaseRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Follow only a bounded GitHub-release redirect chain over HTTPS."""

    def __init__(self, initial_url: str) -> None:
        super().__init__()
        _initial_release_url(initial_url)
        self._initial_url = initial_url
        self._redirects = 0

    def redirect_request(self, request, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        if code not in {301, 302, 303, 307, 308}:
            raise ValueError("security-tool release returned an unsupported redirect status")
        if self._redirects >= MAX_REDIRECTS:
            raise ValueError("security-tool release exceeded the redirect limit")
        current_url = request.full_url
        if current_url == self._initial_url:
            _initial_release_url(current_url)
            _release_asset_url(newurl, context="security-tool release redirect")
        else:
            _release_asset_url(current_url, context="security-tool release redirect source")
            _release_asset_url(newurl, context="security-tool release redirect")
        self._redirects += 1
        return super().redirect_request(request, fp, code, msg, headers, newurl)


def _record_fields(tool: str) -> dict[str, str]:
    """Read one small lock record without interpreting arbitrary YAML features."""

    if tool not in TOOL_ASSETS:
        raise ValueError(f"unknown security tool: {tool}")
    try:
        text = LOCK.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise ValueError("security-tool lock cannot be read as UTF-8") from error
    match = re.search(
        rf"^ {{2}}{re.escape(tool)}:\n(?P<body>.*?)(?=^ {{2}}[a-z][a-z\d_]*:|^dispositions:|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if match is None:
        raise ValueError(f"unknown security tool: {tool}")
    values: dict[str, str] = {}
    for field in re.finditer(r"^ {4}(?P<key>[a-z\d_]+): (?P<value>.+)$", match.group("body"), re.MULTILINE):
        key = field.group("key")
        if key in values:
            raise ValueError(f"{tool}: duplicate {key} lock field")
        values[key] = field.group("value").strip()
    return values


def record(tool: str) -> dict[str, str]:
    """Validate the immutable provenance contract for one supported tool."""

    values = _record_fields(tool)
    required = {"version", "release_commit", "asset", "url", "sha256", "executable", "upstream"}
    missing = required.difference(values)
    if missing:
        raise ValueError(f"{tool}: incomplete lock record ({', '.join(sorted(missing))})")
    version = values["version"]
    if not VERSION.fullmatch(version):
        raise ValueError(f"{tool}: malformed stable release tag")
    if not SHA1.fullmatch(values["release_commit"]):
        raise ValueError(f"{tool}: malformed release commit SHA")
    if not SHA256.fullmatch(values["sha256"]):
        raise ValueError(f"{tool}: malformed SHA-256")
    slug, executable, asset_template = TOOL_ASSETS[tool]
    upstream = f"https://github.com/{slug}"
    if values["upstream"] != upstream:
        raise ValueError(f"{tool}: upstream is not the fixed official GitHub repository")
    if values["executable"] != executable or not EXECUTABLE.fullmatch(values["executable"]):
        raise ValueError(f"{tool}: executable violates the fixed tool policy")
    asset = values["asset"]
    expected_asset = asset_template.format(version=version.removeprefix("v"))
    if not ASSET.fullmatch(asset) or asset != expected_asset:
        raise ValueError(f"{tool}: asset violates the fixed platform contract")
    expected_url = f"{upstream}/releases/download/{version}/{asset}"
    if values["url"] != expected_url:
        raise ValueError(f"{tool}: release asset URL is not the exact recorded upstream release")
    return values


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_member(member: tarfile.TarInfo) -> bool:
    """Read only one ordinary archive file; never trust archive links or paths."""

    path = Path(member.name)
    return member.isfile() and not path.is_absolute() and ".." not in path.parts


def _response_content_length(response: object) -> int | None:
    headers = getattr(response, "headers", None)
    value = headers.get("Content-Length") if headers is not None and hasattr(headers, "get") else None
    if value is None:
        return None
    text = str(value).strip()
    if not text.isdecimal() or int(text) > MAX_DOWNLOAD_BYTES:
        raise ValueError("security-tool release has an invalid Content-Length")
    return int(text)


def _download(url: str, archive: Path) -> None:
    _initial_release_url(url)
    request = urllib.request.Request(
        url,
        headers={"Accept-Encoding": "identity", "User-Agent": "modsecurity-conector-security-tools"},
        method="GET",
    )
    opener = urllib.request.build_opener(TrustedReleaseRedirectHandler(url))
    response = None
    try:
        response = opener.open(request, timeout=NETWORK_TIMEOUT_SECONDS)
        status = getattr(response, "status", None)
        if status is None and hasattr(response, "getcode"):
            status = response.getcode()
        if status is not None and status != 200:
            raise ValueError("security-tool release download did not return HTTP 200")
        actual_url = response.geturl() if hasattr(response, "geturl") else None
        if actual_url == url:
            _initial_release_url(actual_url)
        else:
            _release_asset_url(actual_url, context="security-tool release final URL")
        expected_length = _response_content_length(response)
        total = 0
        with archive.open("xb") as output:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                if type(chunk) is not bytes:
                    raise ValueError("security-tool release returned non-binary data")
                total += len(chunk)
                if total > MAX_DOWNLOAD_BYTES:
                    raise ValueError("security-tool release exceeds the size limit")
                output.write(chunk)
        if expected_length is not None and total != expected_length:
            raise ValueError("security-tool release download was truncated")
    except urllib.error.HTTPError as error:
        raise ValueError(f"security-tool release returned HTTP {error.code}") from error
    except OSError as error:
        raise ValueError("security-tool release download failed") from error
    finally:
        if response is not None and hasattr(response, "close"):
            response.close()


def _safe_destination(destination: Path) -> Path:
    destination.mkdir(parents=True, exist_ok=True)
    metadata = destination.lstat()
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise ValueError("security-tool destination is not a real directory")
    return destination


def fetch(tool: str, destination: Path) -> Path:
    """Download, checksum, and atomically publish exactly one expected binary."""

    values = record(tool)
    destination = _safe_destination(destination)
    target = destination / values["executable"]
    if target.exists() and target.is_symlink():
        raise ValueError(f"{tool}: destination executable is a symbolic link")
    with tempfile.TemporaryDirectory(prefix="security-tool-", dir=destination) as temporary_directory:
        temporary = Path(temporary_directory)
        archive = temporary / values["asset"]
        _download(values["url"], archive)
        if sha256(archive) != values["sha256"]:
            raise ValueError(f"{tool}: SHA-256 mismatch")
        try:
            with tarfile.open(archive, "r:gz") as bundle:
                entries = [
                    member
                    for member in bundle.getmembers()
                    if safe_member(member) and Path(member.name).name == values["executable"]
                ]
                if len(entries) != 1:
                    raise ValueError(f"{tool}: expected exactly one executable")
                source = bundle.extractfile(entries[0])
                if source is None:
                    raise ValueError(f"{tool}: unreadable executable")
                with source:
                    descriptor, staged_name = tempfile.mkstemp(prefix=f".{values['executable']}.", dir=destination)
                    staged = Path(staged_name)
                    try:
                        with os.fdopen(descriptor, "wb") as output:
                            shutil.copyfileobj(source, output)
                            output.flush()
                            os.fsync(output.fileno())
                        os.chmod(staged, 0o755)
                        os.replace(staged, target)
                    finally:
                        try:
                            staged.unlink()
                        except FileNotFoundError:
                            pass
        except (tarfile.TarError, OSError) as error:
            raise ValueError(f"{tool}: release archive is invalid") from error
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", required=True)
    parser.add_argument("--destination", type=Path)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    if args.validate_only:
        record(args.tool)
        return
    if args.destination is None:
        parser.error("--destination is required unless --validate-only is used")
        return
    print(fetch(args.tool, args.destination.resolve()))


if __name__ == "__main__":
    main()
