# PR #421: Abschlussnachweise für Sonar und CI

**Sprache:** [English](sonarqube-pr421-closeout.md) | Deutsch

Dies dokumentiert die gezielte Fortsetzung von [Draft-PR #421](https://github.com/Easton97-Jens/ModSecurity-conector/pull/421). Der Scan der Source-Änderung an `59bc0842cea90d4052c0d005218fae3aca14c2b2` ist unten getrennt vom historischen `4ec7581056889f8c70f44c6725f6bfa65a7fc45b` zugeordnet. Der finale reine Dokumentations-Head benötigt weiterhin eigenes CI-/Server-Rücklesen im PR. Weder Merge, Änderung an `master`, Issue-Transition, Gate-Absenkung noch breite Ausschlüsse werden behauptet. Der [Change Record](../reports/audits/change-records/CR-20261025-sonar-setup-remediation.de.md) erhält die Entwicklungshistorie.

## Entscheidungsvorlagen für die Hauptprojekt-Security

Die vollständige Abfrage an `59bc0842` enthält weiterhin die drei ursprünglichen offenen Schwachstellen `pythonsecurity:S2083` für PR 421; fünf neue Helper-Findings werden unten separat bewertet. Die drei vollständigen Datenflüsse entsprechen den früheren Records des exakten Heads. Jeder Fluss beginnt mit JSON-Dateiinhalt in `run-native-case-comparison.py:129`, wählt `report["request"]` bei 668, durchläuft den Return bei 726–732, `run_requested_cases:1237`, main 1265–1268, `write_summary:1100–1118`, `reader.file_proof:1122`, `EvidenceInputs.file_proof:93–94` und `_descriptor:41` vor den folgenden Sinks.

Die Feldunterscheidung ist entscheidend: `request` sind Daten, das konsumierte `run_dir` wird hingegen bei 658 aus dem Aufrufkontext und bei 433–436 aus privaten Runtime-Verzeichnissen gebildet. Es wurde keine Zuweisung des kontaminierten Requests an `run_dir` gefunden. `latest_case_runs:866` ersetzt gespeichertes `run_dir` durch das tatsächlich geladene Verzeichnis. Der Aufrufer erlaubt unabhängig davon `native-case-runs` bei 1109 und legt das Blatt `native-case-run.json` bei 1118 fest.

| Issue | Vollständiger Fluss | Konkrete Kontrollen und Angriffs-/Kontrollpaar | Vorgeschlagene Entscheidung |
| --- | --- | --- | --- |
| `AaF0ynIMY4cSrRUGTduD` | 1 Fluss, 44 Stellen; `evidence_inputs.py:47` | `_absolute` lehnt relative Pfade, `..` und NUL ab; `path()` prüft aufrufereigene Wurzeln/Dateien. `path.anchor` ist nur POSIX `/` oder `//`, geöffnet mit `O_NOFOLLOW\|O_DIRECTORY`. Externes gespeichertes `run_dir` und Root-Freigabe-Angriffe werden abgelehnt; legitime begrenzte Metadaten bleiben lesbar. Am Anker werden keine geschützten Dateibytes gelesen. | False-Positive-Kandidat, hohe Sicherheit für den geprüften Linux-/POSIX-Vertrag; Status bleibt OPEN. |
| `AaF0ynIMY4cSrRUGTduC` | 1 Fluss, 47 Stellen; `evidence_inputs.py:51` | Jede Zwischenkomponente ist ein einzelner Name relativ zu einem gehaltenen Verzeichnisdeskriptor, mit `O_NOFOLLOW\|O_DIRECTORY`; fehlende Plattformflags führen zur Ablehnung. Zwischenlinks, Geschwisterpräfix und Traversal scheitern; verschachtelte reguläre Records funktionieren. | False-Positive-Kandidat, hohe Sicherheit; Status bleibt OPEN. |
| `AaF0ynIMY4cSrRUGTduB` | 1 Fluss, 44 Stellen; `evidence_inputs.py:54` | Festes Blatt mit `O_NOFOLLOW\|O_NONBLOCK`; `fstat` verlangt eine reguläre Datei. Hashing liest denselben Deskriptor ohne erneutes Öffnen. Blattlinks und Austausch vor dem Öffnen scheitern; reguläre Eingabe liefert den erwarteten Hash. | False-Positive-Kandidat, hohe Sicherheit; Status bleibt OPEN. |

Die folgenden neun benannten bestehenden Tests wurden vom unabhängigen Security-Reviewer tatsächlich ausgeführt: **9 bestanden, 0,350 s, Exit 0**. Jeder eingerückten Methode ist ihr vorangehender Klassenselektor voranzustellen:

```text
tests.test_evidence_input_security.EvidenceInputSecurityTests.
  test_read_and_hash_use_a_regular_file_in_an_explicit_root
  test_rejects_sibling_prefix_traversal_and_final_or_intermediate_links
  test_replacement_before_final_open_cannot_follow_a_link
  test_empty_or_filesystem_root_allowlists_cannot_grant_arbitrary_access
  test_jsonl_parser_keeps_valid_objects_and_ignores_malformed_rows
tests.test_sonar_evidence_boundaries.SonarEvidenceBoundaryTests.
  test_latest_native_record_retains_its_actual_loaded_directory
  test_supplied_native_records_cannot_authorize_external_metadata_inputs
  test_native_metadata_uses_fixture_identity_and_confined_record_bytes
  test_latest_native_record_does_not_follow_a_link
```

Die repositoryrelative Befehlsform lautet `rtk bypass env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 TMPDIR=/var/tmp/codex/ModSecurity-conector .venv/bin/python -m unittest -v` mit diesen neun vollständigen Selektoren. Der ausgeführte Befehl wählte die Parent-Umgebung über ihren absoluten Pfad; deren lokaler Ort ist keine Voraussetzung für Leser. Alle Byte-/Stat-/JSON-/Nachweis-Reader verwenden `_descriptor`; `path()` allein erteilt nur lexikalische Freigabe. Diese Tests beweisen keinen Schutz gegen privilegierten Mount-Austausch, Hardlinks oder Byteänderungen durch einen berechtigten Schreiber. POSIX-Backslashes, kodierte Slashes und Unicode-Verwechslungen bleiben literale Namen; URL-Dekodierung findet nicht statt.

Vorlage für einen autorisierten Issue-Administrator, pro Tabellenzeile getrennt: Issue-ID und exakten Fluss erhalten, zugehörige Kontrollen und benannte Angriffs-/Kontrollergebnisse anhängen, aktuelle Source-Revision prüfen und **False Positive** für den geprüften Fluss vorschlagen. Es wurden keine Issue-Kommentare oder Statusänderungen veröffentlicht. Technische Gegenbelege erteilen keine Transition-Berechtigung; [Sonar-Issue-Bearbeitung](https://docs.sonarsource.com/sonarqube-cloud/managing-your-projects/issues/editing) benötigt außerdem die entsprechende Berechtigung und verändert Gate-Metriken.

## Unabhängige Advisory-Entscheidungen

Die Tabelle betrifft die **vollständigen historischen 23-Issue-Snapshots je Advisory bei `4ec7581056889f8c70f44c6725f6bfa65a7fc45b`**, unabhängig am Source geprüft. Alle 23 Paare haben gleiche Regel, Pfad, Zeile, Meldung und vollständige normalisierte Flüsse; nur das Projektpräfix unterscheidet sich. Ihre Bewertung wurde nicht von den drei Hauptprojekt-Issues abgeleitet. Vorgeschlagen sind **22 Paare `not_actionable`, ein Paar `needs_review`**, ohne Server-Transitions. Dies war ein Source-Review; der Advisory-Reviewer führte keine Tests aus und belegt keine dynamische Abdeckung pro Paar.

| C++20 issue | C++23 issue | Sink | Unabhängiger Gegenbeleg / Entscheidung |
| --- | --- | --- | --- |
| `AaF0yzxvaVChWkKVlx8R` | `AaF0y14uF0XFUMkHWcpz` | `evidence_inputs.py:47` | Absolute Root-Freigabe; Verzeichnisanker mit No-follow. |
| `AaF0yzxvaVChWkKVlx8Q` | `AaF0y14uF0XFUMkHWcp0` | `evidence_inputs.py:51` | Einzelkomponenten relativ zu gehaltenen No-follow-Verzeichnisdeskriptoren. |
| `AaF0yzxvaVChWkKVlx8S` | `AaF0y14uF0XFUMkHWcpy` | `evidence_inputs.py:54` | Festes Blatt, No-follow/nonblocking, reguläre fstat-Datei und derselbe Nachweisdeskriptor. |
| `AaF0ZnLmLhxv2LRQWeOE` | `AaF0Zlbb7GRUxAPzGll5` | `framework_revision_pins.py:106` | Kleingeschriebener ASCII-40-Hex-SHA vor festen Git-Argumenten; keine Shell. |
| `AaF0ZnLpLhxv2LRQWeOF` | `AaF0Zlbd7GRUxAPzGll6` | `prepare-reviewed-framework-handoff.py:292` | Explizite Operatorausgabe; exklusive Erstellung, wendet den Patch niemals an. |
| `AaF0ZnM8Lhxv2LRQWeOX` | `AaF0Zlcx7GRUxAPzGlmM` | `hostruntime_preflight.py:169` | Freigegebenes Runtime-/Source-Lock vor deskriptorbasiertem Lesen; Ablehnung schlägt geschlossen fehl. |
| `AaF0ZnMyLhxv2LRQWeOU` | `AaF0Zlco7GRUxAPzGlmJ` | `write-transport-lifecycle-artifacts.py:487` | Konfigurations-Hash-Eingaben auf Runtime/Source oder aufrufseitige kanonische Framework-Wurzel beschränkt. |
| `AaF0ZnMuLhxv2LRQWeOT` | `AaF0Zlcj7GRUxAPzGlmI` | `resolve-full-lifecycle-profile.py:243` | Eingabe durchläuft runtime_or_source_artifact_path vor dem Laden. |
| `AaF0ZnM0Lhxv2LRQWeOV` | `AaF0Zlcq7GRUxAPzGlmK` | `run-full-matrix-job.py:139` | Kanonischer Runtime-Kontext, validierte Run-ID, feste Subprozessargumente. |
| `AaF0ZnMrLhxv2LRQWeOS` | `AaF0Zlch7GRUxAPzGlmH` | `run-full-matrix-resume.py:88` | Kanonische Wurzeln, Runtime-Eigentum und Run-ID vor festem Vollständigkeitsbefehl. |
| `AaF0ZnMrLhxv2LRQWeOR` | `AaF0Zlch7GRUxAPzGlmG` | `run-full-matrix-resume.py:165` | Erlaubte Connector-/CRS-/MRTS-Werte und begrenztes dezimales Timeout; shell=False. |
| `AaF0ZnMCLhxv2LRQWeOK` | `AaF0Zlb57GRUxAPzGll_` | `run-verified-case.py:85` | Gespeichertes JSON ist Nutzlast; erzeugtes case-run.json-Ziel unmittelbar vor dem Schreiben geprüft. |
| `AaF0ZnMCLhxv2LRQWeOL` | `AaF0Zlb57GRUxAPzGlmA` | `run-verified-case.py:85` | CLI-Tokens, eigene Runtime-Wurzel und erzeugtes Zeitstempelverzeichnis begrenzen das Ziel. |
| `AaF0ZnMPLhxv2LRQWeOQ` | `AaF0ZlcF7GRUxAPzGlmF` | `run-verified-report-run.py:1838` | needs_review: Lesen von current-run-id vor Runtime-Eigentumsprüfung; Blatt-Symlink-/FIFO-Lesen war ungeschützt. |
| `AaF0ZnL-Lhxv2LRQWeOJ` | `AaF0Zlb07GRUxAPzGll-` | `write-engine-lifecycle-artifacts.py:59` | Freigegebene Framework-/Rules- oder Runtime-/Source-Eingabe, kein Alias, reguläres No-follow-Hashing. |
| `AaF0yz5SaVChWkKVlx_W` | `AaF0y2C0F0XFUMkHWcs4` | `bounded_cstring_length:52` | NUL-terminiertes Literal crs-setup.conf erreicht sequenzielles memchr über join_path. |
| `AaF0yz5SaVChWkKVlx_X` | `AaF0y2C0F0XFUMkHWcs5` | `bounded_cstring_length:52` | Gleiche unabhängige Datenflussprüfung für Literal crs-setup.conf.example. |
| `AaF0yz5SaVChWkKVlx_Z` | `AaF0y2C0F0XFUMkHWcs7` | `bounded_cstring_length:52` | Gleiche unabhängige Datenflussprüfung für Literal rules. |
| `AaF0ZnPCLhxv2LRQWeOv` | `AaF0Zlex7GRUxAPzGlmk` | `patched_event_validation.py:17` | Explizite --events-Operatoreingabe; Harness liefert festes SMOKE_DIR/phase4-barrier-events.jsonl. |
| `AaF0ZnM4Lhxv2LRQWeOW` | `AaF0Zlct7GRUxAPzGlmL` | `HTTP fixture:212` | Backend bindet Literal 127.0.0.1; keine Option für breiteres Binding. |
| `AaF0ZnPdLhxv2LRQWeOw` | `AaF0ZlfL7GRUxAPzGlml` | `HTX helper:414` | Validierter Port und Loopback-Backend; Frontend-TLS separat konfiguriert. |
| `AaF0ZnMPLhxv2LRQWeON` | `AaF0ZlcF7GRUxAPzGlmB` | `run-verified-report-run.py:1743` | Gespeichertes JSON ist Manifest-Nutzlast; kanonisches Registry-report_path wählt Ausgabe. |
| `AaF0yz5SaVChWkKVlx_Y` | `AaF0y2C0F0XFUMkHWcs6` | `bounded_cstring_length:52` | POSIX-readdir-d_name-Terminator; Suffixprüfung, kein weiteres readdir vor Nutzung. |

Das Marker-Paar zeigt einen unvollständigen früheren Gegenbeleg: Die kanonische Bildung von `current-run-id` belegte weder Blatt-Sicherheit noch die Validierungsreihenfolge. Harmlose Regressionstests reproduzierten ein Symlink-Lesen und externes Überschreiben über die öffentliche Vorbereitung; die legitime reguläre Marker-Kontrolle bestand. Die Source-Korrektur prüft nun das Verzeichnisvertrauen vor dem Lesen, hält einen No-follow-/Nonblocking-Eltern-/Blattdeskriptor, verlangt eine eigene reguläre Datei ohne Gruppen-/Welt-Schreibrecht mit genau einem Hardlink, begrenzt Lesen auf 4.096 Bytes, validiert die ID vor Umgebungsänderung und schreibt atomar als 0600. Eigene bisherige 0644-Marker, 0755-Verzeichnisse, umgebender Whitespace, fehlende Marker, Append-Phasen und explizite ID-Priorität bleiben unterstützt. Sechzehn Evidence-Grenztests und acht betroffene Runtime-Security-/ID-/Atomic-Write-Tests bestanden; ein unabhängiger Reviewer führte die vorherigen sieben Marker-Fälle erfolgreich aus und fand darin keinen konkreten verbleibenden Bypass. Eine abschließende Root-Prüfung reproduzierte danach mit dem achten Marker-Test, dass ein kurzes os.read einen gültigen Präfix vor nachfolgenden ungültigen Bytes akzeptierte. Eine begrenzte Leseschleife bis EOF oder maximal 4.097 Bytes behebt dies; der neue Test schlug vorher fehl und alle 16 Grenztests bestanden danach. Dieser achte Fall war nicht Teil des vorherigen unabhängigen Sieben-Fall-Reviews. Das ist lokale Grenzverifikation, kein finaler Sonar-Abschluss, keine konkurrierende Race-Ausführung und kein Nachweis entfernter Ausnutzbarkeit. Fester Blattname, spätere strikte Run-ID-Prüfung, explizite `VERIFIED_RUN_ID`-Priorität und spätere Root-Prüfungen sind relevante Gegenbelege, deckten den früheren Zugriff aber nicht ab.

Vom Operator gewählte Ausgaben/Framework-Wurzeln erlauben einem künftigen privilegierten Wrapper keine beliebigen Pfade. Loopback-Binding isoliert nicht gegen andere lokale Principals und qualifiziert kein produktives HTTP. Die vier `memchr`-Fälle beruhen auf den tatsächlichen NUL-terminierten Literalen/`dirent`-Namen und sequenzieller Ersttreffer-Semantik, nicht auf dem Qualitätswert: [C N1570 §7.24.5.1 ¶2](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [POSIX dirent](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/dirent.h.html).

Ein späterer Live-Projekt-Snapshot gehört zur fremden Revision `209ab41a16cc34c88e3dc23d312eada0a38a8169`: C++20-Analyse `bd46227f-a29a-4e0b-8a4c-4f9c70499854`, C++23 `93ef6dc3-f223-42a4-a0cf-38c31cdf851d`. Die Issue-Antwort meldet insgesamt 110, enthält aber nur die ersten 100. Dieser unvollständige fremde Snapshot belegt weder aktuelle Anzahl, Einordnung noch Abschluss von PR 421.

## Architektur: geprüfte Änderung, Anwendung blockiert

Die frische Serverabfrage von Modell `cb04d3a3-7c8f-447c-99f0-ca49c97f054f` für Projekt-UUID `608d0a7b-481a-4f7e-acbf-ae8eb07c3be2` wurde mit [dem exakten Vorschlag](../config/analysis/sonar-python-architecture.patch.json) verglichen. Von 46 Top-Level-Gruppen werden 44 ungültige Slash-Labels behandelt: 14 ausgeschlossene Framework-/MRTS-Gruppen entfallen, 30 Parent-Labels werden von `/` nach `_` umbenannt. Parent-Muster, vier verschachtelte Gruppen, Metadaten und `constraints: []` bleiben erhalten; für die verbleibende Parent-Architektur werden keine Regeln erfunden oder entfernt.

Die kanonische CLI `1.10.1` bietet `--data` und `--verbose`, aber keine Header-/Content-Type-Option. Ein frischer geprüfter PATCH über `rtk bypass /usr/local/bin/sonar-with-env` lieferte erneut **HTTP 415 Unsupported Media Type**. Vorher-/Nachher-Abfragen sind identisch. Es war keine Sonar-MCP-Funktion verfügbar. Dies ist eine Medientypgrenze des Clients, kein Nachweis fehlender Server-Adminberechtigung. Die Perspektive wird weiterhin ignoriert; erfolgreiche Modellanwendung und bestätigende neue Analyse sind **extern blockiert**.

Übergabe für einen unterstützten Zugang unter Erhalt der Authentifizierungsregeln:

1. Authentifiziertes `GET /api/v2/architecture/models?projectId=608d0a7b-481a-4f7e-acbf-ae8eb07c3be2` über den kanonischen Wrapper sichern; Modell-ID und vollständiges aktuelles Modell vor Änderung mit der geprüften Baseline vergleichen.
2. Einen autorisierten unterstützten Client verwenden, der `PATCH /api/v2/architecture/models/cb04d3a3-7c8f-447c-99f0-ca49c97f054f` mit **`Content-Type: application/merge-patch+json`** und dem exakten Vorschlag als Body senden kann. Die gezeigten Pfade sind kanonische CLI-Pfade; das dokumentierte SonarCloud-API-Host-Routing des Clients erhalten. Dessen Authentifizierung mit dem vorgeschriebenen Wrapper autorisieren/integrieren, statt Tokens auszulesen oder den Wrapper zu umgehen.
3. Über den freigegebenen Zugang zurücklesen und exakt 14 Entfernungen/30 Umbenennungen sowie erhaltene Muster, verschachtelte Gruppen und Constraints vergleichen. Bei Zustandsdrift zuerst einen neuen Diff prüfen.
4. Eine neue Analyse des sauberen exakten SHAs ausführen und terminalen Servertask, Analyse-ID und Log sichern, das die Perspektivanwendung ohne die 44 ungültigen Labels belegt.

Keine ungeprüfte UI-Import-/Editorfähigkeit wird vorgeschrieben. Das veraltete `sonar.architecture.configpath` ist kein Ausweg: siehe [Web API](https://docs.sonarsource.com/sonarqube-cloud/appendices/web-api) und [Abkündigungen](https://docs.sonarsource.com/sonarqube-cloud/deprecations-and-removals).

## Nativer Kontext und Taintgrenzen

Am historischen `4ec75810` bleiben alle **136 nativen Übersetzungseinheiten** im Scope: Qualität **91,28/100**, Parsingfehler **193/2.260 Funktionen**, ungelöste Projekt-Includes **46/1.132**. Das verbessert die Baseline 77,52/414/115, ist aber kein Abschlusskriterium. Echter gepinnter Host-Kontext betrifft NGINX `1.31.6`, HAProxy `3.2.25` und gepatchtes lighttpd `1.4.85`. NGINX benötigt echte konfigurierte `objs/ngx_auto_config.h`/`ngx_auto_headers.h` und seine tatsächlichen Include-Pfade; HAProxys Linux-/OpenSSL-Featurekontext ist zielspezifisch; lighttpd braucht zusammenpassende gepatchte Sources und generierte Konfiguration.

Die bestehende unvollständige Compilation Database enthält NGINXs 33 Sources und einen einzelnen C++-Evaluator-Kontext, nicht alle Parent-Units/Varianten, und filtert kopierte HTX-Sources ohne vollständiges Provenienz-Mapping. Ihr Einsatz statt AutoConfig würde Abdeckung verlieren. Der source-gepinnte native Kontext-Helper liest bestehende Verträge als Daten, prüft Archiv-Prüfsummen und protokolliert Generated-Header-/Include-Provenienz. Sechs gezielte Helper-Tests bestanden. Ein echter Entwicklungsversuch konfigurierte NGINX erfolgreich und scheiterte dann, weil der neue lighttpd-Patchaufruf mit --fuzz=0 vom bestehenden nativen apply_core_patch.sh-Pfad abwich. Der zweite Versuch bestand echte NGINX-Konfiguration sowie den unveränderten kanonischen lighttpd-Patchweg einschließlich Patchstamp/ABI-Prüfung (dessen tatsächliche fuzz2/fuzz1-Anwendung steht im Log), endete aber vor lighttpd-Konfiguration: Das genehmigte Archiv enthält kein configure. Der dritte echte vollständige Header-Vorbereitungslauf bestand mit Exit 0: unverändertes Upstream-autogen mit vorhandenen Werkzeugen und Bash für den ERR-Trap, echte gepatchte lighttpd-Konfiguration sowie erzeugte Header/Config-Hashes. Das Manifest belegt Revision `4ec7581056889f8c70f44c6725f6bfa65a7fc45b` mit `uncommitted_changes: true`, elf echte Include-Verzeichnisse, Archiv-/Patch-/Configure-Provenienz und Generated-File-Hashes. Das ist Entwicklungsnachweis, keine neue Sonar-Zählung. Kein komponenteneigenes Skript wurde geändert. Der Workflow misst den Helper unter Python-Coverage vor dem Finalizer; die ausgewählte Suite enthält nun 75 Methoden (61 bisherige, acht Marker-, sechs Header-Tests). Die frische instrumentierte lokale Auswahl bestand alle 75 Tests in 7,256 s. Die Entwicklungs-Coverage des neuen Helpers beträgt 82,48 % für Linien und Branches; das ist kein Sonar-Gatewert. Die saubere Head-CI bleibt erforderlich. Erfundenen Headern, geratenen globalen Defines oder Compilerbefehlen fehlt die Grundlage.

Die Implementierung liegt in [prepare-sonar-native-context.py](../ci/checks/analysis/prepare-sonar-native-context.py), ihre sechs gezielten Regressionen in [test_sonar_native_context.py](../tests/test_sonar_native_context.py). Der erfolgreiche Lauf verwendet frische externe Verzeichnisse; lokale Entwicklungsartefakte werden nicht als saubere CI-Reports wiederverwendet.

[Unterstützte CFamily-Anpassung](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/c-family/customizing-the-analysis) erlaubt echte Include-Properties. **C/C++-Taint wird in AutoConfig nicht unterstützt**, und eine Analyse über Übersetzungseinheiten darf unabhängig ausführbare Connector-Ziele und inkompatible Varianten nicht stillschweigend als ein gelinktes Programm behandeln. Vollständiger variantenerhaltender Kompilierkontext und expliziter C/C++-Taintnachweis bleiben entsprechend **weiterhin offen** / **begründete Analyzergrenze**.

## Python-Analyzergrenzen und Shell

Beide vollständigen Advisory-Scans melden während Python-Security-Analyse exakt:

```text
Too high simulation costs for sink in ci/lib/runtime_path_utils.py:69. This sink will not be analyzed any further.
'21' appears to be a predecessor of '20' but this has already been handled.
'15' appears to be a predecessor of '14' but this has already been handled.
```

Dieselben drei Meldungen gab es bereits für Baseline `9f44647593bac7947113558c6ad183ab118e80af` in [Lauf 40224506735](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40224506735), Hauptjob `121262911582`, C++20 `121262911602`, C++23 `121262911515`. Sie treten erneut in den vollständigen Advisories des exakten Heads auf, Jobs `121288719031`/`121288718833` aus [Lauf 40233061104](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40233061104). `runtime_path_utils.py` ist zwischen diesen Revisionen unverändert. Dies ist eine nachgewiesene bestehende Grenze, keine belegte PR-Regression.

Der Sink ist `absolute.resolve(strict=False) != absolute` in `_contains_symbolic_link`, erreichbar über Runtime-Pfad-/Eigentumsvalidierung und Aufrufer wie `prepare-verified-runtime-paths.py` und Compilation-Capture. Vollständige Advisories behalten 5.253 UCFGs/166 Einstiegspunkte aus insgesamt 15.724 und wenden 32 Taintregeln an; die Baseline behielt 5.227/169 aus 15.660. Das Fehlen dieser Meldungen im Haupt-PR betrifft nur eine gecachte Analyse von 16 geänderten/neuen Dateien, 12 Einstiegspunkten und 1.187 behaltenen UCFGs. Es belegt keine Reparatur. Die Kostengrenze überspringt weitere Analyse dieses Sinks, nicht die gesamte Datei/Sprache oder alle 32 Regeln; genaue ausgelassene Pfade und Regel sind nicht quantifiziert. Predecessor-Nummern lassen sich aus diesen INFO-/WARN-Meldungen allein nicht auf Source abbilden.

SonarSource beschreibt eine fest implementierte Grenze gegen exponentielle Verzweigungsanalyse ohne konfigurierbaren Abschalter: [Erklärung der Kostengrenze](https://community.sonarsource.com/t/how-to-avoid-high-simulation-costs-for-sink-in-error/107841/3). Eine [verwandte Predecessor-Diskussion](https://community.sonarsource.com/t/warnings-during-taint-analysis-for-java/141163) verlangt ausführliche Diagnose; sie betrifft Java und ist keine belegte Python-Abhilfe. Keine Heap-/Timeoutänderung ist als Reparatur belegt. Kontrollierte geheimnissichere Debug-Aufzeichnung wäre ein separater Diagnoseschritt und wurde nicht aktiviert. Dies sind **begründete Analyzergrenze** mit verbleibender Taint-Abdeckungslücke.

Fünf von sechs ursprünglichen Shell-Parserfällen fehlen am zugeordneten Head. `ci/runtime/lifecycle/run-full-matrix-parallel.sh` erhält gültiges `exec 8<>` mit bidirektionaler FIFO-Semantik; die verbleibende Parserwarnung ist eine **begründete Analyzergrenze**. Weder Dateiausschluss noch semantisch andere Umleitung wird angewendet.

## Runtime- und Coverage-Rücklesen

[Runtime-Lauf 40233061042](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40233061042) endete für alle fünf Connector-Jobs und den Aggregate-Job mit **SUCCESS**. Apache-Job `121290821692` bestand das tatsächliche `RUN_ONE_CASE=1 make verified-apache-case CASE=crs_sqli_anomaly_block CRS=with-crs MRTS=no-mrts`: ausgewählter Fall mit HTTP 403 und Regel `942270` abgelehnt; Audit, Cleanup, Selected-Results und Artefaktvalidierung bestanden. Es gibt keinen beobachteten fehlgeschlagenen Apache-Job zu reparieren.

Identität: Parent `4ec7581056889f8c70f44c6725f6bfa65a7fc45b`; Framework `99a7985c1be92a2297b1b59208f64df6768f2cbf`; MRTS `8a6bb546c4c81d8ffc7be801dceac60c6925685f`; CRS `e03a4f6dabc7a30ebd8c52c97d28a154f590a48f`; Profil `with-crs-no-mrts-40233061042-1`, Apache-Zelle `crs-40233061042-1-apache`, logisches Profil `native-httpd-module`.

Apache-Kompaktartefakt `12614940472` wurde im Speicher heruntergeladen/gelesen; sein SHA-256 entspricht GitHubs Digest: `4da09921b83210e54028d449f33dd544d044e54b7de48caaced00a69de7c8832`. Es enthält genau `functional-facts.json`, `manifest.json`, `profile-cell-receipt.json`; rohe Audit-/Ergebnisdaten sind Hashreferenzen, keine enthaltene Rohevidence. Aggregate-Artefakt `12614138658` meldet technischen PASS für fünf Zellen und funktionalen PASS begrenzt auf `selected_crs_block_case_only`: **5 passed, 0 failed, 6 blocked, 13 not_run**, `coverage_complete: false`, `merge_eligible: false`. Apache-/HAProxy-Allow-Kontrollen sind `not_observed`; no-MRTS ist für sie per Workflow/Source deklariert. Andere Zellen behalten Host-/Framework-Attestierungsgrenzen. Grüne CI qualifiziert daher nicht die vollständige Runtime-Matrix.

Echte Python-XML, alle vier Go-Modulreports und 71 native gcov-Reports wurden importiert. Haupt-PR-Coverage auf neuem Code **80,5 %** besteht die unveränderte 80-%-Bedingung; Advisory-Branch-Coverage auf neuem Code ist **82,7 %**. Kumulierte `master`-Previous-Version-Coverage **0,6 %** bleibt eine eigene Baseline-Aussage und wurde durch diesen PR weder repariert noch auf 80 % angehoben. Alle 18 Nicht-Sonar-Workflows am zugeordneten Head endeten erfolgreich.

## Historische Sonar-Nachweistabelle des exakten Heads

Alle Zeilen sind historische exakte Head-Nachweise für `4ec7581056889f8c70f44c6725f6bfa65a7fc45b`, Scanner `8.2.0.6438`, CFamily `6.85.0.102562`, [Lauf 40233061104](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40233061104). Upload allein bedeutet keinen Abschluss.

| Projekt | CE-Task | Analyse-ID | Terminale Verarbeitung / Gate |
| --- | --- | --- | --- |
| Hauptprojekt, PR 421 | `AaF03ulBdkEpBguA0oKZ` | `081d99d7-c136-4a67-b039-96507ad472a4` | SUCCESS; ERROR allein wegen New-Code-Security-Rating E / drei Issues. Coverage, Reliability, Maintainability, Duplikation und Hotspot-Review bestehen. |
| C++20-Advisory-Branch | `AaF03nsWdkEpBguA0oJ9` | `e29a042c-b9e6-4ffa-b6e4-f463dce07c34` | SUCCESS; ERROR. Unabhängige Advisory-Findings bleiben; New-Code-Coverage 82,7 % besteht. |
| C++23-Advisory-Branch | `AaF03alqJ8I9a074ReRm` | `0fdc39d6-930f-4ae9-bdf3-876d7670b4d3` | SUCCESS; ERROR. Unabhängige Advisory-Findings bleiben; New-Code-Coverage 82,7 % besteht. |

Bei allen drei Analysen sind die unveränderten Gate-Bedingungen `new_reliability_rating <= 1` (Ist 1), `new_security_rating <= 1` (Ist 5, ERROR), `new_maintainability_rating <= 1` (Ist 1), `new_coverage >= 80` (Ist Hauptprojekt 80.5, Advisories 82.7), `new_duplicated_lines_density <= 3` (Ist 0.0) und `new_security_hotspots_reviewed >= 100` (Ist 100.0). Keine Bedingungen wurden ignoriert.

Die acht neuen Marker-Tests heißen `test_current_run_marker_rejects_outside_symlink_before_restore`, `test_current_run_marker_fifo_fails_without_waiting_for_a_writer`, `test_current_run_marker_cannot_alias_an_outside_hardlink`, `test_current_run_marker_rejects_oversized_input_without_unbounded_read`, `test_current_run_marker_checks_directory_trust_before_reading`, `test_owned_legacy_marker_preserves_append_and_explicit_id_behavior` `test_current_run_marker_does_not_accept_a_valid_prefix_after_short_read` und `test_public_prepare_cannot_overwrite_an_outside_marker_target` in `tests.test_sonar_evidence_boundaries.SonarEvidenceBoundaryTests`.

Die historischen drei Jobs erhalten echte Coverage, 1.345 Source-/242 Testdateien, 136 native Units und vier Go-Module. Architekturwarnung, native Zahlen, FIFO-Parserwarnung und Python-Warnungen vollständiger Advisories bleiben an jene Revision gebunden. Exakte CE-Activity/Tasks und Analyse-IDs mit Scannerkontext-SHA abfragen; Project-Latest und nicht unterstütztes `api/ce/component?pullRequest`-Filtern reichen nicht als PR-Nachweis.

## Scan der Source-Änderung und neue Entscheidungen

Alle drei Jobs in [Lauf 40238653971](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40238653971) endeten am sauberen `59bc0842cea90d4052c0d005218fae3aca14c2b2`, mit Scanner `8.2.0.6438` und CFamily `6.85.0.102562`. Die Serververarbeitung ist terminal SUCCESS; alle tatsächlichen Gates bleiben allein wegen Security-Rating E auf ERROR. Die unveränderten anderen Bedingungen bestehen: Reliability/Maintainability 1, Duplikation 0,0 %, Hotspot-Review 100 %, Coverage mindestens 80 %. Keine Bedingungen wurden ignoriert.

| Projekt | CE-Task | Analyse-ID | New-Code-Coverage / offene Schwachstellen |
| --- | --- | --- | --- |
| Hauptprojekt PR 421 | `AaF1HfLSwSmsgR9Bxyj2` | `cb8fbb9c-1342-45f1-9b45-fb7f427d7a8c` | 82,3 % PR-Coverage; 8 Issues |
| C++20-Advisory | `AaF1JGXMnC1ELI2PKeSx` | `b7c0cc6c-1f55-4195-81be-bbc6e01cf13b` | 83,7 % Branch-New-Code-Coverage; 27 Issues |
| C++23-Advisory | `AaF1INr6oFotzZs8r-QJ` | `bb234bff-19a3-4929-8eaf-df9f71b6ade4` | 83,7 % Branch-New-Code-Coverage; 24 Issues |

Jeder Job bestand echte Header-Vorbereitung und Coverage-Produzenten, importierte Python-XML, vier Go-Reports und 71 gcov-Reports und erhielt **1.348 Source-/243 Testdateien, 136/136 native Units und vier Go-Module**. Echter Host-Kontext reduziert native Funktionsfehler auf **2/2.263**, ungelöste Projekt-Includes auf **0/1.132**, bei Qualität **95,81/100**. Die Logs melden zusätzlich eine fehlerhafte Klasse von sechs, sieben Statements von 33.762 und ein ungelöstes externes Include. Sie nennen keine Source-Orte für diese verbleibenden aggregierten Fehler; diese Orte und vollständiger Ziel-/Variantenkontext bleiben offen. C/C++-Taint ist in AutoConfig weiterhin ausdrücklich deaktiviert: Der höhere Wert beweist keinen Taintabschluss.

Beide Advisories melden weiterhin Python-Kostenskip und zwei Predecessor-Warnungen: 15.738 UCFGs insgesamt, 167 Einstiegspunkte, 5.269 behalten, 32 Python-Taintregeln. Die Haupt-PR-Analyse behält 1.207/13 aus derselben Gesamtzahl, mit 18 geänderten/neuen Dateien; das Fehlen dieser Meldungen beweist keine Reparatur. Die FIFO-Warnung bleibt in allen drei. Das Hauptprojekt ignoriert die Architekturperspektive weiterhin wegen 44 Labels. Beide Advisories melden außerdem fehlende Blame-Daten für `connectors/envoy/config/lib/tls_yaml_render.sh`; der letzte lokale Commit dieser versionierten Datei ist `75ea06c3cbcf1f909dae9e101faa528229316b80`. Keine Coverage-Importwarnung wurde beobachtet.

Das reparierte Marker-Issue `AaF0ZnMPLhxv2LRQWeOQ` / `AaF0ZlcF7GRUxAPzGlmF` fehlt in beiden vollständigen Advisory-Inventaren ohne Statusänderung. Zusammen mit den Regressionstests belegt dies die abgegrenzte Marker-Korrektur. Das getrennte Manifest-Issue `AaF0ZnMPLhxv2LRQWeON` / `AaF0ZlcF7GRUxAPzGlmB` bleibt bei 1745: Eingelesenes JSON beeinflusst Payload-Bytes, während `report_path(connector_root, "verified_run_manifest", "json")` das Ziel festlegt. Kein zusätzlicher dynamischer Manifest-Angriffstest wurde ausgeführt. C++23 lässt zusätzlich die drei unveränderten Evidence-Reader-Findings aus, die C++20/Hauptprojekt weiter enthalten; der Unterschied erklärt ihr Verschwinden nicht und gilt weder als autorisierter Abschluss noch als gleiches aktuelles Inventar.

Fünf neue Helper-Flüsse wurden vollständig unabhängig geprüft, ab explizitem CLI-`--output-root` und `fresh_root`; sie werden nicht aus den ursprünglichen drei Issues abgeleitet. Jede Zeile ist eine eigene False-Positive-Vorlage für den festen CI-Aufrufer und validierten Operator-Ausgabevertrag, ohne Statusänderung:

| Sink / Regel / Flussorte | Hauptprojekt-Issue | C++20-Issue | C++23-Issue | Konkreter Gegenbeleg |
| --- | --- | --- | --- | --- |
| 86 / S8707 / 9 | `AaF1HfgA7GRUxAPzPdPg` | `AaF1JG-OgQ6c6GT2j3RO` | `AaF1IOniIES1tmkRWQi0` | Absoluter, enger, frischer externer Root; Traversal, System-/Source-/breite Pfade, vorhandene Pfade und Symlinks abgewiesen; Erzeugung mit Modus 0700. |
| 119 / S8707 / 18 | `AaF1HfgA7GRUxAPzPdPh` | `AaF1JG-OgQ6c6GT2j3RM` | `AaF1IOniIES1tmkRWQi2` | Festes Sources-Kind, SHA-256-geprüftes Archiv, erwartetes Top-Level ohne absolute/Traversal-Member, `data`-Extraktionsfilter. |
| 129 / S8705 / 18 | `AaF1HfgA7GRUxAPzPdPe` | `AaF1JG-OgQ6c6GT2j3RK` | `AaF1IOniIES1tmkRWQiz` | Festes Programm/argv ohne Shell; Ausgabe nur innerhalb eines einzelnen `--prefix=`- oder gleichwertigen Zielarguments. |
| 180 / S8707 / 17 | `AaF1HfgA7GRUxAPzPdPi` | `AaF1JG-OgQ6c6GT2j3RL` | `AaF1IOniIES1tmkRWQi1` | Feste Sources-/Downloads-/Logs-Kinder des validierten privaten Roots. |
| 211 / S8707 / 13 | `AaF1HfgA7GRUxAPzPdPf` | `AaF1JG-OgQ6c6GT2j3RN` | `AaF1IOniIES1tmkRWQi3` | Festes lighttpd-build-Kind dieses Roots. |

Die sechs benannten Tests in `tests.test_sonar_native_context.SonarNativeContextTests` paaren falschen Archivhash/Traversal, umgeleitete/Source-/vorhandene Ausgabe, fehlende/Link-Artefakte und mehrdeutige Includes mit erlaubten regulären Archiven/privater Ausgabe/konfigurierten Headern. Ein unabhängiger Lauf bestand alle sechs (0,020 s). Zusätzliche begrenzte Probes wiesen acht Roots ab (relativ, Dot-Dot, `/etc`, `/usr`, Newline, Komma, NUL, Source-Baum); ein erlaubter Root bestand mit Modus 0700. Ein echter Python-Kindprozess erhielt Leerzeichen, Semikolon und Command-Substitution-Text als ein literales Prefixargument; kein Sentinel entstand. Der Workflow setzt die Ausgabe fest auf den aufrufeigenen `RUNNER_TEMP/sonar-native-context`. Diese Prüfungen beweisen keinen Schutz gegen konkurrierenden Pfadaustausch durch denselben Benutzer oder jedes Upstream-Configure-Verhalten bei Pfadnamen.

Fünf Nicht-Sonar-Workflows an `59bc0842` scheiterten allein an einem lokalen Entwicklerpfad in beiden neuen Abschlussdokumenten. Die portable Korrektur besteht lokal `check-variable-documentation` (101 Referenzen), Zweisprachigkeits-, Pfad- und Linkprüfungen. Ein neuer Dokumentations-Head-Lauf ist erforderlich; die Validatorprüfung wird nicht verändert, um den Fehler zu verdecken. Das aktuelle finale Head-CI-/Serverprotokoll gehört ins PR-Rücklesen, statt diesen Source-Lauf als finalen Nachweis zu behandeln.

| Anforderung | Einordnung bei diesem Dokumentationsstand |
| --- | --- |
| Drei Hauptprojekt-Issues | **weiterhin offen**: präzise False-Positive-Vorlagen vorbereitet; keine autorisierten Transitions oder grünes finales Gate. |
| Fünf neue Helper-Findings je Projekt | **weiterhin offen**: unabhängige vollständige Flussprüfung und Angriffs-/Kontrollprobes stützen einzelne False-Positive-Vorlagen; keine Transitions. |
| Advisory-Markerdefekt | **behoben und nachgewiesen** am Source-Änderungshead: Regressionskontrollen bestehen, das konkrete Issue fehlt in beiden neuen Advisories. Andere Issues behalten unabhängige Entscheidungsvorlagen. |
| Architekturperspektive | **extern blockiert**: exakter Delta geprüft, wiederholt HTTP 415, Server unverändert; unterstützte Medientyp-Anwendung und Rescan erforderlich. |
| Natives Parsing/Includes | Projekt-Includes **behoben und nachgewiesen**, 0/1.132; Parsing **weiterhin offen**, 2/2.263 Funktionen, nicht zugeordnete aggregierte Fehler und unvollständiger Ziel-/Variantenkontext. |
| C/C++-Taint / Python-Kosten und Predecessor / FIFO | **begründete Analyzergrenze** im oben beschriebenen Umfang, mit erhaltenen Restlücken. |
| Frühere Apache-CI-Unklarheit | **behoben und nachgewiesen** für ausgewählten Runtime-Lauf/Fall; vollständige Runtime-Qualifikation bleibt offen. |
| Coverage- und Scope-Erhalt | **behoben und nachgewiesen** am Source-Änderungshead, 82,3 % PR-/83,7 % Advisory-New-Code-Coverage mit echten Imports; keine Aussage zur kumulierten master-Coverage. |
| Finaler Abschlussnachweis | **weiterhin offen**: neue exakte Head-CE-/Analyse-/Gate-/Coverage-/Warnungsdaten aller drei Projekte und terminale CI nach Source-Änderung fehlen. PR bleibt Draft. |
