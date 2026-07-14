# Operations and security

**Language:** English | [Deutsch](operations-and-security.de.md)

## Scope

This guide consolidates repository-level operational and security boundaries.
It is not a production deployment guide and does not claim that a connector is
production-ready, runtime-secure, security-verified, CRS-verified, or complete
for every protocol or test case.

## Deployment boundary

Run a selected connector only with its documented host build, configuration,
rules, and runtime prerequisites. Build, cache, runtime, log, and evidence
directories must be writable locations outside the checkout. The repository
does not prescribe a developer-specific absolute path.

| Area | Required practice | Boundary |
| --- | --- | --- |
| Build/cache | Use documented externally writable roots and pinned/selected inputs | A successful build is not host traffic evidence |
| Runtime | Start only the selected host/profile with explicit inputs | A start check is not a request/response test |
| Evidence | Use a non-secret run ID and scoped evidence root | One run does not generalize to another profile |
| Configuration | Load only reviewed host, runtime, and rule inputs | A config check is not a lifecycle result |

## Logs, artifacts, and privacy

Logs and artifacts should contain the minimum metadata necessary to explain a
selected observation. Result and event records must remain payload-safe. Do not
store credentials, session material, cookies, authorization headers, private
keys, certificates, request bodies, response bodies, or a host-private path in
checked-in documentation or artifacts.

Rotate or bound log output in the operational environment. Preserve the run ID,
selected profile, effective non-secret configuration, connector identity, and
artifact provenance required by the applicable validator.

## Limits, timeouts, and buffering

| Control | Operational purpose | Security boundary |
| --- | --- | --- |
| Header and body limits | Bound resource consumption before processing | A higher limit is not evidence of safe buffering |
| Request/response timeouts | Bound a host or bridge wait | A timeout setting does not prove cancellation semantics |
| Response-body scope | Restrict inspected content types and bytes | Do not introduce a connector-owned complete response buffer |
| Event/log limits | Keep diagnostics bounded and payload-safe | Truncation must be represented truthfully |

The exact parser defaults and host contexts belong in the complete connector
configuration references, not in this operational overview.

## Updates, origin, and dependency handling

Keep source attribution, licenses, origin metadata, pinned component inputs,
and adapter metadata consistent with the checked-in source. Update a component
only through its documented source/build process and re-run the relevant
configuration, contract, and evidence checks. A changed source revision does
not itself promote any historical result.

The repository and Framework distinguish a missing optional prerequisite from a
silent fallback. Do not install global components, fall back to an arbitrary
system binary, or download a runtime dependency unless the invoked documented
workflow explicitly allows and records that action.

Connector-local <code>ORIGIN.md</code>, source maps, license material, and
adapter metadata remain the detailed provenance records. Retain enough
repository-level context here to explain that an imported/upstream path is not
an implementation or runtime claim.

| Component | Source URL | Observed commit | Observed version | License |
| --- | --- | --- | --- | --- |
| ModSecurity-apache | https://github.com/owasp-modsecurity/ModSecurity-apache | <code>0488c77f69669584324b70460614a382224b4883</code> | <code>v0.0.9-beta1-26-g0488c77</code> | Apache-2.0 |
| ModSecurity-nginx | https://github.com/owasp-modsecurity/ModSecurity-nginx | <code>9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846</code> | <code>v1.0.4-14-g9eb44fd</code> | Apache-2.0 |

Apache attribution is retained under <code>licenses/apache/</code> and
<code>connectors/apache/ORIGIN.md</code>; productive Apache source and
Autotools/APXS inputs are adapter-owned. NGINX attribution is retained under
<code>licenses/nginx/</code> and <code>connectors/nginx/ORIGIN.md</code>;
productive module source and configuration are adapter-owned. The recorded
NGINX phase-4 source change from
https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/377 at
<code>3d72b004ff27a78ea19c6b945870e2cae62a97ac</code> does not promote
<code>RESPONSE_BODY</code>.

| Engine reference | Source URL | Observed commit | Observed version | License |
| --- | --- | --- | --- | --- |
| ModSecurity v2 | https://github.com/owasp-modsecurity/ModSecurity | <code>02eed22d74667b32091eece088a8ebdf64b6ba67</code> | <code>v2.9.13</code> | Apache-2.0 |
| ModSecurity v3 | https://github.com/owasp-modsecurity/ModSecurity | <code>0fb4aff98b4980cf6426697d5605c424e3d5bb60</code> | <code>v3.0.15</code> | Apache-2.0 |

Do not import upstream Git directories or generated build artifacts. Update
origin maps and license copies when imported files change. Any future source
reduction requires retained attribution and the applicable isolated
build/smoke evidence; Git history retains the removed planning chronology.

## Troubleshooting

| Symptom | First check | Do not infer |
| --- | --- | --- |
| Build or config failure | Selected compiler/build guide and host config-check output | A source defect without inspecting the reported stage |
| Missing runtime component | Declared component/root variable and blocked prerequisite output | That an unrelated system binary is equivalent |
| Unexpected P4 result | Connector guide, phase event, commit/EOS metadata, and selected profile | A strict client action from a rule match alone |
| Report/status mismatch | Run ID, effective configuration, normalized records, and validator output | That a generated summary is raw runtime proof |

## Hardening backlog and non-claims

Transport hardening, cancellation behavior, strict late intervention,
performance, protocol coverage, CRS comparison, restart behavior, and extended
catalog coverage remain separately evidence-gated. Keep them as scoped work
items in current reports or connector guides rather than retaining historical
status snapshots in this document.

## Related references

- [Architecture](architecture.md)
- [Configuration](configuration.md)
- [Testing and evidence](testing-and-evidence.md)
- [Build documentation](build/README.md)
- [Codex extensions](development/codex-extensions.md)
- [CI security tooling](security/ci-security-tooling.md)
- Connector-local <code>ORIGIN.md</code> and source maps
