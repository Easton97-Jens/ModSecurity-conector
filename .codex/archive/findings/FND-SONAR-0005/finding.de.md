# FND-SONAR-0005 — Framework-PR #29: SonarQube-Quality-Gate scheiterte an Workflow-Checker-Pfad-Containment- und Komplexitätsbefunden

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-SONAR-0005` |
| Kategorie | `sonarqube_finding` |
| Repository / Ownership | `framework` / `framework` |
| Priorität / Schwere | `P1` / `not_applicable` |
| Confidence / Status | `validated` / `verified` |
| Machbarkeit | `feasible_now` |
| Release-Blocker | `false` |
| Security-relevant | `true` |

## Zusammenfassung und beobachtetes Verhalten

Der exakte Framework-PR-#29-Head
`191b7e3d1999c7ffb39ad16bfaff7821bfc09825` scheiterte am
SonarCloud-Check-Run `88075927543` am `2026-07-18T11:33:49Z`. Das Quality Gate
meldete Security Rating C auf New Code, obwohl A erforderlich ist, und erzeugte
elf Annotationen in `ci/checks/security/check-github-actions-workflows.py`.
Failure-Level-Annotationen lagen an den Zeilen 122, 126, 284 und 313; die
übrigen Warnings lagen an den Zeilen 32, 38, 48, 51 und 198, mit je zwei
eigenständigen Annotationen an den Zeilen 38 und 48.

Die normale Current-Master-Reconciliation und die fokussierte Remediation
bestanden zunächst SonarCloud am exakten PR-Head
`fdb400b85bfd2779e95cc3ab8fb29a3e2e3793bf` ohne Suppression. Der finale
synchronisierte PR-Head `5fa814d19b86f5c0a406b95914d6121af83ffe07` bestand
anschließend alle zehn frischen PR-Checks, einschließlich SonarCloud Code
Analysis, CodeQL Actions/C++/Python, scaffold-lint und common-structure. Er
hatte keine Reviews und keine Review-Threads. Er wurde am `2026-07-19T15:12:26Z`
als Framework-Master `7a12073c28e62a67492dd501b6513b9914fe5df8` squash-gemergt;
der finale PR- und Master-Tree sind beide
`25dae479a3f23e12a69db0ef9e034edae218f6d9`. Der resultierende Master führte
die ursprüngliche Workflow-Security- und Legitimate-Control-Matrix erfolgreich
erneut aus; deshalb ist dieser Record `verified`, nicht `closed`.

## Erwartetes Verhalten, Impact und Scope

Der kanonische Workflow-Security-Checker muss verschachtelte `.yml`/`.yaml`-
Dateien rekursiv scannen und jede übergebene Root, jeden erkannten Kandidaten
und jedes Leseziel unterhalb der Repository-Root des Aufrufs auflösen. Er muss
Outside-Roots und Symlink-Escapes ablehnen und zugleich striktes YAML-Parsing
und sämtliche Workflow-Trust-Boundary-Controls erhalten.

Das Quality-Gate-Scheitern war ein erforderlicher externer
Integrationsblocker. Der betroffene Validator ist security-relevant, aber die
Evidence belegt keine separat ausnutzbare Produktvulnerabilität; die
Security-Schwere ist daher `not_applicable`. Die exakte frische PR-Head- und
resultierende-Master-Evidence belegt, dass dieses spezifische Gate-Scheitern
nicht mehr reproduzierbar ist. Dies bleibt Framework-only-Scope: Es autorisiert
weder eine Parent-Produkt-/Gitlink-Änderung noch eine MRTS-Aktion.
`FND-SONAR-0002` ist ein separater akzeptierter Default-Branch-Backlog und hat
das frische PR-Head-Gate ausdrücklich nicht waived.

## Evidence, Grundursache und Remediation

Der aufbewahrte Receipt
`/var/tmp/codex/ModSecurity-conector/runs/20260719T081017Z-framework-pr-resolution-20260719-840082e0/evidence/pr29-fdb400b-sonar-remediation.md`
hat SHA-256
`65ce440af9e7ee53221ef36980581bad5f66e9e3273bf611135ceabcf8c9a8ee`. Er
enthält das historische Scheitern, alle Annotation-Positionen, die
Source-Level-Remediation und den Exact-Head-Erfolg. Er wurde mit GitHub-Checks-
API-Befehlen für den alten Check `88075927543`, dessen Annotationen und Commit
`fdb400b…` aus der Parent-Root mit Exit-Code 0 erhoben.

Die Grundursache war eine fehlende einheitliche aufgelöste
Repository-Root-Containment-Grenze für jeden angeforderten, erkannten und
gelesenen Workflow-Pfad sowie eng gekoppelte Scan-Helfer, die Scannerbefunde zu
konstruierten Pfaden und kognitiver Komplexität auslösten. Die Remediation löst
Repository-Root und Workflow-Pfade strikt auf, begrenzt Kandidaten auf die
Workflow-Root, erkennt YAML-Dateien rekursiv, lehnt explizite Outside-Roots und
entweichende Symlinks ab, validiert vor dem Lesen erneut und zerlegt
`source_uses` sowie `validate_permissions`. Sie ergänzt Regressionen für
verschachtelte Workflows, Outside-Roots und Symlink-Escapes ohne Scanner-
Suppression, Exclusion, Quality-Gate-Änderung, Workflow-Deaktivierung oder
Abschwächung eines Security-Controls.

Der unveränderliche Post-Merge-Receipt
`/var/tmp/codex/ModSecurity-conector/runs/20260719T081017Z-framework-pr-resolution-20260719-840082e0/evidence/fnd-sonar-0005-pr29-master-verification.md`
hat SHA-256
`ad53a13fb5d9c8364da23433c0caabe9dd5a980e007413505d84bb1eb7944171`. Er wurde
um `2026-07-19T15:16:31Z` beobachtet, als Task-Evidence aufbewahrt und enthält
die finalen exakten PR-Head-, Merge/Master- und Tree-Identitäten, Tree-Gleichheit
und die native Master-Validierung in
`/var/tmp/codex/worktrees/framework-workflow-hardening` (Exit-Code 0). Der
native vollständige Lint bestand alle sieben Workflow-Security-Contract-Tests—
einschließlich verschachtelter Erkennung, expliziter Outside-Root-Ablehnung und
Symlink-Escape-Ablehnung—sowie einundzwanzig Action-Pin-Tests, zehn
CRS-Provenance-Tests und die übrigen repository-nativen Controls.

## Akzeptanzkriterien und Validierung

- Das historische Exact-Head-Scheitern und seine elf Annotationen mit einem
  hash-adressierten Receipt aufbewahren.
- Verschachtelte Erkennung, Outside-Root-Ablehnung und Symlink-Escape-Ablehnung
  mit der fokussierten Workflow-Security-Regressionssuite beweisen und dabei
  bestehende YAML-, Permission-, Token-, Checkout-, Pull-Request-Target- und
  Action-Pin-Controls erhalten.
- Alle zehn bestehenden frischen Checks am finalen exakten PR-Head `5fa814d…`
  beobachten, einschließlich SonarCloud, ohne Scanner-Policy zu ändern oder
  eine Regel zu unterdrücken, und das Fehlen von Reviews und Review-Threads
  bestätigen.
- Auf Framework-Master `7a12073c…` Gleichheit von finalem PR- und Master-Tree
  feststellen und die ursprüngliche Reproduktion sowie legitime Controls
  erfolgreich erneut ausführen.
- Erfolgreiche Master-Checks für CodeQL C++/Actions/Python, scaffold-lint und
  common-structure beobachten. Der Master-SonarCloud-Check `88207281607`
  scheiterte mit Security E und Reliability D sowie null Annotationen
  ausschließlich unter dem separat akzeptierten `FND-SONAR-0002`; dies ist kein
  frischer PR-Head-Waiver.

## Restrisiko und Historie

Die historische Sonar-Gate-Bedingung von PR #29 ist auf Framework-Master
verifiziert behoben. Der separate master-only-SonarCloud-Check `88207281607`
bleibt als akzeptiertes Risiko `FND-SONAR-0002` mit Security E, Reliability D
und null Annotationen; er waivt dieses Finding weder noch eröffnet er es erneut.
`FND-SONAR-0005` ist auf Master verifiziert, aber nicht geschlossen: Die
ursprüngliche Failure-/Remediation-Evidence bleibt aufbewahrt, und ein künftiger
Lifecycle-Abschluss erfordert eine separate Autorisierung.
`2026-07-18T11:33:49Z`: historisches Exact-Head-Scheitern validiert.
`2026-07-19T14:18:07Z`: nicht-unterdrückende Remediation bestand das erste
Exact-PR-Head-Sonar-Gate. `2026-07-19T15:12:26Z`: finaler Head `5fa814d…`
gemergt als `7a12073c…`. `2026-07-19T15:16:31Z`: Tree-Gleichheit und native
Master-Controls erfolgreich abgeschlossen; Status auf `verified` erhöht.
