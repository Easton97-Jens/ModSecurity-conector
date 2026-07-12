# lighttpd-Validierung

**Sprache:** [English](validation.md) | Deutsch


Status: `minimal_runtime_smoke` für den nativen Phase-1-Header-Pfad

## Beweisschichten

| Schicht | Ziel | Verifiziertes Verhalten |
| --- | --- | --- |
| Legacy-Brückenbau | `build-lighttpd-bridge` | Nur kompilieren |
| Selbsttest der Legacy-Brücke | `self-test-lighttpd-bridge` | nur lokale Sonde; keine Host-Beweise |
| Native Modulerstellung | `build-lighttpd-connector` | C17 PIC kompilieren und verknüpfen mit `-Werror` |
| Konfiguration laden | `check-lighttpd-config` | real lighttpd 1.4.84 lädt Modul, validiert allgemeine Konfiguration und Regeln |
| Smoke-Test starten | `start-smoke-lighttpd` | Der eigentliche Prozess beginnt, bleibt am Leben und stoppt sauber. null Anfragen |
| Laufzeitrauch | `runtime-smoke-lighttpd` | Der echte Hostpfad gibt die Basislinie 200 und die Phase-1-Regel 403 | zurück |
| Gepatchter Kern + Modul-Build | `build-lighttpd-patched-host` | 1.4.84-Kern und -Modul kopiert/gepatcht/konfiguriert/installiert, bereitgestellt mit passenden ABI-Markern und Hashes |
| Gepatchte Hostlast | `check-lighttpd-patched-host` | Die gestaffelte gepatchte Binärdatei exportiert Hook-Symbole und lädt das gestaffelte Modul über echtes `lighttpd -tt` |
| Gepatchter Lebenszyklusrauch | `runtime-smoke-lighttpd-patched` | isolierte gepatchte Host-Baseline 200 und Phase-1-Regel 403; Beim eingecheckten Aufruf bleibt das Antwort-Streaming deaktiviert |
| Entscheidungsereignis | Laufzeitrauch | JSONL enthält `connector=lighttpd` und `rule_id=1000001`; kein Körpernutzlastfeld |

## Native Konfigurationsladeprüfung

Der Harness generiert eine temporäre Common Runtime-Konfiguration und lighttpd
Konfiguration unten `BUILD_ROOT`. Es ruft auf:

```text
LIGHTTPD_BIN -m <connector-module-dir> -tt -f <generated-config>
```

Dies führt dazu, dass der eigentliche Loader `mod_msconnector.so` auflöst und das Plugin ausführt
Initialisierung/Standard-Setup, Validierung der allgemeinen Konfiguration, Initialisierung
libmodsecurity und laden Sie die Zielregeldatei.

## Anfragefrei Smoke-Test starten

`start-smoke-lighttpd` wiederholt zuerst die Konfigurationsladevalidierung und startet lighttpd in
Vordergrundmodus, prüft die PID nach dem Start, sendet keine Anfrage, beendet den
Prozess und wartet auf ein sauberes Herunterfahren. Seine PASS-Zeile zeichnet `requests=0` auf.

## Minimaler Laufzeitrauch

`runtime-smoke-lighttpd` ist absichtlich getrennt. Mit Kompatibilitätsmodul
Autoload deaktiviert, es verwendet den Lighttpd-Kernpfad `OPTIONS *`, also nur den nativen
Das Connector-Modul wird im temporären Modulverzeichnis benötigt.

Es überprüft:

1. `OPTIONS *` ohne Testheader gibt HTTP 200 zurück.
2. Die gleiche echte Lighttpd-Anfrage mit `X-Modsec-Smoke: block` gibt HTTP 403 zurück.
3. Die Common/libmodsecurity-Regel `1000001` wird im JSONL-Ereignis identifiziert.
4. Das Ereignis trägt Connector-Metadaten und enthält keinen Anfrage-/Antworttext
   Nutzlastfeld.
5. Der Host-Prozess bleibt stabil und wird sauber gestoppt.

Der Block wird aus `common/rules/modsecurity_targeted_smoke.conf` und hergestellt
vom Modul mit `http_status_set_err()` abgebildet.

## Patched-Host-Grenze

Das gepatchte Ziel ist absichtlich vom Standardkompatibilitätspfad getrennt
und generischer No-CRS-Läufer. Das Full-Lifecycle-Profil wählt es aus. Es
kopiert und patcht nur lighttpd 1.4.84, erstellt und stellt den Kern und das Modul bereit
Validiert zusammen die passende Plugin-ABI über `lighttpd -tt` und führt sie dann aus
nur der schmale Phase-1-Smoke-Test. Seine eingecheckte generierte Laufzeitdatei erfordert
Beide Körpermodi sind `none` und ihre Manifestdatensätze
`phase4_runtime_evidence=not_executed`.

