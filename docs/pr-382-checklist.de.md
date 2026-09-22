# PR #382: Checkliste für gemeinsames Connector-Verhalten

**Sprache:** [English](pr-382-checklist.md) | Deutsch

[Draft-PR #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382),
Branch `fix/unified-native-results-events-20260921`, Basis
`5170d24801243cdcd7bf1bca6123bf8cb2c72386`. Aktualisiert: 2026-09-22.

**Die Gesamtimplementierung ist nicht abgeschlossen; der PR ist nicht mergebereit.**
Ein abgehakter Teilbereich behauptet keinen erfolgreichen Lauf aller zehn Routen.
Letzter geprüfter Code-Stand: `bced5ce78c62b7665730d2e81b307a3676da42f3`.
Seine fokussierten Tests und beide Sonar-Gates bestanden; eine veraltete
Quellcode-Assertion scheiterte. Diese Listenaktualisierung repariert sie zugleich;
frische gemeinsame CI ist erforderlich.

**Nachweiskorrektur:** Der zuvor genannte Commit `a6898480` wurde nicht
veröffentlicht. Ihm wird kein Ergebnis zugeschrieben. Die sechs Hostaktionstests
wurden tatsächlich in `5a696b7c` veröffentlicht und bestanden zusammen mit den
acht Runtime-Ausgabetests. Parallele Envoy-Änderungen `31200e8c` und `81e53a94`
wurden erhalten und geprüft.

Referenzen: [Vertrag/Migration](pr-382-event-contract.de.md),
[Haupt-Change-Record](../reports/audits/change-records/CR-20260921-pr382-native-results-events.de.md),
[Routenfortsetzung](../reports/audits/change-records/CR-20260922-pr382-route-completion.de.md),
[gemeinsamer NGINX-Abschluss](../reports/audits/change-records/CR-20260922-pr382-nginx-result-tail.de.md).

## 1. Implementierung

- [x] I01: Operationsspezifische native Prädikate: Byte-Append akzeptiert 0/1, Phasenerfolg nur 1. APR-, NGINX-, HTTP-, Common- und Dateiverträge bleiben getrennt.
- [x] I02: Gemeinsame Prädikate in betroffenen Apache-, HAProxy-, Common-Runtime- und NGINX-Body-Pfaden.
- [x] I03: Common-/HAProxy-Interventionsvalidierung, Bereinigung und Fehlerweitergabe.
- [x] I04: HAProxy-Response-Header-Bindingfehler bleiben bei disruptiven Entscheidungen erhalten.
- [x] I05: Gemeinsame JSONL-/Hash-Sicht erhält Eingabevalidierung, Redaktion, Zähler und echte Beobachtungen.
- [x] I06: Technische Apache-/Common-Fehler bleiben von Regelblockierungen getrennt; handgeschriebene Apache-JSON-Fallbacks entfernt.
- [x] I07: Typisierte NGINX-Antwortfehler; kein erfolgreiches EOS aus einem vor der Auswertung gesetzten Flag ableiten.
- [x] I08: Native Engine-Fehler werden als ungültige Engine-Antwort klassifiziert; andere Fehlerklassen bleiben getrennt.
- [ ] I09: Alle verbleibenden nativen/API-Fehlerausgänge und typisierten Request-Fehlererzeuger der unterstützten Routen abschließen.
- [x] I09a: NGINX-Byte-/Dateitrennung, kumulative Grenzen, Abschluss nur bei Erfolg und terminaler Fehlerwiedereintritt (`fcbaca03`; V13).
- [x] I09b: Typisierte NGINX-Request-Fehler, exakte Interventionsabfrage, erste Ursache/Status und ein Ereignisversuch; gültige leere Bodys bleiben erlaubt (`7fe606c5`; V17).
- [x] I09c: Geprüfter, einmaliger nativer NGINX-Auditabschluss mit erhaltenem Fehler (`47714de0`; V17).
- [x] I09d: Envoy-ext_proc-Brücke erhält ersten Common-Fehler, sperrt fehlerhafte Body-/Header-/EOS-Folgeaufrufe, leert ausstehende Regelentscheidung und begrenzt kanonische Fehlermeldung (`31200e8c`; V22).
- [x] I09e: Ein NGINX-Verbindungs-/URI-Helfer ersetzt doppelten Code bei erhaltenem striktem Phasenerfolg, PCRE-/Phasenklammern und unveränderten Hoststatus (`bced5ce7`; V23).
- [ ] I10: Routenübergreifende Off-/Safe-/Strict-Konsistenz einschließlich tatsächlicher nativer und Hostfehler abschließen.
- [x] I10a: Späte technische NGINX-Fehler werden vor Safe-/Strict-Regelpolicy behandelt (`52445b18`; V14).
- [x] I10b: Echte Common-Policy-Tests prüfen fünf Fehlerklassen, zehn registrierte Profile, zwei Vertragsmodi und beide Commit-Zustände; technische Fehler werden nicht zu erfolgreichem Safe-Log-only. Kein Host-I/O-Nachweis.
- [x] I10c: Echte NGINX-Collector-/Dispatcher-/P4-Kettentests erhalten gültige späte Regeln, Off-Verhalten und Bereinigung (`1ce569e1`; V17).
- [x] I10d: Fehlerhafter Envoy-Antwortbeginn stoppt vor Response-Append; leeres EOS erfindet keinen Body-Start. Geprüfte C-ABI reicht Commitfehler nun an den Go-Aufrufer weiter; Kompatibilitäts-ABI bleibt erhalten (`31200e8c`, `81e53a94`). C-Grenztests bestanden; native Go-Tests bleiben V20.
- [ ] I11: Alle Ereigniserzeuger und physischen Ausgaben angleichen: Kennungen/Ursachen, beobachtete Aktionen, doppelte terminale Ereignisse und Öffnungs-/Schreib-/Kurzschreib-/Serialisierungsfehler.
- [x] I11a: NULL/leere/not_observable-Transportwerte belegen keine Regel-/Fehlerdurchsetzung; unbekannte Datensätze und echte Nachweise bleiben erhalten.
- [x] I11b: Verpflichtende NGINX-Phase-4-Logfehler bleiben terminal; ungültige Ausgaben und wiederholte terminale Schreibversuche sind begrenzt.
- [x] I11c: Gemeinsame fehlende-Beobachtung-Behandlung umfasst Body-Limits, nicht unterstützte Fähigkeiten, Client-Abbruch und Upstream-Disconnect (`3730eaa0`; V18).
- [x] I11d: Runtime erhält ursprünglichen Ereignisfehlercode auch ohne Fehlerausgabe, wiederholt fehlgeschlagene Writes nicht, versteckt sie nicht hinter Abschluss-/Snapshot-Abkürzungen und erhält Hash-Fortschreibungsregeln (`68f78e07`; V21).
- [ ] I12: Jede direkte, Companion-, Middleware- und Sidecar-Route separat einschließlich tatsächlicher Host-/Transport-/Logergebnisse prüfen.
- [x] I12a: Separate ext_proc-C-Brückentests prüfen zehn Fehler-/Wiedereintritts-/Leerantwortfälle (`31200e8c`, erneut `bced5ce7`; V22). Dadurch sind weder ext_authz/Companion noch Live-gRPC abgeschlossen.
- [x] I13: Begrenzter HAProxy-Rule-ID-Dekodierer und geordnete Bereinigung ohne veränderte Phasen-/Besitzsemantik ausgelagert.
- [x] I14: NGINX-Adoption behält alle 96 ursprünglichen Tests plus vier Regressionen.
- [x] I15: HAProxy-Helfer-/Aufrufstellenprüfung und acht isolierte Regressionen erhalten.

### Konkrete verbleibende Grenzen

| Punkt | Verbleibende Arbeit, kein vergessenes Häkchen |
| --- | --- |
| I09 | Apache `process_intervention()` benötigt weiterhin exakte native Rückgabeprüfung und Bereinigung jedes Ausgangs; übrige Initialisierungs-, Audit- und reine Hostdiagnose-Fehlerausgänge samt typisierten Ereignissen prüfen. |
| I10 | Tatsächliche Steuerungswege der übrigen Apache-/HAProxy-/direkten/Companion-/Middleware-Adapter prüfen. Durchsetzung nicht aus Common-Policy oder akzeptierter Strict-Konfiguration ableiten. Ergänzte native Go-Commitment-Tests ausführen. |
| I11 | Apaches void-Ereignisschreiber/-Aufrufer propagieren physische Ausgabefehler noch nicht durch den vollständigen Hostpfad. HAProxy SPOP ignoriert noch sein Common-Event-`fputs()`-Ergebnis. Der alte Runtime-Fehlerklassen-Wiedergabefehler ist behoben und nicht mehr offen. |
| I12 | Getrennte Live-Host-, Commit-, Client-Byte-/Reset- und physische Lognachweise jeder Route vervollständigen. Request-only benötigt seinen tatsächlichen Response-Companion; eine kompilierte Brücke ist kein Live-Host. |

## 2. Verifikation

- [x] V01: Erzeugte C-Rückgabetypen ohne abgeschaltete Warnungen/Assertions repariert.
- [x] V02: Ursprünglicher Native-/Event-Schritt bestand für `4f94f33d`, [Lauf 35627469389](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35627469389).
- [x] V03: Kompilierte native Fehlerklassifikationsregressionen und CI-Anbindung.
- [x] V04: Assertions für terminale Fehler, keine zweite Antwort und keine Erfolgszählung nach fehlgeschlagenem Append erhalten.
- [x] V05: Historische fokussierte Tests bestanden für `092dfd1c`; Nachweise unten erhalten.
- [ ] V06: Sämtliche Adoption-/Mutationstests gemeinsam auf dem finalen Freigabehead abschließen.
- [x] V06a: Apache-Helferprüfungen und 16 Negativmutationen bestanden für `1709e1de`, [Job 106445635579](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35633647191/job/106445635579).
- [x] V06b: Alle 100 NGINX-Adoption-/Mutationstests bestanden für `f7aa2f2c`, `092dfd1c` und `bced5ce7`.
- [ ] V07: Alle finalen Freigabeprüfungen/Reviews; kein vollständig grüner Freigabestatus behauptet.
- [ ] V07a: Unabhängigen Secret-Scan-Fehler ohne unbelegte Fehlalarmeinstufung oder Ausnahme klären; ursprünglicher [Job 106651564952](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35698779824/job/106651564952).
- [ ] V08: Gleiche echte Hostfälle für ProcessPartial/Reject, MIME/CSV, leere/mehrteilige Bodys/EOS, Budgets und native Fehler.
- [ ] V09: Unterstütztes spätes Safe-/Strict-Verhalten, Fehler vor/nach Commit, Client-Bytes, Reset-Grenze, Nachbarstreams und Bereinigung.
- [ ] V10: Echte Routenlogs, ungültige/übergroße Metadaten, fehlende Beobachtungen und fehlgeschlagene physische Ausgaben vergleichen.
- [x] V11: Echte Common-JSONL-/Hash-Beobachtungstests erhalten Nachweise/Redaktion; Familiennamen sind keine Hostläufe.
- [x] V12: Acht kompilierte HAProxy-Helfertests und Binding-Compile-/Link-Prüfungen bestanden für `039b7f12`, [Job 106449767189](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35634888103/job/106449767189).
- [x] V13: Neun NGINX-Request-/Dateitests; kontrollierte native/Host-Grenzen, keine vollständige Dateileser-Integration.
- [x] V14: Neun NGINX-Spätfehler-/Wiedereintrittstests; keine vollständige HTTP-Matrix.
- [x] V15: Acht HAProxy-Rule-ID-Adoption-Regressionen.
- [x] V16: EN/DE-Change-Record-/Vorlagenprüfung bestand erneut, auch für `bced5ce7`.
- [x] V17: NGINX-Request-/Native-Gruppe: 43 Tests einschließlich zehn Collector-Ketten- und acht Audittests bestanden für `bced5ce7`.
- [x] V18: Common-/Native-/Event-/Profilgruppe: 55 Tests einschließlich Beobachtungs-Negativkontrolle und Duplikations-Gate-Unit-Tests bestanden für `bced5ce7`.
- [ ] V19: Helferbewusste Quellcode-Assertion dieser Listenlieferung verifizieren. Für `bced5ce7` scheiterte die alte Verbindungs-/URI-Assertion; sie wurde nicht abgeschaltet.
- [ ] V20: Zwei native Go-/CGo-Commitment-Tests aus `81e53a94` ausführen; geprüfte ABI-/Quellcodepräsenz ist kein Ausführungsnachweis.
- [x] V21: Acht Runtime-Schreib-/Fehlerwiedergabetests plus sechs Hostaktionstests bestanden für `bced5ce7` (zusammen 14).
- [x] V22: Zehn vollständige ext_proc-C-Brückenregressionsfälle bestanden für `bced5ce7`; Common-/native Grenzen sind kontrolliert, echte Netzwerklieferung wird nicht geprüft.
- [x] V23: Sechs neue kompilierte Verbindungs-/URI-Aufrufer- und Helferregressionen bestanden für `bced5ce7`.

## 3. Sonar: null Befunde und null Duplikation

- [x] S01: Nur lesendes exaktes Head-/Anbieter-Gate weist fehlende/veraltete/unfertige/mehrdeutige Ergebnisse zurück.
- [x] S02: Negativtests, begrenzte Diagnosen und eingeschränkte Leseberechtigungen erhalten. Keine Scanner-Ausnahmen, akzeptierten Befunde oder schwächeren Regeln.
- [x] S03: Historische Null-Befunde gelten nur für die jeweilige Revision: `039b7f12`, `91f07e12`, `47714de0`.
- [x] S03a: Exaktes Head-Gate bestand für `f7aa2f2c`.
- [x] S03b: `91f07e12`, [Check 106651947571](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106651947571): null neue/akzeptierte Issues, Hotspots und Annotationen.
- [x] S03c: `47714de0`, [Check 106837589312](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106837589312): dieselben vier Null-Zähler.
- [x] S03d: `bced5ce7`, [Check 106898325037](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106898325037): null neue/akzeptierte Issues, Hotspots und Annotationen; angezeigte Duplikation 0,0 %.
- [ ] S04: Sämtliche finalen Freigabehead-Qualitätsnachweise nach der letzten Lieferung bestätigen; ältere Ergebnisse ersetzen keine spätere SHA.
- [x] S05: Pflicht-Duplikationsgate prüft exakt null neue doppelte Zeilen, Blöcke und Dichte statt nur gerundeter Anzeige. Beide eindeutigen Periodenformate unterstützt; sieben Negativ-/Format-Unit-Tests bestanden.
- [x] S06: Exaktes Duplikationsgate bestand für `bced5ce7` im unten genannten Nachweisjob. Die tatsächlichen doppelten Verbindungs-/URI-Abschlüsse wurden vereinheitlicht, nicht von der Analyse ausgeschlossen.

Dies sind New-Code-Metriken des PRs. Null Befunde/Duplikation beweisen weder null
historische Probleme im gesamten Repository noch einen erledigten Secret-Scan.
Coverage ist eine eigene Kennzahl und wird durch diese Änderung nicht als verbessert ausgegeben.

## 4. Routenbezogener Stand

| Familie / Route | Implementierte oder geprüfte Grenze | Verbleibende Nachweise |
| --- | --- | --- |
| NGINX nativ | Request-/Response-Prädikate, typisierte Fehler, Auditmarker, echte Verbindungs-/URI-Aufrufer, 100 Adoption-Fälle | Vollständige Live-Host-/Transport-/Logmatrix |
| Apache nativ | Body-Prädikate und typisierte Fehler | Exakte Interventionsrückgabe/Bereinigung, vollständige physische Fehlerweitergabe, Live-Host-Matrix |
| HAProxy HTX | Binding-Prädikate und Helfer-/Adoption-Tests | Direkte Hoststeuerung, Reset/Abort und Logfehler |
| HAProxy SPOE/SPOP + Companion | Gemeinsame/native Body-Rückgabeverträge | Physisches SPOP-Schreibergebnis und getrennte Companion-/Transportnachweise |
| Envoy ext_proc | C-Brücken-Fehlermarker, geprüfter Antwortbeginn, Leerbody-Metadaten; Go verwendet geprüfte ABI | Native Go-Tests und echte gRPC-/Host-/Logergebnisse |
| Envoy ext_authz + Companion | Gemeinsame Runtime-Prädikat-/Fehlerwiedergabekorrekturen | Getrennte Request-/Response-Companion- und Log-/Transportnachweise |
| Traefik Middleware/UDS | Gemeinsame Runtime-Prädikat-/Fehlerwiedergabekorrekturen | Middleware-/UDS-Hostfehler und physische Ausgaben |
| Traefik forwardAuth + Companion | Gemeinsame Runtime-Prädikat-/Fehlerwiedergabekorrekturen | Getrennte Companion-Lebenszyklus-/Steuerungs-/Lognachweise |
| lighttpd Sidecar | Gemeinsame Runtime-Prädikat-/Fehlerwiedergabekorrekturen | Physische Ausgaben und echtes Socket-/Hostverhalten |
| lighttpd native/gepatchte Profile | Gemeinsame Verträge bei Runtime-Anbindung | Getrennte Hook-Verfügbarkeit, Ablehnung nicht unterstützter Strict-Modi und native Hostnachweise |

Nicht unterstützte Strict-Profile werden weder still aktiviert noch als erfolgreiches
Log-only behandelt. Gemeinsame Semantik bedeutet keine gleichen Hostzahlen oder erfundenen Fähigkeiten.

## 5. Dokumentation und Lieferung

- [x] D01: Bestehender Draft-PR; kein Merge/Master-/Force-Push.
- [x] D02: Zweisprachige EN/DE-Checkliste mit getrennter Implementierung und Verifikation.
- [ ] D03: Alle Connector-Anleitungen/Beispiele und Kompatibilitäts-/Versionsprüfung abschließen.
- [x] D03a: Zweisprachiger Vertrag und Auswerter-/Hash-Migrationswarnungen erhalten.
- [x] D04: Aktuellen Code, Tests und verbleibende Grenzen abgeglichen; behobenen Runtime-Wiedergabefehler aus offenen Aufgaben entfernt und unveröffentlichte Commitbehauptung korrigiert.
- [ ] D05: Finale Freigabehead-Dokumentations-/Link-/Diff-/CI-Prüfungen und PR-/Branch-Abgleich.

## Revisionsgebundene Nachweise

[Job 106897813154](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35772630849/job/106897813154)
für `bced5ce78c62b7665730d2e81b307a3676da42f3` bestand die fokussierten
55/14/10/6/43/9-Testgruppen, alle 100 NGINX- und acht HAProxy-Adoption-Fälle,
Konfigurationsprüfungen, Zweisprachigkeit und beide exakten Sonar-Gates. Die alte
Quellcode-Assertion erwartete Inline-Verbindungs-/URI-Verzweigungen und scheiterte.
Diese Lieferung prüft gemeinsame native Fehlerzweige, Host-Ergebnisse und beide
Aufrufreihenfolgen ausdrücklich; die übrigen bisherigen Negativpfade bleiben
geprüft. Kombinierte Quellcodegruppe und Lightweight-Lint benötigen daher einen
frischen Lauf (V19).

Ältere Nachweise bleiben in [der Checkliste bei 0532b5eb](https://github.com/Easton97-Jens/ModSecurity-conector/blob/0532b5eb6dac5840b482dbc936ae1cf7a7ccbeb9/docs/pr-382-checklist.de.md),
[historischem Job 106648735070](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35697893254/job/106648735070)
und den verlinkten Change Records erhalten. Vorbereitende offene Prüfvermerke
werden ausschließlich für die hier explizit genannte Revision/Testebene ersetzt.

Keine lokalen Projektbefehle/Builds oder Git-Diff-Prüfungen ohne vorgeschriebenen
RTK-Wrapper. Tatsächliche GitHub-CI und Commitvergleiche liefern die genannten Nachweise.
