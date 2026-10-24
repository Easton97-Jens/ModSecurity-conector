# Phase-4-Migrationskonsistenz und Prüfung vor dem Merge

**Sprache:** [English](CR-20260920-phase4-migration-ci.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260920-phase4-migration-ci` |
| Datum (UTC) | `2026-09-20` |
| Basis-Revision | `0819bd819bf6f699149adb8fcdd067895abd0862` |

## Motivation und Problemstellung

PR #380 enthielt nur einen Teil der Migration von minimal/safe/strict zu
off/safe/strict mit Engine-eigener MIME-Auswahl. Veraltete Source-Contract-Tests,
unvollständig verschobene Beispiele, alte generierte Dokumentation und
PR-Schritte, die den eigentlichen Lint-Lauf übersprangen, verdeckten Fehler bis
nach dem Merge.

## Akzeptanzkriterien

Der bestehende PR behält seine Änderungen und enthält zusätzlich konsistente
Off-Profile, quellbasierte EN/DE-Referenzen und Fähigkeitsbeschreibungen.
NGINX-Mutationstests weisen unerreichbare Body-Aufrufe und ignorierte Fehler ab.
Dieselben lint/quick-check-Befehle laufen vor und nach dem Merge. Kein Schutz
und keine Runtime-Durchsetzung werden für einen grünen Check abgeschwächt.

## Implementierungsentscheidung und Begründung

Begrenzte Body-Verarbeitung, natives Off-Verhalten und Safe-/Strict-Verhalten
bleiben erhalten. Tests des entfernten MIME-Laders werden durch Prüfungen
seiner Abwesenheit und der Engine-Zuständigkeit ersetzt. Der vollständige
direkte Chain-Aufruf samt Fehlerrückgabe wird statt einer Textzählung geprüft.
Die übrigen HAProxy-SPOE/SPOP-Begleitdateien werden nach off verschoben;
Host-/Agent-Socketpfade bleiben identisch. Referenzen werden durch ihre
Generatoren erneuert. Historische Evidence und Fähigkeitszustände bleiben
erhalten.

## Geänderte Dateien

Betroffen sind die fünf Lint-/Struktur-Workflows, der NGINX-Adoption-Checker
und seine drei Regressionssuiten, der neue Phase-4-Migrationsguard,
Konfigurations-/Guide-Generatoren samt Tests, der Common-Event-Metadatenkommentar,
aktuelle Connector-Fähigkeitsbeschreibungen, aktive Off-Beispiele samt
README-Sprachpaaren, generierte Konfigurationsreferenzen/Inventar und dieses
EN/DE-Protokoll. Generierte Fähigkeitskataloge werden ohne Runtime-Hochstufung
aus Manifesten aktualisiert. Framework-/MRTS-Quellen und Pins bleiben unverändert.

## Ausgeführte Befehle

Lokale Prüfungen nutzten Python-APIs auf einem authentifizierten Archiv der
versionierten Quellen: 33 Migrations-/Native-/Upstream-Sicherheitstests,
96 Checker-Mutationstests, 20 Konfigurations-/Guide-Tests und
34 Workflow-Regressionstests bestanden. Die 21 Konfigurationsreferenzausgaben
und ihr vollständiger Semantikchecker bestanden, ebenso die Validierung der
sechs Fähigkeitsmanifeste und der NGINX-Adoption-Checker.

Ergänzende Fähigkeits-/Wiring-Tests führten 38 Tests ohne Fehler und mit drei
Framework-abhängigen Skips aus. Runtime-Evidence-Tests führten 58 Tests mit
einem Fehlschlag, zwei Fehlern und drei Skips wegen des fehlenden
Git-Checkouts/Framework-Katalogs im Archiv aus. Dies sind keine bestandenen
Gesamtsuiten. Hosted-Läufe verwenden den echten Git-Checkout, rekursiv
gepinnten Submodule und die Repository-Python-Version für die maßgebliche
Prüfung vor dem Merge.

## Security-Auswirkung

Kein Runtime-Fail-closed-Zweig, Ressourcenlimit, Logdateischutz, Regel-Lade-
Vertrag, CI-Erfordernis oder Branchschutz wird gelockert. Die Regressionstests
sichern Aufruferreichbarkeit und Fehlerweitergabe stärker ab. CI-Ausführung
verwendet lesende Repository-Rechte; Veröffentlichung und Tests sind getrennt.

## Runtime-Evidence

Kein neues client-sichtbares NGINX-/Apache-/anderes Hostergebnis wird behauptet.
Quell-, Generator- und Mutationstests belegen keine Runtime-Response-Blockierung.

## Bekannte Einschränkungen

Dem lokalen Archiv fehlen Git-Metadaten, Submodulinhalte und native
Host-Build-Voraussetzungen. Hosted-Checks belegen jeweils ihre eigene Testebene.

## Verbleibende Risiken

Hostspezifischer Response-Commit und unterstütztes Abbruchverhalten benötigen
weiterhin die ausgewählten nativen Runtime-Profile. Alte datierte Berichte
bleiben historisch und belegen nicht die Prüfung des aktuellen Heads.

## Nicht ausgeführte Prüfungen mit Begründung

Kein vollständiger lokaler nativer Build und keine Sechs-Connector-Runtime-Matrix
wurden ausgeführt. Merge, Release, Dependency-Upgrade oder externes Deployment
waren nicht beauftragt.

## Finaler Diff- und Review-Status

Quelländerungen und generierte Referenzdifferenzen wurden zusammen geprüft.
Dieses Protokoll dokumentiert lokale Evidence; finale Hosted-Ergebnisse gehören
zum exakten PR-Head und werden nicht aus einem übersprungenen oder früheren
grünen Job abgeleitet. Der PR wird nicht automatisch gemergt.
