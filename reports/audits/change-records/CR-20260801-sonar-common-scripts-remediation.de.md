# Change Record: Parent-`common/scripts`-SonarQube-Cloud-Remediation

**Sprache:** [English](CR-20260801-sonar-common-scripts-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260801-sonar-common-scripts-remediation` |
| Datum (UTC) | 2026-08-01 |
| Basis-Revision | `6b4aca18d390363764b96d85cd31969b9bb114a1` |
| Tracking | Aktuelles SonarQube-Cloud-Inventar für `common/scripts/`: 15 Security- und 12 Maintainability-Zeilen. |
| Grenze | Nur Parent `common/scripts/`, direkte Parent-Tests sowie dieses englisch/deutsche Change-Record-Paar und die Indizes. |
| Delivery-Status | Ein task-eigener Draft-PR ist autorisiert; dieser Pre-Delivery-Record beansprucht keinen Commit, Push, PR, keine Hosted-Analyse und keinen Merge. |

## Motivation und Problemstellung

Das aktuelle SonarQube-Cloud-Inventar für `common/scripts/` meldet 15
Security- und 12 Maintainability-Befunde. Der Runtime-Smoke-Helper verarbeitet
Request-, Runtime-Pfad-, Process-, Loopback-Listener- und Evidence-Output-
Inputs. Sein einzelner langer Ablauf vermischte zudem Vorbereitung, Probes,
Outcome-Erzeugung und Cleanup. Der Smoke-Result-Writer und der C++-Targeted-
Evaluator enthielten Maintainability-Befunde für konzentrierten Kontrollfluss
beziehungsweise manuelles Resource-Cleanup.

## Implementierungsentscheidung und Begründung

Der Python-Runner validiert jetzt den engen lokalen Smoke-Protokollvertrag,
bevor Request-Metadaten Loopback-URLs oder den Evaluator erreichen:
unterstützte Methoden, Origin-Form-Targets, begrenzte Portnummern, feste
Probe-Targets, Targeted-Evaluator-Argumente, reguläre Non-Symlink-Connector-
Binaries und verifizierte Output-Roots sind explizite Verträge. Process-
Argumente bleiben strukturierte Listen und der Result-Writer wird direkt statt
über einen Python-Subprozess aufgerufen.

Die Lighttpd- und generischen Proxy-Pfade des Runners sind in Vorbereitungs-,
Probe-, Evidence-, Outcome- und Cleanup-Helper zerlegt. Exception-Pfade geben
gestartete Prozesse und lokale Server vor der Rückkehr frei. Der Writer ist in
kleine Payload- und Dokument-Helper geteilt und behält Connector-Name,
Verified-Root und descriptor-basiertes No-Follow vor jedem Output-Write. Der
C++-Evaluator nutzt RAII für Engine-, Rules-, Transaction- und Rule-Error-
Cleanup; der resultierende Source ist C++17-kompatibel.

Keine SonarQube-Cloud-Regel, kein Quality Gate, keine Exclusion, Suppression,
`NOSONAR`, Workflow-, Framework-, MRTS-, Gitlink- oder `master`-Änderung ist
Teil dieser Arbeit.

## Akzeptanzkriterien

Alle 27 aktuellen Source-Zeilen im genannten SonarQube-Cloud-Scope besitzen
eine konkrete Source-Remediation; fehlerhafte lokale Request-Daten scheitern
vor einem Network- oder Evaluator-Sink; Runtime-Output- und Executable-Grenzen
bleiben fail-closed; normale lokale Smoke-Result-Erzeugung bleibt verfügbar;
der Evaluator kompiliert unter C++17; fokussierte Regression-Tests bestehen;
und der spätere exakte PR-Head muss null New Issues und 0,0 % New-Code-
Duplizierung ohne Scanner-Konfigurationsänderung nachweisen.

## Geänderte Dateien

- `common/scripts/run_local_runtime_smoke.py`
- `common/scripts/write_smoke_result.py`
- `common/scripts/modsecurity_targeted_eval.cc`
- `tests/test_local_runtime_smoke_request_body.py`
- `tests/test_common_runtime_smoke_crs_source_security.py`
- dieses englisch/deutsche Change-Record-Paar und seine Indizes.

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| Gewähltes Parent-Python: `python -m py_compile common/scripts/run_local_runtime_smoke.py common/scripts/write_smoke_result.py` | bestanden. |
| Gewähltes Parent-Python: `python -m unittest -q tests.test_local_runtime_smoke_request_body tests.test_common_runtime_smoke_crs_source_security tests.test_write_smoke_result_security tests.test_c_cpp_diagnostics` | bestanden: 56 Tests. |
| `make check-targeted-evaluator-cpp17` mit task-eigenem Build-Root und der verfügbaren dynamischen `libmodsecurity.so.3.0.15` | bestanden: der Targeted-C++17-Evaluator kompilierte; er wurde nicht ausgeführt. |
| `git diff --check` | vor der Dokumentationsauslieferung bestanden; erneute Ausführung vor dem Commit erforderlich. |
| Versiegelte Codex-Security-Diff-Reviews | bestanden: vollständige Abdeckung der initial drei geänderten Produktquellen und des finalen Sonar-Remediation-Amendments; null reportbare Befunde. |

## Security-Auswirkung

Die Änderung verengt die Input-Grenze des lokalen Smoke-Helpers, ohne seine
Autorität auszuweiten. Sie macht die Loopback-Request-Erzeugung deterministisch,
stoppt unerwartete Methoden und Request-Target-Formen vor lokalen Handlern oder
Evaluator, beschränkt die Executable-Auswahl auf das benannte reguläre
Connector-Binary und bewahrt Verified-Output-Path- sowie No-Follow-Write-
Controls. Strukturierte Subprocess-Argumente bleiben in Verwendung. C++-RAII
verhindert, dass Error-Path-Resource-Ownership von wiederholten manuellen
Cleanup-Branches abhängt.

## Verbleibende Risiken

Der lokale Helper führt weiterhin das ausdrücklich ausgewählte Connector-
Binary aus und linkt den test-only Evaluator gegen den bereitgestellten lokalen
libmodsecurity-Build. Die ergänzte Validierung verengt diese Inputs, belegt
aber keine Publisher-Provenance eines developer-kontrollierten Binary oder
einer Library; dies bleibt dieselbe Local-Development-Trust-Boundary und
benötigt normales geprüftes Build-Provisioning.

## Runtime-Evidence

Fokussierte Python-Controls decken fehlerhafte und Absolute-Form-Request-
Behandlung, Request-Body-Protokollverträge, CRS-Source-Security,
Result-Writer-Output-Containment und C/C++-Diagnostik ab. Der Targeted-
Evaluator besitzt einen erfolgreichen C++17-Kompilierungscontrol gegen die
verfügbare dynamische libmodsecurity.

## Bekannte Einschränkungen

Die isolierte Task-Umgebung führte keine vollständige Connector-Host-Runtime-
Matrix aus. Die Targeted-Evaluator-Kompilierung verwendete die verfügbare
dynamische Library, nachdem ein Static-Link-Versuch fehlende transitive
Libraries im lokalen Artefaktset zeigte; das ist eine lokale Linkage-
Environment-Einschränkung, keine Source-Änderung und kein beanspruchtes
Runtime-Ergebnis.

## Nicht ausgeführte Prüfungen mit Begründung

- Eine vollständige Connector-Host-Runtime-Matrix wurde nicht ausgeführt, weil
  dieser Task auf die Source-Remediation von `common/scripts/` begrenzt ist und
  die isolierte Umgebung keine task-provisionierte Host-Binary-Matrix besitzt.
- Ein statischer Targeted-Evaluator-Link wurde nicht als Evidence akzeptiert,
  weil dem verfügbaren statischen libmodsecurity-Artefakt seine transitiven
  YAJL-, Lua- und XML-Link-Inputs fehlen. Der dynamische C++17-
  Kompilierungscontrol bestand stattdessen.
- GitHub-Actions- und SonarQube-Cloud-Checks können erst existieren, nachdem
  der autorisierte task-eigene Draft-PR committed und veröffentlicht ist. Ihre
  Ergebnisse sind vor jeder Merge-Betrachtung für den exakten PR-Head nötig.

## Finaler Diff- und Review-Status

Die initialen und finalen Amendment-versiegelten Security-Diff-Reviews liegen außerhalb des Checkouts unter
`/var/tmp/codex/ModSecurity-conector/runs/common-scripts-sonar-remediation-20260801/security-diff-scan/report.md`.
Der finale Amendment-Receipt liegt unter
`/var/tmp/codex/ModSecurity-conector/runs/common-scripts-sonar-remediation-20260801/security-diff-scan-amendment/report.md`.
Zusammen decken sie jede geänderte Produktquell-Datei und den direkten
Amendment-Test ab und fanden keinen reportbaren Security-Befund. Dieser Record beansprucht bewusst keinen Commit, Push, keine
PR-Nummer, keinen Hosted-Check, kein SonarQube-Cloud-Ergebnis, keinen Merge
und keine resultierende `master`-Revision, bevor diese Fakten beobachtet sind.
