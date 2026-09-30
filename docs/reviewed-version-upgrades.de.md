# Geprüfte Versionswechsel

**Sprache:** [English](reviewed-version-upgrades.md) | Deutsch

## Zuständigkeit und Freigabe

Die Framework-Datei `ci/lib/common.sh` definiert die geprüften Upstream-Identitäten. Die Parent-Verbraucher müssen dazu passen; Konsistenz ist jedoch keine Freigabe einer neuen Version. NGINX und ModSecurity bleiben außerhalb der generischen Liste veränderlicher Quellfelder. Eine geänderte Quellstruktur benötigt eine ausdrückliche Prüfung, bevor der Parent-Strukturhash aktualisiert wird. Niemals einen neuen Hash ohne Prüfung des vollständigen Kandidatenunterschieds übernehmen.

## Frühe Konsistenzprüfung

`ci/tools/check-reviewed-version-handoff.py` liest begrenzte reguläre Dateien als Daten. Geprüft werden die bestehende Strukturfreigabe, das Framework-NGINX-Release gegen Workflow und Evidence-Writer sowie ModSecurity-v3-Tag und -Commit gegen Anleitungs-Generator, dessen Tests und beide generierten Anleitungen. Netzwerkzugriff, Shell-Auswertung, Quellschreibzugriff und Paketinstallation finden nicht statt. Fehlende, widersprüchliche, unsichere oder symbolisch verlinkte Eingaben werden abgelehnt. Die frühe Quick-Prüfung läuft vor dem aufwendigen Setup; vollständige Kandidaten- und Laufzeitprüfungen bleiben erforderlich.

```sh
python3 ci/tools/check-reviewed-version-handoff.py --repo-root .
python3 -m unittest -v tests.test_reviewed_version_handoff tests.test_runtime_component_cache_identity
```

## Eine Version wechseln

Offizielles Quellrepository, Release-Tag, exakten Commit und gegebenenfalls Archivprüfsumme gemeinsam prüfen. Framework-Referenz, begrenzte Parent-Projektionen und ausdrückliche Strukturfreigabe atomar aktualisieren. Generierte Bauanleitungen über `scripts/generate_compiler_guides.py` aktualisieren, nicht deren erzeugtes Markdown direkt bearbeiten. Der unabhängig geschützte NGINX-Broker behält seinen eigenen Review-Pfad. Die geprüfte Quellidentität nicht durch Umgebungsvariablen überschreiben.

## Neubau und Laufzeitabnahme

Die ModSecurity-Cache-Identität enthält tatsächlichen Quellcommit, Submodulstatus, Buildflags, Toolchain und Abhängigkeiten. Die Apache- und NGINX-Connector-Identitäten hängen von der ModSecurity-Buildidentität ab. Regressionen prüfen diese Invalidierungsgrenzen und das erwartete `libmodsecurity.so.3`-Aliaslayout anhand synthetischer Dateien; sie belegen keine binäre ABI-Kompatibilität. Ein echter Wechsel erfordert weiterhin zusammenpassende Header-, Bibliotheks- und Connector-Builds, Upstream-Tests sowie echte Allow-/Block-, Request-/Response-Body-, Callback-, Logging-, Reload- und Shutdown-Prüfungen. Eine zukünftige Hauptversion oder SONAME wird nicht automatisch akzeptiert.

## Nachweise und lokales Python

Exakten Commit, Befehl, Exitstatus und übersprungene Fähigkeiten ehrlich angeben. Privilegierte Namespace-Tests benötigen einen aufgelösten Interpreter innerhalb der bestehenden Jail-Laufzeitliste statt eines externen virtuellen Alias. Die Aliasauflösung erlaubt weder das Einhängen seines schreibbaren Elternverzeichnisses noch eine Abschwächung der Jail. Erfolgreiche Quell- oder Dateisystemtests belegen weder native WAF-Funktion noch Kompatibilität zukünftiger Releases. GitHub-CI und Sonar müssen am finalen PR-Head geprüft werden, bevor der PR als fertig gilt.
