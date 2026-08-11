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

## Akzeptanzkriterien

- Vertrauenswürdiges Root-seitiges Setup erstellt einen privaten Mount- und
  PID-Namespace, setzt die Mount-Propagation auf `rprivate` und hält dessen
  Lebenszyklus außerhalb der Candidate-Kontrolle.
- Der Candidate erhält Parent- und Framework-Sources einschließlich `.git` nur
  über nicht-rekursive read-only-`nosuid,nodev`-Namespace-Views.
- Der Candidate erhält eine schreibbare `nosuid,nodev`-Namespace-View nur für
  das exakte Child `external` des physischen `--write-root`; er sieht logische
  Namespace-Pfade unter einem root-owned View-Namen-Verzeichnis mit Modus
  `0755`, während der physische Root `external` validator-owned mit Modus
  `0700` bleibt und Root-seitige Verifikation die physischen Pfade prüft.
- Der Candidate ist PID 1 im privaten Namespace; der vertrauenswürdige Launcher
  verarbeitet seine Beendigung vor dem Ende dieses Namespace, garantiert damit
  keine Candidate-Nachzügler und führt danach Root-seitige Host-Verifikation
  durch. Teardown verwendet weder Lazy-Unmount noch `rmtree`.
- Der Root-Workflow ruft einen vertrauenswürdigen Root-`sudo -n python3`-
  Launcher auf. Der Launcher setzt `PR_SET_NO_NEW_PRIVS` fail-closed, entfernt
  zusätzliche Gruppen, fällt auf die Non-login- und Non-sudo-GID und UID von
  `modsecurity-validator` zurück und führt das feste Candidate-Programm über
  `execve` mit einer expliziten festen Umgebung statt einer geerbten Runner-
  Umgebung aus. Dieses Programm führt den unveränderten `make quick-check` aus
  und erhält keine Publisher- oder Produktions-Schreibberechtigung.
- Source-Inventar und physische Output-Verifikation bleiben nach Candidate-Ende
  fail-closed.
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
`nosuid,nodev`. Ein root-owned Logical-Mount-Root mit Modus `0755` stellt nur
die erforderlichen View-Namen bereit; der physische Root `external` bleibt
validator-owned mit Modus `0700`. Der Launcher setzt `PR_SET_NO_NEW_PRIVS`
fail-closed, entfernt zusätzliche Gruppen, setzt Candidate-GID und -UID und
ruft `execve` mit einer expliziten festen Umgebung auf. Der Candidate läuft als
PID 1 im privaten PID-Namespace. Der Launcher wartet auf und verarbeitet seine
Beendigung, baut die private View ohne Lazy-Unmount oder `rmtree` ab und
verifiziert als root physischen Host-Source- und Output-Zustand.

Dies erhält den beabsichtigten Output-Vertrag, ohne dem Candidate Host-seitiges
Traverse- oder List-Recht für Runner-eigene Ahnen zu geben. Parent, Framework
und unterstützte Ausgaben werden nur über Namespace-Views bereitgestellt;
nicht zusammenhängende ambient Host-Pfade bleiben außerhalb dieses Contracts.
Die separate Publisher-Grenze bleibt erhalten; Framework- und MRTS-Source, der
Parent-Gitlink sowie die Semantik der Make-Targets liegen außerhalb des Scopes.

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

Dies ist keine vollständige Host- oder Kernel-Sicherheitsisolation. Parent,
Framework und unterstützte Ausgaben sind die einzigen bereitgestellten
Namespace-Views; nicht zusammenhängende ambient Host-Pfade bleiben außerhalb
des Contracts. Es beweist nicht, dass bösartiger Candidate-Code jede nicht
zusammenhängende, global beschreibbare Host-Einrichtung verwenden, einen
Kernel-Fehler ausnutzen oder eine Prozessgrenze überwinden kann. Die Reparatur
lockert weder Source-/Git-Locks, Output-Verifikation, Validate-only-Publisher-
Guardrails, Branch Protection noch Publisher-Berechtigungen.

## Geänderte Dateien

Die implementierte Reparatur ändert den Parent-Validator-Workflow, den
Root-seitigen Preparer und Namespace-Launcher, fokussierte Contract-Tests sowie
dieses englische/deutsche Build-Dokumentations- und Change-Record-Paar. Sie
autorisiert keine Framework- oder MRTS-Änderung, keine Parent-Gitlink-Änderung
und keine Delivery-Aktion. Die finale exakte Liste geänderter Dateien muss vor
Delivery mit dem reviewten Reparatur-Head abgeglichen werden.

## Ausgeführte Befehle

Für die implementierte Namespace-Reparatur liegt folgende beobachtete lokale
Evidence vor:

- `make check-ci-security-contract` führte die Workflow-, Root-Preparer- und
  Namespace-Suites erfolgreich aus: 48 Tests endeten mit drei erwarteten
  Capability-Skips in der normalen Sandbox. Die Suite deckt den implementierten Workflow-
  Vertrag, den Root-seitigen Preparer und den Namespace-Launcher ab.
- Drei privilegierte Regressionen liefen außerhalb der normalen Sandbox und
  bestanden 3/3: realer Validator-Schreibzugriff nur auf den physischen
  External-Root, ein realer read-only-Bind-Mount sowie PID-1-Terminierung ohne
  Descendant.
- Doku-Link- und Bilingual-Prüfungen bestanden; `py_compile`, actionlint,
  offline zizmor, targeted gitleaks und `git diff --check` bestanden ebenfalls.

Diese lokalen Ergebnisse validieren Implementierung und fokussierte Controls.
Sie ersetzen keinen Current-Head-Security-Scan, keine Hosted-Validierung,
keine PR-Checks, kein SonarQube Cloud, kein Review, keinen Merge, keine
resulting-master-Validierung und keine Delivery.

## Runtime-Evidence

Run `31488072111` ist die einzige neu erfasste Hosted-Tatsache in dieser
Reparaturrunde: Er schlug auf exaktem Head
`5d7d7bbbbb968aa9755d3c0c67a09d8acd651c77` nach Resolver und Sandbox-Setup
während des isolierten Quick Checks fehl. Seine Root-seitige Post-Run-Source-/
Output-Verifikation lief nicht, sein Publisher wurde übersprungen und sein
Outcome schlug fehl, weil die Validierung fehlschlug. Er ist kein erfolgreicher
Namespace-Run, Security-Scan, PR-Check, Merge- oder Delivery-Ergebnis.

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

Dies ist kein finaler Delivery-Record. Englisch-/Deutsch-Paritäts- und
Whitespace-Validierung für die aktuelle Dokumentationsänderung bestanden;
finale Current-Head-Scan-, Hosted-, PR-, Merge- und resulting-master-Evidence
stehen weiterhin aus.
