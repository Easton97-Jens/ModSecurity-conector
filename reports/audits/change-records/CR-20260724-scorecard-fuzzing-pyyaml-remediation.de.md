# Change Record: Scorecard-Fuzzing- und PyYAML-Remediation

**Sprache:** [English](CR-20260724-scorecard-fuzzing-pyyaml-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260724-scorecard-fuzzing-pyyaml-remediation` |
| Datum (UTC) | `2026-07-24` |
| Basis-Revision | `30ee953b57f4aafebaa0e6ed565a80f6500db1de` |
| Grenze | Ausschließlich Parent-Common-HTTP-Header-Helper, der begrenzte C/C++-CodeQL-Job, eine Development-Dependency-Deklaration, fokussierte statische Regression, Leserdokumentation und dieses Change-Record-Paar/Index. Framework, MRTS, Gitlinks, GitHub-Settings, Workflow-Berechtigungen und das bestehende Go-Fuzzing bleiben unverändert. |
| Finding-Verknüpfung | `FND-GITHUB-0001`, Scorecard `FuzzingID #11` und Scorecard `VulnerabilitiesID #12`. |

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
mit `-fsanitize=fuzzer,address,undefined` auf. Der CodeQL-Job behält seine
bestehenden top-level Read-only-Berechtigungen und seinen begrenzten C/C++-
Scope.

Der exakte PyYAML-Pin ist einem Scanner-Ignore vorzuziehen, weil er zum bereits
geprüften CI-Lock passt und Resolver/Scanner eine echte, nicht verwundbare
Version verarbeiten lässt. Künftige Upgrades bleiben absichtlich explizite
Reviews.

## Geänderte Dateien

- `fuzz/common_http_headers_fuzz.c`: begrenzter Common-HTTP-Header-libFuzzer-
  Target mit Parser- und Sanitization-Kontrollen.
- `ci/checks/common/check-common-http-header-fuzz.sh` und `Makefile`: externer
  C17-/Sanitizer-Build und begrenzter Ausführungs-Target.
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
| `make check-common-http-header-fuzz` mit registriertem externem Build-Root | bestanden; C17/libFuzzer/ASan/UBSan-Ausführung schloss 648.679 Eingaben in 16 Sekunden ohne Sanitizer- oder Kontrollfehler ab. |
| `make check-common-helpers-c17` mit demselben externen Build-Root | bestanden. |
| `python3 -m unittest tests/test_ci_security_workflows.py` | bestanden; 18 Tests. |
| `make check-ci-security-contract` | bestanden; 18 statische Tests sowie actionlint-/zizmor-/gitleaks-Lock-Validierung. |
| `sh -n` und `shellcheck` für den neuen Runner | bestanden. |
| Fokussierter Security-Diff-Review | bestanden; keine berichtspflichtige Regression. Er korrigierte die EN/DE-Formulierung von deterministisch zu begrenzt, weil der libFuzzer-Lauf keinen festen Seed hat. |
| Repository-`make check-bilingual-docs` | `blocked_environment`: seine einzigen gemeldeten Fehler sind bereits vorhandene fehlende Linkziele unterhalb des nicht populierten Framework-Gitlinks im isolierten Worktree; Framework wurde nicht initialisiert oder geändert. |

## Security-Auswirkung

Der neue Target ergänzt begrenzte, sanitizer-gestützte Regressionsevidence an
der untrusted HTTP-Header-Parsing-Grenze. Er prüft, dass der Parser keine
fehlerhaften, überlaufenden oder inkonsistenten `Content-Length`-Werte
akzeptiert und dass Log-Sanitizer keine ASCII-Control-Zeichen in ihrem
produzierten Text behalten. Er erzeugt keinen Netzwerk-Listener, Allokations-
Pfad, Credential, Token, Secret oder neue GitHub-Write-Berechtigung.

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
  Review-Evidence benötigen den gepushten Draft PR und müssen für seinen
  exakten Head gelesen werden.
- Die Default-Branch-Scorecard-Closure-Prüfung benötigt einen separat
  autorisierten Merge und anschließend eine frische Hosted-Analyse; sie wird
  nicht aus lokaler Ausführung abgeleitet.
- Keine Framework-/MRTS-Validierung oder -Mutation wird ausgeführt, weil beide
  außerhalb der autorisierten Parent-Source-Grenze liegen.

## Finaler Diff- und Review-Status

Dieser Record wird vor Staging, Commit, Push und Draft-PR-Erstellung geschrieben.
Die oben genannten lokalen C-/Sanitizer-, Helper-, statischen Workflow-,
Dependency-, Shell- und Dokumentationsprüfungen wurden beobachtet. Der
Full-Tree-Bilingual-Check bleibt nur durch den nicht populierten Framework-
Gitlink umgebungsblockiert. Der fokussierte Security-Diff-Review schloss ohne
berichtspflichtige Regression ab. Exact-Head-Hosted-Evidence steht noch aus;
kein Alert wird als geschlossen dargestellt.
