# Build – Connector-Vorlage

**Sprache:** [English](build.md) | Deutsch

## Zweck

Dieses Dokument dokumentiert die Baunachweise, die ein Betonverbinder erbringen muss.
Die Vorlage selbst enthält keine Build-Befehle für eine noch nicht implementierte Version
Connector.

## Checkliste erstellen

- [ ] Build-Befehl dokumentiert.
- [ ] Dokumentierte Pfade einschließen.
- [ ] Bibliothekspfade dokumentiert.
- [ ] Build-Artefakte dokumentiert.
- [ ] Build-Protokollpfad dokumentiert.
- [ ] Bereinigungs-/Aktualisierungsverhalten dokumentiert.
- [ ] Externe Abhängigkeitsversionen oder Pins dokumentiert.
- [ ] Build-Ausgabespeicherort unter `BUILD_ROOT` dokumentiert.
- [ ] Compiler-/Linker-Fehler wurden ohne Vermutung dokumentiert.

## Erforderliche Felder für einen Betonverbinder

```text
Connector:
Source path:
Build command:
Environment:
Include paths:
Library paths:
Artifacts:
Build log:
Exit code:
```

## Checkliste für die Makefile-Integration

- [ ] `smoke-<name>` Ziel gefunden oder mit Beweisen hinzugefügt.
- [ ] Optionales `build-<name>`- oder `check-<name>`-Ziel dokumentiert, falls vorhanden.
- [ ] Erforderliche Umgebungsvariablen dokumentiert.
- [ ] Artefakte bleiben unterhalb des dokumentierten Build-Roots.
- [] Kein globaler Quellbaum wird vom Build-Flow gelöscht oder überschrieben.

## Beweisregeln

- Ein Build-Anspruch erfordert den genauen Befehl, Exit-Code, Artefaktpfad und Protokoll
  Pfad.
- Ein kopiertes Build-Rezept von Apache oder NGINX muss mit dem neuen verglichen werden
  Build-System des Servers.
- Include-/Bibliothekspfade müssen im Build-Befehl, im generierten Makefile, gefunden werden.
  oder Build-Protokoll.
- Wenn kein Abhängigkeitspfad gefunden wird, dokumentieren Sie `Nicht im Repository gefunden`.

## Nicht im Lieferumfang enthalten

Diese Vorlage stellt absichtlich keine konkreten Build-Befehle und keinen Compiler bereit
Flags, Server-SDK-Annahmen oder generierte Artefakte für einen zukünftigen Connector.
