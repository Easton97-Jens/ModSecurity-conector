# Change Record: Parent-Apache/NGINX-Bereinigung auskommentierten Codes für SonarQube Cloud C:S125

**Sprache:** [English](CR-20260727-sonar-c-commented-code-cleanup.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260727-sonar-c-commented-code-cleanup` |
| Datum (UTC) | `2026-07-27` |
| Basis-Revision | `1b0f8825f3510b99b603bb6cd6f0777e1710358e` |
| Tracking | Parent-SonarQube-Cloud-`c:S125`-Code-Smells `AZ4114xeBrFcw9uE-s22`, `AZ4114yYBrFcw9uE-s3E`, `AZ4114y-BrFcw9uE-s3S`, `AZ4114yiBrFcw9uE-s3F`, `AZ43WgS3BO_6kV5uFeJy` und `AZ43WgS3BO_6kV5uFeJz`. |
| Grenze | Nur fünf Parent-Apache/NGINX-Quelldateien, dieses englisch/deutsche Change-Record-Paar und seine gepaarten Indizes. Framework- und MRTS-Quelltext, Gitlinks, Workflow, Scanner-Konfiguration, Quality Gates, Suppressions und externer Sonar-Issue-Status bleiben unverändert. |
| Delivery-Status | Nur lokaler Kandidat. Es gab keinen Commit, Push, Pull Request, keine gehostete CI, keine SonarQube-Cloud-PR-Analyse, kein Review, keinen Merge und kein Default-Branch-Update. |

## Motivation und Problemstellung

Die sechs Receipt-gestützten `c:S125`-Befunde kennzeichnen deaktivierte Makro-,
Guard-, Zuweisungs- und Initialisierungslisten-Kommentare im Parent-
Apache/NGINX-Quelltext. Sie belegen keinen Runtime-Defekt. Ihr Verbleib
erschwert die Unterscheidung zwischen aktuellem Verhalten und altem,
absichtlich inaktivem Verhalten an Request-Method-, Response-Framing- und
Konfigurationsinitialisierungsgrenzen.

## Akzeptanzkriterien

- Nur die sechs Receipt-gestützten Kommentare an den auditierten Parent-Stellen
  entfernen oder umformulieren.
- Keinen GET/POST/HEAD-Guard, keine Content-Length-Umschreibung und keinen
  Konfigurationsinitialisierungspfad aktivieren.
- HTTP-Method-Forwarding, bestehendes Response-Framing und aktive
  `NGX_CONF_UNSET*`-Merge-Sentinel-Initialisierung bewahren.
- Die bestehenden Apache/NGINX-Common-Adoption- und
  C-Standard-Wiring-Prüfungen bestehen lassen.
- Normale C17-Evidence bei fehlenden Host-SDK-Voraussetzungen wahrheitsgemäß
  als `blocked_environment` erfassen, ohne lokale Provisionierung auszulösen.
- Dieses vollständige englisch/deutsche Change-Record-Paar und seine Indizes
  pflegen.

## Implementierungsentscheidung und Begründung

Der Patch löscht das inaktive `REQUEST_EARLY`-Makro, die Receipt-gestützten
Method-Guard-Kommentare in Access- und Log-Handler sowie die deaktivierte
Content-Length-Zuweisung. Die Header-Filter-Erklärung wird durch eine aktuelle
Aussage ersetzt, dass der Filter die bestehende Content-Length bewahrt und das
Response-Framing nicht umschreibt. Die zwei wie Zuweisungen aussehenden
`ngx_pcalloc()`-Listen werden durch Prosa ersetzt, die die tatsächliche
Nullinitialisierung und die nachfolgenden aktiven NGINX-Sentinel-Zuweisungen
beschreibt.

Ein separater, nicht zu einem Receipt gehörender deaktivierter Method-Guard in
`connectors/nginx/src/ngx_http_modsecurity_access.c:403-415` bleibt
unverändert. Die Änderung modifiziert keine Präprozessorbedingung, keine
ausführbare Anweisung, keinen Request-/Response-Flow, keinen
Konfigurationswert und keine ABI.

## Geänderte Dateien

- `connectors/apache/src/mod_security3.h`
- `connectors/nginx/src/ngx_http_modsecurity_access.c`
- `connectors/nginx/src/ngx_http_modsecurity_header_filter.c`
- `connectors/nginx/src/ngx_http_modsecurity_log.c`
- `connectors/nginx/src/ngx_http_modsecurity_module.c`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- `reports/audits/change-records/CR-20260727-sonar-c-commented-code-cleanup.md`
- `reports/audits/change-records/CR-20260727-sonar-c-commented-code-cleanup.de.md`

## Ausgeführte Befehle

| Befehl oder Evidence | Ergebnis |
| --- | --- |
| `rtk proxy git -C <candidate> submodule update --init --checkout modules/ModSecurity-test-Framework` | als read-only Test-/Dokumentationsabhängigkeits-Checkout beim Parent-verzeichneten `47e50e7bc43ba7a3b5bad1a9448111794f664cc0` bestanden; Framework-Quelltext blieb sauber und verschachteltes MRTS blieb uninitialisiert. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-apache-common-adoption check-nginx-common-adoption` | bestanden. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-apache-c-standard-wiring check-nginx-c-standard-wiring` | bestanden. |
| `rtk proxy env CI=true PYTHONDONTWRITEBYTECODE=1 APACHE_C_STANDARDS_OUT=<task-owned external root> BUILD_ROOT=<task-owned external root> CC=cc make check-apache-c17` | blocked_environment: Die zugrunde liegende Prüfung gab wegen fehlendem `apxs`/`apxs2` `77` zurück; `make` gab `2` zurück und kein C-Quelltext wurde kompiliert. |
| `rtk proxy env CI=true PYTHONDONTWRITEBYTECODE=1 BUILD_ROOT=<task-owned external root> CC=cc make check-nginx-c17` | blocked_environment: Die zugrunde liegende Prüfung gab wegen fehlender NGINX-Header/-Quellen `77` zurück; `make` gab `2` zurück und kein C-Quelltext wurde kompiliert. |
| Dieselben zwei C17-Prüfungen mit `CC=clang` | Für dieselben fehlenden Apache- und NGINX-Host-Voraussetzungen blocked_environment; Clang `21.1.8` war vorhanden, aber kein Quelltext wurde kompiliert. |
| `rtk proxy git diff --check` | nach der vollständigen Prüfung des getrackten Source-/Index-Diffs bestanden; nach dieser finalen Record-Textaktualisierung wird die Prüfung noch einmal ausgeführt. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs check-doc-links` | bestanden: `bilingual docs ok`, `repository path references: PASS` und `doc links ok`. |

## Security-Auswirkung

Sicherheitsklassifikation: `not_applicable` als Sicherheitsbefund. Der Patch
ändert keine ausführbare Kontrolle, keine angreiferkontrollierte Eingabe,
keinen Sink, keine Autorisierung, keinen Parser und kein
Memory-Management-Verhalten. Die angrenzenden Protokollinvarianten wurden
dennoch geprüft: Kein HTTP-Method-Guard wird reaktiviert, keine Response-
Content-Length wird umgeschrieben und die aktive NGINX-Merge-Sentinel-
Initialisierung bleibt unverändert. Der verbleibende deaktivierte Nicht-
Receipt-Guard wird ausdrücklich erhalten, nicht stillschweigend verändert.

## Runtime-Evidence

Es wurde keine Apache-, NGINX-, Connector-, CRS-, MRTS- oder Netzwerk-Runtime
ausgeführt. Dies ist eine reine Quelltext-Kommentarbereinigung; die
bestandenen Adoption- und Wiring-Prüfungen sind strukturelle Evidence, keine
Runtime-Evidence.

## Bekannte Einschränkungen

Beide normalen C17-Befehlspfade sind wegen fehlender Host-SDK-Voraussetzungen
`blocked_environment`. `CI=true` wurde ausschließlich übergeben, um den
Apache-Scriptversuch einer nicht autorisierten lokalen Runtime-Provisionierung
zu verhindern; dadurch werden die blockierten Prüfungen nicht bestanden. Eine
SonarQube-Cloud-Analyse auf einem exakten ausgelieferten Head bleibt nötig,
bevor die sechs externen Issue-Keys als behoben gelten können.

## Verbleibende Risiken

Das Restrisiko betrifft Dokumentations-/Historienklarheit, keine
Verhaltensänderung: Ein zukünftiger Maintainer könnte die entfernten
historischen Snippets als ausgelassene Funktion missverstehen. Die knappe
aktuelle Prosa hält das laufende Framing- und Initialisierungsverhalten fest,
während der Change Record den exakten Receipt-Umfang und die Begründung für
inaktive Kontrollen erhält.

## Nicht ausgeführte Prüfungen mit Begründung

Keine Runtime-Matrix, kein Connector-Build, kein Sanitizer und kein gehosteter
Check wurden ausgeführt, weil der Patch kein ausführbares Verhalten ändert und
die C17-Host-Voraussetzungen fehlen. Es wurde keine Framework- oder MRTS-
Quellprüfung ausgewählt: Framework diente nur beim Parent-verzeichneten
Gitlink als Dokumentations-/Testabhängigkeit und MRTS blieb uninitialisiert.

## Finaler Diff- und Review-Status

Der Kandidat ist lokal und uncommittet. Sein geprüfter Quelltext-Diff ist auf
die sechs Receipt-gestützten Kommentaränderungen in fünf Parent-Dateien
begrenzt; dieses Paar und die zwei Indizes liefern Nachvollziehbarkeit. Die
Dokumentationsvalidierung und die finale Prüfung des getrackten Diffs
bestanden. Es wird kein externer Delivery- oder SonarQube-Cloud-Issue-Status
behauptet.
