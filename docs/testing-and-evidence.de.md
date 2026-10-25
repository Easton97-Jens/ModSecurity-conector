# Tests und Nachweise

**Sprache:** [English](testing-and-evidence.md) | Deutsch

## Geltungsbereich

Tests unterscheiden Strukturprüfungen, Build-/Konfigurationsprüfungen,
fokussierten Hostverkehr, Full-Lifecycle-Ausführung und Evidence-Validierung.
Das Bestehen einer Ebene bedeutet nicht, dass eine andere bestanden hat.
Dieser Leitfaden beschreibt ausgewählte HTTP/1.1-Verträge und erhaltene
Spezialschnittstellen; er belegt weder aktuelle Readiness noch Produktionsfreigabe,
CRS-Vollständigkeit, vollständige Matrix, HTTP/2, HTTP/3 oder strikte Abnahme
jedes Connectors.

Das einzige [Aktivinventar](../config/testing/active-cases.json) wählt normales
lokales, CI- und zeitgesteuertes Verhalten. Die geschlossene Fünf-Profil-Baseline
<code>all-connectors-no-crs.yml</code> wählt Apache, HAProxy, Envoy, Traefik und
lighttpd; NGINX besitzt einen getrennten geschützten Exact-Head-Pfad. Ausgewählte
CRS-Prüfungen haben eigene Profil-IDs und Nachweise. Weder ein Fünf-Profil-
Aggregat noch ein erfolgreiches Geschwisterprofil liefert ein unbeobachtetes
Hostergebnis.

## Aktive Fälle, Zulassung und archivierte Spezialprüfungen

Dasselbe Schema-2-Inventar deklariert nun transparent 932 expandierte Fälle / 536 Ausführungen: 89 Kernfälle / 69 Ausführungen (einschließlich der ursprünglichen acht Offline-Fälle) und 843 vom Nutzer autorisierte quellgebundene Python-Offline-Ausnahmen / 467 Ausführungen. Die Kerngrenze bleibt 100 und wird vor allen Kindprozessen erzwungen; Ausnahmevarianten werden ausdrücklich gezählt. Offline-Kinder sperren Prozessstart und Netzwerkzugriff vor Imports; paketweite Discovery verschiebt Offline-Imports in dieses Kind. Rohes `unittest discover -s tests` importiert Module zunächst im Elternprozess, um ihre Hooks zu finden; geprüfte Top-Level führen keine sofortigen Prozess-/Hostaktionen aus, tatsächliche Tests laufen anschließend nur in geschützten Kindern. Dies sind Zahlen der aktuellen Auswahl, keine finale Abnahme. Native-/Go-/Connector-Szenarien fallen nicht unter diese Ausnahme.

Sonar verwendet verbindlich den Workflow aus master #420 mit dessen eigener Scope-/Go-Auswahl. Die zusätzliche PR-Coverage-Pipeline und ihre Gates wurden auf Nutzeranweisung entfernt. Die Inventargrenze gilt für die übrige Parent-Auswahl; eine globale Höchstzahl einschließlich der separaten Master-Sonar-Auswahl wird nicht behauptet.


<code>make check-active-inventory</code> meldet die tatsächliche expandierte
Fallzahl ohne Fallausführung. <code>make test</code> / <code>make test-active</code>
führen das zugelassene Inventar aus. Normale zuständige Gruppen und exakte
Fall-/Modulfilter wählen Teilmengen nach globaler Zulassung. Funktionale Checks
hinter <code>make lint</code>, <code>make quick-check</code>, Builds und CI
verwenden dieselbe Auswahl. Reine Builds, Formatierung, statische Analyse und
Security-Scans bleiben eigene Operationen; dahinter versteckte funktionale
Tests sind nicht von der Fallzählung ausgenommen. Die Wiederholung einer ID bei
begründeter Nachprüfung, Race-Lauf oder Hosted-CI kostet eine weitere Ausführung,
keinen weiteren verschiedenen aktiven Fall.

