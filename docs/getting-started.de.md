# Einstieg

**Sprache:** [English](getting-started.md) | Deutsch

Dieser Guide führt vom frischen Checkout zur ausgewählten Hostkonfiguration
und zur richtigen Einordnung eines Testergebnisses. Er ist ein Einstieg für
Entwicklung und keine Anleitung für ein fertiges Produktionsdeployment.

## 1. Voraussetzungen prüfen

Git und Make, die durch `.python-version` ausgewählte Python-Version sowie
die Host-/Compiler-Voraussetzungen aus dem [Build-Guide](build/README.de.md)
verwenden. Go-Komponenten nutzen zusätzlich `.go-version`. Beide Versionsdateien
sind generierte Ansichten von `ci/tooling/project-versions.lock.json`; ein
fehlender gepinnter Interpreter darf nicht durch eine beliebige Systemversion
ersetzt werden. Siehe [Versions-Pins](reference/version-pins.de.md).

Verschiedene Targets brauchen unterschiedliche Abhängigkeiten. Ein
Dokumentationscheck erfordert nicht die Installation aller Hosts, und ein
fehlendes SDK ist kein Dokumentationsfehler. Die passenden
[Compiler-Guides](build/compilers/README.de.md) verwenden, statt Paketnamen oder
Hostversionen zu erraten.

## 2. Klonen und initialisieren

```sh
git clone --recurse-submodules https://github.com/Easton97-Jens/ModSecurity-conector.git
cd ModSecurity-conector
make check-framework
```

Bereits ohne Submodule geklont? Zuerst `git submodule update --init --recursive`
ausführen. Der Standardpfad des Frameworks ist
`modules/ModSecurity-test-Framework`. Ein externes `FRAMEWORK_ROOT` muss ein
vertrauenswürdiger passender Source-Checkout sein und kein Build-Verzeichnis
oder eine beliebige Systeminstallation.

Für eine beabsichtigte Entwicklungsumgebung stellt das Repository
`make setup-dev` bereit, um Python-Entwicklungsabhängigkeiten über das Framework
vorzubereiten. Das verändert die Entwicklungsumgebung; es installiert oder
qualifiziert nicht jeden Connector-Host. Die aktuellen Build-/Python-Hinweise
für den ausgewählten Interpreter und externe Arbeitspfade beachten.

## 3. Erste Prüfungen ausführen

```sh
make check-active-inventory
make quick-check
```

Der erste Befehl prüft die Zulässigkeit des gesamten
[aktiven Inventars](../modules/ModSecurity-test-Framework/connector_suite/config/testing/active-cases.json), ohne Tests auszuführen.
Der zweite prüft statische Repository-Verträge und zugelassene funktionale
Teilmengen. Die normale Auswahl besitzt eine Kerngrenze von 100 Fällen und eine
getrennt autorisierte geschützte Offline-Python-Ausnahme; diese erweitert nicht
die Connector-E2E-Auswahl. Die ausgewählten Fallzahlen stehen in der Prüfausgabe.

`make test` ausführen, sobald Compiler-, SDK- und Hostvoraussetzungen der
aktiven Auswahl verfügbar sind. Aus Standardaliasen oder Gruppen-/Fallfiltern
keine Qualifikation sämtlicher Profile ableiten. [Tests und Nachweise](testing-and-evidence.de.md)
erklärt die Archivgrenze und die standardmäßig nicht mehr ausgewählte Abdeckung.

## 4. Host und Topologie wählen

| Hostfamilie | Direktes/natives logisches Profil | Weiteres logisches Profil |
| --- | --- | --- |
| Apache | `apache` | — |
| NGINX | `nginx` | — |
| HAProxy | `haproxy-htx` | `haproxy-spoe-spop` |
| Envoy | `envoy-ext-proc` | `envoy-ext-authz` |
| Traefik | `traefik-native-uds` | `traefik-forwardauth` |
| lighttpd | `lighttpd-patched` | `lighttpd-stock` |

Die tatsächlich benötigte Topologie wählen. Autorisierungs-/Companion-Wege
und natives Streaming unterscheiden sich besonders bei der
Request-Body-Sichtbarkeit und bei Aktionen nach Beginn der Response. Der
Stock-lighttpd-Sidecar ist eine eigene Lösung, die den Traffic-Austausch führt.
Vor dem Austausch eines Profils gegen ein anderes den
[Connector-Index](connectors/README.de.md) und die
[Body-Inspection-Matrix](body-inspection-review-matrix.de.md) lesen.

## 5. Ein Beispiel anpassen

