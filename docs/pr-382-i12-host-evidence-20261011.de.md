# PR #382: I12-Hostnachweis, 2026-10-11

**Sprache:** [English](pr-382-i12-host-evidence-20261011.md) | Deutsch

**I12 NOT COMPLETE.** Kein vollständiger erforderlicher Routenteil hat PASS.
Echte Apache-Requests zeigen nützliches begrenztes Verhalten und fünf physische
Sinkfehler; Der historische fokussierte Traefik-Native-/UDS-Allow zeigt einen physischen
`protocol_error`; der spätere Vollauf hat normale Allow-Records und bleibt wegen
fehlendem Nachweis BLOCKED, ohne globalen Regressionsanspruch.
Hoststart, HTTP 200, ein erfolgreicher Driver oder kompilierte Prüfungen schließen
die erforderliche Client-/Backend-/Transport-/Log-/Cleanup-Matrix nicht. Dieser
manuell gepflegte Bericht beschreibt das unten getestete Sourcetupel, keinen
späteren PR-Head oder Liefercommit.

## Source- und Laufbindung

| Feld | Beobachteter Wert |
| --- | --- |
| Run ID | `20261011T063350Z-0df51024008f-i12` |
| Getesteter Parent / Start-HEAD | `0df51024008fc84f0a6820f3b011055b69c3a3e2` |
| Startbranch | `work/pr382-i12-host-evidence-20261011` |
| Start-`origin/master` / Merge-Base | `3019722fbda40dc281b861c1cc38085be2f430a0` / `3019722fbda40dc281b861c1cc38085be2f430a0` |
| Framework-Gitlink / tatsächlicher HEAD | `99a7985c1be92a2297b1b59208f64df6768f2cbf` / `99a7985c1be92a2297b1b59208f64df6768f2cbf` |
| MRTS-Gitlink / tatsächlicher HEAD | `8a6bb546c4c81d8ffc7be801dceac60c6925685f` / `8a6bb546c4c81d8ffc7be801dceac60c6925685f` |
| Dirty-State bei Start | Task-Worktree, Framework und MRTS sauber; fremde Änderung im Hauptcheckout erhalten |
| libModSecurity | Installiert 3.0.14; `/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14` |
| Bibliothek-SHA256 | `32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407` |
| Bibliothek-Sourcecommit | Nicht verfügbar; Binary-/Paketidentität erfasst, kein erfundener Source-SHA |
| Plattform | Ubuntu 26.04.1 LTS; Kernel 7.0.0-38-generic; x86_64; 8 logische CPUs |
| Toolchain | GCC/G++ 15.2.0; Make 4.4.1; Go 1.27.2; curl 8.18.0 |
| Python | Parent, Apache und native Fixturewrapper 3.14.7; native Envoy-/Traefik-Helfer verwenden explizit `/usr/bin/python3` 3.14.4 |
| Hostvoraussetzungen | Apache 2.4.66; NGINX 1.31.6; HAProxy 3.2.25; Envoy 1.39.1; Traefik 3.7.13; lighttpd 1.4.85 stock und patched |

Die initialen `metadata.json`, `pre-execution.json` und `matrix.initial.json`
wurden vor Hostausführung aufbewahrt. Ihr anfänglicher Bestand fehlender Hosts
bleibt historisch; spätere Buildreceipts erfassen Bereitstellung ohne ihn
umzuschreiben. Snapshots je Versuch, echte Konfigurationshashes, Binary-/Modulidentitäten,
direkte Clientabschlüsse, originale physische Logs und Cleanupreceipts binden
einzelne Beobachtungen. Unbeobachtete Felder bleiben null. Framework-/MRTS-Source
und Gitlinks wurden nicht geändert. Erfolgreiche gepinnte Builds sind
Voraussetzungen, kein I12-PASS.


PR #382 lief später auf `498653c2a193d34b7b25b2903b1e4db1c45e7f73` weiter. Die
geprüfte Differenz besteht aus Dokumentation plus einer B09-Teständerung, ohne
Produktänderung. Dieser Bericht hält die originale getestete Bindung
`0df51024008fc84f0a6820f3b011055b69c3a3e2` und vererbt keinen PASS auf den späteren Head.

## Isolation und historischer NGINX-Bereich

Namespace- und UID-Wechselproben im Standardsandbox scheiterten. Unveränderliche
Proben außerhalb des Sandbox bestanden, doch die eigene Root-Master-Übergabe
blieb unter der installierten `bwrap//&unpriv_bwrap`-AppArmor-Grenze abgelehnt.
Keine AppArmor-Policy, Capability-Grenze oder Validierung wurde geschwächt.
Zugelassene Fixtures verwenden echte UID/GID 65534 mit null effektiven Capabilities,
offizielles bwrap, private User-/Network-/PID-Namespaces, Loopback/private UDS,
nur lesbare Root-/Source-/Framework-/Artefaktmounts und taskprivate Schreibbereiche. Root, Source, Framework und bereitgestellte
Artefakte sind nur lesbar; nicht jeder Hostmount wird als nur lesbar behauptet.
Frühere Versuche bewahren die Grenze eines unzugänglichen Root-Mode0700-
Schreibziels auf sysfs; der frische Guard maskiert sysfs. Ein namespacerelatives
UID-0-Mapping beweist keine Host-Root-Identität. Aktueller NGINX-Root/nobody-Nachweis
bleibt durch die erforderliche Identitätsübergabe BLOCKED; kompiliertes
NGINX/Modul ersetzt ihn nicht.

