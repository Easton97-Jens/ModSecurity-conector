# Sicherheitsrichtlinie

**Sprache:** [English](SECURITY.md) | Deutsch

## Meldung einer Schwachstelle

Bitte eröffne für eine vermutete Sicherheitslücke kein öffentliches Issue und
veröffentliche keine Proof-of-Concept-Details. Verwende stattdessen
[GitHub Private Vulnerability Reporting](https://github.com/Easton97-Jens/ModSecurity-conector/security/advisories/new).
Die Private-Reporting-Funktion dieses Repositorys ist der vorgesehene
vertrauliche Kanal.

Füge eine knappe Beschreibung, die betroffene Version, den Commit oder Branch
soweit bekannt, sichere Reproduktionsschritte, das erwartete und beobachtete
Ergebnis sowie eine klare Einschätzung der möglichen Auswirkung bei. Schwärze
Tokens, Zugangsdaten, private Daten und Exploit-Payloads im Bericht und in
Anhängen.

## Unterstützte Versionen

Sicherheitsberichte werden gegen den aktuellen `master`-Branch bewertet. Für
Sicherheitsfixes ist derzeit keine ältere Release-Linie als unterstützt
deklariert. Wenn sich das Problem nur auf einer älteren Revision reproduzieren
lässt, nenne diese Revision und prüfe, ob auch das aktuelle `master` betroffen
ist.

## Geltungsbereich und sichere Forschung

Der Bericht soll versionierte Inhalte dieses Repositorys oder dessen
veröffentlichte GitHub-Actions-Konfiguration betreffen. Teste keine Systeme,
die dir nicht gehören oder für deren Prüfung du keine Erlaubnis hast, greife
nicht auf Daten anderer Benutzer zu und vermeide jede Handlung, die Dienste
stören oder ein Datenschutzrisiko schaffen könnte.

## Was als Nächstes passiert

Maintainer bewerten einen privaten Bericht, können um Klarstellung bitten und
koordinieren bei bestätigtem Befund einen Fix oder eine Mitigation. Der
Zeitpunkt einer Offenlegung wird, soweit praktikabel, mit dem Meldenden
abgestimmt. Diese Richtlinie sagt keine Antwortzeit zu.

## Öffentliche Kanäle sind nicht vertraulich

GitHub-Issues, Pull Requests, Discussions und öffentliche Kommentare sind
keine vertraulichen Meldekanäle. Veröffentliche dort keine Secrets,
personenbezogenen Daten oder Exploit-Details. Nutze für Sicherheitsberichte den
oben genannten privaten Meldekanal.
