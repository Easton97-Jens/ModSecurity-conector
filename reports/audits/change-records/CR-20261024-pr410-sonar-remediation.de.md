# Change Record: CR-20261024-pr410-sonar-remediation

**Sprache:** [English](CR-20261024-pr410-sonar-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261024-pr410-sonar-remediation |
| Datum (UTC) | 2026-10-24 |
| Basis-Revision | `e509db65601057154c184757e2632e65b9dad403` |
| Start der letzten Reparatur | `a1edb5c9b3722eec8c6911345d3315dd82eb145a` |

## Motivation und Problemstellung

PR #410 enthielt noch eine Sonar-Schwachstelle, zwölf Smells, lokale
Lifecycle-Fehler und Apache-CI-Fixturefehler. Die angesammelte Dokumentations-
und Reporthistorie verdeckte zusätzlich die aktuelle Prüffläche. Nach der
vorherigen Reparatur verblieben für diese letzte gezielte Runde ein MINOR-Smell,
ein lokaler Apache-Guard-ERROR und ein davon abhängiger NOT_REACHED-Fall.

## Akzeptanzkriterien

Die benannten Ursachen ohne schwächere Kontrollen reparieren; eine vorab
deklarierte Auswahl von höchstens 100 aktiven Szenarien ohne Retry ausführen;
den tatsächlichen PR-Diff reduzieren; Framework/MRTS erhalten; nur
wahrheitsgetreue Exact-Head-Nachweise veröffentlichen.

## Implementierungsentscheidung und Begründung

Private HAProxy-Captureausgabe nutzt jetzt eine feste externe Grenze,
vertrauenswürdige Vorfahren, ein exklusives 0700-Blatt und deskriptorgebundene
0600-Receipts. Fokussierte Refactorings beseitigen die zwölf Smell-Ursachen.
Testwurzeln und SDK-Includeauswahl sind an ihren Ownern korrigiert. Historische
Prosa/Ergebnisse werden extern archiviert statt im PR erhalten. Die frühere
Reparatur nutzte eine verhaltensgleiche Dictionary-Comprehension, die eine andere
Sonar-Regel auslöste. Der
Apache-Guard kopiert den exakten Registry-hashgebundenen Framework-Fall in seine
private Testwurzel; produktive Pfadfreigaben bleiben unverändert, und negative
Assertions benennen nun ihre vorgesehenen Ablehnungszweige.

## Geänderte Dateien

Die fokussierten Änderungen betreffen HAProxy-Capturehelper,
Envoy-/Apache-/Traefik-Harnesskontrollen, native Observer-Tests, den Apache-
C-Probe, kompakte EN/DE-Dokumentation und einen Change Record. Die letzte
Reparatur ändert zusätzlich nur
`connectors/apache/harness/apache_oracle_overrides.py`,
`tests/test_apache_header_semantics.py`, dieses kompakte EN/DE-Abschlusspaar und
dieses Change-Record-Paar. Zehn maschinenverbrauchte Reporteingaben bleiben aus
dem integrierten PR erhalten.

## Ausgeführte Befehle

RTK umhüllte Git-Inspektion, Python-Kompilierung, Go-Format-/Listingprüfung,
C17-Syntaxprüfung, JSON-/Shell-Preflight, den einzigen koordinierten
Abschlussrunner und Dokumentations-/Diffprüfungen. Es gab keinen ungeschützten
Fallback. Die letzte Reparatur nutzte RTK-umhüllte Sonar-Auslesung,
Python-Kompilierung, JSON-/Shell-/Hash-/Zähl-Preflight und genau einen
Vier-Methoden-unittest-Aufruf über
`rtk bash /var/tmp/codex/ModSecurity-conector/pr410-last-repair-20261024/run-closeout.sh`.

## Security-Auswirkung

Der plausible öffentliche Temp-Ausgabepfad ist ohne Ausnahme oder
Unterdrückung geschlossen. Fokussierte statische Prüfung fand keine relevante
Regression. Es gab keinen Deep Scan, keine Policyabschwächung, keine Änderung
der Secretbehandlung und keine neue Vertrauenswurzel. Die letzte Test-Fixture
bleibt unter einer privaten testeigenen Wurzel und prüft die echten
Framework-Bytes vor Nutzung gegen die bestehende Registry-SHA.

## Runtime-Evidence

Der frühere erhaltene Lauf bleibt bei 73/75 PASS mit einem ERROR und einem
NOT_REACHED. Der separat autorisierte letzte Reparaturlauf
`pr410-last-repair-20261024-final-001` band Start-Head
`a1edb5c9b3722eec8c6911345d3315dd82eb145a` an den ausführbaren Patch mit SHA-256
`2e3681297d924921b82449b82da7675ce4dee0f35d3f968989af0401ec683057`.
Alle vier Methoden / 13 expandierten aktiven Szenarien bestanden, ohne Retry.
Ergebnis-SHA-256:
`f6d02a742713a9d1ec8cab5e399cdb52b32e198b798eaae00795940c20ec0fbf`.

## Bekannte Einschränkungen

Das letzte gezielte lokale Gesamtergebnis ist `PASS`. Dies ist keine vollständige
I12-/V08–V10-Hostabnahme und belegt keine repositoryweite Durchsetzung des
Default-Suite-Limits. `verified_pr` hängt weiterhin von automatischer
Exact-Head-CI/Sonar- und Review-Auslesung ab.

## Verbleibende Risiken

Automatische Final-Head-CI/Sonar kann umgebungsspezifische oder Scannerergebnisse
offenlegen. Vollständige Host-/Protokoll- und blockierte Deploymentnachweise
bleiben außerhalb dieses reduzierten Abschlusses.

## Nicht ausgeführte Prüfungen mit Begründung

Beim früheren Reparaturlauf liefen keine Wiederholung, historische Matrix,
Oracle-Kampagne, kein tiefer Security-Scan, Release, Deployment oder Merge.
Die Retryzahl ist null; Providerchecks starten erst vom gepushten Final-Head.

## Finaler Diff- und Review-Status

Unabhängige statische Reviews fanden nach den Dokumentationskorrekturen keine
Quellregression. Gegenüber der tatsächlichen PR-Basis ist der
Docs-/Report-Anteil von 193 auf 25 geänderte Dateien reduziert. Der letzte
gezielte lokale Lauf besteht; der PR bleibt Draft, solange die automatische
Exact-Head-Prüfung aussteht.

## Autorisierte Integrations-Nachkorrektur

Ausgehend von `11324289a724b61ab2279f56c16e9185e240ccc9` ersetzt eine explizite
Parsingschleife das redundante Generator-/Identitäts-Comprehension-Paar in
`connectors/apache/harness/apache_oracle_overrides.py`. Die vollständigen
Meldungen von `S7494` und `S7500` wurden gelesen; Trennung am ersten `=`,
Priorität doppelter Schlüssel und Ablehnung fehlerhafter Zeilen bleiben erhalten.
Keine Unterdrückung, Regelausnahme oder Änderung der Pfadfreigabe.
Dieselben vier Guard-Methoden / 13 expandierten Szenarien bestanden einmal in
0.759 Sekunden über den RTK-umhüllten Parent-Interpreter (3.14.4). Der
Auswahl-Preflight bestätigt die 13 Szenarien als Teilmenge des bestehenden
75-Fall-Inventars. Aufgabeneigener Befehl, Auswahl, Patch-Digest und Ergebnis
bleiben unter `/var/tmp/codex/ModSecurity-conector/runs/pr382-integrate410-20261024`
erhalten. Hosted-Python3.14.7-Checks und Exact-Head-Sonar bleiben getrennte
Nachweise. Historische Ergebnisse behalten ihre ursprünglichen Revisionsbindungen.

Die veröffentlichte Apache-Korrektur `525d3e5e8a0788c46455b0cab4cd775f2190a325`
zeigte einen Fehler von `TestMiddlewareCancellationAfterClaimSendsBoundedCancel`
unter Hosted-Go1.27.2 (Job `120833096999`). Ein CLAIM-Cancellation-Watcher konnte
`session.exchange` überleben und die nachfolgende CANCEL-Deadline beschädigen.
Die Korrektur in `observer.go` wartet vor dem Unlock auf das Watcher-Ende.
Der neue deterministische `TestSessionExchangeJoinsCanceledDeadlineWriter`
scheitert am ursprünglichen Source an der vorgesehenen Assertion und besteht
mit dem Fix; der bestehende CANCEL-Fall besteht ebenfalls (zwei ausgewählte
Unit-Szenarien, keine Retries, lokales Go1.27.3). Befehle, Baseline-/Fixlogs und
Quelldigests bleiben unter derselben Run-Wurzel erhalten. `observer_test.go`
ergänzt diese Regression ohne Assertions zu entfernen. Die automatische
Exact-Head-Verifikation dieser zweiten Quellkorrektur endete für Quellhead
`3d5095e3561df29a217537ab500ce8595e1a5067` mit 26 erfolgreichen Checks und zwei
bedingten Skips. Sonar-Analyse `32cca90c-523f-4810-9941-5cfe37314c15` ist terminal
SUCCESS, Gate OK mit null offenen/akzeptierten Issues, Hotspots und neuer Duplikation.

## Gemeinsame PR-#382-Reparatur und Abnahme

Die Integration nutzt normale Merge-Commits `86101a0c` und `bba093f5`;
ursprünglicher Quellhead `11324289` und aktualisierter Quellhead `3d5095e3` sind
Vorfahren. Master-Regelrevision `42fd5a8e` bleibt enthalten. Framework-`99a7985c`-
und MRTS-`8a6bb546`-Repositories sowie Gitlinks bleiben unverändert. Die Reduktion
des Quell-PRs auf 25 Docs-/Report-Dateien und maschinenverbrauchte Eingaben bleiben erhalten.

Die #382-Baseline enthält 95 offene Befunde (zwei Reliability-Bugs und 93 Smells),
keine akzeptierten Issues/Hotspots und Duplikation in vier Dateien. Änderungen
betreffen Common-/NGINX-/HAProxy-/Traefik-Source, C-Fixtures, aktuelle
Source-Extraktionsabhängigkeiten und gemeinsame Lifecycle-Stubs. Sie erhalten
öffentliche APIs, alle bestehenden Szenariovarianten, Cleanup-Besitz,
Priorität des ersten Fehlers und Assertions. Der echte Traefik-Lockdauerfehler
hat eine deterministisch fehlschlagende Altquellkontrolle; Descriptor-Snapshots
und allokationsfreies Expiry-Cleanup bestehen ihre gezielten Kontrollen. Eine
unabhängige Prüfung fand und beseitigte ein zwischenzeitliches FD-Erschöpfungs-
Cleanup-Risiko vor Veröffentlichung.

Die koordinierte Auswahl enthält 100 expandierte Unit-/Native-/Vertragsszenarien:
Apache13, Traefik nativ20, HAProxy22, Common9, NGINX10, Trusted-HTTP12,
native Telemetrie7, Cancellation2, Go-Provenance4 und Scannerkontrolle1.
Lokal: 98 PASS, kein FAIL/ERROR, zwei Fremd-UID/GID-Kontrollen durch die `0 0 1`-
User-/Gruppen-Mappings des Hosts blockiert. Ihre exakten nativen Hosted-CI-Tests
lehnen Skips ab; der Testchild nutzt den ausgewählten Interpreter. Kein
Connector-E2E-Fall und keine historische I12-Ausführung wurden ergänzt.
Nicht ausgewählte historische Fälle behalten ihre alten Ergebnisse/Revisionen;
globale E2E-Limitdurchsetzung bleibt unbelegt.

Gitleaks fand zunächst 1.017 unveränderliche Prosa-/Hash-Fehlalarme in der
gemeinsamen Historie. Die Einzelklassifikation enthält Quellzeilen-/Blob-Digests,
typisierte Verbraucher und 903 nachgerechnete Originalquelldigests. Die bereinigte
Triage hat keine ungeklärten Einträge. `.gitleaksignore` enthält nur exakte
unveränderliche Fingerprints; Standardregeln, Redaction und voller PR-Bereich
bleiben aktiv. Der Integrationsscan mit 253 Commits besteht; ein synthetischer
Kontrollfall in einem neuen Commit wird weiterhin erkannt. Dies ist eine
belegte Fehlalarm-Disposition und keine Risikoakzeptanz.

RTK-umhüllte Prüfungen umfassen eingefrorene Auswahl/Preflight und gezielten
Dispatcher, negative Altquellkontrollen, native C17-/Wextra-/Werror-Kompilierung,
nativen NGINX-Build, Go-Build/Testkompilierung/gofmt, Gitleaks-Vollbereich und
Negativkontrolle, Workflow-Lint sowie EN/DE-/Link-/Diff-Validierung. Lokales
Python3.14.4/Go1.27.3 und Hosted-Python3.14.7/Go1.27.2 bleiben getrennt.
Run-Evidence, exakte Befehle, Digests, Skips und Veröffentlichungs-/Auslesefakten
bleiben unter `/var/tmp/codex/ModSecurity-conector/runs/pr382-integrate410-20261024`
erhalten. Aktuelle gemeinsame CI, Sonar-Verarbeitung/Gates und Reviews werden
am veröffentlichten #382-Head bewertet; das grüne #410-Ergebnis überträgt sich
nicht automatisch. Coverage-Import und Runtime-/Lifecycle-Abnahme bleiben von
diesen Tests getrennt. Kein Master-Merge, Release, Deployment oder historische
Qualifikation ist freigegeben.

## Gemeinsame Sonar- und Wartungs-Nachkorrektur

GitHub führt #410 als geschlossen/gemergt bei `bba093f5`. Gemeinsamer Head
`23c583d8` hat 41 erfolgreiche Checks, fünf bedingte Skips und zwei Fehler mit
demselben Sonar-Inventar von 99 Befunden. Go-Testdateien waren fälschlich
MAIN/FIL: `*_test.go` bleibt nun als TEST analysiert, Produktivquellen bleiben
unverändert. Unabhängige Prüfung validiert die Rechteablehnungs- und
HTTP-Speicher-Fixtures als nicht verwundbare Testkontrollen; keine
False-Positive-Markierung beim Provider. C-Includes auf oberster Ebene mit
makrogerechten Prototypen, zwei Const-Deklarationen, Go-Parametergruppierung und
eine korrekte Fixture mit veränderlicher Fehlerausgabe bearbeiten die kleinen
übrigen Ursachen. Die zwölf Trusted-HTTP- und drei MSE1-Unit-Varianten bestehen
mit isoliertem Python 3.15.1 aus offiziell checksumgeprüftem Quellcode.

Der Benutzer erweiterte den Auftrag um Go 1.27.3, Python 3.15.1, alle aktuellen
Actions und fehlerhafte Update-Workflows. Alle zehn externen Actions wurden
gegen offizielle Releases und unveränderliche Tag-Commits geprüft;
setup-python, create-github-app-token und CodeQL steigen auf, ohne Änderungen
an Node-Runtime oder genutzten Input-Verträgen. Build-Toolchain-Selektoren nutzen
`.go-version`; Modul-Sprachminima bleiben unverändert. Die gescheiterte alte
Master-Socket-Fixture des Go-Updaters ist bereits durch `91722137` korrigiert;
zwei gezielte Kontrollen bestehen mit Go 1.27.3. Pythons statisches Inventar,
Setup-Verifikation und Erkennung fester Self-Repository-Reusable-Aufrufe sind repariert. Der
geschützte lighttpd-Namespace behält seinen root-eigenen Systeminterpreter unter
dem vollständigen eigenen Trust-Vertrag. Normale Jobs nutzen kanonisches Python.
Action-Verträge lesen den zentralen Lock statt gültige künftige Kandidaten
durch alte Pins abzulehnen. Vierzehn gezielte Updater-Kontrollen bestehen;
die erneute Metadaten-Publisher-Schritt-Trennungsprüfung besteht ebenfalls nach
Korrektur des zweiten Rate-Limit-Pfads.

GitHub-Metadatenautorisierung bleibt auf die zwei Resolver-Schritte mit festem
Origin begrenzt; Redirects werden vor Credential-Weitergabe abgelehnt, Fehlertexte
bereinigt und Artefakt-/Git-/PR-Operationen behalten ihre eigenen Credentials.
Der Benutzer autorisierte ausdrücklich den eng hashgebundenen offiziellen
PyYAML-6.0.3-Quellbuild für Python 3.15. Parent besitzt dieses Runtime-Artefakt;
die zwei Parent-Verbraucher prüfen dieselbe Dependency-Version des gepinnten
Frameworks ohne Framework-Quellen, Locks oder Gitlinks zu ändern. Dies ist keine
Framework-Zertifizierung. Die anfänglichen lokalen 100-Fall-Ergebnisse bleiben
revisionsgebunden; nachfolgende Unit-Kontrollen sind separat erfasst. Bestehende
Scaffold-CI führte 583 Methoden in 14 Batches aus (eine SDK-Klasse übersprungen),
mehr als die anfängliche Untergrenze von 494 Methoden. Neue Connector-E2E-Fälle
bleiben null. Live-Veröffentlichung durch Default-Branch-Updater wird in diesem
PR-Auftrag nicht ausgeführt; sie benötigt spätere vertrauenswürdige
Master-Integration/Ausführung. Finale Exact-Head-CI-/Sonar-/Review-Fakten bleiben
in externer Task-Evidence und den aktuellen PR-Checks; das frühere grüne
#410-Ergebnis wird nicht übertragen.

In der isolierten Python-3.15.1-Umgebung besteht die finale Sprachauswahl
55 expandierte Unit-Varianten; der Installer besteht 20 eindeutige Unit-Kontrollen.
Der erste echte Quellbuild/Installationslauf, sicheres Mapping-Laden und
Ablehnung unbekannter Tags bestehen ebenso wie `pip check`. Das erzeugte reine
Python-Wheel hat SHA-256
`779a6918447c67ec85d3862ccf51dc57b3ba665c0a50f2955bab850b75c0fc43`;
offizieller Quelldigest und alle drei Build-Werkzeug-Digests bleiben im Receipt
erhalten. Der Candidate-Installationsvertrag des Python-Updaters besteht ebenfalls.
Dies sind getrennte Nachprüfungen; ursprüngliche Versuche und Quellbindungen
bleiben erhalten.
Die echte Wartungsbaseline im kopierten Baum besteht ebenfalls mit Python 3.15.1:
311 Unit-Methoden, 305 bestanden und sechs Umgebungs-/Snapshot-Skips, keine Fehler.
Die übersprungenen Kontrollen bleiben explizit; kein Connector-E2E- oder
Hostnachweis wird daraus abgeleitet.

## Final-Head-Kompatibilität und Workspace-Reparatur

Der veröffentlichte gemeinsame Head `c7225e27` hat 37 erfolgreiche Checks, fünf
bedingte Skips und sechs Fehler: Vier konsumieren denselben Apache-AST-Snapshot-
Fehler; Sonar und sein Scaffold-Verbraucher melden sechs neue Python-Befunde.
Die Go-Test-Scope-Korrektur hat das vorherige Inventar aus der fehlerhaften
Produktivklassifikation beseitigt. Python 3.15 ergänzt Eager-Import-Metadaten
`is_lazy=0` und ändert die Standarddarstellung von `Load`-Kontexten in `ast.dump()`.
Ein expliziter Testserializer erhält den ursprünglichen Golden-Digest und alle
3.205 semantischen Knoten, Meldungen und ihre Reihenfolge. Ursprüngliche Assertion
und fünf Mutationskontrollen bestehen mit Python 3.15.1. Literalextraktion,
redundante Exception-Unterklasse und Setup der Exception-Tests sind ohne
Verhaltensänderung korrigiert; vier gezielte Fehlerkontrollen bestehen.

Der bedingte Workspace-Zulassungsfehler S5443 ist vor Downloads korrigiert:
Fremde Eigentümer, schreibbare oder Symlink-Ahnen werden abgelehnt,
root-eigene Sticky-Vorfahren bleiben erlaubt, eine explizit gewählte geschützte
Wurzel ist erforderlich und ihr zugelassener kanonischer Pfad wird verwendet.
Die veröffentlichte Baseline akzeptierte einen kontrollierten unsicheren Parent;
der korrigierte Helper lehnt ihn vor Downloads/Backend-Ausführung ab und
akzeptiert die echte zuvor verwendete Build-Wurzel. Alle 27 Installer-Unit-
Kontrollen bestehen. Frische unabhängige Baseline-Untersuchung und Post-Patch-
Review fanden keinen verbleibenden Bypass dieser Grenze. Tatsächliche Ausnutzung
auf Hosted RUNNER_TEMP wurde nicht belegt. Bereits geprüfte Source-/Backend-Locks
und Build-Logik bleiben unverändert; kein Backend-Neubuild oder Nachweis einer
Netzwerkisolation durch das Betriebssystem wird ergänzt.

## Automatische Go-Abhängigkeitspflege

Der Folgeauftrag ergänzt wöchentliche Dependabot-Go-Versionsvorschläge für alle
vier Parent-Go-Module, unter Erhalt der Python-Updates und eigenen Action-Pflege.
Konfiguriert sind sieben Tage Versions-Cooldown und
`open-pull-requests-limit: 5`; eine globale PR-Anzahl-Durchsetzung wird nicht behauptet.
Acht Konfigurationskontrollen bestehen im echten Checkout und seinem kopierten
107-Input-Snapshot. Sechzehn Komponenten-Mindeststands-Szenarien bestehen,
einschließlich neuerer/gemischter Bundles, Byte-Erhalt, Downgrade-Ablehnung und
bestehender Sicherheitskontrollen. `approved_minimums` und Komponenten-Konstanten
benennen geprüfte Mindeststände ausdrücklich; tatsächliche neuere
Abhängigkeitsvorschläge kommen von Dependabot. Keine Änderung an Modulmanifesten/
Checksummen, Framework-/MRTS-Repositories oder Connector-E2E. Live-Vorschläge
benötigen die Konfiguration auf dem Default-Branch und bleiben von der
Quell-/CI-Verifikation dieses PRs getrennt.