Erhaltene Spezialprüfungen benötigen einen aktuellen Auftrag für die zusätzliche
Prüfung und explizit <code>ON_DEMAND_TESTS=1</code>. Das Flag nicht global
exportieren oder normalen automatischen Defaults hinzufügen. Es ändert die
Auswahl erhaltener Spezialprüfungen; es erteilt keine Privilegien, Framework-/
MRTS-Schreibrechte, Merge-, Release- oder I12-Qualifikationsbefugnis. Historische
I12-Matrix-/Oracle-/Hostkampagnen bleiben geschlossen: Archivierung plant keine
Wiederholung und belegt kein <code>I12_COMPLETE</code>.

Die generierte [Archivdisposition](../reports/testing/test-selection-archive.generated.json)
verzeichnet erhaltene Python-Methoden und Go-Test-/Fuzz-Definitionen und bindet
ihre Quell-/Inventardigests. Nur <code>ci/tools/update-test-archive.py</code>
erzeugt sie neu. Ihre Definitionszahl ist keine vollständig expandierte
Verhaltensfallzahl, wird nicht zur aktiven Fallzahl addiert und behauptet nicht,
dass jede archivierte Assertion noch besteht. Nicht ausgewählte Parameter einer
teilweise ausgewählten Definition bleiben auf Abruf verfügbar; Native-/Skript-
Collectoren und Framework-Kataloge bleiben in ihren zuständigen Quellen.
Kein Archiveintrag ist ein ausführbarer Selektor oder ein neuer PASS.

| Erhaltener Bereich auf Abruf | Nicht mehr behauptete automatische Abdeckung |
| --- | --- |
| Vollständige Python-Vertrags-/Validator-/Installer-/Updater-Mutationssuiten | Vollständige Permutationen, Tabellen ungültiger Eingaben und historische erwartete Workflow-Layouts außerhalb benannter aktiver Kontrollen. |
| Vollständige Go-Pakete und zufällige C-/Go-Fuzz-Kampagnen | Nicht ausgewählte Tabellen-/Subtestvarianten und generierte Fuzz-Eingaben; aktive exakte Tests, ausgewählte Race-Wiederholungen und substantielle Security-Analyse bleiben. |
| Native Common-/Connector- und Runtime-Pfad-Spezialcollectoren | Vollständige Fehler-/Parametertabellen und der frühere Pfadkatalog mit 35 Szenarien; die vier gewählten echten Pfadeingaben qualifizieren nicht jede alte Pfadbedingung. |
| Vollständige NGINX-Hostkampagnen | Inheritance/Override, Mode-Repair, unsichere Ziele, USR1/Reload/Overlap, Error-Page-/Body-Buffer- und archivierte negative Konfigurationskampagnen; die gewählten Callback-Fälle On/Off belegen diese nicht. |
| Breite Smoke-, Full-Matrix-, MRTS-, H2-/H3- und historische I12-Werkzeuge | Vollständige Katalog-, Protokoll-, Oracle-, Ledger- und Hostqualifikation. Enge ausgewählte Runtime-/CRS-Ergebnisse behalten ihre eigenen Profilgrenzen. |

Das Entfernen eines Verhaltens aus der automatischen Auswahl dokumentiert
verlorene automatische Abdeckung; es löst keinen bekannten Defekt und erfindet
keinen historischen Erfolg. Archivierte Quellen und ihre ursprünglichen
Ergebnisse/Revisionen bleiben erhalten. Neue aktive Kernfälle an der Obergrenze
benötigen einen benannten Ersatz oder echte Konsolidierung mit dokumentierter
betroffener Anforderung und Risiko.

Profilnachweise bleiben getrennt: HAProxy HTX qualifiziert kein SPOE/SPOP mit
Response-Companion; Envoy ext_proc qualifiziert kein ext_authz mit Observer;
Traefik Native-UDS qualifiziert kein forwardAuth mit Observer; lighttpd Stock,
Patched-Native und Beobachtungen des alten Header-Kompatibilitätspfads
qualifizieren einander nicht. Jedes Ergebnis bleibt an sein tatsächlich
ausgewähltes Profil gebunden.

## Testebenen

