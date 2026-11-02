# Neun-Punkte-Master-Abgleich

**Sprache:** [English](README.md) | Deutsch

Gesamtergebnis: partial. Prüfbare Korrekturen werden getrennt geliefert; offene Integritäts-/Runtime-/Dependency-Nachweise bleiben unten erhalten. Kein PR wurde gemergt und keine Repository-Regel angewendet. Das konfigurierte Standardinventar bleibt exakt 100 Fälle. Bestehende Checkout-Änderungen und fremde Worktrees wurden erhalten.

## Revisionen und Lieferung

| Repository | Basis | Task-Lieferung |
| --- | --- | --- |
| Connector |430d3194fa04ca4aafcdaef6aeb256d21dc18f0c |Dieser Task-Branch und sein separater Draft-PR |
| Framework |91145b7ba721bdec4e89af754cf40bf496fd2a08 |[PR159](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/159),624de56a6c2fa08c4369783a6d01b7e6f651da8f |
| MRTS |8a6bb546c4c81d8ffc7be801dceac60c6925685f |[PR5](https://github.com/Easton97-Jens/MRTS/pull/5),bf756a403ead39863cc15a81b5608e2b6062435d |

Parent wählt jetzt bereits integriertes Framework 91145b7ba721bdec4e89af754cf40bf496fd2a08 statt f11d4617ff98ad615c72c1b6672fc386394db41e. Enthalten sind TLS-Untergrenze[PR154](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/154) und Python-Patch[PR156](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/156). Der Stand repräsentiert ausdrücklich nicht die ungemergten Korrekturen aus PR159. Integrationsreihenfolge bleibt Framework zuerst; nach separat genehmigter Integration den tatsächlichen Merge-SHA in Parent pinnen, Projektionen regenerieren und das endgültige eingecheckte Paar prüfen. Kein Merge-SHA wurde erfunden.

Getrennte laufende Arbeiten: Framework-Drafts[PR155](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/155),[PR157](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/157),[PR158](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/158). Ihre Wartungs-/Python-/Bootstrap-Änderungen wurden weder erneut implementiert noch als integriert angenommen. Master-Referenzen wurden vor Lieferung erneut aktualisiert und blieben auf den obigen Basen.

## Anforderungszuordnung

| Punkt | Status und tatsächlicher Nachweis | Verbleibende Grenze / nächster Schritt |
| --- | --- | --- |
|1 Ausgangszustand und Regeln |Lokale Parent-/Framework-/MRTS-Zustände und Worktrees geprüft; Remote-Referenzen, Gitlinks und PR-Abstimmung erneuert; Arbeit isoliert. Ausdrückliche lokale Sonar-Ausnahme beachtet. |Task-Branches und externe Nachweise erhalten; keine destruktive Bereinigung. |
|2 Framework-Korrekturen/Pin |154/156 bereits integriert; Generator mit festem Register aktualisierte Parent-Gitlink, Versionslock und registrierte Workflow-Referenzen auf91145; Check meldet keine Änderungen;55 Pin-/Toolchain-Tests bestehen. |159 und Wartung157/158 bleiben PRs. Statisches check-python-version-contract scheitert an migrierten Workflow-/Bootstrap-Verträgen, die separat158 bearbeitet; keine konkurrierende Korrektur. Endgültiger Merge-SHA-Pin/Paar erfordert genehmigte Integration. |
|3 Traefik-Auth-Vorbereitung |Entfernte Connector-Capture-/Manifestpfade verwenden Framework-source_path; Source-Location-Regression mit getrennten Checkouts besteht unter echter Offline-Zulassung. |Vollständige Vorbereitung scheitert weiterhin mit Sealed Traefik profile differs;10/19 historische Repository-Objekte weichen ab. Registry-/Profil-/Export-Guards erhalten; unterstützte Archivregenerierung und geprüften Quellvertrag bereitstellen. Kein manuelles Archivumschreiben oder Hostanspruch. |
|4 Inheritance und Hostanleitung |Fünf Parent-Policy-Inhalte geprüft; Katalog/Templates und Framework-Vererbungspins erneuert; nativer Parent-Inheritance-Validator besteht. Anleitung erfasst147/437 integriert und436 ungemergt geschlossen. Historischer November1-Beleg vorhanden. |Vollständige native Prüfung gegen aktuell gepinnte Kinder bleibt nicht bestanden; tatsächliche MRTS-Kind-Digests bleiben wegen eng freigegebenem reinen Testumfang unverändert. Kein frischer NGINX-/Envoy-Hostlauf des endgültigen Paars. |
|5 Apache-Dokumentation |EN/DE-Architektur und Apache-Anleitung entsprechen progressiver Weiterleitung vor EOS, Commit-Grenze und engineeigenen Inspection-Limits. Kein Produktquelltext geändert. Native Sprachpaar-/Linkprüfungen bestehen. |Dokumentations-/Quellnachweis, keine neue Runtime-Qualifikation. |
|6 Coverage/Abhängigkeiten |Echte gezielte Python-, vier Go-Modul- und Common-/gcov-Werte mit verfügbaren Branch-Daten; Quelldigests/Selektoren/Ausschlüsse erfasst. Begrenztes Komponenten- und installiertes Paketmetadaten-Inventar erstellt. x/net/html fehlt im tatsächlichen Envoy-Buildgraphen. |Vollständiger Python-Speziallauf scheiterte nach 56 Erfolgen; spätere Caller-Fixture-Korrektur hat 22 Erfolge, Gesamtlauf nicht wiederholt. Generisches Broker-Modul bleibt 45/46. Native Tupelupdates/Erreichbarkeit und vollständige native/Binär-/Container-SBOM bleiben offen. Sonar-Coverage-Ausnahme/-Import unverändert. |
|7 Merge-Prüfungen |Live-Vorher-/Nachher-JSON und eigenständige additive Master-Anlagevorlagen vorbereitet; bestehender Schutz erhalten; Ereignisse, Forks, Pfadfilter, doppelte Namen und Beratungs-/manuelle Grenzen geprüft. |Vorlagen NICHT ANGEWENDET. Gesonderte Adminfreigabe nötig; klassische Branch-Protection liefert 403. Keine manuellen Host-/H2/H3-Kampagnen verpflichtend gemacht. |
|8 FIFO/Einrichtung/MRTS |FIFO-Importstart vom unveränderten 2s-Operationswatchdog getrennt;27 Cold-Cache-Artefakt-/Receipt-/Fixture-Tests bestehen. Ursprünglicher Ubuntu-Framework-Strukturvalidator besteht nach ignorierter nicht geheimer Einrichtung. MRTS-Governance exakt30/30 nach einzeiliger Anpassung an vorhandene Diagnose; alle fünf gelieferten PR5-Checks bestehen. |Lokales Python 3.14.4 bedeutet keine exakte MRTS-CI3.14.6-Parität; GitHub-Governance-Lane liefert eigenen aktuellen Head-Nachweis. Keine MRTS-Korpus-/Produkt- oder Gitlink-Änderung. |
|9 Verifikation/Lieferung |Getrennte Drafts, Sprachpaar-Nachweise, native Generatoren/Prüfungen und unabhängige begrenzte Patchprüfung; keine eingeführten wesentlichen Befunde. Kein Master-/Main-Push, Force-Push, Merge oder Schutzbypass. |Gesamtergebnis partial; CI des aktuellen Heads gesondert bewerten, offene Punkte nicht durch allgemeine grüne CI schließen. |

## Tatsächliche Coverage

| Umfang | Beobachtete Coverage | Bedeutung |
| --- | --- | --- |
|Parent Python,116 benannte Tests |59/6552 Zeilen(0,90%);16/2240 Branches(0,71%) |33 tatsächliche Parent-Dateien; Framework-Code ausgeschlossen, ungetestete operative Parent-Dateien erhalten. |
|Envoy Go |1104/3971 Statements(27,80%) |Bestehende exakte Selektoren, alle Standard-Build-Pakete erhalten. |
|Traefik native Go |586/959 Statements(61,11%) |Dieselbe begrenzte Auswahl. |
|Traefik composite Go |383/563 Statements(68,03%) |Dieselbe begrenzte Auswahl. |
|Traefik observer Go |300/752 Statements(39,89%) |Dieselbe begrenzte Auswahl. |
|Common native |2869/4290 Zeilen(66,88%);1903/3977 Branches(47,85%) |Vereinigung echter gcov-Beobachtungen nach Parent-Quelle/Zeile/Branch über erzeugte Binärdateien. |

Go-Profile liefern Statement-Coverage, keine Branch-Zahlen. Kein beliebiges Ziel hinzugefügt. Die Rohmessung bindet Parent 430d3194 und damalige nicht eingecheckte Framework 91145-Quellen über erfasste SHA-256; spätere Fixture-Metadaten qualifizieren kein anderes Paar rückwirkend. Damit ist die Lücke fehlender tatsächlicher begrenzter Messung geschlossen; breite Python-Ausführung, Host-Coverage und Analyseimport bleiben getrennte Lücken. Bestehender Sonar-Coverage-Ausschluss bleibt erhalten.

## Validierung und Nachweise

Maschinenlesbare Nachweise und Prüfbegründung: [coverage-summary.json](coverage-summary.json),[component-inventory.json](component-inventory.json),[dependencies.de.md](dependencies.de.md),[rules-review.de.md](rules-review.de.md). Leserberichte besitzen deutsche Begleitdateien. Rohartefakte bleiben im privaten konfigurierten Run-Bereich, Run master-reconcile-20261102; nur begrenzte Zusammenfassungen sind versioniert.

Der vollständige Python-Lauf stoppte nach 56 erfolgreichen Ausführungen an der alten geschützten Caller-Fixture. Diese Testeingabe wurde anschließend mit dem exakten letzten Inline-Aufrufer aus Parent f5523da040bd6325b369269ada074be6ba069c4f unter Erhalt der Permission-Erwartungen korrigiert. Tatsächliche geschützte Runtime bleibt blockiert: Der unveränderliche Broker8ae707d72f1a8acb25d239e55e28a73cbc7522b1 liest den aktuellen dünnen Parent-Wrapper, verlangt aber den historischen Inline-Job-/Concurrency-Vertrag. Ablehnung erfolgt vor Artefaktdownload/Build/Root-Zulassung. Historische Testkorrekturen reparieren diese Delegationskette nicht.

Lokale Checker-/Runtime-Ausgabe belegt ausschließlich ihre genannte Ebene. Keine frische Hostkampagne, vollständige H2/H3-Abnahme, umfassende Sicherheitsfreigabe oder endgültige Qualifikation des korrigierten Commitpaars wird behauptet.

Lokale Sonar-Secrets-Prüfung aufgrund ausdrücklicher Benutzeranweisung nicht ausgeführt.
