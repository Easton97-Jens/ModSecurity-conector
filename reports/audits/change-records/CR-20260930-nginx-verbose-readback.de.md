# Change Record: exakte NGINX-Version mit ausführlichen Build-Metadaten

**Sprache:** [English](CR-20260930-nginx-verbose-readback.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260930-nginx-verbose-readback |
| Datum (UTC) | 2026-09-30 |
| Basis-Revision | `e14e2a7d2e3d6f4be8d7ff50d1e387d3e553fa8e` |

## Motivation und Problemstellung

Die vom Eigentümer beauftragte Reparatur in PR #393 fortsetzen. In
[Lauf 36713711425, Job 109881375276](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/36713711425/job/109881375276)
bestanden beide On/Off-Laufzeitzellen vor dem Fehler bei der Veröffentlichung.
Der Harness protokolliert `nginx -V`, der Writer verlangte dagegen eine
einzeilige `-v`-Ausgabe. Compiler- und Configure-Metadaten führten zur Ablehnung.

## Akzeptanzkriterien

Die exakte freigegebene erste Versionszeile mit üblichen Build-Metadaten
akzeptieren; falsche, fehlende, doppelte oder widersprüchliche Versionszeilen
und unerwartete Metadaten ablehnen. Alle bestehenden Nachweis- und
Publikationsprüfungen erhalten. Den Folgecommit über den Hosted-Workflow prüfen.

## Implementierungsentscheidung und Begründung

Den Byte-Parser in ein kleines Prädikat auslagern. Die erste Zeile bleibt
exakt; danach sind nur druckbare Compiler-, TLS-Build-, SNI- und Configure-
Metadaten erlaubt. Metadaten werden weiterhin als Quelle gehasht, niemals in
öffentliche Nachweise kopiert. Zwei Regressionen prüfen beide Betriebsmodi.

## Geänderte Dateien

`ci/runtime/lifecycle/write-nginx-functional-a-evidence.py`,
`tests/test_nginx_functional_evidence.py` und dieses EN/DE-Record-Paar.

## Ausgeführte Befehle

Ein isolierter In-Process-Unittest-Lauf unter Python 3.13.5 verwendete per
Byte-Hash geprüfte aktuelle Writer-/Testquellen und ein minimales Workflow-
Versionsfixture. Die neue Erfolgsregression scheiterte mit dem alten Writer
zweimal. Mit der Korrektur bestanden alle 11 Tests ohne Fehler oder Skips.
AST-Parsing und Leerzeichenprüfungen bestanden. Hochgeladene Quell-Blobs
werden mit den getesteten Bytes verglichen. Das ist kein vollständiger
Checkout-Test oder lokaler RTK-Lauf.

## Security-Auswirkung

Keine Änderung an Versionspins, Quellidentitäten, Policy, Berechtigungen,
Sandbox, geschütztem Broker oder Sonar-Konfiguration. Falsche Releases und
passende Präfixe bleiben abgelehnt. Grenzen, sichere Dateizugriffe,
Identitätsprüfungen, Redaktion, Callbacks, Lifecycle-Marker und einmalige
Veröffentlichung bleiben unverändert.

## Runtime-Evidence

Der bisherige Hosted-Job belegt erfolgreiche On/Off-Zellen, aber eine
fehlgeschlagene Veröffentlichung. Ein erfolgreicher nativer Lauf nach dieser
Korrektur wird hier nicht behauptet; Folgeworkflow und PR-Verifikation
müssen diesen Nachweis liefern.

## Bekannte Einschränkungen

Lokale GitHub-DNS-Auflösung und der Projekt-RTK-Wrapper sind nicht verfügbar.
Vollständige Hosted-CI, native Nachweisveröffentlichung und frische Sonar-
Ergebnisse müssen für den tatsächlichen Folgecommit abgerufen werden.

## Verbleibende Risiken

Neue Upstream-Metadatenformate können eine geprüfte Parseränderung erfordern.
Unerwartete Zeilen werden absichtlich abgelehnt und nicht ignoriert.

## Nicht ausgeführte Prüfungen mit Begründung

Kein lokaler vollständiger Checkout-Build oder nativer Lauf, da Checkout und
Werkzeuge fehlen. Die unveränderten Hosted-Workflows validieren den
gepushten Commit unabhängig.

## Finaler Diff- und Review-Status

Begrenzte Folgekorrektur zu den eingespielten Framework- und ModSecurity-Checks.
Kein Merge, Master-Push, Force-Push oder Start alter lokaler Skripte autorisiert.