Der Patch ruft seinen Antwortrückruf in `http_chunk.c` vor HTTP/1 auf
Transfer-Framing, nicht bei `network_write()` oder auf `r->write_queue`. Im
Im ausgewählten Bereich empfängt es die aktuelle synchrone, geliehene Identitätsentität
Bereich mit einem monotonen Offset und einem einzelnen EOS. Das Modul hängt den Bereich an an
Common Runtime und ruft die Phase-4-Finish-API nur unter EOS auf. Der Rückruf
geschieht vor Socket-Schreibvorgängen, sodass ein späterer kurzer Schreibvorgang oder `EAGAIN` nicht möglich ist
Doppelprüfung. Dies ist ein Quell-/Build- und statisches Vertragsergebnis, kein
Host-Fehlerinjektion oder Antwort-Stream-Laufzeitergebnis. gzip/br, HTTP/2 und
Ungeprüfte Datei-/Zero-Copy-Ausgaberouten liegen außerhalb des ausgewählten Vertrags.

Bei einer störenden EOS-Entscheidung bleibt das Verhalten der sicheren/minimalen Quelle erhalten
sichtbare Antwort und Aufzeichnungen `log_only`; strict protokolliert explizit `NOT EXECUTED`
und geht weiter. Kein echter Kunde hat eine Verpflichtung eingegangen, ein unvollständiger Körper,
Wirtsüberleben und eine anschließende unabhängige Anfrage, sodass keines der beiden Ergebnisse vorliegt
kanonische P4/späte Interventionsbeweise.

## Ressourcen- und Eigentumsprüfungen

Beide Mapper erzwingen vor der Laufzeit Grenzwerte für die Anzahl der Header und die Gesamtanzahl der Header-Bytes
Eintrag. Gemeinsame Ressourcenwächter erzwingen den verbleibenden konfigurierten Header und Body
Grenzen. Körperdaten ungleich Null werden niemals beworben. Header-Arrays und die Laufzeit
Transaktionen werden beim Zurücksetzen der Anforderung zerstört, einschließlich Anforderungszuordnung und
Transaktionsanfangsfehlerpfade.

Repository-C-Standard prüft den Kompilierungs-Connector-C-Code mit C17, optional C23,
und optionale Future-C-Modi. Für den nativen Build ist nur C17 erforderlich.

## Ausdrücklich nicht bestätigt

Die aktuellen Beweise bestätigen nicht:

- Response-Body-Streaming-Laufzeit, Phase 4 oder spätes Eingreifen;
- Short-Write/EAGAIN-Fehlerinjektion, Antwortkürzung oder Body-Limits;
- Umleitungs-/Trennungs-/Verbindungsabbruchverhalten;
- Multi-Worker-/Thread-Belastung, langfristige Belastbarkeit oder Produktionshärtung;
- CRS-Belastung/-Wirksamkeit oder eine beliebige vollständige CRS-Matrix;
- Sicherheitsüberprüfung, Produktionsbereitschaft oder Vollmatrixbereitschaft.

Daher verwenden Connector-Metadaten `minimal_runtime_smoke` und
`partial_runtime_path`, kein umfassender verifizierter oder Produktionsstatus.

## Kanonische Phase-4-Validierung

Das Stock-Modul implementiert keinen Response-Body-Hook. Die gepatchte Version 1.4.84
Das Modul verfügt über einen Identitäts-Entity-Body-Quellpfad, aber keinen kanonischen Streaming-Host
laufen. Folglich `response_body_buffered`, `phase4`,
`phase4_rule_evaluation`, `phase4_pre_commit_deny`, `late_intervention`,
`late_intervention_log_only`, `late_intervention_abort` und
`late_intervention_status_metadata` bleiben `not_implemented` für die ausgewählten
Evidenzprofil.

Phase-4-Fälle bleiben `NOT_EXECUTED` (oder werden durch die Fähigkeitsauswahl weggelassen)
bis echte Host- und Client-Artefakte das Timing und das Transportergebnis belegen.
Sie sind nicht `UNSUPPORTED`: Dies betrifft das ausgewählte Evidenzprofil, nicht ein
Unmöglichkeit in Lighttpd. Der Response-Start-Hook, der statische Quellvertrag und
Phase-1-Smoke-Test beweist keine für den Kunden sichtbare Phase-4-Regel, ursprünglich/angefordert/
sichtbarer Antwortstatus, eine verspätete Aktion oder ein Abbruch. Veranstaltungen und Meldungen bleiben bestehen
Nur Metadaten.
