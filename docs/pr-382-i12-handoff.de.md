# PR #382: I12-Übergabe nach Behebung der Review-Befunde

**Sprache:** [English](pr-382-i12-handoff.md) | Deutsch

Datum: 2026-10-13. Status: **BLOCKED_FOR_I12**. PR #382 bleibt Draft;
PR #410 wird in dieser Aufgabe weder gemergt noch erneut ausgeführt.

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
