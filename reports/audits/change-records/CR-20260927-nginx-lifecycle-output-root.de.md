# Change Record: Materialisierungswurzel des NGINX-Lifecycles

**Sprache:** [English](CR-20260927-nginx-lifecycle-output-root.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260927-nginx-lifecycle-output-root` |
| Datum (UTC) | `2026-09-27` |
| Basis-Revision | `57b0ed6a72ff7c7235037a59f008164be673e7a5` |

Framework: `cc36b37d0f6a0fbc3512f3878a691751e91c5fbb`.
MRTS: `615b13bacbd008562c17408246c41ab27dca3104`.

## Motivation und Problemstellung

Der frische NGINX-Lifecycle scheiterte vor dem ersten Request. Der Parent
übergab einen Laufzeitpfad unter `runs/nginx/<run-id>/host-runtime`, während
der Framework-Materializer `build/nginx/<run-id>` als Output-Root auswählte.
Das Framework verweigerte den Geschwisterpfad korrekt mit
`write path escapes output root`. NGINX-Quellmaterialisierung, Modulbau und
Provisioning waren bereits erfolgreich.

## Akzeptanzkriterien

Baseline und First-Byte müssen innerhalb einer schmalen gemeinsamen
Output-Wurzel materialisieren. Der alte Geschwisterpfad muss weiterhin
abgewiesen werden. Canonical Evidence, Raw-Event-Collector, Connector-Build-
Inventar, Cache-v2, gepinnte Quellidentitäten und externe statische
Docroot-Projektion müssen ihre Grenzen behalten. Ein Laufzeit-PASS erfordert
frische echte Requests mit Root-Master und nobody-Worker sowie validierte
Canonical Evidence.

## Implementierungsentscheidung und Begründung

Das vorhandene HAProxy-Host-Work-Muster wird übernommen: NGINX-Unteraufrufe
verwenden `<connector-run-root>/nginx-host-work` als Framework-`BUILD_ROOT`
mit untergeordneten Laufzeit-, Ergebnis-, Temporär- und Harness-Pfaden. Der
globale Connector-Build-Root des Parents bleibt unverändert. Rohe
Phase-4-Quellen bleiben innerhalb des Raw-Runs des Collectors. First-Byte
erhält diese Stage-Aliasse und explizit
`SYNCHRONIZED_UPSTREAM_CONTROL_ROOT=<connector-run-root>`, damit sein
Evidenzziel enthalten bleibt. Der explizite Report-Root hält den reservierten
Runtime-Environment-Snapshot unter dem unveränderten Connector-Build-Root.
Andere Helper-Aufrufer behalten den bisherigen
Control-Root-Standard. Framework und MRTS benötigen keine Änderung.

## Security-Auswirkung

Framework-Containment, Audit-Prüfungen, Symlink-/Pfadautorität, getrennte
Root-Master-/nobody-Worker-Identitäten, Runtime mit privatem Netzwerk und
Root-eigene externe statische Projektion bleiben aktiv. Es gibt keine globale
temporäre Schreibfreigabe, Source-Map-Änderung oder Provenance-Überschreibung.

## Geänderte Dateien

- `ci/runtime/lifecycle/run-no-crs-baseline.sh`
- `ci/runtime/lifecycle/run-native-first-byte.sh`
- `tests/test_nginx_functional_materialization_layout.py`
- `tests/test_collect_no_crs_source.py`
- Dieses englische/deutsche Change-Record-Paar.

## Ausgeführte Befehle

Alle Shell-Befehle liefen durch RTK. Die zwei neuen Reproduktionen der
Parent-Pfade scheiterten gegen die Basis am beobachteten Containment-Fehler;
nach der Korrektur bestanden alle vier Materialisierungstests. Die kombinierte
Auswahl für Runtime-Resolver/-Pfade, Collector, Runner-Verdrahtung, Projektion,
Master/Worker und Full-Lifecycle-Profile/-Evidenz bestand 156 Tests.
Shell-Syntaxchecks bestanden. ShellCheck meldete 15 bestehende Warnungen;
normalisierte Basis-/Ist-Diagnosen sind identisch. Keine Warnung wurde
unterdrückt. `git diff --check` bestand. Dokumentationschecks werden im
externen Ausführungsplan festgehalten.

## Runtime-Evidence

Die kleinen Tests rufen den echten Framework-Materializer und tatsächliche
Parent-Zuweisungs-/Aufrufteile auf. Die kontrollierte Host-Grenze stoppt vor
Requests; diese Tests sind keine Laufzeit-PASS-Evidenz. Nach dem separaten
Quellcommit folgt ein frischer Lifecycle gegen dessen exakten Stand; sein
Ergebnis wird extern festgehalten.

## Nicht ausgeführte Prüfungen mit Begründung

Bei Vorbereitung dieses Records wurde der echte E2E-Rerun nach dem Commit
noch nicht ausgeführt. Remote-CI, SonarQube, Push, PR und Merge liegen außerhalb
dieser lokalen Aufgabe.

## Bekannte Einschränkungen

Pfadakzeptanz allein beweist weder Root-/nobody-Audit-Kompatibilität noch
Response-Phasen-Verhalten. Unabhängige spätere Laufzeitfehler bleiben Fehler.
Die Lifecycle-Ergebnisse von `aff1ba13` und Basis `57b0ed6` sind kein PASS.

## Verbleibende Risiken

Die Verschiebung nur der Unteraufrufpfade erhält Raw-Collector und
Komponentencache; tatsächliche Host-Ausführung muss Ownership und
Lifecycle-Interaktionen validieren. Cache-Wiederverwendung muss die normalen
Provenance-Prüfungen des Repositorys bestehen.

## Finaler Diff- und Review-Status

Der fokussierte Parent-Diff wurde unabhängig geprüft. Framework-/MRTS-Gitlinks
und die validierte SOURCE_MAP-Reparatur bleiben unverändert. Lieferung ist ein
separater lokaler Commit; weder History-Umschreibung noch Remote-Lieferung
sind autorisiert.
