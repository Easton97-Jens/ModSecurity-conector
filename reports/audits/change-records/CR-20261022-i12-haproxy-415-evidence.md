# Change Record: CR-20261022-i12-haproxy-415-evidence

**Language:** English | [Deutsch](CR-20261022-i12-haproxy-415-evidence.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261022-i12-haproxy-415-evidence |
| Date (UTC) | 2026-10-22 |
| Base revision | `671fb2c7a59b917ea7d51cd2f4f46bbef4843c22` |
| Target branch revision integrated before delivery | `76672071c3f7665dfde3340bef9e64271d6f6e70` |

## Motivation and problem statement

PR #415 needed a current, source-bound reconciliation of the three HAProxy I12
routes. The initial task baseline exposed nine full lifecycle PASS results; the
immediate historical ledger already contained 30. Neither incorporated the
later reviewed HAProxy 3.2.25 captures into a compact current ledger or offered
a durable content-addressed raw evidence download. The current Sonar scan also
treated Oracle source paths as JSON property names and identified bounded
maintainability and path-validation findings in the HAProxy-only harness.

## Acceptance criteria

- Assess Native HTX, SPOP request and the HTX response companion separately;
  never count one request as three host executions.
- Credit only complete host/filter/native-engine lifecycles bound to an
  original Oracle; keep ACK-only, HTTP-only, partial and negative observations
  below lifecycle PASS.
- Reconcile all 278 required IDs and all 124 original HAProxy Oracles with
  explicit unresolved lists.
- Preserve exact revision, binary, configuration, frame, client/backend,
  commit, physical sink and finish/free provenance for every new credit.
- Publish a bilingual human report, a machine-readable ledger and a
  content-addressed raw package with independently verified hashes.
- Limit repository changes to HAProxy harnesses, tests, fixtures and owned
  EN/DE/JSON evidence artifacts. Keep the central matrix, shared captures,
  generators and other connectors unchanged.
- Pass the focused HAProxy C, HTX, SPOP, mutation, documentation and ledger
  validations before normal delivery; leave the PR as Draft and do not merge.

## Implementation decision and rationale

The evidence was reviewed from sealed, route-specific host packets. Thirty-two
new qualifications are bound to product/capture revision
`0325c1d7a1c2dd85ab2ca270d494e97ee8a5b92a`; three narrower controls were built
and executed at measured revision
`671fb2c7a59b917ea7d51cd2f4f46bbef4843c22`. The narrower controls do not
transfer the complete 62-ID inventory to that later revision.

The 124-row Oracle fixture changed only its `original_source_hashes`
representation from object properties to ordered `{path, sha256}` values. The
HAProxy-local reader accepts the frozen and migrated forms, rejects ambiguous
or malformed entries and canonicalizes both to the same semantic digest
`2e9581873d5dfd6acf15b5396acddb690a0de3f71d6f1be0207542c37f2e2689`.
This removes source paths from JSON property names without changing any Oracle,
source binding or disposition.

The batch harness now accepts exactly the six fixed namespace keys before any
`/proc/self/ns` read. Small helper extractions reduce complexity while keeping
Native, SPOP and Companion observation output byte-identical to the pre-change
replays. No connector product source changed.

## Changed files

- `connectors/haproxy/harness/fixtures/i12-oracles-20261015.json`
- `connectors/haproxy/harness/i12_oracle_fixture.py`
- HAProxy-owned I12 batch, Native, SPOP, Companion and route observer modules
  under `connectors/haproxy/harness/`
- HAProxy I12 unit tests under `tests/test_haproxy_i12_*.py`
- `docs/pr-415-i12-haproxy-20261022.md` and its German companion
- `reports/testing/i12-haproxy-415-20261022.json`
- this bilingual Change Record

## Commands executed

- `rtk .../test-env/bin/python -B -m unittest -v` for all eleven
  `tests.test_haproxy_i12_*` modules — exit `0`; 156 tests passed in 8.693
  seconds.
- `rtk make ... check-haproxy-c17` — exit `0`; HAProxy C17 compile passed.
- `rtk make ... check-haproxy-htx-overlay` — exit `0`; all HTX source and
  lifecycle contracts passed.
- `rtk make ... check-haproxy-spop-event-sink` — exit `0`; 19 physical
  serialization/write/flush/close failure tests passed in 3.481 seconds.
- `rtk make ... check-i10-haproxy-callers` — exit `0`; 20 Direct/SPOP caller
  and mutation tests passed in 242.461 seconds.
- `rtk make ... check-haproxy-common-adoption` and
  `check-haproxy-c-standard-wiring` — exit `0`.
- `rtk make check-bilingual-docs` and `rtk make check-doc-links` — exit `0`.
- `rtk proxy /usr/local/bin/python3 -I .../verify-final-report-20261022.py` —
  exit `0`; 278 unique catalog IDs, 124 Oracle rows, 32 unique new PASS IDs and
  100 file hash references verified. The report is 322050 bytes with SHA-256
  `d19aa8008d78c57ab510568f8c7e59b124c5ea8aac365f453a2c96b25b102d26`.
- `rtk sha256sum -c SHA256SUMS` on the freshly extracted draft download — exit
  `0`; all 979 internal entries passed. Its independent verifier passed 974
  content objects and 1,407 source bindings.
- A repeat of the historical absolute-path selection verifier returned exit
  `1` after the later Sonar-only harness refactor because the recorded mutable
  worktree path now has new bytes. The recorded pre-refactor verification
  remains sealed; the unchanged content-addressed download verifier resolves
  and verifies the original objects without mutable paths.
- `rtk --version`, `rtk which rtk` and `rtk gain` confirmed RTK `1.0.1` at
  `/root/.local/bin/rtk`; project commands used the required proxy.

## Security impact

No production trust boundary changes. The namespace reader now rejects missing,
extra, traversal-like or absolute user-supplied keys before filesystem access
and dereferences only fixed namespace paths. Oracle source paths are strictly
validated as values with unique nonempty names and lowercase SHA-256 digests.
Sink-error tests retain fail-closed `fputs`, `ferror`, `fflush` and `fclose`
behavior. An independent scoped security review found no introduced security or
correctness regression. No validation, isolation, redaction, compiler warning
or Quality Gate was weakened.

## Runtime evidence

| Route | Required | Historical PASS | New PASS | Current PASS | Unqualified |
| --- | ---: | ---: | ---: | ---: | ---: |
| `haproxy-native-htx` | 112 | 25 | 6 | 31 | 81 |
| `haproxy-spop-request` | 94 | 3 | 17 | 20 | 74 |
| `haproxy-spop-htx-response-companion` | 72 | 2 | 9 | 11 | 61 |
| **Total** | **278** | **30** | **32** | **62** | **216** |

The original Oracle subset resolves 31/48 Native, 21/44 SPOP and 13/32
Companion rows: 65 resolved and 59 open. The 32 new PASS packets contain six
Native, seventeen SPOP and nine independently measured Companion IDs. The
accepted selection SHA-256 is
`2e497d8b32e9a786bdfca88d314e02e5e666a2ea8e9f05e2b809233891731053`.

The raw archive is 5,181,893 bytes with SHA-256
`ac9de960803803fafe923da1bc2c87ecb6ce485ac51e5580871c0d22f477fe5b`;
its manifest SHA-256 is
`8a1aefe5e5eff2474b0f23de5f08d625979ca4446bf4c70b79dcc1161da3bd47`.
Uploaded draft assets were downloaded again through GitHub's asset API before
publication and verified independently. The release remains Draft until it can
be pinned to the final checked PR commit.

## Known limitations

`I12_PARTIAL` remains the only supported status. Native has 81 unqualified
required IDs and 17 open Oracles; SPOP has 74 and 23; Companion has 61 and 19.
Unknown or chunked SPOP framing and unsupported HTTP/2 mappings remain
uninspected. SPOP remains a bounded authorization sample, not an unlimited
streaming path. Missing, wrong or stale Companion OUTCOME data, missing EOS,
unsupported Strict behavior and missing/expired correlation remain negative or
partial evidence. The parallel Companion attempt had only 10/16 successful main
requests, six `502` responses and seven unknown observations, so it receives no
lifecycle credit.

## Remaining risks

GitHub checks and the Sonar Quality Gate must be read on the exact final pushed
head. The evidence prerelease is still Draft and has no tag ref; publication,
public URL readback and tag-to-head verification occur only after that exact
head is stable. Product defects, if newly confirmed, remain work for #382/#410
and are not repaired through this evidence PR.

## Checks not run and rationale

No new private host capture was manufactured after the two measured revisions.
The 32 new qualifications stay bound to their original `0325c1d7` host runs,
while the three `671fb2c7` controls prove only their named paths. A repository-
wide all-connector matrix was not run because the authorized scope is HAProxy
only and no shared generator or connector product source changed. A public,
unauthenticated release download cannot be checked while the release is Draft;
it is a delivery gate after exact-head CI rather than a substituted local check.

## Final diff and review status

The local diff is limited to HAProxy-owned harnesses, fixtures, tests and the
owned bilingual/JSON evidence artifacts. Independent code, security and
documentation reviews found no blocking issue, no changed Oracle decision and
no lifecycle overclaim. Focused local validation is complete. Normal commit,
push, exact-head GitHub/Sonar readback and final evidence publication remain
delivery steps; no force-push, merge or master change is claimed.
