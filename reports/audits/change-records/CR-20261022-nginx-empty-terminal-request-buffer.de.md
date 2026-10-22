# Change Record: Leerer terminaler NGINX-Requestbuffer

**Sprache:** [English](CR-20261022-nginx-empty-terminal-request-buffer.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20261022-nginx-empty-terminal-request-buffer` |
| Datum (UTC) | `2026-10-22` |
| Basis-Revision | `c03352ba160675a94bf63125cceaa25367f52c27` |
| Pull Request | [#382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382) |

## Motivation und Problemstellung

NGINX stellt einen gültigen leeren Requestbody durch einen genullten
`ngx_buf_t` mit gesetztem `last_buf` dar. Der Requestbody-Adapter wies dessen
NULL-Member `pos` und `last` vor dem Aufruf von `msc_process_request_body` als
ungültigen Datenbereich ab. Der Host lieferte deshalb einen technischen HTTP
500, statt native Phase 2 auszuführen. Die frühere kompilierte `empty`-Fixture
verwendete eine fehlende Chain und prüfte diese echte Hostbufferform nicht.

Eine getrennte Common-Mapper-Fixture bezeichnete außerdem einen Body mit Größe
größer null und NULL-Daten als `oversized`, obwohl der Mapper keine Connector-
eigene Bodygrößenregel besitzt. Diese Eingabe ist der bestehende technische
P1-Fehler `missing body data` und darf nicht zu einem P2-Ergebnis umgedeutet
werden.

## Akzeptanzkriterien

- Ein echter leerer terminaler Steuerbuffer erreicht die native
  Requestbody-Finalisierung genau einmal ohne Nullbyte-Append.
- Daten vor einem terminalen Steuerbuffer werden einmal angehängt und einmal
  finalisiert; nicht terminale Flush- und Sync-Steuerbuffer verdecken keine
  folgenden Daten.
- NULL-Chainbuffer, fehlerhafte nicht spezielle Speicherbereiche und ein
  nichtleerer NULL-Append bleiben technische HTTP-500-Pfade vor der nativen
  Bodyverarbeitung.
- Ein Common-Body mit Größe größer null und NULL-Daten bleibt ein P1-Mapperfehler
  `missing body data`; die Unsupported-Body-Regel behält Vorrang.
- Fokussierte C-Fixtures kompilieren mit Warnings-as-Errors, englische und
  deutsche Dokumentation bleiben gleichwertig und die integrierte I12-
  Hostkampagne liefert den getrennten echten Host-/Client-/Native-/Cleanup-
  Nachweis.

## Implementierungsentscheidung und Begründung

Der Adapter erkennt jetzt `ngx_buf_special`, nachdem er den `ngx_buf_t`-Pointer
geprüft hat. Ein terminaler spezieller Buffer beendet die Chain-Verarbeitung;
Flush- und Sync-Steuerbuffer führen zu späteren Buffern weiter. Alle nicht
speziellen Buffer behalten die bestehende Pointer- und Bereichsprüfung. Damit
kann kein datenführender oder Datei-Buffer ein Steuerflag zur Umgehung nutzen.
EOS bleibt der spätere Aufruf von `msc_process_request_body`.

Die Regression-Fixture verwendet Flaglayout und Makrosemantik des gepinnten
NGINX. Sie ergänzt die echte leere terminale Form, Daten-/Steuerreihenfolge,
Flush-/Sync-Steuerbuffer und negative Speicherbereiche. Der veraltete
`oversized`-Alias entfällt; die ausdrücklichen NULL-Daten- und Unsupported-
Policy-Fälle erhalten den tatsächlichen Common-Mappervertrag.

## Geänderte Dateien

- `connectors/nginx/src/ngx_http_modsecurity_access.c`
- `tests/test_nginx_request_native_results.py`
- `tests/fixtures/nginx_common_input_validation.c`
- `tests/test_nginx_common_input_validation.py`
- `connectors/nginx/README.md` und `connectors/nginx/README.de.md`
- dieses englisch-deutsche Change-Record-Paar

## Ausgeführte Befehle

Alle Befehle wurden durch RTK ausgeführt. Rohe lokale Nachweise bleiben unter
`/var/tmp/codex/ModSecurity-conector/runs/pr416-nginx-complete-20261022`
erhalten.

| Prüfung | Beobachtetes Ergebnis |
| --- | --- |
| Vor dem Fix: `tests.test_nginx_request_native_results` gegen den Basisquellstand | Exit 1: 14 Tests, sechs Fehler. Echter leerer Terminalbuffer, Steuerbufferreihenfolge und native Finalisierung scheitern, während ungültige Bereiche abgewiesen bleiben. `baseline/request-native/pre-fix.log`, SHA-256 `4d33322e77a693dc604ed6a62f3383d7e6c053e6f4760d63b4b646cc0ae97597`. |
| Nach dem Fix: `python3 -m unittest -v tests.test_nginx_request_native_results tests.test_nginx_common_input_validation` | Exit 0: 18 Tests bestehen, einschließlich echtem leeren Terminalbuffer, genau einmaliger Finalisierung, Speicher-/Dateipfaden, Flush/Sync, ungültigen Bereichen und Common-P1-NULL-Datenklassifizierung. |
| Wiederholung der zuvor beobachteten Common-/Cleanup-Fehler auf sauberer Basis | Dieselbe veraltete Erwartung `body too large` und dieselbe Compile-Lücke der Cleanup-Fixture entstehen auf unverändertem `c03352ba...`; `baseline/c033-clean/baseline-failures.log`, SHA-256 `a0a02676ce7c4dfa3e093cb8d67b78a2c06aac0b99cdad8da73541cc3b1c4f45`. Diese Änderung korrigiert die Common-Erwartung und übernimmt die kontrollierte Interventionsschnittstelle der Cleanup-Fixture; beide bestehen nun die fokussierte #382-Prüfung. |
| Finale NGINX-Produktregressionsgruppen | Exit 0: Zwei getrennte finale Läufe bestehen 165 beziehungsweise 82 Tests (247 insgesamt) zu Common-Adoption, exakten Event-Writern, Request-Mapping, P1-/P2-/P3-/P4-Ergebnissen, Bodybuffern, nativen EOS-/Fehlerpfaden, Mutationswächtern und genau einmaligem Close-Cleanup. |
| Finales `make build-nginx` | Exit 0 gegen gepinntes NGINX 1.31.6 und den vorbereiteten libModSecurity-Runtimecache; die Buildstufe kompiliert den Connector aus dem finalen Produktquellstand unter `product-382/runtime-final` neu. Aus diesem Buildergebnis wird kein Hostnachweis abgeleitet. |
| `make check-nginx-c-standard-wiring`; Repository-Pfad-, zweisprachige Dokument- und Change-Record-Prüfungen | Exit 0. Der Change-Record-Check ist strukturell und wird nicht als Evidencevalidierung dargestellt. |
| `git diff --check`; `python3 ci/tools/new-change-record.py check` | Exit 0; der Archivcheck meldet ausschließlich strukturellen PASS. |

Integrierte Root-/Nobody-Host- und revisionsgenaue #410/#416-Ergebnisse gehören
weiterhin der nachgelagerten I12-Kampagne; hier wird keine nicht ausgeführte
Prüfung behauptet.

## Security-Auswirkung

Die Änderung akzeptiert ausschließlich spezielle NGINX-Steuerbuffer, die laut
Definition weder im Speicher noch in einer Datei liegen. Nicht spezielle NULL-
oder umgekehrte Bereiche schlagen weiterhin vor nativer Verarbeitung sicher
fehl. So werden gültige leere Requests nicht mehr als technische Fehler
gemeldet, ohne die Behandlung fehlerhafter Buffer, native Rückgabewertprüfung,
terminale Event-Ownership oder Cleanup zu schwächen. Die Arbeit bleibt innerhalb
der vom Nutzer freigegebenen fokussierten TAC1-Prüfgrenze.

## Runtime-Evidence

Dieser Produkt-Checkpoint enthält kompilierten Adapternachweis, keine Live-Host-
Behauptung. Der gepinnte NGINX-Quellstand belegt unabhängig die leere terminale
Bufferform und `ngx_buf_special`-Semantik. Root-Master-/Nobody-Worker-Host,
Clientbytes, physische Events, natives EOS und Folge-Cleanup werden nach normaler
Integration durch #410 in der nachgelagerten #416-I12-Kampagne erzeugt und an
die Revision gebunden.

## Bekannte Einschränkungen

Die Produkt-Fixture startet selbst weder NGINX noch libModSecurity. Sie belegt
den Adapterzweig und die native Aufrufgrenze mit kompilierten kontrollierten
Abhängigkeiten. Historische I12-Ergebnisse bleiben an ihre ursprünglichen
Revisionen gebunden und werden nicht auf diese Änderung übertragen.

## Verbleibende Risiken

Der integrierte Hostlauf muss beide leeren Framingvarianten, exaktes natives
EOS, Finish/Free, clientseitigen Status und Framing sowie gesunde
Nachbarrequests noch belegen. Jeder dortige Fehler blockiert die NGINX-Abnahme,
statt aus dieser Unit-Regression abgeleitet zu werden.

## Nicht ausgeführte Prüfungen mit Begründung

Revisionsgenaue #410/#416-Host-, Report-, Sonar- und GitHub-Prüfungen sind an
diesem Produkt-Checkpoint nicht ausgeführt, weil der Produktfix noch nicht
committet und integriert ist. Deployment und Merge nach master liegen außerhalb
des freigegebenen Auftrags.

## Finaler Diff- und Review-Status

Der aktuelle Produktdiff beschränkt sich auf NGINX-Quelle, NGINX-/Common-
Fixtures, paarige NGINX-Dokumentation und diesen Record. Ein unabhängiges
Quellreview fand keinen blockierenden Korrektheits- oder Sicherheitsfehler und
forderte den nun abgedeckten Sync-Steuerfall. Finaler Commit, Remote-SHA und
vollständige Validierung werden erst nach normaler Lieferung eingetragen. Dieser
Record erlaubt keinen Merge.
