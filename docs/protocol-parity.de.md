# Workstream zur HTTP/2- und HTTP/3-Protokollparität

**Sprache:** [English](protocol-parity.md) | Deutsch

Dies ist ein unabhängiger laufender Parent-Workstream. Er dokumentiert die
aktuelle Evidence für HTTP/2- und HTTP/3-Lifecycle-Parität über die sechs
ausgewählten Connectoren. Dies ist keine Abschlussbehauptung. HTTP/1.1 bleibt
die Regressions-Baseline.

## Evidence-Grenze

Das neutrale Common-Modell stellt die Protokollzustände `unknown`, H1, H2 und
H3, Stream-Identität, Commit- und EOS-Zustand sowie die Auswahl eines
Stream-Resets dar. H2-Stream-ID 0 und ein frei gesetztes `STREAM_RESET` werden
konservativ nicht als Stream-Reset ausgegeben. Dieses Modell beweist nicht,
dass jeder Adapter es verwendet.

Das Framework-Submodul ist nicht initialisiert und wurde nicht geändert. MRTS
wurde nicht angefasst. curl hat HTTP/2, aber kein HTTP/3. `curl --http3` beendet
sich mit `2`. Daher lautet der H3-Runtime-Status
`runtime_skipped_missing_client`; H3-Runtime ist nicht verifiziert.

## Connector-Statusmatrix

Die Statuswerte sind unabhängig. `not_run` bedeutet, dass für diese Dimension
keine Evidence geliefert wurde; `blocked` bezeichnet eine beobachtete
Voraussetzungsbeschränkung. `source-level fixed` und
`implemented_not_runtime_verified` beschreiben nur Source-Evidence und sind
keine Runtime-Pässe.

| Connector | H1 baseline | H2 code | H2 runtime | H3 code/capability | H3 runtime | P1 | P2 | P3 | P4 | Late intervention | Overall |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Apache | contract_verified (source only) | configured_not_exercised | not_run | not_implemented | runtime_skipped_missing_client / runtime_not_verified | not_run | not_run | contract_verified (source only; protocol from `ap_get_protocol(r->connection)` plus canonical HTTP/1 `r->proto_num`; unknown fails closed) | not_run | not_run | source-level fixed / runtime not verified |
| NGINX | contract_verified (source only) | implemented_not_asserted | not_run | implemented_not_asserted | runtime_skipped_missing_client / runtime_not_verified | not_run | not_run | not_run | not_run | not_run | source-level fixed / runtime not verified |
| HAProxy | not_run | not_implemented | not_run | not_implemented | runtime_skipped_missing_client / runtime_not_verified | not_run | not_run | not_run | not_run | not_run | not_implemented |
| Envoy | not_run | configured_not_exercised | not_run | not_implemented | runtime_skipped_missing_client / runtime_not_verified | not_run | not_run | not_run | not_run | not_run | source-level configured / runtime not verified |
| Traefik | contract_verified (source only) | not_implemented | not_run | not_implemented | runtime_skipped_missing_client / runtime_not_verified | not_run | not_run | not_run | not_run | contract_verified (source only) | source-level fixed / runtime not verified |
| lighttpd | not_run | unsupported_by_host_model | not_run | not_implemented | runtime_skipped_missing_client / runtime_not_verified | not_run | not_run | not_run | not_run | not_run | not_implemented |

Die Apache-P3-Änderung leitet das Protokoll jetzt aus
`ap_get_protocol(r->connection)` plus kanonischem HTTP/1-`r->proto_num` ab und
schlägt bei unbekanntem Protokoll fail closed fehl. NGINX erzeugt für H2-Streams
kein `Transfer-Encoding` mehr und besitzt einen geschützten H3-Pfad. Traefik
markiert einen initialen nicht-EOF-`ReadFrom`-Source-Fehler (mit oder ohne Bytes) als
unvollständig und verhindert, dass ein Response-Body-Engine-Fehler nach Commit
ein synthetisches EOS auslöst. Die ursprüngliche direkte Post-Commit-
Engine-Error-Reproduktion und die neue Initial-ReadFrom-Source-Error-
Reproduktion schlugen vor der Reparatur fehl; die fokussierte Post-Patch-Go-
Auswahl bestand. Es wird keine H2/H3-Traffic-Behauptung aufgestellt und die
tatsächliche Traefik-H2/H3-Runtime wurde nicht ausgeführt. Sein
`responseIncomplete`-Zustand unterdrückt falsches EOS und normales FINISH bei
Host-, Engine-, Commit- und Source-Fehlern. `finish()` markiert einen nach
Commit fehlgeschlagenen EOS-Callback als `responseIncomplete`; fehlgeschriebene
oder nicht bestätigte Pre-Commit-Deny-/Fehlerantworten werden ebenfalls als
unvollständig markiert. Ein initiales `(0,nil)` ReaderFrom delegiert nicht vor
Pre-Commit-Kontrollen. Es wird kein falsches EOS- oder normales FINISH-Verhalten
behauptet. Ein Pre-Commit-EOS-Enginefehler markiert den Abschluss trotz eines
sichtbaren Fallbacks als unvollständig. Fehlende Applied- oder Late-Log-Only-
Acknowledgements markieren den Abschluss ebenfalls als unvollständig, sodass
kein normales FINISH behauptet wird. Bei Late-Log-Only-Ack-Fehlern erzeugt auch
der delegierte ReaderFrom-EOF-Pfad kein synthetisches EOS.

