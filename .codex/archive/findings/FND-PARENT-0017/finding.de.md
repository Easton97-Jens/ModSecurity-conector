# FND-PARENT-0017 — Die Traefik-UDS-Private-Parent-Validierung akzeptierte einen UID-übergreifend ersetzbaren Vorfahren

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-PARENT-0017` |
| Kategorie | `security_hardening` |
| Repository / Ownership | `parent` / `parent` |
| Priorität | `P1` |
| Severity / Confidence | `medium` / `validated` |
| Status / Machbarkeit | `fixed` / `feasible_now` |
| Release-Blocker / Security-Relevanz | `true` / `true` |
| Connector / Protokoll / Profil | Traefik / AF_UNIX pathname / native-traefik-middleware |

## Zusammenfassung

Die früheren UDS-Kontrollen validierten nur den unmittelbaren, dem aktuellen
Benutzer gehörenden Parent mit exakt `0700`. Ein Socket-Parent unter einem
nicht-sticky gruppen- oder weltbeschreibbaren Vorfahren konnte nach der
Validierung und vor `bind()` von einer anderen UID ersetzt werden. Der
Python-Runner, das fokussierte Shell-Harness und C-Listener/Selbsttest
validieren jetzt jeden Vorfahren. Beschreibbare Vorfahren sind nur zulässig,
wenn Sticky-Directory-Semantik einen Kindeintrag der effektiven UID schützt.

## Beobachtetes und erwartetes Verhalten

Vor der Reparatur erzeugte ein task-owned Test einen nicht-sticky Vorfahren mit
Modus `0777` und ein Kind mit Modus `0700`. Sowohl Python-Validator als auch C
`--self-test` akzeptierten das Kind. Ein Live-Exploit mit fremder UID lief nicht,
weil der konfigurierte externe Root privat ist; die Akzeptanzlücke und die
Source-to-Sink-Race-Bedingung waren dennoch konkret.

Jeder ausgewählte Parent muss jetzt absolut, kanonisch, symlinkfrei, dem
aktuellen Benutzer gehörend, exakt `0700` und durch die vollständige
Vorfahrenkette gegen UID-übergreifende Ersetzung geschützt sein. Ein gruppen-
oder weltbeschreibbarer Vorfahr muss sticky sein und sein direktes Kind muss der
effektiven UID gehören. Ungültige Topologien scheitern vor UDS-Allokation oder
`bind()`.

## Auswirkung

Bei der früheren Kontrolle konnte ein operator-ausgewählter Parent unter einem
nicht-sticky, UID-übergreifend beschreibbaren Vorfahren im Intervall zwischen
Validierung und Bind umbenannt/ersetzt werden. Der Dienst konnte unter einem
angreiferkontrollierten Verzeichnis binden und damit die beabsichtigte
UID-übergreifende UDS-Grenze schwächen. Diese Reparatur löst nicht die separat
verfolgten Same-UID-Endpoint-Redial- oder Cleanup-Races.

## Betroffene Dateien und Symbole

- `connectors/traefik/scripts/runtime_native_smoke.py` —
  `assert_private_engine_socket_parent_ancestors_are_safe`,
  `directory_entry_is_protected_from_cross_user_replacement`.
- `connectors/traefik/build/test-engine-service-runtime.sh` — äquivalenter
  Shell-Preflight.
- `connectors/traefik/src/traefik_engine_service.c` —
  `traefik_engine_private_directory_ancestors_are_safe`,
  `traefik_engine_parent_protects_child_from_cross_uid_replacement`.
- `tests/test_traefik_native_local_plugin.py` — Vorfahren-Prädikat-Regression.

## Voraussetzungen und Reproduktion

1. Ein Operator wählt einen dem aktuellen Benutzer gehörenden Parent mit exakt
   `0700` unter einem nicht-sticky gruppen- oder weltbeschreibbaren Vorfahren.
2. Eine andere lokale UID kann diesen Vorfahren traversieren/beschreiben und
   raced nach der Validierung, aber vor `bind()`.
3. Im alten Code akzeptierten Python-Auswahl und C-Selbsttest diese Topologie.

Die task-owned Pre-Fix-Kontrolle liegt in
`logs/119-private-parent-mutable-ancestor-control-gap-pre-fix-final.log`,
SHA-256 `25a6728bca11448352bd922384e22749570e7d453e393f6dd1092cec1abfeee7`.
Sie protokolliert Python-Akzeptanz und C-Engine-Exit `0`; ihr privater äußerer
Root macht sie zu einer Control-Gap-Reproduktion statt zu einem Live-Exploit mit
fremder UID.

## Remediation und Validierung

Die schmale Reparatur erhält die bestehenden Kontrollen für unmittelbaren
Parent, keine Symlinks, keinen öffentlichen Default, Pfadlänge und Same-UID-
Restrisiken. Sie ergänzt dieselbe Vorfahren-Ersetzbarkeitsprüfung in Python,
Shell und C:

- Kein Gruppen-/Other-Write auf einem Vorfahren wird akzeptiert.
- Ein beschreibbarer Vorfahr ist nur zulässig, wenn er sticky ist und sein Kind
  der effektiven UID gehört.
- Ein nicht-sticky veränderbarer Vorfahr wird von Python, Shell (Exit `77`) und
  C-Selbsttest (Exit `1`) abgelehnt.

Die Post-Fix-Negativkontrollen bestanden in
`logs/123-private-parent-ancestor-negative-controls-final.log`, SHA-256
`0cc657a4a58763b44070215e7c354027c12688a1eb248e21cb9a76c9c4a2868c`.
Legitimes Allow/Blocking-Runtime-Verhalten bestand in `logs/125-*`, SHA-256
`c35d629326601b521feeb92953f7f43526cad2bc5b9d7e6c7316d22e85c0cb36`.

Normale C17-Builds/Selbsttests bestanden mit Clang (`logs/121`, SHA-256
`6d044ad0eb36b861fefe8e1d36b28ae6a59d91b48da5c14aca3b73e416612d80`) und
GCC (`logs/122`, SHA-256
`8c6ff06096212dde3a1f272f00b9ed7492c33bef35cfc820f0df074910605156`). Ein
separater externer Hardened-Diagnostic-Build bestand (`logs/126`, SHA-256
`aef7a84d16c3d394bb3adf8d87b608193a1758f655a3d8382adf8eb352f29808`), ebenso
eine kombinierte ASan+UBSan-Runtime mit aktivierter Leak-Erkennung (`logs/128`,
SHA-256 `f2663195a519ad478d1001b44c9fea7584f92c88c1019f8da6520baa54f3587c`)
und GCC `-fanalyzer` (`logs/129`, SHA-256
`dd139757add71aae0683b12d0f6c9c60c1729f2d35db16c9c35e1008ca2d674a`).

## Restrisiko und Historie

`FND-PARENT-0013` und `FND-PARENT-0015` bleiben für Same-UID-Pathname-Cleanup
und Endpoint-Identity nach Bereitschaft offen. Es wird kein Risiko akzeptiert.
Dieses Finding ist lokal fixed; exakte Head-SonarCloud-Verifikation bleibt eine
Delivery-Abhängigkeit von `FND-PARENT-0016`.

- `2026-07-17T16:17:28Z`: Immediate-Parent-only-Akzeptanz reproduziert.
- `2026-07-17T16:56:51Z`: Reparatur und fokussierte Python-/C-/Shell-/Runtime-/
  Hardened-/Sanitizer-/Analyzer-Kontrollen bestanden.
