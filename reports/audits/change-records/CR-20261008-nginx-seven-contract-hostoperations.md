# Change Record: CR-20261008-nginx-seven-contract-hostoperations

**Language:** English | [Deutsch](CR-20261008-nginx-seven-contract-hostoperations.de.md)

Implementation-stage record; runtime and final delivery reconciliation remain outstanding.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-seven-contract-hostoperations |
| Date (UTC) | 2026-10-08 |
| Base revision | `a44d276b37f4ba1ce2c57af2f016d4cf96af43b6` |

## Motivation and problem statement

Selected NGINX configuration cases need real operation-specific host invocations
and retained evidence, not inferred success from HTTP or an arbitrary nonzero
exit. Duplicate headers require actual H1 fields and native observation.

## Acceptance criteria

Closed selected dispatch must invoke each declared configtest with exact input,
exit and diagnostic expectations. Receipts bind case/run/source identity and
raw binary/module/config/output bytes; the collector preserves these bindings.
Missing or mismatched evidence cannot pass. Required selection remains intact.

## Implementation decision and rationale

Extend the existing driver, dispatcher and collector for `missing_rules_file`,
`invalid_rule_syntax`, `unknown_config_key` and `unsafe_event_path`. Use owned
absent/directory leaves inside the authorized case tree, fixed inline syntax,
and NGINX directive lookup respectively. Configtest-only proves actual
`nginx -t`, never a daemon, worker, request or reload. Framework owns the
corresponding strict validation contract and ordered-header fixture; Parent
reuses actual H1 transport. A separate `run-nginx-valid-rules.py` driver performs
the closed `valid_rules_file` startup operation: real configtest, Root-Master/
nobody-Worker startup, GET `/no-crs/deny`, native rule `1100001` correlation and
verified cleanup. Dispatch passes the actual Framework root and rules file;
the collector retains the compound raw artifacts. Explicit `access_log off`
keeps copied configurations from using historical compile-prefix output paths.
Common emits `engine_decision` / `MSCONN_EVENT_ENGINE_DECISION`, not an observed
host action: `actual_action` is empty, `visible_http_status` is `0`, and
`transport_result` is `not_observable`. Separately bound actual HTTP `403`
supplies the client observation without rewriting that event.

## Changed files

`ci/runtime/lifecycle/run-nginx-configtest.py`,
`ci/runtime/lifecycle/run-nginx-valid-rules.py`,
`ci/runtime/lifecycle/run-selected-nginx-configtests.py`,
`ci/runtime/lifecycle/collect-no-crs-source.py`,
`tests/test_nginx_configtest_driver.py`,
`tests/test_nginx_selected_configtest_wiring.py`,
`tests/test_nginx_configtest_collection.py`,
`tests/test_nginx_valid_rules_driver.py`, and
`tests/test_nginx_valid_rules_wiring.py`; this EN/DE pair. Framework changes
and its eventual separate Gitlink integration are separate repository work.

## Commands executed

The repository-native Change Record generator created this pair with base
`a44d276b37f4ba1ce2c57af2f016d4cf96af43b6` and date `2026-10-08`.
Focused test logs under
`/var/tmp/codex/ModSecurity-conector/analysis/nginx-seven-contracts-20261008T080604Z`
show 23 driver tests, 17 dispatch tests, and 7 collector tests passing:
`parent-config-green.log`, `parent-config-wiring-green.log`, and
`parent-collector-green.log`. Red regression logs are retained separately.
These results are unit/integration contract tests, not current runtime coverage.
Documentation validation via `make check-bilingual-docs check-doc-links` and
`python ci/tools/new-change-record.py check` exited `0`; `git diff --check`
also exited `0`. All command payloads used the required RTK proxy.

## Security impact

No path, ownership, symlink, artifact, provenance, validator, or Required rule
is weakened. No foreign sensitive path is touched. No Common/product change,
MRTS mutation, protected dispatch, or administrative approval is included.

### Startup JSON writer follow-up

The generic JSON helper could overwrite an existing file or follow a symlink
in an isolated, task-owned reproducer (two red controls). Its five production
callers already use fixed names below an authorized, fresh, Root-owned `0700`
directory; the Sonar content-taint signal is not proof of CLI path exploitation.
The helper now also enforces the closed five names and external/non-checkout
authority itself, then uses the existing `PrivateRuntimeRoot` directory-FD API
for exclusive, no-follow `0600` creation. Serialized bytes remain identical.
The original two controls are green; four additional driver regressions check
all legitimate leaves, exact bytes/mode, existing files/links, unknown names,
nonprivate roots, symlink roots and checkout rejection. A fresh Sonar result
and integrated native run are still required; no finding disposition or
Quality-Gate exemption is asserted.

## Runtime evidence

Four historical-module diagnostic discovery probes returned actual configtest
exit `1`; they are explicitly not new-head evidence. `diagnostic-valid-r2`
additionally observed actual configtest exit `0`, Root-Master/nobody-Worker,
client exit `0` / HTTP `403`, native rule evidence and verified cleanup, but used
a dirty working revision and historical binary/module artifacts. It remains a
diagnostic, not committed-head coverage. Fresh binary/module-bound operations,
genuine H1/native events, Root-Master/nobody-Worker identity where
required, cleanup, and Canonical evaluation still await integrated execution.
No overall Exact-Head PASS or new coverage count is claimed here.

## Known limitations

`PRODUCT DECISION REQUIRED — invalid_status`: the existing catalog does not
unambiguously choose between Engine status-action syntax and a Common/adapter
default-status field. Those owners and acceptance/rejection semantics differ;
no status range or NGINX directive is invented. The record remains required and
unfulfilled. Other historical producer gaps remain outside this task.

## Remaining risks

Successful unit tests or matching hashes alone do not prove runtime semantics.
The successful-load case needs actual rule `1100001` execution; duplicate
headers need native phase-1 rule `1100504` count/value proof, not HTTP `200`
alone. Protected control-plane prerequisites remain independently required.

## Checks not run and rationale

Full native lint, fresh standard lifecycle, C17 regression, complete Framework
suite, and revision-bound CI/Sonar are not concluded for this working revision.
Earlier results on the base commit are not transferred to the eventual head.

## Final diff and review status

Final diff, whitespace, bilingual, full-suite, runtime and delivery review remain
integration work. PR #396 stays Draft; Framework publishing is authorized only
through `fix/nginx-seven-contracts-20261008` and a new Draft follow-up PR.
No merge, retarget, amend, force-push or protected dispatch is authorized.
No secrets or raw bodies are embedded in this pair.
