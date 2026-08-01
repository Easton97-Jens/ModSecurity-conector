# FND-PARENT-0047 — Go-CodeQL-Versions-Contract-Checker erlaubte YAML-äquivalente Literal-Selektoren

Kategorie: security_hardening\
Repository / Ownership: parent / parent\
Priorität / Severity / Confidence: P2 / low / reproduced\
Status: closed\
Release-Blocker: false\
Sicherheitsrelevant: true\
Protokoll: GitHub-Actions-CodeQL-Go-Toolchain-Selection-Contract\
Delivery-Status: verified_exact_head_ci_and_sonarqube_cloud_passed

## Zusammenfassung

Der statische Go-Versionsvertrag ist ein Defense-in-Depth-Admission-Control für
nicht vertrauenswürdige Pull-Request-Workflow-Änderungen. Seine früheren
partiellen Zeilenprüfungen akzeptierten ein with-Mapping, das
go-version-file: .go-version behielt, aber einen YAML-äquivalenten
Literal-go-version-Selector hinzufügte. Der immutable actions/setup-go-v7-Source
warnt bei beiden Inputs und löst Literal-go-version vor go-version-file auf;
dadurch konnte die zentrale Autorität umgangen werden, während der Checker
Erfolg meldete.

Die Bedingung hat niedrige Auswirkung, weil eine Workflow-Änderung weiterhin
den Repository-Pull-Request-/Review-Pfad benötigt. Sie ist dennoch ein
reproduzierbares gebrochenes CodeQL-Workflow-Control und task-owned von PR #90,
obwohl sie dem lokalen Sonar-Remediation-Follow-up von
d99eafd76d9fdbef5b63a19d084fd2d7caff6c08 vorausgeht.

## Betroffene Dateien, Voraussetzungen und Reproduktion

Betroffene Dateien sind ci/checks/common/check-go-version-contract.py und
tests/test_go_version_contract.py. Der Entry Point sind die actions/setup-go-
Steps envoy-go und traefik-go des Parent-CodeQL-Workflows.

Ein vorgeschlagener Workflow muss den statischen Contract-Checker erreichen und
sowohl den Central-File-Input als auch einen semantisch äquivalenten Literal-Key
enthalten. Vor der Remediation lieferte jede dieser Varianten eine leere
Verletzungsliste:

- go-version : '1.26.5'
- 'go-version': '1.26.5'
- "go-version": "1.26.5"
- ? go-version gefolgt von : '1.26.5'

Die aufbewahrte Reproduktion und der Post-Fix-Rerun stehen in
go-contract-literal-selector-remediation.txt (`/var/tmp/codex/ModSecurity-conector/runs/20260722T183342Z-pr80-go-toolchain-submodule-c30d4a37/evidence/go-contract-literal-selector-remediation.txt`)
mit SHA-256 1d924a16b3c724861070bafe652c487c6bcaf0f512a415dc1ae10a9fa7c32fcc.

## Root Cause, Auswirkung und Remediation

Der frühere Checker akzeptierte erforderliche Zeilen unabhängig und wies nur
eine exakte bare go-version:-Schreibweise zurück. YAML erlaubt äquivalente
Mapping-Keys, daher erzwang das Text-Level-Control keinen eindeutigen Selector.

