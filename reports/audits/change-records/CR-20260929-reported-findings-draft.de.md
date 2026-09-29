# Change Record: Entwurf zu gemeldeten Findings

**Sprache:** [English](CR-20260929-reported-findings-draft.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260929-reported-findings-draft` |
| Datum (UTC) | 2026-09-29 |
| Basis-Revision | `d56af0856507eb048987974d3960e301e7c24371` |
| Zuerst veröffentlichter Head | `b7022654c5b392cb94ea60ad031350a1d18dfd70` |
| Lieferziel | Parent-Draft-PR #392; kein Merge |
| Umfang | B09, B13 und C07; nicht der gesamte Findingbestand |

## Motivation und Problemstellung

Dieser Draft enthält drei begrenzte Änderungen aus den gelieferten Befunden.
Er wurde zuerst als ausdrücklich ungetesteter lokaler Patch vorbereitet und
anschließend als PR #392 veröffentlicht. Aussagen über fehlende Veröffentlichung
im Vorbereitungspaket beziehen sich auf diese historische Vorbereitungsphase,
nicht auf den aktuellen PR.

Am zuerst veröffentlichten Head erreichte quick-check den check-bilingual-docs
und scheiterte an fehlenden Sprachschaltern, Identitätsfeldern und Abschnittsnamen
dieses Record-Paars. Die reine Dokumentationskorrektur stellt den vorhandenen
Vertrag wieder her, ohne Checker, Produktcode oder Testassertionen zu ändern.

## Akzeptanzkriterien

- B13: Original-URI am inklusiven Headerwertlimit mit Platz für NUL akzeptieren;
  vorhandene ungültige maßgebliche Metadaten vor Common ablehnen, statt
  stillschweigend ein anderes Ziel zu prüfen.
- B09: Positive NGINX-Interventionen bleiben bei Fehlerseiten aktiv; negative
  Ergebnisse und die bestehende Behandlung inaktiver Ergebnisse erhalten.
- C07: Den Deny-Wunsch der Engine erhalten, aber den unverändert ausgelieferten
  Response im OFF-Modus mit log_only und ursprünglichem sichtbaren Status erfassen.
- Fehler beim Erfassen der Hostaktion ausdrücklich weitergeben.
- Fokussierte und bestehende Regressionen sowie unterstützte native Builds ausführen.
- Vor Verifikation oder Abschluss das ursprüngliche Fehlerszenario und die
  legitime Kontrolle am echten Host belegen; ein grüner Dokumentationscheck genügt nicht.

## Implementierungsentscheidung und Begründung

- B13 (`csf_d60ac4261fdf382b0cdc51bf`): Headerwertmaximum plus ein NUL-Byte
  für den Original-URI-Puffer reservieren. Ein vorhandener leerer, nicht mit /
  beginnender, zu großer, NUL-haltiger oder nicht kopierbarer maßgeblicher Wert
  ergibt einen Fehler statt eines anderen Headers oder /authorize. Der Aufrufer
  antwortet vor Common mit HTTP 400. Bei fehlenden Metadaten bleibt der Rückfall erhalten.
- B09 (`csf_110c7b683d38cd566861364f`): Eine positive Intervention bleibt auch
  bei einer Fehlerseite aktiv. Nur ein inaktives Ergebnis darf den bisherigen
  Bypass verwenden. Das ist enger als der unabhängige PR #391.
- C07 (Cloud-Finding `8d2cfdfbd7ac819198af08de2ec1a8d4`): Engineentscheidung
  im Stock-lighttpd-OFF-Zweig erhalten, aber Hostaktion log_only, ursprünglichen
  Status und Transportergebnis log_only erfassen. Aufzeichnungsfehler weitergeben
  statt bedingungslosen Erfolg zu melden. Dies behebt B07 nicht.

Die vorgeschlagenen Tests kompilieren tatsächliche isolierte B09-/B13-Helferkörper
mit minimalen Testtypen und untersuchen den B13-Aufrufer sowie den C07-OFF-Zweig.
Sie starten keinen vollständigen Parser, Proxy oder ModSecurity-Host. Fehlendes
cc überspringt kompilierte Checks, statt deren Erfolg zu beweisen. Diese
Dokumentationskorrektur lockert keine Testassertion.

## Geänderte Dateien

- `common/runtime/http_authorization_service.c`
- `connectors/nginx/src/ngx_http_modsecurity_common.h`
- `connectors/lighttpd/stock_sidecar/stock_sidecar.c`
- `tests/test_reported_security_regressions.py`
- Dieses englisch/deutsche Change-Record-Paar.

## Ausgeführte Befehle

| Verfahren | Beobachtetes Ergebnis und Einschränkung |
| --- | --- |
| Ursprüngliche lokale Patchvorbereitung | Kein Produkttest, Build oder Patch-Anwendbarkeitscheck ausgeführt |
| Veröffentlichungshilfe beim Nutzer | Der Veröffentlichungsnachweis nennt Anwendbarkeits-, Whitespace- und Datei-/SHA-Prüfungen; dies sind keine Produkttests |
| Ursprünglicher GitHub-Quick-Check | Run 36547346066, Job 109336805905, zugeordnet zu b7022654c5b392cb94ea60ad031350a1d18dfd70: bei check-bilingual-docs gescheitert |
| Dokumentationskorrektur | Geforderte Paarstruktur aus dem unveränderten Checker-Vertrag wiederhergestellt |
| Lokale Repositorytests und Builds bei Nachbesserung | NOT RUN: vorgeschriebenes RTK und provisionierte Checkout-/Hostumgebung fehlen |
| Aktuelle Head-CI nach Nachbesserung | Neue Ergebnisse ausstehend; durch diesen Record nicht zertifiziert |

Der ursprüngliche Quick-Check verwendete GitHubs PR-Merge-Checkout. Sein Fehler
wird nicht als erfolgreiche native Abnahme direkt am Head ausgegeben. Andere
abgeschlossene Prüfungen des alten Heads belegen keinen Erfolg am nächsten Head.

## Security-Auswirkung

Vorhandene ungültige URI-Metadaten führen absichtlich zu Ablehnung statt Rückfall.
Das Größenlimit des direkten Requestziels bleibt unverändert. Positive
B09-Klassifizierung und wahrheitsgemäße C07-Hostaktionen sind beabsichtigte
Securitykorrekturen, jedoch keine vollständige P2-/P4-Architekturreparatur.

Keine Änderung von Phase4-Default, Regeln, Dependency-Pins, Tokenrechten,
Scanner-Severity, bestehenden Quality Gates, Parent-Framework-Gitlink oder MRTS.

## Runtime-Evidence

Hier wird keine Live-Evidence des ursprünglichen Szenarios belegt. B13 benötigt
reale Proxygrenzfälle mit 8.191/8.192/8.193 Bytes sowie ungültige und fehlende
Metadaten als Kontrollen. B09 benötigt einen erlaubten Ursprungspfad und ein
regelbasiert abgelehntes Fehlerseitenziel einschließlich Contenthandler- und
Rekursionsbeobachtung. C07 benötigt getrennte Beobachtung von Upstream-/Clientstatus,
Body und Engine-/Hostereignissen bei explizitem OFF und fehlendem Standardwert.

Der separate lokale Framework-Testvorschlag ist kein Bestandteil dieses Parent-PRs.
Synthetische Normalizertests sind keine Host-Evidence und belegen nicht, dass
der tatsächliche Framework-PR #128 diese Tests implementiert.

## Bekannte Einschränkungen

Dieser PR ändert nur B09, B13 und C07. Er schließt weder den 59er-Bestand noch
implementiert er Endpunktauthentisierung, allgemeine Headerweitergabe oder
Zurückhalten von Responsebytes. B06/B07 bleiben offen. Die B09-Klassifizierung
allein beweist keinen rekursionssicheren vollständigen NGINX-Hostfix.

## Verbleibende Risiken

PR #391 ändert unabhängig den NGINX-Klassifizierer und den P2-Pfad. Überlappende
Änderungen dürfen nicht ohne geprüften Abgleich und neue Tests kombiniert werden.
Abgelehnte URI-Metadaten und Ereignis-Aufzeichnungsfehler benötigen die beschriebenen
negativen und legitimen Kontrollen. Unveränderte Findings bleiben offen.

## Nicht ausgeführte Prüfungen mit Begründung

Lokale Repositorytests, vollständige C-Übersetzungseinheiten, native Regressionen
und echte Proxy-/ModSecurity-Beobachtungen wurden in der Bearbeitungsumgebung
nicht ausgeführt. Vorgeschriebenes RTK und provisionierte Hostbuilds fehlen.
Strukturprüfungen der Veröffentlichungshilfe und spätere CI bleiben von diesen
fehlenden Laufzeittests getrennt. Keine ausgelassene, übersprungene oder ausstehende
Prüfung ist PASS.

## Finaler Diff- und Review-Status

Die erste CI-Nachbesserung ändert nur diese zwei Records und erhält Originalcode
sowie Regressionstests. Der PR bleibt bis zu neuen Prüfungen am aktuellen Head,
unabhängigem Review und erforderlicher nativer Abnahme ein Draft. Kein Finding
wird automatisch geschlossen oder als Risiko akzeptiert. Diese Korrektur führt
keinen Merge, Force-Push, anderen Branchwechsel, Submodulwechsel oder Veröffentlichung
von Roh-Securityreports aus.
