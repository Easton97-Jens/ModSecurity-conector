# FND-FRAMEWORK-0046 — Framework-PR #42: OSV-Trusted-Base-Interpreter- und Lock-ABI-Mismatch während der CPython-3.14-Umstellung

## Identität

| Feld | Wert |
| --- | --- |
| Kategorie | ci_failure |
| Repository / Ownership | framework / framework |
| Priorität / Schweregrad / Konfidenz | P1 / not_applicable / confirmed |
| Status / Feasibility | verified / already_fixed |
| Release-Blocker / Sicherheitsrelevanz | false / true |
| Historischer fehlschlagender Head | e0564d219980d62bc37162ac6c11641f289f1b71 |
| Exakter behobener Head | 2930e04e1558b5b10bdeb87a76abb077a2085566 |
| Exakter gemergter PR-Head | dc6cf411e78b3f37f1e4be52edef59894560b1ae |
| Resulting Framework Master / Merge-Commit | 935cf14c676a24672be5c336e92cd13457cc35c8 |
| Vertrauenswürdige Basis | f73f8842f45318e2df8aff1d31855eeb7c20a22f |

## Zusammenfassung

Der historische OSV-Pull-Request-Head-Job von Framework-PR #42 scheiterte vor
seinem Dependency-Vergleich. Der exakte Head
e0564d219980d62bc37162ac6c11641f289f1b71 wählt CPython 3.14.6 aus
begrenzten PR-Head-Daten und installiert danach requirements-ci.lock der
ausgecheckten vertrauenswürdigen Basis
f73f8842f45318e2df8aff1d31855eeb7c20a22f. Dieser Lock enthält einen
CP313-only-PyYAML-Hash; deshalb weist pip das heruntergeladene CP314-Wheel
unter Hash-Enforcement korrekt zurück. Der Fehler ist ein Interpreter-/Lock-
ABI-Mismatch an der Trusted-Base-Bootstrap-Grenze; er beweist nicht, dass das
geprüfte CP314-Lock-Tupel ungültig ist.

Dieses Finding erfasste historisch den Fall einer fehlenden
Trusted-Base-.python-version. Die exact-SHA-bound Trusted-Base-
CPython-3.13.14-Bridge ist jetzt committet und in exaktem Head
2930e04e1558b5b10bdeb87a76abb077a2085566 enthalten. Dessen aktueller OSV-
Pull-Request-Head-Check besteht zusammen mit den übrigen aktuellen PR-Checks,
SonarQube Cloud besteht und es gibt weder Review noch Inline-Kommentar. Das
aufbewahrte Verification-Receipt ist framework-pr42-2930e04-hosted-verification.md,
SHA-256 4f7de2c315aa3f262b7a237b7228d5e682529065b28c8ce1046f2519752418b0.
PR #42 wurde danach normal um `2026-07-23T07:41:13Z` mit exaktem Merge-Commit
und resultierendem Framework-Master
935cf14c676a24672be5c336e92cd13457cc35c8 gemergt. Seine Parents sind die
vertrauenswürdige Basis f73f8842f45318e2df8aff1d31855eeb7c20a22f und der
exakt gemergte PR-Head dc6cf411e78b3f37f1e4be52edef59894560b1ae; der
resultierende Tree entspricht dem geprüften PR-Head-Tree. Das aufbewahrte
Resulting-Master-Receipt framework-pr42-20260723-postmerge-verification.md,
SHA-256 0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1,
zeichnet acht erfolgreiche GitHub-Actions-Workflows für den exakten Master
auf. Der PR-only-Job `pull-request-head` wird für das Push-Event erwartbar
übersprungen und scheitert nicht. Zusammen mit dem früheren Exact-PR-Head-
OSV-Pass verifiziert dies die Reparatur. Das Finding ist `verified`, nicht
`closed`.

## Beobachtetes und erwartetes Verhalten

