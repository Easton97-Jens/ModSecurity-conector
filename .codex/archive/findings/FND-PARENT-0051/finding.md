# FND-PARENT-0051 — CPython 3.14 test loader does not register the local runtime-smoke module before dataclass processing

## Identity

| Field | Value |
| --- | --- |
| ID | FND-PARENT-0051 |
| Category | test_failure |
| Repository / ownership | Parent / parent |
| Priority / severity / confidence | P1 / not_applicable / reproduced |
| Status / feasibility | fixed / feasible_now |
| Release blocker / security relevant | true / false |
| Profile | Parent PR #74 normal master update under CPython 3.14.4 |
| Connector / protocol | local runtime smoke harness / Python importlib test loading |
| MRTS impact | none; unchanged |

## Summary, observation, and impact

While updating Parent PR #74 through a normal non-fast-forward merge of the
current Parent master, the focused CPython 3.14.4 test suite failed before its
request-body assertions ran. `tests/test_local_runtime_smoke_request_body.py`
creates `SMOKE` from an importlib spec and immediately calls `exec_module`.
It does not first register that module under `SPEC.name` in `sys.modules`.

The imported smoke runner now has the `RuntimeOutputPaths` `@dataclass` from
current master. CPython 3.14.4's dataclass processing therefore looks up the
module registration and raises `AttributeError` because it is absent. The
failure is a test-loader compatibility defect, not a demonstrated production
request-body parsing, authorization, or path-confinement bypass. It blocks the
selected PR's focused evidence until repaired.

## Reproduction and evidence

Use the Parent virtual environment at CPython 3.14.4 from the isolated PR #74
worktree and run the recorded focused unittest command. It exits `1` while
loading `test_local_runtime_smoke_request_body.py`, with the retained trace
ending in `dataclasses._is_type` and `sys.modules.get(cls.__module__)`.

The retained receipt is
`.codex/runs/20260726T000000Z-pr55-pr74-python314-import/evidence/python314-import-loader-failure.md`
with SHA-256
`75c710e45b9db641bb82a4ef5b39ca088e0f35daf1ea5a0cb9f8a31852b0da2b`.
It also records the legitimate direct-import control: registering the module
under its spec name before `exec_module` exits `0` and imports
`RuntimeOutputPaths` successfully.

## Root cause and remediation

The test omits the standard importlib module-registration step. That omission
was latent before the runner's dataclass declaration and is exposed by CPython
3.14.4's class-processing implementation.

Add `import sys` and set `sys.modules[SPEC.name] = SMOKE` immediately before
`SPEC.loader.exec_module(SMOKE)`. Do not remove the dataclass, loosen the
request-body controls, or relax verified runtime-output-path confinement.

## Acceptance and validation

1. The test registers `SMOKE` under precisely `SPEC.name` before execution.
2. `tests.test_local_runtime_smoke_request_body` passes under CPython 3.14.4.
3. The selected request-body, runtime-path, evidence, HAProxy, workflow,
   documentation, compiler-guide, Makefile, and C timeout checks pass on the
   same candidate head.
4. A fresh exact-head PR cycle is inspected after publication; it is not a
   master-integration authorization.

Legitimate controls retain valid request-body acceptance, invalid
framing/size rejection, and runtime-output-path rejection for symlinks or
out-of-root destinations.

## Dependencies, residual risk, and history

This Parent-only repair depends on the normal PR #74 update branch. It neither
requires nor authorizes Framework, MRTS, Gitlink, branch-cleanup, or master
actions. It is related only to the separate Python-3.14 workflow-contract
finding FND-PARENT-0046; the technical causes are different.

The focused local fix is now present and retested: the original request-body
module passes 10 tests and the focused #74 suite passes 143 tests under
CPython 3.14.4. The record remains `fixed`, not `verified`, until the updated
exact PR head has fresh GitHub and SonarQube Cloud evidence. No security
control or risk is waived.

- 2026-07-26T05:30:02Z — Reproduced on the PR #74 merge candidate and recorded
  with a passing registered-import control. No product, Framework, MRTS, Git,
  GitHub, or Gitlink mutation occurred in producing the receipt.
- 2026-07-26T05:30:02Z — Added the one-line module registration before
  execution. The original CPython-3.14.4 request-body module (10 tests) and
  the focused PR #74 suite (143 tests) passed. Fresh exact-head CI/Sonar
  verification remains pending; no master integration is claimed.
