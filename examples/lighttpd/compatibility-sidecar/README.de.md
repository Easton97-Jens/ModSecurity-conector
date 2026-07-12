# lighttpd-Sidecar-Kompatibilitätsbeispiel

**Sprache:** [English](README.md) | Deutsch

Die bewahrte Datei ist ein illustrativer lighttpd-Proxyaufbau. Sie lädt kein
mod_msconnector.so und ist daher keine native lighttpd-Kernreferenz. Für die
Stock-Form des nativen Moduls [../minimal/](../minimal/) verwenden, für die
gepatchte HTTP/1.1-Identity-Entity-Referenz [../safe/](../safe/).

| Name | Zweck und Format | Pflicht/Default, Setzer, Geltungsbereich | Beispiel und Grenze |
| --- | --- | --- | --- |
| server.modules | Installierte lighttpd-Proxy- und Logging-Module | Pflicht; Host-Konfiguration; Server-Scope | mod_accesslog und mod_proxy. Dies ist nicht mod_msconnector. |
| server.document-root und Logpfade | Host-Dateisystempfade | Pflicht; Host-Konfiguration; Server-Scope | /var/empty und relative Lognamen. Durch beschreibbare Betreiberpfade ersetzen. |
| server.port | Dezimaler TCP-Listener-Port | Pflicht; Host-Konfiguration; Server-Scope | 8080. Für lokale Übungen privaten Listener binden. |
| proxy.server-Host und -Port | Upstream-Endpunkt | Pflicht; Host-Konfiguration; Proxy-Scope | 127.0.0.1:8081. Durch gewünschtes Backend ersetzen. |
| $HTTP-Hostausdruck | lighttpd-Selektor für Request-Host-Header | In diesem Beispiel Pflicht; Host-Konfiguration; Conditional-Scope | Passt auf jeden Host. Ist eine Host-Sprachvariable, keine Shellvariable und kein Secret. |

Ein separater betreiberseitiger Sidecar liegt außerhalb der Lifecycle-Claims der
nativen Beispiele.
