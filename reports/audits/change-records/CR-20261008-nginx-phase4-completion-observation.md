# Change Record: CR-20261008-nginx-phase4-completion-observation

**Language:** English | [Deutsch](CR-20261008-nginx-phase4-completion-observation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-phase4-completion-observation |
| Date (UTC) | 2026-10-08 |
| Base revision | `0981e437968a3d0df5cd6200f4d55b0128e4874e` |

## Motivation and problem statement

Intervention-only records do not establish a successful native Phase-4 completion or actual Engine retained length.

## Acceptance criteria

Require native result1 and completed Common P4 mask/last phase with no active phase. Reject inconsistent/oversized counters; zero append calls only accompany an entirely empty response.

## Implementation decision and rationale

The new NGX-only constructor borrows caller-owned event/reason/header storage. It sets phase4_completion, response_body, actual EOS and supplied-byte counters. Actual retained length and append calls use a bounded payload-free reason. Existing actions/status/identities are preserved; no marker-split or MIME-scope flag is inferred.

## Changed files

New observation header, compiled C fixture and Python harness, plus this EN/DE pair. Shared module/bodyfilter/context/source map remain coordinator-owned.

## Commands executed

Initial compiled RED: absent observation header. Strict C17 -Wall -Wextra -Werror -pedantic-errors sanity0/1 compile and actual Common JSONL serialization pass. Invalid return, phase/mask, counts, pointers and short-buffer controls are exercised.

## Security impact

No payload, rule fabrication, mode change, Common counter reinterpretation or weakened validator. Invalid completion leaves the event unchanged; reason output remains caller-owned.

## Runtime evidence

The compiled fixture proves the constructor and genuine Common serialization, not a running Engine or NGINX. Actual CAPI retained length and append count must be supplied by the adapter after its successful native boundary.

## Known limitations

No adapter call is integrated here. Event storage must be initialized and all borrowed values must outlive serialization.

## Remaining risks

Incorrect caller sampling cannot be repaired by this constructor. Runtime and strict canonical mapping remain independently required.

## Checks not run and rationale

Fresh runtime and rebuilt module integration wait for the coordinator. No Exact-Head or canonical PASS claimed.

## Final diff and review status

Exclusive new files only; no Common/module/bodyfilter/Gitlink/MRTS/publication modifications.
