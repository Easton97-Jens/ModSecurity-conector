# Envoy ext_authz compatibility example

**Language:** English | [Deutsch](README.de.md)

This file is the former request-phase Envoy example. It configures an HTTP
ext_authz call before routing to the upstream and remains separate from the
streamed ext_proc core in [../safe/](../safe/).

## Values to adapt

| Name | Purpose and format | Required/default, setter, scope | Example and boundary |
| --- | --- | --- | --- |
| listener socket address and port_value | TCP listener address and decimal port | Required; YAML static resources; listener scope | 0.0.0.0:8080. Bind loopback for a local exercise unless exposure is intentional. |
| modsecurity_authz | ext_authz cluster name | Required; YAML cluster and filter; filter scope | Endpoint 127.0.0.1:9000. It must be a trusted authorization service. |
| server_uri and timeout | Authorization HTTP URI and positive duration | Required; ext_authz filter; request scope | http://127.0.0.1:9000 and 0.2s. A timeout is not response-phase evidence. |
| authorization and content-type | Allowed request-header names | Optional filter allow-list; request scope | Header names only, not secret values. Do not put credentials in this file. |
| app_backend | Upstream cluster name and endpoint | Required; route and cluster; route scope | 127.0.0.1:8081. Replace with the intended application endpoint. |

ext_authz does not make the later upstream response available to this service.
It is not P3/P4, Safe late-intervention, Strict, first-byte, or no-buffer
evidence.
