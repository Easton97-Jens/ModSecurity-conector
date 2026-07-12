# HAProxy-SPOE/SPOP-Kompatibilitätsbeispiel

**Sprache:** [English](README.md) | Deutsch

Dieses Verzeichnis bewahrt die früheren HAProxy-SPOE/SPOP-Beispiele. Es ist von
der nativen HTX-P1--P4-Safe-Referenz unter [../safe/](../safe/) getrennt.

| Datei | Geltungsbereich |
| --- | --- |
| haproxy-request-only.cfg | Request-SPOE-Gruppe für P1/P2-artige Request-Entscheidungen. |
| haproxy-response-headers.cfg | Ergänzt Response-Header-SPOE; keine Response-Body-Verarbeitung. |
| spoe-modsecurity.conf | Mapping für SPOE-Agent, Gruppen, Nachrichten und Rückgabevariablen. |
| modsecurity-agent.conf | Einstellungen des SPOA-Prozesses. |
| legacy-phase4-strict-abort.cfg | Deaktiviertes historisches Beispiel; nie als P4-Evidence verwenden. |

## Anzupassende Werte

| Name | Zweck und Format | Pflicht/Default, Setzer, Geltungsbereich | Beispiel und Grenze |
| --- | --- | --- | --- |
| filter spoe engine modsecurity config | HAProxy-SPOE-Filter und lesbare Agent-Datei | Pflicht; Host-Konfiguration; Frontend-Scope | /etc/haproxy/spoe-modsecurity.conf. Wählt Kompatibilitäts-SPOE, nicht natives HTX. |
| send-spoe-group | Request- oder Response-Header-SPOE-Nachrichtengruppe | Für passende Datei Pflicht; Host-Konfiguration; Request-/Response-Scope | request-check oder response-check. response-check sendet keinen Response-Body. |
| be_spoa_modsecurity | SPOP-Backendname und Endpunkt | Pflicht; Host-Konfiguration; Backend-Scope | 127.0.0.1:12345. Muss zum listen-Wert des Agenten passen. |
| groups und register-var-names | SPOE-Gruppennamen und Rückgabe-Transaction-Variablen | Pflicht; spoe-modsecurity.conf; Agent-Scope | request-check response-check und blocked/action/status-Felder. Namen müssen zu HAProxy-Enforcement-Ausdrücken passen. |
| max-frame-size | Positives SPOE-Frame-Byte-Limit | Pflicht; spoe-modsecurity.conf; Agent-Scope | 65532. Begrenzt einen Frame, schafft keine P4-Body-Unterstützung. |
| rules-file | Lesbare Agent-Regeldatei | Pflicht; modsecurity-agent.conf; SPOA-Scope | /etc/modsecurity/haproxy-rules.conf. Ein geprüftes Ruleset kann Traffic blockieren. |
| decision-log, audit-log, log-file | Beschreibbare Prozesslogpfade | decision-log Pflicht, andere optional; SPOA-Scope | /var/log/haproxy-modsecurity. Metadaten schützen und keine Secrets loggen. |
| response-body-limit und response-body-timeout | Kompatibilitäts-Response-Body-Controls | Explizit deaktiviert; SPOA-Scope | 0 und 0. Nicht als P4-Unterstützung darstellen. |

SPOP-Adresse 127.0.0.1:12345, HAProxy-Listener 127.0.0.1:8080, Upstream
127.0.0.1:8081 und /etc- oder /var/log-Pfade sind Hostbeispiele, keine
repository-relativen Pfade.

Dieser Pfad darf nicht verwendet werden, um natives HTX-Verhalten,
P4-Response-Body-Verarbeitung, Safe-Late-Verhalten, Strict-Abbruch, First Byte
vor EOS oder No-Full-Response-Buffer zu behaupten.
