# Change Record: Abgekoppelter Parent-Aggregate-Receipt für Full-Matrix-Evidence

**Sprache:** [English](CR-20260718-detached-aggregate-receipt.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260718-detached-aggregate-receipt` |
| Datum (UTC) | `2026-07-18` |
| Basis-Revision | `ffa7776ad43a851a78de87306ab846a35ae2fabb` |
| Finding | `FND-PARENT-0031` |
| Grenze | Nur Parent-Lifecycle-Producer, strikter Report-Evidence-Consumer, Full-Matrix-Report-Generator, fokussierte Tests und Dokumentation; Framework und MRTS bleiben unverändert. |

## Motivation und Problemstellung

`FND-PARENT-0030` ließ den strikten Consumer einen Result-Datei-Hash neu
berechnen, aber Result-Hash, zugehörige Child-`job.json` und Raw-Full-Matrix-
JSONL-Zeile konnten nach Abschluss des Child-Jobs weiterhin gemeinsam
umgeschrieben werden. Der Consumer verglich diese veränderbaren Dokumente
miteinander und akzeptierte eine gefälschte `PASS`-JSONL, wenn alle drei Felder
synchronisiert waren.

Die aufbewahrte Pre-Fix-Fixture reproduzierte genau diesen Weg: Das Ändern
einer Apache-Result-JSONL, ihres Child-Receipt-Hashs und ihrer Raw-Matrix-Zeile
erzeugte keine Fehler der strikten Kette. Dies ist eine separate
Producer-Authentizitäts-Root-Cause und wird nicht in die reine P0030-
Consumer-Änderung gemischt.

## Akzeptanzkriterien

- Der einzige repository-unterstützte Receipt-Erzeugungs-Call-Site ist der
  Parent-`run-verified-report-run.py`-Lifecycle-Pfad. Er erzeugt genau einen
  kanonischen `verified-runs/<run-id>/full-matrix-aggregate-receipt.json` nach
  einem vollständigen Full-Matrix- oder vollständigen Resume-Command. Dies ist
  keine Garantie einer Caller-Identität oder ACL.
- Der Receipt bindet valide Run-ID, Full-Profil, Integrationsmodus,
  normalisiertes Parent-Command-Ergebnis, Connector/Framework/MRTS-Revisionen,
  Raw-Manifest, alle zwölf Job-Receipts und ihre erforderlichen
  Log/Build-Manifest/Summary/Result-Artefakte über kanonische relative Pfade,
  Byte-Anzahlen und SHA-256-Werte.
- Der strikte Consumer leitet den kanonischen Receipt-Pfad ab, prüft ihn gegen
  das Verified-Run-Manifest, berechnet jedes versiegelte Feld neu und weist
  gekoppelte veränderbare Leaf/Job/Raw-Umschreibung, Raw-only-Umschreibung,
  nichtregulären oder Symlink-Receipt, kopierte/fremde Identität,
  unvollständige Matrix und inkonsistenten Hash zurück.
- Report-Refresh kann keinen Receipt prägen. `--rewrite-manifest` validiert
  zuerst, dass seine gewählte Run-ID alle aktuellen Raw-Source-Zeilen besitzt;
  hat dieser Lauf einen Receipt, beweist es identische vorgeschlagene
  Raw-Manifest-Bytes und lässt die Quelle unverändert, andernfalls weist es die
  Umschreibung zurück.
- Eine vollständige valide Kontrolle und ein vollständiges `full-matrix-resume`
  nach einem unvollständigen ersten Versuch bleiben akzeptiert. Ein Receipt hat
  keinen Self-Hash.

## Implementierungsentscheidung und Begründung

`ci/lib/verified_full_matrix_receipt.py` ist ein Parent-only-Shared-Helper für
Producer und Consumer. Er leitet jeden Ort aus Build-Root und der festen
3 × 2 × 2-Matrix ab und vertraut keinem Child-gelieferten Artefaktpfad. Er
weist statisch beobachtete escapte, symlinkte, nichtreguläre, sich ändernde
oder malformatierte Dateien beim Hashing zurück und schreibt das finale JSON
mit exklusiver Erstellung plus `fsync`. Existierende Receipts werden validiert,
niemals überschrieben. Die getrennte `FND-PARENT-0032`-Remediation ist nötig,
bevor Resistenz gegen einen konkurrierenden Zwischenverzeichnis-Swap zwischen
Pfadprüfung und Nutzung behauptet werden kann.

Der Parent-Lifecycle-Runner ruft den Sealer nur auf, nachdem er seine eigene
Runtime-Completion-Semantik auf `full-matrix-parallel` oder
`full-matrix-resume` angewendet hat. `--manifest-only`, Report-Refresh und der
Child-Shell-Runner besitzen keinen Sealer-Aufruf. Der Runner erfasst einen
Sealing-Fehler als erforderlichen Evidence-Fehler statt ihn in einen
Report-Governance-Erfolg umzudeuten. Das Verified-Run-Manifest erhält einen
diagnostischen Pfad/Hash/Byte-Record, aber der strikte Checker leitet den
Receipt-Ort weiterhin selbst ab.

Der Full-Matrix-Generator validiert die Run-ID der aktuellen Raw-Source, bevor
er einen Receipt auswählt. Er kann keine vom Aufrufer gelieferte fremde Run-ID
nutzen, um ein versiegeltes Raw-Manifest umzuschreiben, und er kann die
ausgewählte versiegelte Quelle nicht auf eine andere Byte-Sequenz umschreiben.
Damit bleibt normale Report-Generierung für die bestehende kanonische
Byte-Sequenz möglich, ohne dass sie zur Autorität wird, synchronisierte
Child-Evidence neu zu prägen.

## Security-Auswirkung

Die strikte Kette besitzt nun eine Parent-erzeugte Aggregate-Bindung zwischen
dem tatsächlichen Full-Matrix-Parent-Command und veränderbaren Child-
Artefakten. Sie erkennt die validierte Post-Runtime-Umschreibklasse, statt
gegenseitig konsistente Child-Records als Beweis zu behandeln. Sie bindet den
Receipt außerdem an Profil, Integrationsmodus, Revisionen, Run-ID und die
exakte Zwölf-Zellen-Topologie.

Dies etabliert für sich keinen realen Connector-Host/Prozess/Traffic-Nachweis;
diese Grenzen bleiben separat verfolgt. Es behauptet auch keine kryptografische
Signatur oder Privileggrenze gegenüber beliebigem Same-UID-Code, der den
Receipt nach Parent-Sealing umschreiben kann. Ebenso wird nicht behauptet,
dass die aktuelle pfadnamenbasierte Implementierung einem konkurrierenden
Zwischenverzeichnis-Swap widersteht; dieses getrennte Path-Confinement-Finding
wird als `FND-PARENT-0032` verfolgt.

## Runtime-Evidence

Nicht etabliert. Fokussierte temporäre Fixtures modellieren vollständige
kanonische Datei-Topologie, damit Producer/Consumer-Integritätskontrollen ohne
Behauptung eines echten Connector-Hosts, Request-Traffics, CRS-, MRTS- oder
Framework-Runs ausgeübt werden können. Kein Governance-only-Check wird als
Runtime-Evidence dargestellt.

## Bekannte Einschränkungen

Dem isolierten Worktree fehlen provisionierte Runtime-Komponenten und der
autoritative Framework-Harness, daher kann hier keine echte Zwölf-Zellen-
Runtime laufen. Die aufbewahrten Repository-Reports bleiben korrekt durch das
unabhängige stale-Cross-Evidence-Finding `FND-CROSS-0001` am Strict-Gate
blockiert.

## Verbleibende Risiken

Der Receipt ist eine deterministische SHA-256-Kette, keine Signatur oder
externe Attestierung. Ein Akteur mit beliebiger Same-UID-Schreibberechtigung
nach dem Sealing kann auch einen unsignierten Receipt ersetzen; dies benötigt
eine getrennte Runner-eigene Storage-, ACL-, Identitäts- oder
External-Attestation-Kontrolle. Dieses Risiko wird weder akzeptiert noch durch
diese Änderung verborgen.

Ein konkurrierendes Matrix-Child kann außerdem die gegenwärtigen lexikalischen
Pfadprüfungen durch Austauschen eines Zwischenverzeichnisses nach dessen
Prüfung rennen. `FND-PARENT-0032` verfolgt die notwendige
Descriptor-relative Traversal-/Publikations-Reparatur auf einem getrennten
Path-Confinement-Branch; dieser Record überhöht diese Kontrolle nicht.

## Geänderte Dateien

- `ci/lib/verified_full_matrix_receipt.py`
- `ci/runtime/lifecycle/run-verified-report-run.py`
- `ci/checks/documentation/check-generated-report-layout.py`
- `ci/evidence/reports/generate-full-matrix-job-completeness.py`
- `tests/test_generated_report_evidence_integrity.py`
- dieses englische/deutsche Change-Record-Paar und seine README-Indexlinks

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| Fokussierte gekoppelte veränderbare `PASS`/Job/Raw-Fixture vor dem Producer-Fix | Erwartet fehlgeschlagen: Der alte Consumer lieferte keine Fehler für die synchronisierte Fälschung. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_generated_report_evidence_integrity` | Bestanden: 39 Tests decken valide Kontrolle, gekoppelte und alternative Umschreibungen, Raw-only-Mutation, Pfad/Symlink, Revisionsbindung, unvollständig, Single-Seal, Resume/Current-Run-Bindung, No-Governance-Minting, Selbstreferenz, P0030-Kontrollen, versiegeltes Generator-Verhalten und fremde-Run-Rewrite-Zurückweisung ab. |
| In-Memory-`compile()`-Validierung geänderter Python-Module | Bestanden ohne checkout-lokale Bytecode-Schreibvorgänge. |
| `rtk git diff --check` | Bestanden. |

## Nicht ausgeführte Prüfungen mit Begründung

Der reale Connector-/Runtime-Harness, die vollständige externe
Komponentenmatrix, Exact-Head-CI, CodeQL, SonarQube Cloud und PR-Review
benötigen die separat provisionierte Umgebung oder den zukünftigen Draft-PR.
Ihr Fehlen autorisiert keinen synthetischen Erfolg, Governance-only-Ersatz,
Framework/MRTS-Change oder Merge.

## Finaler Diff- und Review-Status

Die Fixture-first-Implementierung läuft auf ihrem eigenen gestapelten
Parent-Branch. Unabhängiges Security-Review, finale lokale Checks,
Exact-Head-Delivery-Checks und ein separater Draft-PR bleiben erforderlich.
Kein Merge ist autorisiert.
