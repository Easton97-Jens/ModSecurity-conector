# Change Record: CR-20261008-hostruntime-binary-artifact-hash

**Language:** English | [Deutsch](CR-20261008-hostruntime-binary-artifact-hash.de.md)


## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-hostruntime-binary-artifact-hash |
| Date (UTC) | 2026-10-08 |
| Base revision | `810a9b5621b04c79d58b1429c3182f1668e672c9` |

## Motivation and problem statement

The native lifecycle failed after canonical finalization because `artifact_sha256()` decoded a retained configtest ELF as UTF-8. The caller is `run-no-crs-baseline.sh`; the operation requires byte hashing, not text analysis.

## Acceptance criteria

The actual Writer accepts non-UTF-8 artifacts with exact byte digests. Changed/missing artifacts, invalid JSON and unsafe paths/types remain rejected without successful output.

## Implementation decision and rationale

Stream original bytes in 1-MiB chunks through the existing validated path, parent descriptor, `O_NOFOLLOW` and regular-file checks. Keep JSON decoding and manifest digest comparisons unchanged. This also preserves CRLF bytes instead of normalizing line endings.

## Changed files

`ci/runtime/lifecycle/write-hostruntime-record.py`, `tests/test_hostruntime_record.py` and this EN/DE Change Record pair. No Framework/MRTS, Gitlink, dependency or protocol changes.

## Commands executed

`rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_hostruntime_record tests.test_runtime_path_utils`: Coordinator VM-host run, 33 tests PASS, 0 SKIP, exit 0. The expanded suite additionally includes `tests.test_runtime_artifact_utils tests.test_runtime_path_security tests.test_runtime_path_policy`: 82 tests PASS, 0 SKIP, exit 0. Dynamic old-code entrypoint regression: 1 test fails at Unicode decoding, exit 1. New cases cover binary/CRLF/multi-chunk digests, byte changes, missing artifacts and JSON format. `git diff --check` passed.

## Security impact

Existing containment, directory authority, descriptors, no-follow, regular-file, manifest-digest and publication preflight controls are preserved. Streaming bounds working memory, not total file size. The old reader had no independent leaf-owner/hardlink or inode/mtime attestation; no such guarantee is invented.

## Runtime evidence

Isolated historical-artifact Writer repro, NOT fresh E2E: real NGINX/module/library digests verified; Writer exit 0; tampered/missing controls exit 2 without record/summary. Source result/manifest unchanged and copied non-PASS status not promoted. Receipt: `/var/tmp/codex/ModSecurity-conector/analysis/nginx1316-followup-20261008T003355Z/writer-real-repro/writer-repro-receipt.json`.

## Known limitations

Only artifact hashing changes. This does not repair standard H1 forwarding, schedule missing Required scenarios or create Allow events.

## Remaining risks

Complete canonical coverage and independent Protected trust remain separate obligations. Existing total-file-size policy is unchanged.

## Checks not run and rationale

Fresh standard local E2E, full lint and current-head CI/Sonar follow the separate H1/test fixes. Ruff is absent from the Parent environment; no package installation attempted.

## Final diff and review status

Two-file source/test diff inspected with independent static security review. No unsafe decoding fallback, suppression, synthetic runtime evidence or unrelated changes. Atomic follow-up commit planned; no merge, force-push or protected dispatch.
