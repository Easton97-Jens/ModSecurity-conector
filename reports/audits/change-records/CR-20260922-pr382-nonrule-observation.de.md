# Change Record: Beobachtungsparität für Nicht-Regel-Ereignisse

**Sprache:** [English](CR-20260922-pr382-nonrule-observation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260922-pr382-nonrule-observation` |
| Datum (UTC) | `2026-09-22` |
| Basis-Revision | `7fe606c56a423f05454fe200f07a1c03d007ea3f` |

## Motivation und Problemstellung

Bei I11 konnten Body-Limit-, Unsupported-Capability-, Client-Cancel- und
Upstream-Disconnect-Ereignisse weiterhin eine ausgeführte Aktion behalten, obwohl
der Transportnachweis NULL, leer oder `not_observable` war. Regel- und technische
Fehlerereignisse behandelten diesen fehlenden Nachweis bereits. Gemeinsame
Serialisierung allein vereinheitlichte diese übrigen Ereigniskategorien nicht.

## Akzeptanzkriterien

Unbeobachtete tatsächliche Aktionen dieser bekannten Kategorien leeren, ohne
Ereigniskennung, Fehler-/Policy-Klasse, angeforderte Aktion, Phase,
Statusbeobachtungen, Bytezähler oder Transportflags zu verändern. Beobachtete
Aktionen und anwendungseigene Ereignisse erhalten. Echter JSONL- und
Integritätscode müssen übereinstimmen und idempotent bleiben. Eine Negativkontrolle
muss die fehlende Prüfung sichtbar machen.

## Implementierungsentscheidung und Begründung

Ein kleiner Beobachtungshelfer läuft nach der kategorienspezifischen
Normalisierung und vor der abschließenden Meldungsauswahl. Hostfähigkeiten, Modi,
Wiederholungsregeln der Ausgabe, öffentliches Ereignislayout und Parserwerte
bleiben unverändert. Nicht-disruptive Rule-Match-Einträge behalten ihre bisherige
Diagnosesemantik. Dies ist ein I11-Teilschritt, kein Abschluss aller Erzeuger und
physischen Logausgaben.

## Geänderte Dateien

- `common/include/msconnector/event_protocol.h`
- `tests/test_event_transport_observation.py`
- Dieser Bericht und seine englische Begleitdatei.

Der vorhandene fokussierte Lint-Schritt führt das erweiterte Testmodul bereits aus.

## Ausgeführte Befehle

Der CI-Einstiegspunkt lautet:

```sh
python -m unittest -v tests.test_event_transport_observation
```

Die Ausführung steht bei Vorbereitung aus. Zehn Testmethoden umfassen fünf
Nicht-Regel-Szenarien, drei Abwesenheitsmarker, beobachtete Kontrollen,
phasenspezifische Ursachen, familienunabhängige Serialisierung und eine kompilierte
Negativkontrolle mit entfernter Prüfung. Die Testdatei prüft echte JSONL-/Hash-
Gleichheit, Idempotenz und erhaltene Metadaten. Dieser erste Bericht behauptet
kein abgeschlossenes CI- oder Sonar-Ergebnis.

## Security-Auswirkung

Ein Policy-Limit oder getrennter Peer beweist keine Durchsetzung einer
angeforderten Hostaktion. Diese Änderung entfernt die falsche Behauptung.
Ursprüngliche Eingabevalidierung, Query-Redaktion und Ablehnung nicht unterstützter
Profile bleiben unverändert. Scannerbefunde und Akzeptanzschwellen werden nicht
unterdrückt oder verändert.

## Runtime-Evidence

Die Tests kompilieren echten Common-Serializer-/Hash-Code mit kontrollierten
Metadaten. Familiennamen sind keine sechs laufenden Hosts. Konkrete
Adapterdurchsetzung und physische Öffnungs-/Schreib-/Kurzschreibfehler benötigen
eigene Nachweise.

## Bekannte Einschränkungen

I09-I12 bleiben an ihre umfassenderen Akzeptanzkriterien gebunden. Dieser Patch
repariert nicht alle Erzeuger mit nichtleerem, aber unzutreffendem
Beobachtungsmarker. Er belegt keine vollständige direkte/Companion-/Middleware-/
Sidecar-Matrix.

## Verbleibende Risiken

Auswerter müssen auch für diese weiteren bekannten Ereignistypen eine leere
tatsächliche Aktion akzeptieren. Normalisierte Integritätswerte ändern sich
entsprechend; historische Einträge benötigen passende Erzeuger-/Prüferversionen.
Frühere Clientergebnisse werden nicht erfunden.

## Nicht ausgeführte Prüfungen mit Begründung

Wegen des fehlenden vorgeschriebenen RTK-Wrappers wurden keine lokalen
Projektbefehle ausgeführt. Verifikation nutzt frische GitHub-CI; Sonar null für
den endgültigen Head bleibt erforderlich. Der unabhängige Secret-Scan-Fund und
Live-Host-Kriterien bleiben offen.

## Finaler Diff- und Review-Status

Atomare Quellcode-/Test-/Dokumentationsfortsetzung in Draft-PR #382. Parallele
NGINX-/Common-Änderungen bleiben erhalten. Kein Merge, Master-Push, Force-Push,
Abhängigkeits- oder Framework-/MRTS-Update ist enthalten.
