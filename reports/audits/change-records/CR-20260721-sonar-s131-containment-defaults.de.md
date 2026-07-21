# Change Record: Explizite Parent-Analyse-Output-Containment-Defaults für SonarQube Cloud S131

**Sprache:** [English](CR-20260721-sonar-s131-containment-defaults.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260721-sonar-s131-containment-defaults |
| Datum (UTC) | 2026-07-21 |
| Basis-Revision | 2ade0d40983b7af21a65b8cd2884866b85626393 |
| Tracking | Fünf Parent-only-shelldre:S131-Code-Smells: AZ9dWh6Oxi9ITghe3pzl, AZ9dWh6Oxi9ITghe3pzm, AZ9dWiAVxi9ITghe3pzr, AZ9dWiAVxi9ITghe3pzs und AZ9dWiAAxi9ITghe3pzn. |
| Grenze | Nur Parent-C/C++-Analyse-Output-Guards und ihr fokussierter Python-Contract; Framework, MRTS, Gitlinks, Connector-Runtime, Scanner-Konfiguration und Quality Gates bleiben unverändert. |

## Motivation und Problemstellung

Fünf negative Checkout-Output-Containment-Cases verließen sich absichtlich auf
unmatched case fall-through, wenn ein normalisierter Pfad außerhalb des
Checkouts lag. SonarQube-Cloud-Regel shelldre:S131 meldet diese fehlenden
Default-Arme. Das vorhandene Reject-Verhalten ist eine Output-Containment-
Kontrolle und muss für Checkout-Root- und Checkout-Descendant-Pfade fail-closed
bleiben.

## Akzeptanzkriterien

- Jede vorhandene Checkout-Root-/Checkout-Descendant-Rejection-Message, jeder
  Exit-Status, jeder Normalisierungsschritt und die Reihenfolge der
  Directory-Erzeugung bleiben unverändert.
- Nur der bereits erlaubte externe Pfad wird mit dem POSIX-no-op-Default-Arm
  explizit: *) : ;;.
- Ein fokussierter Control beweist, dass externe Outputs bis zum nächsten
  Missing-Tool-Dependency-Gate fortsetzen, während Checkout-Outputs weiterhin
  vor jeder Directory-Erzeugung abgelehnt werden.
- Bevor behauptet wird, dass die fünf ursprünglichen Keys behoben sind, wird
  eine frische SonarQube-Cloud-Analyse für den exakten Draft-PR-Head eingeholt.

## Implementierungsentscheidung und Begründung

Jeder ausgewählte Case behält seinen vorhandenen Matching-Arm bei, der für einen
Output innerhalb des Checkouts mit Status 2 endet. Der ergänzte Default-Arm ruft
den POSIX-colon-no-op auf und fällt anschließend zur unveränderten nächsten
Instruktion durch. Dies entspricht dem bisherigen unmatched-case-Verhalten,
macht aber die erlaubte Fortsetzung für den Shell-Analyzer sichtbar.

Der fokussierte Python-Contract verwendet für einen externen Output-Request
absichtlich einen nicht vorhandenen Compiler-Namen. Er beweist, dass jedes
Skript seine Containment-Prüfung passiert, nur seinen angeforderten externen
Pfad erzeugt und das nächste dokumentierte Dependency-Gate mit Status 77
erreicht. Der vorhandene Rejection-Contract prüft weiterhin Status 2, die
Containment-Message und keine Checkout-lokale Directory-Erzeugung.

## Security-Auswirkung

Dies ist eine Maintainability-Remediation um sicherheitsrelevante
Output-Containment-Checks. Sie erweitert keine akzeptierte Pfadmenge: Ein
normalisierter Checkout-Pfad endet weiterhin vor mkdir, während ein bereits
externer Pfad weiterläuft. Sie fügt keine Suppression, Regel-Deaktivierung,
Quality-Gate-Änderung, NOSONAR-Markierung, Authentifizierungsänderung,
Autorisierungsänderung, Runtime-Protokollverhalten oder Framework-/MRTS-Änderung
hinzu.

## Geänderte Dateien

