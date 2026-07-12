# Protokoll-Evidence für HTTP/2 und HTTP/3

**Sprache:** [English](protocol-evidence.md) | Deutsch

Dieser Vertrag gilt für einen echten Lauf
`Client → nativer Host → Connector`. Er macht weder ein Build-Flag, eine
ALPN-Konfiguration, einen Proxy vor dem Host noch einen internen Stream-Fehler
zu Protokoll-Evidence.

## Kanonische Werte

| Feld | Werte |
|---|---|
| `requested_protocol`, `downstream_protocol`, `upstream_protocol`, `negotiated_protocol` | `http1`, `h2`, `h2c`, `h3` |
| `transport` | `tcp`, `tls_tcp`, `quic_udp` |
| H2 über TLS | `alpn=h2`, `transport=tls_tcp` |
| H2C | `transport=tcp`, kein TLS-ALPN-Claim |
| H3 | `alpn=h3`, `transport=quic_udp`, `fallback_used=false`, `quic_connection_id_present=true`, begrenzte `quic_version` |

Downstream- und Upstream-Protokoll sind unabhängig. Ein Envoy-H3-Downstream
mit HTTP/1-Upstream wird beispielsweise als `h3` / `http1` erfasst; daraus
folgt keine H3-Unterstützung auf dem Upstream.

## Verwalteter Client

Verwende den Framework-eigenen Helper statt eines handgeschriebenen
curl-Kommandos:

```sh
cd modules/ModSecurity-test-Framework
python3 ci/checks/protocol/protocol_client.py \
  --url https://127.0.0.1:8443/no-crs/deny \
  --protocol h2 \
  --artifact-dir /absolute/evidence/client-h2 \
  --connector nginx \
  --integration-mode native-nginx-http-module \
  --run-id example-run \
  --transaction-id tx-1 \
  --transport-case-id nginx-h2-p1-001 \
  --rule-id 1100001 \
  --phase 1 \
  --stream-id 1 \
  --observation-sidecar /absolute/evidence/h2-sidecar.json
```

Der Helper erzwingt je nach Profil `--http2`,
`--http2-prior-knowledge` oder `--http3-only`. Für H3 verwendet er niemals
das fallback-fähige `--http3`. Fehlt dem ausgewählten curl das Feature
`HTTP3`, ist H3 bereits vor einem Netzwerkrequest `BLOCKED`; dies ist ein
Umgebungsblocker, kein `UNSUPPORTED`-Claim über einen Connector.

Jeder Aufruf schreibt atomar nur:

- `client-version.txt`
- `client-features.txt`
- `client-command.txt`
- `client-protocol-observation.json`

Response-Bodies gehen an das Null-Device. Das Command-Artefakt redigiert
Request-Header, Body- und CA-Pfade sowie Query-Strings. Die Observation lehnt
rohe QUIC-Connection-IDs ab und akzeptiert nur
`quic_connection_id_present`.

Für H2/H2C/H3 ist `--transport-case-id` Pflicht. Der Helper sendet ihn nur
als begrenzten Request-Header `X-MSConnector-Transport-Case`, redigiert diesen
Header in `client-command.txt` und behält den Token als Metadatum. Passendes
natives Connector-Event und kanonisches Case-Result müssen exakt denselben
Token tragen; ein kopiertes Bundle kann nicht einer anderen Transaction oder
einem anderen Stream zugeschrieben werden.
Vom Aufrufer gelieferte Header mit diesem Namen werden unabhängig von Groß- und
Kleinschreibung abgelehnt: Nur der Helper schreibt den kausalen
Korrelations-Header.
Ein verwaltetes Bundle steht für genau einen Request; unabhängig promotierbare
Modern-Protocol-Fälle verwenden daher getrennte kanonische Läufe, bis ein
Multiplexing-Client existiert.

Für H2/H3 kann curl allein nicht alle Stream-Fakten liefern. Die optionale
JSON-Sidecar hat daher nur einen kleinen Wortschatz: Stream-ID, ALPN,
`quic_udp_observed`, QUIC-CID-Präsenz/-Version, Connection-Reuse und
Stream-Reset-Fakten. Sie darf keine Request-/Response-Payloads, Header,
stderr, URLs oder rohe CIDs enthalten.

## Strikte Post-Commit-Resets

Ein H2-/H3-Strict-Ergebnis ist nur gültig, wenn alle folgenden Punkte zutreffen:

- kanonisches Connector-Event und Case-Result binden Connector,
  Integrationsmodus, Run-ID, Transaction-ID, Rule-ID, Phase,
  angeforderte/tatsächliche Aktion und Stream-ID;
- die Response war committed und mindestens ein Body-Byte beim Client sichtbar;
- die Response ist unvollständig; es wird kein erfundener später HTTP-403
  behauptet;
- `actual_action=stream_reset`, `stream_reset=true`, ein Reset-Code und
  `transport_result=stream_reset` sind erfasst;
- H3 belegt zusätzlich ausgehandeltes `h3`, `quic_udp`, `alpn=h3` und keinen
  Fallback; und
- ein unabhängiger Health-Request mit erzwungenem Profil gelingt.

