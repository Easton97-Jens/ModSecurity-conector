# Change Record: Selektive Apache-Upstream-PR-#91–#94-Integration

**Sprache:** [English](CR-20260726-apache-upstream-pr-91-94-integration.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260726-apache-upstream-pr-91-94-integration` |
| Datum (UTC) | `2026-07-26` |
| Basis-Revision | `02642a466c94cbae58a9208868e75b6781074c58` |
| Grenze | Nur Parent-Apache-Quellen, Parent-Harness/Tests/Runtime/CI/Provenienz-Dokumentation; Framework, MRTS, Abhängigkeiten, Gitlinks und Submodule-URLs bleiben unverändert. |
| Upstream-Basis | ModSecurity-apache `0488c77f69669584324b70460614a382224b4883` bleibt der Basis-Ursprung. |
| Finding-Verknüpfung | `FND-PARENT-0043` bleibt für Intervention-Ownership erhalten; `FND-PARENT-0055` dokumentiert reparierte Adapter-Preflight-Defekte; native Voraussetzungen bleiben separat durch `FND-HOST-0002` blockiert. |

## Motivation und Problemstellung

Der User wählte eine enge Integration aus aktuellen [ModSecurity-apache-PRs
#91–#94](https://github.com/owasp-modsecurity/ModSecurity-apache/pulls):
#94A RulesSet-APR-Pool-Ownership portieren, die vorhandene sichere #94B-
Intervention-Ownership behalten, #91/#92-Request-Body-Coverage ohne den
Upstream-Production-Handler oder Docker-Stack anpassen und eine Parent-eigene
#93-Memcheck-/Helgrind-Soak-Route erstellen. Der angegebene historische
Analyse-Commit und die Entscheidungsmatrix konnten nicht aus lokaler, Remote-
oder GitHub-Evidence wiedergewonnen werden, daher blieb die explizite aktuelle
User-Auswahl die bindende Scope-Entscheidung.

## Akzeptanzkriterien

- `msc_config.c` registriert jedes nicht-null frische Directory-RulesSet zur
  Bereinigung in seinem APR-Config-Pool, einschließlich gemergter
  Konfigurationen; keine manuelle doppelte Bereinigung wird ergänzt.
- #94B-direkte `free(intervention.url/log)`-Logik wird nicht portiert.
  Vorhandene request-eigene Kopien und eine native Bereinigung bleiben das
  Intervention-Modell.
- Der lokale Apache-Input-Filter-/EOS-/Drain-/Fail-Closed-Pfad bleibt
  produktiv; keine #91-`ap_get_client_block()`-Handler-Implementierung wird
  eingeführt.
- Parent-eigene Controls decken Allow, Deny, Large/Multi-Bucket, Split-Trigger
  Chunked, Unread-Handler, Empty-Body, Keep-Alive-Repeat und deterministisches
  Lower-Filter-Read-Error-Verhalten ab; kein Docker-/Compose-Stack wird ergänzt.
- Parent-eigenes manuelles Memcheck-/Helgrind-Wiring hat begrenzte Roots,
  Prozess- und Evidence-Kontrollen und kann keinen blockierten oder nicht
  instrumentierten Run als Pass melden.
- `SOURCE_MAP.json` schreibt nur den direkten #94A-Source-Transplant zu
  `src/msc_config.c`; Parent-eigene Testanpassungen sind keine Upstream-Importe.

## Implementierungsentscheidung und Begründung

Die #94A-Anpassung ergänzt einen kleinen `msc_rules_set_cleanup()`-APR-
Wrapper und registriert ihn nur, nachdem `msc_create_rules_set()` nicht null
zurückgegeben hat. Jede Directory-Konfiguration, einschließlich eines Merge-
Ziels, besitzt ihr RulesSet über denselben APR-Pool-Lebenszyklus. Der native
Harness deckt normale Pools, Null-Erzeugung, Clear/Destroy, erfolgreichen
Merge, zwei RulesSet-Merge-Fehler und einen Common-Config-Merge-Fehler ab.
Sein Compile-Pfad setzt `NDEBUG` explizit zurück, damit assert-basierte
Controls nicht leer werden.

Das vorhandene `process_intervention()` kopiert behaltene Log- und Redirect-
Werte bereits nach `r->pool`, bevor eine native Bereinigung erfolgt. #94B
wurde deshalb absichtlich nicht transplantiert und vermeidet doppelte oder
Double-Free-Ownership.

Request-Body-Coverage bleibt im Parent-Harness. Ein test-only Lower-Input-
Filter gibt `APR_EGENERAL` nur auf seiner dedizierten Read-Error-Route zurück
und wird nach dem Connector installiert. Damit prüft er den vorhandenen
Fail-Closed-Discard-Pfad, ohne produktives Filtering zu ändern. Der Adapter
registriert seine generierte externe YAML über Frameworks unterstützte
`EXTRA_CASE_ROOTS`-Schnittstelle und wählt seine No-CRS-Baseline. Die #92-
Docker-/Compose-Architektur wird nicht importiert.

Der #93-Runner behält Apache-Lifecycle-Ownership im Parent-Harness. Er ergänzt
einen verifizierten Valgrind-Wrapper, Hard-Timeout, begrenzte task-eigene
Reports, ein payload-freies Upload-Bundle und strikte PASS-Evidence. Eine
Preflight-Reparatur verwendet unterschiedliche POSIX-Shell-Variablen, damit
ein validierter externer Soak-Root nicht zu `/` kollabieren kann.

## Geänderte Dateien

- `connectors/apache/src/msc_config.c`
- `ci/checks/connectors/apache/apache_rules_set_cleanup.c`,
  `ci/checks/connectors/apache/check-apache-rules-set-cleanup.sh` und
  `tests/test_apache_rules_set_cleanup.py`
- `connectors/apache/harness/mod_phase4_terminal_rogue.c` und
  `connectors/apache/harness/run_apache_smoke.sh`
- `ci/runtime/lifecycle/run-apache-request-body-regression.sh` und
  `tests/test_apache_request_body_regression_wiring.py`
- `connectors/apache/harness/apache_soak_workload.py`,
  `ci/runtime/lifecycle/run-apache-soak.sh`,
  `tests/test_apache_soak_wiring.py` und
  `.github/workflows/apache-soak.yml`
- `Makefile`, `connectors/apache/SOURCE_MAP.json`,
  `connectors/apache/ORIGIN.md` und `connectors/apache/ORIGIN.de.md`
- Dieses englische/deutsche Change-Record-Paar und seine gepaarten Indizes.

## Ausgeführte Befehle

| Befehl oder Control | Ergebnis |
| --- | --- |
| `rtk make check-apache-ruleset-cleanup` | Statischer RulesSet-Vertrag bestanden (4 Tests); nativer APR/APXS-Helper blockiert, weil `apxs`/nutzbare Apache-Header fehlen. GNU Make gab nach Child-Exit `77` den Wert `2` zurück. |
| `rtk make check-apache-ruleset-cleanup-lint` | Bestanden: Die 4 statischen RulesSet-Tests bestehen und der konfigurierte native Preflight ist wegen fehlender Apache-Development-Voraussetzungen wahrheitsgemäß als erlaubtes `blocked` dokumentiert. |
| `rtk make check-apache-intervention-cleanup` | Bestanden: 5 vorhandene Ownership-Contract-Tests. |
| `rtk make check-apache-c-standard-wiring` | Bestanden. |
| `rtk make check-apache-request-body-regression-wiring` | Bestanden: 8 Tests plus Shell-Syntax. |
| `rtk make check-apache-request-transaction-cleanup` | Die statische Transaction-Cleanup-Suite besteht (5 Tests); der native Helper ist durch fehlendes `apxs`/nutzbare Apache-Header blockiert. GNU Make gab nach Child-Exit `77` den Wert `2` zurück. |
| `rtk make apache-request-body-small-allow APACHE_REQUEST_BODY_ROOT=…/request-body-retry` | Die generierte externe Case-Datei aufgelöst und danach am fehlenden konfigurierten Apache-`httpd` blockiert; GNU Make gab nach Child-Exit `77` den Wert `2` zurück. |
| `rtk make check-apache-soak-wiring` | Bestanden: 12 Tests plus Shell-Syntax. |
| `rtk make apache-soak-memcheck APACHE_SOAK_ROOT=…/soak-retry` | Begrenztes Report-/Upload-Bundle erstellt und danach wegen nicht verfügbarem Valgrind blockiert; GNU Make gab nach Child-Exit `77` den Wert `2` zurück. |
| `rtk make apache-soak-helgrind APACHE_SOAK_ROOT=…/soak-retry` | Begrenztes Report-/Upload-Bundle erstellt und danach wegen nicht verfügbarem Valgrind blockiert; GNU Make gab nach Child-Exit `77` den Wert `2` zurück. |
| `rtk make check-bilingual-docs` und `rtk make check-doc-links` | Ausschließlich durch die absichtlich fehlenden Framework-Submodule-Targets des isolierten Arbeitsbaums blockiert; kein Befehl meldete einen Change-Record-spezifischen Defekt. Die fokussierte Bilingual-Checker-Unit-Suite bestand (11 Tests). |
| Finalisierung des kanonischen Codex-Security-Diff-Scans | Bestanden: Versiegelte vollständige Working-Tree-Coverage für alle 14 ausführbaren/strukturierten Provenienz-Dateien und 0 reportable Findings. Der einzige Command-Path-Kandidat wurde vor der Execution-Senke dynamisch verworfen. |

## Security-Auswirkung

Die RulesSet-Zerstörung ist jetzt an den owning APR-Config-Pool gebunden und
reduziert ein natives Lifetime-Leak-/Cleanup-Risiko, ohne einen zweiten Owner
hinzuzufügen. Intervention-Ownership bleibt sicher, weil Apache request-pool-
Kopien vor der vorhandenen einzigen nativen Bereinigung behält. Der test-only
Read-Error-Filter ist route-begrenzt und prüft ein Fail-Closed-`400`; er
ändert nicht das Production-Handler-Modell. Externe Case- und Soak-Roots sind
eingegrenzt, und der manuelle Workflow bleibt least-privilege, dispatch-only
und lädt nur begrenztes Report-Material hoch. Ein versiegelter fokussierter
Security-Diff-Review deckt die ausführbaren und strukturierten
Provenienz-Änderungen vollständig ab und meldet keine Schwachstelle. Seine
eine Command-Path-Hypothese wurde sicher falsifiziert: Traversal-Segmente werden
vor der Harness-Execution-Senke abgewiesen.

## Runtime-Evidence

Native Apache-Request-Body-, APR-Lifecycle-, Memcheck- und Helgrind-Evidence
ist in dieser Umgebung nicht verfügbar. Die stärkste ausgeführte Preflight-
Evidence zeigt, dass der Request-Body-Adapter sein externes Fixture auflöst und
dann am fehlenden Apache-Executable fehlgeschlossen scheitert; beide Soak-Modi
erstellen begrenzte task-lokale Evidence und scheitern danach an fehlendem
Valgrind fehlgeschlossen. Diese Ergebnisse sind Blocker, keine bestandenen
Runtime- oder Sanitizer-Resultate.

## Bekannte Einschränkungen

Der in der Anfrage genannte historische Analyse-Commit/-Matrix war nicht
verfügbar, obwohl aktuelle Upstream-PR-Heads und Stack-Beziehungen erneut
validiert wurden. Der Large-Body-Control verarbeitet ein Payload größer als
1 MiB, misst aber keine native APR-Bucket-Anzahl. Es wird kein nativer
Graceful-Reload-Zyklus, HTTP/2- oder HTTP/3-Assertion behauptet. Der RulesSet-
Harness verwendet kontrollierte Stubs und kann Libmodsecuritys produktives
Allocation-Verhalten nicht beweisen.

## Verbleibende Risiken

Der aktuelle Host kann den Apache/APR/Libmodsecurity-ABI-Pfad, tatsächliche
Request-Body-Response-Semantik oder Valgrind-Leak-/Race-Ergebnisse nicht
beweisen. Das vorhandene `FND-PARENT-0043` bleibt bis zu nativer Intervention-
Validierung blockiert. Kein Sicherheitscontrol, Test, Scanner, Workflow-
Permission oder Branch-Protection wurde geschwächt und keine Risikoakzeptanz
ist aufgezeichnet.

## Nicht ausgeführte Prüfungen mit Begründung

- Native RulesSet/APR-C17-Ausführung ist durch fehlende Apache-Development-
  Voraussetzungen (`apxs`/Header) blockiert.
- Vollständige Request-Body-Modus-Ausführung und gewöhnlicher Apache-Smoke sind
  durch das fehlende vorbereitete Apache-Executable und Connector-Runtime
  blockiert.
- Tatsächliches Memcheck und Helgrind sind durch nicht verfügbares Valgrind
  blockiert; kein Ersatzbericht ist Instrumentierungs-Evidence.
- Vollständiges `lint`, vollständiges `smoke-all`, HTTP/2- und HTTP/3-
  Matrizen sind keine Ersatzkontrollen für die eingegrenzten Controls und
  behalten ihre Framework-/Native-Voraussetzungen.

## Finaler Diff- und Review-Status

Der eingegrenzte Security-Diff-Review ist mit vollständiger Coverage und 0
reportable Findings finalisiert. Repository-weite Bilingual- und Link-Checks
wurden ausgeführt, sind aber nur blockiert, weil der isolierte Arbeitsbaum
absichtlich keine Framework-Submodule-Inhalte enthält; die fokussierte
Change-Record-Paritäts-Suite bestand. Nach dem ausführbaren Scan-Snapshot
änderte sich nur dieser leserorientierte Record.

Delivery-Update (vor diesem selbstaktualisierenden Dokumentations-Follow-up
beobachtet):

- Branch: `codex/apache-upstream-pr-91-94-integration`.
- Implementierungs-Commits: `3193b0ab44163f3c291f184f8d077adef602f943`,
  `73241f2634c4c52ee1c593a5f84b122d226d60ed` und
  `325581ea12586f894431ccd33cc0d3cbdfb0701d`.
- Draft-PR: [#124](https://github.com/Easton97-Jens/ModSecurity-conector/pull/124)
  gegen `master`.
- Bei der PR-Erstellung waren lokaler Head,
  `origin/codex/apache-upstream-pr-91-94-integration` und der PR-Head alle
  `325581ea12586f894431ccd33cc0d3cbdfb0701d`.

Dieser Follow-up-Record referenziert absichtlich nicht seine zukünftige eigene
Commit-SHA; die finale Gleichheit von lokalem, Remote- und PR-Head bleibt in
PR- und Task-Delivery-Evidence festgehalten. Die PR bleibt Draft, solange
native Apache/APR- und Valgrind-Runtime-Voraussetzungen nicht verfügbar sind;
CI-/Review-Ergebnisse sind ausstehend. Kein Merge, direkter Default-Branch-
Push, Framework-/MRTS-Delivery, Gitlink-Update oder Risikoakzeptanz wird durch
diesen Record autorisiert.
