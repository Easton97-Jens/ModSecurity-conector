# Common connector-neutral layer

**Language:** English | [Deutsch](README.de.md)

## Purpose and boundary

\`common/\` holds reusable, connector-neutral contracts and helpers shared by
adapter implementations. It can model request, response, transaction,
intervention, status, origin, logging, capability, and evidence shapes without
depending on an Apache, NGINX, HAProxy, Envoy, Traefik, or lighttpd SDK.

It is not a universal host adapter, an ABI for a server, or runtime proof.
Host lifecycle hooks, protocol framing, server configuration glue, and
client-visible enforcement remain in the appropriate connector tree. A
successful Common compile or contract check is not a production, CRS, complete
matrix, or runtime-verification claim.

## Structure and source of truth

| Path | Purpose | Source of truth / placement rule |
| --- | --- | --- |
| \`include/msconnector/\` | Public C-first neutral types and contracts | Headers define the shared interface shape. Keep only connector-neutral declarations here. |
| \`src/\` | Neutral C implementations | Add a \`.c\` implementation and its matching header-level contract together; see [src notes](src/README.md). |
| \`runtime/\` | Reusable local decision-service/runtime support | It must remain host-neutral and must not become a server hook implementation. |
| \`rules/\` | Checked-in targeted smoke rules | These are repository test inputs, not a statement of complete rule coverage. |
| \`scripts/\` | Local test/evidence helpers | Add portable helper code here only when it has no host SDK or system-path dependency. |
| \`docs/\` | Detailed design notes | The [Common architecture](../docs/architecture.md) is the current documentation index for boundaries and ownership. |

The checked-in headers and source are authoritative for the shared code
contract. The root [Makefile](../Makefile) is authoritative for validation
targets. Generated evidence and connector capabilities are not sources of
truth for the Common API.

## Where changes belong

Put a new neutral type in \`include/msconnector/\` and its implementation in
\`src/\` only when it can compile without a host SDK and has a clear
connector-neutral owner. Place a portable smoke/evidence helper in \`scripts/\`
or \`runtime/\`, with an associated test or check. Record design decisions in
\`docs/\` and the current architecture documentation.

Do not add Apache modules, NGINX directives, HAProxy SPOE/HTX processing,
Envoy filters, Traefik middleware, lighttpd module hooks, host build glue, or
server headers here. Do not commit runtime output, caches, external source
trees, download artifacts, secrets, or connector-local test cases.

## Variables and placeholders

The root Makefile owns these inputs. Their complete definitions and safety
rules are in the [variables reference](../docs/reference/variables.md).
The terminology for ownership, interventions, and lifecycle phases is in the
[glossary](../docs/reference/glossary.md).

| Name | Local meaning | Requiredness, format, and example |
| --- | --- | --- |
| \`MSCONNECTOR_C_STD\` | C language mode passed to Common helper compilation | Optional; repository default is \`c17\`. Use a supported profile such as \`c17\`, \`c23\`, or \`c2y\` only with the matching target and compiler support. |
| \`MSCONNECTOR_CFLAGS\` | Compiler flags for Common helpers | Optional; the repository default is \`-std=$(MSCONNECTOR_C_STD) -Wall -Wextra -Werror\`. \`$(MSCONNECTOR_C_STD)\` is Make syntax that expands the named Make variable; do not paste it into a shell as a literal. |
| \`MSCONNECTOR_COMPILER_ID\` | Compiler executable identifier used by standard detection | Optional; it defaults to the basename of \`CC\`. Supply an installed compiler name such as \`clang\` only when intentionally overriding detection. |
| \`BUILD_ROOT\` | Generated build/check workspace | Optional and derived by the root Makefile. An override must be an absolute writable path outside the checkout, for example \`/srv/modsecurity-work/build\`; it must not be a source or secret location. |
| \`<repository-root>\` | Documentation-only absolute checkout root | It names the checkout containing \`common/\` and \`Makefile\`; \`/srv/src/ModSecurity-conector\` is a portable example. Do not include the angle brackets in a command. |

None of these values is a secret. Do not introduce credentials, token values,
or user-specific paths into headers, source, test output, or documentation.

## Relevant targets

| Target | Purpose and outcome boundary |
| --- | --- |
| \`make check-common-helpers\` | Compiles and runs the isolated Common helper smoke with the selected C flags. Exit \`0\` only covers that check. |
| \`make check-common-sdk-contract\` | Verifies SDK-facing Common contract expectations without proving a host integration. |
| \`make check-common-security-contract\` | Checks Common security/data-flow constraints. It is not a penetration test. |
| \`make check-common-memory-safety\` | Runs the repository's focused memory-safety contract. It does not prove all runtime memory behavior. |
| \`make check-common-flow-integrity\` | Checks flow/ownership wiring at the contract level. |
| \`make check-directive-parity\` | Checks shared directive specification parity; connector-specific host parsing remains outside \`common/\`. |
| \`make lint\` | Includes these structural checks plus broader repository checks; it does not produce canonical runtime evidence. |

Use the [Common architecture](../docs/architecture.md),
[testing guide](../docs/testing-and-evidence.md), and
[evidence guide](../docs/testing-and-evidence.md) before treating any result as an
implementation or runtime claim.
