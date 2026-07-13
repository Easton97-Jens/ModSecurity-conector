# Apache Connector Origin Map

**Language:** English | [Deutsch](ORIGIN.de.md)

Status: adapter-owned source cleanup complete

Local reference: `<external-source-root>/ModSecurity-apache`
Upstream source: https://github.com/owasp-modsecurity/ModSecurity-apache
Source branch: `master`
Source commit: `0488c77f69669584324b70460614a382224b4883`
Source describe: `v0.0.9-beta1-26-g0488c77`
License: Apache-2.0, retained in `licenses/apache/`.

| Repository | Local reference | Upstream | Observed commit | Observed version/tag | License |
| --- | --- | --- | --- | --- | --- |
| ModSecurity-apache | `<external-source-root>/ModSecurity-apache` | https://github.com/owasp-modsecurity/ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | `v0.0.9-beta1-26-g0488c77` | Apache-2.0 |

Central attribution: `licenses/apache/`
Per-file provenance: `connectors/apache/SOURCE_MAP.json`
Adapter-owned build source root: `connectors/apache/`
Productive source files: `connectors/apache/src/`
Materialized build source: `$BUILD_ROOT/apache-build/connector-src/`

## Phase 11 Status

Phase 11 moved the Apache connector build input from the former
`connectors/apache/upstream/` reference tree to adapter-owned
`connectors/apache/src/`. A fresh materialized Autotools/APXS build and
real-world Apache smoke run passed before the former upstream tree was removed.

This was a source-location migration only. Apache hooks, filters, bucket
brigades, intervention translation, transaction ownership, YAML smoke
semantics, and `RESPONSE_BODY` classification were not changed.

## Phase 12 Status

Phase 12 removed attribution/history/documentation-only files from
`connectors/apache/src/` after changing the Autoconf source anchor from
`LICENSE` to the functional source file `src/mod_security3.c`. The active
Apache source tree is now a build/runtime tree; durable attribution stays in
`licenses/apache/`, this origin map, and `connectors/apache/SOURCE_MAP.json`.

## Phase 13 Status

Phase 13 simplified the adapter-owned layout without changing runtime
semantics. Autotools/APXS files now live at `connectors/apache/`, productive
Apache C sources live directly under `connectors/apache/src/`, and retained
Autotools test templates live under `modules/ModSecurity-test-Framework/tests/upstream/connector-specific/apache/`. The materializer
still writes the upstream-compatible build layout under
`$BUILD_ROOT/apache-build/connector-src`.

## Adapter-Owned Files

| Adapter-owned path | Original path | Repo | Commit | License | Import reason |
| --- | --- | --- | --- | --- | --- |
| `connectors/apache/autogen.sh` | `autogen.sh` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Autotools bootstrap |
| `connectors/apache/configure.ac` | `configure.ac` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Autotools configure source; local source anchor now points at `src/mod_security3.c` |
| `connectors/apache/Makefile.am` | `Makefile.am` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Automake build source |
| `connectors/apache/build/apxs-wrapper.in` | `build/apxs-wrapper.in` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | APXS build wrapper template |
| `connectors/apache/build/ax_prog_apache.m4` | `build/ax_prog_apache.m4` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache detection macro |
| `connectors/apache/build/find_apxs.m4` | `build/find_apxs.m4` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | APXS detection macro |
| `connectors/apache/build/find_libmodsec.m4` | `build/find_libmodsec.m4` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | libmodsecurity detection macro |
| `connectors/apache/src/mod_security3.c` | `src/mod_security3.c` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache module entrypoint |
| `connectors/apache/src/mod_security3.h` | `src/mod_security3.h` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache module header |
| `connectors/apache/src/msc_config.c` | `src/msc_config.c` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache connector configuration |
| `connectors/apache/src/msc_config.h` | `src/msc_config.h` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache connector configuration header |
| `connectors/apache/src/msc_filters.c` | `src/msc_filters.c` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache input/output filters |
| `connectors/apache/src/msc_filters.h` | `src/msc_filters.h` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache filter header |
| `connectors/apache/src/msc_utils.c` | `src/msc_utils.c` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache connector utilities |
| `connectors/apache/src/msc_utils.h` | `src/msc_utils.h` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache connector utility header |
| `modules/ModSecurity-test-Framework/tests/upstream/connector-specific/apache/t/conf/extra.conf.in` | `t/conf/extra.conf.in` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Test-template layout referenced by configure/build inputs |
| `modules/ModSecurity-test-Framework/tests/upstream/connector-specific/apache/run-regression-tests.pl.in` | `tests/run-regression-tests.pl.in` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | `configure.ac` output template |
| `modules/ModSecurity-test-Framework/tests/upstream/connector-specific/apache/regression/misc/40-secRemoteRules.t.in` | `tests/regression/misc/40-secRemoteRules.t.in` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | `configure.ac` output template |
| `modules/ModSecurity-test-Framework/tests/upstream/connector-specific/apache/regression/misc/50-ipmatchfromfile-external.t.in` | `tests/regression/misc/50-ipmatchfromfile-external.t.in` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | `configure.ac` output template |
| `modules/ModSecurity-test-Framework/tests/upstream/connector-specific/apache/regression/misc/60-pmfromfile-external.t.in` | `tests/regression/misc/60-pmfromfile-external.t.in` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | `configure.ac` output template |
| `modules/ModSecurity-test-Framework/tests/upstream/connector-specific/apache/regression/server_root/conf/httpd.conf.in` | `tests/regression/server_root/conf/httpd.conf.in` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | `configure.ac` output template |