Historischer GitHub-Actions-OSV-Run 29956021487, Job 89045175516, wählte CPython 3.14.6 und
versuchte die Trusted-Base-Lock-Installation. Der Lock erwartete CP313-Digest
0f29edc409a6392443abf94b9cf89ce99889a1dd5376d94316ae5145dfedd5d6; pip
lud ein CP314-Wheel mit Digest
c458b6d084f9b935061bc36216e8a69a7e293a2f1e68bf956dcd9e6cbcd143f5 und
wies es unter Hash-Enforcement korrekt zurück.

Der OSV-Job muss jede Trusted Base mit ihrem geprüften ABI-kompatiblen
Interpreter-/Lock-Paar verbinden und zugleich Trusted-Base-Checkout, Base/Head-
SHA-Validierung, Read-only-Berechtigungen, begrenzte Manifest-Reads sowie
Nichtausführung und Nicht-Checkout von untrusted PR-Content bewahren. Für die
exakte Trusted Base f73f8842f45318e2df8aff1d31855eeb7c20a22f darf die Bridge
nur bei fehlendem Selector das geprüfte CPython-3.13.14-Paar wählen; jede
andere Base, jeder vorhandene CP313-Selector oder fehlende Selector muss fail
closed statt einen generischen Fallback zu erben.

## Grundursache und vorgeschlagene Remediation

Die frühere Remediation behandelte die PR-Head-.python-version korrekt als
begrenzte SHA-verifizierte Daten statt den PR-Head auszuchecken oder
auszuführen. Bei e0564d219980d62bc37162ac6c11641f289f1b71 wurde ihre Auswahl
von CPython 3.14.6 jedoch zur Installation des CP313-only-Locks der Trusted
Base verwendet. Der Workflow koppelte damit eine Trusted-Base-Lock-Installation
an einen PR-Head-Interpreter statt an ein exaktes Trusted-Base-
Interpreter-/Lock-Paar.

Die implementierte Remediation ist eine exact-SHA-bound
Trusted-Base-CPython-3.13.14-Bridge. Sie muss nur die Trusted Base
f73f8842f45318e2df8aff1d31855eeb7c20a22f bei fehlendem Selector matchen,
ihr geprüftes CPython-3.13.14-Bootstrap-Paar wählen und für jede andere Base
oder jeden anderen Selector-Zustand fail closed sein. Sie
muss Trusted-Base-Checkout, Base/Head-SHA-Prüfungen, Read-only-Credentials,
begrenzte data-only-PR-Head-Reads und die No-Untrusted-Code-Execution-Grenze
erhalten. Sie darf weder den PR-Head-Lock installieren, Hashes lockern,
Credentials ergänzen noch einen generischen Interpreter-Fallback einführen.

## Evidence und Reproduktion

| Evidence | Wert |
| --- | --- |
| Aktuelles Receipt | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/framework-pr42-e056-hosted-ci-failures.md |
| Aktuelle Receipt-SHA-256 | 5940246feb917a3d83a7372ef09f2f54673cf506ec24d457d5dec5dfeaa381be |
| Aktueller Receipt-Run / Beobachtungsdatum | 20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e / 2026-07-22 |
| Historischer ursprünglicher Fehler | /var/tmp/codex/ModSecurity-conector/runs/20260722T145132Z-framework-pr-39-41-master-integration-9a3c7dc7/evidence/pr39-osv-trusted-base-python-version-failure.md |
| Historische ursprüngliche SHA-256 | a0d6e64e4acfaabab6cda79704a28f3e9a7257897e0ebe8fc3e168152cc9bf76 |
| Historische lokale Security-Validierung | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/security-diff/consolidation-local-security-closure.md |
| Historische Local-Validation-SHA-256 | 6a5f626d9f574841484055431c33fb8dcfc47bc0029d641ea48359c1a9764719 |
| Historisches Commit-Receipt | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/security-diff/consolidation-commit-receipt.md |
| Historische Commit-Receipt-SHA-256 | c07815638b747cb80002db2f34ff18028d80d0241eb7c7248488d5c8fe6f9e1c |
| Historisches Hosted-Pass-Receipt | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/delivery/pr42-exact-head-hosted-verification.md |
| Historische Hosted-Pass-SHA-256 | 07d30f93ab9bda5fb03fb22b20b9755aba2b8567b67678a34ec3ff7927bcb853 |
| Resulting-Master-Receipt | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/framework-pr42-20260723-postmerge-verification.md |
| Resulting-Master-Receipt-SHA-256 | 0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1 |
| Resulting Master / gemergter PR-Head | 935cf14c676a24672be5c336e92cd13457cc35c8 / dc6cf411e78b3f37f1e4be52edef59894560b1ae |
| Resulting-Master beobachtet am | 2026-07-23T07:51:09Z |

