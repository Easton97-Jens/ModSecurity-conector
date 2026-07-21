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


# The fields below are the source of truth for the detailed three-path guides.
# Technical values (targets, package names, pins, variables, and status) are
# shared by both language renderings.  Only explanatory prose is translated.
PACKAGE_STATUSES = {
    "package-only",
    "package-assisted source build",
    "selected profile not available package-only",
}

BASE_DEBIAN = ("build-essential", "pkg-config", "git", "curl", "ca-certificates")
BASE_FEDORA = ("gcc", "gcc-c++", "make", "pkgconf-pkg-config", "git", "curl", "ca-certificates")

DETAILS: dict[str, dict[str, object]] = {
    "apache": {
        "package_status": "package-assisted source build",
        "extra_prepare": "",
        "host_source": "source",
        "test_prerequisites": (
            "Git, a writable external parent, C/C++ build tools, and the Framework submodule. The preparation route stages Apache, APR, APR-util, PCRE2, and libmodsecurity inputs.",
            "Git, ein beschreibbarer externer Stamm, C/C++-Buildtools und das Framework-Submodule. Der Vorbereitungsweg staged Eingaben für Apache, APR, APR-util, PCRE2 und libmodsecurity.",
        ),
        "source_prerequisites": (
            "APXS, httpd headers, and the executed httpd binary must come from one selected Apache build. The supported Framework preparer owns the exact upstream configure command and its external staging.",
            "APXS, httpd-Header und das ausgeführte httpd-Binary müssen aus einem ausgewählten Apache-Build stammen. Der unterstützte Framework-Vorbereiter besitzt den exakten Upstream-Configure-Befehl und sein externes Staging.",
        ),
        "source_commands": (
            "BUILD_HTTPD_FROM_SOURCE=1 MAKE_JOBS=\"$jobs\" make build-apache",
            "make check-config-apache",
            "make start-smoke-apache",
            "make runtime-smoke-apache",
            "NO_CRS_RUN_ID=\"$run_id\" make full-lifecycle-apache",
        ),
        "source_validation": (
            "make check-config-apache",
            "make start-smoke-apache",
            "make runtime-smoke-apache",
            "NO_CRS_RUN_ID=\"$run_id\" make evidence-check-apache",
        ),
        "pins": (
            ("Apache HTTP Server", "2.4.68 (`HTTPD_VERSION`)", "https://downloads.apache.org/httpd/httpd-2.4.68.tar.bz2", "SHA256 `68c74d4df38c26bed4dfbdb8f3baf1eb532f3872357becc1bba5d136f6b63c06`"),
            ("APR", "1.7.6 (`APR_VERSION`)", "https://downloads.apache.org/apr/apr-1.7.6.tar.bz2", "SHA256 `49030d92d2575da735791b496dc322f3ce5cff9494779ba8cc28c7f46c5deb32`"),
            ("APR-util", "1.6.3 (`APR_UTIL_VERSION`)", "https://downloads.apache.org/apr/apr-util-1.6.3.tar.bz2", "SHA256 `a41076e3710746326c3945042994ad9a4fcac0ce0277dd8fea076fec3c9772b5`"),
            ("PCRE2", "10.47 (`PCRE2_VERSION`)", "https://github.com/PCRE2Project/pcre2/releases/download/pcre2-10.47/pcre2-10.47.tar.bz2", "effective source identity is recorded by preparation"),
            ("libmodsecurity", "configured `MODSECURITY_GIT_REF` (default `v3/master`)", "https://github.com/owasp-modsecurity/ModSecurity.git", "resolved commit is recorded in Cache-v2 provenance"),
        ),
        "abi": (
            "`APXS_BIN`, `APACHE_BIN`, and the executed httpd binary must belong to the same Apache ABI. The module path and `LoadModule` entry are generated and checked by the selected route; do not combine distribution headers with another httpd build.",
            "`APXS_BIN`, `APACHE_BIN` und das ausgeführte httpd-Binary müssen zu derselben Apache-ABI gehören. Modulpfad und `LoadModule`-Eintrag werden vom ausgewählten Weg erzeugt und geprüft; Distributionsheader nicht mit einem anderen httpd-Build kombinieren.",
        ),
        "config": (
            "The config target is the supported httpd config test for the generated selected host configuration.",
            "Das Config-Target ist der unterstützte httpd-Config-Test für die erzeugte Konfiguration des ausgewählten Hosts.",
        ),
        "package_debian": ("autoconf", "automake", "libtool", "libpcre2-dev", "libssl-dev", "libmodsecurity-dev", "apache2", "apache2-dev"),
        "package_fedora": ("autoconf", "automake", "libtool", "pcre2-devel", "openssl-devel", "libmodsecurity-devel", "httpd", "httpd-devel"),
        "package_notes": (
            "Host and APXS packages can assist development, but the repository native module is still built from source against that exact host. A distribution ModSecurity-v2 Apache module is not this libmodsecurity-v3 route.",
            "Host- und APXS-Pakete können die Entwicklung unterstützen, aber das repository-eigene native Modul wird weiterhin aus Source gegen genau diesen Host gebaut. Ein distributionsseitiges ModSecurity-v2-Apache-Modul ist nicht dieser libmodsecurity-v3-Weg.",
        ),
        "cleanup": ("sudo apt remove apache2 apache2-dev", "sudo dnf remove httpd httpd-devel"),
        "vars": (
            ("BUILD_HTTPD_FROM_SOURCE", "0", "1", "Opt in to the Framework-managed Apache source host.", "Opt-in für den Framework-gesteuerten Apache-Source-Host."),
            ("APACHE_BIN", "host discovery or preparation", "external selected httpd path", "Apache executable that must match APXS and module headers.", "Apache-Executable, das zu APXS und Modulheadern passen muss."),
            ("APACHECTL_BIN", "host discovery or preparation", "external selected apachectl path", "Optional apachectl-compatible control command for the same host.", "Optionaler apachectl-kompatibler Steuerbefehl für denselben Host."),
            ("APXS_BIN", "host discovery or preparation", "external selected APXS path", "APXS used to compile the module for the selected httpd.", "APXS zum Kompilieren des Moduls für das ausgewählte httpd."),
        ),
    },
    "nginx": {
        "package_status": "package-assisted source build",
        "extra_prepare": "",
        "host_source": "source",
        "test_prerequisites": (
            "Git, a writable external parent, C/C++ build tools, and the Framework submodule. The selected NGINX and libmodsecurity sources are prepared below the external work root.",
            "Git, ein beschreibbarer externer Stamm, C/C++-Buildtools und das Framework-Submodule. Die ausgewählten NGINX- und libmodsecurity-Quellen werden unter dem externen Arbeitsstamm vorbereitet.",
        ),
        "source_prerequisites": (
            "The module must use the exact NGINX source, configure arguments, prefix, and ABI selected by the Framework. The preparer writes the supported configure invocation to external provenance; no second untested manual configure command is invented here.",
            "Das Modul muss genau die vom Framework ausgewählten NGINX-Quellen, Configure-Argumente, Prefix und ABI verwenden. Der Vorbereiter schreibt den unterstützten Configure-Aufruf in externe Provenienz; hier wird kein zweiter ungetesteter manueller Configure-Befehl erfunden.",
        ),
        "source_commands": (
            "BUILD_NGINX_FROM_SOURCE=1 NGINX_SOURCE_MODE=github-release MAKE_JOBS=\"$jobs\" make build-nginx",
            "make check-config-nginx",
            "make start-smoke-nginx",
            "make runtime-smoke-nginx",
            "NO_CRS_RUN_ID=\"$run_id\" make full-lifecycle-nginx",
        ),
        "source_validation": (
            "make check-config-nginx",
            "make start-smoke-nginx",
            "make runtime-smoke-nginx",
            "NO_CRS_RUN_ID=\"$run_id\" make evidence-check-nginx",
        ),
        "pins": (
            ("NGINX", "release-1.31.2 (`NGINX_SOURCE_GIT_REF`)", "https://github.com/nginx/nginx", "release-tag provenance; no configured archive SHA256"),
            ("libmodsecurity", "configured `MODSECURITY_GIT_REF` (default `v3/master`)", "https://github.com/owasp-modsecurity/ModSecurity.git", "resolved commit is recorded in Cache-v2 provenance"),
        ),
        "abi": (
            "A dynamic NGINX module must match the exact host build, configure arguments, prefix, and module ABI. A module from another distribution or build can be binary-incompatible.",
            "Ein dynamisches NGINX-Modul muss exakt zu Host-Build, Configure-Argumenten, Prefix und Modul-ABI passen. Ein Modul aus einer anderen Distribution oder einem anderen Build kann binär inkompatibel sein.",
        ),
        "config": (
            "The selected config target performs the repository-managed equivalent of `nginx -t`, including the selected module and prefix.",
            "Das ausgewählte Config-Target führt das repository-gesteuerte Äquivalent zu `nginx -t` einschließlich ausgewähltem Modul und Prefix aus.",
        ),
        "package_debian": ("libpcre2-dev", "zlib1g-dev", "libssl-dev", "libmodsecurity-dev", "nginx", "nginx-dev"),
        "package_fedora": ("pcre2-devel", "zlib-devel", "openssl-devel", "libmodsecurity-devel", "nginx"),
        "package_notes": (
            "Packages can supply a host and development libraries, but do not automatically provide a compatible repository module. Fedora NGINX development-package availability is release-dependent; query it before adding a package name.",
            "Pakete können Host und Entwicklungsbibliotheken liefern, stellen aber nicht automatisch ein kompatibles repository-eigenes Modul bereit. Die Verfügbarkeit eines Fedora-NGINX-Entwicklungspakets ist releaseabhängig; vor einem zusätzlichen Paketnamen abfragen.",
        ),
        "cleanup": ("sudo apt remove nginx nginx-dev", "sudo dnf remove nginx"),
        "vars": (
            ("BUILD_NGINX_FROM_SOURCE", "1", "1", "Require the Framework-managed NGINX source build.", "Erfordert den Framework-gesteuerten NGINX-Source-Build."),
            ("NGINX_SOURCE_MODE", "github-release", "github-release", "Supported NGINX source acquisition mode.", "Unterstützter NGINX-Quellbezugmodus."),
            ("NGINX_SOURCE_REPO_URL", "Framework default", "https://github.com/nginx/nginx", "HTTPS GitHub repository used for release acquisition.", "HTTPS-GitHub-Repository für den Release-Bezug."),
            ("NGINX_SOURCE_GIT_REF", "release-1.31.2", "release-1.31.2", "Selected NGINX Git reference; provenance is authoritative.", "Ausgewählte NGINX-Git-Referenz; die Provenienz ist maßgeblich."),
            ("NGINX_RELEASE_TAG", "release-1.31.2", "release-1.31.2", "Requested NGINX release tag; preparation records the resolved release provenance.", "Angefragtes NGINX-Release-Tag; die Vorbereitung protokolliert die aufgelöste Release-Provenienz."),
            ("NGINX_BIN", "resolved by preparation", "external selected nginx path", "NGINX executable paired with the selected dynamic module.", "NGINX-Executable, das mit dem ausgewählten dynamischen Modul zusammengehört."),
            ("NGINX_PREFIX", "generated external staging prefix", "external staging prefix", "Host prefix that must remain paired with the module ABI.", "Host-Prefix, der mit der Modul-ABI zusammenbleiben muss."),
            ("NGINX_MODULE", "generated module path", "external module path", "Generated native module path loaded by selected configuration.", "Erzeugter nativer Modulpfad der ausgewählten Konfiguration."),
        ),
    },
    "haproxy": {
        "package_status": "package-assisted source build",
        "extra_prepare": "",
        "host_source": "source",
        "test_prerequisites": (
            "Git, a writable external parent, C/C++ build tools, libmodsecurity inputs, and the Framework submodule. The selected HAProxy source is provisioned with the pin below.",
            "Git, ein beschreibbarer externer Stamm, C/C++-Buildtools, libmodsecurity-Eingaben und das Framework-Submodule. Die ausgewählte HAProxy-Quelle wird mit dem untenstehenden Pin provisioniert.",
        ),
        "source_prerequisites": (
            "The canonical host path builds a native HTX overlay against Framework-provisioned HAProxy source and libmodsecurity headers/libraries. The root full-lifecycle target is the supported source command because it passes verified source, build root, rules, and event paths together.",
            "Der kanonische Hostweg baut ein natives HTX-Overlay gegen vom Framework provisionierte HAProxy-Quelle sowie libmodsecurity-Header/-Bibliotheken. Das Root-Full-Lifecycle-Target ist der unterstützte Source-Befehl, weil es verifizierte Quelle, Build-Root, Regeln und Eventpfade zusammen übergibt.",
        ),
        "source_commands": (
            "MAKE_JOBS=\"$jobs\" make build-haproxy",
            "make check-config-haproxy",
            "make start-smoke-haproxy",
            "make runtime-smoke-haproxy",
            "NO_CRS_RUN_ID=\"$run_id\" make full-lifecycle-haproxy-htx",
        ),
        "source_validation": (
            "make check-config-haproxy",
            "NO_CRS_RUN_ID=\"$run_id\" make evidence-check-haproxy",
        ),
        "pins": (
            ("HAProxy", "3.2.21 (`HAPROXY_VERSION`)", "https://www.haproxy.org/download/3.2/src/haproxy-3.2.21.tar.gz", "SHA256 `0cb8818a26c5f888e0cb1c40f1b3acb9fb952527d1733f769ce688fedd680339`"),
            ("libmodsecurity", "configured `MODSECURITY_GIT_REF` (default `v3/master`)", "https://github.com/owasp-modsecurity/ModSecurity.git", "resolved commit is recorded in Cache-v2 provenance"),
        ),
        "abi": (
            "The SPOA/SPOP compatibility route and a package-host smoke are separate diagnostics. They do not replace the selected native HTX overlay, its source/build flags, or its `haproxy -c` parser check.",
            "Der SPOA/SPOP-Kompatibilitätsweg und ein Package-Host-Smoke sind getrennte Diagnosen. Sie ersetzen weder das ausgewählte native HTX-Overlay noch dessen Source-/Buildflags oder dessen `haproxy -c`-Parsercheck.",
        ),
        "config": (
            "The config stage validates repository configuration; the selected full lifecycle additionally builds and validates the native HTX host overlay.",
            "Die Config-Stufe validiert die Repository-Konfiguration; der ausgewählte Full-Lifecycle baut und validiert zusätzlich das native HTX-Host-Overlay.",
        ),
        "package_debian": ("libpcre2-dev", "zlib1g-dev", "libssl-dev", "libmodsecurity-dev", "haproxy"),
        "package_fedora": ("pcre2-devel", "zlib-devel", "openssl-devel", "libmodsecurity-devel", "haproxy"),
        "package_notes": (
            "A HAProxy package and dependencies can assist local work, but no ordinary package supplies the selected native HTX filter plus matching source overlay. It is not a package-only substitute.",
            "Ein HAProxy-Paket und Abhängigkeiten können lokale Arbeit unterstützen, aber kein gewöhnliches Paket liefert den ausgewählten nativen HTX-Filter samt passendem Source-Overlay. Es ist kein package-only-Ersatz.",
        ),
        "cleanup": ("sudo apt remove haproxy", "sudo dnf remove haproxy"),
        "vars": (
            ("HAPROXY_VERSION", "3.2.21", "3.2.21", "Pinned HAProxy source version for selected overlay.", "Gepinnte HAProxy-Source-Version für das ausgewählte Overlay."),
            ("HAPROXY_SOURCE_URL", "Framework default", "official HAProxy source URL", "Source URL verified by preparation.", "Von der Vorbereitung verifizierte Source-URL."),
            ("HAPROXY_SHA256", "Framework default", "pinned SHA256", "Integrity input for selected HAProxy archive.", "Integritätseingabe für das ausgewählte HAProxy-Archiv."),
            ("HAPROXY_SOURCE_DIR", "generated external source directory", "external HAProxy source directory", "Provisioned source for native HTX overlay.", "Provisionierte Quelle für das native HTX-Overlay."),
            ("HAPROXY_BIN", "resolved by preparation", "external HTX haproxy path", "HAProxy executable used by the selected HTX runtime.", "HAProxy-Executable des ausgewählten HTX-Runtimewegs."),
            ("HAPROXY_HTX_RUNTIME_ROOT", "derived below BUILD_ROOT", "external HTX runtime directory", "Runtime, event, and overlay files for the selected HTX route.", "Runtime-, Event- und Overlaydateien des ausgewählten HTX-Wegs."),
            ("HAPROXY_HTX_BUILD_DIR", "derived external overlay directory", "external overlay build directory", "Native HTX overlay build location outside checkout.", "Buildort des nativen HTX-Overlays außerhalb des Checkouts."),
        ),
    },
    "envoy": {
        "package_status": "package-assisted source build",
        "extra_prepare": "prepare-envoy-runtime",
        "host_source": "verified binary; service source",
        "go_requirement": "1.26",
        "go_module": "connectors/envoy/ext_proc/go.mod",
        "test_prerequisites": (
            "Git, a writable external parent, Go and C/C++ build tools, libmodsecurity inputs, and the Framework submodule. The specific preparation target obtains only the pinned host binary through repository policy.",
            "Git, ein beschreibbarer externer Stamm, Go- und C/C++-Buildtools, libmodsecurity-Eingaben und das Framework-Submodule. Das spezifische Vorbereitungstarget beschafft das gepinnte Hostbinary ausschließlich über die Repository-Richtlinie.",
        ),
        "source_prerequisites": (
            "The repository builds the ext_proc service, CGo/Common bridge, and generated configuration from source. It does not maintain a tested full Envoy-host source build, so a verified pinned binary is used instead of an invented manual host build.",
            "Das Repository baut ext_proc-Service, CGo/Common-Bridge und erzeugte Konfiguration aus Source. Es pflegt keinen getesteten vollständigen Envoy-Host-Source-Build; daher wird ein verifiziertes gepinntes Binary statt eines erfundenen manuellen Host-Builds verwendet.",
        ),
        "source_commands": (
            "MAKE_JOBS=\"$jobs\" make -C connectors/envoy build-envoy-ext-proc",
            "MAKE_JOBS=\"$jobs\" make -C connectors/envoy test-envoy-ext-proc",
            "MAKE_JOBS=\"$jobs\" make -C connectors/envoy check-envoy-ext-proc-config",
            "NO_CRS_RUN_ID=\"$run_id\" make full-lifecycle-envoy-ext-proc",
        ),
        "source_validation": (
            "go version",
            "grep -Ex 'go 1\\.26\\.[0-9]+' connectors/envoy/ext_proc/go.mod",
            "make -C connectors/envoy check-envoy-ext-proc-config",
            "NO_CRS_RUN_ID=\"$run_id\" make evidence-check-envoy",
        ),
        "pins": (
            ("Envoy host binary", "1.38.2 (`ENVOY_VERSION`)", "https://github.com/envoyproxy/envoy/releases/download/v1.38.2/envoy-1.38.2-linux-x86_64", "SHA256 `87744a1fc998d677078c9703113a192d0830badc6888662441632847fcb38899`"),
            ("repository ext_proc service", "current checkout commit", "connectors/envoy", "Git commit plus external build provenance"),
            ("libmodsecurity", "configured `MODSECURITY_GIT_REF` (default `v3/master`)", "https://github.com/owasp-modsecurity/ModSecurity.git", "resolved commit is recorded in Cache-v2 provenance"),
        ),
        "abi": (
            "The Envoy binary is a verified host input; the ext_proc executable is the repository-owned source build. Generated configuration, ports, CGo bridge, and libmodsecurity runtime library must stay in one external invocation root.",
            "Das Envoy-Binary ist eine verifizierte Hosteingabe; das ext_proc-Executable ist der repository-eigene Source-Build. Erzeugte Konfiguration, Ports, CGo-Bridge und libmodsecurity-Laufzeitbibliothek müssen in einem externen Invocation-Root bleiben.",
        ),
        "config": (
            "The config target checks the repository service and generated Envoy ext_proc configuration; it does not declare a system Envoy package equivalent.",
            "Das Config-Target prüft Repository-Service und erzeugte Envoy-ext_proc-Konfiguration; es erklärt kein System-Envoy-Paket für gleichwertig.",
        ),
        "package_debian": ("golang-go", "protobuf-compiler", "libprotobuf-dev", "libgrpc-dev", "libmodsecurity-dev"),
        "package_fedora": ("golang", "protobuf-devel", "grpc-devel", "libmodsecurity-devel"),
        "package_host_query": ("apt-cache search '^envoy$'", "dnf search envoy"),
        "package_notes": (
            "Checked package names cover build dependencies, not an equivalent selected Envoy host. Any distribution Envoy package still lacks the repository ext_proc service and must be verified separately.",
            "Geprüfte Paketnamen decken Buildabhängigkeiten ab, nicht einen gleichwertigen ausgewählten Envoy-Host. Jedes Distributions-Envoy-Paket enthält weiterhin nicht den repository-eigenen ext_proc-Service und muss separat geprüft werden.",
        ),
        "cleanup": ("sudo apt remove golang-go protobuf-compiler libprotobuf-dev libgrpc-dev", "sudo dnf remove golang protobuf-devel grpc-devel"),
        "vars": (
            ("ENVOY_BIN", "generated external cache binary", "verified external Envoy binary", "Resolved host binary for pinned Envoy release.", "Aufgelöstes Hostbinary für den gepinnten Envoy-Release."),
            ("EXT_PROC_CONFIG", "connector configuration file", "connector ext_proc configuration", "Repository ext_proc service config used by checks.", "Repository-ext_proc-Servicekonfiguration für Checks."),
            ("EXT_PROC_RUNTIME_CONFIG", "derived external runtime file", "external runtime config", "Generated selected ext_proc runtime configuration.", "Erzeugte Laufzeitkonfiguration des ausgewählten ext_proc-Wegs."),
            ("EXT_PROC_RUNTIME_ROOT", "derived under BUILD_ROOT", "external ext_proc runtime directory", "Runtime files and event logs for ext_proc.", "Laufzeitdateien und Eventlogs von ext_proc."),
            ("RULES_FILE", "connector default", "absolute rules file", "Rules-file input for local connector diagnostics; canonical runs provide their own selected rules.", "Rules-Datei für lokale Connector-Diagnosen; kanonische Runs liefern ihre eigenen ausgewählten Regeln."),
            ("MSCONNECTOR_RULES_FILE", "unset", "absolute no-CRS rules file", "Canonical rule input when the selected runtime exports it.", "Kanonische Regeleingabe, wenn die ausgewählte Runtime sie exportiert."),
            ("ENVOY_TRANSPORT_CANCEL_PROBE", "0", "1", "Opt-in cancellation probe; it is not a client-visible strict-reset claim.", "Opt-in-Cancellation-Probe; kein Claim über einen client-sichtbaren strikten Reset."),
        ),
    },
    "traefik": {
        "package_status": "package-assisted source build",
        "extra_prepare": "prepare-traefik-runtime",
        "host_source": "verified binary; middleware/service source",
        "go_requirement": "1.26",
        "go_module": "connectors/traefik/native_middleware/go.mod",
        "test_prerequisites": (
            "Git, a writable external parent, Go and C/C++ build tools, libmodsecurity inputs, and the Framework submodule. Runtime preparation supplies the pinned host binary through provenance policy.",
            "Git, ein beschreibbarer externer Stamm, Go- und C/C++-Buildtools, libmodsecurity-Eingaben und das Framework-Submodule. Die Runtime-Vorbereitung liefert das gepinnte Hostbinary über die Provenienzrichtlinie.",
        ),
        "source_prerequisites": (
            "The native middleware and private UDS engine service are repository source builds using Go, CGo/Common, and libmodsecurity. The selected Traefik host is a verified release binary, not presented as a maintained full host source build.",
            "Die native Middleware und der private UDS-Engine-Service sind Repository-Source-Builds mit Go, CGo/Common und libmodsecurity. Der ausgewählte Traefik-Host ist ein verifiziertes Releasebinary und wird nicht als gepflegter vollständiger Host-Source-Build dargestellt.",
        ),
        "source_commands": (
            "MAKE_JOBS=\"$jobs\" make -C connectors/traefik build-native-middleware",
            "MAKE_JOBS=\"$jobs\" make -C connectors/traefik test-native-middleware",
            "MAKE_JOBS=\"$jobs\" make -C connectors/traefik build-engine-service",
            "MAKE_JOBS=\"$jobs\" make -C connectors/traefik test-engine-service",
            "NO_CRS_RUN_ID=\"$run_id\" make full-lifecycle-traefik-native",
        ),
        "source_validation": (
            "go version",
            "grep -Ex 'go 1\\.26\\.[0-9]+' connectors/traefik/native_middleware/go.mod",
            "make -C connectors/traefik test-engine-service",
            "NO_CRS_RUN_ID=\"$run_id\" make evidence-check-traefik",
        ),
        "pins": (
            ("Traefik host binary", "3.7.5 (`TRAEFIK_VERSION`)", "https://github.com/traefik/traefik/releases/download/v3.7.5/traefik_v3.7.5_linux_amd64.tar.gz", "SHA256 `9da81a928fde965c2c4678698bbc28bc3f600223b14c32b35bd480bf5ec863dc`"),
            ("native middleware and engine service", "current checkout commit", "connectors/traefik", "Git commit plus external build provenance"),
            ("libmodsecurity", "configured `MODSECURITY_GIT_REF` (default `v3/master`)", "https://github.com/owasp-modsecurity/ModSecurity.git", "resolved commit is recorded in Cache-v2 provenance"),
        ),
        "abi": (
            "The host binary, local plugin, File Provider configuration, UDS permissions, engine service, and libmodsecurity runtime library are one invocation-local set. A standard host package does not include native middleware or its engine service.",
            "Hostbinary, lokales Plugin, File-Provider-Konfiguration, UDS-Berechtigungen, Engine-Service und libmodsecurity-Laufzeitbibliothek sind ein invocation-lokaler Satz. Ein Standardhostpaket enthält weder native Middleware noch ihren Engine-Service.",
        ),
        "config": (
            "The config target checks repository connector configuration. The selected native full lifecycle separately starts the pinned host with local plugin and UDS engine; forwardAuth compatibility is not a substitute.",
            "Das Config-Target prüft die Repository-Connectorkonfiguration. Der ausgewählte native Full-Lifecycle startet den gepinnten Host getrennt mit lokalem Plugin und UDS-Engine; ForwardAuth-Kompatibilität ist kein Ersatz.",
        ),
        "package_debian": ("golang-go", "libmodsecurity-dev"),
        "package_fedora": ("golang", "libmodsecurity-devel"),
        "package_host_query": ("apt-cache search '^traefik$'", "dnf search traefik"),
        "package_notes": (
            "Packages provide build dependencies only. A standard Traefik package or unrelated release binary does not contain the repository-native middleware or persistent UDS engine service.",
            "Pakete liefern nur Buildabhängigkeiten. Ein Standard-Traefik-Paket oder unabhängiges Releasebinary enthält nicht die repository-native Middleware oder den persistenten UDS-Engine-Service.",
        ),
        "cleanup": ("sudo apt remove golang-go", "sudo dnf remove golang"),
        "vars": (
            ("TRAEFIK_BIN", "generated external cache binary", "verified external Traefik binary", "Resolved pinned Traefik host binary.", "Aufgelöstes gepinntes Traefik-Hostbinary."),
            ("TRAEFIK_NATIVE_RUNTIME_ROOT", "derived under BUILD_ROOT", "external native runtime directory", "Invocation-local native middleware files.", "Invocationslokale Native-Middleware-Dateien."),
            ("TRAEFIK_CONNECTOR_CONFIG", "connector configuration file", "connector configuration file", "Repository connector configuration.", "Repository-Connectorkonfiguration."),
            ("TRAEFIK_ENGINE_SERVICE_BIN", "derived external executable", "external engine-service executable", "Repository-built private UDS engine service.", "Repository-gebauter privater UDS-Engine-Service."),
            ("MSCONNECTOR_RULES_FILE", "unset", "absolute no-CRS rules file", "Canonical rule input for the selected native runtime when exported by the dispatcher.", "Kanonische Regeleingabe für die ausgewählte native Runtime, wenn der Dispatcher sie exportiert."),
            ("TRAEFIK_ENGINE_SERVICE_CFLAGS", "unset", "-O2 -g", "Optional C flags for the C/C++ engine-service build only.", "Optionale C-Flags nur für den C/C++-Engine-Service-Build."),
            ("TRAEFIK_ENGINE_SERVICE_LDFLAGS", "unset", "-L/opt/modsecurity-connector/lib", "Optional linker flags for the engine service only.", "Optionale Linkerflags nur für den Engine-Service."),
        ),
    },
    "lighttpd": {
        "package_status": "selected profile not available package-only",
        "extra_prepare": "prepare-lighttpd-runtime-build",
        "host_source": "patched source",
        "test_prerequisites": (
            "Git, a writable external parent, C/C++ build tools, patch/build prerequisites, libmodsecurity inputs, and the Framework submodule. The explicit lighttpd preparation target enables the pinned source-build route.",
            "Git, ein beschreibbarer externer Stamm, C/C++-Buildtools, Patch-/Buildvoraussetzungen, libmodsecurity-Eingaben und das Framework-Submodule. Das explizite lighttpd-Vorbereitungstarget aktiviert den gepinnten Source-Build-Weg.",
        ),
        "source_prerequisites": (
            "The selected route needs lighttpd-1.4.84 source, the repository patchset, a patched core, and a module built against matching headers. The root targets own patch check/application, configuration, staging, and real-host execution.",
            "Der ausgewählte Weg benötigt lighttpd-1.4.84-Source, das Repository-Patchset, einen gepatchten Core und ein Modul gegen passende Header. Die Root-Targets besitzen Patchprüfung/-anwendung, Konfiguration, Staging und reale Hostausführung.",
        ),
        "source_commands": (
            "LIGHTTPD_MAKE_JOBS=\"$jobs\" make -C connectors/lighttpd check-lighttpd-core-patch",
            "LIGHTTPD_MAKE_JOBS=\"$jobs\" make -C connectors/lighttpd build-lighttpd-patched-host",
            "LIGHTTPD_MAKE_JOBS=\"$jobs\" make -C connectors/lighttpd check-lighttpd-patched-host",
            "NO_CRS_RUN_ID=\"$run_id\" make full-lifecycle-lighttpd-patched",
        ),
        "source_validation": (
            "make -C connectors/lighttpd check-lighttpd-patched-host",
            "NO_CRS_RUN_ID=\"$run_id\" make evidence-check-lighttpd",
        ),
        "pins": (
            ("lighttpd host source", "1.4.84 (`LIGHTTPD_VERSION`)", "https://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-1.4.84.tar.xz", "SHA256 `076dd43bec8f2ba9ce6db7e7ca7e8ad72271cd529805ead2400b56efaa026f70`"),
            ("repository patchset", "current checkout commit", "connectors/lighttpd/patches", "Git commit plus patch-check provenance"),
            ("libmodsecurity", "configured `MODSECURITY_GIT_REF` (default `v3/master`)", "https://github.com/owasp-modsecurity/ModSecurity.git", "resolved commit is recorded in Cache-v2 provenance"),
        ),
        "abi": (
            "The selected host is not stock lighttpd. Patch verification/application, core build, module build, Entity-Body hook, and module/header ABI are one source set. Do not load the module into a stock binary built from different headers.",
            "Der ausgewählte Host ist kein Stock-lighttpd. Patchprüfung/-anwendung, Core-Build, Modul-Build, Entity-Body-Hook und Modul-/Header-ABI sind ein Sourcesatz. Das Modul nicht in ein Stock-Binary mit anderen Headern laden.",
        ),
        "config": (
            "The config target performs the repository-managed lighttpd config check; the selected patched full lifecycle additionally checks the patched host before real requests.",
            "Das Config-Target führt den repository-gesteuerten lighttpd-Config-Check aus; der ausgewählte gepatchte Full-Lifecycle prüft zusätzlich den gepatchten Host vor realen Requests.",
        ),
        "package_debian": ("libpcre2-dev", "zlib1g-dev", "libssl-dev", "libmodsecurity-dev", "lighttpd"),
        "package_fedora": ("pcre2-devel", "zlib-devel", "openssl-devel", "libmodsecurity-devel", "lighttpd"),
        "package_notes": (
            "A lighttpd package can supply a comparison host and dependencies, but not the repository Entity-Body hook or matching patched core. It cannot be the selected profile package-only.",
            "Ein lighttpd-Paket kann Vergleichshost und Abhängigkeiten liefern, aber nicht den Repository-Entity-Body-Hook oder den passenden gepatchten Core. Es kann nicht package-only das ausgewählte Profil sein.",
        ),
        "cleanup": ("sudo apt remove lighttpd", "sudo dnf remove lighttpd"),
        "vars": (
            ("LIGHTTPD_BIN", "generated external host binary", "external patched lighttpd binary", "Pinned host binary for selected patched route.", "Gepinntes Hostbinary für den ausgewählten gepatchten Weg."),
            ("LIGHTTPD_SOURCE_DIR", "generated external source directory", "external lighttpd-1.4.84 source directory", "Staged source for patch and module steps.", "Gestagte Quelle für Patch- und Modulschritte."),
            ("LIGHTTPD_BUILD_ROOT", "derived external build directory", "external patched-core build directory", "Patched core build root outside checkout.", "Gepatchter Core-Build-Root außerhalb des Checkouts."),
            ("LIGHTTPD_INCLUDE_DIR", "derived from source", "external lighttpd source include directory", "Header directory that must match the patched host and connector module.", "Headerverzeichnis, das zu gepatchtem Host und Connectormodul passen muss."),
            ("LIGHTTPD_MODULE_DIR", "derived external module directory", "external module directory", "Module location for patched host ABI.", "Modulort für die gepatchte Host-ABI."),
            ("LIGHTTPD_PATCHED_ROOT", "derived below BUILD_ROOT", "external patched-host root", "Absolute external root containing patched source, build, and staging directories.", "Absoluter externer Root mit gepatchter Quelle, Build- und Stagingverzeichnissen."),
            ("LIGHTTPD_MAKE_JOBS", "2", "2", "Parallelism for the patched lighttpd core build; reduce it on memory-constrained hosts.", "Parallelität für den gepatchten lighttpd-Core-Build; bei wenig RAM reduzieren."),
            ("ALLOW_RUNTIME_BUILDS", "0", "1", "Explicit opt-in for lighttpd source-build preparation.", "Explizites Opt-in für die lighttpd-Source-Build-Vorbereitung."),
        ),
    },
}

