# Status Model

The framework separates runtime results from import/classification status.

## Runtime Status

| Status | Meaning | Exit effect |
| --- | --- | --- |
| `pass` | Real HTTP behavior matched the YAML expectation | success |
| `fail` | Server ran but behavior differed from the YAML expectation | exit 1 |
| `blocked` | Source, download, build, or runtime prerequisite was missing | exit 77 |
| `xfail` | Expected failure/probe classification, not part of normal smoke | not counted as pass |
| `skipped` | Reserved for explicit future skip behavior | not used silently |

`fail` is used when a rule variable does not reach libmodsecurity or the
connector returns the wrong HTTP status. `blocked` is only for prerequisites.

## Common Operation Status

The C-first common header `common/include/msconnector/status.h` and helper
implementation `common/src/status.c` define connector-neutral operation
outcomes. Harness summaries expose those concepts as append-only JSON metadata;
they do not replace the runtime statuses above.

| Runtime status | `operation_status` | `msconnector_status` equivalent |
| --- | --- | --- |
| `pass` | `ok` | `MSCONNECTOR_STATUS_OK` |
| `fail` | `error` | `MSCONNECTOR_STATUS_ERROR` |
| `blocked` | `blocked` | `MSCONNECTOR_STATUS_BLOCKED` |
| `skipped` | `unsupported` | `MSCONNECTOR_STATUS_UNSUPPORTED` |
| `xfail` | `unsupported` | `MSCONNECTOR_STATUS_UNSUPPORTED` |

The mapping is intentionally one-way. Existing smoke semantics and exit codes
stay unchanged. Python/Shell runners mirror this mapping through
`tests/runners/msconnector_models.py`; they do not load the C helper through
FFI.

## Import Status

| Status | Meaning |
| --- | --- |
| `fully-imported-common` | Source-derived case passed on Apache and NGINX real connector paths |
| `connector-specific` | Valid only for a named connector |
| `mapped-only` | Source is documented but not executable as an active smoke |
| `blocked` | Relevant source exists but current harness cannot execute it |
| `xfail` | Probeable case with known instability or expected failure |

`tests/import-status.json` is the machine-readable manifest for import status
counts. Connector summaries copy those counts into `import_status`.

## Result Metadata

Every connector summary JSON includes:

- `status_model: "msconnector_status"`
- `origin_model: "msconnector_origin"`
- `intervention_model: "msconnector_intervention"`
- `connector_path: "real-world"`
- `validation_mode: "real-world-connector-path"`
- `environment`: `SMOKE_ENVIRONMENT`, otherwise `github-actions` or `local`
- `audit_behavior`: `stable`, `unstable`, or `unexpected`
- `verified_variables`: derived only from passing active cases

Each case entry also includes an `intervention` object with the neutral
`msconnector_intervention` shape: `disruptive`, `status`, and `log_message`.
For non-disruptive expectations the intervention status is `0`; the expected
HTTP response remains available as `expected_status`.

`audit_behavior` is `unstable` while the `nolog,pass` no-audit case remains an
xfail due the local/GitHub Actions difference.
