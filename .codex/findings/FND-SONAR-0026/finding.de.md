# Finding FND-SONAR-0026: PR-#198-Test-Bootstrap verwendet eine optimierungssensitive zusammengesetzte Assert-Anweisung

**Sprache:** Deutsch | [English](finding.md)

## Klassifikation

| Feld | Wert |
| --- | --- |
| Kategorie | `maintainability` |
| Repository / Ownership | `parent` / `parent` |
| Priorität / Schwere / Konfidenz | `P2` / `not_applicable` / `confirmed` |
| Status / Machbarkeit | `verified` / `feasible_now` |
| Release-Blocker / Kandidat-Integrationsblocker / sicherheitsrelevant | nein / nein / nein |
| Sonar-Inventar | `python:S9073`, `AZ-zgsKSuhGCH8wggCxz` |

## Zusammenfassung, Verhalten und Auswirkung

Die anfängliche SonarQube-Cloud-Analyse für PR-#198-Head
`6a9f1d21a927405833aa0f07ae6e09e5aa3fd07d` meldet einen offenen MAJOR-Code-
Smell, `python:S9073`, in `tests/test_prepare_runtime_components.py:22`.
Die zusammengesetzte Modul-Level-Assert-Anweisung schützt die dynamisch
erzeugte Modulspezifikation und ihren Loader vor `module_from_spec()` und
`exec_module()`.

Dies ist ein task-eigenes, nicht sicherheitsrelevantes Maintainability-
Finding. Python entfernt Assertions unter `-O`; daher eignet sich der Guard
nicht für Import-/Bootstrap-Fehlerbehandlung. Das Exact-Head-Quality-Gate ist
`OK`, aber das offene Issue muss vor dem Fortsetzen dieser kontrollierten
Integration remediiert und erneut verifiziert werden. Keine Risikoakzeptanz
des Users deckt dieses PR-lokale Issue ab.

## Scope, Remediation und Controls

- Der Scope ist auf den Parent-Test-Bootstrap
  `tests/test_prepare_runtime_components.py` und seinen zweisprachigen Change
  Record begrenzt.
- Die zusammengesetzte Assert-Anweisung wird durch einen einzelnen expliziten
  Guard ersetzt, der `ImportError` auslöst, wenn `SPEC` oder `SPEC.loader`
  nicht verfügbar ist. Die bestehende dynamische Modulerzeugung und die
  genau-einmalige Ausführungssequenz bleiben erhalten.
- Der gültige Bootstrap und die fokussierte Runtime-Component-Suite werden
  normal und unter `Python -O` sowie mit einer kontrollierten ungültigen
  Spec-Import-Rejection verifiziert.
- Es werden kein `NOSONAR`, kein Assertion-Split, keine Suppression, kein
  cast/type-ignore, keine Sonar-Policy- oder Quality-Gate-Änderung, keine
  Exclusion sowie keine Framework-/MRTS- oder Gitlink-Änderung verwendet.

## Aufbewahrte Evidence

Run-ID: `fnd-sonar-0026-20260730T145943Z`.

| Artefakt | SHA-256 | Ergebnis |
| --- | --- | --- |
| `evidence/sonar-pr198-initial.json` | `6cd1dafc4d62b5d17a2e94196afc36007b43f2a4a4b8c776447b6282df059e3a` | Exakter Sonar-Check und Analyse `dfe0aaad-3fc8-428c-aa03-a1eb3cc684f1` sind erfolgreich und das Quality Gate ist `OK`, aber Issue `AZ-zgsKSuhGCH8wggCxz` bleibt `OPEN`. |

Das Artefakt wird unter
`/var/tmp/codex/ModSecurity-conector/pr-integration-186-199-20260730T072658Z/fnd-sonar-0026-20260730T145943Z/`
aufbewahrt. Es bindet das Issue an den aufgezeichneten Head und Base von PR
#198; Credentials oder rohe Environments werden nicht aufbewahrt.

## Exact-Head-Remediation-Verifikation

Der enge testseitige ImportError-Guard liegt auf exaktem PR-Head
b55eedd470df4e3395a6833f7814363c8beb1974 vor. Seine aufbewahrte finale
Evidence dokumentiert Sonar-Quality-Gate OK, null offene/confirmed
task-eigene PR-Issues, null neue Hotspots und das ursprüngliche Issue
AZ-zgsKSuhGCH8wggCxz / python:S9073 als CLOSED/FIXED durch Analyse
5ef72438-492c-43d3-8ca5-4572826a993f. Erforderliche GitHub-Checks,
No-Bypass-Ruleset-Kontexte, Code- und Secret-Scanning, Mergeability, Reviews
und Threads wurden unabhängig für denselben Head zurückgelesen. Keine Regel,
kein Quality Gate, keine Exclusion, Suppression, kein NOSONAR, Gitlink,
Framework oder MRTS wurde geändert.

