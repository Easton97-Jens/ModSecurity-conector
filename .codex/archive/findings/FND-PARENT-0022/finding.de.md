# FND-PARENT-0022 — Den CodeQL-Reflected-XSS-Alerts #14 und #15 fehlt ein connector-eigener Request-Header-zu-Body-Pfad

| Feld | Record |
| --- | --- |
| Priorität / Status | P2 / closed (archiviert) |
| Ownership | Parent / Traefik Native Middleware |
| Scope | `connectors/traefik/native_middleware` auf `c8ca0d92b630c18232b881855c4f5d1482568ea6` |
| GitHub-Status | #14 und #15 sind als `false positive` dismissed; keiner ist als fixed markiert. |
| Final Disposition | `false_positive_in_connector_scope` |
| Feasibility | `not_applicable` für einen Connector-Patch; das einzige verbleibende Risiko ist ein externer Downstream-Renderer außerhalb dieses Connector-Scopes. |

## Aktuelle Alert-Evidence

| Alert | GitHub-Quelle | GitHub-Sink | Component-Disposition |
| --- | --- | --- | --- |
| #14 | `middleware.go:356:40-54` | `middleware.go:656:30-37` | An diesem Sink bereits sicher: Der Call steht unter `len(payload) == 0` und leitet null Body-Bytes weiter. |
| #15 | `middleware.go:356:40-54` | `middleware.go:688:42-47` | Keine connector-eigene Reflexion: Er leitet einen nichtleeren Chunk eines externen Downstream-Handlers weiter. |

Unmittelbar vor ihrer autorisierten Disposition waren beide aktuelle, offene
CodeQL-2.26.1-`go/reflected-xss`-Ergebnisse mit `error` / hoher
Security-Severity in der Traefik-Go-Analyse `1495452276`. Die GitHub-REST-
Antwort identifiziert Quelle und Sink, gab aber keine erweiterte intermediäre
`codeFlows`-Sequenz zurück; es war kein Workflow-Artefakt verfügbar.

## GitHub-Disposition

Unmittelbar vor jedem PATCH wurden Alertnummer, Rule-ID `go/reflected-xss`,
Open-Status, Revision `c8ca0d92b630c18232b881855c4f5d1482568ea6`, Source-Link,
Datei/Sink und die übereinstimmende retained Evidence erneut geprüft. GitHub
gab danach die folgenden endgültigen Alert-Zustände zurück:

| Alert | Zustand / Grund | Zeitpunkt | Analysierte Quelle und Sink | `fixed_at` |
| --- | --- | --- | --- | --- |
| #14 | `dismissed` / `false positive` | `2026-07-18T08:55:32Z` | `middleware.go:356:40-54` → `middleware.go:656:30-37` | `null` |
| #15 | `dismissed` / `false positive` | `2026-07-18T08:58:49Z` | `middleware.go:356:40-54` → `middleware.go:688:42-47` | `null` |

GitHub-Kommentar für #14 (wortgleich):

> The reported sink is reachable only when len(payload) == 0 and therefore
> writes no response-body bytes. The reported source cannot be reflected
> through this sink. Focused boundary tests confirmed a zero-byte body.

GitHub-Kommentar für #15 (wortgleich):

> The connector forwards bytes produced by an externally supplied downstream
> handler. It does not render the reported source into an HTML or browser
> execution context. Context-specific encoding remains the responsibility of
> any downstream renderer that constructs such content.

## Administrativer Abschluss

Am `2026-07-18T09:43:15Z` wurde dieses Finding administrativ mit
`final_disposition: false_positive_in_connector_scope` geschlossen. Der
aktuelle Alert-Record, die exakt analysierte SHA, Source- und Sink-Stellen,
`fixed_at: null` sowie alle fünf retained Evidence-Artefakte tragen diesen
Abschluss. Dies ist eine connector-spezifische False-Positive-Disposition,
kein Claim, dass einer der Alerts fixed sei, und keine Risikoakzeptanz für ein
Downstream-Deployment.

Der getrennte Zustand der Temporary-Root-Finalisierung wird als
[`FND-HOST-0005`](../FND-HOST-0005/finding.de.md) mit
`blocked_environment` / `temporary_exceed` geführt. Er beeinflusst weder den
GitHub-Alertstatus noch diesen Connector-Scope-Abschluss; es wurde kein Cleanup
ausgeführt.

## Source-to-Response-Analyse

Der Request-Header wird begrenzt und an `Transaction.ProcessHeaders` übergeben:

```text
request.Header → boundedHeaders → processHeaders → Engine-Entscheidung
```

