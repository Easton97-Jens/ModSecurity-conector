# Change Record: Parent-Apache-Output-Filter-Status-Shadowing für SonarQube Cloud C:S1117

**Sprache:** [English](CR-20260727-sonar-apache-output-filter-status-shadowing.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-apache-output-filter-status-shadowing |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent-SonarQube-Cloud-`c:S1117`-Code-Smell `AZ98JcyRLJyjbmyNA5LH` in `connectors/apache/src/msc_filters.c:1213`. |
| Grenze | Parent-Apache-Output-Filter-Quelltext und sein Parent-Source-Contract-Test sowie dieses englisch/deutsche Change-Record-Paar und Indizes. Framework, MRTS, Gitlinks, Scanner-Konfiguration, Quality Gates, Suppressions und externer Sonar-Issue-Status bleiben unverändert. |

## Motivation und Entscheidung

`output_filter(...)` besitzt bereits eine äußere Statusvariable `rc`. Das
lokale Ergebnis von `apache_finish_unread_request_body(...)` trägt nun den
beschreibenden Namen `request_body_rc`; dadurch verschwindet die überschattete
Deklaration, ohne einen Statuswert, Branch, Request-Body-Vorgang,
Response-Header-Vorgang oder die Apache-Filter-ABI zu ändern.

Der zugehörige Source-Contract-Regressionstest hält den relevanten
Kontrollfluss fest: Ein nicht erfolgreicher Unread-Body-Drain-Status wird vor
dem Response-Header-Abschnitt zurückgegeben, während der bestehende
Erfolgspfad zu diesem Abschnitt weiterläuft.

## Validierung

| Prüfung | Ergebnis |
| --- | --- |
| Fokussiertes Parent-Source-Contract-Modul | bestanden: `tests.test_apache_request_transaction_cleanup`, 6 Tests in 0,013 s. |
| Bestehende Apache-Common-Adoption-Strukturkontrolle | bestanden: `ci/checks/connectors/apache/check-apache-common-adoption.py`. |
| Native Apache-Request-Transaction-Cleanup-Prüfung | blocked_environment: Die Prüfung endete mit 77, weil keine nutzbaren `apxs`/`apxs2`-Apache-Header verfügbar sind; der C-Quelltext wurde nicht kompiliert. |
| `git diff --check` | bestanden, nachdem das vollständige B22-Traceability-Paar und die Indizes ergänzt wurden. |

## Motivation und Problemstellung

Die konkrete Sonar-Regel, der Parent-Umfang und die Begründung für den Erhalt
des Verhaltens stehen im vorhergehenden Abschnitt
`## Motivation und Entscheidung`. Diese strukturelle Korrektur ändert weder
den dokumentierten Quelltext noch das Testverhalten.

## Akzeptanzkriterien

- Die bereits dokumentierte Remediation und fokussierte Validierung bleiben
  unverändert.
- Dieses englisch/deutsche Change-Record-Paar behält gleichwertige technische
  Fakten.
- Blockierte, nicht ausgeführte oder ausstehende gehostete Evidence wird nicht
  als bestanden dargestellt.

## Implementierungsentscheidung und Begründung

Die bestehende Begründung und Validierung bleiben erhalten. Die kanonischen
Change-Record-Überschriften werden ergänzt, statt den Dokumentationschecker zu
schwächen oder eine recordspezifische Ausnahme zu schaffen.

## Geänderte Dateien

Der ursprüngliche versionierte Umfang steht in `## Identität` und der
vorhergehenden Implementierungsbeschreibung. Dieses Follow-up ändert nur die
Struktur dieses Change-Record-Paars.

## Ausgeführte Befehle

Die exakten Befehle und beobachteten Ergebnisse bleiben in `## Validierung`;
diese strukturelle Korrektur klassifiziert kein Ergebnis neu.

## Security-Auswirkung

Der bestehende nachfolgende Abschnitt bleibt für diese konkrete Grenze
maßgeblich. Diese Normalisierung ändert keine Sicherheitskontrolle.

## Sicherheitsauswirkung und Einschränkungen

Sicherheitsklassifikation: `not_applicable` als Sicherheitsbefund. Dies ist
ein Code Smell, kein nachgewiesener angreiferkontrollierter Pfad und keine
gebrochene Kontrolle. Die sicherheitsrelevante Protokollinvariante wurde
dennoch geprüft: Ein Fehler beim Unread-Body-Drain muss vor der Übergabe der
Response-Header an ModSecurity zurückkehren; der fokussierte Source-Contract
erhält diese Reihenfolge. Native Apache-Kompilierungs-/Runtime-Validierung
bleibt wegen fehlender Apache-Entwicklungsheader blockiert. Der lokale Kandidat
ist uncommittet; es gab keine gehostete Sonar-Analyse, keine GitHub-CI, keinen
Commit, Push, Pull Request oder Master-Merge. Der Sonar-Key bleibt OPEN, bis
ein ausgelieferter Head analysiert wird.

## Runtime-Evidence

Diese strukturelle Korrektur beansprucht keine zusätzliche Runtime-Evidence;
die bestehende Validierung behält ausschließlich ihren dokumentierten
Source-Contract-Umfang.

## Bekannte Einschränkungen

Der bestehende Security- und Validierungstext beschreibt die fehlenden
Apache-Entwicklungsheader und die daraus folgende Begrenzung der nativen
Validierung.

## Verbleibende Risiken

Die Record-Normalisierung führt kein neues Risiko ein. Gehostete Analyse und
eventuelle native Apache-Evidence bleiben auf später tatsächlich beobachtete
Ergebnisse begrenzt.

## Nicht ausgeführte Prüfungen mit Begründung

Für diese reine Dokumentationskorrektur werden kein zusätzlicher
Connector-Runtime-Test, kein nativer Apache-Build und kein gehosteter Check
ausgeführt; die ursprünglichen blockierten Voraussetzungen bleiben unverändert.

## Finaler Diff- und Review-Status

Die frühere Delivery-Formulierung ist eine Momentaufnahme der ursprünglichen
lokalen Validierung. Dieser Record behauptet keine finale PR-Verifikation,
keinen Merge und keinen Sonar-Issue-Abschluss für einen späteren Delivery-Head.
