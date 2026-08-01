# FND-PARENT-0043 — Apache-Interventionspuffer benötigen request-eigene Kopien vor dem nativen Cleanup

## Klassifikation

| Feld | Wert |
| --- | --- |
| ID | `FND-PARENT-0043` |
| Kategorie | `security_validated` |
| Repository / Ownership | `parent` / `parent` |
| Priorität / Schweregrad | `P2` / `medium` |
| Konfidenz / Status | `validated` / `blocked` |
| Feasibility | Source-Korrektur über PR #72 gemergt; native Verifikation `blocked_environment` |
| Release-Blocker | nein |
| Sicherheitsrelevant | ja |
| Source-Basis / exakter PR-Head | `929fe60dfca30787947027e5bd49003581a5b080` / `486aef56424f5bf33bcd7396f6dc2f881f7f3bdd` |
| Delivery-Zustand | PR #72 als Parent-master `0e8be81d14ee9a6ae0497b9ab67e58ba2def1fd3` squash-gemergt; exakte Resulting-Master-Actions bestanden, native Verifikation bleibt blockiert |

## Zusammenfassung und Sicherheitsinvariante

`process_intervention()` überbrückt libModSecurity-eigene `url`- und `log`-
Puffer in den Apache-Request-Zustand. Für jedes von null verschiedene
`msc_intervention()`-Ergebnis muss Apache zunächst jeden behaltenen Wert nach
`r->pool` kopieren und danach `msc_intervention_cleanup()` genau einmal
aufrufen. `apr_table_setn()` darf `intervention.url` niemals direkt behalten.
Der Null-Ergebnis-Pfad gibt `N_INTERVENTION_STATUS` direkt zurück und führt
keinen Cleanup aus.

Dies ist eine requestseitige native Lebensdauergrenze: Ein Remote-Request, der
eine konfigurierte disruptive Regel erfüllt, kann sie ohne lokale Privilegien
erreichen.

## Beobachtetes Verhalten, Ursache und Auswirkung

Auf der Source-Basis `929fe60dfca30787947027e5bd49003581a5b080` übergab
`process_intervention()` `intervention.url` direkt an nicht kopierendes
`apr_table_setn()` und kehrte ohne Nichtnull-Cleanup-Funnel zurück. Sein
Missing-Log-Fallback schrieb außerdem ein statisches Literal in
`intervention.log`.

Die schreibgeschützte gemeinsame libModSecurity-Source beschreibt, dass
Nichtnull-Interventionsergebnisse ihre Felder initialisieren und dass
`msc_intervention_cleanup()` sowohl `url` als auch `log` freigibt. Apache kann
deshalb keinen der nativen Pointer sicher über den Cleanup hinaus behalten:
direkter Cleanup würde einen hängenden `Location`-Wert hinterlassen, und das
Freigeben eines Fallback-Literals wäre ungültig. Die Basis-Source vermeidet den
unmittelbaren hängenden Pointer nur durch Leaken der nativen Puffer, nicht durch
einen Ownership-Transfer.

Der finale PR-#72-Head `486aef56424f5bf33bcd7396f6dc2f881f7f3bdd` kopiert Log
und Redirect-URL nach `r->pool`, behält den Fallback nur in einer lokalen
Variablen, leitet jedes Nichtnull-Ergebnis durch ein Cleanup-Label und bewahrt
die direkte Null-Ergebnis-Allow-Rückgabe. Er wurde als Parent-master
`0e8be81d14ee9a6ae0497b9ab67e58ba2def1fd3` normal squash-gemergt. Sein
test-only-Follow-up beseitigte das aufgabeneigene SonarQube-Cloud-`python:S8786`-
Issue ohne Suppression.

Die aktuelle Evidence stützt ein Memory-Lifecycle- und Response-Integrity-
Finding mittlerer Auswirkung. Native Exploitability und Sanitizer-Verhalten
bleiben unverified, weil die erforderliche Apache/APR/libModSecurity-Umgebung
nicht verfügbar ist.

## Reproduktion und Evidence

