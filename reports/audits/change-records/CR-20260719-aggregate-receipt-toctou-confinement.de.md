# Change Record: Descriptor-begrenzte Aggregate-Receipt-Veröffentlichung

**Sprache:** [English](CR-20260719-aggregate-receipt-toctou-confinement.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260719-aggregate-receipt-toctou-confinement` |
| Datum (UTC) | `2026-07-19` |
| Basis-Revision | `1fc2321cff39193f70113a3aefee49bae68db4c1` |
| Finding | `FND-PARENT-0037` |
| Grenze | Nur Parent-Aggregate-Receipt-Producer, Lifecycle-Manifest-Weitergabe, strikter Receipt-Consumer, fokussierte Tests und Dokumentation; Framework und MRTS bleiben unverändert. |

## Motivation und Problemstellung

Der `FND-PARENT-0031`-Helper prüfte Komponenten mit `lstat()` und öffnete später erneut den vollständigen Pfadnamen. Leaf-only-`O_NOFOLLOW` band Zwischenverzeichnisse nicht, sodass ein Matrix-Child mit derselben UID eines durch einen Symlink ersetzen, externe Bytes als In-Root-Input hashen oder die `verified-runs`-Veröffentlichung umleiten konnte. Der Lifecycle-Runner hasht den versiegelten Receipt außerdem erneut per Pfadname.

## Akzeptanzkriterien

- Jede Receipt-Artefaktlesung traversiert einen gepinnten `BUILD_ROOT`-Descriptor mit `O_DIRECTORY`, `O_NOFOLLOW` und `dir_fd`.
- Die Veröffentlichung erzeugt `verified-runs/<run-id>` und den exklusiven Receipt descriptor-relativ mit `fchmod` sowie File-/Directory-`fsync`; ein Pfadersatz schlägt fail-closed fehl und erzeugt keinen externen Receipt.
- Runner und Verified-Run-Manifest verwenden den descriptor-abgeleiteten Hash und die Bytezahl statt den Receipt erneut per Pfadname zu hashen.
- Deterministische Read-Swap- und Publication-Swap-Kontrollen schlagen fail-closed fehl; der gültige Zwölf-Zellen-Control und bestehende strikte Regressionen bleiben akzeptiert.
- Es werden weder Framework- noch MRTS-Source, Gitlink, Branch, Commit oder Merge verändert.

## Implementierungsentscheidung und Begründung

`ci/lib/verified_full_matrix_receipt.py` besitzt private Descriptor-Helper für Root, jede feste Directory-Komponente und jedes reguläre Leaf. Sie validieren Deskriptoren mit `fstat`, lehnen fehlende Sicherheitsflags ab und schließen Deskriptoren bei Erfolg und Fehler. Das kanonische Payload-Schema und die Zwölf-Zellen-Topologie bleiben erhalten, aber Raw-Matrix, Job-Receipts, Logs, Manifeste, Summaries und Result-JSONL werden über Deskriptoren gelesen.

Der Sealer liefert einen `{path, sha256, bytes}`-Record aus dem geschriebenen Descriptor. Er verifiziert, dass das geöffnete Receipt-Verzeichnis weiter dem descriptor-erreichbaren Namespace entspricht, und entfernt bei Fehler einen gerade erzeugten nicht erreichbaren File. Der Runner trägt den Record in das Manifest ein und verwendet für einen vorbestehenden Receipt nur eine descriptor-sichere Lesung. Der strikte Checker liest auch den Verified-Command-Receipt über die gepinnte Root, validiert den Aggregate-Receipt nach der Bindung des Parent-Commands und prüft beide Records vor Erfolg erneut, sodass ein Pfadersatz nach der Validierung fail-closed fehlschlägt.

Strukturierte JSON- und JSONL-Receipt-Inputs haben ein Limit von 1 MiB; Log- und Result-Records streamen Hashes, statt ganze Artefakte im Speicher zu halten. Das begrenzt untrusted strukturierte Speicherbelegung, ohne das kanonische Receipt-Schema zu ändern.

## Geänderte Dateien

- `ci/lib/verified_full_matrix_receipt.py`
- `ci/runtime/lifecycle/run-verified-report-run.py`
- `ci/checks/documentation/check-generated-report-layout.py`
- `tests/test_generated_report_evidence_integrity.py`
- dieses englisch/deutsche Change-Record-Paar und seine README-Indexlinks

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| In-Memory-`compile()`-Validierung geänderter Python-Module | Bestanden ohne checkout-lokale Bytecode-Dateien. |
| Fokussierte deterministische Read-Swap-, Publication-Swap- und No-Path-Rehash-Tests | Bestanden. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -q tests.test_generated_report_evidence_integrity` | Bestanden: 57 fokussierte Parent-Integritätstests. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python ci/checks/documentation/check-bilingual-docs.py` | In diesem isolierten Worktree blockiert: Sein erwarteter Framework-Gitlink `cdc91a3…` ist nicht ausgecheckt, deshalb können bestehende Cross-Repository-Links nicht aufgelöst werden. Die fokussierten `tests.test_bilingual_docs`-Prüfungen bestanden im kombinierten 68-Test-Lauf. |
| `rtk proxy git -C /var/tmp/codex/worktrees/parent-evidence-result-authenticity diff --check` | In der finalen lokalen Validierung bestanden. |

## Security-Auswirkung

Der validierte Intermediate-Symlink-Time-of-Check/Time-of-Use-Pfad ist für Receipt-Helper-Lesungen und Veröffentlichung geschlossen: Ein Directory-Descriptor und keine spätere Pfadnamenauflösung benennt jedes traversierte Objekt. Der Runner kann einen veränderbaren Pfad nach dem Sealen nicht mehr in neue angebliche Receipt-Metadaten umwandeln. Der strikte Consumer validiert Aggregate-Receipt und Command-Receipt außerdem unmittelbar vor Erfolg erneut, sodass deterministische Artefakt- und Command-Pfadersatzversuche nach der Validierung fail-closed fehlschlagen. Die `FND-PARENT-0031`-Producer-Authentizitätsbindung und `FND-PARENT-0030`-Consumer-Containment-Prüfungen bleiben erhalten.

Das Follow-up beim zuvor validierten PR-#59-Head
`d4f88b886dac6fd5f483940015d6310bc239f814` setzt
`SEALED_RECEIPT_MODE = stat.S_IRUSR`, macht den versiegelten Aggregate-Receipt
owner-read-only (Modus `0400`) und testet diesen Modus. Das begrenzt regulären
File-Mode-Zugriff nach dem Sealen, etabliert aber keine ACL-, Identitäts-,
Signatur- oder Same-UID-Isolationsgrenze. Es ist weder risk acceptance noch
`risk-accepted`, `verified` oder `closed` für dieses Finding.

## Runtime-Evidence

Nicht etabliert. Fokussierte temporäre Fixtures belegen betroffenes Parent-I/O-Verhalten, behaupten aber keinen Connector-Host, Request-Traffic, CRS-, Framework-, MRTS- oder Zwölf-Zellen-Runtime-Lauf.

## Bekannte Einschränkungen

Strikte Report-Evidence bleibt unabhängig durch das stale Cross-Evidence-Finding `FND-CROSS-0001` blockiert. Das Framework-eigene Phase-4-Identity-Finding `FND-CROSS-0006` liegt außerhalb dieses Parent-only Records und benötigt separate ausdrückliche Framework-Delivery-Autorisation.

## Verbleibende Risiken

Descriptor-relative Traversal und die finalen Rereads des strikten Consumers beseitigen die hier abgedeckten validierten Intermediate-Symlink- und Pfadersatz-Kontrollen nach der Validierung. Sie sind keine Signatur-, ACL-, Prozessisolation- oder externe-Attestation-Grenze: Eine Partei mit beliebigem Same-UID-Schreibzugriff liegt weiterhin außerhalb des durch diese lokalen Filesystem-Checks etablierten Vertrauensmodells.

## Nicht ausgeführte Prüfungen mit Begründung

Es werden kein echter Connector-/Runtime-Matrixlauf, kein externer
Komponentendownload, kein Framework- oder MRTS-Test behauptet. Diese Prüfungen
benötigen ihre isolierten Workflows und dürfen nicht durch Governance-only-
Validierung ersetzt werden. Die beobachtete frühere Exact-Head-Validierung des
Draft-Parent-PR #59 bei `d4f88b886dac6fd5f483940015d6310bc239f814` hatte 33
erfolgreiche und sechs übersprungene Checks; CodeQL und das SonarQube-Cloud-
Quality-Gate bestanden. Diese Evidenz gilt nur für
`d4f88b886dac6fd5f483940015d6310bc239f814`. Der Draft liegt hinter aktuellem
Parent-`master` `9ef0619b9c00729c16b7056943d7843785223095`, daher muss auf ein
reguläres Update frische Exact-Head-CI, CodeQL, SonarQube Cloud und PR-Review
vor der Readiness folgen; die ursprüngliche Reproduktion ist nach einem Merge
zu wiederholen. Keine Gitlink-Änderung und kein Merge erfolgten, und keine
Prüfung darf umgangen werden.

## Finaler Diff- und Review-Status

Der Draft-Parent-PR #59 ist der user-autorisierte gemeinsame/gestaffelte,
Parent-only-Delivery-Kandidat für `FND-PARENT-0030`, `FND-PARENT-0031` und
`FND-PARENT-0037`. Alle drei sind auf diesem Kandidaten fixed, aber keines ist
verified, closed oder risk-accepted. Er enthält das `0400`-
Sealed-Receipt-Hardening-Follow-up bei seinem zuvor validierten Head
`d4f88b886dac6fd5f483940015d6310bc239f814`; der Draft liegt hinter aktuellem
Parent-`master` `9ef0619b9c00729c16b7056943d7843785223095`. Ein reguläres
Update, frische Exact-Head-Checks und Review sowie die ursprüngliche
Reproduktion nach dem Merge bleiben erforderlich. Es wird keine Framework-,
MRTS- oder Gitlink-Änderung und kein Merge behauptet.
