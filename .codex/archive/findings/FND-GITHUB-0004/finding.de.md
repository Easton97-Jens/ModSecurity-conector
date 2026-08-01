# FND-GITHUB-0004 — Plattformverwaltete GitHub-Advanced-Security-Code-Scanning-AI-Runs schlagen mit einem nicht unterstützten Modell fehl

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-GITHUB-0004 |
| Titel | Plattformverwaltete GitHub-Advanced-Security-Code-Scanning-AI-Runs schlagen mit einem nicht unterstützten Modell fehl |
| Kategorie | github_governance |
| Repository | framework |
| Ownership | github_configuration |
| Priorität | P1 |
| Severity | not_applicable |
| Confidence | confirmed |
| Status | accepted_risk |
| Feasibility | out_of_scope |
| Release-Blocker | true |
| Security-Relevanz | true |

## Zusammenfassung, beobachtetes Verhalten und Auswirkung

GitHubs plattformverwalteter GitHub-Advanced-Security-/Code-Scanning-AI-Workflow schlägt fehl, bevor die angeforderte Analyse abgeschlossen ist, weil sein konfiguriertes Modell nicht unterstützt wird. Dies ist eine GitHub-seitige Runtime-/Konfigurationsbedingung und kein Defekt von Framework-Source, Workflow, Parent-Gitlink oder MRTS. Sie verhindert den Claim, dass die dynamische Security-Kontrolle für einen betroffenen exakten PR-Head bestanden hat; sie darf weder verborgen, waived noch als erfolgreicher Scan dargestellt werden.

Auf Framework-PR #26 mit exaktem Head 63c42e97b86acbae1374efa9f1c4209ce2ce673b endeten dynamischer Run 29680055620 und Check 88174464227 / github-advanced-security mit failure. Sein Processing-Request-(Linux)-Output enthält:

~~~text
The requested model is not supported.
code=model_not_supported
param=model
~~~

Der Run identifiziert sweagent-capi:claude-opus-4.6 als konfiguriertes Modell. Der frühere PR-#25-Head c5e7553cf5f3eb7c5535e392798e03ae21f81981 hat einen separaten fehlgeschlagenen Code-scanning-AI-findings-Run 29659308388; seine verfügbare Annotation lautet nur Process completed with exit code 1. Der neue PR-#25-Head c6ba5e11359d6eb30e8717b766d49697f9bed74f hat einen erfolgreichen dynamischen CodeQL-Run, aber keinen passenden Code-Scanning-AI-Run. Daher darf der alte Fehler nicht als Pass gelten und der fehlende Run nicht als Fehler abgeleitet werden.

Ein betroffener Framework-PR kann keine erfolgreiche GitHub-Advanced-Security-Code-Scanning-AI-Coverage wahrheitsgemäß behaupten. Der Zustand ist ein Release-Readiness- und Security-Evidence-Blocker, getrennt von NGINX-Release-Provenance und regulären aktuellen CodeQL-/SonarCloud-Ergebnissen. Er belegt keine Framework-Code-Vulnerability und autorisiert keinen Workaround in Framework-Security-Workflows.

## Erwartetes Verhalten, betroffener Scope, Voraussetzungen und Reproduktion

GitHub muss ein unterstütztes Modell bereitstellen oder ein autorisierter Owner muss eine Plattform-Konfigurationsentscheidung treffen und belegen. Danach muss der plattformverwaltete Check für jeden anwendbaren exakten aktuellen Head erfolgreich laufen, ohne die Kontrolle abzuschwächen, zu unterdrücken oder falsch darzustellen.

Es ist keine fehlerhafte Framework-Source-Datei identifiziert. Betroffene externe Symbole sind GitHub Advanced Security, dynamic/agents/github-advanced-security, github-advanced-security, Processing Request (Linux), model_not_supported und sweagent-capi:claude-opus-4.6.

