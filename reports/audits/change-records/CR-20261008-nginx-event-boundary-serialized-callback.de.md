# Change Record: CR-20261008-nginx-event-boundary-serialized-callback

**Sprache:** [English](CR-20261008-nginx-event-boundary-serialized-callback.md) | Deutsch

Begrenzte Korrektur des serialisierten Events; kein aktueller nativer Runtime- oder E2E-Nachweis.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-event-boundary-serialized-callback |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `1940c1dbda6b371248a37f257c19df9b60fd836d` |

## Motivation und Problemstellung

Der Common-Serializer schreibt `rule_match`/`allow`, nicht `request_rule_match`/`pass` aus der Producer-Struktur. Der Event-Boundary-Driver übersieht sonst den echten Rule1100402-Callback vor der strikten Framework-Prüfung.

## Akzeptanzkriterien

Den tatsächlich serialisierten Phase1-Rule1100402-Callback auswählen. Falsche Rule, alter Strukturname und ungültiges JSON bleiben abgewiesen. Originale JSONL-Bytes und bestehende Source-, Host-, Metadatenlimit- und Canonical-Prüfungen erhalten.

## Implementierungsentscheidung und Begründung

Nur das Eventnamen-Prädikat auf `rule_match` korrigieren. Die kontrollierte Allow-Fixture entspricht dem Serializer; der alte Strukturname wird ausdrücklich abgewiesen. Keine Common-/Produktsemantik ändern oder Ersatzevents erzeugen.

## Geänderte Dateien

`ci/runtime/lifecycle/run-nginx-event-boundary-cases.py`, `tests/test_nginx_event_boundary_driver.py` und dieses generierte EN/DE-Record-Paar.

## Ausgeführte Befehle

Der kontrollierte Test des echten serialisierten Callbacks war zunächst rot (null Callbacks). Danach bestanden drei kontrollierte Tests mit `rtk proxy ... python -m unittest tests.test_nginx_event_boundary_driver`, Exit0. Die zusätzliche Negativkontrolle des alten Namens wird vor dem Commit erneut ausgeführt. Archiv- und Whitespace-Prüfungen dokumentiert der Koordinator; dieses Record behauptet keinen späteren Lauf.

## Security-Auswirkung

Korrektur der Evidence-Treue, keine Sicherheitsbehebung. Keine Prüfungen oder Limits entfallen; der strikte Framework-Reader prüft weiterhin Callback-Identität, Phase, Rule, Originalbytes und explizite Source-/Artefakt-Autorität.

## Runtime-Evidence

Keine für diesen Commit. Kontrollierte Fixtures sind keine Runtime-Events. Alle97 selected Required Records bleiben unverändert; die45 ursprünglichen Lücken benötigen den finalen integrierten Runtime-Nachweis.

## Bekannte Einschränkungen

Das Driver-Prädikat ist keine Canonical-Akzeptanz. Frisches sourcegebundenes Modul/Binary, echte Root/nobody-Invocations, vollständige Events und Offline-Validierung bleiben erforderlich.

## Verbleibende Risiken

Finaler nativer E2E und remote revisionsgebundene CI/Sonar sind offen. Der Draft-PR bleibt Draft; geschützte Trusted Base/Host-Administration ist eine getrennte offene Schicht.

## Nicht ausgeführte Prüfungen mit Begründung

Kein nativer Build oder vollständiger E2E, solange die zentrale Canonical-Integration offen ist. Vollständiger Lint ist nicht zertifiziert; fehlende Werkzeuge werden nicht installiert.

## Finaler Diff- und Review-Status

Nur Prädikat, fokussierte Fixture/Negativkontrolle und generiertes Paar. Keine Gitlink-, MRTS-, generischen Validator- oder Guardrail-Änderungen. Der Koordinator prüft den gestagten Diff vor einem separaten normalen Commit.
