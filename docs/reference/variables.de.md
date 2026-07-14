# Konfigurations- und Runtime-Variablen

**Sprache:** [English](variables.md) | Deutsch

Dies ist die zentrale Referenz für Variablen, die das Root-<code>Makefile</code>,
seine Runtime-Lifecycle-Wrapper und direkt aufrufbare Connector-Harnesses
annehmen. Sie ist bewusst zurückhaltend: Ein deklarierter Source-, Build- oder
Capability-Pfad ist kein Nachweis für einen erfolgreichen Host-Lauf.

## Geltungsbereich und Claim-Grenze

Das Repository besitzt ausgewählte HTTP/1.1-Kern-Lifecycle-Routen für Apache,
NGINX, HAProxy, Envoy, Traefik und lighttpd. Ihr Ergebnis ist immer
laufabhängig und muss aus der kanonischen Evidence des aufgerufenen Targets
gelesen werden.

Diese Referenz erhebt **keinen** Production-, CRS-, HTTP/2-, HTTP/3-,
Extended-Matrix- oder Strict-für-alle-Connectoren-Claim. Insbesondere beweist
eine Variable namens <code>strict</code>, ein Source-Build oder ein
erfolgreicher Konfigurationscheck keinen client-sichtbaren
Post-Commit-Enforcement-Pfad.

Alle folgenden Pfade sind repository-relativ, sofern sie nicht ausdrücklich
als <em>absoluter Runtime-Pfad</em>, <em>Cache-Pfad</em>,
<em>Evidence-Pfad</em> oder <em>Host-Installationspfad</em> bezeichnet sind.
Verwenden Sie für Build-, Cache-, Runtime-, Log- und Evidence-Ausgaben
beschreibbare Pfade außerhalb des Checkouts.

## Variablen setzen

Setzen Sie eine Make-Variable für einen Aufruf oder exportieren Sie sie für
eine Shell-Sitzung. Das erste Beispiel erstellt einen flüchtigen
Runtime-Elternpfad; das zweite identifiziert einen kanonischen Evidence-Lauf.

~~~sh
make quick-check VERIFIED_RUN_PARENT="/srv/modsecurity-work"
NO_CRS_RUN_ID="six-core-20260712T120000Z" make full-lifecycle-all-connectors
~~~

<code>/srv/modsecurity-work</code> ist ein absoluter, beschreibbarer
Runtime-Pfad außerhalb des Repositorys. <code>six-core-20260712T120000Z</code>
ist eine dateisystemsichere Laufkennung. Verwenden Sie weder <code>.</code>,
den Repository-Root, einen Home-Verzeichnispfad, den sich nicht zusammengehörige
Jobs teilen, noch Secrets, Benutzernamen oder Tickettext in einem dieser Werte.

<code>VAR=value make target</code> ist eine Make-Zuweisung. <code>export
VAR=value</code> stellt den Wert Kindskripten als Umgebungsvariable bereit.
Root-Defaults verwenden <code>?=</code>; ein Kommandozeilenwert überschreibt
deshalb einen Repository-Default. Variablen mit „Framework-weitergereicht“
werden vom Root-Makefile exportiert, erhalten ihren detaillierten
provider-spezifischen Default aber im Framework oder Komponenten-Preparer.

## Gemeinsame Pfad-Platzhalter

Die folgenden Winkelklammerformen sind Dokumentationsplatzhalter. Kopieren Sie
die Klammern nicht in ein Kommando, sofern ein Kommando nicht ausdrücklich
literale Klammern erwartet.

| Platzhalter | Zweck | Format / Pflicht | Default / gesetzt durch | Portables Beispiel | Auswirkung und Sicherheit |
|---|---|---|---|---|---|
| <code>&lt;repository-root&gt;</code> | Der Root dieses Connector-Checkouts mit <code>Makefile</code> und <code>docs/</code> | Vorhandenes absolutes Verzeichnis; erforderlich, wenn ein Kommando nach einem Repository-Root fragt | Kein Umgebungsvariablen-Default; wird durch Aufrufer, <code>git rev-parse --show-toplevel</code> oder Target ermittelt | <code>/srv/src/ModSecurity-conector</code> | Löst repository-relative Pfade wie <code>connectors/nginx/</code> auf. Das Beispiel ist kein literaler Entwicklerpfad; verwenden Sie keinen Build-, Cache-, Evidence- oder Secret-Ordner als Repository-Root. |
| <code>&lt;external-source-root&gt;</code> | Ein vom Benutzer ausgewählter Source-Checkout außerhalb dieses Repositorys, etwa Framework oder wiederverwendete Upstream-Source | Vorhandenes absolutes vertrauenswürdiges Source-Verzeichnis; optional, sofern das dokumentierte Kommando es nicht verlangt | Kein Repository-Default; Aufrufer/CI setzt ihn über eine Variable wie <code>FRAMEWORK_ROOT</code> oder dokumentierte Source-Pfad-Variable | <code>/srv/src/ModSecurity-test-Framework</code> | Lässt ein Kommando einen externen Checkout verwenden. Es ist kein Build-/Ausgabepfad und verifiziert weder diesen Checkout noch seine Capabilities. Ersetzen Sie keinen gepinnten CI-Input durch eine nicht vertrauenswürdige/veränderliche Source. |

## Anforderungen auf einen Blick

| Anforderung | Erforderlich für | Zulässiger Wert / Beispiel | Warum dies wichtig ist | Prüfung |
|---|---|---|---|---|
| <code>FRAMEWORK_ROOT</code> | Alle Root-Targets, die an das Framework delegieren | Repository-Default: <code>modules/ModSecurity-test-Framework</code> | Findet Submodule-Runner und Schemas | <code>make check-framework</code> |
| <code>BUILD_ROOT</code> | Builds und Runtime-Targets | Absoluter beschreibbarer Pfad; <code>/srv/modsecurity-work/build</code> | Hält generierte Host-Dateien außerhalb des Checkouts | Target beendet sich mit <code>77</code>, wenn ein erforderlicher Pfad unsicher oder nicht vorhanden ist |
| <code>NO_CRS_RUN_ID</code> | Evidence-Checks und einen reproduzierbaren kanonischen Lauf | <code>six-core-20260712T120000Z</code> | Benennt einen zusammengehörigen Evidence-, Plan-, Log- und Summary-Satz | <code>make evidence-check-all-connectors</code> |
| <code>NO_CRS_RULES_FILE</code> | No-CRS-Baseline-Targets | Absolute vorhandene Regeldatei; Default ist die Framework-Baseline | Verhindert, dass ein unbestimmtes oder anderes Ruleset als Baseline ausgegeben wird | Der Runner prüft die Existenz der Datei |
| <code>CONNECTOR_COMPONENT_CACHE</code> | Runtime-Vorbereitung oder Wiederverwendung | Absoluter Cache-Pfad; <code>/srv/modsecurity-work/cache-v2/shared</code> | Hält wiederverwendbare vorbereitete Komponenten getrennt von jedem Lauf | <code>make runtime-components-inventory</code> |
| Toolchain-Variablen | Source-Builds und C-Checks | <code>CC=clang CFLAGS="-O2"</code> | Wählen Compiler und Flags ohne Änderungen an versionierten Dateien | <code>make check-common-helpers</code> |

Keine Variable in dieser Tabelle ist ein Secret. Wenn eine nachgelagerte
Host-Konfiguration ein Zertifikat, einen privaten Schlüssel, Token, Cookie,
Authorization-Header oder Passwort benötigt, bewahren Sie es in einem sicheren
Store auf; committen Sie es nicht, legen Sie es nicht in kanonische Evidence
und übergeben Sie es nicht als Kommandozeilenargument, das in Prozesslisten
sichtbar sein kann.

## Referenztabelle

„Default“ bedeutet den Root-Makefile-Default, sofern die Zelle nicht
„Framework-weitergereicht“ oder „Harness-spezifisch“ enthält. Ein leerer
Default ist keine Aufforderung, sich auf das aktuelle Arbeitsverzeichnis zu
verlassen; der Aufrufer oder ein Target muss den Wert liefern.

