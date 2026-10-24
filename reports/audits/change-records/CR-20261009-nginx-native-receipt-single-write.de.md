# Change Record: CR-20261009-nginx-native-receipt-single-write

**Sprache:** [English](CR-20261009-nginx-native-receipt-single-write.md) | Deutsch

Jedes native Child-Receipt wird genau einmal veröffentlicht, nachdem alle
Source-gebundenen Felder zusammengestellt wurden.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261009-nginx-native-receipt-single-write |
| Datum (UTC) | 2026-10-09 |
| Basis-Revision | `e5e8569eaf0f0ce1cdc8b56e3181d872d03eb9a8` |

## Motivation und Problemstellung

Der echte NGINX-R8-Lifecycle schloss sechzehn Smoke-Cases, den synchronisierten
First-Byte-Probe, sechs native Cases und den ersten Event-Boundary-Request mit
Root-Master, nobody-Worker, HTTP 200 und verifiziertem Cleanup ab. Danach
stoppte er, weil der Event-Adapter `variant` und `request_headers` durch
Überschreiben eines bereits veröffentlichten `source-result.json` ergänzen
wollte. Die exklusive Freshness-Guardrail wies den zweiten Write korrekt mit
`EEXIST` ab; der MIME-Adapter enthielt dasselbe latente Post-Publication-Muster
für seine Source-Digests und den Fixture-Hash.

## Akzeptanzkriterien

Genau eine exklusive Receipt-Veröffentlichung, Existing-File-Ablehnung sowie
alle Pfad-, Ownership-, Symlink- und Bounded-Capture-Prüfungen erhalten. Die
exakten Event- oder MIME-Adapterfelder vor der Veröffentlichung zusammenbauen,
ihre finalen Bytes versiegeln und die bestehende Framework-Validierung sowie
den Required-Umfang unverändert lassen. Den ursprünglichen Fehler mit RED-Tests
belegen und erfolgreiche Event-/MIME-Zusammenstellung, Metadata-Ablehnung,
unsichere Capture-Ablehnung und Receipt-Reuse-Ablehnung abdecken.

## Implementierungsentscheidung und Begründung

Dem gemeinsamen Parent-Phase-4-Host-Runtime wird genau ein geschlossener
Pre-Publication-Assembly-Punkt hinzugefügt. Event- und MIME-Adapter übergeben
begrenzte Metadata sowie das eine literale MIME-Fixture-Leaf an diese Runtime;
sie lesen und überschreiben das Receipt nicht mehr. Die gemeinsame Runtime
hasht die tatsächlichen begrenzt gelesenen Fixture-Bytes, führt die Felder mit
den Observations zusammen und ruft das unveränderte exklusive `HOST.write_json`
genau einmal auf. Damit bleibt der Producer autoritativ; repariert wird die
Orchestrierung und keine Freshness- oder Canonical-Validierung wird gelockert.

Die Exact-Head-PR-Analyse der veröffentlichten Implementierung meldete danach
`python:S3776`, weil der gemeinsame Writer eine Cognitive Complexity von 19
bei einem Grenzwert von 15 erreichte. Der Follow-up behält dieselben Ausdrücke
und dieselbe Prüfungsreihenfolge bei, verschiebt aber ausschließlich die
geschlossenen Metadata-Prüfungen in einen reinen Helper. Capture-Validierung,
Hashing und der eine exklusive Write bleiben gemeinsam im Writer; Runtime- und
Evidence-Semantik ändern sich nicht.

## Geänderte Dateien

`ci/runtime/lifecycle/run-nginx-phase4-cases.py`,
`ci/runtime/lifecycle/run-nginx-event-boundary-cases.py`,
`ci/runtime/lifecycle/run-nginx-mime-cases.py`,
`tests/test_nginx_phase4_driver.py`,
`tests/test_nginx_event_boundary_driver.py`,
`tests/test_nginx_mime_driver.py` und dieses englisch/deutsche Change-Record-
Paar. Framework und MRTS bleiben unverändert.

## Ausgeführte Befehle

