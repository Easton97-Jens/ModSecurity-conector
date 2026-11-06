# Change Record: CR-20261106-protocol-acceptance-preparation

**Language:** English | [Deutsch](CR-20261106-protocol-acceptance-preparation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261106-protocol-acceptance-preparation |
| Date (UTC) | 2026-11-06 |
| Base revision | `a5f697c35acb5386d2037f91dfed10ad4b469cd9` |

## Motivation and problem statement

Select the separately implemented Framework preparation tests through a
consistent Parent gitlink, central version lock and native workflow projections.
Resolve the local policy inventory discrepancy without publishing a private
instruction or broadening inheritance. This change does not fix connector code.

## Acceptance criteria

The reviewed Framework candidate must be selected consistently, retaining the
MRTS revision and unrelated toolchain pins. Native primary-publication checks
must agree with the trusted Parent base. Policy inventory and inherited digests
must be reported separately. Targeted host results, failed requirements and
cleanup must remain visible. Exact final committed-pair host verification and
reviewable remote delivery remain outstanding; global preparation is NOT_READY.

## Implementation decision and rationale

Select Framework `fa444236fa3b00c91ba94de49f69f52101087087`; retain MRTS
`ee2174431c4edf97e66afe32558ce8454deb2397`. Use the native fixed projection
registry with extracted candidate `common.sh` and official Git object data.
The protected broker provenance pin remains unchanged; ordinary Framework
references in its workflow are updated only by the native projection contract.
Python 3.15.2, Go 1.27.3 and all MRTS values remain unchanged.

The ignored 194-byte local LLM note duplicates existing agent profiles and is
not shared normative policy. After review, a byte-identical archive and local
classification resolve its inventory treatment. The proposed tracked reference
was rejected because the private file would be missing from clean clones. The
27 Parent catalog, 21 Framework and 12 MRTS inherited policy digests remain
unchanged; no blanket child inheritance or checksum substitution was introduced.

## Changed files

- `modules/ModSecurity-test-Framework`: selected Framework gitlink.
- `ci/tooling/project-versions.lock.json`: only `framework_sha` changes.
- 22 native workflow projections under `.github/workflows/`.
- This English/German Change Record pair.

Generated compiler documentation, if required, must be updated through its
native generator; no generator output is hand-edited by this record change.
Local policy classification/archive is local evidence, not a versioned policy.

## Commands executed

`P` denotes the task-owned Parent worktree, `F` its selected nested Framework,
`PYTHON` the selected task-owned Python 3.15.2 interpreter. The Parent validation
environment was created without pip or package installation. `COMMON` denotes the reviewed extracted candidate source; official object data
comes from the selected nested Framework by default. Absolute paths and complete invocation receipts remain external.

| RTK command or procedure | Result |
| --- | --- |
| `rtk bypass "$PYTHON" ci/tools/sync-framework-component-versions.py --sync --repo-root "$P" --framework-common "$COMMON" --framework-sha fa444236fa3b00c91ba94de49f69f52101087087 --mrts-sha ee2174431c4edf97e66afe32558ce8454deb2397` | PASS; native fixed projections synchronized |
| Same native invocation with `--check` instead of `--sync` | PASS; no projection drift |
| Same native inputs with `--verify-primary --base a5f697c35acb5386d2037f91dfed10ad4b469cd9` | PASS; trusted-base publication reconstruction |
| `rtk bypass "$POLICY_PYTHON" .codex/bin/validate-codex-inheritance.py --check --all` | PASS; current native inventory/inheritance |
| `rtk bypass "$POLICY_PYTHON" .codex/bin/validate-v32-structure.py` | PASS; V3.2 structure |
| Separate legacy audit inventory procedure | FAIL; 84 old-contract findings retained in raw evidence |

`POLICY_PYTHON` denotes the earlier Parent-owned Python 3.14.4 interpreter;
a final repeat with the task-owned 3.15.2 interpreter is separate evidence.

Documentation verification used the existing Framework-owned Python 3.15.2
interpreter (`FW_PYTHON`), without installation:

| RTK command or procedure | Result |
| --- | --- |
| `rtk bypass "$FW_PYTHON" ci/tools/new-change-record.py check` with explicit absolute `TEST_ROOT`, `CONNECTOR_ROOT` and Framework `PYTHONPATH` | Exit 0; structure-only Change Record contract |
| `rtk make check-bilingual-docs check-doc-links FRAMEWORK_ROOT="$F" PYTHON="$FW_PYTHON" FRAMEWORK_PYTHON="$FW_PYTHON"` | Exit 0; bilingual, repository paths and links passed |
| `rtk bypass git diff --check` | Exit 0; whitespace passed |

Initial record-check attempts with missing/relative source context failed;
the explicit absolute source context corrected these invocation errors.

Current native consistency and the legacy inventory result are distinct facts;
the latter was not suppressed or reclassified as a pass.

## Security impact

No product security fix, global rights/configuration change, authentication
change, MRTS write or protected broker authorization change. No validation gate
is weakened. Local Sonar remains suspended; existing GitHub Sonar/CodeQL
requirements remain intact. No credentials or raw sensitive material are copied
into the record.

## Runtime evidence

Framework targeted host evidence evaluated all 25 new IDs: 21 PASS / 4 FAIL;
25/25 cleanup verified. Failures are `h2_phase4_strict`, `h2_server_rst_stream`,
`h2_upstream_reset`, `phase4_strict_http2_stream_reset`. Eight adjacent existing
H2/H3 negotiation/P2/P3/P4 host cases passed. The 15 new contract unit methods,
29 adjacent unit regressions and 21 negative mutations of real observations
passed their expectations; every mutation was rejected.

These observations bind the recorded source bytes and artifacts; exact final
committed Parent/Framework pair host verification is forthcoming. They do not
prove that final pair, every logical profile, or comprehensive acceptance.
Full acceptance is NOT_RUN and preparation is NOT_READY.

## Known limitations

Four mandatory H2 reset expectations fail with the peer-isolation contract
preserved. No product correction is included. Required modern Apache H2,
HAProxy HTX H2/SPOE companion H2 stream-shutdown and Envoy ext_proc H2 executable
paths remain open. Current lighttpd stock/patched selected profiles remain
H1-scoped under their existing contract; no new unsupported marker is added.

## Remaining risks

The H2 reset behavior and remaining profile runner obligations prevent
READY_FOR_FULL_ACCEPTANCE. Legacy inventory still reports 84 old-contract
findings. The final committed pair must be verified before making runtime
claims about that pair. Source-matched earlier evidence cannot replace that check.

## Checks not run and rationale

Comprehensive acceptance is explicitly NOT_RUN. Local Sonar install/start/
authentication and scanning are suspended by the user. Exact final committed-pair host reruns were not yet observed at this record
update. Native compiler-guide generation completed with exit 0 and unchanged
output bytes using the proper source context. No remote PR or CI checks ran: automatic approval review rejected
the Framework push twice; fresh user approval is required for that egress action.
No merge or administrative rule change is authorized or performed.

## Final diff and review status

This is the concrete local review record for the Parent candidate. Exact local
commit SHAs, remote branch identities and delivery receipts are retained in
external repository-scoped evidence. No fabricated PR link or successful push/
CI status is asserted. Delivery remains blocked on the rejected Framework push;
the rejection and required fresh user approval must be surfaced before egress.
The local Parent preparation remains reviewable while that approval is pending.
