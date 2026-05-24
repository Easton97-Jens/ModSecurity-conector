# src – Connector Template

Dieses Verzeichnis ist für produktiven Quellcode eines **konkreten** Connectors
reserviert, sobald dessen Design und Validierung vorliegen.

## Aktueller Stand

- Dieses Template enthält absichtlich keinen produktiven C-Code.
- Es werden keine Funktionszusagen für neue Connectoren gemacht.

## Wichtige Warnung

Runtime-Code aus Apache oder NGINX darf **nicht ungeprüft kopiert** werden.
Server-Lifecycle, Hook-Pfade, Filter-Modelle und Body-Verarbeitung sind
connector-spezifisch und müssen separat geprüft und validiert werden.
