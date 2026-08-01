# FND-FRAMEWORK-0036 — Frische ModSecurity-v3-Bereitstellung honoriert lokale Git-Worktree- und Attribute-Konfiguration vor der Provenance-Validierung

## Identität

- Kategorie: `security_validated`
- Repository / Ownership: `framework` / `framework`
- Priorität / Schweregrad / Konfidenz: `P0` / `high` / `validated`
- Status / Machbarkeit: `verified` / `feasible_now`
- Release-Blocker / sicherheitsrelevant: `true` / `true`
- Betroffene Revision: `f98a8739cb13b583f23d646784b144e596b61441` (historisch validiert auf `784977615acfc55567e37b863309abc4a38ac877`)
- Parent-Auswirkung: blockiert die legitime Runtime-Evidence-Voraussetzung für Parent PR #55; keine Parent-Gitlink-Änderung ist autorisiert.
- MRTS-Auswirkung: keine; MRTS bleibt strikt read-only.

## Zusammenfassung, Invariante und Auswirkung

## Aktuelle Master-Verifikation vom 2026-07-26

Die Wiedereröffnungs-Evidence zum f98-basierten Candidate ist historisch.
Framework-PR #44 führte das geprüfte Fresh-Root-Containment und lokale
Config-Scrubbing ein; es ist auf dem aktuellen Master
`47e50e7bc43ba7a3b5bad1a9448111794f664cc0` vorhanden. Die
Current-Master-Suite bestand Real-Git-Worktree-Redirect-, Attributes/Filter-,
Recursive-Update-, Fake-PATH- und saubere legitime Controls zusammen mit
`make test-modsecurity-v3-provenance-contract` und `make lint`. Diese
Verifikation änderte weder Parent-Gitlink noch MRTS-Status.

Nachdem `git init` `MODSECURITY_V3_SOURCE_DIR/.git` erstellt, kann ein
konkurrierender Akteur dessen lokale Konfiguration vor dem frischen gepinnten
Checkout verändern. Der Kandidat ruft `ci_modsecurity_v3_git -C <source>
checkout --detach <approved commit>` vor seinem ersten physischen Worktree- /
Provenance-Guard auf. Der generische Wrapper entfernt geerbte, globale und
System-Konfiguration, honoriert jedoch die neu geschriebene lokale
Konfiguration.

Die Invariante lautet, dass kein frischer Checkout vor der Provenance-
Validierung außerhalb seines vorgesehenen Source-Verzeichnisses schreiben oder
einen Attribute-Filter ausführen darf. Eine task-eigene Actual-Wrapper-Fixture
belegte, dass `core.worktree=<external>` den Checkout mit `0` beendete und
`payload.txt` nur extern schrieb; erst der spätere Guard gab `77` zurück. Eine
zweite Fixture belegte, dass `core.attributesfile` zusammen mit
`filter.evil.smudge` einen harmlosen Marker vor der Validierung erzeugte. Eine
saubere Kontrolle schrieb die Payload nur unter das vorgesehene
Source-Verzeichnis.

Ein Akteur, der sich eine frische Source-Root teilt, kann Checkout-Output
umleiten oder einen lokalen Filter mit der Framework-/CI-Identität ausführen.
Dies ist eine Supply-Chain-Provisioner-Kompromittierung mit hoher Auswirkung;
der Nachweis verwendet nur temporäre lokale Git-Objekte, harmlose Payloads und
einen Marker und greift nicht auf Parent-, autoritative Framework- oder MRTS-
Quellen zu.

Die frühere lokale Remediation ist nur historisch. Am `2026-07-23` stellte ein
unabhängiges statisches Review des isolierten Candidates auf Framework-master
`f98a8739cb13b583f23d646784b144e596b61441` fest, dass dessen frische Route
wieder den generischen Wrapper für Remote-Add, Fetch, Checkout und rekursive
Initialisierung nutzt. Der erforderliche dedizierte Fresh-Root-Helper, die
explizite `--git-dir`/`--work-tree`-Bindung,
`core.attributesfile=/dev/null`, `core.sparseCheckout=false` und unmittelbares
lokales Recursive-Update-Scrubbing fehlen. Die validierte Klasse mit hoher
Auswirkung ist deshalb wieder `in_progress`; die Wiedereröffnung ist statische
Evidence, kein Ersatz für einen frischen dynamischen Rerun.

