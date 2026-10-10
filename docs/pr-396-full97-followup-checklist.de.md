# PR #396 — Full97-Folgearbeit

**Sprache:** [English](pr-396-full97-followup-checklist.md) | Deutsch

Aktualisiert am 2026-10-10. Der neue lokale Standard-Full97 R17 ist vollständig abgenommen: **Canonical PASS, 97/97 Required-PASS**, einschließlich direkt gemessenem generischem Strict-Clientabschluss. [Öffentlicher R17-Bericht](https://github.com/Easton97-Jens/ModSecurity-conector/pull/396#issuecomment-6101794434) wurde vor dieser Dokumentationsänderung veröffentlicht. [Parent PR #396](https://github.com/Easton97-Jens/ModSecurity-conector/pull/396) war bei der Dokumentationsvorbereitung OPEN/DRAFT; tatsächlicher Ready-Übergang und aktueller Status stehen in den PR-Metadaten und im öffentlichen Delivery-Readback; [Framework PR #137](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/137) ist CLOSED/MERGED. Das ist ein lokaler NGINX-H1-Nachweis, kein Protected-Nachweis oder Merge. Die [übergeordnete PR #382-Checkliste](https://github.com/Easton97-Jens/ModSecurity-conector/blob/fix/unified-native-results-events-20260921/docs/pr-382-checklist.de.md) und I09–I12 bleiben separat offen; die [aktuelle Restmatrix](https://github.com/Easton97-Jens/ModSecurity-conector/blob/fix/unified-native-results-events-20260921/docs/pr-382-i09-i12-rest-matrix.de.md) liegt ebenfalls auf dem autorisierten #382-Branch.

## Revisions- und Evidence-Vertrag

| Binding | Tested Parent | Tested Framework | Meaning |
| --- | --- | --- | --- |
| R | `dca17fd5690c2ec2b8806024d1061744db8c3ad8` | `4c6c21e8622840b4c218d8ea5520dd0b10b3fac9` | Unveränderliches historisches R13; ursprüngliche RED-Tests liefen auf ausdrücklich gekennzeichneten Test-/Source-Arbeits-Overlays dieser Basen. |
| G | `b4044d10682cb2881c218fe84cebe41e61b235c2` | `3a1932ef9060103d3a63b47d87c36006af954ee6` | Historical tested source; frische Parent 345-/Framework 413-/Namespace 61-Tests sowie nativer Parent-Lint/Dokumentationscheck. |
| L | `2686b07aaf64b0541d743b53970008bd86caa91f` | `3a1932ef9060103d3a63b47d87c36006af954ee6` | Tatsächlich vollständiger nativer Framework-Lint:604 Testausführungen /19 Suiten, Exit0; nicht auf den späteren Parent G umetikettiert. |
| N | `ff162ecb11217320a81829169a72ca4a5a4081f9` | `1bfc4f8e8e4aa9d618c4cfb2205badd5008d8f75` | Entfernungsintegration; Parent-Lint300/keine SKIPs/Exit0 und Framework 415/keine SKIPs/Exit0. Zwei Config-Startversuche endeten137 vor NGINX. |
| C | `4423e13e7fb26285a93b0c08323a37491e5941a2` | `1bfc4f8e8e4aa9d618c4cfb2205badd5008d8f75` | Historischer vollständiger bounded AB/CD-Checkpoint: ConfigPASS, AB16PASS2FAIL79NE/CD6PASS2FAIL89NE; damaligerB-Pairingdefekt. Tests/Lint nur an dieserBinding. |
| T | `34127a6a462ec448b6b1d0c1d7cf16541c8ab55f` | `9f41f80db7bf53b57429457bce0dda675d2ec5d7` | Historischer begrenzter Runtime-Source-Stand: readyAB und readyCD scoped PASS; ursprüngliche Aggregate bleiben FAIL. |
| U / R17 | `2f02370b07149265841411894f1a2cf7f1e978ff` | `9f41f80db7bf53b57429457bce0dda675d2ec5d7` | Tatsächlich getesteter Source-Stand des einzigen neuen Standard-Full97; Canonical PASS und vollständige direkte Abschlussmessungen. |

R/G/L/N/C/T sind historische Bindungen; ihre damaligen Fehler und Grenzen bleiben unverändert. U ist der tatsächlich getestete Runtime-Head. MRTS bleibt `8a6bb546c4c81d8ffc7be801dceac60c6925685f`, NGINX bleibt 1.31.6. Ein späterer Dokumentationscommit erhält eigene CI und Remote-Readbacks, aber keinen geerbten Runtime-PASS. Der tatsächliche PR-Status und Dokumentations-Head werden separat in den PR-Metadaten ausgewiesen.

| Fix key | Separate commit | Responsibility |
| --- | --- | --- |
| A | `b0d75ef6bbc33228423aef65d8ea3409387ab30f` | Parent: identitätsgebundene Interventionswerte. |
| AF | `7672340c57b3f7c80f4f5c68fc55fecca2ae4af8` | Parent: ausdrücklich positive Fehlerverträge erhalten. |
| B | `58d07970b755d7435c23030e844a32e2f6b6b583` | Parent: First-Byte-Snapshot vor Release und eindeutiger bytegebundener Receipt. |
| C | `e8a8f98a4c24958616b15b98aadedcc73345a786` | Framework: beobachtete native H1-Protokoll-/Eventbindung. |
| D | `0c7f224731cda059decee026c7bd32e58bf9aa21` | Framework: eng begrenztes bestehendes MIME-Allow-Gesamtschema. |
| I | `2686b07aaf64b0541d743b53970008bd86caa91f` | Separate Parent-Integration des Framework-Gitlinks. |
| S | `b4044d10682cb2881c218fe84cebe41e61b235c2` | Zwei verhaltenserhaltende Helfer für tatsächliche `python:S3776`-Findings; keine Suppression. |
| Rm | `41eaa6c7` | Parent: repositoryweite Entfernung der Body-Limit-API; historische/negative Fixtures erhalten. |
| Rf | `1bfc4f8e8e4aa9d618c4cfb2205badd5008d8f75` | Framework: Required-ID `invalid_size` unverändert, Migration auf echte Ablehnung der entfernten Direktive. |
| Ri | `ff162ecb11217320a81829169a72ca4a5a4081f9` | Separater Parent-Framework-Gitlink-Commit; MRTS unverändert. |
| Rc | `4423e13e7fb26285a93b0c08323a37491e5941a2` | Separater relevanter Checker-/CI-Folgefix mit Regressionen; keine Suppression. |
| Bp | `873e51fbebbedb163a5c75a22a7abe0158861a40` | SeparaterFramework-Zwei-Originalevent-Pairingfix. |
| Bq | `9f41f80db7bf53b57429457bce0dda675d2ec5d7` | Minimaler taskrelevanter S3776/S107-Qualitätsfolgefix, ohneSuppression. |
| Pi | `34127a6a462ec448b6b1d0c1d7cf16541c8ab55f` | SeparaterParent-GitlinkCommit; MRTSunverändert. |

## Aktueller lokaler Full97 — U / R17

Run-ID: `nginx_full97_2f02_20261010_r17`. Der einzige freigegebene neue `make full-lifecycle-nginx` endete mit tatsächlichem Make-/Supervisor-Exit0 nach 554.091s; Original-Validator-Exit0, Schemafehlerliste leer. Unveränderte Auswahl: 14 YAML + 42 native + 10 Configtests + 31 explizite Ableitungen = 97 Required-PASS. Das gesamte Inventar166 enthält 97 PASS, 34 nicht ausgewählte NOT_EXECUTED und35 NOT_APPLICABLE. Der Collector-Source bleibt separat PASS mit 31 PASS/42 NOT_EXECUTED-Platzhaltern; spezialisierte Originalreceipts und Canonical schließen die echten Operationen, nicht eine Umdeutung dieser Platzhalter.

Die externe, gehashte Clientmessung bewahrt Argumente/Streams und unterscheidet direkte normale Exits von Signalen. 34 echte Curl-Start-/Abschlusspaare:16 Primärrequests +1 First-Byte +17 Readiness. Generischer Strict-Client: **normaler Exit52**, kein Signal, Invocation `669ba1b19fc340618d62148d715e5fc3`, ChildPID 10440; Rule 1100301, Phase 4, Strict-Abort. Curl-HTTP 000 und der bereits sichtbare Producer-HTTP 200 sind getrennte Beobachtungen. First-Byte-Writer: normaler Exit0, Invocation `1515086ec928494aafd0b0a0fceab107`, ChildPID 12514. Alle 16 vereinbarten direkten Programmreceipts über 11 Klassen haben normale Exits0. Keine Diagnoseauswertung ersetzt die Childmessung.

Tatsächlich 79 HTTP-Operationen ohne Readiness, einschließlich vier positiver Controls; 31 Ableitungen sind keine zusätzlichen Requests. 61 echte Root-Master/nobody-Worker-Lifecycles mit Cleanup,57 unterschiedliche frische root-owned direkte Projection-Kinder. Testsystem: Ubuntu 26.04.1 LTS, Kernel7.0.0-38, KVM; isolierte Loopback-Runtime. NGINX-Binary/Modul wurden für diesen Stand frisch gebaut; die Engine wurde identitätsgeprüft aus dem Cache wiederverwendet. 2589 finale Runtime-Prüfsummen geprüft, Exit0; Ledger-SHA256 `b79fbe3e2b7cf2806c8698f2a6fd7f1f1a4c4f06aed8075924311d4d1c27d97a`.

Qualität an U: 14 Curl-/8 Python-Messcontrols, 71 Fokus- und 61 Namespace-Tests ohne SKIPs bestanden. Tatsächliche CI22 SUCCESS/2 absichtliche H2/H3-SKIPs; frischer Sonar-GateOK, alle fünf Bedingungen bestanden. Zusätzlicher Produkt-ShellCheck:7 Warnungen/7 Infos unverändert. Vollständiger zusätzlicher lokaler Lint nicht erneut ausgeführt; historische16 Apache/MRTS-Diagnosen nicht erneut getestet. H2/H3-SKIP ist kein PASS.

Lokale Originale: `nginx-strict-client-full97-r17-20261010T193127Z` mit `postrun-v3/`, `operations-audit-r17.md` und Runtime-Ledger; dies sind keine öffentlichen Downloads. Der erste eingefrorene Analyzer-Exit1 bleibt erhalten: raw `phase4.log` wurde nach Allowlist-Normalisierung vertragsgemäß gescrubbt. Nur neue Read-only-Auswertungen v2/v3 folgen Original-Normalized-TX und Scrublog; Instrumente/Runtime-Originale unverändert. Historische R15/R16-Ergebnisse bleiben unverändert; R16 hatte noch die generische Abschlussmesslücke.

## Historische begrenzte Evidence — T

- readyAB: fünf echteH1Operationen, Driver/Supervisor 0/255.841s/runtime0/finalize1/validator0. Alle sieben A/B-IDs und acht historischeNE-Ableitungen einzelnOriginalPASS; OriginalCanonicalFAIL18PASS79NE97Required. Rootmaster5/nobodyWorker10/FreshProjections5/Cleanup5/59HashInodebindungen/311Ledgergültig.
- readyCD: vierOperationen (dreiNative + FirstByte, Readinessprobe separat), Driver/Supervisor 0/237.518s/nativeHost0/FirstByte0/runtime0/finalize1/validator0. SechsScopedIDsPASS, OriginalCanonicalFAIL8PASS89NE97Required. NativeMIME2 GET200/27Bytes; StrictH1.1chunked200/10428Bytes/incomplete_read/connection_aborted. Insgesamt vierRootmaster/fünfWorker/vierfrischeRootownedSymlinkfreieDirektprojections, nativeCleanupseparatverified,219Ledger0/taskHostLingering[]. GenerischeCounts nichtaufNativegesamtheitübertragen.
- CurrentFreshInputOffline C8+D16revalidation0/5.790s: H1/NativeAuthority/Canonicalevent/schema0, alle 24Mismatchkontrollenabgelehnt; OriginalBundle/fünfDocs/Statusunverändert. Keine neueRuntimeinvocation.
- invalid_size: gleicherRequiredRecord, echteUnknownDirective-Ablehnung des früher gültigen1048576, NGINX-t1/Driver0/70.97s/keinHTTP. Repositoryweite modsecurity_phase4_body_limit-API entfernt; keineAlias-/deprecatedRegistrierung. SecResponseBodyLimit/fourEngineLimitCases/independent1MiBDefaults/Hardcaps/Invalidmode/Overflowguard bleiben.

AB undCD **nicht zu Full97PASS vereinen**. Am historischen Stand T waren alle 97fresh_full97 NOTRUN/approvalrequired. AuditreadyAB/readyCD VERIFIED_BOUNDED_ONLY/errors[]/incomplete[]; RootfullreadonlyAudit0. AgentGuardedRawlogReadlimit ausdrücklich sichtbar; RootprüfteNativeReceipts und aktuelleLoader-/Hash-Inodebindungen separat.

## Historische Qualität, Evidence und Grenzen — T

GetesteteSourcebindungT: ParentnativeLint0/171.913s; cleanFrameworkfullLint604Tests 19Suites0SKIPExit0/1234.301s; cleanNoCRS4230SKIPExit0/188.042s; Namespace 610SKIPExit0/5.884s. CIParent 22SUCCESS2SKIP/Framework 11SUCCESS3advisorySKIP0pending; exactParentSonar 14:24:46 undFramework 14:23:39 GateOK/0OPEN-CONFIRMEDFindings. HostedCI nichtProtected. Die zweiParenteventgatedPreflightSKIPs beweisenkeinH2/H3; FrameworkOSV/Scorecard/fullhistorySecretScanAdvisorySKIPs sindkeineausgeführtenPASS.

SiebenNGINXauxiliaryund16Apache/MRTSParentShellCheck-Baselinediagnosen/Python3.14.7≠CI3.14.8 und zweiindependentlyreproduzierte113-Baselinetestfehler bleibenoffen, nichtunterdrückt. Historischeworkingtree604-Läufe nichtcleanCommitumetikettiert. FrühereFailedRuntime/Config137/V3adapter/Sonar 873twoFindings/HTTP 400-502/Vortex403 unverändert in vollständigemexternenBericht/OriginalReceipts erhalten; keineaktivenCheckpointbehauptungen daraus.

LokaleNachweise unter nginx-full97-followup-20261010T084822Z: removal-focus-audit/r14-ready-ab-v4/audit.json, r14-ready-cd-v4/audit.json; fresh-cd-revalidation-34127a6a/offline-revalidation.json; artifact-audit-r14-ready-ab/; namespace-quality-34127a6a/; r14-framework-final-readback.json/r14-parent-pre-docs-readback.json. LokalePfade sindkeineöffentlichenGitHubDownloads.

HistorischesR13 bleibt97Required=80CasePASS/9FAIL/8NE, plusviernestedSchemafehlerinzweiMIMEPASS; Make/Supervisor 2/Validator 1/CanonicalFAIL und79genuineRequests erhalten. Alle 80ControlsbleibenBasis, nichtneuFull97ausgeführt;19A-Dplusinvalid_sizeScopedRowsaktuell,77Controlsunverändert.

## Baseline

- [x] B0: Baseline-Revisionen, Branches/Gitlinks und erhaltenes R13 prüfen. Bindung R; Originalvergleich/Readback bestanden; kein Fix; `baseline-reconciliation.json`, `checks/baseline_pr396.log`, `checks/baseline_pr137.log`; nur historisch.
- [x] B1: Alle neun ursprünglichen FAIL-Records zuordnen. Bindung R; deterministischer Original-Matrix-/Resultat-Abgleich bestanden; kein Fix; `baseline-reconciliation.json`, `issue-record-matrix.csv`; kein neuer Runtime-Status.
- [x] B2: Alle acht ursprünglichen NOT_EXECUTED ihrer ersten fehlenden Grenze zuordnen. Bindung R; Original-Record-/Basis-Abgleich bestanden; kein Fix; derselbe Abgleich/dieselbe Matrix; explizite Ableitungen, keine pauschal fehlenden Driver.
- [x] B3: Vier verschachtelte Fehler zwei MIME-Allow-Case-PASS zuordnen. Bindung R; Original-JSON-/Schema-Pfade abgeglichen; kein Fix; `baseline-reconciliation.json`; zwei Cases, nicht vier zusätzliche Runtime-FAILs.

## A — Intervention

- [x] A1: Überschriebene Interventionsfolge reproduzieren. Bindung R als Arbeitsregression, an G bestätigt; `tests.test_no_crs_outcome_projection`, RED Exit1 / G-Gruppe Exit0; Fixes A+AF+S; `parent-ab/a-red.log`, `parent-quality-b4044d10/native-selection-snapshot-authority.log`; nur Unit-Evidence.
- [x] A2: Parent-Projector, überschriebene Entscheidungsfelder und Beobachtungszeitpunkt bestimmen. Bindungen R/G; Trace plus Abschluss-/technische Fehler-Tests an G bestanden; Fixes A+AF+S; A-Change-Record und dieselben Unit-Logs. Regel-/Phasen-/TX-gebundene Entscheidung bleibt getrennt vom späteren Lifecycle-Zustand; echte technische Fehler bleiben sichtbar.
- [x] A3: RED vor der Reparatur nachweisen. Bindung R als Arbeitstests; vier gültige Fehlerkontrollen, Exit1; Fix A; `parent-ab/a-red.log`. Ein ungültiges Nichtinterventions-Fixture wurde offen korrigiert; es zählt nicht als Produktdefekt.
- [x] A4: Minimale identitätsgebundene Reparatur implementieren. Bindung G; Parent-Outcome-/Collector-Regressionsgruppen Exit0; Fixes A+AF+S; `parent-quality-b4044d10/run-checks.sh`, `results.md`; keine Produkt-/Validator-/Required-Änderung.
- [x] A5: Positiv-, technische Fehler-, Cross-TX- und Prioritätskontrollen bestehen. Bindung G; Parent 345 einschließlich betroffener Normal- und positiver Fehlerpfade, Exit0; Fixes A+AF+S; `parent-quality-b4044d10/results.md`, `parent-sonar-followup/results.md`; keine globale nonzero=PASS-Regel oder technische Fehler-Vetos.
- [x] A6: Bindung T; echte vierA-Basisrequests/originalCanonicalPASS anP341/F9f. Root/nobody/Freshness/Cleanup/Artefakte311Ledgergültig; ready-AB-v4 VERIFIED_BOUNDED_ONLY. KeinFull97.
- [x] A7: Historische Bindung T341/9f integriert/clean/veröffentlicht, exakteGitlinksM8aunverändert. Historical Parent native302/FrameworkNoCRS423/fullLint60419/Namespace 61Exit0; echteA-BasisPASS. UrsprünglicheG/L-Belegebleibenhistorisch, keinFull97.
- [x] A8: Originalstatus an U/R17 bestätigt: alle 97 Required-PASS; unveränderte Verträge und echte Invocations, öffentliche R17-Referenz.

## B — First-Byte

- [x] B4: Invocation-/Zeit-/Countervertrag bestimmen. Bindungen R/G; Capture-vor-Release-Ordnungsregression an G bestanden; Fix B; `parent-ab/b-red.log`, B-Change-Record, `parent-quality-b4044d10/native-selection-snapshot-authority.log`. Snapshot wird bei pausiertem Upstream gemessen, nicht nach Response-Abschluss.
- [x] B5: Capture nach Release und fehlenden eindeutigen gebundenen Merge reproduzieren. Bindung R als Arbeitstests; RED Exit1; Fix B; `parent-ab/b-red.log`; historische/Test-Inputs, keine neuen Requests.
- [x] B6: Bindung korrigieren und Mismatchkontrollen erhalten. Bindung G; `tests.test_nginx_first_byte_binding` sowie Collector-/Framework-Suiten Exit0; Fixes B+S; `parent-quality-b4044d10/run-checks.sh`, `framework-quality-b4044d10/no-crs-suite.json`. Falsche Invocation/TX/Zeit, veralteter oder manipulierter Snapshot, doppeltes Event und passende Counter ohne Herkunft bleiben abgelehnt; spätere kumulative Counter bleiben erhalten.
- [x] B7: Bindung T; echter synchronisierter FirstByte, beideBoriginalCanonicalPASS; closed17Append/44RuleInterventionPaar, Snapshot/Order/identities/SafeAntwort geprüft. ready-AB-v4/errors[]/incomplete[], driver0; OriginalgesamtFAIL79fehlendeRequired bleibt. Nurbounded, keinFull97.
- [x] B8: Historische Bindung T; Frameworkpairing873+minimalQuality9f und Parentgitlink341 integriert, genuineAB/CDFirstByte/nobufferPASS, Legacy/MixedTXMismatchkontrollenundNoCRS4230. KeineRuleinjection/Eventmerge/Counterserialization/Guardabschwächung. B-PairingfixverändertApache nicht; repositoryweiteAPI-Entfernung änderteApache separat.
- [x] B9: An U/R17 bestätigt; synchronisierter First-Byte und direkt gemessener Writer-Exit0, keine nachträgliche Snapshot-Umdeutung.

## C — Native H1

- [x] C1: Reale Beobachtung → Operation/Receipt → Canonical-Protokoll/Event verfolgen. Bindung R als Input plus G-Verträge; originale native Bytes im ausdrücklich aktuellen Validator-Replay erneut geöffnet, Exit0; Fix C; `framework-cd/c-historical-replay-v3.log`, C-Change-Record. H1 wird aus beobachteter HTTP-Version11 und passender URI/TX/Case/Run/Phase/Rule abgeleitet, nie aus einem Environment-Default.
- [x] C2: Erste fehlende Canonical-Bindung reproduzieren. Bindung R als Arbeitsregression; C RED Exit1; Fix C; `framework-cd/c-red.log`, `baseline-reconciliation.json`; originale Runtime-Operation vorhanden, Canonical-Protokollfelder/Event fehlten.
- [x] C3: Strenge Bindung implementieren und Negativkontrollen erhalten. Bindung G; Framework 413 Exit0 und ausdrücklich historischer C-Replay Exit0; Fix C; `framework-quality-b4044d10/no-crs-suite.json`, `framework-cd/c-historical-replay-v3.log`. Falsches Protokoll/Invocation/TX/Case, fehlende Beobachtung, veralteter Receipt, falsches Modul/Bytes und Canonical-Manipulation bleiben abgelehnt; keine H1→H2/H3-Umetikettierung.
- [x] C4: Bindung T341/9f; echter readyCDStrictH1CasePASS/nativeHost0, freshretainedC8negative0/H1-Canonicalevent-Authorityreopened. Rootauditv4VERIFIED_BOUNDED_ONLY/219Ledger0/Cleanup/Freshness, nativeCaseIdentitätenseparat. KeinFull97.
- [x] C5: Historische Bindung T sauberintegriert/veröffentlicht, exakteGitlinksP341/F9f/M8a/RemoteOPEN-DRAFT, cleanNoCRS423/fullLint60419/CI-Sonar 0; genuineCD/retainedCnegativesbelegt, MRTSunverändert. KeineHistoryrewrite.
- [x] C6: An U/R17 bestätigt; echte native H1-Operationen und gebundene Originalreceipts, kein H2/H3-Nachweis.

## D — MIME

- [x] D1: Vier Schemafehler getrennt von zwei Case-PASS erfassen. Bindung R; exakte originale JSON-Pfade/Typ/Wert abgeglichen; kein Fix; `baseline-reconciliation.json`; ursprüngliches verschachteltes Action-Enum lehnte String `allow` ab.
- [x] D2: Reader/Normalizer → tatsächliche Aggregatprojektion → verschachteltes Schema verfolgen. Bindung R als Input und G-Tests; historischer tatsächlicher Gesamt-Producer-Replay schema-valid, Exit0, insgesamt weiter FAIL; Fix D; `framework-cd/d-historical-replay.log`, D-Change-Record; kein neues Runtime-Resultat.
- [x] D3: RED über tatsächliche dynamische Aggregation nachweisen. Bindung R als Arbeitstest; zwei Subtests reproduzieren vier Enumfehler, Exit1; Fix D; `framework-cd/d-red.log`; kein handgeschriebener Schema-only-Ersatz.
- [x] D4: Eng begründeten Schemavertrag implementieren. Bindung G; Framework 413 Exit0; Fix D; `framework-quality-b4044d10/no-crs-suite.json`, `framework-cd/d-green.log`. Nur die zwei exakten vorhandenen Case-/Resultat-Paare erlauben `allow/allow`, ohne Rule, späte Intervention oder Abort; Required-Felder, Geschlossenheit und reales null/completed-Transportverhalten bleiben erhalten. Acht Mismatchkontrollen pro MIME-Case bleiben negativ.
- [x] D5: BindungT341/9f; beideechtenreadyCDMIMECasePASS, frischesAggregateSchemaErrors[]/Validator 0, currentfreshD16negatives0. OriginalCanonicalFAIL8PASS89NEbleibt. Evidence currentCDauditv4/freshOfflineJSON, nurbounded.
- [x] D6: Historische Bindung TSchema/Producer/sourceHashesundGitlinksgebunden, cleanNoCRS423/fullLint60419/CI0 und echteMIME+freshD16negatives0. HistorischevierSchemafehler inzweiCasePASSunverändert.
- [x] D7: Gesamtes frisches U/R17-Aggregat validiert: Schemafehlerliste leer, originaler Validator-Exit0.

## E — Derivations

- [x] E1: Jeden Record seiner ersten blockierten Grenze zuordnen. Bindung R; originaler deterministischer Basis-/Record-Abgleich bestanden; kein Fix; `baseline-reconciliation.json`, `issue-record-matrix.csv`; exakte Zuordnung unten.
- [x] E2: A–D-Abhängigkeiten von unabhängigen Ursachen unterscheiden. Bindungen R/G; geschlossene Ableitungs-/Selection-Verträge und Framework 413 Exit0; Fixes A+AF+B+C+D+I soweit zutreffend; dieselbe Matrix und `framework-quality-b4044d10/no-crs-suite.json`; kein unnötiger neuer Driver oder erfundene Evidence.
- [x] E3: Bindung T; alle acht historischenNE-Ableitungen einzeln neuerreadyABCanonicalPASS anP341/F9f, keineExtraRequests/synthetischeEvidence. OriginalABCanonicalFAIL/79NEweiteroffen; keinFull97.
- [x] E4: Alle 97 frischen Originalstatus an U/R17 gemessen:97 PASS;31 explizite Ableitungen, keine 31 zusätzlichen Requests.

## Q — Quality / integration

- [x] Q1: Aktuelle Bindung U: 14 Curl-/8 Python-Messcontrols, 71 Fokustests und 61 Namespace-Tests ohne SKIPs bestanden. Historische G/L/T-Suiten bleiben separat gebunden.
- [x] Q2: Aktuelle Bindung U: verpflichtende CI-Lint-/Docs-/Contracts-Prüfungen erfolgreich; zusätzliche lokale Voll-Lint-Wiederholung nicht ausgeführt. ShellCheck 7 Warnungen/7 Infos unverändert; 16 historische Apache/MRTS-Diagnosen nicht erneut getestet. Dokumentationsnachfolger benötigt eigene Checks.
- [x] Q3: Runtime-getesteter Head U=2f02370b07149265841411894f1a2cf7f1e978ff; Gitlinks F9f/M8a unverändert. Framework PR137 CLOSED/MERGED, Pin bleibt9f. Späterer Dokumentations-Head/Readback separat, kein geerbter Runtime-PASS.
- [x] Q4: Exakte getestete Bindung U: 22 CI SUCCESS/2 absichtliche H2/H3-SKIPs; frischer Sonar-GateOK/alle fünf Bedingungen bestanden. Eigene CI des Dokumentationsnachfolgers separat auswerten; Hosted CI nicht Protected.
- [ ] Q5: Bei der Dokumentationsvorbereitung standen finale EN/DE-Prüfung, Veröffentlichung und Remote-Readback noch aus. Tatsächlichen Abschluss dieses Punkts und Ready-Übergang anhand öffentlicher Delivery-/PR-Metadaten prüfen; kein zukünftiger Status wird hier vorweggenommen.

## F — Full97

- [x] F1: Explizite Freigabe für genau einen neuen lokalen Standard-Full97 erhalten; Attachment f3e597f0.
- [x] F2: Einzigen neuen Standard-Full97 auf eingefrorenem U-Tupel ausgeführt: Make/Supervisor 0,554.091s.
- [x] F3: Ganzes frisches Aggregatschema durch originalen Framework-Validator geprüft: Exit0, Fehlerliste leer.
- [x] F4: Alle 97 unveränderten Required-Records mit echter, identitätsgebundener Evidence PASS.
- [x] F5: Canonical PASS; tatsächliche Lifecycle-/Supervisor-/Collector-/Writer-/Validator-Abschlüsse gemessen. Beim generischen Strict wurde unter der konkreten Strict-Abbruch-Oracle normaler Exit52 gemessen; 52 ist eine Beobachtung, keine erforderliche numerische Vertragsvorgabe oder globale nonzero=PASS-Regel.
- [x] F6: 61 Lifecycle-Cleanups und 57 frische Projection-Kinder bestätigt; 2589 finale Runtime-Prüfsummen, CheckExit0.

## P — Protected

- [ ] P1: Trusted Base unabhängig freigeben.
- [ ] P2: Zulässige Basis-/Gitlink-/Workflow-Bindung prüfen.
- [ ] P3: Runner und Environment administrativ freigeben.
- [ ] P4: Exact-Base-Host-Gate prüfen.
- [ ] P5: Zulässigen geschützten Lauf erst nach diesen Voraussetzungen starten/auswerten.

## Record-Status — historisches T und aktueller Full97 U

Alle folgenden Zeilen haben jetzt originalen Full97-PASS an U/R17; die Tabelle bewahrt historische R13-Status und frühere T-Evidence. Die historische issue-record-matrix.csv wird nicht umetikettiert; aktuelles postrun-v3/required-records97.json ordnet alle 97 echten Records zu. Ableitungen sind keine zusätzlichen Requests.

| Record ID | Historischer R13 | Historische begrenzte T-Evidence |
| --- | --- | --- |
| phase3_deny_before_commit | FAIL | readyAB A-Request |
| phase3_redirect_before_commit | FAIL | readyAB A-Request |
| phase4_deny_after_commit_log_only | FAIL | readyAB A-Request |
| phase4_deny_after_commit_abort | FAIL | readyAB A-Request |
| phase4_deny_after_commit_log_only_safe | FAIL | readyAB explizite Safe-Basisableitung |
| phase4_rule_observed | FAIL | readyAB/readyCD echter FirstByte-Rule-Beleg |
| phase4_no_full_response_buffering | FAIL | readyAB/readyCD FirstByte |
| phase4_first_byte_before_response_end | FAIL | readyAB/readyCD FirstByte |
| phase4_strict_http1_client_abort | FAIL | readyCD tatsächliches Strict-H1 |
| phase4_event_contains_original_status | NOT_EXECUTED | readyAB explizite A-Basisableitung |
| phase4_event_contains_late_intervention_action | NOT_EXECUTED | readyAB explizite A-Basisableitung |
| event_has_no_response_body_payload | NOT_EXECUTED | readyAB explizite A/B-Basisableitung |
| phase3_original_and_visible_status | NOT_EXECUTED | readyAB explizite A-Basisableitung |
| phase4_deny_after_commit_abort_strict | NOT_EXECUTED | readyAB explizite A-Basisableitung |
| phase4_status_metadata | NOT_EXECUTED | readyAB explizite A-Basisableitung |
| phase4_action_metadata | NOT_EXECUTED | readyAB explizite A-Basisableitung |
| phase4_no_payload_event | NOT_EXECUTED | readyAB explizite A/B-Basisableitung |
| phase4_out_of_scope_content_type | CasePASS; zwei Schemafehler | readyCD echtes MIME; schemavalid |
| phase4_missing_content_type | CasePASS; zwei Schemafehler | readyCD echtes MIME; schemavalid |
| invalid_size | PASS; alter API-Vertrag | echter Removed-API-Configtest |

## Abschlussgrenze

R17 lokaler Full97: **PASS**, gemäß eingefrorener lokaler Abnahmeliste und öffentlichem R17-Bericht. Kein zweiter Full97 ausgeführt oder neu freigegeben. Protected **BLOCKED / NOT RUN**: unabhängige Trusted-Base-/Runner-/Host-Gate-Voraussetzungen separat; kein Candidate-Prüfer als Trusted Root-Prüfer. PR #396: Bei der Dokumentationsvorbereitung waren Ready-Übergang und Dokumentationsnachfolger noch Root-Aufgaben; tatsächlicher Abschluss steht in öffentlichen Delivery-/PR-Metadaten. PR #382 bleibt OPEN/DRAFT, I09–I12 offen. Kein Merge, Retarget, Protected-Dispatch oder allgemeiner All-Profile-PASS.
