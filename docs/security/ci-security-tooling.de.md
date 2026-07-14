# CI-Sicherheitswerkzeuge

**Sprache:** [English](ci-security-tooling.md) | Deutsch

## Geltungsbereich und Statusmodell

Dieses Dokument beschreibt Analyse- und Verifikationswerkzeuge. Es validiert
keine Schwachstelle automatisch, aktualisiert keine Dependencies, rotiert kein
Secret, ändert keine Repository-Einstellungen oder Branch-Protection und
befördert kein Build-Ergebnis zu Runtime-Evidenz.

Die autoritativen Metadaten stehen in
[security-tools.lock.yml](../../ci/tooling/security-tools.lock.yml). Ihr
Integrationsstatus ist <code>enabled</code>, <code>documented_only</code>,
<code>not_applicable</code> oder <code>blocked_feature_unavailable</code>. Ein
Toolfehler bleibt <code>failed</code>; eine nicht verfügbare optionale
GitHub-Funktion wird niemals als bestanden berichtet.

## Zugelassene Werkzeuge

| Werkzeug | Offizieller Upstream | Version | Unveränderliche Release-SHA | Integration | Status |
| --- | --- | --- | --- | --- | --- |
| actionlint | <code>rhysd/actionlint</code> | <code>v1.7.12</code> | <code>914e7df21a07ef503a81201c76d2b11c789d3fca</code> | Prüfsummenverifiziertes Linux-Binary | <code>enabled</code> |
| zizmor | <code>zizmorcore/zizmor</code> | <code>v1.27.0</code> | <code>e2627367eb7c917a90503ce05a66872fd91da6fb</code> | Prüfsummenverifiziertes Linux-Binary im Offline-Modus | <code>enabled</code> |
| Gitleaks CLI | <code>gitleaks/gitleaks</code> | <code>v8.30.1</code> | <code>83d9cd684c87d95d656c1458ef04895a7f1cbd8e</code> | Prüfsummenverifiziertes Linux-Binary | <code>enabled</code> |
| Gitleaks Action | <code>gitleaks/gitleaks-action</code> | <code>v3.0.0</code> | <code>e0c47f4f8be36e29cdc102c57e68cb5cbf0e8d1e</code> | Geprüfte Alternative | <code>documented_only</code> |
| CodeQL | <code>github/codeql-action</code> | <code>v4.37.0</code> | <code>99df26d4f13ea111d4ec1a7dddef6063f76b97e9</code> | Advanced GitHub-Actions-Workflow | <code>enabled</code> |
| Dependency Review | <code>actions/dependency-review-action</code> | <code>v5.0.0</code> | <code>a1d282b36b6f3519aa1f3fc636f609c47dddb294</code> | PR-only GitHub Action | <code>blocked_feature_unavailable</code> |
| Scorecard | <code>ossf/scorecard-action</code> | <code>v2.4.3</code> | <code>4eaacf0543bb3f2c246792bd56e8cdeffafb205a</code> | Geplante GitHub Action und SARIF | <code>enabled</code> |
| OSV-Scanner | <code>google/osv-scanner-action</code> | <code>v2.3.8</code> | <code>9a498708959aeaef5ef730655706c5a1df1edbc2</code> | PR-Diff- und geplante Reusable-Workflows | <code>enabled</code> |

actionlint, zizmor und die Gitleaks CLI sind hier reine Analysewerkzeuge. Ihre
Release-Assets werden nur nach Verifikation der dokumentierten SHA-256
akzeptiert. Gitleaks läuft mit vollständiger Redaction und löscht oder rotiert
kein Finding.

Die Gitleaks Action bleibt <code>documented_only</code>: Ihre EULA,
Lizenzanforderung für Organisationen, Standardverhalten für PR-Reporting und
möglicher Write-/Reporting-Surface sind nicht erforderlich, wenn die offizielle
CLI verwendet wird. Das Manifest dokumentiert diese Entscheidung, ohne
Credentials zu speichern.

