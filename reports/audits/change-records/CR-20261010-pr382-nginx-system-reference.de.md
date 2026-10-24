# Change Record: CR-20261010-pr382-nginx-system-reference

**Sprache:** [English](CR-20261010-pr382-nginx-system-reference.md) | Deutsch

Reine nachgelagerte Dokumentationsreferenz; ursprünglicher Runtime-Status und verbleibende Messlücke bleiben getrennt.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261010-pr382-nginx-system-reference |
| Datum (UTC) | 2026-10-10 |
| Basis-Revision | `2a5704f82fdae4ba75902eb3f4244225838e1747` |

## Motivation und Problemstellung

Einen nachgelagerten NGINX-H1-Systemnachweis aus PR #396 referenzieren, ohne einen Runtime-Test des unveränderten PR-#382-Produkts zu behaupten.

## Akzeptanzkriterien

Beide Sprachen erhalten exaktes getestetes Tupel/Run, Original-Canonical-Status, direkten First-Byte-Writer-Exit, konkretes lokales System und verbleibende Messlücke. Breite Connector-Abnahmepunkte bleiben offen; keine Produkt-, Gitlink- oder Runtime-Evidence-Änderungen.

## Implementierungsentscheidung und Begründung

Separaten reinen Dokumentationsworktree auf dem verifizierten PR-#382-Branch verwenden. Neue eng begrenzte I12b/V08a/V09a/V10a referenzieren beobachtete Teilbereiche, keine vollständige Abnahme. Stackaussagen vom 05.10.2026 ausdrücklich historisch markieren.

## Geänderte Dateien

`docs/pr-382-checklist.md`, `docs/pr-382-checklist.de.md` und dieses Change-Record-Paar. Keine Produktdateien oder generierte Runtime-Evidence verändert.

## Ausgeführte Befehle

Ausgeführt: `rtk proxy /var/tmp/codex/ModSecurity-test-Framework/venv/bin/python ci/tools/new-change-record.py create --name pr382-nginx-system-reference --base-revision 2a5704f82fdae4ba75902eb3f4244225838e1747 --date 2026-10-10`: Exit 0. Dokumentationsprüfergebnisse werden nach tatsächlicher Ausführung erfasst; hier wird keine unausgeführte Prüfung behauptet.

Nativer Archivcheck `rtk proxy /var/tmp/codex/ModSecurity-test-Framework/venv/bin/python ci/tools/new-change-record.py check`: Exit 0 (nur Struktur). Ausgeführt: `rtk proxy /var/tmp/codex/ModSecurity-test-Framework/venv/bin/python -m unittest -v tests.test_change_record tests.test_prepare_reviewed_framework_handoff`: 39 Tests, 0 SKIP, Exit 0. Ausgeführt: `rtk proxy git -C /var/tmp/codex/ModSecurity-conector/worktrees/pr382-nginx-system-docs-r16 diff --check`: Exit 0.

Initialer nativer Dokumentationsbefehl `rtk proxy make --no-print-directory PYTHON=/var/tmp/codex/ModSecurity-test-Framework/venv/bin/python FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/framework-nginx-seven-contracts-20261008 BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/analysis/nginx-full97-777a244f-20261010T181030Z/doc-validation-build check-bilingual-docs check-doc-links`: Exit 2. Der unveränderte Zweisprachigkeitschecker meldete 22 fehlende lokale Submodule-Ziele im unbestückten Dokumentationsworktree; check-doc-links wurde nicht ausgeführt. Kein Validator wurde abgeschwächt oder Link-/Symlink-Workaround eingeführt. Dieser Fehlschlag bleibt unabhängig von späterer Validierung dokumentiert.

Nachdem Root den physischen Framework-Baum am unveränderten Gitlink dieser Dokumentationsbasis `dc41bd22c335156cae02d9049098b92af65b7c57` bereitstellte, ausgeführt: `rtk proxy make --no-print-directory PYTHON=/var/tmp/codex/ModSecurity-test-Framework/venv/bin/python FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/pr382-nginx-system-docs-r16/modules/ModSecurity-test-Framework BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/analysis/nginx-full97-777a244f-20261010T181030Z/doc-validation-build check-bilingual-docs check-doc-links`: Exit 0; Zweisprachigkeit, Repository-Pfadreferenzen und Dokumentationslinks bestanden. Der frühere Missing-Tree-Fehler ist behoben, nicht gelöscht. Manueller EN/DE-Abgleich bestätigt gleiche Hashes, IDs, Zähler, Grenzen und angehakte/offene Punkte.

## Security-Auswirkung

Keine Security-Kontrollen, Validatoren, Isolation, Required-Auswahl oder CI-Gates verändert. Keine Secrets, Hostnamen oder öffentlichen Adressen enthalten. Der fehlende exakte generische Strict-Client-Prozessexit bleibt sichtbar.

## Runtime-Evidence

R16 `nginx_full97_777a_20261010_r16`, getesteter Parent `777a244f0689c320475b030b9e7adbb3192febbe`, Framework `9f41f80db7bf53b57429457bce0dda675d2ec5d7`, MRTS `8a6bb546c4c81d8ffc7be801dceac60c6925685f`. Original-Canonical PASS, 97/97 Required-PASS, leere Schemafehler. Genau ein direkter First-Byte-Source-Writer-Abschluss Exit 0; 13 direkte Abschlüsse/neun Programme alle Exit 0. Das Standardtarget lief auf dem in der Checkliste beschriebenen konkreten lokalen System. Original-R15 bleibt unverändert.

## Bekannte Einschränkungen

Der numerische Exit des generischen H1-Strict-curl-Prozesses ist NOT SEPARATELY MEASURED; Diagnose 52 ist kein Exit 52. Die lokale Abnahme bleibt trotz Original-Canonical PASS BLOCKED. Kein H2/H3-, CRS-, Off-, Alle-Plattformen-, Produktions- oder Protected-Nachweis; andere Connector-Routen bleiben getrennt.

## Verbleibende Risiken

Öffentliche Zusammenfassungen verteilen das lokale Raw-Bundle nicht. Der PR-#382-Produktstand wurde durch den nachgelagerten Lauf nicht getestet. Ready-/CI-/Sonar-/Merge-Ergebnisse werden nicht aus Runtime- oder Dokumentationserfolg abgeleitet.

## Nicht ausgeführte Prüfungen mit Begründung

Der Dokumentationsworker führte keinen Full97, Runtime-Lauf, Build, Git-Liefervorgang, API-Vorgang oder Ready-Übergang aus. Root verantwortet Runtime-/Liefer-/Readiness-Entscheidungen; kein zweiter vollständiger Lauf gehört zu dieser Änderung.

## Finaler Diff- und Review-Status

Nur die vier eigenen Dokumentationspfade sind verändert; native Dokumentations-/Archivchecks, 39 Regressionen und Whitespace-Prüfungen bestanden. Manueller EN/DE- und finaler Diff-Abgleich fand keine fremden Änderungen oder unfertigen Vorlagenabschnitte. Dieser Worker hat die Dokumentationsänderungen weder committed noch veröffentlicht; unabhängiger Root-Review und normale Lieferung bleiben getrennt. Kein Merge oder Umschreiben der Historie.
