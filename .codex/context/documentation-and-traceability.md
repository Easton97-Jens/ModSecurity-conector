# Documentation and Traceability

## Bilingual documentation

Versioned reader-facing technical documentation uses English as the technical primary and a complete German companion, normally `name.md` / `name.de.md`.

Maintain both in the same task with equivalent features, prerequisites, warnings, examples, commands, limitations, evidence boundaries, risks, links/tables, and actual status.

Keep technical literals unchanged between languages: code, identifiers, paths, commands/options, config keys, protocol names, hashes/IDs/URLs, exact error messages, and machine-readable content.

Local `AGENTS.md` and `.codex/` control-plane files do not require German companions unless explicitly requested.

## Generated material

Generated documentation/reports must be changed through their documented source/generator. Do not hand-edit generated output as a substitute.

## Change Records

Every non-trivial versioned product change uses the repository's current `docs/change-traceability.md` convention and the established `reports/audits/change-records/` location/templates.

The EN/DE Change Record must truthfully describe scope, old/new behavior, actual changed files/tests, executed commands/results, checks not run, security/compatibility impact, documentation pairs, generated artifacts, limitations/residual risk, and real delivery facts when they exist.

Never invent SHA, PR number, CI/review/Sonar result, merge status, runtime evidence, or delivery outcome.

## PR lifecycle evidence

For actual authorized PR lifecycle work retain only observed repository-scoped facts: ownership/authorization, current head SHA, dependencies/order, required checks/reviews/conversations/Sonar, merge/closure result, resulting master SHA where applicable, restoration, and branch-cleanup disposition.

Parent, Framework, and MRTS lifecycle evidence remain separate even when cross-repository ordering is described.
