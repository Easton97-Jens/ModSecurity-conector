# Change Record: CR-20261018-i12-apache-evidence-boundaries

**Language:** English | [Deutsch](CR-20261018-i12-apache-evidence-boundaries.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-i12-apache-evidence-boundaries |
| Date (UTC) | 2026-10-18 |
| Base revision | `ad510c3b4168ff0e11fc36803e2ce4127a0689ad` |

## Motivation and problem statement

The Cloud analysis of this base revision reported 59 open new findings: 35 vulnerabilities and 24 code smells, Security rating E, 62 new duplicated lines, zero accepted findings and zero new hotspots; the Quality Gate was ERROR. Analysis ID: `fb98417b-c9eb-4f0f-ba1d-e94e5b868a0a`; CE task: `AaFAC4JUzCyA98lidsk1`. These are historical server results, not results for the unpublished changes described here.

This change confines existing Apache evidence tools to admitted private storage and literal loopback client arguments, simplifies the existing extraction and packaging paths, and makes the public readback's provenance explicit. New acceptance drivers, new host observers and their later runtime runs are outside this record.

## Acceptance criteria

Private path and client argument guards reject unsafe input; actual APR calls and return values remain intact. Extraction, complete 155-row ledgers and packages retain their observations, original oracles, unknown values and approval boundaries. The physical source of a public projection remains independently retrievable. Final published-head CI and Cloud analysis remain required before any overall acceptance claim.

## Implementation decision and rationale

`paths.py` validates configured external storage, ancestry ownership/modes, canonical nonsymlink input files, fixture selectors and private output destinations. Both preparers seal this helper and `process_capture.py`; the latter shares existing same-process snapshots without inventing cleanup observations. `observed_curl.py` admits a literal option/value set, one uncredentialed high-port HTTP loopback URL and private body/output paths; genuine readiness curl disables implicit configuration loading.

The APR fault helper requires the opt-in `I12_SINK_ROOT`, canonical current-UID nonshared storage and the existing exact private marker. Typed function pointers, an observation structure and a physical-operation helper replace complex declarations and branching; real descriptor operations and APR results are forwarded. Named collectors split extraction, ledger, package and preparation work. An equivalence check exposed an incorrect candidate selection and accepted-packet overwrite during refactoring; both were corrected and regression coverage preserves the supplied input and accepted packet.

`public_projection.py` renames 18 timestamp-derived numeric client joins from `client_token` to `client_process_correlation_id`. Its metadata explicitly states `is_physical_capture: false`, lists each rename and binds the unmodified source hash. This changes the public field name, not the physical observations or their meaning.

## Changed files

The Apache-only directory `ci/runtime/lifecycle/apache-i12/` contains changes to `apr_sink_fault.c`, `launch.py`, `ledger.py`, `observed_curl.py`, `package.py`, `prepare.py`, `prepare_sinks.py`, `review.py` and `sink_launch.py`, plus `paths.py`, `process_capture.py` and `public_projection.py`.

Associated changes cover `tests/test_apache_i12_boundaries.py`, `tests/test_apache_i12_launch.py`, `tests/test_apache_i12_package.py` and `tests/test_apache_i12_sink_fault.py`; historical reproduction helpers `root-review-duplicate.py`, `root-review-supported.py` and `rule-equivalence-probe.py`; the public `sink-positive-control.json`; and its retained raw source and manifest. This EN/DE Change Record pair documents that scope. No productive connector code, shared observer, workflow, scanner exclusion, Framework/MRTS gitlink or central matrix is changed by this slice.

## Commands executed

The earlier focused run used:

```sh
rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -q tests.test_apache_i12_mapper tests.test_apache_i12_sink_fault tests.test_apache_i12_review tests.test_apache_i12_ledger tests.test_apache_i12_package tests.test_apache_i12_launch tests.test_apache_i12_boundaries
```

Result: 48 tests, exit 0, including eight tests with real APR operations. Disabling the physical fault operation in a separate source mutant ran eight native tests and produced two expected failures, zero errors; the mutation detector exited 0. Full-field comparisons were equal for eight actual unsigned packets, all 155 ledger rows and all 155 package rows. Three preparation checks sealed their inputs; they did not execute hosts. The earlier `rtk proxy git diff --check` exited 0. After this pair was filled, `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python ci/tools/new-change-record.py check` and `rtk proxy git diff --check` both exited 0. The Change Record check validates structure only, not evidence correctness.

Run-scoped receipts are under `/var/tmp/codex/ModSecurity-conector/runs/i12-apache-414-acceptance-20261015/analysis/`: `sonar-checks/receipt.json`, `sonar-checks/mutation-receipt.json`, `sonar-extraction-equivalence.json`, `sonar-ledger-package-equivalence.json`, `sonar-preparation-checks.json` and `sonar-fix-summary.json`. These local receipts describe the recorded working-tree state; they do not establish delivery or final-head checks.

## Security impact

Attack preconditions are attacker-controlled CLI paths, fixture selectors or client arguments reaching these private test tools, or unsafe writable storage substitutions. The guards restrict those inputs and fail closed. Numeric process joins carry no authentication authority. No scanner exclusion, accepted finding, waiver, validation bypass, fault fabrication, warning relaxation or weakened gate is used.

## Runtime evidence

The tests exercise real APR operations and negative controls; equivalence reuses eight existing actual host packets. This record claims no additional native host execution or newly qualified I12 PASS.

The historical case ledger remains byte-identical with SHA256 `927a0c809e7c26bcdb4ffed2f87370c23c6a21a066d6bb7bc217a626be7ea746`. The retained [raw manifest](../apache-i12-20261015/raw/manifest.json) addresses [sink-positive-control.json.gz](../apache-i12-20261015/raw/sink-positive-control.json.gz): compressed SHA256 `22f8ba1e53be10ce9b2cb92fa3849877889f08fd65f086f2acc830df93e57e59`, decoded SHA256 `e52c51888736e9f252d1eff738e75cd7f8dd784045926ec12fad2df85439772f`. The same original is preserved at commit `68e3c34a780e26cfb714155b4f7652ca059a8572`. The public projection is explicitly separate from that physical source.

## Known limitations

The 59 source remedies are candidates until the published head receives a new Cloud analysis. Local Vortex returned HTTP 403; authenticated Cloud readbacks succeeded. Neither that failure nor local source review establishes zero findings. Preparation and packet equivalence do not prove execution of the remaining Apache contracts. Missing measurements remain unknown.

## Remaining risks

Combined-source regressions and newly reported scanner findings require final integrated checks. Existing runtime gaps, original oracle conflicts and the 155-case acceptance decision remain separate work. There is no release approval or `I12_COMPLETE` claim.

## Checks not run and rationale

Final published-head Cloud analysis, strict zero duplication/security acceptance, exact-head GitHub CI and the final integrated host campaign are not established by this slice because it precedes publication and integration. Repository-wide bilingual/link validation is owned by the integrating task after this pair is filled. No merge, deployment or product release was performed for this record.

## Final diff and review status

The recorded scope is an uncommitted Apache evidence-tool candidate based on the revision above; it is not a delivery SHA. The integrating task owns final diff inspection, fresh validation, ordinary commits/push and PR #414 updates. Source remediation is not reported as Cloud resolution.
