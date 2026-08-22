# Change Record

**Language:** English | [Deutsch](CR-20260822-nginx-updater-workflow-publication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260822-nginx-updater-workflow-publication |
| Date (UTC) | 2026-08-22 |
| Base revision | `c8881eaadf7d3ef5d4173d581a62726a2df3fdf2` |
| Delivery status | Prepared on a dedicated branch and pull request; no merge is asserted. |

## Motivation and problem statement

Framework-update run `32557767129` validated candidate
`52fe6ee334f1381c35d5c3b7140433c626469523`, including NGINX `1.31.4`,
but its publisher push was rejected because the built-in workflow token
had no permission to update `.github/workflows/nginx-root-broker.yml`.

## Acceptance criteria

NGINX must remain in its own protected root-broker workflow; the reviewed release tuple must become `release-1.31.4`, `nginx-1.31.4.tar.gz`, and its registered SHA-256; validation jobs must not receive a publisher credential; and the change must remain a Draft PR with no auto-merge.

## Implementation decision and rationale

Keep the dedicated, immutable NGINX root-broker workflow. The submodule
publisher continues to use the built-in token only for pull-request
metadata and uses the existing repository-limited workflow publisher
GitHub App only for Git pushes that can contain reviewed workflow pin
changes. The built-in token loses `contents: write`; no auto-merge,
mutable reusable-workflow reference, or broader root boundary is added.

## Changed files

- Synchronize the Framework gitlink and registered Parent pins to the
  validated candidate, including NGINX `release-1.31.4`.
- Mint the existing workflow publisher App token with only
  `contents:write` and `workflows:write` for Git publication.
- Preserve `github.token` for Draft-PR identity and metadata operations.
- Add static regression assertions for the split-token boundary.
- Align the NGINX archive cache-identity fixture with the registered `1.31.4` release tuple.

## Commands executed

The branch bootstrap runs the exact component synchronizer in `--sync`
and `--check` modes, regenerates compiler guides, executes the focused
updater and CI-security unit suites, runs the aggregate CI-security
contract, checks bilingual documentation, and applies `git diff --check`.
Hosted pull-request checks remain authoritative after PR creation.

## Security impact

The NGINX root broker remains separate from the other connectors and
remains pinned by immutable SHA. The change grants workflow-file write
permission only to the already configured repository-limited publisher
App during the isolated publisher job; validation jobs receive no
publishing credential.

## Runtime evidence

Bootstrap run `32573726344` observed all `48` focused tests and all `122` aggregate CI-security/submodule tests pass. It stopped only at the bilingual Change-Record schema corrected here. The synchronized NGINX tuple is `release-1.31.4`, `nginx-1.31.4.tar.gz`, and SHA-256 `e6f20b644a17a643f059ae6467a1971fe2811587d025e071068753a1f1e3b3c3`.

Follow-up exact-head run `32574140575` passed all `29` Framework protocol-client tests and exposed only the stale Parent cache-identity fixture still bound to `1.31.3`. This repair aligns that fixture to `1.31.4`; the focused cache/protocol contract and aggregate CI-security contract are rerun successfully before the one-commit branch is republished.

## Known limitations

After this update is merged, the protected NGINX caller still requires
a separate reviewed repin to the resulting merged broker commit and the
Framework candidate SHA. This two-stage activation preserves the
immutable broker trust boundary.

## Remaining risks

The final exact-head hosted matrix, GitHub workflow-file authorization, and the protected-master NGINX lifecycle still require hosted evidence. Any failure blocks delivery and does not permit mutable workflow refs or PR-controlled root execution.

## Checks not run and rationale

The final rewritten commit's complete connector matrix, review and branch-protection gates, merge, and post-merge protected-master invocation cannot be claimed before final publication and reviewed integration.

## Final diff and review status

PR #317 remains open and Draft. The final commit is constructed without the temporary bootstrap workflows and directly on base revision `c8881eaadf7d3ef5d4173d581a62726a2df3fdf2`. No merge, ready-for-review transition, or protected-caller activation is asserted.
