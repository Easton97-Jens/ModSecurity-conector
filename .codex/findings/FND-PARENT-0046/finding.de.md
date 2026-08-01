# FND-PARENT-0046 — Python-Versions-Updater-Workflow weist gültige Python-3.14-Patch-Versionen zurück

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-PARENT-0046 |
| Kategorie | ci_failure |
| Repository / Ownership | parent / parent |
| Priorität / Schwere | P2 / not_applicable |
| Konfidenz / Status | reproduced / triaged |
| Machbarkeit | feasible_now |
| Release-Blocker | nein |
| Sicherheitsrelevant | ja |

## Beobachtung, betroffener Scope und Auswirkung

Der wöchentliche/manuelle Workflow `update-python-version` führt
`resolve-python-patch` vor dem read-only-Candidate-Validator und dem engen
Publisher aus. Der Inline-Python-Resolver in
`.github/workflows/update-python-version.yml` verwendet:

```python
r"^3\\.14\\.(?:0|[1-9][0-9]*)$"
```

Die doppelten Backslashes im Raw-String führen dazu, dass normale Punktwerte
fehlschlagen: `3.14.0` und `3.14.6` matchen nicht, während der fehlerhafte Wert
mit Backslashes `3\.14\.6` matcht. Der Resolver endet mit seiner Diagnose für
ungültiges `current_version`/`latest_version` vor Validierung oder
Pull-Request-Erstellung. Er ist daher fail-closed und eröffnet keinen
unsicheren Schreibpfad, deaktiviert aber die geplanten und manuell ausgelösten
zentralen Python-Patch-Updates.

Betroffene Symbole sind `resolve-python-patch`, `validate-python-patch` und
`create-python-update-pr`; die direkt betroffene Datei ist
`.github/workflows/update-python-version.yml`.

## Voraussetzungen, Reproduktion und Evidenz

Voraussetzungen sind ein legitimer `3.14.N`-Wert aus der freigegebenen
Updater-Ausgabe und ein geplanter oder manuell ausgelöster Workflow auf der
vertrauenswürdigen Default-Branch.

1. Die exakte Inline-Regulärexpression mit Python `re.fullmatch` auswerten.
2. `False` für `3.14.0` und `3.14.6` sowie `True` für `3\.14\.6` beobachten.
3. Die Workflow-Blobs auf Parent-Master und PR-#90-Follow-up
   `d99eafd76d9fdbef5b63a19d084fd2d7caff6c08` vergleichen; beide sind
   `80fb3183fae042e982ec3b4507c795bba713cdc1`.

Die aufbewahrte, hash-adressierte Reproduktion ist
`/var/tmp/codex/ModSecurity-conector/runs/20260722T183342Z-pr80-go-toolchain-submodule-c30d4a37/evidence/preexisting-python-updater-regex-reproduction.txt`
(SHA-256 `5ba58ae847649e5f6fc51754c07fde054aa47f007bb7cbbcb286800f21d9df09`,
Exit 0, beobachtet 2026-07-22T21:55:51Z). Die Blob-Gleichheit beweist, dass
dies auf Master vorbesteht und außerhalb des PR-#90-Sonar-Remediation-Diffs
liegt; sie behauptet keine Live-Upstream-Release-Antwort oder einen
write-capable Hosted-Run.

## Ursache, sichere Reparatur und Controls

Eine Regulärexpression mit beabsichtigten escapten literalen Punkten wurde als
Python-Raw-String mit doppelten Backslashes geschrieben. Diese Backslashes
erreichen die Regex-Engine unverändert und kodieren nicht mehr die
beabsichtigten Literal-Punkt-Separatoren.

In einer separat autorisierten Parent-Workflow-Reparatur das Pattern für
exakte `3.14.N`-Werte korrigieren und einen deterministischen Regressionstest
für gültige Punktformen und fehlerhafte Backslash-Formen ergänzen.
Default-Branch-Gating, read-only-Berechtigungen von Resolver und Validator,
Reihenfolge Validierung-vor-Publisher, Candidate-Revalidierung,
Checkout-Einstellungen, Publisher-Scope und die `.python-version`-only-
Writer-Allowlist bewahren. Gültige Werte dürfen nur die bestehende
read-only-Validierungsstufe erreichen; fehlerhafte Werte müssen vor der
Veröffentlichung scheitern.

Dies ist kein Duplikat von FND-PARENT-0044, das einen separaten
`setup-python`-Action-Pin-Contract besitzt. Es ist nur verwandt, weil beide
Befunde die Python-Versionswartung betreffen.

## Akzeptanzkriterien und Validierungsplan

- Der Resolver akzeptiert exakte `3.14.0` und `3.14.6` und weist fehlerhafte
  Backslash-Formen einschließlich `3\.14\.6` zurück.
- Ein deterministischer Test deckt den Inline-Resolver statt Live-Metadaten ab.
- `tests/test_update_python_version.py`,
  `tests/test_python_version_contract.py`,
  `tests/test_ci_security_workflows.py` und
  `make check-python-version-contract check-ci-security-contract` bestehen.
- Exact-Diff-Review und ein ausdrücklich autorisierter Exact-Head-Hosted-Run
  beweisen, dass die Trusted-Staged-Sicherheits- und engen Publisher-Controls
  intakt bleiben.

Abhängigkeiten sind eine separat autorisierte Workflow-Reparatur und
Exact-Head-Hosted-GitHub-Actions-Validierung. Kein Finding blockiert die
Triage, es wird kein Sicherheitsrisiko akzeptiert, und dieser Triage-Record
autorisiert keine aktuelle PR-#90-Source-Änderung.

## Restrisiko und Historie

Bis eine separat geprüfte Reparatur ausgeliefert ist, bleibt die
Python-Patch-Wartung nicht verfügbar. Der beobachtete Defekt bleibt
fail-closed; kein Publisher-Control wird geändert oder abgeschwächt.

- 2026-07-22T21:55:51Z — das exakte Resolver-Verhalten wurde reproduziert und
  die Master-/PR-Workflow-Blob-Gleichheit belegt. Der vorbestehende Befund
  wurde ohne Änderung des Workflows triagiert.
