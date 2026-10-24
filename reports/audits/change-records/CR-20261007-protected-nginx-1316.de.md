# Change Record: CR-20261007-protected-nginx-1316

**Sprache:** [English](CR-20261007-protected-nginx-1316.md) | Deutsch

Benutzerautorisierter Abgleich des geschlossenen Release-Vertrags; kein Runtime- oder Full-E2E-Claim.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261007-protected-nginx-1316 |
| Datum (UTC) | 2026-10-07 |
| Basis-Revision | `60034d48dcee4ae5225bfaff012c48413cc0acd8` |

## Motivation und Problemstellung

Der aktuelle Parent und das freigegebene Framework pinnen bereits NGINX 1.31.6.
Geschützter Builder, Root-Launcher und Result-Collector ließen weiterhin nur
1.31.5 zu; dadurch scheiterten Parent-Provenance- und Release-Abgleichtests.
Der Benutzer autorisierte die separate geschützte Aktualisierung ausdrücklich;
der generische Framework-Updater bleibt von diesem Release-Vertrag ausgeschlossen.

## Akzeptanzkriterien

Alle drei geschützten Grenzen müssen das geprüfte 1.31.6-Tupel akzeptieren und
das vollständige frühere 1.31.5-Tupel, gekreuzte Versions-/Digest-Paare und
beliebige Pins ablehnen. Autorisierung, Pfadautorität, Manifest-Identität und
Runtime-Validierung bleiben strikt. Dependency-Gitlinks und frühere Commits bleiben unverändert.

## Implementierungsentscheidung und Begründung

