# Codex-Erweiterungen

**Sprache:** [English](codex-extensions.md) | Deutsch

## Zweck und Scope

Dieses Dokument beschreibt das kontrollierte Codex-Erweiterungsprofil für das
Parent-Repository. Es zeichnet repository-lokale Skills, geprüfte offizielle
Plugins und externe MCP-Kandidaten auf. Es überträgt keine Erweiterung in das
Submodul `modules/ModSecurity-test-Framework`, aktiviert keinen Netzwerkdienst
und behauptet keinen Runtime-Smoke-Test für eine installierte Erweiterung.

Die maschinenlesbare Source of Truth ist
[`ci/tooling/codex-extensions.lock.yml`](../../ci/tooling/codex-extensions.lock.yml).
Sie pinnt jede geprüfte Upstream-Quelle oder kennzeichnet einen
repository-eigenen Eintrag, zeichnet Daten-, Secret- und Write-Grenzen auf und
trägt einen Status statt einer Sicherheitsannahme.

## Authority und Source-Policy

Für jede Erweiterung gilt die folgende Prioritätsreihenfolge:

1. System- und User-Instruktionen.
2. `AGENTS.md` und Repository-Policies einschließlich Security, Storage,
   Delivery, zweisprachiger Dokumentation und Parent-/Framework-Grenzen.
3. Repository-eigene lokale Skills in `.agents/skills/`.
4. Security- und Kompatibilitätsadapter für installierte Plugins.
5. Third-Party-Skill-, Plugin-, MCP-, Marketplace- und allgemeine Guidance.

Eine Erweiterung wird erst berücksichtigt, nachdem offizielle Quelle,
unveränderliche Revision, Lizenz, Skripte, Dependencies, Netzwerkverhalten,
Credential-Flow, Datenabfluss, Kostenmodell, Write-Fähigkeit und Update-Pfad
geprüft wurden. Ein Verzeichnis- oder Marketplace-Listing ist
Discovery-Material, keine Installations-Authority. Das Repository vendort keine
opaken Binaries oder Hilfsskripte, die authentifizierte GitHub-Review- oder
Check-Daten abrufen.

Repository-lokale Skills sind unter `.agents/skills/` versioniert; ihre
`UPSTREAM.md`-Dateien erhalten Source-URL, Commit, Importumfang, lokale
Anpassung und Update-Prozedur. Erforderlicher Upstream-Lizenztext verbleibt bei
dem adaptierten Material. Eine Quelle ohne verifizierte Lizenz wird nicht
vendort.

## Repository-lokale Skills

| Lokaler Skill | Status | Vorgesehene Nutzung | Bewusste Grenze |
| --- | --- | --- | --- |
| `create-plan` | `adapted_and_vendored` | Evidenzgestützte Pläne für wesentliche Änderungen | Planung publiziert nicht und erweitert keinen Scope |
| `gh-fix-ci` | `adapted_and_vendored` | Exact-SHA-Triage für task-owned GitHub Actions | Kein vendortes Log-Abruf-Hilfsprogramm und keine Credential-Ausgabe |
| `gh-address-comments` | `adapted_and_vendored` | Klassifikation und Bearbeitung aktueller PR-Feedbacks | Kein vendortes authentifiziertes Review-Daten-Hilfsprogramm |
| `stop-slop` | `adapted_and_vendored` | Abschließende reine Prosa-Klarheits- und Unsupported-Claim-Prüfung | Ändert weder technische Literale noch Evidence oder Safety-Caveats |
| `valyu-research` | `enabled` | Begrenzte Research-Planung | Aktiviert oder verwendet Valyu nicht |
| `modsecurity-codebase-migrate` | `enabled` | Parent-/Framework-bewusste Migrationsplanung | Autorisiert keine Framework-Änderung |
| `bilingual-changelog-generator` | `enabled` | Explizite gepaarte englische/deutsche Release-/Changelog-Dokumentation | Erfindet keine Verifikationsergebnisse und erstellt keine Releases |
| `third-party-skill-audit` | `enabled` | Provenienz- und Verhaltensprüfung vor Installation | Führt keine ungeprüfte Erweiterung aus |

