# Apache final physical-evidence review procedure

**Language:** English | [Deutsch](README.de.md)

`final_review.py` adds a conservative Root review procedure to the existing
Apache batch extractor and unchanged shared lifecycle validators. It runs no
host test. Its synthetic tests do not constitute host evidence.

The CLI requires explicit paths and SHA256 digests for the immutable baseline,
case plan, unsigned 155-case index, expected identity and admission spec, plus
the retained attempt directory and a new output directory. See
`rtk proxy python3 -B reports/audits/apache-i12-20261020/final_review.py --help`.
Use the repository Python environment for actual execution. An optional separate
oracle review file also requires its SHA256. The expected identity JSON requires
`run_id`, full `parent_sha`, `framework_sha`, `mrts_sha`, and full SHA256 values
`apache_sha256`, `module_sha256`, `sdk_sha256`. These values must describe the
actual sealed product/run; they are not inferred from a candidate.

Without `--approve-supported-families`, the procedure emits decisions with null
outcomes. The explicit switch invokes only the registered bounded-family review.
It does not resolve an oracle or authorize a new test environment. The procedure
requires equality with fresh extraction from the retained physical attempt and
spec, all 35 applicable shared measurement roles, every required extractor check,
an actually completed case contract, exact product/run identities, and explicit
wire, backend, rule, native phases/appended-byte counts, EOS, physical commit,
finish/free, descriptor/process cleanup and independent control predicates.
The original expected oracle and earlier failures remain unchanged.

The registry covers four exact request IDs: empty, single chunk, CSV and EOS
once. Content-Type present/missing and charset present/missing remain null:
wire fields alone do not prove native mapper/header/MIME propagation, and the
existing generic MIME observation is not a complete independent proof for those
four obligations. CSV means raw request
bytes; it makes no CSV-specific engine processor claim. Other families remain
null even when every structural role is present. Each registered request ID has
the explicit lifecycle oracle phase 2, bound to exactly one actual successful
`native_process_request_body` return in the physical native-phase observations.
The plan's P1 sentinel rule 91041950 is checked separately against the native
audit and physical Common event; its rule phase is not the lifecycle oracle
phase. Additional oracle keys or scope semantics
that this procedure cannot evaluate remain unknown. If a `scope` key is supplied,
only the exact `SUPPORTED_ORACLE_SCOPE` string in the source is supported; a
different scope requires its own independent implementation and review.

Ordering is checked from the existing physical native API JSONL, which retains
both enter and return edges. Each P2/P4/finish/logging/cleanup/retirement operation
must have exactly one matching actual call, increasing native sequence and
monotonic times, bound to the principal PID/run/allocation. For a nonempty request,
APR EOS must precede P2 entry. For the empty request, P2 return must precede the
first empty APR EOS, whose observation must report `request_body_processed=1`.
Response APR EOS must precede P4 entry and follow P2 return. Prefix delivery and
physical socket writes may precede P4; the logical commit flag must precede
output. Terminal release must follow successful P4 return and report response
body processed and EOS released. Common finish, successful native logging,
Common cleanup, native free and association retirement must follow the latest
of P4 return, terminal release return and physical socket return, in that order.
A count alone is insufficient. Missing or inconsistent ordering evidence leaves
the case unqualified.

Configuration and pre-native parser controls always point to the separate
`review_controls.py` procedure and its explicit approval input. This procedure
does not import their approvals. A Root reviewer can supply their independently
validated packets alongside this procedure's packet index to the Apache ledger.

`decisions.json` retains all 155 original rows, individual `PASS`/`FAIL`/null
predicates, physical references, the original oracle, separate nullable oracle
decision, and a per-case registry/gap inventory. A failed or unknown predicate
prevents an approved packet. `reviewed-packets.json` lists only packets accepted
by the unchanged shared validator before publication. `i12_complete` stays false.
Input files and direct physical references are hash checked before review and
revalidated before publication, including control receipt, process and response
files and normalized oracle retest measurements. Referenced JSON files are
immutable leaves; their arbitrary contents are not traversed as a reference
graph. Typed physical-file records are checked without interpreting logical
container paths as host references.

Eight review procedure source files are bound before repository review modules
are imported. Validators are compiled from source without using repository
pycache files. The procedure rechecks all eight sources before publication and
includes their physical references in its output inventory.

A read-only inventory of the executed `case-plan.json` (SHA256
`4017b6ae7919958b554f103062ec0e8588bdb009c08dbc26b9c6422e38f065c1`)
covered all 155 IDs: 4 registered bounded request IDs, 4 missing independent
native header/MIME propagation proofs, 14 separate typed controls,
24 physical fault families needing their own semantics, 24 special-operation
families needing their own semantics, 74 cases needing independent expectation
and family review, and 11 cases with planned expectations but no complete
independent family predicate. These are implementation/gap categories, not test
results or newly qualified PASS cases.

Validation: `rtk proxy <repository-python> -B -m unittest discover -s tests -p
test_apache_i12_final_root_review.py -v`. Mutation negatives include complete
35-role packets with wrong rule, status, backend count/body bytes, native append
bytes, phase, EOS, commit order, finish/free, cleanup, neighbor and native
allocation identity, oracle phase/scope, and absent independent oracle/evidence.
The focused batch/final-review suite completed 52 tests with exit 0 and two
explicit skips. Further negatives cover ambiguous observer finals, empty EOS
ordering, terminal release after finish, invalid socket brackets/accounting,
procedure-source mutation before publication and frozen retest measurements.
