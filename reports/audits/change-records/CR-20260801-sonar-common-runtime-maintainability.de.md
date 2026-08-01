# Change Record: Parent-Common-Runtime-SonarQube-Cloud-Maintainability-Remediation

**Sprache:** [English](CR-20260801-sonar-common-runtime-maintainability.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260801-sonar-common-runtime-maintainability |
| Datum (UTC) | 2026-08-01 |
| Basis-Revision | `b370740dcb16739be7e0b323152f69da31c1a8c1` (finale PR-Basis nach dem erforderlichen Pre-Push-Refresh) |
| Tracking | Vollständige aktuelle `common/runtime/`-SonarQube-Cloud-Maintainability-Remediation. Hosted-Verifikation ist für den exakten veröffentlichten PR-Head erforderlich. |
| Grenze | Parent `common/runtime/`, der direkte Common-SDK-Contract-Check und dieses bilinguale Change-Record-/Index-Paar. Framework, MRTS, Gitlinks, andere Parent-Bereiche, Workflows, SonarQube-Cloud-Konfiguration, Suppressions, Exclusions, Quality Gates und direkte `master`-Writes sind out of scope. |

## Motivation und Problemstellung

Das aktuelle Master-SonarQube-Cloud-Inventar für `common/runtime/` enthält
18 offene/bestätigte Maintainability-Zeilen und keine Security-, Bug-,
Hotspot- oder Duplication-Zeile. Der Auftrag ist, diesen vollständigen
aktuellen Bereich in einem Parent-Pull-Request zu remedieren, ohne
Scanner-Policy zu ändern oder Befunde zu verstecken.

| Regel | Anzahl | Remediation-Disposition |
| --- | ---: | --- |
| `c:S1820` | 1 | Kohäsiven privaten Transaction-State gruppiert. |
| `c:S107` | 1 | Die breite Body-Limit-Helper-Argumentliste durch typisierten Progress- und Policy-Kontext ersetzt. |
| `c:S995` | 2 | Read-only-Runtime-/Parser-Pointer als `const` markiert. |
| `c:S5350` | 10 | Immutable Views für Read-only-Runtime- und Parser-Operationen erhalten. |
| `c:S3776` | 3 | Konfigurationsvalidierung, Event-Konstruktion und Transaction-Start-Phasen in benannte private Helper getrennt. |
| `c:S1912` | 1 | Nicht-reentrante Kalenderumwandlung durch plattformsichere reentrante Umwandlung ersetzt. |
| Gesamt | 18 | 16 Zeilen in `msconnector_runtime.c` und 2 Zeilen in `http_authorization_service.c`. |

## Akzeptanzkriterien

- Jede aktuell inventarisierte `common/runtime/`-SonarQube-Cloud-Zeile mit
  einer Source-Level-Remediation oder einer expliziten evidenzbasierten
  Disposition abdecken.
- Begrenztes HTTP-Parsing, Konfigurationsvalidierung, Body-Limit-Policy,
  Transaction-Phasenreihenfolge, Event-Integrität, Error-Propagation und
  öffentliche Runtime-APIs erhalten.
- Geändertes C als C17 mit `-Wall -Wextra -Werror` mit GCC und Clang
  kompilieren.
- New Violations und New-Code-Duplication bei null halten, verifiziert allein
  durch frische SonarQube-Cloud-Analyse des exakten PR-Heads.
- Nur einen task-eigenen Draft-PR liefern; dieser Record autorisiert keinen
  Merge nach `master`.

## Implementierungsentscheidung und Begründung

Das private Transaction-Objekt gruppiert jetzt zusammengehörige begrenzte
Event-Metadaten und die bereits öffentliche
`msconnector_runtime_body_progress`-Werte. Öffentliche Progress-Accessors
behalten ihre bisherigen Output-Felder; die Runtime behält weiterhin keinen
Host-Request-, Response- oder Body-Pointer. `apply_body_limit_plan` erhält
deshalb ein typisiertes Progress-Objekt und den bestehenden Policy-Kontext
anstatt zehn unabhängiger Pointer und Werte.

Das Konfigurationsparsing ist nach Value-Familie partitioniert und bewahrt alle
akzeptierten Keys, Ziele, Defaults, Validierungsfunktionen, Side Effects und
Error-Texte. Die Event-Assembly ist in Body-, Response-State-, Host-Action-
und JSONL-Write-Helper getrennt, ohne Hash-Reihenfolge, Escaping, Size-Checks
oder die Aktualisierung des Previous-Event-Hash zu ändern. Auch der
Transaction-Start ist nur an seinen bestehenden Validierungs-, Allokations-,
Native-Phase- und Request-Body-Grenzen getrennt; Abort-Verhalten bleibt im
bestehenden Cleanup-Pfad zentralisiert.

Der Authorization-Service ändert nur lokale Parser-Traversal-Pointer zu
`const`. Der Timestamp-Helper verwendet `gmtime_r` auf dem POSIX-Build-Pfad
und `gmtime_s` unter Windows und ersetzt den bisherigen nicht-reentranten
Fallback. Es wird keine öffentliche API-, SonarQube-Cloud-Policy-,
Suppression-, Exclusion- oder `NOSONAR`-Markierung eingeführt.

Der direkte Common-SDK-Contract erkennt jetzt die äquivalente gruppierte
private Body-Progress-Repräsentation. Er fordert weiterhin begrenzten
Progress, Limit-Outcomes, expliziten End-of-Stream-State und das Verbot,
Host-owned Request- oder Response-Pointer zu behalten.

## Security-Auswirkung

Die berührten Pfade verarbeiten nicht vertrauenswürdige HTTP-Request-/Response-
Daten und operator-kontrollierte Konfiguration. Der Refactor erhält die
bestehenden Security-Invarianten: String- und Header-Validierung gehen Engine-
Calls voraus; Resource-Limits und Body-Limit-Action bleiben aktiv; nur
begrenzte Metadaten werden in Events kopiert; JSONL-Serialisierung wird vor
dem Write größenvalidiert; und der Flow-Guard erhält Phase- und Immutable-
Finalization-Enforcement. Keine Authentifizierungs-, Autorisierungs-, Parser-
Validierungs-, Limit-, Path-Policy-, Logging-, Test-, Scanner- oder Quality-
Gate-Kontrolle wurde geschwächt.

Der finalisierte lokale Security-Diff-Review deckt beide Runtime-Translation-
Units und den direkten SDK-Contract ab. Er dokumentiert null neue reportbare
Security-Findings; der lesbare Report liegt im task-eigenen externen
Run-Verzeichnis. Dies ist Source-Level-Evidence und beansprucht keine
vollständige native Host-Runtime.

## Geänderte Dateien

- `common/runtime/msconnector_runtime.c`
- `common/runtime/http_authorization_service.c`
- `ci/checks/common/check-common-sdk-contract.py`
- Dieses englisch/deutsche Change-Record-Paar und beide Change-Record-Indizes.

## Ausgeführte Befehle

| Kontrolle | Ergebnis |
| --- | --- |
| `make check-common-helpers-c17` | bestanden |
| `make check-common-sdk-contract` | bestanden |
| `python3 tests/test_sonar_reliability_contract.py` | bestanden: 12 Tests |
| `make check-common-security-contract` | bestanden |
| `make check-common-memory-safety` | bestanden |
| `make check-common-flow-integrity` | bestanden |
| `make check-http-authorization-service-timeout MSCONNECTOR_C_STD=c17` | bestanden |
| GCC-C17-Syntaxcheck für beide geänderten Runtime-Translation-Units | bestanden |
| Clang-C17-Syntaxcheck für beide geänderten Runtime-Translation-Units | bestanden |
| `make check-bilingual-docs` | nur durch bestehende Links in das bewusst nicht initialisierte Framework-Submodul blockiert; kein neues Change-Record- oder Index-Diagnostic |
| `git diff --check` | bestanden |
| Codex Security Diff-Review | bestanden: vollständige Local-Diff-Abdeckung, null reportbare Findings |

## Runtime-Evidence

Der Authorization-Service-Timeout-Smoke prüft begrenzte HTTP-Eingaben,
Loopback-Service-Start, Timeout-Verhalten und Response-Handling. Common-
Helper-, Contract-, Security-, Memory-Safety- und Flow-Controls prüfen die
relevanten Bounded-Data- und Lifecycle-Invarianten. Diese Checks beanspruchen
kein vollständiges natives Connector-plus-libmodsecurity-Host-Matrix-Ergebnis.

## Nicht ausgeführte Prüfungen mit Begründung

Eine vollständige native Host-Matrix läuft lokal nicht, weil diese Änderung auf
die connector-neutrale Runtime begrenzt ist und keinen Host-Adapter auswählt.
Kein Stub, geänderter Gitlink, Framework-Source oder gelockerte Voraussetzung
wurde genutzt, um diese Evidence zu erzeugen. Der lokale SonarQube-Cloud-
Scanner ist nicht installiert; das maßgebliche New-Code-Issue- und
Duplication-Ergebnis muss am exakten veröffentlichten PR-Head beobachtet
werden.

Das Repository besitzt kein `check-documentation`-Make-Target. Die verfügbare
`check-bilingual-docs`-Kontrolle wurde ausgeführt; ihre einzigen Diagnosen sind
bestehende Framework-Submodul-Link-Targets außerhalb dieser Parent-only-
Änderung.

## Bekannte Einschränkungen

Lokale Source- und fokussierte Runtime-Evidence können nicht das Hosted Quality
Gate für einen zukünftigen PR-Commit beweisen. Jedes SonarQube-Cloud-New-Issue,
neue Duplication oder jeder fehlgeschlagene Required Check muss auf dem
Task-Branch vor Review oder Integration korrigiert werden.

## Verbleibende Risiken

Der exakte gepushte Head kann ein anderes Hosted-Ergebnis als das aktuelle
Master-Inventar erhalten. Dieser Record beansprucht keinen PR, kein Review,
keine Hosted-CI-, SonarQube-Cloud- oder Merge-Ergebnisse, die noch nicht
beobachtet wurden.

## Finaler Diff- und Review-Status

Der Diff ist auf Parent-Common-Runtime-Source, seine direkte Contract-Assertion
und den bilingualen Traceability-Record begrenzt. Hosted-Evidence ist nur
gültig, wenn sie an den aktuell veröffentlichten exakten PR-Head gebunden ist;
sie wird getrennt von diesem Record aufbewahrt. Kein direkter `master`-Write
oder Merge ist durch diesen Auftrag autorisiert.