| Variable | Bereich | Pflicht | Default | Format | Kurzbeschreibung |
|---|---|---:|---|---|---|
| <code>PYTHON</code> | Toolchain | nein | <code>.venv/bin/python</code>, falls vorhanden, sonst <code>python3</code> | Executable oder Executable-Pfad | Python für Repository-Skripte |
| <code>MSCONNECTOR_C_STD</code>, <code>MSCONNECTOR_CFLAGS</code>, <code>MSCONNECTOR_COMPILER_ID</code> | Compiler | nein | <code>c17</code>; Warnings-as-Errors-Flags; Compiler-Basisname | C-Standard, Flags, Executable-Name | Steuert die Kompilierung der Common-Helper |
| <code>COMPDB_OUTPUT</code> | lokale Diagnostik | für Compilation-Database-, clangd- und advisory Baseline-Targets erforderlich | none | absolute Compilation-Database-Datei außerhalb des Checkouts; die advisory Verwendung benötigt sie zusätzlich unterhalb des markierten <code>CODEX_TEMP_ROOT</code> | Atomar veröffentlichte Bear-Compilation-Database; Erfassungen führen nach Translation-Unit zusammen und überschreiben kein fehlgeschlagenes Target; die Baseline liest sie ohne Änderung |
| <code>CPP_BUILD_ROOT</code>, <code>MODSECURITY_INCLUDE_DIR</code>, <code>MODSECURITY_LIB_DIR</code>, <code>MODSECURITY_LIB_FILE</code> | gezielte C++17-Diagnostik | erforderlich außer optionalem <code>MODSECURITY_LIB_FILE</code> | none | absoluter externer Build-Ordner; absolute lokale Header-/Library-Ordner; optionale absolute Library-Datei | Baut und erfasst nur den libmodsecurity-Evaluator; keine Component-Preparation und keine Evaluator-Ausführung |
| <code>CLANG_TIDY</code>, <code>CLANG</code>, <code>CLANGXX</code> | advisory Clang-Analyse | für das ausgewählte advisory Target erforderlich | <code>clang-tidy</code>, <code>clang</code>, <code>clang++</code> | vertrauenswürdiger Executable-Name oder absoluter Executable-Pfad | Wählt die read-only Tidy- und direkten Static-Analyzer-Tools; fehlende Executables liefern <code>77</code> und es wird kein Ersatz installiert |
| <code>CLANG_TIDY_CHECKS</code>, <code>CLANG_ANALYZER_CHECKS</code> | advisory Clang-Analyse | nein | <code>-*,bugprone-*,cert-*</code>; <code>core,unix,security,cplusplus,deadcode</code> | kommagetrennte vertrauenswürdige Clang-Check-Selektoren | Wählt die expliziten Tidy- und direkten Analyzer-Profile im normalisierten JSON; unsichere Selektor-Syntax liefert <code>2</code> |
| <code>ANALYSIS_OUTPUT</code> | advisory Clang-Analyse | für Baseline-Targets erforderlich | none | absolutes Ausgabeverzeichnis unterhalb des markierten <code>CODEX_TEMP_ROOT</code> und außerhalb des Checkouts | Nimmt nur laufbezogene Rohlogs, eigene SARIF-Dateien und normalisiertes Baseline-JSON auf; der Runner entfernt ein vom Aufrufer geliefertes Verzeichnis nie rekursiv |
| <code>VERIFIED_RUN_PARENT</code> | Runtime-Root | nein | <code>RUNNER_TEMP</code>, dann <code>TMPDIR</code>, dann <code>&lt;system-temporary-root&gt;</code> | absolutes Verzeichnis | Elternpfad des invocation-eigenen Runtime-Baums |
| <code>VERIFIED_RUN_ROOT</code>, <code>VERIFIED_STATE_ROOT</code>, <code>VERIFIED_BUILD_ROOT</code>, <code>VERIFIED_SOURCE_ROOT</code>, <code>VERIFIED_TMP_ROOT</code>, <code>VERIFIED_LOG_ROOT</code> | Runtime-Roots | nein | Unterhalb von <code>VERIFIED_RUN_PARENT</code> abgeleitet | absolute Verzeichnisse | Isolierte State-, Build-, Source-, temporäre und Log-Orte |
| <code>STATE_HOME</code>, <code>SOURCE_ROOT</code>, <code>BUILD_ROOT</code>, <code>TMP_ROOT</code>, <code>LOG_ROOT</code>, <code>MATRIX_ROOT</code>, <code>RESULTS_DIR</code> | Build/Runtime | target-abhängig | Von den Verified-Roots abgeleitet; <code>RESULTS_DIR</code> ist Framework-weitergereicht | absolute Verzeichnisse | Arbeitsbereiche für Builds, Harnesses und Report-Writer |
| <code>CHECK_STATUS_ROOT</code>, <code>APACHE_REQUEST_TRANSACTION_CLEANUP_STATUS_FILE</code> | CI-Steuerungsstatus | nein | <code>$(BUILD_ROOT)/check-status</code>; dessen Child <code>apache-request-transaction-cleanup.json</code> | absolute Verzeichnisse/Datei außerhalb des Checkouts | Hält den payloadfreien CI-Status der direkten Apache-Cleanup-Prüfung fest; erzeugt keine Runtime-Evidence |
| <code>FRAMEWORK_ROOT</code>, <code>CONNECTOR_ROOT</code> | Repository-Pfade | <code>FRAMEWORK_ROOT</code>: ja für delegierte Targets | Submodule-Pfad; aktuelles Repository-Verzeichnis | repository-relatives oder absolutes vorhandenes Verzeichnis | Findet Framework und dieses Repository |
| <code>CACHE_ROOT</code>, <code>VERIFIED_COMPONENT_CACHE</code>, <code>CONNECTOR_COMPONENT_CACHE</code> | Cache | nein | <code>cache-v2</code> unter dem Verified-Root; gemeinsames Kind | absolute Verzeichnisse | Wiederverwendbarer Component-Cache, getrennt von einem Lauf |
| <code>VERIFIED_EVIDENCE_ROOT</code>, <code>EVIDENCE_ROOT</code>, <code>RUNTIME_EVIDENCE_ROOT</code> | Evidence | nein | Unterhalb des Verified-Root abgeleitet | absolute Verzeichnisse | Elternpfade kanonischer No-CRS- und Runtime-Evidence |
| <code>RUNTIME_RUN_ROOT</code>, <code>RUNTIME_LOG_ROOT</code> | Runtime | nein | Unterhalb des Verified-Root abgeleitet | absolute Verzeichnisse | Elternpfade für Roh-Läufe und pro-Lauf-Logs |
| <code>VERIFIED_RUN_ID</code> | Report-Lauf | nein | übergebene ID, generierte UTC/Commit-ID oder ID des vorhandenen Manifests | dateisystemsicheres Token | Identifiziert einen Verified-Report-Lauf |
| <code>NO_CRS_CONNECTORS</code> | No-CRS-Auswahl | nein | <code>apache nginx haproxy envoy traefik lighttpd</code> | durch Leerzeichen getrennte Connector-Namen | Begrenzte Connector-Menge für Aggregate-Targets |
| <code>NO_CRS_RUN_ID</code> | No-CRS-Evidence | ja für Evidence-Checks | keiner; Runner können einen UTC/Commit-Wert ableiten | 1–128 ASCII-Buchstaben/Ziffern plus <code>.</code>, <code>_</code>, <code>-</code>; beginnt alphanumerisch | Kanonischer Evidence-Namespace |
| <code>NO_CRS_RULES_FILE</code> | No-CRS-Regeln | nein | Framework <code>tests/rules/no-crs-baseline.conf</code> | absolute vorhandene Datei | Regeldatei der Baseline |
| <code>NO_CRS_ARTIFACT_PROFILE</code>, <code>FULL_LIFECYCLE_HOST_PROFILE</code>, <code>FULL_LIFECYCLE_EXECUTED_TARGET</code> | Lifecycle-Interna | durch Full-Lifecycle-Targets gesetzt | <code>generic</code>; Profil/Target leer | aufzählbare Strings | Bindet einen Lauf an sein ausgewähltes Host-Profil |
| <code>NO_CRS_PROTOCOL_CLIENT</code>, <code>NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR</code> | optionaler Protocol-Probe | nein | <code>0</code>; leer | Boolean; absoluter Roh-Lauf-Nachkomme | Opt-in für eine nicht-promotende Protocol-Beobachtung |
| <code>CAPABILITY_PLAN_ROOT</code>, <code>CAPABILITY_REPORT_EVIDENCE_ROOT</code>, <code>CAPABILITY_REPORT_RUN_ID</code>, <code>CAPABILITY_REPORT_OUTPUT_DIR</code> | Capability-Reports | nein | von Build/Evidence/Run-ID abgeleitet | absolute Verzeichnisse und Run-ID | Steuert Selected-Case-Pläne und Report-Ausgabe |
| <code>SKIP_RUNTIME_COMPONENT_PREPARE</code>, <code>RUNTIME_COMPONENT_STRICT_VERIFY</code>, <code>KEEP_RUNTIME_ARTIFACTS</code> | Provisionierung | nein | <code>0</code> | <code>0</code> oder <code>1</code> | Überspringt Vorbereitung nur mit nutzbarem Snapshot; wählt Verifikations- und Cleanup-Policy |
| <code>RUNTIME_COMPONENT_TARGET</code>, <code>RUNTIME_COMPONENT_ENV_SNAPSHOT</code>, <code>RUNTIME_REPORT_OUTPUT_ROOT</code> | Provisionierung | nein | <code>all</code>; Target-generierter Snapshot und Report-Root | Target-Name; absolute Datei/Verzeichnis | Component-Auswahl und invocation-lokaler Environment-Snapshot |
| <code>RUNTIME_COMPONENT_NETWORK_RETRIES</code>, <code>RUNTIME_COMPONENT_NETWORK_RETRY_DELAY_SECONDS</code> | Provisionierung | nein | <code>3</code>; <code>2</code> | nicht-negative Zahlen | Begrenzte Wiederholungen für Component-Downloads |
| <code>VERIFIED_RUN_RUNTIME_MATRIX_TIMEOUT_SECONDS</code>, <code>VERIFIED_RUN_FULL_MATRIX_RUNTIME_TIMEOUT_SECONDS</code>, <code>VERIFIED_RUN_REPORT_REFRESH_TIMEOUT_SECONDS</code>, <code>VERIFIED_RUN_NATIVE_MRTS_TIMEOUT_SECONDS</code>, <code>VERIFIED_RUN_FULL_MATRIX_JOB_TIMEOUT_SECONDS</code>, <code>VERIFIED_RUN_JOB_FINALIZE_GRACE_SECONDS</code>, <code>VERIFIED_RUN_FULL_MATRIX_TOTAL_TIMEOUT_SECONDS</code> | Timeouts | nein | <code>1800</code>, <code>7200</code>, <code>1800</code>, <code>1800</code>, <code>3600</code>, <code>60</code>, <code>14400</code> Sekunden | positive ganzzahlige Sekunden | Begrenzt lang laufende Report- und Matrix-Arbeit |
| <code>SMOKE_CASES</code>, <code>CASE_SCOPE</code>, <code>TEST_CASE</code>, <code>RUN_ONE_CASE</code>, <code>FORCE_ALL_CASES</code> | Test-Auswahl | nein | Framework-weitergereicht; <code>CASE_SCOPE=all</code> in nativen Harnesses | Case-ID/Liste; Scope; Boolean | Grenzt einen Diagnose-Lauf ein, ohne den Katalog zu ändern |
| <code>DEFAULT_BRANCH</code>, <code>REFRESH</code>, <code>EXTRA_CASE_ROOTS</code> | Framework-weitergereicht | nein | Framework/Provider-Default | Branch, Boolean, Pfade | Weitergereichte Compatibility- und Refresh-Controls |
| <code>MODSECURITY_TEST_VARIANT</code>, <code>MODSECURITY_MRTS_VARIANT</code>, <code>MODSECURITY_RULESET</code>, <code>MODSECURITY_SMOKE_CASE</code>, <code>CRS_SMOKE_CASE</code>, <code>MODSECURITY_MRTS_INCLUDE_FEATURE_DEMO</code>, <code>MODSECURITY_MRTS_PREPARED</code> | Framework-Test-Eingabe | nein | Framework-weitergereicht | Variant, Ruleset, Case, Boolean | Framework-seitige Test- und MRTS-Auswahl |
| <code>MODSECURITY_REPO_URL</code>, <code>MODSECURITY_GIT_REF</code>, <code>MODSECURITY_V3_GIT_URL</code>, <code>MODSECURITY_V3_GIT_REF</code>, <code>MODSECURITY_APACHE_GIT_URL</code>, <code>MODSECURITY_APACHE_GIT_REF</code>, <code>MODSECURITY_NGINX_GIT_URL</code>, <code>MODSECURITY_NGINX_GIT_REF</code> | Source-Provenance | nein | Framework/Provider-Pin | URL und unveränderliche Ref | Upstream-Source-Ort und Revision |
| <code>MODSECURITY_SOURCE_DIR</code>, <code>MODSECURITY_V3_SOURCE_DIR</code>, <code>MODSECURITY_V3_ROOT</code>, <code>MODSECURITY_APACHE_SOURCE_DIR</code>, <code>MODSECURITY_NGINX_SOURCE_DIR</code> | Source-Pfade | nein | Framework-weitergereicht | absolute vorhandene Verzeichnisse | Wiederverwendung eines lokalen Source-Baums statt Fetch |
| <code>MODSECURITY_APACHE_REPO_URL</code>, <code>MODSECURITY_NGINX_REPO_URL</code>, <code>ALLOW_EXTERNAL_CONNECTOR_REPOS</code> | Source-Provenance | nein | Framework-weitergereicht | URLs; Boolean | Steuert die Nutzung externer Apache-/NGINX-Sources |
| <code>CRS_REPO_URL</code>, <code>CRS_GIT_REF</code>, <code>CRS_SOURCE_DIR</code>, <code>CRS_RUNTIME_DIR</code>, <code>MODSECURITY_RULE_PREAMBLE_FILE</code> | optionale CRS-Eingabe | nein | Framework/Provider-Pin | URL/Ref/Pfad | CRS-Vorbereitungs-Eingabe; kein CRS-Verifikations-Claim |
| <code>BUILD_HTTPD_FROM_SOURCE</code>, <code>BUILD_PCRE2_FROM_SOURCE</code>, <code>BUILD_NGINX_FROM_SOURCE</code>, <code>NGINX_SOURCE_MODE</code>, <code>NGINX_SOURCE_REPO_URL</code>, <code>NGINX_SOURCE_GIT_REF</code>, <code>NGINX_GITHUB_REPO</code>, <code>NGINX_RELEASE_TAG</code> | Host-Provisionierung | nein | Framework-weitergereicht | Boolean, Mode, URL/Ref/Tag | Wählt Host-Source-Erwerb und Build-Policy |
| <code>HTTPD_VERSION</code>, <code>HTTPD_SOURCE_URL</code>, <code>HTTPD_SHA256</code>, <code>HTTPD_SHA256_URL</code>, <code>APR_VERSION</code>, <code>APR_SOURCE_URL</code>, <code>APR_SHA256</code>, <code>APR_SHA256_URL</code>, <code>APR_UTIL_VERSION</code>, <code>APR_UTIL_SOURCE_URL</code>, <code>APR_UTIL_SHA256</code>, <code>APR_UTIL_SHA256_URL</code>, <code>PCRE2_VERSION</code>, <code>PCRE2_SOURCE_URL</code>, <code>PCRE2_SHA256</code>, <code>PCRE2_SHA256_URL</code> | Apache-Provisionierung | nein | Framework/Provider-Pin | Version, URL, SHA-256 | Apache-Dependency-Provenance |
| <code>HAPROXY_VERSION</code>, <code>HAPROXY_SOURCE_URL</code>, <code>HAPROXY_SHA256_URL</code>, <code>HAPROXY_SHA256</code>, <code>HAPROXY_SOURCE_ROOT</code>, <code>HAPROXY_DOWNLOAD_DIR</code>, <code>HAPROXY_SOURCE_DIR</code>, <code>HAPROXY_RUNTIME_BUILD_DIR</code>, <code>HAPROXY_RUNTIME_BUILD_WORKTREE</code>, <code>HAPROXY_RUNTIME_DIR</code>, <code>HAPROXY_BIN</code> | HAProxy-Provisionierung | nein | Framework/Provider-Pin | Version, URL, SHA-256, absolute Pfade | HAProxy-Source-, Build- und Host-Executable-Eingaben |
| <code>EXPAT_SOURCE_URL</code>, <code>EXPAT_GIT_REF</code>, <code>EXPAT_GIT_URL</code>, <code>EXPAT_PROMPT_EXPECTED_LATEST</code> | Apache-Dependency | nein | Framework/Provider-Pin | URL/Ref/Boolean | Expat-Provenance und Prompt-Policy |
| <code>GO_FTW_BIN</code>, <code>GO_FTW_SOURCE_URL</code>, <code>GO_FTW_PROMPT_EXPECTED_LATEST</code>, <code>GO_FTW_GIT_REF</code>, <code>ALBEDO_BIN</code>, <code>ALBEDO_SOURCE_URL</code>, <code>ALBEDO_PROMPT_EXPECTED_LATEST</code>, <code>ALBEDO_GIT_REF</code> | MRTS-Tools | nein | <code>go-ftw</code>, <code>albedo</code>; sonst Provider-Pins | Executable, URL, Ref, Boolean | Optionale Framework-/MRTS-Tool-Eingabe |
| <code>MRTS_ROOT</code>, <code>MRTS_DEFINITIONS</code>, <code>MRTS_RULES_OUT</code>, <code>MRTS_FTW_OUT</code>, <code>MRTS_LOAD_FILE</code>, <code>MRTS_CASE_ROOT</code>, <code>MRTS_BUILD_ROOT</code>, <code>MRTS_NATIVE_ROOT</code> | MRTS | nein | Wo definiert: von Build-Root abgeleitet; sonst Framework-weitergereicht | absolute Dateien/Verzeichnisse | MRTS-Materialisierung und Native-Run-Orte |
| <code>MRTS_NATIVE_TARGETS</code>, <code>MRTS_NATIVE_APACHE_PORT</code>, <code>MRTS_NATIVE_NGINX_BIN</code>, <code>MRTS_NATIVE_NGINX_MODULE_DIR</code>, <code>MRTS_NATIVE_NGINX_PORT</code>, <code>MRTS_NATIVE_BACKEND_PORT</code> | MRTS-native | nein | <code>apache2_ubuntu nginx-pr24</code>; Ports <code>19080</code>–<code>19082</code>, wo definiert | Target-Liste, Executable/Pfad, TCP-Ports | Steuert optionale native MRTS-Läufe |
| <code>APACHE_BIN</code>, <code>APACHECTL_BIN</code>, <code>APXS_BIN</code>, <code>NGINX_BIN</code> | Host-Binaries | nein | Framework-weitergereicht | Executable oder absoluter Executable-Pfad | Überschreibt entdeckte Host-Executables |
| <code>RESPONSE_BODY_PROBE_REPEAT</code>, <code>RESPONSE_BODY_PROBE_ROOT</code>, <code>RESPONSE_BODY_PROBE_CASE</code> | Diagnose-Probe | nein | Framework-weitergereicht | positive Anzahl, absoluter Pfad, Case-ID | Steuert eine fokussierte Response-Body-Diagnose |
| <code>DECISION_BACKEND</code>, <code>ENVOY_DECISION_BACKEND</code>, <code>TRAEFIK_DECISION_BACKEND</code>, <code>LIGHTTPD_DECISION_BACKEND</code> | Compatibility-Pfad | nein | Framework-weitergereicht | Provider-definierter Backend-Name | Wählt ein unterstütztes Decision-Backend; kein Capability-Upgrade |
| <code>CC</code>, <code>CXX</code>, <code>CPPFLAGS</code>, <code>CFLAGS</code>, <code>CXXFLAGS</code>, <code>LDFLAGS</code>, <code>LIBS</code>, <code>PKG_CONFIG_PATH</code>, <code>LD_LIBRARY_PATH</code>, <code>PATH</code> | geerbte Toolchain | nein | Shell-/Toolchain-Default | Compiler-Kommandos, Flags, Pfadlisten | Werden an Source-Builds und dynamische Loader weitergereicht |
| Apache-Harness-Variablen | connector-lokal | nur direkter Aufruf | siehe Abschnitt „Apache: direkt verwendete Entry-Point-Variablen“ | Pfade, Ports, Case-Selektoren | Überschreiben einen direkten Apache-Harness |
| NGINX-Harness-Variablen | connector-lokal | nur direkter Aufruf | siehe Abschnitt „NGINX: direkt verwendete Entry-Point-Variablen“ | Pfade, Ports, Protocols, Case-Selektoren | Überschreiben einen direkten NGINX-Harness |
| HAProxy-Harness-Variablen | connector-lokal | nur direkter Aufruf | siehe Abschnitt „HAProxy: direkt verwendete Entry-Point-Variablen“ | Pfade, Ports, Case-Selektoren | Überschreiben einen direkten HAProxy-Harness |
| Envoy-Harness-Variablen | connector-lokal | nur direkter Aufruf | siehe Abschnitt „Envoy: direkt verwendete Entry-Point-Variablen“ | Pfade, Ports, Booleans | Überschreiben ext_proc-/ext_authz-Helper-Entry-Points |
| Traefik-Harness-Variablen | connector-lokal | nur direkter Aufruf | siehe Abschnitt „Traefik: direkt verwendete Entry-Point-Variablen“ | Pfade, Listen-Adressen, Flags | Überschreiben Native-Middleware- oder Compatibility-Helper |
| lighttpd-Harness-Variablen | connector-lokal | nur direkter Aufruf | siehe Abschnitt „lighttpd: direkt verwendete Entry-Point-Variablen“ | Pfade, Ports, Modi | Überschreiben den gepatchten Host-Helper |

