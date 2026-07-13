> Generierte Datei – nicht manuell bearbeiten.
>
> Erstellt unter: `2026-06-19T16:22:55Z`
> Verifizierte Lauf-ID: `2026-06-16T19-12-00Z-614c8049`
> Datenquellenrichtlinie: `verified-inputs-only`
> Generator: `ci/prepare-runtime-components.py`
> Ziel erstellen: `prepare-runtime-components`
> Besitzer: `cache`
> Schweregrad: `cache`
> Connector SHA: `5c9a0ceb2fb04dbc31347f1adc762512ed7fbf9f`
> Framework-SHA: `dc19582d89bd8ef50463c5a9c5a0271cc37bb958`
> Eingabestatus: `complete`

# Laufzeitkomponenten-Cache

**Sprache:** [English](runtime-component-cache.generated.md) | Deutsch

> Hinweis: Diese deutsche Datei ist eine übersetzte Begleitdatei zur generierten englischen Quelle. Maschinenlesbare Werte, Tabellen, IDs, Pfade und Metriken bleiben absichtlich unverändert. Bei einer Neuerzeugung der englischen Quelle muss diese Datei geprüft und aktualisiert werden.

- Cache-Root: `<verified-run-root>/component-cache`
- Root erstellen: `<verified-run-root>/build`
- Erstellt unter: `2026-06-19T16:22:55Z`
- Lokale Cache-Binärdateien und Quellbäume werden nicht festgeschrieben. In diesem Bericht wird die Herkunft dokumentiert.

| Component | Status | Build ID / Ref | Path |
|---|---|---|---|
| modsecurity | reused | `0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72` | `<verified-run-root>/component-cache/prefix/modsecurity/0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72` |
| apache_httpd | reused | `898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67` | `<verified-run-root>/component-cache/builds/connectors/apache/898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67/build` |
| nginx | reused | `d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12` | `<verified-run-root>/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/build` |
| haproxy | reused | `599b09c9a142d357cf043c4b2046ec7dee4f3585edab18520c52968b06936048` | `<verified-run-root>/component-cache/builds/connectors/haproxy/599b09c9a142d357cf043c4b2046ec7dee4f3585edab18520c52968b06936048` |
| go_ftw | present | `v2.4.0` | `<verified-run-root>/component-cache/bin/go-ftw` |
| albedo | present | `v0.3.0` | `<verified-run-root>/component-cache/bin/albedo` |
| expat | present | `R_2_8_1` | `<verified-run-root>/component-cache/prefix/expat` |

## Datenquellen

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `<verified-run-root>/component-cache/manifest.json` | `3778b68a3aad6b58a8b178772552e423541ff7be524de4b074285d65ce6e7eec` | `2026-06-16T19-12-00Z-614c8049` | present |

## Datenverfügbarkeit / fehlende Informationen

| Input | Status | Notes |
|---|---|---|
| `<verified-run-root>/component-cache/manifest.json` | present | input file available |

<!-- runtime-components:start -->
## Laufzeitkomponenten

### Apache httpd
- Status: `reused`
- Blocker: `-`
- Cache-Pfad: `<verified-run-root>/component-cache/archives/apache`
- Build-Pfad: `<verified-run-root>/component-cache/builds/connectors/apache/898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67/build`
- apachectl/APACHECTL_BIN: `<verified-run-root>/component-cache/builds/connectors/apache/898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67/httpd/bin/apachectl-mrts`
- Moduldatei: `<verified-run-root>/component-cache/builds/connectors/apache/898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67/build/output/apache/mod_security3.so`
- Fehlende Datei: `-`
- Build-Komponente: `-`
- Zu setzende Env-Variable: `APACHECTL_BIN`
- Expat-Quelle: `https://github.com/libexpat/libexpat`
- Tag der Expat-Veröffentlichung: `R_2_8_1`
- CPPFLAGS: `-I<verified-run-root>/component-cache/prefix/expat/include`
- LDFLAGS: `-L<verified-run-root>/component-cache/prefix/expat/lib`
- LIBS: `-lcrypt`
- PKG_CONFIG_PATH: `<verified-run-root>/component-cache/prefix/expat/lib/pkgconfig`
- crypt.h Status: `present`
- crypt.h Pfad: `/usr/include/crypt.h`
- libcrypt-Status: `present`
- libcrypt-Pfade: `/usr/lib/x86_64-linux-gnu/libcrypt.so, /lib/x86_64-linux-gnu/libcrypt.so, /usr/lib/x86_64-linux-gnu/libcrypt.so.1, /lib/x86_64-linux-gnu/libcrypt.so.1`
- Crypt-Link-Modus: `compiler:-lcrypt`