Voraussetzungen: Der dynamische Code-Scanning-AI-/GitHub-Advanced-Security-Workflow ist aktiviert, wählt das beobachtete Modell, erzeugt einen Run für einen exakten Framework-PR-Head und Actions-Metadaten bleiben lesbar.

~~~text
rtk gh run view 29680055620 --repo Easton97-Jens/ModSecurity-test-Framework --log-failed
rtk gh run view 29680055620 --repo Easton97-Jens/ModSecurity-test-Framework --json databaseId,name,event,status,conclusion,headSha,workflowName,url,jobs
rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/commits/63c42e97b86acbae1374efa9f1c4209ce2ce673b/check-runs
rtk gh run view 29659308388 --repo Easton97-Jens/ModSecurity-test-Framework --json databaseId,event,headSha,status,conclusion,workflowName,jobs,url
rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/check-runs/88119051677/annotations
~~~

## Evidence

- Run-ID: 20260719T081017Z-framework-pr-resolution-20260719-840082e0
  - Artefakt: /var/tmp/codex/ModSecurity-conector/runs/20260719T081017Z-framework-pr-resolution-20260719-840082e0/evidence/github-advanced-security-pr26-63c42e9.md
  - Typ: github_advanced_security_exact_head_external_platform_failure
  - SHA-256: 7cb69c72059872f0bf6e2a5319d0846cc9f398c0fdb2584e675fd57dd58f6161
  - Befehl: rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/commits/63c42e97b86acbae1374efa9f1c4209ce2ce673b/check-runs; rtk gh run view 29680055620 --json databaseId,name,event,status,conclusion,headSha,headBranch,workflowName,url,jobs; rtk gh run view 29680055620 --log-failed
  - Arbeitsverzeichnis: /root/git/ModSecurity-conector; Exit-Code: 0; beobachtet um 2026-07-19T08:35:08Z; Retention: retained_task_evidence.
- Run-ID: 20260719T081017Z-framework-pr-resolution-20260719-840082e0
  - Artefakt: /var/tmp/codex/ModSecurity-conector/runs/20260719T081017Z-framework-pr-resolution-20260719-840082e0/evidence/pr25-c6ba5e1-final-merge-preflight.md
  - Typ: pr25_current_head_and_related_dynamic_security_disposition
  - SHA-256: ba337d271ba9b033383a8d27394eaa6e9b5d5eef4207b7dd61a564e9e091c98a
  - Befehl: rtk gh pr view 25; rtk gh api commits/c6ba5e11359d6eb30e8717b766d49697f9bed74f/check-runs; rtk gh api actions/runs?head_sha=<sha>; rtk gh run view 29659308388
  - Arbeitsverzeichnis: /root/git/ModSecurity-conector; Exit-Code: 0; beobachtet um 2026-07-19T09:33:15Z; Retention: retained_task_evidence.

## Grundursache, Remediation und Akzeptanzkriterien

Der aufbewahrte Exact-Head-Fehler identifiziert eine nicht unterstützte GitHub-Plattform-Modellauswahl. Repository-eigener Code und Workflow-Controls waren abgeschlossen, bevor der plattformverwaltete Processing-Schritt fehlschlug. Der historische #25-Fehler ist mit derselben Delivery-Grenze vereinbar, enthält aber nicht den spezifischen Modellfehler in der zugänglichen Annotation.

Ein autorisierter GitHub-Repository-Owner oder Plattform-Administrator muss ein unterstütztes Modell wählen oder aktivieren oder eine evidence-gestützte unterstützte Plattform-Disposition bereitstellen. Danach GitHub Advanced Security auf jedem anwendbaren exakten Framework-PR-Head erneut ausführen oder beobachten. Einen repository-eigenen Security-Control darf man nicht als Ersatz entfernen, unterdrücken, advisory machen, umbenennen oder abschwächen. Diese Aufgabe hat keine Autorisierung für GitHub-Plattformkonfiguration, Subscription, Modellverfügbarkeit oder Secrets.

