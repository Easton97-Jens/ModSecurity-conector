# Change Record: CR-20261024-pr410-sonar-remediation

**Language:** English | [Deutsch](CR-20261024-pr410-sonar-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261024-pr410-sonar-remediation |
| Date (UTC) | 2026-10-24 |
| Base revision | `e509db65601057154c184757e2632e65b9dad403` |

## Motivation and problem statement

PR #410 retained one Sonar vulnerability, twelve smells, local lifecycle
failures and Apache CI fixture errors. Its accumulated documentation and report
history also obscured the current review surface.

## Acceptance criteria

Repair the identified causes without weaker controls; run one predeclared
selection of at most 100 active scenarios with no retry; reduce the actual PR
diff; preserve Framework/MRTS; publish only truthful exact-head evidence.

## Implementation decision and rationale

Private HAProxy capture output now uses a fixed external boundary, trusted
ancestors, an exclusive 0700 leaf and descriptor-backed 0600 receipts. Focused
refactors remove the twelve smell causes. Test roots and SDK include selection
are corrected at their owners. Historical prose/results are externally archived
instead of retained in the PR.

## Changed files

The focused changes cover the HAProxy capture helper, Envoy/Apache/Traefik
harness controls, native observer tests, the Apache C probe, concise EN/DE docs,
and one Change Record. Ten machine-consumed report inputs remain unchanged from
the integrated PR content.

## Commands executed

RTK wrapped Git inspection, Python compilation, Go formatting/listing, C17
syntax checking, JSON/shell preflight, the single coordinated closeout runner,
and documentation/diff checks. No unwrapped fallback was used.

## Security impact

The plausible public-temp-output path is closed without an exclusion or
suppression. Focused static review found no actionable regression. No deep scan,
policy weakening, secret handling change, or new trust root was introduced.

## Runtime evidence

At frozen head `251dc1263a2a67300b13daebd680c42bb8f4130c`, the only local run selected
75 active scenarios: 73 PASS, zero FAIL, one ERROR and one NOT_REACHED. Python
passed 32/33 methods; the Go function passed. The Apache error was a local
cross-worktree source-root admission failure. Retry count is zero.

## Known limitations

The local aggregate is `FAIL`. This is not full I12/V08–V10 host acceptance,
does not establish repository-wide default-suite cap enforcement, and cannot be
promoted to `verified_pr`.

## Remaining risks

Automatic final-head CI/Sonar may expose environment-specific or scanner
results. Complete host/protocol and blocked deployment evidence remains outside
this reduced closeout.

## Checks not run and rationale

No second functional run, historical matrix, Oracle campaign, deep security
scan, release, deployment or merge was run. A retry was explicitly forbidden;
provider checks are allowed to start only from the pushed final head.

## Final diff and review status

Independent static reviews found no source regression after two documentation
corrections. The docs/report portion is reduced from 482 to 36 changed files;
the PR remains Draft because the one local closeout did not pass.
