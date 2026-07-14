# Change Record: Kontrolliertes Codex-Erweiterungsprofil

**Sprache:** [English](CR-20260714-codex-extension-profile.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Titel | Kontrolliertes Codex-Erweiterungsprofil |
| Change-ID | CR-20260714-codex-extension-profile |
| Datum (UTC) | 2026-07-14 |
| Autor oder ausführender Agent | Codex agent <code>/root</code> |
| Basis-Revision | <code>be0356af96ef582c3a7dbc0169c7c8b27b7b6b34</code> |
| Zugehöriges Issue oder Pull Request | Pending draft pull request |
| Finale Revision | Ausstehender finaler Delivery-Commit |

## Motivation und Problemstellung

Ein kontrolliertes, auditierbares Codex-Erweiterungsprofil für das
Parent-Repository etablieren. Das Profil muss feste Provenienz- und
Lizenzinformationen erhalten, repository-lokale Policy-Adapter und
deterministische Checks bereitstellen, nur ein geprüftes offizielles Plugin
installieren und ungeprüfte oder unsichere externe MCP-Dienste deaktiviert
lassen.

## Akzeptanzkriterien

| Kriterium | Status | Evidenz |
| --- | --- | --- |
| Jede betrachtete Erweiterung hat Source-URL, feste Revision oder wahrheitsgemäßen blocked-Status, Version, Lizenz, Capability-Grenze und Update-Policy | Erfüllt | <code>ci/tooling/codex-extensions.lock.yml</code> und Extension-Contract-Tests |
| Angefragte repository-lokale Skills sind mit Frontmatter, Provenienz und erforderlichen Lizenzen vorhanden | Erfüllt | Acht Skill-Verzeichnisse und fokussierte Contract-Tests |
| Superpowers ist nur aus dem offiziellen Curated-Snapshot installiert und durch eine ignorierte lokale Kompatibilitäts-Policy begrenzt | Erfüllt, Session-Reload ausstehend | Plugin-Inventar meldet Version-Snapshot <code>bd2122cb</code>; lokale Policy ist nicht gestaged |
| Bestehendes Codex Security bleibt offizielles enabled Plugin ohne implizierten Scan | Erfüllt | Plugin-Inventar und dokumentierte No-Scan-Grenze |
| Morph/WarpGrep- und Valyu-MCP-Kandidaten sind ohne verifizierbare Source-/Tool-/Secret-Kontrollen nicht konfiguriert, aktiviert oder aufgerufen | Erfüllt | Lock-Status, Dokumentation, Presence-Check für fehlende Keys und keine Paid-Calls |
| Englische/deutsche Dokumentation und Change-Record-Companions bleiben ausgerichtet | Erfüllt | Bilingual- und Link-Checks |
| Parent-only-Scope bewahrt Framework-Source und Gitlink | Erfüllt | Finaler Framework-Status war leer und der Parent-Gitlink blieb unverändert |

## Implementierungsentscheidung und Begründung

Nur adaptierte Guidance mit fester Quelle und Lizenz vendoren: historisches
OpenAI-<code>create-plan</code>, zwei OpenAI-GitHub-Workflow-Skills und
<code>stop-slop</code>. Ihre authentifizierten GitHub-Hilfsskripte auslassen,
um keinen Review-/Check-Log-Datenkanal hinzuzufügen. Vier repository-eigene
Skills für begrenzte Research, Migrationsplanung, gepaarte Dokumentation und
künftige Erweiterungs-Audits implementieren.

Alle betrachteten Items in einem Lock-Manifest erfassen und Frontmatter,
Provenienz, Lizenzpräsenz, Source-Pins, relative Links, Secret-Abwesenheit,
deklarierte positive/negative Routing-Grenzen und die Ablehnung unsicherer
Automatisierung mit einem deterministischen Root-Test verifizieren. Den Check
in <code>lint</code> und damit in <code>quick-check</code> aufnehmen.

Den bereits verfügbaren offiziellen Curated-Plugin-Snapshot bei
<code>bd2122cb92f2ade874d8c2b1d00383976ab9415b</code> für Superpowers Version
<code>5.1.3</code> und Codex Security Version <code>0.1.11</code> verwenden.
Die Superpowers-Kompatibilitäts-Policy gibt System-/User-/Repository-Regeln
Priorität und blockiert sein Worktree-, Process-Control-, Cleanup-, Automatic-
Publish- und Policy-Bypass-Verhalten ohne separate Authority.

### Erweiterungsdisposition

Das Lock-Manifest enthält die exakten Source-URLs, Pfade, Capability-Felder und
Update-/Entfernungsdispositionen. Diese Tabelle zeichnet für jede geprüfte
Erweiterung feste Source/Version, Lizenzentscheidung und Integrationsergebnis
auf.

| Erweiterung | Feste Source/Version | Lizenz | Integrationsergebnis und importiertes Material |
| --- | --- | --- | --- |
| `create-plan` | `openai/skills@a5119697b819090e00e5d11ee1d86834d7c1043a` | Apache-2.0 | Adaptiertes/vendortes `SKILL.md`, vollständige Lizenz, Provenienz; keine Skripte |
| `gh-fix-ci` | `openai/plugins@11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` / `0.1.6` | Apache-2.0 | Adaptierte/vendorte Guidance und Lizenz; authentifiziertes Check-Log-Hilfsprogramm ausgelassen |
| `gh-address-comments` | `openai/plugins@11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` / `0.1.6` | Apache-2.0 | Adaptierte/vendorte Guidance und Lizenz; authentifiziertes GraphQL-Hilfsprogramm ausgelassen |
| `stop-slop` | `hardikpandya/stop-slop@8da1f030185bdfe8471220585162991eaeb970e9` | MIT | Adaptierte/vendorte Guidance und Lizenz; keine Skripte |
| `valyu-research` | repository-authored | repository-owned | Enabled Planning-Adapter; aktiviert Valyu nicht |
| `modsecurity-codebase-migrate` | repository-authored | repository-owned | Enabled begrenzter Migrationsplanungsadapter |
| `bilingual-changelog-generator` | repository-authored | repository-owned | Enabled expliziter Release-/Changelog-Adapter |
| `third-party-skill-audit` | repository-authored | repository-owned | Enabled Pre-Install-Audit-Adapter |
| Superpowers | `openai/plugins@bd2122cb92f2ade874d8c2b1d00383976ab9415b` / `5.1.3` | MIT | Offizielles Plugin im User-Profil installiert; `installed_pending_reload`; keine Plugin-Inhalte vendort |
| Codex Security | `openai/plugins@bd2122cb92f2ade874d8c2b1d00383976ab9415b` / `0.1.11` | Proprietary | Bestehendes offizielles Plugin enabled beibehalten; keine Inhalte vendort und kein Scan ausgeführt |
| Morph/WarpGrep | `@morphllm/morphmcp@0.8.206`, git head `ac38aadb555519751cee042a77f0d2cd5e9b01e1` | MIT metadata | `blocked_source_unverified`; keine MCP-Konfiguration oder Anfrage |
| Valyu hosted MCP | offizielle Hosted-Dokumentation, unversioniert | unknown | `blocked_source_unverified`; URL-Secret-Transport und Inventory-Mismatch verhindern Konfiguration |
| `valyuAI/valyu-mcp` | `valyuAI/valyu-mcp@546c3d2f2a113f0c97007eb21da0f168387bbcef` | unknown | `blocked_license_unknown`; nicht vendort oder ausgeführt |
| Composio `pr-review-ci-fix` | `awesome-codex-skills@9c9da64cf1bbea611d43dd14a10788d55369b353` | unknown | `rejected_due_to_overlap` |
| Composio `connect-apps` | `awesome-codex-skills@9c9da64cf1bbea611d43dd14a10788d55369b353` | unknown | `rejected_due_to_permissions` |
| Composio `skill-share` | `awesome-codex-skills@9c9da64cf1bbea611d43dd14a10788d55369b353` | unknown | `rejected_due_to_overlap` |
| Composio `mcp-builder` | `awesome-codex-skills@9c9da64cf1bbea611d43dd14a10788d55369b353` | unknown | `documented_only` |
| Composio frontend/webapp | `awesome-codex-skills@9c9da64cf1bbea611d43dd14a10788d55369b353` | unknown | `not_applicable` |

## Geänderte Dateien

Versionierte Dateien im Scope sind:

- <code>.agents/skills/</code> mit den acht lokalen Skills, Upstream-Records
  und erforderlichen Lizenzdateien für adaptierte Quellen
- <code>ci/tooling/codex-extensions.lock.yml</code>
- <code>tests/test_codex_extensions.py</code> und <code>Makefile</code>
- Englische/deutsche Paare <code>docs/development/codex-extensions.*</code>
  und <code>docs/security/external-agent-services.*</code>
- Englische/deutsche Dokumentationsindizes und Operations-/Security-Cross-Links
- dieses englische/deutsche Change-Record-Paar und seine Indizes

Ignorierte nur lokale Dateien ergänzen die Superpowers-Kompatibilitäts-Policy
und eine <code>AGENTS.md</code>-Referenz. Sie werden absichtlich nicht gestaged.
Keine Product-C/C++-Source, Connector-Konfiguration, Framework-Datei,
Framework-Gitlink, Workflow, generiertes Artefakt oder Secret wird geändert.

## Ausgeführte Befehle

| Sanitisierter Befehl | Ergebnis | Evidence-Grenze |
| --- | --- | --- |
| <code>rtk curl -fsSL ...fixed raw source URLs...</code> | 0 | Nur geprüfter Upstream-Text unterhalb des Task-Temporary-Root heruntergeladen |
| <code>rtk codex plugin marketplace add openai/plugins --ref &lt;fixed-commit&gt; --json</code> | Kontrollierte Ablehnung | Der eingebaute <code>openai-curated</code>-Marketplace ist reserviert; kein Marketplace wurde hinzugefügt |
| <code>rtk codex plugin add superpowers@openai-curated --json</code> | 0 | Superpowers aus Curated-Snapshot <code>bd2122cb</code> außerhalb des Repositorys installiert |
| <code>rtk codex plugin list --json</code> | 0 | Superpowers, Codex Security und bestehende Plugins als installiert/enabled gemeldet; keine Credential-Werte gezeigt |
| <code>rtk proxy /bin/bash -lc '&lt;presence-only checks for MORPH_API_KEY and VALYU_API_KEY&gt;'</code> | 0 | Beide Namen fehlten; keine Werte wurden ausgegeben |
| <code>rtk make check-codex-extension-contract</code> | 0 | Zwölf Extension-Contract-Tests bestanden nach der finalen Erweiterung der Abdeckung |
| <code>rtk make check-bilingual-docs</code> | 0 | Bilingual-Dokumentenvalidierung bestanden |
| <code>rtk make check-doc-links</code> | 0 | Repository- und Framework-Dokumentlinks bestanden |
| <code>rtk git diff --check</code> | 0 | Keine Whitespace-Fehler gemeldet |
| <code>rtk git check-ignore -v AGENTS.md .codex/config.toml .codex/context/superpowers-compatibility-policy.md</code> | 0 | Lokale Kompatibilitäts-Policy und Codex-Konfiguration als ignoriert bestätigt |
| <code>rtk git -C modules/ModSecurity-test-Framework status --short</code> | 0 | Framework-Worktree-Status war leer |
| <code>rtk proxy /bin/bash -lc 'BUILD_ROOT=&lt;task-temp-root&gt;/build ... make lint'</code> | 2 | Durch fehlendes lokales <code>apxs</code>/<code>apxs2</code> bei Vorbereitung des Apache-C17-Checks blockiert |
| <code>rtk proxy /bin/bash -lc 'CI=true BUILD_ROOT=&lt;task-temp-root&gt;/build ... make lint'</code> | 2 | Der Apache-C17-Check wurde wahrheitsgemäß als <code>SKIPPED</code> markiert, aber das rekursive Apache-Cleanup-Target wandelte seinen dokumentierten <code>77</code>-Blocker in Make-Exit <code>2</code> um |
| <code>rtk proxy /bin/bash -lc 'CI=true BUILD_ROOT=&lt;task-temp-root&gt;/build ... make quick-check'</code> | 2 | Über <code>lint</code> denselben Apache-Cleanup-Prerequisite-/rekursiven-Make-Blocker erreicht |
| <code>rtk curl ...sonar PR issue query...</code> | 0 | Vier task-owned Regex-Qualitätsbefunde nach bestandenem Draft-PR-Quality-Gate identifiziert |
| <code>rtk make check-codex-extension-contract</code> | 0 | Zwölf Tests nach der Sonar-getriebenen Regex-Behebung bestanden |

Der erste fokussierte Contract-Run schlug nur fehl, weil seine Negative-Route-
Fixture die Formulierung <code>sensitive data</code> suchte, während der Skill
korrekt die strengere Formulierung <code>sensitive code</code> verwendet. Der
Test wurde korrigiert; der nachfolgende fokussierte Contract-Run bestand. Full
Lint und Quick-Check wurden ausgeführt und als blockiert statt bestanden
gemeldet, weil die lokale Apache-Voraussetzung fehlt und der Cleanup-Lint-
Wrapper den dokumentierten Blocked-Exit nicht durch rekursives Make erhält.

Nach Erstellung des Draft-PR bestand das SonarQube-Cloud-Quality-Gate, meldete
aber vier task-owned Regex-Qualitätsbefunde in
<code>tests/test_codex_extensions.py</code>. Der Follow-up ersetzt den
backtracking-anfälligen <code>git clean</code>-Ausdruck durch eine begrenzte
zeilenlokale Optionsprüfung und entfernt einen unter <code>IGNORECASE</code>
redundanten Zeichenbereich. Der fokussierte Zwölf-Test-Contract-Run bestand
nach der Behebung; eine Remote-Neuanalyse ist nach seinem Follow-up-Push nötig.

## Security-Auswirkung

Die Änderung verbessert die Supply-Chain-Kontrolle für Erweiterungen durch
Source-Pins, lokal reviewbare Lizenzen/Provenienz, ausgelassene authentifizierte
Hilfsskripte, Checks auf häufige Literal-Secret-Formen im versionierten Material
und dokumentierte Network-/Data-/Cost-/Write-Grenzen. Es wurde kein vollständiger
Codex-Security-Scan ausgelöst: Die Aufgabe ändert Erweiterungs-Governance statt
Product-Source, und kein Scan war angefragt.

Ein bereits vorhandenes user-scoped Extension-Credential wurde als Inline-lokale
Konfiguration außerhalb des Repositorys beobachtet. Es wurde nicht ausgegeben,
kopiert, normalisiert oder verändert. Es bleibt ein Credential-Hygiene-Risiko,
das sein Owner über genehmigte Secret-Storage- sowie Rotation-/Revocation-
Prozeduren beheben muss.

Morph und Valyu bleiben blockiert. Es wurden weder Key noch Paid-Call,
Code-Search, externe Datenübertragung oder externe MCP-Tool-Enumeration
durchgeführt. Node.js fehlt, daher wurde gebündeltes lokales Node-gestütztes
MCP-Runtime-Verhalten nicht ausgeführt.

## Runtime-Evidence

Es wurde keine Connector-Runtime-, Protocol-, CRS/MRTS-, Lifecycle-,
Production- oder Security-Scan-Evidence erhoben oder behauptet. Diese Aufgabe
ändert nur Repository-Erweiterungs-Governance und Dokumentation; C17/C23/C2y-
Kompilierung und Hardening-Builds sind nicht anwendbar, weil sich keine
repository-eigene C/C++-Source änderte.

## Bekannte Einschränkungen

- Superpowers ist im User-Profil installiert, erfordert aber eine frische
  Codex-Session, bevor seine Skills in dieser Session als aktiv gelten können.
- Die Superpowers-Quelle enthält Hilfsskripte mit Process- und
  Temporary-Directory-Effekten; die lokale Kompatibilitäts-Policy verbietet ihre
  implizite Nutzung.
- Codex Securitys lokaler Node-gestützter MCP besitzt keine Runtime-Evidence,
  weil Node.js nicht verfügbar ist.
- Morph-Source-Verhalten/Tool-Filtering und Valyu-sicherer Secret-Transport/
  Tool-Inventar sind nicht belegt, daher ist keiner der Dienste konfiguriert.

## Verbleibende Risiken

- Die bereits vorhandene user-scoped Inline-Credential-Konfiguration liegt
  außerhalb der Änderungs-Authority dieser Aufgabe und sollte durch ihren Owner
  migriert/rotiert werden.
- Ein künftiges Codex- oder Plugin-Update kann Erweiterungsverhalten ändern;
  das Lock-Manifest verlangt vor dem Update ein erneutes
  Immutable-Source-Audit.
- Die gewünschte Morph-Tool-Allowlist ist dokumentiert, aber keine erzwungene
  Kontrolle; der Kandidat muss blockiert bleiben, bis ein tatsächlicher
  Client-/Server-Filter belegt ist.
- Valyus dokumentiertes URL-Secret-Format und Tool-Name-Mismatch bleiben offen.

## Nicht ausgeführte Prüfungen mit Begründung

- Kein externer Morph-/WarpGrep- oder Valyu-Request, Key-Validation, Paid-Call
  oder Tool-List-Smoke-Test lief: Die Integrationen sind blockiert, bevor ein
  sicheres Secret und eine erzwingbare Tool-Grenze existieren.
- Kein Codex-Security-Scan lief: Er liegt außerhalb dieser Governance-only-
  Aufgabe, und der User schloss einen vollständigen Security-Scan ausdrücklich
  aus.
- Kein Connector-Build, Configuration-, H1/H2/H3-, CRS/MRTS-, Lifecycle-,
  C17/C23/C2y-, Sanitizer- oder Hardening-Build lief: Keine
  Product-/Connector-/Runtime-Source änderte sich.
- Keine Framework-Aufgabe, kein Framework-Commit, -Push oder -CI lief: Das
  Framework lag außerhalb des Scope.

## Finaler Diff- und Review-Status

Die fokussierte Extension-Contract-, Bilingual-Dokumentations- und
Dokumentlink-Validierung bestanden. Der finale Whitespace-Check bestand;
lokale Kompatibilitäts-Policy/-Konfiguration blieben ignoriert; Framework-
Worktree und Parent-Gitlink blieben unverändert. Full Lint und Quick-Check
wurden beide versucht, sind lokal jedoch durch fehlende Apache-Host-
Voraussetzungen blockiert; der CI-Mode-Cleanup-Wrapper zeigt zusätzlich ein
bestehendes rekursives-Make-Exit-Status-Problem. Es wird kein grüner
Lint-/Quick-Check-Claim erhoben. Dieser Record entspricht dem final beabsichtigten
Diff vor Commit und Push; die task-generierten Runtime-Cache-Reports und
Snapshot-Skripte wurden wiederhergestellt/entfernt und fehlen in diesem Diff.
Exact-final-SHA-Remote-CI bleibt das Delivery-Gate.
