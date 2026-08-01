# FND-FRAMEWORK-0032 — ModSecurity-v3-Provenance-Validator führt lokale Git-fsmonitor-Konfiguration aus und schreibt während der behaupteten schreibgeschützten Validierung

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-FRAMEWORK-0032 |
| Kategorie | security_validated |
| Repository / Ownership | framework / framework |
| Priorität / Severity | P0 / high |
| Konfidenz / Status | validated / fixed |
| Feasibility | feasible_now |
| Release-Blocker | ja |
| Sicherheitsrelevant | ja |

## Zusammenfassung und Verhalten

Der Framework-Kandidat akzeptiert einen vom Aufrufer gelieferten vorhandenen
MODSECURITY_V3_SOURCE_DIR und ruft über ci_modsecurity_v3_git für Root und
jedes freigegebene Child git status auf. Vor dieser Remediation bereinigte der
Wrapper geerbte/globale Konfiguration, überschieb aber weder lokales
core.fsmonitor noch deaktivierte er optionale Git-Locks. Ein privater
Real-Git-Control mit einer harmlosen, Marker schreibenden lokalen
core.fsmonitor-Probe führte die Probe bei einfachem git status aus; mit
git --no-optional-locks -c core.fsmonitor=false führte er sie nicht aus.

Ein zweiter privater Real-Git-Control setzte lokales core.worktree auf einem
nicht vertrauenswürdigen Checkout. git -C <untrusted> rev-parse
--show-toplevel löste dann auf ein anderes physisches Verzeichnis auf. Vor der
Kandidatenkorrektur verlangte der fokussierte Framework-Test fail-closed Exit
77, erhielt aber 0.

Die Validierung darf weder repositorygesteuerte Git-Konfiguration ausführen
noch Git-Metadaten schreiben und muss jeden aufgelösten Root-/Child-Worktree an
das physisch geprüfte Verzeichnis binden. Zusätzliche Remotes, angeheftete
symbolische Heads, externe Child-Git-Verzeichnisse, Topologieabweichungen oder
Pfad-Escapes müssen vor einer Build-Aktion fail-closed fehlschlagen.

## Betroffener Pfad, Voraussetzungen und Auswirkung

Betroffene Symbole sind ci_modsecurity_v3_git,
ci_modsecurity_v3_require_clean_checkout,
ci_require_approved_modsecurity_v3_root_checkout und
ci_require_approved_modsecurity_v3_checkout in ci/lib/common.sh. Apache-,
NGINX- und direkte-v3-Build-Pfade rufen diesen Guard auf einem vorhandenen
Source-Checkout vor der Source-Nutzung auf.

Ein Angreifer benötigt die Möglichkeit, .git/config des akzeptierten
Source-Checkouts oder ein externes Child-Git-Verzeichnis vorzubelegen. Der
git-status-Sink kann dann vor der Provenance-Entscheidung einen vom Angreifer
gewählten fsmonitor-Befehl mit der Framework-Build-/CI-Identität ausführen.
Worktree-/Konfigurationsumleitung kann geprüfte Origin, HEAD und Status auf
einen anderen Baum beziehen. Dies ist ein P0/high-Supply-Chain-Grenzfehler. Der
kontrollierte Nachweis nutzte keine Parent-, autoritative Framework- oder
MRTS-Checkout.

## Evidenz und Reproduktion

Zurückgehaltene Pre-Fix-Evidenz:

- Run-ID: 20260720T173133Z-pr55-runtime-remediation-7e38e876
- Artefakt: /var/tmp/codex/ModSecurity-conector/runs/20260720T173133Z-pr55-runtime-remediation-7e38e876/evidence/framework-modsecurity-v3-git-validator-pre-fix-security-reproduction.md
- SHA-256: 805dcc95732c9f029194240fcab79b397ec21af1cbc1da0bd5bd768dbc23d716
- Befehl: RTK-wrapped private Git core.worktree and core.fsmonitor probes plus focused Framework pre-fix regression
- Arbeitsverzeichnis: /root/git/ModSecurity-conector
- Exit-Code: 0
- Beobachtet am: 2026-07-20T18:36:32Z
- Aufbewahrung: retained_task_evidence

Post-Fix-retained Evidence:

- Run-ID: `20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607`
- Artefakt: `/var/tmp/codex/ModSecurity-conector/runs/20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607/evidence/framework-modsecurity-v3-provenance-remediation-postfix.md`
- Typ: `framework_postfix_security_validation_report`
- SHA-256: `b20ccffd871b9e4d821f5bdf08bb98061a0d7e6ed41a8921551b8fa2ec542aec`
- Befehl: RTK-umhüllte fokussierte Provenance-Suite, Real-Git-
  fsmonitor/worktree/custom-submodule-update-Controls, Framework-Make-
  Provenance-Contract, Dokumentations-Checks und vollständiger Framework-Lint
