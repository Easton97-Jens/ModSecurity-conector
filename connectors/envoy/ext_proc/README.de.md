# Envoy `ext_proc` Common/libmodsecurity Pfad für den gesamten Lebenszyklus

**Sprache:** [English](README.md) | Deutsch

Dieses Verzeichnis ist eine angeheftete Go-Implementierung des Beamten von Envoy
`envoy.service.ext_proc.v3.ExternalProcessor` gRPC-Schnittstelle. Es ist getrennt
vom vorhandenen C `ext_authz`-Dienst und ändert den ausgewählten nicht,
laufzeitnachweisbarer Nur-Anfrage-Pfad.

Der kanonische Full-Lifecycle-Dispatcher wählt diesen Dienst aus
`full-lifecycle-envoy-ext-proc`; es entspricht nicht dem Standard
`ext_authz` Kompatibilitätsläufer. Die ausführbare Datei verknüpft ein Connector-lokales CGo
ABI zu Common Runtime und libmodsecurity, während die Funktionserweiterung weiterhin besteht
gesonderte Entscheidung zur Beweiswürdigung.

## Was hier implementiert ist

– ein unabhängiger `streamState` und Transaktions-Seam pro gRPC `Process`-Aufruf;
– eine echte Common/libmodsecurity-Transaktion pro Stream, geöffnet von Envoy
  Tatsächliche Anforderungsheader werden gelöscht und bei EOS, Abbruch oder Prozessor vernichtet
  Scheitern;
- begrenzte Anforderungs-/Antwort-Header-Zuordnung und inkrementelle Body-Callbacks;
- keine vollständige Sammlung von Anfrage- oder Antworttexten; Staat behält nur Zähler;
- explizite Anforderungs-/Antwort-Body-Finish-Aufrufe für Header-EOS, Body-EOS und
  Anhänger EOS;
- Downstream-Protokoll und Endpunkte, die den angeforderten Envoy-Attributen zugeordnet sind,
  niemals aus dem Envoy-to-Service-gRPC-Socket abgeleitet;
- passende `HeadersResponse`-/`BodyResponse`-Nachrichten für den `STREAMED`-Modus;
- EOS-Bereinigung, Bereinigung des gRPC-Kontextabbruchs und begrenzter, ordnungsgemäßer Stopp;
- Pre-Commit-Anfrage- und Antwortentscheidungen, die `ImmediateResponse` zugeordnet sind,
  wobei allgemeine Host-Aktionsmetadaten erst nach dem passenden gRPC-Versand aufgezeichnet werden
  gelingt;
- rohes Common-Decision-JSONL unter dem Runtime-Root pro Lauf plus einem separaten
  nutzlastfreies Abschlussprotokoll; Letzteres ist ergänzend und ersetzt niemals
  der gemeinsame Ereignisstrom;
- Unit- und CGo-Lebenszyklustests für P1/P2/P3/P4, inkrementelles EOS,
  Stornierung, Commit-Reihenfolge und parallele Transaktionen.

Die angeheftete Abhängigkeit ist das offiziell generierte Envoy Go API-Modul in
`go.mod`/`go.sum`. `../config/envoy-ext-proc-versions.env` zeichnet das beabsichtigte auf
Envoy-Version (`1.38.2`) und `../config/envoy-ext-proc-streaming.yaml.in` werden verwendet
nur `STREAMED` Körpermodi, niemals `BUFFERED`.

## Mindestversionen für die Abhängigkeitssicherheit

Das Modul hält für die aktuell triagierten Dependency-Advisories mindestens
folgende stabile Auswahlen ein:

- `google.golang.org/grpc` `v1.82.1` oder höher;
- `golang.org/x/net` `v0.56.0` oder höher;
- `golang.org/x/sys` `v0.46.0` oder höher; und
- `golang.org/x/text` `v0.39.0` oder höher.

`tests/test_ci_security_workflows.py` prüft diese Grenzen als semantische
Versionsuntergrenzen. Damit bleibt ein späteres stabiles Sicherheitsupdate
zulässig, während ein Downgrade den fokussierten CI-Sicherheitsvertrag verletzt.
Die Grenze belegt die ausgewählten Modulversionen; sie belegt weder die
Erreichbarkeit eines Advisories noch ersetzt sie Go-Modultests oder behauptet,
dass ein gehosteter Dependabot-, OSV- oder Scorecard-Alert bereits aktualisiert
wurde.

## Explizite Nichteinforderungen und verspätetes Handeln

Der ausgelieferte Build verwendet `-tags libmodsecurity`; Ein Go-Build, der nur aus der Quelle stammt, behält a
PassthroughEngine nur für Protobuf/Unit-Entwicklung und lehnt eine Laufzeit ab
config. Der normale Build erfordert lokale libmodsecurity-Header und -Bibliotheken
Pfade und verknüpft dann Common Runtime mit der ausführbaren Datei ext_proc.

Der Dienst verwendet die konservative Antwort-Commit-Grenze: nur eine erfolgreiche
Antwortheader `CONTINUE` send markiert eine Antwort als festgeschrieben. Für eine disruptive
Entscheidung später gefunden:

- `minimal` und `safe` zeichnen ein echtes Common-Host-Ergebnis auf. `log_only` und
  mit dem ursprünglich sichtbaren Antwortstatus fortfahren;
- `strict` zeichnet `strict_abort_not_attempted` auf und fährt fort.`strict` wird absichtlich nicht zu einem gRPC-Fehler, `ImmediateResponse`, oder
ein behaupteter Reset. Diese Mechanismen beweisen nicht unabhängig voneinander, dass sie deterministisch sind
Für den Kunden sichtbarer Abbruch in Envoy. Ein abgebrochener gRPC-Kontext und ein beobachteter gRPC
Peer-EOF werden jeweils als `grpc_context_canceled_unattributed` und aufgezeichnet
`grpc_peer_eof`; Keines der Labels kann ernsthaft als Downstream-Kunde behandelt werden
Reset oder ein Upstream-Reset.

## Lokale Quell-/Build-Befehle

```sh
make -C connectors/envoy build-envoy-ext-proc
make -C connectors/envoy test-envoy-ext-proc
make -C connectors/envoy check-envoy-ext-proc-config
make -C connectors/envoy prepare-envoy-ext-proc-config
make -C connectors/envoy runtime-smoke-envoy-ext-proc ENVOY_BIN=/absolute/path/to/envoy
```

`runtime-smoke-envoy-ext-proc` startet einen echten Pinn-kompatiblen Envoy-Prozess.
der CGo/Common gRPC-Dienst und ein lokaler Upstream. Es spart effektiven Gesandten und
Gemeinsame Konfigurationen, rohes Common JSONL und eine separate Nur-Metadaten-Konfiguration
Abschlussprotokoll außerhalb der Kasse. Die Wirtsrauchübungen P1, P2, P3 verweigern,
P3-Umleitung und P4-Post-Commit-Sicherheits-/Nur-Protokoll-Verhalten. Es bleibt
nicht hochgestuft, bis der kanonische Sammler und die Fähigkeitsüberprüfung dies akzeptieren
rohe Wirtsbeweise.

## Verbleibende Promotion-Grenze

Der Dienst beansprucht keinen deterministischen Post-Commit-Reset oder ein Client-Byte
Beobachtung. Eine verspätete P4-Regel wird bewusst als vom Gastgeber bestätigt erfasst
`log_only`; `strict` bleibt `strict_abort_not_attempted`. Diese Grenzen und
Die unabhängige Validierung des rohen Common JSONL durch den kanonischen Sammler sind
die verbleibende Promotion-Grenze.
