# Change Record: PR-#363-Kandidatenvertrag- und Latest-Go-Reparatur

**Sprache:** [English](CR-20260912-pr363-candidate-contract-repair.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260912-pr363-candidate-contract-repair |
| Datum (UTC) | 2026-09-12 |
| Basis-Revision | 2eb08da41a224c52c57856b355a21fb4a22f693a |
| Delivery-Status | Parent-only-Korrektur ist auf Draft-PR #366 vom Task-Branch agent/pr363-candidate-contract-repair ausgeliefert. Dieser Record behauptet keinen Merge oder master-Schreibvorgang und behandelt ausstehende Hosted-Checks nicht als bestanden. |

## Motivation und Problemstellung

Der Benutzer bat um die geprüfte PR-#363-Korrektur in einem eigenen Worktree und PR, weil andere Arbeit blockiert ist. Die frühere ausdrückliche Anforderung bleibt bestehen: Go-Updater und Verifikation sollen immer die neueste Go-Version verwenden, und die übrigen Verträge sollen an die neue Struktur angepasst werden.

PR #363 stellt den Framework-Gitlink um, lässt aber statische Parent-CRS/no-MRTS-SHA-Konsumenten und separat gepflegte ungeschützte NGINX-Übergabeprojektionen veraltet. Der generische Framework-Synchronisierer besitzt absichtlich kein NGINX. Unabhängig akzeptierte CodeQL nur den gültigen eingecheckten .go-version-Selector, obwohl der begrenzte Updater das neueste stabile Go-Release auflösen kann.

## Scope und Nicht-Ziele

Dieser Parent-only-Record umfasst den Framework-Gitlink-Kandidaten d4f7b69dc264852eac74e1439c0887fcb9fbe372, Parent-SHA-/Fixture- und ungeschützte-NGINX-Vertragsangleichung, einen read-only-Kandidatenverifier, dynamische trusted-base-Go-Auflösung für CodeQL, fokussierte Tests, gepaarte Dokumentation und generierte Compiler-Guides.

Er verändert keinen Framework- oder MRTS-Source, gibt sync-framework-component-versions.py kein generisches NGINX-Ownership, verändert nicht die unabhängig gepinnte geschützte NGINX-Broker-Kette, installiert keine Go-Toolchain, verändert keine Workflow-Berechtigungen oder Action-Pins, ändert PR #363 nicht und autorisiert keinen Merge oder master-Schreibvorgang.

## Implementierungsentscheidung und Begründung

Ein neuer begrenzter read-only-Verifier parst candidate Framework common.sh strikt als Daten. Kandidatenvalidierung und Publisher verlangen beide, dass das initiale Parent-CRS/no-MRTS-SHA-Gate, jeder literale `FRAMEWORK_SHA`-Konsument (einschließlich HAProxy-Evidence-Grenze, Profile-Producer und Aggregat) und das Test-Fixture dem Kandidaten-SHA entsprechen; jede ungeschützte NGINX-Übergabeprojektion muss dem kanonischen Kandidatentupel entsprechen. Zusätzlich verlangt er `NGINX_REQUIRE_PINNED_PROVENANCE: "1"` in beiden ungeschützten NGINX-Workflows und weist jeden Kandidatenversuch zurück, diese Parent-eigene Richtlinie zuzuweisen. Der geschützte NGINX-Broker bleibt absichtlich außerhalb dieses Checks.

Weil Framework-`common.sh` anschließend gesourct wird, kann eine endliche Shell-Token-Denylist nicht beweisen, dass eine beliebige künftige Struktur keinen Schreibvorgang für ein geschütztes Feld synthetisiert. Der Verifier verlangt daher, dass sein geprüfter Struktur-Skeleton SHA-256 `609315092e5f5cdd793a33636f7d620445f2e4e802a383c23bc26a70d1bc7c75` entspricht: Er normalisiert nur die sicheren, exakten RHSs der geschlossenen generischen 25-Feld-Source-Registry nach Grammatikvalidierung. Synchronisierer und Verifier weisen beide eine mehrdeutige nicht geklammerte Variablenreferenz ab, deren Shell-Expansion vom Datenparser abweichen könnte. NGINX und jeder nicht registrierte Byte bleiben im Digest, sodass ihre Änderung weiterhin ein explizites Parent-Review erfordert; ein normales generisches Source-Datenupdate bleibt veröffentlichbar. Direktes dynamisches `eval` wird defense in depth abgewiesen.

Der generische Synchronisierer aktualisiert weiterhin nur seine registrierten Envoy- und HAProxy-Projektionen. Das separat gepflegte Parent-NGINX-Tupel wird manuell auf Framework-d4f-release-1.31.5 angeglichen. Die NGINX-Body-Buffer-Fixture folgt demselben ungeschützten Exact-Head-Release-Tupel.

Für CodeQL führt der trusted-base-Job scripts/update-go-version.py --check --json aus, validiert strikte numerische Versionen, Monotonie, update_available und status und veröffentlicht nur latest_version. Envoy- und Traefik-setup-go-Schritte konsumieren dieses trusted Output. Der eingecheckte Selector bleibt ein trusted lower-bound Input; Prereleases, fehlerhafte Reports, Downgrades und inkonsistente Reports scheitern fail-closed.

Die initiale exakte SonarCloud-Analyse von PR #366 fand Verifier-Qualitätsbefunde. Der Verifier validiert nun den Checksum getrennt, vergleicht jedes kanonische Tupelfeld ohne eine Whole-Dictionary-Bedingung und benennt die vier wiederholten Parent-Pfade. Die Release-Tag-Grammatik bleibt ASCII-only und verwendet die kompakte Digit-Class. Fokussierte Reviews fanden, dass eine eingerückte Doppelzuweisung, Deklaration, Append-, unset-, Parameter-Expansion-Zuweisung oder indirekte `eval`-Mutation den früheren Line-Matcher umgehen konnte; der Data-only-Parser verlangt nun für jedes Kandidatentupelfeld genau eine uneingerückte Plain-Zuweisung, weist dynamische Evaluation ab und weist jede Kandidatenmutation der Parent-eigenen Provenance-Flagge ab. Neue negative Controls decken diese Formen, fehlerhafte Checksums, nichtkanonische Tupel, Drift jeder Parent-Policy-Projektion, zitierte/kommentierte Literal-SHA-Schreibweise und jeden veralteten literalen Framework-SHA-Konsumenten vor dem Publishing ab.

Ein exakter PR-#366-Readback bei `204c9e32f4948ffad811ea1897b9a492a98fa404` zeigte danach trotz `OK`-Quality-Gate vier neue offene Maintainability-Issues. Dieser Follow-up verwendet in beiden nicht geklammerten Referenz-Guards `\w` mit `re.ASCII`, sodass die kompakte Class die frühere ASCII-only-Grammatik nicht erweitert. Er ersetzt die drei Literal-SHA-Alternativen durch eine ausgeglichene optionale Quote-Capture und teilt den RHS-Validator in Value-, Reference- und Character-Helper, ohne die akzeptierte Data-Language zu erweitern. Die gepaarte Regression akzeptiert Bare-, Double-quoted-, Single-quoted- und Commented-SHA-Werte und weist nicht passende Quote-Delimiter zurück. Es werden kein `NOSONAR`, keine Issue-Akzeptanz, Exclusion, Scanner-/Quality-Gate-Konfiguration oder Ownership-Änderung verwendet; ein neuer Exact-Head-SonarCloud-Query muss null offene Issues beweisen.

## Security-Auswirkung

Die Änderung stärkt CI-Provenance und Release-Freshness, ohne Validierung, Berechtigungen, unveränderliche Action-Pins, begrenzten Updater-Transport oder geschützte NGINX-Broker-Provenance zu schwächen. Sie fügt keinen generischen NGINX-Writer hinzu. Die bestätigte Kandidatenvertragslücke könnte sonst den Parent-Full-Smoke-Provenance-Guard für übernommene Native-Artefakte abschalten; sie belegt keine ungepinnte Archivbeschaffung und keinen Protected-Broker-Bypass.

## Kompatibilitätsauswirkung

Der gewählte Framework-Handoff verwendet NGINX release-1.31.5 mit SHA-256 e951607d534836624bd36b6b45a71dbfb055237deae3738da6bbf3270dada279, Envoy 1.39.1 und HAProxy 3.2.23. Der Live-bounded-Go-Updater meldete current_version=latest_version=1.27.1. Eine frühere Exact-Head-Runtime-Matrix deckte veraltete `86451b45…`-Literale in drei CRS/no-MRTS-Evidence-Konsumenten auf; alle verwenden nun den geprüften Framework-`d4f7b69d…`-Pin.

## Geänderte Dateien und Dokumentation

Der begrenzte Change umfasst:
- update-submodules-, CodeQL-, CRS/no-MRTS-, Full-Smoke-, Exact-Head- und CI-Security-Workflowverträge;
- den neuen ci/tools/verify-framework-candidate-contract.py-Verifier;
- Parent-NGINX-Preparation-, Readiness-, Lifecycle- und Body-Buffer-Fixture-Verträge;
- Envoy- und HAProxy-Komponentenprojektionen und ihre fokussierten Tests;
- Go-Version-Contract-Checker und fokussierte Tests;
- generierte englische/deutsche Compiler-Guides und gepaarte Variable- und CI-Security-Dokumentation;
- dieses englische/deutsche Change-Record-Paar und beide Change-Record-Indizes.

Die vollständige finale Dateiliste wird vor Delivery anhand des begrenzten Task-Diffs verifiziert.

## Akzeptanzkriterien

- Passender genehmigter Framework-`common.sh`-Struktur-Skeleton, Kandidaten-SHA, ungeschütztes NGINX-Tupel und Parent-eigene Provenance-Policy bestehen ohne Parent-Schreibvorgänge; ein gültiges reines RHS-Update generischer Registry-Daten wird akzeptiert.
- Nicht genehmigte Framework-`common.sh`-Struktur, NGINX- oder nicht registrierte Datenänderung, veraltete initiale oder literale Workflow-SHA-Konsumenten, Fixture-SHA, fehlerhafte, alternative oder mehrdeutige nicht geklammerte Kandidatenzuweisungssyntax, Parent-eigene Policy-Mutation sowie repräsentative ungeschützte NGINX- oder Policy-Drift scheitern fail-closed vor Veröffentlichung.
- Generische Synchronisierung bleibt NGINX-unowned und geschützte Broker-Pins bleiben unverändert.
- Trusted CodeQL verwendet nur das bounded latest-stable-Go-Resolveroutput, weist inkohärente Reports ab und behält gepinnte trusted-base- und setup-go-Controls.
- Englische/deutsche Dokumentation und generierte Guides entsprechen der Implementierung.

## Ausgeführte Befehle

| Check | Tatsächliches Ergebnis |
| --- | --- |
| Fokussierte Kandidaten-, Updater-, Go-, Workflow- und NGINX-Evidence-Suite | Bestanden: 40 Tests. |
| Breitere CI-Security-, NGINX-, Cache-, Snapshot-, Evidence- und Presentation-Suite | Bestanden: 226 Tests; 27 erwartete Framework-abhängige Skips vor dem Task-Gitlink-Commit. |
| Exact-Gitlink-Framework-APR-/Protected-NGINX-Snapshot-Suite | Bestanden: 38 Tests mit dem sauberen, am Commit-Gitlink referenzierten Framework-Checkout. |
| Zusätzliche Kandidatenverifier- und ausführbare Go-Resolver-Controls | Bestanden: 16 Tests. |
| Fokussierte Post-Review-Kandidaten-/Workflow-Controls | Bestanden: 66 Tests. |
| Fokussierte Runtime-Profile-, Kandidatenverifier- und Workflow-Controls nach Entdeckung des veralteten Literal-SHA, indirektem eval, Struktur-Skeleton und mehrdeutiger Referenz | Bestanden: 75 Tests. |
| Generischer Source-Parser plus Kandidatenverifier-Controls für mehrdeutige Referenzen | Bestanden: 41 Tests; die Abweisung erfolgte vor Synchronisierer-Zielschreibvorgängen und Parent-Projektionsinspektion. |
| Native-Override-Provenance-Guard-Control | Bestanden: 1 Test; ein nativer NGINX-Override wird blockiert, während die Parent-Policy `1` ist. |
| make check-ci-security-contract | Bestanden: 148 Tests mit 5 erwarteten nicht verfügbaren Namespace-/Identity-Skips nach Verifier- und Provenance-Policy-Remediation; validierte actionlint-, zizmor- und gitleaks-Tool-Locks. |
| Sonar-Follow-up fokussierte Parser-/Verifier-Tests | Bestanden: 42 Tests in 32.311s, einschließlich gültiger benachbarter Referenzen, No-write-Abweisung mehrdeutiger Referenzen und ausgeglichener optionaler Quote-Controls. |
| Sonar-Follow-up make check-ci-security-contract | Bestanden: 149 Tests in 51.014s mit 5 erwarteten nicht verfügbaren Namespace-/Identity-Skips; actionlint-, zizmor- und gitleaks-Lock-Validierung bestanden. |
| Lokale Sonar-CLI-Dateianalyse | Durch ein lokales Analyzer-Image mit nicht verfügbaren CPU-Features blockiert; der autoritative Exact-Head-SonarCloud-PR-Query bleibt erforderlich. |
| actionlint für jeden geänderten Workflow | Bestanden ohne Output. |
| zizmor --offline .github/workflows | Bestanden: keine Findings; 95 bestehende Repository-Suppressions wurden gemeldet. |
| Fokussiertes unabhängiges Post-Patch-Security-Review | Nach Remediation bestanden: Es reproduzierte die alternativen Zuweisungs- und Parent-eigene-Provenance-Policy-Lücken, und der Verifier weist beides nun zurück, ohne Kandidatendaten zu sourcen. |
| check-go-version-contract.py --json | Bestanden mit Version 1.27.1 und ohne Violations. |
| scripts/update-go-version.py --check --json | Bestanden mit current_version=latest_version=1.27.1. |
| make check-compiler-guides | Bestanden: 22 Tests. |
| git diff --check und Python-Kompilierung der geänderten Python-Pfade | Bestanden. |
| make check-bilingual-docs | Nur durch vorbestehende fehlende Links in das absichtlich nicht initialisierte Task-Framework-Submodule blockiert; kein task-spezifischer Pair-Fehler wurde gemeldet. Ein Root-Checkout-Retry wurde nach wiederholtem No-Output-Polling unterbrochen und wird nicht als bestanden behauptet. |

## Runtime-Evidence

Dieser statische Source-Record enthält kein Connector-Runtime- oder
Matrix-Resultat des Nachfolger-Heads. Der vorherige exakte PR-Head bestand den
realen Runtime-Schritt für alle fünf Connectors, aber Envoy, Lighttpd und
Traefik scheiterten anschließend bei der Profile-Erzeugung, weil drei spätere
Workflow-Konsumenten Framework-SHA `86451b45…` behielten, während das
ausgecheckte Framework `d4f7b69d…` war; Apache und HAProxy deckten diesen
Identity-Check nicht auf. Der Nachfolger gleicht jeden literalen Konsumenten an
und lässt den Verifier bei künftiger Drift fail-closed scheitern. Lokale
Contract-Evidence ersetzt keine Hosted-Runtime-Evidenz des Nachfolgers.

## Bekannte Einschränkungen

Framework-abhängige Tests müssen nach dem Task-Commit mit exaktem Gitlink und
einem sauberen read-only Framework-Checkout wiederholt werden. Die lokale
Python-Umgebung genügt für fokussierte Tests, ersetzt aber nicht die exakte
Hosted-Workflow-Umgebung.

## Verbleibende Risiken

Das verbleibende Risiko ist Hosted- und Runtime-Evidenz, kein Grund,
Protected-Broker-Ownership zu ändern oder einen Merge zu behaupten.
Task-Worktree und Remote-Branch müssen erhalten bleiben, solange der
resultierende Draft PR offen ist.

## Nicht ausgeführte Prüfungen mit Begründung

Kein final vollständig bestandener hosted GitHub-Actions-, SonarQube-,
Connector-Build-, Nachfolger-Runtime-Matrix-, Scheduler-Updater-, PR-#363-
Änderungs- oder Merge-Resultat wird behauptet. SonarCloud- und Go/CodeQL-
Evidenz des vorherigen Heads bestanden, aber dieser Nachfolger benötigt seinen
eigenen External-Runner-Readback. Diese Checks werden daher nicht als final
bestandene Controls dargestellt.

## Findings und Restrisiko

FND-PARENT-1086 verfolgt den Kandidatenvertrags-Release-Blocker einschließlich des Parent-eigenen Full-Smoke-Provenance-Policy-Guards und der Entdeckung veralteter literaler Framework-SHA-Konsumenten. FND-PARENT-1087 verfolgt dynamische Latest-Go-CodeQL-Freshness. FND-SONAR-0085 ist für die vier exakten Maintainability-Issues bei `204c9e32…` wieder eröffnet und bleibt in progress, bis dieser normale Follow-up-Head einen SonarCloud-Readback mit null Issues hat. FND-PARENT-1085 bleibt ein separater behobener früherer Cross-Series-Grammatikdefekt.

## Finaler Diff- und Review-Status

Begrenzter Diff, explizite Stagingliste, Worktree-Grenze, Gitlink-SHA,
statische Tests, actionlint und ein unabhängiges Post-Patch-Security-Review
sind vollständig. SonarCloud- und Runtime-Resultate des exakten Nachfolger-
Heads bleiben nötig, bevor der PR als vollständig verifiziert gilt.
