#!/usr/bin/env python3
"""Generate lightweight common SDK documentation placeholders."""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "generated"

FILES = {
    "common-sdk.md": "**Language:** English | [Deutsch](common-sdk.de.md)\n\n# Common SDK generated overview\n\nConnector-neutral common SDK metadata; no connector runtime integration is claimed.\n",
    "common-sdk.de.md": "**Sprache:** [English](common-sdk.md) | Deutsch\n\n# Generierter Überblick zum Common SDK\n\nConnector-neutrale Common-SDK-Metadaten; es wird keine Connector-Laufzeitintegration behauptet.\n",
    "directives.md": "**Language:** English | [Deutsch](directives.de.md)\n\n# Common directives\n\nGenerated directive inventory for common scaffolding only.\n",
    "directives.de.md": "**Sprache:** [English](directives.md) | Deutsch\n\n# Common-Direktiven\n\nGeneriertes Direktiveninventar nur für Common-Scaffolding.\n",
    "capabilities.md": "**Language:** English | [Deutsch](capabilities.de.md)\n\n# Capability contract\n\n- phase4-hard-abort -> phase4 hard-abort-after-200 event test\n",
    "capabilities.de.md": "**Sprache:** [English](capabilities.md) | Deutsch\n\n# Fähigkeitsvertrag\n\n- phase4-hard-abort -> Phase-4-Hard-Abort-nach-200-Ereignistest\n",
}


def main() -> int:
    DOCS.mkdir(parents=True, exist_ok=True)
    for name, text in FILES.items():
        (DOCS / name).write_text(text, encoding="utf-8")
    print("generated common docs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
