# Behebung der verbleibenden Security-Scan-Findings

**Sprache:** [English](CR-20260930-security-scan-remaining-findings.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260930-security-scan-remaining-findings |
| Datum (UTC) | 2026-09-30 |
| Basis-Revision | 9bc87cbdb600b09c6edd02667a75b117a1f09eea |
| Lieferziel | Pull Request gegen `master`; kein Merge |

## Motivation und Problemstellung

Der bereitgestellte ModSecurity-conector-Scan enthielt drei validierte Findings. Das NGINX-`error_page`-Intervention-Finding ist in der Basis-Revision bereits durch den gemergten PR #391 behoben; diese Änderung dupliziert den Code daher nicht. Die verbleibende Arbeit entfernt einen HAProxy-Fehlerfortsetzungsweg aus vier Closed-Default-SPOE/SPOP-Profilen und härtet die Identität von Response-Companion-UDS-Peer und -Pfad, bevor ein Response-Observer `CLAIM` sendet.

## Akzeptanzkriterien

Das positive NGINX-Interventionsverhalten bleibt durch die Basis-Revision bereitgestellt. Jedes aufgeführte HAProxy-Profil muss `fail-mode=closed` beibehalten und `option continue-on-error` weglassen. Ein Response-Companion darf nur unter einem privaten Verzeichnis starten, dessen vollständige Ancestor-Chain gegen Austausch durch andere UIDs geschützt ist. Envoy- und Traefik-Response-Observer müssen den verbundenen UDS-Server unter Linux mit `SO_PEERCRED` vor `CLAIM` authentisieren, fehlende oder abweichende UID/GID-Credentials ablehnen und ohne Linux-Credential-Mechanismus fail-closed fehlschlagen.

## Implementierungsentscheidung und Begründung

Die HAProxy-Änderung löscht nur die Error-Continuation-Option aus den vier betroffenen Profildateien und ergänzt einen fokussierten Regressions-Contract, der die Closed Defaults absichert. Die Common Runtime behält ihre vorhandenen Private-Leaf-Prüfungen und erweitert sie über die kanonische gesamte Verzeichniskette: Nicht schreibbare Ancestors werden akzeptiert, schreibbare Ancestors müssen sticky sein und das eigene Child gegen Austausch durch andere UIDs schützen.

Die Envoy- und Traefik-Observer verwenden explizite erwartete UID/GID-Paare. Ohne Konfiguration gelten die effektive UID/GID des Observer-Prozesses; eine explizite Identität verlangt beide Felder und erlaubt bewusst den Wert null. Der Produktionscode von Envoy enthält keinen unauthentisierten Dial-Einstiegspunkt. Der vorhandene ungeprüfte Dial bleibt ausschließlich testintern für Protocol-Framing-Coverage. Der Observer authentisiert unmittelbar nach dem Connect und bevor `CLAIM`-Bytes geschrieben werden.

## Geänderte Dateien

- common/runtime/response_companion_transport.c
- tests/response_companion_transport_test.c
- examples/haproxy/spoe-spop/{strict,safe,off,all}/spoe.cfg
- tests/test_haproxy_spop_peer_isolation_contract.py
- connectors/envoy/ext_proc/internal/responseobserver/{protocol.go,service.go,peercred_linux.go,peercred_other.go,peercred_linux_test.go,protocol_test_helper_test.go}
- connectors/envoy/ext_proc/cmd/msconnector-envoy-response-observer/main.go
- connectors/traefik/response_observer/{observer.go,observer_test.go,peercred_linux.go,peercred_other.go}
- Connector-Source-Maps, Response-Observer-Dokumentation, fokussierte CI-Workflows und dieser gekoppelte Record

## Ausgeführte Befehle

Die GitHub-Connector-Inspektion verglich den vorbereiteten Scope mit der Basis-Revision 9bc87cbdb600b09c6edd02667a75b117a1f09eea und bestätigte, dass die NGINX-`error_page`-Behebung bereits in der Basis vorhanden ist. Die vorgeschlagenen fokussierten CI-Befehle sind:

```sh
python3 -m unittest -v tests.test_haproxy_spop_peer_isolation_contract
go test -mod=readonly -count=1 ./internal/responseobserver
go test -mod=readonly -count=1 -run 'a^' ./cmd/msconnector-envoy-response-observer
go test -mod=readonly -count=1 ./...
```

Sie sind in den PR-Workflows konfiguriert. Aus diesem Windows-Workspace werden sie nicht als lokal bestanden behauptet.

## Security-Auswirkung

Die HAProxy-Profile machen aus einem nicht verfügbaren oder fehlerhaften SPOE-Agenten keinen Continuation-Pfad mehr, wenn sie als Closed Default gekennzeichnet sind. Die Common Runtime lehnt einen Socket-Parent ab, der nur durch ein privates Leaf unter einem schreibbaren, nicht-sticky Ancestor geschützt ist. Die Go-Observer binden ihre Response-Companion-Trust-Entscheidung vor dem Claim von Protocol-State an Kernel-bereitgestellte Peer-Credentials; ein Credential-Fehler wird zum bestehenden Pre-Commit-503-Fail-Closed-Verhalten.

## Runtime-Evidence

Die neuen Regressionstests belegen die erwarteten Source- und Protocol-Grenzen. Linux-Tests verwenden einen echten lokalen Unix-Listener und prüfen, dass ein Peer mit abweichender Identität vor dem Reject null Request-Bytes erhält. Der C-Transporttest erzeugt ein privates Child unter einem schreibbaren, nicht-sticky Ancestor und verlangt einen Startup-Fehler. Dies sind begrenzte Komponententests, keine Live-Acceptance-Behauptung für Envoy-, Traefik-, HAProxy- oder NGINX-Deployments.

## Bekannte Einschränkungen

Linux-`SO_PEERCRED` authentisiert die vom Kernel gemeldete UID/GID des UDS-Peers. Es attestiert weder Executable noch Dateiintegrität, MAC-Label oder User-Namespace-Mapping. Gleiche Unix-IDs bilden eine gemeinsame Vertrauensdomäne. Die Directory-Chain-Prüfung bewertet Ownership, Mode-Bits und Sticky-Schutz; Deployments müssen zusätzlich POSIX-ACLs oder Mount-Policies vermeiden, die einer anderen Identität Ersetzungsrechte geben.

## Verbleibende Risiken

Die Änderung enthält bewusst keinen Nicht-Linux-Credential-Fallback; nicht unterstützte Deployments schlagen fail-closed fehl, statt stillschweigend fortzufahren. Betreiber mit einem Companion unter einer anderen Unix-Identität müssen beide erwarteten IDs konfigurieren. Die fokussierten Tests beweisen weder alle Response-Phase-Host-Verhalten noch beliebige Filesystem-Namespaces oder eine Live-SPOE-Agent-Fehlerinjektion. Die Host-Level-Evidence der NGINX-Basisbehebung bleibt von diesem PR getrennt.

## Nicht ausgeführte Prüfungen mit Begründung

Die gewünschte SonarQube-Analyse konnte in diesem Workspace nicht laufen: Sonar-CLI und ein SonarQube-Connector-Tool waren nicht verfügbar, außerdem war der lokale Container-Daemon nicht erreichbar. Es wurden keine Credentials, Pakete oder Service-Konfigurationen verändert, um diese Einschränkung zu umgehen. Lokale C-/Go-Ausführung war aus dem read-only Windows-Workspace ebenfalls nicht verfügbar; die fokussierten Befehle werden deshalb an Exact-Head-GitHub-Actions delegiert.

## Finaler Diff- und Review-Status

Der Diff beschränkt sich auf die zwei verbleibenden Findings, ihre Regression-Coverage und Deployment-Dokumentation. NGINX-Quellen bleiben bewusst unverändert, weil #391 bereits die aktuelle Basis ist. Ein Review prüft besonders, dass UDS-Authentisierung vor `CLAIM` erfolgt, nicht unterstützte Plattformen fail-closed bleiben und alle vier HAProxy-Profile die Continuation-Option weglassen. PR-CI und Reviewer-Freigabe stehen bei Erstellung dieses Records noch aus.
