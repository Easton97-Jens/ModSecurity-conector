# Change Record: NGINX case audit-log pointer

**Language:** English | [Deutsch](CR-20261001-nginx-audit-result-pointer.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20261001-nginx-audit-result-pointer` |
| Date (UTC) | `2026-10-01` |
| Base revision | `2634d821acd80ad208a8e1cd3e4f49fd7e80c628` |

## Motivation and problem statement

The host writes its audit log under `NGINX_SERVER_LOG_ROOT`, but its case
result pointed to `output_dir/audit.log`. These differ in the root/nobody
layout, so the collector could not read the real audit via the declared path.

## Acceptance criteria

Both result-writing branches use the actual `AUDIT_LOG_FILE`. Early results
before that assignment retain their case-local fallback. No synthetic events,
PASS promotion, collector change, or Framework-validator relaxation.

## Implementation decision and rationale

Pass `${AUDIT_LOG_FILE:-$output_dir/audit.log}` to the existing case-info CLI.
Log placement, ownership, projection, and collection authority remain intact.

## Changed files

- `connectors/nginx/harness/run_nginx_smoke.sh`
- `tests/test_nginx_audit_result_pointer.py`
- This English/German Change Record pair and its archive index entries.

## Commands executed

All shell commands used RTK. The behavior regression first failed on the
wrong pointer; after correction three tests passed. The combined Parent
protocol-wiring, selected-runner, audit-pointer, Phase-4 wiring, projection,
path-authority, projection-invocation, and native-sink focus run passed 58
tests. Fixture-dependent tests used the unchanged Framework pin
`cc36b37d0f6a0fbc3512f3878a691751e91c5fbb`. `sh -n`, `shellcheck -S error`,
and `git diff --check` passed. Full ShellCheck still reports pre-existing
warnings; none were suppressed. `make check-bilingual-docs check-doc-links`
passed; the first documentation attempt required correcting the language-switch format.

## Security impact

This corrects evidence reachability, not validation semantics. Native-event,
case/run identity, containment, and root-master/nobody-worker controls remain
unchanged. The fallback does not turn missing evidence into PASS.

## Runtime evidence

Earlier isolated host probes reproduced an absent declared audit path and
nonempty actual audit log. The new tests capture the real shell function's
CLI arguments; they are not runtime or canonical PASS evidence.

## Known limitations

This does not supply the remaining 54 required H1 paths or repair the
independent downstream-protocol caller contract.

## Remaining risks

An audit pointer cannot replace required native events. A new exact-head
lifecycle remains necessary after all coverage gates pass.

## Checks not run and rationale

No new full E2E, canonical PASS, or SHA256SUMS: required runner coverage is
red. No remote CI, push, PR mutation, merge, or MRTS change occurred.

## Final diff and review status

The pointer diff was independently reviewed. This record concerns only that
correction, not other uncommitted Parent integration work.
