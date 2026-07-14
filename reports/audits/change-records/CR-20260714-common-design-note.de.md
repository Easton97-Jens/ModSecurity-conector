# Change Record: Common-Designnotiz mit aktuellen Produktrouten abgleichen

**Sprache:** [English](CR-20260714-common-design-note.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Titel | Common-Designnotiz mit aktuellen Produktrouten abgleichen |
| Change-ID | CR-20260714-common-design-note |
| Datum (UTC) | 2026-07-14T10:29:29Z |
| Autor oder ausführender Agent | Codex |
| Basis-Revision | db3f1747bddd2d36470f61c9b04029876f864667 |
| Zugehöriges Issue oder Pull Request | None |
| Finale Revision | not committed |

## Motivation und Problemstellung

Die Zeile `Common design note` in `docs/repository-concept.de.md` dokumentierte
eine Parent-only-Abweichung mittlerer Priorität: `common/docs/design.md` war als
`scaffolded` markiert und enthielt historisches Sidecar-/Open-Connector-
Material, das den aktuellen ausgewählten nativen Routen widersprechen konnte.
Insbesondere stand die historische lighttpd-Beschreibung
`integration_mode=sidecar_proxy` im Widerspruch zur aktuellen Route
`patched-native-lighttpd`. Diese Änderung macht die gepaarten
Common-Designnotizen zu einer korrekten, abgegrenzten Anleitung für die
aktuelle Common-Ownership-Grenze und verweist für aktuelle Architekturclaims
ausdrücklich auf die verbindliche Produktdokumentation.

## Betroffene Komponenten und Sicherheitsgrenzen

Der Scope umfasst die Architekturnotiz unter `common/docs/`, ihren
Dokumentations-Contract-Test sowie die betroffene bilinguale Dokumentation und
die Change-Record-Indizes des Parent-Repositorys. Die Grenze lautet: `common/`
bleibt host-neutral; Host-SDK-Objekte, Hooks, Filter, Host-Lebensdauern und
client-sichtbare Aktionen bleiben in `connectors/<name>/`; wiederverwendbare
Testfälle, Runner, Normalizer und Schemas bleiben im Framework. Framework-
Dateien, generierte Reports, Runtime-Artefakte, Connector-Source und
Konfiguration wurden nicht geändert.

## Akzeptanzkriterien

| Kriterium | Status | Evidenz |
| --- | --- | --- |
| Die gepaarten Common-Designnotizen benennen die aktuelle host-neutrale Grenze und verlinken die verbindliche Architektur und das Repository-Konzept. | erfüllt | `tests.test_bilingual_docs` und `make check-bilingual-docs` |
| Historische Routen können nicht als aktuell ausgewählte Routen dargestellt werden; ausdrücklich markiertes historisches oder Kompatibilitätsmaterial bleibt unterscheidbar. | erfüllt | Fokussierte positive, Ablehnungs- und Grenzfall-Tests |
| Die dokumentierte Abweichung `Common design note` wird erst nach Bestehen ihrer fokussierten und verpflichtenden Prüfungen aktualisiert. | erfüllt | Aktualisiertes `docs/repository-concept.de.md` und erfolgreiche fokussierte Prüfungen |
| Englische und deutsche Dokumentation sowie Link- und Whitespace-Prüfungen bestehen. | erfüllt | Dokumentationsprüfungen und `git diff --check` |
| Es wird kein Runtime-, Production-Readiness- oder Framework-Claim ergänzt. | erfüllt | Manueller finaler Review und keine Runtime-Evidence |

## Untersuchte Alternativen

Die Abweichung der Capability-Integrationsmodi wurde nicht gewählt, weil sie
vier Connector-Manifeste und Generatorverhalten umfasst. Runtime-Report-
Provenance, Generated-Report-Freshness, Testgrenze und Generator-Ownership
brauchen Parent-und-Framework-Arbeit oder frische Runtime-Artefakte.
Connector-Selbstständigkeit erfordert einen Connector-für-Connector-Audit von
Build, Packaging und Installation. Ein ADR wurde nicht gewählt, weil keine
aktuelle Entscheidungsautorität zur Annahme einer rückwirkenden dauerhaften
Entscheidung vorlag. Historisches Runtime-Material ohne Current-Boundary-
Contract umzuschreiben oder zu verschieben würde dieselbe Mehrdeutigkeit
belassen.

## Implementierungsentscheidung und Begründung

Die eingerüstete Notiz wurde durch eine kurze bilinguale Current-Boundary-Notiz
ersetzt: C-first-, Bounded-Data-, Ownership- und Evidence-Grenzen von Common,
die sechs ausgewählten Connector-Routen und Links zum verbindlichen
Produktkonzept, zur Architektur und zur Test-/Evidence-Dokumentation. Ein
fokussierter Parent-Dokumentations-Contract ist jetzt Teil des bestehenden
Gates `check-bilingual-docs` und läuft damit auch über `make lint` und
`make quick-check`. Er weist einen eingerüsteten Status, eine falsche
ausgewählte Route oder einen unqualifizierten historischen Integrationsmodus
zurück, erlaubt aber eine ausdrücklich markierte historische oder
`compatibility_only`-Referenz. Dies ist eine Korrektur von Dokumentation und
Contract, keine Runtime- oder Produkt-Source-Änderung.

## Geänderte Dateien

- `ci/checks/documentation/check-bilingual-docs.py`
- `tests/test_bilingual_docs.py`
- `common/docs/design.md`
- `common/docs/design.de.md`
- `common/README.md`
- `common/README.de.md`
- `docs/repository-concept.md`
- `docs/repository-concept.de.md`
- `reports/audits/change-records/CR-20260714-common-design-note.md`
- `reports/audits/change-records/CR-20260714-common-design-note.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

Es wurde keine lokale unversionierte Konfiguration absichtlich geändert.
Getrennte Apache- und `Makefile`-Arbeit erschien nach der anfänglichen sauberen
Statusprüfung; sie wurde weder geändert noch in diese Änderung aufgenommen.

## Hinzugefügte oder geänderte Tests

`tests/test_bilingual_docs.py` ergänzt drei Fälle für die Common-Designnotiz:
einen positiven Current-Document-Fall, einen Ablehnungsfall für `scaffolded`,
eine falsche ausgewählte lighttpd-Route und ein unqualifiziertes
`integration_mode=sidecar_proxy` sowie einen Grenzfall, der eine ausdrücklich
historische `compatibility_only`-Referenz akzeptiert.

## Ausgeführte Befehle

| Exakter Befehl | Exit-Code oder Ergebnis | Sanitisierte relevante Zusammenfassung | Kanonischer Evidence-Pfad | Run-ID |
| --- | --- | --- | --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest -v tests.test_bilingual_docs` | `1`, dann `0` | Der erste fokussierte Lauf zeigte einen Whitespace-Normalisierungsfehler in der neuen Required-Content-Prüfung; nach der Korrektur bestanden alle 9 Tests. | None | None |
| `make check-bilingual-docs` | `0` | Bilinguale Dokumentation einschließlich des neuen Common-Notiz-Contracts und Change-Record-Paars bestand. | None | None |
| `make check-doc-links` | `0` | Parent-Repository-Referenzen und Framework-Dokumentationslinks bestanden. | None | None |
| `make check-variable-documentation` | `0` | 85 dokumentierte Variablenreferenzen wurden erfolgreich gescannt. | None | None |
| `make check-common-sdk-contract` | `0` | Common-Host-SDK-Grenzen-Contract bestand. | None | None |
| `make check-common-security-contract` | `0` | Common-Security-/Data-Flow-Contract bestand. | None | None |
| `make check-common-flow-integrity` | `0` | Common-Flow-/Ownership-Integritäts-Contract bestand. | None | None |
| `make quick-check` | `blocked_by_resource_limit` | Der Lauf begann externe Runtime-Komponenten vorzubereiten und zu kompilieren. Er wurde mit `SIGINT` unterbrochen, nachdem der größte gemessene Temporary-Root-Snapshot `1744452` KiB erreichte; der entkoppelte Command-Wrapper lieferte keinen Exit-Code. | None | None |
| `git diff --check` | `0` | Keine Whitespace-Fehler im getrackten Worktree-Diff. | None | None |
| `git status --short` | `0` | Scope-Review abgeschlossen; getrennte Apache- und `Makefile`-Änderungen blieben unverändert. | None | None |

## Security-Auswirkung

Runtime-Sicherheitsverhalten, Default, Eingabegrenze, Logging-Format und
Vertrauensbeziehung änderten sich nicht. Die korrigierte Notiz reduziert das
Risiko, dass Maintainer einen historischen Sidecar-Pfad für eine aktuelle
ausgewählte Route halten und dadurch Ownership- oder Evidence-Claims falsch
anwenden. Die Common-Security- und Flow-Integrity-Contracts bestehen weiter.

## Dokumentationsänderungen

Die gepaarte Common-Designnotiz beschreibt jetzt die aktuelle Grenze und
ausgewählte Routen; das gepaarte Common-README indexiert sie. Das gepaarte
Repository-Konzept markiert nur diese Abweichung als adressiert. Der gepaarte
Change Record und Index zeichnen die Änderung auf. `docs/architecture.md` und
`.de.md`, Connector-Guides und Runtime-Dokumentation wurden geprüft, brauchten
aber keine Änderung, weil ihre aktuellen Routenbeschreibungen bereits
verbindlich waren.

## Runtime-Evidence

Für diese Änderung wurde keine Runtime-Evidence erhoben oder beansprucht.
Dokumentations-, Source- und Contract-Prüfungen belegen weder Hostverkehr noch
Runtime-Verhalten.

## Bekannte Einschränkungen

Diese Änderung gleicht weder Capability-Manifeste ab noch aktualisiert sie
generierte Reports, erzeugt kanonische Runtime-Evidence, ändert
Kompatibilitätsimplementierungen oder auditiert Connector-Packaging und
Installation. Die Common-Routentabelle ist ein Dokumentations-Contract, kein
Capability- oder Runtime-Ergebnis.

## Verbleibende Risiken

Künftige Änderungen ausgewählter Routen müssen bei Bedarf gleichzeitig das
verbindliche Konzept, den Connector-Guide und die Common-Notiz aktualisieren.
Der unterbrochene `make quick-check` liefert kein vollständiges Lint-Ergebnis;
die kleineren relevanten Prüfungen oben bestanden.

## Nicht ausgeführte Prüfungen mit Begründung

`make lint` wurde nicht separat erneut ausgeführt, weil `make quick-check` es
enthält und die beobachtete Runtime-Komponenten-Kompilierung die 1536-MiB-
Warnschwelle für temporären Speicher überschritt. Runtime-, Smoke-, Lifecycle-
und Connector-Build-Läufe wurden nicht ausgeführt, weil diese Änderung kein
Runtime- oder Build-Verhalten verändert und keine Runtime-Evidence erzeugen
darf.

## Finaler Diff- und Review-Status

Der finale Scope-Review fand nur die aufgeführten Common-Dokumentations-,
Contract-, Test-, Konzept- und Change-Record-Aktualisierungen. `git diff --check`
bestand. Framework-Submodule-Diff und -Status waren leer. Der Worktree enthält
außerdem getrennte Apache-Cleanup- und `Makefile`-Änderungen, die nach der
anfänglichen sauberen Statusprüfung erschienen; sie wurden erhalten und aus
diesem Change Record ausgeschlossen. Der Record stimmt mit der scoped
Implementierung und den tatsächlichen Ergebnissen überein. Vorgesehener
Commit-Titel: `Align Common design note with selected product routes`.
