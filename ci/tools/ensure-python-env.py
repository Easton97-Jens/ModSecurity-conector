#!/usr/bin/env python3
"""Provide the local Python environment for the current version contract.

The root Makefile runs this helper before local Framework-delegated targets.
It reuses a virtual environment only when the environment's identity matches
the exact interpreter selected by `.python-version` and the hashes of the
pinned Framework's reviewed dependency locks and installer. Any change
provisions a fresh environment for the new identity.

Dependencies are installed exclusively through the Framework-owned,
hash-verifying `install-ci-dependencies.py`; this helper never resolves
packages itself. CI does not use it and keeps its explicit toolcache setup.

Exit status: 0 ready, 1 provisioning failed, 77 blocked prerequisite.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

BLOCKED = 77
SCHEMA = 1
STAMP = "msconnector-python-env.json"
VERSION_FILE = ".python-version"
CHECKOUT_LINK = ".venv"
VENV_PYTHON = Path("bin/python")
FRAMEWORK_DEFAULT = Path("modules/ModSecurity-test-Framework")
INSTALLER = Path("connector_suite/modsecurity_connector_ci/tools/install-ci-dependencies.py")
# Every file the installer reads to select artifacts, plus the installer.
FRAMEWORK_INPUTS = (
    Path("connector_suite/requirements-ci.lock"),
    Path("connector_suite/requirements-ci-build.lock"),
    INSTALLER,
    Path("requirements-ci.lock"),
)
PROBE = (
    "import importlib.metadata as m, json, sys\n"
    "import yaml\n"
    "print(json.dumps({'version': '%d.%d.%d' % sys.version_info[:3],"
    " 'virtual': sys.prefix != sys.base_prefix,"
    " 'distributions': sorted([d.metadata['Name'].lower(), d.version]"
    " for d in m.distributions())}))\n"
)
UNMANAGED_HINT = "remove or rename it, or set PYTHON_ENV_AUTO=0 to keep using it unmanaged"


class Blocked(Exception):
    """A prerequisite is missing or an existing path must not be replaced."""


@dataclass(frozen=True)
class Checkout:
    connector: Path
    framework: Path
    revision: str


@dataclass(frozen=True)
class Layout:
    environment: Path
    store: Path | None
    link: Path | None
    alias: Path | None = None


def say(message: str) -> None:
    print(f"python-env: {message}", file=sys.stderr, flush=True)


def digest(path: Path) -> str:
    if not path.is_file():
        raise Blocked(f"required version input is missing: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checkout_roots() -> Checkout:
    connector = Path(os.environ.get("CONNECTOR_ROOT") or Path(__file__).resolve().parents[2])
    framework = Path(os.environ.get("TEST_ROOT") or os.environ.get("FRAMEWORK_ROOT")
                     or connector / FRAMEWORK_DEFAULT)
    if not connector.is_absolute() or not framework.is_absolute():
        raise Blocked("CONNECTOR_ROOT and FRAMEWORK_ROOT must be absolute directories")
    if not (framework / INSTALLER).is_file():
        raise Blocked(f"pinned Framework installer is missing under {framework}; "
                      "run make check-framework")
    revision = os.environ.get("CONNECTOR_REVISION") or subprocess.run(
        ["git", "-C", str(connector), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True).stdout.strip()
    return Checkout(connector, framework, revision)


def required_version(connector: Path) -> str:
    version = (connector / VERSION_FILE).read_text(encoding="ascii").strip()
    if re.fullmatch(r"\d+\.\d+\.\d+", version) is None:
        raise Blocked(f"{VERSION_FILE} must select an exact X.Y.Z interpreter")
    return version


def interpreter_version(executable: str) -> str | None:
    if executable == sys.executable:
        return "%d.%d.%d" % sys.version_info[:3]
    try:
        completed = subprocess.run(
            [executable, "-I", "-c", "import sys; print('%d.%d.%d' % sys.version_info[:3])"],
            capture_output=True, text=True, timeout=30, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    return completed.stdout.strip() if completed.returncode == 0 else None


def select_base(version: str, explicit: str | None) -> Path:
    """Return the real path of an interpreter with exactly the pinned version."""
    major_minor = ".".join(version.split(".")[:2])
    candidates = [explicit] if explicit else [sys.executable, f"python{major_minor}", "python3"]
    seen = []
    for candidate in candidates:
        located = candidate if os.sep in candidate else shutil.which(candidate)
        if not located:
            continue
        observed = interpreter_version(located)
        seen.append(f"{candidate}={observed or 'unusable'}")
        if observed == version:
            return Path(os.path.realpath(located))
    raise Blocked(f"no Python {version} interpreter as selected by {VERSION_FILE} "
                  f"(checked {', '.join(seen) or 'nothing'}); install it or set "
                  f"PYTHON_BASE=/path/to/python{major_minor}")


def identity(role: str, version: str, base: Path, checkout: Checkout) -> tuple[str, dict[str, str]]:
    inputs = {VERSION_FILE: digest(checkout.connector / VERSION_FILE),
              "ci/tools/ensure-python-env.py": digest(Path(__file__).resolve())}
    for relative in FRAMEWORK_INPUTS:
        inputs[f"framework:{relative.as_posix()}"] = digest(checkout.framework / relative)
    material = json.dumps({"schema": SCHEMA, "role": role, "python": version,
                           "base": str(base), "inputs": inputs}, sort_keys=True)
    return hashlib.sha256(material.encode("utf-8")).hexdigest(), inputs


def probe(python: Path) -> dict | None:
    try:
        completed = subprocess.run([str(python), "-I", "-c", PROBE], capture_output=True,
                                   text=True, timeout=60, check=False)
        return json.loads(completed.stdout) if completed.returncode == 0 else None
    except (OSError, ValueError, subprocess.SubprocessError):
        return None


def read_stamp(environment: Path) -> dict | None:
    try:
        return json.loads((environment / STAMP).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def is_current(environment: Path, key: str) -> bool:
    """Accept only the recorded identity with unchanged installed contents."""
    stamp = read_stamp(environment)
    if not stamp or stamp.get("schema") != SCHEMA or stamp.get("key") != key:
        return False
    return probe(environment / VENV_PYTHON) == stamp.get("probe")


def managed_store(link: Path) -> Path | None:
    """Return the external store of a checkout link created by this helper."""
    if not link.is_symlink():
        return None
    stamp = read_stamp(link.resolve())
    return link.resolve().parent if stamp and stamp.get("role") == "parent" else None


def layout(role: str, version: str, key: str, connector: Path) -> Layout:
    """Select the environment: a versioned store entry or the checkout's .venv."""
    checkout_link = connector / CHECKOUT_LINK
    configured = os.environ.get("PYTHON_ENV_ROOT", "")
    store = Path(configured) if configured else managed_store(checkout_link)
    link = checkout_link if role == "parent" else None
    if store is not None:
        if not store.is_absolute() or store.resolve().is_relative_to(connector.resolve()):
            raise Blocked("PYTHON_ENV_ROOT must be an absolute directory outside the checkout")
        return Layout(store / f"{role}-{version}-{key[:12]}", store, link, store / role)
    if role != "parent":
        raise Blocked("the framework environment requires PYTHON_ENV_ROOT outside all checkouts")
    if checkout_link.is_symlink():
        raise Blocked(f"{checkout_link} links to an unmanaged location; remove it, "
                      "set PYTHON_ENV_ROOT, or set PYTHON_ENV_AUTO=0")
    return Layout(checkout_link, None, None)


