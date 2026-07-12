#!/usr/bin/env python3
"""Validate parser-backed connector configuration documentation.

The checker intentionally uses the same connector-specific extractors as the
generator: Apache ``command_rec``, NGINX ``ngx_command_t``, HAProxy's native
HTX keyword parser, Envoy YAML/Go JSON/CLI contracts, Traefik YAML/plugin
configuration, lighttpd ``config_plugin_values_init``, the Common Runtime
branch parser, and directives actually used by example rule files.  It is not
a free-text grep check.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent / "Makefile").is_file())
sys.path.insert(0, str(Path(__file__).resolve().parent))

from connector_config_reference import (  # noqa: E402
    CONNECTORS,
    build_inventory,
    documented_path,
    german_translation_errors,
    inventory_json,
    rendered_files,
)


REQUIRED_INVENTORY_FIELDS = frozenset({
    "connector",
    "name",
    "configuration_layer",
    "source_file",
    "source_symbol",
    "implemented",
    "selected_integration_mode",
    "documented_in",
    "german_documented_in",
    "syntax",
    "value_type",
    "allowed_values",
    "default",
    "default_source",
    "required",
    "contexts",
    "inheritance",
    "merge_behavior",
    "validation",
    "phase_relevance",
    "security_relevance",
    "runtime_effect",
    "example_file",
    "compatibility_only",
    "deprecated",
    "description",
})


def option_sections(text: str) -> set[str]:
    result: set[str] = set()
    for line in text.splitlines():
        if line.startswith("## `") and line.endswith("`"):
            result.add(line[4:-1])
    return result


def required_top_table(text: str) -> bool:
    return "| Option | Layer | Type | Required | Default | Context | Short description |" in text


def profile_layout_errors(root: Path) -> list[str]:
    """Check the committed minimal/safe/strict/detection/disabled examples.

    Host binaries validate materialized host configuration through the existing
    ``check-config-*`` targets.  This static gate additionally prevents the
    documentation tree from advertising a missing or unclassified profile.
    """
    required = {
        "apache": ("minimal/httpd.conf", "safe/httpd.conf", "strict/README.md", "detection-only/httpd.conf", "disabled/httpd.conf", "rules/detection-only.conf", "rules/engine-off.conf"),
        "nginx": ("minimal/nginx.conf", "safe/nginx.conf", "strict/nginx.conf", "detection-only/nginx.conf", "disabled/nginx.conf", "rules/detection-only.conf", "rules/engine-off.conf"),
        "haproxy": ("minimal/haproxy-htx.cfg", "safe/haproxy-htx.cfg", "strict/README.md", "detection-only/haproxy-htx.cfg", "disabled/haproxy-htx.cfg", "rules/detection-only.conf", "rules/engine-off.conf"),
        "envoy": ("minimal/envoy-ext-proc-streaming.yaml.in", "minimal/envoy-ext-proc-service.json", "minimal/msconnector-runtime.conf", "safe/envoy-ext-proc-streaming.yaml.in", "safe/envoy-ext-proc-service.json", "strict/README.md", "detection-only/msconnector-runtime.conf", "disabled/msconnector-runtime.conf", "rules/detection-only.conf", "rules/engine-off.conf"),
        "traefik": ("minimal/traefik-static.yaml", "minimal/traefik-dynamic.yaml", "minimal/traefik-engine-service.conf", "safe/traefik-dynamic.yaml", "safe/traefik-engine-service.conf", "strict/README.md", "detection-only/traefik-engine-service.conf", "disabled/traefik-engine-service.conf", "rules/detection-only.conf", "rules/engine-off.conf"),
        "lighttpd": ("minimal/lighttpd.conf", "minimal/msconnector-runtime.conf", "safe/lighttpd-http1-identity.conf", "safe/msconnector-runtime.conf", "strict/README.md", "detection-only/msconnector-runtime.conf", "disabled/lighttpd.conf", "rules/detection-only.conf", "rules/engine-off.conf"),
    }
    errors: list[str] = []
    for connector, files in required.items():
        base = root / "examples" / connector
        for relative in files:
            if not (base / relative).is_file():
                errors.append(f"examples/{connector}/{relative}: required profile file is missing")
        detection = base / "rules" / "detection-only.conf"
        disabled = base / "rules" / "engine-off.conf"
        if detection.is_file() and "SecRuleEngine DetectionOnly" not in detection.read_text(encoding="utf-8"):
            errors.append(f"{detection.relative_to(root)}: missing SecRuleEngine DetectionOnly")
        if disabled.is_file() and "SecRuleEngine Off" not in disabled.read_text(encoding="utf-8"):
            errors.append(f"{disabled.relative_to(root)}: missing SecRuleEngine Off")
    local_path = re.compile(r"/(?:root/(?:git|conecter)|srv/modsecurity-work)(?:/|\b)")
    for path in (root / "examples").rglob("*"):
        if path.is_file() and path.suffix in {".md", ".conf", ".cfg", ".yaml", ".in", ".json"}:
            if local_path.search(path.read_text(encoding="utf-8", errors="replace")):
                errors.append(f"{path.relative_to(root)}: contains a local development path")
    return errors


def german_prose_errors(text: str) -> list[str]:
    """Catch stale English renderer boilerplate outside explicit source blocks.

    YAML fallback sections deliberately retain original source metadata in a
    ``text`` fence so concrete protocol/default information is not lost.  The
    surrounding German explanation must nevertheless not regress to an old
    English heading, table label, code comment, or combination result.
    """
    markers = (
        "## Scope and source of truth",
        "Compatibility-Einträge",
        "[Common Runtime configuration]",
        "[ModSecurity Engine directives]",
        "[Rule examples]",
        "| Type | Allowed values | Required |",
        "| Profile | File | Status |",
        "| Connector | Engine | Request body | Response body | Result |",
        "No connector transaction; engine setting is not reached.",
        "Repository-Targets:",
        "See [",
        "# Enforce an eligible pre-commit deny.",
        "# Match and log without a disruptive action.",
        "# Do not evaluate rules after they are loaded.",
        "Source:",
        "Merge:",
    )
    errors: list[str] = []
    in_fence = False
    for number, line in enumerate(text.splitlines(), 1):
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for marker in markers:
            if marker in line:
                errors.append(f"line {number}: untranslated renderer marker {marker!r}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    root = args.repo_root.resolve()
    errors: list[str] = []
    try:
        inventory = build_inventory(root)
        rendered = rendered_files(root)
    except (OSError, ValueError) as error:
        print(f"connector config reference: FAIL: {error}", file=sys.stderr)
        return 2

    inventory_path = root / "reports/connector-configuration-inventory.json"
    expected_json = inventory_json(root)
    errors.extend(profile_layout_errors(root))
    errors.extend(german_translation_errors(inventory))
    if not inventory_path.is_file() or inventory_path.read_text(encoding="utf-8") != expected_json:
        errors.append("reports/connector-configuration-inventory.json is stale or missing")
    names_by_doc: dict[str, set[str]] = {}
    for option in inventory:
        missing_fields = REQUIRED_INVENTORY_FIELDS - option.keys()
        if missing_fields:
            errors.append(
                f"{option.get('connector', '<unknown>')}:{option.get('name', '<unknown>')}: "
                f"inventory fields missing: {', '.join(sorted(missing_fields))}"
            )
            continue
        names_by_doc.setdefault(option["documented_in"], set()).add(option["name"])
        names_by_doc.setdefault(option["german_documented_in"], set()).add(option["name"])
        if option["compatibility_only"] and option["configuration_layer"] != "compatibility":
            errors.append(f"{option['connector']}:{option['name']}: compatibility option has wrong layer")
        if option["value_type"] == "historical configuration" and option["implemented"]:
            errors.append(f"{option['connector']}:{option['name']}: historical material must not be marked implemented")
    for path, expected in rendered.items():
        relative = path.relative_to(root).as_posix()
        if not path.is_file():
            errors.append(f"{relative}: missing generated reference")
            continue
        actual = path.read_text(encoding="utf-8")
        if actual != expected:
            errors.append(f"{relative}: generated content differs from source-backed renderer")
        if relative.endswith(".de.md"):
            errors.extend(f"{relative}: {error}" for error in german_prose_errors(actual))
        if path.name.startswith("configuration-reference") or path.name in {"common-connector-configuration.md", "common-connector-configuration.de.md", "modsecurity-directives.md", "modsecurity-directives.de.md"}:
            if not required_top_table(actual):
                errors.append(f"{relative}: missing required top inventory table")
        expected_names = names_by_doc.get(relative, set())
        missing = expected_names - option_sections(actual)
        if missing:
            errors.append(f"{relative}: missing option sections: {', '.join(sorted(missing))}")
    # Technical bilingual parity is checked on the rendered structured content:
    # every documented option section and all source-derived values are emitted
    # from the same inventory in both companions.
    for connector in CONNECTORS:
        english = root / documented_path(connector, False)
        german = root / documented_path(connector, True)
        if english.is_file() and german.is_file():
            if option_sections(english.read_text(encoding="utf-8")) != option_sections(german.read_text(encoding="utf-8")):
                errors.append(f"{connector}: English/German option-section parity differs")
    for connector, filename in (("common", "common-connector-configuration"), ("engine", "modsecurity-directives")):
        english = root / f"examples/common/{filename}.md"
        german = root / f"examples/common/{filename}.de.md"
        if english.is_file() and german.is_file() and option_sections(english.read_text(encoding="utf-8")) != option_sections(german.read_text(encoding="utf-8")):
            errors.append(f"{connector}: English/German option-section parity differs")
    # The JSON remains easy to consume by external tooling, not just this
    # checker.  Reparse it after exact-content validation for schema sanity.
    try:
        payload = json.loads(expected_json)
        if payload.get("schema_version") != 1 or not isinstance(payload.get("options"), list):
            errors.append("inventory JSON schema_version/options shape is invalid")
    except json.JSONDecodeError as error:
        errors.append(f"inventory JSON failed to parse: {error}")
    if errors:
        print("connector config reference: FAIL", file=sys.stderr)
        print("\n".join(sorted(errors)), file=sys.stderr)
        return 1
    counts = {connector: sum(option["connector"] == connector for option in inventory) for connector in (*CONNECTORS, "common", "engine")}
    print("connector config reference: PASS " + ", ".join(f"{name}={count}" for name, count in counts.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
