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
enger Validate-only-Aufruf für genau zwei vertrauenswürdige Parent-Refs
erforderlich: den genauen Head des task-eigenen/reviewten Reparatur-Branch
`fix/ci-enforce-readonly-submodule-validation` vor dem Merge und geschützten
Parent-`master` erst nach dem Merge dieser Reparatur für die Sandbox-
Revalidierung des resultierenden `master`, wenn GitHub
`github.ref_protected == true` meldet, ohne den Publisher ausführbar zu machen.

Der Hosted-Run `31479137202`, Validator-Job `93739826304`, zeigte eine in
diesem Vertrag fehlende Host-Pfad-Voraussetzung: `modsecurity-validator` konnte
das private `/home/runner` nicht durchqueren, um den `RUNNER_TEMP`-Guard zu
erreichen, und das Guard-`mkdir` schlug mit `Permission denied` fehl. Die
Reparatur bewahrt die schreibgeschützte Source-/Git-Grenze und erlaubt nur
Traversal zum benötigten externen Guard; sie ist keine Evidence erfolgreicher
Hosted-Validierung.

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
- Vertrauenswürdiges Root-seitiges Setup gewährt `modsecurity-validator` auf
  den benötigten Ahnen von `$RUNNER_TEMP` Traversal-only-ACL-Zugriff, wenn ein
  Hosted-Runner einen privaten Ahnen hat. Die ACL gewährt weder List- noch
  Schreibzugriff und bewahrt Source-/Git-Locks, Root-Guard und privates
  Output-Child.
- Manueller `workflow_dispatch` mit `validate_only: true` ist auf genau zwei
  vertrauenswürdige Refs im kanonischen Non-fork-Parent-Repository
  `Easton97-Jens/ModSecurity-conector` beschränkt: den task-eigenen/reviewten
  Reparatur-Branch `fix/ci-enforce-readonly-submodule-validation` vor dem
  Merge und geschützten Parent-`master` erst nach dem Merge dieser Reparatur für
  die Sandbox-Revalidierung des resultierenden `master` und wenn GitHub
  `github.ref_protected == true` meldet. Er ist keine Einrichtung zum Ausführen
  beliebiger nicht vertrauenswürdiger Parent-Refs oder Pull Requests. Jeder
  erlaubte Pfad verwendet den jeweiligen dispatchten `github.sha`,
  erzwingt die Validierung auch bei gleichem Candidate und Gitlink und schließt
  den Publisher von der Ausführung aus.
- An beiden erlaubten Refs sind Parent-Workflow- und Helper-SHA vor dem
  Root-seitigen Setup vertrauenswürdig; der Framework-Candidate bleibt nicht
  vertrauenswürdiger, durch die Sandbox regierter Code. Die Zwei-Ref-Allowlist
  ist eine Guardrail; der Master-Pfad erfordert zusätzlich
  `github.ref_protected == true`. Keine der Bedingungen schützt gegen einen
  feindlichen Writer im selben Repository ohne Branch Protection oder
  Environment Approval.
- Die Validate-only-Revalidierung auf geschütztem `master` unterscheidet sich
  vom autorisierten Updater-Dispatch nach dem Merge auf `master` mit falschem
  `validate_only`.
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

Die Reparatur fügt auf den benötigten Ahnen von `$RUNNER_TEMP` eine
Root-trusted Traversal-only-ACL hinzu. Sie behebt den historischen Run
`31479137202`, Validator-Job `93739826304`, in dem die dedizierte Identität
`/home/runner` nicht durchqueren konnte und das Guard-`mkdir` `Permission
denied` zurückgab. Sie gibt dem Validator keine List- oder Schreibberechtigung
auf diesen Ahnen und lässt Root-Guard, privates Output-Child sowie Parent- /
Framework-Source-/Git-Locks unverändert. Dies ist eine abgegrenzte Hosted-
Host-Pfad-Reparatur, kein Nachweis allgemeiner Host-Isolation oder eines
erfolgreichen Reruns.

