# Change Record

**Language:** English | [Deutsch](CR-20260904-protected-base-exact-head-nginx.de.md)

| Field | Value |
| --- | --- |
| Change ID | CR-20260904-protected-base-exact-head-nginx |
| Date (UTC) | 2026-09-04 |
| Base revision | 2b3d7f7f0bec006b236b5998d011069c9125033f |
| Scope | Parent-only protected-base preparation for independent NGINX exact-head evidence |
| Delivery status | Draft PR #355 branch-only Base merge `5368569351e968e8ea641fc485590654df6a4336` plus protected-workflow remediation checkpoint `fa9064a560b31b377dc1dea3a9b8b99e6867809c`; no merge authorization |
| Candidate | PR #354, exact head must be resolved and read back at dispatch time |

## Purpose

This record documents the separately reviewed control-plane preparation needed
to test a candidate NGINX module without allowing the candidate PR to own the
privileged launcher or evidence collector. The trusted base dispatcher binds
the canonical open PR and full head SHA; the unprivileged build packages fixed
artifacts; a protected base launcher executes the two native on/off cells; and
an independent collector emits bounded host-side evidence.

Preparation only — no merge authorization.

The branch-only checkpoint is a normal merge of current `origin/master`
`2b3d7f7f0bec006b236b5998d011069c9125033f` into the Draft PR branch; its
other parent is the prior PR head
`de1c3c05b53a00e077aca1c08a2fcdc552b0344e`. It does not merge PR #355 or PR
#354 into `master`. The historical common base remains
`95bc04203455bc74a9cd18fafc6fb5848af2bbb2`.

## Final successor update — source checkpoint `fa9064a5`

GitHub's fresh `zizmor` result for the prior successor `737c9674…` identified
a direct expansion of `needs.resolve.outputs.tested_pr_head` into the candidate
SHA comparison's Bash `run:` body.  The normal follow-up commit
`fa9064a560b31b377dc1dea3a9b8b99e6867809c` binds that dispatcher-admitted
value only as step-local `VALIDATED_PR_HEAD` data and compares the quoted shell
variable.  The exact checkout `ref` remains an Action input; the protected
Framework Gitlink comparison, unprivileged build, root-owned host gate, and
all later privilege boundaries are unchanged.  This is the scoped remediation
for `FND-PARENT-1034`, not a workflow suppression or Quality-Gate change.

At documentation-successor checkpoint `90735926`, the exact seven-module command
`python -B -m unittest -q tests.test_nginx_exact_head_base_helper tests.test_nginx_exact_head_result_collector tests.test_nginx_exact_head_root_launcher tests.test_protected_nginx_exact_head_builder tests.test_protected_nginx_exact_head_dispatcher tests.test_protected_nginx_exact_head_runner_preflight tests.test_protected_nginx_exact_head_workflow`
passed 99 focused protected-base tests; 22 bilingual tests also passed at that
successor checkpoint.  The separately scoped workflow-plus-dispatcher 29-test
control passed at source checkpoint `fa9064a5`. Python compilation, POSIX shell
syntax, `actionlint`, offline `zizmor`, policy audit, variable-documentation
checking, and `git diff --check` passed in the corresponding successor
validation. The dedicated two-file source-successor scan is sealed and valid at
`security-diff-final-fa9064a5/report.md`; it reports no surviving source
finding and explicitly partial hosted/runtime coverage.  `make check-nginx-c17`
is **blocked**, not passed: supported NGINX headers/source are unavailable and
the underlying target returns exit 77.  Broad documentation-link checks remain
blocked only by the inherited uninitialized Framework Gitlink; it was neither
initialized nor changed.

SonarCloud analyzed exactly `fa9064a5` at `2026-09-04T19:44:32+0000`.
GitHub check `101153230682` completed with `failure` at `19:46:39Z`; the gate
is `ERROR` because `new_security_rating=3` exceeds required `1`.  The other
gate conditions are OK.  The authenticated current inventory contains the
same 80 open keys as the preceding exact head (15 Vulnerabilities and 65 Code
Smells); every key has a retained individual source/sink/privilege/ownership
triage.  The aggregate result is `A=0`, `B=26`, `C=35`, `D=19`; no issue is
silently called a false positive, and unsafe cosmetic changes remain
`blocked_by_security_invariant`.  The fresh GitHub `zizmor` check for
`fa9064a5` succeeded.  These are checkpoint facts only: the final normal
documentation-successor push, its exact remote read-back, and its fresh checks
are separately required and may not reuse an earlier green run as proof.

`FND-PARENT-1013` remains `fixed, verification pending`.  `FND-PARENT-1034`
is `fixed, verification pending` until the successor delivery evidence is
reconciled.  No eligible independent GitHub collaborator exists for the
required reviewer request; no access, invitation, or invented review was made.

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

Those SonarCloud values are retained historical read-back for
`78163d65dc19ee2cf1500dafa4d0f5d5cc36893b`, not current-head evidence. This
record has no immutable local Sonar artifact or current check-run URL for that
historical query; its provenance is therefore `not_verified` for the current
reviewed source. A new authenticated PR #355 inventory and Quality Gate query
are required after the final normal branch push.

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

