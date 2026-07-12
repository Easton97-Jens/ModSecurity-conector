# Envoy-ext_authz-Kompatibilitätsbeispiel

**Sprache:** [English](README.md) | Deutsch

Diese Datei ist das frühere Envoy-Request-Phasen-Beispiel. Sie konfiguriert
einen HTTP-ext_authz-Aufruf vor dem Routing zum Upstream und bleibt vom
gestreamten ext_proc-Kern unter [../safe/](../safe/) getrennt.

## Anzupassende Werte

| Name | Zweck und Format | Pflicht/Default, Setzer, Geltungsbereich | Beispiel und Grenze |
| --- | --- | --- | --- |
| Listener-Socket-Adresse und port_value | TCP-Listener-Adresse und dezimaler Port | Pflicht; YAML static resources; Listener-Scope | 0.0.0.0:8080. Für lokale Übungen Loopback binden, sofern keine Freigabe beabsichtigt ist. |
| modsecurity_authz | ext_authz-Clustername | Pflicht; YAML-Cluster und Filter; Filter-Scope | Endpunkt 127.0.0.1:9000. Muss ein vertrauenswürdiger Authorization-Service sein. |
| server_uri und timeout | Authorization-HTTP-URI und positive Dauer | Pflicht; ext_authz-Filter; Request-Scope | http://127.0.0.1:9000 und 0.2s. Ein Timeout ist keine Response-Phasen-Evidence. |
| authorization und content-type | Erlaubte Request-Headernamen | Optionaler Filter-Allow-List; Request-Scope | Nur Headernamen, keine Geheimwerte. Keine Credentials in diese Datei schreiben. |
| app_backend | Upstream-Clustername und Endpunkt | Pflicht; Route und Cluster; Route-Scope | 127.0.0.1:8081. Durch gewünschten Application-Endpunkt ersetzen. |

ext_authz macht die spätere Upstream-Response diesem Service nicht zugänglich.
Es ist keine P3/P4-, Safe-Late-Intervention-, Strict-, First-Byte- oder
No-Buffer-Evidence.
