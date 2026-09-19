# Change Record

**Sprache:** [English](CR-20260919-update-submodule-sha-projection.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260919-update-submodule-sha-projection |
| Datum (UTC) | 2026-09-19 |
| Basis-Revision | e475baabf0787cbc804f176ae998b62156892825 |

## Motivation und Problemstellung

Der GitHub-Actions-Update-submodules-Run 35441775719 scheiterte bei Validate
Framework component-pin data contract. Sein Kandidat war
cc36b37d0f6a0fbc3512f3878a691751e91c5fbb, während der aktuelle Parent-Gitlink
d4f7b69dc264852eac74e1439c0887fcb9fbe372 war. Der Validator verlangte, dass
die statischen Parent-Konsumenten dem Kandidaten entsprechen, bevor der einzige
autorisierte Publisher diese Projektion erzeugen konnte. Der generische
Synchronisierer besaß diese Konsumenten nicht und die Publisher-Allowlist schloss
sie aus.

Die angeforderte Parent-only-Korrektur beseitigt diesen deterministischen
Ordnungs-Deadlock. Sie ändert weder Framework- noch MRTS-Source, Parent-
Gitlink, NGINX-Ownership, Protected-Broker-Pins, Berechtigungen oder den
Delivery-Status.

## Akzeptanzkriterien

- Ein vom aktuellen Gitlink verschiedener Kandidat besteht die read-only-
  Validierung gegen die aktuelle statische Parent-Projektion.
- Der Publisher beweist den aktuellen Zustand, projiziert den Kandidaten in
  genau fünf geprüfte statische Slots und prüft danach den resultierenden
  Kandidatenzustand.
- Ungültige, fehlende, doppelte, gequotete, falsch platzierte, fehlgeformte
  oder dynamisch aliasierte statische Slots scheitern vor einem Zielschreiben;
  dynamische Workflow-Konsumenten bleiben unverändert.
- Die explizite Publisher-Allowlist und das Staging umfassen nur die zwei neu
  besessenen Projektionsdateien, und generische NGINX-Nichtkonsumierung bleibt
  erzwungen.
- Fokussierte Regressionstests und der CI-Security-Contract bestehen lokal.
  Hosted-Exact-Head-Proof bleibt eine getrennte Delivery-Bedingung.

## Implementierungsentscheidung und Begründung

Der Synchronisierer akzeptiert nun einen separat validierten kleingeschriebenen
Resolver-SHA; er liest diesen Wert nicht aus candidate common.sh. Eine
geschlossene Projektionsregistry besitzt einen CRS/no-MRTS-Workflow und ein
Test-Fixture. Sie verlangt ein EXPECTED_FRAMEWORK_SHA, drei literale
FRAMEWORK_SHA-Zuweisungen, eine Fixture-Konstante und erhält zwei exakt
dynamische Workflow-Zuweisungen byte-identisch.

Die read-only-Validierung vergleicht die fünf statischen Konsumenten mit dem
aktuellen Gitlink. Der privilegierte Publisher wiederholt diesen Vergleich,
projiziert den Resolver-Kandidaten-SHA atomar und prüft anschließend den
Kandidatenzustand. Der Kandidatenverifier akzeptiert einen getrennten erwarteten
Parent-SHA für den Vor-Schreibvergleich. Das bewahrt bestehende Kandidaten-
Origin-, Struktur-, NGINX- und Protected-Broker-Controls, ohne die generische
Source-Registry zu erweitern.

## Geänderte Dateien

- .github/workflows/update-submodules.yml
- ci/tools/sync-framework-component-versions.py
- ci/tools/verify-framework-candidate-contract.py
- tests/test_update_framework_versions.py
- tests/test_verify_framework_candidate_contract.py
- tests/test_ci_security_workflows.py
- reports/audits/change-records/CR-20260919-update-submodule-sha-projection.md
- reports/audits/change-records/CR-20260919-update-submodule-sha-projection.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

Keine Framework-/MRTS-Source, Gitlink-, .gitmodules-, Dependency-, Credential-,
Workflow-Permission-, generierte Report- oder Production-Runtime-Source-Datei
wurde geändert.

## Ausgeführte Befehle

- python -m unittest -v tests.test_update_framework_versions
  tests.test_verify_framework_candidate_contract
  tests.test_ci_security_workflows — 76 Tests bestanden.
- make check-ci-security-contract — 153 Tests bestanden mit fünf erwarteten
  nicht verfügbaren Namespace-/Identity-Integrations-Skips.
- python -m py_compile für geänderte Python-Pfade und Tests — bestanden.

Die Befehle liefen im isolierten Task-Worktree mit eigenen temporären und
Bytecode-Cache-Pfaden. Erwartete Negative-Test-Diagnosen in der Testausgabe
sind Assertions des fail-closed-Verhaltens, keine Testfehler.

## Security-Auswirkung

Diese Änderung berührt eine GitHub-Actions-Publication-Grenze. Der Resolver-SHA
wird getrennt von candidate common.sh validiert, die Zielmenge ist geschlossen
und strikt kardinalitätsgeprüft, der Publisher beweist den aktuellen Zustand vor
dem Schreiben und den Kandidatenzustand danach, und die neuen Pfade sind
explizit allowlisted und gestaged. NGINX bleibt von der generischen
Synchronisierung ausgeschlossen; Protected-Broker-Pins und bestehende Workflow-
Berechtigungen bleiben unverändert.

Ein unabhängiges statisches Post-Patch-Review fand keinen reportierbaren
Security-Befund. Es führte keinen Hosted-Workflow aus und ersetzt keine Exact-
Head-Delivery-Evidenz.

## Runtime-Evidence

Der autoritative Fehler ist [GitHub-Actions-Run 35441775719](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35441775719).
Secret-free zurückgehaltene lokale Evidence ist unter
.codex/runs/20260919-fix-actions-run-35441775719/evidence.md festgehalten; der
aktuelle Artifact-Hash steht im Hash-Inventar dieses Runs.

Zum Zeitpunkt der Erstellung dieses Change Records gab es kein Hosted-Workflow-
Ergebnis für den vorgesehenen Task-Head. Der autorisierte Delivery-Lifecycle
hält seine tatsächlichen Commit-, Branch- und Pull-Request-Fakten in der Task-
Evidence fest. Dieser Change Record behauptet keinen Merge, GitHub-Rerun,
Framework-Change oder MRTS-Change.

## Bekannte Einschränkungen

Lokale Tests können weder GitHub-Hosted-Token-Berechtigungen, Scheduler-
Expressions, Branch-Protection, konkurrierende Remote-Races noch eine reale
spätere Framework-Kandidaten-Transition ausführen. Für die fünf dokumentierten
Skips besitzt die Testumgebung kein verfügbares Namespace-/Identity-
Integrationssetup.

## Verbleibende Risiken

Ein zukünftiger unabhängiger privilegierter Caller muss das neue
--framework-sha-Argument weiterhin an ein offizielles Resolver-Ergebnis binden.
Der aktuelle Workflow tut dies über seinen Resolver-Output. Bewegter Remote-
Zustand, fehlgeformter Kandidat, ungültige Projektion, Allowlist-Mismatch oder
Hosted-Fehler bleiben fail closed; es gibt keinen Fallback, Auto-Merge oder
Permission-Expansion.

## Nicht ausgeführte Prüfungen mit Begründung

Zum Zeitpunkt der Erstellung dieses Change Records war kein autorisierter
Hosted-Workflow-Rerun oder Merge ausgeführt. Deshalb lagen Exact-Task-Head-
Update-submodules-, CI-Security-, GitHub-actionlint-, Branch-Protection-,
Review- und Resulting-master-Evidenz noch nicht vor. Ein separater lokaler
actionlint-Lauf war für den Source-Contract nicht erforderlich, weil das
CI-Security-Target die gepinnte Tool-Verfügbarkeit validiert und die
fokussierten Workflow-Contract-Tests bestanden; Hosted-actionlint am exakten
Head bleibt für die Delivery erforderlich.

make check-bilingual-docs wurde versucht, endete jedoch mit Exit 2, weil der
isolierte Task-Worktree kein initialisiertes Framework-Submodule hat. Es meldete
nur vorbestehende fehlende Links unter modules/ModSecurity-test-Framework und
keinen Fehler für dieses Change-Record-Paar. Das Initialisieren oder Ändern
dieser getrennten Repository-Grenze lag außerhalb des Scopes.

## Finaler Diff- und Review-Status

Die Parent-only-Änderung ist auf Updater-Workflow, begrenzten Projektor und
Verifier, ihre fokussierten Tests sowie diesen gepaarten Change-Record-Index
beschränkt. Sie bestand die festgehaltenen lokalen Checks und ein unabhängiges
statisches Security-Review. Das Finding bleibt in_progress, bis Exact-Head-
Hosted-Evidenz vorliegt; ein Merge wird nicht behauptet.