Der immutable v7-Action-Source bei
[actions/setup-go b7ad1dad31e06c5925ef5d2fc7ad053ef454303e](https://raw.githubusercontent.com/actions/setup-go/b7ad1dad31e06c5925ef5d2fc7ad053ef454303e/src/main.ts)
bevorzugt go-version, wenn beide Inputs geliefert werden. Ein geprüfter
Workflow könnte daher eine Literal-Go-Version statt .go-version auswählen, was
Toolchain-Reproduzierbarkeit und das Vertrauen in CodeQLs zentral geprüften
Compiler/Runtime schwächt.

Die lokale Reparatur verlangt, dass der vollständige setup-go-with-Body exakt
folgendem entspricht:

    with:
      go-version-file: .go-version
      check-latest: false

Jede zusätzliche, alternative, zitierte, Leerraum-Variante, explizites
Mapping, Anchor/Merge oder fehlerhafte Input-Form scheitert fail-closed. Der
immutable Action-Pin, das erwartete Job-Inventar, die zentrale Datei und die
Filesystem-Checks bleiben unverändert.

## Akzeptanz, Validierung und Controls

Akzeptanz verlangt, dass alle vier ursprünglichen Varianten zurückgewiesen
werden; der eingecheckte Workflow mit dem exakten Mapping besteht; Action-Pin
und Job-Inventar exakt bleiben; und fokussierte Tests, Checker-Target,
CI-Security-Tests, finaler Security-Review und Exact-Head-Hosted-Checks vor
der Verifikation bestehen.

Lokal bestanden:

- tests.test_go_version_contract: 6 Tests einschließlich der vier
  Bypass-Klassen und des gültigen Central-Selector-Controls.
- make check-go-version-contract.
- Python-Syntaxkompilierung für Checker und Test.
- git diff --check.

Falsche Action-Pins, Literal-Selector, nicht gelistete Go-Jobs und symlinkte
.go-version-Dateien bleiben zurückgewiesen.

Die anschließende vollständige Remediation-Validierung bestand 100 fokussierte
Tests, alle statischen Contracts, Syntaxkompilierung, sichere CLI-help-Smokes
und `git diff --check`. Der finale Security-Diff-Scan meldete keine Befunde:
report.md (`/var/tmp/codex/ModSecurity-conector/runs/20260722T183342Z-pr80-go-toolchain-submodule-c30d4a37/tmp/codex-security-scans/ModSecurity-conector/d99eafd76d9_20260722T221118Z/report.md`)
(SHA-256 `12df4f3ed8d6f850feaf644a512d7bd1de0c3b41b6fffb5e99e021e21a25e1b4`).

## Abhängigkeiten, Blocker, Restrisiko und Historie

Der exakte Head `06a4e71408a60e5a72a55065a653b9c4e79a1ecf` schloss seine
gewöhnlichen GitHub-Checks erfolgreich oder übersprungen ab und bestand das
SonarQube-Cloud-Quality-Gate. Der Befund ist verifiziert; es ist kein Risiko
akzeptiert. Related Finding FND-SONAR-0010 besitzt den früheren hosted
Quality-Gate-Fehler.

- 2026-07-22T22:18:00Z: vier Bypass-Varianten reproduziert und die immutable
  Action-Input-Precedence geprüft.
- 2026-07-22T22:28:04Z: Exact-Body-Regel implementiert; fokussierte Tests,
  Checker-Target, Syntaxkompilierung und Whitespace-Validierung bestanden.
- 2026-07-22T22:47:54Z: vollständige lokale Remediation-Validierung bestand
  (100 fokussierte Tests, Contracts, Syntax, sichere CLI-help und
  Diff-Validierung); der vollständige Security-Diff-Scan meldete keine
  Befunde. Hosted-Nachweis bleibt ausstehend.
- 2026-07-22T23:02:27Z: Exakter Head `06a4e71` bestand gewöhnliche Hosted-
  Checks und SonarQube-Cloud-Quality-Gate; die Selector-Control-Reparatur ist
  verifiziert.

## Geschlossene Disposition — 2026-08-01

[PR #90](https://github.com/Easton97-Jens/ModSecurity-conector/pull/90) wurde
normal als `ad953cdcbc8c05ede519661ca56c03cf7b1ac7f3` gemergt und ist vom
aktuellen `origin/master` `59aba762f2d852fd917079ca8519e4ea7f49169c` erreichbar.
Der aktuelle Checker verlangt weiterhin `go-version-file: .go-version` und
weist den äquivalenten Literal-Selector zurück; der betroffene Scope änderte
sich seit dem Merge nicht. Die exakten PR-Checks einschließlich CodeQL und
SonarCloud bestanden.
