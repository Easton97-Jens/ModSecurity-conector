# Change Record: CR-20261008-nginx-standard-h1-forwarding

**Sprache:** [English](CR-20261008-nginx-standard-h1-forwarding.md) | Deutsch


## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-standard-h1-forwarding |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `e3fcd1c7d5a9ce09abde7c9593a15690d7ed08f0` |

## Motivation und Problemstellung

Der dokumentierte Harness-Standard ist HTTP/1; der native Parent-Full-Lifecycle-Aufruf ließ das Downstream-Protokoll jedoch bei Framework-Auswahl und Initialisierung aus. Das Framework verweigerte seinen Standard `any` für einen NGINX-Full-Lifecycle-Plan korrekt vor Requests.

## Akzeptanzkriterien

Der Standardaufruf `make full-lifecycle-nginx` reicht den bestehenden HTTP/1-Standard ohne externen Eingriff weiter; explizite kompatible H2/H3-Auswahlen bleiben in reinen Plantests selektiert. Ungültige/widersprüchliche Werte scheitern vor der Auswahl; generische und andere Connector-Pläne bleiben unverändert.

## Implementierungsentscheidung und Begründung

Den bestehenden NGINX-Downstream-Standard nur im NGINX-Full-Lifecycle-Profil einmal auflösen, auf Kompatibilität mit dem bestehenden Buildprofil prüfen, an den Harness exportieren und identisch an Auswahl und Initialisierung übergeben. Ein erweitertes Buildprofil wählt kein anderes Transportprotokoll.

## Geänderte Dateien

`ci/runtime/lifecycle/run-no-crs-baseline.sh`, `tests/test_nginx_full_lifecycle_protocol_wiring.py` und dieses EN/DE-Nachweispaar. Framework, MRTS, Gitlinks, Dependencies, Required-Definitionen und Harness-Guardrails bleiben unverändert.

## Ausgeführte Befehle

Die dynamische Altcode-Regression des Standardaufrufs scheitert an der echten Framework-Auswahl (Exit 1). Fokustests verwenden echte Make-/Framework-select/init-Aufrufe und stoppen vor Host-Ausführung. Bestehende Selection-/Profil-/H1-Request-Tests: 20 PASS, 0 SKIP. Shellsyntax und `git diff --check` grün. ShellCheck behält acht bestehende Diagnosen ohne neue Codes/Schweregrade/Meldungen. Dynamische Standard-/Profilmatrix: `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_nginx_full_lifecycle_protocol_wiring` mit `FRAMEWORK_TEST_PYTHON` auf der gepinnten Framework-Umgebung: 9 Tests PASS, 0 SKIP, Exit 0; Initializer-Sentinel 79 stoppt absichtlich vor Runtime. Der Coordinator wiederholte dieselben neun Tests unabhängig (Exit 0).

## Security-Auswirkung

Nicht unterstützte Downstream-/Buildprofil-Kombinationen werden weiterhin abgewiesen. H1-Evidence erfüllt keine H2/H3-Records. Keine Containment-, Projection-Freshness-, Validator- oder Vertrauensgrenze wird gelockert.

## Runtime-Evidence

Die Regression dieses Commits belegt ausschließlich den Plan, keine Host-Runtime. Ein frischer realer Standardaufruf-Fokus und Full Lifecycle gegen den finalen A/B/C-Stand folgen; kein externer H1-Injektor wird verwendet.

## Bekannte Einschränkungen

Explizite kompatible H2/H3-Pläne sind geprüft, keine H2/H3-Runtime. Fehlende Required-Host-/Fault-/Common-Szenarien und Events werden dadurch nicht erzeugt.

## Verbleibende Risiken

Kanonische Coverage und unabhängige Protected-Voraussetzungen bleiben getrennte Pflichten; erfolgreiche Auswahl beweist weder Requests noch Evidence.

## Nicht ausgeführte Prüfungen mit Begründung

Frischer Standard-Host-Fokus/Full-E2E, vollständiger Lint und CI/Sonar des veröffentlichten Heads folgen den atomaren Fixes. Ruff fehlt; keine Paketinstallation versucht.

## Finaler Diff- und Review-Status

Vollständiger begrenzter Diff und Default-Vertrag geprüft. Der atomare B-Commit bleibt getrennt von Binärhashing und S5778; keine fremde Protocol-Arbeit oder Evidence enthalten.
