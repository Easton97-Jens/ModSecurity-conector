#!/usr/bin/env python3
"""Generate the current bilingual compiler/build guides.

The guides deliberately document repository targets and selected host profiles,
not a distribution-specific installation procedure.  Keeping the English and
German variants here prevents a move or target rename from leaving one variant
with an obsolete command.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "build" / "compilers"
MARKER = "<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->"


CONNECTORS: tuple[dict[str, str], ...] = (
    {
        "slug": "apache",
        "name": "Apache HTTP Server",
        "name_de": "Apache HTTP Server",
        "profile": "native-httpd-module",
        "mode": "native httpd module built through APXS",
        "mode_de": "natives httpd-Modul, das über APXS gebaut wird",
        "full": "full-lifecycle-apache",
        "build": "build-apache",
        "config": "check-config-apache",
        "start": "start-smoke-apache",
        "runtime": "runtime-smoke-apache",
        "prepare": "prepare-runtime-components",
        "source": "The Framework-owned Apache, APR, PCRE2 and libmodsecurity provenance is selected at preparation time. Its effective version, URL and checksum are recorded by the Cache-v2 inventory; do not copy a version from an old guide.",
        "source_de": "Die Framework-gesteuerte Provenienz für Apache, APR, PCRE2 und libmodsecurity wird bei der Vorbereitung ausgewählt. Effektive Version, URL und Prüfsumme stehen im Cache-v2-Inventar; keine Version aus einer alten Anleitung übernehmen.",
        "variables": "`BUILD_HTTPD_FROM_SOURCE`, `APACHE_BIN`, `APACHECTL_BIN`, `APXS_BIN`, and the Framework-forwarded Apache source/checksum variables.",
        "variables_de": "`BUILD_HTTPD_FROM_SOURCE`, `APACHE_BIN`, `APACHECTL_BIN`, `APXS_BIN` sowie die vom Framework weitergereichten Apache-Quell- und Prüfsummenvariablen.",
        "toolchain": "A trusted C compiler, Autotools/APXS and matching Apache development headers are required when the host is built or checked locally. The repository's C17 adoption check may report `77` when headers are unavailable.",
        "toolchain_de": "Ein vertrauenswürdiger C-Compiler, Autotools/APXS und passende Apache-Entwicklungsheader sind für einen lokalen Host-Build oder -Check erforderlich. Der C17-Adoptionscheck des Repositorys kann bei fehlenden Headern `77` melden.",
        "optional": "For a diagnostic source-host smoke, use `BUILD_HTTPD_FROM_SOURCE=1 make smoke-apache`. `make check-apache-c17` checks the adoption boundary; optional newer C profiles remain toolchain-dependent.",
        "optional_de": "Für einen diagnostischen Source-Host-Smoke `BUILD_HTTPD_FROM_SOURCE=1 make smoke-apache` verwenden. `make check-apache-c17` prüft die Adoptionsgrenze; optionale neuere C-Profile hängen weiter vom Toolchain-Support ab.",
        "historical": "Older package-install examples and generic smoke descriptions are compatibility notes only. They neither select nor replace the `native-httpd-module` full-lifecycle profile.",
        "historical_de": "Ältere Paketinstallationsbeispiele und allgemeine Smoke-Beschreibungen sind nur Kompatibilitätshinweise. Sie wählen oder ersetzen das Full-Lifecycle-Profil `native-httpd-module` nicht.",
        "trouble": "If APXS and httpd do not match, rebuild against the selected host. If the config stage fails, inspect the generated config and the sanitized host log before changing rules or module paths.",
        "trouble_de": "Bei nicht zusammenpassendem APXS und httpd gegen den ausgewählten Host neu bauen. Schlägt der Konfigurationsschritt fehl, zuerst generierte Konfiguration und sanitisiertes Host-Log prüfen, bevor Regeln oder Modulpfade geändert werden.",
    },
    {
        "slug": "nginx",
        "name": "NGINX",
        "name_de": "NGINX",
        "profile": "native-nginx-http-module",
        "mode": "native NGINX HTTP module",
        "mode_de": "natives NGINX-HTTP-Modul",
        "full": "full-lifecycle-nginx",
        "build": "build-nginx",
        "config": "check-config-nginx",
        "start": "start-smoke-nginx",
        "runtime": "runtime-smoke-nginx",
        "prepare": "prepare-runtime-components",
        "source": "The Framework resolves the NGINX source policy and libmodsecurity inputs. The prepared Cache-v2 inventory and its provenance records, not this guide, are the source of the effective revision and host build identity.",
        "source_de": "Das Framework löst die NGINX-Quellrichtlinie und die libmodsecurity-Eingaben auf. Das vorbereitete Cache-v2-Inventar mit Provenienz, nicht diese Anleitung, ist die Quelle für effektive Revision und Host-Build-Identität.",
        "variables": "`BUILD_NGINX_FROM_SOURCE`, `NGINX_SOURCE_MODE`, `NGINX_SOURCE_REPO_URL`, `NGINX_SOURCE_GIT_REF`, `NGINX_RELEASE_TAG`, `NGINX_BIN`, `NGINX_PREFIX`, and `NGINX_MODULE`.",
        "variables_de": "`BUILD_NGINX_FROM_SOURCE`, `NGINX_SOURCE_MODE`, `NGINX_SOURCE_REPO_URL`, `NGINX_SOURCE_GIT_REF`, `NGINX_RELEASE_TAG`, `NGINX_BIN`, `NGINX_PREFIX` und `NGINX_MODULE`.",
        "toolchain": "A trusted C compiler and the selected NGINX build inputs are required. Module ABI, prefix, worker permissions and runtime paths belong to the selected host and must stay outside the checkout.",
        "toolchain_de": "Ein vertrauenswürdiger C-Compiler und die ausgewählten NGINX-Build-Eingaben sind erforderlich. Modul-ABI, Prefix, Worker-Berechtigungen und Laufzeitpfade gehören zum ausgewählten Host und müssen außerhalb des Checkouts liegen.",
        "optional": "For a diagnostic source-host smoke, use `BUILD_NGINX_FROM_SOURCE=1 make smoke-nginx`. `make check-nginx-c17` checks the adoption boundary; it is not runtime evidence.",
        "optional_de": "Für einen diagnostischen Source-Host-Smoke `BUILD_NGINX_FROM_SOURCE=1 make smoke-nginx` verwenden. `make check-nginx-c17` prüft die Adoptionsgrenze; das ist kein Laufzeitnachweis.",
        "historical": "A direct dynamic-module build or a narrowed smoke can help diagnose an ABI or permissions issue, but it is not a substitute for the selected `native-nginx-http-module` evidence route.",
        "historical_de": "Ein direkter Dynamic-Module-Build oder ein eingegrenzter Smoke kann ABI- oder Berechtigungsprobleme diagnostizieren, ersetzt aber nicht den ausgewählten Evidenzweg `native-nginx-http-module`.",
        "trouble": "For module-load failures, verify the selected binary, module ABI, prefix and worker-access preflight. Do not relabel a protocol profile as HTTP/2 or HTTP/3 proof without matching evidence.",
        "trouble_de": "Bei Modul-Ladefehlern ausgewähltes Binary, Modul-ABI, Prefix und Worker-Access-Preflight prüfen. Ein Protokollprofil ohne passende Evidenz nicht als HTTP/2- oder HTTP/3-Nachweis bezeichnen.",
    },
    {
        "slug": "haproxy",
        "name": "HAProxy",
        "name_de": "HAProxy",
        "profile": "native-htx-filter",
        "mode": "native HTX filter selected for the full lifecycle",
        "mode_de": "nativer HTX-Filter, der für den vollständigen Lifecycle ausgewählt ist",
        "full": "full-lifecycle-haproxy-htx",
        "build": "build-haproxy",
        "config": "check-config-haproxy",
        "start": "start-smoke-haproxy",
        "runtime": "runtime-smoke-haproxy",
        "prepare": "prepare-runtime-components",
        "source": "The Framework/provider pin selects HAProxy source, checksum and runtime inputs. Cache-v2 provenance and the selected run's host metadata provide the effective host identity; do not infer it from a compatibility agent build.",
        "source_de": "Der Framework-/Provider-Pin wählt HAProxy-Quelle, Prüfsumme und Laufzeiteingaben. Cache-v2-Provenienz und Host-Metadaten des ausgewählten Runs liefern die effektive Host-Identität; diese nicht aus einem Kompatibilitäts-Agent-Build ableiten.",
        "variables": "`HAPROXY_VERSION`, `HAPROXY_SOURCE_URL`, `HAPROXY_SHA256`, `HAPROXY_SOURCE_DIR`, `HAPROXY_BIN`, and the advanced `HAPROXY_HTX_*` paths.",
        "variables_de": "`HAPROXY_VERSION`, `HAPROXY_SOURCE_URL`, `HAPROXY_SHA256`, `HAPROXY_SOURCE_DIR`, `HAPROXY_BIN` und die erweiterten `HAPROXY_HTX_*`-Pfade.",
        "toolchain": "A trusted C/C++ toolchain, libmodsecurity headers/libraries and the selected HAProxy source are needed. The root build stage creates the SPOA/libmodsecurity compatibility artifacts; the selected full-lifecycle route separately builds and observes the HTX host overlay.",
        "toolchain_de": "Ein vertrauenswürdiges C/C++-Toolchain, libmodsecurity-Header/-Bibliotheken und die ausgewählte HAProxy-Quelle werden benötigt. Der Root-Build erzeugt SPOA/libmodsecurity-Kompatibilitätsartefakte; der ausgewählte Full-Lifecycle-Weg baut und beobachtet den HTX-Host-Overlay getrennt.",
        "optional": "`make -C connectors/haproxy build-spoa-runtime` and its self-tests are useful local diagnostics. `make check-haproxy-htx-overlay` checks overlay structure; `make check-haproxy-c17` checks the C adoption boundary.",
        "optional_de": "`make -C connectors/haproxy build-spoa-runtime` und seine Selbsttests sind hilfreiche lokale Diagnosen. `make check-haproxy-htx-overlay` prüft die Overlay-Struktur; `make check-haproxy-c17` die C-Adoptionsgrenze.",
        "historical": "The SPOE/SPOP compatibility agent and a standalone HTX smoke are historical or diagnostic integration routes. They must not be relabelled as the canonical `native-htx-filter` run.",
        "historical_de": "Der SPOE/SPOP-Kompatibilitäts-Agent und ein eigenständiger HTX-Smoke sind historische oder diagnostische Integrationswege. Sie dürfen nicht als kanonischer `native-htx-filter`-Run umetikettiert werden.",
        "trouble": "If a binding build is blocked, inspect the prepared libmodsecurity include/library paths. If the HTX route fails, preserve the generated overlay provenance and sanitized host records instead of substituting a SPOA result.",
        "trouble_de": "Ist ein Binding-Build blockiert, die vorbereiteten libmodsecurity-Include-/Library-Pfade prüfen. Schlägt der HTX-Weg fehl, Overlay-Provenienz und sanitisierte Host-Records bewahren, statt ein SPOA-Ergebnis zu ersetzen.",
    },
    {
        "slug": "envoy",
        "name": "Envoy",
        "name_de": "Envoy",
        "profile": "ext_proc",
        "mode": "streamed Envoy external-processing service with a Common/libmodsecurity bridge",
        "mode_de": "gestreamter Envoy-External-Processing-Service mit Common/libmodsecurity-Bridge",
        "full": "full-lifecycle-envoy-ext-proc",
        "build": "build-envoy",
        "config": "check-config-envoy",
        "start": "start-smoke-envoy",
        "runtime": "runtime-smoke-envoy",
        "prepare": "prepare-envoy-runtime",
        "source": "The Framework runtime preparer selects and verifies the Envoy binary/input provenance. Read the Cache-v2 inventory and generated runtime records for the effective host version and checksum rather than relying on copied release text.",
        "source_de": "Der Framework-Laufzeitvorbereiter wählt und verifiziert Envoy-Binary und Eingabeprovenienz. Für effektive Host-Version und Prüfsumme das Cache-v2-Inventar und generierte Runtime-Records lesen statt kopierten Release-Text zu verwenden.",
        "variables": "`ENVOY_BIN`, `EXT_PROC_CONFIG`, `EXT_PROC_RUNTIME_CONFIG`, `EXT_PROC_RUNTIME_ROOT`, `RULES_FILE`, `MSCONNECTOR_RULES_FILE`, and the opt-in `ENVOY_TRANSPORT_CANCEL_PROBE`.",
        "variables_de": "`ENVOY_BIN`, `EXT_PROC_CONFIG`, `EXT_PROC_RUNTIME_CONFIG`, `EXT_PROC_RUNTIME_ROOT`, `RULES_FILE`, `MSCONNECTOR_RULES_FILE` und das Opt-in `ENVOY_TRANSPORT_CANCEL_PROBE`.",
        "toolchain": "A trusted C compiler, Go toolchain, libmodsecurity build inputs and a verified Envoy binary are needed for the selected ext_proc route. Direct connector targets use generated files beneath an external build root.",
        "toolchain_de": "Für den ausgewählten ext_proc-Weg werden ein vertrauenswürdiger C-Compiler, Go-Toolchain, libmodsecurity-Build-Eingaben und ein verifiziertes Envoy-Binary benötigt. Direkte Connector-Targets verwenden generierte Dateien unterhalb eines externen Build-Roots.",
        "optional": "`make -C connectors/envoy build-envoy-ext-proc`, `test-envoy-ext-proc`, and `check-envoy-ext-proc-config` are focused local gates. `transport-cancel-smoke-envoy-ext-proc` is opt-in and remains non-promoting.",
        "optional_de": "`make -C connectors/envoy build-envoy-ext-proc`, `test-envoy-ext-proc` und `check-envoy-ext-proc-config` sind fokussierte lokale Gates. `transport-cancel-smoke-envoy-ext-proc` ist Opt-in und bleibt nicht-promovierend.",
        "historical": "The `ext_authz` service and `make smoke-envoy` compatibility path remain useful diagnostics. They do not silently become the selected `ext_proc` full-lifecycle profile.",
        "historical_de": "Der `ext_authz`-Service und der Kompatibilitätsweg `make smoke-envoy` bleiben nützliche Diagnosen. Sie werden nicht stillschweigend zum ausgewählten Full-Lifecycle-Profil `ext_proc`.",
        "trouble": "For a failed config/start check, verify the resolved `ENVOY_BIN`, generated ext_proc configuration, loopback ports and libmodsecurity runtime library paths. A cancellation probe does not prove a client-visible strict reset.",
        "trouble_de": "Bei fehlgeschlagenem Config-/Start-Check aufgelöstes `ENVOY_BIN`, generierte ext_proc-Konfiguration, Loopback-Ports und libmodsecurity-Laufzeitbibliothekspfade prüfen. Ein Cancellation-Probe beweist keinen client-sichtbaren strikten Reset.",
    },
    {
        "slug": "traefik",
        "name": "Traefik",
        "name_de": "Traefik",
        "profile": "native-middleware",
        "mode": "native Traefik middleware with a private persistent UDS engine service",
        "mode_de": "native Traefik-Middleware mit privatem persistentem UDS-Engine-Service",
        "full": "full-lifecycle-traefik-native",
        "build": "build-traefik",
        "config": "check-config-traefik",
        "start": "start-smoke-traefik",
        "runtime": "runtime-smoke-traefik",
        "prepare": "prepare-traefik-runtime",
        "source": "The Framework runtime preparer supplies the selected Traefik input and records its provenance. Use Cache-v2 inventory and the selected run records as the version source; a locally installed binary is an explicit override, not a hidden default.",
        "source_de": "Der Framework-Laufzeitvorbereiter liefert die ausgewählte Traefik-Eingabe und dokumentiert ihre Provenienz. Cache-v2-Inventar und Records des ausgewählten Runs sind die Versionsquelle; ein lokal installiertes Binary ist ein explizites Override, kein versteckter Default.",
        "variables": "`TRAEFIK_BIN`, `TRAEFIK_NATIVE_RUNTIME_ROOT`, `TRAEFIK_CONNECTOR_CONFIG`, `TRAEFIK_ENGINE_SERVICE_BIN`, `MSCONNECTOR_RULES_FILE`, and normal compiler/linker variables.",
        "variables_de": "`TRAEFIK_BIN`, `TRAEFIK_NATIVE_RUNTIME_ROOT`, `TRAEFIK_CONNECTOR_CONFIG`, `TRAEFIK_ENGINE_SERVICE_BIN`, `MSCONNECTOR_RULES_FILE` und normale Compiler-/Linker-Variablen.",
        "toolchain": "A trusted Traefik binary, Go toolchain, C compiler and libmodsecurity build inputs are required for the selected native middleware route. The UDS service and generated provider configuration are invocation-local runtime files.",
        "toolchain_de": "Für den ausgewählten nativen Middleware-Weg werden ein vertrauenswürdiges Traefik-Binary, Go-Toolchain, C-Compiler und libmodsecurity-Build-Eingaben benötigt. UDS-Service und generierte Provider-Konfiguration sind invocationslokale Runtime-Dateien.",
        "optional": "`make -C connectors/traefik build-native-middleware`, `test-native-middleware`, `build-engine-service`, and `test-engine-service` are focused local checks. They do not themselves create canonical evidence.",
        "optional_de": "`make -C connectors/traefik build-native-middleware`, `test-native-middleware`, `build-engine-service` und `test-engine-service` sind fokussierte lokale Checks. Sie erzeugen für sich allein keine kanonische Evidenz.",
        "historical": "The forwardAuth compatibility service and `make smoke-traefik` are separate diagnostic routes. They do not replace the selected `native-middleware` profile or prove a strict post-commit action.",
        "historical_de": "Der ForwardAuth-Kompatibilitätsservice und `make smoke-traefik` sind getrennte Diagnosewege. Sie ersetzen das ausgewählte Profil `native-middleware` nicht und beweisen keine strikte Post-Commit-Aktion.",
        "trouble": "Check the selected `TRAEFIK_BIN`, UDS permissions, generated File Provider configuration and loopback listeners. Do not solve a native middleware failure by publishing forwardAuth compatibility output as canonical evidence.",
        "trouble_de": "Ausgewähltes `TRAEFIK_BIN`, UDS-Berechtigungen, generierte File-Provider-Konfiguration und Loopback-Listener prüfen. Einen Native-Middleware-Fehler nicht durch Veröffentlichung von ForwardAuth-Kompatibilitätsausgabe als kanonische Evidenz umgehen.",
    },
    {
        "slug": "lighttpd",
        "name": "lighttpd",
        "name_de": "lighttpd",
        "profile": "patched-native",
        "mode": "patched native lighttpd host and matching connector module",
        "mode_de": "gepatchter nativer lighttpd-Host mit passendem Connector-Modul",
        "full": "full-lifecycle-lighttpd-patched",
        "build": "build-lighttpd",
        "config": "check-config-lighttpd",
        "start": "start-smoke-lighttpd",
        "runtime": "runtime-smoke-lighttpd",
        "prepare": "prepare-lighttpd-runtime-build",
        "source": "The Framework/provider-selected lighttpd source, patch and libmodsecurity inputs are provenance-controlled. The Cache-v2 inventory and selected host records state the effective source identity; a stock local binary is not the selected patched host.",
        "source_de": "Die vom Framework/Provider ausgewählten lighttpd-Quelle, der Patch und libmodsecurity-Eingaben sind provenienzgeführt. Cache-v2-Inventar und Records des ausgewählten Hosts nennen die effektive Source-Identität; ein lokales Stock-Binary ist nicht der ausgewählte gepatchte Host.",
        "variables": "`LIGHTTPD_BIN`, `LIGHTTPD_SOURCE_DIR`, `LIGHTTPD_BUILD_ROOT`, `LIGHTTPD_INCLUDE_DIR`, `LIGHTTPD_MODULE_DIR`, `LIGHTTPD_PATCHED_ROOT`, and the documented `LIGHTTPD_PATCHED_*` runtime paths.",
        "variables_de": "`LIGHTTPD_BIN`, `LIGHTTPD_SOURCE_DIR`, `LIGHTTPD_BUILD_ROOT`, `LIGHTTPD_INCLUDE_DIR`, `LIGHTTPD_MODULE_DIR`, `LIGHTTPD_PATCHED_ROOT` und die dokumentierten `LIGHTTPD_PATCHED_*`-Laufzeitpfade.",
        "toolchain": "A trusted C toolchain, the selected lighttpd source/patch, libmodsecurity headers/libraries and an external build root are required. The patched host and module must be built as one compatible input set.",
        "toolchain_de": "Ein vertrauenswürdiges C-Toolchain, die ausgewählte lighttpd-Quelle mit Patch, libmodsecurity-Header/-Bibliotheken und ein externer Build-Root sind nötig. Gepatchter Host und Modul müssen als kompatibler Eingabesatz gebaut werden.",
        "optional": "`make -C connectors/lighttpd check-lighttpd-core-patch`, `build-lighttpd-patched-host`, and `check-lighttpd-patched-host` are targeted preparation checks. `make smoke-lighttpd` remains a compatibility smoke, not the patched full-lifecycle run.",
        "optional_de": "`make -C connectors/lighttpd check-lighttpd-core-patch`, `build-lighttpd-patched-host` und `check-lighttpd-patched-host` sind gezielte Vorbereitungstests. `make smoke-lighttpd` bleibt ein Kompatibilitäts-Smoke, nicht der gepatchte Full-Lifecycle-Run.",
        "historical": "Stock-host and bridge/sidecar descriptions are historical or diagnostic routes. The current canonical selection is the `patched-native` host profile, and a successful patch application alone is not runtime proof.",
        "historical_de": "Stock-Host- und Bridge-/Sidecar-Beschreibungen sind historische oder diagnostische Wege. Die aktuelle kanonische Auswahl ist das Host-Profil `patched-native`; ein erfolgreicher Patch-Apply allein ist kein Laufzeitnachweis.",
        "trouble": "For module-load or patch failures, keep the selected source, patch and module build roots together and inspect the sanitized host log. Do not combine a stock binary with a module built against a different header set.",
        "trouble_de": "Bei Modul-Lade- oder Patch-Fehlern ausgewählte Quelle, Patch und Modul-Build-Roots zusammenhalten und das sanitisierte Host-Log prüfen. Ein Stock-Binary nicht mit einem Modul aus einem anderen Headersatz kombinieren.",
    },
)


def language_switch(slug: str, german: bool) -> str:
    if german:
        return f"**Sprache:** [English]({slug}.md) | Deutsch"
    return f"**Language:** English | [Deutsch]({slug}.de.md)"


def overview(german: bool) -> str:
    if german:
        rows = "\n".join(
            f"| [{item['name_de']}]({item['slug']}.de.md) | `{item['build']}` | `{item['full']}` | `{item['profile']}` |"
            for item in CONNECTORS
        )
        return f"""{MARKER}

