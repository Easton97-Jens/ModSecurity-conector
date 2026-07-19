# Change Record: Runtime-Pfad-Containment-Härtung

**Sprache:** [English](CR-20260718-runtime-path-confinement.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260718-runtime-path-confinement` |
| Datum (UTC) | `2026-07-18` |
| Basis-Revision | `c8ca0d92b630c18232b881855c4f5d1482568ea6` |
| Finding | `FND-PARENT-0026` |
| Grenze | Nur Parent-Runtime-Pfad-Policy und Lifecycle-Resolver; Framework und MRTS unverändert. |

## Motivation und Problemstellung

`REPO_ROOT`, `CONNECTOR_ROOT` und `FRAMEWORK_ROOT` wurden vom Parent-
Runtime-Pfad-Helper als beschreibbare Projektanker behandelt. Ihre Belegung mit
`/` konnte deshalb `/etc/evidence-escape` und `/root/evidence-escape`
autorisieren. Der Lifecycle-Resolver akzeptierte außerdem schmal wirkende
Bases unter systemeigenen Orten und löste Symlinks nach `/root` ohne
Containment-Prüfung gegen einen Invocation-Root auf. Der Readiness-Report
wiederholte die Ausnahme für veränderliche Projekt-Roots.

## Akzeptanzkriterien

- Veränderliche Projekt-Root-Werte können keine Systempfade autorisieren und
  die Runtime-Allowlist nicht erweitern.
- Breite, systemeigene, Traversal- und Symlink-aufgelöste Lifecycle-Bases
  werden abgewiesen.
- Jede der fünf beschreibbaren Lifecycle-Bases bleibt innerhalb eines
  validierten, kanonischen Invocation-Roots.
- Der Resolver zeichnet diesen Invocation-Root in seiner strukturierten
  Ausgabe auf.
- Kanonische Checkout- und `/src`-Pfade bleiben nur als schreibgeschützte
  Quellpfade verfügbar; sie sind keine beschreibbaren Runtime-Roots.
- Bestehende schmale externe Konfiguration, einschließlich
  `MATRIX_ROOT=/var/tmp/codex/ModSecurity-conector/matrix`, bleibt unterstützt.

## Implementierungsentscheidung und Begründung

Der Parent-Helper leitet Repository-Quell-Roots nun aus seiner eigenen
kanonischen Modulposition ab und ignoriert veränderliche Projekt-Root-
Environmentwerte für Schreibautorisierung. Er weist breite, System-, `/root`-
und Quell-Roots für Runtime-Schreibvorgänge ab und erkennt kanonische
Quellpfade separat als schreibgeschützt.

`resolve-runtime-paths.py` verlangt `--invocation-root`, validiert ihn als
schmalen externen Root und prüft, dass Evidence-, Build-, Raw-Run-, Log- und
Cache-Bases alle Nachfahren sind, bevor Shell-Assignments ausgegeben werden.
Der Parent-No-CRS-Lifecycle-Caller übergibt
`CANONICAL_VERIFIED_RUN_ROOT` explizit.

Die strengere Bindung an eine einzelne Invocation wird absichtlich beim
kanonischen Lifecycle-Resolver angewendet, statt jeden bestehenden
konfigurierbaren Runtime-Root unter `VERIFIED_RUN_ROOT` zu erzwingen.
Repository-Evidence zeigt, dass
`MATRIX_ROOT=/var/tmp/codex/ModSecurity-conector/matrix` eine legitime,
schmale externe Konfiguration ist. Generische Runtime-Roots werden weiterhin
einzeln als nicht-breite, nicht-System- und nicht-Quell-Orte validiert.

Der Readiness-Reporter leitet seine akzeptierten Quell-Roots aus den bereits
validierten Defaults `VERIFIED_SOURCE_ROOT` und `SOURCE_ROOT` ab. Ein späterer
Wert aus `runtime-env.sh` wird gegen diese Roots geprüft; er kann keinen
zusätzlichen Quellort erzeugen. Dies bewahrt den dokumentierten schmalen
externen Source-Root-Kontrollfall, ohne die Ausnahme für veränderliche
Projekt-Roots wiederherzustellen.

## Geänderte Dateien

- `ci/lib/runtime_path_utils.py`
- `ci/runtime/common/resolve-runtime-paths.py`
- `ci/runtime/lifecycle/run-no-crs-baseline.sh`
- `ci/checks/evidence/check-runtime-producer-readiness.py`
- `ci/checks/security/check-runtime-path-policy.py`
- `tests/test_runtime_path_policy.py`
- `tests/test_resolve_runtime_paths.py`
- `tests/test_runtime_producer_readiness_path_policy.py`
- `reports/audits/change-records/CR-20260718-runtime-path-confinement.md`
- `reports/audits/change-records/CR-20260718-runtime-path-confinement.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| `rtk env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_runtime_path_policy.RuntimePathPolicyTest.test_mutable_project_roots_cannot_authorize_system_runtime_paths tests.test_runtime_path_policy.RuntimePathPolicyTest.test_broad_runner_parent_cannot_expand_runtime_allowlist tests.test_resolve_runtime_paths.ResolveRuntimePathsTest.test_rejects_broad_system_and_symlink_base_escapes` | vor dem Fix erwartungsgemäß fehlgeschlagen: veränderliche `/`-Projekt-Roots, breites `RUNNER_TEMP`, System-Bases und ein nach `/root` aufgelöster Symlink wurden akzeptiert. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_runtime_producer_readiness_path_policy` | vor dem Readiness-Report-Fix erwartungsgemäß fehlgeschlagen: `connector_root=/` autorisierte `/etc/evidence-escape`. |
| Fokussierte 13-Test-Parent-`unittest`-Auswahl für `tests.test_runtime_producer_readiness_path_policy`, `tests.test_resolve_runtime_paths` und die neuen Runtime-Path-Policy-Tests | nach dem Fix bestanden. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_runtime_producer_readiness_path_policy tests.test_runtime_path_policy.RuntimePathPolicyTest.test_mutable_project_roots_cannot_authorize_system_runtime_paths tests.test_runtime_path_policy.RuntimePathPolicyTest.test_broad_runner_parent_cannot_expand_runtime_allowlist tests.test_runtime_path_policy.RuntimePathPolicyTest.test_verified_runtime_paths_reject_broad_or_system_writable_roots tests.test_runtime_path_policy.RuntimePathPolicyTest.test_python_path_policy_selftest_accepts_only_writable_run_paths tests.test_resolve_runtime_paths` | bestanden: 16 fokussierte Tests. Die neue Kontrolle akzeptiert einen kanonischen schmalen externen Source-Root; ein System-Override und ein anderer sicherer Sibling bleiben blockiert. |
| `rtk make check-runtime-producer-readiness` | erwartetes `BLOCKED`, weil erforderliche NGINX-, Apache- und HAProxy-Komponenten sowie Caches fehlen; jeder gemeldete Runtime-Pfad, einschließlich `SOURCE_ROOT=/var/tmp/codex/ModSecurity-conector/source`, bestand die Containment-Prüfung. |
| `rtk env TMPDIR=<task-owned-temp-root> PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_bilingual_docs` | bestanden: 11 Tests des Bilingual-Dokumentationscheckers. |
| `rtk sh -n ci/runtime/lifecycle/run-no-crs-baseline.sh` und `rtk git diff --check` | bestanden. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_runtime_path_policy` | durch den isolierten Worktree blockiert: `modules/ModSecurity-test-Framework/ci/lib/common.sh` fehlt, daher kann die bestehende Shell-Hälfte des Checkers nicht laufen. Der reine Python-Selbsttest bestand. |

## Security-Auswirkung

Die korrigierte Grenze verhindert, dass Environment-gesteuerte Projekt-Roots,
breite temporäre Parents, System-Root-Nachfahren und Symlink-Escapes als
beschreibbare Runtime-Evidence-Orte behandelt werden. Eine strukturierte
Resolver-Ausgabe enthält nun den gewählten Invocation-Root und ein
Readiness-Report akzeptiert keinen Caller-bereitgestellten Projekt-Root mehr
als Schreibausnahme.
Er kann seine falsche Ablehnung eines kanonischen schmalen Source-Roots auch
nicht in einen Grund verwandeln, die Runtime-Readiness zu umgehen: Nur
kanonisch validierte Source-Roots werden akzeptiert, während spätere Overrides
fail-closed bleiben.

## Runtime-Evidence

Nicht anwendbar. Die Validierung besteht aus seiteneffektfreier Path-Policy-
und Resolver-Coverage; kein Connector-Host, Traffic-, CRS-, MRTS- oder
Protokoll-Runtime-Run wurde gestartet oder behauptet.

## Bekannte Einschränkungen

Der bestehende vollständige Shell-Policy-Selbsttest kann in diesem isolierten
Worktree nicht laufen, bis der separate Framework-Checkout am aufgezeichneten
Pfad verfügbar ist. Dies autorisiert keine Framework-Änderung. Bei Erstellung
dieses Records hatte der ursprüngliche Draft-PR-#58-Head
`4f028f911807def8b771faaa3b16c58a513e0385` 33 bestandene GitHub-Checks,
einschließlich CodeQL und SonarQube Cloud. Dieses historische Ergebnis trägt
keinen späteren Push: Jede Auslieferungsentscheidung muss die CI-, Quality- und
Review-Nachweise des dann aktuellen exakten PR-Heads verwenden.

## Verbleibende Risiken

Die Policy validiert Pfadidentität und Containment; sie beweist keine
Host-Dateisystemberechtigungen und etabliert keine Runtime-Host-Evidence. Ein
separat konfigurierter schmaler externer Root bleibt eine
Konfigurationsgrenze, während der kanonische Lifecycle-Resolver die strengere
Invocation-Root-Bindung behält.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Connector-Build, Host-Runtime-, Protokoll-Run, CRS/MRTS-Matrix- oder
Framework-Change lief in dieser Remediation. Ein geschützter Merge muss einen
explizit autorisierten, dann aktuellen PR-Head und dessen eigene Exact-Head-
CI-, CodeQL-, SonarQube-Cloud- und Review-Nachweise verwenden. Bei Erstellung
dieses Records hatte kein Merge stattgefunden.

## Finaler Diff- und Review-Status

Bei Erstellung dieses Records bestanden fokussierte lokale
Regression-Coverage, der 11-Test-Bilingual-Checker, Shell-Syntax und finale
Whitespace-Diff-Validierung. Der vollständige Shell-Policy-Check bleibt nur
durch den fehlenden Framework-Checkout blockiert. Dieser Record behauptet
bewusst keinen späteren PR-Auslieferungs- oder Merge-Status; dieser muss aus
dem aktuellen exakten Head ermittelt werden. Bei Erstellung dieses Records
hatte kein Merge stattgefunden.