Der aufbewahrte fokussierte RED-Lauf ließ alle zehn neuen Assertions
fehlschlagen, weil der Assembly-Helper noch nicht existierte (insgesamt 8
Tests, Exit 1; Log-SHA-256
`91f03f90041bd3c83580d3391b63d052770626ad4b53807bc713e54058c44bd0`).
Der fokussierte GREEN-Lauf bestand alle 15 Tests (Exit 0; Log-SHA-256
`fa6a6d03abd87d37beaf313bcd1d79bdf8a8b46b47ec1a036a17bb8e0e2e093f`).
Die erweiterte Driver-Gruppe bestand 134 Tests mit einem expliziten Framework-
Root-Skip (Exit 0; Log-SHA-256
`555c2ebab5ce7075aa5271cb41704ff4d6911e602835f8946627ef82e5a16b5a`);
das übersprungene Modul wurde anschließend gegen den exakten aktuellen
Framework-Checkout wiederholt und bestand alle 9 Tests ohne Skip (Exit 0;
Log-SHA-256
`264942505cba8da96814e0afab6d3317390731642300098072815e81224a42bd`).
Python-Syntax und `git diff --check` bestanden. Zu diesem Zeitpunkt standen
breitere Source-Gates und ein frischer Post-Fix-Lifecycle noch aus. Die
unabhängig gewählte fokussierte Matrix bestand anschließend 112 Parent- und 74
Framework-Tests ohne Skips; Dokumentationsregressionen bestanden 48 Tests und
Lifecycle-Shell-Environment-Regressionen 11 Tests, ebenfalls ohne Skips.
`bash -n` bestand für alle angrenzenden Lifecycle-Entrypoints, und ShellCheck
auf dem Warning-Schwellwert des Repositories bestand für Baseline-, First-Byte-
und Connector-Stage-Skripte. Das vollständige Parent-Gate `make lint` bestand
ohne Skip-/Failure-Marker (Exit 0; Log-SHA-256
`3e601d7c75b4ffd43dfd03eed26c627284c0aa1e4195e0c97bfd279a3a049a3b`).
Zwei Läufe mit unverändertem Inhalt werden getrennt aufbewahrt: Der erste
verwendete einen unzulässigen historischen Apache-Output-Default; der zweite
übergab `BUILD_ROOT` als Make-Kommandozeilen-Override und setzte damit die
absichtlich Case-lokalen Roots von sechs Tests außer Kraft. Der korrigierte,
auf die Umgebung begrenzte Aufruf bestand zuerst alle 20 Optional-Prerequisite-
Tests und danach das vollständige Lint-Gate.

Das verpflichtende Exact-Head-Sonar-Gate auf Parent
`ade09e1ebeee6ef049614b87305605969506f939` reproduzierte genau ein offenes
Issue bei `run-nginx-phase4-cases.py:31` (`python:S3776`, Complexity 19). Nach
der minimalen Extraktion bestand der Event-/MIME-/Phase-4-Fokus 16 Tests (Log-
SHA-256 `e7dea7e9967c2984a3ed6264a02f7cd1af9fbe99471145d63a3c8d9485e2d4ac`),
die Parent-Matrix bestand 113 Tests ohne Skips (Log-SHA-256
`aabd427239fe9aa511dbee688517b12fb907dad99d3b6ef9ecaea4f7301fe76a`),
und die Framework-Matrix blieb bei 74/74 (Log-SHA-256
`1f2c1a733077a2a1df739f539de9afa3f3e0fdeb279100dd96a401d3c42a0af2`).
Python-Kompilierung und `git diff --check` bestanden ebenfalls. Die
vollständige Parent-Prüfung `make lint` bestand ohne Skip-/Failure-Marker (Exit
0; Log-SHA-256
`c46a091719cac62046aad9cc09a50eed7c9397048a11d50dcee1dacd37e2d9ff`). Die
authentifizierte lokale Sonar-CLI konnte den exakten Befund über den
kanonischen Wrapper abfragen, aber ihr File-Analyzer konnte einen benötigten
Analyzer nicht in den schreibgeschützten lokalen Tool-Cache installieren;
daher kann nur die neue Exact-Head-Remote-Analyse den Sonar-Befund schließen.

## Security-Auswirkung

Die Änderung erhält exklusive/no-follow Receipt-Erstellung, private Runtime-
Root-Authority, Bounded Capture und Existing-Child-Ablehnung. Adapter-Metadata
verwendet eine geschlossene Feldmenge mit begrenzten Event-Identitäten/Headern
und exakten kleingeschriebenen SHA-256-Werten; das einzige zusätzlich
aufgenommene Leaf ist das literale MIME-Fixture. Ein unabhängiger Security-
Review fand kein handlungsrelevantes Problem. Er hielt fest, dass keine
direkten Hardlink-/Ownership- und Racing-Replacement-Tests für das Capture
hinzukommen; das Fixture wird weiterhin vom vertrauenswürdigen Adapter im
privaten root-owned Runtime-Verzeichnis erzeugt, und Descriptor-basierte
`O_NOFOLLOW`-/Regular-File-Prüfungen bleiben aktiv.

