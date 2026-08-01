# FND-PARENT-0055 — Apache-Upstream-Integrationsadapter lehnten ihren eigenen task-lokalen Runtime-Vertrag ab

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-PARENT-0055 |
| Kategorie | test_failure |
| Repository / Ownership | parent / parent |
| Priorität / Schweregrad / Konfidenz | P1 / not_applicable / validated |
| Status / Machbarkeit | blocked / feasible_now |
| Release-Blocker / sicherheitsrelevant | false / true |
| Scope | Parent-Apache-Request-Body-Regression- und Valgrind-Soak-Adapter |
| Framework- / MRTS-Auswirkung | read-only / unverändert |

## Beobachtung und Auswirkung

Der anfängliche Parent-Request-Body-Adapter übergab eine generierte externe
YAML über `TEST_CASE`, ohne ihr Konfigurationsverzeichnis über die
Framework-unterstützte `EXTRA_CASE_ROOTS`-Grenze zu registrieren. Framework
lehnte die Case-Datei deshalb vor dem Apache-Start als außerhalb des
ausgewählten Scopes ab.

Der anfängliche Parent-Soak-Adapter verwendete den POSIX-Shell-globalen
Variablennamen `candidate` in verschachtelten Validatoren erneut. Der
Vorfahrenläufer änderte den validierten externen Root des Callers auf `/`, was
einen Versuch eines Run-Verzeichnisses unter `//apache-soak-*` verursachte,
bevor ein Valgrind- oder Apache-Prozess beginnen konnte.

Dies waren Test-Adapterdefekte, kein produktives Apache-Verhalten und kein
Security-Exploit. Sie verhinderten, dass erforderliche Evidence die echten
Umgebungsvoraussetzungen erreichte, und sind jetzt an dieser
Preflight-Grenze als repariert verifiziert.

## Scope und Einschränkungen

Die Korrektur ist ausschließlich Parent-seitig. Sie fügt das generierte
Konfigurationsverzeichnis als einzigen zusätzlichen Case-Root hinzu, aktiviert
die No-CRS-Baseline des Fixtures und lässt alle Framework-Quellen, MRTS,
Gitlinks, Docker-/Compose-Assets, produktiven Handler, Pfadkontrollen und
Artefaktbudgets unverändert.

## Behebung und Validierung

Der Request-Body-Adapter setzt `EXTRA_CASE_ROOTS` jetzt genau auf sein
task-lokales Konfigurationsverzeichnis und `NO_CRS_BASELINE=1`. Der
Soak-Adapter verwendet unterschiedliche Variablen für äußeres Verzeichnis,
Pfadprüfung und Vorfahrenlauf und behält seine Checks für absolute Pfade,
Symlinks und außerhalb des Checkouts bei.

- `make check-apache-request-body-regression-wiring` bestand: 8 Tests und Shell-Syntax.
- `make check-apache-soak-wiring` bestand: 12 Tests und Shell-Syntax.
- Der Request-Body-Rerun löste seine externe Case-Datei auf und blockierte
  danach nur am fehlenden vorbereiteten Apache-`httpd`; der frühere
  Scope-Fehler trat nicht auf.
- Die Memcheck- und Helgrind-Reruns schrieben jeweils begrenzte task-lokale
  Berichte und blockierten danach nur wegen fehlendem Valgrind; der frühere
  Pfadfehler `//apache-soak-*` trat nicht auf.

## Akzeptanzkriterien

1. Die externe Request-Body-YAML wird über `CASE_SCOPE=all`, ein begrenztes
   `EXTRA_CASE_ROOTS` und die No-CRS-Baseline aufgelöst.
2. Ein gültiger externer Soak-Root bleibt über verschachtelte Shell-Helper
   unverändert und wird niemals zu `/` reduziert.
3. Beide fokussierten Parent-Contract-Suiten bestehen.
4. Reruns erreichen nur legitime Apache-/Valgrind-Prerequisite-Blocker.
5. Eine künftig vorbereitete Umgebung führt native Request-Body-, Memcheck-
   und Helgrind-Evidence aus, ohne einen Blocker als Erfolg zu behandeln.

## Evidence und Einschränkung

Zurückbehaltenes Artefakt:
`.codex/runs/20260726T083705Z-apache-upstream-pr-91-94-integration/evidence/apache-adapter-preflight-repair.md`
(SHA-256 `a7ddb2d028d70914dd98178a8913b3c91d74af9f84d27b5d4ada72b8f3609ce5`).

Der stärkste verfügbare Nachweis führte beide ursprünglichen Adapter-Entry-
Points bis zur nächsten legitimen fehlgeschlossenen Voraussetzung erneut aus.
Der Umgebung fehlen ein vorbereiteter Apache-Runtime und Valgrind; daher wird
kein natives HTTP-Ergebnis, Memory-Leak-Ergebnis oder Race-Ergebnis behauptet.

## Restrisiko

Die reparierten Verträge sind lokal verifiziert, aber native Request-Body-,
Memcheck- und Helgrind-Absicherung bleibt durch die separate lokale
Tooling-Bedingung (`FND-HOST-0002`) blockiert. Kein Gate wurde umgangen und
kein Risiko wird akzeptiert.

## Historie

- 2026-07-26 — Die während des Parent-Upstream-PR-#91–#94-Adapter-Preflights
  beobachteten External-Case-Scope- und Shell-Variable-Collision-Fehler
  aufgezeichnet.
- 2026-07-26 — Die engen ausschließlich Parent-seitigen Korrekturen angewandt,
  beide Static-Suiten bestanden und bis zu den legitimen fehlenden-
  `httpd`-/fehlenden-Valgrind-Blockern erneut ausgeführt. Das Finding ist
  verifiziert, aber kein Nachweis eines nativen Runtime-Erfolgs.
