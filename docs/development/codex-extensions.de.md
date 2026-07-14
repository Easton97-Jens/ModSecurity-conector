# Codex-Erweiterungen

**Sprache:** [English](codex-extensions.md) | Deutsch

## Geltungsbereich

Dieses Repository teilt fokussierte Workflow-Hinweise unter
<code>.agents/skills/</code>. Lokale Codex-Einstellungen bleiben von Git
ausgeschlossen: Sie schützen einen vertrauenswürdigen Checkout, ohne eine
Produktkonfiguration oder einen Ersatz für Repository-Richtlinien zu werden.

Lesen Sie vor der Nutzung einer Erweiterung das aktive <code>AGENTS.md</code>
und die einschlägigen Repository-Richtlinien. Das Parent verantwortet diese
Skills und Prüfungen; das Framework bleibt ein separates Repository und wird
durch diese Schicht nie verändert.

## Geteilte Repository-Skills

| Skill | Verwenden für | Nicht verwenden für |
| --- | --- | --- |
| <code>security-finding-lifecycle</code> | Evidenzgestützte Erfassung, Validierung, Erreichbarkeit, Behebung und Regression eines Findings | Ein unvalidiertes Scan-Ergebnis oder automatische Behebung |
| <code>ci-failure-triage</code> | Untersuchung von GitHub Actions anhand der exakten SHA mit vergleichbarem <code>master</code>-Lauf | Vorbeugende Workflow-Änderungen oder einen älteren Lauf |
| <code>delivery-ci</code> | Abgegrenzte Lieferung vom finalen Diff bis Draft-PR und Final-SHA-CI | Direkte <code>master</code>-Lieferung oder ein unbestätigtes Ergebnis |
| <code>bilingual-change-record</code> | EN/DE-Gleichwertigkeit und Abgleich des Change Records | Übersetzen von Quellcode oder Erfinden von Evidenz |
| <code>connector-test-matrix</code> | Getrennte Bewertung von CRS/MRTS und H1/H2/H3 | Einen Transport-/Profilwert als vollständige Abdeckung behandeln |
| <code>framework-parent-handoff</code> | Einen echten Framework-zu-Parent-Handoff | Reine Parent-Arbeit oder eine Framework-Gitlink-Änderung ohne Framework-Lieferung |
| <code>dependency-security-update</code> | Kleine, getrennte Dependency-Sicherheitsupdates | Breite Dependency-Aktualisierungen ohne erneute Verifikation |
| <code>optional-prerequisite-ci</code> | Ehrliche Statusbehandlung optionaler Voraussetzungen | Echte Fehler durch pauschales Erfolgsverhalten verbergen |

Jeder Skill enthält eine kompakte <code>SKILL.md</code> und generierte
<code>agents/openai.yaml</code>. Der versionierte Validator prüft Frontmatter,
eindeutige Namen, erforderliche Workflow-Abschnitte, relative Links,
benutzerspezifische Pfade, secret-ähnliche Inhalte und unsichere
Standard-Befehlsbeispiele.

## Lokale Read-only-Agenten

Die folgenden ignorierten Dateien verwenden das aktuelle projektlokale
Codex-Agentenschema und setzen <code>sandbox_mode = "read-only"</code>:

| Lokaler Agent | Prüfgrenze |
| --- | --- |
| <code>repo-explorer</code> | Architektur, Call-Pfade und Parent-/Framework-Ownership |
| <code>security-reviewer</code> | Speicher-, Datenschutz-, Pfad-, Supply-Chain-, Protokoll- und erreichbare Dependency-Risiken |
| <code>test-evidence-reviewer</code> | Akzeptanzkriterien, Testlücken und Evidenzgrenzen |
| <code>bilingual-doc-reviewer</code> | Semantische EN/DE-Gleichwertigkeit von Pfaden, Befehlen, Status, Grenzen und Risiken |
| <code>ci-triager</code> | Finale SHA, PR-/Push-Läufe und vergleichbare <code>master</code>-Evidenz |

Sie bearbeiten, stagen, committen, pushen, löschen oder wiederholen keine CI,
ändern keinen Branch-Schutz und erklären ein Finding nicht durch Behauptung für
valide. Es gibt absichtlich keine deutschen Kopien lokaler Agentendateien. Die
leere Tabelle <code>[mcp_servers]</code> verhindert, dass geerbte MCP-Server
einen Read-only-Review erweitern.

## Lokale Hooks