# Keep the requested structured command fields in the data model, while the
# common root-target sequence remains derived from the canonical connector map.
for _connector in CONNECTORS:
    _detail = DETAILS[str(_connector["slug"])]
    _detail["test_commands"] = (
        f"make {_connector['build']}",
        f"make {_connector['config']}",
        f"make {_connector['start']}",
        f"make {_connector['runtime']}",
        f'NO_CRS_RUN_ID="$run_id" make {_connector["full"]}',
        f'NO_CRS_RUN_ID="$run_id" make evidence-check-{_connector["slug"]}',
    )
    _detail["package_validation"] = (
        "pkg-config --exists libmodsecurity",
        "pkg-config --atleast-version=3.0 libmodsecurity",
        "pkg-config --modversion libmodsecurity",
        "pkg_version=\"$(pkg-config --modversion libmodsecurity)\"",
        "case \"$pkg_version\" in 3.*) ;; *) printf '%s\\n' \"libmodsecurity major version must be 3: $pkg_version\" >&2; exit 1 ;; esac",
        "pkg-config --cflags libmodsecurity",
        "pkg-config --libs libmodsecurity",
        f"make {_connector['config']}",
    )
    _detail["cleanup_commands"] = _detail["cleanup"]
del _connector, _detail


def language_switch(slug: str, german: bool) -> str:
    if german:
        return f"**Sprache:** [English]({slug}.md) | Deutsch"
    return f"**Language:** English | [Deutsch]({slug}.de.md)"


def localized(value: tuple[str, str], german: bool) -> str:
    return value[1] if german else value[0]


def shell(commands: tuple[str, ...] | list[str]) -> str:
    return "```sh\n" + "\n".join(commands) + "\n```"


def markdown_table(headers: tuple[str, ...], rows: list[tuple[str, ...]]) -> str:
    return "\n".join(
        [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join("---" for _ in headers) + " |",
            *["| " + " | ".join(row) + " |" for row in rows],
        ]
    )


def packages(values: tuple[str, ...]) -> str:
    return " ".join(values)


def detail(item: dict[str, str]) -> dict[str, object]:
    result = DETAILS[item["slug"]]
    status = str(result["package_status"])
    if status not in PACKAGE_STATUSES:
        raise ValueError(f"unsupported package status for {item['slug']}: {status}")
    return result


def status_note(status: str, german: bool) -> str:
    notes = {
        "package-only": (
            "Packages have been verified as the selected compatible host, development inputs, and connector path; verify the same fact again for the target release.",
            "Pakete wurden als ausgewählter kompatibler Host, Entwicklungseingaben und Connectorweg verifiziert; für den Zielrelease erneut prüfen.",
        ),
        "package-assisted source build": (
            "Packages provide dependencies and possibly a host, while the repository connector or host integration remains a source build. Package installation alone is not selected-core evidence.",
            "Pakete liefern Abhängigkeiten und möglicherweise einen Host, während Repository-Connector oder Hostintegration ein Source-Build bleiben. Paketinstallation allein ist keine Evidence des ausgewählten Kerns.",
        ),
        "selected profile not available package-only": (
            "Packages can help with dependencies or a comparison host, but no ordinary package supplies the selected profile. Build it through the repository route.",
            "Pakete können bei Abhängigkeiten oder einem Vergleichshost helfen, aber kein gewöhnliches Paket liefert das ausgewählte Profil. Es über den Repository-Weg bauen.",
        ),
    }
    return localized(notes[status], german)


def route_comparison(item: dict[str, str], info: dict[str, object], german: bool) -> str:
    status = str(info["package_status"])
    host_source = str(info["host_source"])
    if german:
        source_text = {
            "source": "Ja, Repository-Source",
            "patched source": "Ja, gepatchte Source",
            "verified binary; service source": "Verifiziertes Binary; Service aus Source",
            "verified binary; middleware/service source": "Verifiziertes Binary; Middleware/Service aus Source",
        }[host_source]
        package_core = "Nein, nicht package-only" if status == "selected profile not available package-only" else "Nur mit Source-Anteil"
        return markdown_table(
            ("Weg", "Für wen?", "Systemweite Änderungen", "Baut Host aus Source?", "Kernpfad möglich?", "Evidence möglich?"),
            [
                ("Repository-Testweg", "Entwicklung und CI", "Nein", "Repository-gesteuert", "Ja", "Ja, nach Full Lifecycle"),
                ("Lokaler Source-Build", "Entwicklung und Integration", "Optional", source_text, "Ja", "Ja, nur ausgewählter Run"),
                ("Paketweg", "Schneller lokaler Einstieg", "Ja", "Meist nein", package_core, "Nur passendes Profil und Run"),
            ],
        )
    source_text = {
        "source": "Yes, repository source",
        "patched source": "Yes, patched source",
        "verified binary; service source": "Verified binary; service from source",
        "verified binary; middleware/service source": "Verified binary; middleware/service from source",
    }[host_source]
    package_core = "No, not package-only" if status == "selected profile not available package-only" else "Only with source portion"
    return markdown_table(
        ("Path", "For whom?", "System-wide changes", "Builds host from source?", "Core path possible?", "Evidence possible?"),
        [
            ("Repository test path", "Development and CI", "No", "Repository-controlled", "Yes", "Yes, after full lifecycle"),
            ("Local source build", "Development and integration", "Optional", source_text, "Yes", "Yes, selected run only"),
            ("Package path", "Quick local start", "Yes", "Usually no", package_core, "Only matching profile and run"),
        ],
    )


def pin_table(info: dict[str, object], german: bool) -> str:
    headers = ("Komponente", "Pin/Version", "Quelle", "Integrität/Commit") if german else ("Component", "Pin/version", "Source", "Integrity/commit")
    return markdown_table(headers, list(info["pins"]))


def common_variable_rows(german: bool) -> list[tuple[str, str, str, str, str]]:
    if german:
        return [
            ("VERIFIED_RUN_PARENT", "ja", "vom Makefile gewählt, wenn nicht gesetzt", "$HOME/modsecurity-connector-work", "Beschreibbarer externer Stamm für Build, Cache, Runtime, Logs und Evidence; außerhalb des Checkouts und ohne Secrets im Namen."),
            ("VERIFIED_RUN_ROOT", "nein", "unter VERIFIED_RUN_PARENT abgeleitet", "$HOME/modsecurity-connector-work/ModSecurity-conector-verified", "Run-gebundener externer Stamm; enthält abgeleitete Build-, Run-, Log- und Evidence-Pfade."),
            ("BUILD_ROOT", "nein", "unter dem verifizierten Run abgeleitet", "externes Build-Unterverzeichnis", "Staging- und Buildausgabe; nicht in den Git-Checkout legen."),
            ("CACHE_ROOT", "nein", "als Cache-v2 unter dem verifizierten Run abgeleitet", "externes Cache-v2-Unterverzeichnis", "Wiederverwendbare Eingaben; kein PASS und keine kanonische Evidence."),
            ("NO_CRS_RUN_ID", "für Full Lifecycle", "leer", "nginx-core-20260712T120000Z", "Dateisicherer Name eines Evidence-Runs; denselben Wert für Full Lifecycle und Evidence-Check verwenden."),
            ("CC", "nein", "Toolchain-Default", "gcc", "C-Compiler für C- und CGo-nahe Buildschritte."),
            ("CXX", "nein", "Toolchain-Default", "g++", "C++-Compiler für Abhängigkeiten, die ihn benötigen."),
            ("CFLAGS", "nein", "Toolchain-Default", "-O2 -g", "Zusätzliche C-Flags; Beispiel ist Entwicklungswert, kein Repository- oder Produktionsdefault."),
            ("CXXFLAGS", "nein", "Toolchain-Default", "-O2 -g", "Zusätzliche C++-Flags; kein Produktionsprofil."),
            ("CPPFLAGS", "nein", "leer oder Toolchain-Default", "-I/opt/modsecurity-connector/include", "Zusätzliche Include-Flags für bewusst gewählte Headerpfade."),
            ("LDFLAGS", "nein", "leer oder Toolchain-Default", "-L/opt/modsecurity-connector/lib", "Zusätzliche Linkerflags für bewusst gewählte Bibliothekspfade."),
            ("PKG_CONFIG_PATH", "nein", "Paketmanager-/Toolchain-Default", "/opt/modsecurity-connector/lib/pkgconfig", "Zusätzlicher Suchpfad für pkg-config-Metadaten; kein ABI-Ersatz."),
            ("LD_LIBRARY_PATH", "nein", "Loader-Default", "/opt/modsecurity-connector/lib", "Temporärer Suchpfad für Shared Libraries; keine globale Installation."),
            ("MAKE_JOBS", "nein", "vom Framework ermittelt", "2", "Anzahl paralleler Compilerprozesse; bei wenig RAM kleiner wählen."),
            ("HOME", "nein", "Anmeldeverzeichnis", "$HOME", "Shellwert für das Benutzerverzeichnis; keine lokale Entwicklerpfadangabe."),
            ("jobs", "nein", "nicht gesetzt", "2", "Lokale Shellvariable aus `getconf`, die an `MAKE_JOBS` übergeben wird."),
            ("run_id", "nein", "nicht gesetzt", "apache-core-20260712T120000Z", "Lokale Shellvariable, aus der `NO_CRS_RUN_ID` gesetzt wird."),
        ]
    return [
        ("VERIFIED_RUN_PARENT", "yes", "chosen by Make when unset", "$HOME/modsecurity-connector-work", "Writable external parent for build, cache, runtime, logs, and evidence; outside the checkout and without secrets in its name."),
        ("VERIFIED_RUN_ROOT", "no", "derived below VERIFIED_RUN_PARENT", "$HOME/modsecurity-connector-work/ModSecurity-conector-verified", "Run-bound external root; holds derived build, run, log, and evidence paths."),
        ("BUILD_ROOT", "no", "derived below verified run", "external build subdirectory", "Staging and build output; keep it outside the Git checkout."),
        ("CACHE_ROOT", "no", "derived as cache-v2 below verified run", "external cache-v2 subdirectory", "Reusable inputs; not a PASS and not canonical evidence."),
        ("NO_CRS_RUN_ID", "for full lifecycle", "empty", "nginx-core-20260712T120000Z", "Filesystem-safe name of one evidence run; use it for both full lifecycle and evidence check."),
        ("CC", "no", "toolchain default", "gcc", "C compiler for C and CGo-adjacent build steps."),
        ("CXX", "no", "toolchain default", "g++", "C++ compiler for dependencies that need it."),
        ("CFLAGS", "no", "toolchain default", "-O2 -g", "Additional C flags; example is a development value, not a repository or production default."),
        ("CXXFLAGS", "no", "toolchain default", "-O2 -g", "Additional C++ flags; not a production profile."),
        ("CPPFLAGS", "no", "empty or toolchain default", "-I/opt/modsecurity-connector/include", "Additional include flags for deliberately selected header paths."),
        ("LDFLAGS", "no", "empty or toolchain default", "-L/opt/modsecurity-connector/lib", "Additional linker flags for deliberately selected library paths."),
        ("PKG_CONFIG_PATH", "no", "package-manager/toolchain default", "/opt/modsecurity-connector/lib/pkgconfig", "Additional pkg-config metadata search path; not an ABI substitute."),
        ("LD_LIBRARY_PATH", "no", "loader default", "/opt/modsecurity-connector/lib", "Temporary shared-library search path; not a global installation."),
        ("MAKE_JOBS", "no", "detected by Framework", "2", "Number of parallel compiler processes; choose lower on a memory-constrained machine."),
        ("HOME", "no", "login home directory", "$HOME", "Shell value for user home directory; no local developer path."),
        ("jobs", "no", "unset", "2", "Local shell variable from `getconf`, passed to `MAKE_JOBS`."),
        ("run_id", "no", "unset", "apache-core-20260712T120000Z", "Local shell variable used to set `NO_CRS_RUN_ID`."),
    ]


def variable_table(info: dict[str, object], german: bool) -> str:
    headers = ("Variable/Platzhalter", "Pflicht", "Standard", "Beispiel", "Bedeutung") if german else ("Variable/placeholder", "Required", "Default", "Example", "Meaning")
    rows = common_variable_rows(german)
    for name, default, example, english, german_text in info["vars"]:
        rows.append((str(name), "nein" if german else "no", str(default), str(example), str(german_text if german else english)))
    return markdown_table(headers, rows)


HOST_VALIDATION: dict[str, tuple[str, ...]] = {
    "apache": (
        'test -x "$BUILD_ROOT/apache-runtime/httpd/bin/httpd"',
        '"$BUILD_ROOT/apache-runtime/httpd/bin/httpd" -v',
        'test -x "$BUILD_ROOT/apache-runtime/httpd/bin/apxs"',
        '"$BUILD_ROOT/apache-runtime/httpd/bin/apxs" -q LIBEXECDIR',
    ),
    "nginx": (
        'test -x "$BUILD_ROOT/nginx-runtime/nginx/sbin/nginx"',
        '"$BUILD_ROOT/nginx-runtime/nginx/sbin/nginx" -V',
    ),
    "haproxy": (
        'test -x "$VERIFIED_RUN_ROOT/runs/haproxy/$run_id/haproxy-host-work/runtime/overlay-build/worktree/haproxy"',
        '"$VERIFIED_RUN_ROOT/runs/haproxy/$run_id/haproxy-host-work/runtime/overlay-build/worktree/haproxy" -vv',
    ),
    "envoy": (
        'test -x "$CACHE_ROOT/shared/envoy/bin/envoy"',
        '"$CACHE_ROOT/shared/envoy/bin/envoy" --version',
    ),
    "traefik": (
        'test -x "$CACHE_ROOT/shared/traefik/bin/traefik"',
        '"$CACHE_ROOT/shared/traefik/bin/traefik" version',
    ),
    "lighttpd": (
        'test -x "$BUILD_ROOT/lighttpd-core-patched/stage/bin/lighttpd"',
        '"$BUILD_ROOT/lighttpd-core-patched/stage/bin/lighttpd" -v',
    ),
}


ARTIFACT_VALIDATION: dict[str, tuple[str, ...]] = {
    "apache": (
        'test -f "$BUILD_ROOT/apache-build/output/apache/mod_security3.so"',
        'ldd "$BUILD_ROOT/apache-build/output/apache/mod_security3.so" | grep -F libmodsecurity',
    ),
    "nginx": (
        'test -f "$BUILD_ROOT/nginx-runtime/nginx/modules/ngx_http_modsecurity_module.so"',
        'ldd "$BUILD_ROOT/nginx-runtime/nginx/modules/ngx_http_modsecurity_module.so" | grep -F libmodsecurity',
    ),
    "haproxy": (
        'test -x "$VERIFIED_RUN_ROOT/runs/haproxy/$run_id/haproxy-host-work/runtime/overlay-build/worktree/haproxy"',
        'ldd "$VERIFIED_RUN_ROOT/runs/haproxy/$run_id/haproxy-host-work/runtime/overlay-build/worktree/haproxy" | grep -F libmodsecurity',
    ),
    "envoy": (
        'test -x "$BUILD_ROOT/envoy-ext-proc/msconnector_envoy_ext_proc"',
        'ldd "$BUILD_ROOT/envoy-ext-proc/msconnector_envoy_ext_proc" | grep -F libmodsecurity',
    ),
    "traefik": (
        'test -x "$BUILD_ROOT/traefik-engine-service/traefik-engine-service"',
        'ldd "$BUILD_ROOT/traefik-engine-service/traefik-engine-service" | grep -F libmodsecurity',
    ),
    "lighttpd": (
        'test -f "$BUILD_ROOT/lighttpd-core-patched/stage/modules/mod_msconnector.so"',
        'ldd "$BUILD_ROOT/lighttpd-core-patched/stage/modules/mod_msconnector.so" | grep -F libmodsecurity',
    ),
}


# The repository test path first runs the generic build target and then the
# selected full lifecycle.  Traefik's engine service and lighttpd's patched
# host are produced only by that run-bound lifecycle, while their source and
# package-assisted paths build equivalent artifacts directly below BUILD_ROOT.
TEST_HOST_VALIDATION: dict[str, tuple[str, ...]] = {
    **HOST_VALIDATION,
    "lighttpd": (
        'test -x "$VERIFIED_RUN_ROOT/runs/lighttpd/$run_id/host-runtime/lighttpd-patched/stage/bin/lighttpd"',
        '"$VERIFIED_RUN_ROOT/runs/lighttpd/$run_id/host-runtime/lighttpd-patched/stage/bin/lighttpd" -v',
    ),
}


TEST_ARTIFACT_VALIDATION: dict[str, tuple[str, ...]] = {
    **ARTIFACT_VALIDATION,
    "traefik": (
        'test -x "$VERIFIED_RUN_ROOT/runs/traefik/$run_id/traefik-runtime/engine-build/traefik-engine-service"',
        'ldd "$VERIFIED_RUN_ROOT/runs/traefik/$run_id/traefik-runtime/engine-build/traefik-engine-service" | grep -F libmodsecurity',
    ),
    "lighttpd": (
        'test -f "$VERIFIED_RUN_ROOT/runs/lighttpd/$run_id/host-runtime/lighttpd-patched/stage/modules/mod_msconnector.so"',
        'ldd "$VERIFIED_RUN_ROOT/runs/lighttpd/$run_id/host-runtime/lighttpd-patched/stage/modules/mod_msconnector.so" | grep -F libmodsecurity',
    ),
}


def selected_preparation(item: dict[str, str], info: dict[str, object]) -> tuple[str, ...]:
    commands = ["make check-framework", "make prepare-runtime-components"]
    extra = str(info["extra_prepare"])
    if extra and extra != "prepare-runtime-components":
        commands.append(f"make {extra}")
    return tuple(commands)


def source_route_note(item: dict[str, str], german: bool) -> str:
    notes: dict[str, tuple[str, str]] = {
        "apache": (
            "`BUILD_HTTPD_FROM_SOURCE=1` delegates httpd, APR, APR-util, PCRE2, libmodsecurity, APXS, connector configuration, and external staging to the Framework preparer. It records its exact configure commands in the Apache command, source-info, and artifact records below the external build root.",
            "`BUILD_HTTPD_FROM_SOURCE=1` delegiert httpd, APR, APR-util, PCRE2, libmodsecurity, APXS, Connector-Konfiguration und externes Staging an den Framework-Vorbereiter. Er protokolliert seine exakten Configure-Befehle in den Apache-Command-, Source-Info- und Artifact-Records unterhalb des externen Build-Roots.",
        ),
        "nginx": (
            "`BUILD_NGINX_FROM_SOURCE=1` builds the selected host and dynamic module together using the Framework-recorded configure invocation, including `--with-compat` and the selected module input. Do not load that module into an unrelated package host.",
            "`BUILD_NGINX_FROM_SOURCE=1` baut ausgewählten Host und dynamisches Modul gemeinsam mit dem vom Framework protokollierten Configure-Aufruf, einschließlich `--with-compat` und der ausgewählten Moduleingabe. Dieses Modul nicht in einen fremden Pakethost laden.",
        ),
        "haproxy": (
            "`build-haproxy` is a supported compatibility/binding stage. The selected native HTX filter is built and exercised by `full-lifecycle-haproxy-htx` against the matching prepared HAProxy source; a SPOA/SPOP result is not substituted for it.",
            "`build-haproxy` ist eine unterstützte Kompatibilitäts-/Binding-Stufe. Der ausgewählte native HTX-Filter wird von `full-lifecycle-haproxy-htx` gegen die passende vorbereitete HAProxy-Quelle gebaut und ausgeführt; ein SPOA/SPOP-Ergebnis wird nicht dafür eingesetzt.",
        ),
        "envoy": (
            "The focused connector commands build and test the repository ext_proc service. The selected host remains the verified Envoy binary from preparation; `ext_authz` compatibility commands are not the selected route.",
            "Die fokussierten Connector-Befehle bauen und testen den repository-eigenen ext_proc-Service. Der ausgewählte Host bleibt das verifizierte Envoy-Binary aus der Vorbereitung; ext_authz-Kompatibilitätsbefehle sind nicht der ausgewählte Weg.",
        ),
        "traefik": (
            "The focused commands build the local native middleware and its private UDS engine service. The selected host remains the verified Traefik binary from preparation; forwardAuth compatibility is not the selected route.",
            "Die fokussierten Befehle bauen die lokale native Middleware und ihren privaten UDS-Engine-Service. Der ausgewählte Host bleibt das verifizierte Traefik-Binary aus der Vorbereitung; ForwardAuth-Kompatibilität ist nicht der ausgewählte Weg.",
        ),
        "lighttpd": (
            "The focused commands verify the patch and build the matching patched host. `build-lighttpd` is a stock/compatibility module stage; the selected source path is the patched host executed by `full-lifecycle-lighttpd-patched`.",
            "Die fokussierten Befehle prüfen den Patch und bauen den passenden gepatchten Host. `build-lighttpd` ist eine Stock-/Kompatibilitätsmodulstufe; der ausgewählte Source-Weg ist der gepatchte Host von `full-lifecycle-lighttpd-patched`.",
        ),
    }
    return localized(notes[item["slug"]], german)


SOURCE_OWNERS: dict[str, tuple[str, ...]] = {
    "apache": ("modules/ModSecurity-test-Framework/ci/provisioning/prepare-apache-build.sh",),
    "nginx": ("modules/ModSecurity-test-Framework/ci/provisioning/prepare-nginx-build.sh",),
    "haproxy": ("connectors/haproxy/htx-overlay/build-overlay.sh",),
    "envoy": ("connectors/envoy/build/build_ext_proc.sh",),
    "traefik": ("connectors/traefik/build/build-native-middleware.sh", "connectors/traefik/build/build-engine-service.sh"),
    "lighttpd": ("connectors/lighttpd/build/build_patched_core.sh", "connectors/lighttpd/build/build_patched_host.sh"),
}


def source_owner(item: dict[str, str]) -> str:
    return ", ".join(f"`{path}`" for path in SOURCE_OWNERS[item["slug"]])


def stage_contract(item: dict[str, str], info: dict[str, object], german: bool) -> str:
    slug = item["slug"]
    extra = str(info["extra_prepare"])
    preparation = "`make prepare-runtime-components`"
    if extra:
        preparation += f" + `make {extra}`"
    if german:
        headers = ("Befehl", "Zweck", "Voraussetzung", "Ergebnis/Ort", "Exit- und Evidence-Grenze")
        rows = [
            ("`git clone` / `git switch` / `git submodule update`", "definierter Checkout", "Netzwerkzugang und Git", "Checkout mit Framework-Submodule", "Git-Fehler sind keine Build- oder Runtime-Evidence."),
            ("`make check-framework`", "Framework-Vertrag prüfen", "initialisiertes Submodule", "bestätigter Framework-Pfad", "`77` kann ein fehlendes Framework als BLOCKED melden; kein Connector-Test."),
            (preparation, "Cache-v2 und Host-/Source-Eingaben vorbereiten", "beschreibbarer externer Run-Root", "Provenienz, Cache und vorbereitete Eingaben", "`77` bedeutet bewusst blockierte Voraussetzung; Cache ist keine Evidence."),
            (f"`make {item['build']}`", "Buildstufe", "Vorbereitung und Toolchain", f"`$BUILD_ROOT/stages/{slug}/build/results`", "`0` ist Stufenerfolg, kein Config- oder Trafficnachweis."),
            (f"`make {item['config']}`", "Konfiguration laden/prüfen", "erzeugter Host/Connector", f"`$BUILD_ROOT/stages/{slug}/config_load/results`", "`0` ist kein gesendeter HTTP-Request."),
            (f"`make {item['start']}`", "Host ohne Volltraffic starten", "lesbare Konfiguration und freie lokale Ressourcen", f"`$BUILD_ROOT/stages/{slug}/start_smoke/results`", "`0` ist keine Full-Lifecycle-Evidence."),
            (f"`make {item['runtime']}`", "begrenzten repository-eigenen Runtime-Smoke ausführen", "vorbereiteter Host und lokale Ports", f"`$BUILD_ROOT/stages/{slug}/minimal_runtime_smoke/results`", "`0` gilt nur für diesen Smoke."),
            (f"`make {item['full']}`", "ausgewählten No-CRS-Kernlauf ausführen", "sicherer Run-Identifier", f"`$VERIFIED_RUN_ROOT/evidence/no-crs-evidence/{slug}/$run_id`", "Kanonische Artefakte erst nach anschließendem Evidence-Check bewerten."),
            (f"`make evidence-check-{slug}`", "bereits erzeugte kanonische Artefakte validieren", "derselbe Run-Identifier und vollständige Artefakte", f"`$VERIFIED_RUN_ROOT/evidence/no-crs-evidence/{slug}/$run_id`", "validiert vorhandene Evidence; erzeugt keine neuen Logs oder Runtime-Dateien."),
        ]
    else:
        headers = ("Command", "Purpose", "Prerequisite", "Output/location", "Exit and evidence boundary")
        rows = [
            ("`git clone` / `git switch` / `git submodule update`", "defined checkout", "network access and Git", "checkout with Framework submodule", "Git failures are not build or runtime evidence."),
            ("`make check-framework`", "check the Framework contract", "initialized submodule", "confirmed Framework path", "`77` can report a missing Framework as BLOCKED; it is not a connector test."),
            (preparation, "prepare Cache-v2 and host/source inputs", "writable external run root", "provenance, cache, and prepared inputs", "`77` means a deliberately blocked prerequisite; a cache is not evidence."),
            (f"`make {item['build']}`", "build stage", "preparation and toolchain", f"`$BUILD_ROOT/stages/{slug}/build/results`", "`0` is stage success, not config or traffic proof."),
            (f"`make {item['config']}`", "load/check configuration", "built host/connector", f"`$BUILD_ROOT/stages/{slug}/config_load/results`", "`0` is not a sent HTTP request."),
            (f"`make {item['start']}`", "start host without full traffic", "readable config and free local resources", f"`$BUILD_ROOT/stages/{slug}/start_smoke/results`", "`0` is not full-lifecycle evidence."),
            (f"`make {item['runtime']}`", "run bounded repository-owned runtime smoke", "prepared host and local ports", f"`$BUILD_ROOT/stages/{slug}/minimal_runtime_smoke/results`", "`0` applies only to this smoke."),
            (f"`make {item['full']}`", "run selected No-CRS core lifecycle", "safe run identifier", f"`$VERIFIED_RUN_ROOT/evidence/no-crs-evidence/{slug}/$run_id`", "Assess canonical artifacts only after the following evidence check."),
            (f"`make evidence-check-{slug}`", "validate existing canonical artifacts", "same run identifier and complete artifacts", f"`$VERIFIED_RUN_ROOT/evidence/no-crs-evidence/{slug}/$run_id`", "validates existing evidence; it creates no new logs or runtime files."),
        ]
    return markdown_table(headers, rows)


def source_build_contract(item: dict[str, str], german: bool) -> str:
    """Describe the boundary of the source commands shown immediately above."""
    slug = item["slug"]
    if german:
        return markdown_table(
            ("Befehlsgruppe", "Zweck", "Voraussetzung", "Ergebnis und Grenze"),
            [
                ("Source-Buildbefehle oben", "ausgewählten Host, Modul oder Service aus Source bauen", "vorbereitete Provenienz, Toolchain und externer Buildroot", "Artefakte und Command-/Source-Info-Records unter `$BUILD_ROOT`; Exit `0` ist nur Build-Erfolg."),
                ("gezeigte Config-/Test-/Runtime-Targets", "Artefakt, ABI und Loader im selben Staging prüfen", "passende Header, Bibliotheken und lesbare Konfiguration", "Die Targets prüfen das erzeugte Modul bzw. den Service und dessen Library-Auflösung; `77` kann eine fehlende Voraussetzung melden."),
                (f"`make {item['full']}` + Evidence-Check", "ausgewählten Kernpfad ausführen und Artefakte validieren", "sicherer `run_id` und vollständige Runtime", f"Evidence unter `evidence/no-crs-evidence/{slug}/$run_id`; `2` steht für ungültige Eingabe/Stufe, andere Fehler bleiben Fehler."),
            ],
        )
    return markdown_table(
        ("Command group", "Purpose", "Prerequisite", "Output and boundary"),
        [
            ("source-build commands above", "build the selected host, module, or service from source", "prepared provenance, toolchain, and external build root", "artifacts and command/source-info records below `$BUILD_ROOT`; exit `0` is build success only."),
            ("shown config/test/runtime targets", "check artifact, ABI, and loader in the same staging area", "matching headers, libraries, and readable configuration", "Targets check the generated module or service and its library resolution; `77` can report a missing prerequisite."),
            (f"`make {item['full']}` + evidence check", "run selected core path and validate artifacts", "safe `run_id` and complete runtime", f"evidence below `evidence/no-crs-evidence/{slug}/$run_id`; `2` is invalid input/stage and other failures remain failures."),
        ],
    )


def go_requirement_note(info: dict[str, object], german: bool) -> str:
    requirement = str(info.get("go_requirement", ""))
    if not requirement:
        return ""
    module = str(info["go_module"])
    if german:
        return (
            f"Das Go-Modul `{module}` deklariert einen exakt gepinnten Go-{requirement}-Patch in seiner `go`-Direktive. Vor dem Build "
            "`go version` prüfen; der Paketname allein verspricht keine passende Go-Version."
        )
    return (
        f"The Go module `{module}` declares an exact pinned Go {requirement} patch in its `go` directive. Check `go version` "
        "before building; a package name alone does not promise a compatible Go version."
    )


def prefix_table(german: bool) -> str:
    if german:
        return markdown_table(
            ("Ort", "Verwendung", "Grenze"),
            [
                ("`/usr`", "vom Distributionspaket verwaltet", "nicht als manueller Default überschreiben"),
                ("`/usr/local`", "bewusste lokale Installation", "vorher Dateien inventarisieren"),
                ("`/opt/modsecurity-connector`", "bewusst gewählter isolierter Prefix", "`PKG_CONFIG_PATH` und Loaderpfad gezielt setzen"),
                ("`$HOME/.local`", "benutzerlokale Installation", "kein gemeinsam genutzter Systemhost"),
                ("unter `VERIFIED_RUN_PARENT`", "empfohlenes externes Staging", "Standard für diesen Entwicklungsweg; außerhalb des Checkouts"),
            ],
        )
    return markdown_table(
        ("Location", "Use", "Boundary"),
        [
            ("`/usr`", "managed by a distribution package", "do not overwrite it as a manual default"),
            ("`/usr/local`", "deliberate local installation", "inventory files first"),
            ("`/opt/modsecurity-connector`", "deliberately selected isolated prefix", "set `PKG_CONFIG_PATH` and loader path deliberately"),
            ("`$HOME/.local`", "user-local installation", "not a shared system host"),
            ("below `VERIFIED_RUN_PARENT`", "recommended external staging", "default for this development path; outside the checkout"),
        ],
    )


def placeholder_table(item: dict[str, str], german: bool) -> str:
    slug = item["slug"]
    if german:
        rows = [
            ("Connectorname", slug, "Make- und Evidence-Name dieses Guides; kein Platzhalter in den gezeigten Befehlen."),
            ("Source-Verzeichnis", "unter `$BUILD_ROOT` oder vorbereiteter Provenienz", "Vom unterstützten Vorbereiter erzeugte Quelle; keinen zweiten Hand-Checkout als Ersatz verwenden."),
            ("Build-Verzeichnis", f"`$BUILD_ROOT/stages/{slug}`", "Staging- und Stufenergebnisse außerhalb des Checkouts."),
            ("Installationsprefix", "externes Staging unter `VERIFIED_RUN_PARENT`", "Bevorzugter Entwicklungsort statt systemweiter Installation."),
            ("Rules-Datei", "vom Full-Lifecycle-Dispatcher", "Kanonische Regeldatei wird vom ausgewählten Lauf geliefert; keine lokale Datei als gleichwertig ausgeben."),
            ("Modul-/Hostbinary", "von Vorbereitung oder Source-Build aufgelöst", "Pfad, Header und ABI gehören zum selben ausgewählten Host."),
        ]
        return markdown_table(("Dokumentierter Wert", "Beispiel", "Bedeutung"), rows)
    rows = [
        ("connector name", slug, "Make and evidence name for this guide; no placeholder remains in the shown commands."),
        ("source directory", "below `$BUILD_ROOT` or prepared provenance", "Source created by the supported preparer; do not substitute a second manual checkout."),
        ("build directory", f"`$BUILD_ROOT/stages/{slug}`", "Staging and stage results outside the checkout."),
        ("installation prefix", "external staging below `VERIFIED_RUN_PARENT`", "Preferred development location instead of a system-wide installation."),
        ("rules file", "provided by the full-lifecycle dispatcher", "The selected run supplies canonical rules; do not present a local file as equivalent."),
        ("module/host binary", "resolved by preparation or source build", "Path, headers, and ABI belong to the same selected host."),
    ]
    return markdown_table(("Documented value", "Example", "Meaning"), rows)


