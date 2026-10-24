# Change Record: NGINX-Docroot-Projektionen pro Invocation

**Sprache:** [English](CR-20260927-nginx-projection-invocations.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260927-nginx-projection-invocations` |
| Datum (UTC) | `2026-09-27` |
| Basis-Revision | `9fbaa70227b17d71c11005bc45984a11b9dd5dce` |
Framework: `cc36b37d0f6a0fbc3512f3878a691751e91c5fbb`.
MRTS: `615b13bacbd008562c17408246c41ab27dca3104`.

## Motivation und Problemstellung

Der Parent verwendete ein exaktes Projection Child für unabhängige NGINX-Cases
und natives First-Byte mehrfach. Der erste echte Request gelang; spätere
Invocations wurden vom unveränderten Fresh-Child-Guard korrekt verweigert.

## Akzeptanzkriterien

Jeder unabhängige Case- und First-Byte-Aufruf verwendet ein eigenes, noch nicht
existierendes, sicheres direktes Child des gemeinsamen externen Parents.
Wiederverwendung bleibt verboten. Die bisherigen Source-Map-/Containment-Fixes,
Framework/MRTS und Cache-Verträge bleiben unverändert. Exact-Head PASS erfordert
alle vorgesehenen Requests, Root-Master/nobody-Worker, Canonical PASS, Exit 0
und vollständige Evidence mit Prüfsummen.

## Implementierungsentscheidung und Begründung

Der Batch-Dispatch validiert den ursprünglichen Caller-Seed und wählt dann
Geschwisterpfade `nginx-case-<UUID>`. First-Byte validiert separat seinen Seed
und wählt `nginx-first-byte-<UUID>`. Namen bleiben auch mit einem 128 Zeichen
langen Seed begrenzt. Nur der bestehende Projector legt Children an. Direkte
Single-Case-Aufrufe behalten ihren Exact-Root-Vertrag. Baseline übergibt seinen
Canonical Verified Root explizit an First-Byte; dessen Standalone-Default des
Component-Wrappers bleibt erhalten.

## Security-Auswirkung

Freshness-, Containment-, No-Follow-, Ownership-, Worker-Identitäts- und
Private-Network-Kontrollen bleiben erhalten. Fehlerhafte/belegte Seeds werden
nicht stillschweigend repariert. Keine Projektion wird gelöscht oder erneut
verwendet. Private Source-, Regel-, Log-, Evidence- und Cache-Grenzen bleiben
getrennt. Canonical-Validatoren bleiben unverändert.

## Geänderte Dateien

- `connectors/nginx/harness/run_nginx_smoke.sh`
- `ci/runtime/lifecycle/run-native-first-byte.sh`
- `ci/runtime/lifecycle/run-no-crs-baseline.sh`
- `tests/test_nginx_projection_invocations.py`
- `tests/test_nginx_functional_materialization_layout.py`
- `connectors/nginx/harness/README.md` / `README.de.md`
- Dieses englisch/deutsche Change-Record-Paar.

## Ausgeführte Befehle

RTK umschließt jeden Shell-Befehl. Vor dem Fix scheiterten die drei fokussierten
Invocation-Regressionen an der Autorisierung des wiederverwendeten Childs.
Nach dem Fix decken Tests mit echtem Validator/Projector wiederholte Batches,
separates First-Byte, kombinierten Dispatch, ungültige Seeds und den Default
Verified Root ab. Benachbarte Resolver-, Collector-, Runner-, Master/Worker-,
Lifecycle- und Protokolltests bestanden mit 142 Tests. Die fokussierte Suite
bestand mit 34 Tests (insgesamt 176 Tests). Shell-Syntax bestand; ShellCheck
meldete 28 bestehende Diagnosen, identisch zu den normalisierten Basisdiagnosen,
ohne Unterdrückungen. Native Dokumentations-/Path-Policy-Ergebnisse stehen
vor dem Commit im externen Ausführungsplan.

## Runtime-Evidence

Die kleinen Regressionen führen echte Projection Guards an kontrollierten
Host-Schnittstellen aus; sie starten keine Server und behaupten keine
Request-Evidence. Das neue commitgebundene Exact-Head-E2E-Ergebnis und
SHA256SUMS werden nach dem Commit extern aufbewahrt.

## Nicht ausgeführte Prüfungen mit Begründung

Bei Erstellung dieses Records ist der Post-Commit-E2E noch nicht gelaufen.
Remote CI, SonarQube, Push, PR und Merge liegen außerhalb dieses lokalen Tasks.

## Bekannte Einschränkungen

Projection Freshness beweist allein keine vollständigen Canonical Events.
Fehlende Allow-Events werden erst nach Ausführung der vorgesehenen Requests
separat diagnostiziert; Validatoren und Erwartungen bleiben unverändert.

## Verbleibende Risiken

UUID-Kollisionen scheitern unter den bestehenden Freshness Guards geschlossen.
Native Cache-Wiederverwendung/Neubau bleibt normalen Provenance-Prüfungen
unterworfen. Echte Host-Ausführung ist für sämtliche Lifecycle- und
Canonical-Akzeptanzkriterien erforderlich.

## Finaler Diff- und Review-Status

Der fokussierte Parent-only-Diff erhält bestehende Commits und Repository Pins.
Die Auslieferung erfolgt als separater lokaler Commit mit anschließendem
frischem Exact-Head-Nachweis; History-Rewrite und Remote-Auslieferung sind nicht
autorisiert.
