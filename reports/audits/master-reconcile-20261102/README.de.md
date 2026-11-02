# Neun-Punkte-Master-Abgleich

**Sprache:** [English](README.md) | Deutsch

Gesamtergebnis: partial. Prüfbare Korrekturen werden getrennt geliefert; offene Integritäts-/Runtime-/Dependency-Nachweise bleiben unten erhalten. Kein PR wurde gemergt und keine Repository-Regel angewendet. Das konfigurierte Standardinventar bleibt exakt 100 Fälle. Bestehende Checkout-Änderungen und fremde Worktrees wurden erhalten.

## Revisionen und Lieferung

| Repository | Basis | Task-Lieferung |
| --- | --- | --- |
| Connector |430d3194fa04ca4aafcdaef6aeb256d21dc18f0c |[PR440](https://github.com/Easton97-Jens/ModSecurity-conector/pull/440), dieser Task-Branch |
| Framework |91145b7ba721bdec4e89af754cf40bf496fd2a08 |[PR159](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/159),99e8d13cc1cf03f42cc887a4d5abf9e7c766e09b |
| MRTS |8a6bb546c4c81d8ffc7be801dceac60c6925685f |[PR5](https://github.com/Easton97-Jens/MRTS/pull/5),bf756a403ead39863cc15a81b5608e2b6062435d |

Parent wählt jetzt bereits integriertes Framework 91145b7ba721bdec4e89af754cf40bf496fd2a08 statt f11d4617ff98ad615c72c1b6672fc386394db41e. Enthalten sind TLS-Untergrenze[PR154](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/154) und Python-Patch[PR156](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/156). Der Stand repräsentiert ausdrücklich nicht die ungemergten Korrekturen aus PR159. Integrationsreihenfolge bleibt Framework zuerst; nach separat genehmigter Integration den tatsächlichen Merge-SHA in Parent pinnen, Projektionen regenerieren und das endgültige eingecheckte Paar prüfen. Kein Merge-SHA wurde erfunden.

Vor Lieferung erneut geprüfte getrennte Arbeiten: Framework[PR155](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/155) bleibt offen an0b3fd61835837a5a2563fe9b42297ab91e3d8981;[PR158](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/158) bleibt offen und wurde aufe948b5396540e7714b5dd8ff88ba4e8142f3e9e1 fortgeschrieben.[PR157](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/157) ist inzwischen ungemergt geschlossen, letzter Heade72cb90b9f88e9490cc35e15fa00977d4919d48d. Ihre Wartungs-/Python-/Bootstrap-Änderungen wurden weder erneut implementiert noch als integriert angenommen. Master-Referenzen blieben auf den obigen Basen.

## Anforderungszuordnung

| Punkt | Status und tatsächlicher Nachweis | Verbleibende Grenze / nächster Schritt |
| --- | --- | --- |
|1 Ausgangszustand und Regeln |Lokale Parent-/Framework-/MRTS-Zustände und Worktrees geprüft; Remote-Referenzen, Gitlinks und PR-Abstimmung erneuert; Arbeit isoliert. Ausdrückliche lokale Sonar-Ausnahme beachtet. |Task-Branches und externe Nachweise erhalten; keine destruktive Bereinigung. |
|2 Framework-Korrekturen/Pin |154/156 bereits integriert; Generator mit festem Register aktualisierte Parent-Gitlink, Versionslock und registrierte Workflow-Referenzen auf91145; Check meldet keine Änderungen;55 Pin-/Toolchain-Tests bestehen. |Gehostete CI lehnt91145 ab:156 änderte common.sh ohne Regenerierung der geprüften Inventarbindung.159 enthält die regenerierte Korrektur, ist aber ungemergt. Dies unterscheidet sich von den separat158 zugeordneten statischen Workflow-/Bootstrap-Vertragsfehlern. Endgültiger Merge-SHA-Pin/Paar erfordert genehmigte Integration. |
|3 Traefik-Auth-Vorbereitung |Entfernte Connector-Capture-/Manifestpfade verwenden Framework-source_path; Source-Location-Regression mit getrennten Checkouts besteht unter echter Offline-Zulassung. |Vollständige Vorbereitung scheitert weiterhin mit Sealed Traefik profile differs;10/19 historische Repository-Objekte weichen ab. Registry-/Profil-/Export-Guards erhalten; unterstützte Archivregenerierung und geprüften Quellvertrag bereitstellen. Kein manuelles Archivumschreiben oder Hostanspruch. |
|4 Inheritance und Hostanleitung |Fünf Parent-Policy-Inhalte geprüft; Katalog/Templates und Framework-Vererbungspins erneuert; nativer Parent-Inheritance-Validator besteht. Anleitung erfasst147/437 integriert und436 ungemergt geschlossen. Historischer November1-Beleg vorhanden. |Vollständige native Prüfung gegen aktuell gepinnte Kinder bleibt nicht bestanden; tatsächliche MRTS-Kind-Digests bleiben wegen eng freigegebenem reinen Testumfang unverändert. Kein frischer NGINX-/Envoy-Hostlauf des endgültigen Paars. |
|5 Apache-Dokumentation |EN/DE-Architektur und Apache-Anleitung entsprechen progressiver Weiterleitung vor EOS, Commit-Grenze und engineeigenen Inspection-Limits. Kein Produktquelltext geändert. Native Sprachpaar-/Linkprüfungen bestehen. |Dokumentations-/Quellnachweis, keine neue Runtime-Qualifikation. |
|6 Coverage/Abhängigkeiten |Vom Benutzer gewählte gezielte Messung geliefert: echte begrenzte Python-, vier Go-Modul- und Common-/gcov-Werte mit verfügbaren Branch-Daten; Quelldigests/Selektoren/Ausschlüsse erfasst. Begrenztes Komponenten- und installiertes Paketmetadaten-Inventar erstellt. x/net/html fehlt im tatsächlichen Envoy-Buildgraphen. |Historischer vollständiger Python-Speziallauf scheiterte nach56 Erfolgen; Abschluss oder Wiederholung liegt außerhalb des gewählten Messumfangs. Spätere Caller-Fixture-Korrektur hat22 Erfolge; generisches Broker-Modul bleibt45/46 als unabhängiger Fehler. Native Tupelupdates/Erreichbarkeit und vollständige native/Binär-/Container-SBOM bleiben offen. Sonar-Coverage-Ausnahme/-Import unverändert. |
|7 Merge-Prüfungen |Live-Vorher-/Nachher-JSON und eigenständige additive Master-Anlagevorlagen vorbereitet; bestehender Schutz erhalten; Ereignisse, Forks, Pfadfilter, doppelte Namen und Beratungs-/manuelle Grenzen geprüft. |Vorlagen NICHT ANGEWENDET. Gesonderte Adminfreigabe nötig; klassische Branch-Protection liefert 403. Keine manuellen Host-/H2/H3-Kampagnen verpflichtend gemacht. |
|8 FIFO/Einrichtung/MRTS |FIFO-Importstart vom unveränderten 2s-Operationswatchdog getrennt;27 Cold-Cache-Artefakt-/Receipt-/Fixture-Tests bestehen. Ursprünglicher Ubuntu-Framework-Strukturvalidator besteht nach ignorierter nicht geheimer Einrichtung. MRTS-Governance exakt30/30 nach einzeiliger Anpassung an vorhandene Diagnose; alle fünf gelieferten PR5-Checks bestehen. |Lokales Python 3.14.4 bedeutet keine exakte MRTS-CI3.14.6-Parität; GitHub-Governance-Lane liefert eigenen aktuellen Head-Nachweis. Keine MRTS-Korpus-/Produkt- oder Gitlink-Änderung. |
|9 Verifikation/Lieferung |Getrennte Drafts, Sprachpaar-Nachweise, native Generatoren/Prüfungen und unabhängige begrenzte Patchprüfung; keine eingeführten wesentlichen Befunde. Kein Master-/Main-Push, Force-Push, Merge oder Schutzbypass. |Gesamtergebnis partial; CI des aktuellen Heads gesondert bewerten, offene Punkte nicht durch allgemeine grüne CI schließen. |

## Tatsächliche Coverage

Der Benutzer wählte ausdrücklich eine gezielte Messung mit dokumentierten Grenzen:
116 benannte Python-Tests sowie die gemessenen vier Go-Module und Common/Native.
Diese Messungen erfüllen den gewählten Messauftrag. Abschluss oder Wiederholung
des vollständigen Spezialassessments mit977 Ausführungen ist kein
Abschlusskriterium dieses Coverage-Umfangs. Sein historischer Abbruch und
unabhängig relevante Fehler bleiben dokumentiert. CI-Pflichtprüfungen und die
Standardauswahl von100 Fällen bleiben unverändert.

| Umfang | Beobachtete Coverage | Bedeutung |
| --- | --- | --- |
|Parent Python,116 benannte Tests |59/6552 Zeilen(0,90%);16/2240 Branches(0,71%) |33 tatsächliche Parent-Dateien; Framework-Code ausgeschlossen, ungetestete operative Parent-Dateien erhalten. |
|Envoy Go |1104/3971 Statements(27,80%) |Bestehende exakte Selektoren, alle Standard-Build-Pakete erhalten. |
|Traefik native Go |586/959 Statements(61,11%) |Dieselbe begrenzte Auswahl. |
|Traefik composite Go |383/563 Statements(68,03%) |Dieselbe begrenzte Auswahl. |
|Traefik observer Go |300/752 Statements(39,89%) |Dieselbe begrenzte Auswahl. |
|Common native |2869/4290 Zeilen(66,88%);1903/3977 Branches(47,85%) |Vereinigung echter gcov-Beobachtungen nach Parent-Quelle/Zeile/Branch über erzeugte Binärdateien. |

Go-Profile liefern Statement-Coverage, keine Branch-Zahlen. Kein beliebiges Ziel hinzugefügt. Die Rohmessung bindet Parent 430d3194 und damalige nicht eingecheckte Framework 91145-Quellen über erfasste SHA-256; spätere Fixture-Metadaten qualifizieren kein anderes Paar rückwirkend. Damit ist die Lücke fehlender tatsächlicher begrenzter Messung geschlossen. Breitere Python-Ausführung liegt außerhalb des vom Benutzer gewählten Messumfangs; Hostqualifikation und Analyseimport sind nicht nachgewiesen. Bestehender Sonar-Coverage-Ausschluss bleibt erhalten.

## Validierung und Nachweise

Maschinenlesbare Nachweise und Prüfbegründung: [coverage-summary.json](coverage-summary.json),[component-inventory.json](component-inventory.json),[dependencies.de.md](dependencies.de.md),[rules-review.de.md](rules-review.de.md). Leserberichte besitzen deutsche Begleitdateien. Rohartefakte bleiben im privaten konfigurierten Run-Bereich, Run master-reconcile-20261102; nur begrenzte Zusammenfassungen sind versioniert.

### Zulassungssperre in gehosteter CI

Der historische Nachweis [ci-admission-38ebc633.json](ci-admission-38ebc633.json) bindet diese Untersuchung an Parent38ebc633 und Framework91145. Alle28 untersuchten einzeln fehlgeschlagenen Jobs lehnen `modules/ModSecurity-test-Framework/ci/lib/common.sh` vor den ausgewählten Tests/Builds/Runtime-Läufen ab. Framework156 änderte das kanonische Python3.14.8 auf3.14.10; sein Inventar erwartet weiterhin SHA-256 `3aa782dd117fdf66194861e5a1f97e492f13321db77129da79aadcec2e655e2c`, während die tatsächliche Quelle `8e39a221e044441e89753bfff64564579dcbc656bccf7d92368e518a2d7a59db` hat. Genau eine von528 Bindungen weicht ab. Es handelt sich um einen bestehenden Framework-Generierungsfehler, der durch das Parent-Pinupdate wirksam wird; er ist von158 getrennt. Beispielhafte unveränderliche Logs: [Scaffold-Zulassung](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41426394389/job/125213928621) und [Security-Zulassung](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41426394282/job/125213928012).

Der bestehende Wartungsgenerator regeneriert diese Bindung bereits in Framework159. Parent behält den ausgewählten integrierten91145, bis eine gesonderte Framework-Integration freigegeben wird; ein ungemergter oder erfundener Merge-SHA erfüllt die verlangte Integrationsreihenfolge nicht. Nach Übernahme des tatsächlich entstandenen Merge-Commits sämtliche betroffenen Checks erneut qualifizieren. Weitere Fehler hinter der Zulassung bleiben möglich.

Nach demselben frühen Abbruch fehlt Envoy/Traefik/lighttpd das Evidence-Verzeichnis `verified`; auch ihre Aufbewahrung der Fehlerbelege scheitert. Das [Fünf-Zellen-Aggregat](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41426394445/job/125215222415) lädt nur den Apache-Fehlerbeleg und lehnt ein Nichtverzeichnis ab. Diese beobachteten Framework-Fehlerpfadlücken bleiben offen; kein erfolgreicher Fünf-Zellen-Lauf wird abgeleitet. Aktive Framework159-Prüfungen bestanden an624de56a und alle fünf MRTS5-Checks anbf756a40; allgemeine grüne Checks schließen weder die dokumentierten lokalen Fehler noch sämtliche Befunde aus. Die anschließende Framework99e8d13-Folgekorrektur lagert nach gehostetem python:S3776-Feedback die unveränderte Witness-Pfadzuordnung aus, mit42 bestandenen Regressionen vor und nach der Änderung; gehostete Checks des neuen Heads bleiben vom alten Nachweis getrennt.

Der vollständige Python-Lauf stoppte nach 56 erfolgreichen Ausführungen an der alten geschützten Caller-Fixture. Diese Testeingabe wurde anschließend mit dem exakten letzten Inline-Aufrufer aus Parent f5523da040bd6325b369269ada074be6ba069c4f unter Erhalt der Permission-Erwartungen korrigiert. Tatsächliche geschützte Runtime bleibt blockiert: Der unveränderliche Broker8ae707d72f1a8acb25d239e55e28a73cbc7522b1 liest den aktuellen dünnen Parent-Wrapper, verlangt aber den historischen Inline-Job-/Concurrency-Vertrag. Ablehnung erfolgt vor Artefaktdownload/Build/Root-Zulassung. Historische Testkorrekturen reparieren diese Delegationskette nicht.

Lokale Checker-/Runtime-Ausgabe belegt ausschließlich ihre genannte Ebene. Keine frische Hostkampagne, vollständige H2/H3-Abnahme, umfassende Sicherheitsfreigabe oder endgültige Qualifikation des korrigierten Commitpaars wird behauptet.

Lokale Sonar-Secrets-Prüfung aufgrund ausdrücklicher Benutzeranweisung nicht ausgeführt.
