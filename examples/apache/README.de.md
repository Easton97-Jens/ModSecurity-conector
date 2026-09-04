# Apache-Beispiele für das native Modul

**Sprache:** [English](README.md) | Deutsch

## Integration und Grenze

Integrationsmodus: natives httpd-Modul. [Minimalreferenz](minimal/httpd.conf),
[Safe-Referenz](safe/httpd.conf), [Strict-Referenz](strict/httpd.conf) und
[vollständige Referenz](all/httpd.conf) wählen die native HTTP/1.1-P1--P4-
Konfigurationsform. P1 sind Request-Header, P2 Request-Body, P3 Response-
Header und P4 Response-Body. Die vollständige Referenz verwendet den
existierenden parsergültigen Wert `strict`; `all` ist ein Beispiel-Layout und
kein vierter Wert für `modsecurity_phase4_mode`.

Die vollständige Datei lässt beide Host-Korrelationsüberschreibungen bewusst
inaktiv. Common erzeugt die kanonische Transaktions-ID eindeutig; eine externe
Host-ID darf erst nach dem Nachweis aktiviert werden, dass sie eindeutig und
nicht request-abgeleitet ist.

Apache folgt dem gemeinsamen progressiven Phase-4-Vertrag: Es hängt jeden
Response-Daten-Bucket genau einmal an libmodsecurity an und leitet diesen
Bucket anschließend ohne Warten auf EOS an den nächsten Apache-Filter weiter.
Nur das terminale EOS-Fragment bleibt lange genug erhalten, um die Response-
Body-Verarbeitung abzuschließen und die eine finale Entscheidung aufzulösen.
Das verspricht keine Regelentscheidung pro Chunk. Nach einer committed
Response zeichnet Safe ein disruptives Ergebnis als <code>log_only</code> auf
und setzt fort; Strict verwendet den nativen Connection-Abort-Pfad. Die
[Strict-Profilgrenze](#strict-profilgrenze) behauptet kein client-sichtbares
Abbruchergebnis, bevor ein Host-Runtime-Test eines beobachtet.

## Dateien

| Pfad | Typ | Zweck |
| --- | --- | --- |
| [minimal/httpd.conf](minimal/httpd.conf) | Host-Konfiguration | Begrenzter nativer P1--P4-Minimalstart. |
| [safe/httpd.conf](safe/httpd.conf) | Host-Konfiguration | Begrenzte native P1--P4-Safe-Referenz. |
| [strict/httpd.conf](strict/httpd.conf) | Host-Konfiguration | Parserunterstützter Strict-Fallback ohne Behauptung eines client-sichtbaren späten Abbruchs. |
| [all/httpd.conf](all/httpd.conf) | Host-Konfiguration | Vollständige quellenbasierte Parameterreferenz; sie wählt gültiges `strict`, nicht den Phase-4-Modus `all`. |
| [detection-only/httpd.conf](detection-only/httpd.conf) | Host-Konfiguration | Nativer Connector mit DetectionOnly-Engine-Regeln; siehe [DetectionOnly-Profil](#detectiononly-profil). |
| [disabled/httpd.conf](disabled/httpd.conf) | Host-Konfiguration | Auf Apache-Ebene deaktivierter Connector; siehe [Deaktiviertes Profil](#deaktiviertes-profil). |
| [rules/request-only.conf](rules/request-only.conf) | Regeln | Rule-Engine-Einstellungen nur für Requests. |
| [rules/p1-p4-safe.conf](rules/p1-p4-safe.conf) | Regeln | Begrenzte Response-Body-Einstellungen und lokale P4-Illustration. |
| [rules/detection-only.conf](rules/detection-only.conf) | Regeln | DetectionOnly-Engine-Einstellungen. |
| [rules/engine-off.conf](rules/engine-off.conf) | Regeln | Engine-Off-Einstellungen, getrennt vom Deaktivieren des Connectors. |
| [No-CRS-Regeln](#no-crs-regeln) | Dokumentation | No-CRS-Quelle und Bedeutung der Regel-IDs. |
| [P1--P4-Safe-Absicht](#p1-p4-safe-absicht) | Dokumentation | Konfigurationsabsicht, kein Testergebnis. |

Alle Pfade in dieser Tabelle sind ab examples/apache repository-relativ. Pfade
in der Konfiguration, einschließlich /usr/lib/apache2/modules/mod_security3.so,
/etc/modsecurity und /var/log, sind Beispiele für Hostinstallationen.

## Anzupassende Werte

| Name | Zweck und Format | Pflicht/Default, Setzer, Geltungsbereich | Beispiel, Auswirkung und Sicherheit |
| --- | --- | --- | --- |
| security3_module | Von LoadModule geladenes Modul | Pflicht; kein Repository-Default; Apache-Paket oder lokaler Build; Server-Scope | mod_security3.so an installiertem Modulpfad. Falsche ABI oder falscher Pfad verhindert den Start. |
| modsecurity_rules_file | Lesbare libmodsecurity-Regeldatei | Pflicht; kein Repository-Default; Host-Konfiguration; Modul-Scope | /etc/modsecurity/modsecurity-phase4.conf. Ein geprüftes Ruleset kann Traffic blockieren. |
| modsecurity_phase4_mode | Late-P4-Policy: minimal, safe oder strict | Minimal-, Safe-, Strict- und vollständige Datei; Host-Konfiguration; Modul-Scope | Die vollständige Datei verwendet bewusst `strict`; `all` ist kein Parserwert. Die Einstellung wählt die Post-Commit-Aktion, ohne bereits weitergeleitete Bytes umzuschreiben. |
| modsecurity_phase4_content_types_file | Veraltete Legacy-Datei für Response-MIME-Typen | Optionaler Kompatibilitätsparser; Host-Konfiguration; Modul-Scope | Nicht verwenden, um die Pass-through-Reihenfolge zu ändern. `SecResponseBodyMimeType` wählt die Engine-Inspektion. |
| modsecurity_phase4_log | Ziel für Decision-JSONL | Optional; Host-Konfiguration; Modul-Scope | /var/log/modsecurity/apache-phase4.jsonl. Request-Metadaten schützen und rotieren. Ein root-eigenes Parent-Verzeichnis wird nur unterstützt, wenn es nicht für Gruppe/Andere schreibbar ist und die bestehende finale reguläre Datei dem Apache-Worker gehört; der Öffner normalisiert ihren Modus auf 0600. Sie vorab anlegen und diese Eigentümerschaft beim Rotieren erhalten. |
| modsecurity_phase4_body_limit und SecResponseBodyLimit | Positive P4-Byte-Limits | Für begrenztes Safe Pflicht; Host- und Regeldatei; keine automatische Angleichung | Connector-Standard sind 1048576 Byte. Er begrenzt die inkrementelle Inspektion und schlägt bei Überschreitung fail-closed fehl; er erlaubt kein vollständiges Response-Buffering. |
| modsecurity_transaction_id_expr und modsecurity_transaction_id | Optionale Host-Korrelationsüberschreibungen | Optional; Host-Konfiguration; Modul-Scope | Beide stehen in `all/httpd.conf` bewusst als Kommentar. Nur einen validierten, eindeutigen Hostwert aktivieren; URI-abgeleitete oder statische Werte korrelieren Transaktionen nicht sicher. |
| SecRequestBodyAccess und SecResponseBodyAccess | Request-/Response-Body-Schalter | In passenden Regeln Pflicht; Rule-Engine-Scope | On in Safe-Regeln; Response Access ist bei Request-only Off. |
| SecResponseBodyMimeType und SecResponseBodyLimitAction | Engine-P4-Scope und Policy über dem Limit | In Safe-Regeln Pflicht; Rule-Engine-Scope | Explizite Text-/JSON-Typen wählen die Engine-Inspektion. Kein Binary-Verhalten oder eine andere Host-Weiterleitungsreihenfolge ableiten. |
| SecAuditLog | Audit-Log-Ziel | Optional; Regeldatei; Rule-Engine-Scope | /var/log/modsecurity/apache-audit.log. Zugriff und Aufbewahrung steuern. |

Regel-ID 9002801 gehört nur zu p1-p4-safe.conf. Sie ist weder eine OWASP-CRS-
noch eine No-CRS-Baseline-ID; siehe [No-CRS-Regeln](#no-crs-regeln).

## Konfigurationsreferenz

Die generierte [Konfigurationsreferenz](configuration-reference.de.md)
dokumentiert alle 11 registrierten Apache-Direktiven, die hier verwendeten
Hostfelder und ihre Parser-/Default-/Merge-Anker.

| Einstellung | Ebene | Aufgabe |
| --- | --- | --- |
| `modsecurity on|off` | Host / Connector | Aktiviert oder deaktiviert die Apache-Transaction-Erzeugung. |
| `SecRuleEngine` | ModSecurity Engine | Wertet geladene Regeln aus und wählt Enforcement, DetectionOnly oder Off. |
| `SecRequestBodyAccess` | ModSecurity Engine | Stellt dem Engine-P2-Request-Body-Eingaben bereit. |
| `SecResponseBodyAccess` | ModSecurity Engine | Stellt berechtigte P4-Response-Body-Eingaben bereit. |
| `modsecurity_phase4_mode` | Connector / Common Policy | Wählt die Post-Commit-Policy. Er schreibt niemals einen Response-Daten-Bucket rückwirkend um, den Apache bereits weitergeleitet hat. |

`modsecurity on` mit `SecRuleEngine Off` erzeugt den Connector-Pfad, schaltet
aber die Engine-Regelauswertung ab. `modsecurity off` verhindert eine
Connector-Transaction auch dann, wenn eine Regeldatei `SecRuleEngine On` setzt.

## Profile

### DetectionOnly-Profil

`detection-only/httpd.conf` lässt `modsecurity on` aktiv und wählt die
DetectionOnly-Regeldatei. DetectionOnly lädt und bewertet Engine-Regeln und
zeichnet Treffer auf, führt aber keine disruptiven Engine-Aktionen aus.

Nach dem Anpassen der Hostpfade den untenstehenden Connector-
Validierungsbefehl verwenden. Dieses Profil ist Konfigurationsanleitung und
keine Runtime-Evidenz.

### Deaktiviertes Profil

`disabled/httpd.conf` setzt `modsecurity off`; Apache erzeugt keine Connector-
Transaction. Dies unterscheidet sich von `SecRuleEngine Off`, das bei aktivem
Hostconnector die Regelauswertung innerhalb der Engine abschaltet.

Nach dem Anpassen der Hostpfade den untenstehenden Connector-
Validierungsbefehl verwenden. Aus einem deaktivierten Profil kein
P1--P4-Verhalten ableiten.

## P1--P4-Safe-Absicht

Die Safe-Referenz konfiguriert die Verarbeitung des nativen httpd-Moduls für
P1 bis P4 mit einem Response-Body-Limit von 1048576 Byte. Für jeden Nicht-
Metadaten-Response-Bucket ruft Apache zuerst `msc_append_response_body()` auf
und ruft anschließend den nächsten Output-Filter mit demselben Bucket auf.
FLUSH bleibt Host-Metadatum und wird nicht zu Body-Daten. Beim tatsächlichen
EOS führt Apache `msc_process_response_body()` genau einmal aus und emittiert
das terminale EOS-Fragment erst nach Abschluss des finalen Entscheidungspfads.
Dieser Filter hält keine vollständige Response-Kopie.

Das konfigurierbare Byte-Limit begrenzt die inkrementelle Inspektion und
schlägt fail-closed fehl, bevor ein übergroßer Chunk angehängt werden kann. Es
ist kein Grund, eine unbegrenzte Response zurückzuhalten. Die C-API lässt die
wirksame libModSecurity-MIME-Entscheidung für diesen Adapter opak;
`SecResponseBodyMimeType` wählt die Engine-Inspektion, ändert aber nicht die
Pass-through-Reihenfolge. Das veraltete
`modsecurity_phase4_content_types_file` fehlt weiterhin absichtlich in der
Safe-Konfiguration.

Dieser Abschnitt dokumentiert Konfigurationsabsicht plus die quellenbasierte
Reihenfolge, kein client-sichtbares Runtime-Ergebnis. Ein Pre-Commit-Ergebnis
kann weiter den normalen HTTP-Error-/Redirect-Pfad verwenden. Sobald Apache
Response-Bytes weitergeleitet hat, zeichnet Safe ein spätes disruptives
Ergebnis log-only auf und setzt fort; Strict betritt den nativen Connection-
Abort-Pfad. Die ausführbare vollständige Form ist
[all/httpd.conf](all/httpd.conf); sie verwendet bewusst die gültige Strict-
Einstellung und dokumentiert zugleich die Runtime-Evidenzgrenze.

## No-CRS-Regeln

Die wiederverwendbare No-CRS-Quelle ist
[modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf](../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf).
Sie ist repository-relativ und soll vom Betreiber als geprüftes Host-Ruleset,
zum Beispiel /etc/modsecurity/no-crs-baseline.conf, installiert oder kopiert
werden.

| Regel-ID | Phase | Zweck |
| ---: | ---: | --- |
| 1100001 | P1 | Request-Header-Deny |
| 1100101 | P2 | Request-Body-Deny |
| 1100201 | P3 | Response-Header-Deny |
| 1100301 | P4 | Response-Body-Entscheidung für die Safe-Grenze |

Die eingecheckte Datei p1-p4-safe.conf ist eine illustrative Apache-
Regeldatei. Ihre Regel 9002801 gehört nur zu diesem Beispiel und ist weder
eine OWASP-CRS- noch eine No-CRS-Baseline-ID.

## Validierung

Die gewählten Dateien installieren oder einbinden, alle Hostpfade anpassen und
die vollständige installierte Apache-Konfiguration prüfen:

~~~sh
apachectl -t
~~~

Nach einem beabsichtigten Reload Apache-Error-Log, Decision-Log und Audit-Log
prüfen. Ein Syntaxcheck beweist weder P1--P4-Verhalten noch einen
client-sichtbaren P4-Status, CRS-Abdeckung oder Produktionsreife.

## Strict-Profilgrenze <a id="strict-profilgrenze"></a>

`modsecurity_phase4_mode strict` wird vom Parser unterstützt. Der Source
markiert die native Connection nach einem committed disruptiven Phase-4-
Ergebnis als abgebrochen, aber dieses Repository besitzt keinen aktuellen
Apache-Hostnachweis für das client-sichtbare späte Abbruchergebnis. Strict ist
deshalb optional und behauptet dieses client-sichtbare Ergebnis nicht. Es gilt
nur nach dem Commit; es wandelt einen normalen P4-Deny vor Commit nicht in
einen späten Abbruch um.

Von `safe/httpd.conf` ausgehen, `modsecurity_phase4_mode strict` setzen,
mit `apachectl -t` validieren und host-spezifische Evidenz erfassen, bevor auf
eine Post-Commit-Aktion vertraut wird.

Der fokussierte H1/H2-Evidence-Platzhalter ist
`ci/runtime/lifecycle/run-apache-phase4-response-regression.sh`. Erst nach
seiner Ausführung werden laufbezogene Artefakte erfasst; diese
Konfigurationsdokumentation behauptet keinen Pass für eines der Protokolle.

## Verwandtes Material

- [Apache-Connector-Quellcode und Validierungsgrenze](../../connectors/apache/README.de.md)
- [Repository-Beispielübersicht](../README.de.md)
