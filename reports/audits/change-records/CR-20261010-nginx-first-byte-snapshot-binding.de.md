# Change Record: CR-20261010-nginx-first-byte-snapshot-binding

**Sprache:** [English](CR-20261010-nginx-first-byte-snapshot-binding.md) | Deutsch

Gezielte Collector-Korrektur; frische Runtime-Bestätigung bleibt offen.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261010-nginx-first-byte-snapshot-binding |
| Datum (UTC) | 2026-10-10 |
| Basis-Revision | `b0d75ef6bbc33228423aef65d8ea3409387ab30f` |

## Motivation und Problemstellung

Der historische Full97 auf `dca17fd5690c2ec2b8806024d1061744db8c3ad8` hatte 80 Case-PASS, neun FAIL und acht NOT_EXECUTED. Der Host-Snapshot entstand nach Upstream-Freigabe; seine finalen Zähler wurden in jedes Phase-4-Event eingefügt.

## Akzeptanzkriterien

Zähler beim pausierten First Byte erfassen, exakte Invocation-/Event-Bytes binden, spätere Zähler erhalten und Mismatches ablehnen.

## Implementierungsentscheidung und Begründung

NGINX erfasst Host-Metadaten und Barriere-Evidence vor Upstream-Freigabe. Ein separater Metadaten-Receipt bindet originale Pause-Bytes, Log-Präfix, Event-Index/-Hash, Transaktion, Snapshot-Hash und exakte Pfade. Nur das eindeutig passende Append-Event wird ergänzt; spätere Events behalten eigene Zähler. Apache bleibt unverändert.

## Geänderte Dateien

`ci/lib/first_byte_binding.py`, `ci/runtime/lifecycle/collect-no-crs-source.py`, `ci/runtime/lifecycle/write-first-byte-host-metadata.py`, `ci/runtime/lifecycle/write-first-byte-source-results.py`, `connectors/nginx/harness/run_nginx_smoke.sh`, `tests/test_nginx_first_byte_binding.py`, this EN/DE record pair.

## Ausgeführte Befehle

`rtk proxy env PYTHONNOUSERSITE=1 /var/tmp/codex/ModSecurity-test-Framework/venv/bin/python -m unittest -v tests.test_nginx_first_byte_binding tests.test_no_crs_outcome_projection tests.test_collect_no_crs_source_helpers tests.test_collect_no_crs_source tests.test_native_first_byte_shell_environment`: 86 Tests bestanden, Exit 0. Erster B-RED-Lauf mit Exit 1 reproduzierte Erfassung nach Freigabe und fehlende Bound-Merge-API.

## Security-Auswirkung


Validatoren, Datenschutz-Allowlist, Required-Scope und Produktsemantik nicht abgeschwächt. Der Receipt speichert keinen Response-Payload. MRTS unverändert.

## Runtime-Evidence

Historischer R13 unverändert. Offline-Fixtures sind kein neuer Runtime-Lauf. Frischer echter begrenzter Fokus und integrierte SHA-Evidence liegen beim Koordinator und werden hier noch nicht behauptet.

## Bekannte Einschränkungen

Unit-Regressionen sind kein Full97- oder Protected-Exact-Head-Nachweis. Tests liefen auf der uncommitted Sourceüberlagerung der Basis-Revision, nicht als Exact-Head-Runtime. Die aufgeführten Test-Payloads wurden in `rtk proxy bash -c` mit Log-/Exit-Erfassung ausgeführt. Python-Kompilierung, Shell-Syntax, Change-Record-Struktur und `git diff --check` bestanden. ShellCheck mit `--severity=warning` meldete auf Basis und geändertem Harness dieselben sieben bestehenden Warnungen, jeweils Exit 1; keine Unterdrückung.

## Verbleibende Risiken

Frischer First-Byte-Fokus muss Pause-Reihenfolge, vollständige Safe-Response, exakte Snapshot-Zuordnung, Rollen und Cleanup prüfen. Die Receipt-Reihenfolge verwendet beobachtete Datei-Zeitstempel zusätzlich zu Hashes und exakten Pfaden.

## Nicht ausgeführte Prüfungen mit Begründung

Neuer Full97 nicht freigegeben. Protected-/Admin-Operationen außerhalb des Scopes. Vollständiger Lint, frisches CI/Sonar und Veröffentlichung werden durch diesen Worker nicht behauptet.

## Finaler Diff- und Review-Status

Gezielte Sourceänderungen für unabhängigen Review und separaten Commit vorbereitet. Dieser Worker führte keinen Commit, Push, Merge, Retarget oder Undraft aus.
