# Change Record: CR-20261026-nginx-broker-ubuntu26-preparation

**Language:** English | [Deutsch](CR-20261026-nginx-broker-ubuntu26-preparation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261026-nginx-broker-ubuntu26-preparation |
| Date (UTC) | 2026-10-26 |
| Base revision | `7a44f18edac729291d6551d068da64fa3fec4e1e` |

## Motivation and problem statement

The protected caller migration to Ubuntu 26.04 requires a reviewed trusted broker that accepts the complete new runner mode while retaining the deployed legacy caller.

## Acceptance criteria

Accept all three unprivileged jobs on ubuntu-latest or all three on ubuntu-26.04. Reject mixed, unknown, list and self-hosted runner values. Preserve immutable pins and every other caller check. Run the broker on ubuntu-26.04.

## Implementation decision and rationale

Validate one runner mode for the complete caller before checking each job. Exact supplemental hosted labels allow older actionlint to recognize Ubuntu 26.04. Caller source and immutable revision pins remain unchanged.

## Changed files

`.github/workflows/nginx-root-broker.yml`, `.github/actionlint.yaml`, `ci/runtime/broker/nginx_root_broker.py`, `tests/test_nginx_root_broker.py`, and this paired Change Record.

## Commands executed

RTK-wrapped source inspection and native Change Record scaffold generation; Python ast.parse on both changed Python files passed; `/root/go/bin/actionlint -color .github/workflows/nginx-root-broker.yml` passed. Root admitted the frozen external descriptor and source hashes before import or execution. The guarded run passed all seven selected methods: 36 expanded cases, 33 observed subtests, zero skips, failures or errors. Its audit hook rejects process and network calls. The external receipt is `runs/parent-ubuntu26-20261026/broker-preparation-result.json`. The initial custom harness failed to load all seven selectors because a namespace-package attribute was missing; the corrected harness passed. That initial error is retained as harness evidence, not a product regression.

## Security impact

The accepted runner vocabulary grows by exactly one hosted label, only in uniform mode. Permission, gate, inventory, source, artifact and immutable revision checks remain intact. No privilege or trust-anchor changes.

## Runtime evidence

None. No broker dispatch, service, host, matrix, Oracle or I12 campaign was started.

## Known limitations

This preparation does not migrate the caller or advance its broker pin. The separate caller migration requires a verified broker revision after reviewed master integration.

## Remaining risks

Hosted Ubuntu 26.04 runtime behavior remains unmeasured. The focused offline compatibility result does not establish protected broker execution or a hosted build.

## Checks not run and rationale

No canonical active-case inventory exists at this base; the externally admitted descriptor bound the executed selection. Hosted execution and runtime campaigns were not run and remain outside this preparation.

## Final diff and review status

The scoped patch and source hashes are prepared for review. Static Python syntax, actionlint and the admitted offline selection passed. Independent static source review found no concrete bypass. Commit, push and Draft PR publication remain delivery work for Root; this record does not claim them completed. No merge was performed or authorized.
