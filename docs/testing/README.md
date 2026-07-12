# Testing documentation

**Language:** English | [Deutsch](README.de.md)

Testing distinguishes source/contract checks, build/config checks, focused
runtime smokes, and evidence validation. Passing one layer does not imply that
another layer passed. The current documentation covers selected HTTP/1.1 core
routes only; it makes no production, CRS, HTTP/2, HTTP/3, complete-matrix, or
strict-for-all-connectors claim.

## Test layers

| Layer | Typical target | What it checks | What it does not establish |
|---|---|---|---|
| Structural/documentation | <code>make check-bilingual-docs</code>, <code>make lint</code> | Companion files, links, source contracts, syntax, and configured checks | Live connector traffic or canonical runtime evidence |
| Build | <code>make build-<connector></code> | A selected connector build stage | Configuration loading, runtime traffic, or a case outcome |
| Configuration | <code>make check-config-<connector></code> | Selected configuration can be loaded/checked | Request/response behavior |
| Focused runtime | <code>make runtime-smoke-<connector></code> | A narrow host smoke where provided | All cases, all transports, or full-lifecycle promotion |
| No-CRS baseline | <code>make no-crs-baseline-<connector></code> | Capability-selected repository baseline cases | CRS behavior or unsupported capabilities |
| Full lifecycle | <code>make full-lifecycle-<connector></code> | Selected profile plus lifecycle artifact production | Production readiness, all protocols, or strict behavior for every connector |
| Evidence validation | <code>make evidence-check-<connector></code> | Existing canonical run artifacts | A rerun of the host or a PASS for missing data |

The placeholder <code>&lt;connector&gt;</code> accepts only
<code>apache</code>, <code>nginx</code>, <code>haproxy</code>,
<code>envoy</code>, <code>traefik</code>, and <code>lighttpd</code>.
For example, <code>make check-config-nginx</code> checks the selected NGINX
configuration; it does not literally accept the string
<code>&lt;connector&gt;</code>.

## Common commands

### Local documentation and contract check

~~~sh
make quick-check
~~~

This runs the repository’s lint-oriented and diff-oriented checks. It requires
the Framework checkout and the configured local toolchain. It creates
diagnostics and may create temporary build cache content; it does not prepare
or exercise every external host.

### One selected full-lifecycle run

~~~sh
NO_CRS_RUN_ID="six-core-20260712T120000Z" make full-lifecycle-all-connectors
~~~

<code>NO_CRS_RUN_ID</code> is required for later aggregate evidence gates. It
must be a 1–128 character filesystem-safe identifier: it starts with an ASCII
letter or digit and may otherwise contain only letters, digits, <code>.</code>,
<code>_</code>, and <code>-</code>. The example value identifies one
run; it is not a default and must not contain a username, secret, ticket title,
slash, or <code>..</code>.

The target produces candidate artifacts for the selected routes. It does not
make an aggregate assurance merely because the command started or ended with a
technical exit code. Read [Evidence](../evidence/README.md) before interpreting
the output.

### Validate one finalized aggregate run

~~~sh
NO_CRS_RUN_ID="six-core-20260712T120000Z" make check-six-connector-core-completion
~~~

This is a read-only aggregate acceptance check. It requires finalized evidence
under <code>EVIDENCE_ROOT</code>; the root default is
<code>VERIFIED_EVIDENCE_ROOT/no-crs-evidence</code>. Set
<code>EVIDENCE_ROOT</code> only to an absolute evidence path containing the
run you intend to inspect, for example
<code>/srv/modsecurity-work/evidence/no-crs-evidence</code>. Do not point it at
the checkout or an unrelated evidence tree.

## Status values and exit codes