Akzeptanzkriterien:

- Konkrete Evidence belegt, dass ein unterstütztes Modell für das Framework-Repository gewählt und nutzbar ist.
- GitHub-Advanced-Security-Code-Scanning-AI ist für jeden anwendbaren exakten aktuellen Framework-PR-Head erfolgreich.
- Der Record unterscheidet einen aktuellen erfolgreichen CodeQL-Run, einen fehlenden Code-Scanning-AI-Run und einen erfolgreichen Code-Scanning-AI-Run; keiner ersetzt einen anderen.
- Kein Framework-Security-Check, keine Policy, keine Berechtigungsgrenze, kein Parent-Gitlink und kein MRTS-Content wird als Workaround abgeschwächt oder geändert.

## Validierung, Abhängigkeiten, Blocker, verwandte Findings, Restrisiko und Historie

Validierung erfolgt über Exact-Head-Dynamic-Run-Inventar und rohe Check-Runs, GitHub-verfügbare Job-Logs oder Annotations sowie erneute Prüfung von PR-SHA, Required Checks, SonarCloud, Reviews, Review-Threads und Branch-/Ruleset-Status. Aktueller CodeQL-Erfolg ist ein legitimer separater Kontrollfall, keine Code-Scanning-AI-Coverage.

Abhängigkeit: GitHub-Plattform-/Modellverfügbarkeit und eine Entscheidung eines Repository-Owners oder Plattform-Administrators. Die Aufgabe autorisiert keine GitHub-Plattformkonfiguration, Subscription-, Modell- oder Secret-Änderung.

Verwandte Findings: FND-GITHUB-0002 ist eine andere Dependency-Graph-Capability-Lücke; FND-SONAR-0002 ist ein anderer vorbestehender Framework-Default-Branch-Quality-Gate-Backlog; FND-FRAMEWORK-0006 ist eine andere NGINX-Archiv-Provenance-Remediation.

Vor der Archiventscheidung des aktuellen Nutzers vom 2026-07-26 wurde kein Risiko akzeptiert. Aktuelle Exact-Head-Ergebnisse von CodeQL, SonarCloud und repository-eigener CI bleiben getrennte Evidence und dürfen nicht als erfolgreicher Code-Scanning-AI-Run beschrieben werden.

- 2026-07-19T08:35:08Z: platform_model_failure_confirmed — PR-#26-dynamischer GitHub-Advanced-Security-Run 29680055620 schlug mit code=model_not_supported für sweagent-capi:claude-opus-4.6 fehl.
- 2026-07-19T09:33:15Z: pr25_related_dynamic_run_reconciled — alter PR-#25-dynamischer Code-Scanning-AI-Run 29659308388 ist fehlgeschlagen, während neuer Head c6ba5e11359d6eb30e8717b766d49697f9bed74f einen erfolgreichen CodeQL-Dynamic-Run und keinen passenden Code-Scanning-AI-Run hat. Der historische Status war blocked_external_dependency; kein Run wird verborgen oder als erfolgreich reklassifiziert.

## Aktuelle Nutzer-Accepted-Risk-Archiv-Disposition — 2026-07-26

Um `2026-07-26T14:18:25Z` akzeptierte der aktuelle Nutzer dieses exakte
Restrisiko ausdrücklich für die lokale Archivierung. GitHub hat weder ein
unterstütztes Modell noch einen erfolgreichen anwendbaren Code-Scanning-AI-Run
nachgewiesen. CodeQL, SonarCloud und repository-eigene CI bleiben getrennte
Evidence und dürfen nicht als Code-Scanning-AI-Erfolg bezeichnet werden. Der
Status ist `accepted_risk`, nicht `closed`; vor Produktion, Veröffentlichung
oder Release muss der Record wiederhergestellt und neu validiert werden.
