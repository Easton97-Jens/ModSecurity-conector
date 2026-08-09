# Change Record

**Sprache:** [English](CR-20260808-trusted-nginx-root-broker.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260808-trusted-nginx-root-broker |
| Datum (UTC) | 2026-08-08 |
| Basis-Revision | cd1328e25bb2d9e6769461c61c6e7012a2c49d07 |

## Motivation und Problemstellung

Der bestehende NGINX-Smoke-Harness benötigt einen Root-Master und einen
getrennten Nicht-root-Worker. Eine Elevation von Parent- oder Framework-Code
aus PR #240 würde branch-owned Shellcode, generierte Daten, Binaries, Module
oder Libraries als root ausführen. Der User autorisierte deshalb einen
separaten Protected-master-Broker-PR, bevor PR #240 einen exakten Merge-SHA
verwenden darf.

## Akzeptanzkriterien

Der Broker darf nur Protected-master-Code als root ausführen; er muss nur ein
begrenztes deklaratives Manifest und feste Aktionen akzeptieren; die
NGINX-/Modul-Artefakte aus dem geschützten Source bauen oder attestieren; SHA,
Pfade, Owner, Modes, Master-/Worker-Identität, Loopback-Listener, Evidence und
Cleanup prüfen; und gepaarte EN/DE-Dokumentation sowie Tests tragen. Er darf
keine PR-240-Pinning-, CRS-Trennungs-, Framework- oder MRTS-Änderungen
enthalten.

## Implementierungsentscheidung und Begründung

Ein SHA-gebundener wiederverwendbarer Workflow checkt die exakte geschützte
Broker-Revision aus, prüft Protected-master-Ancestry und einen passenden
Framework-Gitlink, baut Artefakte ohne root und übergibt nur ein
sechsfeldriges Caller-Manifest an den Broker. Der Python-Helfer kopiert/hasht
Artefakte erneut in ein root-owned exaktes Layout und implementiert die
geschlossene Aktionsliste. Root-generierte Konfiguration und Regeln verhindern
Caller-Konfigurationsausführung. Die Root-zu-Runner-Projektion ist allowlisted
und descriptor-relativ. Der Broker zeichnet ein Root-Broker-only-Ergebnis auf,
bewusst kein CRS-Ergebnis. Sein privilegierter Parent ist der feste
root-owned State-Ort `/var/lib/msconnector-nginx-root-broker`; kein Caller-
oder Broker-CLI-Input kann Parent, Staging-Root oder Runtime-Snapshot-Pfad
über die Privileggrenze auswählen.

## Geänderte Dateien

- `.github/workflows/nginx-root-broker.yml`
- `ci/runtime/broker/nginx_root_broker.py`
- `tests/test_nginx_root_broker.py`
- `tests/test_nginx_root_broker_workflow.py`
- `tests/test_ci_security_workflows.py`
- `docs/security/trusted-nginx-root-broker.md` und `.de.md`
- `docs/README.md` und `docs/README.de.md`
- dieser Change Record und seine deutsche Begleitdatei

## Ausgeführte Befehle

Python-Kompilierung, die fokussierte Broker-/Workflow-/CI-Security-Suite
(`39` Tests), `make check-ci-security-contract`, `make check-bilingual-docs`,
`make check-doc-links`, `git diff --check`, actionlint mit ShellCheck und
zizmor offline waren in der ersten Prüfung erfolgreich. `make lint` war
erfolgreich; sein optionaler NGINX-C17-Compile-Check wurde explizit
blockiert/übersprungen, weil dieser lokalen Umgebung NGINX-Header/-Source
fehlen. Der finale Security-Diff-Scan endete ohne reportable Finding und mit
einem gültigen versiegelten Artefakt. Nachdem der Branch normal mit
`origin/master` bei `27e8756e212fd9452d99e285743dbadc43c814a6` gemergt wurde,
wurden die fünf PR-spezifischen SonarQube-Cloud-Wartbarkeitsbefunde lokal
adressiert.
Danach waren die fokussierte Broker-/Workflow-/CI-Security-Suite (`40` Tests)
und `git diff --check` erfolgreich. Hosted-Checks, die SonarQube-Cloud-Analyse
für den aktuellen SHA, Review-/Branch-Protection-Gates und der
Protected-master-Root-Aufruf bleiben ausstehende Delivery-Evidence.

## Security-Auswirkung

Die Änderung schafft eine enge privilegierte Grenze, statt PR-Code zu
elevieren. Der Caller kann weder einen Root-Command noch Shellfragment,
Konfigurationspfad oder Ausführungspfad liefern. Die Root-Ausführung ist auf
den exakten geschützten Helfer, das exakte root-kopierte NGINX-Binary und feste
Aktionen begrenzt. Cleanup ist descriptor-relativ und kann keine
caller-kontrollierten Pfade rekursiv verfolgen. Ein per Fault-Injection
ausgelöstes fehlgeschlagenes `chown` entfernt außerdem einen neu angelegten
festen Root-Parent oder Run-Root, statt privilegierten Stale-State zu behalten.
Die Sonar-Nachbesserung nach dem Review zentralisiert nur feste
Diagnosebezeichner und wertet die Test-Runner-GID vor ihrer Exception-Assertion
aus; sie ändert keine Manifest-, Pfad-, Owner- oder Cleanup-Validierung.

## Runtime-Evidence

Es wurde noch kein Protected-master-Hosted-Root-Aufruf beobachtet. Lokale
statische Tests belegen weder GitHub-Reusable-Workflow-Kontextsemantik noch
einen realen NGINX-Root-Master, Worker-Identität, Listener-Freigabe oder
Artefakt-Upload. Der Protected-master-Aufruf ist eine verpflichtende
Resulting-master-Validierung nach der Broker-Integration: Ein Aufruf aus diesem
PR würde den Vertrag verletzen, dass root nur den Protected-master-Helper
ausführt. Er wird daher nicht als Pre-merge-PR-Evidence behauptet.

## Bekannte Einschränkungen

Der Broker führt einen festen statischen ModSecurity-Allow-/Block-Smoke aus.
Sein `matrix_variant` ist nur eine Attributionsbindung; er behauptet weder
CRS-Materialisierung noch CRS-Verhalten. Die frische CRS-Source-Validierung
bleibt eine separate PR-240-Verantwortung.

## Verbleibende Risiken

Die exakten SHA-/Blob- und Protected-master-Prüfungen benötigen
Hosted-Bestätigung in GitHub Actions. Eine ausstehende umgebungsspezifische
Abhängigkeit, Workflow-Kontext- oder NGINX-Runtime-Fehler blockiert die
Broker-Auslieferung, statt einen Fallback zu PR-Branch-Root-Ausführung zu
autorisieren.

## Nicht ausgeführte Prüfungen mit Begründung

Hosted CI, die SonarQube-Cloud-Analyse für den aktuellen SHA sowie
Review-/Branch-Protection-Gates bleiben vor jedem Merge erforderlich. Der
Protected-master-Root-Aufruf bleibt eine verpflichtende Resulting-master-
Validierung unmittelbar nach der Integration; er ist absichtlich kein
Pre-merge-PR-Lauf, weil dieser nicht geschützten PR-Code als root ausführen
würde. Der lokale Security-Diff-Scan ist abgeschlossen; sein Report ist lokale
Evidence und ersetzt nicht die erforderliche Hosted-Root-Lifecycle-Validierung.

## Finaler Diff- und Review-Status

Status zum Zeitpunkt dieser lokalen Nachbesserungsaufnahme: Der Branch enthält
einen normalen Merge von `origin/master` bei
`27e8756e212fd9452d99e285743dbadc43c814a6` und die Sonar-Nachbesserung. Für
diesen Broker-Record wurden keine Parent-PR-240-Änderung, keine
Framework-Source-Änderung, keine MRTS-Änderung, kein Force-Push, kein
History-Rewrite und kein Master-Merge vorgenommen. Exakte Publikations-, PR-,
Check- und Merge-Fakten dürfen erst nach ihrer Beobachtung dokumentiert werden.