Voraussetzungen sind ein gültiger Apache-Request und eine Transaction, ein
von null verschiedenes `msc_intervention()`-Ergebnis und ein disruptiver
Regelpfad. Ein Redirect-Ergebnis liefert einen 3xx-Status und eine URL; Logging
kann einen Log-Puffer liefern oder auslassen.

- Finaler payload-sicherer Receipt: Run
  `20260720T225753Z-apache-intervention-cleanup-40c97373`, Artefakt
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T225753Z-apache-intervention-cleanup-40c97373/evidence/apache-intervention-final-local-validation-20260720T232020Z.json`,
  SHA-256 `349f0a11ed98ad68bf3cbd881599bf7381aba253462113d42e7cf948ed7bf1b6`.
  Er wurde durch
  `rtk run '/root/git/ModSecurity-conector/.codex/bin/storage-budget retain-evidence ...'`
  aus `/root/git/ModSecurity-conector` mit Exit `0` aufbewahrt, beobachtet am
  `2026-07-20T23:20:20Z`, Retention `retained_local_evidence`.
- Der Receipt erfasst, dass `rtk make check-apache-intervention-cleanup` fünf
  Source-Contract-Tests bestand, `rtk make check-apache-c-standard-wiring`
  bestand, `rtk env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
  tests.test_apache_request_transaction_cleanup tests.test_bilingual_docs`
  16 Tests bestand, `rtk git diff --check` bestand und ein unabhängiger
  fokussierter Security-Diff-Review keinen lokalen Delivery-Blocker fand.
- Derselbe Receipt dokumentiert die nativen Grenzen korrekt:
  `rtk make check-apache-request-transaction-cleanup` bestand zuerst fünf
  Python-Assertions, danach fehlten `apxs`/nutzbare Apache-Header und Make gab
  `2` zurück; `rtk run 'APACHE_C_STANDARDS_OUT=/var/tmp/codex/ModSecurity-conector/runs/20260720T225753Z-apache-intervention-cleanup-40c97373/apache-c17 make check-apache-c17'`
  war vor der Compilation wegen fehlender Apache/libModSecurity-Voraussetzungen
  blockiert und gab `2` zurück.
- Schreibgeschützte Upstream-Ownership-Evidence ist `src/transaction.cc`,
  SHA-256 `b148564757d12e9bbe55c65df26d6465d662cb4213a7cd90e9ad4aa9a4a929a7`,
  und `headers/modsecurity/intervention.h`, SHA-256
  `42eca68546bb2a1172b6d5d35c00d5e9aaa2c0649cbacb0cf984bb2a0645fd1d`.
  Die RTK-proxied Hash-Prüfung endete am `2026-07-20T23:11:09Z` mit Exit `0`.
- Aktueller PR- und Change-Record-Receipt: Artefakt
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T225753Z-apache-intervention-cleanup-40c97373/evidence/apache-intervention-pr72-c761-validation-20260720T234605Z.json`,
  SHA-256 `51f57e94617426d9e811b015cd2baae57631a9799741ec31831cd69edf9551bd`.
  Er erfasst, dass der exakte PR-#72-Head `c761a13` sechs erforderliche Checks,
  ein bestehendes SonarQube-Cloud-Quality-Gate, null neue Issues/Hotspots und
  `0,0 %` Duplikation hatte. Er erfasst außerdem fünf fokussierte
  Source-Contract- und elf bilinguale Dokumentations-Unit-Tests nach der
  lokalen EN/DE-Change-Record-Korrektur; vollständige Dokumentations- und
  native Checks bleiben blockiert.
