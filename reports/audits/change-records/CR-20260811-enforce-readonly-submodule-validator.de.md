# Change Record: readonly Submodule-Validator durchsetzen

**Sprache:** [English](CR-20260811-enforce-readonly-submodule-validator.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260811-enforce-readonly-submodule-validator |
| Datum (UTC) | 2026-08-11 |
| Basis-Revision | `4749c02c6dd5e285c4309b4e69b0bb28ae459e48` |
| Delivery-Status | Implementierte und lokal validierte Parent-Reparatur; Current-Head-Security-Scan, Hosted-Validierung, PR-Verifikation und Delivery sind noch ausstehend. |

## Motivation und Problemstellung

Der Framework-Submodule-Updater muss einen nicht vertrauenswürdigen
Framework-Candidate validieren, ohne ihm Host-seitigen Schreibzugriff auf
Parent, Framework oder deren Git-Metadaten zu geben. Der frühere Ansatz über
Host-Pfad-ACLs lieferte für das private Pfadlayout des Hosted-Runners keine
verlässliche Least-Privilege-Ausführungsgrenze. Die Reparatur verschob die
Candidate-Ausführung deshalb in einen Root-seitig erstellten privaten Mount- und
PID-Namespace, statt Host-Ahnen-ACLs zu erweitern.

Der Hosted-Run [31488072111](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/31488072111)
ist nur historische Failure-Evidence auf exaktem Head
`5d7d7bbbbb968aa9755d3c0c67a09d8acd651c77`: Resolver und Sandbox-Setup waren
erfolgreich, aber der Validator scheiterte während `make quick-check` mit fünf
No-CRS-Normalisierungsfehlern an einer Runtime-Verzeichnis-
Traversierungsverweigerung. Der Publisher wurde übersprungen; der Run belegt
somit keine Branch-, Commit- oder Pull-Request-Mutation. `FND-PARENT-0122` ist
exakt als P1, bestätigt, `in_progress`, sicherheitsrelevant und
release-/candidate-integration-blocking erfasst; es gibt keinen fixed- oder
verified-Status.

Die funktionale Release-Blocker-Reparatur modelliert nur die enthaltene
relative Form im Zusammenhang mit `checks/common.pem` im Hosted-Run
`31496603345`. Diese Run-ID identifiziert nur den betroffenen Hosted-Kontext;
ein frischer Hosted-Run auf dem exakten Head muss nachweisen, dass das
tatsächliche Link-Target der Regel entspricht. Dieser Record behauptet weder
einen erfolgreichen Run noch eine erfolgreiche spätere Hosted-Validierung.

## Akzeptanzkriterien

- Vertrauenswürdiges Root-seitiges Setup erstellt einen privaten Mount- und
  PID-Namespace, setzt die Mount-Propagation auf `rprivate` und hält dessen
  Lebenszyklus außerhalb der Candidate-Kontrolle.
- Der Candidate erhält Parent- und Framework-Sources einschließlich `.git` nur
  über nicht-rekursive read-only-`nosuid,nodev`-Namespace-Views.
- Der Workflow muss ein frisches `mktemp -d`-direktes Child
  `/tmp/modsecurity-readonly-namespace.XXXXXX` unter dem sticky `/tmp`
  erstellen, es exakt auf `root:modsecurity-validator` mit Modus `0750` setzen
  und über das erforderliche Argument `--namespace-parent` übergeben. Der
  Launcher akzeptiert nur ein leeres, nicht-symlinktes direktes Child des
  root-owned sticky `/tmp` mit genau diesem Owner und Modus.
- Der Candidate erhält eine schreibbare `nosuid,nodev`-Namespace-View nur für
  das exakte Child `external` des physischen `--write-root`. Die festen
  logischen Platzhalter `mount-root`, `source` und `external` sind jeweils
  `root:modsecurity-validator` mit Modus `0750`, während der physische
  Write-Root `root:root` mit Modus `0711` ist und sein exaktes physisches Child
  `external` validator-owned mit Modus `0700` bleibt; die Root-seitige
  Verifikation prüft die physischen Pfade.
- Der Candidate ist PID 1 im privaten Namespace; der vertrauenswürdige Launcher
  verarbeitet seine Beendigung vor dem Ende dieses Namespace, garantiert damit
  keine Candidate-Nachzügler und führt danach Root-seitige Host-Verifikation
  durch. Teardown verwendet weder Lazy-Unmount noch `rmtree`: Er entfernt nur
  exakte leere Platzhalter mit nicht-rekursivem `rmdir`, und der `EXIT`-Trap des
  Workflows verwendet nicht-rekursives `rmdir` für das vertrauenswürdige
  Namespace-Parent.
- Die lokal implementierte enge Reparatur mountet ein frisches privates `proc`-
  Dateisystem bei `/proc` innerhalb von PID 1, nachdem `rprivate` eingerichtet
  ist, mit `readonly,nosuid,nodev,noexec`. Root mountet es vor
  `PR_SET_NO_NEW_PRIVS` und dem Drop der Validator-Identität, unmountet es
  anschließend und stellt das vorherige `/proc`-Arrangement wieder her, bevor
  der Namespace endet. Es dient ausschließlich dem PID-lokalen `/proc`-Lookup
  von LeakSanitizer (LSan) und ist weder vollständige Host- oder Kernel-
  Isolation; Hosted-Validierung und Finding-Abschluss bleiben ausstehend.
- Der Root-Workflow ruft einen vertrauenswürdigen Root-`sudo -n python3`-
  Launcher auf. Der Launcher setzt `PR_SET_NO_NEW_PRIVS` fail-closed, entfernt
  zusätzliche Gruppen, fällt auf die Non-login- und Non-sudo-GID und UID von
  `modsecurity-validator` zurück und führt das feste Candidate-Programm über
  `execve` mit einer expliziten festen Umgebung statt einer geerbten Runner-
  Umgebung aus. Dieses Programm führt den unveränderten `make quick-check` aus
  und erhält keine Publisher- oder Produktions-Schreibberechtigung.
- Source-Inventar und physische Output-Verifikation bleiben nach Candidate-Ende
  fail-closed.
- Ein symbolischer Link für externe Ausgaben wird nur akzeptiert, wenn er dem
  Validator gehört und sein Link-Text nicht leer, NUL-frei und relativ ist und
  sich lexikalisch innerhalb des physischen Roots `external` normalisiert. Die
  Verifikation darf sein Target nicht auflösen, kein `stat` ausführen und es
  nicht dereferenzieren; absolute Targets, auch in-root absolute Targets,
  lexikalische Escapes zu Source-, Guard- oder anderen Pfaden, Special Objects
  und Hard Links in den Source-Tree bleiben abgewiesen.
- `validate_only: true` bleibt der bestehende nicht veröffentlichende
  Exact-Ref-Pfad und darf keine Einrichtung für beliebige nicht vertrauenswürdige
  Parent-Refs werden.
- Englische und deutsche Dokumente sowie Change Records enthalten dieselben
  wesentlichen Fakten, Evidence-Status und Einschränkungen.

## Implementierungsentscheidung und Begründung

Die Reparatur verwendet Root-seitige Namespace-Konstruktion, weil x-only
Host-ACLs für die bestehende Runtime-Pfad-Validierung keine angemessene
Schnittstelle sind: Das Öffnen eines Verzeichnisses kann Leserecht verlangen,
obwohl reines Traversieren genügt. Der Root-seitige Launcher setzt `rprivate`,
bevor er die Candidate-Mount-View erstellt, bind-mountet Parent- und
Framework-Source-/Git-Zustand read-only, nicht-rekursiv, mit `nosuid,nodev` und
bind-mountet nur das physische Child `--write-root`/`external` schreibbar mit
`nosuid,nodev`. Vor dem Start erstellt die Root-Seite des Workflows das
vertrauenswürdige direkte `/tmp`-Child mit `mktemp -d`, ändert es auf
`root:modsecurity-validator` mit Modus `0750` und übergibt es über das
erforderliche Argument `--namespace-parent`. Der Launcher validiert diese
exakte leere Nicht-Symlink-Topologie und erstellt dann seine festen logischen
Platzhalter `mount-root`, `source` und `external` als
`root:modsecurity-validator` mit Modus `0750`. Der physische Write-Root bleibt
`root:root` mit Modus `0711`, und sein exaktes physisches Child `external`
bleibt validator-owned mit Modus `0700`. Der Launcher setzt
`PR_SET_NO_NEW_PRIVS` fail-closed, entfernt zusätzliche Gruppen, setzt
Candidate-GID und -UID und ruft `execve` mit einer expliziten festen Umgebung
auf. Der Candidate läuft als PID 1 im privaten PID-Namespace. Der Launcher
wartet auf und verarbeitet seine Beendigung, entfernt nur die exakten leeren
Platzhalter mit nicht-rekursivem `rmdir` und verifiziert als root physischen
Host-Source- und Output-Zustand; der `EXIT`-Trap des Workflows entfernt das
vertrauenswürdige Namespace-Parent ebenfalls nur mit nicht-rekursivem `rmdir`.

Die lokal implementierte enge Reparatur mountet ein frisches privates `proc`-Dateisystem
bei `/proc` innerhalb von PID 1 erst, nachdem der Mount-Namespace `rprivate`
ist, mit `readonly,nosuid,nodev,noexec`. Root führt diesen Mount vor dem Setzen
von `PR_SET_NO_NEW_PRIVS` und dem Drop der Validator-Identität durch, unmountet
ihn anschließend und stellt das vorherige `/proc`-Arrangement wieder her,
bevor der Namespace endet. Dies unterstützt ausschließlich den PID-lokalen
`/proc`-Lookup von LeakSanitizer (LSan); es erweitert weder den Namespace-Claim
zu vollständiger Host- oder Kernel-Isolation. Hosted-Validierung und Finding-
Abschluss bleiben ausstehend.

Dies erhält den beabsichtigten Output-Vertrag, ohne dem Candidate Host-seitiges
Traverse- oder List-Recht für Runner-eigene Ahnen zu geben. Parent, Framework
und unterstützte Ausgaben werden nur über Namespace-Views bereitgestellt;
nicht zusammenhängende ambient Host-Pfade bleiben außerhalb dieses Contracts.
Die separate Publisher-Grenze bleibt erhalten; Framework- und MRTS-Source, der
Parent-Gitlink sowie die Semantik der Make-Targets liegen außerhalb des Scopes.

Der physische External-Output-Verifier erlaubt jetzt nur den engen,
validator-owned Relative-Link-Fall aus den Akzeptanzkriterien. Seine Prüfung ist
lexikalische Containment-Prüfung von nicht leerem, NUL-freiem Link-Text im
physischen Root `external`, keine Target-Auflösung oder Filesystem-Inspektion.
Dies modelliert nur eine enthaltene relative Form für `checks/common.pem`; ein
frischer Hosted-Run auf dem exakten Head muss nachweisen, dass das tatsächliche
Target entspricht. Es erhält zugleich die fail-closed-Abweisung absoluter
Links (auch in-root), lexikalischer Escapes, Special Objects und Hard Links in
den Source-Tree.

Der vorhandene `workflow_dispatch`-Input `validate_only: true` bleibt auf den
vertrauenswürdigen Task-Reparatur-Ref vor dem Merge und geschützten Parent-
`master` nach dem Merge mit `github.ref_protected == true` beschränkt. Jeder
erlaubte Pfad verwendet seinen dispatchten `github.sha`, erzwingt Candidate-
Validierung auch bei gleichem Candidate und Gitlink und macht den Publisher
ineligible. Dies ist keine Sandbox für nicht vertrauenswürdige Parent-Pull-
Requests/-Refs: Parent-Workflow und Helper sind vor dem Root-seitigen
Namespace-Setup vertrauenswürdig, der Framework-Candidate ist die nicht
vertrauenswürdige Payload.

## Security-Auswirkung

Die relevante Sicherheitsgrenze liegt zwischen nicht vertrauenswürdiger
Framework-Candidate-Ausführung und Parent-/Framework-Source-/Git-Zustand sowie
dem Updater-Publisher. Der private Mount-/PID-Namespace verhindert, dass der
Candidate eine schreibbare Source-View erhält, und beschränkt unterstützte
Candidate-Ausgaben auf den physischen externen Root, den Root-seitige
Verifikation prüft. `rprivate` verhindert, dass Candidate-Mount-Änderungen
über geteilte Mount-Propagation zurückwirken. `nosuid,nodev` reduziert die
Angriffsfläche der Mount-Views. `PR_SET_NO_NEW_PRIVS` wird vor dem Candidate-
Identity-Drop fail-closed gesetzt, und der Candidate prüft `NoNewPrivs: 1`.
Der lokal implementierte private `/proc`-Mount ist auf PID 1 beschränkt und verwendet
`readonly,nosuid,nodev,noexec`; Root mountet und entfernt ihn während des
Namespace-Lebenszyklus ausschließlich für den PID-lokalen LSan-Lookup.

Dies ist keine vollständige Host- oder Kernel-Sicherheitsisolation. Parent,
Framework und unterstützte Ausgaben sind die einzigen bereitgestellten
Namespace-Views; nicht zusammenhängende ambient Host-Pfade bleiben außerhalb
des Contracts. Es beweist nicht, dass bösartiger Candidate-Code jede nicht
zusammenhängende, global beschreibbare Host-Einrichtung verwenden, einen
Kernel-Fehler ausnutzen oder eine Prozessgrenze überwinden kann. Die Reparatur
lockert weder Source-/Git-Locks, Output-Verifikation, Validate-only-Publisher-
Guardrails, Branch Protection noch Publisher-Berechtigungen.

Der zulässige Symbolic-Link-Fall erweitert diese Grenze nicht: Target-Text wird
lexikalisch geprüft, ohne ein Objekt aufzulösen, zu statten oder zu
dereferenzieren, und alle nicht konformen Links bleiben abgewiesen. Er ist kein
Nachweis vollständiger Host-Isolation.

## Geänderte Dateien

Die implementierte Reparatur ändert den Parent-Validator-Workflow, den
Root-seitigen Preparer und Namespace-Launcher, fokussierte Contract-Tests sowie
dieses englische/deutsche Build-Dokumentations- und Change-Record-Paar. Sie
autorisiert keine Framework- oder MRTS-Änderung, keine Parent-Gitlink-Änderung
und keine Delivery-Aktion. Die finale exakte Liste geänderter Dateien muss vor
Delivery mit dem reviewten Reparatur-Head abgeglichen werden.

## Ausgeführte Befehle

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
  tests.test_ci_security_workflows
  tests.test_prepare_readonly_submodule_validation_sandbox
  tests.test_run_readonly_submodule_validation_namespace` bestand: 55 Tests
  mit drei erwarteten Capability-Skips.
- `PYTHONDONTWRITEBYTECODE=1 make check-ci-security-contract` bestand mit
  demselben 55-Test-/Drei-Skip-Suite-Ergebnis sowie seinen `validate_only`-
  actionlint-, zizmor- und gitleaks-lock-Prüfungen.
- `PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs` bestand (`bilingual
  docs ok`); no-bytecode `py_compile` und `git diff --check` bestanden ebenfalls.

Dies ist begrenzte lokale Test- und Contract-Evidence. Die drei erwarteten
Capability-Skips bedeuten, dass sie kein privilegierter Runtime-Nachweis für
Mounts oder die Validator-Identität ist. Sie ersetzt keinen Current-Head-
Security-Scan, keine Hosted-Validierung, keine PR-Checks, kein SonarQube Cloud,
kein Review, keinen Merge, keine resulting-master-Validierung und keine
Delivery.

## Runtime-Evidence

Run `31488072111` ist die einzige neu erfasste Hosted-Tatsache in dieser
Reparaturrunde: Er schlug auf exaktem Head
`5d7d7bbbbb968aa9755d3c0c67a09d8acd651c77` nach Resolver und Sandbox-Setup
während des isolierten Quick Checks fehl. Seine Root-seitige Post-Run-Source-/
Output-Verifikation lief nicht, sein Publisher wurde übersprungen und sein
Outcome schlug fehl, weil die Validierung fehlschlug. Er ist kein erfolgreicher
Namespace-Run, Security-Scan, PR-Check, Merge- oder Delivery-Ergebnis.

Hosted-Run `31496603345` liefert den `checks/common.pem`-Kontext für die
funktionale Verifier-Reparatur. Er ist hier nicht als erfolgreicher Hosted-Run
oder als Validierung des reparierten Current-Heads erfasst; ein frischer
Hosted-Run auf dem exakten Head muss nachweisen, dass das tatsächliche Target
der Regel entspricht.

## Nicht ausgeführte Prüfungen mit Begründung

- Ein Current-Head-Security-Scan — bis zum finalen Namespace-Reparatur-Head
  ausstehend.
- Ein frischer Hosted-`validate_only`-Run — bis zum finalen Namespace-
  Reparatur-Head ausstehend.
- PR-Checks, Review-Disposition, SonarQube-Cloud-Ergebnis, Squash-Merge und
  resulting-master-Verifikation — bis zu den Current-Head-Scan- und Hosted-
  Validierungs-Gates ausstehend.
- Ein Updater-Dispatch nach Merge und Draft-Gitlink-PR — außerhalb dieses
  Reparaturrecords, bis die Parent-Reparatur gemergt ist und die
  vertrauenswürdige Default-Branch-Validierung erfolgreich ist.

## Bekannte Einschränkungen

Dieser Record beschreibt ein implementiertes Design mit begrenzter lokaler
Validierung. Er beweist nicht unabhängig GitHub-hosted-Runner-Verhalten,
Hosted-Mount-/PID-Namespace-Verfügbarkeit, Current-Head-Source-Integrität oder
erfolgreiche Hosted-Ausführung. Der Reparatur-Head benötigt weiterhin
Exact-Head-Security-Scan und Hosted-Validierung.

## Verbleibende Risiken

Die korrekte Wirkung hängt von GitHub-hosted-Linux-Unterstützung für die
erforderlichen Root-seitigen Namespace- und Mount-Operationen ab sowie davon,
dass der Launcher bei Setup-, Lifecycle-Cleanup- oder physischer Host-
Verifikationsstörung fail-closed scheitert. Ein privater Mount-/PID-Namespace
ist bewusst enger als eine allgemeine Host-Sandbox. `FND-PARENT-0122` bleibt
offen, bis der Fehler behoben ist und frische lokale, Security- und Hosted-
Evidence beobachtet wurde.

## Finaler Diff- und Review-Status

Dies ist kein finaler Delivery-Record. Die beobachteten Bilingual- und
eingeschränkten Whitespace-Prüfungen sind oben erfasst; finale Current-Head-
Scan-, Hosted-, PR-, SonarQube-, Merge- und resulting-master-Evidence stehen
weiterhin aus.
