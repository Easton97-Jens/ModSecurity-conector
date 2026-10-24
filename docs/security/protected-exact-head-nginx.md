# Protected exact-head NGINX runtime infrastructure

**Language:** English | [Deutsch](protected-exact-head-nginx.de.md)

This change prepares a separately reviewed, protected-base control plane for
the native NGINX `modsecurity_use_error_log` exact-head test. It is
preparation only — no merge authorization.

## Trust boundary and hosted gate

The dispatcher and privileged launcher are sourced from the protected base
branch. They resolve an open canonical pull request through the GitHub API,
admit one full immutable candidate SHA as data, and check out only that SHA.
Before it executes a candidate Makefile, the candidate-build helper rejects any
root real, effective, or saved UID/GID. A correctly provisioned non-root,
isolated candidate runner remains an external host prerequisite. The protected
launcher owns the runtime cells and the collector records host-side process
identity, artifact provenance, callback/JSONL observations, WAF decisions, and
the final exit code. Candidate-controlled workflows, launchers, collectors,
evidence paths, secrets, and host sockets are not trusted inputs to the
privileged cell.

The privileged launcher is admissible only through a mandatory host gate. On a
dedicated protected runner, an administrator must preinstall a root-owned,
non-writable bootstrap at
`/usr/local/libexec/modsecurity-protected-exact-head/run-exact-base-launcher`.
That bootstrap must verify the requested protected-base Git object and copy the
launcher and its helpers into a root-owned temporary snapshot before executing
them. It must reject a missing or mismatched base SHA, mutable source path,
unsafe ownership/mode, and untrusted environment. The workflow is not a proof
that this host gate exists; the hosted environment must pass this prerequisite
before runtime evidence is admissible.

Callback and JSONL records are observations emitted by candidate code. They are
schema- and correlation-checked, but are not cryptographically or provenance-
authenticated semantic attestations: a malicious candidate could imitate
their contents. The independently root-observed process identity, network
namespace, transport-level HTTP 403, and exit status provide the trusted
boundary; the candidate WAF semantic decision and callback/JSONL fields remain
bounded, untrusted observations. The collector status is
`validated_observations`; its structured evidence labels callback/JSONL as
`candidate_scratch_untrusted` and the root HTTP observation as
`root_pidfd_network_namespace`. Linux `pidfd` plus `setns(CLONE_NEWNET)` binds
the root HTTP child to the validated network namespace. PID and namespace
lifetime checks must complete on the exact hosted head before any runtime result
is called verified.

The host AppArmor profile is deliberately `flags=(unconfined)`. It is used
only for host user-namespace admission and profile-label validation, not as a
claim of MAC confinement. Namespace isolation, capability bounding, and
`no_new_privs` are separate controls and must be validated independently.

The two fresh cells run the same exact candidate module with
`modsecurity_use_error_log` on and off. Evidence must show transaction
correlation, distinct master/worker identities, equivalent candidate-observed
WAF decisions, and the expected callback/JSONL difference. Any missing
prerequisite or exit 77 is a failure or an external blocked run; it is not a
passing result.

## Review package and current readiness

The detailed bilingual [review package](protected-exact-head-review-package.md)
records the threat model, trust boundaries, TCB inventory, process/FD and
artifact handoffs, cleanup state machine, workflow permissions, negative-test
matrix, and historic Sonar issue inventory.

The current source checkpoint adds root-owned retained directory, cell,
scratch, artifact, helper, and evidence descriptors. Evidence is published
descriptor-relatively; the private scratch tree is selected below a random
root-owned container and cleanup is confined to that container. Runtime
evidence is bound to both `tested_pr_head` and `tested_pr_base`. These are
repository-owned source contracts and local negative-control tests, not hosted
attestation. FND-PARENT-1038 remains in progress until its complete race
evidence is independently verified.

This checkout cannot verify a protected GitHub Environment or
dedicated labelled runner for this control plane. Therefore no hosted exact-head
result, independent attestation, or merge readiness is claimed. An
administrator must configure the environment reviewers, runner labels,
package/tool prerequisites, access policy, and the root-owned exact-blob host
gate before a manual protected-base dispatch can provide runtime evidence.
Final head, GitHub read-back, hosted runtime, and post-push Sonar results remain
pending exact-head validation and must be recorded in the post-push PR comment.

The candidate PR remains a separate delivery. This preparation does not alter
its product remediation, Framework/MRTS source, Gitlink, dependencies, branch
protection, or existing bypass controls.

## Validation contract

Local validation covers dispatcher identity and SHA admission, artifact
manifest binding, launcher path and descriptor controls, collector schema and
negative substitution cases, workflow static security contracts, shell syntax,
Python compilation, and action pin checks. The final acceptance evidence must
be collected from a fresh protected-base dispatch against the candidate's
GitHub-read-back head SHA and must include the complete on/off evidence schema.
A local source contract, an absent host gate, candidate callback/JSONL text, or
an earlier head cannot substitute for that evidence.

Preparation only — no merge authorization.