- Working Directory:
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T173133Z-pr55-runtime-remediation-7e38e876/tmp/framework-worktree`
- Exit-Code / beobachtet: `0` / `2026-07-20T21:07:10Z`
- Retention: `retained_task_evidence`

Sicher nur mit einer task-eigenen harmlosen Marker-Probe reproduzieren:

1. Lokales core.fsmonitor in einem temporären Repository konfigurieren und
   einfaches git status --porcelain=v1 ausführen; den Marker beobachten.
2. Mit git --no-optional-locks -c core.fsmonitor=false wiederholen; der Marker
   darf nicht existieren.
3. core.worktree auf ein anderes temporäres Verzeichnis konfigurieren und die
   rev-parse --show-toplevel-Umleitung beobachten.
4. Den fokussierten Pre-Fix-Worktree-Redirection-Test ausführen; er scheitert,
   weil der Guard 0 statt 77 zurückgibt.

## Ursache und Remediation

Der gehärtete Wrapper vertraute lokaler Git-Konfiguration für Status,
deaktivierte fsmonitor oder optionale Locks nicht und band weder Git-Worktree
noch Child-gitdir an die physische Source-Grenze. Der lokale Candidate nutzt
jetzt `--no-optional-locks`, `core.fsmonitor=false`,
`core.hooksPath=/dev/null`, deaktiviert den eingebauten fsmonitor, verweigert
File-Transport, bindet jeden Root-/Child-Worktree und jedes Child-gitdir,
fordert genau ein `origin` und detached HEADs und weist unsichere Source-
Parents vor Git ab. Unmittelbar vor rekursiven Git-Befehlen löscht er lokale
`core.worktree`, `core.attributesfile`, `core.sparseCheckout` und jeden
lokalen `submodule.*.update`-Key.

Er bewahrt File-Transport-Sperre, TLS-Verifikation, Hook-Path-Härtung, exakte
Root-/Child-Commits und Origins, statische Acht-Child-Topologie und bewusste
rekursive Initialisierung erst nach Root-Validierung. Real-Git-
fsmonitor/worktree/custom-update-, Public-Parent-, Clean-Control-, Topologie-,
Make-, Dokumentations-, Change-Record- und vollständige-Lint-Controls
bestanden. Das unabhängige Review fand keinen verbleibenden High- oder
Critical-Blocker für das dokumentierte Cross-UID-Lokal-Angreifer-Modell.

## Akzeptanzkriterien und Validierung

1. Jeder Provenance-Git-Aufruf deaktiviert core.fsmonitor und optionale Locks.
2. Kanonischer Root-/Child-Worktree sowie Child-gitdir-Containment sind
   erzwungen.
3. Extra-Remote, angehefteter Head, externes gitdir, Worktree-Redirection,
   dirty-, uninitialized-, symlinked-, missing/extra-, Origin- und
   Commit-Varianten schlagen vor Source-Nutzung fehl.
4. Der saubere freigegebene Acht-Child-Control und der frische gepinnte
   Provisioner bestehen.
5. Ein Real-Guard-Aufruf auf der zurückgehaltenen freigegebenen Source hat
   unveränderte ausgewählte Git-Metadaten-Hashes vor/nach dem Aufruf;
   fokussierte Tests, Make-Contract, Syntax, Dokumentation, Change Record,
   Lint und finaler Security-Review bestehen.

Regression-Dateien: tests/security_regression/test_modsecurity_v3_git_ref_provenance.py
und tests/security_regression/git_provenance_test_support.py. Zuständiger
Target: make test-modsecurity-v3-provenance-contract.

## Abhängigkeiten, Restrisiko und Historie

Dieses Finding hängt von derselben Framework-only-Topologie-Remediation wie
FND-FRAMEWORK-0030 ab und ist verwandt mit FND-CROSS-0001. Es ist kein Duplikat
der Availability-False-Rejection von FND-FRAMEWORK-0030 oder des
YAML-Action-Pin-Bypasses von FND-FRAMEWORK-0031. Parent-Gitlink und MRTS bleiben
unverändert.

Dieses Finding ist `fixed`, nicht `verified`: Ein separater Framework-PR,
Exact-Head-Checks/Review/Sonar-Evidence, Framework-master-Verifikation und ein
separat autorisiertes Parent-Gitlink-Update bleiben erforderlich, bevor es
Parent-PR-#55-Runtime-Evidence entblocken kann. Portable pfadbasierte Shell-
Kontrollen können einen konkurrierenden Schreiber mit derselben UID nicht
isolieren; worktree-scoped oder included lokale Konfiguration bleibt ein
Same-UID-Hardening-Kandidat. Es erfolgten kein Framework-master, Parent-
Gitlink oder MRTS-Aktion.

- 2026-07-20T18:36:32Z — task-eigene Real-Git-Controls validierten lokale
  fsmonitor-Ausführung, sichere Command-Line-Unterdrückung, core.worktree
  Redirection und die anfängliche fail-open-Kandidatenregression.
- 2026-07-20T18:36:32Z — das getrennte P0/high-Framework-Finding wurde
  angelegt und die Remediation ohne Delivery-Aktion begonnen.
- 2026-07-20T21:20:47Z — gehärtete Git-Aufrufe, Root-/Child-Worktree- und
  gitdir-Containment, Private-Parent-Validierung und rekursives Local-Config-
  Scrubbing bestanden fsmonitor-, worktree-, custom-update-, clean-control-,
  Make-, Lint-, Dokumentations- und unabhängige Review-Controls. Status ist
  `fixed`, nicht `verified`, bis separater Framework-PR und Master-
  Verifikation vorliegen.
