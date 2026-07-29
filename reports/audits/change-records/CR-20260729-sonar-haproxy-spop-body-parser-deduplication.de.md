# Change Record: Parent-HAProxy-SPOP-Body-Parser-Deduplizierung

**Sprache:** [English](CR-20260729-sonar-haproxy-spop-body-parser-deduplication.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260729-sonar-haproxy-spop-body-parser-deduplication |
| Datum (UTC) | 2026-07-29 |
| Basis-Revision | `9f23ae2c5fe908cef38f203be03f93fda75a8dd7` |
| Tracking | Ein aktuelles SonarQube-Cloud-CPD-Paar bei Zeilen 1214/1230: zwei 15-Zeilen-SPOP-Parser für typed Body-Argumente, gemeldet als 30 Duplikatzeilen. |
| Grenze | Parent-HAProxy-Diagnostic-SPOP-Runtime und fokussierte Test-/Change-Record-Dateien. Keine Framework-, MRTS-, Gitlink-, Workflow-, Sonar-Konfigurations-, Suppression- oder `master`-Änderung. |

## Motivation und Problemstellung

Die SPOP-Argumente `body` und `response_body` wiederholten denselben Parsing- und Owned-Byte-Copy-Pfad für nicht vertrauenswürdige typed Values. Ihr einziger beabsichtigter Unterschied ist, ob ein akzeptierter Byte-Wert den Request als Response-Body-Event markiert. Die Reduktion muss Type-Rejection/-Consumption, Parse-Position, Owned-Memory-Verhalten und Phase-Flags erhalten.

## Akzeptanzkriterien

- Ein privater Helper führt den bestehenden typed Byte-Read aus und akzeptiert nur SPOP-String- oder Binary-Werte.
- Akzeptierte Werte behalten Owned-Copy und `has_body`; nur Response-Body-Input setzt `is_response` und `is_response_body`.
- Nicht-Byte-typed-Werte bleiben konsumiert, setzen jedoch weder Body- noch Response-Flags.
- Der fokussierte C17-Harness, native GCC-/Clang-C17-Runtime-Builds und der repository-native C23-Hinweis-Check bestehen.
- Hosted Exact-Head SonarQube Cloud muss vor jeder Merge-Betrachtung null New Issues und null New-Code-Duplikation melden.

## Implementierungsentscheidung und Begründung

`parse_notify_body_argument` zentralisiert die gemeinsame Read-/Copy-Entscheidung und erhält einen expliziten Boolean für die Response-Body-Semantik. Die beiden öffentlichen Parser-Branches bleiben sichtbar und wählen nur ihre ursprüngliche Rolle. Das ist die engste repository-native Änderung: Sie entfernt das bestätigte CPD-Paar und erhält Protocol-Parsing, Ownership und Phase-Entscheidungen in derselben Source-Datei.

## Geänderte Dateien

- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` — privater gemeinsamer typed Body-Parser und zwei explizite Role-Caller.
- `tests/test_sonar_reliability_contract.py` — C17-Harness-Abdeckung für String-, Binary-, Response- und Non-Byte-Pfade.
- Dieses englisch/deutsche Change-Record-Paar und seine gepaarten Indizes.

## Ausgeführte Befehle

| Ausgeführte Kontrolle | Beobachtetes Ergebnis |
| --- | --- |
| `python3 -m unittest tests.test_sonar_reliability_contract` | bestanden: 11 Tests, einschließlich kompiliertem typed Body-Parser-Harness. |
| Native SPOA-Runtime Build und Self-Test unter GCC C17 `-Wall -Wextra -Werror` | bestanden gegen den vorhandenen temporären libmodsecurity-Prefix. |
| Native SPOA-Runtime Build und Self-Test unter Clang C17 `-Wall -Wextra -Werror` | bestanden gegen denselben temporären Prefix. |
| `make check-haproxy-common-adoption` sowie C17-Wiring-/Lint-Kontrollen | bestanden. |
| `make check-haproxy-c23` | bestanden. |
| `git diff --check` | bestanden. |

## Security-Auswirkung

Der Source-to-Sink-Pfad führt von einem peer-kontrollierten SPOP-typed-Argument in den owned `request->body`-Buffer. Der Helper erhält die bisherige strikte Type-Grenze: Nur String-/Binary-Werte erreichen `copy_bytes`; andere Typen werden vom bestehenden Typed-Data-Reader konsumiert und können Body- oder Response-State nicht verändern. Der fokussierte C17-Harness prüft beide akzeptierten Byte-Typen und die Non-Byte-Negativkontrolle sowie die Response-Flags getrennt. Keine Parser-Bounds-, Ownership-, Autorisierungs-, Protocol- oder Quality-Gate-Kontrolle wird gelockert.

## Runtime-Evidence

Die echte Diagnostic-SPOP-Binärdatei absolvierte Handshake und typed `set-var` ACK-Self-Test unter beiden Compilern. Dies beweist den ausgewählten Diagnostic-Protocol-Pfad, nicht Live-HAProxy-Production-Enforcement oder Response-Body-Phase 4, die der Target als deaktiviert meldet.

## Bekannte Einschränkungen

- Keine Live-HAProxy-plus-ModSecurity-Runtime und keine vollständige Connector-Matrix liefen, weil der version-festgeschriebene Host-Source-/Runtime-Fixture in diesem temporären Task-Worktree fehlt.
- Die vollständige Codex-Security-Diff-Scan-Fähigkeit bleibt unzugänglich, weil ihr verpflichtender Delegated-Worker-Preflight unvollständig ist; kein vollständiger Scan-Report wird behauptet.
- Hosted-Checks und frische Exact-Head-SonarQube-Cloud-Analyse stehen aus.

## Verbleibende Risiken

- Künftige typed Body-Formen müssen den Helper weiter nutzen oder einen gleichwertigen Protocol-/Ownership-Review erhalten; ein dritter akzeptierter Typ erfordert eine neue Security-Entscheidung.

## Nicht ausgeführte Prüfungen mit Begründung

Keine Live-HAProxy-Runtime, keine vollständige Connector-Matrix und kein vollständiger Codex-Security-Diff-Scan liefen. Die erforderlichen externen Host-Fixtures fehlen und die Scan-Fähigkeit kann ihren verpflichtenden Delegated Worker nicht erhalten. Typed-Parser-Harness und zwei native Compiler-/Runtime-Self-Tests sind die stärksten verfügbaren Kontrollen.

## Finaler Diff- und Review-Status

Der Kandidat ist auf Parent-HAProxy-SPOP-Parsing und bilinguale Traceability begrenzt. Er entfernt das einzige bestätigte 30-Zeilen-CPD-Paar und erhält die Request-/Response-Role-Trennung. Lokaler Review ist abgeschlossen; ein separater Draft-PR und Exact-Head-Hosted-Verifikation bleiben vor jeder Delivery- oder Merge-Behauptung erforderlich.
