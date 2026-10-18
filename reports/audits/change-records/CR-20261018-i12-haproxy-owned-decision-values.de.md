# Change Record: CR-20261018-i12-haproxy-owned-decision-values

**Sprache:** [English](CR-20261018-i12-haproxy-owned-decision-values.md) | Deutsch

Interne Speicherkorrektur; Quell-/Engine-Nachweise bleiben von Hostabnahme getrennt.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-i12-haproxy-owned-decision-values |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `630be0bcc7158c5c642e47bc1d6956c5b137acb7` |

## Motivation und Problemstellung

Ein echter Companion-P4-Safe-Hostlauf erreichte natives Deny403/Regel1100301, scheiterte jedoch bei OUTCOME und schloss die Clientantwort. Common hält reason/intervention-log und redirect/intervention-redirect in getrennten eigenen Puffern. Die HA-SPOP-Brücke verlangte fälschlich Zeigeridentität und wies dadurch gleiche gültige Werte vor dem physischen Common-Event zurück. Strict und Redirect durchlaufen dieselbe Grenze.

## Akzeptanzkriterien

Gleiche begrenzte Textwerte nach tatsächlicher Common-Speicherübernahme akzeptieren; fehlende, widersprüchliche, übergroße oder nicht unterstützte Metadaten weiterhin ablehnen. Daten für den Owner vor Ende ihrer Quelllebensdauer kopieren. Native Phase/Status/Regel als Autorität, erste Fehlerursache, geprüfte Sinkfehler, OUTCOME vor RELEASE und einmaliges Cleanup erhalten; kein Hosttransport-Nachweis aus einem Quell-/Engine-Test.

## Implementierungsentscheidung und Begründung

Nur copy_spop_bridge_decision ändert sich: NULL-/Form-/Statusprüfungen bleiben bestehen, native reason/redirect werden in begrenzten aufgabeneigenen Speicher kopiert und doppelte Felder über begrenzten Wertvergleich statt Zeigeridentität geprüft. Keine Common-Quelle, öffentliches Layout, Wire-Protokoll, Konfiguration, Phasenpolitik oder ursprüngliches Oracle ändert sich. Die öffentliche Konfiguration bleibt unverändert; daher dokumentiert das Change-Record-Paar die interne Korrektur ohne README-Änderung.

## Geänderte Dateien

Produkt: `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`. Fokussierte Tests: `tests/test_haproxy_spop_owned_decision.py` und `tests/haproxy_i10_spop_caller_test.c`. Dokumentation: dieses englisch/deutsche Change-Record-Paar. Der neue Test extrahiert unveränderte tatsächliche Common-Kopierfunktionen und den tatsächlichen HA-Helfer; keine der beiden Implementierungen wird durch ein Modell ersetzt.

## Ausgeführte Befehle

Alle Befehle verwendeten RTK. `rtk proxy python3 -m unittest -v tests.test_haproxy_spop_owned_decision` bestand3Tests mit6Mutanten,13ungültigen Kontrollen,128parallelen eigenen Kopien und ASan/UBSan. `rtk proxy python3 -m unittest -v tests.test_haproxy_native_companion_events tests.test_haproxy_redirect_contract.HAProxyNativeRedirect tests.test_haproxy_spop_event_sink_failures` bestand21Tests. Physische Owner-Events und Phasen-/Firstcause-/Reentry-Prüfungen bestanden2Tests mit HAPROXY_I10_BINDING_SANITIZERS=1. Drei unveränderte Transaktionsvertragsfunktionen bestanden über unittest.FunctionTestCase, darunter verzögerte Owner-Lebensdauer mit ASan/UBSan und terminale Timeout-Finalizer. `rtk proxy make check-haproxy-c17 check-haproxy-htx-overlay` bestand. Exakte argv/cwd/Exits/Loghashes und erzeugte C-/Compiler-/Binary-Belege liegen unter `/var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/product-spop/owner-deepcopy` sowie benachbarten `owner-*.json`-Belegen. Frischer vollständiger HAProxy3.2.25-Build, Binding-Selbsttest und produktiver SPOA-Build bestanden (owner-host-build.json). `rtk proxy make check-bilingual-docs check-doc-links` bestand. Bestehende direkte Backendprüfungen für Parallelität/blockierten Nachbarn, Timeout/Finalizer und einmaliges Cleanup kompilierten und bestanden mit ASan/UBSan (owner-backend-asan.json). Der abschließende4Test-Lauf wiederholte tatsächliche Common-Speicher-/Fehler-/Mutationskontrollen und physische P3/P4-Safe-/Strict-Owner-Events mit nativem403, sichtbarem403/200 und tatsächlichem Abbruchflag; alle bestanden.

## Security-Auswirkung

Begrenzte defensive Fehlerkorrektur: gleiche eigene Daten verursachen keinen irrtümlichen Failclosed-Abbruch mehr. Fehlende oder widersprüchliche Metadaten bleiben failclosed; keine Validierung, Sinkprüfung, Redaktion oder Isolation wird geschwächt. Native Daten sind vor verzögerter Verwendung im eigenen Speicher. Kein tiefer Security-Scan wurde durchgeführt.

## Runtime-Evidence

Der quellgebundene Vorher-Test kompiliert unverändertes Produkt und tatsächlichen Common-Kopierpfad und scheitert anschließend an der erwarteten erfolgreichen HA-Kopie (owner-boundary-before-v2). Nach der Korrektur besteht derselbe Vertrag. Echte SDK3.0.14-P3/P4-Events und kanonischer P3-Redirect1100202 bestehen auf ihrer Engine-/API-Ebene. Der von Root erfasste echte Safe-Hostfehler bleibt als Fehler erhalten; echte Hostwiederholungen nach dem Fix sind weiterhin erforderlich.

## Bekannte Einschränkungen

Kontrollierte Parallelität belegt unabhängige lokale Kopien und Lebensdauer, keinen privaten parallelen Hosttransport. Owner-P3/P4-Tests beobachten physische Sinkdaten und übergebene Host-OUTCOMEs; sie belegen keine tatsächliche Frontendzustellung. Der Owner lässt unbekannten Host-phase4-Modus weiterhin weg, statt Safe zu erfinden. Aus einem ACK werden weder EOS, Abbruch noch HTTP-Erfolg abgeleitet.

## Verbleibende Risiken

Vollständige Safe-Clientzustellung, Strict-Transportabbruch, Companion302-Location und Nachbarrequests erfordern unabhängige Hostabnahme nach dem Fix durch den Koordinator. Vollständige I12-Lifecycle-Eignung wird separat gegen sämtliche ursprünglichen Anforderungen geprüft.

## Nicht ausgeführte Prüfungen mit Begründung

Dieser Worker führte keinen Hostruntime, Paketinstallation, Common-Änderung, Git-Commit/Push/Merge, breiten/tiefen Security-Scan oder externe Veröffentlichung aus; Koordinator verantwortet Lieferung und echte Hostwiederholungen. Bestehende unabhängige Sink-/Phasentests bleiben für ihre geprüften Eigenschaften maßgeblich.

## Finaler Diff- und Review-Status

Begrenzten Fünf-Dateien-Diff gegen630be0bcc7158c5c642e47bc1d6956c5b137acb7 geprüft; unabhängige begrenzte Prüfung angefragt und beim Einfrieren noch offen. C17-/Overlay-/Build-/Dokumentationsprüfungen bestanden; exakte Quell- und Rohartefakthashes bleiben extern unter owner-deepcopy erhalten. Keine Git-Aktion, Lieferung oder vollständige Hostqualifikation wird behauptet.