def expanded_guide(item: dict[str, str], german: bool) -> str:
    """Render one complete guide from shared technical connector data."""
    info = detail(item)
    slug = item["slug"]
    name = item["name_de"] if german else item["name"]
    mode = item["mode_de"] if german else item["mode"]
    test_prerequisites = localized(info["test_prerequisites"], german)
    source_prerequisites = localized(info["source_prerequisites"], german)
    abi = localized(info["abi"], german)
    config = localized(info["config"], german)
    package_notes = localized(info["package_notes"], german)
    test_commands = tuple(info["test_commands"])
    source_commands = tuple(info["source_commands"])
    source_validation = tuple(info["source_validation"])
    package_validation = tuple(info["package_validation"])
    package_host_query = tuple(info.get("package_host_query", ()))
    package_host_queries = (
        "# Host-package availability inquiry only; no package is selected by this query",
        *package_host_query,
    ) if package_host_query else ()
    prepare_commands = selected_preparation(item, info)
    test_flow = (
        "git clone --recurse-submodules https://github.com/Easton97-Jens/ModSecurity-conector.git",
        "cd ModSecurity-conector",
        "git switch feature/all-connectors-no-crs-baseline",
        "git submodule update --init --recursive",
        "export VERIFIED_RUN_PARENT=\"$HOME/modsecurity-connector-work\"",
        "export VERIFIED_RUN_ROOT=\"$VERIFIED_RUN_PARENT/ModSecurity-conector-verified\"",
        "export CACHE_ROOT=\"$VERIFIED_RUN_ROOT/cache-v2\"",
        "export BUILD_ROOT=\"$VERIFIED_RUN_ROOT/build\"",
        *prepare_commands,
        *test_commands[:4],
        f'run_id="{slug}-core-$(date -u +%Y%m%dT%H%M%SZ)"',
        *test_commands[4:],
    )
    source_environment = (
        "export VERIFIED_RUN_PARENT=\"$HOME/modsecurity-connector-work\"",
        "export VERIFIED_RUN_ROOT=\"$VERIFIED_RUN_PARENT/ModSecurity-conector-verified\"",
        "export CACHE_ROOT=\"$VERIFIED_RUN_ROOT/cache-v2\"",
        f"export BUILD_ROOT=\"$VERIFIED_RUN_ROOT/build/{slug}-source\"",
        "export CC=gcc",
        "export CXX=g++",
        "export CFLAGS=\"-O2 -g\"",
        "export CXXFLAGS=\"-O2 -g\"",
        "jobs=\"$(getconf _NPROCESSORS_ONLN 2>/dev/null || printf '2')\"",
        *prepare_commands,
        "make runtime-components-inventory",
        "make runtime-components-sources",
        f'run_id="{slug}-source-$(date -u +%Y%m%dT%H%M%SZ)"',
        *source_commands,
    )
    package_query = (
        "# Debian / Ubuntu (apt)",
        f"apt-cache policy {packages(BASE_DEBIAN)}",
        f"apt-cache policy {packages(tuple(info['package_debian']))}",
        "# Fedora / RHEL / Rocky Linux / AlmaLinux (dnf)",
        f"dnf info {packages(BASE_FEDORA)}",
        f"dnf info {packages(tuple(info['package_fedora']))}",
        *package_host_queries,
    )
    package_install = (
        "# Debian / Ubuntu (apt)",
        "sudo apt update",
        f"sudo apt install --yes {packages(BASE_DEBIAN)}",
        f"sudo apt install --yes {packages(tuple(info['package_debian']))}",
        "# Fedora / RHEL / Rocky Linux / AlmaLinux (dnf)",
        f"sudo dnf install -y {packages(BASE_FEDORA)}",
        f"sudo dnf install -y {packages(tuple(info['package_fedora']))}",
    )
    package_source_followup = (
        "export VERIFIED_RUN_PARENT=\"$HOME/modsecurity-connector-work\"",
        "export VERIFIED_RUN_ROOT=\"$VERIFIED_RUN_PARENT/ModSecurity-conector-verified\"",
        "export CACHE_ROOT=\"$VERIFIED_RUN_ROOT/cache-v2\"",
        f"export BUILD_ROOT=\"$VERIFIED_RUN_ROOT/build/{slug}-package\"",
        "jobs=\"$(getconf _NPROCESSORS_ONLN 2>/dev/null || printf '2')\"",
        *prepare_commands,
        "make runtime-components-inventory",
        "make runtime-components-sources",
        f'run_id="{slug}-package-$(date -u +%Y%m%dT%H%M%SZ)"',
        *source_commands,
    )
    if str(info["package_status"]) == "package-only":
        package_source_followup = ()
    base_package_query = (
        "# Debian / Ubuntu (apt)",
        f"apt-cache policy {packages(BASE_DEBIAN)}",
        "# Fedora / RHEL / Rocky Linux / AlmaLinux (dnf)",
        f"dnf info {packages(BASE_FEDORA)}",
    )
    cleanup_commands = tuple(info["cleanup_commands"])
    source_host_checks = HOST_VALIDATION[slug]
    artifact_checks = ARTIFACT_VALIDATION[slug]
    test_host_checks = TEST_HOST_VALIDATION[slug]
    test_artifact_checks = TEST_ARTIFACT_VALIDATION[slug]
    test_validation = (
        *test_host_checks,
        *test_artifact_checks,
        f"make {item['config']}",
        f"make {item['start']}",
        f"make {item['runtime']}",
        f'NO_CRS_RUN_ID="$run_id" make evidence-check-{slug}',
        "make runtime-components-inventory",
        "make runtime-components-sources",
    )
    package_followup_note = localized(
        (
            "The selected package route is package-only; keep the following validation in the same checkout and record the selected run.",
            "Der ausgewählte Paketweg ist package-only; die folgende Validierung im selben Checkout ausführen und den ausgewählten Run protokollieren.",
        ) if str(info["package_status"]) == "package-only" else (
            "Packages provide only the dependency/host portion. Continue with this supported source follow-up; package installation alone does not build the selected connector or host integration.",
            "Pakete liefern nur den Abhängigkeits-/Hostanteil. Anschließend diesen unterstützten Source-Follow-up ausführen; die Paketinstallation baut weder den ausgewählten Connector noch die Hostintegration allein.",
        ),
        german,
    )
    package_host_note = localized(
        (
            "The final query lines only discover whether a distribution offers an Envoy host package; no result is treated as the selected host, because the repository uses its verified binary plus the source-built ext_proc service.",
            "Die letzten Abfragezeilen ermitteln nur, ob eine Distribution ein Envoy-Hostpaket anbietet; kein Ergebnis gilt als ausgewählter Host, weil das Repository sein verifiziertes Binary samt Source-gebautem ext_proc-Service nutzt.",
        ) if slug == "envoy" else (
            "The final query lines only discover whether a distribution offers a Traefik host package; no result is treated as the selected host, because the repository uses its verified binary plus source-built native middleware and engine service.",
            "Die letzten Abfragezeilen ermitteln nur, ob eine Distribution ein Traefik-Hostpaket anbietet; kein Ergebnis gilt als ausgewählter Host, weil das Repository sein verifiziertes Binary samt Source-gebauter nativer Middleware und Engine-Service nutzt.",
        ) if slug == "traefik" else ("", ""),
        german,
    )

    if german:
        return f"""{MARKER}

# Build-, Source- und Paketwege: {name}

{language_switch(slug, True)}

## Zweck und aktueller Integrationspfad

Dieser Guide dokumentiert den ausgewählten Integrationspfad
`{item['profile']}` für {name}: {mode}. Der kanonische Kernlauf ist
`make {item['full']}`. Build-, Konfigurations-, Start- und Kompatibilitäts-
Smokes bleiben davon getrennt.

## Die drei Wege im Vergleich

{route_comparison(item, info, True)}

Der Paketstatus dieses Connectors lautet exakt
`{info['package_status']}`. {status_note(str(info['package_status']), True)}

## Gemeinsame Voraussetzungen

{test_prerequisites}

Der Test- und Source-Weg brauchen nur Basistools und einen beschreibbaren
externen Stamm, keine globale Installation des ausgewählten Connectors. Vor
einer Paketinstallation die Verfügbarkeit abfragen:

{shell(base_package_query)}

Auf einem Rechner nur die Zeile der passenden Distributionsfamilie ausführen.

`VERIFIED_RUN_PARENT` muss außerhalb des Git-Checkouts liegen. Er enthält
Build-, Cache-, Runtime-, Log- und Evidence-Dateien und darf keine Secrets im
Namen tragen. `CACHE_ROOT` ist Cache-v2 mit wiederverwendbaren Eingaben, nicht
mit kanonischer Evidence. Die vorbereiteten, wirksamen Quellen zeigt:

{shell(("make runtime-components-inventory", "make runtime-components-sources"))}

## Weg 1: Repository-gesteuert testen

{test_prerequisites}

Die folgenden Befehle klonen den definierten Branch, initialisieren das
Framework und führen alle getrennten Stufen aus. Sie installieren keinen
Connector systemweit. Fehlen Basistools, zuerst im Paketweg deren Verfügbarkeit
prüfen und nur die dort gezeigten Basispakete installieren.

{shell(test_flow)}

{stage_contract(item, info, True)}

`0` bedeutet Erfolg der jeweiligen Stufe. `77` steht für eine bewusst
blockierte Voraussetzung, etwa fehlendes Framework oder einen ungeeigneten
externen Root. `2` kann bei ungültiger Stage-, Connector- oder
Eingabeauswahl auftreten. Andere Nichtnullwerte sind fehlgeschlagene oder
weitergereichte Checks; sie sind nicht als stärkere Aussage zu interpretieren.

### Validierung

Der vorherige Block führt mit demselben `run_id` Config-, Start- und
HTTP/1.1-Smoke sowie den ausgewählten P1–P4-Kernlauf aus. Die folgenden Befehle
prüfen Host, Artefakt und dynamische Library erneut, wiederholen die
repository-gesteuerten Config-/Start-/Runtime-Checks und validieren die bereits
erzeugte Evidence. Der Evidence-Check startet keinen neuen Kernlauf.

{shell(test_validation)}

## Weg 2: Lokal aus Source bauen

{source_prerequisites}

{go_requirement_note(info, True)}

Die folgenden Pins sind Eingaben des unterstützten Vorbereiters. Bei einem
geänderten Pin sind `runtime-components-inventory` und
`runtime-components-sources` maßgeblich; besonders bei beweglichen
libmodsecurity-Referenzen wird der aufgelöste Commit dort dokumentiert.

{pin_table(info, True)}

`-O2 -g` ist ein nachvollziehbarer Entwicklungswert, kein Repository-Default
und keine Vorgabe für ein Deployment. `jobs` ist die Anzahl paralleler
Compilerprozesse; bei wenig RAM beispielsweise `2` wählen. `CPPFLAGS`,
`LDFLAGS`, `PKG_CONFIG_PATH` und `LD_LIBRARY_PATH` nur für bewusst gewählte
Header-, Bibliotheks- oder Stagingpfade setzen.

{shell(source_environment)}

{source_route_note(item, True)}

{source_build_contract(item, True)}

Der unterstützte Build wird dabei durch {source_owner(item)} umgesetzt; die
Root-Stufen dispatchen über
`ci/runtime/lifecycle/run-connector-stage.sh`, der Full Lifecycle über
`ci/runtime/lifecycle/run-no-crs-baseline.sh`. Diese Skripte sind die
Implementierung hinter den gezeigten Make-Targets, nicht eine zweite,
eigenständig zu kopierende Handbauanleitung.

{abi}

### Prefix und Staging

{prefix_table(True)}

Der unterstützte Vorbereiter besitzt den exakten Upstream-Configure- und
Installationsaufruf. Seine erzeugten Command-, Source-Info- und
Artifact-Records im externen Buildroot sind der nachvollziehbare
Konfigurations- und Kompilierungsnachweis; diese Anleitung erfindet keinen
zweiten Handaufruf.

### Validierung

Die folgenden Befehle prüfen das aufgelöste Hostbinary an seinem dokumentierten
externen Staging- oder Cachepfad nach Vorbereitung beziehungsweise Source-Build.
Danach prüfen die Artefaktbefehle, dass das erzeugte Modul oder der Service
vorhanden ist und `ldd` `libmodsecurity` auflöst. Die unterstützten Targets
prüfen anschließend Link, Konfiguration, Start oder den ausgewählten Lifecycle.

{shell((*source_host_checks, *artifact_checks, *source_validation))}

## Weg 3: Über Pakete beziehungsweise paketgestützt installieren

Status: `{info['package_status']}`. {status_note(str(info['package_status']), True)}

{package_notes}

Paketnamen sind releaseabhängig. Diese Abfrage erfolgt vor jeder Installation;
Fedora `mod_security` ist ModSecurity v2 und kein Ersatz für
`libmodsecurity-devel` aus dem v3-Pfad.

Die ersten Befehle sind für **Debian / Ubuntu (apt)**, die folgenden für
**Fedora / RHEL / Rocky Linux / AlmaLinux (dnf)**. Nur die passende Familie
verwenden.

{shell(package_query)}

{package_host_note}

Nur nach erfolgreicher Prüfung und nach eigener Kontrolle der Liste installieren:

{shell(package_install)}

`sudo` wird verwendet, weil Paketdatenbank und Systempfade gewöhnlich
Administratorrechte benötigen. In CI oder einem Container ist der Prozess oft
bereits root; dann `sudo` weglassen statt die Paketliste zu ändern.

{package_followup_note}

{shell(package_source_followup)}

{source_build_contract(item, True)}

### Validierung

`libmodsecurity` muss als v3-Entwicklungsabhängigkeit Header und
pkg-config-Metadaten liefern. Fehlt einer dieser Befehle, zum
repository-gesteuerten Source-Build zurückkehren; kein ModSecurity-v2-Paket
stillschweigend einsetzen.

{shell((*package_validation, *source_host_checks, *artifact_checks, *source_validation))}

## Nach dem Build konfigurieren

{config}

Die gewählte Konfiguration, Regeln und Modulpfade werden durch die
repository-eigenen Targets erzeugt oder geprüft. Konfigurationsdateien müssen
lesbar sein; keine Cookies, Autorisierungswerte, Tokens, privaten Schlüssel
oder Rohlogs in Konfiguration oder Evidence ablegen.

{shell((f"make {item['config']}",))}

## Build und Installation validieren

Für alle Wege gilt: Hostbinary und Version prüfen, Connectorartefakt und
Shared Libraries im ausgewählten Staging betrachten, dann Config- und
Start-Smoke ausführen. Die Source- und Paketwege enden deshalb jeweils mit
ihrem Validierungsblock; ein einzelner Compile oder Link reicht nicht.

{shell((f"make {item['config']}", f"make {item['start']}", f"make {item['runtime']}"))}

## Realen HTTP/1.1-Test ausführen

`make {item['runtime']}` ist der unterstützte repository-eigene
Minimal-Smoke mit realem HTTP/1.1-Traffic für seine dokumentierte Route. Die
konkreten lokalen Ports, URLs und Requests werden aus der erzeugten
Konfiguration abgeleitet; keinen zweiten `curl`-Endpoint erfinden. Für den
ausgewählten P1–P4-Kernpfad, soweit anwendbar, folgt der Full Lifecycle:

{shell((f'run_id="{slug}-http11-$(date -u +%Y%m%dT%H%M%SZ)"', f'NO_CRS_RUN_ID="$run_id" make {item["full"]}', f'NO_CRS_RUN_ID="$run_id" make evidence-check-{slug}'))}

Der Minimal-Smoke und der Full Lifecycle haben unterschiedliche Grenzen. Ein
P1-Deny, P2/P3/P4-Beobachtungen oder ein PASS gelten nur für den tatsächlich
ausgeführten repository-definierten Fall und werden hier nicht zu einer
allgemeinen Capability-Aussage ausgeweitet.

## Evidence und Logs prüfen

Nach einem Full Lifecycle liegen abgeleitete, run-gebundene Verzeichnisse unter
`$VERIFIED_RUN_ROOT`: Evidence in
`evidence/no-crs-evidence/{slug}/$run_id`, Builddateien in
`build/{slug}/$run_id`, Runtime-Dateien in `runs/{slug}/$run_id` und
sanitisierte Logs in `run-logs/{slug}/$run_id`. Allgemeine Stufenresultate
liegen unter `$BUILD_ROOT/stages/{slug}`. Pfade sind abgeleitet, nicht feste
Systempfade.

{shell((f'NO_CRS_RUN_ID="$run_id" make evidence-check-{slug}', "make runtime-components-inventory", "make runtime-components-sources"))}

Evidence erst nach dem Check teilen und sensible Werte vorher entfernen. Cache
und Downloads sind wiederverwendbare Eingaben, keine Evidence.

## Aktualisieren und neu bauen

Den Checkout nur kontrolliert aktualisieren, danach Submodule und Provenienz
erneut prüfen. Einen alten Cache nicht als Beleg für neue Pins behandeln.

{shell(("git pull --ff-only", "git submodule update --init --recursive", "make runtime-components-inventory", "make runtime-components-sources", *prepare_commands, f"make {item['build']}"))}

## Deinstallieren und bereinigen

Repository-Testweg: Den externen `VERIFIED_RUN_PARENT` erst nach Inspektion
oder Archivierung der gewünschten Evidence leeren; der Git-Checkout bleibt
unverändert. `rmdir` entfernt nur leere Verzeichnisse und ist deshalb der
sichere Abschluss statt eines unkontrollierten rekursiven Löschbefehls.

{shell(("find \"$VERIFIED_RUN_PARENT\" -maxdepth 1 -mindepth 1 -print", "rmdir \"$VERIFIED_RUN_PARENT\""))}

Source-Build: Externes Staging oder einen bewusst gewählten Prefix erst nach
Inventarisierung entfernen. Eine Installation unter `/usr` oder `/usr/local`
nicht pauschal löschen. Paketweg: Nur tatsächlich selbst installierte
Connectorpakete entfernen; Benutzerdaten und Evidence nicht ungefragt löschen.

{shell(cleanup_commands)}

## Troubleshooting

### Testweg

Bei Exit `77` zuerst Framework-Submodule, absoluten externen Root, fehlende
Basistools und Cache-Provenienz prüfen. Bei Exit `2` Connector-, Stage- und
Run-ID-Eingaben prüfen. Ist ein Port belegt, den vorherigen lokalen Prozess
geordnet beenden und den Run mit neuer Run-ID wiederholen; Cache-Einträge nicht
blind mischen oder umbenennen.

### Source-Build

Fehlender Compiler oder Header: die Source-Voraussetzungen und die gewählte
Toolchain prüfen. Findet `pkg-config` libmodsecurity nicht, Header- und
Library-Root sowie `PKG_CONFIG_PATH` prüfen. Bei ABI- oder Modulfehlern Host,
Header, Modul, Prefix und Connector gemeinsam aus derselben vorbereiteten
Quelle bauen. Bei fehlender Shared Library nur den bewussten Stagingpfad und
`LD_LIBRARY_PATH` prüfen, nicht global Dateien kopieren.

### Paketweg

Vor Installation Release-Verfügbarkeit erneut abfragen. Bei fehlenden v3-
Headern oder pkg-config-Metadaten den Source-Build verwenden. Eine nicht
lesbare Konfiguration, falsche Dateiberechtigung oder ein belegter Port ist
kein Paketbeweis. Ein Paket-Host mit nicht passender ABI darf nicht mit einem
Source-Modul kombiniert werden.

## Variablen und Platzhalter

{variable_table(info, True)}

{placeholder_table(item, True)}

## Einschränkungen und nicht erhobene Claims

Die Anweisungen beschreiben reproduzierbare Entwicklungs-, Test- und
Buildwege. Sie sind keine Bewertung als produktionsreifes Paket oder gehärtete
Deployment-Anleitung. Sie behaupten keine vollständige CRS-Abdeckung,
keine vollständige Protokoll- oder Plattformmatrix und keine über den
dokumentierten Run hinausgehende Sicherheitseigenschaft. Ein Paketweg ist nur
dann gleichwertig, wenn der ausgewählte Host-, Modul-, Middleware-, Service-
oder Patchpfad tatsächlich durch den dokumentierten Full Lifecycle ausgeführt
und geprüft wurde.
"""

    return f"""{MARKER}

# Build, source-build, and package paths: {name}

{language_switch(slug, False)}

## Purpose and current integration route

This guide documents the selected integration route `{item['profile']}` for
{name}: {mode}. The canonical core run is `make {item['full']}`. Build,
configuration, start, and compatibility smokes remain separate from it.

## Compare the three paths

{route_comparison(item, info, False)}

The exact package status for this connector is
`{info['package_status']}`. {status_note(str(info['package_status']), False)}

## Shared prerequisites

{test_prerequisites}

The test and source paths need only base tools and a writable external parent,
not a global installation of the selected connector. Query availability before
installing a package:

{shell(base_package_query)}

On one machine, run only the line for its matching distribution family.

`VERIFIED_RUN_PARENT` must stay outside the Git checkout. It holds build,
cache, runtime, log, and evidence files and must not contain secrets in its
name. `CACHE_ROOT` is Cache-v2 with reusable inputs, not canonical evidence.
Show the prepared, effective sources with:

{shell(("make runtime-components-inventory", "make runtime-components-sources"))}

## Path 1: Repository-controlled test

{test_prerequisites}

These commands clone the defined branch, initialize the Framework, and run all
separate stages. They do not install a connector system-wide. If base tools are
missing, first query their availability in the package path and install only
the base packages shown there.

{shell(test_flow)}

{stage_contract(item, info, False)}

`0` means success of the individual stage. `77` means a deliberately blocked
prerequisite, such as a missing Framework or unsuitable external root. `2` can
mean an invalid stage, connector, or input selection. Other nonzero values are
failed or propagated checks; do not interpret them as a stronger result.

### Validation

The preceding block uses the same `run_id` for configuration, start, the
HTTP/1.1 smoke, and the selected P1–P4 core lifecycle. The following commands
recheck the host, artifact, and dynamic library, repeat the repository-owned
config/start/runtime checks, and validate the evidence already produced. The
evidence check does not start a new core lifecycle.

{shell(test_validation)}

## Path 2: Local source build

{source_prerequisites}

{go_requirement_note(info, False)}

These pins are inputs to the supported preparer. When a pin changes,
`runtime-components-inventory` and `runtime-components-sources` are
authoritative; in particular, a moving libmodsecurity reference is documented
there by its resolved commit.

{pin_table(info, False)}

`-O2 -g` is an understandable development value, not a repository default or
a deployment prescription. `jobs` is the number of parallel compiler
processes; choose a lower value such as `2` on a memory-constrained machine.
Set `CPPFLAGS`, `LDFLAGS`, `PKG_CONFIG_PATH`, and `LD_LIBRARY_PATH` only for
deliberately selected header, library, or staging paths.

{shell(source_environment)}

{source_route_note(item, False)}

{source_build_contract(item, False)}

The supported build is implemented by {source_owner(item)}; root stages
dispatch through `ci/runtime/lifecycle/run-connector-stage.sh`, and the full
lifecycle through `ci/runtime/lifecycle/run-no-crs-baseline.sh`. Those scripts
are the implementation behind the shown Make targets, not a second manual
build recipe to copy independently.

{abi}

### Prefix and staging

{prefix_table(False)}

The supported preparer owns the exact upstream configure and installation
invocation. Its generated command, source-info, and artifact records in the
external build root are the reproducible configuration and compilation record;
this guide does not invent a second manual invocation.

### Validation

These commands inspect the resolved host binary at its documented external
staging or cache path after preparation or source build. The artifact commands
then check that the generated module or service exists and that `ldd` resolves
`libmodsecurity`. The supported targets then check link, configuration, start,
or the selected lifecycle.

{shell((*source_host_checks, *artifact_checks, *source_validation))}

## Path 3: Package or package-assisted installation

Status: `{info['package_status']}`. {status_note(str(info['package_status']), False)}

{package_notes}

Package names are release-dependent. Query them before every installation;
Fedora `mod_security` is ModSecurity v2 and is not a replacement for the
v3-path `libmodsecurity-devel` package.

The first commands are for **Debian / Ubuntu (apt)**; the following commands
are for **Fedora / RHEL / Rocky Linux / AlmaLinux (dnf)**. Use only the matching
family.

{shell(package_query)}

{package_host_note}

Install only after a successful query and after reviewing the list yourself:

{shell(package_install)}

`sudo` is used because package databases and system paths normally require
administrator privileges. A CI job or container often already runs as root;
in that case omit `sudo` instead of changing the package list.

{package_followup_note}

{shell(package_source_followup)}

{source_build_contract(item, False)}

### Validation

`libmodsecurity` must provide v3 development headers and pkg-config metadata.
If any of these commands is unavailable, return to the repository-controlled
source build; never silently use a ModSecurity-v2 package.

{shell((*package_validation, *source_host_checks, *artifact_checks, *source_validation))}

## Configure after the build

{config}

The selected configuration, rules, and module paths are generated or checked
by repository-owned targets. Configuration files must be readable; do not put
cookies, authorization values, tokens, private keys, or raw logs into config
or evidence.

{shell((f"make {item['config']}",))}

## Validate build and installation

For every path: inspect the host binary and version, inspect connector output
and shared libraries in the selected staging area, then run config and start
smokes. The source and package paths therefore each end in their own validation
block; a compile or link by itself is insufficient.

{shell((f"make {item['config']}", f"make {item['start']}", f"make {item['runtime']}"))}

## Run a real HTTP/1.1 test

`make {item['runtime']}` is the supported repository-owned minimal smoke with
real HTTP/1.1 traffic for its documented route. Concrete local ports, URLs,
and requests come from generated configuration; do not invent a second `curl`
endpoint. Run the full lifecycle for the selected P1–P4 core path where
applicable:

{shell((f'run_id="{slug}-http11-$(date -u +%Y%m%dT%H%M%SZ)"', f'NO_CRS_RUN_ID="$run_id" make {item["full"]}', f'NO_CRS_RUN_ID="$run_id" make evidence-check-{slug}'))}

The minimal smoke and the full lifecycle have different boundaries. A P1 deny,
P2/P3/P4 observation, or PASS applies only to the repository-defined case that
actually ran and is not expanded here into a general capability statement.

## Inspect evidence and logs

After a full lifecycle, derived run-bound directories are below
`$VERIFIED_RUN_ROOT`: evidence at
`evidence/no-crs-evidence/{slug}/$run_id`, build files at
`build/{slug}/$run_id`, runtime files at `runs/{slug}/$run_id`, and sanitized
logs at `run-logs/{slug}/$run_id`. General stage results are below
`$BUILD_ROOT/stages/{slug}`. These are derived paths, not fixed system paths.

{shell((f'NO_CRS_RUN_ID="$run_id" make evidence-check-{slug}', "make runtime-components-inventory", "make runtime-components-sources"))}

Share evidence only after the check and remove sensitive values first. Caches
and downloads are reusable inputs, not evidence.

## Update and rebuild

Update a checkout deliberately, then recheck submodules and provenance. Do not
treat an old cache as proof for changed pins.

{shell(("git pull --ff-only", "git submodule update --init --recursive", "make runtime-components-inventory", "make runtime-components-sources", *prepare_commands, f"make {item['build']}"))}

## Uninstall and clean up

Repository test path: inspect or archive desired evidence before emptying the
external `VERIFIED_RUN_PARENT`; the Git checkout stays unchanged. `rmdir` only
removes empty directories, so it is the safe final operation instead of an
uncontrolled recursive delete.

{shell(("find \"$VERIFIED_RUN_PARENT\" -maxdepth 1 -mindepth 1 -print", "rmdir \"$VERIFIED_RUN_PARENT\""))}

Source build: remove external staging or a deliberately selected prefix only
after inventorying it. Do not broadly remove an installation below `/usr` or
`/usr/local`. Package path: remove only connector packages actually installed
by the operator; do not delete user data or evidence without review.

{shell(cleanup_commands)}

## Troubleshooting

### Repository test path

For exit `77`, first check the Framework submodule, absolute external root,
missing base tools, and cache provenance. For exit `2`, check connector, stage,
and run-id input. If a port is occupied, stop the previous local process in an
orderly way and repeat with a new run ID; do not blindly mix or rename cache
entries.

### Source build

For a missing compiler or header, check source prerequisites and the selected
toolchain. If pkg-config cannot find libmodsecurity, check the header/library
root and `PKG_CONFIG_PATH`. For ABI or module failures, build host, headers,
module, prefix, and connector together from the same prepared source. For a
missing shared library, check only the deliberate staging path and
`LD_LIBRARY_PATH`; do not globally copy files.

### Package path

Query release availability again before installation. Use the source build if
v3 headers or pkg-config metadata are absent. An unreadable configuration,
wrong file permission, or occupied port is not package proof. Do not combine a
package host with a source module that has a different ABI.

## Variables and placeholders

{variable_table(info, False)}

{placeholder_table(item, False)}

## Limitations and non-claims

These instructions describe reproducible development, test, and build paths.
They are not an assessment of a production package or hardened deployment
guidance. They do not assert complete CRS coverage, a complete protocol or
platform matrix, or a security property beyond the documented run. A package
path is equivalent only when the selected host, module, middleware, service,
or patch path actually ran and was checked through the documented full
lifecycle.
"""


OFFICIAL_DOMAINS = {
    "httpd.apache.org",
    "nginx.org",
    "github.com/owasp-modsecurity",
    "github.com/haproxy",
    "docs.haproxy.org",
    "haproxy.org",
    "www.haproxy.org",
    "envoyproxy.io",
    "www.envoyproxy.io",
    "github.com/envoyproxy",
    "doc.traefik.io",
    "github.com/traefik",
    "github.com/lighttpd",
    "download.lighttpd.net",
    "redmine.lighttpd.net",
}


