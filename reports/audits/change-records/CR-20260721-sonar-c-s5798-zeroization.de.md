# Change Record: Portable C-secure-zero-Härtung für SonarQube Cloud c:S5798

**Sprache:** [English](CR-20260721-sonar-c-s5798-zeroization.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260721-sonar-c-s5798-zeroization |
| Datum (UTC) | 2026-07-21 |
| Basis-Revision | 5c26ffb698a892ffe83b7aa1749a456eae10b956 |
| Tracking | Parent-only SonarQube-Cloud-c:S5798-Keys AZ9MwjLo-bUaKQ_zSGBD, AZ9MwjLo-bUaKQ_zSGBE, AZ9MwjLo-bUaKQ_zSGBK und AZ9cRyrNHhV2CayPTP0O; lokales Finding FND-SONAR-0012 |
| Grenze | Nur Parent Common runtime, geteilter C-Allocator-Helper und Envoy ext_proc bridge. Framework, MRTS und der Parent-Gitlink bleiben unverändert. |

## Motivation und Problemstellung

Die vier nachverfolgten C-Stellen verwendeten ein gewöhnliches
memset(..., 0, sizeof(*object)) unmittelbar vor free. Ein Optimierer kann einen
Store entfernen, dessen Ziel nach free tot ist. Die abgegrenzten Objekte können
einen Remote-Rule-Key, Laufzeitkonfiguration oder begrenzte Request-/
Entscheidungsmetadaten enthalten. Der Befund ist ein glaubwürdiger
Härtungshinweis gegen Speicherremanenz, aber kein Beweis einer End-to-End-
Offenlegung: Es wurde weder eine Heap-Disclosure-Primitive noch Cross-Tenant-
Reuse nachgewiesen.

## Akzeptanzkriterien

- Bestehendes native Cleanup, Objektfreigabereihenfolge, Null-Pointer- und
  Pointer-Nulling-Verhalten erhalten.
- Eine C17-portable, nicht eliminierbare Wipe-Primitive an allen vier
  abgegrenzten Objektfreigabestellen verwenden, ohne Sonar-Suppression,
  Regeländerung oder Quality-Gate-Modifikation.
- Nachweisen, dass die Primitive repräsentative Nichtnull-Bytes vor der
  Freigabe löscht; verfügbare C-Pfade mit GCC und Clang einschließlich -O2
  warnings-clean kompilieren.
- Den gehosteten SonarQube-Cloud-Status des exakten PR-Heads dokumentieren,
  bevor die vier Keys als verified bezeichnet werden; den nicht verfügbaren
  Envoy-Produktbuild nicht als bestanden behaupten.

## Implementierungsentscheidung und Begründung

Eine gemeinsame Funktion msconnector_secure_zero(void *, size_t) schreibt Null
über einen volatile unsigned-char Pointer. Die drei Common-runtime-
Destruktionspfade und Envoy-Bridge-Transaction-Close rufen sie mit
sizeof(*object) unmittelbar vor free auf. Das gewöhnliche
Initialisierungs-memset in runtime_defaults bleibt absichtlich unverändert, weil
es kein Pre-release-Wipe ist.

memset_s wurde nicht gewählt: C17 Annex K ist optional und nicht die portable
Baseline dieses Repositorys. Ein gemeinsamer Helper vermeidet ein Bridge-lokales
Duplikat und gibt der C17-Implementierung einen überprüften Vertrag.

## Security-Auswirkung

Vor Rückgabe der vier abgegrenzten Objektrepräsentationen an den Allocator
behält das neue Verhalten unter optimierten GCC- und Clang-Builds beobachtbare
Zero-Byte-Stores. Es senkt keine Validierungs-, Ressourcen-, Authentifizierungs-,
Isolations- oder Logging-Kontrolle. Es behauptet weder das Löschen
libmodsecurity-eigener Allokationen nach deren Cleanup noch einen
End-to-End-Disclosure-Exploit.

Die Änderung ist innerhalb des Parent-Repositorys Source- und ABI-additiv.
Bestehende Destructor-Reihenfolge und öffentliches Connector-Protokollverhalten
bleiben unverändert.

## Geänderte Dateien

- common/include/msconnector/memory.h
- common/src/memory.c
- common/runtime/msconnector_runtime.c
- connectors/envoy/ext_proc/internal/processor/common_runtime_bridge.c
- ci/checks/common/check-common-memory-safety.sh
- reports/audits/change-records/README.md und README.de.md
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| rtk proxy env BUILD_ROOT=<isolated external task build root> make check-common-memory-safety | Nach der Implementierung bestanden. Der verstärkte Test war vor Existenz des Helpers erwartungsgemäß fehlgeschlagen. |
| rtk proxy env BUILD_ROOT=<isolated external task build root>/gcc CC=gcc make check-common-memory-safety | Mit C17 warnings-as-errors bestanden. |
| rtk proxy env BUILD_ROOT=<isolated external task build root>/clang CC=clang make check-common-memory-safety | Mit C17 warnings-as-errors bestanden. |
| rtk proxy env BUILD_ROOT=<isolated external task build root>/gcc-o2 CC=gcc MSCONNECTOR_CFLAGS=-std=c17 -O2 -Wall -Wextra -Werror make check-common-memory-safety | Bestanden. |
| rtk proxy env BUILD_ROOT=<isolated external task build root>/clang-o2 CC=clang MSCONNECTOR_CFLAGS=-std=c17 -O2 -Wall -Wextra -Werror make check-common-memory-safety | Bestanden. |
| rtk proxy env BUILD_ROOT=<isolated external task build root>/common-helpers CC=gcc make check-common-helpers | Bestanden. |
| rtk proxy env LC_ALL=C gcc and clang -std=c17 -O2 -Wall -Wextra -Werror -S common/src/memory.c | Bestanden; beide Assemblies behalten Zero-Byte-Stores in msconnector_secure_zero. |
| rtk proxy env LC_ALL=C gcc and clang -std=c17 -Wall -Wextra -Werror -fsyntax-only connectors/envoy/ext_proc/internal/processor/common_runtime_bridge.c | Bestanden. |
| rtk proxy env BUILD_ROOT=<isolated external task build root>/envoy sh connectors/envoy/build/build_ext_proc.sh | Blockiert, Exit 77: MODSECURITY_INCLUDE_DIR oder MODSECURITY_PREFIX war nicht bereitgestellt. |
| rtk git diff --check | Nach der finalen Dokumentationsänderung bestanden. |

Die vorgehaltene English/German/JSON-Finding-Evidenz und
Validierungszusammenfassung für FND-SONAR-0012 sind private, hash-adressierte
Task-Artefakte; dieser versionierte Datensatz enthält keine privaten Build-Pfade
oder Credentials.

## Runtime-Evidence

In diesem isolierten Worktree wurde keine vollständige native Connector- oder
Envoy-Runtime ausgeführt. Die vorgehaltene Evidenz ist auf den fokussierten
Allocator/free-Callback-Smoke, Common-helper-Smoke, direkte Bridge-
Syntaxprüfungen und die oben beschriebene compilerbewusste optimierte
Assembly-Prüfung beschränkt.

## Bekannte Einschränkungen

- Der vollständige Envoy-ext-proc-Produktbuild und Runtime-Tests wurden nicht
  ausgeführt, weil im Worktree kein bereitgestelltes libmodsecurity-Development-
  Include-Verzeichnis und keine linkbare Bibliothek vorhanden sind. Der
  versuchte Build stoppte vor der Kompilierung bei seiner expliziten
  Voraussetzung mit Exit 77.
- Es existiert kein End-to-End-Heap-Disclosure-Beweis; daher beschreibt dieser
  Datensatz security hardening, keine validierte Vulnerability.

## Verbleibende Risiken

Gehostete SonarQube-Cloud-Analyse des exakten Heads, GitHub-Checks, Review und
Draft-PR-Delivery stehen bei dieser Source-Revision aus. Das aktuelle Master-
Quality-Gate und die unabhängige Hotspot-Disposition verbleiben unter
FND-SONAR-0001. Die verbleibende Host-Voraussetzung kann eine spätere
vollständige Envoy-Build-Verifikation verhindern, bis eine kompatible
libmodsecurity-Development-Installation bereitgestellt wird.

## Nicht ausgeführte Prüfungen mit Begründung

Der vollständige Envoy-ext-proc-Produktbuild und die Runtime-Suite wurden nicht
ausgeführt, weil die erforderlichen libmodsecurity-Header und die linkbare
Bibliothek in der bereitgestellten Umgebung fehlen. Gehostete SonarQube-Cloud-
und GitHub-Checks können erst nach Push des exakten Draft-PR-Heads existieren.

## Finaler Diff- und Review-Status

Bei dieser Change-Record-Revision ist die Source-Änderung lokal validiert, aber
noch nicht committed, gepusht oder eingereicht. Der Nutzer autorisiert nach
lokaler Verifikation einen Parent-only Draft PR und verbietet ausdrücklich den
Merge. Finaler Branch, Commit, PR-Head, Checks und gehostete SonarQube-Cloud-
Evidenz müssen am exakten ausgelieferten Head beobachtet werden; sie werden hier
nicht abgeleitet.
