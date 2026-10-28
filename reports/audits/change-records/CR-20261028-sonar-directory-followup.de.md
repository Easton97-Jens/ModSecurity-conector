# Change Record: CR-20261028-sonar-directory-followup

**Sprache:** [English](CR-20261028-sonar-directory-followup.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261028-sonar-directory-followup |
| Datum (UTC) | 2026-10-28 |
| Basis-Revision | `c5993ed9a7b59fc0bd58f105595ec79f596c88d6` |

## Motivation und Problemstellung

Die aktuelle Hauptanalyse von Sonar an dieser Basis meldet 15 Befunde in `ci/` und 35 in `connectors/`: 13 Security-Meldungen und 37 Pointer-to-Const-Vorschläge. Der Nutzer hat die sechs `tests/`-Befunde ausgenommen. Dies sind verbliebene Kandidaten nach dem gemergten PR #430. Frische Funktions-/Flussprüfung belegte keinen neuen Exploit oder korrigierbaren privaten Const-Parameter. Das Master-Gate ist ERROR, weil `new_security_rating=5` den erforderlichen Höchstwert `1` übersteigt; sein New-Code-Zeitraum beginnt am `2026-05-14T18:30:31+0000`.

Der Fallberichtsschreiber prüft einen Runtime-Pfad und veröffentlicht JSON anschließend direkt. Ein Veröffentlichungsfehler erhält dadurch nicht die atomare Ersetzungsgarantie des vorhandenen gemeinsamen Schreibhelfers. Diese Änderung übernimmt diesen etablierten Helfer und dokumentiert die übrigen Kandidaten ohne Sonar-Statusänderung.

## Akzeptanzkriterien

Exakte erfolgreiche JSON-Bytes, Schema, Dateinamen und gültige Zielpfade erhalten. Fehlgeschlagene atomare Veröffentlichung muss den vorherigen Bericht erhalten und temporäre Ausgabe entfernen. Den vorhandenen privaten, deskriptorgebundenen No-Follow-Schreiber verwenden. Host-ABI, unterstützte Operator-Pfadwahl, Validierung, Regeln/Gates und unveränderte aktive Auswahl erhalten. `tests/`-Befunde außerhalb des Korrekturumfangs und alle Sonar-Serverstatuswerte unverändert lassen. Einen neuen Draft-PR liefern; die Cloud muss den Scannereffekt unabhängig feststellen.

## Implementierungsentscheidung und Begründung

`write_json()` delegiert an `write_runtime_artifact_text_atomic()` mit demselben sortierten, um zwei Leerzeichen eingerückten JSON plus abschließendem Zeilenumbruch und dem bisherigen Ausgabelabel. Dieser Helfer prüft den Runtime-Pfad, weist unsichere Objekte durch deskriptorgebundene Prüfungen zurück, schreibt eine private temporäre reguläre Datei mit `0600`, führt Flush/Fsync aus und ersetzt das Ziel atomar. Die doppelte Pfadprüfung im Wrapper entfällt; andere Aufrufer behalten ihren bisherigen Import/Gebrauch.

Dies ist eine echte Verbesserung der Artefaktveröffentlichung, kein behaupteter Exploit-Fix. Sie adressiert die zwei mehrdeutigen Meldungen `pythonsecurity:S2083` / `pythonsecurity:S8707` an Basiszeile85. Die übrigen 48 Kandidaten sind ausschließlich dokumentiert: 37 erforderliche API-/Stub-Parametersignaturen und 11 geprüfte CLI-/Pfad-/Inhaltsflussmeldungen. Pointee-Const würde Host-/Native-Callbackdeklarationen verletzen; willkürliche Einschränkungen ausdrücklich gewählter Operator-Pfade würden unterstütztes Verhalten ändern. Git `-C` wurde nicht auf `cwd` geändert, weil das den gemeldeten geprüften Revisionsfluss nicht adressieren würde.

## Geänderte Dateien

`ci/runtime/lifecycle/run-verified-case.py`, `config/testing/active-cases.json`, `reports/testing/test-selection-archive.generated.json`, `reports/audits/sonar-directory-followup-20261028.json`; dieser Record und sein englischer Begleiter. Das JSON erfasst alle 50 Basispositionen mit einzelnen Quellcode-Gegenbelegen; es sind Reviewdaten, kein Nachweis serverseitiger Schließung. Ein geprüfter Quelldigest ändert sich; Ausführungen und archivierte Selektoren bleiben identisch. Das Archiv wird durch `ci/tools/update-test-archive.py` regeneriert.

## Ausgeführte Befehle

- PASS: authentifizierter Read-only-Abruf von Hauptanalyse/Befunden/Hotspots/Verzeichnismetriken/Gate durch RTK und `/usr/local/bin/sonar-with-env`; vollständiges Inventar mit 59 Befunden, 50 ausgewählte Positionen, null Hotspots, exakte Basisrevision.
- PASS: frische native Signatur-/Registrierungsprüfung und Python-Quellcode-/Flussprüfung. Eine dynamische Revisionskontrolle wies 12 ungültige Werte vor Lock-/Git-I/O zurück und erhielt einen gültigen 40-Hex-Wert.
- Erwartetes Basis-FAIL / geändertes PASS: externe atomare Veröffentlichungskontrolle. Beide erhalten exakte normale JSON-Bytes; der neue Schreiber propagiert injizierten Veröffentlichungsfehler, erhält den alten Bericht, bereinigt temporäre Ausgabe und verwendet `0600` statt bisher `0644`.
- PASS: `rtk bypass python3.15 ci/tools/run-active-tests.py --check`; 100 aktive Fälle / 80 Ausführungen, 1.893 On-demand-Fälle getrennt, unveränderte Auswahl.
- PASS: vorhandene `runtime-path.python-allowed` und `runtime-path.python-blocked` durch den aktiven Runner mit explizitem Python3.15 und externem `RUNNER_TEMP` / privatem Ausgabeverzeichnis. Der erste Aufruf ohne vorhandenes Ausgabeverzeichnis wurde vor Ausführung zurückgewiesen; korrigierte Vorbereitung bestand beide Fälle.
- PASS: `rtk bypass python3.15 ci/tools/update-test-archive.py` und `--check`; nur die geprüfte Quellbindung und abgeleitete Archivdigests ändern sich.
- PASS: `rtk make check-bilingual-docs PYTHON=/usr/local/bin/python3.15`, `rtk make check-doc-links PYTHON=/usr/local/bin/python3.15 FRAMEWORK_ROOT=<task-worktree>/modules/ModSecurity-test-Framework`, `rtk bypass python3.15 ci/tools/new-change-record.py check`, Quellcodesyntax, vorgemerktes `git diff --check` und Standard-Gitleaks8.30.1-Scan der vorgemerkten Änderungen mit `--redact=100`. Die anfängliche deutsche Sprachumschalterformatierung wurde zurückgewiesen und korrigiert; beide Dokumentationsprüfungen bestanden danach. CI/Cloud am aktuellen Head benötigt noch terminalen Abruf.

## Security-Auswirkung

Erhält die Runtime-Containment-Grenze und ergänzt Veröffentlichungs-/Deskriptorschutz des gemeinsamen Schreibhelfers. Alle 13 anfänglichen Security-Meldungen wurden gegen tatsächliche Eingaben, Prüfungen und Senken nachgeprüft; kein neu ausnutzbarer Fluss wurde belegt. Das Review ist auf diese Positionen begrenzt. Keine Sonar-Status-/Regel-/Gate-/Analyseumfangsänderung, Unterdrückung, Risikoakzeptanz, Abhängigkeitsaktualisierung oder ABI-Änderung.

## Runtime-Evidence

Die kontrollierte Dateiveröffentlichungsprobe und zwei vorhandene Runtime-Pfadfälle sind lokale Evidence für diese Grenze. Sie qualifizieren keine gehosteten Connectoren oder eine I12-Runtime-Matrix.

## Bekannte Einschränkungen

Lokales Python ist 3.15.2; CI pinnt 3.15.1. Keine Toolchaininstallation. Erst eine frische Cloud-Analyse zeigt, ob die zwei direkten Schreibmeldungen verschwinden; die übrigen 48 dokumentierten Kandidaten werden nicht als behoben oder geschlossen behauptet. Der Fehler des ursprünglichen Master-Gates wird nicht in PASS umgedeutet.

## Verbleibende Risiken

Der Nutzer hat gewählt, Fehlalarm-Kandidaten dokumentiert und serverseitig offen zu lassen. `tests/`-Befunde sind aus dieser Aufgabe ausgenommen, ohne Ausschluss in der Analysekonfiguration. Ein grünes Changed-Code-PR-Gate belegt kein bereinigtes Master-Inventar und löst keine unveränderten Basiskandidaten. Fehlgeschlagene Veröffentlichung wird durch kontrollierte Injektion geprüft, nicht durch eine vollständige Crash-/Stromausfallkampagne.

## Nicht ausgeführte Prüfungen mit Begründung

Keine vollständige Standardsuite, zusätzliche historische/I12-Kampagne, All-Connector-Runtime-Matrix, Deployment oder Merge. Nur die betroffene Dateigrenze und vorhandene aktive Fälle wurden ausgewählt. Kein nativer Code änderte sich; daher war kein neuer lokaler nativer Build erforderlich. Framework wird ausschließlich für Parent-Dokumentationsvalidierung am vorhandenen exakten Gitlink bereitgestellt; keine Framework-/MRTS-Quellcode- oder Lieferänderung.

## Finaler Diff- und Review-Status

Die gezielte Quellcodeänderung ist geprüft und eingefroren. Unabhängige native/Python-Triage und Code-/Dokumentationsreview sind ohne konkrete Regression abgeschlossen. Lokale atomare Schreibprobe, zwei aktive Fälle, Zulassung/Archiv, Dokumentations-/Link-, Syntax-, vorgemerkte Whitespace- und Secret-Prüfungen bestehen. Neue CI-/Cloud-Ergebnisse am exakten Head sind im PR abzurufen; Ergebnisse alter Heads werden nicht wiederverwendet. Kein Merge ist autorisiert.
