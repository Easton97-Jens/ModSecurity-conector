# Change Record: NGINX-Current-Master-Common-Adoption-Contract-Reparatur

**Sprache:** [English](CR-20260905-nginx-current-master-common-adoption-repair.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260905-nginx-current-master-common-adoption-repair |
| Datum (UTC) | 2026-09-05 |
| Basis-Revision | b779167ff979aa73cdd9321a829f9c693d943760 |
| Delivery-Status | Validierter Implementierungs- und Hosted-Evidence-Head: `672d5aa22a94640f50aea191885f991b0d8f45c3`, mit Parent `8af044dd9d801f4edf163971088fd25795dc578f` und Basis `b779167ff979aa73cdd9321a829f9c693d943760`. Auf dem validierten Head war PR #357 offen, zur Review freigegeben, nicht gemergt, Auto-Merge deaktiviert, mergeable und `clean`. Seine Exact-Head-Evidence erfasste 36 terminale Checks (30 erfolgreich und sechs dokumentierte Skips), Sonar-Quality-Gate `OK`, null `OPEN`/`CONFIRMED`-Issues, Bugs, Vulnerabilities, Code-Smells und `TO_REVIEW`-Hotspots sowie A-New-Code-Ratings und 0,0 % neue Duplikation; die API lieferte keinen `new_coverage`-Wert, deshalb wird kein Coverage-Pass behauptet. Der Dokumentationsabgleich-Successor, der diesen Record enthält, hat Parent `672d5aa22a94640f50aea191885f991b0d8f45c3` und verändert ausschließlich die vier Delivery-Dokumentationsdateien dieses Scopes. Checker, Tests und Produktquellcode sind gegenüber dem validierten Parent byte-identisch. Kein Merge, direkter `master`-Push, PR-#346-Aktion oder Governance-Change wird behauptet; Ready for Review ist keine Merge-Autorisierung. |

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
`FND-PARENT-1010` ist `fixed_in_branch`, bleibt aber bis zum separat
autorisierten Merge und zur Resulting-Master-Reproduktion unverified und
unclosed.

Die folgende Exact-Head-Hosted-Analyse von
`8af044dd9d801f4edf163971088fd25795dc578f` ist historische Vorgänger-Evidence.
Sie meldete keine Bugs, Vulnerabilities oder Security Hotspots, aber sechs offene
aufgabeneigene Code-Smells im Checker: drei `python:S6353`-Character-Class-
Beobachtungen, eine `python:S8786`-Regex-Resource-Beobachtung und zwei
`python:S1192`-Duplicate-Signature-Beobachtungen. Es sind Checker-
Qualitätsbefunde, keine nachgewiesenen NGINX-Runtime-Schwachstellen. H13 erhält
die ASCII-C-Identifier-Grammatik ohne die umgebenden Unicode-aware Word-
Boundaries zu ändern, ersetzt die breite Fallback-Definition-Regex durch einen
begrenzten Nicht-Regex-Fallback-Nachweis und teilt die wiederholten Function-
Selector-Literale. Der Nachweis weist eine normalisierte `ddebug.h`-Source-Sicht
über 4.096 Zeichen ab, verlangt genau zwei exakte inerte Fallback-Definitionen,
maskiert nur diese Definitionen und weist danach verbleibende aktive `dd`-
Identifier außer in separat validierten Makro-Directives ab. Er weist außerdem
nicht allowgelistete Directives sowie aktive `_Pragma`-, `asm`-, `__asm`- oder
`__asm__`-Operatoren ab. Das später validierte Successor-Ergebnis ist im
folgenden H15-Abschnitt festgehalten.

Der H13-Follow-up reproduzierte Macro-Alias-, leere Trailing-Macro-Suffix-,
parenthesierte Deklarator-, Funktionszeiger-, GNU-`#pragma weak`- und C-
`_Pragma`-Weak-Alias-False-Passes in begrenzten kopierten Checker-Sources. Jede
Klasse ist PR-kontrollierte Static-Checker-Integritäts-Evidence: Der Pre-Fix-
Checker konnte einen nichtinerten `dd`-Callable akzeptieren, während literale
inerte Decoys erhalten blieben. Es wurde keine mutierte NGINX-Runtime gebaut
oder ausgeführt; daher werden diese nicht als deployte NGINX-Runtime-
Schwachstellen behauptet. `FND-PARENT-1051`, `FND-PARENT-1052` und
`FND-PARENT-1053` behalten ihre getrennte Evidence und ihren Delivery-Status.

`FND-PARENT-1054` reproduzierte danach einen verwandten Checker-Integritäts-
False-Pass in vier eigentümerseitigen Diagnose-Formatliteralen. In begrenzten
kopierten Sources behielt das Ersetzen des Header-Diagnose-`%p`, des
`dd(...)`-Präfixes oder eines der beiden Event-Handler-Diagnose-`%s`-Literale
durch `%n` den jeweiligen Checker-`PASS` vor der H14-Reparatur. H14 bindet und
regressiert zusätzlich das bestehende `dd(...)`-Suffixformat, sodass fünf
exakte sichtbare Literale aktuelle Mutationsabdeckung haben. Die aktive
Checker-Sicht maskiert C-String-Literale, sodass ihre früheren strukturellen
Formen den sichtbaren Formattext nicht binden konnten. Dies ist ein Static-
Contract-Defekt unter PR-kontrollierten Source-Änderungen, kein nachgewiesener
NGINX-Runtime- oder Remote-Exploit; keine mutierte native Runtime wurde gebaut
oder ausgeführt. Das später validierte Successor-Ergebnis ist unten festgehalten.

Während der Sonar-Remediation des Nachfolgers reproduzierte `FND-PARENT-1039`
einen separaten Static-Checker-Control-Bypass: Eine rohe Funktions-Extraktion
konnte an einer Klammer in Kommentar, Literal oder inaktivem Branch vor einem
verbotenen Lifecycle- oder unbeschränkten Response-Body-Append enden. Dies ist
kein Nachweis einer aktuellen NGINX-Runtime-Schwachstelle; der Folgepatch
repariert die gemeinsame Checker-Grenze. Das später validierte
Successor-Ergebnis ist unten festgehalten.

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
keine aktuelle NGINX-Runtime-Schwachstelle; die später validierte
Successor-Evidence ist unten festgehalten.

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
eingegrenzter Security-Scan und Exact-Successor-Head-Evidence waren zu diesem
Zeitpunkt noch erforderlich.

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
  `dd_check_*(r)`-Ternär- bzw. `(void)(r)`-Body. Eine PCRE-Shim ist nur als exakte
  `ngx_http_modsecurity_pcre_malloc_init(x)`/`NULL`- bzw.
  `ngx_http_modsecurity_pcre_malloc_done(x)`/`(void)x`-funktionsartige Form
  zulässig. Ein quoted lokales Include wird abgewiesen, wenn es dynamisch,
  pfadunsicher oder nicht auf die gescannte NGINX-, Common- und Profile-Source-
  Menge auflösbar ist. Die explizit modellierte externe `stdio.h`-Ausnahme ist
  nur zulässig, wenn kein lokaler Kandidat sie überschattet. Ein Angle-Bracket-
  Include muss die feste aktuelle External-Header-Allowlist verwenden und
  dieselbe Local-Shadow-Prüfung erfüllen; nichtstandardisierte `#include_next`
  und `#import` werden abgewiesen.
- Der `ddebug.h`-Fallback-Nachweis arbeitet auf einer Translation-Phase-
  normalisierten Source-Sicht mit höchstens 4.096 Zeichen. Er verlangt genau
  zwei exakte inerte nichtvariadische `dd`-Definitionen, maskiert diese Bereiche
  und weist danach jedes verbleibende aktive `dd`-Token ab, sofern es nicht auf
  einer separat validierten Makro-Directive steht. Nur die aktuellen Directive-
  Formen `define`, `if`, `ifndef`, `else`, `endif` und `include` sind zulässig;
  `_Pragma`, `asm`, `__asm` und `__asm__` werden abgewiesen. Dies ist ein enger
  Callable-/Fallback-Source-Contract und keine allgemeine C-Source-Allowlist.
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
- Der Checker nutzt inline-ASCII `\w` nur für die drei C-Identifier-Suffix-
  Fragmente und behält die umgebenden Standard-Word-Boundaries. Seine nicht-
  direktive `dd`-Definitionszählung ist ein begrenzter linearer Scan: eine
  übergroße oder nicht klassifizierbare Deklaration scheitert fail-closed, und
  genau zwei inerte statische Fallback-Definitionen bleiben erforderlich.
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

Für H13 verwenden die `phase4_`-, `response_body_`- und `ngx_http_next_`-
Suffixe ein inline-ASCII-`\w`-Fragment statt einer breiten Unicode-
Zeichenklasse, während ihre ursprünglichen äußeren Word-Boundaries unverändert
bleiben. Die Diagnostic-Fallback-Definitionsprüfung verlässt sich nicht mehr
auf überlappende unbeschränkte Regex-Klassen. Ihre normalisierte Source-Sicht
mit 4.096 Zeichen muss genau zwei exakte inerte Fallbacks enthalten; nach dem
Maskieren lassen verbleibende aktive `dd`-Tokens, nicht allowgelistete
Directives und `_Pragma`-/Assembler-Operatoren den Check fail-closed scheitern.
Damit werden die reproduzierten Macro-, Deklarator-, Pointer-, Pragma- und
Operator-Repräsentationen geschlossen, ohne beliebigen externen Compiler-State
zu interpretieren. Geteilte Signature-Konstanten erhalten je einen Selector für
die geprüften Mapper- und Header-Filter-Source-Grenzen.

Damit bleibt das aktuelle restriktive C-Verhalten erhalten, statt die
veraltete Warn-only-Mapper-Erwartung oder einen direkten rohen Server-Sink
wiederherzustellen. Unabhängige Read-only-Source-to-Sink-Reviews fanden keinen
Source-Level-Bypass auf den aktuell geprüften Pfaden; keine native Runtime wurde
ausgeführt. Sie identifizierten auch
aufeinanderfolgende Checker-Control-False-Pass-Möglichkeiten, die jetzt durch
die exakten Branch-Prädikate, Makro-Einschränkungen, Include-Auflösung und
Negativ-Controls abgedeckt sind.

## H15-Sonar-Behebung, validierter Head und historische lokale Evidence

Der `8af044dd9d801f4edf163971088fd25795dc578f`-Preflight und seine sechs
`OPEN`-SonarQube-Cloud-Issues sind historische Vorgänger-Evidence. Diese
Checker-only-Issues waren dreimal `python:S6353`-Character-Class, einmal
`python:S8786`-Regex-Resource und zweimal `python:S1192`-Duplicate-Signature.
Sie werden nicht als native NGINX-Runtime-Schwachstellen behauptet.

Der validierte Implementierungs- und Hosted-Evidence-Head ist
`672d5aa22a94640f50aea191885f991b0d8f45c3`, mit Parent
`8af044dd9d801f4edf163971088fd25795dc578f`. Die H15-Behebung verwendet ein
scoped-ASCII-Fragment `(?a:\w*)` für C-Identifier-Suffixe, einen begrenzten
4,096-Zeichen-Fallback-Nachweis und geteilte Selector nur für semantisch
identische Source-Grenzen. Sie fügt weder `NOSONAR` noch Suppression,
Exclusion, Akzeptierung, Regel-, Quality-Gate- oder Workflow-Änderung hinzu.

Auf dem validierten Head war PR #357 offen, zur Review freigegeben, nicht
gemergt, Auto-Merge deaktiviert, mergeable und `clean`; `master` blieb
`b779167ff979aa73cdd9321a829f9c693d943760`. Sein Exact-Head-Rollup war
terminal: 36 Checks insgesamt, 30 `SUCCESS`, sechs dokumentierte `SKIPPED` und
keine fehlgeschlagenen, abgebrochenen, queued oder aktiven Checks. Es gab keine
eingereichten Reviews und keine Review-Threads. Das gehostete SonarQube-Cloud-
Quality-Gate war `OK`, mit null `OPEN`/`CONFIRMED`-Issues, Bugs,
Vulnerabilities, Code-Smells und `TO_REVIEW`-Security-Hotspots; neue
Reliability-, Security- und Maintainability-Ratings waren A und neue Duplikation
war 0,0 %. Die API lieferte keinen `new_coverage`-Wert, deshalb behauptet dieser
Record keinen Coverage-Pass. PR #346 wurde ausschließlich read-only geprüft und
bleibt ein unabhängiger Draft.

Auf dem validierten lokalen Source-/Test-Baum bestand die Python-Kompilierung;
der direkte Checker und `make check-nginx-common-adoption` bestanden jeweils
alle 74 Assertions; 92 isolierte Mutation- und Legitimate-Control-Tests
bestanden; und das Repository-Virtualenv führte alle 54 Companion-Tests aus.
Die zwei an den validierten Patch gebundenen Final-Tree-Static-Security-Diff-
Reviews meldeten null reportable Befunde. Die Vier-Dateien-Binary-Patch-SHA-256
des validierten H14/H15-Successors ist
`9edcc00d0250fa3ec222753a41388d884ec6b6eb42b1e72be2f871466b451843`. Ein
System-Python-Companion-Versuch war ausschließlich wegen seines fehlenden
`yaml`-Moduls environment-blocked und wurde nicht durch eine Installation
ersetzt. Die lokale Vortex-/Sonar-Abfrage blieb HTTP-403-environment-blocked;
Hosted SonarQube Cloud ist die relevante Exact-Head-Evidence.

## Geänderte Dateien

Validiertes PR-#357-Dateiset auf Implementierungs-Head
`672d5aa22a94640f50aea191885f991b0d8f45c3` (sechs getrackte Pfade):

- `ci/checks/connectors/nginx/check-nginx-common-adoption.py`
- `tests/test_nginx_common_adoption.py`
- `reports/audits/change-records/CR-20260905-nginx-current-master-common-adoption-repair.md`
- `reports/audits/change-records/CR-20260905-nginx-current-master-common-adoption-repair.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

Der Dokumentationsabgleich-Successor, der diesen Record enthält, hat Parent
`672d5aa22a94640f50aea191885f991b0d8f45c3` und verändert exakt diese vier
Delivery-Dokumentationspfade:

- `reports/audits/change-records/CR-20260905-nginx-current-master-common-adoption-repair.md`
- `reports/audits/change-records/CR-20260905-nginx-current-master-common-adoption-repair.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

Er verändert keinen Checker-, Test- oder Produktquellcodepfad; diese Pfade sind
gegenüber dem validierten Parent byte-identisch.

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
| `make check-bilingual-docs` und `make check-doc-links` | Durch den nicht initialisierten `modules/ModSecurity-test-Framework`-Gitlink blockiert: vorhandene Repository-Links auf Framework-Dateien fehlen. An diesem historischen Kontrollpunkt meldete kein Befehl einen aufgabeneigenen Change-Record-Linkfehler. Das Paar hatte in jeder Sprache 13 Pflichtüberschriften; dieser historische Kontrollpunkt belegte nicht die Gleichheit jedes Backtick-begrenzten Literals. |
| `git diff --check` | Bestanden. |
| Initialer Security-Diff-Scan | Für die vorhergehende Kommentar-Decoy-Revision abgeschlossen: In diesem Snapshot blieb kein reportable Befund. Er bleibt nur als historische Evidence aufbewahrt. |
| Historischer finaler Function-Macro-Security-Diff-Scan | Abgeschlossen am `2026-09-05T10:22:18.683709Z`: Der vorherige Sechs-Pfad-Snapshot hatte vollständige Abdeckung und null reportable Befunde. Seine SHA-256 lautet `7ff57a88702a922644dc0d3ebca96d3bbbf19e3a0ca9031b656cdf7b9e00d9ae`; er deckte den damaligen FND-PARENT-1040/-1042-Successor-Scope nicht ab und wird nur als historische Evidence behalten. Die späteren Final-Tree-Scans für den validierten Head sind im H15-Abschnitt dokumentiert. |
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
| Frühere H13-Pre-Repräsentations-Controls | Nur historisch: Fünf fokussierte Methoden und der vorhergehende 90-Test-/54-Companion-/74-Assertion-Snapshot bestanden, bevor die späteren Macro-, Deklarator-, Pointer-, Pragma- und `_Pragma`-False-Pass-Klassen gefunden wurden. Dies ist keine Final-Tree-Evidence. |
| H13 ddebug-Repräsentations-Pre-Fix-Controls | Jede begrenzte copied-source Klasse verursachte vor ihrer jeweiligen Reparatur Checker-Exit `0`: Macro-Alias, leeres Macro-Suffix, parenthesierter Deklarator, Funktionszeigerbindung, `#pragma weak` und `_Pragma`-Weak-Alias. Keine mutierte NGINX-Runtime wurde gebaut oder ausgeführt. |
| H13 aktuelle ddebug-Regressionsmethode | Bestanden: `test_additional_conditional_diagnostic_fallback_is_rejected` endete in `20.232s`; sie weist Multiline-, übergroße, Alias-, Suffix-, Deklarator-, Pointer-, direkte-Pragma-, direkte-`_Pragma`- und Macro-umhüllte-`_Pragma`-Controls ab. |
| H13 aktuelle vollständige Checker-Mutation-Suite | Bestanden: 90 isolierte Checker-Mutationstests in `322.007s`; der begrenzte task-owned Prozess endete mit `0`. |
| H13 aktuelle Companion-Suite | Bestanden: 54 Companion-NGINX-Contract-Tests in `1.912s`. |
| H13 aktuelles Checker-Target und Syntax | Bestanden: alle 74 `make check-nginx-common-adoption`-Assertions und `python3 -m py_compile ci/checks/connectors/nginx/check-nginx-common-adoption.py tests/test_nginx_common_adoption.py`. Keine native NGINX-Runtime wurde gebaut oder ausgeführt. |
| H13 unabhängiger Post-Fix-Fallback-Review | Kein konkreter source-valid `dd`-Alias- oder Fallback-Bypass blieb in der eingegrenzten lokalen Source. Externe Compiler-Definitionen, toolchain-vordefinierte Makros und transitive System-Header bleiben explizit unmodellierte Grenzen. |
| Terminaler eingegrenzter H13-Security-Diff-Scan | Abgeschlossen am `2026-09-06T09:41:20Z`: Der exakte lokale Vier-Pfad-Patch hatte vollständige Abdeckung, vier Kandidatenzeilen (drei abgewiesen und eine nicht anwendbar) und null reportable Befunde. Versiegelte Report-SHA-256: `36f8f21464a56842cd9b60507fc4050fc2c08a9dab2a2fe817ea5866bb3b9346`. Dies ist ausschließlich statische Checker-/Test-/Traceability-Evidence; es wird weder ein nativer Runtime-, Hosted- noch Sonar-Resultat behauptet. |
| H14 Diagnose-Format-Pre-Fix-Controls | In vier begrenzten copied-source Fällen behielt das Ändern des Header-Diagnose-`%p`, des `dd(...)`-Präfixes, der Read-Event-Diagnose oder der Write-Event-Diagnose zu `%n` den jeweiligen `PASS` des Pre-Fix-Checkers. Dies bestätigt nur einen Checker-Integritäts-False-Pass; keine mutierte NGINX-Runtime wurde gebaut oder ausgeführt. |
| Frühere H14 zielgerichtete Diagnose-Format-Regression | Historisch vor der Suffixabdeckung: `test_diagnostic_format_literal_side_effect_is_rejected` beendete einen Test in `8.371s` und weist die vier Pre-Fix-`%n`-Mutationen in isolierten kopierten Sources ab. |
| Frühere H14 kombinierte fokussierte Regressionsgruppe | Historisch vor der Suffixabdeckung: Der aktuelle Positiv-Control, die Pre-Guard-Bypasses, der bestehende Macro-Side-Effect-Control und die Diagnose-Format-Regression beendeten vier Tests in `32.648s`. |
| H14 aktuelle zielgerichtete Diagnose- und Source-Path-Regressionen | Bestanden: `test_diagnostic_format_literal_side_effect_is_rejected` weist alle fünf aktuellen `%n`-Literalmutationen einschließlich des Suffixes ab, das kein Pre-Fix-Reproduktionsfall war; zusammen mit `test_critical_macro_source_symlink_is_rejected` endeten die zwei Tests in `11.969s`. Letzterer bestätigt, dass der Critical-Macro-Source-Input ein symbolisches `ddebug.h` abweist, statt sein Ziel still als gescannte Source zu behandeln. |
| H14 aktuelle vollständige Checker-Mutation-Suite | Bestanden: 92 isolierte Checker-Mutationstests in `336.194s`; der begrenzte task-owned Prozess endete mit `0`. |
| H14 aktuelle Companion-Suite | Bestanden: 54 Companion-NGINX-Contract-Tests in `2.039s`. |
| H14 aktuelles Checker-Target, Syntax und Diff-Hygiene | Bestanden: alle 74 `make check-nginx-common-adoption`-Assertions, `python -m py_compile` für Checker und fokussiertes Testmodul sowie `git diff --check`. Keine native NGINX-Runtime wurde gebaut oder ausgeführt. |
| H14 unabhängiger Post-Fix-Diagnose-Review | Die vier Pre-Fix-`%n`-Mutationen, der fünfte `dd(...)`-Suffix-Control, Escaped-Percent-Schreibweise und Literal-Konkatenationsvarianten wurden abgewiesen. Die copied-source-Symlink-Regression deckt den Checker-Inputtyp unabhängig ab. Ein `%n` in einem ansonsten ungebundenen `dd()`-Call bleibt außerhalb dieses Fünf-Literal-Contracts und ist ein Restkandidat für separat eingegrenzte allgemeine Format-String-Analyse, kein nachgewiesener Bypass der H14-Controls. |
| Terminaler eingegrenzter H14-Security-Diff-Scan | Abgeschlossen am `2026-09-06T11:25:34Z`: Der damalige exakte lokale Vier-Pfad-Snapshot hatte vollständige Abdeckung, vier Kandidatenzeilen (zwei abgewiesen und zwei nicht anwendbar) und null reportable Befunde. Versiegelte Report-SHA-256: `35dfd937600e3f2a6f47b72ff5c919e168bb47aca8d8adf0d827685eec4e8a5d`. Dies ist ausschließlich statische Checker-/Test-/Traceability-Evidence; es wird weder ein natives Runtime-, Hosted- noch Sonar-Resultat behauptet. |

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

Für H13 bindet der Diagnose-Fallback-Control jetzt den `dd`-Callable, statt nur
vertrauten Deklarationstext zu zählen. Macro-Aliase, Trailing-Macro-Suffixe,
parenthesierte Deklaratoren, Funktionszeigerbindungen, direkte oder macro-
umhüllte `_Pragma`-Aliase und GNU-Pragma-Aliase können keinen versteckten
nichtinerten Callable hinter zwei literalen Decoys zurücklassen. Der Scan bleibt
bewusst source-lokal: Er behauptet nicht, externe Compiler-Definitionen,
toolchain-vordefinierte Makros, transitive System-Header oder beliebigen anderen
Code in `ddebug.h` zu modellieren. Ein beliebiger nicht zusammenhängender
Constructor ist kein `dd`-Fallback-Bypass und macht aus diesem Checker keine
allgemeine C-Source-Allowlist.

Für H14 behält der Checker seine maskierten strukturellen Sichten bei, verlangt
aber zusätzlich das exakte sichtbare aktuelle Formatliteral an der Header-
Diagnose und den vier eigentümerseitigen `ddebug.h`-Macro-Stellen: insgesamt
fünf Literale. Das schließt den Pre-Fix-`%n`-False-Pass vor einem
vertrauenswürdigen Checker-`PASS`. Unter dem optionalen variadischen
Debug-Macro wird das Literal an `fprintf(stderr, __VA_ARGS__)` weitergereicht;
die Source-to-Sink-Beobachtung motiviert den Static-Control, belegt aber weder
Debug-enabled native Runtime-Reachability noch einen Remote-Exploit. Seine
Critical-Macro-Source-Inputs weisen außerdem Symlinks ab, sodass der geprüfte
`ddebug.h`-Pfad im copied-source-Contract nicht still auf ein ungescanntes Ziel
umgeleitet werden kann.

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
C-Harnesses beweisen nur Syntax. Er wertet externe Compiler-`-D`-Inputs,
Expansion innerhalb allowlisteter Third-Party-/System-Header, nicht modellierte
Compiler-Include-Wurzeln, andere Compiler-Makro-Semantik außerhalb dieser
begrenzten lokalen Oberfläche oder native Runtime-Reachability nicht aus. Ein
künftiges legitimes Refactoring kann ein bewusstes Checker- und Negativ-Control-
Update erfordern.

Der H13-`ddebug.h`-Nachweis besitzt eine 4.096-Zeichen-Grenze für die
normalisierte Sicht und ist bewusst auf Fallback-Callable, genehmigte lokale
Directives und Compiler-/Linkage-Operatoren begrenzt, die diesen Callable ändern
können. Er kontrolliert keine beliebigen nicht zusammenhängenden C-Definitionen
im Header; eine solche Änderung ist ein allgemeines Source-Integrity-Risiko
außerhalb dieses Checker-Contracts und erfordert einen anderen repositoryweiten
Control.

Der sichtbare H14-Literal-Control schützt bewusst nur die fünf aktuellen
eigentümerseitigen Diagnose-Stellen; er ist kein allgemeiner C-Format-String-
Analyzer. Ein `%n`, das in einen anderen ungebundenen `dd()`-Call eingeführt
wird, liegt außerhalb der H14-Invariante und braucht separaten Scope und
Evidence, bevor es als handlungsrelevanter Produktbefund behandelt wird. Der
Checker modelliert die C17-Source-Oberfläche des Repositories; eine hypothetische
C23-`#embed`-Erweiterung gehört weder zu diesem Contract noch zu dessen Evidence
und wird nicht als aktueller Bypass klassifiziert.

Die geprüften Body-/Header-Caller- und Raw-Sink-Anzahlen sind absichtlich exakt
für die aktuell gescannte lokale Source-Oberfläche. Sie beweisen kein Verhalten
in nicht gescanntem generiertem Code, bei externen Compiler-Definitionen,
Drittanbieter-Headern oder einer nativen NGINX-Ausführung; eine legitime
Source-Topologieänderung muss Contract und isolierte Controls aktualisieren,
statt sich auf eine veraltete Anzahl zu stützen.

## Verbleibende Risiken

`FND-SONAR-0079`, `FND-SONAR-0080` und `FND-SONAR-0081` sind auf dem
validierten Head `fixed_in_branch`. `FND-PARENT-1010` ist ebenfalls
`fixed_in_branch`, bleibt aber bis zum separat autorisierten Merge und zur
Resulting-Master-Reproduktion unverified und unclosed. Lokale
`FND-PARENT-1054` und `FND-PARENT-1055` bleiben lokale Nachverfolgung und sind
nicht Teil dieses PR-Diffs. Kein Finding wird allein durch diesen
Dokumentationsabgleich-Successor geschlossen.

Der terminale H13-Scan ist für den geänderten H14-Baum historische Evidence.
Die vollständige H14-Mutation- und Companion-Ausführung, der unabhängige
Post-Fix-Review und die terminalen eingegrenzten Static-Scans bestanden lokal;
der validierte Implementierungs-Head hat außerdem eigene Hosted-Checks,
SonarQube-Cloud-Analyse und Review-Evidence. Diese Aufgabe beansprucht keine
native NGINX-Runtime-Validierung, keine vollständige P1–P4-Abnahme und keine
vollständige native 17×10-Hostmatrix. PR #346 bleibt ein unabhängiger,
unveränderter Draft und muss getrennt gegen einen späteren `master`-Stand
integriert werden.

## Nicht ausgeführte Prüfungen mit Begründung

Es wurden kein nativer NGINX-Runtime-Replay, keine vollständige P1–P4-Abnahme,
keine vollständige native 17×10-Hostmatrix, keine ASan-, UBSan-, TSan- oder
Leak-Prüfung und keine native NGINX-C-Kompilierung ausgeführt, weil der
Delivery-Diff keine NGINX-C-Runtime-Änderung enthält. Zwei isolierte minimale
C-Syntax-Harnesses wurden mit `-fsyntax-only` kompiliert; sie üben weder NGINX
noch einen mutierten Runtime-Call aus. Hosted-Workflow- und SonarQube-Cloud-
Evidence existiert für den validierten Implementierungs-Head
`672d5aa22a94640f50aea191885f991b0d8f45c3`; dieser Dokumentations-only-
Successor überträgt diese Evidence nicht auf seine eigene, absichtlich nicht im
Record benannte Commit-SHA. Die H12- und H13-Post-Patch-Scans sind nur
historische Evidence. Die H14-Mutation- und Companion-Suite, der unabhängige
Post-Fix-Review, terminale eingegrenzte Security-Diff-Scans, die direkte
Paar-Dokument-Suite und Diff-Hygiene sind lokal abgeschlossen. Die
repositoryweiten bilingualen und Path-Reference-Make-Targets sind ausschließlich
durch fehlende Framework-Gitlink-Ziele environment-blocked; sie werden nicht als
bestanden ausgegeben. Das nicht verfügbare lokale `ruff`-Executable wurde nicht
installiert oder ersetzt.

## Finaler Diff- und Review-Status

Der validierte Implementierungs- und Hosted-Evidence-Head für PR #357 ist
`672d5aa22a94640f50aea191885f991b0d8f45c3`, mit Parent
`8af044dd9d801f4edf163971088fd25795dc578f`. Sein H14/H15-Checker- und
Test-Patch besitzt die oben dokumentierte lokale, unabhängige Review- und
Hosted-Evidence. Der Dokumentationsabgleich-Successor, der diesen Record
enthält, hat diesen validierten Head als Parent und verändert nur die
gekoppelten Change-Record- und README-Indexpfade. Er verändert keinen
NGINX-Runtime-C-, Checker-, fokussierten Test-, `.github/**`-, PR-#346- oder
`master`-Pfad; diese Nicht-Dokumentationspfade sind gegenüber dem validierten
Parent byte-identisch.

Die sechs `ddebug.h`-Repräsentationsreparaturen und der terminale H13-Scan
bleiben historische Evidence. H14 behält den Contract der fünf exakten
sichtbaren Diagnose-Literale und die zielgerichteten Literal- und
Source-Symlink-Regressionen, vollständigen aktuellen Suiten, unabhängigen
Post-Fix-Review, direkte bilinguale Dokument-Suite, Diff-Hygiene und terminalen
Scans. Repositoryweite Dokumentationsbefehle sind ausschließlich durch fehlende
Framework-Ziele environment-blocked und werden nicht als bestanden dargestellt.
Dieser Dokumentationsabgleich ist kein Merge, und Ready for Review ist keine
Merge-Autorisierung. Der neue Documentation-only-Successor benötigt nach einem
normalen Push eigene Exact-Head-Checks, SonarQube-Cloud-Analyse und
Review-Readback; die validierte Parent-Evidence bleibt ausschließlich
Parent-Evidence.
