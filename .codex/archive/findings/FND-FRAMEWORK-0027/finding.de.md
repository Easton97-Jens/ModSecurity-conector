# FND-FRAMEWORK-0027 — Framework-Common-Version-Checker lässt freigegebene ModSecurity-v3-Provenance-Literale aus

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-FRAMEWORK-0027 |
| Kategorie | ci_failure |
| Repository / Ownership | framework / framework |
| Priorität / Severity | P1 / not_applicable |
| Konfidenz / Status | validated / verified |
| Feasibility | feasible_now |
| Release-Blocker | false |
| Sicherheitsrelevant | true |

## Zusammenfassung, Beobachtung, erwartetes Verhalten und Auswirkung

Der aktuelle Common-Version-Workflow auf Framework-master schlägt fail-closed
fehl, weil sein Parser literale freigegebene Provenance-Werte nur für
CRS-Variablen akzeptiert. Dadurch lässt er die geprüften ModSecurity-v3-Literale
für Repository, Commit und Release-Tag aus, bevor er die Alias-Defaults
auflöst, die der Checker validiert.

Der geplante Framework-Workflow-Run 29728340118 auf master
efdbcbd98afeed0f39f8912ce1140aaa5742f507 endet in
check-common-versions mit Exit 2; MODSECURITY_REPO_URL, MODSECURITY_GIT_REF,
MODSECURITY_V3_GIT_URL und MODSECURITY_V3_GIT_REF sind leer. Derselbe Fehler
reproduziert sich lokal:

~~~
python3 ci/tools/check-common-versions.py --check --json --timeout 20
~~~

Der Checker muss die vorhandene geprüfte literale ModSecurity-v3-Identität vor
dem Auflösen der Aliase auflösen und fehlende getrackte Provenance-Variablen
weiterhin fail-closed behandeln. Der geplante Check soll bestehen, wenn die
freigegebene common.sh-Identität vorhanden und aktuell ist.

Der verpflichtende Version-Provenance-Check auf Framework-master ist rot,
obwohl die gepinnte Identität vorhanden ist. Das blockiert die
Current-Master-Readiness und verdeckt einen realen Missing-Provenance-Fall
hinter einem Parserdefekt. Der Defekt ist sicherheitsrelevant, weil der Checker
ein Supply-Chain-Provenance-Control ist; er schlägt jedoch fail-closed fehl und
belegt keinen aktiven Provenance-Bypass.

## Scope, Voraussetzungen, Reproduktion und Evidence

Betroffene Framework-Dateien und Symbole:

- ci/tools/check-common-versions.py: parse_common_assignment und parse_common.
- ci/lib/common.sh: MODSECURITY_V3_APPROVED_REPO_URL,
  MODSECURITY_V3_APPROVED_COMMIT, MODSECURITY_V3_RELEASE_TAG und die vier
  abhängigen Repository-/Ref-Aliase.

Die Reproduktion erfordert Framework-Source auf
efdbcbd98afeed0f39f8912ce1140aaa5742f507, wo common.sh die drei
freigegebenen literalen Identitätswerte definiert und der Checker die vier
Aliase darüber auflöst.

1. Den fehlgeschlagenen GitHub-Actions-Run 29728340118, Check
   check-common-versions, für diesen Master-SHA lesen.
2. In einem isolierten Worktree auf diesem SHA den obigen Befehl mit
   task-eigenem externem BUILD_ROOT und State-Pfaden ausführen.
3. Exit-Code 2 und die vier leeren ModSecurity-Repository-/Ref-Variablen
   beobachten.
4. parse_common_assignment inspizieren: Sein Literal-Zweig akzeptiert
   CRS_APPROVED_* und CRS_RELEASE_TAG, aber nicht MODSECURITY_V3_APPROVED_*.

Aufbewahrte Evidence:

- Run: 20260720T080314Z-parent-pr55-57-59-framework-update-3443af13
- Artifact:
  /var/tmp/codex/ModSecurity-conector/runs/20260720T080314Z-parent-pr55-57-59-framework-update-3443af13/evidence/framework-common-version-parser/reproduction.json
- Typ: framework_common_version_parser_reproduction
- SHA-256: 5b5bfe2c6ecff48658b948e3bcfaac9f1a80c7ac3d91cfb56f1a73c342ca8174
- Command: python3 ci/tools/check-common-versions.py --check --json --timeout 20;
  GitHub-Actions-Failed-Log-Readback für Run 29728340118
