# Change Record: Python-3.14.6- und Go-1.26.5-Toolchain-Baseline

**Sprache:** [English](CR-20260721-python314-go1265-toolchain-baseline.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260721-python314-go1265-toolchain-baseline` |
| Datum (UTC) | `2026-07-21` |
| Basis-Revision | `2ade0d40983b7af21a65b8cd2884866b85626393` |
| Grenze | Nur Parent-Python-/Go-Toolchain-Deklarationen, eingecheckte CI-Verträge, Parent-Tests, generierte Parent-Dokumentation und dieses Change-Record-Paar; Framework, MRTS, beide Gitlinks, Abhängigkeiten und historische Change Records bleiben unverändert. |
| Finding-Verknüpfung | `FND-PARENT-0044` (lokaler kanonischer Finding-Record): beobachteter Parent-CI-Sicherheitsvertragsblocker durch eine veraltete Python-Checker-Erwartung. Der reproduzierte Befehl und sein Ergebnis sind unten erfasst. |
| Delivery-Status | Lokale Candidate-Verifikation abgeschlossen. Dieser Record behauptet keinen Commit, Push, Pull Request, Remote-CI, Review, SonarQube-Cloud-Erfolg oder Master-Integration. |

## Motivation und Problemstellung

Der Parent deklarierte die exakten Baselines Python `3.13.14` und Go
`1.24.13`. Diese Änderung hebt den eingecheckten Python-Vertrag auf `3.14.6`
und die beiden Parent-Go-Module samt ihrer CodeQL-Selektoren auf `1.26.5` an.
Exakte Versionsdeklarationen bleiben erforderlich: Eine floating Minor-Version
würde nicht geprüften Patch Drift erlauben.

Der aktuelle Master enthält außerdem einen beobachteten CI-Sicherheitsvertrags-
Fehler. Alle eingecheckten `actions/setup-python`-Workflow-Verwendungen und
der geprüfte Eintrag in `ci/tooling/security-tools.lock.yml` verwenden bereits
den unveränderlichen
`actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0`;
`check-python-version-contract.py` erwartete jedoch weiterhin v6.3.0. Sein
fail-closed-Ergebnis wies jeden gültigen Python-Setup-Job zurück und verdeckte
die verbleibenden Python-Reihenfolge-Checks. Die Reparatur aktualisiert Checker
und positive/negative Fixtures auf die bereits geprüfte v7-Referenz; sie
ändert weder Workflow-Pin noch Security-Lock-Eintrag.

## Akzeptanzkriterien

- `.python-version` deklariert das exakte stabile `3.14.6`; Updater,
  Interpreter-Checker, Workflow-Checker, Workflow-Metadaten und fokussierte
  Fixtures/Tests akzeptieren nur die Serie `3.14.N`.
- Der Updater bleibt bis zu seinem Default-Branch-gated Publisher
  schreibgeschützt; `automation/update-python-314` und
  `chore(ci): propose Python 3.14 patch update` ersetzen die frühere
  3.13-Identität ohne Änderung von Berechtigungen, Triggern, vertrauenswürdigem
  Checkout oder PR-only-Grenze.
- Der Python-Workflow-Checker akzeptiert exakt die vorhandene unveränderliche
  v7.0.0-Setup-Referenz und weist weiterhin einen veränderlichen Tag,
  verkürzten SHA, falschen Kommentar oder nicht geprüfte Referenz zurück.
- Beide Parent-Go-Module deklarieren `go 1.26.5`, und beide Go-CodeQL-Jobs
  selektieren `go-version: '1.26.5'`.
- Generator-abgeleitete EN/DE-Compiler-Guides, CI-Sicherheitsdokumentation,
  Build-Dokumentation und fokussierte Tests beschreiben dieselben exakten
  Baselines.
- Kein `go.sum`, keine Abhängigkeitsversion, keine `toolchain`-Direktive, kein
  Action-Pin, Security-Lock-Wert, keine Workflow-Berechtigung, kein Trigger,
  Framework-Inhalt oder MRTS-Inhalt ändern sich.
- Exakte Python-`3.14.6`- und Go-`1.26.5`-Runtime-Evidence muss aus einem
  beobachteten Hosted-CI-Lauf für den exakten Delivery-Head vor Verifikation
  oder geschützter Delivery kommen.

## Implementierungsentscheidung und Begründung

Die Implementierung pinnt `3.14.6` und `1.26.5` in ihren bestehenden
autoritativen Dateien. Python verwendet weiterhin `python-version-file:
.python-version`; Go verwendet weiterhin seine Moduldeklarationen und exakten
CodeQL-Setup-Selektoren. Das erhält je Toolchain eine reviewbare Source of Truth.

| Alternative | Disposition | Begründung |
| --- | --- | --- |
| Floating `3.14` oder `1.26` | Abgelehnt | Runner, Tool-Cache oder automatische Auflösung könnten ein nicht geprüftes Patch-Release auswählen. |
| Python `3.13.14` oder Go `1.24.13` beibehalten | Abgelehnt | Das erfüllt die angeforderten neuen Baselines nicht. |
| v7-Workflow-Pin oder Security-Lock ändern, damit der Checker besteht | Abgelehnt | Workflows und Lock stimmen bereits auf der verifizierten unveränderlichen v7-Referenz überein; nur die Checker-Erwartung ist veraltet. |
| Go-`toolchain`-Direktive ergänzen, `go get` ausführen oder Abhängigkeiten aktualisieren | Abgelehnt | Dies ist ein begrenztes Toolchain-Baseline-Update; Änderungen am Dependency-Graph benötigen separate Kompatibilitäts-Evidence. |

Die Python-Contract-Reparatur erfolgt atomar mit dem Versions-Upgrade: Checker,
Fixtures und Tests verwenden dieselbe exakte v7-Referenz wie die bereits
geprüften Workflows und der Lock. Sie stellt den legitimen Control wieder her,
ohne einen Integrity-Fehler in eine Allow-all-Regel umzuwandeln. Go bleibt auf
zwei `go.mod`-Direktiven, passende CodeQL-Selektoren und Generator-
Dokumentation beschränkt.

## Geänderte Dateien

- `.python-version`, `.github/workflows/update-python-version.yml`,
  `scripts/update-python-version.py` sowie die Parent-Python-Interpreter- und
  Workflow-Contract-Checker.
- Fokussierte Parent-Python-Updater-, Interpreter-Contract-, Workflow-Contract-
  und CI-Sicherheits-Tests mit ihren Version-Contract-Fixtures.
- `.github/workflows/ci-security-codeql.yml`,
  `connectors/envoy/ext_proc/go.mod`,
  `connectors/traefik/native_middleware/go.mod` und
  `scripts/generate_compiler_guides.py` mit fokussierten Tests und generierten
  Compiler-Guide-Outputs.
- `docs/build/README.md`, `docs/build/README.de.md`,
  `docs/security/ci-security-tooling.md` und
  `docs/security/ci-security-tooling.de.md`.
- Die Change-Record-Indizes und dieses englische/deutsche Change-Record-Paar.

Framework, MRTS, `go.sum`, historische Python-3.13- und Go-1.24.13-Change
Records, unveränderliche Action-Pins und der Security-Tools-Lock werden nicht
geändert.

## Ausgeführte Befehle

| Befehl oder Evidence | Ergebnis |
| --- | --- |
| `env PYTHON=/root/git/ModSecurity-conector/.venv/bin/python PYTHONDONTWRITEBYTECODE=1 make check-python-version-contract` gegen die Basisrevision | fehlgeschlagen, Exit `2`: Der Checker verlangte `actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1 # v6.3.0` und fand keine exakte Referenz, weil eingecheckte Workflows bereits v7.0.0 verwenden. Dies ist der reproduzierte legitime Blocker. |
| `env PYTHON=/root/git/ModSecurity-conector/.venv/bin/python PYTHONDONTWRITEBYTECODE=1 make check-python-version-contract` auf dem Candidate | bestanden: `Python 3.14.6; 25 Python-executing workflow jobs`. Dies ist derselbe Befehl, der gegen die Basisrevision fehlschlug. |
| Fokussierte Python-Contracts, CI-Security-, Compiler-Guide- und Bilingual-Document-Unit-Suite | bestanden: 98 Tests über `tests.test_update_python_version`, `tests.test_python_interpreter_contract`, `tests.test_python_version_contract`, `tests.test_ci_security_workflows`, `tests.test_compiler_guides` und `tests.test_bilingual_docs`. |
| `make check-ci-security-contract` | bestanden: 15 CI-Security-Tests plus Validate-only-Prüfungen der gepinnten Actionlint-, Zizmor- und Gitleaks-Tool-Records. |
| `make check-compiler-guides` | bestanden: 19 Tests zu generierten Guides, Shell-Form, Links und EN/DE-Parität. |
| `python -m compileall -q ci scripts tests` | bestanden mit dem Repository-Virtual-Environment. |
| `git diff --check` sowie kein Diff für `ci/tooling/security-tools.lock.yml` oder beide `go.sum` | bestanden. Keine Action-Lock-, Module-Integrity- oder Whitespace-Änderung wurde eingeführt. |
| `make check-bilingual-docs` | blockiert, Exit `2`, ausschließlich durch fehlende Link-Ziele unter dem absichtlich nicht initialisierten Parent-Framework-Gitlink. Die fokussierte Bilingual-Document-Unit-Suite und die Compiler-Guide-Paritätschecks bestanden; Framework und MRTS wurden nicht initialisiert oder geändert. |
| `GOTOOLCHAIN=local go test ./...` in jedem tatsächlichen Go-Modul | blockiert, Exit `1`: Lokales Go ist `1.26.0`, während jedes migrierte Modul korrekt mindestens `1.26.5` verlangt. Kein automatischer Toolchain-Download war erlaubt. |
| Exakte lokale Python-`3.14.6`- und Go-`1.26.5`-Runtime-Checks | nicht verfügbar: Lokale Executables sind Python `3.14.4` und Go `1.26.0`; sie können die exakten deklarierten Ziele nicht belegen. |

Exact-Head-Hosted-CI, Review, SonarQube Cloud und geschützte Delivery-Ergebnisse
bleiben pending. Kein unbeobachteter Remote-Check wird als bestanden dargestellt.

## Security-Auswirkung

Dies ist eine CI-Supply-Chain- und Toolchain-Baseline-Änderung. Die v7-
Python-Action bleibt ein offizieller vollständiger unveränderlicher Commit,
der vom geprüften Lock abgedeckt ist. Die Checker-Reparatur stellt seine
Fähigkeit wieder her, diese erlaubte Referenz von veränderlichen, verkürzten
oder fehlerhaften Alternativen zu unterscheiden; keine Berechtigung, kein
Trigger, Lock oder Pin wird geschwächt.

Das Anheben exakter Python- und Go-Deklarationen ändert die von Hosted CI und
Modulen ausgewählten Tools, nicht Connector-Request-Parsing, Autorisierung,
Protokollverarbeitung oder Runtime-Privilegien. Ohne Exact-Head-Evidence wird
nicht behauptet, dass ein bestimmtes Upstream-Toolchain-Advisory erreichbar
oder behoben ist.

## Runtime-Evidence

Nicht anwendbar. Diese Änderung startet keinen Connector, verändert keinen
Connector-Protokollpfad und etabliert keine HTTP/1.1-, HTTP/2-, HTTP/3-, CRS-,
Framework-, MRTS- oder Host-Runtime-Kompatibilitäts-Evidence. Das erforderliche
exakte Toolchain-Ergebnis ist Hosted-CI-Evidence, keine lokale Connector-
Runtime-Evidence.

## Bekannte Einschränkungen

Die lokale Umgebung stellt Python `3.14.4` und Go `1.26.0`, nicht exakt Python
`3.14.6` und Go `1.26.5`, bereit. Sie kann Source-Shapes und Dokumentation
validieren, aber nicht beweisen, dass exakte Hosted-Toolchains alle
fokussierten Python- und Go-Checks ausführen. Der Task-Worktree lässt den
Framework-Gitlink absichtlich nicht ausgecheckt; ein Full-Tree-
Dokumentationscheck muss diese Fremdabhängigkeit berichten, statt Framework
oder MRTS zu verändern.

## Verbleibende Risiken

Eine Python- oder Go-Major/Minor-Baseline-Änderung kann
Kompatibilitätsunterschiede auslösen, die statische Checks nicht offenlegen.
Exact-Head-Hosted-CI, einschließlich Python-Candidate-Validierung,
CodeQL-Go-Setup, fokussierter Python-Tests, Go-Modul-Checks,
Dokumentations-Checks, Reviews und SonarQube Cloud, soweit konfiguriert,
bleiben vor einem verifizierten PR oder einer geschützten Delivery erforderlich.
Kein Risiko wird akzeptiert, versteckt oder durch diesen Record übertragen.

## Nicht ausgeführte Prüfungen mit Begründung

- Exakte Hosted-GitHub-Actions-Ausführung mit Python `3.14.6` und Go `1.26.5`
  wurde nicht beobachtet; sie ist die erforderliche Exact-Toolchain-Evidence.
- Exact-PR-Head-CI, Review/Thread-Status, SonarQube-Cloud-Quality-Gate und
  geschützte Merge-/Master-Checks existieren in diesem In-Progress-Record nicht.
- Connector-Builds und -Runtimes sind nicht gewählt, weil diese begrenzte
  Deklarationsänderung keinen Connector-Runtime-Code verändert; sie sind kein
  Ersatz für die erforderlichen fokussierten CI-Checks.
- Ein Full-Tree-Dokumentations-/Link-Ergebnis kann durch den absichtlich nicht
  initialisierten Framework-Gitlink blockiert sein. Framework und MRTS bleiben
  out of scope.

## Finaler Diff- und Review-Status

Der lokale Diff wurde gegen die erklärte Grenze geprüft: Er ist auf Parent-
Python-/Go-Deklarationen, Version-Contracts/Tests, Generator-geleitete Guides,
gepaarte Dokumentation und dieses Change Record beschränkt. Der ursprüngliche
Checker-Fehler ist nicht mehr reproduzierbar, während mutable, short-SHA,
missing-comment und wrong-comment Setup-Python-Fixtures negative Controls
bleiben. Exact-Head-CI, Review, Delivery-Daten und etwaige
Resulting-Master-Evidence bleiben pending und dürfen erst nach Beobachtung
erfasst werden.
