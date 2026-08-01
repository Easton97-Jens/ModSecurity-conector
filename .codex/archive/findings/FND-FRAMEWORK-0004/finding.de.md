# FND-FRAMEWORK-0004 — Mutable Git-Source-Referenzen können Framework-Provisioning-Consumption erreichen

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-FRAMEWORK-0004` |
| Kategorie | `security_validated` |
| Repository / Ownership | `framework` / `framework` |
| Priorität / Severity / Confidence | `P2` / `medium` / `validated` |
| Status | `verified` |
| Release-Blocker / Security-Relevanz | `false` / `true` |
| Final Disposition | `verified_on_framework_master_not_closed` |

## Zusammenfassung

Die Framework-Provisionierung bindet die CRS-Consumption nun an den zentral
freigegebenen literalen HTTPS-Origin und den geprüften kleingeschriebenen
40-Zeichen-Commit. Mutable Aufruferselektoren können keine CRS-Inhalte auswählen,
und Fetch-, Auflösungs- und Checkout-Identitäten werden vor der Consumption
verifiziert.

## Beobachtetes und erwartetes Verhalten

Vor der Remediation konnte `CRS_GIT_REF=main` einen Git-Quellref-Selektor
erreichen. Der aktuelle Master-Tree lehnt abweichende `CRS_REPO_URL`- und
`CRS_GIT_REF`-Werte vor Git ab; ein frisches Repository fetcht nur den
freigegebenen Vollcommit und verifiziert `FETCH_HEAD`, aufgelöstes Objekt und
finales `HEAD`.

Die CRS-Provisionierung darf nur den zentral freigegebenen literalen HTTPS-Origin
und kleingeschriebenen 40-Zeichen-unveränderlichen Commit konsumieren. Das
Release-Label ist Metadatum und niemals Git-Inhaltsselektor. Bestehende
Quellpfade, Origin-Mismatch, Identitäts-Mismatch und `.gitmodules`-Deklarationen
schlagen sicher fehl.

## Auswirkung

Die verifizierte Grenze verhindert, dass aufruferkontrollierte Selektoren,
mutable Tags oder Branches und Ref-Namespace-Schreibweisen den von
Framework-Provisionierung und Regelvorbereitung konsumierten CRS-Quellbaum
auswählen.

## Betroffene Dateien und Symbole

- `modules/ModSecurity-test-Framework/ci/lib/common.sh`
- `modules/ModSecurity-test-Framework/ci/provisioning/fetch-crs.sh`
- `modules/ModSecurity-test-Framework/tests/security_regression/test_crs_git_ref_provenance.py`
- `modules/ModSecurity-test-Framework/docs/reference/variables.md`
- `modules/ModSecurity-test-Framework/docs/reference/variables.de.md`
- `modules/ModSecurity-test-Framework/docs/testing-and-evidence.md`
- `modules/ModSecurity-test-Framework/docs/testing-and-evidence.de.md`
- `modules/ModSecurity-test-Framework/reports/audits/change-records/20260718-01-fix-framework-crs-ref-provenance.md`
- `modules/ModSecurity-test-Framework/reports/audits/change-records/20260718-01-fix-framework-crs-ref-provenance.de.md`

Symbole: `F-DISC-01-02`, `CRS_APPROVED_REPO_URL`, `CRS_APPROVED_COMMIT`,
`CRS_RELEASE_TAG`, `ci_require_full_git_commit`,
`require_approved_crs_provenance`, `crs_git` und `provision_fresh_crs`.

## Voraussetzungen und Reproduktion

- Aufbewahrte Assessment-, Local-Revalidation- und PR-#26-Master-
  Verification-Evidence bleiben verfügbar.
- Finaler PR-#26-Head: `465766c01e2bb0a9a003cfcefa8afca5fceeafe0`; aktueller
  Framework-Master: `36cac3029c735dddf9f717b3ce077b9285567a6a`.
- Post-Merge-Validation-Worktree:
  `/var/tmp/codex/ModSecurity-test-Framework/worktrees/fw-crs-ref-provenance`.
- Parent-Gitlink und MRTS bleiben außerhalb dieser Framework-only-Delivery.

Das ursprüngliche aufbewahrte Assessment steht in
`.codex/reports/repository-full-assessment.md:221-227,238-244`. Die aktuelle
negative Reproduktion führt `CRS_GIT_REF=main` durch die prozessgrenzenbasierte
Fake-Git-Fixture und liefert `77` vor Git-Nutzung. Der fokussierte Master-Check
lautete:

```text
rtk env BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/runs/20260719T081017Z-framework-pr-resolution-20260719-840082e0/tmp/pr26-master-lint-build PYTHONPYCACHEPREFIX=/var/tmp/codex/ModSecurity-conector/runs/20260719T081017Z-framework-pr-resolution-20260719-840082e0/tmp/pr26-master-lint-build/pycache python3 -m unittest discover -s tests/security_regression -p test_crs_git_ref_provenance.py -v
```

## Evidence

1. `20260716T193351Z-repository-full-assessment-0cb855ad` —
   `.codex/reports/repository-full-assessment.md:221-227,238-244`; Typ
   `bilingual_assessment_report`; SHA-256
   `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`;
   `sed -n '221,227p;238,244p' .codex/reports/repository-full-assessment.md`;
   `/root/git/ModSecurity-conector`; Exit `0`; beobachtet
   `2026-07-16T22:46:50Z`; `retained_local_report`.
2. `20260718T092708Z-fnd-framework-0004-crs-ref-provenance-05f04893` —
   `/var/tmp/codex/ModSecurity-conector/runs/20260718T092708Z-fnd-framework-0004-crs-ref-provenance-05f04893/evidence/fnd-framework-0004-local-validation.md`;
   Typ `framework_security_revalidation_and_delivery_evidence`; SHA-256
   `cc8e2a5292c47b416482acaaf8e6c1e5336b90ba6aa9e2e7d791c2fd3ab20757`;
   fokussierte Provenance-Regression, Exact-Head-Draft-PR-CI, SonarCloud und
   Security-Revalidation; obiger Worktree; Exit `0`; beobachtet
   `2026-07-18T10:41:10Z`; `retained_local_evidence`.
3. `20260719T081017Z-framework-pr-resolution-20260719-840082e0` —
   `/var/tmp/codex/ModSecurity-conector/runs/20260719T081017Z-framework-pr-resolution-20260719-840082e0/evidence/fnd-framework-0004-pr26-master-verification.md`;
   Typ `framework_pr26_master_verification_receipt`; SHA-256
   `d64b00219a95d4cbdb550d4af2abc5c9b248cb493796c3cd84301674f6f76f9a`;
   Exact-Head-/Master-Verifikation, Tree-/Diff-/MRTS-Vergleich, fokussierte
   CRS-Checks, Dokumentations-Check und Lint; obiger Worktree; Exit `0`;
   beobachtet `2026-07-19T15:00:59Z`; `retained_local_evidence`.

## Grundursache und Remediation

Der CRS-Provisioning-Pfad akzeptierte das mutable `CRS_GIT_REF`-Release-Tag als
Git-Quellselektor und checkte `FETCH_HEAD` aus, ohne die Consumption an eine
geprüfte unveränderliche Commit-Identität zu binden.

Die Remediation zentralisiert freigegebenen Origin, Release-Metadaten und
Vollcommit-Konstanten; lehnt abweichende Selektoren vor Git ab; validiert den
Vollcommit; verwendet einen isolierten Git-Aufruf und einen frischen Quellpfad;
fetcht nur den literalen Commit; vergleicht `FETCH_HEAD`, aufgelöstes Objekt und
`HEAD`; und schlägt für `.gitmodules` sicher fehl.

## Akzeptanzkriterien und Validierung

- Die Provisionierung verwendet nur den literalen freigegebenen HTTPS-Origin und
  den kleingeschriebenen 40-Zeichen-Vollcommit.
- Tags, Branches, Ref-Namespaces, abgekürzte Hashes, abweichende
  Umgebungsselektoren, geerbte Git-Kontrollen, bestehende Quellpfade und
  `.gitmodules`-Deklarationen schlagen vor CRS-Content-Consumption sicher fehl.
- Der frische Control mit freigegebenem Origin verifiziert `FETCH_HEAD`,
  aufgelöstes Objekt, detached Checkout und finales `HEAD` ohne Submodule-Befehl.
- Finaler PR #26 bestand alle Fresh-Head-Checks: CodeQL Actions/C++/Python,
  zwei `scaffold-lint`-Jobs, zwei `common-structure`-Jobs und SonarCloud Code
  Analysis; es gab keine blockierenden Reviews oder Review-Threads.
- PR #26 wurde um `2026-07-19T14:29:48Z` gemergt; finaler Head
  `465766c01e2bb0a9a003cfcefa8afca5fceeafe0` und resultierender Master
  `36cac3029c735dddf9f717b3ce077b9285567a6a` haben Tree
  `75d90508ca6576ae3595010c52f2fd32cfa662c3`.
- Current-Master `git diff --quiet`, `git diff --check` und MRTS-Vergleich
  bestanden. Die fokussierte Provenance-Suite bestand `10` Tests, einschließlich
  ursprünglicher `main`-Ablehnung und frischem Approved-Origin/Full-Commit-Control.
- `rtk make -s check-documentation` bestand. `rtk make -s lint` bestand mit
  nach task-owned external storage umgeleitetem Bytecode-Cache; der nicht
  umgeleitete Retained-Worktree-Versuch traf nur seinen read-only-`__pycache__`-
  Pfad.

Framework-Master-SonarCloud-Run `88203518811` schlug getrennt unter
`FND-SONAR-0002` accepted risk fehl. Er waived, ersetzt oder interpretiert das
erfolgreiche frische PR-Head-SonarCloud-Ergebnis für dieses Finding nicht neu.

## Regression und legitime Control-Tests

`tests/security_regression/test_crs_git_ref_provenance.py` bestand `10`
fokussierte gemockte Git-/Provenance-Tests auf dem aktuellen Master-Tree. Die
prozessgrenzenbasierte Fake-Git-Fixture akzeptiert nur den freigegebenen
literalen Origin und `55b09f5acfd16413e7b31041100711ceb7adc89c`, beobachtet
dann exakten Fetch, Auflösung, detached Checkout und finale HEAD-Verifikation.

## Abhängigkeiten, Blocker, verwandte Findings und Restrisiko

- Abhängigkeiten: keine.
- Blocker: keine.
- Verwandtes Finding: `FND-FRAMEWORK-0003`.
- Restrisiko: Der genehmigte Commit wird nicht zusätzlich über eine Kette
  signierter Release-Attestierungen verifiziert; die Kontrolle vertraut dem
  zentral geprüften Literal und HTTPS/TLS-Git-Transport. Sie setzt außerdem
  vertrauenswürdigen Framework-Code, `CI_ROOT`, Git-Binary/`PATH`, TLS-Trust-
  Store und exklusives Source-Root-Ownership voraus.

## Historie

- `2026-07-17T10:43:59Z`: `bootstrap_created` — aufbewahrte Evidence erzeugte
  das Finding; keine Remediation, Verifikation, Closure oder Risikoakzeptanz
  erfolgte.
- `2026-07-18T08:09:21Z`: `root_cause_triaged` — statische Evidence bei
  `cdc91a398d6c156eaff927d742b23018a3817fb6` bestätigte die separate CRS-
  Mutable-Ref-Provenance-Lücke.
- `2026-07-18T10:41:10Z`: `local_fix_revalidated` — der Framework-Worktree
  bestand fokussierte gemockte Regression, Shell-/Dokumentations-Checks,
  Direct-Pinning, Lint, Exact-Head-CI, SonarCloud und Security-Revalidation vor
  der finalen Dokumentationskorrektur.
- `2026-07-19T15:00:59Z`: `verified_on_master` — PR #26 wurde als aktueller
  Framework-Master gemergt; die ursprüngliche negative Reproduktion und
  legitime Control liefen erfolgreich erneut. Das Finding ist verified, nicht
  closed.
