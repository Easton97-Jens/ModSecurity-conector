#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
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


def dependency_inventory(env: dict[str, str]) -> list[dict[str, Any]]:
    deps = []
    for name, env_var, default in (
        ("go-ftw", "GO_FTW_BIN", "go-ftw"),
        ("albedo", "ALBEDO_BIN", "albedo"),
        ("apachectl", "APACHECTL_BIN", "apachectl"),
        ("nginx", "MRTS_NATIVE_NGINX_BIN", "nginx"),
    ):
        configured = env.get(env_var) or default
        path = shutil.which(configured) if "/" not in configured else (configured if Path(configured).exists() else None)
        deps.append(
            {
                "name": name,
                "env_var": env_var,
                "configured": configured,
                "path": path,
                "status": "present" if path else "missing",
                "access": "read-only/executable",
            }
        )
    module_dir = env.get("MRTS_NATIVE_NGINX_MODULE_DIR", "/usr/lib/nginx/modules")
    module_path = Path(module_dir) / "ngx_http_modsecurity_module.so"
    deps.append(
        {
            "name": "ngx_http_modsecurity_module.so",
            "env_var": "MRTS_NATIVE_NGINX_MODULE_DIR",
            "configured": module_dir,
            "path": str(module_path),
            "status": "present" if module_path.is_file() else "missing",
            "access": "read-only/module-reference",
        }
    )
    return deps


def markdown_report(payload: dict[str, Any]) -> str:
    lines = [
        "# Runtime Component Cache",
        "",
        f"Generated at: `{payload['generated_at']}`",
        f"Cache root: `{payload['cache_root']}`",
        "",
        "## Git Components",
        "| Name | Status | Ref | Head | Submodules | fsck | Blocker |",
        "|---|---|---|---|---:|---|---|",
    ]
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
            "- System paths are read-only dependencies.",
            "- Runtime writes are constrained to cache/build/runtime roots.",
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
    args = parser.parse_args()

    env = dict(os.environ)
    connector_root = Path(args.connector_root).resolve()
    framework_root = Path(args.framework_root).resolve()
    cache_root = Path(args.cache_root).resolve()
    output_root = Path(args.output_root).resolve()
    report_dir = output_root / "reports/testing/generated"
    strict = env.get("RUNTIME_COMPONENT_STRICT_VERIFY") == "1"
    if is_system_path(cache_root):
        print(
            "prepare-runtime-components: BLOCKED cache: system_path_write_forbidden "
            f"path={cache_root}"
        )
        return 77
    cache_root.mkdir(parents=True, exist_ok=True)

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
        "strict_verify": strict,
        "runtime_env": runtime_env,
        "git_components": git_components,
        "archives": archives,
        "dependencies": dependency_inventory(env),
        "guardrails": {
            "system_paths_read_only": True,
            "no_new_external_sources": True,
            "fsck_cache_enabled": True,
        },
    }
    write_json(cache_root / "manifest.json", payload)
    write_json(cache_root / "git-components.json", {"generated_at": payload["generated_at"], "components": git_components})
    write_json(report_dir / "runtime-component-cache.generated.json", payload)
    (report_dir / "runtime-component-cache.generated.md").write_text(markdown_report(payload), encoding="utf-8")

    blocked = [
        item
        for item in git_components + archives
        if item.get("status") in {"blocked", "corrupt"} and item.get("name") not in {"nginx"}
    ]
    nginx_blocked = [item for item in archives if item.get("name") == "nginx" and item.get("status") in {"blocked", "corrupt"}]
    blocked.extend(nginx_blocked)
    if blocked:
        for item in blocked:
            print(f"prepare-runtime-components: BLOCKED {item.get('name')}: {item.get('blocker_reason')}")
        return 77
    print(f"prepare-runtime-components: cache={cache_root}")
    print(f"prepare-runtime-components: report={report_dir / 'runtime-component-cache.generated.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
