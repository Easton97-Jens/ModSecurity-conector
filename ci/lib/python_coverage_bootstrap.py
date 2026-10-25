"""Trace selected-interpreter Python children without changing their isolation.

The returned environment belongs only to an admitted test execution. Isolated
interpreters, stripped environments, other prefixes/UIDs and killed children
may produce no record; instrumentation never changes those boundaries.
"""
from __future__ import annotations

import atexit
import hashlib
from importlib.machinery import PathFinder
import json
import os
from pathlib import Path
import re
import secrets
import stat
import sys
import threading
import trace
from typing import Any


BOOTSTRAP_MARKER = "# Parent active coverage bootstrap v1\n"
MAX_MODULE_BYTES = 256 * 1024
EXECUTION_ID = re.compile(r"[a-z][a-z0-9_.-]{0,127}", re.ASCII)
BASE_TEST_PATTERNS = ("tests/**", "**/test_*.py", "**/*_test.py")


class BootstrapError(ValueError):
    """A private, selected-interpreter coverage bootstrap cannot be prepared."""


def _directory(path: Path, *, private: bool = False) -> Path:
    path = Path(path)
    if (not path.is_absolute() or path == Path(path.anchor) or ".." in path.parts
            or any(character in str(path) for character in ("\x00", "\r", "\n", os.pathsep))):
        raise BootstrapError("coverage bootstrap paths must be canonical absolute paths")
    current_uid = os.geteuid()
    for component in [*reversed(path.parents), path]:
        observed = component.lstat()
        if not stat.S_ISDIR(observed.st_mode) or observed.st_uid not in (0, current_uid):
            raise BootstrapError("coverage bootstrap ancestry must contain trusted ordinary directories")
        sticky_ancestor = (component != path and observed.st_uid == 0
                           and bool(observed.st_mode & stat.S_ISVTX))
        if observed.st_mode & 0o022 and not sticky_ancestor:
            raise BootstrapError("coverage bootstrap ancestry must not be replaceable by other users")
    if path.resolve(strict=True) != path:
        raise BootstrapError("coverage bootstrap paths must not contain symbolic links")
    if private and (path.stat().st_uid != current_uid or stat.S_IMODE(path.stat().st_mode) != 0o700):
        raise BootstrapError("coverage bootstrap output must be current-user private mode 0700")
    return path


def _regular_bytes(path: Path) -> bytes:
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(descriptor, "rb") as source:
        details = os.fstat(source.fileno())
        if (not stat.S_ISREG(details.st_mode) or details.st_nlink != 1
                or details.st_size > MAX_MODULE_BYTES or details.st_mode & 0o022):
            raise BootstrapError("coverage bootstrap code must be a bounded ordinary non-writable input")
        data = source.read(MAX_MODULE_BYTES + 1)
    if len(data) > MAX_MODULE_BYTES:
        raise BootstrapError("coverage bootstrap code exceeds its bound")
    return data


def _own_sitecustomize(path: str | None, module_digest: str) -> bool:
    if not path:
        return False
    try:
        data = _regular_bytes(Path(path))
    except (OSError, BootstrapError):
        return False
    prefix = BOOTSTRAP_MARKER + "# module-sha256: " + module_digest + "\n"
    return data.startswith(prefix.encode("utf-8"))


def _check_existing_sitecustomize(module_digest: str) -> None:
    loaded = sys.modules.get("sitecustomize")
    if loaded is not None and not _own_sitecustomize(getattr(loaded, "__file__", None), module_digest):
        raise BootstrapError("coverage cannot replace an existing non-project sitecustomize")
    # Include the inherited PYTHONPATH even if a caller changed it after startup.
    search = [*os.environ.get("PYTHONPATH", "").split(os.pathsep), *sys.path]
    specification = PathFinder.find_spec("sitecustomize", search)
    if specification is not None and not _own_sitecustomize(specification.origin, module_digest):
        raise BootstrapError("coverage cannot shadow an existing non-project sitecustomize")


