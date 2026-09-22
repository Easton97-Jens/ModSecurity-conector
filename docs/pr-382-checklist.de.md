# PR #382: Checkliste für gemeinsames Connector-Verhalten

**Sprache:** [English](pr-382-checklist.md) | Deutsch

[Draft-PR #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382),
Branch `fix/unified-native-results-events-20260921`, Basis
`5170d24801243cdcd7bf1bca6123bf8cb2c72386`. Aktualisiert: 2026-09-22.

**Gesamtimplementierung unvollständig; nicht zum Mergen bereit.** Implementierung,
kompilierte Grenztests und echte Live-Routen sind getrennte Nachweise.
Letzter Code-/Test-Prüfstand: `b91b68269027a3c5602b5624058df9e1f865535e`.
Die reparierte Quellcode-/Sicherheitsgruppe bestand dort (V19). Der folgende
Dokumentationscommit braucht eigene Checks; ältere Sonar-Ergebnisse ersetzen sie nicht.

**Nachweiskorrektur:** `a6898480` wurde nicht veröffentlicht und besitzt keine
Test-/Sonar-Nachweise. Die sechs Hostaktionstests wurden tatsächlich in `5a696b7c`
veröffentlicht. Parallele Envoy-Änderungen `31200e8c` und `81e53a94` blieben erhalten.

Referenzen: [Vertrag/Migration](pr-382-event-contract.de.md),
[Haupt-Change-Record](../reports/audits/change-records/CR-20260921-pr382-native-results-events.de.md),
[Routenfortsetzung](../reports/audits/change-records/CR-20260922-pr382-route-completion.de.md),
[gemeinsamer NGINX-Abschluss](../reports/audits/change-records/CR-20260922-pr382-nginx-result-tail.de.md).

## 1. Implementierung

- [x] I01: Natives Byte-Append akzeptiert 0/1, Phasenerfolg nur 1. APR-, NGINX-, HTTP-, Common- und Dateiverträge bleiben getrennt.
- [x] I02: Gemeinsame Prädikate in betroffenen Apache-, HAProxy-, Common-Runtime- und NGINX-Body-Pfaden.
- [x] I03: Common-/HAProxy-Interventionsvalidierung, Bereinigung und Fehlerweitergabe.
- [x] I04: HAProxy-Response-Header-Bindingfehler bleiben bei disruptiven Entscheidungen erhalten.
- [x] I05: Gemeinsame JSONL-/Hash-Sicht erhält Eingabevalidierung, Redaktion, Zähler und echte Beobachtungen.
- [x] I06: Technische Apache-/Common-Fehler bleiben von Regelblockierungen getrennt; handgeschriebene Apache-JSON-Fallbacks entfernt.
- [x] I07: Typisierte NGINX-Antwortfehler; kein erfolgreiches EOS vor der Auswertung ableiten.
- [x] I08: Native Engine-Fehler werden als ungültige Engine-Antwort klassifiziert; andere Klassen bleiben getrennt.
- [ ] I09: Verbleibende native/API-Ausgänge und typisierte Request-Fehlererzeuger aller unterstützten Routen abschließen.
- [x] I09a: NGINX-Byte-/Dateitrennung, kumulative Grenzen, Erfolgsvoraussetzung und terminaler Fehlerwiedereintritt (`fcbaca03`; V13).
- [x] I09b: Typisierte NGINX-Request-Fehler, exakte Interventionsabfrage, erste Ursache/Status und ein Ereignisversuch; leere Bodys bleiben erlaubt (`7fe606c5`; V17).
- [x] I09c: Geprüfter, einmaliger nativer NGINX-Auditabschluss mit erhaltenem Fehler (`47714de0`; V17).
- [x] I09d: Envoy ext_proc erhält ersten Common-Fehler, sperrt fehlerhafte Header-/Body-/EOS-Folgeaufrufe, leert ausstehende Regelentscheidungen und begrenzt kanonische Fehlermeldung (`31200e8c`; V22).
- [x] I09e: Gemeinsamer NGINX-Verbindungs-/URI-Helfer erhält strikten Erfolg, PCRE-/Phasenklammern und Hoststatus ohne doppelte Implementierung (`bced5ce7`; V23).
- [ ] I10: Tatsächliche routenübergreifende Off-/Safe-/Strict-Behandlung einschließlich nativer und Hostfehler abschließen.
- [x] I10a: Späte technische NGINX-Fehler kommen vor Safe-/Strict-Regelpolicy (`52445b18`; V14).
- [x] I10b: Echte Common-Policy-Tests prüfen fünf Fehlerklassen, zehn Profile, zwei Vertragsmodi und beide Commit-Zustände; technische Fehler werden kein Safe-Log-only. Kein Host-I/O-Nachweis.
- [x] I10c: Echte NGINX-Collector-/Dispatcher-/P4-Kettentests erhalten späte Regeln, Off-Verhalten und Bereinigung (`1ce569e1`; V17).
- [x] I10d: Fehlerhafter Envoy-Antwortbeginn stoppt vor Append; leeres EOS erfindet keinen Body-Start. Geprüfte C-ABI reicht Fehler an Go weiter, Kompatibilitäts-ABI bleibt erhalten (`31200e8c`, `81e53a94`). C-Tests bestanden; native Go-Ausführung bleibt V20.
- [ ] I11: Erzeuger-/Ausgabeparität, Kennungen/Ursachen, beobachtete Aktionen, doppelte terminale Ereignisse und Öffnungs-/Schreib-/Kurzschreib-/Serialisierungsfehler abschließen.
- [x] I11a: Fehlende Transportbeobachtungen belegen keine Regel-/Fehlerdurchsetzung; eigene Datensätze und echte Nachweise bleiben erhalten.
- [x] I11b: Verpflichtende NGINX-Phase-4-Logfehler bleiben terminal; ungültige Ausgaben und wiederholte terminale Writes sind begrenzt.
- [x] I11c: Fehlende-Beobachtung-Behandlung umfasst Body-Limits, nicht unterstützte Fähigkeiten, Abbruch und Upstream-Disconnect (`3730eaa0`; V18).
- [x] I11d: Runtime erhält ursprünglichen Ereignisfehler auch ohne Fehlerausgabe, verhindert Write-Wiederholung und Abschluss-/Snapshot-Verdeckung und erhält Hash-Fortschreibungsregeln (`68f78e07`; V21).
- [ ] I12: Jede direkte, Companion-, Middleware- und Sidecar-Route separat samt echten Host-/Transport-/Logergebnissen prüfen.
- [x] I12a: Zehn separate ext_proc-C-Brückenfälle für Fehler, Wiedereintritt und Leerantwort bestehen (V22). Dies erledigt weder ext_authz/Companion noch Live-gRPC.
- [x] I13: Begrenzter HAProxy-Rule-ID-Dekodierer und geordnete Bereinigung ohne geänderte Phasen-/Besitzsemantik ausgelagert.
- [x] I14: Alle 96 ursprünglichen NGINX-Adoption-Fälle plus vier Regressionen erhalten.
- [x] I15: HAProxy-Helfer-/Aufrufstellenprüfung und acht isolierte Regressionen erhalten.

### Konkrete verbleibende Grenzen

| Punkt | Erforderliche Arbeit, kein vergessenes Häkchen |
| --- | --- |
| I09 | Apache `process_intervention()` benötigt exakte native Rückgabeprüfung und Bereinigung jedes Ausgangs. Übrige Initialisierungs-/Audit-/Hostdiagnose-Fehler und typisierte Erzeuger prüfen. |
| I10 | Nachweisen, dass übrige native/Companion-/Middleware-Fehler den echten Host-Steuerungspfad ohne erfolgreichen Rückfall erreichen. Native Go-Commitment-Tests ausführen. |
| I11 | Apaches void-Ereignisschreiber/-Aufrufer reichen physische Fehler noch nicht vollständig weiter. HAProxy SPOP ignoriert noch sein Common-Event-`fputs()`-Ergebnis. Der alte Runtime-Wiedergabefehler ist behoben, nicht offen. |
| I12 | Getrennte Live-Host-, Client-Byte-/Reset- und physische Lognachweise vervollständigen. Request-only braucht seinen Response-Companion; eine kompilierte Brücke ist kein Live-Host. |

## 2. Verifikation

- [x] V01: Erzeugte C-Rückgabetypen ohne abgeschaltete Warnungen/Assertions repariert.
- [x] V02: Ursprünglicher Native-/Event-Schritt bestand für `4f94f33d`, [Lauf 35627469389](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35627469389).
- [x] V03: Kompilierte native Fehlerklassifikationsregressionen und Pflicht-CI.
- [x] V04: Terminale Fehler, keine zweite Antwort und keine Erfolgszählung nach Append-Fehlern bleiben geprüft.
- [x] V05: Historische fokussierte Tests bestanden für `092dfd1c`; Nachweise unten erhalten.
- [ ] V06: Sämtliche Adoption-/Mutationstests auf finalem Freigabehead abschließen.
- [x] V06a: Apache-Helfer und 16 Negativmutationen bestanden für `1709e1de`, [Job 106445635579](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35633647191/job/106445635579).
- [x] V06b: Alle 100 NGINX-Adoption-/Mutationstests bestanden für `f7aa2f2c`, `092dfd1c` und `bced5ce7`.
- [ ] V07: Alle finalen Freigabeprüfungen/Reviews; keine vollständig grüne Freigabe-CI behauptet.
- [ ] V07a: Unabhängigen Secret-Scan ohne unbelegte Ausnahme klären; ursprünglicher [Job 106651564952](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35698779824/job/106651564952). Workflow scheitert auch für `b91b6826`.
- [ ] V08: Echte Hostfälle für ProcessPartial/Reject, MIME/CSV, leere/mehrteilige Bodys/EOS, Budgets und native Fehler.
- [ ] V09: Spätes Safe/Strict, Fehler vor/nach Commit, Client-Bytes, Reset-Grenze, Nachbarstreams und Bereinigung.
- [ ] V10: Echte Routenlogs, ungültige/übergroße Metadaten, fehlende Beobachtungen und fehlerhafte physische Ausgaben.
- [x] V11: Echte Common-JSONL-/Hash-Tests erhalten Nachweise/Redaktion; Familiennamen sind keine Hostläufe.
- [x] V12: Acht kompilierte HAProxy-Helfertests und Binding-Compile/Link bestanden für `039b7f12`, [Job 106449767189](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35634888103/job/106449767189).
- [x] V13: Neun NGINX-Request-/Dateitests mit kontrollierten Grenzen, keine vollständige Dateileser-Integration.
- [x] V14: Neun NGINX-Spätfehler-/Wiedereintrittstests, keine vollständige HTTP-Matrix.
- [x] V15: Acht HAProxy-Rule-ID-Adoption-Regressionen.
- [x] V16: Zweisprachigkeits-/Vorlagenprüfung bestand für `bced5ce7` und `b91b6826`.
- [x] V17: 43 NGINX-Request-/Native-Tests einschließlich zehn Collector- und acht Auditfällen bestanden für `b91b6826`.
- [x] V18: 55 Common-/Native-/Event-/Profilfälle samt Beobachtungs- und Duplikations-Gate-Tests bestanden für `b91b6826`.
- [x] V19: Helferbewusste Quellcode-/Sicherheitsreparatur bestand für `b91b6826`. Beide Aufrufreihenfolgen, exakte native Fehler und Hostrückgaben bleiben geprüft; andere bisherige Negativpfade wurden nicht entfernt.
- [ ] V20: Zwei native Go-/CGo-Commitment-Tests aus `81e53a94` ausführen. Der `test-envoy`-Vertragsworkflow führt sie nicht aus; Quellcode-/ABI-Präsenz ist kein Ausführungsnachweis.
- [x] V21: Acht Runtime-Ausgabe-/Wiedergabe- plus sechs Hostaktionstests bestanden für `b91b6826` (14 insgesamt).
- [x] V22: Zehn vollständige ext_proc-C-Brückentests bestanden für `b91b6826`; kontrollierte Common-/native Grenzen, kein Live-gRPC-/physischer Lognachweis.
- [x] V23: Sechs kompilierte Verbindungs-/URI-Aufrufer-/Helferregressionen bestanden für `b91b6826`.

## 3. Sonar: null Befunde und null Duplikation

- [x] S01: Nur lesendes exaktes Head-/Anbieter-Gate weist fehlende/veraltete/unfertige/mehrdeutige Nachweise zurück.
- [x] S02: Negativtests, begrenzte Diagnosen und eingeschränkte Leserechte erhalten; keine Scanner-Ausnahmen, akzeptierten Befunde oder schwächeren Regeln.
- [x] S03: Historische Null-Zähler bleiben revisionsgebunden: `039b7f12`, `91f07e12`, `47714de0`.
- [x] S03a: Exaktes Head-Gate bestand für `f7aa2f2c`.
- [x] S03b: `91f07e12`, [Check 106651947571](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106651947571): null neue/akzeptierte Issues, Hotspots und Annotationen.
- [x] S03c: `47714de0`, [Check 106837589312](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106837589312): dieselben vier Null-Zähler.
- [x] S03d: `bced5ce7`, [Check 106898325037](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106898325037): dieselben Null-Zähler und angezeigte Duplikation 0,0 %.
- [ ] S04: Finale Freigabehead-Qualität nach letzter Lieferung bestätigen; ältere Analysen ersetzen keine spätere SHA.
- [x] S05: Pflicht-Duplikationsgate verlangt exakt null neue doppelte Zeilen, Blöcke und Dichte; fehlende/gerundete Werte reichen nicht. Sieben Format-/Negativtests bestehen.
- [x] S06: Exaktes Duplikationsgate bestand für `bced5ce7` in [Job 106897813154](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35772630849/job/106897813154). Echte Verbindungs-/URI-Logik wurde gemeinsam implementiert, nicht ausgeschlossen.

Dies sind New-Code-Metriken des PRs, kein Nachweis für null historische Probleme.
Coverage und unabhängiger Secret-Scan bleiben von Sonar-Befunden/Duplikation getrennt.

## 4. Routenbezogener Stand

| Familie / Route | Implementierte oder geprüfte Grenze | Verbleibende Nachweise |
| --- | --- | --- |
| NGINX nativ | Typisierte Fehler, Prädikate, Auditmarker, Verbindungs-/URI-Aufrufer, Adoption | Vollständige Live-Host-/Transport-/Logmatrix |
| Apache nativ | Body-Prädikate und typisierte Fehler | Exakte Interventionsrückgaben/Bereinigung, physische Ausgaben, Hostmatrix |
| HAProxy HTX | Binding-Prädikate und Helfer-/Adoption-Tests | Direkte Hostfehler-/Reset-/Abort-/Logfälle |
| HAProxy SPOE/SPOP + Companion | Common-/native Rückgabeverträge | Physische SPOP-Writes und eigene Companion-/Transportnachweise |
| Envoy ext_proc | Erste Fehlerursache, geprüfter Antwortbeginn, korrekte Leerbody-Metadaten; Go nutzt geprüfte ABI | Native Go- und echte gRPC-/Host-/Lognachweise |
| Envoy ext_authz + Companion | Gemeinsame Runtime-Prädikat-/Wiedergabekorrekturen | Getrennte Request-/Response-Companion-, Log- und Transportnachweise |
| Traefik Middleware/UDS | Gemeinsame Runtime-Korrekturen | Middleware-/UDS-Hostfehler und physische Ausgaben |
| Traefik forwardAuth + Companion | Gemeinsame Runtime-Korrekturen | Getrennte Companion-Lebenszyklus-/Steuerungs-/Lognachweise |
| lighttpd Sidecar | Gemeinsame Runtime-Korrekturen | Physische Ausgaben und echtes Socket-/Hostverhalten |
| lighttpd native/gepatchte Profile | Gemeinsame Verträge bei Runtime-Anbindung | Eigene Hooks, Ablehnung nicht unterstützter Strict-Modi und native Hostnachweise |

Nicht unterstützte Strict-Profile bleiben nicht unterstützt. Gleiche Semantik
bedeutet keine gleichen Hostzahlen oder erfundenen Abort-/Resetfähigkeiten.

## 5. Dokumentation und Lieferung

- [x] D01: Bestehender Draft-PR; kein Merge/Master-/Force-Push.
- [x] D02: Zweisprachige Checkliste trennt Implementierung und Verifikation.
- [ ] D03: Connector-Anleitungen/Beispiele und Kompatibilitäts-/Versionsprüfung abschließen.
- [x] D03a: Zweisprachiger Vertrag und Auswerter-/Hash-Migrationswarnungen erhalten.
- [x] D04: Quelltext/Tests abgeglichen, unveröffentlichte Lieferung richtiggestellt und behobenen Runtime-Wiedergabefehler aus offenen Aufgaben entfernt.
- [ ] D05: Finale Freigabe-Dokumentations-/Link-/Diff-/CI-Prüfung und PR-/Branch-Abgleich.

## Revisionsgebundene Nachweise

[Job 106900742683](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35773496921/job/106900742683)
für `b91b68269027a3c5602b5624058df9e1f865535e` bestand bei der Abfrage die
Zweisprachigkeit, fokussierte 55/14/10/6/43/9-Gruppen und reparierte Quellcode-/
Sicherheitsprüfung. Weitere Schritte liefen noch; kein Gesamtjob-Erfolg wird daraus abgeleitet.
Der vorherige [Job 106897813154](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35772630849/job/106897813154)
für `bced5ce7` bestand 100 NGINX-/acht HAProxy-Adoption-Fälle, Konfigurationschecks
und beide Sonar-Gates, scheiterte aber an der alten Quellcode-Assertion. V19 ersetzt
diesen konkreten Fehler, nicht andere Freigabe- oder Live-Routenanforderungen.

Historische Details bleiben in [der Liste bei 0532b5eb](https://github.com/Easton97-Jens/ModSecurity-conector/blob/0532b5eb6dac5840b482dbc936ae1cf7a7ccbeb9/docs/pr-382-checklist.de.md),
[historischem Job 106648735070](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35697893254/job/106648735070)
und verlinkten Change Records erhalten. Vorbereitende offene Vermerke werden nur
für die ausdrücklich benannte Revision und Testebene ersetzt.

Kein lokaler Projektbefehl/Build oder Git-Diff-Check umging den fehlenden Pflicht-
RTK-Wrapper. Tatsächliche GitHub-CI und Commitvergleiche liefern diese Nachweise.
