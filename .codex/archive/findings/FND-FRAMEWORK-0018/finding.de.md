# FND-FRAMEWORK-0018 — CRS-Testleitfaden widerspricht der fail-closed-Provenance-Kontrolle für vorhandene Checkouts

## Klassifizierung

| Feld | Wert |
| --- | --- |
| Kategorie | documentation_drift |
| Repository / Ownership | Framework / framework |
| Priorität / Schweregrad | P2 / low |
| Konfidenz / Status | validated / verified |
| Release-Blocker | nein |
| Sicherheitsrelevant | ja |
| Machbarkeit | feasible_now |

## Zusammenfassung

## Aktuelle Master-Verifikation vom 2026-07-26

Framework-master `47e50e7bc43ba7a3b5bad1a9448111794f664cc0` bestand
`make test-crs-provenance-contract` und `make check-documentation`. Die
Leitfäden und Variablen drücken jetzt denselben fail-closed-Contract aus:
`CRS_SOURCE_DIR` muss frisch und fehlend sein; vorhandene Verzeichnisse und
Symlinks werden vor Git abgewiesen. Die Exact-Head- und Resulting-Master-
Hosted-Checks von PR #26 wurden erfolgreich beobachtet. Die spätere historische
Formulierung wird durch diese verifizierte Disposition abgelöst.

Die englischen und deutschen CRS-Testleitfäden sagen, dass der geprüfte
vollständige Commit für vorhandene Checkouts funktioniert. Die exakte
Framework-Provenance-Implementierung verlangt dagegen ein fehlendes
CRS_SOURCE_DIR und weist ein bereits vorhandenes Verzeichnis oder einen Symlink
vor jeder Git-Invocation ab. Dies ist eine validierte leserorientierte
Dokumentationsabweichung mit Sicherheitsrelevanz, aber kein nachgewiesener
Runtime-Provenance-Bypass.

## Beobachtetes und erwartetes Verhalten

Sowohl docs/testing-and-evidence.md:99-108 als auch
docs/testing-and-evidence.de.md:103-114 beschreiben Unterstützung für
vorhandene Checkouts. Die Variablenreferenzen unter
docs/reference/variables.md:167-173 und
docs/reference/variables.de.md:171-179 verlangen einen fehlenden Source-Pfad
und eine fail-closed-Abweisung vorhandener Verzeichnisse oder Links. Der exakte
Regressionstest unter tests/security_regression/test_crs_git_ref_provenance.py:247-251
erstellt einen vorhandenen Checkout mit einem nicht vertrauenswürdigen Sentinel
und fordert Exit 77, keine Git-Invocation und die Erhaltung des Sentinels.

Jede leserorientierte Anleitung muss stattdessen festhalten, dass nur ein
frisches, fehlendes Source-Verzeichnis akzeptiert wird; vorhandene Verzeichnisse
und Symlinks werden abgewiesen und dürfen nicht wiederverwendet werden.

## Auswirkung, Voraussetzungen und Reproduktion

Ein Operator oder eine Automatisierung, der bzw. die dem Testleitfaden folgt,
kann ein vorhandenes CRS_SOURCE_DIR mit veralteten oder angreifergesteuerten
Inhalten bereitstellen. Das Ergebnis ist fehlgeschlagenes Provisioning und kann
unsichere manuelle Umgehungen begünstigen. Die statische Evidenz zeigt keinen
Code-Level-Provenance-Bypass, weil die Implementierung den Pfad abweist.

Zur Reproduktion den PR-#26-Exact-Head
63c42e97b86acbae1374efa9f1c4209ce2ce673b gegen Framework-Master
9954b99a31fab0006cdf903ab477c8158c50fea8 prüfen und die zitierten Test-,
Variablenreferenz- und Testing-Guide-Zeilen vergleichen.

## Evidenz

| Run-ID | Artefakt | SHA-256 | Befehl / Ergebnis |
| --- | --- | --- | --- |
| 20260719T081017Z-framework-pr-resolution-20260719-840082e0 | /var/tmp/codex/ModSecurity-conector/runs/20260719T081017Z-framework-pr-resolution-20260719-840082e0/analysis/security-diff-pr26/artifacts/05_findings/FND-FRAMEWORK-0018-evidence.md | 2b363eb35e8ada3bd9302bbc356159fe9d15ff3b17269e2baafda0a4a14403e8 | rtk git diff --check origin/master...HEAD und RTK-präfixierte gezielte Reads endeten mit 0 und reproduzierten den widersprüchlichen Vertrag. |

Der Review war statisch und read-only. Es wurden keine Tests, Builds,
Netzwerkoperationen, Git-/GitHub-Writes, Parent-Änderungen oder MRTS-Operationen
ausgeführt.

## Grundursache und Behebung

Die überarbeiteten Testing-Leitfäden behielten eine unzutreffende Aussage zu
vorhandenen Checkouts bei, obwohl die Provenance-Implementierung bewusst auf
die Abweisung bereits vorhandener Source-Pfade geändert wurde. Diese Aussage in
beiden Leitfäden durch den exakten Frischverzeichnis-fail-closed-Vertrag
ersetzen, die technische Englisch-/Deutsch-Parität erhalten und danach den
fokussierten Provenance-Regressionstest sowie die relevanten
Dokumentationsprüfungen auf dem abgeglichenen Exact Head erneut ausführen.

## Akzeptanz und Validierung

- Beide Testing-Leitfäden halten fest, dass CRS_SOURCE_DIR fehlen/frisch sein
  muss und dass vorhandene Verzeichnisse oder Symlinks abgewiesen werden.
- Die englische und deutsche Aussage sind technisch gleichwertig.
- tests/security_regression/test_crs_git_ref_provenance.py behält den
  fail-closed-Fall für vorhandene Checkouts und eine legitime
  Frisch-Checkout-Kontrolle.
- Der fokussierte Provenance-Target sowie die relevanten Dokumentations- und
  Bilingual-Checks bestehen auf dem abgeglichenen Exact PR Head.

## Abhängigkeiten, verwandte Findings und Restrisiko

Die Korrektur gehört zur Exact-Head-Reconciliation von PR #26. Sie hat keinen
aktuellen technischen Blocker. Verwandtes Finding: FND-FRAMEWORK-0004.

Die Implementierung schlägt aktuell fail-closed fehl, aber die irreführende
Anleitung kann bis zur Korrektur der Dokumentation weiterhin Betriebsfehler
oder unsichere manuelle Wiederverwendungsversuche auslösen.

## Historie

- 2026-07-19T10:29:22Z — Ein read-only Exact-Diff-Sicherheitsreview
  validierte den Widerspruch zwischen beiden Testing-Leitfäden und dem
  getesteten Implementierungsvertrag.
