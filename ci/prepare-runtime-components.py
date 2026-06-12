#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SYSTEM_PREFIXES = (
    "/usr",
    "/usr/local",
    "/opt",
    "/etc",
    "/var",
    "/lib",
    "/lib64",
    "/bin",
    "/sbin",
    "/run",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def is_system_path(path: Path) -> bool:
    text = str(path.resolve(strict=False))
    return any(text == prefix or text.startswith(prefix + "/") for prefix in SYSTEM_PREFIXES)


def sh_quote(value: str) -> str:
    return "'" + value.replace("'", "'\"'\"'") + "'"


def run(cmd: list[str], cwd: Path | None = None, check: bool = False) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and proc.returncode != 0:
        raise RuntimeError((proc.stdout + proc.stderr).strip() or f"command failed: {' '.join(cmd)}")
    return proc


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def tree_manifest(path: Path) -> dict[str, Any]:
    file_count = 0
    total_size = 0
    digest = hashlib.sha256()
    if not path.exists():
        return {"exists": False, "file_count": 0, "total_size": 0, "sha256_manifest": ""}
    for item in sorted(path.rglob("*")):
        if not item.is_file():
            continue
        try:
            rel = item.relative_to(path).as_posix()
            size = item.stat().st_size
        except OSError:
            continue
        file_count += 1
        total_size += size
        digest.update(rel.encode("utf-8", "surrogateescape"))
        digest.update(b"\0")
        digest.update(str(size).encode("ascii"))
        digest.update(b"\0")
    return {
        "exists": True,
        "file_count": file_count,
        "total_size": total_size,
        "sha256_manifest": digest.hexdigest(),
    }


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def git_output(path: Path, *args: str) -> str:
    proc = run(["git", "-C", str(path), *args])
    return proc.stdout.strip()


def submodule_status_clean(status_text: str) -> tuple[bool, str]:
    for line in status_text.splitlines():
        if not line:
            continue
        if line.startswith("-"):
            return False, "submodule_missing"
        if line.startswith("+"):
            return False, "submodule_ref_mismatch"
    return True, ""


def should_skip_fsck(previous: dict[str, Any], record: dict[str, Any], strict: bool) -> bool:
    if strict:
        return False
    return (
        previous.get("url") == record.get("url")
        and previous.get("expected_ref") == record.get("expected_ref")
        and previous.get("actual_head") == record.get("actual_head")
        and previous.get("submodule_status") == record.get("submodule_status")
        and previous.get("git_fsck") == "PASS"
    )


def prepare_git_component(
    name: str,
    url: str,
    expected_ref: str,
    path: Path,
    previous_records: dict[str, dict[str, Any]],
    strict: bool,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "name": name,
        "url": url,
        "expected_ref": expected_ref,
        "path": str(path),
        "recursive_submodules": True,
        "submodule_count": 0,
        "submodule_status_clean": False,
        "git_fsck": "SKIPPED",
        "status": "unknown",
        "blocker_reason": "",
    }
    if not url or not expected_ref:
        record.update(status="blocked", blocker_reason="missing_url_or_ref")
        return record
    if is_system_path(path):
        record.update(status="blocked", blocker_reason="system_path_write_forbidden")
        return record
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and not (path / ".git").exists():
            record.update(status="blocked", blocker_reason="destination_exists_not_git_checkout")
            return record
        if not path.exists():
            run(["git", "clone", "--recursive", url, str(path)], check=True)
        remote_url = git_output(path, "config", "--get", "remote.origin.url")
        if remote_url and remote_url != url:
            record.update(status="blocked", blocker_reason=f"unexpected_origin:{remote_url}")
            return record
        fetch = run(["git", "-C", str(path), "fetch", "--tags", "--prune", "origin", expected_ref])
        if fetch.returncode != 0:
            record.update(status="blocked", blocker_reason="git_fetch_failed", details=(fetch.stdout + fetch.stderr).strip())
            return record
        checkout = run(["git", "-C", str(path), "checkout", "--detach", "FETCH_HEAD"])
        if checkout.returncode != 0:
            record.update(status="blocked", blocker_reason="git_checkout_failed", details=(checkout.stdout + checkout.stderr).strip())
            return record
        for cmd in (
            ["git", "-C", str(path), "submodule", "sync", "--recursive"],
            ["git", "-C", str(path), "submodule", "update", "--init", "--recursive"],
        ):
            proc = run(cmd)
            if proc.returncode != 0:
                record.update(status="blocked", blocker_reason="submodule_update_failed", details=(proc.stdout + proc.stderr).strip())
                return record
        actual_head = git_output(path, "rev-parse", "HEAD")
        status_short = git_output(path, "status", "--short")
        submodules = git_output(path, "submodule", "status", "--recursive")
        clean, reason = submodule_status_clean(submodules)
        record.update(
            actual_head=actual_head,
            status_short=status_short,
            submodule_status=submodules,
            submodule_count=len([line for line in submodules.splitlines() if line.strip()]),
            submodule_status_clean=clean,
            tree=tree_manifest(path),
        )
        if not clean:
            record.update(status="blocked", blocker_reason=reason)
            return record
        previous = previous_records.get(name, {})
        if should_skip_fsck(previous, record, strict):
            record["git_fsck"] = "SKIPPED_CACHED_PASS"
        else:
            fsck = run(["git", "-C", str(path), "fsck", "--full"])
            record["git_fsck"] = "PASS" if fsck.returncode == 0 else "FAIL"
            if fsck.returncode != 0:
                record.update(status="corrupt", blocker_reason="git_fsck_failed", details=(fsck.stdout + fsck.stderr).strip())
                return record
        record["status"] = "present"
        return record
    except Exception as exc:
        record.update(status="blocked", blocker_reason=str(exc))
        return record


def archive_can_list(path: Path) -> bool:
    try:
        with tarfile.open(path) as archive:
            archive.getmembers()
        return True
    except Exception:
        return False


