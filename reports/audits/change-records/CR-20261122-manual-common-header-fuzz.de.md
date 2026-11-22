# Change Record CR-20261122-manual-common-header-fuzz

**Sprache:** [English](CR-20261122-manual-common-header-fuzz.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261122-manual-common-header-fuzz |
| Datum (UTC) | 2026-11-22 |
| Basis-Revision | `d21e34eb42b7e12793f670e318954798293bb897` |

## Motivation und Problemstellung

Den vorhandenen Fuzz-Test für gemeinsame HTTP-Header für Maintainer in GitHub Actions verfügbar machen.

## Akzeptanzkriterien

Der Workflow startet über `workflow_dispatch`, führt das vorhandene begrenzte Make-Target auf einem GitHub-gehosteten Runner aus und meldet einen Testfehler als Jobfehler.

## Implementierungsentscheidung und Begründung

Die ausgewählte Connector-Revision liefert die Produktquellen. Der vermerkte Framework-Gitlink liefert den Test. Der anfängliche Gitlink ist `b4d619127a3fbd2a4074998e874c592d693413b9`.

Auf dem Standardbranch steht **Actions → Common HTTP header fuzzing → Run workflow** zur Verfügung.

## Geänderte Dateien

- `.github/workflows/fuzz-common.yml`
- Dieses englische und deutsche Change-Record-Paar.

## Ausgeführte Befehle

Das im Repository festgelegte `actionlint` mit der Repository-Konfiguration und `bash -n` lieferten jeweils Exitcode `0`. Der unveränderte Shell-Schritt des Workflows lieferte bei der lokalen Ausführung mit Clang 19.1.7 Exitcode `0`.

Mit verfügbarem Clang und einem beschreibbaren absoluten Pfad außerhalb der Worktrees für `BUILD_ROOT` lautet der lokale Aufruf:

```sh
rtk make ON_DEMAND_TESTS=1 BUILD_ROOT="$BUILD_ROOT" check-common-http-header-fuzz
```

## Security-Auswirkung

Der Job hat ein Zeitlimit von fünf Minuten, verwendet Leserechte und speichert beim Checkout keine Zugangsdaten. Build, temporäre Compilerdateien und vollständige Fuzz-Ausgabe bleiben in einem laufbezogenen temporären Verzeichnis. Der Job veröffentlicht nur den Teststatus.

## Runtime-Evidence

Der vorhandene Fuzz-Test im selben Prozess wurde lokal abgeschlossen. Der Test startet keinen Connector-Dienst.

## Bekannte Einschränkungen

Die Prüfung deckt die gemeinsamen HTTP-Header-Helfer ab. Der verfügbare Test folgt dem Framework-Gitlink der ausgewählten Connector-Revision.

## Verbleibende Risiken

Der begrenzte Lauf prüft 15 Sekunden lang generierte Eingaben. Die festen Regressionstests decken die kontinuierliche Prüfung ab.

## Nicht ausgeführte Prüfungen mit Begründung

Ein manueller Lauf auf GitHub steht aus, bis der Workflow auf dem Standardbranch verfügbar ist. Bei der lokalen Prüfung war LeakSanitizer wegen der eingeschränkten Prozessinspektion in der Sandbox deaktiviert.

## Finaler Diff- und Review-Status

Der Diff ergänzt den manuellen Workflow und das Change-Record-Paar. Das aktuelle Pull-Request-Testinventar gilt weiter.