Das aktuelle Receipt bewahrt Run-/Job-Fakten, aber weder Producer-Befehl noch
Beobachtungszeit. Dieser Record bewahrt deshalb 2026-07-22 exakt und erfindet
keinen präziseren Hosted-Timestamp.

Reproduktion der beobachteten Bedingung:

    rtk gh run view 29956021487 --repo Easton97-Jens/ModSecurity-test-Framework --log-failed
    rtk git -C <task-worktree> show f73f8842f45318e2df8aff1d31855eeb7c20a22f:requirements-ci.lock
    rtk git -C <task-worktree> show e0564d219980d62bc37162ac6c11641f289f1b71:.github/workflows/ci-security-osv.yml

## Akzeptanzkriterien und Validierungsplan

1. Nur die exakte Trusted Base f73f8842f45318e2df8aff1d31855eeb7c20a22f mit
   fehlendem Selector wählt ihre SHA-bound geprüfte CPython-3.13.14-Bridge;
   alle anderen Base/Selector-Zustände, einschließlich eines vorhandenen
   Selectors bei dieser Base oder eines fehlenden Selectors bei jeder anderen
   Base, scheitern fail closed.
2. Der OSV-Job behält Trusted-Base-Checkout, validiert beide SHAs, vergleicht
   begrenzte Manifeste und checkt PR-Head-Code weder aus noch führt er ihn aus.
3. Die CP313-Lock/CP314-Head-Mismatch- und
   Absent-Base-Version-File-Pfade besitzen fokussierte Framework-
   Workflow-/Version-Contract-Regression-Coverage.
4. Exakter PR-Head 2930e04e1558b5b10bdeb87a76abb077a2085566 besteht OSV
   pull-request-head und besitzt frische Exact-Head-Checks, Sonar- sowie
   Review/Thread-Evidence.
5. Erfüllt: PR #42 wurde normal als
   935cf14c676a24672be5c336e92cd13457cc35c8 gemergt, und das
   Resulting-Master-Receipt erfasst erfolgreiche GitHub-Actions-Workflows für
   den exakten Master. Der PR-only-Job `pull-request-head` wird beim Push-
   Event korrekt übersprungen.

Der exakte Bridge-Diff, fokussierte Workflow-/Version-Contract-Tests und der
neue Hosted-OSV-Run sind für den behobenen PR-Head aufgezeichnet. Legitimate
Controls bleiben gewahrt: Base/Head-Manifest-Reads bleiben begrenzt und
SHA-verifiziert, Hash-Enforcement bleibt erhalten, kein PR-Head-Lock wird
installiert und es kamen keine write-fähigen Credentials hinzu.

## Abhängigkeiten, Delivery-Limitierungen und Restrisiko

Für diese verifizierte OSV-Reparatur gibt es keine offene Remediation-
Abhängigkeit oder keinen Blocker. Der normale PR-#42-Merge und die
Resulting-Master-Evidence erfüllen den Lifecycle-Nachweis für dieses Finding.
Verwandte Findings sind FND-FRAMEWORK-0044, FND-FRAMEWORK-0049,
FND-FRAMEWORK-0051, FND-SONAR-0009, FND-SONAR-0002 und FND-GITHUB-0007.

