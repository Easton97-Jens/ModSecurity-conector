# Traffic-owning-Sidecar für Stock lighttpd

**Sprache:** [English](README.md) | Deutsch

Dies ist der kanonische Voll-Lifecycle-Pfad der benannten Stock-lighttpd-
Lösung. Seine Topologie ist absichtlich klein und geschlossen:

```text
client -> Common Runtime sidecar -> private, unchanged Stock lighttpd backend
```

Der Sidecar erzeugt die Common Runtime mit Connector-ID `lighttpd` und dem
exakten Integrationsmodus `stock-lighttpd-sidecar`. Er besitzt P1–P4 direkt:
P1 nach den Request-Headern, P2 bei Request-Body-EOS, P3 vor dem
Response-Commit und P4 bei Response-Body-EOS. Das direkte Stock-
`mod_msconnector`-Modul bleibt eine getrennte, exakte P1/P3-
Kompatibilitätsübersetzung (`stock-lighttpd`); es darf in dieser
Backend-Topologie nicht geladen werden, da P1/P3 sonst doppelt ausgewertet
wären.

## Grenze und Framing

Der Sidecar besitzt keine TLS-, Authentisierungs- oder Public-Listener-Schicht.
Darum müssen sowohl `--listen` als auch `--upstream` literale IPv4-
Loopback-Endpunkte im Format `127.0.0.1:<port>` sein; Wildcard-Adressen,
Hostnamen, IPv6 und Nicht-Loopback-Upstreams werden beim Start abgelehnt. Eine
Bereitstellung mit Netzwerk-, TLS- oder geteiltem Trust-Boundary muss diese
Schicht außerhalb dieser Komponente terminieren und einen gleichwertig
privaten Traffic Owner erhalten.

Pro Client-Verbindung wird genau ein HTTP/1.1-Austausch akzeptiert. Der
Sidecar schließt die Verbindung danach; dadurch existieren weder
requestübergreifender State noch Reuse-Korrelation. Unterstützt werden
Identity-Framing mit optionalem Request-`Content-Length` und Response-
`Content-Length` (ausgenommen HEAD, 204 und 304). Übliche HTTP/1.1-
Response-Reason-Phrases sowie `Connection: close`/`keep-alive` werden
akzeptiert; Connection-Felder werden vor dem Forwarding entfernt.
Nicht-Upgrade-informative `1xx`-Responses werden innerhalb der konfigurierten
Grenzen weitergeleitet und treten nicht in P3 ein; nur die folgende finale
Response tritt in P3 ein. Ein `101`-Upgrade bleibt abgelehnt.
Chunked Transfer-Encoding, Upgrades, TE, Trailer, Proxy-Connection, unbekannte
Connection-Tokens, widersprüchliche Längen, fehlerhafte Startzeilen sowie zu
große Header oder Bodies schlagen fail-closed fehl.

Die konfigurierten Common-Header-, Body- und Event-Limits bleiben maßgeblich.
Das Request-Parsen ist durch sein deklariertes Limit begrenzt. Die
Response-Verarbeitung verwendet jeweils genau einen festen begrenzten Chunk
statt einer vollständigen Response-Kopie; ihre Bytes erscheinen niemals in
Event-JSONL. Ein deklarierter Request- oder Response-Body über dem
konfigurierten Limit liefert die konfigurierte Body-Limit-Antwort
(normalerweise 413), erfasst den typisierten terminalen Zustand `body_limit`
und gibt Request oder Response nicht stillschweigend frei.

## Fehler- und Cleanup-Semantik

Eine absolute Austausch-Deadline deckt Client-Reads, Upstream-Connect/Read/
Write und Client-Output ab. Alle Worker-Sockets bleiben nonblocking;
`poll()` und deadline-aware I/O behandeln EAGAIN/EWOULDBLOCK/EINTR. Dadurch
kann ein nicht lesender Peer einen Worker nicht über die Deadline hinaus in
`send()` halten. Engine-Timeout, Connector-Fehler, Protokollfehler,
Client-Cancel und Upstream-Disconnect verwenden ihre getrennten gemeinsamen
terminalen Fehlerklassen. Erreicht eine Fehlerantwort den Client, erfasst die
Common Runtime diese tatsächliche HTTP-Hostaktion; erreicht sie ihn nicht,
erfasst sie stattdessen einen Connection-Abort.

Der Sidecar bildet Response-Header ab und schreibt sie vor dem Body. Danach
liest er jeweils einen begrenzten Response-Chunk, hängt ihn genau einmal an
Common/libModSecurity an und schreibt ihn an den Client, bevor der nächste
Chunk gelesen wird. Bei Response-EOS ruft er die P4-Finish-Operation genau
einmal auf. Ein disruptives P4-Ergebnis kann daher spät sein: Nach einem
committed Präfix erfasst Safe `log_only` und setzt fort; Strict beendet die
Client-Verbindung, statt einen nachträglichen HTTP-Deny oder -Redirect zu
versuchen. Die Runtime markiert den Response-Commit erst, nachdem die
Response-Header tatsächlich geschrieben wurden, und den Body-Start erst nach
gesendeten Bytes.

