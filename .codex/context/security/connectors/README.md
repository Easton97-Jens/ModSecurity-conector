# Connector Security Delta Index

The Parent documents six host families and ten logical connector solutions. Each logical solution has its own evidence boundary.

| Host family | Logical profile | Role |
| --- | --- | --- |
| Apache | `apache` | direct native HTTPD module |
| NGINX | `nginx` | direct native NGINX HTTP module |
| HAProxy | `haproxy-htx` | direct native HTX filter |
| HAProxy | `haproxy-spoe-spop` | SPOP P1/P2 plus mandatory native-HTX response companion for P3/P4 |
| Envoy | `envoy-ext-proc` | direct streamed external processing |
| Envoy | `envoy-ext-authz` | request authorization plus mandatory response observer |
| Traefik | `traefik-native-uds` | native middleware plus private UDS engine |
| Traefik | `traefik-forwardauth` | request authorization plus mandatory response observer |
| lighttpd | `lighttpd-stock` | traffic-owning bounded HTTP/1.1 Stock sidecar |
| lighttpd | `lighttpd-patched` | separate patched-native host/module route |

Do not collapse logical profiles into a host-family PASS. Build/config/runtime evidence for one profile is not evidence for another.
