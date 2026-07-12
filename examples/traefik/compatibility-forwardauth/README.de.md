# Traefik-forwardAuth-Kompatibilitätsbeispiel

**Sprache:** [English](README.md) | Deutsch

Diese Dateien bewahren die frühere Request-Authorization-Konfiguration. Sie
sind vom nativen Local-Plugin-/UDS-Kern unter [../safe/](../safe/) getrennt.

## Anzupassende Werte

| Name | Zweck und Format | Pflicht/Default, Setzer, Geltungsbereich | Beispiel und Grenze |
| --- | --- | --- | --- |
| entryPoints.web.address | Listener-Adressstring | Pflicht; statische Datei; Traefik-Static-Scope | :8080. Ein öffentlicher Listener verändert die Exponierung. |
| providers.file.filename | Dynamischer Dateipfad relativ zum Traefik-Arbeitsverzeichnis | Pflicht; statische Datei; File-Provider-Scope | ./traefik-dynamic.yaml. Für diese Route beide Kompatibilitätsdateien zusammen kopieren. |
| Router-Regel und entryPoints | Request-Matcher und benannter Entry Point | Pflicht; dynamische Datei; Router-Scope | PathPrefix für alle Pfade und web. Für echtes Deployment begrenzen. |
| forwardAuth-Adresse | Authorization-Service-HTTP-URL | Pflicht; dynamische Datei; Middleware-Scope | http://127.0.0.1:9000/authorize. Keine Tokens oder Credentials einbetten. |
| trustForwardHeader | Boolesche Forwarded-Header-Policy | Pflicht; dynamische Datei; Middleware-Scope | false. Änderung verändert die Vertrauensgrenze und benötigt eine explizite Proxy-Header-Policy. |
| App-Service-URL | Upstream-HTTP-URL | Pflicht; dynamische Datei; Service-Scope | http://127.0.0.1:8081. Für Deployment ersetzen. |

forwardAuth läuft vor der Upstream-Response-Verarbeitung. Es darf nicht als
P3/P4-Prüfung, natives Middleware-Verhalten, Safe-Late-Verhalten,
Strict-Verhalten, First-Byte-Evidence oder No-Full-Response-Buffer-Evidence
beschrieben werden.
