#!/usr/bin/env python3
"""Generate paired current connector guides from the selected core contracts."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKER = "<!-- Generated from scripts/generate_connector_guides.py; do not edit directly. -->"
REQUIRED_CANONICAL_RULE_RUNS = "Required for canonical rule runs"
ABSOLUTE_RULES_FILE_PATH = "absolute rules-file path"
MAKE_DEFAULT_OR_CALLER = "Make default or caller"
NO_CRS_RULES_FILE = "`/etc/modsecurity/no-crs-baseline.conf`"
PROVISIONING_OR_CALLER = "Provisioning or caller"
FRAMEWORK_PROVIDER_PIN_OR_CALLER = "Framework/provider pin or caller"
ABSOLUTE_BUILD_DIRECTORY = "absolute build directory"
DOCUMENT_KINDS = (
    "README",
    "architecture",
    "build",
    "configuration",
    "lifecycle",
    "testing",
    "operations",
    "limitations",
)
DOCUMENT_TITLES = {
    "README": ("{name} Connector", "{name}-Connector"),
    "architecture": ("{name} architecture", "{name}-Architektur"),
    "build": ("{name} build", "{name}-Build"),
    "configuration": ("{name} configuration", "{name}-Konfiguration"),
    "lifecycle": ("{name} lifecycle", "{name}-Lifecycle"),
    "testing": ("{name} testing", "{name}-Tests"),
    "operations": ("{name} operations", "{name}-Betrieb"),
    "limitations": ("{name} limitations", "{name}-Grenzen"),
}
GERMAN_LABEL_REPLACEMENTS = {
    "## Host integration": "## Hostintegration",
    "## Data flow": "## Datenfluss",
    "## Ownership": "## Ownership",
    "## Build path": "## Buildpfad",
    "## Prerequisites": "## Voraussetzungen",
    "## Cache and provenance": "## Cache und Provenienz",
    "## Validation": "## Validierung",
    "## Troubleshooting": "## Fehlerdiagnose",
    "## Configuration model": "## Konfigurationsmodell",
    "## Minimal and Safe examples": "## Minimal- und Safe-Beispiele",
    "## Phases": "## Phasen",
    "## Safe and Strict boundary": "## Safe- und Strict-Grenze",
    "## First byte and buffering": "## First Byte und Buffering",
    "## Levels": "## Ebenen",
    "## No-CRS core rules": "## No-CRS-Kernregeln",
    "## Evidence": "## Evidence",
    "## Statuses": "## Statuswerte",
    "## Start and stop": "## Start und Stop",
    "## Logs and health": "## Logs und Health",
    "## Diagnosis": "## Diagnose",
    "## Updates": "## Updates",
    "## Boundaries": "## Grenzen",
    "## Not covered by this guide": "## Nicht durch diesen Leitfaden abgedeckt",
    "## Compatibility paths": "## Kompatibilitätspfade",
}


CONNECTORS = {
    "apache": {
        "name": "Apache",
        "mode": "native-httpd-module",
        "host": "Apache httpd module built through APXS",
        "host_de": "Apache-httpd-Modul, gebaut über APXS",
        "build": "`make build-apache` prepares the selected host path; `make check-config-apache` performs the configuration check.",
        "build_de": "`make build-apache` bereitet den ausgewählten Hostpfad vor; `make check-config-apache` führt den Konfigurationscheck aus.",
        "config": "Apache directives are registered by the adapter. The documented examples use `modsecurity on`, `modsecurity_rules_file`, and existing bounded Phase-4 controls.",
        "config_de": "Apache-Direktiven werden vom Adapter registriert. Die dokumentierten Beispiele verwenden `modsecurity on`, `modsecurity_rules_file` und vorhandene begrenzte Phase-4-Controls.",
        "variables": [("APXS / APXS_BIN", "Optional", "path to an executable APXS", "Set by the operator or provisioning", "`/usr/bin/apxs`"), ("APACHE_BIN / APACHECTL_BIN", "Optional", "path to httpd/apachectl", "Set by provisioning or operator", "`/usr/sbin/apachectl`"), ("BUILD_HTTPD_FROM_SOURCE", "Optional", "`0` or `1`", "Make caller", "`1`"), ("NO_CRS_RULES_FILE", REQUIRED_CANONICAL_RULE_RUNS, ABSOLUTE_RULES_FILE_PATH, MAKE_DEFAULT_OR_CALLER, NO_CRS_RULES_FILE)],
        "limit": "Strict late behavior is a host-specific boundary; this guide does not promote a universal status rewrite after commitment.",
        "limit_de": "Strict-Late-Verhalten ist eine host-spezifische Grenze; dieser Leitfaden promotet keine universelle Statusumschreibung nach dem Commit.",
    },
    "nginx": {
        "name": "NGINX",
        "mode": "native-nginx-http-module",
        "host": "native NGINX HTTP module",
        "host_de": "natives NGINX-HTTP-Modul",
        "build": "`make build-nginx` prepares the selected host path; `make check-config-nginx` validates generated configuration.",
        "build_de": "`make build-nginx` bereitet den ausgewählten Hostpfad vor; `make check-config-nginx` validiert die erzeugte Konfiguration.",
        "config": "The adapter uses existing NGINX directives such as `modsecurity on` and `modsecurity_rules_file`. The dynamic module, prefix, and phase-4 mode are selected by existing harness variables.",
        "config_de": "Der Adapter verwendet vorhandene NGINX-Direktiven wie `modsecurity on` und `modsecurity_rules_file`. Dynamisches Modul, Prefix und Phase-4-Modus werden über vorhandene Harness-Variablen gewählt.",
        "variables": [("NGINX_PREFIX", "Optional", "absolute generated prefix", PROVISIONING_OR_CALLER, "`/srv/modsecurity-work/nginx-runtime/nginx`"), ("NGINX_BINARY", "Optional", "executable NGINX path", "Derived from `NGINX_PREFIX`", "`<nginx-prefix>/sbin/nginx`"), ("NGINX_MODULE", "Optional", "dynamic module path", "Derived from `NGINX_PREFIX`", "`<nginx-prefix>/modules/ngx_http_modsecurity_module.so`"), ("NGINX_PHASE4_MODE", "Optional", "`minimal`, `safe`, or `strict` where host supports it", "Caller/harness", "`safe`")],
        "limit": "Strict is a separate host capability. The selected evidence documents Safe post-commit semantics without claiming a rewritten response after commitment.",
        "limit_de": "Strict ist eine separate Hostfähigkeit. Die ausgewählte Evidence dokumentiert Safe-Post-Commit-Semantik ohne eine umgeschriebene Response nach dem Commit zu behaupten.",
    },
    "haproxy": {
        "name": "HAProxy",
        "mode": "native-htx-filter",
        "host": "native HAProxy HTX filter with the repository overlay",
        "host_de": "nativer HAProxy-HTX-Filter mit dem Repository-Overlay",
        "build": "`make build-haproxy` prepares the pinned overlay path; `make check-haproxy-htx-overlay` validates the source contract.",
        "build_de": "`make build-haproxy` bereitet den gepinnten Overlay-Pfad vor; `make check-haproxy-htx-overlay` validiert den Source-Vertrag.",
        "config": "The selected full-lifecycle path is the native HTX filter. It is not the historical SPOE/SPOP compatibility example.",
        "config_de": "Der ausgewählte Full-Lifecycle-Pfad ist der native HTX-Filter. Er ist nicht das historische SPOE/SPOP-Kompatibilitätsbeispiel.",
        "variables": [("HAPROXY_VERSION", "Optional", "selected host version", FRAMEWORK_PROVIDER_PIN_OR_CALLER, "the current provider pin"), ("HAPROXY_SOURCE_URL", "Optional", "HTTPS archive URL", FRAMEWORK_PROVIDER_PIN_OR_CALLER, "pinned source URL"), ("HAPROXY_SHA256", "Optional", "64-character SHA-256", FRAMEWORK_PROVIDER_PIN_OR_CALLER, "pinned digest"), ("HAPROXY_RUNTIME_BUILD_DIR", "Optional", ABSOLUTE_BUILD_DIRECTORY, "Provisioning", "`<build-root>/haproxy-runtime`")],
        "limit": "SPOE/SPOP remains a compatibility path and is not presented as the selected full-lifecycle evidence path.",
        "limit_de": "SPOE/SPOP bleibt ein Kompatibilitätspfad und wird nicht als ausgewählter Full-Lifecycle-Evidence-Pfad dargestellt.",
    },
    "envoy": {
        "name": "Envoy",
        "mode": "ext_proc",
        "host": "Envoy external processing (`ext_proc`) with the repository bridge",
        "host_de": "Envoy External Processing (`ext_proc`) mit der Repository-Bridge",
        "build": "`make build-envoy` and `make check-config-envoy` use the selected `ext_proc` host path.",
        "build_de": "`make build-envoy` und `make check-config-envoy` verwenden den ausgewählten `ext_proc`-Hostpfad.",
        "config": "The selected configuration streams request and response processing through an `ext_proc` gRPC service. `ext_authz` is kept only as a compatibility example.",
        "config_de": "Die ausgewählte Konfiguration streamt Request- und Response-Verarbeitung über einen `ext_proc`-gRPC-Service. `ext_authz` bleibt nur ein Kompatibilitätsbeispiel.",
        "variables": [("ENVOY_BIN", "Optional", "executable Envoy path", PROVISIONING_OR_CALLER, "`<component-cache>/envoy/bin/envoy`"), ("ENVOY_CONFIG", "Generated", "absolute runtime YAML path", "Harness", "`<build-root>/envoy.yaml`"), ("EXT_PROC_PORT", "Optional", "local TCP port number", "Harness/caller", "`18083`"), ("NO_CRS_RULES_FILE", REQUIRED_CANONICAL_RULE_RUNS, ABSOLUTE_RULES_FILE_PATH, MAKE_DEFAULT_OR_CALLER, NO_CRS_RULES_FILE)],
        "limit": "Safe is the selected documented core mode. Strict enforcement and `ext_authz` compatibility are separate work.",
        "limit_de": "Safe ist der ausgewählte dokumentierte Kernmodus. Strict-Enforcement und `ext_authz`-Kompatibilität sind getrennte Arbeit.",
    },
    "traefik": {
        "name": "Traefik",
        "mode": "native-middleware",
        "host": "native Traefik middleware and local engine service",
        "host_de": "native Traefik-Middleware und lokaler Engine-Service",
        "build": "`make build-traefik` and `make check-config-traefik` prepare the native middleware path.",
        "build_de": "`make build-traefik` und `make check-config-traefik` bereiten den nativen Middleware-Pfad vor.",
        "config": "The selected path uses an EntryPoint, Router, native Middleware, and local engine service. `forwardAuth` remains a compatibility example.",
        "config_de": "Der ausgewählte Pfad verwendet EntryPoint, Router, native Middleware und lokalen Engine-Service. `forwardAuth` bleibt ein Kompatibilitätsbeispiel.",
        "variables": [("TRAEFIK_BIN", "Optional", "executable Traefik path", PROVISIONING_OR_CALLER, "`<component-cache>/traefik/bin/traefik`"), ("TRAEFIK_ENGINE_SERVICE_BUILD_DIR", "Optional", ABSOLUTE_BUILD_DIRECTORY, "Build script or caller", "`<build-root>/traefik-engine-service`"), ("TRAEFIK_ENGINE_SERVICE_BIN", "Optional", "absolute engine-service executable", "Build script or caller", "`<build-root>/traefik-engine-service/traefik-engine-service`"), ("TRAEFIK_CONNECTOR_CONFIG", "Optional", "absolute connector configuration", "Start-smoke harness or caller", "`config/traefik-forwardauth.conf`")],
        "limit": "Safe is the selected documented core mode. Strict enforcement and `forwardAuth` compatibility are separate work.",
        "limit_de": "Safe ist der ausgewählte dokumentierte Kernmodus. Strict-Enforcement und `forwardAuth`-Kompatibilität sind getrennte Arbeit.",
    },
    "lighttpd": {
        "name": "lighttpd",
        "mode": "patched-native",
        "host": "patched native lighttpd host with `mod_msconnector.so`",
        "host_de": "gepatchter nativer lighttpd-Host mit `mod_msconnector.so`",
        "build": "`make build-lighttpd` prepares the patched selected host; `make check-config-lighttpd` checks its configuration.",
        "build_de": "`make build-lighttpd` bereitet den gepatchten ausgewählten Host vor; `make check-config-lighttpd` prüft dessen Konfiguration.",
        "config": "The selected path uses the patched host hook and module configuration. It is distinct from the older sidecar compatibility example.",
        "config_de": "Der ausgewählte Pfad verwendet den gepatchten Host-Hook und die Modulkonfiguration. Er unterscheidet sich vom älteren Sidecar-Kompatibilitätsbeispiel.",
        "variables": [("LIGHTTPD_SOURCE_URL", "Optional", "HTTPS source archive URL", "Provisioning/caller", "pinned source URL"), ("LIGHTTPD_BUILD_ROOT", "Optional", ABSOLUTE_BUILD_DIRECTORY, "Provisioning", "`<build-root>/lighttpd`"), ("LIGHTTPD_CONFIG", "Generated", "absolute host configuration path", "Harness", "`<build-root>/lighttpd.conf`"), ("NO_CRS_RULES_FILE", REQUIRED_CANONICAL_RULE_RUNS, ABSOLUTE_RULES_FILE_PATH, MAKE_DEFAULT_OR_CALLER, NO_CRS_RULES_FILE)],
        "limit": "Host-patch, compression, optional protocol profiles, and strict enforcement remain explicitly bounded by current evidence.",
        "limit_de": "Host-Patch, Kompression, optionale Protokollprofile und Strict-Enforcement bleiben durch die aktuelle Evidence ausdrücklich begrenzt.",
    },
}


def header(title: str, partner: str, german: bool) -> list[str]:
    language = f"**Sprache:** [English]({partner}) | Deutsch" if german else f"**Language:** English | [Deutsch]({partner})"
    return [MARKER, "", f"# {title}", "", language, ""]


def localized(data: dict, key: str, german: bool) -> str:
    """Return a translated connector-specific phrase when one is maintained."""
    return data.get(f"{key}_de", data[key]) if german else data[key]


def scope(german: bool) -> list[str]:
    label = "Geltungsbereich" if german else "Scope"
    text = (
        "Dieser Leitfaden beschreibt den aktuellen ausgewählten HTTP/1.1-P1–P4-Kern. Er behauptet keine Produktionsreife, vollständige CRS-, HTTP/2- oder HTTP/3-Verifikation und keine Strict-Verifikation für alle Connectoren."
        if german
        else "This guide describes the current selected HTTP/1.1 P1–P4 core. It does not claim production readiness, complete CRS, HTTP/2, or HTTP/3 verification, or Strict verification for every connector."
    )
    return [f"## {label}", "", text, ""]


def variables_table(data: dict, german: bool) -> list[str]:
    title = "Konfigurationsvariablen und Platzhalter" if german else "Configuration variables and placeholders"
    headers = "| Name | Pflicht | Format | Gesetzt durch | Beispielwert |" if german else "| Name | Required | Format | Set by | Example value |"
    separator = "| --- | --- | --- | --- | --- |"
    def code(value: str) -> str:
        return value if value.startswith("`") and value.endswith("`") else f"`{value}`"

    rows = [f"| `{name}` | {required} | {format_} | {owner} | {code(example)} |" for name, required, format_, owner, example in data["variables"]]
    lead = (
        "Die Tabelle enthält nur vorhandene Eingaben oder generierte Pfade. Ein Beispielwert ist kein stiller Default; Details zu Pflicht, Scope, Auswirkung und Sicherheit stehen in der zentralen Referenz."
        if german
        else "The table lists only existing inputs or generated paths. An example value is not an implicit default; requiredness, scope, effect, and security notes are in the central reference."
    )
    central = "../../configuration/variables.de.md" if german else "../../configuration/variables.md"
    return [f"## {title}", "", lead, "", headers, separator, *rows, "", f"See the [central variables reference]({central})." if not german else f"Siehe die [zentrale Variablenreferenz]({central}).", ""]


def _document_intro(kind: str, name: str, partner: str, german: bool) -> list[str]:
    title = DOCUMENT_TITLES[kind][1 if german else 0].format(name=name)
    return header(title, partner, german) + scope(german)


def _render_readme(data: dict, name: str, partner: str, german: bool) -> list[str]:
    lines = _document_intro("README", name, partner, german)
    lines += ["## Selected integration mode", "", f"`{data['mode']}` — {data['host']}.", "", "## Current core", "", "HTTP/1.1 P1–P4 with Safe post-commit Phase 4 semantics, first byte before EOS evidence, and no connector-owned full response buffer.", "", "## Quick links", "", "- [Architecture](architecture.md)", "- [Build](build.md)", "- [Configuration](configuration.md)", "- [Lifecycle](lifecycle.md)", "- [Testing](testing.md)", "- [Operations](operations.md)", "- [Limitations](limitations.md)", ""]
    if german:
        lines = _document_intro("README", name, partner, True) + ["## Ausgewählter Integrationsmodus", "", f"`{data['mode']}` — {localized(data, 'host', True)}.", "", "## Aktueller Kern", "", "HTTP/1.1 P1–P4 mit Safe-Post-Commit-Phase-4-Semantik, First-Byte-vor-EOS-Evidence und ohne connector-eigenen vollständigen Response-Buffer.", "", "## Schnelllinks", "", "- [Architektur](architecture.de.md)", "- [Build](build.de.md)", "- [Konfiguration](configuration.de.md)", "- [Lifecycle](lifecycle.de.md)", "- [Tests](testing.de.md)", "- [Betrieb](operations.de.md)", "- [Grenzen](limitations.de.md)", ""]
    return lines


def _render_architecture(data: dict, name: str, partner: str, german: bool) -> list[str]:
    lines = _document_intro("architecture", name, partner, german)
    if german:
        lines += ["## Hostintegration", "", localized(data, "host", True) + ". Common erhält nur neutral gemappte Werte; Host-APIs, Speicherallokation und Callback-Lebensdauer bleiben außerhalb von Common.", "", "## Transaktions-Lifecycle", "", "| Phase | Bedeutung |\n| --- | --- |\n| P1 | Request-Header vor dem Upstream-Request |\n| P2 | Request-Body; Abschluss an Request-EOS |\n| P3 | Response-Header |\n| P4 | Response-Body; Abschluss an Response-EOS |", "", "## Datenfluss und Engine-Anbindung", "", "Die Adapter geben geliehene Header- und Body-Abschnitte an Common weiter. Common ruft die Engine über seine neutrale Schnittstelle auf; Host-spezifische Typen, Puffer und Callbacks werden nicht in Common übertragen.", "", "## Ownership und Lifetime", "", "Body-Chunks werden nicht connector-eigen vollständig gepuffert. Events und Reports speichern keine Roh-Request- oder Response-Bodies. Adapter-Cleanup folgt dem Ende des Host-Lifecycles und bleibt der gleichen Transaktion zurechenbar.", ""]
    else:
        lines += ["## Host integration", "", data["host"] + ". Common receives only neutral mapped values; host APIs, allocation, and callback lifetime remain outside Common.", "", "## Transaction lifecycle", "", "| Phase | Meaning |\n| --- | --- |\n| P1 | Request headers before the upstream request |\n| P2 | Request body; finish at request EOS |\n| P3 | Response headers |\n| P4 | Response body; finish at response EOS |", "", "## Data flow and engine binding", "", "The adapter passes borrowed header and body slices to Common. Common calls the engine through its neutral interface; host-specific types, buffers, and callbacks are never passed into Common.", "", "## Ownership and lifetime", "", "Body chunks are not fully buffered by the connector. Events and reports retain no raw request or response body. Adapter cleanup follows the host lifecycle end and remains attributable to the same transaction.", ""]
    return lines


def _render_build(connector: str, data: dict, name: str, partner: str, german: bool) -> list[str]:
    lines = _document_intro("build", name, partner, german)
    if german:
        lines += ["## Buildpfad und Hostversion", "", localized(data, "build", True), "", "Die maßgebliche Hostversion ist die Version der aktuellen vorbereiteten Runtime oder ihres gepinnten Provisionierungsinputs. Eine dokumentierte Version ist keine Aussage über jede Distribution, ABI oder Betriebsumgebung.", "", "## Toolchain und Abhängigkeiten", "", "Benötigt werden der zum Host passende C/C++- bzw. Go-Toolchainpfad, libmodsecurity-Abhängigkeiten und ein beschreibbarer Build-/Cache-Root außerhalb des Checkouts. Compiler, Flags und Hostrevisionen werden als Build-Provenance festgehalten; dieser Leitfaden behauptet keine universelle Compiler- oder Go-Version.", "", "## Cache-v2 und Provenienz", "", "Die Wiederverwendung von Cache-v2 ist identitätsgebunden. Source-URL, Revision oder Digest, Patchset, Architektur, Compiler und Konfiguration bestimmen, ob ein Cache-Eintrag wiederverwendbar ist. Ein Cache-Treffer ist kein Runtime-PASS.", "", "## Build, Config und Runtime", "", f"Führen Sie `make build-{connector}` und danach `make check-config-{connector}` aus. Start- und Runtime-Smokes existieren nur für die jeweils angebotenen Targetfamilien; der ausgewählte Kernlauf ist `make full-lifecycle-{connector}`. Erfolgreicher Build oder Config-Check ist kein Rule-Engine-PASS.", "", "## Optionale Profile und Fehlerdiagnose", "", "Kompatibilitäts-, CRS-, erweitertes Matrix-, H2/H3- und Strict-Profile sind getrennt vom ausgewählten Kern. Prüfen Sie bei Fehlern Executable-Pfade, ABI, Modul-/Service-Load, beschreibbare Runtime-Roots sowie gepinnte Source-/Patch-Eingaben, bevor Sie Konfiguration ändern.", ""]
    else:
        lines += ["## Build path and host version", "", data["build"], "", "The authoritative host version is the version of the current prepared runtime or its pinned provisioning input. A documented version is not support for every distribution, ABI, or operating environment.", "", "## Toolchain and dependencies", "", "Use the host-appropriate C/C++ or Go toolchain, libmodsecurity dependencies, and a writable build/cache root outside the checkout. Compiler, flags, and host revision are recorded as build provenance; this guide makes no universal compiler or Go-version claim.", "", "## Cache-v2 and provenance", "", "Cache-v2 reuse is identity-bound. Source URL, revision or digest, patchset, architecture, compiler, and configuration decide whether an entry is reusable. A cache hit is not a runtime PASS.", "", "## Build, configuration, and runtime", "", f"Run `make build-{connector}` and then `make check-config-{connector}`. Start and runtime smokes exist only for the target families that provide them; the selected core run is `make full-lifecycle-{connector}`. A successful build or config check is not a rule-engine PASS.", "", "## Optional profiles and troubleshooting", "", "Compatibility, CRS, extended-matrix, H2/H3, and Strict profiles remain separate from the selected core. Before changing configuration, check executable paths, ABI, module/service load, writable runtime roots, and pinned source/patch inputs.", ""]
    lines += variables_table(data, german)
    return lines


def _render_configuration(connector: str, data: dict, name: str, partner: str, german: bool) -> list[str]:
    lines = _document_intro("configuration", name, partner, german)
    if german:
        lines += ["## Konfigurationsmodell", "", localized(data, "config", True), "", "## Minimal, Safe und Strict", "", f"Die [annotierten {name}-Beispiele](../../../examples/{connector}/README.de.md) sind die vollständige lokale Quelle. Ersetzen Sie jeden Pfad, Port und Endpoint für den Zielhost. Minimal und Safe gehören zum dokumentierten Kern; Strict wird nur dort beschrieben, wo der Host und aktuelle Evidence es tragen. Kopieren Sie keine Kompatibilitätskonfiguration als ausgewählten Kernpfad.", "", "## Defaults, Body-Scope und Logging", "", "Nur vorhandene Hostdirektiven und Harness-Optionen sind in den Beispielen aufgeführt. Body- und Content-Type-Verhalten bleiben host- und profilgebunden; keine Konfiguration erlaubt einen connector-eigenen vollständigen Response-Buffer. Nutzen Sie payloadfreie Connector-/Evidence-Logs und speichern Sie keine Secrets in Regeln, Pfaden oder Kommandozeilen.", "", "## Validierung", "", f"Führen Sie `make check-config-{connector}` vor dem Start aus. Der Kernlauf `make full-lifecycle-{connector}` benötigt beschreibbare Runtime- und Evidence-Roots; prüfen Sie das Ergebnis immer anhand der Artefakte.", ""]
    else:
        lines += ["## Configuration model", "", data["config"], "", "## Minimal, Safe, and Strict", "", f"The [annotated {name} examples](../../../examples/{connector}/README.md) are the complete local source. Replace every path, port, and endpoint for the target host. Minimal and Safe belong to the documented core; Strict is described only where the host and current evidence support it. Do not copy a compatibility configuration as the selected core path.", "", "## Defaults, body scope, and logging", "", "Only existing host directives and harness options are listed in the examples. Body and content-type behavior remain host- and profile-bound; no configuration permits a connector-owned full response buffer. Use payload-free connector/evidence logs and keep secrets out of rules, paths, and command lines.", "", "## Validation", "", f"Run `make check-config-{connector}` before starting a host. The core run `make full-lifecycle-{connector}` needs writable runtime and evidence roots; always inspect its artifacts for the result.", ""]
    lines += variables_table(data, german)
    return lines


def _render_lifecycle(data: dict, name: str, partner: str, german: bool) -> list[str]:
    lines = _document_intro("lifecycle", name, partner, german)
    if german:
        lines += ["## Phasen und EOS", "", "| Phase | Bedeutung |\n| --- | --- |\n| P1 | Request-Header |\n| P2 | Request-Body; Abschluss an Request-EOS |\n| P3 | Response-Header |\n| P4 | Response-Body; Abschluss an Response-EOS |", "", "## Pre-Commit und Post-Commit", "", "Vor dem Response-Commit darf ein Host eine unterstützte Pre-Commit-Aktion anwenden. Nach dem Commit protokolliert Safe `log_only`; Safe behauptet keinen umgeschriebenen sichtbaren Status. " + localized(data, "limit", True), "", "## First Byte, Buffering und Cleanup", "", "Die ausgewählte Evidence verlangt, wo anwendbar, eine First-Byte-vor-EOS-Beobachtung und verbietet einen connector-eigenen Full-Response-Buffer. Lifecycle-Counter, Events und Cleanup müssen derselben Transaktion zurechenbar sein.", ""]
    else:
        lines += ["## Phases and EOS", "", "| Phase | Meaning |\n| --- | --- |\n| P1 | Request headers |\n| P2 | Request body; finish at request EOS |\n| P3 | Response headers |\n| P4 | Response body; finish at response EOS |", "", "## Pre-commit and post-commit", "", "Before response commitment, a host may take a supported pre-commit action. After commitment, Safe records `log_only`; Safe does not claim a rewritten visible status. " + data["limit"], "", "## First byte, buffering, and cleanup", "", "The selected evidence requires first-byte-before-EOS observation where applicable and rejects a connector-owned full response buffer. Lifecycle counters, events, and cleanup must be attributable to the same transaction.", ""]
    return lines


def _render_testing(connector: str, name: str, partner: str, german: bool) -> list[str]:
    lines = _document_intro("testing", name, partner, german)
    if german:
        lines += ["## Ebenen", "", f"Führen Sie `make build-{connector}`, `make check-config-{connector}`, einen vorhandenen Start-/Runtime-Smoke und `make full-lifecycle-{connector}` als getrennte Ebenen aus. Build, Config und Start sind kein Rule-Engine-PASS.", "", "## No-CRS-Kernregeln und Cases", "", "Diese Rule-IDs gehören zum repository-eigenen No-CRS-Testprofil, nicht zu OWASP CRS.", "", "| Rule-ID | Phase | Zweck |\n| ---: | --- | --- |\n| `1100001` | P1 | Request-Header deny |\n| `1100101` | P2 | Request-Body deny |\n| `1100201` | P3 | Response-Header deny |\n| `1100301` | P4 | Response-Body deny oder Safe-Late-Intervention |", "", "## Evidence und Run-Grenze", "", "Case-IDs beschreiben eine Capability und den erwarteten Zustand. Ein ausgewählter Case benötigt zurechenbare Result-/Event-Evidence, Profilidentität und die konfigurierte Run-ID. Ein `PASS`-Aggregat darf nicht aus Build-Ausgabe abgeleitet werden.", "", "## Statuswerte", "", "`PASS`, `FAIL`, `BLOCKED`, `NOT EXECUTED`, `NOT APPLICABLE` und `UNSUPPORTED` stehen unter [Testebenen](../../testing/test-levels.de.md).", ""]
    else:
        lines += ["## Levels", "", f"Run `make build-{connector}`, `make check-config-{connector}`, any available start/runtime smoke, and `make full-lifecycle-{connector}` as separate levels. Build, configuration, and start are not rule-engine PASS.", "", "## No-CRS core rules and cases", "", "These rule IDs belong to the repository-owned No-CRS test profile, not OWASP CRS.", "", "| Rule ID | Phase | Purpose |\n| ---: | --- | --- |\n| `1100001` | P1 | Request-header deny |\n| `1100101` | P2 | Request-body deny |\n| `1100201` | P3 | Response-header deny |\n| `1100301` | P4 | Response-body deny or Safe late intervention |", "", "## Evidence and run boundary", "", "Case IDs identify a capability and expected state. A selected case needs attributable result/event evidence, profile identity, and the configured run ID. A PASS aggregate must not be inferred from build output.", "", "## Statuses", "", "`PASS`, `FAIL`, `BLOCKED`, `NOT EXECUTED`, `NOT APPLICABLE`, and `UNSUPPORTED` are defined in [test levels](../../testing/test-levels.md).", ""]
    return lines


def _render_operations(name: str, partner: str, german: bool) -> list[str]:
    lines = _document_intro("operations", name, partner, german)
    if german:
        lines += ["## Start und Stop", "", "Verwenden Sie für lokale Harnesses die passenden Make-Targets. Operatorverwaltete Services verwenden ihren eigenen Service-Manager und den Host-Config-Check.", "", "## Logs, Rotation und Health", "", "Nutzen Sie Host-Error-/Access-Logs und payloadfreie Connector-/Evidence-Logs. Rotieren Sie Logs mit der Hostfunktion, nicht durch Umbenennen offener Dateien. Health bedeutet Erreichbarkeit und geladene Konfiguration; es ist kein Security- oder Lifecycle-PASS.", "", "## Timeouts und Ressourcen", "", "Setzen Sie Host-Timeouts, Worker-/Datei-/Speicherlimits und Runtime-Roots nach den Grenzen des Zielhosts. Repository-Timeoutvariablen begrenzen Jobs, ersetzen aber keine Produktionsdimensionierung. Vermeiden Sie Secrets in Pfaden, Prozessen, Events und kanonischer Evidence.", "", "## Diagnose und Updates", "", "Prüfen Sie Endpoint-Erreichbarkeit, Modul-/Service-Load, Lesbarkeit der Rule-Datei, Runtime-Root-Rechte und den ausgewählten Integrationsmodus, bevor Sie ein fehlendes Ergebnis als Rule-Fehler deuten. Host-, Modul-, Patchset- und Source-Revisionen schaffen eine neue Build-/Cache-Identität; führen Sie danach den ausgewählten Evidence-Target erneut aus.", ""]
    else:
        lines += ["## Start and stop", "", "Use matching Make targets for local harnesses. Operator-managed services use their own service manager and host configuration check.", "", "## Logs, rotation, and health", "", "Use host error/access logs and payload-free connector/evidence logs. Rotate logs through the host facility rather than renaming open files. Health means reachability and a loaded configuration; it is not a security or lifecycle PASS.", "", "## Timeouts and resources", "", "Set host timeouts, worker/file/memory limits, and runtime roots for the target host's boundaries. Repository timeout variables bound jobs but do not replace production sizing. Keep secrets out of paths, processes, events, and canonical evidence.", "", "## Diagnosis and updates", "", "Check endpoint reachability, module/service load, rules-file readability, runtime-root permissions, and the selected integration mode before treating a missing result as a rule failure. Host, module, patchset, and source-revision changes create a new build/cache identity; rerun the selected evidence target afterward.", ""]
    return lines


def _render_limitations(data: dict, name: str, partner: str, german: bool) -> list[str]:
    lines = _document_intro("limitations", name, partner, german)
    if german:
        lines += ["## Grenzen", "", localized(data, "limit", True), "", "## Nicht durch diesen Leitfaden abgedeckt", "", "Strict-Transport-Enforcement über die ausgewählte Evidence hinaus, vollständige HTTP/2- oder HTTP/3-Verifikation, CRS-Verifikation, vollständige Extended-Matrix-Ausführung, Kompressionsverhalten und Produktionsreife bleiben getrennte Arbeit.", "", "## Kompatibilitätspfade", "", "Kompatibilitätskonfigurationen liegen getrennt unter `examples/` und dürfen nicht als ausgewählter Full-Lifecycle-Beweis zitiert werden.", ""]
    else:
        lines += ["## Boundaries", "", data["limit"], "", "## Not covered by this guide", "", "Strict transport enforcement beyond the selected evidence, complete HTTP/2 or HTTP/3 verification, CRS verification, full extended-matrix execution, compression behavior, and production suitability remain separate work.", "", "## Compatibility paths", "", "Compatibility configurations are kept separately in `examples/` and must not be cited as selected full-lifecycle proof.", ""]
    return lines


def _render_sections(
    kind: str, connector: str, data: dict, name: str, partner: str, german: bool
) -> list[str]:
    renderers = {
        "README": lambda: _render_readme(data, name, partner, german),
        "architecture": lambda: _render_architecture(data, name, partner, german),
        "build": lambda: _render_build(connector, data, name, partner, german),
        "configuration": lambda: _render_configuration(connector, data, name, partner, german),
        "lifecycle": lambda: _render_lifecycle(data, name, partner, german),
        "testing": lambda: _render_testing(connector, name, partner, german),
        "operations": lambda: _render_operations(name, partner, german),
        "limitations": lambda: _render_limitations(data, name, partner, german),
    }
    return renderers[kind]()


def _finish_content(lines: list[str], kind: str, german: bool) -> str:
    if german and kind not in {"README"}:
        # Preserve structural parity while translating the repeated practical labels.
        text = "\n".join(lines)
        for old, new in GERMAN_LABEL_REPLACEMENTS.items():
            text = text.replace(old, new)
        return text.rstrip() + "\n"
    return "\n".join(lines).rstrip() + "\n"


def content(kind: str, connector: str, data: dict, german: bool) -> str:
    name = data["name"]
    partner = f"{kind}{'.md' if german else '.de.md'}"
    lines = _render_sections(kind, connector, data, name, partner, german)
    return _finish_content(lines, kind, german)


def main() -> None:
    for connector, data in CONNECTORS.items():
        directory = ROOT / "docs" / "connectors" / connector
        directory.mkdir(parents=True, exist_ok=True)
        for name in DOCUMENT_KINDS:
            directory.joinpath(f"{name}.md").write_text(content(name, connector, data, False), encoding="utf-8")
            directory.joinpath(f"{name}.de.md").write_text(content(name, connector, data, True), encoding="utf-8")


if __name__ == "__main__":
    main()
