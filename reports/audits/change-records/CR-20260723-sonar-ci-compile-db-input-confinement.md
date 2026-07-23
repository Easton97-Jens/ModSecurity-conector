# Change Record: CI compile-database capture-input confinement for SonarQube Cloud

**Language:** English | [Deutsch](CR-20260723-sonar-ci-compile-db-input-confinement.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260723-sonar-ci-compile-db-input-confinement |
| Date (UTC) | 2026-07-23 |
| Base revision | a308d7b414f0859490fe7253e0683a4bde80b563 |
| Tracking | FND-SONAR-0016; SonarQube Cloud `AZ9dWiALxi9ITghe3pzq` (`pythonsecurity:S8707`), `AZ9dWiALxi9ITghe3pzp` (`python:S3516`), and `AZ9dWiALxi9ITghe3pzo` (`python:S3776`). |
| Boundary | Parent CI compile-database tool, its two Bear wrappers, direct regression tests, and this English/German Change Record pair and indexes. Framework, MRTS, gitlinks, scanner configuration, Quality Gates, suppressions, and default branch remain unchanged. |

## Motivation and problem statement

The non-verify compile-database command accepted `--input`, constructed a
`Path`, and passed it to `load_database`, which read it with `read_text` after
only checking that it was a file. The tool enforced an external-output
constraint but no equivalent input capture boundary. A caller-controlled value
could therefore select an unintended file for JSON parsing and later
processing.

The same source also contained the selected redundant-success-return and
cognitive-complexity findings. They are handled without weakening any capture,
source, or output validation.

## Acceptance criteria

- A non-verify `--input` requires an explicit `--capture-root`; verify-only
  rejects both input-side arguments.
- The root is absolute, existing, non-symlinked, outside the checkout, a safe
  runtime path, owned by the effective user, and neither group-writable nor
  accessible by other users.
- The resolved input is absolute, outside the checkout, contained by that
  root, and a regular file before it reaches `load_database`.
- Relative, checkout-contained, symlink-escaping, unsafe-root, and
  symlink-root controls fail before the read; a valid private Bear-style
  capture still publishes.
- Both Bear wrappers pass their own `mktemp` capture directory. Existing
  filtering, merge, atomic publication, and verify-only behavior remain
  covered.
- Fresh exact-head SonarQube Cloud and hosted-check evidence is required before
  the three selected keys are declared resolved.

## Implementation decision and rationale

`compile_database.py` now imports the existing Parent runtime-path policy and
uses it to validate an explicit capture root. It canonicalizes that root with
strict resolution, rejects a direct root symlink, rejects checkout and unsafe
runtime roots, and checks owner/mode metadata. The input is then strictly
resolved and must remain outside the checkout and below the validated root.
Only that canonical input is supplied to `load_database`.

The two existing Bear callers already create private external capture
directories. They now forward that exact directory through `--capture-root`,
which preserves their artifact layout while making the trust boundary explicit
at the read sink.

`collect_entries` delegates parse and filter decisions to narrow helpers. The
same accepted entries, filter messages, duplicate handling, source tracking,
and output-in-checkout rejection are retained while lowering the selected
function's cognitive complexity. `main` has one common success return rather
than separate equivalent returns.

## Changed files

- ci/checks/analysis/compile_database.py
- ci/checks/analysis/compile-db-nginx-c17.sh
- ci/checks/analysis/compile-db-cpp17.sh
- tests/test_c_cpp_diagnostics.py
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Security impact

The repaired source-to-sink path is `args.input` to `Path(args.input)` to
`load_database` and `read_text`. Before that sink, the code now establishes a
canonical external capture-root invariant. The regression control deliberately
places invalid non-JSON data outside the root behind a symlink; the new error
is the root-containment failure, demonstrating that parsing does not occur.

No rule, Quality Gate, suppression, exclusion, issue disposition, or scanner
configuration is changed. No authentication, isolation, validation, logging,
or CI protection is weakened.

## Commands executed

- Focused `tests.test_c_cpp_diagnostics`: passed (7 tests), including the
  legitimate capture and all stated negative controls.
- Focused `tests.test_bilingual_docs`: passed (11 tests).
- `make check-ci-security-contract` with the Parent virtual environment:
  passed (16 workflow-security tests and three installed-tool validation
  checks).
- In-memory syntax compilation of the changed Python source and test, `sh -n`
  for both changed Bear wrappers, and `git diff --check`: passed for the final
  local candidate.
- `make check-bilingual-docs`: blocked only by pre-existing links below the
  intentionally uninitialized Framework gitlink; no missing section or
  equivalence error is reported for this Change Record pair.

## Runtime evidence

The direct regression module starts the real compile-database CLI against
temporary external directories. Its legitimate control publishes a real JSON
compilation database from a private capture root. Its non-JSON symlink target
is outside that root and fails with containment validation before parsing.
No live Bear, NGINX, or C++ build is represented as executed.

## Validation status

For the final local candidate, the focused Parent
`tests.test_c_cpp_diagnostics` suite passes all seven tests, including valid
capture, missing-root, relative input, checkout input, symlink escape,
symlink loop, unsafe-root, symlink-root, and verify-only controls. Selected
syntax, shell syntax, diff, and focused bilingual checks pass. Exact-head
delivery checks are recorded only after their actual post-push execution.

## Known limitations and follow-up

Canonical path validation is not descriptor-level protection against a
concurrent same-user rename after validation. The production wrappers create
private `mktemp` roots, which materially reduces that exposure, but this change
does not claim a race-free descriptor open.

FND-SONAR-0017 records a separate plausible external `--output` read/write
path candidate. It has not been reproduced or classified as a concrete
vulnerability, and this input-focused change does not claim to fix it.

## Remaining risks

A concurrent process with the same effective-user authority could still rename
files after canonical validation and before `read_text`; descriptor-confined
opening would be a separate hardening change. The existing external output
argument is intentionally not reclassified as safe by this PR and remains
tracked in FND-SONAR-0017 pending direct validation.

## Checks not run and rationale

- No live Bear/NGINX/C++ compilation database generation: it requires Bear,
  compilers, NGINX and ModSecurity prerequisites, and an external artifact
  setup; the direct Python boundary and both caller contracts are covered
  deterministically without those dependencies.
- No Framework or MRTS test or modification: both are outside this Parent-only
  batch.
- `make check-bilingual-docs` was run but is blocked only by missing targets in
  the intentionally uninitialized Framework gitlink; it is not represented as
  passing. The targeted bilingual Change Record test passes.
- Hosted checks, exact-head SonarQube Cloud analysis, and Quality Gate are
  pending until the unmerged Draft PR branch is pushed.

## Delivery status

The candidate is prepared on an isolated Parent task branch based on current
master. It will be committed, pushed, and opened only as an unmerged Draft PR.
No merge, default-branch update, or Framework/MRTS change is authorized.

## Final diff and review status

An independent read-only security review found the selected input source-to-
sink closure and caller compatibility sound, and recommended only a fail-
closed `RuntimeError` catch for strict path resolution; that recommendation is
included. The final local diff and all named local validation commands were
rechecked after this record update and passed, except for the separately
documented Framework-gitlink documentation blocker. SonarCloud, hosted checks,
PR number, and Quality Gate remain pending until the exact branch head is
pushed.
