# Change Record: Parent Lighttpd harness JSONL validation deduplication candidate

**Language:** English | [Deutsch](CR-20260727-sonar-lighttpd-harness-duplication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-lighttpd-harness-duplication |
| Date (UTC) | 2026-07-27 |
| Base revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Local Parent candidate for the retained 22+22 duplicated parser/normalizer source block. No external SonarQube Cloud issue, Quality Gate, or success result is asserted. |
| Boundary | Parent Lighttpd harness source/tests, this English/German Change Record pair, and their indexes only. Framework, MRTS, Gitlinks, scanner configuration, suppressions, and external issue state are unchanged. |
| Framework observation | Read-only `git submodule status modules/ModSecurity-test-Framework` observed `47e50e7bc43ba7a3b5bad1a9448111794f664cc0 modules/ModSecurity-test-Framework (heads/master)` at the Parent Gitlink. No Framework source, Gitlink, or delivery change is claimed. |
| Delivery status | `Draft` delivery pending; the observed candidate is local and unstaged. No commit, push, pull request, GitHub CI, hosted SonarQube Cloud analysis, or merge is claimed. |

## Motivation and problem statement

`connectors/lighttpd/harness/write_patched_first_byte_metadata.py` and
`connectors/lighttpd/harness/write_patched_lifecycle_results.py` retained the
same 22+22 duplicated JSONL parser/normalizer source block. The local candidate
shares only JSONL object loading, P4 phase aliases, and the current nonnegative
`int()` coercion. It does not broaden the P4 event contract or change the
callers' output schemas.

The affected input is local JSONL evidence. Blank lines continue to be ignored;
each non-blank line must decode to a JSON object. The candidate centralizes
that primitive handling without converting malformed, non-object, or invalid
counter input into a success case.

## Acceptance criteria

- Replace only the equivalent 22+22 parser/normalizer block with shared
  `load_events`, `phase_is_four`, and `nonnegative` helpers.
- Preserve each caller's error wording through its local `NON_OBJECT_ERROR`
  template: `"{path}:{line_number}: event must be an object"` and
  `"{path}:{line_number} is not an object"`.
- Retain distinct local P4 selectors in `safe_host_action` and
  `safe_phase4_events`; neither selector is shared or relaxed.
- Keep malformed JSONL, non-object records, Boolean and negative counters,
  `body_bytes_inspected` greater than `body_bytes_seen`, and zero, wrong, or
  multiple P4 candidates as failures.
- Keep English/German Change Records and indexes equivalent; record observed
  local source, lifecycle-contract, documentation, and whitespace validation;
  and represent unobserved runtime, hosted, and delivery outcomes truthfully.

## Implementation decision and rationale

The candidate adds
`connectors/lighttpd/harness/patched_event_validation.py` for the three
equivalent primitives. `phase_is_four` keeps the existing `4`, `phase4`, and
`response_body` aliases, including the current hyphen-to-underscore
normalization. `nonnegative` continues to reject `bool`, reject negative
values, and use the existing `int()` conversion for other accepted values;
fractional coercion is therefore not changed by this deduplication.

`load_events` accepts the caller-owned `non_object_error` template instead of
choosing new text. It still calls `json.loads` directly, so malformed JSONL
continues to expose the parser failure. The P4 predicates remain in their
respective writers because their required fields are not identical.

`connectors/lighttpd/tests/test_patched_event_validation.py` is present in the
local candidate as a direct regression test for aliases, schemas, parser and
non-object failures, counter constraints, and candidate cardinality. This
record does not treat the test's presence as an executed source-test result.
Primary implementation validation subsequently ran that module with
`connectors.lighttpd.tests.test_patched_host_contract`; the observed result is
recorded under `## Commands executed`, rather than inferred from the test's
presence.

## Changed files

- `connectors/lighttpd/harness/patched_event_validation.py` — new shared JSONL
  and primitive-validation helper candidate.
- `connectors/lighttpd/harness/write_patched_first_byte_metadata.py` — imports
  the shared primitives while retaining `safe_host_action` and its diagnostic.
- `connectors/lighttpd/harness/write_patched_lifecycle_results.py` — imports
  the shared primitives while retaining `safe_phase4_events` and its
  diagnostic.
- `connectors/lighttpd/tests/test_patched_event_validation.py` — local direct
  regression-test candidate.
- `reports/audits/change-records/CR-20260727-sonar-lighttpd-harness-duplication.md`
  and `reports/audits/change-records/CR-20260727-sonar-lighttpd-harness-duplication.de.md`
  — this complete Change Record pair.
- `reports/audits/change-records/README.md` and
  `reports/audits/change-records/README.de.md` — synchronized index entries.

## Commands executed

The following local results were observed for this candidate. The source and
lifecycle-contract suites were completed by the primary implementation work;
this documentation follow-up records their actual outcomes rather than
claiming them as documentation-worker execution.

- `rtk proxy git status --short` — observed the local source/test candidate as
  unstaged before this documentation pair was added.
- `rtk proxy git submodule status modules/ModSecurity-test-Framework` —
  observed the read-only Parent Gitlink state recorded in `## Identity`.
- `python -m unittest -v connectors.lighttpd.tests.test_patched_event_validation connectors.lighttpd.tests.test_patched_host_contract`
  — `passed`; 20 tests passed.
- `python -m unittest -v tests.test_full_lifecycle_evidence tests.test_collect_no_crs_source`
  — `passed`; 51 tests passed.
- `make check-bilingual-docs check-doc-links` — `passed`.
- `git diff --check` — `passed`; no whitespace error.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_bilingual_docs`
  — `passed`; output reported `Ran 14 tests` and `OK`.

## Security impact

Security classification: `not_applicable` as a new security finding. A focused
security review of this candidate observed no new validated or plausible
finding. This documentation work changes no security control. The observed
candidate retains the fail-closed local-file JSONL boundary: malformed input
remains a parser failure, non-object input retains caller-owned diagnostics,
Boolean/negative counters fail, over-inspection fails, and the P4 selectors
require exactly one matching event. The distinct selectors remain local rather
than becoming a broader shared acceptance rule.

## Runtime evidence

`not_applicable`: no connector service, live host, Framework, or MRTS runtime
was started by this documentation-scoped work. The record reports static local
candidate behavior and observed local source, lifecycle-contract, and
documentation validation; it does not claim runtime behavior.

## Known limitations

Primary source and lifecycle-contract verification is no longer pending: the
two suites under `## Commands executed` passed 20 and 51 tests respectively.
This documentation follow-up did not independently start a connector runtime,
Framework, or MRTS test. The candidate remains pending an authorized `Draft`
commit and later delivery. The record cannot establish a SonarQube Cloud
duplication result until an exact delivered head is analyzed.

## Remaining risks

Later changes to either local P4 selector, caller diagnostic, or counter
conversion can reintroduce behavioral divergence. Hosted analysis, CI/review,
and the `Draft` commit/delivery remain pending and must be recorded only from
later observed evidence.

## Checks not run and rationale

- Connector runtime, Framework, and MRTS tests: `not_run`; they are outside
  this Parent documentation scope.
- SonarQube Cloud analysis, GitHub CI, commit, push, pull request, and merge:
  `not_run`; no delivery or hosted action has occurred or is authorized to this
  worker.

## Final diff and review status

Observed local validation is `passed` for the focused Lighttpd source suite
(20 tests), lifecycle-contract suite (51 tests),
`make check-bilingual-docs check-doc-links`, and `git diff --check` after this
pair and both index entries were updated. The product candidate is local and
unstaged; an authorized `Draft` commit and subsequent delivery remain pending.
No commit, push, pull request, GitHub CI, hosted SonarQube Cloud analysis, or
merge is claimed.
