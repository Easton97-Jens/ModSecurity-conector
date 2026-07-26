# Selektive Integration der Apache-Upstream-PRs #91-#94

**Sprache:** [English](CR-20260726-apache-upstream-pr-91-94-integration.md) | Deutsch


## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260726-apache-upstream-pr-91-94-integration` |
| Datum (UTC) | `2026-07-26` |
| Basis-Revision | `02642a466c94cbae58a9208868e75b6781074c58` |
| Grenze | Nur Parent-Apache-Source, Tests, Runtime-Harness und Provenienz; Framework/MRTS unverändert. |

## Motivation und Problemstellung

Die offenen Upstream-PRs #91-#94 enthalten eine benötigte Lebensdauerkorrektur sowie Ansätze, die Parent-Ownership und Runtime-Architektur widersprechen. Der Analyse-Commit `116193c8007173534707a908d48388738a2aa5f8` war im Fetch/API nicht verfügbar; seine vorgegebenen Entscheidungen blieben erhalten und aktuelle Heads wurden unabhängig geprüft.

## Akzeptanzkriterien

Jedes Connector-RulesSet genau einmal an seinen APR-Konfigurationspool binden; Intervention und EOS erhalten; Body-Regressionen und begrenzten Parent-Soak adaptieren; Framework/MRTS und Security-Kontrollen unverändert lassen.

## Implementierungsentscheidung und Begründung

Parent-Basis und Branch sind `02642a466c94cbae58a9208868e75b6781074c58` und `codex/apache-upstream-pr-91-94-integration`. Verifizierte Heads: #91 `230e14d755bc5912d96e13947aa4b8ef73dbb4fa`, #92 `7d408a10d359601d5771f0446a81284be17fbf29`, #93 `8221baee1f349e3954043dc0d8102b119b9a04bf`, #94 `1e07559819163e4c23338d646859422b0efd5c0e`; #94 baut auf #91, #93 auf #92. #94A wurde semantisch portiert. Nicht portiert: #91-Handler-Body-Consumption, #92-Docker/Compose, #93-Docker/Workflow, #94B-direkte Frees. Der `mp`-Owner registriert nach erfolgreicher Erzeugung einen null-sicheren Cleanup; Merge erzeugt ein unabhängig besessenes Objekt.

## Geänderte Dateien

`connectors/apache/src/msc_config.c`; Parent-Request-Body- und Valgrind-Harness; fokussierte Tests und Make-Ziele; Apache-Origin/Source-Maps; Change-Record-Paar und Indizes. Framework und MRTS blieben unverändert.

## Ausgeführte Befehle

`make check-apache-ruleset-cleanup`, `make check-apache-request-body-regressions`, `make check-apache-valgrind-soak`, Intervention- und Transaction-Tests, C-Standard-Wiring, bilinguale/Dokumentationsprüfungen, JSON-/Python- und Git-Diff-Prüfungen.

## Security-Auswirkung

Das RulesSet-Leak beim Abbau des Konfigurationspools wird ohne Shared-Pointer-Cleanup oder konkurrierende manuelle Freigabe geschlossen. Request-Pool-Kopien und einmaliges `msc_intervention_cleanup()` bleiben unverändert; kein Double-Free. EOS, Drain, Append-after-EOS-Schutz, fail-closed und zentrale Statuslogik bleiben.

## Runtime-Evidence

Fokussierte Source-Verträge bestanden. Native C17 war wegen fehlendem Framework BLOCKED. Live-Body, Smoke, Memcheck und Helgrind waren wegen fehlender nativer Konfiguration bzw. Valgrind BLOCKED und sind nicht PASS. Der Soak schreibt externe JSON-/Markdown-/Log-Evidence und trennt alle Leak-/Invalid-Access-Kategorien.

## Bekannte Einschränkungen

Statische Verträge beweisen kein Allocator-, echtes Multi-Bucket- oder Restart-Concurrency-Verhalten. Native Evidence ist vor dem Merge erforderlich.

## Verbleibende Risiken

Keine breiten Helgrind-Suppressions. Bibliotheksmeldungen müssen triagiert werden. `still reachable` gilt nicht als leak-frei. Das fehlende Analyseobjekt ist ausdrücklich dokumentiert.

## Nicht ausgeführte Prüfungen mit Begründung

`make check-apache-c17`, `make smoke-apache`, `make smoke-all`, Live-Body, Memcheck und Helgrind waren wegen Framework-/Runtime-/Valgrind-Voraussetzungen nicht ausführbar. Nach lokalen Korrekturen verbleiben in Dokumentationsaggregaten nur vorbestehende fehlende Framework-Linkziele.

## Finaler Diff- und Review-Status

Der Diff-Review fand eine RulesSet-Erzeugung, eine Registrierung, einen Adapter-Cleanup-Aufruf, keine geteilten Pointer, keine manuelle Cleanup-Konkurrenz, keine Intervention- oder zweite Body-Consumer-Änderung und keine Workflow-/Security-/Gitlink-Änderung. Wegen nativer Blocker ist ein Draft-PR erforderlich.
