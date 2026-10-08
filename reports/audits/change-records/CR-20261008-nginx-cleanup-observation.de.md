# Change Record: CR-20261008-nginx-cleanup-observation

**Sprache:** [English](CR-20261008-nginx-cleanup-observation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-cleanup-observation |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | 201c6194a0061efe49e854a02f8626170ddee3b1 |

## Motivation und Problemstellung

Native Framing-Evidenz benötigt eine tatsächliche Cleanup-Beobachtung statt einer
Fixture-Behauptung. Der begrenzte Konstruktor erzeugt Metadaten aus Common-Fakten.

## Akzeptanzkriterien

Tatsächlichen Cleanup-Return, Abschluss, Taxonomie und natives Abschlussboolean
erhalten. NULL und abgeschnittene Ausgabe ablehnen. LOGGING-Metadaten ohne erfundene
Quelle, Regel oder Transaktionsidentität erzeugen. Echte Common-Übergangstests
kompilieren und ausführen.

## Implementierungsentscheidung und Begründung

ngx_http_modsecurity_cleanup_observation erhält Event, eigenen Reason-Puffer und
Kapazität, tatsächlichen Common-Return, const Contract und natives Abschlussboolean.
Return 1 bedeutet Konstruktion, 0 ungültige/abgeschnittene Eingabe; das Event bleibt
bei Ablehnung unverändert. Der Reason-Puffer muss bis zur Serialisierung leben.

Erst nach Rückkehr des tatsächlichen Common-Cleanup und nativen void-Cleanup
aufrufen. Nativer Abschluss ist nur wahr, wenn zuvor eine Transaktion existierte
und Cleanup zurückkehrte. Kein nativer Getter nach Freigabe. Der Koordinator bindet
tatsächlichen Request, Transaktion, Host und Protokoll separat.

## Geänderte Dateien

Neu: connectors/nginx/src/ngx_http_modsecurity_cleanup_observation.h,
tests/test_nginx_cleanup_observation.c und dieses Record-Paar.
Modul-/Common-/Source-Map-Verdrahtung bleibt unverändert beim Koordinator.

## Ausgeführte Befehle

RTK-gekapseltes cc -std=c17 -Wall -Wextra -Werror -Icommon/include kompilierte den
Test mit common/src/transaction_state.c in ein externes Task-Binary, Exit 0.
Das Binary prüfte vollständige Phasen/Finish/Cleanup, vorzeitiges und zweites
Cleanup, unvollständige Beobachtung, erhaltenen Timeout, native0 sowie NULL/
Abschneidekontrollen, Exit 0.
Erneute Kompilierung mit -fsanitize=undefined und Ausführung bestanden, Exit 0,
einschließlich exakt passender Reason-Kapazität und unverändertem Contract. Direkte
EN/DE-Record-Prüfung bestand nach Korrektur vorgeschriebener deutscher Überschriften
und Identitätslabels, Exit 0.

## Security-Auswirkung

Payload-freie begrenzte Formatierung; keine Abschwächung, erfundener API-Return oder
synthetische Quellenidentität. Leere Regelmetadaten. LOGGING/allow bezeichnet nur
Cleanup-Erfolg, keine Request-Erlaubnis. Der Konstruktor verändert den Contract nicht.

## Runtime-Evidence

Kein nativer NGINX-Build/Runtime-Lauf. Common-Zustands-Unit-Ausführung belegt weder
nativen Cleanup noch Host-Runtime.

## Bekannte Einschränkungen

Der Aufrufer liefert tatsächliche Fakten und stabile geliehene Metadaten. Nativer
void-Cleanup erhält keinen erfundenen numerischen API-Return. Native0 bleibt explizit.

## Verbleibende Risiken

Integrierte Quellenbindung, Serialisierung und kanonische Runtime benötigen den
Modul-Hook des Koordinators und neue Evidenz.

## Nicht ausgeführte Prüfungen mit Begründung

Native NGINX-Runtime/Build lag außerhalb dieses Schnitts. Vollständige bilinguale
Repository-Prüfung war zuvor durch 22 fehlende Submodul-Linkziele blockiert;
das neue Paar wird direkt geprüft. Ruff fehlt; keine Installation.

## Finaler Diff- und Review-Status

Begrenzten Source-/Test-/Record-Diff geprüft. Separater Commit enthält nur eigene
neue Dateien. Vorherige Commits, Modul-Hooks, Common-Dateien und Gitlinks unverändert.
