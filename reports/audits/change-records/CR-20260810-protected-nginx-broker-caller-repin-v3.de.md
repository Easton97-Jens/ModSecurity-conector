# Change Record

**Sprache:** [English](CR-20260810-protected-nginx-broker-caller-repin-v3.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260810-protected-nginx-broker-caller-repin-v3 |
| Datum (UTC) | 2026-08-10 |
| Basis-Revision | 34f62b11aa3726b0cc781014531d62422ed9bff9 |
| Vorheriger geschützter Broker-SHA | 1df2fcbd0c764c52253348a29034ff9e9b1bf7e2 |
| Aktiver geschützter Broker-SHA | 409caa5b9664bcb8e1919d35684575e00a959f6a |
| Broker-Framework-Gitlink | 03880bf66b3905940466ff10b3a431a27ecc6b26 |

## Motivation und Problemstellung

Der geschützte Caller muss die unveränderliche Broker-Revision auswählen, die
den aktiven ABI-Loader-Schutz enthält. Dieser vollständige Parent-Caller-Repin
hält das exakte Caller-Tupel fest: Broker
`409caa5b9664bcb8e1919d35684575e00a959f6a` und Framework-Gitlink
`03880bf66b3905940466ff10b3a431a27ecc6b26`. Der vorherige Broker-SHA bleibt
hier nur als Vorgängeridentität erhalten; historische Change Records,
einschließlich des beobachteten fail-closed Runner-Fehlers, werden nicht
geändert.

## Akzeptanzkriterien

Die englischen und deutschen Trusted-Broker-Guides nennen denselben aktiven
SHA-40-Broker und Framework-Gitlink, beschreiben den ABI-Loader-Vertrag als
aktiv und halten weiterhin fest, dass noch kein Protected-master-Lifecycle
bestanden hat. Dieser Record und sein deutsches Gegenstück müssen sich
wechselseitig verlinken und festhalten, dass der Repin weder Framework, MRTS
noch einen Gitlink ändert.

## Implementierungsentscheidung und Begründung

Der vollständige Repin ändert den geschützten Caller-Workflow, seinen
Caller-Helper, den Python-Version-Contract-Checker, fokussierte
Caller-/Workflow-Testmodule, die gepaarten Trusted-Broker-Guides und diesen
gepaarten v3 Change Record. Die unveränderliche `uses`-Referenz und die
`protected_broker_sha`-Identität bilden die Auswahlgrenze des privilegierten
Reusable-Workflows: Weder Branch, Tag, Caller-wählbarer Source, Root-Aktion,
Profil, Permission, Secret, Executable noch Pfad wird eingeführt. Die
Framework-Identität bleibt der feste Mode-160000-Gitlink des Broker-Trees.

## Geänderte Dateien

- .github/workflows/run-protected-nginx-root-broker.yml
- ci/runtime/broker/protected_nginx_broker_caller.py
- ci/checks/common/check-python-version-contract.py
- tests/test_ci_security_workflows.py
- tests/test_nginx_root_broker.py
- docs/security/trusted-nginx-root-broker.md
- docs/security/trusted-nginx-root-broker.de.md
- dieser Change Record
- CR-20260810-protected-nginx-broker-caller-repin-v3.md

## Tests und tatsächliche Ergebnisse

Es wurde kein Hosted-, Root- oder Runtime-Lifecycle ausgeführt. Die zweite
scopierte Dokumentationsprüfung meldete keinen Change-Record-Überschriften-
oder Identitätsfehler für dieses Paar; sie blieb nur wegen 20 bereits
bestehender fehlender Framework-Gitlink-Ziele an anderer Stelle im
unmaterialisierten Task-Worktree blockiert. Die scopierte Whitespace-Prüfung
bestand. Fokussierte lokale Befehlsresultate gehören zur Delivery-Evidence.

## Ausgeführte Befehle

- `rtk proxy make check-bilingual-docs` — BLOCKIERT im ersten Lauf: Den neuen
  Records fehlten erforderliche Template-Überschriften, und dem Task-Worktree
  fehlen außerdem die Framework-Gitlink-Ziele, die von 20 bestehenden
  Dokumenten referenziert werden.
- `rtk proxy make check-bilingual-docs` — nach Template-Korrektur nur durch
  diese 20 bereits bestehenden fehlenden Framework-Gitlink-Ziele BLOCKIERT;
  es wurde kein Fehler für einen der beiden v3-Records gemeldet.
- `rtk proxy make check-doc-links` — nur durch 16 bereits bestehende fehlende
  Framework-Gitlink-Ziele außerhalb dieser scopierten Änderung BLOCKIERT.
- `rtk proxy git diff --check -- <zwei getrackte Guides>` — PASS.
- `rtk proxy git diff --no-index --check /dev/null <jeder neue v3-Record>` —
  PASS.
- `rtk proxy rg -n <alter/neuer Broker-SHA und Framework-SHA> <vier scopierte
  Dateien>` — PASS: Die Guides enthalten nur den aktiven Broker-SHA; der
  Vorgänger-SHA bleibt nur im neuen Change Record als historische Identität.

## Security-Auswirkung

Die unveränderliche `uses`-Referenz und die `protected_broker_sha`-Identität
bleiben die Auswahlgrenze des privilegierten Reusable-Workflows. Der Repin
fügt weder eine bewegliche Referenz noch Caller-kontrollierte Autorität über
Source, Root-Aktion, Profil, Permission, Secret, Executable oder Pfad hinzu.

## Runtime-Evidence

Der historische fail-closed Runner-Fehler bleibt als historische Evidenz
erhalten. Für diesen vollständigen Caller-Repin lief kein resultierender-master-
geschützter Lifecycle.

## Bekannte Einschränkungen

Die zwei bereits bestehenden SonarQube-WONTFIX/Accepted-Baseline-Einträge sind
von diesem vollständigen Caller-Repin ausgeschlossen und werden weder neu
bewertet noch geändert. Es werden keine Framework- oder MRTS-Source-, Branch-,
Commit-, Pull-Request- oder Gitlink-Änderungen vorgenommen. Kein historischer
Change Record wird verändert.

## Verbleibende Risiken

Der ausgewählte unveränderliche Broker benötigt weiterhin einen späteren
Protected-master-Lifecycle, um Runtime-Evidence zu erzeugen.

## Nicht ausgeführte Prüfungen mit Begründung

Es wurde kein Hosted-/Root-/Runtime-Lifecycle ausgeführt. Root-Admission,
NGINX-Start, CRS-Fetch, Audit-Evidence, Artefakttransport, Evidence-Readback,
Stop und Cleanup benötigen den späteren geschützten GitHub-hosted-Workflow.

## Ausstehendes Lifecycle-Gate

Diese Änderung behauptet keinen erfolgreichen geschützten Lifecycle. Nach
normalem Merge und Exact-Head-Verifikation muss ein neuer Protected-master-
Dispatch beide No-CRS- und OWASP-CRS-Profile, Identity-Bindings, Root-Master- /
Non-Root-Worker-Verhalten, Evidence-Readback, Stop und Cleanup beweisen.
Hosted Checks, Review, Branch Protection, CodeQL, SonarQube Cloud, Merge und
dieser Lifecycle bleiben Delivery-Gates.

## Finaler Review-Status

Die Dokumentationsimplementierung ist erst vollständig, wenn die für diese
Änderung aufgezeichneten scopierten Paritäts-, Link-, Whitespace- und
Literal-Prüfungen bestanden sind. Der Post-Merge-geschützte Lifecycle bleibt
bewusst ausstehend und ist keine lokale Evidenz.

## Finaler Diff- und Review-Status

Der vollständige Repin-Diff ist auf die oben aufgeführten neun Parent-Pfade
begrenzt. Er ändert keinen Framework-, MRTS- oder Gitlink-Inhalt.
