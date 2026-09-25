# Change Record: SonarCloud-Remediation für Publisher-Credential-Übergabe

**Sprache:** [English](CR-20260925-sonar-publisher-askpass.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260925-sonar-publisher-askpass |
| Datum (UTC) | 2026-09-25 |
| Basis-Revision | `92d4498b6f219704fee9363aa5c3ef7b5a2f7fb4` |
| Finding | Vier Parent-`yaml:S2068`-Findings: `AaDXyDL2LGpgyOOFVN7p`, `AaDXyDL2LGpgyOOFVN7q`, `AaDXyDIrLGpgyOOFVN7n`, `AaDXyDIrLGpgyOOFVN7o` |
| Benutzerautorisierung | Das bereitgestellte SonarCloud-Projekt prüfen, Findings sicher auf einem separaten Branch beheben, wenn möglich einen Pull Request erstellen und ihn verifizieren. |
| Delivery-Status | Parent-only-Änderung auf `fix/sonar-publisher-askpass`; Draft-PR nach `master` geplant. Kein Merge, direkter `master`-Write, Framework-/MRTS-Änderung, keine Suppression, Issue-Akzeptanz oder Quality-Gate-Änderung. |

## Motivation und Problemstellung

Der exakte `master`-Readback fand acht ungelöste SonarCloud-Issues. Vier sind
Parent-`.github/workflows`-`yaml:S2068`-Findings in diesen beiden Updater-
Workflows. Sie entsprechen einem selbst definierten Git-Credential-Helper, der
eine App-Token-Credential-Antwort ausgibt. Der Wert ist nicht hart codiert,
aber diese Antwort in der lokalen Git-Konfiguration einzubetten ist unnötig
und fehleranfällig.

Die drei Framework-Workflow-`yaml:S2068`-Findings und ein Framework-
`python:S1192`-Code-Smell liegen außerhalb dieser Parent-only-Grenze.

## Akzeptanzkriterien

- Alle vier gemeldeten Parent-`credential.helper`-Vorkommen entfernen.
- Die bestehende Publisher-only-Source des repository-limitierten GitHub-App-Tokens erhalten.
- `persist-credentials: false`, vertrauenswürdige Publisher-Gates und nicht-interaktives Git beibehalten.
- Für den Git-Passwort-Prompt ausschließlich ein kurzlebiges, nur für den Owner lesbares Askpass-Programm verwenden und es beim Exit entfernen.
- Einen fokussierten Regression-Contract für beide Parent-Publisher ergänzen.
- SonarCloud, Quality Gate, Validierung, Token-Berechtigungen oder Repository-Protections nicht abschwächen.

## Implementierungsentscheidung und Begründung

Jeder betroffene Publisher-Step erzeugt ein temporäres `GIT_ASKPASS`-Programm
mit Modus `0700` unter `$RUNNER_TEMP`. Das quotierte Heredoc enthält nur die
Variablenreferenz, nicht den Tokenwert. Jeder `publisher_git`-Netzwerkaufruf setzt `-c credential.helper=`, um
geerbte Helper zurückzusetzen, sowie command-lokales
`credential.https://github.com.username=x-access-token` und
`credential.https://github.com.useHttpPath=false`. Bevor der Wrapper existiert,
prüft der Step, dass `origin` eine der zwei direkten kanonischen GitHub-URLs
ist. Das tokenfreie Askpass-Programm schlägt fehl, wenn der Prompt nicht
`https://x-access-token@github.com` benennt.

`GIT_TERMINAL_PROMPT=0` und `GIT_ASKPASS` gelten command-lokal und werden
nicht exportiert. Ein EXIT-Trap entfernt das Script.
Bestehende Checkout-, Branch-Gate-, App-Token-Permission-, Path-Validation-
und Force-with-Lease-Controls bleiben unverändert.

## Security-Auswirkung

Source, Scope und Publisher-only-Grenze des Tokens bleiben unverändert. Es
wird nicht in Git-Konfiguration persistiert und nicht in einer Remote-URL
oder einem Kommandozeilenargument übergeben. Die vorhandenen Trusted-
Repository-/Default-Branch-Event-Gates verhindern weiterhin, dass ein nicht
vertrauenswürdiges Event den Publisher erreicht.

## Geänderte Dateien

- `.github/workflows/update-workflow-tools.yml`
- `.github/workflows/update-python-version.yml`
- `tests/test_ci_security_workflows.py`
- `reports/audits/change-records/CR-20260925-sonar-publisher-askpass.md`
- `reports/audits/change-records/CR-20260925-sonar-publisher-askpass.de.md`

Framework-Source, Gitlinks, MRTS-Source, SonarCloud-Einstellungen und
GitHub-Repository-Einstellungen bleiben unverändert.

## Ausgeführte Befehle

| Prüfung | Ergebnis |
| --- | --- |
| Exakte `master`-SonarCloud-Issues vor dem Patch | Acht ungelöste Issues: vier Parent-`yaml:S2068` im Scope, drei Framework-`yaml:S2068`, ein Framework-`python:S1192`. |
| Exakter `master`-GitHub-SonarCloud-Check vor dem Patch | Erwartet fehlgeschlagen: Security Rating on New Code `C`; erforderlich `A`. |
| Source-Transformations-Review | Vier Parent-Helper-Vorkommen werden durch vier Askpass-Flows ersetzt; Checkout-Persistenz und Publisher-App-Token-Mappings bleiben erhalten. |
| Hosted Checks des initialen Draft-PR-Heads | Während der Reparatur fehlgeschlagen: Der Bilingual-Dokumentvalidator verlangte repositoryspezifische Change-Record-Überschriften und der bestehende no-`gh`-CLI-Contract traf eine Prosa-Formulierung. Dieser Successor korrigiert beides; Recheck steht aus. |
| Hosted Checks und PR-Analyse | Beim Erstellen des Records für den exakten Draft-PR-Head ausstehend; PR-Checks vor Merge prüfen. |

## Runtime-Evidence

Es ändert sich kein Connector-Runtime-Verhalten. Dies betrifft nur die
Credential-Übergabe in geplanten oder manuell gestarteten Maintenance-Publishern.

## Nicht ausgeführte Prüfungen mit Begründung

Lokale Repository-Kommandos wurden nicht ausgeführt: Diese Ausführungsoberfläche
hat keinen lokalen Checkout und keine vom Repository verlangte RTK-Kommando-
Umgebung. Die Update-Publisher wurden nicht manuell gestartet, weil das
außerhalb der angeforderten Sonar-Remediation einen Maintenance-Branch oder
Pull Request erzeugen oder ändern könnte.

## Bekannte Einschränkungen

Die Parent-only-Reparatur lässt vier Framework-gebundene Findings unverändert;
sie benötigen einen separat abgegrenzten Framework-Task. Ein tatsächlicher
Publisher-Git-Push benötigt einen gültigen Maintenance-Kandidaten; Static-
und Hosted-Checks sind daher die verfügbaren sicheren Evidenzen.

## Verbleibende Risiken

Das temporäre Programm entsteht auf einem vertrauenswürdigen GitHub-hosted
Runner und wird beim EXIT entfernt, aber eine spätere Workflow-Änderung könnte
diese Eigenschaft abschwächen. Der Source-Regressionstest schützt die Form;
Hosted Checks und SonarCloud-Analyse müssen für den exakten PR-Head vor
einem Merge dennoch bestehen.

## Finaler Diff- und Review-Status

Der begrenzte Diff ändert zwei Parent-Maintenance-Publisher, einen fokussierten
Regression-Contract und diesen zweisprachigen Change Record. Es wird kein
Merge ausgeführt. Der finale Status hängt vom exakten Draft-PR-Head ab, nicht
von der Pre-Merge-`master`-Analyse.
