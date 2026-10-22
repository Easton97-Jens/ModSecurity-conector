# Change Record: CR-20261015-i12-envoy-host-evidence

**Sprache:** [English](CR-20261015-i12-envoy-host-evidence.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261015-i12-envoy-host-evidence |
| Datum (UTC) | 2026-10-15 |
| Basis-Revision | `76672071c3f7665dfde3340bef9e64271d6f6e70` |
| Historische Quellrevision der nativen/Hostevidenz | `f27eb59b53beff6f65384fc2e5037881a3052c01` |
| Letzte Quellrevision der Envoy-Runtimeevidenz | `afaf6305bd55646073c3b40632b52fc4e5edf714` |

## Motivation und Problemstellung

Das ursprüngliche Envoy-Ledger enthält 284 IDs für ext_proc, Request-Autorisierung und Response-Companion. Drei bestehende Lifecycle-PASS lösen nur drei der 125 ursprünglich offenen Oracles auf. Hostwirkungen bleiben von Unit-/Build-Ergebnissen und reinen Konfigurations-PASS getrennt.

## Akzeptanzkriterien

Alle Original-IDs/Oracles und gepatchten Go-/x/net-Eingaben erhalten; echte isolierte Hostproben sowie native/Go/Race/Vet-Kontrollen ausführen; physische Evidenz binden und jede Route getrennt berichten. Die vollständige Originalfall-Abnahme bleibt unerfüllt: 118 ursprüngliche Oracles bleiben nach vier neuen qualifizierten ext_proc-Original-IDs offen; die erhaltene zentrale Baseline bleibt unverändert.

## Implementierungsentscheidung und Begründung

Nur Envoy-spezifische I12-Producer/-Tests und eigene EN/DE-Berichte ergänzen. Unveränderte envoy-Capture-Registry und gemeinsamen Observer in einer Git-freien Quellkopie nutzen. Binary-/Quell-/SDK-Zuordnung prüfen. Begonnene/abgebrochene Backendrequests getrennt zählen; TCP-Resets und fehlenden gRPC-Status erhalten. Den positiv identifizierten PID-Namespace in der reinen Envoy-Controllerkopie bis nach Cleanup offen halten, mit Identitätsprüfung vor/nach Open und fail-closed Fallback. Ursprüngliche Controllerprüfungen und alle Fehlversuche erhalten.

## Geänderte Dateien

Neue reine Envoy-Dateien unter `ci/runtime/lifecycle/i12/envoy/`: native Vorbereitung, Original-Ledger-Abgleich, Hostfixture-Vorbereitung/-Runner, Transportklassifikation, physischer Reviewer, Berichtsproducer, Tests und EN/DE-README. Eigenes Berichtspaar und exaktes ID-JSON: `reports/testing/i12-envoy-host-evidence-20261015.*`. Parent-Discovery-Wrapper: `tests/test_i12_envoy_evidence.py`. Dieses EN/DE-Change-Record-Paar. Im Task-Diff gegen die Base bleiben gemeinsame Manifeste/Generatoren, Produktdateien, andere Connectoren, Dependencies und Gitlinks unverändert.

## Ausgeführte Befehle

Alle Shell-Einstiegspunkte nutzten RTK. Die exakten afaf-Native-/CGo-Build-, vollständigen Go-Test-, Race- und Vet-Argv/Ergebnisse/Loghashes liegen in `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/current-base-afaf-native-v3/native-build/receipt.json`; alle 16 Schritte enden mit Exit 0. `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_i12_envoy_evidence`: 257 PASS, 0 Skips; aktuelle Rohlogs und die Hashes aller 31 Python-Eingaben (30 Envoy-Quellen und Parent-Discovery-Wrapper) sind in `ci/final-envoy-controls-257-sonar-v2.json` gebunden. Die fokussierten Fehlerproben-Kontrollen haben 16 PASS; die separaten Go-Testproxy-Kontrollen 10 PASS. Die aktuelle Capture-Registry prüft 155 Objekte/10 Profile; die nativen Observer-Kontrollen bestehen 34 Tests. Hostkommandos und Nicht-Null-Exits bleiben in der jeweiligen Batch-runs.json; sie werden nicht zu PASS normalisiert.

## Security-Auswirkung

Die CI-Korrektur schließt unbegrenzte CLI-/JSON-Dateizugriffe in den Envoy-Evidenzlesern. Erlaubte Roots werden vor dem Dateizugriff geprüft; Verzeichnisdeskriptoren, O_NOFOLLOW, Eigentümer-/Rechteprüfung, Bytegrenzen und stabile Dateiidentität schützen das Lesen. Ausgaben werden privat und exklusiv erzeugt; Git-Metadatenargumente erfordern exakte SHAs und festen Umfang. Die aktuelle vollständig ausgeführte Envoy-Suite hat 257 PASS und 0 Skips. Der neue Leser ist in frisch reproduzierten, einzeln freigegebenen Paketen hashgebunden; alte Pakete und rohe Hostläufe bleiben erhalten. Der erste CI-Lauf für Head `d91891fd0e19826d6f09a426daa289dafea9f598` endete mit 21 erfolgreichen, zwei übersprungenen und einer fehlgeschlagenen scaffold-lint-Prüfung. Das SonarCloud Quality Gate bestand; das separate Zero-New-Gate meldete 44 Maintainability-Anmerkungen. Envoy-lokale Refactorings bearbeiten diese Anmerkungen; das endgültige CI-Ergebnis des aktuellen Heads bleibt im Draft-PR417 verfolgt. Regeln, Ausschlüsse, Befunddispositionen und Quality Gate bleiben unverändert.


Synthetische Unit-Fixtures verwenden unabhängig abgegrenzten Temporärspeicher,
damit Hosted-Runner-Pfade die Capture-Wurzel dieses Rechners nicht voraussetzen.
Drei Kontrollen vor der Korrektur scheitern bei fehlender Wurzel; alle 95 ursprünglichen
Portabilitätskontrollen bestehen mit fehlenden Produktionswurzeln und in der
normalen Umgebung. Echte Capture-Containment- und Listener-/Privilegienprüfungen
bleiben unverändert. Receipts: `ci-portability-before.json`,
`ci-portability-controls.json`, `final-envoy-controls-portable.json`.

Keine Produktdefaults, Authentifizierung, Validierung, Compilerwarnungen, Listenerberechtigungen oder Dependency-Pins werden abgeschwächt. Tatsächliche Kandidaten laufen mit UID/GID65534, Capabilities0 und NoNewPrivs1 in privaten Namespaces. Der Namespace-FD verhindert Fehlzuordnung durch Inode-Wiederverwendung bei erhaltenen Ownership-Prüfungen. Kein fremder Prozess wurde signalisiert. Generierte Berichtsmetadaten schließen Payloads, opaque Leases, private Schlüssel, Caches und Binaries aus.

Alle 125 Original-Oracles haben einzelne physisch geprüfte Quellreviews. 33 neue konkrete Fixture-/Erwartungsvorschläge (14/10/9) bleiben von kanonischer Auflösung und Lifecycle-PASS getrennt. Die gesamte Buildquellinventur (2.105 Dateien), Fall-/Routen-/Parent-Bindung sowie der begrenzte äußere Timeout mit bytegenauen Teillogs sind zusätzlich geprüft.

Die Fortsetzung am 18. Oktober 2026 nutzt ausschließlich den vertrauenswürdig exportierten konfigurierten Speicherpfad und verweigert fehlende Konfiguration. Alle 84 alten physischen Reviewausgaben, 34 Fixtureausgaben und die normierte Inventur aller 125 Original-Oracles bleiben exakt gleich. Ein Negativtest reproduzierte einen Refactorfehler bei doppelten Binärdateinamen; jeder ursprüngliche Belegeintrag wird wieder einzeln geprüft. Belege: `ci/resume-final-controls.json`, `ci/review-final-physical-parity.json`, `ci/owned-refactor-parity.json`.

Das neue Companion-Supplement erhielt vor dem Hoststart eine physische Prüfung aller 17 Referenzen und erhält Original-/Effective-/Source-Semantik. Ein erster Controller-Exit 77 erfolgte vor Hoststart, weil 1 GiB registrierte Schätzung unter dem unveränderten 2 GiB-Outputlimit lag. Die offizielle Registrierung wurde auf 3 GiB korrigiert; ursprüngliche Registrierung und Fehlversuch bleiben erhalten. Der echte Wiederholungslauf endet mit Controller 0 / Client 0, ohne Survivors oder Mountleaks. Native Quelle bleibt ausdrücklich `f27eb59…`; der inzwischen fortgeschrittene Parent wird dadurch nicht qualifiziert.

## Runtime-Evidence

Tatsächliche Envoy1.39.1-, SDK3.0.14- und Go1.27.2-Lade-/Buildidentitäten, Client-/Backend-Wire-/Bodyhashes, P1–P4, Bodychunks/EOS, natives Logging/Free, Runtime-/Common-Finish-Zähler, physische Events und Cleanup-Receipts liegen unter `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015`. Eigener EN/DE-Bericht und exaktes ID-JSON erhalten jeden gemessenen Batch und Originalfall. Runner-Exit0 ist keine Lifecycle-Abnahme; Exit77 und unbekannte Beobachtungen bleiben explizit.

86 echte Hostmessungen umfassen 37 Retakes unter 33 exakten Original-IDs. Vier einzelne Root-Freigaben in `root-approved-originals-v14` nach frischer Reproduktion aller 35 Nachweiskategorien qualifizieren die folgenden exakten ext_proc-Original-IDs; drei vorher bestehende Lifecycle-PASS bleiben erhalten:

- `I12::envoy-ext-proc::NEED-request-streaming`
- `I12::envoy-ext-proc::NEED-response-streaming`
- `I12::envoy-ext-proc::NEED-client-response-bytes`
- `I12::envoy-ext-proc::NEED-client-exit-signal`

Die erhaltenen Baseline-PASS sind `I12::envoy-ext-proc::NEED-request-eos-once`, `I12::envoy-ext-authz-request::NEED-request-eos-once` und `I12::envoy-ext-authz-response-companion::NEED-lease-claim`.

Die drei früheren Request-Autorisierungsfreigaben (`I12::envoy-ext-authz-request::NEED-complete-sample`, `I12::envoy-ext-authz-request::NEED-request-multiple-chunks`, `I12::envoy-ext-authz-request::NEED-client-response-bytes`) und die frühere Companion-Freigabe (`I12::envoy-ext-authz-response-companion::NEED-allow`) sind zurückgenommen. Sichtbare `grpc-status:0`-Trailer besitzen keine bewiesene Zuordnung zum Authorization-Stream. Der strikte Parser erfasst deshalb den Remote-Status als unbekannt und erfolgreichen Abschluss als false; passende HTTP-/native Messungen belegen nicht den vollständigen Routenvertrag.

Der physische Request-Trace identifiziert weiterhin Worker 285 / CID1 / SID6459190741822168578 und Hostfragmente 64+31=95 mit anschließendem EOS, danach Authorization Check in Zeile 275. Die Engine erhält ein vollständiges natives 95-Byte-Sample und ein EOS; mehrere Client-Schreibvorgänge bedeuten keine mehreren nativen Callbacks. Rohes HTTP-Framing und Entitybytes bleiben unabhängige Beobachtungen. `max_request_bytes` ist eine Hostbuffer-Grenze und keine WAF-Inspection-Grenze des Connectors. Host-413 vor Engine-Eintritt, native Body-Limit-Entscheidung Reject/ProcessPartial, gültige Regelintervention und technisches gRPC-/Runtimeversagen behalten getrennte Evidenzpflichten.

Der zusätzliche Companion-Retake belegt zwei früh erfasste Backendrequests, Ziel 1 / Nachbar 1, Request 95 / Response 96 und Responsecallbacks 64+32+0/EOS. Lease-Claim, P1–P4, Logging, RuntimeFinish, NativeFree und Cleanup sind physisch belegt; die getrennte Request-Leg erhält daraus keinen weiteren PASS. Physischer lokaler HTTP/2-Reset 2 bleibt getrennt vom unbekannten Remote-gRPC-Status.


Der exakte Base-Head `a62296fb57263f9be18c6ac879e36e0ab2a9935c` wurde in `dfb1a07a863530a53c0006ee204319453d66a2ad` in diesen Branch gemergt. Die erhaltene Baseline und die physischen Quellen wurden mit den aktuellen zentralen Validatoren erneut geprüft; dieser Envoy-Task änderte keinen gemeinsamen Validator. Die historische native und Hostevidenz bleibt auf `f27eb59…` begrenzt. Frische native und Host-Captures der aktuellen Base sind unten getrennt gebunden und ergeben keine weitere Originalfall-Abnahme. Mit der Fixture aus `fault_scenarios.py` und dem separaten Go-Testproxy wurde die echte, begrenzte ext_proc-Response-EOS-Fehlerprobe `fault-host-v1` ausgeführt. Ihr Runner77/Controller1/Client1 bleibt unqualifiziert; neue PASS: 0.
Die Probe verwirft nur den leeren Response-EOS-Callback und führt einen echten Half-Close aus. Engine-API und eindeutig zugeordneter Envoy-Zielstream melden gRPC-Status14. Der Zielclient empfängt HTTP200 mit einem Präfix von 96 Bodybytes in 64+32 ohne abschließenden Nullchunk. P1–P3 sind beobachtet, P4=0; der `runtime_finish`-Versuch hat Result0 und wird nicht als erfolgreicher Finish gewertet. Logging/Free/Cleanup sind jeweils1. Der gesunde Nachbar erreicht P1–P4/Finish jeweils1. Keine Survivors oder Mountleaks bleiben zurück. Der Proxy-Wirestatus ist unbeobachtet; daraus wird kein erfolgreicher Streamabschluss abgeleitet.

## Historische ergänzende a622-Evidenz

`current-base-evidence-v1.json` bindet getrennt Quelle `a62296fb57263f9be18c6ac879e36e0ab2a9935c`, die finale `current-base-a622-native-v3/native-build/receipt.json` und `current-base-a622-host-v3/physical-review.json`. Alle 2.179 aktuellen Buildquelleinträge, Binaries, geladenen Images und physischen Receipts sind geprüft. Der isolierte Engine-Build verwendet exakt Go1.27.2 für Treiber, Compiler und Linker mit dem GOROOT der Task-Toolchain; das auf dem Host installierte Go1.27.3 ist eine getrennte Umgebungsmessung. SDK3.0.14 und Envoy1.39.1 sind physisch identifiziert. Native/CGo/Go/Race/Vet-Prüfungen und 34 gemeinsame native Observer-Kontrollen bestehen; 16/16 native Vorbereitungsschritte enden mit Exit0.

Drei frische echte Streamingproben enden jeweils mit Runner/Controller0, ohne Survivors, Mountleaks oder offene Observer-Scopes. Jede Route beobachtet Ziel-Request/-Response 95/96 Bytes, Nachbar 6/7 Bytes und zwei vollständige Backendrequests. Die Beobachtungen bleiben nach Route getrennt:

- `envoy-ext-proc`: zwei native Transaktionsscopes; Requestcallbacks 64+31+0/EOS und Responsecallbacks 64+32+0/EOS; P1–P4, Runtime-Finish, Logging, natives Cleanup/Destroy sowie physische Event-/Cleanup-Receipts sind gebunden. Zwei idempotente Common-Finish-Aufrufe erzeugen je Transaktion einen Completed-Übergang. Ziel und Nachbar haben vollständige HTTP-Entities und TCP-EOF. Lokaler Process-Reset2 ist beobachtet; der Remote-Process-Status bleibt unbekannt.
- `envoy-ext-authz-request`: Der Host empfängt mehrere Requestfragmente, während die Engine ein vollständiges begrenztes 95-Byte-Sample mit EOS erhält. Native Requestverarbeitung und tatsächliche Client-/Backendwirkung sind unabhängig gebunden. Ziel und Nachbar haben vollständige HTTP-Entities und TCP-EOF. Unmarkierte Authorization-Trailer lassen den Remote-Status unbekannt und erfolgreichen Abschluss false; der Ziel-Process-Scope bleibt unbekannt, während beim Nachbarn lokaler Reset2 beobachtet ist. Diese Streamingprobe allein belegt keinen Host-Reject, keine nativen Limitentscheidungen und keine Regelinterventionen.
- `envoy-ext-authz-response-companion`: Korrelierte native Lease-/Responseevents, P3/P4, Responsecallbacks 64+32+0/EOS, Finish/Free und Cleanup besitzen physische Evidenz. P3 endet vor dem Common-Commit, der vor Response-Bodycallbacks und P4 liegt; dies ist Adapterreihenfolge, kein Kernel-Sendezeitstempel. Das Ziel empfängt die vollständige HTTP-Entity und anschließend TCP-Reset errno104; der Nachbar erreicht TCP-EOF. Ziel-Process-Scope und Remote-Status bleiben unbekannt; beim Nachbarn ist lokaler Reset2 beobachtet. Fehlende/abgelaufene Leases, Observer-/gRPC-Abbruch und Erhalt der ersten Fehlerursache benötigen weiterhin eigene vollständig qualifizierte Originalfall-Nachweise. Keine geteilte HTTP-Receipt qualifiziert beide Routen-Legs unabhängig, und keine P4-Strict-Fähigkeit wird abgeleitet.

Alle nicht zugeordneten Authorization-Trailer bleiben unbekannt und erfolgreicher Abschluss false; kein fehlender Process-grpc-status wird als Erfolg interpretiert. Diese ergänzenden Proben ordnen keine Original-ID zu und ergänzen `new_lifecycle_pass=0`. Der frühere Go1.27.3-Engine-Build in `current-base-a622-native-v1` und seine Proben in `current-base-a622-host-v2` bleiben abgelöst. Die Admission-Fehler aus `current-base-a622-host-v1` behalten Exit77, unbekannte Hostausführung und keinen Cleanup-Nachweis. Der verworfene `current-base-a622-native-v2` scheiterte vor Hoststart mit `compile: version "go1.27.3" does not match go tool version "go1.27.2"`; seine Receipt/Stderr der gemischten Toolchain bleiben gebunden. Der finale v3-Build isoliert GOROOT ausdrücklich und belegt alle drei Toolidentitäten. Historische Fallzahlen und Originalfall-Abnahmen werden durch diese ergänzenden Messungen nicht erhöht.

## Ergänzende afaf-Evidenz der aktuellen Base

Normale Merges erhalten die nachfolgenden Base-Heads `e4c872cde16eb73182de49c09a8ba8ee4219b417` und `afaf6305bd55646073c3b40632b52fc4e5edf714`. `current-base-e4-evidence-v2-sonar.json` erhält den bestandenen nativen e4-Build, den ersten ext_proc-Timeout und den erfolgreichen Host-Retake. `current-base-afaf-evidence-v3-sonar.json` bindet dieses vorherige Supplement an frische native und Host-Receipts für afaf; es erhöht keine Original-ID-Abnahme oder Oracle-Fortschritte. Die afaf-Änderung des gemeinsamen Manifests stammt aus der Base; dieser Task ändert weder gemeinsames Manifest noch Produktquellen. Der Envoy-lokale Quelladapter prüft die aktuelle Registry mit 155 Objekten/10 Profilen und rekonstruiert die historische e4-Registry aus exakten physischen Quellankern.

Die Delivery-Base rückte danach durch einen normalen Merge auf `76672071c3f7665dfde3340bef9e64271d6f6e70` vor. Das geerbte Delta von afaf zu 766 ändert ausschließlich zwei Parent-Testfixtures und deren eigenen EN/DE-Change-Record. Envoy-, Produkt-Runtime-, Capture-, Dependency- und Buildeingaben bleiben unverändert; afaf bleibt damit die letzte Quellrevision echter nativer Envoy-/Hostevidenz. 766 erhält keine neue Hostausführung, keinen Lifecycle-PASS und keinen Oracle-Fortschritt.

`current-base-afaf-native-v3/native-build/receipt.json` hat 16/16 Schritte mit Exit0, einschließlich Native/CGo/Go, Race, Vet und Observer-Kontrollen. Treiber/Compiler/Linker verwenden Go1.27.2; die Hostprobe meldet das installierte Go1.27.3 getrennt. SDK3.0.14, Envoy1.39.1, geladene Images, Binaries und alle 2.196 Buildquelleinträge sind physisch geprüft. Frühere technische Build-/Admission-Fehler bleiben erfasst. Alle drei Runner-/Controllerläufe in `current-base-afaf-host-v2` enden nach den erhaltenen host-v1-Admission-Fehlern mit Exit0. Jede Route erfasst Zielrequest/-response 95/96 Bytes, Nachbar 6/7 Bytes, exakt zwei Backendrequests und physisches Finish/Free/Cleanup ohne verbleibende Taskprozesse oder Mountleaks. UID/GID65534, Capabilities0, NoNewPrivs1 und Namespace-/Listenergrenzen bleiben erhalten.

- `envoy-ext-proc`: P1–P4, native Request-Callbacks 64/31/0-EOS und Response-Callbacks 64/32/0-EOS, getrennte Scopes für Ziel/sequenziellen Nachbarn und Finish/Logging/Free/Common-Cleanup jeweils zweimal. Lokaler Process-reset2 bleibt von fehlendem Remote-gRPC-Status getrennt. Der beobachtete text/plain;charset=utf-8-Header belegt keine unabhängige native MIME-/Charset-Auswahl. Diese Allow-Probe belegt weder Reject/ProcessPartial noch Cancellation oder gezielt fehlende/wiederholte Callbacks.
- `envoy-ext-authz-request`: Client-Schreibvorgänge 32/32/31 werden zu einem vollständigen nativen 95-Byte-Sample mit EOS unter Host-max_request_bytes4096/allow_partial_message=false. Der Hostbuffer-Vertrag bleibt von nativen Inspection-Limits getrennt. Kein Host-Reject, keine native Body-Limit-Entscheidung, gültige Regelintervention oder technisches Runtimeversagen wird ausgelöst. Nicht zugeordnete Status0-Trailer belegen keinen Authorization-Abschluss.
- `envoy-ext-authz-response-companion`: Lease-Ausgabe/angenommener Claim/P3/P4 sind in zwei getrennten Scopes allocationsgebunden; Wire-Token-Gleichheit bleibt unbelegt. P3 liegt vor Commit und Response-Callbacks 64/32/0-EOS/P4 folgen dem Commit. Das erste Client-Entitybyte liegt vor P4; P4 Strict wird deshalb nicht behauptet. Process hat lokalen reset2; zugeordnete Remote-Process-/Authorization-Status fehlen weiterhin. Fehlende/abgelaufene Leases, Observer-/gRPC-Abbruch und die erste technische Fehlerursache erfordern eigene qualifizierte Fälle.

Alle fehlenden oder nicht zugeordneten Remote-gRPC-Status bleiben unbekannt mit erfolgreichem Abschluss false. `new_lifecycle_pass=0`; die strikten 7 Lifecycle-PASS/118 offen, 86 historischen Hostmessungen und 37 Retakes für 33 IDs bleiben unverändert. Begrenzte TAC1-/DrayTek-Blue-Verifikation gilt; ein tieferer Security-Scan wird nicht abgeleitet.

## Bekannte Einschränkungen

Ergebnis PARTIAL. Die geforderte vollständige Hostabnahme aller 284 Originalfälle ist nicht belegt. Aktuelle Lifecycle-PASS sind insgesamt 7: 5/1/1 für 117/94/73 Original-IDs; Konfigurations-PASS 0/8/0; offene ursprüngliche Oracles 46/39/33, insgesamt 118. Von 277 IDs ohne vollständige Lifecycle-Abnahme sind 8 reine Konfigurations-PASS und 269 unqualifiziert. Direkte native MIME-/Charset-Auswahl, vollständig korrelierter paralleler gRPC-Terminalstatus, die vollständige Abnahme gezielt fehlender/wiederholter Callbacks über die einzelne Response-EOS-Fehlerprobe hinaus, alle physischen Event-Sink-Fehler, vollständiger Observer-Stop/Restart und Strict-P4-Fähigkeitsabnahme bleiben unvollständig.

## Verbleibende Risiken

Synthetische Proben haben eigene IDs; keine geteilte HTTP-Receipt überträgt Request-Abnahme auf den Companion. Fehlender Remote-grpc-status ist niemals erfolgreicher Abschluss. Frühere Client-TLS-/TCP-Abschlussbehandlung verdeckte ansonsten vollständige HTTP-Antworten; Wiederholungen erhalten beide Ebenen. Ein alter Controller77 ordnete einen fremden Traefik-Prozess falsch zu; Namespace-Inode-Wiederverwendung ist die abgeleitete Ursache. Der ursprüngliche Fehler bleibt mit einer frischen begrenzten Namespace-Pin-Wiederholung erhalten.

## Nicht ausgeführte Prüfungen mit Begründung

Vollständiges `rtk proxy make check-bilingual-docs PYTHON=/root/git/ModSecurity-conector/.venv/bin/python` endete mit Exit2, weil dieser isolierte Worktree22 unveränderte fehlende Links in den nicht initialisierten Framework-Gitlink hat. Alle Parent-Bilingual-Verträge ohne globale Linkprüfung und jeder Link neuer Dokumente bestanden die begrenzte Checker-API; `ci/docs-sonar-v2.json` hält dieses begrenzte Ergebnis fest. Kein Framework-Checkout, Gitlink oder Baseline-Dokument wurde geändert. Keine Master-Integration und kein Master-Merge. Vollständige 284-Fall-/Original-Oracle-Abnahme und die oben verbleibenden Hostfähigkeiten werden nicht behauptet. Keine breite Framework-/MRTS-Matrix, kein Lauf anderer Connectoren und keine fremde Produktänderung war autorisiert. Hosted-CI- und Quality-Gate-Ergebnisse des aktuellen Heads werden im Draft-PR verfolgt; lokale Ergebnisse belegen keinen CI-Erfolg.

## Finaler Diff- und Review-Status

Begrenztes statisches Review erkannte und korrigierte die auf den Zielrequest begrenzte P3-Regel, alte Quellidentitäten, Build-/Binary-Bindung, native Fixture-Syntax, partielle Backendzähler und Namespace-Lifetime-Rennen. Physisches Evidenzreview erhält Fehler. Lieferung zielt auf `codex/i12-envoy-410-20261015` gegen `work/pr382-i12-host-evidence-20261011`; kein Force-Push oder Master-Merge ist autorisiert. Abschluss bleibt bis zu den genannten Originalfall-Evidenzlücken partiell.
