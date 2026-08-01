# FND-FRAMEWORK-0014 — CRS-Version-Pinning-Check verwendete vorhersagbare temporäre Dateien und verlustbehaftete Pfaditeration

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-FRAMEWORK-0014` |
| Kategorie | `security_hardening` |
| Repository / Ownership | `framework` / `framework` |
| Priorität / Schwere | `P2` / `medium` |
| Confidence / Status | `validated` / `fixed` |
| Machbarkeit | `feasible_now` |
| Release-Blocker | `false` |
| Security-relevant | `true` |

## Zusammenfassung

Der CRS-Version-Pinning-Shell-Validator schrieb Scan-Ausgabe in einen
vorhersagbaren gemeinsam genutzten `/tmp`-Dateinamen und enumerierte Shell-
Pfade mit Word-Splitting. Dadurch entstanden Same-Host-Interferenz und eine
Coverage-Lücke für Dateinamen mit Whitespace.

## Evidence und Remediation

`ci/checks/catalog/check-crs-version-pinning.sh` validiert jetzt seine Runner-
Temporary-Root, setzt `umask 077`, verwendet private `mktemp`-Dateien, räumt
sie per Trap auf, prüft grep-Fehler und übergibt NUL-delimitierte Pfade durch
einen rekursiven `--check-path`-Modus. Die committete Remediation ist
`768a06b5b734547f8213cc6918c26ef4a8ef9f67`. Die exakte lokale HEAD-
Validierung bestand `make lint`, Shell-Syntax, den CRS-Pinning-Contract-Test und
Whitespace-Checks; die aufbewahrte Artefakt-SHA-256 ist
`979715e7ec9a24e700f04ab6722b5f717b1f229023a6c4de6051c675a79155c5`.

## Akzeptanzkriterien

- Kein vorhersagbarer globaler temporärer Dateiname wird verwendet.
- Shell-Dateinamen mit Whitespace werden exakt einmal geprüft.
- Fehler bei Pfad-Enumeration oder Scan lassen den Validator fehlschlagen.
- Exakte Final-PR-Head-CI bestätigt das committete Verhalten.

## Restrisiko und Historie

Die lokale Reparatur ist verifiziert; Remote-Exact-Head-CI- und Review-Evidence
stehen aus. `2026-07-18T15:18:00Z`: erstellt und lokal mit aufbewahrter
Evidence repariert.
