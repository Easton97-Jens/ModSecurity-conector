# FND-MRTS-0002 — MRTS-Upstream-Policy-Sicherheitsmarker fehlte in einer erzwungenen Governance-Kontrolle

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-MRTS-0002` |
| Kategorie | `test_failure` |
| Repository | `mrts` |
| Ownership | `mrts_explicit_user_task` |
| Priorität | `P1` |
| Schweregrad | `not_applicable` |
| Konfidenz | `confirmed` |
| Status | `fixed` |
| Feasibility | `requires_user_decision` |
| Release-Blocker | `false` |
| Security-Relevanz | `true` |

## Zusammenfassung, beobachtetes Verhalten und Auswirkung

Der MRTS-Governance-Validator schlug fehl, weil die aktive Fork-and-Upstream-
Policy die erforderliche ausdrückliche Anweisung fehlte, keine Upstream-URL zu
erraten. Vor der Reparatur beendete sich `tools/validate-governance.py` mit
`1` und identifizierte den fehlenden Marker `Do not guess an upstream URL`. Es
wurde keine Remote-, Source-, Netzwerk- oder Delivery-Aktion versucht.

Der fehlgeschlagene verpflichtende lokale Check verhinderte ein verifiziertes
Configuration-Reconciliation-Ergebnis und ließ eine explizite Defense-in-Depth-
Anweisung an einer Upstream-Trust-Boundary aus. Es wurde kein tatsächlicher
Remote-Missbrauch und kein Runtime-Exploit nachgewiesen.

## Erwartetes Verhalten und betroffene Grenze

Die aktive MRTS-Upstream-Policy muss das Erraten einer Upstream-URL ausdrücklich
verbieten, vor einer Inspektion die Beobachtung des konfigurierten Remote
verlangen und Upstream als inspection-only ohne abgeleitete Delivery-Autorität
beibehalten. Der aktuelle native Validator muss diesen exakten Marker
ausdrücklich prüfen, und seine fokussierten Tests müssen sowohl den fehlenden
Marker als negativen als auch die legitime Policy als positiven Control bewahren.

Betroffene Dateien sind `.codex/context/fork-and-upstream-policy.md`,
`tools/validate-governance.py` und `tools/test_validate_governance.py`.
Betroffene Kontrollen sind der explizite Non-Guessing-Marker, der MRTS-
Governance-Validator und die MRTS-Fork-and-Upstream-Policy.

## Voraussetzungen und sichere Reproduktion

Der bestehende eingebettete MRTS-Checkout und sein nativer Governance-Validator
müssen verfügbar sein. Die retained Pre-Repair-Evidence dokumentiert das exakte
Validator-Kommando und seinen Exit-Code ohne einen Remote zu verändern. Nach der
Reparatur ausführen:

```text
rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-governance.py
rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 tools/test_validate_governance.py
```

Der Validator muss mit `0` enden; die fokussierte Suite muss alle drei Tests
bestehen. Ein aktuell erfolgreicher Validator reicht nicht, wenn er den
ursprünglich fehlenden exakten Marker nicht mehr prüft. Remote-Konfiguration
nicht verändern und keine ausgehende Aktion zur Demonstration der Kontrolle
versuchen.

## Evidence

- Run-ID: `20260726T000000Z-mrts-codex-config-reconciliation-current`
  - Pre-Repair-Artefakt: `evidence/governance-validator-before.txt`
  - SHA-256: `99fac1ae7620a2b32e321603fe51153cdf10f3187b28046c9651bc36de2dfa0a`
  - Kommando: `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-governance.py`
  - Exit-Code: `1`; beobachtet `2026-07-26T04:19:42Z`
  - Retention: `retained_task_evidence`
- Run-ID: `20260726T000000Z-mrts-codex-config-reconciliation-current`
  - Post-Repair-Artefakt: `evidence/governance-validator-after.txt`
  - SHA-256: `f67f95dec10d1042cd42915734114d0a12884b920502df8290cbf406104d6354`
  - Kommandos: der Validator oben und
    `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 tools/test_validate_governance.py`
  - Exit-Code: `0`; beobachtet `2026-07-26T04:24:52Z`
  - Retention: `retained_task_evidence`

## Grundursache und Remediation

Policy und Validator waren auseinander gelaufen: Die Policy bewahrte bereits
Upstream-Inspection-only-Restriktionen, enthielt aber nicht den exakten
ausdrücklichen Non-Guessing-Marker des Validators. Die minimale Reparatur fügt
diesen Marker hinzu, verlangt die Beobachtung des konfigurierten Remote vor der
Inspektion und verbietet die Ableitung eines Upstream-Ziels aus Repository-Namen,
vorherigem Task oder verschachteltem Gitlink. Bestehende Delivery-Verbote bleiben
unverändert.

Das aktuelle Closure-Audit fand jedoch eine spätere Validator-/Test-Änderung:
Die Policy enthält weiter `Do not guess an upstream URL`, aber die aktive
Marker-Liste prüft diesen exakten Text nicht mehr. Die historische Reparatur
bleibt daher eine Code-/Policy-Änderung (`fixed`), nicht eine aktuelle
Verifikation der erzwungenen Kontrolle.

## Akzeptanzkriterien und Validierung

- Die Policy enthält `Do not guess an upstream URL`.
- Upstream bleibt inspection-only; die Reparatur gewährt keine Upstream-Push-,
  Merge-, Synchronisations-, Tag-, Rebase- oder Gitlink-Update-Autorität.
- Der aktuelle native Validator prüft den exakten Non-Guessing-Marker ausdrücklich.
- Der ursprüngliche Validator endet mit `0`.
- Die fokussierte Governance-Regressionssuite besteht alle drei Tests.
- Keine Änderung an MRTS-Produkt-Source, Remote, Branch, Gitlink, Commit, Push,
  PR oder Merge.

Der ursprüngliche Validator und die Drei-Test-Regressionssuite bestanden nach
der Reparatur. Sie bleiben aufbewahrte historische Evidenz, reichen aber nicht
mehr für `verified`, weil der aktuelle Validator denselben exakten Marker nicht
mehr erzwingt. Eine separat autorisierte MRTS-Source-/Test-Korrektur muss die
Assertion wiederherstellen und die Missing-Marker-Negativ- sowie legitimen
Positiv-Controls erneut ausführen.

## Abhängigkeiten, Restrisiko und Historie

Die aktuelle Validierungs-Coverage-Regression blockiert den Abschluss: Die
Wiederherstellung der exakten Validator-Assertion und die erneute Ausführung
der Controls erfordern separat autorisierte MRTS-Source-/Test-Arbeit. Policy
und Validator sind Governance-Evidence, kein Host-seitiger Interceptor. Eine
künftige autorisierte Delivery muss weiterhin ihren unabhängigen
Remote-/Identity-Preflight durchführen; keine Upstream-Delivery-Autorität wird
abgeleitet.

- `2026-07-26T04:19:42Z` — `original_validator_failure_reproduced`: Der native
  Validator endete wegen des fehlenden Markers mit `1`; keine Remote-, Source-,
  Netzwerk- oder Delivery-Aktion erfolgte.
- `2026-07-26T04:24:52Z` — `minimal_policy_repair_verified`: Der explizite
  Marker wurde ohne Authority-Erweiterung ergänzt; der ursprüngliche Validator
  und alle drei fokussierten Regressionstests bestanden.
- `2026-07-26T11:35:17Z` — `verification_reassessed_after_current_validator_coverage_regression`:
  Die aktuelle read-only-Prüfung stellte fest, dass Validator/Test `Do not guess
  an upstream URL` nicht mehr prüfen; der Policy-Text bleibt, aber der
  historische legitime Control ist nicht mehr aktuell. Status ist `fixed`; es
  erfolgte keine MRTS-Source-, Test-, Remote-, Gitlink-, Branch-, Commit- oder
  Delivery-Aktion.

Finale Disposition:
`fixed_policy_marker_present_but_current_validator_no_longer_asserts_exact_marker`.
