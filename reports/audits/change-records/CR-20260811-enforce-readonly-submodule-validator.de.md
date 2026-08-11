# Change Record: readonly Submodule-Validator durchsetzen

**Sprache:** [English](CR-20260811-enforce-readonly-submodule-validator.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260811-enforce-readonly-submodule-validator |
| Datum (UTC) | 2026-08-11 |
| Basis-Revision | 4749c02c6dd5e285c4309b4e69b0bb28ae459e48 |
| Delivery-Status | Parent-Implementierungs- und Dokumentationsaktualisierung; keine Git- oder GitHub-Delivery-Aktion ausgeführt |

## Motivation und Problemstellung

Der Framework-Submodule-Updater validiert einen aufgelösten Candidate, bevor
ein separater Publisher eine Parent-Gitlink-Aktualisierung vorschlagen darf.
Die Dokumentation für Leser muss die beabsichtigte Dateisystem- und
Privilegiengrenze korrekt beschreiben, ohne die Implementierungsbeschreibung in
unbeobachtete Hosted- oder Security-Evidence zu verwandeln.

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

Der Root-seitige Helper inventarisiert beide gesperrten Source-Trees vor der
Candidate-Ausführung und prüft nach dem Check ihre exakte Gleichheit. Das
Inventar zeichnet Pfad, Typ, Größe, Modus, UID, GID und Link-Anzahl sowie
SHA-256 für reguläre Dateien und Link-Text für symbolische Links auf. Separat
scannt er den externen Tree fail-closed: Zugelassen sind nur dem Validator
gehörende Directories und reguläre Dateien ohne Group-/Other-Schreibrechte;
Special Objects, symbolische Links und Hard Links in den Source-Tree werden
abgewiesen.

Dieser Change Record dokumentiert den beabsichtigten Vertrag. Er behauptet
nicht, dass ein Hosted-Workflow-Lauf, eine Candidate-Validierung,
Veröffentlichung, ein Pull Request oder Merge stattgefunden hat.

## Security-Auswirkung

Die relevante Grenze liegt zwischen nicht vertrauenswürdiger Candidate-Ausführung
und Parent-/Framework-Source- sowie Git-Zustand. Das dokumentierte Design
verhindert, dass der Candidate in eines der Repositories oder dessen `.git`-
Metadaten schreibt, und erzwingt alle unterstützten, legitimen Workflow-
Ausgabe-Roots unter seinem privaten externen Child. Dies ist kein allgemeiner
Kernel-Namespace und beweist nicht, dass bösartiger Candidate-Code nicht an
beliebige nicht zusammenhängende, global world-writable Host-Orte schreiben
kann. Ein Security-Scan wurde in dieser Dokumentationsaufgabe weder ausgeführt
noch behauptet.

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
- `make check-bilingual-docs` lief nach den Überschriften- und deutschen
  Link-Korrekturen erneut und bestand (`bilingual docs ok`).

## Runtime-Evidence

Keine. Dieser Record enthält absichtlich keine Hosted-Run-, Runtime-,
Veröffentlichungs-, Pull-Request- oder Merge-Behauptung.

## Nicht ausgeführte Prüfungen mit Begründung

- `make quick-check` — durch diese Aufgabe unverändert; für den reinen
  Dokumentations-Scope wurde keine Candidate-Ausführung lokal durchgeführt.
- Hosted-`update-submodules.yml`-Validierung — kein Workflow-Dispatch und keine
  Hosted-Beobachtung durchgeführt.
- Security-Scan — nicht ausgeführt; dieser Record behauptet kein
  Security-Scan-Ergebnis.
- `make check-bilingual-docs` schlug zunächst fehl, weil diesem Change Record
  die vom Checker verlangten Überschriften fehlten und der Baseline-Clone nicht
  initialisierte Framework-Link-Targets enthält; nach der Korrektur bestand der
  oben dokumentierte erneute Lauf.

## Bekannte Einschränkungen

Der Record dokumentiert die beabsichtigte Grenze anhand der Anforderungen der
abgegrenzten Implementierung. Er weist weder Runner-Identitätsverhalten,
Dateisystemberechtigungen noch einen Hosted-Candidate-Lauf unabhängig nach.
Der abgegrenzte Source-/Output-Vertrag ist keine Evidence für allgemeine
Host-Dateisystemisolierung.

## Verbleibende Risiken

Die korrekte Wirkung hängt davon ab, dass die Workflow-Implementierung den
externen privaten Child weiterhin anlegt und die dedizierte Identität sowie die
schreibgeschützten Berechtigungen vor der Candidate-Ausführung anwendet. Er
umfasst keine nicht zusammenhängenden, global world-writable Host-Orte, die
bösartiger Candidate-Code außerhalb des unterstützten Workflow-Output-Vertrags
nutzen könnte. Runtime- und Hosted-Verifikation bleiben separate
Evidence-Pflichten.

## Finaler Diff- und Review-Status

Abgegrenzter Englisch-/Deutsch-Paritäts- und `git diff --check`-Review
bestanden. Hosted-Validierung und Security-Scan-Ergebnisse bleiben `not_run`.
Es werden weder Commit, Push, Pull Request, Merge, CI-Ergebnis,
SonarQube-Ergebnis noch Security-Scan-Ergebnis behauptet.
