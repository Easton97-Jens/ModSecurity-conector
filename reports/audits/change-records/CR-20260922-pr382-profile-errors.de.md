# Change Record: modusunabhängige technische Fehler

**Sprache:** [English](CR-20260922-pr382-profile-errors.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260922-pr382-profile-errors` |
| Datum (UTC) | `2026-09-22` |
| Basis-Revision | `97d3ea10d526f8ab306bc1cc24fa63f573f36bc9` |

## Motivation und Problemstellung

Die Common-Transaktionspolicy wandelte technische Fehler im Safe-Modus und nach
Antwortbeginn ausdrücklich in `log_only`/`fail_open` um. Das widersprach der
gewünschten nativen Fehlersemantik. Veraltete Engine-Entscheidungstypen konnten
außerdem einen ausdrücklichen Fehlerstatus an der Vertragsgrenze verdecken.

## Akzeptanzkriterien

Engine-Timeout/-Nichtverfügbarkeit/-ungültige Antwort, Connector- und
Protokollfehler müssen in beiden Vertragsmodi terminal bleiben. Vor Antwortbeginn
Deny/Fail-closed, danach Error/Stop-I/O wählen, keine zweite HTTP-Antwort oder
erfundene Resetfähigkeit. Ursache, Antwortstatus, erster Fehler, Bereinigung und
alle gültigen Regelentscheidungs-Policies erhalten.

## Implementierungsentscheidung und Begründung

Vorhandene Entscheidungspolicy korrigieren und ausdrücklichen Fehlerstatus bei
Engine-zu-Vertrag-Klassifikation vorziehen. Kein weiterer Modusschalter und keine
Änderung der Profilfähigkeiten. Nur alte technische Fail-open-Erwartungen im
vorhandenen C-Test anpassen; seine übrigen Assertions bleiben erhalten.

## Geänderte Dateien

- `common/src/transaction_state.c`
- `tests/transaction_phase_contract_test.c`
- `tests/test_pr382_profile_errors.py`
- `.github/workflows/lint.yml`
- Dieser Bericht und seine englische Begleitdatei.

## Ausgeführte Befehle

Der ergänzte CI-Einstieg lautet:

```sh
python -m unittest -v tests.test_pr382_profile_errors
```

Er kompiliert echten Common-Zustand und die connector-eigene Registry und prüft
200 Fälle: zehn tatsächliche Profildefinitionen, zwei Vertragsmodi, zwei Zustände
des Antwortbeginns und fünf technische Ursachen. Vier Testmethoden prüfen Fälle,
Ursachen-/Bereinigungserhalt sowie unveränderten Status und Fähigkeiten. Ausführung
steht bei Vorbereitung aus. Der vollständige bestehende C-Vertragstest bleibt im
zuständigen CI-Ziel.

## Security-Auswirkung

Fehlgeschlagene Untersuchung erhält im Safe-Modus keine Fail-open-Erlaubnis mehr.
Nach Antwortbeginn fordert der Vertrag keinen neuen Antwortstatus an. Konkrete
Adapter bleiben für Transportabbruch zuständig; keine nicht unterstützte
Resetfähigkeit und keine schwächeren Scanner-, Zugriffs- oder Ressourcengrenzen.

## Runtime-Evidence

Die Tests verwenden öffentliche Common-Lebenszyklus-APIs samt Companion-Phasen-
Übergabe/-Übernahme, Fehler, Wiedereintritt und Bereinigung. Dies sind keine zehn
Live-Integrationen. Der separate Host-/Transport-/Ausgabevergleich bleibt erforderlich.

## Bekannte Einschränkungen

Dies schließt die identifizierte Common-Policy-Lücke, nicht jede Hostübersetzung
oder Ereignis-/Ausgaberoute aus I09-I12. Native Fehler- und Logausgabe-Eigentümer
benötigen eigene Verifikation. Der separate Secret-Scan-Fund bleibt offen.

## Verbleibende Risiken

Das alte technische Fail-open-Verhalten entfällt bewusst. Installationen, die
bei Engine-Ausfall weiterliefen, müssen Ablehnung oder gestoppte Ein-/Ausgabe
berücksichtigen. Gültiges ausdrückliches Log-only und späte Regel-Policies bleiben gleich.

## Nicht ausgeführte Prüfungen mit Begründung

Keine lokalen Projektbefehle, da der vorgeschriebene RTK-Wrapper fehlt. End-Head-CI,
exaktes Sonar null und echte Transportergebnisse benötigen eigene Verifikation.
Ein unveränderter Fähigkeitswert ist kein Hosttest.

## Finaler Diff- und Review-Status

Als atomare Code-/Teständerung in Draft-PR #382 vorbereitet, bei erhaltener paralleler
Arbeit. Kein Merge, Master-Push, Force-Push, keine Abhängigkeits-/Framework-/MRTS-Änderung.
