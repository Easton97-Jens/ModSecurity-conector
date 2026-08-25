# lighttpd-Connector

**Sprache:** [English](lighttpd.md) | Deutsch

## Überblick

lighttpd verwendet den ausgewählten <code>patched-native-lighttpd</code>-Pfad
mit <code>mod_msconnector.so</code>. Das ausgewählte Profil ist
HTTP/1.1-fokussiert und verwendet eine versionierte Patched-Host-Grenze für
geliehene Body-Ranges. Es behauptet keine Produktionsreife, keine
Sicherheitsverifikation, keine CRS-Verifikation, keine vollständige Matrix,
keine HTTP/2-/HTTP/3-Abdeckung und keine kanonische P4-Runtime-Evidence.

## Architektur und Ownership

Die Plugin-Lifecycle-Schicht ist host-eigen, und der Mapper ist die einzige
lighttpd-API-Übersetzungsschicht. Common Runtime und Common-SDK-Typen bleiben
frei von lighttpd-Callback-Typen. Eine Runtime wird aus server-scoped
Konfiguration initialisiert; jeder Request erhält bis zum Request-Reset seine
eigene Transaktion und Mapper-Storage.

| Lifecycle-Bereich | Ausgewählte lighttpd-Verantwortung | Grenze |
| --- | --- | --- |
| P1 | URI-/Request-Header mappen und eine zulässige Request-Entscheidung anwenden | Der enge Smoke ist keine breite Hostgarantie |
| P2 | Gepatchte geliehene Request-Body-Ranges inspizieren, während das ausgewählte HTTP/1.1-`mod_proxy`-Gate bis EOS puffert | Nur ein Phase-2-Allow darf den Upstream erreichen; dies ist kein allgemeines Upstream-Streaming |
| P3 | Response-Metadaten bei Response-Start mappen | Response-Status-/Action-Semantik bleibt hostspezifisch |
| P4 | Identity-Entity-Ranges vor HTTP/1-Transfer-Framing empfangen und einmal bei EOS abschließen | Kein Socket-Queue-Callback und keine connector-eigene Body-Queue |
| Cleanup | Mapper-Storage und Transaktion bei Request-Reset freigeben | Statische Lifetime-Checks sind kein Nachweis für Langzeitresilienz |

## Build

Der [lighttpd-Compiler-Guide](../build/compilers/lighttpd.de.md) beschreibt
natives Modul, gepatchten Host, ABI-Prüfungen, Source-Inputs und
Konfigurationsladen. Der [lighttpd-Source-Guide](../../connectors/lighttpd/README.de.md)
bleibt der code-nahe Einstieg. Build-/Load-/Start-Stufen sind von Request-
Verkehr und Evidence-Promotion getrennt.

## Konfiguration

Vollständige Server-/Plugin-/Common-Runtime-Syntax, Defaults, Scopes,
Kompatibilitätsfelder, Profile und Validierungsdetails stehen in der
[lighttpd-Konfigurationsreferenz](../../examples/lighttpd/configuration-reference.de.md).
Das ausgewählte native Profil ist vom beibehaltenen Sidecar-Proxy-
Kompatibilitätsbeispiel getrennt.

## HTTP/1.1-Pre-Upstream-Phase-2-Gate

Für `request_body_mode=streaming` unterdrückt das ausgewählte gepatchte
HTTP/1.1-`mod_proxy`-Profil aktives Host-Request-Streaming vor jedem
Body-Lesen. Der Host puffert Request-Bytes deshalb bis zu terminalem EOS und
der Phase-2-Allow-Entscheidung; erst dann darf der Proxy verbinden und den
Request weiterleiten. Der validierte verzögerte Allow-Gegenfall wurde am
Upstream als `Content-Length` neu gerahmt.

Das Profil verlangt `mod_proxy` vor `mod_msconnector`, ein positives Common-
Request-Body-Limit, `body_limit_action=reject` und das passende
gepatchte Host-/Modulpaar. Es weist vorab konfigurierte
`server.stream-request-body`, `Incremental` und ausdrücklich aktivierte
body-tragende `Upgrade`- plus `gw.upgrade-with-request-body`-Anfragen vor
einer Upstream-Verbindung mit `501` ab. Eine Streaming-Konfiguration mit
`body_limit_action=process_partial` wird bereits beim Laden der Konfiguration
vor einem Listener oder einer Upstream-Verbindung abgewiesen. Dies ist kein
Claim für HTTP/2, HTTP/3, andere Stream-Handler, Response-Body-P4,
unbeschränktes Upstream-Streaming oder Production-Readiness.

Die Grenze für den zurückgehaltenen Body beruht auf dem positiven Common-
`request_body_limit` (standardmäßig 1 MiB) und einem ablehnenden Lesezyklus.
Das Modul konfiguriert `server.max-request-size` nicht; dieser Wert bleibt eine
unabhängige Host-seitige Defense-in-Depth-Grenze.

## P1--P4-Lifecycle und Entity-Body-Grenze

Der gepatchte Host ruft den ausgewählten Response-Callback auf synchronen
geliehenen Identity-Entity-Ranges vor dem Transfer-Framing auf. Er erhöht einen
monotonen Entity-Offset und signalisiert EOS einmal. Spätere Socket-Kurzschreib-
oder Retry-Behandlung darf keine bereits aufgenommene Entity-Range duplizieren;
dies ist ein Source-/Static-Vertrag, kein Fault-Injection-Runtime-Claim.

| P4-Frage | Aktuelle Grenze |
| --- | --- |
| Response-Body-Hook | Gepatchter Identity-Entity-Body-Source-Pfad existiert |
| Safe-/Minimal-Ergebnis | Sichtbare Response erhalten und konservatives <code>log_only</code>-Verhalten aufzeichnen |
| Strict-Ergebnis | Ausdrücklich nicht ausgeführt ohne client-validierte Host-Abort-Primitive |
| Streaming/Limits | Braucht ein reales ausgewähltes Host-/Client-Artefakt zur Promotion |

