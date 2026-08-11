# Change Record: readonly Submodule-Validator durchsetzen

**Sprache:** [English](CR-20260811-enforce-readonly-submodule-validator.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260811-enforce-readonly-submodule-validator |
| Datum (UTC) | 2026-08-11 |
| Basis-Revision | 4749c02c6dd5e285c4309b4e69b0bb28ae459e48 |
| Delivery-Status | Implementierungsrecord; finale Exact-Head-Hosted-Validierungs-, Security-Scan- und Delivery-Evidence liegt in der zugehörigen PR- und Scan-Evidence vor |

## Motivation und Problemstellung

Der Framework-Submodule-Updater validiert einen aufgelösten Candidate, bevor
ein separater Publisher eine Parent-Gitlink-Aktualisierung vorschlagen darf.
Die Dokumentation für Leser muss die beabsichtigte Dateisystem- und
Privilegiengrenze korrekt beschreiben, ohne die Implementierungsbeschreibung in
unbeobachtete Hosted- oder Security-Evidence zu verwandeln. Zusätzlich ist ein
enger Validate-only-Aufruf für diese eine Aufgabe erforderlich, damit der
genaue Head des task-eigenen/reviewten Parent-Branch
`fix/ci-enforce-readonly-submodule-validation` Hosted-Validator-Evidence
erhalten kann, ohne den Publisher ausführbar zu machen.

## Akzeptanzkriterien

- Der Validator wendet `umask 077` vor dem Erstellen eines frischen privaten
  `mktemp`-Roots unter `RUNNER_TEMP` und erneut in der isolierten Candidate-
  Shell vor Candidate-Ausgaben an; alle unterstützten, legitimen Workflow-
  Ausgabe-Roots werden unter dem privaten externen Child des Candidate erzwungen.
- Parent- und Framework-Source-Trees sowie ihre `.git`-Metadaten sind für den
  Candidate schreibgeschützt.
- Der Candidate läuft als dedizierte Non-login- und Non-sudo-Identität
  `modsecurity-validator` über genau einen `sudo -n -u`- / `env -i`-Einstieg.
- `make quick-check` bleibt unverändert.
- Der Validator erhält keine Produktions-Schreibrechte; diese bleiben allein
  dem separaten Publisher vorbehalten.
- Manueller `workflow_dispatch` mit `validate_only: true` ist auf das
  kanonische Parent-Repository `Easton97-Jens/ModSecurity-conector` und den
  task-eigenen/reviewten Branch
  `fix/ci-enforce-readonly-submodule-validation` beschränkt; er ist keine
  Einrichtung zum Ausführen beliebiger nicht vertrauenswürdiger Parent-Refs.
  Er verwendet den dispatchten `github.sha`, erzwingt die Validierung auch bei
  gleichem Candidate und Gitlink und schließt den Publisher von der Ausführung
  aus.
- Der task-eigene/reviewte Parent-Workflow- und Helper-SHA ist vor dem
  Root-seitigen Setup vertrauenswürdig; der Framework-Candidate bleibt nicht
  vertrauenswürdiger, durch die Sandbox regierter Code. Die Branch-Allowlist
  ist eine Guardrail, kein Schutz gegen einen feindlichen Writer im selben
  Repository; dieses Threat Model erfordert Branch Protection oder Environment
  Approval.
- Der Validate-only-Aufruf unterscheidet sich vom autorisierten Updater-
  Dispatch nach dem Merge auf `master` mit falschem `validate_only`.
- Vertrauenswürdige Setup-Probes prüfen Parent-/Framework-Schreibablehnung,
  sudo-Ablehnung und erfolgreiche externe Schreibzugriffe vor dem Quick Check.
- Ein vollständiges Post-Lock-Source-Inventar von Parent/Framework muss nach
  dem Quick Check exakt gleich sein, und der externe Validator-Tree muss seinen
  fail-closed Vertrag für Ownership, Typ, Berechtigungen, symbolische Links und
  Hard Links erfüllen.
- Englische und deutsche Dokumente sowie Change Records enthalten dieselben
  wesentlichen Fakten und Evidence-Grenzen.

## Implementierungsentscheidung und Begründung

Der dokumentierte Vertrag wendet `umask 077` vor seinem frischen privaten
`mktemp`-Root unter `RUNNER_TEMP` und erneut in der isolierten Candidate-Shell
vor Candidate-Ausgaben an. Ein Root-seitiger Helper sperrt Parent- und
Framework-Trees sowie ihre `.git`-Metadaten vor der Candidate-Ausführung
root-owned und nicht beschreibbar, wodurch Source-/Git-Zustand für den
Candidate unveränderlich ist. Alle unterstützten, legitimen Workflow-Ausgabe-
Roots werden unter seinem privaten externen Child erzwungen. Der Candidate tritt
genau einmal über `sudo -n -u` mit `env -i`, ohne User Site und mit externen
Roots für `HOME`, Git-Konfiguration, pip-Cache, Bytecode-Cache, Build, Logs und
Caches unter diesem Child ein. Vertrauenswürdige Probes gehen dem unveränderten
`make quick-check` voraus. Der Validator ist schreibgeschützt; nur der
separate Publisher behält nach der Validierung die eng begrenzte
Produktions-Schreibgrenze.

Für Evidence zum genauen Branch-Head darf manueller `workflow_dispatch`
`validate_only: true` nur im kanonischen Parent-Repository auf dem
task-eigenen/reviewten Branch
`fix/ci-enforce-readonly-submodule-validation` setzen. Er ist keine allgemeine
Einrichtung zum Ausführen beliebiger nicht vertrauenswürdiger Parent-Refs.
Dieser Pfad checkt den dispatchten `github.sha` in Resolver und Validator aus,
erzwingt den Validierungsjob auch dann, wenn der Framework-Candidate diesem
dispatchten Parent-Gitlink entspricht, und schließt den Publisher explizit
aus. Er kann weder einen Gitlink-Branch noch einen Pull Request erstellen oder
aktualisieren. Er ist keine Sandbox für nicht vertrauenswürdige Parent-Pull-
Requests/-Refs: Der task-eigene/reviewte Parent-Workflow- und Helper-SHA ist
vor dem Root-seitigen Setup vertrauenswürdig, während der Framework-Candidate
nicht vertrauenswürdiger, durch die Sandbox regierter Code bleibt. Ein Hosted-
Erfolg wäre funktionale Evidence nur für diesen reviewten SHA. Die Branch-
Allowlist ist eine Guardrail, kein Schutz gegen einen feindlichen Writer im
selben Repository; dieses Threat Model erfordert Branch Protection oder
Environment Approval. Der separat autorisierte Updater-Dispatch nach dem Merge
läuft auf `master` mit falschem `validate_only`; er validiert den Übergang vom
vertrauenswürdigen Default Branch und darf nach der Validierung den begrenzten
Publisher erreichen. Die beiden Aufrufe sind nicht austauschbar, und der
Validate-only-Modus erteilt keine Delivery-Berechtigung.

Der Root-seitige Helper inventarisiert beide gesperrten Source-Trees vor der
Candidate-Ausführung und prüft nach dem Check ihre exakte Gleichheit. Das
Inventar zeichnet Pfad, Typ, Größe, Modus, UID, GID und Link-Anzahl sowie
SHA-256 für reguläre Dateien und Link-Text für symbolische Links auf. Separat
scannt er den externen Tree fail-closed: Zugelassen sind nur dem Validator
gehörende Directories und reguläre Dateien ohne Group-/Other-Schreibrechte;
Special Objects, symbolische Links und Hard Links in den Source-Tree werden
abgewiesen.

Dieser Implementierungsrecord dokumentiert den beabsichtigten Vertrag. Er
behauptet keine finalen Exact-Head-Hosted-Validierungs-, Security-Scan- oder
Delivery-Ergebnisse; diese liegen in der zugehörigen PR- und Scan-Evidence vor.

## Security-Auswirkung

Die relevante Grenze liegt zwischen nicht vertrauenswürdiger Candidate-Ausführung
und Parent-/Framework-Source- sowie Git-Zustand. Das dokumentierte Design
verhindert, dass der Candidate in eines der Repositories oder dessen `.git`-
Metadaten schreibt, und erzwingt alle unterstützten, legitimen Workflow-
Ausgabe-Roots unter seinem privaten externen Child. Dies ist kein allgemeiner
Kernel-Namespace und beweist nicht, dass bösartiger Candidate-Code nicht an
beliebige nicht zusammenhängende, global world-writable Host-Orte schreiben
kann. Finale Security-Scan-Evidence wird in diesem Implementierungsrecord nicht
behauptet und liegt in der zugehörigen Scan-Evidence vor. Der Parent-Workflow-/
Helper-SHA ist vor dem Root-seitigen Setup vertrauenswürdig; `validate_only`
ist keine Sandbox für eine nicht vertrauenswürdige Parent-Ref. Seine Branch-
Allowlist ist kein Schutz gegen einen feindlichen Writer im selben Repository;
dies erfordert Branch Protection oder Environment Approval.

## Geänderte Dateien

- `.github/workflows/update-submodules.yml`
- `ci/tools/prepare-readonly-submodule-validation-sandbox.py`
- `tests/test_ci_security_workflows.py`
- `tests/test_prepare_readonly_submodule_validation_sandbox.py`
- `docs/build/README.md`
- `docs/build/README.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- `reports/audits/change-records/CR-20260811-enforce-readonly-submodule-validator.md`
- `reports/audits/change-records/CR-20260811-enforce-readonly-submodule-validator.de.md`

Die implementierte Grenze liegt in `.github/workflows/update-submodules.yml`
und `ci/tools/prepare-readonly-submodule-validation-sandbox.py`; Contract-
Coverage liegt in `tests/test_ci_security_workflows.py` und
`tests/test_prepare_readonly_submodule_validation_sandbox.py`. Die Änderung
verändert weder Makefile, Parent-Gitlink, Framework noch MRTS.

## Ausgeführte Befehle

Die folgenden Parent-Prüfungen wurden unabhängig durch die Root-Aufgabe
ausgeführt und als direkte Evidence gemeldet:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_prepare_readonly_submodule_validation_sandbox tests.test_ci_security_workflows` endete mit Exit 0: 38 Tests liefen, 37 bestanden und 1 war ein erwarteter Skip, weil die UID/GID `nobody` im User-Namespace nicht verfügbar ist.
- `PYTHONDONTWRITEBYTECODE=1 make check-ci-security-contract` endete mit Exit 0, einschließlich 26 CI-Workflow-Tests und Validate-only-Prüfungen für actionlint, zizmor und den gitleaks-Lock.
- `make check-bilingual-docs` lief nach der Validate-only-Korrektur zum
  Branch-Scope erneut und bestand (`bilingual docs ok`).
- `git diff --check` endete nach der Validate-only-Korrektur zum Branch-Scope
  mit Exit 0 ohne Ausgabe.

## Runtime-Evidence

Dieser Implementierungsrecord behauptet keine finalen Exact-Head-Hosted-
Runtime- oder Validierungs-, Veröffentlichungs-, Pull-Request-, Merge- oder
anderen Delivery-Ergebnisse; diese liegen in der zugehörigen PR-Evidence vor.

## Nicht ausgeführte Prüfungen mit Begründung

- `make quick-check` — durch diese Aufgabe unverändert; für den reinen
  Dokumentations-Scope wurde keine Candidate-Ausführung lokal durchgeführt.
- Hosted-`update-submodules.yml`-Validierung einschließlich
  `validate_only: true` — finale Exact-Head-Hosted-Evidence wird hier nicht
  behauptet und liegt in der zugehörigen PR-Evidence vor.
- Security-Scan — finale Security-Scan-Evidence wird hier nicht behauptet und
  liegt in der zugehörigen Scan-Evidence vor.
- `make check-bilingual-docs` schlug zunächst fehl, weil diesem Change Record
  die vom Checker verlangten Überschriften fehlten und der Baseline-Clone nicht
  initialisierte Framework-Link-Targets enthält; nach der Korrektur bestand der
  oben dokumentierte erneute Lauf.

## Bekannte Einschränkungen

Der Record dokumentiert die beabsichtigte Grenze anhand der Anforderungen der
abgegrenzten Implementierung. Er liefert selbst keinen unabhängigen Nachweis
für Runner-Identitätsverhalten, Dateisystemberechtigungen oder finale Hosted-
Ausführung am dispatchten SHA. Der abgegrenzte Source-/Output-Vertrag ist keine
Evidence für allgemeine Host-Dateisystemisolierung.

## Verbleibende Risiken

Die korrekte Wirkung hängt davon ab, dass die Workflow-Implementierung den
externen privaten Child weiterhin anlegt und die dedizierte Identität sowie die
schreibgeschützten Berechtigungen vor der Candidate-Ausführung anwendet. Er
umfasst keine nicht zusammenhängenden, global world-writable Host-Orte, die
bösartiger Candidate-Code außerhalb des unterstützten Workflow-Output-Vertrags
nutzen könnte. Finale Runtime-, Hosted-, Scan- und Delivery-Evidence liegt in
der zugehörigen PR- und Scan-Evidence vor.

## Finaler Diff- und Review-Status

Abgegrenzter Englisch-/Deutsch-Paritäts- und `git diff --check`-Review
bestanden. Dieser Implementierungsrecord behauptet nur seine lokale
Dokumentationsvalidierung; finale Exact-Head-Hosted-Validierungs-, Security-
Scan- und Delivery-Evidence liegt in der zugehörigen PR- und Scan-Evidence vor.