- Resulting-Master-Receipt: Artefakt
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T225753Z-apache-intervention-cleanup-40c97373/evidence/apache-intervention-pr72-master-validation-20260721T000550Z-final.json`,
  SHA-256 `667e2642b90988cf25096ab96c176f6af66f22bb873b3eb6e937d8dc72a1b9f3`.
  Er erfasst Final-Head `486aef`, normalen Squash-Merge #72 am
  `2026-07-21T00:01:04Z`, Resulting Master `0e8be81`, gleiche PR-/Master-Trees
  und 14 erfolgreiche Resulting-Master-GitHub-Actions-Workflows. Das finale PR
  Quality Gate bestand ohne aufgabeneigenes neues Sonar-Issue oder Hotspot.
  Sonar master bleibt nur wegen bewiesen vorbestehendem Backlog `ERROR`; kein
  Scanner- oder Quality-Gate-Control wurde geändert.
- Finaler Exact-Head-Lokalvalidierungs-Receipt: Artefakt
  /var/tmp/codex/ModSecurity-conector/runs/20260720T225753Z-apache-intervention-cleanup-40c97373/evidence/apache-intervention-final-pr-head-local-validation-20260721T002300Z.json,
  SHA-256 e75d97615af04cca6c26b40c61946660e5b83a5554e6c814790545b38f89a20e.
  Auf dem finalen PR-#72-Head 486aef bestanden fünf Apache-Intervention-
  Ownership-Contracts, Apache-C-Standard-Wiring, fünf Request-Transaction-
  Ownership-Tests, elf bilinguale Dokumentationstests und `git diff --check`.
  Dies erzeugt keine Native-Runtime-Evidence; die Voraussetzung bleibt
  blockiert.

## Erforderliche Remediation und Akzeptanzkriterien

1. Der Null-Ergebnis-Pfad gibt `N_INTERVENTION_STATUS` direkt ohne Cleanup
   zurück.
2. Jedes Nichtnull-Ergebnis erreicht genau einen Cleanup nach request-eigenen
   Kopien jedes von Apache behaltenen Log- und Redirect-URL-Werts.
3. `apr_table_setn()` erhält `intervention.url` nie direkt, und die Fallback-
   Behandlung weist `intervention.log` nie ein statisches Literal zu.
4. Redirect- und Nichtredirect-Status behalten ihre beabsichtigte Semantik.
5. Fokussierte Source-, C-Standard-Wiring-, Transaction-Ownership-,
   Dokumentations-, Diff-, Final-PR-Head- und Sonar-Controls bestehen, ohne
   Scanner-, Compiler- oder Test-Controls abzuschwächen.
6. Eine bereitgestellte Apache/APR/libModSecurity-Umgebung wiederholt native
   Compilation, disruptive Redirect-/Nichtredirect-, Allow-, Missing-Log- und
   verfügbare ASan/LSan-Controls.
7. Das korrigierte EN/DE-Change-Record-Paar ist im Final-PR-Head `486aef`
   enthalten; Resulting-Master-Actions und kausale Sonar-/Code-Scanning-
   Readbacks schließen vor Verifikation oder Closure ab.

Die fokussierte Regression ist `tests/test_apache_intervention_cleanup.py`; der
bestehende, nicht duplizierte Transaction-Control ist
`tests/test_apache_request_transaction_cleanup.py`. Legitimate Controls decken
die direkte Null-Rückgabe, Nichtredirect-Status nach Cleanup, request-eigenen
Redirect-Speicher und einen sicher zu bereinigenden Missing-Log-Fallback ab.

## Grenzen, Blocker, Eindeutigkeit und Restrisiko

Dieses Finding ist `blocked`, nicht `fixed`, `verified` oder `closed`: Die
Source-Korrektur, test-only-Sonar-Hardening und der korrigierte EN/DE-Change-
Record wurden durch PR #72 ausgeliefert, mit Exact-Head- und Resulting-Master-
Evidence. Der strengere Security-Workflow verbietet ein `fixed`-Ergebnis,
solange relevante native Verifikation unbekannt ist. Die native Validierung ist
weiter `blocked_environment`: Apache APXS, nutzbare Development-Header, eine
kompatible libModSecurity-Runtime/-Header und eine sanitizerfähige Testumgebung
fehlen. Sonar master ist `ERROR`, aber der unmittelbar vorherige Master war
bereits failed und das exakte PR-Gate bestand ohne aufgabeneigene neue Issues
oder Hotspots; dies ist nicht aufgabenzugehöriger Backlog, kein bestandenes
Master-Sonar-Ergebnis. Sechs aktuelle GitHub-Code-Scanning-Zeilen sind ebenfalls
vorbestehende Scorecard-Leads ohne Bezug zu dieser Apache-Änderung. Framework,
MRTS, Gitlinks, Abhängigkeiten und Scanner-Controls bleiben unverändert.

Dies ist kein Duplikat des generischen Apache-Request-Transaction-Cleanup-
Contracts, der `msc_t`/`msc_cleanup_request_transaction` besitzt; dieses
Finding besitzt die Lebensdauer von `ModSecurityIntervention.url`/`.log` über
`process_intervention()` und APR-Response-Retention. Es ist außerdem von der
Phase-4-Response-Commit-Grenze `FND-PARENT-0038` und dem Harness-CLI-Contract
`FND-PARENT-0041` getrennt.

Der korrigierte Code liegt auf Parent-master, aber native Runtime- und
Sanitizer-Proofs bleiben nicht verfügbar. Daher könnte trotz fokussierter
Source-Invariante, legitimer Controls, PR-Checks und Resulting-Master-GitHub-
Workflow-Evidence ein deploymentspezifischer Lifecycle- oder Integrationsdefekt
unentdeckt bleiben. Es wurde keine Risikoakzeptanz erteilt.

## Historie

- `2026-07-20T23:20:20Z` — Finaler lokaler Source-Validation-Receipt
  aufbewahrt: direktes Null-Verhalten, Exact-once-Nichtnull-Cleanup,
  fokussierte Controls und unabhängiger Review dokumentiert; native
  Runtime-Validierung bleibt blockiert.
- `2026-07-20T23:22:52Z` — Kanonisches Parent-Finding nach Deduplizierung
  angelegt. Dieses Record-Update führte keine Produkt-, Framework-, MRTS-,
  Gitlink-, Git- oder Delivery-Änderung aus.
- `2026-07-20T23:43:04Z` — PR-#72-Exact-Head auf `c761a13` weitergeschoben;
  sechs erforderliche Checks und das SonarQube-Cloud-Quality-Gate bestanden mit
  null neuen Issues/Hotspots und `0,0 %` Duplikation. Der PR bleibt Draft/offen
  ohne eingereichtes Review oder Resulting-Master-Ergebnis.
- `2026-07-20T23:46:05Z` — Das EN/DE-Change-Record-Paar wurde lokal auf die
  direkte Null-Ergebnis-Rückgabe korrigiert. Fünf Source-Contract- und elf
  bilinguale Unit-Tests sowie `git diff --check` bestanden; vollständige
  Dokumentations- und native Checks bleiben blockiert. Es erfolgten kein
  Change-Record-Commit, Push, PR-Update oder Merge.
- `2026-07-21T00:00:58Z` — Das Finding-Ergebnis von `fixed` auf `blocked`
  korrigiert: Source-Korrektur und Exact-Head-Sonar-Ergebnis bleiben gültig,
  aber native Apache/APR/libModSecurity- und Sanitizer-Verifikation ist weiter
  nicht verfügbar.
- `2026-07-21T00:05:50Z` — PR-#72-Final-Head `486aef` wurde normal als
  Parent-master `0e8be81` squash-gemergt; sein Tree entspricht dem Resulting
  Master und alle 14 beobachteten Master-GitHub-Actions-Workflows bestanden.
  Das finale PR-Sonar-Gate bestand ohne aufgabeneigenes neues Issue oder
  Hotspot. Der aktuelle Master-Sonar-Fehler und sechs Scorecard-Code-Scanning-
  Zeilen wurden unabhängig als vorbestehend und unabhängig von dieser Änderung
  belegt.
- `2026-07-21T00:26:43Z` — Der Lifecycle-Status bleibt `blocked`: Delivery-
  und Resulting-Master-Evidence liegen nun vor, aber der strengere Security-
  Workflow verbietet `fixed`, solange native Apache/APR/libModSecurity- und
  Sanitizer-Validierung `blocked_environment` bleiben. Das Finding ist nicht
  verified oder closed.
- `2026-07-21T00:28:49Z` — Den aufbewahrten finalen PR-Head-Lokalvalidierungs-
  Receipt für `486aef` verknüpft: fokussierte Apache-Intervention-, C-Standard-
  Wiring-, Request-Transaction-Ownership-, bilinguale Dokumentations- und
  Whitespace-Controls bestanden. Dies fügt keinen Native-Runtime-Claim hinzu;
  das Finding bleibt `blocked`.