- Working directory: /var/tmp/codex/worktrees/framework-common-version-parser
- Exit-Code: 2
- Beobachtet: 2026-07-20T09:01:13Z
- Retention: retained
- Ergebnis: Vier Aliase sind leer, obwohl common.sh die drei freigegebenen
  literalen Provenance-Anker enthält.

## Ursachenanalyse und vorgeschlagene Remediation

parse_common_assignment beschränkt literale Zuweisungen auf CRS_APPROVED_* und
CRS_RELEASE_TAG. MODSECURITY_V3_APPROVED_REPO_URL,
MODSECURITY_V3_APPROVED_COMMIT und MODSECURITY_V3_RELEASE_TAG fehlen deshalb
in der Resolver-Map; die Alias-Defaults werden gegen fehlende Anker aufgelöst
und leer.

Nur die explizite Approved-Literal-Allowlist um die drei Identitätsnamen
MODSECURITY_V3_APPROVED_* erweitern. Eine fokussierte Literal-und-Alias-
Regression hinzufügen. Aliase nicht als optional markieren, die Validierung
getrackter Variablen nicht lockern, keine common.sh-Provenance-Pins ändern und
MRTS nicht verändern.

## Akzeptanzkriterien und Validierungsplan

- [x] Der Parser löst alle drei Literal-Anker MODSECURITY_V3_APPROVED_* und
  alle vier abhängigen Aliase aus einer fokussierten Fixture auf.
- [x] validate_entries meldet für eine Fixture mit freigegebenen Literalen und
  Alias-Defaults keine fehlende Variable.
- [x] Eine Fixture ohne freigegebene Anker lässt erforderliche Aliase weiter
  leer und wird durch die bestehende fail-closed-Validierung abgewiesen.
- [x] Die Reproduktion des Kandidaten endet nicht mehr mit Exit 2 wegen
  fehlender ModSecurity-Provenance-Variablen.
- [x] Es ändern sich keine Optional-Variable-Liste, kein Provenance-Pin, keine
  Sonar-Einstellung, keine Parent-Datei und keine MRTS-Datei.

Den fokussierten Common-Version-Provenance-Unit-Test ohne Bytecode-Schreiben,
Python-Syntax-Kompilierung für den Checker, den Framework-ModSecurity-v3-
Provenance-Contract mit externen task-eigenen Pfaden und eine abschließende
fokussierte Security-Review ausführen. Ein späterer Framework-Draft-PR muss
Exact-Head-CI-, CodeQL-, Sonar-, Review- und Konversations-Evidence sammeln.

## Lokale Remediation und beobachtete Validierung

Der isolierte Framework-Task-Branch auf Basis von
`efdbcbd98afeed0f39f8912ce1140aaa5742f507` verwendet nun eine explizite
Allowlist für die vorhandenen CRS-Namen und die drei freigegebenen
ModSecurity-v3-Literal-Anker. Er leitet die ModSecurity-v3-Release-Prüfung
außerdem über einen Provenance-Wrapper: Ein neuerer Tag bleibt als `unknown` /
manuelle Review sichtbar und erzeugt keinen automatischen Update-Plan, solange
keine geprüfte Tag-zu-Immutable-Commit-Änderung vorliegt.

Beobachtete Kandidatenvalidierung im Source-Run
`20260720T080314Z-parent-pr55-57-59-framework-update-3443af13`:

- die fokussierte Common-Version-Provenance-Suite bestand 15 Tests;
- Python-Kompilierung bestand;
- `make test-modsecurity-v3-provenance-contract` bestand 10 Tests mit
  task-eigenen externen Pfaden;
- der nicht schreibende Befehl `--check --json --timeout 20` endete mit Exit 0,
  ohne fehlende erforderliche Variablen und ohne ModSecurity-v3-Update-Plan;
- `make check-bilingual-docs`, `make check-documentation` und `make lint`
  bestanden; und
- unabhängige Source-Security-Review und Folgeprüfung fanden keinen Bypass,
  keine Berechtigungserweiterung und keine MRTS-Änderung.

Die schreibende geplante Variante `--update --markdown --write-files` wurde
nicht gegen kanonisches common.sh ausgeführt. Sie ist für den korrigierten
nicht schreibenden Control nicht erforderlich und würde kanonischen Source
unnötig mutieren.