Es gibt höchstens 16 abgetrennte Austausch-Worker. Ein siebzehnter
gleichzeitiger Client erhält 503, ohne Transaktionsstate anzulegen. Jeder
Worker besitzt genau eine Transaktion, terminalisiert und zerstört sie und
dekrementiert die Active-Anzahl, bevor ein Prozess-Shutdown die gemeinsame
Runtime zerstören kann.

## Build und lokaler Komponententest

Verwende den normalen externen Build-Root und dieselbe libModSecurity-
Installation wie die anderen C-Connectoren:

```sh
export MODSECURITY_INCLUDE_DIR=/absolute/path/to/include
export MODSECURITY_LIB_DIR=/absolute/path/to/lib
export BUILD_ROOT=/var/tmp/ModSecurity-conector-build
make -C connectors/lighttpd build-lighttpd-stock-sidecar
make -C connectors/lighttpd self-test-lighttpd-stock-sidecar
```

Der Selbsttest kompiliert und führt den echten C-Sidecar auf Loopback mit einem
falschen privaten Upstream aus. Er deckt P1–P4-Allow/Block-Pfade,
mehrteilige P2/P4, Response-EOS, Body-/Header-Limits, unsicheres Framing,
Timeout, Client-Cancel, begrenzte Parallelität, Connection-Reuse und
Deadline-Cleanup bei nicht lesenden Clients ab. Er ist Sidecar-Komponenten-
Evidence und keine Behauptung, dass ein unveränderter Stock-lighttpd-Prozess
native Body-Hooks besitzt.

Das gepinnte Test-Framework baut `runtime-begin-smoke` in einem externen
Testausgabeverzeichnis. Es prüft das exakte Common-Profil und die
Streaming-P2/P4-Konfiguration gegen eine reale Runtime-Konfiguration.
Es gehört nicht zum Produktbuild oder Deployment.

## Attestation für reale Stock-Host-Evidenz

`build-lighttpd-stock-sidecar` schreibt
das geschlossene Schema-2-`stock-sidecar-artifact.manifest` neben das produktive
Sidecar. Es enthält Parent-Revision, C17-Modus, exakte Produktbinär- und
Bibliotheks-Hashes und den begrenzten
Common-/Runtime-Build-Input-Hash. Dieser Hash enthält stabile
repository-relative Namen und Inhalts-Digests aller direkten Sidecar-/Common-
Compile-Inputs, einschließlich der privaten Runtime-, Registry- und
Header-Validation-Header. Die Datei ist ausschließlich Build-Metadaten: Da
sie zusammen mit dem ausgewählten Artefakt geschrieben wird, ist sie keine
unabhängige Authentizitätsbehauptung.

Das Framework erzeugt separat ein Schema-1-`stock-sidecar-test-artifact.manifest`.
Es bindet Produktmanifest-Digest, Framework-Revision, Smoke-Quelle und
Smoke-Binärdatei. Der kleine Real-Backend-Make-Einstieg baut dieses Testartefakt
und übergibt dessen expliziten Pfad als `STOCK_SIDECAR_TEST_MANIFEST`; vor dem
Lauf werden beide Manifeste geprüft. Direkte Framework-Aufrufer müssen diesen
Pfad ebenfalls übergeben. Alte Schema-1-Produktmanifeste neu bauen, statt die
beiden Zuständigkeiten zu vermischen. Keines der Manifeste ersetzt die folgende
unabhängige Betreiber-Attestierung.

Der Real-Backend-Target verlangt daher zusätzlich, dass
`STOCK_SIDECAR_ARTIFACT_ATTESTATION` auf eine vom Operator bereitgestellte,
reguläre, nicht verlinkte, nicht gruppen-/weltweit schreibbare Datei außerhalb
der ausgewählten Stock-Build-, Sidecar- und Runtime-Roots zeigt. Sie enthält
exakt dieses Key/Value-Tupel (alle Digests sind SHA-256 in Kleinbuchstaben):

```text
schema_version=1
attestation_kind=operator_expected_artifact_tuple
connector_id=lighttpd
integration_mode=stock-lighttpd-sidecar
parent_commit_sha=<40-or-64-hex-parent-revision>
parent_source_tree_state=<clean-or-dirty>
lighttpd_version=<selected-version>
lighttpd_source_sha256=<selected-source-digest>
stock_lighttpd_binary_sha256=<host-binary-digest>
stock_lighttpd_mod_accesslog_sha256=<loaded-module-digest>
stock_lighttpd_staticfile_linkage=builtin
sidecar_binary_sha256=<sidecar-digest>
sidecar_source_inputs_sha256=<bounded-build-input-digest>
sidecar_modsecurity_library_sha256=<linked-library-digest>
sidecar_c_standard=c17
```

