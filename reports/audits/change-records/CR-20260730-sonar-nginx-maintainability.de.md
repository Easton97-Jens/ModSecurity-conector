# Change Record: Parent-NGINX-Maintainability-Remediation

**Sprache:** [English](CR-20260730-sonar-nginx-maintainability.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260730-sonar-nginx-maintainability` |
| Datum (UTC) | `2026-07-30` |
| Basis-Revision | `caddd86d1eede95de53aa1bc971dd26d875df21c` |
| Bewertete Source-Revision | Lokaler Task-Patch gegen die genannte Basis-Revision. |
| Grenze | Parent-`connectors/nginx/`-Source, ein direkter NGINX-Source-Contract-Check, dieses EN/DE-Paar und gepaarte Indizes. Keine `.github`-, Framework-, MRTS-, Gitlink-, Scanner-Konfigurations-, Quality-Gate-, Exclusion-, Suppression-, `NOSONAR`-, Default-Branch- oder Merge-Aktion. |
| SonarQube-Cloud-Verknüpfung | 16 offene aktuelle C-Code-Smells: `c:S3776` an Access-, Phase-4- und Intervention-Pfaden; `c:S134` in der Header-Traversierung; `c:S3358` in der Phase-4-Event-Auswahl sowie `c:S1134`/`c:S1135` für Deferred-Work-Marker. |

## Motivation und Problemstellung

Das Parent-Inventar für `connectors/nginx/` meldet 16 offene
Maintainability-Befunde, aber null Bugs, Vulnerabilities, Security-Hotspots und
Duplikatzeilen. Drei NGINX-Lifecycle-Funktionen überschreiten Sonars Grenze für
kognitive Komplexität, die Request-Header-Traversierung verschachtelt einen
zweiten Zweig, die Phase-4-Event-Erzeugung benutzt zwei verschachtelte
Ternärausdrücke, und zehn alte `FIXME`-/`TODO`-Kommentare beschreiben keine
noch umsetzbare Arbeit.

Die Remediation muss Funktionskomplexität senken, ohne ModSecurity-Aufrufe über
NGINX-Lifecycle-Grenzen zu verschieben oder Interventionsergebnis, Log-Grund,
Status oder Response-Commit-Entscheidung zu verändern.

## Implementierungsentscheidung und Begründung

Der Access-Handler delegiert Connection-, URI-, Header-List-Traversierung,
Header-Verarbeitung, Body-Anforderung, Stream-Body-Append und finale
Body-Verarbeitung an enge Helper. Jeder bewahrt Phase-Marker, PCRE-Pool-Paarung,
ModSecurity-Aufrufreihenfolge, Event-Reason-Literal und NGINX-Return-Bedingung.
Ein explizites Header-Part-Advance entfernt den verschachtelten Zweig ohne
Änderung der Listeniteration.

Die Phase-4-Event-Konstruktion verwendet explizite Helper für Status,
Message-ID, Transport, Response-Start, Content-Type und begrenzten
Intervention-Identifier. `abort_connection`, `log_only`, `deny`, `redirect`
und andere Aktionen behalten ihre bisherigen Werte. Redirect- und Status-Pfade
sind getrennt, während der vorhandene eine Cleanup-Tail bleibt.

Alte Deferred-Work-Marker beschreiben jetzt korrektes Lifecycle-Verhalten. Es
wird keine Bedingung, Request-Methode, Response-Filter oder Runtime-Verhalten
eingeführt oder entfernt. Der Source-Contract-Test extrahiert das Access-Event
jetzt über den balancierten Funktionsscope statt über die frühere Nachbarschaft
zum Handler, damit die Metadaten-only-Logging-Assertion bei zusätzlichen
Helpern stabil bleibt.

## Akzeptanzkriterien

- Jedes aufgeführte NGINX-Sonar-Issue wird durch Source-Änderung ohne
  Suppression, Policy-, Exclusion-, Quality-Gate- oder Scanner-Änderung
  entfernt.
- Connection-, URI-, Request-Header-, Request-Body-, Phase-4-Event-,
  Redirect- und Status-Intervention-Pfade behalten Aufrufreihenfolge und
  Returns.
- Direkte NGINX-Common-Adoption- und C-Standard-Wiring-Controls bestehen.
- Der exakte künftige PR-Head zeigt null neue SonarQube-Cloud-Issues und `0.0%`
  New-Code-Duplizierung.

## Geänderte Dateien

- `connectors/nginx/src/ngx_http_modsecurity_access.c`
- `connectors/nginx/src/ngx_http_modsecurity_body_filter.c`
- `connectors/nginx/src/ngx_http_modsecurity_header_filter.c`
- `connectors/nginx/src/ngx_http_modsecurity_module.c`
- `ci/checks/connectors/nginx/check-nginx-common-adoption.py`
- dieses englisch/deutsche Change-Record-Paar und seine Indizes

## Ausgeführte Befehle

| Befehl oder Control | Ergebnis |
| --- | --- |
| `make check-nginx-common-adoption` | bestanden; Mapper-, Phase-3/4-Event-, begrenzte Rule-ID- und Response-Body-Controls bleiben geprüft. |
| `make check-nginx-c-standard-wiring` | bestanden; C17 bleibt verpflichtend und die Source-Liste ist vollständig. |
| `make check-nginx-c17-lint` | Wiring-/Lint-Control bestanden und native Übersetzung ohne NGINX-Header/Source korrekt als blockiert gemeldet. |
| Natives `make check-nginx-c17` | `blocked_external_dependency`: Im isolierten Task fehlen NGINX- und libmodsecurity-Header. Hash-geprüfte task-lokale Provisionierung lieferte keine Header; kein fremder Cache und keine globale Installation wurden verwendet. |
| `git diff --check` | bestanden. |

## Security-Auswirkung

Die Änderung refaktoriert HTTP-Request-, Response- und Intervention-Handling,
führt aber keinen neuen Input-, File-, Network-, Subprocess-, Authorization-
oder Logging-Data-Pfad ein. Jeder ModSecurity-Phase-Aufruf behält Phase-Marker
und PCRE-Paarung. Connection-/URI-/Body-Event-Reasons, Redirect-Allocation,
`Location`-Konstruktion, Status-Update, Header-sent-Rejection, einzelner
Cleanup-Tail und metadata-only-Phase-4-Mapping bleiben unverändert. Vor
Delivery ist ein fokussierter Exact-Diff-Security-Review erforderlich.

## Runtime-Evidence

Keine NGINX-Runtime oder native C17-Translation-Unit-Compilation lief. Der
dedizierte Control blockierte korrekt vor der Übersetzung, weil NGINX-/
libmodsecurity-Header nicht verfügbar sind; die begrenzte task-lokale
Provisionierung stellte sie nicht bereit.

## Bekannte Einschränkungen

Source-Contracts sind der stärkste lokale Control, ersetzen aber weder einen
gehosteten Exact-Head-C17-Build noch eine SonarQube-Cloud-Reanalyse. Der
repositoryweite Dokumentations-Control sieht außerdem bestehende fehlende
Framework-Submodul-Link-Targets in diesem isolierten Worktree; nach den
erforderlichen Abschnitten meldet er keinen weiteren geänderten Record-Fehler.

## Verbleibende Risiken

Der finale Security-Diff-Review, Exact-Head-Hosted-Checks, SonarQube-Cloud-
Issue-Readback und das New-Code-Duplikat-Ergebnis stehen noch aus. Dieser
Record beansprucht keine Review-Freigabe, keinen Merge und keinen
Resulting-Master-Status.

## Nicht ausgeführte Prüfungen mit Begründung

- Keine NGINX-Runtime und keine native C17-Translation-Unit-Compilation liefen,
  weil erforderliche NGINX-/libmodsecurity-Header im task-lokalen Environment
  fehlen und Provisionierung sie nicht bereitstellte.
- Hosted GitHub Actions, SonarQube Cloud, Review, Freigabe, Merge und
  Master-Checks können erst laufen, wenn der exakte Draft-PR-Head existiert.

## Delivery-Status

Draft-PR [#206](https://github.com/Easton97-Jens/ModSecurity-conector/pull/206)
existiert gegen `master`. Sein initialer Source-Head war
`33d05fd3d2acf3db792b350cefe22c937cdc2377`; lokaler, Remote- und GitHub-Head
stimmten überein, alle beobachteten erforderlichen Checks waren terminal ohne
Fehler, das Quality Gate war `OK`, und SonarQube Cloud meldete null
OPEN/CONFIRMED-PR-Issues, null neue Issues und `0.0%` New-Code-Duplizierung.
Dieses Delivery-Status-Update erzeugt einen neuen exakten PR-Head, der frische
Hosted- und Sonar-Verifikation erhalten muss, bevor der PR als verifiziert
gelten kann. Kein Merge und keine Master-Aktion sind autorisiert oder impliziert.

## Finaler Diff- und Review-Status

Der lokale Source-Diff bestand Whitespace-, NGINX-Common-Adoption-, C-Standard-
Wiring- und C17-Lint-Controls. Ein fokussierter Security-Review fand keinen
plausiblen diff-eingeführten Kandidaten. Native C17-Compilation bleibt wie oben
beschrieben blockiert. Der initiale PR-Head bestand Hosted-Checks und exakten
Sonar-Readback; dieses dokumentations-only Update verlangt dieselben Controls
für seinen neuen exakten Head. Kein Master-Claim wird erhoben.
