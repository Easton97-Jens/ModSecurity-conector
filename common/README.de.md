# Common connector-neutrale Schicht

**Sprache:** [English](README.md) | Deutsch

## Zweck und Grenze

\`common/\` enthält wiederverwendbare connector-neutrale Contracts und Helfer,
die Adapter-Implementierungen gemeinsam verwenden. Es kann Request-, Response-,
Transaction-, Intervention-, Status-, Origin-, Logging-, Capability- und
Evidence-Shapes modellieren, ohne von einem Apache-, NGINX-, HAProxy-, Envoy-,
Traefik- oder lighttpd-SDK abzuhängen.

Es ist weder ein universeller Host-Adapter noch eine Server-ABI oder ein
Runtime-Nachweis. Host-Lifecycle-Hooks, Protocol-Framing,
Server-Konfigurations-Glue und client-sichtbares Enforcement bleiben im
zuständigen Connector-Baum. Ein erfolgreicher Common-Compile oder Contract-Check
ist kein Production-, CRS-, Full-Matrix- oder Runtime-Verification-Claim.

## Struktur und Source of Truth

| Pfad | Zweck | Source of Truth / Ablageregel |
| --- | --- | --- |
| \`include/msconnector/\` | Öffentliche C-first neutral types und Contracts | Header definieren die gemeinsame Interface-Shape. Hier nur connector-neutrale Deklarationen halten. |
| \`src/\` | Neutrale C-Implementierungen | Eine \`.c\`-Implementierung samt zugehörigem Header-Level-Contract zusammen ergänzen; siehe [src-Notizen](src/README.de.md). |
| \`runtime/\` | Wiederverwendbare lokale Decision-Service-/Runtime-Unterstützung | Muss host-neutral bleiben und darf nicht zu einer Server-Hook-Implementierung werden. |
| \`rules/\` | Eingecheckte targeted smoke rules | Repository-Testinputs, keine Aussage über vollständige Rule-Coverage. |
| \`scripts/\` | Lokale Test-/Evidence-Helfer | Nur portable Helfer ohne Host-SDK- oder System-Path-Abhängigkeit ergänzen. |
| \`docs/\` | Detaillierte Design-Notizen | Die [Common-Architektur](../docs/architecture.de.md) ist der aktuelle Dokumentationsindex für Grenzen und Ownership. |

Die eingecheckten Header und der Source sind maßgeblich für den Shared-Code-
Contract. Das Root-[Makefile](../Makefile) ist maßgeblich für
Validierungs-Targets. Generierte Evidence und Connector-Capabilities sind keine
Source of Truth für die Common-API.

## Wohin Änderungen gehören

Einen neuen neutralen Type in \`include/msconnector/\` und seine Implementierung
in \`src/\` ablegen, nur wenn er ohne Host-SDK kompiliert und einen klaren
connector-neutralen Owner hat. Einen portablen Smoke-/Evidence-Helfer in
\`scripts/\` oder \`runtime/\` mit zugehörigem Test oder Check ablegen.
Designentscheidungen in \`docs/\` und der aktuellen Architekturdokumentation
festhalten.

Keine Apache-Module, NGINX-Direktiven, HAProxy-SPOE-/HTX-Verarbeitung,
Envoy-Filter, Traefik-Middleware, lighttpd-Module-Hooks, Host-Build-Glue oder
Server-Header hier ablegen. Keine Runtime-Ausgaben, Caches, externen
Source-Trees, Download-Artefakte, Secrets oder connector-lokalen Test-Cases
committen.

## Variablen und Platzhalter

Das Root-Makefile besitzt diese Eingaben. Vollständige Definitionen und
Sicherheitsregeln stehen in der [Variablenreferenz](../docs/reference/variables.de.md).
Die Begriffe für Ownership, Interventionen und Lifecycle-Phasen stehen im
[Glossar](../docs/reference/glossary.de.md).

| Name | Lokale Bedeutung | Pflicht, Format und Beispiel |
| --- | --- | --- |
| \`MSCONNECTOR_C_STD\` | C-Sprachmodus für die Common-Helper-Kompilierung | Optional; Repository-Default ist \`c17\`. Einen unterstützten Modus wie \`c17\`, \`c23\` oder \`c2y\` nur mit passendem Target und Compiler-Support verwenden. |
| \`MSCONNECTOR_CFLAGS\` | Compiler-Flags für Common-Helper | Optional; Repository-Default ist \`-std=$(MSCONNECTOR_C_STD) -Wall -Wextra -Werror\`. \`$(MSCONNECTOR_C_STD)\` ist Make-Syntax, die die benannte Make-Variable expandiert; nicht als Literal in eine Shell kopieren. |
| \`MSCONNECTOR_COMPILER_ID\` | Compiler-Executable-ID für Standard-Erkennung | Optional; Default ist der Basisname von \`CC\`. Einen installierten Compiler-Namen wie \`clang\` nur bei bewusster Übersteuerung der Erkennung angeben. |
| \`BUILD_ROOT\` | Generierter Build-/Check-Workspace | Optional und vom Root-Makefile abgeleitet. Ein Override muss ein absolutes beschreibbares Verzeichnis außerhalb des Checkouts sein, etwa \`/srv/modsecurity-work/build\`; kein Source- oder Secret-Ort. |
| \`<repository-root>\` | Reiner Dokumentationsplatzhalter für den absoluten Checkout-Root | Er benennt den Checkout mit \`common/\` und \`Makefile\`; \`/srv/src/ModSecurity-conector\` ist ein portables Beispiel. Winkelklammern nicht in ein Kommando aufnehmen. |

Keiner dieser Werte ist ein Secret. Keine Credentials, Token-Werte oder
benutzerspezifischen Pfade in Header, Source, Testausgabe oder Dokumentation
aufnehmen.

## Relevante Targets

| Target | Zweck und Ergebnisgrenze |
| --- | --- |
| \`make check-common-helpers\` | Kompiliert und führt den isolierten Common-Helper-Smoke mit den gewählten C-Flags aus. Exit \`0\` deckt nur diesen Check ab. |
| \`make check-common-sdk-contract\` | Prüft SDK-nahe Common-Contract-Erwartungen, ohne eine Host-Integration zu belegen. |
| \`make check-common-security-contract\` | Prüft Common-Security-/Data-Flow-Constraints. Kein Penetration-Test. |
| \`make check-common-memory-safety\` | Führt den fokussierten Memory-Safety-Contract des Repositorys aus. Er beweist nicht sämtliches Runtime-Memory-Verhalten. |
| \`make check-common-flow-integrity\` | Prüft Flow-/Ownership-Wiring auf Contract-Ebene. |
| \`make check-directive-parity\` | Prüft die Parität gemeinsamer Directive-Specs; connector-spezifisches Host-Parsing bleibt außerhalb von \`common/\`. |
| \`make lint\` | Enthält diese Strukturchecks plus weitere Repository-Checks; erzeugt keine kanonische Runtime-Evidence. |

Vor der Wertung eines Ergebnisses als Implementierungs- oder Runtime-Claim die
[Common-Architektur](../docs/architecture.de.md), den
[Testing-Guide](../docs/testing-and-evidence.de.md) und den
[Evidence-Guide](../docs/testing-and-evidence.de.md) verwenden.
