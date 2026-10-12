# Request/response body-limit stack checklist

**Language:** English | [Deutsch](response-limit-stack-checklist.de.md)

## Stack and acceptance

[PR #407](https://github.com/Easton97-Jens/ModSecurity-conector/pull/407) uses
`fix/engine-owned-response-limits-stack-20261011`, stacked on #382 branch
`fix/unified-native-results-events-20260921`. Base updates require fresh review;
normal base merges into #407 preserve history. No merge into #382/master,
force-push or history rewrite is authorized. I09/#408 and I11/#406 are integrated;
I10/#409 and I12/#410 remain separate.

Ready for review requires all seven user acceptance criteria. Ready to merge
additionally requires the applicable integration/security/host acceptance.
Read actual Draft/head/base state and exact-head checks from GitHub; this source
document does not certify future commits or encode a stale delivery SHA.

## Product checks

- [x] Remove Common/adapter/service request and response size policies, defaults, parser/merge/fallback gates and connector `body_limit_action`.
- [x] Reject removed options; native directives exclusively choose inspection limits and Reject/ProcessPartial.
- [x] Preserve explicit directional engine policies in fixtures; no hidden fixture defaults.
- [x] Retain pointer/overflow/file/descriptor/frame/message/header/event/timeouts and bounded reusable buffers/private spooling.
- [x] Classify authorization samples independently of engine policy and full native streaming; document unsupported framing.
- [ ] Complete all active-profile full request/response host matrices: independent host/sample limitations and I12 cases remain.

The [ten-profile matrix](body-inspection-review-matrix.md) provides separate
request/response paths, actual evidence layers, all four remaining limits and
durable baseline follow-ups. It records Apache native Reject at append/after
commit and SPOP completeness enforcement before engine admission. Category 4
limitations are never marked fully implemented.

## Review gates and retained evidence

The matrix records observed Common native, Apache APR/C17 and selected SPOP/
combined host results. The repaired SPOP fixture passes the fresh 64-test suite;
its earlier failure is retained as superseded evidence. Historical quick,
Envoy and CI/Sonar success proves only the corresponding tested revision; it
cannot verify new repairs. No scanner exclusions or weakened assertions are
permitted.

- Final affected tests/builds, quick-check, documentation/generators and sensitive former-limit mutation control require fresh run evidence before Ready.
- Final independent redacted secret scan requires its own proof; the master-only secret workflow is not proof for this stacked PR.
- Final exact-head GitHub checks and Sonar require Quality Gate OK, zero new open/accepted issues, hotspots and duplication; expected skips need explicit provenance.
- GitHub Ready transition and readback require all seven criteria; verify unchanged branch names and isDraft=false.

These rules are acceptance requirements, not a remote status feed. The
[live checks](https://github.com/Easton97-Jens/ModSecurity-conector/pull/407/checks)
and final run readback establish their disposition. Sonar without measured
coverage is not a substitute for executable tests.

## Remaining independent evidence

Complete I12/V08–V10 host coverage remains not_run for all ten profiles, including
negotiated protocols, ownership/commit timing and late-abort proof. Selected
Envoy HTTP/1 and combined HAProxy probes do not complete it. Foreign-UID and
read-only-mount spool probes are blocked by root-only UID maps/chown EINVAL and
namespace EPERM; compilation or cached binaries cannot replace them.

FU-COMMON-LOSSY-CONTRACT and FU-STOCK-RST-DELIVERY remain independent baseline
failures with unchanged assertions and exact base/current comparisons in the
matrix. Complete removal of every active total-body restriction is not claimed:
Envoy ext_authz and Traefik forwardAuth remain host full-sample routes, SPOP
remains a bounded complete message, and independent host request-size controls
remain. Native ext_proc, native Traefik UDS and HTX are their streaming alternatives.
The 32768-byte authorization-response safeguard remains separate from application
response inspection. See the [ownership contract](phase4-mode-budget.md) and
[Change Record](../reports/audits/change-records/CR-20261011-response-limit-policy-removal.md).
