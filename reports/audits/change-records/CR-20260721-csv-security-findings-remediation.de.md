# Change Record: Behebung der CSV-Sicherheitsbefunde

**Sprache:** [English](CR-20260721-csv-security-findings-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260721-csv-security-findings-remediation |
| Datum (UTC) | 2026-07-21 |
| Basis-Revision | 5fa90474a79eaee2df034bf1c4389572fdcca42f |
| Grenze | Nur Parent-Quellcode, Parent-Tests, Parent-CI/Runtime-Werkzeuge, Parent-Dokumentation und dieses Change-Record/Index-Paar. Der Branch übernimmt den aktuellen Framework-Gitlink von Parent-master, aber diese Aufgabe verändert weder Framework noch MRTS. |
| Finding-Verknüpfung | Importierte Codex-Security-CSV-Zeilen CSV-01 bis CSV-19; task-owned SonarQube-Cloud-S5443-Follow-up FND-SONAR-0010. |

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
- Ein öffentlich schreibbarer Runtime-Vorgänger wird nur akzeptiert, nachdem
  sein geöffneter Descriptor Root-Ownership und Sticky-Semantik belegt.
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
nativen Puffergrenze. Das Sonar-Follow-up ersetzt Pfadnamenvertrauen für
öffentliche temporäre Wurzeln durch Descriptor-basierten Beweis für
Verzeichnis, UID 0, Sticky-Bit und schreibbaren Mode und erhält die vorhandenen
No-Follow-, Nachfolger-Owner- und Final-Root-Prüfungen.

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

## Current-Master-Fortsetzung (2026-07-23)

Der Draft wurde mit einer bewussten Union-Auflösung vom Parent-`master`
`b37aa629398501f83750d6454f5f6a27eb614818` aktualisiert. Die aktuellen
immutable Action-Pins, der Go-Version-Contract, das strikte
Verified-Report-Evidence-Gate, die Authorization-Timeout-Prüfung und beide
Sprachindizes bleiben gemeinsam erhalten.

Die Fortsetzung behebt anschließend die lokal behebbaren Sonar-Befunde, ohne
eine Kontrolle abzuschwächen: Descriptor-Traversal und Chunk-Parsing sind bei
gleichen Guards in kleinere Helfer aufgeteilt, der Content-Length-Parser
bleibt ASCII-only, der Authorization-Service bindet Per-Connection-Status in
einen privaten Kontext, und die Regressionstests vermeiden verschachtelte
beziehungsweise Mehrfachaufruf-Assertions. Der Timeout-Smoke-Fake behält die
nicht-konstanten Signaturen aus `msconnector_runtime.h` bei, weil dessen
Produktivimplementierungen diese Objekte verändern; es wurde weder eine
Scanner-Suppression noch eine öffentliche ABI-Änderung verwendet.
Ein Exact-Head-Sonar-Detail-Readback zeigte anschließend 22
`python:S3415`-Hinweise zur Assertion-Reihenfolge. Sie sind auf die native
`actual, expected`-Reihenfolge korrigiert, ohne Testbedingung oder geschützte
Kontrolle zu verändern. Die zwei `c:S995`-Hinweise im Timeout-Smoke waren
echte Lücken im Fake-Lifecycle und keine Const-Correctness-Gelegenheit: Die
Fake-Runtime zählt jetzt aktive Transaktionen, und die Fake-Transaktion hält
Owner und Completion-Status. Das Fake-`begin` speichert einen gültigen Owner
und erhöht dessen Zähler; das idempotente Fake-`finish` validiert, dekrementiert
und markiert den Abschluss. Das erhält die gemeinsame nicht-konstante ABI und
macht den Smoke-Lifecycle ohne Scanner-Suppression verhaltenswirksam.

Der Branch wurde anschließend normal auf den aktuellen Parent-`master`
`a308d7b414f0859490fe7253e0683a4bde80b563` aktualisiert. Dabei wurde nur die
aktuelle Framework-Gitlink-Aktualisierung übernommen; kein Framework- oder
MRTS-Worktree wurde von dieser Aufgabe initialisiert, verändert, gestaged oder
committed.

## Ausgeführte Befehle

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| Fokussierte Parent-Unittest-Suite für Compiler-Guides, Workflow-Sicherheit, bilinguale Dokumentation, Generated-Report-Evidence, Runtime-Pfade, Pfadauflösung, Smoke-Request-Bodies und HAProxy-HTX-IDs | bestanden: 146 Tests nach dem S5443-Follow-up (die frühere rebased Suite enthielt 144 Tests). |
| Pre-Fix-S5443-Regressions-Trio für root-owned/sticky-, unsafe-root- und Fremdbesitzer-Pfade | erwartetes Fehlschlagen: Die alte Pfadnamen-Allowlist lehnte die synthetische sichere Wurzel ab, bevor sie den vorgesehenen Ownership-Pfad ausüben konnte. |
| Post-Fix-S5443-Regressions-Trio | bestanden: Root-owned/sticky Shared-Root gelingt; non-sticky/non-root Shared-Roots und fremdbesitzte Nachfolger schlagen vor Final-Root-Erstellung fehl. |
| Vier fokussierte Runtime-Pfad-Policy-Kontrollen | bestanden: Mutable-Root-, Broad-Parent-, ausgewählte Python-Policy- und System-Root-Ablehnungskontrollen bleiben bestanden. |
| Vollständiges Runtime-Path-Policy-Unittest-Modul | blocked_environment für einen Framework-gestützten Shell-Checker: Dem absichtlich nicht initialisierten Framework-Gitlink fehlt `ci/lib/common.sh`; die anderen vier Kontrollen bestanden. |
| Ruff check / format check für die beiden Python-Dateien | not_run: Die ausgewählte Parent-virtuelle Umgebung enthält kein `ruff`-Executable; es wurde keine Dependency installiert. |
| make check-http-authorization-service-timeout mit GCC und Clang | für beide Compiler bestanden. |
| make check-common-helpers-c17 mit GCC und Clang | für beide Compiler bestanden. |
| Common-SDK- und Common-Security-Source-Contract-Kontrollen | bestanden. |
| sh -n für drei geänderte Runtime-Lifecycle-Shell-Einstiegspunkte | bestanden. |
| Strikter Generated-Report-Layout-Checker gegen die aktuelle Evidence | erwartetes Fehlschlagen: unvollständige/veraltete Evidence wurde abgelehnt. Das belegt CSV-06-Fail-Closed-Verhalten und ist kein bestandener Provenienzstatus. |
| make check-bilingual-docs und kanonischer Framework-gestützter HAProxy-Harness | blockiert: Der Framework-Gitlink fehlt absichtlich im Parent-only-Checkout und wurde nicht initialisiert oder verändert. |
| Finales git diff --check nach Abschluss des Change Records | bestanden: keine Whitespace-Fehler im Task-Worktree. |
| Current-Master-Fortsetzung: `tests.test_runtime_path_security`, `tests.test_local_runtime_smoke_request_body`, `tests.test_haproxy_htx_transaction_id` und `tests.test_generated_report_evidence_integrity` | bestanden: 90 Tests einschließlich Symlink-/Ownership-, Request-Framing-, ASCII-Content-Length-, HTX-ID- und Report-Integrity-Kontrollen. |
| Current-Master-Fortsetzung: `tests.test_resolve_runtime_paths` | bestanden: 8 Tests. |
| Current-Master-Fortsetzung: Workflow-Security- und Compiler-Guide-Suiten | bestanden: 37 Tests nach der Konflikt-Union. |
| Current-Master-Fortsetzung: Authorization-Timeout-Smoke | mit GCC und Clang unter isolierten externen Build-Wurzeln bestanden; Common-C17-Helper- und Shell-Syntax-Prüfung bestanden ebenfalls. |
| Current-Master-Fortsetzung: fokussiertes Security-Diff-Review | bestanden: keine neue plausible Sicherheitsregression im geprüften Zehn-Dateien-Remediation-Diff. |
| Exact-Head-Sonar-`S3415`-Assertion-Reihenfolgen-Follow-up | bestanden: 92 fokussierte Runtime-Pfad-, bilinguale Dokumentations- und Generated-Report-Evidence-Tests nach allen 22 Actual/Expected-Reihenfolgenkorrekturen. |
| Current-Master-Fortsetzung: verhaltenswirksamer Timeout-Smoke-Fake-Lifecycle | bestanden: GCC-/Clang-Timeout-Smoke-Kompilierung und -Ausführung üben normales Begin/Finish-Ownership- und Count-Bookkeeping ohne Änderung der Common-Runtime-ABI. |

## Security-Auswirkung

Dies ist Defense-in-Depth über Request-Verarbeitung, lokale Runtime-Werkzeuge,
CI-/Report-Provenienz und einen Connector-Helfer. Es schließt einen getesteten
Local-Helper-Forwarding-Fall für mehrdeutiges TE+CL- und wiederholtes
CL/TE-Framing sowie eine bei der
Prüfung entdeckte plausible Containment-Lücke für konfiguriertes MATRIX_ROOT.
Das S5443-Follow-up lehnt außerdem einen root-owned, aber nicht-sticky
öffentlichen Vorgänger ab, statt ihn anhand seines Pfadnamens zu akzeptieren.
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
sichtbar und werden nicht als gelöst dargestellt. Die lokale S5443-
Source-Remediation ist `fixed`, aber nicht `verified` oder `closed`, bis ein
normaler Follow-up-Push ein frisches Exact-Head-SonarQube-Cloud-Quality-Gate
und einen gefilterten Issue-Readback erhält. Der gemeinsame root-lokale
kanonische Finding-Store ist read-only; sein erforderlicher inkrementeller
FND-SONAR-0010-Import ist daher `blocked_permissions`, und der retained
Task-Record behauptet nicht, diesen Import zu ersetzen. Der exakte PR-Head
benötigt weiterhin reguläre CI, Review und Resulting-Master-Evidence vor jeder
späteren Integrationsentscheidung.

Die verhaltenswirksame `c:S995`-Behebung des Timeout-Smokes benötigt einen
frischen gehosteten Exact-Head-Sonar-Readback. Sie unterdrückt keinen Hinweis
und ändert die öffentlichen Runtime-Deklarationen nicht allein für eine
Stilregel.

## Verbleibende Risiken

Die lokalen Kontrollen können weder die fehlenden Framework-gestützten
kanonischen Connector-Prüfungen noch eine betroffene Lighttpd-Runtime, eine
vollständige Host-/Connector-Matrix oder den Remote-PR-CI-Status belegen.
Bestehende unvollständige Report-Evidence bleibt absichtlich blockierend.
Descriptor-Metadaten können keine Host-ACL-Semantik belegen und schützen nach
dem Schließen der Descriptors nicht gegen einen Angreifer mit derselben UID;
ein dir_fd-haltendes Sink-Refactoring liegt außerhalb dieser fokussierten
Änderung. Keine Kontrolle, kein Test, Scanner, Branch-Protection oder
Evidence-Anforderung wurde für ein positives Ergebnis abgeschwächt.

## Delivery-Status

Dieser Record unterstützt den bestehenden Parent-only-Draft-PR #74. Er nennt
bewusst keinen aktuellen veröffentlichten Head: Jede lokale Fortsetzung
benötigt einen normalen Commit und Push mit anschließendem frischem
Exact-Head-Check-Snapshot. Er autorisiert weder Merge noch Direct-Master-Push,
Framework-/MRTS-Arbeit, History-Rewrite oder die Behauptung bestandener
Remote-CI.

## Finaler Diff- und Review-Status

Der aktuelle lokale Worktree-Whitespace-Review bestand mit git diff --check.
Die fokussierten Security-Regression-/Kontrolltests, die ausgewählte
146-Test-Parent-Suite, vier Runtime-Pfad-Policy-Kontrollen und die bilingualen
Change-Record-Tests bestanden. Ein Framework-gestützter Policy-Checker ist
durch den absichtlich fehlenden Framework-Gitlink blockiert, und Ruff ist in
der ausgewählten venv nicht verfügbar. Ein fokussierter Security-Diff-Review,
normaler Commit/Push, frisches Exact-Head-Sonar-Ergebnis, Remote-CI und Human
Review bleiben getrennte Beobachtungen, bis sie stattfinden.
