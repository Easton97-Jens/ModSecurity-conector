# Envoy-P1--P4-Safe-Absicht

**Sprache:** [English](p1-p4-safe.md) | Deutsch

Die ext_proc-Referenz setzt beide Body-Modi auf STREAMED und die
Service-Policy auf safe. Sie ist die native Full-Lifecycle-Referenz. Ein
P4-Ergebnis nach dem Start der Response wird als Safe-Log-only dargestellt,
nicht als behaupteter später HTTP-Statuswechsel oder deterministischer
Stream-Reset.

Die separate ext_authz-Konfiguration kann weder Upstream-Response-Header noch
-Bodies sehen und wird deshalb absichtlich nicht als P3/P4-Kernpfad
beschrieben. Es gibt kein Strict-Beispiel.
