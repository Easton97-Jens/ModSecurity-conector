# Change Record: Repository-Produktmonorepo-Konzept

**Sprache:** [English](CR-20260714-repository-concept.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Titel | Repository-Produktmonorepo-Konzept |
| Change-ID | CR-20260714-repository-concept |
| Datum (UTC) | 2026-07-14T08:14:32Z |
| Autor oder ausführender Agent | Codex agent /root |
| Basis-Revision | 0fec00442b0031c206b627a44735f1eb07534d51 |
| Zugehöriges Issue oder Pull Request | None |
| Finale Revision | not committed |

## Motivation und Problemstellung

Das Repository benötigte ein dauerhaftes zweisprachiges Zielkonzept, das das
Produktmonorepo vom unabhängigen Framework trennt, Connector- und
Common-Ownership reviewbar macht und verhindert, dass eingecheckte Reports als
neuer Runtime-Nachweis missverstanden werden. Vorhandene Architektur-,
Connector-, Common-, Framework-, Capability- und Evidence-Dokumentation
beschreibt wichtige Teile des Ist-Zustands, stellte aber keine verbindliche
Entscheidungsfläche für den Zielzustand bereit.

## Betroffene Komponenten und Sicherheitsgrenzen

Die versionierte Änderung betrifft ausschließlich Dokumentation. Sie betrifft
Repository-Navigation, Architekturhinweise, ein neues Zielkonzept,
ADR-Hinweise und diesen Traceability-Record. Sie dokumentiert die Grenze
zwischen Parent-owned Product Code, Connector-Adaptern, Common-Runtime-Code und
dem unabhängigen wiederverwendbaren Test-Framework. Sie verändert weder
Request-/Response-Verarbeitung, Security-Defaults, Host-Failure-Verhalten,
Runtime-Storage noch Connector-Binärdateien.

Die lokale ignorierte <code>AGENTS.md</code> wurde um eine kompakte
Repository-Concept-Disziplin ergänzt. Sie liegt absichtlich außerhalb des
versionierten Diffs und hat keinen deutschen Begleiter. Bereits vorhandene oder
gleichzeitig entstandene Arbeitsbaumänderungen außerhalb der unten aufgeführten
Dateien wurden bewahrt und sind nicht Teil dieses Change Records.

## Akzeptanzkriterien

| Kriterium | Status | Evidenz |
| --- | --- | --- |
| Ein zweisprachiges Zielkonzept beschreibt die Grenze von Parent, Connector, Common und Framework. | erfüllt | <code>docs/repository-concept.md</code> und <code>docs/repository-concept.de.md</code> |
| Anforderungen an das fertige Produkt, Lifecycle-Ownership, Konfigurationsgrenzen und Erweiterungsregeln sind explizit. | erfüllt | Konzeptabschnitte „Produktvertrag“, „Lifecycle“, „Konfiguration“ und „Erweiterungsregeln“ |
| Aktuelle Capability-/Report-Konflikte und Framework-Grenzabweichungen bleiben sichtbar, statt umgeschrieben zu werden. | erfüllt | Konzeptabschnitt „Dokumentierte Abweichungen und Follow-up-Grenzen“ |
| Claim-Labels unterscheiden verified, documented_not_runtime_verified, compatibility_only, unknown und out_of_scope. | erfüllt | Konzeptabschnitt „Claim-Labels“ |
| ADR-Prozess und fünf vorgeschlagene Entscheidungsthemen sind in beiden Sprachen verfügbar. | erfüllt | <code>docs/decisions/README.md</code> und <code>docs/decisions/README.de.md</code> |
| Diese Dokumentationsänderung verändert keine Product-Source, Tests, Generatoren, Workflows oder Framework-/Submodule-Dateien. | erfüllt | Inventar der geänderten Dateien und finaler Diff-Review |

## Untersuchte Alternativen

Die aktuelle Ist-Architekturdokumentation zur einzigen Zielzustandsautorität
umzuwidmen, wurde nicht gewählt, weil dies beobachtete Source-Ownership und
zukünftige verbindliche Entscheidungen vermischen würde. Stale Generated
Evidence oder Capability-Manifeste zu aktualisieren, wurde nicht gewählt, weil
diese Dokumentationsaufgabe keine neue Runtime-Evidence erhob und historische
Ausgaben nicht als aktuelle Beweise umetikettieren darf. Parent- oder
Framework-Code zu verschieben lag ebenfalls außerhalb des Umfangs; das Konzept
macht stattdessen den bestehenden Split und seine Abweichungen für spätere
Entscheidungen explizit.

## Implementierungsentscheidung und Begründung

Ein paarweise gepflegtes Zielkonzept wird unter <code>docs/</code> hinzugefügt,
aus Root- und Dokumentationsnavigation verlinkt und durch einen paarweisen
ADR-Einstieg ergänzt. Das Konzept etabliert eine Quellenhierarchie und
explizite Claim-Labels, bevor es die gewünschte Produktmonorepo-Grenze
beschreibt: Der Parent besitzt das Produkt und host-spezifische Seams, das
Framework besitzt wiederverwendbare Testlogik, und Common bleibt
transportneutraler Runtime-Code.

Das Design ordnet bestehende Evidence bewusst
<code>documented_not_runtime_verified</code> zu, wenn Rohartefakte hier nicht
erneut validiert wurden, und stale Generated Reports für aktuelle Promotion als
<code>unknown</code> ein. So bleibt Traceability erhalten, ohne einen
Production-, Availability-, vollständigen Coverage- oder Runtime-Security-Claim
aufzustellen.

## Geänderte Dateien

Versionierte Dokumentationsdateien:

- <code>README.md</code> und <code>README.de.md</code>
- <code>docs/README.md</code> und <code>docs/README.de.md</code>
- <code>docs/architecture.md</code> und <code>docs/architecture.de.md</code>
- <code>docs/repository-concept.md</code> und
  <code>docs/repository-concept.de.md</code>
- <code>docs/decisions/README.md</code> und
  <code>docs/decisions/README.de.md</code>
- Die Einträge <code>CR-20260714-repository-concept</code> in
  <code>reports/audits/change-records/README.md</code> und
  <code>reports/audits/change-records/README.de.md</code>
- Dieses englisch-deutsche Change-Record-Paar

Absichtliche lokale unversionierte Konfiguration: nur <code>AGENTS.md</code>.
Der gemeinsame Change-Record-Index kann außerdem bewahrte gleichzeitig
entstandene Einträge enthalten; dieser Record betrifft nur die oben genannten
Einträge.

## Hinzugefügte oder geänderte Tests

None. Bestehende Repository-Dokumentations- und Quick-Check-Validierungen
wurden ausgeführt; durch diesen Change Record wurden keine Tests, Generatoren,
Workflows, Product-Source- oder Framework-Dateien verändert.

## Ausgeführte Befehle

| Exakter Befehl | Exit-Code oder Ergebnis | Sanitisierte relevante Zusammenfassung | Kanonischer Evidence-Pfad | Run-ID |
| --- | --- | --- | --- | --- |
| <code>rtk make check-bilingual-docs</code> | 0 | Die englisch-deutsche Dokumentationspaarung und Change-Record-Struktur bestanden. | None; nur Befehlsvalidierung | None |
| <code>rtk make check-doc-links</code> | 0 | Repository-relative Dokumentationslinks bestanden. | None; nur Befehlsvalidierung | None |
| <code>rtk make check-variable-documentation</code> | 0 | Dokumentierte Variablenreferenzen bestanden. | None; nur Befehlsvalidierung | None |
| <code>rtk git diff --check</code> | 0 | Keine Whitespace-Fehler im reviewten Arbeitsbaum-Diff. | None; nur Befehlsvalidierung | None |
| <code>rtk env CODEX_TEMP_ROOT=&lt;task-local-root&gt; TMPDIR=&lt;task-local-root&gt;/tmp BUILD_ROOT=&lt;task-local-root&gt;/build TMP_ROOT=&lt;task-local-root&gt;/tmp LOG_ROOT=&lt;task-local-root&gt;/logs VERIFIED_RUN_ROOT=&lt;task-local-root&gt;/verified EVIDENCE_ROOT=&lt;task-local-root&gt;/evidence make quick-check</code> | 143 (terminated) | Erste statische und Contract-Teile bestanden, aber die Apache-C17-Lint-Provisionierung überschritt die Task-Temp-Grenze; der unvollständige Lauf wurde gestoppt. Er ist kein bestandenes Ergebnis und keine Runtime-Evidence. | None; bereinigter task-lokaler temporärer Root | None |

## Security-Auswirkung

Keine Änderung des Sicherheitsverhaltens. Das Konzept dokumentiert bestehende
sicherheitsrelevante Grenzen, einschließlich Ownership, begrenztem
Transaktionszustand, Konfigurationsdefaults und der Grenze
connector-spezifischer Failure-Semantik. Es vermindert das Risiko, historische
Evidence zu stark zu behaupten, validiert aber keine neue Runtime-Security-
Eigenschaft, ändert keinen Default und legt keine sensitiven Daten offen.

## Dokumentationsänderungen

Das paarweise Repository-Konzept und der ADR-Leitfaden wurden hinzugefügt; das
Konzept wurde aus Root-, Dokumentations- und Architekturnavigation verlinkt; die
lokale ignorierte Agent-Anleitung wurde aktualisiert; und dieser paarweise
Change Record mit Indexeintrag wurde ergänzt.

## Runtime-Evidence

Für diese Änderung wurde keine Runtime-Evidence erhoben oder beansprucht. Der
vorhandene Six-Connector-Core-Completion-Report bleibt im Konzept
<code>documented_not_runtime_verified</code>, da seine Rohartefakte hier nicht
unabhängig erneut validiert wurden. Generated Freshness Output mit der Markierung
stale ist für aktuelle Promotion <code>unknown</code>.

## Bekannte Einschränkungen

- Connector-Capability-Manifeste verwenden für mehrere Connectoren historische/
  Compatibility-Profile, während die aktuelle Architektur native Product-Pfade
  auswählt; der Unterschied ist dokumentiert, nicht korrigiert.
- Aktuelle Generated-Freshness- und Full-Run-Zusammenfassungen sind stale und
  wurden nicht neu erzeugt.
- Mehrere generische Lifecycle-/Evidence-Utilities liegen weiter im Parent und
  das Framework enthält etwas host-orientierte Provisionierung; die Zielgrenze
  ist daher dokumentiert und nicht mechanisch durchgesetzt.
- Die historischen Evidence-Rohdaten und alle Connector-Runtimes wurden für
  diese reine Dokumentationsänderung nicht erneut ausgeführt.

## Verbleibende Risiken

Die Zielgrenze kann driften, bis Ownership-Checks automatisiert sind und die
dokumentierten Capability-/Evidence-Abweichungen abgeglichen werden. Der
ADR-Prozess, explizite Claim-Labels, lokale Agent-Anleitung und künftige Change
Records mindern dieses Risiko, ersetzen aber keine Evidence-Aktualisierung oder
architektonische Migration.

## Nicht ausgeführte Prüfungen mit Begründung

Es wurden keine Connector-Builds, Konfigurationsprüfungen, Lifecycles,
Release-Evidence-Neuerzeugung, Capability-Manifest-Aktualisierung oder
vollständige Framework-Migration abgeschlossen. Der geforderte
<code>make quick-check</code> wurde mit isolierten Roots gestartet, aber mit
Exit-Code <code>143</code> beendet, als die Apache-C17-Lint-Provisionierung die
Task-Temp-Grenze überschritt; für ein vollständiges Ergebnis muss er mit einem
genehmigten größeren isolierten Budget erneut laufen. Diese Aktionen liegen
außerhalb eines reinen Dokumentationsumfangs, können externe Abhängigkeiten und
sanitisierte Runtime-Artefakte benötigen und würden Evidence erzeugen oder neu
interpretieren, die diese Aufgabe nicht verifiziert hat. Kein historisches
Runtime-Rohartefakt wurde unabhängig erneut validiert.

## Finaler Diff- und Review-Status

Ein manueller Review bestätigt, dass dieser Record ausschließlich die oben
aufgeführte Dokumentations- und lokale Anleitungsarbeit beschreibt, fremde
Arbeitsbaumänderungen bewahrt und statische Prüfungen nicht als Runtime-Beweis
darstellt. Die finale Whitespace-Prüfung bestand. Der beabsichtigte
Commit-Betreff lautet <code>Document connector monorepo concept</code>; dieser
Task hat keinen Commit und keinen Pull Request erzeugt.
