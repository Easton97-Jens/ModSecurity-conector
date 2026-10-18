# Change Record: CR-20261018-i12-apache-acceptance-instrumentation

**Sprache:** [English](CR-20261018-i12-apache-acceptance-instrumentation.md) | Deutsch

Apache-spezifische Abnahmeinstrumentierung; Runtime-Qualifikation bleibt offen.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-i12-apache-acceptance-instrumentation |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `f1fb6f8e2d2ed59f00da1b82fe788d934c3f743d` |

## Motivation und Problemstellung

Die 155 ursprünglichen Apache-I12-Verträge erfordern unabhängige Beobachtungen von Host, SDK, physischem Sink, Client, Backend und Cleanup. Vorhandene Captures lassen Lücken bei echten Bucket-Lesezugriffen, Multipart-Dateien, nativen Fehlerstellen und abnormaler Beendigung. Diese Änderung erweitert das bestehende Apache-Lifecycle-Paket um begrenzte Helfer und explizite Herkunftsnachweise.

## Akzeptanzkriterien

Alle 155 ursprünglichen Identitäten und Erwartungen bleiben erhalten. Quellen, Konfiguration, Binaries, SDK, Helferobjekte und Laufeingaben werden per Hash gebunden. Tatsächliche Grenzen werden beobachtet; fehlende Beobachtungen bleiben null. Vor jedem neuen vollständigen PASS sind ein frischer Build aktueller Quellen und vollständige fallspezifische Hostbeweise erforderlich. Original-Oracle-Abstimmung, alle Runtime-Gruppen, fünf physische Sinkfehler und abschließendes CI/Sonar bleiben eigene Abschlussanforderungen.

## Implementierungsentscheidung und Begründung

Fallprivate Konfigurationen, Marker, Uploadverzeichnisse und Hashbindungen erweitern den Batchtreiber; die Prüfung extrahiert vorhandene Capture-Rollen. Keepalive-/Abbruchclients und Common-Sink-, Host-I/O-, Bucket-, Multipart- und Fehlerhelfer sind explizit aktivierte Testartefakte. Multipart-Callbacks beobachten öffentlichen SDK-Zustand nach echter Body-Verarbeitung und Cleanup und erhalten Rückgabe/errno. Der Fehlerhelfer erfasst die echte SDK-Rückgabe von msc_add_request_header; ein zusätzlicher GNU-Wrapper für diese API wird nicht behauptet.

Der Builder des beobachteten Moduls verlangt einen verwerfbaren Quellexport, vollständigen Capture-Beleg, alle 33 frisch gebauten Product-Objekte, genaue SDK/Header-Identität und hashgebundenes kanonisches Compilerprotokoll. In einem externen Overlay ergänzt er versionierte Fehlerstellen und Hooks unmittelbar vor ausgewählten echten APR-Bucket-Lesezugriffen, kompiliert zwei Übersetzungseinheiten erneut, behält 31 frische Objekte und linkt vier Observer-Übersetzungseinheiten sowie drei Helferobjekte. Er erhält strikte Flags, prüft ELF-Härtung/SDK-Auflösung und prüft Quell-/Objekthashes erneut. runtime_qualification bleibt null.

Der Apache-Capture implementiert eine explizite Teilmenge von 26 Symbolen des gemeinsamen nativen Wrapper-Tupels. Der Builder verlangt jetzt genau diese Definitionen sowie die Wrapper für private Eventdateien und den Apache-Lifecycle. Zwölf Common-Runtime-/Finalize-/Response-Companion-Symbole, die Apache weder linkt noch aufruft, werden im Beleg getrennt aufgeführt, statt als Apache-Wrapper zu erscheinen. Die ELF-Prüfung verwirft weiterhin jede fehlende erforderliche Definition. CLI-Eingaben des Batchs werden vor dem Laden von Helfern kanonisch auf die versiegelten Fixture- und Artefakt-Mounts begrenzt; Datei-Hashing ist auf diese Mounts, den Framework-Regel-Mount oder die validierte private Speicherwurzel beschränkt. Beide Preload-Bibliotheken sind Admission-Pflicht und Teil der Binäridentität.

## Geänderte Dateien

ci/runtime/lifecycle/apache-i12/acceptance/: cases.py, batch.py, backend.py, review_batch.py, oracles.py, keepalive.py, cancellation.py, common_sink_boundary.c, host_io.c, host_bucket.c, multipart_observer.cpp, fault_boundary.c, build_host_io.py, build_host_bucket.py, build_multipart_observer.py, build_fault_boundary.py, build_observed_module.py.

Neue Tests: tests/test_apache_i12_acceptance_cases.py, test_apache_i12_acceptance_driver.py, test_apache_i12_acceptance_oracles.py, test_apache_i12_batch_review.py, test_apache_i12_cancellation.py, test_apache_i12_common_sink_boundary.py, test_apache_i12_fault_boundary.py, test_apache_i12_host_bucket.py, test_apache_i12_host_io.py, test_apache_i12_keepalive.py, test_apache_i12_multipart_observer.py, test_apache_i12_observed_module_builder.py.

Vorhandene Apache-Dateien: ci/runtime/lifecycle/apache-i12/launch.py, observed_curl.py, prepare.py; reports/audits/apache-i12-20261015/rule-equivalence-probe.py; tests/test_apache_i12_boundaries.py, tests/test_apache_i12_launch.py. Diese behandeln begrenztes Matching, Serialisierung und wiederholte Literale einschließlich Regressionstests. Dieses EN/DE-Paar dokumentiert den Umfang. Diese Instrumentierung ändert keine Produktquellen, gemeinsamen Capture-Manifeste/Observer, anderen Connectoren, Workflows oder Framework/MRTS-Gitlinks.

