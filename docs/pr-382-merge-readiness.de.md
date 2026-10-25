# PR #382: Abschluss für Review- und Merge-Entscheidung

**Sprache:** [English](pr-382-merge-readiness.md) | Deutsch

## Umfang und Revisionsbindung

Dies ist das führende Statusdokument für die separat beauftragte Inventar-/Runner-/Coverage-Migration vom 2026-10-25. Ihre Basis ist `d510d21dba7eab3c9f0ccbe579fbc9c105eb3da1`, an der #410 bereits integriert war. Historische [Checkliste](pr-382-checklist.de.md), [Übergabe](pr-382-i12-handoff.de.md), [Restmatrix](pr-382-i09-i12-rest-matrix.de.md) und [reduzierter I12-Abschluss](pr-410-i12-closeout-20261024.de.md) erhalten ihre ursprünglichen Revisionen und Ergebnisse; alte Arbeitsanweisungen sind aufgehoben. Daraus folgen weder ein neues `I12_COMPLETE` noch eine historische Hostqualifikation.

Dieses Dokument hält den implementierten Auswahl- und Messvertrag fest. Endgültige Identität von lokalem/Remote-/PR-Head, Checks, Coverage-Import/-Werte und Ready-Status müssen aus [PR-Beschreibung und Checks](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382) abgelesen werden. Frühere erfolgreiche CI/Sonar an der Basis verifiziert keinen Folgecommit.

## Eine aktive Auswahl

`config/testing/active-cases.json` ist die einzige Autorität für aktive Selektoren. Jede Ausführung zählt stabile Verhaltensfall-IDs, Anforderungen und logische Profile ausdrücklich auf, einschließlich unabhängiger Parameter innerhalb von Collectoren. Der Runner validiert vor jedem ausgewählten Kindprozess das gesamte expandierte Inventar gegen seine feste Obergrenze von 100. Gruppen-, Fall-, Ausführungs- und Go-Modulfilter erzeugen keine getrennten Budgets. Ein ausgewählter Collector enthält stets alle seine deklarierten Varianten. Unbekannte/leere Auswahlen, Quelländerungen und alternative ausführbare Inventare scheitern; die Auswahl wird niemals gekürzt.

Das geprüfte Inventar enthält 100 eindeutige expandierte Fälle in 81 Ausführungen. Die statische Prüfung umfasst verschachtelte Make-/Build-/geplante Selektoren und bestätigt erhaltene ursprüngliche Assertions in den 436 vorhandenen Hook-Manifest-Quellen. Die ersten 21 Migrations-/Reportkontrollen bestanden, einschließlich der Ablehnung von 101 synthetischen Fällen vor dem Start eines Sentinel-Kindprozesses. Diese Kontrollen zählen im selben Budget. Eine Wiederholung lokal oder in CI erhöht Ausführungskosten, nicht die Zahl verschiedener aktiver Fälle.

Standardeinstiege sind `make test`, `make lint` und `python3 ci/tools/run-active-tests.py`; alle automatischen Workflows und verschachtelten funktionalen Build-/Lintprüfungen müssen dasselbe Inventar verwenden. Python-Discovery ist an Paket- und Modulgrenzen gebunden; direkte Spezialkataloge benötigen ausdrückliches Opt-in. Statische Builds, Lint, Dependency-/Secretscanner und tatsächliche Konfigurationsvalidierung behalten ihre inhaltlichen Gates.

Die generierte Spezialtest-Disposition `reports/testing/test-selection-archive.generated.json` gehört zu `ci/tools/update-test-archive.py`. Sie ist nicht ausführbar und zählt Definitionen statt vollständig expandierter archivierter Szenarien. Erhaltene Spezialtestquellen erzeugen keinen neuen PASS. Explizite Spezialarbeit benötigt `ON_DEMAND_TESTS=1` und ihren dokumentierten konkreten Befehl; sie liegt außerhalb automatischer Standardauswahl.

## Erhaltene und verlorene automatische Abdeckung

Das generierte Archiv erhält Spezialdefinitionen und Quellhashes; aktuell erfasst es 5930 On-demand-Python-/Go-Definitionen statt expandierter Szenarien. Dies ist bewusst verlorene automatische Abdeckung und keine Behauptung, alle entfernten Fälle seien Duplikate. Erhaltene automatische Sicherheitsabsichten umfassen echtes Memory-Wiping/Allokationslimits, HTTP-Header-/Body-Deadlines und Recovery, Parent-APR-util-Pinpolicy/aktuelle Framework-Provenienz, Peer-Besitz, Reportidentität und quellgebundene Admission.

