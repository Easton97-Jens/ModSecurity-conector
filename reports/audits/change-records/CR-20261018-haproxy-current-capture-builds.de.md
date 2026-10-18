# Change Record: CR-20261018-haproxy-current-capture-builds

**Sprache:** [English](CR-20261018-haproxy-current-capture-builds.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-haproxy-current-capture-builds |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `ea62ca995557e7c71dd268e1359fb7b62cc8fe32` |

## Motivation und Problemstellung

Historische Capture-Objekte beschreiben einen älteren Produktbaum. Die Übernahme ihrer vollständigen alten Dateien würde aktuelle Common-, Mapper-, SDK-Accessor- und Request-Authorization-Änderungen verwerfen. Aktuelle HAProxy-Instrumentierung aus einem vollständigen ausgewählten Git-Archiv vorbereiten und historische Capture-Identitäten und Ergebnisse erhalten.

## Akzeptanzkriterien

Bestehende Registry, Observer-Collector und v2-Inventur für wegwerfbare Quellkopien wiederverwenden. Nur exakte, eindeutige historische Delta-Kontexte oder die ausdrücklich geprüften aktuellen Allokations-/SPOP-Ports zulassen. Aktuelle Produktbytes außerhalb dieser Deltas erhalten. Quell-/Archiv-/SDK-/Befehls-/Binäridentitäten erfassen, drei Varianten frisch bauen und Kompilierung von Runtime-Qualifikation trennen.

## Implementierungsentscheidung und Begründung

`i12_current_capture.py` exportiert vollständige Git-Archive anhand einer Revision mit 40 Zeichen, erfasst Dateimodi/-hashes und Gitlink-Metadaten und erzeugt frische externe Quellkopien. Gitlinks werden nicht materialisiert. Registry-Repository-Objekte werden ausschließlich aus Mitgliedern mit exakt passendem Hash der aktuellen oder historischen Archive rekonstruiert; dieses Auflösungsverzeichnis ist niemals ein Produkt-Buildbaum. Ursprüngliches gemeinsames Manifest und Capture-Objekte bleiben unverändert.

Der gewöhnliche Instrumentierungsport verlangt eindeutigen vollständigen Kontext und akzeptiert keinen unscharfen Treffer. Zwei geprüfte Anpassungen erhalten aktuelle Semantik: Den privaten Allokationspfad `begin_request_with_scope`, den direkte, Companion- und reine Request-Authorization-Aufrufe gemeinsam verwenden, beobachten und `request_authorization_only`, tatsächlichen Rückgabewert, native/Common-Handles und gesichertes errno weiterreichen; den aktuellen SPOP-Companion-/Request-Authorization-Zweig mit bestehenden Sample-Beobachtungen umschließen. Eine geänderte private Signatur oder SPOP-Verzweigung scheitert fail-closed.

`i12_request_scope_observer.c` bindet die bestehende Observer-Implementierung einmal ein und ergänzt deren vorhandenen `COMMON_TIME_WRAPPER(finish_request_authorization, "common_finish_request_authorization", 0)`. Diese Übersetzungseinheit ersetzt beim Linken das gewöhnliche Observer-C-Objekt. Sie beobachtet tatsächlichen Common-Eintritts-/Rückkehrzustand, bewahrt bei reiner Request-Verarbeitung die Phasenmaske `3` und erhält die Identitätszuordnung bis zum gewöhnlichen Cleanup. Sie erzeugt weder P3/P4, EOS, Abschluss noch eine Maske `15`.

Der aktuelle Versionsvertrag pinnt HAProxy `3.2.25`, Archiv-SHA-256 `d59a68d0daef7b5c596b019b742089788ff1748513ef96e71fe7b3943577866e`. Nach Hashprüfung werden elf Release-Fixture-Symlinks als gewöhnliche Dateien aus regulären Mitgliedern desselben Archivs materialisiert. Es wird kein Dateisystem-Symlink erzeugt oder verfolgt. Absolute/ausbrechende Links, fehlende oder verkettete Ziele, Hardlinks, Sonderdateien und doppelte Mitglieder werden abgelehnt. Das Normalisierungsreceipt erfasst jeden ursprünglichen Link, aufgelöstes Mitglied, Inhaltshash und Modus. Bestehendes natives Staging erneuert aktuelle Common-Header/-Übersetzungseinheiten, Mapper, Profilregistry und Runtime-Client-Eingaben. Agent-Featureflags bewahren eigene `_GNU_SOURCE`-Definitionen der Übersetzungseinheiten und alle Compilerwarnungen. Das ausgewählte Capture-Tool-Python-Modul und die Build-Eingaben müssen vertrauenswürdige, vom Bediener ausgewählte Dateien sein.

## Geänderte Dateien

`connectors/haproxy/harness/i12_current_capture.py`, `connectors/haproxy/harness/i12_request_scope_observer.c`, `tests/test_haproxy_i12_current_capture.py`; dieses EN/DE-Change-Record-Paar. Keine Änderung an Produkt, gemeinsamen Captures, zentraler Matrix, Framework/MRTS, anderen Connectoren oder historischen R1-Artefakten.

## Ausgeführte Befehle

Der frühere gezielte Befehl `rtk proxy env PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest discover -s tests -p test_haproxy_i12_current_capture.py -v` bestand neun Tests, Exit `0`; Receipt: `i12-haproxy-415-acceptance-20261015/builds/verification-current-capture-final-20261018/receipt.json`. Das Review ergänzte drei Quellporttests zu Allokationsscope/-identitäten, geänderten privaten Signaturen und SPOP-Zweigplatzierung/geänderten Ankern. Nur diese drei neuen Methoden wurden wiederholt, alle bestanden, Exit `0`; die unveränderten neun wurden nicht wiederholt. Der Scaffold-Befehl lautete `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -B ci/tools/new-change-record.py create --name haproxy-current-capture-builds --base-revision ea62ca995557e7c71dd268e1359fb7b62cc8fe32 --date 2026-10-18`. Exakte Build-argv, Exits und Ausgabehashes liegen extern unter `builds/current-ea62-v4/build-commands/commands.json` und `retry-build-commands/commands.json` im selben Lauf. Der Abschlussdriver endete nach allen drei frischen Builds mit Exit `0`; `completion-receipt.json` bindet 15.761 Rohartefakte. Das separate `materialized-input-audit.json` prüft jede ursprüngliche aktuelle Datei gegen ihren ursprünglichen oder deklarierten Capture-Hash und erfasst drei Quellinventare, 1.391 unveränderte Upstream-Dateien, erzeugte Hostdateien und zusätzliche Common-Runtime-/Header-Kopierbindungen.

Dokumentationschecks bestanden, Exit `0`: `rtk proxy env PYTHONNOUSERSITE=1 make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-bilingual-docs`, derselbe Befehl mit `check-doc-links` und `rtk proxy env PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B ci/tools/new-change-record.py check`. Dies validiert Dokumentationsstruktur/-links, keine Runtime-Evidence.

## Security-Auswirkung

Keine Änderung produktiver Sicherheitskontrollen. Archiv-/Pfadannahme und exakte Quellbindungen schützen die Evidence-Grenze. Fehlversuche bleiben ausdrücklich erhalten; kein Fehler wird zu Erfolg umgewertet, keine Compilerwarnung und kein Gate abgeschaltet und keine Zugangsdaten erfasst. Dieser vertrauenswürdige lokale Build-Consumer isoliert kein beliebig übergebenes Python-Capture-Tool in einer Sandbox.

## Runtime-Evidence

Reines Build-Ergebnis aus `ea62ca995557e7c71dd268e1359fb7b62cc8fe32`: direktes Binary-SHA-256 `beee0738953f07810b0de7a1b9b30ed6d32717b4cf37753011cbf2bd5b330237`; Companion `e55d5ae4de28c9d04ee7ada6a52f5ecc7e752d5418787626c61a9df3c4938a0e`; SPOP-Agent `56a81b2ea8119144511c9a72ab2daaacb81c9ec0dcdb71fff1ee32e2a4e4818d`. `nm` bestätigt den Request-Authorization-Finish-Wrapper in allen drei, und `readelf`-Receipts binden dynamische Link-Metadaten. Die SDK-Inventur bindet die tatsächliche kompatible `3.0.14`-Bibliothek und Header. Dies sind drei Build-Artefakte und null Hostläufe dieses Producers, mit `runtime_qualified: false`. Unabhängige Host-Evidence und ursprüngliche Oracle-Qualifikation bleiben getrennt; ein SPOP-ACK qualifiziert den Response-Companion nicht.

## Bekannte Einschränkungen

Frühere Versuche scheiterten an exakter Repository-Objektauflösung, nicht unterstützten Archivlinks, einem fehlenden Observer-Includepfad und redundanten `_GNU_SOURCE`-Definitionen. Ihre Rohlogs und Consumer-Snapshots bleiben erhalten. Der letzte erste Agent-Versuch endete unter unverändertem `-Werror` mit Exit `1`; der erfolgreiche unabhängige Wiederholungsversuch baute jedes Agent-/Observer-Objekt in neuen Verzeichnissen frisch und behielt den bereits erfolgreichen frischen Companion-Build. Direct wurde anschließend frisch gebaut. Das vollständige Inventaraudit nach dem Build ist ein separates laufbezogenes Receipt, keine automatisch garantierte Ausgabe jedes künftigen Producer-Aufrufs. Die Host-Kompilierlogs bewahren Warnungen zu gemischten Deklarationen, einen unbenutzten Precommit-Helper und Upstream-Hinweise auf nicht unterstützte Warnungsoptionen.

## Verbleibende Risiken

Eine spätere Common-Sink-Produktintegration verlangt einen neuen vollständigen Quellexport, Instrumentierungsport und frische Builds; diese Binaries können jene spätere Revision nicht nachweisen. Der Observer belegt ohne unabhängige Runtime-Beobachtungen weder physischen Common-Sink-Erfolg, native Deadline-Unterstützung, native File-API-Nutzung, tatsächlichen Client-Commit/-Reset noch einmaliges Cleanup. Lokale Tests belegen kein Sonar-Server-Quality-Gate-Ergebnis.

## Nicht ausgeführte Prüfungen mit Begründung

Während dieses Dokumentations-/Quellportreviews wurden keine Hostläufe, Produkt-Regressionsbuilds, Sonar-Serveranalyse, Git-Lieferung oder Lifecycle-Qualifikation durchgeführt. Die obigen Build- und Neun-Test-Ergebnisse sind erhaltene frühere Evidence; die drei neu ergänzten Tests wurden separat ausgeführt. Breitere unveränderte Testsuiten wurden nicht wiederholt.

## Finaler Diff- und Review-Status

Producer- und Observer-Bytes bleiben identisch zum eingefrorenen erfolgreichen Retry-Consumer. Dieses Review ergänzt ausschließlich Tests und den gepaarten Change Record. Dokumentationsvalidierung und exakte Review-Receipts liegen extern; es wird weder Commit, Push, Merge noch finale I12-Abnahme behauptet.
