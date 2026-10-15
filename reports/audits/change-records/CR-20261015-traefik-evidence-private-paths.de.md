# Change Record: CR-20261015-traefik-evidence-private-paths

**Sprache:** [English](CR-20261015-traefik-evidence-private-paths.md) | Deutsch

Producer-Grenzkorrektur unter Erhalt unveränderlicher historischer Belege.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261015-traefik-evidence-private-paths |
| Datum (UTC) | 2026-10-15 |
| Basis-Revision | `107e09a657468b815c45af81929e00f33d8e6606` |

## Motivation und Problemstellung

Die bisherigen PR413-Hostproducer erlaubten zu breite Ziele und enthielten Wartbarkeitsbefunde. Die Korrekturen müssen die tatsächlichen Runnerpfade sowie alle historischen Anforderungen und Erwartungen erhalten.

## Akzeptanzkriterien

Private Ziele, Relayziel und Konfiguration begrenzen; Original280 IDs,124 Oracle-Mitgliedschaften, alle107 Provenance-Fingerprints und das historische Ledger exakt erhalten. Das tatsächliche zufällige private Engine-Socket-Unterverzeichnis und den effektiven Konfigurationspfad zulassen. Manipulationen und unsichere Pfade zurückweisen.

## Implementierungsentscheidung und Begründung

Provenance als explizite Pfad-/SHA-Datensätze speichern und vor der bestehenden unveränderlichen Digestprüfung in die ursprüngliche Zuordnung zurückführen; Code ohne Lockerung der Qualifikation aufteilen. Explizites CODEX_TEMP_ROOT und eigene physische Vorfahren verlangen. Authorization-Relay auf Loopback /authorize beschränken, Authorization-Response-Kapazität32768 und tatsächliche Opcode10-ACK-Fehlerinjektion erhalten. Engine-Sockets behalten das vom Runner erzeugte mode0700-Unterverzeichnis; die Konfiguration liegt unter /task/runtime/effective-config/traefik-forwardauth-dynamic.yaml.

## Geänderte Dateien

Nur Traefik-Inventur, native/Auth-Pythonproducer und ihre vier EN/DE-READMEs; i12_ledger.py; drei vorhandene I12-Testmodule und neuer test_traefik_i12_quality_controls.py; dieser Bericht. Gemeinsame Generatoren, Originalmatrix, Produktcode und Framework-/MRTS-Gitlinks bleiben durch diesen Commit unverändert.

## Ausgeführte Befehle

Root führte rtk proxy env TMPDIR=<short-private-external> CODEX_TEMP_ROOT=<configured-external> /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_traefik_i12_ledger tests.test_traefik_i12_auth tests.test_traefik_i12_native_measurements tests.test_traefik_i12_quality_controls aus:40 Tests bestanden. Kontrollen für Inventur- und historische Ledger-Äquivalenz bestanden. git diff --check bestand. Exakte Belege liegen im externen Lauf i12-traefik-acceptance-20261015/quality und checks/quality-root-i12.json.

## Security-Auswirkung

Keine Lockerung von Security-Gate, Admission, Namespace, UID, Capabilities, Symlink- oder Read-only-Grenzen. Neue Pfadprüfungen verlangen physische eigene Verzeichnisse und begrenzte reguläre Eingaben. Keine Issue-Akzeptanz, Suppression oder Scanner-Ausnahme wird eingeführt.

## Runtime-Evidence

Dies sind Producer- und Qualifikationsregressionen. Die unabhängige Prüfung fand zwei vor Auslieferung korrigierte Reparaturregressionen: Zurückweisung des gültigen zufälligen UDS-Unterverzeichnisses und einen falschen festen Konfigurationspfad. Positivkontrollen mit tatsächlicher Runner-Allokation/Socket und erzeugtem Treiber decken diese ABIs jetzt ab. Kein neuer Hostlauf und keine Original-ID-Hochstufung werden behauptet.

## Bekannte Einschränkungen

Vollständige Hostabnahme und finale gehostete Sonar-Ergebnisse bleiben Anforderungen der fortgesetzten PR413-Arbeit. Lokale Quellkorrekturen belegen kein grünes gehostetes Gate.

## Verbleibende Risiken

Neue Abnahmeproducer müssen weiterhin aktuelle Capture-/Observer-Verträge verwenden und physische fallbezogene Belege erzeugen. Das unveränderliche historische Ledger bleibt von der Qualifikation der aktuellen Revision getrennt.

## Nicht ausgeführte Prüfungen mit Begründung

Der vollständige EN/DE-/Link-Make scheiterte zunächst an22 fehlenden Framework-Linkzielen im isolierten Checkout; die Ausgabe bleibt erhalten. Gezielte Prüfungen aller vier geänderten READMEs bestanden. Vollständige Prüfungen verwenden den zugelassenen privaten schreibgeschützten Framework-Mount; Submodulschreibzugriff oder Gitlink-Update sind nicht erforderlich.

## Finaler Diff- und Review-Status

Die unabhängige Read-only-Prüfung bestätigte verlustfreie Inventurnormalisierung und historische Ledger-Äquivalenz. Root prüfte die endgültige Korrektur und wiederholte ihre40 Tests. Veröffentlichung durch normale Commits; kein automatischer Merge und keine History-Umschreibung.
