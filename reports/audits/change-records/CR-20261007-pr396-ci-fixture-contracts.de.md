# Change Record: CR-20261007-pr396-ci-fixture-contracts

**Sprache:** [English](CR-20261007-pr396-ci-fixture-contracts.md) | Deutsch

Begrenzte CI-Remediation für den bestehenden Draft-PR #396, kein neuer Runtime-Claim.
Getrennte Source-Commits: `cee4cdfe191045296f2388e4529e1d4337273a3d`,
`ab7db2dd3be6e10b5bb6a83fc8b7f56949dcb7f7`,
`7da51a310fe7a6a366017f58f556f54bc48bd162`.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261007-pr396-ci-fixture-contracts |
| Datum (UTC) | 2026-10-07 |
| Basis-Revision | `1f68c3742bd29b23a6938b36816adff4524944c7` |

## Motivation und Problemstellung

Der fortgesetzte PR-Head hat vier fehlgeschlagene Workflow-Läufe: Scaffold-Lint,
Workflow-Security-Lint und Envoy für Pull-Request- und Push-Events. Reproduzierbare
Ursachen sind unvollständige Source-Extraktions-Fixtures, ein Default-Deny-/Publisher-
Pfadvertragskonflikt und ein zu langer Unix-Socket-Testpfad. Vorhandene Sourcefixes
und die extern weiterentwickelten Dependency-Pins bleiben erhalten.

## Akzeptanzkriterien

Alte Fehler vor der Reparatur reproduzieren; betroffene Tests und integrierte
CI-Verträge bestehen ohne Abschwächung von Assertions, Warnungen oder Guardrails.
Framework `dc41bd22c335156cae02d9049098b92af65b7c57` und MRTS
`8a6bb546c4c81d8ffc7be801dceac60c6925685f` bleiben wie ausdrücklich ausgewählt.
PR #396 bleibt OPEN/DRAFT/unmerged. CI/Sonar des neu veröffentlichten exakten SHA
müssen vor frischer Coverage-Messung oder MIME-/Required-Fortsetzung bestehen.

## Implementierungsentscheidung und Begründung

Drei unabhängige Ursachen erhalten getrennte Follow-up-Commits:

- C-Test-Fixtures ergänzen den echten Integrity-Emission-Callee und benötigte
  POSIX-Header; die NGINX-Fixture implementiert den direkten Context-Getter der
  aktuellen extrahierten Source. Kein Produktcode und keine Assertion geändert.
- Der geschützte Workflow verweigert globale Berechtigungen und gibt seinem
  Resolver nur `contents: read`. Sein einzelner exakter Pfad kommt in beide
  bestehenden geschlossenen Updater-Allowlisten. Actor-, Protected-Master-, SHA-
  und Privilege-Kontrollen bleiben erhalten.
- Der Envoy-Peer-Credential-Test nutzt den vorhandenen privaten Kurzverzeichnis-
  Helper statt des langen Testnamen-Verzeichnisses. Freshness, Cleanup und UID-
  Mismatch-Abweisung vor jeglichen Claim-Bytes bleiben erhalten.

## Geänderte Dateien

`tests/test_runtime_event_sink_failures.py`,
`tests/test_nginx_request_error_events.py`,
`connectors/envoy/ext_proc/internal/responseobserver/peercred_linux_test.go`,
`.github/workflows/run-protected-nginx-exact-head.yml`,
`.github/workflows/update-workflow-tools.yml`, `ci/tools/update-workflow-tools.py`,
dieses EN/DE-Record-Paar und `reports/audits/change-records/README.md` / `README.de.md`.
Kein Produkt-C/Go-, Dependency-, Framework-/MRTS-Source- oder Gitlink-Eingriff.

## Ausgeführte Befehle

