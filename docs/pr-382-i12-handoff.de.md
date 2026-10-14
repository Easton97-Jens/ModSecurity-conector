# PR #382: I12-Übergabe nach Behebung der Review-Befunde

**Sprache:** [English](pr-382-i12-handoff.md) | Deutsch

## Aktuelle I12-Lifecycle-Konsolidierung, 2026-10-14

Status: **I12_PARTIAL** und unabhängig **RELEASE_BLOCKED_SECRET_HISTORY**.
Beide PRs bleiben Draft. Der [aktuelle Hostbericht](pr-382-i12-host-evidence-20261014.de.md)
und [vollständige Originalindex](pr-382-i12-missing-case-index-20261014.de.md)
binden physische Pakete, Originalverträge und Hashes. Frühere Abschnitte unten
beschreiben ausschließlich ihren historischen Stand.

Die unveränderte Auswahl enthält 1484 Original-IDs: 1406 verpflichtende und 78
diagnostische. Es bestehen 21 vollständige Pflichtfall-Lifecycle-PASS und 0 FAIL,
mit mindestens einem vollständigen Fall auf jedem der 13/13 Pflicht-Routenteile.
Für 151 Original-IDs ist tatsächliche Ausführung erfasst. Die 37 historischen
Config-PASS enthalten 36 Pflichtfälle; insgesamt bestehen 57 qualifizierte
Pflicht-PASS, 0 Pflicht-FAIL und 1426 weiterhin unqualifizierte Original-IDs.
Von ursprünglich 596 ungeklärten Oracles sind 21 unabhängig quellbestätigt und
tatsächlich erneut ausgeführt; 575 bleiben ungeklärt. Originalmitgliedschaft,
Oracle-Nullwerte, Rohbelege und frühere Fehlläufe bleiben erhalten.

Die 21 vollständigen Fälle qualifizieren nicht alle 1406 Pflicht-IDs. Anwendbare
Host-/native EOS-, MIME-, Finish-/Free-, Client-/Backend-, Handle- und
Cleanup-Belege sind für diese Pakete physisch gemessen; begründete
Nichtanwendbarkeit bleibt ausdrücklich erhalten. Nullbyte-Append und Client-EOF
ersetzen keinen nativen EOS-Nachweis. Stock native bleibt Diagnose, einschließlich
seiner 23 ursprünglich ungeklärten Oracles; keine pauschale Unsupported-
Umetikettierung. Übrige Pflicht-IDs, fehlende Fixtures, weitere Limits,
Late-/Commit-, Sinkfehler-, Cancellation-/Reset- und Nachbarfälle bleiben offen.
I12/V08–V10 bleiben insgesamt offen.

[Private Capture-Quellen](../ci/runtime/lifecycle/i12/README.de.md) erhalten neun ausdrückliche Varianten.
Jedes Paket bindet tatsächliche Quellen, geladene Images, SDKs und Konfiguration.
Frühere a9-/0275-Builds bleiben von aktuellen Produkt-/Lieferrevisionen getrennt;
ein grüner Quelltest ersetzt keine Hostausführung.

Veröffentlichter Produkt-Head von #382:
`9980eb049dde0643da6a4f04e3b6712801b670b3`; normale #410-Integration:
`eca03db3`. Der reine Testfolgefix ersetzt die veraltete Mapper400-Assertion
durch typisierten Dispatch/Default500 und den getrennt begrenzten
Headercount400-Vertrag; alle 38 angeforderten Vertragstests und fünf
kompilierten Mappertests bestehen. Neue #382-CI steht aus. e47-Sonar-SUCCESS
(Check `116148729241`, Gate OK, Security A, neue/akzeptierte Issues 0,
Hotspots 0, Duplikation 0) bleibt ausschließlich historischer e47-Nachweis,
ohne Übertragung auf 9980 oder #410. Remote #410 bleibt an diesem
Vor-Push-Checkpoint bei `02754040bced960cfc1857416cd7101bb3116ef4`;
#410-Source-CI erwartet Root-Push und frischen Readback. Historisches Gitleaks
bleibt ein unabhängiger Releaseblocker. Kein Gesamt-CI-PASS, Master-Merge oder Release.