Unter [Beispiele](../examples/README.de.md) den passenden Host öffnen. Ein
`safe`-Bundle eignet sich als Lernreferenz; `off` behält native Behandlung ohne
zusätzliche Late-Action-Policy bei. `strict` benötigt eine vom Profil
unterstützte Hostaktion und kann beim Start abgewiesen werden. `all` zeigt das
vollständige Konfigurationslayout, keinen vierten Phase-4-Modus und keine
Garantie für ein ausführbares Bundle.

Vor dem Laden Modul- und Regelpfade, Listener/Upstreams, Service-Identitäten,
private Sockets und Logziele anpassen. Body-Zugriff, Inspection-Limits und
Limitaktionen in Engine-Regeln konfigurieren. Entfernte Connector-Limits für
Requests und Responses sind keine akzeptierten Kompatibilitätsoptionen; bei
bestehenden Einrichtungen [Migration](migration.de.md) beachten.

`SecRuleEngine DetectionOnly`, `SecRuleEngine Off`, einen deaktivierten
Hostconnector und Phase-4-`off` auseinanderhalten: Sie wirken auf
unterschiedlichen Ebenen.

## 6. Ausgewählten Host bauen und validieren

Zum Beispiel nach Vorbereitung der erforderlichen NGINX-Inputs:

```sh
make build-nginx
make check-config-nginx
```

Für andere Hosts ein anderes dokumentiertes Root-Target verwenden; nicht
annehmen, dass jedes logische Profil ein gleichnamiges Make-Target besitzt.
Root-Lifecycle-Namen, logische Profil-IDs und Integrationsmodi sind
unterschiedliche Bezeichner.

Generierte Build-/Runtime-Daten gehören außerhalb des Checkouts. Ein explizites
`BUILD_ROOT` muss ein absoluter beschreibbarer externer Pfad sein; siehe
[Variablen](reference/variables.de.md). Build-Erfolg belegt die Build-Stufe;
ein erfolgreicher Konfigurationscheck belegt, dass der Host die gewählte
Konfiguration akzeptiert. Keines der Ergebnisse beweist allein die
Regeldurchsetzung an echtem Traffic.

## 7. Ergebnisse einordnen und Fehler beheben

| Beobachtung | Nächster Schritt |
| --- | --- |
| Framework fehlt oder falsche Revision | Aufgezeichnete Submodule initialisieren und Versions-Pin-Vertrag prüfen |
| Python- oder SDK-Voraussetzung fehlt | Dokumentierte Target-Voraussetzungen verwenden; Prüfung nicht umgehen |
| Alte Body-Limit-Option wird abgewiesen | Veraltete Connector-Option entfernen und Engine-Regeln anhand des Migrationsguides prüfen |
| Strict-Start wird abgewiesen | Strict-Grenze des Profils lesen; eine abgewiesene Konfiguration nicht als unterstützt darstellen |
| Aktive Gruppe leer, unbekannt oder Quellbindung geändert | Inventar und beabsichtigte Revision prüfen; Auswahl nicht kürzen und Zulassungsprüfung nicht deaktivieren |
| Build/Config besteht, Laufzeitverhalten unbekannt | Gesondert autorisierte profilspezifische Nachweise erheben und validieren |

Exit-Status null gilt für den jeweiligen Befehl und Lauf. Er ist kein Nachweis
für Produktionsreife, CRS-Vollständigkeit, vollständige HTTP/2-/HTTP/3-Abdeckung,
eine vollständige Matrix oder Strict-Verhalten jedes Profils.

## Spezialkampagnen bleiben getrennt

Eine aggregierte Lifecycle-Kampagne nicht als routinemäßigen Setup-Schritt
starten. Eine gesondert autorisierte Prüfung kann mit tatsächlichen
Voraussetzungen und einer nicht geheimen, dateisystemsicheren Run-ID die
folgende dokumentierte Befehlsfolge verwenden:

```sh
run_id="core-$(date -u +%Y%m%dT%H%M%SZ)"
ON_DEMAND_TESTS=1 NO_CRS_RUN_ID="$run_id" make full-lifecycle-all-connectors
NO_CRS_RUN_ID="$run_id" make check-six-connector-core-completion
```

`ON_DEMAND_TESTS=1` ist eine explizite Auswahl für Spezialarbeit und kein
Standard oder allgemeiner Bypass. Es eröffnet abgeschlossene I12-Arbeit nicht
erneut. Geschützte NGINX-Ausführung bleibt eine eigene Vertrauensgrenze. Vor
Laufzeitarbeit [Tests und Nachweise](testing-and-evidence.de.md) sowie
[Betrieb und Sicherheit](operations-and-security.de.md) lesen.