# Compiler- und Build-Wege

**Sprache:** [English](README.md) | Deutsch

## Zweck

Dieses Verzeichnis beschreibt die aktuellen Repository-Wege für Build,
Konfigurationsladung, Start-Smoke, minimalen Runtime-Smoke und den ausgewählten
No-CRS-Full-Lifecycle-Run. Es ist keine Anleitung, einen beliebigen
Distributionshost global zu installieren. Ein erfolgreicher Build, Link oder
Config-Check ist kein Produktions-, CRS-, HTTP/2-, HTTP/3- oder
Vollmatrix-Nachweis.

## Ausgewählte Wege

| Detailanleitung | Build | ausgewähltes Full-Lifecycle-Target | Host-Profil |
| --- | --- | --- | --- |
{rows}

Die Host-Profilwerte setzt das jeweilige Full-Lifecycle-Target selbst. Die
internen Variablen `NO_CRS_ARTIFACT_PROFILE`,
`FULL_LIFECYCLE_HOST_PROFILE` und `FULL_LIFECYCLE_EXECUTED_TARGET` dürfen nicht
manuell gesetzt werden, um einen Kompatibilitäts-Smoke umzubenennen.

## Gemeinsamer Ablauf

```sh
make check-framework
make prepare-runtime-components
make build-<connector>
make check-config-<connector>
make start-smoke-<connector>
make runtime-smoke-<connector>
```

