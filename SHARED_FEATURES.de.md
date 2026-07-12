# Gemeinsame Funktionen

**Sprache:** [English](SHARED_FEATURES.md) | Deutsch

Dieses Dokument erweitert den Abschnitt `Connector Feature Status` der Root-README. Es
beschreibt das Verhalten gemeinsam genutzter Connectors nur, wenn dieses Verhalten im sichtbar ist
README, vorhandene Dokumentation, Tests, Skripte, Makefiles oder Quelldateien.
Wo das Repository nur allgemeinen ModSecurity-Connector-Hintergrund bereitstellt oder
umweltspezifische Anleitung, die deutlich gekennzeichnet ist.

## Bestätigtes Repository-Verhalten

Das Repository ist ein Connector-Monorepo für libmodsecurity v3-basierte Server
Anschlüsse. Apache und NGINX teilen konnektorneutrale Metadaten in `common/`, aber
Das Laufzeitverhalten des Servers bleibt in den Connector-Bäumen im Besitz des Adapters erhalten.

Bestätigt aus der Root-README-Datei:

- `common/include/msconnector/` definiert gemeinsame Direktive, Option/Standard,
  Rule-Load-Stat, Anfrage, Antwort, Transaktion, Intervention, Fähigkeit,
  Ursprungs-, Protokollierungs- und Statusdatenformen.
- `common/src/` enthält kleine connector-neutrale Hilfsimplementierungen.
- `connectors/apache/` enthält den Apache-Connector-Adapter Autotools/APXS
  Erstellen Sie Eingaben, nutzen Sie Dateien, Metadaten und produktive Quellen unter
  `connectors/apache/src/`.
- `connectors/nginx/` enthält den NGINX-Anschlussadapter, Modul `config`,
  Nutzen Sie Dateien, Metadaten und produktive Quellen unter `connectors/nginx/src/`.
- Die Connector-Quelle ist repo-lokal. Apache- und NGINX-Connector-Repositorys sind vorhanden
  nicht als Laufzeitstandard abgerufen.
- Laufzeit- und Abdeckungsnachweise dürfen nicht aus generierten Metadaten abgeleitet werden
  allein.
- XFAIL-, ausstehende, zukünftige, Connector-Gap- und Laufzeitdifferenz-Fälle bleiben bestehen
  Evidence-Klassen, bis sie durch einen dokumentierten Laufzeitbeweis ausdrücklich gefördert werden.
- `RESPONSE_BODY` bleibt nicht verifiziert und wird nicht beworben.

## Gemeinsame Architektur

Die gemeinsame Architektur ist metadatenorientiert und konnektorneutral. `common/`
besitzt keine Apache- oder NGINX-Laufzeit-APIs. Es stellt Datenformen und Hilfsfunktionen bereit
Funktionen, die von Adapter-eigenem Code und von Framework-Berichten genutzt werden können
ohne Server-SDKs in die gemeinsame Ebene zu ziehen.

Bestätigte gemeinsame Pfade:

| Pfad | Bestätigte Rolle |
| --- | --- |
| `common/include/msconnector/directives.h` | Gemeinsam genutzte Konstanten für Direktivennamen |
| `common/include/msconnector/options.h` | Gemeinsame Option/Standardmetadaten |
| `common/include/msconnector/rule_load_stats.h` | Gemeinsam genutzte Rule-Load-Stat-Datenform |
| `common/include/msconnector/request.h` | Connector-neutrale Wunschform |
| `common/include/msconnector/response.h` | Connector-neutrale Antwortform |
| `common/include/msconnector/transaction.h` | Connector-neutrale Phasen- und Transaktionsansicht |
| `common/include/msconnector/intervention.h` | Connector-neutrale Eingriffsform |
| `common/include/msconnector/status.h` | Connector-neutrale Statuswerte |
| `common/include/msconnector/capabilities.h` | Flags für connector-neutrale Fähigkeiten |
| `common/include/msconnector/origin.h` | Connector-neutrale Ursprungs-/Herkunftsform |
| `common/include/msconnector/logging.h` | Connector-neutrale Protokollierungsform |
| `common/src/` | Kleine Hilfsimplementierungen für konnektorneutrale Metadaten |

