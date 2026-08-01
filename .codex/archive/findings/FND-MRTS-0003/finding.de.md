# FND-MRTS-0003 — MRTS-Runner-Profilvertrag widersprach einer nutzergenehmigten lokalen Konfiguration

## Identität

| Feld | Wert |
| --- | --- |
| ID | \`FND-MRTS-0003\` |
| Kategorie | \`documentation_drift\` |
| Repository | \`mrts\` |
| Ownership | \`mrts_explicit_user_task\` |
| Priorität | \`P2\` |
| Severity | \`not_applicable\` |
| Confidence | \`confirmed\` |
| Status | \`not_applicable\` (archiviert) |
| Feasibility | \`not_applicable\` |
| Release-Blocker | \`false\` |
| Security-relevant | \`false\` |
| Profil | \`MRTS shared local Codex runner profile\` |

## Aktuelle Disposition

**Verdikt: `not_applicable` als Produkt-Sicherheitsbefund.** Der aktuelle
Nutzer bestätigte, dass die aufbewahrte Framework-artige MRTS-Konfiguration das
beabsichtigte vertrauenswürdige lokale Runner-Profil ist. Parent und Framework
verwenden denselben Profiltyp; der MRTS-spezifische restriktive Vertrag war
Dokumentations-/Validator-Drift.

### Beobachtetes und erwartetes Verhalten

Die Live-Konfiguration entspricht dem aufbewahrten Snapshot SHA-256
`ee2e0437e2c5c3b8926b96ff68b617197140bea2602a8b8e094d4c1686ec0cfb`.
Sie deklariert den aktiven MRTS-Workspace plus vier exakte beschreibbare
Support-Wurzeln, Netzwerkzugriff, Slash-TMP-Ausschluss, die explizite
MRTS-TMPDIR-Pfadzuordnung, `inherit = "all"`, Default-Secret-Ausschlüsse und
eine nicht geheime Umgebungszuordnung. Das Strukturmanifest deklariert dasselbe
Profil; der native Validator lehnt Abweichungen davon ab, statt die gewollte
Konfiguration zu verbieten.

### Grenze, Auswirkung und Evidence

Die ignorierte lokale Konfiguration ist vertrauenswürdige Operator-Eingabe. Es
gibt keinen Nachweis eines weniger privilegierten oder Remote-Writers, einer
unterstützten Produktgrenze oder eines Live-Sandbox-Escapes. Der aufbewahrte
Profil-Snapshot und der statische Vergleich mit Parent/Framework widerlegen
daher den ursprünglichen Sicherheitsclaim. Dies bleibt lokale deklarative
Evidence, kein Beweis von Runtime-Dateisystem- oder Netzwerk-Enforcement.

Betroffen bleiben `.codex/config.toml`, `.codex/structure-manifest.toml`, die
direkt widersprüchlichen MRTS-Governance-Policies,
`tools/validate-governance.py`, `tools/test_validate_governance.py` und die
von ihnen validierten Sandbox-/Umgebungseinstellungen. Keine Produktgenerator-,
Dependency-, Git-, Gitlink-, Remote- oder Delivery-Oberfläche wurde geändert.

### Auflösung und Validierung

Das exakte aufbewahrte Profil wurde wiederhergestellt und Manifest, Validator,
fokussierte Tests sowie direkt widersprüchliche Dokumentation wurden
ausgerichtet. Explizite Secret-Ausschlüsse, No-MCP/Plugin-Checks, `on-request`,
deaktivierte Login-Shells und die separaten Task-Autorisierungs-/Gitlink-Grenzen
bleiben erzwungen.

- TOML-Parsing von MRTS-Config und Manifest bestand.
- Der native MRTS-Governance-Validator bestand.
- Sechs fokussierte MRTS-Governance-Tests bestanden, einschließlich
  Profilabweichungs- und Manifest-gesteuerter Umgebungstabellen-Fälle.
- Die Parent-MRTS-scoped- und All-Root-Vererbungsvalidatoren bestanden; das
  All-Root-Ergebnis behielt nur vier bereits dokumentierte Parent-Warnungen.
- Die Parent-Control-Plane-Suite bestand 133 Tests.

Restrisiko: Das nutzergenehmigte Profil deklariert Netzwerkzugriff und
Support-Wurzeln für vertrauenswürdige lokale Arbeit. Es beweist nicht, dass eine
Runtime diese Einstellungen erzwang, und nicht zusammenhängende parallele
Workspace-Änderungen verhindern weiterhin eine vollständige
Whole-Workspace-Continuity-Aussage.

## Historischer Datensatz — überholte Evidenz des restriktiven Vertrags

Eine ignorierte lokale MRTS-Codex-Konfiguration wurde durch eine breitere Framework-artige Konfiguration ersetzt. Der native Governance-Validator reproduzierte sechs Verstöße: aktiviertes Netzwerk, breite Schreibwurzeln, erlaubtes geerbtes TMPDIR, vollständige Umgebungsvererbung, eine injizierte Umgebungs-Tabelle und einen expliziten Netzwerk-Aktivierungsmarker. Eine reine Konfigurationsrestaurierung stellte den dokumentierten Default-Deny-Vertrag wieder her. Der ursprüngliche native Validator, seine fünf fokussierten Regressionstests und der scoped Parent-Vererbungsvalidator bestehen wieder. Dies ist eine verifizierte statische Control-Recovery, kein Beweis dafür, dass eine Live-Session die deklarierte Sandbox anwendete oder umging.

## Beobachtetes und erwartetes Verhalten

Vor der Reparatur hatte MRTS \`.codex/config.toml\` \`network_access = true\`, vier Nicht-MRTS-Schreibwurzeln, \`exclude_tmpdir_env_var = false\`, \`inherit = "all"\` und eine Tabelle \`[shell_environment_policy.set]\`. Der native \`tools/validate-governance.py\` endete mit \`1\` und sechs Konfigurationsfehlern; der Parent-Validator meldete zusätzlich \`mrts:config_environment_inherit\` und endete mit \`1\`.

Die erwartete Konfiguration ist der restriktive deklarative Vertrag der aktuellen MRTS-Policy: deaktiviertes Netzwerk; exakt \`/var/tmp/codex/ModSecurity-conector/mrts-sandbox\` als deklarierte externe Schreibwurzel; Slash-TMP- und geerbte-TMPDIR-Ausschlüsse; \`inherit = "core"\`; und keine injizierte Umgebungs-Tabelle. Die Deklaration verleiht weder zusätzliche Task-Autorität noch beweist sie Runtime-Enforcement.

## Auswirkung und Scope

Wenn eine Codex-Session die aufgeweitete lokale Konfiguration auflöst und nutzt, kann sie bedingt Netzwerk-Egress, Schreibzugriffe außerhalb der MRTS-Grenze, Sichtbarkeit der vollständigen geerbten Umgebung und injizierten Tool-/Pfadstatus erhalten. Es gibt keine Evidence dafür, dass ein nicht vertrauenswürdiger Remote-Akteur diese ignorierte lokale Datei kontrollierte, dass diese Parent-Root-Session sie lud oder dass ein Live-Sandbox-Escape stattfand.

Betroffene Control-Plane-Dateien und Symbole:

- \`.codex/config.toml\`, \`.codex/structure-manifest.toml\`, \`.codex/context/security.md\`, \`.codex/context/read-only-policy.md\` und \`.codex/context/governance-validation.md\`;
- \`tools/validate-governance.py\` und \`tools/test_validate_governance.py\`;
- \`sandbox_workspace_write.network_access\`, \`sandbox_workspace_write.writable_roots\`, \`sandbox_workspace_write.exclude_tmpdir_env_var\`, \`shell_environment_policy.inherit\` und \`shell_environment_policy.set\`.

## Voraussetzungen und Reproduktion

Die Bedingung erfordert einen Principal oder Prozess, der die ignorierte lokale MRTS-\`.codex/config.toml\` ändern kann, gefolgt von einer Codex-Session, die diese Konfiguration auflöst und nutzt.

1. Das aufbewahrte Pre-Remediation-Snapshot mit SHA-256 \`2eb63d56f02fa9b76a35f5b6b21916bf6b47d9d8ab594d0230b573374c18ea4b\` prüfen.
2. Vom MRTS-Root aus \`rtk proxy env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python tools/validate-governance.py\` ausführen. Die Pre-Remediation-Konfiguration endet mit \`1\` und den sechs deklarierten Vertragsverletzungen.
3. Vom Parent-Root aus \`rtk proxy /root/git/ModSecurity-conector/.venv/bin/python .codex/bin/validate-codex-inheritance.py --check --repository mrts --json --explain\` ausführen. Die Pre-Remediation-Konfiguration endet mit \`1\` und \`config_environment_inherit\`.

## Evidence

| Artefakt | SHA-256 | Command / Ergebnis |
| --- | --- | --- |
| \`/var/tmp/codex/ModSecurity-conector/runs/20260726T041432Z-codex-control-plane-unification-d42a1961/evidence/security-remediation/mrts-config-before-remediation.toml\` | \`2eb63d56f02fa9b76a35f5b6b21916bf6b47d9d8ab594d0230b573374c18ea4b\` | Nativer MRTS-Validator, MRTS-Root, Exit \`1\`, beobachtet \`2026-07-26T05:15:58Z\`. |
| \`/var/tmp/codex/ModSecurity-conector/runs/20260726T041432Z-codex-control-plane-unification-d42a1961/evidence/security-remediation/mrts-config-after-remediation.toml\` | \`c8897b0c3489e145b2bb7b1a9b103638bbe8217233e9bc8e6ca0fa79af523a85\` | Nativer MRTS-Validator und Parent-MRTS-scoped-Validator, Exit \`0\`, beobachtet \`2026-07-26T05:23:33Z\`. |

Beide sind aufbewahrte Task-Evidence für den Run \`20260726T041432Z-codex-control-plane-unification-d42a1961\`.

## Root Cause und Remediation

Ein paralleles lokales Überschreiben ersetzte MRTS-spezifische deklarierte Sandbox-Vertragswerte durch Framework-artige Konfigurationswerte. Die Config ist ignoriert und hat keinen getrackten Git-Baseline, daher war ein Git-Restore weder verfügbar noch angemessen.

Die minimale Remediation änderte nur die verletzten Konfigurationskontrollen: Netzwerk deaktiviert, die eine genehmigte externe Wurzel, beide Temporary-Root-Ausschlüsse, \`core\`-Vererbung und Entfernung der injizierten Umgebungs-Tabelle. Sie bewahrte nicht zusammenhängende aktuelle Top-Level-Feature- und Agent-Deklarationen und änderte weder Policy, Validator, Produkt, Git, Gitlink, Remote, Dependency noch Delivery-Status.

## Akzeptanzkriterien und Validierung

- \`network_access = false\` und exakt \`/var/tmp/codex/ModSecurity-conector/mrts-sandbox\` sind deklariert.
- Beide Temporary-Root-Ausschlüsse, \`inherit = "core"\` und keine \`[shell_environment_policy.set]\`-Tabelle sind deklariert.
- Der ursprüngliche MRTS-Governance-Validator endet mit \`0\`.
- Der Parent-MRTS-scoped-Vererbungsvalidator endet ohne Konfigurationsverletzung mit \`0\`.
- \`tools/test_validate_governance.py::GovernanceValidatorTests.test_workspace_sandbox_contract_rejects_broader_settings\` ist durch die fünf bestandenen fokussierten Tests abgedeckt.
- Keine Produktquelle, Testquelle, Git-, Gitlink-, Remote-, Dependency- oder Delivery-Aktion wurde geändert.

Der Security-Closure-Nachweis erfolgte durch erneutes Ausführen des ursprünglichen nativen Validators und des Parent-MRTS-scoped-Validators nach der Konfigurationsreparatur. Das legitime Control-Verhalten zeigte die normale Erfolgsmeldung des nativen Validators und seine fünf fokussierten Tests, die breitere Wurzeln, Netzwerkzugang, Temporary-Root-Ausschlüsse, \`inherit = "all"\` und Umgebungsinjektion ausüben.

## Abhängigkeiten, Blocker und Restrisiko

Es gibt keine Remediation-Abhängigkeiten oder Blocker. Verwandtes Finding: \`FND-MRTS-0002\`.

Konfiguration und Validatoren bleiben nur lokale Governance-Evidence. Eine separate umgebungsbezogene Untersuchung ist erforderlich, bevor behauptet wird, dass eine Codex-Runtime die MRTS-Config lud oder dass Filesystem-/Netzwerk-Enforcement aktiv war. Parallele nicht task-eigene Parent-, Framework-, MRTS- und ignorierte Control-Plane-Änderungen verhindern weiterhin eine Whole-Workspace-Continuity-Aussage.

## Historie

- \`2026-07-26T05:15:58Z\` — statische Control-Regression beobachtet.
- \`2026-07-26T05:23:33Z\` — minimale Konfigurationsrestaurierung verifiziert.
