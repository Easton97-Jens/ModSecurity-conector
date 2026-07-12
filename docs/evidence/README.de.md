# Evidence-Dokumentation

**Sprache:** [English](README.md) | Deutsch

Evidence ist der run-spezifische Nachweis, der eine konkrete Testbeobachtung
stützt. Sie ist keine dauerhafte Zusicherung außerhalb ihres ausgewählten
Host-Profils, ihrer Rules, ihres Connectors und ihrer Run-ID. Diese
Dokumentation erhebt keinen Production-, CRS-, HTTP/2-, HTTP/3-, vollständige-
Matrix- oder Strict-für-alle-Connectoren-Claim.

## Evidence-Ort und Platzhalter

Kanonische No-CRS-Evidence ist konzeptionell so organisiert:

~~~text
<evidence-root>/<connector>/<run-id>/
~~~

<code>&lt;evidence-root&gt;</code> ist ein absoluter, beschreibbarer
Evidence-Elternpfad, zum Beispiel
<code>/srv/modsecurity-work/evidence/no-crs-evidence</code>. Er ist nicht der
literale Text <code>&lt;evidence-root&gt;</code>, nicht der Repository-Checkout
und kein Secret-haltiges Verzeichnis.

<code>&lt;connector&gt;</code> ist genau einer von <code>apache</code>,
<code>nginx</code>, <code>haproxy</code>, <code>envoy</code>,
<code>traefik</code> oder <code>lighttpd</code>. Er benennt den Connector,
dessen ausgewählte Host-Route die Artefakte erzeugte.

<code>&lt;run-id&gt;</code> ist ein 1–128 Zeichen langes
dateisystemsicheres Token, das mit ASCII-Buchstabe oder -Ziffer beginnt und
sonst nur Buchstaben, Ziffern, <code>.</code>, <code>_</code> und
<code>-</code> verwendet. Beispiel: <code>six-core-20260712T120000Z</code>.
Es darf weder Secrets, persönliche Daten, Schrägstriche noch
Traversal-Segmente enthalten.

