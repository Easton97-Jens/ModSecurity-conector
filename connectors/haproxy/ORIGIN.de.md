# Ursprung des HAProxy-Connectors

**Sprache:** [English](ORIGIN.md) | Deutsch

Status: live-yaml-spoa-runtime (partial)
Runtime status: live request-side YAML execution through HAProxy, SPOA/SPOP,
and libmodsecurity.

In dieses Repository wurde keine Upstream-Quellbasis eines HAProxy-Connectors
importiert. Unter `connectors/haproxy` werden weder ein HAProxy-Quellbaum,
HAProxy-Header noch eine SPOE/SPOA-Protokollbibliothek vendort. Der
repository-verfasste libmodsecurity-Binding-Quellcode wird von der lokalen
SPOP-Runtime für die Ausführung von Framework-YAML auf der Request-Seite
verwendet; er ist kein produktiver HAProxy-Runtime-Adapter.

## Nativer HTX-Transport-Smoke für das Full-Lifecycle-Profil

Das Repository vendort keinen HAProxy-Quellcode. `htx-overlay/` kopiert
stattdessen einen repository-verfassten Filter, Binding-Quellen und einen
schmalen Makefile-Patch in einen isolierten, versionsgeprüften HAProxy-3.2.21-
Worktree. Das separate Profil `full-lifecycle-haproxy-htx` wählt diesen
connector-lokalen Smoke. Es validiert `filter modsecurity-htx`, lädt
kanonische No-CRS-Regeln und durchläuft P1–P4 durch echten HAProxy. Native
P1/P3-Deny-Entscheidungen werden in für Clients sichtbare Antworten umgesetzt
(403 und die kanonische P1-429-Alternative); P2/P4 bleiben nur beobachtend.
Es implementiert weder Redirect noch Post-Commit-Abort, verändert nicht die
SPOP-Kompatibilitäts-Claims und stuft keine Lifecycle-Fähigkeit hoch.

Das ausgewählte Profil zeichnet eine native Precommit-Route auf echtem Host
auf, keine alternative SPOP-Deployment. Der Standard-SPOP-Kompatibilitätspfad
bleibt getrennt; kein HTX-Host-Record darf als SPOP-Enforcement, als
Safe-/Strict-Late-Action oder als Full-Response-Body-Evidenz wiederverwendet
werden.

## Aktuelle Quellen-Provenienz