## Detaillierte Root-Variablen

### Runtime- und Repository-Pfade

| Eigenschaft | <code>VERIFIED_RUN_PARENT</code> | <code>BUILD_ROOT</code> | <code>FRAMEWORK_ROOT</code> | <code>CONNECTOR_COMPONENT_CACHE</code> |
|---|---|---|---|---|
| Zweck | Elternpfad eines flüchtigen Invocation-Baums | Build-Ausgabe-Root für die Host-Vorbereitung | Findet Framework-Submodule oder gleichwertigen Checkout | Wiederverwendbarer Cache vorbereiteter Komponenten |
| Format | Absolutes beschreibbares Verzeichnis | Absolutes beschreibbares Verzeichnis außerhalb des Checkouts | Vorhandenes Verzeichnis mit Framework-Makefile und <code>ci/</code> | Absolutes beschreibbares Verzeichnis außerhalb des Checkouts |
| Pflicht | Nein; ein sicherer Default wird abgeleitet | Für Builds erforderlich; Root leitet einen ab | Ja für Targets, die an das Framework delegieren | Nein; Root leitet ein gemeinsames Cache-Kind ab |
| Root-Default | <code>RUNNER_TEMP</code>, dann <code>TMPDIR</code>, dann <code>&lt;system-temporary-root&gt;</code> | <code>VERIFIED_RUN_ROOT/build</code> | <code>modules/ModSecurity-test-Framework</code> | <code>CACHE_ROOT/shared</code> |
| Gesetzt durch | Aufrufer, CI-Runner oder Makefile | Aufrufer oder Makefile | Aufrufer oder Makefile | Aufrufer, Komponenten-Preparer oder Makefile |
| Gültigkeitsbereich | Eine Invocation und ihre Nachkommen | Eine Invocation; connector-lokale Kindpfade werden abgeleitet | Eine Invocation | Wiederverwendbar zwischen kompatiblen Invocations |
| Beispiel | <code>/srv/modsecurity-work</code> | <code>/srv/modsecurity-work/verified/build</code> | <code>modules/ModSecurity-test-Framework</code> | <code>/srv/modsecurity-work/verified/cache-v2/shared</code> |
| Auswirkung | Verschiebt alle abgeleiteten Run-Roots | Bestimmt generierte Host- und Report-Arbeitsorte | Fehlender Pfad lässt <code>check-framework</code> mit <code>77</code> enden | Verwendet Component-Downloads/-Builds bei passender Identität wieder |
| Sicherheit | Nicht auf Checkout, Systemverzeichnisse oder einen Secret-haltigen Home-Baum zeigen | Runner weist unsichere Checkout-Pfade zurück | Muss vertrauenswürdiger Source-Code der erwarteten Revision sein | Als Build-Eingabe behandeln; keine Zugangsdaten speichern |