Für diesen OSV-Defekt ist kein Risiko akzeptiert. Die Resulting-Master-Sonar-
Bedingung (`FND-SONAR-0002`) und die gequeue-te Cloudflare-Suite
(`FND-GITHUB-0007`) sind getrennte, vom Nutzer für PR #42 begrenzte Delivery-
Limitierungen. Ihre globalen Findings bleiben unabhängig getrackt; keine der
beiden Bedingungen reproduziert oder blockiert diese verifizierte OSV-
Reparatur. Es gab keine Parent-Gitlink- oder MRTS-Aktion. Das Finding ist
verified und absichtlich nicht closed.

## Historie

- 2026-07-23T07:51:09Z — verified_after_pr42_normal_merge_and_resulting_master:
  PR #42 wurde um 2026-07-23T07:41:13Z normal als Framework-Master
  935cf14c676a24672be5c336e92cd13457cc35c8 aus Vorgänger
  f73f8842f45318e2df8aff1d31855eeb7c20a22f und gemergtem Head
  dc6cf411e78b3f37f1e4be52edef59894560b1ae integriert. Das aufbewahrte
  Postmerge-Receipt SHA-256
  0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1
  erfasst acht erfolgreiche GitHub-Actions-Workflows für den exakten Master;
  der PR-only-pull-request-head-Job wird beim Push-Event korrekt übersprungen.
  Mit dem vorherigen Exact-PR-Head-OSV-Pass wechselt das Finding von fixed zu
  verified, nicht closed. FND-SONAR-0002 und FND-GITHUB-0007 bleiben getrennte
  begrenzte Delivery-Limitierungen, keine Blocker dieser Reparatur.
- 2026-07-22T22:35:46Z — framework_pr42_2930_exact_head_osv_fixed:
  Exakter Head 2930e04e1558b5b10bdeb87a76abb077a2085566 bestand den
  behobenen OSV-Pull-Request-Head-Control und alle aktuellen PR-Checks. Die
  aufbewahrte Verification-Receipt-SHA-256 ist
  4f7de2c315aa3f262b7a237b7228d5e682529065b28c8ce1046f2519752418b0.
  Die Trusted-Base-, Read-only- und No-Untrusted-Code-Execution-Grenze bleibt
  intakt. Der Status ist nur fixed; es erfolgten kein Master-Merge, keine
  Resulting-Master-Evidence, keine Parent-Gitlink-Aktion und keine MRTS-Aktion.
- 2026-07-22T15:07:13Z — historisch
  exact_head_ci_failure_reproduced_and_tracked: die ursprüngliche fehlende
  PR-#39-Trusted-Base-.python-version wurde aufgezeichnet.
- 2026-07-22T17:04:03Z — historisch
  consolidation_remediation_locally_fixed: der data-only-PR-Head-Bootstrap-
  Pfad bestand fokussierte lokale Controls.
- 2026-07-22T17:24:06Z — historisch
  consolidation_remediation_committed: dieser lokale Pfad wurde an
  22747d460a9f7be02760edf05c311be376492457 gebunden.
- 2026-07-22T17:42:25Z — historisch
  exact_pr_head_hosted_controls_passed: Head
  1fd3b362e0fed9766c6920e3c7bd1939535850f2 bestand Hosted-OSV; dies ist
  keine aktuelle Verifikation.
- 2026-07-22T21:23:05Z —
  current_e056_trusted_base_interpreter_lock_mismatch_confirmed: das retained
  Receipt erfasst den aktuellen Fehler von e0564d219980d62bc37162ac6c11641f289f1b71
  in Run 29956021487, Job 89045175516.
- 2026-07-22T21:23:05Z —
  sha_bound_cp313_bridge_recorded_as_uncommitted_follow_up: die berichtete
  CPython-3.13.14-Bridge ist nur für exakte Base
  f73f8842f45318e2df8aff1d31855eeb7c20a22f mit fehlendem Selector erlaubt;
  jede andere Base oder jeder andere Selector-Zustand scheitert fail closed.
  Es wird kein fixed-, Hosted-Verification-, Merge- oder Resulting-Master-
  Claim gemacht.
