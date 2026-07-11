# Einsatzreife der verbleibenden Connectoren: Envoy, Traefik und lighttpd

**Sprache:** [English](remaining-connectors-readiness.md) | Deutsch

> **Hinweis zum Evidence-Umfang.** Dies ist ein historischer lokaler
> Evidence-Snapshot, kein kanonisches No-CRS-Ergebnis und kein aktueller
> aggregierter Capability-Status. Die nachfolgenden
> `minimal_runtime_smoke`-Bezeichnungen beziehen sich nur auf die aufgezeichneten
> Läufe vom 10.07.2026. Der generierte
> [No-CRS-Gesamtsnapshot](all-connectors-no-crs-baseline.de.md) und die
> [kanonische Capability-Matrix](testing/generated/canonical/connector-capabilities.generated.de.md)
> sind maßgeblich für den aktuellen Status; nur kanonische `result.json`-Dateien
> können ein No-CRS-Ergebnis heraufstufen.

Belegstand: 10.07.2026

## Ergebnis

Envoy, Traefik und lighttpd besitzen jeweils `minimal_runtime_smoke`-Belege für
einen engen lokalen Anfragekopfpfad durch einen echten Host-Prozess, den
repository-eigenen Connector, die Common-Laufzeit und libmodsecurity. Jeder
Pfad belegt ein erlaubtes HTTP 200, eine Ablehnung durch Regel `1000001` mit
HTTP 403 und ein reines Metadatenereignis.

Die Belege sind bewusst connectorspezifisch und eng begrenzt. Zusammen ergeben
sie keine Aussage über vollständige Connector-Abdeckung. Insbesondere bleiben
Körperdaten, Antworten, CRS, breite Testmatrizen, Sicherheit, betriebliche
Härtung und Langzeitbetrieb außerhalb des belegten Umfangs.

## Lückenmatrix

„Erfolgreich“ bezeichnet in dieser Matrix die unten beschriebenen lokalen
Belege vom 10.07.2026. „Implementiert“ ohne „geprüft“ bedeutet, dass Code
vorhanden ist, der gezielte Laufzeittest für diese Spalte aber keine
Verhaltensaussage prüfte.

| Connector | Host-Integration | Common SDK | Konfiguration | Anfrage | Anfragekörper | Antwort | Antwortkörper | Entscheidung | Ereignisse | Bauvorgang | Start | Minimale Laufzeit |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Envoy | Echter HTTP-`ext_authz`-Dienst durch Envoy verwendet | Aktiver Pfad für Konfiguration, generische Mapper und Laufzeit | Common-Prüfung und Envoy-YAML-Validierung erfolgreich | Echter GET-/Kopfpfad; 200/403 | Pufferung bis 4096 Byte konfiguriert; nicht ausgeführt | Nachgelagerte Antwort für Dienst nicht verfügbar | Nicht unterstützt | Anfrageentscheidung aus Regel `1000001` -> 403 | Common-JSONL-Metadaten; keine Körpernutzdaten | C17-Dienst erfolgreich kompiliert und gelinkt | Dienst und Envoy aktiv/beendet; keine Anfragen | `minimal_runtime_smoke` |
| Traefik | Echter HTTP-`forwardAuth`-Dienst durch Traefik verwendet | Aktiver Pfad für Konfiguration, generische Mapper und Laufzeit | Dienstkonfiguration und `File Provider`-Pfad erfolgreich | Echter GET-/Kopfpfad; 200/403 | Nicht übertragen oder ausgeführt; Ergebnis enthält false | Nachgelagerte Antwort nicht verfügbar; nur Autorisierungsantwort | Nicht unterstützt | Anfrageentscheidung aus Regel `1000001` -> 403 | Common-JSONL-Metadaten; keine Körpernutzdaten | C17-Dienst erfolgreich kompiliert und gelinkt | Dienst und Traefik aktiv/beendet; keine Anfragen | `minimal_runtime_smoke` |
| lighttpd | Natives `mod_msconnector.so` durch lighttpd geladen | Aktiver Pfad für Konfiguration, generische Mapper und Laufzeit | Echtes Modulladen und Common-Regelkonfiguration erfolgreich | Echter `OPTIONS *`-/Kopfpfad; 200/403 | Nicht unterstützt; Modus muss `none` sein | Kopf-Rückruf implementiert; keine antwortspezifische Prüfung | Nicht unterstützt; Modus muss `none` sein | Phase-1-Regel `1000001` -> 403 | Common-JSONL-Metadaten; keine Körpernutzdaten | C17-PIC-Modul erfolgreich kompiliert und gelinkt | lighttpd aktiv/beendet; keine Anfragen | `minimal_runtime_smoke` |