<code>VERIFIED_RUN_ROOT</code> verwendet standardmäßig
<code>VERIFIED_RUN_PARENT/ModSecurity-conector-verified</code>. Seine Kinder
<code>state</code>, <code>build</code>, <code>src</code>, <code>tmp</code>,
<code>logs</code>, <code>cache-v2</code>, <code>evidence</code>,
<code>runs</code> und <code>run-logs</code> werden über die entsprechenden
<code>VERIFIED_*</code>-, <code>CACHE_ROOT</code>- und
<code>RUNTIME_*</code>-Variablen der Referenztabelle bereitgestellt.
<code>TMP_ROOT</code> und <code>LOG_ROOT</code> liegen standardmäßig unter
<code>BUILD_ROOT</code>; dadurch bleiben temporäre Host-Dateien unter der
Invocation statt in einem versionierten Baum.

<code>&lt;system-temporary-root&gt;</code> ist ein Dokumentationsplatzhalter für
den temporären System-Fallback, den die eingecheckte Runtime wählt, wenn weder
<code>RUNNER_TEMP</code> noch <code>TMPDIR</code> gesetzt ist. Er ist kein
literaler Kommando-Wert und ändert diesen Runtime-Default nicht.

### No-CRS- und Evidence-Variablen

| Eigenschaft | <code>NO_CRS_RUN_ID</code> | <code>NO_CRS_CONNECTORS</code> | <code>NO_CRS_RULES_FILE</code> | <code>EVIDENCE_ROOT</code> |
|---|---|---|---|---|
| Zweck | Benennt einen kanonischen Lauf | Wählt Connectoren für Aggregate-Targets | Wählt Baseline-Regeln | Elternpfad kanonischer No-CRS-Evidence |
| Format | Sicheres Token: Buchstaben/Ziffern, <code>.</code>, <code>_</code>, <code>-</code>; maximal 128 Zeichen | Durch Leerzeichen getrennte Teilmenge von <code>apache nginx haproxy envoy traefik lighttpd</code> | Absolute vorhandene Datei | Absolutes beschreibbares Verzeichnis |
| Pflicht | Ja für Evidence-Checks und reproduzierbare Aggregate-Evidence | Nein | Nein | Nein |
| Root-Default | Leer; Runner kann UTC/Commit-Wert ableiten | Alle sechs Connector-Namen | Framework <code>tests/rules/no-crs-baseline.conf</code> | <code>VERIFIED_EVIDENCE_ROOT/no-crs-evidence</code> |
| Gesetzt durch | Aufrufer, CI oder Runner | Aufrufer oder Makefile | Aufrufer oder Makefile | Aufrufer oder Makefile |
| Gültigkeitsbereich | Ein Lauf, alle zugehörigen Artefakte | Ein Aggregate-Target | Eine Baseline-Invocation | Ein oder mehrere Evidence-Läufe |
| Beispiel | <code>six-core-20260712T120000Z</code> | <code>apache nginx</code> | <code>/srv/rules/no-crs-baseline.conf</code> | <code>/srv/modsecurity-work/evidence/no-crs-evidence</code> |
| Auswirkung | Wählt das von der Validierung verwendete Run-Verzeichnis | Begrenzte Aggregate-Schleifen; erzeugt keine Evidence für ausgelassene Connectoren | Ändert die Regeln und damit die Vergleichbarkeit | Wählt Evidence-Verzeichnisse, die Checks konsumieren |
| Sicherheit | Nie Zugangsdaten, Benutzernamen oder Issue-Text aufnehmen | Keine unbekannten Connector-Namen verwenden | Lokalen Regelinhalt prüfen; Regeln sind ausführbare Policy | Sensible Roh-Logs nicht mit kanonischer Ausgabe mischen |

