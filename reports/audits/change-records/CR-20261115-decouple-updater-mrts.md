# Change Record: CR-20261115-decouple-updater-mrts

**Language:** English | [Deutsch](CR-20261115-decouple-updater-mrts.de.md)

Connector updater ownership change requested by the user; validation status is recorded below.

**Pre-publication validation snapshot.** This record captures local validation before task-branch and Draft pull-request delivery. Track the exact delivered head and current CI results in the resulting pull request. Integration into `master` is outside this task's authority.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261115-decouple-updater-mrts |
| Date (UTC) | 2026-11-15 |
| Base revision | `3b47c48e58caad35dc66f7e5b6786f81ed7fed9b` |

## Motivation and problem statement

The Update submodules run `43708408697` rejected a descendant Framework commit because its MRTS gitlink moved backwards. The user requested that the Connector updater stop making an independent MRTS selection decision.

## Acceptance criteria

Accept an exact descendant Framework candidate regardless of the ancestry of its nested MRTS pin. Derive the lock's `mrts_sha` from that candidate, without fetching MRTS. Preserve Framework ancestry, exact identities, nested topology/URL checks, isolated validation and constrained publication.

## Implementation decision and rationale

Remove the updater's MRTS remote fetch and ancestry comparison. In both validator and publisher, read the nested pin from the exact Framework object using the existing gitlink reader. Pass that derived value to all three verifier calls with `--expected-candidate-mrts-sha` and all five synchronization/primary-verification calls with `--mrts-sha`. This preserves a consistent revision-lock pair without a separate MRTS release decision. Other callers' defaults and the lock schema remain unchanged.

Four sandbox invocations still referenced Parent script paths removed by the test-ownership migration. Route prepare, verify and cleanup through the existing authenticated `ci/run-trusted-framework.py` bridge with `--tool readonly-prepare`, and namespace execution with `--tool readonly-namespace`. Bind `--connector-revision` to `EXPECTED_PARENT_HEAD`, supply the reader UID/GID and trusted Framework object, and load the standard-library-only helper from the old pinned Framework object even while the candidate is checked out. Sandbox isolation and output contracts remain unchanged. Independent review of the helpers and their standard-library dependencies reported no findings.

## Changed files

- `.github/workflows/update-submodules.yml`: Framework-owned nested selection, complete lock-value propagation and authenticated routing of all four sandbox helper calls.
- `ci/README.md`, `ci/README.de.md`: equivalent ownership and validation documentation.
- `reports/audits/change-records/CR-20261115-decouple-updater-mrts.md`, `reports/audits/change-records/CR-20261115-decouple-updater-mrts.de.md`: this record pair.

## Commands executed

The user explicitly permitted Windows execution without the unavailable RTK wrapper and Linux startup skill. The native POSIX scaffolder ran in existing WSL Ubuntu with explicit Connector/Framework context: `python3 -B ci/tools/new-change-record.py create --name decouple-updater-mrts --date 2026-11-15 --base-revision 3b47c48e58caad35dc66f7e5b6786f81ed7fed9b` (exit 0; both scaffolds created).

- Explicit `sonar analyze secrets` checks passed for the selected source and verification inputs; raw scanner output was suppressed. Delivery retains the Secrets-before-read requirement for final edited bytes.
- Existing WSL Ubuntu executed the Secrets-scanned external task artifact `verify_updater.py` with `python3 -B` (exit 0). It parsed the complete YAML, checked all 26 `run` steps with `bash -n`, and verified argument propagation to exactly three verifier and five synchronization calls.
- Its offline Git fixtures passed same, forward, backward and divergent MRTS selections with the MRTS repository deliberately unreachable: workflow checkout, both derivation snippets, structural/state validation, pre/post contract verification and correct idempotent lock projection passed. The baseline workflow reproduced the exact MRTS rollback rejection. Invalid pins, an inconsistent old lock and non-descendant Framework commits were rejected.
- Independent workflow review reported no findings. `git diff --check` passed (exit 0) before this record update.
- The first native test run on the Windows mount encountered a file-permission failure and was stopped. The replacement run used native Linux task storage under `/var/tmp/codex/ModSecurity-conector/updater-20261115`: all three existing local-Git and 15 state-validation tests passed (18 tests, 110.948 seconds, exit 0).
- The external task artifact `verify_updater_docs.py` passed (exit 0): native EN/DE language switches and structure, Change Record schema/identity, and every local link in all four changed documentation files.
- After the helper-routing change, `verify_updater.py --static` passed (exit 0): complete YAML, all 26 Bash steps, three verifier/five synchronization argument paths, four complete authenticated object-bridge calls, and existence of every directly invoked Parent Python path.
- Actual `--help` smoke invocations of `readonly-prepare` and `readonly-namespace` through `ci/run-trusted-framework.py` each passed (exit 0), using the exact Parent revision, reader UID/GID `1000`/`1000` and `--trusted-framework-object`. These prove authenticated helper loading and argument parsing, not full namespace execution.
- Independent helper/standard-library review reported no findings. `verify_updater_docs.py` passed again (exit 0) after the routing change.

## Security impact

MRTS release selection belongs to Framework. Parent retains exact Framework identity and forward ancestry, nested metadata allowlists, old lock-pair integrity, read-only validation isolation and publication constraints. The sandbox helper bridge authenticates the baseline Parent revision and pinned Framework object before loading code; candidate-selected Python is not trusted. No MRTS source or repository is changed. CI permissions, branch protection, scanner configuration and Cloud gates remain unchanged.

## Runtime evidence

No hosted workflow rerun or connector runtime qualification has been performed for these local changes.

## Known limitations

This pre-publication snapshot does not claim a delivered commit, pull-request identity or current-head hosted CI result. Task-branch and Draft pull-request delivery are tracked separately; no merge authority is granted. The historical failed run is unchanged. The separate Framework/MRTS ownership and repository structure remain intact.

## Remaining risks

The updater now accepts Framework-owned MRTS pin changes, including backwards or divergent selections, without independent Parent release approval. Framework maintainers own that selection; Parent still rejects malformed or inconsistent projection data and unrelated nested topology changes.

## Checks not run and rationale

Hosted CI, Cloud analysis, product builds, full namespace execution and runtime matrices have not run for this pre-publication snapshot; this task changes updater ownership rather than connector runtime behavior. Completed local helper-routing checks and smoke tests establish only the evidence layers stated above.

## Final diff and review status

Independent workflow and helper reviews reported no findings. Offline behavioral/syntax checks, all 18 selected native tests, scoped documentation checks, final static bridge-routing checks and both authenticated helper-loading smoke tests passed. This is the pre-publication validation snapshot; resolve the exact delivered head and current CI from the resulting Draft pull request. `master` integration is outside the authorized scope.
