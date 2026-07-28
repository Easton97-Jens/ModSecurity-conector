# Change Record: Traefik result optional-text nullability remediation for SonarQube Cloud

**Language:** English | [Deutsch](CR-20260728-sonar-traefik-result-nullability.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260728-sonar-traefik-result-nullability |
| Date (UTC) | 2026-07-28 |
| Base revision | 8e8acb8dab1cd03723de269cab7da7dd62e5e010 |
| Boundary | Parent Traefik C engine-result serialization and its focused source-contract test, plus this English/German Change Record pair and indexes only. Framework, MRTS, both gitlinks, workflows, scanner policy, and generated reports remain unchanged. |
| Finding linkage | Targets live SonarQube Cloud `c:S2637` issue keys `AZ9cRyv8HhV2CayPTP10`, `AZ9cRyv8HhV2CayPTP11`, and `AZ9cRyv8HhV2CayPTP12`. The issues remain externally open until an exact-head hosted analysis observes the candidate. |

## Motivation and problem statement

`traefik_engine_send_result` serializes optional transaction, rule, and
redirect text into a private local-engine Unix-socket result frame. The prior
implementation guarded each `memcpy` with a null test and a length test. The
runtime accessor and decision fields are legitimately nullable, but the
analyzer could not prove that the pointer was non-null at the copy site.

The required remediation must retain the wire contract: an absent optional
value is an empty, zero-length field, and present values retain their exact
bytes and field order. It must not add a suppression, change the protocol, or
weaken the existing size limits.

## Acceptance criteria

- The three optional source pointers used by the result serializer have a
  non-null immutable empty-text default.
- Nullable runtime and decision inputs replace that default only after an
  explicit null check.
- Empty optional values still produce zero-length fields; non-empty values
  preserve the original order, lengths, action, phase, status, and flags.
- A direct C17 socket-pair harness compiles the actual translation unit and
  verifies both the all-empty and populated result frames byte-for-byte.
- The focused source contract, whitespace check, and focused security-diff
  review pass without a suppression or scanner/CI-policy change.
- No hosted issue closure, PR state, merge, master update, Framework/MRTS
  change, or full host-runtime result is claimed before it is observed.

## Implementation decision and rationale

`traefik_engine_empty_text` is a private immutable empty C string. The three
serializer pointers start at that value. The function obtains the nullable
runtime transaction ID and nullable decision fields into local variables, and
uses each only if it is non-null. Consequently, the bounded-string helper and
the later `memcpy` calls always receive non-null inputs while the existing
size-limited serialization remains intact.

No control flow is moved across the decision/session boundary. The decision
kind, phase, HTTP-status clamp, disruptive and late-intervention flags, frame
header, field ordering, and maximum field limits remain where they were. A
missing value has the same zero size as before, so it writes no payload bytes.

## Changed files

- `connectors/traefik/src/traefik_engine_service.c`
- `tests/test_sonar_reliability_contract.py`
- `reports/audits/change-records/README.md` and `README.de.md`
- this English/German Change Record pair

## Commands executed

| Command or control | Result |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 .venv/bin/python -B tests/test_sonar_reliability_contract.py` | passed: 11 tests, including the C17 compile-and-run result-frame harness. |
| `.venv/bin/python -m unittest -v tests.test_c_cpp_diagnostics` | passed: 7 C/C++ diagnostics-contract tests. |
| `TMPDIR=<task-owned external root> make check-remaining-connectors-c17` | passed: every remaining-connector C translation unit, including the changed Traefik engine service, compiles under C17 with `-Wall -Wextra -Werror`. |
| `.venv/bin/python -m unittest -v tests.test_bilingual_docs tests.test_traefik_native_local_plugin tests.test_traefik_runtime_smoke_security` | passed: 39 focused documentation and Traefik runtime/security-contract tests. |
| `git diff --check` | passed; no whitespace errors. |
| Repository bilingual-documentation checker against a task-owned external candidate overlay with the Parent-pinned Framework revision `47e50e7bc43ba7a3b5bad1a9448111794f664cc0` | passed: language pairs, Change Record structure, links, and Framework references resolve without changing any checkout. |
| Focused `codex-security:security-diff-scan` of the exact local patch | passed; no reportable vulnerability candidate. The sealed scan report is bound to patch SHA-256 `f221a59b23fe79abd46f3f0ec9a3364030492960d0381c8552c8bd4c415a2df7`. |
| Normal task-branch push and Draft PR creation | completed: [Parent PR #150](https://github.com/Easton97-Jens/ModSecurity-conector/pull/150) is open against `master`; its exact-head hosted checks remain pending. |

## Security impact

The changed function is a security-relevant private Unix-socket serialization
boundary. The remediation removes nullable pointer values at the copy sites
without expanding what can be serialized. Existing field-size bounds, uint16
clamping, result-frame construction, session checks, and decision metadata
handling are preserved. The focused review found no new untrusted
source-to-sink path, length bypass, lifetime regression, or transport change.

## Runtime evidence

The direct test includes the real C translation unit, links only the narrowly
required transaction-ID accessor stub, and executes
`traefik_engine_send_result` over a Unix socket pair. It proves zero-length
encoding for absent optional text and byte-exact populated-field encoding. It
is source-level protocol evidence, not a full Traefik/Common/libmodsecurity
host-runtime test.

## Known limitations

The isolated environment has no verified libmodsecurity headers or library:
`pkg-config libmodsecurity` is unavailable and no compatible include/library
pair was found in the approved local locations. Full host/plugin execution is
therefore not represented as a passing local result.

## Remaining risks

An external Traefik host, loaded plugin, and live Common/libmodsecurity
transaction may add behavior not exercised by the local source-level harness.
The exact SonarQube Cloud rule disposition also remains external until a fresh
analysis of the candidate head has completed.

## Checks not run and rationale

- The full `connectors/traefik` native host-runtime target was not run because
  its required verified libmodsecurity development dependency is absent; no
  substitute full-runtime claim is made.
- Exact PR-head CI, SonarQube Cloud analysis, review, and merge remain pending
  for Draft PR #150. The Draft state deliberately does not assert a quality
  result or merge eligibility.

## Final diff and review status

The implementation was committed and normally pushed on its task branch, and
[Draft Parent PR #150](https://github.com/Easton97-Jens/ModSecurity-conector/pull/150)
is open against `master`. Its focused source contract and security-diff review
passed. GitHub Actions, SonarQube Cloud, review, and every master action remain
unobserved for the current PR head. The three targeted external issues are not
claimed closed until fresh exact-head SonarQube Cloud evidence confirms it.
