# FND-PARENT-0020 — Traefik-Native-Middleware-UDS-Tests überschritten unter dem genehmigten temporären Root die AF_UNIX-Pfadlänge

## Klassifizierung

| Feld | Wert |
| --- | --- |
| ID | FND-PARENT-0020 |
| Kategorie | test_failure |
| Repository / Ownership | parent / parent |
| Priorität | P1 |
| Severity | not_applicable |
| Confidence | reproduced |
| Status | fixed |
| Feasibility | feasible_now |
| Release-Blocker | false |
| Sicherheitsrelevant | false |
| Connector / Profil | Traefik / native-traefik-middleware |
| Protokoll | AF_UNIX pathname length in the Go UDS test harness |

## Zusammenfassung

Das fokussierte native-middleware-Go-Target konnte seine UDS-Protokollassertions
nicht ausführen, wenn TMPDIR der erforderliche private externe Projekt-Root
war. Go-Testings t.TempDir() fügte eine lange Testkennung ein und ließ
engine.sock die AF_UNIX-Pfadgrenze überschreiten, bevor eine
Testprotokollaktion lief.

## Beobachtetes und erwartetes Verhalten

Vor der Korrektur endete das Target mit Code 2. Mehrere Tests erreichten
net.Listen("unix", socketPath) und schlugen für Pfade unter
/var/tmp/codex/ModSecurity-conector/tmp/TestUDSEngine.../001/engine.sock mit
bind: invalid argument fehl. Es war noch keine Middleware-/Session-Assertion
gelaufen.

Die fokussierten UDS-Tests müssen unter dem genehmigten externen TMPDIR laufen,
einen Socketpfad innerhalb der AF_UNIX-Grenze binden, die Temporary-Root-Policy
bewahren und nur ihr eigenes privates Testverzeichnis entfernen.

## Auswirkung und Scope

Ein verpflichtendes fokussiertes Regressionstarget war in der autorisierten
Storage-Konfiguration nicht verfügbar und ließ UDS-Protokoll- und
Middleware-Verhalten unvalidiert. Dies betrifft nur die Testharness-
Infrastruktur: Kein Produktions-Request-Pfad und kein Runtime-UDS-Listener
wurden als betroffen nachgewiesen.

Betroffene Datei und Symbole:

- connectors/traefik/native_middleware/engine_uds_test.go
- startUDSTestServer
- newUDSTestSocketPath

Voraussetzungen sind das konfigurierte
TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp, die Verwendung von
testing.T.TempDir() und ein resultierender Pfad über der Plattformgrenze für
AF_UNIX.

## Grundursache und Korrektur

startUDSTestServer konstruierte seinen Socketpfad aus t.TempDir(). Das
Go-Framework enthält Testnamen und numerische Komponente, sodass absichtlich
lange Testnamen zusammen mit dem genehmigten TMPDIR die AF_UNIX-Kapazität
überschritten. Der Produktions-Runner ist nicht beteiligt.

Die fokussierte Korrektur verwendet os.MkdirTemp("", "uds-"), um ein kurzes
privates Child unter demselben konfigurierten TMPDIR anzulegen, registriert
t.Cleanup zum Entfernen genau dieses angelegten Verzeichnisses und konstruiert
engine.sock darunter. Sie wählt keinen globalen oder nicht genehmigten
Temporary-Root.

## Evidenz

Run-ID: 20260718T053406Z-pr-51-master-integration-546d9dc2

