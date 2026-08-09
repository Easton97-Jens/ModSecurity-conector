# Change Record

**Sprache:** [English](CR-20260809-ci-nginx-broker-runtime-snapshot.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260809-ci-nginx-broker-runtime-snapshot |
| Datum (UTC) | 2026-08-09 |
| Basis-Revision | ef88a616498e0a2893cd3da54003dd7cdea57015 |
| Framework-Gitlink | 03880bf66b3905940466ff10b3a431a27ecc6b26 |

## Motivation und Problemstellung

Der geschützte Lifecycle-Lauf 31328046595 stoppte korrekt vor der
Candidate-Erzeugung und vor jeder Root-Aktion, weil sein No-CRS-Job die
erforderlichen Exporte NGINX_BINARY und NGINX_MODULE nicht im aufruflokalen
Runtime-Snapshot fand. Der Broker verlangt zusätzlich MODSECURITY_SHARED_PREFIX.

Der generische Producer konnte effektive Runtime-Werte veröffentlichen, die von
Umgebung oder MRTS-Kompatibilitätseingaben beeinflusst waren. Das ist keine
zulässige Quelle für den privilegierten Broker. Die Reparatur gibt deshalb nur
dem geschützten Broker-Workflow einen engen, unabhängig validierten
Producer-zu-Consumer-Vertrag.

## Akzeptanzkriterien

Der geschützte Workflow wählt vor der Dependency-Vorbereitung einen festen
Snapshotvertrag. Sein einziger aufruflokaler Snapshot enthält exakt je eine
nichtleere Zuweisung für NGINX_BINARY, NGINX_MODULE und
MODSECURITY_SHARED_PREFIX und keine weiteren Exporte.

Diese Werte entsprechen einem privaten, kanonischen Provenance-Record, der aus
dem vollständigen NGINX-Plan statt aus Caller-Umgebung, PATH, einem
System-Binary, MRTS-Kompatibilitäts-Overrides oder einem ungeprüften
Cacheeintrag abgeleitet wird. Der Broker muss bei fehlenden, leeren, doppelten,
fehlerhaften, widersprüchlichen, ersetzten, außerhalb der Root liegenden,
verlinkten, falsch besessenen, schreibbaren oder Digest-inkonsistenten Eingaben
vor der Candidate-Erzeugung fail-closed abbrechen. No-CRS benötigt kein
CRS-Bundle; With-CRS ergänzt ausschließlich das geschützte Bundle und behält
dieselben NGINX-Artefakt-Digests in getrennten privaten Staging-Roots.

## Technische Entscheidungen

Der Vertrag ist bewusst auf den geschützten Workflow begrenzt. So bleibt die
Kompatibilitätsoberfläche generischer Snapshots erhalten, während die
Broker-Eingabe unabhängig reproduzierbar und ablehnbar wird.

## Implementierungsentscheidung und Begründung

nginx-root-broker.yml wählt RUNTIME_COMPONENT_SNAPSHOT_CONTRACT=protected-nginx-broker
vor make fetch-deps. In diesem Modus schreiben der bestehende kanonische
Serializer und der atomare Veröffentlichungsweg vor dem eingeschränkten
aufruflokalen Snapshot einen festen Record mit Modus 0600 unter
build/runtime-component-reports/trusted-nginx-broker-provenance.json.

Der Record hat ein festes Schema und eine kanonische kompakte SHA-256-Identität.
Er bindet Parent-Broker-Source-Revision, Framework-Gitlink, vollständigen
NGINX-Plan, Release-Tupel, kanonische NGINX-Binary-/Modulpfade,
ModSecurity-Library-Pfad sowie Artefaktmetadaten und Digests. Der Producer
leitet die beiden NGINX-Pfade aus dem kanonischen Planlayout ab, nicht aus
effektiven Umgebungswerten.

Der Broker liest sowohl Record als auch Snapshot ohne eine Datei zu sourcen. Er
verlangt exakte Record-Identität, private Regulärdatei-Metadaten, kanonische
Roots und Gleichheit der drei Snapshotwerte und leitet Candidate-Eingaben dann
nur aus dem erneut validierten Record ab. Generische Runtime-Snapshots behalten
ihr bestehendes Kompatibilitätsverhalten.

Das einzige Gitlink-Update setzt modules/ModSecurity-test-Framework mit Modus
160000 auf 03880bf66b3905940466ff10b3a431a27ecc6b26. Dieser Phase-B-Kandidat
ändert weder Framework-Source, MRTS-Source, MRTS-Gitlink, MRTS-Remote,
Caller-Pin noch Root-Aktion.

## Geänderte Dateien

- .github/workflows/nginx-root-broker.yml
- ci/provisioning/components/prepare-runtime-components.py
- ci/provisioning/components/prepare-runtime-components.sh
- ci/runtime/broker/nginx_root_broker.py
- modules/ModSecurity-test-Framework
- tests/test_runtime_env_snapshot_contract.py
- tests/test_nginx_root_broker.py
- tests/test_nginx_root_broker_crs_profile.py
- tests/test_nginx_root_broker_workflow.py
- tests/test_ci_security_workflows.py
- docs/security/trusted-nginx-root-broker.md und sein deutsches Gegenstück
- dieser Change Record und sein deutsches Gegenstück

## Tests und tatsächliche Ergebnisse

Fokussierte Producer-, Consumer-, Workflow-, Profil-, Dokumentations- und
Static-Checks decken den geschützten Vertrag ab; die beobachteten Befehle und
Ergebnisse folgen.

## Ausgeführte Befehle

Die folgenden reproduzierbaren Befehlsformen wurden im isolierten
Phase-B-Worktree beobachtet. TMPDIR war ein vorhandenes task-eigenes externes
Verzeichnis; kein Test schrieb in den Source-Tree.

- PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-owned TMPDIR> python3 -m unittest -v tests.test_runtime_env_snapshot_contract tests.test_runtime_producer_readiness_path_policy tests.test_nginx_root_broker tests.test_protected_nginx_broker_caller tests.test_nginx_root_broker_workflow tests.test_nginx_root_broker_crs_profile tests.test_ci_security_workflows — PASS, 100 Tests.
- make PYTHON=<Parent .venv>/bin/python check-runtime-producer-readiness — BLOCKED, Exit 77: Der isolierte Worktree hat absichtlich weder vorbereitetes NGINX-Binary/-Modul noch Archiv-Cache. make prepare-runtime-components würde einen unabhängigen netzwerkgebundenen Runtime-Build hinzufügen; die hermetischen Producer-Readiness-Tests oben sind die anwendbare lokale Kontrolle.
- make PYTHON=<Parent .venv>/bin/python check-ci-security-contract — PASS, 26 Workflow-Security-Tests sowie read-only actionlint-, zizmor- und gitleaks-Lock-Validierung.
- python3 -m py_compile ci/provisioning/components/prepare-runtime-components.py ci/runtime/broker/nginx_root_broker.py tests/test_runtime_env_snapshot_contract.py tests/test_nginx_root_broker.py tests/test_nginx_root_broker_crs_profile.py — PASS.
- sh -n ci/provisioning/components/prepare-runtime-components.sh — PASS.
- shellcheck --shell=sh --severity=error ci/provisioning/components/prepare-runtime-components.sh — PASS. Ein vollständiger Informationslauf meldet nur bestehende Diagnosen SC1007, SC1091 und SC2034; keine stammt aus diesem Diff.
- actionlint -shellcheck=/usr/bin/shellcheck .github/workflows/*.yml — PASS.
- zizmor --offline .github/workflows — PASS, keine Findings.
- make check-bilingual-docs und make check-doc-links — PASS.
- git diff --check HEAD — PASS.

Die optionale Cache-/Identity-/Producer-Suite hatte einen Fehler in
test_nginx_discards_marker_owned_partial_root_before_build: Ihrem Fixture fehlt
common/src/header_validation_internal.h. Derselbe Test schlägt auf sauberem
Parent master identisch fehl und ist bereits als FND-PARENT-0077 erfasst; er
wurde durch diese Reparatur weder unterdrückt noch geändert.

## Security-Auswirkung

Die Reparatur schließt die nachgewiesene Producer-/Consumer-Vertragslücke, ohne
den Broker zu lockern. Snapshot-Text bleibt deklarativ und kann kein
Candidate-Artefakt auswählen. Ein nur den Snapshot ersetzender Angriff, ein
Caller-Override, ein System- oder MRTS-Pfad und ein widersprüchlicher
Provenance-Record scheitern vor Candidate-Staging oder einer privilegierten
Operation. Die bestehende feste Root-Action-Allowlist bleibt unverändert.

## Runtime-Evidence

Für diesen lokalen Kandidaten lief kein neuer geschützter Master-Lifecycle. Der
frühere Lauf 31328046595 bleibt als Fehlerreproduktion erhalten: Beide
Profiljobs stoppten vor Candidate-Admission, sudo, NGINX-Start,
Evidence-Projektion und Cleanup. Ein frischer Hosted-Lifecycle ist erst
erforderlich, nachdem dieser separate Parent-Broker-PR seine Exact-Head-Gates
erfüllt und normal gemergt wurde.

## Bekannte Einschränkungen

Das verfügbare lokale Python ist CPython 3.14.4; .python-version verlangt
CPython 3.14.6. Das lokale Ergebnis ist daher Source-/Static-Validierung und
keine CI-äquivalente Interpreter-Evidence. Lokale Tests beweisen weder GitHub
Actions Context-Enforcement noch tatsächliches Runner sudo, vollständige
NGINX-Ausführung, CRS-Netzwerk-Fetch, Audit-Evidence, Artefakttransport oder
Cleanup-Verhalten.

## Verbleibende Risiken

Jeder Fehler des Parent-Broker-PRs, jedes Review-Finding, jeder
Branch-Protection-Fehler, jedes CodeQL-/SonarQube-Cloud-Finding oder ein
resultierender Master-Lifecycle-Fehler blockiert Phase C und die Fortsetzung
von PR #240. Dieser Record autorisiert weder bewegliche Refs noch direkte
Master-Änderungen, einen Bypass, einen System-Fallback, eine Root-Shell oder
einen synthetischen Runtime-PASS.

## Nicht ausgeführte Prüfungen mit Begründung

Der geschützte No-CRS-/With-CRS-Runtime-Lauf, Root-Admission,
Worker-Verifikation, CRS-/Audit-Nachweis, Evidence-Readback und Cleanup werden
absichtlich nicht lokal ausgeführt: Sie benötigen den resultierenden
geschützten Parent-master-Workflow und einen vertrauenswürdigen
GitHub-Hosted-Runner. make test-no-crs, make test-with-crs und breitere
Runtime-Targets sind deshalb für den späteren verpflichtenden Hosted-Lifecycle
deferiert. Der direkte Target check-runtime-producer-readiness wurde wie oben
erfasst versucht und blockiert; für die anwendbaren lokalen Vertragschecks ist
keine Framework- oder MRTS-Remote-Operation erforderlich.

## Finaler Review-Status

Der Kandidat bleibt lokal, bis eine Exact-Head-PR-Validierung und Review-Runde
abgeschlossen ist; aus diesen lokalen Checks wird keine Delivery-Schlussfolgerung
abgeleitet.

## Finaler Diff- und Review-Status

Dies ist ein uncommitteter Phase-B-Kandidat im task-eigenen externen Worktree
auf fix/ci-nginx-broker-runtime-snapshot, basierend auf
ef88a616498e0a2893cd3da54003dd7cdea57015. Der finale Diff enthält nur die
aufgeführten Parent-Workflow-/Producer-/Broker-/Test-/Dokumentationsdateien
und den einen Framework-Gitlink. Ein unabhängiges fokussiertes Security-Review
fand keine reportbare Trust-Boundary-Regression. Dieser Record behauptet keinen
Commit, Push, Pull Request, Hosted Check, Merge oder Phase-C-Runtime-Ergebnis.
