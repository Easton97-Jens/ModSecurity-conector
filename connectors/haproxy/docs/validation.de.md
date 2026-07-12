# HAProxy-Validierung

**Sprache:** [English](validation.md) | Deutsch

Status: teilweise; Das historische SPOA-Laufzeitmaterial ist evidenzbasiert und dies auch
kanonische Phase-4-Facetten nicht fördern.

`make smoke-haproxy` überprüft Framework-YAML-Fälle, indem es jeden Fall materialisiert.
Starten von HAProxy, Starten von `haproxy-modsecurity-spoa`, Starten eines Backends,
Senden der Fallanfrage über HAProxy und Geltendmachung des beobachteten Status.

`make runtime-matrix-haproxy` zeichnet Zeilen aus Live-Zusammenfassungsbeweisen auf. PASS und
FAIL werden nur für die Live-HAProxy-Ausführung verwendet. Die erzeugten Artefakte können sich unterscheiden
Umgebung und Fallbestand, es kann jedoch kein HAProxy PASS/FAIL erstellt werden
synthetische Matrixreihen.

## Befehle

```bash
git submodule update --init --recursive
make -C connectors/haproxy build-modsecurity-binding
make -C connectors/haproxy build-spoa-runtime
HAPROXY_HTX_SOURCE_DIR=/absolute/path/to/haproxy-3.2.21 \
  MODSECURITY_INCLUDE_DIR=/absolute/path/to/include \
  MODSECURITY_LIB_DIR=/absolute/path/to/lib \
  BUILD_ROOT=/srv/modsecurity-work/haproxy-htx-smoke \
  make -C connectors/haproxy runtime-smoke-haproxy-htx
make smoke-haproxy
make runtime-matrix-haproxy
FORCE_ALL_CASES=1 make runtime-matrix-haproxy
make generate-test-matrix
make check-test-matrix
```

## Historische Beweise

Bei diesen Schnappschüssen handelt es sich nicht um aktuelle kanonische Facettenbeweise der Phase 4.

| Beweissatz | Versucht | PASS | FEHLER | GESPERRT | NOT_EXECUTABLE |
| --- | ---: | ---: | ---: | ---: | ---: |
| Standard-HAProxy-Smoke-Test (historisch) | 55 | 55 | 0 | 0 | 0 |
| HAProxy force-all (historical) | 133 | 104 | 23 | 0 | 6 |

Beweise werden aufgezeichnet in:

- `/src/ModSecurity-conector-build/results/with-crs/haproxy-summary.json`
- `/src/ModSecurity-conector-build/results/force-all/haproxy-summary.json`
- `reports/testing/generated/haproxy-runtime-results.generated.md`
- `reports/testing/haproxy-poc.md`
- `reports/testing/runtime-validation-snapshot.json`

## Nicht beansprucht

- Force-all-FAIL-Zeilen werden standardmäßig nicht ausgeblendet.
- Die Ganzkörper-RESPONSE_BODY-Unterstützung wird nicht gefördert.
- Ein Build-Selbsttest allein ist keine Laufzeitüberprüfung.
- Es gibt keinen Schreiber für synthetische Matrizen.

Phase 4 / RESPONSE_BODY bleibt nicht hochgestuft. Der alte begrenzte Beispielzweig
ist deaktiviert, da `http-response wait-for-body` erforderlich ist; es ist kein
echter hostseitiger Antwortstrom oder strikter Abbruchnachweis.

## Kanonische Phase-4-Validierung

Die ausgewählte SPOA/SPOP-Konfiguration hat keinen Antworttextpfad: ersteren
Der begrenzte Zweig ist deaktiviert. Das separate `full-lifecycle-haproxy-htx`-Profil
wählt einen HAProxy 3.2.21 HTX-Pfad mit P1–P4-Verkehr des echten Hosts aus. Es beweist
Für den Client sichtbare Precommit-Antworten für kanonische P1-Regeln `1100001` (403) und
`1100002` (429) und für die kanonische P3-Regel `1100201` (403) vor dem Upstream
Header-Antwort wird weitergeleitet. Es handelt sich nicht um einen SPOP-Antwortpfad. Der Einblocker
Die P2-Probe gibt einen Client 403 über die Reply-and-Close-API und Datensätze von HAProxy zurück
null oder eine beobachtete Upstream-Anfrage ohne Nachweis ihrer Bestellung; das tut es
keine inkrementelle Weiterleitung oder eine allgemeine Pufferungsgarantie. P4 Safe leitet die weiter
ursprüngliche Antwort mit
`host_action=log_only`; P4 Strict bleibt `host_action=not_attempted`.
`response_body_buffered`, `phase4` und `phase4_rule_evaluation` bleiben bestehen
`not_implemented` für das ausgewählte SPOP-Fähigkeitsprofil; kein Post-Commit
Abbruch, First-Byte-Timing oder Client-No-Full-Buffer-Proof liegt vor. Der Läufer bleibt bewusst zurück
`capability_promotion=not_permitted`, also diese echten lokalen Host-Ergebnisse
werden nicht zu Selected-Path-Fähigkeitszusicherungen.

| Fall | Erforderliche Nachweise | Ausgeschlossener Ersatz |
| --- | --- | --- |
| `phase4_rule_observed` | Regel `1100301` wird über den realen Antwortpfad beobachtet | ein Selbsttest oder ein Nur-Agent-Protokoll |
| `phase4_deny_before_commit` | `NOT_EXECUTED`: Implementieren Sie zuerst den vom Host beobachteten Clientstatus und das Commitment-Timing | Von der Richtlinie abgeleitete Agentenfelder |
| `phase4_deny_after_commit_log_only` | `NOT_EXECUTED`: Ein Quell-/Harness-`log_only`-Datensatz ist kein vom Client validiertes kanonisches Ergebnis | ein bloßer Antwortstatus oder ein antworterhaltender Richtlinienwert |
| `phase4_deny_after_commit_abort` | `NOT_EXECUTED`: Implementieren Sie zuerst das kontrollierte Post-Commit `abort_connection` | Zeitüberschreitung, Agentenfehler oder generische Verbindungstrennung |
| Status-/Aktionsmetadaten | `NOT_EXECUTED`: Implementieren Sie zuerst den vom Host beobachteten ursprünglichen/sichtbaren Status und das Timing | ein Statusfeld, eine Regel-ID oder von der Richtlinie abgeleitete Werte |

Kein kanonischer Lauf bedeutet `NOT_EXECUTED`, kein synthetischer 403 `PASS`.  Veranstaltung und
Berichtsartefakte sind reine Metadaten und dürfen niemals Antworttextdaten enthalten.
