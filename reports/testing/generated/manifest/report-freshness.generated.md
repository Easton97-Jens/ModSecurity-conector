> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T05:58:01Z`
> Verified run id: `2026-06-15T21-01-39Z-9391a8d0`
> Data source policy: `verified-inputs-only`
> Generator: `ci/refresh-connector-reports.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `important`
> Connector SHA: `9391a8d0d5bf170f8af994c361f0b9fa50015834`
> Framework SHA: `708183dce7dcd0ad190a5cb5211b1ba3de6a2385`
> Input status: `blocked`

# Report Freshness

| Report | Status | Generated At | Newest Input | Newest Output | Missing Inputs | Notes |
|---|---|---|---|---|---|---|
| `connector_coverage_reports` | fresh | - | 2026-06-15T21:17:13Z | 2026-06-16T05:56:27Z | - | generated |
| `full_runtime_matrix` | fresh | 2026-06-16T05:56:27Z | 2026-06-16T05:54:45Z | 2026-06-16T05:56:27Z | - | generated |
| `full_matrix_job_completeness` | fresh | 2026-06-16T05:56:28Z | 2026-06-16T05:56:28Z | 2026-06-16T05:56:28Z | - | generated |
| `verified_runtime_mismatch_analysis` | fresh | 2026-06-16T05:56:32Z | 2026-06-16T05:56:28Z | 2026-06-16T05:56:32Z | - | generated |
| `connector_work_queue` | fresh | 2026-06-16T05:56:37Z | 2026-06-16T05:56:27Z | 2026-06-16T05:56:37Z | - | generated |
| `phase_work_queue` | fresh | 2026-06-16T05:56:37Z | 2026-06-16T05:56:37Z | 2026-06-16T05:56:38Z | - | generated |
| `native_mrts_reports` | fresh | 2026-06-16T05:56:38Z | 2026-06-15T23:18:04Z | 2026-06-16T05:56:38Z | - | generated |
| `nolog_audit_evidence` | fresh | 2026-06-16T05:56:40Z | 2026-06-16T05:56:39Z | 2026-06-16T05:56:40Z | - | generated |
| `response_header_hook_analysis` | fresh | 2026-06-16T05:56:44Z | 2026-06-16T05:56:43Z | 2026-06-16T05:56:44Z | - | generated |
| `phase4_hard_abort_capability` | fresh | 2026-06-16T05:56:55Z | 2026-06-16T05:56:43Z | 2026-06-16T05:56:56Z | - | generated |
| `remaining_failure_analysis` | fresh | 2026-06-16T05:57:06Z | 2026-06-16T05:56:56Z | 2026-06-16T05:57:54Z | - | generated |
| `intervention_blocking_analysis` | stale | 2026-06-16T05:57:55Z | 2026-06-16T05:57:54Z | 2026-06-16T05:57:56Z | - | skipped_stale_input |
| `no_mrts_intervention_nomatch_analysis` | stale | 2026-06-16T05:57:56Z | 2026-06-16T05:57:55Z | 2026-06-16T05:57:56Z | - | blocked |
| `body_processor_analysis` | stale | 2026-06-16T05:57:57Z | 2026-06-16T05:57:54Z | 2026-06-16T05:57:57Z | - | skipped_stale_input |
| `rule_chain_semantics_analysis` | stale | 2026-06-16T05:57:58Z | 2026-06-16T05:57:54Z | 2026-06-16T05:57:58Z | - | skipped_stale_input |
| `final_consistency_audit` | stale | 2026-06-16T05:57:59Z | 2026-06-16T05:57:58Z | 2026-06-16T05:58:00Z | - | blocked |
| `runtime_cache_reports` | fresh | 2026-06-16T04:53:27Z | 2026-06-16T05:58:01Z | 2026-06-16T05:58:01Z | - | generated |
| `report_dependency_graph` | fresh | 2026-06-16T05:58:01Z | 2026-06-16T05:58:01Z | 2026-06-16T05:58:01Z | - | generated |
| `report_data_lineage` | fresh | 2026-06-16T05:58:01Z | 2026-06-16T05:58:01Z | 2026-06-16T05:58:03Z | - | generated |
| `report_path_migration` | fresh | 2026-06-16T05:58:01Z | - | 2026-06-16T05:58:04Z | - | generated |
| `generator_runtime_summary` | fresh | 2026-06-16T05:58:01Z | - | 2026-06-16T05:58:05Z | - | generated |
| `report_freshness` | fresh | 2026-06-16T05:58:01Z | 2026-06-16T05:58:05Z | 2026-06-16T05:58:06Z | - | generated |
| `merge_readiness_dashboard` | fresh | 2026-06-16T05:58:01Z | 2026-06-16T05:58:06Z | 2026-06-16T05:58:09Z | - | generated |
| `report_refresh_manifest` | fresh | 2026-06-16T05:58:01Z | - | 2026-06-16T05:53:29Z | - | generated |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/test-coverage-overview.md` | `5c8096063ef4627fe301c55db152507274507583728ddfe1d838c120bdeaa911` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/runtime/apache-runtime-results.generated.md` | `a28cd43ad41b51b5397b5d542e39aaaccce8fddd63cd0c5a0e06cfa1e5f05548` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/coverage/case-matrix.generated.md` | `6c2cf32f66b95482ba864f02b9c23a79f021efea6ec43d3cef15c63f043f6a55` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/coverage/connector-gap-summary.generated.md` | `30112aa6b53bbe12a9c556a55797f19433263e17a1ebd8ba8360ecf68d938956` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/coverage/coverage-summary.generated.md` | `685217f2e609c0dab93da959964ee7051ae5f40cabeea5e7837feb180bb4866f` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/runtime/haproxy-runtime-results.generated.md` | `f3d82897a6445b0406e1ef82c43eb0bb158624a186845ef72a35bcfda70226f3` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/runtime/nginx-runtime-results.generated.md` | `af7f8dd177fd37efd1ce5654bcc191bf79a33fc325922b9a030e93054004e410` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/coverage/phase-coverage.generated.md` | `adba249dc1947b867070bce66995422b5e2b1382a5dc869c940b7c26b9e519bc` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/runtime/runtime-matrix.generated.md` | `f1d38e3f1aa11d933e5072eb18fc97c6df67d40091368450fbe1c0937fc2617c` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/coverage/xfail-summary.generated.md` | `0846a9b025210a8230eef85ea2c21fbaa177f0eaaf09801c4db1137b7cac2165` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `6ad06c76b68ec65d7a60b26b5409cfa84c7277e45c1c48488bc3c081dec5e49f` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.md` | `88c53686af8ed22a6df85445ed579a6caf9eb059cb3792ac9d90be5dfc609314` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | `ef201dcb5ca9b34cbf5f9ab3da0155432d039d172c68772af3d7c7c5a6e9ea0a` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.md` | `8451d85bc8576f8316879e03204632ce4581a355e31fe30353ab389f63b43f67` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `83d51671872ea0d825c2c8cb8b45513768809f0538f240eae04881bbdc7d52c1` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.md` | `d5a68616af218960cead0b1878520cf112f78847ded912644e6fa5178f8e793a` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `8b6bfa1ccfca933d937939b21678b9543df4b9a125b9802c4b4ace67429daa24` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.md` | `3096c9ea75fdb7828f81fd939f27dc44d1014b1daf0aec07c9f5bf827733b100` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `0c993999eb0da54fd0b131b1170d183a7d38c68529d7bd8e63f9d5c45f2a96c7` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `a5fed8d79686c9688405e54f9e80b6eaa664b85b06d205c7914f0c936f57a1c3` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-full.generated.json` | `d8491f26ad38bce8967afdcdea0d538f3dd44e9fb8f60228bd96e44658c92afb` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-full.generated.md` | `fbc388c6fabc2131fda3dd9baa7c15966480a8f4265516125c557d824280d477` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | `410a57c9f3059a1bd9876227185044fdc74896cce1270eeb18434628648e2221` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.md` | `47b3d636ddebd0ab51d520bf5409c5a8f996fdb0f20c3dacfd5cdcdce4e132a2` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | `4be1206f0d2f50dd3b08893fc18ae6237b68ecd11476f824802ccea9733cac93` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.md` | `618b4acf1b5d5290595bed890fd82e20e84ee22c3645befe2ce78873a4cd2095` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | `76f13eeeb07f9680bd79fe061b8c3e7283630a80f2ecec31242b108e22c61161` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.md` | `e6a7c83840b4b62e25cbe9c92e9b5e911fe0365be73b832bfe0e79e6347ed0e6` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json` | `1f4c8b9040baccbd172c717c40116e4ea01296d78062886cbaa1a3ccb3cc4654` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.md` | `54a9bc01033302f194afe055b940850d183b8c221bd812a5a7d75cbe2842665d` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `0c993999eb0da54fd0b131b1170d183a7d38c68529d7bd8e63f9d5c45f2a96c7` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `a5fed8d79686c9688405e54f9e80b6eaa664b85b06d205c7914f0c936f57a1c3` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json` | `ea853430a51cf140efe5a29c350ec15cb586c158eb80fe252e8b9213b93c1b42` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.md` | `e0f419e064b8cfe58090b113b151769cb966c77e6653d9e589283c0fa1421e0f` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `0c993999eb0da54fd0b131b1170d183a7d38c68529d7bd8e63f9d5c45f2a96c7` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `a5fed8d79686c9688405e54f9e80b6eaa664b85b06d205c7914f0c936f57a1c3` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json` | `49bb0bf74ecc0e5ed80a547ccdb0876b7de88d4479df685c0193e0d2d5705da4` | `2026-06-15T21-01-39Z-9391a8d0` | stale |
| Declared input | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.md` | `4844b208867f6e587a0048db29f98fc011e64624e58c8bbb8ce94412a2bf7b41` | `2026-06-15T21-01-39Z-9391a8d0` | stale |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `0c993999eb0da54fd0b131b1170d183a7d38c68529d7bd8e63f9d5c45f2a96c7` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `a5fed8d79686c9688405e54f9e80b6eaa664b85b06d205c7914f0c936f57a1c3` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `d54beb4d40ea472648b5615ad1c493533ae642434a4cd62026a055fca9bda479` | `2026-06-15T21-01-39Z-9391a8d0` | stale |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.md` | `ed74183b02a05487010b6ccfbb01506b92ae4acf1530b0d223f9b895c9c0f4ea` | `2026-06-15T21-01-39Z-9391a8d0` | stale |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `6a543b34e8941ce08cc523fbb3492eeeeaed4f16ac4b925105f87bdb71c1247d` | `2026-06-15T21-01-39Z-9391a8d0` | stale |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.md` | `2ed89881c9b17d0d31145caf46ae132d165495e3f651c58a69d41a5997c2808c` | `2026-06-15T21-01-39Z-9391a8d0` | stale |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `7d6a5dc9ffaf32181caa561e8371b8b73077a42b7350d56dea0c2c497712934d` | `2026-06-15T21-01-39Z-9391a8d0` | stale |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.md` | `a4ea3dee1001f0882624513394e8401250e1298e5df4ddd43818afb03f9a5c9a` | `2026-06-15T21-01-39Z-9391a8d0` | stale |
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | `68d737435a1d14cf21aeaeb32fecf65b0283f5ad6da2192d849dd261b4587eeb` | `2026-06-15T21-01-39Z-9391a8d0` | skipped_stale_input |
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.md` | `2e8496cb47390b419338abe349b8ecdce3085320041e364acab3d75dfcab0e12` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json` | `063dd8a70bd170aba2eb05c6231787b00bbb6c03a06ffb52e9453689002a7c3c` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.md` | `831ed96bd6f2e13348c284475683cc3cc17aaf577c7cf007ca585001415a455f` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json` | `39a4083ed1e26c6fdf9069a83f4b6e428500ef6b7919c784d16a6623244f3d7f` | `2026-06-15T21-01-39Z-9391a8d0` | skipped_stale_input |
| Declared input | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.md` | `3e1384eb8a34ec8e4bb26da72b2a7c0368502081537fc2ed11a0140df54c9575` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json` | `bee021d0f08bd8e225ab21c6d42a604430dbbab5fa15f12695951827b5dde4bc` | `2026-06-15T21-01-39Z-9391a8d0` | skipped_stale_input |
| Declared input | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.md` | `20298989e3c7e2e2056a7dbb34c5077f89e28e8c94ce247a10c44ef9465138ea` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.json` | `9e1ead55a10b0f6205588b4c14516da3e47df27279a2062d577d73e9ba53bd2b` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.md` | `403596c0f76496003954c75e138cbf14adea8149acf315e9c2cbd1a0a1a85909` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/cache/runtime-component-cache.generated.json` | `cb6706def1a85d59cfb8562b1d15c697a2118f936f7319a9401b229206798c11` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/cache/runtime-component-cache.generated.md` | `45cdb3aff692c89b12052deb83ad3bae10c58433f3bf43bca8ca630a105971d3` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/cache/runtime-build-cache.generated.json` | `443a82e324f1acc1b0ab2faaa3304e7244e40bfd18e5666297bb3fed586c0d16` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/cache/runtime-build-cache.generated.md` | `6710a7aec9c0b8bf82a48f90200bf7ebf352e2313536d9fc6b60558b24643ec0` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/manifest/report-dependency-graph.generated.json` | `8783ab2c36d47b909473e4cc1960786e48d77064bbc5a1898cd2798f2fb6908a` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/manifest/report-dependency-graph.generated.md` | `5deb12fe1b5a87188e7ee969ac92dcd68a3ad9f4ec80ed943538ca1dc8dfe182` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/manifest/report-data-lineage.generated.json` | `8d38aa6a31fb2d833b65f65190ac426c47bf1e4e0860ae320da0c673d799f9c6` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/manifest/report-data-lineage.generated.md` | `002b0340fda1a51e6b1ae6acce3075b90c5c68cc2553988a45222d6de379b46e` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/manifest/report-path-migration.generated.json` | `ec5ce67241029c33028bd82345d1899fbb63c803db833befd12a36fb759ef1d0` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/manifest/report-path-migration.generated.md` | `b7ce9a42eb273e88e6967c7df77da10aedce4e236e30d57e007ce424dcf82a7c` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/manifest/generator-runtime-summary.generated.md` | `3b0c1a32a69b9332a7052dad194bacff63a857e9ff05964945f3b269796d51db` | `2026-06-15T21-01-39Z-9391a8d0` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/test-coverage-overview.md` | present | input file available |
| `reports/testing/generated/runtime/apache-runtime-results.generated.md` | present | input file available |
| `reports/testing/generated/coverage/case-matrix.generated.md` | present | input file available |
| `reports/testing/generated/coverage/connector-gap-summary.generated.md` | present | input file available |
| `reports/testing/generated/coverage/coverage-summary.generated.md` | present | input file available |
| `reports/testing/generated/runtime/haproxy-runtime-results.generated.md` | present | input file available |
| `reports/testing/generated/runtime/nginx-runtime-results.generated.md` | present | input file available |
| `reports/testing/generated/coverage/phase-coverage.generated.md` | present | input file available |
| `reports/testing/generated/runtime/runtime-matrix.generated.md` | present | input file available |
| `reports/testing/generated/coverage/xfail-summary.generated.md` | present | input file available |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.md` | present | input file available |
| `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | present | input file available |
| `reports/testing/generated/manifest/full-matrix-job-completeness.generated.md` | present | input file available |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | present | input file available |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.md` | present | input file available |
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/connector-work-queue.generated.md` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.md` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-full.generated.json` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-full.generated.md` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-apache.generated.md` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-nginx.generated.md` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-summary.generated.md` | present | input file available |
| `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json` | present | input file available |
| `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.md` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.md` | present | input file available |
| `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json` | present | input file available |
| `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.md` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.md` | present | input file available |
| `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.md` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.md` | present | input file available |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.md` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/canonical/next-fix-plan.generated.md` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/canonical/full-run-evidence.generated.md` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | skipped_stale_input | generated report input is not usable: status=skipped_stale_input |
| `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.md` | present | input file available |
| `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.md` | present | input file available |
| `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json` | skipped_stale_input | generated report input is not usable: status=skipped_stale_input |
| `reports/testing/generated/focused-analysis/body-processor-analysis.generated.md` | present | input file available |
| `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json` | skipped_stale_input | generated report input is not usable: status=skipped_stale_input |
| `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.md` | present | input file available |
| `reports/testing/generated/canonical/final-consistency-audit.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/canonical/final-consistency-audit.generated.md` | present | input file available |
| `reports/testing/generated/cache/runtime-component-cache.generated.json` | present | input file available |
| `reports/testing/generated/cache/runtime-component-cache.generated.md` | present | input file available |
| `reports/testing/generated/cache/runtime-build-cache.generated.json` | present | input file available |
| `reports/testing/generated/cache/runtime-build-cache.generated.md` | present | input file available |
| `reports/testing/generated/manifest/report-dependency-graph.generated.json` | present | input file available |
| `reports/testing/generated/manifest/report-dependency-graph.generated.md` | present | input file available |
| `reports/testing/generated/manifest/report-data-lineage.generated.json` | present | input file available |
| `reports/testing/generated/manifest/report-data-lineage.generated.md` | present | input file available |
| `reports/testing/generated/manifest/report-path-migration.generated.json` | present | input file available |
| `reports/testing/generated/manifest/report-path-migration.generated.md` | present | input file available |
| `reports/testing/generated/manifest/generator-runtime-summary.generated.md` | present | input file available |
