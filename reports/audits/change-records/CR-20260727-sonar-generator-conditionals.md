# Change Record: Parent Python generator conditionals for SonarQube Cloud python:S3358

**Language:** English | [Deutsch](CR-20260727-sonar-generator-conditionals.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-generator-conditionals |
| Date (UTC) | 2026-07-27 |
| Base revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent SonarQube Cloud Code Smell `python:S3358`. The original candidate's local evidence is recorded below; the normal current-master refresh creates a new exact head that requires its own hosted analysis. |
| Boundary | Parent conditional refactoring in `ci/lib/generated_report_utils.py` and `scripts/generate_compiler_guides.py`, the focused existing test sources, this English/German pair, and its indexes. No generated output, workflow, configuration, Framework, MRTS, or Gitlink change is part of the candidate; this record is refreshed only to correct its PR delivery-state description. |

## Motivation and problem statement

The batch resolves the selected `python:S3358` nested-conditional expressions
with explicit `if`/`elif`/`else` branches. The objective is to make the
provenance-status and guide-note choices easier to read without altering their
observable behavior.

## Acceptance criteria

- Preserve the Framework provenance statuses `not_a_gitlink`,
  `matches_checkout`, and `checkout_mismatch` for the same inputs.
- Preserve the compiler-guide package-note selection for Envoy and Traefik,
  the blank fallback for other connectors, and the existing `http_note`
  override/default fallback behavior.
- Leave generated guide output, workflows, configuration, Framework, MRTS,
  Gitlinks, and delivery unchanged.
- Record the exact base, handed-over local validation receipt, limitations,
  and required fresh exact-head Sonar analysis in this complete English/German
  pair and its indexes.

## Implementation decision and rationale

`framework_provenance()` now assigns `gitlink_status` in an explicit branch
before returning the same metadata dictionary: an unknown recorded Gitlink is
`not_a_gitlink`, an equal checkout is `matches_checkout`, and any other
recorded Gitlink is `checkout_mismatch`.

`expanded_guide()` first selects the existing English/German package-note pair
for `envoy` or `traefik`, or the existing empty pair otherwise, then passes it
to `localized()`. `source_first_guide()` likewise keeps the existing
`info["http_note"]` override and uses the same loopback-only default note when
that key is absent. These explicit branches preserve framework-provenance
status and guide output/fallback semantics; they do not regenerate or edit any
generated guide.

## Changed files

- ci/lib/generated_report_utils.py
- scripts/generate_compiler_guides.py
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md
- this English/German Change Record pair

## Tests and actual results

- An earlier handed-over focused receipt reported 100 tests: 21 compiler-guide
  tests, 5 Framework-provenance tests, and 74 generated-report
  evidence-integrity tests. Its exact invocation and duration were not
  retained, so neither is attributed to that earlier receipt.
- The final local validation expanded the provenance module to its full 13
  tests and passed 108 tests in total: 21 compiler-guide, 13 connector-
  capabilities, and 74 generated-report evidence-integrity tests.
- The final scoped `git diff --check`, bytecode-free syntax compilation, and
  bilingual documentation check passed after this pair and both index entries
  were added.

## Commands executed

- `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1`
  `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v`
  `tests.test_compiler_guides tests.test_connector_capabilities`
  `tests.test_generated_report_evidence_integrity` passed 108 tests in
  22.348s.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 make`
  `check-bilingual-docs` passed after this record was completed.
- `git diff --check` and bytecode-free `py_compile` of both changed Python
  sources passed.

## Security impact

This is a behavior-preserving readability refactor in a provenance/evidence
path and a guide generator. It preserves the existing Framework provenance
status values, guide note selection, and guide fallback semantics; it adds no
new untrusted input, command, filesystem, network, credential, authorization,
or isolation behavior. No security control is weakened and no security finding
is asserted by this record.

## Runtime evidence

No compiler, package, connector, Framework, MRTS, generator, or host runtime
was run. The focused test evidence is local unit-test evidence, not runtime or
external Sonar evidence.

## Checks not run and rationale

- No generated guide output was regenerated or compared as new output, because
  generated output is explicitly outside this refactor/documentation scope.
- After a read-only checkout of the Parent-pinned Framework revision,
  `make check-doc-links` passed together with `make check-bilingual-docs`.
  The earlier candidate later became Draft PR #140, so its former head-specific
  hosted CI/Sonar/review state is no longer represented as absent. This normal
  current-master refresh creates a different head; no fresh hosted result,
  review result, or merge outcome for that refreshed head is asserted here.

## Known limitations

The original source base is
`1b0f8825f3510b99b603bb6cd6f0777e1710358e`; the candidate is now Draft PR
#140 and receives a normal current-master refresh. The 108-test result is
focused local evidence only; it does not establish a result for the refreshed
exact head, runtime result, review, or delivery outcome.

## Remaining risks

The status and guide branches feed provenance/evidence handling and rendered
documentation. Existing focused test coverage supports semantic preservation,
but any later source, documentation, or commit change creates a different
head. A fresh SonarQube Cloud analysis for the exact delivered head remains
required before the `python:S3358` finding can be treated as externally
resolved.

## Final diff and review status

The candidate is an open Draft PR. No generated output, workflow,
configuration, Framework, MRTS, or Gitlink change is included. No merge or
other delivery outcome is asserted by this record; a fresh exact-head hosted
analysis remains required after the current-master refresh.
