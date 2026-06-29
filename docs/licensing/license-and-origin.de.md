# Lizenz und Herkunft

**Sprache:** [English](license-and-origin.md) | Deutsch

Status: umgesetzt

Dieses Repository enthält kontrollierte Importe des Apache-2.0-lizenzierten Connectors
Code. Die importierten Quelldateien bleiben Connector-spezifisch und werden dokumentiert in:

- `connectors/apache/ORIGIN.md`
- `connectors/nginx/ORIGIN.md`

Der zentrale Attributionsindex wird unter `licenses/` gespeichert. Es spiegelt das wider
Upstream-Lizenz- und Namensnennungsdateien zur schnellen Überprüfung. Jetzt Apache und NGINX
aus Adapter-eigenen Quellbäumen erstellen; ihre frühere lokale `upstream/`-Referenz
Bäume wurden nach materialisierten Bauten und realer Smokedichtigkeit entfernt.

## Apache-Connector

| Repository | Repo-lokale Referenz | Upstream | Beobachteter Commit | Beobachtet version/tag | Lizenz |
| --- | --- | --- | --- | --- | --- |
| ModSecurity-Apache | `connectors/apache/`, `licenses/apache/` | https://github.com/owasp-modsecurity/ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | `v0.0.9-beta1-26-g0488c77` | Apache-2.0 |

Beobachtete Quellenrevision:

- Zweig: `master`
- Commit: `0488c77f69669584324b70460614a382224b4883`
- beschreiben: `v0.0.9-beta1-26-g0488c77`
- Lizenz: Apache-Lizenz 2.0

Die Upstream-Dateien `LICENSE`, `AUTHORS` und `CHANGES` bleiben in erhalten
`licenses/apache/`. Apache-Quelle und Autotools/APXS-Build-Eingaben sind
Adapter im Besitz unter `connectors/apache/`, mit produktiven C-Dateien in
`connectors/apache/src/` und Quellenherkunft aufgezeichnet in
`connectors/apache/SOURCE_MAP.json` und `connectors/apache/ORIGIN.md`. Der
Der frühere `connectors/apache/upstream/`-Baum wurde in Phase 11 entfernt. Phase 13
Behält Attributions- und Support-Metadaten außerhalb des strengen Produktquellenbaums.

Zentrale Zuschreibungskopien:

- `licenses/apache/LICENSE`
- `licenses/apache/AUTHORS`
- `licenses/apache/CHANGES`
- `licenses/apache/ORIGIN.md`

## NGINX-Connector

| Repository | Repo-lokale Referenz | Upstream | Beobachteter Commit | Beobachtet version/tag | Lizenz |
| --- | --- | --- | --- | --- | --- |
| ModSecurity-nginx | `connectors/nginx/`, `licenses/nginx/` | https://github.com/owasp-modsecurity/ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | `v1.0.4-14-g9eb44fd` | Apache-2.0 |

Beobachtete Quellenrevision:

- Zweig: `master`
- Commit: `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846`
- beschreiben: `v1.0.4-14-g9eb44fd`
- Lizenz: Apache-Lizenz 2.0

Die Upstream-Dateien `LICENSE`, `AUTHORS` und `CHANGES` bleiben in erhalten
`licenses/nginx/`. Das NGINX-Modul `config` gehört zum Adapter
`connectors/nginx/config`, produktive Quelldateien sind unter
`connectors/nginx/src/` und die Herkunft der Quelle wird darin aufgezeichnet
`connectors/nginx/SOURCE_MAP.json` und `connectors/nginx/ORIGIN.md`. Ersteres
Der `connectors/nginx/upstream/`-Baum wurde in Phase 10 entfernt.

ModSecurity-nginx PR #377
(https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/377) Quelle
Änderungen beim Commit `3d72b004ff27a78ea19c6b945870e2cae62a97ac` werden aufgezeichnet
die adaptereigenen Phase-4-Dateien. Dadurch wird `RESPONSE_BODY` nicht zu a hochgestuft
verifizierte Variable.