# This second, source-first model is intentionally independent from the
# Framework target map above.  It records upstream material and the manual
# hand-off into a repository connector.  Commands, pins, URLs, and variables
# are shared by the English and German renderers; only explanatory prose is
# localized.
MANUAL_GUIDES: dict[str, dict[str, object]] = {
    "apache": {
        "components": (
            "libmodsecurity v3, Apache HTTP Server 2.4, APR/APR-util, PCRE2, the repository Apache adapter, APXS, a local rule file, and a loopback httpd instance.",
            "libmodsecurity v3, Apache HTTP Server 2.4, APR/APR-util, PCRE2, der Repository-Apache-Adapter, APXS, eine lokale Regeldatei und eine httpd-Instanz auf Loopback.",
        ),
        "repository_connector_title": ("Apache connector", "Apache-Connector"),
        "repository_connector_path": "connectors/apache",
        "repository_connector_readme": (
            "../../../connectors/apache/README.md",
            "../../../connectors/apache/README.de.md",
        ),
        "repository_connector_source_links": (
            (
                "Productive Apache sources",
                "Produktive Apache-Quellen",
                "../../../connectors/apache/src/",
            ),
        ),
        "repository_connector_build_files": (
            (
                "Autotools configuration",
                "Autotools-Konfiguration",
                "../../../connectors/apache/configure.ac",
            ),
            (
                "Source mapping",
                "Source-Zuordnung",
                "../../../connectors/apache/SOURCE_MAP.json",
            ),
            (
                "Standalone Apache configuration harness",
                "Eigenständiges Apache-Konfigurationsharness",
                "../../../connectors/apache/harness/apache_smoke.conf",
            ),
        ),
        "repository_connector_build_steps": (
            "Section 7 materializes this adapter-owned source into an external Autotools worktree and builds it with the selected APXS/httpd pair.",
            "Abschnitt 7 materialisiert diese adaptereigene Quelle in einen externen Autotools-Worktree und baut sie mit dem ausgewählten APXS-/httpd-Paar.",
        ),
        "alternative_connector_title": ("ModSecurity-apache", "ModSecurity-apache"),
        "alternative_connector_url": "https://github.com/owasp-modsecurity/ModSecurity-apache",
        "alternative_connector_note": (
            "The main path in this guide uses the repository-owned adapter under [`connectors/apache/`](../../../connectors/apache/README.md). A separate upstream build does not automatically include the repository-owned Common integration and is not automatically equivalent to the checked path here.",
            "Der Hauptweg dieser Anleitung verwendet den repository-eigenen Adapter unter [`connectors/apache/`](../../../connectors/apache/README.de.md). Ein separater Upstream-Build enthält nicht automatisch die repository-eigene Common-Integration und ist nicht automatisch mit dem hier geprüften Pfad gleichwertig.",
        ),
        "official_sources": (
            ("Compiling and Installing", "https://httpd.apache.org/docs/2.4/install.html", "Apache's official source release, APR/APR-util and PCRE2 prerequisites, configure, make, installation, start, and stop sequence.", "Offizieller Apache-Quellrelease sowie Voraussetzungen für APR/APR-util und PCRE2, Configure, Make, Installation, Start und Stop.", "HTTP Server 2.4; choose and verify the release again before building."),
            ("APXS", "https://httpd.apache.org/docs/2.4/programs/apxs.html", "The DSO build/install interface and the queries that bind a module to one httpd build.", "Die DSO-Build-/Installationsschnittstelle und die Abfragen, die ein Modul an genau einen httpd-Build binden.", "HTTP Server 2.4 APXS reference."),
            ("Apache HTTP Server Download", "https://httpd.apache.org/download.cgi", "Official release archives, PGP signatures, checksums, and Apache KEYS.", "Offizielle Releasearchive, PGP-Signaturen, Prüfsummen und Apache KEYS.", "The page changes when Apache publishes a release."),
            ("ModSecurity repository", "https://github.com/owasp-modsecurity/ModSecurity", "The libmodsecurity v3 source and its Autotools build instructions.", "Die libmodsecurity-v3-Quelle und ihre Autotools-Buildanleitung.", "The selected Git tag/commit is recorded below."),
        ),
        "package_queries": ('apt-cache search apache2', 'dnf search httpd', 'apache2 -v 2>/dev/null || httpd -v 2>/dev/null || true'),
        "package_note": (
            "A package host can be useful for comparison, but its APXS, headers, module directory, configuration layout, and service name can differ from this source prefix. Query the matching distribution's official package documentation before choosing package names; rebuild the adapter with that package's APXS if that is the intended host.",
            "Ein Pakethost kann zum Vergleich nützlich sein, aber sein APXS, seine Header, sein Modulverzeichnis, Konfigurationslayout und Servicename können von diesem Source-Prefix abweichen. Vor konkreten Paketnamen die offizielle Paketdokumentation der passenden Distribution prüfen; den Adapter mit APXS dieses Pakets neu bauen, wenn er der beabsichtigte Host ist.",
        ),
        "variables": (
            ("HTTPD_VERSION", "Selected Apache 2.4 release; revalidate against the download page.", "Ausgewählter Apache-2.4-Release; gegen die Downloadseite erneut validieren."),
            ("HTTPD_ARCHIVE", "Release archive filename derived from HTTPD_VERSION.", "Aus HTTPD_VERSION abgeleiteter Releasearchivname."),
            ("HTTPD_URL", "Official Apache archive URL.", "Offizielle Apache-Archiv-URL."),
            ("HTTPD_SRC", "Unpacked Apache source tree.", "Entpackter Apache-Source-Baum."),
            ("APXS", "APXS from the same host that will load the module.", "APXS desselben Hosts, der das Modul lädt."),
            ("CONNECTOR_SRC", "Repository Apache connector source selected from CONNECTOR_ROOT.", "Aus CONNECTOR_ROOT ausgewählte Repository-Source des Apache-Connectors."),
            ("CONNECTOR_BUILD_DIR", "External materialized Autotools worktree for the repository Apache adapter.", "Externer materialisierter Autotools-Worktree für den Repository-Apache-Adapter."),
            ("HTTPD_BIN", "httpd executable paired explicitly with APXS during configuration.", "httpd-Executable, das beim Configure ausdrücklich mit APXS gepaart wird."),
            ("MODULE_PATH", "Installed repository DSO resolved by APXS.", "Durch APXS aufgelöstes installiertes Repository-DSO."),
            ("HTTPD_MODULE_DIR", "Apache module directory reported by the selected APXS.", "Vom ausgewählten APXS gemeldetes Apache-Modulverzeichnis."),
            ("HTTPD_RUNTIME_ROOT", "Private writable Apache runtime root for the standalone loopback instance.", "Privater beschreibbarer Apache-Laufzeitroot für die eigenständige Loopback-Instanz."),
            ("HTTPD_DOCUMENT_ROOT", "Private document root containing the explicit local test page.", "Privates Document-Root mit der expliziten lokalen Testseite."),
            ("HTTPD_MODULES", "Generated module-load file for the standalone Apache instance.", "Erzeugte Modul-Ladedatei der eigenständigen Apache-Instanz."),
            ("HTTPD_CONFIG", "Local standalone httpd configuration.", "Lokale eigenständige httpd-Konfiguration."),
        ),
        "troubleshoot": (
            "If `apxs -q` points at different headers or a different module directory than the running httpd, stop and rebuild the adapter. A module built against one Apache ABI must not be loaded by another one.",
            "Wenn `apxs -q` auf andere Header oder ein anderes Modulverzeichnis als das laufende httpd zeigt, stoppen und den Adapter neu bauen. Ein gegen eine Apache-ABI gebautes Modul darf nicht von einer anderen geladen werden.",
        ),
    },
    "nginx": {
        "components": (
            "libmodsecurity v3, an official NGINX source release, the repository-owned dynamic NGINX connector, the Common integration, a local rule file, and a loopback NGINX instance.",
            "libmodsecurity v3, ein offizieller NGINX-Source-Release, der repository-eigene dynamische NGINX-Connector, die Common-Integration, eine lokale Regeldatei und eine NGINX-Instanz auf Loopback.",
        ),
        "repository_connector_title": ("NGINX connector", "NGINX-Connector"),
        "repository_connector_path": "connectors/nginx",
        "repository_connector_readme": (
            "../../../connectors/nginx/README.md",
            "../../../connectors/nginx/README.de.md",
        ),
        "repository_connector_source_links": (
            (
                "NGINX module configuration",
                "NGINX-Modulkonfiguration",
                "../../../connectors/nginx/config",
            ),
            (
                "Productive NGINX sources",
                "Produktive NGINX-Quellen",
                "../../../connectors/nginx/src/",
            ),
        ),
        "repository_connector_build_files": (
            (
                "Source mapping",
                "Source-Zuordnung",
                "../../../connectors/nginx/SOURCE_MAP.json",
            ),
        ),
        "repository_connector_build_steps": (
            "Section 7 builds this adapter-owned connector as the documented dynamic NGINX module; official host documentation only provides the NGINX host source or package context.",
            "Abschnitt 7 baut diesen adaptereigenen Connector als dokumentiertes dynamisches NGINX-Modul; die offizielle Hostdokumentation stellt nur die NGINX-Hostquelle oder den Paketkontext bereit.",
        ),
        "alternative_connector_title": ("ModSecurity-nginx", "ModSecurity-nginx"),
        "alternative_connector_url": "https://github.com/owasp-modsecurity/ModSecurity-nginx",
        "alternative_connector_note": (
            "This guide uses the connector in [`connectors/nginx/`](../../../connectors/nginx/README.md) by default because it contains the repository-owned Common integration, configuration, and tested adaptations. An upstream-only build is a different build path and is not automatically equivalent to the selected repository connector.",
            "Diese Anleitung verwendet standardmäßig den Connector aus [`connectors/nginx/`](../../../connectors/nginx/README.de.md), weil dieser die repository-eigene Common-Integration, Konfiguration und die hier getesteten Anpassungen enthält. Ein Upstream-only-Build ist ein anderer Buildpfad und nicht automatisch gleichwertig mit dem ausgewählten Repository-Connector.",
        ),
        "official_sources": (
            ("Building nginx from Sources", "https://nginx.org/en/docs/configure.html", "The official configure options, including prefix paths, compatibility, compiler, and linker flags.", "Die offiziellen Configure-Optionen einschließlich Prefix-Pfaden, Kompatibilität sowie Compiler- und Linkerflags.", "NGINX options are release-dependent; inspect `./configure --help` for the selected source archive."),
            ("Official NGINX packages", "https://nginx.org/en/linux_packages.html", "Official distribution package repositories and package-install context; not an ABI-equivalence claim for a source-built module.", "Offizielle Distributionsrepositories und Paketinstallationskontext; kein ABI-Gleichwertigkeitsclaim für ein aus Source gebautes Modul.", "Package layout changes by distribution and release."),
            ("ModSecurity repository", "https://github.com/owasp-modsecurity/ModSecurity", "The libmodsecurity v3 engine source.", "Die libmodsecurity-v3-Enginequelle.", "The selected tag/commit is shown in the shared build section."),
        ),
        "config_note": (
            "For the complete directive-level contract, read the repository [NGINX configuration reference](../../../examples/nginx/configuration-reference.md) before adapting this local example.",
            "Für den vollständigen Direktivenvertrag vor der Anpassung dieses lokalen Beispiels die repository-eigene [NGINX-Konfigurationsreferenz](../../../examples/nginx/configuration-reference.de.md) lesen.",
        ),
        "package_queries": ('apt-cache search nginx', 'dnf search nginx', 'nginx -V 2>&1 || true'),
        "package_note": (
            "An official package can provide a host, but it is not interchangeable with this source-built NGINX/connector pair. Check the official NGINX package page and the package's own `nginx -V` output before choosing a different host build.",
            "Ein offizielles Paket kann einen Host bereitstellen, ist aber nicht mit diesem aus Source gebauten NGINX-/Connectorpaar austauschbar. Vor der Wahl eines anderen Host-Builds die offizielle NGINX-Paketseite und die Ausgabe `nginx -V` des Pakets prüfen.",
        ),
        "variables": (
            ("NGINX_BUILD_BASE", "External NGINX source/build/provenance directory.", "Externes NGINX-Source-/Build-/Provenienzverzeichnis."),
            ("NGINX_VERSION", "Selected official NGINX release.", "Ausgewählter offizieller NGINX-Release."),
            ("NGINX_ARCHIVE", "Archive name derived from NGINX_VERSION.", "Aus NGINX_VERSION abgeleiteter Archivname."),
            ("NGINX_URL", "Official NGINX archive URL.", "Offizielle NGINX-Archiv-URL."),
            ("NGINX_SRC", "Unpacked NGINX source tree.", "Entpackter NGINX-Source-Baum."),
            ("NGINX_PREFIX", "Private NGINX installation prefix.", "Privater NGINX-Installationsprefix."),
            ("MSCONNECTOR_COMMON_INC", "Repository Common header directory passed to the NGINX module configuration.", "An die NGINX-Modulkonfiguration übergebenes Repository-Common-Headerverzeichnis."),
            ("MSCONNECTOR_COMMON_SRC", "Repository Common source directory compiled into the NGINX module.", "In das NGINX-Modul kompilierte Repository-Common-Quelldateien."),
            ("MODSECURITY_INC", "libmodsecurity header directory selected from the shared build.", "Aus dem gemeinsamen Build ausgewähltes libmodsecurity-Headerverzeichnis."),
            ("MODSECURITY_LIB", "libmodsecurity library directory selected from the shared build.", "Aus dem gemeinsamen Build ausgewähltes libmodsecurity-Bibliotheksverzeichnis."),
            ("NGINX_CONFIG", "Local NGINX configuration for the loopback test.", "Lokale NGINX-Konfiguration für den Loopback-Test."),
            ("NGINX_DOCROOT", "External local document root used by the protected static-content test.", "Externes lokales Document-Root des geschützten Static-Content-Tests."),
        ),
        "troubleshoot": (
            "A startup or directive failure normally means the NGINX binary, dynamic-module configure arguments, repository connector, or installed library differ. Rebuild the pair together; do not combine it with an unrelated package installation.",
            "Ein Start- oder Direktivenfehler bedeutet normalerweise, dass NGINX-Binary, Configure-Argumente für das dynamische Modul, Repository-Connector oder installierte Library voneinander abweichen. Das Paar gemeinsam neu bauen; nicht mit einer fremden Paketinstallation kombinieren.",
        ),
    },
    "haproxy": {
        "components": (
            "libmodsecurity v3, HAProxy 3.2.21 source, the repository native HTX filter/overlay, the Common bridge, a local rule file, a loopback frontend, and a loopback upstream.",
            "libmodsecurity v3, HAProxy-3.2.21-Source, der repository-eigene native HTX-Filter/Overlay, die Common-Bridge, eine lokale Regeldatei, ein Loopback-Frontend und ein Loopback-Upstream.",
        ),
        "repository_connector_title": ("HAProxy connector", "HAProxy-Connector"),
        "repository_connector_path": "connectors/haproxy",
        "repository_connector_readme": (
            "../../../connectors/haproxy/README.md",
            "../../../connectors/haproxy/README.de.md",
        ),
        "repository_connector_source_links": (
            (
                "Productive HAProxy sources",
                "Produktive HAProxy-Quellen",
                "../../../connectors/haproxy/src/",
            ),
            (
                "Native HTX overlay",
                "Nativer HTX-Overlay",
                "../../../connectors/haproxy/htx-overlay/",
            ),
        ),
        "repository_connector_build_files": (
            (
                "HTX overlay builder",
                "HTX-Overlay-Builder",
                "../../../connectors/haproxy/htx-overlay/build-overlay.sh",
            ),
            (
                "Source mapping",
                "Source-Zuordnung",
                "../../../connectors/haproxy/SOURCE_MAP.json",
            ),
            (
                "Native HTX runtime configuration helper",
                "Native-HTX-Laufzeitkonfigurationshelper",
                "../../../connectors/haproxy/harness/run_haproxy_htx_runtime.sh",
            ),
        ),
        "repository_connector_build_steps": (
            "Section 7 applies the repository-owned HTX overlay to the selected host source and builds the Common/libmodsecurity integration.",
            "Abschnitt 7 wendet den repository-eigenen HTX-Overlay auf die ausgewählte Hostquelle an und baut die Common-/libmodsecurity-Integration.",
        ),
        "alternative_connector_title": "",
        "alternative_connector_url": "",
        "alternative_connector_note": ("", ""),
        "official_sources": (
            ("HAProxy INSTALL", "https://github.com/haproxy/haproxy/blob/master/INSTALL", "Official target selection, build options, compilation, and installation guidance.", "Offizielle Anleitung zur Target-Auswahl, Buildoptionen, Kompilierung und Installation.", "Read the INSTALL file for the exact selected HAProxy release."),
            ("HAProxy Documentation", "https://docs.haproxy.org/", "Configuration syntax and CLI documentation for `haproxy -c` and runtime operation.", "Konfigurationssyntax und CLI-Dokumentation für `haproxy -c` und den Laufzeitbetrieb.", "Use documentation matching the selected major/minor series."),
            ("HAProxy Releases", "https://www.haproxy.org/download/", "Official source downloads and release series selection.", "Offizielle Source-Downloads und Auswahl der Release-Serie.", "The repository overlay currently fixes its compatible source to 3.2.21."),
            ("ModSecurity repository", "https://github.com/owasp-modsecurity/ModSecurity", "The libmodsecurity v3 engine source.", "Die libmodsecurity-v3-Enginequelle.", "The selected tag/commit is shown in the shared build section."),
        ),
        "connector_intro": (
            "The official HAProxy release does not contain this connector. The repository native HTX integration copies the compatible source to a fresh external worktree, checks and applies its overlay, adds the HTX filter plus Common/libmodsecurity bridge, and rebuilds the host. The timestamped worktree avoids accidental reuse because the builder refuses an existing worktree. SPOE/SPOP is a separate compatibility path and is not evidence for this native filter.",
            "Der offizielle HAProxy-Release enthält diesen Connector nicht. Die repository-eigene native HTX-Integration kopiert die kompatible Quelle in einen frischen externen Worktree, prüft und wendet ihren Overlay an, fügt HTX-Filter sowie Common-/libmodsecurity-Bridge hinzu und baut den Host neu. Der Zeitstempel-Worktree vermeidet versehentliche Wiederverwendung, weil der Builder einen vorhandenen Worktree verweigert. SPOE/SPOP ist ein separater Kompatibilitätsweg und keine Evidence für diesen nativen Filter.",
        ),
        "connector_commands": (
            'export HAPROXY_HTX_SOURCE_DIR="$HAPROXY_SRC"',
            'export HAPROXY_HTX_BUILD_DIR="$HOST_BUILD_BASE/htx-overlay-$(date -u +%Y%m%dT%H%M%SZ)"',
            'export MAKE_JOBS=2',
            'CONNECTOR_ROOT="$CONNECTOR_ROOT" sh "$CONNECTOR_ROOT/connectors/haproxy/htx-overlay/build-overlay.sh"',
            'export HAPROXY_HTX_BIN="$HAPROXY_HTX_BUILD_DIR/worktree/haproxy"',
            'test -x "$HAPROXY_HTX_BIN"',
            '"$HAPROXY_HTX_BIN" -vv',
        ),
        "config_commands": (
            'export RULES_FILE="$HOST_BUILD_BASE/modsecurity-local.conf"',
            'export HAPROXY_CONFIG="$HOST_BUILD_BASE/haproxy-local.cfg"',
            'cat > "$RULES_FILE" <<EOF\nSecRuleEngine On\nSecRule REQUEST_URI "@streq /blocked" "id:100001,phase:1,deny,status:403,log"\nEOF',
            'cat > "$HAPROXY_CONFIG" <<EOF\nglobal\n    daemon\ndefaults\n    mode http\n    timeout connect 5s\n    timeout client 30s\n    timeout server 30s\nfrontend local\n    bind 127.0.0.1:8080\n    filter modsecurity-htx rules-file "$RULES_FILE" phase4-mode safe\n    default_backend local_upstream\nbackend local_upstream\n    server app 127.0.0.1:8081\nEOF',
            '"$HAPROXY_HTX_BIN" -c -f "$HAPROXY_CONFIG"',
        ),
        "validation": (
            '"$HAPROXY_HTX_BIN" -vv',
            'file "$HAPROXY_HTX_BIN"',
            'ldd "$HAPROXY_HTX_BIN" | grep -F libmodsecurity | grep -Fv "not found"',
            'test -f "$HAPROXY_HTX_BUILD_DIR/overlay-build.env"',
            'sha256sum "$HAPROXY_HTX_BIN"',
        ),
        "http_commands": (
            'mkdir -p "$HOST_BUILD_BASE/www"',
            'printf "haproxy local upstream\\n" > "$HOST_BUILD_BASE/www/index.html"',
            'python3 -m http.server 8081 --bind 127.0.0.1 --directory "$HOST_BUILD_BASE/www" > "$HOST_BUILD_BASE/upstream.log" 2>&1 &',
            'upstream_pid=$!',
            'LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" "$HAPROXY_HTX_BIN" -db -f "$HAPROXY_CONFIG" > "$HOST_BUILD_BASE/haproxy.log" 2>&1 &',
            'haproxy_pid=$!',
            'attempt=0\nwhile [ "$attempt" -lt 50 ]; do\n    if ! kill -0 "$upstream_pid" 2>/dev/null || ! kill -0 "$haproxy_pid" 2>/dev/null; then\n        exit 1\n    fi\n    if [ "$(curl -sS --connect-timeout 1 -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/ 2>/dev/null)" = "200" ]; then\n        break\n    fi\n    attempt=$((attempt + 1))\n    sleep 0.1\ndone',
            'test "$attempt" -lt 50',
            'test "$(curl -sS -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/)" = "200"',
            'test "$(curl -sS -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/blocked)" = "403"',
            'kill "$haproxy_pid" "$upstream_pid"',
        ),
        "package_queries": ('apt-cache search haproxy', 'dnf search haproxy', 'haproxy -vv 2>/dev/null || true'),
        "package_note": (
            "A package can provide an ordinary HAProxy for comparison, but it does not carry the repository HTX overlay. It therefore cannot substitute for the selected native filter path; use the exact compatible source and overlay build.",
            "Ein Paket kann ein gewöhnliches HAProxy zum Vergleich bereitstellen, trägt aber nicht den repository-eigenen HTX-Overlay. Es kann daher den ausgewählten nativen Filterweg nicht ersetzen; die exakt kompatible Quelle und den Overlay-Build verwenden.",
        ),
        "variables": (
            ("HAPROXY_VERSION", "Version required by the current HTX overlay.", "Von der aktuellen HTX-Overlay verlangte Version."),
            ("HAPROXY_ARCHIVE", "Archive name derived from HAPROXY_VERSION.", "Aus HAPROXY_VERSION abgeleiteter Archivname."),
            ("HAPROXY_URL", "Official HAProxy source archive URL.", "Offizielle HAProxy-Sourcearchiv-URL."),
            ("HAPROXY_SHA256", "Expected SHA-256 for the selected source archive.", "Erwartete SHA-256 des ausgewählten Sourcearchivs."),
            ("HAPROXY_SRC", "Verified upstream source tree.", "Verifizierter Upstream-Source-Baum."),
            ("HAPROXY_PREFIX", "Private upstream host installation prefix.", "Privater Upstream-Host-Installationsprefix."),
            ("HAPROXY_STAGE", "Staging root used with DESTDIR.", "Mit DESTDIR verwendeter Staging-Root."),
            ("HAPROXY_BIN", "Staged ordinary HAProxy binary.", "Gestagtes gewöhnliches HAProxy-Binary."),
            ("HAPROXY_HTX_SOURCE_DIR", "Verified source consumed by the overlay builder.", "Vom Overlay-Builder verwendete verifizierte Quelle."),
            ("HAPROXY_HTX_BUILD_DIR", "External disposable overlay worktree and provenance directory.", "Externes disponierbares Overlay-Worktree- und Provenienzverzeichnis."),
            ("HAPROXY_HTX_BIN", "Repository-built native HTX host binary.", "Repository-gebautes natives HTX-Hostbinary."),
            ("MAKE_JOBS", "Parallel-job value passed to the repository overlay builder.", "An den Repository-Overlay-Builder übergebener Parallel-Job-Wert."),
            ("HAPROXY_CONFIG", "Local loopback HAProxy configuration.", "Lokale Loopback-HAProxy-Konfiguration."),
        ),
        "troubleshoot": (
            "The overlay refuses a version other than 3.2.21, an in-tree build directory, missing libmodsecurity headers, or a missing library. Treat that as a compatibility boundary, not as a reason to substitute a SPOA result.",
            "Der Overlay verweigert eine andere Version als 3.2.21, ein In-Tree-Buildverzeichnis, fehlende libmodsecurity-Header oder eine fehlende Bibliothek. Das als Kompatibilitätsgrenze behandeln, nicht als Grund, ein SPOA-Ergebnis einzusetzen.",
        ),
    },
    "envoy": {
        "components": (
            "libmodsecurity v3, an official Envoy binary or optional Bazel build, the repository ext_proc service, its CGo/Common bridge, gRPC configuration, a local rule file, and loopback Envoy/upstream listeners.",
            "libmodsecurity v3, ein offizielles Envoy-Binary oder optionaler Bazel-Build, der repository-eigene ext_proc-Service, seine CGo-/Common-Bridge, gRPC-Konfiguration, eine lokale Regeldatei und Loopback-Listener für Envoy/Upstream.",
        ),
        "repository_connector_title": ("Envoy connector", "Envoy-Connector"),
        "repository_connector_path": "connectors/envoy",
        "repository_connector_readme": (
            "../../../connectors/envoy/README.md",
            "../../../connectors/envoy/README.de.md",
        ),
        "repository_connector_source_links": (
            (
                "Productive ext_proc service",
                "Produktiver ext_proc-Service",
                "../../../connectors/envoy/ext_proc/",
            ),
            (
                "Connector configuration",
                "Connector-Konfiguration",
                "../../../connectors/envoy/config/",
            ),
        ),
        "repository_connector_build_files": (
            (
                "ext_proc build helper",
                "ext_proc-Build-Helper",
                "../../../connectors/envoy/build/build_ext_proc.sh",
            ),
            (
                "Source mapping",
                "Source-Zuordnung",
                "../../../connectors/envoy/SOURCE_MAP.json",
            ),
        ),
        "repository_connector_build_steps": (
            "Section 7 builds the repository-owned ext_proc service; the official Envoy documentation only explains the host binary and host configuration.",
            "Abschnitt 7 baut den repository-eigenen ext_proc-Service; die offizielle Envoy-Dokumentation erläutert nur Hostbinary und Hostkonfiguration.",
        ),
        "alternative_connector_title": "",
        "alternative_connector_url": "",
        "alternative_connector_note": ("", ""),
        "official_sources": (
            ("Installing Envoy", "https://www.envoyproxy.io/docs/envoy/latest/start/install", "Official binary, package, and container installation choices plus version inspection.", "Offizielle Auswahl von Binary-, Paket- und Containerinstallation sowie Versionsprüfung.", "The page is version-sensitive; use the docs matching the selected Envoy release."),
            ("Run Envoy", "https://www.envoyproxy.io/docs/envoy/latest/start/quick-start/run-envoy.html", "The official version, configuration validation, and local startup commands.", "Die offiziellen Befehle für Version, Konfigurationsvalidierung und lokalen Start.", "Use the selected Envoy release documentation."),
            ("Static configuration", "https://www.envoyproxy.io/docs/envoy/latest/start/quick-start/configuration-static", "Listener, HTTP connection manager, route, and cluster configuration used by the loopback example.", "Listener-, HTTP-Connection-Manager-, Route- und Clusterkonfiguration des Loopback-Beispiels.", "Verify field names against the selected release."),
            ("HTTP external processing filter", "https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/ext_proc_filter", "The official ext_proc filter and bidirectional gRPC configuration contract.", "Der offizielle ext_proc-Filter und der Vertrag für bidirektionale gRPC-Konfiguration.", "Filter fields and semantics are release-dependent."),
            ("Envoy admin interface", "https://www.envoyproxy.io/docs/envoy/latest/operations/admin.html", "Loopback-only admin endpoints and their local diagnostic purpose.", "Nur auf Loopback gebundene Admin-Endpunkte und ihren lokalen Diagnosezweck.", "Do not expose the local example as a general management interface."),
            ("Envoy v1.38.2 release", "https://github.com/envoyproxy/envoy/releases/tag/v1.38.2", "Official selected release page, binary asset, and checksum material.", "Offizielle Seite des ausgewählten Releases, Binary-Asset und Prüfsummenmaterial.", "This guide pins the binary route to v1.38.2."),
            ("Envoy source/Bazel guidance", "https://github.com/envoyproxy/envoy/blob/v1.38.2/bazel/README.md", "Official optional source-build guidance; it is resource-intensive and not the default route.", "Offizielle optionale Source-Build-Anleitung; sie ist ressourcenintensiv und nicht der Standardweg.", "Use only with the selected tag and sufficient CPU, memory, and storage."),
            ("ModSecurity repository", "https://github.com/owasp-modsecurity/ModSecurity", "The libmodsecurity v3 engine source.", "Die libmodsecurity-v3-Enginequelle.", "The selected tag/commit is shown in the shared build section."),
        ),
        "connector_intro": (
            "The repository ext_proc executable is the source-built component. It links the Common/libmodsecurity bridge and is not part of an official Envoy binary. The generated host configuration uses `envoy.extensions.filters.http.ext_proc.v3.ExternalProcessor`, an HTTP/2 gRPC cluster, and a router after that filter. Build the service into an external root, then generate both configurations there.",
            "Das repository-eigene ext_proc-Executable ist die aus Source gebaute Komponente. Es linkt die Common-/libmodsecurity-Bridge und ist nicht Teil eines offiziellen Envoy-Binaries. Die erzeugte Hostkonfiguration verwendet `envoy.extensions.filters.http.ext_proc.v3.ExternalProcessor`, einen HTTP/2-gRPC-Cluster und einen Router nach diesem Filter. Den Service in einen externen Root bauen und danach beide Konfigurationen erzeugen.",
        ),
        "connector_commands": (
            'export BUILD_ROOT="$HOST_BUILD_BASE/repository-build"',
            'BUILD_ROOT="$BUILD_ROOT" MODSECURITY_INCLUDE_DIR="$MODSECURITY_INCLUDE_DIR" MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" sh "$CONNECTOR_ROOT/connectors/envoy/build/build_ext_proc.sh"',
            'export EXT_PROC_BIN="$BUILD_ROOT/envoy-ext-proc/msconnector_envoy_ext_proc"',
            'test -x "$EXT_PROC_BIN"',
            'BUILD_ROOT="$BUILD_ROOT" MODSECURITY_INCLUDE_DIR="$MODSECURITY_INCLUDE_DIR" MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" sh "$CONNECTOR_ROOT/connectors/envoy/build/test_ext_proc.sh"',
        ),
        "config_commands": (
            'export RULES_FILE="$HOST_BUILD_BASE/modsecurity-local.conf"',
            'export ENVOY_CONFIG="$BUILD_ROOT/envoy-ext-proc/config/envoy-ext-proc.yaml"',
            'export EXT_PROC_CONFIG="$CONNECTOR_ROOT/connectors/envoy/config/envoy-ext-proc-service.json"',
            'export RUNTIME_ROOT="$BUILD_ROOT/envoy-ext-proc/runtime-smoke"',
            'export EXT_PROC_RUNTIME_CONFIG="$RUNTIME_ROOT/envoy-ext-proc-runtime.conf"',
            'export ENVOY_PORT=18080',
            'export ENVOY_UPSTREAM_PORT=18081',
            'export EXT_PROC_PORT=18083',
            'export ENVOY_ADMIN_PORT=19001',
            'cat > "$RULES_FILE" <<EOF\nSecRuleEngine On\nSecRule REQUEST_URI "@streq /blocked" "id:100001,phase:1,deny,status:403,log"\nEOF',
            'OUTPUT_CONFIG="$ENVOY_CONFIG" LISTEN_PORT="$ENVOY_PORT" UPSTREAM_PORT="$ENVOY_UPSTREAM_PORT" EXT_PROC_PORT="$EXT_PROC_PORT" ADMIN_PORT="$ENVOY_ADMIN_PORT" sh "$CONNECTOR_ROOT/connectors/envoy/config/prepare_envoy_ext_proc_config.sh"',
            'OUTPUT_CONFIG="$EXT_PROC_RUNTIME_CONFIG" RULES_FILE="$RULES_FILE" EVENT_PATH="$RUNTIME_ROOT/events.jsonl" sh "$CONNECTOR_ROOT/connectors/envoy/config/prepare_envoy_ext_proc_runtime_config.sh"',
            '"$ENVOY_BIN" --mode validate -c "$ENVOY_CONFIG"',
            '"$EXT_PROC_BIN" --check-config --config "$EXT_PROC_CONFIG" --runtime-config "$EXT_PROC_RUNTIME_CONFIG"',
        ),
        "validation": (
            '"$ENVOY_BIN" --version',
            'test -x "$EXT_PROC_BIN"',
            'file "$EXT_PROC_BIN"',
            'ldd "$EXT_PROC_BIN" | grep -F libmodsecurity | grep -Fv "not found"',
            'grep -F "envoy.filters.http.ext_proc" "$ENVOY_CONFIG"',
            'grep -F "request_body_mode: STREAMED" "$ENVOY_CONFIG"',
        ),
        "http_commands": (
            'RUNTIME_ROOT="$RUNTIME_ROOT" ENVOY_BIN="$ENVOY_BIN" RULES_FILE="$RULES_FILE" ENVOY_SMOKE_PORT="$ENVOY_PORT" ENVOY_UPSTREAM_PORT="$ENVOY_UPSTREAM_PORT" ENVOY_EXT_PROC_PORT="$EXT_PROC_PORT" ENVOY_ADMIN_PORT="$ENVOY_ADMIN_PORT" EXT_PROC_RUNTIME_CONFIG="$EXT_PROC_RUNTIME_CONFIG" sh "$CONNECTOR_ROOT/connectors/envoy/harness/run_envoy_ext_proc_runtime.sh"',
            '# The bounded runner regenerates its run-local Envoy and ext_proc runtime files, then starts Envoy, ext_proc, and a loopback upstream, sends local HTTP/1.1 requests, and stops them.',
        ),
        "http_note": (
            "Run only against loopback. The bounded repository harness starts Envoy, ext_proc, and its upstream, then sends HTTP/1.1 allow and local denial probes through the generated `ext_proc` route. Its admin endpoint is loopback-only and used for local readiness diagnostics. Its results apply only to those observed requests.",
            "Nur gegen Loopback ausführen. Das begrenzte Repository-Harness startet Envoy, ext_proc und seinen Upstream und sendet dann HTTP/1.1-Allow- und lokale Deny-Probes durch die erzeugte `ext_proc`-Route. Sein Admin-Endpunkt ist nur auf Loopback gebunden und dient lokalen Readiness-Diagnosen. Seine Ergebnisse gelten nur für diese beobachteten Requests.",
        ),
        "package_queries": ('apt-cache search envoy', 'dnf search envoy', 'envoy --version 2>/dev/null || true'),
        "package_note": (
            "Packages can provide a host binary or build dependencies, but they do not include the repository ext_proc service or its Common/libmodsecurity bridge. Validate a package binary separately and retain the source-built service.",
            "Pakete können ein Hostbinary oder Buildabhängigkeiten liefern, enthalten aber nicht den repository-eigenen ext_proc-Service oder seine Common-/libmodsecurity-Bridge. Ein Paketbinary getrennt validieren und den aus Source gebauten Service beibehalten.",
        ),
        "variables": (
            ("ENVOY_VERSION", "Selected official Envoy release for the binary route.", "Ausgewählter offizieller Envoy-Release für den Binary-Weg."),
            ("ENVOY_BIN", "Verified Envoy executable.", "Verifiziertes Envoy-Executable."),
            ("ENVOY_DOWNLOAD_URL", "Official Envoy release-binary URL.", "Offizielle Envoy-Releasebinary-URL."),
            ("ENVOY_SHA256", "Expected binary checksum for the selected release.", "Erwartete Binary-Prüfsumme des ausgewählten Releases."),
            ("BUILD_ROOT", "External repository connector build root.", "Externer Build-Root des Repository-Connectors."),
            ("EXT_PROC_BIN", "Repository-built ext_proc service executable.", "Repository-gebautes ext_proc-Service-Executable."),
            ("ENVOY_CONFIG", "Generated loopback Envoy configuration.", "Erzeugte Loopback-Envoy-Konfiguration."),
            ("EXT_PROC_CONFIG", "Repository ext_proc service configuration validated with the generated runtime configuration.", "Repository-ext_proc-Servicekonfiguration, die zusammen mit der erzeugten Laufzeitkonfiguration validiert wird."),
            ("EXT_PROC_RUNTIME_CONFIG", "Generated Common runtime configuration for ext_proc.", "Erzeugte Common-Laufzeitkonfiguration für ext_proc."),
            ("OUTPUT_CONFIG", "Output path consumed by one configuration-materialization command.", "Ausgabepfad eines Konfigurationsmaterialisierungsbefehls."),
            ("EVENT_PATH", "Absolute local event-log path passed to the ext_proc runtime configuration writer.", "Absoluter lokaler Eventlog-Pfad für den ext_proc-Laufzeitkonfigurationsgenerator."),
            ("RUNTIME_ROOT", "External ephemeral root used by the bounded Envoy runtime harness.", "Externer temporärer Root des begrenzten Envoy-Laufzeitharnesses."),
            ("LISTEN_PORT", "Loopback listener port passed to the Envoy configuration materializer.", "An den Envoy-Konfigurationsgenerator übergebener Loopback-Listenerport."),
            ("UPSTREAM_PORT", "Loopback upstream port passed to the Envoy configuration materializer.", "An den Envoy-Konfigurationsgenerator übergebener Loopback-Upstream-Port."),
            ("ADMIN_PORT", "Loopback admin port passed to the Envoy configuration materializer.", "An den Envoy-Konfigurationsgenerator übergebener Loopback-Adminport."),
            ("ENVOY_PORT", "Loopback Envoy listener port.", "Loopback-Listenerport von Envoy."),
            ("ENVOY_UPSTREAM_PORT", "Loopback upstream port used by the test.", "Vom Test genutzter Loopback-Upstream-Port."),
            ("EXT_PROC_PORT", "Loopback gRPC ext_proc service port.", "Loopback-gRPC-Port des ext_proc-Service."),
            ("ENVOY_SMOKE_PORT", "Loopback listener port passed to the bounded repository Envoy harness.", "An das begrenzte Repository-Envoy-Harness übergebener Loopback-Listenerport."),
            ("ENVOY_EXT_PROC_PORT", "Loopback gRPC port passed to the bounded repository Envoy harness.", "An das begrenzte Repository-Envoy-Harness übergebener Loopback-gRPC-Port."),
            ("ENVOY_ADMIN_PORT", "Loopback Envoy admin port.", "Loopback-Adminport von Envoy."),
        ),
        "troubleshoot": (
            "An official Envoy binary is only the host. If validation fails, check the generated ext_proc YAML, gRPC port ownership, the ext_proc service configuration, and the libmodsecurity loader path; do not replace ext_proc with the separate ext_authz compatibility service.",
            "Ein offizielles Envoy-Binary ist nur der Host. Schlägt die Validierung fehl, erzeugtes ext_proc-YAML, Besitz der gRPC-Ports, ext_proc-Servicekonfiguration und libmodsecurity-Loaderpfad prüfen; ext_proc nicht durch den separaten ext_authz-Kompatibilitätsservice ersetzen.",
        ),
    },
    "traefik": {
        "components": (
            "libmodsecurity v3, Traefik, the repository native Go middleware, the C/C++ engine service, Common/libmodsecurity, a private Unix-domain socket, static and dynamic File Provider configuration, and loopback HTTP traffic.",
            "libmodsecurity v3, Traefik, die repository-eigene native Go-Middleware, der C/C++-Engine-Service, Common/libmodsecurity, ein privater Unix-Domain-Socket, statische und dynamische File-Provider-Konfiguration sowie HTTP-Traffic auf Loopback.",
        ),
        "repository_connector_title": ("Traefik connector", "Traefik-Connector"),
        "repository_connector_path": "connectors/traefik",
        "repository_connector_readme": (
            "../../../connectors/traefik/README.md",
            "../../../connectors/traefik/README.de.md",
        ),
        "repository_connector_source_links": (
            (
                "Native middleware source",
                "Native Middleware-Quelle",
                "../../../connectors/traefik/native_middleware/",
            ),
            (
                "Engine-service sources",
                "Engine-Service-Quellen",
                "../../../connectors/traefik/src/",
            ),
        ),
        "repository_connector_build_files": (
            (
                "Native middleware builder",
                "Native-Middleware-Builder",
                "../../../connectors/traefik/build/build-native-middleware.sh",
            ),
            (
                "Engine-service builder",
                "Engine-Service-Builder",
                "../../../connectors/traefik/build/build-engine-service.sh",
            ),
            (
                "Source mapping",
                "Source-Zuordnung",
                "../../../connectors/traefik/SOURCE_MAP.json",
            ),
            (
                "Native middleware static configuration",
                "Statische Konfiguration der nativen Middleware",
                "../../../connectors/traefik/config/traefik-native-middleware-static.yaml",
            ),
            (
                "Native middleware dynamic configuration",
                "Dynamische Konfiguration der nativen Middleware",
                "../../../connectors/traefik/config/traefik-native-middleware-dynamic.yaml",
            ),
        ),
        "repository_connector_build_steps": (
            "Section 7 builds the repository native middleware and its engine service; the official Traefik material only documents the host.",
            "Abschnitt 7 baut die repository-eigene native Middleware und ihren Engine-Service; das offizielle Traefik-Material dokumentiert nur den Host.",
        ),
        "alternative_connector_title": "",
        "alternative_connector_url": "",
        "alternative_connector_note": ("", ""),
        "official_sources": (
            ("Traefik Getting Started", "https://doc.traefik.io/traefik/getting-started/", "Official installation choices, entry points, routers, services, and safe local startup context.", "Offizielle Installationsoptionen, EntryPoints, Router, Services und sicherer lokaler Startkontext.", "Confirm the documentation version for the selected Traefik release."),
            ("Building and Testing", "https://doc.traefik.io/traefik/contributing/building-testing/", "Official source checkout, Go/tooling, build, and test workflow.", "Offizieller Source-Checkout sowie Go-/Tooling-, Build- und Testablauf.", "The required Go version is defined by the selected release's `go.mod`."),
            ("Traefik v3.7 configuration overview", "https://doc.traefik.io/traefik/v3.7/getting-started/configuration-overview/", "The distinction between static installation configuration and dynamic routing configuration.", "Die Unterscheidung zwischen statischer Installations- und dynamischer Routing-Konfiguration.", "Use one static configuration method and recheck it for another release."),
            ("Traefik v3.7 EntryPoints", "https://doc.traefik.io/traefik/v3.7/reference/install-configuration/entrypoints/", "Static loopback entry-point configuration.", "Statische Konfiguration der Loopback-EntryPoints.", "Field names are release-specific."),
            ("Traefik v3.7 File Provider", "https://doc.traefik.io/traefik/v3.7/reference/routing-configuration/other-providers/file/", "Dynamic File Provider routers, middleware, and services.", "Dynamische Router, Middleware und Services des File Providers.", "Recheck the selected version before using another release."),
            ("Traefik v3.7 health check", "https://doc.traefik.io/traefik/v3.7/reference/install-configuration/observability/healthcheck/", "The loopback ping endpoint used to confirm local host startup.", "Der Loopback-Ping-Endpunkt zur Bestätigung des lokalen Hoststarts.", "Do not enable an insecure dashboard for this local check."),
            ("Traefik v3.7.5 release", "https://github.com/traefik/traefik/releases/tag/v3.7.5", "Official fixed release material and checksum source.", "Offizielles festes Releasematerial und Prüfsummenquelle.", "This guide selects v3.7.5 as the repository-compatible host input."),
            ("Traefik v3.7.5 source", "https://github.com/traefik/traefik/tree/v3.7.5", "Official selected source tree; its go.mod defines the required host Go version.", "Offizieller ausgewählter Source-Baum; sein go.mod definiert die benötigte Go-Version des Hosts.", "The host's Go requirement is distinct from the repository middleware module's requirement."),
        ),
        "connector_intro": (
            "A standard Traefik binary does not include the native ModSecurity middleware or the persistent engine service. Section 7 compiles and tests the repository Go middleware package, then builds the C/C++ service outside this checkout; Section 8 stages the plugin source for the local run. The engine socket must be private to the local run and must not be reused as a shared system endpoint.",
            "Ein Standard-Traefik-Binary enthält weder die native ModSecurity-Middleware noch den persistenten Engine-Service. Abschnitt 7 kompiliert und testet das repository-eigene Go-Middleware-Paket und baut danach den C/C++-Service außerhalb dieses Checkouts; Abschnitt 8 stellt die Pluginquelle für den lokalen Lauf bereit. Der Engine-Socket muss für den lokalen Run privat sein und darf nicht als geteilter Systemendpunkt wiederverwendet werden.",
        ),
        "connector_commands": (
            'export BUILD_ROOT="$HOST_BUILD_BASE/repository-build"',
            'export TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR="$BUILD_ROOT/traefik-native-middleware"',
            'export TRAEFIK_ENGINE_SERVICE_BUILD_DIR="$BUILD_ROOT/traefik-engine-service"',
            'export TRAEFIK_ENGINE_SERVICE_BIN="$TRAEFIK_ENGINE_SERVICE_BUILD_DIR/traefik-engine-service"',
            'BUILD_ROOT="$BUILD_ROOT" TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR="$TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR" sh "$CONNECTOR_ROOT/connectors/traefik/build/build-native-middleware.sh" build',
            'BUILD_ROOT="$BUILD_ROOT" TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR="$TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR" sh "$CONNECTOR_ROOT/connectors/traefik/build/build-native-middleware.sh" test',
            'BUILD_ROOT="$BUILD_ROOT" TRAEFIK_ENGINE_SERVICE_BUILD_DIR="$TRAEFIK_ENGINE_SERVICE_BUILD_DIR" TRAEFIK_ENGINE_SERVICE_BIN="$TRAEFIK_ENGINE_SERVICE_BIN" MODSECURITY_INCLUDE_DIR="$MODSECURITY_INCLUDE_DIR" MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" sh "$CONNECTOR_ROOT/connectors/traefik/build/build-engine-service.sh" build',
            'test -x "$TRAEFIK_ENGINE_SERVICE_BIN"',
            'BUILD_ROOT="$BUILD_ROOT" TRAEFIK_ENGINE_SERVICE_BUILD_DIR="$TRAEFIK_ENGINE_SERVICE_BUILD_DIR" TRAEFIK_ENGINE_SERVICE_BIN="$TRAEFIK_ENGINE_SERVICE_BIN" MODSECURITY_INCLUDE_DIR="$MODSECURITY_INCLUDE_DIR" MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" sh "$CONNECTOR_ROOT/connectors/traefik/build/build-engine-service.sh" test',
        ),
        "config_commands": (
            'export TRAEFIK_RUNTIME_ROOT="$BUILD_ROOT/traefik-native-runtime-$(date -u +%Y%m%dT%H%M%SZ)"',
            'export RULES_FILE="$TRAEFIK_RUNTIME_ROOT/traefik-native-rules.conf"',
            'export TRAEFIK_STATIC_CONFIG="$TRAEFIK_RUNTIME_ROOT/traefik-static.yaml"',
            'export TRAEFIK_DYNAMIC_CONFIG="$TRAEFIK_RUNTIME_ROOT/traefik-dynamic.yaml"',
            'export TRAEFIK_ENGINE_CONFIG="$TRAEFIK_RUNTIME_ROOT/traefik-engine.conf"',
            'export TRAEFIK_SOCKET_DIR="$(mktemp -d /tmp/msconnector-traefik-uds.XXXXXX)"',
            'chmod 700 "$TRAEFIK_SOCKET_DIR"',
            'export TRAEFIK_ENGINE_SOCKET="$TRAEFIK_SOCKET_DIR/engine.sock"',
            'test "${#TRAEFIK_ENGINE_SOCKET}" -lt 108',
            'export TRAEFIK_PORT=18080',
            'export TRAEFIK_UPSTREAM_PORT=18081',
            'export TRAEFIK_PING_PORT=18082',
            'export TRAEFIK_PLUGIN_MODULE="github.com/Easton97-Jens/ModSecurity-conector/connectors/traefik/native_middleware"',
            'export TRAEFIK_PLUGIN_SOURCE="$TRAEFIK_RUNTIME_ROOT/plugins-local/src/$TRAEFIK_PLUGIN_MODULE"',
            'mkdir -p "$TRAEFIK_PLUGIN_SOURCE" "$TRAEFIK_RUNTIME_ROOT/logs"',
            'cp -a "$CONNECTOR_ROOT/connectors/traefik/native_middleware/." "$TRAEFIK_PLUGIN_SOURCE/"',
            'cat > "$RULES_FILE" <<EOF\nSecRuleEngine On\nSecRule REQUEST_HEADERS:X-Modsec-Smoke "@streq block" "id:100001,phase:1,deny,status:403,log"\nEOF',
            'cat > "$TRAEFIK_STATIC_CONFIG" <<EOF\nentryPoints:\n  web:\n    address: "127.0.0.1:$TRAEFIK_PORT"\n  health:\n    address: "127.0.0.1:$TRAEFIK_PING_PORT"\nproviders:\n  file:\n    filename: "$TRAEFIK_DYNAMIC_CONFIG"\n    watch: false\nping:\n  entryPoint: health\nexperimental:\n  localPlugins:\n    modsecurityNative:\n      moduleName: $TRAEFIK_PLUGIN_MODULE\n      settings:\n        envs: []\nEOF',
            'cat > "$TRAEFIK_DYNAMIC_CONFIG" <<EOF\nhttp:\n  routers:\n    native:\n      entryPoints: [web]\n      rule: "PathPrefix(`/`)"\n      middlewares: [native]\n      service: upstream\n  middlewares:\n    native:\n      plugin:\n        modsecurityNative:\n          maxHeaderCount: 128\n          maxHeaderBytes: 65536\n          maxRequestChunkBytes: 32768\n          maxResponseChunkBytes: 32768\n          transactionIDHeader: X-Request-Id\n          engineMode: uds\n          engineSocketPath: $TRAEFIK_ENGINE_SOCKET\n  services:\n    upstream:\n      loadBalancer:\n        servers:\n          - url: http://127.0.0.1:$TRAEFIK_UPSTREAM_PORT\nEOF',
            'cat > "$TRAEFIK_ENGINE_CONFIG" <<EOF\nenabled=on\nrules_file=$RULES_FILE\ntransaction_id_header=x-request-id\nrequest_body_mode=streaming\nresponse_body_mode=streaming\nrequest_body_limit=4096\nresponse_body_limit=4096\nbody_limit_action=reject\nphase4_mode=safe\ndefault_block_status=403\ndefault_error_status=500\nuse_error_log=off\nevent_path=$TRAEFIK_RUNTIME_ROOT/logs/traefik-events.jsonl\nmax_header_count=100\nmax_header_name_size=256\nmax_header_value_size=8192\nmax_total_header_bytes=65536\nmax_event_json_bytes=16384\nEOF',
            '( cd "$TRAEFIK_RUNTIME_ROOT" && "$TRAEFIK_BIN" check --configFile="$TRAEFIK_STATIC_CONFIG" )',
            '"$TRAEFIK_ENGINE_SERVICE_BIN" --check-config --config "$TRAEFIK_ENGINE_CONFIG"',
        ),
        "config_note": (
            "The configuration deliberately uses only loopback entry points and does not enable an insecure dashboard or API. Treat any dashboard or administration endpoint as optional and secure it separately for a real deployment.",
            "Die Konfiguration verwendet bewusst nur Loopback-EntryPoints und aktiviert kein unsicheres Dashboard oder API. Jedes Dashboard oder jeden Administrationsendpunkt nur optional verwenden und für einen echten Betrieb separat absichern.",
        ),
        "validation": (
            '"$TRAEFIK_BIN" version',
            'test -f "$TRAEFIK_STATIC_CONFIG"',
            'test -f "$TRAEFIK_DYNAMIC_CONFIG"',
            'test -x "$TRAEFIK_ENGINE_SERVICE_BIN"',
            'ldd "$TRAEFIK_ENGINE_SERVICE_BIN" | grep -F libmodsecurity | grep -Fv "not found"',
            'grep -F "modsecurityNative" "$TRAEFIK_STATIC_CONFIG"',
            'grep -F "engineSocketPath" "$TRAEFIK_DYNAMIC_CONFIG"',
        ),
        "http_commands": (
            'python3 -m http.server "$TRAEFIK_UPSTREAM_PORT" --bind 127.0.0.1 --directory "$TRAEFIK_RUNTIME_ROOT" > "$TRAEFIK_RUNTIME_ROOT/logs/upstream.log" 2>&1 &',
            'upstream_pid=$!',
            'LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" "$TRAEFIK_ENGINE_SERVICE_BIN" --serve --config "$TRAEFIK_ENGINE_CONFIG" --socket "$TRAEFIK_ENGINE_SOCKET" > "$TRAEFIK_RUNTIME_ROOT/logs/engine.log" 2>&1 &',
            'engine_pid=$!',
            'attempt=0\nwhile [ "$attempt" -lt 50 ] && [ ! -S "$TRAEFIK_ENGINE_SOCKET" ]; do\n    attempt=$((attempt + 1))\n    sleep 0.1\ndone',
            'test -S "$TRAEFIK_ENGINE_SOCKET"',
            'test "$(stat -c "%a" "$TRAEFIK_ENGINE_SOCKET")" = "600"',
            '( cd "$TRAEFIK_RUNTIME_ROOT" && LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" "$TRAEFIK_BIN" --configFile="$TRAEFIK_STATIC_CONFIG" ) > "$TRAEFIK_RUNTIME_ROOT/logs/traefik.log" 2>&1 &',
            'traefik_pid=$!',
            'attempt=0\nwhile [ "$attempt" -lt 50 ]; do\n    if ! kill -0 "$traefik_pid" 2>/dev/null; then\n        exit 1\n    fi\n    if curl --http1.1 -fsS "http://127.0.0.1:$TRAEFIK_PING_PORT/ping" >/dev/null; then\n        break\n    fi\n    attempt=$((attempt + 1))\n    sleep 0.1\ndone',
            'test "$attempt" -lt 50',
            'curl --http1.1 -fsS "http://127.0.0.1:$TRAEFIK_PING_PORT/ping"',
            'test "$(curl --http1.1 -sS -o /dev/null -w "%{http_code}" -H "X-Request-Id: traefik-native-allow" http://127.0.0.1:$TRAEFIK_PORT/native)" = "200"',
            'test "$(curl --http1.1 -sS -o /dev/null -w "%{http_code}" -H "X-Modsec-Smoke: block" -H "X-Request-Id: traefik-native-deny" http://127.0.0.1:$TRAEFIK_PORT/native)" = "403"',
            'kill "$traefik_pid" "$engine_pid" "$upstream_pid"',
        ),
        "http_note": (
            "Run only against loopback. `/ping` confirms host startup; the ordinary `/native` request exercises the private UDS route, and the `X-Modsec-Smoke: block` test header triggers the local 403 rule. These observations do not establish a broader claim.",
            "Nur gegen Loopback ausführen. `/ping` bestätigt den Hoststart; der normale Request auf `/native` nutzt den privaten UDS-Weg, und der Testheader `X-Modsec-Smoke: block` löst die lokale 403-Regel aus. Diese Beobachtungen begründen keinen weitergehenden Claim.",
        ),
        "package_queries": ('apt-cache search traefik', 'dnf search traefik', 'traefik version 2>/dev/null || true'),
        "package_note": (
            "A package or a separately downloaded host binary can supply Traefik itself, but neither contains the repository Go middleware, CGo/Common bridge, or UDS engine service. Keep those source-built components and validate their socket permissions.",
            "Ein Paket oder separat geladenes Hostbinary kann Traefik selbst bereitstellen, aber keines enthält die repository-eigene Go-Middleware, CGo-/Common-Bridge oder den UDS-Engine-Service. Diese aus Source gebauten Komponenten beibehalten und ihre Socket-Berechtigungen validieren.",
        ),
        "variables": (
            ("TRAEFIK_VERSION", "Repository-compatible Traefik release input.", "Repository-kompatible Traefik-Releaseeingabe."),
            ("TRAEFIK_REF", "Git tag derived from TRAEFIK_VERSION.", "Aus TRAEFIK_VERSION abgeleiteter Git-Tag."),
            ("TRAEFIK_SRC", "Pinned upstream Traefik source tree.", "Gepinnter Upstream-Traefik-Source-Baum."),
            ("TRAEFIK_BIN", "Built or otherwise verified host binary.", "Gebautes oder anderweitig verifiziertes Hostbinary."),
            ("BUILD_ROOT", "External root for repository-native outputs and runtime files.", "Externer Root für repository-native Ausgaben und Laufzeitdateien."),
            ("TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR", "External Go middleware build report directory.", "Externes Go-Middleware-Buildreport-Verzeichnis."),
            ("TRAEFIK_ENGINE_SERVICE_BUILD_DIR", "External C/C++ engine-service build directory.", "Externes C/C++-Engine-Service-Buildverzeichnis."),
            ("TRAEFIK_ENGINE_SERVICE_BIN", "Built private engine-service executable.", "Gebautes privates Engine-Service-Executable."),
            ("TRAEFIK_RUNTIME_ROOT", "Private working directory that contains the staged local plugin during a manual run.", "Privates Arbeitsverzeichnis mit dem für einen manuellen Lauf bereitgestellten lokalen Plugin."),
            ("TRAEFIK_SOCKET_DIR", "Short private directory for the run-local Unix-domain socket; its mode is 0700.", "Kurzes privates Verzeichnis für den run-lokalen Unix-Domain-Socket; sein Modus ist 0700."),
            ("TRAEFIK_STATIC_CONFIG", "Local-plugin registration configuration.", "Konfiguration der lokalen Pluginregistrierung."),
            ("TRAEFIK_DYNAMIC_CONFIG", "File Provider router/middleware configuration.", "File-Provider-Konfiguration für Router/Middleware."),
            ("TRAEFIK_ENGINE_CONFIG", "Private engine-service runtime configuration.", "Private Laufzeitkonfiguration des Engine-Service."),
            ("TRAEFIK_ENGINE_SOCKET", "Private run-local UDS endpoint, not a global path.", "Privater run-lokaler UDS-Endpunkt, kein globaler Pfad."),
            ("TRAEFIK_PLUGIN_MODULE", "Official local-plugin module path staged beneath plugins-local/src.", "Offizieller lokaler Plugin-Modulpfad unter plugins-local/src."),
            ("TRAEFIK_PLUGIN_SOURCE", "Staged source directory for the local Traefik plugin.", "Bereitgestelltes Source-Verzeichnis für das lokale Traefik-Plugin."),
            ("TRAEFIK_PORT", "Loopback web entry point for the manual test.", "Loopback-Web-EntryPoint für den manuellen Test."),
            ("TRAEFIK_UPSTREAM_PORT", "Loopback test upstream port.", "Loopback-Port des Test-Upstreams."),
            ("TRAEFIK_PING_PORT", "Loopback ping endpoint port.", "Loopback-Port des Ping-Endpunkts."),
        ),
        "troubleshoot": (
            "If Traefik starts without the middleware, check the local-plugin workspace, static registration, File Provider, and the permissions/ownership of the run-local UDS directory. A forwardAuth compatibility route does not diagnose the selected native middleware path.",
            "Wenn Traefik ohne Middleware startet, lokalen Plugin-Workspace, statische Registrierung, File Provider sowie Berechtigungen/Eigentümer des run-lokalen UDS-Verzeichnisses prüfen. Ein ForwardAuth-Kompatibilitätsweg diagnostiziert den ausgewählten nativen Middleware-Weg nicht.",
        ),
    },
    "lighttpd": {
        "components": (
            "libmodsecurity v3, lighttpd 1.4.84 source, the repository Entity-Body patch, a patched host, a matching connector module, a local runtime configuration, and loopback HTTP/1.1 traffic.",
            "libmodsecurity v3, lighttpd-1.4.84-Source, der repository-eigene Entity-Body-Patch, ein gepatchter Host, ein passendes Connectormodul, eine lokale Laufzeitkonfiguration und HTTP/1.1-Traffic auf Loopback.",
        ),
        "repository_connector_title": ("lighttpd connector", "lighttpd-Connector"),
        "repository_connector_path": "connectors/lighttpd",
        "repository_connector_readme": (
            "../../../connectors/lighttpd/README.md",
            "../../../connectors/lighttpd/README.de.md",
        ),
        "repository_connector_source_links": (
            (
                "Connector module source",
                "Connectormodul-Quelle",
                "../../../connectors/lighttpd/module/mod_msconnector.c",
            ),
            (
                "Productive lighttpd sources",
                "Produktive lighttpd-Quellen",
                "../../../connectors/lighttpd/src/",
            ),
        ),
        "repository_connector_build_files": (
            (
                "Patched-host builder",
                "Patched-Host-Builder",
                "../../../connectors/lighttpd/build/build_patched_host.sh",
            ),
            (
                "Connector module builder",
                "Connectormodul-Builder",
                "../../../connectors/lighttpd/build/build_module.sh",
            ),
            (
                "Entity-Body patch",
                "Entity-Body-Patch",
                "../../../connectors/lighttpd/patches/0001-lighttpd-1.4.84-msconnector-stream-hooks.patch",
            ),
            (
                "Source mapping",
                "Source-Zuordnung",
                "../../../connectors/lighttpd/SOURCE_MAP.json",
            ),
            (
                "Native lighttpd configuration",
                "Native-lighttpd-Konfiguration",
                "../../../connectors/lighttpd/config/lighttpd-native.conf",
            ),
        ),
        "repository_connector_build_steps": (
            "Section 7 builds the repository module against the matching patched host; official lighttpd documentation only provides the host source and host instructions.",
            "Abschnitt 7 baut das Repository-Modul gegen den passenden gepatchten Host; die offizielle lighttpd-Dokumentation stellt nur Hostquelle und Hostanleitung bereit.",
        ),
        "alternative_connector_title": "",
        "alternative_connector_url": "",
        "alternative_connector_note": ("", ""),
        "official_sources": (
            ("lighttpd INSTALL", "https://github.com/lighttpd/lighttpd1.4/blob/master/INSTALL", "Official prerequisites, Autotools/source-build, test, installation, and startup guidance.", "Offizielle Voraussetzungen sowie Autotools-/Source-Build-, Test-, Installations- und Startanleitung.", "Re-check INSTALL for the selected lighttpd release."),
            ("lighttpd Source Downloads", "https://download.lighttpd.net/lighttpd/", "Official release archives and checksum material.", "Offizielle Releasearchive und Prüfsummenmaterial.", "The latest upstream release can differ from the repository patch pin."),
            ("lighttpd Documentation", "https://redmine.lighttpd.net/projects/lighttpd/wiki", "Official configuration and command documentation when applicable to the selected host release.", "Offizielle Konfigurations- und Befehlsdokumentation, soweit sie für den ausgewählten Hostrelease gilt.", "Check accessibility and release relevance before relying on a page."),
            ("ModSecurity repository", "https://github.com/owasp-modsecurity/ModSecurity", "The libmodsecurity v3 engine source.", "Die libmodsecurity-v3-Enginequelle.", "The selected tag/commit is shown in the shared build section."),
        ),
        "connector_intro": (
            "The repository module must use the same patched source headers and generated `config.h` as the host. The source build script links it to libmodsecurity and writes the module to an external directory. The selected source host builds its index and static-file modules into the binary; Section 8 names them explicitly because compatibility module loading stays disabled. A normal lighttpd package lacks the Entity-Body hook and cannot load this selected module as an equivalent path.",
            "Das Repository-Modul muss dieselben gepatchten Source-Header und dieselbe generierte `config.h` wie der Host verwenden. Das Source-Buildskript linkt es mit libmodsecurity und schreibt das Modul in ein externes Verzeichnis. Der ausgewählte Source-Host baut seine Index- und Static-File-Module in das Binary ein; Abschnitt 8 nennt sie ausdrücklich, weil das Kompatibilitätsladen deaktiviert bleibt. Ein normales lighttpd-Paket besitzt den Entity-Body-Hook nicht und kann dieses ausgewählte Modul nicht als gleichwertigen Weg laden.",
        ),
        "connector_commands": (
            'export BUILD_ROOT="$HOST_BUILD_BASE/repository-build"',
            'export LIGHTTPD_MODULE_DIR="$BUILD_ROOT/modules"',
            'BUILD_ROOT="$BUILD_ROOT" LIGHTTPD_CONNECTOR_OUT_DIR="$BUILD_ROOT/connector" LIGHTTPD_MODULE_DIR="$LIGHTTPD_MODULE_DIR" LIGHTTPD_MSCONNECTOR_CORE_MODE=patched LIGHTTPD_SOURCE_DIR="$LIGHTTPD_PATCHED_SRC" LIGHTTPD_BUILD_ROOT="$LIGHTTPD_BUILD_DIR" MODSECURITY_INCLUDE_DIR="$MODSECURITY_INCLUDE_DIR" MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" sh "$CONNECTOR_ROOT/connectors/lighttpd/build/build_module.sh"',
            'export LIGHTTPD_MODULE="$LIGHTTPD_MODULE_DIR/mod_msconnector.so"',
            'test -f "$LIGHTTPD_MODULE"',
        ),
        "config_commands": (
            'export RULES_FILE="$HOST_BUILD_BASE/modsecurity-local.conf"',
            'export LIGHTTPD_RUNTIME_CONFIG="$HOST_BUILD_BASE/msconnector-runtime.conf"',
            'export LIGHTTPD_CONFIG="$HOST_BUILD_BASE/lighttpd-local.conf"',
            'export LIGHTTPD_DOCUMENT_ROOT="$HOST_BUILD_BASE/htdocs"',
            'mkdir -p "$LIGHTTPD_DOCUMENT_ROOT"',
            'printf "lighttpd modsecurity test\\n" > "$LIGHTTPD_DOCUMENT_ROOT/index.html"',
            'cat > "$RULES_FILE" <<EOF\nSecRuleEngine On\nSecRule REQUEST_URI "@streq /blocked" "id:100001,phase:1,deny,status:403,log"\nEOF',
            'cat > "$LIGHTTPD_RUNTIME_CONFIG" <<EOF\nrules_file=$RULES_FILE\nrequest_body_mode=none\nresponse_body_mode=none\nphase4_mode=safe\nEOF',
            'cat > "$LIGHTTPD_CONFIG" <<EOF\nserver.compat-module-load = "disable"\nserver.modules = ( "mod_indexfile", "mod_msconnector", "mod_staticfile" )\nindex-file.names = ( "index.html" )\nserver.bind = "127.0.0.1"\nserver.port = 8080\nserver.document-root = "$LIGHTTPD_DOCUMENT_ROOT"\nserver.pid-file = "$HOST_BUILD_BASE/lighttpd.pid"\nserver.errorlog = "$HOST_BUILD_BASE/lighttpd-error.log"\nmsconnector.enabled = "enable"\nmsconnector.config-file = "$LIGHTTPD_RUNTIME_CONFIG"\nEOF',
            '"$LIGHTTPD_PREFIX/sbin/lighttpd" -tt -f "$LIGHTTPD_CONFIG" -m "$LIGHTTPD_MODULE_DIR"',
        ),
        "validation": (
            '"$LIGHTTPD_PREFIX/sbin/lighttpd" -V',
            'file "$LIGHTTPD_MODULE"',
            'ldd "$LIGHTTPD_MODULE" | grep -F libmodsecurity | grep -Fv "not found"',
            'nm -D "$LIGHTTPD_MODULE" | grep -E "mod_msconnector_plugin_init$"',
            'nm "$LIGHTTPD_PREFIX/sbin/lighttpd" | grep -E "mod_(indexfile|staticfile)_plugin_init$"',
            'grep -F LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION "$LIGHTTPD_PATCHED_SRC/src/plugin.h"',
        ),
        "http_commands": (
            'LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" "$LIGHTTPD_PREFIX/sbin/lighttpd" -D -f "$LIGHTTPD_CONFIG" -m "$LIGHTTPD_MODULE_DIR" &',
            'lighttpd_pid=$!',
            'attempt=0\nwhile [ "$attempt" -lt 50 ]; do\n    if ! kill -0 "$lighttpd_pid" 2>/dev/null; then\n        exit 1\n    fi\n    if [ "$(curl -sS --connect-timeout 1 -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/ 2>/dev/null)" = "200" ]; then\n        break\n    fi\n    attempt=$((attempt + 1))\n    sleep 0.1\ndone',
            'test "$attempt" -lt 50',
            'test "$(curl -sS -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/)" = "200"',
            'test "$(curl -sS -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/blocked)" = "403"',
            'kill "$lighttpd_pid"',
        ),
        "package_queries": ('apt-cache search lighttpd', 'dnf search lighttpd', 'lighttpd -V 2>/dev/null || true'),
        "package_note": (
            "A package can supply a comparison host and prerequisites, but it cannot supply this repository's versioned Entity-Body patch or a module built with matching patched headers. It is not a package-only version of the selected path.",
            "Ein Paket kann einen Vergleichshost und Voraussetzungen liefern, aber nicht den versionierten Entity-Body-Patch dieses Repositorys oder ein Modul mit passenden gepatchten Headern. Es ist keine package-only-Version des ausgewählten Weges.",
        ),
        "variables": (
            ("LIGHTTPD_VERSION", "Exact upstream version required by the repository patch.", "Vom Repository-Patch verlangte exakte Upstream-Version."),
            ("LIGHTTPD_ARCHIVE", "Archive name derived from LIGHTTPD_VERSION.", "Aus LIGHTTPD_VERSION abgeleiteter Archivname."),
            ("LIGHTTPD_URL", "Official lighttpd source archive URL.", "Offizielle lighttpd-Sourcearchiv-URL."),
            ("LIGHTTPD_CHECKSUM_URL", "Official selected-release checksum URL.", "Offizielle Prüfsummen-URL des ausgewählten Releases."),
            ("LIGHTTPD_CHECKSUM_FILE", "Downloaded official checksum file for the selected archive.", "Geladene offizielle Prüfsummendatei für das ausgewählte Archiv."),
            ("LIGHTTPD_SHA256", "Expected selected archive checksum.", "Erwartete Prüfsumme des ausgewählten Archivs."),
            ("LIGHTTPD_SRC", "Verified unmodified upstream source tree.", "Verifizierter unveränderter Upstream-Source-Baum."),
            ("LIGHTTPD_PATCHED_SRC", "Disposable patched copy of the selected source.", "Disponierbare gepatchte Kopie der ausgewählten Quelle."),
            ("LIGHTTPD_BUILD_DIR", "Out-of-tree patched lighttpd build directory.", "Out-of-tree-Buildverzeichnis des gepatchten lighttpd."),
            ("LIGHTTPD_PREFIX", "Private patched host installation prefix.", "Privater Installationsprefix des gepatchten Hosts."),
            ("LIGHTTPD_PATCH_FILE", "Repository versioned Entity-Body patch.", "Versionierter Entity-Body-Patch des Repositorys."),
            ("LIGHTTPD_SOURCE_DIR", "Patched lighttpd source tree supplied to the connector module builder.", "Dem Connectormodul-Builder übergebener gepatchter lighttpd-Source-Baum."),
            ("LIGHTTPD_BUILD_ROOT", "Matching patched lighttpd build tree that provides generated headers and config.h.", "Passender gepatchter lighttpd-Buildbaum mit generierten Headern und config.h."),
            ("LIGHTTPD_CONNECTOR_OUT_DIR", "External intermediate output directory for the connector module build.", "Externes Zwischen-Ausgabeverzeichnis des Connectormodul-Builds."),
            ("LIGHTTPD_MSCONNECTOR_CORE_MODE", "Builder mode that requires the patched lighttpd core ABI.", "Builder-Modus, der die ABI des gepatchten lighttpd-Cores verlangt."),
            ("LIGHTTPD_MODULE_DIR", "External directory for the matching connector module.", "Externes Verzeichnis für das passende Connectormodul."),
            ("LIGHTTPD_MODULE", "Built matching module path.", "Pfad des gebauten passenden Moduls."),
            ("LIGHTTPD_RUNTIME_CONFIG", "Connector runtime rules/mode configuration.", "Connector-Laufzeitkonfiguration für Regeln/Modus."),
            ("LIGHTTPD_DOCUMENT_ROOT", "External document root containing the explicit loopback test page.", "Externes Document-Root mit der expliziten Loopback-Testseite."),
            ("LIGHTTPD_CONFIG", "Local lighttpd server configuration.", "Lokale lighttpd-Serverkonfiguration."),
        ),
        "troubleshoot": (
            "If patch dry-run fails, do not force it: verify the exact 1.4.84 source and patch checksum. If the module cannot load, rebuild the patched core and module from the same source/header/configuration set.",
            "Wenn der Patch-Dry-Run fehlschlägt, ihn nicht erzwingen: die exakte 1.4.84-Quelle und Patch-Prüfsumme prüfen. Kann das Modul nicht geladen werden, gepatchten Core und Modul aus demselben Source-/Header-/Konfigurationssatz neu bauen.",
        ),
    },
}


