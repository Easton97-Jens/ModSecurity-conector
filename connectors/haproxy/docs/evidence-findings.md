# HAProxy Evidence Findings

**Language:** English | [Deutsch](evidence-findings.de.md)

Status: current runtime evidence

## Finding Summary

| Finding | Status | Evidence |
| --- | --- | --- |
| SPOE/SPOP integration path | selected and implemented for current scope | HAProxy examples, harness, production SPOA runtime |
| Production SPOA binary | implemented | `haproxy-modsecurity-spoa` |
| libmodsecurity binding | implemented | build and self-test targets |
| Request phases 1/2 | live evidenced | default smoke and matrix summaries |
| Phase 3 response headers | implemented, live evidenced | response SPOE group and decision logs |
| Decision log | implemented | `decision.jsonl` |
| Audit-log plumbing | implemented | `audit.log` paths and live artifacts |
| Phase 4 / RESPONSE_BODY | bounded strict-abort evidence only | phase4 HAProxy example and runtime evidence |
| Synthetic matrix writer | not used | generated reports consume runtime summaries and snapshots |

## Current Counts

- Default HAProxy smoke: `55/55 PASS`.
- HAProxy force-all: `133 attempted / 104 PASS / 23 FAIL / 0 BLOCKED /
  6 NOT_EXECUTABLE`.

## External Basis

HAProxy documents SPOE/SPOP as the mechanism used to communicate with external
stream-processing agents. The repository implements that path with a local SPOA
runtime that loads libmodsecurity and returns HAProxy transaction variables.

## Remaining Findings

- Full-body RESPONSE_BODY support is not proven.
- Multi-worker, long-running cache pressure, and packaging remain production
  hardening tasks.
- Dynamic disruptive status mapping beyond the current HAProxy rules remains
  limited.

Phase 4 / RESPONSE_BODY remains non-promoted; bounded strict-abort evidence is
documented/reported as runtime evidence only.
