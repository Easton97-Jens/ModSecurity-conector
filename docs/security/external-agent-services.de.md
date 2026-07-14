# Externe Agent-Dienste

**Sprache:** [English](external-agent-services.md) | Deutsch

## Scope

Dieses Dokument setzt die Datenschutz-, Secret-, Data-Egress-, Kosten- und
Aktivierungsgrenze für Codex-Erweiterungen, die mit einem externen Dienst
kommunizieren. Es ist keine Dienstempfehlung, konfiguriert kein Credential und
belegt nicht, dass ein Remote-Dienst oder Tool-Filter sicher ist.

Das aktuelle Erweiterungsinventar und die unveränderliche Provenienz stehen in
[`ci/tooling/codex-extensions.lock.yml`](../../ci/tooling/codex-extensions.lock.yml).
Die aktuelle Gesamtposition ist `partial_extension_integration`:
Repository-Skills und dokumentierte Plugin-Kontrollen existieren, externe
MCP-Kandidaten bleiben jedoch blockiert.

## Nicht verhandelbare Kontrollen

- Speichern Sie keinen API-Key, Bearer-Token, OAuth-Material, Cookie, privaten
  Key, Zertifikat, Request-Payload, Response-Payload oder privaten Host-Pfad im
  Repository, einer versionierten Test-Fixture, Dokumentation oder einem
  Lock-Manifest.
- Verwenden Sie nur eine Secret-Referenz aus der genehmigten Runtime-Umgebung,
  nachdem Secret-Transport-Design und Tool-Inventar des Dienstes verifiziert
  sind. Platzieren Sie niemals einen Key in einer URL.
- Behandeln Sie Source-Code, Repository-Struktur, Query-Text, Review-Daten,
  Pfade und Search-Ergebnisse als extern verarbeitete Daten, wenn ein hosted
  MCP beteiligt ist.
- Holen Sie explizite Authority vor einem kostenpflichtigen Request, einer neuen
  Third-Party-Application-Verbindung oder einem Dienst mit Write-Fähigkeit
  außerhalb des Task-Scope ein.
- Verwenden Sie eine Allowlist nur, wenn Client und Dienst einen dokumentierten,
  verifizierbaren Enforcement-Punkt bieten. Eine gewünschte Liste ist allein
  keine Sicherheitskontrolle.
- Loggen Sie nur minimale nicht geheime Metadaten, die eine Entscheidung
  erklären. Bewahren Sie keine Remote-Payloads in Evidence-Dateien auf.

## Morph-/WarpGrep-Kandidat

| Attribut | Geprüfter Wert |
| --- | --- |
| Kandidat | `@morphllm/morphmcp@0.8.206` |
| Package-Source-Revision | `ac38aadb555519751cee042a77f0d2cd5e9b01e1` |
| Package-Lizenzmetadaten | MIT |
| Dokumentierter Credential-Name | `MORPH_API_KEY` |
| Status | `blocked_source_unverified` |
| Paid-Service-Verhalten | Kein Request wurde ausgeführt; der Dienst verarbeitet extern nach Nutzungsmodell |

Die Package-Metadaten wurden gepinnt und ihre Integrity-Daten während der
Prüfung aufgezeichnet. Das reicht nicht aus, um das Verhalten aller effektiven
MCP-Tools oder einen Codex-seitigen Filter zu belegen. Die öffentliche
Dokumentation beschreibt einen Befehl mit Package-Runner und `MORPH_API_KEY`;
Node.js ist im aktuellen Runtime nicht verfügbar, daher wurden weder
Package-Ausführung, Key-Check, Tool-List-Call noch Paid-Request durchgeführt.

Die angefragte künftige Exposition ist auf `codebase_search` und
`github_codebase_search` begrenzt. Die Namen sind als gewünschte Allowlist
aufgezeichnet, aber keine Konfiguration behauptet ihre Durchsetzung. Auch
dokumentiertes Server-Verhalten für Editieren oder andere Nicht-Search-Tools
erfordert Prüfung. Bis unveränderliches Source-Verhalten und ein echter
Enforcement-Mechanismus unabhängig verifiziert sind, wird der MCP weder
konfiguriert noch aktiviert oder ausgeführt.

Die Nutzung eines solchen Dienstes könnte Repository-Struktur, Search-Fragen
und relevante Code-Snippets an Morph übertragen. Die geprüfte
Pricing-Information nennt `$0.80` pro Million Input-/Output-Tokens; eine Aufgabe
muss dies als externe Kostengrenze und nicht als Erlaubnis zum Service-Call
behandeln.

## Valyu-Kandidaten

### Hosted MCP