Artefakte mit Präfix `analysis/` liegen unter dem autorisierten externen Root
`/var/tmp/codex/ModSecurity-conector`, nicht im Checkout. Exakte umgebungsgebundene
Befehle, Ownership und Ergebnisse stehen in
`analysis/framework-pr135-sonar-plan.md`. Alle Shell-Prüfungen nutzten RTK.

Parent-Interpreter: `/root/git/ModSecurity-conector/.venv/bin/python`.
Der integrierte C-Test-Payload war `-B -m unittest -v` mit diesen Modulen:

```text
tests.test_runtime_event_sink_failures tests.test_runtime_host_action_validation
tests.test_nginx_request_error_events tests.test_c_source_contract
tests.test_nginx_request_native_results tests.test_nginx_request_phase_completion
tests.test_runtime_transaction_snapshot_contract tests.test_event_runtime_security_contract
```

Baseline: drei Fixture-Kompilierfehler, Exit 1. Reparierter Gesamtlauf:
59 Tests PASS, keine SKIPs, Exit 0. Log:
`analysis/pr396-ci-fixtures-integrated-20261007.log` und `.exit`.
Workflow-Baseline: zwei exakte Regressionen scheitern, Exit 1. Reparierte
Workflow-Suite: 31 Tests PASS; Updater-Suite: 38 Tests PASS. Native Root-Prüfung
`rtk proxy env ... make check-ci-security-contract` bestand: 219 Tests, sechs
explizite SKIPs, Exit 0; auch Tool-Lock-Validate-only-Prüfungen bestanden. Log:
`analysis/pr396-ci-contract-env-bound-20261007.log` und `.exit`. Nach Bereitstellung
des unveränderten verschachtelten Framework-Checkouts bestand dieselbe native
Prüfung erneut: 219 Tests, fünf Namespace-/Identity-SKIPs, Exit 0; die echte
reviewte Framework-Fixture lief nun. Log:
`analysis/pr396-ci-contract-nested-20261007.log` und `.exit`. Root wiederholte
auch beide vollständigen Workflow-/Updater-Suites gemeinsam: 69 Tests PASS,
keine SKIPs, Exit 0; `analysis/pr396-workflow-updater-integrated-20261007.log`.
Der erste native Aufruf endete mit Exit 2, weil ein Kommandozeilen-`BUILD_ROOT`
über `MAKEFLAGS` vererbt wurde; der unveränderte Wiederholungslauf übergab die
Roots wie CI über die Umgebung. Der erste Fehler bleibt erhalten und ist kein PASS.

Go-Prüfungen nutzten lokales Go 1.27.1, externe Caches, `GOPROXY=off`,
`-mod=readonly` und denselben absichtlich langen externen Temp-Root. Test-/Vet-
Befehle liefen aus `connectors/envoy/ext_proc`, gofmt aus dem Parent-Root. Ein
unveränderliches Alt-Source-Overlay reproduziert `bind: invalid argument`, Exit 1.
Aktuelle Befehle:

```text
go test -mod=readonly -count=1 -timeout=120s ./internal/responseobserver
go test -mod=readonly -race -count=1 -timeout=120s ./internal/responseobserver
go vet -mod=readonly ./internal/responseobserver
go test -mod=readonly -count=1 -run 'a^' ./cmd/msconnector-envoy-response-observer
gofmt -l connectors/envoy/ext_proc/internal/responseobserver/peercred_linux_test.go
```

