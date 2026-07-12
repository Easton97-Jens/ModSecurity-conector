# lighttpd sidecar compatibility example

**Language:** English | [Deutsch](README.de.md)

This retained file is an illustrative lighttpd proxy setup. It does not load
mod_msconnector.so and therefore is not the native lighttpd core reference.
Use [../minimal/](../minimal/) for the stock native module shape or
[../safe/](../safe/) for the patched HTTP/1.1 identity-entity reference.

| Name | Purpose and format | Required/default, setter, scope | Example and boundary |
| --- | --- | --- | --- |
| server.modules | Installed lighttpd proxy and logging modules | Required; host config; server scope | mod_accesslog and mod_proxy. This is not mod_msconnector. |
| server.document-root and log paths | Host filesystem paths | Required; host config; server scope | /var/empty and relative log names. Replace with writable operator paths. |
| server.port | Decimal TCP listener port | Required; host config; server scope | 8080. Bind a private listener for a local exercise. |
| proxy.server host and port | Upstream endpoint | Required; host config; proxy scope | 127.0.0.1:8081. Replace with the intended backend. |
| $HTTP host expression | lighttpd request Host-header selector | Required in this example; host config; conditional scope | Matches every host. It is a host-language variable, not a shell variable or secret. |

A separate operator-supplied sidecar remains outside lifecycle claims made by
the native examples.