Zentrale Zuschreibungskopien:

- `licenses/nginx/LICENSE`
- `licenses/nginx/AUTHORS`
- `licenses/nginx/CHANGES`
- `licenses/nginx/ORIGIN.md`

## ModSecurity Engine-Referenzen

ModSecurity v2 und v3 sind schreibgeschützte Referenz-Repositories, keine importierte Engine
Quellbäume. Ihre beobachteten Revisionen und Lizenzbeobachtungen sind in dokumentiert
`licenses/modsecurity/README.md`.

| Repository | Repo-lokale Referenz | Upstream | Beobachteter Commit | Beobachtet version/tag | Lizenz |
| --- | --- | --- | --- | --- | --- |
| ModSecurity v2 | `licenses/modsecurity/` | https://github.com/owasp-modsecurity/ModSecurity | `02eed22d74667b32091eece088a8ebdf64b6ba67` | `v2.9.13` | Apache-2.0 |
| ModSecurity v3 | `licenses/modsecurity/` | https://github.com/owasp-modsecurity/ModSecurity | `0fb4aff98b4980cf6426697d5605c424e3d5bb60` | `v3.0.15` | Apache-2.0 |

## Regeln

– Importieren Sie keine Upstream-`.git`-Verzeichnisse oder generierte Build-Artefakte.
- Behaupten Sie nicht, dass importierter Code funktioniert, es sei denn, der Smoke Harness erstellt ihn und führt ihn aus.
- Verschieben Sie Code nicht ohne einen separaten Prüf- und Überprüfungsschritt in `common/`.
- Halten Sie Ursprungskarten auf dem neuesten Stand, wenn importierte Dateien hinzugefügt, entfernt oder entfernt werden
von Upstream aktualisiert.
- Halten Sie `licenses/` mit importierten Quellquellen und Lizenzdateien synchronisiert.
– Halten Sie attribution/history-Dateien von funktionalen, adaptereigenen Quellbäumen fern
es sei denn, ein Build-System erfordert sie ausdrücklich.
- Entfernen Sie keine Adapter-eigenen Quelldateien zur kosmetischen Bereinigung. nur reduzieren
Nach dem Austausch wurde die Namensnennung beibehalten und es wurden Smoke-Traces festgestellt. Apache
und NGINX behalten keine lokalen `upstream/`-Bäume mehr; dauerhafte Zuschreibung lebt
unter `licenses/apache/` und `licenses/nginx/`.

## Schnittbewertung

Die aktuell importierten Connector-Bäume wurden überprüft
`modules/ModSecurity-test-Framework/docs/imports/upstream-pruning-analysis.md` und zusammengefasst in
`modules/ModSecurity-test-Framework/docs/imports/minimal-upstream-file-set.md`.

Spätere Ersetzungs- und Reduzierungsphasen entfernten den importierten NGINX-Debug-Helfer,
migrierten NGINX `config`/`src/*` in adaptereigenen Quellcode und entfernten danach den
verbleibenden NGINX-Upstream-Referenzbaum nach Smoke-Nachweis. Phase 11 migrierte
Apache-Quelle, Autotools/APXS-Eingaben und erforderliche `.in`-Vorlagen in die
Adaptereigener Apache-Baum, erwies sich als materialisierter Build- und Smoke-Run und
Der ehemalige Apache-Upstream-Baum wurde entfernt. Phase 13 hat Support-Metadaten aus verschoben
`src/` und `src/` konzentrierten sich weiterhin auf die produktive Quelle. Jede zukünftige Reduzierung muss
dokumentiert werden
relevanten `ORIGIN.md`, behalten Sie die Lizenz- und Namensnennungsabdeckung bei und bestehen Sie eine
Isolierte `$BUILD_ROOT` build/smoke-Sonde, bevor sie festgeschrieben wird.
