# Traefik-I12-Nachweise für Autorisierung und Companion

**Sprache:** [English](README.md) | Deutsch

Dieser Parent-spezifische Producer erweitert die bestehende zentrale
Capture-Variante `traefik-forwardauth` in externen, verwerfbaren Quellkopien.
Produktdateien, zentrale I12-Matrix, gemeinsame Generatoren, Framework und MRTS
liegen außerhalb seines Schreibbereichs. Die Quellvorbereitung startet keinen
Host und qualifiziert keine ursprüngliche Anforderung.

`prepare.py` prüft und übernimmt den zentralen Quellvertrag, begrenzt die
synthetischen Probes auf eine feste Auswahl, erhält native API-Beobachtung und
unabhängige Prozess-Snapshots und erstellt einen frischen Treiber. Vor dem
Hoststart parst das bereits installierte PyYAML von `/usr/bin/python3` die erzeugte
dynamische Konfiguration. Routerstruktur, Request-Puffergrenze 4096 und
Authorization-Response-Kapazität 32768 werden getrennt geprüft. Pakete und
Toolchains werden nicht installiert.

```sh
rtk proxy python3 -B connectors/traefik/harness/i12_auth/prepare.py --repository "$PWD" --output /var/tmp/codex/ModSecurity-conector/your-run/auth-inputs --leg traefik-forwardauth-request
rtk proxy python3 -B -m unittest discover -s tests -p test_traefik_i12_auth.py -v
```

Für einen unabhängigen Companion-Lauf dient
`--leg traefik-forwardauth-response-companion`. Das gezielte Fixture für die
Authorization-Response-Kapazität wählt
`--cases auth-cap-boundary auth-cap-overlimit neighbor`. Diese beiden Probes
ersetzen den Relay-Response-Body ausdrücklich durch 32768/32769 synthetische Bytes,
nachdem die echte Engine geantwortet hat. Native und Relay-Response-Größen bleiben
getrennt. Eine Host-Grenzüberschreitung gilt nicht als native Engine-Entscheidung.

Die Ausführung erfordert vorherige Prüfung und Versiegelung der Quell-, Fixture-
und Host-/Toolchain-Ledger durch den zuständigen privaten Nonroot-Controller.
Der erhaltene Treiber erwartet die Controller-ABI `/mnt/src`, `/mnt/fixtures`,
`/mnt/artifacts/traefik`, `/task` sowie UID/GID 65534. Der Controller wird hier nicht
dupliziert. Jeder Lauf benötigt eigene Quell-/Hash-Bindung, wirksame Konfiguration,
Zulassung und abschließenden Cleanup-Beleg. Kopierte historische Binärdateien
oder Nachweise sind keine neue Ausführung.

Der unabhängige Client erhält Socketbytes und Exit-Belege. Das Backend erhält
Request-/Response-Byte-Hashes. Ein begrenztes Autorisierungs-Relay protokolliert
getrennt tatsächliche Autorisierungssamples und Engine-Statuswerte. Fehlende oder
ungültige Handles sowie ein ausdrücklich fehlerhafter MRC1-Peer derselben UID
prüfen Fehlergrenzen des Observers. Diese injizierten Fehler bleiben von nativen
Engine-Ergebnissen getrennt. Die verkürzte Backendantwort erhält ihren
Client-Parserfehler; der Nachbar-Probe läuft trotzdem. Weder ein Writer-Rückgabewert
noch TCP-EOF belegt natives EOS oder tatsächlichen Client-Commit.

`review.py` liest physische Artefakte und prüft Content-Length beziehungsweise
vollständiges Chunk-Framing. `packets.py` schlägt 35 vorgeschriebene Beobachtungen
für ausgewählte ursprüngliche Fälle vor. Oracle-Auswertung, Urteil und Root-Prüfung
bleiben offen. Fehlende Framework-/MRTS-Revisionsidentitäten werden nicht ersetzt.
Die Qualifikation erfolgt durch unabhängige Root-Prüfung einschließlich der
Metadatenanforderungen des ausgewählten ursprünglichen Falls.

Frische Nachweise vom 15. Oktober 2026 zeigen Host-Request 4097 ->401 vor der
Autorisierung, native Requests 1500/4096 ->403, P3-Deny ->403, P4 Safe ->200,
Observer-Fehler ->503 und eine vollständige 40019-Byte-Anwendungsantwort trotz
Authorization-Response-Kapazität 32768. Der getrennte Kapazitätskontrolllauf maß
32768 ->200 mit Backendzugriff und 32769 ->401 ohne Backendzugriff nach nativer
Allow-Antwort 200. Separate Request- und Companion-Läufe erfassten jeweils 13
native Allokationen, Logging-Aufrufe und Freigaben; danach bestanden keine
laufenden Aufrufe oder lebenden Zuordnungen und der Prozess-Cleanup war sauber.

Die Nachweise erhalten außerdem eine Metadatenabweichung: Tatsächliche
P4 Safe-Log-only-Events melden `late_intervention=false`; das Feld `late_intervention_mode` fehlt.
Damit ist das ursprüngliche Safe-Metadaten-Oracle vollständig qualifiziert FAIL. Beim großen
Response erhielt der Client bereits vor nativem P4 Bytes; dies belegt den
Wire-Commit unabhängig. POST-Clientrequests erzeugten native Common-Events mit
Methode GET des Autorisierungsrequests. Die Prüfung der ursprünglichen
Anwendungsmethode ist hier deshalb nicht belegt. Produktdiagnose und Reparatur
gehören in die zuständige Übergabe, nicht in diesen Producer. Eine vollständige
Abdeckung sämtlicher ursprünglicher IDs wird nicht behauptet.
