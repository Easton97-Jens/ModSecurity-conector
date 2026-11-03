# Change Record: CR-20261102-submodule-candidate-context

**Language:** English | [Deutsch](CR-20261102-submodule-candidate-context.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261102-submodule-candidate-context |
| Date (UTC) | 2026-11-02 |
| Base revision | `a18ffca3b5bb54887c0b8859ece95478e83cf262` |

## Motivation and problem statement

Run 41495088844 / job 125448091161 checked out Framework candidate `1b0885a2aa9b91b3faad76de6df8250bf8147eef` while retaining the old `FRAMEWORK_REVISION`. Workflow expansion raised `ContextError`. The publisher had the reverse inconsistency after rewriting Parent pins. Correct source selection then exposed candidate NGINX 1.31.8 against stale 1.31.6 action/producer projections. The user explicitly selected repair of that version conflict too.

## Acceptance criteria

Validate old/new Parent pins independently of Framework checkout/context; reject wrong pins and missing blobs; execute only the committed Parent's trusted parser. Align ordinary NGINX handoffs with the canonical 1.31.8 tuple and preserve the historical protected 1.31.4 broker contract. The subsequent user instruction requires zero current-PR Sonar issues and required checks before integrating Framework #165, repinning Parent to its actual merged master commit, and integrating Parent #442.

## Implementation decision and rationale

Followup on 2026-11-03: use the existing `FRAMEWORK_PATH` constant from the
revision-pin owner for Framework source lookups and exact gitlink matching.
This removes Sonar `python:S1192` without changing paths, source selection or
validation. The eight selected Git-context/verifier regression tests passed.
Current-head Sonar issue count must be read back after analysis; a passing gate
alone does not satisfy the user's zero-issues requirement. The user now
authorizes integration of the selected Framework and Parent PRs after zero
issues and required checks, with actual squash-master repinning between merges.

The required Traefik CRS job exposed a second runtime failure while loading
the local plugin in canonical Traefik 3.7.17 / Yaegi 0.16.1. An isolated
source comparison identified the local `plainConfig` pointer passed to
`json.Unmarshal`. Explicit `any(&decoded)` avoids the interpreter's special
decoder-wrapper selection while preserving Go decoding semantics. Removed-key
rejection, limits and error propagation remain intact. Framework #165 also
adds payload-safe failure-origin reporting and three negative regression tests.

The Apache CRS job failed before runtime because APR-util 1.6.5 was retired
from the live Apache download directory. Framework #165 updates only the
canonical APR-util version/checksum to 1.6.6. The official SHA-256 metadata and
downloaded archive bytes agree; the exact source-host/provenance guards remain
in place. Historical provenance fixtures remain historical.

Read bounded regular UTF-8 Git blobs at the validated Parent lock revision. Obtain parser code separately from committed Parent HEAD's Framework gitlink and reuse its closed-schema expander with a Git-backed data reader. Run updater verifier calls with isolated Python (`-I`); provision the existing reviewed PyYAML dependency in the separate publisher job before App credentials. Keep migrated producers Framework-owned. Synchronize component/full-SHA references with the existing Parent tool and regenerate compiler guides from source. Framework dependency: [PR #165](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/165).

## Changed files

Updater/verifier, Traefik native middleware decoder, direct full-smoke NGINX tuple, Framework gitlink, registry-managed component/workflow pins, generated EN/DE Envoy/HAProxy/NGINX compiler guides, `ci/README.md` / `ci/README.de.md`, and this Change Record pair. Framework source/tests have a separate commit and PR. MRTS is unchanged.

## Commands executed

All commands used RTK. The task-owned `with-context.py` launcher records explicit Connector/Framework roots and HEADs, profile `h1`, external outputs/TMPDIR and Python user-site isolation. Retained evidence root: `/var/tmp/codex/ModSecurity-conector/runs/fix-submodule-candidate-context`.

- Original verifier: pinned control exit 0; candidate checkout with stale context reproduced the reported `ContextError`, exit 1.
- Corrected `python -I ci/tools/verify-framework-candidate-contract.py` with compatible reviewed common data: exit 0 despite stale context.
- The four `VerifyFrameworkCandidateGitContextTests` plus four selected `VerifyFrameworkCandidateContractTests`: 8 passed. Controls cover old/new selection, unexecuted candidate Python, shadow-source precedence, wrong wrapper SHA, missing blob, stale lock, NGINX drift and provenance requirements.
- `python -I ci/tools/sync-framework-component-versions.py --sync` and `--check`, using extracted candidate common data and the exact selected SHA: passed; final check reports no changes.
- `python -I ci/tools/verify-framework-candidate-contract.py` against synchronized pins: exit 0, `release-1.31.8` verified.
- `python scripts/generate_compiler_guides.py`: exit 0.
- Active inventory admission: 100 active cases / limit 100; the complete catalog was not executed.
- Python AST parsing and `git diff --check`: passed.
- Traefik decoder/configuration tests through the Framework-owned Go overlay: five test functions passed, including all case/null/value rejection controls. `go vet -mod=readonly ./...` and `gofmt -l` passed with Go 1.27.3 and external caches; no dependency/toolchain changes.
- Three selected Framework failure-diagnostic regression tests passed independently after integration at `90053afc6954efcf4b9ac3f62f0f89ecb1fccfd1`.

An initial synchronizer attempt correctly rejected a common file outside its allowed temporary root; extraction into the task-owned runner root resolved setup.

Final integrated validation at Framework 965797c84142813e2992971fdf2add9a56170d5a: 8 focused tests passed. RTK-wrapped make check-bilingual-docs, make check-doc-links, and python ci/tools/new-change-record.py check passed. Automated review confirmed every other workflow edit is solely the registered full-SHA substitution.

Framework #165 was subsequently squash-merged as
`bb6c7580208a05c17d6d6674571731b6a71028cb` after exact-head checks and Sonar
readback confirmed zero issues/hotspots and Quality Gate OK. Parent now selects
that actual merged commit in the gitlink, lock and registered workflow refs.
The eight focused verifier tests and isolated 1.31.8 contract check passed
again; native synchronization `--check` reported no changes. Compiler-guide
generation produced no additional diff. Parent final-head CI/merge evidence is
tracked in its PR and task plan.

## Security impact

No weaker checks, privileges or provenance requirements. Candidate Python is not imported by the isolated verifier. Action/producer data uses the selected pin; parser code uses the committed trusted pin. Missing, oversized, symlink-mode, non-UTF-8 and inconsistent sources fail closed. Framework source-map ownership takes precedence over local shadows. Historical broker source tuples remain unchanged.

## Runtime evidence

The bounded native Traefik CRS probe reproduced the original interpreter panic
before engine events. With the decoder conversion applied to the tracked Parent
source, the canonical 3.7.17 host loaded the plugin and CRS 4.29.0 produced
allow/block/transformed-block outcomes 200/403/403, correlated to the expected
trigger and intervention events. Processes stopped and socket/workspace cleanup
passed. Evidence is retained under the external run directory
`runs/traefik-ci-diagnostics-20261103/native-tracked-parent`. This focused probe
does not establish full lifecycle qualification or production readiness. No
hosted NGINX traffic is claimed by Git-object tests or source synchronization.

## Known limitations

Framework and Parent require separate PR review/integration. The protected-base updater publisher cannot exercise the repaired branch before integration. Exact-head merge and master-workflow evidence are tracked in the PRs/task plan; no workflow dispatch with publisher credentials was performed.

## Remaining risks

The trusted Framework expander's data-acquisition seam remains an explicit compatibility dependency, covered by real Git-object regression fixtures. Host runtime qualification is separate from this scoped maintenance repair.

## Checks not run and rationale

No full connector/I12 matrix or hosted NGINX runtime campaign: outside this scoped repair. Local checks use available Python 3.14; GitHub CI selects the repository's Python 3.15 patch contract. Current-head GitHub checks and review are tracked separately in the PR/task plan; no CI or Sonar success is inferred from local results.

## Final diff and review status

Independent read-only review identified and corrected local-shadow precedence, NUL rejection and publisher dependency provisioning. Final integration/documentation results and actual merge/master state are retained in the task plan and PR. The original user checkout remains unchanged; task-owned external checkouts/evidence are retained.