# The common engine guide is deliberately a small, separate model.  The first
# tuple is the only definition of the official beginner command sequence.
# Connector renderers consume the reference entries below instead of copying
# any engine-build command into their own guides.
COMMON_MODSECURITY: dict[str, object] = {
    "common_modsecurity_beginner_commands": (
        "git clone https://github.com/owasp-modsecurity/ModSecurity.git",
        "cd ModSecurity",
        "git submodule update --init --recursive",
        "git submodule status",
        "./build.sh",
        "./configure",
        "make",
        "sudo make install",
    ),
    "common_modsecurity_command_explanations": (
        (
            "Downloads the ModSecurity v3 source code.",
            "Lädt den ModSecurity-v3-Quellcode herunter.",
        ),
        (
            "Changes into the downloaded directory.",
            "Wechselt in das heruntergeladene Verzeichnis.",
        ),
        (
            "Downloads the additional required subprojects.",
            "Lädt die zusätzlich benötigten Unterprojekte.",
        ),
        (
            "Checks that the subprojects are present completely.",
            "Prüft, ob die Unterprojekte vollständig vorhanden sind.",
        ),
        (
            "Creates the required Autotools build files.",
            "Erzeugt die benötigten Autotools-Builddateien.",
        ),
        (
            "Checks compilers and libraries and creates the Makefiles.",
            "Prüft Compiler und Bibliotheken und erstellt die Makefiles.",
        ),
        (
            "Compiles libmodsecurity.",
            "Kompiliert libmodsecurity.",
        ),
        (
            "Installs headers and the library system-wide.",
            "Installiert Header und Bibliothek systemweit.",
        ),
    ),
    "common_modsecurity_advanced": {
        "commands": (
            'MODSECURITY_REF="v3.0.16"',
            'MODSECURITY_COMMIT="7ea9fefbe0ba409d8733b4d682c8c4c059cd028d"',
            'git -C ModSecurity fetch --tags origin',
            'git -C ModSecurity checkout --detach "$MODSECURITY_REF"',
            'test "$(git -C ModSecurity rev-parse HEAD)" = "$MODSECURITY_COMMIT"',
            'git -C ModSecurity verify-tag "$MODSECURITY_REF"',
            'git -C ModSecurity submodule status',
            'MODSECURITY_PREFIX="$HOME/.local/modsecurity"',
            'cd ModSecurity',
            'export CFLAGS="-O2 -g"',
            'export CXXFLAGS="-O2 -g"',
            'export LDFLAGS="-Wl,-rpath,$MODSECURITY_PREFIX/lib"',
            './configure --prefix="$MODSECURITY_PREFIX"',
            'JOBS="$(getconf _NPROCESSORS_ONLN 2>/dev/null || printf 2)"',
            'make -j"$JOBS"',
            'make check',
            'make install',
            'export PKG_CONFIG_PATH="$MODSECURITY_PREFIX/lib/pkgconfig${PKG_CONFIG_PATH:+:$PKG_CONFIG_PATH}"',
            'export LD_LIBRARY_PATH="$MODSECURITY_PREFIX/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"',
            '{ git rev-parse HEAD; git submodule status; cc --version; c++ --version; } > build-provenance.txt',
        ),
    },
    "connector_engine_reference": {
        "apache": (
            "Build libmodsecurity v3 first with the shared guide:\n\n[Build libmodsecurity v3](libmodsecurity.md)",
            "Baue zuerst libmodsecurity v3 nach der gemeinsamen Anleitung:\n\n[libmodsecurity v3 bauen](libmodsecurity.de.md)",
        ),
        "nginx": (
            "Install libmodsecurity v3 first:\n\n[Simple libmodsecurity v3 build](libmodsecurity.md)\n\nNGINX and the repository-owned NGINX connector are built afterwards.",
            "Installiere zuerst libmodsecurity v3:\n\n[Einfacher libmodsecurity-v3-Build](libmodsecurity.de.md)\n\nDanach werden NGINX und der repository-eigene NGINX-Connector gebaut.",
        ),
        "haproxy": (
            "Build libmodsecurity v3 first with the shared guide:\n\n[Build libmodsecurity v3](libmodsecurity.md)",
            "Baue zuerst libmodsecurity v3 nach der gemeinsamen Anleitung:\n\n[libmodsecurity v3 bauen](libmodsecurity.de.md)",
        ),
        "envoy": (
            "Build libmodsecurity v3 first with the shared guide:\n\n[Build libmodsecurity v3](libmodsecurity.md)",
            "Baue zuerst libmodsecurity v3 nach der gemeinsamen Anleitung:\n\n[libmodsecurity v3 bauen](libmodsecurity.de.md)",
        ),
        "traefik": (
            "Build libmodsecurity v3 first with the shared guide:\n\n[Build libmodsecurity v3](libmodsecurity.md)",
            "Baue zuerst libmodsecurity v3 nach der gemeinsamen Anleitung:\n\n[libmodsecurity v3 bauen](libmodsecurity.de.md)",
        ),
        "lighttpd": (
            "Build libmodsecurity v3 first with the shared guide:\n\n[Build libmodsecurity v3](libmodsecurity.md)",
            "Baue zuerst libmodsecurity v3 nach der gemeinsamen Anleitung:\n\n[libmodsecurity v3 bauen](libmodsecurity.de.md)",
        ),
    },
}


