# B09-NGINX-Kontextisolation bei internen Redirects

**Sprache:** [English](CR-20260930-nginx-b09-context-isolation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260930-nginx-b09-context-isolation |
| Datum (UTC) | 2026-09-30 |
| Basis-Revision | e3f97d22446b8919e1d7f29de71ddf97bc735e92 |
| Lieferziel | Bestehender Parent-Draft-PR #391; normaler Folgecommit, kein Merge |

## Motivation und Problemstellung

Die echte B09-Host-Fixture für Fehlerseiten zeigte auf der Basis-Revision einen sicherheitsrelevanten Bypass: /origin-on leitet intern zum geschützten /target um, doch ein P2-Deny lieferte 200 statt 403. NGINX löscht beim Redirect seinen Modulkontext. Der Connector-Access-Handler stellte danach die Cleanup-eigene Ursprungstransaktion mit den erlaubenden Ursprungsregeln wieder her und übersprang die Initialisierung mit den geschützten Regeln der Ziel-Location.

## Akzeptanzkriterien

Ein aktiviertes umgeleitetes Ziel muss eine Transaktion aus seiner aktuellen Location-Konfiguration initialisieren. Die bestehende Hosted-Fixture behält ihre strengen Assertions: Ein block-Marker liefert 403, erreicht den geschützten Backend nicht und erzeugt Regel 9803911 mit einer nativen Phase-2-Entscheidung. Die legitime Kontrolle liefert 200 mit dem Zielbody. Deaktivierte und aktiv erlaubende Ursprünge, wiederholte Ablehnungen und ein späterer erlaubter Request bleiben abgedeckt. Der Cleanup-Recovery-Pfad bleibt außerhalb der Access-Initialisierung verfügbar.

## Implementierungsentscheidung und Begründung

Nur ngx_http_modsecurity_access_handler liest den rohen aktuellen ngx_http_get_module_ctx-Wert, wenn es über die Initialisierung einer Transaktion entscheidet. Es verwendet nicht mehr ngx_http_modsecurity_get_module_ctx; dessen Cleanup-Fallback bleibt unverändert für Request-Read-, Filter-, Logging- und Post-Access-Finalisierungspfade. Ein aktiviertes Redirect-Ziel erhält damit einen frischen Kontext und sein eigenes Regelset, während ein deaktiviertes Ziel die vorhandene Post-Access-Behandlung erhält.

Die fokussierte Python-Regression ergänzt einen Source-Contract für diese Access-Handler-Grenze. Sie ergänzt die echte gehostete HTTP/1-B09-Fixture, statt sie zu ersetzen. Die frühere /origin-Sonar-Literalkorrektur und der vorhandene Intervention-Klassifizierer werden bewusst nicht verändert.

## Security-Auswirkung

Die betroffene Vertrauensgrenze ist der Übergang von einer Ursprungs-Location zu einem geschützten internen Fehlerseitenziel. Ein vom Client steuerbarer Request-Header kann die Deny-Regel der Fixture auswählen, darf aber nicht dazu führen, dass das Ziel die permissive Ursprungstransaktion übernimmt. Die Korrektur stellt die P2-Durchsetzung der Ziel-Location wieder her, ohne Worker-Isolation, Cleanup-, Logging-Kontrollen, CI-Berechtigungen oder Assertions abzuschwächen.

## Geänderte Dateien

- connectors/nginx/src/ngx_http_modsecurity_access.c
- tests/test_nginx_error_page_intervention.py
- reports/audits/change-records/CR-20260930-nginx-b09-context-isolation.md
- reports/audits/change-records/CR-20260930-nginx-b09-context-isolation.de.md

Keine Framework- oder MRTS-Quelle, kein Gitlink, Workflow, Dependency, Berechtigung oder Sonar-Konstantenänderung gehört zu dieser Korrektur.

## Ausgeführte Befehle

Vor der nativen Änderung schlug der neue fokussierte Source-Contract fehl, weil der Access-Handler noch ngx_http_modsecurity_get_module_ctx aufrief. Nach der Änderung bestand python -m unittest tests.test_nginx_error_page_intervention.NginxErrorPageContextContractTests -v. Der vollständige Befehl python -m unittest tests.test_nginx_error_page_intervention -v erreichte den bestandenen Source-Contract, stoppte danach aber, weil diese lokale Windows-Umgebung keinen C17-Compiler besitzt; daraus wird kein bestandener kompilierter Klassifizierer-/P1-/P2-Seam abgeleitet.

Die erforderliche echte Host-Validierung bleibt der Exact-Head-GitHub-Workflow. Der Basis-Revision-Lauf 36708275117, Job 109863649363, ist der reproduzierte Fehler; nach der Auslieferung ist ein frisches Successor-Head-Ergebnis erforderlich.

Die direkten Checker für zweisprachige Dokumentation und Repository-Pfade meldeten nur bereits vorhandene fehlende Linkziele des `modules/ModSecurity-test-Framework` in unveränderter Dokumentation; keiner fand ein durch diese Änderung eingeführtes Problem.

## Runtime-Evidence

Die vorhandene gehostete Fixture ist der maßgebliche Runtime-Nachweis für diesen Scope. Sie verwendet einen Root-NGINX-Master, einen getrennten Non-Root-Worker, private Laufpfade und provisionierte Exact-Head-Artefakte. Aus dem Source-Contract oder der nicht verfügbaren Windows-Toolchain wird kein neuer lokaler nativer Runtime-Claim abgeleitet.

## Nicht ausgeführte Prüfungen mit Begründung

Lokale C17-Kompilierung, der vollständige Python-B09-Seam, die Make-Wrapper `make check-bilingual-docs` und `make check-doc-links` sowie die echte NGINX-Fixture können in der aktuellen Umgebung nicht laufen, weil der notwendige Compiler, Make, die NGINX-/libmodsecurity-Runtime und die Root-Worker-Provisionierung fehlen. Die direkten Dokumentationschecker melden nur die bereits fehlenden Ziele des Framework-Submoduls. Es wurden keine Pakete installiert, Dienste geändert, Tests gelockert oder Ersatz-Runtimes verwendet. Frische gehostete Successor-Head-Evidence steht zum Zeitpunkt dieses Records noch aus.

## Bekannte Einschränkungen

Die B09-Fixture beweist HTTP/1, einen internen URI-Fehlerseitenschritt und ein P2-Headerprädikat. Sie etabliert kein Verhalten für Named Locations, beliebige Rekursion, Body-Transfer-Modi, Response-Phase, andere Transporte oder Deployments.

## Verbleibende Risiken

Wenn ein aktiviertes Ziel seine eigene Transaktion erzeugt, beobachtet das abschließende Logging naturgemäß diesen Zielkontext. Diese fokussierte Korrektur führt keine Richtlinie zur Zuordnung mehrerer Audit-Transaktionen ein. Der beibehaltene Cleanup-Fallback unterstützt weiter die Post-Access-Behandlung, wenn kein aktivierter Zielkontext erzeugt wird, einschließlich einer deaktivierten Ziel-Location. Der gehostete B09-Nachweis muss die beobachtbare Entscheidung des geschützten Ziels bestätigen.

## Finaler Diff- und Review-Status

Der Scope beschränkt sich auf die native Access-Kontextentscheidung, einen fokussierten Regressions-Contract und diesen gekoppelten Nachvollziehbarkeits-Record. Die bestehenden B09-Host-Assertions bleiben streng. Die Auslieferung ist auf einen normalen Folgecommit und Push auf dem bestehenden Draft-PR-Branch beschränkt; kein Force-Push oder Merge ist autorisiert.
