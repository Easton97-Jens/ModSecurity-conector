# Sonar source roles

**Language:** English | [Deutsch](sonar-source-roles.de.md)

The checked-in [source-role contract](../config/testing/sonar-source-roles.json)
is the authority for <code>sonar.test.inclusions</code> in
[Automatic Analysis configuration](../.sonarcloud.properties) and
[CI scanner configuration](../sonar-project.properties). It classifies source;
it neither selects nor executes a behavioral test case. The separate active-case
inventory remains the authority for automatic test execution.

## Reviewed scope

The contract preserves four standard test patterns, the three existing exact
native C test files and the existing
<code>fuzz/common_http_headers_fuzz.c</code> fixture. It additionally identifies
45 individually reviewed fixture files. Every additional file has its exact
path, TEST role, purpose, source evidence and an actual caller or test
consumer recorded in the contract. Evidence includes exact checked-in line
anchors; a changed anchor fails the scope check and requires source review.

| Owning group | Additional exact files | Reviewed purpose |
| --- | --- | --- |
| <code>common-http-authorization</code> | 1 | Stub-runtime regression fixture; actual <code>common/runtime/http_authorization_service.c</code> remains MAIN and is measured separately. |
| <code>nginx-i12</code> | 4 | Sealed fixture runner, scenario inputs, bounded wire client and explicit invalid-return preload. |
| <code>apache-i12</code> | 14 | Private fixture launch/client/backend, case materialization, cancellation/keepalive operations and test-only sink/host/multipart observers. |
| <code>traefik-native-i12</code> | 6 | Acceptance backend/client/driver, selected-operation fault relays and own-child syscall observer. |
| <code>traefik-forwardauth-i12</code> | 7 | Synthetic physical acceptance endpoints, client/driver, explicit fault peer, authorization relay and private fixture CA. |
| <code>haproxy-i12</code> | 4 | Frozen SPOP fixtures, private SPOP/companion captures and immutable native-HTX fixture materialization. |
| <code>lighttpd-i12</code> | 7 | Bounded private wire clients and explicit spool-floor/socket-observation fixtures, plus the test-only SDK MIME accessor. |
| <code>native-observer</code> | 2 | The optional SDK accessor and explicit GNU link-wrap observer, both restricted to test artifacts. |

This is an exact-file correction. There is no blanket classification of
<code>ci/**</code> or connector harness directories. Mixed operational tooling,
preparation/provenance builders and
<code>connectors/haproxy/harness/i12_spop_wire.py</code> retain their production
role. The approved native-HTX fixture materializer is listed individually because
it only prepares immutable case inputs. Real product source remains MAIN,
including <code>common/src/headers.c</code>,
<code>common/src/test_result.c</code> and
<code>common/scripts/modsecurity_targeted_eval.cc</code>.

## Synchronization and report classification

The [generator](../ci/tools/sync-sonar-test-scope.py) owns only the single
<code>sonar.test.inclusions</code> line in each properties file. It preserves all
other project, source, language-version, gate and baseline settings. Invoke the
native commands through any execution proxy required by the local agreement:

~~~sh
python3 ci/tools/sync-sonar-test-scope.py --write
python3 ci/tools/sync-sonar-test-scope.py --check
~~~

The [classification helper](../ci/lib/sonar_source_roles.py) loads the same
contract and exposes <code>is_test_source(relativepath)</code>. It rejects
absolute, noncanonical, traversing and symlinked inputs. Batch consumers can
load <code>SourceRoles</code> once and pass that validated contract to the helper.
Coverage producers use the same roles rather than treating test-fixture hits as
production coverage. A role check is a static source check, not a test run or a
coverage import.

## Evidence boundaries

The historical I12 results retain their original source/run identities. Listing
these fixtures does not reopen a historical campaign, add active cases, assert
<code>I12_COMPLETE</code> or establish current-head host behavior. TEST files
remain analyzed as tests; no production exclusion is introduced.

The existing Sonar coverage requirement remains <code>new_coverage &gt;= 80</code>.
Correct classification does not establish that the threshold is achievable or
met. Actual report generation, successful scanner import and revision-bound
total/new-code metrics require their separate execution and server evidence.
