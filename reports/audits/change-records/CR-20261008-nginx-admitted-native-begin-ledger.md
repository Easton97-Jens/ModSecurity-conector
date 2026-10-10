# Change Record: CR-20261008-nginx-admitted-native-begin-ledger

**Language:** English | [Deutsch](CR-20261008-nginx-admitted-native-begin-ledger.de.md)

Attempt-scoped BEGIN allocation evidence, no native runtime promotion.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-admitted-native-begin-ledger |
| Date (UTC) | 2026-10-08 |
| Base revision | `20478534e305a35c7f92fd80e8303a92121a5a3a` |

## Motivation and problem statement

The scoped native allocation fixture previously returned NULL silently and had no inherited evidence-descriptor guard. The driver did not retain native BEGIN observations and excluded ordinary/fault/finish events from its full Source projection.

## Acceptance criteria

One actual own-child exact-TX injected NULL ledger before return, private Root-owned initial-empty descriptor guard, wrong-TX/no-FD/invalid-FD controls, full original event retention and raw SHA. No native NGINX runtime or product module build; bounded C17 fixture verification explicitly allowed.

## Implementation decision and rationale

Root constructor requires exact mode/TX and inherited MSCONNECTOR_OWNED_BEGIN_FD decimal >=3, writable regular root-owned private0600/single-link/empty. The actual nobody child of that master writes one row before returning NULL: native_operation msc_new_transaction_with_id, observed_return null, actual worker_pid/worker_uid65534/master_pid, transaction_id, injected true. Missing/invalid descriptors do not arm; failed writes do not inject. No phases/rules/events are fabricated. Driver preopens the ledger, passes the existing descriptor tuple only to the actual master, fsyncs and closes in nested finally, captures original native_begin and native_begin_sha256, and retains every original phase1 event for all sequence cases.

## Changed files

Only owned tests/fixtures/nginx_transaction_fault.c and ci/runtime/lifecycle/run-nginx-lifecycle-sequences.py, new tests/test_nginx_native_begin_ledger.py and test_nginx_begin_driver_evidence.py, and this paired record. Root approved normal cherry-pick materialization of seven previous sequence-driver commits; its paired record conflict retained both old transport/finish facts. No new source/Gitlink/Framework/MRTS/shared collector edits.

## Commands executed

RTK-wrapped Parent unittest commands use `${PARENT_PYTHON}`, PYTHONNOUSERSITE=1/PYTHONDONTWRITEBYTECODE=1. `-m unittest discover -s tests -p test_nginx_native_begin_ledger.py`: sandbox exit1 from setuid restriction (not product RED); escalated old-fixture exit1/ten targeted failures; changed fixture exit0/three tests, thirteen bounded fake-engine/harness invocations. Each compiled cc -std=c17 -Wall -Wextra -Werror (attempt-only shared fixture/stub/harness). `-p test_nginx_begin_driver_evidence.py`: three tests0; `-p test_nginx_sequence_driver.py`: nine0; `-p test_nginx_sequence*.py`: fifteen0; dispatcher regression eight0. Scaffold initially rejected abbreviated base SHA exit2, then full-SHA create0. Final AST/record/pair/diff checks in handoff.

## Security impact

Closed own root master/nobody child/transaction boundary; no global failure or foreign-process mutation. Descriptor guards are strengthened, not relaxed. Root-only inherited capability retains metadata with no native payload, phase or rule premise. Negative fixture controls cover identity, missing/invalid descriptor, permissions, link count, initial contents, readonly access, UID and parent scope.

## Runtime evidence

No native NGINX execution or module build. The C17 harness calls the actual attempt interposer through a fake original Engine symbol, forks actual credential-scoped children, and validates its ledger; this is fixture behavior only, not Engine/host/Common integration evidence. Root module admission/error/cleanup changes were read-only context and remain separately authenticated.

## Known limitations

Root must rebuild the actual selected fault library and provide its immutable digest authority. C source hash is not compiled-library proof. The child credential fixture requires Root/compiler and permission to drop subprocess credentials; strict environment failures are not reclassified as green.

## Remaining risks

Actual admitted Common-before-native-allocation error and cleanup(native0), plus full Source phase1 rows, require Root's new module and reader validation at runtime. D agreed exact BEGIN receipt fields/native_begin_sha256 and remains reader owner. All previous native runtime gaps remain open.

## Checks not run and rationale

No native runtime/full E2E/product build, Framework/MRTS mutation or scanner/publish/push. Parent Ruff previously unavailable; no install. Root owns final integrated source/library/module/reader checks.

## Final diff and review status

Only new BEGIN ledger and full Source event capture changes reviewed against the exact delegated boundaries. Ordinary WRITE/FINISH/BUDGET modes and host FD guards remain unchanged or receive guaranteed close-on-fsync-error cleanup. No runtime promotion or central validation relaxation.
