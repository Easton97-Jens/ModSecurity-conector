# Change Record: selektierte NGINX-Size-Konfigurationsablehnung

**Sprache:** [English](CR-20261003-nginx-size-configtest.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20261003-nginx-size-configtest` |
| Datum (UTC) | `2026-10-03` |
| Basis-Revision | `b1dd58a1289a84f15903fa0bb46474cf776e67db` |

## Motivation und Problemstellung

Dem Pflichtrecord `invalid_size` fehlte eine konkrete selektierte NGINX-Invocation.
Die bereits abgeschlossene Boolean-Ablehnung beweist kein Size-Parsing.

## Akzeptanzkriterien

`modsecurity_phase4_body_limit maybe;` mit echtem `nginx -e stderr -t` ausführen.
Exit 1 und beide exakten Size-Diagnosen verlangen; FAIL für Wrong-Module-,
Boolean-Diagnose-, falsche Exit- und Receipt-Mismatch-Kontrollen erhalten.
Unabhängige selektierte Cases benötigen frische getrennte Bundles. Required-
Auswahl nicht verkleinern; kein HTTP, Startup, Reload oder Full E2E behaupten.

## Implementierungsentscheidung und Begründung

Den bestehenden begrenzten Treiber um zwei explizite Case-Deskriptoren erweitern,
nicht um eine generische Phase-0-Ausnahme. Selektiertes `invalid_size` in seinem
eigenen frischen Verzeichnis `configtests/invalid_size` ausführen. Vorherige
Boolean-Realisierung und bestehenden Collector-Vertrag erhalten. Das Companion-
Framework besitzt unabhängig Katalog-/Receipt-Validierung und case-spezifische
kanonische Aufbewahrung.

## Security-Auswirkung

Nichtfolgenden Regular-File-Snapshots, 64-MiB-Binary-/Modulgrenzen,
64 KiB gemeinsame Captures, 10-Sekunden-Deadline, expliziten Argumentvektor und
minimale Umgebung erhalten. PASS verlangt weiterhin exakte Directive/Wert,
Exit und beide Parserfragmente. Keine Guardrail, kein Validator, Common oder
MRTS wird abgeschwächt.

## Geänderte Dateien

- `ci/runtime/lifecycle/run-nginx-configtest.py`
- `ci/runtime/lifecycle/run-selected-nginx-configtests.py`
- `tests/test_nginx_configtest_driver.py`
- `tests/test_nginx_selected_configtest_wiring.py`
- `docs/testing-and-evidence.md` / `.de.md`
- Dieses Record-Paar und Archive-Index-Paar

## Ausgeführte Befehle

Der Coordinator beobachtete einen frischen RTK-gewrappten Parent-Fokus:
191 Tests bestehen in 65.658 Sekunden, Exit 0; aufbewahrtes Log und Exit-Receipt
liegen unter `analysis/parent-config-size-focus-20261003.log` und `.exit` im
externen Taskspeicher. Die fokussierten Driver-/Wiring-Prüfungen bestanden mit
24 Tests. Frische RTK-gewrappte Parent-Prüfungen `check-bilingual-docs` /
`check-doc-links` und Repository-Pfadprüfungen bestanden mit owning Interpreter
und externen Build-/Temp-Roots. `rtk proxy git diff --check` bestand in beiden
Repositories. Die getrennte Companion-Framework-No-CRS-Suite bestand mit 166
Tests in 111.503 Sekunden und ihre öffentliche API-Suite mit 23 Tests in
28.847 Sekunden, jeweils Exit 0; diese zertifizieren keine Parent-Hostausführung.
Vollständiges Framework-Precommit-`make lint` endete mit Exit 0; die vom Nutzer
verlangte Postcommit-Wiederholung ist eine separate spätere Verifikation.
Parent-Python-Kompilierung, Shell-Syntax und ShellCheck auf Error-Level bestanden.

## Runtime-Evidence

Die echte Producer → Collector → Canonical-Finalizer-Diagnose
`runs/diagnosis/nginx-config-size-retained-6si2byjk` unter
`/var/tmp/codex/ModSecurity-conector` erzeugt individuelles `invalid_size` PASS
und Wrong-Module FAIL. Beide echten NGINX-Invocations haben Exit 1. Jede hat
fünf aufbewahrte Operationsdateien; alle acht kanonischen Validatoren melden
null Fehler. Alle 47 aufbewahrten Checksums wurden geprüft. Beide Aggregate
bleiben FAIL, ohne Starts, Requests oder Events. Dies ist Precommit-Evidence
mit verändertem Source-Worktree und aufbewahrten gecachten C-Artefakten, kein
neuer Exact-Head-Build oder Full-Lifecycle-Nachweis.

## Nicht ausgeführte Prüfungen mit Begründung

Full E2E, Protocol-Wiring, Gitlink-Updates, Pushes, PR-Mutation und Merge sind
aus diesem Teil ausgeschlossen. Root-Master-/nobody-Worker-Nachweis ist für
reines `nginx -t` nicht anwendbar. Postcommit-Framework-Lint wird separat
nachverfolgt und durch diesen Record nicht als künftiges PASS vorweggenommen.

## Bekannte Einschränkungen

Nur `invalid_boolean` und `invalid_size` besitzen implementierte geschlossene
Configtest-Realisierungen. Frisches `measure-nginx-config-size.py` prüft echte
Bytes, Run-Identitäten, alle acht Validatoren und alle 47 Checksums erneut:
Open Paths sanken 52 → 51, Konfiguration 9 → 8, bei unveränderten 97 required
selektierten Records. Dies erfüllt die verbleibenden Pfade nicht.

## Verbleibende Risiken

Vertrauenswürdige gecachte C-Inputs und unabhängiges Source-/Run-Identity-Binding
bleiben nötig. Snapshots ausgeführter Bytes beweisen keinen neuen quellgenauen
C-Build. Acht Konfigurationspfade und weitere Pflichtszenarien bleiben unerfüllt.

## Finaler Diff- und Review-Status

Unabhängiges Security-Review fand keinen Blocker. Der dauerhafte Shared-
Finalizer-Test bestand: Zwei Cases bewahren zehn getrennte Manifest-Einträge
auf; Cross-Case-Aliase und Bundle-Wiederverwendung bleiben abgewiesen. Der finale
fokussierte Diff bestand das Review für einen separaten lokalen Parent-Commit. Bestehende Protocol-
Änderungen liegen außerhalb dieses Teils und müssen unstaged bleiben.
Parent-Gitlinks und MRTS sind unverändert. PR #396 bleibt OPEN/DRAFT/UNMERGED;
keine Remote-Delivery und kein Exact-Head-E2E-PASS werden behauptet. Dieser Record
enthält keine Secrets oder rohen Logs.
