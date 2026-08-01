# FND-SONAR-0004 — SonarQube-Cloud-Projekt analysiert schreibgeschützte Framework- und MRTS-Bäume

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-SONAR-0004` |
| Kategorie | `sonarqube_finding` |
| Repository | `parent` |
| Ownership | `sonarqube_configuration` |
| Priorität | `P1` |
| Severity | `not_applicable` |
| Confidence | `confirmed` |
| Status | `blocked` |
| Release-Blocker | `true` |
| Sicherheitsrelevant | `true` |

## Zusammenfassung

Das aktuelle Parent-SonarQube-Cloud-Projekt enthält 341 ausschließlich zum
Framework gehörende und 17 MRTS-Issue-Records, obwohl diese verschachtelten
Repositories schreibgeschützt und außerhalb der Ownership-Grenze dieser
Aufgabe liegen.

## Beobachtetes und erwartetes Verhalten

Die ersetzende zurückgehaltene paginierte Baseline für Remote-Parent-SHA
`aabde81a9a315bf3e494e595ab0399357c596f9c` enthält 358 Records unterhalb von
`modules/ModSecurity-test-Framework/`: 337 offene und 4 geschlossene
ausschließlich zum Framework gehörende Records sowie 17 offene Records im
MRTS-Subtree. Öffentliche effektive Settings bestätigen
`sonar.autoscan.enabled=true`; der Parent besitzt keine versionierte
Scanner-Konfiguration. Kein Parent-eigener Source-Fix kann diese
Nested-Source-Records beheben.

Eine Parent-Sonar-Analyse muss ausschließlich Parent-eigene Source-Pfade
ausweisen. Framework- und MRTS-Pfade müssen null analysierte Issue-Records
haben, ohne Parent-Source-Regeln zu unterdrücken, zu deaktivieren oder breit
auszuschließen.

## Auswirkung, Scope und Voraussetzungen

Die aktuelle Analyse kann nicht vollständig durch autorisierte Parent-
Source-Änderungen abgeglichen werden; verschachtelte Security-/Quality-Records
können projektweite Metriken und die Gate-Triage verfälschen. Voraussetzung
sind Automatic Analysis des Parent-Checkouts und die schreibgeschützte
Framework-/MRTS-Grenze dieser Aufgabe; keines der verschachtelten Repositories
wurde gelesen oder geändert.

Betroffene Pfade:

- `modules/ModSecurity-test-Framework/`
- `modules/ModSecurity-test-Framework/tools/MRTS/`

## Evidence und Reproduktion

Zurückgehaltene Evidence:

- Run: `20260719T131708Z-sonarcloud-parent-remediation-baseline-bbce9d6b`
- Artifact: `/var/tmp/codex/ModSecurity-conector/runs/20260719T131708Z-sonarcloud-parent-remediation-baseline-bbce9d6b/evidence/sonar-baseline-issues.json`
- SHA-256: `1d03d14de35cd0ec0bb5e26854534e1f1ec4694ed3e917ac220e65c0ed5ef25f`
- Producer: RTK-proxierte öffentliche SonarQube-Cloud-V1-Issue-Paginierung mit
  anschließender Component-Prefix-Auswertung; Working Directory
  `/root/git/ModSecurity-conector`; Exit-Code `0`; beobachtet
  `2026-07-19T13:18:35Z`; Retention `retained_task_evidence`.
- Run: `20260719T134711Z-sonarcloud-parent-remediation-current-3de21a87`
- Artifact:
  `/var/tmp/codex/ModSecurity-conector/runs/20260719T134711Z-sonarcloud-parent-remediation-current-3de21a87/evidence/sonar-baseline-issues.json`
- SHA-256: `b219bff16466e443c11733e335ae8b9bf9b63aac2cf556bd5b0d9fd8d3e8175c`
- Producer: RTK-proxierte öffentliche SonarQube-Cloud-V1-Exact-Current-Issue-
  Paginierung mit anschließender Component-Prefix-Auswertung; Working Directory
  `/root/git/ModSecurity-conector`; Exit-Code `0`; Analyse beobachtet
  `2026-07-19T13:20:27Z`; Retention `retained_task_evidence`.

Zur Reproduktion werden die Components in der zurückgehaltenen Baseline mit
dem Präfix `Easton97-Jens_ModSecurity-conector:modules/ModSecurity-test-Framework/`
und dessen `/tools/MRTS/`-Subtree gezählt; anschließend ist das öffentliche
effektive Project-Setting `sonar.autoscan.enabled` auszulesen.

## Grundursache und vorgeschlagene Remediation

Der Projekt-Scope ist durch verschachtelte Framework-/MRTS-Pfade kontaminiert.
Das öffentliche effektive Setting `sonar.autoscan.enabled=true` und die
fehlende Parent-Scanner-Konfiguration stützen Automatic Analysis als aktiven
Mechanismus; diese Aufgabe hat jedoch weder Projektadministrations-Credential
noch Autorität, dieses externe Setting zu ändern.

Ein autorisierter SonarQube-Cloud-Administrator muss eine enge Ownership-
Grenze konfigurieren, die ausschließlich diese beiden verschachtelten
Repository-Bäume ausschließt, oder einen CI-gesteuerten Scanner mit explizitem
Parent-only-Source-Scope genehmigen. Die Lösung darf weder `NOSONAR`,
Regeldeaktivierung, Suppressions noch breite Parent-Source-Exclusions verwenden.

## Akzeptanzkriterien und Validierung

1. Eine frische SHA-gebundene Analyse enthält null Components und
   Issue-Records unterhalb der Framework- und MRTS-Pfade.
2. Parent-Source bleibt analysiert, und alle Parent-Regeln sowie Gate-Controls
   bleiben aktiv.
3. Die Scope-Änderung und die exakte resultierende Analysis-Revision sind ohne
   Secrets zurückgehalten.

Die Validierung muss die Post-Change-Issues paginieren, Parent-Zählungen und
Gate-Conditions vergleichen und belegen, dass keine verbotene Suppression oder
breite Exclusion eingeführt wurde. Eine repräsentative Parent-Component ist die
legitime Kontrolle.

## Abhängigkeiten, Blocker, verwandte Records und Restrisiko

Abhängigkeit und Blocker: SonarQube-Cloud-Projektadministrationszugriff oder
eine genehmigte CI-Scanner-Migrationsentscheidung. Verwandter Record:
`FND-SONAR-0001`.

Restrisiko: Projektweite Quality- und Security-Zählungen enthalten
verschachtelte Findings, die diese Parent-only-Aufgabe nicht ändern darf. Es
liegt keine Risikoakzeptanz durch den Benutzer vor.

## Historie

- `2026-07-19T13:30:00Z`: Aus der paginierten aktuellen Sonar-Baseline nach
  Deduplication gegenüber `FND-SONAR-0001` erstellt. Es wurden weder Nested
  Source noch Projekt-Settings geändert.
- `2026-07-19T14:09:34Z`: Ersetzende Current-Scope-Baseline erneut validiert —
  Remote-Parent-SHA `aabde81a9a315bf3e494e595ab0399357c596f9c` behält exakt
  dieselbe Zählung: 337 offene und 4 geschlossene ausschließlich zum Framework
  gehörende Records sowie 17 offene MRTS-Subtree-Records. Es wurden keine
  Nested Source, Projekt-Settings, Suppressions, Regeln oder Risikoakzeptanzen
  geändert; die autorisierte externe Scope-Korrektur bleibt blockiert.