## Repo-Owned Metadata Files

| Path | Purpose |
| --- | --- |
| `connectors/apache/metadata.c` | Summary/report origin metadata source |
| `connectors/apache/metadata.h` | Summary/report origin metadata declarations |
| `connectors/apache/SOURCE_MAP.json` | Machine-readable per-file provenance |

## Relocated Attribution Files

| Former source-tree path | Durable location | Reason |
| --- | --- | --- |
| `connectors/apache/src/LICENSE` | `licenses/apache/LICENSE` | License text is attribution metadata, not an Apache build input after the source anchor moved to `src/mod_security3.c` |
| `connectors/apache/src/AUTHORS` | `licenses/apache/AUTHORS` | Upstream attribution is retained centrally |
| `connectors/apache/src/CHANGES` | `licenses/apache/CHANGES` | Upstream change history is retained centrally |
| `connectors/apache/src/README.md` | `connectors/apache/README.md` and docs under `docs/` | Source-tree overview belongs in connector documentation |

## Phase 13 Layout Moves

| Former path | Current path | Materialized path |
| --- | --- | --- |
| `connectors/apache/src/autogen.sh` | `connectors/apache/autogen.sh` | `autogen.sh` |
| `connectors/apache/src/configure.ac` | `connectors/apache/configure.ac` | `configure.ac` |
| `connectors/apache/src/Makefile.am` | `connectors/apache/Makefile.am` | `Makefile.am` |
| `connectors/apache/src/build/` | `connectors/apache/build/` | `build/` |
| `connectors/apache/src/src/*.c`, `*.h` | `connectors/apache/src/*.c`, `*.h` | `src/*.c`, `*.h` |
| Apache generated source `t/conf/extra.conf.in` template | `modules/ModSecurity-test-Framework/tests/upstream/connector-specific/apache/t/conf/extra.conf.in` | `t/conf/extra.conf.in` |
| Apache generated source test-template tree | `modules/ModSecurity-test-Framework/tests/upstream/connector-specific/apache/` | `tests/` |
| `connectors/apache/src/metadata.*` | `connectors/apache/metadata.*` | not materialized |
| `connectors/apache/src/SOURCE_MAP.json` | `connectors/apache/SOURCE_MAP.json` | not materialized |

## Excluded Upstream Files

The full Apache regression tree, `.git`, `.travis.yml`, release scripts,
generated Autotools files, `.deps`, and build/runtime artifacts are not
imported. The former `connectors/apache/upstream/` tree was removed after
Phase 11 build and smoke proof; it is no longer an active or required path.

## Central Attribution Copies

The Apache upstream `LICENSE`, `AUTHORS`, and `CHANGES` files are retained
under `licenses/apache/` for repository-level license review. Those durable
copies remain even though the local upstream reference tree and source-tree
duplicates were removed.

## Pruning Review

The Framework's current [connector integration guide](../../modules/ModSecurity-test-Framework/docs/connector-integration.md)
records the applicable source/catalog boundary.

Apache adapter-owned source may be reduced only after a functional replacement,
updated origin/license documentation, and passing real-world `smoke-apache` and
`smoke-all` evidence. Cosmetic deletion is not allowed.
