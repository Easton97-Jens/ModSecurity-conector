# Change Record: CR-20261018-haproxy-harness-source-boundaries

**Sprache:** [English](CR-20261018-haproxy-harness-source-boundaries.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-haproxy-harness-source-boundaries |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `8582074ce1efc0df330277c1c2514d762f17afab` |

## Motivation und Problemstellung

Der bereitgestellte Sonar-Serverbericht für die aktuelle Basis enthält 15 HAProxy-Befunde. Eine Quellpfadprüfung wies statische Traversal- und Symlinkpfade ab, öffnete danach jedoch den ursprünglichen vollständigen CLI-Pfad erneut. Ein nach der Prüfung ausgetauschter Vorfahr konnte das Lesen umleiten. Die getrennte ausstehende native Physical-Sink-Produktänderung benötigt außerdem eine ausdrückliche wirksame Filteroption in künftigen Fixtures.

## Akzeptanzkriterien

Den tatsächlichen Quelllese-Race beseitigen und alle 14 Wartbarkeitsbefunde ohne Ausschlüsse oder Unterdrückungen bearbeiten. Das erzeugte Verhalten von nativem v6 und Companion v5 erhalten. Anschließend genau eine Option `events-file /task/common-events.jsonl` ausschließlich in frisch erzeugte native v7-Launcher aufnehmen. Ursprüngliche Oracles, versiegelte Fixtures und Runtime-Evidence-Grenzen erhalten.

## Implementierungsentscheidung und Begründung

`i12_native_contracts.py` lässt absolute lexikalische Nachfahren des bestehenden externen Speicherroots zu. Es durchläuft jedes Verzeichnis von einem eigenen Descriptor aus mit `O_DIRECTORY | O_NOFOLLOW`, öffnet das Blatt relativ zum gehaltenen Elternverzeichnis mit `O_NOFOLLOW | O_NONBLOCK`, prüft mittels `fstat` eine reguläre Datei, liest diesen Descriptor und schließt alle eigenen Descriptoren. Der ursprüngliche vollständige Eingabepfad wird nach der Prüfung niemals erneut geöffnet. Hashreferenzen, Inventar-/Katalog-/Regelparsing und deklarative Fixture-Lesezugriffe teilen diese Grenze. Ein deterministischer Test ersetzt einen geprüften Vorfahren unmittelbar vor dem Öffnen des Blatts durch einen Symlink; die alte Implementierung liest umgeleitete Bytes, die neue erhält die ursprüngliche Verzeichnis-/Dateiidentität. Dieser lokale Linux-Harness erzeugt keine allgemeine Sandbox für andere Programme oder Pfade.

Die übrigen Befunde verwenden gemeinsame MIME-/Task-/Fixture-/Hauptpfadkonstanten, ausdrückliche Bedingungsschritte, eine Tupel-Präfixprüfung, gezielte Hilfsfunktionen für Empfang/Fehler und Backend-Body, einen kleingeschriebenen lokalen Klassenwertnamen, Entfernung eines unbenutzten Parameters und `dict.fromkeys` für unveränderliche fehlende Werte. Unabhängige Transportfakten, Fehlerreihenfolge und Nachbarverhalten bleiben erhalten.

Eine getrennte ausdrücklich autorisierte Fixture-Änderung hängt die native Produktoption an die eindeutige historische Filterdirektive an. Fehlende oder doppelte Anker scheitern vor der Vorbereitung. Der ausstehende Produktparser akzeptiert `events-file` mit einem nichtleeren privaten Pfad. Der Preparer erzeugt keine erfundene Eventdatei und keine Physical-Log-Erfolgsreceipt.

## Geänderte Dateien

`connectors/haproxy/harness/i12_companion_cases.py`, `i12_companion_host.py`, `i12_native_cases.py`, `i12_native_contracts.py`; `tests/test_haproxy_i12_native_cases.py`; dieses EN/DE-Change-Record-Paar. Der getrennte Current-Capture-Producer, Observer-Wrapper und dessen Capture-Tests bleiben eingefroren. Produkt, SPOP-Dateien anderer Zuständigkeit, zentrale/gemeinsame Capture-Objekte, Framework/MRTS und historische Evidence bleiben unverändert.

## Ausgeführte Befehle

Regelbeschreibungen wurden mit `rtk proxy /usr/local/bin/sonar-with-env api get` und öffentlicher Organisation `easton97-jens` abgefragt; frühere Fehler wegen fehlender Organisation bleiben erhalten. Die betroffenen Suiten liefen mit `rtk proxy env PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_haproxy_i12_native_cases tests.test_haproxy_i12_companion_host`: 52 Tests bestanden, Exit `0`. Der korrigierte gespeicherte Security-Reproducer für die Basis endet an der Assertion zu umgeleitetem Inhalt mit Exit `1`; korrigierter Race-, alternative Eingabe- und gewöhnliche Eingabekontrollen enden mit Exit `0`. Sein früherer Importpfadfehler bleibt erhalten und zählt nicht als Reproduktion.

Vor der Events-Option waren alle sieben Dateien jeder der 80 nativen Fixtures bytegleich zu Basis und versiegeltem v6; alle 71 Companion-Transaktionsdefinitionen waren bytegleich; Body-/Oracle-Vorhersagen stimmten für alle 82 versiegelten v5-Profile/-Kontrollen überein. Frische native v7-Vorbereitung liefert 112 ursprüngliche IDs, 80 Fixtures, null Hostläufe und null Lifecycle-Passes. Jede v7-Quelldatei entspricht versiegeltem v6 mit Ausnahme der einzelnen Option pro Launcher; deren Entfernung stellt exakte v6-Launcherbytes wieder her. Exakte argv/Exits, Rohhashes, Security-Trigger-Evidence, Regelabfragen, Einzelbefund-Dispositionen und Paritätsreceipts liegen extern unter `i12-haproxy-415-acceptance-20261015/sonar-haproxy/current15-20261018/`.

## Security-Auswirkung

Der validierte Race beim Ersetzen von Elternverzeichnissen ist an der gemeinsamen Quelllesegrenze geschlossen. Hashes legitimer physischer Eingaben und erzeugte Bytes bleiben erhalten. Pfade außerhalb des Roots, relative und Traversalpfade scheitern vor dem Öffnen; Blatt-Symlinks, Sonderdateien und Symlinkvorfahren können nicht verfolgt werden. FIFO-Ablehnung blockiert nicht. Dies gewährt keinen Zugriff außerhalb des bisherigen externen Roots und schwächt weder Datei-, Protokoll-, Compiler-, Test- noch Sonar-Kontrollen.

## Runtime-Evidence

Es wird kein Host-, Client-zu-HAProxy-, Native-Engine- oder Physical-Sink-Lauf behauptet. Unit-Socket-/Fake-Handler-Prüfungen und Fixture-Erzeugung bleiben ihre eigene Evidence-Ebene. Der v7-Pfad konfiguriert ausschließlich den künftigen Produkt-Sink; frische integrierte Produktbuilds und unabhängige tatsächliche Sink-/Client-/Backend-/Lifecycle-Beobachtungen bleiben notwendig. Kein bestehendes Oracle und kein reines Request-ACK werden zu einem Companion-Lifecycle-Pass hochgestuft.

## Bekannte Einschränkungen

Ursprüngliche unaufgelöste/Null-Werte und die 31 nativen Transaktions-Fixturelücken bleiben unverändert. Die neue Option wird von den anfänglichen Binaries aus `ea62ca995557e7c71dd268e1359fb7b62cc8fe32` nicht unterstützt und benötigt die separat integrierte Sink-Produktrevision. Bestehende v6-/v5-Verzeichnisse bleiben versiegelt und unverändert; v7 ist eine neue Fixture-Erzeugung, keine Umetikettierung eines vergangenen Laufs.

## Verbleibende Risiken

Alle 15 Befunde haben eine lokale Quelldisposition; serverseitiger Befundabschluss und Quality-Gate-Erfolg werden nicht behauptet. Sonar-Readback des aktuellen Heads und Review der Hauptaufgabe bleiben getrennte Lieferanforderungen. Anforderungen an native Timeouts, File-API, Transport-Reset und physische Sinkfehler benötigen ihre exakten ursprünglichen Verträge und unabhängige echte Host-Evidence.

## Nicht ausgeführte Prüfungen mit Begründung

In dieser Harness-Änderung wurden keine Hostläufe, Produktbuilds, Server-Neuscans oder Git-Lieferung ausgeführt. Die ursprünglichen neun Current-Capture-Tests blieben unverändert und wurden nicht wiederholt. Suiten anderer Connectoren, von Framework und MRTS lagen außerhalb des Umfangs.

## Finaler Diff- und Review-Status

Lokales Quellreview und gezielte Evidence sind abgeschlossen; unabhängiges Review der Hauptaufgabe, Server-Readback des aktuellen Heads und Lieferung stehen aus. Kein Befund wurde unterdrückt, ausgeschlossen, als sicher akzeptiert oder durch einen Serverübergang als behoben markiert. Englischer und deutscher Record bewahren dieselben technischen Fakten und Grenzen.
