# Glossar

**Sprache:** [English](glossary.md) | Deutsch

Dieses Glossar definiert Repository-Begriffe. Es ersetzt nicht die kurze lokale
Erklärung, die beim ersten Auftreten eines Begriffs in einem Kommando, einer
Konfiguration oder einem Evidence-Guide erforderlich ist.

| Begriff | Bedeutung in diesem Repository |
|---|---|
| ABI | Application Binary Interface: der binäre Vertrag zwischen kompilierten Komponenten. Eine passende API garantiert allein keine ABI-Kompatibilität. |
| ALPN | Application-Layer Protocol Negotiation, der TLS-Mechanismus zur Aushandlung eines Application-Protokolls wie HTTP/2. Sein Vorhandensein ist allein kein HTTP/2-Nachweis. |
| API | Application Programming Interface: auf Source-Ebene sichtbare Funktionen, Typen und Verträge für Aufrufer. |
| APXS | Apache Extension Tool; wird von Apache-Modul-Builds für Compiler-/Linker-Einstellungen und die Modulinstallation verwendet. |
| Capability | Eine deklarierte Host-/Profil-Eigenschaft in <code>capabilities.json</code>. Sie kann implementiert, unasserted, unsupported oder nicht implementiert sein; sie ist nicht automatisch ein PASS-Ergebnis. |
| Kanonische Evidence | Ein validierter, run-spezifischer Artefaktsatz am konfigurierten Evidence-Root. Er muss Run-ID, ausgewähltes Profil sowie erforderliche Result-/Event-Informationen bewahren. |
| CRS | OWASP Core Rule Set. Die repository-eigenen No-CRS-Regeln sind davon getrennt; CRS-Eingabe vorzubereiten oder auszuwählen beweist kein CRS-Verhalten. |
| Entity Body | HTTP-Nachrichtenkörper nach dem Dekodieren des Transfer-Framings. Für die ausgewählte gepatchte lighttpd-Route ist der Entity-Body-Hook die relevante Response-Body-Repräsentation. |
| EOS | End of stream. Eine Phase kann bei EOS finalisieren, auch wenn Daten davor inkrementell eingetroffen sind. |
| Evidence | Artefakte, die eine konkrete Beobachtung stützen: Results, Events, effektive Konfiguration, Logs oder Transport-Beobachtungen. Evidence gilt für ihren Lauf und extrapoliert nicht darüber hinaus. |
| ext_authz | Envoy-Integration für externe Autorisierung. Sie entscheidet normalerweise vor der Upstream-Response und besitzt deshalb eine andere Response-Sicht als <code>ext_proc</code>. |
| ext_proc | Envoy-Integration für externe Verarbeitung. Die ausgewählte Envoy-Full-Lifecycle-Route verwendet diese Streamed-Bridge; ihr Strict-Post-Commit-Reset bleibt eine separate Nachweisfrage. |
| First Byte Before EOS | Synchronisierte Beobachtung, dass der Client ein Response-Byte erhielt, bevor die Upstream-Response EOS erreichte. Sie erfordert explizite Timing-/Transport-Artefakte, nicht nur eine abgeschlossene Response. |
| Full Lifecycle | Die ausgewählte Host-Route, die Build, Config Load, Startup, Runtime-Traffic, capability-ausgewählte No-CRS-Cases und erforderliche Artefakte an eine Identität bindet. Sie ist kein Production- oder All-Protocol-Claim. |
| HTX | Interne HTTP-Transaction-Repräsentation von HAProxy. Die ausgewählte HAProxy-Route verwendet einen nativen HTX-Filter und erreicht Response-Body-Abschluss bei HTX-EOS. |
| Integrationsmodus | Ein aufgezeichnetes Host-/Bridge-Modell wie <code>native-httpd-module</code>, <code>native-nginx-http-module</code>, <code>native-htx-filter</code>, <code>ext_proc</code>, <code>native-traefik-middleware</code> oder <code>patched-native-lighttpd</code>. |
| JSONL | JSON Lines: ein JSON-Objekt pro Zeile. Runtime-Events und -Results verwenden dieses Format, damit Records gestreamt und unabhängig validiert werden können. |
| Late Intervention | Eine angeforderte WAF-Aktion, nachdem die Response bereits committed ist. Die tatsächliche Aktion kann ein sicheres Log-only-Ergebnis, ein Abort, wo der Host ihn nachweist, oder eine andere aufgezeichnete Grenze sein. |
| No Full Response Buffering | Der Connector darf keinen connector-eigenen vollständigen Response-Body allein zur Auswertung einer Response-Body-Rule halten. Diese Eigenschaft erfordert eigene Source-/Runtime-Evidence. |
| No-CRS | Die repository-eigene Baseline ohne CRS-Include. Ihre IDs liegen im Bereich <code>1100000</code> und sind keine OWASP-CRS-IDs. |
| P1 / P2 / P3 / P4 | Die hier verwendeten ModSecurity-Verarbeitungsphasen: Request Headers; Request Body; Response Headers; Response Body. Ein Host-Modell kann unterschiedliche Teilmengen unterstützen. |
| Promotion | Der evidence-gesteuerte Vorgang, ein Run-Ergebnis zur Stützung einer genannten Capability- oder Completion-Aussage zuzulassen. Source-Wiring, Konfiguration oder ein Compatibility-Smoke können sich nicht selbst promoten. |
| QUIC | UDP-basiertes Transportprotokoll von HTTP/3. Ein konfiguriertes Binary oder Protocol-Label ist keine QUIC-/HTTP/3-Validierung. |
| Safe | Die Late-Intervention-Policy, die eine Aktion aufzeichnet, ohne einen client-sichtbaren Post-Commit-Status-Rewrite oder Connection-Abort zu behaupten. |
| SPOA / SPOE / SPOP | HAProxy Stream Processing Offload Agent, Engine und Protocol. Sie beschreiben den HAProxy-Agent-Integrationswortschatz; sie sind nicht gleichbedeutend mit dem ausgewählten nativen HTX-Filtermodus. |
| Strict | Eine getrennte Late-Intervention-Policy/-Route, die möglicherweise einen Host-sichtbaren Abort nach Commit erfordert. Sie ist nur bedeutsam, wenn ausgewählter Host und Evidence sie nachweisen. |
| TTFB | Time to first byte. In diesem Repository benötigen First-Byte-Claims bei anwendbarem Case die stärkere synchronisierte „First Byte Before EOS“-Evidence. |
| UDS | Unix domain socket, ein lokaler Interprozess-Kommunikationsendpunkt. Die ausgewählte native Traefik-Middleware verwendet einen lokalen UDS-Service; ein UDS-Pfad muss privat und für die vorgesehenen Prozesse beschreibbar sein. |
| Upstream | Der Server oder die Fixture, die dem Host-Proxy/-Modul die Response liefert. Er ist vom Downstream-Client verschieden. |
| Wire Body | Auf dem Wire dargestellte Bytes, möglicherweise einschließlich Transfer-Coding oder Content-Encoding. Er unterscheidet sich vom Entity Body. |

## Verwandte Referenzpunkte

- [Variablen und Platzhalter](../configuration/variables.de.md)
- [Build-Dokumentation](../build/README.de.md)
- [Testing-Dokumentation](../testing/README.de.md)
- [Evidence-Dokumentation](../evidence/README.de.md)

Die obigen Begriffe beschreiben die aktuelle HTTP/1.1-Kern-
Dokumentationsgrenze. Sie erheben keine Production-, CRS-, HTTP/2-, HTTP/3-,
Extended-Matrix- oder Strict-für-alle-Connectoren-Claims.
