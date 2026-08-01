# FND-PARENT-0073 — HAProxy-HTX-Metadaten-Event-Test schlug vor seiner Pfad- und TLS-Kontrolle fehl

## Klassifikation

| Feld | Wert |
| --- | --- |
| ID | FND-PARENT-0073 |
| Kategorie | test_failure |
| Repository / Ownership | parent / parent |
| Priorität | P1 |
| Severity | not_applicable |
| Confidence | confirmed |
| Status | verified |
| Machbarkeit | feasible_now |
| Release-Blocker | false |
| Candidate-Integration-Blocker | false |
| Sicherheitsrelevant | false |
| Connector / Profil | haproxy / PR-#182-exakter aktueller-Master-Hosted-Head `76644bfe832d1530704ca2ae0f2182338949ead5` |

## Zusammenfassung

Am exakten vorherigen PR-#182-Head `d79750b4869080ab04137d1c3eff7a9c751af760`
lud `HAProxyHTXSmokeHelperTest.test_event_contains_only_metadata` `root` in
Helper-Aufrufen, band ihn aber nie. Die vollständige Helper-Suite kann aktuell
wegen der bewusst nicht initialisierten Framework-Fixture die Testentdeckung
nicht erreichen, doch aufbewahrte statische AST-Evidence bestätigt den
Source-Defekt.

Der exakte aktuelle-Master-Hosted-Head weist jetzt `root = Path(temporary)` vor jedem
betroffenen Pfad und Helper-Aufruf zu und zentralisiert das doppelte HAProxy- /
Envoy-Descriptor-Safe-Artefaktprotokoll. Seine 42 fokussierten Common-/HAProxy-
/Envoy-/Runtime-Path-Kontrollen sowie die aufgezeichneten statischen, direkten
Private-Root-Metadaten-Event-, Transaction-ID-/TLS-, Shell-, HTX-Overlay-,
Common-Adoption-, Bilingual- und Whitespace-Kontrollen bestehen. Erforderliche
GitHub-Kontexte bestehen, Sonar hat Quality Gate `OK` mit null offenen Issues
und null New-Code-Duplizierung, und Review-/Thread-Readbacks sind leer. Der
Candidate-Blocker ist aufgehoben; geschützter Merge und resulting-master-
Validierung bleiben erforderlich.

## Auswirkung und Scope

Die vorgesehene pfad-/TLS-sensitive Testkontrolle stoppte vor ihren Assertions
für Metadaten, Private Root und Host-Evidence. Dies ist ein Test-Control-Fehler;
es gibt keine Evidence für einen Produktions-HTX-Pfad-, TLS- oder Metadaten-
Sicherheitsdefekt.

Betroffene Source und Symbol:

- `connectors/haproxy/harness/test_haproxy_htx_smoke_helper.py`
- `HAProxyHTXSmokeHelperTest.test_event_contains_only_metadata`

## Ursache und Remediation

Der Test erzeugte einzelne `Path(temporary)`-Werte, wies aber nicht den
gemeinsamen `root` zu, den der Helper-Confinement-Vertrag verlangt. Die
Reparatur weist `root = Path(temporary)` einmal zu und leitet Event- und
Log-Pfade davon ab.

Die vollständige Framework-gestützte Helper-Suite und die Live-HAProxy-/
libmodsecurity-Runtime bleiben in diesem Task-Clone nicht verfügbar.
Framework/MRTS dürfen nicht allein zum Umgehen dieser fehlenden Fixture
initialisiert oder geändert werden.

## Evidence und Validierung

| Stufe | Artefakt | SHA-256 | Ergebnis |
| --- | --- | --- | --- |
| Exakte Pre-Fix-Statikanalyse | `/var/tmp/codex/ModSecurity-conector/runs/merge-prs-181-182-master-20260729.nq2EeI/evidence/pr182-unbound-root-static.md` | `82ff93736e180b8d17c2499661ffd04bd4c48edbded48a18c5cda83a0c286d05` | `root` war geladen, aber nie lokal gebunden. |
| Lokale Post-Fix-Focused-Controls | `/var/tmp/codex/ModSecurity-conector/runs/merge-prs-181-182-master-20260729.nq2EeI/evidence/pr182-root-binding-postfix.md` | `b74d25130e749b4c58a5c42966f58d441bcedc9bcb0810f2952abc5dbea15668` | Bindungs-, direkte Metadaten-Event-, Transaction-ID-/TLS-, Shell-, statische, Bilingual- und Diff-Controls bestanden. |
| Committed Shared-Artefakt-Remedy | `/var/tmp/codex/ModSecurity-conector/runs/merge-prs-181-182-master-20260729.nq2EeI/evidence/pr182-shared-artifact-remediation-local.md` | `a9066f4f4420f1ac53a366bae14f563228560b14f80efcb6da64d5dba1747648` | Der Workspace-Tree, der später als `c15092f2bf05d5281f0976e87450bb79e6ea9e65` committed wurde, bestand 42 fokussierte Common-/HAProxy-/Envoy-/Runtime-Path-Kontrollen; frische gepushte-Head-Hosted-Evidence bleibt erforderlich. |
| Exakte Hosted-Readiness | `/var/tmp/codex/ModSecurity-conector/runs/merge-prs-181-182-master-20260729.nq2EeI/evidence/pr182-c798-exact-head-hosted.md` | `f02e5612bb3394387d349aec72da4025a130f6e84d71b8aae76ae32ad5271add` | Historischer exakter Head `c798334f9e6ddb5f2f4385e66779aba55be06156` war clean, mergeable, required-context-clean, Sonar-clean und hatte null Review-Threads/Reviews. |
| Exakte aktuelle-Master-Hosted-Readiness | `/var/tmp/codex/ModSecurity-conector/runs/merge-prs-181-182-master-20260729.nq2EeI/evidence/pr182-766-current-master-exact-head-hosted.md` | `e306a4e68c3c91b623f9e8851df00f37fc1a84b3cc76fc3ffa0a7e3e177bb7bc` | Aktueller Head `76644bfe832d1530704ca2ae0f2182338949ead5`, erzeugt durch normales Basis-Update, ist clean, mergeable, required-context-clean, Sonar-clean und hat null Review-Threads/Reviews. |

Die Akzeptanz verlangt einen gebundenen Source-Root, bestandene fokussierte
Kontrollen auf dem committed Kandidaten sowie frische Exact-Head-GitHub-
Actions-, SonarQube-Cloud-, Review-/Thread- und Mergeability-Evidence nach dem
Push.

## Verbleibender Zustand

Die lokale Reparatur ist `fixed`, aber der gesamte Framework-gestützte
Helper-Test und die Live-HTX-Runtime sind durch fehlende autorisierte
Voraussetzungen blockiert. Es wird kein Runtime-Sicherheitsbefund behauptet.
Der exakte aktuelle-Master-PR-Head hat frische Hosted-Evidence; geschützter Merge und
resulting-master-Validierung bleiben vor dem Schließen erforderlich.
