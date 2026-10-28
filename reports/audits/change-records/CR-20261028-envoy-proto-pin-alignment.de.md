# Change Record: CR-20261028-envoy-proto-pin-alignment

**Sprache:** [English](CR-20261028-envoy-proto-pin-alignment.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261028-envoy-proto-pin-alignment |
| Datum (UTC) | 2026-10-28 |
| Basis-Revision | `32b63db8ae38fbec20e5609495171b19373e17d6` |

## Motivation und Problemstellung

Nach Reparatur der Inventarzulassung in PR #429 erreichten Envoy-Vertrags- und CRS-Runtime-Jobs den Build-Preflight und lehnten die gepinnte Go-Proto-Version ab. Der Parent-Lock enthielt noch v1.37.0, während die bereits genehmigte go.mod github.com/envoyproxy/go-control-plane/envoy v1.40.0 verlangte. Die Basis b8f76fd718bf26dd3a4345dd6700534690d8a49d hat dieselbe Abweichung.

## Akzeptanzkriterien

Den Parent-Proto-Lock mit dem genehmigten Manifest abgleichen und dabei exaktes natives Build-Gate und bestehende Sicherheitsuntergrenzen erhalten. Eine Konsistenzregression ergänzen, Modul-/Abhängigkeitsdateien und sämtliche Inventarauswahlen erhalten und abgeleitete Artefakte über den nativen Erzeuger regenerieren.

## Implementierungsentscheidung und Begründung

ENVOY_GO_PROTO_VERSION auf v1.40.0 anheben. Die bestehende Abhängigkeitsregression verlangt jetzt exakt eine offizielle Modul-/Versionszuweisung und Gleichheit mit der geparsten go.mod-Anforderung. Die Framework-Synchronisierung besitzt in diesem Vertrag nur ENVOY_RELEASE/ENVOY_IMAGE und erhält deshalb den Parent-Proto-Pin.

## Geänderte Dateien

connectors/envoy/config/envoy-ext-proc-versions.env; tests/test_ci_security_workflows.py; config/testing/active-cases.json; reports/testing/test-selection-archive.generated.json; dieses EN/DE-Change-Record-Paar. Nur zwei geprüfte Quellbindungen ändern sich. Compiler-Guides wurden regeneriert und blieben byteidentisch.

## Ausgeführte Befehle

Alle Projekt-Shell-Befehle verwendeten das aufgabeneigene RTK v1.0.1 bypass. Drei gezielte Workflow-/Abhängigkeitsmethoden bestanden unter Python 3.15.1. Die neue Konsistenz-Assertion scheiterte mit altem v1.37.0 und bestand mit v1.40.0. Der Hauptagent führte den unveränderten Precompile-Shell-Block gegen die tatsächliche go.mod aus: alter Pin Exit 2 mit gehosteter Diagnose, korrigierter Pin Exit 0. Native Compiler-Guide-Erzeugung und git diff --check bestanden. Native Archivregenerierung folgte den zwei geprüften Quellbindungsänderungen. Vollständige Zulassung (100 Standard / 1893 auf Abruf), Archiv --check, EN/DE-Dokumentation, 103 Variablenreferenzen, Repository-/Dokumentationslinks und Whitespace bestanden.

## Security-Auswirkung

Die exakte Proto-Pin-Prüfung und bestehenden Sicherheitsuntergrenzen für Abhängigkeiten bleiben aktiv. Keine Änderungen an Go-Modul/Sum, Compiler, Sanitizer, nativem Quellcode, Berechtigungen, Zugangsdaten oder Isolation. Die Regression erkennt künftige einseitige Manifest-/Lock-Abweichungen, statt eine ungeprüfte Abweichung zuzulassen.

## Runtime-Evidence

Vertrags-Jobs 122787881979 und 122787859265 sowie CRS-Runtime-Job 122787881189 melden am Head cef2ab5ee8fe35e316620acbee5d9eb2f0f73bf3 ausdrücklich denselben Precompile-Widerspruch. Native-Security-Job 122791600138 meldet build_ext_proc.sh Exit 2 mit verborgenem innerem stderr; die Zuordnung zum gleichen Preflight ist eine Schlussfolgerung. Lokale Evidence beweist nur die exakte Precompile-Grenze, keinen vollständigen nativen Build oder gehostete Runtime.

## Bekannte Einschränkungen

Der vollständige native Envoy-Build lief lokal nicht: Go war nicht auf PATH verfügbar und ein lokales ModSecurity-SDK mit Headern/Bibliotheken fehlte. Keine Pakete wurden installiert. Neue gehostete CI am tatsächlichen Head bleibt erforderlich.

## Verbleibende Risiken

Spätere unabhängige native Build-/Runtime-Fehler bleiben möglich und benötigen eigene Evidence. Dependabot-Änderungen dieser Proto-Abhängigkeit müssen die zugehörige Parent-Lock-Änderung mitführen; der neue Konsistenztest macht Abweichungen sichtbar.

## Nicht ausgeführte Prüfungen mit Begründung

Keine zusätzliche Connector-Matrix, I12-Qualifizierung oder breite Security-Prüfung. Bestehende gehostete CI ist die vollständige native Build-/Runtime-Validierungsgrenze; lokaler Manifest-/Precompile-Erfolg ersetzt sie nicht.

## Finaler Diff- und Review-Status

Der begrenzte Diff ändert einen Parent-Pin und ergänzt zehn Assertion-/Setup-Zeilen einer bestehenden Regression samt abgeleiteten Hash-Begleitdateien und gepaarter Traceability. Keine reader-facing Compiler-Guide-Inhalte änderten sich. Finaler Veröffentlichungs-/Prüfstatus bleibt an den tatsächlichen PR-Head gebunden.
