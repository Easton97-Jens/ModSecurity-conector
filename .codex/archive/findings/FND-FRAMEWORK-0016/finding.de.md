# FND-FRAMEWORK-0016 — Security-Tool-Downloader akzeptierte einen nicht eingegrenzten Lockfile-Pfad

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-FRAMEWORK-0016` |
| Kategorie | `security_hardening` |
| Repository / Ownership | `framework` / `framework` |
| Priorität / Schwere | `P2` / `medium` |
| Confidence / Status | `validated` / `fixed` |
| Machbarkeit | `feasible_now` |
| Release-Blocker | `false` |
| Security-relevant | `true` |

## Zusammenfassung

Die generische `--lock`-CLI-Grenze im Security-Tool-Downloader akzeptierte eine
reguläre nicht verlinkte Lockdatei außerhalb der Framework-Root. Der eingecheckte
Workflow-Aufruf war vertrauenswürdig, aber die generische CLI-Eingrenzung war zu
breit.

## Evidence und Remediation

`ci/tools/fetch-security-tool.py` löst relative Locks jetzt von der Framework-
Root auf und lehnt absolute Pfade außerhalb der Root, Traversal-Pfade, Symlink-
Komponenten, Symlink-Leaves und Nonregular Files vor dem YAML-Parsing ab.
Fokussierte Regressionen akzeptieren den echten Framework-Lock und lehnen
externe, Traversal- und Symlink-Pfade ab. Die Remediation ist in
`768a06b5b734547f8213cc6918c26ef4a8ef9f67` committet; exaktes lokales
`make lint` und 64 CI-Security-Tests bestanden. Aufbewahrte Artefakt-SHA-256:
`979715e7ec9a24e700f04ab6722b5f717b1f229023a6c4de6051c675a79155c5`.

## Akzeptanzkriterien

- `--lock` ist vor dem Lock-Parsing auf die Framework-Root eingegrenzt.
- Legitime relative und absolute In-Root-Lock-Pfade bleiben akzeptiert.
- Externe, Traversal-, Symlink- und Nonregular-Pfade schlagen vor YAML-Zugriff fehl.
- Exakte Final-PR-Head-CI bestätigt das committete Downloader-Verhalten.

## Restrisiko und Historie

Der tatsächliche Workflow-Lock war vor der Reparatur vertrauenswürdig, aber
generische CLI-Aufrufer haben jetzt fail-closed Confinement. Remote-Exact-Head-
Evidence steht aus. `2026-07-18T15:18:00Z`: erstellt und lokal repariert.
