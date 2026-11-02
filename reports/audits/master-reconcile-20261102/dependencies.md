# Build component inventory and advisory assessment

**Language:** English | [Deutsch](dependencies.de.md)

Checked on 2026-11-02 against Connector430d3194fa04ca4aafcdaef6aeb256d21dc18f0c and Framework 91145b7ba721bdec4e89af754cf40bf496fd2a08. [Machine-readable inventory](component-inventory.json) contains 17 native/runtime/toolchain components, four direct and six indirect Envoy Go requirements, three go.sum-only entries and 11 observed installed development packages. This is a source/build inventory, not an exhaustive binary or container SBOM. A checksum file does not prove linkage.

## Findings requiring further work

| Component | Selected / reviewed release | Disposition |
| --- | --- | --- |
| NGINX | release-1.31.6 / fixed mainline minimum 1.31.7, observed 1.31.8 | Upstream version falls inside five published ranges. HTTP/3 is an actual optional build/configuration path. Selected H1 fixture omits several advisory prerequisites; arbitrary consumer configurations remain unresolved. No exploit or patched build was demonstrated. |
| Envoy | 1.39.1 / fixed 1.39.2, observed 1.39.6 | BoringSSL certificate-memory fix is newer. Selected TLS template verifies a supplied CA; attacker control of an admitted certificate was not established. Patched tuple/build and local reachability remain open. |
| Parent Python | 3.15.1 / security3.15.2 | Security release fixes CA distrust and tar_filter link replacement. Exact reviewed runner readiness and reachable archive/TLS preconditions remain unverified. Existing Python/bootstrap PRs remain separately owned. |

Official evidence: [NGINX advisories](https://nginx.org/en/security_advisories.html), [NGINX releases](https://nginx.org/news.html), [Envoy1.39.2](https://www.envoyproxy.io/docs/envoy/v1.39.2/version_history/v1.39/v1.39.2), [Python 3.15.2](https://www.python.org/downloads/release/python-3152/).

These unresolved items are not closed by general CI. No runtime tuple was changed without its reviewed provenance, generator and matching build/regression evidence. The remaining action is a focused, reviewed tuple update and appropriate build validation, preserving protected NGINX admission and existing maintenance ownership.

## Conditions excluded by evidence

Traefik 3.7.13 is downloaded as a hash-verified official release. The [SNI advisory](https://github.com/traefik/traefik/security/advisories/GHSA-fh26-gfpp-7xxx) explicitly excludes official Go1.26 binaries; Parent Go1.27.3 does not imply that the official host was rebuilt. Selected ForwardAuth templates do not configure NTLM/Negotiate connection-bound authentication. [ForwardAuth](https://github.com/traefik/traefik/security/advisories/GHSA-hrpp-p4fc-wwf8) and [FastProxy](https://github.com/traefik/traefik/security/advisories/GHSA-53qr-784g-cj35) conditions remain relevant for custom deployments; those deployments were not qualified. Latest observed Traefik is 3.7.17.

The real Envoy default-build package graph produced with go1.27.3 contains x/net HTTP2/HPACK, IDNA, trace and internal helper packages, but no golang.org/x/net/html. Consequently [GO-2026-6866](https://pkg.go.dev/vuln/GO-2026-6866) and [GO-2026-6860](https://pkg.go.dev/vuln/GO-2026-6860), whose module range includes x/net v0.61.0 and fix is v0.62.0, are not reachable through that observed graph. Reassess new tags/custom builds. No blanket x/net or remaining-module security claim follows.

Framework Python 3.14.10, OpenSSL 4.0.3, ModSecurity v3.0.17 and PCRE2 10.49 include the selected published fixes listed in the inventory. Apache 2.4.69, APR 1.7.6, APR-util 1.6.5, HAProxy 3.2.25, lighttpd 1.4.85 and PyYAML 6.0.3 match observed upstream versions; freshness alone proves no absence of vulnerabilities. AWS-LC v5.11.0 is explicitly an unused future candidate, not an active runtime requiring an update merely because 5.12.0 exists.

## Inventory boundaries

Installed Ubuntu development metadata was queried for GCC/G++, APR/APR-util, curl, LMDB, PCRE2, OpenSSL, libxml2, YAJL and zlib. Several installed versions differ from canonical source tuples. They are recorded separately; no selected product artifact linkage or distribution-patch advisory assessment was inferred. Full native transitive features, vendored submodules, downloaded artifact linkage, OS/container package graphs and complete remaining-module advisory coverage stay unresolved.

No packages or source versions were updated by this inventory pass. The coverage-only task environment uses the existing hash-locked coverage 7.17.0 requirement; no global environment or dependency lock was changed.

Lokale Sonar-Secrets-Prüfung aufgrund ausdrücklicher Benutzeranweisung nicht ausgeführt.
