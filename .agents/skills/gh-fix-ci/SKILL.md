---
name: gh-fix-ci
description: Triage and remediate a task-owned GitHub Actions failure for the exact published commit under this repository's delivery rules.
---

# Triage a GitHub Actions failure

Use this local adapter to investigate a failing pull-request check after the
commit under review has been identified.

## Trigger conditions

- A GitHub Actions check for this repository's pull request is failing.
- The user asks to diagnose or fix a CI failure.
- A post-push delivery loop needs exact-SHA check evidence.

## Do not use when

- No check failure exists or the requested work is ordinary local test work.
- The failure belongs to an unrelated repository, branch, or external service.
- The exact commit and pull request cannot be established from repository or
  GitHub evidence.

## Local procedure

1. Record the pull request, branch, and immutable commit SHA before reading
   check results. Run `rtk gh auth status`, then use `rtk gh` and repository
   commands only.
2. Enumerate both push and pull-request checks for the exact head SHA. Capture
   machine-readable check, job, annotation, and minimal log metadata without
   copying credentials, payloads, or private URLs into versioned evidence.
3. Classify the failure as task-owned, infrastructure, flaky, pre-existing, or
   unrelated. Route SonarCloud, CodeQL, and other external quality-gate
   findings into the PR-feedback workflow; never treat unavailable detail as a
   passing result. Compare with `master` when a pre-existing failure is
   plausible.
4. Read the affected workflow and local policy before changing source. Preserve
   every quality gate and make the smallest task-owned correction. Ask only
   when the repair requires an architecture, scope, public API, security, or
   quality-gate decision.
5. Run the applicable local verification ladder and update the Change Record
   with actual results. The main agent creates an ordinary follow-up commit and
   pushes it when delivery policy permits.
6. Verify the remote SHA, then restart complete check and feedback monitoring
   for that new exact SHA. Continue until task-owned feedback/checks resolve or
   a documented external blocker remains.

## Safety boundary

Only the main agent may stage, commit, push, create or update a pull request,
reply to review feedback, or declare final CI status. Do not amend a published
commit. Do not force-push. Do not use `git add -A`. Do not add
`continue-on-error`. Do not use `|| true`. Do not weaken, skip, or suppress a
quality gate.

This adapter never grants authority to alter workflows, expose authentication
material, rewrite published history, or merge a pull request. Local delivery
and PR-feedback policies take precedence.

## Provenance

Adapted from the OpenAI GitHub plugin skill recorded in
[UPSTREAM.md](UPSTREAM.md). The upstream helper script is deliberately not
vendored because it retrieves GitHub check and log data at runtime.
