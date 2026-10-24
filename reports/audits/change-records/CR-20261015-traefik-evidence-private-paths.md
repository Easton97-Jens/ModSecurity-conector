# Change Record: CR-20261015-traefik-evidence-private-paths

**Language:** English | [Deutsch](CR-20261015-traefik-evidence-private-paths.de.md)

Producer boundary repair with immutable historical evidence.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261015-traefik-evidence-private-paths |
| Date (UTC) | 2026-10-15 |
| Base revision | `107e09a657468b815c45af81929e00f33d8e6606` |

## Motivation and problem statement

The previous PR413 host producers admitted overly broad destinations and exposed maintainability findings. Repairs must preserve actual runner paths and every historical requirement and expectation.

## Acceptance criteria

Bound private destination, relay target and configuration inputs; preserve original280 IDs,124 oracle membership, all107 provenance fingerprints and the historical ledger exactly. Admit the real random private engine-socket child and effective configuration path. Reject tampering and unsafe paths.

## Implementation decision and rationale

Keep provenance as explicit path/SHA records, reconstruct the original mapping before the existing immutable digest check, and factor code without weakening qualification. Require explicit CODEX_TEMP_ROOT and owned physical ancestry. Restrict authorization relay to loopback /authorize, retain32768 authorization-response capacity and actual opcode10 ACK fault. Engine sockets retain the runner-created mode0700 child; configuration uses /task/runtime/effective-config/traefik-forwardauth-dynamic.yaml.

## Changed files

Traefik-only inventory, native/auth producer Python files and their four EN/DE READMEs; i12_ledger.py; three existing I12 test modules and new test_traefik_i12_quality_controls.py; this record. Shared generators, original matrix, product code and Framework/MRTS gitlinks are unchanged by this commit.

## Commands executed

Root ran rtk proxy env TMPDIR=<short-private-external> CODEX_TEMP_ROOT=<configured-external> /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_traefik_i12_ledger tests.test_traefik_i12_auth tests.test_traefik_i12_native_measurements tests.test_traefik_i12_quality_controls:40 tests passed. Inventory and historical-ledger equivalence controls passed. git diff --check passed. Exact receipts are under external run i12-traefik-acceptance-20261015/quality and checks/quality-root-i12.json.

## Security impact

No security gate, admission, namespace, UID, capability, symlink or read-only boundary is weakened. New path checks enforce physical owned directories and bounded regular inputs. No issue acceptance, suppression or scanner exclusion is introduced.

## Runtime evidence

These are producer and qualification regression checks. Independent review found and corrected two repair regressions before delivery: legitimate random-child UDS rejection and a wrong fixed effective-config path. Actual runner allocation/socket and generated-driver positive controls now cover those ABIs. No new host execution or original-ID promotion is claimed.

## Known limitations

Complete host acceptance and final hosted Sonar results remain requirements of continuing PR413 work. Local source remediation does not establish a green hosted gate.

## Remaining risks

New acceptance producers must continue to consume current capture/observer contracts and produce physical per-case evidence. The immutable historical ledger stays separate from current revision qualification.

## Checks not run and rationale

Full EN/DE/link make initially failed because the isolated checkout lacked22 Framework link targets; that output is retained. Focused checks on all four changed READMEs passed. Complete checks use the approved private read-only Framework view; no submodule write or gitlink update is needed.

## Final diff and review status

Independent read-only review verified lossless inventory normalization and historical ledger equivalence. Root reviewed the final repair and reran its40 tests. Publication uses normal commits; no automatic merge or history rewrite.
