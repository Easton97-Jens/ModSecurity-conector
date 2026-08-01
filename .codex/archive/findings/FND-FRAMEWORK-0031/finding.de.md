# FND-FRAMEWORK-0031 — Umgehung des Action-Pins in einer Flow-Sequenz

- **Status:** auf resultierendem Framework-master verifiziert — Cloud-Revalidierung ausstehend
- **Schweregrad / Priorität:** hoch / P1
- **Cloud-Befund:** `48ddc89c01548191aac6fdc953d4a69b` (`new` im gelieferten Export)
- **Betroffene Framework-Revision:** `784977615acfc55567e37b863309abc4a38ac877`

## Root Cause und Auswirkung

`flow_mapping_uses_values()` beginnt die Action-Extraktion nach `{` oder einem
Komma in einer geschweiften Map, nicht aber nach `[`. Eine gültige
`steps: [uses: actions/setup-python@v6]`-Flow-Sequenz erreicht daher den
Full-SHA-Check nicht. Ein Pull Request könnte veränderliche externe Actions
trotz der Immutable-Pin-Sicherheitskontrolle verwenden.

## Behebung und Nachweis

Framework-PR [#38](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/38)
auf `8907c8ec047df070a579fab926e25b0d94dfbc2e` erkennt nun Mapping-Einträge
in Flow-Sequenzen nach `[` und enthält negative Mutable-Tag-/alternative
Komma- sowie positive Full-SHA-Tests. Der ursprüngliche negative Fall schlug
vor der Korrektur fehl; danach bestanden die fokussierte Suite (25 Tests), der
direkte Pin-Check echter Workflows, Python-Kompilierung, Change Record,
zweisprachige Dokumentations- und Dokumentationslink- sowie Diff-Checks.

Alle anwendbaren GitHub-Checks für genau diesen Head bestanden, darunter
CodeQL für actions/c-cpp/python, Secret-Scanning, OSV, OpenSSF Scorecard,
Workflow-Security-Quality und das SonarQube-Cloud-Quality-Gate (null neue
Issues und null Security Hotspots). Der PR ist reviewbereit, ohne
Review-Anforderung oder offenen Review-Thread. PR #38 wurde anschließend mit
dem exakten Merge-Commit `9dab40c2b8799dc1e4597cb2a2c223ec3f6cd72b` gemergt.
GitHub meldet den resultierenden Master-Tree
`4a91bfc7c47efef3b8e44d993e8f4ab1ed5a8cbc`, identisch zum geprüften
PR-Head-Tree; die ursprünglichen negativen und Full-SHA-Legitimate-Control-
Tests bestehen auf diesem Tree. Auch die resultierenden Master-Actions und
CodeQL-Checks bestehen.

Das master-only-SonarQube-Cloud-Ergebnis scheitert weiterhin an der
vorgefundenen Security-Rating-on-New-Code-E-Bedingung. Es wird getrennt als
`FND-SONAR-0002` geführt, dieser Änderung nicht kausal zugeschrieben und
verhindert ohne eigene Remediation oder Risikoentscheidung die aggregierte
Master-Integrationsverifikation. Der Cloud-Befund wird absichtlich nicht
geschlossen: Er bleibt `new`, bis ein exakter Codex-Cloud-Scan auf gemergtem
Framework-`master` vorliegt. Parent und MRTS bleiben außerhalb des Scopes und
unverändert.

Der Parent bleibt uncommitted und referenziert weiterhin Framework
`784977615acfc55567e37b863309abc4a38ac877`. Sein lokaler Submodule-Worktree
meldet vorübergehend eine Revisionsabweichung, weil der Framework-Checkout auf
das Merge-Ergebnis vorgerückt ist. Die vorgeschriebene nicht erzwingende
Restoration auf den Parent-referenzierten Commit ist derzeit blockiert, weil die
Sandbox den Framework-`index.lock`-Write verweigert; es wurde weder ein
Force-Checkout noch ein Parent-Pointer-Update versucht.

Die Exportquelle ist
`.codex/findings/codex-security-findings-2026-07-20T17-18-10.034Z.csv`
(SHA-256 `4836e7d8a1aba6088f1d125e7f48dd2cb333c2e7d4c1d19117d911c0aad45daf`).
Die vollständige abhängigkeitsgestützte lokale Permission-/Lint-Suite wurde
nicht ausgeführt, weil die Framework-eigene CPython-3.13.14-Umgebung fehlt;
die GitHub-CI für den exakten Head lief jedoch erfolgreich durch.
