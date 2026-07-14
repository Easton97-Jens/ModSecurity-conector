# Change Record: NGINX-URL-Eigentümerschaft der Intervention und natives Cleanup

**Sprache:** [English](CR-20260713-nginx-intervention-url-ownership.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Titel | NGINX-URL-Eigentümerschaft der Intervention und natives Cleanup |
| Change-ID | CR-20260713-nginx-intervention-url-ownership |
| Datum (UTC) | 2026-07-14T07:56:59Z |
| Autor oder ausführender Agent | Codex-Agent <code>/root</code> |
| Basis-Revision | 0fec00442b0031c206b627a44735f1eb07534d51 |
| Zugehöriges Issue oder Pull Request | None; bestätigtes Finding im Task-Anhang |
| Schweregrad | Im bereitgestellten Finding-Material nicht angegeben (bestätigt) |
| Finale Revision | Nicht committed |

## Motivation und Problemstellung

Nur das bestätigte Finding beheben: „NGINX retains a borrowed intervention URL
and does not clean native intervention completely.“ Das bereitgestellte Finding
benennt <code>connectors/nginx/src/ngx_http_modsecurity_module.c</code>. Die
betroffene Funktion war vor diesem Fix gegenüber der Scan-Revision
<code>056f93232c6f5dba132bfb2204d96ce49707507b</code> unverändert.

Der frühere Redirect-Pfad speicherte den nativen
<code>intervention.url</code>-Zeiger direkt im NGINX-Header
<code>Location</code>, während die native Intervention nicht vollständig
bereinigt wurde. Cleanup nach dieser Zuweisung würde einen hängenden
Header-Zeiger hinterlassen; fehlendes Cleanup behielt native Ressourcen. Es
wurde kein versionierter Report oder Schweregrad bereitgestellt; dieser Record
hält diese Tatsache fest.

## Betroffene Komponenten und Sicherheitsgrenzen

Die Änderung beschränkt sich auf die NGINX-Intervention-Bridge, einen
fokussierten Production-Source-Contract-Test und dieses englisch-deutsche
Change-Record-Paar. Die Sicherheitsgrenze liegt zwischen nativem
libmodsecurity-Intervention-Speicher und NGINX-Request-Pool-Speicher: native
<code>url</code>- und <code>log</code>-Werte sind temporär und werden durch
<code>msc_intervention_cleanup</code> freigegeben; der ausgegebene Header muss
auf Speicher aus <code>r-&gt;pool</code> zeigen.

Keine Framework-Quelle oder kein Framework-Submodule-Pointer, kein anderer
Connector, kein Workflow, kein Konfigurationsdefault und kein Runtime-Fixture
wurden geändert. Temporäre Header-Quellen und Compile-Objekte blieben unter
<code>/var/tmp/codex/ModSecurity-conector</code> und sind nicht versioniert.

## Akzeptanzkriterien

| Kriterium | Status | Evidenz |
| --- | --- | --- |
| Ein Redirect-Header behält keinen geliehenen nativen URL-Zeiger | Erfüllt | URL wird geprüft, kopiert und in <code>r-&gt;pool</code> NUL-terminiert, bevor der Header gesetzt wird; fokussierter Contract-Test besteht. |
| Natives Intervention-Cleanup läuft auf jedem Funktionsausgang genau einmal | Erfüllt | Vollständige Nullinitialisierung, ein Cleanup-Label, ein Cleanup-Aufruf und ein Return; fokussierter Contract-Test und unabhängiges Review bestehen. |
| Überlauf- und Allocation-Fehler sind deterministisch | Erfüllt | Überlauf, Request-Pool-Allocation und Header-List-Allocation liefern <code>NGX_HTTP_INTERNAL_SERVER_ERROR</code> und erreichen Cleanup. |
| Gültige Redirects und Nicht-Redirect-Status behalten ihr Verhalten | Erfüllt | Nichtleere URLs behalten den Intervention-Status; Nicht-Redirect-Statusverarbeitung bleibt erhalten; C17-Kompilierung und Source-Contract bestehen. |
| Leere oder fehlende URLs erzeugen keinen leeren oder geliehenen Location-Header | Erfüllt | Redirect-Behandlung verlangt eine nichtleere URL; normale Statusbehandlung und Cleanup bleiben aktiv. |
| Geforderte statische Verifikation ist real und abgegrenzt | Erfüllt | Fokussierter Test, echte NGINX/Common-C17-Kompilierung mit <code>-Werror</code>, NGINX-Checks, CI-Modus-Lint und Quick-Check bestehen. |

## Untersuchte Alternativen

- Die geliehene URL behalten und Cleanup verzögern. Verworfen, weil der Header
  während der NGINX-Request lebt, nicht während des nativen Intervention-Records.
- Nur die URL kopieren und das direkte
  <code>free(intervention.log)</code> behalten. Verworfen, weil Ownership
  aufgeteilt bliebe und vollständigem nativen Cleanup widerspräche.
- Einen Header ohne Allocation-Prüfungen anlegen. Verworfen, weil
  Intervention-Fehler deterministisch sein und native Ressourcen freigeben
  müssen.
- Einen NGINX-Runtime-/Lifecycle-Test ausführen. Nicht gewählt: keine geeignete
  Host-Umgebung war vorhanden, und der Task erlaubt dies nur dann.

## Implementierungsentscheidung und Begründung

Die Intervention-Struktur wird vollständig genullt und ihr Status auf
<code>200</code> gesetzt. Jeder Ausgang läuft durch ein
<code>cleanup</code>-Label, das
<code>msc_intervention_cleanup(&amp;intervention)</code> genau einmal aufruft
und das gewählte Ergebnis zurückgibt. Der Missing-Context-Pfad nutzt dieses
Cleanup ebenfalls; sein Record ist sicher nullinitialisiert und es erfolgte
noch keine native Abfrage.

Für eine nichtleere Redirect-URL bestimmt der Code die Länge, lehnt einen
Überlauf der Allocation für das Terminierungsbyte ab, allokiert
<code>length + 1</code> Bytes aus <code>r-&gt;pool</code>, kopiert und
NUL-terminiert die URL und erstellt sowie veröffentlicht danach den NGINX-Header
<code>Location</code>. Ein alter Location-Header wird erst nach erfolgreicher
Header-List-Allocation bereinigt. Natives Cleanup erfolgt erst, nachdem die
Request-Pool-Kopie zum Header-Wert wurde.

<code>url == ""</code> gilt als kein Redirect: Es wird kein leerer
Location-Header angelegt und der normale Intervention-Statuspfad verwendet.
Dies ändert keinen gültigen Redirect, der ein nichtleeres Ziel braucht.

## Geänderte Dateien

- <code>connectors/nginx/src/ngx_http_modsecurity_module.c</code>
- <code>tests/test_nginx_intervention_url_ownership.py</code>
- <code>reports/audits/change-records/CR-20260713-nginx-intervention-url-ownership.md</code>
- <code>reports/audits/change-records/CR-20260713-nginx-intervention-url-ownership.de.md</code>

Keine Framework-Submodule-Datei und kein Pointer wurden geändert. Temporäre
Quellen, konfigurierte NGINX-Header, Compile-Objekte und Logs sind nur lokal
und unversioniert.

## Hinzugefügte oder geänderte Tests

<code>tests/test_nginx_intervention_url_ownership.py</code> wurde hinzugefügt.
Er parst die Produktionsfunktion
<code>ngx_http_modsecurity_process_intervention</code> und prüft vollständige
Nullinitialisierung, genau ein Cleanup und Return, Entfernung des direkten
Log-Free, eine Request-Pool-URL-Kopie vor Cleanup, NUL-Terminierung, keine
geliehene URL-Zuweisung, Überlaufschutz und Cleanup-Routing bei fehlendem
Context/fehlender Konfiguration, gesendeten Headern und beiden Allocation-Fehlern.
Er ist ein Production-Source-Contract-Test, keine Ersatz-NGINX-Implementierung.

## Ausgeführte Befehle

<code>$TASK_ROOT</code> bezeichnet
<code>/var/tmp/codex/ModSecurity-conector/tmp/task.nginx-intervention.ZzgRxQ</code>.
Kein Befehl erzeugte ein kanonisches Runtime-Evidence-Artefakt.

| Exakter Befehl | Exit-Code oder Ergebnis | Sanitisierte relevante Zusammenfassung | Kanonischer Evidence-Pfad | Run-ID |
| --- | --- | --- | --- | --- |
| <code>rtk proxy git diff 056f93232c6f5dba132bfb2204d96ce49707507b..HEAD -- connectors/nginx/src/ngx_http_modsecurity_module.c</code> | 0 | Zielquelle war vor dem Fix gegenüber der bereitgestellten Scan-Revision unverändert. | None | None |
| <code>rtk proxy env ... PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_nginx_intervention_url_ownership</code> | 1, vor Fix | Sieben erwartete Assertions schlugen gegen die frühere Borrowed-Pointer-/unvollständige-Cleanup-Implementierung fehl. | None | None |
| <code>rtk proxy env VERIFIED_RUN_ROOT=$TASK_ROOT RUNNER_TEMP=$TASK_ROOT SOURCE_ROOT=$TASK_ROOT/sources MODSECURITY_V3_SOURCE_DIR=$TASK_ROOT/sources/ModSecurity_V3 sh modules/ModSecurity-test-Framework/ci/provisioning/fetch-smoke-sources.sh v3</code> | 0 | Temporäre libmodsecurity-Header nur für Kompilierung geholt; keine Runtime gebaut oder ausgeführt. | None | None |
| <code>rtk proxy env TMPDIR=$TASK_ROOT/tmp ./auto/configure --with-compat</code> im temporären NGINX-Quellcode <code>release-1.31.2</code> | 0 | Nur NGINX-Konfigurationsheader erzeugt; kein NGINX-Binary gebaut oder gestartet. | None | None |
| <code>rtk proxy env ... make check-nginx-c17</code> | 2 (unterliegender Check 77), vor Header-Vorbereitung | Erwartungsgemäß blockiert, weil NGINX-Header/Quellcode fehlten. | None | None |
| <code>rtk proxy env ... MODSECURITY_INCLUDE_DIR=$TASK_ROOT/sources/ModSecurity_V3/headers NGINX_SOURCE_DIR=$TASK_ROOT/sources/nginx-1.31.2 make check-nginx-c17</code> | 0 | Alle gelisteten NGINX/Common-Units unter C17 mit <code>-Wall -Wextra -Werror</code> kompiliert. | <code>$TASK_ROOT/build/nginx-c-standards/</code> | None |
| <code>rtk proxy env ... PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_nginx_intervention_url_ownership</code> | 0 | Drei fokussierte Ownership-, Cleanup- und Failure-Path-Contract-Tests bestanden. | None | None |
| <code>rtk proxy env ... make check-nginx-common-adoption</code> | 0 | NGINX-Common-Adoption-Strukturchecks bestanden. | None | None |
| <code>rtk proxy env ... make check-nginx-c-standard-wiring</code> | 0 | NGINX-C-Standard-Target-/Source-Wiring-Checks bestanden. | None | None |
| <code>rtk proxy env ... MODSECURITY_INCLUDE_DIR=$TASK_ROOT/sources/ModSecurity_V3/headers NGINX_SOURCE_DIR=$TASK_ROOT/sources/nginx-1.31.2 make check-nginx-c17-lint</code> | 0 | Lint-integrierte NGINX-C17-Kompilierung mit vorbereiteten Headern bestanden. | <code>$TASK_ROOT/build/nginx-c-standards/</code> | None |
| <code>rtk proxy env ... make lint</code> | 130 | Angehalten, als ein fremder Apache-Check lokale Runtime-Provisionierung begann; sein task-lokaler Cache wurde entfernt. | None | None |
| <code>rtk proxy env CI=true ... make lint</code> | 0 | Vollständiger statischer Lint bestand; nicht verfügbare Apache-/HAProxy-Host-C17-Checks wurden übersprungen statt provisioniert. | None | None |
| <code>rtk proxy env CI=true ... make quick-check</code> | 0 | Quick-Check bestand, einschließlich Lint, Framework-Python-Kompilierung und Whitespace-Checks. | None | None |
| <code>rtk proxy env ... make check-bilingual-docs</code> im Hauptarbeitsbaum | 2 | Durch fremde ungetrackte <code>docs/decisions/</code>-Dateien mit fehlenden lokalen Link-Zielen blockiert; keine Task-Datei wurde dafür geändert. | None | None |
| <code>rtk proxy env ... make check-bilingual-docs &amp;&amp; make check-doc-links</code> in einem sauberen temporären Git-Worktree mit versioniertem Basisstand und diesem Record-Paar | 0 | Prüfungen des zweisprachigen Paars und der Dokumentlinks bestanden für den versionierten Basisstand plus diese Änderung. | None | None |
| <code>rtk proxy git diff --check &amp;&amp; git diff --check -- connectors/nginx/src/ngx_http_modsecurity_module.c &amp;&amp; git diff --submodule=log -- modules/ModSecurity-test-Framework</code> | 0 | Vollständige getrackte und abgegrenzte Whitespace-Checks bestanden; kein Framework-Submodule-Diff lag vor. | None | None |

## Security-Auswirkung

Der Redirect-Header überschreitet die Ownership-Grenze jetzt durch Kopieren der
nativen URL in NGINX-Request-Pool-Speicher vor dem nativen Cleanup. Die
Intervention wird an einer Stelle freigegeben, beseitigt behaltene native
URL-/Log-Allocations und vermeidet einen durch Cleanup verursachten hängenden
Location-Zeiger. Es gibt kein separates direktes
<code>free(intervention.log)</code>. Überlauf- und Allocation-Fehler liefern
nach Cleanup einen Internal-Server-Status statt einen teilweise initialisierten
Redirect offenzulegen.

## Dokumentationsänderungen

Dieses englisch-deutsche Change-Record-Paar wurde hinzugefügt. Kein
Connector-Guide wurde geändert: Es gibt keine benutzerseitige Konfiguration,
Direktive oder unterstützte Runtime-Verhaltensänderung über diesen
implementierungsnahen Security-Fix hinaus.

## Runtime-Evidence

Für diese Änderung wurde keine Runtime-Evidence erhoben oder beansprucht. Der
temporäre NGINX-Quellcode wurde nur konfiguriert, um Header für den
C17-Compile-Check bereitzustellen; es wurden kein NGINX-Server, kein
Request-Lifecycle, keine Allocation-Fehlerinjektion und keine Redirect-Response
ausgeführt.

## Bekannte Einschränkungen

- Der fokussierte Test ist ein statischer Contract über die Produktions-C-Funktion.
  Er kann weder die Live-Lebensdauer des NGINX-Request-Pools beweisen noch einen
  echten <code>ngx_pnalloc</code>-Fehler erzwingen.
- Temporäre Header ermöglichen Kompilierung, sind aber kein gelinktes Modul,
  kein Host-Lifecycle und kein Runtime-Kompatibilitätsergebnis.
- Das bereitgestellte Finding-Material hatte keinen versionierten Report und
  keinen Schweregrad.

## Verbleibende Risiken

- Eine künftige Änderung des libmodsecurity-Ownership-Contracts erfordert eine
  erneute Validierung dieser Bridge. Die Implementierung begrenzt native Zeiger
  auf das Intervall vor dem einzigen Cleanup-Aufruf.
- Ein Live-NGINX-Integrationstest könnte host-spezifisches Verhalten zeigen,
  das der Source-Contract nicht abbildet. Dies wird durch Kompilieren des
  tatsächlichen NGINX-Moduls gegen konfigurierte NGINX-Header gemindert, ohne
  einen Runtime-Claim zu machen.

## Nicht ausgeführte Prüfungen mit Begründung

- NGINX-Runtime-/Lifecycle- und echte Allocation-Fehler-Tests wurden nicht
  ausgeführt, weil keine geeignete Host-Umgebung vorhanden war und der Task sie
  nur dann autorisiert. Es wurde kein Server installiert, gebaut oder gestartet.
- Optionale C23-/Future-C-NGINX-Checks, Sanitizer und nicht zugehörige
  Security-Scans wurden nicht ausgeführt, weil das bestätigte Finding auf den
  geforderten C17-Pfad begrenzt ist und der User keine Umfangserweiterung wünscht.
- Kein Framework-Fixture/-Source änderte sich: Das vorhandene Redirect-Fixture
  beobachtet Location nicht und kann diese Eigenschaft ohne verbotene
  Framework-Änderungen nicht beweisen.

## Finaler Diff- und Review-Status

Der fokussierte Test, die echte C17-Kompilierung, NGINX-Adoption-/Wiring-Checks,
CI-Modus-Lint und Quick-Check bestehen. Der direkte Dokumentationscheck im
Hauptarbeitsbaum ist durch fremde ungetrackte Dokumentation blockiert; dieselben
zweisprachigen und Link-Checks bestehen in einem sauberen temporären Git-
Worktree mit versioniertem Basisstand und diesem Record-Paar. Die finalen
vollständigen getrackten und abgegrenzten Whitespace-Checks bestehen; Framework-
Submodule-Diff und sein Worktree-Status sind leer. Ein unabhängiges Read-only-
Review fand keinen blockierenden Ownership-, Cleanup-, C-Kompatibilitäts- oder
Verhaltensregressionsbefund und bestätigte das Leere-URL-Verhalten als sichere
deterministische Verfeinerung. Der finale Status enthält außerdem fremde
User-Änderungen in <code>Makefile</code>, <code>ci/checks/analysis/</code> und
<code>docs/</code>; sie wurden weder zur Änderung inspiziert noch verändert.
Das beabsichtigte Ergebnis ist <code>fixed</code>. Es wurde kein Commit oder
Pull Request erstellt.
