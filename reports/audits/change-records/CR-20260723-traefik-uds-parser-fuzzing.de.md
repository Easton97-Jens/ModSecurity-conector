# Change Record: Traefik-UDS-Parser-Fuzzing

**Sprache:** [English](CR-20260723-traefik-uds-parser-fuzzing.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260723-traefik-uds-parser-fuzzing |
| Datum (UTC) | 2026-07-23 |
| Basis-Revision | a308d7b414f0859490fe7253e0683a4bde80b563 |
| Grenze | Ausschließlich Parent-Traefik-Native-Middleware-UDS-Parser, zugehöriger CodeQL-Job, fokussierter Workflow-Vertrag, Leserdokumentation sowie dieses Change-Record-Paar/Index. Framework, MRTS und beide Gitlinks bleiben unverändert. |
| Finding-Verknüpfung | Scorecard FuzzingID #11; FND-PARENT-0001. |

## Motivation und Problemstellung

Das frische Scorecard-Inventar meldete keinen vom Repository erkannten
Fuzz-Target für den eigenen Traefik-UDS-Frame- und Result-Parser. Dieser Parser
verarbeitet Bytes aus der privaten Unix-Domain-Socket-Engine-Verbindung der
Middleware und muss abgeschnittene oder fehlerhafte Protokolldaten ohne Panic
zurückweisen. Der ausgewählte Host konfiguriert den Peer als privaten
Same-UID-Service; das ersetzt keine begrenzte Parser-Regressionsevidence.

## Akzeptanzkriterien

- Ein Go-nativer FuzzUDSFrameAndResult-Target übt den begrenzten UDS-Frame-
  Reader und Result-Parser mit deterministischen fehlerhaften und gültigen
  Seeds sowie beliebiger begrenzter Eingabe aus.
- Der Target öffnet keinen Socket, startet keine Engine, ruft weder CGo/Common
  auf, ändert kein Protokoll und behauptet kein Host-Runtime-Verhalten.
- Der bestehende traefik-go-CodeQL-Job führt ihn 15 Sekunden mit einem Worker aus.
- Lokale Formatter-, Go-Test-, Vet-, Build-, Modulintegritäts-, begrenzte Fuzz-
  und fokussierte Workflow-Vertragsprüfungen bestehen mit task-lokalem Go 1.26.5.
- Englisch/deutsche Leserdokumentation und dieses Change-Record-Paar
  beschreiben dieselbe Grenze und Einschränkungen.
- Es werden weder gehostete Alert-Closure, Merge, direkter master-Push,
  Framework-Änderung noch MRTS-Änderung behauptet.

## Implementierungsentscheidung und Begründung

Der Fuzz-Target ruft readUDSFrame über einen In-Memory-bytes.Reader auf und
begrenzt die bereitgestellte Eingabe auf einen maximalen Protokollframe plus
Header. Erfolgreiche Reads werden mit writeUDSFrame zurückgeschrieben und mit
den exakt konsumierten Bytes verglichen; ein nachfolgender Frame im selben
Stream bleibt absichtlich zulässig. Result-Payloads werden nur für den
Result-Opcode geparst; akzeptierte Aktionen müssen im erkannten Bereich des
Parsers bleiben.

Der deterministische Korpus enthält leere und abgeschnittene Daten, einen
normalen Begin-Frame, zwei verkettete Frames sowie Allow-, Deny- und Redirect-
Result-Payloads. Das deckt Framing- und Aktionszweige ab, ohne einen Socket zu
erzeugen, den privaten Engine-Service zu starten oder vom host-spezifischen
Traefik-Laden abzuhängen. Der fokussierte CI-Sicherheitsvertrag prüft
Target-Namen und Zeit-/Worker-Grenzen, damit die Workflow-Integration nicht
stillschweigend verschwindet.

## Geänderte Dateien

- connectors/traefik/native_middleware/engine_uds_fuzz_test.go
- .github/workflows/ci-security-codeql.yml
- tests/test_ci_security_workflows.py
- connectors/traefik/native_middleware/README.md und README.de.md
- reports/audits/change-records/README.md und README.de.md
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| Task-lokale offizielle Go-1.26.5-Provenance-/Hash-Verifikation | bestanden; die SHA-256 des vorgehaltenen Archivs stimmte mit 5c2c3b16caefa1d968a94c1daca04a7ca301a496d9b086e17ad77bb81393f053 überein. |
| gofmt -d für den neuen Fuzz-Target | bestanden; keine Formatter-Ausgabe. |
| Modul-Go-Test und Vet | bestanden. |
| Begrenzter Go-Fuzz-Target, 15 Sekunden, ein Worker | bestanden; 105.190 Ausführungen und kein Crash. |
| go mod verify und go mod tidy -diff | bestanden. |
| Go-Build mit deaktiviertem buildvcs im isolierten Worktree | bestanden. |
| make -C connectors/traefik test-native-middleware mit task-lokalem Go und registriertem Output | bestanden. |
| Fokussierter CI-Sicherheitsvertrag | bestanden; 16 Tests plus actionlint-, zizmor- und gitleaks-Validate-only-Prüfungen. |
| Repository-Bilingual-Dokumentationsprüfung | nur durch 20 bereits bestehende fehlende Framework-Gitlink-Linkziele in diesem isolierten Worktree blocked_environment; keine Meldung für die geänderten englischen/deutschen Paare. |
| Unabhängiger fokussierter Security-Diff-Review | bestanden; kein neuer berichtspflichtiger Security-Befund. Er bestätigte unabhängig Parser-Allokationsgrenze, Aktionsvalidierung, Stream-Invariante und Untrusted-PR-Workflow-Kontrollen. |

## Security-Auswirkung

Dies ergänzt Regressionsevidence an der UDS-Protokollparsergrenze und macht sie
im Sicherheitsworkflow des Repositorys sichtbar. Es kontrolliert Parser-Panics
und die Akzeptanz ungültiger Aktionen; es beweist nicht die Abwesenheit aller
Parserfehler, Socket-Level-Angriffe, Engine-Defekte, Host-Verhalten oder einen
gehosteten FuzzingID-Refresh.

Der Target ist absichtlich ressourcenbegrenzt. Er weist Eingaben größer als
einen Protokoll-Maximalframe vor der Allokation zurück, erhält Stream-Semantik
durch Prüfung nur des konsumierten Frames und behandelt Parserfehler als
erwartete Fuzz-Ergebnisse.

## Runtime-Evidence

Der lokale Fuzz-Target ist ausschließlich In-Memory-Source-Level-Evidence. Er
öffnet keinen Unix-Socket, startet weder Traefik noch die persistente
Common/libmodsecurity-Engine, lädt kein Plugin in einen Host und ruft kein CGo
auf. Der Native-Middleware-Source-Testtarget bestand, doch keine
Full-Lifecycle-Host-Capability wird gefördert.

## Bekannte Einschränkungen

Die eingecheckte Kontrolle läuft absichtlich 15 Sekunden mit einem Worker, um
CodeQL-Zeit- und Ressourcenverbrauch zu begrenzen. Sie hat keine langlaufende
Korpus-, Sanitizer-, Socket-Peer-Fault-Injection- oder Common/libmodsecurity-
Integrationsabdeckung. Temporäre Go-Fuzz-Entdeckungen bleiben im task-lokalen
Cache; nur geprüfte deterministische Seeds sind versioniert.

## Verbleibende Risiken

Scorecard muss die resultierende Default-Branch-Revision erneut scannen, bevor
es den Target erkennen und FuzzingID aktualisieren kann. Die getrennten
Scorecard-Governance-Ursachen (BranchProtectionID, CodeReviewID, MaintainedID
und CIIBestPracticesID) bleiben außerhalb dieser Parent-Source-Änderung. Es wird
weder eine externe Governance-Einstellung, Reviewer-Evidence, OpenSSF-
Registrierung noch Alert-Dismissal versucht.

## Nicht ausgeführte Prüfungen mit Begründung

- Exakte PR-Head-CodeQL-, Scorecard-Refresh-, Dependabot-Refresh-, OSV-,
  Gitleaks-Range-, SonarQube-Cloud- und GitHub-Review-Evidence benötigen einen
  gepushten Draft PR oder Default-Branch-Scan.
- Voller Traefik/Common/libmodsecurity-Runtime-Smoke benötigt explizite native
  Host- und Engine-Voraussetzungen; er ist für diese fokussierte Parsergrenze
  nicht erforderlich.
- Längere Fuzz-Kampagnen, Sanitizer und Socket-Peer-Fault-Injection sind
  zukünftige Hardening-Optionen, keine Evidence für diese begrenzte Kontrolle.

## Finaler Diff- und Review-Status

Dieser Record ist vor Staging, Commit, Push, Pull-Request-Erstellung und
externer Check-/Review-Evidence geschrieben. Lokale Validierung und
unabhängiger fokussierter Security-Review sind abgeschlossen und fanden keinen
neuen berichtspflichtigen Befund. Finale Delivery-Evidence steht noch aus; es
wird keine Alert-Closure behauptet.
