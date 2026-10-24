# Change Record: CR-20261009-nginx-sequence-prefix-publication-barrier

**Sprache:** [English](CR-20261009-nginx-sequence-prefix-publication-barrier.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261009-nginx-sequence-prefix-publication-barrier |
| Datum (UTC) | 2026-10-09 |
| Basis-Revision | `fabc2b7b436cf1fe276a4fc681e8edc1221145b7` |
| Framework-Revision | `4c6c21e8622840b4c218d8ea5520dd0b10b3fac9` |
| MRTS-Revision | `8a6bb546c4c81d8ffc7be801dceac60c6925685f` |

## Motivation und Problemstellung

Der echte R12-Full97-Lifecycle erreichte realen Root-Master-/nobody-Worker-Traffic, stoppte aber bei `keepalive_after_strict_new_connection` vor dessen zweitem Request. Die Parent-Fixture schrieb die ersten HTTP-Header und das Prefix durch einen ungepufferten `SocketWriter`, setzte `prefix_sent` jedoch erst nach `flush()`. Der Client konnte deshalb zuerst gültige Header beobachten und sie fälschlich als `client headers preceded the upstream prefix` ablehnen.

## Akzeptanzkriterien

Das Publication-Event muss gesetzt sein, bevor der erste Header-/Prefix-Write für den Client sichtbar werden kann. Ein Fehler beim ersten Write oder Flush muss das Event löschen und die Marker-Barrier überspringen. Suffix-Fehler, Barrier-Timeout, Callbacks vor der Publication und Follow-up-Requests müssen ihr bestehendes Fail-Closed-Verhalten behalten. Framework-Validatoren, Required-Auswahl, Produktquellen, Root/nobody-Kontrollen und MRTS bleiben unverändert.

## Implementierungsentscheidung und Begründung

Für Late-Response-Fixtures aktiviert der Parent-Upstream `prefix_sent` unmittelbar vor dem ungepufferten ersten Write. Er löscht das Event, wenn dieser Write oder sein Flush fehlschlägt, und ruft `send_marker()` erst nach erfolgreichem Abschluss beider Schritte auf. Marker-Write-Fehler behalten das erfolgreich veröffentlichte Prefix bei und lassen `marker_sent=false`. Dadurch entsteht die erforderliche Happens-before-Beziehung ohne Warten im Client, das während des absichtlich großen Backpressure-Prefixes innerhalb von `sendall()` deadlocken könnte.

## Geänderte Dateien

- `ci/runtime/lifecycle/nginx_sequence_upstream.py`
- `tests/test_nginx_sequence_upstream_barrier.py`
- `reports/audits/change-records/CR-20261009-nginx-sequence-prefix-publication-barrier.md`
- `reports/audits/change-records/CR-20261009-nginx-sequence-prefix-publication-barrier.de.md`

## Ausgeführte Befehle

Die Befehle liefen über RTK. Parent-Befehle liefen aus dem Parent-Worktree; der unveränderte Framework-Validator-Befehl lief aus dem exakten Framework-Worktree:

```sh
rtk run -- env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_nginx_sequence_upstream_barrier.py -v
rtk run -- env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_nginx_sequence_*py' -v
rtk run -- env PYTHONDONTWRITEBYTECODE=1 FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/framework-nginx-seven-contracts-20261008 python3 -m unittest -v tests.test_nginx_dispatch_routes tests.test_nginx_driver_contract_tables tests.test_nginx_begin_driver_evidence tests.test_nginx_sequence_client tests.test_nginx_sequence_driver tests.test_nginx_sequence_driver_phases tests.test_nginx_sequence_transport tests.test_nginx_sequence_upstream_barrier
rtk run -- env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.no_crs.test_nginx_lifecycle_sequence
rtk run -- env PYTHONDONTWRITEBYTECODE=1 python3 -c 'from pathlib import Path; [compile(Path(name).read_bytes(), name, "exec") for name in ("ci/runtime/lifecycle/nginx_sequence_upstream.py", "tests/test_nginx_sequence_upstream_barrier.py")]'
rtk run -- shellcheck ci/runtime/lifecycle/run-no-crs-baseline.sh
rtk run -- python3 ci/tools/new-change-record.py check
rtk make check-bilingual-docs PYTHON=python3
rtk make check-doc-links PYTHON=python3 FRAMEWORK_ROOT=modules/ModSecurity-test-Framework
rtk run -- env BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/validation/r12-sequence-race-lint PYTHON=/root/git/ModSecurity-conector/.venv/bin/python FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/framework-nginx-seven-contracts-20261008 FRAMEWORK_PYTHON=/var/tmp/codex/ModSecurity-test-Framework/venv/bin/python APACHE_C_STANDARDS_OUT=/var/tmp/codex/ModSecurity-conector/validation/r12-sequence-race-lint/apache-c-standards make lint
rtk git diff --check
```

Das maßgebliche fokussierte RED führte zehn Tests aus und erzeugte genau zwei Fehler in den Kontrollen für Callback während Write und Callback während Flush. Nach der Source-Korrektur bestand die erweiterte Sequence-Suite 51/51 Tests. Die Parent-Vertragssuite mit explizitem Framework-Root bestand 64/64, und der unveränderte strikte Sequence-Validator des Frameworks bestand 18/18. Python-Kompilierung, ShellCheck des tatsächlichen Shell-Wrappers, Change-Record-Struktur, bilinguale Dokumentation, Linkprüfung und `git diff --check` bestanden. Das vollständige Parent-`make lint` endete mit Exit 0, nachdem alle Ausgabe-Roots als Umgebungsvariablen unter `/var/tmp/codex` gesetzt waren.

Drei Nicht-Source-Aufrufe bleiben erhalten und werden nicht umetikettiert: Die Parent-venv besitzt kein `pytest`; ShellCheck gegen den Python-Driver lieferte `SC1071`; und zwei frühe Lint-Versuche verwendeten zuerst einen gesperrten Legacy-Ausgabe-Root und dann `BUILD_ROOT` auf der Make-Kommandozeile, dessen `MAKEFLAGS`-Vererbung synthetische Tests an der Wahl ihrer privaten Roots hinderte. Die korrigierten repository-eigenen Aufrufe oben bestanden alle ohne Source-Workaround.

## Security-Auswirkung

Keine Sicherheitsprüfung wird gelockert. Frühe Callbacks werden weiterhin abgelehnt, wenn nicht exakt diese Upstream-Publication aktiviert wurde; ein Fehler der ersten Ausgabe löscht diese Autorität und bleibt als `upstream_write_failed` erhalten. Pfadautorität, Projection-Freshness, Root/nobody-Isolation, Evidence-Validierung und Required-Scope bleiben unverändert. Es werden keine Secrets gespeichert.

## Runtime-Evidence

R12 bleibt ein unveränderlicher terminaler FAIL: Supervisor-Exit 2, nativer Make-Exit 2 und kein Canonical `result.json`. Seine inneren und äußeren SHA256-Ledger validieren unter echtem Root erneut; der fehlgeschlagene Case protokolliert Root-Master- und nobody-Worker-Identitäten sowie erfolgreiches Cleanup, und kein Host-nginx verbleibt. Unit-Tests etikettieren R12 nicht um und belegen keinen korrigierten Full97-PASS.

## Bekannte Einschränkungen

Das Fixture-Event bezeichnet, dass die Publication unmittelbar vor dem ungepufferten Write aktiviert wurde; erfolgreiche finale Evidence erfordert weiterhin das Ausbleiben eines Write-Fehlers und echte Client-/Native-Beobachtungen. Dieser Change Record behauptet keinen korrigierten Exact-Head-Full97-Lauf.

## Verbleibende Risiken

Ein frischer source-gebundener Root-Master-/nobody-Worker-Lifecycle ist weiterhin erforderlich, um das korrigierte Interleaving mit NGINX 1.31.6 zu beweisen und ein Canonical-Ergebnis zu erzeugen. Bestehende R12-Evidence kann diese Anforderung nicht erfüllen.

## Nicht ausgeführte Prüfungen mit Begründung

Ein frischer Post-Fix-Build, der Full97-Lifecycle, der geschützte Workflow und Remote-CI/Sonar des aktuellen Heads sind nicht gelaufen. Der Abschluss ist bewusst auf den belegten Parent-Race begrenzt; es wird keine unabhängige Defektarbeit eröffnet.

## Finaler Diff- und Review-Status

Der finale Pre-Commit-Diff ist auf eine Parent-Fixture, ihre deterministischen Regression-Kontrollen und diesen EN/DE-Record begrenzt. Framework- und MRTS-Gitlinks bleiben unverändert. Unabhängige Test-, Dokumentations- und Security-Reviews melden GO ohne Blocker, und die finale lokale Validierung ist grün. Ein separater Commit und normaler Remote-Readback bleiben erforderlich; PR #396 bleibt Draft.
