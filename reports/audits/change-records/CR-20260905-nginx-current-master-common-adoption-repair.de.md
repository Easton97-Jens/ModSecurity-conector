# Change Record: NGINX-Current-Master-Common-Adoption-Contract-Reparatur

**Sprache:** [English](CR-20260905-nginx-current-master-common-adoption-repair.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260905-nginx-current-master-common-adoption-repair |
| Datum (UTC) | 2026-09-05 |
| Basis-Revision | b779167ff979aa73cdd9321a829f9c693d943760 |
| Delivery-Status | Draft PR #357 besteht auf dem autorisierten fokussierten Branch am initialen Exact-Head `e9ceb86723383c31914f179638f1b7043ea79609`, basierend auf `b779167ff979aa73cdd9321a829f9c693d943760`. Eine lokale uncommittete Successor-Remediation wird verifiziert. Dieser Record behauptet keinen Ready-for-Review-Vorgang, Merge, direkten `master`-Push, PR-#346-Aktion oder Governance-Change. Das Initial-Head-Sonar-Quality-Gate war `OK`, aber fünf offene checker-lokale Issues blockieren die Delivery bis frische Exact-Head-Evidence für den Successor vorliegt. |

## Motivation und Problemstellung

Nach dem autorisierten Squash-Merge von PR #356 wurden 15 Resulting-Master-
Workflows auf `b779167ff979aa73cdd9321a829f9c693d943760` terminal: zehn waren
erfolgreich, und fünf stoppten an denselben zwei NGINX-Common-Adoption-Checker-
Assertions. Die Apache-Common-Adoption-Assertion bestand im fehlgeschlagenen
Apache-Workflow.

Die zwei Assertions waren veraltete Checker-Shapes und kein Nachweis eines
NGINX-Runtime-Defekts. Der aktive Request-Mapper ist fail-closed, während der
Server-Response-Header-Resolver jetzt an einen begrenzten Common-Wrapper
delegiert, statt den rohen Response-Header-Sink direkt aufzurufen.
`FND-PARENT-1010` bleibt bis zur Exact-Head-Delivery-Evidence dieses
Nachfolgers in Bearbeitung.

Während der Sonar-Remediation des Nachfolgers reproduzierte `FND-PARENT-1039`
einen separaten Static-Checker-Control-Bypass: Eine rohe Funktions-Extraktion
konnte an einer Klammer in Kommentar, Literal oder inaktivem Branch vor einem
verbotenen Lifecycle- oder unbeschränkten Response-Body-Append enden. Dies ist
kein Nachweis einer aktuellen NGINX-Runtime-Schwachstelle; der Folgepatch
repariert die gemeinsame Checker-Grenze und wartet weiterhin auf frischen
Successor-Head-Review und Delivery-Evidence.

`FND-PARENT-1042` reproduzierte danach einen separaten Macro-Integritäts-
Bypass in derselben Checker-Grenze. Ein allowgelistetes objektartiges Macro
konnte einen verbotenen Mapper-Lifecycle-, Processing-, Filter-Chain-,
Allokations- oder Phase-4-Pre-Gate-Response-Body-Pfad aliasieren, während die
Assertions weiterhin nur den Alias inspizierten. `FND-PARENT-1040`
reproduzierte außerdem einen gewöhnlichen neu benannten Helper-Aufruf vor
demselben Scope-Gate. Die lokale Reparatur weist daher die vollständige
Mapper-Markermenge und alle fünf erreichbaren Pre-Gate-Body-Pfade in erlaubten
Macro-Ersatzlisten ab und verlangt für den Chain-Buffer-Helper selbst eine
vollständige direkte Gate-only-Form. Dies ist erneut Static-Checker-Evidence,
keine aktuelle NGINX-Runtime-Schwachstelle; Exact-Successor-Head-Review und
Delivery-Evidence bleiben erforderlich.

Der H11-Control-Review reproduzierte danach drei Repräsentations- und
Erreichbarkeitslücken in derselben statischen Grenze. `FND-PARENT-1043` zeigte,
dass die sichtbare Sicht von `c_function` Stringliterale als ausführbare
Phase-4-Scope- und kumulative Body-Limit-Assertions akzeptierte.
`FND-PARENT-1044` zeigte, dass ein unerreichbarer Response-Mapper-Call ein
textuelles Caller-Prädikat erfüllen konnte. `FND-PARENT-1045` zeigte, dass
legaler Whitespace in `ctx -> processed` ein Exact-Member-Literal umging. Der
lokale Successor verwendet `c_checked_function` für ausführbare Contracts,
verlangt direkte Mapper-Caller-Formen und normalisiert geschützten Memberzugriff
in Direct- und Macro-Replacement-Checks. Dies sind Checker-Control-Findings,
keine aktuellen NGINX-Runtime-Schwachstellen; unabhängiger Review, frischer
eingegrenzter Security-Scan und Exact-Successor-Head-Evidence bleiben
erforderlich.

H12 reproduzierte danach weitere Checker-Control-Pfade: Status- oder Return-
Änderungen vor dem ersten genehmigten Header-Guard, Seiteneffekte im erlaubten
`dd(..., ctx)`-Argument, Statusänderungen oder Returns zwischen dem erforderlichen
Header-Mapper-Aufruf und dem Processed-Guard, veränderliche Speicherzugriffe auf
den `const`-Mapper-Kontext, direkte, statische Fallback- oder indirekte Aufruf-
Seiteneffekte in den lokal modellierten Diagnoseformen, ein objektartiges `dd`-
Redirect auf einen mutierenden Header-Helper, ein zusätzlicher bedingter nicht-
inerter `static dd`-Fallback und objektartige PCRE-Allocator-Shim-Replacements,
die typisierte Null-Funktionszeigeraufrufe bilden. Der Successor verlangt nun den
vollständigen genehmigten Header-Prefix und den leeren Mapper-zu-Validation-zu-
Processed-Guard-Korridor, die exakte unveränderliche Mapper-Helper-Form, genau
eine `(void)ctx`-Verwendung in `map_response_from_ctx`, die exakten aktuellen
Diagnose-Makronamen und Parameterlisten, genau zwei nicht-direktive inerte
`dd`-Funktionsdefinitionen sowie die exakten funktionsartigen PCRE-Shim-Formen.
Dies bleiben Checker-Control-Findings und sind keine aktuellen NGINX-Runtime-
Schwachstellen; unabhängiger Review, frischer eingegrenzter Security-Scan und
Exact-Successor-Head-Evidence waren zu diesem Zeitpunkt noch erforderlich.
Das aktuelle Ergebnis des eingegrenzten statischen Scans ist unten festgehalten.

Ein späterer blinder H12-Source-to-Sink-Review reproduzierte vier weitere
Checker-only-Bypässe: das Weglassen des begrenzten Wrapper-Aufrufs in der
Response-Body-Schleife, die Umleitung dieser Schleife über einen neuen rohen
Body-Sink-Helper, das Weglassen des äußeren Response-Header-Collection-Aufrufs
und die Umleitung der Collection über einen neuen rohen Header-Sink-Helper.
Unabhängige Folge-Controls zeigten außerdem, dass sowohl der generische
validierte Wrapper-Aufruf als auch die synthetische Resolver-Schleife entfernt
werden konnten, während der alte Checker weiterhin bestand. Der Successor
verlangt nun den exakten Body-Loop-Call-Korridor, den einzigen rohen Body-Sink
im begrenzten Chunk-Helper, den exakten Collection-Korridor des Header-Filters
vor der Metadatenverarbeitung, die vollständige aktuelle Collection-Traversal- /
Wrapper-Oberfläche und den einzigen rohen Header-Sink im kanonischen validierten
Common-Wrapper. Dies sind ausschließlich Findings an der Static-Checker-
Trust-Boundary: Die aktuellen NGINX-C-Sources behalten alle geprüften Pfade,
und kein mutierter oder produktiver Runtime-Pfad wurde ausgeführt.

Der eine zulässige frische Post-Patch-Source-to-Sink-Review reproduzierte danach
fünf weitere Checker-only-False-Passes in isolierten Source-Kopien: einen
Zwischen-Caller im Body-Filter vor der geprüften Chain, eine Memory-Buffer-Route
zum rohen Chunk-Helper, ein unbedingtes Phase-4-Scope-Prädikat, eine
synthetische `Date`-Resolver-/Table-Route ohne den begrenzten Common-Wrapper
und einen frühen Return im gemeinsamen Iterator für verkettete Header. Eine
anschließende direkte Source-Inspektion zeigte außerdem, dass der begrenzte
Memory-Helper den vom Common-Plan berechneten Wert `allowed` ignorieren und
`len` an den rohen Chunk-Helper weitergeben konnte. Der lokale Checker verlangt
nun für jede dieser Funktionen sowie für die aktuelle synthetische Resolver-
Tabelle die vollständige direkte aktuelle Form. Die Evidence betrifft allein
statische Checker-Akzeptanz/-Abweisung; sie belegt keine aktuelle NGINX-
Runtime-Schwachstelle und führt keinen mutierten Runtime-Pfad aus.

## Akzeptanzkriterien

- Der Checker verlangt, dass fehlerhaftes Request-Mapping
  `NGX_HTTP_BAD_REQUEST` zurückgibt, und verlangt die exakte fail-closed-
  Propagierung des Initializers vor Hostname- und Request-Header-Verarbeitung.
- Der Checker verlangt, dass der Server-Resolver seine explizite Länge erhält,
  `ngx_http_modsecurity_add_n_response_header` aufruft und keinen rohen
  `msc_add_n_response_header`-Aufruf enthält.
- Der Checker verlangt, dass der Common-Response-Header-Wrapper bei
  Validierungsfehler vor dem rohen Sink mit `NGX_ERROR` abweist.
- Der öffentliche Body-Filter behält ausschließlich die geprüfte Prepare- /
  Declined- / Error- / direkte-Chain-Route. Seine Memory-Buffer-Route delegiert
  an den begrenzten Helper; dieser übergibt den vom Common-Plan berechneten Wert
  `allowed` und nicht das Eingabe-`len` an den rohen Chunk-Helper. Das
  Phase-4-Scope-Prädikat, die synthetische Resolver-Tabelle samt `Date`-
  Wrapper und der Iterator für verkettete Header behalten ihre geprüften
  direkten aktuellen Formen.
- `ngx_http_modsecurity_process_response_body_chain()` muss genau einen
  direkten Aufruf des geprüften Chain-Buffer-Wrappers in seinem Scope-/Loop-/
  Error-Korridor behalten; danach folgt unmittelbar die Fehlerpropagierung.
  `msc_append_response_body()` darf in der gescannten NGINX-/Common-Source nur
  im begrenzten Chunk-Helper mit seinen exakten Transaction-/Data-/Byte-
  Argumenten vorkommen.
- Der Header-Filter muss seinen direkten
  `ngx_http_modsecurity_add_response_headers(r, ctx)`-Fehlerpfad nach dem
  Processed-Guard und vor Response-Metadaten behalten. Der Collection-Helper
  muss seine aktuelle synthetische Resolver-Schleife, verkettete Listen-
  Traversierung, den reinen Sanity-Block, den direkten validierten Wrapper- /
  Fehlerpfad und seine Return-Oberfläche behalten; alle zehn geprüften
  `ngx_http_modsecurity_add_n_response_header(ctx, ...)`-Aufrufstellen bleiben
  vorhanden. `msc_add_n_response_header()` darf in der gescannten
  NGINX-/Common-Source nur im kanonischen validierten Common-Wrapper vorkommen.
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
- Jeder verbleibende `c_function`-Auszug wählt seine Grenzen aus derselben
  aktiven Translation-Phase-normalisierten lexikalischen Sicht und gibt für
  legitime Diagnose-Literale die korrespondierende sichtbare Sicht zurück.
  Kommentare, Strings, Character-Literale und nichtkanonische bedingte Branches
  können keinen Auszug beenden oder einen erforderlichen Security-Marker liefern.
- Die reparierten Mapper-, Initializer- und Common-Wrapper-Prädikate verlangen
  jeweils exakt eine direkte Fehler-/Sink-Form und weisen verschachtelten,
  ungeklammerten oder nichtlinearen Kontrollfluss darum herum ab. Dies ist
  eine konservative Static-Contract-Einschränkung und kein Anspruch auf einen
  vollständigen C-Control-Flow-Beweis.
- Der Checker scheitert fail-closed, wenn eine Source-Level-Makro-Directive
  einen geprüften Token definieren, undefinieren, ändern oder liefern kann,
  einen UCN, Token-Pasting oder einen Kontrollfluss-Token in ihrer Ersatzliste
  enthält. Die einzige Kontrollfluss-Ausnahme ist eine exakte aktuelle
  funktionsartige Diagnose-Makroform mit exakt ihrer Parameterliste: ein leeres
  oder dreifach-`fprintf`-variadisches `dd(...)`-Body oder ein geprüftes
  `dd_check_*(r)`-Ternär- bzw. `(void)(r)`-Body. Genau zwei gesamte
  nicht-direktive `dd`-Funktionsdefinitionen müssen zur inerten nicht-
  variadischen Fallback-Form passen. Eine PCRE-Shim ist nur als exakte
  `ngx_http_modsecurity_pcre_malloc_init(x)`/`NULL`- bzw.
  `ngx_http_modsecurity_pcre_malloc_done(x)`/`(void)x`-funktionsartige Form
  zulässig. Ein quoted lokales Include wird abgewiesen, wenn es dynamisch,
  pfadunsicher oder nicht auf die gescannte NGINX-, Common- und Profile-Source-
  Menge auflösbar ist. Die explizit modellierte externe `stdio.h`-Ausnahme ist
  nur zulässig, wenn kein lokaler Kandidat sie überschattet. Ein Angle-Bracket-
  Include muss die feste aktuelle External-Header-Allowlist verwenden und
  dieselbe Local-Shadow-Prüfung erfüllen; nichtstandardisierte `#include_next`
  und `#import` werden abgewiesen.
- Die Response-Mapper-All-Branch-Forbidden-Markermenge und alle fünf
  erreichbaren Pre-Gate-Chain-Buffer-Response-Body-Pfade bilden eine gemeinsame
  Quelle für den Matcher erlaubter Macro-Ersatzlisten. Jedes allowgelistete
  objektartige Replacement mit `common_response_validated`, einem verbotenen
  `ctx`-State-Marker, einem verbotenen Processing-/Filter-/Allokations-Marker
  oder einem Body-Pfad wird abgewiesen. Eine terminale geschützte Definition
  weist auch einen Kettenalias ab; harmlose objektartige Konstanten bleiben
  zulässig.
- Der Chain-Buffer-Helper selbst muss die vollständige direkte Gate-only-Form
  treffen: seinen eindeutigen `phase4_in_scope == 0`-`NGX_OK`-Return gefolgt
  von dem einen genehmigten
  `ngx_http_modsecurity_append_response_body_buffer`-Return. Ein früherer
  direkter, Helper-, Macro-Helper-, indirekter, statusändernder oder bedingter
  Pfad scheitert fail-closed, statt sich auf einen partiellen Call-Graph zu
  verlassen.
- Der Common-Response-Header-Wrapper besitzt exakt zwei lexikalische
  `return`-Tokens: seinen direkten Validierungsfehler-Return und seinen finalen
  direkten Raw-Sink-Return. Ein früher macro-vermittelter Return oder ein
  unerreichbarer Raw-Sink-Decoy kann den begrenzten Response-Header-Contract
  nicht erfüllen.
- Phase-4-Scope-, Response-Body-Planner-/Counter- und Direct-Caller-Controls
  verwenden aktive ausführbare Source statt eines sichtbaren lexikalischen
  Slice, sodass Strings, Kommentare und maskierte Branches keine semantische
  Anweisung liefern können.
- Die Body- und Header-Response-Mapper-Caller müssen ihre geprüfte direkte
  Validation-Assignment-/Guard-/Call-Form auf Top-Level-Tiefe treffen; ein
  unerreichbarer, bedingter, verschachtelter oder ungeklammerter Call kann den
  Contract nicht erfüllen. Die Header-Form besitzt einen deklarations-only
  Prefix, eine direkte Kontextakquisition, den einen geprüften Diagnoseaufruf,
  nur Null-/Interventions-Guards und Returns vor dem Mapping sowie keinen
  ausführbaren oder Präprozessorinhalt vom Mapper über
  `common_response_validated` bis zum Processed-Guard; die eine direkte
  Processed-Zuweisung folgt diesem Guard.
- Verbotene Response-Mapper-`ctx`-Member werden mit legalem Whitespace um `->`
  in aktiver direkter Source und erlaubten Macro-Replacements erkannt;
  objektartige Aliasse geschützter Memberkomponenten werden abgewiesen, ohne
  die vorhandenen begrenzten Diagnostic- und PCRE-Macro-Ausnahmen zu schwächen.
- Der Response-Mapper-Helper muss seine vollständige normalisierte unveränderliche
  Mapping-und-Warning-Form behalten. `map_response_from_ctx` darf genau seine
  eine `(void)ctx`-Verwendung behalten; direkte, verschachtelt gecastete,
  indexierte, Member-, Makro- oder sonstige indirekte Aufrufsyntax darf keine
  dieser Grenzen erweitern.
- Enthalten sind keine NGINX-C-Runtime-Source-, Framework-, MRTS-, Gitlink-,
  Workflow-, Ruleset-, Branch-Protection-, Required-Check-, Quality-Gate-,
  Exclusion-, Suppression-, Source-Lock-, Provenienz-, PR-#346- oder
  `master`-Änderungen.

## Implementierungsentscheidung und Begründung

Die Implementierungslogik ändert nur
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

Die verbleibenden `c_function`-Consumer verwenden jetzt dieselbe aktive
lexikalische Auswahl für Brace-Bounds und geben den passenden sichtbaren Slice
zurück. Damit bleiben reale Diagnostiken für die bestehenden Source-Assertions
verfügbar, aber Kommentar, Literal oder inaktiver Branch können keinen späteren
Lifecycle-Token oder unbeschränkten Response-Body-Append verbergen. Die
Änderung deckt den gemeinsamen Extraktionshelfer statt einzelner Contract-
Ausnahmen ab.

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

Die Macro-Grenze verwendet jetzt außerdem das vollständige Mapper-Marker-Tupel
und alle fünf erreichbaren Pre-Gate-Chain-Buffer-Body-Pfade: Buffer, Limited,
File, Chunk und Raw Append. Damit kann ein ansonsten erlaubtes objektartiges
Macro keinen Mapper-Lifecycle-/State-/Processing-/Filter-/Allokations-Marker
oder einen Body-Pfad vor dem Source-Contract verbergen. Der Matcher sieht eine
terminale geschützte Definition in einer lokalen Aliaskette, modelliert aber
keine externen Compiler-Definitionen oder beliebige Third-Party-Header-
Expansion.

Der Chain-Buffer-Helper ist unabhängig auf seine vollständige normalisierte
direkte Gate-only-Form beschränkt. Seine einzigen ausführbaren Ergebnisse sind
der `phase4_in_scope`-`NGX_OK`-Return und der genehmigte direkte begrenzte
Buffer-Return; jeder neue Pre-Gate-Helper, Macro-Helper, indirekte Aufruf,
Statusmutation oder bedingte Branch scheitert am Source-Contract, ohne eine
partielle Call-Graph-Auflösung zu versuchen.

Der Caller- und Sink-Beweis erstreckt sich nun auf die geprüften
Source-to-Sink-Kanten. Die Body-Verarbeitungsschleife muss ihren direkten
begrenzten Wrapper-Aufruf im exakten Scope-/Assignment-/Loop-/Error-Korridor
ausführen, während der rohe Body-Append nur im begrenzten Chunk-Helper zulässig
ist. Der Header-Filter muss seinen einen Collection-Aufruf zwischen Processed-
Guard und Response-Metadaten ausführen. Der Collection-Helper ist auf seine
aktuellen synthetischen und verketteten Traversierungen, den optionalen reinen
Sanity-Block, Fehler-Returns und die validierte Wrapper-Oberfläche begrenzt;
der rohe Response-Header-Sink ist nur im kanonischen Common-Wrapper zulässig.
Diese absichtlich exakten lexikalischen Contracts weisen einen künftigen
alternativen Helper, einen ungenutzten sicheren Decoy oder einen entfernten
Collection-Pfad ab, statt einen Whole-Program-C-Call-Graph zu modellieren.

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

Für H11-ausführbare Contract-Checks liefert `c_checked_function` die aktive
non-code-maskierte Funktionssicht; `c_function` bleibt auf den passenden
sichtbaren Slice für Diagnostic-Literale beschränkt. Die Response-Mapper-
Caller-Contracts verlangen ihre vollständige direkte Top-Level-Form und weisen
unstrukturierten Kontrollfluss um diese Form ab. Die gemeinsamen Forbidden-
Member-Patterns erkennen legalen Spacing um `->`, geklammertes `ctx` und
`(*ctx).member`-Formen in aktiver Source und erlaubten Macro-Replacements.
Objektartige Macro-Komponenten, die einen geschützten Memberzugriff
rekonstruieren würden, werden abgewiesen; die vorhandenen strukturell sicheren
Diagnostic- und PCRE-Function-like-Macros bleiben begrenzte Ausnahmen. Dies ist
ein konservativer lexikalischer Source-Contract, kein vollständiger C-Parser-
oder Compiler-Preprocessor-Beweis.

Damit bleibt das aktuelle restriktive C-Verhalten erhalten, statt die
veraltete Warn-only-Mapper-Erwartung oder einen direkten rohen Server-Sink
wiederherzustellen. Unabhängige Read-only-Source-to-Sink-Reviews fanden keinen
Source-Level-Bypass auf den aktuell geprüften Pfaden; keine native Runtime wurde
ausgeführt. Sie identifizierten auch
aufeinanderfolgende Checker-Control-False-Pass-Möglichkeiten, die jetzt durch
die exakten Branch-Prädikate, Makro-Einschränkungen, Include-Auflösung und
Negativ-Controls abgedeckt sind.

## Geänderte Dateien

Initiales Draft-PR-#357-Dateiset (sechs getrackte Pfade):

- `ci/checks/connectors/nginx/check-nginx-common-adoption.py`
- `tests/test_nginx_common_adoption.py`
- `reports/audits/change-records/CR-20260905-nginx-current-master-common-adoption-repair.md`
- `reports/audits/change-records/CR-20260905-nginx-current-master-common-adoption-repair.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

Aktueller uncommitteter Successor-Delta (vier veränderte Pfade):

- `ci/checks/connectors/nginx/check-nginx-common-adoption.py`
- `tests/test_nginx_common_adoption.py`
- `reports/audits/change-records/CR-20260905-nginx-current-master-common-adoption-repair.md`
- `reports/audits/change-records/CR-20260905-nginx-current-master-common-adoption-repair.de.md`

## Ausgeführte Befehle

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| Pre-Patch `make check-nginx-common-adoption` | Genau die veralteten Mapper-nonfatal- und Server-direct-raw-sink-Assertions auf `b779167ff979aa73cdd9321a829f9c693d943760` reproduziert. |
| Früheres Post-Patch `make check-nginx-common-adoption` | Alle 61 NGINX-Common-Adoption-Assertions bestanden auf dieser historischen Revision. |
| FND-PARENT-1039-Pre-Fix-Raw-Extraction-Controls | Vier isolierte Temporary-Repository-Controls scheiterten jeweils erwartet, weil der damalige Checker mit null endete: Kommentar- und String-Klammern verbargen einen verbotenen Response-Mapper-Lifecycle-Aufruf, während Kommentar- und `#if 0`-Klammern einen direkten Full-Buffer-Response-Body-Append verbargen. Payload-freie Receipt-SHA-256: `966aebb8a3b62777fd9c2c198c285bdd1a6f523d084a39f27f9bf96735757ffa`. |
| FND-PARENT-1039-Successor-Lexical-Extraction-Controls | Bestanden: Alle vier zuvor umgehbaren Mutationen werden abgewiesen, nachdem Bounds aus der aktiven lexikalischen Sicht gewählt werden, und das native Checker-Target besteht weiterhin alle 61 Assertions. |
| `python -B -m py_compile ci/checks/connectors/nginx/check-nginx-common-adoption.py tests/test_nginx_common_adoption.py` | Bestanden. |
| Vor-H11 `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -q tests.test_nginx_common_adoption` | Bestanden: 56 isolierte Checker-Tests in `96.176s`, einschließlich der direkten Gate-only-Wrapper- und Macro-Replacement-Regressionen. |
| H11-fokussierte Literal-/Caller-/Member-/Macro-Controls | Bestanden: die ersten sechs fokussierten Mutationsmethoden in `60.382s`, danach die Macro-Component-Alias-Methode in `2.629s`. |
| Beobachteter H11 `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -q tests.test_nginx_common_adoption` | Bestanden: 63 isolierte Checker-Tests in `132.067s`, einschließlich jeder H11-Literal-only-, unerreichbarer-Caller-, Member-Spacing- und Macro-Component-Regression. |
| Frühere H12-fokussierte Caller-/Member-Controls | Bestanden: vier fokussierte Testmethoden in `19.294s`, die Präprozessor- oder strukturierte frühe Mapper-Returns und indexierte/dereferenzierte geschützte Memberformen abweisen. |
| Früherer H12 `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -q tests.test_nginx_common_adoption` | Bestanden: 65 isolierte Checker-Tests in `149.256s`. |
| FND-PARENT-1040/-1042-fokussierte Direct-Function- und Macro-Auswahl | Bestanden in `20.523s`: fünf Testmethoden weisen alle fünf direkten Pre-Gate-Pfade, Response-Body-/harmless-/object-macro-Helper-Aufrufe, einen active-conditional Direct-Append und Objektaliase aller fünf Pfade ab; ein harmloser Macro-Control bleibt zulässig. Die payload-freie Pre-Fix-Receipt-SHA-256 lautet `53edc252ab3ab4893501ab93b4b71f4f6f29d08b8bb3c9542c8ad3e2ee403f6b`; das aufgabeneigene Fixture wurde entfernt. |
| Vor-H11 `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -q tests.test_nginx_native_security_contract tests.test_nginx_upstream_security_contract tests.test_nginx_header_iteration_contract tests.test_ci_security_workflows` | Bestanden: 54 Companion-NGINX-Contract-Tests in `2.139s`; 110 ausgewählte bestandene Tests aggregiert. |
| Beobachteter H11 `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -q tests.test_nginx_native_security_contract tests.test_nginx_upstream_security_contract tests.test_nginx_header_iteration_contract tests.test_ci_security_workflows` | Bestanden: 54 Companion-NGINX-Contract-Tests in `2.972s`; 117 ausgewählte bestandene Tests aggregiert mit der H11-fokussierten Suite. |
| Früherer H12 `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -q tests.test_nginx_native_security_contract tests.test_nginx_upstream_security_contract tests.test_nginx_header_iteration_contract tests.test_ci_security_workflows` | Bestanden: 54 Companion-NGINX-Contract-Tests in `2.696s`; 119 ausgewählte bestandene Tests aggregiert mit dieser früheren fokussierten Suite. |
| Aktuelle Fünf-Fall-Auswahl für Makro-Rebinding-Regressionen | Bestanden in `4.768s`: Mutationen für geprüften Mapper, Request-Validator, Response-Validator, `NGX_HTTP_BAD_REQUEST` und token-gepasteten Raw-Sink werden jeweils abgewiesen. |
| Frühere vier isolierte Source-only-Mutations-Fixtures | Jede endete mit `1` genau an ihrem erwarteten geänderten Contract-Label; der positive Hotfix-Worktree-Checker endete mit `0`. Die payload-freie Receipt-SHA-256 lautet `244fad874b3b6fc4e1044caa03908e5ad005262a1d14a2449651a6d5b5677aab`. |
| Isoliertes C-Kommentar-Decoy-Fixture | Beim Pre-Hardening-Checker endete ein fehlerhafter Mapper-Return mit einem synthetischen fail-closed-Block innerhalb eines C-Kommentars mit `0`. Der gehärtete Checker endete mit `1` an `NGINX request mapper validation fails closed before request-header initialization`; eine synthetische kommentierte Signatur vor der realen Funktion blieb abgewiesen. Die payload-freie Receipt-SHA-256 lautet `d4af6ebda9b256030f775d38260e5b0686412939806f062ec7e30c211e75c501` und bleibt mit dem Task-Manifest erhalten. |
| Frühere `tests.test_nginx_common_adoption`-Preprocessor-Receipt | Bestanden: vier isolierte Checker-Runs. Die legitime helper-aware Source bestand; drei `#if 0`-Zwillinge mit fehlerhaftem live Mapper-, Initializer- oder Response-Wrapper-Code scheiterten jeweils am entsprechenden reparierten Contract-Label. |
| Historische finale Translation-/Control-Receipt | Bestanden: 16 isolierte Checker-Fälle—ein legitimer helper-aware Positivfall und 15 Negativ-Controls für gewöhnliche, phase-spliced, Trigraph-, Digraph- und Outer-Guard-Decoys; Mapper-Bindung; verschachtelten/ungeklammerten Kontrollfluss; sowie line-spliced/UCN-Raw-Sinks. Receipt-SHA-256: `d83c042215792b836de7c275f678683a281ac2ad8ec507af590f8dae9f40be13`. |
| Historische finale Makro-Control-Receipt | Bestanden: 24 isolierte Checker-Fälle—ein legitimer helper-aware Positivfall und 23 Negativ-Controls. Receipt-SHA-256: `dd64ddf7217297afc0ded5f215a10e93ecc8fce506adec2ea4b1fd60328cc1b6`. |
| Historische finale Makro-und-Include-Control-Receipt | Bestanden: 29 isolierte Checker-Fälle—ein legitimer helper-aware Positivfall und 28 Negativ-Controls. Receipt-SHA-256: `0c62ddfce3e2e962cdcb167a78c196269d2b374671c84fd8392e97ea8764e968`. |
| Historische finale Makro-und-Include-Control-Receipt mit Angle-Grenze | Bestanden: 31 isolierte Checker-Fälle—ein legitimer helper-aware Positivfall und 30 Negativ-Controls. Receipt-SHA-256: `08ef383d8f861aea50af98dfcf30b3b2b582f46f5d7c186867126aa268c22d14`. |
| Historische finale Makro-und-Include-Control-Receipt mit Directive-Grenze | Bestanden: 32 isolierte Checker-Fälle—ein legitimer helper-aware Positivfall und 31 Negativ-Controls, einschließlich Makro-Neudefinition/-Undefinition, nicht freigegebener Makronamen, Token-Pasting sowie Alternate-Extension-, Traversal-, Out-of-Root-, Makro-expanded-, Local-Shadow-, Unknown-Angle- und `#include_next`-Include-Controls. Receipt-SHA-256: `d8d298beb742f7d00ddd3cc4a73e0d3dd8b5cdd1a8965d755987f5d01a4f296f`. |
| Historische finale Makro-Alias- und Terminal-Return-Control-Receipt | Bestanden: 35 isolierte Checker-Fälle—ein legitimer helper-aware Positivfall und 34 Negativ-Controls, einschließlich `#import`, eines erlaubten Common-Header-Raw-Sink-Alias und eines frühen erlaubten Macro-Returns mit unerreichbarem Raw-Sink-Decoy. Receipt-SHA-256: `2c945c7e01d9c69d8ae0ad8daf17559226859dee13dd491f4ae96e2daecb4192`. |
| Initiale Successor-Function-Macro-Control-Receipt | Bestanden: 44 isolierte Checker-Fälle—ein legitimer helper-aware Positivfall und 43 Negativ-Controls, einschließlich Macro-Early-Return, Kontrollfluss-Capture, UCN-Macro-Name, parameterisiertem Raw-Sink-Return und parameterisiertem Prevalidation-Raw-Sink-Control. Receipt-SHA-256: `43cef8d34b51febb4eb5286a4ff3ba5d899bb33e44f4f0bdacc8623efa4767dc`. |
| `make check-bilingual-docs` und `make check-doc-links` | Durch den nicht initialisierten `modules/ModSecurity-test-Framework`-Gitlink blockiert: vorhandene Repository-Links auf Framework-Dateien fehlen. An diesem historischen Kontrollpunkt meldete kein Befehl einen aufgabeneigenen Change-Record-Linkfehler. Das Paar hat in jeder Sprache 13 Pflichtüberschriften und identische Backtick-begrenzte technische Literale. |
| `git diff --check` | Bestanden. |
| Initialer Security-Diff-Scan | Für die vorhergehende Kommentar-Decoy-Revision abgeschlossen: In diesem Snapshot blieb kein reportable Befund. Er bleibt nur als historische Evidence aufbewahrt. |
| Finaler Function-Macro-Security-Diff-Scan | Abgeschlossen am `2026-09-05T10:22:18.683709Z`: Der vorherige Sechs-Pfad-Snapshot hatte vollständige Abdeckung und null reportable Befunde. Seine SHA-256 lautet `7ff57a88702a922644dc0d3ebca96d3bbbf19e3a0ca9031b656cdf7b9e00d9ae`; er deckt den aktuellen FND-PARENT-1040/-1042-Successor-Scope nicht ab, für den ein frischer finaler Scan ein Delivery-Gate ist. |
| Früheres H12 `python3 -m py_compile ci/checks/connectors/nginx/check-nginx-common-adoption.py tests/test_nginx_common_adoption.py` | Bestanden. |
| Frühere H12 gezielte Diagnose-/Indirection-Controls | Bestanden: `test_diagnostic_macro_side_effect_is_rejected` und `test_indirect_calls_are_rejected` in `10.500s`; direkte, nicht aufrufende, verschachtelt gecastete, indexierte und Member-Formen wurden isoliert abgewiesen. |
| Früherer H12 `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_nginx_common_adoption` | Bestanden: 71 isolierte Checker-Tests in `178.460s`. |
| Frühere H12-Companion-Suite | Bestanden: 54 Companion-Tests in `2.092s`; 125 ausgewählte Tests bestanden aggregiert. |
| Aktuelles H12 objektartiges `dd`-Pre-Fix-Control | Erwartungsgemäß fehlgeschlagen in `4.558s`: der kopierte Checker akzeptierte den objektartigen Diagnose-Redirect. |
| Aktuelles H12 bedingter Static-Fallback-/objektartiger PCRE-Pre-Fix-Control | Erwartungsgemäß fehlgeschlagen in `4.916s`: drei kopierte Checker-Runs wurden akzeptiert. |
| Aktuelle H12 isolierte Syntax-Harnesses | `cc -std=c11 -Wall -Wextra -Werror -fsyntax-only` bestand für den objektartigen `dd`-Redirect sowie die bedingte Static-Fallback- und typisierten PCRE-Formen; die Harnesses wurden nicht ausgeführt. |
| Aktuelles H12 `python3 -m py_compile ci/checks/connectors/nginx/check-nginx-common-adoption.py tests/test_nginx_common_adoption.py` | Bestanden. |
| Aktuelle H12 fokussierte Diagnose-/Fallback-/PCRE-Controls | Bestanden: vier fokussierte Methoden in `10.020s`; alle kopierten Mutationen wurden abgewiesen. |
| Aktueller H12 `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_nginx_common_adoption` | Bestanden: 73 isolierte Checker-Tests in `178.357s`. |
| Aktuelle H12-Companion-Suite | Bestanden: 54 Companion-Tests in `2.123s`; 127 ausgewählte Tests bestanden aggregiert. |
| Aktuelles H12 `make check-nginx-common-adoption` | Bestanden: alle 62 NGINX-Common-Adoption-Assertions. |
| Aktuelle H12 Caller-/Raw-Sink-Pre-Fix-Controls | Unabhängig reproduziert: Entfernen des Body-Loop-Wrappers, Entfernen des Header-Collection-Aufrufs, Umleitung der Schleife über einen rohen Body-Helper und Umleitung der Collection über einen rohen Header-Helper ließen den damaligen kopierten Checker mit `0` enden; alle 62 Assertions meldeten `PASS`. Die kopierten Sources sind begrenzte task-owned Fixtures; keine NGINX-Runtime wurde gebaut oder ausgeführt. |
| Aktuelle H12 Collection-Wrapper-/Traversal-Pre-Fix-Controls | Jeder erwartete Reject-Test schlug fehl, weil der damalige kopierte Checker `0` zurückgab: generisches Validated-Wrapper-Entfernen in `2.304s` und Entfernen der synthetischen Resolver-Schleife in `2.205s`. |
| Aktuelle H12 Caller-/Sink-fokussierte Controls | Bestanden: sechs fokussierte Mutationsmethoden in `13.189s`; alle Body-Loop-, Raw-Body-, Outer-Collection-, Raw-Header-, Generic-Wrapper- und Synthetic-Traversal-Mutationen wurden abgewiesen. |
| Aktuelle H12 `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_nginx_common_adoption` | Bestanden: 79 isolierte Checker-Tests in `249.299s`. |
| Aktuelle H12 Companion-Suite | Bestanden: 54 Companion-Tests in `2.090s`; 133 ausgewählte Tests aggregiert mit der aktuellen fokussierten Suite bestanden. |
| Aktuelle H12 `make check-nginx-common-adoption` nach Caller-/Sink-Reparatur | Bestanden: alle 68 NGINX-Common-Adoption-Assertions. |

| Frischer Post-Patch-Source-to-Sink-Review | Validierte fünf weitere Static-Checker-False-Passes in isolierten Source-Kopien: einen Body-Filter-Zwischen-Caller, eine Memory-Buffer-Route zum rohen Chunk, ein unbedingtes Phase-4-Scope-Prädikat, eine synthetische `Date`-Resolver-/Table-Route und einen frühen Return im Iterator für verkettete Header. Der Review erhebt keine Runtime-Behauptung. |
| Post-Review-Limited-Helper-Pre-Fix-Control | Reproduziert: Das Ersetzen des geplanten `allowed` durch `len` in `ngx_http_modsecurity_append_limited_response_body()` ließ den kopierten Checker mit `0` enden; die neue Regression schlug daher vor dem Hinzufügen des Contracts erwartungsgemäß fehl. |
| Aktuelle fokussierte Caller-/Sink-/Helper-Controls | Bestanden: 11 zielgerichtete Mutationsmethoden in `26.271s`, einschließlich der fünf Review-Kandidaten und der Bounded-Allowance-Regression. |
| Aktuelle vollständige `tests.test_nginx_common_adoption`-Suite | Bestanden: 90 isolierte Checker-Mutationstests in `307.948s`; der begrenzte task-owned Prozess endete mit `0`. |
| Aktuelle Companion-Suite | Bestanden: 54 Companion-NGINX-Contract-Tests in `2.126s`; 144 ausgewählte Static-Contract-Tests bestanden aggregiert mit der aktuellen vollständigen Suite. |
| Aktuelles `make check-nginx-common-adoption` und `py_compile` | Bestanden: alle 74 aktuellen NGINX-Common-Adoption-Assertions und die Python-Syntaxvalidierung für Checker und fokussiertes Testmodul. |
| Eingegrenzter H12-Post-Patch-Security-Diff-Scan | Abgeschlossen am `2026-09-05T19:43:13Z`: Alle vier abgeglichenen lokalen geänderten Pfade wurden mit vollständiger statischer Abdeckung geprüft. Zehn aufbewahrte Checker-Integritätskandidaten aus kopierten Sources wurden durch die aktuellen exakten Contracts abgewiesen; null reportable aktuelle Produktbefunde blieben übrig. Versiegelte Report-SHA-256: `7c86a8a875c6636a22ba5c1b2b080eb6a89ca39190d345585e84a160b693e04b`. Dies ist ausschließlich statische Checker-/Test-/Traceability-Evidence; die aktuelle Vortex-/Sonar-Anfrage bleibt mit HTTP 403 blockiert, und es wird weder ein nativer Runtime- noch ein Delivery-Resultat behauptet. |

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

Der geprüfte Response-Body-Pfad fließt von jedem `ngx_chain_t`-Element in
`ngx_http_modsecurity_process_response_body_chain()` über den Phase-4-Scope-
Gate-Wrapper, die begrenzte Memory-/File-/Planner-Kette und den einzigen rohen
`msc_append_response_body()`-Aufruf im begrenzten Chunk-Helper. Der geprüfte
Response-Header-Pfad fließt vom Header-Filter über
`ngx_http_modsecurity_add_response_headers()`, beide synthetischen und
verketteten Header-Traversierungen, den validierten Common-Wrapper und den
einzigen rohen `msc_add_n_response_header()`-Aufruf. Die neuen Contracts binden
diese aktuellen Caller- und Sink-Kanten, damit ein ungenutzter sicherer Helper
allein einen geänderten Source-Pfad nicht konform erscheinen lässt.

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

Der FND-PARENT-1039-Fix erweitert dieselbe Grenze auf jeden verbleibenden
rohen Funktionsauszug: Aktiver lexikalischer Code liefert die Brace-Struktur,
während die passende sichtbare Sicht legitime Diagnose-Literale bewahrt. Die
vier reproduzierten Kommentar-, String- und Inactive-Branch-Decoys können daher
weder die Response-Mapper-Lifecycle-Aktion noch einen unbeschränkten
Response-Body-Append vor dem Static Contract verbergen.

Für FND-PARENT-1042 behandelt dieselbe Grenze das vollständige Mapper-All-
Branch-Forbidden-Marker-Tupel plus alle fünf erreichbaren Chain-Buffer-Body-
Pfade als verbotenen Macro-Ersatzlisteninhalt. Für FND-PARENT-1040 weist der
direkte Gate-only-Funktionsbeweis beliebige Helper-Indirection vor dem Gate ab.
Zusammen bewahren sie die Source-Invariante für lokale objektartige Aliasse,
terminale lokale Aliaskettendefinitionen und nicht erkannte lokale Helpernamen,
ohne sich auf einen partiellen Call-Graph zu stützen.

Für H12 umfasst die Checker-Integritätsgrenze außerdem die exakten Header-
Prefix-, `ddebug.h`-Fallback- und PCRE-Shim-Call-Target-Formen. Eine von PR
kontrollierte objektartige `dd`-Definition könnte sonst den bestehenden
`dd(..., ctx)`-Aufruf vor den Header-Guards umleiten; ein zusätzlicher bedingter
Fallback oder ein objektartiges PCRE-Replacement könnte ebenfalls ein
bestehendes Call-Target verändern, während alte Texttreffer an anderer Stelle
erhalten bleiben. Der reparierte Static Contract weist diese lokalen Formen ab,
bevor er ein vertrauenswürdiges `PASS` ausgibt. Die isolierten Syntax-Harnesses
belegen nur C-Syntax; kein mutierter Runtime-Pfad wurde ausgeführt.

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
`##`, UCNs sowie sicherheitskritische/Kontrollfluss- und vollständige Mapper/
Body-Forbidden-Marker-Ersatzlisten-Tokens ab und
prüft quoted lokale Include-Syntax, Pfad, Auflösung und gescannte-Source-
Zugehörigkeit sowie die feste aktuelle Angle-Include-Allowlist.
Die exakten lokalen `ddebug.h`- und PCRE-Formen begrenzen die modellierte
Source-Oberfläche, beweisen aber kein Debug-enabled-Runtime-Verhalten, keine
Compilerkonfiguration und keine Expansion externer Header. Die minimalen
C-Harnesses beweisen nur Syntax.
Er wertet aber externe Compiler-`-D`-Inputs, Expansion innerhalb allowlisteter Third-Party-/

Die geprüften Body-/Header-Caller- und Raw-Sink-Anzahlen sind absichtlich exakt
für die aktuell gescannte lokale Source-Oberfläche. Sie beweisen kein Verhalten
in nicht gescanntem generiertem Code, bei externen Compiler-Definitionen,
Drittanbieter-Headern oder einer nativen NGINX-Ausführung; eine legitime
Source-Topologieänderung muss Contract und isolierte Controls aktualisieren,
statt sich auf eine veraltete Anzahl zu stützen.

Er wertet aber externe Compiler-`-D`-Inputs, Expansion innerhalb allowlisteter Third-Party-/
System-Header, nicht modellierte Compiler-Include-Wurzeln, andere Compiler-
Makro-Semantik außerhalb dieser begrenzten lokalen Oberfläche oder native
Runtime-Reachability nicht aus. Ein künftiges legitimes Refactoring kann ein
bewusstes Checker- und Negativ-Control-Update erfordern.

## Verbleibende Risiken

`FND-PARENT-1010`, `FND-PARENT-1039`, `FND-PARENT-1040`, `FND-PARENT-1042`,
`FND-PARENT-1043`, `FND-PARENT-1044` und `FND-PARENT-1045` werden nicht durch
lokale Evidence geschlossen. Exact-Successor-Head-Hosted-Checks,
SonarQube-Cloud-Analyse, Reviews und jede Resulting-Master-Evidence bleiben
separate Delivery-Pflichten. Die Aufgabe beansprucht keine vollständige
P1–P4-Abnahme oder vollständige native 17×10-Hostmatrix. PR #346 bleibt ein
unabhängiger, unveränderter Draft und muss getrennt gegen den neuen `master`
integriert werden.

## Nicht ausgeführte Prüfungen mit Begründung

Es wurden kein nativer NGINX-Runtime-Replay, keine vollständige P1–P4-Abnahme,
keine vollständige native 17×10-Hostmatrix, keine ASan-, UBSan-, TSan- oder
Leak-Prüfung und keine C-Kompilierung ausgeführt, weil der Delivery-Diff keine
NGINX-C-Runtime-Änderung enthält. Für den lokalen uncommitteten Successor-Head
existieren noch kein Hosted-Workflow und keine SonarQube-Cloud-Analyse. Der
eine frische lokale Post-Patch-Source-to-Sink-Review ist abgeschlossen; sein
rein statischer Follow-up in Form des eingegrenzten Security-Diff-Scans ist
ebenfalls abgeschlossen. Initiale Draft-PR-#357-Evidence existiert nur für
`e9ceb86723383c31914f179638f1b7043ea79609` und verifiziert diesen Successor
nicht. Das nicht verfügbare lokale `ruff`-Executable wurde nicht installiert
oder ersetzt.

## Finaler Diff- und Review-Status

In dieser Record-Revision enthält die initiale Draft-PR #357 bei
`e9ceb86723383c31914f179638f1b7043ea79609` die Sechs-Dateien-Initialänderung
für Checker, Test und Traceability. Ihr lokaler uncommitteter Successor ändert
nur Checker, zielgerichtete Tests und diesen gekoppelten Change Record; er
ändert keine NGINX-Runtime-C, `.github/**`, PR #346 oder `master`. Unabhängige
Read-only-Reviews bestätigten die aktuellen C-Source-to-Sink-Controls und
fanden dann Branch-Binding-, inaktive-Preprocessor-,
Translation-Phase-, Raw-Sink-Schreibweisen-, Kontrollfluss-, Makro-
Ersatzlisten-, Macro-Early-Return-, UCN-Macro-Name-, Function-Macro-Parameter-
Substitution-, Quoted-Local-Include-, Angle-Include- und nichtstandardisierte
Include-Directive-Checker-Bypässe in aufeinanderfolgenden Kandidatenrevisionen.
Die neuesten abgeschlossenen Reviews reproduzierten objektartige Macro-Aliasse für verbotene
Mapper- und Direct-Body-Append-Controls (`FND-PARENT-1042`) sowie einen neu
benannten gewöhnlichen Pre-Gate-Helper (`FND-PARENT-1040`). Der anschließende
unabhängige H10-Review fand keinen source-valid Bypass des exakten direkten
Gate-only-Function-Contracts. H11 reproduzierte danach Literal-only-
ausführbare Controls, unerreichbare Mapper-Caller und Whitespace-/Member- oder
Macro-Component-Varianten (`FND-PARENT-1043`, `FND-PARENT-1044` und
`FND-PARENT-1045`). H12 reproduzierte anschließend Header-Prefix-/Korridor-,
unveränderliche-Mapper-, Diagnose-Body-, objektartige Diagnose-Redirect-,
bedingte Static-Fallback- und objektartige PCRE-Shim-Call-Target-Varianten.
Ein späterer H12-Source-to-Sink-Review reproduzierte Body-Loop-, Raw-Body-,
Outer-Collection-, Raw-Header-, Generic-Wrapper- und Synthetic-Loop-Checker-
False-Passes, alle nur in isolierten Kopien. Der eine frische Post-Patch-Review
reproduzierte danach einen Body-Filter-Zwischen-Caller, eine Memory-Buffer-
Raw-Chunk-Route, ein unbedingtes Scope-Prädikat, eine synthetische `Date`-
Resolver-/Table-Route und einen frühen Return im Iterator für verkettete Header;
direkte Folge-Tests reproduzierten außerdem eine `allowed`-zu-`len`-
Substitution im Limited-Helper. Die aktuelle fokussierte Suite bestand 90
Tests und die vier Companion-Module 54 Tests in der Repository-virtuellen
Umgebung; damit bestanden 144 ausgewählte Tests aggregiert, und das native
Checker-Target bestand alle 74 Assertions. Die aufgabeneigenen
Mutations-Fixtures wurden entfernt, nachdem payload-freie Receipts aufbewahrt
wurden. `git diff --check` bestand vor diesem Record-Update und ist nach seiner
Finalisierung ein verpflichtender Delivery-Check. Die repositoryweiten
Dokumentationsbefehle sind wegen des fehlenden Framework-Checkouts
environment-blocked, während die Pflichtüberschriften und Tabellenzeilenzahlen
des Paares in der aktuellen lokalen Prüfung übereinstimmen. Der vorherige Function-Macro-Scan ist nur historische
Evidence; der aktuelle eingegrenzte H12-Post-Patch-Scan schloss vier
abgeglichene Pfade, zehn abgewiesene Checker-Integritätskandidaten und null
reportable aktuelle Produktbefunde ab. Jede spätere Source- oder Traceability-
Änderung erfordert einen neuen eingegrenzten Review. Ein zweiter normaler
Commit bleibt von frischem Delivery-Preflight, normalem Push, aktualisierten
Draft-PR-Exact-Head-Checks, SonarQube Cloud und Hosted-Review-Evidence abhängig.