def replace_link(link: Path, target: Path, store: Path, *, checkout: bool = False) -> None:
    """Atomically point a helper-owned link at the selected environment.

    Only a link into the store, or a helper-provisioned in-checkout parent
    environment, may be replaced; anything else is reported, never removed.
    """
    if link.is_symlink():
        current = Path(os.path.realpath(link))
        if current == target.resolve():
            return
        if current.parent != store.resolve() and current.exists():
            raise Blocked(f"{link} links outside {store}; remove it or set PYTHON_ENV_AUTO=0")
    elif link.exists():
        stamp = read_stamp(link)
        if not checkout or not stamp or stamp.get("role") != "parent":
            raise Blocked(f"{link} is an unmanaged environment; {UNMANAGED_HINT}")
        try:
            shutil.rmtree(link)
        except OSError as error:
            raise RuntimeError(f"cannot remove the previous in-checkout environment "
                               f"{link}: {error}") from error
        say(f"replaced the previous in-checkout environment by a link into {store}")
    temporary = link.with_name(f".{link.name}.tmp-{os.getpid()}")
    try:
        os.symlink(target, temporary)
        os.replace(temporary, link)
    except OSError as error:
        if temporary.is_symlink():
            temporary.unlink()
        raise RuntimeError(f"cannot point {link} at {target}: {error}") from error


def linked(selected: Layout) -> bool:
    """Require this checkout's link and an existing latest-environment alias."""
    if selected.alias is not None and not selected.alias.exists():
        return False
    if selected.link is None or selected.store is None:
        return True
    return selected.link.is_symlink() and (
        Path(os.path.realpath(selected.link)) == selected.environment.resolve())


def installer_environment(checkout: Checkout) -> dict[str, str]:
    child = dict(os.environ)
    framework = checkout.framework
    child.update(CONNECTOR_ROOT=str(checkout.connector), CONNECTOR_REVISION=checkout.revision,
                 TEST_ROOT=str(framework), FRAMEWORK_ROOT=str(framework),
                 PYTHONPATH=f"{framework}{os.pathsep}{framework / 'connector_suite'}",
                 PYTHONNOUSERSITE="1", PYTHONDONTWRITEBYTECODE="1",
                 PIP_REQUIRE_VIRTUALENV="true", PIP_DISABLE_PIP_VERSION_CHECK="1")
    return child