## Betroffener Pfad, Source-to-Sink und Reproduktion

- `ci/provisioning/fetch-smoke-sources.sh` —
  `provision_fresh_modsecurity_v3` initialisiert Git und checkt vor seinem
  Root-Guard aus.
- `ci/lib/common.sh` — `ci_modsecurity_v3_git`.
- `tests/security_regression/test_modsecurity_v3_git_ref_provenance.py` —
  erforderliche Real-Git-Regressionen.

Setze lokal `core.worktree=<external>` nach `git init`, führe dann den
Actual-Candidate-Checkout aus: Der gepinnte Checkout besteht, schreibt aber
nur extern. Alternativ setze `core.attributesfile=<attacker attributes>` und
`filter.evil.smudge=<benign marker script>`: Checkout besteht und erzeugt den
Marker bevor ein Guard läuft. Eine saubere Same-Boundary-Kontrolle besteht
sicher.

## Retained Evidence

- Run-ID: `20260720T173133Z-pr55-runtime-remediation-7e38e876`
- Artefakt:
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T173133Z-pr55-runtime-remediation-7e38e876/evidence/framework-fresh-checkout-config-race-validation.md`
- Typ: `task_owned_real_git_fresh_checkout_config_race_validation`
- SHA-256: `af927b36a6221b831c47446f15aa0ce25258dff1bad5325f933f686aa896eb81`
- Befehl: RTK-umhüllte task-eigene `invoke-wrapper.sh`-Experimente für
  Worktree, Attributes/Filter, saubere Kontrolle und contained Checkout
- Working Directory: `/root/git/ModSecurity-conector`
- Exit-Code / beobachtet: `0` / `2026-07-20T19:59:28Z`
- Retention: `retained_task_evidence`

Post-Fix-retained Evidence:

- Run-ID: `20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607`
- Artefakt:
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607/evidence/framework-modsecurity-v3-provenance-remediation-postfix.md`
- Typ: `framework_postfix_security_validation_report`
- SHA-256: `b20ccffd871b9e4d821f5bdf08bb98061a0d7e6ed41a8921551b8fa2ec542aec`
- Befehl: RTK-umhüllte fokussierte Provenance-Suite, Real-Git-Kontrolle für
  benutzerdefiniertes Submodule-Update, Framework-Make-Provenance-Contract,
  Dokumentations-Checks und vollständiger Framework-Lint