Framework-Draft-PR [#36](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/36)
liefert nun Exact-Head-gehostete Evidence für
`2bf862e1a5f262251043ec421447f6e4db11e17d` gegen Basis
`efdbcbd98afeed0f39f8912ce1140aaa5742f507`: Er ist offen, Draft und
mergeable `CLEAN`. Alle 14 terminalen Checks sind aktuell: 11 bestanden
(einschließlich CodeQL Actions/Python/C++, SonarCloud Code Analysis,
PR-Head/Range, scaffold-lint und common-structure); 3 Advisory-Checks sind
erwartete Skips; keiner schlug fehl, wurde abgebrochen oder ist noch pending.
Es wurden keine Reviews oder ungelösten Review-Threads beobachtet.

Post-Merge-Lifecycle-/Evidence-Ereignis vom `2026-07-20T13:10:07Z`: PR #36
wurde am `2026-07-20T13:06:39Z` normal als Framework-master
`784977615acfc55567e37b863309abc4a38ac877` gemergt. Der aktualisierte PR-Head
`1608352912a755f0f8639eddfa2350436446067e` ist ein Vorfahr und sein Tree ist
identisch mit diesem Master. Frische gehostete Evidence für genau diesen Head
bestand: CodeQL Actions, Python und C++; OSV; OpenSSF; Secret Scanning; lint;
test-common; und das PR-SonarQube-Cloud-Quality-Gate mit 0 neuen Issues, 0
Security Hotspots und 0.0% Duplikation. Es wurden keine menschlichen Reviews,
Review Requests oder ungelösten Review-Threads beobachtet. Resultierende
Master-CodeQL-Actions-/Python-/C++-, lint-, test-common- und OpenSSF-Checks
bestanden ebenfalls. Der getrennte Master-Sonar-Check scheiterte nur mit
geerbtem FND-SONAR-0002 Security E unter der abgegrenzten master-only-
Akzeptanz des aktuellen Nutzers; diesem Finding wird keine Kausalität
zugeschrieben.

Das aufbewahrte isolierte Exact-Master-Original-Reproduktionsartefakt
`analysis/pr36-master-common-version-original-reproduction.json`
(SHA-256 `4d2311ab1287b3943633b5f9d5243451ad697d66726d6a6d57012b3fae7eb1ab`)
erfasst Exit-Code 0 für `--check --json --timeout 20`: `missing_required` ist
leer und alle freigegebenen ModSecurity-v3-Anker und abhängigen Aliase lösen
auf. Es erfasst außerdem v3.0.15 gegenüber v3.0.16 als `unknown` / manuelle
Review mit leerer Update-Liste. Der Befehl verwendete nur `--check` und führte
weder `--update`, `--markdown` noch `--write-files` aus. Die früheren lokalen
Parser-15/15-, Provenance-Contract-10/10-, `py_compile`-, Bilingual-/
Documentation- und Diff-Checks bleiben Teil der Exact-Head-Evidence. Die
getrennte FND-SONAR-0002-Akzeptanz hebt keinen frischen PR-Head-Check, kein
PR-Sonar-Gate, Review-, Berechtigungs- oder Security-Control auf.

## Regressions- und Legitimate-Control-Tests

Regressionstests:

- tests/security_regression/test_common_versions_sonar_provenance.py
- make test-modsecurity-v3-provenance-contract

Legitimate Controls:

- Ein fehlender freigegebener Anker bleibt durch validate_entries fail-closed.
- Das vorhandene freigegebene ModSecurity-v3-Repository, der Commit und der
  Release-Tag bleiben die aufgelöste Quelle der Aliase.
- Allein das Parsen der Fixture verursacht keinen Network-Lookup.

## Abhängigkeiten, Grenzen, verwandte Findings und Restrisiko

Die historischen Exact-Head- und aktuellen Exact-Master-Controls erfüllen nun
die Source-Validierungsabhängigkeit dieses Findings. Upstream-Verfügbarkeit
bleibt eine legitime Runtime-Abhängigkeit der Common-Version-Checks. Der
getrennte Framework-Master-Sonar-Blocker FND-SONAR-0002 bleibt global blocked;
seine aktuelle abgegrenzte master-only-Akzeptanz ermöglichte die geschützte
#36-Delivery, schwächt, ersetzt oder eröffnet jedoch die Controls dieses
Findings nicht erneut.

Dieses Finding ist kein Duplikat von FND-FRAMEWORK-0001, dessen test-common-
und common-structure-Fehler eine andere Ursache haben, oder FND-SONAR-0002,
das das unabhängige Current-Master-Sonar-Gate besitzt. FND-FRAMEWORK-0028
besitzt separat den partiellen Auto-Update-Pfad, der nach dem Auflösen der
freigegebenen Literale erreichbar wird.

Die normale Framework-Master-Delivery erfolgte ohne Parent-Datei oder
Parent-Gitlink-Update und ohne MRTS-Inhalts- oder Git-Aktion. Das Bestehen
dieser Korrektur und des PR-Head-SonarCloud-Checks löst nicht das separate
Framework-Master-Sonar-Gate.

Eine künftige Änderung des common.sh-Layouts oder der Provenance-Namen erfordert
eine explizite Parser-Review. Die Korrektur muss auf die freigegebenen
ModSecurity-v3-Identitätsnamen beschränkt bleiben, damit beliebige Literale
nicht in den getrackten Resolver gelangen.

## Aktuelle Delivery-Disposition

Dieses Finding ist `verified`, nicht `closed` oder risikoakzeptiert. PR #36
wurde normal als exakter Framework-master
`784977615acfc55567e37b863309abc4a38ac877` gemergt; sein Tree entspricht dem
aktualisierten Head `1608352912a755f0f8639eddfa2350436446067e`, und die
ursprüngliche Missing-Approved-Literal-Reproduktion sowie Legitimate Controls
bestanden auf diesem Master. FND-SONAR-0002 bleibt ein separates blocked
Framework-Master-Issue mit abgegrenzter master-only-Akzeptanz; es verändert
weder den verified-Status dieses Findings noch hebt es seine PR-Controls auf.
Es erfolgte keine Parent-Gitlink- oder MRTS-Aktion.

## Historie

- 2026-07-20T09:01:13Z — confirmed_and_remediation_started: Der geplante
  Master-Check und die fokussierte isolierte lokale Kontrolle endeten beide mit
  Exit 2, weil der Parser die literalen Provenance-Anker
  MODSECURITY_V3_APPROVED_* ausließ. Eine enge Parser- und
  Regressionstest-Remediation wurde autorisiert; es gab keine Parent-,
  Framework-Master- oder MRTS-Git-Aktion.
- 2026-07-20T09:36:58Z — local_remediation_validated: Der Task-Branch löst nur
  die vorgesehenen freigegebenen Literale auf, bewahrt das fail-closed-Verhalten
  für fehlende Anker und besteht die fokussierten Provenance-Contract-,
  Dokumentations- und Framework-Lint-Controls. Der separate Draft-PR und
  Exact-Head-gehostete Evidence bleiben ausstehend; es gab keine Framework-
  Master-, Parent- oder MRTS-Git-Aktion.
- 2026-07-20T10:14:31Z — fixed_on_framework_pr_36_exact_head_validated:
  Draft-PR #36 Exact Head `2bf862e1a5f262251043ec421447f6e4db11e17d`, basierend
  auf `efdbcbd98afeed0f39f8912ce1140aaa5742f507`, ist mergeable CLEAN mit 11
  erfolgreichen und 3 expected-skipped terminalen Checks sowie ohne
  fehlgeschlagenen/pending Check, Review oder ungelösten Review-Thread.
  Master-Merge, Current-Master-Reproduktion, Parent-Gitlink und MRTS-Aktionen
  bleiben out of scope.
- 2026-07-20T13:10:07Z — verified_on_framework_master_after_pr_36_normal_merge:
  PR #36 wurde am `2026-07-20T13:06:39Z` normal als Framework-master
  `784977615acfc55567e37b863309abc4a38ac877` gemergt; exakter Head
  `1608352912a755f0f8639eddfa2350436446067e` ist ein Vorfahr mit einem zu
  Master identischen Tree. Frische PR-Head-Controls und resultierende
  Master-CodeQL-Actions-/Python-/C++-, lint-, test-common- und OpenSSF-Checks
  bestanden. Das aufbewahrte Exact-Master-Artefakt
  `analysis/pr36-master-common-version-original-reproduction.json` (SHA-256
  `4d2311ab1287b3943633b5f9d5243451ad697d66726d6a6d57012b3fae7eb1ab`) erfasst
  Exit 0, keine fehlende Required Variable und alle aufgelösten freigegebenen
  Anker und Aliase. Das Master-Sonar Security E ist das getrennte geerbte
  FND-SONAR-0002-Gate unter einer abgegrenzten Akzeptanz, keine kausale
  Disposition dieses Findings; es erfolgte keine Parent-Gitlink- oder
  MRTS-Aktion.
