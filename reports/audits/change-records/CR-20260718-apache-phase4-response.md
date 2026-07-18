# Change Record: Apache Phase-4 response enforcement

**Status:** Local remediation, focused native runtime validation, and Codex
Security revalidation are complete. Delivery is pending on a Parent-only Draft
PR; no commit, push, pull request, CI, CodeQL, SonarQube Cloud result, or merge
is claimed by this record.

**Language:** English | [Deutsch](CR-20260718-apache-phase4-response.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260718-apache-phase4-response |
| Date (UTC) | 2026-07-18 |
| Base revision | c8ca0d92b630c18232b881855c4f5d1482568ea6 |
| Scope | Parent repository only |
| Related finding | FND-PARENT-0038 |
| Framework / MRTS state | read-only, clean at cdc91a398d6c156eaff927d742b23018a3817fb6 / 13aa91291adea12d5c607fdd165d010fcfb1da78 |

## Motivation and problem statement

Apache could forward response buckets before libModSecurity ran the EOS-only
Phase-4 RESPONSE_BODY decision. A disruptive deny could therefore occur after
the protected bytes had passed the downstream commit boundary. The retained
pre-fix internal-redirect reproducer shows the direct target denied by rule
2190411 while the redirect returned HTTP 200 and the response marker.

This record remediates only the Apache/libModSecurity Phase-4 response path.
It does not alter another connector, Framework, or MRTS.

## Acceptance criteria

The broken-control chain was:

~~~
upstream response bucket
  -> MODSECURITY_OUT append/forward
  -> downstream ap_pass_brigade before EOS
  -> msc_process_response_body + process_intervention at EOS
~~~

Attacker prerequisites are a reachable response whose body matches a deployed
disruptive Phase-4 SecRule RESPONSE_BODY rule before EOS; normal internal
redirects and multiple brigades make the old escape easier to demonstrate. No
local privilege is assumed.

The security invariant is that a response byte which Phase 4 can consider must
not reach downstream before msc_process_response_body and the resulting
intervention have resolved. The last blocking point is therefore the first and
only downstream release, not sent_bodyct-like Apache state that can be marked
upstream of the connector.

The smallest complete enforcement boundary is an EOS gate for every response
that reaches the Apache output filter. libModSecurity's C API does not expose a
safe query for the effective SecResponseBodyMimeType decision. Narrowing the
gate by the connector's legacy MIME list, forwarding an inspected prefix, or
releasing an uninspected tail would recreate the bypass.

The completed repair must therefore demonstrate all of the following:

- a Phase-4 deny suppresses the matching body before the first downstream
  commit;
- allow and log-only retain one complete normalized response, including empty
  and multiple-brigade responses;
- late output, pre-commit errors, unsafe redirects, and cleanup cannot leak
  held original bytes or duplicate EOS; and
- native Apache H1/H2, focused CRS/MRTS controls, and current-source security
  checks produce retained evidence without changing Framework or MRTS.

## Implementation decision and rationale

- The output filter normalizes every pre-EOS brigade and holds it with
  ap_save_brigade while appending the complete bounded body to libModSecurity.
- At EOS it runs msc_process_response_body and process_intervention before the
  only release. Allow restores the Phase-3 snapshot and releases saved brigades
  once; deny discards the original brigades and enters the terminal error path.
- Connector-owned release state and observed commit state replace sent_bodyct
  as the evidence of a connector release.
- MODSECURITY_PHASE4_GUARD remains in the protocol filter chain to discard
  producer output after EOS or terminal deny, including a second body or EOS.
- Oversize, append, bucket-read, setaside, missing-context, and unsafe
  redirect conditions fail closed before original bytes are released.
- The existing unread-request-body route uses that same pre-commit terminal
  bridge only when a Phase-2/error response reaches MODSECURITY_OUT. This is a
  necessary compatibility part of the new output boundary: the protocol guard
  otherwise changes error emission underneath that route. It does not alter
  Phase-2 rule evaluation or add a second response body path.
- A valid first Apache error bucket uses the pre-commit terminal bridge.
  Apache-core-marked local ErrorDocument emission is bounded to one hop while
  terminal output is emitting; ordinary r->prev redirects fail closed because a
  native transaction cannot safely rebind to the target request.
- Cleanup discards held brigades. The patch does not disable Phase 4 and does
  not reinterpret deny as log-only.

Legitimate response delivery after an allowed EOS remains intact. Progressive
delivery before a Phase-4 decision is intentionally unavailable for this
security boundary; the implementation preserves response semantics after the
decision rather than exposing bytes before it.

## Changed files

Production and Apache harness:

- connectors/apache/src/mod_security3.c and mod_security3.h
- connectors/apache/src/msc_filters.c and msc_filters.h
- connectors/apache/src/msc_config.c
- connectors/apache/src/msc_utils.c and msc_utils.h
- connectors/apache/harness/apache_smoke.conf
- connectors/apache/harness/run_apache_smoke.sh
- connectors/apache/harness/mod_phase4_terminal_rogue.c

Focused regression and static wiring:

- ci/runtime/lifecycle/run-apache-phase4-response-regression.sh
- ci/runtime/lifecycle/apache_phase4_content_type_synchronized_upstream.py
- ci/runtime/lifecycle/cases/apache-phase4-response/
- tests/test_apache_phase4_response_regression_wiring.py
- tests/test_nginx_phase4_runner_wiring.py
- ci/checks/connectors/apache/check-apache-common-adoption.py
- ci/checks/documentation/connector_config_reference.py

Documentation and generated contracts:

- connectors/apache/README.md and README.de.md
- connectors/apache/TODO.md and TODO.de.md
- connectors/apache/capabilities.json
- docs/architecture.md and architecture.de.md
- docs/connectors/apache.md and apache.de.md
- docs/operations-and-security.md and operations-and-security.de.md
- docs/repository-concept.md and repository-concept.de.md
- examples/apache/README.md and README.de.md
- examples/apache/configuration-reference.md and configuration-reference.de.md
- examples/apache/rules/p1-p4-safe.conf and examples/apache/safe/httpd.conf
- reports/connector-configuration-inventory.json
- reports/testing/generated/canonical/connector-capabilities.generated.json,
  connector-capabilities.generated.md, and connector-capabilities.generated.de.md

## Commands executed

All retained runtime/build evidence is under
/var/tmp/codex/ModSecurity-conector/runs/20260718T075119Z-apache-phase4-response-098df329.

1. Pre-fix reproduction passed as an observation: the direct URI target logged
   rule 2190411 with HTTP 403, but the retained internal redirect returned HTTP
   200 plus no-crs-response-body-marker.
2. Current focused native cases passed: deny, allow, log-only, rogue H1 deny,
   rogue H1 allow, rogue H2 deny, empty allow/deny, connector limit,
   ProcessPartial, custom MIME, client abort, P3 deny/header-freeze, valid
   upstream/downstream ErrorDocument H1/H2, nested/pre-output ErrorDocument
   fail-closed controls, and normal/target/URI redirect fail-closed controls.
3. The current H1/H2 multi-brigade denies logged rule 2190401 with HTTP 403,
   response_not_committed, headers_sent false, and eos_seen true.
4. make build-apache passed using component
   696a153ff197a6c939ce29034a59291e7694674f16ff20af7efe3a591e273a3d.
   make check-config-apache passed; every native harness invocation performs
   httpd -t before startup.
5. Static checks passed: shell syntax for the harness and focused runner,
   tests.test_apache_phase4_response_regression_wiring (8 tests),
   check-apache-common-adoption, generated configuration-reference checks, and
   git diff --check.
6. GCC C17 and strict focused GCC/Clang C17 checks passed. Whole-source strict
   Clang remains blocked only by the unchanged origin/master msc_config.c:110
   initializer from commit cfc8b487.
7. Fresh v12 APXS ASan and UBSan DSOs passed native rogue-h1, deny, and
   rogue-h2. The H2 transfer was negotiated as HTTP/2; six diagnostic scans
   had no AddressSanitizer or UndefinedBehaviorSanitizer finding. Apache httpd
   and libModSecurity themselves were not instrumented, and ASan used
   detect_leaks=0.
8. make clang-analysis-baseline passed. The current harness clang analyzer
   produced no findings; clang-tidy produced only non-security advisory
   warnings.
9. The focused Apache CRS profile passed
   crs_sqli_anomaly_block with HTTP 403. The canonical no-CRS Phase-4 fixture
   intentionally rejects a CRS preamble, so it was not treated as a failed CRS
   test.
10. The focused Apache MRTS profile
    mrts_100152_mrts_069_response_body_100152_1 passed as a live Phase-4
    RESPONSE_BODY non-disruptive control with HTTP 200.
11. Independent Codex Security source-to-sink and bypass review found no
    remaining confirmed bypass of the original held response-body path.

## Runtime evidence

Pre-fix and post-fix evidence is hash-addressed in
FND-PARENT-0038. The central retained artifacts are:

| Evidence | SHA-256 |
| --- | --- |
| Pre-fix HTTP 200 redirect status | c11e3f4837efde2441e23a7b9da02131f53bf59fddeb7147c4ab81afe400460f |
| Pre-fix marker body | b186cc3103543b398e617165a51528ccae430b063105434b29a0b01aea28c9ee |
| Current deny Phase-4 log | 45732d58de3644852c63c4d20d29118d7c6cae3f667407efdf3c3654ff03be41 |
| Current H2 rogue Phase-4 log | bd18170c8e4b3a3dae42abaa03af232f7f2b452f2b6e88556e0e23c95904516d |
| Fresh v12 ASan H2 rogue transfer | e4f4ac5699d92415b1de480cf593d029b8d3185b025db81e0662de40532dd8fe |
| Fresh v12 UBSan H2 rogue transfer | ab569dde9d18e2e942792e39100dd0bebe3ca292c819172b8d051e24689e181a |
| CRS compatibility result | 8c7de5d36446759e0753874937565dd13808098e70cbe16e5096ae84bbd9ecd8 |
| MRTS Phase-4 result | d77175c27bd56ad0a08c4945aa1a2e56e6628df55a3f5c5154d48154582f5444 |

## Security impact

The repair converts an EOS-only decision that was formerly downstream of the
first response release into a pre-commit gate. It explicitly covers late
intervention, duplicated output, empty responses, body-limit failures, error
buckets, cleanup, redirects, and ErrorDocument behavior. It retains a
deliberate fail-closed policy where Apache/libModSecurity transaction semantics
cannot safely be preserved.

## Documentation and compatibility

The English/German Apache documentation and examples describe the EOS gate,
opaque libModSecurity MIME decision, bounded response-body limit, terminal
guard, fail-closed redirect policy, and evidence limitations. Generated
configuration/capability artifacts were refreshed through their configured
checks. Framework and MRTS source/gitlinks remain unchanged.

## Known limitations

- The bounded local ErrorDocument exception uses Apache-core no_local_copy and
  REDIRECT_STATUS correlation. It is strong Apache-core evidence but not an
  unforgeable provenance primitive; no request-only exploit was demonstrated.
- The Phase-3 snapshot covers normal response headers, not an all-purpose
  guarantee over HTTP/2 trailers or downstream filters that mutate state after
  release. This cannot leak the held original body after deny.
- Response bytes subject to Phase 4 are held through EOS. This is the smallest
  safe boundary with the available libModSecurity C API and trades progressive
  Phase-4 streaming for enforcement.

## Remaining risks

- The full CRS/MRTS matrix was not run; focused applicable profiles were run.
- Exact-head external delivery evidence remains outstanding.

## Checks not run and rationale

- Draft-PR CI, CodeQL, and SonarQube Cloud: no Draft PR/head exists yet.
- Full CRS/MRTS matrix: not required for this focused Parent fix; a focused CRS
  compatibility control and the exact MRTS RESPONSE_BODY Phase-4 control ran.
- Whole-source strict Clang C17: blocked by the unchanged origin/master
  msc_config.c:110 baseline warning, not by the Phase-4 patch.
- Full repository bilingual-docs link check: the new Change Record's EN/DE
  structure passed, but the dedicated worktree intentionally leaves its
  Framework gitlink unpopulated. The remaining checker output is limited to
  pre-existing links into that read-only Framework checkout; the external
  Framework and MRTS checkouts were separately confirmed clean.

## Final diff and review status

The user authorized a focused Parent branch, commit, push, and Draft PR, but
explicitly prohibited a merge. At this record revision the delivery state is
pending. The next update must record only observed branch, commit, remote,
Draft-PR, exact-head, CI, CodeQL, SonarQube Cloud, review, and revalidation
facts. The requested terminal status is verified_pr, not merge.