Envoy besitzt jetzt getrennt materialisierte Downstream-Profile `http1` und
`h2`: `http1` wählt ausschließlich ALPN `http/1.1` und den HTTP/1-HCM-Codec,
während `h2` ALPN `h2`, den HTTP/2-HCM-Codec und
`http2_protocol_options` wählt. Der Materializer weist jeden anderen Wert
zurück, statt zurückzufallen. Sein vorhandener Python-Runtime-Helper bleibt
ausdrücklich HTTP/1.1-only. Fokussierte Go-Contract-Tests für den
`ext_proc`-Request-Header-Adapterpfad bewahren einen von Envoy gelieferten
Metadatenwert `HTTP/2` und weisen doppelte, großgeschriebene oder nicht
unterstützte Request-Pseudo-Header, CR/LF/NUL-Headerwerte,
Connection-spezifische Header für moderne Protokolle und ungültige `TE`-Werte
zurück, wenn das gelieferte Protokoll HTTP/2 oder HTTP/3 ist. Dies sind ausschließlich Source-/Konfigurations- und
Adaptergrenzprüfungen: Es wurde weder ein Envoy-Binary-/Config-Load noch
Client-ausgehandelter H2-Traffic ausgeführt.

Die Matrix bewahrt die getrennten Angaben aus
`connectors/*/capabilities.json`: Apache H2 ist
`configured_not_exercised` und sein H3-Host-Pfad ist `not_implemented`; NGINX
H2 und H3 sind `implemented_not_asserted`; HAProxy und Traefik sind für die
ausgewählten nativen Modern-Protocol-Profile `not_implemented`; Envoy
Downstream-H2 und TLS/ALPN sind `configured_not_exercised`; lighttpd H2 ist
`unsupported_by_host_model` und H3 ist `not_implemented`.

Kein Security-Finding ist vollständig verifiziert. Die zutreffende
Klassifizierung für die obigen Änderungen ist source-level fixed / runtime not
verified.

## Neutrales Lifecycle-Contract

Der Common-Contract hält Protokoll- und Lifecycle-Entscheidungen von
Connector-spezifischen Host-Typen getrennt. Er umfasst:

- die Protokollauswahl `unknown`, H1, H2 und H3;
- Stream-Identität und Transaktionskorrelation;
- Commit-Zustand und terminale EOS-Behandlung;
- Stream-Reset-Auswahl für ein Multiplexing-Protokoll; sowie
- Safe- und Strict-Entscheidungen für späte Interventionen.

Adapter müssen weiterhin nachweisen, dass sie dieses Modell abbilden und
durchsetzen. Die Matrix erhebt daher Common-Modell-Abdeckung nicht zu
Connector-Runtime-Abdeckung.

## Regressions- und Capability-Evidence

- 28 ausgewählte Python-Tests bestanden (Apache/NGINX/C/C++-Gruppe).
- Der aktuelle kombinierte Python-Befehl bestand mit 98 Tests und 1 erwarteten
  Framework-Identity-Skip.
- Frühere Baselines waren 20 passed/3 skipped und 39 passed/2 skipped.
- Capability-Gruppe 93 hatte einen erwarteten Environment-Fehler, weil der
  Framework-Validator fehlte, während das Framework-Submodul nicht initialisiert
  war.
- Common C17 bestand.
- Common C17 helper bestand.
- Common SDK/adapter/security checks bestanden.
- Apache C17 bestand.
- Apache statischer Test bestand.
- Traefik-Pakettest bestand.
- Vier fokussierte Go-Regressionen schlugen absichtlich vor dem Fix fehl und
  bestanden danach.
- Drei test-first Go-Regressionen schlugen absichtlich vor dem Fix fehl und
  bestanden danach.
- Ein neuer test-first ReaderFrom-Regressionsfall schlug vor dem Guard fehl und
  besteht danach.
- Für die Matrix wurde kein H2-Runtime-Traffic geliefert.
- H3-Runtime ist `runtime_skipped_missing_client` und nicht verifiziert.

Während des Workstreams wurde eine versehentliche anfängliche Ausgabe in einem
gemeinsamen Build-Verzeichnis beobachtet. Dies ist nur eine lokale
Storage-Beschränkung; es ist keine Protokoll- oder Runtime-Evidence und stützt
keine weitergehende Behauptung.

## Delivery-Status

Commit `5e7b34d1887984f74d061872d7652a3f71d87856` ist als
`feature/http2-http3-protocol-parity` gepusht und durch Draft-PR
[#348](https://github.com/Easton97-Jens/ModSecurity-conector/pull/348)
vertreten. Bei der initialen Delivery-Verifikation stimmten lokaler, Remote- und
PR-Head-SHA überein. CI-Prüfungen waren in Warteschlange oder in Ausführung und
werden nicht als bestanden behauptet. Kein Merge hat stattgefunden. Das
Framework-Submodul und MRTS bleiben unverändert.