## Implementierte Architekturen

### Envoy

Der primäre Pfad ist ein repository-eigener externer HTTP-Autorisierungsdienst
für Envoy `ext_authz`. Connector-lokaler C17-Code definiert Envoy-Hostprofil
und dünne Common-Mapper-Rückrufe. Der gemeinsame HTTP-Autorisierungsdienst und
die libmodsecurity-Transaktionslaufzeit bleiben connector-neutral.

### Traefik

Der primäre Pfad ist ein repository-eigener externer HTTP-`forwardAuth`-Dienst.
Er ist weder Go-Plugin noch cgo-Modul. Traefik prüft die Autorisierung vor der
Anfrage an den nachgelagerten Dienst; der Connector sieht dessen spätere
Antwort deshalb nicht.

### lighttpd

Der primäre Pfad ist ein natives repository-eigenes lighttpd-Plugin. Es
registriert die Serverkonfiguration, bildet Anfrage- und Antwortköpfe ab,
beginnt und beendet eine Common-Transaktion, überträgt eine Phase-1-Ablehnung
auf lighttpd und räumt beim Zurücksetzen der Anfrage auf. Körpermodi werden
abgelehnt, wenn sie nicht `none` sind.

## Common-SDK-Anbindung

Alle drei Connectoren verwenden echte Funktionen statt wirkungsloser
Makro-Aliase:

- `msconnector_generic_config_init()`
- `msconnector_generic_map_request()`
- `msconnector_generic_map_response()`
- Common-Konfigurationsparser und -validierung sowie Regelladen
- Common-Pfade für Transaktions-ID, Entscheidung und Aktion, Intervention,
  Status, Ressourcenschutz, Ablauf und Integrität, Ereignis und JSONL

Hostspezifische Typen, Profile, Rückrufsignaturen und Hostkonfigurationen bleiben
in den jeweiligen Connector-Verzeichnissen. Die zusammengefassten statischen
Prüfungen waren erfolgreich:

```sh
make check-remaining-connectors-common-adoption
make check-remaining-connectors-host-integration
make check-remaining-connectors-build-wiring
make check-remaining-connectors-start-wiring
```

## Reproduktionsbefehle und Belege

Die übergeordneten Repository-Hilfsskripte lösen verwaltete lokale
Host-Programme, Kopfdateien und libmodsecurity-Pfade auf oder stellen sie bereit.
Bauvorgang, Konfiguration, Start und Laufzeit bleiben getrennte Belegstufen.

| Connector | Bauvorgang | Konfiguration | Anfragefreier Start | Echter Host-Laufzeitpfad |
|---|---|---|---|---|
| Envoy | `make build-envoy-connector` | `make check-envoy-config` | `make start-smoke-envoy` | `make runtime-smoke-envoy` |
| Traefik | `make build-traefik-connector` | `make check-traefik-config` | `make start-smoke-traefik` | `make runtime-smoke-traefik` |
| lighttpd | `make build-lighttpd-connector` | `make check-lighttpd-config` | `make start-smoke-lighttpd` | `make runtime-smoke-lighttpd` |

Zusammengefasste Einstiegspunkte sind:

```sh
make build-remaining-connectors
make start-smoke-remaining-connectors
make runtime-smoke-remaining-connectors
make readiness-remaining-connectors
```

