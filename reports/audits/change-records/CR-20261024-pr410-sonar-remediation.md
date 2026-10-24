# Change Record: CR-20261024-pr410-sonar-remediation

**Language:** English | [Deutsch](CR-20261024-pr410-sonar-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261024-pr410-sonar-remediation |
| Date (UTC) | 2026-10-24 |
| Base revision | `30d50a181278904a552e295d9a2c1ae1265e8b87` |

## Motivation and problem statement

The exact PR #410 head failed its Sonar Quality Gate because the New Code
Security Rating was E instead of A. The complete analysis contained 231 open
issues and 21 duplicated blocks. Most apparent code was immutable historical
I12 source material stored with executable suffixes; the remainder was live
path/process handling, generator complexity, and genuine native test
duplication. The task required causal repair, one shared-budget local run, and
one final publication without reopening the historical I12 campaign.

## Acceptance criteria

- Bind the complete issue/metric/duplication inventory to the exact starting
  analysis and revision.
- Remove scanner-executable historical-source storage without changing any
  reconstructed byte, result, profile, delta, or revision identity.
- Correct live security/maintainability causes without exclusions,
  suppressions, weakened validation, or changed qualification semantics.
- Consolidate genuine native-test duplication while preserving distinct cases.
- Freeze one import-free, preflighted selection within the shared 100-case
  ceiling; execute it once with no retry.
- Keep Framework/MRTS Gitlinks and reduced I12 closeout unchanged.
- Update EN/DE documentation, publish once to the existing PR branch, and read
  automatic exact-head CI/Sonar to terminal state.
- Claim `verified_pr` only if every result passes. A failed local run must remain
  a failed local verification even if provider checks later pass.

## Implementation decision and rationale

The work used an isolated worktree at
`30d50a181278904a552e295d9a2c1ae1265e8b87`. Sixty-one plain-text historical
objects and one historical observer repository snapshot were migrated to the
archive's existing lossless `text_lines` JSON form. This changes their analysis boundary, not their content: 346,634 bytes
reconstruct exactly and retain their declared SHA-256 identities.

Maintained Envoy parsers replace transitive historical-helper imports, with
separate current and historical identities. A shared `i12_path_safety` module
now applies bounded descriptor-pinned reads, explicit protected output roots,
and traversal/symlink/private-path/mode/checkout controls. A shared process
observation module replaced active imports from the archive. Report generators,
NGINX validation, native C finalization, and tests were decomposed around their
existing control boundaries. `.sonarcloud.properties` adds Python/test
classification only; it contains no exclusion.

The single-run plan counts every loop/subtest/materially distinct assertion
path conservatively. It selected 79 active scenarios and retained the existing
21-case historical reserve, exactly 100 combined. The repository-wide automatic
default paths are not all wired to this inventory, so global technical cap
enforcement is explicitly not claimed.

## Changed files

- `.sonarcloud.properties` supplies analysis language/test classification.
- `ci/lib/i12_path_safety.py` and `i12_process_observation.py` supply maintained
  shared evidence/path/process controls.
- `ci/runtime/lifecycle/i12/manifest.json`, 61 plain-text conversions plus one
  repository-snapshot conversion, capture
  validation, current pins, Envoy maintained parsers, and EN/DE I12/Envoy
  documentation establish the lossless code/data boundary.
- Parent evidence generators, Apache acceptance, lighttpd, NGINX, Envoy,
  HAProxy, Traefik, and native lifecycle code use the maintained controls and
  smaller cause-coherent functions.
- Focused regression tests preserve existing distinct cases and add path/archive
  negatives; the native observer test shares its duplicated compile fixture.
- `docs/pr-410-sonar-remediation-20261024*.md`, the three machine-readable
  records under `reports/testing/pr410-sonar-remediation-20261024/`, and this
  EN/DE Change Record document the baseline, plan, and actual failed result.
- Framework remains `99a7985c1be92a2297b1b59208f64df6768f2cbf`; MRTS remains
  `8a6bb546c4c81d8ffc7be801dceac60c6925685f`.

## Commands executed

- Required-wrapper Sonar CLI/API reads retrieved all 231 open issues, issue
  facets/rules, the gate and measures, all 15 duplication-positive files and
  their blocks, compute-task metadata/warnings, and all 50 GitHub annotations.
- RTK-wrapped Git/GitHub reads established the exact PR/base/master heads,
  Draft state, check state, branch permission, and isolated-worktree baseline.
- The external static verifier reconstructed every line object, checked all
  object/delta hashes and manifest transitions, parsed 61 changed Python files,
  validated 64 JSON files/current pins/no-exclusion state, and passed.
- `git diff --check` passed. Strict C17 `-Wall -Wextra -Werror -fsyntax-only`
  checks passed for `native-lifecycle-observer.c` and
  `apache_header_semantics_probe.c`.
- The import-free test-plan preflight resolved 30 selectors to 39 methods and
  passed the `79 + 21 = 100` guard without imports, builds, or tests.
- One RTK-wrapped `python -m unittest -v` invocation executed the frozen
  selectors with explicit roots/toolchain/SDK/fixture identity and zero retry.
  It ran for 11.431 seconds and returned nonzero with five failures and one
  error. It was not repeated.

## Security impact

The patch narrows trust boundaries: untrusted evidence paths cannot escape
approved roots, follow symlinks, consume private configuration, overwrite
create-only records, or use unsafe parents; reads are size-bounded and
descriptor-pinned. Historical program text is inert authenticated data and no
longer participates in active imports. Existing identity, provenance,
physical-producer, lifecycle, and negative-event requirements remain.

Fresh advisory access readback reported the user's available TAC1 status. It
did not expand repository/platform authority. One focused defensive static
review found no remaining actionable security issue in the patch. No deep
repository scan, credential, suppression, gate weakening, or server-side issue
disposition was used.

## Runtime evidence

The one local functional run is recorded in
`reports/testing/pr410-sonar-remediation-20261024/run-result.json`. Of 79
expanded active scenarios, 65 passed, five failed, one errored, and eight were
not reached after the first companion-loop failure. The unittest summary was
`FAILED (failures=5, errors=1)` across 39 methods.

The Envoy error was a fixture-root binding mismatch before the intended
no-transitive-import assertion. All five native failures stopped in the shared
C++ SDK-helper prerequisite because `-isystem /usr/include` made GCC 15
libstdc++ unable to resolve `#include_next <stdlib.h>`. No failed scenario was
rerun and no executable behavior changed after the run.

The raw 21,256-byte log is retained at
`/var/tmp/codex/ModSecurity-conector/pr410-sonar-final-20261024.0T0N9T/functional-run.log`
with SHA-256
`4015acc961e1af01a1d88884a2960ae349230f44a001c4d93841521ea6fcdaa3`.

## Known limitations

- Current-head runtime acceptance and final local verification are missing
  because the only permitted run failed and eight selected variants were not
  reached.
- The automatic global default-suite inventory and technical 100-case guard
  remain `not_verified`; only this task's frozen plan had a passing guard.
- Sonar supplied no PR coverage measure, so no coverage percentage is claimed.
- Static source evidence predicts issue/duplication closure but cannot replace
  the automatic exact-published-head Sonar analysis.
- The existing 21-case closeout remains historical and is not transferred to
  this new head.

## Remaining risks

The fixture-root mismatch and C++ include-path failure need a future explicitly
authorized remediation and new run; this task's no-retry contract prevents
repair-and-retest here. Automatic CI may expose additional failures. Any open
Sonar finding, red/pending required check, review blocker, or head mismatch also
keeps the PR at `remediation_required` or `checks_pending`.

## Checks not run and rationale

No second functional run, full suite, `make lint`, `quick-check`, or
`codex-check` was run because those paths contain functional tests and would
repeat or exceed the frozen selection. No historical I12 host/matrix campaign,
Oracle reconciliation, PASS refresh, Framework/MRTS execution, release,
deployment, or merge was authorized. No local Sonar scanner upload was used;
the mandatory automatic analysis belongs to the one published head.

## Final diff and review status

Static integration review findings concerning `CODEX_PROJECT_STATE`, current
source pins, the old native observer object, and active archive consumers were
corrected before the run. The focused security review had no actionable
finding. Archive identity, Framework Gitlink, JSON/Python/C static checks, and
diff whitespace checks passed.

The functional checkpoint failed, so this Change Record does not assert
`verified_pr` or review readiness. The final published commit and terminal
automatic CI/Sonar identities are written to PR #410 after the single push;
their outcome cannot retroactively change the failed local evidence.
