# Einstieg

**Sprache:** [English](getting-started.md) | Deutsch

## Geltungsbereich

Dies ist der kürzeste sichere Weg von einem frischen Checkout zur
Repository-Validierung. Er bereitet weder ein Produktionsdeployment noch einen
allgemeinen Runtime-Claim vor.

## Framework initialisieren

```sh
git submodule update --init --recursive
make check-framework
```

`FRAMEWORK_ROOT` wählt normalerweise `modules/ModSecurity-test-Framework`.
Der Wert darf nur auf einen vertrauenswürdigen, bestehenden Framework-Checkout
außerhalb dieses Repositorys gesetzt werden. Eine fehlende Voraussetzung wird
als dokumentierte Blocked-/Prerequisite-Exit-Bedingung gemeldet; eine
nicht zusammenhängende Systeminstallation ist kein Ersatz.

## Checkout validieren

```sh
make quick-check
```

Dies validiert Repository-Verträge, Dokumentation und ausgewählte strukturelle
Prüfungen. Es baut nicht jeden Host, führt nicht den gesamten Connector-Traffic
aus und erzeugt keine kanonische Lifecycle-Evidence.

## Nächsten Guide auswählen

| Ziel | Kanonischer Guide |
| --- | --- |
| Einen Host bauen, konfigurieren oder starten | [Build](build/README.de.md) und der passende [Connector-Guide](connectors/README.de.md) |
| Ein Profil oder eine Direktive anpassen | [Konfiguration](configuration.de.md) und die vollständige Connector-Referenz in `examples/` |
| Evidence ausführen oder deuten | [Tests und Nachweise](testing-and-evidence.de.md) |
| Limits, Datenschutz, Origin oder Betrieb prüfen | [Betrieb und Sicherheit](operations-and-security.de.md) |

Für einen ausgewählten Aggregatlauf wird eine dateisystemsichere, nicht geheime
Run-ID verwendet:

```sh
run_id="core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-all-connectors
NO_CRS_RUN_ID="$run_id" make check-six-connector-core-completion
```

Ein Exit-Status null gilt nur für den aufgezeichneten Befehl und den
ausgewählten Lauf. Er behauptet weder Produktionsreife, CRS-Verifikation,
vollständige Protokollabdeckung, eine vollständige Matrix noch Strict-Verhalten
für jeden Connector.