Die beobachteten engen Laufzeitbelege waren:

| Connector | Verwaltete Host-Version | Erlaubt | Blockiert | Regel-/Ereignisbeleg |
|---|---:|---:|---:|---|
| Envoy | 1.38.2 | 200 | 403 | `envoy`, `envoy-block-1`, `1000001` |
| Traefik | 3.7.5 | 200 | 403 | `traefik`, `traefik-forwardauth-block`, `1000001` |
| lighttpd | 1.4.84 | 200 | 403 | `lighttpd`, Anfragekopfphase, `1000001` |

Die standardmäßigen lokalen Belegpfade liegen unter
`/var/tmp/ModSecurity-conector-verified/build/`. Es handelt sich um
reproduzierbare Arbeitsbereichsartefakte, nicht um aufbewahrte,
plattformübergreifende CI-Belege. Fehlende Voraussetzungen vor dem Lauf dürfen
BLOCKED/77 ergeben; vorhandene Fehler bei Bauvorgang, Konfiguration, Start,
Abbildung, Status oder Ereignissen sind Fehlschläge.

## Connectorübergreifende Grenzen und verbleibende Arbeit

- Begrenzte Übertragung von Anfragekörpern und Verhaltensprüfungen ergänzen, wo
  das Host-Modell dies ermöglicht; andernfalls die ausdrückliche
  Nichtunterstützung beibehalten.
- Antwortkopfprüfungen nur für Host-Modelle ergänzen, die die Antwort tatsächlich
  bereitstellen; aus einem gelinkten generischen Mapper keine Antwortfähigkeit
  ableiten.
- Antwortkörpererfassung und späte Intervention erst entwerfen, wenn ein
  Host-Rückruf und ein sicheres Puffermodell vorhanden sind.
- Eingebettete und entfernte Regeln sowie breitere Common-Direktivenkombinationen
  erst ausführen, nachdem jeder Host sie ausdrücklich abbildet.
- Negative Konfiguration, Grenzen, Abschneidung, fehlerhafte Eingaben,
  Umleitung, Verbindungsabbruch, Parallelität, Langzeitstabilität und Leistung
  abdecken.
- Connectorgeeignete Matrizen ohne und mit CRS ausführen, bevor eine breitere
  Belegaussage geändert wird.
- Reproduzierbare CI-Artefakte für unterstützte Plattformen und Host-Versionen
  aufbewahren.
- Eine eigene Sicherheitsprüfung und betriebliche Härtung durchführen.

Connectorspezifische Einzelheiten stehen in:

- `reports/envoy-connector-readiness.de.md`
- `reports/traefik-connector-readiness.de.md`
- `reports/lighttpd-connector-readiness.de.md`

## Durch die Belege gestützte Aussagen

- Jeder Connector besitzt einen echten hostintegrierten Anfragekopfpfad mit
  Common-Laufzeit und libmodsecurity.
- Bauvorgang, Konfigurationsprüfung, anfragefreier Starttest und Laufzeittest sind bei
  jedem Connector unterscheidbare Stufen.
- Jeder gezielte Laufzeitpfad hat `minimal_runtime_smoke`-Belege für HTTP
  200/403 und reine Regelmetadaten.
- Der ältere lighttpd-Brücken-Selbsttest ist vom Laufzeitnachweis des nativen
  Host-Pfads getrennt.

## Bewusst nicht erhobene Claims

- Produktionsreife oder Produktionshärtung eines Connectors
- sichere Laufzeit oder bestätigte Sicherheit eines Connectors
- CRS-Bestätigung oder CRS-Vollständigkeit
- Bestätigung einer vollständigen Testmatrix
- Bestätigung von Anfragekörpern über alle drei Connectoren
- Bestätigung nachgelagerter Antworten oder Antwortkörper
- breite Plattform- oder Hostversionskompatibilität
- Bestätigung aller Connectoren oder jeder Connector-Fähigkeit
