# Testing-Dokumentation

**Sprache:** [English](README.md) | Deutsch

Testing unterscheidet Source-/Contract-Checks, Build-/Config-Checks,
fokussierte Runtime-Smokes und Evidence-Validierung. Das Bestehen einer Schicht
impliziert nicht, dass eine andere Schicht bestanden hat. Die aktuelle
Dokumentation deckt nur ausgewählte HTTP/1.1-Kernrouten ab; sie erhebt keinen
Production-, CRS-, HTTP/2-, HTTP/3-, vollständige-Matrix- oder
Strict-für-alle-Connectoren-Claim.

## Testschichten

| Schicht | Typisches Target | Was es prüft | Was es nicht feststellt |
|---|---|---|---|
| Struktur/Dokumentation | <code>make check-bilingual-docs</code>, <code>make lint</code> | Begleitdateien, Links, Source-Contracts, Syntax und konfigurierte Checks | Live-Connector-Traffic oder kanonische Runtime-Evidence |
| Build | <code>make build-<connector></code> | Eine ausgewählte Connector-Build-Stage | Config-Load, Runtime-Traffic oder Case-Ergebnis |
| Konfiguration | <code>make check-config-<connector></code> | Ausgewählte Konfiguration kann geladen/geprüft werden | Request-/Response-Verhalten |
| Fokussierte Runtime | <code>make runtime-smoke-<connector></code> | Einen schmalen Host-Smoke, wo vorhanden | Alle Cases, alle Transporte oder Full-Lifecycle-Promotion |
| No-CRS-Baseline | <code>make no-crs-baseline-<connector></code> | Capability-ausgewählte repository-eigene Baseline-Cases | CRS-Verhalten oder nicht unterstützte Capabilities |
| Full Lifecycle | <code>make full-lifecycle-<connector></code> | Ausgewähltes Profil plus Lifecycle-Artefakterzeugung | Production Readiness, alle Protocols oder Strict-Verhalten jedes Connectors |
| Evidence-Validierung | <code>make evidence-check-<connector></code> | Vorhandene kanonische Run-Artefakte | Erneuten Host-Lauf oder PASS für fehlende Daten |

Der Platzhalter <code>&lt;connector&gt;</code> akzeptiert nur
<code>apache</code>, <code>nginx</code>, <code>haproxy</code>,
<code>envoy</code>, <code>traefik</code> und <code>lighttpd</code>.
<code>make check-config-nginx</code> prüft zum Beispiel die ausgewählte
NGINX-Konfiguration; der String <code>&lt;connector&gt;</code> wird nicht
literal akzeptiert.

## Gemeinsame Kommandos

### Lokalen Dokumentations- und Contract-Check ausführen

~~~sh
make quick-check
~~~

Dies führt die lint-orientierten und diff-orientierten Checks des Repositorys
aus. Es benötigt Framework-Checkout und konfigurierte lokale Toolchain. Es
erzeugt Diagnostik und kann temporären Build-Cache-Inhalt erzeugen; es bereitet
oder prüft nicht jeden externen Host.

### Einen ausgewählten Full-Lifecycle-Lauf ausführen

~~~sh
NO_CRS_RUN_ID="six-core-20260712T120000Z" make full-lifecycle-all-connectors
~~~

<code>NO_CRS_RUN_ID</code> ist für spätere Aggregate-Evidence-Gates
erforderlich. Sie muss ein 1–128 Zeichen langes dateisystemsicheres
Identifikationsmerkmal sein: Sie beginnt mit ASCII-Buchstabe oder -Ziffer und
darf sonst nur Buchstaben, Ziffern, <code>.</code>, <code>_</code> und
<code>-</code> enthalten. Der Beispielwert identifiziert einen Lauf; er ist
kein Default und darf weder Benutzername, Secret, Tickettitel, Schrägstrich
noch <code>..</code> enthalten.

Das Target erzeugt Candidate-Artefakte für die ausgewählten Routen. Es erhebt
keine Aggregate-Zusicherung, nur weil das Kommando startete oder mit einem
technischen Exit-Code endete. Lesen Sie [Evidence](../evidence/README.de.md),
bevor Sie die Ausgabe interpretieren.

### Einen finalisierten Aggregate-Lauf validieren

~~~sh
NO_CRS_RUN_ID="six-core-20260712T120000Z" make check-six-connector-core-completion
~~~

Dies ist ein Read-only-Aggregate-Acceptance-Check. Er benötigt finalisierte
Evidence unter <code>EVIDENCE_ROOT</code>; der Root-Default ist
<code>VERIFIED_EVIDENCE_ROOT/no-crs-evidence</code>. Setzen Sie
<code>EVIDENCE_ROOT</code> nur auf einen absoluten Evidence-Pfad, der den zu
prüfenden Lauf enthält, zum Beispiel
<code>/srv/modsecurity-work/evidence/no-crs-evidence</code>. Zeigen Sie nicht
auf Checkout oder einen nicht zusammengehörigen Evidence-Baum.

## Statuswerte und Exit-Codes