def install(selected: Layout, base: Path, role: str, checkout: Checkout) -> dict:
    """Create the environment and fill it only through the reviewed installer."""
    environment = selected.environment
    subprocess.run([str(base), "-I", "-m", "venv", "--clear", str(environment)], check=True)
    # Mark the environment as helper-owned before anything can fail, so an
    # interrupted run is provisioned again instead of reported as unmanaged.
    write_stamp(environment, {"schema": SCHEMA, "role": role, "state": "incomplete"})
    build_root = Path(tempfile.mkdtemp(prefix=f".build-{role}-", dir=selected.store))
    child = installer_environment(checkout)
    command = [str(environment / VENV_PYTHON), "-P", str(checkout.framework / INSTALLER),
               "--build-root", str(build_root)]
    if role == "framework":
        command += ["--framework-lock", (FRAMEWORK_DEFAULT / "requirements-ci.lock").as_posix()]
    if subprocess.run(command, cwd=checkout.connector, env=child, check=False).returncode:
        raise RuntimeError(f"reviewed installer failed; build logs kept in {build_root}")
    receipts = sorted(build_root.glob("ci-dependency-build-*/receipt.json"))
    if len(receipts) != 1:
        raise RuntimeError(f"installer receipt missing; build logs kept in {build_root}")
    receipt = json.loads(receipts[0].read_text(encoding="utf-8"))
    checked = subprocess.run([str(environment / VENV_PYTHON), "-I", "-m", "pip", "check"],
                             env=child, check=False)
    if checked.returncode:
        raise RuntimeError(f"pip check failed; build logs kept in {build_root}")
    try:
        shutil.rmtree(build_root)
    except OSError as error:
        # The environment is complete; a leftover external build directory is
        # reported for cleanup but does not fail the provisioning.
        say(f"could not remove the build directory {build_root}: {error}")
    return receipt


def write_stamp(environment: Path, stamp: dict) -> None:
    partial = environment / f".{STAMP}.tmp"
    try:
        partial.write_text(json.dumps(stamp, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(partial, environment / STAMP)
    except OSError as error:
        raise RuntimeError(f"cannot write the environment stamp in {environment}: "
                           f"{error}") from error


def provision(selected: Layout, base: Path, role: str, version: str, key: str,
              inputs: dict[str, str], checkout: Checkout) -> None:
    environment = selected.environment
    if (selected.store is None and environment.is_dir() and not read_stamp(environment)
            and any(environment.iterdir())):
        raise Blocked(f"{environment} is an unmanaged environment; {UNMANAGED_HINT}")
    say(f"provisioning {role} environment for Python {version} "
        f"(identity {key[:12]}) at {environment}")
    receipt = install(selected, base, role, checkout)
    observed = probe(environment / VENV_PYTHON)
    if not observed or observed.get("version") != version or not observed.get("virtual"):
        raise RuntimeError(f"provisioned environment failed its probe: {environment}")
    framework_revision = subprocess.run(
        ["git", "-C", str(checkout.framework), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=False).stdout.strip()
    created = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    write_stamp(environment, {"schema": SCHEMA, "role": role, "key": key, "python": version,
                              "base": str(base), "inputs": inputs,
                              "framework_revision": framework_revision,
                              "created_utc": created, "receipt": receipt, "probe": observed})
    if selected.alias is not None:
        replace_link(selected.alias, environment, selected.store)
    say(f"{role} environment ready: {environment}")


def ensure(role: str, explicit_base: str | None, verbose: bool) -> Path:
    checkout = checkout_roots()
    if role == "framework" and (checkout.framework.resolve()
                                != (checkout.connector / FRAMEWORK_DEFAULT).resolve()):
        raise Blocked("the framework environment validates the default Framework gitlink path")
    version = required_version(checkout.connector)
    base = select_base(version, explicit_base)
    key, inputs = identity(role, version, base, checkout)
    selected = layout(role, version, key, checkout.connector)
    if is_current(selected.environment, key) and linked(selected):
        if verbose:
            say(f"{role} environment current: {selected.environment}")
        return selected.environment

    lock_directory = selected.store or checkout.connector
    lock_directory.mkdir(mode=0o755, parents=True, exist_ok=True)
    descriptor = os.open(lock_directory, os.O_RDONLY)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        if not is_current(selected.environment, key):
            provision(selected, base, role, version, key, inputs, checkout)
        if selected.store is not None and selected.link is not None:
            replace_link(selected.link, selected.environment, selected.store, checkout=True)
        if selected.alias is not None and not selected.alias.exists():
            replace_link(selected.alias, selected.environment, selected.store)
    finally:
        os.close(descriptor)
    return selected.environment


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--role", choices=("parent", "framework"), default="parent")
    parser.add_argument("--base", help=f"interpreter with the exact {VERSION_FILE}")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    try:
        ensure(args.role, args.base, args.verbose)
    except Blocked as error:
        print(f"BLOCKED: python-env: {error}", file=sys.stderr)
        return BLOCKED
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as error:
        print(f"FAIL: python-env: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
