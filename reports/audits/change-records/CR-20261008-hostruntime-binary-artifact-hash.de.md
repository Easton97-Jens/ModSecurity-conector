# Change Record: CR-20261008-hostruntime-binary-artifact-hash

**Sprache:** [English](CR-20261008-hostruntime-binary-artifact-hash.md) | Deutsch


## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-hostruntime-binary-artifact-hash |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `810a9b5621b04c79d58b1429c3182f1668e672c9` |

## Motivation und Problemstellung

Der native Lifecycle scheiterte nach der Canonical-Finalisierung, weil `artifact_sha256()` ein gespeichertes Configtest-ELF als UTF-8 dekodierte. Aufrufer ist `run-no-crs-baseline.sh`; die Operation benötigt Byte-Hashing, keine Textanalyse.

## Akzeptanzkriterien

Der echte Writer akzeptiert Nicht-UTF-8-Artefakte mit exakten Byte-Digests. Geänderte/fehlende Artefakte, ungültiges JSON und unsichere Pfade/Typen bleiben ohne erfolgreiche Ausgabe abgewiesen.

## Implementierungsentscheidung und Begründung

Originalbytes in 1-MiB-Blöcken über die vorhandenen validierten Pfad-, Parent-Descriptor-, `O_NOFOLLOW`- und Regular-File-Prüfungen hashen. JSON-Dekodierung und Manifest-Digestvergleich unverändert lassen. Dadurch bleiben auch CRLF-Bytes statt normalisierter Zeilenenden erhalten.

## Geänderte Dateien

`ci/runtime/lifecycle/write-hostruntime-record.py`, `tests/test_hostruntime_record.py` und dieses EN/DE-Change-Record-Paar. Keine Framework-/MRTS-, Gitlink-, Dependency- oder Protocol-Änderungen.

## Ausgeführte Befehle

`rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_hostruntime_record tests.test_runtime_path_utils`: Coordinator-VM-Host-Lauf, 33 Tests PASS, 0 SKIP, Exit 0. Die erweiterte Suite enthält zusätzlich `tests.test_runtime_artifact_utils tests.test_runtime_path_security tests.test_runtime_path_policy`: 82 Tests PASS, 0 SKIP, Exit 0. Dynamische Einstiegsregression am alten Code: 1 Test scheitert an der Unicode-Dekodierung, Exit 1. Neue Fälle prüfen Binär-/CRLF-/Mehrblock-Digests, Byteänderungen, fehlende Artefakte und JSON-Format. `git diff --check` bestanden.

## Security-Auswirkung

Vorhandene Containment-, Verzeichnisautoritäts-, Descriptor-, No-Follow-, Regular-File-, Manifest-Digest- und Veröffentlichungs-Preflight-Kontrollen bleiben erhalten. Streaming begrenzt Arbeitsspeicher, nicht die Gesamtdateigröße. Der alte Reader besaß keine unabhängige Leaf-Owner-/Hardlink- oder Inode-/mtime-Attestierung; eine solche Garantie wird nicht erfunden.

## Runtime-Evidence

Isolierter Writer-Repro mit historischen Artefakten, KEIN frischer E2E: echte NGINX-/Modul-/Library-Digests geprüft; Writer Exit 0; Manipulations-/Missing-Kontrollen Exit 2 ohne Record/Summary. Quell-Ergebnis/Manifest unverändert und kopierter Nicht-PASS-Status nicht hochgestuft. Receipt: `/var/tmp/codex/ModSecurity-conector/analysis/nginx1316-followup-20261008T003355Z/writer-real-repro/writer-repro-receipt.json`.

## Bekannte Einschränkungen

Nur Artefakt-Hashing ändert sich. Dies repariert weder H1-Standardweitergabe noch das Scheduling fehlender Required-Szenarien und erzeugt keine Allow-Events.

## Verbleibende Risiken

Vollständige Canonical-Coverage und unabhängiger Protected-Vertrauensnachweis bleiben getrennte Pflichten. Die vorhandene Gesamtdateigrößen-Policy ist unverändert.

## Nicht ausgeführte Prüfungen mit Begründung

Frischer lokaler Standard-E2E, vollständiger Lint und CI/Sonar am aktuellen Head folgen den separaten H1-/Testfixes. Ruff fehlt im Parent-Environment; keine Paketinstallation versucht.

## Finaler Diff- und Review-Status

Source-/Test-Diff mit zwei Dateien und unabhängigem statischem Security-Review geprüft. Keine unsicheren Dekodierungsfallbacks, Suppressionen, synthetische Runtime-Evidence oder fremden Änderungen. Atomarer Folgecommit vorgesehen; kein Merge, Force-Push oder Protected-Dispatch.
