# HAProxy Connector PoC

**Sprache:** [English](haproxy-poc.md) | Deutsch

Status: Produktions-SPOA-Laufzeitnachweis nur für Request-Phasen und
Response-Header; Phase 4 / RESPONSE_BODY ist kein kanonischer Nachweis

## Umgesetzt

- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` erstellt die
  `haproxy-modsecurity-spoa` Produktion SPOA/SPOP Laufzeit.
- `connectors/haproxy/src/haproxy_modsecurity_binding.c` integriert die SPOA
  Laufzeit mit libmodsecurity.
- `connectors/haproxy/harness/run_haproxy_smoke.sh` startet HAProxy, die SPOA
  Laufzeit und einem lokalen Backend, zeichnet dann Live-Laufzeitentscheidungen auf.
- `modules/ModSecurity-test-Framework/ci/runtime/run-haproxy-runtime-matrix.sh` läuft
  die Pfade ohne CRS, mit CRS und alle Nachweise erzwingen.
- Der Laufzeitnachweis umfasst `decision.jsonl`, HAProxy-Protokolle, SPOA-Protokolle und Audit
  Protokolliert bei Konfiguration JSONL Fallergebnisse und generierte Zusammenfassungen.

Wenn der Smoke-Test durchgeht, handelt es sich um eine Connectorvalidierung im Produktionsstil:

```text
HTTP client -> HAProxy -> SPOE/SPOP -> haproxy-modsecurity-spoa -> libmodsecurity -> HAProxy response
```

Es gibt keinen Writer für synthetische Matrizen. Generierte Berichte verbSmoke-Testen Live-Laufzeit
Artefakte und der Laufzeitvalidierungs-Snapshot.

## Build-Flow

Der lokale Build hält generierte Artefakte außerhalb des Checkouts:

```bash
BUILD_ROOT=/src/ModSecurity-conector-build
SOURCE_ROOT=/src
make -C connectors/haproxy build-modsecurity-binding
make -C connectors/haproxy build-spoa-runtime
make -C connectors/haproxy self-test-modsecurity-binding
make -C connectors/haproxy self-test-spoa-runtime
```

Die Produktion der SPOA-Binärdatei erfolgt unter:

```text
/src/ModSecurity-conector-build/haproxy-spoa-runtime/haproxy-modsecurity-spoa
```

Der HAProxy-Laufzeithelfer lädt HAProxy herunter, überprüft, erstellt und stellt ihn bereit
unter `BUILD_ROOT` unter Verwendung von Quellpins von
`modules/ModSecurity-test-Framework/ci/lib/common.sh`.

## Runtime-Smoke

Führen Sie den Standardbeweis aus:

```bash
make smoke-haproxy
make runtime-matrix-haproxy
make generate-test-matrix
make check-test-matrix
```

Aktuell generierter Standardstatus:

| Connector | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE |
| --- | ---: | ---: | ---: | ---: | ---: |
| HAProxy | 55 | 55 | 0 | 0 | 0 |

Der Standard-HAProxy-Nachweis ist die unterstützte Nicht-Former-XFAIL-Teilmenge von Live
Nachweise für die HAProxy-Matrix. Ehemalige XFAIL- und breitere Zeilen bleiben getrennte Laufzeiten
Nachweise.

## Force-All-Nachweis

Führen Sie alle Nachweise erzwingen aus:

```bash
FORCE_ALL_CASES=1 make runtime-matrix-haproxy
make generate-test-matrix
make check-test-matrix
```

Aktuell generierter Force-All-Status:

| Connector | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE |
| --- | ---: | ---: | ---: | ---: | ---: |
| HAProxy | 133 | 104 | 23 | 0 | 6 |

Alle erzwungenen FAIL- und NOT_EXECUTABLE-Zeilen bleiben erhalten
`reports/testing/generated/runtime/haproxy-runtime-results.generated.md`. Wurzel
Zusammenfassungen bleiben konnektorneutral.

## Entscheidungs- und Prüfprotokolle

Die Laufzeit schreibt pro Fall und aggregierte Nachweise:

- `decision.jsonl`: SPOA Entscheidungen, Aktion, Status, Regel-ID, Phase und
  Verarbeitungsflags.
- `audit.log`: libmodsecurity-Audit-Ausgabe, wenn die Audit-Protokollierung konfiguriert ist.
- `haproxy.stderr.log`: HAProxy-Laufzeitdiagnose.
- `spoa-agent.log`: SPOA Laufzeitdiagnose.
- `haproxy-results.jsonl`: normalisierte Fallbeweise.
- `haproxy-summary.json`: normalisierte Zählungen und Artefaktreferenzen.

Beispielpfade im Produktionsstil:

```text
/var/log/haproxy-modsecurity/decision.jsonl
/var/log/haproxy-modsecurity/audit.log
/var/log/haproxy-modsecurity/agent.log
```

## Anfragephasen

Die Gruppe `request-check` SPOE sendet:

- Anfrage-ID
- Client- und Serveradressen
- Methode, Pfad, URI und Host
- Anforderungsheader
- Anforderungskörperbytes und Länge

Die SPOA-Laufzeit ordnet diese Felder der libmodsecurity-Anforderungsverarbeitung zu und
gibt HAProxy-Variablen wie `blocked`, `action`, `status` zurück.
`redirect_url`, `rule_id`, `phase` und `error`.

## Antwortheader der Phase 3

Die Gruppe `response-check` SPOE sendet Antwortstatus und Antwortheader.
einschließlich Inhaltstyp, Standort, gesetztem Cookie, Server und zuletzt geänderten Werten.
Die SPOA-Laufzeit verarbeitet Antwortheader über libmodsecurity und gibt zurück
HAProxy-Variablen für die reaktionsseitige Durchsetzung.

## Phase 4 / RESPONSE_BODY

Phase 4 / RESPONSE_BODY ist im gewählten SPOE/SPOP-Pfad `not_implemented`.
Das frühere `wait-for-body`-Sample mit seinen `response_body`-Argumenten ist
deaktiviert: Der Harness setzt `HAPROXY_ENABLE_RESPONSE_BODY=0` und emittiert
keines von beiden. Das ausgemusterte Sample ist historisch/nicht kanonisch und
darf nicht als aktueller Laufzeitnachweis berichtet werden. Der getrennte
HAProxy-3.2.21-HTX-Full-Lifecycle-Pfad ist nicht promotet; sein einblockiger
P2-Probe protokolliert null oder eine beobachtete Upstream-Anfrage ohne deren
Reihenfolge zu belegen und belegt kein inkrementelles Forwarding.

## Produktionskonfigurationsform

Der beispielhafte Produktionspfad ist:

- HAProxy-Konfiguration: `/etc/haproxy/haproxy.cfg`
- SPOE Konfiguration: `/etc/haproxy/spoe-modsecurity.conf`
- SPOA Konfiguration: `/etc/haproxy/modsecurity-agent.conf`
- SPOA binär: `/usr/local/sbin/haproxy-modsecurity-spoa`
- ModSecurity-Regeln: `/etc/modsecurity/haproxy-rules.conf`

Das Ändern der HAProxy- oder SPOE-Konfiguration erfordert ein Neuladen von HAProxy. Wechselagent
config, die Binär-, libmodsecurity- oder Regeldateien SPOA erfordern einen Neustart der
SPOA Dienst.

## Statusbedeutungen

- `PASS`: Live-HAProxy und SPOA-Laufzeit erzeugten das erwartete Fallergebnis.
- `FAIL`: Live-Laufzeit ausgeführt, aber beobachtetes Verhalten weicht von der ab
  Erwartung.
- `BLOCKED`: relevant, aber durch Umgebungs- oder Laufzeitvoraussetzungen blockiert.
- `NOT_EXECUTABLE`: außerhalb des aktuellen HAProxy-Laufzeitbereichs.
- `former_xfail`: Umfassendere Nachweise, die außerhalb der standardmäßigen Smoke-Teilmenge verfolgt werden.

## Verfolgte offene Arbeit

- Umfassendere Force-All-FAIL-Untersuchung.
- Förderkriterien für volle RESPONSE_BODY-Unterstützung.
- Beispiele für Produktionsverpackungen und Servicemanager.
- Umfangreichere Bereitstellungsdokumentation nach zusätzlichen Laufzeitumgebungen
  bewiesen.

## Verwandte Berichte

- `reports/testing/generated/runtime/haproxy-runtime-results.generated.md`
- `reports/testing/test-coverage-overview.md`
- `modules/ModSecurity-test-Framework/TEST-COVERAGE-SUMMARY.md`
- `docs/build/compilers/haproxy.md`