`<connector>` ist ein Dokumentationsplatzhalter für genau einen Namen aus der
Tabelle. Den Platzhalter nicht wörtlich an `make` übergeben. Für eine
kanonische Evidenz muss ein sicherer Run-Identifier derselben Ausführung
verwendet werden:

```sh
run_id="core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-<connector>
NO_CRS_RUN_ID="$run_id" make evidence-check-<connector>
```

Die vollständige Ausführung aller sechs Connectoren ist
`NO_CRS_RUN_ID="$run_id" make full-lifecycle-all-connectors`. Sie erzeugt
run-spezifische Evidenz; sie ersetzt keine Prüfung der resultierenden
Artefakte.

## Cache-v2, Versionen und Provenienz

`VERIFIED_RUN_PARENT` bestimmt einen externen, beschreibbaren
Ausführungsstamm. Daraus leitet der Root-Makefile `BUILD_ROOT` sowie
`CACHE_ROOT=.../cache-v2` und dessen gemeinsames Component-Cache ab. Das Cache
ist wiederverwendbare Eingabe, nicht kanonische Evidenz. Quellen, Versionen,
Prüfsummen und lokale Overrides werden durch die vorbereiteten Komponenten
gebunden; die effektive Identität zeigt:

```sh
make runtime-components-inventory
make runtime-components-sources
```