Der ausgewählte Contract-Build bindet `mod_staticfile` in das exakte
Host-Executable ein; `mod_accesslog.so` ist das dynamisch geladene Modul. Der
Harness prüft das exportierte Symbol `mod_staticfile_plugin_init` im
attestierten Executable sowie den exakten Digest des regulären, nicht
schreibbaren dynamischen Moduls. Er lehnt Aliase und schreibbare nicht-sticky
Ancestor-Verzeichnisse für jeden ausgewählten Artefaktpfad ab und prüft die
Digests von Start-Binary/Modul und Attestation unmittelbar vor dem Start
beider Prozesse erneut. Er prüft jeden Tuple-Wert, bevor er `lighttpd -v`
ausführt, und übernimmt nur begrenzte Identitätsmetadaten und Hashes in das
payload-freie verifizierte Receipt. Ein fehlendes, fehlerhaftes, schreibbares,
aliasiertes, im Artefaktbaum liegendes oder nicht passendes Tupel schlägt
fail-closed fehl. Das vom Operator bereitgestellte Tupel macht die lokale
Trust-Grenze explizit; es ist keine kryptografische Abwehr gegen einen
Same-UID-Akteur, der sowohl die Artefakte als auch den Operator-Input
kontrolliert.

Die ausgelieferten argv-Dateien wählen separate private, diskgestützte
Verzeichnisse unter `/var/lib/msconnector/lighttpd-stock/{all,off,safe,strict}`.
Ein Profil wird als Service-UID mit
`python3 connectors/lighttpd/launch_stock_sidecar.py --profile safe` gestartet.
Der Launcher akzeptiert ausschließlich `all`, `off`, `safe` und `strict`, liest
deren feste repository-eigene argv-Dateien und startet die installierte native
Komponente unter `/usr/libexec/msconnector/lighttpd-stock-sidecar`. Beliebige
Programm- oder argv-Dateipfade und zusätzliche Optionen sind nicht unterstützt.
Er prüft Eigentümer, Berechtigungen und nativen Artefakttyp und führt das Programm
über einen festgehaltenen Deskriptor aus. Der Launcher erstellt
fehlende Spoolverzeichnisse und verwirft unsichere bestehende Pfade ohne Änderung
ihrer Berechtigungen. Konfigurationsverzeichnisse wie `/etc/lighttpd` dürfen 0755
behalten; Spoolverzeichnisse müssen der effektiven UID gehören und 0700 haben.
`--install-root` verlagert den festen Komponentenpfad sowie absolute
Konfigurations- und Spoolpfade für gestufte Installationen. Externe Builds müssen
an diesem festen Komponentenpfad bereitgestellt werden. Regel- und
Ereignispfade im Konfigurationsinhalt sind weiterhin
an die Installation anzupassen.

`--spool-capacity-bytes` verwendet standardmäßig 268435456 (256 MiB) für die
Summe offener, auf Dateisystemblöcke gerundeter Reservierungen pro Prozess.
`--spool-free-reserve-bytes` verwendet standardmäßig 67108864 (64 MiB) für den
unprivilegiert verfügbaren freien Speicher. Dies sind technische Kapazitäten der
Disk-Zulassung, unabhängig von nativer WAF-Body-Policy. Nach P1-Allow prüft die
Zulassung das festgehaltene Dateisystem, allokiert die vollständige deklarierte
Request-Länge mit `posix_fallocate` und prüft den freien Speicher erneut, bevor
ein Body-Chunk an die native Engine gelangt. Fehler liefern 503 und einen
technischen Connector-Ressourcenfehler, niemals ein WAF-BODY_LIMIT-Ereignis.
Es gibt keinen Sparse-Datei-Fallback. Reservierungen bleiben bis zum Schließen
des Deskriptors auf jedem Ausgang bestehen, auch bei Replay, Abbruch und
Receipt-Fehlern. Eine Verzeichnissperre für die Prozesslebensdauer verwirft einen
zweiten Sidecar für dasselbe Verzeichnis. Deadline-Prüfungen vor und nach der
Allokation machen synchrone Aufrufe für reguläre Dateien nicht abbrechbar.

Ein Administrator muss root-eigene, nicht beschreibbare Vorfahren bereitstellen,
bevor ein unprivilegierter Dienst `/var/lib` verwenden kann, beispielsweise mit
`install -d -o root -g root -m 0755 /var/lib/msconnector /var/lib/msconnector/lighttpd-stock`
und anschließend `install -d -o SERVICE_UID -g SERVICE_GID -m 0700 /var/lib/msconnector/lighttpd-stock/safe`
(sowie den weiteren ausgewählten Profilen). Diese Befehle beschreiben die
Erstbereitstellung; bestehende unsichere Pfade dürfen damit nicht implizit
repariert werden. Der Launcher erstellt fehlende Kinder nur dort, wo seine
effektive UID Schreibrechte besitzt; administratorseitig bereitgestellte Pfade
prüft er ohne Rechteerhöhung.