Alle aktuellen Befehle bestanden über `rtk proxy` mit Exit 0; die Command-Package-
Prüfung ist compile-only, keine Runtime-Evidence. Logs:
`analysis/pr396-envoy-peercred-{baseline,current,race}-20261007.log` und `.exit`.
`rtk proxy actionlint` der geänderten Workflows (einschließlich ShellCheck) und
`rtk proxy git diff --check` bestanden. Native Bilingual-/Pfad-/Link-Prüfungen
bestanden mit Exit 0: `analysis/pr396-ci-docs-nested-20261007.log` und `.exit`.
Die erste Doc-Prüfung lehnte Links durch ein leeres verschachteltes Framework-
Verzeichnis korrekt ab. Ein zusätzlicher vollständiger Parent-Lint-Versuch
endete mit Exit 2 am Apache-Checker-Output-Default außerhalb des autorisierten
Codex-Roots. Der Wiederholungslauf nutzt dessen vorhandenen
`APACHE_C_STANDARDS_OUT`-Override unter dem Task-Build-Root, bei unveränderten
Prüfungen; er erreichte fehlende HAProxy-Header und breite automatische Runtime-
Provisionierung und wurde deshalb mit Exit 130 gestoppt. Keiner der vollständigen
Lint-Versuche ist PASS. Logs: `analysis/pr396-parent-lint-20261007.log` und
`analysis/pr396-parent-lint-root-bound-20261007.log`; dessen `.exit` dokumentiert
die vom Tool beobachtete Unterbrechung, kein abgeschlossenes Wrapper-Receipt.
Exakte Befehle/CWD im Plan. Geänderte Python-Dateien kompilierten ebenfalls
erfolgreich mit externem Bytecode-Output.

## Security-Auswirkung

Kein Validator, Containment-, Freshness-, Peer-Authentifizierungs-, Event-,
Canonical-Status-, Compilerwarnungs- oder Security-Assertion-Vertrag wird gelockert.
Der Publisher erhält einen exakten autorisierten Workflow-Pfad, keinen Wildcard-
oder beliebigen Schreibzugriff. Der vorhandene Socket-Helper erzeugt ein privates
frisches Verzeichnis und registriert Cleanup.

## Runtime-Evidence

Kein manueller Host-Lifecycle, HTTP-Request, Protected-Workflow-Dispatch, neue
kanonische Runtime-Evidence oder Full Exact-Head E2E in diesem Remediation-Schritt.
Unit-Test-Sockets und Fixture-Kompilierungen beweisen keine NGINX-Runtime-Coverage.

## Bekannte Einschränkungen

Die ersten sechs integrierten SKIPs enthielten die nicht initialisierte Framework-
Fixture; nach Bereitstellung ihres unveränderten Checkouts bleiben fünf nobody-/
Mount-/PID-Namespace-SKIPs. Dies sind keine bestandenen Isolationstests.
Ein beliebig langer Temp-Root selbst kann die
Unix-Socket-Grenze weiterhin überschreiten. Historische Coverage-Zahlen und ältere
CI-/Sonar-Ergebnisse sind kein aktueller Head-Nachweis.

## Verbleibende Risiken

Vollständiger lokaler Parent-Lint bleibt unvollständig; Hosted-CI und Sonar-
Readback des neuen Heads bleiben Delivery-Gates. Fehlende
Required-Runtime-Evidence bleibt fehlend; diese Fixture-/Workflow-Fixes geben
keine Coverage-Gutschrift.

## Nicht ausgeführte Prüfungen mit Begründung

Full E2E ist in diesem Schritt ausdrücklich verboten. Protected-Dispatch und
Live-Publisher-Ausführung sind für begrenzte Fixture-/Allowlist-Änderungen nicht
nötig. Frische Coverage-/MIME-Arbeit wartet auf die Remote-Gates des neuen Heads.
Kein Master-Merge autorisiert.

## Finaler Diff- und Review-Status

Die sechs Code-/Test-/Workflow-Pfade umfassen 14 Einfügungen und vier Löschungen.
Unabhängiger statischer Security-Review fand keinen validierten Befund; bestehende
Negativkontrollen bleiben aktiv. Unabhängiger EN/DE-Review bestätigte Parität und
exakte Befehlsnachvollziehbarkeit; native Dokumentationsprüfungen bestanden.
Der finale begrenzte Diff ist sauber; SHA-gebundene Remote-Delivery-Prüfungen
bleiben erforderlich. Kein History-Rewrite, Merge oder Staging von Secrets.
