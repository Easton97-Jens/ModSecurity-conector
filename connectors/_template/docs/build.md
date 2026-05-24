# Build – Connector Template

## Zweck

Platzhalter für die Build-Strategie eines konkreten neuen Connectors.

## Grundsatz

Jeder Connector benötigt eigene, server-spezifische Build-Regeln. Ein
Build-Rezept aus Apache oder NGINX darf nur nach technischer Prüfung und
Anpassung übernommen werden.

## Mindestinhalte (noch zu prüfen)

- Build-Voraussetzungen (Compiler, SDKs, Server-Header, libmodsecurity)
- Verzeichnislayout für Build-Artefakte unter `BUILD_ROOT`
- Schritte zur lokalen Reproduktion (clean build)
- Fehlerbilder und Troubleshooting
- Versionierung/Pinning der externen Quellen

## Makefile-Integration (TODO)

Für einen konkreten Connector sind TODOs zu prüfen:

- [ ] `smoke-<name>` Target ergänzen
- [ ] optional `build-<name>`/`check-<name>` Targets ergänzen
- [ ] Dokumentation der notwendigen Umgebungsvariablen ergänzen
- [ ] sicherstellen, dass keine Artefakte außerhalb `BUILD_ROOT` entstehen

## Nicht enthalten

Dieses Template liefert absichtlich keine konkreten Build-Kommandos für einen
noch nicht implementierten Connector.
