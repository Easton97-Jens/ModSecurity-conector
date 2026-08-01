# FND-PARENT-0018 — Partielle Dependabot-CodeQL-Action-Updates verletzen Immutable-Pin- und Init/Analyze-Konsistenz

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-PARENT-0018` |
| Kategorie | `ci_security_consistency` |
| Repository / Ownership | `parent` / `parent` |
| Priorität | `P1` |
| Severity / Confidence | `medium` / `confirmed` |
| Status / Machbarkeit | `closed` (archiviert) / `already_fixed` |
| Ergebnis / finale Disposition | `no_change` / `already_fixed_on_current_master` |
| Validierte Master-SHA | `c8ca0d92b630c18232b881855c4f5d1482568ea6` |
| Delivery-Disposition | `not_applicable`; keine Produktänderung, kein Commit, Push oder Pull Request erforderlich oder erfolgt |
| Release-Blocker / Security-Relevanz | `false` / `true` |
| Scope | GitHub-Actions-CI / CodeQL-Action-v4.37.1-Batch |

## Zusammenfassung

Die Dependabot-PRs #48, #49 und #50 aktualisierten historisch jeweils nur eine
`github/codeql-action`-Komponente, während die Immutable-Action-Registry auf
v4.37.0 blieb. Ihre exakten Heads belegten sowohl Immutable-Pin- als auch
CodeQL-Konfigurations-/Action-Versionsfehler. Auf der ausgewählten Revision
`c8ca0d92b630c18232b881855c4f5d1482568ea6` pinnt der frühere Commit
`635b8f603f852cff10926cd6f5449e763f6194a4` bereits alle zehn Workflow-
Referenzen und die Registry atomar auf v4.37.1-SHA
`7188fc363630916deb702c7fdcf4e481b751f97a`. Die aktuelle Revalidierung findet
keinen verbleibenden Defekt. Das Finding-Ergebnis lautet `no_change`; die
finale Disposition ist `already_fixed_on_current_master`.

## Beobachtetes und erwartetes Verhalten

Die elf zurückgehaltenen Job-Logs belegen, dass alle drei ursprünglichen
PR-Heads an `test_all_remote_actions_are_immutable_sha_pins` scheiterten, weil
der offizielle SHA `7188fc363630916deb702c7fdcf4e481b751f97a` im Lock fehlte.
PR #48 verwendete `init` v4.37.0 mit `analyze` v4.37.1; PR #50 belegte die
umgekehrte Richtung. Beide CodeQL-Jobs meldeten eine Konfigurations-/Action-
Versionsabweichung. Die aktuelle Revision enthält keine gemischte abgegrenzte
Referenz: Jede CodeQL-Action-Verwendung und ihr Registry-Eintrag lösen bei
unveränderten bestehenden Kontrollen auf ein offizielles unveränderliches
Release auf.

## Auswirkung

Ein einzelnes Mergen würde eine bekannte ungültige CI-Security-Konfiguration
erzeugen. Dies ist ein CI-/Supply-Chain-Konsistenzdefekt; ein Connector-Runtime-
Exploit wird nicht behauptet.

## Remediation und Validierung

Der historische Ersatz aktualisierte alle zehn Referenzen und den zugehörigen
Registry-Eintrag auf den offiziellen v4.37.1-SHA
`7188fc363630916deb702c7fdcf4e481b751f97a`. Diese Revalidierung führte den
Immutable-Pin-Vertrag, Actionlint mit ShellCheck, Offline-Zizmor sowie sichere/
unsichere Zizmor-Kontrollen erfolgreich erneut aus. Die Exact-Head-CodeQL-,
Workflow- und SonarQube-Cloud-Checks von PR #52 bestanden; auch die CodeQL-
und Actions-Checks der ausgewählten Revision bestanden. Es ist keine neue
Source-Änderung erforderlich oder vorgenommen; Delivery ist
`not_applicable`: Kein Commit, Push oder Pull Request ist erforderlich oder
erfolgt.

Das zurückgehaltene bereinigte Exact-Head-Log-Archiv ist
`evidence/dependabot-failed-job-logs-retained.tar.gz`, SHA-256
`78e1f5213915163acc279e61885451e54a10f1021efb816c66fc694a4b44a8a3`.

## Administrativer Abschluss und Plan-Disposition

Der Lifecycle-Status ist erst nach dem bereits dokumentierten Zustand
`verified` auf `closed` gesetzt: Zur verfügbaren Abschluss-Evidence gehören
zurückgehaltene exakte ursprüngliche PR-#48/#50-Evidence, der gemergte
Ersatz-PR #52, die aktuelle Master-Validierung und die legitimen Kontrollen.
Der frühere Worktree-Plan wurde mit SHA-256
`3d6cd95176279b513e1cc7f426a54a7f1feea4c263a84731f493518a0aea0e08`
geprüft und nicht aufbewahrt. Er enthält nur operative Planungsfakten, die
bereits im kanonischen Finding-Record und im zurückgehaltenen
Validierungs-Receipt
`/var/tmp/codex/ModSecurity-conector/runs/20260718T080726Z-fnd-parent-0018-4dd4e268/evidence/fnd-parent-0018-no-change-validation.md`
(SHA-256 `728c55f02d52bc394207e81ccb79bbc47ecc89a39ed430b4b86b54f784cd0233`)
enthalten sind: Source-to-Sink-Nachweis, beide Mixed-Version-Richtungen,
aktuelle Gegen-Evidence, Kontrollen, PR-#52-/aktuelle-CI-Evidence,
Sonar-Abgrenzung und die No-Delivery-Begründung.

## Analoge Dependabot-Action-Transaktion vom 2026-07-21

Dieselbe atomare Immutable-Pin-/Lock-Membership-Invariante trat außerhalb des
historischen CodeQL-v4.37.1-Scopes dieses Findings erneut auf. Dependabot-PR
#67 aktualisierte `actions/setup-python` auf v7.0.0 und PR #68
`actions/checkout` auf v7.0.1, aber jeder exakte Bot-Head scheiterte am
Immutable-Action-Vertrag, weil der zugehörige offizielle SHA im geprüften Lock
fehlte. Die task-eigenen atomaren Ersetzungen #75 und #76 aktualisierten jede
betroffene Workflow-Referenz zusammen mit genau einem passenden Lock-Eintrag;
beide exakten Heads bestanden die sechs strikten Protected-Branch-Contexts,
SonarQube Cloud mit null neuen Issues und null neuen Hotspots sowie die
Review-Thread-Anforderung vor normalen geschützten Squash-Merges.

Ersetzung #75 wurde als `5c26ffb698a892ffe83b7aa1749a456eae10b956` und #76
als aktueller Master `2ade0d40983b7af21a65b8cd2884866b85626393` gemergt.
Letzterer hat 15 erfolgreiche GitHub-Actions-Workflow-Runs sowie 19
erfolgreiche und zwei erwartbar übersprungene terminale Check-Runs. Sein
einziger fehlschlagender Check ist die separate bereits bestehende
`FND-SONAR-0001`-Sonar-Baseline: dieselben drei unreviewten
`python:S5332`-Hotspots, Security Rating `5` und Hotspot-Review `0.0%`. Die
ursprünglichen Dependabot-PRs #67 und #68 wurden von `dependabot[bot]`
unmerged geschlossen; diese Task hat sie nicht geschlossen. Es wird keine neue
kanonische ID vergeben, weil dies dieselbe unabhängig behebbare atomare
Workflow-Pin-/Lock-Transaktionsinvariante ist. Diese Wiederkehr ändert nicht
rückwirkend die historische `no_change`-Delivery-Disposition der ursprünglichen
CodeQL-spezifischen Evidence.

## Restrisiko und Historie

GitHub meldet das offizielle annotierte v4.37.1-Tag als `unsigned`;
Provenienz ist auf offizielles Repository, Release, Tag-Ziel und vollständigen
SHA begrenzt. Der aktuelle `master`-SonarQube-Cloud-Fehler ist ein identischer
bereits bestehender Zustand, der als `FND-SONAR-0001` verfolgt wird, und keine
FND-PARENT-0018-Regression. `FND-SONAR-0001` bleibt offen und `blocked`; dieser
Abschluss dispositioniert oder verändert ihn nicht. Es wird kein Risiko
akzeptiert.

- `2026-07-17T18:16:59Z`: exakte ursprüngliche Heads und Fehler
  zurückgehalten und klassifiziert.
- `2026-07-17T18:45:07Z`: atomare lokale Kontrollen bestanden; externe PR-
  und `master`-Evidence bleibt ausstehend.
- `2026-07-18T08:17:17Z`: aktuelle Revision mit `no_change` anhand von
  aktueller Source, fokussierten lokalen Kontrollen, zurückgehaltener
  PR-#48/#50-Mixed-Version-Evidence und Exact-SHA-GitHub-Checks revalidiert.
  Es wurde keine Produktänderung vorgenommen.
- `2026-07-18T09:17:25Z`: administrativ mit Ergebnis `no_change` und finaler
  Disposition `already_fixed_on_current_master` geschlossen; es erfolgte keine
  Delivery-Aktion. Der frühere Worktree-Plan wurde geprüft und nicht
  aufbewahrt, weil das checksum-verifizierte zurückgehaltene
  Validierungs-Receipt die ausreichende kanonische technische Evidence ist.
- `2026-07-21T08:05:05Z`: eine analoge Dependabot-Action-Pin-Wiederkehr wurde
  in dieses atomare Immutable-Pin-/Lock-Membership-Finding dedupliziert. Die
  exakten Bot-Heads #67/#68 hatten keinen passenden geprüften Lock-Eintrag;
  die task-eigenen Ersatz-PRs #75/#76 bestanden alle strikten Exact-Head-
  Contexts, Sonar-PR-Gates und Thread-Controls vor geschützten Squash-Merges zu
  `5c26ffb698a892ffe83b7aa1749a456eae10b956` und
  `2ade0d40983b7af21a65b8cd2884866b85626393`. Die aktuelle Master-Actions-
  Evidence ist erfolgreich; der separate Sonar-Fehler bleibt
  `FND-SONAR-0001`. Der Bot schloss die ursprünglichen PRs #67/#68 unmerged;
  es erfolgten keine Task-Schließung, kein Bypass, kein Force, keine Framework-
  oder MRTS-Änderung, keine Gitlink-, Ruleset- oder Scanner-Änderung.
