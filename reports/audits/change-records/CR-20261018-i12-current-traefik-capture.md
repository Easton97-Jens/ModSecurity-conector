# Change Record: CR-20261018-i12-current-traefik-capture

**Language:** English | [Deutsch](CR-20261018-i12-current-traefik-capture.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-i12-current-traefik-capture |
| Date (UTC) | 2026-10-18 |
| Base revision | `a311c725c44a7a4da95acb1a4818f66bd56c462a` |

## Motivation and problem statement

Current product integration invalidated three historical repository object references and the exact historical observer input pins rejected complete current Traefik exports.

## Acceptance criteria

All historical source/result identities remain exact; only reviewed current observer bases are additionally admitted after complete v2 validation; negative controls reject legacy alternate bases and unrelated tampering.

## Implementation decision and rationale

Freeze the three authenticated historical byte streams as lossless text_lines. Keep historical pins and result bytes. Add exact current_before_sha256 alternatives only to the two observer targets in each existing Traefik profile, and record actual input hashes in the receipt.

## Changed files

`ci/runtime/lifecycle/i12/capture_sources.py`, `manifest.json`, `test_capture_sources.py`, `README.md`, `README.de.md`, three `objects/*.lines.json`, and this Change Record pair.

## Commands executed

`rtk proxy python3 -B ci/runtime/lifecycle/i12/capture_sources.py verify`: passed, 155 objects and 9 profiles. `rtk proxy python3 -B -m unittest discover -s ci/runtime/lifecycle/i12 -p test_capture_sources.py -q`: passed, 51 tests.

## Security impact

No UID, namespace, peer, admission, filesystem or hash checks are weakened. The current alternative is manifest-pinned and requires complete inventory validation before any capture write.

## Runtime evidence

No host was started. Source validation proves source application only.

## Known limitations

The retained instrumented result bytes have their historical observer ABI. Each fresh build must bind and validate its actual SDK and loaded instrumentation.

## Remaining risks

A valid source application cannot establish host lifecycle qualification. Fresh integrated builds and observations remain the owning task responsibility.

## Checks not run and rationale

Host execution and hosted CI/Sonar were not run by this source-only subtask; they follow integration.

## Final diff and review status

Focused source tests passed. Root integration and independent review remain pending; unrelated gate edits in the shared worktree were preserved.

During normal integration of parallel commit `61e45cf6dd211f21835709a014fe6884d4bcda62`, Root verified that its three HAProxy frozen objects reproduce exactly the same original byte hashes. The merged manifest uses those published `objects/text/` paths and removes this task's duplicate files; all original object IDs, source bytes, capture results and current Traefik base guards remain unchanged. The original commits remain in history. The parallel lighttpd anchors and exact parser-exit repair are preserved.