# Section 6 has one purpose: provide a host or proxy.  These records keep its
# beginner host flow distinct from connector integration, configuration,
# artifact checks, and runtime traffic in Sections 7–10.  Every command tuple
# is rendered unchanged in English and German.
#
# A block is: (English title, German title, English explanation, German
# explanation, shell commands).
HOST_SETUP: dict[str, dict[str, object]] = {
    "apache": {
        "host_simple_intro": (
            "For the simplest local adapter build, install an Apache package together with its development package. The development package supplies APXS and the matching headers.",
            "Für den einfachsten lokalen Adapterbuild ein Apache-Paket zusammen mit seinem Entwicklungspaket installieren. Das Entwicklungspaket liefert APXS und die passenden Header.",
        ),
        "host_simple_variables": (),
        "host_download_steps": (
            (
                "Debian / Ubuntu",
                "Debian / Ubuntu",
                "Install the host and its APXS/header package from the distribution.",
                "Host und zugehöriges APXS-/Header-Paket aus der Distribution installieren.",
                ("sudo apt update", "sudo apt install apache2 apache2-dev"),
            ),
            (
                "Fedora / RHEL",
                "Fedora / RHEL",
                "Install the corresponding httpd and development packages.",
                "Die entsprechenden httpd- und Entwicklungspakete installieren.",
                ("sudo dnf install httpd httpd-devel",),
            ),
        ),
        "host_build_steps": (),
        "host_installed": (
            "The package path provides Apache httpd, APXS, the module directory, and the headers needed to build a module for that exact host.",
            "Der Paketweg stellt Apache httpd, APXS, das Modulverzeichnis und die Header für ein Modul dieses konkreten Hosts bereit.",
        ),
        "host_success_check": (
            "These queries show the host prefix, header directory, module directory, and Apache version. They must describe the same Apache installation.",
            "Diese Abfragen zeigen Host-Prefix, Headerverzeichnis, Modulverzeichnis und Apache-Version. Sie müssen dieselbe Apache-Installation beschreiben.",
            (
                'APXS="${APXS:-$(command -v apxs || command -v apxs2)}"',
                'test -x "$APXS"',
                'HTTPD_BIN="${HTTPD_BIN:-$("$APXS" -q SBINDIR)/$("$APXS" -q PROGNAME)}"',
                '"$APXS" -q PREFIX',
                '"$APXS" -q INCLUDEDIR',
                '"$APXS" -q LIBEXECDIR',
                '"$HTTPD_BIN" -v',
            ),
        ),
        "host_source_alternative": (
            (
                "Optional: build Apache completely from source",
                "Optional: Apache vollständig aus Source bauen",
                "APR and APR-util are Apache portability libraries. Use matching system development packages, or place verified APR and APR-util source trees below srclib before configuring Apache.",
                "APR und APR-util sind Apache-Portable-Bibliotheken. Passende System-Entwicklungspakete verwenden oder verifizierte APR- und APR-util-Source-Bäume vor dem Configure unter srclib ablegen.",
                (
                    'WORKDIR="$HOME/connector-build/apache"',
                    'VERSION="2.4.68"',
                    'INSTALL_DIR="$HOME/.local/apache-modsecurity"',
                ),
            ),
            (
                "Download and unpack",
                "Herunterladen und entpacken",
                "This verifies the archive before unpacking it and creates an isolated source tree; it does not build the adapter. Import the Apache release signing key from the official download page before running the GPG check.",
                "Dies prüft das Archiv vor dem Entpacken und erstellt einen isolierten Source-Baum; der Adapter wird dadurch noch nicht gebaut. Vor der GPG-Prüfung den Apache-Release-Signaturschlüssel von der offiziellen Downloadseite importieren.",
                (
                    'mkdir -p "$WORKDIR"',
                    'cd "$WORKDIR"',
                    'curl -fLO "https://downloads.apache.org/httpd/httpd-$VERSION.tar.bz2"',
                    'curl -fLO "https://downloads.apache.org/httpd/httpd-$VERSION.tar.bz2.sha256"',
                    'curl -fLO "https://downloads.apache.org/httpd/httpd-$VERSION.tar.bz2.asc"',
                    'sha256sum -c "httpd-$VERSION.tar.bz2.sha256"',
                    'gpg --verify "httpd-$VERSION.tar.bz2.asc" "httpd-$VERSION.tar.bz2"',
                    'tar -xjf "httpd-$VERSION.tar.bz2"',
                ),
            ),
            (
                "Build the host",
                "Host bauen",
                "Configure and install Apache into the private prefix. The connector remains Section 7 work.",
                "Apache in den privaten Prefix konfigurieren und installieren. Der Connector bleibt Arbeit für Abschnitt 7.",
                (
                    'cd "$WORKDIR/httpd-$VERSION"',
                    './configure --prefix="$INSTALL_DIR" --enable-mods-shared=most --with-pcre="$(command -v pcre2-config)"',
                    "make -j2",
                    "make install",
                ),
            ),
            (
                "Check source-host outputs",
                "Source-Host-Ausgaben prüfen",
                "These checks confirm that the private source host exposes the APXS and executable pair that Section 7 must use.",
                "Diese Prüfungen bestätigen, dass der private Source-Host genau das APXS-/Executable-Paar bereitstellt, das Abschnitt 7 verwenden muss.",
                (
                    'test -x "$INSTALL_DIR/bin/httpd"',
                    'test -x "$INSTALL_DIR/bin/apachectl"',
                    'test -x "$INSTALL_DIR/bin/apxs"',
                    '"$INSTALL_DIR/bin/apxs" -q PREFIX',
                ),
            ),
        ),
        "host_advanced_verification": (),
        "source_build_is_primary": False,
        "variables": (
            ("WORKDIR", "External Apache source workspace.", "Externes Apache-Source-Arbeitsverzeichnis."),
            ("VERSION", "Selected Apache source release in the optional source path.", "Ausgewählter Apache-Source-Release im optionalen Source-Weg."),
            ("INSTALL_DIR", "Private Apache installation prefix in the optional source path.", "Privater Apache-Installationsprefix im optionalen Source-Weg."),
            ("HTTPD_BIN", "Apache executable resolved from the selected APXS installation.", "Über die ausgewählte APXS-Installation aufgelöstes Apache-Executable."),
        ),
    },
    "nginx": {
        "host_simple_intro": (
            "Download only the selected official NGINX host source. The repository source of truth currently pins `NGINX_RELEASE_TAG=release-1.31.2`, which corresponds to the official `1.31.2` archive below. This does not load a connector from another repository: the connector is already in this checkout under `connectors/nginx/`.",
            "Nur die ausgewählte offizielle NGINX-Hostquelle herunterladen. Die Repository-Source-of-Truth pinnt derzeit `NGINX_RELEASE_TAG=release-1.31.2`; dies entspricht dem unten verwendeten offiziellen Archiv `1.31.2`. Dabei wird kein Connector aus einem anderen Repository geladen: Der Connector liegt bereits in diesem Checkout unter `connectors/nginx/`.",
        ),
        "host_simple_variables": (
            'WORKDIR="$HOME/nginx-modsecurity"',
            'VERSION="1.31.2"',
        ),
        "host_download_steps": (
            (
                "Download and unpack the host source",
                "Hostquelle herunterladen und entpacken",
                "This verifies the selected NGINX archive before unpacking it and creates only the host source tree. Import the NGINX release signing key from the official release site before running the GPG check. Section 7 adds the repository-owned dynamic connector from the current checkout.",
                "Dies prüft das ausgewählte NGINX-Archiv vor dem Entpacken und erstellt nur den Host-Source-Baum. Vor der GPG-Prüfung den NGINX-Release-Signaturschlüssel von der offiziellen Release-Seite importieren. Abschnitt 7 fügt den repository-eigenen dynamischen Connector aus dem aktuellen Checkout hinzu.",
                (
                    'mkdir -p "$WORKDIR"',
                    'cd "$WORKDIR"',
                    'curl -fLO "https://nginx.org/download/nginx-$VERSION.tar.gz"',
                    'curl -fLO "https://nginx.org/download/nginx-$VERSION.tar.gz.asc"',
                    'gpg --verify "nginx-$VERSION.tar.gz.asc" "nginx-$VERSION.tar.gz"',
                    'tar -xzf "nginx-$VERSION.tar.gz"',
                ),
            ),
        ),
        "host_build_steps": (),
        "host_installed": (
            "No host binary or module has been built yet. The NGINX source is ready for Section 7, and the repository-owned connector remains in `connectors/nginx/` in this checkout.",
            "Es wurde noch kein Hostbinary oder Modul gebaut. Die NGINX-Quelle ist für Abschnitt 7 bereit, und der repository-eigene Connector bleibt in diesem Checkout unter `connectors/nginx/`.",
        ),
        "host_success_check": (
            "This file proves that the selected upstream NGINX source input was obtained.",
            "Diese Datei zeigt, dass die ausgewählte Upstream-NGINX-Source-Eingabe vorhanden ist.",
            (
                'test -f "$WORKDIR/nginx-$VERSION/configure"',
            ),
        ),
        "host_source_alternative": (),
        "host_advanced_verification": (),
        "source_build_is_primary": False,
        "variables": (
            ("WORKDIR", "External NGINX host-source workspace.", "Externes NGINX-Host-Source-Arbeitsverzeichnis."),
            ("VERSION", "Selected official NGINX release.", "Ausgewählter offizieller NGINX-Release."),
            ("INSTALL_DIR", "Private NGINX installation prefix for the dynamic-module build.", "Privater NGINX-Installationsprefix für den Dynamic-Module-Build."),
            ("JOBS", "Deliberately small number of parallel NGINX build jobs.", "Bewusst kleine Anzahl paralleler NGINX-Buildjobs."),
        ),
    },
    "haproxy": {
        "host_simple_intro": (
            "Build the exact HAProxy release required by the native HTX overlay. This is an ordinary upstream host build; the repository overlay remains Section 7 work.",
            "Den exakten HAProxy-Release bauen, den der native HTX-Overlay verlangt. Dies ist ein gewöhnlicher Upstream-Hostbuild; der Repository-Overlay bleibt Arbeit für Abschnitt 7.",
        ),
        "host_simple_variables": (
            'WORKDIR="$HOME/connector-build/haproxy"',
            'VERSION="3.2.21"',
            "JOBS=2",
        ),
        "host_download_steps": (
            (
                "Download and unpack HAProxy",
                "HAProxy herunterladen und entpacken",
                "This downloads the selected official host source into an isolated workspace.",
                "Dies lädt die ausgewählte offizielle Hostquelle in ein isoliertes Arbeitsverzeichnis.",
                (
                    'mkdir -p "$WORKDIR"',
                    'cd "$WORKDIR"',
                    'curl -fLO "https://www.haproxy.org/download/3.2/src/haproxy-$VERSION.tar.gz"',
                    'curl -fLO "https://www.haproxy.org/download/3.2/src/haproxy-$VERSION.tar.gz.sha256"',
                    'sha256sum -c "haproxy-$VERSION.tar.gz.sha256"',
                    'tar -xzf "haproxy-$VERSION.tar.gz"',
                ),
            ),
        ),
        "host_build_steps": (
            (
                "Build the upstream host",
                "Upstream-Host bauen",
                "The selected build options enable the libraries used by this local host build. They do not add the repository HTX filter.",
                "Die ausgewählten Buildoptionen aktivieren die Libraries dieses lokalen Hostbuilds. Sie fügen nicht den Repository-HTX-Filter hinzu.",
                ('cd "$WORKDIR/haproxy-$VERSION"', 'make -j"$JOBS" TARGET=linux-glibc USE_OPENSSL=1 USE_ZLIB=1 USE_PCRE2=1'),
            ),
        ),
        "host_installed": (
            "The upstream haproxy executable is built in the unpacked source tree. No staging prefix or connector overlay is part of the simple path.",
            "Das Upstream-haproxy-Executable wird im entpackten Source-Baum gebaut. Kein Staging-Prefix und kein Connector-Overlay gehören zum einfachen Weg.",
        ),
        "host_success_check": (
            "The verbose version output identifies the selected upstream binary and its enabled build features.",
            "Die ausführliche Versionsausgabe identifiziert das ausgewählte Upstream-Binary und seine aktivierten Buildfeatures.",
            ('"$WORKDIR/haproxy-$VERSION/haproxy" -vv',),
        ),
        "host_source_alternative": (),
        "host_advanced_verification": (
            (
                "Optional: stage the ordinary host",
                "Optional: gewöhnlichen Host stagen",
                "A staged installation is useful for inspection, but it is not the native HTX connector build.",
                "Eine gestagte Installation ist für die Prüfung nützlich, aber nicht der native HTX-Connectorbuild.",
                (
                    'cd "$WORKDIR/haproxy-$VERSION"',
                    'INSTALL_DIR="$HOME/.local/haproxy-modsecurity"',
                    'STAGE="$WORKDIR/stage"',
                    'make install-bin DESTDIR="$STAGE" PREFIX="$INSTALL_DIR"',
                    '"$STAGE$INSTALL_DIR/sbin/haproxy" -vv',
                ),
            ),
        ),
        "source_build_is_primary": False,
        "variables": (
            ("WORKDIR", "External HAProxy source workspace.", "Externes HAProxy-Source-Arbeitsverzeichnis."),
            ("VERSION", "Exact HAProxy version required by the HTX overlay.", "Vom HTX-Overlay verlangte exakte HAProxy-Version."),
            ("JOBS", "Deliberately small number of parallel HAProxy build jobs.", "Bewusst kleine Anzahl paralleler HAProxy-Buildjobs."),
            ("TARGET", "HAProxy host target passed to make; this guide uses linux-glibc.", "An make übergebenes HAProxy-Hosttarget; dieser Guide verwendet linux-glibc."),
            ("USE_OPENSSL", "Enable OpenSSL support for the optional ordinary host build.", "Aktiviert OpenSSL-Unterstützung für den optionalen gewöhnlichen Hostbuild."),
            ("USE_ZLIB", "Enable zlib support for the optional ordinary host build.", "Aktiviert zlib-Unterstützung für den optionalen gewöhnlichen Hostbuild."),
            ("USE_PCRE2", "Enable PCRE2 support for the optional ordinary host build.", "Aktiviert PCRE2-Unterstützung für den optionalen gewöhnlichen Hostbuild."),
            ("INSTALL_DIR", "Optional private ordinary HAProxy installation prefix.", "Optionaler privater Installationsprefix des gewöhnlichen HAProxy."),
            ("STAGE", "Optional staging root for the ordinary host installation.", "Optionaler Staging-Root der gewöhnlichen Hostinstallation."),
            ("DESTDIR", "Staging root passed directly to HAProxy's install target.", "Direkt an das HAProxy-Installationsziel übergebener Staging-Root."),
            ("PREFIX", "Installation prefix passed directly to HAProxy's install target.", "Direkt an das HAProxy-Installationsziel übergebener Installationsprefix."),
        ),
    },
    "envoy": {
        "host_simple_intro": (
            "Use the repository-compatible official Envoy release binary. The ext_proc service is a separate repository component and is built in Section 7.",
            "Das repository-kompatible offizielle Envoy-Releasebinary verwenden. Der ext_proc-Service ist eine getrennte Repository-Komponente und wird in Abschnitt 7 gebaut.",
        ),
        "host_simple_variables": ('WORKDIR="$HOME/connector-build/envoy"',),
        "host_download_steps": (
            (
                "Download the release binary",
                "Releasebinary herunterladen",
                "The official x86_64 asset is written to a local workspace and made executable.",
                "Das offizielle x86_64-Artefakt wird in ein lokales Arbeitsverzeichnis geschrieben und ausführbar gemacht.",
                (
                    'mkdir -p "$WORKDIR"',
                    'cd "$WORKDIR"',
                    'curl -fL "https://github.com/envoyproxy/envoy/releases/download/v1.38.2/envoy-1.38.2-linux-x86_64" -o envoy',
                    'printf "%s  %s\\n" "87744a1fc998d677078c9703113a192d0830badc6888662441632847fcb38899" "envoy" | sha256sum -c -',
                    "chmod 755 envoy",
                    "./envoy --version",
                ),
            ),
        ),
        "host_build_steps": (),
        "host_installed": (
            "Only the official Envoy host binary is present. It does not include the repository ext_proc executable, its Common bridge, or configuration.",
            "Es ist nur das offizielle Envoy-Hostbinary vorhanden. Es enthält weder das repository-eigene ext_proc-Executable noch seine Common-Bridge oder Konfiguration.",
        ),
        "host_success_check": (
            "The file and version checks confirm that the intended local host binary is ready for Section 7.",
            "Datei- und Versionsprüfung bestätigen, dass das beabsichtigte lokale Hostbinary für Abschnitt 7 bereit ist.",
            ('test -x "$WORKDIR/envoy"', '"$WORKDIR/envoy" --version'),
        ),
        "host_source_alternative": (
            (
                "Optional: build Envoy from source",
                "Optional: Envoy aus Source bauen",
                "A full Bazel build is resource-intensive and deliberately not part of the beginner path. Follow the [official Envoy source-build guidance](https://www.envoyproxy.io/docs/envoy/latest/start/building/local_docker_build.html) for the selected release before using it as a host override.",
                "Ein vollständiger Bazel-Build ist ressourcenintensiv und absichtlich nicht Teil des Einsteigerwegs. Vor der Nutzung als Host-Override die [offizielle Envoy-Source-Build-Anleitung](https://www.envoyproxy.io/docs/envoy/latest/start/building/local_docker_build.html) für den ausgewählten Release befolgen.",
                (),
            ),
        ),
        "host_advanced_verification": (),
        "source_build_is_primary": False,
        "variables": (("WORKDIR", "External Envoy binary workspace.", "Externes Envoy-Binary-Arbeitsverzeichnis."),),
    },
    "traefik": {
        "host_simple_intro": (
            "Use the repository-compatible official Traefik release binary. Native middleware and the engine service remain separate Section 7 components.",
            "Das repository-kompatible offizielle Traefik-Releasebinary verwenden. Native Middleware und Engine-Service bleiben getrennte Komponenten von Abschnitt 7.",
        ),
        "host_simple_variables": (
            'WORKDIR="$HOME/connector-build/traefik"',
            'VERSION="3.7.5"',
        ),
        "host_download_steps": (
            (
                "Download and unpack Traefik",
                "Traefik herunterladen und entpacken",
                "The official linux_amd64 release archive contains the host binary; no repository middleware is built here.",
                "Das offizielle linux_amd64-Releasearchiv enthält das Hostbinary; hier wird keine Repository-Middleware gebaut.",
                (
                    'mkdir -p "$WORKDIR"',
                    'cd "$WORKDIR"',
                    'curl -fLO "https://github.com/traefik/traefik/releases/download/v${VERSION}/traefik_v${VERSION}_linux_amd64.tar.gz"',
                    'curl -fLO "https://github.com/traefik/traefik/releases/download/v${VERSION}/traefik_v${VERSION}_checksums.txt"',
                    'grep "traefik_v${VERSION}_linux_amd64.tar.gz" "traefik_v${VERSION}_checksums.txt" | sha256sum -c -',
                    'tar -xzf "traefik_v${VERSION}_linux_amd64.tar.gz"',
                ),
            ),
        ),
        "host_build_steps": (),
        "host_installed": (
            "The release archive provides only the Traefik host binary. The repository native middleware, CGo/Common bridge, and UDS engine service are built later.",
            "Das Releasearchiv stellt nur das Traefik-Hostbinary bereit. Repository-native Middleware, CGo-/Common-Bridge und UDS-Engine-Service werden später gebaut.",
        ),
        "host_success_check": (
            "These checks identify the extracted host binary before the connector build starts.",
            "Diese Prüfungen identifizieren das entpackte Hostbinary, bevor der Connectorbuild beginnt.",
            ('test -x "$WORKDIR/traefik"', '"$WORKDIR/traefik" version'),
        ),
        "host_source_alternative": (
            (
                "Optional: build Traefik from source",
                "Optional: Traefik aus Source bauen",
                "Traefik v3.7.5's selected source declares Go 1.25.0 in go.mod; check that exact requirement before cloning it. This path builds only the Traefik host; the repository middleware and engine still belong to Section 7.",
                "Die ausgewählte Traefik-v3.7.5-Quelle deklariert Go 1.25.0 in go.mod; diese exakte Anforderung vor dem Klonen prüfen. Dieser Weg baut nur den Traefik-Host; Repository-Middleware und Engine bleiben Abschnitt 7.",
                (
                    "go version",
                    'git clone https://github.com/traefik/traefik.git "$WORKDIR/traefik-source"',
                    'cd "$WORKDIR/traefik-source"',
                    'git checkout --detach "v$VERSION"',
                    'grep -E "^go " go.mod',
                    'grep -Fx "go 1.25.0" go.mod',
                    "git rev-parse HEAD",
                ),
            ),
            (
                "Build the Traefik source host",
                "Traefik-Source-Host bauen",
                "The official build command and version output confirm the source-host result. The repository middleware and engine remain Section 7 work.",
                "Der offizielle Buildbefehl und die Versionsausgabe bestätigen das Source-Host-Ergebnis. Repository-Middleware und Engine bleiben Arbeit für Abschnitt 7.",
                (
                    'cd "$WORKDIR/traefik-source"',
                    "make binary",
                    'export TRAEFIK_BIN="$WORKDIR/traefik-source/dist/traefik"',
                    '"$WORKDIR/traefik-source/dist/traefik" version',
                ),
            ),
        ),
        "host_advanced_verification": (),
        "source_build_is_primary": False,
        "variables": (
            ("WORKDIR", "External Traefik host workspace.", "Externes Traefik-Host-Arbeitsverzeichnis."),
            ("VERSION", "Repository-compatible Traefik release.", "Repository-kompatibler Traefik-Release."),
        ),
    },
    "lighttpd": {
        "host_simple_intro": (
            "The selected path requires a patched lighttpd source host. The first steps download the exact version required by the repository patch; the patch and host build follow under the source-build heading. Use a fresh external workspace for a new patch run so a reviewed patched copy is never silently nested or reused.",
            "Der ausgewählte Weg benötigt einen gepatchten lighttpd-Source-Host. Die ersten Schritte laden die vom Repository-Patch verlangte exakte Version; Patch und Hostbuild folgen unter der Source-Build-Überschrift. Für einen neuen Patchlauf einen frischen externen Workspace verwenden, damit eine geprüfte gepatchte Kopie nie still verschachtelt oder wiederverwendet wird.",
        ),
        "host_simple_variables": (
            'WORKDIR="$HOME/connector-build/lighttpd"',
            'VERSION="1.4.84"',
            'INSTALL_DIR="$HOME/.local/lighttpd-modsecurity"',
        ),
        "host_download_steps": (
            (
                "Download lighttpd",
                "lighttpd herunterladen",
                "This leaves the verified upstream source untouched so that the patch is applied only to a disposable copy.",
                "Dadurch bleibt die verifizierte Upstream-Quelle unverändert; der Patch wird nur auf eine disponierbare Kopie angewendet.",
                (
                    'mkdir -p "$WORKDIR"',
                    'cd "$WORKDIR"',
                    'curl -fLO "https://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-$VERSION.tar.xz"',
                    'curl -fL "https://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-$VERSION.sha256sum" -o "lighttpd-$VERSION.sha256sum"',
                    "awk -v archive=\"lighttpd-$VERSION.tar.xz\" '$2 == archive { print }' \"lighttpd-$VERSION.sha256sum\" | sha256sum -c -",
                    'printf "%s  %s\\n" "076dd43bec8f2ba9ce6db7e7ca7e8ad72271cd529805ead2400b56efaa026f70" "lighttpd-$VERSION.tar.xz" | sha256sum -c -',
                    'tar -xJf "lighttpd-$VERSION.tar.xz"',
                ),
            ),
        ),
        "host_build_steps": (
            (
                "Create a working copy and test the patch",
                "Arbeitskopie erstellen und Patch testen",
                "The first patch command only tests whether the selected source accepts the patch. The second command changes the disposable working copy.",
                "Der erste Patchbefehl testet nur, ob die ausgewählte Quelle den Patch akzeptiert. Der zweite Befehl verändert die disponierbare Arbeitskopie.",
                (
                    'cd "$WORKDIR"',
                    'export LIGHTTPD_PATCHED_SRC="$WORKDIR/lighttpd-$VERSION-patched"',
                    'test ! -e "$LIGHTTPD_PATCHED_SRC"',
                    'cp -a "lighttpd-$VERSION" "$LIGHTTPD_PATCHED_SRC"',
                    'cd "$LIGHTTPD_PATCHED_SRC"',
                    'patch --dry-run -p1 < "$CONNECTOR_ROOT/connectors/lighttpd/patches/0001-lighttpd-1.4.84-msconnector-stream-hooks.patch"',
                    'patch -p1 < "$CONNECTOR_ROOT/connectors/lighttpd/patches/0001-lighttpd-1.4.84-msconnector-stream-hooks.patch"',
                ),
            ),
            (
                "Build the patched host",
                "Gepatchten Host bauen",
                "This builds only the patched lighttpd host. The connector module is deliberately deferred to Section 7.",
                "Dies baut nur den gepatchten lighttpd-Host. Das Connectormodul wird bewusst auf Abschnitt 7 verschoben.",
                (
                    "test -x ./autogen.sh && ./autogen.sh",
                    './configure --prefix="$INSTALL_DIR"',
                    "make -j2",
                    "make install",
                ),
            ),
        ),
        "host_installed": (
            "The private prefix contains the patched lighttpd host. It does not contain the repository connector module yet.",
            "Der private Prefix enthält den gepatchten lighttpd-Host. Er enthält noch nicht das repository-eigene Connectormodul.",
        ),
        "host_success_check": (
            "The upstream 1.4.84 installation layout places lighttpd below sbin for this prefix.",
            "Das Upstream-Installationslayout von 1.4.84 legt lighttpd für diesen Prefix unter sbin ab.",
            ('"$INSTALL_DIR/sbin/lighttpd" -V',),
        ),
        "host_source_alternative": (
            (
                "Optional: use an out-of-tree host build",
                "Optional: Out-of-tree-Hostbuild verwenden",
                "Keep this advanced alternative for comparison or reproducible build layouts; it still builds only the patched host.",
                "Diese fortgeschrittene Alternative für Vergleich oder reproduzierbare Buildlayouts beibehalten; sie baut weiterhin nur den gepatchten Host.",
                (
                    'cd "$WORKDIR/lighttpd-$VERSION-patched"',
                    './autogen.sh',
                    'export LIGHTTPD_BUILD_DIR="$WORKDIR/build-$VERSION"',
                    'mkdir -p "$LIGHTTPD_BUILD_DIR"',
                    'cd "$LIGHTTPD_BUILD_DIR"',
                    '"$WORKDIR/lighttpd-$VERSION-patched/configure" --prefix="$INSTALL_DIR"',
                    "make -j2",
                    "make check",
                    "make install",
                ),
            ),
        ),
        "host_advanced_verification": (),
        "source_build_is_primary": True,
        "variables": (
            ("WORKDIR", "External lighttpd source workspace.", "Externes lighttpd-Source-Arbeitsverzeichnis."),
            ("VERSION", "Exact lighttpd version required by the repository patch.", "Vom Repository-Patch verlangte exakte lighttpd-Version."),
            ("INSTALL_DIR", "Private patched lighttpd installation prefix.", "Privater Installationsprefix des gepatchten lighttpd."),
        ),
    },
}


