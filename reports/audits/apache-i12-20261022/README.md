# Apache I12 native-host campaign — 22 October 2026

**Language:** English | [Deutsch](README.de.md)

The current campaign captured a principal or control execution for each of the
155 Apache I12 requirements. Independent review qualifies **four complete native
lifecycle PASS cases; 151 outcomes remain null/open**. `i12_complete` is false.
This report grants no release or merge approval. Earlier results remain in the
[15 October report](../../../docs/i12-apache-native-evidence-20261015.md); their qualifications do not
automatically transfer to this product/run.

The machine-readable [case ledger](case-ledger.json) preserves the exact approved
155-case decisions, original oracles, individual predicates, gaps and physical
references. The [execution index](execution-index.json) preserves the exact U6
unsigned extraction. The [evidence index](evidence-index.json) supplies artifact
hashes and the campaign summary. An observed execution, a completed case contract
and a qualified PASS are separate facts.

## Product, review and execution identity

| Binding | Value |
| --- | --- |
| Executed product source | `57e94983e808bcc4c1ca4f5fcf9745f6dc9d4a38` |
| Published reviewer source head | `de23f2fa4b490c66f15ac97f2646434351f05c5e` |
| PR target head | `76672071c3f7665dfde3340bef9e64271d6f6e70` |
| Framework pin | `99a7985c1be92a2297b1b59208f64df6768f2cbf` |
| MRTS pin, identity metadata only | `8a6bb546c4c81d8ffc7be801dceac60c6925685f` |
| Run ID | `apache-i12-batch` |
| Retained attempt | `attempt-1792695566065515062` |
| Apache 2.4.66 binary SHA256 | `6e9f25c01b14cf5fb3450fdbd268d784b1d38e377a523a345dd406a4055d81ff` |
| Observed connector module SHA256 | `6d8b7bb5fb4424e0a5e2aa90f629e92efe4713faa7a387fdc62473771794daf8` |
| libModSecurity 3.0.14 SHA256 | `32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407` |

The retained physical evidence is under
`/var/tmp/codex/ModSecurity-conector/runs/i12-apache-414-acceptance-20261015/`.
The runtime controller/driver returned exit 0, with no timeout, 155 stdout rows
and a duration of 1046.93 seconds. Its cleanup checks passed. The execution kinds
were 141 `host_http`, ten `configtest` and four `host_pre_native_rejection`.
All 155 unsigned rows report `execution_observed=true`; the applicable lifecycle
contract completed in 115 rows and failed in 26. That predicate is absent/not
applicable for the 14 typed controls. Exit 0 does not override those case results.

## Qualified results and original oracles

The four independently approved full lifecycle cases are:

- `I12::apache-native::NEED-request-empty`
- `I12::apache-native::NEED-request-single-chunk`
- `I12::apache-native::NEED-request-csv`
- `I12::apache-native::NEED-request-eos-once`

For each of these four, the approved packet binds all 35 applicable physical
roles to the principal case, with native observations bound to the same PID,
run and native allocation. The reviewer separately
checks the P1 sentinel rule, successful native request-body processing, body
append counts, response processing, APR EOS, logical commit, physical delivery,
finish, native logging, cleanup, free and association retirement. Nonempty
request EOS precedes P2; for the empty request, successful P2 return precedes
the first empty APR EOS and that EOS reports the body as processed. Response EOS
precedes P4. Prefix/socket delivery may occur before P4, while the logical
commit flag precedes output; terminal release follows successful P4, and cleanup
follows P4, terminal release and the physical socket return. Follow-up and
neighbor controls are independent physical requests.

This bounded proof does not transfer to ProcessPartial, native Reject,
transport truncation, MIME/charset mapping or other body/chunk families. Those
rows retain their individual null results and missing predicates.

The unchanged shared lifecycle validator accepted all four reviewed packets.
The shared ledger reports four fresh executed/full lifecycle PASS cases and
four resolved original open oracles out of 54; **50 original open oracles remain**.
The source-backed oracle review and the physical lifecycle qualification are
separate requirements. Original expectations and previous failure evidence are
retained; changing an expectation alone never creates a PASS.

