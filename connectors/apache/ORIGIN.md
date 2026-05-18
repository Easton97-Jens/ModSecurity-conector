# Apache Connector Origin Map

Status: adapter-owned source migration complete

Local reference: `/root/conecter/ModSecurity-apache`
Upstream source: https://github.com/owasp-modsecurity/ModSecurity-apache
Source branch: `master`
Source commit: `0488c77f69669584324b70460614a382224b4883`
Source describe: `v0.0.9-beta1-26-g0488c77`
License: Apache-2.0, retained in `licenses/apache/` and in the
adapter-owned build source at `connectors/apache/src/LICENSE`.

| Repository | Local reference | Upstream | Observed commit | Observed version/tag | License |
| --- | --- | --- | --- | --- | --- |
| ModSecurity-apache | `/root/conecter/ModSecurity-apache` | https://github.com/owasp-modsecurity/ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | `v0.0.9-beta1-26-g0488c77` | Apache-2.0 |

Central attribution: `licenses/apache/`
Per-file provenance: `connectors/apache/src/SOURCE_MAP.json`
Adapter-owned build source: `connectors/apache/src/`
Materialized build source: `$BUILD_ROOT/apache-build/connector-src/`

## Phase 11 Status

Phase 11 moved the Apache connector build input from the former
`connectors/apache/upstream/` reference tree to adapter-owned
`connectors/apache/src/`. A fresh materialized Autotools/APXS build and
real-world Apache smoke run passed before the former upstream tree was removed.

This was a source-location migration only. Apache hooks, filters, bucket
brigades, intervention translation, transaction ownership, YAML smoke
semantics, and `RESPONSE_BODY` classification were not changed.

## Adapter-Owned Files

| Adapter-owned path | Original path | Repo | Commit | License | Import reason |
| --- | --- | --- | --- | --- | --- |
| `connectors/apache/src/LICENSE` | `LICENSE` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | License text and `configure.ac` source anchor |
| `connectors/apache/src/AUTHORS` | `AUTHORS` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Upstream attribution |
| `connectors/apache/src/CHANGES` | `CHANGES` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Upstream change context |
| `connectors/apache/src/autogen.sh` | `autogen.sh` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Autotools bootstrap |
| `connectors/apache/src/configure.ac` | `configure.ac` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Autotools configure source |
| `connectors/apache/src/Makefile.am` | `Makefile.am` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Automake build source |
| `connectors/apache/src/build/apxs-wrapper.in` | `build/apxs-wrapper.in` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | APXS build wrapper template |
| `connectors/apache/src/build/ax_prog_apache.m4` | `build/ax_prog_apache.m4` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache detection macro |
| `connectors/apache/src/build/find_apxs.m4` | `build/find_apxs.m4` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | APXS detection macro |
| `connectors/apache/src/build/find_libmodsec.m4` | `build/find_libmodsec.m4` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | libmodsecurity detection macro |
| `connectors/apache/src/src/mod_security3.c` | `src/mod_security3.c` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache module entrypoint |
| `connectors/apache/src/src/mod_security3.h` | `src/mod_security3.h` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache module header |
| `connectors/apache/src/src/msc_config.c` | `src/msc_config.c` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache connector configuration |
| `connectors/apache/src/src/msc_config.h` | `src/msc_config.h` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache connector configuration header |
| `connectors/apache/src/src/msc_filters.c` | `src/msc_filters.c` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache input/output filters |
| `connectors/apache/src/src/msc_filters.h` | `src/msc_filters.h` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache filter header |
| `connectors/apache/src/src/msc_utils.c` | `src/msc_utils.c` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache connector utilities |
| `connectors/apache/src/src/msc_utils.h` | `src/msc_utils.h` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache connector utility header |
| `connectors/apache/src/t/conf/extra.conf.in` | `t/conf/extra.conf.in` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Test-template layout referenced by configure/build inputs |
| `connectors/apache/src/tests/run-regression-tests.pl.in` | `tests/run-regression-tests.pl.in` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | `configure.ac` output template |
| `connectors/apache/src/tests/regression/misc/40-secRemoteRules.t.in` | `tests/regression/misc/40-secRemoteRules.t.in` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | `configure.ac` output template |
| `connectors/apache/src/tests/regression/misc/50-ipmatchfromfile-external.t.in` | `tests/regression/misc/50-ipmatchfromfile-external.t.in` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | `configure.ac` output template |
| `connectors/apache/src/tests/regression/misc/60-pmfromfile-external.t.in` | `tests/regression/misc/60-pmfromfile-external.t.in` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | `configure.ac` output template |
| `connectors/apache/src/tests/regression/server_root/conf/httpd.conf.in` | `tests/regression/server_root/conf/httpd.conf.in` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | `configure.ac` output template |

## Repo-Owned Metadata Files

| Path | Purpose |
| --- | --- |
| `connectors/apache/src/README.md` | Adapter-owned source tree overview |
| `connectors/apache/src/metadata.c` | Summary/report origin metadata source |
| `connectors/apache/src/metadata.h` | Summary/report origin metadata declarations |
| `connectors/apache/src/SOURCE_MAP.json` | Machine-readable per-file provenance |

## Excluded Upstream Files

The full Apache regression tree, `.git`, `.travis.yml`, release scripts,
generated Autotools files, `.deps`, and build/runtime artifacts are not
imported. The former `connectors/apache/upstream/` tree was removed after
Phase 11 build and smoke proof; it is no longer an active or required path.

## Central Attribution Copies

The Apache upstream `LICENSE`, `AUTHORS`, and `CHANGES` files are mirrored
under `licenses/apache/` for repository-level license review. Those durable
copies remain even though the local upstream reference tree was removed.

## Pruning Review

Last reviewed in `docs/imports/upstream-pruning-analysis.md`.

Apache adapter-owned source may be reduced only after a functional replacement,
updated origin/license documentation, and passing real-world `smoke-apache` and
`smoke-all` evidence. Cosmetic deletion is not allowed.