<code>.codex/hooks.json</code> verwendet das offizielle projektlokale
Hook-Schema. Codex muss geänderte nicht verwaltete Hooks über
<code>/hooks</code> prüfen und vertrauen; starten Sie die Sitzung nach lokalen
Hook-Änderungen neu oder fort.

| Ereignis | Deterministische Prüfung | Entscheidung |
| --- | --- | --- |
| <code>SessionStart</code> | Erwarteter Git-Root, vertrauenswürdige Projektkonfiguration, <code>on-request</code>, <code>workspace-write</code>, Requirements-Ausschlüsse, Temp-Root und Parent-/Framework-Präsenz | Ergänzt eine explizite configured- oder blocked-Diagnose; ersetzt Codex-Enforcement nicht |
| <code>PreToolUse</code> für <code>Bash</code> | Breites Staging, Force-Push, Hard-Reset, direkter <code>master</code>-Push, rekursives Löschen außerhalb des Temp-Roots und geschützte Staging-Pfade | Verweigert den unterstützten gefährlichen Toolaufruf, ohne seinen Befehl auszugeben |
| <code>PermissionRequest</code> für <code>Bash</code> | Prüft dieselben Kategorien gefährlicher Befehle vor einer Eskalationsanfrage erneut | Verweigert die Anfrage bei gesperrter Kategorie |

Die Hook-Policy lädt nie Daten herunter, gibt keine Tokens oder
Befehlsinhalte aus, committet oder pusht nicht, löscht Produktdateien nicht
automatisch und ersetzt nicht die Codex-Sandbox, Approval-Policy oder
<code>requirements.toml</code>. Sie ist ein deterministischer
Befehls-Schutzmechanismus, kein fachliches Security-Urteil.

Die versionierten Vertragstests verwenden synthetische Befehle für die lokale
Policy: Gefährliche Git-Befehle werden verweigert, reine Lese-Befehle bleiben
erlaubt, geschützte Pfade werden vom Staging ausgeschlossen und die Ausgabe
enthält kein synthetisches Secret.

## MCP-Disposition

| MCP-Fähigkeit | Status | Begründung |
| --- | --- | --- |
| Offizielles OpenAI-Entwicklerdokumentations-MCP | Lokal konfiguriert; Session-Neuladung erforderlich | Es liefert autoritatives Read/Search-Material für Codex-Schemafragen ohne Repository-Credential |
| Offizieller GitHub-MCP-Server | <code>documented_only</code> | Vorhandener <code>gh</code>-Zugriff deckt die erforderlichen Leseoperationen ab; kein zusätzlicher konfigurierter Read-Surface war nachweislich nötig |

Kein Token, Access-Credential oder breites Write-Tool-Allowlist wird in einer
Repository- oder lokalen Erweiterungsdatei gespeichert. Das Dokumentations-MCP
ist durch Auswahl read-only. Ein GitHub-MCP darf erst nachgewiesen werden, wenn
eine dokumentierte Read-only-Lücke besteht und eine sichere
Authentifizierungsmethode verfügbar ist.

## Validierung und Pflege

Führen Sie die geteilten Prüfungen im Repository-Root aus:

```sh
make check-codex-skills
python3 -m unittest -v tests.test_codex_skills tests.test_codex_hook_policy
python3 -m json.tool .codex/hooks.json
```

Der letzte Befehl ist lokal und gilt nur, nachdem die ignorierten Hook-Dateien
installiert wurden. Stagen Sie nicht <code>.codex/</code>, <code>.rtk/</code>,
<code>AGENTS.md</code>, <code>RTK.md</code>, lokale Analyseausgabe, temporäre
oder Build-Bäume oder mögliche Secret-Dateien.

Wenn Codex sein dokumentiertes Skill-, Agenten- oder Hook-Schema ändert,
prüfen Sie die offizielle Dokumentation, aktualisieren Sie zuerst den
versionierten Skill-Vertrag, aktualisieren Sie ignorierte lokale Dateien erst
nach dieser Prüfung, führen Sie die fokussierten Tests aus, prüfen Sie
<code>/hooks</code> und starten Sie die vertrauenswürdige Sitzung neu. Kopieren
Sie keine lokale Konfiguration in einen Commit.

## Verwandte Referenzen

- [Repository-Konzept](../repository-concept.de.md)
- [Architektur](../architecture.de.md)
- [Change-Traceability](../change-traceability.de.md)
- [CI-Sicherheitswerkzeuge](../security/ci-security-tooling.de.md)
- [Offizielle Codex-Dokumentation](https://developers.openai.com/codex/)
