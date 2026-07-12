# Minimale ext_proc-Referenz

**Sprache:** [English](README.md) | Deutsch

Der ausgewählte Envoy-Kern benötigt gestreamte ext_proc-Eingaben in beiden
Richtungen. Dieses Verzeichnis liefert deshalb eine vollständige minimale
Transportform in
[envoy-ext-proc-streaming.yaml.in](envoy-ext-proc-streaming.yaml.in), ihren
validierten Service-Vertrag und eine passende Common-Runtime-Datei mit
`phase4_mode=minimal`. Es ist kein nativer Request-only-Pfad: Die Bridge
benötigt weiterhin STREAMED-Request- und Response-Body-Modi. Das getrennte
ext_authz-Request-only-Material bleibt unter
[compatibility-ext-authz](../compatibility-ext-authz/README.de.md).
