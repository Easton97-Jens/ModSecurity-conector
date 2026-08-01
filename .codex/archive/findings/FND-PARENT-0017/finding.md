# FND-PARENT-0017 — Traefik UDS private-parent validation accepted a cross-UID-replaceable ancestor

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-PARENT-0017` |
| Category | `security_hardening` |
| Repository / ownership | `parent` / `parent` |
| Priority | `P1` |
| Severity / confidence | `medium` / `validated` |
| Status / feasibility | `fixed` / `feasible_now` |
| Release blocker / security relevant | `true` / `true` |
| Connector / protocol / profile | Traefik / AF_UNIX pathname / native-traefik-middleware |

## Summary

The earlier UDS controls validated only the immediate current-user-owned,
exact-`0700` parent. A socket parent beneath a non-sticky group- or
other-writable ancestor could be replaced by a different UID after validation
and before `bind()`. The Python runner, focused shell harness, and C
listener/self-test now validate every ancestor. Writable ancestors are accepted
only when sticky-directory semantics protect a child entry owned by the
effective UID.

## Observed and expected behavior

Before the repair, a task-owned test made a non-sticky mode-`0777` ancestor
and a mode-`0700` child. Both the Python validator and C `--self-test`
accepted the child. A live foreign-UID exploit was not run because the
configured external root is private, but the acceptance gap and source-to-sink
race condition were concrete.

Every selected parent must now be absolute, canonical, symlink-free,
current-user-owned, exact-`0700`, and protected from cross-UID replacement by
the complete ancestor chain. A group- or other-writable ancestor must be sticky
and its direct child must belong to the effective UID. Invalid topology fails
before UDS allocation or `bind()`.

## Impact

With the former control, an operator-selected parent under a non-sticky,
cross-UID-writable ancestor could be renamed/replaced during the
validation-to-bind interval. The service could bind beneath an
attacker-controlled directory, weakening the intended UDS cross-UID boundary.
This repair does not address the separately tracked same-UID endpoint-redial or
cleanup races.

## Affected files and symbols

- `connectors/traefik/scripts/runtime_native_smoke.py` —
  `assert_private_engine_socket_parent_ancestors_are_safe`,
  `directory_entry_is_protected_from_cross_user_replacement`.
- `connectors/traefik/build/test-engine-service-runtime.sh` — equivalent shell
  preflight.
- `connectors/traefik/src/traefik_engine_service.c` —
  `traefik_engine_private_directory_ancestors_are_safe`,
  `traefik_engine_parent_protects_child_from_cross_uid_replacement`.
- `tests/test_traefik_native_local_plugin.py` — ancestor-predicate regression.

## Preconditions and reproduction

1. An operator selects a current-user-owned exact-`0700` parent beneath a
   non-sticky group- or other-writable ancestor.
2. A different local UID can traverse/write that ancestor and races after
   validation but before `bind()`.
3. In the old code, Python selection and C self-test accepted this topology.

The task-owned pre-fix control is retained in
`logs/119-private-parent-mutable-ancestor-control-gap-pre-fix-final.log`,
SHA-256 `25a6728bca11448352bd922384e22749570e7d453e393f6dd1092cec1abfeee7`.
It records Python acceptance and C engine exit `0`; its private outer root
means it is a control-gap reproduction rather than a live foreign-UID exploit.

## Remediation and validation

The narrow repair preserves the existing immediate-parent, no-symlink,
no-public-default, path-length, and same-UID residual controls. It adds the
same ancestor-replaceability test to Python, shell, and C:

- no group/other write on an ancestor is accepted;
- a writable ancestor is accepted only if sticky and its child belongs to the
  effective UID;
- a non-sticky mutable ancestor is rejected by Python, shell (exit `77`), and
  C self-test (exit `1`).

The post-fix negative controls passed in
`logs/123-private-parent-ancestor-negative-controls-final.log`, SHA-256
`0cc657a4a58763b44070215e7c354027c12688a1eb248e21cb9a76c9c4a2868c`.
Legitimate Allow/Blocking runtime behavior passed in `logs/125-*`, SHA-256
`c35d629326601b521feeb92953f7f43526cad2bc5b9d7e6c7316d22e85c0cb36`.

Normal C17 builds/self-tests passed with Clang (`logs/121`, SHA-256
`6d044ad0eb36b861fefe8e1d36b28ae6a59d91b48da5c14aca3b73e416612d80`) and
GCC (`logs/122`, SHA-256
`8c6ff06096212dde3a1f272f00b9ed7492c33bef35cfc820f0df074910605156`). A
separate external hardened diagnostic build passed (`logs/126`, SHA-256
`aef7a84d16c3d394bb3adf8d87b608193a1758f655a3d8382adf8eb352f29808`), as
did a combined ASan+UBSan runtime with leak detection enabled (`logs/128`,
SHA-256 `f2663195a519ad478d1001b44c9fea7584f92c88c1019f8da6520baa54f3587c`)
and GCC `-fanalyzer` (`logs/129`, SHA-256
`dd139757add71aae0683b12d0f6c9c60c1729f2d35db16c9c35e1008ca2d674a`).

## Residual risk and history

`FND-PARENT-0013` and `FND-PARENT-0015` remain open for same-UID pathname
cleanup and post-readiness endpoint identity. No risk is accepted. This finding
is locally fixed; exact-head SonarCloud verification remains a delivery
dependency of `FND-PARENT-0016`.

- `2026-07-17T16:17:28Z`: immediate-parent-only acceptance reproduced.
- `2026-07-17T16:56:51Z`: repair and focused Python/C/shell/runtime/hardened/
  sanitizer/analyzer controls passed.
