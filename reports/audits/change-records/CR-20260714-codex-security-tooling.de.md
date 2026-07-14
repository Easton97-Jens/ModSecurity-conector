# Change Record: Codex-Erweiterungen und CI-Sicherheitswerkzeuge

**Sprache:** [English](CR-20260714-codex-security-tooling.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Titel | Codex-Erweiterungen und CI-Sicherheitswerkzeuge |
| Change-ID | CR-20260714-codex-security-tooling |
| Datum (UTC) | 2026-07-14T00:00:00Z |
| Autor oder ausführender Agent | Codex |
| Basis-Revision | be0356af96ef582c3a7dbc0169c7c8b27b7b6b34 |
| Zugehöriges Issue oder Pull Request | [Draft PR #44](https://github.com/Easton97-Jens/ModSecurity-conector/pull/44) |
| Finale Revision | Delivery-Kandidat <code>8a3982d29b5007e7c421a193933a18cc1ba3696b</code>; Evidence-Record-Commit ausstehend |

## Motivation und Problemstellung

Das Parent benötigte eine geteilte, wartbare Codex-Skill-Schicht und eng
begrenzte lokale Erweiterungen sowie unabhängig verifizierbare
CI-Sicherheitsanalyse. Das Design muss die Framework-Grenze bewahren,
Credentials aus Konfiguration fernhalten und Analyseergebnisse weder in
automatische Remediation noch in Runtime-Claims verwandeln.

## Betroffene Komponenten und Sicherheitsgrenzen

Der versionierte Scope enthält <code>.agents/skills/</code>, Skill- und
Security-Tool-Validatoren, fokussierte Unit-Tests, einen
prüfsummenverifizierenden Binary-Fetch-Helper, Workflows, unveränderliche
Action-Pins, Dokumentation und diesen Record. Framework-Worktree und Gitlink
bleiben außerhalb des Scopes.

Der ignorierte lokale Scope enthält <code>.codex/agents/</code>,
<code>.codex/hooks.json</code> und lokale Hook-Skripte. Das lokale
Dokumentations-MCP ist ohne Repository-Credential konfiguriert; GitHub MCP
bleibt <code>documented_only</code>. Lokale Dateien liegen absichtlich
außerhalb des Git-Diffs und ersetzen weder Sandbox, Approval-Policy noch
verwaltete Requirements.

## Akzeptanzkriterien

| Kriterium | Status | Evidenz |
| --- | --- | --- |
| Acht geteilte Skills folgen dem aktuellen dokumentierten Format und validieren | Lokal erfüllt | Skill-Validator und fokussierte Tests |
| Lokale Read-only-Agenten und deterministische Hooks sind syntaktisch valide und ignoriert | Lokal erfüllt | TOML/JSON/Python-Prüfungen, synthetische Hook-Entscheidungen, <code>git check-ignore</code> |
| Security-Metadaten erfassen zugelassene Upstreams, Policy-Dispositionen, Releases, unveränderliche SHAs, Prüfsummen, Berechtigungen, Plattformen, Verfügbarkeit und Status | Lokal erfüllt | Security-Tools-Manifest-Validator |
| actionlint und zizmor analysieren alle Workflows unabhängig | Lokal und für den Delivery-Kandidaten erfüllt | Prüfsummenverifizierte lokale Tools; unsicheres Fixture abgewiesen und sicheres Fixture akzeptiert; Run <code>29357810936</code> bestanden |
| Gitleaks verwendet redigierte PR-Range-Semantik ohne Remediation | Lokal und für den Delivery-Kandidaten erfüllt | Redigierte Basis-bis-Kandidat-Range über 13 Commits ohne Leaks; Run <code>29357811166</code> bestanden |
| Dependency Review wird ohne erforderliche GitHub-Funktion nicht aktiviert | Erfüllt | <code>blocked_feature_unavailable</code>-Disposition |
| CodeQL-, Scorecard- und OSV-Workflows verwenden minimale dokumentierte Berechtigungen und unveränderliche Caller-Pins | Für den Delivery-Kandidaten erfüllt | CodeQL <code>29357810753</code>, Scorecard <code>29357810737</code> und OSV-PR-Vergleich <code>29357812062</code> bestanden |
| Framework und Gitlink bleiben unverändert | Für den Delivery-Kandidaten erfüllt | <code>make check-framework</code>; Framework-SHA <code>aac462cf217cdd5d09a56e3029c279459158f3ac</code>; kein Gitlink-Diff |

## Untersuchte Alternativen

Die Gitleaks Action wurde wegen ihrer aktuellen EULA, Lizenzanforderung für
Organisationen, Standard-Reporting-Verhalten und möglichem Write-Surface nicht
ausgewählt; für die offizielle CLI sind diese Grenzen unnötig. Eine direkte
OSV-CLI aus einem separaten Repository wurde nicht installiert, weil die
zugelassene Integration die aufgeführte offizielle GitHub Action ist.
Dependency Review wurde nicht durch einen schwächeren Ersatz ersetzt, solange
die Dependency-Graph-Funktion nicht verfügbar ist. Artifact Attestations wurden
nicht ergänzt, weil kein echter Release-Workflow existiert.

## Ausgewählte Upstreams und Vertrauensbewertung

Alle ausgewählten Repositories gehören zur für diesen Auftrag zugelassenen
Upstream-Menge. Jeder Eintrag wurde am 2026-07-14 bewertet; das versionierte
Manifest erfasst offiziellen Owner, Release-Datum, vollständige
Release-Commit-SHA, Security-Policy-Disposition, unterstützte
Integrationsplattform, Verfügbarkeit für öffentliche Repositories, minimale
Berechtigungen, Secrets und automatisches Fix-Verhalten.

| Werkzeug | Offizieller Upstream und Policy-Disposition | Lizenz | Release und vollständige SHA | Verifizierte Plattform / öffentliche Verfügbarkeit | Integration und Status |
| --- | --- | --- | --- | --- | --- |
| actionlint | <code>rhysd/actionlint</code>; <code>rhysd/actionlint/security/policy</code> | MIT | <code>v1.7.12</code>; <code>914e7df21a07ef503a81201c76d2b11c789d3fca</code> | Verifiziertes Linux-x86_64-Asset; frei, kein Credential | Prüfsummenverifiziertes Binary; <code>enabled</code> |
| zizmor | <code>zizmorcore/zizmor</code>; <code>zizmorcore/zizmor/security/policy</code> | MIT | <code>v1.27.0</code>; <code>e2627367eb7c917a90503ce05a66872fd91da6fb</code> | Verifiziertes Linux-x86_64-Asset; frei, kein Credential | Prüfsummenverifiziertes Binary; <code>enabled</code> |
| Gitleaks CLI | <code>gitleaks/gitleaks</code>; <code>gitleaks/gitleaks/security/policy</code> | MIT | <code>v8.30.1</code>; <code>83d9cd684c87d95d656c1458ef04895a7f1cbd8e</code> | Verifiziertes Linux-x86_64-Asset; frei, kein Credential | Prüfsummenverifiziertes Binary; <code>enabled</code> |
| Gitleaks Action | <code>gitleaks/gitleaks-action</code>; <code>gitleaks/gitleaks-action/security/policy</code> | Gitleaks Action EULA | <code>v3.0.0</code>; <code>e0c47f4f8be36e29cdc102c57e68cb5cbf0e8d1e</code> | GitHub-gehostetes Linux; Organisationslizenz erforderlich | Nur bewertet; <code>documented_only</code> |
| CodeQL | <code>github/codeql-action</code>; <code>github/codeql-action/security/policy</code> | MIT Action; CodeQL-CLI-Bedingungen gelten | <code>v4.37.0</code>; <code>99df26d4f13ea111d4ec1a7dddef6063f76b97e9</code> | GitHub-gehostetes Linux; Open-Source-Repositories auf GitHub unterstützt | SHA-gepinnte Action; <code>enabled</code> |
| Dependency Review | <code>actions/dependency-review-action</code>; <code>actions/dependency-review-action/security/policy</code> | MIT | <code>v5.0.0</code>; <code>a1d282b36b6f3519aa1f3fc636f609c47dddb294</code> | GitHub-gehostetes Linux; benötigte Graph-/SBOM-Funktion hier nicht verfügbar | Nicht aktiviert; <code>blocked_feature_unavailable</code> |
| Scorecard | <code>ossf/scorecard-action</code>; <code>ossf/scorecard-action/security/policy</code> | Apache-2.0 | <code>v2.4.3</code>; <code>4eaacf0543bb3f2c246792bd56e8cdeffafb205a</code> | GitHub-gehostetes Linux; frei für öffentliche Repositories | SHA-gepinnte Action; <code>enabled</code> |
| OSV-Scanner | <code>google/osv-scanner-action</code>; <code>google/osv-scanner-action/security/policy</code> | Apache-2.0 | <code>v2.3.8</code>; <code>9a498708959aeaef5ef730655706c5a1df1edbc2</code> | GitHub-gehostetes Linux; kein Repository-Secret | SHA-gepinnte direkte PR-Leaf-Actions und geplanter Reusable-Workflow; <code>enabled</code> |

## Implementierungsentscheidung und Begründung

Die Implementierung pinnt Actions auf vollständige Release-Commit-SHAs,
verifiziert Binary-Downloads gegen dokumentierte SHA-256-Werte, hält Scanner
analyse-only und verwendet Job-level <code>security-events: write</code> nur
für SARIF-Upload. actionlint und zizmor sind getrennte Jobs; Gitleaks trennt
PR-Diff von geplanter Full-History. CodeQL begrenzt C/C++ auf einen realen
Common-C17-Build und scannt die zwei Go-Module getrennt.

Bestehende mutable Actions-Referenzen wurden in einer getrennten
Änderungswelle gepinnt. Workflow-Lint fand eine vorbestehende
ShellCheck-Style-Diagnose und einen Template-Injection-Pfad; beide wurden als
notwendige Voraussetzungen für ein sinnvolles All-Workflow-Gate korrigiert.
Credential-Persistenz wird für Checkout-Schritte deaktiviert, wo kein Write
erforderlich ist.

Der Pin-Validator prüft jeden <code>.yml</code>- und <code>.yaml</code>-Workflow
rekursiv gegen eine versionierte Karte offizieller Releases, nicht nur gegen
eine 40-stellige SHA und einen versionsförmigen Kommentar.

Der veröffentlichte OSV-<code>v2.3.8</code>-PR-Reusable-Workflow überschritt
GitHubs 1-MiB-Job-Output-Limit, obwohl Scanner, Reporter, SARIF-Upload und
Basis-gegen-PR-Vergleich erfolgreich waren. Der release-gepinnte PR-Pfad
spiegelt daher seine Scanner-/Reporter-Schritte, exportiert jedoch kein
vollständiges JSON als Job-Output; der geplante Full-Scan bleibt beim offiziellen
Reusable-Workflow. Damit ist der task-eigene
<code>workflow_configuration_failure</code> ohne unreleased Upstream-Commit
und ohne Abschwächung von <code>--fail-on-vuln=true</code> behoben.

## Geänderte Dateien

Versionierte Dateien umfassen alle acht <code>.agents/skills/</code>-Ordner,
<code>ci/checks/documentation/check_codex_skills.py</code>,
<code>ci/checks/security/codex_hook_policy.py</code>,
<code>ci/checks/security/check_security_tools_manifest.py</code>,
<code>ci/tooling/security-tools.lock.yml</code>,
<code>ci/tools/fetch_security_tool.py</code>, fokussierte Tests,
zizmor-Fixtures, Security-Workflows, bestehende Workflow-Pins,
<code>Makefile</code>, gepaarte Dokumentation und diesen gepaarten Change
Record.

Lokale unversionierte Dateien umfassen die fünf Read-only-Agent-Definitionen
und die Session-, Pre-Tool- und Permission-Request-Hooks unter
<code>.codex/</code>. Sie werden nicht gestaged oder committed.

## Hinzugefügte oder geänderte Tests

- <code>tests/test_codex_skills.py</code>
- <code>tests/test_codex_hook_policy.py</code>
- <code>tests/test_security_tools_manifest.py</code>
- <code>tests/test_fetch_security_tool.py</code>
- Sichere und absichtlich unsichere zizmor-Fixtures
- Fokussierte Make-Targets für Codex-Skills und Security-Tooling

## Ausgeführte Befehle

| Exakter Befehl | Exit-Code oder Ergebnis | Sanitisierte relevante Zusammenfassung | Kanonischer Evidence-Pfad | Run-ID |
| --- | --- | --- | --- | --- |
| <code>python3 ci/checks/documentation/check_codex_skills.py</code> | 0 | Alle erforderlichen Skills valide | None | None |
| <code>make check-codex-skills</code> | 0 | Versioniertes Skill-Target bestanden | None | None |
| <code>python3 ci/checks/security/check_security_tools_manifest.py</code> | 0 | Manifest und Workflow-Pins valide | None | None |
| <code>make check-security-tools</code> | 0 | Manifest, Release-Karte und alle Workflow-Pins valide | None | None |
| <code>python3 -m unittest -v tests.test_codex_skills tests.test_codex_hook_policy tests.test_security_tools_manifest tests.test_fetch_security_tool</code> | 0 | Zweiundzwanzig fokussierte Tests bestanden | None | None |
| <code>actionlint -shellcheck=/usr/bin/shellcheck</code> | 0 | Alle entdeckten Workflows mit ShellCheck-Integration valide | None | None |
| <code>zizmor --offline .github/workflows</code> | 0 | Alle Workflows melden keine Findings | None | None |
| <code>zizmor --offline ci/fixtures/zizmor/insecure.yml</code> | Erwartet ungleich null | Gefährlicher Trigger und Template Injection wurden erkannt | None | None |
| <code>zizmor --offline ci/fixtures/zizmor/safe.yml</code> | 0 | Sicheres Fixture akzeptiert | None | None |
| <code>gitleaks git --redact=100 --log-opts="--all" .</code> | 1 | 83 historische Kandidaten; keine Baseline angelegt und nicht als Task-Regression gewertet | None | None |
| <code>gitleaks git --redact=100 --log-opts="be0356af96ef582c3a7dbc0169c7c8b27b7b6b34..HEAD" .</code> | 0 | Dreizehn Delivery-Kandidaten-Commits gescannt; keine Leaks gefunden | None | None |
| <code>make check-bilingual-docs</code> | 0 | Gepaarte Dokumentation valide | None | None |
| <code>make check-doc-links</code> | 0 | Links und Repository-Pfadreferenzen valide | None | None |
| <code>make quick-check</code> | 2 | Unvollständig: Lokales DNS konnte den ModSecurity-Upstream während der Provisionierung nicht auflösen; dadurch blieb die Apache/APXS-Voraussetzung nicht verfügbar, kein Task-Source-Defekt nachgewiesen | None | None |
| <code>make lint</code> | 2 | Unvollständig: lokale Apache/APXS-Provisionierung meldete <code>missing_local_httpd_build</code>; kein Task-Source-Defekt nachgewiesen | None | None |
| GitHub Actions Security-Workflow-Lint | 0 | actionlint und zizmor bestanden | GitHub Actions | <code>29357810936</code> |
| GitHub Actions Secret-Scan | 0 | Pull-Request-Commit-Range-Scan bestanden | GitHub Actions | <code>29357811166</code> |
| GitHub Actions CodeQL | 0 | Actions-, Go-Envoy-, Go-Traefik- und begrenzte C/C++-Jobs bestanden | GitHub Actions | <code>29357810753</code> |
| GitHub Actions Scorecard | 0 | Same-Repository-Pull-Request-Job bestanden; Default-Branch-Job absichtlich übersprungen | GitHub Actions | <code>29357810737</code> |
| GitHub Actions OSV-PR-Vergleich | 0 | Basis-/PR-Scans, Reporter, SARIF und Artefakte ohne Job-Output-Export bestanden | GitHub Actions | <code>29357812062</code> |
| SonarCloud Quality Gate | 0 | Neue Reliability-, Security- und Maintainability-Ratings bestanden | SonarCloud PR #44 | None |

Der Delivery-Kandidat wurde zu <code>origin</code> gepusht; seine Remote-SHA
entsprach <code>8a3982d29b5007e7c421a193933a18cc1ba3696b</code>, und Draft PR
#44 bleibt ohne Merge oder Auto-Merge offen. Der Evidence-Record-Commit
benötigt noch seine eigene Exact-SHA-Verifikation; kein nicht ausgeführter
Befehl wird als bestanden dargestellt.

## Security-Auswirkung

Die Änderung ergänzt deterministische lokale Guardrails und CI-Analyse, ohne
neue breite Write-Berechtigungen zu geben. Sie entfernt mutable Caller-Refs,
macht Binary-Provenienz prüfbar, prüft Workflow-Injection- und Permission-Risiken
und redigiert Gitleaks-Ausgabe. Sie validiert kein Finding automatisch,
modifiziert keine Dependencies, entfernt keine Secrets, rotiert keine
Credentials, ändert keine Branch-Protection und erhebt keine Runtime-Evidenz.

## Dokumentationsänderungen

Gepaarte Dokumente zu Codex-Erweiterungen und CI-Sicherheitswerkzeugen wurden
hinzugefügt; gepaarter Dokumentationsindex und Betrieb/Sicherheit wurden
aktualisiert; dieser gepaarte Change Record wurde ergänzt. Die Dokumente
erfassen Upstream-Auswahl, Lizenzierung, Updateprozess, False-Positive-Triage,
Secret-/Redaction-Regeln, Grenzen und lokale-only-Konfiguration.

## Runtime-Evidence

Für diese Änderung wurde keine Runtime-Evidence erhoben oder beansprucht.
Builds, statische Analyse, Lint, Unit-Tests und CI-Workflow-Konfiguration sind
keine Connector-Runtime-Evidenz.

## Matrix- und Protokoll-Disposition

| Dimension | Status | Begründung |
| --- | --- | --- |
| H1 | <code>not_applicable</code> | Dieser Scope ändert nur Skills, Dokumentation und CI-Sicherheitswerkzeuge |
| H2 | <code>not_applicable</code> | Dieser Scope ändert nur Skills, Dokumentation und CI-Sicherheitswerkzeuge |
| H3 | <code>not_applicable</code> | Dieser Scope ändert nur Skills, Dokumentation und CI-Sicherheitswerkzeuge |
| no_crs_no_mrts | <code>not_applicable</code> | Kein Connector-Lifecycle-Verhalten wurde geändert |
| with_crs_no_mrts | <code>not_applicable</code> | Kein Connector-Lifecycle-Verhalten wurde geändert |
| no_crs_with_mrts | <code>not_applicable</code> | Kein Connector-Lifecycle-Verhalten wurde geändert |
| with_crs_with_mrts | <code>not_applicable</code> | Kein Connector-Lifecycle-Verhalten wurde geändert |

## Bekannte Einschränkungen

Lokale OSV-Ausführung ist <code>not_executed</code>; keine nicht aufgeführte
direkte CLI wurde installiert. Ihr zugelassener GitHub-PR-Vergleich bestand für
den Delivery-Kandidaten, während der geplante Full-Scan künftige Evidenz bleibt.
Dependency Review ist <code>blocked_feature_unavailable</code>. CodeQL
beansprucht keine vollständige externe Connector-C/C++-Abdeckung.
Lokale Hooks erfordern ein vertrauenswürdiges Projekt, <code>/hooks</code>-Review
und Session-Neustart/-Fortsetzung, um aktiv zu werden.
<code>pull_request</code>-Analyse vermeidet den unsicheren
<code>pull_request_target</code>-Kontext, ist aber kein eigenständig
manipulationssicheres Merge-Gate; dafür ist ein externer geschützter Required
Workflow oder ein Ruleset erforderlich.

## Verbleibende Risiken

Scorecard und OSV behalten verschachtelte mutable Docker-/Action-Referenzen
jenseits des Caller-SHA-Pins. Gitleaks-Full-History-Ergebnisse können getrennt
geprüfte Baseline-Behandlung benötigen. Verfügbarkeit geplanter
CodeQL-/OSV-/SARIF-Läufe bleibt von künftiger GitHub-Workflow-Ausführung
abhängig. Scanner-Reports benötigen Reachability- und False-Positive-Triage vor
Remediation. Diese Risiken werden dokumentiert, nicht automatisch unterdrückt.

Der experimentelle Scorecard-PR-Head-Pfad läuft absichtlich nur für Pull
Requests desselben Repositorys mit <code>contents: read</code>; Fork-PRs
überspringen ihn, weil die Upstream-Action sie nicht unterstützt. Der
Default-Branch-Pfad behält den SARIF-Upload.

Der redigierte lokale Gitleaks-Full-History-Lauf meldete 83 historische
Kandidaten. In dieser Aufgabe wurde keine Baseline, Unterdrückung, Löschung oder
Rotation angelegt. Die redigierte Basis-bis-Delivery-Kandidaten-Range scannte
13 Commits und fand keine Leaks.

## Nicht ausgeführte Prüfungen mit Begründung

Kein großer Connector-Build, keine Connector-Runtime, keine CRS/MRTS-Matrix und
kein H1/H2/H3-Transporttest liefen, weil kein Connector-Verhalten geändert
wurde. Eine direkte lokale OSV-CLI lief nicht, weil sie außerhalb der
zugelassenen Upstream-Integration liegt. Die geplanten OSV- und
Default-Branch-Scorecard-Scans liefen nicht für einen Pull Request; ihr
übersprungener Status ist erwartet. Das angeforderte Target
<code>make check-repository-path-references</code>
existiert nicht; <code>make check-doc-links</code> rief seinen zugrundeliegenden
Repository-Pfadreferenz-Checker auf und bestand. Ein Retry mit
<code>SKIP_RUNTIME_COMPONENT_PREPARE=1 make lint</code> lief nicht, weil dieser
Schalter den direkten Apache/APXS-Provisionierungspfad von lint nicht abdeckt
und ohne zusätzlichen Evidenzgewinn generierte Runtime-Reports umschreiben
könnte.

## Finaler Diff- und Review-Status

Der Delivery-Kandidat <code>8a3982d29b5007e7c421a193933a18cc1ba3696b</code>
ist gepusht und seine Remote-SHA verifiziert. Alle task-eigenen Security- und
Quality-Runs bestanden. Fünf bestehende Struktur-/Lint-Jobs scheiterten, weil
dem Runner nutzbares Apache-<code>apxs</code>/Header fehlt; der Vergleich mit
<code>master</code> bestätigte dieselbe unabhängige Fehlerklasse. Sie sind
<code>unrelated_repository_failure</code>; der Delivery-Kandidaten-Status ist
daher <code>ci_blocked_unrelated_failure</code>. Dieses reine Evidence-Record-
Update muss committed, gepusht und für seine eigene exakte SHA verifiziert
werden. Kein Merge oder Auto-Merge ist autorisiert.
