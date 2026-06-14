# Testing Reports

Status: current merge-readiness index.

This directory contains connector-owned runtime evidence and generated analysis
reports. Generated files under `generated/` must be refreshed through Make
targets and generators; do not patch them by hand.

## Current Merge Snapshot

| Area | Current evidence |
| --- | --- |
| SonarCloud PR #13 | Quality Gate `OK`; Reliability `A`; Security `A`; Bugs `0`; Vulnerabilities `0`; Security Hotspots `0 open / 100% reviewed` |
| Full-Matrix | `3074 PASS / 782 FAIL / 0 BLOCKED` |
| Final consistency audit | `recommended_next_fix_cluster: none` |
| Active runtime-fixable clusters | none |
| Body/XML/Multipart active clusters | `0` |
| Audit/nolog active cluster | `0` |
| Intervention-blocking active cluster | `0` |
| Phase 4 hard-abort capability | classified as `not_next`; bounded strict evidence only |

The remaining 782 Full-Matrix FAIL rows are still visible in the generated
reports. They are classified as semantic differences, capability gaps,
report-only cases, or `not_next` work that should not be solved by changing
Expected statuses, rules, or PASS/FAIL values.

## Canonical Generated Reports

| Report | Purpose |
| --- | --- |
| [full-runtime-matrix.generated.md](./generated/full-runtime-matrix.generated.md) | Complete connector Full-Matrix result summary |
| [full-run-evidence.generated.md](./generated/full-run-evidence.generated.md) | Evidence rollup for the current full-run inputs |
| [connector-work-queue.generated.md](./generated/connector-work-queue.generated.md) | Connector-scoped queue and classification state |
| [phase-work-queue.generated.md](./generated/phase-work-queue.generated.md) | Phase-scoped queue and classification state |
| [remaining-failure-analysis.generated.md](./generated/remaining-failure-analysis.generated.md) | Remaining failure clustering and classification |
| [next-fix-plan.generated.md](./generated/next-fix-plan.generated.md) | Current recommendation; should remain `none` for this merge state |
| [final-consistency-audit.generated.md](./generated/final-consistency-audit.generated.md) | Merge-readiness consistency gate |
| [report-refresh-manifest.generated.md](./generated/report-refresh-manifest.generated.md) | Generator catalog and refresh inputs |

## Focused Analysis Reports

| Report | Purpose |
| --- | --- |
| [body-processor-analysis.generated.md](./generated/body-processor-analysis.generated.md) | Request-body, multipart, and XML processor classification |
| [intervention-blocking-analysis.generated.md](./generated/intervention-blocking-analysis.generated.md) | Intervention blocking classification and no-match separation |
| [no-mrts-intervention-nomatch-analysis.generated.md](./generated/no-mrts-intervention-nomatch-analysis.generated.md) | Framework-owned no-MRTS no-match semantics |
| [nolog-audit-evidence.generated.md](./generated/nolog-audit-evidence.generated.md) | Explicit `nolog` audit-evidence classification |
| [phase4-hard-abort-capability.generated.md](./generated/phase4-hard-abort-capability.generated.md) | Phase 4 hard-abort capability evidence |
| [response-header-hook-analysis.generated.md](./generated/response-header-hook-analysis.generated.md) | Response-header hook and backend setup analysis |
| [rule-chain-semantics-analysis.generated.md](./generated/rule-chain-semantics-analysis.generated.md) | Rule-chain semantics and runtime-fixability analysis |

## Runtime And Native Evidence

| Report | Purpose |
| --- | --- |
| [apache-runtime-results.generated.md](./generated/apache-runtime-results.generated.md) | Apache runtime summary |
| [nginx-runtime-results.generated.md](./generated/nginx-runtime-results.generated.md) | NGINX runtime summary |
| [haproxy-runtime-results.generated.md](./generated/haproxy-runtime-results.generated.md) | HAProxy runtime summary |
| [runtime-matrix.generated.md](./generated/runtime-matrix.generated.md) | Default runtime matrix summary |
| [mrts-native-apache.generated.md](./generated/mrts-native-apache.generated.md) | Apache native MRTS infrastructure evidence |
| [mrts-native-nginx.generated.md](./generated/mrts-native-nginx.generated.md) | NGINX native MRTS infrastructure evidence |
| [mrts-native-summary.generated.md](./generated/mrts-native-summary.generated.md) | Native MRTS summary |
| [mrts-native-full.generated.md](./generated/mrts-native-full.generated.md) | Combined native MRTS report |
| [runtime-build-cache.generated.md](./generated/runtime-build-cache.generated.md) | Runtime build-cache report |
| [runtime-component-cache.generated.md](./generated/runtime-component-cache.generated.md) | Runtime component-cache report |

Native MRTS infrastructure reports are separate from connector Full-Matrix
evidence. They compare upstream-style native behavior where available and must
not be used to overwrite connector Expected statuses.

## Refresh And Pre-Merge Checks

Refresh connector reports:

```sh
FRAMEWORK_ROOT=/path/to/ModSecurity-test-Framework make refresh-all-reports
```

Refresh framework-owned generated docs:

```sh
make -C modules/ModSecurity-test-Framework refresh-framework-reports
```

Before merging, run lint and quick checks for both repositories, dry-run the
full-matrix and native-MRTS targets, and verify the final consistency audit. Do
not commit runtime caches, generated MRTS rules, generated FTW YAML, load files,
job directories, bytecode caches, or temporary smoke output.