Die [Variablenreferenz](../../configuration/variables.de.md) definiert Format,
Standard, Scope, Wirkung und Sicherheitsgrenze aller Build-, Cache-,
Provenienz- und Hostvariablen. Nur vertrauenswürdige absolute Pfade außerhalb
des Checkouts für Build, Cache, Log und Evidenz verwenden.

## Dokumentationsgrenze

Die nachstehenden pro-Connector-Anleitungen verweisen auf die aktuelle
[Build-Übersicht](../README.de.md), die
[Teststufen](../../testing/README.de.md), die
[Evidenzregeln](../../evidence/README.de.md), Connector-Anleitungen und
Beispiele. Ältere Integrationsbeschreibungen bleiben gegebenenfalls als
historische oder diagnostische Hinweise markiert; sie sind keine aktiven
Profilselektoren und dürfen keine Capability promoten.

## Weiterführend

Die kompaktere Übersicht für Envoy, Traefik und lighttpd steht in
[Open-Connector-Wege](overview.de.md). Die Detailanleitungen beginnen bei
[Apache](apache.de.md).
"""

    rows = "\n".join(
        f"| [{item['name']}]({item['slug']}.md) | `{item['build']}` | `{item['full']}` | `{item['profile']}` |"
        for item in CONNECTORS
    )
    return f"""{MARKER}