| Ebene | Typisches Target | Belegt | Belegt nicht |
| --- | --- | --- | --- |
| Dokumentation und Verträge | <code>make quick-check</code>, <code>make lint</code> | Konsistenz von Quelle, Schema, Links, Sprache und Verträgen | Live-Hostverkehr |
| Build | <code>make build-&lt;connector&gt;</code> | Einen ausgewählten Buildschritt | Konfigurationsladen oder Request-/Response-Verhalten |
| Konfiguration | <code>make check-config-&lt;connector&gt;</code> | Dass die ausgewählte Konfiguration geparst oder geladen werden kann | Laufzeitverhalten |
| Fokussierter Smoke | <code>make runtime-smoke-&lt;connector&gt;</code> | Die vom Target dokumentierte enge Hostübung | Full Lifecycle oder Katalogvollständigkeit |
| Full Lifecycle auf Abruf | <code>ON_DEMAND_TESTS=1 make full-lifecycle-&lt;connector&gt;</code> | Ausgewähltes Profil plus Artefakterzeugung | Produktionsreife oder alle Protokolle |
| Evidence-Validierung | <code>make evidence-check-&lt;connector&gt;</code> | Dass vorhandene Laufartefakte den Vertrag dieses Validators erfüllen | Einen neuen Hostlauf |

Der Platzhalter <code>&lt;connector&gt;</code> ist genau einer von Apache,
NGINX, HAProxy, Envoy, Traefik oder lighttpd in der kleingeschriebenen
Target-Form.

## Kernbefehle

| Ziel | Befehlsmuster | Grenze |
| --- | --- | --- |
| Schnelle Repository-Validierung | <code>make quick-check</code> | Startet nicht jeden Host und erstellt keine kanonische Evidence |
| Ausdrücklicher Spezial-Aggregatkandidat | <code>ON_DEMAND_TESTS=1 NO_CRS_RUN_ID=&lt;run-id&gt; make full-lifecycle-all-connectors</code> | Erzeugt nur Kandidatenartefakte |
| Aggregierte Kernvalidierung | <code>NO_CRS_RUN_ID=&lt;run-id&gt; make check-six-connector-core-completion</code> | Liest finalisierte Evidence für diese Run-ID |
| Eine Konfigurationsprüfung | <code>make check-config-&lt;connector&gt;</code> | Sendet keinen Verkehr |

<code>NO_CRS_RUN_ID</code> ist ein dateisystemsicherer, nicht geheimer
Bezeichner. Er bindet Artefakte an eine Invocation; er ist kein Ergebnislabel
und kein Promotion-Mechanismus.

## Cases, Regeln und Protokollgrenzen

Das Framework besitzt wiederverwendbare YAML-Falldefinitionen, Schemata und
Normalisierung. Parent besitzt automatische Fallzulassung, Hostintegration und
ausgewählte Regel-/Konfigurationsinputs; durch Parent erreichte Framework-
Auswahlen müssen mit demselben Aktivinventar übereinstimmen. Repository-eigene No-CRS-Regeln und
IDs sind vom OWASP CRS getrennt. Ein vorbereitetes CRS-Input oder ein
quellbasierter Protokollpfad verifiziert weder CRS-Verhalten noch HTTP/2 oder
HTTP/3.

| Thema | Erforderlicher Nachweis |
| --- | --- |
| P1/P2/P3 | Ausgewählter Hostverkehr, passende Ergebnisdatensätze und profilgerechte Events |
| P4 | Phasenspezifische Artefakte plus tatsächliche Commit-/EOS-Grenze |
| First Byte vor EOS | Synchronisierte Timing- oder Transportbeobachtung, nicht nur eine abgeschlossene Response |
| Kein vollständiges Response-Buffering | Quell- und/oder Hostbeobachtung, die einen connector-eigenen vollständigen Response-Puffer ausschließt |
| Protokollclaims | Explizite Protocol-Client-, Host- und Artefaktnachweise für das genannte Protokoll |

## Evidence-Modell

Kanonische Evidence ist laufbezogen. Sie identifiziert Connector, ausgewähltes
Profil, Regeln, Run-ID, effektive Konfiguration, Status und erforderliche
Result-/Eventdatensätze. Rohe invocation-lokale Ausgabe wird nicht automatisch
befördert: Normalisierung und Validierung müssen Provenienz und die ausgewählte
Fähigkeitsgrenze erhalten.

