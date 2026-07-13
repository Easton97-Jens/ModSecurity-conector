> Generierte Datei – nicht manuell bearbeiten.
>
> Erstellt unter: `2026-06-19T16:22:55Z`
> Verifizierte Lauf-ID: `2026-06-16T19-12-00Z-614c8049`
> Datenquellenrichtlinie: `verified-inputs-only`
> Generator: `ci/update-runtime-reports.py`
> Ziel erstellen: `prepare-runtime-components`
> Besitzer: `cache`
> Schweregrad: `cache`
> Connector SHA: `5c9a0ceb2fb04dbc31347f1adc762512ed7fbf9f`
> Framework-SHA: `dc19582d89bd8ef50463c5a9c5a0271cc37bb958`
> Eingabestatus: `complete`

# Laufzeit-Cache-Index

**Sprache:** [English](runtime-cache-index.generated.md) | Deutsch

> Hinweis: Diese deutsche Datei ist eine übersetzte Begleitdatei zur generierten englischen Quelle. Maschinenlesbare Werte, Tabellen, IDs, Pfade und Metriken bleiben absichtlich unverändert. Bei einer Neuerzeugung der englischen Quelle muss diese Datei geprüft und aktualisiert werden.

- Status: `cache_input_present`
- Komponenten-Cache-Stamm: `<verified-run-root>/component-cache`
- Root erstellen: `<verified-run-root>/build`
- Komponentenpräsenz: `7/7`
- Wichtige Dateien vorhanden: `12/12`
- Richtlinie: Lokale Cache-Verzeichnisse und Binärdateien werden nicht festgeschrieben. Dieser generierte Index erfasst nur die Herkunft.

## Manifestiert

| Item | Status | SHA256 | Path |
|---|---|---|---|
| component-cache manifest | present | `3778b68a3aad6b58a8b178772552e423541ff7be524de4b074285d65ce6e7eec` | `<verified-run-root>/component-cache/manifest.json` |
| runtime build-cache manifest | present | `469f87fe5487ee2770567fa49e980ec79e88106f7c4b6f1cd37a4627bbba4789` | `<verified-run-root>/component-cache/runtime-build-cache.json` |
| git components manifest | present | `c4e18783b970500f25f92964b3035b9b441fe307da19582c3de4ce62b66b2b86` | `<verified-run-root>/component-cache/git-components.json` |
| runtime env | present | `4dc7cbd3c334faeac71db45df2839a4ff297029d8746d80f2cc38683429dedf8` | `<verified-run-root>/component-cache/runtime-env.sh` |

## Komponenten

| Component | Status | Build ID | Source / Path |
|---|---|---|---|
| modsecurity | reused | `0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72` | `<verified-run-root>/component-cache/prefix/modsecurity/0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72` |
| apache_httpd | reused | `898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67` | `<verified-run-root>/component-cache/builds/connectors/apache/898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67/build` |
| nginx | reused | `d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12` | `<verified-run-root>/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/build` |
| haproxy | reused | `599b09c9a142d357cf043c4b2046ec7dee4f3585edab18520c52968b06936048` | `<verified-run-root>/component-cache/builds/connectors/haproxy/599b09c9a142d357cf043c4b2046ec7dee4f3585edab18520c52968b06936048` |
| go_ftw | present | `-` | `<verified-run-root>/component-cache/bin/go-ftw` |
| albedo | present | `-` | `<verified-run-root>/component-cache/bin/albedo` |
| expat | present | `-` | `<verified-run-root>/component-cache/prefix/expat` |

## Wichtige Dateien

