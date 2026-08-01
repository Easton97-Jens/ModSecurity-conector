# Change Record: Vollständige Parent-HAProxy-SonarQube-Cloud-Remediation

**Sprache:** [English](CR-20260801-sonar-haproxy-complete-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260801-sonar-haproxy-complete-remediation |
| Datum (UTC) | 2026-08-01 |
| Basis-Revision | `c3319575ae86d9810da8b5428590336d60cd3daf` |
| Tracking | Vollständige aktuelle `connectors/haproxy/`-SonarQube-Cloud-Remediation; SHA-gebundene Hosted-Verifikation steht noch aus. |
| Grenze | Parent `connectors/haproxy/`, dessen direkte Tests/Checks sowie dieses bilinguale Change-Record-/Index-Paar. Framework, MRTS, Gitlinks, andere Connectoren, Workflows, Sonar-Konfiguration, Suppressions und `master` bleiben unverändert. |

## Motivation und Problemstellung

Das aktuelle Master-SonarQube-Cloud-Inventar enthält nach Filterung mit dem
kanonischen Component-Präfix `connectors/haproxy/` 33 offene/bestätigte Zeilen:
ein `python:S5332`-Security-Signal und 32 Maintainability-Zeilen. Der Auftrag
fordert die Remediation dieses gesamten aktuellen Bereichs in einem fokussierten
PR, ohne Sonar-Regeln, Exclusions, Quality Gates oder Scanner-Suppressions zu
ändern.

Die erste Exact-Head-Analyse des Draft-PR #210 identifizierte drei zusätzliche
PR-eigene Reliability-Zeilen in der refaktorierten Runtime: zwei `c:S995`-
Constness-Zeilen und einen `c:S836`-Uninitialized-Value-Error-Path. Dieses
Follow-up committet die enge Typ-/Initialisierungsbehebung vor einer neuen
Exact-Head-Analyse.

| Regel | Anzahl | Remediation-Dispositon |
| --- | ---: | --- |
| `python:S5332` | 1 | Den generischen URL-Öffner durch den bereits eingeschränkten direkten Loopback-HTTPS-Client ersetzt. |
| `python:S9073` | 3 | Zusammengesetzte Module-Loader-Assertions in explizite Vorbedingungen getrennt. |
| `c:S107` | 1 | Die breite Legacy-Server-Parameterliste durch ein typisiertes Konfigurationsobjekt ersetzt. |
| `c:S134` | 9 | Verschachtelte SPOP- und Lifecycle-Branches in benannte Helper verschoben. |
| `c:S1820` | 2 | Kohäsive C17-Runtime-/Konfigurationsmember gruppiert, ohne ihren direkten Access-Contract zu ändern. |
| `c:S3358` | 5 | Verschachtelte Bedingungen durch explizite Branches und Accessors ersetzt. |
| `c:S3776` | 5 | Verantwortlichkeiten für Request, Response, Parser, Server und Command-Dispatch getrennt. |
| `c:S5350` | 1 | Einen read-only Pointer für den Konfigurationswert wiederhergestellt. |
| `c:S5955` | 2 | Fragile indizierte Command-Loops durch einen expliziten Cursor-Helper ersetzt. |
| `c:S886` | 4 | Loop-Control-Variablen lokal in ihren Command-Parser-Helpern gehalten. |
| `c:S995` (PR-Follow-up) | 2 | Read-only-Notify-Inputs als `const` markiert. |
| `c:S836` (PR-Follow-up) | 1 | Den Error-Path-Value-Pointer initialisiert, bevor er geloggt werden kann. |

## Akzeptanzkriterien

- Jede aktuell inventarisierte HAProxy-Zeile mit einer Source-Änderung oder
  einer expliziten, testbaren Disposition abdecken.
- Begrenztes SPOP-Parsing, Transaction-Cache-Lifecycle, ModSecurity-
  Request-/Response-Verarbeitung, Private-Runtime-File-Verhalten und
  Loopback-TLS-Containment erhalten.
- Geändertes C als C17 mit `-Wall -Wextra -Werror` kompilieren.
- PR-New-Code-Violations und -Duplikation bei null halten, verifiziert allein
  durch eine frische SonarQube-Cloud-Analyse des exakten PR-Heads.
- Alle Änderungen Parent-only halten; diesen Record nicht nach `master` mergen.

## Implementierungsentscheidung und Begründung

Der HTX-Smoke-Helper sendet seinen bereits validierten lokalen HTTPS-Request
jetzt mit `http.client.HTTPSConnection`, dem bestehenden Private-Root-
Zertifikatslader und einem expliziten Response-/Connection-Cleanup-Pfad. Er
führt kein Redirect-Handling erneut ein und lockert nicht das credential-free
`https://127.0.0.1`-Prädikat.

Das Native-Binding extrahiert seinen wiederholten Request-Lifecycle in Helper,
die die bisherigen Defaults, libmodsecurity-Aufrufreihenfolge, disruptive
Decision-Checks und einen Final-Cleanup-Pfad erhalten. Die SPOP-Runtime trennt
typed HELLO-Parsing, Request-/Response-Construction, Transaction-Completion,
Notify-Dispatch, Runtime-File-Setup und Command-Line-Parsing. Die Helper
bewahren die bisherigen begrenzten Parser-Primitiven sowie die Unterscheidung
zwischen Request-Body-Limits, optionalen Response-Body-Limits und Legacy-
Evaluation ohne Limit.

Das PR-Follow-up markiert die beiden Helper-Input-Pointer read-only und
initialisiert den Config-Loader-Value-Pointer auf einen bekannten Nullwert. Das
letztere hält die bestehende Fehlermeldung deterministisch, wenn einem
abschließenden `--config` sein Argument fehlt; akzeptierte Command-Line-Syntax
ändert sich nicht.

## Security-Auswirkung

Die geänderten Pfade verarbeiten nicht vertrauenswürdige SPOP-Frames, HTTP-
Request-Metadaten/-Bodies, lokale Runtime-Root-Pfade und einen Loopback-TLS-
Endpunkt. Die Security-Invariante bleibt erhalten: Nur begrenzte typed
Frame-Daten erreichen Request-Felder; der Transaction-Lifecycle kann seine
bisherigen Abort-/Store-/Finish-Regeln nicht überspringen; TLS-Probes bleiben
credential-free HTTPS zu Literal-Loopback mit dem verifizierten Private-Root-
Zertifikat; und Evidence behält Metadaten statt Payloads.
Keine Authentifizierungs-, Parser-, TLS-, File-Containment-, Logging-, Test-,
Scanner- oder Quality-Gate-Kontrolle wurde geschwächt. Es wurde keine
`NOSONAR`-, Suppression-, Exclusion- oder Sonar-Konfigurationsänderung genutzt.

Der versiegelte lokale Security-Diff-Review des initialen exakten Four-File-
Patches und des nachfolgenden Three-File-PR-Follow-ups erfassen jeweils null
neue reportbare Security-Findings. Ihre aufbewahrten Reports sind
`/var/tmp/codex/ModSecurity-conector/runs/haproxy-complete-sonar-pr-20260801/security-diff-scan-c3319575/report.md`
und
`/var/tmp/codex/ModSecurity-conector/runs/haproxy-complete-sonar-pr-20260801/security-diff-scan-follow-up-4b364607/report.md`.

## Geänderte Dateien

- `connectors/haproxy/harness/haproxy_htx_smoke_helper.py`
- `connectors/haproxy/harness/test_haproxy_htx_smoke_helper.py`
- `connectors/haproxy/src/haproxy_modsecurity_binding.c`
- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`
- Dieses englisch/deutsche Change-Record-Paar und beide Change-Record-Indizes.

## Ausgeführte Befehle

| Kontrolle | Ergebnis |
| --- | --- |
| `cc -std=c17 -Wall -Wextra -Werror -fsyntax-only -Icommon/include -Iconnectors/haproxy/src connectors/haproxy/src/haproxy_modsecurity_binding.c` | blockiert: installierte libmodsecurity-Header deklarieren `msc_get_rules_messages_rule_ids` nicht |
| `cc -std=c17 -Wall -Wextra -Werror -fsyntax-only -Icommon/include -Iconnectors/haproxy/src connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` | bestanden |
| `python3 -m unittest tests.test_sonar_reliability_contract tests.test_haproxy_htx_transaction_id` | bestanden: 15 Tests |
| `python3 ci/checks/connectors/haproxy/check-haproxy-common-adoption.py` | bestanden |
| `python3 ci/checks/connectors/haproxy/check-haproxy-htx-overlay.py` | bestanden: 26 Checks |
| `python3 -m py_compile connectors/haproxy/harness/haproxy_htx_smoke_helper.py connectors/haproxy/harness/test_haproxy_htx_smoke_helper.py` | bestanden |
| `python3 ci/checks/documentation/check-bilingual-docs.py` | nur durch fehlende Links in das bewusst nicht initialisierte Framework-Submodul blockiert; kein Fehler nennt das neue Change Record oder den Index |
| `git diff --check` | bestanden |
| Codex Security Security-Diff-Finalisierung | bestanden: initiale Four-File- und Follow-up-Three-File-Abdeckung, null reportbare Findings |

## Runtime-Evidence

`tests.test_haproxy_htx_transaction_id` führt die legitime Loopback-TLS-Probe
und die Unsafe-URL-Kontrolle aus. Die Contract-Checks decken statische Parser-,
Transaction-, HTX- und Common-Adoption-Invarianten ab. Sie beanspruchen kein
vollständiges natives HAProxy-plus-libmodsecurity-Runtime-Ergebnis.

## Nicht ausgeführte Prüfungen mit Begründung

`make -C connectors/haproxy build-modsecurity-binding` ist
`blocked_external_dependency`: Der projektnative Target findet keine
libmodsecurity-Development-Header oder -Bibliothek unter `/src` oder im
registrierten Task-Build-Root. Das fokussierte Harness-Modul wird außerdem
nicht als ganzes Modul ausgeführt, weil es ein bewusst nicht initialisiertes
Framework-Submodul in diesem Parent-only-Worktree importiert. Es wurde kein
Framework-Source, Gitlink, Stub oder Bypass eingeführt, um diese Grenze zu
ändern. Der lokale Sonar-Scanner ist nicht installiert; die SonarQube-Cloud-
Verifikation muss deshalb am exakten veröffentlichten PR-Head erfolgen.

Der unabhängige Binding-Syntax-Befehl erreicht das installierte, inkompatible
libmodsecurity-Declaration-Set: `msc_get_rules_messages_rule_ids` fehlt. Auch
dies ist eine externe Dependency-Grenze; es wurde keine künstliche Deklaration
oder Compiler-Warning-Lockerung ergänzt.

Der Whole-Tree-Checker für bilinguale Dokumentation wurde nach dem Hinzufügen
dieses Records ausgeführt. Er meldet nur bestehende Links in dasselbe bewusst
nicht initialisierte Framework-Submodul; kein neues Change-Record- oder
Index-Diagnostic bleibt. Das Framework wurde nicht nur initialisiert, um eine
Parent-only-Dokumentationsprüfung grün zu machen.

## Bekannte Einschränkungen

Draft PR #210 wurde aus dem initialen Remediation-Commit erstellt. Seine erste
Exact-Head-Analyse hat korrekt die oben dokumentierten drei PR-eigenen Zeilen
offengelegt; die Follow-up-Source-Änderungen warten auf ein frisches
Exact-Head-Hosted-Ergebnis. Dieser Record beansprucht kein bestehendes Quality
Gate, Review-Resultat oder Merge, bevor jedes davon am finalen Delivery-Head
beobachtet wurde.

## Verbleibende Risiken

SonarQube Cloud kann nach der PR-Analyse ein Source-Level-Detail melden, das
vom aktuellen Master-API-Inventar abweicht. Jede von null abweichende New
Violation, neue Duplicate Line oder New-Code-Duplication-Density sowie jede
verbleibende HAProxy-Baseline-Zeile benötigt task-eigenes Follow-up, bevor der
PR als verifiziert gelten kann.

## Finaler Diff- und Review-Status

Der lokale Diff bleibt auf den Parent-HAProxy-Bereich und das Change-Record-
Paar begrenzt. Er ist für finale Dokumentationsvalidierung und kontrollierte
Draft-PR-Delivery vorbereitet. Eine `master`-Integration ist von diesem Task
nicht autorisiert.
