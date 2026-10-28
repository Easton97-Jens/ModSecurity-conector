# Change Record: CR-20261028-submodule-inventory-publication

**Sprache:** [English](CR-20261028-submodule-inventory-publication.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261028-submodule-inventory-publication |
| Datum (UTC) | 2026-10-28 |
| Basis-Revision | `cef2ab5ee8fe35e316620acbee5d9eb2f0f73bf3` |

## Motivation und Problemstellung

PR #429 änderte Framework-Gitlink und zentralen Lock, ließ aber die Inventar-Begleitdateien aus. Seine Zulassung unter Python 3.15.1 scheiterte vor Ausführung ausgewählter Prüfungen mit reviewed source digest mismatch für ci/tooling/project-versions.lock.json. Der Publisher selbst war in Lauf 40671467579 erfolgreich. Der Benutzer beauftragte die Reparatur des offenen PRs und des Erzeugers.

## Akzeptanzkriterien

PR #429 ohne Änderung der Fall-/Selektor-/Profil-/Quellmitgliedschaft reparieren. Exakt zwei Begleitdateien atomar mit festen primären Zielen synchronisieren. Vollständige primäre und abgeleitete Bytes vor dem Staging unabhängig aus dem vertrauenswürdigen Master und danach aus Stage-zero-Blobs rekonstruieren. Gefälschte Metadaten, veraltete Quellbindungen und unsichere Begleitdateimodi ablehnen; Rollback und vorhandene Branch-Identitäts-/Historienregeln erhalten.

## Implementierungsentscheidung und Begründung

Der Synchronisierer verwendet die vollständige Inventarzulassung und feste Begleitdateiableitung wieder. Seine bestehende Transaktion umfasst Ersetzungen der Begleitdateien und erneute Zulassung nach dem Schreiben. Die unabhängige Rekonstruktion mit --verify-companions --base beweist zuerst die vollständigen registrierten primären Bytes, danach die exakten abgeleiteten Begleitdateibytes; --staged prüft reguläre 100644-Stage-zero-Blobs. Vorhandene source_sha256-Felder des Archivs dürfen nur nachgewiesenen Änderungen fester primärer Testquellen folgen; inventory_sha256 folgt dem generierten Inventar. Definitionen und Auswahlmetadaten bleiben unverändert. Der Workflow ergänzt nur die zwei festen Pfade und einen strikten 100644/M-Zweig im Raw-Diff-Vertrag.

## Geänderte Dateien

ci/tools/sync-framework-component-versions.py; tests/test_update_framework_versions.py; .github/workflows/update-submodules.yml; tests/test_ci_security_workflows.py; config/testing/active-cases.json; reports/testing/test-selection-archive.generated.json; docs/build/README.md und docs/build/README.de.md; dieses Change-Record-Paar. Der getrennte Reparatur-Commit cef2ab5ee8fe35e316620acbee5d9eb2f0f73bf3 in PR #429 enthält nur die zwei generierten Begleitdateien.

## Ausgeführte Befehle

Alle Projekt-Shell-Befehle verwendeten das aufgabeneigene RTK v1.0.1 bypass mit isolierten Daten-/Konfigurations-/Temp-Verzeichnissen. Unter Python 3.15.1 bestand ci/tools/run-active-tests.py --check für den reparierten PR #429: 100 Standardfälle und 1893 auf Abruf. ci/tools/update-test-archive.py --check und git diff --check bestanden. Zwei gezielte Workflow-Tests bestanden, einschließlich echter Shell-Ausführung von Allowlist und Raw-Diff-Vertrag mit zulässigen Begleitdateien und abgelehnten ausführbaren/Symlink-/Add-/Delete-/unregistrierten Varianten. Die neue Regression lehnte das zulässige Update mit dem ursprünglichen Workflow ab. Der Hauptagent führte am integrierten Tree frisch 41 Tests aus (39 Synchronisierer-Tests plus die zwei Workflow-Tests); alle bestanden in 48.691s. Vollständige Inventarzulassung, natives Archiv --check, zweisprachige Dokumentation, Variablenreferenzen (103), Repository-/Dokumentationslinks, Change-Record-Struktur und Whitespace bestanden. Die Backend-Regression scheitert gegen den alten Synchronisierer ebenfalls gezielt wegen der fehlenden Begleitdateien.

## Security-Auswirkung

Der Publisher verarbeitet statisch geparste Candidate-Daten und vertrauenswürdigen Master-Code. Neue Begleitdateibefugnisse bleiben auf zwei vorhandene reguläre Dateien, exakte Ableitung aus vertrauenswürdiger Basis und unveränderte Auswahl/Metadaten begrenzt. Atomarer Rollback und Schutz konkurrierender Änderungen bleiben aktiv. Validator-Isolation, Berechtigungen, Zugangsdaten, Candidate-Ausführung, Ref-Gates, Auto-Merge-Verbot und die Regel für exakt einen Updater-Commit eines offenen Branches bleiben unverändert.

## Runtime-Evidence

Die ursprüngliche Ablehnung einer veralteten Bindung wurde am PR-Head 7bfe28818bff8319a77693254d49b6053231d8e4 reproduziert und tritt nach Reparatur cef2ab5ee8fe35e316620acbee5d9eb2f0f73bf3 nicht mehr auf. Dies ist Inventar-/Veröffentlichungs-Evidence, keine Connector-Runtime- oder I12-Qualifizierung. Neue gehostete CI-Ergebnisse bleiben an ihren tatsächlichen Head gebunden.

## Bekannte Einschränkungen

Der reparierte offene PR #429 hat einen zusätzlichen geprüften Commit. Sein Branch bleibt gemäß bestehender Regel für exakt einen Updater-Commit bis zur geprüften Integration absichtlich von automatischer Wiederverwendung als offener Branch ausgeschlossen. Diese Reparatur autorisiert keinen Merge. Eine vollständige gehostete Updater-Veröffentlichung mit der dauerhaften Korrektur benötigt Integration des vertrauenswürdigen Publisher-Codes.

## Verbleibende Risiken

Ein neuer gehosteter Lauf kann einen späteren unabhängigen Fehler aufdecken; keiner wird stillschweigend akzeptiert. Exakte Byte-Rekonstruktion und Stage-zero-Prüfungen lehnen konkurrierende Abweichungen absichtlich ab, statt sie zu überschreiben. Framework und MRTS bleiben für diese Aufgabe getrennte schreibgeschützte Repositories.

## Nicht ausgeführte Prüfungen mit Begründung

Keine neue All-Connector-Matrix, I12-Kampagne oder breite Security-Prüfung wurde gestartet. Gehostete Runtime, Sonar und Merge-Bereitschaft werden nicht aus lokalen Fixture- oder Inventarerfolgen abgeleitet. Erforderliche Head-gebundene CI bleibt ein separates Delivery-Kriterium.

## Finaler Diff- und Review-Status

Die unmittelbare PR-Reparatur wurde aus der vertrauenswürdigen Basis b8f76fd718bf26dd3a4345dd6700534690d8a49d abgeleitet; lokaler und veröffentlichter Tree 65236d801b1bc73bb74de9cd57591e1034f9d9b0 stimmten überein. Das unabhängige finale Quell-/Workflow-Review fand keinen materiellen Blocker. Ein frischer vollständiger Parent-Checkout an 7eb41bb805c6c3d07244af2068d6db9930740bdc führte den echten Framework-Wechsel von 99a7985c1be92a2297b1b59208f64df6768f2cbf auf 3a4f2281568139d94fda6b51dc2e07bb8fc06c67 über die öffentliche CLI aus: --sync änderte nur zentralen Lock und zwei Begleitdateien, --check und natives Archiv --check bestanden, und --verify-companions --base bestand vor sowie nach explizitem Staging mit --staged. Die dauerhafte Publisher-Korrektur wird direkt in den reparierten PR #429 aufgenommen, damit beide Inventaränderungen gemeinsam geprüft, getestet und integriert werden. Diese Änderung autorisiert keinen Merge.