Historisches [R17](https://github.com/Easton97-Jens/ModSecurity-conector/pull/396#issuecomment-6101794434)
hatte 97/97 ausgewählte Required-PASS für Parent
`2f02370b07149265841411894f1a2cf7f1e978ff`, Framework
`9f41f80db7bf53b57429457bce0dda675d2ec5d7` und denselben MRTS. Sein exakter
generischer Strict-curl-Exit 52 bleibt historisch. Die geprüfte Differenz enthält
keine native NGINX-/Common-Produkt-, Build- oder Lifecycle-Änderung; CRS-Pins
und Frameworkwartung unterscheiden sich. Dieser Vergleich überträgt keinen
Runtime-PASS auf das hier getestete Tupel. H2/H3, CRS, Off, Produktion und
Protected Exact-Head werden durch das historische H1-Ergebnis nicht bewiesen.

## Erforderliche Routenteile

Zehn logische Routen ergeben dreizehn erforderliche Teile, weil SPOP, ext_authz
und forwardAuth jeweils getrennte Request- und Response-Companion-Nachweise
benötigen. Die vierzehnte lighttpd-Stock-native-Diagnosekontrolle ist ergänzend
und ersetzt den verkehrsführenden Stock-Sidecar nicht. Vollständige Routenteil-PASS:
**0**. Die ausgewählten Receipts breiterer Läufe sind abgeglichen; ihre
Driver-Exits schließen fehlende Pflichtbeobachtungen nicht und ändern diese Abnahmestatus nicht.

| Logische Route | Erforderlicher Teil | Abnahmestand / verbleibender Nachweis |
| --- | --- | --- |
| Apache native/direct | `apache-native` | FAIL: fünf physische Sinkfälle; sieben vollständige MIME-/EOS-Verträge nicht ausgeführt; weitere Pflichtfälle offen |
| NGINX native/direct | `nginx-native` | BLOCKED: aktuelle Root-Master-/nobody-Worker-Zulassung; R17 getrennt erhalten |
| HAProxy HTX direct | `haproxy-native-htx` | BLOCKED: acht echte Fälle; natives stderr getrennt vom Helfer-JSONL; direkte Client-/native Sink-/Cleanup-Lücken |
| HAProxy SPOE/SPOP + Companion | `haproxy-spop-request` | BLOCKED: getrennter Requestnachweis und vollständige physische Sink-/Pflichtfallabdeckung |
| HAProxy SPOE/SPOP + Companion | `haproxy-spop-htx-response-companion` | BLOCKED: getrennte Companion-Korrelation, gehaltene Transaktion und Hostaktion |
| Envoy ext_proc direct | `envoy-ext-proc` | BLOCKED: echte HTTP-/gRPC-Beobachtungen vorhanden; unabhängiger Backend-, Transport-, Cleanup- und Pflichtfallnachweis unvollständig |
| Envoy ext_authz + Companion | `envoy-ext-authz-request` | BLOCKED: echte Allow-/Block-Beobachtungen vorhanden; exakter Request-/Backend- und vollständiger Pflichtfallnachweis unvollständig |
| Envoy ext_authz + Companion | `envoy-ext-authz-response-companion` | BLOCKED: Companion-Events allein beweisen weder Downstream-Aktion, Cleanup noch physische Sinkfehlerbehandlung |
| Traefik Native/UDS | `traefik-native-uds` | FAIL: historischer fokussierter physischer protocol_error bleibt ausgewählt; jüngster Vollauf allein BLOCKED mit normalen Allow-/P1-/P2-/P3-/P4-Records |
| Traefik forwardAuth + Companion | `traefik-forwardauth-request` | BLOCKED: echter fokussierter Allow vorhanden; direkter Clientabschluss und vollständiger Pflichtfallnachweis unvollständig |
| Traefik forwardAuth + Companion | `traefik-forwardauth-response-companion` | BLOCKED: Response-Companion benötigt unabhängigen Aktions-/Log-/Cleanup- und Pflichtfallnachweis |
| lighttpd stock/sidecar | `lighttpd-stock-sidecar` | BLOCKED: full06-Rohdaten erhalten; genaue leere Engine-actual_action-Enumabweichung vor nativem deny451; direkter Denyclientnachweis fehlt; vier spätere Fälle NOT_EXECUTED |
| lighttpd patched/native | `lighttpd-patched-native` | BLOCKED: nur begrenzter Staticfile-Allow; full03 Trusteddirectory-ablehnung77; Strict-Abort nicht unterstützt |
| Ergänzende Stock-Kontrolle | `lighttpd-stock-native-control` | NOT_EXECUTED: kein Ersatz für erforderlichen Stock-Sidecar oder native Bodyhooks |


## Repräsentative E2E-Receiptmatrix

Unten steht eine aufbewahrte repräsentative Beobachtung je Teil; keine vollständige Fallabdeckung. `null` bedeutet unbeobachtet oder noch nicht abgeglichen. Client bezeichnet echtes HTTP / gewarteten Exit / gemessene Bytes. Driver-Exits und projizierte Diagnosen werden nicht eingesetzt. Historische Fokusfehler bleiben getrennt begrenzt.

| Test-ID | Routenteil | Host | Mode | Fall / Versuch | Client HTTP/Exit/Bytes | Backendrequests | Transport | Physisches Log | Cleanup | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `E2E-APACHE-INVALID-EVENT-PATH` | `apache-native` | `Apache 2.4.66` | `native-httpd-module` | `invalid-event-path` | `200/0/10` | `1` | `http_completed` | `main physical event absent; sink warning` | `PASS` | `FAIL` |
| null | `nginx-native` | `NGINX 1.31.6` | `root/nobody H1` | `identity admission` | null | null | null | null | null | `BLOCKED` |
| null | `haproxy-native-htx` | `HAProxy 3.2.25` | `native HTX` | `phase1_403; full02` | `403/null/93` | `0` | null | `actual native stderr deny; canonical JSONL is helper projection` | `namespace reaped; transaction null` | `BLOCKED` |
| null | `haproxy-spop-request` | `HAProxy 3.2.25` | `SPOE/SPOP request` | `p4-safe; full03` | `200/null/23` | null | null | `native request decision retained` | `namespace reaped; transaction null` | `BLOCKED` |
| null | `haproxy-spop-htx-response-companion` | `HAProxy 3.2.25` | `HTX response companion` | `missing-correlation; full03` | `503/null/107` | null | null | `actual native fail-closed response claim503` | `namespace reaped; transaction null` | `BLOCKED` |
| `E2E-envoy-ext-proc-direct-envoy-ext-proc-allow-1` | `envoy-ext-proc` | `Envoy 1.39.1` | `common_libmodsecurity_nonpromoted` | `Allow; envoy-ext-proc/unpriv-runtime-04` | `200/0/28` | `1` | null | `matching native records present` | null | `BLOCKED` |
| `E2E-envoy-ext-authz-request-envoy-allow-1` | `envoy-ext-authz-request` | `Envoy 1.39.1` | `ext_authz` | `Allow; envoy-ext-authz/unpriv-runtime-02` | `200/0/28` | null | null | `physical sink empty` | null | `BLOCKED` |
| `E2E-envoy-ext-authz-response-companion-envoy-allow-1` | `envoy-ext-authz-response-companion` | `Envoy 1.39.1` | `response companion` | `Allow; envoy-ext-authz/unpriv-runtime-02` | `200/0/28` | null | null | `physical sink empty` | null | `BLOCKED` |
| `E2E-traefik-native-uds-direct-traefik-native-p1-allow` | `traefik-native-uds` | `Traefik 3.7.13` | `Native/UDS` | `Allow; traefik-native-uds/unpriv-runtime-02` | `200/null/54` | null | null | `matching native records present` | null | `BLOCKED` |
| `E2E-traefik-forwardauth-request-traefik-forwardauth-allow` | `traefik-forwardauth-request` | `Traefik 3.7.13` | `forwardAuth` | `Allow; traefik-forwardauth/unpriv-runtime-02` | `200/null/null` | null | null | `physical sink empty` | null | `BLOCKED` |
| `E2E-traefik-forwardauth-response-companion-traefik-forwardauth-allow` | `traefik-forwardauth-response-companion` | `Traefik 3.7.13` | `response companion` | `Allow; traefik-forwardauth/unpriv-runtime-02` | `200/null/null` | null | null | `physical sink empty` | null | `BLOCKED` |
| null | `lighttpd-stock-sidecar` | `lighttpd 1.4.85` | `stock traffic-owning sidecar` | `p1_deny; full06` | `null/null/null` | `0 for /p1-block in actual access log` | null | `native engine actual_action empty then same-TX request_blocked deny451/rule9821001` | `namespace reaped; direct transaction null` | `BLOCKED` |
| null | `lighttpd-patched-native` | `lighttpd 1.4.85` | `patched borrowed hooks` | `staticfile Allow; focus02` | `200/0/32` | null | null | `native host startup log; events empty` | `namespace reaped; transaction null` | `BLOCKED` |
| null | `lighttpd-stock-native-control` | `lighttpd 1.4.85` | `advisory diagnostic control` | `not selected` | null | null | null | null | null | `NOT_EXECUTED` |

## Jüngster Envoy- und Traefik-Rohdatenreview

Der jüngste geschlossene Rohbestand enthält 27 Fälle: ext_proc-Versuch04 hat 10,
ext_authz-Versuch02 hat 5, Native/UDS-Versuch02 hat 7 und forwardAuth-Versuch02
hat 5. Strenge Nachweiszählung: **0 PASS, 0 FAIL, 27 BLOCKED**. Der physische
Allow-`protocol_error` aus dem früheren Native-/UDS-Fokus bleibt ein getrennter
historischer FAIL; jüngster Native-/UDS-Allow hat normale Events. Keiner löscht
den anderen oder begründet eine globale Produktregression.

ext_proc-Versuch03 hatte eine Fixture-Regel-/Markerabweichung; passendes
`common/rules/modsecurity_p1_p4_vectors.conf` in Versuch04 endete mit Driver-Exit
0 unter `common_libmodsecurity_nonpromoted` und echtem HTTP 200/403/413/302.
Envoy hat direkt gewarteten Client-Exit 0; viele echte Bytezählungen, explizite
Clienttransportresultate und unabhängiges Cleanup je Fall fehlen weiter.
Native/UDS erfasst echtes 200/403/429, Safe P4 55 Bytes/`completed` und Folge-200,
doch direkte Client-Exits/Backendrequestzählungen/Cleanup bleiben null.
forwardAuth hat echte Request-Block- und Response-P3-/Safe-P4-Events mit denselben
unabhängigen Nachweislücken. Request- und Response-Teile werden nicht als separate
PASS dupliziert.

## Jüngster nativer HAProxy- und lighttpd-Review

Aufbewahrtes `native-runtime-fixtures/reviews/final-native-routes-review.json`
enthält 262 Rohdatei-Hashreferenzen. Seine strengen Routenstatus bleiben BLOCKED;
begrenztes Hostverhalten und generierter Harness-PASS werden kein voller I12-PASS.

HAProxy HTX full02 führt acht echte Fälle aus: Allow, P1 403/429, leeres P2 EOS,
P2-Deny, P3-Deny, leeres P4 EOS und synchronisiertes Safe P4. Natives Deny-stderr
und Safe-`log_only` bestehen neben echtem Client 200/403/429 und gemessenen Bodys.
Erster Clientread 1 Byte, erster Upstreamchunk 17 Bytes; die Barriere belegt
Reihenfolge ohne echte First-Byte-/EOS-Timestamps. Backendzählung der Safe-Barriere
ist null, weil Helferliteral1 keine Rohrequestzählung ist. Kanonisches JSONL ist
Helferprojektion, kein nativer physischer kanonischer Sink. Direkte Client-Exits,
volle Header/Hashes/Timestamps und natives Transaktionscleanup fehlen weiter.

SPOP full03 führt sechs echte Fälle mit getrennten Requestentscheidungen und
Response-Companion-Nachweisen aus: P3-Deny liefert 403/93 Bytes, Safe P4 200/23,
fehlende Korrelation 503/107, außerdem Clientcancel, TTL-Ablauf und Verbindungsreuse.
Das native Responselog erfasst tatsächlich P4-`log_only`, fail-closed503 bei
Korrelation und Postcommit-TTL-Fehler. Gewartete Exits/EOS-Timestamps je Fall,
korrelierte Backendzählungen und native Companion-P3-/EOS-/Cleanup-Sinks fehlen.
Das globale Backendlog hat sieben Ankünfte, kann wiederholte Routennamen jedoch
nicht einzelnen Transaktionen zuordnen. Namespacedriver/eigene Kinder sind
bereinigt; kein natives Transaktionscleanup. Companionbewertung bleibt getrennt.

Gepatchtes lighttpd focus02 korrigiert das zuvor fehlende Staticfilemodul der
Fixture: echter curl0/HTTP200/32 Bytes belegt begrenzten Staticfile-Allow-Start,
bei leeren nativen Events. Full03 endet vor Hostverkehr mit Exit77, weil der
verpflichtende verschachtelte Namespace-Trusteddirectory-Guard `/` ablehnt.
Das gescheiterte Ownership-/Mode-Tupel wurde nicht erfasst, wird nicht erfunden.
Strict-Client-Abort-Fähigkeit bleibt nicht unterstützt.

Stock-lighttpd full06 erhält 16 Rohdateien mit geprüftem SHA256-Ledger, ohne
übersprungene Dateien oder Snapshotfehler. Echtes Backendaccesslog enthält nur
die zwei Allow-GETs (200/20 Bytes und 200/0); kein `/p1-block` erreicht dieses
Backend. Die erhaltene P1-`engine_decision`-Zeile hat `actual_action=""`, bevor
eine Hostaktion beobachtet ist. Der Enumvalidator des Harness schließt diesen
Leerwert aus und endet mit Exit77. Zeile2 derselben Transaktion ist echtes
`request_blocked`, `actual_action=deny`, HTTP451, `transport_result=http_status`,
Rule9821001 mit korrelierter Sequenz-/Hashkette. Diese genaue native Event-/Validator-
Vertragsabweichung beweist weder Produktregression noch unabhängigen
Clientenforcementfehler: echte Deny-Clientheader/Body/Exit/EOS bleiben null.
P2-Deny, P2-Bodylimit, P3-Deny und Safe-P4-Ratelimit bleiben NOT_EXECUTED.
Producersnapshots und Namespacecleanup sind vom fehlenden direkten Client-/
Transaktionsnachweis getrennt. Historischer full05-Rohdateiverlust bleibt getrennt
erhalten; full06 schließt diese Aufbewahrungslücke ohne Validierungsschwächung
oder Attestationsumschreibung.

## Apache-Beobachtungen und physische Sinkfehler

Die vollständige Fixture hat 19 Fälle: 16 begrenzte Beobachtungen PASS und drei
physische Sink-FAIL. Sieben begrenzte MIME-/EOS-Beobachtungen haben nicht den
vollständigen Pflichtvertrag und bleiben für die Abnahme NOT_EXECUTED. Zwei weitere
echte physische Sinkfehler sind FAIL. Der geschlossene Apache-Bestand von 21
verschiedenen Fällen enthält somit **9 PASS, 5 FAIL, 7 NOT_EXECUTED** nach dem
vollständigen Vertragsoracle. Das ist kein vollständiger Bestand aller Routen
oder auch nur aller Apache-Pflichtfälle.

| Fall | Client HTTP / Exit / Bytes | Backendrequests | Vollvertragsstatus |
| --- | --- | --- | --- |
| `E2E-APACHE-ALLOW` | 200 / 0 / 10 | 1 | PASS |
| `E2E-APACHE-P1-DENY` | 403 / 0 / 239 | 0 | PASS |
| `E2E-APACHE-P2-DENY` | 403 / 0 / 239 | 0 | PASS |
| `E2E-APACHE-P3-DENY` | 403 / 0 / 239 | 1 | PASS |
| `E2E-APACHE-P3-REDIRECT` | 302 / 0 / 256 | 1 | PASS |
| `E2E-APACHE-P4-SAFE-LATE` | 200 / 0 / 33 | 1 | PASS |
| `E2E-APACHE-P4-STRICT-LATE` | 200 / 18 / 33 | 1 | PASS |
| `E2E-APACHE-TECHNICAL-PRECOMMIT` | 500 / 0 / 571 | 0 | PASS |
| `E2E-APACHE-TECHNICAL-POSTCOMMIT` | 200 / 18 / 10 | 1 | PASS |
| `E2E-APACHE-MIME-SCOPEOUT` | 200 / 0 / 33 | 1 | NOT_EXECUTED |
| `E2E-APACHE-MISSING-CONTENT-TYPE` | 200 / 0 / 10 | 1 | NOT_EXECUTED |
| `E2E-APACHE-MISSING-CHARSET` | 200 / 0 / 10 | 1 | NOT_EXECUTED |
| `E2E-APACHE-WITH-CHARSET` | 200 / 0 / 10 | 1 | NOT_EXECUTED |
| `E2E-APACHE-EMPTY-EOS` | 200 / 0 / 0 | 1 | NOT_EXECUTED |
| `E2E-APACHE-ONE-EOS` | 200 / 0 / 10 | 1 | NOT_EXECUTED |
| `E2E-APACHE-MULTI-EOS` | 200 / 0 / 30 | 1 | NOT_EXECUTED |
| `E2E-APACHE-INVALID-EVENT-PATH` | 200 / 0 / 10 | 1 | FAIL |
| `E2E-APACHE-UNSAFE-DEVFULL` | 200 / 0 / 10 | 1 | FAIL |
| `E2E-APACHE-UNWRITABLE-EVENT-SINK` | 200 / 0 / 10 | 1 | FAIL |
| `E2E-APACHE-SINK-CLOSED-DESCRIPTOR` | 200 / 0 / 10 | 1 | FAIL |
| `E2E-APACHE-SINK-PHYSICAL-ENOSPC` | 200 / 0 / 10 | 1 | FAIL |

Echte Traces binden erste Bytes vor Backend-EOS. Safe P4 liefert alle 33 Bytes
und natives `log_only`. Strict P4 erhält 33 Bytes, dann curl-Exit 18 wegen
unvollständigen Framings mit nativem committed abort; kein pauschales
nonzero=PASS. Technischer Postcommit erhält die ersten 10 Bytes vor dem zweiten
Upstreamchunk, dann curl 18 und `invalid_engine_response`. Precommit liefert
500 ohne Backendzugriff. Folgerequests erholen sich. Worker UID65534/CapEff0,
geschlossene Hostlistener, fehlende Host-PIDs, geschlossener Backendlistener/
gestoppter Thread und Reaping des privaten Runners werden unabhängig beobachtet
statt aus Driver-Exit abgeleitet. Leere native Timestamps und null Sequenz-/Hashwerte
bleiben ohne synthetischen Ersatz erhalten.

Unsichere Zielablehnung liefert keine geprüfte Hostweitergabe: ungültiger Pfad,
`/dev/full` und nicht schreibbarer Sink liefern weiterhin 200 und erreichen das
Backend. Weitere begrenzte Fehler erreichen tatsächlich APR: geschlossener
Descriptor liefert APR 9 (und Closefehler); ein geprüfter Event-FD, auf `/dev/full`
umgeleitet, liefert APR 28. Das jeweilige physische Hauptlog ist leer, UID65534,
Mode0600, während der Client 200 erhält und das Backend einen Request. Recovery
erzeugt drei echte physische Records, verwendet Keepalive wieder und räumt auf.
Diese zwei Injektionen beweisen die beobachteten EBADF-/ENOSPC-Pfade, keine
natürliche Dateisystemerschöpfung oder jede parallele Descriptorwiederverwendung.
Kein APR-Flush-Nachweis, weil der Writer ungepuffert ist; fehlendes physisches
Haupt-`host_action` bleibt null.


## Apache-PASS-Identitätsledger

Die folgenden neun PASS-Receipts erhalten exaktes `result_record_sha256`, effektives Config-SHA256 und originale physische Logreferenzen. Pfade sind relativ zum privaten Runroot, keine öffentlichen Downloads. Physische Artefakthashes bleiben in `apache/full-review.json`.

| Test-ID | `result_record_sha256` | Config SHA256 | Originales physisches Eventlog |
| --- | --- | --- | --- |
| `E2E-APACHE-ALLOW` | `fa77c550e02ac22c8ceca3e4bca738963718cb664bb6d6e893ada8621852f11d` | `ec365b3a8e52fd41c1a82d46e85624d87d571408bdfeafec2ee377697afd5e9a` | `apache/unpriv-runtime-03/results/allow/events.jsonl` |
| `E2E-APACHE-P1-DENY` | `f1e8ee62340d7c43ac2b3e8654160d95826c469b54124077aa51a157b5802020` | `b5505fac254fc66fa525b6e3c855a1123785466c3166a36f80ffa9526e651e27` | `apache/unpriv-runtime-03/results/p1-deny/events.jsonl` |
| `E2E-APACHE-P2-DENY` | `f146eaf8aabd4dffe1d75bf5d8b13feb9e5555b3434eb691aa82ba38115b6bb8` | `8f6e0cb987dc50f1e847655d11376f92a5c0c19b1d5d5d060225a141c68fc10f` | `apache/unpriv-runtime-03/results/p2-deny/events.jsonl` |
| `E2E-APACHE-P3-DENY` | `32dbcfc2bb4fc1ecee91000fea9462b0dc53d7e369e51c6ad84952b42fbf8745` | `93cf68afd5e045925be96c65bbcf68f05bde6e83bcd846236b28ca087f6ccfbb` | `apache/unpriv-runtime-03/results/p3-deny/events.jsonl` |
| `E2E-APACHE-P3-REDIRECT` | `bf74dc9d19c4593cb1de752ead80cb6b3a775080bb0b6b41165e427d65d787ce` | `ce6e76e2b5e4f13eeeefc1e255c3e4ce1ae77fe63abc284235e88f52ccfd38fe` | `apache/unpriv-runtime-03/results/p3-redirect/events.jsonl` |
| `E2E-APACHE-P4-SAFE-LATE` | `31c8c3a5d4e6c1b0db19ccb499ba2baedb971036f7625bdbecbaaacce833c7fe` | `dbe7ab23a41fdce90cfccbf825aea7b0f7e13b0b81ec5e5d318ef2fbbb0e5b8a` | `apache/unpriv-runtime-03/results/p4-safe-late/events.jsonl` |
| `E2E-APACHE-P4-STRICT-LATE` | `5f60821b3ae4b7d30d99d23471b04a82d909ff5725b662eda1bbc8c332ce0a58` | `07a187dba67dd9b2d0e36b41d223cdc861f17497d961aeec425e033f52f866aa` | `apache/unpriv-runtime-03/results/p4-strict-late/events.jsonl` |
| `E2E-APACHE-TECHNICAL-PRECOMMIT` | `5c7e9392ca0d753e34a9fa2acb235ce04c9e0da8c0f75b2e195e87b7b6bb16e5` | `26bcd6fa5d15b5521fb1676ca8095ba0d87167559de1dfa1fa1be68dd9fba9b6` | `apache/unpriv-runtime-03/results/technical-precommit/events.jsonl` |
| `E2E-APACHE-TECHNICAL-POSTCOMMIT` | `73e9226091da1293e4f05bffc4d4e95476e1bd07c51663ab0f8ed7af52ed05c0` | `7e9108a117bc1da1d9218a055c22a28a46e8121d59c0427ac944d9b7450e6c19` | `apache/unpriv-runtime-03/results/technical-postcommit/events.jsonl` |

## Erforderliche Restfälle

I12 bleibt in der [Checkliste](pr-382-checklist.de.md) unabgehakt und aktuelle
Laufbeobachtungen vom historischen Sourcebestand in der
[Restmatrix](pr-382-i09-i12-rest-matrix.de.md) getrennt. Apaches physischer
void-Writer und SPOP ungeprüftes `fputs`/`fflush` bleiben getrennte
I11-Implementierungslücken. Diese Aufgabe liefert Nachweise und korrigiert keinen Produktcode.

| Bereich | Erforderlicher Restnachweis |
| --- | --- |
| Start / Allow / Block | Exakte Host-/Modul-/Engine-/Configidentität; deterministische Rule-IDs; echter Clientabschluss und Backend-Ausschluss wo erforderlich; unabhängige Companion-Teile |
| Technischer Pre-/Postcommit | Echter Engine-/Adapterfehler, erste typisierte Ursache, echte Precommit-Antwort oder unterstützte Postcommit-Transportaktion; kein erfolgreicher EOS erfunden |
| Body / EOS / MIME | ProcessPartial/Reject und kumulative Grenzen; deklarierte gegenüber echt gemessenen Bytes; Scope-in/out, fehlender Content-Type, Charset/CSV; leere/einzelne/mehrere Chunks und genau einmal EOS |
| Physischer Sink | Originale File-/FD-Ownership, Mode, IDs, Aktion/Ursache, Reihenfolge und echte Hashes; Serialisierungs-/Open-/Write-/Short-Write-/Closefehler und begrenzte Duplikate |
| Folge / Nachbar | Echte Verbindungwiederverwendung wo unterstützt, Nachbarstreamgesundheit und begrenzter Fehler; neue Verbindung allein beweist keine Wiederverwendung |
| Cleanup | Listener-/Socketabschluss, fehlende eigene Host-/Backend-/Service-PIDs, gewartete Childstatus und private Namespace-Bereinigung; gescheiterte Setups erhalten |

Transport-Short-Write/EAGAIN, UDS-/gRPC-Fehler und erfolgreiche Diagnoseprojektionen
beweisen keine physische Sinkfehlerbehandlung. Soft-Budget-Erkennung nach
Engine-Rückkehr beweist keinen harten Abbruch einer hängenden Engine.

## Ausgeführte Parent-Verifikation

Aufbewahrtes `verification/results.json` enthält exakte argv, cwd, Laufzeiten,
Exits und Logs; `workflow-inputs.json` bindet alle 32 aktuellen Workflowinputs.
Befehle verwenden RTK und ausdrücklich installiertes `/usr/local/bin/python3`
3.14.7. Keine Pakete, Toolchains oder Dependencydateien wurden installiert oder geändert.

| Prüfung | Echtes Ergebnis / Grenze |
| --- | --- |
| Python-Interpretervertrag | Exit 1: erforderlicher `python`-Alias fehlt trotz passendem `python3` 3.14.7 |
| `make check-ci-security-contract` | Exit 2: 177 Tests, drei Importfehler wegen fehlendem PyYAML, sechs Skips; nachfolgende Lockprüfungen nicht erreicht |
| `make test-hostruntime-preflight` | Exit 0; 27 Unittests; kein Host-I/O-Nachweis |
| Native Event-/Sink-/Lifecycle-Unittest-Batch | Exit 1; 74 Tests, 15 Assertion-/Subtestfehler, zwei Errors; 69 ausdrücklich erfolgreiche Methoden neben dem Fehlschlag |
| `make check-bounded-smoke-runtime-contract` | Exit 2; 119 Tests, vier Assertion-/Subtestfehler, 12 Errors |
| `make check-common-helpers-c17` | Exit 0; nur kompilierte Common-Prüfungen |
| actionlint 1.7.12 | Exit 0 für alle 32 Workflows plus zwei Permissionfixtures; lokale Source-Binary-Provenienz aufbewahrt |
| zizmor 1.29.0 `--offline` | Exit 0 für Workflows; unsichere Kontrollen jeweils erwarteter Exit 14; sichere Kontrollen Exit 0 |
| RTK-Verifikation | `rtk gain` Exit 0 |
| Vorläufige Dokumentationsprüfungen | Wegen fehlendem Worktree-Framework und danach nicht auflösbaren relativen Gitmetadaten gescheitert; ursprüngliche Fehlversuche bleiben erhalten. |
| Finale Dokumentations-/Change-Record-/Linkprüfungen | `make check-bilingual-docs`, `make check-doc-links`, nativer Change-Record-Check und `git diff --check`: Exit 0 in `document-mount-checks-02/results.json`. Die private Mountnamespace für statische Prüfungen zeigt echte Framework-/Gitmetadaten nur lesbar, mit privaten nur lesbaren Gitpfadaliasen; Originalrepositories und Validatoren bleiben unverändert. |

Gescheiterte native Seams enthalten veraltete Regexerwartungen direkter Rückgaben,
einen extrahierten NGINX-Off-Zweig ohne vorhergehenden technischen Fehlerpfad
und eine Envoy-Substringassertion ohne aufgerufenen NULL-Guard. Das ist benannter
Testvertragsdrift, kein unabhängiger Beweis eines Live-Bypasses. Breitere Prüfungen
treffen zudem hardcodierte leere Worktree-Frameworkpfade, fehlendes PyYAML und
UID-Grenzen des Standardsandbox. Kein Trust-Guard wurde geschwächt oder
gescheiterte Ausführung umetikettiert. Lokale Scanner belegen weder Hosted-CI,
Sonar, Protected-Abnahme noch Releasereife.

## Finale Zählung des ausgewählten Bestands

`matrix.final.json` gleicht **79 ausgewählte Records: 9 PASS, 6 FAIL, 53 BLOCKED,
11 NOT_EXECUTED** ab. Dieser begrenzte ausgewählte Bestand ist nicht die vollständige
Pflichtfallmatrix aller Routen. Die ergänzende Stock-native-Diagnosekontrolle
ist NOT_EXECUTED und nicht in 79 enthalten. Getrennte Companionrecords können
HTTP-Beobachtungen teilen, ohne den anderen Teil zu beweisen. Erforderliche
Gesamtroutenteile über 13 Teile: **0 PASS, 2 FAIL, 11 BLOCKED**: Apache und der
erhaltene historische fokussierte Native-/UDS-Fehler bleiben FAIL; spätere
Native-/UDS-Vollfälle bleiben BLOCKED.

Das normalisierte Routenteilledger unter `normalized/` erhält `metadata.json`,
`client.json`, `backend.json`, `host.json`, `cleanup.json` und `result.json` für
alle dreizehn Pflichtteile. Originalbeobachtungen bleiben erhalten und kein
synthetisches `events.jsonl` ersetzt einen physischen Sink. Unabhängige
Artefaktprüfung bestätigt **791 Referenzen: 529 Apache + 262 native**.
Identitätsprüfung macht fehlendes oder gescheitertes Verhalten nicht zu PASS.

## Aufbewahrung, Dokumentationsdiff und Lieferung

Rohnachweise bleiben lokal unter
`/var/tmp/codex/ModSecurity-conector/runs/e2e/20261011T063350Z-0df51024008f-i12`.
Dieser Pfad ist kein herunterladbares GitHub-Artefakt. Nützliche relative Receipts
sind `metadata.json`, `pre-execution.json`, `matrix.initial.json`, `matrix.final.json`, `normalized/`, Apache
`full-review.json`/`sink-review.json`, `prerequisites/open-hosts/final-review.json`,
`native-runtime-fixtures/reviews/final-native-routes-review.json`,
routebezogene Isolations-/Runtimebereiche und `verification/results.json`/`logs/`.
Receipts enthalten echte Artefakt-/Confighashes; eine Checksumme beweist Identität,
keinen semantischen PASS. Gescheiterte Setups und historische Läufe bleiben erhalten.
`SHA256SUMS` und `checksum-verification.json` binden aufbewahrte reguläre Artefakte;
nicht reguläre Ausschlüsse stehen ausdrücklich in `manifest-exclusions.json`.
Lieferreceipts unter `delivery/` bleiben getrennt von diesem Artefaktmanifest.

Der Checklistdiff ergänzt exakte aktuelle Laufbindung und unabgehakte I12c–l;
historisches I12b/R17 und alle 56 Source-Matrixzeilen bleiben unverändert.
Empfohlene Partition ist ein atomarer Dokumentationscommit mit Checklistpaar,
Restmatrixpaar, diesem Berichtpaar und dem
[Change-Record-Paar](../reports/audits/change-records/CR-20261011-pr382-i12-host-evidence.de.md)
(acht Dateien). Rohfixtures/Builds/Nachweise und lokale Pläne bleiben außerhalb.
Der Nutzer autorisierte einen gestapelten Draft PR auf
`fix/unified-native-results-events-20260921`; Liefer-/Reviewergebnisse werden erst
nach echtem Abruf erfasst. Kein Merge, Deployment, Produktfix, grüne CI oder
I12-Abschluss wird behauptet.

**I12 NOT COMPLETE – remaining required host evidence:** physische Sinkweitergabe, vollständige Body-/EOS-/MIME-Verträge, unabhängige Companion-, Nachbar- und Cleanupreceipts sowie aktuelle NGINX-Identitätszulassung bleiben offen.