Die offizielle Hosted-Dokumentation verwendet einen Endpoint in der Form
`https://mcp.valyu.ai/mcp?valyuApiKey=...&maxPrice=50`. Ein Credential in der
URL verletzt die Secret-Grenze dieses Repositorys, da URLs in
Prozessargumente, Diagnostik, History, Proxies oder Logs gelangen können.
Daher ist der hosted MCP nicht konfiguriert.

Das dokumentierte Inventar enthält Tools wie `valyu_search`,
`valyu_academic_search` und `valyu_contents`. Es belegt keine Tools mit den
Namen `knowledge` oder `feedback`; diese Integration mappt keinen der
angefragten Namen stillschweigend auf eine andere Service-Operation. Valyu
dokumentiert kostenpflichtige Suchen mit einem Mindestpreis von `$0.01` pro
Suche. Es wurden weder Key-Validierung noch Tool-Liste oder Paid-Request
ausgeführt.

### Lokaler Repository-Kandidat

Der geprüfte Kandidat `valyuAI/valyu-mcp` bei
`546c3d2f2a113f0c97007eb21da0f168387bbcef` besitzt in der geprüften Quelle
keine verifizierte Lizenz. Sein Setup schreibt eine lokale Environment-Datei
und sein Verhalten kann Queries und vollständige Responses loggen. Er ist
`blocked_license_unknown`, wird nicht vendort und hat keine genehmigten Tools.

## Grenzen offizieller Plugins

| Erweiterung | Aktuelle Kontrolle |
| --- | --- |
| Superpowers | Nur aus der festen offiziellen `openai/plugins`-Revision installiert. Seine lokale Kompatibilitäts-Policy gibt System-/User-/Repository-Regeln Priorität und verbietet ungeprüften MCP, destruktives Cleanup, automatisches Publish und Policy-Bypass. Ein Session-Reload steht noch aus. |
| Codex Security | Nur Inventar des offiziellen Plugins. Der gebündelte Node-gestützte MCP besitzt keine Runtime-Evidence, weil Node.js fehlt. Diese Arbeit initiierte weder Security-Scan noch write-fähige Application-Aktion. |
| GitHub-Workflow-Adapter | Versionierte lokale Anpassungen. Sie lassen Upstream-Skripte aus, die authentifizierte Check-Logs oder Review-Kommentare abrufen, und kopieren keine user-scoped Konfiguration oder Credentials. |

Die bestehende user-scoped Erweiterungskonfiguration liegt außerhalb des
Repository-Scope. Sie muss als Secret-tragende Konfiguration behandelt werden
und wird durch diese Änderung weder kopiert noch normalisiert.

## Revalidierung und Incident Response

Vor dem Aktivieren eines blockierten Kandidaten müssen alle folgenden Punkte
abgeschlossen sein:

1. Offizielle unveränderliche Source, Lizenz, Maintainer, Version und
   Package-Integrity erneut auflösen.
2. Skripte, Dependencies, Subprozesse, Netzwerkendpunkte, Data-Egress,
   Credential-Handling, Logging, Write-Aktionen und Kostenverhalten prüfen.
3. Die tatsächliche Codex-/MCP-Allowlist und den Disable-Mechanismus mit
   dokumentierten Tool-Namen belegen. Allowlist nicht aus Prosa ableiten.
4. Credential nur in einer genehmigten Environment-only-Referenz behalten;
   ausschließlich Presence/Absence verifizieren, ohne den Wert auszugeben.
5. Separate Authority für Paid-Calls oder neue externe Verbindungen einholen,
   einen begrenzten nicht sensitiven Smoke-Test ausführen und exakte
   Scope-/Result-Evidence aufzeichnen.
6. Lock-Manifest, Tests, englische/deutsche Dokumentation und Change Record
   aktualisieren, bevor der Kandidat als enabled gemeldet wird.

Wenn ein Credential an einer repository-kontrollierten oder command-sichtbaren
Stelle beobachtet wird, stoppen Sie seine Verarbeitung, vermeiden Sie Echo oder
Kopie, entfernen Sie es nur mit geeigneter Authority, rotieren/widerrufen Sie
es über den Credential-Owner und zeichnen Sie einen nicht geheimen
Remediation-Status auf. Ein blockierter Dienst bleibt blockiert, bis diese
Reaktion und Revalidierung abgeschlossen sind.

## Weiterführende Referenzen

- [Codex-Erweiterungen](../development/codex-extensions.de.md)
- [Betrieb und Sicherheit](../operations-and-security.de.md)
- [Nachvollziehbarkeit von Änderungen](../change-traceability.de.md)