- Working Directory:
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T173133Z-pr55-runtime-remediation-7e38e876/tmp/framework-worktree`
- Exit-Code / beobachtet: `0` / `2026-07-20T21:07:10Z`
- Retention: `retained_task_evidence`

Aktuelle Wiedereröffnungs-Evidence:

- Run-ID: `20260723T162517Z-fnd-cross-0001-runtime-evidence-bcda7d1d`
- Candidate `ci/lib/common.sh`:
  `/var/tmp/codex/ModSecurity-conector/runs/20260723T162517Z-fnd-cross-0001-runtime-evidence-bcda7d1d/tmp/parent/modules/ModSecurity-test-Framework/ci/lib/common.sh`
  - Typ: `isolated_f98_based_framework_candidate_static_fresh_root_common_review`
  - SHA-256: `46744e1ad7f1b6dd4817984586985b6841085589d307b86fe963aed12c57ca62`
- Candidate `ci/provisioning/fetch-smoke-sources.sh`:
  `/var/tmp/codex/ModSecurity-conector/runs/20260723T162517Z-fnd-cross-0001-runtime-evidence-bcda7d1d/tmp/parent/modules/ModSecurity-test-Framework/ci/provisioning/fetch-smoke-sources.sh`
  - Typ: `isolated_f98_based_framework_candidate_static_fresh_root_fetch_review`
  - SHA-256: `97f3026f1958f0af08de69f90458e3236e310f7d140bd825cccae185dd476a19`
- Die RTK-umhüllte Diff-/Kontext-/Hash-Inspektion endete `0` um
  `2026-07-23T17:31:41Z`. Sie fand nur generische Wrapper-Aufrufe und keine
  erforderlichen Fresh-Root-Containment-/Scrubbing-Controls.

## Remediation, Validierung und Restrisiko

Der korrigierte Candidate muss vor Git eine private Source-Root etablieren und
für jeden frischen Remote-Add-, Fetch-, Checkout- und rekursiven Submodule-
Befehl einen dedizierten Fresh-Root-Checkout-/Acquisition-Helper wiederherstellen.
Er muss `--git-dir=<source>/.git`, `--work-tree=<source>`,
`-c core.attributesfile=/dev/null` und `-c core.sparseCheckout=false` nutzen
und lokale `core.worktree`, `core.attributesfile`, `core.sparseCheckout` sowie
jeden lokalen `submodule.*.update`-Key unmittelbar vor den jeweiligen Git-
Befehlen löschen. Allein `-c core.worktree=<source>` bleibt unzureichend, weil
das kontrollierte Experiment Checkout-Output weiterhin umleitete.

Die aufbewahrten Real-Git-Regressionen decken Worktree-Redirect,
Attribute-/Filter-Ausführung, einen öffentlichen vor Git abgewiesenen
Source-Parent, einen benutzerdefinierten `submodule.*.update`-Marker, der
niemals läuft während das legitime Child initialisiert, sowie die saubere
Kontrolle ab. Die historische fokussierte Suite (24 Tests), der
Framework-Make-Provenance-Contract (24 Tests), der CI-Bootstrap-Contract
(6 Tests), Dokumentations-/Change-Record-Checks und vollständiger
Framework-Lint bestanden nur für den früheren lokalen Candidate. Sie
validieren den aktuellen f98-basierten Patch nicht; dieselben Tests plus
unabhängiges Bypass-Review müssen auf dessen korrigiertem exakten Head erneut
laufen.

Dieses Finding ist `in_progress`, nicht `fixed` oder `verified`: Ein
korrigierter Framework-PR, dynamische Exact-Head-Checks/Review/Sonar-Evidence,
Framework-master-Verifikation und ein separat autorisiertes Parent-Gitlink-
Update bleiben erforderlich, bevor Parent-PR-#55-Runtime-Evidence fortfahren
kann. Portable pfadbasierte Shell-Kontrollen können einen konkurrierenden
Schreiber mit derselben UID nicht isolieren; worktree-scoped oder included
lokale Konfiguration bleibt daher ein Same-UID-Hardening-Kandidat und keine
bestätigte Isolationsaussage. Der Befund bleibt verschieden von
`FND-FRAMEWORK-0032` (Inspection-Konfiguration), `FND-FRAMEWORK-0034`
(veränderbare Source-Bytes), `FND-FRAMEWORK-0035`
(Materialization-Output-Containment) und dem getrennten Host-Git-PATH-
Kandidaten `FND-FRAMEWORK-0054`.

## Verwandte Findings und Verlauf

- Verwandt: `FND-FRAMEWORK-0030`, `FND-FRAMEWORK-0032`,
  `FND-FRAMEWORK-0034`, `FND-FRAMEWORK-0035` und `FND-CROSS-0001`.
- `2026-07-20T19:59:28Z`: dynamisch in einer task-eigenen Actual-Wrapper-
  Fixture validiert; Kandidat-Delivery pausiert.
- `2026-07-20T21:20:47Z`: private Source-Parent-Validierung, explizites Fresh-
  Checkout-Containment und rekursives Local-Config-Scrubbing bestanden die
  Worktree-, Attributes/Filter-, Custom-Update-, Clean-Control-, Make-, Lint-,
  Dokumentations- und unabhängigen Review-Kontrollen auf dem damals geprüften
  lokalen Candidate; dies ist historische lokale Evidence.
- `2026-07-23T17:31:41Z`: Unabhängiges Review und statische Inspektion des
  isolierten f98-basierten Candidates fanden keinen dedizierten Fresh-Root-
  Helper und keine erforderlichen Containment-/Scrubbing-Optionen vor den
  generischen Git-Aufrufen. Das validierte P0/high-Finding ist bis zu einem
  korrigierten Candidate und frischen dynamischen Controls wieder
  `in_progress`; diese Tracking-Aktualisierung änderte keinen Produkt-Source,
  keinen Framework-Branch/PR, keinen Parent-Gitlink und keinen MRTS-Zustand.
