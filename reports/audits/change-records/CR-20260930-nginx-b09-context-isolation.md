# B09 NGINX internal-redirect context isolation

**Language:** English | [Deutsch](CR-20260930-nginx-b09-context-isolation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260930-nginx-b09-context-isolation |
| Date (UTC) | 2026-09-30 |
| Base revision | e3f97d22446b8919e1d7f29de71ddf97bc735e92 |
| Delivery target | Existing Parent Draft PR #391; normal follow-up commit, no merge |

## Motivation and problem statement

The B09 real-host error-page fixture exposed a security-relevant bypass on the base revision: /origin-on internally redirects to the protected /target, but a P2 deny returned 200 instead of 403. NGINX clears its module context on the redirect. The connector access handler then recovered the cleanup-owned origin transaction, created with allowing origin rules, and skipped initialization with the target location's protected rules.

## Acceptance criteria

An enabled redirected target must initialize a transaction from its current location configuration. The existing hosted fixture retains its strict assertions: a block marker returns 403, does not reach the protected backend, and produces rule 9803911 with a Phase-2 native decision. Its legitimate control returns 200 with the target body. Disabled and enabled/allowing origins, repeated denies, and a later allowed request remain covered. Cleanup recovery remains available outside access initialization.

## Implementation decision and rationale

Only ngx_http_modsecurity_access_handler reads the raw current ngx_http_get_module_ctx value when deciding whether to initialize a transaction. It no longer uses ngx_http_modsecurity_get_module_ctx; that helper's cleanup fallback remains unchanged for request-read, filter, logging, and post-access finalization paths. An enabled redirect target therefore receives a fresh context and its own ruleset, while a disabled target preserves existing post-access handling.

The focused Python regression adds a source contract for this access-handler boundary. It supplements rather than replaces the real hosted HTTP/1 B09 fixture. The earlier /origin Sonar literal correction and existing intervention classifier are deliberately not modified.

## Security impact

The affected trust boundary is the transition from an origin location to a protected internal error-page target. A client-controlled request header can select the fixture's deny rule, but it must not make the target inherit the origin's permissive transaction. The correction restores target-location P2 enforcement without weakening worker isolation, cleanup, logging controls, CI permissions, or assertions.

## Changed files

- connectors/nginx/src/ngx_http_modsecurity_access.c
- tests/test_nginx_error_page_intervention.py
- reports/audits/change-records/CR-20260930-nginx-b09-context-isolation.md
- reports/audits/change-records/CR-20260930-nginx-b09-context-isolation.de.md

No Framework or MRTS source, Gitlink, workflow, dependency, permission, or Sonar-constant change is part of this correction.

## Commands executed

Before the native change, the new focused source contract failed because the access handler still called ngx_http_modsecurity_get_module_ctx. After the change, python -m unittest tests.test_nginx_error_page_intervention.NginxErrorPageContextContractTests -v passed. The full python -m unittest tests.test_nginx_error_page_intervention -v command reached the passing source contract but then stopped because this local Windows environment has no C17 compiler; it does not substitute a pass for the compiled classifier/P1/P2 seam.

The required real-host validation remains the exact-head GitHub workflow. Base-revision run 36708275117, job 109863649363, is the reproduced failure; a fresh successor-head result is required after delivery.

The direct bilingual-documentation and repository-path checkers reported only pre-existing absent `modules/ModSecurity-test-Framework` link targets in unchanged documentation; neither found an issue introduced by this change.

## Runtime evidence

The existing hosted fixture is the authoritative runtime proof for this scope. It uses a root NGINX master, a distinct non-root worker, private run paths, and provisioned exact-head artifacts. No new local native runtime claim is made from the source contract or unavailable Windows toolchain.

## Checks not run and rationale

Local C17 compilation, the full Python B09 seam, the Make wrappers `make check-bilingual-docs` and `make check-doc-links`, and the real NGINX fixture cannot run in the current environment because the required compiler, Make, NGINX/libmodsecurity runtime, and root-worker provisioning are unavailable. The direct documentation checkers report only the absent Framework submodule's pre-existing targets. No package installation, service change, test relaxation, or substitute runtime was used. Fresh hosted successor-head evidence is pending at the time of this record.

## Known limitations

The B09 fixture proves HTTP/1, one internal URI error-page hop, and a P2 header predicate. It does not establish named-location behavior, arbitrary recursion, body-transfer modes, response-phase behavior, other transports, or deployment coverage.

## Remaining risks

When an enabled target creates its own transaction, final logging naturally observes that target context. This focused correction does not introduce a multi-transaction audit association policy. The retained cleanup fallback continues to support post-access handling where no enabled target context is created, including a disabled target location. Hosted B09 proof is required to confirm the protected target's observable decision.

## Final diff and review status

The scope is limited to the native access-context decision, one focused regression contract, and this paired traceability record. Existing B09 host assertions remain strict. Delivery is limited to a normal follow-up commit and push on the existing Draft PR branch; no force-push or merge is authorized.
