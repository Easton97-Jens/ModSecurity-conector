# Change Record: Parent-HTTP-Authorization-CLI-Schleifensteuerung für SonarQube Cloud c:S5955, c:S886 und c:S3776

**Sprache:** [English](CR-20260728-sonar-http-authorization-cli-scope.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260728-sonar-http-authorization-cli-scope |
| Datum (UTC) | 2026-07-28 |
| Basis-Revision | 8e8acb8dab1cd03723de269cab7da7dd62e5e010 |
| Grenze | Parent `common/runtime/http_authorization_service.c`, dieses englische/deutsche Change-Record-Paar und die Change-Record-Indizes. Framework, MRTS, beide Gitlinks, Workflows, Scanner-Policy, generierte Reports und Connector-Verhalten bleiben unverändert. |
| Finding-Verknüpfung | SonarQube-Cloud-Code-Smells `AZ9MwjL6-bUaKQ_zSGBL` (`c:S5955`), `AZ-orCBNFp8FN2qblodn` (`c:S886`) und Exact-PR-Head `AZ-ovroGM5o_ow3fPM0Z` (`c:S3776`) bei `parse_cli`. |

## Motivation und Problemstellung

Der gemeinsame CLI-Parser des HTTP-Authorization-Service deklarierte seinen
Schleifenzähler außerhalb der einzigen Schleife, die ihn verwendet. SonarQube
Cloud meldet dies als `c:S5955`. Die initiale schleifenlokale Korrektur legte
daraufhin `c:S886` in demselben berührten Parser offen, weil direkte
`argv[++index]`-Ausdrücke den `for`-Zähler auch im Schleifenrumpf änderten. Das
Explizitmachen des zweigliedrigen Skips bereinigte die Zählerwarnung, erhöhte
aber die kognitive Komplexität von `parse_cli` von 25 auf 29. SonarQube Cloud
meldet dies als `c:S3776`, obwohl das Quality Gate `OK` ist. Der Parser wird
von Parent-Authorization-Service-Wrappern gemeinsam verwendet; daher muss die
Folgekorrektur Argumentverbrauch, Timeout-Grenzdurchsetzung und Rejection
ungültiger Eingaben exakt erhalten und zugleich Schleifensteuerung sowie
Funktionskomplexität innerhalb der Analyzer-Erwartung halten.

## Akzeptanzkriterien

- Der Zähler wird nur im C17-`for`-Initializer deklariert und nur durch dessen
  Update-Ausdruck geändert.
- CLI-Grammatik, Parsing-Reihenfolge, Rückgabepfade, Werteverbrauch und
  `AUTH_CONNECTION_TIMEOUT_*`-Grenzen bleiben unverändert.
- Fehlende Werte nach `--config`, `--listen`, `--max-requests` und
  `--connection-timeout-ms` werden mit dem vorhandenen CLI-Fehlerstatus
  abgelehnt.
- Unbekannte Optionen und nichtnumerische `--max-requests`-Werte behalten
  ihren vorhandenen CLI-Fehlerstatus.
- Die Dispatch-Logik der werttragenden Optionen ist so ausgelagert, dass
  `parse_cli` das SonarQube-Cloud-Limit für kognitive Komplexität nicht mehr
  überschreitet.
- Der Timeout-/Ungültigeingaben-Smoke besteht mit beiden verfügbaren C17-
  Compilern unter `-std=c17 -Wall -Wextra -Werror` und task-eigenen externen
  Outputs.
- Fokussierte Parent-Source-Contract- und Whitespace-Validierung bestehen.
- Es werden weder gehostete Closure noch Ready-for-review, Merge,
  Master-Update, Framework-/MRTS-Änderung, Gitlink-Update oder
  Scanner-Policy-Änderung behauptet.

## Implementierungsentscheidung und Begründung

Die schleifenlokale C17-Deklaration bleibt erhalten. Ein explizites Flag
`skip_option_value` erhält das vorhandene Verhalten zweigliedriger Optionen:
Die Optionsiteration liest `argv[index + 1]`, validiert ihn bei Bedarf und
markiert die folgende Iteration als bereits konsumierten Wert. Die nächste
Iteration löscht das Flag und fährt fort, während `++index` ausschließlich im
`for`-Kopf bleibt.

`parse_cli_value_option` enthält ausschließlich die vier vorhandenen
werttragenden Optionsfälle und deren bestehende Numeric-/Timeout-Prädikate.
Damit entfallen die wiederholten Branches aus `parse_cli`; es entsteht weder
eine neue Option noch eine Akzeptanz fehlender Werte oder ein anderer Fehler
beim ersten ungültigen Argument.

Dies ersetzt weder Parser-Grammatik, Kommandozeilenoption, Timeout-Default,
Timeout-Maximum, Allokation, Socket-Operation noch Authorization-Entscheidung.
Es macht den vorhandenen Skip explizit, statt den Schleifenzähler durch einen
Ausdruck im Branch-Rumpf zu verändern.

## Security-Auswirkung

Dies ist eine verhaltensbewahrende Maintainability-Korrektur neben einem
Authorization-Service-Parser und kein validierter Security-Befund. Unverändert
bleibende legitime Controls sind geordneter Optionswerteverbrauch, die
Rejection ungültiger Zahlen und fehlender Werte, die Zero-Timeout-Rejection und
die konfigurierte maximale Timeout-Grenze. Die fokussierte Review fand keinen
geänderten Authentication-, Authorization-, Request-, Netzwerk-, Dateisystem-
oder Command-Execution-Pfad.

## Geänderte Dateien

- `common/runtime/http_authorization_service.c`
- `ci/checks/common/http_authorization_service_timeout_smoke.c`
- `reports/audits/change-records/README.md` und `README.de.md`
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

| Befehl oder Kontrolle | Tatsächliches Ergebnis |
| --- | --- |
| `make check-http-authorization-service-timeout` mit GCC, explizitem task-eigenem `TMPDIR`, `VERIFIED_RUN_ROOT`, `VERIFIED_BUILD_ROOT` und `BUILD_ROOT` | bestanden; der Smoke kompilierte die geänderte Translation Unit mit `-std=c17 -Wall -Wextra -Werror` und übte blockierte Requests, Drip-Header, Zero-Timeout-Rejection, alle vier Rejections fehlender Optionswerte, Unknown-Option-Rejection und nichtnumerische Max-Request-Rejection aus. |
| `make check-http-authorization-service-timeout` mit `CC=clang`, denselben expliziten C17-Flags und isolierten Roots | bestanden mit denselben gültigen und ungültigen CLI-Controls. |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_sonar_reliability_contract` | bestanden, 10 Tests. |
| Task-eigenes externes Overlay aus dem exakten Parent-Kandidaten und dem read-only Parent-gebundenen Framework-Archiv `47e50e7bc43ba7a3b5bad1a9448111794f664cc0`: `check-bilingual-docs.py`, `check-repository-path-references.py` und Framework-`check-doc-links.py` | bestanden: `bilingual docs ok`, `repository path references: PASS` und `doc links ok`. |
| `git diff --check` | bestanden; keine Ausgabe. |

## Runtime-Evidence

Der Timeout-Smoke ist ein fokussierter lokaler Service-Control-Test. Er ist
keine Host-Connector-Runtime-Evidence, startet weder Traefik noch Envoy und
behauptet nichts über eine vollständige Deployment-Umgebung.

## Nicht ausgeführte Prüfungen mit Begründung

- Frische Exact-PR-Head-GitHub-Checks und SonarQube-Cloud-Analyse stehen bis
  zum normalen task-eigenen Draft-PR-Folgezyklus aus.
- Vollständige Connector-Matrizen und Host-Runtime-Suites sind für diese
  lexikalische Parserbereichsänderung nicht anwendbar und wurden nicht als
  Ersatz für den fokussierten Authorization-Service-Control verwendet.

## Bekannte Einschränkungen

SonarQube Cloud ist die Autorität für die Entfernung von
`AZ9MwjL6-bUaKQ_zSGBL`, `AZ-orCBNFp8FN2qblodn` und
`AZ-ovroGM5o_ow3fPM0Z`; lokale C17-Kompilierung kann die gehostete
Regeldisposition nicht beweisen. Der projektweite Backlog aus 652 Issues und
Duplikatzeilen liegt außerhalb dieser einzelnen parserfokussierten Korrektur.

## Verbleibende Risiken

Die Korrektur lässt das öffentliche CLI-Design absichtlich unverändert. Jede
künftige funktionale CLI-Änderung muss Argumentreihenfolge, Timeout-Policy und
Authorization-Service-Wrapper-Verhalten separat neu bewerten.

## Finaler Diff- und Review-Status

Die initiale Bereichskorrektur wurde als
`8fa2f2cf8e8c6130ee1530f97008284c63bf298b` committet. Der exakte PR-Head
`ea52192f30ca091f9389eb10c87e9a99e2bbab4c` hatte danach ein erfolgreiches
Quality Gate und null neue Duplikatzeilen, aber einen OPEN-`c:S3776`-Receipt.
Diese Folgeänderung ergänzt nur den Value-Option-Helper, der zur Senkung der
Funktionskomplexität nötig ist; der geprüfte Kandidat bleibt ein Draft-PR.
Nach dem normalen Folge-Push ist frische issue-freie Exact-Head-Hosted-Evidence
erforderlich. Kein Ready-for-review-Übergang und kein Merge werden behauptet.
