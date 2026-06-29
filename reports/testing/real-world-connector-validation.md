# Real-World Connector Validation

**Language:** English | [Deutsch](real-world-connector-validation.de.md)

Status: implemented

`real-world-connector-path` means the smoke result came from this path:

```text
HTTP client
  -> real Apache, NGINX, or HAProxy process
  -> real ModSecurity connector module or SPOA/SPOP integration path
  -> libmodsecurity
  -> rule variables
  -> real HTTP response
```

This is different from the connector-free libmodsecurity API smoke documented
under
`modules/ModSecurity-test-Framework/docs/testing/v3-api-smoke-test.md`. The API
smoke proves a public libmodsecurity C API path, but it does not prove that a
server connector populated the same variables, buffered the same bodies, wrote
the same audit artifacts, or ran the same hook phase.

## Why This Exists

Direct API tests do not exercise server and connector behavior. The
real-world connector path catches issues such as:

- server-specific query argument normalization before `ARGS` reaches
  libmodsecurity;
- headers not being passed into `REQUEST_HEADERS` as expected;
- request bodies not being read early enough for phase:2 rules;
- raw JSON body content being unavailable to `REQUEST_BODY`;
- multipart uploads not populating `FILES`, `FILES_NAMES`,
  `FILES_COMBINED_SIZE`, or `MULTIPART_FILENAME`;
- audit-log artifacts being written differently by a connector runtime;
- response filter behavior differing from direct API expectations.

If the server starts and the module loads, but an expected variable does not
reach libmodsecurity and the YAML expectation fails, that is `fail`, not
`blocked`. `blocked` is reserved for missing sources, downloads, build tools,
module artifacts, libraries, or runtime prerequisites.

## Current Proof Cases

The YAML cases are the only source of rules, requests, and expectations. The
connector harnesses materialize them and send real HTTP requests.

The current generated default runtime summaries report real-world connector
PASS evidence for these variable families. Full-Matrix and force-all evidence
also record FAIL classes for former expected-failure, future, connector-gap,
runtime-difference, semantic, capability, and response-body cases. Do not read
the table below as a blanket stable status for every YAML case.

| Verified variable | Example active cases | Status |
| --- | --- | --- |
| `ARGS` | `phase2_args_block`, `collection_args_get_block`, V2 operator/transform cases | Present in default connector smoke evidence where the case is promoted |
| `REQUEST_HEADERS` | `phase1_header_block` | Present in default connector smoke evidence where the case is promoted |
| `REQUEST_BODY` | `request_body_json_block`, `request_body_raw_text_block`, `json_request_body_block` | Present in default connector smoke evidence where the case is promoted |
| `FILES` | `multipart_files_value_block`, `multipart_files_names_block`, `multipart_files_combined_size`, `multipart_filename_block` | Remaining multipart gaps are classified and non-promoted |
| `XML` | `xml_request_body_block` | Remaining XML processor activation gaps are classified and non-promoted |
| `AUDIT_LOG` | `audit_log_phase1_block` | Explicit `nolog` and audit-evidence gaps are classified; no active `audit_log_evidence` next-fix cluster remains |
| `RESPONSE_HEADERS` | `response_header_basic` | Phase 3 response-header evidence is implemented; remaining MRTS DetectionOnly cases are classification-only |

`RESPONSE_BODY` is deliberately not listed as verified. The active
`response_body_pass` case proves pass-through with response-body access enabled,
but response-body rule-variable blocking remains mapped/xfail until both
connectors return stable HTTP 403 for the same YAML case.
ModSecurity-nginx PR #377 source changes are recorded as NGINX source
provenance, not as connector validation.

## Result Metadata

Each connector summary under `$BUILD_ROOT/results/` records:

```json
{
  "status_model": "msconnector_status",
  "origin_model": "msconnector_origin",
  "intervention_model": "msconnector_intervention",
  "connector_path": "real-world",
  "validation_mode": "real-world-connector-path",
  "server": "apache",
  "server_binary": "...",
  "module": "...",
  "libmodsecurity": "...",
  "origin": {
    "source": "adapter-owned|monorepo-upstream|external",
    "source_repo": "ModSecurity-apache",
    "source_commit": "...",
    "source_version": "...",
    "license": "Apache-2.0",
    "imported_path": "..."
  },
  "verified_variables": ["ARGS", "REQUEST_BODY"]
}
```

`verified_variables` is computed only from active cases whose result is
`pass`. Mapped-only, xfail, blocked, and failed cases do not add variables.

## Runtime Port And PID Safety

The harnesses choose ports deterministically from the requested base port and
scan forward for a free `127.0.0.1` listener slot. If a generated runtime pid
file remains from an earlier run, the harness only stops that process when the
pid file is under `BUILD_ROOT` and the process command line points back to the
same generated runtime directory.

The harnesses do not kill unrelated Apache, NGINX, or system processes. A pid
file that points outside the generated runtime is reported as `blocked`. If a
bind conflict still races after the preflight port check, the case retries once
on the next free port and keeps the normal `fail`/`blocked` distinction if the
server still cannot run.

## Current Connector Status

Current generated default runtime evidence:

| Connector | Runtime path | Integration path | Default summary |
| --- | --- | --- | --- |
| Apache | real Apache process | Apache module | 54 PASS / 0 FAIL / 0 BLOCKED |
| NGINX | real NGINX process | NGINX module | 60 PASS / 0 FAIL / 0 BLOCKED |
| HAProxy | real HAProxy process | SPOA/SPOP agent | 55 PASS / 0 FAIL / 0 BLOCKED |

These local results do not promote force-all failures, xfail probes,
mapped-only inventory, future cases, connector-gap cases, runtime-difference
cases, API-only smokes, or `RESPONSE_BODY` blocking.

Current force-all and Full-Matrix evidence:

| Scope | Result |
| --- | --- |
| Apache force-all | 100 PASS / 27 FAIL / 0 BLOCKED |
| NGINX force-all | 95 PASS / 39 FAIL / 0 BLOCKED |
| HAProxy force-all | 104 PASS / 23 FAIL / 0 BLOCKED |
| Full-Matrix | 3074 PASS / 782 FAIL / 0 BLOCKED |

Other environments must run the same smoke targets before claiming pass. The
Full-Matrix FAIL rows are classified in the generated reports and the final
consistency audit currently recommends no next runtime-fixable connector
cluster.

## Future Connectors

Envoy, Lighttpd, and Traefik need analogous proof before any runtime claim is
made:

- real server/proxy process;
- real integration module, plugin, filter, SPOE service, or middleware;
- libmodsecurity or documented equivalent integration path;
- active YAML cases sent as HTTP traffic;
- result summary with real server binary/module metadata and verified
  variables derived only from passing cases.

HAProxy has an evidence-scoped SPOA/SPOP runtime path. Its broader gaps remain
reported and non-promoted until runtime evidence justifies a narrower or wider
support claim.