| Value | Meaning |
|---|---|
| <code>PASS</code> | The specific case/check met its recorded conditions. It does not generalize to unselected connectors, profiles, cases, or protocols. |
| <code>FAIL</code> | The case/check did not meet a required condition. |
| <code>BLOCKED</code> | A prerequisite was missing or unsafe. It is not a PASS and should name the missing condition. |
| <code>NOT EXECUTED</code> | The case/path was deliberately not run; no behavioral conclusion follows. |
| <code>NOT APPLICABLE</code> | The case does not apply to the selected profile/host model. |
| <code>UNSUPPORTED</code> | The selected host model cannot provide the capability that the case needs. |
| <code>NOT_EXECUTABLE</code> | Historical harness spelling for a case that cannot run in the environment. |
| <code>0</code> | The process completed its own technical contract. It does not mean every catalog case is PASS. |
| <code>1</code> | General runtime, configuration, or validation failure. |
| <code>2</code> | Invalid invocation, input, or validation/contract failure. |
| <code>77</code> | Missing prerequisite or optional environment condition, such as a Framework path or host component. |

## Cases, rules, and IDs

The repository-owned No-CRS catalog lives in
<code>modules/ModSecurity-test-Framework/tests/cases/no-crs-baseline/catalog.json</code>.
It selects only cases whose required capabilities apply to the selected host
profile. The rule file is
<code>modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf</code>.
Both are repository-relative paths from the connector repository root.

| ID / item | Context |
|---|---|
| <code>1100001</code> | P1 request-header deny rule |
| <code>1100101</code> | P2 request-body deny rule |
| <code>1100201</code> | P3 response-header deny rule |
| <code>1100301</code> | P4 response-body observation/late-intervention rule |
| <code>allow_without_marker</code> | Basic allow case |
| <code>deny_header_marker_403</code> | P1 deny case tied to <code>1100001</code> |
| <code>deny_request_body_marker_403</code> | P2 case tied to <code>1100101</code> |
| <code>deny_response_header_marker_403</code> | P3 case tied to <code>1100201</code> |
| <code>phase4_rule_observed</code> | P4 rule-observation case; it is not a visible pre-commit-403 assertion |
| <code>phase4_first_byte_before_response_end</code> | Requires synchronized first-byte-before-EOS artifacts |
| <code>phase4_no_full_response_buffering</code> | Requires evidence that the connector does not hold a complete response buffer |

These are not OWASP CRS rule IDs. The full rule/case reference, including
late-intervention cases and expected evidence fields, is in
[configuration variables](../configuration/variables.md#rule-ids-and-representative-case-ids).

## Test-selection variables

| Variable | Purpose | Default / format | Boundary |
|---|---|---|---|
| <code>NO_CRS_CONNECTORS</code> | Limits an aggregate target to a connector subset | Default: all six names; space-separated valid connector names | Omitting a connector does not create evidence for it |
| <code>NO_CRS_RULES_FILE</code> | Selects baseline rules | Default: Framework No-CRS rules; absolute existing file | Changing rules changes comparability |
| <code>SMOKE_CASES</code>, <code>TEST_CASE</code> | Narrows a direct harness diagnostic | Optional documented case ID/list | A narrow smoke is not an aggregate completion run |
| <code>CASE_SCOPE</code> | Selects a Framework/harness case scope | Harness default is commonly <code>all</code> | Does not alter the catalog or capability manifest |
| <code>FORCE_ALL_CASES</code>, <code>RUN_ONE_CASE</code> | Direct-run selector flags | Optional boolean values | Use for diagnosis only; record the actual selection |
| <code>NO_CRS_PROTOCOL_CLIENT</code> | Opts into an optional stage-owned protocol probe | Default <code>0</code>; use <code>1</code> to opt in | The probe is non-promoting and not an HTTP/2/HTTP/3 claim |

For each variable’s setter, scope, effect, and security notes, see the
[central variable reference](../configuration/variables.md).

## Test data and privacy

Results and events are evidence inputs, not a place for request bodies,
authorization headers, cookies, tokens, private keys, or passwords. Use
synthetic markers from the checked-in No-CRS baseline. If a local test needs a
secret to reach a private host, load it from a secure store and do not commit,
echo, or include it in canonical artifacts.

## Next reads

- [Evidence documentation](../evidence/README.md)
- [Connector documentation](../connectors/README.md)
- [Build documentation](../build/README.md)
- [Glossary](../reference/glossary.md)
