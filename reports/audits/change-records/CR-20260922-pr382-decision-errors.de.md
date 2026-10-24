# Change Record: PR #382 gemeinsame Fehlergrenze für Entscheidungen

**Sprache:** [English](CR-20260922-pr382-decision-errors.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260922-pr382-decision-errors` |
| Datum (UTC) | `2026-09-22` |
| Basis-Revision | `1301a4e30f04cb82dd0546607bfaab1461671b7b` |
| Pull Request | [Draft #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382) |

## Motivation und Problemstellung

Der gemeinsame Hostaktionsmapper lieferte bei fehlender oder unbekannter
Entscheidung `log_only`. Eine Entscheidung mit ausdrücklichem Fehlerstatus
konnte einen früheren Allow-, Log-only- oder Regeltyp behalten. Der
Ereigniserzeuger wiederholte diesen veralteten Typ und behauptete eine tatsächliche
Hostaktion, obwohl lediglich eine Engine-Entscheidung vorlag.

## Akzeptanzkriterien

Fehlende/unbekannte Entscheidungen und ausdrücklicher Fehlerstatus müssen
`error` ergeben, nie erfolgreiche Safe-Beobachtung. Fehlerereignisse dürfen keine
veraltete Regel-ID enthalten. Gültige Entscheidungstypen, Body-Limit-Ablehnung und
konfigurierte HTTP-Fehlerstatus bleiben erhalten. Eine Entscheidung allein darf
keine beobachtete Hostaktion behaupten. Adapterspezifische Policy bleibt beim Eigentümer.

## Implementierungsentscheidung und Begründung

Den vorhandenen Common-Mapper und Erzeuger korrigieren, statt einen zweiten
routenspezifischen Klassifizierer einzuführen. Fehlerstatus hat Vorrang vor dem
Entscheidungstyp; unbekannte Typen ergeben Fehler. Allow-/Disruptive-Prädikate
folgen dieser Grenze. Der Ereigniserzeuger verwendet dieselbe Fehlerklassifikation
und lässt die tatsächliche Aktion für den beobachtenden Adapter leer. Keine Änderung
am Struct-Layout.

## Geänderte Dateien

- `common/src/decision_action.c`
- `common/src/decision.c`
- `tests/test_pr382_decision_safety.py`
- `.github/workflows/lint.yml`
- Dieser Bericht und seine englische Begleitdatei.

## Ausgeführte Befehle

Der ergänzte CI-Befehl lautet:

```sh
python -m unittest -v tests.test_pr382_decision_safety
```

Die Testdatei kompiliert echte Common-Entscheidungs-/Ereignisabhängigkeiten mit
C17 und `-Wall -Wextra -Werror` und prüft 23 Fälle in sieben Testmethoden. Bei
Commitvorbereitung steht die Ausführung aus; hier wird kein Erfolg behauptet.
Keine lokalen Projektbefehle, da der vorgeschriebene RTK-Wrapper fehlt.

## Security-Auswirkung

Eine fehlende oder fehlgeschlagene Kontrolle darf nicht still zu erfolgreicher
Beobachtung werden. Keine Scannerregeln, Rechte oder vorhandenen Tests werden
abgeschwächt; keine nicht unterstützte Strict-/Resetfähigkeit wird eingeführt.
Metadaten bleiben durch den Serializer begrenzt; keine Bodydaten in Ereignissen.

## Runtime-Evidence

Dies sind kompilierte Common-Grenztests, keine sechs Live-Server oder zehn
Routenintegrationen. Jede tatsächliche Route benötigt eigene Integrationsnachweise.

## Bekannte Einschränkungen

Dies ist ein Beitrag zu I10/I11, kein Abschluss von I09-I12. Übrige native API-,
Ausgabe-, Profil- und Transportanforderungen bleiben in der
[Hauptcheckliste](../../../docs/pr-382-checklist.de.md) offen.

## Verbleibende Risiken

Auswerter müssen `actual_action` als Beobachtung, nicht angeforderte Policy behandeln.
Aufrufer, die sich auf Log-only bei ungültigen Entscheidungen verließen, müssen nun
`error` behandeln. Gültige ausdrückliche Log-only-Entscheidungen bleiben erhalten.

## Nicht ausgeführte Prüfungen mit Begründung

Vollständige Host-/Transport-/Ausgabefehlerinjektion und End-Head-Sonar/CI sind durch
diese Quelländerung nicht nachgewiesen. Die exakte Sonar-Null-Prüfung bleibt aktiv.
Der separate Secret-Scan-Fund wird durch diese Änderung nicht zurückgewiesen.

## Finaler Diff- und Review-Status

Stand bei Vorbereitung: Implementierung vorhanden, Verifikation ausstehend. Arbeit
bleibt im eigenen Draft-PR. Kein Merge, Master-Push, Deployment, Abhängigkeits- oder
Framework-/MRTS-Schreibzugriff. Parallele Branch-Änderungen müssen erhalten bleiben.
