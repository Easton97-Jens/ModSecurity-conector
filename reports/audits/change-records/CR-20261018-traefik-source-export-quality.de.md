# Change Record: CR-20261018-traefik-source-export-quality

**Sprache:** [English](CR-20261018-traefik-source-export-quality.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-traefik-source-export-quality |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `a29019558678222b88913be0e202db3c9d14323a` |

## Motivation und Problemstellung

Der exakt veröffentlichte PR-#413-Head `a29019558678222b88913be0e202db3c9d14323a` erhielt Sonar python:S3776 für `validate_destination` (Komplexität 17, Grenze 15) und python:S1172 für den ungenutzten Parameter `profile` von `refresh_capture_source`.

## Akzeptanzkriterien

Alle Prüfungen für externe Speicherwurzel, physischen Pfad, Vorfahren, Symlinks, Git-Marker, Eigentümer und private Modi bleiben mit gleicher Reihenfolge und Speichergrenze erhalten. Der ungenutzte private Parameter und das Argument seines einzigen internen Aufrufers entfallen. Committete Quellbytes, Dateimodi, Gitlinks und Quellmanifeste bleiben erhalten.

## Implementierungsentscheidung und Begründung

Die bestehenden Prüfungen je Vorfahr werden in `validate_private_ancestor` ausgelagert. Der Aufrufer läuft weiterhin vom Ziel bis zur konfigurierten Speicherwurzel, prüft jeden Vorfahr vor dem Stopp und untersucht keine darüberliegenden Pfade. Der Helper behält dieselben Symlink-, UID-/Modus- und Git-Marker-Prüfungen unterhalb der Wurzel. Dem nativen Preparer entfällt nur ein ungenutztes Argument; profilabhängiges Fixture-Staging bleibt unverändert.

## Geänderte Dateien

- `connectors/traefik/harness/i12/source_export.py`.
- `connectors/traefik/harness/i12/native/prepare.py`.
- `tests/test_traefik_i12_source_export.py`.
- Dieses EN/DE-Change-Record-Paar.

## Ausgeführte Befehle

Alle Befehle nutzten RTK und das Parent-Virtualenv. Neun Source-Export-Charakterisierungstests bestanden vor dem Refactor. Anschließend bestanden mit `python -m unittest tests.test_traefik_i12_source_export tests.test_traefik_i12_native_measurements tests.test_traefik_i12_auth tests.test_traefik_i12_ledger` 34 Tests. Zusammen mit den Modulen für zweisprachige Dokumentation und Change Records bestanden 76 Tests in 5,706 Sekunden. AST-Syntax für drei Python-Dateien, Change-Record-Struktur und `git diff --check` bestanden. Exakte gewrappte Befehle und Quellhashes bleiben unter `source-export-quality/after.json` im externen Aufgabenverzeichnis erhalten.

## Security-Auswirkung

Keine Admission- oder Pfadprüfung wird entfernt oder abgeschwächt. Neue Kontrollen prüfen ein zulässiges privates verschachteltes Ziel, gruppenschreibbare Vorfahren, fremde UID, normale und ins Leere zeigende Git-Symlink-Marker, Symlink-Vorfahren und die Speicherwurzel selbst als Ziel. Vorhandene Prüfungen für committete Objekte, Inventur und Überschreibschutz bleiben erhalten.

## Runtime-Evidence

Diese Tests prüfen physische Dateisystem-Fixtures und committeten Quellexport ohne Hoststart oder Repository-Mutation. Sie qualifizieren keine Hosttransaktionen und verändern keine historische I12-Evidenz.

## Bekannte Einschränkungen

Lokale Tests prüfen Verhaltenserhalt und Aufrufkompatibilität. Erst eine frische gehostete Sonar-Analyse kann die Abwesenheit dieser beiden Befunde am nächsten veröffentlichten Head belegen.

## Verbleibende Risiken

Der getrennte S5332-Befund und der HAProxy-Fixture-Kompilierfehler liegen bei der übergeordneten Aufgabe. Diese begrenzte Änderung behauptet keinen gesamten CI- oder Sonar-Erfolg.

## Nicht ausgeführte Prüfungen mit Begründung

Keine Hosts, Scanner-Uploads, Git-Veröffentlichungen oder Sonar-Befundzustände werden ausgeführt beziehungsweise verändert. Die übergeordnete Aufgabe verantwortet integrierte Abschlusschecks und Veröffentlichung.

## Finaler Diff- und Review-Status

Der finale Diff beschränkt sich auf Helper-Extraktion, Entfernung des ungenutzten Parameters/Aufruferarguments, sinnvolle Grenzkontrollen und diesen Record. Andere Acceptance-Producer und Änderungen am Authorization-Relay bleiben bei ihren Verantwortlichen.
