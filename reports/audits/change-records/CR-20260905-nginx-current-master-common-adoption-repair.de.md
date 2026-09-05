# Change Record: NGINX-Current-Master-Common-Adoption-Contract-Reparatur

**Sprache:** [English](CR-20260905-nginx-current-master-common-adoption-repair.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260905-nginx-current-master-common-adoption-repair |
| Datum (UTC) | 2026-09-05 |
| Basis-Revision | b779167ff979aa73cdd9321a829f9c693d943760 |
| Delivery-Status | Lokale Checker-Reparatur auf einem autorisierten fokussierten Branch. Dieser Record behauptet keinen Commit, Push, Pull Request, Ready-for-Review-Vorgang oder Merge. Ein normaler Draft PR ist erst nach frischem Delivery-Preflight und finaler lokaler Evidence autorisiert. |

## Motivation und Problemstellung

Nach dem autorisierten Squash-Merge von PR #356 wurden 14 Resulting-Master-
Workflows auf `b779167ff979aa73cdd9321a829f9c693d943760` terminal: neun waren
erfolgreich, und fünf stoppten an denselben zwei NGINX-Common-Adoption-Checker-
Assertions. Die Apache-Common-Adoption-Assertion bestand im fehlgeschlagenen
Apache-Workflow.

Die zwei Assertions waren veraltete Checker-Shapes und kein Nachweis eines
NGINX-Runtime-Defekts. Der aktive Request-Mapper ist fail-closed, während der
Server-Response-Header-Resolver jetzt an einen begrenzten Common-Wrapper
delegiert, statt den rohen Response-Header-Sink direkt aufzurufen.
`FND-PARENT-1010` bleibt bis zur Exact-Head-Delivery-Evidence dieses
Nachfolgers in Bearbeitung.

## Akzeptanzkriterien

- Der Checker verlangt, dass fehlerhaftes Request-Mapping
  `NGX_HTTP_BAD_REQUEST` zurückgibt, und verlangt die exakte fail-closed-
  Propagierung des Initializers vor Hostname- und Request-Header-Verarbeitung.
- Der Checker verlangt, dass der Server-Resolver seine explizite Länge erhält,
  `ngx_http_modsecurity_add_n_response_header` aufruft und keinen rohen
  `msc_add_n_response_header`-Aufruf enthält.
- Der Checker verlangt, dass der Common-Response-Header-Wrapper bei
  Validierungsfehler vor dem rohen Sink mit `NGX_ERROR` abweist.
- Isolierte Negativ-Controls verwerfen veränderte Mapper-Returns,
  Mapper-Propagierung, Server-Raw-Sink- und Response-Validierungs-Branches.
- Die betroffenen Mapper-, Server-Resolver- und Common-Wrapper-Prädikate
  verwenden eine C-Translation-Phase-normalisierte lexikalische Sicht:
  Trigraph-Konvertierung, Backslash-Newline-Splicing und `%:`-Directive-
  Digraphs erfolgen, bevor Kommentare, Strings, Character-Literale und
  bedingte Branches ausgeschlossen werden. Ein UCN-Escape in einer geprüften
  Code- oder Makro-Source-Grenze wird abgewiesen. Ein inaktiver Branch—einschließlich des
  `#else` des äußeren Include-Guards—kann keinen fail-closed-Branch oder
  Raw-Sink-Marker liefern; nur der verifizierte Primär-Branch des kanonischen
  äußeren Include-Guards des Common-Headers bleibt strukturell erhalten.
- Die reparierten Mapper-, Initializer- und Common-Wrapper-Prädikate verlangen
  jeweils exakt eine direkte Fehler-/Sink-Form und weisen verschachtelten,
  ungeklammerten oder nichtlinearen Kontrollfluss darum herum ab. Dies ist
  eine konservative Static-Contract-Einschränkung und kein Anspruch auf einen
  vollständigen C-Control-Flow-Beweis.
- Der Checker scheitert fail-closed, wenn eine Source-Level-Makro-Directive
  einen geprüften Token ändern oder liefern kann, einen UCN, Token-Pasting oder
  einen Kontrollfluss-Token in ihrer Ersatzliste enthält. Die einzige
  Kontrollfluss-Ausnahme ist die vorhandene funktionsartige `dd*`-Diagnoseform
  mit exakt `do { ... } while (0)` als Ersatz und ohne Kontrollfluss-Token im
  Body. Eine funktionsartige Makroform ist ansonsten nur zulässig, wenn sie
  eine der exakten vorhandenen leeren `dd(...)`- oder PCRE-Allocation-Shim-
  Formen ist. Ein quoted lokales Include wird abgewiesen, wenn es dynamisch,
  pfadunsicher oder nicht auf die gescannte NGINX-, Common- und Profile-Source-
  Menge auflösbar ist. Die explizit modellierte externe `stdio.h`-Ausnahme ist
  nur zulässig, wenn kein lokaler Kandidat sie überschattet. Ein Angle-Bracket-
  Include muss die feste aktuelle External-Header-Allowlist verwenden und
  dieselbe Local-Shadow-Prüfung erfüllen; nichtstandardisierte `#include_next`
  und `#import` werden abgewiesen.
- Der Common-Response-Header-Wrapper besitzt exakt zwei lexikalische
  `return`-Tokens: seinen direkten Validierungsfehler-Return und seinen finalen
  direkten Raw-Sink-Return. Ein früher macro-vermittelter Return oder ein
  unerreichbarer Raw-Sink-Decoy kann den begrenzten Response-Header-Contract
  nicht erfüllen.
- Enthalten sind keine NGINX-C-Runtime-Source-, Framework-, MRTS-, Gitlink-,
  Workflow-, Ruleset-, Branch-Protection-, Required-Check-, Quality-Gate-,
  Exclusion-, Suppression-, Source-Lock-, Provenienz-, PR-#346- oder
  `master`-Änderungen.

## Implementierungsentscheidung und Begründung

Die Reparatur ändert nur
`ci/checks/connectors/nginx/check-nginx-common-adoption.py`. Sie begrenzt die
vorhandenen Source-Checks auf die zwei relevanten C-Funktionen und verlangt
exakte fail-closed Mapper-, Initializer-Propagierungs- und Common-Response-
Header-Validierungs-Branches. Die Source-Sicht normalisiert C-Trigraphs,
Line-Splicing und `%:`-Preprocessor-Digraphs vor dem Maskieren von Kommentaren,
Strings, Character-Literalen und inaktiven Preprocessor-Branches. Eine
kommentar-maskierte Begleitsicht erhält das reale Mapper-Diagnose-Literal,
ohne dass Nicht-Code-Text es liefern kann.

Der Checker erlaubt nur den verifizierten Primär-Branch des kanonischen äußeren
Include-Guards des Common-Headers; dessen `#else` wird wie jeder andere
bedingte Branch maskiert. Er weist UCN-Escapes in der geprüften Code- und
vollständigen Makro-Source-Grenze vor dem Directive-Matching ab und verlangt
jeweils eine direkte Branch-/Call-/Sink-Form, während verschachtelter,
ungeklammerter und nichtlinearer Kontrollfluss abgewiesen wird. Erforderliche
Controls müssen daher unbedingter und strukturell direkter Source-Code sein;
ein künftiges legitimes bedingtes oder Kontrollfluss-Refactoring erfordert ein
bewusstes Contract- und Negativ-Control-Update. Der verbotene direkte rohe
Response-Header-Sink wird weiterhin über allen lexikalischen Code einschließlich
bedingter Branches geprüft.

Der Checker behandelt außerdem die Integrität von Source-Level-Makros und
Includes als Voraussetzungen für beide reparierten Assertions. Er scannt die
lokale NGINX-Source-Menge, Common-C/C++-Header und das aktuelle quoted Include
`connectors/profile_registry.h`; er weist `#undef`, nicht freigegebene oder
kritische Makro-Neudefinitionen, UCNs in der vollständigen Nicht-Kommentar- und
Nicht-Literal-Makro-Source-Sicht, Ersatzlisten mit sicherheitskritischen oder
Kontrollfluss-Tokens sowie Token-Pasting ab. Die einzige erlaubte
Kontrollfluss-Ersatzliste ist die strukturell begrenzte funktionsartige
`dd*`-Diagnoseform `do { ... } while (0)` ohne Kontrollfluss-Token in ihrem
Body. Ein quoted lokales Include wird nur akzeptiert, wenn es ein regulärer
C/C++-Header an einem sicheren Pfad ist, der auf diese Eingabemenge auflösbar
ist. Dynamische Include-Formen werden abgewiesen. Angle-Bracket-Includes
erfordern die feste External-Header-Allowlist und werden abgewiesen, wenn ein
vorhandener lokaler Kandidat nicht auf diese Eingabemenge auflösbar ist. Das
vorhandene quoted `stdio.h` ist nur ohne lokalen Kandidaten an den modellierten
Suchwurzeln eine feste externe Ausnahme. Nichtstandardisierte `#include_next`
und `#import`-Directives werden abgewiesen.

Funktionsartige Makros sind nur für die vorhandene leere `dd(...)`-Form, die
begrenzte `dd*`-Diagnoseform und die zwei exakten PCRE-Allocation-Shims
zulässig. Das weist Parameter-Substitution ab, die sonst einen vom Caller
gelieferten Identifier vor der Validierung in einen rohen Response-Header-Sink
verwandeln könnte.

Für den Common-Response-Header-Wrapper verlangt der Checker außerdem exakt
zwei lexikalische `return`-Tokens: den direkten Validierungsfehler-Return
gefolgt vom terminalen direkten Raw-Sink-Return. Das weist einen frühen
erlaubten Macro-Return, einen parameterisierten macro-vermittelten Raw-Sink-
Return oder einen unerreichbaren Raw-Sink-Decoy ab, statt nur ein späteres
Raw-Sink-Vorkommen zu akzeptieren.

Damit bleibt das aktuelle restriktive C-Verhalten erhalten, statt die
veraltete Warn-only-Mapper-Erwartung oder einen direkten rohen Server-Sink
wiederherzustellen. Unabhängige Read-only-Source-to-Sink-Reviews fanden keinen
aktuellen Runtime-Bypass auf diesen Pfaden. Sie identifizierten auch
aufeinanderfolgende Checker-Control-False-Pass-Möglichkeiten, die jetzt durch
die exakten Branch-Prädikate, Makro-Einschränkungen, Include-Auflösung und
Negativ-Controls abgedeckt sind.

## Geänderte Dateien

- `ci/checks/connectors/nginx/check-nginx-common-adoption.py`
- `tests/test_nginx_common_adoption.py`
- `reports/audits/change-records/CR-20260905-nginx-current-master-common-adoption-repair.md`
- `reports/audits/change-records/CR-20260905-nginx-current-master-common-adoption-repair.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| Pre-Patch `make check-nginx-common-adoption` | Genau die veralteten Mapper-nonfatal- und Server-direct-raw-sink-Assertions auf `b779167ff979aa73cdd9321a829f9c693d943760` reproduziert. |
| Post-Patch `make check-nginx-common-adoption` | Alle 60 NGINX-Common-Adoption-Assertions bestanden auf der aktuellen erweiterten Revision. |
| `python -B -m py_compile ci/checks/connectors/nginx/check-nginx-common-adoption.py tests/test_nginx_common_adoption.py` | Bestanden. |
| Zwei explizite `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -q`-Auswahlen für `tests.test_nginx_common_adoption.NginxCommonAdoptionCheckerTests` | Bestanden: 44 isolierte Checker-Fälle in begrenzten 22/22-Aufrufen—ein legitimer Positivfall und 43 Negativ-Controls. Der One-Shot-Aufruf überschreitet das lokale Befehlszeitlimit. |
| `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -q tests.test_nginx_native_security_contract tests.test_nginx_upstream_security_contract tests.test_nginx_header_iteration_contract tests.test_ci_security_workflows` | Bestanden: 54 Companion-NGINX-Contract-Tests; 98 ausgewählte bestandene Tests aggregiert. |
| Frühere vier isolierte Source-only-Mutations-Fixtures | Jede endete mit `1` genau an ihrem erwarteten geänderten Contract-Label; der positive Hotfix-Worktree-Checker endete mit `0`. Die payload-freie Receipt-SHA-256 lautet `244fad874b3b6fc4e1044caa03908e5ad005262a1d14a2449651a6d5b5677aab`. |
| Isoliertes C-Kommentar-Decoy-Fixture | Beim Pre-Hardening-Checker endete ein fehlerhafter Mapper-Return mit einem synthetischen fail-closed-Block innerhalb eines C-Kommentars mit `0`. Der gehärtete Checker endete mit `1` an `NGINX request mapper validation fails closed before request-header initialization`; eine synthetische kommentierte Signatur vor der realen Funktion blieb abgewiesen. Die payload-freie Receipt-SHA-256 lautet `d4af6ebda9b256030f775d38260e5b0686412939806f062ec7e30c211e75c501` und bleibt mit dem Task-Manifest erhalten. |
| Frühere `tests.test_nginx_common_adoption`-Preprocessor-Receipt | Bestanden: vier isolierte Checker-Runs. Die legitime helper-aware Source bestand; drei `#if 0`-Zwillinge mit fehlerhaftem live Mapper-, Initializer- oder Response-Wrapper-Code scheiterten jeweils am entsprechenden reparierten Contract-Label. |
| Historische finale Translation-/Control-Receipt | Bestanden: 16 isolierte Checker-Fälle—ein legitimer helper-aware Positivfall und 15 Negativ-Controls für gewöhnliche, phase-spliced, Trigraph-, Digraph- und Outer-Guard-Decoys; Mapper-Bindung; verschachtelten/ungeklammerten Kontrollfluss; sowie line-spliced/UCN-Raw-Sinks. Receipt-SHA-256: `d83c042215792b836de7c275f678683a281ac2ad8ec507af590f8dae9f40be13`. |
| Historische finale Makro-Control-Receipt | Bestanden: 24 isolierte Checker-Fälle—ein legitimer helper-aware Positivfall und 23 Negativ-Controls. Receipt-SHA-256: `dd64ddf7217297afc0ded5f215a10e93ecc8fce506adec2ea4b1fd60328cc1b6`. |
| Historische finale Makro-und-Include-Control-Receipt | Bestanden: 29 isolierte Checker-Fälle—ein legitimer helper-aware Positivfall und 28 Negativ-Controls. Receipt-SHA-256: `0c62ddfce3e2e962cdcb167a78c196269d2b374671c84fd8392e97ea8764e968`. |
| Historische finale Makro-und-Include-Control-Receipt mit Angle-Grenze | Bestanden: 31 isolierte Checker-Fälle—ein legitimer helper-aware Positivfall und 30 Negativ-Controls. Receipt-SHA-256: `08ef383d8f861aea50af98dfcf30b3b2b582f46f5d7c186867126aa268c22d14`. |
| Historische finale Makro-und-Include-Control-Receipt mit Directive-Grenze | Bestanden: 32 isolierte Checker-Fälle—ein legitimer helper-aware Positivfall und 31 Negativ-Controls, einschließlich Makro-Neudefinition/-Undefinition, nicht freigegebener Makronamen, Token-Pasting sowie Alternate-Extension-, Traversal-, Out-of-Root-, Makro-expanded-, Local-Shadow-, Unknown-Angle- und `#include_next`-Include-Controls. Receipt-SHA-256: `d8d298beb742f7d00ddd3cc4a73e0d3dd8b5cdd1a8965d755987f5d01a4f296f`. |
| Historische finale Makro-Alias- und Terminal-Return-Control-Receipt | Bestanden: 35 isolierte Checker-Fälle—ein legitimer helper-aware Positivfall und 34 Negativ-Controls, einschließlich `#import`, eines erlaubten Common-Header-Raw-Sink-Alias und eines frühen erlaubten Macro-Returns mit unerreichbarem Raw-Sink-Decoy. Receipt-SHA-256: `2c945c7e01d9c69d8ae0ad8daf17559226859dee13dd491f4ae96e2daecb4192`. |
| Aktuelle finale Function-Macro-Control-Receipt | Bestanden: 44 isolierte Checker-Fälle—ein legitimer helper-aware Positivfall und 43 Negativ-Controls, einschließlich Macro-Early-Return, Kontrollfluss-Capture, UCN-Macro-Name, parameterisiertem Raw-Sink-Return und parameterisiertem Prevalidation-Raw-Sink-Control. Receipt-SHA-256: `43cef8d34b51febb4eb5286a4ff3ba5d899bb33e44f4f0bdacc8623efa4767dc`. |
| `make check-bilingual-docs` und `make check-doc-links` | Durch den nicht initialisierten `modules/ModSecurity-test-Framework`-Gitlink blockiert: vorhandene Repository-Links auf Framework-Dateien fehlen. Kein Befehl meldete einen aufgabeneigenen Change-Record-Linkfehler. Das neue Paar hat in jeder Sprache 12 Pflichtüberschriften und identische Backtick-begrenzte technische Literale. |
| `git diff --check` | Bestanden. |
| Initialer Security-Diff-Scan | Für die vorhergehende Kommentar-Decoy-Revision abgeschlossen: In diesem Snapshot blieb kein reportable Befund. Er bleibt nur als historische Evidence aufbewahrt. |
| Finaler Function-Macro-Security-Diff-Scan | Abgeschlossen am `2026-09-05T10:22:18.683709Z`: Alle sechs aktuellen geänderten Pfade wurden mit vollständiger Abdeckung und null reportable Befunden berücksichtigt. Die SHA-256 des versiegelten Reports lautet `7ff57a88702a922644dc0d3ebca96d3bbbf19e3a0ca9031b656cdf7b9e00d9ae`; dies ist ausschließlich statische Checker-/Test-/Dokumentations-Evidence. |

## Security-Auswirkung

Die Request-Grenze fließt von `ngx_http_request_t` über
`ngx_http_modsecurity_validate_common_request_mapper()` in die Request-
Initialisierung und spätere Request-Header-Verarbeitung. Die Source verlangt,
dass ein Mapper-Fehler vor diesem Header-Pfad stoppt.

Die Response-Header-Grenze fließt von `r->headers_out.server` über
`ngx_http_modsecurity_resolv_header_server()` in
`ngx_http_modsecurity_add_n_response_header()`, dann über
`ngx_http_modsecurity_validate_header()` vor den rohen
`msc_add_n_response_header()`-Sink. Die Reparatur asserted diesen begrenzten
Explizit-Längen-Pfad und den abweisenden Validierungs-Branch.

Die Checker-Integritätsgrenze wendet jetzt die dokumentierte Translation-Phase-
Normalisierung vor dem Maskieren von Nicht-Code-C-Text und bedingten
Preprocessor-Branches an, weist UCN-Escapes in der geprüften Code- und Makro-
Source-Grenze ab und verlangt direkte strukturelle Pfade für diese reparierten
Source-Contracts. Sie verwirft die reproduzierten Kommentar-, inaktiven-
Preprocessor-/Function-Directive-, Kontrollfluss-, Raw-Sink-Schreibweisen-,
Makro-Ersatzlisten-, Macro-Early-Return-, UCN-Macro-Name-, parameterisierten
Raw-Sink-, Quoted-Local-Include-, Unknown-Angle-Include- und
nichtstandardisierten Include-Directive-Decoys, ohne den NGINX-Runtime-Pfad zu
ändern.

Es ändern sich keine C-Runtime-Semantik, Body-/Event-Payload-Verarbeitung,
Remote-Rule-Policy, Filesystem-Verhalten, Netzwerkendpunkte oder Secret-Flows.
Die geprüfte Source ist bereits fail-closed; dies ist eine Static-Contract-
Reparatur, keine behauptete Runtime-Vulnerability-Remediation.

## Runtime-Evidence

Für diese Checker-only-Änderung wurde kein nativer NGINX-Server, Proxy,
Request, Response, Sanitizer oder Hostmatrix gestartet. Kein Request- oder
Response-Body wurde aufbewahrt. Statische Source-to-Sink-Evidence und
isolierte Checker-Mutations-Controls ersetzen keine native Runtime-Validierung.

## Bekannte Einschränkungen

Der Checker ist ein bewusst enger Source-Contract, kein vollständiger C-Parser
und kein Beweis beliebiger Compiler- oder Runtime-Reachability-Semantik. Seine
lexikalische Sicht normalisiert nur die dokumentierten Trigraph-, Line-Splicing-
und `%:`-Directive-Formen, weist UCN-Escapes und unstrukturierten Kontrollfluss
bewusst ab und maskiert bedingte Branches außer dem verifizierten Primär-Branch
des kanonischen äußeren Include-Guards des Common-Headers. Er prüft
Source-Level-Makro-Directives, begrenzt funktionsartige Makroformen, weist
`##`, UCNs und sicherheitskritische/Kontrollfluss-Ersatzlisten-Tokens ab und
prüft quoted lokale Include-Syntax, Pfad, Auflösung und gescannte-Source-
Zugehörigkeit sowie die feste aktuelle Angle-Include-Allowlist. Er wertet aber
externe Compiler-`-D`-Inputs, Expansion innerhalb allowlisteter Third-Party-/
System-Header, nicht modellierte Compiler-Include-Wurzeln, andere Compiler-
Makro-Semantik außerhalb dieser begrenzten lokalen Oberfläche oder native
Runtime-Reachability nicht aus. Ein künftiges legitimes Refactoring kann ein
bewusstes Checker- und Negativ-Control-Update erfordern.

## Verbleibende Risiken

`FND-PARENT-1010` wird nicht durch lokale Evidence geschlossen. Exact-
Successor-Head-Hosted-Checks, SonarQube-Cloud-Analyse, Reviews und jede
Resulting-Master-Evidence bleiben separate Delivery-Pflichten. Die Aufgabe
beansprucht keine vollständige P1–P4-Abnahme oder vollständige native 17×10-
Hostmatrix. PR #346 bleibt ein unabhängiger, unveränderter Draft und muss
getrennt gegen den neuen `master` integriert werden.

## Nicht ausgeführte Prüfungen mit Begründung

Es wurden kein nativer NGINX-Runtime-Replay, keine vollständige P1–P4-Abnahme,
keine vollständige native 17×10-Hostmatrix, keine ASan-, UBSan-, TSan- oder
Leak-Prüfung und keine C-Kompilierung ausgeführt, weil der Delivery-Diff keine
NGINX-C-Runtime-Änderung enthält. Für diesen Successor-Head existieren noch
kein Hosted-Workflow, keine SonarQube-Cloud-Analyse, kein Review, Push oder
Pull Request. Das nicht verfügbare lokale `ruff`-Executable wurde nicht
installiert oder ersetzt.

## Finaler Diff- und Review-Status

In dieser Record-Revision enthält der Worktree nur die Checker-Reparatur, ihren
zielgerichteten Checker-Mutationstest und dieses gekoppelte Traceability-
Update. Unabhängige Read-only-Reviews bestätigten die aktuellen C-Source-to-
Sink-Controls und fanden dann Branch-Binding-, inaktive-Preprocessor-,
Translation-Phase-, Raw-Sink-Schreibweisen-, Kontrollfluss-, Makro-
Ersatzlisten-, Macro-Early-Return-, UCN-Macro-Name-, Function-Macro-Parameter-
Substitution-, Quoted-Local-Include-, Angle-Include- und nichtstandardisierte
Include-Directive-Checker-Bypässe in aufeinanderfolgenden Kandidatenrevisionen.
Die aktuelle lexikalische Control verwirft 43 begrenzte Negativ-Controls; die
44-Fall-fokussierte Suite und die vier Companion-Module (54 Tests) bestanden
in der Repository-virtuellen Umgebung, für 98 ausgewählte bestandene Tests
aggregiert. Die aufgabeneigenen Mutations-Fixtures wurden entfernt, nachdem
payload-freie Receipts aufbewahrt wurden. `git diff --check` bestand; die repositoryweiten
Dokumentationsbefehle sind wegen des fehlenden Framework-Checkouts environment-
blocked, während die Pflichtüberschriften und technischen Literale des neuen
Paars übereinstimmen. Der finale unabhängige Diff-Review fand keinen
reproduzierbaren aktuellen Checker-False-Pass im begrenzten Mapper- oder
Response-Header-Pfad, und der finale Function-Macro-Security-Diff-Scan wurde
mit vollständiger Sechs-Pfad-Abdeckung und null reportable Befunden
abgeschlossen. Commit, normaler Push, Draft-PR-Erstellung, Exact-Head-Hosted-
Checks, SonarQube Cloud und Review-Evidence stehen aus.
