"""Skeleton runner core for connector tests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from adapter_interface import ConnectorAdapter


@dataclass
class RunnerResult:
    response: Any
    artifacts: Mapping[str, Any]


class RunnerCore:
    """Minimal orchestration around a connector adapter."""

    def __init__(self, adapter: ConnectorAdapter) -> None:
        self.adapter = adapter

    def run_case(self, case: Mapping[str, Any]) -> RunnerResult:
        self.adapter.prepare()
        try:
            self.adapter.apply_config(case.get("config", {}))
            self.adapter.apply_rules(str(case.get("rules", "")))
            self.adapter.start()
            response = self.adapter.send_request(case.get("request", {}))
            artifacts = self.adapter.collect_artifacts()
            return RunnerResult(response=response, artifacts=artifacts)
        finally:
            self.adapter.stop()
            self.adapter.cleanup()