Bestätigte Nichtgrenzen von `docs/architecture/common-runtime-boundaries.md`:

- Common besitzt keine Apache-Hook-Registrierung oder Bucket-Brigaden.
- Common besitzt keine NGINX-Modulregistrierung, Phasenhandler oder Filter.
- Common ist nicht für die Handhabung des Anforderungs- oder Antworttexts zuständig.
- Common ist nicht Eigentümer des libmodsecurity-Objekts oder der Transaktionslebensdauer.
- Common besitzt kein `RESPONSE_BODY`-Verhalten.

Jede zukünftige Extraktion, die diese Laufzeitbereiche berührt, erfordert eine separate Extraktion
Design, Beweise und reale Connector-Smokes.

## Framework- und Validierungsintegration

Das Framework-Modul befindet sich unter:

```text
modules/ModSecurity-test-Framework
```

Die Root-README-Datei definiert das Setup- und Override-Muster:

```sh
git submodule update --init --recursive

FRAMEWORK_ROOT=/path/to/ModSecurity-test-Framework make quick-check
FRAMEWORK_ROOT=/path/to/ModSecurity-test-Framework make runtime-matrix-all
```

Das Framework verfügt über YAML-Fälle, Runner, Normalisierer, Laufzeitmatrixlogik,
Coverage-Generierung, v3-API-Smoke-Helfer und wiederverwendbare Testdokumentation.
Konnektorspezifisch generierte Beweise werden geschrieben unter:

```text
reports/testing/
TEST-COVERAGE-SUMMARY.md
```

Die in der README-Datei aufgeführten öffentlichen Connector-Ziele sind:

```sh
make setup-dev
make lint
make quick-check
make generate-test-matrix
make check-test-matrix
make runtime-matrix-all
make smoke-apache
make smoke-nginx
make smoke-all
```

Die Beweisregel der README-Datei ist wichtig: `make smoke-all` ist nur maßgeblich
wann es tatsächlich erfolgreich ausgeführt wird. Die generierte Berichterstattung ist keine Berichterstattung
Laufzeitbeweis für sich.

Aktuelle Bezugspunkte:

| Thema | Referenz |
| --- | --- |
| YAML-Schemaform | `modules/ModSecurity-test-Framework/docs/imports/common/schema.md` |
| Geteilte Geräte | `modules/ModSecurity-test-Framework/docs/imports/common/fixtures.md` |
| Smoke-Zielsemantik | `modules/ModSecurity-test-Framework/docs/testing/fast-checks.md` |
| Fähigkeitsmodell | `docs/architecture/capability-model.md` |
| Statusmodell | `docs/architecture/status-model.md` |
| Herkunft/Herkunft und Lizenzen | `docs/licensing/license-and-origin.md` |
| Realer Verbindungspfad | `reports/testing/real-world-connector-validation.md` |
| Fallmatrix | `reports/testing/case-matrix.md` und `reports/testing/generated/case-matrix.generated.md` |
| PR/Quellennachweis | `reports/testing/evidence/pr-evidence-summary.md` |

## Gemeinsam genutzte Build-Variablen

Die README-Datei dokumentiert das Muster für gemeinsam genutzte Quell-Build-Variablen:

```sh
BUILD_ROOT=$HOME/.local/state/ModSecurity-conector-build
SOURCE_ROOT=$BUILD_ROOT/sources
MODSECURITY_GIT_REF=v3/master
MODSECURITY_SOURCE_DIR=$SOURCE_ROOT/ModSecurity_V3
```

Diese Variablen gelten sowohl für die vom Apache- als auch vom NGINX-Framework unterstützten Buildpfade:

