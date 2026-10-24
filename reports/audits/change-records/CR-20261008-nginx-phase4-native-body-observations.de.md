# Änderungsnachweis: CR-20261008-nginx-phase4-native-body-observations

**Sprache:** [English](CR-20261008-nginx-phase4-native-body-observations.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-phase4-native-body-observations |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `764402f47b7d2db941e5002485b205b4d4563cbd` |

## Motivation und Problemstellung

Der nativen Phase4-Evidenz fehlten tatsächliche Append-Zahlen und behaltene Engine-Länge. Engine-Reject kann Append-Erfolg mit ausstehender regel-ID-freier Intervention zurückgeben. Wird diese erst bei EOS abgeholt, kann der abgelehnte Body den nächsten Filter erreichen. Eine Engine-Budget-Ablehnung nach Rückgabe muss tatsächliches natives EOS von abgelehntem Common-Abschluss unterscheiden.

## Akzeptanzkriterien

Jedes gültige native Append protokolliert tatsächliche Rückgabe, gelieferte Länge, Aufrufindex und behaltene Engine-Länge. Abschluss verlangt native Prozessrückgabe 1 und strikten Common-P4-Abschluss. Sofortiger Reject verhindert Weiterleitung und liefert genaue regel-ID-freie native 403/reject-Metadaten. Timeout liefert technischen 504 mit tatsächlichem EOS; alle Fehlerpfade bleiben terminal.

## Implementierungsentscheidung und Begründung

Der eigene Body-Filter ruft `msc_get_response_body_length` auf und erhält die gelieferten Common-Byte-Zähler. Eigene Append-/Abschlussereignisse verwenden bestehende strikte Common-JSONL. Append-Callbacks sind von tatsächlicher Phase4-Aktivität umschlossen. Nach jeder gültigen nativen Rückgabe 0 oder 1 wird vor Weiterleitung die echte Intervention abgeholt; keine Fixture weist ein beobachtetes Ergebnis zu.

Die gepinnte Quelle `Transaction::appendResponseBody` liefert bei Reject true und setzt eine 403/disruptive-Intervention; ProcessPartial liefert false. Die C-API gibt diesen Integer direkt zurück. Aufbewahrte reine Engine-Diagnosen beobachteten unabhängig Reject-Append 1/behalten 0 sowie Partial-Append 0/behalten 64. Nur bei Rückgabe 0 abzuholen würde Reject übersehen. Exaktes Antwortlimit-Prädikat und Klassifikation bleiben externe Abhängigkeiten des Moduls.

Terminale Verarbeitung umschließt den tatsächlichen nativen Aufruf mit der Budget-API des Koordinators. Nativer Erfolg setzt vor Budget-Prüfung natives EOS; Common-Abschluss und strikte Beobachtung folgen erst nach erfolgreicher Budget-Prüfung. Nativer Reject verwendet 403, Connector-Buchungslimits behalten 413 und sonstige Steuerungsfehler ihre bestehende Klassifikation. Fehlerereignisse bewahren tatsächliche Commit-/Abort-/EOS-Werte; nativer Reject trägt ausdrücklich reject ohne Rule-ID.

## Geänderte Dateien

Nur `connectors/nginx/src/ngx_http_modsecurity_body_filter.c`, `tests/test_nginx_phase4_native_body_source.py` und dieses EN/DE-Paar. Kontextfelder, Budget-API, Modulklassifikation und SOURCE_MAP gehören dem Koordinator und werden hier nicht geändert.

## Ausgeführte Befehle

Die RTK-verpackte kontrollierte C17-Regression scheiterte zunächst am fehlenden Beobachtungshelfer. Nach Implementierung kompilieren sechs fokussierte Tests echte Quellfunktionen gegen den echten Common-Serializer für Sanity 0/1. Native Aufrufe, Hostgrenzen und Begin-/Complete-Wrapper sind kontrollierte Fixture-Grenzen; Common-Body-Buchung/-Fehler und Serialisierung sind echt. Split/Partial/Leerantwort, tatsächliche Chain-Reject ohne Weiterleitung, ungültige Rückgabe/Länge/Zählerüberlauf sowie Prozess-/Abschluss-/Budget-/Schreibfehler sind geprüft. Frühere Phase4-Discovery bestand 33 Tests mit drei vorhandenen SKIPs; abschließende Ergebnisse stehen in der Übergabe.

## Security-Auswirkung

Keine Payload gelangt in native Event-Metadaten. Die Engine besitzt weiterhin die Limits. Abgelehnter Body erreicht nie den nächsten Filter, fehlgeschlagener Abschluss erzeugt keine Abschlussevidenz und technische Fehler werden nicht zu SAFE-Log-only-Erfolg.

## Runtime-Evidence

Kontrollierte Fixture-Tests sind kein tatsächlicher NGINX-/Engine-Lauf. Frühere reine Engine-Diagnosen belegen API-Grenzverhalten ihrer gepinnten Bibliothek, keinen neuen Connector-Build. Root muss Kontext/API/Modul integrieren und frische quellgebundene native Evidenz ausführen.

## Bekannte Einschränkungen

Dem isolierten Quellcheckout fehlen bewusst Kontext-/API-Änderungen des Koordinators. Die fokussierte Fixture stellt diese Schnittstellen bereit; finale integrierte Kompilierung bleibt erforderlich. Unerwartete Append-Rule-Interventionen scheitern geschlossen und belegen weder EOS noch kanonisches PASS.

## Verbleibende Risiken

Tatsächliche Host-, Artefakt-, Wire-Framing-, Cleanup- und Revisionsbindung benötigen finale Koordinatorintegration und Laufzeitvalidierung. Abschlussevidenz allein beweist keine Downstream-Zustellung.

## Nicht ausgeführte Prüfungen mit Begründung

Kein nativer Connector-Build-/Laufzeit-Slot wurde zugewiesen. Vollständiger Lint, finaler nativer Lauf und frisches CI/Sonar bleiben beim Koordinator.

## Finaler Diff- und Review-Status

Fokussierte eigene Teilaufgabe; keine Modul-/Common-Header-/SOURCE_MAP-/gemeinsamen Worktree-/MRTS-Änderungen, Veröffentlichung oder Gitlink-Aktualisierung.
