# Change Record: Vollständige Parent-HAProxy-SonarQube-Cloud-Remediation

**Sprache:** [English](CR-20260801-sonar-haproxy-complete-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260801-sonar-haproxy-complete-remediation |
| Datum (UTC) | 2026-08-01 |
| Basis-Revision | `f70110536cd163cebce5f57ccd8ca95d5cf9f02b` |
| Tracking | Vollständige aktuelle `connectors/haproxy/`-SonarQube-Cloud-Remediation. Die Hosted-Verifikation bestand für den aktualisierten PR-Head `4dbd7c0e2bf49374c4d1e70e2cfc0fb51c060198`; diese Delivery-Record-Korrektur benötigt vor dem Merge eine weitere Exact-Head-Runde. |
| Grenze | Parent `connectors/haproxy/`, dessen direkte Tests/Checks sowie dieses bilinguale Change-Record-/Index-Paar. Framework, MRTS, Gitlinks, andere Connectoren, Workflows, Sonar-Konfiguration, Suppressions und direkte `master`-Writes bleiben out of scope. Der aktuelle Nutzer autorisierte ausschließlich die kontrollierte Integration von PR #210 nach `master`. |

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
- Alle Änderungen Parent-only halten; nur über den aktuell autorisierten,
  Exact-Head-geschützten PR-#210-Workflow integrieren.

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
| `gh pr checks 210` bei `4dbd7c0e2bf49374c4d1e70e2cfc0fb51c060198` | bestanden: 33 Checks, 0 fehlgeschlagen |
| SonarQube Cloud PR #210 bei `4dbd7c0e2bf49374c4d1e70e2cfc0fb51c060198` | bestanden: Quality Gate `OK`, 0 neue Issues, 0,0 % New-Code-Duplikation |

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
Verifikation erfolgt deshalb am exakten veröffentlichten PR-Head. Der
aktualisierte Head `4dbd7c0e2bf49374c4d1e70e2cfc0fb51c060198` bestand; diese
nur dokumentarische Delivery-Record-Korrektur erzeugt einen neuen Head, der
vor dem Merge dieselbe Hosted-Evidence erhalten muss.

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
offengelegt. Nach dem aktuellen `master`-Refresh bestand Head
`4dbd7c0e2bf49374c4d1e70e2cfc0fb51c060198` alle 33 Hosted-Checks und das
SonarQube-Cloud-Quality-Gate mit null neuen Issues und null New-Code-
Duplikation. Die vorliegende nur dokumentarische Delivery-Record-Korrektur
ändert den PR-Head erneut; seine finalen Exact-Head-Checks und sein Quality
Gate müssen vor dem autorisierten Merge beobachtet werden. Dieser Record
beansprucht kein Review oder Merge.

## Verbleibende Risiken

Der finale Documentation-Correction-Head kann ein anderes Hosted-Ergebnis
erhalten. Jede von null abweichende New Violation, neue Duplicate Line,
New-Code-Duplication-Density, fehlgeschlagener Required Check, blockierendes
Review oder ungelöste Konversation benötigt task-eigenes Follow-up, bevor der
PR gemergt werden kann.

## Finaler Diff- und Review-Status

Der lokale Diff bleibt auf den Parent-HAProxy-Bereich und das Change-Record-
Paar begrenzt. Der aktuelle Nutzer hat `bringe das pr 210 in den master`
ausdrücklich autorisiert. Nach dem nur dokumentarischen Follow-up-Commit
benötigt sein neuer exakter Head eine frische finale Checks-, Review-,
Konversations- und SonarQube-Cloud-Runde. Die autorisierte Integration nutzt
danach die etablierte Squash-Methode des Repositorys mit Exact-Head-Schutz;
kein direkter `master`-Write, Bypass oder Auto-Merge ist zulässig.
