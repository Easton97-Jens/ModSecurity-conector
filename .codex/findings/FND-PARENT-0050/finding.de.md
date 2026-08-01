# FND-PARENT-0050 — Die generische Git-Akquisition von Parent-ModSecurity-v3 ist lokal durch die Framework-Provisionierungs-Bridge behoben; gehostete Evidence steht aus

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-PARENT-0050 |
| Kategorie | security_hardening |
| Repository / Ownership | parent / parent |
| Priorität / Schweregrad / Konfidenz | P1 / medium / validated |
| Status / Machbarkeit | fixed / feasible_now |
| Release-Blocker / sicherheitsrelevant | true / true |
| Historisch validierte Parent-Revision | 2404f66d3919bda6f2e5a721f5e070f1cb61cb68 |
| Aktuell geprüfter Parent-Candidate | c53ea5de38bc884fdd7f8b686005f6c22ee0a628 |
| Read-only verwendete Framework-Revision | 77d73decd094a8f289fbe0ef2582f12430923e24 |
| Parent-Auswirkung | Der direkte Generic-Acquisition-Defekt ist lokal behoben; #55 bleibt bis frische Exact-Head-Runtime-Evidence und das FND-CROSS-0001-Gate bestehen ein Release-Blocker. |
| MRTS-Auswirkung | keine; originales MRTS bleibt read-only |

## Historische Beobachtung und aktuelle Disposition

Der aufbewahrte historische Source-to-Sink-Trace validierte eine Control-Order- und Evidence-Integrity-Lücke. An der historischen Parent-Revision 2404f66d konnte die Route ein generisches GitHub-HTTPS-ModSecurity-v3-Checkout materialisieren und den Shared-Build aufrufen, bevor die Framework-Admission für unveränderliche OWASP-Origin, freigegebenen Commit und überprüfte rekursive Topologie lief. Der absichtlich gestoppte Teil-Build ist von FND-CROSS-0001-Runtime-Evidence ausgeschlossen.

Der aktuelle Parent-Candidate c53ea5d entfernt diesen generischen V3-Acquisition-Pfad. Nachdem der Framework-Configuration-Guard besteht, reserviert Parent ein entry-marker-eigenes, aber fehlendes Staging-Child und ruft die öffentliche Framework-API ci_provision_approved_modsecurity_v3_checkout an der bereits durch den Parent-Gitlink festgehaltenen Revision auf. Parent verifiziert das Checkout danach erneut, liest Metadaten über verifiziertes /usr/bin/git mit minimaler bereinigter Umgebung, schreibt einen vollständigen Managed-Cache-Marker und publiziert erst nach allen Controls atomar. Der vorhandene build-time-Framework-Checkout-Guard bleibt Defense in Depth.

Die neue Route enthält keinen ModSecurity-v3-Aufruf von prepare_git_component. Abgelehnte Configuration-, Bridge- oder Post-Provision-Verifikationspfade liefern blockierte Records und können weder auf generisches Git zurückfallen noch unverifiziertes Staging publizieren. Der direkte statische/Control-Order-Defekt ist damit behoben und lokal regression-getestet. Dieses Finding bleibt offen, weil lokale Controls keinen frischen Exact-Head-gehosteten Strict/Full-Producer, kein terminales Evidence-Gate, Review, SonarQube oder geschützte Integration ersetzen.

## Scope und Grenze

Betroffener Parent-Inhalt ist begrenzt auf:

- ci/provisioning/components/prepare-runtime-components.py;
- tests/test_prepare_runtime_components.py; und
- das vorhandene englisch/deutsche Change-Record-Paar für PR #55.

Framework-Source, Framework-/MRTS-Gitlinks, MRTS-Source, Branches, Commits und Pull Requests bleiben unverändert. Framework-Revision 77d73de wird read-only verwendet; sie stellt die überprüfte öffentliche Provisionierungs-API bereits bereit. Keine aktuelle Task-Aktion erfordert eine Framework- oder MRTS-Delivery.

## Root Cause und Remediation

Die historische Parent-Route behandelte ModSecurity v3 als generische Git-Komponente und verschob unveränderliche Checkout-Admission bis nach Akquisition und Shared-Build-Pfad. Die korrigierte Parent-Route delegiert die Erzeugung einer frischen Source an die unveränderliche öffentliche Framework-API, die freigegebene Origin, vollständigen Commit, rekursive Topologie, Fresh-Root- und Host-Git-Controls besitzt. Parent besitzt nur sichere Staging-Reservierung, Re-Verifikation, Cache-Admission und Publication nach Framework-Freigabe.

Der exakte Candidate verhindert außerdem, dass umgebungsabhängige Git-/Loader-Konfiguration Parent-Metadatenreads beeinflusst: Er verwendet verifiziertes /usr/bin/git, einen festen PATH, deaktivierte globale/System-Konfiguration, deaktivierte Hooks/Fsmonitor und eine minimale Umgebung.

