# Change Record: Parent-HAProxy-SPOE-Header-Parser-Deduplizierung und SonarQube-Cloud-Reliability-Behebung

**Sprache:** [English](CR-20260729-sonar-haproxy-spop-header-parser-duplication.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260729-sonar-haproxy-spop-header-parser-duplication |
| Datum (UTC) | 2026-07-29 |
| Basis-Revision | `dbbc9c6aa2bca22fcd0385fa76b878873ccab2cc` |
| Tracking | Vier aktuelle SonarQube-Cloud-`c:S1854`-Befunde in `handle_connection(...)` und zwei aktuelle Duplikatblöcke (82 Zeilen) in `parse_notify_payload(...)`. |
| Grenze | Parent-HAProxy-Diagnose-Runtime, ein Parent-Reliability-Contract-Test und dieses englisch/deutsche Change-Record-Paar mit seinen gepaarten Indizes. Framework, MRTS, Gitlinks, Workflows, Sonar-Konfiguration, Quality Gates, Suppressions und `master` bleiben unverändert. |
| Delivery-Status | Ein Draft-Parent-PR ist die vorgesehene Auslieferung. Dieser Record beansprucht nur beobachtete lokale Checks, keine gehostete CI, kein gehostetes Quality Gate, keinen externen Issue-Abschluss und keinen Merge. |

## Motivation und Problemstellung

`parse_notify_payload(...)` enthielt vier strukturell duplizierte Zweige für
binäre und textuelle Request-/Response-Header-Argumente. Die Zweige mussten
Typed-Value-Grenzen, Parse-Fehlerverhalten, Header-Ownership und
Response-Rollen-Semantik gleich halten. SonarQube Cloud meldet außerdem vier
`c:S1854`-Zuweisungen ohne Leser in derselben Runtime: einen ungenutzten
initialen Diagnosezeiger und drei Werte nach Body-Trunkierung oder einem
Transaction-Cache-Fehler.

Der aktuelle Master-Duplikatdienst meldet zwei Quell-Duplikatblöcke in dieser
Datei mit zusammen 82 Zeilen. Es sind genau die wiederholten Header-Zweige;
das Follow-up reduziert bewusst diesen gemeinsamen Produktcode, statt die
Sonar-Konfiguration zu ändern oder Ausschlüsse einzuführen.

## Akzeptanzkriterien

- Die vier Header-Argument-Zweige delegieren an zwei begrenzte Helper, ohne
  akzeptierte Typed-Werte, Parser-Position, Response-Rolle oder
  Fehlerweitergabe zu ändern.
- Temporäre Text-Header-Ownership wird auf jedem Nicht-Transfer-Pfad freigegeben
  und erst nach einer erfolgreichen Ersetzungsentscheidung übertragen.
- Die vier gemeldeten ungelesenen Diagnosezuweisungen werden entfernt, ohne
  Body-Limits, Transaction-Cleanup, Fail-open-/Fail-closed-Auswahl oder
  ACK-Erzeugung zu schwächen.
- Eine dauerhafte C17-Harness deckt binäre und textuelle Header-Helper für
  Request- und Response-Rollen ab, einschließlich eines Nicht-Byte-Werts mit
  Response-Key.
- Lokale Checks bestehen; eine frische Exact-Head-SonarQube-Cloud-Analyse muss
  weiterhin null neue Issues, null New-Code-Duplizierung und eine niedrigere
  Gesamtduplikatanzahl beweisen, bevor der Kandidat als hosted-verifiziert gilt.

## Implementierungsentscheidung und Begründung

`parse_notify_headers_bin(...)` zentralisiert das begrenzte Lesen des
Typed-Bytes und den Binär-Header-Parser. `parse_notify_headers_text(...)`
verwendet dieselbe begrenzte Lesegrenze, erhält das bestehende temporäre
`notify_request`-Parsing und überträgt dessen alloziertes Header-Array nur,
wenn es nicht leer und nicht kleiner als die bereits geparste Header-Liste ist.
Beide Helper setzen `is_response`, nachdem der Typed-Wert konsumiert wurde. Das
erhält bewusst das frühere Verhalten für Response-Keys mit syntaktisch gültigem
Nicht-Byte-Typed-Wert.

Die früheren `reason`-Strings für Body-Trunkierung oder Transaction-Cache-
Fehler wurden nur gesetzt, aber nie gelesen. Die Refaktorierung entfernt nur
diese ungelesenen Zuweisungen. Fehlerspezifische Gründe bleiben in den beiden
ModSecurity-Fehlerzweigen lokal, wo `runtime_init_decision(...)` sie nutzt.

## Geänderte Dateien

- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` — zwei begrenzte
  Header-Parser-Helper, vier Call-Site-Ersetzungen und Entfernung von vier
  ungelesenen Zuweisungen.
- `tests/test_sonar_reliability_contract.py` — dauerhafte C17-Source-Harness
  für binäre/textuelle Header-Behandlung und Erhalt der Response-Rolle.
- `reports/audits/change-records/CR-20260729-sonar-haproxy-spop-header-parser-duplication.md`
  und `.de.md` — dieses bilinguale Change-Record-Paar.
- `reports/audits/change-records/README.md` und `README.de.md` — gepaarte
  Indexeinträge.

## Ausgeführte Befehle

| Ausgeführte Kontrolle | Beobachtetes Ergebnis |
| --- | --- |
| Fokussierte `unittest`-Methode `test_haproxy_append_string_runtime_boundaries` | bestanden; die C17-Harness kompiliert und führt die tatsächliche HAProxy-Diagnose-Runtime einschließlich der neuen Binär-/Text-Helper-Checks aus. |
| `ci/checks/connectors/haproxy/check-haproxy-common-adoption.py` | bestanden. |
| `ci/checks/connectors/haproxy/check-haproxy-c-standard-wiring.py` | bestanden. |
| `make check-haproxy-c17-lint` | bestanden; die verpflichtende C17-Kompilierung wurde abgeschlossen. |
| `git diff --check` | bestanden. |
| `make check-bilingual-docs` | blocked_external_dependency nach Validierung dieses Change-Record-Paars: Der isolierte Worktree hat keinen initialisierten Parent-festgeschriebenen Framework-Checkout, daher fehlen 20 vorbestehende Cross-Repository-Dokumentationslinks. |
| Fokussierter Codex-Security-Diff-Scan | bestanden mit null reportbaren Befunden; der vollständige Parser-Source und der unterstützende Test wurden geprüft, und die C17-Harness lieferte direkte Regressionsevidence. |

## Security-Auswirkung

Der geänderte Code verarbeitet HTTP-abgeleitete, nicht vertrauenswürdige
SPOE-Payload-Werte. Die Helper behalten `read_typed_bytes_ref(...)` als einzige
Typed-Value-Grenze bei, erhalten `-1`-Parse-Fehler und ersetzen Header erst
nach einer vollständig geparsten, qualifizierten temporären Liste. Der
Response-Marker bleibt für Response-Header-Keys auch dann wahr, wenn das
Typed-Argument kein String oder Binärwert ist; dies entspricht dem Verhalten
vor der Refaktorierung. Keine Authentifizierung, Autorisierung,
Prozessberechtigung, Netzwerk-Listener, Scanner- oder Quality-Gate-Kontrolle
wird gelockert.

## Runtime-Evidence

Die fokussierte C17-Harness kompiliert und führt die tatsächliche
HAProxy-Diagnose-Runtime-Translation-Unit aus. Sie prüft die neuen Binär- und
Text-Header-Helper für Request- und Response-Rollen, die konsumierte
Parser-Position und Header-Flags und erhält das frühere Response-Key-Verhalten
für ein Nicht-Byte-Argument. Dies ist direkte Source-Ausführungs-Evidence,
keine End-to-End-HAProxy-Deployment-Evidence.

Der kanonische fokussierte Scan-Report liegt außerhalb des Git-Worktrees unter
`/var/tmp/codex/ModSecurity-conector/security-scans/ModSecurity-conector/dbbc9c6-local-patch-20260729T042755Z/report.md`.

## Bekannte Einschränkungen

- Die C17-Harness ist direkte Source-Ausführung, kein Live-Integrationstest
  mit HAProxy und libmodsecurity.
- Das vollständige Modul `tests/test_sonar_reliability_contract.py` hat einen
  separat reproduzierbaren aktuellen-Master-Fehler in der unveränderten
  Traefik-Optionaltext-Harness; er wird diesem HAProxy-Patch nicht zugerechnet.
- `make check-bilingual-docs` erkennt dieses englisch/deutsche Paar, ist aber
  durch 20 Cross-Repository-Links blockiert, weil dieser isolierte Parent-
  Worktree bewusst keinen initialisierten Framework-Checkout hat.

## Verbleibende Risiken

- Gehostete GitHub-Checks und eine frische Exact-Head-SonarQube-Cloud-Analyse
  bleiben erforderlich, bevor behauptet wird, dass die vier externen Befunde
  und 82 Quell-Duplikatzeilen auf dem Delivery-Head geschlossen sind.

## Nicht ausgeführte Prüfungen mit Begründung

Es liefen keine Live-Integration mit HAProxy und libmodsecurity und keine
vollständige Connector-Matrix, weil diese fokussierte Sonar-Behebung eine
begrenzte native Harness hat und die erforderlichen externen Runtime-Fixtures
in diesem Worktree nicht vorhanden sind. Das vollständige Reliability-Contract-
Modul lief und scheiterte nur in der unveränderten Traefik-Optionaltext-Harness;
derselbe Einzeltest scheitert auf aktuellem `master`, daher wird er als
Baseline-Fehler dokumentiert, weder unterdrückt noch diesem Patch zugerechnet.
Gehostete CI und SonarQube Cloud sind auf einem Delivery-Head noch nicht
gelaufen.

## Finaler Diff- und Review-Status

Der Kandidat ist auf den Parent-HAProxy-Connector und seinen fokussierten Test
sowie bilinguale Traceability begrenzt. Er reduziert bestätigte bestehende
Duplikate und bestätigte bestehende Sonar-Befunde gemeinsam. Der finale Diff
hat keine Whitespace-Fehler, und die lokalen C17-, HAProxy-Adoption- und
HAProxy-Standards-Checks bestehen. Kein Merge ist autorisiert oder behauptet.
