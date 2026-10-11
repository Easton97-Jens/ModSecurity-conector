# Change Record: CR-20261011-pr406-i09-i11-conflict-resolution

**Sprache:** [English](CR-20261011-pr406-i09-i11-conflict-resolution.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261011-pr406-i09-i11-conflict-resolution |
| Datum (UTC) | 2026-10-11 |
| Basis-Revision | `6a79efe7d571d9fc980f970a08073d6334c36a7a` |

## Motivation und Problemstellung

PR #406 hatte nach dem I09-Abgleich nativer API-/Fehlerrouten Konflikte mit seiner gestapelten PR-#382-Basis. Die reine Auswahl eines Branches würde I09-First-error-Prüfungen oder geprüfte physische I11-Sink-Weitergabe verwerfen. Der veröffentlichte User-Merge `6a79efe7d571d9fc980f970a08073d6334c36a7a` bleibt erhalten; Basis `492663334d89428dce084792145ef94e91579788` wird mit einem normalen Merge-Commit integriert.

## Akzeptanzkriterien

Alle fünf Merge-Konflikte sind gelöst; Apache verhindert erfolgreiche Reentry nach Contract- oder Sinkfehler; SPOP führt neue technische Fehlerereignisse durch geprüfte Serializer und physische Sinks, erhält die native erste Ursache und unterdrückt ACK/Wiederholung nach zwingendem Sinkfehler. Bestehende Bool-Serializer-Aufrufer behalten ihren Vertrag. Dokumentpaare erhalten historische Belege und offene Host-Akzeptanz. Frische lokale Validierung und unabhängiger Review gehen normaler Task-Branch-Delivery voraus; GitHub-/Sonar-Prüfungen des aktuellen Heads werden nach Push getrennt verifiziert.

## Implementierungsentscheidung und Begründung

Apache-Guards mit OR kombinieren, typisierte Writer-Rückgaben und unbeobachtetes I09-`actual_action=""` erhalten. Technische SPOP-Records vor physischer I/O stagen, erfolgreiche Auslassung mit additiven checked APIs von Serialisierungsfehlern unterscheiden und Bool-Wrapper erhalten. Gelockte First-error-Latch über Bridge-Tasks und Cleanup bewahren. Für native Request-only-Finishfehler einen geprüften Event-Write nach Finish wiederherstellen: vorgezogenes initiales Logging hätte sonst den neuen terminalen I09-Producer ausgelassen. Kleinen Bridge-Flush-Helper ohne Änderung der Lock-Ownership extrahieren. Common für Envoy frisch bauen, statt ein gegen das vorherige Strukturlayout kompiliertes Archiv zu linken.

## Geänderte Dateien

Manuelle Auflösungen/Anpassungen: `connectors/apache/src/msc_filters.c`; Apache-Adoptionschecker/-test und `tests/test_apache_i09_filter_events.py`; `connectors/haproxy/src/haproxy_modsecurity_binding.c`, dessen Header und SPOP-Runtime; native/Host-/Sink-/Timeout-Fixtures von HAProxy; EN/DE-Checkliste, Restmatrix und historischer I09-Audit; dieses Record-Paar. Der Merge übernimmt außerdem I09-Basisänderungen und deren [I09-Record](CR-20261011-i09-native-route-reconciliation.de.md). Frühere I11-Implementierung bleibt durch den [I11-Record](CR-20261011-pr382-i11-physical-sink-parity.de.md) nachvollziehbar. Keine Framework-/MRTS- oder Gitlink-Änderungen.

## Ausgeführte Befehle

Jeder folgende Befehl lief tatsächlich im Integrations-Checkout. Der erste integrierte Lauf mit 68 Tests und der breite Lauf mit 215 Tests lagen vor der abschließenden Request-Finish-Korrektur; die `-final`-Läufe prüfen den endgültigen Quellstand. Counts überlappen und sind keine Summe eindeutiger Tests.

Abschließende lokale Ergebnisse: integriert 70 Tests; breit HAProxy 217 Tests mit zwölf dokumentierten Skips; fokussiert HAProxy 43 und ASan/UBSan 26 Tests; Runtime-Sink acht Tests; Apache-C17/Adoption 20 Tests; frischer nativer Envoy-Build/Tests über acht Pakete und Native-Race 142 Top-level-Tests/228 Cases/drei Pakete. Common-C17/SDK/Security/Flow/Memory, 26 Python-Syntax-/sechs Go-Formatdateien, Workflow-Lint, Bilingual-/Pfad-/Link- und Change-Record-Strukturprüfungen bestanden.

| Exact command / Exakter Befehl | Exit | Receipt / Beleg |
| --- | --- | --- |
| `rtk proxy env CI=true MODSECURITY_INCLUDE_DIR=/usr/include APACHE_C_STANDARDS_OUT=/var/tmp/codex/ModSecurity-conector/runs/i11-conflict-apache-c17 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-apache-c17 check-apache-common-adoption` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-conflicts/apache-c17-adoption.json` |
| `rtk proxy python3 ci/tools/new-change-record.py check` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-conflicts/change-record-structure.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python /var/tmp/codex/ModSecurity-conector/analysis/i11-conflicts/verify_changed_source.py` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-conflicts/changed-source-format.json` |
| `rtk proxy env BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/runs/i11-conflict-common TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-common-helpers-c17 check-common-sdk-contract check-common-security-contract check-common-flow-integrity check-common-memory-safety` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-conflicts/common-native-contracts.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-bilingual-docs check-doc-links` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-conflicts/docs-acceptance.json` |
| `rtk proxy env BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/runs/i11-conflict-envoy-native-build MODSECURITY_INCLUDE_DIR=/usr/include MODSECURITY_LIB_DIR=/usr/lib/x86_64-linux-gnu ENVOY_EXT_PROC_COMMON_TEST=1 GOFLAGS=-p=1 GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off GOMODCACHE=/var/tmp/codex/ModSecurity-conector/cache/i11-gomodcache GOCACHE=/var/tmp/codex/ModSecurity-conector/cache/i09-go GOTMPDIR=/var/tmp/codex/ModSecurity-conector/tmp TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp sh connectors/envoy/build/build_ext_proc.sh` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-conflicts/envoy-native-build.json` |
| `rtk proxy env CGO_ENABLED=1 'CGO_CFLAGS=-D_DEFAULT_SOURCE -std=c17 -I/var/tmp/codex/ModSecurity-conector/worktrees/i11-sink-parity -I/var/tmp/codex/ModSecurity-conector/worktrees/i11-sink-parity/common/include -I/var/tmp/codex/ModSecurity-conector/worktrees/i11-sink-parity/common/runtime -I/usr/include' 'CGO_LDFLAGS=/var/tmp/codex/ModSecurity-conector/runs/i11-conflict-envoy-native-build/envoy-ext-proc/libmsconnector_envoy_ext_proc_common.a -L/usr/lib/x86_64-linux-gnu -lmodsecurity -Wl,-rpath,/usr/lib/x86_64-linux-gnu -lstdc++ -pthread' GOFLAGS=-p=1 GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off GOMODCACHE=/var/tmp/codex/ModSecurity-conector/cache/i11-gomodcache GOCACHE=/var/tmp/codex/ModSecurity-conector/cache/i09-go GOTMPDIR=/var/tmp/codex/ModSecurity-conector/tmp TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp go test -mod=readonly -count=1 -race -tags libmodsecurity -json -p=1 ./internal/processor ./internal/responseobserver ./internal/composite` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-conflicts/envoy-native-race.json` |
| `rtk proxy env TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest discover -s tests -p 'test_haproxy*.py' -v` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-conflicts/haproxy-broad-final.json` |
| `rtk proxy env TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest discover -s tests -p 'test_haproxy*.py' -v` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-conflicts/haproxy-broad.json` |
| `rtk proxy env TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-i09-native-routes check-apache-event-sink check-haproxy-spop-event-sink` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-conflicts/i09-i11-integrated-final.json` |
| `rtk proxy env TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-i09-native-routes check-apache-event-sink check-haproxy-spop-event-sink` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-conflicts/i09-i11-integrated.json` |
| `rtk proxy env TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_runtime_event_sink_failures` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-conflicts/runtime-event-sink.json` |
| `rtk proxy /root/go/bin/actionlint .github/workflows/lint.yml .github/workflows/test-apache.yml .github/workflows/test-haproxy.yml` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-conflicts/workflow-lint.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_haproxy_spop_event_sink_failures tests.test_haproxy_native_results tests.test_haproxy_host_native_results tests.test_haproxy_common_adoption tests.test_haproxy_spop_response_timeout_contract` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-review/haproxy-i09-i11-request-finish-focused.json` |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/tmp 'CC=clang -fsanitize=address,undefined -fno-omit-frame-pointer' /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_haproxy_spop_event_sink_failures tests.test_haproxy_native_results tests.test_haproxy_host_native_results` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-review/haproxy-i09-i11-request-finish-sanitizers.json` |
| `rtk proxy cc -std=c17 -Wall -Wextra -Werror -pthread -I common/include -I connectors/haproxy/src -fsyntax-only connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` | 0 | `/var/tmp/codex/ModSecurity-conector/analysis/i11-review/haproxy-i09-i11-request-finish-syntax.json` |

## Security-Auswirkung

Fehlerklassifikation und First-cause-Erhalt bewahren; keine Tests, Compilerwarnungen, CI, Isolation oder Quality Gates abschwächen. Neue technische Ereignisse können auf den geprüften Request-/Response-/Bridge-Pfaden nicht still den checked Sink umgehen. Bestehende unbeobachtete Hostaktionen bleiben leer. Keine Credentials oder rohen Request-/Bodydaten zu Belegen hinzufügen.

## Runtime-Evidence

Es wurde keine Runtime-Evidence erhoben oder beansprucht. Kompilierte Fixtures produktiver Funktionen prüfen kontrollierte echte Dateideskriptor-Write-/Flushfehler, Zustandserhalt, Cleanup und ACK-Unterdrückung. Das sind begrenzte lokale Tests, kein Live-HAProxy-/Apache-/Envoy-Host- oder clientseitig sichtbarer Transportnachweis.

## Bekannte Einschränkungen

Die breite HAProxy-Suite überspringt zwölf Fälle: elf Cross-identity-Staging-Fixtures benötigen gemappte Identitäten/setpriv, einer benötigt eine ausdrücklich gebaute SPOP-Runtime und registrierte temporäre Wurzel. Vollständige HTX-Host-Header-Kompilierung und Live-Host-/Companion-Validierung am exakten Stand erfolgten nicht. I10, I12 und V08–V10 bleiben offen. Historisches lokales I09-Sonar-403 beschreibt nicht die Cloud-Analyse des aktuellen Heads.

## Verbleibende Risiken

Der unabhängige Review vermerkte einen übernommenen Common-Typed-CANCEL-Pfad mit void-fail-Callback: Ownership-Freigabequittierung und Meldung zwingender Sinkfehler bleiben getrennte API-Semantik. Sein Wire-Verhalten wurde nicht geprüft; dieser Merge ändert den bestehenden Common-Callback-Vertrag nicht. Lokale Ergebnisse begründen keine vollständige Live-Host- oder Release-Akzeptanz.

## Nicht ausgeführte Prüfungen mit Begründung

Für diese Konfliktauflösung liefen keine Live-Host-Matrix, H2/H3, CRS/Off, Deployments oder Client-Transportexperimente. Keine Pakete, Toolchains oder Systemdienste wurden verändert. CI und Sonar des aktuellen Heads benötigen die gepushte SHA und werden in PR #406 sowie externen Delivery-Belegen festgehalten, nicht aus ursprünglichen I11-/I09-Heads abgeleitet.

## Finaler Diff- und Review-Status

Die begrenzte Auflösung wurde unabhängig gegen beide Elternstände geprüft. Der Review identifizierte die Request-Finish-Producer-Lücke; geprüfter Write und kompilierte Positiv-/Fehlerkontrollen schließen diese Merge-Regression. Die kontrollierte kompilierte Red-Variante ohne den Write erzeugt null terminale Ereignisse, der aktuelle Helper eines. Abschließende Staging-Prüfungen müssen fehlende unmerged Indexeinträge, Konfliktmarker, Whitespacefehler, fremde Dateien und lokale Artefakte bestätigen; Delivery nutzt normalen Merge-Commit und Task-Branch-Push ohne PR-Merge oder History-Rewrite.
