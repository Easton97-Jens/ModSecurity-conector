# Change Record: Audit-Log-Pointer im NGINX-Case-Resultat

**Sprache:** [English](CR-20261001-nginx-audit-result-pointer.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20261001-nginx-audit-result-pointer` |
| Datum (UTC) | `2026-10-01` |
| Basis-Revision | `2634d821acd80ad208a8e1cd3e4f49fd7e80c628` |

## Motivation und Problemstellung

Der Host schreibt sein Audit-Log unter `NGINX_SERVER_LOG_ROOT`, das
Case-Resultat verwies jedoch auf `output_dir/audit.log`. Im Root/nobody-Layout
sind diese verschieden; der Collector konnte das echte Audit daher nicht
über den deklarierten Pfad lesen.

## Akzeptanzkriterien

Beide Resultat-Zweige verwenden das tatsächliche `AUDIT_LOG_FILE`. Frühe
Resultate vor der Zuweisung behalten ihren Case-lokalen Fallback. Keine
synthetischen Events, PASS-Promotion, Collector-Änderung oder gelockerte
Framework-Validierung.

## Implementierungsentscheidung und Begründung

`${AUDIT_LOG_FILE:-$output_dir/audit.log}` wird an die bestehende Case-Info-CLI
übergeben. Log-Layout, Ownership, Projection und Collection-Autorität bleiben erhalten.

## Geänderte Dateien

- `connectors/nginx/harness/run_nginx_smoke.sh`
- `tests/test_nginx_audit_result_pointer.py`
- Dieses EN/DE-Change-Record-Paar und seine Archive-Index-Einträge.

## Ausgeführte Befehle

Alle Shell-Befehle nutzten RTK. Die Verhaltensregression scheiterte zuerst am
falschen Pointer; nach der Korrektur bestanden drei Tests. Der gemeinsame
Parent-Fokuslauf für Protocol-Wiring, Selected-Runner, Audit-Pointer,
Phase-4-Wiring, Projection, Path-Authority, Projection-Invocations und nativen
Sink bestand 58 Tests. Fixture-abhängige Tests verwendeten das unveränderte
Framework-Pin `cc36b37d0f6a0fbc3512f3878a691751e91c5fbb`. `sh -n`,
`shellcheck -S error` und `git diff --check` bestanden. Vollständiger
ShellCheck meldet bestehende Warnungen; keine wurde unterdrückt.
`make check-bilingual-docs check-doc-links` bestand; beim ersten
Dokumentationsversuch musste das Format des Sprachwechsels korrigiert werden.

## Security-Auswirkung

Dies korrigiert die Erreichbarkeit der Evidence, nicht die Validierungssemantik.
Native-Event-, Case/Run-Identitäts-, Containment- und Root-Master/nobody-Worker-
Kontrollen bleiben unverändert. Der Fallback macht fehlende Evidence nicht zu PASS.

## Runtime-Evidence

Frühere isolierte Host-Proben reproduzierten einen fehlenden deklarierten
Audit-Pfad und ein nichtleeres tatsächliches Audit-Log. Die neuen Tests
erfassen CLI-Argumente der echten Shell-Funktion; dies ist kein Runtime- oder
kanonischer PASS.

## Bekannte Einschränkungen

Dies liefert weder die verbleibenden 54 H1-Pflicht-Pfade noch behebt es den
unabhängigen Downstream-Protocol-Aufrufvertrag.

## Verbleibende Risiken

Ein Audit-Pointer ersetzt keine erforderlichen nativen Events. Nach grünen
Coverage-Gates bleibt ein neuer Exact-Head-Lifecycle notwendig.

## Nicht ausgeführte Prüfungen mit Begründung

Kein neuer Full-E2E, kanonischer PASS oder SHA256SUMS: Die Runner-Coverage ist
rot. Kein Remote-CI, Push, PR-Eingriff, Merge oder MRTS-Eingriff.

## Finaler Diff- und Review-Status

Der Pointer-Diff wurde unabhängig geprüft. Dieser Record betrifft nur diese
Korrektur, nicht andere uncommittete Parent-Integration.
