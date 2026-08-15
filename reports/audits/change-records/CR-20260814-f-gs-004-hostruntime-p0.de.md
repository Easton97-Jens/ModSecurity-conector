# Change Record: F-GS-004 Hostruntime-P0-Härtung

**Sprache:** [English](CR-20260814-f-gs-004-hostruntime-p0.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260814-f-gs-004-hostruntime-p0 |
| Datum (UTC) | 2026-08-14 |
| Basis-Revision | ea3b48abab7940de49997a371f9117b409c05a2a |
| Delivery-Status | Der aktuelle User hat die Integration des Parent-[PR #287](https://github.com/Easton97-Jens/ModSecurity-conector/pull/287) nach `master` ausdrücklich autorisiert. Das Code- und Sonar-Follow-up unmittelbar vor diesem Delivery-Record-Update ist Head `04f1fb81549360b22719344dee90ec0196d63f19`: alle aktuellen PR-Checks waren terminal und bestanden, SonarQube Cloud meldete Quality Gate `OK` mit null neuen/akzeptierten Issues und null Security Hotspots, und es gab weder Reviews noch Review-Threads. Dieses gepaarte Record-Update benötigt vor dem autorisierten Merge eine frische Exact-Head-Validierung; zum Zeitpunkt dieses Commits wurde kein Pull Request gemergt. |

## Motivation und Problemstellung

F-GS-004 enthielt trotz eines historisch erfolgreichen HAProxy-HTX-Hostlaufs
einen pauschalen Blocker für Hostruntime-Abdeckung. Außerdem drifteten
Runtime-Komponentenversionen zwischen Parent- und Framework-Dokumentation,
und CI hatte keinen einheitlichen sicheren maschinenlesbaren Preflight sowie
keine einheitliche Runtime-Evidence-Projektion.

## Akzeptanzkriterien

- Das Framework besitzt einen validierten Lock für die sieben benannten
  Runtime-Profile; daraus abgeleitete Parent-Dokumentation stimmt überein,
  ohne den ungemergten Parent-Gitlink zu ändern.
- Parent-Preflight-Ergebnisse verwenden ausschließlich das begrenzte
  Statusvokabular und klassifizieren fehlende Hostvoraussetzungen als
  `BLOCKED`.
- Unvollständige Host-Evidence kann nicht zu `PASS` werden; Workflow-Uploads
  bleiben bereinigt und laufen auch für blockierte Ergebnisse.
- Distribution-ModSecurity-Header und -Bibliotheken werden für HAProxy HTX
  mit validierter Priorität, Architektur, Linkbarkeit und sicherer Ausgabe
  erkannt.
- Ein frischer echter HAProxy-3.2.21-HTX-Hostlauf weist Prozessstart,
  Konfiguration, Loopback-Anfragen, Ergebnisprüfungen und Bereinigung nach.

## Implementierungsentscheidung und Begründung

Framework-Draft-PR #79 führt den kanonischen Runtime-Component-Lock und die
gehärtete Downloadbehandlung ein. Der Parent verwendet diesen Lock pro Profil
im Preflight, lässt den aktuellen Framework-Gitlink unverändert und dokumentiert
die Abhängigkeit statt Framework-eigene Versionen zu kopieren.

Der Parent-Preflight erzeugt eine begrenzte JSON/Markdown-Projektion. Die vier
Connector-Workflows schreiben einen separaten Runtime-Record mit `NOT_RUN`,
solange ein vollständiger Host-Lifecycle nicht alle geforderten Nachweise
liefert. Connector-Makefile-Wrapper delegieren ohne rohen Shell-Argumentkanal
an den Root-Preflight. HAProxy sucht zuerst explizite Pfade, danach
`pkg-config` und dann bekannte Distributionspfade; Symlink-Ziele, Architektur,
`ldd`-Abhängigkeiten und die Eingabe für die erzeugte Environment-Datei werden
fail-closed validiert.

## Geänderte Dateien

- Parent-Preflight und Lifecycle-Evidence: `Makefile`,
  `ci/runtime/common/hostruntime_preflight.py`,
  `ci/runtime/common/hostruntime-preflight.py`,
  `ci/runtime/lifecycle/write-hostruntime-record.py` und
  `ci/runtime/lifecycle/run-no-crs-baseline.sh`.
- Parent-Workflows: `.github/workflows/test-nginx.yml`,
  `.github/workflows/test-haproxy.yml`, `.github/workflows/test-envoy.yml`
  und `.github/workflows/test-traefik.yml`.
- HAProxy-Integration: `connectors/haproxy/Makefile`,
  `connectors/haproxy/htx-overlay/resolve-modsecurity.sh` sowie HTX-Harness-
  Helper- und Runtime-Skripte.
- Connector-Makefile-Integration: `connectors/envoy/Makefile` und
  `connectors/traefik/Makefile`.
- Versionierte Dokumentation/Konfiguration: Compiler-Guides, Envoy-, Traefik-
  und HAProxy-Reader-Dokumentation sowie `scripts/generate_compiler_guides.py`
  und dieser gepaarte englische/deutsche Change Record.
- Fokussierte Tests: Hostruntime-Preflight, Workflow-Evidence,
  Lifecycle-Record, HAProxy-Resolver und HTX-Harness-Abdeckung.

Kein Parent-Gitlink, Framework-Quellcode, MRTS-Quellcode, Cache, Build-Output,
Secret oder Runtime-Log ist Teil der Parent-Änderung.

## PR-#287-SonarQube-Cloud- und Submodule-Follow-up

Der öffentliche SonarQube-Cloud-PR-Endpunkt meldete am initialen Follow-up-Head
drei task-eigene offene New Issues:

- `python:S1192` in `ci/runtime/common/hostruntime_preflight.py`: Das
  Diagnostikliteral `"runtime lock"` war dreimal wiederholt. Das Modul verwendet
  nun die einzelne Konstante `RUNTIME_LOCK_LABEL`, ohne Diagnostik zu ändern.
- `python:S1481` im selben Preflight-Modul: Eine unbenutzte lokale Variable
  `summary` wurde entfernt; der bestehende Ausgabe-Pfadausdruck bleibt
  unverändert.
- `python:S9073` in `tests/test_hostruntime_record.py`: Der Import-Bootstrap
  verwendet nun einen expliziten `SPEC`-/Loader-Guard und bewahrt damit
  Fail-fast-Verhalten auch dann, wenn Python-Assertions optimiert werden.

Der gemeldete rekursive-Submodule-Fehler wurde ausschließlich im registrierten
isolierten Parent-Worktree reproduziert, nie im autoritativen Checkout. Am
deklarierten Parent-Gitlink `1260aaae411ecf88cf50dc480b80e2e20ac47901` endeten
sowohl `git submodule sync --recursive` als auch
`git submodule update --init --recursive` mit Exit null und materialisierten
die aufgezeichneten Framework- und MRTS-Revisionen. Der ursprüngliche
Fehlertext lag nicht vor und kein Fehler reproduzierte sich; deshalb ist keine
Änderung an Gitlink, Framework-/MRTS-Quellcode oder Submodule-Update-Pfad
gerechtfertigt.

Die lokale Follow-up-Validierung bestand `git diff --check`, Python-Kompilation
mit externem Cache, die kombinierte Preflight-/Record-Suite (38 Tests), die
Record-Suite unter `python -O` (11 Tests) sowie
`make test-hostruntime-preflight` (27 Tests). Am exakten Source-Follow-up-Head
`04f1fb81549360b22719344dee90ec0196d63f19` waren alle aktuellen Hosted-
PR-Checks terminal und bestanden; SonarQube Cloud meldete Quality Gate `OK`,
null neue/akzeptierte Issues und null Security Hotspots; kein Review oder
Review-Thread war offen. Dieses gepaarte Delivery-Record-Update ändert den
PR-Head, daher ist vor dem autorisierten Merge seine frische Exact-Head-
Validierung erforderlich. Zum Zeitpunkt dieses Dokumentationscommits erfolgte
kein Merge.

## Ausgeführte Befehle

- Fokussierte Parent-Unittest-Suite für Preflight, Resolver, Lifecycle-Record,
  Workflow-Evidence, Compiler-Guides und bilinguale Dokumentation: bestanden,
  77 Tests.
- `make test-hostruntime-preflight`: bestanden, 14 Tests.
- `sh -n` für jedes geänderte Parent-Shellskript: bestanden.
- `make -C connectors/haproxy check-htx-overlay`: bestanden.
- Jeder Connector-Makefile-Wrapper wurde mit dem Framework-PR-Lock ausgeführt;
  der darunterliegende Preflight lieferte für die absichtlich fehlende
  Host-Binary `BLOCKED`/Exit 77 und `runtime_status=NOT_RUN`.
- Ein begrenzter frischer
  `make -C connectors/haproxy runtime-smoke-haproxy-htx`-Lauf mit isolierten
  externen Roots bestand; seine Host-Evidence ist unten beschrieben.

Dies sind beobachtete lokale Ergebnisse, keine Hosted-CI- oder PR-Check-Evidence.

## Security-Auswirkung

Die Framework-Downloadänderungen behalten verpflichtende TLS-Verifikation und
SHA-256-Prüfung, begrenzte Timeouts sowie die Bereinigung leerer, partieller
oder nicht übereinstimmender Artefakte bei. Der Parent führt keine unsichere
Downloadoption ein.

Parent-Artefakte verwenden eine Allowlist-Projektion und laden keine rohen
Payloads, URLs, Credentials oder vollständigen Hostpfade hoch. Ein fokussiertes
Review fand, dass ein bösartiger versionierter Bibliotheksname zuvor die
quotierte erzeugte Resolver-Environment-Datei brechen konnte. Der Resolver
akzeptiert jetzt nur `libmodsecurity.so`, `libmodsecurity.a` oder numerische
gepunktete `libmodsecurity.so.<version>`-Namen; ein Regressionstest beweist,
dass ein Quote-/Metazeichenname blockiert wird, ohne seinen Marker auszuführen.
Die Root- und Connector-Make-Targets hängen außerdem keine rohen
Preflight-Argumente mehr an ein Shell-Rezept an.

## Runtime-Evidence

Der frische aufbewahrte Lauf unter
`/var/tmp/codex/ModSecurity-conector/runs/f-gs-004-parent-20260814/htx-rerun-4`
endete mit Exit null. Seine `runtime-summary.txt` enthält HAProxy `3.2.21`,
`status=PASS`, `runtime_verified=true`, `requests_sent=true`, die erwarteten
Allow/Block-Status `200`/`403` und `processes_stopped=yes`. Er verwendet die
kanonischen No-CRS-Regeln aus Framework-PR #79 schreibgeschützt. Das HTX-
Ergebnis ist echte Host-Evidence, bleibt jedoch gemäß bestehender
Connector-Policy Capability-nicht-promoted.

Die aktuellen Component-Preflights lassen NGINX, HAProxy SPOE/SPOP, Envoy und
Traefik als `BLOCKED`, nicht als `FAIL`, weil ihre erwartete Binary und Quelle
fehlen. Envoy `ext_authz` und Traefik `forwardAuth` behalten nicht anwendbare
Response-Body-/P4-Semantik.

## Bekannte Einschränkungen

- Framework-PR #79 ist als Framework-`master`
  `01952978772995c054ba6a4cba86adc5d0cd1e7d` gemergt. Der Parent-Gitlink
  bleibt absichtlich unverändert; kein Parent-Pointer-Update ist Teil dieser
  Aufgabe.
- Hosted-PR-Evidence am unmittelbar vorherigen exakten Source-Head ersetzt
  nicht die frische Exact-Head-Validierung, die dieses gepaarte Delivery-
  Record-Update erfordert.
- Kein NGINX-, HAProxy-SPOE/SPOP-, Envoy- oder Traefik-Hostprozess wurde
  gestartet: Die erforderlichen Binary-/Quellvoraussetzungen fehlen.

## Verbleibende Risiken

Die autorisierte Parent-Integration bleibt nach diesem gepaarten Delivery-
Record-Update durch frische Exact-Head-PR-Checks, Review-/Thread- und
Protection-Evidence sowie anschließend durch die Resulting-`master`-Workflows
abgesichert. Plattformspezifische Paketlayouts außerhalb des getesteten Linux-
Distributionslayouts benötigen ihre normale CI-Abdeckung. Die Nicht-HTX-
Komponenten bleiben umgebungsblockiert statt validierte Runtime-Passes.

## Nicht ausgeführte Prüfungen mit Begründung

- Vollständige Host-Smokes für NGINX, HAProxy SPOE/SPOP, Envoy und Traefik
  wurden wegen fehlender geprüfter Binaries und Quellen nicht ausgeführt;
  jeder Preflight besitzt einen aufbewahrten `BLOCKED`-Record.
- `actionlint` wurde nicht ausgeführt, weil es lokal nicht installiert ist;
  YAML-Parsing und Workflow-Contract-Tests bestanden.
- Der aktuelle User hat den Parent-Merge autorisiert, aber zum Zeitpunkt dieses
  Record-Commits werden weder Merge noch Resulting-`master`-Checks behauptet.
  Die durch dieses Dokumentationsupdate erforderliche frische Exact-Head-
  PR-Validierung muss zuvor enden. Ein Parent-Gitlink-Update bleibt außerhalb
  des Scopes.

## Finaler Diff- und Review-Status

Der finale begrenzte Parent-Diff-Check, die fokussierte 77-Test-Suite, der
HTX-Overlay-Check, Shell-Syntax-/ShellCheck-Checks, der Compiler-Guide-Check
und der versiegelte Scoped Security-Diff-Review bestanden. Das Sonar-Follow-up
bei `04f1fb81549360b22719344dee90ec0196d63f19` bestand außerdem seine
fokussierten lokalen und Hosted-Exact-Head-Checks. Framework und Parent bleiben
getrennte Git-Grenzen; Framework-PR #79 ist gemergt, während diese Parent-
Änderung absichtlich kein Gitlink-Update staged. Dieses gepaarte Record-Update
benötigt vor dem autorisierten Parent-Merge eine frische Exact-Head-
Validierung. Zum Zeitpunkt dieses Record-Commits wurde kein Pull Request
gemergt.

## Post-Merge-CI-Fixture-Portabilitätskorrektur

PR #287 wurde anschließend als Parent-Master
`29a2a8bcab57e936c5274f8fe64a15c6fee879bd` squash-gemergt. Der manuell
ausgelöste Parent-`Update submodules`-Run `31866612619` erreichte danach den
isolierten Quick-Check: Submodule-Auflösung, Candidate-Git-State-Validierung,
Sandbox-Vorbereitung und Source-/Output-Verifikation bestanden, aber der
Quick-Check scheiterte in
`test_valid_lock_drives_version_and_safe_artifact_metadata`. Damit ist der
zuvor aufgezeichnete Hostruntime-Test-Portabilitätsdefekt bestätigt, nicht
etwa ein Submodule-, Gitlink-, Framework- oder MRTS-Fehler.

Der korrigierte Test ruft nicht länger hostverwaltetes `/bin/true` auf. Er
kopiert den ausgewählten Testinterpreter in ein privates temporäres
`trusted-binaries`-Verzeichnis, übergibt dieses reguläre Executable durch die
vorhandenen Argumente `--binary-root` und `--binary` und schreibt die
Lock-Version aus `sys.version_info` desselben Interpreters. Damit bleiben eine
echte Versionsprobe und ein erfolgreicher `ldd`-Check erhalten, während
runnerspezifische Coreutils-Metadaten entfallen. Produktions-Preflight,
strikter Versionsvergleich, Trusted-Root-Validierung, negative Controls,
Updater-Workflow und Gitlink bleiben unverändert.

Die geänderten Pfade dieses korrigierenden Follow-ups sind
`tests/test_hostruntime_preflight.py` und dieses bestehende englische/deutsche
Change-Record-Paar. Es änderten sich weder Framework- oder MRTS-Quellcode,
Submodule-Revision, Workflow, Runtime-Artefakt, Abhängigkeit noch erzeugter
Report.

Die tatsächliche lokale Validierung mit dem ausgewählten Parent-Virtual-
Environment-Interpreter bestand `python -m unittest -v
tests.test_hostruntime_preflight` (27 Tests) und
`make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python
test-hostruntime-preflight` (27 Tests). Der fokussierte Security-Diff-Review
ergab null reportable Findings: Der kopierte Interpreter wird vom Test-Runner
kontrolliert, existiert nur unter `TemporaryDirectory` und bleibt den
bestehenden Preflight-Controls für Trusted-Root, bereinigte Umgebung, Version
und dynamische Libraries unterworfen. Die bestehenden Controls für
Versionsmismatch, untrusted Roots und gruppenschreibbare Roots bestanden in
derselben fokussierten Suite. `git diff --check` bestand.

Das Ergebnis von `make check-bilingual-docs` im Task-Worktree ist kein
verwendbares lokales Akzeptanzsignal: Das absichtlich nicht initialisierte
gepinnte Framework-Submodul lässt dessen repository-weiten Link-Pass nur
fehlende Framework-Link-Ziele melden. Es wurde deshalb nicht als bestanden
gewertet; keine Framework-Initialisierung oder -Aktualisierung erfolgte.
Dieses aktualisierte englische/deutsche Change-Record-Paar erhielt einen
direkten Paritätsreview; ein Hosted-Exact-Head-Dokumentationscheck bleibt
erforderlich.

Der Draft-Korrektur-PR #290 ist von
`agent/fix-run-31866612619-hostruntime-fixture` gegen `master` geöffnet.
Dieses Update behauptet keine SonarQube-Cloud-Reanalyse, keinen Hosted-
Exact-Head-Check und keinen Resulting-Master-Rerun. Die Aufgabe muss vor einer
späteren Master-Integration den normalen geschützten Parent-Delivery-Pfad
verwenden; eine neue Master-Autorisierung wird hier nicht behauptet.
