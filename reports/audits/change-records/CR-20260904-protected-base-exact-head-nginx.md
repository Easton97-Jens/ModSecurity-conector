# Change Record

**Language:** English | [Deutsch](CR-20260904-protected-base-exact-head-nginx.de.md)

| Field | Value |
| --- | --- |
| Change ID | CR-20260904-protected-base-exact-head-nginx |
| Date (UTC) | 2026-09-04 |
| Base revision | 95bc04203455bc74a9cd18fafc6fb5848af2bbb2 |
| Scope | Parent-only protected-base preparation for independent NGINX exact-head evidence |
| Delivery status | Draft PR #355 successor remediation in preparation; no merge authorization |
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

## SonarCloud read-back and source remediation

The first published Draft-PR head
`78163d65dc19ee2cf1500dafa4d0f5d5cc36893b` received a fresh SonarCloud
Quality Gate `ERROR`: `new_security_rating=5` exceeds the configured threshold
of `1`. The authenticated PR inventory contained 26 Vulnerabilities and 72
Code Smells. Two `githubactions:S7630` rows were confirmed: the manually
dispatched PR number was rendered directly into shell source before the Python
validator could run. The successor passes that value only through a quoted
step environment variable.

The successor also strengthens dispatcher and collector file boundaries with
full-chain, descriptor-relative, no-follow operations; binds the collector
manifest to its fixed private task-root location; rejects writable input
artifacts; and moves sandbox temporary storage to a fresh private
`/run/nginx-exact-head-tmp` mount. The unprivileged candidate builder retains
the admitted task descriptor across candidate `make`; during packaging it
opens and retains the admitted build and package descriptors. It reads the
selected snapshot and fixed artifacts and publishes the fixed artifact names
and manifest only relative to those descriptors. Snapshot enumeration is
lexical only to select a candidate name; packaging opens its components below
the retained task descriptor. Controlled task-root, build-root, and
output-directory swap regressions prove that a replacement directory is not
used and that an identity change rejects the package result before return.
Focused source refactors preserve the existing fail-closed behavior. No
`NOSONAR`, issue or risk acceptance, scanner exclusion,
Quality-Gate/rule change, coverage reduction, or workflow weakening is used.
A fresh exact-successor Sonar analysis is still required; the initial head's
result is not evidence for a successor.

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

Focused Python `unittest`: passed, 86 tests. Python compilation, `/bin/sh -n`,
and `actionlint` for the protected workflow passed. Evidence-root and leaf
reads are descriptor-anchored, dispatcher/collector path-substitution
regressions pass, and JSON schema versions require an actual JSON integer, so
`true` cannot masquerade as version `1`. These are pre-successor-commit local
results only; hosted and Sonar evidence must be re-read for its exact SHA.

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
After the builder's final descriptor-identity checks, a same-UID candidate
background process could still race the lexical upload path returned to its
unprivileged caller. This is outside the builder's retained-descriptor
packaging window; the returned bundle is treated as untrusted by the root
launcher and re-admitted through fixed-name descriptor/digest checks. Exact
hosted-runner evidence is still required for that handoff.

## Checks not run and rationale

Protected hosted NGINX runtime and independent host attestation were not run
because the required environment and runner are unavailable. PR #354/Sonar
remediation checks are outside this Base-preparation scope.

## Final diff and review status

Local checks passed as recorded above. Hosted verification remains blocked; this
is preparation only and has no merge authorization.

## Local validation observed

The focused Python unit suite for the protected dispatcher, builder, preflight,
launcher, collector, helper, and workflow contracts passed with 86 tests.
Descriptor-anchored evidence-root/leaf reads, dispatcher/collector
path-substitution regressions, strict rejection of boolean schema versions,
and environment-variable-only handling of the dispatched PR number and expected
SHA passed. Candidate task/build/output-directory swap regressions also passed:
replacement directories are not used, and replaced task/output identities fail
closed before a package path is returned.
Python compilation and shell syntax checks passed. `actionlint` passed for
`.github/workflows/run-protected-nginx-exact-head.yml`. A local Bubblewrap
mount-layout probe is blocked by this container's namespace policy and is not
claimed as a host-runtime result. A hosted NGINX runtime, protected Environment,
dedicated runner, and independent attestation were not available locally and
remain blocked external evidence.
