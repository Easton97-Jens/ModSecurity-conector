# Befundgebundene NGINX-Entscheidungspriorität und Quellenregister

**Sprache:** [English](CR-20260929-findings-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260929-findings-remediation` |
| Datum (UTC) | 2026-09-29 |
| Basis-Revision | `d56af0856507eb048987974d3960e301e7c24371` |
| Quellbefund | `B09` / `csf_110c7b683d38cd566861364f` |
| Lieferziel | Parent-Draft-PR #391; kein Merge |

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

Der zuerst veröffentlichte Workflow verwendete den runner-Kontext unzulässig
in Umgebungswerten auf Jobebene. Die CI-Korrektur verschiebt TMPDIR in den
ausführenden Schritt, in dem dieser Kontext unterstützt wird, ohne den
Regressionsbefehl zu entfernen. Der Change Record folgt nun dem vorhandenen
zweisprachigen Schema; Checker und Pflichtabschnitte werden nicht gelockert.

## Akzeptanzkriterien

- Eine positive native Intervention bleibt auch bei einer Fehlerseite aktiv.
- Negative native Ergebnisse behalten die bestehende Fail-Closed-Behandlung.
- Ein P1-Ergebnis null führt auch bei einer Fehlerseite weiter zu P2.
- Reguläres Verhalten ohne Intervention und native Fehlerbehandlung bleiben erhalten.
- Der separate P2-Ergebnispfad darf positive Ergebnisse nicht unterdrücken.
- Request-, Terminalzustands- und Fehlerprüfungen bleiben erhalten.
- Das ursprüngliche native Fehlerseiten-Routingszenario benötigt vor einer
  Verifikation von B09 weiterhin einen gepinnten Live-Host-Regressionstest.
- Der dedizierte Workflow muss seine Tests ausführen; vorhandene Dokumentations-
  und Workflowprüfungen müssen am korrigierten PR-Head erfolgreich sein.

## Implementierungsentscheidung und Begründung

Der gemeinsame Klassifizierer leitet die Engineentscheidung nicht mehr aus
dem allgemeinen Fehlerseitenmarker ab. Ein P1-Ergebnis null bleibt ALLOW,
damit die Request-Body-Prüfung ausgeführt wird. P1- und P3-Aufrufer verwenden
weiterhin diesen Klassifizierer. Der unabhängige P2-Pfad kehrt nicht mehr
allein wegen des Markers früh zurück; Fehler-, Entscheidungsereignis- und
Terminalbehandlung bleiben erhalten.

Der neue C17-Regressionstest kompiliert den tatsächlichen Klassifizierer und
die tatsächlichen P1-/P2-Ergebnisabschnitte mit kontrollierten nativen Rückgaben
und Ereignissenken-Doubles. Er deckt positive 302/403/451-, Null- und negative
Ergebnisse mit gesetztem sowie gelöschtem Marker ab. Dies ist kein laufender
NGINX- oder libmodsecurity-Integrationstest.

Ein unabhängiger Registertest prüft alle 72 Quellaliase und die 59er-Zuordnung.
Ein begrenzter GitHub-Workflow mit Leserechten führt diese Tests am PR-Head aus
und verwendet bereits vorhandene Action-Pins. Das temporäre Verzeichnis wird
vor dem Test mit privater umask angelegt. Bestehende Pflichtprüfungen,
Dependency-Locks, Tokenrechte und Quality Gates bleiben erhalten.

## Geänderte Dateien

- `connectors/nginx/src/ngx_http_modsecurity_common.h`
- `connectors/nginx/src/ngx_http_modsecurity_access.c`
- `tests/test_nginx_error_page_intervention.py`
- `tests/test_security_finding_intake.py`
- `.github/workflows/ci-findings-regressions.yml`
- `reports/audits/findings/20260929-intake.json`
- Dieses englisch/deutsche Change-Record-Paar.

## Ausgeführte Befehle

| Prüfung | Tatsächlicher Nachweis und Einschränkung |
| --- | --- |
| Ursprüngliche GitHub-Basisdateiübernahme | Beide vollständigen C-Dateien stimmten vor der ersten Änderung mit ihrem Git-Blob-SHA-1 überein |
| Ursprünglicher Quellvergleich | Nur die genannten Klassifizierer-/P2-Änderungen; keine fremden Quelländerungen |
| Ursprüngliche Python-Syntax / Register-JSON | Als Daten geparst; keine Ausführung der neuen Tests |
| Lokale kompilierte/Unit-Regression | NOT RUN: verpflichtender RTK-Wrapper nicht verfügbar |
| Lokaler nativer Build / Live-Host | NOT RUN: kein vollständiger Checkout oder Host-Build in der Bearbeitungsumgebung |
| Lokales git diff --check | NOT RUN; diese API-Änderung belegt keinen lokalen Git-Check |
| Ursprünglicher Workflow am exakten Head | Ungültiger runner-Kontext verhinderte den beabsichtigten dedizierten Regressionslauf |
| Korrigierter Workflow am exakten Head und gesamte CI | Neue Ergebnisse nach diesem Commit stehen aus; hier kein PASS behauptet |

Der verfügbare Code-Work-Skill wurde gelesen. Der im Repository referenzierte
globale Ausführungsskill war in der Bearbeitungsumgebung nicht zugänglich.
Kein lokaler Projektbefehl wurde stillschweigend anstelle des verpflichtenden
RTK-Pfads ausgeführt.

## Security-Auswirkung

Eine echte Block-/Redirect-Entscheidung gilt nicht mehr allein deshalb als
abwesend, weil NGINX eine Fehlerseite verarbeitet. Ein P1-Ergebnis ohne
Intervention überspringt bei Fehlerseiten P2 nicht mehr. Wiedereintritt und
tatsächliches Host-/Clientverhalten benötigen weiterhin Live-Host-Nachweise.
Nicht unterstützte Streaming-, Endpunkt-, Socket-, Supply-Chain- oder andere
Connector-Pfade werden hier nicht geändert. Die CI-Korrektur ändert die
Produktentscheidungslogik nicht.

## Runtime-Evidence

Dieser Record belegt keine Live-Host-Reproduktion des ursprünglichen
Szenarios. Der extrahierte C-Test prüft nur seine erklärte Ebene. Ein
 erfolgreicher Build, Fixturetest, anderer Workflow oder Konfigurationsload
belegt keinen rekursionssicheren B09-Laufzeitfix. Neue headgebundene CI-Ergebnisse
müssen vor einer Verifikationsaussage gesondert bewertet werden.

## Bekannte Einschränkungen

B09 bleibt ein Kandidatenpatch, nicht verifiziert oder geschlossen. Alle
übrigen Parent-Arbeitseinträge bleiben in diesem Draft unverändert. Die
Framework-Mitigation am B03-Eingang wird separat geliefert; der ursächliche
Code gehört MRTS und wird nicht geändert.

## Verbleibende Risiken

Die unabhängigen Draft-PRs #382 und #370 enthalten überlappende NGINX-Arbeit;
PR #392 berührt ebenfalls den Klassifizierer. Deren Branches und Nachweise
werden nicht importiert. Eine Integration erfordert einen späteren geprüften
Abgleich. Fehlerseitenrekursion und der vollständige P1-/P2-/P3-Hostpfad
benötigen eigene Abnahmenachweise.

## Nicht ausgeführte Prüfungen mit Begründung

Lokale Repositorytests, vollständige native Builds und Live-Host-Abnahme
wurden mangels vorgeschriebenem RTK-Ausführungspfad und provisionierter
Repository-/Hostumgebung nicht ausgeführt. Keine ausgelassene Prüfung ist
PASS. Ausstehende Prüfungen am korrigierten Head werden nicht durch Erfolge
an älteren Heads ersetzt.

## Finaler Diff- und Review-Status

Die CI-Nachbesserung ändert nur den dedizierten Workflow und dieses Record-Paar.
Regressionsbefehle und alle bisherigen Prüfungen bleiben erhalten. Der PR
bleibt bis zum Abschluss der aktuellen Headprüfungen und Reviews ein Draft.

Parent- und Framework-Commits/PRs bleiben unabhängig. Beide Gitlinks bleiben
unverändert. Diese Änderung führt weder Default-Branch-/Force-Push, Merge,
Risikoakzeptanz, Rohscan-Veröffentlichung noch abgeschwächte Gates aus.