| Artefaktklasse | Zweck | Datenschutz- und Aufbewahrungsregel |
| --- | --- | --- |
| Result-Datensätze | Case-Status und beobachtbare Response-Fakten aufzeichnen | Payload-freie Felder und begrenzte IDs behalten |
| Event-Datensätze | Phase, Aktion, Limits und Late-/Commit-Kontext erklären | Keine Request- oder Response-Bodies enthalten |
| Effektive Konfiguration | Einen Lauf an ausgewählte nicht geheime Inputs binden | Secrets und host-private Werte redigieren |
| Logs und Transportbeobachtungen | Einen angegebenen Debugging- oder Timing-Claim stützen | Nur die minimal nötigen Metadaten behalten |

Zugangsdaten, Cookies, Authorization-Werte, private Schlüssel, Zertifikate,
rohe Request-Bodies, rohe Response-Bodies oder lokale Runtime-Ausgabe werden
nicht eingecheckt.

### Archivierte NGINX-Konfigurationsspezialisten ohne Requests

Die unten erhaltenen negativen Konfigurationsverträge liegen auf Abruf
außerhalb der normalen aktiven Auswahl. Ihre historischen Receipts behalten
ihre ursprüngliche Revision; die aktiven Callback-Fälle On/Off wiederholen
oder qualifizieren diese Negativprüfungen nicht.

Die geschlossenen Konfigurationsverträge `invalid_boolean` und `invalid_size`
verwenden `ci/runtime/lifecycle/run-nginx-configtest.py`. Eine echte Invocation
`nginx -e stderr -t` muss `modsecurity maybe;` mit Exit 1 und beiden Diagnosen
`"modsecurity" directive` und `invalid boolean value` abweisen. Für
`invalid_size` bleibt die Required-ID erhalten, wird aber ausdrücklich auf
Ablehnung der entfernten API migriert: Der früher gültige Input
`modsecurity_phase4_body_limit 1048576;` muss Exit 1 und
`unknown directive "modsecurity_phase4_body_limit"` erzeugen, klassifiziert als
`removed_directive`. Dies ist kein Engine-Response-Limit-Test. Ein
nicht zugehöriger Modul-Ladefehler, eine falsche Direktive, eine fehlende
Diagnose, Timeout oder falscher Exit sind kein bestandener Negativtest.

Jede Invocation benötigt ein frisches externes Ausgabeverzeichnis unter
`/var/tmp/codex/ModSecurity-conector`, außerhalb von Checkouts und ohne
Symlink-Pfade. Der Treiber bewahrt Snapshots `nginx-binary` und
`nginx-module.so` auf und verwendet genau diese; beide sind auf je 64 MiB
begrenzt. Zusammen mit `nginx.conf`, `stdout.log` und `stderr.log` bilden sie
das digestgebundene Evidence-Bundle aus fünf Dateien; Captures sind gemeinsam
auf 64 KiB und die Ausführung auf 10 Sekunden begrenzt. `source-result.json`
und sein Companion `source-result.jsonl` mit einem Datensatz tragen Receipt
und `artifacts.configtest_dir` für den offiziellen Collector. Diese lokalen
Artefakte bleiben extern; sie sind weder Upload- noch Commit-Material.
Der selektierte Treiber führt jeden registrierten Case in einem eigenen
frischen Child `configtests/<case_id>` aus; die kanonische Aufbewahrung nutzt
`inventory/configtests/<case_id>`. Ein Boolean-Receipt erfüllt den Size-Case
nicht; unabhängig ausgeführte Cases überschreiben kein gemeinsames Bundle.

Die Verzeichniszulassung prüft den genauen externen Ausgabeparent und seine
Vorfahren sowie Build-, Results- und Konfigurationsparents des selektierten
Treibers durch den bestehenden Non-Following-Vertrag
`ensure_safe_runtime_directory`. Eigene `0755`-Parents sind zulässig;
gruppen- oder fremdschreibbare Parents werden abgelehnt. Jedes neue Case-Child
ist privat `0700`; ein bestehendes Case-Child wird vor dem Anhängen an
Results abgelehnt. Eine bestehende Resultdatei muss der effektiven UID gehören,
regulär sein, genau einen Hardlink besitzen, keine `0022`-Berechtigungsbits
haben und höchstens 4 MiB groß sein. Eine ansonsten zulässige
`0644`-Resultdatei bleibt erlaubt. Diese Prüfungen erhalten externe
Root-Containment und Checkout-Ausschluss; sie ergänzen keine HTTP-Evidence
und ändern die akzeptierten Configtest-Diagnosen nicht.

