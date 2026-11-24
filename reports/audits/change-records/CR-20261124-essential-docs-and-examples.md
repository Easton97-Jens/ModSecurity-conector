# Change Record: CR-20261124-essential-docs-and-examples

**Language:** English | [Deutsch](CR-20261124-essential-docs-and-examples.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261124-essential-docs-and-examples |
| Date (UTC) | 2026-11-24 |
| Base revision | `48c4672dc07458411288570515bb8357f1e9e581` |

## Motivation and problem statement

Repeated onboarding, mode explanations and validation caveats made it hard to find the host-specific choices and commands. Old PR and analysis records appeared alongside the current guides.

## Acceptance criteria

Readers can choose any of the ten profiles, reach its configuration layouts and validation instructions, and find current prerequisites in both languages. Historical records remain reachable. Active example directives and generated references retain their existing meaning.

## Implementation decision and rationale

Use the documentation and example indexes as navigation, keep setup in the getting-started guide and leave host-specific prerequisites with the matching examples. Move the response-limit checklist and two PR #421 SonarQube records into the audit archive, with short pointers at their former paths. Select the checked-in Envoy template explicitly and remove an obsolete NGINX comment about native event logging.

## Changed files

- `docs/README{,.de}.md` and `docs/getting-started{,.de}.md`
- `examples/README{,.de}.md` and the six host README pairs under `examples/`
- `examples/nginx/safe/nginx.conf` comments
- `docs/response-limit-stack-checklist{,.de}.md` and `docs/sonarqube-pr421-{closeout,triage}{,.de}.md`, with their content under `reports/audits/documentation-history/`
- This Change Record pair

## Commands executed

- `make check-bilingual-docs`, `make check-doc-links` and `make check-variable-documentation` passed on the edited guides with the pinned Framework checkout and Python `3.15.2`.
- `git diff --check` passed. A focused comparison confirmed identical ten-profile layout links and active NGINX directives relative to the base revision.
- The Envoy README snippet ran with a temporary `BUILD_ROOT`. It generated local TLS files and rendered the selected template as parseable YAML.

## Security impact

The change affects documentation and example comments. Existing host, private socket, certificate, logging and policy boundaries remain specified in the relevant guides. The temporary TLS files were used only for configuration preparation.

## Runtime evidence

Configuration materialization was verified for the Envoy example. This establishes template rendering and YAML parsing only.

## Known limitations

The repository link check covers checked-in relative links. External destinations and historical runtime statements retain their original scope.

## Remaining risks

Links from outside the repository to archived sections may need the corresponding archive URL.

## Checks not run and rationale

No connector hosts or lifecycle campaigns were started for these editorial changes. The Framework example module is archived and the standard test admission rejected the invocation. The focused comparison and materialization checks above cover the changed example material.

## Final diff and review status

The scoped review covers English and German guides, archived records, their pointers and one comment-only configuration change. Publication and CI are tracked on the pull request.
