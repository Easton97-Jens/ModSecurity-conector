# FND-PARENT-0045 — Update-Submodules-Validierungstests erwarten ein verbotenes HAProxy-Runtime-Binärprogramm aus dem Shared Cache

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-PARENT-0045 |
| Kategorie | ci_failure |
| Repository / Ownership | parent / parent |
| Priorität / Schwere | P1 / not_applicable |
| Konfidenz / Status | confirmed / fixed |
| Machbarkeit | feasible_now |
| Release-Blocker | ja |
| Sicherheitsrelevant | ja |

## Beobachtung und Auswirkung

Der GitHub-Actions-Run [29945542984](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29945542984)
löste den Framework-Candidate `f73f8842f45318e2df8aff1d31855eeb7c20a22f`
erfolgreich auf und checkte ihn aus, doch sein read-only-`make quick-check`
scheiterte in drei Parent-HAProxy-Managed-Cache-Tests. Jeder endet mit:

```text
haproxy_prepare: blocked HAPROXY_RUNTIME_BUILD_DIR must be under BUILD_ROOT
```

Der Publisher wurde korrekt übersprungen. Dies ist ein
CI-Control-Kompatibilitätsfehler, kein Exploit: Er verhindert eine
Candidate-Veröffentlichung, statt einem schreibfähigen Job einen unsicheren
Pfad zu geben.

## Ursache und sichere Reparaturgrenze

Die direkte Parent-Test-Fixture konstruiert Runtime-Build-Verzeichnis,
Worktree, Runtime-Verzeichnis und HAProxy-Binärprogramm unter
`cache-v2/shared`, übergibt aber eine andere `BUILD_ROOT`. Der aktuelle
Framework-Master verlangt korrekt, dass diese Runtime-Outputs unter
`BUILD_ROOT` bleiben; seine Sicherheitsregression fordert dasselbe
fail-closed-Verhalten.

Der Parent-Komponentenpräparer verwendet beim Aufruf des Framework-Scripts
bereits seinen Managed-Connector-Entry als effektive `BUILD_ROOT`. Daher ist
die direkte Test-Fixture die abweichende Ebene. Die Reparatur muss ihre
veraltete positive Reuse-Assertion durch einen legitimen Managed-Entry-Control
und einen expliziten Rejection-Control für getrenntes `BUILD_ROOT` ersetzen.

Sie darf weder Framework-Source, Parent-Gitlink oder MRTS noch
Workflow-Berechtigungen, das read-only-Validierungsgate oder die
Publisher-Berechtigungsregel ändern.

## Lokale Reparatur und erforderliche Validierung

Die Parent-Fixture-/Invocation-Seam ist jetzt im isolierten Task-Worktree
korrigiert. Die fokussierte Suite lief über die bewusst übergebene read-only-
Framework-Root bei `f73f8842…`, führte 61 Tests aus und bestand. Sie enthält
legitimen Managed-Entry-Reuse, einen vollständigen Entry ohne Cache-Marker,
einen No-Rebuild-Control und die explizite Split-Root-Exit-77-Rejection. Das
Go-/Python-/CI-Contract-Target bestand einschließlich des Static-Nachweises,
dass `update-submodules.yml` Resolve → read-only-Validierung → engen Publisher
und die Berechtigungen bewahrt. Ein fokussierter Security-Diff-Scan wurde mit
null reportierbaren Befunden finalisiert.

Der initiale Draft-PR-#90-Head `0acba7768848651758610928e89f4481dbb90c81`
erreichte fünf abgeschlossene normale Push-Workflows (29955277020, 29955277057,
29955276989, 29955277045 und 29955277071). Die authentifizierte
Failed-Log-Prüfung zeigt bei allen dieselbe veraltete Assertion: Der alte
Parent-Test erwartete Exit 77, während der Legacy-Gitlink
`784977615acfc55567e37b863309abc4a38ac877` durch Managed-Cache-Reuse korrekt
Exit 0 lieferte. Der begrenzte Follow-up überspringt nur diese exakte
Legacy-Revision, schlägt bei unbekannten oder nicht-strengen Revisionen
fail-closed fehl und führt den Exit-77-Control gegen F73 aus. Er bestand erneut
die 61 fokussierten Tests, 11 bilingualen Tests, die Go-/Python-/CI-Contracts
und einen vollständigen finalen Security-Scan mit null reportierbaren Befunden.