<code>NO_CRS_PROTOCOL_CLIENT=1</code> schaltet einen stage-eigenen
Protocol-Probe ein. Wenn über <code>NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR</code>
ein Artefaktverzeichnis bereitgestellt wird, muss es unter dem Roh-Evidence-
Verzeichnis dieser Invocation liegen und das Artefaktprofil muss
<code>full_lifecycle</code> sein. Dies ist eine Diagnose-Eingabe: Sie
promotet nicht selbst HTTP/2, HTTP/3, QUIC oder Strict-Transport-Verhalten.

Die Root-Full-Lifecycle-Targets setzen <code>NO_CRS_ARTIFACT_PROFILE</code>,
<code>FULL_LIFECYCLE_HOST_PROFILE</code> und
<code>FULL_LIFECYCLE_EXECUTED_TARGET</code> selbst. Setzen Sie diese Interna
nicht, um einen Compatibility-Smoke als Full-Lifecycle-Evidence umzubenennen.

### Provisionierungs-, Source- und Toolchain-Variablen

Die Source-URL-, Ref-, Checksum-, Version- und Pfadvariablen der
Referenztabelle bilden eine Gruppe. Sie besitzen die folgenden gemeinsamen
Eigenschaften:

| Eigenschaft | Source-/Provenance-Gruppen |
|---|---|
| Zweck | Teilt dem Framework-Komponenten-Preparer mit, welche gepinnte Source, welches Archiv, welcher lokale Baum, welches Host-Binary oder welches optionale MRTS-Tool zu verwenden ist |
| Format | URLs verwenden <code>https://</code> oder ein anderes vom Provider unterstütztes Schema; Refs/Tags sind nicht-leere Source-Identifikatoren; SHA-256-Werte bestehen aus 64 Hex-Zeichen; bei lokaler Wiederverwendung sind Pfade absolute vorhandene Pfade |
| Pflicht | Am Root optional. Ein Target verwendet entweder seinen Provider-Default oder meldet eine fehlende Voraussetzung; Source-Overrides sind für gewöhnliche Root-Targets nicht erforderlich |
| Default | „Framework-weitergereicht“ bedeutet, dass das Root-Makefile den Namen exportiert, aber keinen Root-Wert definiert. Der Framework-/Provider-Pin ist maßgeblich |
| Gesetzt durch | Fortgeschrittener lokaler Aufrufer oder CI-Provisionierungs-Konfiguration |
| Gültigkeitsbereich | Die relevante Component-Preparation-Invocation; Cache-Ausgabe ist an die effektive Eingabeidentität gebunden |
| Beispiel | <code>HAPROXY_VERSION=3.2.21</code>, <code>NGINX_SOURCE_MODE=release</code>, <code>CC=clang</code> |
| Auswirkung | Kann einen Rebuild erzwingen, eine Source-Herkunft ändern oder ein anderes Executable wählen; upgraded niemals einen Capability-State oder ein Evidence-Ergebnis |
| Sicherheit | HTTPS und verifizierte Checksums verwenden. Einen gepinnten Provenance-Wert in kanonischer CI nicht durch eine veränderliche oder nicht vertrauenswürdige Source ersetzen |

<code>CC</code>, <code>CXX</code>, <code>CPPFLAGS</code>, <code>CFLAGS</code>,
<code>CXXFLAGS</code>, <code>LDFLAGS</code>, <code>LIBS</code>,
<code>PKG_CONFIG_PATH</code>, <code>LD_LIBRARY_PATH</code> und
<code>PATH</code> sind geerbte konventionelle Toolchain-Variablen. Sie sind
optional, besitzen keinen Repository-Default und werden normalerweise von der
Shell oder CI gesetzt. Sie beeinflussen Compiler-Erkennung, Includes,
Library-Erkennung und dynamisches Laden. Beschränken Sie ihre Pfadelemente auf
vertrauenswürdige Orte; ein bösartiger Library-Pfad kann das ausgeführte Binary
ändern.

### Testauswahl-, Report- und Timeout-Variablen

<code>SMOKE_CASES</code>, <code>CASE_SCOPE</code>, <code>TEST_CASE</code>,
<code>RUN_ONE_CASE</code> und <code>FORCE_ALL_CASES</code> sind
Diagnose-Selektoren. Sie sind optional und Framework-weitergereicht, sofern ein
nativer Harness keinen Default nennt. Verwenden Sie eine Katalog-Case-ID oder
eine dokumentierte durch Komma/Leerzeichen getrennte Case-Liste; erfinden Sie
keine Case-IDs. Ein eingegrenzter Lauf ersetzt keinen Aggregate-Evidence-Lauf.

<code>VERIFIED_RUN_ID</code> steuert einen Report-Run-Namespace. Falls er
nicht gesetzt ist, verwendet das Root-Makefile eine ID aus dem vorhandenen
generierten Manifest, wenn verfügbar, sonst einen UTC-Zeitstempel plus den
aktuellen Short-Commit. Die ID ist nur als Dateisystem-Token sicher. Die
Timeout-Variablen sind positive ganzzahlige Sekunden, die Aufrufer oder CI
setzen; die Root-Defaults der Referenztabelle sind operative Grenzen, keine
Evidence-Qualitätsschwellen.

<code>SUPPRESS_FULL_RUN_EVIDENCE_SIDE_EFFECTS</code>,
<code>FULL_MATRIX_MANIFEST</code>, <code>VERIFIED_RUN_COMMANDS_FILE</code>,
<code>VERIFIED_RUN_PROFILE</code>, <code>DEBUG_MISMATCH_GENERATOR</code> und
<code>ALLOW_IN_PROGRESS_SYSTEM_PROOF</code> sind Report-Tool-Controls, die
einzelne Python-Tools konsumieren. Sie sind optional, haben keinen
Root-Makefile-Default und sollten nur vom aufrufenden Target oder für eine
Expertendiagnose verwendet werden. Sie können Report-Arbeit unterdrücken oder
umleiten; sie ändern keine Case-Wahrheit.

## Connector: direkt verwendete Entry-Point-Variablen

Die normale Schnittstelle ist ein Root-Make-Target. Die folgenden Namen
existieren für direkte Harness-Aufrufe und werden hier dokumentiert, damit ein
Leser sie nicht aus Shell-Source herleiten muss. Sie sind keine zusätzlichen
Connector-Features.

### Apache: direkt verwendete Entry-Point-Variablen

