# KI-Übergabe

**Sprache:** [English](AI-HANDOFF.md) | Deutsch

## Stand und Ziel

- Datum: **2026-11-14 (Europe/Berlin)**; Checkout: Repository-Root (`$CONNECTOR_ROOT`).
- Branch: `master`; Task-Branch `codex/ai-handoff-and-framework-pin-20261114` bei `902eaa71`; per Squash über PR #449 in `master` am **2026-11-14T10:45 UTC** gemerged; `origin/master` identisch; Arbeitsbaum sauber; Bereinigung des Task-Branches noch nicht dispositionsiert.
- **Gesprächskontext:** Zunächst eine rein dokumentarische Claude-Code-Übergabe vorbereiten, danach einen PR einschließlich der anderen vorhandenen Änderungen erstellen. Der zweite Auftrag erlaubt Task-Branch-Commit/Push/PR und die Aufnahme des Framework-Pins, keinen Merge. Der Nutzer erlaubte anschließend die exakte Operator-Freigabe für Gitlink/Index; diese ist jetzt installiert; die Arbeit wurde später durch PR #449 ausgeliefert. Frühere Produktgespräche oder Testprotokolle liegen hier nicht vor.
- **Belegte Fakten:** Lokale Diffs und native Befehlsdefinitionen wurden untersucht; frische Remote-Abfragen bestätigten Parent-`master` am PR-#449-Merge-Commit und Framework-`master` bei `31531f74cfe26c2a40d4bb5f6eaae4c0920127e1`; Current-Head-CI bei `da212088f018b7852284768ced03feca286980ef` wurde per GitHub CLI zurückgelesen.
- **Annahme:** Claude Code setzt in diesem Checkout fort, wo ignorierte lokale Anweisungen verfügbar bleiben. Diesen Stand vor Verwendung abgleichen.
- **Letzte Aufgabe (2026-11-19, Claude Code):** Korrekturen aus der Sicherheitsprüfung vom 2026-11-15 auf dem Task-Branch `claude/fix-security-findings-20261119` (Basis `b79c3d93efbb8330f121caf8fb7c1a7874195e57`), ausgeliefert als Draft-PR, nicht gemergt. Umfang, Entscheidungen (einschließlich der Begründung, warum CAND-024 nicht geändert wird), Befehle und Ergebnisse: [Change Record](../reports/audits/change-records/CR-20261119-composite-cleanup-redirect-haproxy-rule-id.de.md). Die Tests nutzten den offiziellen ModSecurity-v3.0.17-Build, nicht die Systembibliothek. Der folgende Stand beschreibt die frühere Arbeit vom 2026-11-14 und bleibt historisch.

## Relevante Komponenten und umgesetzte Arbeit

