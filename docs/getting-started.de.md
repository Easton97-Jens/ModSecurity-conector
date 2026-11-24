# Einstieg

**Sprache:** [English](getting-started.md) | Deutsch

## 1. Voraussetzungen prüfen

Git, Make und den durch `.python-version` gepinnten Interpreter verwenden.
Go-Komponenten folgen `.go-version`. Die [Build-Voraussetzungen](build/README.de.md)
des Hosts und die [Versions-Pins](reference/version-pins.de.md) prüfen.

## 2. Klonen und initialisieren

```sh
git clone --recurse-submodules https://github.com/Easton97-Jens/ModSecurity-conector.git
cd ModSecurity-conector
make check-framework
```

Wenn einem bestehenden Checkout Submodule fehlen, zuerst
`git submodule update --init --recursive` ausführen. Das Framework liegt
standardmäßig unter `modules/ModSecurity-test-Framework`. Bei abweichendem
`FRAMEWORK_ROOT` einen vertrauenswürdigen Checkout der passenden Revision verwenden.

Lokal rufen delegierte Targets `make python-env` auf, um die gepinnte
Python-Umgebung mit den gelockten Framework-Abhängigkeiten bereitzustellen.
Mit `PYTHON_ENV_ROOT` liegt die Umgebung außerhalb des Checkouts.
Mit `PYTHON` lässt sich ein vorbereiteter Interpreter wählen. Siehe
[Variablenreferenz](reference/variables.de.md).

## 3. Erste Prüfungen ausführen

```sh
make check-active-inventory
make quick-check
```

`make check-active-inventory` prüft die Testauswahl. `make quick-check` führt
statische Checks und zugelassene funktionale Teilmengen aus. Für `make test`
die Compiler-, SDK- und Hostvoraussetzungen der aktiven Auswahl vorbereiten.
[Tests und Nachweise](testing-and-evidence.de.md) beschreibt die abgedeckten Fälle.

## 4. Host und Topologie wählen

Ein [logisches Connector-Profil](connectors/README.de.md) auswählen und dessen
[Body-Inspection-Grenzen](body-inspection-review-matrix.de.md) prüfen.

## 5. Ein Beispiel anpassen

Mit dem passenden [Beispielbundle](../examples/README.de.md) beginnen. Pfade,
Listener, Upstreams, Service-Identitäten, private Sockets und Logziele anpassen.
Body-Zugriff und Limits in den Engine-Regeln einstellen. Für eine ältere
Konfiguration die [Migration](migration.de.md) beachten.

## 6. Ausgewählten Host bauen und validieren

Zum Beispiel mit vorbereiteten NGINX-Voraussetzungen:

```sh
make build-nginx
make check-config-nginx
```

Weitere Host-Targets stehen im [Build-Guide](build/README.de.md). Ein explizites
`BUILD_ROOT` muss ein absoluter, beschreibbarer Pfad außerhalb des Checkouts sein.
Siehe [Variablen](reference/variables.de.md).

## 7. Ergebnisse einordnen und Fehler beheben

Ein Build prüft die Kompilierung. Ein Konfigurationscheck prüft, ob der Host
die ausgewählte Konfiguration lädt. Wie Regeln auf Traffic wirken, zeigen
profilspezifische [Laufzeitnachweise](testing-and-evidence.de.md).

- Bei fehlendem Framework oder falscher Revision die [Versions-Pins](reference/version-pins.de.md) prüfen.
- Bei abgewiesenen Altoptionen die [Migration](migration.de.md) lesen. Bei
  abgewiesenem Strict-Start die Anforderungen an späte Aktionen des Profils prüfen.
- Bei leerer oder abgewiesener Auswahl das [aktive Inventar](../modules/ModSecurity-test-Framework/connector_suite/config/testing/active-cases.json)
  und die ausgecheckte Revision prüfen.

## Spezialkampagnen bleiben getrennt

[Tests und Nachweise](testing-and-evidence.de.md) erklärt Voraussetzungen und
Opt-in für vollständige Lifecycle-Läufe und geschützte Hostprüfungen.
