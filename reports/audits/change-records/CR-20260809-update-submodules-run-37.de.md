# Change Record

**Sprache:** [English](CR-20260809-update-submodules-run-37.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260809-update-submodules-run-37 |
| Datum (UTC) | 2026-08-09 |
| Basis-Revision | 128a2f63f182758b1c1a1d4746f5e56f609d245d |

## Motivation und Problemstellung

GitHub-Actions-Update-submodules-Run #37, ID 31307156102, scheiterte, nachdem
sein Resolver den Parent-Gitlink 3a8074e0b7ef698b941e7649b8a86e639f838a0c zum
Framework-Kandidaten 4c9af1cee72caa0107fa011e59eef9e853338cf5 auflöste.
Resolver-Job 93229208675 bestand. Validator-Job 93229238042 detach-te den
Kandidaten und startete make quick-check; sein erster echter Fehler war
test_haproxy_prepare_does_not_rebuild_a_verified_runtime_binary bei
tests/test_prepare_runtime_components.py:1254 mit AssertionError: True is not
false. Zwei verwandte Cache-Reuse-Fehler folgten, make endete mit 2, und
Publisher-Job 93229465918 wurde ohne Commit-, Push- oder Pull-Request-Mutation
übersprungen.

Dies war Kategorie C, Parent/Framework-Kompatibilität: Die Parent-Test-Fixture
kodierte die frühere reale HAProxy-Provenance 3.2.21 und
0cb8818a26c5f888e0cb1c40f1b3acb9fb952527d1733f769ce688fedd680339, übergab
sie aber nicht als Testinput. Kandidat 4c9af1c verwendet korrekt HAProxy 3.2.22
und afca3a26d573df53d0e1fc475dcd743ec5875e038e1476c80e871d70228ca2da,
erkennt stale Provenance, baut neu und invalidiert eine Reuse-Assertion. Es war
kein Resolver-, Checkout-, Publisher- oder GitHub-Permissions-Fehler.

## Akzeptanzkriterien

- Die Fixture verwendet atomare synthetische Baseline- und Ziel-Version-/Digest-
  Tupel; sie behandelt keinen realen aktuellen Framework-Produktionspin als
  Unit-Test-Voraussetzung.
- Ein synthetisches Future-Tupel beweist verifizierten Binary-Reuse ohne
  Download oder Rebuild, während der separate BUILD_ROOT-Exit-77-Negativcontrol
  erhalten bleibt.
- Kandidatenvalidierung bleibt read-only und obligatorisches make quick-check
  läuft, bevor der write-fähige Publisher eligible werden kann.
- Publisher löst Kandidat und aktuellen Parent-master-Gitlink erneut auf,
  erlaubt nur den Framework-Gitlink und scheitert fail closed bei stale,
  malformed, fremdem, Auto-Merge- oder mehrdeutigem Maintenance-Zustand.
- Zustand A erzeugt einen Branch normal; bewiesener Zustand B aktualisiert
  einen markierten Draft-PR über eine SHA-gebundene Lease; bewiesener Zustand C
  reused nur einen verifizierten gemergten Updater-Branch über dieselbe
  explizite Lease; jeder andere Zustand scheitert.
- Der always-run read-only-Resultjob behandelt Resolver-Success plus
  changed=false und skipped Validator/Publisher als Success, hält aber unknown
  Output und Validator-/Publisher-Fehler rot.

## Implementierungsentscheidung und Begründung

Der Parent-Cache-Fixture-Helper übergibt jetzt synthetische HAPROXY_VERSION,
HAPROXY_SOURCE_URL, HAPROXY_SHA256_URL, HAPROXY_SHA256 und passende
Source-Directory-Werte. Baseline 3.2.9000/a*64 und Target 3.2.9001/b*64 sind
test-only-Werte, die atomar durch den bestehenden Environment-Seam gehen. Keine
Framework-Shell-Datei wird gesourct, geparst oder ausgewertet, um einen Wert zu
lesen. Ein Future-Tuple-Test verifiziert das beabsichtigte Reuse-Verhalten.

Der Workflow behält Resolver-, Validator- und Publisher-Trennung und ergänzt
einen always-run read-only-Outcome-Job. Resolver validiert exakt eine
offizielle Referenz und den aktuellen Gitlink. Validator prüft Candidate-
Ancestry, offiziellen Origin, detached rekursive Sauberkeit und obligatorisches
make quick-check.

Vor jedem Publisher-Commit/Push werden aktueller Framework-master und
Parent-master erneut gelesen; ein bewegter Parent-Gitlink scheitert statt eines
stale Übergangs. Publisher konstruiert exakt eine mode-160000-Gitlink-Änderung
von aktuellem master mit commit-tree und weist jeden anderen staged Pfad ab. Er
verwendet normalen Push nur für fehlenden Branch Zustand A und
--force-with-lease=refs/heads/chore/update-submodules:EXPECTED_REMOTE_HEAD nur
für bewiesenen Zustand B oder C. Er löscht keinen Branch, verwendet keinen
General-Force-Push, aktiviert kein Auto-Merge und verwendet keinen PAT-, SSH-
oder Deploy-Key-Fallback.

Der aktuelle Remote chore/update-submodules-Zustand war C-ähnlich:
fd7e63d7994fd9322c5bbb7862ef283d436c88d5 ist der Head von gemergtem PR #258
und es gibt keinen passenden offenen PR. Sein alter Body hat keinen neuen
Marker, daher prüft der Workflow Metadaten/History zur Laufzeit erneut statt
diese Beobachtung zu vertrauen.

## Geänderte Dateien

- .github/workflows/update-submodules.yml
- tests/test_prepare_runtime_components.py
- tests/test_ci_security_workflows.py
- reports/audits/change-records/CR-20260809-update-submodules-run-37.md
- reports/audits/change-records/CR-20260809-update-submodules-run-37.de.md

Keine Framework-Source, MRTS-Source, Parent-Gitlink, .gitmodules-Datei,
Generator oder generierte Dokumentation änderte sich.

## Ausgeführte Befehle

Die detached Pre-Fix-Reproduktion verwendete Parent
83094eb659f0b5df8c2df30b1ae718d524a9adf0 und Kandidat
4c9af1cee72caa0107fa011e59eef9e853338cf5. Ihr unterstützender lokaler
CPython-3.14.4-/PyYAML-6.0.3-Lauf reproduzierte dieselben ersten drei Fehler und
Exit 2; Hosted-CPython-3.14.6-Run-#37-Evidence ist autoritativ.

Post-Fix-Checks bestanden im Task-Worktree gegen denselben Kandidaten:

- fokussierte fünf Managed-Cache-Tests, inklusive synthetischem Future-Tuple und
  separatem BUILD_ROOT-Control;
- PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
  tests.test_ci_security_workflows, 24 Tests;
- make check-ci-security-contract, inklusive lokaler immutable security-tool
  lock validation;
- Workflow-YAML-Parse- und Bash-Syntax-Checks;
- kandidatengebundenes make quick-check, inklusive 96 Core-Tests und seinen
  restlichen Repository-Checks;
- actionlint mit ShellCheck und zizmor offline plus seinen Safe/Unsafe-Fixtures.

Der initiale check-python-version-contract-Lauf scheiterte nur an
pre-existing Inventory-Einträgen ohne Bezug zu update-submodules; er meldete
diesen Workflow nicht. Er ist als Baseline-Limitierung, nicht als aufgehobener
Fehler erfasst.

## Security-Auswirkung

make quick-check bleibt obligatorisch im contents-read-Validator, dessen
Checkout persistierte Credentials deaktiviert und keinen GH_TOKEN- oder
Secrets-Reference hat. Der contents-write/pull-requests-write-Publisher ist ein
frischer nicht-rekursiver Checkout und führt weder quick-check noch einen
Framework-Submodule-Befehl aus. Candidate-SHA-Validierung, Official-URL-Checks,
Ancestry-Checks, Pre-Publish-Re-Resolution, no stale-master transition, exakte
Index-/Raw-Diff-Validierung, explizite B/C-Leases, PR-Marker/Draft/Author/Auto-
Merge-Checks und Post-Push-Head-Re-Read reduzieren TOCTOU- und Fremd-Branch-
Overwrite-Risiko.

Der erforderliche quick-check übt zwangsläufig geprüften Kandidaten-Code in der
isolierten read-only-Validierungsgrenze aus. Dieser Record behauptet kein neues
Framework-Shell-Sourcing, keinen Parser, keine Command Substitution und keine
Publisher-seitige Framework-Ausführung, um Versionen zu ermitteln.

## Runtime-Evidence

Die portable autoritative Quelle ist [GitHub-Actions-Run #37](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/31307156102)
und die oben genannten Resolver-, Validator- und Publisher-Job-IDs. Eine
secret-free lokale corroborating Summary ist für FND-PARENT-0114 mit SHA-256
335cbf19594d0c17b29820d7b09920e0e1e48ef0c08c30acc7d551210bbd100b versiegelt;
sie erfasst Resolver-Success, Candidate-/Current-SHA, Validatorfehler,
make-quick-check-Start, ersten Fehler, Folgefehler, Exit 2 und übersprungenen
Publisher. Sie ist kein versionierter Product- oder Delivery-Proof. Kein
Raw-GitHub-Log wird in diesen Record kopiert.

Jedes oben genannte Post-Fix-Ergebnis benennt den nativen Befehl und sein
beobachtetes Ergebnis gegen diesen Task-Worktree. Raw-lokales stdout gilt
absichtlich nicht als Delivery-Evidence; Exact-Head-PR-Checks, CI-Security-
Checks, Sonar-Quality-Gate und Review-Evidence bleiben erforderlich und sind
unten ausdrücklich pending.

## Bekannte Einschränkungen

Die lokale Umgebung hat CPython 3.14.4, während der Workflow 3.14.6 deklariert;
der exakte Hosted-Run #37 ist Patch-Version-Autorität. Statische Tests und
read-only-Zustandsinspektion können weder GitHub-Scheduler-Expressions noch
GitHub-Token, Branch-Protection-Verhalten, konkurrierende Remote-Races oder ein
tatsächliches späteres Framework-Update ausführen. Der Task darf diesen PR
ausdrücklich nicht mergen oder den Post-Merge-master-Workflow dispatchen.

## Verbleibende Risiken

GitHub-Zustand kann sich zwischen REST-Reads und der nächsten Aktion ändern.
Der Workflow prüft Zustand erneut und bindet B/C-Pushes an die beobachtete
Remote-SHA, aber kein lokaler Test kann eine Multi-Service-Branch-/PR-Operation
global atomar machen. Ein fehlgeschlagener Candidate-Quick-Check, stale
Candidate, bewegter master-Gitlink, Lease-Fehler, fremder Zustand, PR-Creation-
Race, Token-Konfigurationsfehler oder Hosted-Check-Fehler bleibt fail closed
und darf keinen Fallback oder Auto-Merge erzeugen.

## Nicht ausgeführte Prüfungen mit Begründung

In diesem Record-Stadium sind finale Exact-Head-Hosted-Checks, CodeQL,
CI Security, actionlint, zizmor, SonarQube Cloud Quality Gate, Review-Thread-
Status und Branch-Protection-Status bis zum autorisierten normalen Push und
genau einem Draft-PR offen. Der spätere master-Workflow-Lauf wird absichtlich
nicht dispatcht. Die lokale exakte CPython-3.14.6-Reproduktion ist nicht
verfügbar.

## Finaler Diff- und Review-Status

Der beabsichtigte Diff ist Parent-only: Test-Fixture-Entkopplung, Updater-
Workflow-Härtung/Result-Reporting, fokussierte statische Contracts und dieser
bilinguale Change Record. Er enthält keine Framework-/MRTS-Source-Änderung,
Gitlink-Änderung, .gitmodules-Änderung, General-Force-Push, Fallback-
Credential, Token-Expansion, Quality-Gate-Absenkung, Suppression oder Auto-
Merge. Finales Exact-Path-Staging, normaler Commit, normaler Push, ein Draft-
PR und Current-Head-Hosted-/Sonar-/Review-Verifikation bleiben vor Abschluss
der Delivery erforderlich.

## Framework-Pin-Drift-Audit

| Komponente | Framework-Quelle | Parent-Treffer klassifiziert | Quick-check-Relevanz | Korrektur |
| --- | --- | --- | --- | --- |
| HAProxy | ci/lib/common.sh defaults | Runtime-Cache-Test-Fixture war kausal | ja | Synthetische atomare Fixture-Tupel |
| NGINX | Framework provider/configuration | Parent forwarding oder non-runtime references | kein kausales Duplikat | Keine |
| Apache httpd | Framework provider/configuration | Nur documentation/generator literals | kein kausales Duplikat | Keine |
| APR | Framework provider/configuration | Nur documentation/reference material | kein kausales Duplikat | Keine |
| APR-util | Framework provider/configuration | Nur documentation/reference material | kein kausales Duplikat | Keine |
| PCRE2 | Framework provider/configuration | Parent forwarding/reference material | kein kausales Duplikat | Keine |
| CRS | Framework provider/configuration | Documentation/reference material | keine direkte Fixture | Keine |
| ModSecurity v3 | Framework provider/configuration | Test/reference material, nicht diese Fixture | kein kausales Duplikat | Keine |
| Traefik | Framework/provider metadata | Nur documentation metadata | kein kausales Duplikat | Keine |
| Envoy | Framework/provider metadata | Nur documentation metadata | kein kausales Duplikat | Keine |
| lighttpd | Framework/provider metadata | Nur documentation metadata | kein kausales Duplikat | Keine |
