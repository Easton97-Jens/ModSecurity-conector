# Change Record: NGINX-Alignment des terminalen Response-Header-Checkers

**Sprache:** [English](CR-20260912-nginx-terminal-checker-alignment.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260912-nginx-terminal-checker-alignment |
| Datum (UTC) | 2026-09-12 |
| Basis-Revision | `a24d22da8e11cd99ba05f24f9f53f92a792591c4` |
| Delivery-Status | Nur lokaler Successor-Patch. Kein Successor-Commit, Remote-Branch, Pull Request oder Successor-Merge ist erfolgt. PR #360 wurde bereits in der Basis-Revision per Squash gemergt; ein eigener Successor-PR braucht separate exakte Merge-Autorisierung. |

## Motivation und Problemstellung

Nach dem Merge von PR #360 scheiterten fünf Resulting-Master-Workflows durch
denselben NGINX-Common-Adoption-Checker. Der Checker erwartete weiterhin die
frühere Header-Filter-Form mit zwei Guards und einen Collection-Fehlerzweig ohne
das neue Sticky-Fehlerflag. Der Produktquellcode ist absichtlich strenger: Ein
terminaler Response-Header-Processing-Fehler gibt bei Filter-Reentry `NGX_ERROR`
zurück, statt an den nächsten Header-Filter weiterzuleiten.

## Akzeptanzkriterien

- Der aktuelle Fail-Closed-Header-Filter-Quellcode wird von
  `check-nginx-common-adoption.py` akzeptiert.
- Der Checker verlangt einen direkten `response_headers_processing_failed`-
  Guard mit `NGX_ERROR` vor dem permissiven Intervention-Guard.
- Der Collection-Fehlerzweig setzt dieses Sticky-Flag vor seinem terminalen
  `NGX_ERROR`-Return.
- Isolierte Mutationen, die den Retry-Guard permissiv machen oder die
  Collection-Fehlerzuweisung entfernen, werden verworfen.
- Bestehende NGINX-Source-Contract-, Fixture-Contract- und CI-Security-Checks
  bleiben grün; weder Runtime-Source noch CI-Control werden abgeschwächt.

## Implementierungsentscheidung und Begründung

Geändert werden nur der NGINX-Common-Adoption-Checker und seine isolierte
Mutation-Coverage. Der Checker erkennt drei geordnete Top-Level-Guards:
fehlender Kontext, Sticky-terminaler Fehler, danach Intervention. Er verlangt
außerdem die Sticky-Zuweisung im direkten Response-Header-Collection-
Fehlerzweig.

Keine NGINX-C-Runtime-Source, Framework-/MRTS-Source, Gitlink, Workflow,
Ruleset, Branch-Protection, SonarQube-Einstellung, Exclusion, Suppression oder
Dependency wird geändert. Der direkte Wrapper, der exakte `ret != 1`-
Native-Error-Contract und die Anti-Bypass-Strukturchecks bleiben erhalten.

## Security-Auswirkung

Diese Static-Checker-Korrektur verstärkt den Nachweis des vorhandenen
Fail-Closed-Verhaltens. Ein persistenter Response-Header-Processing-Fehler darf
nicht in den Intervention-Pfad umgewandelt werden, der an den nächsten
Header-Filter weiterleitet. Die neuen Mutationstests belegen, dass der Checker
eine permissive Ersetzung dieses Guards sowie das Entfernen der Collection-
Fehler-Sticky-Zuweisung verwirft.

Ein benachbarter Negative-Intervention-Reentry-Pfad wurde untersucht, aber mit
der verfügbaren Source-only-Evidenz nicht als erreichbar belegt. Er ist eine
offene Validierungsfrage, keine nachgewiesene Schwachstelle und kein Grund,
Runtime-Source spekulativ zu ändern.

## Geänderte Dateien

- `ci/checks/connectors/nginx/check-nginx-common-adoption.py`
- `tests/test_nginx_common_adoption.py`
- `reports/audits/change-records/CR-20260912-nginx-terminal-checker-alignment.md`
- `reports/audits/change-records/CR-20260912-nginx-terminal-checker-alignment.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

| Befehl oder Check | Ergebnis | Beobachtetes Ergebnis |
| --- | --- | --- |
| `python -m py_compile ci/checks/connectors/nginx/check-nginx-common-adoption.py tests/test_nginx_common_adoption.py` | bestanden | Python-Syntaxvalidierung bestanden. |
| `make check-nginx-common-adoption` | bestanden | Alle ausgegebenen NGINX-Common-Adoption-Assertions bestanden. |
| fokussierte Checker- und Upstream-Security-Tests | bestanden | 20 Tests bestanden. |
| vollständige Checker-, Upstream-Security- und Fixture-Contract-Suite | bestanden | 115 Tests bestanden. |
| `python -m unittest -v tests.test_ci_security_workflows` | bestanden | 30 CI-Security-Contract-Tests bestanden. |
| `git diff --check` | bestanden | Keine Whitespace-Fehler im lokalen Successor-Diff. |

## Runtime-Evidence

Für diese reine Checker-/Test-Änderung wurde keine native NGINX-Runtime gebaut
oder ausgeführt. Der vorhandene Fixture-Contract deckt strukturell Zero-,
Negative- und Reinvocation-Szenarien ab; er ist keine Host-Runtime-Evidenz.

## Nicht ausgeführte Prüfungen mit Begründung

`make lint` wurde nicht ausgeführt, weil es das Framework-Submodul in diesem
isolierten Parent-Worktree benötigt. `make check-bilingual-docs` und
`make check-doc-links` wurden ausgeführt und scheiterten ausschließlich an
vorbestehenden Links in dieses nicht initialisierte Submodul. Die Parent-
Boundary-Policy verbietet eine automatische Initialisierung ohne separate
explizite Benutzerentscheidung. Exact-Successor-Head-Hosted-Checks,
SonarQube-Cloud-Analyse, Review-Disposition und Resulting-Master-Workflows
können erst existieren, wenn ein Successor-PR autorisiert und erstellt ist.

## Bekannte Einschränkungen

Die Basis-Revision bleibt in fünf Workflow-Call-Chains rot, bis der Successor
ausgeliefert ist und seine Exact-Head-Checks laufen. Lokale Evidenz beweist nur
die Checker-/Test-Grenze, nicht NGINX-Host-Runtime-Verhalten. Die benachbarte
Negative-Intervention-Reentry-Frage bleibt unbelegt.

## Verbleibende Risiken

Die Korrektur verlangt absichtlich die aktuell geprüfte C-Form. Ein künftiges
legitimes Refactoring der Header-Filter-Guards oder des Collection-Fehlerzweigs
muss den Checker und seine Negativkontrollen in derselben Änderung aktualisieren.
Kein Security-Finding wird allein aufgrund dieser lokalen Evidenz geschlossen.

## Finaler Diff- und Review-Status

Der lokale Zwei-Dateien-Implementierungsdiff wurde unabhängig auf Security und
Test-Coverage geprüft. Der Review fand keine Abschwächung und keinen direkten
Checker-Bypass. Der Checker verlangt den terminalen Guard und die Sticky-
Zuweisung; fokussierte Mutation- und Contract-Evidenz bestand. Delivery,
Hosted-Validierung, SonarQube Cloud und ein Successor-Merge warten auf separate
Autorisierung.
