# Change Record: Behebung der CSV-Sicherheitsbefunde

**Sprache:** [English](CR-20260721-csv-security-findings-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260721-csv-security-findings-remediation |
| Datum (UTC) | 2026-07-21 |
| Basis-Revision | 5fa90474a79eaee2df034bf1c4389572fdcca42f |
| Grenze | Nur Parent-Quellcode, Parent-Tests, Parent-CI/Runtime-Werkzeuge, Parent-Dokumentation und dieses Change-Record/Index-Paar. Der Branch übernimmt den aktuellen Framework-Gitlink von Parent-master, aber diese Aufgabe verändert weder Framework noch MRTS. |
| Finding-Verknüpfung | Importierte Codex-Security-CSV-Zeilen CSV-01 bis CSV-19; task-owned SonarQube-Cloud-S5443-Follow-up FND-SONAR-0010. |

## Motivation und Problemstellung

Die bereitgestellte Codex-Security-Zusammenfassung enthält 19 Befunde zu
bereits vorhandenen Behebungen, Build-Provenienz, Request-Parsing,
Runtime-Artefakt-Containment, Workflow-Evidence, generierten Berichten und
Connector-Helfersicherheit. Diese Änderung gleicht jede Zeile mit dem aktuellen
Parent-Stand ab, implementiert anwendbare Parent-only-Behebungen und benennt
ungelöste Evidence-Lücken explizit.

## Akzeptanzkriterien

- CSV-01 bis CSV-19 haben jeweils eine explizite Disposition.
- Anwendbare Parent-only-Behebungen besitzen fokussierte Regressionstests;
  frühere Behebungen werden weder zurückgenommen noch doppelt gepatcht.
- Mehrdeutiges Transfer-Encoding-plus-Content-Length-Framing wird abgelehnt,
  bevor eine Backend-Anfrage abgesetzt wird.
- Jede konfigurierte Runtime-Schreibwurzel einschließlich MATRIX_ROOT wird
  descriptor-begrenzt und eigentumsvalidiert, bevor sie verwendet wird.
- Ein öffentlich schreibbarer Runtime-Vorgänger wird nur akzeptiert, nachdem
  sein geöffneter Descriptor Root-Ownership und Sticky-Semantik belegt.
- Build- und Report-Evidence-Kontrollen schlagen fehlgeschlossen fehl.
- Englische/deutsche Dokumentation bleibt gepaart.
- Der PR ist erst für eine geschützte Integration geeignet, wenn ein frischer
  Exact-Head-Full-Evidence-Lauf sowie alle anwendbaren Checks, Review-/Thread-
  und Ruleset-Anforderungen bestanden sind; es gibt keinen direkten
  `master`-Write und keinen Bypass.

## Dispositionen der Befunde

| CSV-Zeile | Disposition |
| --- | --- |
| CSV-01 | Bereits durch Parent-Commit 1fc2321 behoben (Apache Phase-4 Bypass); kein doppelter Patch. |
| CSV-02 | Bereits durch Parent-Commit 63819e4 behoben (privilegierter Submodule-Workflow); kein doppelter Patch. |
| CSV-03 | Gepinnte und verifizierte libmodsecurity-Tag-/Commit-Anweisungen vor Detached Checkout, Submodule-Update, Build, Test und Install implementiert. |
| CSV-04 | Nichtblockierende Authorization-Clients, monotone Deadline, begrenztes Polling und 408 für langsame Clients implementiert. |
| CSV-05 | Bereits durch Parent-Commit 63819e4 behoben (Write-Token des Updated-Submodule-Workflows); kein doppelter Patch. |
| CSV-06 | Striktes Verified-Report-Provenienz-/Evidence-Gate implementiert. Der Workflow provisioniert nun kontrollierte lokale Abhängigkeiten und führt den vorhandenen strikten/vollständigen Parent-Producer vor seinem terminalen Gate aus; dessen frisches Exact-Head-Ergebnis steht noch aus und wird hier nicht als bestanden behauptet. |
| CSV-07 | Descriptor-sichere, no-follow- und eigentumsvalidierte Behandlung aller konfigurierten Schreibwurzeln einschließlich MATRIX_ROOT implementiert. |
| CSV-08 | Bereits durch Parent-Commit a73c335 behoben (Blocked-Status-Marker); kein doppelter Patch. |
| CSV-09 | Validierung von Markdown-Fence-Markern und -Längen für generierte Berichte implementiert. |
| CSV-10 | Keine Lighttpd-Quellcodeänderung: blocked_missing_evidence. Im isolierten Parent-Checkout fehlen gepinnter betroffener Lighttpd-Quellcode/Host/Modul sowie Queue-/Multi-Chunk-Client-Evidence. |
| CSV-11 | Bereits durch Parent-Commit aabde81 behoben (veränderliche Projektwurzeln); kein doppelter Patch. |
| CSV-12 | Remote-Rule-Merging implementiert: Leere Remote-Werte erben lokale Werte; partielle Remote-Credential-Konfiguration wird abgelehnt. |
| CSV-13 | Begrenztes lokales Smoke-Request-Body-/Chunk-/Trailer-Parsing und Deadlines implementiert; TE+CL und wiederholtes CL/TE-Framing werden vor dem Forwarding abgelehnt. |
| CSV-14 | Validierte Verified-Run-IDs für Runtime-Artefaktpfade implementiert. |
| CSV-15 | Strenge BUILD_ROOT-Evidence-Weitergabe für Report-Layout-/Provenienzprüfungen implementiert. |
| CSV-16 | Zufällige task-eigene sichere Temporär-Writer statt vorhersagbarer Pfade implementiert. |
| CSV-17 | HAProxy-HTX-Transaktions-IDs auf das native 127-Zeichen-Payload-Limit begrenzt, mit Parent-only-Regression. |
| CSV-18 | Validierung deutscher Companions generierter Berichte und ihrer Layout-/Evidence-Regeln implementiert. |
| CSV-19 | Bereits durch Parent-Commit 0f82f74 behoben (Action Majors); kein doppelter Patch. |

## Implementierungsentscheidung und Begründung

Nur ungelöstes Parent-eigenes Verhalten wird geändert. Der Authorization-Service
verwendet nun monotones Timeout/nichtblockierendes Polling; der Smoke-Helper
lehnt TE+CL und wiederholtes CL/TE-Framing vor dem Forwarding ab; alle Lifecycle-Schreibwurzeln werden
descriptor-begrenzt, nicht nur die Default-Wurzel; Run-IDs,
no-follow-Verzeichnisoperationen und zufällige task-eigene Temporärverzeichnisse
verhindern Traversal-, Symlink- und Kollisionspfade. Generierte Berichte
erfordern unveränderliche Build-Provenienz, striktes Layout/Evidence und
strukturell gültige bilinguale Inhalte. HAProxy-Helfer-IDs bleiben an der
nativen Puffergrenze. Das Sonar-Follow-up ersetzt Pfadnamenvertrauen für
öffentliche temporäre Wurzeln durch Descriptor-basierten Beweis für
Verzeichnis, UID 0, Sticky-Bit und schreibbaren Mode und erhält die vorhandenen
No-Follow-, Nachfolger-Owner- und Final-Root-Prüfungen.

## Geänderte Dateien

- Compiler-Guide-Generierung und englische/deutsche Compiler-Guides;
- Verified-Report-Workflow, Evidence-Receipt-/Layout-Prüfungen und
  Berichtsgeneratoren;
- Full-Evidence-Orchestrierung der Report-Governance und ihr fokussierter
  CI-Sicherheits-Regressionsvertrag einschließlich begrenzter
  Diagnosepfade nur bei Fehlern;
- Runtime-Pfad-, Run-ID- und Temporärverzeichnis-Helfer sowie direkte
  schreibfähige Lifecycle-Einstiegspunkte;
- lokales Smoke-Request-Parsing, Authorization-Timeout, Remote-Rule-Merging
  und HAProxy-HTX-Helferverhalten;
- fokussierte Python-, Shell-, C-, Workflow-, Dokumentations- und
  Evidence-Tests;
- dieses englische/deutsche Change-Record-Paar und das Indexpaar.

## Current-Master-Fortsetzung (2026-07-23)

Der Draft wurde mit einer bewussten Union-Auflösung vom Parent-`master`
`b37aa629398501f83750d6454f5f6a27eb614818` aktualisiert. Die aktuellen
immutable Action-Pins, der Go-Version-Contract, das strikte
Verified-Report-Evidence-Gate, die Authorization-Timeout-Prüfung und beide
Sprachindizes bleiben gemeinsam erhalten.

Die Fortsetzung behebt anschließend die lokal behebbaren Sonar-Befunde, ohne
eine Kontrolle abzuschwächen: Descriptor-Traversal und Chunk-Parsing sind bei
gleichen Guards in kleinere Helfer aufgeteilt, der Content-Length-Parser
bleibt ASCII-only, der Authorization-Service bindet Per-Connection-Status in
einen privaten Kontext, und die Regressionstests vermeiden verschachtelte
beziehungsweise Mehrfachaufruf-Assertions. Der Timeout-Smoke-Fake behält die
nicht-konstanten Signaturen aus `msconnector_runtime.h` bei, weil dessen
Produktivimplementierungen diese Objekte verändern; es wurde weder eine
Scanner-Suppression noch eine öffentliche ABI-Änderung verwendet.
Ein Exact-Head-Sonar-Detail-Readback zeigte anschließend 22
`python:S3415`-Hinweise zur Assertion-Reihenfolge. Sie sind auf die native
`actual, expected`-Reihenfolge korrigiert, ohne Testbedingung oder geschützte
Kontrolle zu verändern. Die zwei `c:S995`-Hinweise im Timeout-Smoke waren
echte Lücken im Fake-Lifecycle und keine Const-Correctness-Gelegenheit: Die
Fake-Runtime zählt jetzt aktive Transaktionen, und die Fake-Transaktion hält
Owner und Completion-Status. Das Fake-`begin` speichert einen gültigen Owner
und erhöht dessen Zähler; das idempotente Fake-`finish` validiert, dekrementiert
und markiert den Abschluss. Das erhält die gemeinsame nicht-konstante ABI und
macht den Smoke-Lifecycle ohne Scanner-Suppression verhaltenswirksam.

Der Branch wurde anschließend normal auf den aktuellen Parent-`master`
`a308d7b414f0859490fe7253e0683a4bde80b563` aktualisiert. Dabei wurde nur die
aktuelle Framework-Gitlink-Aktualisierung übernommen; kein Framework- oder
MRTS-Worktree wurde von dieser Aufgabe initialisiert, verändert, gestaged oder
committed.

## Integrationsremediation (2026-07-26)

Der vorherige Workflow führte einen Governance-only-Report-Check aus und
scheiterte dann korrekt am strikten Consumer, weil in seinem flüchtigen Runner
keine aktuelle Runtime-Evidence erzeugt worden war. Diese Remediation behält
das fehlgeschlossene terminale Gate bei und fügt den vorhandenen
strikten/vollständigen Parent-Producer hinzu, statt Reports oder Receipts zu
kopieren. Der Job erstellt mit dem ausgewählten CPython-3.14-Interpreter eine
virtuelle Umgebung und installiert das vorhandene Framework-
`requirements-ci.lock` mit `--require-hashes`, `--only-binary` und
`pip check`; er aktualisiert weder Pip noch installiert er
`requirements-dev.txt`. Er aktiviert den strikten Runtime-Komponenten-Pfad und
übergibt den überprüften unveränderlichen Expat-Commit
`c61098da494eea1cbd091118118dcee417faacea`, der aus dem verifizierten
Upstream-Release `R_2_8_2` aufgelöst wurde. Der strikte Parent-Pfad lehnt
Branch, Tag, abgekürzten SHA und Latest-Release-Lookup ab und prüft den
Checkout-Head, bevor er den Producer speisen kann. Dies wird als
`FND-PARENT-0052` verfolgt.

Der Job nutzt außerdem die bereits unterstützten Runtime-Download-/Build-
Opt-ins und besitzt ein 360-Minuten-Timeout passend zum dokumentierten
345-Minuten-Maximalbudget des Producers. Die Reihenfolge lautet
hash-gesperrte Installation, `make report-governance`,
`make verified-report-run` und das terminale
`make verified-report-evidence-gate`; der fokussierte Workflow-
Sicherheitstest sperrt diese Reihenfolge, den strikten Modus, die
Provenienz-Eingaben, beide Opt-ins und das Budget fest.

Der isolierte Task-Worktree materialisiert die von Parent referenzierten
Framework- und MRTS-Revisionen ausschließlich als Runtime-Abhängigkeiten. Zu
dieser Remediation gehören keine Framework-/MRTS-Quellcodeänderung, kein
Branch, Commit, Push, Pull Request oder Parent-Gitlink-Update. Der
veröffentlichte Exact Head
`28a4a1af5e764860d27ecb670bd82283e7b1aa74` erreichte in seinen gehosteten
Push- und Pull-Request-Läufen den vollständigen Producer und schlug dann
korrekt mit `apache_httpd: missing_local_httpd_build` fehl. Dieser Record
behauptet weder frischen Runtime-Erfolg noch SonarCloud- oder Merge-Erfolg: Der
gehärtete nächste Exact Head muss im gehosteten CI laufen, bevor solche
Ergebnisse behauptet werden können.

Die bisherige nur-bei-Fehler aktive Diagnose gab nur das äußere Producer-Log
aus und zeigte daher die Apache-Klassifizierung, aber nicht die innere
Build-Ursache. Sie liest jetzt ausschließlich den regulären, nicht-symlinked
Pointer `$BUILD_ROOT/verified-runs/current-run-id`; sie lehnt eine leere
Kennung, eine Kennung mit mehr als 128 Zeichen, eine Kennung ohne initiales
alphanumerisches Zeichen oder eine Kennung mit Zeichen außerhalb von
`[A-Za-z0-9._-]` ab; und sie konstruiert exakt
`$BUILD_ROOT/verified-runs/$run_id/logs/02-make-prepare-runtime-components.log`.
Sie tailt diesen Pfad und das zusätzliche feste
`$BUILD_ROOT/logs/runtime-components/apache-build.log` nur dann, wenn jeder
eine reguläre, nicht-symlinked Datei ist, und begrenzt jeden Tail auf 300
Zeilen. Sie rekursiert nicht, verwendet keine Globs und gibt keine breite
Log-Wurzel aus. Jeder Raw-Log-Tail wird von einem frischen `uuidgen`-GitHub-
`::stop-commands::`-Token und seinem passenden Resume-Token umschlossen, damit
Log-Inhalt nicht als Workflow-Befehl interpretiert werden kann. Die Diagnose
akzeptiert weder den fehlgeschlagenen Producer noch verändert sie das terminale
Gate; sie macht nur die legitime Apache-Remediation im nächsten Exact-Head-Lauf
beobachtbar.

+## PCRE2-Digest-Remediation (2026-07-26)

Die frische gehostete begrenzte Diagnose am exakten Head `d93446a1b53be344f5599c48272060e2c664ae86` legte im Run `30193495484`, Job `89770795068`, den inneren Fehler offen:

```text
apache_poc: blocked missing required SHA256 digest for pcre2
```

Das Parent-`Makefile` hatte eine ansonsten undefinierte `PCRE2_SHA256` bedingungslos exportiert. GNU Make übergab Framework dadurch einen explizit leeren Wert und unterdrückte dessen absichtlichen nur-bei-nicht-gesetztem-Wert greifenden Default. Der Parent-Archiv-Prefetch-Pfad behandelte die PCRE2-Prüfsumme außerdem als optional und erlaubte Checksum-URL-Fallback, Download, Archiv-Parsing und Cache-Publikation, bevor Framework eine leere Prüfsumme vor der Extraction korrekt ablehnte.

Die Parent-only-Korrektur dupliziert das Framework-Pin nicht. Sie exportiert `PCRE2_SHA256` nur, wenn GNU Make einen tatsächlich vom Caller bereitgestellten Wert meldet, und verlangt vor Parent-Archiv-/Cache-Zustand eine literale 64-hex-Prüfsumme. Gültige Eingabe wird kleingeschrieben; leere, nur aus Whitespace bestehende, fehlerhafte und nicht passende Eingabe bleibt fehlgeschlossen, und `PCRE2_SHA256_URL` kann keine fehlende literale Prüfsumme ersetzen. Framework bleibt die alleinige Default-Pin-Autorität und sein Extraction-Time-Verifier bleibt unverändert. Diese Korrektur wird durch `FND-PARENT-0053` verfolgt.

Fokussierte lokale Evidence bestand: 33 Cache-Contract-/Cache-Identity-Tests, 20 CI-Security-Tests, 18 Runtime-Komponenten-Tests, `make check-ci-security-contract`, Variablendokumentations-Validierung, bilinguale Dokumentations-Validierung und `git diff --check`. Die direkte Framework-PCRE2-Archiv-Digest-Fixture bestand nicht: Ihre synthetische V3-Source besitzt das aktuell erforderliche nicht-symlinked `.gitmodules`-Manifest nicht und wird vor ihren beabsichtigten PCRE2-Assertions abgelehnt. Diese separate Framework-Fixture-Regression ist als `FND-FRAMEWORK-0056` erfasst; keine Framework- oder MRTS-Source, kein Branch, Gitlink oder Delivery-Schritt ist hier enthalten.

Diese lokalen Kontrollen sind keine gehostete Runtime-Evidence. Ein frischer Exact-Head-gehosteter strikter/vollständiger Producer und das unveränderte terminale Evidence-Gate müssen nach der normalen PR-Branch-Veröffentlichung bestehen, bevor SonarCloud-, Review-, Integrations- oder Resulting-Master-Erfolg behauptet wird.

## Runtime-Matrix-Diagnose-Follow-up (2026-07-26)

Am exakten Head `7238c9d0a0902affbf7dfae1d7f96d6603d80f89` bestanden im Hosted-Run `30196090664`, Job `89777788658` die Komponenten-Vorbereitung, die Runtime-Producer-Readiness und die begrenzte Apache-Kontrolle; `apache_poc` meldete das gebaute Modul. Der strikte/vollständige Producer schlug danach bei `make runtime-matrix-all-runtime` mit `rc=2` fehl; abhängige Matrix-, Report-Refresh-, Layout-, Lint- und Quick-Check-Consumer schlugen ebenfalls fehl oder wurden ungültig. Der äußere Job-Log bewahrte den festen verschachtelten Pfad `verified-runs/<validated-run-id>/logs/04-make-runtime-matrix-all-runtime.log`, aber nicht seinen kausalen Inhalt auf.

Das Parent-only-Follow-up fügt keinen Akzeptanzpfad hinzu und ändert das terminale Evidence-Gate nicht. Bei Fehlern leitet es genau diesen festen Matrix-Log erst nach Validierung des vorhandenen regulären Nicht-Symlink-Run-ID-Pointers ab, verlangt auch für den Log eine reguläre Nicht-Symlink-Datei, gibt höchstens 300 Zeilen aus und schirmt rohe Inhalte mit einem frischen GitHub-`stop-commands`-Token ab. Die vorhandenen begrenzten Preparation- und Apache-Diagnosen bleiben erhalten. Der nächste exakte Hosted-Head muss die Matrix-Ursache liefern; Matrix-, SonarQube-Cloud-, Review-, Integrations- oder Resulting-Master-Erfolg wird hier nicht behauptet. Diese undurchsichtige Evidenzlücke wird als `FND-PARENT-0054` verfolgt.

## SonarQube-Cloud-Follow-up (2026-07-26)

Die SonarQube-Cloud-PR-Analyse für den exakten Head `b28b8744765a2cac6e3cf91f7bd3070d49d7774d` bestand zwar ihr Quality Gate, meldete aber weiterhin 22 OPEN task-eigene Findings und 59 neue duplizierte Zeilen (1.6638465877044557 %). Das erfüllt nicht das aktuelle Delivery-Akzeptanzkriterium von null offenen PR-Findings und null New-Code-Duplizierung.

Die fokussierte Parent-only-Remediation setzt in den betroffenen `unittest`-Gleichheitsassertions den beobachteten Wert vor den erwarteten Wert, verwendet den vorhandenen kompilierten Immutable-Git-Commit-Ausdruck statt sein Literal zu wiederholen und entfernt die duplizierte Transaction-ID-Grenzabdeckung aus dem Helper-lokalen Test, weil der dedizierte Parent-Regressionstest dieses Verhalten bereits besitzt. Sie ändert keine SonarQube-Cloud-Regel, kein Quality Gate, keine Exclusion, keine Suppression, keinen Coverage-Schwellenwert, keine Scanner-Konfiguration, kein Framework, kein MRTS und keinen Gitlink.

Nach der Veröffentlichung bleibt eine frische Exact-Head-SonarQube-Cloud-Analyse erforderlich. Dieses Dokument behauptet vor Abschluss dieser Analyse keinen Null-Issue-, Null-Duplizierungs-, CI-, Review-, Integrations- oder Resulting-Master-Erfolg.

## Payload-sichere Hosted-Evidence-Retention-Follow-up (2026-07-26)

Eine Exact-Head-Prüfung von Parent-PR #74 zeigte, dass
`make verified-report-run` die aktuellen
`verified-run-manifest.generated.json`, `report-freshness.generated.json`,
`report-refresh-manifest.generated.json`, `verified-commands.json`,
`full-matrix-aggregate-receipt.json`, den rohen
`full-runtime-matrix-runs.jsonl`-Index und die zwölf job-lokalen `job.json`-
Records erzeugt. Sie werden jedoch nur im ephemeren GitHub-hosted Runner
erzeugt: Der Workflow besaß keinen Artifact-Upload-Schritt und seine
erfolgreichen Logs zeigen nur Command-Ergebnisse statt der vollständigen
maschinenlesbaren Receipt-Kette. Das erfüllt das Akzeptanzkriterium von
FND-CROSS-0001 für ein aufbewahrtes Freshness-Manifest nicht.

Der erste Artifact-Retention-Nachfolger wird nicht als Evidence akzeptiert:
Eine Prüfung zeigte, dass seine Shell-Pfadprüfungen die spätere Upload-Action
nicht an die geprüften Dateien banden. Die beiden task-owned Läufe dieses
unsicheren Nachfolgers wurden vor dem Upload abgebrochen; aus ihnen wurde kein
Artifact erzeugt oder geprüft.

Das korrigierende Parent-only-Follow-up behält den vollständigen Producer und
das erste strikte Gate. Es staged die feste 18-Dateien-Structured-Allowlist
über descriptor-relative `O_NOFOLLOW`-Traversal, stabile Regular-File-Reads
und exklusive Writes in ein neues zufälliges Kind eines privaten,
runner-owned Staging-Parents. Die Upload-Action erhält nur diese Staging-Wurzel.
Danach läuft das strikte Gate erneut; derselbe descriptor-sichere Code
vergleicht jeden staged Digest und Byte-Count mit dem Live-Source-Set und lehnt
Zusätze, Symlinks, Ersetzungen oder eine geänderte Quelle vor dem Upload ab.
Das Artifact wird zehn Tage aufbewahrt und schlägt bei fehlender Staging-Wurzel
fehl. Es enthält die drei generierten Manifest-JSON-Dateien, die Command- und
Aggregate-Receipts des aktuellen Runs, den rohen Matrix-Index und alle zwölf
Job-JSON-Records. Build-Trees, rohe Logs, `run.log`, Result-JSONL,
Request-/Response-Payloads, Header und Cookies sind bewusst ausgeschlossen.

Der Workflow entfernt außerdem doppelte teure PR-Arbeit, ohne den
Runtime-Nachweis zu verkürzen: Automatische Pushes sind auf `master` begrenzt,
jeder Pull Request erhält weiter einen vollständigen Producer, und eine
Concurrency-Gruppe pro PR/Ref bricht nur überholte Läufe ab. Ein separater
kurzer Read-only-Contract-Preflight führt
`make check-ci-security-contract` vor dem 360-Minuten-Producer-Job aus. Beide
Jobs checken den exakten Pull-Request-Head aus (außerhalb eines PR die
Event-SHA), daher nutzt auch die Artifact-Identität dieselbe Revision. Der
Workflow behält `permissions: contents: read`, verwendet kein
`pull_request_target`, erhält keine Secrets und gewinnt keine Write-Permission.
Nach seinem setup-python-Interpreter-Verifier setzt der Preflight explizit
`PYTHON=python3`, damit Make keine von einem nicht vertrauenswürdigen Pull
Request gelieferte repository-lokale `.venv` auswählen kann.

Dies ist ein descriptor-sicherer staged Snapshot, kein transaktionaler
Filesystem-Snapshot und kein Schutz gegen einen beliebigen weiterlaufenden
Same-UID-Prozess, der einen Runner-Pfad nach dem finalen Vergleich ändern kann.
Der Retention-Claim setzt daher voraus, dass vom finalen Vergleich bis zum
Upload kein solcher nicht vertrauenswürdiger weiterlaufender Prozess existiert;
ein stärkeres Modell benötigte eine getrennte Identität oder einen Uploader,
der einen geschützten Descriptor/Stream konsumiert.

Die aktiven Läufe vor der Retention können dieses Artifact nicht rückwirkend
erhalten. Ein Nachfolge-Exact-PR-Head muss den vollständigen Hosted-Producer,
beide strikten Gate-Beobachtungen, die staged-Source-Bindung und den neuen
payload-sicheren Upload bestehen, bevor das Artifact heruntergeladen und auf
eine übereinstimmende Run-ID, aktuelle Parent-/Framework-Revisionen,
deklarierte Hashes sowie keine stale oder ungeklärte Abweichung geprüft werden
kann. Hier wird weder eine
FND-CROSS-0001-Schließung noch ein SonarQube-Cloud-, Review- oder geschützter
Integrations-Erfolg behauptet.

## Ausgeführte Befehle

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| Fokussierte Parent-Unittest-Suite für Compiler-Guides, Workflow-Sicherheit, bilinguale Dokumentation, Generated-Report-Evidence, Runtime-Pfade, Pfadauflösung, Smoke-Request-Bodies und HAProxy-HTX-IDs | bestanden: 146 Tests nach dem S5443-Follow-up (die frühere rebased Suite enthielt 144 Tests). |
| Pre-Fix-S5443-Regressions-Trio für root-owned/sticky-, unsafe-root- und Fremdbesitzer-Pfade | erwartetes Fehlschlagen: Die alte Pfadnamen-Allowlist lehnte die synthetische sichere Wurzel ab, bevor sie den vorgesehenen Ownership-Pfad ausüben konnte. |
| Post-Fix-S5443-Regressions-Trio | bestanden: Root-owned/sticky Shared-Root gelingt; non-sticky/non-root Shared-Roots und fremdbesitzte Nachfolger schlagen vor Final-Root-Erstellung fehl. |
| Vier fokussierte Runtime-Pfad-Policy-Kontrollen | bestanden: Mutable-Root-, Broad-Parent-, ausgewählte Python-Policy- und System-Root-Ablehnungskontrollen bleiben bestanden. |
| Vollständiges Runtime-Path-Policy-Unittest-Modul | blocked_environment für einen Framework-gestützten Shell-Checker: Dem absichtlich nicht initialisierten Framework-Gitlink fehlt `ci/lib/common.sh`; die anderen vier Kontrollen bestanden. |
| Ruff check / format check für die beiden Python-Dateien | not_run: Die ausgewählte Parent-virtuelle Umgebung enthält kein `ruff`-Executable; es wurde keine Dependency installiert. |
| make check-http-authorization-service-timeout mit GCC und Clang | für beide Compiler bestanden. |
| make check-common-helpers-c17 mit GCC und Clang | für beide Compiler bestanden. |
| Common-SDK- und Common-Security-Source-Contract-Kontrollen | bestanden. |
| sh -n für drei geänderte Runtime-Lifecycle-Shell-Einstiegspunkte | bestanden. |
| Strikter Generated-Report-Layout-Checker vor der Remediation gegen die damalige Evidence | erwartetes Fehlschlagen: unvollständige/veraltete Evidence wurde abgelehnt. Das belegt CSV-06-Fail-Closed-Verhalten und ist kein bestandener Provenienzstatus. |
| make check-bilingual-docs und kanonischer Framework-gestützter HAProxy-Harness | blockiert: Der Framework-Gitlink fehlt absichtlich im Parent-only-Checkout und wurde nicht initialisiert oder verändert. |
| Finales git diff --check nach Abschluss des Change Records | bestanden: keine Whitespace-Fehler im Task-Worktree. |
| Current-Master-Fortsetzung: `tests.test_runtime_path_security`, `tests.test_local_runtime_smoke_request_body`, `tests.test_haproxy_htx_transaction_id` und `tests.test_generated_report_evidence_integrity` | bestanden: 90 Tests einschließlich Symlink-/Ownership-, Request-Framing-, ASCII-Content-Length-, HTX-ID- und Report-Integrity-Kontrollen. |
| Current-Master-Fortsetzung: `tests.test_resolve_runtime_paths` | bestanden: 8 Tests. |
| Current-Master-Fortsetzung: Workflow-Security- und Compiler-Guide-Suiten | bestanden: 37 Tests nach der Konflikt-Union. |
| Current-Master-Fortsetzung: Authorization-Timeout-Smoke | mit GCC und Clang unter isolierten externen Build-Wurzeln bestanden; Common-C17-Helper- und Shell-Syntax-Prüfung bestanden ebenfalls. |
| Current-Master-Fortsetzung: fokussiertes Security-Diff-Review | bestanden: keine neue plausible Sicherheitsregression im geprüften Zehn-Dateien-Remediation-Diff. |
| Exact-Head-Sonar-`S3415`-Assertion-Reihenfolgen-Follow-up | bestanden: 92 fokussierte Runtime-Pfad-, bilinguale Dokumentations- und Generated-Report-Evidence-Tests nach allen 22 Actual/Expected-Reihenfolgenkorrekturen. |
| Current-Master-Fortsetzung: verhaltenswirksamer Timeout-Smoke-Fake-Lifecycle | bestanden: GCC-/Clang-Timeout-Smoke-Kompilierung und -Ausführung üben normales Begin/Finish-Ownership- und Count-Bookkeeping ohne Änderung der Common-Runtime-ABI. |
| Historisches gehostetes Exact-Head-CI und SonarCloud für `95c59343dca602b8b6412b307b0d0002a3dca91d` | bestanden für SonarCloud-Quality-Gate und alle Nicht-Evidence-GitHub-Checks; die gefilterte Sonar-Issue-Abfrage lieferte null offene Issues. `report-governance` schlug korrekt nur wegen fehlender/veralteter Runtime-Receipts und Downstream-Evidence fehl. |
| Integrationsremediation: fokussierte `tests.test_prepare_runtime_components` und `tests.test_ci_security_workflows` mit der task-lokalen Python-Umgebung | bestanden: 37 Tests decken strikten unveränderlichen-Expat-Dispatch, Mutable-Ref-Ablehnung vor der Source-Vorbereitung, Checkout-Head-Mismatch-Ablehnung, Nicht-Strict-Kompatibilität, korrekte Runtime-Guardrail-Beschreibungen und den Workflow-Vertrag ab. |
| Integrationsremediation: `make check-ci-security-contract` mit der task-lokalen Python-Umgebung | bestanden: 19 Workflow-Sicherheits-Tests sowie actionlint-, zizmor- und gitleaks-Lock-Validierung. |
| Integrationsremediation: `ci/checks/documentation/check-bilingual-docs.py` mit der task-lokalen Python-Umgebung | bestanden: Das aktualisierte englisch/deutsche Change-Record-Paar bleibt strukturell gepaart. |
| Integrationsremediation: `git diff --check` | bestanden: kein Whitespace-Fehler im scoped PR-#74-Worktree. |
| PR-#74-Härtung der begrenzten Diagnose: `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 .venv/bin/python -m unittest -v tests.test_ci_security_workflows` | bestanden: 19 Tests einschließlich exaktem Current-Run-Pointer, Kennungsvalidierung, zwei festen Log-Pfaden, Regular-/Nicht-Symlink-Gate, 300-Zeilen-Grenze, Command-Shielding und beibehaltener terminaler-Gate-Reihenfolge. |
| PR-#74-Härtung der begrenzten Diagnose: `rtk proxy env PYTHON=.venv/bin/python PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 make check-ci-security-contract` | bestanden: dieselben 19 Workflow-Sicherheits-Tests sowie actionlint-, zizmor- und gitleaks-Lock-Validierung. |
| PR-#74-Härtung der begrenzten Diagnose: `rtk proxy env PYTHON=.venv/bin/python PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 make check-bilingual-docs` | bestanden: Das englisch/deutsche Change-Record-Paar bleibt nach der Zwei-Pfad-Diagnoseaktualisierung strukturell gepaart. |
| PR-#74-Härtung der begrenzten Diagnose: `rtk git diff --check -- .github/workflows/verified-report-governance.yml tests/test_ci_security_workflows.py reports/audits/change-records/CR-20260721-csv-security-findings-remediation.md reports/audits/change-records/CR-20260721-csv-security-findings-remediation.de.md` | bestanden: kein Whitespace-Fehler im scoped Vier-Dateien-Diff. |
| Payload-sichere Hosted-Evidence-Retention: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_ci_security_workflows` | bestanden: 20 Tests, einschließlich strikter-Gate-Reihenfolge, unveränderlichem Action-Pin, SHA/run-gebundenem Artifact-Namen, vollständiger 12-Job-Allowlist und Ausschluss von Logs und Result-Payload-Pfaden. |
| Payload-sichere Hosted-Evidence-Retention: `PYTHONDONTWRITEBYTECODE=1 make check-ci-security-contract` | bestanden: dieselben 20 Workflow-Sicherheits-Tests sowie actionlint-, zizmor- und gitleaks-Lock-Validierung. |
| Payload-sichere Hosted-Evidence-Retention: `PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs` | bestanden: Das englisch/deutsche Change-Record-Paar ist strukturell gepaart. |
| Payload-sichere Hosted-Evidence-Retention: `git diff --check -- .github/workflows/verified-report-governance.yml tests/test_ci_security_workflows.py reports/audits/change-records/CR-20260721-csv-security-findings-remediation.md reports/audits/change-records/CR-20260721-csv-security-findings-remediation.de.md` | bestanden: kein Whitespace-Fehler im scoped Vier-Dateien-Diff. |
| Artifact-Retention-Sicherheitskorrektur und Runtime-Effizienz-Follow-up: `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_generated_report_evidence_integrity tests.test_ci_security_workflows tests.test_python_version_contract` | bestanden: 117 Tests decken descriptor-relatives Staging aller 18 Allowlist-Records, Intermediate-/Final-Symlink-Ablehnung, Source-Ersetzung und -Mutation, Staged-Source-Bindung, die exakte Workflow-Reihenfolge und das Python-Workflow-Inventar ab. |
| Artifact-Retention-Sicherheitskorrektur und Runtime-Effizienz-Follow-up: `rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-ci-security-contract` | bestanden: 20 Workflow-Sicherheits-Tests sowie actionlint-, zizmor- und gitleaks-Lock-Validierung. |
| Artifact-Retention-Sicherheitskorrektur und Runtime-Effizienz-Follow-up: `rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-python-version-contract` | bestanden: kanonisches Python 3.14.6 und 29 Python-ausführende Workflow-Jobs; der Staging-Workflow verwendet statische, zuvor verifizierte `python3`-Command-Heads und einen privaten Virtualenv-PATH. |
| Artifact-Retention-Sicherheitskorrektur und Runtime-Effizienz-Follow-up: `rtk proxy timeout 180s env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python ci/checks/documentation/check-bilingual-docs.py` | bestanden: `bilingual docs ok`. |
| Artifact-Retention-Sicherheitskorrektur und Runtime-Effizienz-Follow-up: Framework-Workflow-YAML-Checker und `git diff --check` | bestanden: Der Parent-Workflow parst und der scoped Diff enthält keinen Whitespace-Fehler. |

## Security-Auswirkung

Dies ist Defense-in-Depth über Request-Verarbeitung, lokale Runtime-Werkzeuge,
CI-/Report-Provenienz und einen Connector-Helfer. Es schließt einen getesteten
Local-Helper-Forwarding-Fall für mehrdeutiges TE+CL- und wiederholtes
CL/TE-Framing sowie eine bei der
Prüfung entdeckte plausible Containment-Lücke für konfiguriertes MATRIX_ROOT.
Das S5443-Follow-up lehnt außerdem einen root-owned, aber nicht-sticky
öffentlichen Vorgänger ab, statt ihn anhand seines Pfadnamens zu akzeptieren.
Die begrenzte Fehlerdiagnose ist zusätzliche Defense in Depth, keine
validierte Schwachstelle: Sie behandelt rohe lokale Build-Logs als nicht
vertrauenswürdige Workflow-Ausgabe und verhindert, dass deren Inhalt zu
GitHub-Workflow-Befehlen wird, während der Nonzero-Fehler des Producers
erhalten bleibt.
Die Hosted-Evidence-Fortsetzung ist ebenfalls allowlisted und nur-bei-Erfolg:
Sie öffnet jede Source-Komponente descriptor-relativ ohne Symlink-Following,
liest jeden der festen 18 Structured-Records stabil und schreibt eine
exklusive staged Kopie unter einer privaten runner-owned Wurzel. Der Upload
erhält ausschließlich diese Staging-Wurzel. Nach dem zweiten unveränderten
strikten Gate vergleicht dieselbe descriptor-sichere Logik jeden staged Digest
und Byte-Count mit dem aktuellen Source-Set und lehnt eine Ergänzung, einen
Symlink, eine Ersetzung oder eine geänderte Source vor dem Upload ab. Sie lädt
keine Logs, Result-Payloads, Build-Trees, Credentials oder breiten
Verzeichnisse hoch und bewahrt das vorhandene Read-only-
Workflow-Permissionsmodell. Dies schützt die normale Runner-Grenze, ist aber
kein transaktionaler Filesystem-Snapshot gegen einen beliebigen weiterlaufenden
Same-UID-Prozess nach dem finalen Vergleich.
Es behauptet weder Produktionshost-Exposure noch eine vollständige
Connector-Matrix oder Produktions-Exploitierbarkeit über die getesteten
Kontrollen hinaus.

## Runtime-Evidence

Vor der Integrationsremediation war keine vollständige Host-/Connector-Matrix
verfügbar. Der lokale
Helper-Test belegt, dass TE+CL- oder wiederholte-CL/TE-Eingaben 400 erhalten und nicht zum Test-Backend
weitergeleitet werden; er belegt kein Apache-, NGINX-, Lighttpd-, HAProxy-,
HTTP/2- oder HTTP/3-Runtime-Verhalten. Für CSV-10 lag keine
Lighttpd-Queue-/Multi-Chunk-Behebungs-Evidence vor.

Der aktualisierte unprivilegierte Workflow führt nun den vorhandenen
strikten/vollständigen Parent-Producer im flüchtigen Checkout aus und behält
den terminalen strikten Consumer. Der einzige akzeptable frische Nachweis ist
der Exact Head `28a4a1af5e764860d27ecb670bd82283e7b1aa74` erreichte diesen
Producer, schlug jedoch mit `apache_httpd: missing_local_httpd_build` fehl; die
äußere `prepare-runtime-components`-Zusammenfassung enthielt die Apache-
Build-Ursache nicht. Die gehärtete Zwei-Pfad-Diagnose ist keine Runtime-
Evidence und repariert Apache nicht. Ein nachfolgender gehosteter Exact-Head-
Lauf muss den begrenzten Apache-Build-Tail zeigen, den unveränderten strikten
Producer und terminalen Consumer erneut ausüben und eine revisionsgebundene
Receipt-Kette bereitstellen, bevor ein Erfolg behauptet wird. Die Python- und
Expat-Eingaben des strikten Producers bleiben unveränderlich/überprüft, bevor
er diese Evidence erzeugen kann; sein Nicht-Strict-Kompatibilitätspfad ist kein
Evidence-Ersatz.

## Nicht ausgeführte Prüfungen mit Begründung

- Der frische Exact-Head-Full-Runtime-Lauf und das terminale strikte Gate
  warten auf die Veröffentlichung dieser Remediation. Sie müssen im gehosteten
  CI laufen; fehlende/veraltete Evidence wird weiterhin abgelehnt und nicht
  als Ersatz akzeptiert.
- Framework-gestützte kanonische Connector-Prüfungen bleiben außerhalb des
  Quellcodeänderungs-Scopes. Der task-eigene isolierte Worktree materialisierte
  die referenzierten Framework- und MRTS-Revisionen read-only für die Runtime-
  Dependency-Preflight; weder Repository wurde geändert, gestaged, committed,
  gepusht noch zum PR-Ziel gemacht.
- Keine MRTS-Arbeit, kein Deployment-, Produktionshost-, vollständiger
  Connector-Matrix-, HTTP/2- oder HTTP/3-Check wurde durchgeführt.

## Bekannte Einschränkungen und Follow-up

CSV-06 bleibt blocked_missing_evidence, bis die authentischen aktuellen
Verified-Runtime-Reports des aktualisierten Workflows das strikte Gate
erfüllen. CSV-10 bleibt blocked_missing_evidence, bis eine gepinnte betroffene
Lighttpd-Umgebung und Queue-/Multi-Chunk-Test-Evidence vorliegen. Keiner der
Punkte wird vor einem frischen Exact-Head-Ergebnis als gelöst dargestellt.
`FND-PARENT-0052` bleibt in progress, bis der aktualisierte Exact Head die
hash-gesperrte Python-Installation, den unveränderlichen Expat-Checkout, den
vollständigen Producer und das terminale Gate im gehosteten CI belegt. Die lokale S5443-
Source-Remediation und die verhaltenswirksame `c:S995`-
Behebung des Timeout-Smokes sind auf dem veröffentlichten Exact Head
`95c59343dca602b8b6412b307b0d0002a3dca91d` verifiziert: SonarCloud schloss
seine neue Analyse am 2026-07-23T14:14:56Z mit einem `OK`-Quality-Gate und
einem gefilterten Open-Issue-Count von null ab. Der gemeinsame root-lokale
kanonische Finding-Store ist read-only; sein erforderlicher inkrementeller
FND-SONAR-0010-Import ist daher `blocked_permissions`, und dieser retained
Change Record behauptet nicht, ihn zu ersetzen. Der exakte Head hat
bestandene gehostete Nicht-Evidence-CI; das strikte Report-Evidence-Gate bleibt
absichtlich blockiert. Human Review und Resulting-Master-Evidence bleiben vor
jeder späteren Integrationsentscheidung erforderlich.

## Verbleibende Risiken

Die lokalen Kontrollen können weder die fehlenden Framework-gestützten
kanonischen Connector-Prüfungen noch eine betroffene Lighttpd-Runtime oder eine
vollständige Host-/Connector-Matrix belegen. Der frühere gehostete Exact-Head-
Snapshot ist historisch; der aktualisierte Full-Evidence-Lauf bleibt bis zu
seinem neuen Exact-Head-Ergebnis eine blockierende Bedingung. Unvollständige
Report-Evidence wird weiterhin abgelehnt. Descriptor-Metadaten können
keine Host-ACL-Semantik belegen und schützen nach dem Schließen der Descriptors
nicht gegen einen Angreifer mit derselben UID; ein dir_fd-haltendes
Sink-Refactoring liegt außerhalb dieser fokussierten Änderung. Keine Kontrolle,
kein Test, Scanner, Branch-Protection oder Evidence-Anforderung wurde für ein
positives Ergebnis abgeschwächt.

## Delivery-Status

Dieser Record unterstützt die aktuelle Parent-only-PR-#74-Remediation. Der
aktuelle Nutzer hat eine geschützte Integration nach allen Exact-Head-
Voraussetzungen autorisiert, aber dieser Record autorisiert weder einen
Direct-Master-Push, Bypass, Framework-/MRTS-Arbeit, History-Rewrite noch die
Behauptung eines bestandenen strikten Report-Evidence-Gates. Der aktualisierte
Head muss veröffentlicht und verifiziert sein, bevor der PR bereit gemacht
oder integriert wird.

## Finaler Diff- und Review-Status

Der aktuelle lokale Whitespace-Review und der aktualisierte bilinguale
Change-Record-Check bestanden. Der fokussierte 19-Test-Workflow-
Sicherheitsvertrag und die Tool-Lock-Validierung bestanden; vollständige
Runtime-Evidence, frisches SonarCloud, frisches gehostetes CI, Human Review
und Resulting-Master-Evidence bleiben getrennte Anforderungen. Historische
fokussierte Security-Regression-/Kontrolltests, die ausgewählte 146-Test-
Parent-Suite und vier Runtime-Pfad-Policy-Kontrollen bleiben oben dokumentiert.

## CPU-bewusste Full-Matrix-Scheduler-Fortsetzung (2026-07-26)

Die Full-Runtime-Matrix verwendet für ihre isolierten Runtime-Jobs nun
standardmäßig die Online-Prozessorzahl, die zuerst über `nproc`, dann über
`getconf _NPROCESSORS_ONLN` und andernfalls sicher mit eins ermittelt wird.
Ein expliziter positiver Wert von `FULL_MATRIX_MAX_PARALLEL_JOBS` bleibt eine
Obergrenze für gemeinsam genutzte Runner. In der beobachteten Task-Umgebung
melden beide Befehle 12, sodass eine vollständig vorbereitete
Zwölf-Job-Matrix alle zwölf Jobs ohne manuelles Cap zulassen kann.

Die Vorbereitung bleibt seriell, damit keine Cache-Refreshes gleichzeitig
ablaufen. Erst wenn alle angeforderten cache-gestützten Connector-Artefakte
bereit sind, lässt der Parent-Scheduler global geplante Jobs über einen
completion-getriebenen Worker-Pool zu. Er füllt jeden frei werdenden Slot
sofort wieder auf, statt auf einen langsamen Batch-Geschwisterjob zu warten,
und nur der Parent schreibt das Manifest in Plan-Reihenfolge. Fehlt ein
Artefakt, bleibt die Ausführung seriell. Ein abhängigkeitenfreier Planer
reserviert und validiert disjunkte Apache-, NGINX- und HAProxy-
Listener-Suchfenster im unprivilegierten Portbereich, bevor ein Runtime-Befehl
startet.

Der Completion-Pfad schlägt fehlgeschlossen fehl. Ein regulärer,
nicht-symlinked FD-9-`flock` sperrt konkurrierende Matrix-Läufe aus, während
ein privates FIFO jeden Abschluss einem verfolgten Kind-PID zuordnet. Ein
generationsgebundener Watchdog verwendet das vorhandene positive Limit
`VERIFIED_RUN_FULL_MATRIX_JOB_TIMEOUT_SECONDS`: Stirbt ein Wrapper vor seiner
Completion-Meldung, beendet der Scheduler mit 77, statt unbegrenzt zu warten.
Der Watchdog schließt FD 9 vor seinem Sleep und kann die Sperre daher nach
einem getöteten Parent nicht verlängern; echte Job-Nachfahren halten sie bis
zu ihrem eigenen Ende. Ein Completion-Ereignis genau an der Timeout-Grenze
kann konservativ Exit 77 erzeugen, wodurch Evidence- und Isolationskontrollen
erhalten bleiben.

Die lokale Validierung bestand `sh -n`, `git diff --check`, den ausgewählten
107-Test-Python-Regressionlauf mit `-W error::ResourceWarning`,
`make check-ci-security-contract`, Variablen- und bilinguale
Dokumentationsprüfungen, den Python-Version-Contract, gepinntes Actionlint
und Offline-Zizmor. Fokussierte Kontrollen belegen das erkannte Default-Cap,
Cap-zwei-Work-Conservation, Portplan-Ablehnung, Live-Lock-Ablehnung,
Parent-Kill-Lock-Reuse und den begrenzten Lost-Wrapper-Fehler mit anschließendem
Lock-Reuse. Diese lokalen Prüfungen ersetzen nicht den neuen Exact-Head-
Hosted-Producer, GitHub-, SonarQube-Cloud-, Review- oder
Integrationsnachweis, der erforderlich ist, bevor dieser Draft-PR verifiziert
oder gemergt werden kann.

## Exact-Head-SonarQube-Cloud-Korrektur (2026-07-26)

Der direkte PR-#74-Readback für den veröffentlichten Head
`a9086a4527d7c82fa4657d229099b1ef2fe12f9c` meldete trotz eines `OK` Quality
Gates vier task-eigene `OPEN`-Befunde: unbenutztes `build_root` in
`_current_verified_run_id_for_staging`, eine inkonsistente
Listener-Offset-Rückgabeform sowie Cognitive-Complexity-Befunde für den
Portplaner und den Exact-Staged-Tree-Reader. Derselbe Readback meldete
`new_duplicated_lines=38` und
`new_duplicated_lines_density=0.5794449527294907`, vollständig aus den zwei
Same-File-Scheduler-Lock-Reuse-Testblöcken. Das erfüllt nicht das strengere
Akzeptanzkriterium dieser Aufgabe von null offenen Befunden und null
Duplizierung.

Das Follow-up nimmt ausschließlich verhaltensbewahrende Parent-Änderungen
vor. Der Receipt-Reader erhält keinen unbenutzten Pfad mehr und zerlegt seine
descriptor-relative, `O_NOFOLLOW`- und Exact-Allowlist-Traversierung in kleine
Helfer, ohne die Path-Containment-Prüfungen zu ändern. Der Portplaner baut
eine typisierte Offset-Sequenz und delegiert Einzigartigkeit, Reihenfolge und
Allokation, behält aber seine fehlgeschlossenen Kollisions- und
Bereichsprüfungen. Die Scheduler-Tests verwenden einen gemeinsamen
Post-Descendant-Lock-Reuse-Retry-Helper und erhalten ihre individuellen
Assertions. Keine SonarQube-Cloud-Regel, kein Quality Gate, keine Exclusion,
keine Suppression, keine Coverage-Einstellung, kein Framework, kein MRTS,
kein Gitlink und kein Master-Branch wurden geändert.

Der ausgewählte lokale 107-Test-Regressionbefehl mit
`-W error::ResourceWarning` bestand nach diesen Korrekturen. Der nächste
normale Follow-up-Commit benötigt weiterhin frisches Exact-Head-hosted-CI und
einen direkten SonarQube-Cloud-Readback, bevor null offene Befunde, null
Duplizierung, PR-Verifikation oder Integration behauptet werden können; PR
#74 bleibt Draft.

## Ersetzende schlanke Hosted-Workflow-Fortsetzung (2026-07-27)

Diese Fortsetzung ersetzt ausschließlich die Hosted-Delivery-Erwartung der
früheren Einträge. Ihre Chronologie bleibt erhalten: Der frühere
strikte/vollständige Producer, die Runtime-Matrix mit zwölf Zellen,
Report-Refresh/-Generierung, das gestagte Artifact und ihre fehlgeschlagenen
Hosted-Läufe bleiben historische Diagnose-Evidence, sind aber keine
Voraussetzung des schlanken Nachfolgers von Parent-PR #74 mehr. Insbesondere
lassen ihre Apache-, PCRE2- und Matrix-Fehler den neuen Hosted-Workflow nicht
fehlschlagen und werden durch diese Entscheidung nicht als behoben behauptet.

Die erforderliche Hosted-Konfiguration ist exakt der aktuelle
`master`-Report-Governance-Workflow: ein read-only-Job
`report-governance`, ein 20-Minuten-Timeout und `make report-governance`.
GitHub darf weder `verified-report-run`, einen `all`-/runtime-all- oder
Zwölf-Zellen-Matrixlauf, Report-Refresh oder -Generierung, das strikte
Evidence-Gate, Runtime-Downloads oder -Builds noch einen Artifact-Upload
ausführen. Vollständiger Producer, Zwölf-Zellen-Matrix und Report-Generatoren
bleiben ausschließlich absichtliche manuelle lokale Arbeit; diese Fortsetzung
entfernt sie nicht und behandelt sie nicht als GitHub-PR-Evidence.

Die PR-#55-Provenance-Source-Bridge wird getrennt in #74 übertragen. Ihr
früheres striktes Hosted-Gate bleibt auf keinem der schlanken PRs erhalten;
dieser Record behauptet weder, dass #55 geschlossen, noch dass einer der PRs
gemergt wurde.

Das begrenzte Baseline-Sonar-Ziel umfasst 103
`python:S3415`-Korrekturen der Assertion-Reihenfolge sowie zwei bereits
vorhandene `S5443`-Behebungen sicherer temporärer Dateien. Es verwendet echte
Source-/Test-Korrekturen, keine Exclusion, Suppression, Quality-Gate-Änderung
oder Scanner-Abschwächung. Eine endgültige Reduktion der Sonar-
Main-Branch-Baseline bleibt bewusst der Post-Merge-Master-Analyse vorbehalten;
die PR-Analyse allein kann dieses Ergebnis nicht belegen.

Dieser Record behauptet keinen Post-Supersession-Exact-Head-GitHub-Lauf, keine
Sonar-PR-Analyse und keine Sonar-Main-Branch-Analyse. Historische lokale
Erfolge und historische Full-Runtime-Ergebnisse oben validieren diese
Nachfolger-Konfiguration nicht. Verbleibende Evidence sind fokussierte lokale
Tests der übertragenen Source und Sonar-Korrekturen, ein frischer Exact-Head-
20-Minuten-GitHub-Governance-Lauf, ein frischer Sonar-PR-Readback ohne
New-Code-Regression, normale Review-/Ruleset-Prüfungen sowie nach einem
autorisierten Merge die Master-Sonar-Analyse, die die begrenzte
Baseline-Reduktion misst.
