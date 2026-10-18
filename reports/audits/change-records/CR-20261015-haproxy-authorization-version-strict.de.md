# Change Record: CR-20261015-haproxy-authorization-version-strict

**Sprache:** [English](CR-20261015-haproxy-authorization-version-strict.md) | Deutsch

Produktkorrektur im bestehenden PR #382; Integration und Hostabnahme in #410/#415.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261015-haproxy-authorization-version-strict |
| Datum (UTC) | 2026-10-15 |
| Basis-Revision | `9980eb049dde0643da6a4f04e3b6712801b670b3` |

## Motivation und Problemstellung

Begrenztes SPOP-P1/P2-Allow scheiterte fälschlich am allgemeinen Abschluss des vollständigen Lifecycle. Die native URI-Verarbeitung kodierte HTTP/1.1 fest. Strict behielt nach Auswahl der Abschaltung wartende Response-Kanalbytes bei.

## Akzeptanzkriterien

Deklarierte P1/P2 ohne synthetische P3/P4 abschließen; zugelassene HTTP-Versionen weiterreichen; abgelehnte wartende Responsebytes entfernen und die Filterfortschaltung stoppen. Frische integrierte Hostverifikation bleibt in #415 erforderlich.

## Implementierungsentscheidung und Begründung

Eine eigene Common-Abschlussoperation für Requestautorisierung bei vorab deklarierter direkter Maske 3 ohne Companion ergänzen; der allgemeine Abschluss bleibt bei Maske 15. Das tatsächliche Request-http_version verlangen. Strict entfernt wartende HTX-/Kanalausgabe, bricht nur den betroffenen Stream ab und liefert ein negatives Filterergebnis.

## Geänderte Dateien

Common-Transaktionsvertrag/-zustand; HAProxy-Binding, Mapper, SPOP-Runtime und HTX-Filter; gezielte Request-/Versions-/Limit-/Aufrufer-/Fehlertests; gepaarte Common- und HAProxy-Anleitungen. Keine Änderung an Framework-/MRTS-Quellen oder Gitlinks.

## Ausgeführte Befehle

Die Hauptaufgabe führte RTK-umhülltes CPython3.14.7-pytest für test_haproxy_transaction_contract_binding, test_haproxy_spop_request_target, test_haproxy_native_http_version, test_haproxy_request_authorization_contract, test_haproxy_i10_host_callers, test_haproxy_i10_binding_callers und test_haproxy_spop_event_sink_failures aus: 69passed,43subtests passed,exit0. Exakte argv/cwd/Ausgabehashes liegen im externen Lauf i12-haproxy-415-acceptance-20261015/commands/product-targeted-pytest-v2.json. Ein früherer nicht vorhandener Testdateiname führte vor der Sammlung zu exit4; sein Receipt bleibt erhalten.

## Security-Auswirkung

Admission bleibt fail-closed. Sampleeingaben können den Umfang nicht erweitern. Unbekannte/fehlende/widersprüchliche Versionen scheitern vor nativer Allokation. Das Layout der Common-Struktur bleibt unverändert; alle internen Verbraucher der HAProxy-Requeststruktur müssen neu gebaut werden. Keine Sicherheitsausnahme, Gateänderung oder Payloadprotokollierung.

## Runtime-Evidence

Tests mit echtem SDK prüfen Versionen 1.0/1.1/2.0, Allow/Deny, terminale Fehler und einmalige Freigabe. Strict-Komponententests prüfen direkte/Companion-Callbacks, wartende 0/33/65537 Bytes, bereits ausgelieferte Bytes sowie Safe- und Nachbarkontrollen. Separate Sanitizer- und Mutationsreceipts bleiben erhalten. Die tatsächliche HAProxy3.2.25-Filter-Übersetzungseinheit kompiliert. Diese Beobachtungen stellen kein frisches Host-Lifecycle-PASS dar.

## Bekannte Einschränkungen

Tatsächliche H1-Mux-Ausgabe ist von HTX-/Kanalpufferung getrennt. Dieser Patch liefert keinen nativen Common-Event-Sink und belegt nicht jede HTTP/2-Framingabbildung.

## Verbleibende Risiken

Bereits ausgelieferte Bytes lassen sich nicht zurücknehmen. Frische begrenzte, leere, große, Streaming-, Cancel- und parallele Hostfälle müssen tatsächliche Commit-/Entscheidungs-/Clientreihenfolge messen. Historische Evidence bleibt unverändert.

## Nicht ausgeführte Prüfungen mit Begründung

Frische integrierte private Hostläufe und CI/Sonar am finalen Head folgen normaler Integration und Neubau über #382→#410→#415. Der historische Gitleaks-Releaseblocker von #382 bleibt unabhängig ohne Ausnahme bestehen.

## Finaler Diff- und Review-Status

Unabhängige Reviews fanden kein wesentliches Problem im Request-/Versions- oder Strict-Patch. Gezielte pytest-, Sanitizer-, Mutations-, SDK- und Kompilierungsreceipts bleiben erhalten. Die vollständige I12-Abnahme erfordert weiterhin frische Hostqualifikation und Gates am aktuellen Head.