| Pfad | Ursprung | Lizenzstatus | Hinweise |
| --- | --- | --- | --- |
| `connectors/haproxy/metadata.c` | repository-verfasste Starter-Metadaten | not selected | Implementiert weder HAProxy-API, SPOE/SPOA-Protokoll noch libmodsecurity-Aufrufe. |
| `connectors/haproxy/metadata.h` | repository-verfasste Starter-Metadaten | not selected | Deklariert nur Metadaten-Accessors. |
| `connectors/haproxy/Makefile` | repository-verfasste Starter-Build-Datei | not selected | Kompiliert nur Metadaten und lokale Starter-Binärdateien. |
| `connectors/haproxy/src/haproxy_spoa_agent_starter.c` | repository-verfasster SPOA-Agent-Starter | not selected | Nur lokale synthetische Request-Decision-Logik; kein SPOP-Parser und keine HAProxy-Runtime. |
| `connectors/haproxy/src/haproxy_spoa_agent_starter.h` | repository-verfasster SPOA-Agent-Starter | not selected | Nur lokale Starter-Deklarationen. |
| `connectors/haproxy/src/haproxy_spoa_main.c` | repository-verfasste SPOA-Agent-Starter-CLI | not selected | Unterstützt nur `--describe` und `--self-test`. |
| `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` | repository-verfasste SPOP-Runtime | not selected | Parst live HAProxy-Request-seitige SPOE-Argumente, führt sie libmodsecurity zu und gibt set-var-ACKs für disruptive 403-Entscheidungen zurück; keine vollständige SPOA-Agent-Implementierung. |
| `connectors/haproxy/src/haproxy_modsecurity_binding.c` | repository-verfasstes ModSecurity-Binding | not selected | Verwendet lokal verifizierte libmodsecurity-C-API-Signaturen für materialisierte Regeln, URI, Header, Request-Body-Bytes und CRS-SQLi-Entscheidungen. |
| `connectors/haproxy/src/haproxy_modsecurity_binding.h` | repository-verfasstes ModSecurity-Binding | not selected | Deklariert die vom Binding-Self-Test und der SPOP-Runtime verwendete Request-/Auswertungsform. |
| `connectors/haproxy/src/haproxy_modsecurity_binding_self_test.c` | repository-verfasste ModSecurity-Binding-Self-Test-CLI | not selected | Unterstützt nur `--describe` und `--self-test`; Live-HAProxy-Runtime-Enforcement wird durch das Framework-Smoke-Harness behandelt. |
| `connectors/haproxy/htx-overlay/` | repository-verfasster HAProxy-3.2.21-Overlay-Quellcode und Build-Patch | selected only by the non-promoted full-lifecycle profile | Wird in einen verifizierten, disponiblen HAProxy-Source-Worktree kopiert; native P1/P3-Deny-Antworten werden mit echtem Host-Traffic ausgeübt, während P2/P4 nur beobachtend bleiben. |
| `connectors/haproxy/harness/run_haproxy_htx_runtime.sh` | repository-verfasster nativer HTX-Transport-Smoke | selected only by the non-promoted full-lifecycle profile | Baut/startet einen gepatchten HAProxy, lädt kanonische No-CRS-Regeln und zeichnet echte P1/P3-Statusantworten sowie payload-freie P2/P4-Beobachtungen ohne Capability-Promotion auf. |
| `docs/connectors/haproxy.md` | repository-verfasste kanonische Dokumentation | not selected | Dokumentiert die ausgewählte Route, die historische Kompatibilitätsgrenze und Blocker. |
| `connectors/haproxy/harness/README.md` | repository-verfasste Dokumentation | not selected | Nur Harness-Vertrag. |

## Upstream-Auswahl

- HAProxy-Upstream-Quelle: not selected.
- HAProxy-Integrations-API-/Header-Set: not selected.
- SPOE/SPOA-Protokollabhängigkeit: not selected.
- SPOP-Frame-Implementierung: request-side runtime subset only.
- ModSecurity/libmodsecurity-Binding für HAProxy: Live-Enforcement für
  gemeinsame request-side YAML-Fälle in No-CRS- und With-CRS-Runs verifiziert.
- Importierte produktive Quelldateien: none.

## Evidenzgrenze

Der aktuelle Starter/die Runtime beweist, dass Metadaten und lokale
Binärdateien kompiliert werden können, dass der SPOA-Starter einen lokalen
synthetischen Request-Decision-Self-Test ausführen kann und dass
`make smoke-haproxy` gemeinsame request-side YAML-Fälle durch Live-HAProxy,
die SPOP-Runtime und libmodsecurity ausführen kann. Die aktuelle Evidenz deckt
`REQUEST_URI`, `REQUEST_HEADERS`, `REQUEST_HEADERS_NAMES`, `ARGS`,
`ARGS_NAMES`, `REQUEST_COOKIES`, `REQUEST_COOKIES_NAMES`, `REQUEST_BODY`,
`FILES`, `XML` und den CRS-SQLi-Anomaliefall ab. Sie beweist keinen
produktiven HAProxy-Adapter-Build, keine Vollständigkeit des SPOE/SPOA-
Protokolls, kein kanonisches Response-Phase-Enforcement des ausgewählten
Pfads, keine Audit-Log-Assertions, kein disruptives Status-Mapping außer 403,
keine Redirects und kein Blocking von `RESPONSE_BODY`.
