# Change Record: Vertrauenswürdige physische NGINX-Event-Provenienz

**Sprache:** [English](CR-20261022-nginx-trusted-event-provenance.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20261022-nginx-trusted-event-provenance` |
| Datum (UTC) | `2026-10-22` |
| Basis-Revision | `c03352ba160675a94bf63125cceaa25367f52c27` |
| Pull Request | [#382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382) |

## Motivation und Problemstellung

Die ausgewählten NGINX-Timeout- und Transportverträge verlangen `run_id`,
`transport_case_id` und `connection_id` gemeinsam im selben physischen JSONL-
Event. Der native NGINX-Adapter schrieb diese Felder nicht. Controller-Receipts
konnten diese Producer-Lücke nicht beheben, ohne Eventinhalt zu erfinden.

## Akzeptanzkriterien

- Die Provenienz stammt ausschließlich aus administrativ kontrollierter
  Prozesskonfiguration und niemals aus HTTP-Headern.
- Run- und Case-ID fehlen beide oder sind beide gültige ASCII-Tokens mit
  1–128 Bytes aus `[A-Za-z0-9_.:-]`.
- Die Verbindungs-ID stammt aus der tatsächlichen NGINX-Verbindungsnummer;
  Reuse folgt der Requestanzahl dieser Verbindung.
- Beide echten JSONL-Writer projizieren die Provenienz vor der Common-
  Serialisierung auf ihre private Eventkopie; das Caller-Event bleibt gleich.
- Ungültige oder unvollständige Provenienz erzeugt kein ungebundenes physisches
  Event und erhält den bestehenden Fehlervertrag des jeweiligen Writers.
- Die integrierte Root-Master-/Nobody-Worker-Hostkampagne weist die Felder im
  tatsächlichen physischen Event nach, bevor I12 einen PASS beansprucht.

## Implementierungsentscheidung und Begründung

Beide nativen Writer-Tails verwenden einen begrenzten Helper. Ein vollständig
fehlendes Paar erhält das bisherige optionale Verhalten. Bei aktiver
Konfiguration validiert der Helper beide Prozessumgebungswerte ohne unbegrenztes
Lesen vor der Prüfung, leitet `nginx-<connection-number>` ab und setzt das
Reuse-Flag vor dem strikten Common-Serializer. NGINX muss beide Werte mit
`env`-Direktiven im Main-Kontext ausdrücklich erhalten. Damit bleibt die
Vertrauensgrenze bei der administrativ kontrollierten Prozesskonfiguration und
der Producer selbst besitzt die Felder, nicht ein Bericht.

## Geänderte Dateien

- `connectors/nginx/src/ngx_http_modsecurity_common.h`
- `ci/checks/connectors/nginx/check-nginx-common-adoption.py`
- `tests/test_nginx_bounded_event_uri.py`
- `tests/test_nginx_common_adoption.py`
- fokussierte P1-/P3-/Request-/Cleanup-Extraction-Fixtures
- `connectors/nginx/README.md` und `connectors/nginx/README.de.md`
- dieses englisch-deutsche Change-Record-Paar

## Ausgeführte Befehle

Alle Befehle wurden durch RTK ausgeführt. Rohe Nachweise liegen unter
`/var/tmp/codex/ModSecurity-conector/runs/pr416-nginx-complete-20261022/product-382/provenance`.

| Prüfung | Beobachtetes Ergebnis |
| --- | --- |
| Exact-Writer-Regression vor der Produktänderung | Exit 1: neun Tests mit 46 erwarteten Untertestfehlern, weil den physischen JSONL-Events die geforderte Provenienz fehlt. `pre-fix.log`, SHA-256 `0e1f9f9af6e805490a4afa5d0bb53a666c5ca3ddb3152fed51d059dde5514913`. |
| Fokussierte Writer-, P1-/P3-/Request- und Adoption-Mutationstests nach der Änderung | Exit 0: 36 Tests bestehen. `post-fix.log`, SHA-256 `4d53de0f0ca1ec1986cb5527c93d12fb79a228dd9445c2dea90c7c28ef9dfc53`. |
| Finale Exact-Writer-Suite | Exit 0: zehn Tests bestehen; geprüft sind fehlende, vollständige, unvollständige, ungültige, 128-/129-Byte-, Verbindungsnummer-, Reuse- und unveränderte Sourceevent-Pfade. |
| `make check-nginx-c17` | Exit 0; die NGINX-/Common-C17-Kompilierung mit Warnings-as-Errors besteht. |
| Finale NGINX-Produktregressionsgruppen | Exit 0: Zwei getrennte finale Läufe bestehen 165 und 82 Tests (247 insgesamt), einschließlich Exact-Writer-, Adoption-, Sicherheitsgrenz-, Native-Result-, Mutations- und Cleanup-Abdeckung. |
| Finales `make build-nginx` | Exit 0 gegen gepinntes NGINX 1.31.6 und den vorbereiteten libModSecurity-Runtimecache aus dem finalen Produktquellstand unter `product-382/runtime-final`. Dies ist ausschließlich Build-Evidence. |
| NGINX-C-Standard-Wiring, Repository-Pfad-, zweisprachige Dokument-, Change-Record- und Diffprüfungen | Exit 0; das Change-Record-Ergebnis ist ausschließlich strukturell. |

Live-Root-/Nobody-Vererbung und physische Eventergebnisse bleiben nachgelagerte
I12-Arbeit; keine ausstehende Prüfung wird als PASS bezeichnet.

## Security-Auswirkung

Die Änderung ergänzt einen engen vertrauenswürdigen Metadateneingang. Werte
werden nur als validiertes Paar aus der Prozessumgebung akzeptiert, deren
Erhalt der NGINX-Administrator auswählt. Kein requestgesteuerter Header, keine
URI und kein Body liefert diese Felder. Ungültige Konfiguration lässt den
Event-Write fehlschlagen, statt falsch gebundene Evidence zu erzeugen. Die
Arbeit bleibt innerhalb der vom Nutzer freigegebenen fokussierten TAC1-Grenze.

## Runtime-Evidence

Kompilierte Fixtures belegen die echten Writer- und Common-Serializergrenzen.
Sie belegen weder Worker-Vererbung noch ein Live-Host-Event. Die nachgelagerte
#416-I12-Kampagne muss einen Root-Master mit Nobody-Workern, ausdrückliche
`env`-Erhaltung, den geladenen Connector und libModSecurity ausführen und alle
drei Identitäten gemeinsam im physischen Event sowie Native-/Client-/Cleanup-
Evidence prüfen.

## Bekannte Einschränkungen

Die beiden Umgebungs-IDs sind eine prozessweite Kampagnenidentität. Sie ändern
sich nicht zwischen Requests einer Keepalive-Verbindung. Unabhängige Case-IDs
benötigen daher unabhängige NGINX-Prozessläufe. Verbindungsnummern gelten im
deklarierten Run und werden nicht als global eindeutig dargestellt. Ein
Fehler der Hostvererbung oder der physischen Eventprüfung blockiert I12.

## Verbleibende Risiken

Der integrierte Hostlauf muss noch belegen, dass ein Root-Master beide Variablen
für Nobody-Worker erhält und dass die exakten Run-, Fall- und Verbindungswerte
jedes physische Event erreichen. Jede Abweichung blockiert die NGINX-Abnahme,
statt in einem Receipt oder Bericht repariert zu werden.

## Nicht ausgeführte Prüfungen mit Begründung

Revisionsgenaue #410/#416-Host-, Report-, Sonar- und GitHub-Prüfungen sind an
diesem Produkt-Checkpoint nicht ausgeführt, weil die Produktänderung noch nicht
committet und integriert ist. Deployment und Merge nach master liegen außerhalb
des freigegebenen Auftrags.

## Finaler Diff- und Review-Status

Die Produktänderung beschränkt sich auf NGINX-Eventprojektion sowie NGINX-
eigene Prüfungen, Fixtures und paarige Dokumentation. Finaler Commit/Remote-
Stand und revisionsgenaue Hostevidence stehen aus. Dieser Record erlaubt keinen
Merge.
