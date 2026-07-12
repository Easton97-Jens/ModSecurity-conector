# Dokumentationsstil-Leitfaden

**Sprache:** [English](documentation-style-guide.md) | Deutsch

Dieser Leitfaden gilt für repository-eigenes Markdown. Er ist eine
Wartungsregel, keine Generator-Spezifikation: Generierte Dokumente dürfen nicht
manuell umgeschrieben werden.

## Erforderliche Dokumentform

- Verwenden Sie genau eine H1, gefolgt von einer logischen H2/H3-Hierarchie.
- Platzieren Sie den Sprachumschalter direkt unter der H1 in jedem
  English-/German-Paar.
- Schreiben Sie kurze Absätze und verwenden Sie Tabellen nur, wenn Leser Werte
  vergleichen müssen.
- Geben Sie jedem Codeblock einen passenden Sprach-Tag wie <code>sh</code>,
  <code>make</code>, <code>json</code>, <code>yaml</code> oder <code>text</code>.
- Nennen Sie Zweck, Aktualität, Source of Truth und Claim-Grenze des Dokuments,
  wenn sie sonst unklar wären.
- Bevorzugen Sie repository-relative Links und erklären Sie ihr
  Ausgangsverzeichnis.

Führen Sie den Checker vor der Übergabe einer Dokumentationsänderung aus:

~~~sh
make check-bilingual-docs
~~~

Dieses Target prüft erforderliche English-/German-Begleitdateien und lokale
Markdown-Links. Es zertifiziert nicht die faktische Richtigkeit eines
Runtime-Claims.

## English/German technische Parität

English- und German-Dokumente müssen dieselben technischen Fakten enthalten.
Behalten Sie Variablennamen, Defaults, erlaubte Werte, Pfade, Targets, IDs,
Statuswerte, Rule-IDs, Case-IDs und Integrationsmodus-Namen identisch.
Übersetzen Sie Prosa, nicht maschinenlesbare Werte.

Erstellen oder aktualisieren Sie beide Dateien in einer Änderung. Wenn in einer
Sprache eine Tabelle existiert, behalten Sie äquivalente Zeilen und Werte in
der Begleitdatei. Ein deutscher Link soll auf die deutsche Begleitdatei zeigen,
wenn sie existiert. Behalten Sie die Standard-Header exakt:

~~~text
Sprachzeile: English | deutscher Partner `file.de.md`
Deutsche Zeile: englischer Partner `file.md` | Deutsch
~~~

### Von der Übersetzung ausgenommene Connector-Metadaten

Nur `connectors/**/ORIGIN.md` und `connectors/**/TODO.md` sind von der Regel
für Begleitdateien ausgenommen. Sie sind Herkunfts- oder
Arbeitsverfolgungsmetadaten statt Leser-Guides; ihre maschinenorientierten Namen
und Werte bleiben einsprachig. Diese Ausnahme gilt nicht für Connector-READMEs,
`docs/`, `harness/`, `src/` oder PoC-Designnotizen: Diese leserorientierten
Dokumente benötigen eine deutsche Begleitdatei.

`docs/en/README.md` und `docs/de/README.md` sind das einzige bewusst
beibehaltene Sprachindex-Paar über Verzeichnisse hinweg. Sie behalten ihre
stabilen Navigationspfade, statt irreführende `README.de.md`-Dateien zu
erhalten. Der Bilingual-Checker validiert sowohl die Ausnahme als auch ihre
wechselseitigen Sprachlinks.

## Variablen und Platzhalter

Erklären Sie jeden benutzerseitig anpassbaren Wert im selben Dokument nahe
seiner ersten Verwendung und verlinken Sie dann auf die zentrale
[Variablenreferenz](../configuration/variables.de.md). Die lokale Erklärung
beantwortet:

1. Wie lautet Name und Zweck?
2. Welches Format und welche Werte sind erlaubt?
3. Ist der Wert Pflicht oder optional, und was ist der tatsächliche Default?
4. Wer setzt ihn, welchen Scope beeinflusst er und was passiert bei einem falschen Wert?
5. Enthält er Secrets oder ist er anderweitig sicherheitsrelevant?
6. Welches realistische Beispiel kann der Leser anpassen?

Verwenden Sie dieses Muster: Stellen Sie die Variable in Prosa vor und zeigen
Sie dann das Kommando. Sagen Sie zum Beispiel, dass <code>BUILD_ROOT</code>
ein optionales absolutes, beschreibbares Build-Verzeichnis außerhalb des
Checkouts ist, weil das Root-Makefile einen Default ableitet. Zeigen Sie dann:

~~~sh
make quick-check BUILD_ROOT="/srv/modsecurity-work/build"
~~~

Erklären Sie nach dem Kommando, dass
<code>/srv/modsecurity-work/build</code> ein Beispiel für einen absoluten
Runtime-Pfad ist, nicht Repository-Root oder Systemverzeichnis, und verlinken
Sie auf die zentrale
[Variablenreferenz](../configuration/variables.de.md#runtime-und-repository-pfade).

Lassen Sie keinen ausführbaren Platzhalter unerklärt. Erklären Sie
<code>&lt;connector&gt;</code>, <code>&lt;path&gt;</code>,
<code>REPLACE_ME</code>, <code>CHANGE_ME</code>, <code>$VAR</code> und
<code>$(MAKE_VAR)</code> unmittelbar mit erlaubten Werten und Beispiel.
Erklären Sie Beispiel-Path-, Host- und Port-Werte in YAML/JSON als ersetzbare
Beispielwerte, auch wenn sie syntaktisch keine Variablen sind.

Sagen Sie zum Beispiel, dass <code>&lt;connector&gt;</code> einer von
<code>apache</code>, <code>nginx</code>, <code>haproxy</code>,
<code>envoy</code>, <code>traefik</code> oder <code>lighttpd</code> ist, und
geben Sie dann das literale Beispiel <code>make build-nginx</code>.

Verwenden Sie keine unerklärten Auslassungszeichen in ausführbaren Beispielen.
Wenn eine fokussierte Konfiguration Standarddirektiven auslässt, sagen Sie dies
in Prosa und verlinken Sie auf ein vollständiges eingechecktes Beispiel.

## Pfade, Defaults und Secrets

Kennzeichnen Sie die Rolle jedes bedeutenden Pfads: repository-relativ,
absoluter Runtime-Pfad, Host-Installation, generiert, temporär, Cache oder
Evidence. Veröffentlichen Sie keine entwicklerspezifischen Pfade wie ein
persönliches Home-Verzeichnis oder lokalen Workspace. Bevorzugen Sie ein
portables Beispiel wie <code>/srv/modsecurity-work/build</code> und
kennzeichnen Sie es als Beispiel.

Unterscheiden Sie diese Begriffe exakt:

| Label | Bedeutung |
|---|---|
| Repository-Default | Ein Wert, der durch ein eingechecktes Makefile oder eine Konfiguration zugewiesen wird |
| Host-Default | Ein Wert, den die installierte Host-Software liefert |
| Beispielwert | Ein lesbarer Wert, der nur das Format illustriert |
| Empfohlener lokaler Wert | Eine vorgeschlagene portable lokale Wahl, kein zugewiesener Default |
| CI-Wert | Ein von CI abgeleiteter oder injizierter Wert |
| Kein Default | Aufrufer oder Target muss den Wert liefern |

Nehmen Sie niemals private Schlüssel, Token, Passwörter, Cookies,
Authorization-Header, API-Keys, Client-Secrets oder reale Zertifikate in
Dokumentation auf. Verwenden Sie <code>&lt;secret-from-secure-store&gt;</code>,
sagen Sie, dass er nicht committed oder in kanonische Evidence kopiert werden
darf, und vermeiden Sie Kommandozeilenbeispiele, die ihn in einer Prozessliste
offenlegen.

## Kommandos, Targets, Status und IDs

Nennen Sie für jedes dokumentierte Make-Target Zweck, Voraussetzungen,
wichtige Eingabevariablen, Ausgabe/Artefakte, Exit-Code-Verhalten und die
Abgrenzung zu einem nahe liegenden Target. Erklären Sie Target-Platzhalter
sofort.

Verwenden Sie die gemeinsamen Statusnamen präzise: <code>PASS</code>,
<code>FAIL</code>, <code>BLOCKED</code>, <code>NOT EXECUTED</code>,
<code>NOT APPLICABLE</code>, <code>UNSUPPORTED</code> und historisch
<code>NOT_EXECUTABLE</code>. Erklären Sie, dass Prozess-Exit-Code
<code>0</code> bedeutet, dass der aufgerufene Prozess seinen eigenen
technischen Vertrag erfüllte; er bedeutet nicht, dass jeder Case eines
Katalogs bestanden hat.

Geben Sie Rule-IDs, Case-IDs, Message-IDs, Schemafelder und Integrationsmodi
nahe ihrer Verwendung Kontext. Nennen Sie, ob eine ID zur No-CRS-Baseline des
Repositorys statt zu OWASP CRS gehört. Definieren Sie nicht offensichtliche
Begriffe wie <code>EOS</code>, <code>HTX</code>, <code>ext_proc</code> oder
<code>APXS</code> beim ersten lokalen Auftreten und verlinken Sie auf das
[Glossar](../reference/glossary.de.md).

## Claims und Evidence

Halten Sie Source-, Konfigurations-, Build-, Runtime- und kanonische
Evidence-Claims getrennt. Nennen Sie das ausgewählte Host-Profil und die
exakte Evidence-Grenze, wenn Sie ein Ergebnis beschreiben. Verwandeln Sie
weder Capability-Deklaration, Config-Load-Erfolg noch Compatibility-Smoke in
eine weitergehende Zusicherung.

Behaupten Sie keine Production Readiness, CRS-Verifikation/-Vollständigkeit,
vollständige HTTP/2-Verifikation, vollständige HTTP/3-Verifikation,
vollständige Matrix oder Strict-Verifikation für alle Connectoren. Verwenden
Sie präzise Alternativen wie „ausgewählte HTTP/1.1-Kernroute“,
„run-spezifische Evidence“ oder „nicht ausgeführt“, wenn dies den Artefakten
entspricht.

## Generierte und historische Dokumente

Erkennen Sie generierte Dateien an ihrem Generated-Hinweis, Verzeichnis oder
Generator-Vertrag. Aktualisieren Sie Generator/Source of Truth und regenerieren
Sie, statt Ausgabe von Hand zu bearbeiten. Bewahren Sie Generated-Hinweise und
maschinenlesbare Werte.

Historische Reports bewahren ihre Provenance. Kennzeichnen Sie einen ersetzten
Report als historisch und verlinken Sie auf die aktuelle Ablösung; schreiben
Sie Run-IDs, Commits, Counts oder frühere Schlussfolgerungen nicht
stillschweigend als aktuelle Fakten um.

## Review-Checkliste

- Beide Sprachdateien existieren und besitzen die Standard-Header.
- Lokale Links lösen auf, und deutsche Links zeigen bei vorhandenen
  Begleitdateien auf diese.
- Jedes neue Kommando hat Zweck, Voraussetzung, Eingabeerklärung und Ergebnis.
- Jede Variable/jeder Platzhalter besitzt nahe Erklärung und realistisches Beispiel.
- Pfadrollen und Defaults sind präzise gekennzeichnet.
- Secrets und sensible Daten fehlen.
- IDs, Status, Integrationsmodi und ungewöhnliche Abkürzungen besitzen Kontext.
- Generierte Dateien wurden nur über ihren Generator geändert.
- Claims bleiben innerhalb der aufgezeichneten Evidence-Grenze.