## Akzeptanzkriterien

1. Abgelehnte V3-Configuration kann weder Framework-Bridge, generisches Git noch Build-Sink aufrufen. **Lokal bestanden.**
2. Eine freigegebene V3-Source wird nur über die öffentliche Framework-Fresh-Destination-Bridge akquiriert; Parent ruft für V3 kein prepare_git_component auf. **Lokal bestanden.**
3. Ein Bridge- oder Post-Provision-Verifikationsfehler bewahrt einen publizierten Cache, entfernt nur den Managed-Staging-Eintrag und kann weder Completion-Metadaten schreiben noch abgelehntes Checkout publizieren. **Lokal bestanden.**
4. Die exakte Framework-Provenance-/Fresh-Root-Regressionssuite besteht an der durch Parent festgehaltenen Framework-Revision. **Lokal bestanden.**
5. Frische Exact-Head-#55-Evidence nutzt den legitimen Strict/Full-Producer, erreicht das Terminal-Gate und erfüllt FND-CROSS-0001 sowie PR-Review-, SonarQube- und Branch-Protection-Anforderungen. **Ausstehend.**

## Validierungsplan

- Die historische Evidence und das aktuelle lokale Bridge-Validation-Artefakt aufbewahren; gestoppte historische Ausgabe nicht als Runtime-Evidence umdeuten.
- Die separate #74-Apache-Producer-Remediation nutzen, um die legitime Full-Producer-Grundlage zu erhalten, ohne das strikte Terminal-Gate zu schwächen.
- #55 anschließend gegen das resultierende master abgleichen und frische Exact-Head-Checks, FND-CROSS-0001-Evidence, SonarQube, Reviews, Threads und Mergeability vor geschützter Integration prüfen.

## Evidenz

Historische aufbewahrte Source-to-Sink-Evidence:

- Candidate-Revision: 2404f66d3919bda6f2e5a721f5e070f1cb61cb68
- Artefakt: /var/tmp/codex/ModSecurity-conector/runs/20260723T162517Z-fnd-cross-0001-runtime-evidence-bcda7d1d/evidence/parent-modsecurity-v3-provenance-gap.md
- SHA-256: b18f34ca2f6a056e9fb4055d6f52bf22f64560645a97dece53f437da10d66fe
- Der isolierte Teil-Build stoppte mit Exit 130 unmittelbar nach Bestätigung der Reihenfolge und ist von Runtime-Evidence ausgeschlossen.

Aktuelle aufbewahrte lokale Remediation-Evidence:

- Candidate-Revision: c53ea5de38bc884fdd7f8b686005f6c22ee0a628
- Artefakt: .codex/runs/20260726T081500Z-pr55-framework-v3-bridge/evidence/local-bridge-validation.md
- SHA-256: ba0954d5d9c3e7c6bc31d558f55b9acc99b44ee93984c817aed1fba35d381f15
- Parent-Source-/Cache-Controls: 44 Tests bestanden; Framework-V3-Provenance-/Fresh-Root-Controls: 18 Tests bestanden; CI-Security-Contract, Bilingual-Documentation und Whitespace-Checks bestanden.
- Dies ist nur lokale Validation, keine gehostete Runtime-, Delivery- oder Master-Evidence.

## Abhängigkeiten und Restrisiko

Die öffentliche Framework-Bridge bei 77d73de ist über den festgehaltenen Parent-Gitlink bereits verfügbar; weder Framework-Source-Delivery noch Parent-Gitlink-Änderung sind Restabhängigkeiten. Die verbleibenden Delivery-Abhängigkeiten sind die separate #74-Apache-Runtime-Producer-Remediation, FND-CROSS-0001-legitime Runtime-Evidence und die Exact-Head-PR-Controls von #55.

Kein Risiko ist akzeptiert. Parent PR #55 darf weder auf dem historischen gestoppten Run noch nur auf lokalen Controls integriert werden. Bis frische Exact-Head-Evidence besteht, bleibt das Finding ein Release-Blocker, obwohl der direkte Generic-Acquisition-Pfad entfernt ist.

## Historie

- 2026-07-23T16:25:17Z — Aufbewahrte isolierte Source-to-Sink-Evidence validierte die historische Parent-V3-Control-Order-Lücke; der Teil-Build stoppte und wurde aus FND-CROSS-0001-Runtime-Evidence ausgeschlossen.
- 2026-07-23T17:41:30Z — Statisches Review des Candidates 59321ca stellte fest, dass sein Framework-Configuration-Guard V3-Acquisition weiter an generisches nacktes Git vor dem späteren Checkout-Guard delegierte.
- 2026-07-26T08:15:00Z — Normaler Parent-PR-#55-Commit c53ea5d ersetzte den generischen V3-Pfad durch die aktuelle öffentliche Framework-Bridge. Parent-44-Test- und Framework-18-Test-Controls bestanden; frische gehostete Evidence steht aus.
