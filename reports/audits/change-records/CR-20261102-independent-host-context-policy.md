# Change Record: CR-20261102-independent-host-context-policy

**Language:** English | [Deutsch](CR-20261102-independent-host-context-policy.de.md)

Independent policy delivery; Framework pin remains separate.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261102-independent-host-context-policy |
| Date (UTC) | 2026-11-02 |
| Base revision | `2abad408cae7e5a103d12a9a9e432129bfe0468f` |

## Motivation and problem statement

Publish the independent host execution-context guidance now, while the broader Framework-pin qualification remains open in [#436](https://github.com/Easton97-Jens/ModSecurity-conector/pull/436). UID 0 alone does not establish identity-transition or private-socket prerequisites.

## Acceptance criteria

Route native host-test context decisions from the Parent index; preserve identity, ownership, socket, protected-broker and cleanup requirements; bind the separately integrated Framework guide without updating the Parent pin; update only the two owned catalog digests; pass applicable exact-head checks before regular master integration.

## Implementation decision and rationale

Use an immutable guide reference at Framework `b85280278310f4034af78149ac13671438965c7b`. Parent remains pinned to `e6284e8a8a64d999bf60f777252987172ab24756`, which lacks the new guide and `--execution-context-only`. The example requires an explicitly selected, compatible and approved Framework implementation. Missing implementation blocks the host test. No automatic escalation or compatibility admission follows from this policy. The guide is reachable through `AGENTS.md` → `.codex/context/index.md` → `.codex/context/security-runtime-preflight.md`.

## Changed files

`.codex/context/index.md`, `.codex/context/security-runtime-preflight.md`, `.codex/inheritance-manifest.toml`, and this EN/DE record pair. No product, gitlink, lock, workflow projection, Framework source or MRTS change.

## Commands executed

All shell commands use RTK. `rtk bypass env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 /var/tmp/codex/ModSecurity-test-Framework/venv/bin/python -P .codex/bin/validate-v32-structure.py`: PASS. The same interpreter with `.codex/bin/validate-codex-inheritance.py --check --repository parent --json`: exit 1, five independent stale digests preserved (six on the base, including the owned index entry). `git diff --check`: PASS. `make check-bilingual-docs check-doc-links PYTHON=/var/tmp/codex/ModSecurity-test-Framework/venv/bin/python` with explicit `TEST_ROOT`, `FRAMEWORK_ROOT`, `CONNECTOR_ROOT`, exact `CONNECTOR_REVISION` and external output root: PASS (bilingual docs, repository paths and links). `ci/tools/new-change-record.py check`: PASS (structure only). The two owned digests and unchanged pin/projection/product surfaces: PASS. Baseline-versus-candidate inheritance comparison: PASS for no new diagnostics (9 → 8 including Framework child diagnostics; global validator still fails). Gitleaks 8.30.1 on the five-file source export: PASS. Exact staged/commit bytes and delivery results are checked again before integration.

## Security impact

Preserve same-launcher/namespace preflight, actual worker transitions and access denials, private UDS validation, and protected-broker admission. RTK and tool-specific wrappers remain mandatory. No guard, UID check, CI requirement or Quality Gate is weakened. Private verification JSON, raw logs, runtime directories and environment data are excluded.

## Runtime evidence

No new host run is claimed. The private 2026-11-01 receipt is dated evidence for its original source/artifact pair only. Envoy remains unconfirmed without its own host run. Reused NGINX artifacts still require matching product-source, build and artifact admission evidence.

## Known limitations

The unchanged Parent Framework pin cannot run the new CLI example. The full pin update, compatible product APIs from separately managed [#348](https://github.com/Easton97-Jens/ModSecurity-conector/pull/348), and final commit-pair qualification remain outside this policy-only integration. The required `traefik-go` failure at #436 head `1c91434752b7da3e31a4fe03c4d8c7d4a3707add` reports missing `Summary.ResponseIncomplete`.

## Remaining risks

Five independent Parent catalog entries remain stale: `PARENT-CHANGE-WORKFLOW`, `PARENT-CONNECTOR-MATRIX`, `PARENT-DEFINITION-OF-DONE`, `PARENT-PHASE4-TARGET-SEMANTICS`, `PARENT-TESTING-AND-EVIDENCE`. The existing Framework child command-policy inheritance mismatch remains unchanged. These are documented drift, not a global inheritance PASS.

## Checks not run and rationale

Final Framework-pin/provenance qualification, Apache contract, renewed NGINX artifact admission, fresh NGINX host proof, separate launcher and cleanup evidence belong to #436 after its dependencies. They are not prerequisites demonstrated by this documentation-only change and are not claimed as PASS.

## Final diff and review status

Focused split reviewed against base `2abad408cae7e5a103d12a9a9e432129bfe0468f`. Only the policy, routing, two owned digests and paired record are selected. The user authorized separate regular master integration; current-head CI, Sonar zero-new-issue/hotspot readback, reviews and exact-head protection checks remain mandatory before merge. Delivery/merge facts are read back from GitHub rather than predicted here.