The 155-row review inventory contains 74 cases needing independent expectation
and family review, 11 needing additional family predicates, 14 typed controls,
24 physical fault cases, 24 special-operation cases, four registered request
cases and four missing independent native header/MIME propagation proofs.
These categories describe review coverage and gaps, not additional PASS results.

## Remaining evidence and contradictions

None of the ten configuration or four pre-native controls qualifies in this
campaign. All ten configuration process receipts lack eight required binding
fields and independent expectation sources. The unsafe-event-path case actually
reports `Syntax OK`, contradicting its rejection oracle. The invalid-size and
two scope cases reject an unknown directive, which does not prove their intended
configuration semantics.

Pre-native cases 017, 018 and 020 return HTTP 400 but lack the required Apache
diagnostic and contain duplicate native sequences. Case 019 returns HTTP 500,
with native allocation, P1, finish and cleanup plus proxy diagnostic `AH01093`;
it does not prove pre-native rejection or the original HTTP 400 expectation.
These are observed contradictions or missing proof, not approved product fixes.

Duplicate-header qualification remains open. Apache 2.4.66 Core source supports
the version-bound HTTP/1.x APR merge value `one, two`; the current review has not
approved the complete independent wire/Core/connector-mapper/native-engine
chain. The original oracle and failure remain preserved. The five known physical
sink scenarios—invalid event path, `/dev/full`, non-writable sink, closed
descriptor and ENOSPC—were rerun. Their current review category remains
unqualified; a run does not establish all required APR returns, host actions,
client behavior, physical JSONL, cleanup and recovery observations.

The fresh physical observations for all five have the same client and recovery
shape: the main client exited 0 with HTTP 500 and a 571-byte entity, its backend
count was zero, and separate follow-up and neighbor clients each exited 0 with
HTTP 200, three entity bytes and one backend request. Common and native cleanup
were each observed once, no descriptor was added across the main request, and
the controller reported no surviving namespace process or outside-mount leak.

| Fault | Fresh physical boundary | Contract/review limit |
| --- | --- | --- |
| Invalid event path | No APR call was captured | Independent Common/POSIX first cause and native rule `120016` join are missing |
| `/dev/full` as configured sink | No APR call was captured | Same missing first-cause/rule join |
| Non-writable sink | No APR call was captured | Same missing first-cause/rule join |
| Closed descriptor | `apr_file_write_full` returned 9/`EBADF`, 0 of 1067 bytes; close returned 9 | Executed case contract completed, but no independent physical-fault family approval exists |
| Physical ENOSPC | `apr_file_write_full` returned 28/`ENOSPC`, 0 of 1065 bytes; close returned 0 | Executed case contract completed, but no independent physical-fault family approval exists |

All five have zero Common-finish calls and one native logging call in the
current capture, so none is promoted to full lifecycle PASS. The absence of an
APR row for the first three is retained as missing evidence rather than filled
from the historical campaign.

Further qualification requires family-specific independent review and, where
the current shared producers lack required typed observations, a separately
scoped integration. Missing observations remain null. No productive Apache fix
is approved by this evidence report.

## Validation and authorization boundary

| Check | Observed result |
| --- | --- |
| Full Apache I12 discovery | 387 tests, exit 0; five explicit skips |
| Focused batch/final reviewer | 52 tests, exit 0; two explicit skips |
| Native/helper regressions | 67 tests total, exit 0; one root-DAC skip |
| Shared lifecycle ledger regressions | 40 tests, exit 0 |
| Python compilation and `git diff --check` | exit 0 |

The focused negative tests include ambiguous observer finals, empty-body EOS
ordering, terminal release after finish, invalid physical socket observations,
review-procedure source mutation and immutable retest references. Synthetic
tests validate reviewer behavior; they add no native-host PASS cases.

The TAC query at `2026-10-22T20:59:23.107554+00:00` returned `granted`, `tac1`, source
`user`. This campaign treats that as the stated DrayTek-Blue limit and performs
defensive test, build and evidence work in the authorized private environment.
No missing security authorization blocks the work reported here. The remaining
limits are missing or contradictory evidence and separately scoped shared
producer work. Offensive expansion was not performed or marked complete.
