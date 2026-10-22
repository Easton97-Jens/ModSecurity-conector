# Change Record: CR-20261022-i12-haproxy-415-evidence

**Sprache:** [English](CR-20261022-i12-haproxy-415-evidence.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261022-i12-haproxy-415-evidence |
| Datum (UTC) | 2026-10-22 |
| Basis-Revision | `671fb2c7a59b917ea7d51cd2f4f46bbef4843c22` |
| Vor Lieferung integrierte Zielbranch-Revision | `76672071c3f7665dfde3340bef9e64271d6f6e70` |

## Motivation und Problemstellung

PR #415 benötigte einen aktuellen, quellgebundenen Abgleich der drei
HAProxy-I12-Routen. Die anfängliche Aufgabenbasis enthielt neun vollständige
Lifecycle-PASS-Ergebnisse; das unmittelbar vorherige historische Ledger bereits
30. Keines von beiden integrierte die später geprüften HAProxy-3.2.25-Captures
in ein kompaktes aktuelles Ledger oder bot einen dauerhaft abrufbaren,
inhaltsadressierten Rohdatendownload. Der aktuelle Sonar-Lauf behandelte
außerdem Oracle-Quellpfade als JSON-Property-Namen und meldete begrenzte
Maintainability- und Pfadvalidierungsbefunde im ausschließlich HAProxy-bezogenen
Harness.

## Akzeptanzkriterien

- Native HTX, SPOP Request und den HTX Response-Companion getrennt bewerten;
  eine Anfrage niemals als drei Hostausführungen zählen.
- Nur vollständige, an ein Original-Oracle gebundene Host-/Filter-/Native-
  Engine-Lifecycles qualifizieren; ACK-only-, HTTP-only-, partielle und
  negative Beobachtungen unterhalb Lifecycle-PASS halten.
- Alle 278 Pflicht-IDs und 124 ursprünglichen HAProxy-Oracles mit expliziten
  offenen Listen abgleichen.
- Exakte Revisions-, Binary-, Konfigurations-, Frame-, Client-/Backend-,
  Commit-, physische Sink- und Finish-/Free-Provenienz für jeden neuen Kredit
  bewahren.
- Einen zweisprachigen Bericht, ein maschinenlesbares Ledger und ein
  inhaltsadressiertes Rohdatenpaket mit unabhängig geprüften Hashes liefern.
- Repository-Änderungen auf HAProxy-Harnesses, Tests, Fixtures und eigene
  EN/DE-/JSON-Evidence begrenzen. Zentrale Matrix, gemeinsame Captures,
  Generatoren und andere Connectoren unverändert lassen.
- Fokussierte HAProxy-C-, HTX-, SPOP-, Mutations-, Dokumentations- und Ledger-
  Prüfungen vor normaler Lieferung bestehen; den PR als Draft belassen und
  nicht mergen.

## Implementierungsentscheidung und Begründung

Die Evidence wurde aus versiegelten, routenspezifischen Hostpaketen geprüft.
32 neue Qualifikationen sind an Produkt-/Capture-Revision
`0325c1d7a1c2dd85ab2ca270d494e97ee8a5b92a` gebunden; drei engere Kontrollen
wurden auf der gemessenen Revision
`671fb2c7a59b917ea7d51cd2f4f46bbef4843c22` gebaut und ausgeführt. Diese
Kontrollen übertragen das vollständige 62-ID-Inventar nicht auf die spätere
Revision.

Im 124-Zeilen-Oracle-Fixture änderte sich nur die Darstellung von
`original_source_hashes`: von Objekt-Properties zu geordneten
`{path, sha256}`-Werten. Der HAProxy-lokale Leser akzeptiert eingefrorene und
migrierte Form, verwirft mehrdeutige oder fehlerhafte Einträge und
kanonikalisiert beide auf denselben semantischen Digest
`2e9581873d5dfd6acf15b5396acddb690a0de3f71d6f1be0207542c37f2e2689`.
Kein Oracle, keine Quellbindung und keine Disposition ändern sich.

Der Batch-Harness akzeptiert nun exakt die sechs festen Namespace-Schlüssel,
bevor er `/proc/self/ns` liest. Kleine Helper-Extraktionen senken Komplexität,
während Native-, SPOP- und Companion-Replays byteidentisch zu den
Voränderungsbeobachtungen bleiben. Kein Connector-Produktsource änderte sich.

## Geänderte Dateien

- `connectors/haproxy/harness/fixtures/i12-oracles-20261015.json`
- `connectors/haproxy/harness/i12_oracle_fixture.py`
- HAProxy-eigene I12-Batch-, Native-, SPOP-, Companion- und Route-Observer-
  Module unter `connectors/haproxy/harness/`
- HAProxy-I12-Unittests unter `tests/test_haproxy_i12_*.py`
- `docs/pr-415-i12-haproxy-20261022.md` und die deutsche Begleitdatei
- `reports/testing/i12-haproxy-415-20261022.json`
- dieses zweisprachige Change Record

## Ausgeführte Befehle

- `rtk .../test-env/bin/python -B -m unittest -v` für alle elf
  `tests.test_haproxy_i12_*`-Module — Exit `0`; 156 Tests bestanden in 8,693
  Sekunden.
- `rtk make ... check-haproxy-c17` — Exit `0`; HAProxy-C17-Kompilierung
  bestanden.
- `rtk make ... check-haproxy-htx-overlay` — Exit `0`; alle HTX-Quell- und
  Lifecycle-Verträge bestanden.
- `rtk make ... check-haproxy-spop-event-sink` — Exit `0`; 19 physische
  Serialisierungs-/Write-/Flush-/Close-Fehlerprüfungen bestanden in 3,481
  Sekunden.
- `rtk make ... check-i10-haproxy-callers` — Exit `0`; 20 Direct-/SPOP-Caller-
  und Mutationstests bestanden in 242,461 Sekunden.
- `rtk make ... check-haproxy-common-adoption` und
  `check-haproxy-c-standard-wiring` — Exit `0`.
- `rtk make check-bilingual-docs` und `rtk make check-doc-links` — Exit `0`.
- `rtk proxy /usr/local/bin/python3 -I .../verify-final-report-20261022.py` —
  Exit `0`; 278 eindeutige Katalog-IDs, 124 Oracle-Zeilen, 32 eindeutige neue
  PASS-IDs und 100 Dateihashreferenzen geprüft. Der Bericht umfasst 322050 Byte
  und hat SHA-256
  `d19aa8008d78c57ab510568f8c7e59b124c5ea8aac365f453a2c96b25b102d26`.
- `rtk sha256sum -c SHA256SUMS` auf dem frisch extrahierten Draft-Download —
  Exit `0`; alle 979 internen Einträge bestanden. Sein unabhängiger Verifier
  bestand 974 Inhaltsobjekte und 1.407 Quellbindungen.
- Eine Wiederholung des historischen Absolute-Path-Auswahlverifiers endete
  nach dem späteren reinen Sonar-Harness-Refactor mit Exit `1`, weil der
  aufgezeichnete veränderliche Worktree-Pfad nun neue Bytes enthält. Die
  aufgezeichnete Vorrefactor-Prüfung bleibt versiegelt; der unveränderte
  inhaltsadressierte Downloadverifier löst und prüft die ursprünglichen Objekte
  ohne veränderliche Pfade.
- `rtk --version`, `rtk which rtk` und `rtk gain` bestätigten RTK `1.0.1`
  unter `/root/.local/bin/rtk`; Projektbefehle nutzten den vorgeschriebenen
  Proxy.

## Security-Auswirkung

Keine Produktions-Trust-Boundary ändert sich. Der Namespace-Leser verwirft
fehlende, zusätzliche, traversalartige oder absolute benutzerbeeinflusste
Schlüssel vor Dateisystemzugriffen und dereferenziert nur feste Namespace-
Pfade. Oracle-Quellpfade werden als Werte mit eindeutigen nichtleeren Namen und
lowercase SHA-256 strikt validiert. Sinkfehlertests erhalten fail-closed-
Verhalten für `fputs`, `ferror`, `fflush` und `fclose`. Ein unabhängiges
begrenztes Security-Review fand keine eingeführte Security- oder Correctness-
Regression. Keine Validierung, Isolation, Redaction, Compilerwarnung oder
Quality Gate wurde abgeschwächt.

## Runtime-Evidence

| Route | Pflicht | Historische PASS | Neue PASS | Aktuelle PASS | Unqualifiziert |
| --- | ---: | ---: | ---: | ---: | ---: |
| `haproxy-native-htx` | 112 | 25 | 6 | 31 | 81 |
| `haproxy-spop-request` | 94 | 3 | 17 | 20 | 74 |
| `haproxy-spop-htx-response-companion` | 72 | 2 | 9 | 11 | 61 |
| **Gesamt** | **278** | **30** | **32** | **62** | **216** |

Die ursprüngliche Oracle-Teilmenge löst 31/48 Native-, 21/44 SPOP- und 13/32
Companion-Zeilen auf: 65 aufgelöst und 59 offen. Die 32 neuen PASS-Pakete
enthalten sechs Native-, siebzehn SPOP- und neun unabhängig gemessene
Companion-IDs. Die akzeptierte Auswahl hat SHA-256
`2e497d8b32e9a786bdfca88d314e02e5e666a2ea8e9f05e2b809233891731053`.

Das Roharchiv umfasst 5.181.893 Byte mit SHA-256
`ac9de960803803fafe923da1bc2c87ecb6ce485ac51e5580871c0d22f477fe5b`;
sein Manifest hat SHA-256
`8a1aefe5e5eff2474b0f23de5f08d625979ca4446bf4c70b79dcc1161da3bd47`.
Die hochgeladenen Draft-Assets wurden vor Veröffentlichung über GitHubs Asset-
API erneut heruntergeladen und unabhängig geprüft. Das Release bleibt Draft,
bis es an den final geprüften PR-Commit gebunden werden kann.

## Bekannte Einschränkungen

`I12_PARTIAL` bleibt der einzig belegte Status. Native hat 81 unqualifizierte
Pflicht-IDs und 17 offene Oracles, SPOP 74 und 23, Companion 61 und 19.
Unbekanntes oder chunked SPOP-Framing und nicht unterstützte HTTP/2-Abbildungen
bleiben unvollständig inspiziert. SPOP bleibt ein begrenztes Authorization-
Sample und kein unbegrenzter Streamingpfad. Fehlende, falsche oder veraltete
Companion-OUTCOME-Daten, fehlendes EOS, nicht unterstütztes Strict-Verhalten
und fehlende/abgelaufene Correlation bleiben negative oder partielle Evidence.
Der parallele Companion-Versuch hatte nur 10/16 erfolgreiche Hauptrequests,
sechs `502`-Antworten und sieben unbekannte Beobachtungen und erhält daher
keinen Lifecycle-Kredit.

## Verbleibende Risiken

GitHub-Checks und das Sonar Quality Gate müssen auf dem exakt final gepushten
Head gelesen werden. Das Evidence-Prerelease ist noch Draft und besitzt keine
Tag-Referenz; Veröffentlichung, öffentlicher URL-Readback und Tag-zu-Head-
Prüfung erfolgen erst, wenn genau dieser Head stabil ist. Neu bestätigte
Produktfehler bleiben Arbeit für #382/#410 und werden nicht über diesen
Evidence-PR repariert.

## Nicht ausgeführte Prüfungen mit Begründung

Nach den beiden gemessenen Revisionen wurde kein neuer privater Host-Capture
erfunden. Die 32 neuen Qualifikationen bleiben an ihre ursprünglichen
`0325c1d7`-Hostläufe gebunden; die drei `671fb2c7`-Kontrollen belegen nur ihre
benannten Pfade. Eine repository-weite All-Connector-Matrix lief nicht, weil
der autorisierte Umfang HAProxy-spezifisch ist und sich weder gemeinsamer
Generator noch Connector-Produktsource änderte. Ein öffentlicher,
unauthentifizierter Release-Download ist nicht prüfbar, solange das Release ein
Draft ist; er ist ein Delivery-Gate nach Exact-Head-CI und kein Ersatz für eine
lokale Prüfung.

## Finaler Diff- und Review-Status

Der lokale Diff ist auf HAProxy-eigene Harnesses, Fixtures, Tests sowie eigene
zweisprachige/JSON-Evidence begrenzt. Unabhängige Code-, Security- und
Dokumentationsreviews fanden keinen blockierenden Befund, keine geänderte
Oracle-Entscheidung und keine Lifecycle-Überbewertung. Die fokussierte lokale
Validierung ist abgeschlossen. Normaler Commit, Push, GitHub-/Sonar-Readback
auf dem exakten Head und finale Evidence-Veröffentlichung bleiben Delivery-
Schritte; kein Force-Push, Merge oder Master-Änderung wird behauptet.
