# RAW Argument Collections Evidence

Status: mapped-only

Upstream PR: https://github.com/owasp-modsecurity/ModSecurity/pull/3564  
Upstream repository: https://github.com/owasp-modsecurity/ModSecurity

PR #3564 introduces RAW argument collection support in ModSecurity:

- `ARGS_RAW`
- `ARGS_GET_RAW`
- `ARGS_POST_RAW`
- `ARGS_NAMES_RAW`
- `ARGS_GET_NAMES_RAW`
- `ARGS_POST_NAMES_RAW`

## Current Classification

The locally observed ModSecurity v3 reference is:

| Repository | Local reference | Upstream | Observed commit | Observed version/tag |
| --- | --- | --- | --- | --- |
| ModSecurity v3 | `/root/conecter/ModSecurity_V3` | https://github.com/owasp-modsecurity/ModSecurity | `0fb4aff98b4980cf6426697d5605c424e3d5bb60` | `v3.0.15` |

This source is treated as read-only. RAW argument collections are not counted as
active common PASS in this repository unless the configured local v3 source
contains the feature and both Apache and NGINX return the expected real HTTP
behavior through the shared smoke harness.

## Import Rule

Future RAW-ARGS YAML cases may become active only after all of these are true:

- source evidence points to a configured ModSecurity v3 checkout with PR #3564
  behavior available;
- Apache and NGINX build against that source under `BUILD_ROOT`;
- both connector smokes return the expected HTTP status for the same YAML case;
- `verified_variables` is updated only from passing active cases.

Until then, RAW-ARGS remains mapped-only/evidence-only.
