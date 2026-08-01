# FND-PARENT-0068 — Apache cleanup runners execute compiler output from predictable shared temporary trees

## Identity

- Category: `security_validated`
- Repository / ownership: `parent` / `parent`
- Priority / severity / confidence: `P3` / `low` / `validated` (`0.72`)
- Status / feasibility: `in_progress` / `feasible_now`
- Release blocker / candidate-integration blocker / security relevance: `false` / `true` / `true`
- Connector / protocol / profile: `apache` / `local/shared-host CI and test-runner filesystem execution boundary` / `task-introduced uncommitted RulesSet-cleanup snapshot plus identical current request-transaction cleanup sibling`

## Summary

Retained security-diff evidence validates a task-introduced pre-remediation Apache RulesSet-cleanup runner weakness. It selects a predictable default below `/var/tmp/ModSecurity-conector-verified/build`, accepts only an absolute path, preserves an existing tree with `mkdir -p`, links a fixed binary name, and executes it. On a multi-user developer host or shared self-hosted runner, a lower-privileged actor can preseed or race that tree before the victim process.

The identical pre-existing request-transaction cleanup runner remains on Parent master. GitHub external-PR/token escalation is specifically counterevidenced: no `pull_request_target`, untrusted workflow input, writable token, or PR path reaches this runner. That counterevidence does not erase the independent local/shared-host execution path. The finding is remediation-required and `in_progress`, not fixed, verified, closed, committed, delivered, or merged.

## Observed and expected behavior

The retained pre-remediation candidate snapshot has the root control at `ci/checks/connectors/apache/check-apache-rules-set-cleanup.sh:8`, the absolute-only control at `:19–25`, and the `mkdir` / compiler-output / execution sink at `:82–91`. `OUT` comes from `APACHE_RULES_SET_CLEANUP_OUT`, `BUILD_ROOT`, or `/var/tmp/ModSecurity-conector-verified/build/apache-rules-set-cleanup`. `mkdir -p` preserves a pre-existing tree; the compiler creates the fixed `apache-rules-set-cleanup` filename and the script immediately executes it. Direct host evidence records `/var/tmp` as `root:root` mode `1777`, while the predictable project/build parents are ordinary mode `755` directories.

Current Parent source has the same pattern in `ci/checks/connectors/apache/check-apache-request-transaction-cleanup.sh` at lines `8`, `19–25`, and `81–89`: output-root selection, absolute-only check, `mkdir -p`, fixed `apache-request-transaction-cleanup` binary, and immediate execution. Each runner must instead create a fresh private mode-`700` output directory below a validated temporary parent and compile/execute only there. An inherited `OUT`, `BUILD_ROOT`, predictable default, existing directory, symlink, or final-name replacement must not become authority over compiler output or execution.

## Impact, source-to-sink path, and preconditions

```text
lower-privileged local/shared-host actor -> predictable sticky-/var/tmp output tree -> absolute-only OUT control -> mkdir -p preserves attacker-owned tree -> compiler writes a fixed binary name -> attacker races replacement -> victim script executes the substituted pathname
```

A successful race can cause one developer or shared-runner process to execute a substituted local binary under the victim identity, or redirect compiler output. The effect is potentially high for that process, but the vector is `localhost` and requires a multi-user/shared-host timing precondition. The retained attack-path analysis therefore calibrates this as low/P3. The evidence establishes neither a public endpoint nor a remote exploit, GitHub PR/token escalation, secret access, fleet-wide impact, connector request-processing effect, or a normal hosted-CI attacker path.

Preconditions are a lower-privileged local actor sharing `/var/tmp`, use of the predictable/default or otherwise controllable output root, a precreate/race before or between compiler/linker output and immediate fixed-name execution, and ordinary Apache/APXS/APR prerequisites that let the runner reach the sink.

## Affected scope, reproduction, and evidence

- `ci/checks/connectors/apache/check-apache-rules-set-cleanup.sh`: `APACHE_RULES_SET_CLEANUP_OUT`, `BUILD_ROOT`, `OUT`, `mkdir -p`, `apache-rules-set-cleanup`, and `BIN`.
- `ci/checks/connectors/apache/check-apache-request-transaction-cleanup.sh`: `APACHE_REQUEST_TRANSACTION_CLEANUP_OUT`, `BUILD_ROOT`, `OUT`, `mkdir -p`, `apache-request-transaction-cleanup`, and `BIN`.

Read the retained bounded validation and attack-path reports for the pre-remediation RulesSet snapshot, then inspect the current request-transaction sibling. Do not run a live cross-user race for this record task: it would require unsafe concurrent manipulation. The deterministic source-to-sink path plus the observed sticky ancestor establish the bounded local/shared-host precondition.

