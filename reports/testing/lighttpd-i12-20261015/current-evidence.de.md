# Aktuelle lighttpd-I12-Evidenz

**Sprache:** [English](current-evidence.md) | Deutsch

Dies ist der fortlaufende Abnahmestand von [Draft-PR #412](https://github.com/Easton97-Jens/ModSecurity-conector/pull/412). Die ursprünglichen Inventuren bleiben unverändert: Stock-Sidecar153, Patched-Native116 und diagnostisch Stock-Native78; die ursprünglichen Oracle-Inventuren enthalten51,52 und23 Erwartungen. Ein Capture, erfolgreicher Treiber oder Worker-Urteil qualifiziert keinen Originalfall.

## Qualifizierung und aktuelle Ledger

`ci/runtime/lifecycle/i12/lighttpd/qualification.py` verlangt eine separate Root-Prüfung mit den exakten Hashes des Packet- und Oracle-Vorschlags und ruft danach die vorhandene gemeinsame Oracle-Reconciliation und Lifecycle-Qualifizierung auf. Jedes Ergebnis erhält unveränderliche Kopien der ausgeführten Qualifizierungsquellen. Gesonderte Konfigurations- und Pre-Native-Validatoren behalten ihren engeren Prüfumfang. Eine Pre-Native-Zurückweisung benötigt zusätzlich die exakte Root-Quellen-/Requestfreigabe; sie erzeugt weder native Transaktion noch Body-Lifecycle.

`current_ledger.py` prüft physische Vorschläge, freigegebene Ableitungen und gemeinsame Ergebnisse erneut, bevor getrennte Routenledger exportiert werden. Root-geprüfte Capture-Abdeckung kann einen tatsächlichen HTTP-/Parserlauf belegen, ohne PASS oder Oracle-Abschluss zu vergeben. Reine Startversuche zählen nicht als HTTP-Requests. Kopierte Prozessreceipts zählen nicht als neue Ausführungen. Vollständige diagnostische Fallabnahme bleibt von verpflichtender Body-Lifecycle-Abnahme getrennt.

Der unabhängig erneut qualifizierte Checkpoint04 enthält121 angenommene Originale: Stock47, Patched57 und Diagnose17, einschließlich acht Parserkontrollen. Diese Zahlen beschreiben genau den gespeicherten Checkpoint; spätere Captures und Quellenkorrekturen benötigen eine weitere Prüfung. Die abschließende Reconciliation aller347 Fälle sowie CI-/Sonar-Abnahme des finalen Heads laufen noch.

## Abrufbarer Rohdaten-Checkpoint

Das [Checkpoint03-Evidenz-Prerelease](https://github.com/Easton97-Jens/ModSecurity-conector/releases/tag/evidence-i12-lighttpd-pr412-20261018-checkpoint03) enthält ein nach Inhalten adressiertes Rohdatenarchiv, Manifest, exakte Auswahl, Prüfsummen und einen eigenständig ausführbaren Verifier. Es umfasst89 Qualifizierungen und238 historische RST-/Quellen-/Logdateien. Es liegt vor Checkpoint04 und behauptet keine Abdeckung aller347 Fälle.

| Objekt | SHA256 |
| --- | --- |
| `lighttpd-i12-raw.tar.gz` | `e05d4fdb2c91fa6417f46b40b189ea85dd2a39e4f14f572fcaf47b8dad8a1c44` |
| `manifest.json` | `6696df68c9c4df45135cc3c1f94947b8e4685a8ab321343ea204969d1347e103` |

Ein tatsächlicher GitHub-Download wurde vor Ausführung des heruntergeladenen Verifiers mit den fünf ursprünglichen Asset-Hashes abgeglichen. Die Prüfung akzeptierte2284 eindeutige Inhaltsobjekte für2462 physische Pfade ohne fehlende Referenzen. Archivpfade bestehen aus Inhaltshashes; ursprüngliche absolute Producerpfade sind Manifestmetadaten. Die Prüfung entpackt keine Dateien. Nach Asset-Download und Prüfung von `SHA256SUMS-checkpoint03` reproduzierbar:

```sh
rtk proxy python3 verify-lighttpd-i12.py \
  --archive lighttpd-i12-raw.tar.gz \
  --expected-sha256 e05d4fdb2c91fa6417f46b40b189ea85dd2a39e4f14f572fcaf47b8dad8a1c44
```

`artifact.py` verpackt nur eine ausdrücklich hashgebundene Auswahl mit ihrer JSON-Referenzmenge bei begrenzten Dateien, Einträgen und Gesamtbytes. Nicht freigegebene fehlende Referenzen, Symlinks, geteilte Hardlinks, veränderte Bytes, unsichere Archivmitglieder und veränderte Objekte werden zurückgewiesen. Verpackung belegt Abrufbarkeit und Integrität, keine Fallqualifizierung. Aufgabenartefakte enthalten synthetischen Fixtureverkehr und ausdrücklich ausgewählte Quellen statt Zugangsdaten oder vollständiger Umgebungsdateien. Die begrenzte Prüfung auf Zugangsdatenmuster bestand; Gitleaks war nicht verfügbar und wird nicht als bestanden ausgewiesen.

## Routen- und Produktionsgrenzen

Stock behält private0700-Spoolverzeichnisse,0600-Dateien, gemeinsame256MiB-Technikkapazität und64MiB-Reserve. Physische Erschöpfung ist ein technisches503 ohne native Body-Verarbeitung; Freigabe/Wiederzulassung und die unveränderte Reserveprimitive sind getrennt gemessen. Die gelieferten Off-/Safe-/Strict-/All-Konfigurationen bleiben getrennte tatsächliche Ausführungen.

Patched-Hostevidenz verwendet gepinntes lighttpd1.4.85, gemessene Modul-/Core-/SDK-Images und tatsächliche Hooks. Die fünf zuvor bestätigten Delivery-/EOS-/Cleanup-Fixes wurden auf bestehendem#382 committet und normal über#410 integriert. Bei der abschließenden Großantwortprüfung zeigte eine neue Messung, dass Zero-Copy-Upstream-Splice einen Teil der nativen Antwortprüfung umgehen kann. Dieser Fall erhält bis zur regressionsgebundenen Korrektur und echten Wiederholung keine aktuelle Abnahme. Kurzes Schreiben beweist kein EAGAIN; lokale Abbruchabsicht beweist keinen empfangenen Peer-RST. Strict-Clientabort wird nicht als Fähigkeit erfunden.

Stock-Native bleibt eine diagnostische Header-/Konfigurationskontrolle. Seine drei exakten fehlerhaften CL-Zurückweisungen vor nativer Allokation werden gesondert mit tatsächlichem400, keiner nativen Haupt-/Backendaktivität, positiven Kontrollen, privaten Log-/Eventfenstern und Cleanup geprüft. Es ersetzt kein natives Body-Streaming.

Die unveränderte historische Merge-Revision `5e3b95864403dc642f77f01ef963d8c459b08628` reproduziert den ursprünglichen Stock-RST-Testfehler mit leerer physischer Eventdatei. Das frühere exakte September-Pre-Merge-Objekt ist nicht verfügbar; diese Revisionen werden nicht gleichgesetzt. Root- und tatsächliche UID65534-Läufe bleiben getrennt. Namespace-, AppArmor-, UID-, Symlink- und Read-only-Grenzen wurden nicht abgeschwächt.

## Verifikation und verbleibende Arbeit

Root-Kontrollen für Adapter/aktuelles Ledger/Artefakt/unverändertes Ledger:29 Tests bestanden. Die integrierten gemeinsamen Reconciliation-/Lifecycle-/Berichtskontrollen bestanden82 Tests. Die Produktregression für Precommit-Antwort/EOS/Stock/Native/Spool/Sink/Cleanup führte214 Tests aus:201 bestanden,13 wurden wegen ausdrücklicher Namespace-/UID-Einschränkungen übersprungen; passende echte Nonroot-Captures bleiben separate Evidenz. Zweisprachigkeits- und native Dokumentationslinkprüfungen für den integrierten Produktnachweis bestanden. Aktuelle finale Headprüfungen stehen aus; vollständige grüne Abnahme wird nicht behauptet.

Offen bleiben vollständige Reconciliation je ID, quellenspezifische Entscheidungen zu offenen Oracles, Großantwort-Hookregression/Fix, Veröffentlichung/Download späterer Rohdaten, finale getrennte Routenledger und alle Pflichtprüfungen auf dem final veröffentlichten SHA. Lebender Ausführungsplan und genaue Befehle bleiben aufgabenlokal; historische Evidenz und Baseline-Exporte werden erhalten.