Der passende Framework-Vertrag validiert Konfigurations-Evidence, statt ein
Native-Request-Event zu erfinden. Diese Operation belegt nur Parsing/Ablehnung:
keine HTTP-Requests, Daemon-Starts, Listener, Master-/Worker-Identität, Reloads
oder Protokoll-Coverage werden behauptet. Vom Aufrufer übergebene Source-SHAs
benötigen unabhängiges Run-Provenienz-Binding; vertrauenswürdige Build-Inputs
bleiben Voraussetzung. Die Verträge sind auf `invalid_boolean` und
`invalid_size` begrenzt, nicht
auf alle Phase-0-Katalog-Cases, und können weder vollständige Required-Coverage
noch Exact-Head-E2E-PASS belegen.

### HAProxy-Hosted-Evidence-Projektion

Die feste HAProxy-Runtime-Zelle `with-crs/no-mrts` darf Evidence erst hochladen,
nachdem ihre Runtime beendet ist und ihr Cleanup-Ergebnis geprüft wurde. Sie
lädt weder den Runtime-Root, Build-Root, Cache-Root, Prozesslogs noch eine
Kopie eines dieser Roots hoch. Stattdessen wird ein Source-Receipt für den
festen HAProxy-P2-Case strikt geparst, mit vertrauenswürdigen Workflowwerten
verglichen und anschließend ausschließlich in
`haproxy-runtime-evidence.json` und `manifest.json` neu serialisiert. Beide
Dateien enthalten nur begrenzte Allowlist-Metadaten und SHA-256-Digests; sie
enthalten keinen Body, Headerwert, Cookie, Token, Credential, opaque Handle,
absoluten Pfad, rohen Log oder freien Runtime-Fehlertext.

Receipt-Bytes passieren eine feste unprivilegierte Stream-Grenze
`head --bytes=16385` und danach den Evidence-Projektor nur über Standard-
Eingabe nach der Privilegabgabe. Der Projektor akzeptiert höchstens 16 KiB und
weist das 16.419. Byte zurück; der Workflow puffert daher keine untrusted
Receipt-Ausgabe in einer Shell-Variablen. Receipt-Bytes sind niemals
Kommandozeilen-Argumente für `sudo`, `unshare` oder `setpriv`.

Projektion und Verifier weisen unerwartete Namen, Pfade, JSON-Schlüssel,
Typen, Special Files, Symlinks, Größenlimitverletzungen und Digest-Mismatches
zurück. Ihr Staging-Paket entsteht unterhalb eines neuen root-besessenen
`RUNNER_TEMP`-Childs. Das Paketverzeichnis gehört der getrennten Evidence-UID
und hat die Runtime-GID des Upload-Lesers als Gruppe: Es beginnt mit `0700`,
danach versiegelt der Projektor es mit `0550`. Die zwei festen Dateien der
Evidence-Identität bleiben `0444`, aber eine nicht zugehörige Identität kann
das `0550`-Verzeichnis nicht traversieren; der effektive lesbare Pfadzugriff
ist auf den Evidence-Owner und diese Upload-Leser-Gruppe begrenzt. Der
Runtime-/Upload-Leser erhält nur Lesen/Traversieren, niemals Verzeichnis-
Schreiben, Umbenennen, Unlink oder chmod. Der Verifier prüft diesen Ownership-
und Modusvertrag unmittelbar vor der gepinnten Upload-Action. Checkout-Code
für Runtime, Source-Export, Projektion, Verifikation und die abschließende
Workflow-Summary läuft nur nach privatem PID-/Mount-Namespace und
Privilegabgabe mit `no_new_privs`; privilegierte Operationen haben feste
nur-Staging-Pfade und führen keinen Checkout-Code aus.

Jeder eingebettete Immutable-Git-Object-Launcher verifiziert den exakten
Git-Blob-Preimage `b"blob " + decimal length + b"\0" + source`, bevor `compile`
ihn ausführen kann. `\0` ist hier Git's einzelnes NUL-Trennbyte und nicht ein
druckbarer Backslash plus Null; ein abweichender Preimage lässt den Job
fehlschlagen, bevor ausgewählter Checkout-Code ausgeführt wird.

