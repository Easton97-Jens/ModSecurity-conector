**Sprache:** [English](pr27-issue-reduction.md) | Deutsch

# PR 27 Sonar-Issue-Inventar

Diese deutsche Begleitdatei fasst die lokalen Common-SDK-Korrekturen zusammen.
Die Änderungen betreffen connector-neutrale Common-SDK-Hilfen, C-Standard-Probes,
Ereignis-/JSONL-Trunkierungsverhalten, Header-/Pfad-/Konfigurationsvalidierung
und neue Common-Infrastruktur.

SonarCloud after-count: NOT VERIFIED.

Es wird keine Connector-Laufzeitintegration, keine Produktionsreife und keine
Connector-Fähigkeit behauptet.

## Abschluss des Common-SDK-Pakets

Ergänzt wurden lokale, ausschließlich common-bezogene Helfer für
Konfigurationsparser, Request-/Response-Validierung, Rule-Merge/Error/Event,
Test-Result-JSON, Connector-Manifeste, Runtime-Report-Skelette,
Origin-Governance, Build-Verträge, C++-Wrapper, Limits, Rule-ID-Extraktion,
Log-Sanitizing und Body-Snippet-Redaktion.

SonarCloud after-count: NOT VERIFIED.

## PR-27-Bereinigung für SonarCloud und Codex Review

SonarCloud-Issue-Abruf: lokal über die SonarCloud-Issues-API für Pull Request 27 am 2026-07-02 verifiziert.

Lokale Korrektur: Die offenen neuen SonarCloud-Hinweise wurden in den Common-SDK-Dateien durch explizitere Deklarationen, ausgeschriebene Kontrollflüsse, entfernte verschachtelte Bedingungsoperatoren, einen gruppierten Event-JSON-Formatter und Shell-Hilfsfunktionen mit lokalen Parameterzuweisungen adressiert. Diese Änderungen bleiben connector-neutral und ändern keine Connector-Laufzeitpfade.

SonarCloud after-count: NOT VERIFIED. Die lokalen Prüfungen lösen keine neue SonarCloud-Analyse aus.
