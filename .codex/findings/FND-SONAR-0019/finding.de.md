# Befund FND-SONAR-0019: Sonar-Blocker der Traefik-Resultatserialisierung von PR #150

**Sprache:** [English](finding.md) | Deutsch

## Status

`fixed` — der exakte Draft-PR-#150-Head
`4dae04f2d584da855139d6f42ab36c1bdf8c8d63` hat die erforderliche Hosted-
Evidence. Der Befund ist nicht `verified` oder `closed`: PR #150 bleibt Draft
und ungemergt, daher ist nach einem separat autorisierten Merge Current-Master-
Evidence erforderlich.

## Beobachtetes Verhalten

Der erste veröffentlichte Draft-Parent-PR-#150-Head
`7418dfe9a509ea87c0209d64f3082a6c601013c2` hatte drei neue OPEN-BLOCKER-
`c:S3519`-Meldungen an den Copy-Sites von `traefik_engine_send_result`. Sein
Quality Gate war `ERROR`, weil das New-Code-Reliability-Rating `E` war.

Die erste Korrektur verwendete für fehlende Optionalfelder einen gemeinsamen
einbytegroßen leeren C-String. Sonar modellierte anschließend eine positive
Kopierlänge mit diesem Fallback. Der bestehende Bounded-Size-Helper liefert
dafür null zurück; dieser Datensatz behauptet daher keinen nachgewiesenen
Runtime-Out-of-Bounds-Read.

Der normale Nachfolger entfernt diesen Fallback, nutzt einen fail-closed
Bounded-Copy-Helper und beschränkt seinen Zähler auf den C17-`for`-Initializer.
Der exakte Head `4dae04f2d584da855139d6f42ab36c1bdf8c8d63` hat einen an GitHub
gebundenen erfolgreichen SonarCloud-Check, Quality Gate `OK` und null
OPEN/CONFIRMED-PR-Issues. Seine PR-Maße sind null Bugs, Vulnerabilities und
Code-Smells; vererbte Aggregatduplizierung bleibt eine separate projektweite
Altlast.

## Umgesetzte Korrektur

Nullable Optionalfelder für die Bounded-Size-Berechnung behalten. Eine private
begrenzte Copy-Grenze akzeptiert Länge null ohne Quelle und weist eine positive
Länge mit Nullquelle vor der Kopie ab. Sie muss Resultatframe-Feldreihenfolge,
Null-Längen-Kodierung, die `256`/`256`/`2048`-Maxima und Decision-Metadaten
ohne Sonar-Suppression, Exclusion, Quality-Gate- oder Scanner-
Konfigurationsänderung erhalten.

Der finale reine Scope-Nachfolger ändert weder Schleifengrenzen noch kopierte
Bytes: Er deklariert den Zähler an seiner Verwendung. Der direkte Source-
Contract assertiert diese Form, damit die `c:S5955`-Remediation nicht
versehentlich regressiert.

## Evidence

- Aufbewahrte Exact-Head-Issue-Antwort:
  `runs/sonar-652-duplication-zero-20260728-W8wqjk/evidence/pr150-s3519/issues.json`
  (`85137dd3fcc6f78b77d4a5558893c69fec3200e44cf3a405da07108d5ccfbb47`).
- Aufbewahrte Exact-Head-Quality-Gate-Antwort:
  `runs/sonar-652-duplication-zero-20260728-W8wqjk/evidence/pr150-s3519/quality-gate.json`
  (`5d39d167e470b398aec47026771eb8b1dc8216afccffcf75d49e7f29772f0d09`).
- Aufbewahrte Exact-Head-Maße:
  `runs/sonar-652-duplication-zero-20260728-W8wqjk/evidence/pr150-s3519/measures.json`
  (`36112d78bac4adb0d868a0e583fc8c8caf822fc3a1410ec1a06c96bf6d6136c7`).
- Finale Exact-Head-Issues:
  `runs/sonar-652-duplication-zero-20260728-W8wqjk/evidence/pr150-final-4dae.lWGym5/issues.json`
  (`55f044e91d4122d08d0c18dfcf5dc57a1316761d9e59c954b4d3e72f669f6c1e`):
  null OPEN/CONFIRMED-Issues.
- Finales Exact-Head-Quality-Gate:
  `runs/sonar-652-duplication-zero-20260728-W8wqjk/evidence/pr150-final-4dae.lWGym5/quality-gate.json`
  (`c7e717905dde072d807b54104fb4c004f6eef55e0a2900a2cf019db663293d77`):
  `OK` für alle berichteten New-Code-Bedingungen.
- GitHub-Check-Run-Receipt:
  `runs/sonar-652-duplication-zero-20260728-W8wqjk/evidence/pr150-final-4dae.lWGym5/github-check-runs.json`
  (`4674862df6f2e0aa8d10473158911c5bc9ff71b75c54e10235d371ca1a84d3dd`):
  SonarCloud Code Analysis ist auf Exact-Head `4dae04f` `success`.

## Akzeptanz und Validierung

1. Direkte C17-Socketpair-Checks beweisen, dass fehlende, gefüllte und maximal
   lange Resultatfelder den binären Wire-Vertrag erhalten, und dass eine
   positive Länge mit Nullquelle fehlgeschlossen scheitert.
2. Relevante C17-, Diagnostics-, Traefik-Contract-, Dokumentations- und
   Security-Diff-Controls bestehen.
3. Der exakte PR-#150-Head `4dae04f` hat ein frisches Quality Gate `OK` und
   kein OPEN/CONFIRMED-neues Sonar-Issue.

Die nicht verifizierte vollständige Traefik-Host-/Plugin-/Common-/
libmodsecurity-Runtime bleibt außerhalb lokaler Evidence, weil verifizierte
libmodsecurity-Development-Abhängigkeiten fehlen. Nach einem ausdrücklich
autorisierten Merge die Current-Master-Evidence wiederholen, bevor dieser
Befund von `fixed` auf `verified` oder `closed` wechselt.
