# Change Record: Parent-CI-Deduplizierung der Verified-Runtime-Mismatch-Control-Evidence

**Sprache:** [English](CR-20260729-sonar-ci-verified-runtime-mismatch-duplication.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260729-sonar-ci-verified-runtime-mismatch-duplication` |
| Datum (UTC) | `2026-07-29` |
| Basis-Revision | `9f23ae2c5fe908cef38f203be03f93fda75a8dd7` |
| Bewertete Source-Revision | Lokaler Task-Patch gegen die genannte Basis-Revision |
| Grenze | Ausschließlich Parent `ci/evidence/reports/generate-verified-runtime-mismatch-analysis.py`, sein direkter Parent-Regressionstest, dieses englische/deutsche Change-Record-Paar und die gepaarten Indizes. Keine `.github/`, keine `scripts/`, kein Framework, kein MRTS, kein Gitlink, keine SonarQube-Cloud-Konfiguration, kein Quality Gate, keine Exclusion, keine Suppression, keine Default-Branch- oder Merge-Aktion sind enthalten. |
| SonarQube-Cloud-Verknüpfung | Entfernt ein aktuelles Same-File-20-Zeilen-Duplikatpaar im Parent-CI-Generator. Keine Scanner-Kontrolle wird geändert. |

## Motivation und Problemstellung

Der aktuelle Parent-CI-Generator enthielt zwei äquivalente Full-Matrix-
Control-Evidence-Schleifen. Ihr einziger beabsichtigter Unterschied war der
feste gegenüber dem übergebenen Control-Case-Namen. Das Paar ist ein aktuelles
SonarQube-Cloud-Duplikatziel, liegt jedoch an einer Merge-Readiness-Evidence-
Grenze: Ein Refaktor muss den festen Case, die deterministische Sechs-Entry-
Matrix und die All-Pass-Classification-Gates bewahren.

Der fokussierte Security-Review reproduzierte außerdem `FND-PARENT-0066`: Ein
ungültiger Producer-Record konnte im Fallback `status: pass` behalten, nachdem
er das erforderliche `pass`/`403`/`403`/live-Prädikat nicht erfüllt hatte.
Downstream-Classifier gaten auf den ausgegebenen Status, so dass dies eine
reine Evidence-Reklassifizierung fälschlich erlauben konnte. Die begrenzte
Korrektur gehört in denselben Helper, weil sie den Deduplizierungs-Contract
bewahrt und gleichzeitig den ungültigen Fallback fail closed macht.

## Akzeptanzkriterien

- `full_matrix_control_evidence()` behält seine API und sein festes
  `ARGS_NAMES_CONTROL_CASE`-Verhalten und delegiert dabei an den
  parametrisierten Helper.
- Ein Control wird nur dann als `pass` ausgegeben, wenn `status=pass`, expected
  `403`, actual-oder-observed `403` und `live_executed=true` gemeinsam gelten.
- `pass`/`403`/`403`/non-live- und `pass`/`403`/`200`/live-Records sind nicht
  erfolgreich und können keinen der beiden Downstream-All-Pass-Classifier
  erfüllen.
- Gültige Apache- und NGINX-Live-403-Controls, Missing-Evidence, Map-Ordering,
  Evidence-Felder, Safe-Root-Verhalten und Report-Output-Verhalten bleiben
  kompatibel.
- Der ausgewählte Source-/Test-Diff hat fokussierte Regression-, Syntax-,
  Whitespace- und Security-Review-Evidence. Ein späterer exakter Draft-PR-Head
  muss null neue SonarQube-Cloud-Issues und `0.0%` New-Code-Duplizierung ohne
  Abschwächung von Scanner-Kontrollen zeigen.

## Implementierungsentscheidung und Begründung

Der Fixed-Case-Helper ist jetzt ein Kompatibilitäts-Wrapper um
`full_matrix_case_control_evidence(build_root, ARGS_NAMES_CONTROL_CASE)`.
Der parametrisierte Helper bleibt die einzige Loop- und Output-Implementierung.

Das Erfolgsprädikat selbst bleibt explizit. Nur der Fallback ändert sich: Wenn
der Producer `pass` sagt, das vollständige Prädikat jedoch fehlgeschlagen ist,
wird sein ausgegebener Control-Status zu `fail`. Bestehende Producer-Zustände
außer `pass` und ihre Evidence-Felder bleiben unverändert. Dies ist bewusst
enger als Änderungen an den Downstream-Classifiers oder an der
Report-/Readiness-Output-Logik.

Die direkten Regressionstests decken Wrapper-Äquivalenz, gültiges Live-403,
Missing-Evidence, Non-Live-Evidence, einen Actual-200-False-Allow, den NGINX-
`observed_status`-Kompatibilitätspfad und beide Classifier-Consumer ab.

## Security-Auswirkung

Die geänderte Grenze konsumiert von CI-Producern erstelltes Full-Matrix-
Summary-JSON und speist danach eine Collection-Semantics-Classification, die
generierte Mismatch-Kritikalität und Merge-Readiness-Reporting beeinflussen
kann. Die Reparatur ist fail closed: unvollständige, veraltete, non-live oder
False-Allow-Evidence kann nicht allein deshalb zu einem erfolgreichen Control
werden, weil ihr Producer-Status `pass` lautet.

Der finale lokale Codex-Security-Diff-Scan deckt Generator und direkten Test
ab, hat vollständige Worklist-Receipts und enthält null reportierbare diff-
induzierte Findings. Sein aufbewahrter Report ist
`/var/tmp/codex/ModSecurity-conector/security-scans/ModSecurity-conector/9f23ae2c5fe908cef38f203be03f93fda75a8dd7_20260729T090933Z/report.md`.
Dies ist eine CI-Evidence-Integrity-Korrektur, kein Claim eines Request-Path-
Enforcement-Bypasses oder eines externen Hosted-CI-Angreiferpfads.

## Geänderte Dateien

- `ci/evidence/reports/generate-verified-runtime-mismatch-analysis.py`
- `tests/test_report_conditional_remediation.py`
- `reports/audits/change-records/CR-20260729-sonar-ci-verified-runtime-mismatch-duplication.md`
- `reports/audits/change-records/CR-20260729-sonar-ci-verified-runtime-mismatch-duplication.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

### Tests und tatsächliche Ergebnisse

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| Aufbewahrte gezielte Pre-Fix-Regression | schlug erwartungsgemäß fehl: Ein `pass`/`403`/`403`/non-live-Control wurde als `pass` ausgegeben; aufbewahrtes SHA-256 `ef0876d194abe7258f5302263b0efa0a35f40a869cf84d2d00ad5d463427efe9`. |
| `PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<task-pycache> TMPDIR=<task-tmp> /root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_report_conditional_remediation` | bestanden: 11 Tests. |
| Ausgewähltes `py_compile` für geänderten Generator und Test | bestanden. |
| `git diff --check origin/master` | nach den versionierten Source-, Test- und Change-Record-Änderungen bestanden. |
| Finaler lokaler Codex-Security-Diff-Scan | bestanden mit vollständiger Coverage und null reportierbaren Findings. |
| `make check-bilingual-docs` | `blocked_external_dependency`: Die erforderlichen Überschriften des neuen Records bestehen seine Validierung; dem isolierten Worktree fehlen die in bestehenden Repository-Dokumenten referenzierten Framework-Submodul-Targets. |
| `make check-doc-links` | `blocked_external_dependency`: Jedes gemeldete Target liegt unter dem fehlenden Framework-Submodul; kein Target dieses Change-Record-Paars wird gemeldet. |
| `make lint` | `blocked_external_dependency`: Shell-Syntax und Parent-Python-Kompilierung liefen, danach konnte ein bestehender No-CRS-Check das fehlende Framework `ci/checks/catalog/no_crs_baseline.py` nicht importieren. |

## Runtime-Evidence

Es wird keine Connector-Runtime-Matrix, keine netzwerkgestützte Vorbereitung
und kein Report-Generator-Lauf beansprucht. Die direkten Tests üben die reinen
Evidence-Classification-Contracts aus, ohne generierte Runtime-Reports zu
schreiben. Die normale Matrix benötigt generierte Evidence und nicht
verfügbaren Framework-Inhalt und bleibt deshalb außerhalb dieser engen CI-
Source-Reparatur.

## Nicht ausgeführte Prüfungen mit Begründung

- Vollständige Connector-Runtime-Matrix und Report-Generator-Ausführung liefen
  nicht: Sie benötigen generierte Evidence und den nicht verfügbaren
  Framework-Inhalt.
- Hosted-GitHub-Actions, SonarQube-Cloud-PR-Analyse, Review, Freigabe, Merge
  und Master-Verifikation existieren noch nicht und werden nicht lokal
  hergeleitet.

## Bekannte Einschränkungen

Die Source-Reparatur ist lokal verifiziert, doch ein späterer exakter Draft-
PR-Head wird weiterhin für Hosted-Checks und die verlangten SonarQube-Cloud-
Metriken null neue Issues und null neue Duplizierung benötigt. Der Task-
Worktree enthält absichtlich nicht den Framework-Inhalt, den die normale
Runtime-Matrix braucht.

## Verbleibende Risiken

Der Source-Level-Fallback ist jetzt fail closed, aber das finale Ergebnis ist
auf dem Hosted-PR-Head und auf aktuellem `master` noch nicht verifiziert. Jedes
CI-Producer- oder Reporting-Verhalten außerhalb der festen Source-/Test-Grenze
dieses Helpers bleibt unverändert und wird durch diesen Record nicht als sicher
beansprucht.

## Finaler Diff- und Review-Status

Lokale Source-, Regression-, Syntax-, Whitespace- und vollständige Security-
Diff-Review-Evidence liegen vor. Die Repository-Dokumentations- und Lint-
Targets wurden versucht und sind nur durch das absichtlich fehlende Framework-
Submodul blockiert, wie oben aufgezeichnet. Der initiale Source-Record war vor
Delivery; das folgende Update zeichnet die danach beobachtete Draft-PR-
Erstellung auf. Es werden kein Hosted-Check, kein SonarQube-Cloud-PR-Ergebnis,
keine Freigabe, kein Merge und keine `master`-Änderung beansprucht.

Delivery-Update: [Draft PR #178](https://github.com/Easton97-Jens/ModSecurity-conector/pull/178)
wurde am `2026-07-29T09:39:18Z` gegen `master` vom initialen exakten Head
`7831e83b6385bd843b9320c59a34167fa1dd410a` geöffnet, der bei Erstellung dem
lokalen und Remote-Task-Branch-Commit entspricht. Dieses Follow-up zeichnet
den beobachteten PR-Fakt auf, beansprucht aber keinen Hosted-Check, kein
Review, kein SonarQube-Cloud-Ergebnis, keine Freigabe, keinen Merge und keine
`master`-Änderung. Die nächste Exact-PR-Head-Beobachtung ist erforderlich,
nachdem dieses Change-Record-Follow-up gepusht wurde.
