# Change Record: Parent-Cache-Test-Behebung eines unbenutzten Lokals für SonarQube Cloud S1481

**Sprache:** [English](CR-20260721-sonar-s1481-cache-test-unused-local.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260721-sonar-s1481-cache-test-unused-local |
| Datum (UTC) | 2026-07-21 |
| Basis-Revision | 2ade0d40983b7af21a65b8cd2884866b85626393 |
| Tracking | Ein Parent-only-python:S1481-Code-Smell: AZ9cRzAcHhV2CayPTP44; vorgehaltene Finding-ID FND-SONAR-0016. |
| Grenze | Nur der Parent-NGINX-Runtime-Component-Cache-Contract-Test sowie dieses Parent-Traceability-Paar/der Index; Framework, MRTS, Gitlinks, Production-Runtime-Component-Code, Scanner-Konfiguration und Quality Gates bleiben unverändert. |

## Motivation und Problemstellung

`RuntimeComponentCacheContractTest.test_nginx_discards_marker_owned_partial_root_before_build`
definiert einen verschachtelten NGINX-Build-Mock. Der Mock liest
`NGINX_BUILD_DIR` in `active_build_path`, aber keine Assertion, kein Fixture,
kein Artefaktpfad und kein Control-Flow-Branch beobachtet dieses Lokale.
SonarQube-Cloud-Regel `python:S1481` meldet die tote Zuweisung. Der umgebende
Test muss weiterhin Managed-Partial-Root-Cleanup, NGINX-Artefakterstellung,
Executable Permissions und Cache-Manifest-Readiness prüfen, ohne eine
Scanner-Suppression einzuführen.

## Akzeptanzkriterien

- Nur die unbenutzte `active_build_path`-Zuweisung für
  `AZ9cRzAcHhV2CayPTP44` entfernen.
- Die Nutzung von `NGINX_PREFIX` durch den Mock sowie jede vorhandene
  Partial-Cache-Cleanup-, Artefakt-, Executable- und Manifest-Assertion
  erhalten.
- Vor der Delivery Syntax der ausgewählten Python-Datei, das vollständige
  fokussierte Cache-Contract-Testmodul, Bilingual-/Change-Record-Checks und
  finale Diff-Validierung ausführen.
- Bevor behauptet wird, dass der Key behoben ist, frische SonarQube-Cloud-
  Evidence für den exakten Draft-PR-Head einholen; der PR muss ungemergt
  bleiben.

## Implementierungsentscheidung und Begründung

Die Zuweisung wird gelöscht statt umbenannt oder durch `_` ersetzt: Der Wert
hat keine beobachtbare Verwendung, während `active_nginx_prefix` der einzige
abgeleitete Pfad für die Erstellung der Binary-, Module- und
Configuration-Fixtures bleibt. Dies ist eine Ein-Source-/Ein-Key-
Maintainability-Korrektur und kein mechanischer projektweiter
`python:S1481`-Sweep.

## Security-Auswirkung

Die Änderung ist auf einen Parent-Test-Mock beschränkt und entfernt keine
Validation-, Containment-, Dependency-, File-Path-, Network-, Subprocess-,
Authentication-, Authorization-, Logging-, Scanner-, Quality-Gate-,
Suppression-, `NOSONAR`- oder False-Positive-Control. Die fokussierte
Bewertung ergab keine Änderung einer Security Boundary, die eine separate
Security-Finding-Remediation erfordert.

## Geänderte Dateien

- tests/test_runtime_component_cache_contract.py
- reports/audits/change-records/README.md und README.de.md
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| Selected Parent Virtual-Environment Identity Check | bestanden: `/root/git/ModSecurity-conector/.venv/bin/python`, Python `3.14.4`, Venv-Prefix verifiziert. |
| Selected-File-Python-Syntax mit externem Bytecode-Cache | bestanden: `python -B -s -m compileall -q tests/test_runtime_component_cache_contract.py`. |
| Fokussiertes `tests.test_runtime_component_cache_contract`-`unittest`-Modul | bestanden: 25 Tests. |
| Initial Auxiliary Source-Structure Assertion | nur fehlgeschlagen, weil ihr breiter Count das separate, verwendete Apache-`active_build_path` einschloss; kein Product-Check schlug fehl. |
| Corrected NGINX-Block Source-Structure Assertion | bestanden: Der `build_nginx`-Mock enthält weder `active_build_path` noch `NGINX_BUILD_DIR` und behält `active_nginx_prefix`. |
| Fokussierter Change-Record-Pair-Contract | bestanden: erforderliche Abschnitte, übereinstimmende Identity-Werte, Heading Levels und Table Structure. |
| `tests.test_bilingual_docs`-`unittest`-Modul | bestanden: 11 Tests. |
| `rtk proxy git diff --check` | bestanden. |

Hosted-Exact-Head-Evidence bleibt bei Erstellung des Records zukünftige Arbeit;
dieser Record behauptet keine unbeobachteten CI-, SonarQube-Cloud-, Review- oder
Delivery-Ergebnisse.

## Runtime-Evidence

Es ändern sich weder Connector-Runtime-Pfade noch die Production-
Runtime-Component-Implementierung. Der fokussierte Parent-Contract-Test ist
das Verhalten-Control für den Mock, der NGINX-Artefakte im
Cache-Recovery-Szenario vorbereitet.

## Nicht ausgeführte Prüfungen mit Begründung

- Eine Connector-Build-/Runtime- oder CRS/MRTS-Matrix ist nicht anwendbar: Es
  ändern sich weder Connector-Source noch Production-Lifecycle,
  Transportverhalten, Framework-Dateien oder MRTS-Dateien.
- Ein vollständiger Repository-Sonar-Sweep wird nicht als lokale Evidence
  verwendet. Die SonarQube-Cloud-PR-Analyse für den exakten Head ist der
  erforderliche Hosted-Entscheidungspunkt.

## Bekannte Einschränkungen

Diese Korrektur behandelt nur eine aktuelle SonarQube-Cloud-Beobachtung. Der
fokussierte Test beweist sein vorhandenes Parent-Cache-Contract-Verhalten,
nicht aber einen vollständigen NGINX-Build oder Runtime-Lifecycle. Die aktuelle
CI-Lane ist `3.13.14` aus `.python-version`; der verfügbare lokale Parent-Venv
ist `3.14.4`, daher bleibt die Ausführung in der exakten Lane ein erforderlicher
Hosted-Check.

## Verbleibende Risiken

Der größere Parent-only-SonarQube-Cloud-Backlog bleibt separat getrackt.
Hosted-Exact-Head-SonarQube-Cloud- und GitHub-Actions-Evidence sind für einen
Draft-PR weiterhin erforderlich; er muss ungemergt bleiben.

## Finaler Diff- und Review-Status

Lokale Source-, fokussierte Test-, Traceability- und Final-Diff-Checks bestanden.
Der beabsichtigte Source-Diff entfernt eine tote Test-Lokalzuweisung und fügt
bilinguale Traceability hinzu. Bevor ein Draft-PR als verifiziert gilt, müssen
exakte lokale/Remote/PR-SHA-Gleichheit, anwendbare GitHub-Checks (einschließlich
der konfigurierten Python-`3.13.14`-Lane), SonarQube-Cloud-Quality-Gate,
Selected-Key-Query und PR-Status für den tatsächlichen Head erneut geprüft
werden.
