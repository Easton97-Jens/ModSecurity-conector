# Einstieg

**Sprache:** [English](getting-started.md) | Deutsch

Dieser Guide ist der kürzeste Weg von einem frischen Clone zu einem korrekt
eingeordneten Entwicklungs-Checkout. Er endet bewusst vor jeder Aussage über
Production Readiness oder Runtime-Qualität.

## 1. Klonen und initialisieren

```sh
git clone --recurse-submodules https://github.com/Easton97-Jens/ModSecurity-conector.git
cd ModSecurity-conector
make check-framework
```

Wenn ohne Submodule geklont wurde, führen Sie vor `make check-framework`
`git submodule update --init --recursive` aus.

## 2. Checkout validieren

```sh
make quick-check
```

Dies prüft Repository-Verträge, Dokumentation und ausgewählte strukturelle
Anforderungen. Es baut **nicht** jeden Host, sendet keinen Traffic durch jeden
Connector und erzeugt keine kanonische Lifecycle-Evidence.

## 3. Host und logisches Profil wählen

| Hostfamilie | Beginnen mit | Zusätzliches logisches Profil |
| --- | --- | --- |
| Apache | `apache` | — |
| NGINX | `nginx` | — |
| HAProxy | `haproxy-htx` | `haproxy-spoe-spop` |
| Envoy | `envoy-ext-proc` | `envoy-ext-authz` |
| Traefik | `traefik-native-uds` | `traefik-forwardauth` |
| lighttpd | `lighttpd-patched` | `lighttpd-stock` |

Lesen Sie vor der Wahl eines alternativen logischen Profils den
[Connector-Index](connectors/README.de.md). Alternative Profile können andere
Request-/Response-Sichtbarkeit und andere Runtime-Grenzen besitzen.

## 4. Beispielprofil wählen

Öffnen Sie den [Beispielindex](../examples/README.de.md) und wählen Sie die
passende logische Lösung. Als praktische Regel:

- `safe` ist der beste Einstieg, um die vollständige eingecheckte
  P1–P4-Konfigurationsform zu verstehen, ohne einen späten client-sichtbaren
  Abbruch anzunehmen.
- `off` deaktiviert das zusätzliche connector-eigene kumulative
  Phase-4-Budget; die konfigurierte Response-Body-Inspection von libmodsecurity
  wird dadurch nicht deaktiviert.
- `strict` drückt die strikte Late-Action-Policy aus, ist aber nur dort
  ausführbar, wo der ausgewählte Host/das Profil die nötige Aktion unterstützt.
- `all` ist das umfassende quellenbasierte Konfigurationslayout. Es wählt
  gültige Einstellungen (typischerweise einschließlich `strict`);
  `all` ist kein vierter Phase-4-Modus.

Halten Sie außerdem `DetectionOnly`, Engine `Off` und einen deaktivierten
Connector auseinander: Sie verändern unterschiedliche Ebenen.

## 5. Einen ausgewählten Host bauen oder prüfen

Verwenden Sie das Root-Makefile statt eines direkten Connector-Harness-Aufrufs.
Zum Beispiel:

```sh
make build-nginx
make check-config-nginx
```

Ersetzen Sie `nginx` dort, wo das Target existiert, durch einen der sechs im
Root-Makefile dokumentierten Hostfamiliennamen. Build-Erfolg belegt nur den
Build-Schritt; Konfigurationserfolg belegt nur, dass der ausgewählte Host seine
Konfiguration akzeptiert hat.

## 6. Lifecycle-Evidence nur für eine benötigte Runtime-Aussage ausführen

Für einen aggregierten Run des ausgewählten Kerns verwenden Sie eine
dateisystemsichere, nicht geheime Run-ID:

```sh
run_id="core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-all-connectors
NO_CRS_RUN_ID="$run_id" make check-six-connector-core-completion
```

Das Validierungsergebnis gilt nur für diesen Run, seine ausgewählten Profile,
Rules, den Protokoll-Scope und seine Artefakte.

## Was Erfolg bedeutet

Exit-Status null bedeutet, dass der ausgeführte Befehl **seinen eigenen
Vertrag** erfüllt hat. Das bedeutet nicht automatisch:

- Production Readiness oder Production Hardening;
- CRS-Verifikation;
- vollständige HTTP/2- oder HTTP/3-Abdeckung;
- vollständige Protokoll-/Profilmatrix; oder
- Strict-Post-Commit-Verhalten für jeden Connector.

## Wie es weitergeht

| Bedarf | Dokument |
| --- | --- |
| konkrete Konfiguration wählen | [Beispiele](../examples/README.de.md) |
| Host/Profil verstehen | [Connector-Index](connectors/README.de.md) |
| Einstellungen verstehen | [Konfiguration](configuration.de.md) |
| Build-Details | [Build](build/README.de.md) |
| Test-/Ergebnis-Semantik | [Tests und Nachweise](testing-and-evidence.de.md) |
| sicherer Betrieb | [Betrieb und Sicherheit](operations-and-security.de.md) |
