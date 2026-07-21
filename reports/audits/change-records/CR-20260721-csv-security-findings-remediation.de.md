# Change Record: Behebung der CSV-Sicherheitsbefunde

**Sprache:** [English](CR-20260721-csv-security-findings-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260721-csv-security-findings-remediation |
| Datum (UTC) | 2026-07-21 |
| Basis-Revision | 5fa90474a79eaee2df034bf1c4389572fdcca42f |
| Grenze | Nur Parent-Quellcode, Parent-Tests, Parent-CI/Runtime-Werkzeuge, Parent-Dokumentation und dieses Change-Record/Index-Paar. Framework, MRTS, Abhängigkeiten und Gitlinks bleiben unverändert. |
| Finding-Verknüpfung | Importierte Codex-Security-CSV-Zeilen CSV-01 bis CSV-19. |

## Motivation und Problemstellung

Die bereitgestellte Codex-Security-Zusammenfassung enthält 19 Befunde zu
bereits vorhandenen Behebungen, Build-Provenienz, Request-Parsing,
Runtime-Artefakt-Containment, Workflow-Evidence, generierten Berichten und
Connector-Helfersicherheit. Diese Änderung gleicht jede Zeile mit dem aktuellen
Parent-Stand ab, implementiert anwendbare Parent-only-Behebungen und benennt
ungelöste Evidence-Lücken explizit.

## Akzeptanzkriterien

- CSV-01 bis CSV-19 haben jeweils eine explizite Disposition.
- Anwendbare Parent-only-Behebungen besitzen fokussierte Regressionstests;
  frühere Behebungen werden weder zurückgenommen noch doppelt gepatcht.
- Mehrdeutiges Transfer-Encoding-plus-Content-Length-Framing wird abgelehnt,
  bevor eine Backend-Anfrage abgesetzt wird.
- Jede konfigurierte Runtime-Schreibwurzel einschließlich MATRIX_ROOT wird
  descriptor-begrenzt und eigentumsvalidiert, bevor sie verwendet wird.
- Build- und Report-Evidence-Kontrollen schlagen fehlgeschlossen fehl.
- Englische/deutsche Dokumentation bleibt gepaart.
- Der resultierende PR ist Draft/offen und wird nicht gemergt.

## Dispositionen der Befunde

| CSV-Zeile | Disposition |
| --- | --- |
| CSV-01 | Bereits durch Parent-Commit 1fc2321 behoben (Apache Phase-4 Bypass); kein doppelter Patch. |
| CSV-02 | Bereits durch Parent-Commit 63819e4 behoben (privilegierter Submodule-Workflow); kein doppelter Patch. |
| CSV-03 | Gepinnte und verifizierte libmodsecurity-Tag-/Commit-Anweisungen vor Detached Checkout, Submodule-Update, Build, Test und Install implementiert. |
| CSV-04 | Nichtblockierende Authorization-Clients, monotone Deadline, begrenztes Polling und 408 für langsame Clients implementiert. |
| CSV-05 | Bereits durch Parent-Commit 63819e4 behoben (Write-Token des Updated-Submodule-Workflows); kein doppelter Patch. |
| CSV-06 | Striktes Verified-Report-Provenienz-/Evidence-Gate implementiert. Aktuelle Evidence lässt es absichtlich fehlschlagen; finale Provenienz ist blocked_missing_evidence und nicht passed. |
| CSV-07 | Descriptor-sichere, no-follow- und eigentumsvalidierte Behandlung aller konfigurierten Schreibwurzeln einschließlich MATRIX_ROOT implementiert. |
| CSV-08 | Bereits durch Parent-Commit a73c335 behoben (Blocked-Status-Marker); kein doppelter Patch. |
| CSV-09 | Validierung von Markdown-Fence-Markern und -Längen für generierte Berichte implementiert. |
| CSV-10 | Keine Lighttpd-Quellcodeänderung: blocked_missing_evidence. Im isolierten Parent-Checkout fehlen gepinnter betroffener Lighttpd-Quellcode/Host/Modul sowie Queue-/Multi-Chunk-Client-Evidence. |
| CSV-11 | Bereits durch Parent-Commit aabde81 behoben (veränderliche Projektwurzeln); kein doppelter Patch. |
| CSV-12 | Remote-Rule-Merging implementiert: Leere Remote-Werte erben lokale Werte; partielle Remote-Credential-Konfiguration wird abgelehnt. |
| CSV-13 | Begrenztes lokales Smoke-Request-Body-/Chunk-/Trailer-Parsing und Deadlines implementiert; TE+CL und wiederholtes CL/TE-Framing werden vor dem Forwarding abgelehnt. |
| CSV-14 | Validierte Verified-Run-IDs für Runtime-Artefaktpfade implementiert. |
| CSV-15 | Strenge BUILD_ROOT-Evidence-Weitergabe für Report-Layout-/Provenienzprüfungen implementiert. |
| CSV-16 | Zufällige task-eigene sichere Temporär-Writer statt vorhersagbarer Pfade implementiert. |
| CSV-17 | HAProxy-HTX-Transaktions-IDs auf das native 127-Zeichen-Payload-Limit begrenzt, mit Parent-only-Regression. |
| CSV-18 | Validierung deutscher Companions generierter Berichte und ihrer Layout-/Evidence-Regeln implementiert. |
| CSV-19 | Bereits durch Parent-Commit 0f82f74 behoben (Action Majors); kein doppelter Patch. |

## Implementierungsentscheidung und Begründung

Nur ungelöstes Parent-eigenes Verhalten wird geändert. Der Authorization-Service
verwendet nun monotones Timeout/nichtblockierendes Polling; der Smoke-Helper
lehnt TE+CL und wiederholtes CL/TE-Framing vor dem Forwarding ab; alle Lifecycle-Schreibwurzeln werden
descriptor-begrenzt, nicht nur die Default-Wurzel; Run-IDs,
no-follow-Verzeichnisoperationen und zufällige task-eigene Temporärverzeichnisse
verhindern Traversal-, Symlink- und Kollisionspfade. Generierte Berichte
erfordern unveränderliche Build-Provenienz, striktes Layout/Evidence und
strukturell gültige bilinguale Inhalte. HAProxy-Helfer-IDs bleiben an der
nativen Puffergrenze.

## Geänderte Dateien

- Compiler-Guide-Generierung und englische/deutsche Compiler-Guides;
- Verified-Report-Workflow, Evidence-Receipt-/Layout-Prüfungen und
  Berichtsgeneratoren;
- Runtime-Pfad-, Run-ID- und Temporärverzeichnis-Helfer sowie direkte
  schreibfähige Lifecycle-Einstiegspunkte;
- lokales Smoke-Request-Parsing, Authorization-Timeout, Remote-Rule-Merging
  und HAProxy-HTX-Helferverhalten;
- fokussierte Python-, Shell-, C-, Workflow-, Dokumentations- und
  Evidence-Tests;
- dieses englische/deutsche Change-Record-Paar und das Indexpaar.

## Ausgeführte Befehle

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| Fokussierte Parent-Unittest-Suite für Compiler-Guides, Workflow-Sicherheit, bilinguale Dokumentation, Generated-Report-Evidence, Runtime-Pfade, Pfadauflösung, Smoke-Request-Bodies und HAProxy-HTX-IDs | bestanden: 144 Tests nach Rebase auf die aktuelle Master-Basis. |
| make check-http-authorization-service-timeout mit GCC und Clang | für beide Compiler bestanden. |
| make check-common-helpers-c17 mit GCC und Clang | für beide Compiler bestanden. |
| Common-SDK- und Common-Security-Source-Contract-Kontrollen | bestanden. |
| sh -n für drei geänderte Runtime-Lifecycle-Shell-Einstiegspunkte | bestanden. |
| Strikter Generated-Report-Layout-Checker gegen die aktuelle Evidence | erwartetes Fehlschlagen: unvollständige/veraltete Evidence wurde abgelehnt. Das belegt CSV-06-Fail-Closed-Verhalten und ist kein bestandener Provenienzstatus. |
| make check-bilingual-docs und kanonischer Framework-gestützter HAProxy-Harness | blockiert: Der Framework-Gitlink fehlt absichtlich im Parent-only-Checkout und wurde nicht initialisiert oder verändert. |
| Finales git diff --check nach Abschluss des Change Records | bestanden: keine Whitespace-Fehler im Task-Worktree. |

## Security-Auswirkung

Dies ist Defense-in-Depth über Request-Verarbeitung, lokale Runtime-Werkzeuge,
CI-/Report-Provenienz und einen Connector-Helfer. Es schließt einen getesteten
Local-Helper-Forwarding-Fall für mehrdeutiges TE+CL- und wiederholtes
CL/TE-Framing sowie eine bei der
Prüfung entdeckte plausible Containment-Lücke für konfiguriertes MATRIX_ROOT.
Es behauptet weder Produktionshost-Exposure noch eine vollständige
Connector-Matrix oder Produktions-Exploitierbarkeit über die getesteten
Kontrollen hinaus.

## Runtime-Evidence

Eine vollständige Host-/Connector-Matrix war nicht verfügbar. Der lokale
Helper-Test belegt, dass TE+CL- oder wiederholte-CL/TE-Eingaben 400 erhalten und nicht zum Test-Backend
weitergeleitet werden; er belegt kein Apache-, NGINX-, Lighttpd-, HAProxy-,
HTTP/2- oder HTTP/3-Runtime-Verhalten. Für CSV-10 lag keine
Lighttpd-Queue-/Multi-Chunk-Behebungs-Evidence vor.

## Nicht ausgeführte Prüfungen mit Begründung

- Das strikte Verified-Report-Gate kann erst bestehen, wenn aktuelle
  authentische Runtime-Evidence erzeugt wird; fehlende/veraltete Evidence
  bleibt absichtlich eine fehlschlagende Kontrolle.
- Framework-gestützte kanonische Connector-Prüfungen liefen nicht, weil der
  Framework-Gitlink fehlt und außerhalb des Scopes liegt. Er wurde nicht
  initialisiert, geändert, gestaged oder committed.
- Keine MRTS-Arbeit, kein Deployment-, Produktionshost-, vollständiger
  Connector-Matrix-, HTTP/2- oder HTTP/3-Check wurde durchgeführt.

## Bekannte Einschränkungen und Follow-up

CSV-06 bleibt blocked_missing_evidence, bis authentische aktuelle
Verified-Runtime-Reports das strikte Gate erfüllen. CSV-10 bleibt
blocked_missing_evidence, bis eine gepinnte betroffene Lighttpd-Umgebung und
Queue-/Multi-Chunk-Test-Evidence vorliegen. Beide Punkte bleiben im Draft-PR
sichtbar und werden nicht als gelöst dargestellt. Der exakte PR-Head benötigt
weiterhin reguläre CI, Review und Resulting-Master-Evidence vor jeder späteren
Integrationsentscheidung.

## Verbleibende Risiken

Die lokalen Kontrollen können weder die fehlenden Framework-gestützten
kanonischen Connector-Prüfungen noch eine betroffene Lighttpd-Runtime, eine
vollständige Host-/Connector-Matrix oder den Remote-PR-CI-Status belegen.
Bestehende unvollständige Report-Evidence bleibt absichtlich blockierend.
Keine Kontrolle, kein Test, Scanner, Branch-Protection oder
Evidence-Anforderung wurde für ein positives Ergebnis abgeschwächt.

## Delivery-Status

Dieser Record unterstützt einen Parent-only-Draft-Pull-Request. Er autorisiert
weder Merge noch Direct-Master-Push noch Framework-/MRTS-Arbeit oder die
Behauptung bestandener Remote-CI. Finale Diff-Prüfung, Commit, Push,
PR-Erstellung und PR-Check-Snapshots werden erst nach Beobachtung dokumentiert.

## Finaler Diff- und Review-Status

Der finale lokale Worktree-Whitespace-Review bestand nach der
Change-Record-Schema-Korrektur mit git diff --check. Ein fokussierter
Security-Review und die aufgeführten lokalen Kontrollen sind abgeschlossen.
Commit, Push, Draft-PR-Erstellung, Remote-CI und Human Review bleiben getrennte
künftige Beobachtungen, bis sie stattfinden.
