# Change Record: CR-20261009-nginx-body-buffer-event-scope

**Language:** English | [Deutsch](CR-20261009-nginx-body-buffer-event-scope.de.md)


## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261009-nginx-body-buffer-event-scope |
| Date (UTC) | 2026-10-09 |
| Base revision | `dcbefad1144b38f1545399a9f72967fbb1b3d424` |

## Motivation and problem statement

URI-only selection conflated rule intervention evidence with legitimate same-request phase4_append, phase4_completion and transaction_cleanup telemetry. Append telemetry already exposed this defect before the cleanup metadata fix.

## Acceptance criteria

Six legitimate controls each require exactly one phase4_intervention in response_body with rule_id 1250001 and exact typed body/EOS accounting. Telemetry alone, mismatches and duplicates must fail.

## Implementation decision and rationale

Select intervention candidates by URI and event identity, then strictly validate phase, rule and all existing accounting fields. Other telemetry remains untouched in the original log and cannot satisfy the claim.

## Changed files

tests/run_nginx_body_buffer_fixture.py; tests/test_nginx_body_buffer_fixture.py; this English/German Change Record pair.

## Commands executed

All commands used rtk proxy. RED mixed-telemetry regression: exit 1, genuine accounting failure on unchanged validator. GREEN focused fixture/observation tests: exit 0. Logs: external analysis/nginx-all-required-20261008T124555Z/body-buffer-event-scope/{red,green}.log. Existing Parent .venv interpreter used with PYTHONNOUSERSITE=1 and external bytecode cache. Ruff probe: exit 1, No module named ruff. Syntax is checked by the existing AST contract. Change Record structure check: exit 0.

## Security impact

Evidence acceptance stays fail-closed for required intervention identity, rule, phase, body, EOS and uniqueness. No product, Framework, MRTS or selection changes.

## Runtime evidence

No hosted fixture or lifecycle executed by this worker. Unit rows are test inputs, never runtime evidence.

## Known limitations

Focused contracts prove event selection/accounting only; fresh hosted requests remain required.

## Remaining risks

Independent review and integrated hosted execution remain pending.

## Checks not run and rationale

No build, E2E, commit, push, CI or Sonar by this worker. Ruff unavailable in the existing environment; no dependency installation.

## Final diff and review status

Four owned files only; awaiting coordinator review. No commit or push.
