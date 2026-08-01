# Finding archive / Finding-Archiv

This user-directed local archive preserves completed finding triplets without
deleting evidence. `.codex/findings/` remains the active unresolved and
revalidation store; this directory is a non-active historical store. It also
contains the current user's test-only, no-release archive of `fixed` records
whose release-blocker flags remain true, plus explicitly accepted local
`accepted_risk` records. No `archived` lifecycle state is invented: each record
retains the evidence-supported status it had when it was moved.

Dieses nutzerbeauftragte lokale Archiv bewahrt vollständige Finding-Tripel,
ohne Evidence zu löschen. `.codex/findings/` bleibt der aktive Bestand für
offene Arbeit und Neubewertung; dieses Verzeichnis ist ein nicht aktiver
historischer Bestand. Es enthält außerdem das vom aktuellen Nutzer gewählte
Test-only-/No-Release-Archiv von als `fixed` markierten Records, deren Release-Blocker-Flags
weiterhin `true` bleiben. Es wird kein Lifecycle-Status `archived` erfunden:
Jeder Record behält beim Verschieben seinen evidence-gestützten Status.

## Archive review / Archivprüfung

### 2026-08-01 strict active-finding reconciliation / Strenger Active-Finding-Abgleich 2026-08-01

Seven additional complete triplets were moved losslessly after a fresh
per-finding review. Each is `closed`, has a canonical Parent PR and merge
commit reachable from current `origin/master`
`59aba762f2d852fd917079ca8519e4ea7f49169c`, and has current source,
scanner, workflow, or focused-control evidence. No active record was moved
solely because a branch, commit, or closed PR existed. The current archive
therefore contains 107 canonical triplets; the corresponding seven IDs are
absent from the active index and active backlog record set.

Sieben zusätzliche vollständige Tripel wurden nach einer frischen Prüfung pro
Finding verlustfrei verschoben. Jedes ist `closed`, besitzt einen kanonischen
Parent-PR und einen vom aktuellen `origin/master`
`59aba762f2d852fd917079ca8519e4ea7f49169c` erreichbaren Merge-Commit sowie
aktuelle Source-, Scanner-, Workflow- oder fokussierte Control-Evidence. Kein
aktives Finding wurde allein wegen eines Branches, Commits oder geschlossenen
PRs verschoben. Das aktuelle Archiv enthält damit 107 kanonische Tripel; die
sieben entsprechenden IDs fehlen im aktiven Index und im aktiven Backlog-
Record-Set.