| Artefakt | SHA-256 | Ergebnis |
| --- | --- | --- |
| fnd-sonar-0026-20260730T164415Z/evidence/sonar-pr198-remediated.json | 9b59e06506d7d513f9939a77bfaaa6ad316971ee9a8164a6363e82d95abc7c07 | Exact-PR-Head-Remediation-Verifikation; ursprüngliches Issue CLOSED/FIXED und kein task-eigenes Ersatz-Issue. |

## Resulting-Master-Verifikation

Der geschützte SHA-gebundene Squash-Merge von PR #198 erzeugte Parent-master
`4e5d45072bf32ff822f4b1039517026416259493` um `2026-07-30T16:58:50Z`.
Das Ergebnis besitzt den identischen Tree des geprüften Heads, genau die sechs
genehmigten Pfade, sauberen Whitespace und den unveränderten Parent-Framework-
Gitlink `6400ee882afa0527e5c0763fa6efb850ffa403f2`. Erforderliche geschützte
Kontexte, CodeQL und die verfügbare Secret-Scanning-Service-/Alert-Evidence
bestanden.

Die Sonar-Analyse `32425f2d-a1e8-47bb-b22a-276b1f93cd6b` ist an diesen
Master-SHA gebunden. Sie meldet null offene `python:S9073`-Issues am
betroffenen Testpfad; der ursprüngliche Key fehlt im zugänglichen aktuellen
Index und sein Detailendpunkt ist nicht mehr abrufbar. Der einzige rote
Sonar-Master-Check ist exakt die separat dokumentierte FND-SONAR-0001-
Signatur: nur ihre drei bekannten `python:S5332`-Hotspots und zwei bekannten
fehlgeschlagenen Bedingungen. Das ist keine grüne Sonar-Behauptung und
übergeht keinen anderen PR-, Scanner-, Review- oder Master-Control. Die
queued Zero-Run-Cloudflare-Suite ist nicht anwendbar: Sie ist keine Ruleset-
Anforderung, kein Deployment-Pfad/keine Konfiguration wurde geändert oder
existiert, und das exakte-SHA-Deployment-Inventar ist leer.

## Akzeptanz und Disposition

Akzeptanz verlangt ein explizites Invalid-Spec-`ImportError` in normalem und
optimiertem Python, die Bewahrung des gültigen Modul-Ladens und aller
fokussierten Runtime-Component-Controls, einen finalen Exact-Head-Security-
Diff-Review, terminale erforderliche Hosted-Checks ohne ungelösten Review-
Thread sowie einen Sonar-Readback, der das ursprüngliche Key und jedes
task-eigene Ersatz-Issue als abwesend zeigt. Das Finding ist auf dem
Resulting-Master `verified`; aus einer bloßen Index-Abwesenheit wird es bewusst
nicht `closed`.

`FND-SONAR-0016` ist ein verwandtes aggregiertes New-Code-Follow-up und
`FND-SONAR-0024` ist ein anderes C-Komplexitäts-Issue; keines ist ein Duplikat.
`FND-SONAR-0001` ist separater Master-Level-Risikokontext. Die aktuelle
Risikoakzeptanz des Users ist absichtlich auf diese unveränderte Master-
Signatur begrenzt, nicht auf dieses PR-lokale Issue.

## Historie

- `2026-07-30T14:59:43Z`: exakte PR-#198-Evidence bestätigte offenes
  `AZ-zgsKSuhGCH8wggCxz` / `python:S9073`; das eigenständige Parent-P2-
  Finding wurde als `in_progress` triagiert und eine enge Remediation geplant.
  Kein Merge, keine Suppression und keine Sonar-Konfigurationsänderung
  erfolgten.
- `2026-07-30T16:41:38Z`: der exakte Remediation-PR-Head
  `b55eedd470df4e3395a6833f7814363c8beb1974` bestand lokale Controls,
  versiegelten Security-Diff-Review, terminale Hosted-/Governance-Checks und
  PR-gebundene Sonar-Analyse `5ef72438-492c-43d3-8ca5-4572826a993f`.
  Ursprüngliches Issue `AZ-zgsKSuhGCH8wggCxz` ist `CLOSED/FIXED`; der
  Status wechselte zu `fixed`, Resulting-Master-Verifikation steht noch aus.
- `2026-07-30T17:06:29Z`: geschützter Squash von #198 erzeugte Master
  `4e5d45072bf32ff822f4b1039517026416259493` mit dem Tree des geprüften
  Heads. Die SHA-gebundene Analyse `32425f2d-a1e8-47bb-b22a-276b1f93cd6b`
  hat null offene `python:S9073`-Issues am betroffenen Pfad; der ursprüngliche
  Key fehlt im zugänglichen Master-Index. Status wechselte zu `verified`,
  nicht zu `closed`.
