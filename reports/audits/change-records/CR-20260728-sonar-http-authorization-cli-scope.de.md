# Change Record: Parent-HTTP-Authorization-CLI-Zählerbereich für SonarQube Cloud c:S5955

**Sprache:** [English](CR-20260728-sonar-http-authorization-cli-scope.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260728-sonar-http-authorization-cli-scope |
| Datum (UTC) | 2026-07-28 |
| Basis-Revision | 8e8acb8dab1cd03723de269cab7da7dd62e5e010 |
| Grenze | Parent `common/runtime/http_authorization_service.c`, dieses englische/deutsche Change-Record-Paar und die Change-Record-Indizes. Framework, MRTS, beide Gitlinks, Workflows, Scanner-Policy, generierte Reports und Connector-Verhalten bleiben unverändert. |
| Finding-Verknüpfung | SonarQube-Cloud-Code-Smell `AZ9MwjL6-bUaKQ_zSGBL`, Regel `c:S5955`, bei `parse_cli` Zeile 110. |

## Motivation und Problemstellung

Der gemeinsame CLI-Parser des HTTP-Authorization-Service deklarierte seinen
Schleifenzähler außerhalb der einzigen Schleife, die ihn verwendet. SonarQube
Cloud meldet dies als `c:S5955`. Der Parser wird von Parent-
Authorization-Service-Wrappern gemeinsam verwendet; daher muss die Änderung
Argumentverbrauch, Timeout-Grenzdurchsetzung und Rejection ungültiger Eingaben
exakt erhalten.

## Akzeptanzkriterien

- Der Zähler wird nur im C17-`for`-Initializer deklariert.
- CLI-Grammatik, `argv[++index]`-Verbrauch, Parsing-Reihenfolge, Rückgabepfade
  und `AUTH_CONNECTION_TIMEOUT_*`-Grenzen bleiben unverändert.
- Der Timeout-/Ungültigeingaben-Smoke besteht mit beiden verfügbaren C17-
  Compilern unter `-std=c17 -Wall -Wextra -Werror` und task-eigenen externen
  Outputs.
- Fokussierte Parent-Source-Contract- und Whitespace-Validierung bestehen.
- Es werden weder gehostete Closure noch Ready-for-review, Merge,
  Master-Update, Framework-/MRTS-Änderung, Gitlink-Update oder
  Scanner-Policy-Änderung behauptet.

## Implementierungsentscheidung und Begründung

Die einzige Source-Änderung entfernt die eigenständige Deklaration `int index;`
und verwendet `for (int index = 1; index < argc; ++index)`. C17 unterstützt
die schleifenlokale Deklaration. Der Zähler wird nach der Schleife nicht
verwendet; deshalb bleiben Initialisierung, Bedingung, Inkremente und alle
indizierten Zugriffe identisch.

Weder Helper noch Parser-Refactor, Kommandozeilenoption, Timeout-Default,
Timeout-Maximum, Allokation, Socket-Operation oder Authorization-Entscheidung
ändern sich.

## Security-Auswirkung

Dies ist eine verhaltensbewahrende Maintainability-Korrektur neben einem
Authorization-Service-Parser und kein validierter Security-Befund. Unverändert
bleibende legitime Controls sind der geordnete `argv[++index]`-Werteverbrauch,
die Rejection ungültiger Zahlen, die Zero-Timeout-Rejection und die
konfigurierte maximale Timeout-Grenze. Die fokussierte Review fand keinen
geänderten Authentication-, Authorization-, Request-, Netzwerk-, Dateisystem-
oder Command-Execution-Pfad.

## Geänderte Dateien

- `common/runtime/http_authorization_service.c`
- `reports/audits/change-records/README.md` und `README.de.md`
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

| Befehl oder Kontrolle | Tatsächliches Ergebnis |
| --- | --- |
| `make check-http-authorization-service-timeout` mit GCC, explizitem task-eigenem `TMPDIR`, `VERIFIED_RUN_ROOT`, `VERIFIED_BUILD_ROOT` und `BUILD_ROOT` | bestanden; der Smoke kompilierte die geänderte Translation Unit mit `-std=c17 -Wall -Wextra -Werror` und übte blockierte Requests, Drip-Header und Zero-Timeout-Rejection aus. |
| `make check-http-authorization-service-timeout` mit `CC=clang`, denselben expliziten C17-Flags und isolierten Roots | bestanden. |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_sonar_reliability_contract` | bestanden, 10 Tests. |
| `git diff --check` | bestanden; keine Ausgabe. |

## Runtime-Evidence

Der Timeout-Smoke ist ein fokussierter lokaler Service-Control-Test. Er ist
keine Host-Connector-Runtime-Evidence, startet weder Traefik noch Envoy und
behauptet nichts über eine vollständige Deployment-Umgebung.

## Nicht ausgeführte Prüfungen mit Begründung

- Exact-PR-Head-GitHub-Checks und SonarQube-Cloud-Analyse stehen bis zum
  normalen task-eigenen Draft-PR-Zyklus aus.
- Vollständige Connector-Matrizen und Host-Runtime-Suites sind für diese
  lexikalische Parserbereichsänderung nicht anwendbar und wurden nicht als
  Ersatz für den fokussierten Authorization-Service-Control verwendet.

## Bekannte Einschränkungen

SonarQube Cloud ist die Autorität für die Entfernung von
`AZ9MwjL6-bUaKQ_zSGBL`; lokale C17-Kompilierung kann die gehostete
Regeldisposition nicht beweisen. Der projektweite Backlog aus 652 Issues und
Duplikatzeilen liegt außerhalb dieses einzelnen Befunds.

## Verbleibende Risiken

Die Korrektur lässt das vorhandene Parser-Design absichtlich unverändert. Jede
künftige funktionale CLI-Änderung muss Argumentreihenfolge, Timeout-Policy und
Authorization-Service-Wrapper-Verhalten separat neu bewerten.

## Finaler Diff- und Review-Status

Die Source-Korrektur wurde als `8fa2f2cf8e8c6130ee1530f97008284c63bf298b`
committet und auf ihren Task-Branch gepusht, bevor diese erforderliche
Dokumentationsänderung erfolgte. Der geprüfte Source-Diff ist auf die
Schleifenzählerbereichs-Korrektur begrenzt. Dieser Record und seine
Index-Einträge sind die ausstehende Dokumentationsänderung; es werden noch
kein Pull Request, kein gehostetes Ergebnis, keine Review, kein
Ready-for-review-Übergang und kein Merge behauptet.
