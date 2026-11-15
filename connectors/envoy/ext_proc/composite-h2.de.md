# Composite-Response-Policy

**Sprache:** [English](composite-h2.md) | Deutsch

Der gemeinsame Service `msconnector_composite` akzeptiert
`--late-action-policy off|safe|strict` (Standard `safe`). Strict wird nur mit
einer nativen Engine zugelassen, deren eingelesene Common-Laufzeit
`phase4_mode=strict` verwendet. Auch die umgekehrte Strict/Safe-Abweichung wird
vor dem Start eines Listeners abgelehnt.

Diese Policy gilt unabhängig für die vollständigen Pfade Envoy ext_authz mit
Response-Companion und Traefik ForwardAuth mit Response-Companion. Sie ergänzt
kein Response-Verhalten für ein ungepaartes Autorisierungsprotokoll. Safe
erhält die bereits begonnene Antwort. Strict sendet Envoys späte native lokale
Antwort oder Traefiks `http.ErrAbortHandler`-Sentinel nach dem Freigeben der
gehaltenen Transaktion. Kleine geprüfte Traefik-Chunks werden vor Upstream-EOS
ausgegeben.

Der Lebenszyklusbeleg `host_action_request` beschreibt die angeforderte späte
Host-Operation. Er behauptet keinen durch Common bestätigten Downstream-Reset.
Tatsächliche H2-Frames und unabhängige Host-Zugriffe müssen Abbruch und Isolation
gleichzeitig aktiver Streams belegen. Der Koordinator protokolliert einen
begrenzten SHA256 aus Methode, NUL und URI zur unabhängigen Zuordnung von
Request und gehaltener Transaktion; Lease und Response-Inhalt werden niemals
ausgegeben.

Ein tatsächlich geschlossener Companion-Protokollpfad ohne EOS wird mit Commons
typisiertem Protokollabschluss beendet. EOS und eine Zuordnung der Ursache zu
Client oder Upstream werden nicht erfunden. Unbekannte Abschlussgründe behalten
die native Phasensequenzprüfung. Die gemeinsame CGo-Engine behält ihre
Backend-Identität `envoy`/`ext_proc`; nativer Host und Koordinator-Übergabebelege
identifizieren jedes vollständige logische Profil getrennt.