Für eine Evidence-Receipt-Runtime fordert das Cleanup zuerst den `setsid`-
Leader zum Stoppen auf, gibt ihm ein begrenztes Reaping-Fenster, beendet dann
eine verbleibende Prozessgruppe und eskaliert nur nach Ablauf des begrenzten
Termination-Fensters auf `KILL`. Es wartet weiterhin auf den aufgezeichneten
Leader und verifiziert eine leere Prozessgruppe. Jeder fehlgeschlagene Stop-,
Wait- oder Residual-Group-Check verhindert Receipt, Projektion und Upload.

Diese Grenze zeichnet nur den festen P2-Receipt auf und beansprucht weder
P3/P4 noch Produktionsreife oder ein erfolgreiches Hosted-Ergebnis, bevor der
exakte Workflow-Lauf und sein hochgeladenes Artefakt beobachtet wurden.

## Status und Promotion

| Status | Bedeutung |
| --- | --- |
| <code>PASS</code> | Die ausgewählte Prüfung erfüllte ihre aufgezeichneten Bedingungen |
| <code>FAIL</code> | Eine erforderliche Bedingung wurde nicht erfüllt |
| <code>BLOCKED</code> | Eine deklarierte Voraussetzung war nicht verfügbar oder unsicher |
| <code>NOT EXECUTED</code> | Der Case/Pfad wurde absichtlich nicht ausgeführt |
| <code>NOT APPLICABLE</code> | Der Case/Pfad liegt außerhalb des dokumentierten Scope des ausgewählten Jobs oder Profils |
| <code>UNSUPPORTED</code> | Das ausgewählte Hostmodell kann die erforderliche Fähigkeit nicht bereitstellen |

Promotion ist Evidence-gesteuert. Ein Build, Konfigurationsladen,
Capability-Manifest, generierter Bericht oder statisches Inventar macht einen
nicht ausgeführten Case nicht zu PASS. Aktuelle Readiness und laufbezogener
Status gehören in die aktuellen Reports; dieser Guide erklärt das Modell statt
historische Statusmatrizen zu bewahren.

CI-Steuerungsdatensätze können die entsprechenden kleingeschriebenen Werte
`passed`, `failed`, `blocked`, `not_executed` und `not_applicable` verwenden.
Sie erhalten das Ergebnis der direkten Prüfung, bevor eine rekursive
Orchestrierungsschicht ihren Exitcode ersetzen kann; sie sind keine
Runtime-Evidence-Datensätze. Ein `blocked`- oder `not_applicable`-
Steuerungsdatensatz erlaubt Workflow-Erfolg nur dort, wo der konkrete
Workflow-Vertrag ihn ausdrücklich zulässt.

## Historischer Kontext

Frühere Connector-spezifische Proof-of-Concept-Zusammenfassungen,
Planungsnotizen und Zwischenstände der Evidence wurden in die
Connector-Guides, aktuellen Reports und den Architektur-/Evidence-Audit
überführt. Sie begründeten keine eigene Source of Truth und bleiben über die
Git-Historie verfügbar. Die oben beschriebene aktuelle Evidence-Grenze bleibt
unverändert.

## Lokale Entwicklung und Sicherheit

Verwenden Sie extern beschreibbare Runtime-, Cache-, Build-, Log- und
Evidence-Roots, die über dokumentierte Variablen ausgewählt werden. Das
Repository schreibt keinen Entwickler-Checkout-Ort vor. Fehlende optionale
Komponenten sollen das deklarierte Blocked-/Prerequisite-Exit-Verhalten nutzen,
statt stillschweigend eine nicht zusammenhängende System-Binary herunterzuladen,
zu installieren oder zu verwenden.

Format, Defaults, Setter und Sicherheitshinweise der Variablen stehen unter
[Variablen](reference/variables.de.md). Host-/Profilsyntax steht unter
[Konfiguration](configuration.de.md).

## Verwandte Referenzen

- [Architektur](architecture.de.md)
- [Connector-Guides](connectors/README.de.md)
- [Betrieb und Sicherheit](operations-and-security.de.md)
- [Aktuelle Reports](../reports/README.de.md)
