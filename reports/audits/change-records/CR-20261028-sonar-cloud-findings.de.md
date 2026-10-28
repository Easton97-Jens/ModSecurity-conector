# Change Record: CR-20261028-sonar-cloud-findings

**Sprache:** [English](CR-20261028-sonar-cloud-findings.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261028-sonar-cloud-findings |
| Datum (UTC) | 2026-10-28 |
| Basis-Revision | `15cea9e4d778fa1ec6e27e6fe084b347010f1367` |

## Motivation und Problemstellung

Die angeforderte Behebung umfasst alle 15 konfigurierten Parent-Cloud-Projekte (C++17-Hauptprojekt, zwei unverbindliche Standardanalysen, zwölf native Sicherheitsprojekte). Der vollständige authentifizierte paginierte Issue-/Hotspot-Abruf ergab 909 offene Vorkommen, 261 unterschiedliche Datei/Zeile/Regel/Meldungs-Positionen und null Hotspots. Das Hauptprojekt enthält 223 Issues. Haupt-/Native-Analysen gehören zur obigen Basis; der Advisory-Abruf gehört getrennt zu `1d161212124ad882064f8acfcefb721c67bc3d1d`. Dies sind Ausgangszahlen, keine Ergebnisse dieser Änderung.

## Akzeptanzkriterien

C17/C++17-Kompatibilität und Host-Callback-ABI erhalten, zutreffende Quellcodebefunde korrigieren, betroffenes Verhalten prüfen und einen Draft-PR erstellen. Quellcodekorrekturen des ursprünglichen Bestands adressieren 180 Positionen; 81 einzeln untersuchte Ausgangskandidaten benötigen noch Cloud-Bestätigung oder ausdrückliche False-Positive-Einstufung. Keine serverseitigen Statusänderungen wurden vorgenommen. Vollständiger Abschluss erfordert CI-/Cloud-Evidence am aktuellen Head und Klärung dieser Kandidaten; er wird nicht behauptet.

## Implementierungsentscheidung und Begründung

Apache speichert mutable Transaktionszeiger im Modulvektor `request_config` statt einer String-Tabelle; Suche über aktuelle/Haupt-/vorherige Requests und Owner-Bereinigung bleiben erhalten. NGINX erhält die Breite von Host-Ergebnissen, begrenzt Status vor der Konvertierung und verwendet einen const Allocator-Snapshot nur für wirkungslose PCRE2-/deaktivierte Hooks; echtes PCRE1 behält seinen mutablen Wiederherstellungszeiger. HAProxy begrenzt die ursprüngliche Response-Headerzahl vor der Verengung und prüft die Allokationskapazität vor Schreibzugriffen im zweiten Durchlauf. Private Zeiger/Schleifen sind const/lokal begrenzt; APR-Zeitformatierung folgt dem Typvertrag. Der Cleanup-Owner des Evaluators ist weder kopierbar noch verschiebbar.

Python vereinfacht Archivkanonisierung bei Erhalt ursprünglicher Bytes bei semantischen Nulländerungen, nutzt Funktionstypparameter und spezifische Assertions und zerlegt gleichwertige Timeout-/Fehlerausdrücke. Shell-Auswahlen weisen unbekannte Werte ausdrücklich ab. Drei reine Test-SDK-Observer nutzen bedingt modernes `contains` unter Erhalt von C++17-Fallbacks. Diese Quellcodepflege nimmt I12-Qualifikation nicht wieder auf.

## Geänderte Dateien

Betroffene native Apache-/NGINX-/HAProxy-/lighttpd-Dateien und Fixtures; `common/scripts/modsecurity_targeted_eval.cc`; gemeldete Python-/Shell-Helfer unter `ci/`; `scripts/version_updater_common.py`; drei SDK-Observer-Quellen; betroffene Apache-/NGINX-Tests und Framework-Updater-Assertion. In `config/testing/active-cases.json` ändern sich ausschließlich dreizehn geprüfte Digests; Definitionen/Auswahl bleiben gleich. `reports/testing/test-selection-archive.generated.json` wird über den bestehenden Generator regeneriert. Leserorientierte Dokumentation sind dieser Record und sein englischer Begleiter. Die manuell geprüfte Entscheidungsquelle [Triage-JSON](../sonarqube-cloud-20261028-triage.json) nennt alle 83 aktuellen Kandidatenpositionen und ihre ursprünglichen Projekt-/Issue-IDs. Framework/MRTS, Gitlinks, Dependencies, Analyseumfang, Regeln und Gates bleiben gleich.

## Ausgeführte Befehle

Alle Befehle nutzten RTK und externe Task-eigene Build-/Ausgabewurzeln; detaillierte Argument-/Exit-Aufzeichnungen bleiben in der Task-Evidence erhalten.

| Befehl/Verfahren | Beobachtetes Ergebnis |
| --- | --- |
| `/usr/local/bin/sonar-with-env auth status` und paginierte Issue-/Hotspot-/Analyse-/Gate-/Regelabfragen | Verbunden; alle 15 Projekte gelesen; keine Statusänderungen |
| `make check-apache-c17` | PASS, C17 `-Wall -Wextra -Werror`; ursprüngliches nur gelesenes Framework ausgewählt |
| Drei Apache-Harness-/Cleanup-Quellen mit `cc -std=c17 -Wall -Wextra -Werror -fsyntax-only` | PASS |
| NGINX-Produktion/Fixtures, GCC/Clang, `MODSECURITY_SANITY_CHECKS=0/1` | PASS, 36 C17-Kompilierungen; Produktion besteht zusätzlich Clang `-Wshorten-64-to-32 -Werror` |
| `make check-targeted-evaluator-cpp17` | PASS, Kompilierung/Link mit installiertem SDK |
| `sh connectors/lighttpd/build/build_module.sh` mit gepinnten gepatchten Headern | PASS, reale C17-Modulkompilierung/Link |
| `sh connectors/haproxy/htx-overlay/build-overlay.sh` mit gepinnter Quelle und acht Workern | PASS, nativer Build; vorhandene Warnungen in unberührtem Binding/Common bleiben |
| SPOP-Quelle C17-Warning-as-Error-Syntax; `make check-haproxy-htx-overlay` | PASS |
| Drei SDK-Observer, C++17/20/23-Warning-as-Error-Syntax | PASS, neun Kompilierungen |
| Sechs ausdrücklich ausgewählte Updater-Unittest-Methoden | PASS, Archividempotenz/-Zulassung und Python-/Go-Updateverhalten; Standardsuite unverändert |
| Geändertes Python über `ast.parse`; Legacy-Smoke-Skript `sh -n`; `shellcheck -x` | PASS |
| `ci/tools/run-active-tests.py --group apache --group null-guard --execution common.targeted-cpp-allow --group nginx --group haproxy` mit privaten externen Wurzeln | PASS, 15 ausgewählte aktive Fälle einschließlich tatsächlicher Evaluator-Allow-Ausführung |
| `make check-bilingual-docs`; `make check-doc-links`; Change-Record-Archivprüfung | PASS |
| Folgekorrekturen: nativer Apache-/HAProxy-/lighttpd-Build, 36 NGINX-Kompilierungen und drei SDK-Accessor-Standards | PASS |
| `make check-apache-common-adoption`; `make check-nginx-common-adoption`; `make check-lighttpd-common-adoption`; `make check-haproxy-htx-overlay`; zwei Config-Referenztests und drei gezielte NGINX-Checker-Kontrollen | PASS; positiver Vertrag sowie Ablehnung von Wrapper-Bypass und unbekanntem Include bestätigt |
| `make check-active-inventory PYTHON=/usr/local/bin/python3.15` | PASS, 100 Standardfälle / 80 Ausführungen; 1.893 On-Demand-Fälle getrennt; Archiv stimmt überein |

Der erste Active-Runner-Versuch wies ein fehlendes Ausgabeverzeichnis vor den Fällen zurück; der nächste wies einen veralteten Quellcode-Digest nach einer letzten Whitespace-Änderung zurück. Bindings/Archiv wurden vor dem finalen Lauf aktualisiert. Keiner der zurückgewiesenen Versuche ist Erfolg. Die Native-Context-Vorbereitung konfigurierte und prüfte Hostquellen per Checksumme, wies aber bei der abschließenden Prüfung des unveränderten Checkouts parallele Änderungen zurück. Strikte ISO-C17-Verarbeitung von GNU-Erweiterungen aus HAProxy-Upstream scheiterte; der tatsächliche native Host-Build oben bestand. Dokumentationsprüfungen scheiterten zunächst, da das gepinnte Framework im neuen Worktree nicht materialisiert war. Nach Initialisierung des exakten vorhandenen Gitlinks bestanden Bilingual-/Link-Gates und `shellcheck -x`; keine Diagnose wurde unterdrückt. Der aktiven NGINX-Extraktionsfixture fehlte zunächst der neue private Snapshot-Typ; acht betroffene Fixtures wurden angepasst, der exakte aktive Fall bestand und sieben benachbarte Setups kompilierten ohne Ausführung ihrer Szenarien. Die folgende Evaluator-Auswahl benötigte explizites `RUNNER_TEMP`; der Fehler wegen fehlender Variable blieb erhalten und die finale Auswahl wurde mit privater externer Wurzel wiederholt. Finale Ergebnisse des ausgewählten Laufs/der Dokumentationsprüfungen gehören nach Ausführung in den PR. Der erste PR-Head `108530d96b3b8dd783264831edc7714dd6db75b1` bestand die drei allgemeinen Sonar-Jobs/Gates, meldete aber 23 zusätzliche Wartbarkeitshinweise: Folgekorrekturen adressieren 22; ein weiterer nativer Cleanup-API-Kandidat bleibt. Damit bestehen 82 aktuelle Entscheidungsvorschläge; der ursprüngliche Bestand mit 261 Positionen bleibt getrennt dokumentiert.

CI am ersten Head zeigte zwei Schreibweisen-Inkompatibilitäten in Quellcodeprüfern. Apache-Direktivenextraktion erlaubt jetzt eine optionale explizite Callback-Adresse; strukturelle Apache-/NGINX-Prüfungen erhalten ihre Invarianten und erkennen aktuelle Const-/C17-Formen. Die Konfigurationsreferenzprüfung besteht mit allen 21 generierten Dateien unverändert; zwei gezielte Konfigurationsregressionen bestehen.

Das Secret-Gate am ersten Head meldete 287 generische Treffer, alle im Triage-JSON. Jede unveränderliche Trefferzeile wurde einzeln als Issue-/Analyse-/Event-Bezeichner aus der authentifizierten Sonar-Antwort bestätigt. Gemäß bestehendem `.gitleaksignore`-Vertrag wurden ausschließlich exakte Fingerprints aus erstem Commit/Datei/Regel/Zeile eingestuft. Der unveränderte redigierte Standard-PR-Bereichsscan bestand anschließend. Eine Kontrolle mit neuem Commit erkennt alle 287 identischen Datei-/Regel-/Zeilenvorkommen an einer neuen Revision (erwarteter Scanner-Exit 1) und belegt, dass der Fingerprint zukünftige Vorkommen nicht ausnimmt. Aktuelles JSON nutzt `id`/`issue_id` für Bezeichner, um irreführende Credential-artige Feldnamen zu vermeiden. Kein Regel-/Pfadausschluss, keine Schwellwertänderung, Credential-Offenlegung oder History-Umschreibung erfolgte.

Die zweite Quellrevision `839eb00795f5c2622a4cfad3d4034def5765ac7b` bestand das erforderliche Sonar-Gate und beide Advisory-Jobs; die Hauptanalyse meldete null Bugs/Schwachstellen/Hotspots und drei Wartbarkeitshinweise. Der vorhandene Cleanup-API-Kandidat bleibt; ein neu sichtbarer HAProxy-Host-Callback benötigt ebenfalls seine mutable Signatur (`flt_ops.http_payload`). Damit stehen 83 Kandidaten in der Einzeltriage. Der dritte Hinweis betrifft überlappende Whitespace-Quantifizierer im Direktiven-Regex; ein optionaler, durch `&` abgegrenzter Block entfernt die Mehrdeutigkeit. Alle neun vorhandenen Callback-Einträge bleiben identisch; ungültige Eingaben mit 4.000/8.000 Leerzeichen benötigten vorher 0,212/0,880 s und danach 0,000724/0,001457 s. Dies sind begrenzte lokale Messungen. Die 21 generierten Referenzen bleiben unverändert; beide gezielten Konfigurationsregressionen bestehen. Die Folgerevision benötigt erneut CI-/Cloud-Nachweis.

Der vollständige Advisory-Abgleich an `9060770ae03c04b9dbfb2b5dd553a7505b79949d` ergab 66 offene C++20- und 73 offene C++23-Hinweise bei jeweils bestandenem Gate und null Hotspots. Zwei weitere private Const-Stellen lagen außerhalb der PR-Neucode-Sicht: Response-Konfigurationsleser in `msc_filters.c` sowie ein HTX-Blockiterator. Die vollständige private Apache-Lesekette ist jetzt const; Host-/Native-Signaturen bleiben gleich. Echter Apache-C17-Build, drei aktive Apache-Fälle, native HAProxy-Kompilierung/Link und beide Quellcodeverträge bestehen. Diese zwei zusätzlichen Quellcodekorrekturen erhöhen die adressierten Positionen auf 180 Ausgangspositionen plus 25 Folgepositionen; die 83 Entscheidungskandidaten bleiben getrennt. Die neue Revision benötigt eigene Cloud-/CI-Evidence.

## Security-Auswirkung

Kontrollen, Callback-ABI, Ownership-Prüfungen, JSON-Escaping, Regeln und Gates bleiben aktiv. Unabhängige Read-only-Untersuchung verfolgte Python-Pfad-/Argument- und native Taint-Kandidaten; keiner der vorgelegten Flüsse belegte eine verbleibende ausnutzbare Schwachstelle. Ein weiterer unabhängiger Kandidaten-Reviewer fand keinen konkreten Bypass/Rückschritt. Dies ist eine abgegrenzte Prüfung, keine Sicherheitszusage für das gesamte Repository.

Die 83 aktuellen Kandidaten umfassen 21 Apache- und 15 NGINX-Host-/API-Callback-Parameter; neun HAProxy-Callbacks und drei C-Struct-Member-Namensraummeldungen; neun begrenzte/escapte native Meldungen; zwanzig Python-Pfad-/Argument-/Inhaltsflussmeldungen; drei beabsichtigte HTTP-Fixture-Referenzen; drei begrenzte In-Memory-Textkopien, die als Logging gemeldet wurden. Vorhandene Root-Prüfungen, strikte SHA-/Variantenvalidierung, JSON-Escaping und Allokationsgrenzen bleiben erhalten. Explizite Operator-Pfade werden nicht stillschweigend eingeschränkt. Serverkandidaten bleiben offen; False-Positive-Freigabe oder Risikoakzeptanz werden nicht abgeleitet.

## Runtime-Evidence

Es wurde keine gehostete Connector-Runtime-Evidence erhoben oder beansprucht. Native Builds, Syntax, ausgewählte Unit-/Vertragsfälle und der gezielte Evaluator bleiben getrennte Evidence-Schichten. Historische I12-Ergebnisse qualifizieren diese Revision nicht.

## Bekannte Einschränkungen

Lokales Python ist 3.15.2 statt des Pins 3.15.1; die vorhandene virtuelle Umgebung ist 3.14.4. Keine Toolchain-Installation/-Änderung. Reale PCRE1-Header fehlen: Zeiger-/Signaturkompatibilität wurde im Quellcode geprüft, während PCRE2-Builds bestanden. Zusätzliche Clang-Präzisionswarnungen nur in Fixtures bestehen bereits; Produktions-Präzisionsprüfungen und gewöhnliche Warning-as-Error-Fixture-Builds bestehen. CI-/Cloud-Nachweis am aktuellen Head bleibt für verifizierte Lieferung erforderlich.

## Verbleibende Risiken

Unit-Fixtures belegen keine tatsächliche gehostete Apache-Redirect-/Subrequest-Suche: einige ersetzen den Modulvektor-Lookup, während der Cleanup-Harness reale Vektorspeicherung und Owner-Bereinigung ausführt. Alle 83 Kandidatenpositionen und neue Cloud-Befunde benötigen Weiterbearbeitung. Eine Quellcodekorrektur allein schließt kein Cloud-Issue.

## Nicht ausgeführte Prüfungen mit Begründung

Keine vollständige Standardsuite, All-Connector-Runtime-Matrix, historische I12-Kampagne, reale PCRE1-Kompilierung oder Produktionsbereitstellung. Ausschließlich betroffene Prüfungen wurden ausgewählt. Ausstehendes CI/Sonar am aktuellen Head ist kein PASS. Kein Merge ist autorisiert.

## Finaler Diff- und Review-Status

Unabhängige abgegrenzte Kandidatenprüfung fand keinen konkreten Bypass/Rückschritt; Whitespace-Prüfungen der Worker bestanden. Finale integrierte ausgewählte Prüfungen, Dokumentations-Gates und Delivery-Fakten müssen am aktuellen PR-Head gelesen werden. Draft-[PR #430](https://github.com/Easton97-Jens/ModSecurity-conector/pull/430) besteht; vollständiger Task-Abschluss bleibt teilweise, bis verbleibende Kandidaten und Evidence am aktuellen Head geklärt sind.
