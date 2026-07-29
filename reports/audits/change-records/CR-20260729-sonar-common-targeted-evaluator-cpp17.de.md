# Change Record: Parent-Common-Targeted-Evaluator-C++17-Remediation

**Sprache:** [English](CR-20260729-sonar-common-targeted-evaluator-cpp17.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260729-sonar-common-targeted-evaluator-cpp17 |
| Datum (UTC) | 2026-07-29 |
| Basis-Revision | `9f23ae2c5fe908cef38f203be03f93fda75a8dd7` |
| Tracking | 24 ursprünglich gemeldete SonarQube-Cloud-Code-Smells in `common/scripts/modsecurity_targeted_eval.cc`, einschließlich C++20-only-API-Empfehlungen, überschatteter Namen, Raw-String-Delimiter und kognitiver Komplexität. |
| Grenze | Parent-Common-Evaluator-Source und gepaarte Change Records. Keine Framework-, MRTS-, Gitlink-, Workflow-, Sonar-Konfigurations- oder Suppression-Änderung. |

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

`ArgumentMap` verwendet `std::less<>` und eine auf `lower_bound` basierende
Lookup-Hilfsfunktion. Dadurch werden C++20-only `contains` und wiederholte
Map-Membership-Tests vermieden. Die requestbezogene Logik ist in enge
Hilfsfunktionen aufgeteilt, deren Parameter die vorhandenen Ownership- und
Bereinigungsbeziehungen sichtbar machen. Die String-Suche nutzt die lokale
C++17-Hilfsfunktion `string_contains` und erhält die bisherige abgesicherte
Teilstring-Bedingung. `main` behält die bisherige Ressourcen-Lebensdauer und
Bereinigungsreihenfolge bei.

## Geänderte Dateien

- `common/scripts/modsecurity_targeted_eval.cc` — C++17-kompatibler Options-
  Lookup und Aufteilung von Evaluator-Setup, Ausführung, Ergebnis-Logging und
  Success-JSON-Rendering.
- Dieses englisch/deutsche Change-Record-Paar und seine gepaarten Indizes.

## Ausgeführte Befehle

| Ausgeführte Kontrolle | Beobachtetes Ergebnis |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_c_cpp_diagnostics` | bestanden; 7 Tests bestanden mit Python 3.14.4 (Repository-Pin ist 3.14.6). |
| `make check-targeted-evaluator-cpp17` mit GCC 15 und task-eigenen externen Libmodsecurity-Include-/Build-Pfaden | bestanden gegen reale Libmodsecurity 3.0.14. |
| `make check-targeted-evaluator-cpp17` mit Clang 21 und derselben realen Libmodsecurity-Schnittstelle | bestanden. |
| Reale Evaluator-Runtime-Kontrollen | bestanden: Phase-1-Targeted-Header-Block (403), legitimes Header-Allow (200) und Phase-2-Request-Body-Block (403). |
| Parser-Negativkontrollen | bestanden: fehlende Rule, nicht unterstütztes Ruleset und hängendes `--rule-file` lieferten jeweils den erwarteten strukturierten Fehler. |
| `git diff --check` | bestanden. |
| Fokussierte Bilingual-Documentation-Suite | bestanden; 21 Tests bestanden. |
| Breiter Repository-Dokumentationschecker | durch fehlende Framework-Submodule-Linkziele im isolierten Parent-Worktree blockiert; er wird nicht als bestanden ausgegeben. |
| Fokussierter Codex-Security-Diff-Scan | bestanden mit null reportbaren Befunden für den synchronisierten Kandidaten; versiegelte Scan-ID: `67fe74f1f0cf8d21c820e330fae31433ab68ebf4_20260729T155321Z`. |

## Security-Auswirkung

Dieser Evaluator bildet vom Operator gewählte Command-Line-Werte auf eine
ModSecurity-Transaction und Ergebnis-Evidence ab. Die Änderung erweitert weder
akzeptierte Optionen noch lockert sie Validierung, Rule-File-Verarbeitung,
HTTP-Request-/Body-Mapping oder Intervention-/Resource-Cleanup. Die fokussierte
Exact-Head-Prüfung fand keine neu erreichbare Security-Regression. Reale
Libmodsecurity-Kontrollen bestätigen das erwartete Header-/Body-Blocking und
legitime Allow-Verhalten; sie ersetzen nicht die erforderlichen
Exact-Head-Hosted-Delivery-Gates.

## Runtime-Evidence

Die task-eigene externe Testumgebung linkt und führt den Evaluator gegen reale
Libmodsecurity 3.0.14 aus. GCC 15 und Clang 21 bestehen beide den nativen
C++17-Target; direkte Phase-1-Header-, Phase-2-Body-, legitime-Allow- und
Parser-Negativkontrollen liefern lokale Enforcement-Evidenz.

## Bekannte Einschränkungen

- Die direkte Diagnostics-Suite nutzte Python 3.14.4, während
  `.python-version` 3.14.6 vorgibt.
- Der breite Repository-Dokumentationschecker ist durch fehlende
  Framework-Submodule-Linkziele im isolierten Parent-Worktree blockiert.
- Hosted-CI und eine frische Exact-Head-SonarQube-Cloud-Analyse für den finalen
  Delivery-Kandidaten stehen aus.

## Nicht ausgeführte Prüfungen mit Begründung

Der breite Repository-Dokumentationschecker kann in diesem isolierten
Parent-Worktree nicht vollständig laufen, weil seine Framework-Submodule-
Linkziele fehlen. Der finale Delivery-Kandidat hat noch keine Hosted-CI- oder
SonarQube-Cloud-Analyse erhalten; diese Exact-Head-Gates bleiben vor der
Integration erforderlich.

## Verbleibende Risiken

Künftige Änderungen müssen die C++17-Kompilierung und die explizite
Bereinigungsreihenfolge für Transaction, Rules und ModSecurity-Instanzen
erhalten. Jede neue Option, die einen Rule-Pfad, Request-Daten oder Audit-Output
beeinflusst, benötigt eine eigene Input-Boundary-Prüfung.

## Finaler Diff- und Review-Status

Der Kandidat ist auf Parent-Common-Evaluator-Source und bilinguale Traceability
begrenzt. Lokale C++17-, Runtime-, Contract-, Whitespace- und fokussierte
Security-Evidence sind unter den festgehaltenen Einschränkungen vollständig;
Exact-Head-Hosted-Verifikation bleibt vor jeder Delivery- oder Merge-
Behauptung erforderlich.