Der spätere exakte PR-#90-Head
`06a4e71408a60e5a72a55065a653b9c4e79a1ecf` hat Gleichheit von lokalem,
Remote- und PR-SHA, gewöhnliche GitHub-Checks terminal erfolgreich oder
übersprungen sowie SonarQube-Cloud-Quality-Gate `OK`. Sein Receipt ist
hosted-pr90-06a4e71-validation.json (`/var/tmp/codex/ModSecurity-conector/runs/20260722T183342Z-pr80-go-toolchain-submodule-c30d4a37/evidence/hosted-pr90-06a4e71-validation.json`)
(SHA-256 `db38c89e5c1646e343ec022466d7fec899998dda05558ccf85789196d273ea20`).

Die aktuelle Disposition ist `fixed`, nicht verified oder closed. Der
Replacement-PR benötigt weiterhin eine Exact-Head-Hosted-`Update submodules`-
Validierung vor Verifikation oder Closure. Das breite Documentation-Target ist
nur durch den absichtlich nicht initialisierten Parent-Framework-Gitlink
blockiert. Die installierte Go-1.26.0-Executable blockiert lokale
`GOTOOLCHAIN=local`-Modul-Test-/Vet-Aufrufe korrekt, weil beide Module 1.26.5
erfordern; sie lud keine Toolchain nach und änderte keine Module.

Der einzelne spätere autorisierte Current-Master-Run `29981644356` erreichte
read-only-Candidate-Checkout und Interpreter-Vertrag, scheiterte dann aber
früher an der separaten PyYAML-Fixture-Syntax-Voraussetzung, bevor er die
verbleibende notwendige Evidence für dieses Finding liefern konnte. Der
Publisher wurde übersprungen. Dies öffnet die Parent-HAProxy-Fixture-Ursache
nicht erneut; sie wird separat als `FND-PARENT-0048` erfasst. Dessen
Korrektur-PR muss integriert und anschließend auf `master` erneut ausgeführt
werden, bevor einer der beiden Records verifiziert werden kann.

## Historie

- 2026-07-22T18:45:02Z — Source- und Sicherheitsregressionsreview bewiesen,
  dass der Framework-Containment-Check beabsichtigt ist; der
  Parent-Fixture-/Invocation-Vertrag besitzt die Korrektur.
- 2026-07-22T18:51:17Z — kanonisches Parent-Finding vor der Reparatur angelegt,
  ohne Control-Abschwächung oder Cross-Repository-Aktion.
- 2026-07-22T20:18:14Z — Parent-only-Reparatur und fokussierte lokale
  Controls bestanden im isolierten Worktree. Das Finding wechselt zu `fixed`;
  Hosted-Exact-Head-Validierung bleibt erforderlich, und es erfolgten keine
  Framework-, MRTS-, Gitlink-, Berechtigungs- oder Master-Aktionen.
- 2026-07-22T21:06:32Z — Der Exact-Head-Fehler des initialen PR #90 wurde
  direkt auf die gemeinsame Legacy-Parent-Assertion aller fünf Runs
  zurückgeführt. Der SHA-spezifische Follow-up ist lokal erneut validiert,
  aber noch nicht committed oder gepusht; ein frischer Exact-Head-Hosted-Zyklus
  bleibt erforderlich.
- 2026-07-22T21:25:24Z — Der SHA-spezifische Follow-up wurde als
  `d99eafd76d9fdbef5b63a19d084fd2d7caff6c08` committed und normal gepusht;
  lokaler, Remote- und PR-Head stimmen überein und alle anwendbaren normalen
  Exact-Head-Actions bestanden. Das getrennte aufgabeneigene Sonar-Quality-
  Gate-`ERROR` wird durch `FND-SONAR-0010` erfasst; es erfolgten kein
  `Update submodules`-Dispatch, keine Master-, Framework-/MRTS-Aktion und
  keine Gitlink-Änderung.
- 2026-07-22T23:02:27Z — Exakter Head `06a4e71` bestand gewöhnliche
  Hosted-Checks und SonarQube-Cloud-Quality-Gate. Dieses Finding bleibt
  `fixed`, nicht `verified`, weil die separat autorisierte read-only-
  `Update submodules`-Candidate-Validierung nicht ausgelöst wurde.
- 2026-07-23T05:15:37Z — Der nun autorisierte Current-Master-Run
  `29981644356` bewahrte fail-closed-Publisher-Verhalten, scheiterte aber am
  separaten PyYAML-Fixture-Syntax-Dependency-Preparation-Schritt.
  `FND-PARENT-0048` besitzt diese Korrektur; dieses Finding bleibt `fixed`,
  nicht verified.