| Namen | Zweck und Format | Default / gesetzt durch | Auswirkung und Sicherheit |
|---|---|---|---|
| <code>APACHE_BUILD_ROOT</code>, <code>HTTPD_PREFIX</code>, <code>MODSECURITY_V3_DIR</code>, <code>MODSECURITY_LIB_DIR</code>, <code>PCRE2_PREFIX</code>, <code>APACHE_MODULE</code> | Absolute Build-/Module-Pfade | Von <code>connectors/apache/harness/run_apache_smoke.sh</code> unter <code>BUILD_ROOT</code> abgeleitet | Richtet den direkten Harness auf einen vorbereiteten Apache-/libmodsecurity-Build; Pfade müssen außerhalb des Checkouts liegen |
| <code>APACHE_HTTPD</code>, <code>APACHE_HTTPD_BIN</code>, <code>APACHE</code>, <code>APACHE_BIN</code>, <code>APACHECTL_BIN</code>, <code>APXS</code>, <code>APXS_BIN</code> | Executable-Kommando oder absoluter Executable-Pfad | Root-/Provider-Erkennung oder Harness-abgeleiteter Pfad | Überschreibt die Host-Executable-Erkennung; nur vertrauenswürdige Executable-Dateien verwenden |
| <code>PORT</code>, <code>PORT_SEARCH_LIMIT</code>, <code>PORT_RETRY_LIMIT</code> | TCP-Port sowie positive Search-/Retry-Anzahlen | <code>18080</code>, <code>100</code>, <code>1</code> im direkten Harness | Wählt Loopback-Smoke-Ports; keine privilegierten oder belegten Ports verwenden |
| <code>MSCONNECTOR_FULL_LIFECYCLE_SYNC</code>, <code>FULL_LIFECYCLE_EVIDENCE_OUTPUT</code> | Boolean und absolute Evidence-Datei | <code>0</code>; leer | Aktiviert Synchronisation/Evidence-Übergabe für den Lifecycle-Runner; Evidence nicht in den Checkout schreiben |

### NGINX: direkt verwendete Entry-Point-Variablen

| Namen | Zweck und Format | Default / gesetzt durch | Auswirkung und Sicherheit |
|---|---|---|---|
| <code>NGINX_BUILD_DIR</code>, <code>NGINX_PREFIX</code>, <code>NGINX_BINARY</code>, <code>NGINX_MODULE</code>, <code>MODSECURITY_LIB_DIR</code> | Absolute Prepared-Build-, Install-, Binary-, Modul- oder Library-Pfade | Von <code>BUILD_ROOT</code> abgeleitet, sofern nicht gesetzt | Überschreibt NGINX-Build-/Host-Suche; alle Pfade müssen vertrauenswürdig sein |
| <code>NGINX_HARNESS_PARENT</code>, <code>NGINX_HARNESS_WORK_ROOT</code>, <code>RUNTIME_BASE</code>, <code>RUNTIME_ROOT</code>, <code>LOG_DIR</code>, <code>RESULTS_DIR</code> | Absolute Runtime-/Ausgabeverzeichnisse | Root leitet einen Harness-Elternpfad ab; direkter Harness erzeugt ein Work-Kind | Steuert temporäres Runtime-Layout; muss beschreibbar und für Worker-Zugriff außerhalb des Administrator-Home-Verzeichnisses liegen |
| <code>NGINX_WORKER_USER</code>, <code>NGINX_WORKER_GROUP</code>, <code>NGINX_WORKER_PREFLIGHT_FILE</code>, <code>PERMISSIONS_LOG</code> | OS-Account/-Gruppe und absolute Log-Datei | <code>nobody</code>; Gruppe/Log abgeleitet | Steuert Worker-Access-Diagnostik, keine Identity-Eskalation |
| <code>NGINX_PROTOCOL_PROFILE</code>, <code>NGINX_DOWNSTREAM_PROTOCOL</code>, <code>NGINX_UPSTREAM_PROTOCOL</code> | Profil-/Protocol-Labels | Harness-spezifisch; Downstream/Upstream standardmäßig <code>http1</code> | Wählt ein Build-/Run-Profil. Ein Label ist kein HTTP/2- oder HTTP/3-Nachweis |
| <code>PORT</code>, <code>PORT_SEARCH_LIMIT</code>, <code>PORT_RETRY_LIMIT</code>, <code>CURL</code> | TCP-Port, Grenzen, Client-Kommando | <code>18081</code>, <code>100</code>, <code>1</code>, leer | Direkte Smoke-Transport-Controls; Loopback und vertrauenswürdigen Client verwenden |

### HAProxy: direkt verwendete Entry-Point-Variablen

| Namen | Zweck und Format | Default / gesetzt durch | Auswirkung und Sicherheit |
|---|---|---|---|
| <code>HAPROXY_BIN</code>, <code>SPOA_RUNTIME_BIN</code>, <code>MODSECURITY_BINDING_DIR</code> | Absolute Host-Executable-, SPOA-Executable- und Binding-Verzeichnisse | Root-/Provider-abgeleitet unter <code>BUILD_ROOT</code> | Wählt native HTX-/SPOA-Runtime-Eingaben; nicht auf nicht vertrauenswürdige Binaries zeigen |
| <code>HAPROXY_SOURCE_ROOT</code>, <code>HAPROXY_DOWNLOAD_DIR</code>, <code>HAPROXY_SOURCE_DIR</code>, <code>HAPROXY_RUNTIME_BUILD_DIR</code>, <code>HAPROXY_RUNTIME_BUILD_WORKTREE</code>, <code>HAPROXY_RUNTIME_DIR</code> | Absolute Source-/Build-/Runtime-Pfade | Framework-/Provider-abgeleitet | Source- und Host-Layout; Source-Präsenz allein ist kein Runtime-Nachweis |
| <code>HAPROXY_SPOA_PORT_OFFSET</code>, <code>HAPROXY_BACKEND_PORT_OFFSET</code>, <code>PORT</code>, <code>PORT_SEARCH_LIMIT</code>, <code>PORT_RETRY_LIMIT</code> | Port-Offsets und Port-Search-Werte | <code>12000</code>, <code>24000</code>, <code>18082</code>, <code>100</code>, <code>1</code> | Allokiert Loopback-Listener für den direkten Harness |
| <code>HAPROXY_HTX_SOURCE_DIR</code>, <code>HAPROXY_HTX_CANONICAL_RULES_FILE</code>, <code>HAPROXY_HTX_HOST_EVIDENCE_LOG_PATH</code>, <code>HAPROXY_HTX_BUILD_PROVENANCE</code> | Absolute HTX-Source-/Regel-/Evidence-/Provenance-Pfade | Harness-abgeleitet oder Framework-Baseline | Fortgeschrittene HTX-Overlay-Eingabe; kanonische Regeln und sanitisierte Evidence erhalten |

### Envoy: direkt verwendete Entry-Point-Variablen

| Namen | Zweck und Format | Default / gesetzt durch | Auswirkung und Sicherheit |
|---|---|---|---|
| <code>ENVOY_BIN</code>, <code>EXT_PROC_BIN</code>, <code>SERVICE_BIN</code> | Absolute Envoy-, ext_proc- oder Compatibility-Service-Executables | Prepared-Build-abgeleitet | Wählt vertrauenswürdige Host-/Service-Binaries |
| <code>ENVOY_CONFIG</code>, <code>ENVOY_CONFIG_ROOT</code>, <code>EXT_PROC_CONFIG</code>, <code>EXT_PROC_RUNTIME_CONFIG</code>, <code>OUTPUT_CONFIG</code>, <code>TEMPLATE</code>, <code>VERSION_LOCK</code> | Absolute Konfigurations-/Template-Pfade | Harness-abgeleitet | Erzeugt oder konsumiert Runtime-Konfiguration außerhalb des Checkouts |
| <code>LISTEN_ADDRESS</code>, <code>LISTEN_PORT</code>, <code>UPSTREAM_PORT</code>, <code>EXT_PROC_PORT</code>, <code>ADMIN_PORT</code> | Loopback-Adresse und TCP-Ports | <code>127.0.0.1</code>; <code>18080</code>, <code>18081</code>, <code>18083</code>, <code>19001</code>, wo definiert | Steuert generierte Host-Topologie; Ports müssen 1–65535 sein |
| <code>EVENT_LOG_PATH</code>, <code>COMMON_EVENT_LOG_PATH</code>, <code>COMPLETION_LOG_PATH</code>, <code>FULL_LIFECYCLE_EVIDENCE_OUTPUT</code> | Absolute Event-/Evidence-Dateien | Von Runtime-Root abgeleitet oder leer | Schreibt Roh-/sanitisierte Evidence-Eingaben; niemals Body-Payloads oder Secrets ablegen |
| <code>ENVOY_TRANSPORT_CANCEL_PROBE</code>, <code>ENVOY_PHASE4_BARRIER_TIMEOUT_SECONDS</code> | Boolean und positive Timeout-Sekunden | <code>0</code>, <code>10</code> | Opt-in-Diagnose-Transport-Probe und Barrier-Wait; nicht-promotend |

### Traefik: direkt verwendete Entry-Point-Variablen