# Compiler and build paths

**Language:** English | [Deutsch](README.de.md)

## Purpose

This directory documents the current repository paths for build,
configuration-load, start-smoke, minimal runtime smoke, and the selected
No-CRS full-lifecycle run. It is not a procedure for globally installing an
arbitrary distribution host. A successful build, link, or config check is not
production, CRS, HTTP/2, HTTP/3, or full-matrix evidence.

## Selected routes

| Detail guide | Build | selected full-lifecycle target | Host profile |
| --- | --- | --- | --- |
{rows}

Each full-lifecycle target sets its host-profile values itself. Do not set the
internal `NO_CRS_ARTIFACT_PROFILE`, `FULL_LIFECYCLE_HOST_PROFILE`, or
`FULL_LIFECYCLE_EXECUTED_TARGET` variables manually to relabel a compatibility
smoke.

## Shared workflow

```sh
make check-framework
make prepare-runtime-components
make build-<connector>
make check-config-<connector>
make start-smoke-<connector>
make runtime-smoke-<connector>
```

`<connector>` is a documentation placeholder for exactly one name in the
table; do not pass it literally to `make`. Canonical evidence uses a safe run
identifier consistently within the invocation:

```sh
run_id="core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-<connector>
NO_CRS_RUN_ID="$run_id" make evidence-check-<connector>
```

