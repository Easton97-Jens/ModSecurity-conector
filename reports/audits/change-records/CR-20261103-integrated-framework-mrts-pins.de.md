# Change Record: CR-20261103-integrated-framework-mrts-pins

**Sprache:** [English](CR-20261103-integrated-framework-mrts-pins.md) | Deutsch

Tatsächlich getrennt integrierte Framework-/MRTS-Abhängigkeiten auswählen.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261103-integrated-framework-mrts-pins |
| Datum (UTC) | 2026-11-03 |
| Basis-Revision | `829229c53a2547f8966aa6d776f00f49f4aa61cc` |

## Motivation und Problemstellung

Die ausdrücklich genehmigte Reihenfolge hat tatsächliche Squashes erzeugt: MRTSee2174431c4edf97e66afe32558ce8454deb2397 und Framework189c42d0b4362fccc732d2480935348220c287da. Der nötige Dokumentationsfolge-PR #168 wurde tatsächlich als62b411e073551ef0fef22ab3d372e2489f2ae168 integriert; Parent wählt dieses finale Frameworkobjekt und MRTS statt des alten bb6c758/75394f9-Paars oder eines PR-Heads.

## Akzeptanzkriterien

Gewöhnlichen Gitlink und beide Lockrevisionen über native Verträge aktualisieren. Alte/neue Gitlinkherkunft, exakte registrierte Projektionen, unveränderte geschützte Broker-/Compositeidentitäten und Produkt-/Komponentenwerte prüfen. Frische Head-CI und spätere echte Endpaarlaufzeit verlangen. Der strikte Parent-Dokumentationsconsumer fand nach der ersten Projektion vier Umschalterzeilen; der reguläre Framework-Sechszeilenfolgefix repariert Umschalter und technische JSON-Beispielparität ohne Prüfregeländerung.

## Implementierungsentscheidung und Begründung

Bestehende Updater-Gitlinkprimitive, explizit geprüfte MRTS-Übergabe und Kandidatenverifier gegen unveränderliche tatsächliche Framework-Gitdaten verwenden. Kein Publisherdispatch und keine pauschale SHA-Ersetzung. Nativen Compiler-Guide-Generator auch bei unverändertem Ergebnis ausführen.

## Geänderte Dateien

Parent-Gitlink, zentraler Project-Versions-Lock und22 registrierte Workflow-/Callerprojektionsdateien sowie dieses EN/DE-Paar. Feste Komponentenziele und erzeugte Compiler-Guides wurden verarbeitet, bleiben bei gleichen Komponentenwerten byteidentisch. Framework-/MRTS-Quellen und unveränderliche Broker-/Compositeidentitäten bleiben unverändert.

## Ausgeführte Befehle

RTK mit regulärem CPython3.15.2: Kandidatenverifier vor Übergabe mit explizitem MRTS; Synchronisierer --validate, --sync und --check; Defaultverifier nach Lockaktualisierung; Compiler-Guide-Generator; trusted-base --verify-primary; Whitespace. Alle Aufrufe Exit0. Exakte argv/Ergebnisse: Integrationslauf20261103T175654Z-integration, parent-pin-sync/commands.json und parent-pin-sync-final/commands.json. Postcommit-Reader, Inventar, Quellen/Vererbung, Projektion und Hosted-Checks erhalten getrennte tatsächliche Revisionsbelege.

## Security-Auswirkung

Im geschlossenen Fünfschlüssellock ändern nur framework_sha und mrts_sha; Python3.15.2, Go1.27.3 und Schema bleiben gleich. Tatsächliche alte/neue Frameworkobjekte belegen beide verschachtelten Selektionen vor Schreibzugriff. Broker8ae707d72f1a8acb25d239e55e28a73cbc7522b1 und geschütztes Framework99a7985c1be92a2297b1b59208f64df6768f2cbf bleiben getrennt und unveränderlich. Kein Gate, Recht oder Herkunftsguard geschwächt.

## Runtime-Evidence

Diese Pintransformation behauptet keinen Hostverkehr.13 frische gezielte H2/H3-Invokationen folgen nach tatsächlicher Parentintegration mit gleichem Launcher-Preflight, ursprünglicher Buildherkunft/Zulassung, kanonischen Originalen/Seals und Cleanup. Alte Kandidatenläufe bleiben historisch.

## Bekannte Einschränkungen

Vollständige aktuelle Head-CI und tatsächliche Master-CI sind getrennte Pflichtbelege. Bekannte C++20/23-Advisorybefunde benötigen nach Projektion frischen Quellen-/Flow-/Analyseinputabgleich; keine pauschale Akzeptanz oder Alles-grün-Aussage.

## Verbleibende Risiken

Unveränderte Quellen-/Buildkonfiguration allein beweist weder Protokollverhalten, geschützte Brokerlaufzeit noch vollständige Coverage-/SBOM-Abnahme. Vollabnahme/Reset/Multiplex und zusätzliche Profil-/Recoveryziele bleiben getrennt.

## Nicht ausgeführte Prüfungen mit Begründung

Lokale Sonar-Vorprüfung, Installation und Authentifizierungsreparatur bleiben ausdrücklich ausgesetzt. Keine Vollkampagne, Publisher-/geschützten Dispatches, Adminregeländerung, direkter Master- oder Forcepush. Saubere eingecheckte Reader und finale Hostbelege folgen der notwendigen Commit-/Integrationsgrenze.

## Finaler Diff- und Review-Status

Native trusted-base-Rekonstruktion und Whitespace bestanden. Finale Staged-Rekonstruktion, eingecheckte Pinkette und unabhängiges Review sind vor Veröffentlichung/Merge erforderlich und in PR-Belegen erhalten. Nur eigene Pfade stagen; fremde Änderungen, Worktrees und Nachweise erhalten.