| Namen | Zweck und Format | Default / gesetzt durch | Auswirkung und Sicherheit |
|---|---|---|---|
| <code>TRAEFIK_BIN</code>, <code>TRAEFIK_CONNECTOR_BIN</code>, <code>TRAEFIK_ENGINE_SERVICE_BIN</code> | Absolute Executable-Pfade | Prepared-Cache-/Build-Pfad | Wählt vertrauenswürdiges Traefik-, Connector- oder Engine-Service-Binary |
| <code>TRAEFIK_NATIVE_RUNTIME_ROOT</code>, <code>TRAEFIK_RESULT_ROOT</code>, <code>TRAEFIK_LOG_ROOT</code>, <code>TRAEFIK_CONNECTOR_START_ROOT</code>, <code>TRAEFIK_ENGINE_SERVICE_BUILD_DIR</code> | Absolute Runtime-/Build-/Ausgabe-Pfade | Von Build-Root abgeleitet | Steuert direkte Host-Ausgabe; muss absolut, beschreibbar und außerhalb des Checkouts sein |
| <code>TRAEFIK_CONNECTOR_CONFIG</code>, <code>TRAEFIK_CONNECTOR_TRAEFIK_CONFIG</code>, <code>TRAEFIK_CONFIG_ROOT</code> | Konfigurationsdatei-/Template-/Root-Pfade | Connector-Konfigurations-Defaults oder Runtime-Root-abgeleitet | Wählt erzeugte File-Provider-/Connector-Konfiguration |
| <code>TRAEFIK_CONNECTOR_LISTEN</code>, <code>TRAEFIK_START_LISTEN</code>, <code>TRAEFIK_START_UPSTREAM</code> | Loopback-Host:Port-Werte | <code>127.0.0.1:19090</code>, <code>127.0.0.1:19080</code>, <code>127.0.0.1:19091</code> | Direkte Start-Smoke-Topologie; nur Loopback-Adressen werden akzeptiert |
| <code>TRAEFIK_ENGINE_SERVICE_CFLAGS</code>, <code>TRAEFIK_ENGINE_SERVICE_LDFLAGS</code>, <code>MSCONNECTOR_RULES_FILE</code> | Compiler-/Linker-Flags und absolute Regeldatei | Leer; Framework-Baseline, wenn ein Runner sie liefert | Fortgeschrittene direkte Build-/Regel-Eingabe; Shell-Quoting und vertrauenswürdige Pfade erhalten |

### lighttpd: direkt verwendete Entry-Point-Variablen

| Namen | Zweck und Format | Default / gesetzt durch | Auswirkung und Sicherheit |
|---|---|---|---|
| <code>LIGHTTPD_BIN</code>, <code>LIGHTTPD_SOURCE_DIR</code>, <code>LIGHTTPD_BUILD_ROOT</code>, <code>LIGHTTPD_BUILD_DIR</code>, <code>LIGHTTPD_CONFIG_DIR</code>, <code>LIGHTTPD_INCLUDE_DIR</code> | Absolute Host-Binary-/Source-/Build-/Config-/Include-Pfade | Prepared-Build-abgeleitet | Wählt gepatchte Native-Host-Eingaben; Pfad nicht als Evidence interpretieren |
| <code>LIGHTTPD_CONNECTOR_BUILD_ROOT</code>, <code>LIGHTTPD_CONNECTOR_MODULE</code>, <code>LIGHTTPD_MODULE_DIR</code>, <code>LIGHTTPD_SMOKE_PREPARER</code> | Absolute Modul-/Build-/Preparer-Pfade | Von Build-Root abgeleitet | Wählt Connector-Modul und direkte Smoke-Vorbereitung |
| <code>LIGHTTPD_PATCHED_ROOT</code>, <code>LIGHTTPD_PATCHED_SOURCE_DIR</code>, <code>LIGHTTPD_PATCHED_SMOKE_DIR</code>, <code>LIGHTTPD_SMOKE_DIR</code> | Absolute Patch-Host-/Smoke-Verzeichnisse | Von Build-Root abgeleitet | Enthält gepatchten Host-Build und flüchtige Smoke-Ausgabe |
| <code>LIGHTTPD_SMOKE_PORT</code>, <code>LIGHTTPD_PROXY_BARRIER_PORT</code>, <code>LIGHTTPD_PROXY_FIXTURE_PORT</code> | TCP-Ports | <code>18084</code>; Barrier/Fixture dynamisch zugewiesen | Direkte Loopback-Fixture-Topologie |
| <code>LIGHTTPD_REQUEST_BODY_MODE</code>, <code>LIGHTTPD_RESPONSE_BODY_MODE</code>, <code>LIGHTTPD_RESPONSE_HEADER_MARKER</code>, <code>LIGHTTPD_PATCHED_REQUEST_BODY_MODE</code>, <code>LIGHTTPD_PATCHED_RESPONSE_BODY_MODE</code>, <code>LIGHTTPD_PATCHED_RESPONSE_HEADER_MARKER</code>, <code>LIGHTTPD_PATCHED_ENTITY_ENCODING</code> | Mode-/Marker-/Encoding-Werte | <code>none</code> für ungepatchte direkte Vorbereitung; Lifecycle-Runner liefert Streaming-Modi | Direkte Diagnose-Konfiguration; Mode-Auswahl ist kein Strict- oder Protocol-Claim |
| <code>MSCONNECTOR_RULES_FILE</code>, <code>RULES_FILE</code>, <code>FULL_LIFECYCLE_EVIDENCE_OUTPUT</code>, <code>LD_LIBRARY_PATH</code> | Regeln, Evidence, Dynamic-Library-Pfade | Framework-Baseline/abgeleitete Pfade | Steuert Eingabe und Runtime-Loading; niemals Secrets in Dateien oder nicht vertrauenswürdige Verzeichnisse legen |

## Targets, Statuswerte, IDs und Integrationsmodi

### Referenz der primären Targets

| Target | Zweck | Voraussetzungen / wichtige Eingaben | Ausgabe | Exit-Code-Bedeutung und Grenze |
|---|---|---|---|---|
| <code>make check-framework</code> | Bestätigt, dass das Framework-Verzeichnis existiert | <code>FRAMEWORK_ROOT</code> | Nur Konsolendiagnostik | <code>0</code> bedeutet: Verzeichnis existiert; <code>77</code> bedeutet: Voraussetzung fehlt |
| <code>make prepare-runtime-components</code> | Bereitet gepinnte wiederverwendbare Runtime-Komponenten vor | Sicherer <code>BUILD_ROOT</code>, Cache, Framework | Cache und invocation-lokaler Environment-Snapshot | Führt nicht alle Connector-Lifecycles aus |
| <code>make quick-check</code> | Führt lint-orientierte Source-, Contract-, Dokumentations- und Diff-Checks aus | Python, Framework, Toolchain | Nur Diagnostik | Erzeugt keine All-Host-Runtime-Evidence |
| <code>make build-<connector></code> | Führt eine Connector-Build-Stage aus | <code>&lt;connector&gt;</code> ist Apache, NGINX, HAProxy, Envoy, Traefik oder lighttpd | Connector-lokale Build-Ausgabe | Build-Erfolg ist kein Runtime- oder Evidence-Claim |
| <code>make check-config-<connector></code> | Prüft das Laden der ausgewählten Konfiguration | Vorbereiteter Host und Connector | Config-Load-Diagnostik | Sendet keinen Runtime-Traffic |
| <code>make runtime-smoke-<connector></code> | Führt einen fokussierten minimalen Runtime-Smoke aus, wo das Target existiert | Vorbereiteter Host, sichere Runtime-Pfade | Runtime-Smoke-Artefakte | Compatibility-Smoke ist keine Full-Lifecycle-Evidence |
| <code>make no-crs-baseline-<connector></code> | Führt capability-ausgewählte No-CRS-Cases aus | Regeldatei, sichere Pfade | Kanonische Candidate-Evidence für einen Connector | Ergebnisstatus bleibt evidence- und capability-abhängig |
| <code>make full-lifecycle-<connector></code> | Führt die ausgewählte Full-Lifecycle-Route eines Connectors aus | Generierte Profil-/Target-Identität plus normale No-CRS-Eingaben | Full-Lifecycle-Candidate-Artefakte | Nur passende Target-/Profil-Identität darf validiert werden |
| <code>make full-lifecycle-all-connectors</code> | Führt die sechs ausgewählten Routen aus | Alle Komponenten-Voraussetzungen, <code>NO_CRS_RUN_ID</code> empfohlen | Ein Candidate-Run pro ausgewähltem Connector | Erhebt keine Production-, CRS-, HTTP/2-, HTTP/3- oder Strict-für-alle-Claims |
| <code>make evidence-check-all-connectors</code> | Validiert kanonische Evidence eines Laufs | <code>NO_CRS_RUN_ID</code> oder connector-spezifische letzte ID, <code>EVIDENCE_ROOT</code> | Validierungsdiagnostik | Führt Hosts nicht erneut aus und verwandelt fehlende Evidence nicht in PASS |
| <code>make check-six-connector-core-completion</code> | Read-only kompakter Acceptance-Check | <code>NO_CRS_RUN_ID</code> und finalisierte Evidence | Aggregate-Diagnostik | <code>0</code> bedeutet, dass die Bedingungen dieses Checkers bestanden; nicht, dass jeder Katalog-Case oder jedes Protocol bestanden hat |

