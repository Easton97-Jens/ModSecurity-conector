# Repository-Contract-Tests

**Sprache:** [English](README.md) | Deutsch

## Zweck und Grenze

\`tests/\` enthält fokussierte Python-Tests für Root-Orchestrierung,
Konfiguration, Artefakt-Layout, Lifecycle-Wiring, Capability-Grenzen und
Path-/Security-Contracts. Sie liefern schnelle Regression-Coverage für
Repository-Verhalten, das ohne die Darstellung eines synthetischen Host-Laufs
als Evidence geprüft werden kann.

Diese Tests sind weder der Framework-Case-Katalog noch Ersatz für
Connector-Harnesses oder kanonische Runtime-Evidence. Bestandene Unit-Tests
belegen keine Production Readiness, CRS-Vollständigkeit, HTTP/2-/HTTP/3-
Verifikation, vollständige Matrix oder Strict-Verifikation für alle Connectoren.

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
| \`.venv/bin/python -m unittest -v tests.test_runtime_path_policy\` | Führt ein fokussiertes Testmodul aus, wenn \`.venv/bin/python\` vorhanden ist. Das Modul-Suffix durch einen literalen eingecheckten Testnamen ersetzen; Unit-Coverage, keine Host-Evidence. |
| \`python3 -m unittest discover -v tests\` | Findet Root-Python-Tests mit dem System-Python, wenn er die Projektabhängigkeiten erfüllt. Führt nicht die Framework-Suite aus. |
| \`make check-framework-fixture-syntax\` | Validiert Framework-Fixture-Syntax über das Root-Target; ein Syntax-/Contract-Check, kein Runtime-Ergebnis. |
| \`make check-test-matrix\` | Prüft Konsistenz und Ownership-Grenzen der generierten Test-Matrix. |
| \`make quick-check\` | Führt die fokussierten schnellen Repository-Contract-Checks aus. Erzeugt keine kanonische Runtime-Evidence. |
| \`make lint\` | Führt breite Syntax-, Contract-, Dokumentations- und Governance-Checks aus, einschließlich Root-Test-bezogener Contracts. |

Für Auswahl der Testebene und korrekte Ergebnisdarstellung [Testebenen](../docs/testing-and-evidence.de.md),
[Core-Lifecycle-Testing](../docs/testing-and-evidence.de.md) und den
[Evidence-Guide](../docs/testing-and-evidence.de.md) verwenden.
