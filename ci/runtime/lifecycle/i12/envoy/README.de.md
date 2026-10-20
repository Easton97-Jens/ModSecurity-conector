# Envoy-I12-Hostevidenz

**Sprache:** [English](README.md) | Deutsch

Diese reine Envoy-Testerweiterung nutzt die vorhandene Capture-Variante `envoy`
und den gemeinsamen nativen Observer. Der [Taskbericht](../../../../../reports/testing/i12-envoy-host-evidence-20261015.de.md)
ist **PARTIAL**: 284 Original-IDs bleiben erhalten. Acht neu freigegebene
Nachweispakete erhöhen den aktuellen Lifecycle-PASS-Bestand auf elf;
114 ursprüngliche Oracles bleiben offen. Die zentrale Baseline bleibt
unverändert. Synthetische Hostproben qualifizieren Original-IDs nicht automatisch.

Alle 125 Original-Oracles haben einzelne Quellreviews. Die 33 neuen
Fixture-gebundenen Quellvorschläge bleiben von kanonischer Auflösung und
Hostabnahme getrennt.

## Aktueller Abnahmestand

| Route | Lifecycle-PASS / Original-IDs | Offene Original-Oracles |
| --- | ---: | ---: |
| `envoy-ext-proc` | 5 / 117 | 46 |
| `envoy-ext-authz-request` | 4 / 94 | 36 |
| `envoy-ext-authz-response-companion` | 2 / 73 | 32 |

Von 273 IDs ohne vollständige Lifecycle-Abnahme sind 8 reine
Konfigurations-PASS und 265 unqualifiziert. Die 86 echten Hostmessungen umfassen
37 Retakes unter 33 exakten Original-IDs. Die acht neuen Einzelfreigaben sind:

- `I12::envoy-ext-proc::NEED-request-streaming`
- `I12::envoy-ext-proc::NEED-response-streaming`
- `I12::envoy-ext-proc::NEED-client-response-bytes`
- `I12::envoy-ext-proc::NEED-client-exit-signal`
- `I12::envoy-ext-authz-request::NEED-complete-sample`
- `I12::envoy-ext-authz-request::NEED-request-multiple-chunks`
- `I12::envoy-ext-authz-request::NEED-client-response-bytes`
- `I12::envoy-ext-authz-response-companion::NEED-allow`

Die zwei zusätzlichen Request-Autorisierungsfreigaben binden Host- und Clientvertrag unabhängig. Der physische Envoy-Trace identifiziert Worker 285 / CID1 / SID6459190741822168578 und Hostfragmente 64+31=95 mit anschließendem EOS, danach den Authorization Check in Zeile 275. Die Engine erhält ein vollständiges natives 95-Byte-Sample und ein EOS; mehrere Client-Schreibvorgänge bedeuten keine mehreren nativen Callbacks. Die Responsebyte-Freigabe prüft rohes HTTP-Framing und Client-Entitybytes unabhängig. Der Process-Remote-gRPC-Status bleibt unbekannt und wird nicht als Erfolg gezählt.

## Producer

| Producer | Evidenzgrenze |
| --- | --- |
| `reconcile.py` | Prüft ursprüngliche Oracle-Quellen und physisches Ledger erneut; erhält alle 284 exakten Envoy-IDs |
| `prepare_native.py` | Git-freie aktuelle Quellkopie, unveränderte Capture-Overlays, native/CGo-Build, Go/Race/Vet und Observer-Kontrollen |
| `source_inventory.py` | Rekonstruiert sämtliche Buildeingaben aus dem hashgebundenen Gitarchiv und den expliziten Capture-Ergänzungen |
| `evidence_io.py` | Begrenzt physische Lesezugriffe auf erlaubte, besitzgeprüfte Pfade; sperrt Symlinks, private Konfiguration und Änderungen beim Lesen |
| `validate_oracles.py` | Prüft alle 125 Original-ID-Reviews und physischen Referenzen; erhält kanonische Ergebnisse |
| `host_scenarios.py` | Versiegelte unabhängige Fixtures, TLS-Eingaben, Binary-/Quellbindung und privater Controller; startet keine Hosts |
| `fault_scenarios.py` | Versiegelte Response-EOS-Fehlerfixture mit separatem Testproxy; realer Lauf `fault-host-v1` bleibt Runner77/Controller1/Client1, unqualifiziert und ohne neuen PASS |
| `bind_originals.py` | Versiegelt neue Retakes geprüfter Fixtures unter exakten Original-IDs mit sämtlichen Eingaben innerhalb des aktuellen privaten Laufs |
| `run_host.py` | Begrenzte Starts mit dem bestehenden nonroot Controller; Exitcodes bleiben Beobachtungen |
| `review_runs.py` | Physische Hashes, geladene Images, Client-/Backendbytes, native/Hostcallbacks, Cleanup und Transportfakten |
| `transport.py` | Unterscheidet tatsächlichen lokalen HTTP/2-Reset von explizitem Remote-gRPC-Erfolg |
| `qualify_originals.py` | Bereitet ausgewählte Originalfälle vor; Einzelfreigabe verlangt exakte Fixturegleichheit, frische Reproduktion aller 35 Nachweisfelder und den gemeinsamen Validator |
| `write_report.py` | Erzeugt nur den eigenen EN/DE-Taskbericht und das exakte ID-JSON; ändert keine gemeinsamen Generatoren oder Ledger |

