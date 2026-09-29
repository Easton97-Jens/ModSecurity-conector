# Change record: reported findings — unverified patch draft

**State:** proposed source changes; no tests, build, patch-application check or runtime execution performed.
**Base:** `d56af0856507eb048987974d3960e301e7c24371`.
**Scope:** B09, B13 and C07 only. This is not a closure of the complete scan inventory.

## Proposed behavior

- **B13** (`csf_d60ac4261fdf382b0cdc51bf`): reserve the header-value maximum plus one NUL byte for the original-URI override. A present empty, non-origin-form, oversized, NUL-containing or uncopyable authoritative value returns an invalid result, not another header or `/authorize`. The caller returns HTTP 400 before invoking Common. The existing fallback for absent metadata is retained. This does not implement endpoint authentication or general header propagation.
- **B09** (`csf_110c7b683d38cd566861364f`): classify a positive intervention as active even during an error-page request. Only an inactive result can use the existing bypass path. Negative error handling and ordinary allow behavior are retained.
- **C07** (Cloud finding `8d2cfdfbd7ac819198af08de2ec1a8d4`): in the stock-lighttpd OFF branch, preserve the engine decision but record host action `log_only`, the original response status and transport result `log_only`. Propagate recording failure rather than unconditionally reporting success. This does not withhold response bytes or fix B07.

## Regression material

`tests/test_reported_security_regressions.py` adds isolated C-helper tests for B09/B13 and source-contract checks for the B13 caller and C07 OFF branch. The C-helper tests use actual function bodies with minimal surrounding test types; they do not run a real parser, proxy or ModSecurity host. Missing `cc` skips the compiled checks rather than producing a successful execution result.

The corresponding Framework draft adds synthetic normalizer cases for C07 and pre-commit evidence boundaries B06/B07. A normalized synthetic record is not a host-runtime result.

## Remaining acceptance work — not executed

- Build the affected C translation units in supported host configurations.
- Run the proposed tests and existing relevant suites in the repository's prescribed environment.
- B13: exercise 8,191 / 8,192 / 8,193-byte targets through the real proxy, plus present invalid preferred metadata and absent metadata controls.
- B09: exercise an allowed original route and an error-page target denied by an actual rule. Observe the content-handler invocation and recursion behavior. The classification change alone is not a demonstrated recursion-safe full host fix.
- C07: observe a real upstream HTTP 200 and P4 deny/status:403 under explicit OFF and omitted/default mode. Verify delivered status/body and emitted host-action fields separately.
- Check source-window patch applicability at the exact base. No complete local checkout was available when authoring the patch.
- Keep all findings open until their own acceptance conditions are met.

## Boundaries and compatibility

Invalid present URI metadata now rejects instead of falling back; this is intentional. The direct request-target size setting is unchanged.
No changes to P2/P4 streaming architecture, default phase4 mode, rules, dependency pins, CI privileges, scan severity, historical closure states, Parent Framework gitlink or MRTS.
No branch, commit, push, merge or online PR is created by this file.

Only the local package carries the complete source-record mapping. Do not automatically publish raw scans, exploit payloads or personal metadata.
