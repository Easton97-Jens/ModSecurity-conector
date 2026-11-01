# Change Record: CR-20261101-sec-traefik-native-001

**Sprache:** [English](CR-20261101-sec-traefik-native-001.md) | Deutsch

Gezielte Produktkorrektur; sämtliche Regressionen und Testadapter gehören dem Framework.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261101-sec-traefik-native-001 |
| Datum (UTC) | 2026-11-01 |
| Basis-Revision | `a6001a09210bc9516256d28af5da45d73f0fe2f2` |

## Motivation und Problemstellung

SEC-TRAEFIK-NATIVE-001: Ein nichtterminales informatorisches WriteHeader verbrauchte
Request-EOS, finales P3 und Common-Commit. Ein erst final gesetzter Schutzheader
umging P3; eine echte HTTP-Regression beobachtete finales 200 und geschützte
Upstream-Bytes statt der erwarteten Ablehnung.

## Akzeptanzkriterien

Nichtterminale 1xx lassen den finalen P2-/P3-/Commit-Zustand verfügbar. Finale
Header und Status erreichen P3 genau einmal; Allow, Deny, Redirect, begrenztes
Streaming, P4/EOS, 101/Hijack und Cleanup bleiben gültig. Echte Informationsantworten
und die ausgewählte Ubuntu-Traefik-/Plugin-/UDS-/Common-/libmodsecurity-Grenze prüfen.

## Implementierungsentscheidung und Begründung

100--199 außer 101 vor der finalen Response-Vorbereitung behandeln. Begrenzte
Header-Validierung beibehalten und Informationsheader direkt weiterleiten, ohne
die Host-Headermap zu leeren oder Engine-Zustand zu ändern. Bestehende finale und
Upgrade-Pfade bleiben für P3 und Commit zuständig. Kein Response-Bodypuffer kam hinzu.

## Geänderte Dateien

`connectors/traefik/native_middleware/middleware.go`, `docs/connectors/traefik.md`,
`docs/connectors/traefik.de.md` und dieses EN/DE-Change-Record-Paar. Der unabhängige
Framework-Branch besitzt Tests, Fixtures, Adapter, Inventar und Testdokumentation.
Die autorisierte Integrationsnachbesserung aktualisiert außerdem Framework-Gitlink,
`ci/tooling/project-versions.lock.json` und die 22 registrierten Workflow-Verbraucher
auf den tatsächlichen Framework-#146-Squash-Merge-Commit
`c3f3aa4747315bdbfc7f6443edb47cef54a4e804`. Komponenten- und MRTS-Pins bleiben unverändert.

## Ausgeführte Befehle

RTK-gekapselter öffentlicher Framework-Overlay-/Inventar-Aufruf mit ausdrücklichem
CONNECTOR_ROOT, exakter Basis-CONNECTOR_REVISION, TEST_ROOT und externem Output:
31 neue expandierte Go-Fälle bestanden nach dem Fix. Der echte HTTP-Reproducer
schlug vorher fehl; drei Kontrollen ohne 1xx bestanden. Frische native Modulprüfungen
`go test -race -mod=readonly -count=1 -overlay <framework-overlay> ./...` und
`go vet -mod=readonly -overlay <framework-overlay> ./...` bestanden. `gofmt` wurde
angewendet. Parent-Zweisprachigkeits-/Link-/Change-Record- und Framework-
Dokumentationsprüfungen bestanden. Gitleaks 8.30.1 fand keine Leaks im Snapshot der
geänderten Dateien. Committed-Pair-Ergebnisse werden nach Ausführung mit der
PR-Verifikation dokumentiert.

## Security-Auswirkung

Stellt prospektive Final-Response-Header-Durchsetzung nach Informationsantworten
wieder her. Finales P3-Deny/Redirect hält Upstream-Bytes zurück und erlaubt den
eigenen Ablehnungsbody der Middleware. Informationsheader behalten konfigurierte
Limits. Keine Isolation, Identitäts-, Engine- oder Validierungskontrolle wurde geschwächt.

## Runtime-Evidence