Ein neuer Companion-NEED-allow-Retake bindet vor Ausführung ein separates ergänzendes Quellreview. Seine frühe Backend-Request-Line-Erfassung belegt genau einen Ziel- und einen Nachbarrequest; alte Receipts mit unterer Zählgrenze bleiben unverändert.

## Validierung

Im Parent-Worktree mit dem Repository-eigenen Python-Interpreter ausführen:

```sh
rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest discover -s ci/runtime/lifecycle/i12/envoy -p 'test_*.py' -v
rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -B ci/runtime/lifecycle/i12/capture_sources.py verify
```

Die vollständige aktuelle Envoy-Suite hat 188 PASS und 0 Skips. Beleg: `ci/final-envoy-controls-188-base-a622-v2.json`. Die fokussierten Fehlerproben-Kontrollen haben 16 PASS, die separaten Go-Testproxy-Kontrollen 10 PASS. Diese Kontrollen qualifizieren den Hostlauf nicht automatisch.

Jeder Producer bietet `--help`. Native Vorbereitung benötigt eine neue
registrierte externe Laufwurzel, den aktuellen Checkout, den vorhandenen
Offline-Modulcache, das ausgewählte echte SDK und die gepatchte Go-Toolchain.
`--validate-existing` erhält fehlgeschlagene Setup-Evidenz und wiederholt
Prüfungen, ohne Binaries still neu zu bauen. Für UDS-Tests einen kurzen privaten
physischen Temporärpfad verwenden.

Hostvorbereitung benötigt außerdem die ausdrücklich hashgebundenen erhaltenen
v5-Controller-/Template-Eingaben und die passende native Build-Receipt. Diese
sind externe Voraussetzungen, keine mitgelieferten Binaries und keine Erlaubnis
zur Toolinstallation. Der Controller entfernt Capabilities, wechselt in private
Namespaces und lässt UID/GID 65534 mit NoNewPrivs zu, bevor Capture-Programme
laufen. Die Envoy-Kopie hält ihren positiv identifizierten PID-Namespace bis
nach Cleanup offen, damit Inode-Wiederverwendung keine fremden Prozesse
fehlzuordnet. Alle ursprünglichen Prüfungen bleiben aktiv; fehlgeschlagene
Ownership-Prüfungen bleiben Fehler.


Die Quellrevision der nativen und Hostevidenz bleibt ausschließlich
`f27eb59b53beff6f65384fc2e5037881a3052c01`. Der exakte Base-Head
`a62296fb57263f9be18c6ac879e36e0ab2a9935c` wurde in
`dfb1a07a863530a53c0006ee204319453d66a2ad` in diesen
Branch gemergt. Die erhaltene Baseline und die physischen Quellen wurden mit den
aktuellen zentralen Validatoren erneut geprüft; dieser Envoy-Task änderte
keinen gemeinsamen Validator. Die erhaltenen Laufzeitreceipts qualifizieren
den gemergten Base-Produktstand nicht; eine frische Capture der aktuellen
Base bleibt erforderlich. Begrenzte Dokumentationsevidenz:
`ci/docs-postmerge-a622-v2.json`.

Die echte ext_proc-Fehlerprobe `fault-host-v1` verwirft ausschließlich den leeren Response-EOS-Callback und führt einen tatsächlichen Half-Close aus. Engine-API und dem Zielstream eindeutig zugeordneter Envoy-Trace melden gRPC-Status14. Der Client empfängt einen HTTP200-Präfix mit 96 Bodybytes in 64+32, jedoch keinen Nullchunk. Runner77/Controller1/Client1 bleiben unqualifiziert; neue PASS: 0. Am Ziel sind P1–P3 und P4=0, ein `runtime_finish`-Versuch mit Result0 sowie Logging/Free/Cleanup jeweils1 beobachtet. Der gesunde Nachbar hat P1–P4/Finish jeweils1; Survivors und Mountleaks fehlen. Der Proxy-Wirestatus bleibt unbeobachtet. Fehlender Status wird nicht als erfolgreicher Abschluss interpretiert.

## Aussagegrenzen

`max_request_bytes` ist Envoys Hostbuffer-Grenze. Authorization-Samples, native
Limits und technische gRPC-Fehler benötigen getrennte Beobachtungen. Begonnene
oder abgebrochene Backendrequests werden unabhängig von abgeschlossenen Receipts
gezählt. Mehrere Client-Schreibvorgänge allein belegen keine mehreren nativen
Bodycallbacks. Vollständiges HTTP-Framing, TCP-Reset, gRPC-Status, EOS, Finish
und Free sind getrennte Fakten. Fehlender Remote-gRPC-Status ist niemals
erfolgreicher Abschluss.

Verbleibende Lücken stehen im Taskbericht und im exakten ID-JSON. Über diese
Erweiterung keine gemeinsamen Manifeste, Originalkataloge, anderen Connectoren
oder Produktquellen ändern. Rohartefakte extern erhalten; nur geprüfte Metadaten
versionieren.
