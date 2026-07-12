# src – Connector-Vorlage

**Sprache:** [English](README.md) | Deutsch

Dieses Verzeichnis ist für produktiven Quellcode eines konkreten Connectors reserviert
nach seiner Herkunft sind Lizenz, Metadaten, Design und Validierungsnachweise bekannt.

## Aktueller Status

- Die Vorlage enthält keinen produktiven C/C++-Quellcode.
- Die Vorlage erhebt keine Laufzeitansprüche.
- Die Vorlage ist erst `adapter-owned`, wenn konkrete Quelle, Herkunft, Metadaten,
  und es liegen bautechnische Beweise für einen echten Connector vor.

## Vor dem Hinzufügen der Quelle

- [ ] Upstream-Quelle und Lizenz dokumentiert in `ORIGIN.md`.
- [ ] Importierte Dateien dokumentiert in `SOURCE_MAP.json` oder gleichwertig.
- [ ] Lokale Änderungen dokumentiert.
- [ ] Server-Hook/Lebenszyklusmodell dokumentiert.
- [ ] Build-Befehl und Include-/Bibliothekspfade dokumentiert.
- [ ] Laufzeitvalidierungsplan dokumentiert.

## Warnung

Kopieren Sie den Apache- oder NGINX-Laufzeitcode nicht ohne Prüfung in einen neuen Connector
dass der Zielserver über kompatible Lebenszyklen, Hooks, Filter und Body-Handling verfügt.
Protokollierung und Interventionsverhalten.