### NGINX
- Status: `reused`
- Blocker: `-`
- Cache-Pfad: `<verified-run-root>/component-cache/archives/nginx`
- Build-Pfad: `<verified-run-root>/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/build`
- MRTS_NATIVE_NGINX_BIN: `<verified-run-root>/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/sbin/nginx`
- MRTS_NATIVE_NGINX_MODULE_DIR: `<verified-run-root>/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/modules`
- Moduldatei: `<verified-run-root>/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/modules/ngx_http_modsecurity_module.so`
- Fehlende Datei: `-`
- Build-Komponente: `-`
- Zu setzende Env-Variable: `MRTS_NATIVE_NGINX_BIN/MRTS_NATIVE_NGINX_MODULE_DIR`

### Expat
- Status: `present`
- Blocker: `-`
- Quelle: `https://github.com/libexpat/libexpat`
- Release-Tag: `R_2_8_1`
- Tatsächlicher Kopf: `c7ffbf3879f6aef7a7b020ef84ddb4ee00222b19`
- Präfix: `<verified-run-root>/component-cache/prefix/expat`
- expat.h: `<verified-run-root>/component-cache/prefix/expat/include/expat.h`
- lib dir: `<verified-run-root>/component-cache/prefix/expat/lib`
- Rekursive Untermodule: `-`

### go-ftw / albedo
| Dependency | Status | Binary | Env override | Source | Release tag | Head | Submodules | Release note | Blocker |
|---|---|---|---|---|---|---|---|---|---|
| go-ftw | present | `<verified-run-root>/component-cache/bin/go-ftw` | `GO_FTW_BIN` | `https://github.com/coreruleset/go-ftw` | `v2.4.0` | `23db497e3a6133888fcd5e087b8cf456556df041` | `-` | prompt_expected_latest=v2.2.0; current_latest=v2.4.0 | - |
| albedo | present | `<verified-run-root>/component-cache/bin/albedo` | `ALBEDO_BIN` | `https://github.com/coreruleset/albedo` | `v0.3.0` | `3f7d0238b32d1f98059f5c70e0ffcafad514952c` | `-` | - | - |
<!-- runtime-components:end -->

<!-- runtime-build-cache:start -->
## Laufzeit-Build-Cache
- Geteilter ModSecurity-Status: `reused`
- Geteilte ModSecurity-Quelle ref/SHA: `v3/master` / `2fd49292d751fc383b8faf7da6a8d480904774d0`
- Geteilter ModSecurity-Build ID: `0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72`
- Gemeinsames ModSecurity-Präfix: `<verified-run-root>/component-cache/prefix/modsecurity/0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72`
- Zusammenfassung der Build-Wiederverwendung: neu erstellt `0`, wiederverwendet `3`, blockiert `0`, gespeicherte Neuaufbauschätzung `3`

| Connector | Status | Connector build ID | Uses ModSecurity build ID | Blocker |
|---|---|---|---|---|
| apache | reused | `898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67` | `0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72` | - |
| nginx | reused | `d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12` | `0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72` | - |
| haproxy | reused | `599b09c9a142d357cf043c4b2046ec7dee4f3585edab18520c52968b06936048` | `0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72` | - |
<!-- runtime-build-cache:end -->

<!-- runtime-diagnostics:start -->
## Native Laufzeitdiagnose

- Es wurden keine generierten nativen Laufzeitdiagnosen erkannt.
<!-- runtime-diagnostics:end -->