- ci/checks/analysis/compile-db-cpp17.sh
- ci/checks/analysis/compile-db-nginx-c17.sh
- ci/checks/analysis/check-targeted-evaluator-cpp17.sh
- tests/test_c_cpp_diagnostics.py
- reports/audits/change-records/README.md und README.de.md
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| rtk proxy sh -n ci/checks/analysis/compile-db-cpp17.sh | bestanden. |
| rtk proxy sh -n ci/checks/analysis/compile-db-nginx-c17.sh | bestanden. |
| rtk proxy sh -n ci/checks/analysis/check-targeted-evaluator-cpp17.sh | bestanden. |
| rtk proxy env TMPDIR=<task-owned external path> PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 python3 -m unittest -v tests.test_c_cpp_diagnostics | bestanden: 6 Tests, einschließlich Checkout-Rejection- und External-Output-Continuation-Controls. |
| rtk proxy git diff --check | nach der Source- und Contract-Änderung bestanden. |

## Runtime-Evidence

Es ändert sich kein Connector-Runtime-Verhalten. Der fokussierte Contract ruft
nur die drei lokalen Analyse-Skripte mit einem absichtlich fehlenden Compiler
nach ihren Output-Containment-Checks auf. Er führt keinen Compilation-Database-
Build aus, linkt kein libmodsecurity und startet keinen Connector.

## Exact-PR-Head-Delivery-Evidence

Ein Draft-PR sowie Exact-Head-GitHub-Actions-/SonarQube-Cloud-Evidence sind nach
dem normalen Source-Commit und Push erforderlich. Dieser Record behauptet diese
zukünftigen Ergebnisse nicht. Die finale PR-Beschreibung und vorgehaltene
Task-Evidence werden tatsächlichen finalen SHA und Exact-Hosted-Ergebnisse ohne
selbstreferenziellen Commit-Loop benennen.

## Nicht ausgeführte Prüfungen mit Begründung

- make compile-db-cpp17 und make compile-db-nginx-c17 wurden nicht ausgeführt:
  Sie benötigen Bear sowie vollständige C++-/NGINX- und libmodsecurity-
  Build-Voraussetzungen, während der fokussierte Test die ausgewählten
  Default-Arme beweist, ohne einen nicht verfügbaren Produkt-Build als bestanden
  darzustellen.
- check-targeted-evaluator-cpp17 mit einem realen Compiler wurde nicht
  ausgeführt: Es benötigt verwendbares MODSECURITY_INCLUDE_DIR und
  MODSECURITY_LIB_DIR. Der fokussierte External-Control erreicht stattdessen
  sein dokumentiertes Missing-Compiler-Gate.
- Der vollständige Repository-Bilingual-Checker wird im isolierten Parent-
  Worktree voraussichtlich durch nicht ausgefüllte Framework-Linkziele
  environment-blocked sein; der fokussierte bilinguale Dokumentationstest und
  die exakte PR-CI bleiben die verfügbaren Controls.

## Bekannte Einschränkungen

Die lokale Validierung beweist die fünf Shell-Arme und ihr unmittelbares
Containment-/Dependency-Verhalten, nicht eine vollständige Compilation Database
oder Connector-Runtime. Hosted Exact-Head-SonarQube-Cloud-Evidence bleibt
erforderlich.

## Verbleibende Risiken

Andere shelldre:S131-Beobachtungen haben unterschiedliche Policies für
unbekannte Werte und werden absichtlich nicht hier gruppiert. Der breitere
Parent-SonarQube-Cloud-Vulnerability- und Maintainability-Backlog bleibt
getrennt getrackt. Dieser Record autorisiert keinen Merge.

## Finaler Diff- und Review-Status

Der beabsichtigte Diff besteht aus fünf expliziten no-op-Default-Armen, einem
fokussierten Contract-Test und diesem Traceability-Paar/Index. Bevor ein
Draft-PR als verifiziert gilt, müssen finaler Diff, exakte lokale/Remote/PR-SHA-
Gleichheit, GitHub Actions, SonarQube-Cloud-Quality-Gate, Five-Key-Issue-Query
und Review-Status für den aktuellen Head erneut geprüft werden.
