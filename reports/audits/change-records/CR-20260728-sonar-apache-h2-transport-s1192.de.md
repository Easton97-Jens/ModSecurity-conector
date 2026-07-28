# Change Record: Parent-Apache-H2-Transport-Result-Literal-Ownership für SonarQube Cloud S1192

**Sprache:** [English](CR-20260728-sonar-apache-h2-transport-s1192.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260728-sonar-apache-h2-transport-s1192 |
| Datum (UTC) | 2026-07-28 |
| Basis-Revision | 8e8acb8dab1cd03723de269cab7da7dd62e5e010 |
| Kandidatenbezeichnung | Parent-#155-Kandidat. Diese lokale Bezeichnung behauptet keinen gehosteten PR, Remote-Head, Review, Quality Gate oder Delivery-Ergebnis. |
| Tracking | `AZ98JczJLJyjbmyNA5LW`, `AZ98JczJLJyjbmyNA5LO`, `AZ98JczJLJyjbmyNA5LS` und `AZ98JczJLJyjbmyNA5LU`; alle sind vor diesem Kandidaten Live-Parent-`shelldre:S1192`-Findings. |
| Grenze | Parent-Apache-Phase-4-H2-Smoke-Harness, dieses englisch/deutsche Change-Record-Paar und seine zwei Indizes. Framework, MRTS, Gitlinks, Workflows, Reports, Scanner-Policy und gehosteter Status bleiben unverändert. |

## Motivation und Problemstellung

Fünf Apache-H2-Smoke-Pfade wiederholen denselben Curl-Feature-Ausdruck, die
Status-/Versions-Write-out-Grammatik und die Awk-Programme für den ersten
Datensatz. SonarQube Cloud meldet die vier wiederholten Literale als
S1192-Maintainability-Findings. Der Code liegt an einer fail-closed Phase-4-
Transport-Grenze; Literal-Ownership darf deshalb weder ändern, ob ein Curl ohne
H2-Fähigkeit einen Fall blockiert, noch was Curl schreibt oder wie der erste
Transportdatensatz geparst wird.

## Akzeptanzkriterien

- Jedes ausgewählte Literal erhält genau einen unveränderlichen file-local
  Owner und wird nur an den fünf bestehenden H2-Stellen verwendet.
- Alle H2-Support-Checks behalten das Verhalten `grep -E ... || blocked`.
- Curl behält sein exaktes Status-/Versions-Write-out-Argument,
  Argumentreihenfolge, Output-Sink und dieselbe Ein-URL-Zwei-Felder-
  Datensatzgrammatik.
- Die zwei Awk-Programme wählen weiterhin nur Feld eins beziehungsweise zwei
  des ersten tabulatorgetrennten Datensatzes.
- Shell-Syntax, fokussiertes Apache-Phase-4-Wiring, Whitespace, bilinguale
  Dokumentation und Exact-Head-Hosted-Evidence müssen wahrheitsgemäß erfasst
  werden.

## Implementierungsentscheidung und Begründung

Der Harness deklariert nun vier POSIX-`readonly`-Werte nahe seiner anderen
file-local Konfiguration:

- `CURL_HTTP2_FEATURE_PATTERN`
- `CURL_HTTP_STATUS_VERSION_FORMAT`
- `AWK_FIRST_TAB_RECORD_STATUS`
- `AWK_FIRST_TAB_RECORD_VERSION`

Sie werden aus den exakten früheren single-quoted Literalen initialisiert und
nur über double-quoted Expansions verwendet. Das erhält genau ein Shell-
Argument für jeden Grep-, Curl- oder Awk-Aufruf und verhindert Word-Splitting,
Globbing oder Shell-Interpretation der eingebetteten Awk-Feldreferenzen. Die
getrennte Multi-URL-Transfer-Grammatik an anderer Stelle des Harness wird
bewusst nicht mit diesem Zwei-Felder-H2-Result-Contract zusammengeführt.

## Geänderte Dateien

- `connectors/apache/harness/run_apache_smoke.sh`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- `reports/audits/change-records/CR-20260728-sonar-apache-h2-transport-s1192.md`
- `reports/audits/change-records/CR-20260728-sonar-apache-h2-transport-s1192.de.md`

## Ausgeführte Befehle

| Befehl oder Kontrolle | Tatsächliches Ergebnis |
| --- | --- |
| `sh -n connectors/apache/harness/run_apache_smoke.sh` im exakten Task-Worktree | bestanden. |
| `/root/git/ModSecurity-conector/.venv/bin/python -B tests/test_apache_phase4_response_regression_wiring.py` mit deaktiviertem Bytecode/User-Site im exakten Task-Worktree | bestanden: 10/10 Tests. |
| `git diff --check` | bestanden; kein Whitespace-Fehler. |
| Fokussierte Shell-/Protocol-Sicherheitsreview | genehmigt; kein plausibles oder validiertes Finding. |

## Security-Auswirkung

Der Kandidat betrifft Shell-Argumente für HTTP/2-Fähigkeitserkennung,
Curl-Transport-Result-Output und Awk-Parsing. Das geprüfte Invariant ist, dass
H2-only-Fälle blockiert bleiben, sofern Curl keine H2-Unterstützung zeigt, und
dass Response-Privacy-Checks denselben Status-/Versions-Datensatz konsumieren,
ohne Response-Bodies, Header, Trace-Daten oder Stderr in einen Shell-
ausgewerteten Kontext zu verschieben.

Die Werte sind feste Source-Literale, werden vor jeder Verwendung deklariert
und stets double quoted expandiert. Die Review stellt fest, dass POSIX-
`readonly`-Syntax, Curl-Argumentreihenfolge, Write-out-Bytes,
First-Record-Parsing und bestehende Output-Sinks unverändert bleiben. Kein
kontrollierter Request, Response, Environment-Wert oder Command-Substitution
wird zu einer Grep-RegEx oder einem Awk-Programm. Diese fokussierte Review
identifizierte kein Security-Finding.

## Runtime-Evidence

Es wurde keine Apache-Host-Runtime, Connector-Matrix-, Framework- oder MRTS-
Runtime gestartet. Shell-Syntax und der fokussierte Source-Wiring-Test sind
nur lokale Contract-Evidence; sie belegen weder Deployment-Kompatibilität noch
eine promotete Runtime-Capability.

## Bekannte Einschränkungen

Dieser Record besitzt keine gehostete Exact-Head-PR-, SonarQube-Cloud-
Post-Change-Issue-, Quality-Gate-, Workflow-, Review-, Merge- oder
Default-Branch-Evidence. Er behauptet kein vollständiges Apache-H2-
Runtime-Ergebnis. Die vorbestehende Pipeline-Status-Eigenschaft von
`curl --version | grep` wurde geprüft, bleibt aber unverändert und es wurde
kein konkreter neuer Fail-open-Pfad gezeigt.

## Verbleibende Risiken

Eine spätere Harness-Änderung könnte ein neues hard-codiertes äquivalentes
Literal einführen, eine Curl-Record-Grammatik ändern oder einen H2-Gate
außerhalb dieses Scopes verändern. Feste Literal-Owner, direktes Wiring,
Shell-Syntax und die fokussierte Review mindern dieses Risiko. Eine frische
Exact-Head-Hosted-Analyse bleibt erforderlich, bevor die vier zitierten
Receipts als erledigt behandelt werden.

## Nicht ausgeführte Prüfungen mit Begründung

- Kein Apache-Host-Build, Real-H2-Smoke-Runtime, Full-Matrix, Report-
  Generierung, Workflow-Ausführung, Framework-Source-Check oder MRTS-Check
  wurde ausgeführt; jeder liegt außerhalb dieser Parent-only-Literal-
  Extraktion.
- Repositoryweite Dokumentationschecks und gehostete PR-/Sonar-Evidence sind
  für diesen Kandidaten noch nicht verfügbar. Ein späteres disposable
  Parent-/Framework-Dokumentationsoverlay und ein Exact-Head-Hosted-Zyklus
  sind erforderlich, bevor die Delivery als verifiziert gilt.

## Finaler Diff- und Review-Status

Der lokale Kandidat ändert nur die vier Literal-Owner und ihre zwanzig H2-
Call-Sites sowie dieses gepaarte Traceability-Update und seine Indizes. Die
oben genannten Syntax-/Test-/Whitespace-/Security-Evidence bestehen. Es werden
weder Commit, Push, PR, gehosteter Check, Quality Gate, Review, Merge,
Master-Änderung, Framework-/MRTS-Änderung, Gitlink-Update, Workflow-Änderung
noch Scanner-Policy-Aktion behauptet.
