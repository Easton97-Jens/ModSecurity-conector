# Change Record: CR-20261015-traefik-companion-method-metadata

**Language:** English | [Deutsch](CR-20261015-traefik-companion-method-metadata.de.md)

Component regression evidence for two bounded Traefik fixes. Integrated host acceptance remains a separate PR #413 obligation.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261015-traefik-companion-method-metadata |
| Date (UTC) | 2026-10-15 |
| Base revision | `9980eb049dde0643da6a4f04e3b6712801b670b3` |

## Motivation and problem statement

The qualified historical Companion P4 Safe event requested deny403 and correctly applied log_only after commit, but omitted late-intervention metadata. Separately, the pinned Traefik forwardAuth implementation defaults its authorization method to GET; the checked-in templates did not enable method preservation.

## Acceptance criteria

Validated committed P4 disruptive OUTCOME events retain their late flag and actual configured policy mode. Allow, precommit, malformed/duplicate OUTCOME and technical errors remain distinct. ForwardAuth preserves the original method while regenerating trusted forwarding metadata with `trustForwardHeader: false`. Authorization-response capacity remains unchanged.

## Implementation decision and rationale

Annotate the retained MRC1 decision only after outcome sequence and payload validation, using actual committed, response-EOS, P4 and disruptive-decision state. Runtime continues to select the policy mode. Native MSE1 provides an independent comparison. Enable `preserveRequestMethod: true` in both templates and the runtime configuration producer; reject missing, disabled or ambiguous method/trust settings in its validator. The pinned upstream implementation is Traefik 3.7.13 commit `fc92cc118a0557a029c7019d5ee06665127b0f13`, `pkg/middlewares/auth/forward.go`.

## Changed files

`common/runtime/response_companion_transport.c`; both forwardAuth dynamic templates; `runtime_smoke.py` and `start-smoke.sh`; paired Traefik READMEs; `test_traefik_forwardauth_p2_contract.py`; new Companion metadata Python test and three C probes; this EN/DE record. No Framework/MRTS files or gitlinks change.

## Commands executed

`rtk proxy env CODEX_RUN_ROOT=<external-run>/product python3 -B -m unittest -v tests.test_traefik_i12_companion_metadata`: 11 PASS. The public MRC1/real-SDK regression failed before the fix in Safe and Off; three metadata/policy mutations and an annotation-before-admission mutation were detected. Eighteen adjacent MRC1/I10/native event contracts passed. `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_traefik_forwardauth_p2_contract tests.test_traefik_runtime_smoke_security`: 35 PASS, two optional real-host loader tests skipped because their explicit host prerequisite was absent. The new method contract failed seven subcases against the previous helper. Exact commands, exits, source hashes and outputs are retained in the run receipts. Root integrated verification is recorded separately.

## Security impact

No protocol, enforcement, capability or public API changes. Existing frame admission precedes annotation. Client forwarding headers remain untrusted; `trustForwardHeader: false`, request sample limits and `maxResponseBodySize=32768` are retained. Strict profile admission is not relaxed. Per-worker ownership and cleanup remain unchanged.

## Runtime evidence

The immutable historical FAIL and physical JSONL/audit proof are retained under the original revision. Fresh component probes execute the actual SDK, MRC1 client/server and JSONL recorder; they prove the metadata regression rather than a live Traefik lifecycle. External run: `i12-traefik-acceptance-20261015`, `product/companion-metadata-final-manifest.json` and `method-uri/{before,after}.json`. A new integrated host retake must qualify the same original ID after normal #382 → #410 → #413 synchronization.

## Known limitations

This product patch does not qualify the 280 Traefik original IDs. Host delivery, native EOS, finalization/free and configuration applicability require their own physical evidence. Method-preservation compatibility with older Traefik releases is not established.

## Remaining risks

Root verification also passed: all three Go modules with `go test -mod=readonly -count=1 -race ./...` and `go vet -mod=readonly ./...`; 53 focused tests (two optional host-loader skips), 59 broader native/security/error contracts (two capability skips), native engine-service/UDS tests, Common security/SDK/flow checks, Change Record structure and EN/DE/link checks with a private read-only Framework mount. Initial long-socket-path failures and missing explicit SDK-path setup are retained separately; short private paths and the installed SDK passed the retakes. Exact receipts: `checks/product-*.json` in the external acceptance run.

The final integrated host matrix and exact-head CI/Sonar results remain separate acceptance requirements. The historical #382 Gitleaks problem remains independent; no history rewrite or exception is introduced.

## Checks not run and rationale

The two optional host-loader tests require the admitted nonroot private host environment and will be repeated there. Full Traefik I12 qualification, final hosted analysis and durable raw-evidence publication are owned by the continuing #413 work rather than claimed by this component record.

## Final diff and review status

An independent read-only source review found no actionable issue after moving annotation behind admission. `rtk proxy git diff --check` passed. Normal commit/push and integration are authorized; no PR merge, force push, rebase or master change is authorized or claimed.