| ID | Status at move / Status beim Move | Parent PR and merge / Parent-PR und Merge |
| --- | --- | --- |
| `FND-PARENT-0029` | `closed` | [#56](https://github.com/Easton97-Jens/ModSecurity-conector/pull/56) · `a73c33529f4b900e0e5722f6c8eae2ae47e41c1f` |
| `FND-PARENT-0039` | `closed` | [#65](https://github.com/Easton97-Jens/ModSecurity-conector/pull/65) · `1fa024ca6ec97023ea5b6f7dff5215e43f10b74c` |
| `FND-PARENT-0047` | `closed` | [#90](https://github.com/Easton97-Jens/ModSecurity-conector/pull/90) · `ad953cdcbc8c05ede519661ca56c03cf7b1ac7f3` |
| `FND-PARENT-0048` | `closed` | [#92](https://github.com/Easton97-Jens/ModSecurity-conector/pull/92) · `95fb4917b63dd8a5c5973bb49fd955bd3d2b29a3` |
| `FND-PARENT-0074` | `closed` | [#213](https://github.com/Easton97-Jens/ModSecurity-conector/pull/213) · `f335965fd5f7b9640fc39a1dd7873d46d7c989c5` |
| `FND-SONAR-0020` | `closed` | [#197](https://github.com/Easton97-Jens/ModSecurity-conector/pull/197) · `caddd86d1eede95de53aa1bc971dd26d875df21c` |
| `FND-SONAR-0021` | `closed` | [#177](https://github.com/Easton97-Jens/ModSecurity-conector/pull/177) · `a1c8394e528bfcd7b54bc3e0aac4cdf3430d1345` |

- Date / Datum: `2026-07-26`
- Scope / Geltungsbereich: one hundred records: the previous ninety-two plus
  eight current-user-selected Framework records. `FND-HOST-0001` and
  `FND-HOST-0005` retain `verified`; `FND-HOST-0002` and `FND-HOST-0004`
  retain the evidence-backed `not_applicable` disposition for the current local
  test scope. The latter is not a technical Python or HTTP/3 closure, and none
  of the four records authorizes release readiness. The accepted-risk entries
  elsewhere in this archive remain local archive dispositions only, not
  technical closures or release approvals. `FND-HOST-0003`,
  `FND-HOST-0006`, every active `blocked`/missing-evidence record, and every
  still-active release-blocking record remain under `.codex/findings/`.
- Integrity / Integrität: every retained file is regular, has no symlink or
  special-file indirection, and is listed in [SHA256SUMS](./SHA256SUMS).
- Active summaries / Aktive Übersichten: all one hundred records are absent
  from the active index and active backlog records. The five accepted-risk
  GitHub records and the three Parent Sonar records are also absent from active
  roadmap phase membership.
  Historical ID references remain intact. The twenty-nine test-only records
  retain `fixed` and their release-blocker flags in their archived JSON and
  reader records; the nine accepted-risk records retain their exact residual
  risks and are not represented as passing or closed.

## Archived records / Archivierte Records

### Current-user Framework verified and accepted-risk archive / Aktuelles Nutzerarchiv verifizierter und risikoakzeptierter Framework-Records

| ID | Status at move / Status beim Move | Record / Record |
| --- | --- | --- |
| `FND-FRAMEWORK-0013` | `verified` | [English](./FND-FRAMEWORK-0013/finding.md) · [Deutsch](./FND-FRAMEWORK-0013/finding.de.md) · [JSON](./FND-FRAMEWORK-0013/finding.json) |
| `FND-FRAMEWORK-0018` | `verified` | [English](./FND-FRAMEWORK-0018/finding.md) · [Deutsch](./FND-FRAMEWORK-0018/finding.de.md) · [JSON](./FND-FRAMEWORK-0018/finding.json) |
| `FND-FRAMEWORK-0019` | `verified` | [English](./FND-FRAMEWORK-0019/finding.md) · [Deutsch](./FND-FRAMEWORK-0019/finding.de.md) · [JSON](./FND-FRAMEWORK-0019/finding.json) |
| `FND-FRAMEWORK-0025` | `accepted_risk` (local test-only archive) | [English](./FND-FRAMEWORK-0025/finding.md) · [Deutsch](./FND-FRAMEWORK-0025/finding.de.md) · [JSON](./FND-FRAMEWORK-0025/finding.json) |
| `FND-FRAMEWORK-0029` | `accepted_risk` (local test-only archive) | [English](./FND-FRAMEWORK-0029/finding.md) · [Deutsch](./FND-FRAMEWORK-0029/finding.de.md) · [JSON](./FND-FRAMEWORK-0029/finding.json) |
| `FND-FRAMEWORK-0031` | `verified`; release blocker retained | [English](./FND-FRAMEWORK-0031/finding.md) · [Deutsch](./FND-FRAMEWORK-0031/finding.de.md) · [JSON](./FND-FRAMEWORK-0031/finding.json) |
| `FND-FRAMEWORK-0036` | `verified`; release blocker retained | [English](./FND-FRAMEWORK-0036/finding.md) · [Deutsch](./FND-FRAMEWORK-0036/finding.de.md) · [JSON](./FND-FRAMEWORK-0036/finding.json) |
| `FND-FRAMEWORK-0054` | `verified`; release blocker retained | [English](./FND-FRAMEWORK-0054/finding.md) · [Deutsch](./FND-FRAMEWORK-0054/finding.de.md) · [JSON](./FND-FRAMEWORK-0054/finding.json) |

The current user selected the six verified records for local archival. The three
verified release blockers retain their flags and must be restored and
revalidated before any production, publication, or release decision.
`FND-FRAMEWORK-0025` and `FND-FRAMEWORK-0029` are accepted only for this local
test-only archive: neither is fixed or technically closed. The external helper
may still omit `ci`/`tests` files, and the Codex Cloud inventory remains
unavailable; GitHub CodeQL is not a Cloud substitute. No fixture digest,
release tag, or other substitute is accepted for a genuine normal NGINX
upstream digest. Decision receipt:
`.codex/runs/20260726-framework-archive-current-dispositions/evidence/archive-decision.md`,
SHA-256 `4f314bd2ca703eb0509d71546648bfb0367c3d35f2ff1a1e13c56b7f9bedcc30`.

Der aktuelle Nutzer wählte die sechs verifizierten Records für die lokale
Archivierung. Die drei verifizierten Release-Blocker behalten ihre Flags und
müssen vor jeder Produktions-, Veröffentlichungs- oder Release-Entscheidung
wiederhergestellt und neu validiert werden. `FND-FRAMEWORK-0025` und
`FND-FRAMEWORK-0029` sind nur für dieses lokale test-only Archiv akzeptiert:
Keiner ist fixed oder technisch geschlossen. Der externe Helper kann weiterhin
`ci`-/`tests`-Dateien auslassen, und das Codex-Cloud-Inventar bleibt nicht
verfügbar; GitHub CodeQL ist kein Cloud-Ersatz. Kein Fixture-Digest,
Release-Tag oder anderer Ersatz wird als Evidence für einen echten normalen
NGINX-Upstream-Digest akzeptiert. Decision-Receipt:
`.codex/runs/20260726-framework-archive-current-dispositions/evidence/archive-decision.md`,
SHA-256 `4f314bd2ca703eb0509d71546648bfb0367c3d35f2ff1a1e13c56b7f9bedcc30`.

### Current-user Parent Sonar archive disposition / Aktuelle Nutzer-Parent-Sonar-Archiv-Disposition

| ID | Status at move / Status beim Move | Record / Record |
| --- | --- | --- |
| `FND-SONAR-0010` | `verified` | [English](./FND-SONAR-0010/finding.md) · [Deutsch](./FND-SONAR-0010/finding.de.md) · [JSON](./FND-SONAR-0010/finding.json) |
| `FND-SONAR-0013` | `accepted_risk` (local archive only) | [English](./FND-SONAR-0013/finding.md) · [Deutsch](./FND-SONAR-0013/finding.de.md) · [JSON](./FND-SONAR-0013/finding.json) |
| `FND-SONAR-0014` | `accepted_risk` (local archive only) | [English](./FND-SONAR-0014/finding.md) · [Deutsch](./FND-SONAR-0014/finding.de.md) · [JSON](./FND-SONAR-0014/finding.json) |

The current user selected exactly this Parent Sonar subset after the
current-master/Sonar reconciliation. `FND-SONAR-0010` retains its
evidence-backed `verified` status. `FND-SONAR-0013` is accepted only for this
local archive while its hosted per-rule evidence, real CRS/libmodsecurity/
connector smoke, broader filesystem/identity models, and current scanner
signals remain unresolved; its release-blocker flag remains effective.
`FND-SONAR-0014` is accepted only for this local archive while the retained
current per-rule S1192/S3415 SonarQube receipt remains absent. Neither
accepted-risk record claims a fix, technical closure, passing Quality Gate,
production safety, publication, or release readiness. Restore the complete
triplet and rerun its original criteria before any such decision. Decision
evidence: external task-owned run
`20260726T182851Z-user-selected-parent-sonar-archive`, SHA-256
`d5dc1ed08dfca22b841c02eee45e0459665f026924ff531f158d1e5dd0145cdf`.

Der aktuelle Nutzer wählte exakt diese Parent-Sonar-Teilmenge nach dem
Current-Master-/Sonar-Abgleich. `FND-SONAR-0010` behält seinen evidence-
gestützten Status `verified`. `FND-SONAR-0013` ist nur für dieses lokale Archiv
akzeptiert, während Hosted-Per-Rule-Evidence, echter CRS-/libmodsecurity- /
Connector-Smoke, breitere Filesystem-/Identity-Modelle und aktuelle
Scanner-Signale ungelöst bleiben; sein Release-Blocker-Flag bleibt wirksam.
`FND-SONAR-0014` ist nur für dieses lokale Archiv akzeptiert, während der
aufbewahrte aktuelle Per-Rule-S1192/S3415-SonarQube-Receipt fehlt. Keiner der
beiden `accepted_risk`-Records behauptet einen Fix, technischen Abschluss,
ein bestandenes Quality Gate, Produktionssicherheit, Veröffentlichung oder
Release-Reife. Vor jeder solchen Entscheidung das vollständige Tripel
wiederherstellen und seine ursprünglichen Kriterien erneut ausführen.
Entscheidungs-Evidence: externer task-eigener Run
`20260726T182851Z-user-selected-parent-sonar-archive`, SHA-256
`d5dc1ed08dfca22b841c02eee45e0459665f026924ff531f158d1e5dd0145cdf`.

### Current-user FND-HOST archive and scope disposition / Aktuelles Nutzerarchiv und Scope-Disposition für FND-HOST

| ID | Status at move / Status beim Move | Record / Record |
| --- | --- | --- |
| `FND-HOST-0001` | `verified` | [English](./FND-HOST-0001/finding.md) · [Deutsch](./FND-HOST-0001/finding.de.md) · [JSON](./FND-HOST-0001/finding.json) |
| `FND-HOST-0002` | `not_applicable` | [English](./FND-HOST-0002/finding.md) · [Deutsch](./FND-HOST-0002/finding.de.md) · [JSON](./FND-HOST-0002/finding.json) |
| `FND-HOST-0004` | `not_applicable` | [English](./FND-HOST-0004/finding.md) · [Deutsch](./FND-HOST-0004/finding.de.md) · [JSON](./FND-HOST-0004/finding.json) |
| `FND-HOST-0005` | `verified` | [English](./FND-HOST-0005/finding.md) · [Deutsch](./FND-HOST-0005/finding.de.md) · [JSON](./FND-HOST-0005/finding.json) |

The current user selected this exact FND-HOST subset for local archival.
`FND-HOST-0001` and `FND-HOST-0005` retain their fully evidenced `verified`
status. `FND-HOST-0002` preserves the fact that the host/local venv is behind
the declared Python lane and native/optional tools are absent, but the current
user excludes exact local parity from the current scope. `FND-HOST-0004`
preserves the unavailable HTTP/3 client/harness condition, but the current
user excludes HTTP/3 from that scope. Neither `not_applicable` record claims a
local or hosted pass, installed tool, HTTP/3 implementation, or connector
validation. Restore the complete triplet and rerun its original acceptance
criteria before any local-parity, HTTP/3, production, publication, or release
reliance. Decision evidence: run
`20260726T180544Z-fnd-host-archive-20260726-8b20e52d`, SHA-256
`50f77adb2bfbe8dbea9341bb4012ed67acaa4bf43a540ef3268f7ef2121c666b`.

Der aktuelle Nutzer wählte diese exakte FND-HOST-Teilmenge für die lokale
Archivierung. `FND-HOST-0001` und `FND-HOST-0005` behalten ihren vollständig
belegten Status `verified`. `FND-HOST-0002` bewahrt den Umstand, dass
Host/lokale venv hinter der deklarierten Python-Lane liegen und
Native-/optionale Tools fehlen, aber der aktuelle Nutzer schließt exakte lokale
Parität aus dem aktuellen Scope aus. `FND-HOST-0004` bewahrt den nicht
verfügbaren HTTP/3-Client-/Harness-Zustand, aber der aktuelle Nutzer schließt
HTTP/3 aus diesem Scope aus. Keiner der `not_applicable` Records behauptet
einen lokalen oder gehosteten Pass, ein installiertes Tool, eine HTTP/3-
Implementierung oder Connector-Validierung. Vor jeder lokalen Paritäts-,
HTTP/3-, Produktions-, Veröffentlichungs- oder Release-Nutzung das vollständige
Tripel wiederherstellen und seine ursprünglichen Akzeptanzkriterien erneut
ausführen. Entscheidungs-Evidence: Run
`20260726T180544Z-fnd-host-archive-20260726-8b20e52d`, SHA-256
`50f77adb2bfbe8dbea9341bb4012ed67acaa4bf43a540ef3268f7ef2121c666b`.

### Current-user fixed non-blocking Framework addition / Aktuelle Nutzerergänzung fester nicht blockierender Framework-Findings

| ID | Status at move / Status beim Move | Record / Record |
| --- | --- | --- |
| `FND-FRAMEWORK-0003` | `fixed` | [English](./FND-FRAMEWORK-0003/finding.md) · [Deutsch](./FND-FRAMEWORK-0003/finding.de.md) · [JSON](./FND-FRAMEWORK-0003/finding.json) |
| `FND-FRAMEWORK-0005` | `fixed` | [English](./FND-FRAMEWORK-0005/finding.md) · [Deutsch](./FND-FRAMEWORK-0005/finding.de.md) · [JSON](./FND-FRAMEWORK-0005/finding.json) |
| `FND-FRAMEWORK-0006` | `fixed` | [English](./FND-FRAMEWORK-0006/finding.md) · [Deutsch](./FND-FRAMEWORK-0006/finding.de.md) · [JSON](./FND-FRAMEWORK-0006/finding.json) |
| `FND-FRAMEWORK-0012` | `fixed` | [English](./FND-FRAMEWORK-0012/finding.md) · [Deutsch](./FND-FRAMEWORK-0012/finding.de.md) · [JSON](./FND-FRAMEWORK-0012/finding.json) |
| `FND-FRAMEWORK-0014` | `fixed` | [English](./FND-FRAMEWORK-0014/finding.md) · [Deutsch](./FND-FRAMEWORK-0014/finding.de.md) · [JSON](./FND-FRAMEWORK-0014/finding.json) |
| `FND-FRAMEWORK-0015` | `fixed` | [English](./FND-FRAMEWORK-0015/finding.md) · [Deutsch](./FND-FRAMEWORK-0015/finding.de.md) · [JSON](./FND-FRAMEWORK-0015/finding.json) |
| `FND-FRAMEWORK-0016` | `fixed` | [English](./FND-FRAMEWORK-0016/finding.md) · [Deutsch](./FND-FRAMEWORK-0016/finding.de.md) · [JSON](./FND-FRAMEWORK-0016/finding.json) |
| `FND-FRAMEWORK-0023` | `fixed` | [English](./FND-FRAMEWORK-0023/finding.md) · [Deutsch](./FND-FRAMEWORK-0023/finding.de.md) · [JSON](./FND-FRAMEWORK-0023/finding.json) |
| `FND-FRAMEWORK-0024` | `fixed` | [English](./FND-FRAMEWORK-0024/finding.md) · [Deutsch](./FND-FRAMEWORK-0024/finding.de.md) · [JSON](./FND-FRAMEWORK-0024/finding.json) |
| `FND-FRAMEWORK-0033` | `fixed` | [English](./FND-FRAMEWORK-0033/finding.md) · [Deutsch](./FND-FRAMEWORK-0033/finding.de.md) · [JSON](./FND-FRAMEWORK-0033/finding.json) |
| `FND-FRAMEWORK-0055` | `fixed` | [English](./FND-FRAMEWORK-0055/finding.md) · [Deutsch](./FND-FRAMEWORK-0055/finding.de.md) · [JSON](./FND-FRAMEWORK-0055/finding.json) |

The current user selected this exact `fixed` / `release_blocker: false`
Framework subset for local archival. The move is lossless and does not convert
any finding to `verified` or `closed`, weaken a security control, or establish
release readiness. Before a future decision relies on one of these records as
current verification, restore the complete triplet to `.codex/findings/` and
revalidate it against its existing acceptance criteria.

Der aktuelle Nutzer wählte diese exakte Framework-Teilmenge mit `fixed` /
`release_blocker: false` für die lokale Archivierung. Der Move ist verlustfrei
und konvertiert kein Finding in `verified` oder `closed`, lockert keine
Security-Control und begründet keine Release-Readiness. Bevor sich eine spätere
Entscheidung auf einen dieser Records als aktuelle Verifikation stützt, ist das
vollständige Tripel nach `.codex/findings/` zurückzuverschieben und gegen seine
bestehenden Akzeptanzkriterien neu zu validieren.

### Framework PR #50/#51 resulting-master closure addition / Framework-PR-#50/#51-Resulting-Master-Abschluss-Ergänzung

| ID | Status at move / Status beim Move | Record / Record |
| --- | --- | --- |
| `FND-FRAMEWORK-0002` | `closed` | [English](./FND-FRAMEWORK-0002/finding.md) · [Deutsch](./FND-FRAMEWORK-0002/finding.de.md) · [JSON](./FND-FRAMEWORK-0002/finding.json) |
| `FND-FRAMEWORK-0011` | `closed` | [English](./FND-FRAMEWORK-0011/finding.md) · [Deutsch](./FND-FRAMEWORK-0011/finding.de.md) · [JSON](./FND-FRAMEWORK-0011/finding.json) |
| `FND-FRAMEWORK-0053` | `closed` | [English](./FND-FRAMEWORK-0053/finding.md) · [Deutsch](./FND-FRAMEWORK-0053/finding.de.md) · [JSON](./FND-FRAMEWORK-0053/finding.json) |
| `FND-FRAMEWORK-0056` | `closed` | [English](./FND-FRAMEWORK-0056/finding.md) · [Deutsch](./FND-FRAMEWORK-0056/finding.de.md) · [JSON](./FND-FRAMEWORK-0056/finding.json) |

These four records were closed only after the exact Framework resulting master
`de705a5efb872f95f010346fe2e6143c88876ad4`, its applicable successful push
workflows, PR #50/#51 SonarQube Cloud `OK`/zero-issue readback, and focused
original-condition plus legitimate-control regressions. Receipt SHA-256:
`519b89ef349a2d1a66b8cf78a5f0056f2df1909df2f386e5e67b7742bf277a2d`.
`FND-FRAMEWORK-0057` is not part of this addition: Parent has adopted the
Framework Gitlink, but its fresh Parent #74 producer and strict terminal-gate
evidence remains active.

### Framework PR #52 resulting-master closure addition / Framework-PR-#52-Resulting-Master-Abschluss-Ergänzung

| ID | Status at move / Status beim Move | Record / Record |
| --- | --- | --- |
| `FND-FRAMEWORK-0010` | `closed` | [English](./FND-FRAMEWORK-0010/finding.md) · [Deutsch](./FND-FRAMEWORK-0010/finding.de.md) · [JSON](./FND-FRAMEWORK-0010/finding.json) |

`FND-FRAMEWORK-0010` was closed only after Framework PR #52 merged normally at
`2026-07-26T17:35:13Z` as resulting master
`47e50e7bc43ba7a3b5bad1a9448111794f664cc0`. The reviewed PR-head tree equals
resulting master; the 11-test negative/legitimate control suite, the Framework
documentation aggregate, and all applicable master checks passed. Receipt
SHA-256: `cbf90db531a6e4eab99ae84de6ba1008a07d6644b9805dcae2745fc54ad2aee9`.
Parent source/Gitlink, Framework-to-MRTS Gitlink, and MRTS source were
unchanged.

### 2026-07-26 closure addition / Abschluss-Ergänzung 2026-07-26

| ID | Status at move / Status beim Move | Record / Record |
| --- | --- | --- |
| `FND-MRTS-0003` | `not_applicable` | [English](./FND-MRTS-0003/finding.md) · [Deutsch](./FND-MRTS-0003/finding.de.md) · [JSON](./FND-MRTS-0003/finding.json) |
| `FND-PARENT-0004` | `not_applicable` | [English](./FND-PARENT-0004/finding.md) · [Deutsch](./FND-PARENT-0004/finding.de.md) · [JSON](./FND-PARENT-0004/finding.json) |
| `FND-PARENT-0012` | `closed` | [English](./FND-PARENT-0012/finding.md) · [Deutsch](./FND-PARENT-0012/finding.de.md) · [JSON](./FND-PARENT-0012/finding.json) |
| `FND-PARENT-0018` | `closed` | [English](./FND-PARENT-0018/finding.md) · [Deutsch](./FND-PARENT-0018/finding.de.md) · [JSON](./FND-PARENT-0018/finding.json) |
| `FND-PARENT-0022` | `closed` | [English](./FND-PARENT-0022/finding.md) · [Deutsch](./FND-PARENT-0022/finding.de.md) · [JSON](./FND-PARENT-0022/finding.json) |
| `FND-PARENT-0023` | `closed` | [English](./FND-PARENT-0023/finding.md) · [Deutsch](./FND-PARENT-0023/finding.de.md) · [JSON](./FND-PARENT-0023/finding.json) |
| `FND-PARENT-0025` | `closed` | [English](./FND-PARENT-0025/finding.md) · [Deutsch](./FND-PARENT-0025/finding.de.md) · [JSON](./FND-PARENT-0025/finding.json) |
| `FND-PARENT-0027` | `closed` | [English](./FND-PARENT-0027/finding.md) · [Deutsch](./FND-PARENT-0027/finding.de.md) · [JSON](./FND-PARENT-0027/finding.json) |
| `FND-PARENT-0030` | `closed` | [English](./FND-PARENT-0030/finding.md) · [Deutsch](./FND-PARENT-0030/finding.de.md) · [JSON](./FND-PARENT-0030/finding.json) |
| `FND-PARENT-0031` | `closed` | [English](./FND-PARENT-0031/finding.md) · [Deutsch](./FND-PARENT-0031/finding.de.md) · [JSON](./FND-PARENT-0031/finding.json) |
| `FND-PARENT-0037` | `closed` | [English](./FND-PARENT-0037/finding.md) · [Deutsch](./FND-PARENT-0037/finding.de.md) · [JSON](./FND-PARENT-0037/finding.json) |
| `FND-PARENT-0040` | `closed` | [English](./FND-PARENT-0040/finding.md) · [Deutsch](./FND-PARENT-0040/finding.de.md) · [JSON](./FND-PARENT-0040/finding.json) |
| `FND-SONAR-0011` | `closed` | [English](./FND-SONAR-0011/finding.md) · [Deutsch](./FND-SONAR-0011/finding.de.md) · [JSON](./FND-SONAR-0011/finding.json) |
| `FND-SONAR-0012` | `closed` | [English](./FND-SONAR-0012/finding.md) · [Deutsch](./FND-SONAR-0012/finding.de.md) · [JSON](./FND-SONAR-0012/finding.json) |
| `FND-SONAR-0015` | `closed` | [English](./FND-SONAR-0015/finding.md) · [Deutsch](./FND-SONAR-0015/finding.de.md) · [JSON](./FND-SONAR-0015/finding.json) |
| `FND-SONAR-0017` | `closed` | [English](./FND-SONAR-0017/finding.md) · [Deutsch](./FND-SONAR-0017/finding.de.md) · [JSON](./FND-SONAR-0017/finding.json) |

`FND-SONAR-0012` was closed only after the historical PR #3 failure receipt,
the hash-valid PR #4 remediation/resulting-main receipts, current MRTS main
`615b13bacbd008562c17408246c41ab27dca3104`, all four terminal PR #4 checks,
and a fresh public SonarQube Cloud/GitHub readback confirmed Quality Gate `OK`
and zero vulnerabilities. It does not resolve `FND-SONAR-0009`.

### 2026-07-26 accepted-risk addition / Risikoakzeptanz-Ergänzung 2026-07-26

| ID | Status at move / Status beim Move | Record / Record |
| --- | --- | --- |
| `FND-GITHUB-0004` | `accepted_risk`; Code Scanning AI model remains unavailable, not technically closed | [English](./FND-GITHUB-0004/finding.md) · [Deutsch](./FND-GITHUB-0004/finding.de.md) · [JSON](./FND-GITHUB-0004/finding.json) |
| `FND-GITHUB-0005` | `accepted_risk`; Framework governance bypass risk remains, not technically closed | [English](./FND-GITHUB-0005/finding.md) · [Deutsch](./FND-GITHUB-0005/finding.de.md) · [JSON](./FND-GITHUB-0005/finding.json) |
| `FND-GITHUB-0006` | `accepted_risk`; Advanced CodeQL configuration disposition remains unresolved | [English](./FND-GITHUB-0006/finding.md) · [Deutsch](./FND-GITHUB-0006/finding.de.md) · [JSON](./FND-GITHUB-0006/finding.json) |
| `FND-GITHUB-0007` | `accepted_risk`; queued Cloudflare suites remain without conclusion | [English](./FND-GITHUB-0007/finding.md) · [Deutsch](./FND-GITHUB-0007/finding.de.md) · [JSON](./FND-GITHUB-0007/finding.json) |
| `FND-GITHUB-0008` | `accepted_risk`; required GitHub App configuration remains absent | [English](./FND-GITHUB-0008/finding.md) · [Deutsch](./FND-GITHUB-0008/finding.de.md) · [JSON](./FND-GITHUB-0008/finding.json) |

| ID | Status at move / Status beim Move | Record / Record |
| --- | --- | --- |
| `FND-GITHUB-0001` | `closed` | [English](./FND-GITHUB-0001/finding.md) · [Deutsch](./FND-GITHUB-0001/finding.de.md) · [JSON](./FND-GITHUB-0001/finding.json) |
| `FND-GITHUB-0002` | `closed` | [English](./FND-GITHUB-0002/finding.md) · [Deutsch](./FND-GITHUB-0002/finding.de.md) · [JSON](./FND-GITHUB-0002/finding.json) |
| `FND-GITHUB-0003` | `not_applicable` | [English](./FND-GITHUB-0003/finding.md) · [Deutsch](./FND-GITHUB-0003/finding.de.md) · [JSON](./FND-GITHUB-0003/finding.json) |
| `FND-PARENT-0001` | `closed` | [English](./FND-PARENT-0001/finding.md) · [Deutsch](./FND-PARENT-0001/finding.de.md) · [JSON](./FND-PARENT-0001/finding.json) |
| `FND-FRAMEWORK-0046` | `verified` | [English](./FND-FRAMEWORK-0046/finding.md) · [Deutsch](./FND-FRAMEWORK-0046/finding.de.md) · [JSON](./FND-FRAMEWORK-0046/finding.json) |
| `FND-FRAMEWORK-0051` | `verified` | [English](./FND-FRAMEWORK-0051/finding.md) · [Deutsch](./FND-FRAMEWORK-0051/finding.de.md) · [JSON](./FND-FRAMEWORK-0051/finding.json) |
| `FND-FRAMEWORK-0052` | `verified` | [English](./FND-FRAMEWORK-0052/finding.md) · [Deutsch](./FND-FRAMEWORK-0052/finding.de.md) · [JSON](./FND-FRAMEWORK-0052/finding.json) |
| `FND-SONAR-0006` | `verified` | [English](./FND-SONAR-0006/finding.md) · [Deutsch](./FND-SONAR-0006/finding.de.md) · [JSON](./FND-SONAR-0006/finding.json) |
| `FND-CROSS-0006` | `verified` | [English](./FND-CROSS-0006/finding.md) · [Deutsch](./FND-CROSS-0006/finding.de.md) · [JSON](./FND-CROSS-0006/finding.json) |
| `FND-FRAMEWORK-0004` | `verified` | [English](./FND-FRAMEWORK-0004/finding.md) · [Deutsch](./FND-FRAMEWORK-0004/finding.de.md) · [JSON](./FND-FRAMEWORK-0004/finding.json) |
| `FND-FRAMEWORK-0021` | `verified` | [English](./FND-FRAMEWORK-0021/finding.md) · [Deutsch](./FND-FRAMEWORK-0021/finding.de.md) · [JSON](./FND-FRAMEWORK-0021/finding.json) |
| `FND-FRAMEWORK-0022` | `verified` | [English](./FND-FRAMEWORK-0022/finding.md) · [Deutsch](./FND-FRAMEWORK-0022/finding.de.md) · [JSON](./FND-FRAMEWORK-0022/finding.json) |
| `FND-FRAMEWORK-0026` | `verified` | [English](./FND-FRAMEWORK-0026/finding.md) · [Deutsch](./FND-FRAMEWORK-0026/finding.de.md) · [JSON](./FND-FRAMEWORK-0026/finding.json) |
| `FND-FRAMEWORK-0027` | `verified` | [English](./FND-FRAMEWORK-0027/finding.md) · [Deutsch](./FND-FRAMEWORK-0027/finding.de.md) · [JSON](./FND-FRAMEWORK-0027/finding.json) |
| `FND-FRAMEWORK-0028` | `verified` | [English](./FND-FRAMEWORK-0028/finding.md) · [Deutsch](./FND-FRAMEWORK-0028/finding.de.md) · [JSON](./FND-FRAMEWORK-0028/finding.json) |
| `FND-FRAMEWORK-0045` | `verified` | [English](./FND-FRAMEWORK-0045/finding.md) · [Deutsch](./FND-FRAMEWORK-0045/finding.de.md) · [JSON](./FND-FRAMEWORK-0045/finding.json) |
| `FND-FRAMEWORK-0049` | `verified` | [English](./FND-FRAMEWORK-0049/finding.md) · [Deutsch](./FND-FRAMEWORK-0049/finding.de.md) · [JSON](./FND-FRAMEWORK-0049/finding.json) |
| `FND-SONAR-0002` | `verified` | [English](./FND-SONAR-0002/finding.md) · [Deutsch](./FND-SONAR-0002/finding.de.md) · [JSON](./FND-SONAR-0002/finding.json) |
| `FND-SONAR-0005` | `verified` | [English](./FND-SONAR-0005/finding.md) · [Deutsch](./FND-SONAR-0005/finding.de.md) · [JSON](./FND-SONAR-0005/finding.json) |
| `FND-FRAMEWORK-0001` | `fixed`; release blocker retained (test-only archive) | [English](./FND-FRAMEWORK-0001/finding.md) · [Deutsch](./FND-FRAMEWORK-0001/finding.de.md) · [JSON](./FND-FRAMEWORK-0001/finding.json) |
| `FND-FRAMEWORK-0008` | `fixed`; release blocker retained (test-only archive) | [English](./FND-FRAMEWORK-0008/finding.md) · [Deutsch](./FND-FRAMEWORK-0008/finding.de.md) · [JSON](./FND-FRAMEWORK-0008/finding.json) |
| `FND-FRAMEWORK-0017` | `fixed`; release blocker retained (test-only archive) | [English](./FND-FRAMEWORK-0017/finding.md) · [Deutsch](./FND-FRAMEWORK-0017/finding.de.md) · [JSON](./FND-FRAMEWORK-0017/finding.json) |
| `FND-FRAMEWORK-0020` | `fixed`; release blocker retained (test-only archive) | [English](./FND-FRAMEWORK-0020/finding.md) · [Deutsch](./FND-FRAMEWORK-0020/finding.de.md) · [JSON](./FND-FRAMEWORK-0020/finding.json) |
| `FND-FRAMEWORK-0030` | `fixed`; release blocker retained (test-only archive) | [English](./FND-FRAMEWORK-0030/finding.md) · [Deutsch](./FND-FRAMEWORK-0030/finding.de.md) · [JSON](./FND-FRAMEWORK-0030/finding.json) |
| `FND-FRAMEWORK-0032` | `fixed`; release blocker retained (test-only archive) | [English](./FND-FRAMEWORK-0032/finding.md) · [Deutsch](./FND-FRAMEWORK-0032/finding.de.md) · [JSON](./FND-FRAMEWORK-0032/finding.json) |
| `FND-FRAMEWORK-0034` | `fixed`; release blocker retained (test-only archive) | [English](./FND-FRAMEWORK-0034/finding.md) · [Deutsch](./FND-FRAMEWORK-0034/finding.de.md) · [JSON](./FND-FRAMEWORK-0034/finding.json) |
| `FND-FRAMEWORK-0035` | `fixed`; release blocker retained (test-only archive) | [English](./FND-FRAMEWORK-0035/finding.md) · [Deutsch](./FND-FRAMEWORK-0035/finding.de.md) · [JSON](./FND-FRAMEWORK-0035/finding.json) |
| `FND-FRAMEWORK-0037` | `fixed`; release blocker retained (test-only archive) | [English](./FND-FRAMEWORK-0037/finding.md) · [Deutsch](./FND-FRAMEWORK-0037/finding.de.md) · [JSON](./FND-FRAMEWORK-0037/finding.json) |
| `FND-FRAMEWORK-0038` | `fixed`; release blocker retained (test-only archive) | [English](./FND-FRAMEWORK-0038/finding.md) · [Deutsch](./FND-FRAMEWORK-0038/finding.de.md) · [JSON](./FND-FRAMEWORK-0038/finding.json) |
| `FND-FRAMEWORK-0039` | `fixed`; release blocker retained (test-only archive) | [English](./FND-FRAMEWORK-0039/finding.md) · [Deutsch](./FND-FRAMEWORK-0039/finding.de.md) · [JSON](./FND-FRAMEWORK-0039/finding.json) |
| `FND-FRAMEWORK-0044` | `fixed`; release blocker retained (test-only archive) | [English](./FND-FRAMEWORK-0044/finding.md) · [Deutsch](./FND-FRAMEWORK-0044/finding.de.md) · [JSON](./FND-FRAMEWORK-0044/finding.json) |
| `FND-FRAMEWORK-0047` | `fixed`; release blocker retained (test-only archive) | [English](./FND-FRAMEWORK-0047/finding.md) · [Deutsch](./FND-FRAMEWORK-0047/finding.de.md) · [JSON](./FND-FRAMEWORK-0047/finding.json) |
| `FND-FRAMEWORK-0048` | `fixed`; release blocker retained (test-only archive) | [English](./FND-FRAMEWORK-0048/finding.md) · [Deutsch](./FND-FRAMEWORK-0048/finding.de.md) · [JSON](./FND-FRAMEWORK-0048/finding.json) |
| `FND-FRAMEWORK-0050` | `fixed`; release blocker retained (test-only archive) | [English](./FND-FRAMEWORK-0050/finding.md) · [Deutsch](./FND-FRAMEWORK-0050/finding.de.md) · [JSON](./FND-FRAMEWORK-0050/finding.json) |
| `FND-PARENT-0016` | `fixed`; release blocker retained (test-only archive) | [English](./FND-PARENT-0016/finding.md) · [Deutsch](./FND-PARENT-0016/finding.de.md) · [JSON](./FND-PARENT-0016/finding.json) |
| `FND-PARENT-0017` | `fixed`; release blocker retained (test-only archive) | [English](./FND-PARENT-0017/finding.md) · [Deutsch](./FND-PARENT-0017/finding.de.md) · [JSON](./FND-PARENT-0017/finding.json) |
| `FND-PARENT-0019` | `fixed`; release blocker retained (test-only archive) | [English](./FND-PARENT-0019/finding.md) · [Deutsch](./FND-PARENT-0019/finding.de.md) · [JSON](./FND-PARENT-0019/finding.json) |
| `FND-PARENT-0024` | `fixed`; release blocker retained (test-only archive) | [English](./FND-PARENT-0024/finding.md) · [Deutsch](./FND-PARENT-0024/finding.de.md) · [JSON](./FND-PARENT-0024/finding.json) |
| `FND-PARENT-0033` | `fixed`; release blocker retained (test-only archive) | [English](./FND-PARENT-0033/finding.md) · [Deutsch](./FND-PARENT-0033/finding.de.md) · [JSON](./FND-PARENT-0033/finding.json) |
| `FND-PARENT-0034` | `fixed`; release blocker retained (test-only archive) | [English](./FND-PARENT-0034/finding.md) · [Deutsch](./FND-PARENT-0034/finding.de.md) · [JSON](./FND-PARENT-0034/finding.json) |
| `FND-PARENT-0035` | `fixed`; release blocker retained (test-only archive) | [English](./FND-PARENT-0035/finding.md) · [Deutsch](./FND-PARENT-0035/finding.de.md) · [JSON](./FND-PARENT-0035/finding.json) |
| `FND-PARENT-0038` | `fixed`; release blocker retained (test-only archive) | [English](./FND-PARENT-0038/finding.md) · [Deutsch](./FND-PARENT-0038/finding.de.md) · [JSON](./FND-PARENT-0038/finding.json) |
| `FND-PARENT-0041` | `fixed`; release blocker retained (test-only archive) | [English](./FND-PARENT-0041/finding.md) · [Deutsch](./FND-PARENT-0041/finding.de.md) · [JSON](./FND-PARENT-0041/finding.json) |
| `FND-PARENT-0044` | `fixed`; release blocker retained (test-only archive) | [English](./FND-PARENT-0044/finding.md) · [Deutsch](./FND-PARENT-0044/finding.de.md) · [JSON](./FND-PARENT-0044/finding.json) |
| `FND-PARENT-0045` | `fixed`; release blocker retained (test-only archive) | [English](./FND-PARENT-0045/finding.md) · [Deutsch](./FND-PARENT-0045/finding.de.md) · [JSON](./FND-PARENT-0045/finding.json) |
| `FND-PARENT-0049` | `fixed`; release blocker retained (test-only archive) | [English](./FND-PARENT-0049/finding.md) · [Deutsch](./FND-PARENT-0049/finding.de.md) · [JSON](./FND-PARENT-0049/finding.json) |
| `FND-PARENT-0051` | `fixed`; release blocker retained (test-only archive) | [English](./FND-PARENT-0051/finding.md) · [Deutsch](./FND-PARENT-0051/finding.de.md) · [JSON](./FND-PARENT-0051/finding.json) |
| `FND-SONAR-0003` | `fixed`; release blocker retained (test-only archive) | [English](./FND-SONAR-0003/finding.md) · [Deutsch](./FND-SONAR-0003/finding.de.md) · [JSON](./FND-SONAR-0003/finding.json) |

The archive is lossless: every listed finding retains its original ID,
English/German reader records, structured JSON, retained evidence references,
and historical lifecycle entries. This archive does not authorize a product,
Framework, MRTS, Gitlink, delivery, or status change.

## Current-user accepted-risk decision / Aktuelle Nutzer-Risikoakzeptanz

At `2026-07-26T14:18:25Z`, the current user explicitly accepted the exact
residual risks of `FND-GITHUB-0004` through `FND-GITHUB-0008` for local
archival only. The records respectively retain the unavailable Code Scanning
AI model, missing Framework master governance, unresolved Advanced CodeQL
configuration disposition, queued Cloudflare suites, and missing dedicated
GitHub App configuration. This is not a technical remediation, a passing
check, a closure, or authorization for production, publication, or release.
Before any such decision, restore every one of these five records to
`.codex/findings/` and revalidate it under its existing acceptance criteria.

Am `2026-07-26T14:18:25Z` akzeptierte der aktuelle Nutzer die exakten
Restrisiken von `FND-GITHUB-0004` bis `FND-GITHUB-0008` ausdrücklich nur für
die lokale Archivierung. Die Records bewahren jeweils das nicht verfügbare Code
Scanning AI-Modell, fehlende Framework-master-Governance, die ungelöste
Advanced-CodeQL-Konfigurationsdisposition, queued Cloudflare-Suites und die
fehlende dedizierte GitHub-App-Konfiguration. Dies ist keine technische
Remediation, kein bestandener Check, kein Abschluss und keine Autorisierung
für Produktion, Veröffentlichung oder Release. Vor einer solchen Entscheidung
muss jeder dieser fünf Records nach `.codex/findings/` zurückverschoben und
nach seinen bestehenden Akzeptanzkriterien neu validiert werden.

`FND-FRAMEWORK-0031` is archived only under the current user's test-only
scope. Although it reports `verified`, its P1 release blocker and pending
external Cloud revalidation remain effective; it is not technically closed or
safe for release.

## Test-only fixed release-blocker decision / Test-only-Entscheidung zu fixed Release-Blockern

The current user explicitly selected the twenty-nine `fixed` records above for
this archive because the repository is used for testing only and no release is
planned. This is not a status change, a release approval, a security
verification, or an acceptance that the fixes are safe for production. Their
exact residual risk remains: the original condition or a related bypass can
still require current exact-head, resulting-master, original-reproduction, or
external validation. Before any production, publication, or release decision,
each such record must be restored to `.codex/findings/` and revalidated under
its existing acceptance criteria.

Das Archiv ist verlustfrei: Jedes aufgelistete Finding behält seine ursprüngliche
ID, die englischen/deutschen Leserrecords, das strukturierte JSON, die
aufbewahrten Evidence-Referenzen und historische Lifecycle-Einträge. Dieses
Archiv autorisiert keine Produkt-, Framework-, MRTS-, Gitlink-, Delivery- oder
Statusänderung.

`FND-FRAMEWORK-0031` ist nur im test-only Scope des aktuellen Nutzers
archiviert. Obwohl es `verified` meldet, bleiben sein P1-Release-Blocker und
die ausstehende externe Cloud-Neubewertung wirksam; es ist weder technisch
geschlossen noch releasesicher.

Der aktuelle Nutzer hat die obenstehenden neunundzwanzig `fixed` Records
ausdrücklich für dieses Archiv gewählt, weil das Repository nur zum Testen
verwendet wird und kein Release geplant ist. Dies ist keine Statusänderung,
keine Release-Freigabe, keine Security-Verifikation und keine Aussage, dass die
Fixes für Produktion sicher sind. Das exakte Restrisiko bleibt: Die ursprüngliche
Bedingung oder ein verwandter Bypass kann weiterhin aktuelle Exact-Head-,
Resulting-Master-, Original-Reproduktion- oder externe Validierung erfordern.
Vor jeder Produktions-, Veröffentlichungs- oder Release-Entscheidung muss jeder
solche Record nach `.codex/findings/` zurückverschoben und anhand seiner
bestehenden Akzeptanzkriterien erneut validiert werden.