| Stufe | Artefakt | SHA-256 | Exit | Ergebnis |
| --- | --- | --- | ---: | --- |
| Pre-Fix-Reproduktion | /var/tmp/codex/ModSecurity-conector/runs/20260718T053406Z-pr-51-master-integration-546d9dc2/evidence/validation/go-native-middleware-long-tmpdir-regression.log | f960246f3e6052e1da13d960e8d647c660b39ec5bd47bd308b3e9f4117b2306c | 2 | UDS-Bind schlug vor den Protokollassertions fehl. |
| Post-Fix-Validierung | /var/tmp/codex/ModSecurity-conector/runs/20260718T053406Z-pr-51-master-integration-546d9dc2/evidence/validation/go-native-middleware-long-tmpdir-regression.log | f960246f3e6052e1da13d960e8d647c660b39ec5bd47bd308b3e9f4117b2306c | 0 | go test ./... und go vet ./... bestanden. |
| Fokussierte Sicherheitsprüfung | /var/tmp/codex/ModSecurity-conector/runs/20260718T053406Z-pr-51-master-integration-546d9dc2/evidence/validation/go-test-harness-security-review.md | 0ec987bc3e4e70f9e2dc7dc144d9feb44b2e2b0aa315a5897d99bcc3ed18d684 | 0 | Privater Testpfad und exaktes Cleanup sind bereits sicher; kein reportable Security Finding. |
| Exakter Commit-SHA | /var/tmp/codex/ModSecurity-conector/runs/20260718T053406Z-pr-51-master-integration-546d9dc2/evidence/validation/go-native-middleware-exact-2589c08.log | c244e81ed67a49158d2e5d6238371eb8f8b20dc83e33f91a25dcf1e0dad67920 | 0 | Commit 2589c085a1ed7bbb2c2033635f06e71f5f75fb8b führte Tests ohne Go-Testcache erneut aus und bestand. |
| Aktueller Master | /var/tmp/codex/ModSecurity-conector/runs/20260718T053406Z-pr-51-master-integration-546d9dc2/evidence/validation/master-c8ca0d9-traefik-regressions.log | 1f766b416d36f8f0ce35e7e904e8e3f50b57d1e80af1571e2cc9e59c164004af | 0 | Der gemergte Master c8ca0d92b630c18232b881855c4f5d1482568ea6 führte das Originaltarget ohne Cache erneut aus und bestand. |

Beide Stufen verwendeten:

~~~text
rtk env BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/runs/20260718T053406Z-pr-51-master-integration-546d9dc2/build TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR=/var/tmp/codex/ModSecurity-conector/runs/20260718T053406Z-pr-51-master-integration-546d9dc2/build/native-middleware GOCACHE=/var/tmp/codex/ModSecurity-conector/runs/20260718T053406Z-pr-51-master-integration-546d9dc2/cache/go-build GOMODCACHE=/var/tmp/codex/ModSecurity-conector/runs/20260718T053406Z-pr-51-master-integration-546d9dc2/cache/go-mod GOTOOLCHAIN=local GOWORK=off GO=go TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp make -C connectors/traefik test-native-middleware
~~~

Die Post-Fix-Verzeichnisauflistung zeigte kein uds-*-Child unter dem
konfigurierten Temporary-Root.

## Akzeptanz und Validierung

1. Das exakte Pre-Fix-fokussierte Go-Target besteht mit
   TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp.
2. Seine Stufen go test ./... und go vet ./... bestehen.
3. Unter dem konfigurierten TMPDIR bleibt kein uds-*-Verzeichnis zurück.
4. Die Änderung bleibt testharness-only und git diff --check besteht.
5. Der exakte finale PR-Head und der aktuelle Master behalten das bestehende
   Ergebnis.

Der Validierungsplan ist, dasselbe Target erneut auszuführen, die
Pfad-/Cleanup-Grenze des Helpers zu prüfen, das Ergebnis an den gepushten
PR-Head zu binden und es auf dem gemergten Master zu wiederholen.

## Abhängigkeiten, verwandte Records und Restrisiko

Die Current-Master-Verifikation ist abgeschlossen. FND-FRAMEWORK-0008 ist verwandt, weil es eine
getrennte produktive UDS-Pfadgrenze abdeckt; dieser Record hat eine eigene
Testharness-Ursache und Korrektur.

Die Korrektur betrifft nur Tests und validiert den verfügbaren nativen
Go-Harness. Für den getrennten Full-Lifecycle-Test bleibt ein echter
Traefik-Host-Binary nicht verfügbar. Es wurde kein Sicherheitsrisiko
akzeptiert.

## Historie

- 2026-07-18T06:14:59Z — Das ursprüngliche fokussierte Target schlug unter
  dem genehmigten externen TMPDIR mit Exit-Code 2 vor den
  UDS-Protokollassertions fehl.
- 2026-07-18T06:14:59Z — Das kurze os.MkdirTemp-Child und das exakte
  Test-Cleanup ließen dasselbe Target bestehen; es blieb kein uds-*-Child
  zurück.
- 2026-07-18T06:26:39Z — Commit
  2589c085a1ed7bbb2c2033635f06e71f5f75fb8b führte das Target mit
  GOFLAGS=-count=1 unter dem genehmigten externen TMPDIR erneut aus; Go test
  und vet bestanden.
- 2026-07-18T06:40:39Z — Der gemergte Master
  c8ca0d92b630c18232b881855c4f5d1482568ea6 führte das Originaltarget ohne
  Go-Testcache erneut aus; Go test und vet bestanden und es blieb kein
  uds-*-Child zurück.
