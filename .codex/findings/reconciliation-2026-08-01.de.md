# Finding-Abgleich — 2026-08-01

**Sprache:** Deutsch | [English](reconciliation-2026-08-01.md)

## Scope und Evidenzgrenze

Dieses Register ist der aktuelle, schreibgeschützte Abgleich jedes kanonischen
aktiven Findings unter `.codex/findings/` zum `2026-08-01T17:36:54Z`. Es
umfasst 80 kanonische Tripel und bewahrt das reservierte leere Legacy-Verzeichnis
`FND-PARENT-0032`. Das vorhandene Archiv wurde auf Kollisionen,
Regulärdatei-Sicherheit und sein 300-Mitglieder-Checksum-Manifest geprüft; es
wird durch diesen Auftrag nicht rückwirkend umgeschrieben.

Der anfängliche Parent-Evidenz-Snapshot war `origin/master`
`d7dfbc505b5aa0adf22d10d8517a518ff05b95be` (PR #226). Vor dem Staging lief die
aktuelle Parent-Basis über PR #228 auf PR #227,
`522e791c1efa21da6101f9a0908d5e185736b518` und danach über den test-only-PR
#229 auf den aktuellen `origin/master` `59aba762f2d852fd917079ca8519e4ea7f49169c`
weiter. PR #229 ändert 29 Testmodule, darunter die Generated-Report-Evidence-
Suite; die gezielten Current-Base-Controls wurden nach dem Rebase wiederholt.
PR #228 ändert nur den Parent→Framework-Gitlink auf
`5cb371949ceafec6685cf716ba50a75d0f448bd1`; sein Framework-Snapshot ändert nur
CodeQL-Workflow-/Lock-Dateien und behält Framework→MRTS bei
`615b13bacbd008562c17408246c41ab27dca3104`. PR #227 retirert absichtlich
einzelne historische Change Records und bewahrt die Nachvollziehbarkeit über
Git-Historie/Commits/PRs; kein Finding-Markdown-Link zeigt auf einen entfernten
Bericht. Parent, Framework und MRTS blieben in getrennten Ownership-Grenzen,
und diese Aufgabe änderte keinen Gitlink.

Die Aktionslabels verwenden das Repository-Lifecycle-Vokabular. `fixed` bedeutet
einen gemergten Root-Cause-Change mit weiterhin fehlenden aktuellen
Akzeptanzkontrollen und ist keine Archivfreigabe. `ARCHIVE` wird nur verwendet,
wenn ursprünglicher PR/Abschluss, Default-Branch-Erreichbarkeit, aktueller
Quell- oder Scannerbeleg, legitimer Control und kein widersprechendes offenes
task-spezifisches Scanner-Signal belegt sind.

Frische Remote-Evidence: PRs und Commits wurden gegen das richtige Repository
und den aktuellen Default-Branch geprüft; GitHub zeigt keine offenen Code-
Scanning-, Secret-Scanning-, Dependabot- oder Security-Advisory-Alerts. Das
Default-Branch-Sonar-Quality-Gate steht wegen der separat aktiven
`FND-SONAR-0001`-Security-Rating-Bedingung auf `ERROR` und ist kein
Pass-Ersatz. Der finale Dokumentations-PR benötigt separat eine grüne
Exact-Head-Sonar-Analyse.

## Entscheidungsmatrix pro Finding

| Finding | Vorheriger Status | Ermittelter Status / Aktion | Archiv | Evidence oder verbleibender Blocker |
| --- | --- | --- | --- | --- |
| FND-CROSS-0001 | validated | validated · UPDATE_EVIDENCE | nein | 58 stale und 9 SHA-mismatch Assessment-Einträge; Governance-Artefakte fehlen. |
| FND-CROSS-0002 | validated | validated · UPDATE_EVIDENCE | nein | Kein frisches kanonisches JSON-Receipt oder zurechenbarer Remediation-PR. |
| FND-CROSS-0003 | blocked | blocked · KEEP_UNCHANGED | nein | Keine isolierte Restart-/Port-Release-Matrix. |
| FND-CROSS-0004 | blocked | blocked · KEEP_UNCHANGED | nein | Keine aktuelle External-Copy-CRS-Allow/Block-Profile-Evidence. |
| FND-CROSS-0005 | blocked | blocked · KEEP_UNCHANGED | nein | Abhängige Cross-Repository- und Scanner-Voraussetzungen bleiben offen. |
| FND-CROSS-0007 | fixed | fixed · UPDATE_EVIDENCE | nein | Behauptete Commits sind Gitlink-Updates, kein zurechenbarer Policy-Fix-PR. |
| FND-CROSS-0008 | in_progress | fixed · UPDATE_STATUS_AND_EVIDENCE | nein | #74-Root-Fix vorhanden; Runtime-/Terminal-Artefakt fehlt. |
| FND-FRAMEWORK-0007 | blocked | blocked · UPDATE_EVIDENCE | nein | Finalizer-Quellcode vorhanden, aber kein Raw-Lifecycle-/Allow-Block-Receipt. |
| FND-FRAMEWORK-0009 | blocked | blocked · UPDATE_EVIDENCE | nein | H2-Quell-Support ist kein aufbewahrtes NGINX-H2-Runtime-Ergebnis. |
| FND-FRAMEWORK-0057 | blocked | fixed · UPDATE_STATUS_AND_EVIDENCE | nein | Framework #51 und Parent #126/#74 gemergt; Parent-Runtime-Beleg fehlt. |
| FND-HOST-0003 | blocked | blocked · UPDATE_EVIDENCE | nein | NGINX fehlt; kein Service/Harness gestartet. |
| FND-HOST-0006 | blocked | blocked · UPDATE_EVIDENCE | nein | sqlite3-Header/pkg-config fehlen; kein autorisierter Rebuild. |
| FND-MRTS-0001 | blocked | blocked · UPDATE_EVIDENCE | nein | Read-only-MRTS-Tip sauber, aber kein External-Copy-Allow/Block-Profil. |
| FND-MRTS-0002 | fixed | fixed · UPDATE_EVIDENCE | nein | Marker bleibt; Validator besteht, Regression-Suite scheitert derzeit 1/30. |
| FND-PARENT-0002 | triaged | triaged · UPDATE_EVIDENCE | nein | Historische ShellCheck-Diagnostik ohne frischen Äquivalent-Run. |
| FND-PARENT-0003 | triaged | triaged · UPDATE_EVIDENCE | nein | Historische Staticcheck-Diagnostik ohne frischen Äquivalent-Run. |
| FND-PARENT-0005 | validated | fixed · UPDATE_STATUS_AND_EVIDENCE | nein | #74-Deadline-Fix gemergt; aktueller Timeout-Control nicht wiederholt. |
| FND-PARENT-0006 | validated | validated · UPDATE_EVIDENCE | nein | NGINX hält weiter nur das konfigurierte Body-Präfix. |
| FND-PARENT-0007 | validated | validated · UPDATE_EVIDENCE | nein | Traefik hat keine maximale Worker-Admission-Bound. |
| FND-PARENT-0008 | fixed | fixed · UPDATE_EVIDENCE | nein | #183 gemergt; aktueller Compiler-Warning-Control nicht wiederholt. |
| FND-PARENT-0009 | triaged | triaged · UPDATE_EVIDENCE | nein | Kein frischer Production-Artifact-Linker-Hardening-Scan. |
| FND-PARENT-0010 | blocked | blocked · UPDATE_EVIDENCE | nein | HAProxy-Contract verbietet Capability-Promotion weiterhin ausdrücklich. |
| FND-PARENT-0011 | blocked | blocked · UPDATE_EVIDENCE | nein | Envoy bleibt partial/minimal; keine Promotion-Autorität. |
| FND-PARENT-0013 | blocked | blocked · UPDATE_EVIDENCE | nein | Same-UID-Final-Unlink-Race ohne hostile Race-Harness. |
| FND-PARENT-0014 | blocked | blocked · UPDATE_EVIDENCE | nein | Storage-Final-Leaf-Replacement-Window bleibt ungetestet. |
| FND-PARENT-0015 | blocked | blocked · UPDATE_EVIDENCE | nein | UDS-Readiness-to-Dial-Peer-Identity-Rebinding-Control fehlt. |
| FND-PARENT-0020 | verified | fixed · UPDATE_STATUS_AND_EVIDENCE | nein | #51 erreichbar, aber aktueller Native-Middleware-Control nicht wiederholt. |
| FND-PARENT-0021 | blocked | blocked · KEEP_UNCHANGED | nein | Storage-Helper fail-closed; Control-Plane-Fix out of scope. |
| FND-PARENT-0026 | fixed | fixed · UPDATE_EVIDENCE | nein | #58-Root-Confinement vorhanden; negativer Runtime-Path-Control fehlt. |
| FND-PARENT-0028 | triaged | triaged · UPDATE_EVIDENCE | nein | Gepinnte äußere Actions referenzieren mutable innere Docker-Tags. |
| FND-PARENT-0029 | in_progress | closed · ARCHIVE | ja | #56-Merge `a73c335…`, kanonischer Return, zwei aktuelle Controls bestanden, ursprünglicher Sonar-Key resolved. |
| FND-PARENT-0032 | reserved | reserved · KEEP_UNCHANGED | nein | Bewusst leeres Legacy-Verzeichnis im Strukturmanifest. |
| FND-PARENT-0036 | fixed | fixed · KEEP_UNCHANGED | nein | Stärkster ASan-/Allocator-Replay bleibt nicht verfügbar. |
| FND-PARENT-0039 | in_progress | closed · ARCHIVE | ja | #65-Closure-Merge `1fa024ca…`; #227 retirierte die korrigierten Records, daher wird die veraltete Formulierung nicht mehr veröffentlicht; exakte PR-Checks grün. |
| FND-PARENT-0042 | blocked | blocked · UPDATE_EVIDENCE | nein | #55 closed/unmerged; Tag-Archive-Quelle bleibt im Code. |
| FND-PARENT-0043 | blocked | blocked · KEEP_UNCHANGED | nein | Native-Apache/APR/LibModSecurity-Sanitizer-Run fehlt. |
| FND-PARENT-0046 | triaged | triaged · UPDATE_EVIDENCE | nein | Aktuelle Python-Version-Regex bleibt semantisch falsch. |
| FND-PARENT-0047 | verified | closed · ARCHIVE | ja | #90-Merge `ad953cd…`; Go-Selector unverändert, exakte PR-Checks grün. |
| FND-PARENT-0048 | in_progress | closed · ARCHIVE | ja | #92-Merge `95fb491…`; Locked Install und aktueller Quick-Check-Workflow bestanden. |
| FND-PARENT-0050 | in_progress | fixed · UPDATE_STATUS_AND_EVIDENCE | nein | #74-Root-Change vorhanden; Producer-/Cross-Repo-Validierung fehlt. |
| FND-PARENT-0052 | in_progress | fixed · UPDATE_STATUS_AND_EVIDENCE | nein | #74-EXPAT-Immutable-Path vorhanden; Producer-Validierung fehlt. |
| FND-PARENT-0053 | in_progress | fixed · UPDATE_STATUS_AND_EVIDENCE | nein | #74-PCRE2-Literal-Hash-Path vorhanden; Terminal-Producer-Gate fehlt. |
| FND-PARENT-0054 | verified | in_progress · UPDATE_STATUS_AND_EVIDENCE | nein | Der historische begrenzte Diagnose-Commit `b28b874…` ist vom aktuellen Master nicht erreichbar; der heutige leichte Workflow schließt diesen Strict-Producer-Pfad ausdrücklich aus. |
| FND-PARENT-0055 | verified | blocked · UPDATE_STATUS_AND_EVIDENCE | nein | Referenzierte Dateien ohne autorisierte Entfernungs-/Replacement-Provenance. |
| FND-PARENT-0056 | in_progress | fixed · UPDATE_STATUS_AND_EVIDENCE | nein | #74/#126-Source-/Gitlink-Evidence vorhanden; Strict-Producer-Replay fehlt. |
| FND-PARENT-0057 | in_progress | in_progress · UPDATE_EVIDENCE | nein | Staging-Root-Repair nicht auf aktuellem Master vorhanden. |
| FND-PARENT-0058 | in_progress | fixed · UPDATE_STATUS_AND_EVIDENCE | nein | #74-Port-Plan-Fix bleibt, Full-Matrix-/Hosted-Replay fehlt. |
| FND-PARENT-0059 | in_progress | fixed · UPDATE_STATUS_AND_EVIDENCE | nein | #74-Locking-Fix bleibt, Target-Receipt/Hosted-Run fehlt. |
| FND-PARENT-0060 | fixed | fixed · UPDATE_EVIDENCE | nein | #74-FIFO-Fix/Test existiert; aktueller Control-Replay fehlt. |
| FND-PARENT-0061 | fixed | fixed · UPDATE_EVIDENCE | nein | #74-Wrapper-/FD-Control existiert; Runtime-Replay fehlt. |
| FND-PARENT-0062 | validated | validated · KEEP_UNCHANGED | nein | Aktueller Governance-Job-Mismatch reproduziert sich. |
| FND-PARENT-0063 | validated | validated · REQUIRES_USER_DECISION | nein | Release-Provenance-Policy benötigt Owner-Entscheidung. |
| FND-PARENT-0064 | verified | verified · UPDATE_EVIDENCE | nein | #183/Harness bestehen; breiter Live-Apache-Closure-Control fehlt. |
| FND-PARENT-0065 | validated | fixed · UPDATE_STATUS_AND_EVIDENCE | nein | #175-Safe-File-Fix/Regressionen vorhanden; Resulting-Master-Control fehlt. |
| FND-PARENT-0066 | fixed | fixed · UPDATE_EVIDENCE | nein | #178 gemergt; Original-Bypass nicht frisch wiederholt. |
| FND-PARENT-0067 | validated | validated · KEEP_UNCHANGED | nein | Unabhängige Leak-Root-Cause bleibt offen. |
| FND-PARENT-0068 | in_progress | in_progress · UPDATE_EVIDENCE | nein | #183 fixt einen Runner; Sibling-Root-Cause bleibt. |
| FND-PARENT-0069 | validated | validated · KEEP_UNCHANGED | nein | C17/Werror-Hardening-Gap bleibt. |
| FND-PARENT-0070 | fixed | fixed · UPDATE_EVIDENCE | nein | #183-Source-Fix vorhanden; APXS/DSO/HTTP-Control fehlt. |
| FND-PARENT-0071 | fixed | fixed · UPDATE_EVIDENCE | nein | #183-Source-Fix vorhanden; Live-Start/Readiness-Control fehlt. |
| FND-PARENT-0072 | fixed | fixed · UPDATE_EVIDENCE | nein | #183-PR-Sonar sauber; Default-Branch-Key-Readback fehlt. |
| FND-PARENT-0073 | fixed | verified · UPDATE_STATUS_AND_EVIDENCE | nein | #182-fokussierte Controls bestehen; vollständige Framework-Suite bewusst blockiert. |
| FND-PARENT-0074 | closed | closed · ARCHIVE | ja | #213-Merge `f335965…`; aktuelle Root-/Symlink-Controls bestanden (107 Tests). |
| FND-PARENT-0075 | not_applicable | not_applicable · UPDATE_EVIDENCE | nein | #213-Clean-History-Replacement gemergt; formale Supersession bleibt aktiv. |
| FND-SONAR-0001 | blocked | blocked · UPDATE_EVIDENCE | nein | Aktuelles Master-QG-ERROR gehört zu diesem Security-Rating-Blocker. |
| FND-SONAR-0004 | blocked | blocked · KEEP_UNCHANGED | nein | Sonar-Admin-Autorität bleibt extern. |
| FND-SONAR-0009 | blocked | blocked · UPDATE_EVIDENCE | nein | Framework-Coverage-Workflow/Owner-Konfiguration fehlt. |
| FND-SONAR-0016 | in_progress | in_progress · KEEP_UNCHANGED | nein | Aggregierte Restpunkte einschließlich 0001 bleiben offen. |
| FND-SONAR-0019 | fixed | fixed · UPDATE_EVIDENCE | nein | #150 gemergt; Traefik-Runtime-Revalidierung fehlt. |
| FND-SONAR-0020 | closed | closed · ARCHIVE | ja | #197 `caddd86…`, aktueller Sonar-Key CLOSED/FIXED, PR-Checks grün. |
| FND-SONAR-0021 | closed | closed · ARCHIVE | ja | #177 `a1c839…`, aktueller S131-Key CLOSED/FIXED, PR-Checks grün. |
| FND-SONAR-0022 | fixed | fixed · UPDATE_EVIDENCE | nein | #200-Source-Fix; globales QG ist kein Resulting-Master-Pass. |
| FND-SONAR-0023 | verified | verified · UPDATE_EVIDENCE | nein | #200-Key resolved; Lifecycle ist kein formaler Abschluss. |
| FND-SONAR-0024 | verified | verified · UPDATE_EVIDENCE | nein | #200-Key resolved; Lifecycle ist kein formaler Abschluss. |
| FND-SONAR-0025 | verified | verified · UPDATE_EVIDENCE | nein | #201 gemergt; direkter aktueller Key-Readback fehlt. |
| FND-SONAR-0026 | verified | verified · UPDATE_EVIDENCE | nein | #198-Key fehlt in Master-Analyse; formaler Abschluss nicht belegt. |
| FND-SONAR-0027 | verified | verified · UPDATE_EVIDENCE | nein | #206 gemergt; globales QG separat blockiert. |
| FND-SONAR-0028 | verified | verified · UPDATE_EVIDENCE | nein | #221-Original-Key aktuell CLOSED/FIXED, Record bleibt verified. |
| FND-SONAR-0029 | verified | verified · UPDATE_EVIDENCE | nein | #221-Original-Key CLOSED/FIXED; erst Schema-/Evidence-Repair nötig. |
| FND-SONAR-0030 | fixed | fixed · UPDATE_EVIDENCE | nein | #226 gemergt; zwei direkte aktuelle Sonar-Key-Readbacks fehlen. |
| FND-SONAR-0031 | verified | verified · UPDATE_EVIDENCE | nein | #225-Keys/Controls resolved; Lifecycle bleibt verified. |

## Archivierungsmenge

Die sieben `ARCHIVE`-Zeilen werden verlustfrei mit englischem, deutschem und
JSON-Record verschoben. Erforderlichenfalls erhalten die Records davor den
Lifecycle `closed`; Archiv-README und SHA-256-Manifest werden aktualisiert.
Alle anderen kanonischen Findings bleiben aktiv. Kein Status wird allein wegen
eines PRs oder Commits angehoben.

## Während dieses Abgleichs ausgeführte Validierung

- Current Parent PR-/Merge-/Default-Branch-Erreichbarkeit sowie GitHub Actions,
  CodeQL, Code Scanning, Secret Scanning, Dependabot und Sonar-API-Readbacks.
- Aktuelle `python3 -B -m unittest`-Root-/Symlink-Controls für
  `FND-PARENT-0074`: 107 Tests bestanden.
- Zwei spezifizierte aktuelle Optional-Prerequisite-Controls für
  `FND-PARENT-0029`: beide bestanden.
- Portable Dokumentationslinks: Alle relativen Markdown-Ziele lösen in diesem
  Checkout auf. Historische task-lokale Evidence-Pfade bleiben als Literale
  erhalten statt als nicht portable absolute Hyperlinks oder erfundene
  Replacement-Ziele; dies umfasst 24 historische Pfade, die auf diesem Host
  nicht mehr vorhanden sind.
- Read-only-Source-/Revision-Vergleiche für alle restlichen Records;
  nicht verfügbare Runtime-, Native-, External-Copy- und Retained-Artifact-
  Controls sind als Lücken, nie als Pass, dokumentiert.