## Ausgeführte Befehle

Der Koordinator führte rtk proxy env mit PYTHONDONTWRITEBYTECODE=1 und externem RUNNER_TEMP/CODEX_TEST_TMP_ROOT in der virtuellen Parent-Umgebung aus: python -m unittest discover -v -s tests -p 'test_apache_i12_*.py' — 240 Tests, OK, skipped3, exit0, einschließlich Regressionen für den exakten Wrapperumfang, versiegelte Pfade und jede einzelne Preload-Admission. Die fokussierte Treiber-/Buildergruppe bestand 60 Tests, exit0. Ein früherer Versuch mit nicht vorhandenem RUNNER_TEMP scheiterte bei vier Setup-Operationen und bleibt ein ungültiger Versuch. Die separate aktivierte Batchprüfung anhand des tatsächlichen Smoke-Captures und der Quellmetadaten bestand 8 Tests, exit0. Die Common-Sink-Suite ohne Root-Rechte bestand 9/9 Tests ohne Skips, exit0 unter UID/GID65534; sowohl Kontrollpfad als auch gewrappter Pfad lieferten tatsächliches EACCES errno13. Dauerhafte Evidence: /var/tmp/codex/ModSecurity-conector/runs/i12-apache-414-acceptance-20261015/analysis/resume-20261018/nonroot-common-boundary-v1/evidence. Weitere Validierungsevidence liegt unter derselben resume-20261018-Wurzel.

## Security-Auswirkung

Fehleraktivierung erfordert explizite Testkonfiguration in privaten autorisierten Hosts. Helfer belegen kein Produktionsverhalten und rechtfertigen keine Erwartungsänderungen. Der Builder verwirft mehrdeutige Befehle, veraltete Eingaben, historische Objekte, unsichere Compiler-Nebenausgaben und abweichende Wrapper/SDK. Die Begrenzung auf versiegelte Pfade schließt eine unbeschränkte lokale CLI-Hashoberfläche; im privaten Controller wurde kein Pfad von einem entfernten Angreifer zu einem Dateilesezugriff nachgewiesen. Authentifizierung, Isolation, Compilerwarnungen und CI/Sonar-Kontrollen bleiben verpflichtend.

## Runtime-Evidence

Die passive Multipart/Host-I/O-Integration nutzt die echte SDK mit und ohne aktiviertes Preload, vergleicht Rückgabe/errno und beobachtet temporäre Dateien sowie tatsächliches Cleanup. Dies stützt ausschließlich Helfertransparenz. Historische Host-Captures behalten ihre eigene Identität. Kein neuer vollständiger Host-PASS, genehmigtes Original-Oracle, Produktfehler, keine Freigabe und kein I12_COMPLETE wird behauptet.

## Bekannte Einschränkungen

Die 41 bedingten Abstimmungsvorschläge benötigen weiterhin Quellfreigabe und Runtime-Bestätigung; 13 Original-Oracle-Lücken bleiben. Die abgeschlossene Helfersuite ohne Root-Rechte belegt nur ihre Berechtigungsgrenze; sie ersetzt nicht die Apache-Host-Sinkwiederholung. Cleanup nativer Transaktionen, physisches JSONL, Descriptor-/Prozess-Cleanup und Wiederherstellung durch Folgerequests benötigen vollständige Captures des aktuellen Builds für jeden zutreffenden Fall.

## Verbleibende Risiken

Injizierte Pfade können von natürlich auftretenden Fehlern abweichen. Aktivierung, tatsächliche SDK/APR-Rückgabe und Hostaktion müssen unabhängig beobachtet werden. Das Overlay-Linken erfordert vor Hostnutzung die Prüfung gegen den kanonischen Build. Fehlende Evidence bleibt null und verhindert Qualifikation.

## Nicht ausgeführte Prüfungen mit Begründung

Ein exakter Build des Heads 32ede7b kompilierte alle 33 Product-Übersetzungseinheiten in zwei byteidentischen sauberen Builds. Sein erster beobachteter Link schloss Kompilierung und Linken ab, scheiterte jedoch korrekt am verschärften ELF-Gate, weil der alte Apache-Builder zwölf gemeinsame Wrappernamen importiert hatte, die sein Capture nicht definiert. Der fehlgeschlagene Beleg bleibt erhalten und beweist kein Runtime-Ergebnis. Ein frischer Build/Link der abschließend committeten Quellen, alle 155 Hostausführungen mit aktuellem Build, fünf Sinkwiederholungen und abschließendes CI/Sonar des genauen Heads sind offene Koordinatorarbeit. Die vollständigen Bilingual- und Dokumentlinkprüfungen bestanden in einem privaten Mount-Namespace gegen Framework-Revision 99a7985c1be92a2297b1b59208f64df6768f2cbf; Gitlinks blieben unverändert und kein Mount trat nach außen aus.

## Finaler Diff- und Review-Status

Die Basisrevision wurde vor Erstellung dieses Paars mit ci/tools/new-change-record.py erneut geprüft. Beide Sprachen wurden manuell hinsichtlich technischer Fakten und Einschränkungen abgeglichen. rtk proxy python3 ci/tools/new-change-record.py check bestand, exit0 (nur Struktur); die kanonischen Bilingual-/Dokumentlinkprüfungen und rtk proxy git diff --check bestanden, exit0. Die RTK-Prüfung bestätigte Version1.0.1, den installierten Pfad und verfügbare gain-Auswertung. Alle Shellvalidierungen nutzten RTK. Abschließende integrierte Diffprüfung und Lieferung verbleiben beim Koordinator.
