# Change Record: Parent-Framework-Komponentenresolver

**Sprache:** [English](CR-20260818-framework-component-resolver.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260818-framework-component-resolver |
| Datum (UTC) | 2026-08-18 |
| Basis-Revision | 274c9e01770ebd9ac932eacf5c2ba2e5e85026c2 |
| Historischer Actions-Lauf | 32163726555 |
| Framework-Kandidat | bd69ee96e0e7082317d4afe1232bee625665eb9a |
| Auslieferungsstatus | Parent-PR #300 ist offen. Dieser Record erfasst das lokale Source-/Test-Follow-up; Hosted-Checks am Successor-Head, Review und Merge stehen noch aus. Es wird keine Framework-Änderung oder Gitlink-Aktualisierung behauptet. |

## Motivation und Problemstellung

Der GitHub-Actions-Lauf `32163726555` schlug im Job `Validate submodule update`
beim Schritt `Validate Framework component-pin data contract` fehl, als der
Kandidat `bd69ee96e0e7082317d4afe1232bee625665eb9a` vom Parent-Gitlink
`3cb33609626ff689c54b6dc0f31fb7e9401fe75e` geprüft wurde. Die beobachtete
Meldung lautet:

```text
sync-framework-component-versions: error: non-literal assignment in LIGHTTPD_SOURCE_URL
```

Die Vorab-Reproduktion extrahierte nur mit `git show` eine reguläre temporäre
Datendatei und ließ Parent `--validate` mit Exit 2 und derselben Meldung
beenden. Es wurde keine Kandidaten-Shell- oder Python-Datei gesourct,
ausgeführt, importiert oder ausgewertet durch diese Reproduktion.

Separat führte die zunächst wirksame Parent-Full-Discovery bestehende
Framework-Python- und Shell-Pfade aus dem Kandidaten-Checkout aus. Dies ist
eine Verletzung der Task-Grenze, keine Behauptung, dass dieser Kandidat bösartig
war. Sie bleibt als Evidenz für `FND-PARENT-0178` erhalten und wird unten
eingedämmt.

## Akzeptanzkriterien

- Kanonische, reihenabgeleitete Kandidatendaten ohne Framework-Codeausführung parsen.
- Feste Source-/Target-Listen, fail-closed Syntax, Pfadsicherheit, Modi, atomaren Ersatz und Rollback bewahren.
- Lighttpd `1.5.x`, generisches HAProxy `3.3.x`, unabhängige HTX-Werte sowie NGINX/OpenSSL-Ableitungen unterstützen.
- Einen abweichenden Framework-Test-Root zurückweisen, bevor ein Parent-Test Framework-eigenen Code importiert, sourct oder startet.
- Aufgelöste Referenzausgabe vor semantischer Validierung begrenzen und das
  Git-Programm, das Framework-Root-Vertrauen begründet, niemals aus geerbtem
  `PATH` auswählen.
- Nur beobachtete lokale Evidenz dokumentieren und keinen Hosted-Erfolg behaupten.

## Implementierungsentscheidung und Begründung

Der Parent-Synchronisierer verwendet nun eine feste `SOURCE_REGISTRY` mit
Validatoren und Verbraucherkennzeichnungen. Sein begrenzter, nicht
ausführender Resolver akzeptiert direkte Literale, `$NAME`, `${NAME}` sowie
Konkatenationen aus Literalen und erlaubten Referenzen; als einzige Sonderform
ist `${NGINX_RELEASE_TAG#release-}` erlaubt. Der weiter bestehende
Selbst-Default `NGINX_QUIC_TLS_LIBRARY` wird statisch zu `openssl`
aufgelöst, niemals aus der Aufruferumgebung.

Unbekannte Referenzen, nicht erlaubte Operatoren, CR/LF, Duplikate, Zyklen,
fehlende Werte, ungültige Tupel, Ausgabe pro Wert über 64 KiB und aggregierte
Ausgabe über 256 KiB schlagen vor jedem Schreibzugriff oder vor semantischer
Validierung fehl.

Die erste SonarQube-Cloud-Analyse des Draft-PR meldete aufgabeneigene
Maintainability-Issues. Das fokussierte Follow-up bewahrt statische Grammatik
und Byte-Budget-Controls, extrahiert aber Helper für Variable/Referenz und
Namensauflösung, zentralisiert wiederholte Registry-Labels, bewahrt
ASCII-only-Digit-Semantik und vereinheitlicht die betroffene Assertion-Order.
Es führt keine Regelunterdrückung, kein `NOSONAR` und keine Quality-Gate-
Änderung ein.
Lighttpd-Projektionen enthalten jetzt `LIGHTTPD_SERIES`; der Shell-Contract
hat keine Schemaversion, daher ist kein Versionssprung nötig. Das vorhandene
HTX-Ziel verwendet ausschließlich `HAPROXY_HTX_*`; `TargetSpec` und Workflow
blieben unverändert.

Die Parent-Test-Suite verwendet nun vor jedem auditierten Framework-Import,
jeder Source oder jedem Framework-eigenen Launch einen gemeinsamen
Trusted-Framework-Root-Guard. Er prüft Parent-Gitlink, exakten Framework-HEAD,
vollständige Worktree-Sauberkeit und eine reguläre `ci/lib/common.sh` mit
bereinigten lock-freien Git-Metadatenaufrufen. Sein Git-Programm wird
ausschließlich aus festen absoluten Systempfaden und nie aus geerbtem `PATH`
gewählt. Der aktuelle abweichende Kandidat wird vor dem Sink übersprungen; ein
Unit-Control lässt einen sauberen Exact-Gitlink-Root zu.

Das Follow-up bindet jede APR-util-Child-Umgebung in
`tests/test_runtime_env_snapshot_contract.py` an diesen bereits validierten
Root, statt ein geerbtes `FRAMEWORK_ROOT` über `setdefault` zu behalten. Der
Regression-Control beweist die Ersetzung eines kollidierenden Umgebungswerts.

## Geänderte Dateien

- `ci/tools/sync-framework-component-versions.py`
- `tests/test_update_framework_versions.py` und `tests/test_ci_security_workflows.py`
- `tests/test_runtime_env_snapshot_contract.py`
- Lighttpd-Contract, Source-Map, Leser und Contract-Tests
- Parent-Test-Root-Trust-Helper plus alle auditierten Framework-ausführenden
  Parent-Testpfade
- gepaarte Variablendokumentation, `FND-PARENT-0177` bis
  `FND-PARENT-0181`, Evidenz, Roadmap/Index sowie dieser gekoppelte Change Record

## Ausgeführte Befehle

| Prüfung | Beobachtetes Ergebnis |
| --- | --- |
| Read-only `gh run view 32163726555 --log-failed` | historischer Exit-2-Fehler beobachtet |
| Vorab `git show` + Parent `--validate` | reproduziert: Exit 2, exakte `LIGHTTPD_SOURCE_URL`-Meldung |
| `python3 -m py_compile ci/tools/sync-framework-component-versions.py tests/test_update_framework_versions.py` | bestanden |
| `.venv/bin/python -m unittest tests.test_update_framework_versions -v` | bestanden: 17 Tests nach Hinzufügen der Controls für aufgelöste Bytes |
| `.venv/bin/python -m unittest tests.test_ci_security_workflows -v` | bestanden: 28 Tests |
| `.venv/bin/python -m unittest connectors.lighttpd.tests.test_patched_host_contract -v` | bestanden: 27 Tests |
| `.venv/bin/python -m unittest tests.test_haproxy_modsecurity_resolver -v` | bestanden: 11 Tests |
| `make PYTHON=.venv/bin/python check-ci-security-contract` | bestanden: 110 Tests, 4 erwartete Capability-Skips |
| Offline-Canonical-Fixture `--validate` | bestanden: Exit 0 |
| Temporäre Parent-Kopie `--sync`, danach `--check` | beide Exit 0; `--check` meldete `changed: []` |
| Exakte Kandidaten-Gitdaten `--validate` | bestanden: Exit 0, ohne Kandidatencodeausführung |
| Finale fokussierte Resolver-/Contract-/Consumer-Suite | bestanden: 103 Tests |
| Parent-Test-Root-Containment-Suite | bestanden: 184 Tests, 62 erwartete Abweichungs-Skips vor auditierten Kandidatenausführungssinks |
| Control für kollidierende Umgebung in `tests.test_runtime_env_snapshot_contract` | bestanden: 22 Tests; jeder APR-util-Child ersetzt das geerbte `FRAMEWORK_ROOT` durch den validierten Root |
| Vollständige Parent-Discovery im sauberen Standalone-Clone mit kollidierendem Umgebungs-`FRAMEWORK_ROOT` | bestanden: 1.216 Tests, 4 erwartete Skips; der Exact-Gitlink-Framework-Root wurde gewählt und Clone sowie gemeinsamer Checkout blieben erhalten |
| Fokussierte Suite nach Security-Remediation | bestanden: 290 Tests, 62 erwartete Abweichungs-Skips; Fake-PATH-Git-Auswahl- und Resolver-Fan-out-Controls bestanden ohne Kandidatenausführung |
| SonarQube-Cloud-Exact-Head-Issue-Inspektion des Draft-PR | Quality Gate bestanden, aber 27 aufgabeneigene New-Issue-Code-Smells erforderten fokussierte Remediation; eine Successor-Head-Analyse bleibt erforderlich |
| Bilingual-Checker-Unit-Suite, gezieltes Record-Paar, Variablen- und Parent-Pfadprüfung | bestanden: 22 Tests; gezieltes Paar; 100 Referenzen; Parent-Pfade PASS |
| `git diff --check` | bestanden: Exit 0 |
| Wörtliches `python -m unittest discover -q` | Exit 5: null Tests gefunden |
| Historische wirksame `python -m unittest discover -s tests -q` im Kandidaten-Checkout | Exit 1: 1.186 Tests, 16 Failures und 1 Error; als unsichere historische Evidenz erhalten, keine aktuelle Validierung |

## Security-Auswirkung

Dies ist eine Supply-Chain-Datengrenze. Der statische Updater behandelt
Kandidaten-`common.sh`-Bytes weiterhin nur als Daten; nicht unterstützte Syntax,
unsichere URLs, fehlerhafte Digests, Symlinks, nicht-reguläre Dateien,
unsichere Pfade und Fehler blockieren Schreibzugriffe. `TARGET_REGISTRY` bleibt
die einzige Parent-Schreiballowlist.

Die initiale abgegrenzte Full-Discovery deckte ein separates validiertes
High-Impact-Testgrenzen-Finding auf: Sie konnte einen abweichenden Kandidaten
vor einer Vertrauensprüfung ausführen. `FND-PARENT-0178` ist durch den
gemeinsamen Parent-Test-Root-Guard lokal fixed. Die Post-Fix-Containment-Suite
aus 12 Modulen bestand mit allen kandidatenabhängigen Pfaden, die vor ihren
Ausführungssinks überspringen. Ein später autorisierter Standalone-Clone stellte
einen sauberen Exact-Gitlink-Framework-Root bereit; das Child-Environment-
Follow-up erzwingt diesen Root an jedem APR-util-Sink. Sein fokussierter
Control mit kollidierender Umgebung bestand 22 Tests, und die Full-Discovery
bestand mit 1.216 Tests und 4 erwarteten Skips bei Erhalt von Clone und
gemeinsamem Checkout.

Die Delivery-Diff-Review validierte außerdem zwei unabhängige Controls im neuen
Code: `FND-PARENT-0179` zeigte, dass ein Git-Programm aus geerbtem PATH den
Guard umgehen konnte, und `FND-PARENT-0180` zeigte, dass allowlistetes
Referenz-Fan-out vor semantischer Validierung CI-Ressourcen erschöpfen konnte.
Beide sind lokal durch absolute Git-Pfadauswahl und explizite Budgets für
aufgelöste Bytes behoben; die fokussierte Suite mit 290 Tests deckt bösartige
und legitime Controls ohne Kandidatencode-Ausführung ab.

`FND-PARENT-0181` ist ein validiertes aufgabeneigenes Maintainability-Finding,
keine Security-Schwachstelle und kein Hotspot. Seine fokussierte Remediation
bewahrt die statische, nicht ausführende Sicherheitsgrenze des Resolvers; es
wurde keine SonarQube-Unterdrückung und keine Quality-Gate-Änderung verwendet.

## Runtime-Evidence

Der Hosted-Fehler ist ausschließlich Vorab-Evidenz. Nach dem Fix liegen lokale
statische, Contract-, Regression-, Kandidaten-Test-Root-Containment- und saubere
Standalone-Full-Suite-Evidenz vor; sie behauptet keinen Source-, Build-,
Produktions-, Publisher- oder Hosted-Erfolg. Der Resolver verwirft absichtlich
künftige Shellformen außerhalb seiner dokumentierten Grammatik.

## Bekannte Einschränkungen

Aktuelle Parent-NGINX-Broker-Projektionen weichen vom
Kandidaten ab; lokales `--validate` meldet daher mögliche Änderungen ohne zu
schreiben. Nur die temporäre Parent-Kopie wurde für den No-Drift-Check
synchronisiert. Die frühere Discovery im Kandidaten-Checkout bleibt unsichere
historische Evidenz. Die Ursache der gemeinsamen-Checkout-Mutation aus
`FND-PARENT-0182` ist weiterhin nicht lokalisiert; der bestandene Standalone-
Clone kapselt ihre PR-Validierungsauswirkung, ohne diese historische Mutation
zu erklären.

## Verbleibende Risiken

Frische Hosted-Checks am Successor-Head einschließlich SonarQube Cloud, wenn
konfiguriert, bleiben für verifizierte Delivery-Evidenz erforderlich.
`FND-PARENT-0177` bis `FND-PARENT-0181` sind lokal behoben, nicht am
Successor-Head oder resultierenden master verifiziert. `FND-PARENT-0182`
bleibt ein nicht lokalisierter Lifecycle-Befund, aber sein PR-spezifischer
Validierungsblocker ist durch den bestandenen Standalone-Clone gekapselt;
dieser Record behauptet keinen Hosted-Erfolg oder Merge.

## Nicht ausgeführte Prüfungen mit Begründung

Keine Framework-Änderung, kein Parent-Gitlink-Update, Dependency-Upgrade,
Hosted-Dispatch/Rerun, Merge, Runtime-Matrix oder Netzwerk-Download wurden
ausgeführt. Der breite `check-bilingual-docs`-Scan wurde nach wiederholtem
Polling ohne Ausgabe abgebrochen; `make check-doc-links` wurde nicht
ausgeführt, weil es ein Framework-Skript aufruft und damit die
Kandidaten-Nichtausführungsgrenze verletzen würde.

Die vollständige Parent-Suite wurde nach Containment nur in einem task-eigenen
Standalone-Clone mit sauberem Exact-Gitlink-Framework-Root und kurzer privater
AF_UNIX-Temporärwurzel wiederholt. Sie bestand; dieses Ergebnis lokalisiert die
historische gemeinsame-Checkout-Mutation in `FND-PARENT-0182` nicht.

## Finaler Diff- und Review-Status

Fokussierte Source-, Contract-, Security-, Dokumentations- und statische
Kandidatenprüfungen bestanden. Die Suite nach der Security-Remediation mit
290 Tests, der 22-Test-Child-Environment-Control mit kollidierender Umgebung
und die Standalone-Full-Suite mit 1.216 Tests bestanden. Die finale Prüfung
`git diff --check` bestand vor dem Successor-Commit mit Exit 0; der
Parent-`HEAD`-Gitlink bleibt `3cb33609626ff689c54b6dc0f31fb7e9401fe75e`, und
es liegt keine im Index vorgemerkte Gitlink-Änderung vor.
Bereinigte Evidenz liegt unter
`.codex/runs/20260818T180159Z-parent-framework-component-resolver/evidence/pre-fix-and-local-validation.md`
mit SHA-256
`67ee7d5a7c9bce730f3d0154aa2a3409d0049e4f5740752880c0b7b392529166`.
Containment-Evidenz liegt unter
`.codex/runs/20260818T180159Z-parent-framework-component-resolver/evidence/post-fix-candidate-test-root-containment.md`
mit SHA-256
`0b5fe7d8eca9cff654c9640d9dae61bde3b44265202c4373c3bb445150aafbc4`.
Der erfolgreiche Standalone-Full-Suite-Receipt liegt unter
`.codex/runs/20260819T014107Z-parent-framework-component-resolver-delivery/evidence/pr300-clean-clone-full-suite-success.md`
mit SHA-256
`e62096e99e323223dc5348f16ef6edaf62258d90ffa91bcaacc3bad073b8f56f`.
