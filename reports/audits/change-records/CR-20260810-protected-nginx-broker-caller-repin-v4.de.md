# Change Record

**Sprache:** [English](CR-20260810-protected-nginx-broker-caller-repin-v4.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260810-protected-nginx-broker-caller-repin-v4 |
| Datum (UTC) | 2026-08-10 |
| Basis-Revision | 7a9240d35e50475cc1a381fa103b0bb5cca2bee3 |
| Vorheriger geschützter Broker-SHA | 409caa5b9664bcb8e1919d35684575e00a959f6a |
| Aktiver geschützter Broker-SHA | 7a9240d35e50475cc1a381fa103b0bb5cca2bee3 |
| Broker-Framework-Gitlink | 03880bf66b3905940466ff10b3a431a27ecc6b26 |
| Broker-Verfügbarkeit | [PR #273](https://github.com/Easton97-Jens/ModSecurity-conector/pull/273) mergte Broker-Commit `7a9240d35e50475cc1a381fa103b0bb5cca2bee3` um 2026-08-10T14:13:09Z |
| Delivery-PR | Draft [PR #274](https://github.com/Easton97-Jens/ModSecurity-conector/pull/274), initial beobachtet bei `9a54f316248edf22b3e43ccfbb3310a651253921` |

## Motivation und Problemstellung

Die Trusted-Broker-Guides müssen das Caller-Tupel nennen, das der getrennte
Phase-B-Caller-Repin-Commit `9a54f316248edf22b3e43ccfbb3310a651253921`
auswählt. PR #273 mergte Broker-Commit
`7a9240d35e50475cc1a381fa103b0bb5cca2bee3` nach `master` und machte diese
Broker-Revision verfügbar, doch sein commitierter Caller-Workflow/-Helper
pinnt weiterhin `409caa5b9664bcb8e1919d35684575e00a959f6a`. Der Phase-B-
Commit repinnt den Caller auf Broker `7a9240d35e50475cc1a381fa103b0bb5cca2bee3`
mit Framework-Gitlink `03880bf66b3905940466ff10b3a431a27ecc6b26`; Draft
PR #274 trägt die Delivery. Historische Change Records bleiben unverändert
erhalten.

## Akzeptanzkriterien

Die englische und deutsche Guide enthalten denselben aktiven Broker-SHA-40 und
Framework-Gitlink in beiden Reusable-Workflow-Beispielen und im Caller-Tupel.
Sie unterscheiden korrekt zwischen der durch PR #273 bereitgestellten Broker-
Revision und dem durch den getrennten Phase-B-Commit und Draft PR #274
ausgewählten Tupel, ohne Merge, Master-Checks oder lokale Validierung als
geschützte Runtime-Evidence zu behandeln. Dieser Record und sein deutsches Gegenstück verlinken
sich wechselseitig, weisen nur beobachteten Phase-B-Lokal-, Hosted- und
Lifecycle-Status aus und enthalten weder privaten Pfad noch Secret.

## Implementierungsentscheidung und Begründung

Technische Entscheidung: Phase-B synchronisiert das unveränderliche Caller-
Tupel über Caller-Workflow, Caller-Helper, Python-Version-Contract-Checker,
fokussierte Tests, gepaarte Trusted-Broker-Guides und diesen gepaarten Change
Record. Die unveränderliche `uses`-Referenz und `protected_broker_sha` bleiben
die privilegierte Auswahlgrenze des Callers; es wird kein Branch oder
beweglicher Ref eingeführt. Der Framework-Wert ist der exakte
Mode-`160000`-Gitlink der Broker-Revision. Die Synchronisierung ändert weder
Verhalten, Admission-Gate, Permission, Schema noch Root-Command. PR #273
liefert den verfügbaren Broker-Commit; sein commitierter Caller bleibt bei
`409caa5b9664bcb8e1919d35684575e00a959f6a`, und der getrennte Phase-B-Commit
führt den Caller-Repin unter Draft PR #274 aus. Der Record trennt diesen
Zustand, die beobachteten PR-273-Master-Checks und den getrennten,
nur-dispatchbaren geschützten Lifecycle, der durch gewöhnliche `push`-Workflows
nicht belegt ist.

## Security-Auswirkung

Die Änderung verändert keine Runtime-Kontrolle. Sie bewahrt die dokumentierte
fail-closed-Auswahl des unveränderlichen Brokers und behauptet nicht, dass
Root-Admission, NGINX-Ausführung, CRS-Verarbeitung, Artefakt-Readback oder
Cleanup erfolgreich waren.

## Geänderte Dateien

- docs/security/trusted-nginx-root-broker.md
- docs/security/trusted-nginx-root-broker.de.md
- .github/workflows/run-protected-nginx-root-broker.yml
- ci/runtime/broker/protected_nginx_broker_caller.py
- ci/checks/common/check-python-version-contract.py
- tests/test_ci_security_workflows.py
- tests/test_nginx_root_broker.py
- reports/audits/change-records/CR-20260810-protected-nginx-broker-caller-repin-v4.md
- reports/audits/change-records/CR-20260810-protected-nginx-broker-caller-repin-v4.de.md

## Tests und tatsächliche Ergebnisse

Die exakte-master-Hosted-Evidence des Broker-Verfügbarkeits-Commits wurde mit
`rtk proxy gh run list --repo Easton97-Jens/ModSecurity-conector --commit 7a9240d35e50475cc1a381fa103b0bb5cca2bee3 --limit 100 --json databaseId,name,status,conclusion,workflowName,event,headSha,url,createdAt,updatedAt`
beobachtet. Alle aufgeführten Läufe waren `push`-Läufe auf genau diesem Head
und endeten mit `success`:

| Workflow | Run-ID |
| --- | ---: |
| protocol-contract | 31396967424 |
| verified-report-governance | 31396967538 |
| Security workflow lint | 31396967572 |
| test-lighttpd | 31396967725 |
| test-envoy | 31396967530 |
| OpenSSF Scorecard | 31396968045 |
| test-haproxy | 31396967380 |
| test-traefik | 31396968058 |
| test-common | 31396967586 |
| test-nginx | 31396967630 |
| lint | 31396967719 |
| test-apache | 31396967342 |
| quick-framework-check | 31396967765 |
| CodeQL security analysis | 31396967460 |

Die korrigierte Bilingual-Prüfung meldete keine Diagnose für einen der beiden
v4-Records oder eine der beiden Trusted-Broker-Guides; ihre verbleibenden
Fehler sind die 20 bereits bestehenden fehlenden Framework-Gitlink-Ziele
außerhalb dieses Task-Worktrees. Der Change Record fügt über den oben
aufgeführten vollständigen neun-Dateien-Phase-B-Scope hinaus keinen weiteren
Source- oder Testpfad hinzu.

Die tatsächliche lokale Phase-B-Validierung bestand 109 Tests in 9.253s mit
den Testmodulen für geschützten Caller, Broker, Workflow, CI-Security-Workflow
und Python-Version-Contract. `check-ci-security-contract` bestand außerdem
seine 26 CI-Security-Tests plus validate-only-actionlint/zizmor/gitleaks
locks. Der eigenständige Python-Version-Contract-Befehl endete nur wegen
unveränderter aktueller-`master`-Inventarverletzungen in
`verified-report-governance`, `ci-security-codeql` trusted-go-version,
Apache/HAProxy und `update-workflow-tools` mit Exit 2; dies ist Evidenz einer
nicht bestandenen Baseline-Prüfung und keine Phase-B-Pin-
Verletzung.

## Ausgeführte Befehle

- `rtk proxy gh pr view 273 --repo Easton97-Jens/ModSecurity-conector --json number,url,state,isDraft,mergedAt,mergeCommit,headRefName,headRefOid,baseRefName,statusCheckRollup,reviewDecision` — PR #273 wurde als `MERGED` nach `master` beobachtet, mit Head `bf838c3985e574756870498de176fd3294cba028`, resulting-SHA `7a9240d35e50475cc1a381fa103b0bb5cca2bee3` und Merge-Zeit `2026-08-10T14:13:09Z`.
- `rtk proxy gh run list --repo Easton97-Jens/ModSecurity-conector --commit 7a9240d35e50475cc1a381fa103b0bb5cca2bee3 --limit 100 --json databaseId,name,status,conclusion,workflowName,event,headSha,url,createdAt,updatedAt` — PASS: Die oben genannten 14 exakten Head-`push`-Läufe endeten mit `success`.
- `rtk proxy gh pr view 274 --repo Easton97-Jens/ModSecurity-conector --json number,state,isDraft,baseRefName,headRefName,headRefOid,mergeable,mergeStateStatus,reviewDecision,url,autoMergeRequest,reviews` — Draft PR #274 wurde als `OPEN` gegen `master`, initial bei `9a54f316248edf22b3e43ccfbb3310a651253921`, `MERGEABLE`/`CLEAN`, ohne Reviews und ohne Auto-Merge-Request beobachtet.
- `rtk proxy gh api 'repos/Easton97-Jens/ModSecurity-conector/commits/9a54f316248edf22b3e43ccfbb3310a651253921/check-runs?per_page=100' -H 'Accept: application/vnd.github+json' --jq '[.check_runs[] | {status, conclusion}] | group_by([.status, .conclusion]) | map({status: .[0].status, conclusion: .[0].conclusion, count: length})'` — 35 terminale Current-Head-Checks wurden beobachtet: 29 `success` und 6 scope-bedingte `skipped`; CodeQL endete erfolgreich.
- `rtk proxy gh api repos/Easton97-Jens/ModSecurity-conector/check-runs/93500714235 --jq '{status, conclusion, title: .output.title, summary: .output.summary, details_url}'` — SonarCloud Code Analysis endete mit `success`; sein Quality Gate bestand mit 0 New Issues, 0 Accepted Issues und 0 Security Hotspots für den initialen Head `9a54f316248edf22b3e43ccfbb3310a651253921`.
- `rtk proxy make check-bilingual-docs` — erster Lauf BLOCKIERT wegen fehlender erforderlicher Überschriften dieses neuen Paars; korrigierter Wiederholungslauf nur durch 20 bereits bestehende fehlende Framework-Gitlink-Ziele BLOCKIERT und ohne Diagnose für einen der beiden v4-Records oder eine der beiden Trusted-Broker-Guides.
- `rtk proxy make check-doc-links` — nur durch 16 bereits bestehende fehlende Framework-Gitlink-Ziele außerhalb dieses Scopes BLOCKIERT; es wurde keine scopierte Pfad-Diagnose gemeldet.
- `rtk proxy git diff --check -- docs/security/trusted-nginx-root-broker.md docs/security/trusted-nginx-root-broker.de.md` — PASS.
- `rtk proxy git diff --no-index --check /dev/null <jeder neue v4 Record>` — PASS für Whitespace; die New-File-Differenz ist erwartet.
- `rtk proxy rg -n <alter/neuer Broker-SHA, Framework-SHA und PR-Head> <vier scopierte Dateien>` — PASS: Beide Guides enthalten nur den aktiven Broker-SHA und Framework-Gitlink; der vorherige SHA bleibt nur als historische Identität in diesem neuen Record-Paar.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_protected_nginx_broker_caller tests.test_nginx_root_broker tests.test_nginx_root_broker_workflow tests.test_ci_security_workflows tests.test_python_version_contract` — PASS: 109 Tests in 9.253s.
- `rtk proxy make PYTHON=python3 check-ci-security-contract` — PASS: 26 CI-Security-Tests plus validate-only-actionlint/zizmor/gitleaks locks.
- `rtk proxy make PYTHON=python3 check-python-version-contract` — Exit 2 nur wegen unveränderter aktueller-`master`-Inventarverletzungen in `verified-report-governance`, `ci-security-codeql` trusted-go-version, Apache/HAProxy und `update-workflow-tools`; Evidenz einer nicht bestandenen Baseline-Prüfung, keine Phase-B-Pin-Verletzung.

## Runtime-Evidence

Es wurde keine geschützte resulting-Caller-Phase-B-Lifecycle-Evidence
beobachtet. Die obige Exact-Head-Liste enthält nur die 14 gewöhnlichen
`push`-Workflows für den Broker-Verfügbarkeits-Commit; sie zeigt keinen
erfolgreichen Dispatch von `Protected NGINX Root Broker Lifecycle` für den
Caller-Repin von Draft PR #274 und kann dessen Root-Master-/Nicht-root-Worker-,
CRS-, Artefakt- oder Cleanup-Verhalten nicht beweisen.

## Nicht ausgeführte Prüfungen mit Begründung

Für diesen Phase-B-Caller-Repin wurden kein geschützter Lifecycle-Dispatch,
keine Root-Aktion, kein NGINX-Start, kein CRS-Fetch, kein Audit, kein
Artefakt-Readback, kein Stop und kein Cleanup ausgeführt. Diese Vorgänge
benötigen den getrennten geschützten GitHub-hosted-Workflow und folgen nicht
aus PR #273 oder seinen Exact-master-Checks.

## Bekannte Einschränkungen

Dieser Record dokumentiert den vollständigen Phase-B-Caller-Repin-Scope und
die oben beobachtete lokale Validierung. PR #273 stellte nur die Broker-
Verfügbarkeit her. Für den initialen Draft-PR-#274-Head
`9a54f316248edf22b3e43ccfbb3310a651253921` liegt die oben festgehaltene
Hosted-Check- und SonarQube-Cloud-Evidence vor, sie deckt aber keinen späteren
reinen Dokumentations-Delivery-Commit ab, beweist weder finalen Exact-Head-
Branch-Protection- noch Review-/Merge-Status und etabliert keinen
resulting-Caller-Lifecycle-Befund.

## Verbleibende Risiken

Das Caller-Tupel von Draft PR #274 benötigt weiterhin einen getrennten
resulting-master-geschützten Lifecycle, um Runtime-Evidence für beide
`no-crs`- und `owasp-crs`-Profile zu erzeugen.

## Finaler Review-Status

Der scopierte Review aktiver Literale, des zweisprachigen Paars, der
wechselseitigen Links und des Whitespace ist abgeschlossen. Globale
Dokumentationsprüfungen bleiben wegen der bereits bestehenden,
unmaterialisierten Framework-Ziele blockiert. Die beobachtete lokale Phase-B-
Validierung und die Hosted-Evidence des initialen PR-Heads sind oben
festgehalten; diese Evidence bleibt von nicht beobachteter Protected-
Lifecycle-Evidence getrennt, und ein finaler Delivery- oder Lifecycle-Befund
wird nicht behauptet. Dieses Dokument selbst autorisiert weder Staging,
Commit, Push, Pull Request noch Merge.

## Finaler Diff- und Review-Status

Der Phase-B-Scope sind die oben aufgeführten neun Pfade; der scopierte
Whitespace-Review für Guides/Records ist sauber. Historische Records,
Framework-Inhalt, MRTS-Inhalt und Gitlinks werden durch diesen Caller-Repin
nicht geändert.