# Configuration creation belongs in Section 8.  These syntax/configuration
# checks use the files written there, so render them with the other artifact
# checks in Section 9 instead of quietly validating a configuration while it
# is being written.
CONFIGURATION_VALIDATIONS: dict[str, tuple[str, ...]] = {
    "haproxy": ('"$HAPROXY_HTX_BIN" -c -f "$HAPROXY_CONFIG"',),
    "envoy": (
        '"$ENVOY_BIN" --mode validate -c "$ENVOY_CONFIG"',
        '"$EXT_PROC_BIN" --check-config --config "$EXT_PROC_CONFIG" --runtime-config "$EXT_PROC_RUNTIME_CONFIG"',
    ),
    "traefik": (
        '( cd "$TRAEFIK_RUNTIME_ROOT" && "$TRAEFIK_BIN" check --configFile="$TRAEFIK_STATIC_CONFIG" )',
        '"$TRAEFIK_ENGINE_SERVICE_BIN" --check-config --config "$TRAEFIK_ENGINE_CONFIG"',
    ),
    "lighttpd": ('"$LIGHTTPD_PREFIX/sbin/lighttpd" -tt -f "$LIGHTTPD_CONFIG" -m "$LIGHTTPD_MODULE_DIR"',),
}


# Section 16 documents the variables used by the active Section 6–10 paths,
# not historical host-model names retained in older connector metadata.
ACTIVE_MANUAL_VARIABLES: dict[str, frozenset[str]] = {
    "apache": frozenset(
        {
            "APXS",
            "HTTPD_BIN",
            "CONNECTOR_BUILD_DIR",
            "MODULE_PATH",
            "HTTPD_MODULE_DIR",
            "HTTPD_RUNTIME_ROOT",
            "HTTPD_DOCUMENT_ROOT",
            "HTTPD_MODULES",
            "HTTPD_CONFIG",
        }
    ),
    "nginx": frozenset(
        {
            "MSCONNECTOR_COMMON_INC",
            "MSCONNECTOR_COMMON_SRC",
            "MODSECURITY_INC",
            "MODSECURITY_LIB",
            "NGINX_CONFIG",
            "NGINX_DOCROOT",
        }
    ),
    "haproxy": frozenset(
        {
            "HAPROXY_SRC",
            "HAPROXY_HTX_SOURCE_DIR",
            "HAPROXY_HTX_BUILD_DIR",
            "HAPROXY_HTX_BIN",
            "MAKE_JOBS",
            "HAPROXY_CONFIG",
        }
    ),
    "envoy": frozenset(
        {
            "ENVOY_BIN",
            "EXT_PROC_BIN",
            "ENVOY_CONFIG",
            "EXT_PROC_CONFIG",
            "EXT_PROC_RUNTIME_CONFIG",
            "OUTPUT_CONFIG",
            "EVENT_PATH",
            "RUNTIME_ROOT",
            "LISTEN_PORT",
            "UPSTREAM_PORT",
            "ADMIN_PORT",
            "ENVOY_PORT",
            "ENVOY_UPSTREAM_PORT",
            "EXT_PROC_PORT",
            "ENVOY_SMOKE_PORT",
            "ENVOY_EXT_PROC_PORT",
            "ENVOY_ADMIN_PORT",
        }
    ),
    "traefik": frozenset(
        {
            "TRAEFIK_BIN",
            "TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR",
            "TRAEFIK_ENGINE_SERVICE_BUILD_DIR",
            "TRAEFIK_ENGINE_SERVICE_BIN",
            "TRAEFIK_RUNTIME_ROOT",
            "TRAEFIK_SOCKET_DIR",
            "TRAEFIK_STATIC_CONFIG",
            "TRAEFIK_DYNAMIC_CONFIG",
            "TRAEFIK_ENGINE_CONFIG",
            "TRAEFIK_ENGINE_SOCKET",
            "TRAEFIK_PLUGIN_MODULE",
            "TRAEFIK_PLUGIN_SOURCE",
            "TRAEFIK_PORT",
            "TRAEFIK_UPSTREAM_PORT",
            "TRAEFIK_PING_PORT",
        }
    ),
    "lighttpd": frozenset(
        {
            "LIGHTTPD_PATCHED_SRC",
            "LIGHTTPD_BUILD_DIR",
            "LIGHTTPD_PREFIX",
            "LIGHTTPD_SOURCE_DIR",
            "LIGHTTPD_BUILD_ROOT",
            "LIGHTTPD_CONNECTOR_OUT_DIR",
            "LIGHTTPD_MSCONNECTOR_CORE_MODE",
            "LIGHTTPD_MODULE_DIR",
            "LIGHTTPD_MODULE",
            "LIGHTTPD_RUNTIME_CONFIG",
            "LIGHTTPD_DOCUMENT_ROOT",
            "LIGHTTPD_CONFIG",
        }
    ),
}


def manual_localized(value: tuple[str, str], german: bool) -> str:
    return value[1] if german else value[0]


def fenced(language: str, body: str) -> str:
    return f"```{language}\n{body.rstrip()}\n```"


def manual_heading(number: int, english: str, german_text: str, german: bool) -> str:
    return f"## {number}. {german_text if german else english}"


def repository_connector_section(info: dict[str, object], german: bool) -> str:
    """Render the local adapter source separately from upstream host material."""
    language_index = 1 if german else 0
    title = info["repository_connector_title"][language_index]
    connector_path = info["repository_connector_path"]
    readme = info["repository_connector_readme"][language_index]
    links = [f"- [{title}]({readme})"]
    for english_title, german_title, path in info["repository_connector_source_links"]:
        links.append(f"- [{german_title if german else english_title}]({path})")
    for english_title, german_title, path in info["repository_connector_build_files"]:
        links.append(f"- [{german_title if german else english_title}]({path})")
    heading = "Connector in diesem Repository" if german else "Connector in this repository"
    primary_path = (
        f"Dies ist der primäre Connectorpfad dieser Anleitung: {connector_path}/. Die offizielle Hostdokumentation im folgenden Abschnitt erklärt nur Bereitstellung oder Build des Hosts und ersetzt nicht die Connectorquelle.",
        f"This is the primary connector path for this guide: {connector_path}/. The official host documentation in the following section explains only how to provide or build the host; it does not replace the connector source.",
    )
    return "\n\n".join(
        (
            f"## {heading}",
            "\n".join(links),
            primary_path[0] if german else primary_path[1],
            manual_localized(info["repository_connector_build_steps"], german),
        )
    )


def alternative_connector_section(info: dict[str, object], german: bool) -> str:
    """Render an upstream connector only as prose-only alternative material."""
    url = info["alternative_connector_url"]
    if not url:
        return ""
    language_index = 1 if german else 0
    title = info["alternative_connector_title"][language_index]
    heading = (
        "Alternative: offizieller Upstream-Connector"
        if german
        else "Alternative: official upstream connector"
    )
    introduction = (
        f"Der offizielle Upstream-Connector [{title}]({url}) ist eine alternative Implementierung."
        if german
        else f"The official upstream connector [{title}]({url}) is an alternative implementation."
    )
    return "\n\n".join(
        (
            f"## {heading}",
            introduction,
            manual_localized(info["alternative_connector_note"], german),
        )
    )


def manual_official_sources(info: dict[str, object], german: bool) -> str:
    rows: list[str] = []
    for title, url, english_scope, german_scope, version_scope in info["official_sources"]:
        if url == "https://github.com/owasp-modsecurity/ModSecurity":
            continue
        purpose = "Quelle und Umfang" if german else "Source and scope"
        scope = german_scope if german else english_scope
        version_label = "Versionsbezug" if german else "Version scope"
        version_text = (
            f"Dieser Bezug ist versionsabhängig; Release, Optionen und Kompatibilität vor dem Build erneut gegen die Quelle prüfen. ({version_scope})"
            if german
            else version_scope
        )
        rows.append(f"- **{purpose}:** [{title}]({url})\n  {scope} {version_label}: {version_text}")
    return "\n".join(rows)


def manual_common_variables(german: bool, slug: str) -> list[tuple[str, str]]:
    """Return only shared placeholders that are used by this guide."""
    descriptions: dict[str, tuple[str, str]] = {
        "CONNECTOR_ROOT": (
            "Git top level of this checkout; connector scripts are called from it.",
            "Git-Top-Level dieses Repository-Checkouts; die Connector-Skripte werden von dort aus aufgerufen.",
        ),
        "HOST_BUILD_BASE": (
            "Connector-specific external directory for sources, builds, configuration, and local logs.",
            "Connector-spezifisches externes Verzeichnis für Quellen, Builds, Konfiguration und lokale Logs.",
        ),
        "BUILD_ROOT": (
            "External build and runtime root for repository-owned connector components.",
            "Externer Build- und Laufzeitstamm der repository-eigenen Connector-Komponenten.",
        ),
        "RULES_FILE": (
            "Local test-rule file, not a CRS rule file.",
            "Lokale Testregeldatei; keine CRS-Regeldatei.",
        ),
        "MODSECURITY_PREFIX": (
            "libmodsecurity installation prefix. The official simple-build default is /usr/local/modsecurity.",
            "Installationsprefix von libmodsecurity. Der offizielle Standard des einfachen Builds ist /usr/local/modsecurity.",
        ),
        "MODSECURITY_INCLUDE_DIR": (
            "libmodsecurity header directory selected from MODSECURITY_PREFIX.",
            "Aus MODSECURITY_PREFIX ausgewähltes Headerverzeichnis von libmodsecurity.",
        ),
        "MODSECURITY_LIB_DIR": (
            "libmodsecurity shared-library directory selected from MODSECURITY_PREFIX; the hand-off detects lib64 when needed.",
            "Aus MODSECURITY_PREFIX ausgewähltes Shared-Library-Verzeichnis von libmodsecurity; der Handoff erkennt bei Bedarf lib64.",
        ),
        "LD_LIBRARY_PATH": (
            "Process-local loader search path used only for a documented local module or service check; do not set it globally.",
            "Nur für einen dokumentierten lokalen Modul- oder Servicecheck verwendeter Prozess-Loaderpfad; nicht global setzen.",
        ),
        "VERIFIED_RUN_PARENT": (
            "External parent for a fresh repository-test checkout and its test artifacts.",
            "Externer Elternordner eines frischen Repository-Testcheckouts und seiner Testartefakte.",
        ),
        "run_id": (
            "Unique identifier for one repository-controlled full-lifecycle run.",
            "Eindeutige Kennung eines repository-gesteuerten Full-Lifecycle-Laufs.",
        ),
        "NO_CRS_RUN_ID": (
            "Exported full-lifecycle identifier for the following Make invocation; it keeps evidence and runtime data separated.",
            "Exportierte Full-Lifecycle-Kennung für den nachfolgenden Make-Aufruf; sie hält Evidence und Laufzeitdaten getrennt.",
        ),
        "upstream_pid": (
            "Local test-upstream process ID from $!; use it only in the same shell run.",
            "Lokale Prozess-ID des Test-Upstreams aus $!; nur im selben Shell-Lauf verwenden.",
        ),
        "haproxy_pid": (
            "Local started-HAProxy process ID from $!; use it only in the same shell run.",
            "Lokale Prozess-ID des gestarteten HAProxy aus $!; nur im selben Shell-Lauf verwenden.",
        ),
        "engine_pid": (
            "Local started Traefik engine-service process ID from $!; use it only in the same shell run.",
            "Lokale Prozess-ID des gestarteten Traefik-Engine-Service aus $!; nur im selben Shell-Lauf verwenden.",
        ),
        "traefik_pid": (
            "Local started Traefik process ID from $!; use it only in the same shell run.",
            "Lokale Prozess-ID des gestarteten Traefik aus $!; nur im selben Shell-Lauf verwenden.",
        ),
        "lighttpd_pid": (
            "Local started-lighttpd process ID from $!; use it only in the same shell run.",
            "Lokale Prozess-ID des gestarteten lighttpd aus $!; nur im selben Shell-Lauf verwenden.",
        ),
    }
    common_names = (
        "CONNECTOR_ROOT",
        "RULES_FILE",
        "MODSECURITY_PREFIX",
        "MODSECURITY_INCLUDE_DIR",
        "MODSECURITY_LIB_DIR",
        "VERIFIED_RUN_PARENT",
        "run_id",
        "NO_CRS_RUN_ID",
    )
    connector_names: dict[str, tuple[str, ...]] = {
        "apache": ("LD_LIBRARY_PATH",),
        "nginx": (),
        "haproxy": ("HOST_BUILD_BASE", "LD_LIBRARY_PATH", "upstream_pid", "haproxy_pid"),
        "envoy": ("HOST_BUILD_BASE", "BUILD_ROOT"),
        "traefik": (
            "HOST_BUILD_BASE",
            "BUILD_ROOT",
            "LD_LIBRARY_PATH",
            "upstream_pid",
            "engine_pid",
            "traefik_pid",
        ),
        "lighttpd": ("HOST_BUILD_BASE", "BUILD_ROOT", "LD_LIBRARY_PATH", "lighttpd_pid"),
    }
    names = (*common_names, *connector_names[slug])
    return [
        (name, descriptions[name][1] if german else descriptions[name][0])
        for name in names
    ]


def manual_variable_table(info: dict[str, object], german: bool, slug: str) -> str:
    rows = manual_common_variables(german, slug)
    active_names = ACTIVE_MANUAL_VARIABLES[slug]
    for name, english, german_text in info["variables"]:
        if name in active_names:
            rows.append((name, german_text if german else english))
    existing = {name for name, _ in rows}
    for name, english, german_text in HOST_SETUP[slug]["variables"]:
        if name not in existing:
            rows.append((name, german_text if german else english))
            existing.add(name)
    headers = ("Variable/Platzhalter", "Bedeutung") if german else ("Variable/placeholder", "Meaning")
    return markdown_table(headers, rows)


def host_blocks(blocks: tuple[tuple[str, str, str, str, tuple[str, ...]], ...], german: bool) -> str:
    rendered: list[str] = []
    for english_title, german_title, english_text, german_text, commands in blocks:
        body = f"#### {german_title if german else english_title}\n\n{german_text if german else english_text}"
        if commands:
            body += f"\n\n{shell(commands)}"
        rendered.append(body)
    return "\n\n".join(rendered)


def shell_groups(commands: tuple[str, ...], size: int = 6) -> str:
    """Keep a numbered manual stage in one shell so its variables stay live."""
    del size
    return shell(commands)


def host_provisioning_section(slug: str, german: bool) -> str:
    setup = HOST_SETUP[slug]
    simple_heading = "### Einfacher Weg" if german else "### Simple path"
    installed_heading = "### Was wurde installiert oder gebaut?" if german else "### What was installed or built?"
    success_heading = "### Erfolg prüfen" if german else "### Check the result"
    source_heading = "### Source-Build und Integritätsprüfung" if german else "### Source build and integrity checks"
    simple_parts = [
        simple_heading,
        manual_localized(setup["host_simple_intro"], german),
    ]
    variables = tuple(setup["host_simple_variables"])
    if variables:
        simple_parts.append(shell(variables))
    download = host_blocks(tuple(setup["host_download_steps"]), german)
    if download:
        simple_parts.append(download)
    simple_build = host_blocks(tuple(setup["host_build_steps"]), german)
    source_parts = [source_heading]
    if setup["source_build_is_primary"] and simple_build:
        source_parts.append(simple_build)
    source_alternative = host_blocks(tuple(setup["host_source_alternative"]), german)
    if source_alternative:
        source_parts.append(source_alternative)
    verification = host_blocks(tuple(setup["host_advanced_verification"]), german)
    if verification:
        source_parts.append(verification)
    installed = f"{installed_heading}\n\n{manual_localized(setup['host_installed'], german)}"
    success = (
        f"{success_heading}\n\n{manual_localized(setup['host_success_check'][:2], german)}"
        f"\n\n{shell(tuple(setup['host_success_check'][2]))}"
    )
    if not setup["source_build_is_primary"] and simple_build:
        simple_parts.append(simple_build)
    if setup["source_build_is_primary"]:
        return "\n\n".join((*simple_parts, installed, "\n\n".join(source_parts), success))
    return "\n\n".join((*simple_parts, installed, success, "\n\n".join(source_parts)))


def common_modsecurity_guide(german: bool) -> str:
    """Render the common engine guide from one shared data model."""
    beginner_commands = tuple(COMMON_MODSECURITY["common_modsecurity_beginner_commands"])
    explanations = list(COMMON_MODSECURITY["common_modsecurity_command_explanations"])
    advanced = COMMON_MODSECURITY["common_modsecurity_advanced"]
    advanced_commands = tuple(advanced["commands"])
    if german:
        explanation_rows = [
            (f"`{command}`", german_text)
            for command, (_, german_text) in zip(beginner_commands, explanations, strict=True)
        ]
        sections = [
            f"{MARKER}\n\n# libmodsecurity v3 bauen",
            language_switch("libmodsecurity", True),
            "## Offizielle Quellen\n\nDie aktuelle [ModSecurity-README](https://github.com/owasp-modsecurity/ModSecurity) ist die primäre Buildquelle. Die [Compilation Recipes für v3.x](https://github.com/owasp-modsecurity/ModSecurity/wiki/Compilation-recipes-for-v3.x) dienen nur als ergänzender Hinweis für distributionsspezifische Abhängigkeiten. Historische CentOS-, Ubuntu- oder andere Beispiele daraus sind kein aktueller Standard.",
            "## Voraussetzungen\n\nBenötigt werden unter anderem:\n\n- Git\n- C- und C++-Compiler\n- GNU Make\n- Autoconf und Automake\n- libtool\n- Flex und Bison\n- YAJL\n- PCRE2\n\nDie aktuelle README nennt YAJL als Pflichtabhängigkeit und PCRE2 als Standard für reguläre Ausdrücke. Für einen kompakten Einstieg sind diese gegen aktuelle Paketquellen geprüften Namen geeignet; nur den Block der eigenen Distribution ausführen.\n\n```sh\n# Debian / Ubuntu\nsudo apt update\nsudo apt install build-essential git autoconf automake libtool flex bison pkg-config libyajl-dev libpcre2-dev\n```\n\n```sh\n# Fedora / RHEL\nsudo dnf install gcc gcc-c++ make git autoconf automake libtool flex bison pkgconf-pkg-config yajl-devel pcre2-devel\n```",
            "## Einfacher offizieller Build\n\nWenn die benötigten Entwicklungspakete bereits installiert sind, besteht der offizielle Unix-Build im Wesentlichen aus diesen acht Befehlen:\n\n"
            + shell(beginner_commands)
            + "\n\n## Bedeutung der Befehle\n\n"
            + markdown_table(("Befehl", "Bedeutung"), explanation_rows)
            + "\n\n`build.sh` kompiliert die Bibliothek noch nicht. `configure` prüft die Umgebung. `make` kompiliert. `make install` installiert das Ergebnis.",
            "## Erfolg prüfen\n\nDer Standardprefix des offiziellen einfachen Builds ist `/usr/local/modsecurity`. Die Library liegt normalerweise darunter in `lib`; bewusst gewählte Plattformlayouts können `lib64` verwenden.\n\n```sh\nls /usr/local/modsecurity/include/modsecurity\nfind /usr/local/modsecurity -maxdepth 2 -type f -name 'libmodsecurity.so*' -print\n```",
            "## Optional: Installation nur für den eigenen Benutzer\n\nNur diese Abweichung vom einfachen Ablauf verwenden:\n\n```sh\n./configure --prefix=\"$HOME/.local/modsecurity\"\nmake\nmake install\n```\n\nDabei wird nicht systemweit installiert und `sudo` ist nicht erforderlich.",
            "## Fortgeschrittene und reproduzierbare Builds\n\nDieser Abschnitt ist für bewusst gepinnte oder lokale Entwicklungsbuilds. Ein fester Release-Tag und der erwartete Commit machen die Eingabe nachvollziehbar. Eine GPG-Tag-Prüfung setzt einen vertrauenswürdigen Maintainer-Schlüssel voraus; bei Releasearchiven zusätzlich die veröffentlichte SHA-Prüfsumme vor dem Entpacken prüfen.\n\n"
            + shell(advanced_commands)
            + "\n\nHier gehören eigener Installationsprefix, `PKG_CONFIG_PATH`, `LD_LIBRARY_PATH`, parallele Buildjobs, `CFLAGS`, `CXXFLAGS`, `LDFLAGS`, `make check` und die Build-Provenienz hin. Bei `lib64` statt `lib` die Pfadangaben bewusst anpassen; `LD_LIBRARY_PATH` nur für lokale Entwicklung und Tests verwenden, nicht als globale Loader-Konfiguration.",
        ]
        return "\n\n".join(sections) + "\n"
    explanation_rows = [
        (f"`{command}`", english_text)
        for command, (english_text, _) in zip(beginner_commands, explanations, strict=True)
    ]
    sections = [
        f"{MARKER}\n\n# Build libmodsecurity v3",
        language_switch("libmodsecurity", False),
        "## Official sources\n\nThe current [ModSecurity README](https://github.com/owasp-modsecurity/ModSecurity) is the primary build source. The [v3.x compilation recipes](https://github.com/owasp-modsecurity/ModSecurity/wiki/Compilation-recipes-for-v3.x) are only supplementary context for distribution-specific dependencies. Historical CentOS, Ubuntu, or other examples there are not a current default.",
        "## Prerequisites\n\nAmong the required tools and development packages are:\n\n- Git\n- C and C++ compilers\n- GNU Make\n- Autoconf and Automake\n- libtool\n- Flex and Bison\n- YAJL\n- PCRE2\n\nThe current README identifies YAJL as mandatory and PCRE2 as the default regex engine. These compact package names were checked against current package sources; run only the block for the distribution in use.\n\n```sh\n# Debian / Ubuntu\nsudo apt update\nsudo apt install build-essential git autoconf automake libtool flex bison pkg-config libyajl-dev libpcre2-dev\n```\n\n```sh\n# Fedora / RHEL\nsudo dnf install gcc gcc-c++ make git autoconf automake libtool flex bison pkgconf-pkg-config yajl-devel pcre2-devel\n```",
        "## Simple official build\n\nOnce the required development packages are installed, the official Unix build is essentially these eight commands:\n\n"
        + shell(beginner_commands)
        + "\n\n## Meaning of the commands\n\n"
        + markdown_table(("Command", "Meaning"), explanation_rows)
        + "\n\n`build.sh` does not compile the library yet. `configure` checks the environment. `make` compiles. `make install` installs the result.",
        "## Check the result\n\nThe official simple-build default prefix is `/usr/local/modsecurity`. Its library normally lives below that prefix in `lib`; a deliberately selected platform layout can use `lib64`.\n\n```sh\nls /usr/local/modsecurity/include/modsecurity\nfind /usr/local/modsecurity -maxdepth 2 -type f -name 'libmodsecurity.so*' -print\n```",
        "## Optional: installation for the current user only\n\nShow only this deviation from the simple flow:\n\n```sh\n./configure --prefix=\"$HOME/.local/modsecurity\"\nmake\nmake install\n```\n\nThis does not install system-wide and does not require `sudo`.",
        "## Advanced and reproducible builds\n\nUse this section for deliberately pinned or local development builds. A fixed release tag and expected commit make the input traceable. GPG tag verification requires a trusted maintainer key; for release archives, also verify the published SHA checksum before unpacking.\n\n"
        + shell(advanced_commands)
        + "\n\nThis is where an own installation prefix, `PKG_CONFIG_PATH`, `LD_LIBRARY_PATH`, parallel build jobs, `CFLAGS`, `CXXFLAGS`, `LDFLAGS`, `make check`, and build provenance belong. Adjust paths deliberately when the system uses `lib64`; use `LD_LIBRARY_PATH` only for local development and tests, not as global loader configuration.",
    ]
    return "\n\n".join(sections) + "\n"


def connector_engine_reference(item: dict[str, str], german: bool) -> str:
    reference = COMMON_MODSECURITY["connector_engine_reference"][item["slug"]]
    default_paths = (
        "The following hand-off uses the official simple-build default `/usr/local/modsecurity`. Override MODSECURITY_PREFIX, MODSECURITY_INCLUDE_DIR, or MODSECURITY_LIB_DIR only for a deliberately selected installation. It checks the header and chooses `lib64` only when `lib` lacks libmodsecurity.",
        "Der folgende Handoff verwendet den offiziellen Standard des einfachen Builds `/usr/local/modsecurity`. MODSECURITY_PREFIX, MODSECURITY_INCLUDE_DIR oder MODSECURITY_LIB_DIR nur für eine bewusst gewählte Installation überschreiben. Er prüft den Header und wählt `lib64` nur, wenn `lib` libmodsecurity nicht enthält.",
    )
    apache_limit = (
        "Apache's current adapter accepts a prefix and assumes its `lib` directory, so use the normal default layout for Apache or enhance that adapter before selecting lib64.",
        "Der aktuelle Apache-Adapter akzeptiert einen Prefix und setzt dessen Verzeichnis `lib` voraus; für Apache daher das normale Standardlayout verwenden oder den Adapter vor der Auswahl von lib64 erweitern.",
    )
    commands = (
        'export MODSECURITY_PREFIX="${MODSECURITY_PREFIX:-/usr/local/modsecurity}"',
        'export MODSECURITY_INCLUDE_DIR="${MODSECURITY_INCLUDE_DIR:-$MODSECURITY_PREFIX/include}"',
        'export MODSECURITY_LIB_DIR="${MODSECURITY_LIB_DIR:-$MODSECURITY_PREFIX/lib}"',
        'if [ ! -f "$MODSECURITY_LIB_DIR/libmodsecurity.so" ] && [ -f "$MODSECURITY_PREFIX/lib64/libmodsecurity.so" ]; then\n    MODSECURITY_LIB_DIR="$MODSECURITY_PREFIX/lib64"\nfi',
        'test -f "$MODSECURITY_INCLUDE_DIR/modsecurity/modsecurity.h"',
        'test -f "$MODSECURITY_LIB_DIR/libmodsecurity.so"',
    )
    limit = f"\n\n{manual_localized(apache_limit, german)}" if item["slug"] == "apache" else ""
    return f"{manual_localized(reference, german)}\n\n{manual_localized(default_paths, german)}{limit}\n\n{shell(commands)}"


def normalized_connector_commands(commands: tuple[str, ...]) -> tuple[str, ...]:
    """Preserve the deliberate libmodsecurity hand-off in connector stages."""
    normalized: list[str] = []
    for command in commands:
        normalized.append(command.replace("$jobs", "2"))
    return tuple(normalized)


def connector_context(slug: str) -> tuple[str, ...]:
    """Reintroduce only the hand-off paths that later manual stages require."""
    contexts: dict[str, tuple[str, ...]] = {
        "haproxy": (
            'export HOST_BUILD_BASE="$HOME/connector-build/haproxy"',
            'export HAPROXY_SRC="$HOST_BUILD_BASE/haproxy-3.2.21"',
            'export HAPROXY_HTX_BUILD_DIR="$HOST_BUILD_BASE/htx-overlay"',
        ),
        "envoy": (
            'export HOST_BUILD_BASE="$HOME/connector-build/envoy"',
            'export ENVOY_BIN="$HOST_BUILD_BASE/envoy"',
        ),
        "traefik": (
            'export HOST_BUILD_BASE="$HOME/connector-build/traefik"',
            'export TRAEFIK_BIN="${TRAEFIK_BIN:-$HOST_BUILD_BASE/traefik}"',
        ),
        "lighttpd": (
            'export HOST_BUILD_BASE="$HOME/connector-build/lighttpd"',
            'export LIGHTTPD_PATCHED_SRC="$HOST_BUILD_BASE/lighttpd-1.4.84-patched"',
            'export LIGHTTPD_BUILD_DIR="${LIGHTTPD_BUILD_DIR:-$LIGHTTPD_PATCHED_SRC}"',
            'export LIGHTTPD_PREFIX="$HOME/.local/lighttpd-modsecurity"',
        ),
    }
    return contexts.get(slug, ())


def nginx_connector_build(german: bool) -> str:
    intro = (
        "Section 6 provided only the NGINX host source. The adapter-owned connector is already in this checkout under `connectors/nginx/`; build it as the selected dynamic NGINX module. The Common and libmodsecurity paths below are explicit so the dynamic module is built from the same repository and engine inputs. `make install` installs the dynamic module at the configured modules path; do not copy it a second time.",
        "Abschnitt 6 hat nur die NGINX-Hostquelle bereitgestellt. Der adaptereigene Connector liegt bereits in diesem Checkout unter `connectors/nginx/`; ihn als ausgewähltes dynamisches NGINX-Modul bauen. Die Common- und libmodsecurity-Pfade unten sind bewusst explizit, damit das dynamische Modul aus denselben Repository- und Engine-Eingaben gebaut wird. `make install` installiert das dynamische Modul in den konfigurierten Modulpfad; es nicht ein zweites Mal kopieren.",
    )
    commands = (
        'INSTALL_DIR="$HOME/.local/nginx-modsecurity"',
        "JOBS=2",
        'cd "$WORKDIR/nginx-$VERSION"',
        'MODSECURITY_INC="$MODSECURITY_INCLUDE_DIR"',
        'MODSECURITY_LIB="$MODSECURITY_LIB_DIR"',
        "\n".join(
            (
                'MSCONNECTOR_COMMON_INC="$CONNECTOR_ROOT/common/include" \\',
                'MSCONNECTOR_COMMON_SRC="$CONNECTOR_ROOT/common/src" \\',
                'MODSECURITY_INC="$MODSECURITY_INC" \\',
                'MODSECURITY_LIB="$MODSECURITY_LIB" \\',
                './configure \\',
                '  --prefix="$INSTALL_DIR" \\',
                '  --sbin-path="$INSTALL_DIR/sbin/nginx" \\',
                '  --modules-path="$INSTALL_DIR/modules" \\',
                '  --conf-path="$INSTALL_DIR/conf/nginx.conf" \\',
                '  --pid-path="$INSTALL_DIR/logs/nginx.pid" \\',
                '  --error-log-path="$INSTALL_DIR/logs/error.log" \\',
                '  --http-log-path="$INSTALL_DIR/logs/access.log" \\',
                '  --with-compat \\',
                '  --add-dynamic-module="$CONNECTOR_ROOT/connectors/nginx"',
            )
        ),
        'make -j"$JOBS"',
        "make install",
    )
    return f"{manual_localized(intro, german)}\n\n{shell_groups(commands)}"


