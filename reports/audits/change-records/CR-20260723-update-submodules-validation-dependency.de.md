# Change Record: Reparatur der read-only Update-Submodules-Validierungsabhängigkeit

**Sprache:** [English](CR-20260723-update-submodules-validation-dependency.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260723-update-submodules-validation-dependency |
| Datum (UTC) | 2026-07-23 |
| Basis-Revision | ad953cdcbc8c05ede519661ca56c03cf7b1ac7f3 |
| Grenze | Parent-`Update submodules`-read-only-Validierungsworkflow, sein Parent-static-CI-Security-Contract, ein CI-only-PyYAML-Hash-Lock, dieses englische/deutsche Change-Record-Paar und beide Change-Record-Indizes. Framework-Source, MRTS, Parent-Gitlink, die Development-Dependency-Deklaration, Action-Pins, Berechtigungen und Publisher-Verhalten bleiben unverändert. |
| Finding-Verknüpfung | FND-PARENT-0048: aktuelle fehlende Validierungsvoraussetzung; FND-PARENT-0045: vorherige Parent-HAProxy-Fixture-Reparatur, die auf eine erfolgreiche Hosted-Candidate-Validierung wartet. |
| Delivery-Status | Der Draft-Parent-[PR #92](https://github.com/Easton97-Jens/ModSecurity-conector/pull/92) trägt die Korrekturserie. Sein erster Head zeigte die als FND-PARENT-0049 erfasste YAML-Scalar-Regression. Der quotierte-Scalar-Amendment-Head `a9af868d0723b6c35c14f35dc733dbbcb1896a25` schloss GitHub-Actions-Checks terminal erfolgreich oder erwartungsgemäß übersprungen ab und bestand das SonarQube-Cloud-Quality-Gate mit null neuen Issues. Dieses Record behandelt die Evidence des vorherigen PR-Heads nicht als Merge- oder Resulting-Master-Verifikation; der PR bleibt Draft. |

## Motivation und Problemstellung

Der Nutzer autorisierte einen separaten PR, um die ausstehende
`Update submodules`-Reparatur fertigzustellen. Der einzelne autorisierte
Current-Master-Workflow-Run
[29981644356](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29981644356)
löste den aktuellen Framework-Candidate auf und führte seine read-only-
Checkout- und Interpreter-Controls aus, doch `make quick-check` scheiterte,
weil der Fixture-Syntax-Checker die bereits deklarierte Abhängigkeit
`PyYAML>=6,<7` nicht importieren konnte. Der enge Publisher wurde korrekt
übersprungen.

## Akzeptanzkriterien

- Der read-only-Validator installiert seinen unveränderlichen CI-only-PyYAML-
  Lock nach seinem Interpreter-Vertrag und vor `make quick-check`.
- Statische CI-Security-Coverage sichert Befehl und Reihenfolge ab und bewahrt
  den Resolver → read-only-Validator → enger-Publisher-Control-Flow.
- Die Korrektur verwendet `--require-hashes` und `--only-binary=:all:` gegen
  das exakte Linux-x86_64-Artifact; sie ändert weder die plattformübergreifende
  Development-Dependency-Deklaration noch Action-Pins, Berechtigungen,
  Secrets, Framework-/MRTS-Inhalte oder den Parent-Gitlink.
- Fokussierte Tests, CI-Security-Contract, Security-Diff-Review,
  Whitespace-Check und Exact-Head-PR-Checks werden wahrheitsgemäß erfasst.
- Diese Aufgabe öffnet nur einen PR; der master-only-Workflow wird nicht als
  PR-Head-Validierung dargestellt und es findet kein Merge statt.

## Implementierungsentscheidung und Begründung

Der Workflow ruft nun das Pip-Modul des gewählten Python-Interpreters mit einem
von der bestehenden Development-Deklaration abgeleiteten CI-only-Lock vor der
Candidate-Validierung auf. Der Lock nennt PyYAML 6.0.3 und die SHA-256 des
offiziellen Linux-x86_64-Wheels; Pip akzeptiert nur ein Binärartifact mit
diesem Hash. Damit wird die neue Package-Acquisition-Grenze geschlossen, ohne
die plattformübergreifende Development-Deklaration zu ändern, ein lokales
Environment anzulegen oder ein breiteres Setup-Target zu verwenden. Der Schritt
bleibt im `contents: read`-Validator, hat kein explizit injiziertes Secret oder
schreibfähiges Token, und der statische Contract bindet ihn zwischen `Verify
Python interpreter contract` und `make quick-check`. Er verhindert sowohl die
Missing-Prerequisite-Regression als auch unpinned-/Source-Build-Fallbacks,
ohne das Publisher-Gate zu schwächen.

## Geänderte Dateien

- `.github/workflows/update-submodules.yml`: Installation der hash-gelockten
  Validierungsabhängigkeit im read-only-Validator.
- `ci/requirements/update-submodules-validation-linux-x86_64.txt`: CI-only-
  PyYAML-6.0.3-Binär-/Hash-Lock für den GitHub-hosted-Linux-x86_64-Validator.
- `tests/test_ci_security_workflows.py`: Assertion für den Dependency-
  Installationsbefehl, Lock-Identität, Hash und seine erforderliche Reihenfolge.
- Dieses englische/deutsche Change-Record-Paar und beide Change-Record-Indizes.

Keine Framework-Source, kein MRTS, Parent-Gitlink, plattformübergreifende
Development-Dependency-Deklaration, Action-Pin, Workflow-Berechtigung, Secret
oder Publisher-Code wird geändert.

## Ausgeführte Befehle

- Hosted-Diagnose: Run `29981644356` erreichte den exakten Parent-Master
  `ad953cdcbc8c05ede519661ca56c03cf7b1ac7f3`; Resolver, Checkout, Python-
  Contract und Candidate-Checkout bestanden, während `make quick-check` mit
  Exit 2 bei `check-framework-fixture-syntax` und `PyYAML is required for
  fixture syntax lint` scheiterte. Der Publisher wurde übersprungen.
- Lokale Validierung bestand: der fokussierte Update-Submodules-Workflow-
  Security-Test, `make check-ci-security-contract` (16 Tests) und die
  fokussierte bilinguale Dokumentationssuite (11 Tests). `pip check`, der
  Vergleich der offiziellen PyPI-Metadaten für den gelockten Wheel-Hash und
  `git diff --check` bestanden ebenfalls.
- `make check-bilingual-docs` bleibt wegen bekannter fehlender verlinkter
  Dateien unterhalb des nicht initialisierten Framework-Submoduls blockiert;
  kein Framework-Inhalt wurde geändert, und der fokussierte englisch/deutsche
  Paar-Test bestand.
- Hosted-PR-Evidence für den quotierten-Scalar-Amendment-Head
  `a9af868d0723b6c35c14f35dc733dbbcb1896a25` schloss mit terminal erfolgreichen
  oder erwartungsgemäß übersprungenen GitHub-Actions-Checks ab. SonarQube Cloud
  bestand das Quality Gate mit null neuen Issues und null Security Hotspots.
  Dies ist nur PR-Head-Evidence und kein master-only-`Update submodules`-Run.

## Security-Auswirkung

Der Resolver validiert einen vollständigen offiziellen SHA, Candidate-Code läuft
nur im read-only-Validator, und der isolierte Writer bleibt an erfolgreichen
Validierungsabschluss gebunden und validiert den offiziellen SHA erneut, bevor
er nur den Gitlink ändert. Die neue Pip-Grenze ist auf den zugelassenen
Linux-x86_64-Wheel-Hash von PyYAML 6.0.3 beschränkt und weist Source-
Distributionen zurück. Keine Berechtigung, Credential, Secret, Action-Pin,
Candidate-Scope oder Publisher-Pfad wird erweitert. Der fokussierte
Supply-Chain-Security-Diff-Review der CI-Korrektur ist mit vollständiger
Source-Coverage und null berichtspflichtigen Findings abgeschlossen. Ein
finaler Source-Diff-Review deckt vor dem Commit auch die begleitende
Dokumentationsformulierung ab.

## Runtime-Evidence

Nicht anwendbar. Dies ist eine GitHub-Actions-Voraussetzungs-/Contract-
Reparatur; sie baut oder startet keinen Connector und etabliert keinen HTTP-,
H2-, H3- oder Runtime-Claim.

## Bekannte Einschränkungen

Das plattformübergreifende `requirements-dev.txt` deklariert weiterhin den
begrenzten PyYAML-Range für lokale Entwicklung. Der CI-only-Lock unterstützt
absichtlich den aktuellen GitHub-hosted-Linux-x86_64-CPython-3.14-Validator und
schlägt bei einem Plattformwechsel fail-closed fehl, bis ein ausdrückliches
Lock-Update geprüft ist. Der Hosted-`Update submodules`-Workflow checkt
absichtlich `master` aus und kann den neuen PR-Head daher vor einer separat
autorisierten Integration nicht beweisen.

## Verbleibende Risiken

Bis ein separat autorisierter Merge und ein Current-Master-Workflow-Rerun
erfolgreich sind, bleibt die automatisierte Framework-Candidate-
Veröffentlichung blockiert. Die bestehenden fail-closed-Validierung und enge
Publisher-Isolierung verhindern Veröffentlichung bei einem Fehler. Kein Risiko
wird akzeptiert.

## Nicht ausgeführte Prüfungen mit Begründung

- Keine lokale Pip-Installation: Eine Installation in Parent-`.venv`, System-
  Python oder User-Site liegt außerhalb dieser Aufgabe und ist für einen
  statischen Workflow-Contract-Test unnötig.
- Ein frischer `Update submodules`-Erfolg ist gegen diesen PR-Head nicht
  ausführbar, weil der Workflow absichtlich `master` auscheckt; er bleibt bis
  zu einem separat autorisierten Merge ausstehend.
- Kein master-only-`Update submodules`-Run, Merge, Framework-Candidate-PR,
  Gitlink-Update oder Resulting-Master-Verifikation wurde angefordert oder
  durchgeführt. Hosted-PR-Head-Ergebnisse bleiben im Draft-PR erhalten und
  müssen für jeden späteren PR-Head erneut bewertet werden.

## Finaler Diff- und Review-Status

Der Source-Diff ist bewusst auf den read-only-hash-gelockten Setup-Befehl,
seine statische Regression und vollständige bilinguale Traceability begrenzt.
Lokale Validierung, der fokussierte Security-Diff-Review, die Exact-Head-
Checks des quotierten-Scalar-Amendments und der finale Exact-Diff-Review sind
für das dokumentierte Amendment abgeschlossen. Der Draft-PR bleibt dem
normalen Review unterworfen; jeder spätere Head benötigt eigene Exact-Head-
Evidence. Kein Master-Change, Candidate-PR, Framework-/MRTS-Aktion, Gitlink-
Update oder Branch-Cleanup ist erfolgt.