The all-six route is `NO_CRS_RUN_ID="$run_id" make
full-lifecycle-all-connectors`. It creates run-specific evidence; it does not
replace inspection of the resulting artifacts.

## Cache-v2, versions, and provenance

`VERIFIED_RUN_PARENT` selects an external writable execution parent. The root
Makefile derives `BUILD_ROOT`, then `CACHE_ROOT=.../cache-v2` and its shared
component cache from it. The cache is reusable input, not canonical evidence.
Prepared components bind sources, versions, checksums, and local overrides;
the effective identity is shown by:

```sh
make runtime-components-inventory
make runtime-components-sources
```

The [variable reference](../../configuration/variables.md) defines the format,
default, scope, effect, and security boundary for build, cache, provenance, and
host variables. Use trusted absolute paths outside the checkout for build,
cache, logs, and evidence.

## Documentation boundary

The per-connector guides below link to the current
[build overview](../README.md), [test levels](../../testing/README.md),
[evidence rules](../../evidence/README.md), connector guides, and examples.
Older integration descriptions are explicitly marked historical or diagnostic
where they remain useful; they are not active profile selectors and cannot
promote a capability.

## Next

The compact index for Envoy, Traefik, and lighttpd is
[open-connector paths](overview.md). Start the detailed guides with
[Apache](apache.md).
"""


def open_connector_overview(german: bool) -> str:
    selected = tuple(item for item in CONNECTORS if item["slug"] in {"envoy", "traefik", "lighttpd"})
    if german:
        rows = "\n".join(
            f"| [{item['name_de']}]({item['slug']}.de.md) | `{item['prepare']}` | `{item['full']}` | `{item['profile']}` |"
            for item in selected
        )
        return f"""{MARKER}

# Open-Connector-Build-Wege

**Sprache:** [English](overview.md) | Deutsch

## Zweck

Envoy, Traefik und lighttpd verwenden repository-eigene Build- und
Runtime-Komponenten. Dieser Index fasst nur ihre aktuellen ausgewählten Wege
zusammen; alle Details stehen in den Einzelanleitungen und in der
[vollständigen Compilerübersicht](README.de.md).

| Connector | Anleitung | explizite Runtime-Vorbereitung | Full Lifecycle | ausgewähltes Profil |
| --- | --- | --- | --- | --- |
{rows}

## Aktiver Weg

1. `make check-framework` ausführen.
2. Die in der Tabelle genannte Runtime-Vorbereitung ausführen, wenn ein Host
   oder dessen Cache-Eingabe noch fehlt.
3. `make build-<connector>`, `make check-config-<connector>`,
   `make start-smoke-<connector>` und `make runtime-smoke-<connector>` als
   getrennte Stufen ausführen.
4. Mit einem sicheren `NO_CRS_RUN_ID` den tabellierten Full-Lifecycle-Target
   und anschließend `make evidence-check-<connector>` ausführen.

Der Build von Envoys `ext_authz`-Service, Traefiks ForwardAuth-Service oder
einer lighttpd-Bridge kann als Kompatibilitätsdiagnose vorkommen. Keine dieser
Routen ersetzt den tabellierten ext_proc-, native-middleware- oder
patched-native-Hostweg.

## Versionen, Cache und Grenzen

`make runtime-components-inventory` und `make runtime-components-sources`
zeigen die vorbereitete Cache-v2-Provenienz. Ein erfolgreiches Herunterladen,
Entpacken, Bauen, Konfigurationsladen oder Starten ist noch kein
Produktions-, CRS-, HTTP/2-, HTTP/3-, Strict- oder vollständiger
Capability-Nachweis. Siehe die [Variablenreferenz](../../configuration/variables.de.md)
und die [Evidenzregeln](../../evidence/README.de.md).
"""
    rows = "\n".join(
        f"| [{item['name']}]({item['slug']}.md) | `{item['prepare']}` | `{item['full']}` | `{item['profile']}` |"
        for item in selected
    )
    return f"""{MARKER}

