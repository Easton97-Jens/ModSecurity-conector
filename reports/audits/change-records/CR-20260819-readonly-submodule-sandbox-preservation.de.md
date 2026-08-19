# Change Record: Source-Preservation der Read-only-Submodule-Sandbox

**Sprache:** [English](CR-20260819-readonly-submodule-sandbox-preservation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260819-readonly-submodule-sandbox-preservation |
| Datum (UTC) | 2026-08-19 |
| Basis-Revision | `35c435483dcd637c7b9df0277bed34d6f94dc44d` |
| Historischer Framework-Gitlink | `bd69ee96e0e7082317d4afe1232bee625665eb9a` |
| Delivery-Status | Der aktuelle Benutzer autorisierte ausdrücklich die Veröffentlichung eines Draft-PR aus dem aktuellen Checkout und akzeptierte/deferierte die fehlende Evidence für gemappten Non-root-Namespace/Hosted sowie die fünf unabhängigen HAProxy-Cache-Fixture-Fehler ausschließlich für diesen Draft-PR. Dieser Record behauptet noch keinen gepushten Commit, keine PR-Nummer, kein Hosted-Ergebnis, keinen Ready-for-Review-Status und keinen Merge. |

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

## Security-Auswirkung

Dies entfernt eine hochwirksame vertrauenswürdige Root-Mutation von Source- und
Git-Metadaten und erhält zugleich die Containment-Grenze für nicht
vertrauenswürdigen Framework-Candidate-Code. Es schwächt weder Candidate-
No-write-Probes, Root-seitige Inventory-Verifikation, External-Output-
Validierung, No-new-privileges, Capability-Checks, Publisher-Trennung,
Action-Pins, Repository-/Default-Branch-Guards noch Read-only-Job-Permissions.
Es fügt keine Netzwerk-Egress- oder Kernel-Exploit-Isolation hinzu.

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
  bestand: 34 Tests, 3 erwartete Namespace-Capability-Skips einschließlich
  Cleanup nach einem Partial-Mount-Layout-Erzeugungsfehler.
- Eine dedizierte Virtual Environment unter dem registrierten externen Task-
  Root installierte hash-locked `PyYAML==6.0.3`; ihr Lauf
  `python -m unittest tests.test_ci_security_workflows` bestand: 28 Tests.
- `make check-ci-security-contract` bestand: 121 Tests, 5 erwartete Skips,
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
- Hosted `validate_only`, Security-Scan, Pull-Request-Checks, SonarQube und
  Review sind noch nicht ausgeführt. Die Veröffentlichung eines Draft-PR ist
  jetzt mit der im Delivery-Status genannten begrenzten Risikoannahme
  ausdrücklich autorisiert; weder Ready-for-Review noch Merge sind autorisiert.

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

## Finaler Diff- und Review-Status

Der finale lokale Review ist abgeschlossen: Source-Locking ist entfernt, das
private Guard-Cleanup behandelt partielles Namespace-Setup, fokussierte
Regression-/Security-Contracts und Dokumentationsprüfungen bestehen, und der
finale Diff enthält keine Whitespace-Fehler. Das Finding bleibt lokal `fixed`,
nicht `verified` oder closed, weil gemappte Non-root-Namespace- und Hosted-
Exact-Head-Evidence weiterhin fehlen/noch nicht beobachtet wurden; der
unabhängige HAProxy-Testblocker verhindert außerdem einen grünen breiten
Lint-/Quick-check-Claim. Der aktuelle Benutzer akzeptierte/deferierte diese
exakten Lücken ausschließlich, um die Veröffentlichung eines Draft-PR aus dem
aktuellen Checkout zu erlauben. Dieser Record behauptet bewusst kein
Hosted-CI-, PR-Nummer-, Ready-for-Review- oder Merge-Ergebnis.
