# Change Record: Apache-Intervention-Ownership-Cleanup

**Sprache:** [English](CR-20260720-apache-intervention-ownership.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260720-apache-intervention-ownership` |
| Datum (UTC) | `2026-07-20` |
| Basis-Revision | `929fe60dfca30787947027e5bd49003581a5b080` |
| Grenze | Ausschließlich Parent-Apache-Connector-Source, Parent-Source-Contract-/Wiring-Tests und dieses Parent-Change-Record-/Index-Paar; Framework, MRTS, Abhängigkeiten und beide Gitlinks bleiben unverändert. |
| Finding-Verknüpfung | `FND-PARENT-0043`; `CAND-PARENT-APACHE-INTERVENTION-LEAK-0001`. |

## Motivation und Problemstellung

`process_intervention()` empfängt `ModSecurityIntervention`-Werte von
libmodsecurity. Der Helper vor der Änderung gab nonzero-Interventionsergebnisse
nicht frei. Sein Redirect-Zweig übergab außerdem `intervention.url` an das
nicht kopierende Apache-`apr_table_setn()`, sodass eine Cleanup-Korrektur diesen
Wert zuerst in Request-eigenen Speicher kopieren muss. Einen null
Intervention-Log durch Schreiben eines statischen Literals in das
Intervention-Feld zu ersetzen, wäre ebenfalls unsicher, wenn der native Cleanup
dieses Feld freigibt.

## Akzeptanzkriterien

- Jedes von null verschiedene `msc_intervention()`-Ergebnis erreicht genau
  einen `msc_intervention_cleanup()`-Aufruf, nachdem Apache die Werte kopiert
  hat, die es behält.
- Der No-Intervention-Pfad (`z == 0`) bewahrt die bestehende direkte
  Allow-Rückgabe und ruft keinen nativen Cleanup auf.
- Der gecachte Intervention-Log und die Redirect-URL werden in `r->pool`
  kopiert, bevor Apache sie behält; `Location` behält niemals den
  native-eigenen URL-Zeiger.
- Ein null Log verwendet einen lokalen Fallback-Zeiger, ohne das native-eigene
  Intervention-Feld zu überschreiben.
- Eine fokussierte Source-Contract-Regression deckt Cleanup-,
  No-Intervention-, Fallback-Log-, Redirect-Ownership- und
  C17-Source-List-Invarianten ab.
- Keine Framework-/MRTS-Source, kein Gitlink, keine Abhängigkeit,
  Scanner-Konfiguration oder externe Alert-Disposition ändert sich durch
  diesen Patch.

## Implementierungsentscheidung und Begründung

Die Korrektur verwendet lokale Variablen `log`, `location`, `result` und `z`
in `process_intervention()`. Sie kopiert den Log in `r->pool`, kopiert eine
Redirect-URL in `r->pool` vor `apr_table_setn()` und verwendet einen
`cleanup:`-Pfad für jedes von null verschiedene Ergebnis. Der `z == 0`-Zweig
behält die bestehende direkte Allow-Rückgabe vor dem Behalten eines Apache-Werts,
während Nichtnull-Pfade `result` nach dem nativen Cleanup zurückgeben.

Der neue Source-Contract-Test verhindert, dass ein späterer Nichtnull-Return-
Pfad den Cleanup umgeht, fordert die direkte Null-Ergebnis-Rückgabe, verhindert
das direkte Behalten von `intervention.url`, verhindert die Mutation von
`intervention.log` zum Fallback-Literal und fordert die geänderte Translation
Unit in der Apache-C17-Compilation-Liste. Der Test ist in ein eigenes
Make-Target und das `lint`-Aggregate eingebunden.

## Geänderte Dateien

- `connectors/apache/src/mod_security3.c`
- `tests/test_apache_intervention_cleanup.py`
- `Makefile`
- `ci/checks/connectors/apache/check-apache-c-standards.sh`
- `reports/audits/change-records/README.md` und `README.de.md`
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| `rtk make check-apache-intervention-cleanup` | bestanden: 5 fokussierte Source-Contract-Tests. |
| `rtk make check-apache-c-standard-wiring` | bestanden: Apache-C-Standard-Skript- und Makefile-Wiring-Checks. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_apache_request_transaction_cleanup` | bestanden: 5 bestehende Apache-Transaction-Ownership-Contract-Tests. |
| `rtk make check-apache-request-transaction-cleanup` | statischer Python-Teil bestanden (5 Tests); der native Helper meldete danach fehlendes `apxs`/nutzbare Apache-Header und Make gab `2` zurück. |
| `rtk run 'APACHE_C_STANDARDS_OUT=/var/tmp/codex/ModSecurity-conector/runs/20260720T225753Z-apache-intervention-cleanup-40c97373/apache-c17 make check-apache-c17'` | Environment blockiert: Die Runtime-Component-Preparation schlug fail-closed vor der Compilation fehl, weil lokale Apache-/libmodsecurity-Voraussetzungen fehlen; der Wrapper gab `2` zurück. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_bilingual_docs` | bestanden: 11 Bilingual-Checker-Unit-Tests. |
| `rtk make check-bilingual-docs` | durch bestehende Links in den fehlenden Framework-Gitlink blockiert und Rückgabe `2`; es wurde kein Fehler für dieses Change-Record-Paar gemeldet. |
| `rtk make check-doc-links` | durch dieselben bestehenden fehlenden Framework-Targets blockiert und Rückgabe `2`; es wurde kein geänderter Apache-Change-Record-Link gemeldet. |
| `rtk git diff --check` | bestanden: keine Whitespace-Fehler im Task-Worktree. |

## Security-Auswirkung

Dies ist eine Native-Lifecycle- und Availability-Remediation. Eine Remote-
Anfrage, die eine normale disruptive ModSecurity-Regel trifft, kann Apache
veranlassen, eine Intervention zu verarbeiten. Der ursprüngliche nonzero-Pfad
leakte native Intervention-eigene Puffer. Die Korrektur gibt diese native
Ownership frei und bewahrt Apache-Verhalten, indem sie die behaltenen Werte
zuerst kopiert; dadurch kann der Cleanup keinen Redirect-Dangling-Pointer-Pfad
erzeugen. Der Patch behauptet weder eine gemessene Leak-Rate, noch eine
Produktions-Exposition oder einen abgeschlossenen nativen Sanitizer-Run.

## Runtime-Evidence

Im aktuellen isolierten Parent-Worktree nicht verfügbar. Dem Host fehlen die
Apache-Entwicklungs- und libmodsecurity-Voraussetzungen zum Kompilieren und
Ausführen der betroffenen Translation Unit; eine Apache-ASan/LSan-Wiederholung
wurde nicht ausgeführt. Die erfolgreichen Tests belegen ausschließlich
Source-Level-Ownership- und Control-Flow-Invarianten.

## Protokollbewertung

`process_intervention()` ist transportagnostischer Host-Lifecycle-Code, aber
die betroffene Apache-Grenze bleibt transportnah. Aus den Source-Tests wird
kein Wire-Protokoll-Verhalten behauptet:

- HTTP/1.1: `not_run`; keine native Apache-Runtime war verfügbar.
- HTTP/2: `not_run`; keine native Apache-Runtime oder HTTP/2-Konfiguration war
  verfügbar.
- HTTP/3: `not_run`; keine native Apache-Runtime oder HTTP/3-Konfiguration war
  verfügbar.

Der Patch behauptet über das erhaltene Source-Level-
Intervention-Ownership-Verhalten hinaus keine H1/H2/H3-Kompatibilität.

## Nicht ausgeführte Prüfungen mit Begründung

- Native Apache/APR/libmodsecurity-C17-Compilation und ASan/LSan-Wiederholung
  sind durch fehlendes `apxs`, nutzbare Apache/APR-Header und
  libmodsecurity-Runtime-/Build-Voraussetzungen blockiert. Die fail-closed
  Runtime-Preparation wurde als Environment-Evidence aufbewahrt und nicht
  umgangen.
- Beim Readback `2026-07-20T23:43:04Z` hatte der exakte PR-#72-Head
  `c761a13cb5b4dd3717018960aa03d928758fd21d` sechs erforderliche bestandene
  GitHub-Checks, ein bestehendes SonarQube-Cloud-Quality-Gate, null neue
  Issues, null neue Hotspots und `0,0 %` Duplikation. Der PR war Draft/offen
  und hatte kein eingereichtes Review. Diese Fakten werden nicht auf eine
  spätere SHA übertragen; diese benötigt eigene CI-, Sonar-, Review- und
  Resulting-Master-Evidence.
- Das vollständige `lint`-Aggregate wurde nicht ausgeführt, weil seine
  bestehenden Framework- und nativen Apache-Voraussetzungen in diesem
  isolierten Worktree fehlen; der neu eingebundene Target-Check wurde direkt
  ausgeführt und bestand.
- Kein Framework- oder MRTS-Test lief, weil keine der beiden Grenzen Teil
  dieser Parent-only-Korrektur ist.

## Bekannte Einschränkungen

Die Regression ist strukturell und kein nativer Apache-Prozesstest. Sie kann
kein Allokationsverhalten messen oder die Abwesenheit von Leaks unter
wiederholten Anfragen beweisen. Das kanonische Finding bleibt offen, bis ein
exakter PR-Head mit allen erforderlichen Reviews und der Resulting Master
revalidiert sind; native Sanitizer-Evidence bleibt eine umgebungsabhängige
Folgeanforderung.

## Verbleibende Risiken

Der aktuelle Host beweist weder den vollständigen Host-/Connector-/
libmodsecurity-ABI-Pfad noch das Sanitizer-Verhalten. Andere unabhängig
verfolgte Apache-, NGINX-, Sonar-, Scorecard-, Dependabot-, OSV- und
Secret-Scanning-Punkte liegen außerhalb dieses engen Patches. Es wird kein
Risiko akzeptiert, kein Alert dismissed und kein Scanner-Control geschwächt.

## Finaler Diff- und Review-Status

Die Source-Korrektur ist als
`23b84324e1db8fe13af48ddcc8bf04caae26e30c` auf
`agent/apache-intervention-ownership-20260720` committed und gepusht; ihr
test-only-Sonar-Follow-up ist `c761a13cb5b4dd3717018960aa03d928758fd21d`.
Letzterer ist der beobachtete Head von Draft-PR #72 und bewahrt die direkte
Null-Ergebnis-Rückgabe. Zur Completion sind ein Security-Diff-Review,
geschützte Pull-Request-Validierung, normaler Merge und exakte
Resulting-Master-Revalidierung erforderlich. Die fehlenden nativen
Voraussetzungen sind als Blocker, nicht als bestandener Test erfasst.