Die vier adaptierten Skills behalten feste Source-Commits: die historische
OpenAI-`create-plan`-Quelle bei `a5119697b819090e00e5d11ee1d86834d7c1043a`,
die OpenAI-GitHub-Plugin-Quellen bei
`11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` und `stop-slop` bei
`8da1f030185bdfe8471220585162991eaeb970e9`. Der historische Ursprung von
`create-plan` wird bewusst als historisch gekennzeichnet und nicht als aktuelle
bewegliche Upstream-Branch behandelt.

## Routing-Vertrag

Die Contract-Tests validieren deklarierte Routing-Texte; sie beweisen nicht das
Dispatch-Verhalten eines interaktiven Codex-Routers. Die erwarteten positiven
und negativen Grenzen sind:

| Erweiterung oder Dienst | Verwenden, wenn | Nicht verwenden, wenn |
| --- | --- | --- |
| `create-plan` | Eine wesentliche Implementierung einen Evidence- und Verifikationsplan benötigt | Eine ein-schrittige Faktenantwort keinen Repository-Plan braucht |
| `gh-fix-ci` | Ein task-owned GitHub-Actions-Check fehlgeschlagen ist | Kein exakter fehlgeschlagener PR-Check vorliegt |
| `gh-address-comments` | Bestehendes PR-Feedback eine begrenzte Antwort benötigt | Ein breiter Review ohne bestehende Kommentare angefragt ist |
| `stop-slop` | Entwurfsprosa vage oder nicht belegte Claims enthält | Fakten/Security-Schlüsse nicht ermittelt sind |
| `valyu-research` | Aktuelle autoritative externe Recherche nötig ist | Sensitive Daten das Repository verlassen würden oder Valyu-Aktivierung angefragt ist |
| `modsecurity-codebase-migrate` | Ownership oder Kompatibilität Komponenten überschreiten kann | Ein lokaler Defekt keine Migrationsgrenze hat |
| `bilingual-changelog-generator` | Eine explizite zweisprachige Release-/Changelog-Anfrage einen Commit-/Tag-Bereich besitzt | Gewöhnliche Projektdokumentation ohne Release-/Changelog-Anfrage benötigt wird |
| `third-party-skill-audit` | Ein externer Skill, Plugin oder MCP vorgeschlagen ist | Die Quelle nicht auf eine auditierbare Revision fixiert werden kann |
| WarpGrep/Morph | Eine später genehmigte Codebase-Search-Integration benötigt wird | Tool-Filtering und Source-Verhalten ungeprüft bleiben |
| Valyu MCP | Eine später genehmigte External-Research-Integration benötigt wird | Secret-Transport und effektives Tool-Inventar unsicher/ungeprüft bleiben |

## Geprüfte Plugins

| Plugin | Feste offizielle Quelle | Beobachtete Version | Status | Grenze |
| --- | --- | --- | --- | --- |
| Superpowers | `openai/plugins`-Curated-Snapshot bei `bd2122cb92f2ade874d8c2b1d00383976ab9415b` | `5.1.3` | `installed_pending_reload` | Lokale Kompatibilitäts-Policy überschreibt kollidierende generische Workflows; kein ungeprüfter MCP, kein destruktives Cleanup, kein autonomes Publish und kein Policy-Bypass |
| Codex Security | `openai/plugins`-Curated-Snapshot bei `bd2122cb92f2ade874d8c2b1d00383976ab9415b` | `0.1.11` | `enabled` | Der lokale Node-gestützte MCP-Runtime wurde nicht ausgeführt; diese Integration impliziert keinen Security-Scan |

Superpowers wird nur aus der geprüften offiziellen Plugin-Quelle bei festem
Commit installiert. Seine repository-lokale Kompatibilitäts-Policy ist
ignorierte lokale Konfiguration und daher absichtlich kein versionierter
Produktvertrag. Eine frische Codex-Session ist nötig, bevor ein
`installed_pending_reload`-Status als aktiv gelten kann.

Das geprüfte Superpowers-Manifest bei diesem Snapshot deklariert sein
Skill-Bundle und keine MCP-Server-, Application- oder Hook-Deklaration. Seine
gebündelten Hilfsskripte wurden getrennt geprüft; Process-Control und
Temporary-Directory-Cleanup sind verboten, sofern eine begrenzte Aufgabe sie
nicht separat autorisiert.

