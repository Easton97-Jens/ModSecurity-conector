# Change Record: gesperrte CI-Testabhängigkeiten in Version-Updatern

**Sprache:** [English](CR-20260814-locked-ci-test-dependencies.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260814-locked-ci-test-dependencies |
| Datum (UTC) | 2026-08-14 |
| Basis-Revision | `5e77de897841b62fd9e982f70cad3036fce570ef` |
| Delivery-Status | Die Auslieferung genau dieser Änderung über einen Draft-PR ist autorisiert. Weder Merge noch `master`-Integration sind autorisiert. Bei Erstellung dieses Records lag kein Hosted-Check-Ergebnis für einen exakten Head vor. |

## Motivation und Problemstellung

Der vom Benutzer bereitgestellte GitHub-Actions-Lauf `31818093186` scheiterte in `validate-go-patch`: Er rief `tests.test_ci_security_workflows` auf, dessen Importpfad PyYAML benötigt, bevor der bestehende hash-gesperrte CI-Abhängigkeitssatz installiert war. Die Quellinspektion bestätigte dieselbe fehlende Vorbedingung in `validate-python-patch`.

`requirements-ci.lock` pinnt bereits `PyYAML==6.0.3` mit Hashes. Diese Änderung verwendet diese bestehende gesperrte Eingabe; sie fügt keine Python-Abhängigkeit hinzu, aktualisiert sie nicht und lockert sie nicht.

## Akzeptanzkriterien

- Beide Version-Updater-Validator-Jobs installieren `requirements-ci.lock` nach ihrer Python-Interpreter-Prüfung und vor ihrem ersten importsensitiven Test.
- Jede Installation verwendet `--require-hashes`, `--only-binary=:all:`, `--no-input` und die bestehende Lock-Datei und führt anschließend `python3 -m pip check` aus.
- Regressionstests verifizieren Lock-Datei, Flags, pip check und Reihenfolge für beide Workflow-Jobs mit bestehenden Job-Blöcken und normalisierten Shell-Skripten.
- Keine Änderung an Workflow-Berechtigungen, Action-Pins, Lock-Dateien, Paketversionen, Checkout, Timeouts, Triggern oder Testunterdrückungen.

## Implementierungsentscheidung und Begründung

Jeder Validator hat jetzt direkt nach seiner bestehenden Python-Interpreter-Contract-Prüfung einen kleinen Schritt `Install hash-locked CI test dependency`. Der Schritt führt `python3 -m pip install --disable-pip-version-check --no-input --only-binary=:all: --require-hashes -r requirements-ci.lock` und anschließend `python3 -m pip check` aus. Damit steht der Abhängigkeits-Contract bereit, bevor das Testmodul PyYAML importieren kann, und eine ungültige oder unvollständige Umgebung scheitert fehlgeschlossen.

`tests/test_ci_security_workflows.py` ergänzt eine gemeinsame Assertion, die die bestehenden Helfer `job_blocks` und `normalize_shell_script` verwendet. Die Go- und Python-Updater-Tests verlangen jeweils den benannten Installationsschritt, den gesperrten Befehl, pip check und die geforderte relative Reihenfolge vor ihrem ersten Workflow-Test.

## Security-Auswirkung

Dies ist eine CI-Abhängigkeits- und Codeausführungsgrenze. Die Sicherheitsinvariante lautet, dass ein importsensitiver Workflow-Test nur den bereits vorhandenen hash-verifizierten, binär-only Abhängigkeitssatz erhält und seine Integritätsprüfung vor der Testausführung besteht. Der Fix erhält Lock-Datei und alle bestehenden Workflow-Kontrollen; er führt weder eine ungepinnte PyYAML-Installation ein noch schwächt er Hashes, Pins, Berechtigungen oder Validierung.

## Geänderte Dateien

- `.github/workflows/update-go-version.yml`
- `.github/workflows/update-python-version.yml`
- `tests/test_ci_security_workflows.py`
- dieses englische/deutsche Change-Record-Paar und seine englischen/deutschen Archivindex-Einträge.

Lokale, ignorierte Control-Plane-Evidenz bleibt als `FND-PARENT-0131` unter `.codex/findings/` und ihrem passenden `.codex/runs/`-Receipt erhalten. Sie wird nicht stillschweigend zusammen mit nicht zusammenhängenden lokalen Datensätzen per Force hinzugefügt.

## Ausgeführte Befehle

Der vom Repository ausgewählte Interpreter `.venv/bin/python3` wurde verwendet, weil die Python-Policy eine Repository-Virtualenv statt einer Mutation des Systeminterpreters verlangt. Die ausgeführten Prüfungen umfassen:

- `.venv/bin/python3 -m pip install --disable-pip-version-check --no-input --only-binary=:all: --require-hashes -r requirements-ci.lock`
- `.venv/bin/python3 -m pip check`
- `.venv/bin/python -m unittest -v tests.test_ci_security_workflows`
- `.venv/bin/python3 -m compileall -q ci scripts tests`
- `PYTHON=.venv/bin/python make check-go-version-contract`
- die Sechs-Modul-Unittest-Ausführung für Version-Updater- und Workflow-Contracts
- `make check-ci-security-contract`
- den checksum-verifizierten `actionlint`-Abrufmechanismus und beide geänderten Workflows.

## Tests und tatsächliche Ergebnisse

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| Hash-gesperrte Installation der CI-Abhängigkeiten | bestanden; bestehender `PyYAML==6.0.3`-Lock-Eintrag erfüllt |
| `python3 -m pip check` | bestanden; keine defekten Requirements gefunden |
| Fokussierte CI-Workflow-Contracts | bestanden; 28 Tests |
| `python3 -m compileall -q ci scripts tests` | bestanden, Exit 0 |
| `make check-go-version-contract` | bestanden, Exit 0 |
| Sechs-Modul-Suite für Version-Updater-/Workflow-Contracts | bestanden; 98 Tests |
| `make check-ci-security-contract` | bestanden; 90 Tests, 4 übersprungen |
| Checksum-verifiziertes `actionlint` (`v1.7.12`) für beide geänderten Workflows | bestanden, Exit 0 |
| `make check-bilingual-docs` | bestanden; `bilingual docs ok` |
| `make check-doc-links` | bestanden; Repository-Pfadreferenzen und Dokumentationslinks bestanden |
| `git diff --check` | bestanden, Exit 0 |

## Runtime-Evidence

Die verfügbare Evidenz ist lokale statische Workflow-Validierung und die Ausführung der Python-Contracts. Kein GitHub-Hosted-Runner, kein Candidate-Update-Pfad und keine Produktions-Runtime wurden ausgeführt oder behauptet.

## Nicht ausgeführte Prüfungen mit Begründung

Bei Erstellung dieses Change Records lag kein GitHub-Actions-Ergebnis für einen exakten Head vor. Der nachfolgende Draft-PR muss ausschließlich gegen seine exakte Head-SHA bewertet werden. Weder Merge noch Verifikation von resultierendem `master` sind autorisiert.

## Bekannte Einschränkungen

Die lokalen Prüfungen belegen die deklarierte Workflow-Struktur und Testreihenfolge. Sie können aber nicht das exakte Runner-Image, die Netzwerkverfügbarkeit oder den Cache-Zustand einer zukünftigen Hosted-Ausführung beweisen. Dieser Nachweis erfordert einen ausdrücklich autorisierten Lauf der ausgelieferten Revision.

## Verbleibende Risiken

Der zukünftige Hosted-Lauf bleibt die abschließende Bestätigung, dass der Runner das bereits gesperrte Binär-Wheel wie erwartet auflöst. Der kontrollierte Fehlermodus ist beabsichtigt: Ein fehlendes Wheel, Hash-Mismatch, defekter Abhängigkeitssatz oder fehlgeschlagener pip check stoppt den Validator vor seinem importsensitiven Test.

## Finaler Diff- und Review-Status

Die begrenzte Quellprüfung fand nur die zwei angeforderten Workflow-Änderungen, ihre zielgerichtete Regression und diesen erforderlichen gepaarten Traceability-Record. `git diff --check`, `make check-bilingual-docs` und `make check-doc-links` bestanden, nachdem der Record und die Archivindex-Einträge vorlagen. Es wird weder Hosted-Verifikation noch Delivery-Status behauptet.