def _write_fresh(path: Path, data: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(descriptor, "wb") as output:
        output.write(data)


def _sitecustomize_source(configuration: dict[str, Any], module_digest: str) -> str:
    # Read/compile the fixed module instead of importing it through the project
    # package or writing bytecode into the source checkout. CLI arguments and
    # sys.path are never reassigned by this hook.
    return (BOOTSTRAP_MARKER + "# module-sha256: " + module_digest + "\n" +
            "import os as _coverage_os\nimport sys as _coverage_sys\n" +
            "_coverage_configuration = " + repr(configuration) + "\n" +
            "if (_coverage_os.geteuid() == _coverage_configuration['uid'] and\n"
            "        _coverage_os.path.realpath(_coverage_sys.prefix) == _coverage_configuration['python_prefix']):\n"
            "    import hashlib as _coverage_hashlib\n"
            "    from types import ModuleType as _CoverageModule\n"
            "    _coverage_filename = _coverage_configuration['module_file']\n"
            "    _coverage_descriptor = _coverage_os.open(_coverage_filename, _coverage_os.O_RDONLY | _coverage_os.O_NOFOLLOW | _coverage_os.O_NONBLOCK)\n"
            "    with _coverage_os.fdopen(_coverage_descriptor, 'rb') as _coverage_input:\n"
            "        _coverage_bytes = _coverage_input.read(262145)\n"
            "    if _coverage_hashlib.sha256(_coverage_bytes).hexdigest() != " + repr(module_digest) + ":\n"
            "        raise RuntimeError('selected Python coverage bootstrap source changed')\n"
            "    _coverage_module = _CoverageModule('_parent_active_coverage_bootstrap')\n"
            "    _coverage_module.__file__ = _coverage_filename\n"
            "    exec(compile(_coverage_bytes, _coverage_filename, 'exec', dont_inherit=True), _coverage_module.__dict__)\n"
            "    _coverage_module.start_recording(_coverage_configuration)\n")


def provision_bootstrap(directory: Path, source_root: Path, execution_id: str,
                        python_prefix: Path = Path(sys.prefix), uid: int = os.geteuid(),
                        test_patterns: tuple[str, ...] = ()) -> dict[str, str]:
    """Return a child-only PYTHONPATH overlay and create private recording paths.

    ``directory/python-subprocess/*.json`` contains successful clean-exit
    records. Existing project hooks may be replaced for a nested fixture child;
    non-project sitecustomize hooks are rejected instead of silently shadowed.
    """
    directory = _directory(directory, private=True)
    source_root = _directory(source_root)
    if directory == source_root or source_root in directory.parents:
        raise BootstrapError("coverage bootstrap output must stay outside the measured source")
    if EXECUTION_ID.fullmatch(execution_id) is None or type(uid) is not int or uid < 0:
        raise BootstrapError("coverage bootstrap requires a fixed execution ID and UID")
    prefix = Path(python_prefix).resolve(strict=True)
    if not prefix.is_absolute() or not prefix.is_dir():
        raise BootstrapError("coverage bootstrap requires an existing selected interpreter prefix")
    if not isinstance(test_patterns, (tuple, list)) or any(not isinstance(value, str) for value in test_patterns):
        raise BootstrapError("coverage bootstrap test patterns must be explicit strings")
    module_file = Path(__file__).resolve(strict=True)
    module_digest = hashlib.sha256(_regular_bytes(module_file)).hexdigest()
    _check_existing_sitecustomize(module_digest)
    bootstrap = directory / "python-bootstrap"
    records = directory / "python-subprocess"
    bootstrap.mkdir(mode=0o700)
    records.mkdir(mode=0o700)
    _directory(bootstrap, private=True)
    _directory(records, private=True)
    configuration = {"source_root": str(source_root), "execution_id": execution_id,
                     "python_prefix": str(prefix), "uid": uid, "records": str(records),
                     "module_file": str(module_file), "test_patterns": list(test_patterns)}
    _write_fresh(bootstrap / "sitecustomize.py", _sitecustomize_source(configuration, module_digest).encode("utf-8"))
    inherited = os.environ.get("PYTHONPATH")
    value = str(bootstrap) if inherited is None else str(bootstrap) + os.pathsep + inherited
    return {"PYTHONPATH": value}


def _pattern(pattern: str) -> re.Pattern[str]:
    # Match the supplied Sonar contract: leading **/ also matches zero folders.
    expression = re.escape(pattern).replace(r"\*\*/", r"(?:.*/)?")
    expression = expression.replace(r"\*\*", ".*").replace(r"\*", "[^/]*")
    return re.compile(expression)


class _Recorder:
    def __init__(self, configuration: dict[str, Any]):
        self.root = Path(configuration["source_root"])
        self.records = _directory(Path(configuration["records"]), private=True)
        self.target = configuration["execution_id"] + ":subprocess"
        self.uid = configuration["uid"]
        self.prefix = sys.prefix
        self.module_file = Path(configuration["module_file"])
        self.patterns = tuple(_pattern(value) for value in (*BASE_TEST_PATTERNS, *configuration["test_patterns"]))
        self.cache: dict[str, str | None] = {}
        self.tracer = trace.Trace(count=True, trace=False)
        self.lock = threading.Lock()
        self.enabled = True

    def _relative_source(self, filename: str) -> str | None:
        if filename not in self.cache:
            path = Path(filename)
            relative = None
            if path.is_absolute() and path.suffix == ".py" and path.is_relative_to(self.root):
                candidate = path.relative_to(self.root).as_posix()
                try:
                    ordinary = path.is_file() and path.resolve(strict=False) == path
                except (OSError, ValueError):
                    ordinary = False
                if (ordinary and path != self.module_file
                        and candidate.split("/", 1)[0] not in {"modules", ".codex"}
                        and not any(pattern.fullmatch(candidate) for pattern in self.patterns)):
                    relative = candidate
            self.cache[filename] = relative
        return self.cache[filename]

    def _selected_identity(self) -> bool:
        return self.enabled and os.geteuid() == self.uid and sys.prefix == self.prefix

    def global_trace(self, frame, _event, _argument):
        if self._selected_identity() and self._relative_source(frame.f_code.co_filename) is not None:
            return self.local_trace
        return None

    def local_trace(self, frame, event, argument):
        if not self._selected_identity():
            return None
        with self.lock:
            self.tracer.localtrace_count(frame, event, argument)
        return self.local_trace

    def finish(self) -> None:
        self.enabled = False
        if os.geteuid() != self.uid or sys.prefix != self.prefix:
            return
        if sys.gettrace() == self.global_trace:
            sys.settrace(None)
        if threading.gettrace() == self.global_trace:
            threading.settrace(None)
        with self.lock:
            counts = dict(self.tracer.results().counts)
        files: dict[str, dict[str, int]] = {}
        for (filename, line), count in counts.items():
            relative = self._relative_source(filename)
            if relative is not None and line > 0 and count > 0:
                files.setdefault(relative, {})[str(line)] = count
        document = {"schema_version": 1, "target": self.target, "files": files}
        _directory(self.records, private=True)
        filename = f"{os.getpid()}-{secrets.token_hex(16)}.json"
        _write_fresh(self.records / filename, (json.dumps(document, sort_keys=True) + "\n").encode("utf-8"))


def start_recording(configuration: dict[str, Any]) -> None:
    """Start only after the generated hook has checked prefix and effective UID."""
    if sys.gettrace() is not None or threading.gettrace() is not None:
        raise BootstrapError("selected Python child already has a trace hook")
    recorder = _Recorder(configuration)
    atexit.register(recorder.finish)
    threading.settrace(recorder.global_trace)
    sys.settrace(recorder.global_trace)
