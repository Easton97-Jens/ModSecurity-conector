# Repository-Contract-Tests

**Sprache:** [English](README.md) | Deutsch

## Zweck und Grenze

\`tests/\` enthält fokussierte Python-Tests und native Fixtures für Root-Orchestrierung,
Konfiguration, Artefakt-Layout, Lifecycle-Wiring, Capability-Grenzen und
Path-/Security-Contracts. Sie liefern schnelle Regression-Coverage für
Repository-Verhalten, das ohne die Darstellung eines synthetischen Host-Laufs
als Evidence geprüft werden kann.

Diese Tests sind weder der Framework-Case-Katalog noch Ersatz für
Connector-Harnesses oder kanonische Runtime-Evidence. Bestandene Unit-Tests
belegen keine Production Readiness, CRS-Vollständigkeit, HTTP/2-/HTTP/3-
Verifikation, vollständige Matrix oder Strict-Verifikation für alle Connectoren.

## Ein automatisches Aktivinventar

[config/testing/active-cases.json](../config/testing/active-cases.json) wählt **100 expandierte Standardfälle / 80 Ausführungen** für alle automatischen lokalen, CI- und geplanten funktionalen Prüfungen gemeinsam. Die frühere zusätzliche Offline-Freigabe ist für die automatische Auswahl durch den abschließenden Umfangsstopp des Nutzers ersetzt. Connector-E2E bleibt bei 26 Fällen; historische I12-Host-/Matrix-/Oraclekampagnen bleiben geschlossen.

Dasselbe Schema-3-Inventar bewahrt **1893 On-demand-Fälle / 839 Ausführungen** außerhalb sämtlicher Standardpfade. `make test`, der Inventar-Runner ohne Selektor, Python-Discovery und automatische Gruppenfilter verwenden nur den Standardabschnitt. Eine gemeinsame Gruppe aktiviert keine archivierten Zeilen. Vollständige Schema-/Quell-/Selektorzulassung bleibt Pflicht; mehr als 100 expandierte Standardfälle werden vor dem ersten Kindprozess abgewiesen. Die Auswahl wird nie still gekürzt.

`make check-active-inventory` prüft ohne Ausführung. Für eine ausdrücklich beauftragte Spezialprüfung ist ein genauer Selektor erforderlich, etwa `python3 ci/tools/run-active-tests.py --on-demand --execution <archived-execution-id> --output-root <existing-external-parent>`. Die Freigabe ohne Gruppen-/Fall-/Ausführungsselektor scheitert. Aufbewahrte modulweite Befehle verlangen ausdrücklich `ON_DEMAND_TESTS=1`; in Standards und Zeitplänen bleibt es ungesetzt. Keiner der Wege erlaubt historische I12-Kampagnen, erhöhte Rechte oder Arbeit über Repository-Grenzen hinweg.

Sonar behält Quellanalyse am exakten Head, nativen Kontext, Required-/Advisory-Matrix, Secret-Isolation und echtes Warten auf das Gate. Seine speziellen Python-/Go-/Common-Coverage-Sammlungen laufen nicht mehr automatisch. Der aufbewahrte Collector verlangt vor Ausgabe oder Testbefehl ausdrücklich `--on-demand`. Coverage ist nach späterer Nutzerentscheidung für Sicherheit und Merge irrelevant; keine Sicherheitsregel, verbleibende Gate-Bedingung oder fachliche Assertion entfällt.

Die generierte [Archivdisposition](../reports/testing/test-selection-archive.generated.json) nennt aufbewahrte Definitionen außerhalb der Standardauswahl. Definitionszahlen sind keine expandierten Fallzahlen und kein PASS. Erzeugung erfolgt über `ci/tools/update-test-archive.py`. Statische Kompilierung, CodeQL, actionlint, zizmor, OSV und Secret-Scanning behalten ihre unabhängigen Kontrollen. Siehe [Tests und Evidence](../docs/testing-and-evidence.de.md) und [PR-#382-Status](../docs/pr-382-merge-readiness.de.md).

## Struktur und Source of Truth

| Pfadmuster | Zweck | Source of Truth / Ablageregel |
| --- | --- | --- |
| \`test_*.py\` | Root-Level-Python-Unit- und Contract-Tests | Jeder Test ist für seine explizite Assertion maßgeblich; Implementierung und Root-Makefile bleiben maßgeblich für Verhalten und Target-Wiring. |
| \`test_*lifecycle*.py\` | Lifecycle-Artefakt-/Profil-/Wiring-Checks | Auf Run-Metadaten und Contracts fokussieren, nicht auf fabrizierten Runtime-Erfolg. |
| \`test_*capabilit*.py\` und \`test_*evidence*.py\` | Capability-/Evidence-Grenzchecks | Schema- und Claim-Regeln prüfen; keine breitere Capability kodieren, als die aufgezeichnete Evidence trägt. |
| \`test_*path*.py\`, \`test_*cache*.py\` und \`test_*component*.py\` | Path-, Cache- und Component-Preparation-Contracts | Pfade portabel halten und die Sicherheitsgrenze testen, statt auf einen Entwickler-Workspace zu vertrauen. |

Das Framework-Submodule besitzt wiederverwendbare YAML-Cases, Normalizer und
Runner-Tests. Root-\`tests/\` besitzt nur Connector-Repository-Contracts. Das
Root-[Makefile](../Makefile) ist maßgeblich für Target-Namen; der aktuelle
[Testing-Guide](../docs/testing-and-evidence.de.md) erklärt die Testebenen.

## Tests hinzufügen oder ändern

Einen neuen Root-Contract-Test als \`tests/test_<area>.py\` ablegen. Dabei ist
\`<area>\` ein Dokumentationsplatzhalter: durch eine kurze kleingeschriebene
Kennung wie \`runtime_path_policy\` ersetzen; daraus wird die literale Datei
\`tests/test_runtime_path_policy.py\`. Niemals eine Datei namens
\`test_<area>.py\` anlegen.

Kern-Ergänzungen benötigen an der Grenze weiterhin einen benannten Ersatz. Explizite Offline-Ausnahmen benötigen eigene geprüfte quellgebundene Python-Selektoren und vollständig gezählte Varianten; die Nutzerausnahme ist kein ungezählter zweiter Katalog.

Ein neues automatisch ausgewähltes Verhalten benötigt eine stabile Fall-ID,
Anforderung, Profil und ausführbaren Selektor im Aktivinventar. An der Kerngrenze
müssen das ersetzte oder tatsächlich konsolidierte Verhalten und verlorene
Abdeckung benannt werden; eine neue Methode oder versteckte unabhängige
Szenarien in einer Schleife umgehen die Zählung nicht.

Fixtures eigenständig, portabel und secret-frei halten. Das kleinste
Root-Verhalten testen, das einen Contract schützt; wiederverwendbare
Katalog-Cases, Normalizer-Änderungen und Framework-Runner-Tests gehören nach
\`modules/ModSecurity-test-Framework/\`. Kein \`__pycache__/\`, keine generierten
Reports, echte Runtime-Ausgabe, Downloads, Build-Trees, Credentials oder
kopierte Evidence in dieses Verzeichnis committen.

## Variablen und Platzhalter

Das Root-Makefile besitzt die relevanten Werte. Zentrale Definitionen außerhalb
dieses lokalen Test-Scopes stehen in der [Variablen- und Platzhalterreferenz](../docs/reference/variables.de.md)
und im [Glossar](../docs/reference/glossary.de.md).

| Name | Lokale Bedeutung | Pflicht, Format und Beispiel |
| --- | --- | --- |
| \`PYTHON\` | Python-Executable für Make-Targets und Checks | Optional; das Root-Makefile nutzt bei Vorhandensein \`.venv/bin/python\`, sonst \`python3\`. Eine installierte Executable oder ein Executable-Pfad, kein Shell-Fragment verwenden. |
| \`PYTHONDONTWRITEBYTECODE\` | Steuert die Python-Bytecode-Erstellung während Checks | Optional; Repository-Default ist \`1\`. Für saubere Source-Tree-Checks bei \`1\` lassen, soweit eine Diagnose nicht ausdrücklich Bytecode benötigt. |
| \`BUILD_ROOT\` | Disposable Workspace für Checks mit Artefakten | Optional und vom Root abgeleitet. Ein Override muss ein absolutes beschreibbares Verzeichnis außerhalb des Checkouts sein, etwa \`/srv/modsecurity-work/build\`; kein Fixture-Verzeichnis. |
| \`FRAMEWORK_ROOT\` | Framework-Checkout für delegierte Root-Targets | Für delegierte Make-Targets erforderlich. Repository-Default ist \`modules/ModSecurity-test-Framework\`; ein Override muss einen vorhandenen vertrauenswürdigen Checkout benennen. |
| \`<repository-root>\` | Reiner Dokumentationsplatzhalter für den absoluten Root dieses Checkouts | Nur wenn ein Kommando ihn benötigt einen realen Pfad wie \`/srv/src/ModSecurity-conector\` verwenden. Winkelklammern nicht in Python oder Shell-Kommando kopieren. |

Keine Testvariable ist ein Secret. Niemals Tokens, Cookies,
Authorization-Header, private Schlüssel oder echte Kunden-Payloads in
Testname, Fixture, Kommandoargument oder erwartetes Artefakt aufnehmen.

## Relevante Kommandos und Targets

| Kommando oder Target | Zweck und Ergebnisgrenze |
| --- | --- |
| <code>make check-active-inventory</code> | Prüft das gesamte expandierte Inventar und gibt seine tatsächliche Fallzahl ohne Fallausführung aus. |
| <code>make test</code>, <code>make test-active</code> | Führt die vollständige zugelassene Auswahl mit nativen und Runtime-Voraussetzungen aus; kein leichter hostfreier Check. |
| <code>python3 ci/tools/run-active-tests.py --group inventory --output-root /srv/modsecurity-work/tests</code> | Führt eine zugelassene Gruppe mit dem kanonischen Projekt-Python aus; der bestehende Ausgabeparent muss vertrauenswürdig, eigen, kanonisch und extern sein. |
| <code>python3 -m unittest discover -v tests</code> | Führt über gemeinsame Discovery-Hooks nur zugelassene Python-Definitionen aus. Deckt keine Go-/Native-/Runtime-Auswahl ab und startet keinen Framework-Katalog. |
| <code>ON_DEMAND_TESTS=1 python3 -m unittest -v tests.test_runtime_path_policy</code> | Fordert ausdrücklich das erhaltene Spezialmodul an; seine breiteren Assertions liegen außerhalb der automatischen Auswahl und können separat beauftragte Wartung erfordern. |
| <code>make check-framework-fixture-syntax</code> | Statische Framework-Fixture-Syntax-/Vertragsprüfung, kein Runtime-Ergebnis. |
| <code>make check-test-matrix</code> | Prüft generierte Matrixkonsistenz und Zuständigkeit; die Matrixerzeugung führt ihre Fälle nicht aus. |
| <code>make quick-check</code>, <code>make lint</code> | Erhält statische, Konfigurations-, Dokumentations- und Governance-Checks; funktionale Teile wählen dasselbe Aktivinventar und erzeugen keine allgemeine Hostqualifikation. |
| <code>ON_DEMAND_TESTS=1 make check-native-engine-body-inspection</code> | Erhaltene vollständige native Limits-/Serialisierungs-/Phasensuite; benötigt echten C17-Compiler und ausgewähltes SDK. Ohne Flag wählt dieser Alias die aktive Common-Gruppe, nicht die komplette Spezialsuite. |
| <code>ON_DEMAND_TESTS=1 make check-native-lifecycle-observer</code> | Erhaltene vollständige GNU-Linker-Observer-Suite mit explizitem <code>NATIVE_OBSERVER_TEST_OUT</code>, <code>MODSECURITY_INCLUDE_DIR</code> und <code>MODSECURITY_LIB_DIR</code>. Ohne Flag wählt dieser Alias nach seinem bestehenden SDK-/Ausgabe-Preflight die aktive Common-Gruppe. |

Die native Suite auf Abruf akzeptiert die bestehende SDK-Auswahl über
`MODSECURITY_PREFIX`, `MODSECURITY_INCLUDE_DIR`, `MODSECURITY_LIB_FILE` und
`MODSECURITY_LIB_DIR`; ungültige explizite Pfade scheitern vor der Kompilierung.
Bei einer externen Bibliothek verwenden Executables deren Verzeichnis als
Runtime-Suchpfad. Inspection-Fixtures setzen native Limits/Aktionen ausdrücklich.
Verlustfreie Byte-Escapes müssen Phase und Eventintegrität erhalten;
Escape-Feldüberlauf darf weder schreiben noch die Hashkette fortsetzen.
Leichtgewichtige Eventprotokolltests behalten ihre getrennte Dependency-Grenze.

Der Lifecycle-Observer auf Abruf erfasst tatsächliche API-Eintritts-/Rückkehrpaare, getrennte
Host- und kanonische Transaktions-IDs, Common-Zustandsaufnahmen und finale Belege
pro Prozess. Er wird ausschließlich in Testartefakte mit den vierzehn `--wrap`-
Symbolen aus `tests/test_native_lifecycle_observer.py` gelinkt. Ein Supervisor
übergibt einen privaten geerbten Append-Deskriptor und erhält dessen originales
JSONL. Interne Aufrufe desselben Objekts können Wrapping umgehen; fehlende finale
Belege oder offene Zuordnungen lassen Cleanup unqualifiziert. Native MIME-Auswahl
und tatsächliches Host-EOS bleiben `null`. Erfolgreiche Komponententests oder
API-Zähler allein belegen keinen Host-Lifecycle-Abschluss.
Native Append-Belege enthalten tatsächliche Bytezahlen und NULL-/Nicht-NULL-
Eingabearten. Diese APIs haben kein EOS-Argument; leere Appends belegen kein
Host-EOS.

Der optionale Helper `ci/runtime/lifecycle/native-lifecycle-sdk.cpp` liest die
öffentliche Transaktions-ID des gewählten C++-SDK nach Ausschluss einer abweichenden
Runtime-Version. Vor dem Linken in ein Host-Testartefakt müssen exakte Header- und
Bibliothekshashes sowie beide echten Konstruktoren geprüft sein. Damit werden auch
anonyme native IDs erfasst; die übergebene Eingabe-ID bleibt getrennt, eine Common-/
Native-Korrelation wird nicht abgeleitet. Die Versionsprüfung allein qualifiziert
keinen beliebigen Build mit scheinbar passendem ABI. Ohne Helper bleibt das native
ABI für den Observer undurchsichtig. Abgewiesene oder überlange IDs machen die
Messung ungültig und erhalten den nativen Aufruf sowie errno.

Für Auswahl der Testebene und korrekte Ergebnisdarstellung [Testebenen](../docs/testing-and-evidence.de.md),
[Core-Lifecycle-Testing](../docs/testing-and-evidence.de.md) und den
[Evidence-Guide](../docs/testing-and-evidence.de.md) verwenden.
