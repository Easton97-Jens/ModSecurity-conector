# FND-PARENT-0044 — Python-Workflow-Sicherheitsvertrag weist den aktuellen unveränderlichen setup-python-v7-Pin zurück

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-PARENT-0044 |
| Kategorie | ci_failure |
| Repository / Ownership | parent / parent |
| Priorität / Schwere | P1 / not_applicable |
| Konfidenz / Status | confirmed / fixed |
| Machbarkeit | feasible_now |
| Release-Blocker | ja |
| Sicherheitsrelevant | ja |

## Beobachtung und Auswirkung

Der aktuelle Master `2ade0d40983b7af21a65b8cd2884866b85626393` pinnt jede
aktive `actions/setup-python`-Verwendung und ihren geprüften Lock-Eintrag
korrekt auf `5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0`. Der
strengere Python-Workflow-Checker verlangt stattdessen weiterhin
`ece7cb06caefa5fff74198d8649806c4678c61a1 # v6.3.0`.

Der auf sauberem Master festgehaltene Befehl

```text
rtk proxy env PYTHON=/root/git/ModSecurity-conector/.venv/bin/python PYTHONDONTWRITEBYTECODE=1 make check-python-version-contract
```

endet deshalb mit `2`. Er weist den freigegebenen v7-Pin zurück, meldet null
erkannte Setup-Schritte und erzeugt kaskadierend falsche Setup-before-use-
Fehler. Das ist ein Verfügbarkeits- und Integritätsproblem eines CI-Supply-
Chain-Controls; weder die Ausführung einer veränderlichen Action noch
Credential-Exposure, Repository-Write-Bypass oder ein Connector-Runtime-
Exploit wurden belegt.

## Evidence, Ursache und beabsichtigte Reparatur

- Run: `20260721T101749Z-parent-python314-go126-upgrade-8add1076`
- Retained Artifact:
  `/var/tmp/codex/ModSecurity-conector/runs/20260721T101749Z-parent-python314-go126-upgrade-8add1076/evidence/python-contract-prechange-failure.md`
- SHA-256:
  `461d1710225eb8f79008308ebbc168fab50d968dc2e9ea8e55da5e1e1b3fb921`
- Exit-Status: `2`
- Post-Remediation-Retained-Artifact:
  `/var/tmp/codex/ModSecurity-conector/runs/20260721T101749Z-parent-python314-go126-upgrade-8add1076/evidence/python-go-toolchain-final-local-validation.md`
- Post-Remediation-SHA-256:
  `2dca237a075dd15f7e7e5a90e26bca8328a88bb89076063856a21ccb15bb3dbd`

Der v7-Workflow und der Eintrag in `ci/tooling/security-tools.lock.yml` sind
bereits korrekt und dürfen nicht geändert werden. Die vorherige v7-Transaktion
ließ diesen Python-spezifischen Checker, seine gültigen Fixtures und erwartete
Teststrings auf der alten v6-Identität. Die enge Reparatur aktualisiert exakt
diese Checker-/Test-/Fixture-Erwartungen auf den vorhandenen v7-SHA und
-Kommentar und bewahrt Immutable-Pins, Lock-Mitgliedschaft, Berechtigungen,
Trigger, Checkout-Verhalten, `check-latest: false` und die Setup-before-use-
Validierung.

Der gleiche atomare Candidate hebt die gewünschte Python-Serie auf exakt
`3.14.6`. Der Updater akzeptiert weiterhin nur stabile exakte `3.14.N`-
Patches; er darf kein Cross-Minor- oder Floating-Version-Updater werden.

## Erforderliche Controls und Disposition

Der reparierte Checker muss eine gültige exakte v7-Referenz akzeptieren und
weiterhin einen veränderlichen Tag, kurzen SHA, fehlenden Kommentar, falschen
Kommentar und einen nicht zum Lock passenden SHA zurückweisen. Der
ursprüngliche Vertrag und seine Unit-Suite müssen ebenso wie der unabhängige
CI-Sicherheitsworkflow-Vertrag bestehen. Ein Diff-Review muss bestätigen, dass
tatsächliche Workflow-Pins und der geprüfte Lock unverändert bleiben.

Das lokale Ergebnis ist `confirmed` und `fixed`, nicht verified oder closed.
Der ursprüngliche Vertrag besteht jetzt für Python `3.14.6` und 25 Python-Jobs;
auch 98 fokussierte Unit-Tests, der unabhängige CI-Sicherheitsvertrag, der
Compiler-Guide-Check, compileall sowie die begrenzten Lock-/Diff-Controls
bestehen. Die exakte Auflösung von Python `3.14.6` durch die Action und die
exakte Go-`1.26.5`-CodeQL-Ausführung benötigen weiterhin Hosted-Evidence am
finalen Candidate-Head. Das vollständige Bilingual-Target ist nur durch den
absichtlich nicht initialisierten Framework-Gitlink blockiert; Framework und
MRTS bleiben unverändert. Es gab kein Staging, keinen Commit, Push, Pull
Request oder Merge sowie keine Framework- oder MRTS-Aktion.

## Historie

- 2026-07-21T10:17:49Z — die saubere Current-Master-Reproduktion hielt den
  v6/v7-Mismatch und Exit `2` fest.
- 2026-07-21T10:28:55Z — nach Deduplizierung gegen FND-PARENT-0018 wurde ein
  eigenständiges Parent-CI-Supply-Chain-Contract-Finding angelegt; die atomare
  lokale Reparatur begann ohne Änderung realer Action-Pins oder Locks.
- 2026-07-21T11:07:03Z — Reparatur und legitime Controls bestanden lokal: der
  ursprüngliche Vertrag, 98 fokussierte Unit-Tests, CI-Sicherheitsvertrag,
  Compiler-Guide-Check, compileall und begrenztes Lock-/Diff-Review bestanden;
  exakte Target-Runtime- und Exact-Head-Hosted-Evidence bleiben erforderlich.