# Open connector build paths

**Language:** English | [Deutsch](overview.de.md)

## Purpose

Envoy, Traefik, and lighttpd use repository-owned build and runtime
components. This index summarizes only their current selected routes; the
individual guides and the [complete compiler overview](README.md) contain the
details.

| Connector | Guide | explicit runtime preparation | Full lifecycle | selected profile |
| --- | --- | --- | --- | --- |
{rows}

## Active route

1. Run `make check-framework`.
2. Run the runtime preparation named in the table when a host or its cache
   input is not already present.
3. Run `make build-<connector>`, `make check-config-<connector>`,
   `make start-smoke-<connector>`, and `make runtime-smoke-<connector>` as
   separate stages.
4. With a safe `NO_CRS_RUN_ID`, run the listed full-lifecycle target, then
   `make evidence-check-<connector>`.

Building Envoy's `ext_authz` service, Traefik's forwardAuth service, or a
lighttpd bridge can be useful compatibility diagnostics. None replaces the
listed ext_proc, native-middleware, or patched-native host route.

## Versions, cache, and boundary

`make runtime-components-inventory` and `make runtime-components-sources`
show the prepared Cache-v2 provenance. A successful download, extraction,
build, configuration load, or start is not production, CRS, HTTP/2, HTTP/3,
Strict, or complete-capability evidence. See the
[variable reference](../../configuration/variables.md) and
[evidence rules](../../evidence/README.md).
"""


def guide(item: dict[str, str], german: bool) -> str:
    slug = item["slug"]
    if german:
        return f"""{MARKER}

# Build und Lifecycle: {item['name_de']}

{language_switch(slug, True)}

## Zweck und ausgewählter Hostweg

Diese Anleitung beschreibt die aktuellen Root-Make-Targets für {item['name_de']}.
Der ausgewählte Full-Lifecycle-Weg ist `{item['full']}` mit Profil
`{item['profile']}`: {item['mode_de']}. Er ist von Build-, Konfigurations- und
Kompatibilitäts-Smokes getrennt.

| Stufe | aktuelles Target | Bedeutung | keine Aussage über |
| --- | --- | --- | --- |
| Build | `make {item['build']}` | baut die für den Connector ausgewählte Stufe | Konfigurationsladung oder Traffic |
| Konfiguration | `make {item['config']}` | lädt/prüft die ausgewählte Konfiguration | gesendeten Request |
| Start | `make {item['start']}` | startet und beendet den Hostweg ohne Volltraffic | Lifecycle-Coverage |
| minimaler Runtime-Smoke | `make {item['runtime']}` | führt begrenzten Runtime-Traffic aus | kanonischer Full Lifecycle |
| Full Lifecycle | `make {item['full']}` | sammelt ausgewählte No-CRS-Hostevidenz | Produktion, CRS oder Komplettmatrix |

## Hostversion und Quellherkunft

{item['source_de']}

Vor einem Build die vorbereiteten Werte sichtbar machen:

```sh
make runtime-components-inventory
make runtime-components-sources
```

Relevante Variablen: {item['variables_de']}
Ihre Formate, Defaults, Scope, Wirkung und Sicherheitsgrenzen stehen in der
[zentralen Variablenreferenz](../../configuration/variables.de.md). Ein
Override ist ein expliziter Eingabewechsel und kein Capability-Upgrade.

## Toolchain und Cache-v2

{item['toolchain_de']}

Für einen sauberen lokalen Start einen beschreibbaren Stamm außerhalb des
Checkouts auswählen. `VERIFIED_RUN_PARENT` leitet `BUILD_ROOT` und
`CACHE_ROOT=.../cache-v2` ab. Das gemeinsame Cache-Verzeichnis enthält
wiederverwendbare Eingaben, aber keine kanonische Evidenz. Nicht manuell
umsortieren oder zwischen nicht passenden Provenienzen mischen.

```sh
make {item['prepare']} VERIFIED_RUN_PARENT="/srv/modsecurity-work"
make {item['build']} VERIFIED_RUN_PARENT="/srv/modsecurity-work"
```

`/srv/modsecurity-work` ist ein Beispiel für einen absoluten Laufzeitpfad,
kein Repository-Default. Der Target kann bei fehlenden Voraussetzungen mit
Exit-Code `77` als `BLOCKED` enden.

## Build, Konfiguration und Smoke

Die Stufen getrennt ausführen, damit ein Fehler keiner stärkeren Aussage
zugeordnet wird:

```sh
make {item['build']}
make {item['config']}
make {item['start']}
make {item['runtime']}
```

Für eine ausgewählte kanonische Evidenzausführung denselben sicheren
Run-Identifier verwenden. Der Befehl `evidence-check` validiert nur bereits
erzeugte Artefakte.

```sh
run_id="{slug}-core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make {item['full']}
NO_CRS_RUN_ID="$run_id" make evidence-check-{slug}
```

`NO_CRS_RUN_ID` muss ein dateisystemsicherer Token sein. Interne
Full-Lifecycle-Profilvariablen nicht setzen, um einen direkten oder
Kompatibilitätslauf umzubenennen.

## Optionale und historische Integrationsnotizen

{item['optional_de']}

> Historischer Hinweis: {item['historical_de']}