Für Exact-Head-Nachweis und Revalidierung des resultierenden `master` darf
manueller `workflow_dispatch` `validate_only: true` nur im kanonischen
Non-fork-Parent-Repository an genau zwei vertrauenswürdigen Refs setzen: am
task-eigenen/reviewten Reparatur-Branch
`fix/ci-enforce-readonly-submodule-validation` vor dem Merge oder am
geschützten Parent-`master` erst nach dem Merge dieser Reparatur. Ersterer
liefert den Exact-Head-Nachweis vor dem Merge; letzterer führt die Sandbox auf
dem resultierenden `master`-Tree erneut aus und erfordert, dass GitHub
`github.ref_protected == true` meldet. Keiner der Pfade ist eine allgemeine
Einrichtung zum Ausführen beliebiger nicht vertrauenswürdiger Parent-Refs oder
Pull Requests. Jeder checkt den jeweiligen dispatchten `github.sha` in Resolver
und Validator aus, erzwingt den Validierungsjob auch dann, wenn der Framework-
Candidate dem dispatchten Parent-Gitlink entspricht, und schließt den Publisher
explizit aus. Er kann weder einen Gitlink-Branch noch einen Pull Request
erstellen oder aktualisieren. Dies ist keine Sandbox für nicht vertrauenswürdige
Parent-Pull-Requests/-Refs: An beiden erlaubten Refs sind Parent-Workflow- und
Helper-SHA vor dem Root-seitigen Setup vertrauenswürdig, während der Framework-
Candidate nicht vertrauenswürdiger, durch die Sandbox regierter Code bleibt.
Ein Hosted-Erfolg wäre funktionale Evidence nur für den jeweiligen reviewten
Reparatur-SHA oder resultierenden geschützten Master-SHA. Die Zwei-Ref-
Allowlist ist eine Guardrail; der Master-Pfad erfordert zusätzlich
`github.ref_protected == true`. Keine der Bedingungen schützt gegen einen
feindlichen Writer im selben Repository ohne Branch Protection oder Environment
Approval. Der separat autorisierte Updater-Dispatch nach dem Merge
läuft auf `master` mit falschem `validate_only`; er validiert den Übergang vom
vertrauenswürdigen Default Branch und darf nach der Validierung den begrenzten
Publisher erreichen. Keiner der Validate-only-Pfade erteilt
Veröffentlichungsberechtigung oder ersetzt diesen Updater-Dispatch nach dem
Merge.

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
behauptet und liegt in der zugehörigen Scan-Evidence vor. An beiden erlaubten
Validate-only-Refs sind Parent-Workflow-/Helper-SHA vor dem Root-seitigen Setup
vertrauenswürdig; `validate_only` ist keine Sandbox für eine nicht
vertrauenswürdige Parent-Ref. Seine Zwei-Ref-Allowlist ist kein Schutz gegen
einen feindlichen Writer im selben Repository; der Master-Pfad erfordert auch
`github.ref_protected == true`, während dieses Threat Model Branch Protection
oder Environment Approval erfordert.

Die ACL-Reparatur hat dieselbe Grenze: Vertrauenswürdiges Root-seitiges Setup
darf auf den Ahnen, die zum Erreichen von `$RUNNER_TEMP` benötigt werden, nur
Directory-Traversal gewähren; List- oder Schreibzugriff darf es nicht gewähren.
Ihre Wirkung ist auf die in Run `31479137202` beobachtete private Hosted-
Ahnenbedingung begrenzt, nicht auf allgemeine Host-Dateisystemisolation.

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
- `make check-bilingual-docs` lief nach der Validate-only-Korrektur zur
  Protected-master-Enforcement erneut und bestand (`bilingual docs ok`).
- `git diff --check` endete nach der Validate-only-Korrektur zur Protected-
  master-Enforcement mit Exit 0 ohne Ausgabe.

## Runtime-Evidence

Hosted-Run `31479137202`, Validator-Job `93739826304`, schlug vor der Candidate-
Ausführung fehl, weil `modsecurity-validator` `/home/runner` nicht zum
`RUNNER_TEMP`-Guard durchqueren konnte und `mkdir` `Permission denied`
zurückgab. Dies ist Failure-Evidence nur für die fehlende Traversal-
Berechtigung. Dieser Record behauptet keinen erfolgreichen Rerun und keine
finalen Exact-Head-Hosted-Runtime- oder Validierungs-, Veröffentlichungs-, Pull-
Request-, Merge- oder anderen Delivery-Ergebnisse.

## Nicht ausgeführte Prüfungen mit Begründung

- `make quick-check` — durch diese Aufgabe unverändert; für den reinen
  Dokumentations-Scope wurde keine Candidate-Ausführung lokal durchgeführt.
- Ein Hosted-Rerun von `update-submodules.yml` einschließlich
  `validate_only: true` — für diesen Repair-Record nicht ausgeführt; der
  beobachtete Run `31479137202` schlug vor der Candidate-Ausführung fehl und
  ist daher keine erfolgreiche Repair-Evidence.
- Security-Scan — finale Security-Scan-Evidence wird hier nicht behauptet und
  liegt in der zugehörigen Scan-Evidence vor.
- `make check-bilingual-docs` schlug zunächst fehl, weil diesem Change Record
  die vom Checker verlangten Überschriften fehlten und der Baseline-Clone nicht
  initialisierte Framework-Link-Targets enthält; nach der Korrektur bestand der
  oben dokumentierte erneute Lauf.

## Bekannte Einschränkungen

Der Record dokumentiert die beabsichtigte Grenze anhand der Anforderungen der
abgegrenzten Implementierung. Er liefert selbst keinen unabhängigen Nachweis
für Runner-Identitätsverhalten, reparierte ACL-Wirkung,
Dateisystemberechtigungen oder eine erfolgreiche Hosted-Ausführung an einem
der erlaubten dispatchten SHAs. Der abgegrenzte Source-/Output-Vertrag und die
Host-Pfad-ACL-Reparatur sind keine Evidence für allgemeine Host-
Dateisystemisolation.

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
Dokumentationsvalidierung; finale Hosted-Validierungs-, Security-Scan- und
Delivery-Evidence für erlaubte Refs liegt in der zugehörigen PR- und Scan-
Evidence vor.
