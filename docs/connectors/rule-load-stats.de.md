# Regel lädt Statistikmetadaten

**Sprache:** [English](rule-load-stats.md) | Deutsch

Status: aktueller, dem Adapter gehörender Apache- und NGINX-Code

In diesem Dokument werden die allgemeinen Regelladestatistik-Metadaten aufgezeichnet, die von der gemeinsam genutzt werden
Apache- und NGINX-Anschlüsse. Es werden nur beobachtbare Metadaten beschrieben. Die Statistiken tun es
Ändern Sie nicht das Laden von Regeln, das Zusammenführen von Regeln, die Requestsverarbeitung, die Antwortverarbeitung usw
jede Runtimeentscheidung.

## Gemeinsame Struktur

`common/include/msconnector/rule_load_stats.h` definiert
`msconnector_rule_load_stats` mit diesen Feldern:

| Feld | Bedeutung |
| --- | --- |
| `inline_rules` | Anzahl der Regeln, die aus Inline-`modsecurity_rules`-Inhalten geladen werden |
| `file_rules` | Anzahl der aus Regeldateien geladenen Regeln |
| `remote_rules` | Anzahl der Regeln, die von Remote-Regelladevorgängen geladen wurden |

Die Werte zählen geladene Regeln, keine Direktivenaufrufe. `file_rules` zählt
Regeln, die aus Regeldateien geladen werden; Die Anzahl der Dateien wird nicht gezählt. Der
Die Struktur enthält keine Apache-Typen, keine NGINX-Typen und keinen libmodsecurity-Eigentum
Objekte und keine Runtimerückrufe.

Der gemeinsame Header bietet auch kleine Inline-Helfer zum Initialisieren einer Statistik
Strukturieren und Inline-, Datei-, Remote- oder Aggregatzähler hinzufügen. Diese Helfer sind
reine Gegenoperationen. Sie weisen keinen Speicher zu, protokollieren nicht und schließen den Server nicht ein
Header oder akzeptieren Sie den Besitz eines beliebigen Connector-Runtimeobjekts. Anrufer passieren gültig
Statistikzeiger; Die Helfer definieren keinen stillen NULL-Zeigerpfad.

## Semantik

Regelladestatistiken sind Metadaten. Sie werden erst nach Erfolg erhöht
`msc_rules_add*`-Aufrufe, die bereits die vorhandenen libmodsecurity-Rückgabewerte verwenden
wird von jedem Anschluss verwendet. Bei fehlgeschlagenen Ladeversuchen bleibt der vorhandene Fehlerpfad erhalten und funktioniert nicht
Erhöhen Sie die Zähler nicht.

Kein Connector verwendet diese Statistiken, um zu entscheiden, ob eine Anfrage verarbeitet werden soll.
blockiert, protokolliert oder überprüft werden. NGINX stellt die Werte durch sein Vorhandenes zur Verfügung
Startup-Log. Apache speichert die Werte derzeit nur als interne Konfigurationsmetadaten.

## Meldestatus

NGINX meldet Regelladestatistiken über sein vorhandenes Startup-Log. Der Connector
verwendet intern den allgemeinen Statistikhelfer, aber den Protokolltext, das Format, die Ebene und
Die Reihenfolge bleibt beim bestehenden NGINX-Verhalten.

Apache speichert Regelladestatistiken als Metadaten in `msc_conf_t`. Dies ist derzeit nicht der Fall
Melden Sie diese Werte im Post-Config-Protokoll. Die Apache-Berichterstellung wird verschoben bis
Die Aggregationsquelle und die Zusammenführungssemantik für die Anzeige werden explizit definiert.

`msconnector_rule_load_stats` ist nur eine Datenform. Es gibt keine gemeinsame Berichterstattung
API für diese Werte noch nicht verfügbar.

## Apache

Apache speichert `msconnector_rule_load_stats` in `msc_conf_t`.

Die Apache-Parserpfade aktualisieren die Statistiken erst nach erfolgreichem Laden der Regeln:

- Inline-Regeln zu `inline_rules` hinzufügen;
- Aus Dateien geladene Regeln werden zu `file_rules` hinzugefügt.
- Remote-Regeln werden zu `remote_rules` hinzugefügt.

Durch die Zusammenführung der Apache-Verzeichniskonfiguration werden übergeordnete und untergeordnete Statistiken als Metadaten hinzugefügt. Das tut es
`msc_rules_merge()`-Rückgabewerte werden nicht als Zähler verwendet und sie ändern sich nicht
das RuleSet-Zusammenführungsverhalten.

Apache verwendet die gängigen Inline-Hilfsfunktionen für die erfolgreiche Initialisierung
Ladeinkremente und reine Metadaten-Merge-Hinzufügung.

Kein Apache-Runtimepfad liest die Statistiken. Haken, Filter, Eimerbrigaden,
Interventionshandhabung, Transaktionseigentum, Handhabung des Requeststexts und
Die Handhabung des Response Bodys bleibt unverändert.

## NGINX

NGINX behält seine vorhandenen lokalen Zähler:

- `rules_inline`
- `rules_file`
- `rules_remote`

Ein kleiner Adapter-Helfer kopiert diese Werte in `msconnector_rule_load_stats`.
Die lokalen `ngx_uint_t`-Felder bleiben die vom aktuellen NGINX verwendete Quelle
Connector. Das vorhandene Startup-Log liest die Werte über den Helfer ohne
Ändern des Protokolltextes, des Formats, der Ebene oder der Reihenfolge. Der Helfer ändert sich nicht
Regeln laden, Konfigurationszusammenführung, Init-Verhalten, PCRE-Zuweisungsverhalten, RulesSet
Eigentum oder Fehlerbehandlung.

## Nicht-Ziele

Die Metadaten der Regelladestatistiken ändern sich nicht:

- RuleSet-Eigentum oder -Lebensdauer;
- `msc_rules_merge()`-Semantik;
- Verhalten des PCRE-Allokators;
- Fehlerpfade beim Laden von Regeln;
- Lebenszyklus des Requests- oder Response Bodyes;
- Verhalten in Phase 4;
- Haken oder Filter;
- Eimerbrigaden;
- Runtimeverhalten des Eingriffs.

## Aufgeschoben

Die folgenden Arbeiten werden absichtlich zurückgestellt:

- gemeinsame Berichterstattung für Regelladestatistiken;
- Apache-Postkonfigurationsberichterstellung;
- gemeinsame Metadatenprotokollierung;
- Testergebnis- oder Audit-Log-Auswertung der Statistiken;
- Fähigkeitsberichte, die die Anzahl der Regellasten enthalten;
- jegliche Runtimenutzung der Zähler.
