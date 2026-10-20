# Change Record: CR-20261020-i12-lighttpd-capture-producers

**Language:** English | [Deutsch](CR-20261020-i12-lighttpd-capture-producers.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261020-i12-lighttpd-capture-producers |
| Date (UTC) | 2026-10-20 |
| Base revision | `eef8c1b432c0ce372c551a32fa6977cf4633b6c3` |

## Motivation and problem statement

Original Stock-Sidecar153, Patched-Native116 and diagnostic Stock-Native78 IDs require physical host measurements and independently reviewed qualification. Capture success alone cannot establish acceptance. This change makes lighttpd-specific producers and current provenance reviewable without changing baseline inventories or shared validators.

## Acceptance criteria

Preserve all347 original IDs and original51/52/23 oracle inventories. Bind client/backend/host/native/log/cleanup measurements to exact packet/oracle proposals and independent Root review. Separate diagnostic configuration/header acceptance from required body lifecycle. Reject copied receipts, stale source bindings and unsupported strict-abort claims. Retain private0700 directories/0600 files and actual UID65534 provenance.

## Implementation decision and rationale

Route-specific modules separate capture construction, transport observation, configuration cases, packet assembly and qualification proposals. Stock retains technical spool/sink failure attribution and readmission. Patched measures actual native request/response hooks and transport completion. Diagnostic models supported P1/configuration/technical controls, including separately approved pre-native rejections; it creates no body-streaming capability. Diagnostic audit fallback accepts only an exact rule token inside the selected main transaction record. Physical observers and bounded fault fixtures are test-only. Existing shared validators qualify only after exact Root review.

The qualification adapter resolves external storage lazily only through an explicit `I12_TEST_ROOT`; import needs no pre-existing fixed `/var/tmp/codex`. Actual storage use validates ownership and write permissions. Artifact/current-ledger consumers retain that guard, supporting fresh runners without weakening evidence-path validation or treating a generic temporary directory as evidence storage.

## Changed files

Under `ci/runtime/lifecycle/i12/lighttpd/`: `stock_capture.py` and Stock configuration/inventory/client/spool/floor/packet/qualification/transport/fault helpers; `patched_capture.py`, `patched_qualification.py` and native SDK/transport/fault observers; `diagnostic_capture.py` and diagnostic configuration/coverage/scenario/native/pre-native/packet/transport/fault helpers and oracle fixtures; `qualification.py`, `current_ledger.py` and `artifact.py`. Focused `tests/test_lighttpd_i12_*.py` controls cover these paths.

Documentation comprises this EN/DE pair and the [current evidence](../../testing/lighttpd-i12-20261015/current-evidence.md) pair. Generated `reports/testing/lighttpd-i12-20261015/current-20261020/` ledgers and summary come from the lighttpd exporter. Product fixes remain on existing#382 and shared changes on#410. No central matrix, shared generator, Framework/MRTS or unrelated connector is edited.

## Commands executed

The native scaffold command succeeded: `rtk proxy /usr/local/bin/python3 ci/tools/new-change-record.py create --name i12-lighttpd-capture-producers --base-revision eef8c1b432c0ce372c551a32fa6977cf4633b6c3 --date 2026-10-20`. Current-source qualification replay accepted168 exact originals before export. Independent full-inventory review checked347 rows and6214 physical references; a separate privileged read verified24 private UID65534 files without changing permissions.

`rtk proxy /usr/local/bin/python3 ci/tools/new-change-record.py check` passed the archive structure contract. The focused `test_lighttpd_i12_*.py` suite passed99 tests. Independent review of all36 selected diagnostic qualifications confirmed that all15 rule-bearing normal host cases have exact physical main-transaction events and require no audit fallback. The15 Sonar reliability contract tests passed after using an existing private `TMPDIR`. `rtk make check-bilingual-docs`, `rtk make check-doc-links` and `rtk git diff --check` passed. Manual EN/DE comparison confirmed equivalent scopes, counts, revisions and limitations.

## Security impact

Bounded functional/regression work stays within the user's Blue scope. No deep scan, exploit work, external target expansion, isolation relaxation or Quality Gate weakening is introduced. Root and UID65534 runs remain distinct. Private files stay0600 and spool directories0700. Technical exhaustion remains a technical failure, never an invented native `BODY_LIMIT` decision. Lazy storage resolution retains ownership/permission checks at use.

## Runtime evidence

Current qualification is168 PASS: Stock60, Patched72 and diagnostic36 (28 host plus8 parser controls). Actual executions are128 HTTP,112 HTTP and69 HTTP plus8 parser, respectively. The347-row capture index grants no PASS. Currently unqualified counts are92/44/42 under the historical/current union; original oracles still open are17/13/19. Newly qualified IDs are59/70/35 and newly resolved original oracles32/37/4. Generated route ledgers retain source-specific remaining reasons.

Six product fixes are normally integrated from#382 through#410. Fix `c523dce9966b47bc8be6efe39ee49f2d88de3397` closes response inspection bypass through splice/sendfile. Fresh UID65534 evidence measures1,050,657 response bytes across native/host/client/backend and one EOS. Five P3 rejects produce403/158 body bytes; nine affected response cases were retaken. Reject retains `runtime_finish=0`, `common_finish=2` and logging/free/destroy each1. Export binds product `12cc380c3749fd76c246c05ce479f51446127880`, base `a62296fb57263f9be18c6ac879e36e0ab2a9935c` and pre-producer integration `eef8c1b432c0ce372c551a32fa6977cf4633b6c3`.

The [current evidence prerelease](https://github.com/Easton97-Jens/ModSecurity-conector/releases/tag/evidence-i12-lighttpd-pr412-20261020-current) targets published source head `2008b875f1860774627878051582b607f835b019`. Its archive SHA256 is `c7dccdfd5bb1c69029eb92864a5c9b62bd06e24a9a2466183c7f40ddc281d1bf`; the manifest SHA256 is `eaf8d88e515b59965505aeb0c66fbb991dc96d8cce0c9bb24b0ef7a1e2b656f1`. All six assets were downloaded afresh. The downloaded checksums, standalone verifier and embedded/external manifest comparison passed for4917 objects,7602 physical paths,543,241,266 unique bytes and zero unavailable selected references. The separate publication review enumerates three out-of-scope mixed/foreign references and four exact immutable snapshot resolutions; neither class adds qualification credit. A bounded high-confidence credential-pattern scan covered4918 archive members and546,077,222 uncompressed bytes without a finding.

## Known limitations

Full acceptance is incomplete. Unqualified originals and open oracles remain visible. Stock-Native cannot replace Sidecar. Strict client abort is unsupported where the actual registry says so; short writes prove neither EAGAIN nor peer RST. Historical merged snapshot `5e3b95864403dc642f77f01ef963d8c459b08628` reproduces Stock RST/empty-event deviation; the exact earlier pre-merge object is unavailable and is not equated with that snapshot.

## Remaining risks

Current raw artifact publication and actual download verification are complete. Historical checkpoint03 remains separate and does not prove current168 qualifications. Source-specific oracle decisions, final published-head CI/Sonar and unavailable local Gitleaks evidence prevent complete acceptance.

## Checks not run and rationale

Gitleaks is locally unavailable; no pass is claimed and bounded credential-pattern review does not replace it. Final hosted CI/Sonar results await publication and observation. Deep scans and unsupported capabilities are outside the bounded authorized scope.

## Final diff and review status

Separate route ledgers preserve immutable originals and narrow scopes. Exact Root-reviewed source-bound results, independent physical-reference review and the freshly downloaded current artifact support this checkpoint. Source and evidence publication are complete; final hosted checks remain active on existing Draft#412. No complete acceptance, merge or master integration is claimed.