<code>&lt;connector&gt;</code> in der Target-Tabelle ist ein Platzhalter, keine
literale Syntax. Erlaubte Werte sind <code>apache</code>, <code>nginx</code>,
<code>haproxy</code>, <code>envoy</code>, <code>traefik</code> und
<code>lighttpd</code>. Verwenden Sie zum Beispiel
<code>make build-nginx</code>, nicht <code>make build-&lt;connector&gt;</code>.

### Status- und Prozess-Exit-Codes

| Wert | Bedeutung |
|---|---|
| <code>PASS</code> | Der konkrete Case/Check erfüllte seine erklärten Bedingungen mit der aufgezeichneten Evidence. Dies verallgemeinert nicht auf andere Profile, Protocols oder Cases. |
| <code>FAIL</code> | Der Case/Check lief oder wurde ausgewertet und erfüllte eine erforderliche Bedingung nicht. |
| <code>BLOCKED</code> | Eine Voraussetzung wie Tool, Source, sicherer Pfad oder Host-Komponente fehlte. Dies ist kein verstecktes PASS. |
| <code>NOT EXECUTED</code> | Der Case/Pfad wurde bewusst nicht ausgeführt; daraus folgt keine Runtime-Aussage. |
| <code>NOT APPLICABLE</code> | Der Case trifft auf das ausgewählte Profil oder Host-Modell nicht zu. |
| <code>UNSUPPORTED</code> | Das ausgewählte Host-Modell kann die erforderliche Capability nicht bereitstellen. |
| <code>NOT_EXECUTABLE</code> | Historische Harness-Schreibweise für einen Case, der in dieser Umgebung nicht ausführbar ist. |
| <code>0</code> | Der aufgerufene Prozess erfüllte seinen eigenen technischen Vertrag. Dies garantiert nicht, dass alle Katalog-Cases PASS sind. |
| <code>1</code> | Allgemeiner Runtime-, Konfigurations- oder Validierungsfehler, wenn kein spezifischerer Code verwendet wird. |
| <code>2</code> | Ungültige Invocation, Validierungs-, Contract- oder Aggregate-Input-Fehler. |
| <code>77</code> | Fehlende optionale/Voraussetzungs-Umgebung wie Framework-Checkout oder erforderliche Host-Eingabe; niemals als Build-PASS interpretieren. |

### Rule-IDs und repräsentative Case-IDs

Diese Rule-IDs gehören zur repository-eigenen No-CRS-Baseline in
<code>modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf</code>.
Sie sind keine OWASP-CRS-Rule-IDs.

| Rule-ID | Phase | Zweck der Baseline |
|---:|---:|---|
| <code>1100001</code> | P1 | Verweigert den Request-Header-Marker mit HTTP 403 |
| <code>1100002</code> | P1 | Verweigert einen Request-Header-Marker mit HTTP 429 |
| <code>1100003</code> | P1 | Zeichnet Transaction-ID-Metadaten auf |
| <code>1100101</code> | P2 | Verweigert den Request-Body-Marker |
| <code>1100201</code> | P3 | Verweigert den Response-Header-Marker |
| <code>1100202</code> | P3 | Redirect-Response-Header-Probe |
| <code>1100301</code> | P4 | Beobachtet den Response-Body-Marker und modelliert Late Intervention |
| <code>1100401</code> | P1 | Redirect-Request-Header-Marker |
| <code>1100402</code> | P1 | Log-only-Request-Header-Marker |
| <code>1100403</code> | P1 | Drop/Abort-Request-Header-Marker, wo ein Host-Modell dies unterstützt |

| Case-ID | Capability / erwartete Beobachtung | Evidence-Grenze |
|---|---|---|
| <code>allow_without_marker</code> | P1-Allow-Pfad | Erfordert einen Live-Selected-Host-Pfad; ein 200 allein ist kein All-Phase-Claim |
| <code>deny_header_marker_403</code> | P1-Deny, Rule <code>1100001</code> | Erfordert die aufgezeichneten Rule-/Status-Event-Felder, wo anwendbar |
| <code>deny_request_body_marker_403</code> | P2-Buffered-Body-Deny, Rule <code>1100101</code> | Wird nur ausgewählt, wenn Capabilities dies erlauben |
| <code>deny_response_header_marker_403</code> | P3-Response-Header-Verhalten, Rule <code>1100201</code> | Kann für ein Host-Modell ohne Response-Sicht UNSUPPORTED sein |
| <code>phase4_rule_observed</code> | P4-Rule-Beobachtung, Rule <code>1100301</code> | Impliziert keinen sichtbaren Pre-Commit-403 |
| <code>phase4_deny_after_commit_log_only</code> | Safe-Late-Intervention-Verhalten | Erfordert Metadaten zu angeforderter/tatsächlicher Aktion und Commit |
| <code>phase4_deny_after_commit_abort</code> | Strict-Late-Abort-Verhalten | Bleibt getrennt und gilt nur, wenn der Host es nachweisen kann |
| <code>phase4_first_byte_before_response_end</code> | Erstes Byte erreicht Client vor Upstream-EOS | Erfordert synchronisierte First-Byte-Evidence |
| <code>phase4_no_full_response_buffering</code> | Kein connector-eigener vollständiger Response-Buffer | Erfordert Source-/Runtime-Evidence; wird nicht aus einem Config-Wert abgeleitet |

### Ausgewählte Integrationsmodi

| Connector | Full-Lifecycle-Profilwert | Aufgezeichneter Integrationsmodus | Host-Rolle und Grenze |
|---|---|---|---|
| Apache | <code>native-httpd-module</code> | <code>native-httpd-module</code> | Natives Apache-HTTP-Modul; P1–P4 sind laufabhängig und Response-Body-Auswertung kann bei EOS enden |
| NGINX | <code>native-nginx-http-module</code> | <code>native-nginx-http-module</code> | Natives NGINX-HTTP-Modul; P1–P4 sind laufabhängig und müssen nachgewiesen werden |
| HAProxy | <code>native-htx-filter</code> | <code>native-htx-filter</code> | Nativer HTX-Filter; Body-Slices werden inkrementell weitergereicht und P4 endet bei HTX-EOS |
| Envoy | <code>ext_proc</code> | <code>ext_proc</code> | Streamed External-Processing-Bridge; Strict-Post-Commit-Reset bleibt getrennt/nicht ausgeführt, bis er nachgewiesen ist |
| Traefik | <code>native-middleware</code> | <code>native-traefik-middleware</code> | Native Middleware mit lokalem UDS-Common-/libmodsecurity-Service; Strict-Reset bleibt getrennt/nicht ausgeführt, bis er nachgewiesen ist |
| lighttpd | <code>patched-native</code> | <code>patched-native-lighttpd</code> | Gepatchter nativer lighttpd-Host/Modul; Entity-Body-Ranges werden vor Transfer-Framing verarbeitet und P4 endet bei Entity-EOS |

<code>ext_authz</code>, <code>forwardAuth</code> und
<code>spoe-spop-agent</code> können in Connector-Material als Compatibility-
oder alternative Integrationsbegriffe erscheinen. Sie dürfen nicht
stillschweigend als ausgewählte Full-Lifecycle-Route umbenannt werden. Kurze
Definitionen stehen im [Glossar](../reference/glossary.de.md); die
[Connector-Dokumentation](../connectors/README.de.md) dient als Navigation.

## Weiterführende Dokumentation

- Die [Build-Dokumentation](../build/README.de.md) erläutert Target-Familien
  und sichere Build-Pfade.
- Die [Testing-Dokumentation](../testing-and-evidence.de.md) erläutert Status,
  Auswahl und Validierungsgrenzen.
- Die [Evidence-Dokumentation](../testing-and-evidence.de.md) erläutert Artefakte
  und Promotion-Grenzen.
- Die [Nachvollziehbarkeitsrichtlinie](../change-traceability.de.md) definiert
  die erforderliche zweisprachige Erklärung für zukünftige Variablen und
  Platzhalter.
- `AGENTS.md` ist eine optionale lokale Anweisungsdatei für Codex und gehört
  nicht zur versionierten Projektdokumentation. Für sie gibt es keine deutsche
  Begleitdatei.