| Variable | Gemeinsame Bedeutung |
| --- | --- |
| `BUILD_ROOT` | Lokaler Build-/Ausgabespeicherort, kein Cache-Vertrag |
| `SOURCE_ROOT` | Quell-Checkout-Bereich, der von Hilfsskripten verwendet wird |
| `MODSECURITY_GIT_REF` | libmodsecurity v3 git ref |
| `MODSECURITY_SOURCE_DIR` | libmodsecurity v3-Quellverzeichnis |
| `FRAMEWORK_ROOT` | Optionale Test-Framework-Überschreibung |

Apache und NGINX fügen jedoch Connector-spezifische Variablen in ihre Hilfsskripte ein
Die Konvention auf README-Ebene besagt, dass die generierte Build- und Laufzeitausgabe erhalten bleibt
unter `BUILD_ROOT`.

## Unterstützung für gemeinsame Anweisungen

Die gemeinsame Funktionstabelle der Stamm-README-Datei beschreibt den aktuellen Implementierungsstatus
nur. Die allgemeinen Metadaten der Direktive stammen von
`common/include/msconnector/directives.h`, während serverspezifische Anweisung
Die Registrierung bleibt Eigentum des Adapters.

Bestätigte gemeinsame Anweisungen:

| Funktion | Apache | NGINX | Notizen |
| --- | --- | --- | --- |
| `modsecurity on|off` | Unterstützt | Unterstützt | Name der gemeinsam genutzten Direktive; Die serverspezifische Registrierung bleibt Eigentum des Adapters. |
| Inline-Regeln | Unterstützt | Unterstützt | `modsecurity_rules`; Das Laden von Regeln und Fehlerpfade bleiben Connector-spezifisch. |
| Regeldatei | Unterstützt | Unterstützt | `modsecurity_rules_file`; Erfolgreiche Ladevorgänge zählen zu den Regellademetadaten. |
| Remote-Regeln | Unterstützt | Unterstützt | `modsecurity_rules_remote`; Das Remote-Laden bleibt konnektorspezifisch. |
| Richtlinie zur Weiterleitung von Fehlerprotokollen | Unterstützt | Unterstützt | `modsecurity_use_error_log on|off`; Die Standardeinstellung ist aktiviert. Audit-Protokolle, Interventionen und die Bearbeitung von Anfragen/Antworten bleiben unverändert. |
| Regelladestatistik-Metadaten | Unterstützt | Unterstützt | Gemeinsame Datenform in `common/include/msconnector/rule_load_stats.h`; Nur Metadaten. |
| Allgemeine Direktiven-Metadaten | Verwendet | Verwendet | Gemeinsam genutzte Direktivennamenkonstanten werden von beiden Connectoren verwendet. |
| Allgemeine Optionsmetadaten | Teilweise | Teilweise | Apache verwendet allgemeine Bool-/Standardmetadaten für die Fehlerprotokollrichtlinie. NGINX verwendet allgemeine Standardeinstellungen für die Aktivierung, Fehlerprotokollweiterleitung und den Phase-4-Modus. |

## Verhalten der Transaktions-ID

Das Verhalten der Transaktions-ID wird als Funktionsbereich gemeinsam genutzt, ist jedoch nicht identisch
Syntax.

Bestätigtes aktuelles Verhalten:

- Apache unterstützt `modsecurity_transaction_id <string>`.
- Apache unterstützt `modsecurity_transaction_id_expr <apache-expression>`.
– NGINX unterstützt `modsecurity_transaction_id` als komplexen NGINX-Wert.

Apache-Semantik aus der README-Datei und `docs/connectors/directive-parity.md`:

- `modsecurity_transaction_id` behält die Semantik statischer Zeichenfolgen bei.
- `modsecurity_transaction_id_expr` ist ein Opt-In-Apache-String-Ausdruck.
– Die bestätigte Ausdruckssyntax umfasst `%{REQUEST_URI}`.
– Statische und Ausdrucks-Transaktions-IDs schließen sich gegenseitig aus
  Apache-Kontext.
