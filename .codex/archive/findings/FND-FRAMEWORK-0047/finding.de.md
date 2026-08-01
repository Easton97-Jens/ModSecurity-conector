# FND-FRAMEWORK-0047 — Ein gequoteter YAML-`uses`-Schlüssel umgeht die geprüfte Action-Lock-Bindung eines schreibfähigen Framework-Publishers

- Kategorie: `security_validated`
- Repository / Ownership: `framework` / `framework`
- Priorität / Schweregrad / Konfidenz: `P1` / `high` / `reproduced`
- Status / Feasibility: `fixed` / `feasible_now`
- Release-Blocker / Sicherheitsrelevanz: `true` / `true`

## Zusammenfassung

Framework-PR #40 ergänzt einen geprüften Action-Lock für Workflow-Tools. Sein
Lock-Equality-Checker parst nur Quellzeilen, die mit dem literalen ungequoteten
`uses:` beginnen. Ein YAML-zulässiger gequoteter Schlüssel wie:

```yaml
"uses": actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
```

wird als dasselbe `uses`-Feld geparst, umgeht aber diesen Source-Line-Parser.
Die anderen verpflichtenden Validatoren verlangen eine vollständige
unveränderliche SHA, vergleichen sie jedoch nicht mit dem geprüften Lock. Die
exakte PR-#40-Validator-Kette akzeptiert deshalb eine vom Lock abweichende
Publisher-Action-Referenz.

## Auswirkung und Grenzen

Der Publisher läuft später mit `contents: write` und `pull-requests: write`
und nutzt sein eingegrenztes GitHub-Token. Dieses Finding behauptet nicht, dass
eine nicht authentisierte Partei einen Commit in einem offiziellen
`actions/*`-Repository erzeugen kann. Es beweist, dass die Reviewed-Lock-
Provenance-Grenze des Frameworks umgangen werden kann, bevor ein token-
tragender Publisher nach Übernahme einer Änderung in den vertrauenswürdigen
Default-Branch läuft.

Mutable Tags werden weiterhin abgelehnt; dies ist ein getrennter Full-SHA-
Lock-Equality-Bypass. Bis zur Korrektur und Regressionstestung ist er ein
P1-Release-Blocker mit hohem Schweregrad.

## Exakte Evidence und Reproduktion

- Basis: `f73f8842f45318e2df8aff1d31855eeb7c20a22f`
- Betroffener Head: `c274460a3e27b9fc0dfe904e1ce5eba33042f444`
- Run: `20260722T145132Z-framework-pr-39-41-master-integration-9a3c7dc7`
- Evidence: `CAND-FW40-QUOTED-USES/validation_report.md`
- SHA-256: `a7f5df22d62985136dede2c12d775da8d80661646e24e11a57ff45941dd46b8c`

Der reine Evidence-Harness mutierte einen abgetrennten Exact-Head-Worktree und
führte dieselben drei statischen Validatoren wie der read-only-`validator`-Job
aus. Der Workflow wurde nach jedem Fall wiederhergestellt. Der normale Workflow
und der negative Mutable-Tag-Case verhielten sich korrekt. Die gequotete andere
Full-SHA bestand alle drei Validatoren.

Der Publisher hängt von dem erfolgreichen Validator ab und besitzt kein
`always()`-Override; deshalb kann dieser erfolgreiche Fall den Publisher unter
normalen vertrauenswürdigen Schedule-/Dispatch-Bedingungen erreichen. Bei der
Reproduktion liefen kein Publisher, keine Netzwerkaktion und kein token-
tragender Befehl.

## Erforderliche Remediation und Validierung

Jede geparste externe `uses`-Referenz muss unabhängig von der YAML-Schreibweise
an den geprüften Action-Lock gebunden werden. Das bestehende Verhalten für
lokale Actions, Version-Comment-Prüfungen, Least-Privilege-Berechtigungen,
Publisher-Abhängigkeit und Branch-Bedingung bleibt erhalten. Ergänze fokussierte
Quoted-Key- und Flow-Mapping-Full-SHA-Regressionen sowie einen legitimen
Current-Lock-Control.

Bevor dieses Finding geschlossen werden kann, muss der Konsolidierungsbranch
die fokussierten Tests und alle drei statischen Validatoren bestehen. Sein
exakter PR-Head muss anschließend die anwendbaren gehosteten Security-, CI- und
Sonar-Controls bestehen. `FND-FRAMEWORK-0046` und `FND-SONAR-0002` bleiben
getrennte Blocker.

Die Konsolidierung ist lokal `fixed`: Ihr Contract vergleicht geparste externe
`uses`-Referenzen rekursiv mit dem überprüften Lock, während fokussierte Tests
sowohl Quoted-Key- als auch Flow-Mapping-Lock-divergente Full-SHAs ablehnen.
Least-Privilege-Berechtigungen und Validator-Abhängigkeit des Publishers sind
unverändert. Hosted Exact-Head-Workflow-Security- und Quality-Evidence bleibt
vor der Verifikation erforderlich.

Die lokale Korrektur ist an Framework-Commit
`22747d460a9f7be02760edf05c311be376492457` gebunden; Clean-Worktree-,
Exact-Range-Whitespace- und native `make lint`-Checks bestanden. Hosted
Exact-Head-Evidence bleibt erforderlich.

Der offene Framework-PR #42 bei
`1fd3b362e0fed9766c6920e3c7bd1939535850f2` bestand alle anwendbaren Hosted-
Security- und Quality-Controls einschließlich CodeQL und Sonar-PR-Quality-
Gate. Dies stärkt den Status `fixed`, doch das Finding ist erst nach normalem
Master-Merge und resulting-master-Evidence `verified` oder geschlossen.
