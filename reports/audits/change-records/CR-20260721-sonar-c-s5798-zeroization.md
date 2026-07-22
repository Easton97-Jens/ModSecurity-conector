# Change Record: Portable C secure-zero hardening for SonarQube Cloud c:S5798

**Language:** English | [Deutsch](CR-20260721-sonar-c-s5798-zeroization.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260721-sonar-c-s5798-zeroization |
| Date (UTC) | 2026-07-21 |
| Base revision | 5c26ffb698a892ffe83b7aa1749a456eae10b956 |
| Tracking | Parent-only SonarQube Cloud c:S5798 keys AZ9MwjLo-bUaKQ_zSGBD, AZ9MwjLo-bUaKQ_zSGBE, AZ9MwjLo-bUaKQ_zSGBK, and AZ9cRyrNHhV2CayPTP0O; local finding FND-SONAR-0012 |
| Boundary | Parent Common runtime, shared C allocator helper, and Envoy ext_proc bridge only. Framework, MRTS, and the Parent gitlink are unchanged. |

## Motivation and problem statement

The four tracked C locations used an ordinary
memset(..., 0, sizeof(*object)) immediately before free. An optimizer may remove
a store whose target is dead after free. The scoped objects can contain a
remote-rule key, runtime configuration, or bounded request/decision metadata.
The report is a credible memory-remanence hardening lead, not proof of an
end-to-end information disclosure: no heap-disclosure primitive or cross-tenant
reuse was demonstrated.

## Acceptance criteria

- Preserve existing native cleanup, object-release order, null-pointer, and
  pointer-nulling behavior.
- Use one C17-portable, non-elidable wiping primitive at all four scoped
  object-release sites without a Sonar suppression, rule change, or quality-gate
  modification.
- Prove the primitive clears representative nonzero bytes before release;
  compile available C paths warning-clean under GCC and Clang, including -O2.
- Record exact-head hosted SonarQube Cloud disposition before claiming the four
  keys verified; do not claim the unavailable Envoy product build passed.

## Implementation decision and rationale

A shared msconnector_secure_zero(void *, size_t) function now writes zero
through a volatile unsigned-char pointer. The three Common runtime destruction
paths and Envoy bridge transaction close call it with sizeof(*object)
immediately before free. The ordinary initialization memset in runtime_defaults
is intentionally unchanged because it is not a pre-release wipe.

memset_s was not selected: C17 Annex K is optional and is not the portable
baseline of this repository. A shared helper avoids a bridge-local duplicate and
gives the C17 implementation one reviewed contract.

## Security impact

Before returning the four scoped object representations to the allocator, the
new behavior retains observable zero-byte stores under optimized GCC and Clang
builds. It does not lower a validation, resource, authentication, isolation, or
logging control. It neither claims to wipe libmodsecurity-owned allocations
after their cleanup nor demonstrates an end-to-end disclosure exploit.

The change is source and ABI additive within the Parent repository. Existing
destructor ordering and public connector protocol behavior are unchanged.

## Changed files

- common/include/msconnector/memory.h
- common/src/memory.c
- common/runtime/msconnector_runtime.c
- connectors/envoy/ext_proc/internal/processor/common_runtime_bridge.c
- ci/checks/common/check-common-memory-safety.sh
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Commands executed

| Command | Result |
| --- | --- |
| rtk proxy env BUILD_ROOT=<isolated external task build root> make check-common-memory-safety | Passed after the implementation. The strengthened test had first failed as expected before the helper existed. |
| rtk proxy env BUILD_ROOT=<isolated external task build root>/gcc CC=gcc make check-common-memory-safety | Passed with C17 warnings-as-errors. |
| rtk proxy env BUILD_ROOT=<isolated external task build root>/clang CC=clang make check-common-memory-safety | Passed with C17 warnings-as-errors. |
| rtk proxy env BUILD_ROOT=<isolated external task build root>/gcc-o2 CC=gcc MSCONNECTOR_CFLAGS=-std=c17 -O2 -Wall -Wextra -Werror make check-common-memory-safety | Passed. |
| rtk proxy env BUILD_ROOT=<isolated external task build root>/clang-o2 CC=clang MSCONNECTOR_CFLAGS=-std=c17 -O2 -Wall -Wextra -Werror make check-common-memory-safety | Passed. |
| rtk proxy env BUILD_ROOT=<isolated external task build root>/common-helpers CC=gcc make check-common-helpers | Passed. |
| rtk proxy env LC_ALL=C gcc and clang -std=c17 -O2 -Wall -Wextra -Werror -S common/src/memory.c | Passed; both assemblies retain zero-byte stores in msconnector_secure_zero. |
| rtk proxy env LC_ALL=C gcc and clang -std=c17 -Wall -Wextra -Werror -fsyntax-only connectors/envoy/ext_proc/internal/processor/common_runtime_bridge.c | Passed. |
| rtk proxy env BUILD_ROOT=<isolated external task build root>/envoy sh connectors/envoy/build/build_ext_proc.sh | Blocked, exit 77: MODSECURITY_INCLUDE_DIR or MODSECURITY_PREFIX was not supplied. |
| rtk git diff --check | Passed after the final documentation edit. |
| rtk proxy env BUILD_ROOT=<isolated external task build root>/pr77-gcc-o2 CC=gcc MSCONNECTOR_CFLAGS=-std=c17 -O2 -Wall -Wextra -Werror make check-common-memory-safety | Passed on the current-master reconciliation tree. |
| rtk proxy env BUILD_ROOT=<isolated external task build root>/pr77-clang-o2 CC=clang MSCONNECTOR_CFLAGS=-std=c17 -O2 -Wall -Wextra -Werror make check-common-memory-safety | Passed on the current-master reconciliation tree. |
| rtk proxy env BUILD_ROOT=<isolated external task build root>/pr77-common-helpers CC=gcc MSCONNECTOR_CFLAGS=-std=c17 -O2 -Wall -Wextra -Werror make check-common-helpers | Passed on the current-master reconciliation tree. |
| rtk proxy make check-common-security-contract | Passed on the current-master reconciliation tree. |
| rtk proxy gcc -std=c17 -O2 -Wall -Wextra -Werror -I common/include -S common/src/memory.c | Passed; the inspected current reconciliation assembly retains volatile zero-byte stores in msconnector_secure_zero. |
| rtk proxy clang -std=c17 -O2 -Wall -Wextra -Werror -I common/include -S common/src/memory.c | Passed; the inspected current reconciliation assembly retains volatile zero-byte stores in msconnector_secure_zero. |
| rtk proxy git diff --cached --check origin/master | Passed after the current-master documentation-conflict resolution. |

The retained run-scoped English/German/JSON finding evidence and validation
summary are private, hash-addressed task artifacts for FND-SONAR-0012; no
private build paths or credentials are included in this versioned record.

## Runtime evidence

No complete native connector or Envoy runtime was exercised in this isolated
worktree. The retained evidence is limited to the focused allocator/free
callback smoke, Common-helper smoke, direct bridge syntax checks, and
compiler-aware optimized assembly inspection described above. The current-
master reconciliation also received a focused source/lifetime review of the
four wrapper-release sites. The smoke explicitly calls msconnector_secure_zero
before its observing free callback; it proves the helper at that call site but
does not make msconnector_free_checked a generic secure-free API or dynamically
exercise all four production destructor paths.

## Known limitations

- The full Envoy ext_proc product build and runtime tests were not run because
  the worktree has no supplied libmodsecurity development include directory and
  linkable library. The attempted build stopped at its explicit prerequisite
  check with exit 77 before compilation.
- No end-to-end heap disclosure proof exists; this record therefore describes
  security hardening, not a validated vulnerability.

## Remaining risks

The original PR #77 head ef801b316334285816bc1566e2640087ee137f7f had observed
successful required GitHub checks and SonarQube Cloud analysis, but it became
stale and conflicting and those results do not establish the current-master
reconciliation. The reconciled exact upstream head still requires fresh
GitHub, SonarQube Cloud, review, and Draft-delivery evidence. The remaining
host prerequisite can prevent future full Envoy-build verification until a
compatible libmodsecurity development installation is supplied.

## Checks not run and rationale

The full Envoy ext_proc product build and runtime suite were not run because
the required libmodsecurity headers and linkable library are absent from the
supplied environment. This also prevents dynamic exercise of the four real
release paths in their production bridge/runtime configuration. Hosted
SonarQube Cloud and GitHub checks cannot exist until the exact reconciled Draft
PR head is pushed.

## Final diff and review status

The source change was committed as 3ef1bb551b4bf98f2034335b44b0ca05e431c48d,
with later traceability commits producing the original PR #77 head
ef801b316334285816bc1566e2640087ee137f7f. This record corrects the earlier
pre-delivery wording. Current-master reconciliation and any resulting master
integration are separate delivery events: their final branch, commit, PR head,
checks, SonarQube Cloud disposition, review, and merge result must be observed
at their exact delivered heads and are not inferred here.
