# HAProxy Scaffold Build Plan

## Hinweis

Dieses Dokument beschreibt offene Build-Fragen. Es behauptet keine
funktionierende Build-Pipeline.

## Offene Build-Fragen (noch zu prüfen)

- [ ] Wird ein kompilierter Connector-Bestandteil benötigt?
- [ ] Wird ein separater SPOA-Agent gebaut?
- [ ] Welche Abhängigkeiten/Versionen sind erforderlich?
- [ ] Gibt es HAProxy-Testcontainer für reproduzierbare Läufe?
- [ ] Welche Artefakte entstehen und wo werden sie abgelegt?

## Build-Isolation (noch zu prüfen)

- [ ] Alle generierten Artefakte unter `BUILD_ROOT` halten.
- [ ] Keine Seiteneffekte außerhalb der vorgesehenen Build-Verzeichnisse.

## Makefile-Integration (später, noch zu prüfen)

- [ ] `smoke-haproxy` Target definieren.
- [ ] Optional `build-haproxy`/`check-haproxy` Targets definieren.
- [ ] Erforderliche Umgebungsvariablen dokumentieren.

## Nicht enthalten

- Keine finalen Build-Kommandos.
- Keine Aussage, dass ein HAProxy-Build aktuell möglich ist.
