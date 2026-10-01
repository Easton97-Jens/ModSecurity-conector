#!/usr/bin/env python3
"""Run one connector stage with short, invocation-owned Unix socket paths."""
from __future__ import annotations

import os
from pathlib import Path
import signal
import shutil
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from runtime_path_utils import ensure_safe_runtime_directory, is_safe_runtime_parent


def live_group_members(group: int) -> list[int]:
    """Inspect Linux process states; unreaped zombies cannot use the socket."""
    members = []
    for entry in Path("/proc").iterdir():
        if not entry.name.isdecimal():
            continue
        try:
            record = (entry / "stat").read_text()
            fields = record[record.rfind(")") + 2:].split()
            if int(fields[2]) == group and fields[0] not in {"Z", "X"}:
                members.append(int(entry.name))
        except (FileNotFoundError, ProcessLookupError, PermissionError):
            continue
    return members


def stop_group(group: int) -> bool:
    remaining = bool(live_group_members(group))
    for signum in (signal.SIGTERM, signal.SIGKILL):
        if not live_group_members(group):
            return remaining
        try:
            os.killpg(group, signum)
        except ProcessLookupError:
            return remaining
        deadline = time.monotonic() + 2
        while live_group_members(group) and time.monotonic() < deadline:
            time.sleep(0.02)
    if live_group_members(group):
        raise RuntimeError("connector stage process group did not terminate; socket root retained")
    return remaining


def run(command: list[str]) -> int:
    selected = os.environ.get("RUNNER_TEMP") or os.environ.get("TMPDIR")
    if not selected:
        raise ValueError("RUNNER_TEMP or TMPDIR must select a trusted socket parent")
    parent = Path(selected)
    if not parent.is_absolute() or not parent.is_dir() or not is_safe_runtime_parent(parent):
        raise ValueError("socket parent must be an existing safe absolute directory")
    ensure_safe_runtime_directory(parent)
    if len(os.fsencode(parent / "mcs.12345678" / "traefik-forwardauth-companion.sock")) >= 108:
        raise ValueError("configured socket parent is too long for Unix sockets")
    root = Path(tempfile.mkdtemp(prefix="mcs.", dir=parent))
    safe_to_remove = True
    try:
        ensure_safe_runtime_directory(root)
        environment = dict(os.environ, MSCONNECTOR_PRIVATE_SOCKET_ROOT=str(root))
        child: subprocess.Popen[bytes] | None = None
        pending_signals: list[int] = []
        previous = {}

        def forward(signum: int, _frame: object) -> None:
            # Include intermediate make/shell processes and their services.
            # Keep the directory until the stage and its process group exit.
            if child is None:
                pending_signals.append(signum)
            else:
                try:
                    os.killpg(child.pid, signum)
                except ProcessLookupError:
                    pass

        try:
            for signum in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
                previous[signum] = signal.signal(signum, forward)
            child = subprocess.Popen(command, env=environment, start_new_session=True)
            for signum in pending_signals:
                forward(signum, None)
            status = child.wait()
        finally:
            try:
                if child is not None:
                    safe_to_remove = False
                    lingering = stop_group(child.pid)
                    child.wait()
                    safe_to_remove = True
            except (OSError, ValueError, RuntimeError):
                print(f"retained private socket root: {root}", file=sys.stderr)
                raise
            finally:
                for signum, handler in previous.items():
                    signal.signal(signum, handler)
        if lingering and status == 0:
            print("FAIL: connector stage left live processes after exit", file=sys.stderr)
            return 1
        return status if status >= 0 else 128 - status
    finally:
        if safe_to_remove:
            shutil.rmtree(root)


if __name__ == "__main__":
    try:
        if not sys.argv[1:]:
            raise ValueError("a connector stage command is required")
        sys.exit(run(sys.argv[1:]))
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"FAIL: private socket stage: {exc}", file=sys.stderr)
        sys.exit(1)
