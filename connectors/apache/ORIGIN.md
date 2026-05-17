# Apache Connector Origin Map

Status: implemented

Source repository: `/root/conecter/ModSecurity-apache`  
Source branch: `master`  
Source commit: `0488c77f69669584324b70460614a382224b4883`  
Source describe: `v0.0.9-beta1-26-g0488c77`  
License: Apache-2.0, imported as `connectors/apache/upstream/LICENSE`

Central attribution: `licenses/apache/`

| Imported path | Original path | Repo | Commit | License | Import reason |
| --- | --- | --- | --- | --- | --- |
| `connectors/apache/upstream/LICENSE` | `LICENSE` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | License text for imported Apache connector files |
| `connectors/apache/upstream/AUTHORS` | `AUTHORS` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Upstream attribution |
| `connectors/apache/upstream/CHANGES` | `CHANGES` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Upstream change context |
| `connectors/apache/upstream/README.md` | `README.md` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Upstream build and usage context |
| `connectors/apache/upstream/autogen.sh` | `autogen.sh` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Autotools bootstrap |
| `connectors/apache/upstream/configure.ac` | `configure.ac` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Autotools configure source |
| `connectors/apache/upstream/Makefile.am` | `Makefile.am` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Automake build source |
| `connectors/apache/upstream/build/apxs-wrapper.in` | `build/apxs-wrapper.in` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | APXS build wrapper template |
| `connectors/apache/upstream/build/ax_prog_apache.m4` | `build/ax_prog_apache.m4` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache detection macro |
| `connectors/apache/upstream/build/find_apxs.m4` | `build/find_apxs.m4` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | APXS detection macro |
| `connectors/apache/upstream/build/find_libmodsec.m4` | `build/find_libmodsec.m4` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | libmodsecurity detection macro |
| `connectors/apache/upstream/src/mod_security3.c` | `src/mod_security3.c` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache module entrypoint |
| `connectors/apache/upstream/src/mod_security3.h` | `src/mod_security3.h` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache module header |
| `connectors/apache/upstream/src/msc_config.c` | `src/msc_config.c` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache connector configuration |
| `connectors/apache/upstream/src/msc_config.h` | `src/msc_config.h` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache connector configuration header |
| `connectors/apache/upstream/src/msc_filters.c` | `src/msc_filters.c` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache input/output filters |
| `connectors/apache/upstream/src/msc_filters.h` | `src/msc_filters.h` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache filter header |
| `connectors/apache/upstream/src/msc_utils.c` | `src/msc_utils.c` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache connector utilities |
| `connectors/apache/upstream/src/msc_utils.h` | `src/msc_utils.h` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache connector utility header |
| `connectors/apache/upstream/t/conf/extra.conf.in` | `t/conf/extra.conf.in` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Minimal test template directory required by configure/build inputs |
| `connectors/apache/upstream/tests/run-regression-tests.pl.in` | `tests/run-regression-tests.pl.in` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | `configure.ac` output template |
| `connectors/apache/upstream/tests/regression/misc/40-secRemoteRules.t.in` | `tests/regression/misc/40-secRemoteRules.t.in` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | `configure.ac` output template |
| `connectors/apache/upstream/tests/regression/misc/50-ipmatchfromfile-external.t.in` | `tests/regression/misc/50-ipmatchfromfile-external.t.in` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | `configure.ac` output template |
| `connectors/apache/upstream/tests/regression/misc/60-pmfromfile-external.t.in` | `tests/regression/misc/60-pmfromfile-external.t.in` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | `configure.ac` output template |
| `connectors/apache/upstream/tests/regression/server_root/conf/httpd.conf.in` | `tests/regression/server_root/conf/httpd.conf.in` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | `configure.ac` output template |

## Excluded Upstream Files

The full Apache regression tree, `.git`, `.travis.yml`, release scripts,
generated Autotools files, `.deps`, and build/runtime artifacts are not imported.

## Central Attribution Copies

The Apache upstream `LICENSE`, `AUTHORS`, and `CHANGES` files are also mirrored
under `licenses/apache/` for repository-level license review. The copies in this
`upstream/` tree remain authoritative for the imported source layout and are not
removed.

## Pruning Review

Last reviewed in `docs/upstream-pruning-analysis.md`.

No imported Apache files were removed in the pruning pass. The imported tree is
already limited to license/provenance files, Autotools build inputs, module
source files, and `.in` templates referenced by `configure.ac` or the retained
upstream test-template layout. Files with unclear build relevance are retained
until an isolated `$BUILD_ROOT` probe proves they can be removed without
breaking `make smoke-apache`, `make smoke-nginx`, and `make smoke-all`.
