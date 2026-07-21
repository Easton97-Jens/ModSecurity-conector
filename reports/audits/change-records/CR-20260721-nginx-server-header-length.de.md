# Change Record: NGINX-Korrektur der Server-Header-Bytelänge

**Sprache:** [English](CR-20260721-nginx-server-header-length.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260721-nginx-server-header-length` |
| Datum (UTC) | `2026-07-21` |
| Basis-Revision | `0e8be81d14ee9a6ae0497b9ab67e58ba2def1fd3` |
| Scope | Nur Parent-Repository; Framework- und MRTS-Source und Gitlinks bleiben unverändert. |
| Zugehöriges Finding | `FND-PARENT-0044` ist als pending canonical EN/DE/JSON-Import retained, weil der lokale `.codex`-Mount read-only ist. |

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

Lokale, ignorierte Evidence hält zusätzlich den vollständigen pending canonical `FND-PARENT-0044`-EN/DE/JSON-Record und den erforderlichen Finding-System-Update-Plan fest; sie ersetzt keine versionierte Source, Tests oder diesen Change Record.

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

## Security-Auswirkung

Die Korrektur stellt die beabsichtigte semantische Länge an der NGINX-zu-libModSecurity-Response-Header-Grenze wieder her. Sie erlaubt einer exakten oder verankerten `RESPONSE_HEADERS:Server`-Policy, den Default-Wert ohne verborgenen Terminator zu vergleichen. Sie erweitert kein Parsing, ändert keine Policy-Auswahl, verändert keinen client-sichtbaren Default-Server-Text und schwächt den korrekt längenbegrenzten Custom-Header-Pfad nicht.

Die statische Source-to-Sink- und Attack-Path-Evidence nennt einen gewöhnlichen Remote-Request als Entry Point, wenn ein Operator den Default-Server-Pfad und eine relevante Response-Header-Policy nutzt. Kein Secret-, Autorisierungs-, Sensitive-Content- oder nachgewiesener client-sichtbarer Integrity-Impact wurde gefunden; die validierte Schwere bleibt `low` / `P3`.

## Runtime-Evidence

Es gibt keine native NGINX/libModSecurity-Runtime-Bestätigung für den Default-Zweig `r->headers_out.server == NULL`. Insbesondere hat kein aufgezeichneter Default-Header-Run bisher eine exakte oder endverankerte Phase-3-Policy-Intervention für beide `server_tokens`-Werte bewiesen. Die C17-Checks kompilieren Connector- und Common-Source gegen eine task-eigene normale NGINX-1.31.2-Konfiguration, führen aber keinen NGINX-Host oder eine libModSecurity-Transaktion aus. Ein proxied Custom-Response-Header würde `h->value.len` statt des fehlerhaften Default-Literalzweigs ausführen und wurde nicht als gleichwertige Evidence ersetzt.

Das retained Final-Validation-Receipt ist `/var/tmp/codex/ModSecurity-conector/runs/20260721T003354Z-nginx-server-header-nul-20260721-34ca8ca8/evidence/nginx-server-header-nul-validation-20260721T005556Z-final.json` mit SHA-256 `01a2cb1a836c08b34537e2bc2aa13949600679d29b255f1600b7e4f8c6bec6da`.

## Bekannte Einschränkungen

Ein task-eigener, signierter und checksum-pinnter NGINX-1.31.2-Source-Baum mit normalen generierten Headern steht für die C17-Compilation zur Verfügung. Dem Host fehlt weiterhin eine kompatible lauffähige NGINX/libModSecurity-Integrationsumgebung. Die ursprüngliche statische Regression und die echten C17-Compiles beweisen die Source-Invariante und die legitimen Custom-/Header-Sink-Controls, aber keine ausgerollte Rule-Entscheidung oder client-sichtbares Response-Verhalten.

Neue Verzeichnis-Allokation unter `.codex/findings` ist in dieser Sitzung verweigert: `mkdir -p .codex/findings/FND-PARENT-0044` lieferte `Read-only file system`. Das kanonische FND-0044-Verzeichnis, Indizes, Backlog, Roadmap und Reconciliation-Report können daher nicht als neuer kanonischer Record synchronisiert werden. Sein vollständiges pending EN/DE/JSON-Import-Paket ist unter dem Task-Run hash-retained.

Die getrennte gzip-deaktivierte C17-Warnung ist separat als `FND-PARENT-0045` (`compiler_warning`, P2, nicht sicherheitsrelevant) triagiert. Sie ändert weder die Server-Header-Korrektur noch ihre normalen GCC-/Clang-Controls und wird bewusst nicht in diesen Change kombiniert.

## Verbleibende Risiken

Nach dem verpflichtenden Security-Workflow bleibt das zugehörige Finding `blocked`, nicht `fixed`, `verified` oder `closed`, bis relevanter nativer Behavioral Proof verfügbar ist. Ein integrationsspezifisches NGINX/libModSecurity-Verhalten könnte bis zur Ausführung von Default-Header-Exact-/End-Anchored-, Custom-Header- und Non-Match-Controls in einer nativen Umgebung unentdeckt bleiben. Es wurde kein Risiko akzeptiert.

Die Source-Korrektur ist bei Record-Autorenschaft lokal. Commit, Push, Draft-PR, Exact-Head-Hosted-Checks, Review, SonarQube Cloud, Merge und Resulting-Master-Scan-Fakten existieren noch nicht und werden hier nicht behauptet.

## Nicht ausgeführte Prüfungen mit Begründung

`make check-nginx-c17-lint` gab zunächst `BLOCKED: missing NGINX headers/source for NGINX connector C checks` und `SKIPPED: nginx C17 compile check blocked in lint environment` aus. Sein Wrapper-Exit `0` belegt keinen C-Compilation-Pass. Für die C17-Evidence wurde dies durch die tatsächlichen `make check-nginx-c17`-Läufe gegen die task-eigene normale NGINX-1.31.2-Source abgelöst, die mit GCC und Clang bestanden.

Der vollständige Lauf `make lint` endete vor den NGINX-Lint-Stufen bei `make check-apache-c17-lint` mit `2`. Ohne lokales APXS forderte der Framework-Helper die All-Component-Runtime-Provisionierung an. Deren NGINX-Pfad lud ein GitHub-Tag-Archiv herunter, während er den für das abweichende nginx.org-Release-Archiv gepinnten Checksum anwandte; der Integrity-Check schlug daher korrekt fail-closed fehl, und Apache/APXS sowie das NGINX-Runtime-Modul blieben nicht verfügbar. Die Framework-Grenze und der Parent-Gitlink liegen außerhalb des Schreib-Scope dieser Remediation, daher wurde kein Framework-Workaround oder Checksum-Weakening vorgenommen.

Native NGINX/libModSecurity-Rule-Verifikation, Sanitizer-Coverage, Hosted-PR-Checks, SonarQube-Cloud-Analyse, Review und Resulting-Master-Revalidierung sind nicht ausgeführt, weil noch kein commiteter oder gepushter PR-Head existiert. Die Repository-Bilingual-/Documentation-Checks liefen nach dem Anlegen dieses Record-Paars und bestanden im task-eigenen Delivery-Clone mit dem exakten Framework-Gitlink. Diese isolierte Framework-Kopie initialisierte oder änderte MRTS nicht.

## Finaler Diff- und Review-Status

Ein unabhängiges fokussiertes Review der zwei Source-/Test-Dateien bestand ohne blockierendes Security- oder Compatibility-Problem. Es bestätigte beide Literal-Korrekturen, den unveränderten Custom-`h->value.len`-Pfad und den erhaltenen expliziten Sink.

Bei Record-Aktualisierung enthält der Task-Delivery-Clone nur die zwei Source-/Test-Edits und dieses EN/DE-Change-Record- plus README-Index-Paar. Er basiert auf `0e8be81d14ee9a6ae0497b9ab67e58ba2def1fd3`; kein Commit, Push, PR, Review, Hosted-Check, Sonar-Ergebnis, Merge oder Master-Scan wird behauptet. Der finale lokale Diff und die echten GCC-/Clang-C17-Checks bestanden. Die vollständigen Bilingual-/Documentation-Checks bestanden im Delivery-Clone; der breite Lauf `make lint` bleibt wegen des getrennten fail-closed Framework-Provisionierungsblockers als nicht bestanden dokumentiert.
