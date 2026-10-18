# Änderungsnachweis: CR-20261018-i12-lighttpd-qualified-artifacts

**Sprache:** [English](CR-20261018-i12-lighttpd-qualified-artifacts.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-i12-lighttpd-qualified-artifacts |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `cc5285a6` |
| Parent-PR | #412, Basis #410 |

## Motivation und Problemstellung

Die ursprünglichen lighttpd-Inventuren mit347 Fällen müssen unverändert bleiben, während tatsächliche aktuelle Fallqualifizierung und abrufbare physische Evidenz fortgeschrieben werden. Worker-Captureurteile und ausschließlich lokale Pfade belegen weder Abnahme noch dauerhafte Lieferung.

## Akzeptanzkriterien

Separate exakte Root-Packet-/Oracleprüfung, vorhandene gemeinsame Validatoren, physische SHA-Prüfung, unveränderliche ausgeführte Qualifizierungsquellen und korrekte HTTP-/Parser-/Start-/Diagnoseumfänge verlangen. Ergebnisse vor aktuellem Ledgerexport erneut prüfen. Eine ausdrücklich begrenzte Evidenzauswahl verpacken und ein tatsächlich heruntergeladenes Archiv ohne Entpacken prüfen. Fehlende Daten, nicht unterstützte Fähigkeiten und historische Fehler sichtbar erhalten.

## Implementierungsentscheidung und Begründung

Die ausschließlich lighttpd gehörenden Module `qualification.py`, `current_ledger.py` und `artifact.py` adaptieren vorhandene gemeinsame Verträge. Der Adapter übernimmt kein Worker-Urteil direkt. Gesonderte Pre-Native-Freigabe bindet den exakten Quellenvorschlag und ruft weiterhin den strengen gemeinsamen physischen Validator auf. Der Routenexport erhält Baseline-Zeilen und ursprüngliche Oracle-Historie; Capture-Abdeckung vergibt kein PASS. Das Archiv verwendet nach Inhalten adressierte Objekte, eine rekursive explizite SHA-Referenzmenge und begrenzte Prüfung ohne Entpacken. Der vorhandene Baseline-Exporter wurde ohne Änderung seines durch acht Tests geprüften Verhaltens aufgeteilt.

## Geänderte Dateien

Die vier lighttpd-Evidenzmodule, ihre drei neuen Testmodule, dieser EN/DE-Nachweis und das Paar [aktuelle Evidenz](../../testing/lighttpd-i12-20261015/current-evidence.de.md). Capture-Producer, Produktfixes und gemeinsame Validatoren haben getrennte Verantwortlichkeiten/Nachweise. Diese Änderung bearbeitet weder zentrale Matrix, Framework/MRTS, Abhängigkeiten noch fremde Connectoren.

## Ausgeführte Befehle

`rtk proxy /usr/local/bin/python3 -m unittest -q tests.test_lighttpd_i12_qualification tests.test_lighttpd_i12_current_ledger tests.test_lighttpd_i12_artifact tests.test_lighttpd_i12_ledger` —29 bestanden. Negative Kontrollen prüfen veränderte/fehlende/fremde Evidenz, fehlende separate Freigaben, Quellenänderung während der Qualifizierung, verbotene Pfade, Symlinks/Hardlinks, Worker-PASS-Hochstufung, kopierte Ausführungsreceipts, diagnostische Lifecycle-Trennung, unsichere Archivmitglieder und veränderte/fehlende heruntergeladene Objekte.

## Security-Auswirkung

Begrenzte funktionale Evidenzarbeit innerhalb des vom Nutzer vorgegebenen Blue-Umfangs. Keine Angriffs-/Exploitscans oder Abschwächung der Isolation. Physische Datenauswahl schließt Authentifizierungs-/Umgebungsdateien aus. Verpackung ist begrenzt und entpackt keine Archivmitglieder. Sonar verwendet den vorgeschriebenen Wrapper; kein Quality Gate wurde abgeschwächt.

## Runtime-Evidence

[Checkpoint03](https://github.com/Easton97-Jens/ModSecurity-conector/releases/tag/evidence-i12-lighttpd-pr412-20261018-checkpoint03) wurde tatsächlich heruntergeladen und geprüft:2284 Inhaltsobjekte/2462 physische Pfade/keine fehlenden Referenzen. Archiv-SHA256: `e05d4fdb2c91fa6417f46b40b189ea85dd2a39e4f14f572fcaf47b8dad8a1c44`. Es enthält89 Qualifizierungen und historische Quellen-/RST-Daten; der aktuelle Checkpoint04 hat121 erneut bewertete Qualifizierungen. Dies sind ausdrücklich verschiedene Snapshots, keine finale Abnahme aller347 Fälle.

## Bekannte Einschränkungen

Finale aktuelle Exporte je ID und ein späterer Rohdatencheckpoint bleiben aktive Arbeit. Eine neu belegte Hooklücke des gepatchten Antwort-Splicepfads erhält bis zu eigener Produktregression/Fix/Wiederholung keine Abnahme. Frühere physische Fehler und fehlende exakte historische Quelle bleiben erhalten. Diagnostische Abnahme liefert keine Body-Streaming-Gutschrift.

## Verbleibende Risiken

Finale ursprüngliche Oracle-Reconciliation und CI/Sonar des exakt veröffentlichten Heads bleiben unvollständig. Spätere Artefakte müssen die tatsächlich später ausgewählten Ergebnisse binden; das ältere Archiv darf nicht als finale Evidenz umetikettiert werden.

## Nicht ausgeführte Prüfungen mit Begründung

Gitleaks wird wegen fehlender Binärdatei nicht als bestanden behauptet. Finale Hosted-/Sonar-Gateprüfungen werden vor Veröffentlichung und Prüfung des endgültigen Codes nicht als bestanden ausgegeben. Breitere Produkt-/Nativregressionen und echte Hostcapturen sind separat dokumentiert.

## Finaler Diff- und Review-Status

Root-eigene Evidenzwerkzeuge und29 gezielte Kontrollen sind geprüft. Baseline-Exporte und historische Daten bleiben unverändert. Normale begrenzte Lieferung läuft im bestehenden Draft#412 weiter; finale Abnahme ist in Arbeit.
