# Minimale ext_proc-Referenz

**Sprache:** [English](README.md) | Deutsch

Der ausgewählte Envoy-Kern benötigt eine gestreamte ext_proc-Konfiguration für
alle vier Phasen. Deshalb gibt es hier keine zweite native Request-only-
Konfiguration. Ausgangspunkt ist [das Safe-Template](../safe/envoy-ext-proc-streaming.yaml.in)
mit seiner Safe-Policy. Das separate ext_authz-Request-only-Material liegt
unter [compatibility-ext-authz](../compatibility-ext-authz/README.de.md).