| Wert | Bedeutung |
|---|---|
| <code>PASS</code> | Der konkrete Case/Check erfüllte seine aufgezeichneten Bedingungen. Dies generalisiert nicht auf nicht ausgewählte Connectoren, Profile, Cases oder Protocols. |
| <code>FAIL</code> | Der Case/Check erfüllte eine erforderliche Bedingung nicht. |
| <code>BLOCKED</code> | Eine Voraussetzung fehlte oder war unsicher. Dies ist kein PASS und soll die fehlende Bedingung benennen. |
| <code>NOT EXECUTED</code> | Der Case/Pfad wurde bewusst nicht ausgeführt; daraus folgt keine Verhaltensaussage. |
| <code>NOT APPLICABLE</code> | Der Case trifft auf ausgewähltes Profil/Host-Modell nicht zu. |
| <code>UNSUPPORTED</code> | Das ausgewählte Host-Modell kann die vom Case benötigte Capability nicht bereitstellen. |
| <code>NOT_EXECUTABLE</code> | Historische Harness-Schreibweise für einen in der Umgebung nicht ausführbaren Case. |
| <code>0</code> | Der Prozess erfüllte seinen eigenen technischen Vertrag. Dies bedeutet nicht, dass jeder Katalog-Case PASS ist. |
| <code>1</code> | Allgemeiner Runtime-, Config- oder Validierungsfehler. |
| <code>2</code> | Ungültige Invocation, Eingabe oder Validierungs-/Contract-Fehler. |
| <code>77</code> | Fehlende Voraussetzung oder optionale Umgebungsbedingung, zum Beispiel Framework-Pfad oder Host-Komponente. |

## Cases, Rules und IDs

Der repository-eigene No-CRS-Katalog liegt unter
<code>modules/ModSecurity-test-Framework/tests/cases/no-crs-baseline/catalog.json</code>.
Er wählt nur Cases aus, deren erforderliche Capabilities auf das ausgewählte
Host-Profil zutreffen. Die Regeldatei liegt unter
<code>modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf</code>.
Beide sind repository-relative Pfade vom Connector-Repository-Root.

| ID / Element | Kontext |
|---|---|
| <code>1100001</code> | P1-Request-Header-Deny-Rule |
| <code>1100101</code> | P2-Request-Body-Deny-Rule |
| <code>1100201</code> | P3-Response-Header-Deny-Rule |
| <code>1100301</code> | P4-Response-Body-Beobachtungs-/Late-Intervention-Rule |
| <code>allow_without_marker</code> | Basic-Allow-Case |
| <code>deny_header_marker_403</code> | P1-Deny-Case, gebunden an <code>1100001</code> |
| <code>deny_request_body_marker_403</code> | P2-Case, gebunden an <code>1100101</code> |
| <code>deny_response_header_marker_403</code> | P3-Case, gebunden an <code>1100201</code> |
| <code>phase4_rule_observed</code> | P4-Rule-Beobachtungs-Case; keine sichtbare Pre-Commit-403-Aussage |
| <code>phase4_first_byte_before_response_end</code> | Benötigt synchronisierte First-Byte-before-EOS-Artefakte |
| <code>phase4_no_full_response_buffering</code> | Benötigt Evidence, dass der Connector keinen vollständigen Response-Buffer hält |

Dies sind keine OWASP-CRS-Rule-IDs. Die vollständige Rule-/Case-Referenz mit
Late-Intervention-Cases und erwarteten Evidence-Feldern steht unter
[Konfigurationsvariablen](../configuration/variables.de.md#rule-ids-und-repräsentative-case-ids).

## Testauswahl-Variablen

| Variable | Zweck | Default / Format | Grenze |
|---|---|---|---|
| <code>NO_CRS_CONNECTORS</code> | Beschränkt ein Aggregate-Target auf eine Connector-Teilmenge | Default: alle sechs Namen; durch Leerzeichen getrennte gültige Connector-Namen | Ausgelassener Connector erhält keine Evidence |
| <code>NO_CRS_RULES_FILE</code> | Wählt Baseline-Regeln | Default: Framework-No-CRS-Regeln; absolute vorhandene Datei | Änderung der Regeln ändert Vergleichbarkeit |
| <code>SMOKE_CASES</code>, <code>TEST_CASE</code> | Grenzt eine direkte Harness-Diagnose ein | Optionale dokumentierte Case-ID/Liste | Ein schmaler Smoke ist kein Aggregate-Completion-Run |
| <code>CASE_SCOPE</code> | Wählt Framework-/Harness-Case-Scope | Harness-Default häufig <code>all</code> | Ändert weder Katalog noch Capability-Manifest |
| <code>FORCE_ALL_CASES</code>, <code>RUN_ONE_CASE</code> | Direkte Run-Selektor-Flags | Optionale Boolean-Werte | Nur zur Diagnose verwenden; tatsächliche Auswahl aufzeichnen |
| <code>NO_CRS_PROTOCOL_CLIENT</code> | Schaltet optionalen stage-eigenen Protocol-Probe ein | Default <code>0</code>; <code>1</code> zum Opt-in | Probe ist nicht-promotend und kein HTTP/2-/HTTP/3-Claim |

Setter, Scope, Auswirkung und Sicherheitsnotizen jeder Variablen stehen in der
[zentralen Variablenreferenz](../configuration/variables.de.md).

## Testdaten und Privacy

Results und Events sind Evidence-Eingaben, kein Ort für Request-Bodies,
Authorization-Headers, Cookies, Token, Private Keys oder Passwörter. Verwenden
Sie synthetische Marker aus der eingecheckten No-CRS-Baseline. Wenn ein lokaler
Test ein Secret zum Erreichen eines privaten Hosts benötigt, laden Sie es aus
einem sicheren Store und committen, echoen oder übernehmen Sie es nicht in
kanonische Artefakte.

## Nächste Lektüre

- [Evidence-Dokumentation](../evidence/README.de.md)
- [Connector-Dokumentation](../connectors/README.de.md)
- [Build-Dokumentation](../build/README.de.md)
- [Glossar](../reference/glossary.de.md)
