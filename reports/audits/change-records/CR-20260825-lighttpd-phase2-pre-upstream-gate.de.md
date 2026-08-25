# Change Record CR-20260825: Lighttpd-Phase-2-Pre-Upstream-Gate

**Sprache:** [English](CR-20260825-lighttpd-phase2-pre-upstream-gate.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260825-lighttpd-phase2-pre-upstream-gate` |
| Datum (UTC) | `2026-08-25` |
| Basis-Revision | `5d71be74369123257851eb5ec612d7523a6b061d` |
| Scope | Nur Parent-Repository: der ausgewählte gepatchte Lighttpd-HTTP/1.1-`mod_proxy`-Phase-2-Request-Body-Zulassungspfad, fokussierter Harness/Contracts, EN/DE-Dokumentation und gekoppelte Nachvollziehbarkeit. Keine Framework-, MRTS-, Gitlink-, Workflow-, Dependency-, Quality-Control-, P3- oder P4-Änderung. |

## Motivation und Problemstellung

Vor dieser Änderung konnten aktive Request-Stream-Flags `mod_proxy` zum
Verbinden oder Weiterleiten veranlassen, während die Common Runtime noch die
Phase-2-Inspektion bei terminalem EOS benötigte. Das verletzt die Pre-Upstream-
Zulassungsgrenze. Die exakte ablehnende libmodsecurity-Request-Body-Limit-
Intervention musste außerdem als HTTP 413 statt als generische 403-Signatur am
Host sichtbar sein.

Wenn ein Streaming-Request bis EOS zurückgehalten wird, darf der Host nach
einer nur abgeschnittenen Common-Runtime-Inspektion keinen unbegrenzten Body
weiter annehmen. `body_limit_action=process_partial` hat dieses Verhalten und
ist deshalb für dieses zurückhaltende Profil unsicher. PR #339 ist in die
aktuelle `master`-Basis gemergt; sein Stock-ABI-Layout wird geerbt und ist
keine offene Dependency. Der Benutzer autorisierte einen Task-Branch, einen
atomaren Commit, Push und einen Draft PR, aber keinen Merge.

## Akzeptanzkriterien

- Vor EOS erzeugen eine Phase-2-Ablehnung, Body-Limit-Ablehnung, ein Timeout
  eines unvollständigen Bodys oder ein nicht unterstützter Modus keine
  Upstream-Verbindung und keine Byte-Lieferung.
- Nach EOS erzeugt ein erlaubter Request genau eine vollständige
  Upstream-Lieferung des Bodys.
- Bereits aktive/reaktivierte Stream-Flags, `Incremental` und body-tragendes
  `Upgrade` schlagen im ausgewählten Profil mit HTTP 501 fail closed fehl.
- Streaming akzeptiert nur `body_limit_action=reject`; `process_partial`
  schlägt beim Laden der Konfiguration vor Listener oder Upstream fehl.
- Die exakte ablehnende `SecRequestBodyLimitAction`-Phase-2-Signatur wird auf
  HTTP 413 abgebildet; andere Interventionsstatus bleiben unverändert.
- C17-Build-/Contract-/Runtime-Nachweise und wahrheitsgemäße EN/DE-
  Dokumentation bestehen; keine `.github/`-Datei ändert sich.

## Implementierungsentscheidung und Begründung

- `mod_msconnector_prepare_request_body()` löscht aktive Request-Stream-Flags
  vor Body-Reads und wartet, bis terminales EOS die Phase-2-Entscheidung
  erzeugt hat. Bereits aktives Streaming, `Incremental` und `Upgrade` werden
  abgelehnt.
- Der Request-Body-Hook wiederholt die Aktivflag-Prüfung; auch eine spätere
  Aktivierung bleibt damit fail closed. Eine pro Request gesetzte Gate-
  Ablehnungsmarke vermeidet normale Transaction-Vervollständigung nur für
  diesen abgelehnten Request.
- `msconnector_runtime_body_limit_action()` stellt die geparste Common-
  Runtime-Aktion bereit. Im gepatchten ABI-Zweig lehnt das Setup Streaming ab,
  wenn die Aktion nicht `MSCONNECTOR_BODY_LIMIT_ACTION_REJECT` ist; Stock- und
  Nicht-Streaming-Verhalten bleiben unverändert.
- `native_intervention_status()` bildet nur die exakte No-Redirect-
  Request-Body-Limit-Signatur auf 413 ab und erhält alle nicht verwandten Regeln
  und Statuswerte.
- Die Grenze für den zurückgehaltenen Body ergibt sich aus dem positiven
  Common-`request_body_limit` (standardmäßig 1 MiB) und dem ablehnenden
  Lesezyklus. Das Modul konfiguriert `server.max-request-size` nicht; dieser
  Wert bleibt eine unabhängige Host-seitige Defense-in-Depth-Einstellung.

## Geänderte Dateien

- `common/runtime/msconnector_runtime.c`
- `common/runtime/msconnector_runtime.h`
- `connectors/lighttpd/module/mod_msconnector.c`
- `connectors/lighttpd/harness/run_phase2_pre_upstream_gate.py`
- `connectors/lighttpd/tests/test_patched_host_contract.py`
- `tests/test_lighttpd_phase2_pre_upstream_gate_contract.py`
- `tests/test_modsecurity_request_body_limit_status_contract.py`
- `connectors/lighttpd/README.md` und `connectors/lighttpd/README.de.md`
- `connectors/lighttpd/harness/README.md` und `connectors/lighttpd/harness/README.de.md`
- `docs/connectors/README.md` und `docs/connectors/README.de.md`
- `docs/connectors/lighttpd.md` und `docs/connectors/lighttpd.de.md`
- dieses Change-Record-Paar und die gepaarten Change-Record-Archivindizes

## Ausgeführte Befehle

| Check | Tatsächliches Ergebnis |
| --- | --- |
| Frischer Patched-Host-GCC/C17-Build und `check-lighttpd-patched-host` | Bestanden mit dem gepinnten Lighttpd-1.4.85-Patch SHA-256 `e00d3892ab0ad7fb409e1ef593e2c3bda71ea44ee2002c4db325712d46bfa8b5`. |
| Stock GCC und Clang; Patched-Clang-Modulbuilds | Unter `-std=c17 -Wall -Wextra -Werror` bestanden. |
| `make -C connectors/lighttpd check-lighttpd-core-patch` | Bestanden. |
| `make check-common-helpers-c17` | Bestanden. |
| `make check-connector-config-reference` | Bestanden. |
| Ausgewählte Shell-Syntax und Python-Kompilierung | Bestanden. |
| Fokussierter Phase-2-/Status-/ABI-Befehl | Bestanden: 10 Tests. |
| Master-basierte Lighttpd-Host-Contracts | Bestanden: 70 Tests, 12 erwartete Namespace-Skips. |
| `make check-bilingual-docs` und `make check-doc-links` | Environment-blocked: Der Rerun meldete nur repositoryweite fehlende Ziele unter dem nicht initialisierten Gitlink `modules/ModSecurity-test-Framework` und keine Task-Dokumentdiagnose. |

## Runtime-Evidence

Private Receipts enthalten begrenzte Metadaten und keine öffentliche lokale
Evidence-URL.

| Receipt | SHA-256 | Beobachtetes Ergebnis |
| --- | --- | --- |
| `master-5d71-bufferbound-gate-summary` | `17ad572e3aa4699a2af051346ba7f782db418973a22b22331dedae1bf85dd2a3` | Verzögerter Marker: 403 und null Preterminal-Upstream-Reach; verzögertes Allow: 200 und genau eine vollständige Post-EOS-Lieferung; unmittelbarer Marker: 403; `Incremental`, konfigurierter Stream und aktiviertes body-tragendes `Upgrade`: 501 ohne neue Upstream-Verbindung; Streaming plus `process_partial`: Konfigurationsablehnung vor Listener/Upstream. |
| `master-5d71-bufferbound-p0-p2-summary` | `eb72d9ce51260da3e76b8d79b0ca7eb2d2c6215efd57c40b41c4d9f192337f81` | P1/P2-Allow/Deny, leerer Body, sichtbares 413 bei 33/64 Byte, RST-Controls, Folgeanfrage und Cleanup bestanden; Deny-/Limit-/Reset-Fälle erreichten keinen Upstream. |
| `master-5d71-bufferbound-timeout-summary` | `5d72aea037b9d08e682c31c16e75477cd55a4b181d6da613254c7b1bad136888` | Ein partieller Content-Length-Body lief vor EOS aus, ohne Event/Upstream; der Listener blieb gesund und ein folgender erlaubter 32-Byte-Request wurde genau einmal geliefert. |

Der historische Rules-Pfad des aufbewahrten P0/P2-Helfers fehlte, daher
endete sein erster Start vor Prozess oder Listener. Ein task-eigener Wrapper
lieferte nur dieselbe verifizierte schreibgeschützte Rules-Eingabe und der
frische Retry bestand. Weder Produkt-Source noch der historische Helfer wurden
verändert.

## Security-Auswirkung

Die betroffene Vertrauensgrenze ist nicht vertrauenswürdige HTTP/1.1-Request-
Body-Eingabe vor dem Proxy-Upstream. Das Control ist für nicht unterstütztes/
reaktiviertes Streaming und `process_partial` fail closed. Ein fokussierter
Source-to-Sink-Security-Review fand keinen plausiblen Pre-Upstream-Bypass oder
C/API-Fehler und kein High-/Critical-Finding. `FND-PARENT-0316` ist auf diesem
Task-Branch `fixed_pending_merge` und nicht auf `master` geschlossen.

## Bekannte Einschränkungen

Dies ist nur das ausgewählte gepatchte HTTP/1.1-`mod_proxy`-Phase-2-Gate. Es
beansprucht weder HTTP/2, HTTP/3, P3/P4, CRS, allgemeines Request-Streaming,
einen vollständigen P1-P4-Rollout, Production-Readiness noch eine unabhängig
konfigurierte Host-Grenze `server.max-request-size`. Die 12 Namespace-Skips
benötigen nicht privilegierte User-, Mount- und PID-Namespace-Unterstützung.

## Verbleibende Risiken

- Eine künftige Lighttpd- oder libmodsecurity-Verhaltensänderung benötigt eine
  erneute Runtime-Validierung der Stream-Flags und der absichtlich engen
  413-Abbildung.
- Exact-Head-Hosted-Checks und Review können nicht aus lokaler Evidence
  abgeleitet werden.

## Nicht ausgeführte Prüfungen mit Begründung

- Keine HTTP/2-, HTTP/3-, P3/P4-, CRS- oder Full-P1-P4-Runtime-Matrix lief,
  weil sie außerhalb des ausgewählten HTTP/1.1-Phase-2-Scopes liegt.
- Hosted-PR-, SonarCloud-, Governance- und Resulting-`master`-Checks benötigen
  einen Draft PR auf seinem exakten Head und werden davor nicht behauptet.
- Dokumentationschecks sind allein wegen repositoryweiter fehlender Ziele
  unter dem nicht initialisierten Framework-Gitlink environment-blocked; es
  wurde keine Task-Dokumentdiagnose gemeldet.

## Finaler Diff- und Review-Status

Der finale lokale Scope ist für einen atomaren Commit, normalen Push und einen
Draft PR gegen `master` vorbereitet. Dieser Record behauptet absichtlich weder
Push, PR, Hosted-Checks, direkten `master`-Push noch Merge; Delivery-Fakten
werden erst nach ihrer Beobachtung dokumentiert.
