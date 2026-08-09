# Change Record: Draft-Vertrag des Submodule-Updaters

**Sprache:** [English](CR-20260809-update-submodules-draft-contract.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260809-update-submodules-draft-contract |
| Datum (UTC) | 2026-08-09 |
| Basis-Revision | aa640d5a6d6a41a6ba8d87a0300f995c7392b5df |

## Motivation und Problemstellung

Update-submodules-Run [31317377866](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/31317377866), Publisher-Job
[93254814385](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/31317377866/job/93254814385), validierte Candidate und Parent-master, erkannte Zustand C, prüfte den Updater-Branch, stagete nur den Framework-Gitlink, validierte den Raw-Diff mit vollständigen SHAs, erzeugte einen Maintenance-Commit und aktualisierte den Branch mit explizit gebundener Lease von `fd7e63d7994fd9322c5bbb7862ef283d436c88d5` auf `51db35ddf74da9053553da3c6250685d812a8e00`.

Danach erzeugte der Publisher [PR #261](https://github.com/Easton97-Jens/ModSecurity-conector/pull/261). Base, Head, Head-SHA, Titel, Bot-Autor, Marker, Ein-Datei-Scope und fehlendes Auto-Merge entsprachen dem Updater-Vertrag, GitHub lieferte jedoch `draft=false`. Die abschließende Prüfung wies diesen Ready-Zustand korrekt ab.

Run [31317356208](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/31317356208), actionlint-Job
[93254643817](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/31317356208/job/93254643817), bestand actionlint und die Workflow-YAML-Prüfung, bevor `tests.test_ci_security_workflows` scheiterte: Die Assertion verlangte eine einzeilige `git update-index`-Schreibweise, obwohl der sichere Befehl lediglich Shell-Fortsetzungen verwendete.

## Akzeptanzkriterien

Nur ein exakt identifizierter updater-eigener PR darf konvertiert werden; Ready ist niemals gültiger Endzustand; Konvertierungs- und Readbackfehler bleiben fatal. Die Shell-Layout-Normalisierung muss alle exakten Gitlink-Staging-Argumente erhalten und breites Staging ablehnen.

## Implementierungsentscheidung und Begründung

Die Prüfung offener PRs ist in mutationsfreie Identitätsprüfung und eine finale Prüfung getrennt, die weiterhin `draft=true` verlangt. Das Draft-Enforcement prüft zuerst State, Repository-Kontext, Base, Head, exakte Remote-Head-SHA, Titel, Bot-Autor, genau einen Marker und fehlendes Auto-Merge. Ein Ready-PR wird erst nach erneutem Remote-Head- und vollständigem Identitäts-Readback ausschließlich mit `gh pr ready --undo` geändert; der finale vollständige Readback muss Draft beobachten. Mehrdeutigkeit, Abweichung, Konvertierungsfehler oder erneutes Ready schlagen fail-closed vor `published=true` fehl.

Damit wird auch ein PR-261-ähnlicher Zustand B vor Branchhistorienprüfung und SHA-gebundener Branchaktualisierung wiederhergestellt. Ready wird niemals gültiger Endzustand. Candidate-Validierung, Quick-Check, Pfad-Scope, Commit-Provenienz, Lease-Bindung, Token-Policy und der fail-closed Result-Job bleiben unverändert streng.

Der CI-Vertragstest entfernt nun Backslash-Newline-Fortsetzungen und reduziert Whitespace, ohne Shell auszuführen oder Variablen zu expandieren. Er verlangt weiterhin exakt `git update-index --add --cacheinfo "160000,$CANDIDATE_SHA,$SUBMODULE_PATH"` und weist fehlende Flags, anderen Modus/Pfad sowie breites `git add`-Staging ab.

Framework-/MRTS-Source, Gitlink, Secrets, Berechtigungen, Auto-Merge, Quality Gate und Result-Job-Verhalten bleiben unverändert. Weder PR #261 noch dieser Source-Fix werden durch diese Arbeit gemergt oder auto-gemergt; der separat zu autorisierende Post-Merge-master-E2E bleibt ausstehend.

## Geänderte Dateien

`.github/workflows/update-submodules.yml`, `tests/test_ci_security_workflows.py` und dieses gepaarte Change Record. Kein Gitlink wurde geändert.

## Ausgeführte Befehle

Fokussierte Unittests, CI-Security-Vertrag, YAML-Parser, Python-Compiler, Dokumentationsprüfungen, Security-Tools und Diff-Prüfungen werden lokal ausgeführt. Exakte Ergebnisse stehen im Source-Fix-PR; Framework-abhängige Prüfungen benötigen einen initialisierten Framework-Checkout.

## Security-Auswirkung

Nur ein zweimal identifizierter PR am exakten Remote-Head kann die einzige Mutation `gh pr ready --undo` erreichen. Finaler Draft-Readback ist Pflicht, Auto-Merge bleibt verboten und `published=true` folgt erst nach der Prüfung.

## Runtime-Evidence

Die verlinkten Runs und Jobs sind maßgeblich. PR #261 bleibt während dieses Source-Fixes unveränderte Post-Merge-Recovery-Fixture.

## Bekannte Einschränkungen

Lokale statische Simulation kann GitHub nicht mutieren oder API-Timing reproduzieren. Der Post-Merge-master-Dispatch liegt absichtlich außerhalb dieses Auftrags.

## Verbleibende Risiken

GitHub-Zustand kann zwischen Reads wechseln; wiederholte Identitätsprüfung, Remote-Head-Vergleich und bestehende exakte Lease lassen jede beobachtete Abweichung fail-closed scheitern.

## Nicht ausgeführte Prüfungen mit Begründung

Hosted Exact-Head-Checks und master-E2E existieren erst nach Push/PR und werden anschließend ohne Merge oder master-Dispatch geprüft.

## Finaler Diff- und Review-Status

Der Source-Diff ergänzt keine Berechtigung, Fallback-Credentials, Auto-Merge, allgemeinen Force-Push, Result-Job-Lockerung, Framework-/MRTS- oder Gitlink-Änderung.
