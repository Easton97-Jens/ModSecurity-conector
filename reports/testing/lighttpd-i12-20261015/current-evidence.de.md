# Aktuelle lighttpd-I12-Evidenz

**Sprache:** [English](current-evidence.md) | Deutsch

Dies ist der fortlaufende Abnahmestand von [Draft-PR #412](https://github.com/Easton97-Jens/ModSecurity-conector/pull/412). Die ursprünglichen Inventuren bleiben unverändert: Stock-Sidecar153, Patched-Native116 und diagnostisch Stock-Native78; die ursprünglichen Oracle-Inventuren enthalten51,52 und23 Erwartungen. Ein Capture, erfolgreicher Treiber oder Worker-Urteil qualifiziert keinen Originalfall.

## Qualifizierung und aktuelle Ledger

`ci/runtime/lifecycle/i12/lighttpd/qualification.py` verlangt eine separate Root-Prüfung mit den exakten Hashes des Packet- und Oracle-Vorschlags und ruft danach die vorhandene gemeinsame Oracle-Reconciliation und Lifecycle-Qualifizierung auf. Jedes Ergebnis erhält unveränderliche Kopien der ausgeführten Qualifizierungsquellen. Gesonderte Konfigurations- und Pre-Native-Validatoren behalten ihren engeren Prüfumfang. Eine Pre-Native-Zurückweisung benötigt zusätzlich die exakte Root-Quellen-/Requestfreigabe; sie erzeugt weder native Transaktion noch Body-Lifecycle.

`current_ledger.py` prüft physische Vorschläge, freigegebene Ableitungen und gemeinsame Ergebnisse erneut, bevor getrennte Routenledger exportiert werden. Root-geprüfte Capture-Abdeckung kann einen tatsächlichen HTTP-/Parserlauf belegen, ohne PASS oder Oracle-Abschluss zu vergeben. Reine Startversuche zählen nicht als HTTP-Requests. Kopierte Prozessreceipts zählen nicht als neue Ausführungen. Vollständige diagnostische Fallabnahme bleibt von verpflichtender Body-Lifecycle-Abnahme getrennt.

Der unabhängig erneut qualifizierte Checkpoint08 enthält168 aktuell angenommene Originale: Stock60, Patched72 und Diagnose36. Die Diagnoseabnahme umfasst28 Hostkontrollen und acht Konfigurationsparserkontrollen; sie erteilt keine Body-Lifecycle-Abnahme. Die [aktuelle Zusammenfassung](current-20261020/summary.json) und getrennten Routenledger behalten jede Original-ID, ihre Messungen, ihren Qualifizierungsumfang und offenen Gründe bei.

| Route | Original-IDs | Tatsächliche HTTP-/Parserläufe | Aktuelle PASS | Aktuell unqualifizierte IDs | Ursprüngliche Oracles | Weiter offene Oracles |
| --- | --- | --- | --- | --- | --- | --- |
| [Stock-Sidecar](current-20261020/lighttpd-stock-sidecar.json) | 153 | 128 / 0 | 60 | 92 | 51 | 17 |
| [Patched-Native](current-20261020/lighttpd-patched-native.json) | 116 | 112 / 0 | 72 | 44 | 52 | 13 |
| [Stock-Native diagnostisch](current-20261020/lighttpd-stock-native-control.json) | 78 | 69 / 8 | 36 | 42 | 23 | 19 |

Die unqualifizierten Zahlen verwenden die Vereinigung historischer und aktueller Qualifizierungen im Ledger; sie entsprechen daher nicht einfach Original-IDs abzüglich aktueller PASS. Neu qualifizierte Original-IDs sind59/70/35; neu geklärte ursprüngliche Oracles sind32/37/4. Die ursprünglichen Oracle-Zahlen und historischen Ergebnisse bleiben unverändert. Der vollständige Root-geprüfte Ausführungsindex mit347 Zeilen enthält317 tatsächliche HTTP-/Parserergebnisse nach Wait; seine reinen Capture-Zeilen vergeben keine zusätzlichen PASS. Die übrigen Zeilen umfassen13 reine Startversuche und17 Fälle ohne Ausführung. Qualifizierung mit aktuellen Quellen und Ausführungsabdeckung sind getrennte Aussagen.

Der Export bindet den Integrationshead `eef8c1b432c0ce372c551a32fa6977cf4633b6c3`, Basis #410 `a62296fb57263f9be18c6ac879e36e0ab2a9935c` und Produkt #382 `12cc380c3749fd76c246c05ce479f51446127880`. Dies sind die Revisionen beim Export vor Veröffentlichung der späteren lighttpd-Produceränderungen. Das aktuelle Evidenzrelease bindet den veröffentlichten Producer-/Quell-Head `2008b875f1860774627878051582b607f835b019`. Die CI-/Sonar-Abnahme des final veröffentlichten Heads läuft noch.

## Abrufbarer Rohdaten-Checkpoint

Das [aktuelle Evidenz-Prerelease](https://github.com/Easton97-Jens/ModSecurity-conector/releases/tag/evidence-i12-lighttpd-pr412-20261020-current) enthält das inhaltsadressierte Rohdatenarchiv, Manifest, exakte Auswahl, Publikationsprüfung, Prüfsummen und den eigenständig ausführbaren Verifier für die168 aktuellen Qualifizierungen und alle347 getrennten Ledgerzeilen. Es zielt auf den veröffentlichten Quell-Head `2008b875f1860774627878051582b607f835b019`. Das frühere [Checkpoint03-Prerelease](https://github.com/Easton97-Jens/ModSecurity-conector/releases/tag/evidence-i12-lighttpd-pr412-20261018-checkpoint03) bleibt der historische Snapshot für89 Qualifizierungen und RST-Evidenz und gilt nicht als aktueller Nachweis.

| Objekt | SHA256 |
| --- | --- |
| `lighttpd-i12-raw.tar.gz` | `c7dccdfd5bb1c69029eb92864a5c9b62bd06e24a9a2466183c7f40ddc281d1bf` |
| `manifest.json` | `eaf8d88e515b59965505aeb0c66fbb991dc96d8cce0c9bb24b0ef7a1e2b656f1` |
| `selection-checkpoint10-current.json` | `734c063a129cad529d2879e630df451b9005925b93bf7c59658e4ad3722778de` |

Alle sechs Release-Assets wurden frisch von GitHub heruntergeladen. `SHA256SUMS-checkpoint10-current` akzeptierte die fünf aufgeführten Nutzdatenassets, bevor der heruntergeladene Verifier4917 eindeutige Inhaltsobjekte für7602 physische Pfade und543.241.266 eindeutige Bytes ohne fehlende ausgewählte Referenz akzeptierte. Das heruntergeladene externe Manifest stimmte außerdem bytegenau mit dem eingebetteten Archivmanifest überein. Drei gemischte/fremde Referenzen stehen ausdrücklich außerhalb des Umfangs; vier fehlende historische Produzentenpfade werden nur auf unveränderliche Snapshots mit exakt passendem Digest und gleicher Größe aufgelöst. Die Publikationsprüfung führt beide Klassen einzeln auf; keine vergibt Qualifizierungscredit. Archivpfade bestehen aus Inhaltshashes; ursprüngliche absolute Producerpfade sind Manifestmetadaten. Die Prüfung entpackt keine Dateien. Nach Asset-Download reproduzierbar:

```sh
rtk proxy sha256sum -c SHA256SUMS-checkpoint10-current
rtk proxy python3 verify-lighttpd-i12.py \
  --archive lighttpd-i12-raw.tar.gz \
  --expected-sha256 c7dccdfd5bb1c69029eb92864a5c9b62bd06e24a9a2466183c7f40ddc281d1bf
```

`artifact.py` verpackt nur eine ausdrücklich hashgebundene Auswahl mit ihrer ausgewählten JSON-Referenzmenge innerhalb dokumentierter lighttpd-Wurzeln bei begrenzten Dateien, Einträgen und Gesamtbytes. Opake Nachweise werden nicht rekursiv erweitert; gemischte oder fremde Referenzen werden als außerhalb des Umfangs protokolliert. Ein exakter, von Root ausgewählter unveränderlicher Snapshot darf einen fehlenden oder abgewichenen Originalpfad nur bei übereinstimmendem Digest und gleicher Größe auflösen; jede solche Auflösung wird protokolliert. Nicht freigegebene fehlende Referenzen, nicht freigegebene veränderte Bytes, Symlinks, geteilte Hardlinks, unsichere Archivmitglieder und veränderte Objekte werden zurückgewiesen. Verpackung belegt Abrufbarkeit und Integrität, keine Fallqualifizierung. Aufgabenartefakte enthalten synthetischen Fixtureverkehr und ausdrücklich ausgewählte Quellen statt Zugangsdaten oder vollständiger Umgebungsdateien. Eine begrenzte Hochkonfidenzprüfung auf Zugangsdatenmuster untersuchte4918 Archivmitglieder und546.077.222 entpackte Bytes ohne Treffer; Gitleaks war nicht verfügbar und wird nicht als bestanden ausgewiesen.

## Routen- und Produktionsgrenzen

Stock behält private0700-Spoolverzeichnisse,0600-Dateien, gemeinsame256MiB-Technikkapazität und64MiB-Reserve. Physische Erschöpfung ist ein technisches503 ohne native Body-Verarbeitung; Freigabe/Wiederzulassung und die unveränderte Reserveprimitive sind getrennt gemessen. Die gelieferten Off-/Safe-/Strict-/All-Konfigurationen bleiben getrennte tatsächliche Ausführungen.

Patched-Hostevidenz verwendet gepinntes lighttpd1.4.85, gemessene Modul-/Core-/SDK-Images und tatsächliche Hooks. Sechs bestätigte Delivery-/EOS-/Cleanup-/Response-Hook-Fixes wurden auf bestehendem#382 committet und normal über#410 integriert. Der sechste Fix, `c523dce9966b47bc8be6efe39ee49f2d88de3397`, korrigiert die Umgehung der Antwortprüfung durch Upstream-Splice/Sendfile. Die echte UID65534-Wiederholung misst1,050,657 Antwortbytes auf Native-/Host-/Client-/Backendebene, ein EOS, physisches Logging/Free/Destroy und erfolgreiche Nachbarrequests. Fünf neue P3-Zurückweisungen liefern tatsächliches403 mit158 Antwortbodybytes; neun betroffene Antwortfälle wurden wiederholt. Frühere betroffene Antwortqualifizierungen wurden ersetzt. Im Reject-Umfang gelten `runtime_finish=0` und `common_finish=2`; Logging/Free/Destroy sind jeweils1. Diese getrennten Zähler bleiben erhalten und werden nicht als einmaliger Finish beschrieben. Kurzes Schreiben beweist kein EAGAIN; lokale Abbruchabsicht beweist keinen empfangenen Peer-RST. Strict-Clientabort wird nicht als Fähigkeit erfunden.

Stock-Native bleibt eine diagnostische Header-/Konfigurationskontrolle. Seine drei exakten fehlerhaften CL-Zurückweisungen vor nativer Allokation werden gesondert mit tatsächlichem400, keiner nativen Haupt-/Backendaktivität, positiven Kontrollen, privaten Log-/Eventfenstern und Cleanup geprüft. Es ersetzt kein natives Body-Streaming.

Die unveränderte historische Merge-Revision `5e3b95864403dc642f77f01ef963d8c459b08628` reproduziert den ursprünglichen Stock-RST-Testfehler mit leerer physischer Eventdatei. Das frühere exakte September-Pre-Merge-Objekt ist nicht verfügbar; diese Revisionen werden nicht gleichgesetzt. Root- und tatsächliche UID65534-Läufe bleiben getrennt. Namespace-, AppArmor-, UID-, Symlink- und Read-only-Grenzen wurden nicht abgeschwächt.

## Verifikation und verbleibende Arbeit

Die fokussierte lighttpd-I12-Suite für Producer/Adapter/aktuelles Ledger/Artefakt bestand99 Tests einschließlich exakter Regelbindung an die Haupttransaktion und negativer Archivkontrollen. Eine unabhängige Wiederholung aller36 ausgewählten Diagnosequalifizierungen fand15 regeltragende normale Hostfälle mit exakten physischen Haupttransaktionsereignissen und ohne Auditfallback. Die integrierten gemeinsamen Reconciliation-/Lifecycle-/Berichtskontrollen bestanden82 Tests. Die Produktregression für Precommit-Antwort/EOS/Stock/Native/Spool/Sink/Cleanup führte214 Tests aus:201 bestanden,13 wurden wegen ausdrücklicher Namespace-/UID-Einschränkungen übersprungen; passende echte Nonroot-Captures bleiben separate Evidenz. Zweisprachigkeits- und native Dokumentationslinkprüfungen für den integrierten Produktnachweis bestanden. Aktuelle finale Headprüfungen stehen aus; vollständige grüne Abnahme wird nicht behauptet.

Aktuelle Routenledger je ID, die regressionsgebundene Großantwortkorrektur mit Wiederholung und das tatsächlich heruntergeladene aktuelle Rohdatenarchiv liegen vor. Aktuelle Zweisprachigkeits-, Repositorypfad-/Link- und Change-Record-Strukturprüfungen bestanden. Offen bleiben Qualifizierung nicht abgenommener Originale, quellenspezifische Entscheidungen zu offenen Oracles und alle CI-/Sonar-Pflichtprüfungen auf dem final veröffentlichten SHA. Lokale Gitleaks-Evidenz bleibt nicht verfügbar; die begrenzte Prüfung auf Zugangsdatenmuster ersetzt sie nicht. Lebender Ausführungsplan und genaue Befehle bleiben aufgabenlokal; historische Evidenz und Baseline-Exporte werden erhalten. Vollständige Connector-Abnahme wird nicht behauptet.
