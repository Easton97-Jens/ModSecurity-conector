# Change Record: Apache Phase-4 response enforcement

**Language:** English | [Deutsch](CR-20260718-apache-phase4-response.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260718-apache-phase4-response` |
| Date (UTC) | `2026-07-18` |
| Base revision | `aabde81a9a315bf3e494e595ab0399357c596f9c` |
| Scope | Parent repository only; Framework and MRTS source are unchanged. |
| Related findings | `FND-PARENT-0038`, `FND-PARENT-0041`, `FND-PARENT-0042`, and `FND-PARENT-0043`. |

## Motivation and problem statement

Apache must not release a response byte that Phase 4 can consider before
`msc_process_response_body` and any intervention have resolved. Before this
repair, a fragmented pre-EOS response could cross the commit boundary before a
late decision. Native request reuse during a normal internal redirect is also
unsafe: the transaction cannot be rebound reliably to target URI, rules, and
request variables. In addition, a byte limit does not bound the number of APR
bucket objects retained through EOS.

Generated report metadata had a separate evidence-integrity defect: `git -C`
from an unpopulated Framework gitlink directory could discover the Parent
repository above it and falsely present Parent state as Framework provenance.

## Acceptance criteria

- A disruptive Phase-4 decision prevents the first original response-byte
  release and terminal late output is sealed.
- Unsafe normal redirects fail closed before a target quick-handler or normal
  handler runs; the bounded Apache-core ErrorDocument case remains available.
- The connector retains no more than 4,096 normalized response buckets across
  filter calls and rejects the next one before append/setaside.
- The 4,095-data-bucket-plus-EOS boundary releases normally, while the
  4,097-bucket fragmented sequence fails closed.
- Framework provenance records a real checkout separately from its Parent
  gitlink and treats missing or divergent checkout evidence as stale.
- English and German documentation, generated references, and Change Records
  pass the repository documentation checks without weakening them.

## Implementation decision and rationale

`MODSECURITY_OUT` retains normalized pre-EOS brigades, reaches the Phase-4
decision at EOS, and releases exactly once only after the result is safe. The
protocol guard seals later producer output after denial, EOS, or terminal
failure. An early quick-handler guard plus an early normal-handler fallback
refuse unsafe `r->prev` redirects; the only allowed redirect is a bounded
local ErrorDocument transition with core-shaped provenance proof.

The repair counts every normalized bucket retained pending EOS in
`response_brigade_bucket_count`. `MSCONNECTOR_PHASE4_MAX_HELD_BUCKETS` is
`4096U`; failure happens before append/setaside and release/discard/cleanup
reset the counter.

The generated-report helper now requires Git's reported worktree root to equal
the requested path. It emits actual Framework checkout SHA, recorded gitlink
SHA, checkout status, and gitlink relation as separate metadata. Dependent
generated inputs become stale when the Framework checkout is absent or differs
from its recorded gitlink.

## Changed files

The complete PR #60 diff contains 57 paths. Its executable and test paths are
`ci/checks/connectors/apache/check-apache-common-adoption.py`,
`ci/checks/documentation/connector_config_reference.py`,
`ci/lib/generated_report_utils.py`,
`ci/runtime/lifecycle/apache_phase4_content_type_synchronized_upstream.py`,
`ci/runtime/lifecycle/run-apache-phase4-response-regression.sh`, the ten
`ci/runtime/lifecycle/cases/apache-phase4-response/*.yaml` controls,
`connectors/apache/harness/apache_smoke.conf`,
`connectors/apache/harness/mod_phase4_terminal_rogue.c`,
`connectors/apache/harness/run_apache_smoke.sh`,
`connectors/apache/src/mod_security3.c`,
`connectors/apache/src/mod_security3.h`,
`connectors/apache/src/msc_config.c`,
`connectors/apache/src/msc_filters.c`,
`connectors/apache/src/msc_filters.h`,
`connectors/apache/src/msc_utils.c`,
`connectors/apache/src/msc_utils.h`,
`tests/test_apache_phase4_content_type_synchronized_upstream.py`,
`tests/test_apache_phase4_response_regression_wiring.py`,
`tests/test_connector_capabilities.py`, and
`tests/test_nginx_phase4_runner_wiring.py`.

The paired documentation and generated paths are
`connectors/apache/README.md`, `connectors/apache/README.de.md`,
`connectors/apache/TODO.md`, `connectors/apache/TODO.de.md`,
`connectors/apache/capabilities.json`, `docs/architecture.md`,
`docs/architecture.de.md`, `docs/connectors/apache.md`,
`docs/connectors/apache.de.md`, `docs/operations-and-security.md`,
`docs/operations-and-security.de.md`, `docs/repository-concept.md`,
`docs/repository-concept.de.md`, `examples/apache/README.md`,
`examples/apache/README.de.md`, `examples/apache/configuration-reference.md`,
`examples/apache/configuration-reference.de.md`,
`examples/apache/rules/p1-p4-safe.conf`, `examples/apache/safe/httpd.conf`,
`reports/connector-configuration-inventory.json`,
`reports/testing/generated/canonical/connector-capabilities.generated.json`,
its English and German Markdown companions, this Change Record pair, and the
Change Record README pair.

## Commands executed

- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_apache_phase4_response_regression_wiring tests.test_bilingual_docs tests.test_connector_capabilities.ConnectorCapabilitiesTest.test_metadata_uses_gitlink_when_framework_is_not_checked_out tests.test_connector_capabilities.ConnectorCapabilitiesTest.test_framework_provenance_marks_a_matching_gitlink_checkout tests.test_connector_capabilities.ConnectorCapabilitiesTest.test_framework_provenance_marks_a_checkout_that_differs_from_its_gitlink tests.test_connector_capabilities.ConnectorCapabilitiesTest.test_input_record_marks_a_missing_framework_checkout_stale tests.test_connector_capabilities.ConnectorCapabilitiesTest.test_input_record_marks_a_framework_gitlink_mismatch_stale` passed: 26 tests.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-connector-config-reference` passed: 21 generated files current.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python ci/evidence/collectors/connector_capabilities.py check` passed: 6 connectors and 60 capabilities.
- `rtk proxy bash -n connectors/apache/harness/run_apache_smoke.sh ci/runtime/lifecycle/run-apache-phase4-response-regression.sh` passed.
- `rtk proxy shellcheck ci/runtime/lifecycle/run-apache-phase4-response-regression.sh` passed. The full harness still reports only seven pre-existing baseline diagnostics; the focused audit-log assertion cleanup introduced none.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_apache_phase4_response_regression_wiring` passed: 10 tests after the focused shell cleanup.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs` reproduced the Change Record schema failure before this correction; the local rerun remains blocked only by pre-existing links into the unpopulated Framework gitlink and the populated Framework CI rerun is required.
- `rtk proxy git diff --check` passed before the documentation remediation and is rerun for the corrected candidate.

## Security impact

The changed boundary is before the first original response-byte release. It
prevents a disruptive `RESPONSE_BODY` policy from degrading to log-only merely
because a body arrives in multiple brigades. Unsafe redirect reuse fails closed
instead of continuing with a stale native transaction. The bucket cap closes a
validated CWE-400 availability condition below the byte limit. The provenance
gate prevents Parent Git state from masquerading as Framework evidence.

## Runtime evidence

The retained native Apache validation reproduces pre-fix HTTP 200 for 4,097
one-byte buckets below the one MiB byte cap. The repaired module rejects a
split 4,097-bucket sequence with HTTP 500 before release, releases
4,095 data buckets plus EOS with HTTP 200 and exactly 4,095 bytes, and passed
the serial 32-mode safe matrix. The 30-mode sealed receipt is
`runs/20260719T162259Z-pr60-exact-head-revalidation-dfba422e/evidence/pr60-exact-native-phase4-manifest.json`
with SHA-256
`1f44c2817676ef2952f70573917657d67645d8d85d57e829a47c9d67ee2ea548`.
The retained 32-mode report is
`runs/20260719T183551Z-pr60-final-security-diff-93404fdd/evidence/security-diff/artifacts/05_findings/CAND-PR60-001/validation_report.md`
with SHA-256
`79e7e1b3fcca6acdf8d02ed941eaadcea566258656abe269a54289a59e88db8c`.

## Known limitations

Phase-4 responses within scope are intentionally held through EOS; progressive
streaming is not available at that enforcement boundary. The bounded local
ErrorDocument transition relies on Apache-core `no_local_copy` plus
`REDIRECT_STATUS`, not on an unforgeable token. The Phase-3 snapshot does not
claim to freeze HTTP/2 trailers.

## Remaining risks

`FND-PARENT-0042` is locally fixed but still needs exact pushed-head and
resulting-master verification. `FND-PARENT-0043` remains P2/low: the shared
helper and current capability artifacts are corrected, while four
report-specific direct Git sinks and one critical layout-relation check remain
tracked follow-up work. No High or Critical finding was identified locally.

## Checks not run and rationale

The full `tests.test_connector_capabilities` module has one expected
environment-blocked case because this dedicated worktree lacks
`modules/ModSecurity-test-Framework/ci/checks/catalog/no_crs_baseline.py`.
The focused changed-path tests pass. The full CRS/MRTS matrix was not rerun;
the retained focused native Apache validation is described above. No direct
push, force push, bypass, or master merge is claimed by this record.

## Final diff and review status

PR #60 targets `master`. Before this Change Record schema correction, its
exact head `418465645e2ceae60e842d1c3d7994d8bed93fa6` had the six required
protected contexts, CodeQL, and SonarCloud passing, while Change Record schema
checks failed. This correction produces a new candidate head and restarts the
exact-head CI, review/conversation, and current-base verification cycle. The
PR is not merged at record authoring. A subsequent focused shell-lint cleanup
keeps the audit-log assertions fail closed and requires the same exact-head
verification cycle.