gzip/br, HTTP/2, nicht untersuchte File-/Zero-Copy-Ausgabe, Short-Write-
Fault-Injection und nicht ausgewählte Buffering-Modi liegen außerhalb des
ausgewählten Vertrags.

## Tests und Nachweise

<code>make check-lighttpd-config</code> prüft reales Modul-/Konfigurationsladen;
das ausgewählte Lifecycle-Target führt eine laufbezogene Hostübung aus. Der
enge native Smoke kann nur seine angegebene Request-Pfad-Beobachtung belegen.
`connectors/lighttpd/harness/run_phase2_pre_upstream_gate.py` liefert zusätzlich
einen Repository-eigenen, payload-sicheren Loopback-Nachweis: Ein verzögerter
Phase-2-Marker endete mit `403` und null Upstream-Verbindungen vor EOS, und
ein verzögerter benigner Chunked-Request erreichte den Upstream erst nach
EOS/Allow.
Der gleiche Runner belegt die profil-lokale `process_partial`-
Konfigurationsablehnung, ohne Request-Nutzdaten aufzubewahren.
P4- und Late-Intervention-Facets bleiben nicht ausgeführt oder
capability-selected, bis reale Host-/Client-Artefakte Timing und sichtbares
Ergebnis belegen. Siehe [Tests und Nachweise](../testing-and-evidence.de.md).

## Betrieb und Fehlerbehebung

Matching gepatchter Core und Modul werden gemeinsam in einem externen Build-Root
gestaged. Bei Loader-/Config-Fehlern sind ABI-Marker, Modulverzeichnis,
Common-Runtime-Konfiguration, Rule-Load und die reale
<code>lighttpd -tt</code>-Ausgabe zu prüfen. Modul-, Runtime-, Log- und
Evidence-Pfade bleiben außerhalb des Checkouts.

## Grenzen und Kompatibilität

Der Legacy-Sidecar-Proxy ist nur Kompatibilität und wird nicht zu nativem
lighttpd-Verhalten. Das ausgewählte Evidence-Profil belegt ohne dedizierte
Artefakte weder P4-Regelauswertung noch sichtbare Late-Action, Abort,
Response-Trunkierung, vollständiges CRS-Verhalten oder Produktionshärtung.

## No-CRS-Fixture-Isolation

Die No-CRS-Baseline des gepatchten Lifecycles verwendet den vertrauenswürdigen
privaten Namespace-Runner aus dem [Harness-Guide](../../connectors/lighttpd/harness/README.de.md).
Root-eigene `/usr/bin/unshare`, das feste `/usr/bin/dash` und
`/usr/bin/mount` und danach `/usr/bin/bwrap` errichten die User-, Mount- und
PID-Grenze. Das Shell-Setup macht die Propagation privat und mountet ein
privates `nosuid,nodev,noexec`-tmpfs auf `/tmp`. Bwrap stellt nur die minimalen
schreibgeschützten System- und Runtime-Binds bereit, die der Harness benötigt,
sowie den exakten Task-eigenen Smoke-Root als einzigen beschreibbaren Bind.
Der Fixture-Root hat den Modus 0700.

Das Namespace-Setup ist capability-geprüft. Nach dem Setup bestätigt der
Runner, dass alle Capability-Sets einschließlich Bounding- und Ambient-Set
leer sind und `no_new_privs` aktiviert ist, bevor der Test-Harness startet.
Fehlende Kernel-Capabilities oder eine fehlgeschlagene Attestierung führen zu
einem fail-closed Abbruch; das frühere Cleanup aus Pfadprüfung und
anschließendem `rmdir` ist kein Fallback.

Das Fixture-Cleanup ist an die Lebensdauer von Kindprozess und Namespace
gebunden. Reguläre Fertigstellung, Testfehler, Timeout, Signal,
Helper-Fehler und teilweise Initialisierung beenden die Kindprozessgruppe und
geben den privaten Namespace frei. Der finale Namespace-State-Verifier prüft
ausschließlich Capability-Sets, `no_new_privs`, den Mount-Zustand und die
Device/Inode-Identität (`dev:ino`) des festen Fixture-Roots. Der
Descriptor-I/O-Cleanup-Befehl prüft separat das Allowlist-Inventar der
Fixture-Blätter, behält jedes Blatt und löscht nichts beziehungsweise löst den
Fixture-Pfad nicht erneut auf. Alle Blätter und das Verzeichnis verschwinden
beim Abbau des privaten tmpfs-Namespace.

Bedrohungsmodell: Ein Prozess mit derselben UID kann den früheren Fixture-Pfad
durch Umbenennen, Ersetzen oder Neuanlegen in ein Race zwingen. Der private
Namespace und der kontrollierte beschreibbare Root sorgen dafür, dass die
Freigabe des Namespace die Fixture-Mounts entfernt, ohne eine über den
Host-Pfad ausgewählte Ersetzung zu löschen.

Der aktuelle verschachtelte lokale Container stellt nur eine einzeilige
UID-/GID-Zuordnung bereit; daher kann der vollständige Produktionspfad für
Nicht-root lokal nicht ausgeführt werden. Das ist eine Validierungsgrenze und
keine Erlaubnis, die fail-closed-Voraussetzungsprüfungen abzuschwächen.

## Verwandte Referenzen

- [Architektur](../architecture.de.md)
- [Konfiguration](../configuration.de.md)
- [Betrieb und Sicherheit](../operations-and-security.de.md)
- [lighttpd-Konfigurationsreferenz](../../examples/lighttpd/configuration-reference.de.md)