Ubuntu 26.04.1; Go 1.27.3; gepinntes Traefik 3.7.13. Framework-Probelauf `host-run-5`
bestand alle vier Probes: 103/Deny 403, ohne 103/Deny 403, 103/Allow 201 und legitimer
Folgezugriff 201 auf derselben TCP-Verbindung. Jeder hatte genau ein korreliertes
finales P3; Ablehnungen passten zu Rule 1199001 und zeigten nur den eigenen
Ablehnungsbody. Kein Recovery-Panic verblieb; Prozesse, private Sockets und
temporäre Workspaces wurden bereinigt. Evidence liegt extern unter
`/var/tmp/codex/ModSecurity-conector/sec-traefik-native-001/host-run-5`.
Dieser Probelauf verwendete Basis-HEAD plus Middleware-SHA-256
`03944b42c9d64391eda579aa0cdd5a6cc239b02baf5907ca1c6357a61385c337`;
er ist von den drei separat im PR berichteten Committed-Pair-Abnahmewiederholungen
zu unterscheiden.

## Bekannte Einschränkungen

Frühere Hostversuche scheiterten an der portablen privaten UDS-Pfadlängengrenze,
Route-Readiness-Timing oder vorzeitiger Testclient-Cancellation während P4/Cleanup.
Diese Fehlschläge bleiben erhalten. Der Framework-Adapter beobachtet nun physisches
EOF beim finalen Connection: close-Probe; Panic-Erkennung bleibt aktiv. Keine Aussage
gilt für andere Connectoren, forwardAuth, HTTP/2/3, MRTS oder eine allgemeine Protokollmatrix.

## Verbleibende Risiken

Der rohe Hijack-Ownership-Vertrag bleibt erhalten und wird nicht neu entworfen.
Sourcetests belegen nicht jedes Upgrade- oder Deployment-Szenario. Bestehende CI-
und Quality-Gates müssen vor einem separat autorisierten Merge am ausgelieferten
PR-Head bewertet werden.
Der Benutzer hat die reguläre Integration von Framework #146 und danach
Connector #435 jetzt unter der Bedingung abschließender Head-Prüfungen und
frischer Abnahme des neuen Connector-/gemergten-Framework-Paars autorisiert.
Die Hostnachweise des früheren Paars sind historisch und ersetzen diese Abnahme
nicht.

## Nicht ausgeführte Prüfungen mit Begründung

Keine vollständige Connector-/Protokoll-/MRTS-Matrix: ausdrücklich außerhalb dieser
Korrektur. Kein Produktionsdeployment. Hosted-CI-/Sonar-Status und die drei
Hostwiederholungen des neuen Paars gehören zur Verifikation des tatsächlichen
finalen PR-Heads, nicht zum früheren lokalen Ausführungsnachweis. Direkter
master-Push oder administrativer Bypass ist nicht autorisiert.

## Finaler Diff- und Review-Status

Eine unabhängige Read-only-Kandidatenprüfung fand keinen konkreten verbleibenden
Bypass oder Regression an der geänderten Grenze. Produkt und Framework bleiben
getrennte Commits und separat reviewbare PRs. Framework #146 wurde nach bestandenen
finalen Head-Prüfungen und Sonar-Gate ohne offene PR-Befunde/Hotspots regulär
per Squash gemergt. Der native reine Datenverifier akzeptierte den tatsächlichen
Merge-Commit; der native Synchronisierer aktualisiert nur die registrierten
Framework-Identitätsziele. Connector #435 muss mit genau diesem gemergten
Framework-Pin ein neues finales Review, CI/Sonar und drei unabhängige reale
Hostläufe bestehen, bevor sein regulärer Merge erfolgt. Die fünf neuen
Framework-Sonar-Befunde wurden ohne Unterdrückungen oder Gate-Änderungen behoben;
unabhängige Baseline-Inventare (Framework 83, Connector 5) bleiben getrennt unter
dem externen Evidence-Root `integration/`.
Die Zweisprachigkeitsprüfung des neuen Paars zeigte anschließend eine falsche
Reihenfolge der deutschen Sprachumschaltung im neuen Framework-Leitfaden.
Framework #149 bereitet die gezielte Dokumentationskorrektur vor; er liegt
außerhalb der zwei ausgewählten Merge-PRs und benötigt eine zusätzliche Auswahl.
Die Connector-Integration bleibt blockiert, bis diese Abhängigkeit aufgelöst
und das daraus entstandene finale Paar frisch verifiziert ist.
