# lighttpd-Quelle

**Sprache:** [English](README.md) | Deutsch

Status: nativer Phase-1-Mapper plus beibehaltene Legacy-Starter

Primäre native Quelle:

- `../module/mod_msconnector.c`: Lighttpd-Plugin-Lebenszyklus und Common Runtime
  Callsites;
- `lighttpd_modsecurity_mapper.h/.c`: echte Anfrage-/Antwort-Metadaten und Header
  Zuordnung von angehefteten Lighttpd-Typen zu allgemeinen SDK-Typen.

Der Mapper verfügt über einen Nicht-Host-Stub, sodass Repository-weite Common C-Standard-Prüfungen möglich sind
kompilieren, ohne Lighttpd-Header bereitzustellen. `build/build_module.sh` definiert
`MSCONNECTOR_LIGHTTPD_HOST_API` und kompiliert die tatsächliche Implementierung gegen
Host-Quelle angepinnt und `config.h` generiert.

`lighttpd_build_starter.c` bleibt eine Metadatenprobe.
`lighttpd_bridge.h/.c` und `lighttpd_bridge_main.c` bleiben eine separate Historie
Entscheidungsservice-Brückenstarter. Sein Selbsttest ist kein Beweis für den nativen Wirt.

Die native Quelle ordnet derzeit nur Header zu. Es bildet bewusst keine Anfrage ab
oder Antwortkörper und erstellt keinen Körper, CRS, Produktion, Sicherheit oder Vollmatrix
Anspruch.