Archivierte Anforderungen umfassen vollständige Redirect-/Options-/Kapazitäts-/Parser-Parametermatrizen, I09-/I10-/I12-Fehler-/Lifecycle-Kampagnen, vollständige Scaffold-/Validator-Korpora, zufälliges Fuzzing, vollständigen H2-/H3-Preflight, NGINX-Inheritance-/Override-/Reload-/Error-Page-/Body-Buffer-Kampagnen, breite MRTS-Kataloge und ausgelassene Installer-/Admission-/Header-/Phasenvarianten. Insbesondere bleiben Kontrollen unbekannter/leerer Gruppen und die positive Installer-Private-Root-Kontrolle auf Abruf erhalten; ihre Produktionsguards bleiben wirksam. Kein Nachbarprofil erbt Nachweise: HAProxy SPOE unterscheidet sich von HTX; Envoy ext_authz von ext_proc; Traefik forwardAuth von native; lighttpd-Kompatibilität von stock/patched-native. Siehe [Testanleitung](testing-and-evidence.de.md) und [Quellrollen](sonar-source-roles.de.md).

Die geplante Abnahmevereinigung umfasst 56 Coverage-Fälle, zwei zusätzliche Shell-Pfadfälle, vier Scanner-Fixtures, einen Stock-Sidecar-Fall, drei strikte Peer-Fälle, 21 No-CRS-Konfigurations-/Start-/Allow-/Deny-Fälle, 11 CRS-Fälle und zwei NGINX-Callback-Fälle. Wiederholte IDs in Lint, lokaler Coverage oder Hosted-CI erzeugen keinen unabhängigen Fall. Lokale und Hosted-Ergebnisse werden getrennt erfasst; nicht ausgeführte oder blockierte Fälle werden niemals als bestanden gemeldet.

## Coverage und Nachweisgrenzen

Die frühere Sonar Automatic Analysis importierte keine Coverage: Coverage-Messwerte fehlten, während `new_lines_to_cover` null war. Dies war kein gemessenes Ergebnis von 0 %. Die Analyse über CI sammelt Reports während echter inventarselektierter Ausführung. Python verwendet tatsächliches Stdlib-Zeilentracing, die vier Go-Module behalten native `go test`-Profile und GCC/gcov misst tatsächlich gelinkte C-/C++-Quellen. Extrahierter temporärer Native-Fixturetext wird nicht der ursprünglichen Produktionsquelle zugerechnet. Geeignete Python-Kinder desselben Präfixes/derselben UID werden ohne Änderung ihrer Isolationsflags gemessen. Isolierte Kinder, solche mit bereinigter Umgebung/anderem Präfix/anderer UID/beendete Kinder und nicht ausgeführte Hostpfade können ungemessen bleiben. Dies sind Zeilenmessungen ohne Branch-Beobachtungen.

Das Reportmanifest bindet Quellrevision, Dirty-/Clean-Status, Inventar-Digest, ausgewählte Fall-IDs, Quell-/Reporthashes, Toolchain, tatsächliche SDK-Identität und Quellrollen-/Scanner-Konfigurationshashes. Beide Properties müssen vor Sammlung/Import dem geprüften Quellrollenvertrag entsprechen. Scannerimport verlangt den sauberen exakt veröffentlichten Quellstand. Reporterzeugung, erfolgreicher Import und endgültige Gesamt-/New-Code-Serverwerte sind getrennte Aussagen und benötigen jeweils beobachtete Nachweise. Bestehende Quality-Gate-Bedingungen, Produktionsumfang und New-Code-Baseline bleiben unverändert. Das bestehende Gate verlangt `new_coverage >= 80`; das frühere Projektstatusergebnis ließ diese Bedingung wegen fehlender Coverage-Messwerte aus. Die Schwelle bleibt erhalten.

## Späterer Wartungsbetrieb

Erst eine separat autorisierte Masterintegration ermöglicht den Live-Nachweis auf dem Default-Branch. Vertrauenswürdige Resolver-, Validator- und Publisher-Ergebnisse für Go/Python/Actions prüfen; einen tatsächlich zulässigen Kandidaten und wirklich erzeugten Wartungs-PR samt Autor/Basis/Head/Diff und nachgelagerter Pflicht-CI prüfen. Ein Lauf ohne Update beweist keine PR-Erstellung. Go verwendet `github.token`; eventuell freigabepflichtige PR-getriggerte Workflows vor der Behauptung unbeaufsichtigter Ausführung prüfen. Dependabot umfasst wöchentlich pip und die vier Parent-Go-Verzeichnisse mit sieben Tagen Go-Cooldown; sein konfiguriertes Fünf-PR-Limit wird nicht als globale Grenze behauptet. Dieser Auftrag veröffentlicht nichts auf dem Default-Branch.

## Rückverfolgbarkeit

[Change Record](../reports/audits/change-records/CR-20261025-pr382-global-inventory-coverage.de.md). Framework-/MRTS-Quellen, Repositories und Gitlinks liegen außerhalb des Schreibumfangs. Master-Merge, Release und Deployment sind nicht autorisiert.
