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

Dies validiert statische Repository-Verträge und zugelassene funktionale
Teilmengen des einzigen [Aktivinventars](../config/testing/active-cases.json).
Die globale Grenze beträgt 100 vollständig expandierte Verhaltensfälle,
einschließlich Infrastruktur- und Runtime-Fällen. Mit
<code>make check-active-inventory</code> wird die vollständige Auswahl vor einem
Teststart geprüft. <code>make test</code> führt die aktive Auswahl aus und
benötigt ihre echten Compiler-, SDK- und Hostvoraussetzungen. Gruppen-/Fallfilter
und Standardaliase sind Teilmengen, keine vollständige Profilqualifikation.
Details zu Archiv, verlorener Abdeckung und getrennten Profilen stehen unter
[Tests und Nachweise](testing-and-evidence.de.md).

## Nächsten Guide auswählen

| Ziel | Kanonischer Guide |
| --- | --- |
| Einen Host bauen, konfigurieren oder starten | [Build](build/README.de.md) und der passende [Connector-Guide](connectors/README.de.md) |
| Ein Profil oder eine Direktive anpassen | [Konfiguration](configuration.de.md) und die vollständige Connector-Referenz in `examples/` |
| Evidence ausführen oder deuten | [Tests und Nachweise](testing-and-evidence.de.md) |
| Limits, Datenschutz, Origin oder Betrieb prüfen | [Betrieb und Sicherheit](operations-and-security.de.md) |

Nur für eine separat autorisierte Spezialprüfung bleibt folgendes breiteres
Aggregatbeispiel erhalten. Es liegt außerhalb automatischer Standardauswahl,
benötigt <code>ON_DEMAND_TESTS=1</code> und eröffnet keine geschlossene I12-
Kampagne. Eine dateisystemsichere, nicht geheime Run-ID verwenden:

```sh
run_id="core-$(date -u +%Y%m%dT%H%M%SZ)"
ON_DEMAND_TESTS=1 NO_CRS_RUN_ID="$run_id" make full-lifecycle-all-connectors
NO_CRS_RUN_ID="$run_id" make check-six-connector-core-completion
```

Ein Exit-Status null gilt nur für den aufgezeichneten Befehl und den
ausgewählten Lauf. Er behauptet weder Produktionsreife, CRS-Verifikation,
vollständige Protokollabdeckung, eine vollständige Matrix noch Strict-Verhalten
für jeden Connector.
