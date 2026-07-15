# Change Record: Optionalen Apache-Voraussetzungsstatus in CI bewahren

**Sprache:** [English](CR-20260714-optional-apache-prerequisite-ci.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Titel | Optionalen Apache-Voraussetzungsstatus in CI bewahren |
| Change-ID | CR-20260714-optional-apache-prerequisite-ci |
| Datum (UTC) | 2026-07-14T15:36:31Z |
| Autor oder ausführender Agent | Codex |
| Basis-Revision | `be0356af96ef582c3a7dbc0169c7c8b27b7b6b34` |
| Zugehöriges Issue oder Pull Request | [PR #43](https://github.com/Easton97-Jens/ModSecurity-conector/pull/43); PR #42 wird unabhängig geprüft und erst nach grüner Master-CI von PR #43 integriert. |
| Finale Revision | Geprüfter Implementierungskopf `cd4a1def258a1705dda6f3253334dadc564d60c0`; vor der Lieferung ist ein Evidence-Abgleich-Follow-up erforderlich. Die unveränderlichen finalen Branch- und Merge-Revisionen mit exakten-SHA-CI-Ergebnissen werden in PR #43 festgehalten. |

## Motivation und Problemstellung

Fünf bereits bestehende Push-Workflows schlugen fehl, wenn ihr gemeinsamer
`make lint`-Pfad auf fehlendes `apxs` oder nutzbare Apache-
Entwicklungsheader traf. Der direkte Apache-Cleanup-Harness meldete bewusst
`BLOCKED` mit Exit `77`, aber
`check-apache-request-transaction-cleanup-lint` rief ihn zuerst über ein
rekursives GNU-Make-Target auf. GNU Make meldete seine fehlgeschlagene Recipe
als Exit `2`, sodass der Wrapper, der nur `77` erkannte, nie lief.

Der Fehler liegt vor dem reinen Dokumentationscommit
`2a3788dc20f93bb14f0c2fc784444402c3e3f64b` und PR #42. Dieselben fünf Fehler
traten auf der Basisrevision auf: [lint](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29332329968), [test-common](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29332329953), [test-apache](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29332329928), [test-nginx](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29332329926) und [quick-framework-check](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29332329950). Die entsprechenden fünf Läufe für den Delivery-Smoke-Commit schlugen ebenfalls fehl: [lint](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29342695839), [test-common](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29342695813), [test-apache](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29342695806), [test-nginx](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29342695931) und [quick-framework-check](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29342695753).

## Betroffene Komponenten und Sicherheitsgrenzen

- Nur Parent-CI-Orchestrierung: Root-`Makefile`, Apache-Cleanup-Lint-Target,
  ein kleiner Parent-`ci/tools/`-Statusrunner und Root-Vertragstests.
- Leserorientierte Parent-CI-, Testing-/Evidence-, Variablenreferenz- und
  Change-Record-Dokumentation werden auf Englisch und Deutsch aktualisiert.
- Das Framework bleibt unverändert und sein Gitlink wird nicht geändert. Sein
  `skip_blocked`-Vertrag gibt korrekt `BLOCKED` und Exit `77` aus; der Verlust
  lag ausschließlich an der rekursiven Parent-Make-Grenze.
- Der JSON-Datensatz ist payloadfreie CI-Steuerungs-Evidence unter einem
  externen `BUILD_ROOT`, keine kanonische Runtime-Evidence. Er speichert weder
  Request-Daten, Zugangsdaten noch Build-Ausgaben.

## Akzeptanzkriterien

| Kriterium | Status | Evidence |
| --- | --- | --- |
| Ein direkter optionaler Apache-Voraussetzungsblock bleibt sichtbar und lässt generisches Lint nicht fälschlich fehlschlagen. | lokal erfüllt | `make check-apache-request-transaction-cleanup-lint` zeichnet `blocked` mit direktem Exit `77` und `CHECK_STATUS_REASON apache_development_prerequisite` auf und liefert nur unter diesem exakten Vertrag `0`. |
| Python-Quellprüfungen und echte Native-Check-Fehler bleiben rot. | lokal erfüllt | Das strikte Target bleibt ohne `apxs` nichtnull; synthetische Fehler bei vorhandenem `apxs`, unbekannte Exits und ein unklassifizierter Framework-Block sind Regressionstests. |
| Eine fehlende Pflichtvoraussetzung wird nicht zu Erfolg. | lokal erfüllt | Synthetisches striktes Make-Fixture behält `blocked`-Evidence und ein nichtnull-Ergebnis. |
| Rekursives Make kann die Klassifikation nicht stillschweigend verlieren. | lokal erfüllt | Synthetisches verschachteltes Make-Fixture behält JSON-`blocked`-Evidence, während nur der ausdrücklich erlaubte Wrapper `0` liefert. |
| Andere Common- oder Connector-Checks werden nicht übersprungen. | lokal erfüllt | Separate synthetische `common`- und `connector`-Recipes bleiben nach einem erlaubten optionalen Block nichtnull. |
| Statusmodell und öffentlicher Make-Vertrag sind in beiden Sprachen dokumentiert. | lokal erfüllt | `ci/README.*`, `docs/testing-and-evidence.*` und `docs/reference/variables.*`. |
| Erforderliche exakte-SHA-Push- und Pull-Request-Workflow-Ergebnisse sind festgehalten. | in Bearbeitung | Der geprüfte Implementierungskopf bestand seine vorhandenen Push- und Pull-Request-Workflows; dieser Evidence-Abgleich-Follow-up startet vor der Lieferung absichtlich einen frischen exakte-SHA-Zyklus. |

## Scope- und Workflow-Entscheidung

Die Untersuchung klärte die geforderten Fragen vor der Implementierung:

| Frage | Entscheidung und Repository-Evidence |
| --- | --- |
| Ist `apxs` für jeden betroffenen Workflow optional? | Ja, aber nur für den eingebetteten nativen Apache/APR-Cleanup-Harness. Jeder betroffene Step ist ein generischer Lint-, Struktur- oder Dry-Run-Pfad; keiner ist ein nativer Apache-Build-Job. |
| Welche Jobs dürfen bei fehlendem `apxs` überspringen? | Kein ganzer Job wird übersprungen. Nur der direkte native Cleanup-Harness darf als `blocked` festgehalten und durch `check-apache-request-transaction-cleanup-lint` erlaubt werden, wenn kein nutzbares `apxs` mit `httpd.h` gefunden wird. |
| Welche Jobs müssen bei fehlendem `apxs` fehlschlagen? | Das strikte `make check-apache-request-transaction-cleanup`-Target und tatsächliche native Apache-Build-/Verifikationspfade bleiben nichtnull. Der verpflichtende Python-Quellvertrag bleibt bei Fehler in jedem Pfad nichtnull. |
| Ist der Blocked-Status öffentliches Make-Verhalten? | Ja. Die direkten Skripte und die CI-Dokumentation verwenden `BLOCKED`/Exit `77` für eine deklarierte nicht verfügbare optionale Voraussetzung; die strikten und Lint-Targets dokumentieren jetzt ihre unterschiedlichen Verträge. |
| Ist Exit `77` außerhalb rekursiven Make zuverlässig? | Ja. Der direkte Shell-Harness gibt `77` aus, und benachbarte direkte Lint-Wrapper klassifizieren ihn bereits. Rekursives GNU Make wandelt die fehlgeschlagene Child-Recipe in sein eigenes `2` um. |
| Gab es bereits ein maschinenlesbares Evidence-Format für diesen Check? | Kein eigener Datensatz bestand. Das Repository hatte menschenlesbare `BLOCKED`-Ausgabe und breitere Evidence-Formate, daher fügt diese Änderung einen fokussierten payloadfreien JSON-Statusdatensatz plus `CHECK_STATUS`-JSON-Ausgabe hinzu. |

| Workflow | Job und Push-Step | Make-Target-Kette | Apache-Voraussetzungsdisposition |
| --- | --- | --- | --- |
| `lint` | `scaffold-lint` / `Run lightweight lint` | `make lint` → `check-apache-request-transaction-cleanup-lint` | Nur der Preflight ohne nutzbares `apxs`/`httpd.h` ist optional; Python-Quellvertrag verpflichtend. |
| `test-common` | `common-structure` / `Lightweight framework checks` | `make quick-check` → `lint` → Cleanup-Lint-Target | Nur dieser Apache-Preflight ist optional; Common-Checks bleiben verpflichtend. |
| `test-apache` | `apache-structure` / `Syntax and dry-run checks` | `make quick-check` → `lint` → Cleanup-Lint-Target | Dies ist kein nativer Build; nur dieser Preflight ist optional und der Quellvertrag verpflichtend. |
| `test-nginx` | `nginx-structure` / `Syntax and dry-run checks` | `make quick-check` → `lint` → Cleanup-Lint-Target | Nur dieser Apache-Preflight ist optional; NGINX-Checks bleiben verpflichtend. |
| `quick-framework-check` | `quick-check` / `Lightweight connector/framework checks` | `make quick-check` → `lint` → Cleanup-Lint-Target | Nur dieser Apache-Preflight ist optional; alle übrigen Quick-Checks bleiben verpflichtend. |

Der direkte Harness gibt seinen fehlende-Voraussetzungs-Status über
`ci/checks/connectors/apache/check-apache-request-transaction-cleanup.sh` und
das Framework-`skip_blocked` aus. Das alte Parent-Lint-Target überschritt dann
die rekursive Make-Grenze, bevor es ihn zu prüfen versuchte, wodurch in jeder
obigen Kette der falsche Exit `2` entstand.

## Untersuchte Alternativen

- Den alten rekursiven Wrapper zu bewahren wurde verworfen, weil GNU Make das
  `77` des Child-Prozesses nicht als Exitcode des rekursiven Make-Prozesses
  erhält.
- Ein breites Workflow-`continue-on-error`, `|| true` oder ein Job-Level-Skip
  wurde verworfen, weil es echte Source-, Konfigurations-, Common- oder
  Connector-Fehler verdecken könnte.
- Apache-Entwicklungspakete zu installieren wurde verworfen, weil dies einen
  CI-Klassifikationsfehler maskieren und die Umgebung statt des dokumentierten
  Vertrags verändern würde.
- Eine Framework-Änderung wurde verworfen, weil dessen `skip_blocked`-
  Implementierung korrekt ist und der validierte Fehler nur im Parent liegt.

## Implementierungsentscheidung und Begründung

`ci/tools/run-check-status.py` führt den nativen Harness direkt aus, ordnet
direkten Exit `0` `passed`, direkten `77` `blocked` und jeden anderen Exit
`failed` zu und schreibt dann einen JSON-Datensatz, bevor er zu Make
zurückkehrt. Er definiert auch explizite `not_applicable`- und
`not_executed`-Dispositionen. Ein blockierter Befehl liefert nur dann Erfolg,
wenn seine direkte Ausgabe exakt den vom Aufrufer erlaubten
`CHECK_STATUS_REASON`-Marker hat; `not_applicable` benötigt ebenfalls eine
explizite Allow-Option des Aufrufers, und `not_executed` ist nie implizit
erfolgreich.

Der Runner akzeptiert keinen vom Aufrufer gewählten Statusdateipfad. Er leitet
den festen Dateinamen im Stil von
`apache-request-transaction-cleanup.json` aus der validierten Check-Kennung
unter dem externen Verzeichnis `BUILD_ROOT/check-status` ab. Er weist einen
fehlenden, relativen, nichtkanonischen, Checkout-lokalen oder symbolisch
verlinkten Ausgabeort zurück, öffnet das validierte Verzeichnis vor dem Child
und verwendet diesen verankerten Verzeichnis-Handle für eine exklusiv erzeugte
temporäre Datei und das finale Ersetzen.

`ci/checks/connectors/apache/check-apache-request-transaction-cleanup.sh`
ermittelt `apxs` jetzt über `framework_find_apxs`, das nutzbares `httpd.h`
verifiziert, und gibt `CHECK_STATUS_REASON apache_development_prerequisite`
nur aus, wenn diese Suche scheitert. Das Lint-Target führt weiterhin die
verpflichtenden Python-Quellvertragstests aus und ruft dann den direkten
Statusrunner mit `--allow-blocked-reason apache_development_prerequisite` auf.
Fehlende Framework-, Compiler-, APR- oder libmodsecurity-Voraussetzungen geben
keinen erlaubten Marker aus und bleiben nichtnull. Das strikte Target wird nicht
verändert. Die Statusdatei liegt für diese Prüfung fest unter
`$(BUILD_ROOT)/check-status/apache-request-transaction-cleanup.json` und muss
außerhalb des Checkouts bleiben. `CHECK_STATUS` gibt dasselbe JSON in lokalen
und GitHub-Actions-Logs aus, damit Reviewer `blocked` von `passed`
unterscheiden können, auch wenn das Aggregation-Target erfolgreich endet.

Die dokumentierten Statuswerte sind `passed`, `failed`, `blocked`,
`not_applicable` und `not_executed`. Ein erfolgreicher generischer Workflow
darf nur eine konkret erlaubte `blocked`- oder `not_applicable`-Subprüfung
tragen; er etikettiert diese Subprüfung nicht als passed um.

## Geänderte Dateien

- `Makefile`
- `ci/tools/run-check-status.py`
- `ci/checks/connectors/apache/check-apache-request-transaction-cleanup.sh`
- `tests/test_optional_prerequisite_status.py`
- `ci/README.md` und `ci/README.de.md`
- `docs/testing-and-evidence.md` und `docs/testing-and-evidence.de.md`
- `docs/reference/variables.md` und `docs/reference/variables.de.md`
- Dieses Change-Record-Paar und seine zweisprachigen Indexeinträge

Keine Framework-Datei, kein Framework-Commit, kein Submodule-Gitlink, kein
Workflow-Trigger und keine Datei von PR #42 wird geändert.

## Hinzugefügte oder geänderte Tests

`tests/test_optional_prerequisite_status.py` verwendet synthetische
`PATH`-Fixtures und temporäre direkte Befehle für:

1. vorhandenes `apxs` und bestandene abhängige Prüfung;
2. vorhandenes `apxs` und fehlgeschlagene abhängige Prüfung;
3. fehlendes optionales `apxs`, das als erlaubtes `blocked` klassifiziert wird;
4. fehlendes verpflichtendes `apxs`, das durch Make nichtnull bleibt;
5. einen rekursiven Make-Aufruf mit erhaltener persistierter `blocked`-Klassifikation;
6. einen unbekannten Exitcode, der `failed` bleibt;
7. einen nicht erlaubten `framework_unavailable`-Marker, der nichtnull bleibt;
8. nachfolgende Common- und Connector-Checks, die jeweils nichtnull bleiben; und
9. explizites `not_applicable`- und `not_executed`-Dispositionsverhalten; und
10. die Zurückweisung fehlender, Checkout-lokaler, nichtkanonischer,
    historischer Schnittstellen für willkürliche Pfade und symbolisch
    verlinkter Statusausgabeanfragen bei unverändertem Ziel; und
11. einen vom Child verursachten Austausch von `BUILD_ROOT` nach der
    Vorbereitung, der die bereits verankerte Statusausgabe nicht umleiten darf.

Er ruft außerdem den echten Lint-Target mit einem ausführbaren synthetischen
`apxs` auf, dessen Include-Verzeichnis kein `httpd.h` enthält. Dies bestätigt,
dass der direkte Preflight den einzigen erlaubten Marker ausgibt und sein
erlaubtes `blocked`-Ergebnis persistiert. Ein separater echter Target-Fall mit
fehlendem Framework-Root bleibt nichtnull mit einem unklassifizierten
`blocked`-Datensatz.

## Ausgeführte Befehle

| Exakter Befehl | Exitcode oder Ergebnis | Bereinigte relevante Zusammenfassung | Kanonischer Evidence-Pfad | Run-ID |
| --- | --- | --- | --- | --- |
| `make check-apache-request-transaction-cleanup-lint` auf dem Basiscode vor dem Fix | `2` | Fünf Python-Quelltests bestanden; nativer Harness gab `77` aus; rekursives Make meldete `2`. | None | None |
| `make check-optional-prerequisite-status` | `0` | Sechzehn fokussierte Statusvertrags-Regressionstests einschließlich Statuspfad-Grenz- und Child-Pfadaustausch-Regressionen bestanden. | None | None |
| `make check-apache-request-transaction-cleanup-lint` nach dem Fix | `0` | Fünf Python-Quelltests bestanden; fehlendes `apxs` schrieb `blocked`, direkten Exit `77` und erlaubten Workflow-Exit `0`. | `$(BUILD_ROOT)/check-status/apache-request-transaction-cleanup.json` | None |
| `make check-apache-request-transaction-cleanup` nach dem Fix | erwartete Negativkontrolle `2` | Fünf Python-Quelltests bestanden; fehlendes `apxs` blieb `BLOCKED` und nichtnull. | None | None |
| `make lint` | `failed` (Exit `2`, nur lokal) | Der unveränderte Apache-C17-Preflight versuchte lokale Runtime-Provisionierung und stoppte bei `missing_local_httpd_build`, bevor das geänderte Cleanup-Target lief. | None | None |
| `CI=true make lint` | `0` | Der lokale CI-Modus nahm denselben Pfad für fehlende Voraussetzungen wie GitHub Actions: Der bestehende C17-Check wurde sichtbar übersprungen und der geänderte Cleanup-Check gab seinen erlaubten `blocked`-Datensatz aus. | None | None |
| `make quick-check` | `failed` (Exit `2`, nur lokal) | Er erbt denselben unveränderten lokalen Apache-C17-Provisionierungsfehler aus `lint`, bevor das geänderte Cleanup-Target läuft. | None | None |
| `CI=true make quick-check` | `0` | Der CI-Modus-Quick-Check bestand; dies ist lokaler Vertragsnachweis, kein Ersatz für GitHub Actions der exakten SHA. | None | None |
| `make check-bilingual-docs` | `0` | Zweisprachige Dokumentationsprüfung bestand. | None | None |
| `make check-doc-links` | `0` | Repository-Pfadreferenz- und Dokumentationslinkprüfungen bestanden. | None | None |
| `make check-variable-documentation` | `0` | Variablendokumentationsprüfung bestand. | None | None |
| `make -n test-common`, `make -n test-apache`, `make -n test-nginx`, `make -n quick-framework-check` | `not_applicable` | Das Root-Makefile definiert keine Targets mit diesen Workflow-Namen; ihre echten Ketten stehen oben. | None | None |
| `make -n check-repository-path-references` | `not_applicable` | Kein Standalone-Target besteht; `make check-doc-links` rief die tatsächliche Repository-Pfadreferenzprüfung auf. | None | None |
| `git diff --check` | `0` | Keine Whitespace-Fehler zum dokumentierten lokalen Review-Zeitpunkt. | None | None |

## Security-Auswirkung

Kein Produktsicherheitsverhalten, keine Host-Aktion, Authentifizierung,
Autorisierung oder Runtime-Datengrenze ändert sich. Der Runner ist für jeden
unbekannten Nichtnull-Command-Exit und jedes `77` ohne den exakten erlaubten
Marker seines Aufrufers fail-closed. Sein Statusziel hat keine Schnittstelle
für willkürliche Pfade: Eine validierte Kennung wählt einen festen Dateinamen
unter einem kanonischen externen Build-Root, während Checkout-lokale,
nichtkanonische und symbolisch verlinkte Roots oder Ziele zurückgewiesen werden.
Der Runner verankert das verifizierte Verzeichnis vor dem Ausführen des Child,
sodass ein Child die temporäre Erstellung oder das finale Ersetzen durch einen
Austausch des Build-Root-Pfads nicht umleiten kann. Er persistiert nur eine
feste Check-Kennung, Status, Command- und Workflow-Exitcodes sowie bei Bedarf
einen nicht sensitiven Dispositionsgrund.

## Dokumentationsänderungen

- `ci/README.*` definiert den Statusrunner, seinen JSON-Statusvertrag und das
  strikte-gegenüber-Lint-Make-Verhalten.
- `docs/testing-and-evidence.*` ergänzt `NOT APPLICABLE` und trennt die
  kleingeschriebenen CI-Steuerungsstatus von Runtime-Evidence.
- `docs/reference/variables.*` dokumentiert die externen Status-Root-Variablen.
- Dieses Change-Record-Paar hält Ursache, Workflow-Scope, Tests und
  Delivery-Follow-up fest.

## Runtime-Evidence

Für diese Änderung wurde keine Runtime-Evidence erhoben oder behauptet. Die
Tests sind Source-, Prozesssteuerungs- und CI-Vertragstests; weder ein
erfolgreicher Lint-Lauf noch ein JSON-Statusdatensatz beweist Apache-
Runtime-Verhalten.

## CRS/MRTS- und Protokolldisposition

| Scope | CRS/MRTS-Kombinationen | H1/H2/H3 | Status | Grund |
| --- | --- | --- | --- | --- |
| Apache-Cleanup-Statusübergabe | `no_crs_no_mrts`, `with_crs_no_mrts`, `no_crs_with_mrts`, `with_crs_with_mrts` | H1, H2, H3 | `not_applicable` | Die Änderung betrifft nur Parent-CI-Steuerfluss, bevor ein nativer Harness laufen kann; sie verändert weder Ruleset-Auswahl noch Request-/Response-Verhalten oder Transport. |
| NGINX, HAProxy, Envoy, Traefik und lighttpd | `no_crs_no_mrts`, `with_crs_no_mrts`, `no_crs_with_mrts`, `with_crs_with_mrts` | H1, H2, H3 | `not_applicable` | Kein Connector-Produktcode, Build-Vertrag, keine Konfiguration und kein Runtime-Pfad wurde geändert. |

## Bekannte Einschränkungen

- Der lokale Umgebung fehlen `apxs` und nutzbare Apache-Entwicklungsheader,
  daher bleibt der native Apache/APR-Harness lokal `blocked`.
- Unverändertes lokales `make lint` und `make quick-check` verwenden die
  Framework-Policy zur lokalen Provisionierung, die fehlende Apache-Komponenten
  zu bauen versucht und derzeit bei `missing_local_httpd_build` vor dem
  Cleanup-Target dieser Änderung stoppt. Der CI-Modus liefert stattdessen die
  deklarierte fehlende Voraussetzung und bestand lokal; Remote-Läufe der
  exakten SHA bleiben die maßgebliche CI-Evidence.
- Der Datensatz bewahrt nur eine Steuerungsdisposition; die detaillierte
  direkte Voraussetzungsdiagnose bleibt in der Harness-Log-Ausgabe.
- Pull-Request-Instanzen der fünf Workflows überspringen absichtlich ihren
  schweren Push-only-Step; ihr erfolgreiches Scaffold-Ergebnis ersetzt keine
  Push-Evidence.
- CRS/MRTS- und H1/H2/H3-Runtime-Matrizen sind `not_applicable`: Diese Aufgabe
  verändert weder Connector-Runtime-Verhalten noch Ruleset- oder
  Transportauswahl; die expliziten Dispositionen stehen oben.

## Verbleibende Risiken

Die explizite Erlaubnis ist bewusst eng: Nur fehlende Suche nach einem
nutzbaren `apxs`/`httpd.h`-Paar trägt derzeit
`apache_development_prerequisite`. Zukünftige Aufrufer von
`run-check-status.py` müssen ihren eigenen exakten erlaubten Marker oder
`not_applicable`-Vertrag dokumentieren, statt ihn als globalen Bypass
wiederzuverwenden. Exakte-SHA-GitHub-Actions-Verifikation bleibt vor dem
Lieferabschluss erforderlich.

Die Directory-FD-Abwehr setzt voraus, dass der invocation-eigene `BUILD_ROOT`-
Pfad nicht vor dem Öffnen seines Statusverzeichnisses gleichzeitig durch einen
gleichberechtigten externen Prozess ersetzt wird. Nach dem Öffnen beweist die
Child-Pfadaustausch-Regression, dass das Child den Statusschreibvorgang nicht
umleiten kann. Für ein stärkeres Modell mit hostile Parent-Dateisystem wären
komponentenweise Verzeichnisöffnungen ab einer separat vertrauenswürdigen Basis
erforderlich.

## Nicht ausgeführte Prüfungen mit Begründung

- Kein nativer Apache-Build, keine APR-Lifecycle-Binary-Ausführung,
  kein Runtime-Smoke und kein Protokolltest lief, weil die lokale Apache-
  Buildvoraussetzung fehlt; erwarteter Status ist `blocked`, und die
  fokussierten synthetischen Regressionstests decken den Statusübergabevertrag
  ab.
- Kein `make test-common`, `make test-apache`, `make test-nginx`,
  `make quick-framework-check` oder `make check-repository-path-references`
  lief, weil diese Target-Namen nicht bestehen; die anwendbaren tatsächlichen
  Prüfungen stehen oben.
- Exakte finale Push- und Pull-Request-Workflow-Befehle stehen bis zur
  Branch-Lieferung aus und werden nicht als lokale Passing-Evidence dargestellt.
  Lokale `CI=true`-Läufe üben nur den Framework-CI-Zweig aus und ersetzen sie
  nicht.

## Finaler Diff- und Review-Status

Zu diesem Evidence-Abgleich-Reviewzeitpunkt besteht `git diff --check` und der
geprüfte Scope ist auf den Parent-CI-Klassifikationsvertrag, seine
Regressionstests, gepaarte Dokumentation und diesen Record beschränkt. Vor der
Lieferung werden Staging-Diff, Draft-PR und exakte-SHA-GitHub-Actions-Ergebnisse
erneut geprüft. Eine unveränderliche finale SHA kann ohne Selbstreferenz nicht
in diesem committeten Record stehen; PR #43 hält sie nach finalem Push und
Merge fest. Kein Framework-Zustand und kein Inhalt aus PR #42 sind in diesem
PR enthalten.
