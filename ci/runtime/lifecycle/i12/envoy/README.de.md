# Envoy-I12-Hostevidenz

**Sprache:** [English](README.md) | Deutsch

Diese reine Envoy-Testerweiterung nutzt die vorhandene Capture-Variante `envoy`
und den gemeinsamen nativen Observer. Der [Taskbericht](../../../../../reports/testing/i12-envoy-host-evidence-20261015.de.md)
ist **PARTIAL**: 284 Original-IDs bleiben erhalten. Drei neu freigegebene
Nachweispakete erhöhen den aktuellen Lifecycle-PASS-Bestand auf sechs;
119 ursprüngliche Oracles bleiben offen. Die zentrale Baseline bleibt
unverändert. Synthetische Hostproben qualifizieren Original-IDs nicht automatisch.

Alle 125 Original-Oracles haben einzelne Quellreviews. Die 33 neuen
Fixture-gebundenen Quellvorschläge bleiben von kanonischer Auflösung und
Hostabnahme getrennt.

## Producer

| Producer | Evidenzgrenze |
| --- | --- |
| `reconcile.py` | Prüft ursprüngliche Oracle-Quellen und physisches Ledger erneut; erhält alle 284 exakten Envoy-IDs |
| `prepare_native.py` | Git-freie aktuelle Quellkopie, unveränderte Capture-Overlays, native/CGo-Build, Go/Race/Vet und Observer-Kontrollen |
| `source_inventory.py` | Rekonstruiert sämtliche Buildeingaben aus dem hashgebundenen Gitarchiv und den expliziten Capture-Ergänzungen |
| `evidence_io.py` | Begrenzt physische Lesezugriffe auf erlaubte, besitzgeprüfte Pfade; sperrt Symlinks, private Konfiguration und Änderungen beim Lesen |
| `validate_oracles.py` | Prüft alle 125 Original-ID-Reviews und physischen Referenzen; erhält kanonische Ergebnisse |
| `host_scenarios.py` | Versiegelte unabhängige Fixtures, TLS-Eingaben, Binary-/Quellbindung und privater Controller; startet keine Hosts |
| `bind_originals.py` | Versiegelt neue Retakes geprüfter Fixtures unter exakten Original-IDs mit sämtlichen Eingaben innerhalb des aktuellen privaten Laufs |
| `run_host.py` | Begrenzte Starts mit dem bestehenden nonroot Controller; Exitcodes bleiben Beobachtungen |
| `review_runs.py` | Physische Hashes, geladene Images, Client-/Backendbytes, native/Hostcallbacks, Cleanup und Transportfakten |
| `transport.py` | Unterscheidet tatsächlichen lokalen HTTP/2-Reset von explizitem Remote-gRPC-Erfolg |
| `qualify_originals.py` | Bereitet vier ausgewählte Originalfälle vor; Einzelfreigabe verlangt exakte Fixturegleichheit, frische Reproduktion aller 35 Nachweisfelder und den gemeinsamen Validator |
| `write_report.py` | Erzeugt nur den eigenen EN/DE-Taskbericht und das exakte ID-JSON; ändert keine gemeinsamen Generatoren oder Ledger |

## Validierung

Im Parent-Worktree mit dem Repository-eigenen Python-Interpreter ausführen:

```sh
rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest discover -s ci/runtime/lifecycle/i12/envoy -p 'test_*.py' -v
rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -B ci/runtime/lifecycle/i12/capture_sources.py verify
```

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
