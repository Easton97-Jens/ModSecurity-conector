# Änderungsnachweis: CR-20261015-i12-measurement-compatibility

**Sprache:** [English](CR-20261015-i12-measurement-compatibility.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261015-i12-measurement-compatibility |
| Datum (UTC) | 2026-10-15 |
| Basis-Revision | `f27eb59b53beff6f65384fc2e5037881a3052c01` |

Eigentümer: Parent-PR #410.

## Motivation und Problemstellung

Scaffold-Job116469396655 von PR #412 scheitert am Distributions-SDK: Die deterministische Constructor-Fixture deklariert eine konstante ID, deren ausgewählter Header eine veränderliche ID deklariert; die APR-Probe ruft außerdem einen dort fehlenden Intervention-Cleanup-Helfer auf. Weitere Kompatibilitätskontrollen zeigen, dass die aktuelle Common Runtime den freigegebenen neueren SDK benötigt. Lint muss diesen SDK über den vorhandenen gemeinsamen Komponentenproducer vorbereiten.

## Akzeptanzkriterien

Strenge Compilerwarnungen und alle bestehenden Negativkontrollen erhalten. Fixture-Signatur gegen den tatsächlichen Header kompilierend bestimmen. Aufruferseitige Intervention-Strings der Probe über die portable C-Allokations-API freigeben. Den Hostqualifizierer nur um seinen vorhandenen direkten SDK-MIME-Producer ergänzen. Ursprüngliche Parserauswahlen getrennt qualifizieren, ohne HTTP-/Native-Lifecycle-Belege zu erfinden.

## Implementierungsentscheidung und Begründung

Lint verwendet `prepare-runtime-components` mit Ziel `shared` und dessen exakten Umgebungssnapshot über den vorhandenen geprüften Wrapper `with-runtime-components.sh`. Damit bleiben Ziel-/Cache-Prüfungen erhalten und ein neues dynamisches Source-Fragment im Workflow entfällt. Bestehende Framework-Pins bleiben verbindlich. Constructor-Probes bewahren Eingaben, Compiler-Argumente und Diagnosen. MIME erlaubt `native_api`; Transportbelege bleiben dafür ungültig. `reviewed_configuration_packet` akzeptiert ausschließlich ursprüngliche `actual_configtest`-Verträge mit unabhängig gebundenen Parser-/Image-/Konfigurations-/Quell-/Cleanup-Belegen und liefert immer `full_lifecycle_qualified: false`.

## Geänderte Dateien

Lint-Workflow, Native-Observer-Testfixture, unabhängige APR-Probe, gemeinsamer Lifecycle-Qualifizierer und Negativkontrollen. Produktquellen, unveränderliche Capture-Objekte/Manifest sowie Framework-/MRTS-Gitlinks bleiben unverändert.

## Ausgeführte Befehle

Alle lokalen Befehle liefen über RTK. Explizit ausgewählter SDK3.0.14: Observer-Suite33 PASS. Gemeinsame Oracle-/Ledger-/Report-Suite34 PASS. Echte APR-/Native-Probe4 PASS. Eine synthetische ältere Headerumgebung reproduziert zusätzliche Inkompatibilitäten der aktuellen Runtime und bleibt als Fehlerbeleg erhalten; sie ist kein Runtime-PASS eines älteren SDK. Hosted-Provisionierung und finale Head-Prüfungen sind nach Veröffentlichung zu beobachten.

## Security-Auswirkung

Keine Warnung, Prüfung, Quality Gate, Isolation oder Provenienzgrenze wird abgeschwächt. Abhängigkeiten entstehen im bestehenden externen runner-eigenen Cache. Parserqualifikation kann keine HTTP-/Body-Pflicht ersetzen. Synthetische Validator-Unitfixtures sind keine Hostevidenz.

## Runtime-Evidence

Run `i12-lighttpd-412-completion-20261015`, Verzeichnis `shared`, bewahrt ursprüngliches CI-Log, Header-Probes, Compile-/Runtime-Receipts und erfolgreiche wie fehlgeschlagene Prüfungen. Diese Messkontrollen allein erzeugen keinen Connector-Lifecycle-PASS.

## Bekannte Einschränkungen

Finale Hosted-SDK-Vorbereitung und Head-gebundene Sonar-/CI-Ergebnisse stehen aus. Die Stringfreigabe betrifft ausschließlich Testprobes. Produktkompatibilität mit älteren SDK-Versionen wird nicht ergänzt.

## Verbleibende Risiken

Die gemeinsame SDK-Provisionierung verlängert Lint; der terminale Hosted-Lauf muss die Runner-Abhängigkeiten bestätigen. Parser-PASS gilt ausschließlich für die Konfigurationsebene.

## Nicht ausgeführte Prüfungen mit Begründung

Keine lokale Paketinstallation, Veröffentlichung eines Releases, Deployment, Master-Integration oder andere Connector-Hostmatrix. Der netzabhängige Workflow-Build wird nach Veröffentlichung im Hosted-Lauf geprüft.

## Finaler Diff- und Review-Status

Der begrenzte Quelldiff erhält ursprüngliche physische Producerrollen und Baseline-Exporte. Der lighttpd-Folgeauftrag übernimmt diese gemeinsamen Korrekturen regulär aus #410; keine Historienumschreibung ist autorisiert.