Genau sechs Konstanten ändern; alle anderen Produktbytes bleiben unverändert:
Version `1.31.6` und Source-SHA256
`974ed5298a5e398e008704ed5db284e655fc270c596493dbccada452448fc9f1`.
Das vorhandene Parent-Provenance-Tupel und Framework-`common.sh` stimmen mit den
[offiziellen Release-Asset-Metadaten](https://github.com/nginx/nginx/releases/tag/release-1.31.6)
für `nginx-1.31.6.tar.gz` überein (veröffentlicht 2026-09-15; 1.373.124 Bytes).
Diese Metadatenprüfung ist keine Attestierung des heruntergeladenen Archivs oder der Runtime.

Framework bleibt `dc41bd22c335156cae02d9049098b92af65b7c57`; MRTS bleibt
`8a6bb546c4c81d8ffc7be801dceac60c6925685f`.

## Geänderte Dateien

Drei Produktdateien unter `ci/runtime/broker/`:
`protected_nginx_exact_head_builder.py`, `nginx_exact_head_root_launcher.py`,
`nginx_exact_head_result_collector.py`; ihre drei entsprechenden Testmodule
unter `tests/`; dieses EN/DE-Record-Paar und die EN/DE-Archivindizes.
Keine Framework-, MRTS-, Gitlink-, generischen Updater- oder Workflow-Änderungen in diesem Commit.

## Ausgeführte Befehle

Alle Shell-Prüfungen verwenden RTK und den Parent-Interpreter
`/root/git/ModSecurity-conector/.venv/bin/python`. Temporäre Dateien, Logs und
Bytecode liegen unter `/var/tmp/codex/ModSecurity-conector/analysis`, nicht im Checkout.
Befehlsumfang, Umgebung und Evidence-Referenzen stehen in
`analysis/framework-pr135-sonar-plan.md` unter diesem externen Root;
exakte Aufrufe bleiben in der Task-Tool-Historie erhalten.

Die neuen Methoden `test_rejects_previous_release_and_crossed_*_pins` an den
Builder-, Launcher- und Collector-Grenzen liefen zuerst gegen unveränderten
Produktcode: drei Fehler, Exit 1, weil das vollständige alte Tupel akzeptiert wurde.
Nach dem Konstantenpatch: drei Tests PASS, Exit 0; alle neun Negativkombinationen abgelehnt.
Logs: `analysis/nginx1316-tuple-{red,green}-20261007.log` und `.exit`.
Builder-Archivtests mocken nur den beobachteten Deskriptor-Hash, keine erwarteten Pins.
Alte Archivnamen scheitern vor dem Hashing; aktueller Name/alter Hash prüft die Digest-Ablehnung.

```text
-B -m unittest -v tests.test_protected_nginx_exact_head_builder
  tests.test_nginx_exact_head_root_launcher tests.test_nginx_exact_head_result_collector
-B -m unittest -v tests.test_protected_nginx_exact_head_workflow
  tests.test_protected_nginx_exact_head_dispatcher tests.test_protected_nginx_exact_head_runner_preflight
  tests.test_nginx_exact_head_base_helper tests.test_nginx_exact_head_gate_contract
  tests.test_nginx_exact_head_diagnostics tests.test_protected_nginx_broker_caller
```

Vollständige drei Grenz-Suites: 91 Tests PASS, keine SKIPs, Exit 0. Geschützte Nachbarn:
76 Tests PASS, keine SKIPs, Exit 0. Aktueller Pin-/Selection-/Wiring-Fokus: 31 Tests PASS,
keine SKIPs, Exit 0, einschließlich der echten Trusted-Framework-API. Logs:
`analysis/nginx1316-{three-suites,protected-neighbors,current-pins-wiring}-20261007.log`.
Auch die acht wiederholten C-Fixture-Module bestehen: 59 Tests, keine SKIPs, Exit 0;
`analysis/nginx1316-ci-fixtures-20261007.log`.

Python-Kompilierung aller sechs geänderten Dateien und `rtk proxy git diff --check`
bestehen. Ein exakter Source-Vergleich bestätigt nur die sechs freigegebenen Ersetzungen.
Natives `make check-ci-security-contract`: 219 Tests ausgeführt, 214 bestanden und
fünf explizite Namespace-/Identity-SKIPs, Exit 0; Tool-Lock-Validate-only-Prüfungen bestehen.
Vollständige Workflow-/Updater-Wiederholung: 69 Tests PASS, keine SKIPs, Exit 0. Logs:
`analysis/nginx1316-{ci-security-contract,workflow-updater}-20261007.log` und `.exit`.
Natives `make check-bilingual-docs check-doc-links` und die reine Archivprüfung
`ci/tools/new-change-record.py check` bestehen. Geänderter Workflow:
`rtk proxy actionlint .github/workflows/run-protected-nginx-exact-head.yml`
(einschließlich ShellCheck) besteht. Dokumentationslog:
`analysis/nginx1316-docs-20261007.log`, Exit 0. Der erste Actionlint-Versuch verwendete
einen nicht vorhandenen verkürzten Dateinamen und endete mit Exit 3; das ist kein Lint-PASS.

## Security-Auswirkung

Keine Guardrail, kein Schema, keine Berechtigung, Isolation, Containment, Freshness,
No-follow-Prüfung, Evidence-Validierung, Warnung oder Test-Assertion wird abgeschwächt.
Das alte Release wird aus der geschlossenen Allowlist entfernt, nicht neben dem neuen zugelassen.
Trusted-Tool-/Master-Zulassungsregeln des geschützten Workflows bleiben unverändert;
diese Konstantenänderung macht einen gestapelten PR nicht zum geschützten Dispatch berechtigt.

## Runtime-Evidence

Keine erzeugt. Unit-Manifeste, private Collector-Fixtures und gemockte Source-Hashes
sind Vertragstests, keine echte HTTP-, Root→nobody- oder kanonische Coverage-Evidence.
Kein manueller Lifecycle oder geschützter Dispatch wurde ausgeführt.

## Bekannte Einschränkungen

Ein vollständiger lokaler Parent-Lint-Versuch aus dem vorherigen Fix bleibt unvollständig:
anfänglicher Output-Root-Fehler und abgebrochenes breites Provisioning sind kein PASS.
Namespace-/Identity-Tests können lokal fehlende Capabilities benötigen; explizite
SKIPs erhalten keinen Isolation-Credit. Historische CI-/Sonar-Ergebnisse beweisen
den neuen Commit nicht. Frische Remote-Ergebnisse müssen an den veröffentlichten Nachfolger-SHA gebunden sein.

## Verbleibende Risiken

Unit- und statische Prüfungen attestieren weder eine neue Binärdatei noch eine
geschützte Runtime. Neue Head-gebundene Hosted-CI und anwendbares Sonar-Readback
bleiben Delivery-Gates. Breitere frische Coverage-/MIME-Arbeit wartet auf diese Gates.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Full E2E, geschützter Workflow-Dispatch, keine Paketinstallation, Framework-/
MRTS-Änderung, kein Master-Push oder Merge ist in diesem begrenzten Follow-up autorisiert.
Kein Archiv-Download/Build ist nötig, um den geschlossenen Tupelfehler zu beheben und zu testen.

## Finaler Diff- und Review-Status

Sechs Produktersetzungen und 60 Testergänzungen; keine vorhandenen Assertions entfernt.
Das unabhängige begrenzte Security-Review fand keinen validierten Befund.
Ursprüngliche RED-Evidence bleibt erhalten. Separater Follow-up-Commit, kein Amend
oder Umschreiben der Historie; PR #396 bleibt OPEN/DRAFT. Remote-Gates werden nicht vorab behauptet.
