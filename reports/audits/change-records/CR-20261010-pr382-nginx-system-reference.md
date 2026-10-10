# Change Record: CR-20261010-pr382-nginx-system-reference

**Language:** English | [Deutsch](CR-20261010-pr382-nginx-system-reference.de.md)

Documentation-only downstream reference; original runtime status and remaining measurement gap are separate.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261010-pr382-nginx-system-reference |
| Date (UTC) | 2026-10-10 |
| Base revision | `2a5704f82fdae4ba75902eb3f4244225838e1747` |

## Motivation and problem statement

Document a downstream NGINX-H1 system evidence reference from PR #396 without claiming that the unchanged PR #382 product was runtime-tested.

## Acceptance criteria

Both languages retain the exact tested tuple/run, original Canonical status, direct First-Byte-writer exit, concrete local system and remaining measurement gap. Broad connector acceptance points stay open; no product, Gitlink or runtime-evidence changes.

## Implementation decision and rationale

Use a separate documentation-only worktree on the verified PR #382 branch. New narrowly scoped I12b/V08a/V09a/V10a entries reference observed subsets, not complete acceptance. Mark 2026-10-05 stack assertions explicitly historical.

## Changed files

`docs/pr-382-checklist.md`, `docs/pr-382-checklist.de.md`, and this paired Change Record. No product files or generated runtime evidence changed.

## Commands executed

Executed `rtk proxy /var/tmp/codex/ModSecurity-test-Framework/venv/bin/python ci/tools/new-change-record.py create --name pr382-nginx-system-reference --base-revision 2a5704f82fdae4ba75902eb3f4244225838e1747 --date 2026-10-10`: exit 0. Documentation validation results are recorded after their actual execution; no unexecuted check is claimed here.

Executed native archive check `rtk proxy /var/tmp/codex/ModSecurity-test-Framework/venv/bin/python ci/tools/new-change-record.py check`: exit 0 (structure only). Executed `rtk proxy /var/tmp/codex/ModSecurity-test-Framework/venv/bin/python -m unittest -v tests.test_change_record tests.test_prepare_reviewed_framework_handoff`: 39 tests, 0 SKIP, exit 0. Executed `rtk proxy git -C /var/tmp/codex/ModSecurity-conector/worktrees/pr382-nginx-system-docs-r16 diff --check`: exit 0.

Initial native documentation command `rtk proxy make --no-print-directory PYTHON=/var/tmp/codex/ModSecurity-test-Framework/venv/bin/python FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/framework-nginx-seven-contracts-20261008 BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/analysis/nginx-full97-777a244f-20261010T181030Z/doc-validation-build check-bilingual-docs check-doc-links`: exit 2. The unchanged bilingual checker reported 22 missing local submodule targets in the unpopulated documentation worktree; check-doc-links did not execute. No validator was weakened or link/symlink workaround introduced. This failure remains recorded independently from later validation.

After Root populated the physical Framework tree at this documentation base's unchanged Gitlink `dc41bd22c335156cae02d9049098b92af65b7c57`, executed `rtk proxy make --no-print-directory PYTHON=/var/tmp/codex/ModSecurity-test-Framework/venv/bin/python FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/pr382-nginx-system-docs-r16/modules/ModSecurity-test-Framework BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/analysis/nginx-full97-777a244f-20261010T181030Z/doc-validation-build check-bilingual-docs check-doc-links`: exit 0; bilingual docs, repository path references and doc links all passed. The earlier missing-tree failure is resolved, not erased. Manual EN/DE review confirms identical hashes, IDs, counts, boundaries and checked/unchecked items.

## Security impact

No security controls, validators, isolation, Required selection or CI gates changed. No secrets, hostnames or public addresses are included. The missing exact generic Strict client process exit remains visible.

## Runtime evidence

R16 `nginx_full97_777a_20261010_r16`, tested Parent `777a244f0689c320475b030b9e7adbb3192febbe`, Framework `9f41f80db7bf53b57429457bce0dda675d2ec5d7`, MRTS `8a6bb546c4c81d8ffc7be801dceac60c6925685f`. Original Canonical PASS, 97/97 Required-PASS, empty schema errors. Exactly one direct First-Byte source writer completion exit 0; 13 direct completions/nine programs all exit 0. The standard target ran on the concrete local system described in the checklist. Original R15 remains untouched.

## Known limitations

The generic H1 Strict curl process's numeric exit is NOT SEPARATELY MEASURED; diagnostic 52 is not exit 52. LOCAL acceptance remains BLOCKED despite original Canonical PASS. No H2/H3, CRS, Off, all-platform, production or Protected proof; other connector routes remain separate.

## Remaining risks

Public summaries do not distribute the local raw bundle. The PR #382 product revision was not tested by this downstream run. Ready/CI/Sonar/merge outcomes are not inferred from runtime or documentation success.

## Checks not run and rationale

No Full97, runtime, build, Git delivery, API action or Ready transition was performed by the documentation worker. Root owns runtime/delivery/readiness decisions; no second full run is part of this change.

## Final diff and review status

Only the four owned documentation paths are changed; native documentation/archive checks, 39 regressions and whitespace checks passed. Manual EN/DE and final diff review found no unrelated changes or unfinished scaffold sections. Documentation edits are not committed or published by this worker; independent Root review and normal delivery remain separate. No merge or history rewrite.
