"""Filesystem boundaries for task-owned Apache inputs and private outputs."""

import os
from pathlib import Path
import stat


def storage_root():
    """Use the configured external storage, rejecting substitutions and unsafe parents."""
    root = Path(os.environ["CODEX_TEMP_ROOT"])
    if not root.is_absolute() or root.resolve(strict=True) != root:
        raise ValueError("Configured storage must be an existing canonical absolute directory")
    for parent in (root, *root.parents):
        item = parent.stat()
        if not stat.S_ISDIR(item.st_mode) or item.st_uid not in (0, os.geteuid()):
            raise ValueError("Storage ancestry has an unexpected owner or object type")
        if item.st_mode & 0o022 and not (item.st_uid == 0 and item.st_mode & stat.S_ISVTX):
            raise ValueError("Storage ancestry permits untrusted replacement")
    return root


def input_path(value):
    """CLI inputs may read regular files only within the repository or configured storage."""
    supplied = Path(value).absolute()
    resolved = supplied.resolve(strict=True)
    repository = Path(__file__).resolve().parents[4]
    if supplied != resolved or not any(resolved.is_relative_to(root) for root in (storage_root(), repository)):
        raise ValueError("Input escapes the authorized Apache evidence roots or follows a symlink")
    if not resolved.is_file():
        raise ValueError("Expected a regular evidence input")
    return resolved


def new_output(value):
    """Create-new callers may write only beneath configured external storage."""
    path = Path(value).absolute()
    root = storage_root()
    if not path.is_relative_to(root) or path == root or path.resolve() != path:
        raise ValueError("Output escapes configured storage or follows a symlink")
    for parent in path.parents:
        if parent.exists():
            item = parent.stat()
            if item.st_uid not in (0, os.geteuid()) or item.st_mode & 0o022:
                raise ValueError('Output ancestry permits an untrusted writer')
        if parent == root:
            break
    return path


def private_directory(value):
    """Create one nonshared runtime directory without accepting existing objects."""
    path = new_output(value)
    path.mkdir(mode=0o700)
    return path


def fixture_path(value):
    """Select a regular fixture below the controller's read-only fixture mount."""
    root = Path('/mnt/fixtures')
    relative = Path(value)
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError('Fixture selector must be relative and cannot traverse parents')
    path = root / relative
    if path.resolve(strict=True) != path or not path.is_file():
        raise ValueError('Fixture selector must name a regular nonsymlink fixture')
    return path
