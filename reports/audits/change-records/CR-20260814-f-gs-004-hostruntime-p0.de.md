# Change Record: F-GS-004 Hostruntime-P0-Härtung

**Sprache:** [English](CR-20260814-f-gs-004-hostruntime-p0.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260814-f-gs-004-hostruntime-p0 |
| Datum (UTC) | 2026-08-14 |
| Basis-Revision | ea3b48abab7940de49997a371f9117b409c05a2a |
| Delivery-Status | Lokale Implementierung, Validierung und Scoped Security Review abgeschlossen; Erstellung des Parent-Draft-PR steht aus. Framework-Draft-PR #79 ist eine erforderliche Abhängigkeit. |

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
  und HAProxy-Reader-Dokumentation sowie `scripts/generate_compiler_guides.py`.
- Fokussierte Tests: Hostruntime-Preflight, Workflow-Evidence,
  Lifecycle-Record, HAProxy-Resolver und HTX-Harness-Abdeckung.

Kein Parent-Gitlink, Framework-Quellcode, MRTS-Quellcode, Cache, Build-Output,
Secret oder Runtime-Log ist Teil der Parent-Änderung.

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

- Der Framework-Lock stammt aus dem ungemergten Framework-Draft-PR #79. Der
  aktuelle Parent-Gitlink muss unverändert bleiben, bis der Framework-Lifecycle
  durch seinen eigenen autorisierten Merge abgeschlossen ist.
- Keine Hosted-Workflow-, exakte Parent-PR-Head-Check- oder Hosted-Artefakt-
  Evidence wurde lokal beobachtet.
- Kein NGINX-, HAProxy-SPOE/SPOP-, Envoy- oder Traefik-Hostprozess wurde
  gestartet: Die erforderlichen Binary-/Quellvoraussetzungen fehlen.

## Verbleibende Risiken

Der Parent-Draft-PR bleibt von Framework-PR #79 abhängig und benötigt frische
Hosted-Checks für den exakten Head, nachdem beide PRs existieren.
Plattformspezifische Paketlayouts außerhalb des getesteten Linux-
Distributionslayouts benötigen ihre normale CI-Abdeckung. Die Nicht-HTX-
Komponenten bleiben umgebungsblockiert statt validierte Runtime-Passes.

## Nicht ausgeführte Prüfungen mit Begründung

- Vollständige Host-Smokes für NGINX, HAProxy SPOE/SPOP, Envoy und Traefik
  wurden wegen fehlender geprüfter Binaries und Quellen nicht ausgeführt;
  jeder Preflight besitzt einen aufbewahrten `BLOCKED`-Record.
- `actionlint` wurde nicht ausgeführt, weil es lokal nicht installiert ist;
  YAML-Parsing und Workflow-Contract-Tests bestanden.
- Hosted-CI, PR-Checks, Review, Merge und ein Parent-Gitlink-Update werden
  nicht behauptet, weil Delivery noch nicht erfolgt und ein Merge nicht
  autorisiert ist.

## Finaler Diff- und Review-Status

Der finale begrenzte Parent-Diff-Check, die fokussierte 77-Test-Suite, der
HTX-Overlay-Check, Shell-Syntax-/ShellCheck-Checks, der Compiler-Guide-Check
und der versiegelte Scoped Security-Diff-Review bestanden. Getrennte Commits
und der Parent-Draft-PR stehen noch aus. Framework und Parent bleiben getrennte
Git-Grenzen; Framework-Draft-PR #79 muss zuerst mergen, und diese Parent-
Änderung staged absichtlich kein Gitlink-Update. Kein Pull Request wurde
gemergt.
