# Change Record: Parent HAProxy HTX diagnostic-range literal for SonarQube Cloud `shelldre:S1192`

**Language:** English | [Deutsch](CR-20260728-sonar-haproxy-htx-diagnostic-s1192.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260728-sonar-haproxy-htx-diagnostic-s1192 |
| Date (UTC) | 2026-07-28 |
| Base revision | `8e8acb8dab1cd03723de269cab7da7dd62e5e010` |
| Tracking | Parent SonarQube Cloud issue `AZ9cRysjHhV2CayPTP01`, rule `shelldre:S1192`, initially reported at `connectors/haproxy/harness/run_haproxy_htx_runtime.sh:445` for the literal `1,160p` repeated in 13 failure diagnostics. |
| Boundary | Parent-only HAProxy HTX runtime harness, its focused Parent helper contract test, and this English/German Change Record pair with its indexes. Framework, MRTS, Gitlinks, Makefiles, workflows, scanner configuration, Quality Gates, suppressions, and external issue state are unchanged. |
| Candidate status | Local candidate only. A future Draft pull request and its fresh exact-head hosted validation are pending. This record asserts no commit, push, pull request, merge, `master` update, or global SonarQube Cloud closure. |

## Motivation and problem statement

The HAProxy HTX runtime harness used the static `sed` range `1,160p` in 13
failure-diagnostic calls. SonarQube Cloud reported that repeated literal as
`shelldre:S1192`. The range is a fixed presentation bound for failure logs;
it is not a runtime input and does not control HAProxy or ModSecurity request
processing.

The candidate names the range once as the readonly shell variable
`HAPROXY_HTX_DIAGNOSTIC_RANGE` and uses that variable at each of the 13
diagnostic call sites. The distinct pre-existing version-file diagnostic range
`1,40p` remains independent and is outside this change.

## Acceptance criteria

- `HAPROXY_HTX_DIAGNOSTIC_RANGE` declares exactly the fixed value `1,160p`.
- The 13 affected failure diagnostics retain their existing log operands,
  `sed -n` operation, standard-error redirection, `|| true`, and following
  failure `exit` behavior.
- The change neither adds input-derived shell evaluation nor changes any
  Parent/Framework/MRTS ownership boundary.
- A focused contract test checks the exact diagnostic command sequence, while
  live HAProxy runtime remains explicitly out of this candidate's evidence.
- A future Draft exact-head hosted analysis is required before claiming that
  the external SonarQube Cloud issue is closed.

## Implementation decision and rationale

Use a shell `readonly` variable rather than changing the failure paths or
introducing a helper function. The value is constant text controlled by the
repository, so each `sed -n "$HAPROXY_HTX_DIAGNOSTIC_RANGE" <existing-log>
>&2 || true` invocation retains the original range, operand, redirection,
best-effort diagnostic behavior, and surrounding `exit` path. This is a
literal-centralization change only.

The focused helper contract test reads the harness as source text and asserts
one declaration, no remaining repeated `sed -n '1,160p'` literal, and the
complete ordered list of 13 updated diagnostic invocations plus the unchanged
`1,40p` version-file diagnostic. It therefore guards the diagnostic interface
without executing a host runtime.

## Changed files

- `connectors/haproxy/harness/run_haproxy_htx_runtime.sh` — candidate Parent
  shell-harness literal centralization for the 13 `1,160p` failure diagnostics.
- `connectors/haproxy/harness/test_haproxy_htx_smoke_helper.py` — focused
  source-contract coverage for the declaration and exact diagnostic commands.
- `reports/audits/change-records/CR-20260728-sonar-haproxy-htx-diagnostic-s1192.md`
  and `.de.md` — this bilingual Change Record pair.
- `reports/audits/change-records/README.md` and `README.de.md` — paired index
  entries.

## Commands executed

| Executed control | Observed result |
| --- | --- |
| `rtk proxy -- sh -n connectors/haproxy/harness/run_haproxy_htx_runtime.sh` | passed. |
| `rtk proxy -- git diff --check -- connectors/haproxy/harness/run_haproxy_htx_runtime.sh connectors/haproxy/harness/test_haproxy_htx_smoke_helper.py` | passed. |
| Exact `awk` source contract for all 14 ordered `sed -n` calls (the 13 centralized failure diagnostics plus the independent `1,40p` version-file diagnostic) | passed. |
| Python source-syntax compilation of `connectors/haproxy/harness/test_haproxy_htx_smoke_helper.py` | passed. |
| Local paired Change Record structure, reciprocal language links, paired README index entries, runtime-boundary wording, and `git diff --check` | passed: both records contain 12 top-level sections. This narrow local control did not enforce the canonical Change Record heading contract. |
| Focused `tests.test_haproxy_htx_smoke_helper` execution in a disposable read-only Parent-pinned-Framework overlay | passed: 9 tests. |
| Full Parent bilingual documentation check in the corrected exact read-only candidate overlay | passed: Parent bilingual docs `OK`, repository-path references `PASS`, and Framework documentation links `OK`. The initial run failed only because this Change Record pair lacked canonical required headings; the corrected pair was rerun successfully. |
| Focused security review of the shell-only change | approved: the range remains a repository-controlled readonly value and the command operands, error redirection, best-effort diagnostics, and failure exits are preserved. |

The static HTX harness controls and the nine focused helper tests passed in the
exact read-only overlay. Neither result is host-runtime evidence.

## Security impact

This change touches a shell-command diagnostic boundary, so it received a
focused review. `HAPROXY_HTX_DIAGNOSTIC_RANGE` is static repository-controlled
text, not command substitution or request-derived data. It is passed as the
same quoted `sed -n` range at every affected call site. The candidate does not
change command operands, redirection to standard error, `|| true`, cleanup,
or error exits; it adds no shell injection path, privilege change, network
operation, or request-data handling.

## Runtime evidence

No host runtime was run. This record has no live HAProxy, HTX, SPOP, or
ModSecurity runtime evidence. The focused source-contract test validates
static diagnostic-call preservation only; it is not host-runtime evidence.

## Checks not run and rationale

- No live HAProxy runtime or full connector matrix was run for this candidate.
- No hosted GitHub Actions or hosted SonarQube Cloud analysis has been observed
  for a future exact Draft head.
- No Framework or MRTS source, delivery, or Gitlink action was run.
- No additional documentation validation beyond the successful exact read-only
  overlay was run. That overlay did not initialize or alter Framework, MRTS,
  or a Gitlink.

## Known limitations

- The original SonarQube Cloud receipt is tied to the stated base revision.
  A fresh analysis of the future Draft exact head is necessary to establish
  whether `AZ9cRysjHhV2CayPTP01` is externally resolved.
- Static source-contract coverage cannot prove live HAProxy startup, log
  availability, or all host-runtime error paths.
- This narrow Parent-only change cannot close the global SonarQube Cloud issue
  or duplication backlog by itself.

## Remaining risks

Centralizing a diagnostic range could accidentally alter a command form if a
call site were omitted or reordered. The focused contract test mitigates that
risk by asserting the complete ordered diagnostic sequence, including the
separate `1,40p` diagnostic. Hosted checks may still reveal scanner or platform
behavior not observable locally.

## Final diff and review status

At record creation, the scoped Parent source/test candidate and this bilingual
documentation pair are local worktree changes. The focused security review,
the static HTX controls, the 9-test direct overlay execution, and the corrected
full read-only documentation overlay all passed. Delivery, hosted checks, and
SonarQube Cloud closure remain pending. The record makes no claim about a
pull-request head, merge, `master`, or global quality state.
