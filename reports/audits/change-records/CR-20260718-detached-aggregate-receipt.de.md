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
niemals überschrieben. Der speziell validierte Aggregate-Receipt-
Zwischenverzeichnis-Swap wird durch die descriptor-relative
Traversal-/Publikations-Remediation in `FND-PARENT-0037` adressiert, die im
selben gemeinsamen Parent-Kandidaten enthalten ist. Dieser Record behauptet
keine unabhängige Verifikation dieser Remediation. `FND-PARENT-0032` bleibt ein
eigenständiges historisches Finding und wird hier weder umbenannt noch
geschlossen.

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
dass dieser Record Resistenz gegen einen konkurrierenden
Zwischenverzeichnis-Swap unabhängig verifiziert. Die zugehörige
descriptor-relative Reparatur wird als `FND-PARENT-0037` im selben gemeinsamen
Kandidaten verfolgt und benötigt weiter frische Exact-Head-Validierung.
`FND-PARENT-0032` bleibt ein eigenständiges historisches Finding und wird durch
diese Arbeit weder umbenannt noch geschlossen.

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

Die speziell validierte Zwischenverzeichnis-Swap-Klasse wird durch die
descriptor-relative Traversal-/Publikations-Reparatur in `FND-PARENT-0037`
adressiert, die im selben gemeinsamen Kandidaten enthalten ist und weiter
frische Exact-Head-Validierung erwartet. `FND-PARENT-0032` bleibt ein
eigenständiges historisches Finding; es ist weder gleichbedeutend mit noch
durch `FND-PARENT-0037` geschlossen. Dieser Record überhöht keine der beiden
Kontrollen.

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

Der reale Connector-/Runtime-Harness und die vollständige externe
Komponentenmatrix benötigen die separat provisionierte Umgebung. Ihr Fehlen
autorisiert keinen synthetischen Erfolg oder Governance-only-Ersatz. Die
beobachtete frühere Exact-Head-Validierung des Draft-Parent-PR #59 bei
`d4f88b886dac6fd5f483940015d6310bc239f814` hatte 33 erfolgreiche und sechs
übersprungene Checks; CodeQL und das SonarQube-Cloud-Quality-Gate bestanden.
Diese Evidenz gilt nur für `d4f88b886dac6fd5f483940015d6310bc239f814`. Dieser
Kandidat enthält nun eine normale lokale Synchronisierung von Parent-`master`
`6f80c90592fdd1f2eb990fe1514fdfc4efbf01e8` und bleibt ein Draft. Sein nächster
gepushter Exact Head muss vor der Readiness frische Exact-Head-CI, CodeQL,
SonarQube Cloud und PR-Review erhalten; die ursprüngliche Reproduktion ist nach
einem Merge zu wiederholen. Kein Framework- oder MRTS-Test, keine task-eigene
Gitlink-Änderung und keine Parent-master-Integration erfolgten, und keine
Prüfung darf umgangen werden.

Dieser Kandidat enthält außerdem die eng begrenzte, verhaltensgleiche
`FND-SONAR-0006`-Nacharbeit für alle acht bei diesem Stand ermittelten
PR-SonarQube-Cloud-Maintainability-Code-Smells: Helper-Extraktionen im strikten
Consumer, Aggregate-Receipt-Generator und Runner, eine Konstante für
wiederholte Run-ID-Diagnostik und eine präzisere Tamper-Assertion. Die neue
lokale 57-Test-Receipt-Integrity-Suite, `sh -n`, der Bilingual-Check und
`git diff --check` bestanden. Keine Receipt-, Pfad-, Hash- oder
TOCTOU-Kontrolle wird geändert oder unterdrückt; ein neuer exakter Head muss
vor der Readiness erneut SonarQube Cloud durchlaufen.

## Finaler Diff- und Review-Status

Der Draft-Parent-PR #59 ist der user-autorisierte gemeinsame/gestaffelte,
Parent-only-Delivery-Kandidat für `FND-PARENT-0030`, `FND-PARENT-0031` und
`FND-PARENT-0037`. Alle drei sind auf diesem Kandidaten fixed, aber keines ist
verified, closed oder risk-accepted. Sein zuvor validierter Head ist
`d4f88b886dac6fd5f483940015d6310bc239f814`; dieser Kandidat enthält nun eine
normale lokale Synchronisierung von Parent-`master`
`6f80c90592fdd1f2eb990fe1514fdfc4efbf01e8` und bleibt ein Draft. Frische
Exact-Head-Checks und Review sowie die ursprüngliche Reproduktion nach dem
Merge bleiben erforderlich. Es wird keine Framework-, MRTS- oder task-eigene
Gitlink-Änderung und keine Parent-master-Integration behauptet.
