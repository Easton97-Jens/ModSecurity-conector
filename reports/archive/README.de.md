# Archivierte Berichte

**Sprache:** [English](README.md) | Deutsch

Dieses Verzeichnis bewahrt ersetzte Planungs-, Readiness- und Analyseberichte.
Jeder aufbewahrte Bericht beginnt mit einem historischen Status-Banner und
erhält seine ursprünglichen Daten, Run-IDs und Commit-Referenzen. Er ist keine
aktuelle Runtime-Evidence.

## Aufbewahrte generierte Snapshots

Wenn für einen generierten Bericht keine neueren verifizierten Eingaben
vorliegen, bewahrt sein Generator den früheren evidenztragenden Snapshot,
statt ihn durch einen leeren Platzhalter zu ersetzen. Das Generated-Markdown
nennt seinen aktuellen Refresh-Status und Grund direkt unter den Metadaten.
Lesen Sie den aktuellen
[Refresh-Manifest](../testing/generated/manifest/report-refresh-manifest.generated.de.md),
bevor Sie einen aufbewahrten Snapshot als aktuellen Bericht behandeln.

Diese Regel bewahrt Provenance, ohne einen alten Full-Matrix-Snapshot als
Ergebnis des aktuellen kompakten Sechs-Connector-Kernlaufs zu promoten.
