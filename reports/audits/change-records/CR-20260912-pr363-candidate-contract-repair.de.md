# Change Record: PR-#363-Kandidatenvertrag- und Latest-Go-Reparatur

**Sprache:** [English](CR-20260912-pr363-candidate-contract-repair.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260912-pr363-candidate-contract-repair |
| Datum (UTC) | 2026-09-12 |
| Basis-Revision | 2eb08da41a224c52c57856b355a21fb4a22f693a |
| Delivery-Status | Parent-only-Korrektur ist auf Task-Branch agent/pr363-candidate-contract-repair in Arbeit. Dieser Record behauptet keinen Commit, Push, PR-Nummer, Hosted-Resultat, Merge oder master-Schreibvorgang. |

## Motivation und Problemstellung

Der Benutzer bat um die geprüfte PR-#363-Korrektur in einem eigenen Worktree und PR, weil andere Arbeit blockiert ist. Die frühere ausdrückliche Anforderung bleibt bestehen: Go-Updater und Verifikation sollen immer die neueste Go-Version verwenden, und die übrigen Verträge sollen an die neue Struktur angepasst werden.

PR #363 stellt den Framework-Gitlink um, lässt aber statische Parent-CRS/no-MRTS-SHA-Konsumenten und separat gepflegte ungeschützte NGINX-Übergabeprojektionen veraltet. Der generische Framework-Synchronisierer besitzt absichtlich kein NGINX. Unabhängig akzeptierte CodeQL nur den gültigen eingecheckten .go-version-Selector, obwohl der begrenzte Updater das neueste stabile Go-Release auflösen kann.

## Scope und Nicht-Ziele

Dieser Parent-only-Record umfasst den Framework-Gitlink-Kandidaten d4f7b69dc264852eac74e1439c0887fcb9fbe372, Parent-SHA-/Fixture- und ungeschützte-NGINX-Vertragsangleichung, einen read-only-Kandidatenverifier, dynamische trusted-base-Go-Auflösung für CodeQL, fokussierte Tests, gepaarte Dokumentation und generierte Compiler-Guides.

Er verändert keinen Framework- oder MRTS-Source, gibt sync-framework-component-versions.py kein generisches NGINX-Ownership, verändert nicht die unabhängig gepinnte geschützte NGINX-Broker-Kette, installiert keine Go-Toolchain, verändert keine Workflow-Berechtigungen oder Action-Pins, ändert PR #363 nicht und autorisiert keinen Merge oder master-Schreibvorgang.

## Implementierungsentscheidung und Begründung

Ein neuer begrenzter read-only-Verifier parst candidate Framework common.sh strikt als Daten. Kandidatenvalidierung und Publisher verlangen beide, dass jeder Parent-CRS/no-MRTS-SHA-Konsument und das Test-Fixture dem Kandidaten-SHA entsprechen und jede ungeschützte NGINX-Übergabeprojektion dem kanonischen Kandidatentupel entspricht. Der geschützte NGINX-Broker bleibt absichtlich außerhalb dieses Checks.

Der generische Synchronisierer aktualisiert weiterhin nur seine registrierten Envoy- und HAProxy-Projektionen. Das separat gepflegte Parent-NGINX-Tupel wird manuell auf Framework-d4f-release-1.31.5 angeglichen. Die NGINX-Body-Buffer-Fixture folgt demselben ungeschützten Exact-Head-Release-Tupel.

Für CodeQL führt der trusted-base-Job scripts/update-go-version.py --check --json aus, validiert strikte numerische Versionen, Monotonie, update_available und status und veröffentlicht nur latest_version. Envoy- und Traefik-setup-go-Schritte konsumieren dieses trusted Output. Der eingecheckte Selector bleibt ein trusted lower-bound Input; Prereleases, fehlerhafte Reports, Downgrades und inkonsistente Reports scheitern fail-closed.

## Security-Auswirkung

Die Änderung stärkt CI-Provenance und Release-Freshness, ohne Validierung, Berechtigungen, unveränderliche Action-Pins, begrenzten Updater-Transport oder geschützte NGINX-Broker-Provenance zu schwächen. Sie fügt keinen generischen NGINX-Writer hinzu. Das beobachtete Problem ist eine CI-/Control-Konsistenzlücke, keine validierte ausnutzbare Schwachstelle.

## Kompatibilitätsauswirkung

Der gewählte Framework-Handoff verwendet NGINX release-1.31.5 mit SHA-256 e951607d534836624bd36b6b45a71dbfb055237deae3738da6bbf3270dada279, Envoy 1.39.1 und HAProxy 3.2.23. Der Live-bounded-Go-Updater meldete current_version=latest_version=1.27.1.

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

- Passender Framework-Kandidaten-SHA und ungeschütztes NGINX-Tupel bestehen ohne Parent-Schreibvorgänge.
- Veralteter Workflow-SHA, Fixture-SHA, fehlerhafte Kandidatensyntax und repräsentative ungeschützte NGINX-Drift scheitern fail-closed vor Veröffentlichung.
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
| make check-ci-security-contract | Bestanden: 132 Tests mit 5 erwarteten nicht verfügbaren Namespace-/Identity-Skips; validierte actionlint-, zizmor- und gitleaks-Tool-Locks. |
| actionlint für jeden geänderten Workflow | Bestanden ohne Output. |
| zizmor --offline .github/workflows | Bestanden: keine Findings; 95 bestehende Repository-Suppressions wurden gemeldet. |
| Frisches unabhängiges Post-Patch-Security-Review | Bestanden: kein plausibler neuer Security-Befund im begrenzten Diff; Kandidatendaten bleiben begrenzt und unsourced, trusted Workflow-Grenzen und Berechtigungen bleiben unverändert. |
| check-go-version-contract.py --json | Bestanden mit Version 1.27.1 und ohne Violations. |
| scripts/update-go-version.py --check --json | Bestanden mit current_version=latest_version=1.27.1. |
| make check-compiler-guides | Bestanden: 22 Tests. |
| git diff --check und Python-Kompilierung der geänderten Python-Pfade | Bestanden. |
| make check-bilingual-docs | Nur durch vorbestehende fehlende Links in das absichtlich nicht initialisierte Task-Framework-Submodule blockiert; kein task-spezifischer Pair-Fehler wurde gemeldet. Ein Root-Checkout-Retry wurde nach wiederholtem No-Output-Polling unterbrochen und wird nicht als bestanden behauptet. |

## Runtime-Evidence

Dieser statische Source-Record enthält kein Connector-Runtime-, hosted GitHub-
Actions-, CodeQL-, SonarQube- oder Matrix-Resultat. Lokale Contract-Evidence
wird nur für das begrenzte Source-Verhalten aufbewahrt und ersetzt keine
Exact-Task-PR-Head- oder Hosted-Runtime-Evidenz.

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

Keine hosted GitHub Actions, CodeQL, SonarQube, Connector-Builds, Runtime-
Matrix, Scheduler-Updater-Ausführung, PR-#363-Änderung oder Merge-Resultat
werden behauptet. Sie benötigen den exakten Task-PR-Head, externe Runner oder
separate aktuelle Benutzerautorisierung und wurden daher nicht als lokal
bestandene Controls dargestellt.

## Findings und Restrisiko

FND-PARENT-1086 verfolgt den Kandidatenvertrags-Release-Blocker; FND-PARENT-1087 verfolgt dynamische Latest-Go-CodeQL-Freshness. Beide bleiben in_progress, bis exakter Task-PR-Head und anwendbare Hosted-Controls beobachtet sind. FND-PARENT-1085 bleibt ein separater behobener früherer Cross-Series-Grammatikdefekt.

## Finaler Diff- und Review-Status

Begrenzter Diff, explizite Stagingliste, Worktree-Grenze, Gitlink-SHA,
statische Tests, actionlint und ein unabhängiges Post-Patch-Security-Review
sind vollständig. Delivery-Fakten werden erst nach Beobachtung dokumentiert.
