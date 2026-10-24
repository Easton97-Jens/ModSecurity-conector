# Change Record: CR-20261024-pr410-sonar-remediation

**Language:** English | [Deutsch](CR-20261024-pr410-sonar-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261024-pr410-sonar-remediation |
| Date (UTC) | 2026-10-24 |
| Base revision | `e509db65601057154c184757e2632e65b9dad403` |
| Final repair start | `a1edb5c9b3722eec8c6911345d3315dd82eb145a` |

## Motivation and problem statement

PR #410 retained one Sonar vulnerability, twelve smells, local lifecycle
failures and Apache CI fixture errors. Its accumulated documentation and report
history also obscured the current review surface. After the prior remediation,
one MINOR smell and one local Apache guard ERROR with one dependent NOT_REACHED
case remained for this final targeted repair.

## Acceptance criteria

Repair the identified causes without weaker controls; run one predeclared
selection of at most 100 active scenarios with no retry; reduce the actual PR
diff; preserve Framework/MRTS; publish only truthful exact-head evidence.

## Implementation decision and rationale

Private HAProxy capture output now uses a fixed external boundary, trusted
ancestors, an exclusive 0700 leaf and descriptor-backed 0600 receipts. Focused
refactors remove the twelve smell causes. Test roots and SDK include selection
are corrected at their owners. Historical prose/results are externally archived
instead of retained in the PR. The earlier repair used a behavior-equivalent
dictionary comprehension, which triggered a different Sonar rule. The Apache guard copies the exact registry-hash-bound
Framework case into its private test root; production path admission is unchanged,
and negative assertions now identify their intended rejection branches.

## Changed files

The focused changes cover the HAProxy capture helper, Envoy/Apache/Traefik
harness controls, native observer tests, the Apache C probe, concise EN/DE docs,
and one Change Record. The final repair additionally changes only
`connectors/apache/harness/apache_oracle_overrides.py`,
`tests/test_apache_header_semantics.py`, this concise EN/DE closeout pair and this
Change Record pair. Ten machine-consumed report inputs remain unchanged from the
integrated PR content.

## Commands executed

RTK wrapped Git inspection, Python compilation, Go formatting/listing, C17
syntax checking, JSON/shell preflight, the single coordinated closeout runner,
and documentation/diff checks. The final repair used RTK-wrapped Sonar readback,
Python compilation, JSON/shell/hash/count preflight and exactly one four-method
unittest invocation through
`rtk bash /var/tmp/codex/ModSecurity-conector/pr410-last-repair-20261024/run-closeout.sh`.
No unwrapped fallback was used.

## Security impact

The plausible public-temp-output path is closed without an exclusion or
suppression. Focused static review found no actionable regression. No deep scan,
policy weakening, secret handling change, or new trust root was introduced. The
final test fixture remains under a private test-owned root and validates the real
Framework bytes against the existing registry SHA before use.

## Runtime evidence

The earlier retained run remains 73/75 PASS with one ERROR and one NOT_REACHED.
The separately authorized final repair run
`pr410-last-repair-20261024-final-001` bound starting head
`a1edb5c9b3722eec8c6911345d3315dd82eb145a` to executable patch SHA-256
`2e3681297d924921b82449b82da7675ce4dee0f35d3f968989af0401ec683057`.
All four methods / 13 expanded active scenarios passed, with zero retries. Result
SHA-256: `f6d02a742713a9d1ec8cab5e399cdb52b32e198b798eaae00795940c20ec0fbf`.

## Known limitations

The final targeted local aggregate is `PASS`. This is not full I12/V08–V10 host
acceptance and does not establish repository-wide default-suite cap enforcement.
`verified_pr` still depends on automatic exact-head CI/Sonar and review readback.

## Remaining risks

Automatic final-head CI/Sonar may expose environment-specific or scanner
results. Complete host/protocol and blocked deployment evidence remains outside
this reduced closeout.

## Checks not run and rationale

No second final-repair run, historical matrix, Oracle campaign, deep security
scan, release, deployment or merge was run. Retry count is zero; provider checks
start only from the pushed final head.

## Final diff and review status

Independent static reviews found no source regression after the documentation
corrections. Against the actual PR base, the docs/report portion is reduced
from 193 to 25 changed files. The final targeted local run passes; the PR remains
Draft while automatic exact-head verification is pending.

## Authorized integration follow-up

Starting at `11324289a724b61ab2279f56c16e9185e240ccc9`, replace the redundant
generator/identity-comprehension pair with an explicit parsing loop in
`connectors/apache/harness/apache_oracle_overrides.py`. Full `S7494` and `S7500`
messages were read; first-`=` splitting, duplicate-key precedence and malformed
line rejection are preserved. No suppression, rule exclusion or admission change.
The same four guard methods / 13 expanded scenarios passed once in 0.759 seconds
through the RTK-wrapped Parent interpreter (3.14.4). Selection preflight confirms
that these 13 scenarios are a subset of the existing 75-case inventory.
The task-owned command, selection, patch digest and result are retained at
`/var/tmp/codex/ModSecurity-conector/runs/pr382-integrate410-20261024`.
Hosted 3.14.7 checks and exact-head Sonar for this unpublished follow-up remain
pending. Existing historical results keep their original revision bindings.