The post-merge source review additionally found that the candidate builder
could reach its candidate-controlled `Makefile` under a root-configured runner
because it did not reject real, effective, or saved root identities. The
builder now rejects every root UID/GID before candidate path access or the
fixed `make` vector, and emits the admitted `nginx` binary with fixed `0500`
mode while data-only module/library artifacts remain `0400`. Regression tests
exercise root rejection, non-root controls, non-executable binary rejection,
and fixed output modes. This is the source correction for
`FND-PARENT-1032`; it remains verification-pending until final exact-head
validation and read-back complete.

The successor source review also found an inherited root-control-file race in
the same launcher boundary. A candidate can write the runner-owned cell runtime
directory. The former publisher closed a predictable temporary pathname before
path-based replacement, after which the release and completion callers applied
path-based root metadata operations. A substituted symlink could therefore
redirect root `chmod` or `chown`; moreover the ordinary completion path rejected
its intentionally missing leaf. The corrected central publisher retains a
no-follow parent descriptor, writes, mode-checks, and identifies the temporary
file by descriptor before descriptor-relative replacement, then reopens and
compares the published leaf without following it. Callers no longer apply
post-publication path-based metadata changes. Controlled pre-fix tests showed
the release race did not fail closed and a task-owned victim mode changed from
`0644` to `0400`; the post-fix regressions reject both release and completion
substitution and the ordinary completion control publishes correctly. Release
and completion markers now live below a root-owned cell hierarchy in a
separately created candidate-non-writable control directory; the Base helper
verifies that directory before it trusts either fixed marker, so a candidate
cannot recreate one after publication. A fresh exact-successor source and
hosted review remains required.

## Scope exclusions

No product remediation, Framework/MRTS source, Gitlink, dependency, branch
protection, merge, force-push, secret, privileged PR workflow, or Sonar
suppression is part of this record. `FND-PARENT-1013` remains `fixed,
verification pending`. `FND-GITHUB-0009` remains open until a fresh protected
runtime validates the acceptance criteria and the host-gate/lifetime controls.
`FND-PARENT-1032` is a Parent-only source correction and does not reduce the
separate host-gate or runner-isolation prerequisite.

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

The protected-base diff from current Base contains exactly these 23 paths:

- `.github/actionlint.yaml`
- `.github/workflows/run-protected-nginx-exact-head.yml`
- `ci/runtime/broker/nginx_exact_head_result_collector.py`
- `ci/runtime/broker/nginx_exact_head_root_launcher.py`
- `ci/runtime/broker/protected_nginx_exact_head_builder.py`
- `ci/runtime/broker/protected_nginx_exact_head_dispatcher.py`
- `ci/runtime/broker/protected_nginx_exact_head_runner_preflight.py`
- `ci/runtime/broker/run_nginx_exact_head_cells.sh`
- `docs/security/protected-exact-head-host-gate.de.md`
- `docs/security/protected-exact-head-host-gate.md`
- `docs/security/protected-exact-head-nginx.de.md`
- `docs/security/protected-exact-head-nginx.md`
- `reports/audits/change-records/CR-20260904-protected-base-exact-head-nginx.de.md`
- `reports/audits/change-records/CR-20260904-protected-base-exact-head-nginx.md`
- `reports/audits/change-records/README.de.md`
- `reports/audits/change-records/README.md`
- `tests/test_nginx_exact_head_base_helper.py`
- `tests/test_nginx_exact_head_result_collector.py`
- `tests/test_nginx_exact_head_root_launcher.py`
- `tests/test_protected_nginx_exact_head_builder.py`
- `tests/test_protected_nginx_exact_head_dispatcher.py`
- `tests/test_protected_nginx_exact_head_runner_preflight.py`
- `tests/test_protected_nginx_exact_head_workflow.py`

## Commands executed

### Tests and actual results

The following local results were observed for source checkpoint
`53aee10ddeb448ed7506e645709d2162aeab091f`; the final branch read-back and
hosted checks remain separately required.

- `python -B -m unittest -q tests.test_protected_nginx_exact_head_dispatcher tests.test_protected_nginx_exact_head_builder tests.test_protected_nginx_exact_head_runner_preflight tests.test_nginx_exact_head_root_launcher tests.test_nginx_exact_head_result_collector tests.test_nginx_exact_head_base_helper tests.test_protected_nginx_exact_head_workflow` — passed, 98 tests.
- `python -B -m unittest -q tests.test_bilingual_docs` — passed, 22 tests.
- `python -B -m unittest -q tests.test_event_runtime_security_contract tests.test_nginx_native_security_contract tests.test_nginx_upstream_security_contract tests.test_connector_config_reference tests.test_sonar_reliability_contract` — passed, 48 tests.
- `python -B -m py_compile` for the five protected broker Python files — passed; `sh -n` and `bash -n` for `run_nginx_exact_head_cells.sh` — passed; `actionlint .github/workflows/*.yml` — passed.
- `make check-variable-documentation` — passed, 101 documented variable references; Parent local-policy validation — consistent; `git diff --check` — passed before staging.
- `make check-nginx-c17` — blocked: supported NGINX headers/source are absent, and its underlying target returned exit 77. This is not a passing native NGINX result.
- `make check-bilingual-docs` and `make check-doc-links` — blocked solely by pre-existing missing links inside the uninitialized Framework Gitlink; the Change-Record-specific German-link failure was corrected.

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
