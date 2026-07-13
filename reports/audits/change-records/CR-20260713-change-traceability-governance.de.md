# Change Record: Versionierte Change-Traceability-Governance

**Sprache:** [English](CR-20260713-change-traceability-governance.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Titel | Versionierte Change-Traceability-Governance |
| Change-ID | CR-20260713-change-traceability-governance |
| Datum (UTC) | 2026-07-13T19:24:43Z |
| Autor oder ausführender Agent | Codex-Agent <code>/root</code> |
| Basis-Revision | 056f93232c6f5dba132bfb2204d96ce49707507b |
| Zugehöriges Issue oder Pull Request | None |
| Finale Revision | Nicht committed |

## Motivation und Problemstellung

Einen verbindlichen, versionierten Weg etablieren, der nicht triviale
Repository-Änderungen von Motivation und Akzeptanzkriterien über
Entscheidungen, Implementierung, Tests und Dokumentation bis zu bekannten
Grenzen nachvollziehbar macht.

## Betroffene Komponenten und Sicherheitsgrenzen

Die abgegrenzte Änderung betrifft Repository-Dokumentation, manuelle
Audit-Records, Pull-Request-Vorlage und die lokal ignorierte
Anweisungsdatei <code>AGENTS.md</code>. Richtlinie und Vorlagen bewahren die
Grenze, dass Secrets, sensible Rohdaten, Runtime-Daten, Builds und Caches
außerhalb des Checkouts bleiben. Die lokale Änderung an
<code>AGENTS.md</code> ist durch <code>.git/info/exclude</code> absichtlich
ausgeschlossen und kein Teil des versionierten Diffs.

Im finalen Working Tree lagen außerdem unabhängige Änderungen an Connector-
TODOs. Sie wurden für diesen Record weder verändert noch reviewed.

Während dieser Arbeit wurde der aktive Bilingual-Checker unabhängig um
Abschnittsanforderungen für Dateien im Change-Record-Verzeichnis erweitert.
Dieser Record ändert den Checker nicht; das neue Verzeichnis-README
dokumentiert die Pflichtfelder nun als Guide auf Indexebene.

## Akzeptanzkriterien

| Kriterium | Status | Evidenz |
| --- | --- | --- |
| Verbindliche englisch-deutsche Richtlinie und gepaarte Change-Record-Vorlagen existieren | Erfüllt | Bilinguale Dokumentationsprüfung bestand nach Korrektur der deutschen Links. |
| Dokumentationsindizes und Pull-Request-Vorlage machen den Prozess auffindbar | Erfüllt | Abgegrenztes Final-Review und erfolgreiche bilinguale Link-Validierung. |
| Lokale AGENTS-Anweisung ist aktualisiert, ohne lokale Codex-Dateien zu versionieren | Erfüllt | Die lokal ignorierte Datei ist aktualisiert und erscheint nicht im Git-Status. |
| Erforderliche Dokumentations-, Link-, Whitespace- und Statuschecks sind ehrlich dokumentiert | Erfüllt | Die finalen Bilingual-, Repository-Link-, Whitespace- und Statuschecks sind mit ihren tatsächlichen Ergebnissen dokumentiert. |

## Untersuchte Alternativen

- Nur die Pull-Request-Vorlage verwenden. Verworfen, weil sie keinen
  dauerhaften, auffindbaren, versionierten Record neben der Änderung bietet.
- Records unter <code>reports/testing/generated/</code> ablegen. Verworfen,
  weil dieses Verzeichnis generatorverwaltet und für manuelle Audit-Dokumente
  ungeeignet ist.
- Vollständige Befehlsausgaben oder Runtime-Rohartefakte speichern. Verworfen,
  weil sie sensible Daten offenlegen könnten und der Evidence-Grenze des
  Repositorys widersprechen.
- Nur englische Records anlegen. Verworfen, weil manuell gepflegte Reports
  englisch-deutsche Begleitdateien benötigen.
- Den parallel geänderten Checker ändern, damit er das README ausnimmt.
  Verworfen, weil diese Checker-Änderung außerhalb dieses Record-Umfangs
  liegt; die Erweiterung des neuen README zu einem nützlichen Feld-Guide
  erfüllt den aktiven Vertrag ohne Änderung unabhängiger Arbeit.

## Implementierungsentscheidung und Begründung

Eine verbindliche englisch-deutsche Richtlinie unter <code>docs/</code> und
ein manuell gepflegtes, versioniertes EN/DE-Record-Verzeichnis unter
<code>reports/audits/</code> ergänzen. Die Vorlagen verlangen den vollständigen
Entscheidungs- und Prüfpfad, begrenzen aufbewahrte Evidence aber auf kurze
sanitisierte Zusammenfassungen. Indexlinks und die bilinguale Pull-Request-
Vorlage machen den Prozess beim Erstellen und Review auffindbar. Diese
Einrichtung erhält selbst einen Record, weil sie eine nicht triviale
Governance-Änderung ist. Das Verzeichnis-README fasst außerdem jedes
Pflichtfeld zusammen, sodass es zugleich Navigationsindex bleibt und mit dem
aktiven Dokumentationsvertrag kompatibel ist.

## Geänderte Dateien

Versionierte Dateien im Umfang:

- <code>.github/pull_request_template.md</code>
- <code>README.md</code> und <code>README.de.md</code>
- <code>docs/README.md</code> und <code>docs/README.de.md</code>
- <code>docs/change-traceability.md</code> und
  <code>docs/change-traceability.de.md</code>
- <code>reports/README.md</code> und <code>reports/README.de.md</code>
- <code>reports/audits/change-records/README.md</code> und
  <code>reports/audits/change-records/README.de.md</code>
- <code>reports/audits/change-records/TEMPLATE.md</code> und
  <code>reports/audits/change-records/TEMPLATE.de.md</code>
- dieses englisch-deutsche Change-Record-Paar

Absichtliche lokale, unversionierte Änderung: <code>AGENTS.md</code>. Sie ist
ignoriert und fehlt deshalb absichtlich im Git-Diff.

## Hinzugefügte oder geänderte Tests

None. Diese Änderung fügt Dokumentations- und Governance-Artefakte statt
ausführbarer Tests hinzu.

## Ausgeführte Befehle

| Exakter Befehl | Exit-Code oder Ergebnis | Sanitisierte relevante Zusammenfassung | Kanonischer Evidence-Pfad | Run-ID |
| --- | --- | --- | --- | --- |
| <code>rtk make check-bilingual-docs</code> | 2 | Die erste Validierung fand zwei deutsche Links, die fälschlich auf englische Begleiter zeigten; beide wurden korrigiert. | None | None |
| <code>rtk make check-bilingual-docs</code> | 0 | Bilinguale Dokumentations- und lokale Link-Validierung meldete <code>bilingual docs ok</code>. | None | None |
| <code>rtk make check-bilingual-docs</code> | 2 | Eine spätere Revision des aktiven Checkers verlangte Change-Record-Abschnitte im Verzeichnis-README; der README-Feld-Guide wurde erweitert, ohne diesen unabhängigen Checker zu ändern. | None | None |
| <code>rtk make check-bilingual-docs</code> | 0 | Der erneute Lauf nach der README-Feld-Guide-Aktualisierung meldete <code>bilingual docs ok</code>. | None | None |
| <code>rtk make check-doc-links</code> | 2 | Der repository-weite Check meldet nur bereits vorhandene fehlende <code>AGENTS.de.md</code>-Ziele in <code>README.de.md</code> und <code>docs/reference/variables.de.md</code>. | None | None |
| <code>rtk make check-doc-links</code> | 2 | Ein späterer Lauf nach unabhängigen Working-Tree-Änderungen bestand den Root-Pfadcheck, scheiterte aber im Framework-Linkcheck an geänderten lokalen AGENTS-Ankern und Connector-TODO-Sprachbegleitern. | None | None |
| <code>rtk make check-doc-links</code> | 0 | Die finale Validierung meldete <code>repository path references: PASS</code> und <code>doc links ok</code>. | None | None |
| <code>rtk git diff --check</code> | 0 | Keine Whitespace-Diagnostik für getrackte Working-Tree-Änderungen. | None | None |
| <code>rtk rg -n '[[:blank:]]+$' docs/change-traceability.md docs/change-traceability.de.md reports/audits/change-records .github/pull_request_template.md README.md README.de.md docs/README.md docs/README.de.md reports/README.md reports/README.de.md</code> | 1, erwartet | Keine Trailing-Whitespace-Treffer im abgegrenzten Umfang; Exit 1 bedeutet kein Treffer. | None | None |
| <code>rtk git status --short</code> | 0 | Listete die abgegrenzten Änderungen und unabhängige Connector-TODO-Änderungen; das lokal ignorierte <code>AGENTS.md</code> fehlte. | None | None |

## Security-Auswirkung

Keine Änderung des Connector-Runtime-Sicherheitsverhaltens. Der Prozess senkt
das Risiko undokumentierter Security-Entscheidungen und versehentlich
aufbewahrter sensibler Evidence durch eine Security-Auswirkungssektion,
Runtime-Evidence-Grenze und explizite Datenausschlüsse. Er ersetzt weder
Code-Review noch Secret-Scanning oder Runtime-Validierung.

## Dokumentationsänderungen

Englisch-deutsche Richtlinie zur Nachvollziehbarkeit, englisch-deutsche
README- und Vorlagen-Dateien für Change Records sowie diesen Bootstrap-Record
hinzugefügt. Root-, Dokumentations- und Reports-Indizes in beiden Sprachen
aktualisiert. Beide Abschnitte der Pull-Request-Vorlage erweitert. Die lokal
ignorierte Regel in <code>AGENTS.md</code> aktualisiert, ohne lokale
Codex-Konfiguration zu versionieren.

## Runtime-Evidence

Für diese Änderung wurde keine Runtime-Evidence erhoben oder beansprucht.
Diese Governance-Änderung macht keinen Connector-Runtime-Claim.

## Bekannte Einschränkungen

- Frühere <code>make check-doc-links</code>-Fehler traten auf, während
  unabhängige Working-Tree-Dokumentations-/Konfigurationsänderungen in Arbeit
  waren. Sie bleiben in der Befehlshistorie erhalten, aber der finale
  repository-weite Linkcheck besteht.
- Change Records werden manuell gepflegt. Der Ablauf beruht auf Autor- und
  Reviewer-Disziplin statt auf einem automatischen Vollständigkeits-Gate.
- Die Anweisung in <code>AGENTS.md</code> bleibt absichtlich unversioniert;
  der maßgebliche Prozess ist deshalb zusätzlich in versionierter
  Dokumentation enthalten.

## Verbleibende Risiken

Ein Autor kann einen Record weiterhin auslassen oder veralten lassen, bis ein
Review dies erkennt; englische und deutsche Begleiter können trotz
Strukturchecks semantisch auseinanderlaufen. Pull-Request-Checkliste,
gepaarte Vorlagen, Pflicht zum Final-Diff-Abgleich und der vorhandene
Bilingual-Check mindern diese Risiken, beseitigen sie aber nicht vollständig.

## Nicht ausgeführte Prüfungen mit Begründung

- <code>make quick-check</code> und <code>make lint</code> wurden nicht
  ausgeführt. Die verlangten Validierungsziele waren die fokussierten
  Dokumentations-, Link-, Diff- und Statuschecks; die Änderung enthält keinen
  ausführbaren Source.
- Connector-Builds, Konfigurationschecks, Lifecycle-Läufe und Runtime-Tests
  wurden nicht ausgeführt, weil diese Dokumentations-/Governance-Änderung
  keinen Runtime-Claim erhebt und solche Befehle externe Build-/Runtime-
  Artefakte erzeugen können.

## Finaler Diff- und Review-Status

Der abgegrenzte finale Diff einschließlich neuer ungetrackter Markdown-Dateien
wurde per Self-Review geprüft. <code>git diff --check</code> endete mit
Exit-Code 0, und der abgegrenzte Trailing-Whitespace-Scan fand keine Treffer.
Der Bilingual-Check bestand nach einer korrigierten Link-Iteration und einer
vom aktiven Checker geforderten Aktualisierung des Verzeichnis-README. Der
finale repository-weite Linkcheck meldete
<code>repository path references: PASS</code> und <code>doc links ok</code>.

Dieser Record ist mit dem abgegrenzten tatsächlichen Diff und den realen
Ergebnissen oben abgeglichen. Es wurde kein Commit und kein Pull Request
erstellt. Die erforderlichen Checks werden nach diesem Record-Abgleich erneut
ausgeführt; kein Test gilt allein als bestanden, weil er geplant war.
