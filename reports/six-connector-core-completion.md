# Six-connector HTTP/1.1 core completion

**Language:** English | [Deutsch](six-connector-core-completion.de.md)

## Evidence boundary

This is the compact working matrix for the selected real HTTP/1.1 hosts. It
records only the existing core catalog cases and their final canonical-run
evidence. Strict transport handling, HTTP/2, HTTP/3, and the remaining
catalog are outside this milestone.

| Connector | P1 | P2 | P3 | P4 rule | P4 Safe | First byte | No full buffer | Cleanup | Current blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Apache | Pending final native-host run | Pending final native-host run | Pending final native-host run | Pending final native-host run | Pending final native-host run | Pending final native-host run | Pending final native-host run | Pending final lifecycle inventory | Fresh aggregate run |
| NGINX | Pending final native-host run | Pending final native-host run | Pending final native-host run | Pending final native-host run | Pending final native-host run | Pending final native-host run | Pending final native-host run | Pending final lifecycle inventory | Fresh aggregate run |
| HAProxy | Pending final HTX run | Pending final HTX P2 run | Pending final HTX run | Pending final HTX P4 run | Pending final HTX P4 run | Pending final HTX barrier | Pending final HTX barrier | Pending final lifecycle inventory | Fresh aggregate run |
| Envoy | Pending final ext_proc run | Pending final ext_proc run | Pending final ext_proc run | Pending final ext_proc run | Pending final ext_proc run | Pending final ext_proc barrier | Pending final ext_proc barrier | Pending final lifecycle inventory | Fresh aggregate run |
| Traefik | Pending final native-middleware run | Pending final native-middleware run | Pending final native-middleware run | Pending final native-middleware run | Pending final native-middleware run | Pending final native barrier | Pending final native barrier | Pending final lifecycle inventory | Fresh aggregate run |
| lighttpd | Pending final patched-host run | Pending final patched-host run | Pending final patched-host run | Pending final entity-body P4 run | Pending final entity-body P4 run | Pending final patched-host barrier | Pending final patched-host barrier | Pending final lifecycle inventory | Fresh aggregate run |

The corresponding current-run IDs and PASS/FAIL/NOT EXECUTED outcomes are
recorded here only after the individual and shared canonical runs finish.
