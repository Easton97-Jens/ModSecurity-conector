# Change Record

**Language:** English | [Deutsch](CR-20260904-protected-base-exact-head-nginx.de.md)

| Field | Value |
| --- | --- |
| Change ID | CR-20260904-protected-base-exact-head-nginx |
| Date (UTC) | 2026-09-04 |
| Base revision | 95bc04203455bc74a9cd18fafc6fb5848af2bbb2 |
| Scope | Parent-only protected-base preparation for independent NGINX exact-head evidence |
| Delivery status | Separate Draft PR preparation; no merge authorization |
| Candidate | PR #354, exact head must be resolved and read back at dispatch time |

## Purpose

This record documents the separately reviewed control-plane preparation needed
to test a candidate NGINX module without allowing the candidate PR to own the
privileged launcher or evidence collector. The trusted base dispatcher binds
the canonical open PR and full head SHA; the unprivileged build packages fixed
artifacts; a protected base launcher executes the two native on/off cells; and
an independent collector emits bounded host-side evidence.

Preparation only — no merge authorization.

## Acceptance criteria

- Every privileged command and evidence parser is selected from protected base
  source, with no candidate workflow or shell execution under privilege.
- The dispatcher reads back the canonical repository, PR state, base and full
  head SHA, then admits only that immutable candidate revision.
- Artifact and runtime evidence are bound to the candidate SHA and trusted base
  digest; candidate-writable paths cannot replace them.
- Fresh on/off cells provide independently root-observed distinct master/worker
  identities, transaction-correlated callback/JSONL observations, equivalent
  candidate-observed WAF decisions, and exit 0. The transport-level HTTP 403
  and identity boundary are root-observed; the candidate WAF semantic decision
  and Callback/JSONL are bounded sandbox observations, not cryptographically or
  provenance-authenticated semantic attestations. The collector status is
  `validated_observations`, with `candidate_scratch_untrusted` for callback/
  JSONL and `root_pidfd_network_namespace` for root HTTP.
- Negative substitution, path, descriptor, environment, and runner controls
  fail closed; no bypass or quality-gate weakening is introduced.

## Mandatory hosted gate

The privileged workflow is admissible only on a dedicated protected runner
with a preinstalled root-owned, non-writable bootstrap at
`/usr/local/libexec/modsecurity-protected-exact-head/run-exact-base-launcher`.
The bootstrap must validate the protected-base Git object and copy the exact
launcher/helpers into a root-owned temporary snapshot before execution. It must
reject mutable source paths, unsafe ownership/modes, mismatched base SHA, and
untrusted environment. This repository does not provision or attest that host
component; its absence blocks hosted evidence.

## Evidence status

Local source-contract and unit-test evidence is the only evidence available at
this record update. GitHub currently has no configured protected Environment or
dedicated labelled runner for the privileged job. Consequently the exact-head
host run, independent runtime attestation, and final PR #354 verification are
blocked/not verified and are not inferred from earlier runs.
Linux `pidfd` plus `setns(CLONE_NEWNET)` is the source-level lifetime boundary
for the root HTTP child. Its hosted runtime proof still requires validation on
the exact hosted head; no runtime proof is recorded here.

The host AppArmor profile is intentionally `flags=(unconfined)`. It provides
host user-namespace admission and profile-label validation only; it is not a
MAC-confinement claim. Namespace isolation, capability bounding, and
`no_new_privs` remain separate controls requiring independent validation.

## Scope exclusions

No product remediation, Framework/MRTS source, Gitlink, dependency, branch
protection, merge, force-push, secret, privileged PR workflow, or Sonar
suppression is part of this record. `FND-PARENT-1013` remains `fixed,
verification pending`. `FND-GITHUB-0009` remains open until a fresh protected
runtime validates the acceptance criteria and the host-gate/lifetime controls.

## Required next evidence

After protected Environment and runner provisioning, dispatch from the reviewed
base, read back the exact candidate SHA from GitHub, and retain the complete
collector record including `tested_pr_head`, `trusted_dispatcher_base_sha`,
NGINX version/source digest, module digest, master/worker identities, on/off
callback and JSONL results, WAF decisions, `decision_equivalent`, and
`final_exit_code`.

## Identity

Parent-only preparation record for the protected-base exact-head control plane;
not a product-remediation record for PR #354.

## Motivation and problem statement

Candidate-controlled PR code cannot own privileged runtime launch or evidence
collection while its exact head is being tested.

## Implementation decision and rationale

Use protected Base admission, the mandatory host gate, unprivileged build, and
root-side collection. Root HTTP uses Linux `pidfd` and `setns(CLONE_NEWNET)`;
candidate WAF semantics and callback/JSONL remain observations.

## Changed files

See the protected dispatcher, builder, preflight, launcher, collector, helper,
workflow, focused tests, and bilingual documentation files in this Draft PR.

## Commands executed

Focused Python `unittest`: passed, 72 tests. Python compilation, `/bin/sh -n`,
and `actionlint` for the protected workflow passed. Evidence-root and leaf
reads are descriptor-anchored, and path-substitution regression coverage
passed. JSON schema versions require an actual JSON integer, so `true` cannot
masquerade as version `1`.

## Security impact

The control plane fails closed for source, SHA, path, descriptor, environment,
and runner substitutions. Root-observed transport HTTP 403 and process identity
are the boundary; candidate WAF semantic values and callback/JSONL are not
trusted attestations.

## Runtime evidence

No hosted runtime evidence exists for this head. Required collector status is
`validated_observations`, with `root_pidfd_network_namespace` and
`candidate_scratch_untrusted` labels.

## Known limitations

The host bootstrap, protected Environment, dedicated runner, and independent
attestation are external prerequisites unavailable in this checkout.

## Remaining risks

Candidate code can imitate callback/JSONL and WAF semantic values. PID/namespace
lifetime and host-gate behavior still require exact-head hosted validation.

## Checks not run and rationale

Protected hosted NGINX runtime and independent host attestation were not run
because the required environment and runner are unavailable. PR #354/Sonar
remediation checks are outside this Base-preparation scope.

## Final diff and review status

Local checks passed as recorded above. Hosted verification remains blocked; this
is preparation only and has no merge authorization.

## Local validation observed

The focused Python unit suite for the protected dispatcher, builder, preflight,
launcher, collector, helper, and workflow contracts passed with 72 tests.
Descriptor-anchored evidence-root/leaf reads and path-substitution regression
coverage also passed, as did strict rejection of boolean schema versions.
Python compilation and shell syntax checks passed. `actionlint` passed for
`.github/workflows/run-protected-nginx-exact-head.yml`. A hosted NGINX runtime,
protected Environment, dedicated runner, and independent attestation were not
available locally and remain blocked external evidence.
