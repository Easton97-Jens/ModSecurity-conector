# Validierung des Envoy-Connectors

**Sprache:** [English](validation.md) | Deutsch


Status: Connector-Service `compile_verified`; gezielte Envoy ext_authz-Anfrage
Pfad `minimal_runtime_smoke` / `connector-gap`.

## Konfigurationsvalidierung

`config/envoy-ext-authz.conf` ist eine unveränderliche Beispielvorlage. Der Launcher
erstellt eine konkrete Kopie unter `BUILD_ROOT` und ersetzt nur die Regeln und das Ereignis
Wege. Beide können als Befehlszeilen-/Make-Eingaben bereitgestellt werden:

```sh
make -C connectors/envoy check-envoy-config \
  RULES_FILE=/absolute/path/rules.conf \
  EVENT_LOG_PATH=/absolute/runtime/path/events.jsonl
```

Der erstellte Dienst führt `--check-config --config PATH` aus. Ungültige Syntax,
Unbekannte Schlüssel, unsichere Pfade, Regelladefehler, ungültige Status oder Grenzwerte schlagen fehl
der Scheck.

## Anfragefrei Smoke-Test starten

```sh
make -C connectors/envoy start-smoke-envoy \
  ENVOY_BIN=/absolute/path/envoy \
  RULES_FILE=/absolute/path/rules.conf
```

Diese Gate-Konfiguration überprüft den Connector, validiert die generierte Envoy-YAML und startet
Sowohl Connector-Service als auch Envoy, zeichnet beide PIDs/Liveness-Status auf, sendet Nr
Anfrage, stoppt beide und schreibt außerhalb des Checkouts eine Zusammenfassung.

## Echter Envoy-Laufzeitrauch

```sh
make -C connectors/envoy runtime-smoke-envoy \
  ENVOY_BIN=/absolute/path/envoy \
  RULES_FILE=/absolute/path/rules.conf
```

Der Smoke-Test:

1. erstellt eine temporäre Envoy `ext_authz` YAML-Konfiguration;
2. validiert es mit Envoy;
3. startet einen lokalen Upstream, Connector-Dienst und Envoy;
4. erfordert eine zulässige Anfrage zur Rückgabe von HTTP 200;
5. erfordert `X-Modsec-Smoke: block`, um die Regel `1000001` und HTTP 403 auszulösen;
6. erfordert ein gemeinsames Ereignis, das nur aus Metadaten besteht;
7. stoppt alle Prozesse bei Erfolg, Misserfolg oder Signal.

Nur fehlende ausführbare Dateien/Regeleingaben sind GESPERRT/77. Konfigurationsablehnung, früh
Prozessabbruch, Anforderungsfehler, falscher Status oder fehlender Ereignisnachweis ist ein
echtes Scheitern.

Beobachtete lokale Implementierungsnachweise werden außerhalb der Kasse unten aufgeführt
das ausgewählte `BUILD_ROOT`. Es zeichnet `response_body_verified=false` und auf
`production_ready=false`. Body-Payloads werden nicht in das Ereignisprotokoll geschrieben.

## Grenzen

- Das implementierte Modell ist HTTP `ext_authz` in der Anforderungsphase.
- Anforderungstexte werden auf höchstens 4096 Bytes gepuffert; Teilnachrichten sind nicht vorhanden
  durch die Smoke-Konfiguration erlaubt.
- Upstream-Antwortheader und Antworttexte stehen hierfür nicht zur Verfügung
  Protokoll und werden weiterhin nicht unterstützt.
- Der angestrebte 200/403-Smoke-Test ist nicht CRS-vollständig, Vollmatrix, Sicherheit oder
  Produktionsnachweise.

## Kanonische Phase-4-Validierung

Der Envoy HTTP `ext_authz` wird vor der Upstream-Verarbeitung aufgerufen.  Der ausgewählte Gastgeber
Der Pfad kann daher die Header oder den Hauptteil der Upstream-Antwort nicht beobachten
`response_body_buffered`, `phase4`, `phase4_rule_evaluation`,
`phase4_pre_commit_deny`, `late_intervention`, `late_intervention_log_only`,
`late_intervention_abort` und `late_intervention_status_metadata` sind
`unsupported_by_host_model`.

Die kanonischen Phase-4-Fälle müssen daher `UNSUPPORTED` lauten
genaue Host-Modell-Grenze als Grund.  Die Anforderungsseite erlaubt/verweigert Smoke-Test
Antworttextregel kann nicht nachgewiesen werden, Antwortverweigerung vor dem Commit, Post-Commit
Nur-Protokoll-Ergebnis, Abbruch, ursprünglicher Upstream-Status oder sichtbarer Post-Eingriff
Status.  `UNSUPPORTED` ist nicht `PASS` und es ist keine Nutzlast für den Antworttext zulässig
in einer Veranstaltung oder einem Bericht.

## Separate ext_proc-Prüfungen

Der Go/CGo ext_proc-Pfad verfügt über die folgenden Connector-lokalen Prüfungen:

```sh
make -C connectors/envoy test-envoy-ext-proc \
  MODSECURITY_INCLUDE_DIR=/absolute/prefix/include \
  MODSECURITY_LIB_DIR=/absolute/prefix/lib
make -C connectors/envoy check-envoy-ext-proc-config
make -C connectors/envoy prepare-envoy-ext-proc-config
make -C connectors/envoy prepare-envoy-ext-proc-runtime-config
make -C connectors/envoy runtime-smoke-envoy-ext-proc \
  ENVOY_BIN=/absolute/path/to/envoy \
  MODSECURITY_INCLUDE_DIR=/absolute/prefix/include \
  MODSECURITY_LIB_DIR=/absolute/prefix/lib
```

Die reinen Quelltests decken das Verhalten des Protobuf-Dienstes ab; mit den expliziten Pfaden,
Das gleiche Ziel kompiliert und testet auch die CGo Common/libmodsecurity-Brücke für
P1/P2/P3/P4, inkrementelles EOS, Abbruch, Commit-Reihenfolge und parallel
Transaktionen. Die Vorlage verfügt über `STREAMED`-Anforderungs-/Antwortkörpermodi,
Anhänger-EOS-Lieferung und kein `BUFFERED`-Modus. Der Laufzeitrauch ruft real auf
Envoy wählt nur `ext_proc` aus, führt die Common/libmodsecurity-Regeln aus und
prüft run-local raw Common Decision JSONL plus vom Host bestätigtes Deny, Redirect,
und sichere Nur-Protokoll-Aktionen. Es beweist keinen Timeout/Reset/Client-Abbruch/Upstream-
Abort/First-Byte/Client-Byte oder HTTP/2-Verhalten, und es fördert kein
ext_proc-Fähigkeit oder kanonisches Laufzeitergebnis.
