# Change Record: CR-20261119-local-prerequisite-autoprovision

**Sprache:** [English](CR-20261119-local-prerequisite-autoprovision.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261119-local-prerequisite-autoprovision |
| Datum (UTC) | 2026-11-19 |
| Basis-Revision | `b79c3d93efbb8330f121caf8fb7c1a7874195e57` |

## Motivation und Problemstellung

Lokale Läufe hingen von zwei manuell vorbereiteten Voraussetzungen ab.

- Python: Das Root-Makefile wählte `.venv/bin/python` nur, wenn eine manuell
  vorbereitete `.venv` existierte, und fiel sonst auf `python3` ohne die gelockte
  PyYAML-Abhängigkeit zurück. Die Framework-Diagnosen `doctor`/`doctor-quick`
  endeten mit `BLOCKED: venv missing (.venv/bin/python); run make setup-dev` (an
  der Basis-Revision beobachtet: Exit 77 des Framework-Targets, make-Exit 2). Der
  dokumentierte Weg `make setup-dev` installiert ein ungepinntes `pip`-Upgrade
  und einen PyYAML-Versionsbereich, den die Python-Policy des Repositorys nicht
  als automatische Quelle zulässt.
- Sicherheitswerkzeuge: Die Workflow-Fixture-Checks lesen nur das
  checksum-geprüfte `$RUNNER_TEMP/security-tools/zizmor`. Lokal stellte es nichts
  bereit, daher endete `make test` mit `FAIL: checksum-verified zizmor executable
  is unavailable` (beobachtet: Exit 2 nach 282 s). Ein `zizmor` auf `PATH`
  (beobachtet `1.29.0`, der Lock pinnt `v1.32.0`) wird bewusst nicht verwendet.
  Die Go-Analysewerkzeuge waren im Repository gar nicht gepinnt; ein lokal
  installiertes älteres `staticcheck` konnte Go-1.27-Exportdaten nicht lesen.

Beides muss stattdessen immer zum aktuellen Versionsvertrag passen und nur dort
entstehen, wo ein lokaler Lauf es braucht.

## Akzeptanzkriterien

- Ein lokaler `make`-Aufruf jedes an das Framework delegierten Targets sowie von
  `framework-native-selftest`/`framework-go-test` stellt zuerst eine
  Python-Umgebung für den exakten Interpreter aus `.python-version` sicher; kein
  manueller Schritt.
- Die Umgebung erhält Abhängigkeiten nur über das Framework-eigene,
  hash-verifizierende `install-ci-dependencies.py`.
- Eine geänderte `.python-version`, ein geänderter Framework-Lock,
  Framework-Installer oder Helper sowie ein abweichender installierter Inhalt
  führen jeweils zu einer neu bereitgestellten Umgebung; eine abgebrochene
  Bereitstellung wird wiederholt und nicht als unverwaltet gemeldet.
- Ein fehlender exakter Interpreter ist `BLOCKED` (Exit 77); nichts wird ersetzt.
- Umgebungen können außerhalb des Checkouts liegen (`PYTHON_ENV_ROOT`); der
  Checkout trägt dann nur einen ignorierten `.venv`-Link. Eine getrennte
  Framework-eigene Umgebung ist auf Anforderung verfügbar.
- Mit gesetztem `RUNNER_TEMP` installieren delegierte Targets zuerst die
  gelockten Release-Werkzeuge und die neu gelockten Go-Werkzeuge zur Laufzeit in
  das laufprivate `$RUNNER_TEMP/security-tools`, als reguläre Dateien gemäß Lock;
  anderswo wird nichts installiert.
- CI (`CI` oder `GITHUB_ACTIONS` ist `true`) und ein explizit gewähltes `PYTHON`
  behalten ihr bisheriges Verhalten.
- Vorhandene unverwaltete `.venv`-Verzeichnisse, fremde Links und verlinkte
  Werkzeugverzeichnisse werden nie verändert.
- Die bestehenden Makefile-Verträge des Frameworks bleiben erfüllt.

## Implementierungsentscheidung und Begründung

- `ci/tools/ensure-python-env.py` (nur Standardbibliothek). Seine Identität ist
  der SHA-256 über exakte Interpreter-Version und realen Pfad,
  `.python-version`, den Helper selbst und die gepinnten Framework-Eingaben
  `connector_suite/requirements-ci.lock`, `connector_suite/requirements-ci-build.lock`,
  `connector_suite/modsecurity_connector_ci/tools/install-ci-dependencies.py` und
  `requirements-ci.lock`. Ein Stempel hält Identität, Eingaben,
  Installer-Receipt und eine Prüfung der installierten Distributionen fest; der
  schnelle Pfad akzeptiert nur eine passende Identität mit unveränderter Prüfung.
  Vor dem Entfernen alter vom Helper verwalteter Inhalte wird ein vorläufiger
  Stempel (`state: incomplete`) geschrieben. Die Bereinigung erhält diesen
  Stempel, entfernt Symlinks ohne ihnen zu folgen und ruft `venv` ohne
  `--clear` auf. Fehlgeschlagenes Anlegen und abgebrochene Bereinigung erhalten
  die Eigentumskennzeichnung für den nächsten Versuch.
- Ohne `PYTHON_ENV_ROOT` ist die Umgebung `.venv` im Checkout. Mit dieser
  Variable liegen versionierte Umgebungen `<role>-<version>-<identity>` in diesem
  Speicher, die Links `parent`/`framework` zeigen auf die zuletzt bereitgestellte
  und werden repariert, wenn sie fehlen, und `.venv` verweist auf die exakte
  Umgebung dieses Checkouts; ein vorhandener vom Helper angelegter Link wählt
  seinen Speicher automatisch. Die Bereitstellung hält ein exklusives `flock` auf
  dem Speicher- bzw. Checkout-Verzeichnis.
- `ci/tooling/go-tools.lock.json` pinnt `staticcheck` (`honnef.co/go/tools`
  `v0.8.2`, MIT) und `govulncheck` (`golang.org/x/vuln` `v1.10.0`,
  BSD-3-Clause) mit ihren `h1:`-Modulsummen.
- `ci/tools/ensure-security-tools.py` installiert jedes Release-Werkzeug aus
  `ci/tooling/security-tools.lock.yml` über das bestehende checksum-prüfende
  `fetch_security_tool.py` und jedes Go-Werkzeug per `go install` mit dem Go aus
  `.go-version` (`GOTOOLCHAIN=local`, `CGO_ENABLED=0`, `-trimpath`) nach Prüfung
  der Modulsumme und prüft danach die Build-Informationen der Binary. Ein Stempel
  je Werkzeug hält den erzeugenden Lock-Eintrag fest; fehlende, geänderte,
  verlinkte oder ungestempelte Binaries werden unter exklusivem `flock` atomar
  über ein Staging-Verzeichnis ersetzt. Eine andere Go-Toolchain blockiert nur
  die Go-Werkzeuge.
- Root-`Makefile`: `PYTHON_ENV_AUTO`, `PYTHON_ENV_ROOT`, `PYTHON_BASE` und
  `SECURITY_TOOLS_AUTO`; `FORCE` (Voraussetzung der unveränderten
  `%`-Weiterleitung) hängt von `python-env` und `security-tools-auto` ab, die
  beiden direkten Framework-Einstiege von `python-env`, sodass der bestehende
  `.venv/bin/python`-Default des Framework-Sub-Makes die bereitgestellte Umgebung
  findet. `security-tools` ist die strikte ausdrückliche Form; der automatische
  Schritt meldet ein nicht installierbares Werkzeug als Warnung, sodass nur die
  Checks fehlschlagen, die es benötigen. Lokal führen
  `setup-dev`/`install-dev-deps` zum verwalteten Python-Schritt statt zum
  ungepinnten Framework-Bootstrap. Die vom Framework-Vertrag festgeschriebenen
  Rezeptzeilen der `%`-Weiterleitung und von `framework-native-selftest` sind
  unverändert.
- `python-env-framework` stellt eine getrennte Umgebung bereit, die mit
  `--framework-lock modules/ModSecurity-test-Framework/requirements-ci.lock`
  validiert wird; sie benötigt einen Speicher und entsteht nur auf Anforderung.
- `.gitignore` ignoriert `.venv` als Verzeichnis oder Link.
- Keine Framework- oder MRTS-Datei wurde geändert. Die Pfadprüfung in
  Framework-`doctor.sh` wird durch die bereitgestellte `.venv` erfüllt; ihre
  Entkopplung ist eine getrennte Framework-Aufgabe.

## Geänderte Dateien

- `.gitignore`
- `Makefile`
- `ci/tools/ensure-python-env.py` (neu)
- `ci/tools/ensure-security-tools.py` (neu)
- `ci/tooling/go-tools.lock.json` (neu)
- `ci/README.md`, `ci/README.de.md`
- `docs/build/README.md`, `docs/build/README.de.md`
- `docs/getting-started.md`, `docs/getting-started.de.md`
- `docs/reference/variables.md`, `docs/reference/variables.de.md`
- `docs/security/ci-security-tooling.md`, `docs/security/ci-security-tooling.de.md`
- `reports/audits/change-records/CR-20261119-local-prerequisite-autoprovision.md`,
  `reports/audits/change-records/CR-20261119-local-prerequisite-autoprovision.de.md`

## Ausgeführte Befehle

Alle Befehle liefen über `rtk bypass` in einem Task-Worktree an der
Basis-Revision mit dem gepinnten Framework
`95f228936efe17fda24f21323ad87cd698940b48` und MRTS
`ee2174431c4edf97e66afe32558ce8454deb2397`, ohne `PYTHON`-Override und mit
externen Build-/Temporärwurzeln. Die Szenario-Suiten liefen gegen die finalen
Helper-Versionen.

| Befehl | Ergebnis |
| --- | --- |
| `make doctor-quick` vor der Änderung | Exit 2: `BLOCKED: venv missing (.venv/bin/python)` und fehlendes PyYAML mit `PYTHON=python3` |
| `make test` mit leerem `RUNNER_TEMP`, vor dem Sicherheitswerkzeug-Helper | Exit 2 nach 282 s: `FAIL: checksum-verified zizmor executable is unavailable` |
| Python-Szenario-Suite, 22 Prüfungen | alle bestanden: Bereitstellung im Checkout (`pip 26.2.2`, `pyyaml 6.0.3`, Receipt `libyaml_extension: false`); schneller Pfad etwa 0,6 s; `doctor-quick` Exit 0 mit `venv: detected`; Abweichung neu bereitgestellt; `.python-version` `3.15.9` blockiert (77, make 2); Speicher-Migration, -Erkennung und Links `parent`/`framework`; Framework-Umgebung sowie `BLOCKED` ohne Speicher; CI und explizites `PYTHON` nicht verwaltet; unverwaltetes Verzeichnis und fremder Link blockiert und unverändert; gleichzeitige Läufe stellen einmal bereit; fehlende Links ohne Bereitstellung repariert; ein abgebrochener Lauf (Download über einen nicht erreichbaren Proxy) erfolgreich wiederholt |
| derselbe Abbruch-Fall mit dem Helper vor dem vorläufigen Stempel | Wiederholung `BLOCKED: ... is an unmanaged environment` (Defekt reproduziert, dann behoben) |
| `make security-tools RUNNER_TEMP=<frisch>` | Exit 0: `actionlint 1.7.12`, `zizmor 1.32.0`, `gitleaks 8.30.1`, `staticcheck 2026.2.2 (0.8.2)`, `govulncheck v1.10.0`; Verzeichnismodus `0700`; Wiederholung etwa 0,4 s |
| Sicherheitswerkzeug-Szenario-Suite, 12 Prüfungen | alle bestanden: ungestempelte Werkzeuge ersetzt; ein veralteter Stempel installiert nur dieses Werkzeug neu; ein verlinktes Werkzeug wird ersetzt, ohne sein Ziel zu berühren; ein anderes Go blockiert nur die Go-Werkzeuge (77), während der automatische Hook warnt und das Target läuft; ein verlinktes Zielverzeichnis wird abgelehnt; keine automatische Installation in CI oder ohne `RUNNER_TEMP`; gleichzeitige Läufe installieren einmal; `check-workflow-fixture.sh insecure`/`safe` melden `reject`/`accept` |
| gelocktes `staticcheck` auf `connectors/envoy/ext_proc` | läuft auf Go-1.27-Code (kein Exportdaten-Fehler); meldet bestehende `ST1005`/`U1000`-Befunde, hier nicht geändert |
| `make check-remaining-connectors-build-wiring`, `check-repository-architecture`, `check-python-version-contract`, `check-project-versions`, `check-active-inventory`, `check-framework` | jeweils Exit 0 |
| `ci/tools/new-change-record.py check`; `make check-variable-documentation`; `make check-doc-links`; `make check-bilingual-docs` | jeweils Exit 0 |
| `make quick-check` auf dem finalen Diff, Umgebung aus dem lokalen `msc-test-env.sh` mit frischem `RUNNER_TEMP` | Exit 0 nach 814 s; der automatische Schritt installierte zuerst alle fünf Werkzeuge, der Python-Schritt nahm den schnellen Pfad |
| `make test` mit einer früheren Helper-Revision | Exit 2 nach 1808 s; die vier Workflow-Fixture-Ausführungen bestanden mit dem laufprivaten `zizmor`; `runtime.no-crs.apache` lief mit 0 fehlgeschlagenen Fällen, sein Evidence-Gate verweigerte PASS aber, weil der Worktree nicht sauber war; das gecachte `httpd` löste außerdem `libpcre2-8` aus dem Systembibliothekspfad auf, daher ist dieser Lauf keine gültige Runtime-Evidence |

## Nacharbeit zur Wiederholung der Bereitstellung, 2026-11-21

Der veröffentlichte Helper schrieb seinen vorläufigen Stempel nach
`venv --clear`. Ein Fehler in diesem Unterprozess konnte eine teilweise
angelegte Umgebung ohne Stempel hinterlassen, die beim nächsten Versuch als
unverwaltet abgelehnt wurde. Die Nacharbeit erhält den Stempel während der
Bereinigung alter Inhalte und beim Anlegen der Umgebung.

Eine Task-eigene Regressionstest-Suite aus der Standardbibliothek außerhalb des
Checkouts reproduzierte den fehlenden Stempel mit dem veröffentlichten Helper.
Nach der Änderung bestanden alle fünf Fälle. Sie prüfen fehlgeschlagenes Anlegen
mit erneutem Versuch, abgebrochene Bereinigung, den Erhalt einer unverwalteten
Umgebung, sicheres Entfernen von Symlinks und das echte lokale Anlegen einer Venv
mit `pip check`. Nur im Fall mit echter Venv wurde der geprüfte
Abhängigkeitsinstaller durch einen Stub ersetzt. Es wurden keine Pakete
heruntergeladen. Die Parent-eigene Python-Umgebung führte diese Prüfungen aus.
Ruff war in dieser Umgebung nicht verfügbar.

## Security-Auswirkung

Die Installation von Abhängigkeiten und Werkzeugen wird für lokale Läufe
eingeengt: Python-Pakete kommen nur von den exakten offiziellen URLs und
SHA-256-Pins des Framework-Installers (reines Python-PyYAML ohne C-Erweiterung);
Release-Werkzeuge nur von ihren gelockten offiziellen Assets mit
SHA-256-Prüfung; Go-Werkzeuge nur aus exakten Modulversionen, deren `h1:`-Summe
vor und deren Build-Informationen nach dem Build geprüft werden. Die erste
Installation lädt diese gelockten Artefakte herunter (`files.pythonhosted.org`,
GitHub-Releases, Go-Modul-Proxy mit Checksum-Datenbank). Der ungepinnte
`setup-dev`-Bootstrap wird lokal nicht mehr verwendet. Die Helper lehnen einen
Speicher im Checkout oder ein verlinktes Werkzeugverzeichnis ab, ersetzen nur
ihre eigenen Links und gestempelten Artefakte und löschen nie unverwaltete
Umgebungen. CI-Verhalten, Workflows, Scanner und Quality Gates sind unverändert.

## Runtime-Evidence

Nicht anwendbar: Weder Connector-Produktcode noch Host-Konfiguration oder
Runtime-Pfade wurden geändert. Die obigen Prüfungen sind ausschließlich
Nachweise für lokales Tooling.

## Bekannte Einschränkungen

- Der erste lokale Lauf und jede Identitäts- oder Lock-Änderung benötigen
  Netzzugriff sowie etwa eine halbe Minute für Python und bis etwa eine Minute
  für die Go-Builds.
- Ein exakter Interpreter aus `.python-version` muss vorhanden sein; sonst ist
  jedes delegierte Target `BLOCKED`, bis `PYTHON_BASE` oder ein explizites
  `PYTHON` gesetzt ist. Die Go-Werkzeuge benötigen die exakte Toolchain aus
  `.go-version`.
- Abgelöste Umgebungen in einem Speicher werden nicht automatisch entfernt.
- Innerhalb des Framework-Sub-Makes rufen `bootstrap-all` und
  `cloud-quick-check` weiterhin das Framework-eigene `setup-dev` auf; ein
  späterer Lauf erkennt die Abweichung und stellt erneut bereit. Das
  eigenständige Framework-Makefile stellt nichts bereit.
- Jedes lokal delegierte Target ergänzt beide Prüfungen (zusammen etwa 1 s).

## Verbleibende Risiken

Entfernt der Anbieter ein gelocktes Artefakt, blockieren neue Installationen,
bis die Locks aktualisiert sind. `govulncheck`-Ergebnisse hängen zur Laufzeit von
der Online-Schwachstellendatenbank ab.

## Nicht ausgeführte Prüfungen mit Begründung

- Die aktuellen SonarCloud-Befunde und CI-Ergebnisse sind nach Veröffentlichung
  der Nacharbeit zu prüfen.
- `make test` auf einer sauberen committeten Revision mit den gepinnten
  PCRE2-/APR-Laufzeitbibliotheken wurde nicht ausgeführt; die früheren Läufe oben
  gelten nicht als bestanden.
- Gehostete CI läuft erst nach dem Push.
- Der lokale Git-pre-commit/pre-push-Secrets-Hook konnte nicht laufen, weil sein
  Integrationsbeleg fehlte; auf ausdrückliche Entscheidung des Nutzers wurden
  Commit und Push ohne ihn ausgeführt. Ein manueller Secrets-Scan jedes gestagten
  Blobs bestand.

## Finaler Diff- und Review-Status

Task-Branch `claude/python-env-autoprovision-20261119`, als Draft-Pull-Request zur
Prüfung geliefert; ein Merge ist nicht Teil dieser Änderung.

Der Security-Tool-Helfer bindet den kanonischen Zielpfad an das unabhängig konfigurierte Verzeichnis `RUNNER_TEMP/security-tools` und prüft die Checkout-Grenze vor der Installation. Das Root-Makefile exportiert diesen Laufkontext. Direkte Helper-Aufrufe müssen ihn konfigurieren, und `--base` bestätigt den Interpreter, der den Python-Umgebungshelper bereits ausführt. `PYTHON_BASE` wählt weiterhin den Interpreter, mit dem das Makefile den Helper startet. Acht Zielpfadprüfungen, fünf Interpreter-Identitätsprüfungen, fünf Bereitstellungs-Wiederholungsprüfungen und die Prüfung des Makefile-Umgebungsexports bestanden. Der SonarCloud-Befundstand für diese Nacharbeit ist nach Veröffentlichung zu prüfen.