## Runtime-Evidence

R8 bleibt als ursprüngliche Fehler-Evidence erhalten und bleibt Canonical
`FAIL` mit Supervisor-/Native-Exit 2; er wird weder wiederverwendet noch
umetikettiert. Das erste fehlschlagende Event-Child belegt Configtest 0,
Client-Exit 0, HTTP 200, Root-Master, nobody-Worker und verifiziertes Cleanup,
bevor das Receipt-Überschreiben scheiterte. Nach dem Fix lief noch keine native
Runtime.
R9 erzeugte und prewarmte echte revisionsgebundene Build-Artefakte mit Exit 0,
führte aber keine Requests aus. Da der Sonar-Follow-up die Parent-Revision
ändert, bleibt R9 diagnostisch und darf nicht als spätere Exact-Head-Evidence
umetikettiert werden.

## Bekannte Einschränkungen

Pure Driver-Tests belegen weder natives Produktverhalten noch Canonical-
Abschluss. Ein separater Commit, frisch gebaute Exact-Head-Artefakte und ein
neuer isolierter Root/nobody-Lifecycle bleiben erforderlich. Ruff bleibt nicht
verfügbar und wurde nicht ausgeführt.

## Verbleibende Risiken

Der frische Lifecycle kann unabhängige nachgelagerte Evidence-/Validierungs-
Defekte zeigen, nachdem alle vorgesehenen Requests ausgeführt wurden. Solche
Fehler müssen getrennt bleiben und dürfen nicht durch Änderungen an Required-
Selection oder Validatoren verdeckt werden. R8 zeigte acht bestehende
Canonical-Fehler und stoppte mit 52 ausgewählten Records ohne PASS; diese
Zahlen sind Fehler-Evidence und keine Post-Fix-Schlussfolgerung.

## Nicht ausgeführte Prüfungen mit Begründung

Clean-Head-Parent-Lint und der revisionsgebundene R9-Build/Prewarm bestanden
für den primären Fix. Der Maintainability-Follow-up benötigt weiterhin
Clean-Head-Lint und eine neue aktuelle Remote-CI-/Sonar-Analyse. Kein Post-Fix-
Request, vollständiger lokaler 97-Record-Lifecycle oder geschützter Exact-Head-
Lauf ist an diesem Checkpoint abgeschlossen. Ein roher Default-Severity-
ShellCheck über den unveränderten großen NGINX-Smoke-Harness meldet weiterhin
seine bestehenden
Warnings; die Warning-Level-Lifecycle-Prüfungen des Repositories sind grün,
und unabhängige Shell-Bereinigung liegt außerhalb dieses Fixes. Der geschützte
Pfad bleibt durch seine Voraussetzungen einer unabhängig freigegebenen Trusted
Base, eines übereinstimmenden Gitlinks, Runner/Environment und eines
administrativen Host-Gates blockiert.

## Finaler Diff- und Review-Status

Der Implementierungs-/Test-Diff aus sechs Dateien und das gepaarte Change
Record bestanden fokussierte, erweiterte und vollständige Lint-Gates sowie
Syntax-, Dokumentations- und Whitespace-Prüfungen. Unabhängige Security-
und Code-Reviews fanden kein handlungsrelevantes Problem. Der Code-Review hielt
eine exakte Adapter-Profiltrennung als optionale Härtung fest, nicht als
nachgewiesenen Defekt: Alle tatsächlichen Aufrufer sind fest verdrahtet und
unvollständige Records werden weiterhin durch die Framework-Validierung
abgelehnt. Der primäre Fix wurde als
`ade09e1ebeee6ef049614b87305605969506f939` committed und normal gepusht;
Remote-Branch und Draft-PR #396 lasen exakt diesen SHA zurück. Der reine
Maintainability-Follow-up benötigt noch einen separaten Commit, normalen Push,
neuen Remote-Sonar-Readback und frische Build-/Runtime-Evidence. Merge,
Retarget, geschützter Dispatch oder Framework-/MRTS-Änderung erfolgten nicht.
