# FND-PARENT-0056 — Bereite NGINX-Runtime-Snapshots lassen den Parent-Common-Source-Root aus

## Identität

| Feld | Wert |
| --- | --- |
| Kategorie | `ci_failure` |
| Repository / Ownership | `parent` / `parent` |
| Priorität / Schweregrad / Konfidenz | `P1` / `not_applicable` / `confirmed` |
| Status / Machbarkeit | `fixed` / `feasible_now` |
| Release-Blocker / Sicherheitsrelevanz | ja / ja |
| Scope | Parent-#74-NGINX-Runtime-Snapshot-Veröffentlichung; Framework- und MRTS-Source bleiben unverändert |

## Beobachtung, Auswirkung und Voraussetzungen

Der exakte Parent-PR-#74-Head `a0f337b8e45e5661b1ed09c7bf39b958548fbd14`
beendete die Component-Vorbereitung und Readiness in beiden Hosted-Producern.
NGINX schlug danach bei der Konfiguration mit `ngx_http_modsecurity: missing
Common source root; set MSCONNECTOR_COMMON_SRC` fehl; das strikte terminale
Evidence-Gate wurde übersprungen und akzeptierte keine fehlgeschlagene
Evidence.

Die direkte Matrix konsumiert nach der NGINX-Cache-Vorbereitung einen
Invocation-lokalen Snapshot. Framework materialisiert den Adapter getrennt von
den Parent-Common-Source-Dateien und NGINX-configure kompiliert diese Common-C-
Quellen. Die Auslassung blockiert frische legitime Evidence und die geschützte
#74-Integration. Es wird kein produktiver Exploit behauptet; die relevante
Sicherheitsgrenze ist die Parent-kontrollierte Build-Umgebung, die weder einen
vom Job gelieferten Source-Pfad noch einen Fallback akzeptieren darf.

## Ursache, Source-to-Sink und Behebung

Die Parent-Cache-Vorbereitung übergibt beim Bauen des verwalteten NGINX-
Eintrags ein kontrolliertes Common-Source-Verzeichnis. Ihre spätere
`runtime_env`-Rekonstruktion veröffentlichte bereites Binary, Modul,
Build-Verzeichnis und Owner Root, ließ aber `MSCONNECTOR_COMMON_SRC` aus.
`with-runtime-components.sh` sourct diesen lokalen Snapshot für die direkte
Matrix. Frameworks `run_blocked ... env` erbt den Wert normal, wenn er
vorhanden ist; es löscht oder ersetzt ihn nicht.

Die Parent-only-Behebung leitet `MSCONNECTOR_COMMON_SRC` mit
`nginx_runtime_environment` ausschließlich aus dem aufgelösten
`CONNECTOR_ROOT/common/src` für einen bereiten NGINX-Record ab. Ein nicht
bereiter Record veröffentlicht keine NGINX-Runtime-Werte. Das bestehende
Cache-Owner-Containment und der fehlgeschlossene Framework-Check für fehlende
Quellen bleiben unverändert. Framework- und MRTS-Source, Heads, Gitlinks,
Branches und Delivery-Status bleiben unangetastet.

Der neuere exakte Parent-#74-Head
`c6db0f8ab5b95be67a92ba925a1f4caa3d3d0a1d` zeigt, dass die ursprüngliche
Missing-Common-Source-Bedingung nicht mehr reproduzierbar ist: Apache- und
NGINX-Vorbereitung endeten erfolgreich, und NGINX konfigurierte das Modul. Der
Producer erreichte danach den eigenständigen Framework-Case-Schema-Fehler
`FND-FRAMEWORK-0057`. Framework-PR #51 ist jetzt als `de705a5` gemergt und
Parent-PR #126 hat den Gitlink bereits übernommen, daher bleibt dieser
Parent-Befund nur bis zum erneuten vollständigen Producer und Terminal-Gate
offen.

## Evidence und Reproduktion

