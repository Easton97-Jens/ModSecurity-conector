# F-GS-003 — Gepinnte NGINX-Release-Provenance für Full-Smoke

**Sprache:** [English](CR-20260802-f-gs-003-pinned-nginx-release-asset.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | F-GS-003 |
| Datum (UTC) | 2026-08-02 |
| Basis-Revision | a308e52508a46a62b2f948245ebfa8e153f73bce |

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

Die Parent-Master-Synchronisierung übernimmt den Framework-Gitlink
`209389022c942d83113f6be88bf31d25637352f0` aus ihrer bereits gemergten
Parent-Basis. Er ist keine durch F-GS-003 erzeugte Änderung, und dieser
Change Record behauptet weder eine Framework-Änderung noch untersucht er
Framework-PR #74.

## Geänderte Dateien

Die folgende Liste ist der abgeglichene Parent-Bestand des PR-Range nach dem
Merge der aktuellen Parent-Basis am 2026-08-12. Der Framework-Gitlink steht
nicht in dieser Liste, weil er aus der Basis stammt und keine F-GS-003-Änderung
ist.

- .github/workflows/test-full-smoke-sequential.yml
- Makefile
- ci/checks/evidence/check-runtime-producer-readiness.py
- ci/evidence/reports/generate-system-environment-proof.py
- ci/evidence/reports/update-runtime-reports.py
- ci/provisioning/components/prepare-runtime-components.py
- ci/provisioning/components/prepare-runtime-components.sh
- ci/runtime/lifecycle/prepare-fresh-crs-source.sh
- connectors/nginx/README.md und connectors/nginx/README.de.md
- connectors/nginx/harness/README.md und connectors/nginx/harness/README.de.md
- docs/reference/variables.md und docs/reference/variables.de.md
- tests/test_prepare_runtime_components.py
- tests/test_report_presentation_literals.py
- tests/test_runtime_component_cache_contract.py
- tests/test_runtime_component_cache_identity.py
- tests/test_runtime_env_snapshot_contract.py
- tests/test_evidence_output_security.py

`prepare-fresh-crs-source.sh` bleibt in diesem Parent-Range als separater
CRS-Source-Separation-Helper erhalten. Er behebt oder validiert nicht die
separaten Broker-/CRS-Findings. APR-util-/Provider-Arbeit, Broker-Reparaturen
und die CRS-Fehler-Disposition bleiben außerhalb von F-GS-003 und sind keine
Merge-Blocker für diesen reinen Provenance-Akzeptanzpfad.

## Ausgeführte Befehle

- Am 2026-08-12 bestand die aktuelle lokale statische Validierung mit der
  vorhandenen nicht CI-äquivalenten Parent-Python-3.14.4-virtuellen Umgebung:
  Die sechs fokussierten Runtime-Component-/Evidence-Unittest-Module endeten
  mit Exit 0; die zwei F-GS-003-Workflow-Contract-Testmethoden bestanden;
  geänderte Python-Dateien kompilierten; geänderte Shell-Dateien bestanden
  `sh -n`; und der Repository-Workflow-YAML-Checker akzeptierte alle 29
  Workflow-YAML-Dateien.
- `make check-ci-security-contract` bestand lokal: 26 Tests, actionlint,
  zizmor und die gitleaks-Validierung waren erfolgreich. Dies sind
  statische/lokale Prüfungen, keine Runtime-Provision oder Hosted-Gate-Ergebnis.
- Zwei unabhängige Läufe von `make --no-print-directory prepare-runtime-components`
  mit `RUNTIME_COMPONENT_TARGET=nginx`, festem NGINX-1.31.3-Tupel und
  isolierten externen Build-/Cache-/Report-Roots endeten vor dem finalen
  Traceability-Commit mit Exit 0. Diese Pre-Final-Commit-lokale Evidence ist an
  Parent `1aa5f6f7` gebunden und ein nützlicher Konsistenzcheck, keine finale
  PR-Head-Evidence. Ihre Report-SHA-256-Werte sind
  `0927d2e4f912038c47d681bd401ba8f88f28322986af85f3833b2be68282999c`
  (Lauf A) und
  `be456afbd3021f669bdf5fa13e818774332b2ec6ff9119357d32bbd9acc4ba42`
  (Lauf B). Jeder Report weist die erwartete NGINX-Archiv-Prüfsumme
  `a7657c50811c2d92d9895395e8b873ef60398142c4db21eb647811c38f6dd525` als
  `PASS` sowie einen gültigen Runtime-Contract aus. Nur `modsecurity-v3` und
  `expat` waren ausgewählte Git-Komponenten; Apache, HAProxy, go-ftw und
  albedo waren `not_selected`. Die beobachteten Binary-/Modul-SHA-256-
  Identitäten waren `f19f8b9a…afc7e` / `40a5c734…9b38` (Lauf A) sowie
  `087c5e5e…5b1e` / `03b49502…f4fd` (Lauf B), bei Parent `1aa5f6f7` und
  Framework `209389`. Es wurde kein MRTS-Workload aufgerufen; ein inert
  konfigurierter Root ist kein MRTS-Workload oder Evidence-Anspruch.
- Ein eingegrenztes `git diff --check` bestand nach der Synchronisierung. Die
  zweisprachigen und Variablen-Dokumentations-Checker bleiben Teil der finalen
  Dokumentationsvalidierung und werden erst nach ihrem erneuten Lauf gegen
  diesen Abgleich als bestanden beansprucht.

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

Zwei frische Parent-NGINX-only-Provisionen wurden als lokale Runtime-Evidence
vor dem finalen Traceability-Commit akzeptiert. Sie verwendeten unabhängige
task-eigene externe Roots, die in einer nicht versionierten, hash-gebundenen
Receipt erhalten sind, und führten weder einen Host-Smoke, einen Hosted-Workflow
noch einen MRTS-Workload aus. Sie ersetzen nicht den noch ausstehenden
Runtime-Environment-Snapshot, Producer-Readiness-Output oder System-Environment-
Proof des vollständigen Delivery-Lifecycles. Zwei frische isolierte
Provisionen müssen nach dem finalen versionierten Commit und Push erneut laufen;
sie werden noch nicht als finale PR-Head-Provisionen beansprucht.

Der erforderliche Managed-Full-Smoke-Runtime-Evidence-Record muss bei seiner
Erzeugung Release, Ref und Asset; erwartete und tatsächliche Archiv-SHA-256-
Werte; Source-Version und Verzeichnis; Binary-Pfad, SHA-256 und Versions-
Readback; Configure-Argumente; Build-, Framework- und Parent-IDs; sowie die
Erstellungszeit identifizieren. Diese Feldliste ist ein erforderliches Schema
und keine Behauptung, dass ein aktueller Parent-Runtime-Record existiert.

Der aus der Basis stammende Framework-Gitlink ist nur eine Dependency-Identität;
er ist keine Framework-Runtime-, CI-, PR- oder Merge-Evidence für diese
Parent-Änderung.

## Bekannte Einschränkungen

Die repository-erforderliche virtuelle Python-3.14.6-Umgebung ist lokal nicht
verfügbar; der verfügbare Systeminterpreter ist Python 3.14.4 und keine
CI-äquivalente Evidence.

Die aktuelle lokale Python-Version ist 3.14.4 statt der repository-erforderlichen
3.14.6; alle lokal beobachteten Python-Ergebnisse bleiben deshalb
nicht CI-äquivalent.

## Verbleibende Risiken

- Die aktuelle lokale Suite lief nicht unter der repository-erforderlichen
  Python-3.14.6-Umgebung.
- Es wurde keine Host-Smoke-, Hosted-Workflow-, Parent-CI-, Parent-PR- oder
  Parent-Merge-Evidence beobachtet.
- Die zwei dokumentierten isolierten Provisionen liegen vor dem finalen
  Traceability-Commit; finale PR-Head-Provisionen bleiben erforderlich.

## Nicht ausgeführte Prüfungen mit Begründung

- Die aktuellen fokussierten lokalen Python-Checks sind nicht CI-äquivalent,
  weil Python 3.14.6 lokal nicht verfügbar ist.
- Host-Smoke, verbleibende Runtime-Evidence-Generierung, Hosted-Checks,
  finale PR-Head-isolierte Provisionen, Exakt-Head-PR-Gates und
  Merge-Verifizierung bleiben als Delivery-Evidence ausstehend.

## Finaler Diff- und Review-Status

Der Status bleibt in Bearbeitung, nicht abgeschlossen. Der finale Parent-Diff,
Host-Smoke- und Hosted-Runtime-Validierung, finale PR-Head-isolierte
Provisionen, Parent-CI, Exakt-Head-PR-Gates und die Merge-Disposition müssen
vor einer Abschlusserklärung geprüft werden.
Dieser Record beansprucht keine Parent-Delivery-Aktion.
