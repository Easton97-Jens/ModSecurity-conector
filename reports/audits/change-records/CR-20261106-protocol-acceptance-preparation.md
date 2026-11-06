# Change Record: CR-20261106-protocol-acceptance-preparation

**Language:** English | [Deutsch](CR-20261106-protocol-acceptance-preparation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261106-protocol-acceptance-preparation |
| Date (UTC) | 2026-11-06 |
| Base revision | `a5f697c35acb5386d2037f91dfed10ad4b469cd9` |
| Follow-up starting Parent | `adf75d05ced37ccab066b8608aed1ce297be84e3` |
| Follow-up starting Framework | `b5d8d9442d7751c04ee84f478f594fc84a236e3b` |
| Delivery | [Parent Draft PR #445](https://github.com/Easton97-Jens/ModSecurity-conector/pull/445), [Framework Draft PR #169](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/169) |

## Motivation and problem statement

Close acceptance-preparation failures using real host evidence, preserve existing
regressions and the 100 standard cases, and select the corrected Framework
through consistent native pins/projections. The continuation explicitly permits
proven product and dependency fixes. Comprehensive acceptance remains NOT_RUN.

## Acceptance criteria

The four preserved H2 regressions require causal before/after proof; selected
Apache, local HTX, SPOP/HTX companion and ext_proc H2 paths require executable
independent readers. Final committed-pair targeted runs, fresh Apache CRS and
aggregate, current hosted checks, native policy/inheritance and integrity/cleanup
must be reconciled before READY_FOR_FULL_ACCEPTANCE. Candidate evidence alone
cannot satisfy final delivery criteria.

## Implementation decision and rationale

NGINX's queued H2 reset was waiting on an unscheduled real-connection write
path while another stream remained active. The Framework versions a minimal
zero-fuzz native-source patch, bound into the normal build cache/provenance.
An independent TLS/H2 frame experiment separates server queueing from client
processing. Existing assertions and timeouts remain unchanged.

Apache's H2 Strict path marked the secondary connection aborted without sending
terminal metadata through its native connection-output chain. A held peer and
independent raw-frame probe demonstrated the missing reset. The narrow fix sends
ERROR/FLUSH metadata through that chain before the abort flag, preserving the
sealed request-producer guard and the existing HTTP/1 behavior. Native pinned
HTTPD beam handling owns the cross-thread metadata copy and stream reset.

A hardened repetition exposed an additional pinned HTTPD purge race after the
reset. A native APR interleaving control proves that neither the original path
nor a wakeup alone retires the joined stream promptly. The Framework versions
the two-part wake/pending-purge correction at the safe outer cleanup point,
preserving shutdown/abort precedence and binding patch bytes into Apache's
native cache identity. Fresh build and final live cleanup proof remain required.

Envoy ext_proc Strict now sends a late ImmediateResponse through the pinned
host. Only that profile's strict-action admission bit changes in the Common
profile registry. The service records a successful gRPC send separately from
actual downstream reset; selected native Envoy client/access evidence proves
the affected stream and healthy peer/follow-up. Runtime config accepts explicit
off/safe/strict policy. The base ext_authz profile does not inherit this claim.

The native Framework synchronizer owns Parent gitlink/lock/workflow projections.
MRTS remains `ee2174431c4edf97e66afe32558ce8454deb2397`; protected provenance,
Python/Go and unrelated toolchain pins remain unchanged. No merge is performed.

The reviewed ignored local LLM note remains byte-identically archived and
classified as local non-normative material. The 27 Parent, 21 Framework and
12 MRTS policy digests remain unchanged. The separate 84 legacy inventory
findings remain visible; no unchecked digest refresh erases them.

## Changed files

- Selected Framework gitlink, central version lock and 22 native workflow projections.
- Apache H2 terminal metadata dispatch, profile-qualified capabilities and paired guide.
- Envoy ext_proc processor, exact profile admission, runtime config materializer,
  profile-qualified capability metadata and paired source/connector guides.
- Generated configuration reference through its Framework-owned generator.
- This paired Change Record; local plans and external evidence are not committed.

## Commands executed

Commands use RTK and explicit selected Parent/Framework roots and revisions.
Exact commands, complete output, run identities and absolute evidence paths are
retained in the external follow-up report.

| Procedure | Observed result |
| --- | --- |
| Four unchanged H2 regressions at starting pair | 4 FAIL, retained as before evidence |
| Independent verified TLS/H2 no-PING/PING frame probes | Queued server output proven; no-PING reset about 12 s before, about 15 ms after |
| Fresh patched native H2/H3 builds | PASS; four regressions and eight neighbors PASS in focused candidate runs |
| Envoy untagged and real-libmodsecurity-tagged Go suites | All eight packages PASS in each selection |
| Envoy candidate real H2 cases | 8 PASS / 24 transactions; native target cleanup before peer release |
| Local HTX candidate real H2 cases | 8 PASS; writer-failure cleanup and corruption controls PASS |
| SPOP/HTX companion candidate real H2 cases | 8 PASS; original owner EOS rule and actual native stream action joined without invented MRC1 fields |
| Profile metadata contracts | 39 tests PASS |
| Apache fresh build, CRS and aggregate | Final native results retained in follow-up report; not inferred from failure-artifact upload |
| Final pins, policy/inheritance, units/generators and current-head CI | Required final readback retained externally |

## Security impact

Strict remains constrained to the selected profile and actual host action.
Original engine decisions, successful service sends and wire observations stay
separate. TLS verification, evidence bounds, source admission, UDS ownership,
process isolation, compiler warnings, scanner coverage and Gate rules remain.
No administrative rule changes, local Sonar setup/scan, or MRTS writes occur.

## Runtime evidence

Earlier sealed 21-PASS/4-FAIL evidence remains immutable. The new follow-up root
retains baseline reproduction, native dependency patch/build identities,
independent frame proofs, profile-specific access/Common/cleanup observations,
Apache failure diagnostics and fresh-build receipts. Final source-pair hashes,
counts, cleanup, CI and integrity manifest belong to the external report rather
than a self-referential commit SHA in this versioned record.

## Known limitations

Ext_authz, ForwardAuth and native profiles remain separate claims. SPOP's current
NOTIFY ABI needs explicit zero Content-Length for this empty-H2-body fixture;
forwarded rule metadata is not invented. Traefik modern/Strict paths require
separate qualification. Stock/patched lighttpd retain their H1 contract.

## Remaining risks

Current required hosted Sonar disposition and Gate results must be read back
at the exact delivered Framework head. Individual local reviews do not alter
server disposition. Existing independent C++20/C++23 advisory failures and the
84 legacy findings remain visible separately from new regressions.

## Checks not run and rationale

Comprehensive acceptance is NOT_RUN by user instruction. No merge, administrative
settings change, local Sonar install/start/auth/scan or MRTS mutation is authorized.
No global readiness is inferred from this source record.

## Final diff and review status

Focused normal commits continue the existing Draft PRs. Final review checks
product scope, generated pins/reference outputs, unchanged standard inventory,
protected pins and policy solution. Actual final full SHAs, terminal CI and
requirement dispositions are recorded in the reconciled external report.
