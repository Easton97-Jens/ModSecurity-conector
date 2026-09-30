# Reviewed version upgrades

**Language:** English | [Deutsch](reviewed-version-upgrades.de.md)

## Ownership and approval

Framework `ci/lib/common.sh` owns the reviewed upstream identities. Parent consumers must agree with those identities, but consistency is not approval of a new release. NGINX stays outside the generic mutable-source registry; the exact ModSecurity-v3 repository/tag/commit tuple is registered. The Parent submodule updater is manually dispatched and no longer compares a candidate to a fixed shell-structure digest. It creates a Draft PR, never an automatic merge. Review the complete Framework delta and runtime checks before accepting that PR; a manual trigger is not source-code approval.

## Early consistency check

`ci/tools/check-reviewed-version-handoff.py` reads bounded regular files as data. It checks the closed source-data registry, the Framework NGINX release against its workflow and evidence writer, and the ModSecurity v3 tag/commit against the compiler-guide generator, its tests and both generated guides. It performs no network access, shell evaluation, source writes or dependency installation. Missing, conflicting, unsafe or symlinked inputs fail closed. The early quick-check runs it before expensive setup; full candidate and runtime gates remain required.

```sh
python3 ci/tools/check-reviewed-version-handoff.py --repo-root .
python3 -m unittest -v tests.test_reviewed_version_handoff tests.test_runtime_component_cache_identity
```

## Changing a release

Review the official source repository, release tag, exact commit and applicable archive digest together. After a separate Framework merge, manually dispatch the Parent updater on `master`; it validates the candidate and proposes the Framework reference and registered Parent projections in a Draft PR. Changes to the NGINX handoff still need an atomic, separately reviewed Parent update. Update generated compiler guides through `scripts/generate_compiler_guides.py`, not by editing its generated Markdown directly. Keep the independently protected NGINX broker on its own review path. Do not change environment variables to override the reviewed source identity.

## Rebuild and runtime acceptance

The ModSecurity cache identity includes its actual source commit, submodule status, build flags, toolchain and dependencies. Apache and NGINX connector identities depend on the ModSecurity build identity. Regression tests exercise these invalidation boundaries and the expected `libmodsecurity.so.3` alias layout using synthetic files; they do not prove binary ABI compatibility. An actual upgrade still requires matching headers/library/connector builds, upstream tests and real allow/block, request/response body, callback, logging, reload and shutdown checks. A future major version or SONAME is not automatically accepted.

## Evidence and local Python

Report each exact commit, command, exit status and skipped capability honestly. Privileged namespace tests must use a resolved interpreter in the existing jail runtime allowlist, not an external virtualenv alias. Resolving that alias does not permit mounting its writable parent or weakening the jail. Passing source or filesystem tests is not a native WAF or future-release compatibility claim. GitHub CI and Sonar must be checked on the final PR head before the PR is declared ready.
