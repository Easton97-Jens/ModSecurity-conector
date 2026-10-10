# Change Record: CR-20261010-r17-pr382-nginx-system-evidence

**Language:** English | [Deutsch](CR-20261010-r17-pr382-nginx-system-evidence.de.md)

Documentation-only evidence reference; runtime acceptance belongs to the exact downstream tested tuple.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261010-r17-pr382-nginx-system-evidence |
| Date (UTC) | 2026-10-10 |
| Base revision | `b2622a5d6ca746485c08f4789208299a111f47c7` |

## Motivation and problem statement

Record the newly published R17 NGINX-H1 downstream evidence and expose the exact I09–I12 rest scope without converting NGINX-only coverage into upstream/cross-connector acceptance. Historical R16 retained its measurement gap; R17 measures the generic Strict numeric client completion.

## Acceptance criteria

Complete EN/DE parity; immutable R16 history; exact R17 identity, client/writer completions and public link; nine-column 56-row matrix for 14 route legs; broad I09–I12/V08–V10 remain open and I09f/I10e remain completed; no product/Gitlink/runtime change; native documentation/archive/regression/diff checks truthfully recorded.

## Implementation decision and rationale

Documentation-only update on the actual #382 documentation worktree at the base below. Use immutable b262 source/test links as inventory, not fresh passing tests. Separate proven Apache void-sink propagation and SPOP unchecked fputs gaps from incomplete audits and physical-host evidence. Request/response companion legs stay separate. Generated Change Record scaffolds use the native schema, then actual facts replace scaffold prose.

## Changed files

- `docs/pr-382-checklist.md`
- `docs/pr-382-checklist.de.md`
- `docs/pr-382-i09-i12-rest-matrix.md`
- `docs/pr-382-i09-i12-rest-matrix.de.md`
- `reports/audits/change-records/CR-20261010-r17-pr382-nginx-system-evidence.md`
- `reports/audits/change-records/CR-20261010-r17-pr382-nginx-system-evidence.de.md`

## Commands executed

Working directory: `/var/tmp/codex/ModSecurity-conector/worktrees/pr382-nginx-system-docs-r17`.

```sh
rtk proxy env PYTHONDONTWRITEBYTECODE=1 /var/tmp/codex/ModSecurity-test-Framework/venv/bin/python ci/tools/new-change-record.py create --name r17-pr382-nginx-system-evidence --base-revision b2622a5d6ca746485c08f4789208299a111f47c7 --date 2026-10-10
```

Actual scaffold creation exit 0. Native `make check-bilingual-docs check-doc-links` passed (exit 0), with the exact local Framework documentation worktree and all temporary data under the R17 analysis root. Bilingual structure, repository paths and documentation links passed. `python -m unittest -v tests.test_change_record tests.test_bilingual_docs tests.test_prepare_reviewed_framework_handoff`: 61 tests, no SKIPs, exit 0. Native archive validation and `git diff --check` also passed. All commands were RTK-wrapped; RTK 0.51.0 verified. Final remote CI is separate and is not preclaimed.

## Security impact

No guardrail, authorization, isolation, validator, Required selection, sink policy or source code changes. No raw payload/environment/secrets published. Diagnostic numbers are not client exits; actual direct-child completion is explicitly scoped. No Protected or merge authorization inferred.

## Runtime evidence

Downstream tested tuple: Parent `2f02370b07149265841411894f1a2cf7f1e978ff`, Framework `9f41f80db7bf53b57429457bce0dda675d2ec5d7`, MRTS `8a6bb546c4c81d8ffc7be801dceac60c6925685f`; run `nginx_full97_2f02_20261010_r17`. Actual standard Full97 exit 0 / 554.091 seconds, original Canonical PASS, 97 Required PASS (14 YAML / 42 native / 10 config / 31 derivations), zero required missing/FAIL/BLOCKED/NOT_EXECUTED, empty schema errors. Generic Strict actual normal curl exit 52 invocation `669ba1b19fc340618d62148d715e5fc3`, PID 10440; First-Byte writer actual exit 0 invocation `1515086ec928494aafd0b0a0fceab107`, PID 12514. 34 curl pairs, 16 program completions all normal 0; 79 non-readiness HTTP operations including four positive controls, 61 lifecycles/cleanup, 57 fresh projections. Final ledger 2589 entries, independent check 0, SHA256 `b79fbe3e2b7cf2806c8698f2a6fd7f1f1a4c4f06aed8075924311d4d1c27d97a`. [Public report](https://github.com/Easton97-Jens/ModSecurity-conector/pull/396#issuecomment-6101794434) preceded this change. No runtime executed for this documentation revision.

## Known limitations

R17 is local NGINX-H1 scope on Ubuntu 26.04.1 LTS / kernel 7.0.0-38-generic / x86_64 KVM / NGINX 1.31.6, actual Root UID0/nobody UID65534 in private namespaces. Not #382 product, later documentation SHA, H2/H3, CRS, Off, production, other connectors or Protected acceptance. Curl HTTP000 is not producer/original200; native Strict HTTP200 is a separate observer. Original 42 source NOT_EXECUTED placeholders remain, with genuine specialized lineage. Local raw evidence is not a public downloadable artifact.

## Remaining risks

Open I09–I12/V08–V10 across route legs; incomplete caller/API audit and independent physical sinks/host controls. Completed Apache I09f/I10e are not reopened. Transport short-write/EAGAIN is not physical event sink short-write; soft budget after return is not hard cancellation. Final delivered documentation-head CI/reviews/Sonar and branch readback remain Root-owned; no automatic acceptance transfer.

## Checks not run and rationale

No new runtime, Full97 retry, Protected dispatch, cross-connector tests/source fixes, full product lint, API mutation, Git delivery or merge executed by this documentation task. Only documentation-native validation is in scope. The current downstream runtime already ran separately; its public report is referenced rather than rerun.

## Final diff and review status

Six assigned documentation paths only; Root owns final independent review and normal commit/publication. No source, Framework/MRTS pins, history or runtime artifacts altered. #382 remains Draft. This record claims no future #396 Ready transition, current-documentation CI result, merge or retarget. Native documentation, archive and 61 regression checks passed locally; final delivered-head CI and independent delivery remain Root-owned and are reported in public PR metadata.