– Während der Konfigurationszusammenführung gelten die normalen Überschreibungen des untergeordneten Kontexts.
– Wenn keine der Anweisungen festgelegt ist oder der Ausdruck einen leeren Wert ergibt
  oder fehlschlägt, behält Apache den vorhandenen `UNIQUE_ID`-Fallback bei und erstellt dann einen
  Transaktion ohne explizite ID, wenn kein verwendbarer `UNIQUE_ID`-Wert vorhanden ist
  verfügbar.

NGINX-Semantik:

– `modsecurity_transaction_id` verwendet einen komplexen NGINX-Wert.
- Werte können auf Anfrage von NGINX ausgewertet werden.

Dies ist ein bestätigter Unterschied zwischen Connectoren.

## Rule-Load-Statistik-Metadaten

`common/include/msconnector/rule_load_stats.h` definiert die gemeinsame Datenform:

```c
typedef struct msconnector_rule_load_stats {
    unsigned inline_rules;
    unsigned file_rules;
    unsigned remote_rules;
} msconnector_rule_load_stats;
```

Bestätigte Semantik von `docs/connectors/rule-load-stats.md`:

- Werte zählen geladene Regeln, keine Direktivenaufrufe.
- `file_rules` zählt Regeln, die aus Regeldateien geladen wurden; es zählt nicht
  Anzahl der Dateien.
- Statistiken werden nur nach erfolgreichen `msc_rules_add*`-Aufrufen erhöht.
- Fehlgeschlagene Ladeversuche behalten den bestehenden Fehlerpfad bei und erhöhen den nicht
  Zähler.
- Kein Konnektor verwendet diese Statistiken, um zu entscheiden, ob eine Anfrage gestellt werden soll
  verarbeitet, gesperrt, protokolliert oder eingesehen werden.
– NGINX macht die Werte über sein vorhandenes Startprotokoll verfügbar.
– Apache speichert die Werte derzeit nur als interne Konfigurationsmetadaten.

Regelladestatistiken sind Metadaten. Sie ändern nicht das Laden von Regeln, das Zusammenführen von Regeln,
Anfragebearbeitung, Antwortbearbeitung oder jede Laufzeitentscheidung.

## Anfrage- und Antwortverarbeitung

Allgemeiner Hintergrund zum ModSecurity-Connector: Normalerweise wird ein Server-Connector zugeordnet
Verbindungsmetadaten, URI, Header, Anforderungstext, Antwortheader, Antwort
Hauptteil, Protokollierung und Eingriffe in libmodsecurity-Transaktionsaufrufe.

Bestätigte Repository-Grenze: Apache- und NGINX-Laufzeitverarbeitung ist
Adapterbesitz. Common ist nicht Eigentümer dieser Pfade.

Apache besitzt:

- Hakenregistrierung
- Eingabe- und Ausgabefilter
- Verhalten der Eimerbrigade
- Analyse der Apache-Konfiguration
- Abschluss der Intervention
- Lebensdauer der libmodsecurity-Transaktion

NGINX besitzt:

- Modulanmeldung
- Zugriffs-, Header-, Text- und Protokollfilter
- Phasenhandler
- Spätinterventionsverhalten der Phase 4
- Lebensdauer der libmodsecurity-Transaktion

Das Vorhandensein einer konnektorneutralen Anfrage, Antwort, Transaktion usw
Interventionsdatenformen in `common/include/msconnector/` bedeuten das nicht
Die produktive Apache- und NGINX-Laufzeit wurde in eine gemeinsame umgestaltet
Motorschicht.

## Protokollierung und Audit-Protokollierung

Bestätigte gemeinsame Richtlinie:- `modsecurity_use_error_log on|off` existiert sowohl für Apache als auch für NGINX.
- Die Standardeinstellung ist aktiviert.
– `off` unterdrückt die Weiterleitung von Serverfehlerprotokollen aus dem libmodsecurity-Protokoll
  Nur Rückruf.
- Audit-Protokolle, Interventionen, Hooks, Filter, Buckets, Transaktionseigentum,
  und Anfrage-/Antwortbehandlung bleiben unverändert.

