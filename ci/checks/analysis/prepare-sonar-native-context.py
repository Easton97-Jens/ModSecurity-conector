#!/usr/bin/env python3
"""Prepare real, pinned host headers for full-scope CFamily AutoConfig.

This produces configure-time context, not a complete compilation database or a
claim that independent executable targets and their variants share an ABI.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tarfile
import urllib.request
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "ci/lib"))
from runtime_path_utils import is_safe_runtime_root


def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def contracts() -> dict[str, dict[str, str]]:
    """Read existing Parent pins as data, without executing contract content."""
    module = ast.parse((ROOT / "ci/provisioning/components/prepare-runtime-components.py").read_text())
    values = {
        target.id: ast.literal_eval(node.value)
        for node in module.body if isinstance(node, ast.Assign)
        for target in node.targets if isinstance(target, ast.Name)
        and target.id.startswith("NGINX_PINNED_")
    }
    haproxy = json.loads((ROOT / "connectors/haproxy/htx-overlay/version-contract.json").read_text())
    lighttpd = dict(
        line.split("=", 1) for line in
        (ROOT / "connectors/lighttpd/lighttpd-version.contract").read_text().splitlines()
        if line and not line.startswith("#")
    )
    nginx_version = values["NGINX_PINNED_VERSION_READBACK"].split("/", 1)[1]
    result = {
        "nginx": {"version": nginx_version, "directory": f"nginx-{nginx_version}",
                  "url": values["NGINX_PINNED_SOURCE_REPOSITORY"] + "/releases/download/"
                  + values["NGINX_PINNED_RELEASE_TAG"] + "/" + values["NGINX_PINNED_RELEASE_ASSET_NAME"],
                  "sha256": values["NGINX_PINNED_RELEASE_ASSET_SHA256"]},
        "haproxy": {"version": haproxy["version"], "directory": "haproxy-" + haproxy["version"],
                    "url": haproxy["source_url"], "sha256": haproxy["sha256"]},
        "lighttpd": {"version": lighttpd["LIGHTTPD_VERSION"],
                     "directory": "lighttpd-" + lighttpd["LIGHTTPD_VERSION"],
                     "url": lighttpd["LIGHTTPD_DOWNLOAD_URL"], "sha256": lighttpd["LIGHTTPD_SHA256"],
                     "patch": lighttpd["LIGHTTPD_PATCH_FILENAME"]},
    }
    for item in result.values():
        parsed = urlsplit(item["url"])
        if (parsed.scheme != "https" or not parsed.hostname or parsed.username is not None
                or parsed.password is not None or parsed.query or parsed.fragment):
            raise ValueError("native source contracts require credential-free pinned HTTPS URLs")
        if not re.fullmatch(r"[a-f0-9]{64}", item["sha256"]):
            raise ValueError("native source contract requires an exact SHA-256")
        if not re.fullmatch(r"[a-z]+-[0-9]+(?:\.[0-9]+)+", item["directory"]):
            raise ValueError("native source contract directory is invalid")
    if Path(result["lighttpd"]["patch"]).name != result["lighttpd"]["patch"]:
        raise ValueError("lighttpd patch must be a versioned leaf filename")
    return result


def fresh_root(value: str) -> Path:
    path = Path(value)
    if (not path.is_absolute() or ".." in path.parts or any(c in value for c in "\r\n,\0")
            or not is_safe_runtime_root(path) or path.is_relative_to(ROOT)
            or ROOT.is_relative_to(path)):
        raise ValueError("native context root must be a safe absolute external path")
    if path.exists() or path.is_symlink():
        raise ValueError("native context root must be fresh")
    path.mkdir(parents=True, mode=0o700)
    return path


def verified_archive(item: dict[str, str], downloads: Path, archives_root: Path | None) -> Path:
    name = Path(urlsplit(item["url"]).path).name
    cached = archives_root / name if archives_root is not None else None
    if cached is not None and (cached.exists() or cached.is_symlink()):
        if cached.is_symlink() or not cached.is_file():
            raise ValueError("cached native archive must be a regular file")
        archive = cached
    else:
        archive = downloads / name
        request = urllib.request.Request(item["url"], headers={"User-Agent": "Parent-Sonar-native-context"})
        with urllib.request.urlopen(request, timeout=60) as response, archive.open("xb") as output:
            if urlsplit(response.geturl()).scheme != "https":
                raise ValueError("native source download redirected away from HTTPS")
            shutil.copyfileobj(response, output)
    if sha256(archive) != item["sha256"]:
        raise ValueError(f"native archive SHA-256 mismatch: {name}")
    return archive


def unpack(archive: Path, sources: Path, expected: str) -> Path:
    destination = sources / expected
    if destination.exists() or destination.is_symlink():
        raise ValueError("native extraction destination must be fresh")
    with tarfile.open(archive, "r:*") as bundle:
        members = bundle.getmembers()
        if not members or any(not Path(m.name).parts or Path(m.name).is_absolute()
                              or ".." in Path(m.name).parts
                              or Path(m.name).parts[0] != expected for m in members):
            raise ValueError("native archive has an unexpected top-level directory")
        bundle.extractall(sources, members=members, filter="data")
    if not destination.is_dir() or destination.is_symlink():
        raise ValueError("native archive did not produce the expected source directory")
    return destination


def run(command: list[str], cwd: Path, log: Path, *,
        environment: dict[str, str] | None = None) -> dict[str, object]:
    selected_environment = environment or {}
    with log.open("x", encoding="utf-8") as output:
        subprocess.run(command, cwd=cwd, stdout=output, stderr=subprocess.STDOUT, check=True,
                       env=dict(os.environ, TMPDIR=str(log.parent), **selected_environment))
    return {"arguments": command, "directory": str(cwd), "log": str(log),
            "environment": selected_environment}


def required_files(paths: list[Path]) -> dict[str, str]:
    for path in paths:
        if not path.is_file() or path.is_symlink() or path.stat().st_size == 0:
            raise ValueError(f"required native context file is missing or invalid: {path}")
    return {str(path): sha256(path) for path in paths}


def nginx_includes(source: Path) -> list[Path]:
    """Use the real configure-generated include search list, not guessed flags."""
    makefile = (source / "objs/Makefile").read_text().replace("\\\n", " ")
    match = re.search(r"^ALL_INCS\s*=\s*(.*)$", makefile, re.MULTILINE)
    if match is None:
        raise ValueError("NGINX configure did not publish ALL_INCS")
    arguments = shlex.split(match.group(1))
    result = []
    for index, argument in enumerate(arguments):
        if argument == "-I":
            directory = (source / arguments[index + 1]).resolve()
        elif argument.startswith("-I"):
            directory = (source / argument[2:]).resolve()
        else:
            continue
        if directory.is_relative_to(source) and directory not in result:
            result.append(directory)
    if not result:
        raise ValueError("NGINX configure did not publish host include directories")
    return result


def include_value(paths: list[Path]) -> str:
    if not paths or any(not p.is_dir() or any(c in str(p) for c in "\r\n,\0") for p in paths):
        raise ValueError("native include directories must exist and have unambiguous paths")
    return ",".join(str(path) for path in paths)


def checkout_state() -> tuple[str, str]:
    def git(*arguments: str) -> str:
        return subprocess.check_output(["git", "-C", str(ROOT), *arguments], text=True).strip()
    return git("rev-parse", "HEAD"), git("status", "--porcelain", "--untracked-files=all")


def prepare(output: Path, pins: dict[str, dict[str, str]], archives_root: Path | None) -> dict[str, object]:
    revision, initial_status = checkout_state()
    sources, downloads, logs = (output / name for name in ("sources", "downloads", "logs"))
    for path in (sources, downloads, logs):
        path.mkdir()
    hosts = {}
    for name, item in pins.items():
        archive = verified_archive(item, downloads, archives_root)
        source = unpack(archive, sources, item["directory"])
        hosts[name] = {"version": item["version"], "archive_url": item["url"],
                       "archive_sha256": item["sha256"], "source": str(source)}
    nginx = Path(hosts["nginx"]["source"])
    hosts["nginx"]["configure"] = run(
        ["sh", "./configure", "--with-compat", "--add-dynamic-module=" + str(ROOT / "connectors/nginx")],
        nginx, logs / "nginx-configure.log")
    generated = required_files([nginx / "objs/ngx_auto_config.h", nginx / "objs/ngx_auto_headers.h",
                                nginx / "objs/Makefile"])
    stock = Path(hosts["lighttpd"]["source"])
    patched = sources / ("lighttpd-patched-" + pins["lighttpd"]["version"])
    patch = ROOT / "connectors/lighttpd/patches" / pins["lighttpd"]["patch"]
    hosts["lighttpd"]["patch_sha256"] = sha256(patch)
    hosts["lighttpd"]["patch_command"] = run(
        ["sh", str(ROOT / "connectors/lighttpd/build/apply_core_patch.sh"), "--apply"],
        ROOT, logs / "lighttpd-patch.log", environment={
            "BUILD_ROOT": str(output), "LIGHTTPD_SOURCE_DIR": str(stock),
            "LIGHTTPD_PATCHED_SOURCE_DIR": str(patched)})
    stamp = patched / ".msconnector-lighttpd-patch.sha256"
    generated.update(required_files([stamp]))
    if stamp.read_text().strip() != hosts["lighttpd"]["patch_sha256"]:
        raise ValueError("patched lighttpd source stamp disagrees with the current patch")
    hosts["lighttpd"]["patch_stamp"] = str(stamp)
    plugin = (patched / "src/plugin.h").read_text()
    if not re.search(r"^#define\s+LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION\s+2\s*$", plugin, re.MULTILINE):
        raise ValueError("patched lighttpd header does not declare stream hook ABI 2")
    build, stage = output / "lighttpd-build", output / "lighttpd-stage"
    build.mkdir()
    configure = patched / "configure"
    if not configure.is_file():
        autogen = patched / "autogen.sh"
        hosts["lighttpd"]["autogen_sha256"] = required_files([autogen])[str(autogen)]
        # The unchanged upstream script installs an ERR trap despite its sh
        # shebang. Bash supports that trap and runs its actual autoreconf flow.
        hosts["lighttpd"]["bootstrap"] = run(
            ["bash", str(autogen)], patched, logs / "lighttpd-autogen.log")
    generated.update(required_files([configure]))
    hosts["lighttpd"]["configure"] = run(
        [str(configure), "--prefix=" + str(stage), "--bindir=" + str(stage / "bin"),
         "--sbindir=" + str(stage / "bin"), "--libdir=" + str(stage / "lib")],
        build, logs / "lighttpd-configure.log")
    generated.update(required_files([build / "config.h", patched / "src/plugin.h"]))
    haproxy = Path(hosts["haproxy"]["source"])
    required_files([haproxy / "include/haproxy/api.h", haproxy / "VERSION", patched / "src/base.h"])
    if (haproxy / "VERSION").read_text().strip() != pins["haproxy"]["version"]:
        raise ValueError("HAProxy source VERSION disagrees with the contract")
    includes = nginx_includes(nginx) + [haproxy / "include", build, patched / "src"]
    if checkout_state() != (revision, initial_status):
        raise ValueError("checkout changed while native context was being prepared")
    manifest = {"revision": revision, "uncommitted_changes": bool(initial_status),
                "hosts": hosts, "generated_files": generated,
                "includes": [str(path) for path in includes], "include_value": include_value(includes),
                "limitations": ["Header/configure context only; no complete compilation database.",
                                "HAProxy make-derived feature defines are not globally injected.",
                                "lighttpd headers select patched-native; stock and patched ABIs are not interchangeable.",
                                "Per-file HAVE_CONFIG_H/MSCONNECTOR_LIGHTTPD_HOST_API and other variants are not proven by include directories.",
                                "AutoConfig C/C++ taint and independent executable-target assumptions remain unchanged."]}
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--archives-root", type=Path)
    args = parser.parse_args()
    try:
        pins = contracts()
        manifest = prepare(fresh_root(args.output_root), pins, args.archives_root)
    except (ValueError, OSError, subprocess.CalledProcessError, tarfile.TarError) as error:
        print(f"Sonar native context failed: {error}", file=sys.stderr)
        return 1
    print(manifest["include_value"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
