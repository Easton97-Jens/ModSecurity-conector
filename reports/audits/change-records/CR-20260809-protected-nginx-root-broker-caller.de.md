# Change Record

**Sprache:** [English](CR-20260809-protected-nginx-root-broker-caller.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260809-protected-nginx-root-broker-caller |
| Datum (UTC) | 2026-08-09 |
| Basis-Revision | 83094eb659f0b5df8c2df30b1ae718d524a9adf0 |

## Motivation und Problemstellung

Der vertrauenswürdige NGINX-Root-Broker v2 wurde als wiederverwendbarer
`workflow_call`-Code gemergt, doch geschütztes Parent-`master` besaß keinen
nur per Dispatch ausführbaren Caller. Daher konnte kein resulting-master-Lauf
beide festen Brokerprofile `no-crs` und `owasp-crs`, ihre hochgeladene
Evidence und den descriptor-relativen Cleanup beweisen, bevor PR #240 auf
dieser Grenze aufbaut.

## Akzeptanzkriterien

Der neue Caller ist nur über `workflow_dispatch` auf dem kanonischen
Nicht-Fork-geschützten `master` verfügbar und akzeptiert ausschließlich das
erforderliche `parent_head_sha`. Dieser Wert ist ausschließlich lowercase-
SHA-40-Commit-Evidence: Er wird über einen festen read-only-GitHub-API-Endpunkt
geprüft und niemals ausgecheckt, importiert, gesourct, gebaut, gestartet,
geladen oder als root ausgeführt. Der Caller erzeugt exakt zwei private
Schema-v2-Manifeste und ruft exakt zweimal den unveränderlichen Broker-SHA
`e06254ea9622d214a9030b9ba786756560ace417` auf, gebunden an Framework-SHA
`c71e15db7b7517b237add9fa09b3493e7bc93627`.

Die zwei geschlossenen Profile sind `no-crs`/`no-crs` und
`with-crs`/`owasp-crs`. Ein unprivilegierter Readback prüft exakte
Evidence-Dateien, Schemata, Identitäten, Root-Master-/Nicht-root-Worker-
Records, Cleanup PASS und die CRS-Audit-/Bundle-Bindung. Ein finaler
Always-Run-Ergebnisjob muss fail-closed fehlschlagen, wenn Vorbereitung, einer
der Broker oder Readback fehlschlägt.

## Implementierungsentscheidung und Begründung

Die Implementierung ergänzt einen Parent-eigenen Workflow, statt die
wiederverwendbare Broker-Schnittstelle zu verbreitern oder einen zweiten Root-
Runner hinzuzufügen. Ein kleiner repositoryeigener Python-Helper besitzt nur
Unterbefehle zur Manifest-Erzeugung und Evidence-Prüfung. Er serialisiert
deterministisches JSON mit privaten Pfaden und Modi, weist unbekannte/doppelte
Felder und Symlinks ab und behandelt Artefaktinhalte ausschließlich als
begrenzte Daten. Der Caller verwendet nur Full-SHA-Action-Pins und den
bestehenden Full-SHA-Reusable-Broker-Ref; er besitzt keine Secrets,
Write-Berechtigungen, kein `sudo`, keinen lokalen Reusable-Ref, keine Profil-,
Pfad- oder Command-Inputs und keinen Target-Commit-Checkout.

Der Helper akzeptiert keinen vom Caller gewählten Manifest- oder Evidence-
Dateisystempfad. Er leitet seine zwei festen Roots ausschließlich aus einem
absoluten, nicht-symlinkenden, vom Runner bereitgestellten `RUNNER_TEMP`-
Verzeichnis und den validierten gepaarten festen Run-IDs ab. Ungültige oder
nicht passende Pfadidentität schlägt daher vor API-Zugriff, Artefakterzeugung
oder Evidence-Readback fehl; jeder abgeleitete Root muss zusätzlich ein
nicht-symlinkendes Verzeichnis sein.

Das Workflow-Python-Inventar des Repositorys erhält nur für die zwei bekannten
unveränderlichen Reusable-Aufrufe eine eng enumerierte Ausnahme. Damit bleibt
die fail-closed-Regel für jeden anderen Reusable-Workflow-Aufruf erhalten,
statt einen Remote-Root-Broker-Aufruf fälschlich als Third-Party-Action-
Lockeintrag einzuordnen.

## Geänderte Dateien

- `.github/workflows/run-protected-nginx-root-broker.yml`
- `ci/runtime/broker/protected_nginx_broker_caller.py`
- `ci/checks/common/check-python-version-contract.py`
- `tests/test_protected_nginx_broker_caller.py`
- `tests/test_ci_security_workflows.py`
- `tests/test_python_version_contract.py`
- `docs/security/trusted-nginx-root-broker.md` und `.de.md`
- dieser Change Record und sein deutsches Gegenstück

## Ausgeführte Befehle

Die Exact-Head-Lokalvalidierung bestand mit dem verfügbaren lokalen Python
3.14.4 als nicht kanonischem statischem Fallback: Die fokussierten Caller-,
Broker-, CI-Security- und Python-Version-Suites (82 Tests),
`make check-ci-security-contract`, Quell-`py_compile`, `make lint`, bilinguale
Dokumentations- und Link-Prüfungen, actionlint mit ShellCheck, zizmor offline
und `git diff --check` bestanden. Der fokussierte Security-Diff-Scan wurde mit
vollständigen 10/10 File-Worklist-Receipts und ohne reportable Finding
versiegelt. Das Projekt fordert Python 3.14.6; dies beansprucht daher nicht das
erforderliche exakte lokale Interpreter-Gate.
`make check-python-version-contract` hat denselben vorbestehenden
Inventory-Fehler auf unverändertem `master` und wird nicht als Caller-Regression
behandelt.

Auf Draft-PR #259 meldete SonarQube Cloud zunächst sieben aufgabeneigene offene
Befunde und ließ die New-Code-Sicherheitsrating-Bedingung fehlschlagen. Die
Folgekorrektur entfernt beliebige Helper-Dateisystempfadargumente, leitet nur
feste Runner-Temp-Roots ab und prüft sie, extrahiert die gemeldeten
Validierungszweige und ergänzt Pre-I/O-Pfadregressionstests. Fokussierte
Caller-/CI-Security-Tests, Python-Kompilierung, CI-Security-Contract-Checks,
vollständiges `make lint`, bilinguale und Link-Prüfungen, actionlint mit
ShellCheck, zizmor offline und Diff-Prüfungen bestanden lokal mit dem
verfügbaren Python-3.14.4-Fallback. Frische Exact-Head-Hosted- und
SonarQube-Cloud-Analyse bleiben erforderlich.

## Security-Auswirkung

Der Caller erhält die bestehende Root-Grenze: Nur der unveränderliche Broker-
Commit checkt geschützten Broker-Source aus und führt ihn unter root aus,
während der Caller weder Target-Parent-Code noch eine Root-Aktion ausführt.
Sein Target-SHA wird geprüft, bevor er in ein Manifest gelangen kann, und kein
Shellcommand, Artefaktpfad, keine Variante, kein Profil, Framework-SHA,
Broker-SHA, CRS-Tupel, Regel, Binary, Modul oder Konfiguration wird durch den
Dispatch-Input ausgewählt. Der explizite Evidence-Validator verhindert zudem,
dass ein veraltetes, fremdes, unvollständiges, unbekanntes oder mit
fehlgeschlagenem Cleanup versehenes Artefakt als erfolgreicher Caller-
Lifecycle gemeldet wird.

## Runtime-Evidence

Zu diesem lokalen Change-Record-Zeitpunkt wurde kein Protected-master-Caller-
Lauf beobachtet. Ein erfolgreicher manueller Post-Merge-Dispatch muss den
realen GitHub-Kontext, den unveränderlichen Reusable-Aufruf, Root-Master-/Nicht-
root-Worker-Lifecycle, beide Profile, CRS-Audit, Artefakt-Upload/-Download und
Cleanup beweisen. Lokale Tests können diese resulting-master-Evidence nicht
ersetzen.

## Bekannte Einschränkungen

Der Caller validiert absichtlich die begrenzte Evidence eines unveränderlichen
Brokers; er verwandelt sie nicht in ein allgemeines privilegiertes
Ausführungssystem. Der GitHub-Artefakttransport bleibt die Plattformgrenze
zwischen Broker und unprivilegiertem Readback. Der Readback prüft daher strikte
Struktur und Cross-Field-Identität, statt ein separates Artefakt-
Signaturschema zu erfinden.

## Verbleibende Risiken

Die noch nicht beobachtete Hosted-Umgebung kann die read-only-API-Anfrage, den
Reusable-Workflow-Kontext, Artefakttransfer, NGINX-/ModSecurity-/CRS-Runtime
oder Cleanup abweisen. Ein Fehler eines Pre-Merge-Caller-Quality- oder
Protection-Gates blockiert den Caller-Merge. Ein Fehler des resulting-master-
Runtime-Dispatches blockiert dagegen nach diesem Caller-Merge die Fortsetzung
von PR #240; keines der Ergebnisse autorisiert einen Branch-Ref, Target-Code-
Ausführung, synthetisches PASS oder einen PR-240-Merge.

## Nicht ausgeführte Prüfungen mit Begründung

Das finale Python-3.14.6-Testgate, Hosted-Checks, CodeQL, SonarQube Cloud,
Review-/Branch-Protection-Gates und der Protected-master-Runtime-Dispatch
wurden für den finalen Head noch nicht beobachtet. Alle außer dem separaten
Post-Merge-Protected-master-Runtime-Dispatch bleiben vor Caller-Delivery oder
Caller-Master-Integration erforderlich. Dieser Runtime-Dispatch ist stattdessen
vor der Fortsetzung von PR #240 erforderlich.

## Finaler Diff- und Review-Status

Der normale initiale Push erzeugte Draft-PR #259 auf dem getrennten Branch
`fix/ci-protected-nginx-broker-caller`, synchronisiert mit aktuellem
`origin/master` bei `83094eb659f0b5df8c2df30b1ae718d524a9adf0`. Sein initialer
Head war `b50849263b88a1e9aae5e2c596d05a9af1e88832`: Sichtbare GitHub-Actions-
und CodeQL-Checks bestanden, während SonarQube Cloud die oben festgehaltenen
aufgabeneigenen Befunde fand. Die Upstream-Synchronisierung enthält im finalen
PR-Diff keine task-eigene Framework- oder MRTS-Gitlink-Änderung. Es gab keine
PR-240-Änderung, Framework-Quelländerung, MRTS-Quelländerung, keinen Force-
Push, History-Rewrite, Admin-Bypass oder Auto-Merge. Der Caller-PR muss Draft
und merge-blockiert bleiben, bis seine Exact-Head-Lokal-, Security-, Hosted-,
Sonar-, Review- und Branch-Protection-Evidence vollständig ist.
