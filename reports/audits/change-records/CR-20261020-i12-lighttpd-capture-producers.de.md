# Change Record: CR-20261020-i12-lighttpd-capture-producers

**Sprache:** [English](CR-20261020-i12-lighttpd-capture-producers.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261020-i12-lighttpd-capture-producers |
| Datum (UTC) | 2026-10-20 |
| Basis-Revision | `eef8c1b432c0ce372c551a32fa6977cf4633b6c3` |

## Motivation und Problemstellung

Die ursprünglichen Stock-Sidecar153-, Patched-Native116- und diagnostischen Stock-Native78-IDs benötigen physische Hostmessungen und unabhängig geprüfte Qualifizierung. Capture-Erfolg allein belegt keine Abnahme. Diese Änderung macht lighttpd-spezifische Producer und aktuelle Provenienz prüfbar, ohne Baseline-Inventuren oder gemeinsame Validatoren zu ändern.

## Akzeptanzkriterien

Alle347 Original-IDs und ursprünglichen51/52/23 Oracle-Inventuren erhalten. Client-/Backend-/Host-/Native-/Log-/Cleanup-Messungen an exakte Packet-/Oracle-Vorschläge und unabhängige Root-Prüfung binden. Diagnostische Konfigurations-/Headerabnahme von verpflichtendem Body-Lifecycle trennen. Kopierte Receipts, veraltete Quellenbindung und unbelegte Strict-Abort-Aussagen zurückweisen. Private0700-Verzeichnisse/0600-Dateien und tatsächliche UID65534-Provenienz erhalten.

## Implementierungsentscheidung und Begründung

Routenspezifische Module trennen Capture-Erstellung, Transportbeobachtung, Konfigurationsfälle, Packet-Erstellung und Qualifizierungsvorschläge. Stock behält technische Spool-/Sink-Fehlerursachen und Wiederzulassung. Patched misst tatsächliche native Request-/Response-Hooks und Transportabschluss. Diagnose modelliert unterstützte P1-/Konfigurations-/Technikkontrollen einschließlich separat freigegebener Pre-Native-Zurückweisungen; sie erzeugt keine Body-Streaming-Fähigkeit. Der diagnostische Auditfallback akzeptiert nur ein exaktes Regeltoken innerhalb des ausgewählten Haupttransaktionssatzes. Physische Observer und begrenzte Fehlerfixtures dienen nur Tests. Vorhandene gemeinsame Validatoren qualifizieren erst nach exakter Root-Prüfung.

Der Qualifizierungsadapter löst externen Speicher verzögert nur über ein ausdrücklich gesetztes `I12_TEST_ROOT` auf; der Import benötigt kein vorab vorhandenes festes `/var/tmp/codex`. Tatsächliche Speichernutzung prüft Eigentümer und Schreibrechte. Artefakt-/Current-Ledger-Verbraucher behalten diese Kontrolle und unterstützen frische Runner, ohne die Evidenzpfadprüfung abzuschwächen oder ein allgemeines temporäres Verzeichnis als Evidenzspeicher zu behandeln.

## Geänderte Dateien

Unter `ci/runtime/lifecycle/i12/lighttpd/`: `stock_capture.py` und Stock-Helfer für Konfiguration/Inventur/Client/Spool/Floor/Packet/Qualifizierung/Transport/Fehler; `patched_capture.py`, `patched_qualification.py` und native SDK-/Transport-/Fehlerobserver; `diagnostic_capture.py` und Diagnosehelfer für Konfiguration/Abdeckung/Szenario/Native/Pre-Native/Packet/Transport/Fehler sowie Oraclefixtures; `qualification.py`, `current_ledger.py` und `artifact.py`. Fokussierte `tests/test_lighttpd_i12_*.py`-Kontrollen prüfen diese Pfade.

Die Dokumentation umfasst dieses EN/DE-Paar und das Paar [aktuelle Evidenz](../../testing/lighttpd-i12-20261015/current-evidence.de.md). Generierte Ledger und Zusammenfassung unter `reports/testing/lighttpd-i12-20261015/current-20261020/` stammen aus dem lighttpd-Exporter. Produktfixes bleiben auf bestehendem#382, gemeinsame Änderungen auf#410. Zentrale Matrix, gemeinsame Generatoren, Framework/MRTS und andere Connectoren werden nicht geändert.

## Ausgeführte Befehle

Der native Scaffold-Befehl bestand: `rtk proxy /usr/local/bin/python3 ci/tools/new-change-record.py create --name i12-lighttpd-capture-producers --base-revision eef8c1b432c0ce372c551a32fa6977cf4633b6c3 --date 2026-10-20`. Die Qualifizierungswiederholung mit aktuellen Quellen akzeptierte168 exakte Originale vor dem Export. Die unabhängige vollständige Inventurprüfung prüfte347 Zeilen und6214 physische Referenzen; ein separater privilegierter Lesezugriff prüfte24 private UID65534-Dateien ohne Rechteänderung.

`rtk proxy /usr/local/bin/python3 ci/tools/new-change-record.py check` bestand den Archivstrukturvertrag. Die fokussierte `test_lighttpd_i12_*.py`-Suite bestand99 Tests. Eine unabhängige Prüfung aller36 ausgewählten Diagnosequalifizierungen bestätigte für alle15 regeltragenden normalen Hostfälle exakte physische Haupttransaktionsereignisse ohne benötigten Auditfallback. Die15 Sonar-Reliability-Vertragstests bestanden mit einem vorhandenen privaten `TMPDIR`. `rtk make check-bilingual-docs`, `rtk make check-doc-links` und `rtk git diff --check` bestanden. Manueller EN/DE-Abgleich bestätigte gleiche Prüfumfänge, Zahlen, Revisionen und Einschränkungen.

## Security-Auswirkung

Begrenzte Funktions-/Regressionsarbeit bleibt im Blue-Umfang des Benutzers. Kein Tiefenscan, Exploit, zusätzliche externe Ziele, abgeschwächte Isolation oder Quality Gates. Root- und UID65534-Läufe bleiben getrennt. Private Dateien behalten0600, Spoolverzeichnisse0700. Technische Erschöpfung bleibt ein technischer Fehler, niemals eine erfundene native `BODY_LIMIT`-Entscheidung. Verzögerte Speicherauflösung erhält Eigentümer-/Rechtekontrollen bei Nutzung.

## Runtime-Evidence

Aktuelle Qualifizierung ist168 PASS: Stock60, Patched72 und Diagnose36 (28 Host- und8 Parserkontrollen). Tatsächliche Ausführungen sind jeweils128 HTTP,112 HTTP sowie69 HTTP plus8 Parser. Der Capture-Index mit347 Zeilen vergibt keine PASS. Aktuell unqualifiziert sind92/44/42 gemäß historischer/aktueller Vereinigung; ursprüngliche weiter offene Oracles sind17/13/19. Neu qualifizierte IDs sind59/70/35, neu geklärte ursprüngliche Oracles32/37/4. Generierte Routenledger erhalten quellenspezifische offene Gründe.

Sechs Produktfixes sind normal von#382 über#410 integriert. Fix `c523dce9966b47bc8be6efe39ee49f2d88de3397` schließt die Umgehung der Antwortprüfung durch Splice/Sendfile. Frische UID65534-Evidenz misst1,050,657 Antwortbytes über Native/Host/Client/Backend und ein EOS. Fünf P3-Zurückweisungen liefern403/158 Bodybytes; neun betroffene Antwortfälle wurden wiederholt. Reject behält `runtime_finish=0`, `common_finish=2` und Logging/Free/Destroy jeweils1. Der Export bindet Produkt `12cc380c3749fd76c246c05ce479f51446127880`, Basis `a62296fb57263f9be18c6ac879e36e0ab2a9935c` und Integration vor Produceränderungen `eef8c1b432c0ce372c551a32fa6977cf4633b6c3`.

Das [aktuelle Evidenz-Prerelease](https://github.com/Easton97-Jens/ModSecurity-conector/releases/tag/evidence-i12-lighttpd-pr412-20261020-current) zielt auf den veröffentlichten Quell-Head `2008b875f1860774627878051582b607f835b019`. Die Archiv-SHA256 ist `c7dccdfd5bb1c69029eb92864a5c9b62bd06e24a9a2466183c7f40ddc281d1bf`, die Manifest-SHA256 `eaf8d88e515b59965505aeb0c66fbb991dc96d8cce0c9bb24b0ef7a1e2b656f1`. Alle sechs Assets wurden frisch heruntergeladen. Heruntergeladene Prüfsummen, Standalone-Verifier und Vergleich von eingebettetem und externem Manifest bestanden für4917 Objekte,7602 physische Pfade,543.241.266 eindeutige Bytes und keine fehlende ausgewählte Referenz. Die getrennte Publikationsprüfung führt drei gemischte/fremde Referenzen außerhalb des Umfangs und vier exakte unveränderliche Snapshotauflösungen auf; keine Klasse ergänzt Qualifizierungscredit. Eine begrenzte Hochkonfidenzprüfung auf Zugangsdatenmuster untersuchte4918 Archivmitglieder und546.077.222 entpackte Bytes ohne Treffer.

## Bekannte Einschränkungen

Vollständige Abnahme ist unvollständig. Unqualifizierte Originale und offene Oracles bleiben sichtbar. Stock-Native ersetzt Sidecar nicht. Strict-Clientabort bleibt dort ununterstützt, wo die tatsächliche Registry dies vorgibt; kurzes Schreiben belegt weder EAGAIN noch Peer-RST. Historischer Merge-Snapshot `5e3b95864403dc642f77f01ef963d8c459b08628` reproduziert die Stock-RST-/Empty-Event-Abweichung; das exakte frühere Pre-Merge-Objekt ist nicht verfügbar und wird nicht mit diesem Snapshot gleichgesetzt.

## Verbleibende Risiken

Veröffentlichung des aktuellen Rohartefakts und tatsächliche Downloadprüfung sind abgeschlossen. Historischer Checkpoint03 bleibt getrennt und belegt keine aktuellen168 Qualifizierungen. Quellenspezifische Oracleentscheidungen, finales CI/Sonar auf veröffentlichtem Head und fehlende lokale Gitleaks-Evidenz verhindern vollständige Abnahme.

## Nicht ausgeführte Prüfungen mit Begründung

Gitleaks ist lokal nicht verfügbar; kein PASS wird behauptet, und begrenzte Zugangsdatenmusterprüfung ersetzt es nicht. Finale gehostete CI-/Sonar-Ergebnisse erwarten Veröffentlichung und Beobachtung. Tiefenscans und nicht unterstützte Fähigkeiten liegen außerhalb des begrenzten freigegebenen Umfangs.

## Finaler Diff- und Review-Status

Getrennte Routenledger erhalten unveränderte Originale und enge Prüfumfänge. Exakte Root-geprüfte quellengebundene Ergebnisse, unabhängige physische Referenzprüfung und das frisch heruntergeladene aktuelle Artefakt stützen diesen Checkpoint. Quell- und Evidenzveröffentlichung sind abgeschlossen; finale gehostete Prüfungen laufen auf bestehendem Draft#412. Vollständige Abnahme, Merge oder Masterintegration werden nicht behauptet.
