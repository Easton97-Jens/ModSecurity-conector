# Traefik forwardAuth compatibility example

**Language:** English | [Deutsch](README.de.md)

These files preserve the former request-authorization configuration. They are
separate from the native local-plugin/UDS core in [../safe/](../safe/).

## Values to adapt

| Name | Purpose and format | Required/default, setter, scope | Example and boundary |
| --- | --- | --- | --- |
| entryPoints.web.address | Listener address string | Required; static file; Traefik static scope | :8080. A public listener changes exposure. |
| providers.file.filename | Dynamic-file path relative to the Traefik working directory | Required; static file; File Provider scope | ./traefik-dynamic.yaml. Copy both compatibility files together if using this route. |
| router rule and entryPoints | Request matcher and named entry point | Required; dynamic file; router scope | PathPrefix for all paths and web. Restrict for a real deployment. |
| forwardAuth address | Authorization service HTTP URL | Required; dynamic file; middleware scope | http://127.0.0.1:9000/authorize. Do not embed tokens or credentials in it. |
| trustForwardHeader | Boolean forwarded-header policy | Required; dynamic file; middleware scope | false. Changing it alters trust boundaries and needs an explicit proxy-header policy. |
| app service URL | Upstream HTTP URL | Required; dynamic file; service scope | http://127.0.0.1:8081. Replace for deployment. |

forwardAuth runs before upstream response processing. It must not be described
as P3/P4 inspection, native middleware behavior, Safe late behavior, Strict
behavior, first-byte evidence, or no-full-response-buffer evidence.