Eine disruptive Request-Header-Entscheidung kehrt vor Konstruktion des
gewrappten Response-Writers oder Aufruf von `next.ServeHTTP` zurück.
Middleware-generierte Failure- und Deny-Responses löschen Header, setzen
`text/plain; charset=utf-8` und schreiben feste Literale. Das Engine-Ergebnis
enthält nur Action, Status und eine optionale Redirect-Location; es kann die
gemeldeten Response-Body-Bytes nicht liefern.

Für #14 liegt `responseWriter.Write` im Empty-Payload-Zweig, daher erhält
`target.Write` keine Bytes. Für #15 stammt der Response-Writer-Chunk vom von
Traefik bereitgestellten `next`-Handler. Der Connector weist weder Request-
Header noch Metadaten oder ein Engine-Ergebnis diesem Chunk zu.

Eine Application-Level-Reflexion benötigt einen zusätzlichen externen Pfad:

```text
Request-Header → Downstream-Handler liest ihn → Handler rendert unsicheren Browser-Kontext
→ transparente Middleware leitet Handler-Bytes weiter
```

Dieser Handler wurde im autorisierten Parent-Connector-Source nicht gefunden.

## Controls, Kompatibilität und Test-Evidence

- Der task-eigene Go-Boundary-Probe bestand HTML-, Attribut-, Script-, URL-,
  encodierte, doppelt encodierte, leere, Unicode- und Invalid-UTF-8-Varianten.
- Eine sichere Downstream-HTML-Response enthielt nie den kontrollierten Header.
- Der #14-Empty-Write-Zweig commitete einen Zero-Byte-Body.
- Eine Pre-Request-Deny schrieb nur `request rejected\n` mit festem text/plain
  und rief den Downstream-Handler nie auf.
- Ein absichtlich unsicherer Downstream-HTML-Echo bewahrte Input exakt. Dieser
  Control beweist, dass der Output-Kontext diesem Handler gehört, nicht dass der
  Connector verwundbar oder ein Middleware-Sanitizer ist.
- `make -C connectors/traefik test-native-middleware` und
  `build-native-middleware` bestanden beide mit task-eigenen Cache-/Build-Outputs.

Globales HTML-Escaping oder erzwungenes `text/plain` im Streaming-Adapter ist
keine sichere Remediation: Es würde HTML-, JSON-, Binär-, bereits encodierte und
Streaming-Response-Semantik beschädigen und keinen kontextkorrekten
Output-Encoder etablieren.

## Erforderliche nächste Aktion

Den Connector für diese dismissed connector-lokalen False Positives weder
ändern noch unterdrücken. Falls ein konkreter Downstream-Handler eines
Deployments in den Scope kommt, diesen Handler tracen und an seinem
tatsächlichen HTML-/Attribut-/JavaScript-/URL-Renderer kontextspezifisches
Encoding anwenden; anschließend renderer-eigene Regression-, Legitimate-
Control- und Bypass-Tests hinzufügen. Das Dismissal untersucht, remediated
oder risikoakzeptiert diesen Downstream-Deployment-Pfad nicht.

## Evidence und Residual Risk

Der kanonische JSON-Record listet gehashte aktuelle GitHub-Inventar-, Probe-,
Connector-Validation- und Disposition-Artefakte unter den Runs
`20260718T074759Z-codeql-xss-alerts-14-15-87ada941` und
`20260718T084215Z-github-code-scanning-disposition-14-15-babc842c`.

#14 hat keinen component-lokalen reflektierten Body-Pfad. #15 kann nur dann
Teil eines realen Application-Level-XSS sein, wenn ein externer Downstream-
Handler eine unsichere Reflexion ohne kontextkorrektes Encoding in einen HTML-,
Script-, Attribut- oder URL-Kontext rendert. Dieser Deployment-Pfad ist durch
diese Aufgabe weder belegt, untersucht, remediated noch risikoakzeptiert. Es
änderten sich kein Produktcode, keine Produkttests, kein Framework, kein MRTS,
kein Gitlink, kein Commit und kein Pull Request.

## Historie

- `2026-07-18T08:18:55Z`: Aktuelle Alerts wurden mit retained
  Connector-Boundary-Evidence triagiert; es gab keine Statusänderung.
- `2026-07-18T09:02:09Z`: GitHub zeichnete #14 und #15 als dismissed / `false
  positive` auf; `fixed_at` bleibt für beide `null`.
- `2026-07-18T09:43:15Z`: administrativ als
  `false_positive_in_connector_scope` geschlossen; das einzige verbleibende
  Risiko ist ein externer Downstream-Renderer mit unsicherer
  kontextabhängiger Ausgabe.
