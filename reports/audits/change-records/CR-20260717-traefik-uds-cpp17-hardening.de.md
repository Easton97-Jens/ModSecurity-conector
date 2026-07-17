# Change Record: Traefik-UDS- und C++-Evaluator-Härtung

**Status:** lokale Implementierung und fokussierte Validierung sind partial; Delivery-Disposition ist ein Parent-only-Draft-PR ohne Merge; Remote-CI und Review bleiben ausstehend

**Sprache:** [English](CR-20260717-traefik-uds-cpp17-hardening.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260717-traefik-uds-cpp17-hardening` |
| Datum (UTC) | `2026-07-17` |
| Basis-Revision | `02f9f98cdbbdd70bbc530ac1399974e53884f4e9` |
| Scope | Nur Parent-Repository |
| Zugehörige Findings | `FND-FRAMEWORK-0008`, `FND-PARENT-0012`, `FND-PARENT-0013`, `FND-PARENT-0014`, `FND-PARENT-0015` |

## Motivation und Problemstellung

Der native Traefik-Smoke-Runner konnte einen zu langen Unix-Domain-Socket-Pfad
erzwingen und bot keine validierte Short-Parent-Auswahl. Sein UDS-Lifecycle
benötigte außerdem explizite Collision-, Path-, Identity- und Cleanup-Controls.
Separat hatte der C++-Targeted-Evaluator interne gleich typisierte String-
Schnittstellen, die künftige Fehler in der Argumentreihenfolge unnötig leicht
machten.

## Akzeptanzkriterien

- Ein nativer Runner wählt einen kurzen task-owned UDS-Parent über expliziten
  Wert, `TMPDIR` oder erzeugten privaten Fallback und lehnt unsichere Pfade ab.
- Fokussierte Tests decken Länge, relative Pfade, Symlinks, vorhandene Sockets,
  parallele Allokation, Setup-Fehler, YAML-Quoting und Cleanup-Refusal ab.
- Der C17-Service lehnt Pre-Bind-, Post-Bind- und Post-Probe-
  Pathname-Replacements ab, bevor Listener-Ownership erfasst wird.
- Der bestehende Protocol-Lifecycle behält Allow- und Blocking-Controls;
  gewöhnliches fokussiertes Cleanup ist abgedeckt, ohne Same-UID-Race-Proof-
  Deletion oder Live-Endpoint-Identity zu behaupten.
- Der Evaluator kompiliert mit C++17 `-Wall -Wextra -Werror` und erhält das
  direkte Allow/Block-Ergebnis bei weniger vertauschbaren internen Eingaben.

## Implementierungsentscheidung und Begründung

Der Python-Runner priorisiert `TRAEFIK_ENGINE_SOCKET_PARENT` vor `TMPDIR` und
erzeugt danach einen kurzen privaten Fallback. Er validiert absolute, dem
aktuellen Benutzer gehörende `0700`-Parents außerhalb des Checkouts, lehnt
Symlink-Komponenten/Steuerzeichen ab, JSON-quotiert die erzeugte YAML und
speichert Directory-Identity vor Cleanup-Checks. Diese Checks verweigern
beobachtete Abweichung oder Restinhalte; sie sind keine atomare Same-UID-
Deletion-Garantie.

Der C-Service verwendet descriptor-basierte Rechte und erfasst Socket-Identity.
Vor der Bereitschaft führt er unter Linux eine begrenzte nichtblockierende
lokale UDS-Probe aus und verlangt, dass der akzeptierte `SO_PEERCRED`-Peer der
Engine-Prozess ist. Er vergleicht die `lstat()`-Identity unmittelbar vor und
nach der Probe. Deterministische Selbsttest-Hooks decken Replacement vor Bind,
nach Bind und nach der Probe ab.

Der Evaluator verwendet `std::string_view` für den unveränderlichen Field-Key
und einen benannten `DecisionLogInput`-Wert für den Decision-Log-Aufruf. Dies
ändert nur interne Schnittstellen, keine öffentliche API und kein ausgegebenes
Decision-Verhalten.

## Geänderte Dateien

- `common/scripts/modsecurity_targeted_eval.cc`
- `connectors/traefik/scripts/runtime_native_smoke.py`
- `connectors/traefik/src/traefik_engine_service.c`
- `connectors/traefik/build/test-engine-service-runtime.sh`
- `tests/test_traefik_native_local_plugin.py`
- `connectors/traefik/README.md` und `connectors/traefik/README.de.md`
- `docs/connectors/README.md` und `docs/connectors/README.de.md`
- `docs/reference/variables.md` und `docs/reference/variables.de.md`
- Dieser bilinguale Change Record und seine bilingualen Indexeinträge in
  `reports/audits/change-records/README.md` und
  `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

Alle Befehle liefen aus `/root/git/ModSecurity-conector` mit task-owned Output
unter `/var/tmp/codex/ModSecurity-conector/runs/20260717T114213Z-feasibility-runtime-remediation-838d9adc/`.

- `make -C connectors/traefik test-engine-service` mit expliziten task-owned
  Build-/Socket-Roots und verifizierten lokalen libmodsecurity-Include-/Library-
  Pfaden — bestanden; retained als
  `logs/056-traefik-engine-service-double-observation-race-regression.log`
  (SHA-256 `fd8d6bafee0adf474880625b73c26e719a114e60d44036fb141fc940658b36da`).
- `python -B -m unittest -v tests.test_traefik_native_local_plugin` — 13 Tests
  bestanden; retained als
  `logs/057-traefik-native-local-plugin-double-observation-contract.log`
  (SHA-256 `8103a918dbb83bd07437f347cf9d30c6484391821b8459a8e5510fd05ad15dae`).
- Dieselbe fokussierte Python-Contract-Suite wurde nach einer reinen
  Test-Portabilitätskorrektur erneut ausgeführt — 14 Tests bestanden; retained
  als `logs/073-traefik-native-local-plugin-portable-contract-final-rerun.log`
  (SHA-256 `fc511f1554f3cb31ae1105854cdb6b82d51476139f41189cb73e10b48b40adcb`).
- Das kanonische Roh-C++-Evidence-Manifest ist
  `evidence/cpp17-revalidation-evidence-manifest.json`. Es enthält für jede
  abgeschlossene aktuelle Verifikation exakten Befehl, CWD, UTC-Start/-Ende,
  Exit-Ergebnis, Raw-Log-Pfad, SHA-256 und Zusammenfassung. Aktuelle C++17-
  Compilation (`074`), Compilation-Database (`075`), Diagnostics-Contracts
  (`080`, fünf Tests) und Allow/Block-Controls (`081`) bestanden. Die aktuelle
  Swappable-Parameter-Reanalyse wurde vom Repository-Storage-Gate gestoppt
  (`076`, Exit `77`) und nicht umgangen; weil dieses Gate den Wrapper vor der
  Ausgabe eines Endzeitstempels stoppte, enthält das Manifest die Raw-Log-mtime
  als ausdrücklich gekennzeichnete End-Evidence. Erhaltene historische
  `031`/`032`-Static-Analysis-Evidence ist ebenfalls mit ihrer älteren
  fehlenden-Endzeitstempel-Schemaeinschränkung gekennzeichnet statt als neuer
  erfolgreicher Lauf behauptet zu werden.

## Security-Auswirkung

Die Änderung stärkt Path-Validierung, YAML-Serialisierung, UDS-Collision-
Handling, Replacement-Detection und Cleanup-Refusal. Der modellierte
Pre-Capture-Post-`bind`-Identity-Race ist geschlossen: Ein Replacement vor,
während oder unmittelbar nach der Selbstprobe wird nicht als engine-owned
erfasst.

`FND-PARENT-0013` bleibt offen: POSIX/Linux besitzt keine atomare bedingte
Unlink-by-Expected-Inode-Operation. Ein bösartiger Prozess mit derselben
Service-UID und veränderbarem Verzeichnis kann weiterhin das finale
`lstat()`-zu-`unlink()`-Intervall rennen. Dieser Record behauptet nicht, dass
das finale Cleanup Same-UID-Race-proof ist.

`FND-PARENT-0014` erfasst getrennt das analoge finale Manifest-Leaf-
Validierungs-zu-Entfernungs-Intervall. `FND-PARENT-0015` ist für den nativen
Host-Pfad folgenreicher: Nach Bereitschaft kann ein Same-UID-Mutator den Pfad
vor einem späteren Middleware-Dial neu binden. Der Client öffnet pro
Transaktion eine neue UDS-Verbindung und hat aktuell keine verifizierte Peer-
Identity-Bindung; ein Fake-Endpoint mit protokollgültigem Allow kann diese
Transaktion umleiten. Dies ist source-backed, aber ohne echte Host-
Reproduktion; es wird als P1/medium/probable und nicht als High oder confirmed
erfasst.

## Runtime-Evidence

Der kompilierte C17-Service bestand Protocol-Selbsttest, Socket-Ownership-
Selbsttest, normalen lokalen Protocol-Lifecycle und deliberate
Replacement-Sentinel-Negativkontrolle. In der Negativkontrolle ist
`socket_cleanup` das erwartete fail-closed Service-Ergebnis und der Test selbst
bestand.

Kein echter Traefik/libmodsecurity-Host-Lifecycle wurde ausgeführt: Die nötigen
Host-Binary-/Runtime-Eingaben fehlten, daher bleibt diese Evidence
`blocked_environment`.

## Bekannte Einschränkungen

- Der native Pathname-Listener scheitert außerhalb des für verifizierte
  Ownership-Capture verwendeten Linux-Peer-Credential-Mechanismus geschlossen.
- `FND-PARENT-0013` blockiert eine strikte Same-UID-No-Foreign-Socket-Cleanup-
  Behauptung.
- `FND-PARENT-0014` blockiert eine strikte Same-UID-No-Foreign-Manifest-Leaf-
  Deletion-Behauptung.
- `FND-PARENT-0015` blockiert eine strikte Same-UID-Live-Client-zu-Engine-
  Endpoint-Identity-Behauptung; die bestehende Selbstprobe gilt nur vor
  Bereitschaft.
- `0700` schützt über UIDs hinweg; es ist keine Isolation zwischen bösartigen
  Prozessen mit derselben Owner-UID.

## Verbleibende Risiken

Die finalen Pathname- und Manifest-Leaf-Deletion-Grenzen sind nicht
risikoakzeptiert. Eine künftige Lösung muss automatische Pathname-Deletion
vermeiden, getrennt vertraute Cleanup-Boundaries einführen oder einen
kompatiblen atomaren Expected-Object-Deletion-Mechanismus beweisen. Die Live-
Endpoint-Umleitungsgrenze benötigt zusätzlich ein verifiziertes Ende-zu-Ende-
Client-/Engine-Identity-Design; Abstract-AF_UNIX, Client-Peer-Credentials und
Descriptor-Handoff sind künftige Kandidaten, keine aktuellen verifizierten
Fixes.

## Nicht ausgeführte Prüfungen mit Begründung

- Echter nativer Traefik-Host-Lifecycle und vollständige CRS/MRTS-Profile wurden
  nicht ausgeführt, weil erforderliche Host-/Runtime-Eingaben fehlten; kein
  Download, keine Installation, kein Build und kein Retest wurde genutzt, um
  sie zu erzwingen.
- NGINX-, Apache- und MRTS-blockierte Items bleiben in ihren eigenen
  Feasibility-Dispositions; keine Framework- oder MRTS-Dateien wurden geändert.
- H3 was intentionally not investigated in this remediation task because no approved compatible client solution is currently available.

## Finaler Diff- und Review-Status

Der lokale Source-/Test-/Documentation-Diff ist partial, nicht security-
complete: Pre-Capture-Hardening, Short-Parent-Auswahl und fokussierte Controls
sind für Delivery-Review bereit, während `FND-PARENT-0013`,
`FND-PARENT-0014` und `FND-PARENT-0015` ohne Risikoakzeptanz blocked bleiben.
Zum Zeitpunkt der Record-Erstellung war er noch nicht committed, gepusht oder
als Draft PR eingereicht. Die Delivery-Disposition ist ein Parent-only-Draft-
PR ohne Merge-Autorisierung; als bestandene Remote-CI oder Review wird er nicht
dargestellt.
