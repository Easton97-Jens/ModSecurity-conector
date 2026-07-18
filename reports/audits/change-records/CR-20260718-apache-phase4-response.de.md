# Change Record: Apache-Phase-4-Response-Enforcement

**Status:** Die Phase-4-Remediation liegt in Parent-only-Draft-PR #60. Sein
initialer Head `783c024b8cb90c783adfa7a18e85de170a28e1b5` bestand CI und
CodeQL, aber SonarQube Cloud schlug bei task-eigenem Regression-Control-Code
fehl. Die fokussierte Remediation von `FND-SONAR-0001` läuft; dieser Record
behauptet keinen finalen SonarQube-Cloud-Erfolg oder Merge.

**Sprache:** [English](CR-20260718-apache-phase4-response.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260718-apache-phase4-response |
| Datum (UTC) | 2026-07-18 |
| Basis-Revision | c8ca0d92b630c18232b881855c4f5d1482568ea6 |
| Scope | Nur Parent-Repository |
| Zugehöriges Finding | FND-PARENT-0038 |
| Zugehöriges Delivery-Quality-Finding | FND-SONAR-0001 |
| Framework- / MRTS-Status | read-only, clean bei cdc91a398d6c156eaff927d742b23018a3817fb6 / 13aa91291adea12d5c607fdd165d010fcfb1da78 |

## Motivation und Problemstellung

Apache konnte Response-Buckets weiterleiten, bevor libModSecurity die
EOS-only-Phase-4-RESPONSE_BODY-Entscheidung traf. Ein disruptiver Deny konnte
deshalb nach der Downstream-Commit-Grenze geschützter Bytes erfolgen. Der
aufbewahrte Pre-Fix-Internal-Redirect-Reproducer zeigt den direkten Target mit
Regel 2190411 und HTTP 403, während der Redirect HTTP 200 und den
Response-Marker zurückgab.

Dieser Record behebt ausschließlich den Apache-/libModSecurity-Phase-4-
Response-Pfad. Er ändert keinen anderen Connector, kein Framework und kein
MRTS.

## Akzeptanzkriterien

Die Broken-Control-Kette war:

~~~
upstream response bucket
  -> MODSECURITY_OUT append/forward
  -> downstream ap_pass_brigade before EOS
  -> msc_process_response_body + process_intervention at EOS
~~~

Angreifervoraussetzungen sind eine erreichbare Response, deren Body vor EOS
eine bereitgestellte disruptive Phase-4-SecRule RESPONSE_BODY matcht; normale
Internal Redirects und mehrere Brigades machen die alte Escape-Bedingung leichter
nachweisbar. Lokale Privilegien werden nicht vorausgesetzt.

Die Sicherheitsinvariante ist, dass ein Response-Byte, das Phase 4
berücksichtigen kann, Downstream nicht erreicht, bevor
msc_process_response_body und die resultierende Intervention entschieden sind.
Der letzte Blocking-Zeitpunkt ist daher der erste und einzige Downstream-Release,
nicht sent_bodyct-artiger Apache-State, der Upstream des Connectors markiert
werden kann.

Die kleinste vollständige Enforcement-Grenze ist ein EOS-Gate für jede Response,
die den Apache-Output-Filter erreicht. Die C-API von libModSecurity exponiert
keine sichere Query für die effektive SecResponseBodyMimeType-Entscheidung. Ein
Narrowing durch die Legacy-MIME-Liste des Connectors, das Forwarding eines
inspizierten Präfixes oder ein Release eines uninspektierten Tails würde den
Bypass wiederherstellen.

Die abgeschlossene Reparatur muss daher alle folgenden Punkte nachweisen:

- Ein Phase-4-Deny unterdrückt den matchenden Body vor dem ersten
  Downstream-Commit.
- Allow und log-only erhalten eine vollständige normalisierte Response genau
  einmal, einschließlich leerer und mehrerer Brigades.
- Late Output, Pre-Commit-Fehler, unsichere Redirects und Cleanup können weder
  gehaltene Originalbytes leaken noch EOS duplizieren.
- Native-Apache-H1/H2-, fokussierte CRS/MRTS-Controls und Current-Source-
  Security-Checks erzeugen aufbewahrte Evidenz, ohne Framework oder MRTS zu
  ändern.

## Implementierungsentscheidung und Begründung

- Der Output-Filter normalisiert jede Pre-EOS-Brigade, hält sie mit
  ap_save_brigade zurück und hängt den vollständigen begrenzten Body an
  libModSecurity an.
- Bei EOS führt er msc_process_response_body und process_intervention vor dem
  einzigen Release aus. Allow stellt den Phase-3-Snapshot wieder her und
  releast gespeicherte Brigades genau einmal; Deny verwirft die
  Original-Brigades und geht in den terminalen Fehlerpfad.
- Connector-eigener Release-State und beobachteter Commit-State ersetzen
  sent_bodyct als Nachweis eines Connector-Releases.
- MODSECURITY_PHASE4_GUARD bleibt in der Protocol-Filter-Kette, um Producer-
  Output nach EOS oder terminalem Deny einschließlich zweitem Body/EOS zu
  verwerfen.
- Oversize-, Append-, Bucket-Read-, Setaside-, Missing-Context- und unsichere
  Redirect-Bedingungen fail-closed, bevor Originalbytes releast werden.
- Der bestehende Unread-Request-Body-Pfad nutzt dieselbe Pre-Commit-Terminal-
  Bridge nur dann, wenn eine Phase-2-/Error-Response MODSECURITY_OUT erreicht.
  Das ist ein notwendiger Kompatibilitätsteil der neuen Output-Grenze: Der
  Protocol-Guard würde andernfalls die Error-Emission unter diesem Pfad
  verändern. Phase-2-Regelauswertung wird dadurch nicht verändert und es
  entsteht kein zweiter Response-Body-Pfad.
- Ein gültiger erster Apache-Error-Bucket nutzt die Pre-Commit-Terminal-Bridge.
  Apache-core-markierte lokale ErrorDocument-Emission ist auf einen Hop
  begrenzt, während terminaler Output emittiert; gewöhnliche r->prev-Redirects
  fail-closed, weil eine native Transaction nicht sicher an den Target-Request
  neu gebunden werden kann.
- Cleanup verwirft gehaltene Brigades. Der Patch deaktiviert Phase 4 nicht und
  deutet Deny nicht zu log-only um.

Legitime Response-Auslieferung nach einem erlaubten EOS bleibt erhalten.
Progressive Auslieferung vor einer Phase-4-Entscheidung ist für diese
Sicherheitsgrenze absichtlich nicht verfügbar; die Implementierung erhält die
Response-Semantik nach der Entscheidung, statt Bytes davor offenzulegen.

## Geänderte Dateien

Produktionscode und Apache-Harness:

- connectors/apache/src/mod_security3.c und mod_security3.h
- connectors/apache/src/msc_filters.c und msc_filters.h
- connectors/apache/src/msc_config.c
- connectors/apache/src/msc_utils.c und msc_utils.h
- connectors/apache/harness/apache_smoke.conf
- connectors/apache/harness/run_apache_smoke.sh
- connectors/apache/harness/mod_phase4_terminal_rogue.c

Fokussierte Regression und statisches Wiring:

- ci/runtime/lifecycle/run-apache-phase4-response-regression.sh
- ci/runtime/lifecycle/apache_phase4_content_type_synchronized_upstream.py
- ci/runtime/lifecycle/cases/apache-phase4-response/
- tests/test_apache_phase4_response_regression_wiring.py
- tests/test_apache_phase4_content_type_synchronized_upstream.py
- tests/test_nginx_phase4_runner_wiring.py
- ci/checks/connectors/apache/check-apache-common-adoption.py
- ci/checks/documentation/connector_config_reference.py

Dokumentation und generierte Verträge:

- connectors/apache/README.md und README.de.md
- connectors/apache/TODO.md und TODO.de.md
- connectors/apache/capabilities.json
- docs/architecture.md und architecture.de.md
- docs/connectors/apache.md und apache.de.md
- docs/operations-and-security.md und operations-and-security.de.md
- docs/repository-concept.md und repository-concept.de.md
- examples/apache/README.md und README.de.md
- examples/apache/configuration-reference.md und configuration-reference.de.md
- examples/apache/rules/p1-p4-safe.conf und examples/apache/safe/httpd.conf
- reports/connector-configuration-inventory.json
- reports/testing/generated/canonical/connector-capabilities.generated.json,
  connector-capabilities.generated.md und connector-capabilities.generated.de.md

## Ausgeführte Befehle

Alle aufbewahrte Runtime-/Build-Evidenz liegt unter
/var/tmp/codex/ModSecurity-conector/runs/20260718T075119Z-apache-phase4-response-098df329.

1. Die Pre-Fix-Reproduktion bestand als Beobachtung: Der direkte URI-Target
   loggte Regel 2190411 mit HTTP 403, aber der aufbewahrte Internal Redirect
   lieferte HTTP 200 plus no-crs-response-body-marker.
2. Aktuelle fokussierte Native-Cases bestanden: deny, allow, log-only, rogue-H1-
   Deny, rogue-H1-Allow, rogue-H2-Deny, empty Allow/Deny, Connector-Limit,
   ProcessPartial, Custom-MIME, client-abort, P3-Deny/Header-Freeze, gültige
   Upstream-/Downstream-ErrorDocument-H1/H2, nested-/pre-output-ErrorDocument-
   fail-closed-Controls und normale/Target-/URI-Redirect-fail-closed-Controls.
3. Die aktuellen H1/H2-Multi-Brigade-Denies loggten Regel 2190401 mit HTTP 403,
   response_not_committed, headers_sent false und eos_seen true.
4. make build-apache bestand mit Component
   696a153ff197a6c939ce29034a59291e7694674f16ff20af7efe3a591e273a3d.
   make check-config-apache bestand; jede native Harness-Invocation führt
   httpd -t vor Start aus.
5. Statische Checks bestanden: Shell-Syntax für Harness und fokussierten Runner,
   tests.test_apache_phase4_response_regression_wiring (8 Tests),
   check-apache-common-adoption, generierte Configuration-Reference-Checks und
   git diff --check.
6. GCC C17 und strikte fokussierte GCC-/Clang-C17-Checks bestanden.
   Whole-source strict Clang bleibt nur wegen des unveränderten
   origin/master-msc_config.c:110-Initializers aus Commit cfc8b487 blockiert.
7. Frische v12-APXS-ASan- und UBSan-DSOs bestanden native rogue-h1, deny und
   rogue-h2. Der H2-Transfer wurde als HTTP/2 verhandelt; sechs
   Diagnose-Scans enthielten keinen AddressSanitizer- oder
   UndefinedBehaviorSanitizer-Finding. Apache httpd und libModSecurity selbst
   waren nicht instrumentiert, und ASan nutzte detect_leaks=0.
8. make clang-analysis-baseline bestand. Der aktuelle Harness-Clang-Analyzer
   erzeugte keine Findings; clang-tidy erzeugte nur nicht-sicherheitsrelevante
   Advisory-Warnungen.
9. Das fokussierte Apache-CRS-Profil bestand crs_sqli_anomaly_block mit HTTP
   403. Die kanonische No-CRS-Phase-4-Fixture lehnt eine CRS-Preamble
   absichtlich ab und wurde daher nicht als fehlgeschlagener CRS-Test behandelt.
10. Das fokussierte Apache-MRTS-Profil
    mrts_100152_mrts_069_response_body_100152_1 bestand als Live-Phase-4-
    RESPONSE_BODY-Nicht-Disruptive-Control mit HTTP 200.
11. Unabhängiger Codex-Security-Source-to-Sink- und Bypass-Review fand keinen
    verbleibenden bestätigten Bypass des ursprünglichen Held-Response-Body-Pfads.
12. Nachdem SonarQube Cloud den initialen PR-Head beanstandete, bestanden die
    fokussierte Control-Path-Härtung, die Shell-Syntax, die Apache-
    Response-Wiring-Tests zusammen mit den neuen Content-Type-Synchronized-
    Upstream-Unit-Tests (14 Tests), check-apache-common-adoption und
    git diff --check. Der Helper akzeptiert Control-Dateien nun nur unter einem
    existierenden harness-eigenen Control-Root.
13. Der geänderte Helper bestand auch die native Custom-MIME-synchronisierte
    Phase-4-Deny-Regression mit Apache-Konfigurationsprüfung. Er hielt die
    Upstream-Response bis EOS zurück und lieferte das erwartete HTTP 403 ohne
    den geschützten Original-Body.

## Runtime-Evidence

Pre-Fix- und Post-Fix-Evidenz ist in FND-PARENT-0038 hash-adressiert. Die
zentralen aufbewahrten Artefakte sind:

| Evidenz | SHA-256 |
| --- | --- |
| Pre-Fix-HTTP-200-Redirect-Status | c11e3f4837efde2441e23a7b9da02131f53bf59fddeb7147c4ab81afe400460f |
| Pre-Fix-Marker-Body | b186cc3103543b398e617165a51528ccae430b063105434b29a0b01aea28c9ee |
| Aktuelles Deny-Phase-4-Log | 45732d58de3644852c63c4d20d29118d7c6cae3f667407efdf3c3654ff03be41 |
| Aktuelles H2-Rogue-Phase-4-Log | bd18170c8e4b3a3dae42abaa03af232f7f2b452f2b6e88556e0e23c95904516d |
| Frischer v12-ASan-H2-Rogue-Transfer | e4f4ac5699d92415b1de480cf593d029b8d3185b025db81e0662de40532dd8fe |
| Frischer v12-UBSan-H2-Rogue-Transfer | ab569dde9d18e2e942792e39100dd0bebe3ca292c819172b8d051e24689e181a |
| CRS-Kompatibilitätsergebnis | 8c7de5d36446759e0753874937565dd13808098e70cbe16e5096ae84bbd9ecd8 |
| MRTS-Phase-4-Ergebnis | d77175c27bd56ad0a08c4945aa1a2e56e6628df55a3f5c5154d48154582f5444 |

## Security-Auswirkung

Die Reparatur wandelt eine EOS-only-Entscheidung, die früher Downstream des
ersten Response-Releases lag, in ein Pre-Commit-Gate um. Sie deckt Late
Intervention, duplizierten Output, leere Responses, Body-Limit-Fehler,
Error-Buckets, Cleanup, Redirects und ErrorDocument-Verhalten ausdrücklich ab.
Sie behält eine absichtliche Fail-Closed-Policy, wo Apache-/libModSecurity-
Transaction-Semantik nicht sicher erhalten werden kann.

## Dokumentation und Kompatibilität

Die englische/deutsche Apache-Dokumentation und Beispiele beschreiben EOS-Gate,
opaque libModSecurity-MIME-Entscheidung, begrenztes Response-Body-Limit,
terminalen Guard, fail-closed-Redirect-Policy und Evidenzgrenzen. Generierte
Configuration-/Capability-Artefakte wurden durch ihre konfigurierten Checks
aktualisiert. Framework- und MRTS-Source/Gitlinks bleiben unverändert.

## Bekannte Einschränkungen

- Die begrenzte lokale ErrorDocument-Ausnahme nutzt die Apache-Core-Korrelation
  von no_local_copy und REDIRECT_STATUS. Sie ist starke Apache-Core-Evidenz,
  aber keine unforgeable Provenance-Primitve; ein request-only Exploit wurde
  nicht gezeigt.
- Der Phase-3-Snapshot umfasst normale Response-Headers, aber keine
  Allzweck-Garantie über HTTP/2-Trailer oder Downstream-Filter, die State nach
  Release mutieren. Dies kann den gehaltenen Original-Body nach Deny nicht
  leaken.
- Response-Bytes, die Phase 4 unterliegen, werden bis EOS gehalten. Das ist mit
  der verfügbaren libModSecurity-C-API die kleinste sichere Grenze und tauscht
  progressive Phase-4-Streaming gegen Enforcement.

## Verbleibende Risiken

- Die volle CRS/MRTS-Matrix lief nicht; fokussierte anwendbare Profile liefen.
- Exact-Head-externe Delivery-Evidenz für den SonarQube-Cloud-Remediation-
  Follow-up steht noch aus.

## Nicht ausgeführte Prüfungen mit Begründung

- Draft-PR #60, initialer Head `783c024b8cb90c783adfa7a18e85de170a28e1b5`:
  CI und CodeQL bestanden, aber SonarQube Cloud schlug beim Quality Gate mit
  C Security Rating und D Reliability Rating auf neuem Code fehl. Der
  betroffene task-eigene Helper, Harness und statische Checker sind als
  `FND-SONAR-0001` getrackt; der Follow-up-Exact-Head ist noch nicht verifiziert.
- Volle CRS/MRTS-Matrix: Für diesen fokussierten Parent-Fix nicht erforderlich;
  eine fokussierte CRS-Kompatibilitäts-Control und die exakte
  MRTS-RESPONSE_BODY-Phase-4-Control liefen.
- Whole-source strict Clang C17: wegen der unveränderten
  origin/master-msc_config.c:110-Baseline-Warnung blockiert, nicht wegen des
  Phase-4-Patches.
- Vollständiger Repository-Bilingual-Docs-Link-Check: Die EN/DE-Struktur des
  neuen Change Records bestand, aber der dedizierte Worktree lässt seinen
  Framework-Gitlink absichtlich nicht ausgecheckt. Die verbleibende Checker-Ausgabe
  ist auf bereits vorhandene Links in diesen read-only-Framework-Checkout
  beschränkt; die externen Framework- und MRTS-Checkouts wurden separat als
  clean bestätigt.

## Finaler Diff- und Review-Status

Der User autorisierte einen fokussierten Parent-Branch, Commit, Push und Draft
PR, verbot aber explizit einen Merge. PR #60 bleibt ein Draft. Der
Delivery-Status ist pending, bis lokaler, Remote- und PR-Head des SonarQube-
Follow-up exakt übereinstimmen und CI-, CodeQL-, SonarQube-Cloud-, Review- und
Revalidation-Fakten beobachtet sind. Der gewünschte Terminal-Status ist
verified_pr, nicht Merge.
