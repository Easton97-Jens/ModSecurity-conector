# Change Record: CR-20261009-nginx-input-fault-inherited-fd-20261009

**Sprache:** [English](CR-20261009-nginx-input-fault-inherited-fd-20261009.md) | Deutsch

Begrenzter isolierter Patch; keine native Runtime- oder Scanner-Closure-Evidence.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261009-nginx-input-fault-inherited-fd-20261009 |
| Datum (UTC) | 2026-10-09 |
| Basis-Revision | `f63996290925f4b0c04d286506171825de9dc2ff` |

## Motivation und Problemstellung

Der Driver erzeugte und schloss ein privates Ledger, bevor die C-Fixture einen Umgebungs-Pfad erneut öffnete. Leaf-O_NOFOLLOW plus lexikalisches Präfix band nicht an das erzeugte Inode; Traversal/intermediäre Symlinks und mehrere Links waren nicht ausgeschlossen. Gewöhnliche unprivilegierte Erreichbarkeit durch den validierten0700-Workflow ist unbelegt.

## Akzeptanzkriterien

Nur einen echten geerbten schreibbaren FD>=3 für ein root-owned0600 leeres reguläres Single-Link-Inode verwenden. Own-Worker-UID/PPID, exakte Transaction/URI/POST, einmaligen Trigger und tatsächlichen Common-Validator-Return erhalten. Legacy-Pfade niemals erneut öffnen.

## Implementierungsentscheidung und Begründung

MSCONNECTOR_OWNED_INPUT_FD mit striktem bounded Decimal-Parsing, F_GETFL und fstat-Prüfungen verwenden. Descriptor-Lifetime gehört dem koordinierten Driver. ID-Parameter und Callback-Typedef an const char * des ausgewählten Engine-Headers angleichen; C17-Generic-Static-Assertions prüfen Callback-/Export-Kompatibilität ohne Casts.

## Geänderte Dateien

`tests/fixtures/nginx_common_input_fault.c`, `tests/fixtures/nginx_common_input_fault_scope.c`, `tests/test_nginx_common_input_fault_scope.py` und dieses EN/DE-Paar. Driver-Integration ist separat owned.

## Ausgeführte Befehle

Abschließende Zusatzprüfungen:alle sieben betroffenen C-Fixtures/Cleanup-Dateien C17-Syntax Exit0; drei geänderte Python-Dateien py_compile Exit0; `tests.test_change_record` und `tests.test_prepare_reviewed_framework_handoff`:39 Tests, Exit0; Record-Archiv-Check Exit0; Pfad-/Linkdiagnostik für die vier neuen Records:0 Fehler. `make check-bilingual-docs` und `make check-doc-links` scheiterten an bestehenden Submodule-Links, da das Framework-Verzeichnis im isolierten Worktree nicht befüllt ist. Der explizite externe FRAMEWORK_ROOT ersetzt diese relativen Links nicht. Keine fehlende Dependency wurde verändert oder eine Prüfung gelockert.

RTK-wrapped FD-only Legitimate-Kontrolle am ursprünglichen Konstruktor:zwei Fehler (tatsächlich1 1 statt0 1). Nach Migration:sieben Scope-Tests, Exit0; finaler kombinierter Lauf mit sieben Suites:34 Tests, Exit0. Negative prüfen malformed/invalid FD, read-only, Hardlink, nonregular, nonempty, falschen Modus/Owner und Legacy-Pfad. Rename/Replacement plus Legacy-Symlink-Alias schreibt ausschließlich ins ursprüngliche retained Inode.

## Security-Auswirkung

Schließt die Create-Close-Reopen-Grenze der Fixture durch Entfernen der C-Pfadauflösung. Unabhängige Pre-Patch-Prüfung bestätigte die Lücke, belegte jedoch keine gewöhnliche Angreifer-Erreichbarkeit oder HTTP/RCE-Ausnutzung. Tatsächliche Private-Inode-Prüfungen und Prozess-/Transaction-Scope bleiben verpflichtend.

## Runtime-Evidence

Keine. Worker-Rollen und Foreign-Owner-Metadaten sind kontrollierte C17-Inputs; tatsächliche Common-Validierung ist gelinkt. Das Dateisystem wies eine versuchte chown-Kontrolle mit EINVAL ab; Owner-Ablehnung verwendet daher ein ausdrücklich kontrolliertes fstat-Owner-Feld.

## Bekannte Einschränkungen

Python-Driver-Migration und kombinierte unabhängige Candidate-Prüfung sind getrennte Ownership-Grenzen. Keine integrierte native Evidence oder Sonar-Closure wird behauptet.

## Verbleibende Risiken

Ein veraltetes oder ungültiges Original-Receipt wird durch diese Tests nicht repariert. Frische Driver-/Fixture-Integration, strikte Source-Capture und echter nativer Neulauf bleiben erforderlich.

## Nicht ausgeführte Prüfungen mit Begründung

Native Build/Runtime, frische Scanner-Closure und koordinierte Driver-Integration wurden von diesem Worker nicht ausgeführt.

## Finaler Diff- und Review-Status

RED-to-GREEN-Kontrollen und Inode-Alias-Prüfungen bestanden. Keine Git-Schreiboperation oder Shared-Root-Source-Änderung erfolgte. Die separate unabhängige Candidate-Prüfung steht beim Koordinator noch aus.
