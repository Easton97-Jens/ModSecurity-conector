# Change Record: Source-Preservation der Read-only-Submodule-Sandbox

**Sprache:** [English](CR-20260819-readonly-submodule-sandbox-preservation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260819-readonly-submodule-sandbox-preservation |
| Datum (UTC) | 2026-08-19 |
| Basis-Revision | `35c435483dcd637c7b9df0277bed34d6f94dc44d` |
| Historischer Framework-Gitlink | `bd69ee96e0e7082317d4afe1232bee625665eb9a` |
| Delivery-Status | Draft PR [#302](https://github.com/Easton97-Jens/ModSecurity-conector/pull/302) wurde aus `agent/readonly-submodule-sandbox-preservation` bei `c1b07a572321c31de1a0a9ae1fd554e2f9811b9f` erstellt; der Traceability-Follow-up machte `a0f46d4e22830f081b20096734caf7e4a059b5cd` zu seinem aktuellen committed Head. Erforderliche GitHub Actions bestanden an diesem exakten Head, aber SonarCloud-Check-Run `96097393398` scheiterte an `6.4% Duplication on New Code`. Der aktuelle Benutzer autorisierte eine enge Source-/Test-Remediation und eine bedingte geschützte `master`-Integration nur, nachdem ein Successor-Head Null-Duplikation und alle frischen Gates bestanden hat. Der Successor ist noch nicht committed oder gepusht; PR #302 bleibt Draft und kein Merge wird behauptet. |

## Motivation und Problemstellung

Der Root-seitige Read-only-Submodule-Preparer rief zuvor rekursiv
`_lock_tree(source)` und `_lock_tree(framework)` auf. Diese Aufrufe änderten
den echten Parent-Checkout, Parent `.git` und `.git/modules` sowie den
Framework-Subtree in-place durch `os.chown(..., 0, 0)` und
`os.chmod(... & ~0o022)`. Der historische Kontext sind
[PR #301](https://github.com/Easton97-Jens/ModSecurity-conector/pull/301) und
Merge-Commit `35c435483dcd637c7b9df0277bed34d6f94dc44d`; der Gitlink ist
historischer Kontext und nicht die Ursache. Ein Restore-basierter Ansatz ist
unsicher, weil ursprüngliche Owner, Groups, Modi, ACLs und lokale Workspace-
Policy nicht zuverlässig rekonstruiert werden können.

Der exakte Draft-PR-#302-Head `a0f46d4e22830f081b20096734caf7e4a059b5cd`
scheiterte danach am unveränderten SonarCloud-Quality-Gate wegen
`6.4% Duplication on New Code`. Seine task-eigenen Annotations benennen ein
doppeltes Source-Literal, Cognitive Complexity `16` bei erlaubtem Wert `15`
und eine Test-Assertion mit mehreren potenziell werfenden Aufrufen. Der
Follow-up muss die Duplikation durch quellnative Änderungen auf Null reduzieren,
nicht durch Änderungen an Scanner, Quality Gate, Exclusion, Suppression,
`NOSONAR` oder Issue-Dismissal.

## Akzeptanzkriterien

- Parent, Framework, `.git` und `.git/modules` bleiben über Prepare-,
  Candidate-, Verify-, Fehler- und Cleanup-Pfade hinweg byte-, typ-, owner-,
  group-, modus-, link- und link-target-identisch.
- Der Candidate erhält weiterhin nur nicht-rekursive Read-only-Source-Views;
  ausschließlich der exakte private `external`-Output-Root ist beschreibbar.
- Der Candidate bleibt eine dedizierte unprivilegierte Identität mit leeren
  Supplementary Groups, keinen effektiven Capabilities und `no_new_privs`.
- Das vollständige Source-Inventar wird vor der Candidate-Ausführung erhoben
  und danach verglichen; Output-, Link-, Hardlink-, Gitfile-, Mount- und
  Descriptor-Kontrollen bleiben fail-closed.
- Verschachtelte Source-Mounts werden vor Source-Bind oder Candidate-Code
  abgelehnt.
- Root-Nutzung im Workflow ist auf privaten Guard/Identity/Inventory/Namespace/
  Cleanup beschränkt; Candidate-State-Prüfungen und `git diff --check` laufen
  nicht über `sudo`.
- Cleanup akzeptiert nur ein geprüftes direktes privates Child von
  `RUNNER_TEMP` und kann weder Symlinks folgen, Source traversieren noch einen
  aktiven Mount löschen.
- Ein Successor-Exact-PR-#302-Head meldet `new_duplicated_lines=0` und
  `new_duplicated_lines_density=0.0` am unveränderten SonarCloud-Quality-Gate
  und keine neue task-eigene Annotation.
- Die Sonar-Remediation erhält dieselben Source-Isolation-, Mount-Topologie-,
  fail-closed-Decoder-, Cleanup- und legitimen External-Output-Controls.
- Erforderliche GitHub Actions und SonarCloud-Ergebnisse werden am selben
  Successor-Head beobachtet, bevor eine Ready-for-Review- oder geschützte
  Merge-Aktion stattfindet.

## Implementierungsentscheidung und Begründung

`_lock_tree` und beide Aufrufe auf den echten Source- und Framework-Roots sind
entfernt. Der Preparer validiert Topologie, Source-Links und Gitfiles, weist
strikte Source-Submounts ab, validiert die Identität, inventarisiert die
unveränderte Source, schreibt ein root-eigenes Inventory mit Modus `0600` in
den privaten Guard und erzeugt den dem Validator gehörenden mode-`0700`
`external`-Root. Der Namespace-Runner bleibt die tatsächliche Schreibgrenze:
private Mount-Propagation, ein nicht-rekursiver Source-Bind mit
Read-only-Remount und `nosuid,nodev`, privates Jail/Chroot/PID-Namespace,
geschlossene geerbte Deskriptoren, explizite Umgebung, Identity-Drop,
`PR_SET_NO_NEW_PRIVS` und Candidate-Probes bleiben erhalten. Er weist
verschachtelte Source-Mounts unabhängig ab.

Der Workflow erzeugt und exportiert den Guard mit festem Prefix
`$RUNNER_TEMP/modsecurity-readonly-validation.XXXXXX`, bevor Prepare scheitern
kann. Der Helper-Cleanup-Modus verlangt kanonische nicht-symlinkte Pfade, ein
exaktes direktes `RUNNER_TEMP`-Child mit diesem Prefix, disjunkte
Parent-/Framework-/Git-Pfade, root-owned Modus `0711` und keinen aktiven Mount.
Er öffnet Pfadkomponenten mit `O_NOFOLLOW` per Deskriptor und entfernt nur
deskriptor-relative Einträge.

Der Sonar-Follow-up dedupliziert das `source root`-Literal des Preparers,
schreibt den mountinfo-Decoder in eine äquivalente Split-and-Validate-Form um,
extrahiert das bestehende exakte Placeholder-Cleanup aus `run()` und ergänzt
Malformed-octal-Decoder-Coverage. Sein Test-Refactor teilt ausschließlich die
Fixture-Erzeugung und behält die bestehenden Source-Preservation-, Exception-
und External-Output-Assertions. Keine Scanner-Einstellung, kein Quality Gate,
keine Exclusion, Suppression oder Sandbox-Control wird geändert.

## Security-Auswirkung

Dies entfernt eine hochwirksame vertrauenswürdige Root-Mutation von Source- und
Git-Metadaten und erhält zugleich die Containment-Grenze für nicht
vertrauenswürdigen Framework-Candidate-Code. Es schwächt weder Candidate-
No-write-Probes, Root-seitige Inventory-Verifikation, External-Output-
Validierung, No-new-privileges, Capability-Checks, Publisher-Trennung,
Action-Pins, Repository-/Default-Branch-Guards noch Read-only-Job-Permissions.
Es fügt keine Netzwerk-Egress- oder Kernel-Exploit-Isolation hinzu.

Der enge Refactor wurde gegen versiegelten Patch SHA-256
`79074648aa1f204bcaeddd98a2c50cb62f92d2b2d01e22b98d1cb6b0ce2d9378`
als Security-Diff geprüft. Er erzeugte null reportable Findings. Der einzige
Cleanup-Pfad-Kandidat `NSR-001` wurde verworfen, weil
`_create_mount_layout()` bereits innerhalb von `run()`s `try/finally` liegt
und die injizierte Partial-Layout-Regression exaktes Cleanup beweist.

## Geänderte Dateien

- `ci/tools/prepare-readonly-submodule-validation-sandbox.py`
- `ci/tools/run-readonly-submodule-validation-namespace.py`
- `.github/workflows/update-submodules.yml`
- `tests/test_prepare_readonly_submodule_validation_sandbox.py`
- `tests/test_run_readonly_submodule_validation_namespace.py`
- `tests/test_ci_security_workflows.py`
- `docs/build/README.md` und `docs/build/README.de.md`
- dieses Change-Record-Paar und der gepaarte Archivindex
- Parent-lokales Finding `FND-PARENT-0184` sowie task-lokale Evidence-/Plan-Records

Der Sonar-Follow-up ändert nur die beiden Python-Helper, die beiden
fokussierten Testmodule und dieses gekoppelte Change-Record-Paar.
Reader-facing Build-Dokumentation bleibt unverändert, weil sich das
dokumentierte Verhalten und der Sicherheitsvertrag der Sandbox nicht ändern.

Dieser Record autorisiert keine Framework- oder MRTS-Source, keinen Gitlink,
keinen Product-Source, Commit, Push, Pull Request oder Merge.

## Ausgeführte Befehle

- Die reine Pre-fix-Fixture-Reproduktion zeichnete eine Modusmutation von
  `0664` zu `0644` durch den alten `_lock_tree`-Pfad auf; kein echter Checkout
  wurde berührt.
- `python3 -m py_compile` für die geänderten Helper und fokussierten Tests
  bestand.
- `python3 -m unittest tests.test_prepare_readonly_submodule_validation_sandbox`
  bestand: 25 Tests, 2 erwartete Capability-/Identity-Skips. Er enthält
  vollständige Metadaten-Snapshots nach Prepare, injizierte Namespace-Setup-
  und Candidate-Result-Fehler, Verify und Cleanup.
- `python3 -m unittest tests.test_run_readonly_submodule_validation_namespace`
  bestand: 35 Tests, 3 erwartete Namespace-Capability-Skips einschließlich
  Cleanup nach einem Partial-Mount-Layout-Erzeugungsfehler.
- Eine dedizierte Virtual Environment unter dem registrierten externen Task-
  Root installierte hash-locked `PyYAML==6.0.3`; ihr Lauf
  `python -m unittest tests.test_ci_security_workflows` bestand: 28 Tests.
- `make check-ci-security-contract` bestand: 122 Tests, 5 erwartete Skips,
  danach hash-gelockte actionlint-/zizmor-/gitleaks-Validierung.
- Exaktes gepinntes `actionlint .github/workflows/update-submodules.yml`,
  `make check-doc-links`, gezielte gepaarte Dokument-Struktur-/Link-Checks und
  `git diff --check` bestanden jeweils.
- `python3 -m unittest discover -q` endete mit Exit `5` nach `Ran 0 tests`;
  der Standardaufruf dieses Repositories entdeckt das `tests`-Package nicht.
- `make lint` und `make quick-check` endeten jeweils mit Exit `2` an denselben
  fünf unabhängigen HAProxy-Cache-Tests, die alle durch `CRS_REPO_URL override
  is not permitted` blockiert wurden, bevor der Candidate-Pfad dieser Sandbox
  ausgeführt wurde.
- Nach byteidentischer Recovery des Sonar-Patches bestand
  `PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python
  -m unittest -v tests.test_prepare_readonly_submodule_validation_sandbox`:
  25 Tests, 2 erwartete Skips; der äquivalente Namespace-Befehl bestand: 35
  Tests, 3 erwartete Skips. `make check-ci-security-contract` bestand danach:
  122 Tests, 5 erwartete Skips. `git diff --check` bestand.

## Runtime-Evidence

Die reine Fixture-Pre-fix-Reproduktion ist unter
`/var/tmp/codex/ModSecurity-conector/runs/readonly-submodule-sandbox-preservation-20260819/evidence/pre-fix-lock-tree-reproduction.json`
mit SHA-256
`8b83a574f71d29300d627fb2d2a8c672e1c9b3501d6f4f4afeaf3100fca7ec49`
aufbewahrt. Die aktuelle Umgebung mappt nur UID/GID 0; deshalb beobachtete die
Reproduktion direkt die alte Modusmutation, kann aber nicht zeigen, dass eine
Nicht-root-UID zu UID 0 wird. Der neue privilegierte Prepare/Candidate/Verify-
Integrationstest existiert und skippt fail-closed, wenn Kernel oder User-
Namespace die dedizierte Identität nicht mappen oder das erforderliche
Namespace nicht erstellen können.

Für diese Änderung wird kein erfolgreicher Hosted Run behauptet. Ein direkter
gemappter User-/Mount-/PID-Namespace-Probe endete mit Exit `1` und
`Operation not permitted`.

Der versiegelte Working-Tree-Security-Diff-Report ist
`/var/tmp/codex/ModSecurity-conector/20260819T145000Z-sonar-duplication-security-diff/report.md`
(SHA-256 `761396a57c0182b0b2c4778fdcf4ba08f6514b9039d73d38f31d404f261445c4`).
Er deckt alle vier geänderten Pfade ab und hat null reportable Findings. Der
geprüfte und der wiederhergestellte Patch haben die identische SHA-256
`79074648aa1f204bcaeddd98a2c50cb62f92d2b2d01e22b98d1cb6b0ce2d9378`.

## Nicht ausgeführte Prüfungen mit Begründung

- Die reale gemappte Non-root-Prepare/Candidate/Verify-Integration ist in
  diesem Container blockiert: Sowohl das `nobody`-Identity-Mapping als auch
  User-/Mount-/PID-Namespace-Erzeugung fehlen. Die Tests skippen, statt die
  Grenze zu schwächen.
- Der breite `make check-bilingual-docs`-Target wurde nach mehr als sieben
  Minuten ohne Ergebnis gestoppt, weil sein rekursiver Walk ignorierte
  Virtual-Environment-Inhalte vor Anwendung des Ignore-Filters betritt. Die
  geänderten Paare bestanden gezielte Struktur-, Identity- und lokale
  Link-Checks; Checker-Verhalten liegt außerhalb dieses Remediation-Scopes.
- Eine korrekt abgegrenzte Full-Discovery (`-s tests`) lief im gemeinsamen
  Checkout nicht, weil `FND-PARENT-0182` ein separates Checkout-Preservation-
  Risiko dokumentiert. Die angeforderte Default-Discovery wurde dennoch
  ausgeführt und oben festgehalten.
- Die erforderlichen GitHub Actions des vorherigen exakten PR-#302-Heads
  bestanden, aber sein SonarCloud-Check-Run `96097393398` scheiterte an
  `6.4% Duplication on New Code`. Der quellnative Successor ist noch nicht
  committed oder gepusht; daher sind SonarCloud, GitHub Actions, Review,
  Ready-for-Review und Merge-Evidence am Successor-Head noch nicht verfügbar.
  Die lokale gemappte Non-root-Namespace-Integration bleibt nicht verfügbar.

## Bekannte Einschränkungen

Der lokale Container darf möglicherweise kein vollständiges Mount/PID-Namespace
erzeugen oder die dedizierte `nobody`-Identität mappen; betroffene
Integrationstests skippen, statt die Grenze zu schwächen. Diese Reparatur ändert
keinen bereits root-eigenen Checkout automatisch. Benutzer müssen einen
konkreten Pfad prüfen und bei Bedarf außerhalb des Workflows bewusst manuell
reparieren.

## Verbleibende Risiken

Der Namespace ist eine begrenzte Dateisystem-/Prozess-Grenze und keine
vollständige Host-, Kernel- oder Netzwerk-Isolation. Cleanup führt initiale und
finale Active-Mount-Checks sowie deskriptor-relative Löschung aus; es setzt
voraus, dass der vertrauenswürdige Runner nicht gleichzeitig
angreiferkontrollierte Inhalte in den root-eigenen Guard mountet. Künftige
Änderungen müssen die statischen Verträge für Source-Preservation,
verschachtelte Mounts, private Pfade und No-Restore behalten.

Der gemeinsame Checkout wechselte unerwartet zu `master`, während der
Follow-up-Patch uncommitted war, und kehrte dann zum Task-Branch zurück. Der
Patch wurde byteidentisch wiederhergestellt und kein Akteur wird zugeschrieben;
`FND-PARENT-0182` hält diesen separaten Lifecycle-Defekt fest. Branch, Reflog,
Source-Scope und Patch-Identität müssen vor Staging oder Push erneut geprüft
werden.

## Finaler Diff- und Review-Status

Die lokale Sonar-Remediation ist abgeschlossen und geprüft: Sie hat keine
Whitespace-Fehler, der fokussierte Security-Review fand null reportable
Findings, die fokussierten Module bestanden nach der Recovery und
`make check-ci-security-contract` bestand. Sie ist noch nicht `verified`:
Es gibt keinen Successor-Commit/-Head und kein Hosted-SonarCloud-Ergebnis, der
gemappte Non-root-Namespace-Nachweis bleibt nicht verfügbar und der unabhängige
HAProxy-Blocker verhindert weiterhin einen grünen breiten Lint-/Quick-check-
Claim. Kein Ready-for-Review-, verified-PR- oder Merge-Ergebnis wird behauptet.