Codex Security war bereits ein installiertes offizielles Plugin. Diese Aufgabe
inventarisiert nur Quelle und Grenzen. Sie löst weder einen Repository-Scan aus
noch aktiviert sie write-fähige Tracker- oder GitHub-App-Aktionen. Der
verfügbare Runtime enthält kein Node.js, daher hat sein gebündelter lokaler MCP
Server keine Runtime-Evidence.

Die oben stehenden GitHub-Workflow-Adapter sind versionierte lokale Skills. Sie
kopieren keine user-scoped GitHub-Konfiguration oder Credentials in dieses
Repository und ersetzen nicht die PR- und Delivery-Policies des Repositorys.

## Externe MCP-Kandidaten

| Kandidat | Status | Grund | Behauptete genehmigte Schnittstelle |
| --- | --- | --- | --- |
| Morph `@morphllm/morphmcp@0.8.206` | `blocked_source_unverified` | Package-Metadaten sind gepinnt, aber unabhängig auditierbares effektives Source-Verhalten und Codex-seitiges Tool-Filtering sind nicht belegt | Angefragte künftige Allowlist: `codebase_search`, `github_codebase_search`; nicht konfiguriert und nicht als effektiv behauptet |
| Valyu hosted MCP | `blocked_source_unverified` | Die Dokumentation übergibt den API-Key in einer URL und listet andere Tools als die angefragten Namen | Kein Mapping von `knowledge` oder `feedback`; nicht konfiguriert |
| `valyuAI/valyu-mcp` candidate | `blocked_license_unknown` | Keine verifizierte Lizenz; Setup-/Logging-Verhalten erhöht Secret- und Query-Data-Risiko | Keine Tools genehmigt |

Kein Morph- oder Valyu-Key wird in einer Repository-Datei, lokaler
Projektkonfiguration, Dokumentationsbeispiel oder Test-Fixture gespeichert. Im
Rahmen dieser Integration ging keine Anfrage an einen der kostenpflichtigen
externen Dienste. Siehe [External agent services](../security/external-agent-services.de.md)
für Daten-, Kosten-, Credential- und Revalidierungsdetails.

Wenn Morph später genehmigt wird, wird es nur für semantische Exploration
unbekannter großer Codepfade, verteilter Implementierungen oder Architektur-/
Call-Path-Fragen verwendet. Seine Ergebnisse sind Search-Hinweise und jeder
Fund wird lokal validiert. Für einen exakten String, exakten Symbolnamen,
bekannte Regex oder kleine lokale Suche ist `rg` zu verwenden; diese Fälle
werden nicht an einen externen Codebase-Dienst geleitet.

## Framework-Disposition

Diese Änderung modifiziert ausschließlich das Parent-Repository. Sie editiert,
committet, pusht oder aktualisiert den Framework-Gitlink nicht. Ein global
installiertes offizielles Plugin kann in einer separaten Framework-Session
sichtbar sein, aber repository-lokale Adapter werden durch diese Änderung nicht
übertragen. Jede Framework-Übernahme benötigt eine eigene Aufgabe,
Provenienzprüfung, Tests, Dokumentation, Commit, Push und CI-Evidence.

## Update, Rollback und Entfernung

1. Führen Sie das Third-Party-Skill-Audit vor jeder Änderung einer externen
   Erweiterung erneut aus.
2. Lösen Sie eine neue unveränderliche Revision, Lizenz, Verhalten,
   Daten-/Secret-Flow und Tool-Grenze auf; ersetzen Sie weder durch eine
   bewegliche Branch noch durch ein ähnlich benanntes Tool.
3. Aktualisieren Sie Lock-Manifest, lokale Provenienz, Contract-Tests,
   englische/deutsche Dokumentation und Change Record zusammen.
4. Entfernen oder deaktivieren Sie die betroffene Erweiterung, wenn eine Grenze
   nicht belegt werden kann; behalten Sie den Lock-Eintrag mit wahrheitsgemäßem
   blocked/rejected-Status.
5. Verifizieren Sie das fokussierte Contract-Target und die normalen
   Dokumentations-/Diff-Checks vor gewöhnlicher Repository-Delivery.

Das Erweiterungsprofil ist absichtlich konservativ: Ein dokumentierter
blockierter Kandidat ist ein erfolgreiches Kontrollergebnis und keine Einladung,
ihn zu umgehen.
