# Change Record: Parent-Common-Targeted-Evaluator-C++17-Remediation

**Sprache:** [English](CR-20260729-sonar-common-targeted-evaluator-cpp17.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260729-sonar-common-targeted-evaluator-cpp17 |
| Datum (UTC) | 2026-07-29 |
| Basis-Revision | `fd0b2f4bdd3ca42b496deae85fcd1d2aee6adc1c` |
| Tracking | 24 aktuelle SonarQube-Cloud-Code-Smells in `common/scripts/modsecurity_targeted_eval.cc`, einschließlich C++20-only-API-Empfehlungen, überschatteter Namen, Raw-String-Delimiter und kognitiver Komplexität. |
| Grenze | Parent-Common-Evaluator-Source und gepaarte Change Records. Keine Framework-, MRTS-, Gitlink-, Workflow-, Sonar-Konfigurations-, Suppression- oder `master`-Änderung. |

## Motivation und Problemstellung

Der Targeted Evaluator wird bewusst als C++17 kompiliert. Seine Argument-
Verarbeitung, Request-Konstruktion, ModSecurity-Auswertung, Intervention-
Bereinigung und JSON-Ausgabe hatten einen großen Kontrollflusskörper sowie
Empfehlungen für unter C++17 nicht verfügbare APIs angesammelt. Die Behebung
muss die gemeldeten Source-Befunde reduzieren, ohne CLI-Semantik, Ownership der
ModSecurity-Objekte, Response-Auswahl oder Bereinigungsreihenfolge zu ändern.

## Akzeptanzkriterien

- Der Evaluator bleibt C++17-kompatibel; keine C++20-Container- oder String-
  Membership-API wird eingeführt.
- Bestehende CLI-Optionswerte, CRS-Auswahl, Request-Mapping, JSON-Felder,
  Interventionsstatus und Bereinigungsreihenfolge bleiben erhalten.
- Die Implementierung trennt Optionsverarbeitung, Request-Setup,
  Transaction-Auswertung, Decision-Log-Konstruktion und Success-JSON-Rendering
  in kleine benannte Einheiten.
- Hosted-Checks und eine frische Exact-Head-SonarQube-Cloud-Analyse müssen vor
  jeder Integrationsbehauptung weiterhin null New Issues und null New-Code-
  Duplikatzeilen beweisen.

## Implementierungsentscheidung und Begründung

`ArgumentMap` verwendet einen transparenten Comparator und eine auf
`lower_bound` basierende Lookup-Hilfsfunktion. Dadurch werden C++20-only
`contains` und wiederholte Map-Membership-Tests vermieden. Die requestbezogene
Logik ist in enge Hilfsfunktionen aufgeteilt, deren Parameter die vorhandenen
Ownership- und Bereinigungsbeziehungen sichtbar machen. Die String-Suche nutzt
`std::search`, das unter C++17 verfügbar ist. `main` behält die bisherige
Ressourcen-Lebensdauer und Bereinigungsreihenfolge bei.

## Geänderte Dateien

- `common/scripts/modsecurity_targeted_eval.cc` — C++17-kompatibler Options-
  Lookup und Aufteilung von Evaluator-Setup, Ausführung, Ergebnis-Logging und
  Success-JSON-Rendering.
- Dieses englisch/deutsche Change-Record-Paar und seine gepaarten Indizes.

## Ausgeführte Befehle

| Ausgeführte Kontrolle | Beobachtetes Ergebnis |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest -v tests.test_c_cpp_diagnostics` | bestanden; 7 Tests bestanden. |
| `g++ -std=c++17 -Wall -Wextra -Werror -fsyntax-only` mit einem task-eigenen externen Libmodsecurity-Interface-Stub | bestanden. |
| `clang++ -std=c++17 -Wall -Wextra -Werror -fsyntax-only` mit demselben Stub | bestanden. |
| C++17-Stub-backed-Link- und Evaluator-Kontrollen | bestanden; sowohl der CRS-Ergebnisvertrag als auch der Fehlervertrag für fehlendes `--rule-file` wurden ausgeführt. |
| `make check-targeted-evaluator-cpp17` | durch die Umgebung blockiert: `MODSECURITY_INCLUDE_DIR` sowie reale Libmodsecurity-Entwicklungsheader/-Library fehlen (Target beendet sich mit 77). |
| `git diff --check` | bestanden. |
| Lokale Follow-up-Controls | bestanden: 28 C/C++-Diagnose- und Bilingual-Documentation-Tests, C++17-`g++`-/`clang++`-Checks mit `-Werror` sowie Stub-backed-CRS-, Missing-Rule-File-, Request-Body-Marker-Present- und Request-Body-Marker-Absent-Controls. |
| Fokussierter Codex-Security-Diff-Scan | bestanden mit null reportbaren Befunden; versiegelter Report: `/var/tmp/codex/ModSecurity-conector/runs/20260729-complete-common-connectors-sonar-remediation/security-scans/fc6027681cfae342dcef8e1606a38523c450044c_20260729T084000Z/report.md`. |

## Security-Auswirkung

Dieser Evaluator bildet vom Operator gewählte Command-Line-Werte auf eine
ModSecurity-Transaction und Ergebnis-Evidence ab. Die Änderung erweitert weder
akzeptierte Optionen noch lockert sie Validierung, Rule-File-Verarbeitung,
HTTP-Request-/Body-Mapping oder Intervention-/Resource-Cleanup. Die fokussierte
Diff-Prüfung fand keine neu erreichbare Security-Regression. Die reale externe
Libmodsecurity-Runtime bleibt eine explizit fehlende Abhängigkeit und wird nicht
durch eine Sicherheitsbehauptung ersetzt.

## Runtime-Evidence

Der task-eigene Stub ermöglicht lokale C++17-Syntax-, Link-, erfolgreiches
CRS-Result- und Invalid-Option-Kontrollen. Er ist keine Libmodsecurity-Runtime
und keine Enforcement-Assertion. Ein repository-nativer Link-/Runtime-Check
ist wegen fehlender externer Entwicklungsartefakte blockiert.

## Bekannte Einschränkungen

- Die lokale Umgebung hat keine realen Libmodsecurity-Header oder -Library;
  daher wurde der Evaluator nicht gegen diese Abhängigkeit gelinkt oder
  ausgeführt.
- Hosted-CI und eine frische Exact-Head-SonarQube-Cloud-Analyse stehen aus.

## Nicht ausgeführte Prüfungen mit Begründung

Der native Link-/Runtime-Control `make check-targeted-evaluator-cpp17` wurde
nicht erfolgreich ausgeführt, weil diese Umgebung weder die externen
Libmodsecurity-Entwicklungsheader noch die Library oder den erforderlichen
Include-Pfad bereitstellt. Der task-eigene C++17-Stub validiert nur Syntax und
ausgewählte Evaluator-Contracts; er ersetzt kein reales Libmodsecurity-Runtime-
Ergebnis.

## Verbleibende Risiken

Künftige Änderungen müssen die C++17-Kompilierung und die explizite
Bereinigungsreihenfolge für Transaction, Rules und ModSecurity-Instanzen
erhalten. Jede neue Option, die einen Rule-Pfad, Request-Daten oder Audit-Output
beeinflusst, benötigt eine eigene Input-Boundary-Prüfung.

## Finaler Diff- und Review-Status

Der Kandidat ist auf Parent-Common-Evaluator-Source und bilinguale Traceability
begrenzt. Lokale C++17-, Contract-, Whitespace- und fokussierte Security-
Evidence sind vollständig; ein separater Draft-PR und Exact-Head-Hosted-
Verifikation sind vor jeder Delivery- oder Merge-Behauptung weiterhin nötig.
