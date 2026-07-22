"""Shared offline fixtures and spec-loader support for version updater tests."""

from __future__ import annotations

import importlib.util
import sys
from functools import partial
from pathlib import Path
from typing import Callable


SCRIPTS_DIRECTORY = Path(__file__).resolve().parents[1] / "scripts"


def load_updater(module_name: str, script: Path) -> object:
    """Spec-load a hyphenated updater while making its sibling core importable."""

    spec = importlib.util.spec_from_file_location(module_name, script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {script}")
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(SCRIPTS_DIRECTORY))
    try:
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
    finally:
        del sys.path[0]
    return module


class FakeResponse:
    """Small response double with explicit metadata headers and a trusted URL."""

    def __init__(
        self,
        body: bytes,
        *,
        canonical_url: str,
        content_type: str | None = "application/json; charset=utf-8",
        content_length: int | None = None,
        url: str | None = None,
        status: int = 200,
    ) -> None:
        self.body = body
        self.status = status
        self.url = canonical_url if url is None else url
        self.headers: dict[str, str] = {}
        if content_type is not None:
            self.headers["Content-Type"] = content_type
        self.headers["Content-Length"] = str(len(body) if content_length is None else content_length)
        self.closed = False

    def read(self, size: int = -1) -> bytes:
        return self.body if size < 0 else self.body[:size]

    def geturl(self) -> str:
        return self.url

    def getcode(self) -> int:
        return self.status

    def close(self) -> None:
        self.closed = True


class FakeOpener:
    """Record requests while returning one controlled response or controlled error."""

    def __init__(self, response: FakeResponse | None = None, error: Exception | None = None) -> None:
        self.response = response
        self.error = error
        self.requests = []

    def open(self, request, timeout):
        self.requests.append((request, timeout))
        if self.error is not None:
            raise self.error
        if self.response is None:
            raise AssertionError("FakeOpener needs a response or an error")
        return self.response


def response_factory(canonical_url: str) -> Callable[..., FakeResponse]:
    """Bind one adapter's canonical endpoint into the shared response fixture."""

    return partial(FakeResponse, canonical_url=canonical_url)


def uses_shared_core(module: object) -> bool:
    """Confirm that a spec-loaded adapter resolves the sibling shared core."""

    return (
        getattr(getattr(module, "_decode_metadata", None), "__module__", None)
        == "version_updater_common"
        and getattr(getattr(module, "_RUNTIME", None).__class__, "__module__", None)
        == "version_updater_common"
    )
