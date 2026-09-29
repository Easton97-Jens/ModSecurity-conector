# Befundgebundene NGINX-Entscheidungspriorität und Quellenregister

**Sprache:** Deutsch | [English](CR-20260929-findings-remediation.md)

## Identität

| Feld | Wert |
| --- | --- |
| Change ID | `CR-20260929-findings-remediation` |
| Date (UTC) | 2026-09-29 |
| Parent-Basisrevision | `d56af0856507eb048987974d3960e301e7c24371` |
| Quellbefund | `B09` / `csf_110c7b683d38cd566861364f` |
| Lieferziel | Separater aufgabeneigener Draft-PR; kein Merge |

## Motivation und Problemstellung

Der Nutzer verlangt eine quellengebundene Bearbeitung der gelieferten Befunde
und je ausgewähltem Repository einen Draft-PR. Dies ist die erste begrenzte
Implementierung, keine Behauptung, alle 59 konsolidierten Arbeitseinträge seien
behoben.

Das reine [Quellen-ID-Register](../findings/20260929-intake.json) erhält alle
72 Originaleinträge, deren gemeldete Schweregrade, Export-Hashes und die
vereinbarte Zuordnung zu 59 Arbeitseinträgen. Rohberichte, private Pfade,
Payloads und Autoreninformationen werden nicht veröffentlicht. A08 gehört zu
zwei getrennten Connector-Einträgen; Teilüberschneidungen bleiben sichtbar,
statt unabhängige Body- oder Stream-Grenzen zu entfernen. Frühere Bewertungen
im Gespräch sind keine neue Verifikation und schließen oder senken hier
keinen Quellbefund.

## Abnahmekriterien

- Eine positive native Intervention bleibt auch bei einer Fehlerseite aktiv.
- Negative native Ergebnisse behalten die bestehende Fail-Closed-Behandlung.
- Ein P1-Ergebnis null führt auch bei einer Fehlerseite weiter zu P2.
- Reguläres Verhalten ohne Intervention und native Fehlerbehandlung bleiben erhalten.
- Der separate P2-Ergebnispfad darf positive Ergebnisse nicht unterdrücken.
- Request-, Terminalzustands- und Fehlerprüfungen bleiben erhalten.
- Das ursprüngliche native Fehlerseiten-Routingszenario benötigt vor einer
  Verifikation von B09 weiterhin einen gepinnten Live-Host-Regressionstest.

## Implementierungsentscheidung und Begründung

Der gemeinsame Klassifizierer leitet die Engineentscheidung nicht mehr aus
dem allgemeinen Fehlerseitenmarker ab. Ein P1-Ergebnis null bleibt ALLOW,
damit die Request-Body-Prüfung ausgeführt wird. P1- und P3-Aufrufer verwenden weiterhin diesen
Klassifizierer. Der unabhängige P2-Pfad kehrt nicht mehr allein wegen des
Markers früh zurück; Fehler-, Entscheidungsereignis- und Terminalbehandlung
bleiben erhalten.

Der neue C17-Regressionstest kompiliert den tatsächlichen Klassifizierer und
die tatsächlichen P1-/P2-Ergebnisabschnitte mit kontrollierten nativen Rückgaben
und Ereignissenken-Doubles. Er deckt positive 302/403/451-, Null- und negative
Ergebnisse mit gesetztem sowie gelöschtem Marker ab. Dies ist kein laufender
NGINX- oder libmodsecurity-Integrationstest.

Ein unabhängiger Registertest prüft alle 72 Quellaliase und die 59er-Zuordnung.
Ein begrenzter GitHub-Workflow mit Leserechten führt diese Tests am PR-Head aus
und verwendet bereits vorhandene Action-Pins. Bestehende Pflichtprüfungen,
Berechtigungen, Dependency-Locks und Quality Gates werden nicht verändert.

## Sicherheits- und Kompatibilitätsauswirkung

Eine echte Block-/Redirect-Entscheidung gilt nicht mehr allein deshalb als
abwesend, weil NGINX eine Fehlerseite verarbeitet. Ein P1-Ergebnis ohne
Intervention überspringt bei Fehlerseiten P2 nicht mehr. Wiedereintritt bei Fehlerseiten und tatsächliches Host-/
Clientverhalten benötigen weiterhin Live-Host-Nachweise. Nicht unterstützte
Streaming-, Endpunkt-, Socket-, Supply-Chain- oder andere Connector-Pfade
werden hier nicht geändert.

Die unabhängigen Draft-PRs #382 und #370 enthalten überlappende NGINX-Arbeit.
Deren Branches und Nachweise werden nicht geändert oder übernommen. Eine
Integration erfordert einen späteren geprüften Abgleich; ein anderer grüner
Check verifiziert diesen Draft nicht.

## Geänderte Dateien und Tests

- `connectors/nginx/src/ngx_http_modsecurity_common.h`
- `connectors/nginx/src/ngx_http_modsecurity_access.c`
- `tests/test_nginx_error_page_intervention.py`
- `tests/test_security_finding_intake.py`
- `.github/workflows/ci-findings-regressions.yml`
- `reports/audits/findings/20260929-intake.json`
- Dieses englisch/deutsche Change-Record-Paar.

## Befehle und Ergebnisse

| Prüfung | Tatsächlicher Stand bei Vorbereitung |
| --- | --- |
| GitHub-Basisdateiübernahme | Beide vollständigen C-Dateien stimmten vor Änderung mit ihrem Git-Blob-SHA-1 überein |
| Begrenzter Quellvergleich | Nur die genannten Klassifizierer-/P2-Änderungen; keine fremden Quelländerungen |
| Python-Syntax / Register-JSON | Als Daten geparst; keine Ausführung der neuen Tests |
| Lokale kompilierte/Unit-Regression | NOT RUN: verpflichtender RTK-Wrapper nicht verfügbar |
| Lokaler nativer Build / Live-Host | NOT RUN: kein vollständiger Checkout oder Host-Build; GitHub-DNS-Download gescheitert |
| Natives git diff --check | NOT RUN; Whitespace neuer Zeilen wird separat untersucht |
| Neue GitHub-Regressionsjobs am exakten Head | Konfiguriert, Ergebnis ausstehend; PR-Checks prüfen |
| Gesamte CI / SonarQube / Securityscan | Durch diesen Change Record nicht als erfolgreich behauptet |

Der verfügbare Code-Work-Skill wurde gelesen. Der im Repository referenzierte
globale Ausführungsskill war in dieser Umgebung nicht zugänglich. Kein lokaler
Projektbefehl wurde stillschweigend anstelle des verpflichtenden RTK-Pfads
ausgeführt.

## Verbleibende Arbeit und Zuständigkeit

B09 ist ein Kandidatenpatch, nicht verifiziert oder geschlossen. Alle übrigen
Parent-Arbeitseinträge bleiben in diesem Draft unverändert. Die Framework-
Mitigation am B03-Eingang wird separat geliefert; der ursächliche Code gehört
MRTS und wird nicht geändert.

Parent- und Framework-Commits/PRs bleiben unabhängig. Beide Gitlinks bleiben
unverändert. Dieser Record autorisiert weder Default-Branch-/Force-Push,
Merge, Risikoakzeptanz, Rohscan-Veröffentlichung noch abgeschwächte Gates.