Allgemeiner ModSecurity-Hintergrund: Die Audit-Protokollierung wird hauptsächlich von gesteuert
libmodsecurity-Konfiguration und -Regeln, zum Beispiel `SecAuditEngine` und
`SecAuditLog`. Dieses Repository dokumentiert kein separates gemeinsames Audit-Protokoll
Laufzeitschicht. Das Verhalten des Audit-Protokolls sollte durch reale
Connector-Smokes und generierte Evidence validiert werden, nicht allein aus
Metadaten abgeleitet werden.

## NGINX-spezifische Phase-4-Kontrollen

Der NGINX-Connector unterstützt derzeit:

- `modsecurity_phase4_mode minimal|safe|strict`
- `modsecurity_phase4_content_types_file <path>`
- `modsecurity_phase4_log <path>`

Dabei handelt es sich um NGINX-spezifische Laufzeitsteuerungen. Sie sind kein üblicher Connector
Vertrag und werden nicht von Apache implementiert.

In der README-Datei werden Apache-Phase-4-Anweisungen ausdrücklich als zurückgestellt aufgeführt:

- `modsecurity_phase4_mode`
- `modsecurity_phase4_content_types_file`
- `modsecurity_phase4_log`

Das Verhalten des Reaktionskörpers wird weiterhin nicht gefördert. `RESPONSE_BODY` bleibt bestehen
nicht verifiziert und nicht beworben.

## Funktionsmatrix

Diese Matrix zeichnet das bestätigte Repository-Verhalten und die aktuelle README-Datei auf
Nur implementierter Zustand.

| Funktion | NGINX | Apache | Notizen |
| --- | --- | --- | --- |
| `modsecurity on|off` | Ja | Ja | Name der gemeinsam genutzten Direktive; Die Laufzeitregistrierung ist Adaptereigentum. |
| Inline-Regeln | Ja | Ja | `modsecurity_rules`; Das Ladeverhalten bleibt im Besitz des Connectors. |
| Laden der Regeldatei | Ja | Ja | `modsecurity_rules_file`; Erfolgreiche Ladevorgänge zählen zu den Metadaten. |
| Remote-Regeln werden geladen | Ja | Ja | `modsecurity_rules_remote`; Das Remote-Laden bleibt Eigentum des Connectors. |
| Statische Transaktions-ID | Nein | Ja | Apache `modsecurity_transaction_id <string>`. NGINX verwendet stattdessen komplexe Werte. |
| Ausdruck/komplexe Transaktions-ID | Ja | Ja | NGINX verwendet `modsecurity_transaction_id`; Apache verwendet `modsecurity_transaction_id_expr`. Die Syntax ist serverspezifisch. |
| Richtlinie zur Weiterleitung von Fehlerprotokollen | Ja | Ja | `modsecurity_use_error_log on|off`; hat keinen Einfluss auf Überwachungsprotokolle oder Interventionen. |
| Regelladestatistik-Metadaten | Ja | Ja | Gemeinsame Datenform. NGINX meldet beim Start; Apache speichert intern. |
| Header-Verarbeitung anfordern | Adapterbesitz | Adapterbesitz | In Connector-Laufzeitpfaden vorhanden, nicht im Besitz von `common/`. |
| Verarbeitung des Anforderungstexts | Adapterbesitz | Adapterbesitz | In Connector-Laufzeitpfaden vorhanden, nicht im Besitz von `common/`. |
| Antwort-Header-Verarbeitung | Adapterbesitz | Adapterbesitz | In Connector-Laufzeitpfaden vorhanden, nicht im Besitz von `common/`. |
| Verarbeitung des Antworttextes | Nicht gefördert | Nicht gefördert | `RESPONSE_BODY` bleibt nicht verifiziert und wird nicht beworben. |
| Audit-Protokollierung | libmodsecurity/rules-driven | libmodsecurity/rules-driven | Es ist keine gemeinsame Laufzeitebene für Überwachungsprotokolle dokumentiert. |
| NGINX Phase-4-Steuerungen | Ja | Nein | NGINX-spezifische Laufzeitsteuerungen; Die Apache-Parität wird zurückgestellt. |

