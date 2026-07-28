# Change Record: Parent-Python-Generator-Conditionals für SonarQube Cloud python:S3358

**Sprache:** [English](CR-20260727-sonar-generator-conditionals.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-generator-conditionals |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent-SonarQube-Cloud-Code-Smell `python:S3358`. Die lokale Evidence des ursprünglichen Kandidaten ist unten festgehalten; die normale Aktualisierung auf den aktuellen Master erzeugt einen neuen exakten Head, der eine eigene Hosted-Analyse benötigt. |
| Grenze | Parent-Conditional-Refactoring in `ci/lib/generated_report_utils.py` und `scripts/generate_compiler_guides.py`, die fokussierten vorhandenen Testquellen, dieses englisch/deutsche Paar und seine Indizes. Kein Generated Output, Workflow, keine Konfiguration, kein Framework, kein MRTS und kein Gitlink gehören zum Kandidaten; dieser Record wird nur aktualisiert, um seine PR-Delivery-Statusbeschreibung zu korrigieren. |

## Motivation und Problemstellung

Der Batch behebt die ausgewählten verschachtelten `python:S3358`-
Conditional-Expressions durch explizite `if`/`elif`/`else`-Branches. Ziel ist,
die Auswahl von Provenance-Status und Guide-Notes besser lesbar zu machen,
ohne ihr beobachtbares Verhalten zu ändern.

## Akzeptanzkriterien

- Die Framework-Provenance-Status `not_a_gitlink`, `matches_checkout` und
  `checkout_mismatch` für dieselben Eingaben bewahren.
- Die Compiler-Guide-Package-Note-Auswahl für Envoy und Traefik, den leeren
  Fallback für andere Connectors und das bestehende `http_note`-
  Override/Default-Fallback-Verhalten bewahren.
- Generated Guide Output, Workflows, Konfiguration, Framework, MRTS, Gitlinks
  und Delivery unverändert lassen.
- Die exakte Basis, die übergebene lokale Validierungsquittung,
  Einschränkungen und die erforderliche frische Exact-Head-Sonar-Analyse in
  diesem vollständigen englisch/deutschen Paar und seinen Indizes festhalten.

## Implementierungsentscheidung und Begründung

`framework_provenance()` weist `gitlink_status` jetzt in einem expliziten
Branch zu, bevor dasselbe Metadaten-Dictionary zurückgegeben wird: Ein
unbekannter aufgezeichneter Gitlink ist `not_a_gitlink`, ein gleicher Checkout
ist `matches_checkout`, und jeder andere aufgezeichnete Gitlink ist
`checkout_mismatch`.

`expanded_guide()` wählt zuerst das bestehende englisch/deutsche
Package-Note-Paar für `envoy` oder `traefik` beziehungsweise das bestehende
leere Paar für alle anderen und übergibt es danach an `localized()`.
`source_first_guide()` behält ebenso das bestehende `info["http_note"]`-
Override bei und verwendet dieselbe ausschließlich Loopback betreffende
Default-Note, wenn dieser Key fehlt. Diese expliziten Branches bewahren
Framework-Provenance-Status und Guide-Output-/Fallback-Semantik; sie
regenerieren oder bearbeiten keinen Generated Guide.

## Geänderte Dateien

- ci/lib/generated_report_utils.py
- scripts/generate_compiler_guides.py
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md
- dieses englisch/deutsche Change-Record-Paar

## Tests und tatsächliche Ergebnisse

- Eine frühere übergebene fokussierte Quittung meldete 100 Tests: 21
  Compiler-Guide-Tests, 5 Framework-Provenance-Tests und 74 Generated-Report-
  Evidence-Integrity-Tests. Ihre exakte Invocation und Dauer sind nicht
  erhalten, daher werden sie dieser früheren Quittung nicht zugeschrieben.
- Die finale lokale Validierung erweiterte das Provenance-Modul auf seine
  vollständigen 13 Tests und bestand insgesamt 108 Tests: 21 Compiler-Guide-,
  13 Connector-Capabilities- und 74 Generated-Report-Evidence-Integrity-
  Tests.
- Der finale begrenzte `git diff --check`, die bytecodefreie Syntaxkompilierung
  und der bilinguale Dokumentationscheck bestanden, nachdem dieses Paar und
  beide Indexeinträge ergänzt waren.

## Ausgeführte Befehle

- `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1`
  `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v`
  `tests.test_compiler_guides tests.test_connector_capabilities`
  `tests.test_generated_report_evidence_integrity` bestand 108 Tests in
  22.348s.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 make`
  `check-bilingual-docs` bestand, nachdem dieser Record vollständig war.
- `git diff --check` und die bytecodefreie `py_compile`-Prüfung beider
  geänderter Python-Quellen bestanden.

## Security-Auswirkung

Dies ist ein verhaltensbewahrendes Lesbarkeitsrefactoring in einem
Provenance-/Evidence-Pfad und einem Guide-Generator. Es bewahrt die bestehenden
Framework-Provenance-Statuswerte, Guide-Note-Auswahl und Guide-Fallback-
Semantik; es fügt kein neues unzuverlässiges Input-, Command-, Filesystem-,
Network-, Credential-, Authorization- oder Isolation-Verhalten hinzu. Kein
Security-Control wird geschwächt, und dieser Record behauptet kein
Security-Finding.

## Runtime-Evidence

Es liefen kein Compiler-, Package-, Connector-, Framework-, MRTS-, Generator-
oder Host-Runtime-Lauf. Die fokussierte Test-Evidence ist lokale Unit-Test-
Evidence und keine Runtime- oder externe Sonar-Evidence.

## Nicht ausgeführte Prüfungen mit Begründung

- Es wurde kein Generated Guide Output als neue Ausgabe regeneriert oder
  verglichen, weil Generated Output ausdrücklich außerhalb dieses
  Refactoring-/Documentation-Scopes liegt.
- Nach einem ausschließlich lesenden Checkout der im Parent festgeschriebenen
  Framework-Revision bestand `make check-doc-links` gemeinsam mit
  `make check-bilingual-docs`. Der frühere Kandidat wurde später zu Draft PR
  #140; sein früherer head-spezifischer Hosted-CI-/Sonar-/Review-Status wird
  daher nicht mehr als nicht ausgeführt dargestellt. Diese normale
  Current-Master-Aktualisierung erzeugt einen anderen Head; für ihn wird hier
  kein frisches Hosted-, Review- oder Merge-Ergebnis behauptet.

## Bekannte Einschränkungen

Die ursprüngliche Source-Basis ist
`1b0f8825f3510b99b603bb6cd6f0777e1710358e`; der Kandidat ist jetzt Draft PR
#140 und erhält eine normale Current-Master-Aktualisierung. Das 108-Test-
Ergebnis ist nur fokussierte lokale Evidence; es belegt kein Ergebnis für den
aktualisierten exakten Head, kein Runtime-Ergebnis, kein Review und kein
Delivery-Ergebnis.

## Verbleibende Risiken

Die Status- und Guide-Branches speisen Provenance-/Evidence-Handling und
gerenderte Documentation. Bestehende fokussierte Testabdeckung stützt die
semantische Bewahrung, aber jede spätere Source-, Documentation- oder
Commit-Änderung erzeugt einen anderen Head. Eine frische SonarQube-Cloud-
Analyse für den exakten Delivered Head bleibt erforderlich, bevor der
`python:S3358`-Befund als extern aufgelöst gelten kann.

## Finaler Diff- und Review-Status

Der Kandidat ist ein offener Draft-PR. Kein Generated Output, Workflow, keine
Konfiguration, kein Framework, kein MRTS und kein Gitlink gehören dazu. Dieser
Record behauptet kein Merge- oder anderes Delivery-Ergebnis; eine frische
Exact-Head-Hosted-Analyse bleibt nach der Current-Master-Aktualisierung
erforderlich.
