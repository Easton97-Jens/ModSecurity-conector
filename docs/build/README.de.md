# Build-Dokumentation

**Sprache:** [English](README.md) | Deutsch

Dieser Bereich erläutert, wie Root- und Connector-Make-Targets ausgewählte
Connector-Routen vorbereiten und bauen. Ein Build-, Link- oder Config-Load-
Ergebnis ist keine Runtime-Evidence und erhebt keinen Production-, CRS-,
HTTP/2-, HTTP/3-, vollständige-Matrix- oder Strict-für-alle-Connectoren-Claim.

## Build-Eingaben und sichere Pfade

Das Root-Makefile leitet seinen Arbeitsbaum unter
<code>VERIFIED_RUN_ROOT</code> ab. Setzen Sie für einen reproduzierbaren
lokalen Build <code>BUILD_ROOT</code> auf ein absolutes, beschreibbares
Verzeichnis außerhalb des Checkouts:

~~~sh
make build-nginx BUILD_ROOT="/srv/modsecurity-work/build"
~~~

<code>BUILD_ROOT</code> ist optional, weil das Makefile
<code>VERIFIED_RUN_ROOT/build</code> ableitet, wenn kein Wert bereitgestellt
wird. Der Beispielwert <code>/srv/modsecurity-work/build</code> ist ein
absoluter Runtime-Pfad, kein Repository-Default. Verwenden Sie weder
Repository-Root noch Systemverzeichnis oder einen Pfad mit Secrets. Details zu
Format, Scope, Auswirkung und Sicherheit stehen unter
[Konfigurationsvariablen](../reference/variables.de.md#runtime-und-repository-pfade).

Der Platzhalter <code>&lt;connector&gt;</code> bedeutet genau einen von
<code>apache</code>, <code>nginx</code>, <code>haproxy</code>,
<code>envoy</code>, <code>traefik</code> oder <code>lighttpd</code>.
Verwenden Sie zum Beispiel <code>make build-nginx</code>; schreiben Sie nicht
literally <code>make build-&lt;connector&gt;</code>.

## Target-Familien

| Target | Zweck | Voraussetzungen / wichtige Variablen | Erzeugte Ausgabe | Grenze |
|---|---|---|---|---|
| <code>make check-framework</code> | Prüft, dass das Framework verfügbar ist | <code>FRAMEWORK_ROOT</code> zeigt auf einen vorhandenen Framework-Checkout | Konsolenergebnis | Baut keinen Connector |
| <code>make setup-dev</code> | Installiert oder bereitet Entwicklungs-Python-Dependencies über das Framework vor | <code>PYTHON</code>, <code>FRAMEWORK_ROOT</code> | Änderungen der Entwicklungsumgebung außerhalb versionierter Sources | Bereitet nicht jede Host-Komponente vor |
| <code>make prepare-runtime-components</code> | Holt/baut wiederverwendbare gepinnte Host-Komponenten | Sichere Build-/Cache-Pfade, optionale Source-Pin-Variablen | Component-Cache und Environment-Snapshot | Führt keinen Connector-Lifecycle-Traffic aus |
| <code>make build-<connector></code> | Führt die ausgewählte Connector-Build-Stage aus | Framework, Build-Root, target-spezifische Host-Eingaben | Connector-spezifische Build-Ausgabe | Erfolgreicher Build ist kein Config- oder Runtime-Nachweis |
| <code>make build-all-connectors</code> | Führt die Build-Stage für alle sechs Connector-Namen aus | Alle relevanten Host-/Component-Voraussetzungen | Per-Connector-Build-Ausgabe | Aggregate-Build erzeugt keine Full-Lifecycle-Evidence |
| <code>make check-config-<connector></code> | Lädt/prüft die ausgewählte Connector-Konfiguration | Vorbereiteter ausgewählter Build und Konfiguration | Config-Load-Diagnostik | Sendet keinen Traffic |
| <code>make prepare-open-connector-runtimes</code> | Bereitet ausgewählte Envoy-, Traefik- und lighttpd-Host-Eingaben vor | Framework- und Cache-/Provisionierungs-Voraussetzungen | Component-Preparation-Ausgabe | Vorbereitung ist keine Capability-Promotion |
| <code>make lint</code> | Führt Source-, Contract- und dokumentationsorientierte Checks aus | Python, Shell-Tools, Framework, C-Toolchain, wo vorhanden | Diagnostik | Kein All-Host-Runtime-Test |

Prozess-Exit-Code <code>0</code> bedeutet nur, dass das aufgerufene Target
seinen technischen Vertrag erfüllte. <code>1</code> ist ein allgemeiner
Fehler, <code>2</code> ungültige Eingabe/Contract-Validierung und
<code>77</code> eine fehlende optionale oder erforderliche
Umgebungsvoraussetzung. Das Statusvokabular steht unter
[Testing](../testing-and-evidence.de.md).

## Compiler- und Linker-Variablen

Verwenden Sie Standard-Compiler-Umgebungsvariablen nur, wenn die lokale
Toolchain sie erfordert. Die Root-Defaults sind:

| Variable | Pflicht | Root-Default | Beispiel | Auswirkung / Sicherheit |
|---|---:|---|---|---|
| <code>PYTHON</code> | nein | <code>.venv/bin/python</code>, falls vorhanden, sonst <code>python3</code> | <code>PYTHON=python3</code> | Wählt Python-Interpreter für Skripte; vertrauenswürdiges Executable verwenden |
| <code>MSCONNECTOR_C_STD</code> | nein | <code>c17</code> | <code>MSCONNECTOR_C_STD=c23</code> | Wählt Common-Helper-C-Profil; nicht unterstützte optionale Profile können übersprungen werden |
| <code>MSCONNECTOR_CFLAGS</code> | nein | <code>-std=$(MSCONNECTOR_C_STD) -Wall -Wextra -Werror</code> | <code>MSCONNECTOR_CFLAGS="-std=c17 -Wall -Wextra -Werror"</code> | Flags für Common-Helper-Checks; Quoting erhalten |
| <code>CC</code>, <code>CXX</code> | nein | Shell-/Toolchain-Default | <code>CC=clang</code> | Wählen vertrauenswürdige C/C++-Compiler |
| <code>CPPFLAGS</code>, <code>CFLAGS</code>, <code>CXXFLAGS</code>, <code>LDFLAGS</code>, <code>LIBS</code> | nein | kein Root-Default | <code>CFLAGS="-O2"</code> | Fügt Compile-/Link-Eingaben hinzu; nicht vertrauenswürdige Flags können den Build ändern |
| <code>PKG_CONFIG_PATH</code>, <code>LD_LIBRARY_PATH</code>, <code>PATH</code> | nein | Shell-Default | <code>PKG_CONFIG_PATH="/srv/prefix/lib/pkgconfig"</code> | Ändert Tool-/Library-Discovery; auf vertrauenswürdige Pfade beschränken |

Die Schreibweise <code>$(MSCONNECTOR_C_STD)</code> oben ist eine
Make-Variablenreferenz, kein Shell-Kommando. Das Makefile löst sie vor dem
Ausführen eines Rezepts auf. Vollständige Formate, Defaults und
Framework-weitergereichte Source-Variablen stehen unter
[Konfigurationsvariablen](../reference/variables.de.md).

## Cache- und Source-Provisionierung

<code>CACHE_ROOT</code> verwendet standardmäßig
<code>VERIFIED_RUN_ROOT/cache-v2</code> und
<code>CONNECTOR_COMPONENT_CACHE</code> dessen Kind <code>shared</code>.
Beide sind nach dem Ableiten absolute Cache-Pfade. Der Cache ist
wiederverwendbare Eingabe, keine kanonische Evidence.

Wählen Sie vor der Vorbereitung einen isolierten Elternpfad:

~~~sh
make prepare-runtime-components VERIFIED_RUN_PARENT="/srv/modsecurity-work"
~~~

<code>VERIFIED_RUN_PARENT</code> ist optional; der Root wählt
<code>RUNNER_TEMP</code>, dann <code>TMPDIR</code>, dann den dokumentierten
Fallback <code>&lt;system-temporary-root&gt;</code>, wenn die Variable leer
ist. <code>&lt;system-temporary-root&gt;</code> bezeichnet den temporären
System-Fallback der Runtime; es ist ein Dokumentationsplatzhalter und ändert
keinen eingecheckten Runtime-Default. Das Beispiel ist ein empfohlener lokaler
Wert, kein Repository-Default. Setzen Sie
<code>SKIP_RUNTIME_COMPONENT_PREPARE=1</code> nur, wenn bereits ein gültiger
invocation-lokaler Snapshot und kompatibler Cache existieren. Dies bedeutet
nicht „fehlende Dependencies überspringen“.

Fortgeschrittene Source-/Provenance-Werte wie <code>HAPROXY_SOURCE_URL</code>,
<code>HTTPD_SHA256</code>, <code>NGINX_SOURCE_GIT_REF</code> und
<code>MODSECURITY_V3_GIT_REF</code> sind Framework-weitergereicht. URLs,
Revisionen, Checksums und Source-Pfade ändern die Provisionierungsidentität und
können Rebuilds auslösen. Sie ändern keine Connector-Capability und promoten
kein Ergebnis.

## Ausgewählte Build-Routen

| Connector | Build-Target | Ausgewähltes Full-Lifecycle-Profil | Build-/Integrationshinweis |
|---|---|---|---|
| Apache | <code>build-apache</code> | <code>native-httpd-module</code> | Native httpd-Modulroute; APXS- und Host-Eingaben werden getrennt provisioniert/geprüft |
| NGINX | <code>build-nginx</code> | <code>native-nginx-http-module</code> | Native NGINX-HTTP-Modulroute; Modul-, Prefix- und Worker-Pfade bleiben Host-spezifisch |
| HAProxy | <code>build-haproxy</code> | <code>native-htx-filter</code> | Native HTX-Filterroute; Source-/Build-Präsenz ist kein Response-Body-Claim |
| Envoy | <code>build-envoy</code> | <code>ext_proc</code> | Streamed-External-Processing-Route; ein alternativer ext_authz-Helper ist nicht stillschweigend die ausgewählte Route |
| Traefik | <code>build-traefik</code> | <code>native-middleware</code> | Native Middleware-Route mit lokalem UDS-Service; forwardAuth-Compatibility-Helper bleiben getrennt |
| lighttpd | <code>build-lighttpd</code> | <code>patched-native</code> | Gepatchte Native-Host-/Modulroute; Patch-/Build-Erfolg ist kein Full-Lifecycle-Nachweis |

Die Profilwerte werden von Full-Lifecycle-Targets geliefert. Setzen Sie
<code>FULL_LIFECYCLE_HOST_PROFILE</code> nicht manuell, um einen direkten oder
Compatibility-Build umzubenennen.

## Troubleshooting

| Symptom | Bedeutung | Sichere nächste Aktion |
|---|---|---|
| <code>BLOCKED: FRAMEWORK_ROOT is missing</code> / Exit <code>77</code> | Submodule-/Framework-Pfad ist nicht verfügbar | Submodule initialisieren oder <code>FRAMEWORK_ROOT</code> auf einen vertrauenswürdigen vorhandenen Framework-Checkout setzen |
| Build-Root wird abgewiesen | Ausgabe liegt im Checkout oder ist anderweitig unsicher | <code>BUILD_ROOT</code> oder <code>VERIFIED_RUN_PARENT</code> auf absoluten externen beschreibbaren Pfad setzen |
| Component Preparation fehlt | Cache/Snapshot fehlt oder Vorbereitung wurde übersprungen | <code>make prepare-runtime-components</code> ohne Skip-Flag ausführen |
| Compiler-Profil übersprungen | Optionales C-Profil ist nicht verfügbar | Dokumentierten Default-C17-Check verwenden oder Compiler mit optionalem Profil installieren |
| Config-Check schlägt fehl | Build, Host-Konfiguration oder Eingabedatei ist ungültig | Passendes Build-Target ausführen, sanitisiertes Log prüfen und dokumentierte Variablen verifizieren |

Kopieren Sie keine Roh-Logs mit Cookies, Authorization-Headers, TLS-Private-
Keys oder anderen sensitiven Werten in Issues oder kanonische Evidence.