Die Erweiterung enthält vier zusätzliche HAProxy-Body-/Headerfälle, zwei native
HAProxy-Request-Limitfälle mit 16 Bytes (`Reject` und `ProcessPartial`) sowie
zwei echte lighttpd-Leerbodyfälle. Getrennte bestätigte Erwartungen und Retakes
qualifizieren keine Geschwisterfälle. Gepatchtes lighttpd erfasst ein tatsächliches
Null-EOS-Argument im echten Leerbody-Zweig und native P2-Finalisierung ohne Request-Append.

Apache erhält ursprünglichen Duplicate-Header-FAIL und Originalregel. Ein separat
hash-/versionsgebundener Override folgt dem tatsächlichen Apache-/APR-Merge zu
einem Headerwert `one, two`, ohne Comma-Splitting im Produkt. 14 kanonische
Hostfälle, 12 echte APR-/SDK-Regressionen und vollständiges Root-geprüftes
Apache-Paket sind getrennte Nachweise. NGINX-Fix
`12756aa957f54d3efce6bd97ec0dbac07fa576cc` propagiert interne Mapperfehler als
HTTP500; echte HTTP500-/Client-HTTP400-Retakes und vollständiger Fall09 sind
separat gebunden. Der frühere Body-P2-/Injected-P1-Geltungsbereichskonflikt
bleibt als historische Disposition erhalten.

Genau drei Generatoren erzeugen Oracle-Reconciliation, Lifecycle-Ledger und
aktuellen EN/DE-Bericht samt Index. Originale, 596-Mitgliedschaft und Nullwerte
bleiben erhalten. Der native Testobserver erfasst 38 Wrapper sowie ausdrücklichen
Snapshot, typisierte Handle-Zuordnungen und echte Rückgaben. Der Renderer bindet
die 37 historischen Config-PASS an ihre unveränderte physische Originalquelle
und verwirft unbelegte PASS-/Scope-/Ausführungsangaben. Private Hooks gehören
nicht in Releaseartefakte.

Tatsächlich bestanden: 62 Native-/Oracle-/Ledger-/Apache-Tests, 13 Renderertests,
115 NGINX-Mutationstests, 77 Guards, fünf kompilierte Mappertests, Root-Quick06,
Nativecontracts und Docs10. Capture-Prüfungen bestehen neun Varianten,
45 Patchanwendungen, 15 Negativguards und fünf Capture-Gruppen. Der Sourcecopy-
Receipt-Overwrite-Fix verweigert ein vorhandenes Receipt vor jedem Schreibvorgang
und legt es exklusiv an; drei neue Kontrollen erhalten Datei-/Hardlink-/
Verzeichnisziele. Die Registry mit 150 Objekten ist verifiziert; Observer-C/H
und Manifeste sind unverändert. Dies ist ein funktionaler Sourcecopy-Guard,
kein Securityscan. Root validiert den finalen kombinierten Doku-/Source-Snapshot
nach dieser Übergabe erneut.

Kein Deep-Security-Scan und keine Abschwächung von Gates oder Guards erfolgten.
Framework-/MRTS-Gitlinks und Originalrohbelege bleiben unverändert. Alle früheren
CR-Abschnitte und der unveränderliche Originalindex bleiben erhalten.

Root bestätigte zusätzlich 20 ergänzende `HARNESS_DEFECT_CONFIRMED`-
Dispositionen außerhalb der ursprünglichen 596-Mitgliedschaft. Der originale
generische Katalogexit 1 bleibt unverändert und gilt nicht als Direct-native-
oder Wrapperdriver-Vertrag: tatsächlich abgewartete Native-Exits sind 255 x 8,
78 x 9, 2 x 1 und 77 x 2. Dies sind Prozessausgänge, keine HTTP-Statuswerte;
neun Operationen sind reine Parserläufe und elf Dienststartfehler. Neun
Firstcauses aus physisch leerem Sidecar-stderr bleiben NULL; Quell-/Configursache
bleibt getrennt. Scopefile-Fälle verwerfen den unbekannten Common-Runtime-Key
`phase4_content_types_file` und belegen keine MIME-/Wildcard-Parserausführung.
Formale resolved expectation und retest bleiben null; daraus folgt kein
zusätzliches Konfigurations- oder Lifecycle-PASS. Die anderen 29 historischen
Original596-Lücken und 23 diagnostischen Stock-native-Oracles bleiben ungeklärt;
keine neue Unsupported-Freigabe wird abgeleitet.

