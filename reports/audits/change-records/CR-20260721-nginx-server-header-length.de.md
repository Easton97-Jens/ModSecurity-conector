# Change Record: NGINX-Korrektur der Server-Header-Bytelänge

**Sprache:** [English](CR-20260721-nginx-server-header-length.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260721-nginx-server-header-length` |
| Datum (UTC) | `2026-07-21` |
| Basis-Revision | `0e8be81d14ee9a6ae0497b9ab67e58ba2def1fd3` |
| Scope | Nur Parent-Repository; Framework- und MRTS-Source und Gitlinks bleiben unverändert. |
| Zugehöriges Finding | Bei der Erstellung dieses Records war keine kanonische Finding-ID vergeben; dieser Record hält nur die begrenzte Evidence des statischen Candidates fest. |

## Motivation und Problemstellung

`ngx_http_modsecurity_resolv_header_server()` übergibt den NGINX-Default-`Server`-Wert an libModSecurity, wenn `r->headers_out.server == NULL` ist. Seine zwei connector-eigenen C-Arrays wurden durch die explizitlängige `msc_add_n_response_header()`-API mit bloßem `sizeof(...)` übergeben, was das terminale NUL jedes Literals einschließt. Eine exakte oder endverankerte Phase-3-`RESPONSE_HEADERS:Server`-Policy kann daher ein Byte evaluieren, das nicht Teil des semantischen HTTP-Headerwerts ist, und nicht intervenieren.

Der Candidate wurde statisch als reportable `low` / `P3` validiert. Der Fehler unterscheidet sich von Response-Body-Inspection-Limits: Er ist eine enge Response-Header-Byte-Length-Canonicalization-Grenze.

## Akzeptanzkriterien

- Die `server_tokens`- und nichttokenisierten Default-Server-Literalzweige übergeben `sizeof(...)-1U` als `value.len`; keine bloße Default-`sizeof(...)`-Zuweisung bleibt.
- Der Custom-`r->headers_out.server`-Pfad behält `h->value.len` ohne Subtraktion, `strlen`- oder `ngx_strlen`-Konvertierung.
- Der Resolver behält den expliziten `msc_add_n_response_header(..., value.data, value.len)`-Sink.
- Der fokussierte Source-Contract schlägt vor der Source-Korrektur für die zwei Default-Längen fehl und besteht danach, einschließlich Custom-Header- und Sink-Controls.
- Es erfolgen keine Framework-, MRTS- oder Gitlink-Änderungen und kein Compiler-, Test-, Scanner- oder Quality-Gate-Control wird abgeschwächt.

## Implementierungsentscheidung und Begründung

Nur die zwei Literal-Speicherlängen ziehen ihr terminales Byte ab:

```c
value.len = sizeof(ngx_http_server_full_string) - 1U;
value.len = sizeof(ngx_http_server_string) - 1U;
```

Der vorhandene Custom-Zweig bleibt `value.len = h->value.len;`. NGINX besitzt diese explizite `ngx_str_t`-Länge bereits; eine Subtraktion oder Anwendung von C-String-Semantik dort würde gültige Custom-Werte beschädigen. Auswahl, sichtbare Werte und explizitlängiger API-Sink des Header-Resolvers bleiben unverändert. Die lint-verdrahtete NGINX-Common-Adoption-Prüfung verlangt beide korrigierten Literalzweige, verwirft ihre früheren bloßen Zuweisungen, verlangt die Custom-Length-Kontrolle und prüft den Sink.

## Geänderte Dateien

- `connectors/nginx/src/ngx_http_modsecurity_header_filter.c`
- `ci/checks/connectors/nginx/check-nginx-common-adoption.py`
- `reports/audits/change-records/CR-20260721-nginx-server-header-length.md`
- `reports/audits/change-records/CR-20260721-nginx-server-header-length.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

Dieser Change Record referenziert keinen kanonischen Finding-Record. Der aktuelle lokale `.codex/findings`-Speicher ist read-only, daher wurden keine Allokation und kein Import durchgeführt; diese begrenzte Evidence des statischen Candidates ersetzt weder versionierte Source noch Tests oder diesen Change Record.

## Ausgeführte Befehle

Vor der Source-Korrektur endete der ergänzte Contract mit `1`, wobei genau die zwei Default-Length-Assertions fehlschlugen; seine Custom-Header- und expliziten Sink-Controls bestanden. Nach der Korrektur wurden diese Ergebnisse beobachtet:

```text
rtk run env PYTHONDONTWRITEBYTECODE=1 python3 ci/checks/connectors/nginx/check-nginx-common-adoption.py
rtk run env PYTHONDONTWRITEBYTECODE=1 make check-nginx-common-adoption
rtk run env PYTHONDONTWRITEBYTECODE=1 make check-nginx-c-standard-wiring
rtk run env PYTHONDONTWRITEBYTECODE=1 make check-nginx-c17-lint
rtk env PYTHONDONTWRITEBYTECODE=1 FRAMEWORK_ROOT=/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework CONNECTOR_COMPONENT_CACHE=/var/tmp/codex/ModSecurity-conector/cache/shared BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/runs/20260721T003354Z-nginx-server-header-nul-20260721-34ca8ca8/build/c17-check-gcc NGINX_SOURCE_DIR=/var/tmp/codex/ModSecurity-conector/runs/20260721T003354Z-nginx-server-header-nul-20260721-34ca8ca8/build/nginx-c17/nginx-1.31.2 CC=gcc make check-nginx-c17
rtk env PYTHONDONTWRITEBYTECODE=1 FRAMEWORK_ROOT=/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework CONNECTOR_COMPONENT_CACHE=/var/tmp/codex/ModSecurity-conector/cache/shared BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/runs/20260721T003354Z-nginx-server-header-nul-20260721-34ca8ca8/build/c17-check-clang NGINX_SOURCE_DIR=/var/tmp/codex/ModSecurity-conector/runs/20260721T003354Z-nginx-server-header-nul-20260721-34ca8ca8/build/nginx-c17/nginx-1.31.2 CC=clang make check-nginx-c17
rtk run env PYTHONDONTWRITEBYTECODE=1 make lint
rtk git -C /var/tmp/codex/ModSecurity-conector/runs/20260721T003354Z-nginx-server-header-nul-20260721-34ca8ca8/worktree diff --check
rtk run env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs
rtk run env PYTHONDONTWRITEBYTECODE=1 make check-doc-links
rtk run env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_bilingual_docs
```

Die direkte fokussierte Prüfung bestand alle vorhandenen Assertions plus die vier neuen Default-/Custom-/Sink-Assertions. `make check-nginx-common-adoption` und `make check-nginx-c-standard-wiring` bestanden. `git diff --check` bestand. `make check-nginx-c17-lint` gab zunächst `0` zurück, meldete aber semantisch eine Umgebungsblockade und Skip; dieses Pre-Provisioning-Wrapper-Ergebnis ist unten dokumentiert und zählt nicht als nativer C-Compilation-Pass. Nach einer task-eigenen, signierten und SHA-256-pin-verifizierten NGINX-1.31.2-Source-Bereitstellung und normaler NGINX-Konfiguration bestand das tatsächliche Ziel `make check-nginx-c17` sowohl mit GCC 15.2 als auch mit Clang 21.1 und kompilierte die vollständige NGINX/Common-Source-Liste mit `-std=c17 -Wall -Wextra -Werror`. Der vollständige Parent-Lauf `make lint` endete vor seinen NGINX-Lint-Stufen bei `make check-apache-c17-lint` mit `2`. Die Apache/APXS-Provisionierung rief den All-Component-Runtime-Preparer auf, der bei einem getrennten NGINX-Archiv-SHA-256-Mismatch und fehlenden Runtime-Voraussetzungen fail-closed endete. Dies ist kein bestandener Full-Lint und keine Evidence gegen die fokussierten NGINX-Controls; sein getrennter Provisionierungsblocker ist unten dokumentiert.

`make check-bilingual-docs` und `make check-doc-links` bestanden im Delivery-Clone unter Verwendung einer task-eigenen detached Kopie des exakt auf Master gepinnten Framework-Gitlinks; sein verschachteltes MRTS-Submodule blieb uninitialisiert. Das Change-Record-Paar wurde zusätzlich manuell auf passende erforderliche Überschriften, Identity-Felder, Sprachumschalter, Tabellen und technische Literale geprüft.

Am `2026-07-22` startete die Current-Master-Reconciliation in einem isolierten Delivery-Clone einen Merge von `origin/master` bei `b0cc501d8edeada4709118b91194ab838b6d681e` mit dem ursprünglichen Draft-PR-#73-Inhalt. Nur die bilingualen Change-Record-Indizes hatten Konflikte; die Source- und Checker-Hunks nicht. Die fokussierte Prüfung `rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-nginx-common-adoption` bestand, einschließlich beider Default-Terminal-NUL-Controls, des Custom-Length-Controls und des Explicit-Sink-Controls. `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_bilingual_docs` bestand alle 11 Tests. Der aktuelle Versuch `rtk proxy env BUILD_ROOT=<task-owned-external-build-root> make check-nginx-c17` ist `blocked`: NGINX-Header/Source fehlen, daher gibt sein zugrunde liegendes Script `77` und `make` `2` zurück; dies ist kein aktueller C17-Compilation-Pass.

## Security-Auswirkung

Die Korrektur stellt die beabsichtigte semantische Länge an der NGINX-zu-libModSecurity-Response-Header-Grenze wieder her. Sie erlaubt einer exakten oder verankerten `RESPONSE_HEADERS:Server`-Policy, den Default-Wert ohne verborgenen Terminator zu vergleichen. Sie erweitert kein Parsing, ändert keine Policy-Auswahl, verändert keinen client-sichtbaren Default-Server-Text und schwächt den korrekt längenbegrenzten Custom-Header-Pfad nicht.

Die statische Source-to-Sink- und Attack-Path-Evidence nennt einen gewöhnlichen Remote-Request als Entry Point, wenn ein Operator den Default-Server-Pfad und eine relevante Response-Header-Policy nutzt. Kein Secret-, Autorisierungs-, Sensitive-Content- oder nachgewiesener client-sichtbarer Integrity-Impact wurde gefunden; die validierte Schwere bleibt `low` / `P3`.

## Runtime-Evidence

Es gibt keine native NGINX/libModSecurity-Runtime-Bestätigung für den Default-Zweig `r->headers_out.server == NULL`. Insbesondere hat kein aufgezeichneter Default-Header-Run bisher eine exakte oder endverankerte Phase-3-Policy-Intervention für beide `server_tokens`-Werte bewiesen. Die C17-Checks kompilieren Connector- und Common-Source gegen eine task-eigene normale NGINX-1.31.2-Konfiguration, führen aber keinen NGINX-Host oder eine libModSecurity-Transaktion aus. Ein proxied Custom-Response-Header würde `h->value.len` statt des fehlerhaften Default-Literalzweigs ausführen und wurde nicht als gleichwertige Evidence ersetzt.

Das retained Final-Validation-Receipt ist `/var/tmp/codex/ModSecurity-conector/runs/20260721T003354Z-nginx-server-header-nul-20260721-34ca8ca8/evidence/nginx-server-header-nul-validation-20260721T005556Z-final.json` mit SHA-256 `01a2cb1a836c08b34537e2bc2aa13949600679d29b255f1600b7e4f8c6bec6da`.

## Bekannte Einschränkungen

Ein task-eigener, signierter und checksum-pinnter NGINX-1.31.2-Source-Baum mit normalen generierten Headern steht für die C17-Compilation zur Verfügung. Dem Host fehlt weiterhin eine kompatible lauffähige NGINX/libModSecurity-Integrationsumgebung. Die ursprüngliche statische Regression und die echten C17-Compiles beweisen die Source-Invariante und die legitimen Custom-/Header-Sink-Controls, aber keine ausgerollte Rule-Entscheidung oder client-sichtbares Response-Verhalten.

Neue Verzeichnis-Allokation unter `.codex/findings` ist in dieser Sitzung mit `Read-only file system` verweigert. In diesem Change Record ist keine kanonische Finding-ID vergeben; diese Storage-Einschränkung macht begrenzte statische Evidence nicht zu nativer Behavioral Verification.

Die getrennte gzip-deaktivierte C17-Warnung ist separat als `FND-PARENT-0045` (`compiler_warning`, P2, nicht sicherheitsrelevant) triagiert. Sie ändert weder die Server-Header-Korrektur noch ihre normalen GCC-/Clang-Controls und wird bewusst nicht in diesen Change kombiniert.

## Verbleibende Risiken

Der statische Candidate wird nicht als runtime-verifiziert behauptet; es wurde kein kanonisches Finding alloziert oder geschlossen. Relevanter nativer Behavioral Proof ist weiterhin erforderlich. Ein integrationsspezifisches NGINX/libModSecurity-Verhalten könnte bis zur Ausführung von Default-Header-Exact-/End-Anchored-, Custom-Header- und Non-Match-Controls in einer nativen Umgebung unentdeckt bleiben. Es wurde kein Risiko akzeptiert.

Die Source-Korrektur wurde als Draft PR #73 beim ursprünglichen Head `264f8ca131b5c7371d8be3a7840601255a68ac0e` committet und gepusht. Dieser Head liegt hinter dem aktuellen `master`, daher wird seine frühere Hosted-Evidence nicht wiederverwendet. Die Current-Master-Reconciliation benötigt weiterhin frische Exact-Head-CI, Review, SonarQube Cloud, Merge und Resulting-Master-Verifikation; vor Beobachtung wird nichts davon behauptet.

## Nicht ausgeführte Prüfungen mit Begründung

`make check-nginx-c17-lint` gab zunächst `BLOCKED: missing NGINX headers/source for NGINX connector C checks` und `SKIPPED: nginx C17 compile check blocked in lint environment` aus. Sein Wrapper-Exit `0` belegt keinen C-Compilation-Pass. Für die C17-Evidence wurde dies durch die tatsächlichen `make check-nginx-c17`-Läufe gegen die task-eigene normale NGINX-1.31.2-Source abgelöst, die mit GCC und Clang bestanden.

Der vollständige Lauf `make lint` endete vor den NGINX-Lint-Stufen bei `make check-apache-c17-lint` mit `2`. Ohne lokales APXS forderte der Framework-Helper die All-Component-Runtime-Provisionierung an. Deren NGINX-Pfad lud ein GitHub-Tag-Archiv herunter, während er den für das abweichende nginx.org-Release-Archiv gepinnten Checksum anwandte; der Integrity-Check schlug daher korrekt fail-closed fehl, und Apache/APXS sowie das NGINX-Runtime-Modul blieben nicht verfügbar. Die Framework-Grenze und der Parent-Gitlink liegen außerhalb des Schreib-Scope dieser Remediation, daher wurde kein Framework-Workaround oder Checksum-Weakening vorgenommen.

Native NGINX/libModSecurity-Rule-Verifikation und Sanitizer-Coverage sind für die Current-Master-Reconciliation nicht ausgeführt, weil diese Task-Umgebung keine kompatible lauffähige NGINX/libModSecurity-Integration bereitstellt. Der ursprüngliche Draft PR #73 wurde bei `264f8ca131b5c7371d8be3a7840601255a68ac0e` committet und gepusht; jeder Current-Master-Conflict-Resolution- oder Rebase-Follow-up benötigt einen neuen Exact-Head-Hosted-Zyklus, daher werden keine aktuellen CI-, SonarQube-Cloud-, Review- oder Resulting-Master-Fakten vor Beobachtung behauptet. Die historischen Repository-Bilingual-/Documentation-Checks liefen nach dem Anlegen dieses Record-Paars und bestanden im task-eigenen Delivery-Clone mit dem exakten Framework-Gitlink. Diese isolierte Framework-Kopie initialisierte oder änderte MRTS nicht.

Der aktuelle isolierte Clone hat absichtlich keinen Framework-Working-Tree. Seine Versuche mit `make check-bilingual-docs` und `make check-doc-links` geben beide `2` für repository-weite fehlende Framework-Link-Targets zurück; sie widerlegen weder die fokussierte Heading-, Identity- und Literal-Parität dieses Change-Record-Paars noch werden sie als bestandene Documentation-Checks berichtet.

## Finaler Diff- und Review-Status

Ein unabhängiges fokussiertes Review der zwei Source-/Test-Dateien bestand ohne blockierendes Security- oder Compatibility-Problem. Es bestätigte beide Literal-Korrekturen, den unveränderten Custom-`h->value.len`-Pfad und den erhaltenen expliziten Sink.

Die Current-Master-Reconciliation kombiniert die Source-/Checker-Edits des ursprünglichen PR #73, seine EN/DE-Change-Record- und README-Index-Updates sowie den ausgewählten Current-Master-Inhalt. Der ursprüngliche PR-Head ist `264f8ca131b5c7371d8be3a7840601255a68ac0e`; ein Follow-up-Exact-Head wird separat verifiziert. Der finale lokale Diff und die historischen echten GCC-/Clang-C17-Checks bestanden in ihrem angegebenen Scope. Historische Bilingual-/Documentation-Checks bestanden im Delivery-Clone; der breite Lauf `make lint` bleibt wegen des getrennten fail-closed Framework-Provisionierungsblockers als nicht bestanden dokumentiert.
