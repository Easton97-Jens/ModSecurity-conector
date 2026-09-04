# Geschützte NGINX-Runtime-Infrastruktur für exakte Heads

**Sprache:** [English](protected-exact-head-nginx.md) | Deutsch

Diese Änderung bereitet eine separat geprüfte, geschützte Base-Steuerung für
den nativen NGINX-Exact-Head-Test von `modsecurity_use_error_log` vor. Dies ist
ausschließlich Vorbereitung — keine Merge-Autorisierung.

## Vertrauensgrenze und Hosted-Gate

Dispatcher und privilegierter Launcher stammen aus dem geschützten Base-
Branch. Sie lösen einen offenen Pull Request über die GitHub-API auf, lassen
genau eine vollständige unveränderliche Candidate-SHA als Daten zu und
checken ausschließlich diese SHA aus. Der Candidate-Build läuft unprivilegiert.
Der geschützte Launcher besitzt die Runtime-Zellen; der Collector erfasst
hostseitige Prozessidentität, Artefaktprovenienz, Callback-/JSONL-Beobachtungen,
WAF-Entscheidungen und den finalen Exit-Code. PR-gesteuerte Workflows,
Launcher, Collector, Evidence-Pfade, Secrets und Host-Sockets sind keine
vertrauenswürdigen Eingaben der privilegierten Zelle.

Der privilegierte Launcher darf nur durch ein obligatorisches Host-Gate
zugelassen werden. Auf einem dedizierten geschützten Runner muss ein
Administrator einen root-eigenen, nicht beschreibbaren Bootstrap unter
`/usr/local/libexec/modsecurity-protected-exact-head/run-exact-base-launcher`
vorinstallieren. Dieser Bootstrap muss das angeforderte geschützte Base-Git-
Objekt prüfen und Launcher sowie Helper vor der Ausführung in einen root-
eigenen temporären Snapshot kopieren. Fehlende oder abweichende Base-SHA,
veränderliche Source-Pfade, unsichere Eigentümer/Rechte und eine nicht
vertrauenswürdige Umgebung müssen abgelehnt werden. Der Workflow beweist nicht,
dass dieses Host-Gate vorhanden ist; die Hosted-Umgebung muss diese
Voraussetzung vor der Zulassung von Runtime-Evidence erfüllen.

Callback- und JSONL-Records sind von Candidate-Code ausgegebene
Beobachtungen. Sie werden auf Schema und Korrelation geprüft, sind aber keine
kryptografisch oder provenance-authentifizierten semantischen Attestierungen:
Ein bösartiger Candidate könnte ihre Inhalte nachahmen. Die unabhängig root-
seitig beobachtete Prozessidentität, der transportseitige HTTP-403 und der
Exit-Status bilden die vertrauenswürdige Grenze; die semantische Candidate-WAF-
Entscheidung und Callback/JSONL bleiben begrenzte, nicht vertrauenswürdige
Beobachtungen. Der Collector-Status lautet `validated_observations`; seine
strukturierte Evidence markiert Callback/JSONL als
`candidate_scratch_untrusted` und die root-seitige HTTP-Beobachtung als
`root_pidfd_network_namespace`. Linux-`pidfd` plus `setns(CLONE_NEWNET)` bindet
das root-seitige HTTP-Kind an den validierten Network-Namespace. PID- und
Namespace-Lifetime-Prüfungen müssen am exakten Hosted-Head abgeschlossen sein,
bevor ein Runtime-Ergebnis als verifiziert bezeichnet wird.

Das Host-AppArmor-Profil ist absichtlich `flags=(unconfined)`. Es dient nur
der Zulassung des Host-User-Namespace und der Validierung des Profil-Labels,
nicht als Zusage einer MAC-Einschränkung. Namespace-Isolation,
Capability-Begrenzung und `no_new_privs` sind getrennte Kontrollen und müssen
unabhängig validiert werden.

Die beiden frischen Zellen verwenden dasselbe exakte Candidate-Modul mit
`modsecurity_use_error_log` on und off. Die Evidence muss Transaktions-
Korrelation, getrennte Master-/Worker-Identitäten, gleichwertige beobachtete
Candidate-WAF-Entscheidungen und den erwarteten Callback-/JSONL-Unterschied
zeigen. Jede fehlende Voraussetzung oder Exit 77 ist ein Fehler beziehungsweise
ein externer Blocker, kein Erfolg.

## Aktueller Bereitschaftsstand

Source-Contracts und lokale Negativkontrolltests werden auf einem separaten
Branch vorbereitet. Im Repository sind derzeit weder eine geschützte GitHub-
Environment noch ein dedizierter gelabelter Runner für diese Steuerung
konfiguriert. Daher wird kein gehostetes Exact-Head-Ergebnis, keine
unabhängige Attestierung und keine Merge-Bereitschaft behauptet. Vor einem
manuellen geschützten Base-Dispatch müssen Administratoren Environment-
Reviewer, Runner-Labels, Paket-/Tool-Voraussetzungen, Zugriffsregeln und das
root-eigene Exact-Blob-Host-Gate einrichten.

Der Candidate-PR bleibt eine getrennte Auslieferung. Diese Vorbereitung ändert
weder seine Produktreparatur noch Framework/MRTS-Source, Gitlink,
Abhängigkeiten, Branch-Schutz oder bestehende Bypass-Kontrollen.

## Validierungsvertrag

Die lokale Validierung umfasst Dispatcher-Identität und SHA-Admission,
Artefakt-Manifest-Bindung, Launcher-Pfad- und Descriptor-Kontrollen,
Collector-Schema und Negativsubstitutionen, statische Workflow-
Security-Contracts, Shell-Syntax, Python-Kompilierung und Action-Pin-Prüfung.
Die abschließende Evidence muss aus einem frischen geschützten Base-Dispatch
gegen die aus GitHub zurückgelesene Candidate-Head-SHA stammen und das
vollständige On/Off-Evidence-Schema enthalten. Lokaler Source-Contract, ein
fehlendes Host-Gate, Candidate-Callback/JSONL-Text oder ein früherer Head
können diese Evidence nicht ersetzen.

Ausschließlich Vorbereitung — keine Merge-Autorisierung.