Der aktuelle verwaltete curl-Helper dient bewusst nur der Negotiation: Er kann
keinen stream-lokalen Reset/Cancel oder multiplexte Peers selbst auslösen oder
unabhängig dekodieren. Daher kann er Strict-, Reset-/Cancel- und
Multiplexing-Fälle nicht promoten; sie bleiben `NOT EXECUTED`, bis ein
dedizierter Stream-Control-Client bereitsteht. Der Checker behält den
Strict-Vertrag als exaktes, nicht-promotierendes Acceptance-Gate für diesen
späteren Client.

Übergib `--followup-url` für den unabhängigen Health-Request. Dadurch entsteht
das zusätzliche payload-freie `client-followup-observation.json`, das die
Strict-Validierung benötigt. Der Helper leitet einen eigenen begrenzten
Follow-up-`transport_case_id` ab und persistiert ihn zusammen mit einem nicht
rückrechenbaren `target_authority_sha256`; die Strict-Validierung verlangt
diesen anderen Token und denselben Target-Authority-Hash, ohne rohe URL oder
Request-Payload zu behalten. Validiere anschließend die Client-Seite explizit:

```sh
python3 ci/checks/protocol/check_protocol_evidence.py \
  --artifact-dir /absolute/evidence/client-h3-strict \
  --protocol h3 \
  --strict \
  --connector nginx \
  --integration-mode native-nginx-http-module \
  --run-id example-run \
  --transaction-id tx-4 \
  --rule-id 1100301 \
  --phase 4
```

Der No-CRS-Finalizer lehnt unabhängig davon einen H2-/H3-`PASS` ohne passende
kanonische Event-Provenienz ab. Für einen kanonischen Full-Lifecycle-Lauf wird
das Client-Bundle mit `--protocol-client-artifact-dir` an
`no_crs_baseline.py finalize` übergeben; es wird vor dem Erhalt eines
Modern-Protocol-`PASS` unter `inventory/protocol-client/` mit
Manifest-Checksummen kopiert. Der Root-Full-Lifecycle-Runner reicht ein
explizites, reguläres und symlinkfreies
`NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR` nur weiter, wenn es im Raw-Run dieser
Invocation liegt. Alternativ reserviert `NO_CRS_PROTOCOL_CLIENT=1` selbst ein
Verzeichnis `raw-run/protocol-client`; fehlt das optionale Bundle, weil der
gewählte Host seinen Protokollpfad nicht starten kann, bleibt dies ausdrücklich
nicht promotierend. Beide Gates sind nötig; keines ersetzt das andere.

## NGINX-Profile

Die verwalteten NGINX-Profile sind `h1` (Default), `h1-h2` und
`h1-h2-h3-quic`. H2-/H3-Profile erhalten getrennte Build-Pfade und
Cache-Identitäten. Das H3-Profil verlangt gepinnte TLS-/QUIC-Source-Inputs und
prüft mit `nginx -V` die Flags `--with-http_ssl_module`,
`--with-http_v2_module` und `--with-http_v3_module`. Auch ein erfolgreicher
Build bleibt Build-Provenienz, bis ein erzwungener Client und passende Events
die obigen Gates bestehen.

Für lokale H2-/H3-Listener erzeugt der Harness eine ephemere Test-CA und ein
davon getrennt ausgestelltes Leaf-Zertifikat mit einem Tag Laufzeit für
`localhost`/`127.0.0.1`. Er erfasst TCP- und UDP-Listener getrennt, auch wenn
beide dieselbe Portnummer verwenden. 0-RTT wird nicht getestet;
`http3_0rtt` bleibt `NOT EXECUTED`.

Ein optionaler NGINX-H2-/H3-Aufruf führt den verwalteten erzwungenen Client
durch eine ModSecurity-aktive Allow-Route aus, während der Listener lebt, und
hält sein payload-freies Bundle im frischen Raw-Run:

```sh
NO_CRS_RUN_ID="protocol-nginx-$(date -u +%Y%m%dT%H%M%SZ)" \
NO_CRS_PROTOCOL_CLIENT=1 \
NGINX_PROTOCOL_PROFILE=h1-h2 \
NGINX_DOWNSTREAM_PROTOCOL=h2 \
make full-lifecycle-nginx
```

Der begrenzte Harness liefert seinen eigenen festen Probe-Token, damit der
verwaltete Client den erzwungenen Request ausführen kann; kein natives Event
und kein Catalog-Case übernimmt diesen Token. Er liefert bewusst weder eine
synthetische Stream-ID noch eine ALPN-Sidecar. Deshalb wird auch eine
erfolgreiche erzwungene Negotiation als `NOT_EXECUTED` erfasst, bis ein natives
Event und ein Protocol-Case die erforderliche Stream-/Case-Korrelation
herstellen; allein dadurch wird keine H2-/H3-Capability promotet.

## CI-Aufteilung

Der Workflow `protocol-contract` führt auf Pull Requests die Prüfungen für
Payload/Privacy/Client und den NGINX-Profilvertrag aus. Seine geplante/manuelle
Matrix baut die NGINX-Profile `h1-h2` und `h1-h2-h3-quic`, erzeugt je ein
erzwungenes Client-Preflight-Artefakt und lädt ausschließlich das
payload-freie Bundle hoch. Ein Preflight ohne Listener ist ausdrücklich keine
Connector-Runtime-Evidence; eine H3-Observation `BLOCKED` wird als
Client-Umgebungszustand berichtet.

Die aktuellen Connector-Grenzen und bewusst nicht erhobenen Claims stehen im
[Audit zur Transport-Härtung](../../reports/audits/transport-hardening-audit.de.md).
