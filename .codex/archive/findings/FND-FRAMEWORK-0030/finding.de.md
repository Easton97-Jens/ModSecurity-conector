# FND-FRAMEWORK-0030 — Framework-ModSecurity-v3-Provenance-Guard weist die freigegebene rekursive Quelltopologie zurück

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-FRAMEWORK-0030 |
| Kategorie | ci_failure |
| Repository / Ownership | framework / framework |
| Priorität / Severity | P1 / not_applicable |
| Konfidenz / Status | validated / fixed |
| Feasibility | feasible_now |
| Release-Blocker | ja |
| Sicherheitsrelevant | ja |

## Beobachtung und Auswirkung

Auf Framework-master `784977615acfc55567e37b863309abc4a38ac877` stoppen sowohl
der isolierte Apache- als auch der NGINX-Consumer vor der Source-Nutzung mit:

```text
BLOCKED: ModSecurity v3 checkout declares submodules without an approved provenance rule
```

Das zurückgehaltene Komponenten-Inventar dokumentiert die Checkout-Root-Origin
`https://github.com/owasp-modsecurity/ModSecurity.git`, den exakten Root-
Commit `0fb4aff98b4980cf6426697d5605c424e3d5bb60`, `git fsck: PASS`, rekursiv
initialisierte Submodule, acht gepinnte Children und einen sauberen Submodule-
Status. Der pauschale Framework-Guard weist diese bekannte freigegebene
Topologie allein zurück, weil die Upstream-Root `.gitmodules` und Gitlinks
enthält.

Das aktuelle Ergebnis ist fail-closed: Kein nicht freigegebener Source erreichte
einen Build. Es blockiert aber auch den legitimen Source und damit die Apache-
und NGINX-Komponenten-Vorbereitung, aktuelle Evidence für `FND-CROSS-0001` und
den geschützten Integrationspfad für Parent PR #55.

## Evidence und Ursache

| Consumer / Evidence | SHA-256 |
| --- | --- |
| Apache-Provenance-Blocker-Log | `62685d6097be5af3e933c735ac2c04bb0f08a51050485d2e36661b1793fe11b5` |
| NGINX-Provenance-Blocker-Log | `d2b6288dec1b94a6e59d55040fa9355de4949519ae922cefd1ceb7ded9693fd2` |
| Zurückgehaltenes Komponenten-Inventar | `d7e6517fe8be3a610dd51478cbb45c2fe9b4af3b1720562076129e24822efac3` |

Alle Artefakte liegen im Run
`20260720T163253Z-pr55-runtime-evidence-refresh-698b1734` im Verzeichnis
`evidence/`. Die ersten beiden sind Apache-/NGINX-Consumer-Logs; das dritte
ist `runtime-component-manifest-initial-failure.json`, dessen rekursives
Source-Inventar die freigegebene Root und saubere Acht-Child-Topologie meldet.

`ci_require_approved_modsecurity_v3_checkout` weist jedes `.gitmodules`-
Manifest oder mode-`160000`-Gitlink kategorisch zurück, bevor eine
topologiespezifische Regel es validieren kann. Diese Regel ist mit dem exakten
freigegebenen Upstream-Commit unvereinbar, der legitimerweise einen rekursiven
gepinnte Submodule-Graphen verwendet.

Post-Fix-retained Evidence:

| Feld | Wert |
| --- | --- |
| Run-ID | `20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607` |
| Artefakt | `/var/tmp/codex/ModSecurity-conector/runs/20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607/evidence/framework-modsecurity-v3-provenance-remediation-postfix.md` |
| Typ | `framework_postfix_security_validation_report` |
| SHA-256 | `b20ccffd871b9e4d821f5bdf08bb98061a0d7e6ed41a8921551b8fa2ec542aec` |
| Befehl | RTK-umhüllte fokussierte Topologie-/Provenance-Suite, Framework-Make-Provenance-Contract, Dokumentations-Checks, vollständiger Framework-Lint und unabhängiges fokussiertes Security-Re-Review |
| Working Directory | `/var/tmp/codex/ModSecurity-conector/runs/20260720T173133Z-pr55-runtime-remediation-7e38e876/tmp/framework-worktree` |
| Exit-Code / beobachtet | `0` / `2026-07-20T21:07:10Z` |
| Retention | `retained_task_evidence` |

## Erforderliche Remediation und Validierung

