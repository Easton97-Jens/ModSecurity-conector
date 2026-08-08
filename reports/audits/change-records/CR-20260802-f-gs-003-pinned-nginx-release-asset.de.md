# F-GS-003 — Gepinnte NGINX-Release-Provenance für Full-Smoke

**Sprache:** [English](CR-20260802-f-gs-003-pinned-nginx-release-asset.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | F-GS-003 |
| Datum (UTC) | 2026-08-02 |
| Basis-Revision | 97afc25007a20fff0c637d364745a22c2feb7bba |

## Motivation und Problemstellung

Die NGINX-Quellauswahl von Full-Smoke verwendete einen veränderlichen
Release-Selektor. Damit kann für einen sicherheitsrelevanten Runtime-Build
keine reproduzierbare und überprüfbare Source-Provenance nachgewiesen werden.
Diese Änderung dokumentiert das beabsichtigte feste Release-Tupel und die
zugehörige Evidence-Grenze.

## Akzeptanzkriterien

- Der Full-Smoke-Workflow übergibt das überprüfte NGINX-1.31.3-Release-Tupel:
  GitHub-Release-Modus, Repository nginx/nginx, Tag und Ref release-1.31.3,
  Asset nginx-1.31.3.tar.gz und SHA-256
  a7657c50811c2d92d9895395e8b873ef60398142c4db21eb647811c38f6dd525.
- Veränderliche latest-Selektoren werden nicht als Full-Smoke-Provenance
  akzeptiert, und der Resolver validiert das feste Tupel vor Cache-, Netzwerk-,
  Download- oder Extraktionsarbeit.
- Die Cache-Identität bindet das vollständige Tupel; das strikte
  Full-Smoke-Flag weist geerbte System- oder MRTS-NGINX-Overrides als Evidence
  zurück.
- Die manuelle Cleanup-Eingabe ist boolesch und standardmäßig deaktiviert.
  Cleanup läuft nur nach einem ausdrücklichen Opt-in, während der Smoke-Job
  seine Abhängigkeit behält und eine always-Bedingung verwendet, damit ein
  übersprungener Cleanup Smoke nicht überspringt.
- Englische und deutsche NGINX- und Variablendokumentation beschreiben
  dieselbe Release-Provenance-Grenze.
- Parent-Runtime-, CI-, Pull-Request- und Merge-Evidence bleiben ausstehend
  und gelten in diesem Record nicht als Akzeptanznachweis.

## Implementierungsentscheidung und Begründung

Workflow und Wrapper übergeben das vollständige feste Tupel an den
Parent-Resolver. Das Design weist veränderliche Selektoren früh zurück, bindet
die Cache-Wiederverwendung an jedes überprüfte Tupel-Mitglied, verifiziert den
Archiv-Digest und lässt den strikten Full-Smoke-Pfad keine geerbten nativen
NGINX-Binär- oder Modul-Overrides zu. Direkte Release-Asset-Provenance ersetzt
jede latest-Release-Ermittlung.

Artifact-Cleanup kann frühere Evidence löschen und ist deshalb bewusst keine
normale Nebenwirkung eines manuellen Runs. Der Job cleanup-artifacts wird durch
die Workflow-Dispatch-Eingabe cleanup_artifacts gesteuert, deren Standardwert
false ist. Der Smoke-Job behält seine needs-Beziehung und toleriert den
übersprungenen Cleanup-Job ausdrücklich.

Framework-Provenance wird getrennt von Parent-Delivery dokumentiert. Framework
PR #60 hatte vor der Integration Head
9c4ebef13eab8cfb2e8626bbf2738023c2320ad5. Ein angefragter SHA-gebundener
Merge wurde zurückgewiesen, weil Merge-Commits deaktiviert sind; der
repository-gebilligte SHA-gebundene Squash-Merge wurde um
2026-08-02T13:29:14Z abgeschlossen. Sein PR-#60-Merge/Master-Ergebnis ist
8362b569406cabc5237a41e4e46f0505fb04c51f, das in diesem Parent-Task-Worktree
bewusst das Gitlink-Ziel ist.

## Geänderte Dateien

Die folgende Liste ist der abgeglichene Task-Worktree-Bestand nach der
Integration der Core-, Evidence- und Test-Slices.

- .github/workflows/test-full-smoke-sequential.yml
- ci/checks/evidence/check-runtime-producer-readiness.py
- ci/evidence/reports/generate-system-environment-proof.py
- ci/evidence/reports/update-runtime-reports.py
- ci/provisioning/components/prepare-runtime-components.py
- ci/provisioning/components/prepare-runtime-components.sh
- connectors/nginx/README.md und connectors/nginx/README.de.md
- connectors/nginx/harness/README.md und connectors/nginx/harness/README.de.md
- docs/reference/variables.md und docs/reference/variables.de.md
- Gitlink modules/ModSecurity-test-Framework
- tests/test_prepare_runtime_components.py
- tests/test_report_presentation_literals.py
- tests/test_runtime_component_cache_contract.py
- tests/test_runtime_component_cache_identity.py
- tests/test_runtime_env_snapshot_contract.py
- tests/test_evidence_output_security.py

## Ausgeführte Befehle

- Der Repository-Workflow-YAML-Checker wurde für
  .github/workflows/test-full-smoke-sequential.yml erfolgreich ausgeführt.
- Eingegrenzte statische Assertions für das exakte Full-Smoke-NGINX-Tupel, das
  Fehlen von latest-Selektoren in diesem Workflow und den Wrapper-Export der
  Provenance-Variablen waren erfolgreich.
- Der Checker für zweisprachige Dokumentation und der
  Variablendokumentations-Checker waren nach dem Hinzufügen dieses Change
  Records erfolgreich.
- Die Shell-Syntaxprüfung war erfolgreich. ShellCheck meldete nur die drei
  bereits im Basis-Wrapper vorhandenen Diagnosen.
- Eingegrenztes git diff --check war beim Ausführen für den Dokumentations- und
  Workflow-Slice erfolgreich.
- Auf dem nicht CI-äquivalenten lokalen Python-3.14.4-Interpreter bestanden
  AST-Parsing, der Producer-Readiness-Path-Policy-Test mit 4/4, der
  Evidence-Output-Security-Test mit 9/9 und das Report-Presentation-Unittest-
  Modul mit 5/5. Der Evidence-Slice-Diff-Check bestand, und es wurde keine
  Consumer-Referenz auf nginx-latest-release.json gefunden.
- Die integrierte fokussierte diagnostische Suite bestand 108 Tests auf dem
  vorhandenen Parent-Interpreter der virtuellen Umgebung (Python 3.14.4), mit
  `PYTHONDONTWRITEBYTECODE=1` und einem externen `PYTHONPYCACHEPREFIX`. Dies
  ist nur nützliche lokale Evidence; das Projekt erfordert Python 3.14.6 für
  CI-äquivalente Validierung.
- Die Python-Kompilierung des geänderten Resolvers und des System-Environment-
  Proof-Reporters bestand. Ein finaler eingegrenzter `git diff --check` bestand
  vor der Delivery.

## Security-Auswirkung

Die beabsichtigte Kontrolle ist fail-closed Release-Provenance: Ein
überprüftes Tupel muss vollständig und gültig sein, bevor Cache- oder
Beschaffungsarbeit beginnt, und das Archiv muss vor der Nutzung seinem
überprüften Digest entsprechen. Der strikte Full-Smoke-Modus verhindert, dass
geerbte System- oder MRTS-NGINX-Artefakte als erforderliche
Managed-Build-Evidence dargestellt werden.

Die integrierten Core-, Evidence- und Test-Slices binden zusätzlich den
Managed-Modulpfad an den Producer-Record und weisen MRTS- oder
Systempfad-Mismatches zurück. Dieser Record behauptet weiterhin nicht, dass
Parent-Runtime-Enforcement vollständig bewiesen ist: Hosted-Runtime- und
CI-Evidence bleiben ausstehend.

Der finale lokale Diff-Review fand, dass der System-Environment-Proof-Reporter
zuvor ein aus der Umgebung gewähltes `NGINX_BIN -v` vor der neuen Managed-
Runtime-Contract-Validierung ausführen konnte. Der Reporter liest den Contract
jetzt zuerst, schlägt fehlgeschlossen fehl, wenn er nicht `PASS` ist, ignoriert
`NGINX_BIN` und Framework-Kandidaten-Fallbacks und ruft nur den Contract-
`binary_path` nach einem erneuten SHA-256-Readback auf. Regressionstests
beweisen sowohl fehlendes Lookup/Ausführen bei ungültigem Contract als auch
fehlendes Ausführen nach einem Binary-Digest-Mismatch.

## Runtime-Evidence

Für diese Änderung wurden kein Parent-Build, kein Smoke-Run, kein
Runtime-Environment-Snapshot, kein Producer-Readiness-Output und kein
System-Environment-Proof als Evidence akzeptiert.

Der erforderliche Managed-Full-Smoke-Runtime-Evidence-Record muss bei seiner
Erzeugung Release, Ref und Asset; erwartete und tatsächliche Archiv-SHA-256-
Werte; Source-Version und Verzeichnis; Binary-Pfad, SHA-256 und Versions-
Readback; Configure-Argumente; Build-, Framework- und Parent-IDs; sowie die
Erstellungszeit identifizieren. Diese Feldliste ist ein erforderliches Schema
und keine Behauptung, dass ein aktueller Parent-Runtime-Record existiert.

Die beobachtete Framework-Integrationsevidence ist auf Folgendes begrenzt:
Für Framework PR #60 bestanden exakte-Head-PR-Checks und Sonar
Zero/Quality Gate vor der Integration; nach dem Merge bestanden auf Framework
Master die Workflows test-common, OpenSSF Scorecard, CodeQL analysis und lint.
Dies ist nur Framework-Provenance, keine Parent-Runtime-, CI-, PR- oder
Merge-Evidence.

## Bekannte Einschränkungen

Die repository-erforderliche virtuelle Python-3.14.6-Umgebung ist lokal nicht
verfügbar; der verfügbare Systeminterpreter ist Python 3.14.4 und keine
CI-äquivalente Evidence.

Core-, Evidence- und Test-Slices sind integriert, einschließlich der
diagnostischen Archiv-Nebenwirkungs-, Producer-zu-Checker-Contract- und
System-Proof-No-NGINX-I/O-vor-Contract-Abdeckung. Das fokussierte
108-Test-Ergebnis wurde nur mit Python 3.14.4 erzeugt und ist daher keine
CI-äquivalente Validierung.

## Verbleibende Risiken

- Die diagnostische Suite wurde nicht unter der repository-erforderlichen
  Python-3.14.6-Umgebung ausgeführt.
- Hosted-Workflow-, Parent-Runtime-, Parent-CI-, Parent-PR- und Parent-Merge-
  Evidence wurde noch nicht beobachtet.

## Nicht ausgeführte Prüfungen mit Begründung

- actionlint wurde lokal nicht ausgeführt, weil es für diesen Task nicht
  installiert oder bereitgestellt ist; hosted actionlint bleibt ausstehend.
- Parent-Unit- und Integrationstests wurden nicht unter der erforderlichen
  Python-3.14.6-Umgebung ausgeführt, weil diese exakte Umgebung nicht
  verfügbar ist. Die fokussierte diagnostische 108-Test-Suite lief stattdessen
  in der vorhandenen Parent-virtuellen Umgebung mit Python 3.14.4 und ist
  ausdrücklich nicht CI-äquivalent.
- Parent-Build-, Runtime-Smoke-, Evidence-Generierungs-, manueller
  Full-Smoke-Matrix-, CI-, PR- und Merge-Checks bleiben als Hosted-Runtime- und
  Delivery-Evidence ausstehend.

## Finaler Diff- und Review-Status

Der Status beim Erstellen des Records ist in Bearbeitung, nicht abgeschlossen.
Ein unabhängiger Englisch/Deutsch-NGINX-Dokumentationsparitätsreview war
erfolgreich, und die Core-/Evidence-/Test-Slices sind integriert. Finaler
Parent-Diff, Hosted-Runtime-Validierung sowie Parent-CI-, PR- und
Merge-Disposition müssen vor einer Abschlusserklärung geprüft werden. Dieser
Record beansprucht keine Parent-Delivery-Aktion.