def download(url: str, dest: Path) -> None:
    with urllib.request.urlopen(url, timeout=60) as response, dest.open("wb") as handle:
        shutil.copyfileobj(response, handle)


def expected_sha_from_url(url: str, archive_name: str, dest: Path) -> str:
    if not url:
        return ""
    download(url, dest)
    text = dest.read_text(encoding="utf-8", errors="replace")
    for line in text.splitlines():
        fields = line.split()
        if not fields:
            continue
        if len(fields) == 1 or archive_name in fields[-1]:
            return fields[0]
    return ""


def prepare_archive(name: str, url: str, expected_sha: str, sha_url: str, dest_dir: Path) -> dict[str, Any]:
    archive_name = url.rstrip("/").split("/")[-1] if url else ""
    path = dest_dir / archive_name if archive_name else dest_dir / name
    record: dict[str, Any] = {
        "name": name,
        "url": url,
        "path": str(path),
        "status": "unknown",
        "blocker_reason": "",
        "checksum_status": "checksum_unavailable",
    }
    if not url:
        record.update(status="blocked", blocker_reason="missing_url")
        return record
    if is_system_path(dest_dir):
        record.update(status="blocked", blocker_reason="system_path_write_forbidden")
        return record
    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
        if not path.is_file() or path.stat().st_size <= 0 or not archive_can_list(path):
            if path.exists():
                path.unlink()
            download(url, path)
        size = path.stat().st_size
        if size <= 0:
            record.update(status="corrupt", blocker_reason="empty_archive")
            return record
        if not archive_can_list(path):
            record.update(status="corrupt", blocker_reason="archive_list_failed")
            return record
        local_sha = sha256_file(path)
        record.update(size=size, sha256=local_sha, archive_list="PASS")
        expected = expected_sha
        if not expected and sha_url:
            expected = expected_sha_from_url(sha_url, archive_name, dest_dir / f"{name}.sha256")
        if expected:
            record["expected_sha256"] = expected
            record["checksum_status"] = "PASS" if expected == local_sha else "FAIL"
            if expected != local_sha:
                record.update(status="corrupt", blocker_reason="sha256_mismatch")
                return record
        record["status"] = "present"
        return record
    except Exception as exc:
        record.update(status="blocked", blocker_reason=str(exc))
        return record


def github_repo_path(url: str) -> str:
    repo = url
    for prefix in ("https://github.com/", "http://github.com/", "git@github.com:"):
        if repo.startswith(prefix):
            repo = repo[len(prefix) :]
            break
    repo = repo.removesuffix(".git").strip("/")
    if "/" not in repo:
        raise RuntimeError(f"not a GitHub owner/repo URL: {url}")
    return repo


