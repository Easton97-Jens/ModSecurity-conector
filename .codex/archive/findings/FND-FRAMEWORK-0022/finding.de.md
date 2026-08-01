# FND-FRAMEWORK-0022 — Framework-Action-Lock hinkt dem aktiven unveränderlichen upload-artifact-Pin hinterher

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-FRAMEWORK-0022` |
| Kategorie | `ci_failure` |
| Repository / Ownership | `framework` / `framework` |
| Priorität / Severity | `P1` / `not_applicable` |
| Confidence / Status | `confirmed` / `verified` |
| Feasibility | `feasible_now` |
| Release-Blocker | `false` |
| Security-relevant | `true` |

## Zusammenfassung, Beobachtung und Auswirkung

Der aktuelle Framework-Source verwendet in drei Security-Workflow-Schritten
unveränderliches
`actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a` mit dem
Release-Kommentar `v7.0.1`. Das repository-eigene
`ci/tooling/security-tools.lock.yml` verzeichnete weiterhin den früheren
Release `v5.0.0` und den Commit
`330a01c490aca151604b8cf639adc76d48f6c5d4`.

Der externe Dependabot-Commit `61fec7cb40e0b940760c079f0e8da3f977bc9ae8`
änderte die Workflow-Uses, synchronisierte aber den Custom-Provenance-Lock
nicht. Der statische CI-Security-Vertrag lehnte die Abweichung korrekt ab. Der
Befund ist ein P1-Release-Blocker, weil der unveränderliche Action-Supply-Chain-
Vertrag die aktuellen Workflows nicht wahrheitsgemäß validieren kann, solange
sein eigenes Inventar veraltet ist.

Dies ist kein Permission- oder Workflow-Runtime-Scope: Keine Permission,
Artifact-Retention, Workflow-Referenz, kein mutabler Tag und kein Checker wird
abgeschwächt. Die aktuelle autorisierte Reparatur aktualisiert ausschließlich
den veralteten Lock-Record auf den bereits aktiven, offiziell verifizierten
unveränderlichen v7.0.1-Commit.

## Scope, Reproduktion und Evidence

Betroffen sind `.github/workflows/ci-security-osv.yml`,
`.github/workflows/ci-security-scorecard.yml` und
`ci/tooling/security-tools.lock.yml`.

```text
rtk git show --format='%H%n%s' --no-patch 61fec7cb40e0b940760c079f0e8da3f977bc9ae8
rtk gh api repos/actions/upload-artifact/git/ref/tags/v7.0.1 --jq .object.sha
rtk rg -n 'actions/upload-artifact|version: v5.0.0|330a01c490aca151604b8cf639adc76d48f6c5d4' .github/workflows ci/tooling/security-tools.lock.yml
```

Die offizielle GitHub-Tag-API löst `v7.0.1` auf
`043fb46d1a93c77aae656e7c1c64a875d1fc6a0a` auf. Nach der fokussierten
Lock-Reparatur bestand die lokale Matrix des Tasks für
`test-ci-security-contract`, unveränderliche Workflow-Pins und
Workflow-Permissions (69 CI-Security-Tests sowie die 21-Tests umfassende
Pin-Suite). Externe API- und Commit-Daten bleiben externe Evidence; ihre Hashes
werden bewusst nicht erfunden.

## Grundursache, erwartetes Verhalten und Remediation

Das Dependabot-Workflow-Update enthielt nicht den repository-spezifischen
security-tools-Provenance-Lock. Jede externe Action-Referenz muss einem
vollständigen Lock-Record entsprechen: exakter Release, exakter vollständiger
Commit, Upstream-Release-URL, Lizenz, Zweck, Plattform und Update-Prozedur.
Der Vertrag muss veraltete, mutable, verkürzte, fehlerhafte oder nicht passende
Referenzen weiterhin ablehnen.

Der aktuelle Task aktualisiert genau den `actions/upload-artifact`-Lock-Record
auf `v7.0.1`, den verifizierten unveränderlichen Commit und die passende
Upstream-Release-URL. Er bewahrt alle Workflow-Referenzen, Action-Pin-
Enforcement, Permissions, Retention-Policy und die etablierte Update-Prozedur.

- [verifiziert] Der geprüfte Lock-Record entspricht `v7.0.1` und seinem
  exakten SHA.
- [verifiziert] Die fokussierten CI-Security-, Action-Pin- und
  Permission-Checks akzeptieren den reparierten Record und prüfen weiterhin
  Ablehnungs-Controls.
- [verifiziert] Exakter PR-Head
  `e94029f5b893ef6a8efa118d21698426a43c82dd` und resultierender Master
  `9a729226d2e040d07d7e7a4acebf201faf06ab37` bestanden die anwendbaren
  gehosteten CI-Security- und Immutable-Action-Controls.

## Grenzen, verwandte Findings und Restrisiko

Dieser Befund ist von `FND-FRAMEWORK-0021` verschieden, das den CPython-ABI-
und PyYAML-Wheel-Hash-Mismatch besitzt, und von `FND-FRAMEWORK-0019`, das die
Flow-Style-YAML-Vertragsinkompatibilität besitzt. Er hängt mit dem früheren
Immutable-Action-Pin-Hardening in `FND-FRAMEWORK-0003` zusammen, aber die
Regression ist ein veralteter Custom-Provenance-Record, keine mutable
Action-Referenz.

Der lokale Testinterpreter ist CPython 3.14.4, aber exakte gehostete PR- und
resultierende-Master-Controls belegen nun die beabsichtigte Action-Runtime. Das
Finding ist auf Master `9a729226d2e040d07d7e7a4acebf201faf06ab37` `verified`;
unveränderliche Pins, Permissions, Retention und Mismatch-Rejection bleiben
unverändert. Der separate Master-SonarQube-Cloud-Backlog ist
`FND-SONAR-0002`. Keine Parent- oder MRTS-Änderung wurde autorisiert oder
vorgenommen.

- `2026-07-19T21:31:45Z`:
  `stale_action_provenance_lock_confirmed_and_remediation_started` — die durch
  Dependabot entstandene Workflow-/Lock-Abweichung wurde bestätigt; die
  v7.0.1-Tag-Identität wurde unabhängig geprüft, die minimale Lock-Reparatur
  durchgeführt und die fokussierte lokale Security-Matrix bestanden. Gehostete
  Validierung steht aus.
- `2026-07-19T22:18:45Z`:
  `verified_after_exact_pr33_merge_and_master_contract_controls` — Framework-
  PR #33 bestand Exact-Head-GitHub-Actions und SonarQube Cloud ohne Reviews
  oder Threads und wurde dann normal am erwarteten Head
  `e94029f5b893ef6a8efa118d21698426a43c82dd` als Master
  `9a729226d2e040d07d7e7a4acebf201faf06ab37` gemergt. Master
  `actionlint-and-contract` und `zizmor` bestanden mit dem synchronisierten
  v7.0.1-Lock; Permissions, Retention und Immutable-Pin-Enforcement blieben
  unverändert.
