# Change Record: Parent-HAProxy-HTX-Diagnosebereichsliteral für SonarQube Cloud `shelldre:S1192`

**Sprache:** [English](CR-20260728-sonar-haproxy-htx-diagnostic-s1192.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260728-sonar-haproxy-htx-diagnostic-s1192 |
| Datum (UTC) | 2026-07-28 |
| Basis-Revision | `8e8acb8dab1cd03723de269cab7da7dd62e5e010` |
| Tracking | Parent-SonarQube-Cloud-Issue `AZ9cRysjHhV2CayPTP01`, Regel `shelldre:S1192`, ursprünglich gemeldet bei `connectors/haproxy/harness/run_haproxy_htx_runtime.sh:445` für das Literal `1,160p`, das in 13 Fehlerdiagnosen wiederholt wurde. |
| Grenze | Ausschließlich Parent-HAProxy-HTX-Runtime-Harness, sein fokussierter Parent-Helper-Contract-Test sowie dieses englisch/deutsche Change-Record-Paar mit seinen Indizes. Framework, MRTS, Gitlinks, Makefiles, Workflows, Scanner-Konfiguration, Quality Gates, Suppressions und externer Issue-Status bleiben unverändert. |
| Kandidatenstatus | Nur lokaler Kandidat. Ein zukünftiger Draft Pull Request und seine frische Exact-Head-gehostete Validierung stehen aus. Dieser Record behauptet keinen Commit, Push, Pull Request, Merge, `master`-Update oder globalen SonarQube-Cloud-Abschluss. |

## Motivation und Problemstellung

Der HAProxy-HTX-Runtime-Harness verwendete den statischen `sed`-Bereich
`1,160p` in 13 Fehlerdiagnose-Aufrufen. SonarQube Cloud meldete dieses
wiederholte Literal als `shelldre:S1192`. Der Bereich ist eine feste
Darstellungsgrenze für Fehlerlogs; er ist keine Runtime-Eingabe und steuert
weder HAProxy- noch ModSecurity-Request-Verarbeitung.

Der Kandidat benennt den Bereich einmal als readonly-Shell-Variable
`HAPROXY_HTX_DIAGNOSTIC_RANGE` und verwendet diese Variable an allen 13
Diagnose-Aufrufstellen. Der abweichende vorbestehende Version-Datei-
Diagnosebereich `1,40p` bleibt eigenständig und liegt außerhalb dieser Änderung.

## Akzeptanzkriterien

- `HAPROXY_HTX_DIAGNOSTIC_RANGE` deklariert genau den festen Wert `1,160p`.
- Die 13 betroffenen Fehlerdiagnosen behalten ihre bestehenden Log-Operanden,
  die Operation `sed -n`, Standardfehlerumleitung, `|| true` und das
  anschließende Fehler-`exit`-Verhalten.
- Die Änderung fügt weder eingabeabgeleitete Shell-Auswertung hinzu noch
  verändert sie eine Parent/Framework/MRTS-Ownership-Grenze.
- Ein fokussierter Contract-Test prüft die exakte Diagnose-Befehlsfolge,
  während Live-HAProxy-Runtime ausdrücklich außerhalb der Evidence dieses
  Kandidaten bleibt.
- Eine zukünftige Exact-Head-gehostete Analyse eines Draft ist erforderlich,
  bevor behauptet werden kann, dass der externe SonarQube-Cloud-Issue
  geschlossen ist.

## Implementierungsentscheidung und Begründung

Es wird eine Shell-Variable `readonly` verwendet, statt die Fehlerpfade zu
ändern oder eine Hilfsfunktion einzuführen. Der Wert ist vom Repository
kontrollierter konstanter Text, daher erhält jeder Aufruf
`sed -n "$HAPROXY_HTX_DIAGNOSTIC_RANGE" <bestehendes-log> >&2 || true` den
ursprünglichen Bereich, Operand, Redirection, das Best-Effort-
Diagnoseverhalten und den umgebenden `exit`-Pfad. Dies ist ausschließlich eine
Literalzentralisierung.

Der fokussierte Helper-Contract-Test liest den Harness als Source-Text und
prüft eine Deklaration, kein verbleibendes wiederholtes Literal
`sed -n '1,160p'` sowie die vollständige geordnete Liste der 13 aktualisierten
Diagnose-Aufrufe samt unveränderter `1,40p`-Version-Datei-Diagnose. Er schützt
damit die Diagnoseschnittstelle, ohne eine Host-Runtime auszuführen.

## Geänderte Dateien

- `connectors/haproxy/harness/run_haproxy_htx_runtime.sh` — Kandidaten-
  Literalzentralisierung im Parent-Shell-Harness für die 13 `1,160p`-
  Fehlerdiagnosen.
- `connectors/haproxy/harness/test_haproxy_htx_smoke_helper.py` — fokussierte
  Source-Contract-Abdeckung für Deklaration und exakte Diagnose-Befehle.
- `reports/audits/change-records/CR-20260728-sonar-haproxy-htx-diagnostic-s1192.md`
  und `.de.md` — dieses bilinguale Change-Record-Paar.
- `reports/audits/change-records/README.md` und `README.de.md` — gepaarte
  Indexeinträge.

## Ausgeführte Befehle

| Ausgeführte Kontrolle | Beobachtetes Ergebnis |
| --- | --- |
| `rtk proxy -- sh -n connectors/haproxy/harness/run_haproxy_htx_runtime.sh` | bestanden. |
| `rtk proxy -- git diff --check -- connectors/haproxy/harness/run_haproxy_htx_runtime.sh connectors/haproxy/harness/test_haproxy_htx_smoke_helper.py` | bestanden. |
| Exakter `awk`-Source-Contract für alle 14 geordneten `sed -n`-Aufrufe (die 13 zentralisierten Fehlerdiagnosen plus die unabhängige `1,40p`-Version-Datei-Diagnose) | bestanden. |
| Python-Source-Syntaxkompilierung von `connectors/haproxy/harness/test_haproxy_htx_smoke_helper.py` | bestanden. |
| Lokale Struktur des gepaarten Change Record, reziproke Sprachlinks, gepaarte README-Indexeinträge, Runtime-Grenzformulierung und `git diff --check` | bestanden: Beide Records enthalten 12 Top-Level-Abschnitte. Diese enge lokale Kontrolle erzwang nicht den kanonischen Change-Record-Überschriftenvertrag. |
| Fokussierte Ausführung von `tests.test_haproxy_htx_smoke_helper` in einem disposable read-only Parent-pinned-Framework-Overlay | bestanden: 9 Tests. |
| Vollständiger Parent-Bilingual-Dokumentationscheck im korrigierten exact read-only candidate overlay | bestanden: Parent-Bilingual-Dokumentation `OK`, Repository-Path-Referenzen `PASS` und Framework-Dokumentationslinks `OK`. Der initiale Lauf schlug ausschließlich fehl, weil diesem Change-Record-Paar kanonische Pflichtüberschriften fehlten; das korrigierte Paar wurde erfolgreich erneut geprüft. |
| Fokussierter Security-Review der Shell-only-Änderung | freigegeben: Der Bereich bleibt ein repository-kontrollierter readonly-Wert und Befehlsoperanden, Fehlerumleitung, Best-Effort-Diagnostik und Fehler-Exits bleiben erhalten. |

Die statischen HTX-Harness-Kontrollen und die neun fokussierten Helper-Tests
bestanden im exact read-only overlay. Keines der Ergebnisse ist Host-Runtime-
Evidence.

## Security-Auswirkung

Diese Änderung berührt eine Shell-Befehl-Diagnosegrenze und erhielt deshalb
einen fokussierten Review. `HAPROXY_HTX_DIAGNOSTIC_RANGE` ist statischer,
vom Repository kontrollierter Text, weder Command-Substitution noch
requestabgeleitete Daten. Er wird als derselbe quotierte `sed -n`-Bereich an
jeder betroffenen Aufrufstelle übergeben. Der Kandidat verändert weder
Befehlsoperanden, Standardfehlerumleitung, `|| true`, Cleanup noch
Fehler-Exits; er fügt keinen Shell-Injection-Pfad, keine Privilegänderung,
keine Netzwerkoperation und keine Request-Datenverarbeitung hinzu.

## Runtime-Evidence

Es wurde keine Host-Runtime ausgeführt. Dieser Record besitzt keine Live-
HAProxy-, HTX-, SPOP- oder ModSecurity-Runtime-Evidence. Der fokussierte
Source-Contract-Test validiert ausschließlich die statische Erhaltung der
Diagnoseaufrufe; er ist keine Host-Runtime-Evidence.

## Nicht ausgeführte Prüfungen mit Begründung

- Es wurde keine Live-HAProxy-Runtime und keine vollständige Connector-Matrix
  für diesen Kandidaten ausgeführt.
- Für einen zukünftigen exakten Draft-Head wurden keine gehosteten GitHub
  Actions oder gehostete SonarQube-Cloud-Analyse beobachtet.
- Es wurde keine Framework- oder MRTS-Quelle, Delivery oder Gitlink-Aktion
  ausgeführt.
- Über das erfolgreiche exact read-only overlay hinaus wurde keine zusätzliche
  Dokumentationsvalidierung ausgeführt. Dieses Overlay initialisierte oder
  veränderte weder Framework, MRTS noch einen Gitlink.

## Bekannte Einschränkungen

- Der ursprüngliche SonarQube-Cloud-Receipt ist an die angegebene
  Basis-Revision gebunden. Eine frische Analyse des zukünftigen Draft-Exact-
  Heads ist nötig, um festzustellen, ob `AZ9cRysjHhV2CayPTP01` extern behoben
  ist.
- Statische Source-Contract-Abdeckung kann keinen Live-HAProxy-Start, keine
  Log-Verfügbarkeit und nicht alle Host-Runtime-Fehlerpfade beweisen.
- Diese enge Parent-only-Änderung kann den globalen SonarQube-Cloud-Issue- oder
  Duplication-Backlog nicht allein schließen.

## Verbleibende Risiken

Die Zentralisierung eines Diagnosebereichs könnte versehentlich eine
Befehlsform verändern, wenn eine Aufrufstelle ausgelassen oder umgeordnet
wird. Der fokussierte Contract-Test mindert dieses Risiko, indem er die
vollständige geordnete Diagnosefolge einschließlich der separaten `1,40p`-
Diagnose prüft. Gehostete Checks können weiterhin Scanner- oder Plattform-
Verhalten zeigen, das lokal nicht beobachtbar ist.

## Finaler Diff- und Review-Status

Zum Zeitpunkt der Record-Erstellung sind der begrenzte Parent-Source-/Test-
Kandidat und dieses bilinguale Dokumentationspaar lokale Worktree-Änderungen.
Der fokussierte Security-Review, die statischen HTX-Kontrollen, die direkte
Overlay-Ausführung mit 9 Tests und das korrigierte vollständige read-only
Dokumentationsoverlay bestanden. Delivery, gehostete Checks und SonarQube-
Cloud-Abschluss stehen weiterhin aus. Der Record beansprucht keinen Pull-
Request-Head, Merge, `master` oder globalen Qualitätsstatus.
