# PR #382: Checkliste für gemeinsames Connector-Verhalten

**Sprache:** [English](pr-382-checklist.md) | Deutsch

[Draft-PR #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382),
Branch `fix/unified-native-results-events-20260921`, Basis
`5170d24801243cdcd7bf1bca6123bf8cb2c72386`. Aktualisiert: 2026-10-10.
Historischer Stack-Abruf vom 05.10.2026: Der Branch war über Merge-Commit `dfd5e5b1` mit dem damals aktuellen `master` `820b6975495bdf0f90aca67eee86e27a3b7d329b` synchronisiert; bei diesem Abruf lag er keine Commits zurück.

**Bei I09 und I10 fehlt noch mehr als der Live-Host-Nachweis.** Fertiger Code,
ausgeführte kompilierte Tests, offene native Tests und echte Hostnachweise bleiben
getrennt. Der Apache-Modulteil ist inzwischen implementiert und darf nicht weiter
als unbearbeiteter Interventions-/Initialisierungs-/Auditfehler aufgeführt werden.

Historische veröffentlichte Testreparatur (05.10.2026): `7d05e89fc12dca64c7129553d0c83157e956e0f3`.
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


## Historisches R16: 2026-10-10 nachgelagerter NGINX-H1-Systemnachweis aus PR #396

Dies ist ein nachgelagerter NGINX-H1-Systemnachweis aus PR #396, kein Runtime-Test
des unveränderten PR-#382-Produktstands. Die Dokumentationsbasis ist
`2a5704f82fdae4ba75902eb3f4244225838e1747`; diese Referenz integriert weder
den getesteten #396-Code noch verändert sie dessen Gitlinks.

| Bindung | Beobachteter Wert |
| --- | --- |
| Getesteter Parent | `777a244f0689c320475b030b9e7adbb3192febbe` |
| Getestetes Framework | `9f41f80db7bf53b57429457bce0dda675d2ec5d7` (PR #137) |
| Getestetes MRTS | `8a6bb546c4c81d8ffc7be801dceac60c6925685f` |
| Run / Datum (UTC) | `nginx_full97_777a_20261010_r16` / 2026-10-10 |
| Standardtarget | `make full-lifecycle-nginx` über den isolierten RTK-umhüllten Supervisor |
| Konkretes lokales Testsystem | Ubuntu 26.04.1 LTS; Kernel 7.0.0-38-generic; x86_64; KVM (echter Host-Abruf); GCC 15.2.0; Python 3.14.7; NGINX 1.31.6 |
| Isolation / Identitäten | Private Mount-/PID-/Network-Namespaces; Loopback; echter Root-Master UID 0 / nobody-Worker UID 65534 |
| Original-Canonical / Schema | `PASS`; 97/97 ausgewählte Required-PASS; beide Schemafehlerlisten leer |
| Übriges Inventar | 34 nicht ausgewählte `NOT_EXECUTED`, 35 `NOT_APPLICABLE`; kein ausgewählter Nicht-PASS-Record |
| Direkt gemessene Abschlüsse | 13 Abschlüsse für neun exakte Programme, alle Exit 0, keine Signale |
| First-Byte-Writer | `write-first-byte-source-results.py`: genau ein direkter Child-Wait, Exit 0; Invocation `1d65c03b1453430eaeede8c1271dd487` |
| Make / Supervisor / Collector / Validator | 0 / 0 / 0 / 0 |
| Tatsächliche HTTP-Operationen | 79 Nicht-Readiness-Requests: 75 primäre/Fault-Requests plus vier Parserkontrollen; 17 Readiness-Probes separat gezählt |
| Weitere echte Operationen | 61 Server-Lifecycles / 61 Cleanup-Beobachtungen; 17 Reloads; 10 Config-Operationen (neun spezifische Ablehnungen Exit 1, ein akzeptierter Start Exit 0) |
| Bindungsbeobachtungen | 57 frische root-owned direkte Projection-Kinder; 43 native Invocation-Receipts für 42 native Required-Records; 24 Engine-/Modul-Mappings der Worker |
| Runtime-Prüfsummenledger SHA256 | `2c35f93c059dd80bbe84bb158f52bff3bfbe97b81d44379e53ecb3e2bce0e246` |
| Source-/Ledger-Prüfung | 3552 Source-Dateihashes unverändert; Runtime-Ledger 2514 Einträge, unabhängiger Prüfsummencheck Exit 0 |

Öffentliche Zusammenfassungen: [PR-#396-R16-Ergebnis](https://github.com/Easton97-Jens/ModSecurity-conector/pull/396#issuecomment-6100868299)
und [Framework-PR-#137-Umfang](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/137#issuecomment-6100868488).

**Zum R16-Checkpoint blieb die lokale Abnahme wegen einer Messlücke BLOCKED:** Der exakte numerische
Exit des generischen H1-Strict-curl-Prozesses wurde nicht persistiert. Sein
Fehlschlag ist als nonzero bekannt, aber die Diagnosenummer `52` beweist keinen
Exit 52. Dies ist vom nativen Strict-Driver und dessen erwarteter
Incomplete-Read-Evidence getrennt. Canonical PASS und gemessene Writer-Exits
schließen den fehlenden direkten Client-Statusnachweis nicht. PR #396 blieb
deshalb bei diesem Checkpoint Draft; hier wird weder ein gesamter lokaler E2E-Abnahme-PASS noch ein
Ready-Übergang behauptet.

Raw-Evidence und Record-Zuordnung bleiben lokal unter
`/var/tmp/codex/ModSecurity-conector/analysis/nginx-full97-777a244f-20261010T181030Z`
und dem getrennten Task-Runtime-Root erhalten. Lokale Dateien sind keine
herunterladbaren GitHub-Artefakte; der öffentliche PR-Bericht ist eine
Zusammenfassung, kein Raw-Bundle. Historisches R15 behält seinen ursprünglichen
Canonical PASS und die separate First-Byte-Writer-Messlücke; der frische Lauf
schreibt es nicht um.

Dies belegt nur die beobachteten NGINX-H1-Verträge auf diesem konkreten lokalen
System. Es ist keine H2/H3-, CRS-, Off-, Alle-Plattformen-, Produktions-,
Connector-übergreifende oder Protected-Exact-Head-Abnahme. Die breiten I09-I12 und
V08-V10 bleiben offen. Die Review-Reife von Framework-PR #137 wird separat geprüft;
diese Referenz mergt keinen der PRs.
Soft-Budget-Fälle belegen Überschreitungserkennung nach Engine-Rückkehr, keinen
harten Abbruch einer hängenden Engine. Transport-Short-Write-/EAGAIN-Beobachtungen
belegen keinen physischen Event-Log-Sink-Short-Write.

## R17: nachgelagerter NGINX-H1-Systemnachweis aus PR #396

**Nachgelagerter NGINX-H1-Systemnachweis aus PR #396.** Der [öffentliche R17-Bericht](https://github.com/Easton97-Jens/ModSecurity-conector/pull/396#issuecomment-6101794434) wurde vor dieser Dokumentationsänderung veröffentlicht. Er dokumentiert genau einen freigegebenen lokalen Standard-Full97; er testet weder das PR-#382-Produkt noch diese spätere Dokumentationsrevision. Dokumentationsbasis: `b2622a5d6ca746485c08f4789208299a111f47c7`. Keine Produktquellen- oder Gitlink-Änderungen.

| Bindung | Tatsächliches R17-Ergebnis |
| --- | --- |
| Getesteter Parent | `2f02370b07149265841411894f1a2cf7f1e978ff` |
| Getestetes Framework / MRTS | `9f41f80db7bf53b57429457bce0dda675d2ec5d7` / `8a6bb546c4c81d8ffc7be801dceac60c6925685f` |
| Run / Target | `nginx_full97_2f02_20261010_r17` / `make full-lifecycle-nginx` |
| System / Isolation | Ubuntu 26.04.1 LTS; Kernel 7.0.0-38-generic; x86_64/KVM; GCC 15.2.0; Python 3.14.7; NGINX 1.31.6; private Mount-/PID-/Network-Namespaces, Loopback, echter Root UID 0 / nobody UID 65534 |
| Tatsächlicher Lifecycle | Exit 0; 554.091 Sekunden; lokaler begrenzter funktionaler PASS |
| Original-Canonical / Auswahl | PASS; unveränderte 97 Required = 14 YAML + 42 native + 10 Config + 31 explizite Ableitungen; null Required FAIL/BLOCKED/NOT_EXECUTED/missing; Schemafehlerlisten leer |
| Übriges Inventar / Source-Platzhalter | 34 nicht ausgewählte NOT_EXECUTED + 35 NOT_APPLICABLE; originales source-result erhält 31 PASS + 42 NOT_EXECUTED-Platzhalter, mit tatsächlicher spezialisierter nativer Lineage statt synthetischem PASS |
| Generischer Strict-Direktabschluss des Clients | Tatsächlicher normaler curl-Exit 52, keine Diagnoseableitung; Invocation `669ba1b19fc340618d62148d715e5fc3`, Child-PID 10440; Rule 1100301 strict/abort; exakte Case-/Run-/Source-/Log-/TX-Bindung |
| Client-Beobachtungsgrenze | Tatsächlicher curl-HTTP-Wert 000; Producer-/Originalstatus 200 ist ein anderer Beobachter. Native Strict erhielt separat HTTP 200, 10428 Bytes, chunked/incomplete_read/connection_aborted, Driver-Exit 0 |
| First-Byte-Source-Writer | Tatsächlicher normaler Exit 0; Invocation `1515086ec928494aafd0b0a0fceab107`, Child-PID 12514; ursprüngliche Barrier-/EOS-/Identitätsbindung erhalten |
| Direktabschluss-Inventar | 34 curl-Paare = 16 primäre + 1 First-Byte + 17 Readiness; 16 Programm-Abschlusspaare, alle normaler Exit 0, keine Signale |
| HTTP / Lifecycle / Cleanup | 79 Nicht-Readiness-HTTP-Operationen einschließlich vier positiver Kontrollen; 17 Readiness separat; 61 echte Server-Lifecycles / Cleanup-Beobachtungen; 17 Reloads |
| Config / Native / Projections | 10 Config-Operationen (neun normale Reject-Exits 1, ein akzeptierter Start Exit 0); 43 native Invocations für 42 native Required-Records; 57 getrennte frische root-owned direkte Projection-Kinder ohne Symlinks |
| Source / finales Prüfsummenledger | 3554 Source-Dateihashes unverändert; 2589 finale Einträge, unabhängiger Prüfsummencheck Exit 0; SHA256 `b79fbe3e2b7cf2806c8698f2a6fd7f1f1a4c4f06aed8075924311d4d1c27d97a` |

Der externe Direct-Child-Recorder nutzte den bestehenden curl-Einspeisepunkt ohne funktionale Parent-/Framework-/MRTS-Änderungen. Er persistierte den tatsächlichen `subprocess.Popen/direct-child.wait`-Status unter Erhalt von Argumenten, Streams und Signalen; keine pauschale nonzero=PASS-Regel. Die konkrete Strict-Oracle, echte Rule-/Transport- und exakte Identitätsbindung bleiben erforderlich. Ein echter begrenzter Fokus ging dem einzelnen Full97 voraus. Fehlgeschlagene Fokusvorbereitungen vor Requests sowie historische R15/R16 bleiben unverändert.

Dies schließt die R16-Messlücke **nur für den neuen lokalen R17-NGINX-H1-Umfang**. Es ist kein Protected Exact-Head, H2/H3, CRS, Off, Produktion, anderer Connector oder Runtime-PASS für eine spätere Dokumentations-SHA. Framework-PR #137 war bereits mit getestetem Head `9f41f80…` gemergt; sein Merge-Commit ändert den getesteten Gitlink nicht. Diese Referenz behauptet weder Ready-, Merge- noch Retarget-Aktion für #396. #382 bleibt Draft.

Die [I09–I12-Restmatrix](pr-382-i09-i12-rest-matrix.de.md) enthält 56 explizite Zeilen für 14 getrennte Routenteile, jeweils mit Vertrag, Source-/Test-SHA, offener Implementierung/Hostnachweis und nächster Aktion. Breite I09–I12 und V08–V10 bleiben unabgehakt; erledigte I09f/I10e bleiben erledigt. Apaches void-Sinkabschluss und SPOP ungeprüftes `fputs` sind sourcebestätigte getrennte Implementierungslücken. Transport-Short-Write/EAGAIN beweist keine physische Sink-Fehlerbehandlung; Soft-Budgets erkennen Überschreitung nach Rückkehr, keinen harten Abbruch.

Lokale Raw-Evidence bleibt unter `/var/tmp/codex/ModSecurity-conector/analysis/nginx-strict-client-full97-r17-20261010T193127Z` und dem getrennten Runtime-Root. Der öffentliche Bericht ist eine Zusammenfassung, kein herunterladbares Raw-Bundle. Prüfsummen allein beweisen keinen semantischen PASS.

### Historischer Stack- und Konfliktabgleich vom 05.10.2026

- [x] `master` wurde ohne Force-Push in PR #382 gemergt. Zwölf überlappende Dateien wurden semantisch zusammengeführt: aktuelle CI-/Sicherheitsänderungen aus `master` bleiben gemeinsam mit den PR-#382-Verträgen für native Rückgaben, erste Fehlerursache, Apache-Lifecycle, terminale NGINX-Fehler und native Envoy-Brücke erhalten.
- [x] Der resultierende PR-#382-Head `dfd5e5b1` wurde mit `mergeable=true` und `behind=0` zurückgelesen; PR #382 bleibt Draft und ungemergt.
- [x] Zwei durch frische CI sichtbare Merge-Nacharbeiten wurden in `29af9abe` korrigiert: doppelte `permissions` in `.github/workflows/lint.yml` sowie die B09-NGINX-C-Regressionsfixture ohne Stub für den neueren Transaction-Contract. Für diesen Folgecommit ist frische Verifikation erforderlich; die fehlgeschlagenen Merge-Checks werden nicht nachträglich als PASS bezeichnet.
- [x] Der gestapelte PR #396 wurde geprüft und auf die aktualisierte #382-Basis gezogen. Seine NGINX-Exact-Head-Arbeit bleibt eine getrennte Draft-Abnahmeebene; sie schließt I09-I12 nicht automatisch und belegt keinen kanonischen vollständigen E2E-PASS.
- [x] Framework-PR #135 ist gemergt. Dessen Merge-Commit `dc41bd22c335156cae02d9049098b92af65b7c57` ist der Framework-Gitlink auf aktuellem `master`/#382. Der historische PR-#396-Zeiger `dd4af7d...` wird daher nicht als aktueller Parent-Gitlink verwendet.

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
- [x] I12b: Nachgelagertes R17 aus PR #396 führte die NGINX-H1-Standardroute mit echtem Root/nobody und frischen Projektionen aus, lokaler begrenzter funktionaler PASS. Dies schließt nur den Ausführungsreferenz-Teilbereich, keinen PR-#382-Produkttest oder breiten I12; R16 bleibt historisch.
- [x] I13: Begrenzter HAProxy-Rule-ID-Dekodierer und geordnete Bereinigung ohne geänderte Phasen-/Besitzsemantik ausgelagert.
- [x] I14: Alle 96 ursprünglichen NGINX-Adoption-Fälle plus vier Regressionen erhalten.
- [x] I15: HAProxy-Helfer-/Aufrufstellenprüfung und acht isolierte Regressionen erhalten.

Die [neunspaltige I09–I12-Matrix](pr-382-i09-i12-rest-matrix.de.md) zeigt verbleibende Implementierung und Hostnachweise für alle 14 Routenteile explizit; diese Inventur schließt keinen breiten Punkt.

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
- [ ] V07a: Unabhängigen Secret-Scan ohne unbelegte Ausnahme klären. Der frische Secret-Scanning-Lauf `37281536909` / Job `111670517150` für den synchronisierten Stack scheitert weiterhin. Aus diesem Status werden keine Secret-Inhalte abgeleitet oder reproduziert.
- [ ] V08: Echte Hostfälle für ProcessPartial/Reject, MIME/CSV, leere/mehrteilige Bodys/EOS, Budgets und native Fehler.
- [x] V08a: R17 liefert echte NGINX-H1-Operationszuordnungen und originale 97/97 Required-PASS (14 YAML / 42 native / 10 Config / 31 explizite Ableitungen). Ableitungen sind Records, keine zusätzlichen Requests; andere Hosts/Profile und breiter V08 bleiben offen.
- [ ] V09: Spätes Safe/Strict, Fehler vor/nach Commit, Client-Bytes, Reset-Grenze, Nachbarstreams und Bereinigung.
- [x] V09a: R17 erhält echte Safe-/Strict-, native Incomplete-Read-/Abort- und Cleanup-Evidence sowie tatsächlichen normalen generischen Strict-curl-Exit 52 mit Case-/Run-/Rule-Bindung. Dies schließt nur diese Messlücke; andere Profile, Nachbarstreams und breiter V09 bleiben offen.
- [ ] V10: Echte Routenlogs, ungültige/übergroße Metadaten, fehlende Beobachtungen und fehlerhafte physische Ausgaben.
- [x] V10a: R17 besitzt schemagültiges Original-Canonical, 16 echte Programmabschlüsse alle normaler Exit 0, genau einen First-Byte-Source-Writer mit Exit 0 und 34 echte curl-Paare. Dies schließt nicht sämtliche physischen Sink-/Logverträge des breiten V10.
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
- [x] V27: `dfd5e5b1` integriert den aktuellen `master` `820b6975` ohne Force-Push in #382; der Branch wurde vor der Folgekorrektur mit `behind=0` und `mergeable=true` zurückgelesen.
- [x] V28a: `29af9abe` korrigiert die zwei deterministischen Merge-Nachwirkungen aus actionlint und dem begrenzten NGINX-B09-Regressionsbuild. Damit sind die Fixes geliefert, nicht deren frischer CI-Lauf.
- [ ] V28: Frische CI für `29af9abe` und den späteren Dokumentationshead verlangen; weder die fehlgeschlagenen `dfd5e5b1`-actionlint/B09-Ergebnisse noch ältere grüne Ergebnisse werden vererbt.
- [x] V29: Beim Stack-Abgleich von PR #396 wurden sechs überlappende Textpfade und der Framework-Gitlink geprüft. Für den Parent-Gitlink ist das gemergte Ergebnis von Framework-PR #135 `dc41bd22` maßgeblich; PR #396 bleibt Draft und braucht eigene Checks nach dem Refresh.
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
- [x] D04: Tatsächliche Apache-/Envoy-Arbeit, den Master-Konfliktabgleich vom 05.10., den Stack-Stand von PR #396 und den gemergten Framework-#135-Gitlink abgeglichen; veraltete Vor-Sync-Aussagen entfernt.
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

Am 05.10.2026 wurde #382 in `dfd5e5b1` mit dem aktuellen Master synchronisiert. Frische CI auf diesem Merge bestätigte mehrere Connector-Workflows, zeigte aber zwei deterministische Merge-Nachwirkungen: doppelte Job-Permissions im Lint und eine veraltete kompilierte B09-Fixture. Beide sind in `29af9abe` korrigiert; frische Folgechecks bleiben erforderlich. Secret Scanning bleibt unabhängig offen. PR #396 wurde außerdem als gestapelter Draft geprüft; seine NGINX-Exact-Head-Kette liefert nachgelagerte Evidence, der historische kanonische Lauf war jedoch kein vollständiger E2E-PASS.

Frühere Nachweise bleiben in [der Liste bei ad22918e](https://github.com/Easton97-Jens/ModSecurity-conector/blob/ad22918e92849a10483439d72ac9a50154ec00be/docs/pr-382-checklist.de.md)
und verlinkten Change Records erhalten. Der Nutzer hat den RTK-Geltungsbereich
für diese Fortsetzung klargestellt; GitHub-API-Änderungen brauchen keinen lokalen
Wrapper. Neue native Go-Fixture und Aufrufer wurden lokal formatiert; vollständige
native Ausführung übernimmt GitHub-CI, da GitHub-DNS/Download im Bearbeitungscontainer
nicht verfügbar war.
