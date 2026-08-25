# Change Record

**Language:** English | [Deutsch](CR-20260825-trusted-lighttpd-runtime-supervisor-infrastructure.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260825-trusted-lighttpd-runtime-supervisor-infrastructure |
| Date (UTC) | 2026-08-25 |
| Base revision | `5d71be74369123257851eb5ec612d7523a6b061d` |
| Delivery status | A separate Parent Draft PR is authorized. No merge, auto-merge, direct default-branch push, Framework/MRTS change, or Gitlink update is authorized by this record. |

## Motivation and problem statement

The protected Lighttpd namespace dispatcher currently proves only its
constrained namespace fixture. It must not present that result as host-runtime
evidence, and PR-writable plans, results, events, or summaries cannot prove a
real Lighttpd runtime. The missing control is a protected-master-owned
supervisor that creates and observes the runtime itself.

## Acceptance criteria

- A standard-library supervisor accepts only a closed, sealed artifact plan and
  fails closed before a subprocess starts when any identity, path, ownership,
  digest, no-CRS, or privilege invariant is absent.
- The supervisor starts the exact sealed Lighttpd binary as a non-root identity,
  independently observes its executable, connector module, and loopback socket,
  sends fixed control/detection/negative probes, and writes a private receipt.
- The dispatcher summary is bound only to the protected fixture step and says
  explicitly that neither the supervisor nor runtime evidence was invoked.
- Static mutations prevent the summary or status from calling the fixture a
  Lighttpd runtime result.
- No NGINX, Framework, MRTS, Gitlink, dependency, lockfile, toolchain, or PR
  #335 change is included.

## Implementation decision and rationale

`trusted_lighttpd_runtime_supervisor.py` is deliberately a protected-runtime
primitive rather than a PR workflow step. It validates a complete digest
manifest for every regular file in the root-owned sealed tree, rejects extra
files, symlinks, mutable ownership, hard links, Linux file capabilities, and
set-ID bits, and requires a separate private receipt root. It reads the
generated configuration through the same no-follow descriptor used for its
digest, rejects CRS references and includes, and rejects every `rules_file`
and `event_path` directive until a separate canonical protected rule/data
provenance contract exists. It records that static check as distinct from
runtime provenance and blocks before it can start Lighttpd or emit a `PASS`
receipt. It sets both
`MSCONNECTOR_CRS_RUNTIME=0` and `MODSECURITY_RULESET=no-crs` in the child
environment.

The later enabled start path has a fixed argument vector and a new process
group. It may start only as PID 1 in its private PID namespace, binds the child
PID to a start-time token, checks `/proc` for the sealed executable and mapped
module before and after the probes, requires exactly one `127.0.0.1` listener
owned by that child, emits three fixed `OPTIONS *` probes, requires fresh host
transaction IDs, and verifies that no child remains in the private namespace
during cleanup. Until the independent provenance gate exists, execution stops
before this path. A receipt is written once through a root-owned directory
descriptor with an atomic hard-link publication; the unavailable prerequisite
yields only `BLOCKED`, declares runtime no-CRS provenance `NOT_VERIFIED`, and
declares MRTS `NOT_INVOKED`.

The existing protected dispatcher remains fixture-only. Its new job summary
can show the resolved SHA and the fixture outcome, but it never reads PR
source, receives a write token, or asserts runtime evidence. A subsequent
protected-master integration must invoke the supervisor from inside the same
restricted namespace and must create the sealed artifacts itself; this record
does not claim that future runtime execution.

## Changed files

| File | Purpose |
| --- | --- |
| `ci/runtime/lifecycle/trusted_lighttpd_runtime_supervisor.py` | New protected runtime supervisor primitive. |
| `tests/test_trusted_lighttpd_runtime_supervisor.py` | Focused sealed-plan, process, probe, receipt, and cleanup contracts. |
| `.github/workflows/run-trusted-lighttpd-namespace-dispatch.yml` | Bounded fixture-only GitHub summary. |
| `tests/test_trusted_lighttpd_namespace_dispatch_workflow.py` | Summary and status fail-closed mutation contracts. |
| This paired record and archive indexes | Authorized bilingual traceability. |

## Commands executed

- `rtk proxy python3 -m py_compile ci/runtime/lifecycle/trusted_lighttpd_runtime_supervisor.py` — passed.
- `rtk proxy python3 -m unittest -v tests.test_trusted_lighttpd_runtime_supervisor tests.test_trusted_lighttpd_namespace_dispatch_workflow` — passed (`16` focused tests).
- `rtk proxy make check-ci-security-contract` — passed.
- `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m pip check` — passed.
- The pinned task-local `actionlint` invocation for `.github/workflows/run-trusted-lighttpd-namespace-dispatch.yml` — passed.
- The pinned task-local `zizmor` invocation for `.github/workflows/run-trusted-lighttpd-namespace-dispatch.yml` — passed; offline mode reported no findings and three existing suppressions.
- `rtk proxy git diff --check` — passed.

## Security impact

The new code narrows the eventual runtime trust boundary: PR-controlled output
cannot select a binary, module, config, port, probe, process, or receipt
result. It adds no PR-triggered privileged execution and does not alter the
dispatcher's least-privilege token split. The later protected invocation still
requires independent review because it is the component that will create the
sealed artifacts and run this supervisor as root before dropping the Lighttpd
child identity.

## Runtime evidence

No Lighttpd runtime evidence was collected or claimed by this change. The
current dispatcher still runs only the protected namespace fixture. The
supervisor's focused tests exercise local control behavior and are not host
runtime evidence for a pull request.

## Known limitations

This PR intentionally does not attach the supervisor to the protected
dispatcher, construct the sealed artifact set, create the later canonical
protected rule/data provenance contract, enable the blocked start path,
dispatch against a PR SHA, invoke MRTS, or close
FND-PARENT-0303. The existing namespace must remain the execution home; a
host-side process observer cannot honestly observe a child confined to a
separate PID namespace.

## Remaining risks

The protected-master integration is still required. Its inputs must remain
master-owned literals or independently sealed outputs, and it must retain the
exact process, listener, request, receipt, and cleanup observations defined
here. Hosted exact-head checks, SonarCloud, and a manual protected runtime run
remain pending after the Draft PR is opened.

## Checks not run and rationale

- No protected `workflow_dispatch` execution: the workflow is intentionally
  gated to protected `master`, which this unmerged Draft PR cannot exercise.
- No real Lighttpd/MRTS run: this infrastructure PR does not yet create sealed
  Lighttpd artifacts or invoke the supervisor.
- No hosted PR checks or SonarCloud analysis: they require the later exact
  Draft PR head SHA.
- `make check-bilingual-docs` is blocked by the uninitialised Framework
  gitlink in this separate worktree, which causes existing missing local-link
  targets below `modules/ModSecurity-test-Framework/`; this task does not
  initialise or alter that repository.
- Ruff is not installed in the repository's existing virtual environment. It
  was not added solely for this task because that would be an unauthorised
  dependency/tool change.

## Final diff and review status

The local supervisor and dispatcher contracts passed the focused tests, the
CI-security contract, workflow linters, and final whitespace diff check. An
independent final security-diff review confirmed that the supervisor blocks
before any runtime start until independent runtime no-CRS provenance exists;
no remaining evidenced High/Critical finding was reported. Exact-head hosted
checks, SonarCloud, and a protected runtime execution remain pending delivery.
