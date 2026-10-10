# Change Record: CR-20261008-native-unit-fixture-boundaries

**Sprache:** [English](CR-20261008-native-unit-fixture-boundaries.md) | Deutsch

Begrenzte Fixture-Korrekturen; lokale Unit- und Namespace-Evidence.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-native-unit-fixture-boundaries |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `06df37a5fc8963bdc8c9c5577d602b9861e4bb4d` |

## Motivation und Problemstellung

Der Legacy-Routen-Unit-Replay änderte seine Fixture unbemerkt nicht mehr, nachdem Prefix-Erhaltung den Routenblock erweitert hatte. Ein echter Namespace-Jail-Test verwendete fest /tmp statt des geforderten externen Task-TMPDIR.

## Akzeptanzkriterien

Den veralteten Replay-Fehler reproduzieren, genau eine tatsächliche Routenzuweisung mit Änderungsassertions transformieren, Routenerwartungen erhalten und den vollständigen echten Jail-Test unter konfiguriertem Temporärspeicher ohne schwächere Isolation ausführen.

## Implementierungsentscheidung und Begründung

Der Replay ersetzt nur die exakte native host_script-Zuweisung durch die Legacy-Framework-Zuweisung; er verlangt genau einen Quelltreffer, geänderte Fixture und Abwesenheit der Originalzuweisung. Produktrouting und Prefix-Kontrollen bleiben unverändert. Namespace-TemporaryDirectory folgt TMPDIR; der Kommentar erläutert physische Hostpfad-Ablehnung ohne feste /tmp-Annahme.

## Geänderte Dateien

Nur tests/test_nginx_selected_configtest_wiring.py, tests/test_run_readonly_submodule_validation_namespace.py und dieser zweisprachige Record. Die freigegebene vorhandene Integrationsabhängigkeit 9cfae553 wurde regulär übernommen, um aktuelle Quellen zu reproduzieren; sie gehört nicht zum neuen Delivery-Diff.

## Ausgeführte Befehle

RTK-verpackter Replay-Test scheiterte vor der Korrektur (RED). Das vollständige Selected-Configtest-Wiring-Modul bestand 17 Tests in 6,998 Sekunden. Fünf inspizierte Namespace-Prüfungen außerhalb der UID0-only-Sandbox bestanden nach Diff-Inspektion in 0,396 Sekunden ohne Skips. Neutraler kurzer externer Task-TMPDIR/Cache wurde verwendet. Der Generator lehnte zuerst eine kurze Basisrevision ab; der Aufruf mit vollständiger40-SHA erzeugte das korrekte Paar.

## Security-Auswirkung

Die Fixture-Transformation kann nicht still zum No-op werden. Namespace-Jail, UID-Drop, Schließen geerbter Deskriptoren, verbotene Host-/Quell-/Git-Schreibzugriffe, Read-only-Runtime, PID1 und Lebensdauer von Hintergrundprozessen bleiben unverändert geprüft. Keine /tmp-Ausnahme oder Gate-Aufweichung.

## Runtime-Evidence

Nur echte lokale Berechtigungs- und Namespace-Unit-Proben. Die fünfte Prüfung verwendet den tatsächlichen privaten Jail und nobody. Das ist keine NGINX-Runtime-, Compiled-Artifact-Authority-, Protected-Workflow- oder kanonische PASS-Evidence.

## Bekannte Einschränkungen

UID-/GID-Zuordnungen außerhalb der Sandbox werden für das vorhandene nobody-Konto benötigt; EINVAL in der eingeschränkten Sandbox belegt keine Host-Unfähigkeit. Kernel-Namespace-Support bleibt explizite vorhandene Voraussetzung und wird nicht umgangen.

## Verbleibende Risiken

Übereinstimmende integrierte Parent-/Framework-Pins und autorisierte native Builds/Runtime bleiben getrennte Koordinator-Gates. Bestehende ShellCheck-Warnings und fremde Dependency-Skips werden hier nicht behoben.

## Nicht ausgeführte Prüfungen mit Begründung

Keine nativen Builds/Runtime, Protected-Pipeline, Framework-/MRTS-Änderung, Pin-Updates, Installation oder Produktrouting-Quelländerung. Prüfungen außerhalb dieses begrenzten Fixture-Slice werden nicht behauptet.

## Finaler Diff- und Review-Status

Nur die beiden freigegebenen Test-Diffs und der generierte zweisprachige Record geprüft. Vorhandene Quellen und fremde Commits erhalten; ein separater normaler fokussierter Commit enthält keine übernommene Abhängigkeit.