Aufbewahrte Evidence:
`.codex/runs/20260726T135925Z-pr74-nginx-common-source-snapshot/evidence/parent-nginx-common-source-snapshot-root-cause.md`
(SHA-256 `f9b8c36c52f41e9fda2535ffa7522033f06b9e52bfe21e61a6d1e5c25ed5f52a`).
Sie dokumentiert die exakte Diagnose und Source-to-Sink-Klassifikation ohne
Runner-Umgebung, Credentials, Payloads oder vollständige Hosted-Logs.

Zur Reproduktion diese begrenzte NGINX-configure-Diagnose des exakten Heads
inspizieren; anschließend `prepare_nginx_runtime`, `runtime_env`,
`with-runtime-components.sh` und Framework `prepare-nginx-build.sh` verfolgen.
Nicht das Terminal-Gate deaktivieren, einen Cache-Pfad ersetzen, einen
Caller-Wert weiterreichen oder Framework/MRTS verändern, um den Producer grün
zu machen.

## Akzeptanz und Validierung

1. Ein bereiter NGINX-Snapshot enthält genau den Parent-abgeleiteten Common-
   Source-Root; ein nicht bereiter Record enthält keine NGINX-Runtime-Werte.
2. Die direkte Framework-Runtime-Matrix-Grenze erhält den Wert durch den
   sourcebaren Invocation-lokalen Snapshot.
3. Ein Cache-contained Refresh bleibt akzeptiert, während ein Outside-Owner-
   Root vor `make` abgewiesen wird.
4. Fokussierte Tests bestehen; danach bestehen ein neuer exakter #74-Hosted-
   Producer und sein striktes Terminal-Gate ohne Fallback oder gelockerte
   Kontrolle.
5. Exact-Head-SonarQube Cloud, Reviews, Protection und Integrations-Evidence
   bleiben erforderlich; eine MRTS-Aktion ist weder erlaubt noch nötig.

`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest
tests.test_runtime_env_snapshot_contract
tests.test_full_matrix_cache_owner_root
tests.test_runtime_component_cache_contract` bestand alle 38 Tests. Die
ersten beiden kontrollieren Snapshot-Veröffentlichung und Framework-Runner-
Propagation; der dritte erhält den Component-Cache-Vertrag. Sie behaupten
keinen nativen NGINX-Build oder Hosted-Producer-Erfolg.

## Abhängigkeiten, Restrisiko und Historie

`FND-CROSS-0008` besitzt den separaten Cache-Deletion-Owner-Containment-
Defekt; dies ist eine eigenständige Parent-only-Snapshot-Source-Auslassung.
Der ursprüngliche Hosted-Fehler reproduziert auf Exact Head `c6db0f8` nicht
mehr; Framework-PR #51 ist gemergt und Parent-PR #126 hat seinen Gitlink
übernommen. Die verbleibende Akzeptanz-Evidence ist ein frischer Exact-Head-
Producer und ein Terminal-Gate auf dem normal aktualisierten #74-Branch. Es
wird kein Risiko akzeptiert.

- 2026-07-26 — Begrenzte Exact-Head-NGINX-Diagnose und Source-Review
  identifizieren die Parent-Snapshot-Auslassung; fokussierte Reparatur und
  lokale Kontrollen beginnen.
- 2026-07-26 — Exact Head `c6db0f8` beendet Apache-/NGINX-Vorbereitung und
  konfiguriert das NGINX-Modul, daher reproduziert die ursprüngliche Bedingung
  nicht mehr. Der nächste Fehler ist der eigenständig verfolgte Framework-
  Schema-Blocker `FND-FRAMEWORK-0057`; dieser Record kann vor Abschluss des
  vollständigen Producers und strikten Terminal-Gates nicht verifiziert
  geschlossen werden.
- 2026-07-26 — Framework-PR #51 wurde als `de705a5` gemergt und Parent-PR
  #126 hat den Gitlink übernommen. Die externe Abhängigkeit ist gelöst;
  Parent #74 benötigt jetzt nur sein normales Base-Update und frische
  Exact-Head-Producer-, strikte-Gate-, Sonar-, Review-, Protection- und
  Integrationsevidenz.