Jede Integration besitzt ein eigenes <code>evaluated_at</code>-Datum, eine
Security-Policy-URL oder die ausdrückliche Disposition
<code>not_published_at_evaluation</code>, einen unterstützten Runner oder ein
verifiziertes Release-Asset sowie eine Aussage zur Verfügbarkeit für öffentliche
Repositories. Eine fehlende Policy wird als Prüfergebnis erfasst und niemals als
Freigabe angenommen. Die versionierte Zuordnung <code>pinned_actions</code>
bindet jede externe <code>uses:</code>-Referenz an ihren offiziellen Upstream,
die Release-Version und die vollständige Commit-SHA.

## Workflows und Berechtigungen

| Workflow | Trigger | Minimale Berechtigungen | Ergebnisgrenze |
| --- | --- | --- | --- |
| <code>ci-security-workflow-lint.yml</code> | Pull Request, Push auf geschützten Branch, manuell | <code>contents: read</code> | Getrennte actionlint- und Offline-zizmor-Ergebnisse; synthetische Fixtures beweisen die erwartete Erkennung |
| <code>ci-security-secrets.yml</code> | Pull-Request-Diff, geplanter Full-History-Scan, manuell | <code>contents: read</code> | Redigierter PR-Commit-Bereich und getrennt geprüfte History |
| <code>ci-security-osv.yml</code> | Pull-Request-Diff, geplanter Full-Scan, manuell | Job-level <code>actions: read</code>, <code>contents: read</code>, <code>security-events: write</code> | SARIF-Schwachstellenscan ohne Fix-Befehl |
| <code>ci-security-codeql.yml</code> | Pull Request, Push auf geschützten Branch, geplant, manuell | Job-level <code>contents: read</code>, <code>security-events: write</code> | Ein SARIF-Upload pro Sprachanalyse |
| <code>ci-security-scorecard.yml</code> | Push auf geschützten Branch, geplant, Branch-Protection-Ereignis, manuell | Job-level <code>contents: read</code>, <code>security-events: write</code> | Heuristische SARIF-Bewertung ohne Publishing oder Repository-Änderungen |

Alle neuen <code>uses:</code>-Referenzen sind vollständige 40-stellige
Commit-SHAs mit stabilem Versionskommentar. Bestehende mutable
Actions-Referenzen wurden in einer getrennten Änderungswelle nach derselben
Regel gepinnt. Die Manifestprüfung validiert die gespeicherte
Upstream-/Release-Zuordnung für jeden Workflow mit der Endung
<code>.yml</code> oder <code>.yaml</code>, nicht nur die Form der SHA.

Analyse-Workflows verwenden <code>pull_request</code> und nicht
<code>pull_request_target</code>, erhalten keine Repository-Secrets aus Forks
und setzen die Persistenz von Checkout-Credentials auf false, sofern kein Write
benötigt wird. Dadurch wird der unsichere Ausführungskontext des Ziel-Repository
vermieden. Das bedeutet auch, dass ein PR seinen eigenen Workflow oder
Downloader verändern kann: Konfigurieren Sie außerhalb dieses Repositories
einen geschützten Required Workflow oder ein Ruleset, bevor diese Jobs als
manipulationssicheres Merge-Gate behandelt werden. Hier wurde keine
Repository-Einstellung geändert; die Read-only-PR-Jobs bleiben nützliche
Analyse-Evidenz.

## Abdeckung und Grenzen

CodeQL scannt GitHub Actions, jedes vorhandene Go-Modul getrennt und einen
abgegrenzten C/C++-Scope, der die repository-eigenen Common-C17-Helper baut. Es
beansprucht keine vollständige Connector-C/C++-Abdeckung: Externe Host-Header
und reale Connector-Build-Capture sind eine getrennte Folgeaufgabe.

OSV scannt rekursiv durch den offiziellen Reusable-Workflow und erfasst
Go-Moduldateien sowie erkannte unterstützte Lock-, Vendor-, Container- und
Paketdefinitionen, sofern sie vorhanden sind. Es ersetzt nicht
<code>govulncheck</code> für Go-Call-Path-Evidenz. Die zugelassene Integration
ist die aufgeführte GitHub Action; daher wird keine direkte lokale CLI aus
einem separaten Repository installiert. Der lokale OSV-Status vor der
GitHub-Ausführung ist <code>not_executed</code>, während der geplante und
PR-Workflow der aktivierte Ausführungspfad ist. Verwenden Sie in diesem
Repository niemals einen OSV-Fix-Befehl.