## Bekannte Unterschiede und zurückgestellte Bereiche

Bestätigt aus der README-Datei:

| Bereich | Aktueller Stand |
| --- | --- |
| Transaktions-ID-Zuordnung | Apache unterstützt statische Zeichenfolgen sowie Opt-in-Apache-Zeichenfolgenausdrücke über `modsecurity_transaction_id_expr`; NGINX unterstützt komplexe Werte durch `modsecurity_transaction_id`. |
| Apache Phase-4-Anweisungen | `modsecurity_phase4_mode`, `modsecurity_phase4_content_types_file` und `modsecurity_phase4_log` sind für Apache nicht implementiert. |
| Verhalten des Apache-Antworttexts | Nicht gefördert; `RESPONSE_BODY` bleibt nicht verifiziert und wird nicht beworben. |
| Apache-Bucket-/Filter-/Interventionspfade | In dieser Arbeit mit allgemeinen Metadaten absichtlich nicht umgestaltet. |
| Gemeinsame Schicht | Enthält nur konnektorneutrale Metadaten und Datenformen; Es besitzt keine Apache- oder NGINX-Laufzeit-APIs. |
| Berichterstattung über Regelladestatistiken | NGINX meldet über sein bestehendes Startprotokoll; Apache speichert Statistiken als interne Metadaten, bis die Anzeigeaggregation und die Zusammenführungssemantik explizit entworfen werden. |

## Fehlerbehebung bei gemeinsamen Funktionen

### Geteilte Fälle werden nicht ausgeführt

Initialisieren oder überschreiben Sie das Framework-Modul:

```sh
git submodule update --init --recursive
FRAMEWORK_ROOT=/path/to/ModSecurity-test-Framework make quick-check
```

Führen Sie dann connector-spezifische Smoke-Ziele aus:

```sh
make smoke-apache
make smoke-nginx
```

### Die generierten Beweise sehen veraltet aus

Generieren und überprüfen Sie die Matrixdateien mithilfe der in der README-Datei aufgeführten Ziele neu:

```sh
make generate-test-matrix
make check-test-matrix
```

Denken Sie daran, dass generierte Metadaten an sich kein Laufzeitbeweis sind.

### Regeln scheinen nicht zu laden

Überprüfen Sie bei Repository-Smoke die Protokolle unter `BUILD_ROOT`, insbesondere den Connector
Protokolle unten:

```text
$BUILD_ROOT/logs/apache/
$BUILD_ROOT/logs/nginx/
```

Regelladestatistiken sind Metadaten. NGINX meldet sie in Startprotokollen; Apache-Stores
sie intern. Fehlgeschlagene Regelladevorgänge sollten konnektorspezifisch erfolgen
Konfigurationsfehlerpfade.

### Apache und NGINX verhalten sich unterschiedlich

Prüfen Sie zunächst, ob das Verhalten als bekannter Unterschied dokumentiert ist:

- Die Syntax der Transaktions-ID ist unterschiedlich
- Apache hat `modsecurity_transaction_id_expr`
- NGINX verfügt über NGINX-spezifische Phase-4-Anweisungen
- `RESPONSE_BODY` ist nicht verifiziert und nicht beworben
- Hooks, Filter, Körperhandhabung, Interventionsabschluss und Transaktion
  Lebensdauer sind Eigentum des Adapters

Validieren Sie dann mit den Framework-gestützten Smoke-Zielen, anstatt sie zu vergleichen
allein generierte Metadaten.

## Weiterführende Literatur

- [Kompilieren Sie Nginx](./docs/build/compilers/nginx.de.md)
- [Apache](./docs/build/compilers/apache.de.md) kompilieren
- `README.md`
- `docs/architecture/architecture.md`
- `docs/architecture/common-runtime-boundaries.md`
- `docs/connectors/directive-parity.md`
- `docs/connectors/rule-load-stats.md`
- `connectors/nginx/README.md`
- `connectors/apache/README.md`
- `connectors/nginx/harness/README.md`
- `connectors/apache/harness/README.md`