| Item | Status | SHA256 | Path |
|---|---|---|---|
| libmodsecurity | present | `61d6f374dfafb684b62415bd8ef97ccb3b8615516fd93b0f972f89eeb62125ca` | `<verified-run-root>/component-cache/prefix/modsecurity/0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72/lib/libmodsecurity.so` |
| apache_httpd | present | `82242c219cc91b9645d0bfbae8629be5afaf046bd2653a8c92cccab0b8bc40a2` | `<verified-run-root>/component-cache/builds/connectors/apache/898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67/httpd/bin/httpd` |
| apache_apxs | present | `9bac676928668024d7dbbd233e2c509ab6b6382bee472a374542f96dd1957036` | `<verified-run-root>/component-cache/builds/connectors/apache/898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67/httpd/bin/apxs` |
| apache_mod_security3 | present | `06c04934d991976410700bebb8418933643cc2cdd0e0952d94588fe5079b1182` | `<verified-run-root>/component-cache/builds/connectors/apache/898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67/build/output/apache/mod_security3.so` |
| nginx | present | `4b12b2bc1e056a68f42d0918e02ed9d8dbf455e5e1b6fdcedd9187297e98e459` | `<verified-run-root>/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/sbin/nginx` |
| nginx_modsecurity_module | present | `058c8d15f828864a09919b650d5e6c4293cf2ccb549aa0b3059f4f763ed6f773` | `<verified-run-root>/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/modules/ngx_http_modsecurity_module.so` |
| haproxy | present | `591fb673cd8dc2f0140c8eeed333b44940afcb461e50322e30e09cb05ea3cedb` | `<verified-run-root>/component-cache/builds/connectors/haproxy/599b09c9a142d357cf043c4b2046ec7dee4f3585edab18520c52968b06936048/haproxy-runtime/haproxy/sbin/haproxy` |
| haproxy_spoa | present | `058a20d2b33929b68b401b7916cdd6737faf52661a43400f93214b734b16b8ed` | `<verified-run-root>/component-cache/builds/connectors/haproxy/599b09c9a142d357cf043c4b2046ec7dee4f3585edab18520c52968b06936048/haproxy-spoa-runtime/haproxy-modsecurity-spoa` |
| go-ftw | present | `332425c41385ee10fa79c543ce8527c099873fd73bcaf73dd2a2cc353f84b952` | `<verified-run-root>/component-cache/bin/go-ftw` |
| albedo | present | `72872f718729f51e924fa8ba3c82b3b5eca9db6be4490fc5cbb731317f2ad1bd` | `<verified-run-root>/component-cache/bin/albedo` |
| expat_header | present | `52d756026bf09befdb211c453e2009a646d6c6b519e6885e971b2550396619fb` | `<verified-run-root>/component-cache/prefix/expat/include/expat.h` |
| shared_build_libmodsecurity | present | `61d6f374dfafb684b62415bd8ef97ccb3b8615516fd93b0f972f89eeb62125ca` | `<verified-run-root>/component-cache/prefix/modsecurity/0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72/lib/libmodsecurity.so` |

## Datenquellen

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `<verified-run-root>/component-cache/manifest.json` | `3778b68a3aad6b58a8b178772552e423541ff7be524de4b074285d65ce6e7eec` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/component-cache/runtime-build-cache.json` | `469f87fe5487ee2770567fa49e980ec79e88106f7c4b6f1cd37a4627bbba4789` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/component-cache/git-components.json` | `c4e18783b970500f25f92964b3035b9b441fe307da19582c3de4ce62b66b2b86` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/component-cache/runtime-env.sh` | `4dc7cbd3c334faeac71db45df2839a4ff297029d8746d80f2cc38683429dedf8` | `2026-06-16T19-12-00Z-614c8049` | present |

## Datenverfügbarkeit / fehlende Informationen

| Input | Status | Notes |
|---|---|---|
| `<verified-run-root>/component-cache/manifest.json` | present | input file available |
| `<verified-run-root>/component-cache/runtime-build-cache.json` | present | input file available |
| `<verified-run-root>/component-cache/git-components.json` | present | input file available |
| `<verified-run-root>/component-cache/runtime-env.sh` | present | input file available |