Dispositionsquelle: `catalog-conflicts/final-supplemental20/disposition-summary.json`,
SHA256 `d68c2535d5ece0990670b3e01f173df9d98ad26684fef1f7bf39ca37cc436021`.
Root-bestätigte records15, oracle13 und ledger08 erhalten 21 geklärte/575 offene
Oracles, 21 vollständige PASS, 13 Routen, 151 ausgeführte IDs, 37 Config-PASS,
57 qualifizierte Pflicht-PASS und 1426 unqualifizierte IDs. Tatsächliche Quick06
und Docs10 bestanden; Root90-Tests und SourceRoot05 bestanden mit 150 Quellobjekten,
neun Varianten, 45 Patchanwendungen und 15 Guards. Dies bleibt von ausstehender
gehosteter CI getrennt.

## Historischer Review-Checkpoint, 2026-10-13

Die frühere Reviewaufgabe war **BLOCKED_FOR_I12** und führte #410 nicht erneut aus.
Ihre revisionsgebundenen Beobachtungen folgen unverändert als Historie.

Die endgültig gelieferte Parent-SHA, revisionsgenauen CI-/Sonar-/Review-Ergebnisse
und normalen Commit-IDs stehen in der aktuellen [Beschreibung von PR #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382).
Die Ausgangsrevision dieses Dokuments und historische Runs ersetzen diese
Lieferbindung nicht. Das lokale Lieferprotokoll bleibt unter
`/var/tmp/codex/ModSecurity-conector/runs/pr382-review-20261013` erhalten.

| Revision | Bindung |
| --- | --- |
| Parent-Ausgangspunkt der Behebung | `4639f982a8125f4150394e4d4f2e8af4e690f494` |
| Master bei Aufgabenbeginn | `6aae115fff8531eb1e08a4b10745d7ae93550124` |
| Framework, unveränderter Gitlink | `99a7985c1be92a2297b1b59208f64df6768f2cbf` |
| MRTS, unveränderter verschachtelter Gitlink | `8a6bb546c4c81d8ffc7be801dceac60c6925685f` |
| Historischer Head von #410 | `511c4ac4515f0e515f68b3bbc38274c5a230d903` |

Der [konsolidierte Change Record](../reports/audits/change-records/CR-20261013-pr382-consolidated.de.md)
erhält die 122 ursprünglichen Change-IDs und unveränderlichen Detailnachweise.
I09/I10/I11 und Engine-eigene Inspection-Limits bleiben Implementierungsverträge;
sie ersetzen keinen I12-Hostnachweis.

Der unabhängige Gitleaks-Scan des PR-Commitbereichs findet weiterhin zwei
Prosa-False-Positives in veröffentlichten Commits: `generic-api-key` in
`docs/pr-382-event-contract.md` bei `91f07e124fe09056dc46dc59d65693f406b4b1a1`
und `docs/pr-382-i09-route-audit.de.md` bei
`492663334d89428dce084792145ef94e91579788`. Die aktuelle Prosa ist korrigiert;
ein angehängter Commit entfernt historische Treffer nicht. Es gibt keine
Scanner-Ausnahmen, eingeschränkten Scanbereiche oder History-Rewrites. Kein
Credential-Wert wird wiedergegeben. Historische Bereinigung erfordert eine
gesonderte Nutzerentscheidung; der fehlgeschlagene unabhängige Check verhindert
READY_FOR_I12.

Der lokale Go-Reparaturstand verwendet zentrale Version 1.27.2 und vier
Modulminima 1.26.9. Nur notwendige Envoy-Requirements wurden auf `x/net` 0.61.0,
`x/sys` 0.49.0 und `x/text` 0.43.0 erhöht; grpc 1.83.2/protobuf 1.36.11 bleiben
unverändert. Vier Modulprüfungen einschließlich Race/govulncheck, 71 Updater-/
Workflowtests und actionlint bestehen lokal. OSV meldet null neue Paare gegenüber
der Ausgangsbasis, aber drei verbleibende Graph-Baselinepaare zu zwei Advisories
in unbenutzten SDK-/openpgp-Pfaden; das ist kein OSV-Nullbefundnachweis.
`GO_UPDATER_FIXED_IN_PR` erfordert finale PR-Verifikation und wird an diesem
lokalen Checkpoint nicht behauptet. **MASTER_WORKFLOW_VERIFIED: NOT_EXECUTED**:
Master-Run `38370968157` bleibt der frühere Fehllauf. Nach einer gesondert
freigegebenen Integration muss der vertrauenswürdige master-Updater tatsächlich
neu laufen; die PR-Kandidatenprüfung mit Leserechten ersetzt das nicht.

Vor einer neuen I12-Kampagne müssen Parent-Checks auf der exakt integrierten
SHA terminal bestehen, ebenso die strengen Sonar-Nullbefund-/Duplikations-Gates
und ein unabhängiger Secret-Scan mit Exit 0. Frische Codex-/Security-Reviews
dürfen keine bestätigten offenen P1/P2 enthalten. Lokalen HEAD, Remote-Branch
und PR-Head abgleichen; vollständige SHAs und alle Check-/Run-URLs erhalten.
Ein früheres grünes Ergebnis gilt nach einem neuen Push nicht weiter.

Für #410 beide Sprachversionen von Checkliste und Restmatrix mit den aktuellen
I09/I10/I11- und Body-Policy-Verträgen abgleichen. Historischen I12-Bericht und
originale Rohbelege unverändert aufbewahren. Den vorgeschlagenen Change Record
in den Gesamtrecord übernehmen, statt die entfernte Sammlung wiederherzustellen.
Die früheren 79 Records (9 PASS, 6 FAIL, 53 BLOCKED, 11 NOT_EXECUTED) gelten
ausschließlich für ihr ursprünglich getestetes Produkt. #410 ist aktuell
merge-konflikthaft; Konfliktauflösung und neue Testrevision sind separate Arbeit.

I12/V08–V10 auf dem tatsächlich integrierten Produkt neu ausführen und zehn
Profile sowie vierzehn Routenteile getrennt binden: Apache native; NGINX native;
HAProxy HTX und SPOP/Response-Companion; Envoy ext_proc und
ext_authz/Response-Observer; Traefik native UDS und forwardAuth/Response-Observer;
lighttpd Stock-Sidecar, diagnostische Stock-native-Kontrolle und gepatchter
nativer Pfad. Nicht unterstützte Modi bleiben nicht unterstützt. Die
Stock-native-Kontrolle erhält keine Body-Hooks; ein Strict-Abort bei gepatchtem
lighttpd bleibt unbewiesen.

Jeder anwendbare Routenteil benötigt neue native Regel- und technische
Fehlerfälle, Off/Safe/Strict-Verhalten, Request-/Response-Body-Chunks, EOS und
MIME-Auswahl, Pre-/Postcommit-Status und tatsächliche Hostaktion, frühe/späte
Write-Fehler, Abort/Reset sowie Nachbar-/Folgeverkehr, physische Event-Sink-Fehler,
einmaliges Finish/Cleanup und originale Client-/Transport-/Logbelege. Native
Reject-/ProcessPartial-Fälle und Marker jenseits des früheren Body-Caps erneut
prüfen. Begrenzte Autorisierungssamples und SPOP-Framing von Inspection-Limits
trennen. Private Stock-Spool-Rechte, technische Zulassung/Erschöpfung und erneute
Zulassung ohne BODY_LIMIT-Event einbeziehen.

Echte Hosts, gepinnte native Bibliotheken/Module, private Ports und Runtime-Pfade,
passende Service-UIDs sowie beschreibbarer privater Spool-Speicher sind
Voraussetzungen. Der lokale Namespace bildet nur UID 0 (`0 0 1`) ab:
Der neue echte Nonroot-Starttest ist BLOCKED; Root-Profil-Readiness und injizierte
Ownership-/Read-only-Kontrollen sind getrennte Nachweise. Reguläre
Dateiallokationen können durch Socket-Deadlines nicht abgebrochen werden;
fremde Dateisystemschreiber bei benötigter Garantie über dedizierte Dateisysteme
oder Quotas isolieren.

Historisch gemeldete Stock-RST-Leerevent- und Common-Lossy-Event-Fehler auf der
neuen exakten Revision erneut prüfen; ohne Ausführung weder als aktuelle Fehler
noch als PASS umetikettieren. Historische breite Apache-/HAProxy-Fehler,
UID-/Mount-Einschränkungen und quellgebundene R16/R17-Ergebnisse bleiben in den
unveränderlichen Records erhalten. Rohbeleg-Roots und Prüfsummenprotokolle
aufbewahren. Diese Aufgabe führt fokussierte Reparaturtests und Parent-CI aus,
**keine vollständige I12-Matrix**.
