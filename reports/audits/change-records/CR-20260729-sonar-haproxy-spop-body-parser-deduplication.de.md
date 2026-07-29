# Change Record: Parent-HAProxy-SPOP-Body-Parser-Deduplizierung

**Sprache:** [English](CR-20260729-sonar-haproxy-spop-body-parser-deduplication.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260729-sonar-haproxy-spop-body-parser-deduplication |
| Datum (UTC) | 2026-07-29 |
| Basis-Revision | `a81456110a6bb6f7cf2f8202f5223fb3f7b3a194` |
| Tracking | Das ursprüngliche 30-Zeilen-SPOP-CPD-Paar für typed Body-Argumente ist in einem Value-Helper zentralisiert. Der aktuelle exakte PR-Head hat zwei SonarQube-Cloud-`c:S134`-Befunde in `parse_notify_payload` für die verbleibenden verschachtelten `body`- und `response_body`-Key-Branches. |
| Grenze | Parent-HAProxy-Diagnostic-SPOP-Runtime und fokussierte Test-/Change-Record-Dateien. Keine Framework-, MRTS-, Gitlink-, Workflow-, Sonar-Konfigurations-, Suppression- oder `master`-Änderung. |

## Motivation und Problemstellung

Die SPOP-Argumente `body` und `response_body` wiederholten ursprünglich denselben Parsing- und Owned-Byte-Copy-Pfad für nicht vertrauenswürdige typed Values. Der bestehende Value-Helper entfernt dieses CPD-Paar, doch die beiden verbleibenden verschachtelten Key-Branches lösen jetzt Sonar `c:S134` aus. Das Follow-up muss exakte Key-Erkennung, Unknown-Key-Nicht-Consumption, Type-Rejection/-Consumption, Parse-Position, Owned-Memory-Verhalten und Phase-Flags erhalten.

## Akzeptanzkriterien

- Ein privater Value-Helper führt den bestehenden typed Byte-Read aus und akzeptiert nur SPOP-String- oder Binary-Werte.
- Ein privater Key-Dispatcher erkennt nur `body` und `response_body`, delegiert ihre ursprünglichen Rollen und liefert für unbekannte Keys ohne Datenverbrauch das bestehende Parser-Fallthrough-Ergebnis.
- Akzeptierte Werte behalten Owned-Copy und `has_body`; nur Response-Body-Input setzt `is_response` und `is_response_body`.
- Nicht-Byte-typed-Werte bleiben konsumiert, setzen jedoch weder Body- noch Response-Flags.
- Der fokussierte C17-Harness, native GCC-/Clang-C17-Runtime-Builds und der repository-native C23-Hinweis-Check bestehen.
- Hosted Exact-Head SonarQube Cloud muss vor jeder Merge-Betrachtung null New Issues und null New-Code-Duplikation melden.

## Implementierungsentscheidung und Begründung

`parse_notify_body_argument` behält die gemeinsame Read-/Copy-Entscheidung und seine explizite Response-Body-Rolle. Der neue `parse_notify_body_key_argument` zentralisiert nur die beiden begrenzten Literal-Key-Entscheidungen und nutzt denselben Tri-State-Vertrag wie der Header-Dispatcher: null für konsumiertes bekanntes Argument, eins für einen anderen Parser und `-1` für fehlerhafte Eingabe. Das entfernt die zwei verschachtelten Fehler-Branches und erhält Protocol-Parsing, Ownership und Phase-Entscheidungen in derselben Source-Datei.

## Geänderte Dateien

- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` — privater gemeinsamer typed Body-Value-Parser plus begrenzter Body-Key-Dispatcher.
- `tests/test_sonar_reliability_contract.py` — C17-Harness-Abdeckung für String-, Binary-, Response-, Non-Byte- und Unknown-Key-Nicht-Consumption-Pfade.
- Dieses englisch/deutsche Change-Record-Paar und seine gepaarten Indizes.

## Ausgeführte Befehle

| Ausgeführte Kontrolle | Beobachtetes Ergebnis |
| --- | --- |
| `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_sonar_reliability_contract` | bestanden: 11 Tests, einschließlich kompiliertem Body-Key-Dispatcher-Harness. |
| `make check-haproxy-common-adoption`, `make check-haproxy-c-standard-wiring` und `make check-haproxy-c17-lint` | bestanden. |
| `make check-haproxy-c23` | bestanden. |
| `CC=clang HAPROXY_C_STD_PROFILE=c17 sh ci/checks/connectors/haproxy/check-haproxy-c-standards.sh` | bestanden. |
| `git diff --check` | bestanden. |

## Security-Auswirkung

Der Source-to-Sink-Pfad führt von einem peer-kontrollierten SPOP-typed-Argument in den owned `request->body`-Buffer. Der Key-Dispatcher nutzt exakten begrenzten Literalvergleich und lässt unbekannte Keys sowie die Parse-Position für den bestehenden allgemeinen Skip-Pfad unverändert. Der Value-Helper erhält die strikte Type-Grenze: Nur String-/Binary-Werte erreichen `copy_bytes`; andere Typen werden vom bestehenden Typed-Data-Reader konsumiert und können Body- oder Response-State nicht verändern. Der fokussierte C17-Harness prüft beide akzeptierten Byte-Typen, die Non-Byte-Negativkontrolle und Unknown-Key-Nicht-Consumption. Keine Parser-Bounds-, Ownership-, Autorisierungs-, Protocol- oder Quality-Gate-Kontrolle wird gelockert.

## Runtime-Evidence

Der fokussierte C17-Harness kompiliert den tatsächlichen Diagnostic-Runtime-Source und prüft den ausgewählten Key-Dispatch-Pfad. Es werden kein Live-HAProxy-Production-Enforcement und keine Response-Body-Phase 4 beansprucht.

## Bekannte Einschränkungen

- Keine Live-HAProxy-plus-ModSecurity-Runtime und keine vollständige Connector-Matrix liefen, weil der version-festgeschriebene Host-Source-/Runtime-Fixture in diesem temporären Task-Worktree fehlt.
- Die vollständige Codex-Security-Diff-Scan-Fähigkeit bleibt unzugänglich, weil ihr verpflichtender Delegated-Worker-Preflight unvollständig ist; kein vollständiger Scan-Report wird behauptet.
- Hosted-Checks und frische Exact-Head-SonarQube-Cloud-Analyse stehen aus.

## Verbleibende Risiken

- Künftige typed Body-Formen müssen den Helper weiter nutzen oder einen gleichwertigen Protocol-/Ownership-Review erhalten; ein dritter akzeptierter Typ erfordert eine neue Security-Entscheidung.

## Nicht ausgeführte Prüfungen mit Begründung

Keine Live-HAProxy-Runtime, keine vollständige Connector-Matrix und kein vollständiger Codex-Security-Diff-Scan liefen. Die erforderlichen externen Host-Fixtures fehlen und die Scan-Fähigkeit kann ihren verpflichtenden Delegated Worker nicht erhalten. Typed-Parser-Harness und zwei native Compiler-/Runtime-Self-Tests sind die stärksten verfügbaren Kontrollen.

## Finaler Diff- und Review-Status

Der Kandidat ist auf Parent-HAProxy-SPOP-Parsing und bilinguale Traceability begrenzt. Er erhält die ursprüngliche CPD-Reduktion und entfernt die zwei aktuellen `c:S134`-Nesting-Branches bei Erhalt der Request-/Response-Role-Trennung. Lokaler Review ist abgeschlossen; der Draft-PR benötigt vor jeder Delivery- oder Merge-Behauptung frische Exact-Head-Hosted-Verifikation.
