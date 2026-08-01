# FND-PARENT-0042 — Parent-Runtime-Komponenten-Cache bindet den NGINX-Release-Digest an ein anderes Tag-Archiv

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-PARENT-0042 |
| Kategorie | ci_failure |
| Repository / Ownership | parent / parent |
| Priorität / Severity | P1 / not_applicable |
| Konfidenz / Status | validated / blocked |
| Feasibility | blocked_environment nach lokal belegter Source-Korrektur |
| Release-Blocker | ja |
| Sicherheitsrelevant | ja |

## Beobachtung und Auswirkung

Die isolierte Parent-PR-#55-Runtime-Evidence-Vorbereitung wählte
`https://github.com/nginx/nginx/archive/refs/tags/release-1.31.2.tar.gz`,
wendete aber den geprüften SHA-256 des anderen GitHub-Release-Assets
`nginx-1.31.2.tar.gz` an. Das zurückgehaltene Manifest dokumentiert erwartet
`af2a957c41da636ddc4f883e4523c6d140b4784dbce42000c364ae5092aa473c` und
beobachtet `d886473e988ce6802d897310421e3ef038c06edc66c5424cd33ed1b15382e323`.
Die Prüfsummen-Kontrolle scheiterte korrekt fail-closed mit `sha256_mismatch`.

Kein ungeprüftes Archiv wurde verwendet. Die Auswirkung betrifft die
Verfügbarkeit legitimer Evidence: Die erforderliche NGINX-Komponente kann
nicht vorbereitet werden, daher können die aktuelle Runtime-Matrix für
`FND-CROSS-0001` und die geschützte Integration von PR #55 nicht fortfahren.

Die lokale Parent-Korrektur leitet nun ausschließlich
`https://github.com/nginx/nginx/releases/download/release-1.31.2/nginx-1.31.2.tar.gz`
ab, nachdem die vollständige gepinnte Release-Identität validiert wurde. Ihr
zurückgehaltenes Runtime-Manifest dokumentiert Archivstatus `present`,
Prüfsummenstatus `PASS` und passende erwartete/beobachtete SHA-256
`af2a957c41da636ddc4f883e4523c6d140b4784dbce42000c364ae5092aa473c`.
Der ursprüngliche `sha256_mismatch` reproduziert daher nicht mehr. Die legitime
Vorbereitung stoppt anschließend unabhängig bei `missing_nginx_modsecurity_module`
mit NGINX-Build-Exit `77`; dies ist keine vollständige Native-/Runtime-Evidence.

## Evidence, Ursache und Source-Korrektur

