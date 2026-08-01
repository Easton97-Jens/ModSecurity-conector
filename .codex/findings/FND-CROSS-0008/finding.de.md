# FND-CROSS-0008 — Cache-gestützte Apache- und NGINX-Refreshes verlieren ihren Owner-Root-Vertrag in der Parent-Runtime-Matrix

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-CROSS-0008` |
| Kategorie | `ci_failure` |
| Repository / Ownership | `parent_and_framework` / `cross_repository` |
| Priorität / Schweregrad / Konfidenz | `P1` / `not_applicable` / `confirmed` |
| Status / Machbarkeit | `fixed` / `feasible_now` |
| Release-Blocker / Sicherheitsrelevanz | ja / ja |

## Beobachtung und Auswirkung

Der exakte Hosted-Lauf `30197684223`, Job `89782035387`, des Parent-PR #74
für Head `6809e348ad043bf3fcfd9b90d963882cc2fb2` bestand die
Runtime-Komponenten-Vorbereitung und Readiness. Sein Apache-Nachweis baute und
lud `mod_security3.so`. Die verpflichtende Runtime-Matrix lehnte danach beide
Cache-gestützten Connector-Build-Verzeichnisse bei `REFRESH=1` ab: Ihr Owner
Root war das Job-lokale verifizierte `build`-Verzeichnis, während ihre Pfade
unter dem verwalteten Component-Cache liegen.

Die fehlgeschlossenen Entscheidungen verhinderten vollständige
Connector-Summaries; das strikte terminale Evidence-Gate wurde übersprungen.
PR #74 kann daher noch keine frische legitime Runtime-Evidence erzeugen oder
integriert werden. Keine fehlgeschlagene Evidence wurde akzeptiert.

## Ursache und betroffene Grenzen

Parent `ci/runtime/lifecycle/run-full-matrix-parallel.sh` übergibt vorbereitete
Cache-gestützte `APACHE_BUILD_ROOT` und `NGINX_BUILD_DIR` an eine Matrix, die
jedem Job ein separates `BUILD_ROOT` gibt. Für Apache verwendet sie dieses
nicht zugehörige `SHARED_BUILD_ROOT` explizit als `APACHE_BUILD_OWNER_ROOT`.
Dieser Parent-Matrix-Handoff ist fehlerhaft.

Zum Zeitpunkt der Parent-#74-Beobachtung hatte Framework
`ci/provisioning/prepare-nginx-build.sh` keinen unabhängigen NGINX-Owner-Root-
Eingang. Sein `safe_remove_dir` verwendete immer `BUILD_ROOT` als Owner für
`safe_remove_runtime_path`. Das war ein Framework-eigener fehlender Parameter-
und Testvertrag. Framework-PR #48 hat diese historische Framework-Hälfte nun
repariert; der fehlerhafte Parent-Matrix-Handoff bleibt bestehen. Die
kombinierte Ursache ist kein Duplikat des vorherigen Parent-Observability-
Records `FND-PARENT-0054`.

Die Kontrolle selbst ist sicherheitsrelevant: Sie verhindert, dass ein
Refresh-Pfad ein Verzeichnis außerhalb seines deklarierten Owner Roots löscht.
Die korrekte Reparatur muss dieses Containment erhalten und darf es nicht
aufweiten oder umgehen.

Die kontrollierten Werte sind `APACHE_BUILD_ROOT`/`NGINX_BUILD_DIR` aus dem
vorbereiteten Runtime-Snapshot und die Matrix-`REFRESH`-Entscheidung. Die
vertrauenswürdigen Eingaben sind der verifizierte Parent-Component-Cache und
der Framework-Helper `safe_remove_runtime_path`; der Löschguard ist der Sink.
Es wird kein angreiferkontrollierter Pfad oder Runtime-Exploit behauptet. Die
Sicherheitsinvariante lautet: Ein Refresh-Target muss ein absoluter sicherer
generierter Pfad innerhalb eines explizit validierten Connector-Cache-Owner-
Roots sein; weder ein Job-lokales `BUILD_ROOT` noch ein Cache-Root darf still
einen Sibling-, Symlink-, relativen oder Systempfad autorisieren.

## Evidence und Reproduktion

Aufbewahrte begrenzte Evidence ist
`.codex/runs/20260726T103539Z-pr74-cache-owner-root/evidence/hosted-cache-owner-root-blocker.md`
(SHA-256 `aeeb731c3c4b3eb5902b6624b5a5c7db41fb3367f01c2ca594735195181a3d9a`). Sie dokumentiert exakten Run/Job,
die zwei fehlgeschlossenen Owner-Root-Entscheidungen und die
Source-to-Sink-Aufteilung ohne Credentials oder destruktive Reproduktion.

Aufbewahrte Framework-Integrations-Evidence ist
`.codex/runs/20260726T115300Z-framework-pr48-master-integration/evidence/framework-pr48-master-integration.md`
(SHA-256 `2460d2f15a027e79f08aee120ce487a6ff2714d882fa46b15786d2615d43c7c3`). Sie dokumentiert geschützten Refresh,
Exact-Head-Checks, normalen Merge, Gleichheit des Result-Trees, Master-
Workflows und exakte Master-SonarQube-Cloud-Analyse ohne Credentials oder
Payloads.

Zur Reproduktion diesen exakten Hosted-Job inspizieren und die Parent-
Matrix-Aufrufe sowie Framework-NGINX-`safe_remove_dir` verfolgen. Nicht
`REFRESH` deaktivieren, `BUILD_ROOT` aufweiten, Cache-Inhalt löschen oder das
terminale Gate ändern, nur um einen grünen Lauf zu erhalten.

## Erforderliche Reparatur und Validierung

Framework-PR [#48](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/48)
ist nun gemergt. GitHub refreshte ihn auf exakten Head
`19ec85c5359e83d3da59213e03bbeae9ac6c8ede` auf Basis
`ab7374e08f12f80b1e6a7224418e4e04ca19ddc6` und mergte ihn anschließend normal
mit Exact-Head-Schutz als `a7ebf5a1d9cad2b0a65a7603476a1434fdb16cf6`. Der
Result-Tree entspricht dem geprüften Head-Tree `a6d405c6bc2ff8af689989fbee2d2505389f8f18`.
Die Cache-contained-Positivkontrolle und Outside-Owner-, Symlink- und
Relative-Owner-Root-Negativkontrollen bestanden; alle refreshed-Head-Checks
und alle resultierenden Master-Workflows bestanden. PR- und Master-SonarQube-
Cloud-Quality-Gates sind `OK` mit null offenen Issues und `0.0` neuer
Duplicated-Lines-Density.

Parent-PR-#74-Head `093df42d8773c3d0a5c843225fe7c3575fa4e67f` leitet nun
`CONNECTOR_COMPONENT_CACHE/builds/connectors` ab, validiert jeden Apache-/NGINX-
Build-Root kanonisch darunter und übergibt ihn explizit an beide Refresh-Guards,
während der Job-spezifische `BUILD_ROOT` isoliert bleibt. Der echte Matrix-
Runner hat lokale Same-Boundary-Positivkontrollen für beide Connectoren bei
`REFRESH=1` sowie eine Outside-Owner-Ablehnung vor `make`. Das normale Branch-
Update führt den Framework-Gitlink aus Parent-PR #125 mit. Frische Exact-Head-
Hosted-Producer- und strikte Terminal-Gate-Evidence bleiben erforderlich; MRTS
bleibt unverändert, weil keine MRTS-eigene Reparatur nachgewiesen ist.

## Restrisiko und Historie

### Fortsetzung — 2026-07-26

Das begrenzte a0f-NGINX-configure-Log hat den verbleibenden Source-Build-Fehler
nun klassifiziert. Die getrennt behebbare Parent-only-Auslassung ist
`FND-PARENT-0056`: Die Cache-Vorbereitung übergab `MSCONNECTOR_COMMON_SRC`,
aber der bereite Invocation-lokale Snapshot nicht. Frameworks normale `env`-
Vererbung löscht diesen Wert nicht. Der Parent leitet ihn jetzt ausschließlich
aus `CONNECTOR_ROOT/common/src` ab; es werden weder Job-Override noch Fallback,
Guard-Lockerung, Framework-Änderung oder MRTS-Aktion verwendet. Die
aufbewahrte Klassifikations-Evidence ist
`.codex/runs/20260726T135925Z-pr74-nginx-common-source-snapshot/evidence/parent-nginx-common-source-snapshot-root-cause.md`
(SHA-256 `f9b8c36c52f41e9fda2535ffa7522033f06b9e52bfe21e61a6d1e5c25ed5f52a`).
Dieses Finding besitzt weiterhin das unabhängige Owner-Root-Containment-Problem
und dessen frische Exact-Head-Producer-Voraussetzung.

Die Framework-Containment-Reparatur ist ohne Lockerung eines Guards verifiziert
und der Parent-Handoff ist auf dem veröffentlichten exakten #74-Head
implementiert, aber das strikte Terminal-Gate bleibt für diesen Head noch
unbewiesen. Es erfolgte keine Suppression, Owner-Root-Aufweitung, Guard-Bypass
oder Risikoakzeptanz; MRTS-Source und Gitlink bleiben unverändert.
`FND-CROSS-0001`, `FND-PARENT-0053`, `FND-PARENT-0054` und
`FND-SONAR-0016` sind verwandt.

- 2026-07-26 — Exakte Hosted-#74-Evidence stellte den Parent/Framework-
  Owner-Root-Vertragssplit und seinen fehlgeschlossenen Release-Blocker fest.
- 2026-07-26 — Der aktuelle Nutzer autorisierte ausdrücklich einen isolierten
  Framework-Branch, Commit, Push und Draft-PR (sowie einen MRTS-PR nur falls
  nötig). Die Framework-Reparatur ist damit `feasible_now`; ihr Merge und die
  spätere Parent-Gitlink-Aktion bleiben absichtlich bis zur Nutzerprüfung und
  -meldung zurückgestellt.
- 2026-07-26 — Framework-Draft-PR #48 wurde auf exaktem Head
  `f98c4b58f4dbbf8e15064f4ae1139a470529bd9f` geöffnet. Er ergänzt den
  defaulteten und validierten NGINX-Owner-Root nur am bestehenden
  Refresh-Löschguard sowie Same-Boundary-Positiv-/Negativkontrollen. Er ist
  geöffnet, Draft und hat Current-Head-Checks ausstehend; Codex mergte ihn
  nicht.
- 2026-07-26 — Exact-Head-SonarQube Cloud für Framework-PR #48 bestand mit 0
  OPEN/CONFIRMED-Issues, `new_duplicated_lines=0` und
  `new_duplicated_lines_density=0.0`. CodeQL, Secret Scanning, OSV, OpenSSF
  und Common-Structure sind terminal erfolgreich; Lint bleibt ausstehend,
  daher ist der PR noch nicht `verified_pr`.
- 2026-07-26 — PR #48 wurde geschützt auf `19ec85c…` refresht, alle
  Exact-Head-Checks bestanden nach einem erfolgreichen Retry eines externen
  OSV-Service-Ausfalls, und der nutzerautorisierte normale Merge erzeugte
  Framework-Master `a7ebf5a…`. Der Merge-Tree entspricht dem geprüften Tree
  `a6d405c6…`; Master-Lint, Test-Common, OpenSSF, CodeQL, SonarQube-Cloud-
  Quality-Gate und Leak-Period-Open-Issue-Abfrage bestanden. Die Framework-
  Hälfte ist verifiziert, aber Parent-#74-Source-Handoff und Exact-Head-
  Runtime-Evidence bleiben der Release-Blocker. Parent-PR #125s Bot-Gitlink-
  Advance ist beobachteter externer Zustand und kein Ersatz für diese
  Validierung.
- 2026-07-26 — Parent-#74-Head
  `093df42d8773c3d0a5c843225fe7c3575fa4e67f` wurde normal mit aktuellem
  `master` gemergt und gepusht. Er implementiert den engen Parent-Owner-Root-
  Handoff und fokussierte Cache-contained-/Outside-Owner-Regressionstests.
  Shell-Syntax, 18 fokussierte Runtime-/Pfad-Tests, Runtime-Pfad-Policy,
  CI-Sicherheitsvertrag, zweisprachige Dokumentation, Dokumentationslinks,
  Framework-Fixture-Syntax und Whitespace-Checks bestanden lokal. Exact-Head-
  Hosted-Abschluss bleibt ausstehend.
- 2026-07-26 — Die Exact-Head-Producer-Läufe `30201764369`/`89792783415` und
  `30201763067`/`89792780237` beendeten Vorbereitung/Readiness, scheiterten
  aber fail-closed in direktem `runtime-matrix-all-runtime`: Dem lokalen
  Snapshot fehlte `NGINX_BUILD_OWNER_ROOT`, daher wies Framework den Cache-Build
  korrekt gegen den Job-Root ab. Die Parent-Nachfolge-Reparatur veröffentlicht
  den engen `CONNECTOR_COMPONENT_CACHE/builds/connectors`-Owner-Root für beide
  Connector-Builder und Snapshot-Consumer. Drei Direct-/Full-Matrix-
  Kontrollen, 27 Cache-Contract-Kontrollen, Runtime-Pfad-Policy,
  CI-Sicherheitsvertrag, bilinguale Dokumentation, Fixture-Syntax,
  Dokumentationslinks und Whitespace bestanden lokal; frische Hosted-Evidence
  für den Nachfolge-Head bleibt erforderlich.
- 2026-07-26 — Die exakten Hosted-Producer `30203025925`/`89796178895` und
  `30203024433`/`89796175146` für Nachfolge-Head
  `ece2d335c7106a38bf51feb3f9937ec3b9e09ef1` bestanden Component-Vorbereitung
  und Readiness und erreichten danach NGINX-Source-Build-`configure` statt der
  historischen Owner-Root-Ablehnung. Das feste Configure-Log fehlte in der
  begrenzten Parent-Failure-Summary, daher wird seine Source-Build-Ursache
  nicht hergeleitet. Die aufbewahrte Zusammenfassung
  `.codex/runs/20260726T132600Z-pr74-nginx-configure-observability/evidence/hosted-nginx-configure-observability-gap.md`
  hat SHA-256 `a89b41b87ea076a5a83e29e19fcfa490f8fba1ce327157cff649d884ab3bebbe`.
  Parent-Head `a0f337b8e45e5661b1ed09c7bf39b958548fbd14` ergänzt nur diese
  feste Diagnose für reguläre Nicht-Symlink-Dateien mit Command-Masking und
  ihre Workflow-Security-Regression mit 20 Tests; vollständige Exact-Head-
  Evidence bleibt erforderlich.
