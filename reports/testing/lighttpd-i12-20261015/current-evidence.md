# Current lighttpd I12 evidence

**Language:** English | [Deutsch](current-evidence.de.md)

This is the continuing acceptance record for [Draft PR #412](https://github.com/Easton97-Jens/ModSecurity-conector/pull/412). The original inventories remain immutable: Stock-Sidecar153, Patched-Native116 and diagnostic Stock-Native78; their original oracle inventories contain51,52 and23 expectations. A capture, a successful driver or a worker verdict does not qualify an original case.

## Qualification and current ledgers

`ci/runtime/lifecycle/i12/lighttpd/qualification.py` requires a separate Root review binding the exact packet and oracle proposal hashes, then invokes the existing shared oracle reconciliation and lifecycle validator. Each result retains immutable copies of the executed qualification sources. Dedicated configuration and pre-native rejection validators preserve their narrower scopes. A pre-native rejection requires another exact Root source/request approval; it creates no native transaction or body lifecycle.

`current_ledger.py` revalidates the physical proposals, reviewed derivatives and shared results before exporting separate route ledgers. Root-reviewed capture coverage can establish an actual HTTP/parser execution without assigning PASS or closing an oracle. Startup-only attempts do not count as HTTP requests. Copied process receipts do not count as new executions. Diagnostic full-case acceptance remains separate from mandatory body-lifecycle acceptance.

The independently re-evaluated checkpoint08 contains168 currently accepted originals: Stock60, Patched72 and diagnostic36. Diagnostic acceptance comprises28 host controls and eight configuration parser controls; it grants no body-lifecycle acceptance. The [current summary](current-20261020/summary.json) and separate route ledgers retain every original ID, its measurements, qualification scope and unresolved reasons.

| Route | Original IDs | Actual HTTP/parser executions | Current PASS | Currently unqualified IDs | Original oracles | Still open oracles |
| --- | --- | --- | --- | --- | --- | --- |
| [Stock-Sidecar](current-20261020/lighttpd-stock-sidecar.json) | 153 | 128 / 0 | 60 | 92 | 51 | 17 |
| [Patched-Native](current-20261020/lighttpd-patched-native.json) | 116 | 112 / 0 | 72 | 44 | 52 | 13 |
| [Stock-Native diagnostic](current-20261020/lighttpd-stock-native-control.json) | 78 | 69 / 8 | 36 | 42 | 23 | 19 |

The unqualified counts use the ledger's union of historical and current qualifications, so they are not simply original IDs minus current PASS. Newly qualified original IDs are59/70/35; newly resolved original oracles are32/37/4, respectively. Original oracle counts and historical results remain unchanged. The full347-row Root-reviewed execution index has317 actual waited HTTP/parser results; its capture-only rows grant no additional PASS. Remaining rows comprise13 startup-only attempts and17 cases without execution. Current-source qualification and execution coverage are separate claims.

The export binds integration head `eef8c1b432c0ce372c551a32fa6977cf4633b6c3`, qualification-era base #410 `a62296fb57263f9be18c6ac879e36e0ab2a9935c` and product #382 `12cc380c3749fd76c246c05ce479f51446127880`. These are the revisions at export, before publication of later lighttpd producer changes. The final evidence release binds published producer/source head `31a2c5bc717c08b3a64c7f61b152aae897f5361b`; its current #410 base at publication was `afaf6305bd55646073c3b40632b52fc4e5edf714`. Later base integration and producer hardening grant no new host qualification. Exact-source Sonar passed with strict zero findings and duplication.

## Downloadable raw checkpoint

The [final evidence prerelease](https://github.com/Easton97-Jens/ModSecurity-conector/releases/tag/evidence-i12-lighttpd-pr412-20261022-final) contains the content-addressed raw archive, manifest, exact selection, publication review, checksums and standalone verifier for the168 current qualifications and all347 separate ledger rows. It targets published source head `31a2c5bc717c08b3a64c7f61b152aae897f5361b`. The earlier [checkpoint03 prerelease](https://github.com/Easton97-Jens/ModSecurity-conector/releases/tag/evidence-i12-lighttpd-pr412-20261018-checkpoint03) remains the historical89-qualification/RST snapshot and is not treated as current evidence.

| Object | SHA256 | Bytes |
| --- | --- | ---: |
| `lighttpd-i12-raw.tar.gz` | `0790569c37a4f0767dd69c901c5dc2db5597819f2d517c3ba43df8be66e21ad0` | 54,685,172 |
| `manifest.json` | `9dc68be73105af0ef1f17b12dd95f4a587e11d9bcef0d915ec91f5c7f998f0c9` | 2,852,551 |
| `selection-checkpoint17-final.json` | `6c65f83695e32d9d387e8136a72917018ddb08678703dbe9a423f9a86fc6a323` | 27,022 |

All six release assets were downloaded afresh from GitHub. `SHA256SUMS-checkpoint17-final` accepted the five listed payload assets before the downloaded verifier accepted4962 unique content objects representing7649 physical paths and543,842,840 unique bytes, with zero unavailable selected references. The downloaded external manifest matched the archive's embedded manifest byte for byte. Three mixed/foreign references are explicitly out of scope and five historical producer references resolve only to exact digest-and-size-matched immutable snapshots; the publication review enumerates both classes, and neither grants qualification credit. All47 tracked current capture sources match the bound Git head. Archive paths are content hashes; original absolute producer paths are manifest metadata. Verification does not extract files. Reproduce after downloading the assets:

```sh
rtk proxy sha256sum -c SHA256SUMS-checkpoint17-final
rtk proxy python3 verify-lighttpd-i12.py \
  --archive lighttpd-i12-raw.tar.gz \
  --expected-sha256 0790569c37a4f0767dd69c901c5dc2db5597819f2d517c3ba43df8be66e21ad0
```

`artifact.py` packages only an explicit hash-bound selection and its selected JSON reference closure inside recorded lighttpd roots, with bounded files, entries and total bytes. Opaque attestations remain unexpanded; mixed or foreign references are recorded as out of scope. An exact Root-selected immutable snapshot may resolve a missing or drifted original path only when digest and size match, and every such resolution is recorded. The packer rejects missing unapproved references, unapproved changed bytes, symlinks, shared hardlinks, unsafe archive members and altered objects. Packaging establishes availability and integrity; it grants no case qualification. Task artifacts contain synthetic fixture traffic and explicitly selected sources, rather than credential or full environment files. A bounded high-confidence credential-pattern check covered4963 archive members and546,695,391 uncompressed bytes without a finding; Gitleaks was unavailable and is not reported as passed.

## Route and production boundaries

Stock retains private0700 spool directories,0600 files, shared256MiB technical capacity and64MiB reserve. Physical exhaustion is a technical503 with native body processing absent; release/readmission and the unchanged reserve primitive are measured independently. Off/Safe/Strict/All delivered configurations remain separate actual executions.

Patched host evidence uses pinned lighttpd1.4.85, measured module/core/SDK images and actual hooks. Six confirmed delivery/EOS/cleanup/response-hook fixes were committed on existing#382 and normally integrated through#410. The sixth fix, `c523dce9966b47bc8be6efe39ee49f2d88de3397`, corrects response inspection bypass through upstream splice/sendfile. The genuine UID65534 retest measures1,050,657 response bytes at native/host/client/backend layers, one EOS, physical logging/free/destroy and successful neighbor requests. Five fresh P3 rejects deliver actual403 with158 response-body bytes; nine affected response cases were retaken. Earlier affected response qualifications were superseded. In the Reject scope, `runtime_finish=0` and `common_finish=2`; logging/free/destroy are each1. These distinct counters are retained rather than described as one finish. A short write does not prove EAGAIN; local abort intent does not prove a received peer RST. Strict client abort capability is not invented.

Stock-Native remains a diagnostic header/configuration control. Its three exact malformed-CL host-before-native rejections are checked in a dedicated scope with actual400, zero main native/backend activity, positive controls, private log/event windows and cleanup. It provides no native body streaming substitute.

The historical unchanged merged revision `5e3b95864403dc642f77f01ef963d8c459b08628` reproduces the original Stock RST test failure with an empty physical event file. The earlier exact September pre-merge object is unavailable; these revisions are not equated. Root and actual UID65534 runs remain distinct. No namespace, AppArmor, UID, symlink or read-only boundary was relaxed.

## Verification and remaining work

The focused lighttpd I12 producer/adapter/current-ledger/artifact suite ran118 tests:117 passed and one ownership test skipped honestly because this host returned `EINVAL` for `chown(..., 65534)`; no boundary was relaxed. An independent replay of all36 selected diagnostic qualifications found15 rule-bearing normal host cases with exact physical main-transaction events and no audit fallback. The integrated shared reconciliation/lifecycle/report controls passed82 tests. Product precommit-response/EOS/Stock/native/spool/sink/cleanup regression ran214 tests:201 passed and13 explicitly skipped for namespace/UID restrictions; matching genuine nonroot captures are separate evidence. The canonical native suite passed15/17; its two inherited Traefik `sockaddr_un` fixture-path failures passed2/2 unchanged with a private short external path. On evidence source head `31a2c5bc717c08b3a64c7f61b152aae897f5361b`, Sonar reports Quality Gate OK, zero active or accepted issues, zero hotspots, Security A and zero new duplicated blocks, lines or density.

Current per-ID route ledgers, the regression-bound large-response correction/retest and the actually downloaded final raw archive are present. The current bilingual documentation, repository path/link and Change Record structure checks pass. The required lighttpd and Sonar checks pass on the evidence source head. Required HAProxy CI inherited from the current base remains failed because its fake SDK header does not declare `msc_get_request_body_length`; the scoped lighttpd delivery does not modify HAProxy or shared runtime ownership. Unaccepted originals and source-specific unresolved oracle decisions remain open. Local Gitleaks evidence remains unavailable; the bounded credential-pattern check does not replace it. Historical evidence and baseline exports are retained. Full connector acceptance is not claimed.