- Run: `20260720T163253Z-pr55-runtime-evidence-refresh-698b1734`
- Zurückgehaltenes Artefakt:
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T163253Z-pr55-runtime-evidence-refresh-698b1734/evidence/runtime-component-manifest-initial-failure.json`
- Artefakt-SHA-256:
  `d7e6517fe8be3a610dd51478cbb45c2fe9b4af3b1720562076129e24822efac3`
- Befehl: isoliertes `make prepare-runtime-components`, dessen sämtliche
  Output-Wurzeln im registrierten Task-Run liegen; Exit-Code `2`.

- Korrigierter Run: `20260721T005621Z-fnd-parent-0042-release-asset-b9e7172d`
- Korrigiertes Runtime-Manifest:
  `/var/tmp/codex/ModSecurity-conector/runs/20260721T005621Z-fnd-parent-0042-release-asset-b9e7172d/build/runtime-component-reports/reports/testing/generated/cache/runtime-component-cache.generated.json`
- SHA-256 des korrigierten Manifests:
  `3adf2284d3318cc35e690d319a84fe27200fe33047f43db22a328bf3c986253a`
- Finaler Validation-Receipt:
  `/var/tmp/codex/ModSecurity-conector/runs/20260721T005621Z-fnd-parent-0042-release-asset-b9e7172d/evidence/fnd-parent-0042-final-validation-20260721T014617Z.json`
- SHA-256 des finalen Receipts:
  `448fe124b2e1ed12a27e9402a38bc01d8809a2d7eee0fa9f14f9bcb0dbadf970`
- Ergebnis der korrigierten Vorbereitung: Das geprüfte Release-Asset bestand
  seine Prüfsummengrenze und stoppte anschließend bei
  `missing_nginx_modsecurity_module`, NGINX-Build-Exit `77`.

Auf der Source-Basis baute `resolve_nginx_archive` im Modus `github-release`
eine GitHub-Tag-Archiv-URL. Sein Shell-Wrapper übergab den bereits
konfigurierten `NGINX_RELEASE_ASSET_NAME` nicht, sodass der Resolver die
passende Release-Download-URL nicht bauen und validieren konnte. Der direkte
Framework-NGINX-Provisioner verwendet bereits das korrekte Release-Asset; dies
ist deshalb ein separater Parent-Cache-Provider-Defekt und keine Wiederöffnung
von `FND-FRAMEWORK-0006`.

Die lokale Implementierung exportiert `NGINX_RELEASE_ASSET_NAME` und
`NGINX_SHA256`, verwendet `nginx_release_asset_identity()` für das kanonische
HTTPS-GitHub-Repository, passende konfigurierte Aliase, exakten Tag/Ref,
aus dem Tag abgeleiteten Asset-Namen und SHA-256 mit 64 Kleinbuchstaben/Hex-
Zeichen und besitzt keinen Latest-Lookup oder Tag-Archiv-Fallback.
`github_repo_path()` weist prozentkodierte, reservierte, Dot-Segment-,
fehlgebildete Owner- und überlange Repository-Komponenten vor der generischen
GitHub-URL-Konstruktion ab. Die URL-inklusive Cache-Identität bleibt erhalten,
sodass ein Tag-Archiv-Cache-Record mit gleichem Basisnamen die Release-Asset-
Anforderung nicht erfüllen kann.

## Implementierte Source-Controls und verbleibende Validierung

Die implementierte Korrektur bewahrt den geprüften Digest, leitet die exakte
Release-Download-URL ab, weist fehlgebildete/inkonsistente Release-Identitäten
vor dem Download ab und passt den Digest nicht an das Tag-Archiv an oder führt
keinen Fallback auf `/archive/refs/tags` ein.

Abgeschlossener Nachweis:

1. `rtk run /root/git/ModSecurity-conector/.venv/bin/python -B -s -m unittest -v tests.test_runtime_component_cache_contract`
   bestand alle `31` Cache-/Provenance-Tests, einschließlich exaktem
   Release-Asset, Abweisung fehlgebildeter Identitäten, kodierter/reservierter/
   Dot-Segment-Pfade und Nichtwiederverwendung veralteter Tag-Archiv-Caches.
2. Shell-Syntax, AST-Syntax der geänderten Python-Datei, Variablendokumentation
   (`86` Referenzen), die bilinguale Dokumentations-Unit-Suite (`11` Tests)
   sowie `rtk git diff --check` bestanden.
3. Die isolierte Vorbereitung hielt das korrigierte Manifest oben zurück und
   erreichte mit unverändertem ursprünglichem geprüftem SHA-256 die unabhängige
   NGINX-Modul-Build-Grenze.
4. Drei unabhängige Review-Runden schlossen Canonicalization-Gaps für
   kodierte/reservierte Komponenten und Dot-Segmente; das finale Review fand
   keinen verbleibenden konkreten GitHub-URL-Parser-/Canonicalization-Bypass.

Die legitime Kontrolle besteht aus der festen Konfiguration `release-1.31.2` /
`nginx-1.31.2.tar.gz`, die zur exakten `releases/download`-URL aufgelöst wird.
Ein Tag-Archiv-Cache-Record mit gleichem Basisnamen darf nicht für diese
Release-Asset-URL wiederverwendet werden.

Vor Delivery, Verifikation oder Closure weiterhin erforderlich:

1. Eine autorisierte Umgebung mit der fehlenden Voraussetzung
   `ngx_http_modsecurity_module` bereitstellen und die legitime NGINX-Modul- /
   Runtime-Vorbereitung wiederholen.
2. Die nachgelagerten legitimen `FND-CROSS-0001`-Controls wiederholen, sobald
   die native Voraussetzung verfügbar ist.
3. Die breiten Dokumentations-Make-Checks nur mit über einen autorisierten
   Weg verfügbarem Framework-Boundary wiederholen; sie enden derzeit mit `2`
   ausschließlich für bestehende Links in den bewusst uninitialisierten
   Framework-Gitlink.
4. Erst nachdem diese lokalen Gates bestehen, einen separaten Parent-Delivery-
   Candidate erstellen und dessen Exact-Head-Review, CI, SonarQube Cloud und
   Resulting-Master-Evidence einholen.

## Grenzen und Disposition

Dieser Record ist `validated` und `blocked`, nicht fixed, verified, closed
oder risikoakzeptiert. Der ursprüngliche Prüfsummen-Mismatch ist lokal
remediiert, doch der strengere Workflow verbietet ein stärkeres Ergebnis,
solange der Native-/Runtime-Nachweis `blocked_environment` bleibt. Die
Evidence beweist einen fail-closed Mismatch und seine korrigierte
Release-Asset-Grenze, keinen vollständigen Modul-Build oder eine vollständige
Runtime-Matrix. Es erfolgten kein Staging, Commit, Push, Pull Request, Merge,
Framework-Änderung, Parent-Gitlink-Update oder MRTS-Aktion.

Der getrennte Framework-Rekursiv-Provenance-Blocker ist
`FND-FRAMEWORK-0030`. Auch nach beiden Source-Reparaturen bleiben eine
vollständige legitime aktuelle Runtime-Evidence-Kette und ein frischer
Exact-Head-Protected-Delivery-Zyklus für PR #55 erforderlich.

## Historie

- 2026-07-20T16:53:52Z — die isolierte Evidence-Vorbereitung dokumentierte
  den Tag-Archiv/Release-Asset-Digest-Mismatch und stoppte fail-closed.
- 2026-07-20T17:14:09Z — der Parent-only-Defekt wurde dedupliziert und zur
  Remediation angelegt; es erfolgte keine Prüfsummen-Abschwächung oder
  Delivery-Aktion.
- 2026-07-21T01:46:17Z — die lokale Parent-Source-Korrektur und der finale
  Validation-Receipt wurden dokumentiert. Das korrigierte Release-Asset bestand
  die Prüfsummenverifikation und die `31` fokussierten Cache-/Provenance-Tests
  bestanden, doch die Vorbereitung stoppte unabhängig bei
  `missing_nginx_modsecurity_module` (NGINX-Build-Exit `77`). Das Finding ist
  daher `blocked`; keine Delivery wurde versucht.
