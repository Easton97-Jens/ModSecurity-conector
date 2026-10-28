# Change Record: CR-20261001-pr370-refresh-relevance

**Sprache:** [English](CR-20261001-pr370-refresh-relevance.md) | Deutsch

Current-Master-Wartung von PR #370; keine Readiness-Promotion.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261001-pr370-refresh-relevance |
| Datum (UTC) | 2026-10-28 |
| Basis-Revision | `15cea9e4d778fa1ec6e27e6fe084b347010f1367` |

## Motivation und Problemstellung

Der Benutzer verlangte, den bestehenden Draft-PR [#370](https://github.com/Easton97-Jens/ModSecurity-conector/pull/370) auf den aktuellen Stand von `master` zu bringen, wobei `master` für die Phase-4-Verarbeitung maßgeblich ist. Der veröffentlichte Branch lag 13 Commits zurück; sein verbliebener Qualifikationscode verwies auf entfernte Common- und Connector-Limit-APIs. Die Sonar-Duplizierung auf neuem Code muss vor Abschluss exakt null sein. NGINX darf `master` folgen, bleibt aber von Readiness-B-Qualifikation und Runtime-Anrechnung ausgeschlossen.

## Akzeptanzkriterien

Die beobachtete Basisrevision normal mergen, keine Konflikte hinterlassen, aktuelle Master-Semantik für Phase 4 und technische Fehler bewahren, nur relevante additive Korrekturen erhalten, das aktive Inventar bei höchstens 100 Fällen halten, fokussierte lokale Validierung bestehen, diese zweisprachige Nachverfolgbarkeit aktualisieren, ohne Force über den bestehenden PR-Branch veröffentlichen und Exact-Head-CI sowie Sonar-Duplizierungsdichte/-zeilen/-blöcke von null erreichen. Ein direkter `master`-Push oder Merge ist nicht autorisiert.

## Implementierungsentscheidung und Begründung

Der normale Merge legte 43 Textkonflikte offen. Jeder konfliktbehaftete Produkt-, Common-, Dokumentations- und Workflowpfad wurde zunächst auf die exakte `master`-Version gesetzt. Anschließend wurde der verbleibende PR-Diff connectorweise geprüft. Veraltete Qualifikations-Harnesses, entfernte Body-Limit-Konfiguration, verwaiste Composite-APIs, überholte lighttpd-Keepalive-Behauptungen und alte Orakel für technische Fehler wurden aus dem Netto-Diff entfernt, statt Verhalten vor dem aktuellen Master wiederherzustellen.

Die erhaltenen Änderungen sind eng begrenzt: frische externe APXS-Profilregistrierungs-Stages für Wiederholungen; Envoy-Authorization-Path-Autorität und Auswahl der Response-Companion-Smoke-Regeln; ein HAProxy-Source-Checker, der Forward-Deklarationen korrekt behandelt; strengere Traefik-Fixture-Grenzen für Framing, begrenztes Lesen/Schreiben und Payload-Digests; sowie zwei kleine deterministische Testkorrekturen. Geprüfte Source-Hashes und das generierte Specialist-Archiv wurden ohne Änderung von Selektoren oder Fallzahlen aktualisiert.

## Geänderte Dateien

- Apache-Build-Containment und EN/DE-Dokumentation: `connectors/apache/build/apxs-wrapper.in`, `connectors/apache/README.md`, `connectors/apache/README.de.md` und `tests/test_apache_apxs_profile_registry_staging.py`.
- Geschützte Envoy-URI und Response-Companion-Smoke-Pfad einschließlich EN/DE-Dokumentation und Tests: `connectors/envoy/src/envoy_ext_authz_service_main.c`, `connectors/envoy/config/envoy-ext-authz-smoke.yaml.in`, `connectors/envoy/harness/run_envoy_connector_runtime.sh`, `common/rules/modsecurity_response_companion_smoke.conf`, `connectors/envoy/README.md`, `connectors/envoy/README.de.md` und `tests/test_envoy_transport_hardening_contract.py`.
- HAProxy- und Traefik-Verifikation: `ci/checks/connectors/haproxy/check-haproxy-htx-overlay.py`, `connectors/traefik/scripts/runtime_native_smoke.py` und `tests/test_traefik_transport_hardening_contract.py`.
- Deterministische Testkorrekturen: `tests/test_bounded_nginx_cases.py` und `tests/test_logical_connector_example_matrix.py`.
- Inventar und generierter Begleiter: `config/testing/active-cases.json` und `reports/testing/test-selection-archive.generated.json`.
- Dieses EN/DE-Record-Paar und die EN/DE-Archivindizes.

## Ausgeführte Befehle

Alle Projekt-Shell-Befehle liefen RTK-wrapped. Umfangreiche Ausgabe und Go-Caches verwendeten private Pfade unter `/var/tmp/codex/ModSecurity-conector`.

| Prüfung | Beobachtetes lokales Ergebnis |
| --- | --- |
| Fokussiertes APXS-Modul | 7/7 bestanden. |
| Fokussiertes Envoy-Transportmodul | 3/3 bestanden. |
| Fokussiertes Traefik-Transportmodul | 6/6 bestanden. |
| NGINX-Umask- und logische Beispielregressionen | 3/3 bestanden; kein NGINX-Runtime- oder B-Qualifikationslauf. |
| `make check-haproxy-htx-overlay` | Bestanden. |
| `python3 ci/tools/update-test-archive.py --check` | Bestanden. |
| `make check-active-inventory` | Bestanden: 100 Core-Fälle, Hard-Limit 100, 1.893 On-Demand-Fälle. |
| Prüfung der aktiven Sechs-Gruppen-Auswahl | Bestanden: 22 Ausführungen und 26 expandierte Fälle. |
| Aktive Sechs-Gruppen-Ausführung mit `--strict-skips` | Der finale Lauf bestand alle 26 Fälle ohne Skip. Beim ersten Versuch fehlten explizite libmodsecurity-Pfade; der zweite zeigte einen schreibgeschützten Standard-Go-Cache. Der erfolgreiche Wiederholungslauf verwendete vorhandenes System-libmodsecurity und private externe Go-Caches. |
| Unabhängiges Security-Review des eingegrenzten Diffs | Keine validierte neue Security-Schwachstelle; `git diff --check origin/master` bestand. |
| Statische Common-/Adapter-Contract-Targets | Alle sechs ausgewählten Targets bestanden. |
| EN/DE-, Link-, Variablen- und generierte Connector-Referenzprüfungen | Nach read-only Materialisierung des exakten Framework-Gitlinks bestanden. |
| Direktes repositoryeigenes Envoy-Connector-Buildskript | Gegen das vorhandene System-libmodsecurity bestanden; beide Service-Binärdateien wurden erzeugt. Der Root-Lifecycle-Wrapper wurde getrennt abgebrochen, nachdem während der Vorbereitung kein beobachtbarer Fortschritt entstand; dafür wird kein Wrapper-Build-Pass behauptet. |
| `sh -n` für beide geänderten Shellpfade | Bestanden. Direkter ShellCheck lief ebenfalls, meldete jedoch bestehende Template-Shebang-, `CDPATH`-, Dynamic-Source- und beabsichtigte Splitting-Findings außerhalb der geänderten Zeilen; keine Suppression wurde ergänzt. |
| Change-Record-Struktur und finale Whitespace-Prüfungen | Lokal bestanden. |

## Security-Auswirkung

Envoy behandelt nachgelagerte Original-URI-Hinweisheader nicht mehr als Autorität für die Policy-Auswahl; der Path des Authorization-Requests ist maßgeblich. Traefik-Evidence-Reader verwerfen mehrdeutiges Content-Length/Transfer-Encoding-Framing, nicht kanonische oder übergroße Fixture-Längen, unvollständige Eingaben, zu kurze Ausgaben und gleich lange Payload-Ersetzungen. APXS-Rebuilds vertrauen keinem früher bereitgestellten Unterverzeichnis und überschreiben es nicht. Der HAProxy-Checker verwechselt eine Forward-Deklaration nicht mehr mit einem Funktionskörper. Es werden keine Suppression, Quality-Gate-Lockerung, Dependency-Änderung, Berechtigungserweiterung oder Compiler-Warning-Reduktion eingeführt.

## Runtime-Evidence

Der ausgewählte aktive Lauf übte 26 geprüfte Fälle über Common, Apache, HAProxy, Envoy, Traefik und lighttpd aus, einschließlich des echten Stock-lighttpd-Loopback-Allow-Falls. Dies sind begrenzte Contract- und Component-/Runtime-Prüfungen nur für das ausgewählte Inventar. Sie belegen weder drei frische Starts noch jedes G1–G9-Gatter, Produktionsreife oder Readiness B für jedes Nicht-NGINX-Profil. NGINX wurde nur über den eingehenden `master` aktualisiert und erhielt keine Readiness-Anrechnung.

## Bekannte Einschränkungen

Der APXS-Wrapper setzt weiterhin vertrauenswürdige Vorfahren des externen Build-Roots voraus; die Änderung begrenzt Wiederverwendung unterhalb dieser Grenze, behauptet aber keinen Schutz vor einem feindlichen lokalen Schreiber, der einen Vorfahren kontrolliert. Die erhaltenen Traefik-Änderungen härten den lokalen Evidence-Harness und erweitern keine Connector-Fähigkeitsbehauptungen. Das ausgewählte aktive Inventar ist weder die historische vollständige I12- noch die Gesamtprofil-Qualifikationsmatrix.

## Verbleibende Risiken

Hosted-Prüfungen und Sonar müssen an die final ausgelieferte SHA gebunden sein. Lokaler Erfolg belegt weder Hosted-Workflow-Berechtigungen noch externe Service-Verfügbarkeit oder null Duplizierung auf neuem Code. Der Root-Envoy-Lifecycle-Wrapper wurde lokal nicht abgeschlossen, obwohl das darunterliegende repositoryeigene Buildskript bestand. Das größere Readiness-B-Ziel bleibt unbewiesen, bis die erforderliche Host-/Profil-/Run-Evidence vorliegt.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Neustart der historischen Vollmatrix/I12, keine G1–G9-Kampagne über alle Profile, kein Framework-/MRTS-Source-Schreibvorgang, keine Dependency-Installation, kein direkter `master`-Push, Force-Push oder Merge. Exact-Head-CI und Sonar sind erst nach Veröffentlichung des Nachfolger-Commits verfügbar und stehen zu diesem Zeitpunkt noch aus.

## Finaler Diff- und Review-Status

Master-first-Relevanz- und Phase-4-Audits sind abgeschlossen. Der eingegrenzte Diff erhielt unabhängige Security-, Testauswahl- und Dokumentationsreviews; die oben qualifizierten lokalen statischen, Dokumentations-, Build-, fokussierten und aktiven 26-Fall-Prüfungen bestanden. Delivery-SHA-Abgleich und Hosted-CI-/Sonar-Ergebnisse werden nur nach tatsächlicher Beobachtung festgehalten.