- `common/` besitzt gemeinsame Produktverträge/Laufzeitlogik; `connectors/` besitzt Adapter für Apache, NGINX, HAProxy, Envoy, Traefik und lighttpd. Logische Profile behalten getrennte Laufzeitaussagen; siehe [Connector-Übersicht](connectors/README.de.md) und [Architektur](architecture.de.md).
- Das Root-`Makefile` definiert Produkt-Build-Einstiege und delegiert Test-/Check-Targets an `modules/ModSecurity-test-Framework/connector_suite/connector.mk`. Framework und dessen verschachteltes `tools/MRTS` bleiben getrennte Repositorys.
- Der bestehende Parent-HEAD aktualisiert Workflow-Werkzeug-Pins in `.github/workflows/`, `ci/tooling/security-tools.lock.yml` und `docs/security/ci-security-tooling{,.de}.md` (#447). Vorhandene Commits belegen keine bestandenen Prüfungen.
- Diese Arbeit ergänzt das Übergabepaar, dauerhafte Übergaberegeln in `AGENTS.md`, einen lokalen `CLAUDE.md`-Einstieg und den [Change Record](../reports/audits/change-records/CR-20261114-ai-handoff-and-framework-pin.de.md).
- Das native `ci/tools/sync-framework-component-versions.py` synchronisierte Parent-Lock und 22 Workflow-Identitäten für den ausgewählten Framework-Commit. Ein unabhängiger Bytevergleich bestätigte, dass jede Workflow-Änderung nur die alte Framework-SHA durch die neue ersetzt; im Lock ändert sich nur `framework_sha`. Kein Connector-, Framework- oder MRTS-Quelltext wurde bearbeitet.

## Für den PR ausgewählte Änderungen

Die folgende ursprüngliche 30-Pfade-Auswahl wurde in `82472f02170c34183998780f8ab77b90a7c8a299` committet. Danach war der Arbeitsbaum sauber; diese Aktualisierung ändert nur Übergabe- und Change-Record-Paar für einen reinen Dokumentations-Folgecommit. Gestagte, ungestagte und neue Dateien vor weiterer Arbeit erneut prüfen.

| Pfad | Herkunft / PR-Inhalt |
| --- | --- |
| `.gitignore` | Vorhandene ungestagte Ergänzungen `.claude`, `.rtk`, `.aws`; zusätzliche abschließende Leerzeile während der PR-Vorbereitung für die Whitespace-Prüfung entfernt. |
| `AGENTS.md` | Drei dauerhafte Übergaberegeln; ursprüngliche Regeln erhalten. |
| `docs/AI-HANDOFF.md`, `docs/AI-HANDOFF.de.md` | Neues englisches/deutsches Übergabepaar, vor ausdrücklichem Staging unversioniert. |
| `modules/ModSecurity-test-Framework` | Vorhandene Checkout-Abweichung für den Parent-Commit ausgewählt: `62b411e073551ef0fef22ab3d372e2489f2ae168` nach `31531f74cfe26c2a40d4bb5f6eaae4c0920127e1`. |
| `ci/tooling/project-versions.lock.json`, 22 Dateien unter `.github/workflows/` | Erforderliche generierte Framework-Identitätsprojektionen, über ihren nativen Eigentümer synchronisiert. |
| `reports/audits/change-records/CR-20261114-ai-handoff-and-framework-pin.md`, `reports/audits/change-records/CR-20261114-ai-handoff-and-framework-pin.de.md` | Neues Change-Record-Paar aus der nativen Vorlage. |
| `CLAUDE.md` | Vorhandene ignorierte lokale Datei, um den Projektanweisungseinstieg ergänzt; ursprüngliche RTK-Hinweise erhalten. Vom PR ausgeschlossen und nicht durch einen normalen Clone übertragen. |

Framework ist auf `master` intern sauber; ausgewählt ist dessen bereits veröffentlichte Wartungsaktualisierung #170. MRTS bleibt bei `ee2174431c4edf97e66afe32558ce8454deb2397`, passend zum Framework-Gitlink. Kein verschachteltes Repository wurde gestagt oder committet. `CLAUDE.md` bleibt durch `.gitignore:50` ignoriert; keine Zugangsdatenablagen oder Anmeldekonfigurationsdateien wurden untersucht.

## Entscheidungen, verworfene Ansätze und offene Arbeit

- Dauerhafte Regeln gehören in `AGENTS.md`, wechselnder Arbeitsstand hierher. EN/DE-Begleiter, verpflichtendes RTK und Secrets-Prüfung vor Dateilektüre erhalten. `.codex/context/index.md` und geltende Verzeichnisanweisungen heranziehen.
- Ein reines Framework-Zeigerupdate wurde verworfen: Parent-Lock und Workflow-Identitäten müssen übereinstimmen. Der vorhandene Synchronisierer besitzt diese generierten Projektionen; keine manuellen Workflow-Änderungen oder abgeschwächten Gates.
- Frühere verworfene Produktansätze sind im verfügbaren Gespräch nicht belegt. Die historische Reparatur `prepare-reviewed-framework-handoff.py` wurde nicht verwendet, weil sie andere feste Revisionen adressiert.
- Die ursprüngliche globale Whitespace-Prüfung scheiterte an `.gitignore:55`; die PR-Vorbereitung entfernte diese Leerzeile. Hier wurde kein Produktfehler reproduziert.
- Keine Laufzeitqualifikation für den aktuellen HEAD oder Merge-Bereitschaft wird beansprucht. Der [Readiness-Bericht vom 2026-11-03](../reports/audits/change-records/CR-20261103-runtime-readiness-prerequisites.de.md) ist historischer Nachweis mit älteren Pins, kein frisches Ergebnis dieses Branches.

## Ausgeführte Prüfungen und Grenzen

**Behobene Auslieferungssperre:** Nach ausdrücklicher Nutzerfreigabe wurde eine operatorseitige Freigabe für den exakten ursprünglichen Worktree/Index/Gitlink installiert. Vollständige Secrets-Nachweise erfassen alle 2514 regulären Framework-Blobs und 9 reinen Git-Aliasse sowie alle 431 regulären MRTS-Blobs und 41 Aliasse; alle abgeschlossenen Scans bestanden. Der normale Git-Hook erzeugte danach `82472f02170c34183998780f8ab77b90a7c8a299`; die Arbeit wurde über [PR #449](https://github.com/Easton97-Jens/ModSecurity-conector/pull/449) ausgeliefert, später geschlossen und per Squash vom Task-Branch-Head `902eaa71382bdf471e3a22679be96f44168e5bdf` an `da212088f018b7852284768ced03feca286980ef` gemerged. Dieser Folgecommit korrigierte den CI-Pfadkonventionsfehler; Checks des aktuellen HEAD nach dem Merge wurden zurückgelesen.

| Befehl oder Vorgehen | Beobachtetes Ergebnis |
| --- | --- |
| `rtk bypass git status --short --branch --untracked-files=all`; Prüfung gestagter/ungestagter Diffs; `rtk bypass git submodule status --recursive` | Obige Identitäten und Änderungen untersucht; Framework intern sauber. |
| `rtk bypass git ls-remote https://github.com/Easton97-Jens/ModSecurity-conector.git refs/heads/master`; gleichwertige Framework-Remote-Abfrage | Exit 0; die beiden obigen Remote-master-Identitäten bestätigt. |
| `rtk bypass /usr/local/bin/sonar-with-env analyze secrets --stdin` für ausgewählte Anweisungs-/Quelltext-/Diff-/Dokumentationsbytes | Abgeschlossene ausdrückliche Scans mit Exit 0; rohe Ausgabe unterdrückt. Ein früherer Hook beim externen Prüfhelfer blieb unvollständig, gefolgt von einem erfolgreichen ausdrücklichen Scan. Keine Aussage zur Codequalität. |
| `rtk bypass python3 -B /var/tmp/codex/ModSecurity-conector/ai-handoff-20261114/validate_handoff.py` | Begrenzte ursprüngliche Übergabeprüfungen bestanden; ein vorheriger Fehler des deutschen Sprachumschalters/von vier Links war vor diesem Erfolg korrigiert. |
| Nativer Kandidatenprüfer vor/nach Synchronisation; nativer Synchronisierer `--check` und `--verify-primary` | Exit 0; Kandidat verifiziert, `changed=[]`, `FRAMEWORK_PRIMARY_VERIFIED`. Exakte Befehle stehen im Change Record. |
| `rtk make check-doc-links`; `rtk bypass git diff --cached --check` | Exit 0; Repository-Pfade, lokale Links und gestagter Whitespace sauber. |
| `rtk make check-bilingual-docs` | Nach 15 Minuten CPU-Arbeit in wiederholter Ignore-Pfadabfrage beendet; Exit 2 nach Abbruch, kein PASS. |
| `rtk bypass env CONNECTOR_REVISION=5672c5ff562495ddbc47a1932b1641e0073746f5 .venv/bin/python -B /var/tmp/codex/ModSecurity-conector/ai-handoff-pr-20261114/check_bilingual.py` | Exit 0, `bilingual docs ok`; alle vorhandenen Regeln/Auswahlen des vollständigen Prüfers erhalten, mit gleichwertigem indiziertem Ignore-Pfadprädikat. Kein Prüferquelltext geändert. |
| Native Change-Record-Archivprüfung | Exit 0; Strukturvertrag bestanden. |
| `rtk make check-variable-documentation` | Zunächst Exit 2; nach Pfadkorrektur über Repository-Variable Exit 0, 109 Referenzen. |
| `rtk bypass git commit -m 'Prepare AI handoff and synchronize Framework maintenance pin'` | Exit 1; pre-commit-Hook verweigerte den gestagten Gitlink: `No exact operator V2 admission for selected Gitlink`. In diesem ersten Versuch kein Commit erstellt. |
| `rtk bypass python3 -B /var/tmp/codex/ModSecurity-conector/ai-handoff-pr-20261114/operator_admission.py install --expected-plan-sha256 4da207519ebc4839396b5ea98de19b6db3b4bc5f747e98e0a4ca6ae1822dd362` | Exit 0; vom Nutzer autorisierte exakte Indexfreigabe nach vollständigen Quellen-/geschützten nativen Prüfungen installiert; bestehende Einträge und ausführbare Guards erhalten. |
| `rtk bypass git commit -m 'Prepare AI handoff and synchronize Framework maintenance pin'` | Folgeversuch mit Exit 0 durch den normalen Hook; erster 30-Dateien-Commit `82472f02170c34183998780f8ab77b90a7c8a299`. |
| `rtk bypass .venv/bin/python -I ci/tools/read-framework-revisions.py --parent-sha 82472f02170c34183998780f8ab77b90a7c8a299` | Exit 0; committete Framework-/MRTS-Pins stimmen mit den materialisierten Checkouts überein. |
| `gh` GitHub-CLI-Rückmeldung (`gh api` PR #449; `gh run list --branch master`) am gemergten HEAD `da212088f018b7852284768ced03feca286980ef` | PR #449 geschlossen/merged um 2026-11-14T10:45:17Z; Current-Head-CI-Rückmeldung: 17 Runs am Head, 16 abgeschlossen `success`, 1 noch `queued` (`Native target Sonar security`). |
| Übernahmesitzungs-Verifikation dieser Übergabeaktualisierung: `rtk make check-doc-links`; `rtk make check-variable-documentation`; bilingualer Adapter `check_bilingual.py` bei `CONNECTOR_REVISION=da212088f018b7852284768ced03feca286980ef`; `rtk bypass git diff --check`; Secrets-Rescan beider Übergabedateien; native Pin-Prüfung `read-framework-revisions.py --parent-sha da212088f018b7852284768ced03feca286980ef` | Alle Exit 0; `doc links ok`; `variable documentation: PASS (109 documented variable references scanned)`; `bilingual docs ok`; Whitespace sauber; Pins stimmen überein (`framework_sha` `31531f74cfe26c2a40d4bb5f6eaae4c0920127e1`, `mrts_sha` `ee2174431c4edf97e66afe32558ce8454deb2397`). Gewöhnliches volles `make check-bilingual-docs` in dieser Sitzung nicht erneut ausgeführt; dokumentierter historischer CPU-bound Abbruch oben erhalten. |

Den ersten Vorlagenaufrufen fehlten explizite Framework-Umgebung/Importpfade; der erfolgreiche native Aufruf setzte beides. Der Kandidatenprüfung mit System-Python fehlte `yaml`; mit der Repository-`.venv/bin/python` bestand sie. Der erste Synchronisiereraufruf verweigerte eine Eingabe außerhalb seines erlaubten temporären Wurzelverzeichnisses; mit dem aufgabeneigenen `RUNNER_TEMP` bestand er ohne Lockerung der Pfadprüfungen.

Gehostete CI bei `9bb05b578275d918f095e2a3a977e59a3e3ea405` fand das maschinenspezifische Checkout-Literal der Übergabe in [test-apache](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/43584116251). `rtk make check-variable-documentation` reproduzierte lokal Exit 2; der Ersatz durch `$CONNECTOR_ROOT` in beiden Übergaben ergab Exit 0 (109 Referenzen). Gehostetes `make check-bilingual-docs` bestand an diesem historischen HEAD. Frische CI für den späteren Korrekturcommit gesondert abfragen.

Der erste große Quellenbatch lief in eine Zeitüberschreitung (Exit 1); sein gesamter Inhalt wurde vor Ausgabe der vollständigen Nachweise erfolgreich in kleineren vollständigen Blob-Batches erneut geprüft. Zwei große Git-Blobs wurden tatsächlich über ganze Dateien geprüft; keine Quellbytes ausgelassen. Die Prüfung mit verkürzter Parent-SHA wurde abgewiesen (Exit 1); der obige Aufruf mit vollen 40 Zeichen bestand.

**Nicht ausgeführt:** Produkt-Builds, `quick-check`, `test`, Host-/Konfigurations-/Laufzeitprüfungen, Cloud Quality Gate, gewöhnliches volles `make check-bilingual-docs` (dokumentierter historischer CPU-bound Abbruch; bilingualer Adapter-Äquivalent bestand oben). Current-Head-CI am gemergten Commit wurde zurückgelesen (siehe Tabelle); ältere Ergebnisse qualifizieren keinen neueren Commit.

## Aus dem Repository ermittelte Start-, Build- und Testbefehle

Die folgenden Referenzen sind keine ausgeführten Produkttestergebnisse. Vom Parent-Root mit den ausgewählten Voraussetzungen aus [Erste Schritte](getting-started.de.md) und externen beschreibbaren Build-/Laufzeitpfaden aus `.codex/config.toml` ausführen.

| Zweck | Befehl / Quelle |
| --- | --- |
| Framework-Verzeichnis / aktive Auswahl | `rtk make check-framework`; `rtk make check-active-inventory` — Root-`Makefile`, `README.md`. Verzeichnisexistenz belegt keine Pin-Gleichheit. |
| Schnelle Checks / Standardtests | `rtk make quick-check`; `rtk make test` — Root-`Makefile`, `README.md`; einfaches `make` führt standardmäßig `test` aus. |
| NGINX-Build / Konfiguration | `rtk make build-nginx BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/build`; `rtk make check-config-nginx BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/build` — `docs/getting-started.md`. |
| Dokumentation | `rtk make check-bilingual-docs`; `rtk make check-doc-links` — `README.md`, delegierte Framework-Targets. Ausgewählte neue Dateien vor Prüfungen mit Auswahl versionierter Dateien stagen. |
| Envoy-ext_proc-Dienst | `rtk make -C connectors/envoy serve-envoy-ext-proc BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/build EXT_PROC_RULES_FILE=/absolute/path/to/reviewed/rules.conf` — `connectors/envoy/Makefile`. Regelpfad durch eine vorhandene geprüfte Datei ersetzen; benötigt Go/CGo/libmodsecurity-Eingaben. Startet den Dienst, nicht den Envoy-Host. |

## Nächste Schritte

1. `AGENTS.md`, geltende Verzeichnisanweisungen und diese Übergabe lesen; Branch/HEAD, gestagte/ungestagte Dateien sowie Framework-/MRTS-Identitäten abgleichen. Diese Sitzung schloss die Abgleichung ab: Branch `master`, HEAD `da212088`, sauberer Baum, Framework `31531f74…`, MRTS `ee21744…`.
2. Vorhandenen PR des Task-Branches und Prüfungen seines aktuellen HEAD prüfen; nur bei Bedarf veröffentlichen/einen Draft-PR öffnen. Erledigt: [PR #449](https://github.com/Easton97-Jens/ModSecurity-conector/pull/449) ist geschlossen und an `da212088f018b7852284768ced03feca286980ef` gemerged; Current-Head-CI wurde zum Merge-Zeitpunkt zurückgelesen; kein Draft-PR blieb zu veröffentlichen. Erfasste lokale Ergebnisse und Grenzen erhalten.
3. Das nächste konkrete Produktziel festlegen. Betroffenen Quelltext untersuchen und nur relevante Prüfungen auswählen; archivierte I12-/Matrix-Kampagnen ohne ausdrücklichen Auftrag nicht wieder aufnehmen. Offen: Es wurde in dieser Übernahmesitzung kein neues vom Nutzer gewähltes Produktziel festgelegt.
4. Tatsächliche Ergebnisse und verbleibende Lücken vor dem nächsten Codex-/Claude-Code-Wechsel in beiden Übergabefassungen erfassen. Die ignorierte lokale `CLAUDE.md` bei einem Workspace-Wechsel gesondert erhalten. Mit dieser Aktualisierung erledigt; beide Sprachfassungen wurden synchronisiert und in dieser Sitzung mit dem bilingualen Check verifiziert.
