# Change Record: Parent-Envoy-Runtime-Artefaktbegrenzung und Loopback-TLS

**Sprache:** [English](CR-20260729-sonar-envoy-runtime-artifact-tls-containment.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260729-sonar-envoy-runtime-artifact-tls-containment |
| Datum (UTC) | 2026-07-29 |
| Basis-Revision | `5bf35f7f50f2ff9ed8b17f538d8043b3909b945b` |
| Tracking | Fünfzehn aktuelle SonarQube-Cloud-Kandidaten in `connectors/envoy/harness/envoy_smoke_helper.py`: `pythonsecurity:S8703` ×3, `pythonsecurity:S8707` ×6, `python:S5332` ×1 und fünf Cognitive-Complexity-Zeilen. |
| Grenze | Parent-Envoy-Harness, Konfigurationsmaterializer/-template, Connector-Test, erforderliche leserorientierte Dokumentation und gepaarte Change-Record-Indizes. Keine Framework-, MRTS-, Gitlink-, Workflow-, Sonar-Konfigurations-, Suppression- oder `master`-Änderung. |

## Motivation und Problemstellung

Der Envoy-ext_proc-Smoke-Helper akzeptierte CLI-gesteuerte URLs, Host/Port-
Paare und Evidence-Pfade an Netzwerk- und Dateisystem-Sinks. Sein Runner
stellte den Downstream-Listener über Klartext-HTTP bereit. Lexikalische
Absolute-Pfad-Prüfungen beweisen keine Begrenzung auf private Runtime-Roots,
und ein nur auf Loopback beschränkter HTTP-Endpunkt bietet weiterhin weder
Vertraulichkeit noch Integrität des Transports.

## Akzeptanzkriterien

- Jedes vom Helper erzeugte oder gelesene Runtime-Artefakt ist ein absoluter,
  nicht-symlinkender Nachfahre eines verifizierten privaten Runtime-Roots und
  wird durch descriptor-sichere Read-/Write-Operationen verarbeitet.
- Envoy-Smoke-Client-Endpunkte sind credential-freies HTTPS auf exakt
  `127.0.0.1`, verwenden einen zertifikatverifizierenden Client-Kontext und
  verlangen TLS 1.2 oder neuer.
- Der erzeugte Envoy-Listener nutzt das private Zertifikat und den Key des
  jeweiligen Runs; gewöhnliche Phase-, Probe- und Client-Cancel-Evidence bleibt
  payload-frei.
- Bestehende legitime Loopback-Probes, das Phase-4-Barrier-Verhalten und das
  optionale Client-Cancel-Verhalten funktionieren weiterhin in fokussierten
  temporären TLS-Tests.
- Konfigurationsmaterialisierung, Tests, englische/deutsche Dokumentation und
  die Hosted-Analyse des exakten aktuellen PR-Heads müssen vor einer
  Integration null New-Code-Issues und Duplikatzeilen bewahren.

## Implementierungsentscheidung und Begründung

Der Helper verwendet die Parent-`runtime_path_utils`-Policy für private Roots
wieder und ergänzt No-Follow-Descriptor-Helper für JSON- und JSONL-Artefakte.
Die Pfade `probe`, `client-cancel` und der Phase-4-Client weisen Nicht-
Loopback-, Klartext-, Credential-haltige, fragmentierte und ungültige
Port-Ziele vor einem Netzwerk-Sink ab. Der Runner erzeugt ein eintägiges,
self-signed SAN-Zertifikat ausschließlich unter seinem verifizierten privaten
Root, übergibt es an Envoys Downstream-TLS-Transport-Socket und verwendet das
passende Zertifikat als Python-Client-Trust-Anchor.

Der Standardbibliotheks-Python-Upstream bleibt eine interne Loopback-Fixture
hinter Envoy. Diese Änderung behauptet nicht, dass er eine Produktions-
Upstream-TLS-Topologie modelliert. Die optionale Full-Lifecycle-Evidence-
Übergabe bleibt nur über einen separat verifizierten privaten Output-Root
außerhalb des Checkouts unterstützt; sie akzeptiert niemals einen beliebigen
Output-Pfad.

## Geänderte Dateien

- `connectors/envoy/harness/envoy_smoke_helper.py` — Root-begrenzte
  Artefakt-Helper, verifizierte Loopback-TLS-Client-Pfade und kleinere
  Command-/Evidence-Funktionen.
- `connectors/envoy/harness/run_envoy_ext_proc_runtime.sh` — private
  Zertifikatserzeugung, TLS-Listener-Wiring und Root-Argumente für jeden
  Artefakt-tragenden Helper-Aufruf.
- `connectors/envoy/config/envoy-ext-proc-streaming.yaml.in` und
  `connectors/envoy/config/prepare_envoy_ext_proc_config.sh` — erforderliche
  Zertifikat-/Key-Platzhalter und Downstream-TLS-Transport-Socket.
- `connectors/envoy/Makefile` und `connectors/envoy/build/test_ext_proc.sh` —
  temporäres Zertifikat-/Key-Konfigurations-Wiring und Assertions für die
  erzeugte Konfiguration.
- `tests/test_envoy_transport_hardening_contract.py` — echte temporäre TLS-
  Legitimate-Controls sowie Negativ-Controls für Klartext, Remote-Host,
  Credentials, Outside-Root und Symlink-Nachfahren.
- `scripts/generate_compiler_guides.py`, erzeugte englische/deutsche Envoy-
  Compiler-Guides, `examples/envoy/README.md` und
  `examples/envoy/README.de.md` — gültige private TLS-
  Materialisierungsbeispiele.
- Dieses englisch/deutsche Change-Record-Paar und seine gepaarten Indizes.

## Ausgeführte Befehle

| Ausgeführte Kontrolle | Beobachtetes Ergebnis |
| --- | --- |
| `python3 -m unittest tests.test_envoy_transport_hardening_contract` | bestanden; zehn fokussierte Tests prüften echte temporäre TLS-Probe-, Client-Cancel- und Phase-4-Pfade sowie negative Pfad- und Endpunkt-Controls. |
| `python3 -m py_compile connectors/envoy/harness/envoy_smoke_helper.py tests/test_envoy_transport_hardening_contract.py` | bestanden. |
| `sh -n connectors/envoy/harness/run_envoy_ext_proc_runtime.sh connectors/envoy/config/prepare_envoy_ext_proc_config.sh` | bestanden. |
| `shellcheck -S error` auf den geänderten Envoy-Shell-Skripten | bestanden; vorhandene Advisory-Diagnosen wurden nicht zu einem Error-Level-Fehler gemacht. |
| `make -C connectors/envoy … prepare-envoy-ext-proc-config` mit temporärem `BUILD_ROOT` | bestanden; das Ergebnis enthält den TLS-Transport-Socket und die erwarteten Zertifikat-/Key-Pfade. |
| `make -C connectors/envoy … test-envoy-ext-proc` mit temporären Go-Caches | Go-Pakettests bestanden; der anschließende Common/libmodsecurity-Schritt ist durch die fehlende Framework-Regeldatei blockiert. |
| `make check-envoy-common-adoption` | bestanden. |
| `git diff --check` | bestanden. |

## Security-Auswirkung

Diese Änderung liegt an einer Network-Client-, Local-Listener-,
Filesystem-Artefakt- und Runtime-Evidence-Grenze. Sie entfernt den Klartext-
Client-zu-Envoy-Transport, weist Remote-/Credential-haltige Endpunkte ab und
begrenzt dynamische Artefakte auf private No-Symlink-Roots. TLS-Verifikation
ist explizit (`ssl.PROTOCOL_TLS_CLIENT`, Zertifikatsverifikation, privater
Trust-Anchor und mindestens TLS 1.2). Keine Validierungs-, Logging-, Evidence-,
Quality-Gate- oder CI-Kontrolle wird gelockert.

## Runtime-Evidence

Fokussierte Python-Controls starteten echte lokale TLS-Server mit einem
temporären SAN-Zertifikat und beobachteten die vorgesehenen Client-Pfade. Die
Konfigurationsmaterialisierung erzeugte Envoys Downstream-TLS-Transport-Socket.
Diese Controls sind keine vollständige Envoy-plus-ext_proc-plus-libmodsecurity-
Runtime; es wird keine Produktions-Topologie oder Full-Lifecycle-Promotion
behauptet.

## Bekannte Einschränkungen

- In dieser Umgebung ist kein `envoy`-Binary installiert, daher können keine
  Envoy-Konfigurationsvalidierung und kein vollständiger ext_proc-Runtime-Smoke
  lokal laufen.
- Die vom vorhandenen ext_proc-Test benötigte Framework-Submodule-Regeldatei
  fehlt; sie wird nicht durch eine lokale Fixture ersetzt.
- Ein vollständiger Codex-Security-Scan ist in dieser Runtime nicht verfügbar,
  weil sein erforderlicher Delegated-Worker-Modus deaktiviert ist. Fokussierte
  Source-to-Sink- sowie Negative-/Legitimate-Controls sind die stärkste
  verfügbare Evidence.

## Verbleibende Risiken

- Vor der Integration muss der exakte aktuelle PR-Head unabhängig bestätigen,
  dass die fünfzehn ausgewählten SonarQube-Cloud-Kandidaten ohne neue Issues
  oder Duplikate entfernt sind; der gehostete PR-Status und nicht dieser
  historische Record ist die Evidence für dieses Gate.
- Zukünftige Envoy-Konfigurationskonsumenten müssen weiterhin Zertifikat- und
  Private-Key-Pfade übergeben; der Materializer weist ihr Fehlen jetzt ab.

## Nicht ausgeführte Prüfungen mit Begründung

Keine vollständige Envoy-/ext_proc-/libmodsecurity-Runtime, Envoy-Binary-
Validierung oder komplette Connector-Matrix lief, weil das benötigte Envoy-
Binary und die Framework-Regel-Fixture lokal nicht verfügbar sind. Hosted
Actions, SonarQube-Cloud-Analyse, Review-/Thread-Status und der Merge-Vorgang
sind Delivery-Evidence, die unmittelbar vor einer Integration am exakten
aktuellen PR-Head gelesen wird. Dieser Record behauptet kein Ergebnis für
einen künftigen Head und dokumentiert keinen `master`-Merge.

## Hosted-Feedback-Follow-up

Der initiale exakte PR-Head `b4401deec9bce94a806dd56f1cc0215431881f93` erhielt
ein `OK`-SonarQube-Cloud-Quality-Gate mit 0,0 % New-Code-Duplizierung, aber
fünf task-eigene neue Code Smells: zwei duplizierte Literale und drei
Exception-Testformen. Sein push-ausgelöster `scaffold-lint`-Lauf schlug zudem
fehl, weil der erzeugte Envoy-Compiler-Guide die neu verwendeten Platzhalter
`TLS_CERTIFICATE` und `TLS_PRIVATE_KEY` nicht aufführte; die OpenSSL-Tokens
`CN` und `subjectAltName` sind feste Optionsnamen, keine Platzhalter. Der
fokussierte Follow-up extrahiert die Literale, berechnet Exception-Test-
Argumente vorab, dokumentiert die zwei Variablen in beiden erzeugten Guides
und lässt den Placeholder-Test feste OpenSSL-Optionsnamen unterscheiden. Die
52 fokussierten Envoy-Transport-, Compiler-Guide- und Bilingual-Tests bestehen
lokal. Follow-up-Commit `1b6cc0372f6d5b9ba175fc9e22b61e3ba84bd0c5`
absolvierte seinen Exact-Head-Hosted-Zyklus erfolgreich; kein Fehler wurde
erlassen oder als akzeptiert markiert.

## Finaler Diff- und Review-Status

Der Kandidat ist auf den Parent-Envoy-Connector, seine direkten Tests und die
erforderliche bilinguale Traceability/Dokumentation begrenzt. Dieser Record
erfasst den finalen versionierten Source-/Dokumentationsumfang, lokale
Kontrollen und Runtime-Einschränkungen. Delivery-Evidence wird absichtlich
unmittelbar vor jeder Integration vom exakten aktuellen PR-Head bezogen; sie
wird nicht für spätere Dokumentations- oder Lifecycle-Commits selbst behauptet.
Dieser Change Record dokumentiert keinen `master`-Merge.