def resolve_nginx_archive(env: dict[str, str]) -> tuple[str, str]:
    mode = env.get("NGINX_SOURCE_MODE", "github-release")
    if mode != "github-release":
        raise RuntimeError(f"unsupported NGINX_SOURCE_MODE={mode}")
    repo_url = env.get("NGINX_SOURCE_REPO_URL") or env.get("NGINX_GITHUB_REPO")
    tag = env.get("NGINX_RELEASE_TAG") or env.get("NGINX_SOURCE_GIT_REF") or "latest"
    if not repo_url:
        raise RuntimeError("missing NGINX_SOURCE_REPO_URL")
    repo = github_repo_path(repo_url)
    if tag == "latest":
        api_url = f"https://api.github.com/repos/{repo}/releases/latest"
        with urllib.request.urlopen(api_url, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
        tag = data.get("tag_name")
        if not isinstance(tag, str) or not tag:
            raise RuntimeError("GitHub latest release response missing tag_name")
    return tag, f"https://github.com/{repo}/archive/refs/tags/{tag}.tar.gz"


def default_state_home() -> Path:
    return Path(os.environ.get("XDG_STATE_HOME", str(Path.home() / ".local/state")))


def executable(path: Path) -> bool:
    return path.is_file() and os.access(path, os.X_OK)


def resolve_executable(configured: str) -> str | None:
    if not configured:
        return None
    if "/" in configured:
        path = Path(configured)
        return str(path) if executable(path) else None
    return shutil.which(configured)


def read_key_values(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if "=" not in line or line.lstrip().startswith("#"):
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def artifact_status(paths: dict[str, Path], executable_keys: set[str] | None = None) -> tuple[bool, list[str]]:
    executable_keys = executable_keys or set()
    missing = []
    for key, path in paths.items():
        if key in executable_keys:
            if not executable(path):
                missing.append(f"{key}:{path}")
        elif not path.is_file():
            missing.append(f"{key}:{path}")
    return not missing, missing


def build_env(base: dict[str, str], **overrides: str) -> dict[str, str]:
    result = dict(base)
    for key, value in overrides.items():
        if value is not None:
            result[key] = value
    return result


def run_build(script: Path, env: dict[str, str], cwd: Path, log_path: Path) -> subprocess.CompletedProcess[str]:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        ["sh", str(script)],
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    log_path.write_text(proc.stdout, encoding="utf-8", errors="replace")
    return proc


def map_apache_blocker(text: str, missing: list[str]) -> str:
    lowered = text.lower()
    if "expat.h" in lowered or "expat" in lowered and "header" in lowered:
        return "missing_expat_headers"
    if "missing required command" in lowered or "not found" in lowered:
        return "missing_apache_build_dependency"
    if any(item.startswith("modsecurity_lib:") for item in missing) or "libmodsecurity" in lowered:
        return "missing_libmodsecurity_build"
    return "missing_local_httpd_build"


def map_nginx_blocker(text: str, missing: list[str]) -> str:
    lowered = text.lower()
    if any(item.startswith("module_file:") for item in missing):
        return "missing_nginx_modsecurity_module"
    if any(item.startswith("modsecurity_lib:") for item in missing) or "libmodsecurity" in lowered:
        return "missing_libmodsecurity_build"
    if "missing required command" in lowered or "not found" in lowered:
        return "missing_nginx_build_dependency"
    return "missing_local_nginx_build"


def write_apachectl_wrapper(
    wrapper_path: Path,
    httpd_bin: Path,
    httpd_prefix: Path,
    modsecurity_lib_dir: Path,
    pcre2_lib_dir: Path,
) -> None:
    if is_system_path(wrapper_path):
        raise RuntimeError(f"system_path_write_forbidden: {wrapper_path}")
    wrapper_path.parent.mkdir(parents=True, exist_ok=True)
    content = f"""#!/bin/sh
set -eu

HTTPD_BIN={sh_quote(str(httpd_bin))}
HTTPD_PREFIX={sh_quote(str(httpd_prefix))}
MODSECURITY_LIB_DIR={sh_quote(str(modsecurity_lib_dir))}
PCRE2_LIB_DIR={sh_quote(str(pcre2_lib_dir))}

server_root=""
previous=""
for arg in "$@"; do
    if [ "$previous" = "-d" ]; then
        server_root=$arg
        previous=""
        continue
    fi
    if [ "$arg" = "-d" ]; then
        previous="-d"
    fi
done

if [ -n "$server_root" ]; then
    export APACHE_RUN_DIR="${{APACHE_RUN_DIR:-$server_root/run}}"
    export APACHE_LOCK_DIR="${{APACHE_LOCK_DIR:-$server_root/run}}"
    export APACHE_LOG_DIR="${{APACHE_LOG_DIR:-$server_root/log}}"
fi

if [ -z "${{APACHE_RUN_USER:-}}" ]; then
    if [ "$(id -u)" = "0" ]; then
        APACHE_RUN_USER=nobody
    else
        APACHE_RUN_USER=$(id -un)
    fi
    export APACHE_RUN_USER
fi
if [ -z "${{APACHE_RUN_GROUP:-}}" ]; then
    if [ "$(id -u)" = "0" ]; then
        APACHE_RUN_GROUP=$(getent group nogroup >/dev/null 2>&1 && printf '%s' nogroup || printf '%s' nobody)
    else
        APACHE_RUN_GROUP=$(id -gn)
    fi
    export APACHE_RUN_GROUP
fi

LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR:$HTTPD_PREFIX/lib:$PCRE2_LIB_DIR${{LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}}"
export LD_LIBRARY_PATH
exec "$HTTPD_BIN" "$@"
"""
    wrapper_path.write_text(content, encoding="utf-8")
    wrapper_path.chmod(0o755)


def prepare_apache_httpd(
    env: dict[str, str],
    connector_root: Path,
    framework_root: Path,
    cache_root: Path,
    build_root: Path,
    native_root: Path,
    sources_root: Path,
    archives_root: Path,
) -> dict[str, Any]:
    apache_build_root = Path(env.get("APACHE_BUILD_ROOT", str(build_root / "apache-build"))).resolve()
    httpd_prefix = Path(env.get("HTTPD_PREFIX", str(build_root / "apache-runtime/httpd"))).resolve()
    httpd_bin = Path(env.get("APACHE_HTTPD") or env.get("APACHE") or str(httpd_prefix / "bin/httpd")).resolve()
    apxs_bin = Path(env.get("APXS") or env.get("APXS_BIN") or str(httpd_prefix / "bin/apxs")).resolve()
    apache_module = Path(env.get("APACHE_MODULE", str(apache_build_root / "output/apache/mod_security3.so"))).resolve()
    modsecurity_lib_dir = Path(
        env.get("APACHE_MRTS_MODSECURITY_LIB_DIR", str(apache_build_root / "output/modsecurity/lib"))
    ).resolve()
    pcre2_prefix = Path(env.get("PCRE2_PREFIX", str(apache_build_root / "output/pcre2"))).resolve()
    pcre2_lib_dir = pcre2_prefix / "lib"
    wrapper_path = native_root / "apache2_ubuntu/bin/apachectl"
    override_apachectl = env.get("APACHECTL_BIN", "")
    effective_apachectl = Path(override_apachectl).resolve() if override_apachectl else wrapper_path
    artifacts = {
        "httpd_bin": httpd_bin,
        "apxs_bin": apxs_bin,
        "module_file": apache_module,
        "modsecurity_lib": modsecurity_lib_dir / "libmodsecurity.so",
    }
    ready, missing = artifact_status(artifacts, {"httpd_bin", "apxs_bin"})
    record: dict[str, Any] = {
        "source": "connector-local-build",
        "expected_ref": env.get("HTTPD_VERSION", ""),
        "cache_path": str(archives_root / "apache"),
        "build_path": str(apache_build_root),
        "httpd_prefix": str(httpd_prefix),
        "httpd_bin": str(httpd_bin),
        "apxs_bin": str(apxs_bin),
        "module_file": str(apache_module),
        "modsecurity_lib_dir": str(modsecurity_lib_dir),
        "apachectl_bin": str(effective_apachectl),
        "status": "unknown",
        "blocker_reason": "",
        "searched_paths": [str(path) for path in artifacts.values()],
        "env_override": "APACHECTL_BIN",
    }
    if override_apachectl and not executable(Path(override_apachectl)):
        record.update(status="blocked", blocker_reason="missing_local_httpd_build", missing_file=override_apachectl)
        return record
    if not ready:
        log_path = build_root / "logs/runtime-components/apache-build.log"
        proc = run_build(
            framework_root / "ci/prepare-apache-build.sh",
            build_env(
                env,
                FRAMEWORK_ROOT=str(framework_root),
                CONNECTOR_ROOT=str(connector_root),
                CONNECTOR_COMPONENT_CACHE=str(cache_root),
                SOURCE_ROOT=str(sources_root),
                MODSECURITY_SOURCE_DIR=str(sources_root / "ModSecurity_V3"),
                MODSECURITY_V3_SOURCE_DIR=str(sources_root / "ModSecurity_V3"),
                MODSECURITY_V3_ROOT=str(sources_root / "ModSecurity_V3"),
                BUILD_ROOT=str(build_root),
                TMP_ROOT=str(build_root / "tmp"),
                LOG_ROOT=str(build_root / "logs"),
                APACHE_BUILD_ROOT=str(apache_build_root),
                APACHE_BUILD_OWNER_ROOT=str(build_root),
                HTTPD_PREFIX=str(httpd_prefix),
                APACHE_DOWNLOAD_DIR=str(archives_root / "apache"),
                BUILD_HTTPD_FROM_SOURCE="1",
                BUILD_PCRE2_FROM_SOURCE="1",
                AUTO_FETCH_SMOKE_SOURCES="0",
                REFRESH="1",
                SKIP_RUNTIME_COMPONENT_PREPARE="1",
            ),
            connector_root,
            log_path,
        )
        record["build_log"] = str(log_path)
        record["build_exit_code"] = proc.returncode
        artifacts_file = apache_build_root / "logs/apache/artifacts.txt"
        if artifacts_file.is_file():
            record["artifacts"] = read_key_values(artifacts_file)
        ready, missing = artifact_status(artifacts, {"httpd_bin", "apxs_bin"})
        if proc.returncode != 0 or not ready:
            blocker = map_apache_blocker(proc.stdout, missing)
            blocker_details: dict[str, Any] = {}
            if blocker == "missing_expat_headers":
                blocker_details = {
                    "missing_file": "expat.h",
                    "build_component": "apache_httpd_source_build",
                    "env_variable_can_set": "CPPFLAGS/LDFLAGS",
                    "dependency_searched_paths": [env.get("CPPFLAGS") or "<compiler default include paths>"],
                }
            record.update(
                status="blocked",
                blocker_reason=blocker,
                missing_files=missing,
                **blocker_details,
            )
            return record
    try:
        if not override_apachectl:
            write_apachectl_wrapper(wrapper_path, httpd_bin, httpd_prefix, modsecurity_lib_dir, pcre2_lib_dir)
        elif not executable(Path(override_apachectl)):
            raise RuntimeError(f"APACHECTL_BIN is not executable: {override_apachectl}")
    except Exception as exc:
        record.update(status="blocked", blocker_reason="missing_local_httpd_build", details=str(exc))
        return record
    record.update(
        status="present",
        tree=tree_manifest(apache_build_root),
        apachectl_bin=str(effective_apachectl),
    )
    return record


def prepare_nginx_runtime(
    env: dict[str, str],
    connector_root: Path,
    framework_root: Path,
    cache_root: Path,
    build_root: Path,
    sources_root: Path,
    archives_root: Path,
) -> dict[str, Any]:
    nginx_build_root = Path(env.get("NGINX_BUILD_DIR", str(build_root / "nginx-build"))).resolve()
    nginx_prefix = Path(env.get("NGINX_PREFIX", str(build_root / "nginx-runtime/nginx"))).resolve()
    local_nginx_bin = Path(env.get("NGINX_BINARY", str(nginx_prefix / "sbin/nginx"))).resolve()
    local_module = Path(
        env.get("NGINX_MODULE", str(nginx_prefix / "modules/ngx_http_modsecurity_module.so"))
    ).resolve()
    modsecurity_lib_dir = Path(
        env.get("NGINX_MRTS_MODSECURITY_LIB_DIR", str(nginx_build_root / "output/modsecurity/lib"))
    ).resolve()
    override_bin = env.get("MRTS_NATIVE_NGINX_BIN", "")
    override_module_dir = env.get("MRTS_NATIVE_NGINX_MODULE_DIR", "")
    effective_bin = Path(override_bin).resolve() if override_bin else local_nginx_bin
    effective_module = (
        Path(override_module_dir).resolve() / "ngx_http_modsecurity_module.so"
        if override_module_dir
        else local_module
    )
    local_artifacts = {
        "nginx_bin": local_nginx_bin,
        "module_file": local_module,
        "modsecurity_lib": modsecurity_lib_dir / "libmodsecurity.so",
    }
    effective_artifacts = {
        "nginx_bin": effective_bin,
        "module_file": effective_module,
    }
    local_ready, local_missing = artifact_status(local_artifacts, {"nginx_bin"})
    effective_ready, effective_missing = artifact_status(effective_artifacts, {"nginx_bin"})
    record: dict[str, Any] = {
        "source": "connector-local-build",
        "expected_ref": env.get("NGINX_RELEASE_TAG") or env.get("NGINX_SOURCE_GIT_REF", ""),
        "cache_path": str(archives_root / "nginx"),
        "build_path": str(nginx_build_root),
        "nginx_prefix": str(nginx_prefix),
        "nginx_bin": str(effective_bin),
        "module_dir": str(effective_module.parent),
        "module_file": str(effective_module),
        "local_nginx_bin": str(local_nginx_bin),
        "local_module_file": str(local_module),
        "modsecurity_lib_dir": str(modsecurity_lib_dir),
        "status": "unknown",
        "blocker_reason": "",
        "searched_paths": [str(path) for path in local_artifacts.values()],
        "env_override": "MRTS_NATIVE_NGINX_BIN/MRTS_NATIVE_NGINX_MODULE_DIR",
    }
    if override_bin and not executable(Path(override_bin)):
        record.update(status="blocked", blocker_reason="missing_local_nginx_build", missing_file=override_bin)
        return record
    if override_module_dir and not (Path(override_module_dir) / "ngx_http_modsecurity_module.so").is_file():
        record.update(
            status="blocked",
            blocker_reason="missing_nginx_modsecurity_module",
            missing_file=str(Path(override_module_dir) / "ngx_http_modsecurity_module.so"),
        )
        return record
    if not effective_ready and not local_ready:
        log_path = build_root / "logs/runtime-components/nginx-build.log"
        proc = run_build(
            framework_root / "ci/prepare-nginx-build.sh",
            build_env(
                env,
                FRAMEWORK_ROOT=str(framework_root),
                CONNECTOR_ROOT=str(connector_root),
                CONNECTOR_COMPONENT_CACHE=str(cache_root),
                SOURCE_ROOT=str(sources_root),
                MODSECURITY_SOURCE_DIR=str(sources_root / "ModSecurity_V3"),
                MODSECURITY_V3_SOURCE_DIR=str(sources_root / "ModSecurity_V3"),
                MODSECURITY_V3_ROOT=str(sources_root / "ModSecurity_V3"),
                BUILD_ROOT=str(build_root),
                TMP_ROOT=str(build_root / "tmp"),
                LOG_ROOT=str(build_root / "logs"),
                NGINX_BUILD_DIR=str(nginx_build_root),
                NGINX_PREFIX=str(nginx_prefix),
                NGINX_BINARY=str(local_nginx_bin),
                NGINX_MODULE=str(local_module),
                NGINX_DOWNLOAD_DIR=str(archives_root / "nginx"),
                BUILD_NGINX_FROM_SOURCE="1",
                AUTO_FETCH_SMOKE_SOURCES="0",
                REFRESH="1",
                SKIP_RUNTIME_COMPONENT_PREPARE="1",
            ),
            connector_root,
            log_path,
        )
        record["build_log"] = str(log_path)
        record["build_exit_code"] = proc.returncode
        artifacts_file = nginx_build_root / "logs/nginx/artifacts.txt"
        if artifacts_file.is_file():
            record["artifacts"] = read_key_values(artifacts_file)
        local_ready, local_missing = artifact_status(local_artifacts, {"nginx_bin"})
        effective_ready, effective_missing = artifact_status(effective_artifacts, {"nginx_bin"})
        if proc.returncode != 0 or not local_ready:
            blocker = map_nginx_blocker(proc.stdout, local_missing)
            blocker_details = {
                "build_component": "nginx_modsecurity_module_build",
                "env_variable_can_set": "MRTS_NATIVE_NGINX_BIN/MRTS_NATIVE_NGINX_MODULE_DIR",
            }
            if blocker == "missing_libmodsecurity_build":
                blocker_details["build_component"] = "libmodsecurity_build"
            elif blocker == "missing_local_nginx_build":
                blocker_details["build_component"] = "nginx_source_build"
            record.update(
                status="blocked",
                blocker_reason=blocker,
                missing_files=local_missing,
                **blocker_details,
            )
            return record
    if not override_bin:
        effective_bin = local_nginx_bin
    if not override_module_dir:
        effective_module = local_module
    effective_ready, effective_missing = artifact_status(
        {"nginx_bin": effective_bin, "module_file": effective_module},
        {"nginx_bin"},
    )
    if not effective_ready:
        blocker = map_nginx_blocker("", effective_missing)
        record.update(
            status="blocked",
            blocker_reason=blocker,
            missing_files=effective_missing,
            build_component="nginx_native_runtime_inventory",
            env_variable_can_set="MRTS_NATIVE_NGINX_BIN/MRTS_NATIVE_NGINX_MODULE_DIR",
        )
        return record
    record.update(
        status="present",
        nginx_bin=str(effective_bin),
        module_dir=str(effective_module.parent),
        module_file=str(effective_module),
        tree=tree_manifest(nginx_build_root),
    )
    return record


def known_tool_source(tool: str, roots: list[Path]) -> tuple[str, str, bool]:
    token = f"github.com/coreruleset/{tool}"
    source_url = ""
    known_ref = ""
    can_build = False
    build_markers = (f"go install {token}", f"git clone https://{token}", f"git clone git@github.com:coreruleset/{tool}")
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if ".git" in path.parts or not path.is_file():
                continue
            if path.suffix not in {"", ".md", ".sh", ".py", ".txt", ".yaml", ".yml", ".mk", ".json"}:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if token in text and not source_url:
                source_url = f"https://{token}"
            if any(marker in text for marker in build_markers):
                can_build = True
            if token in text and "ref=" in text and not known_ref:
                known_ref = "see " + str(path)
    return source_url, known_ref, can_build


def inventory_tool(
    dependency: str,
    env_var: str,
    default: str,
    env: dict[str, str],
    cache_root: Path,
    build_root: Path,
    native_root: Path,
    source_roots: list[Path],
) -> dict[str, Any]:
    configured = env.get(env_var, "")
    candidates = []
    if configured:
        candidates.append(configured)
    candidates.extend(
        [
            default,
            str(cache_root / f"bin/{dependency}"),
            str(cache_root / f"tools/{dependency}"),
            str(build_root / f"bin/{dependency}"),
            str(build_root / f"tools/{dependency}"),
            str(native_root / f"bin/{dependency}"),
        ]
    )
    searched = []
    resolved = ""
    for candidate in candidates:
        if not candidate or candidate in searched:
            continue
        searched.append(candidate)
        path = resolve_executable(candidate)
        if path and not resolved:
            resolved = path
    source_url, known_ref, can_build = known_tool_source(dependency, source_roots)
    status = "present" if resolved else "blocked"
    blocker = "" if resolved else f"missing_{dependency.replace('-', '_')}_source_ref"
    return {
        "dependency": dependency,
        "status": status,
        "path": resolved,
        "searched_paths": searched,
        "env_override": env_var,
        "known_source": source_url,
        "known_source_url": source_url,
        "known_ref": known_ref,
        "can_build_locally": can_build and bool(known_ref),
        "blocker_reason": blocker,
    }


def dependency_inventory(
    apache_httpd: dict[str, Any],
    nginx: dict[str, Any],
    go_ftw: dict[str, Any],
    albedo: dict[str, Any],
) -> list[dict[str, Any]]:
    return [
        {
            "name": "go-ftw",
            "env_var": "GO_FTW_BIN",
            "path": go_ftw.get("path"),
            "status": "present" if go_ftw.get("status") == "present" else "missing",
            "access": "read-only/executable",
        },
        {
            "name": "albedo",
            "env_var": "ALBEDO_BIN",
            "path": albedo.get("path"),
            "status": "present" if albedo.get("status") == "present" else "missing",
            "access": "read-only/executable",
        },
        {
            "name": "apachectl",
            "env_var": "APACHECTL_BIN",
            "path": apache_httpd.get("apachectl_bin"),
            "status": "present" if apache_httpd.get("status") == "present" else "missing",
            "access": "local-wrapper/read-only-executable",
        },
        {
            "name": "nginx",
            "env_var": "MRTS_NATIVE_NGINX_BIN",
            "path": nginx.get("nginx_bin"),
            "status": "present" if nginx.get("status") == "present" else "missing",
            "access": "local-build/read-only-executable",
        },
        {
            "name": "ngx_http_modsecurity_module.so",
            "env_var": "MRTS_NATIVE_NGINX_MODULE_DIR",
            "path": nginx.get("module_file"),
            "status": "present" if nginx.get("status") == "present" else "missing",
            "access": "local-build/module-reference",
        },
    ]


def markdown_report(payload: dict[str, Any]) -> str:
    apache = payload.get("apache_httpd", {})
    nginx = payload.get("nginx", {})
    go_ftw = payload.get("go_ftw", {})
    albedo = payload.get("albedo", {})
    lines = [
        "# Runtime Component Cache",
        "",
        f"Generated at: `{payload['generated_at']}`",
        f"Cache root: `{payload['cache_root']}`",
        "",
        "## Prepare Phases",
    ]
    for phase in payload.get("prepare_phases", []):
        lines.append(f"- {phase}")
    lines.extend(
        [
            "",
            "## Apache httpd",
            f"- Status: `{apache.get('status', '-')}`",
            f"- Blocker: `{apache.get('blocker_reason') or '-'}`",
            f"- Source: `{apache.get('source', '-')}`",
            f"- Expected ref/version: `{apache.get('expected_ref', '-')}`",
            f"- Cache path: `{apache.get('cache_path', '-')}`",
            f"- Build path: `{apache.get('build_path', '-')}`",
            f"- apachectl/APACHECTL_BIN: `{apache.get('apachectl_bin', '-')}`",
            f"- Missing file: `{apache.get('missing_file') or '-'}`",
            f"- Build component: `{apache.get('build_component') or '-'}`",
            f"- Env variable to set: `{apache.get('env_variable_can_set') or apache.get('env_override') or '-'}`",
            "",
            "## NGINX",
            f"- Status: `{nginx.get('status', '-')}`",
            f"- Blocker: `{nginx.get('blocker_reason') or '-'}`",
            f"- Source: `{nginx.get('source', '-')}`",
            f"- Expected ref/version: `{nginx.get('expected_ref', '-')}`",
            f"- Cache path: `{nginx.get('cache_path', '-')}`",
            f"- Build path: `{nginx.get('build_path', '-')}`",
            f"- MRTS_NATIVE_NGINX_BIN: `{nginx.get('nginx_bin', '-')}`",
            f"- MRTS_NATIVE_NGINX_MODULE_DIR: `{nginx.get('module_dir', '-')}`",
            f"- Module file: `{nginx.get('module_file', '-')}`",
            f"- Missing file: `{nginx.get('missing_file') or '-'}`",
            f"- Build component: `{nginx.get('build_component') or '-'}`",
            f"- Env variable to set: `{nginx.get('env_variable_can_set') or nginx.get('env_override') or '-'}`",
            "",
            "## go-ftw / albedo",
            "| Dependency | Status | Env override | Known source | Known ref | Can build locally | Blocker |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for item in (go_ftw, albedo):
        lines.append(
            "| {dep} | {status} | `{env}` | `{source}` | `{ref}` | {can_build} | {blocker} |".format(
                dep=item.get("dependency", "-"),
                status=item.get("status", "-"),
                env=item.get("env_override", "-"),
                source=item.get("known_source") or "-",
                ref=item.get("known_ref") or "-",
                can_build="yes" if item.get("can_build_locally") else "no",
                blocker=item.get("blocker_reason") or "-",
            )
        )
    lines.extend(
        [
        "",
        "## Git Components",
        "| Name | Status | Ref | Head | Submodules | fsck | Blocker |",
        "|---|---|---|---|---:|---|---|",
        ]
    )
    for item in payload["git_components"]:
        lines.append(
            "| {name} | {status} | `{ref}` | `{head}` | {subs} | {fsck} | {blocker} |".format(
                name=item.get("name", "-"),
                status=item.get("status", "-"),
                ref=item.get("expected_ref", "-"),
                head=item.get("actual_head", "-"),
                subs=item.get("submodule_count", 0),
                fsck=item.get("git_fsck", "-"),
                blocker=item.get("blocker_reason", "-") or "-",
            )
        )
    lines.extend(["", "## Archives", "| Name | Status | Checksum | Path | Blocker |", "|---|---|---|---|---|"])
    for item in payload["archives"]:
        lines.append(
            "| {name} | {status} | {checksum} | `{path}` | {blocker} |".format(
                name=item.get("name", "-"),
                status=item.get("status", "-"),
                checksum=item.get("checksum_status", "-"),
                path=item.get("path", "-"),
                blocker=item.get("blocker_reason", "-") or "-",
            )
        )
    lines.extend(["", "## Local Dependencies", "| Name | Status | Env | Path | Access |", "|---|---|---|---|---|"])
    for item in payload["dependencies"]:
        lines.append(
            "| {name} | {status} | `{env}` | `{path}` | {access} |".format(
                name=item.get("name", "-"),
                status=item.get("status", "-"),
                env=item.get("env_var", "-"),
                path=item.get("path") or item.get("configured") or "-",
                access=item.get("access", "-"),
            )
        )
    lines.extend(
        [
            "",
            "## Guardrails",
            "- System paths are not used for runtime component writes.",
            "- Runtime writes are constrained to cache/build/runtime roots.",
            "- Native Apache and NGINX use local prepared components when env overrides are absent.",
            "- go-ftw and albedo are inventoried only; no source/ref is guessed.",
            "- `RUNTIME_COMPONENT_STRICT_VERIFY=1` forces full git fsck.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector-root", required=True)
    parser.add_argument("--framework-root", required=True)
    parser.add_argument("--cache-root", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--build-root", default=None)
    parser.add_argument("--native-root", default=None)
    args = parser.parse_args()

    env = dict(os.environ)
    connector_root = Path(args.connector_root).resolve()
    framework_root = Path(args.framework_root).resolve()
    cache_root = Path(args.cache_root).resolve()
    output_root = Path(args.output_root).resolve()
    build_root = Path(args.build_root or env.get("BUILD_ROOT", str(default_state_home() / "ModSecurity-conector-build"))).resolve()
    native_root = Path(args.native_root or env.get("MRTS_NATIVE_ROOT", str(build_root / "mrts-native"))).resolve()
    report_dir = output_root / "reports/testing/generated"
    strict = env.get("RUNTIME_COMPONENT_STRICT_VERIFY") == "1"
    if is_system_path(cache_root):
        print(
            "prepare-runtime-components: BLOCKED cache: system_path_write_forbidden "
            f"path={cache_root}"
        )
        return 77
    for label, path in (("BUILD_ROOT", build_root), ("MRTS_NATIVE_ROOT", native_root)):
        if is_system_path(path):
            print(f"prepare-runtime-components: BLOCKED {label}: system_path_write_forbidden path={path}")
            return 77
    cache_root.mkdir(parents=True, exist_ok=True)
    build_root.mkdir(parents=True, exist_ok=True)
    native_root.mkdir(parents=True, exist_ok=True)

    previous_manifest = read_json(cache_root / "manifest.json")
    previous_git = {
        str(item.get("name")): item
        for item in previous_manifest.get("git_components", [])
        if isinstance(item, dict) and item.get("name")
    }

    sources_root = cache_root / "sources"
    archives_root = cache_root / "archives"
    modsec_path = sources_root / "ModSecurity_V3"
    crs_path = sources_root / "coreruleset"
    haproxy_source_root = sources_root / "haproxy"
    prepare_phases = [
        "1. validate safe paths",
        "2. prepare git/source/archive cache recursively",
        "3. prepare/build local ModSecurity if required",
        "4. prepare/build local Apache/httpd for Apache connector/native",
        "5. prepare/build local NGINX + ngx_http_modsecurity_module.so for NGINX connector/native",
        "6. inventory go-ftw/albedo",
        "7. write manifests/reports",
    ]

    git_components = [
        prepare_git_component(
            "modsecurity-v3",
            env.get("MODSECURITY_V3_GIT_URL") or env.get("MODSECURITY_REPO_URL", ""),
            env.get("MODSECURITY_V3_GIT_REF") or env.get("MODSECURITY_GIT_REF", ""),
            modsec_path,
            previous_git,
            strict,
        ),
        prepare_git_component(
            "coreruleset",
            env.get("CRS_REPO_URL", ""),
            env.get("CRS_GIT_REF", ""),
            crs_path,
            previous_git,
            strict,
        ),
    ]
    if env.get("ALLOW_EXTERNAL_CONNECTOR_REPOS") == "1":
        for name, url_key, ref_key in (
            ("modsecurity-apache", "MODSECURITY_APACHE_GIT_URL", "MODSECURITY_APACHE_GIT_REF"),
            ("modsecurity-nginx", "MODSECURITY_NGINX_GIT_URL", "MODSECURITY_NGINX_GIT_REF"),
        ):
            url = env.get(url_key, "")
            ref = env.get(ref_key, "")
            if not url or not ref:
                git_components.append(
                    {
                        "name": name,
                        "url": url,
                        "expected_ref": ref,
                        "path": str(sources_root / name),
                        "status": "blocked",
                        "blocker_reason": "missing_url_or_ref",
                    }
                )
            else:
                git_components.append(prepare_git_component(name, url, ref, sources_root / name, previous_git, strict))

    archives = [
        prepare_archive("httpd", env.get("HTTPD_SOURCE_URL", ""), env.get("HTTPD_SHA256", ""), env.get("HTTPD_SHA256_URL", ""), archives_root / "apache"),
        prepare_archive("apr", env.get("APR_SOURCE_URL", ""), env.get("APR_SHA256", ""), env.get("APR_SHA256_URL", ""), archives_root / "apache"),
        prepare_archive("apr-util", env.get("APR_UTIL_SOURCE_URL", ""), env.get("APR_UTIL_SHA256", ""), env.get("APR_UTIL_SHA256_URL", ""), archives_root / "apache"),
        prepare_archive("pcre2", env.get("PCRE2_SOURCE_URL", ""), env.get("PCRE2_SHA256", ""), env.get("PCRE2_SHA256_URL", ""), archives_root / "apache"),
        prepare_archive("haproxy", env.get("HAPROXY_SOURCE_URL", ""), env.get("HAPROXY_SHA256", ""), env.get("HAPROXY_SHA256_URL", ""), archives_root / "haproxy"),
    ]
    try:
        nginx_tag, nginx_url = resolve_nginx_archive(env)
        nginx_record = prepare_archive("nginx", nginx_url, env.get("NGINX_SHA256", ""), "", archives_root / "nginx")
        nginx_record["resolved_tag"] = nginx_tag
        archives.append(nginx_record)
    except Exception as exc:
        archives.append({"name": "nginx", "status": "blocked", "blocker_reason": str(exc), "checksum_status": "unknown"})

    apache_httpd = prepare_apache_httpd(
        env,
        connector_root,
        framework_root,
        cache_root,
        build_root,
        native_root,
        sources_root,
        archives_root,
    )
    nginx = prepare_nginx_runtime(
        env,
        connector_root,
        framework_root,
        cache_root,
        build_root,
        sources_root,
        archives_root,
    )
    source_roots = [connector_root, framework_root]
    go_ftw = inventory_tool("go-ftw", "GO_FTW_BIN", "go-ftw", env, cache_root, build_root, native_root, source_roots)
    albedo = inventory_tool("albedo", "ALBEDO_BIN", "albedo", env, cache_root, build_root, native_root, source_roots)

    runtime_env = {
        "CONNECTOR_COMPONENT_CACHE": str(cache_root),
        "SOURCE_ROOT": str(sources_root),
        "MODSECURITY_SOURCE_DIR": str(modsec_path),
        "MODSECURITY_V3_SOURCE_DIR": str(modsec_path),
        "MODSECURITY_V3_ROOT": str(modsec_path),
        "CRS_SOURCE_DIR": str(crs_path),
        "APACHE_DOWNLOAD_DIR": str(archives_root / "apache"),
        "NGINX_DOWNLOAD_DIR": str(archives_root / "nginx"),
        "HAPROXY_SOURCE_ROOT": str(haproxy_source_root),
        "HAPROXY_DOWNLOAD_DIR": str(archives_root / "haproxy"),
        "HAPROXY_SOURCE_DIR": str(haproxy_source_root / f"haproxy-{env.get('HAPROXY_VERSION', '3.2.19')}"),
    }
    if apache_httpd.get("status") == "present":
        runtime_env.update(
            {
                "APACHECTL_BIN": str(apache_httpd.get("apachectl_bin", "")),
                "APACHE_HTTPD": str(apache_httpd.get("httpd_bin", "")),
                "APXS": str(apache_httpd.get("apxs_bin", "")),
                "APXS_BIN": str(apache_httpd.get("apxs_bin", "")),
                "HTTPD_PREFIX": str(apache_httpd.get("httpd_prefix", "")),
                "APACHE_MODULE": str(apache_httpd.get("module_file", "")),
                "APACHE_MRTS_MODULE": str(apache_httpd.get("module_file", "")),
                "APACHE_MRTS_MODSECURITY_LIB_DIR": str(apache_httpd.get("modsecurity_lib_dir", "")),
            }
        )
    if nginx.get("status") == "present":
        runtime_env.update(
            {
                "MRTS_NATIVE_NGINX_BIN": str(nginx.get("nginx_bin", "")),
                "MRTS_NATIVE_NGINX_MODULE_DIR": str(nginx.get("module_dir", "")),
                "MRTS_NATIVE_NGINX_MODULE_FILE": str(nginx.get("module_file", "")),
                "MRTS_NATIVE_NGINX_MODSECURITY_LIB_DIR": str(nginx.get("modsecurity_lib_dir", "")),
                "NGINX_PREFIX": str(nginx.get("nginx_prefix", "")),
            }
        )
    if go_ftw.get("path"):
        runtime_env["GO_FTW_BIN"] = str(go_ftw["path"])
    if albedo.get("path"):
        runtime_env["ALBEDO_BIN"] = str(albedo["path"])
    env_path = cache_root / "runtime-env.sh"
    env_path.write_text(
        "\n".join(f"export {key}={sh_quote(value)}" for key, value in sorted(runtime_env.items())) + "\n",
        encoding="utf-8",
    )

    payload = {
        "generated_at": utc_now(),
        "cache_root": str(cache_root),
        "connector_root": str(connector_root),
        "framework_root": str(framework_root),
        "build_root": str(build_root),
        "native_root": str(native_root),
        "strict_verify": strict,
        "prepare_phases": prepare_phases,
        "runtime_env": runtime_env,
        "git_components": git_components,
        "archives": archives,
        "apache_httpd": apache_httpd,
        "nginx": nginx,
        "go_ftw": go_ftw,
        "albedo": albedo,
        "dependencies": dependency_inventory(apache_httpd, nginx, go_ftw, albedo),
        "guardrails": {
            "system_paths_read_only": True,
            "no_new_external_sources": True,
            "fsck_cache_enabled": True,
            "native_system_apachectl_dependency": False,
            "native_system_nginx_dependency": False,
        },
    }
    write_json(cache_root / "manifest.json", payload)
    write_json(cache_root / "git-components.json", {"generated_at": payload["generated_at"], "components": git_components})
    write_json(report_dir / "runtime-component-cache.generated.json", payload)
    (report_dir / "runtime-component-cache.generated.md").write_text(markdown_report(payload), encoding="utf-8")
    postprocess = connector_root / "ci/update-runtime-reports.py"
    if postprocess.is_file():
        run([sys.executable, str(postprocess), "--connector-root", str(connector_root)])

    blocked = [
        item
        for item in git_components + archives
        if item.get("status") in {"blocked", "corrupt"} and item.get("name") not in {"nginx"}
    ]
    nginx_blocked = [item for item in archives if item.get("name") == "nginx" and item.get("status") in {"blocked", "corrupt"}]
    blocked.extend(nginx_blocked)
    for component_name, component in (("apache_httpd", apache_httpd), ("nginx", nginx)):
        if component.get("status") in {"blocked", "corrupt"}:
            blocked.append({"name": component_name, **component})
    if blocked:
        for item in blocked:
            print(f"prepare-runtime-components: BLOCKED {item.get('name')}: {item.get('blocker_reason')}")
        return 77
    print(f"prepare-runtime-components: cache={cache_root}")
    print(f"prepare-runtime-components: report={report_dir / 'runtime-component-cache.generated.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
