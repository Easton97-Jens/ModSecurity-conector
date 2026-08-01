# NGINX-Connector

**Sprache:** [English](nginx.md) | Deutsch

## Überblick

NGINX verwendet den ausgewählten Pfad <code>native-nginx-http-module</code>.
Das dynamische HTTP-Modul mappt NGINX-Request-/Response-Zustand über
connector-eigene Phasen und Filter auf libmodsecurity v3. Dieser Guide deckt
nur den ausgewählten HTTP/1.1-P1--P4-Kern ab und behauptet weder Produktion,
CRS, vollständige Matrix, HTTP/2, HTTP/3 noch Strict für alle Connectoren.

## Architektur und Ownership

Produktiver Quellcode liegt unter <code>connectors/nginx/src/</code>;
Modul-Build-Metadaten liegen unter <code>connectors/nginx/config</code>. NGINX
besitzt Main-/Location-Konfiguration create/merge, Access- und Log-Phasen,
Header-/Body-Filter, Subrequest-/End-of-Stream-Behandlung, dynamisches
Modulladen und Hostaktions-Mapping. Common liefert neutrale Konfigurations-,
Parser-, Mapping-, Limit-, Event- und Metadatenverträge, ohne
<code>ngx_http_request_t</code> oder einen NGINX-Filter zu besitzen.

| Lifecycle-Bereich | Ausgewählte NGINX-Verantwortung | Grenze |
| --- | --- | --- |
| P1/P2 | Access-Phase-Request-Mapping und Body-Abschluss | Einen Body nicht vor seinem ausgewählten End-of-Stream abschließen |
| P3 | Response-Header-Filter-Mapping | Pre-Commit-Zustand aus der Hostresponse bestimmen |
| P4 | Begrenzte Body-Filter-Aufnahme und einmaliger EOS-Abschluss | Tatsächliche Aktion und sichtbaren Status nach Commit erhalten |
| Logging | Payload-freie Event-/Result-Metadaten | JSON-/Event-Trunkierung ist von Body-Trunkierung getrennt |

## Selektive Upstream-Aufnahme

Der Parent-eigene Connector bleibt auf ModSecurity-nginx
`9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` mit seinem früheren lokalen
PR-#377-Overlay `3d72b004ff27a78ea19c6b945870e2cae62a97ac` basiert. Die
aktuelle Source-Aufnahme ist selektiv und in [der Ursprungsübersicht](../../connectors/nginx/ORIGIN.de.md)
aufgezeichnet:

- [PR #384](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/384)
  bei `65de4cd8739209f22d924d85548bd012a4d94607` behält eindeutiges finales
  Body-Processing fail-closed bei, ohne `ProcessPartial`-Append-/From-File-
  Trunkierung in einen generischen Fehler zu verwandeln.
- [PR #385](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/385)
  bei `471a2a54843bb8f560758a7e75b146db2243ab29` liefert ausgewählte
  Response-Header- und Redirect-Replacement-Behandlung. Der Parent-Task
  schließt zusätzlich fiktive synthetische `Connection`-/`Keep-Alive`-Felder
  für natives HTTP/3 als task-lokale Härtung aus.
- [PR #386](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/386)
  bei `a7fd4fcc18dc442b1b093d253f457b9317b7f588` liefert ausgewählte
  Header-Registration-Sichtbarkeit sowie Address- und Body-Loop-Behandlung.
- [PR #387](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/387)
  bei `4c1f0362ca0f25ef216ce59cad5fa6c9703c1438` prägt den Parent-eigenen
  opt-in bounded native soak (`make soak-nginx`) und die H1-Memcheck-Diagnose
  (`make memcheck-nginx`). Beide bleiben außerhalb von Default-Smoke/Test/CI
  und schreiben begrenzte payload-freie Summaries. Der source-gesteuerte
  Soak-Selektor lässt zwischen einer und acht eindeutige IDs aus seinem
  expliziten kanonischen Katalog zu und weist leere, doppelte oder außerhalb
  des Katalogs liegende Selektionen vor der Case-Discovery ab; kein Upstream-Docker,
  Workflow, Valgrind-/Helgrind-Konfiguration oder Runtime-Ergebnis wird
  importiert oder behauptet.

Die fokussierte Task-Evidence umfasst einen strikten isolierten Rebuild,
bestandene C17-/C23-/c2y-Checks, eine neu materialisierte Build-Source-SHA, die
dem Task-Filter entsprach, sowie einen bestandenen ausgewählten nativen
H1-Out-of-Scope-Fall ohne CRS und ohne MRTS. Sie behauptet keinen kanonischen
Lifecycle-, HTTP/2-, HTTP/3-, Remote-Rule-, Soak-, kanonischen Memcheck-,
Helgrind- oder Delivery-Erfolg.

## Build

Der [NGINX-Compiler-Guide](../build/compilers/nginx.de.md) beschreibt
Source-Build, Dynamic-Module-Inputs, Komponentenroots und Diagnose. Erforderliche
C17-Prüfungen sind Struktur-/Compile-Nachweise; optionale neuere
Sprachprüfungen bedeuten keine Laufzeitverifikation. Der
[NGINX-Source-Guide](../../connectors/nginx/README.de.md) bleibt der
code-nahe Einstieg.

Für diese Task bestanden der strikte isolierte Rebuild sowie C17, C23 und c2y;
die neu materialisierte Build-Source-SHA entsprach dem Task-Filter. Diese
beobachtete Build-Evidence ersetzt weder einen kanonischen Lifecycle-Lauf noch
einen finalen Exact-Head-Proof.

## Konfiguration

Vollständige NGINX-Syntax, Werte, Defaults, Kontexte, Merge-Verhalten,
Validierungshinweise und Profilbeispiele stehen in der
[NGINX-Konfigurationsreferenz](../../examples/nginx/configuration-reference.de.md).
NGINX-Variablen werden nur verwendet, wo die registrierte Direktive sie
dokumentiert. <code>modsecurity_transaction_id_expr</code> ist
Apache-spezifisch und keine NGINX-Direktive.

## P1--P4-Lifecycle und Protokollgrenze

P3-Entscheidungen gehören in den Response-Header-Pfad vor dem Header-Commit.
Der Response-Body-Filter ist ein separates P4-Timing-Modell. Ein P4-Regelmatch
belegt ohne passende Host-/Client-Artefakte weder sichtbares 403 noch Abort oder
HTTP/2- oder HTTP/3-Ergebnis.

Die Task stellt eine vor der Task bestehende Parent-Regression bei der
Content-Type-Aufnahme wieder her: Begrenzte Response-Bytes erreichen
ModSecurity unabhängig vom Connector-Content-Type-Scope. Der Scope wird erst
beim Mapping einer erkannten Intervention angewendet, sodass eine außerhalb des
Scopes liegende Intervention zu <code>log_only</code> mit
<code>content_type_not_in_scope</code> wird. Dies erhält die ausgewählte
#384-Grenze: Finales <code>msc_process_response_body()</code> mit einem
Ergebnis ungleich <code>1</code> bleibt fail-closed, während Append-/From-
File-<code>ProcessPartial</code>-Verhalten absichtlich nicht fatal bleibt.

Auf Source-Ebene erhält ein Pre-Commit-Redirect seinen `Location`-Header,
verwirft obsolet gewordene Entity-Metadaten und veranlasst den Body-Filter, den
ersetzten Response-Body zu drainen. Ein terminaler P4-Finalization-Guard stoppt
Reinspection, leitet aber die verbleibende NGINX-Chain weiterhin weiter. Keine
der beiden Aussagen ist ein client-sichtbares Redirect-, Body-Filter-, Safe-
oder Strict-Runtime-Ergebnis.

| P4-Frage | Erforderliche Beobachtung |
| --- | --- |
| Regel beobachtet | Ausgewählte native Regel und Phase-4-Metadaten |
| Deny vor Commit | Ein Hostpfad, der für die ausgewählte Response tatsächlich vor Commit liegt |
| Safe Late Result | Angeforderte Aktion, tatsächliches <code>log_only</code>, unveränderter sichtbarer Status und Late-Flag |
| Strict Late Result | Tatsächliche Abort-Aktion, erhaltener bereits sichtbarer Status und Client-/Hostnachweis |

Der ausgewählte native H1-Out-of-Scope-Fall ohne CRS und ohne MRTS bestand. Die
ausgewählten Parent-Safe-/Strict-Ergebnisse wurden als Safe
<code>log_only</code> mit unverändertem sichtbarem Status und Strict
<code>abort_connection</code> nach Commit beobachtet. Der vollständige
ausgewählte Runner endet dennoch nichtnull, weil read-only-Framework-Fixtures
diesen Contracts widersprechen: Safe erwartet den Modus als Reason, und Strict
erwartet zugleich einen stabilen <code>403</code>/eine obsolete Action trotz
Connection-Abort. Dies ist `FND-FRAMEWORK-0058` (`blocked`, `out_of_scope`);
es wird keine Framework-Änderung behauptet, und die Beobachtungen werden nicht
zu einem kanonischen Lifecycle-Pass hochgestuft.

Ein HTTP/2- oder HTTP/3-Build-Flag ist kein Transportnachweis. Source-Level-
Negotiated-Version-Mapping und die Auslassung synthetischer HTTP/1.x-Hop-by-
Hop-Header belegen kein Host-Transport-Ergebnis. Wenn ein Hostlauf ein HTTP/2-
oder HTTP/3-Applicability-Artefakt schreibt, bleibt ein nicht verfügbares
Feature nicht anwendbar und ein nicht ausgeführter Protocol-Case nicht
ausgeführt.

## Tests und Nachweise

<code>make check-config-nginx</code> validiert die Konfiguration,
<code>make full-lifecycle-nginx</code> führt einen ausgewählten nativen
Hostlauf aus. Result, Event, effektive Konfiguration, Hostversion und
Protocol-Applicability-Artefakte der ausgewählten Run-ID sind zu prüfen. Das
gemeinsame Modell steht unter [Tests und Nachweise](../testing-and-evidence.de.md).

Die kanonische Lifecycle-Containment- und die schmale Worker-sichtbare
Docroot-Projektion befinden sich unter `FND-PARENT-0078` weiterhin in Arbeit.
Daher berichtet dieser Guide keinen Erfolg für <code>runtime-smoke-nginx</code>,
Soak, kanonischen Memcheck, H2/H3, Remote-CI, SonarQube, Pull Request oder
Delivery.

### Grenze der direkten H1-Memcheck-Diagnose

Die initiale direkte H1-Valgrind-Memcheck-Diagnose beobachtete eine 8-Byte-
`definitely-lost`-Allocation auf dem NGINX-Core-Worker-Exit-Pfad. Sie ist kein
Connector- oder ModSecurity-Sicherheitsfehler. Der exakt generierte Stack wurde
gegen ein unabhängig SHA-verifiziertes offizielles `nginx-1.31.2`-Archiv
geprüft (beobachtetes SHA-256-Präfix/-Suffix `af2a957...473c`).

Das begrenzte direkte H1-O7-Artifact nach der Suppression
`direct-nginx-h1-memcheck-suppressed-20260801T234500Z-c8d9e0f1` ist nur
innerhalb dieser direkten Diagnosegrenze clean: `status=clean`, `complete=1`,
`errors_detected=0`, `error_count=0`, `definitely_lost_bytes=0`,
`indirectly_lost_bytes=0`, `possibly_lost_bytes=28160` und
`still_reachable_bytes=329918`. Der ausgewählte Connector-geladene gutartige
Fall schloss `48` Requests mit `request_failures=0`,
`worker_summary_failures=0` und `server_alive=1` ab. Der isolierte Lifecycle
zeichnete `shutdown=graceful`, `wait=exited`, `wrapper_exit_code=0` und
`containment=isolated` auf; es blieben kein NGINX- oder Valgrind-Prozess,
keine `nginx.pid` und keine Testport-Bindung zurück.

Die lokale source-controlled
[`valgrind-nginx-core-1.31.2.supp`](../../connectors/nginx/harness/valgrind-nginx-core-1.31.2.supp)
wird nicht aus Upstream kopiert. Sie matcht nur einen definiten `Memcheck:Leak`
mit der exakten NGINX-Core-Chain `malloc -> ngx_alloc -> ngx_set_environment ->
ngx_worker_process_init -> ngx_worker_process_cycle -> ngx_spawn_process ->
ngx_start_worker_processes -> ngx_master_process_cycle -> main`. Das Artifact
zeichnet `suppressed: 1 from 1` auf. Mögliche Verluste bleiben in der payload-
freien Summary sichtbar, statt unterdrückt zu werden. Ein veränderter Stack,
eine Connector- oder libmodsecurity-Diagnose oder eine Invalid-Access-Diagnose
matcht nicht und bleibt fehlschlagend.

Die source-controlled Suppression wird nur im opt-in-Modus `NGINX_MEMCHECK=1`
verwendet, nachdem alle drei Laufzeit-Identitätsgates bestanden sind: Das
ausgewählte `NGINX_BINARY` entspricht `$NGINX_PREFIX/sbin/nginx`; die
`nginx -v`-Ausgabe lautet exakt `nginx version: nginx/1.31.2`; und
`$NGINX_BUILD_DIR/verified-archives/nginx-1.31.2.tar.gz` hat die
source-controlled SHA-256
`af2a957c41da636ddc4f883e4523c6d140b4784dbce42000c364ae5092aa473c`.
Außerhalb des Memcheck-Modus behalten normale Harness-Aufrufe das bestehende
vom Aufrufer gewählte `NGINX_BINARY`-Override-Verhalten bei.

Dies ist nicht kanonische Diagnose-Evidenz: Sie umgeht weder den
`FND-PARENT-0078`-Provisioning-/Lifecycle-Block noch belegt sie ein
Runtime-Smoke-, H2/H3-, Remote-Rule-, Remote-CI-, SonarQube-, Pull-Request-
oder Delivery-Ergebnis.

## Betrieb und Fehlerbehebung

Verwenden Sie einen externen Build-/Runtime-/Evidence-Root. Bei Modul- oder
Konfigurationsfehlern sind Source-Build-Inputs, Dynamic-Module-Kompatibilität
und Config-Check-Ausgabe zu prüfen. Bei P4- oder Protocol-Fragen ist der
aufgezeichnete Commit-/EOS-Kontext des Response-Filters zu prüfen, statt aus
einer Source-Option oder einem HTTP-Status allein zu extrapolieren.

## Grenzen und Kompatibilität

NGINX-Syntax, Kontexte, Vererbung und Ausdruckssemantik sind hostspezifisch.
Apache-Ausdrucksdirektiven dürfen nicht nach NGINX kopiert werden. Response-
Body, Strict Late Action, First Byte, No-Full-Buffer und Protocol-Eigenschaften
bleiben einzeln evidence-gesteuert. Der opt-in bounded native soak und die H1-
Memcheck-Diagnose sind bei Ausführung Source-verkabelte Lifecycle-Probes, kein
Leak-Freedom- oder Transport-Claim; native Ausführung bleibt getrennt nötig.
`FND-PARENT-0080` bleibt im kanonischen Parent-Tracking `validated`, weil
aktuelles `master` weiterhin das frühere In-Scope-Ingestion-Verhalten enthält;
die Korrektur im Task-Worktree benötigt noch finalen Current-Head-Nachweis.
`FND-PARENT-0078` bleibt in Arbeit.

## Verwandte Referenzen

- [Architektur](../architecture.de.md)
- [Konfiguration](../configuration.de.md)
- [Betrieb und Sicherheit](../operations-and-security.de.md)
- [NGINX-Konfigurationsreferenz](../../examples/nginx/configuration-reference.de.md)
