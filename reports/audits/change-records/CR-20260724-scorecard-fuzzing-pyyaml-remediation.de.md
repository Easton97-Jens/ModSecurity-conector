# Change Record: Scorecard-Fuzzing- und PyYAML-Remediation

**Sprache:** [English](CR-20260724-scorecard-fuzzing-pyyaml-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260724-scorecard-fuzzing-pyyaml-remediation` |
| Datum (UTC) | `2026-07-24` |
| Basis-Revision | `9e788057d2b551ba51ad7c4e6e1d8c5198b77834` |
| Ursprüngliche Source-Basis | `30ee953b57f4aafebaa0e6ed565a80f6500db1de` |
| Grenze | Ausschließlich Parent-Common-HTTP-Header-Helper, der begrenzte C/C++-CodeQL-Job, eine Development-Dependency-Deklaration, fokussierte statische Regression, Leserdokumentation und dieses Change-Record-Paar/Index. Die aufgabeneigene SonarQube-Cloud-S131-Korrektur beschränkt sich auf einen expliziten No-op-`case`-Default im neuen Runner. Framework, MRTS, Gitlinks, GitHub-Settings, Workflow-Berechtigungen und das bestehende Go-Fuzzing bleiben unverändert. |
| Finding-Verknüpfung | `FND-GITHUB-0001`, Scorecard `FuzzingID #11`, Scorecard `VulnerabilitiesID #12` und SonarQube-Cloud-`shelldre:S131`-Issue `AZ-VF2RWRo9R-gan4Xej`. |

## Motivation und Problemstellung

Aktuelle Default-Branch-Scorecard v5.3.0 meldet, dass das Projekt nicht gefuzzt
wird, und meldet zwei PyYAML-Advisory-Familien. Der bestehende begrenzte
Go-Fuzz-Target ist echt, aber die Sprachprominenz-Heuristik von Scorecard scannt
Go in diesem Repository nicht. Die Development-Deklaration `PyYAML>=6,<7`
schließt beide Advisory-Bereiche bereits aus, aber der eingebettete OSV Scanner
interpretiert den zusammengesetzten Specifier als fehlerhafte Literalversion
`6,<7`.

Diese Änderung ergänzt einen echten C/libFuzzer-Target an einer Common-HTTP-
Header-Grenze einer prominenten Sprache und liefert dem Scanner die tatsächliche
sichere PyYAML-Release. Sie unterdrückt keinen Alert und erzeugt keinen
künstlichen Scanner-Erkennungsmarker.

Die SonarQube-Cloud-Analyse des ursprünglichen PR-Heads meldete zusätzlich
S131 für den Containment-`case` des Runners. Der Guard weist bereits
Checkout-interne Build-Roots zurück; sein sicherer nicht passender Pfad ist
absichtlich ein No-op. Ein explizites `*) ;;` macht diesen Pfad vollständig,
ohne Guard, Build-Root oder Scanner-Konfiguration zu ändern.

## Akzeptanzkriterien

- Ein C-Target stellt `LLVMFuzzerTestOneInput` bereit, übt Common-Header-
  Parsing und Log-Sanitization mit beliebigen begrenzten Bytes aus und hält die
  gültigen, fehlerhaften, Overflow- und widersprüchlichen `Content-Length`-
  Kontrollen beobachtbar.
- Der bestehende begrenzte C/C++-CodeQL-Job kompiliert den Target mit C17,
  libFuzzer, AddressSanitizer und UndefinedBehaviorSanitizer und führt ihn
  anschließend mit endlicher Zeit-, Speicher-, Timeout- und Ein-Worker-Grenze
  aus.
- `requirements-dev.txt` löst die exakte sichere Release `PyYAML==6.0.3` auf,
  synchron zum geprüften CI-only-Hash-Lock, ohne OSV-Ignore.
- Fokussierte statische Coverage verhindert, dass der neue Workflow-Aufruf und
  die exakte Dependency-Deklaration stillschweigend verschwinden.
- Der Checkout-Containment-`case` des Runners hat einen expliziten
  `*) ;;`-Default, sodass sein beabsichtigter nicht passender No-op-Pfad
  vollständig ist, ohne die Zurückweisungskontrolle abzuschwächen.
- Englisch/deutsche Leserdokumentation und dieses Change-Record-Paar
  beschreiben dieselbe Grenze und Einschränkungen.
- Es werden weder Alert-Schließung, Merge, direkter Master-Push, GitHub-
  Governance-Änderung, Framework-/MRTS-Aktion noch Full-Service-/Runtime-
  Fuzzing behauptet.

## Implementierungsentscheidung und Begründung

Der Target konstruiert begrenzte `msconnector_header`-Views über libFuzzer-
Eingabe. Er ruft `msconnector_headers_parse_content_length`, Content-Type-
Matching, Kopieren und beide Log-Sanitization-Helper auf. Deterministische
Assertions erhalten die legitime Akzeptanz von `Content-Length: 123` sowie die
Zurückweisung nichtdezimaler, überlaufender und widersprüchlicher doppelter
Werte. Dies ist ein echter Parser-Grenz-Target statt eines Dummysymbols; sein
Source erreicht dieselbe `Content-Length`-Kontrolle, die die HTTP-Request-
Body-Allokation schützt.

Der Runner weist relative und Checkout-interne Build-Verzeichnisse zurück,
schreibt nur in einen externen Build-Root und ruft das lokal verfügbare `clang`
mit `-fsanitize=fuzzer,address,undefined` auf. Sein expliziter `*) ;;`-Branch
erhält den No-op-Pfad erst nach Auswertung des Containment-Matches. Der
CodeQL-Job behält seine bestehenden top-level Read-only-Berechtigungen und
seinen begrenzten C/C++-Scope.

Der exakte PyYAML-Pin ist einem Scanner-Ignore vorzuziehen, weil er zum bereits
geprüften CI-Lock passt und Resolver/Scanner eine echte, nicht verwundbare
Version verarbeiten lässt. Künftige Upgrades bleiben absichtlich explizite
Reviews.

## Geänderte Dateien

- `fuzz/common_http_headers_fuzz.c`: begrenzter Common-HTTP-Header-libFuzzer-
  Target mit Parser- und Sanitization-Kontrollen.
- `ci/checks/common/check-common-http-header-fuzz.sh` und `Makefile`: externer
  C17-/Sanitizer-Build und begrenzter Ausführungs-Target; der Runner hat einen
  expliziten sicheren `case`-Default für SonarQube Cloud S131.
- `.github/workflows/ci-security-codeql.yml`: Ausführung des Targets im
  bestehenden begrenzten C/C++-CodeQL-Job.
- `requirements-dev.txt`: exakte `PyYAML==6.0.3`-Deklaration.
- `tests/test_ci_security_workflows.py`: statische Workflow- und Dependency-
  Pin-Regressionsassertions.
- `docs/security/ci-security-tooling.md` und `.de.md`: Dokumentation der
  begrenzten C/C++-Coverage.
- Dieses englische/deutsche Change-Record-Paar und beide Indizes.

## Ausgeführte Befehle

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| Normaler Master-Update | bestanden; normaler Merge ohne History-Rewrite Commit `d946043` integrierte Basis `9e788057d2b551ba51ad7c4e6e1d8c5198b77834` in diesen PR-Branch. |
| `make check-common-http-header-fuzz` mit registriertem externem Build-Root | bestanden; C17/libFuzzer/ASan/UBSan-Ausführung schloss 636.146 Läufe in 16 Sekunden ohne Sanitizer- oder Kontrollfehler ab. |
| `make check-common-helpers-c17` mit demselben externen Build-Root | bestanden. |
| `gcc -std=c17 -Wall -Wextra -Werror -c fuzz/common_http_headers_fuzz.c` | bestanden mit GCC 15.2.0. |
| `python3 -m unittest -v tests.test_ci_security_workflows` | bestanden; 18 Tests. |
| `make check-ci-security-contract` | bestanden; 18 statische Tests sowie actionlint-/zizmor-/gitleaks-Lock-Validierung. |
| `sh -n` und `shellcheck` für den Runner | bestanden. |
| Negative Runner-Checkout-Containment-Kontrolle | bestanden: `BUILD_ROOT=<Checkout>` lieferte den erwarteten Status 77 vor Compiler-Aufruf oder Output-Erzeugung. |
| `/root/git/ModSecurity-conector/.venv/bin/python -m pip check` | bestanden: `No broken requirements found.` |
| `git diff --check origin/master` | bestanden. |
| `python3 -m unittest -v tests.test_bilingual_docs` | bestanden; 11 Tests, einschließlich Change-Record-Identität und Struktur paariger Überschriften. |
| Repository-`make check-bilingual-docs` | `blocked_environment`: 20 fehlende lokale Linkziele liegen sämtlich unterhalb des nicht populierten Parent-Framework-Gitlinks; kein Framework-Content wurde initialisiert, inspiziert oder geändert. |
| Fokussierter Security-Diff-Review | bestanden; keine berichtspflichtige Regression. Er korrigierte die EN/DE-Formulierung von deterministisch zu begrenzt, weil der libFuzzer-Lauf keinen festen Seed hat. |

## Security-Auswirkung

Der neue Target ergänzt begrenzte, sanitizer-gestützte Regressionsevidence an
der untrusted HTTP-Header-Parsing-Grenze. Er prüft, dass der Parser keine
fehlerhaften, überlaufenden oder inkonsistenten `Content-Length`-Werte
akzeptiert und dass Log-Sanitizer keine ASCII-Control-Zeichen in ihrem
produzierten Text behalten. Er erzeugt keinen Netzwerk-Listener, Allokations-
Pfad, Credential, Token, Secret oder neue GitHub-Write-Berechtigung. Der
S131-Default-Branch ist nach demselben Checkout-Containment-Vergleich ein
No-op und erweitert weder einen Build-Pfad noch Scanner-, Workflow- oder
Berechtigungsverhalten.

## Runtime-Evidence

Nicht anwendbar. Der Target ist ein Source-Level-In-Process-Parser-Fuzz-Test.
Er startet keinen Connector, Service, HTTP-Listener, H2/H3-Transport oder
libmodsecurity-Engine und behauptet kein vollständiges Runtime-Verhalten.

## Bekannte Einschränkungen

Der eingecheckte Lauf ist absichtlich kurz und begrenzt. Er hat keinen
persistierten Korpus, keine langlaufende Kampagne, keinen vollständigen HTTP-
Service-Aufruf, keine Connector-Host-Integration und keinen Continuous-
Fuzzing-Service. Er ergänzt statt ersetzt den bestehenden Go-UDS-Parser-Fuzzer.

## Verbleibende Risiken

Scorecard muss den resultierenden Default-Branch-Commit erneut scannen, bevor
`FuzzingID` oder `VulnerabilitiesID` als geändert gelten können. Die getrennten
`BranchProtectionID`-, `CodeReviewID`-, `MaintainedID`- und
`CIIBestPracticesID`-Bedingungen erfordern GitHub-Governance, unabhängige
Review-Historie, abgelaufenes Repository-Alter oder externe OpenSSF-
Registrierung; ein Source-PR kann sie nicht ehrlich schließen.

## Nicht ausgeführte Prüfungen mit Begründung

- Exact-PR-Head-CodeQL-, OSV-, Gitleaks-, Scorecard-PR-, SonarQube-Cloud- und
  Review-Evidence benötigen den gepushten aktualisierten PR und müssen für
  seinen exakten Head gelesen werden.
- Die Default-Branch-Scorecard-Closure-Prüfung benötigt einen separat
  autorisierten Merge und anschließend eine frische Hosted-Analyse; sie wird
  nicht aus lokaler Ausführung abgeleitet.
- Keine Framework-/MRTS-Validierung oder -Mutation wird ausgeführt, weil beide
  außerhalb der autorisierten Parent-Source-Grenze liegen.

## Finaler Diff- und Review-Status

Dieser Record wurde nach dem normalen Master-Update und der fokussierten
S131-Korrektur vor dem Push des aktualisierten PR-Heads aktualisiert. Für den
aktuellen lokalen Kandidaten liegen beobachtete C-/Sanitizer-, Helper-, C17-,
statische Workflow-, Dependency-, Shell-, Containment-Negativkontroll- und
Whitespace-Evidence vor. Der fokussierte Security-Diff-Review schloss ohne
berichtspflichtige Regression ab. Exact-Head-Hosted-Evidence und der
erforderliche unabhängige Review stehen noch aus; kein Alert wird als
geschlossen dargestellt.