Dependency Review wird nicht ersetzt, solange die
Dependency-Graph-/SBOM-Funktion nicht verfügbar ist. Prüfen Sie diese
GitHub-Funktion erneut, bevor ihr konservativer PR-only-Workflow aktiviert
wird. Sie muss <code>blocked_feature_unavailable</code> bleiben und darf weder
still übersprungen noch als bestanden berichtet werden.

Scorecard ist heuristische Evidenz, keine Branch-Protection-Entscheidung. Ihr
Caller ist SHA-gepinnt, aber seine Docker-Metadaten können weiterhin einen
mutablen GHCR-Tag wählen. Der OSV-Reusable-Workflow behält ebenfalls
verschachtelte Docker-/Action-Referenzen. Diese Rest-Risiken werden zur Prüfung
dokumentiert statt verborgen.

Artifact Attestations sind
<code>not_applicable_until_release_workflow_exists</code>: Dieses Repository
besitzt keine echten Release-Tags, Release-Artefakte, Prüfsummen oder
dokumentierten Release-Workflow. Es wurde keine künstliche Release-Pipeline
erstellt.

## Lokale Verifikation

Verwenden Sie ein task-spezifisches temporäres Ziel:

```sh
python3 ci/tools/fetch_security_tool.py --tool actionlint --destination "$CODEX_TEMP_ROOT/tmp/security-tools"
python3 ci/tools/fetch_security_tool.py --tool zizmor --destination "$CODEX_TEMP_ROOT/tmp/security-tools"
python3 ci/tools/fetch_security_tool.py --tool gitleaks_cli --destination "$CODEX_TEMP_ROOT/tmp/security-tools"
"$CODEX_TEMP_ROOT/tmp/security-tools/actionlint" -shellcheck="$(command -v shellcheck)"
"$CODEX_TEMP_ROOT/tmp/security-tools/zizmor" --offline .github/workflows
"$CODEX_TEMP_ROOT/tmp/security-tools/gitleaks" git --redact=100 --log-opts="<base-sha>..HEAD" .
make check-security-tools
```

Ohne Pfadargument entdeckt actionlint die Repository-Workflows. CI verwendet
ein explizites rekursives <code>find</code> für <code>.yml</code> und
<code>.yaml</code>; der Manifest-Validator deckt dieselbe Menge ab. Das
unsichere zizmor-Fixture muss mit Exit ungleich null enden; das sichere
Fixture muss mit Exit null enden. Fügen Sie kein <code>--fix</code> hinzu,
erstellen Sie keine ungeprüfte Gitleaks-Baseline und führen Sie keinen
Paketmanager nur aus, damit ein Scanner vollständig erscheint. Prüfen Sie ein
Finding auf Direktheit, Indirektheit und Erreichbarkeit, bevor Sie eine
getrennte Remediation-Aufgabe öffnen.

## Triage und Updates

Behandeln Sie Scanner-Ausgabe als Kandidaten. Erfassen Sie exakten Commit,
Toolversion, Workflow-/Job-URL, redigiertes Ergebnis, betroffene Dependency
oder Codepfad und ob das Finding direkt, indirekt, erreichbar oder nicht
erreichbar ist. Eine False-Positive- oder Accepted-Risk-Entscheidung benötigt
eine dokumentierte Begründung und einen Ablauf-/Review-Zeitpunkt; unterdrücken
Sie keinen Audit global, nur um einen grünen Lauf zu erhalten.

Prüfen Sie bei jedem Update offiziellen Owner, Lizenz, Security Policy, stabiles
Release, Release-Datum, vollständige Release-SHA, Binary-Digest soweit
anwendbar, Berechtigungen, Secrets, Verfügbarkeit für öffentliche Repositories
und automatisches Fix-Verhalten. Aktualisieren Sie Manifest, unveränderliche
Workflow-Kommentare, fokussierte Tests, englische/deutsche Dokumentation und
Change Record zusammen. Kein Token- oder Secret-Wert gehört in diese Dateien.

## Verwandte Referenzen

- [Sicherheitswerkzeug-Manifest](../../ci/tooling/security-tools.lock.yml)
- [Codex-Erweiterungen](../development/codex-extensions.de.md)
- [Betrieb und Sicherheit](../operations-and-security.de.md)
- [Change Records](../../reports/audits/change-records/README.de.md)
