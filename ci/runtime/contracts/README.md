# Canonical Runtime Observation Contract

**Language:** English | [Deutsch](README.de.md)

This directory defines the one Parent-owned, connector-neutral contract for a
runtime claim. It does not run a host, grant a runtime PASS from a process
exit code, or replace a connector's structured evidence collection.

```text
connector-specific structured evidence
  -> strict connector adapter
  -> canonical runtime observation
  -> common validator
  -> canonical validation result
```

The versioned [transport schema](runtime-observation.schema.json) has seven
top-level fields: six objects (`identity`, `runtime`, `framework`, `isolation`,
`cleanup`, and `provenance`) plus `schema_version`. The semantic rules and secure file
handling live in [runtime_observation.py](runtime_observation.py); JSON Schema
alone is not treated as proof of a runtime claim.

## Identity and profile matrix

Every observation binds its connector, integration mode, profile, CRS and
MRTS axes, run ID, Parent/Framework/MRTS commits, producer, and producer
version. The following centrally defined matrix applies to every connector;
there are no connector-specific validator exceptions.

| Profile | Framework requirement | MRTS attestation | Required result |
| --- | --- | --- | --- |
| `no-crs-no-mrts` | selected, executed live no-CRS case | all five no-MRTS facts are `false` | live evidence and clean cleanup |
| `no-crs-with-mrts` | selected, executed live no-CRS case | all five MRTS facts are `true` | live evidence and clean cleanup |
| `with-crs-no-mrts` | selected, executed live CRS case | all five no-MRTS facts are `false` | live evidence and clean cleanup |
| `with-crs-with-mrts` | selected, executed live CRS case | all five MRTS facts are `true` | live evidence and clean cleanup |

For every profile `identity.mrts_commit` must be the supplied lowercase full
commit. For a no-MRTS profile it is an identity binding only: the producer
must not invoke an MRTS runner, load its inventory, start its process, create
a listener, use an MRTS artifact, or read an MRTS checkout.

Required runtime assertions are `config_test`, `host_start`, `reachability`,
`allow_case`, and `block_case`. `bypass_case` is the only centrally optional
assertion. A connector cannot mark another field `NOT_APPLICABLE`; an optional
assertion must explicitly be non-required, non-applicable, and unexecuted.

The framework section supports typed expectations, including `http_status`,
`intervention`, `action`, `rule_match`, `rule_id`, `event`, header/body,
transport, lifecycle, cleanup, compound, and `not_applicable` kinds. Body and
header cases use bounded semantic predicates or digests, never raw payload or
header values.

## PASS decision

The validator returns `PASS` only when all of the following hold:

- the identity and profile matrix match the supplied identity;
- every mandatory runtime assertion is present, live-executed, and matched;
- the framework case is selected, executed, live-executed, matched, has
  `CONTRACT_VALIDATED`, and has zero failure and mismatch counts;
- the profile's MRTS facts match and every cleanup counter is zero;
- producer, evidence class, evidence inventory, and evidence digests bind
  together; and
- the observation and referenced evidence pass safe input checks.

Missing mandatory evidence is `VALIDATION_FAILED` in `strict` policy and may
be `PARTIAL` only in explicit `partial` policy. Neither status is a PASS.

## Connector adapter boundary

| Connector | Contract state in this change |
| --- | --- |
| Envoy | strict structured adapter; normalized observations use the common validator |
| Lighttpd | strict structured adapter; normalized observations use the common validator |
| Traefik | strict structured adapter; normalized observations use the common validator |
| Apache | interface and canonical unit fixture only; live claims fail closed until a separate producer exists |
| HAProxy | interface and canonical unit fixture only; live claims fail closed until a separate producer exists |
| NGINX | representable as `protected-separate`; the generic validator fails closed without a verified broker bridge, and the protected root/broker production boundary is unchanged |

Canonical fixtures are test inputs, not synthetic live evidence and not
runtime capability proof. The `fixture` policy is available only to the
in-process API for those fixtures; the CLI exposes only `strict` and
`partial` policies.

## Safe input and output

`load_runtime_observation_file()` opens evidence roots and path components
descriptor-by-descriptor with no-follow flags. It accepts only current-UID
owned 0700 evidence roots and descendants plus regular files at exact mode
0600, rejects symlinks and hard links, verifies file identity before and after
reading, caps the input at 1 MiB, requires strict UTF-8 JSON, and rejects
duplicate keys and non-finite values. Relative evidence paths are bounded and
cannot contain an absolute path, traversal, raw log content, payload, or
secret-like metadata.

`write_canonical_evidence_file()` creates a fresh owner-only leaf through the
same descriptor-pinned boundary and refuses to overwrite a pre-existing
canonical result. It does not create privileged listeners, change ownership,
or require a root runner.

## API and CLI

The public Python API is:

```python
validate_runtime_observation(observation, expected_identity, policy)
```

It returns a bounded `ValidationResult`; callers must treat only
`result.status == "PASS"` as success. The command-line boundary is:

```sh
python3 ci/runtime/contracts/validate-runtime-observation.py \
  --observation "<private-evidence-root>/runtime-observation.json" \
  --evidence-root "<private-evidence-root>" \
  --connector envoy --profile with-crs-no-mrts --run-id RUN_ID \
  --parent-sha PARENT_SHA --framework-sha FRAMEWORK_SHA \
  --mrts-sha MRTS_SHA \
  --policy strict
```

The CLI emits payload-free JSON, exits `0` only for `PASS`, and exits `2` for
a validation failure or partial result. `--mrts-sha` is required for every
profile.

## Verification boundary

The contract tests exercise schema/semantic validation, fixtures, adapters,
file safety, and CLI behavior. They do not constitute a hosted runtime run,
live capability assertion, Framework delivery, or NGINX production-path
change.
