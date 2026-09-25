# PR #382: Checkliste für gemeinsames Connector-Verhalten

**Sprache:** [English](pr-382-checklist.md) | Deutsch

[Draft-PR #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382),
Branch `fix/unified-native-results-events-20260921`, Basis
`5170d24801243cdcd7bf1bca6123bf8cb2c72386`. Aktualisiert: 2026-09-23.

**Bei I09 und I10 fehlt noch mehr als der Live-Host-Nachweis.** Fertiger Code,
ausgeführte kompilierte Tests, offene native Tests und echte Hostnachweise bleiben
getrennt. Der Apache-Modulteil ist inzwischen implementiert und darf nicht weiter
als unbearbeiteter Interventions-/Initialisierungs-/Auditfehler aufgeführt werden.

Neueste veröffentlichte Testreparatur: `7d05e89fc12dca64c7129553d0c83157e956e0f3`.
Sonar bestätigt dafür null Befunde und angezeigte 0,0 % neue Duplikation.
Sein vollständiger nativer Envoy-Job bestand inzwischen einschließlich echtem
Common/libModSecurity und Go-Tests mit libmodsecurity-Buildtag (V20/V25).
Datumsfelder und zweisprachige Checkliste bestanden für `b92459ba` die unveränderte
Prüfung (V26). Diese revisionsgebundenen Ergebnisse gelten nicht automatisch für
diese spätere reine Nachweisaktualisierung.

Nachweiskorrektur: `a6898480` wurde nie veröffentlicht; behauptete Ergebnisse
werden nicht verwendet. Historische Nachweise gelten nur für ihre Revision und
Testebene. Die sechs Hostaktionstests wurden tatsächlich in `5a696b7c` geliefert.

Referenzen: [Vertrag/Migration](pr-382-event-contract.de.md),
[Haupt-Change-Record](../reports/audits/change-records/CR-20260921-pr382-native-results-events.de.md),
[Apache-Lebenszyklus](../reports/audits/change-records/CR-20260923-pr382-apache-native-lifecycle.de.md),
[Apache-Adoption](../reports/audits/change-records/CR-20260923-pr382-apache-adoption.de.md),
[native Envoy-Testreparatur](../reports/audits/change-records/CR-20260923-pr382-envoy-test-boundaries.de.md).

## 1. Implementierung

- [x] I01: Natives Byte-Append akzeptiert 0/1, Phasenerfolg nur 1. APR-, NGINX-, HTTP-, Common- und Dateiverträge bleiben getrennt.
- [x] I02: Gemeinsame Prädikate in betroffenen Apache-, HAProxy-, Common-Runtime- und NGINX-Body-Pfaden.
- [x] I03: Common-/HAProxy-Interventionsvalidierung, Bereinigung und Fehlerweitergabe.
- [x] I04: HAProxy-Response-Header-Bindingfehler bleiben bei disruptiven Entscheidungen erhalten.
- [x] I05: Gemeinsame JSONL-/Hash-Sicht erhält Eingabevalidierung, Redaktion, Zähler und echte Beobachtungen.
- [x] I06: Technische Apache-/Common-Fehler bleiben von Regelblockierungen getrennt; handgeschriebene JSON-Fallbacks entfernt.
- [x] I07: Typisierte NGINX-Antwortfehler; kein erfolgreiches EOS vor Auswertung ableiten.
- [x] I08: Native Engine-Fehler werden als ungültige Engine-Antwort klassifiziert; andere Klassen bleiben getrennt.
- [ ] I09: Verbleibende native/API- und typisierte Fehlerpfade jeder Route prüfen, daraus folgende Implementierungslücken beheben und gemeinsame native Verifikation abschließen.
- [x] I09a: NGINX-Byte-/Dateitrennung, kumulative Grenzen, Erfolgsvoraussetzung und terminaler Wiedereintritt (`fcbaca03`; V13).
- [x] I09b: Typisierte NGINX-Request-Fehler, exakte Interventionsabfrage, erste Ursache/Status und einmaliger Ereignisversuch; leere Bodys bleiben gültig (`7fe606c5`; V17).
- [x] I09c: Geprüfter, einmaliger nativer NGINX-Auditabschluss mit erhaltenem Fehler (`47714de0`; V17).
- [x] I09d: Envoy ext_proc erhält erste Common-Fehler, sperrt Header-/Body-/EOS-Wiederholungen, leert alte Regelmetadaten und begrenzt Fehlermeldung (`31200e8c`; V22).
- [x] I09e: Gemeinsamer NGINX-Verbindungs-/URI-Helfer erhält strikten Erfolg, PCRE-/Phasenklammern und Hoststatus ohne doppelte Implementierung (`bced5ce7`; V23).
- [x] I09f: Apache-Modul prüft exakte Interventionsrückgaben, gibt native Puffer auf jedem Ausgang nach dem Aufruf frei, prüft Kopien, trennt native/Host-Ursachen, prüft Initialisierung und bindet Engine-Cleanup an die Konfigurationsgeneration. Für `3c29004b` vorhanden und getestet; V24.
- [ ] I10: Tatsächliche Off-/Safe-/Strict-Fehlerbehandlung aller Routen einschließlich nativer Integrationsverifikation abschließen, nicht nur gemeinsame Policy-Tests.
- [x] I10a: Späte technische NGINX-Fehler kommen vor Safe-/Strict-Regelpolicy (`52445b18`; V14).
- [x] I10b: Echte Common-Policy-Tests prüfen fünf Fehlerklassen, zehn Profile, zwei Vertragsmodi und beide Commit-Zustände; technische Fehler werden kein Safe-Log-only. Kein Host-I/O-Nachweis.
- [x] I10c: Echte NGINX-Collector-/Dispatcher-/P4-Kettentests erhalten späte Regeln, Off-Verhalten und Bereinigung (`1ce569e1`; V17).
- [x] I10d: Fehlerhafter Envoy-Antwortbeginn stoppt vor Append; leeres EOS erfindet keinen Bodybeginn. Geprüfte C-ABI reicht Fehler bis Go weiter; Kompatibilitäts-ABI bleibt erhalten (`31200e8c`, `81e53a94`). Native Verifikation bestand für `7d05e89f` (V20).
- [x] I10e: Apache-Collector ändert keine bereits gesendeten Location-Header und verwendet bei technischen Fehlern keine alten Regelmetadaten. Audit markiert seinen Versuch vor Callbacks und setzt keine ausführbare Intervention aus der Logphase durch. Für `3c29004b` vorhanden; V24 prüft kompilierte APR-/native Grenzen, kein Live-httpd.
- [ ] I11: Erzeuger-/Ausgabeparität, Kennungen/Ursachen, beobachtete Aktionen, doppelte terminale Ereignisse und Öffnungs-/Schreib-/Kurzschreib-/Serialisierungsfehler abschließen.
- [x] I11a: Fehlende Transportbeobachtungen belegen keine Regel-/Fehlerdurchsetzung; eigene Datensätze und tatsächliche Nachweise bleiben erhalten.
- [x] I11b: Verpflichtende NGINX-Phase-4-Logfehler bleiben terminal; ungültige Ausgaben und wiederholte Writes sind begrenzt.
- [x] I11c: Fehlende-Beobachtung-Behandlung umfasst Body-Limits, nicht unterstützte Fähigkeiten, Abbruch und Upstream-Disconnect (`3730eaa0`; V18).
- [x] I11d: Runtime erhält erste Ereignisfehler ohne Ausgabepointer, verhindert Write-Wiederholung und Abschluss-/Snapshot-Verdeckung und erhält Hash-Regeln (`68f78e07`; V21).
- [ ] I12: Jede direkte, Companion-, Middleware- und Sidecar-Route getrennt samt echten Host-/Transport-/Logergebnissen prüfen.
- [x] I12a: Zehn separate ext_proc-C-Brückenfälle für Fehler, Wiedereintritt und Leerantwort bestehen (V22); kein Abschluss von ext_authz/Companion oder Live-gRPC.
- [x] I13: Begrenzter HAProxy-Rule-ID-Dekodierer und geordnete Bereinigung ohne geänderte Phasen-/Besitzsemantik ausgelagert.
- [x] I14: Alle 96 ursprünglichen NGINX-Adoption-Fälle plus vier Regressionen erhalten.
- [x] I15: HAProxy-Helfer-/Aufrufstellenprüfung und acht isolierte Regressionen erhalten.

### Was vor „nur Hostnachweis fehlt“ noch nötig ist

| Punkt | Verbleibende Anforderung |
| --- | --- |
| I09 | Filter-/API-Ausgänge außerhalb des fertigen Apache-Moduls und übrige HAProxy-, direkte, Companion- und Middleware-Erzeuger prüfen. Jeden Fehler durch tatsächliche Aufrufer und Cleanup verfolgen; gemeinsame Prädikate oder Diagnosen allein reichen nicht. Die obigen Apache-Collector-/Init-/Auditkorrekturen sind nicht mehr offen. |
| I10 | Fehlerweitergabe jeder verbleibenden Route bis zur Hoststeuerung einschließlich Fehlern nach Antwortbeginn prüfen. Native Envoy-Verifikation ist jetzt unter V20 abgeschlossen, keine offene Voraussetzung mehr. Fehlende Prüfungen in einem Helfer allein beweisen keinen Fehler, wenn Common bereits weitere Aufrufe verhindert. |
| I11 | Apaches void-Ereignisschreiber/-Aufrufer brauchen vollständige physische Fehlerweitergabe; HAProxy SPOP muss sein Common-Event-fputs-Ergebnis behandeln. Der ursprüngliche Runtime-I/O-Wiedergabefehler ist behoben. Dies bleibt Implementierungsarbeit, nicht bloß Live-Nachweis. |
| I12 | Routebezogene Host-, Client-Byte-/Reset-, Nachbarstream-, Cleanup- und physische Logfälle ausführen. Request-only benötigt seinen wirklichen Response-Companion. |

## 2. Verifikation

- [x] V01: Erzeugte C-Rückgabetypen ohne abgeschaltete Warnungen/Assertions repariert.
- [x] V02: Ursprünglicher Native-/Event-Schritt bestand für `4f94f33d`, [Lauf 35627469389](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35627469389).
- [x] V03: Kompilierte native Fehlerklassifikationsregressionen und Pflicht-CI.
- [x] V04: Terminale Fehler, keine zweite Antwort und keine Erfolgszählung nach Append-Fehlern bleiben geprüft.
- [x] V05: Historische fokussierte Tests bestanden für `092dfd1c`; Nachweise unten erhalten.
- [ ] V06: Sämtliche Adoption-/Mutationstests auf finalem Freigabehead abschließen.
- [x] V06a: Historische Apache-Helfer und 16 Negativmutationen bestanden für `1709e1de`; neue 25-Fall-Prüfung siehe V24.
- [x] V06b: Alle 100 NGINX-Adoption-/Mutationstests bestanden für `f7aa2f2c`, `092dfd1c` und `bced5ce7`.
- [ ] V07: Alle finalen Freigabeprüfungen/Reviews; keine vollständig grüne Freigabe-CI behauptet.
- [ ] V07a: Unabhängigen Secret-Scan ohne unbelegte Ausnahme klären. Der [Workflow für 7d05e89f](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35896111802) scheitert weiterhin.
- [ ] V08: Echte Hostfälle für ProcessPartial/Reject, MIME/CSV, leere/mehrteilige Bodys/EOS, Budgets und native Fehler.
- [ ] V09: Spätes Safe/Strict, Fehler vor/nach Commit, Client-Bytes, Reset-Grenze, Nachbarstreams und Bereinigung.
- [ ] V10: Echte Routenlogs, ungültige/übergroße Metadaten, fehlende Beobachtungen und fehlerhafte physische Ausgaben.
- [x] V11: Echte Common-JSONL-/Hash-Tests erhalten Nachweise/Redaktion; Familiennamen sind keine Hostläufe.
- [x] V12: Acht kompilierte HAProxy-Helfertests und Binding-Compile/Link bestanden für `039b7f12`.
- [x] V13: Neun NGINX-Request-/Dateitests mit kontrollierten Grenzen, keine vollständige Dateileser-Integration.
- [x] V14: Neun NGINX-Spätfehler-/Wiedereintrittstests, keine vollständige HTTP-Matrix.
- [x] V15: Acht HAProxy-Rule-ID-Adoption-Fälle.
- [x] V16: Historische Zweisprachigkeits-/Vorlagenprüfung bestand für `bced5ce7` und `b91b6826`; neuere Apache-Berichtsreparatur ist V26, kein geerbter Erfolg.
- [x] V17: 43 NGINX-Request-/Native-Fälle einschließlich zehn Collector- und acht Auditfällen bestanden für `b91b6826`.
- [x] V18: 55 Common-/Native-/Event-/Profilfälle bestanden für `b91b6826`.
- [x] V19: Helferbewusste Quellcode-/Sicherheitsreparatur bestand für `b91b6826`, ohne andere Negativpfade zu entfernen.
- [x] V20: [Nativer Envoy-Job 107300314663](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35896111748/job/107300314663) bestand für exakt `7d05e89f`, einschließlich echtem Common/libModSecurity-Build und `go test -mod=readonly -tags libmodsecurity -count=1 ./...`. Beide geprüften Commitment-Fälle sind enthalten; kein bloßer Quellcode-/Vorabcheck.
- [x] V21: Acht Runtime-Ausgabe-/Wiedergabe- plus sechs Hostaktionstests bestanden für `b91b6826` (14 insgesamt).
- [x] V22: Zehn vollständige ext_proc-C-Brückenfälle bestanden für `b91b6826`; kontrollierte Common-/native Grenzen, kein Live-Transportnachweis.
- [x] V23: Sechs kompilierte Verbindungs-/URI-Aufrufer-/Helferfälle bestanden für `b91b6826`.
- [x] V24: Für `3c29004b` bestand der [native Apache-Job 107137107158](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35847504774/job/107137107158) die 20 kompilierten Lifecycle-Fälle und Bootstrap. [Strukturjob 107137106792](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35847504774/job/107137106792) bestand 25 Adoption-/Mutationsfälle und scheiterte erst an getrennt fehlenden Berichtsdatumsfeldern.
- [x] V25a: `7d05e89f` enthält native Testreparaturen: getrennte gültige 413- und terminale ungültige Bestätigungsfälle, explizit unsichere Dateirechte und erhaltene ursprüngliche Inode. Produktivschutz und bestehende Positivkontrollen bleiben unverändert.
- [x] V25: Die native Go-Suite aus V20 bestand die V25a-Reparaturen einschließlich erster Fehlerursache und unveränderter Ereignisbytes nach fehlgeschlagenen Wiederholungen. Der ursprüngliche fehlgeschlagene Lauf bleibt als Regressionsbaseline erhalten.
- [x] V26: [Lint-Job 107304638636](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35897399419/job/107304638636) bestand für `b92459ba` den unveränderten Zweisprachigkeitsvalidator; beide Datumsfelder und die Checkliste sind bestätigt. Gesamtstatus war bei diesem Abruf noch laufend.

## 3. Sonar: null Befunde und null Duplikation

- [x] S01: Nur lesendes exaktes Head-/Anbieter-Gate weist fehlende, veraltete, unfertige und mehrdeutige Nachweise zurück.
- [x] S02: Negativtests, begrenzte Diagnosen und eingeschränkte Leserechte bleiben erhalten; keine Ausnahmen, akzeptierten Befunde oder schwächeren Regeln.
- [x] S03: Historische Null-Zähler bleiben revisionsgebunden: `039b7f12`, `91f07e12`, `47714de0`.
- [x] S03a: Exaktes Head-Gate bestand für `f7aa2f2c`.
- [x] S03b: `91f07e12`, [Check 106651947571](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106651947571): null neue/akzeptierte Issues, Hotspots und Annotationen.
- [x] S03c: `47714de0`, [Check 106837589312](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106837589312): dieselben vier Null-Zähler.
- [x] S03d: `bced5ce7`, [Check 106898325037](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106898325037): dieselben Null-Zähler und angezeigte 0,0 % Duplikation.
- [x] S03e: Exakt `7d05e89f`, [Check 107300845580](https://github.com/Easton97-Jens/ModSecurity-conector/runs/107300845580): null neue/akzeptierte Issues, Hotspots und Annotationen; angezeigte New-Code-Duplikation 0,0 %.
- [ ] S04: Finale Freigabehead-Qualität nach letzter Lieferung bestätigen; frühere Analyse beweist keine spätere Dokumentations-SHA.
- [x] S05: Pflicht-Duplikationsgate verlangt exakt null neue doppelte Zeilen, Blöcke und Dichte statt nur gerundeter Anzeige.
- [x] S06: Exaktes Duplikationsgate bestand für `bced5ce7`, [Job 106897813154](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35772630849/job/106897813154), und für `b91b6826` im vollständigen Lint-Lauf unten.

Dies sind New-Code-Metriken des PRs, keine Behauptung zu allen historischen
Repository-Befunden. Coverage und Secret-Scan bleiben unabhängig davon.

## 4. Routenbezogener Stand

| Route | Erledigter Teilbereich | Verbleibend |
| --- | --- | --- |
| NGINX nativ | Typisierte Fehler, Prädikate, Auditmarker, Aufrufer-/Adoptiontests | Finale gemeinsame Prüfung und Live-Transport-/Logmatrix |
| Apache nativ | Exakter Collector, Kopien, erste Fehler, geprüfter Audit/Init/Generations-Cleanup; 20 kompilierte und 25 Adoptionfälle | Weitere Filter-/API-Ausgänge, physische Ausgabeweitergabe und Live-Matrix |
| HAProxy HTX | Binding-Prädikate und Helfer-/Adoptiontests | Aufruferbezogene Fehler/Cleanup und Host-/Reset-/Logprüfung |
| HAProxy SPOE/SPOP + Companion | Native/Common-Rückgabeverträge | SPOP-Schreibfehler und getrennte Companion-/Steuerungsnachweise |
| Envoy ext_proc | Geprüfter Commit, erste Fehler, zehn C-Brückenfälle und echte native Go-Suite bestanden | Live-gRPC-/Host-/Logfälle und finale gemeinsame Verifikation |
| Envoy ext_authz + Companion | Gemeinsame Runtime-Korrekturen | Getrennter Companion-Lebenszyklus und physische Ausgabe |
| Traefik Middleware/UDS | Gemeinsame Runtime-Korrekturen | Adapterfehler, physische Ausgabe und Live-Host-Nachweis |
| Traefik forwardAuth + Companion | Gemeinsame Runtime-Korrekturen | Getrennte Companion-Steuerungs-/Lognachweise |
| lighttpd Sidecar | Gemeinsame Runtime-Korrekturen | Adapterfehler und echte Socket-/Lognachweise |
| lighttpd nativ/gepatcht | Gemeinsame Verträge auf Runtime-Routen | Getrennte Hooks, Strict-Zulassung und native Hosts |

Nicht unterstützte Strict-Profile bleiben nicht unterstützt. Gleiche Semantik
verlangt keine gleichen Hostzahlen und erteilt keine neue Reset-/Abbruchfähigkeit.

## 5. Dokumentation und Lieferung

- [x] D01: Bestehender Draft-PR; kein Merge, Master- oder Force-Push.
- [x] D02: EN/DE-Checkliste trennt implementierten Code von Verifikation.
- [ ] D03: Connector-Anleitungen/Beispiele und Kompatibilitätsprüfung vervollständigen.
- [x] D03a: Zweisprachiger Vertrag und Auswerter-/Hash-Migrationswarnungen bleiben erhalten.
- [x] D04: Tatsächliche Apache-Ergänzungen und veröffentlichte Envoy-Testreparatur abgeglichen; veraltete Behauptung eines unberührten Apache-Modulteils entfernt.
- [ ] D05: Finale Dokument-/Link-/Diff-/CI-Prüfung und PR-/Branch-Abgleich.

## Revisionsgebundene Nachweise

Der vollständige [Lint-Job 106900742683](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35773496921/job/106900742683)
bestand für `b91b6826`, einschließlich beider Sonar-Gates. Das ist historischer
Nachweis, kein automatischer Erfolg neuer Apache-Quellen oder Envoy-Tests.
Der Apache-Strukturjob für `3c29004b` erreichte die abschließende Zweisprachigkeits-
prüfung und scheiterte an zwei Datumsfeldern; der native/APR-Job bestand getrennt.
Der erste echte Envoy-Lauf [35847504839](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35847504839)
scheiterte an drei Fixture-/Erwartungsfällen. Der reparierte vollständige native
Lauf bestand für `7d05e89f` (V20/V25), ohne geänderten Produktivschutz. Nach Ergänzung
der Datumsfelder bestand die unveränderte Zweisprachigkeitsprüfung für `b92459ba` (V26).

Frühere Nachweise bleiben in [der Liste bei ad22918e](https://github.com/Easton97-Jens/ModSecurity-conector/blob/ad22918e92849a10483439d72ac9a50154ec00be/docs/pr-382-checklist.de.md)
und verlinkten Change Records erhalten. Der Nutzer hat den RTK-Geltungsbereich
für diese Fortsetzung klargestellt; GitHub-API-Änderungen brauchen keinen lokalen
Wrapper. Neue native Go-Fixture und Aufrufer wurden lokal formatiert; vollständige
native Ausführung übernimmt GitHub-CI, da GitHub-DNS/Download im Bearbeitungscontainer
nicht verfügbar war.