Der lokale Candidate behält Root-Origin-/Commit-/Ref- und gehärtete Git-
Kontrollen bei, ersetzt die pauschale `.gitmodules`-/Gitlink-Ablehnung durch
eine statische exakte Acht-Child-`(Pfad, Origin, Commit)`-Topologie und
validiert saubere Root-/Child-Worktrees, kanonische Pfade, Child-gitdir-
Containment, genau ein `origin` und detached HEADs. Fehlende,
uninitialisierte, zusätzliche, schmutzige, pfad-inkonsistente,
origin-inkonsistente, commit-inkonsistente, symlinked, escaping oder nicht
parsebare Topologie schlägt fail-closed fehl. Rekursive Submodule werden nie
generisch akzeptiert.

Die frische Akquisition etabliert eine private Source-Root vor Git, pinnt die
Root, scrubbt lokale Recursive-Update-Konfiguration, initialisiert/checkt die
freigegebenen Children explizit aus und validiert dieselbe Topologie erneut.
Die fokussierte Suite deckt die exakte saubere Topologie sowie dirty,
missing/uninitialized, extra, falsche Origin/Commit, Path-Escape/Symlink,
externes gitdir, Worktree, Remote und Symbolic-HEAD-Varianten ab. Die Suite
(24 Tests), der Framework-Make-Provenance-Contract (24 Tests), der CI-
Bootstrap-Contract (6 Tests), Dokumentations-/Change-Record-Checks und der
vollständige Framework-Lint bestanden. Das unabhängige fokussierte Review fand
keinen verbleibenden High- oder Critical-Blocker für das dokumentierte Cross-
UID-Lokal-Angreifer-Modell.

Die Dokumentation beschreibt jetzt diese exakte rekursive Initialisierung und
Validierung; sie behauptet keine kategoriale Ablehnung aller `.gitmodules` oder
Gitlinks. Ein frischer Parent-Komponenten-/Runtime-Lauf benötigt weiterhin die
unabhängige Parent-Cache-Reparatur `FND-PARENT-0042` und eine unabhängig
gelieferte Framework-Revision.

## Grenzen und Disposition

Dieser Record ist `fixed`, nicht `verified`, closed oder risikoakzeptiert. Die
Evidence beschreibt weiter eine Availability-False-Rejection und keinen
erfolgreichen Supply-Chain-Bypass; Dirty-Worktree-Prüfungen sind eine
erforderliche fail-closed-Reparaturkontrolle. Das begleitende P0/high
`FND-FRAMEWORK-0032` ist im selben Candidate ebenfalls lokal `fixed`.

Es erfolgten kein Framework-Branch, Pull Request, Merge, Parent-Gitlink-Update
oder MRTS-Aktion. Ein separater Framework-PR, Exact-Head-Checks/Review/Sonar-
Evidence, Framework-master-Verifikation, ein separat autorisiertes Parent-
Gitlink-Update, die unabhängige `FND-PARENT-0042`-Reparatur und frische
`FND-CROSS-0001`-Runtime-Evidence bleiben erforderlich, bevor Parent PR #55
fortschreiten kann.

## Historie

- 2026-07-20T16:53:52Z — Apache- und NGINX-Consumer-Pfade reproduzierten
  beide den kategorialen Framework-Guard-Fehler; das zurückgehaltene Inventar
  zeigte die freigegebene Root und saubere rekursive Topologie.
- 2026-07-20T17:14:09Z — der Befund wurde von früheren ModSecurity-v3-
  Parser-/Updater-Records dedupliziert und für eine Framework-only fail-closed
  Provenance-Reparatur angelegt; es erfolgte keine Framework- oder MRTS-
  Delivery-Aktion.
- 2026-07-20T18:36:32Z — FND-FRAMEWORK-0032 wurde als getrenntes validiertes
  P0/high-Local-Git-Sicherheitsblocker im Kandidaten angelegt. Die
  Topologie-Reparatur bleibt in_progress, ist aber nicht deliverbar, bis dieses
  Finding fokussierte Regression, Legitimate-Control und No-Mutation-Proof
  bestanden hat.
- 2026-07-20T21:20:47Z — der lokale Candidate installierte den statischen
  exakten Acht-Child-Topologie-Guard, härtete und begrenzte frische rekursive
  Initialisierung und bestand fokussierte Topologie-/Konfigurations-Negative,
  Legitimate-Controls, Make, Lint, Dokumentation, Change Record und
  unabhängiges Review. Status ist `fixed`, nicht `verified`, bis separater
  Framework-PR und Master-Verifikation vorliegen.