Die Root-Variable <code>EVIDENCE_ROOT</code> verwendet standardmäßig
<code>VERIFIED_EVIDENCE_ROOT/no-crs-evidence</code>. Nach dem Ableiten ist der
Eltern-Root ein absoluter Evidence-Pfad. Vollständige Anforderungen an Format,
Setter, Scope und Sicherheit stehen unter
[Konfigurationsvariablen](../configuration/variables.de.md#no-crs-und-evidence-variablen).

## Kanonisches Artefaktlayout

Validator und Framework-Schemas sind maßgeblich. Ein finalisierter
kanonischer Lauf enthält normalerweise die folgenden Artefaktrollen; ein
Artefakt kann fehlen, wenn das ausgewählte Profil die entsprechende
unterstützte Beobachtung nicht erzeugt. In diesem Fall müssen Manifest/Status
dies sagen, statt Daten zu erfinden.

| Relativer Pfad | Rolle | Datensensitivität / Interpretation |
|---|---|---|
| <code>result.json</code> | Aggregate-Result und Run-Identität | Als Summary lesen, nicht als Nachweis nicht aufgeführter Cases |
| <code>results.jsonl</code> | Ein kanonisches Case-Result pro JSONL-Zeile | Enthält Outcome-Metadaten; darf keine Request-/Response-Body-Payloads enthalten |
| <code>events.jsonl</code> | Kanonische Event-Records | Nur Metadaten-Event-Evidence; Secrets und Body-Payloads vermeiden/redacten |
| <code>plan.json</code> | Capability-ausgewählter Case-Plan | Erklärt ausgewählte/ausgelassene Cases; Auswahl allein ist keine Ausführung |
| <code>manifest.json</code> | Artefaktinventar und Identität | Verknüpft erzeugte/fehlende Artefakte mit dem Lauf |
| <code>inventory/run.json</code> | Run-Inventar/Provenance | Identifiziert die ausgewählten Run-Eingaben |
| <code>inventory/first-byte-evidence.json</code> | First-Byte-Beobachtungs-Eingabe | Erforderlich, wenn ein anwendbarer First-Byte-Case promotet wird |
| <code>inventory/barrier-events.jsonl</code> | Synchronisierte Barrier-Event-Records | Erforderlich für Checks mit kausaler First-Byte-/EOS-Reihenfolge |
| <code>effective-config/manifest.json</code> | Effektives Konfigurationsinventar | Zeichnet die tatsächlich verwendete Konfiguration auf; auf sensitive Werte prüfen |

Roh-Host-Logs, Build-Bäume und temporäre Dateien sind nicht automatisch
kanonische Evidence, nur weil sie unter einem Runtime-Root existieren. Der
Lifecycle-Wrapper sanitisiert/normalisiert Daten vor der Finalisierung; halten
Sie Rohdaten außerhalb des versionierten Checkouts und kopieren Sie keine
Secrets in kanonische Dateien.

## Evidence-Targets

| Target | Zweck | Erforderliche Eingabe | Ergebnis und Grenze |
|---|---|---|---|
| <code>make no-crs-baseline-<connector></code> | Erzeugt Candidate-Baseline-Evidence für einen ausgewählten Connector | Rules, sichere Runtime-Pfade, Capabilities des ausgewählten Profils | Candidate-Artefakte; keine CRS- oder All-Protocol-Evidence |
| <code>make full-lifecycle-<connector></code> | Erzeugt Candidate-Artefakte für eine ausgewählte Full-Lifecycle-Route | Target-eigene Profil-Identität und normale No-CRS-Eingaben | Candidate-Full-Lifecycle-Run; Target-Name kann keine andere Route umbenennen |
| <code>make full-lifecycle-all-connectors</code> | Führt alle sechs ausgewählten Routen aus | Component-Voraussetzungen; <code>NO_CRS_RUN_ID</code> empfohlen | Candidate-Run pro Connector; keine breite Zusicherung |
| <code>make evidence-check-<connector></code> | Validiert vorhandene Evidence eines Connectors | <code>EVIDENCE_ROOT</code>, Run-ID oder Latest-Marker | Read-only-Validierung; führt keinen Host erneut aus |
| <code>make evidence-check-all-connectors</code> | Validiert vorhandene Evidence über die konfigurierte Connector-Menge | Dasselbe plus <code>NO_CRS_CONNECTORS</code> | Nur Aggregate-Validierung |
| <code>make check-first-byte-before-response-end</code> | Prüft First-Byte-before-EOS-Evidence | Explizite <code>NO_CRS_RUN_ID</code> und Full-Lifecycle-Artefakte | Benötigt synchronisierte kausale Artefakte |
| <code>make check-no-full-response-buffering</code> | Prüft No-Full-Response-Buffering-Bedingung | Explizite Run-ID und Full-Lifecycle-Artefakte | Leitet die Eigenschaft nicht aus einem Konfigurationswert ab |
| <code>make check-full-lifecycle-event-privacy</code> | Prüft Event-Privacy-Constraints | Explizite Run-ID und kanonische Events | Bestätigt Checker-Bedingungen, nicht allgemeine Host-Sicherheit |
| <code>make check-full-lifecycle-promotion</code> | Wendet Promotion-bezogene Evidence-Checks an | Explizite Run-ID und ausgewählte Artefakte | Upgraded keine nicht ausgeführten/nicht unterstützten Capabilities |
| <code>make check-six-connector-core-completion</code> | Read-only-Six-Connector-Completion-Gate | Explizite Run-ID und finalisierte kanonische Evidence | Erfolgreicher Prozess-Exit ist auf den Vertrag dieses Gates begrenzt |

Der Platzhalter <code>&lt;connector&gt;</code> besitzt die oben genannten sechs
Werte. Beispiel:

~~~sh
NO_CRS_RUN_ID="six-core-20260712T120000Z" make evidence-check-nginx
~~~

Dies validiert das NGINX-Evidence-Verzeichnis für diese Run-ID oder meldet eine
fehlende/ungültige Eingabe. Es führt NGINX nicht erneut aus und ändert sein
Capability-Manifest nicht.

## Promotion und Grenzen

Promotion ist eine Evidence-gesteuerte Schlussfolgerung, keine Dateikopie. Sie
bindet ausgewählten Integrationsmodus, Case-ID, gegebenenfalls Rule-ID,
Result-Status, Event-Metadaten und erforderliche kausale/Transport-Artefakte an
denselben Lauf.

| Beobachtung | Benötigte Evidence | Nicht ausreichend |
|---|---|---|
| P1/P2/P3/P4-Case-Result | Passender kanonischer Result-Record und erforderliche Event-Felder | Regeldatei, Source-Code oder Host-Build |
| Safe Late Intervention | Angeforderte/tatsächliche Aktion, Commit-/Status-Metadaten und passendes Event/Result | Das Wort <code>safe</code> in einer Konfiguration |
| Strict Late Abort | Host-sichtbare, kausale Artefakte der ausgewählten Strict-Route | Strict-Policy-Name, gRPC-Fehler oder Source-Branch |
| First Byte Before EOS | Synchronisierte First-Byte-, Barrier- und Transport-Evidence | Abgeschlossene HTTP-Response oder Timestamp ohne kausale Ordnung |
| No Full Response Buffering | Erforderliche Source-/Runtime-Evidence und Checker-Bedingungen | Body-Limit-Direktive oder Fehlen einer offensichtlichen Buffer-Datei |
| Event Privacy | Kanonische Event-Records ohne Body-Payloads/Secrets plus Privacy-Check | Annahme, dass Logs sicher sind, weil sie JSONL sind |

Die No-CRS-Rule-IDs im Bereich <code>1100000</code> sind
repository-eigene Baseline-IDs, keine OWASP-CRS-IDs. Details zu Rules/Cases und
Status stehen unter
[Konfigurationsvariablen](../configuration/variables.de.md#rule-ids-und-repräsentative-case-ids)
und [Testing](../testing/README.de.md).

## Status und Validierung

<code>PASS</code> bedeutet, dass ein konkreter artefaktgestützter Case/Check
seine erklärten Bedingungen erfüllte. <code>FAIL</code> bedeutet, dass er dies
nicht tat. <code>BLOCKED</code> bedeutet fehlende Voraussetzung;
<code>NOT EXECUTED</code> bedeutet keine Run-Schlussfolgerung;
<code>NOT APPLICABLE</code> und <code>UNSUPPORTED</code> bewahren
Host-Modell-Grenzen. Prozess-Exit <code>0</code> bedeutet nicht, dass jeder
Katalog-Case bestand; <code>1</code>, <code>2</code> und <code>77</code>
behalten die unter [Testing](../testing/README.de.md#statuswerte-und-exit-codes)
dokumentierten Bedeutungen.

## Privacy und Aufbewahrung

Legen Sie weder Request-Bodies, Response-Bodies, Authorization-Headers,
Cookies, Token, Passwörter, Private Keys, Zertifikate noch persönliche Daten
in kanonische Evidence. Verwenden Sie synthetische Baseline-Marker. Halten Sie
Roh-Host-Ausgabe unter einem externen temporären/Runtimeroot mit restriktiven
Berechtigungen, prüfen Sie die effektive Konfiguration vor Weitergabe und
bewahren Sie nur vom Evidence-Contract benötigte Artefakte auf.

Generated-Report-Dateien sind Verbraucher dieser Evidence. Aktualisieren Sie
ihren Generator und regenerieren Sie sie; generiertes Markdown oder JSON darf
nicht manuell umgeschrieben werden.

## Nächste Lektüre

- [Testing-Dokumentation](../testing/README.de.md)
- [Connector-Dokumentation](../connectors/README.de.md)
- [Konfigurationsvariablen](../configuration/variables.de.md)
- [Glossar](../reference/glossary.de.md)