| Artifact | SHA-256 | Result |
| --- | --- | --- |
| `validation_report.md` | `05bcf8565c7de8f6fcadf2f607e8266ff762fd5e7296d9434066c78a4eada6f7` | Bounded static source/configuration trace and host metadata validate the local/shared-host path with confidence `0.72`; GitHub PR/token path is separately absent. |
| `attack_path_analysis_report.md` | `bf50d4a22613eeccc59d6b99d512e28f2d109c6315d21c097c22bf26f553171f` | Reportable localhost process-execution path; high effect per successful race, low likelihood, low/P3 severity. |
| Current request-transaction sibling | `9c4594c75e8848085de9f7f4b7dcc61f8984a80a106d6351904254683d7a37a5` | Direct source observation confirms the identical pre-existing instance. |

The pre-remediation candidate is classified as `CWE-73`, `CWE-59`, and `CWE-367`. The live candidate ledger changed after the pre-remediation observation and contains later remediation-validation data, so it is deliberately excluded from this record's acceptance evidence. The two hash-stable reports above govern the finding state; this does not claim a current candidate fix or change the `in_progress` status.

The retained scan artifacts are under `/var/tmp/codex/ModSecurity-conector/runs/selective-apache-prs-master-20260729/security-diff-scan/artifacts/05_findings/cand-apache-rules-set-cleanup-output-confinement/`.

## Root cause and remediation direction

The runner treats an absolute path string as sufficient authority and reuses a deterministic directory below a sticky shared ancestor. `mkdir -p` establishes neither ownership, freshness, permissions, non-symlink identity, nor a post-link binding. The compiler then emits a predictable binary name which the script executes.

Repair both Apache cleanup runners through one audited output-confinement contract: choose a validated temporary parent, create a fresh private mode-`700` directory using `mktemp -d`, compile and execute only inside that directory, and reject or remove externally selected deterministic output-root authority. Add negative source-contract coverage for a preseeded default or `BUILD_ROOT`, a symlink, and final-name replacement, plus legitimate APR compile/run coverage. Do not weaken workflow permissions, scanner exclusions, Quality Gates, compiler/APXS/APR behavior, or production Apache behavior.

## Acceptance criteria and validation plan

1. Both runners create a fresh private mode-`700` output directory below a validated temporary parent before compiler output exists.
2. A preseeded default, inherited `BUILD_ROOT`/`OUT`, symlink, or final-name replacement cannot select or replace the executable invoked by either runner.
3. Both legitimate Apache/APXS/APR harnesses compile and run in an isolated task-owned environment.
4. Focused source-contract, negative containment, legitimate-control, shell syntax, and security-diff checks pass without control weakening.
5. Fresh exact-head review and hosted checks exist before any `fixed`, `verified`, or `closed` disposition.

Required regressions are fresh-private-directory/no-inherited-output static contracts for both runners, preseeded-root/symlink/final-name negative controls, and shell syntax. Legitimate controls compile and run the RulesSet and request-transaction harnesses with verified Apache/APXS/APR prerequisites inside fresh task-owned output directories; normal hosted callers retain job-local temporary roots and read-only contents permissions.

## Deduplication, dependencies, and residual risk

The request-transaction runner is not a separate canonical finding. It has the same Parent owner, local/shared-host source, absolute-only output-root control, `mkdir -p` preservation, fixed-binary execution sink, security invariant, and fresh-private-directory remediation. It is a related pre-existing instance of this finding. `FND-PARENT-0064` concerns RulesSet APR lifecycle cleanup and `FND-PARENT-0043` concerns request-transaction memory lifecycle; neither owns this output-confinement/TOCTOU execution boundary.

Follow-up needs a task-owned Parent worktree, an audited temporary-parent contract, shell `mktemp`, Apache/APXS/APR/libmodsecurity prerequisites for the legitimate controls, and fresh exact-head hosted evidence. The sealed report remains pre-remediation evidence for the task-introduced RulesSet snapshot; the current sibling remains unresolved. No source repair, candidate-current-source, PR, hosted exact-head, merge, master, risk-acceptance, or closure claim is made by this record.

## History

- `2026-07-29T09:42:56Z`: retained validation and attack-path evidence created `FND-PARENT-0068` for the local/shared-host output-confinement path.
- `2026-07-29T09:42:56Z`: the identical pre-existing request-transaction runner was deduplicated into this canonical finding rather than assigned a second ID.
- `2026-07-29T10:04:18Z`: the mutable post-observation candidate ledger was excluded from acceptance evidence; the finding remains `in_progress`.