def apache_connector_build(german: bool) -> str:
    intro = (
        "The adapter used in this guide is under [connectors/apache](../../../connectors/apache/README.md). Its productive module code is under [connectors/apache/src](../../../connectors/apache/src/). Use the APXS checked in Section 6; the package path normally exposes apxs, while the optional source-host assignment below selects the matching private APXS explicitly. The supported materialization step keeps generated Autotools templates in an external worktree while preserving connectors/apache/ as the adapter source of record.",
        "Der in dieser Anleitung verwendete Adapter befindet sich unter [connectors/apache](../../../connectors/apache/README.de.md). Der produktive Modulcode liegt unter [connectors/apache/src](../../../connectors/apache/src/). Das in Abschnitt 6 geprüfte APXS verwenden; der Paketweg stellt normalerweise apxs bereit, während die optionale Source-Host-Zuweisung unten das passende private APXS ausdrücklich auswählt. Der unterstützte Materialisierungsschritt hält erzeugte Autotools-Templates in einem externen Worktree, während connectors/apache/ die maßgebliche Adapterquelle bleibt.",
    )
    source_apxs = (
        "#### Optional: select the source-host APXS\n\nIf you built the optional Apache source host in Section 6, run this in the same shell before the adapter commands. Package-host users skip it.\n\n```sh\nAPXS=\"$HOME/.local/apache-modsecurity/bin/apxs\"\n```",
        "#### Optional: Source-Host-APXS auswählen\n\nWenn der optionale Apache-Source-Host aus Abschnitt 6 gebaut wurde, diese Zuweisung vor den Adapterbefehlen in derselben Shell ausführen. Nutzer des Pakethosts überspringen sie.\n\n```sh\nAPXS=\"$HOME/.local/apache-modsecurity/bin/apxs\"\n```",
    )
    commands = (
        'APXS="${APXS:-$(command -v apxs || command -v apxs2)}"',
        'test -x "$APXS"',
        'HTTPD_BIN="${HTTPD_BIN:-$("$APXS" -q SBINDIR)/$("$APXS" -q PROGNAME)}"',
        'cd "$CONNECTOR_ROOT/connectors/apache"',
        'test -f "$CONNECTOR_ROOT/connectors/apache/configure.ac"',
        'mkdir -p "$HOME/connector-build/apache"',
        'CONNECTOR_BUILD_DIR="$(mktemp -d "$HOME/connector-build/apache/connector-src.XXXXXX")"',
        'CONNECTOR_ROOT="$CONNECTOR_ROOT" sh "$CONNECTOR_ROOT/modules/ModSecurity-test-Framework/ci/provisioning/materialize-connector-source.sh" --connector apache --adapter-dir "$CONNECTOR_ROOT/connectors/apache" --dest-dir "$CONNECTOR_BUILD_DIR"',
        'cd "$CONNECTOR_BUILD_DIR"',
        "./autogen.sh",
        './configure --with-libmodsecurity="$MODSECURITY_PREFIX" --with-apxs="$APXS" --with-apache="$HTTPD_BIN"',
        "make -j2",
        'if [ -w "$("$APXS" -q LIBEXECDIR)" ]; then\n    make install\nelse\n    sudo make install\nfi',
        'MODULE_PATH="$("$APXS" -q LIBEXECDIR)/mod_security3.so"',
        'test -f "$MODULE_PATH"',
    )
    apache_binding_note = (
        "configure.ac accepts --with-apache as an optional lookup override, but this guide passes the httpd derived from the selected APXS explicitly. The repository build helper uses the same pairing, preventing an adapter from being configured against a different host binary.",
        "configure.ac akzeptiert --with-apache als optionales Lookup-Override, aber diese Anleitung übergibt das aus dem ausgewählten APXS abgeleitete httpd ausdrücklich. Der Repository-Buildhelper verwendet dieselbe Paarung und verhindert so, dass der Adapter gegen ein anderes Hostbinary konfiguriert wird.",
    )
    return f"{manual_localized(intro, german)}\n\n{manual_localized(source_apxs, german)}\n\n#### {'Adapter materialisieren, bauen und installieren' if german else 'Materialize, build, and install the adapter'}\n\n{manual_localized(apache_binding_note, german)}\n\n{shell_groups(commands)}"


def connector_build_section(item: dict[str, str], info: dict[str, object], german: bool) -> str:
    slug = item["slug"]
    if slug == "nginx":
        return nginx_connector_build(german)
    if slug == "apache":
        return apache_connector_build(german)
    intro = manual_localized(info["connector_intro"], german)
    commands = (
        *connector_context(slug),
        'cd "$CONNECTOR_ROOT"',
        *normalized_connector_commands(info["connector_commands"]),
    )
    handoff = (
        "The host path is reintroduced here only so that the connector commands can consume the Section 6 host without rebuilding it.",
        "Der Hostpfad wird hier nur erneut gesetzt, damit die Connectorbefehle den Host aus Abschnitt 6 verwenden können, ohne ihn erneut zu bauen.",
    )
    return f"{intro}\n\n{manual_localized(handoff, german)}\n\n{shell_groups(commands)}"


def nginx_configuration_section(info: dict[str, object], german: bool) -> str:
    intro = (
        "Create a local test rule and nginx.conf. The primary connector is a dynamic module, so nginx.conf loads it before the events and http blocks. This section writes configuration only; Section 10 validates and starts it.",
        "Eine lokale Testregel und nginx.conf erstellen. Der primäre Connector ist ein dynamisches Modul; deshalb lädt nginx.conf es vor den Blöcken events und http. Dieser Abschnitt schreibt nur Konfiguration; Abschnitt 10 validiert und startet sie.",
    )
    note = manual_localized(info["config_note"], german)
    commands = (
        'RULES_FILE="$WORKDIR/modsecurity-local.conf"',
        'NGINX_CONFIG="$INSTALL_DIR/conf/nginx.conf"',
        'NGINX_DOCROOT="$WORKDIR/htdocs"',
        'mkdir -p "$NGINX_DOCROOT"',
        'printf "nginx modsecurity test\\n" > "$NGINX_DOCROOT/index.html"',
        "cat > \"$RULES_FILE\" <<'EOF'\nSecRuleEngine On\nSecRule REQUEST_URI \"@streq /blocked\" \"id:100001,phase:1,deny,status:403,log\"\nEOF",
        'cat > "$NGINX_CONFIG" <<EOF\nload_module modules/ngx_http_modsecurity_module.so;\n\nevents {}\nhttp {\n    server {\n        listen 127.0.0.1:8080;\n        modsecurity on;\n        modsecurity_rules_file "$RULES_FILE";\n        location = /__modsec_ready {\n            modsecurity off;\n            return 204;\n        }\n        location / {\n            root "$NGINX_DOCROOT";\n            index index.html;\n        }\n    }\n}\nEOF',
    )
    return f"{manual_localized(intro, german)}\n\n{shell_groups(commands)}\n\n{note}"


def apache_configuration_section(german: bool) -> str:
    intro = (
        "Create the local test rule and an isolated, writable Apache configuration. This section does not start Apache; Section 10 performs the syntax check and loopback requests. The generated module file selects a package-host MPM and supporting DSOs when present; a source host with a static MPM remains valid without an extra MPM line.",
        "Die lokale Testregel und eine isolierte, beschreibbare Apache-Konfiguration erstellen. Dieser Abschnitt startet Apache nicht; Abschnitt 10 führt Syntaxprüfung und Loopback-Anfragen aus. Die erzeugte Moduldatei wählt bei Vorhandensein einen Pakethost-MPM und unterstützende DSOs; ein Source-Host mit statischem MPM bleibt ohne zusätzliche MPM-Zeile gültig.",
    )
    commands = (
        'APXS="${APXS:-$(command -v apxs || command -v apxs2)}"',
        'test -x "$APXS"',
        'HTTPD_BIN="${HTTPD_BIN:-$("$APXS" -q SBINDIR)/$("$APXS" -q PROGNAME)}"',
        'HTTPD_MODULE_DIR="$("$APXS" -q LIBEXECDIR)"',
        'HTTPD_RUNTIME_ROOT="$HOME/connector-build/apache/runtime"',
        'HTTPD_DOCUMENT_ROOT="$HTTPD_RUNTIME_ROOT/htdocs"',
        'HTTPD_MODULES="$HTTPD_RUNTIME_ROOT/httpd-modules.conf"',
        'RULES_FILE="$HOME/connector-build/apache/modsecurity-local.conf"',
        'HTTPD_CONFIG="$HTTPD_RUNTIME_ROOT/httpd-local.conf"',
        'mkdir -p "$HTTPD_RUNTIME_ROOT/logs" "$HTTPD_RUNTIME_ROOT/run" "$HTTPD_DOCUMENT_ROOT"',
        'printf "apache modsecurity test\\n" > "$HTTPD_DOCUMENT_ROOT/index.html"',
        ': > "$HTTPD_MODULES"',
        'for mpm in mpm_event mpm_worker mpm_prefork; do\n    if [ -f "$HTTPD_MODULE_DIR/mod_$mpm.so" ]; then\n        printf "LoadModule %s_module \\"%s/mod_%s.so\\"\\n" "$mpm" "$HTTPD_MODULE_DIR" "$mpm" >> "$HTTPD_MODULES"\n        break\n    fi\ndone',
        'for module in authz_core authz_host mime dir unixd; do\n    if [ -f "$HTTPD_MODULE_DIR/mod_$module.so" ]; then\n        printf "LoadModule %s_module \\"%s/mod_%s.so\\"\\n" "$module" "$HTTPD_MODULE_DIR" "$module" >> "$HTTPD_MODULES"\n    fi\ndone',
        'cat > "$RULES_FILE" <<EOF\nSecRuleEngine On\nSecRule REQUEST_URI "@streq /blocked" "id:100001,phase:1,deny,status:403,log"\nEOF',
        'cat > "$HTTPD_CONFIG" <<EOF\nServerRoot "$HTTPD_RUNTIME_ROOT"\nPidFile "run/httpd.pid"\nDefaultRuntimeDir "run"\nListen 127.0.0.1:8080\nServerName 127.0.0.1\nErrorLog "logs/error.log"\nInclude "$HTTPD_MODULES"\nLoadModule security3_module "$MODULE_PATH"\nDocumentRoot "$HTTPD_DOCUMENT_ROOT"\n<Directory "$HTTPD_DOCUMENT_ROOT">\n    Require all granted\n</Directory>\n<Location "/">\n    modsecurity on\n    modsecurity_rules_file "$RULES_FILE"\n</Location>\nEOF',
    )
    return f"{manual_localized(intro, german)}\n\n{shell_groups(commands)}"


def configuration_section(item: dict[str, str], info: dict[str, object], german: bool) -> str:
    if item["slug"] == "nginx":
        return nginx_configuration_section(info, german)
    if item["slug"] == "apache":
        return apache_configuration_section(german)
    intro = (
        "The local rule below is a test rule, not a CRS rule. Keep configuration and runtime files outside the Git checkout.",
        "Die folgende lokale Regel ist eine Testregel und keine CRS-Regel. Konfigurations- und Laufzeitdateien außerhalb des Git-Checkouts halten.",
    )
    note = "\n\n" + manual_localized(info["config_note"], german) if "config_note" in info else ""
    validation_commands = CONFIGURATION_VALIDATIONS.get(item["slug"], ())
    commands = tuple(
        command for command in info["config_commands"] if command not in validation_commands
    )
    return f"{manual_localized(intro, german)}{note}\n\n{shell_groups(normalized_connector_commands(commands))}"


def nginx_validation_section(german: bool) -> str:
    commands = (
        'test -x "$INSTALL_DIR/sbin/nginx"',
        'test -f "$INSTALL_DIR/modules/ngx_http_modsecurity_module.so"',
        '"$INSTALL_DIR/sbin/nginx" -V',
        '"$INSTALL_DIR/sbin/nginx" -V 2>&1 | grep -F -- "--add-dynamic-module=$CONNECTOR_ROOT/connectors/nginx"',
        'file "$INSTALL_DIR/modules/ngx_http_modsecurity_module.so"',
        'ldd "$INSTALL_DIR/modules/ngx_http_modsecurity_module.so" | grep -F libmodsecurity | grep -Fv "not found"',
        'test -f "$RULES_FILE"',
        'test -f "$NGINX_CONFIG"',
    )
    return shell_groups(commands)


def apache_validation_section(german: bool) -> str:
    commands = (
        '"$HTTPD_BIN" -v',
        '"$HTTPD_BIN" -M | grep -E "(^|[[:space:]])so_module"',
        '"$APXS" -q PREFIX',
        '"$APXS" -q INCLUDEDIR',
        '"$APXS" -q LIBEXECDIR',
        'file "$MODULE_PATH"',
        'LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" ldd "$MODULE_PATH" | grep -F libmodsecurity | grep -Fv "not found"',
    )
    return shell_groups(commands)


def validation_section(item: dict[str, str], info: dict[str, object], german: bool) -> str:
    if item["slug"] == "nginx":
        return nginx_validation_section(german)
    if item["slug"] == "apache":
        return apache_validation_section(german)
    commands = (*CONFIGURATION_VALIDATIONS.get(item["slug"], ()), *info["validation"])
    return shell_groups(normalized_connector_commands(commands))


def nginx_runtime_section(german: bool) -> str:
    intro = (
        "Run the syntax check first, then start the local host, send one ordinary and one blocked loopback request, and stop it.",
        "Zuerst die Syntax prüfen, dann den lokalen Host starten, eine normale und eine geblockte Loopback-Anfrage senden und ihn wieder stoppen.",
    )
    commands = (
        '"$INSTALL_DIR/sbin/nginx" -t -p "$INSTALL_DIR" -c conf/nginx.conf',
        '"$INSTALL_DIR/sbin/nginx" -p "$INSTALL_DIR" -c conf/nginx.conf',
        'test "$(curl -sS -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/)" = "200"',
        'test "$(curl -sS -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/blocked)" = "403"',
        '"$INSTALL_DIR/sbin/nginx" -p "$INSTALL_DIR" -c conf/nginx.conf -s quit',
    )
    return f"{manual_localized(intro, german)}\n\n{shell_groups(commands)}"


def apache_runtime_section(german: bool) -> str:
    commands = (
        'LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" "$HTTPD_BIN" -d "$HTTPD_RUNTIME_ROOT" -f "$HTTPD_CONFIG" -t',
        'LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" "$HTTPD_BIN" -d "$HTTPD_RUNTIME_ROOT" -f "$HTTPD_CONFIG" -k start',
        'test "$(curl -sS -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/)" = "200"',
        'test "$(curl -sS -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/blocked)" = "403"',
        'LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" "$HTTPD_BIN" -d "$HTTPD_RUNTIME_ROOT" -f "$HTTPD_CONFIG" -k stop',
    )
    return shell_groups(commands)


def runtime_section(item: dict[str, str], info: dict[str, object], german: bool) -> str:
    if item["slug"] == "nginx":
        return nginx_runtime_section(german)
    if item["slug"] == "apache":
        return apache_runtime_section(german)
    return shell_groups(normalized_connector_commands(info["http_commands"]))


# The detailed engine build used to live in every connector guide.  It is now
# rendered only by common_modsecurity_guide() from COMMON_MODSECURITY.


def repository_test_path(item: dict[str, str], german: bool) -> str:
    slug = item["slug"]
    flow = (
        'export VERIFIED_RUN_PARENT="$HOME/modsecurity-connector-work"',
        'mkdir -p "$VERIFIED_RUN_PARENT"',
        'cd "$VERIFIED_RUN_PARENT"',
        'git clone --recurse-submodules https://github.com/Easton97-Jens/ModSecurity-conector.git',
        'cd ModSecurity-conector',
        'git switch feature/all-connectors-no-crs-baseline',
        'git submodule update --init --recursive',
        'make check-framework',
        'make prepare-runtime-components',
        f'make {item["build"]}',
        f'make {item["config"]}',
        f'make {item["start"]}',
        f'make {item["runtime"]}',
        f'run_id="{slug}-core-$(date -u +%Y%m%dT%H%M%SZ)"',
        f'NO_CRS_RUN_ID="$run_id" make {item["full"]}',
        f'NO_CRS_RUN_ID="$run_id" make evidence-check-{slug}',
    )
    explanation = (
        "This section follows the manual build. The targets automate and test the build and integration steps described above; they do not replace their technical documentation. Exit `77` means a deliberately blocked prerequisite, and one successful target is not a broader release claim.",
        "Dieser Abschnitt folgt nach dem manuellen Build. Die Targets automatisieren und testen die zuvor beschriebenen Build- und Integrationsschritte; sie ersetzen nicht deren technische Dokumentation. Exit `77` bedeutet eine bewusst blockierte Voraussetzung, und ein einzelner Target-Erfolg ist keine weitergehende Freigabe.",
    )
    return f"{manual_localized(explanation, german)}\n\n{shell(flow)}"


def source_first_guide(item: dict[str, str], german: bool) -> str:
    slug = item["slug"]
    info = MANUAL_GUIDES[slug]
    name = item["name_de"] if german else item["name"]
    purpose = (
        f"This guide describes the manual development and integration build for `{item['profile']}` on {name}. The manual source build is the primary path; the repository test path follows it as an automated verification route.",
        f"Dieser Guide beschreibt den manuellen Entwicklungs- und Integrationsbuild für `{item['profile']}` bei {name}. Der manuelle Source-Build ist der Hauptpfad; der Repository-Testweg folgt danach als automatisierte Prüfstrecke.",
    )
    prereqs = (
        "Build libmodsecurity first with the shared guide. Then install the selected host's documented development tools and keep the host, connector, headers, and libraries compatible.",
        "Zuerst libmodsecurity mit der gemeinsamen Anleitung bauen. Danach die dokumentierten Entwicklungswerkzeuge des ausgewählten Hosts installieren und Host, Connector, Header sowie Libraries kompatibel halten.",
    )
    prereq_commands = (
        'command -v git cc c++ make',
        'export CONNECTOR_ROOT="$(git rev-parse --show-toplevel)"',
        'test -f "$CONNECTOR_ROOT/Makefile"',
    )
    go_prereqs: dict[str, tuple[str, str, tuple[str, ...]]] = {
        "envoy": (
            "The repository ext_proc module requires the exact pinned Go 1.26 patch declared in its go.mod; verify that directive before its Section 7 build.",
            "Das repository-eigene ext_proc-Modul verlangt den exakt gepinnten Go-1.26-Patch aus seinem go.mod; diese Direktive vor dem Build in Abschnitt 7 prüfen.",
            ('go version', 'grep -Ex "go 1\\.26\\.[0-9]+" "$CONNECTOR_ROOT/connectors/envoy/ext_proc/go.mod"'),
        ),
        "traefik": (
            "The repository native middleware module requires the exact pinned Go 1.26 patch declared in its go.mod; this differs from the optional Traefik-v3.7.5 host-source requirement in Section 6.",
            "Das repository-eigene native Middleware-Modul verlangt den exakt gepinnten Go-1.26-Patch aus seinem go.mod; dies unterscheidet sich von der optionalen Traefik-v3.7.5-Host-Source-Anforderung in Abschnitt 6.",
            ('go version', 'grep -Ex "go 1\\.26\\.[0-9]+" "$CONNECTOR_ROOT/connectors/traefik/native_middleware/go.mod"'),
        ),
    }
    go_prereq = go_prereqs.get(slug)
    package_intro = (
        f"Status: `{DETAILS[item['slug']]['package_status']}`. Package queries deliberately precede installation. Use only the line matching the distribution.",
        f"Status: `{DETAILS[item['slug']]['package_status']}`. Paketabfragen sind absichtlich vor einer Installation platziert. Nur die zur Distribution passende Zeile verwenden.",
    )
    update_commands = (
        'git -C "$CONNECTOR_ROOT" pull --ff-only',
        'git -C "$CONNECTOR_ROOT" submodule update --init --recursive',
        '# Rebuild the selected host and connector with the commands above.',
    )
    cleanup_paths: dict[str, tuple[str, ...]] = {
        "apache": ("$HOME/connector-build/apache", "$HOME/.local/apache-modsecurity", "$HOME/modsecurity-connector-work"),
        "nginx": ("$HOME/nginx-modsecurity", "$HOME/.local/nginx-modsecurity", "$HOME/modsecurity-connector-work"),
        "haproxy": ("$HOME/connector-build/haproxy", "$HOME/.local/haproxy-modsecurity", "$HOME/modsecurity-connector-work"),
        "envoy": ("$HOME/connector-build/envoy", "$HOME/modsecurity-connector-work"),
        "traefik": ("$HOME/connector-build/traefik", "$HOME/modsecurity-connector-work"),
        "lighttpd": ("$HOME/connector-build/lighttpd", "$HOME/.local/lighttpd-modsecurity", "$HOME/modsecurity-connector-work"),
    }
    cleanup_commands = (
        *(f'test ! -e "{path}" || find "{path}" -maxdepth 2 -mindepth 1 -print' for path in cleanup_paths[slug]),
        *(('test -z "${TRAEFIK_SOCKET_DIR:-}" || test ! -e "$TRAEFIK_SOCKET_DIR" || find "$TRAEFIK_SOCKET_DIR" -maxdepth 2 -mindepth 1 -print',) if slug == "traefik" else ()),
        '# Review the listed external paths first; remove only a chosen host-build or test directory.',
    )
    boundary = (
        "These instructions describe a reproducible development and integration build. They are not a production release. They do not claim complete CRS coverage, a complete protocol or platform matrix, or package-path equivalence when a host patch, module, middleware, or service is absent.",
        "Diese Anleitung beschreibt einen nachvollziehbaren Entwicklungs- und Integrationsbuild. Sie ist keine Produktionsfreigabe. Sie behauptet keine vollständige CRS-Abdeckung, keine vollständige Protokoll- oder Plattformmatrix und keine Gleichwertigkeit eines Paketwegs, wenn Hostpatch, Modul, Middleware oder Service fehlen.",
    )
    update_note = (
        "Before an update, recheck the linked upstream documentation, release version, and configure/build options. Then repeat every affected host, connector, ABI, and local HTTP test.",
        "Vor einem Update immer die verlinkte Upstream-Anleitung, Releaseversion sowie Configure-/Buildoptionen erneut prüfen. Anschließend alle betroffenen Host-, Connector-, ABI- und lokalen HTTP-Tests wiederholen.",
    )
    cleanup_note = (
        "Do not copy files indiscriminately to `/usr/lib` and do not remove global directories. A user prefix does not need `sudo`. Remove evidence or logs only after deliberate review.",
        "Keine Dateien pauschal nach `/usr/lib` kopieren und keine globalen Verzeichnisse entfernen. Bei einem Benutzer-Prefix ist kein `sudo` nötig. Evidence oder Logs erst nach bewusster Prüfung entfernen.",
    )
    trouble_prefix = (
        "Common: for missing headers or libraries, return to the shared guide's advanced section and check the deliberately selected prefix and pkg-config output. For an ABI failure, rebuild host, headers, and connector from the same selected source set.",
        "Gemeinsam: Bei fehlenden Headern oder Libraries zum fortgeschrittenen Abschnitt der gemeinsamen Anleitung zurückkehren und den bewusst gewählten Prefix sowie die pkg-config-Ausgabe prüfen. Bei einem ABI-Fehler Host, Header und Connector aus demselben ausgewählten Quellensatz neu bauen.",
    )
    host_build = host_provisioning_section(slug, german)
    connector_build = connector_build_section(item, info, german)
    configuration = configuration_section(item, info, german)
    validation = validation_section(item, info, german)
    http_test = runtime_section(item, info, german)
    variables = manual_variable_table(info, german, slug)
    return f"""{MARKER}

# {"Manueller Source-Build" if german else "Manual source build"}: {name}

{language_switch(item['slug'], german)}

{manual_heading(1, "Purpose and selected integration path", "Zweck und ausgewählter Integrationspfad", german)}

{manual_localized(purpose, german)}

{manual_heading(2, "Build components", "Komponenten des Builds", german)}

{manual_localized(info['components'], german)}

{repository_connector_section(info, german)}

{manual_heading(3, "Official upstream documentation", "Offizielle Upstream-Dokumentation", german)}

{manual_official_sources(info, german)}

{alternative_connector_section(info, german)}

{manual_heading(4, "Prerequisites", "Voraussetzungen", german)}

{manual_localized(prereqs, german)}

{shell(prereq_commands)}

{manual_localized(go_prereq[:2], german) + "\n\n" + shell(go_prereq[2]) if go_prereq else ""}

{manual_heading(5, "Prepare libmodsecurity v3", "ModSecurity vorbereiten", german)}

{connector_engine_reference(item, german)}

{manual_heading(6, "Provide the host or proxy", "Host oder Proxy bereitstellen", german)}

{host_build}

{manual_heading(7, "Build and integrate the connector", "Connector bauen und einbinden", german)}

{connector_build}

{manual_heading(8, "Configuration", "Konfiguration", german)}

{configuration}

{manual_heading(9, "Build and ABI validation", "Build- und ABI-Validierung", german)}

{("Validate the selected host, connector artifact, dynamic library resolution, and generated configuration before sending traffic." if not german else "Ausgewählten Host, Connector-Artefakt, Auflösung dynamischer Libraries und erzeugte Konfiguration vor dem Senden von Traffic validieren.")}

{validation}

{manual_heading(10, "Local HTTP/1.1 functional test", "Lokaler HTTP/1.1-Funktionstest", german)}

{manual_localized(info['http_note'], german) if 'http_note' in info else ("Run only against loopback. A 200 response on `/` and a 403 response on `/blocked` demonstrate the local rule path; they do not establish a broader claim." if not german else "Nur gegen Loopback ausführen. Eine 200-Antwort auf `/` und eine 403-Antwort auf `/blocked` zeigen den lokalen Regelweg; sie begründen keinen weitergehenden Claim.")}

{http_test}

{manual_heading(11, "Package-assisted path", "Paketgestützter Weg", german)}

{manual_localized(package_intro, german)}

{("Treat the host package, its matching development/API package, and connector build dependencies as separate inputs. The queries below establish local availability before a package name is selected; the final command prints the candidate host version. The connector component described above remains a source build whenever the selected module, service, middleware, or host patch is not part of that package." if not german else "Hostpaket, dazu passendes Entwicklungs-/API-Paket und Connector-Buildabhängigkeiten als getrennte Eingaben behandeln. Die folgenden Abfragen klären zunächst die lokale Verfügbarkeit; der letzte Befehl gibt die Kandidaten-Hostversion aus. Die oben beschriebene Connector-Komponente bleibt ein Source-Build, wenn das ausgewählte Modul, der Service, die Middleware oder der Hostpatch nicht Bestandteil dieses Pakets ist.")}

{shell(info['package_queries'])}

{manual_localized(info['package_note'], german)}

{manual_heading(12, "Repository-controlled test path", "Repository-gesteuerter Testweg", german)}

{repository_test_path(item, german)}

{manual_heading(13, "Update and rebuild", "Aktualisieren und neu bauen", german)}

{manual_localized(update_note, german)}

{shell(update_commands)}

{manual_heading(14, "Uninstall and cleanup", "Deinstallation und Cleanup", german)}

{manual_localized(cleanup_note, german)}

{shell(cleanup_commands)}

{manual_heading(15, "Troubleshooting", "Troubleshooting", german)}

{manual_localized(trouble_prefix, german)}

{manual_localized(info['troubleshoot'], german)}

{manual_heading(16, "Variables and placeholders", "Variablen und Platzhalter", german)}

{variables}

{manual_heading(17, "Boundaries and non-claims", "Grenzen und nicht erhobene Claims", german)}

{manual_localized(boundary, german)}
"""


def rendered_files() -> dict[str, str]:
    """Return every generated compiler-guide file without writing it."""
    rendered = {
        "README.md": generated_index(False),
        "README.de.md": generated_index(True),
        "overview.md": generated_overview(False),
        "overview.de.md": generated_overview(True),
        "libmodsecurity.md": common_modsecurity_guide(False),
        "libmodsecurity.de.md": common_modsecurity_guide(True),
    }
    for item in CONNECTORS:
        rendered[f"{item['slug']}.md"] = source_first_guide(item, False)
        rendered[f"{item['slug']}.de.md"] = source_first_guide(item, True)
    return rendered


def generated_index(german: bool) -> str:
    rows = []
    for item in CONNECTORS:
        info = detail(item)
        guide_name = item["name_de"] if german else item["name"]
        suffix = ".de" if german else ""
        rows.append((f"[{guide_name}]({item['slug']}{suffix}.md)", f"`make {item['build']}`", f"`make {item['full']}`", f"`{info['package_status']}`", f"`{item['profile']}`"))
    if german:
        return f"""{MARKER}

# Compiler-, Source-Build- und Paketwege

**Sprache:** [English](README.md) | Deutsch

## Zweck

Jeder Detailguide beschreibt einen repository-gesteuerten Testweg, einen
lokalen Source-Build und einen ehrlichen Paketweg. Ein Build, Link,
Config-Check, Start oder Paketinstallationsresultat ist für sich allein keine
Runtime-, CRS-, Sicherheits-, Produktions- oder Vollmatrix-Evidence.

## Gemeinsamer Einstieg

Vor jedem Connector zuerst [libmodsecurity v3 bauen](libmodsecurity.de.md).
Der Einsteigerablauf steht nur dort; die Connector-Guides beginnen danach mit
ihrem jeweiligen Host und Connector.

## Entscheidungsmatrix

{markdown_table(("Connector", "Testweg", "Source-Build", "Paketstatus", "Ausgewählter Kernpfad"), rows)}

## Entscheidungsbaum

Nur testen?
→ Repository-Testweg verwenden.

Eigene Builds oder Änderungen entwickeln?
→ Lokalen Source-Build mit externem `VERIFIED_RUN_PARENT` verwenden.

Systempakete für Host und Abhängigkeiten verwenden?
→ Paketweg prüfen, Verfügbarkeit vor Installation abfragen und v3/ABI validieren.

Benötigt der Kernpfad Hostpatch, Modul, Middleware oder Service?
→ Paketgestützten Source-Build verwenden, kein Standardpaket als gleichwertig ausgeben.

## Gemeinsame Voraussetzung

```sh
export VERIFIED_RUN_PARENT="$HOME/modsecurity-connector-work"
```

Der externe Stamm liegt außerhalb des Checkouts, enthält Build-, Cache-,
Runtime-, Log- und Evidence-Dateien und sollte keine Secrets im Namen tragen.
Siehe auch [den Connectorüberblick](overview.de.md), die
[Variablenreferenz](../../reference/variables.de.md) und die
[Test-/Evidence-Grenzen](../../testing-and-evidence.de.md).
"""
    return f"""{MARKER}

# Compiler, source-build, and package paths

**Language:** English | [Deutsch](README.de.md)

## Purpose

Each detailed guide describes a repository-controlled test path, a local source
build, and an honest package path. A build, link, config check, start, or
package-install result alone is not runtime, CRS, security, production, or
full-matrix evidence.

## Shared starting point

Before any connector, [build libmodsecurity v3](libmodsecurity.md). The
beginner sequence exists only there; the connector guides then start with their
own host and connector.

## Decision matrix

{markdown_table(("Connector", "Test path", "Source build", "Package status", "Selected core path"), rows)}

## Decision tree

Only need to test?
→ Use the repository test path.

Developing a build or change?
→ Use the local source build with external `VERIFIED_RUN_PARENT`.

Need system packages for host and dependencies?
→ Check the package path, query availability before installation, and validate v3/ABI.

Does the core path need a host patch, module, middleware, or service?
→ Use a package-assisted source build; do not present a standard package as equivalent.

## Shared prerequisite

```sh
export VERIFIED_RUN_PARENT="$HOME/modsecurity-connector-work"
```

The external parent stays outside the checkout, holds build, cache, runtime,
log, and evidence files, and should not contain secrets in its name. See the
[connector overview](overview.md), [variable reference](../../reference/variables.md),
and [testing/evidence boundary](../../testing-and-evidence.md).
"""


def generated_overview(german: bool) -> str:
    rows = []
    for item in CONNECTORS:
        info = detail(item)
        suffix = ".de" if german else ""
        joiner = " und " if german else " and "
        preparation = f"`{item['prepare']}`"
        if info["extra_prepare"] and info["extra_prepare"] != item["prepare"]:
            preparation += joiner + f"`{info['extra_prepare']}`"
        rows.append((f"[{item['name_de'] if german else item['name']}]({item['slug']}{suffix}.md)", preparation, f"`{item['build']}`", f"`{item['config']}`", f"`{item['full']}`"))
    if german:
        title = "Überblick über die sechs Compilerwege"
        switch = "**Sprache:** [English](overview.md) | Deutsch"
        headings = ("Connector", "Vorbereitung", "Build", "Config-Test", "Ausgewählter Full Lifecycle")
        body = "Die Detailguides enthalten vollständige Befehle, erwartete Dateien, Exit-Code-Grenzen und Paketprüfungen. Vor einem Lauf `make runtime-components-inventory` und `make runtime-components-sources` ausführen; deren vorbereitete Records sind bei aktualisierten Pins maßgeblich."
        comparison = "| Weg | Geeignet für | Systemweite Änderungen | Host aus Source? | Kernpfad möglich? | Evidence möglich? |\n| --- | --- | --- | --- | --- | --- |\n| Repository-Testweg | Entwicklung und CI | Nein | Repository-gesteuert | Ja | Ja, nach Full Lifecycle und Evidence-Check |\n| Lokaler Source-Build | Entwicklung und Integration | Optional | Connectorabhängig dokumentiert | Ja | Ja, nur ausgewählter Run |\n| Paketweg | Schneller lokaler Einstieg | Ja | Meist nein | Connectorabhängig | Nur passendes Profil und Run |"
        limit = "Die Targets erzeugen reproduzierbare Entwicklungs-, Test- und Buildartefakte. Sie sind keine Bewertung als produktionsreifes Paket oder gehärtete Deployment-Anleitung. Ein Paket, Compile oder einzelner Smoke wird nicht zu Produktions-, CRS-, Sicherheits- oder Vollmatrix-Evidence befördert."
    else:
        title = "Overview of the six compiler paths"
        switch = "**Language:** English | [Deutsch](overview.de.md)"
        headings = ("Connector", "Preparation", "Build", "Config check", "Selected full lifecycle")
        body = "Detailed guides contain complete commands, expected files, exit-code boundaries, and package checks. Before a run, execute `make runtime-components-inventory` and `make runtime-components-sources`; their prepared records are authoritative when pins change."
        comparison = "| Path | Suitable for | System-wide changes | Host from source? | Core path possible? | Evidence possible? |\n| --- | --- | --- | --- | --- | --- |\n| Repository test path | Development and CI | No | Repository-controlled | Yes | Yes, after full lifecycle and evidence check |\n| Local source build | Development and integration | Optional | Documented per connector | Yes | Yes, selected run only |\n| Package path | Quick local start | Yes | Usually no | Connector-dependent | Only matching profile and run |"
        limit = "Targets create reproducible development, test, and build artifacts. They are not an assessment of a production package or hardened deployment guidance. A package, compile, or individual smoke is not promoted to production, CRS, security, or full-matrix evidence."
    return f"""{MARKER}

# {title}

{switch}

## Target map

{markdown_table(headings, rows)}

{body}

## Three paths, three different statements

{comparison}

## Shared boundary

{limit}
"""


def write(name: str, content: str) -> None:
    path = OUTPUT / name
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for name, content in rendered_files().items():
        write(name, content)


if __name__ == "__main__":
    main()