Ein eingeschränkter Fall, `FORCE_ALL_CASES=1` oder eine direkte
Connector-Subdirectory-Ausführung ist Diagnoseinput. Nur der dokumentierte
Target mit seinem Artefaktprofil kann kanonische Evidenz produzieren.

## Konfiguration, Beispiele und Fehlersuche

- Aktuelle Connector-Dokumentation:
  [{item['name_de']}](../../connectors/{slug}/README.de.md)
- Konfigurationsdetails:
  [Connector-Konfiguration](../../connectors/{slug}/configuration.de.md)
- Repository-Beispiele:
  [examples/{slug}](../../../examples/{slug}/README.de.md)
- Test- und Evidenzgrenzen:
  [Teststufen](../../testing/README.de.md) ·
  [Evidenzregeln](../../evidence/README.de.md)

{item['trouble_de']}

Keine ungefilterten Cookies, Autorisierungswerte, Tokens, private Schlüssel
oder Rohlogs in Konfigurationen, Issues oder Evidenz aufnehmen.

## Evidenzgrenze

Dieser Text behauptet keine Produktionsreife, vollständige CRS-Abdeckung,
HTTP/2- oder HTTP/3-Unterstützung, vollständige Matrix oder strikte
Post-Commit-Intervention. Ein PASS gilt nur für den tatsächlich ausgeführten
Target, das dokumentierte Hostprofil und dessen sanitisierten, run-spezifischen
Evidenzsatz.
"""

    return f"""{MARKER}

# Build and lifecycle: {item['name']}

{language_switch(slug, False)}

## Purpose and selected host route

This guide documents the current root Make targets for {item['name']}. The
selected full-lifecycle route is `{item['full']}` with profile
`{item['profile']}`: {item['mode']}. It is deliberately separate from build,
configuration, and compatibility smokes.

| Stage | current target | what it does | does not establish |
| --- | --- | --- | --- |
| Build | `make {item['build']}` | builds the connector's selected stage | config load or traffic |
| Configuration | `make {item['config']}` | loads/checks the selected configuration | a sent request |
| Start | `make {item['start']}` | starts and stops the host route without full traffic | lifecycle coverage |
| Minimal runtime smoke | `make {item['runtime']}` | sends bounded runtime traffic | canonical full lifecycle |
| Full lifecycle | `make {item['full']}` | collects selected No-CRS host evidence | production, CRS, or full matrix |

## Host version and source provenance

{item['source']}

Show the prepared values before building:

```sh
make runtime-components-inventory
make runtime-components-sources
```

Relevant variables: {item['variables']}
Their format, defaults, scope, effect, and security boundary are defined in the
[central variable reference](../../configuration/variables.md). An override is
an explicit input change, not a capability upgrade.

## Toolchain and Cache-v2

{item['toolchain']}

For a clean local invocation, choose a writable parent outside the checkout.
`VERIFIED_RUN_PARENT` derives `BUILD_ROOT` and `CACHE_ROOT=.../cache-v2`. The
shared cache holds reusable inputs, not canonical evidence; do not manually
rearrange it or mix incompatible provenance.

```sh
make {item['prepare']} VERIFIED_RUN_PARENT="/srv/modsecurity-work"
make {item['build']} VERIFIED_RUN_PARENT="/srv/modsecurity-work"
```

`/srv/modsecurity-work` is an example absolute runtime path, not a repository
default. A target can end with `BLOCKED`/exit code `77` when a prerequisite is
absent.

## Build, configuration, and smoke

Run stages independently so that a failure is not mistaken for a stronger
claim:

```sh
make {item['build']}
make {item['config']}
make {item['start']}
make {item['runtime']}
```

For one selected canonical evidence run, use the same safe run identifier. The
`evidence-check` command validates already-produced artifacts only.

```sh
run_id="{slug}-core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make {item['full']}
NO_CRS_RUN_ID="$run_id" make evidence-check-{slug}
```

`NO_CRS_RUN_ID` must be a filesystem-safe token. Do not set internal
full-lifecycle profile variables to relabel a direct or compatibility run.

## Optional and historical integration notes

{item['optional']}

> Historical note: {item['historical']}

A narrowed case, `FORCE_ALL_CASES=1`, or a direct connector-subdirectory
command is diagnostic input. Only the documented target with its artifact
profile can produce canonical evidence.

## Configuration, examples, and troubleshooting

- Current connector guide: [{item['name']}](../../connectors/{slug}/README.md)
- Configuration details:
  [connector configuration](../../connectors/{slug}/configuration.md)
- Repository examples: [examples/{slug}](../../../examples/{slug}/README.md)
- Test and evidence boundaries: [test levels](../../testing/README.md) ·
  [evidence rules](../../evidence/README.md)

{item['trouble']}

Do not put unsanitized cookies, authorization values, tokens, private keys, or
raw logs into configuration, issues, or evidence.

## Evidence boundary

This text does not claim production readiness, complete CRS coverage, HTTP/2
or HTTP/3 support, a full matrix, or strict post-commit intervention. A PASS
applies only to the target actually executed, its documented host profile, and
its sanitized run-specific evidence set.
"""


def write(name: str, content: str) -> None:
    path = OUTPUT / name
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    write("README.md", overview(False))
    write("README.de.md", overview(True))
    write("overview.md", open_connector_overview(False))
    write("overview.de.md", open_connector_overview(True))
    for item in CONNECTORS:
        write(f"{item['slug']}.md", guide(item, False))
        write(f"{item['slug']}.de.md", guide(item, True))


if __name__ == "__main__":
    main()
