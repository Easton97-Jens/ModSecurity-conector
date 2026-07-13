> Generated file - do not edit manually.
>
> Generated at: `2026-07-12T20:12:32Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/evidence/reports/refresh-connector-reports.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `important`
> Connector SHA: `9b718cee0523da3e0822754dc4b05f327b6d969d`
> Framework SHA: `4e9d4ba616235127b6fc0a2ee87107d93d03f40b`
> Input status: `stale`

# Report Freshness

**Language:** English | [Deutsch](report-freshness.generated.de.md)

| Report | Status | Generated At | Newest Input | Newest Output | Missing Inputs | Notes |
|---|---|---|---|---|---|---|
| `connector_coverage_reports` | fresh | - | 2026-07-11T12:42:23Z | 2026-07-12T20:12:25Z | - | generated |
| `full_runtime_matrix` | skipped | 2026-06-19T16:57:56Z | - | 2026-07-12T20:12:25Z | BUILD_ROOT:full-matrix/full-runtime-matrix-runs.jsonl | skipped_missing_input |
| `full_matrix_job_completeness` | skipped | 2026-06-19T16:57:57Z | - | 2026-07-12T20:12:25Z | BUILD_ROOT:verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json, BUILD_ROOT:full-matrix/full-runtime-matrix-runs.jsonl | skipped_missing_input |
| `verified_runtime_mismatch_analysis` | skipped | 2026-06-19T16:58:03Z | - | 2026-07-12T20:12:25Z | BUILD_ROOT:verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json, BUILD_ROOT:full-matrix/full-runtime-matrix-runs.jsonl | skipped_missing_input |
| `nginx_mrts_http500_cluster_analysis` | stale | 2026-06-19T16:58:04Z | 2026-07-12T20:12:15Z | 2026-07-12T20:12:25Z | BUILD_ROOT:verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json, BUILD_ROOT:full-matrix/full-runtime-matrix-runs.jsonl | skipped_missing_input |
| `connector_work_queue` | stale | 2026-06-19T16:58:08Z | 2026-07-12T20:12:15Z | 2026-07-12T20:12:26Z | - | skipped_stale_input |
| `phase_work_queue` | stale | 2026-06-19T16:58:16Z | 2026-07-12T20:12:15Z | 2026-07-12T20:12:26Z | - | skipped_stale_input |
| `native_mrts_reports` | skipped | 2026-06-19T16:58:10Z | - | 2026-07-12T20:12:26Z | BUILD_ROOT:mrts-native/apache2_ubuntu/job.json, BUILD_ROOT:mrts-native/nginx-pr24/job.json | skipped_missing_input |
| `native_semantics_comparison` | stale | 2026-06-19T16:58:11Z | 2026-07-12T20:12:15Z | 2026-07-12T20:12:26Z | - | skipped_stale_input |
| `nolog_audit_evidence` | stale | 2026-06-19T16:58:12Z | 2026-07-12T20:12:15Z | 2026-07-12T20:12:26Z | - | skipped_stale_input |
| `response_header_hook_analysis` | stale | 2026-06-19T16:58:16Z | 2026-07-12T20:12:15Z | 2026-07-12T20:12:27Z | - | skipped_stale_input |
| `phase4_hard_abort_capability` | stale | 2026-06-19T16:58:23Z | 2026-07-12T20:12:15Z | 2026-07-12T20:12:27Z | - | skipped_stale_input |
| `remaining_failure_analysis` | stale | 2026-06-19T16:58:27Z | 2026-07-12T20:12:15Z | 2026-07-12T20:12:28Z | - | skipped_stale_input |
| `intervention_blocking_analysis` | stale | 2026-06-19T16:58:52Z | 2026-07-12T20:12:15Z | 2026-07-12T20:12:29Z | - | skipped_stale_input |
| `no_mrts_intervention_nomatch_analysis` | stale | 2026-06-19T16:58:53Z | 2026-07-12T20:12:15Z | 2026-07-12T20:12:29Z | - | skipped_stale_input |
| `body_processor_analysis` | stale | 2026-06-19T16:59:03Z | 2026-07-12T20:12:15Z | 2026-07-12T20:12:29Z | - | skipped_stale_input |
| `rule_chain_semantics_analysis` | stale | 2026-06-19T16:59:05Z | 2026-07-12T20:12:15Z | 2026-07-12T20:12:30Z | - | skipped_stale_input |
| `final_consistency_audit` | stale | 2026-06-19T16:59:06Z | 2026-07-12T20:12:15Z | 2026-07-12T20:12:30Z | - | skipped_stale_input |
| `runtime_cache_reports` | fresh | 2026-07-12T19:36:08Z | 2026-07-12T19:36:08Z | 2026-07-12T20:12:32Z | - | generated |
| `report_freshness` | fresh | 2026-07-12T20:12:32Z | 2026-07-12T20:12:37Z | 2026-07-12T20:12:38Z | - | generated |
| `merge_readiness_dashboard` | fresh | 2026-07-12T20:12:32Z | 2026-07-12T20:12:38Z | 2026-07-12T20:12:40Z | - | generated |
| `report_refresh_manifest` | fresh | 2026-07-12T20:12:32Z | - | 2026-07-12T19:49:19Z | - | generated |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/test-coverage-overview.md` | `eb8531f6d83fa7fc29cf775e273b40c46468dbcebf88cac876d10f0e6eb62148` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/runtime/apache-runtime-results.generated.md` | `6a0f4f705b0062709c0f21b73fb0a26b6a2a38a6f52abcc0fb376dde47995eb3` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/coverage/case-matrix.generated.md` | `89f35d5215d00186f03b3017c1839bfbc58b60f8d90b39516f1ce72f9a055571` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/coverage/connector-gap-summary.generated.md` | `4b665723632d5fa69f0e47593feb1663cf007bce7a3a0eeec252289b5949f3cb` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/coverage/coverage-summary.generated.md` | `b0f44ffa879cd44c19b256cd4d2bf1570fd6452adddf868cb2fa60bcee941577` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/runtime/haproxy-runtime-results.generated.md` | `d628984b45415314b2f3461ff4f84dbe64921cad698f9a40eb665b2386257c71` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/runtime/nginx-runtime-results.generated.md` | `ec863bca499782fa69096708e53616ab5761b9672f5de15a4d9e1ade8a27ddb9` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/coverage/phase-coverage.generated.md` | `7da89e3821de5ee8fdc4c129dcd766a10eed8eece8c1cd928b58b531fcf30872` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/runtime/runtime-matrix.generated.md` | `e13f0ca3911ebc5c030f9a2c3fa6e4e33d67590d712c1f73030a2a50a8f7abcb` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/coverage/xfail-summary.generated.md` | `e986e49ce78158b2f96e153d340148b2590f5237ff923aae96940126ba617290` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `3f41446a7fb73a361c12e31507673774698ec41d108f2c8e75c8c57b8d2ef007` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.md` | `5a12905087f9da1f324337ebb39e52c494c3b57229aa0b2d069cfe425796c3a8` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | `a54dc3f43ffc6d2eb4493ad56c58e6eff959cb2ce1380f5eb3d4b4e02003f5c2` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.md` | `b809a1641f4bbaa22b18d6a63ef6d32cd6389ac937b316d684001a055b0f8ef4` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `340546dbab42432eef255f99fda65c0d4301db589d6ac5c9f2a201a94326420e` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.md` | `28890c18ba215d54856cb43939a16bba7b0d75592c73250ea357c407302303c7` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.json` | `cd80349d7516fe254fed03188f7d84fc61979b5680b09607c7a8e19d142eff47` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.md` | `b0bc132f9a6d93e7c57492f00024431541e0f7de53b67dbcf64514c58a41167c` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `89f3d29f508ef24e279589f6a3fa791c2f62d5a13ca89f58b10adb4ba4cd3484` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.md` | `2d4b68a3dc593f3ce95b202a124fbd24454fda261089e7cde5f67b972d23db00` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `de46f52db4aa93f393cf9e7a97ef734435d9e9d7f9af4c99ceed8294867d9a1b` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `3f500554ef2376d55d16972b04e773c3309dfacdda3f069ca8a14ff2be07e643` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-full.generated.json` | `d7fbd046106a858fc6bbb11c7f14ddb745bef5059b9fc5cbdba9b1b512ddf8c4` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-full.generated.md` | `28766e05f7832dc1491b012493336b71a5d1c67dd0022050d9dc0f472a7c4e77` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | `a628c7910973dfe3ea2379d1de447632bb7a68bc93945814d7e5922711b01933` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.md` | `88f142196ac211bcdd631f901a53610578c5ce4eebc5dd6fe866eb1b8780e929` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | `dcb7aea74fa53c58425123bf580dbe52ae9898bbc0af29bd38ee98925848c833` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.md` | `b09e3147b1a44e2aa2039095d7996803e03cb2ecaf282ea443d4ed0155565f65` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | `8b8298f135b70c6487dcfbae620801fc09fabe03e73c91fe8657a27505216bce` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.md` | `507a9dfbea95edeb3aaf73b3688d080924d090aa8add76c5808f1a760b57938d` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/manifest/native-semantics-comparison.generated.json` | `cf34c749555c04585d0e5dbe339f2f7da889f2888ec57811bf3f83b9caae1e07` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/manifest/native-semantics-comparison.generated.md` | `eb8ce1c9decb259adf692692beae6e5fc25da35e7af672a6cbfce5e3d5345563` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json` | `4cc4b220df8adb4ebdb3e8666a41be8c1e37660ba0baf0a37e489087415dca4c` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.md` | `808d96eb46c2b51c9621f7c7c9524a4190c567e96ee07ea5aba2e8b4563b9fe7` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `de46f52db4aa93f393cf9e7a97ef734435d9e9d7f9af4c99ceed8294867d9a1b` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `3f500554ef2376d55d16972b04e773c3309dfacdda3f069ca8a14ff2be07e643` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json` | `7d73f40c3ec211958b2eb5979a0c45f13303b53da032a90f96f00d8d77da5092` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.md` | `e2b30f56ea6c305276604d2b5414e8083f8839e337666251bf3eed3c3c9fe7d1` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `de46f52db4aa93f393cf9e7a97ef734435d9e9d7f9af4c99ceed8294867d9a1b` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `3f500554ef2376d55d16972b04e773c3309dfacdda3f069ca8a14ff2be07e643` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json` | `6e00d5cd2e1239d414915f89feca72d744dcaf27d5c224513dc78ed3db310682` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.md` | `b0e3b4c05ca0a7d24cbaaa32b7c3e8457cb1e7f9b9be51454edb3c89e88ac1ea` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `de46f52db4aa93f393cf9e7a97ef734435d9e9d7f9af4c99ceed8294867d9a1b` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `3f500554ef2376d55d16972b04e773c3309dfacdda3f069ca8a14ff2be07e643` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `c581790d4581ac9cf843e973f127b274784caf286d1661d72b5144f078049165` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.md` | `e1fe9715830ba612d0939617b59f9abe8ffc1380faef9b08a88cb0573327f096` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `45c592a17f99671474b5f510d59c5c5f162861bcc74e37f4a7c72e6e4bc6a736` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.md` | `096cf8ab13676c7f65285d701339b5ee66e9f5d1bc7d2e3da55771390c69438b` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `486d395cbc4da9e489dcc2f81e0fda69c34e66971e03133f02f797570f9a2400` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.md` | `fd411d0b1f24a595c3a46d871f8a69868608335f55b1c50d239f6e95988092d5` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | `256bdac6851d1bea706d7ae21377412ce79edb977969ec5774e0b27a6ae56a8e` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.md` | `479ef888acb275528232d32a0fbdbd54f6abaee78e3e87ba31a999a82ebe62a0` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json` | `a163cfa2dd4408fb802138a063f4651c6c930b4799b6089976083e19a45b5082` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.md` | `6abd7b7b7bde4a426e1284c51ef867ba9f90a1ddaa045677f54ee88e79dad4db` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json` | `4ca4fc4f48a5420c3dc9892faa3d53b1b28b322dc49fcc3adc6e341681465be4` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.md` | `7be2d1b763aa475bea209bcf0554848d3faac7e662e97a10f8781fbd202522f2` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json` | `97fca3207c05713f8e25bc092e5bf9e9ab65c7f36e5ba1da28cece9ff7637636` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.md` | `b81577dc9928b17577f390deb7f131190c85898d037b76d3a6749d2fd11f8c45` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.json` | `d969736e6a6b68e331b83c17dd8edb8516314b1d78dd5e8c9ab41806bfea1502` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.md` | `80f770f9d8f05480c8fc1e57ed715ccbc41a5fb0a0bf5299911d3e90dd53bfe5` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/cache/runtime-component-cache.generated.json` | `03c2f68e9bc059c277b9d9fa23b7b98ffe0f4bb74e172e1205a356ac69e5661e` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-component-cache.generated.md` | `640e44bb2748b0364a82c762b2f9d9009dc670188f9877e46fdd4c6e2714e12c` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-build-cache.generated.json` | `1ac095cbdfe784f36f77e7cfee3f26c0f1f7fd29dd33530fc737dee1ef6c96b6` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-build-cache.generated.md` | `481addeceeba6fd3405387e6efaacdb2662e81092d230baf9dc33d678bc67dc3` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-cache-index.generated.json` | `312b6e1f09927d2c042ee760974d2211ba43a0a06efb7d0c578030aae64f7e4f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-cache-index.generated.md` | `cb212b15d611770acb02dc0fd96f9680b243943c04e8d93699bf5dda5d3c9a16` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/test-coverage-overview.md` | present | input file available |
| `reports/testing/generated/runtime/apache-runtime-results.generated.md` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/coverage/case-matrix.generated.md` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/coverage/connector-gap-summary.generated.md` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/coverage/coverage-summary.generated.md` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/runtime/haproxy-runtime-results.generated.md` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/runtime/nginx-runtime-results.generated.md` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/coverage/phase-coverage.generated.md` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/runtime/runtime-matrix.generated.md` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/coverage/xfail-summary.generated.md` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.md` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/manifest/full-matrix-job-completeness.generated.md` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.md` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.md` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/work-queues/connector-work-queue.generated.md` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/work-queues/phase-work-queue.generated.md` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/mrts-native/mrts-native-full.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/mrts-native/mrts-native-full.generated.md` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/mrts-native/mrts-native-apache.generated.md` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/mrts-native/mrts-native-nginx.generated.md` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/mrts-native/mrts-native-summary.generated.md` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/manifest/native-semantics-comparison.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/manifest/native-semantics-comparison.generated.md` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.md` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/work-queues/phase-work-queue.generated.md` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.md` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/work-queues/phase-work-queue.generated.md` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.md` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/work-queues/phase-work-queue.generated.md` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.md` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/canonical/next-fix-plan.generated.md` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/canonical/full-run-evidence.generated.md` | present | input file available |
| `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.md` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.md` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/focused-analysis/body-processor-analysis.generated.md` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.md` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/canonical/final-consistency-audit.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/canonical/final-consistency-audit.generated.md` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/cache/runtime-component-cache.generated.json` | present | input file available |
| `reports/testing/generated/cache/runtime-component-cache.generated.md` | present | input file available |
| `reports/testing/generated/cache/runtime-build-cache.generated.json` | present | input file available |
| `reports/testing/generated/cache/runtime-build-cache.generated.md` | present | input file available |
| `reports/testing/generated/cache/runtime-cache-index.generated.json` | present | input file available |
| `reports/testing/generated/cache/runtime-cache-index.generated.md` | present | input file available |
