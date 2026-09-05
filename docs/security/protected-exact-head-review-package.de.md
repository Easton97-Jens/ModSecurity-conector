# Review-Paket für geschützten Exact-Head

**Sprache:** [English](protected-exact-head-review-package.md) | Deutsch

Ausschließlich Vorbereitung — keine Merge-Autorisierung.

## Umfang und Disposition

Dieses Paket beschreibt die geschützte Base-Steuerung für den nativen NGINX-
Test `modsecurity_use_error_log`. Es ist eine Review-Hilfe, keine gehostete
Attestierung. Der Candidate-Checkout ist Datenbestand; geschützter Base-
Dispatcher und privilegierter Launcher bilden die TCB der Steuerung.
`independent_review_requested=false` und
`reason=no_authorized_reviewer_available`; eine Reviewer-Freigabe wird nicht
behauptet.

Der externe codex-security-Archiv-Receipt bleibt
`blocked_external_dependency` (FND-PARENT-1036). Der aufbewahrte alte Run und
die synthetischen Fixtures sind nur Fehler-Evidence. Der erste Exact-Read-back
für `c8f1a00a5d45cbc5c4a7e52e1da17e8611e767db` ist historischer
Remediation-Input, keine finale Abnahme: Er fand trotz grünem Gate 20 offene
Code Smells. Sein erster Source-/Test-Successor `0524be2f…` zeigte danach drei
andere offene Issues; der nächste normale Successor wird behoben, nicht
akzeptiert. Gehostete Runtime und Sonar-Ergebnis nach dem Push bleiben
ausstehende Exact-Head-Validierung.

## Bedrohungsmodell und Vertrauensgrenzen

Unvertrauenswürdige Eingaben sind Pull-Request-Metadaten, Candidate-Source und
-Workflow, Candidate-Callback-/JSONL-Records, temporäre Verzeichnisse und
Netzwerkantworten. Die geschützte Base lässt genau eine exakte 40-stellige
lowercase-Git-SHA zu, verwendet feste semantische Orte und übergibt nur
validierte Deskriptoren an die privilegierte Zelle. Ein root-eigener,
nicht beschreibbarer Host-Bootstrap muss Base-Objekt und unveränderlichen
Launcher-Snapshot unabhängig prüfen. Candidate-Angaben sind Beobachtungen,
keine Attestierungen.

## TCB und Übergaben

Zur TCB gehören geschützter Base-Workflow, Dispatcher, Runner-Preflight,
Builder, Root-Launcher, Collector und der administrativ installierte
Host-Bootstrap. Candidate-Modul, Makefile, Callback-/JSONL-Ausgabe und WAF-Text
liegen außerhalb der TCB. Candidate- und privilegierte Zellen verwenden
rollenbezogene private Verzeichnisse; der Runner übergibt feste
`RUNNER_TEMP`- und `GITHUB_WORKSPACE`-Werte und akzeptiert keine beliebigen
Pfad-CLI-Optionen. FD-Ownership ist descriptor-relativ und an privaten Grenzen
no-follow. Der Collector prüft Prozessidentität, Namespace, Artefaktmanifest,
Exit-Status und Ergebnis-Publikation vor einem runner-eigenen Terminalresultat.

Cleanup und Publikation bleiben Gegenstand der Prüfung zu FND-PARENT-1038. Die
aktuelle NGINX-Steuerung hält root-eigene Deskriptoren für Verzeichnis, Zelle,
Scratch, Artefakt, Helper und Evidence, verwendet feste Sandbox-Mount-Ziele,
publiziert Evidence descriptor-relativ und bindet Cleanup vor dem Abschluss an
eine validierte Identität. Ein zufällig gewähltes root-seitiges Scratch-
Container-Leaf verhindert, dass eine veraltete Ressource mit festem Namen für
den aktuellen Run gehalten wird; Cleanup bleibt auf diesen root-eigenen
Container begrenzt. Root-Evidence ist zusätzlich zu `tested_pr_head` an
`tested_pr_base` gebunden. Dies sind laufende repository-eigene Source-
Contracts und ausführbare lokale Tests; sie werden weder als behoben noch als
hosted-validiert behauptet.

## Workflow- und Evidence-Vertrag

Der Workflow vergibt nur die für Checkout und deklarierte Outputs erforderlichen
Berechtigungen; Candidate-Pfade, Secrets und Launcher werden im privilegierten
Job nicht vertraut. Die zwei frischen Zellen laufen mit On-/Off-Einstellung und
müssen korrelierte Transaktionen, getrennte Master-/Worker-Identitäten,
gleichwertige WAF-Beobachtungen und den erwarteten Callback-/JSONL-Unterschied
zeigen. Fehlendes Host-Gate, Exit 77, veralteter Head oder unvollständiges
Schema sind Fehler beziehungsweise externe Blocker, niemals ein Pass.

## Negativtest-Matrix

| Grenze | Erforderliche Negativkontrolle |
| --- | --- |
| SHA/Pfad-Admission | Unicode-Ziffern, Traversal, Symlink, externer Root und veränderliche Candidate-Pfade |
| Artefaktübergabe | Falscher Owner/Modus, Replacement, Symlink, veraltetes Manifest und falscher Digest |
| Prozess-/FD-Lifecycle | Descriptor-Substitution von Verzeichnis/Artefakt, Ersetzung des Sandbox-Ziels, Identitätskonflikt beim Cleanup und unvollständige Publikation |
| Runtime-Evidence | Falsche PID/Namespace, fehlende Korrelation, unerwarteter Exit und unvollständige On/Off-Records |
| Dokumentation/Security | Ungepinnte Action, unsichere Shell, geschwächte Berechtigung und fehlende zweisprachige Ergänzung |

Die fokussierten Source-Contract- und Negativkontrolltests sind die ausführbare
Evidence für diese Kontrollen. Sie decken gehaltene FD-Autorität,
Replacement-Races, identitätsgebundenes Cleanup, begrenzte Prozessaufsicht und
descriptor-sichere Evidence-Publikation ab. Sie ersetzen nicht den geschützten Hosted-
Runtime-Nachweis. Die finalen Befehlsresultate müssen nach dem exakten
GitHub-Read-back des finalen Heads erneut erhoben werden.

## Historisches Sonar-Inventar

Der Baseline-Stand am früheren PR-Head enthielt 80 offene Issues: 15
Vulnerabilities und 65 Code Smells; das Quality Gate war ERROR mit drei neuen
Security-Issues. Die historische Issue-Key-Matrix ist unten aufgeführt. Jeder
Eintrag war ein Ziel für Code-/Test-Reparatur, keine administrative Disposition;
alle Einträge erfordern eine frische Exact-Head-Neuanalyse.

| Regel / Ort | Historische Issue-Keys |
| --- | --- |
| S1066 Root | `AaBsRF5SmWRUlaV2f7fb` |
| S1192 Collector | `AaBs7c_xmWRUlaV2mVXl`, `AaBs7c_xmWRUlaV2mVXk` |
| S1192 Root | `AaBs7c4JmWRUlaV2mVXc`, `AaBsRF5SmWRUlaV2f7fa`, `AaBsRF5SmWRUlaV2f7fU`, `AaBsRF5SmWRUlaV2f7fV`, `AaBsRF5SmWRUlaV2f7fZ`, `AaBsRF5SmWRUlaV2f7fS`, `AaBsRF5SmWRUlaV2f7fW`, `AaBsRF5SmWRUlaV2f7fX`, `AaBsRF5SmWRUlaV2f7fT` |
| S2612 Collector | `AaBsRF5-mWRUlaV2f7gb` |
| S2737 Root | `AaBsRF5SmWRUlaV2f7fk` |
| S3776 Collector | `AaBsRF5-mWRUlaV2f7ga` |
| S3776 Root | `AaBs7c4JmWRUlaV2mVXd`, `AaBsRF5SmWRUlaV2f7fl`, `AaBsRF5SmWRUlaV2f7fm`, `AaBsRF5SmWRUlaV2f7fp`, `AaBsRF5SmWRUlaV2f7fq`, `AaBsRF5SmWRUlaV2f7fr`, `AaBsRF5SmWRUlaV2f7ft`, `AaBsRF5SmWRUlaV2f7fu`, `AaBsRF5SmWRUlaV2f7f1` |
| S5713 Dispatcher | `AaBsRF5pmWRUlaV2f7gF`, `AaBsRF5pmWRUlaV2f7gG`, `AaBsRF5pmWRUlaV2f7gH` |
| S5754 Root | `AaBsRF5SmWRUlaV2f7fn`, `AaBsRF5SmWRUlaV2f7fo`, `AaBsRF5SmWRUlaV2f7fv`, `AaBsRF5SmWRUlaV2f7fw`, `AaBsRF5SmWRUlaV2f7fx`, `AaBsRF5SmWRUlaV2f7fy`, `AaBsRF5SmWRUlaV2f7fz`, `AaBsRF5SmWRUlaV2f7f0`, `AaBsRF5SmWRUlaV2f7f2`, `AaBsRF5SmWRUlaV2f7f5`, `AaBsRF5SmWRUlaV2f7f6`, `AaBsRF5SmWRUlaV2f7f7`, `AaBsRF5SmWRUlaV2f7f8`, `AaBsRF5SmWRUlaV2f7f9`, `AaBsRF5SmWRUlaV2f7f-` |
| S5778 Builder-Test | `AaBt2WmkRykRCVXHzVty`, `AaBs7dARmWRUlaV2mVXm`, `AaBs7dARmWRUlaV2mVXn`, `AaBsRF6ImWRUlaV2f7gj` |
| S5778 Root-Test | `AaBsRF65mWRUlaV2f7gu` |
| S5778 Dispatcher-Test | `AaBsRF6pmWRUlaV2f7gp`, `AaBsRF6pmWRUlaV2f7gq`, `AaBsRF6pmWRUlaV2f7gr`, `AaBsRF6pmWRUlaV2f7gs` |
| S6353 Collector | `AaBsRF5-mWRUlaV2f7gX`, `AaBsRF5-mWRUlaV2f7gY`, `AaBsRF5-mWRUlaV2f7gZ` |
| S6353 Root | `AaBsRF5SmWRUlaV2f7fc`, `AaBsRF5SmWRUlaV2f7fd`, `AaBsRF5SmWRUlaV2f7fe`, `AaBsRF5SmWRUlaV2f7ff`, `AaBsRF5SmWRUlaV2f7fg`, `AaBsRF5SmWRUlaV2f7fh`, `AaBsRF5SmWRUlaV2f7fi`, `AaBsRF5SmWRUlaV2f7fj`, `AaBsRF5SmWRUlaV2f7fs` |
| S9073 Root-Test | `AaBsRF65mWRUlaV2f7gt` |
| S9073 Builder-Test | `AaBsRF6ImWRUlaV2f7gi` |
| S9073 Dispatcher-Test | `AaBsRF6pmWRUlaV2f7go` |
| S8705 Builder/Runner | `AaBsRF51mWRUlaV2f7gR`, `AaBsRF5dmWRUlaV2f7gD` |
| S8707 Dispatcher | `AaBs7c_AmWRUlaV2mVXf`, `AaBs7c_AmWRUlaV2mVXg`, `AaBs7c_AmWRUlaV2mVXj`, `AaBs7c_AmWRUlaV2mVXi`, `AaBs7c_AmWRUlaV2mVXh`, `AaBs7c_AmWRUlaV2mVXe` |
| S8707 Collector | `AaBsRF5-mWRUlaV2f7gd`, `AaBsRF5-mWRUlaV2f7gf`, `AaBsRF5-mWRUlaV2f7ge`, `AaBsRF5-mWRUlaV2f7gc`, `AaBsRF5-mWRUlaV2f7gg` |
| S8707 Runner | `AaBsRF5dmWRUlaV2f7gE` |

Diese historische Baseline ist kein Nachweis für den finalen Head; Issues werden nicht über `NOSONAR`, Exclusions oder ein abgeschwächtes
Gate verworfen.

## Aktuelles Exact-Head-Sonar-Feedback — `c8f1a00a5d45cbc5c4a7e52e1da17e8611e767db`

SonarCloud analysierte diesen exakten PR-Head um `2026-09-05T08:25:15Z`. Das
Quality Gate war `OK`, die New-Code-Ratings für Reliability, Security und
Maintainability waren `A`, und Bugs, Vulnerabilities sowie Hotspots waren null.
Dieses Gate gilt nicht als Abschluss: Die API lieferte weiterhin 20 `OPEN`
Code Smells und null `CONFIRMED` Issues. Die folgende vollständige Matrix
bindet jeden Key an eine reale Source-/Test-Änderung dieses Successors; weder
Suppression noch Akzeptanz, Exclusion oder Quality-Gate-Änderung werden
verwendet. Erst die Analyse nach dem Push kann die Behebung der Keys beweisen.

| Aktuelle Key-Gruppe | Reale Remediation und Regression-Evidence |
| --- | --- |
| Collector `AaBwrYPNwqJS101QKLQy` (`S5713`) | Die redundante `FileNotFoundError`-Subklasse wird aus dem atomaren Result-Cleanup entfernt; die Collector-Regression-Suite deckt atomare Publikation ab. |
| Launcher `AaBwrYH-wqJS101QKLQk`, `AaBwrYH-wqJS101QKLQm`, `AaBwrYH-wqJS101QKLQn`, `AaBwrYH-wqJS101QKLQo`, `AaBwrYH-wqJS101QKLQl`, `AaBwrYH-wqJS101QKLQq`, `AaBwrYH-wqJS101QKLQr`, `AaBwrYH-wqJS101QKLQs`, `AaBwrYH-wqJS101QKLQi`, `AaBwrYH-wqJS101QKLQj`, `AaBwrYH-wqJS101QKLQt`, `AaBwrYH-wqJS101QKLQu`, `AaBwrYH-wqJS101QKLQv`, `AaBs7c4JmWRUlaV2mVXd`, `AaBwrYH-wqJS101QKLQw`, `AaBwrYH-wqJS101QKLQp`, `AaBsRF5SmWRUlaV2f7fu` (`S1192`, `S3776`, `S5713`, `S1481`, `S1172`, `S2589`) | Descriptor-Admission, atomare Control-/Evidence-Publikation, Lexer, Evidence-Parsing und Cleanup-Phasen werden extrahiert; feste Literale werden zentralisiert; No-follow, Pre-/Post-Identity, fsync, PIDFD und Quieszenz bleiben erhalten. Launcher-Regressionen decken Retained-FD-, Symlink-, Cleanup-, JSONL- und Callback-Grenzen ab. |
| Dispatcher `AaBwrYOpwqJS101QKLQx` (`S1192`) | Das feste Dispatcher-Manifest-Leaf wird zentralisiert; die Dispatcher-Regression-Suite deckt das feste Location-Mapping ab. |
| Launcher-Test `AaBwrYQAwqJS101QKLQz` (`S5778`) | UID/GID-Testwerte werden vor der Exception-Assertion gebunden, sodass genau eine Operation getestet wird; die fokussierte Launcher-Suite erhält die Duplicate-Child-Negativkontrolle. |

## Exact-Head-Successor-Feedback — `0524be2f95a9281a948e8f94e3c1c31690775662`

SonarCloud analysierte diesen exakten Successor um `2026-09-05T09:12:16Z`.
Das Quality Gate war `ERROR`: Reliability und Maintainability blieben `A`,
Security war jedoch `C` (`new_security_rating=3`). Die API lieferte zwei
`OPEN` Vulnerabilities und einen `OPEN` Code Smell, aber null `CONFIRMED`,
`ACCEPTED` und Hotspot-Issues. Dies ist ein echter repository-eigener
Remediation-Checkpoint, keine False-Positive- oder Scanner-Ausnahme.

| Exakte Key(s) | Root Cause | Sicherer Successor-Remedy und Regression-Evidence |
| --- | --- | --- |
| `AaBw2LTiwSzpTW4LCOTU`, `AaBw2LTiwSzpTW4LCOTT` (`S8707`) | Der Root-Launcher ließ ein CLI-abgeleitetes Evidence-Leaf nur mit Separator-Prüfungen vor descriptor-relativem `mkdir`/`open` zu. Sein Fallback konnte außerdem einen Parent-Pfad erneut öffnen. | Ein ASCII-allowlistiertes Einzel-Leaf direkt vor der Erstellung verlangen und einen bereits admittierten Parent-FD verpflichtend machen. Neue Negativkontrollen verwerfen Traversal, Control-Zeichen, Unicode und überlange Leafs vor der Erstellung und beweisen, dass ein ersetzter Parent-Pfad die Retained-FD-Operation nicht umleiten kann. |
| `AaBw2LTiwSzpTW4LCOTS` (`S3776`) | Retained-FD-Parsing, Descriptor-Walk, Flag-Auswahl, finale Typ-Prüfung und Cleanup waren in einem Helper kombiniert. | Parsing, Flag-Auswahl, Descriptor-Walk und finale Metadata-Validierung trennen; `O_NOFOLLOW`, Descriptor-Transfer und Fail-closed-Fehler bleiben erhalten. Die bestehenden Retained-FD-Regular-/Directory-/Traversal-Kontrollen und die vollständige Launcher-Suite decken die Grenze ab. |

Kein `NOSONAR`, keine Exclusion, keine Issue-Akzeptanz, Regel- oder
Quality-Gate-Änderung wird verwendet. Erst die Analyse des nächsten Exact Head
kann zeigen, dass alle 23 beobachteten Successor-Keys nicht mehr vorhanden sind.

## Matrix zur Behebung historischer Issues

Die obigen Key-Gruppen bleiben für die Traceability einzeln erhalten. Diese
Matrix dokumentiert für jede Gruppe die reale Source-/Regression-Richtung;
erst die PR-Analyse nach dem Push kann die endgültige Behebung feststellen.

| Historische Key-Gruppe | Source zu Sink / Root Cause | Sichere Source-Behebung | Regression-Evidence |
| --- | --- | --- | --- |
| Dispatcher `S8707`, `S5713` | Runner-eigene Location-/Environment-Strings erreichten Manifest- und Output-Dateioperationen. | Feste semantische Location-Mappings, descriptor-relative No-follow-Admission, begrenztes Parsing und enge Fehlerbehandlung. | Dispatcher-Kontrollen für Location, Traversal, Symlink, Unicode-Ziffer und PR-Identität. |
| Collector `S8707`, `S2612`, `S1192`, `S3776`, `S6353` | Runner-Task-Pfade und veränderliche Handoff-Metadaten erreichten Evidence-/Result-Sammlung. | Getrennte Task-/Input-/Evidence-Admission, gehaltene Deskriptoren, Fixed-Leaf-atomare Publikation und Root-Evidence-Bindung für Head-/Base-Identität. | Collector-Kontrollen für Replacement, Evidence-Substitution, vorgesäte Temporärdatei und Dispatcher-Base-Replacement. |
| Builder `S8705`, `S5778`, `S9073` | Candidate-Build-Werte und Cleanup-Pfade kreuzten die unprivilegierte Build-/Package-Grenze. | Fester Make-Vektor ohne Shell, gesäuberte Environment, descriptor-gebundene Artefakt-Paketierung und explizite Testassertions. | Builder-Kontrollen für Source/Archiv, Output-Replacement, Artefakt-Link und Environment. |
| Runner-Preflight `S8705`, `S8707` | Runner-Environment und Base-Checkout-Pfade erreichten Rollenvorbereitung und Git-Prüfung. | Rollenbezogene feste private Roots, Environment-Allowlist, No-follow-Descriptor-Prüfungen und Base-Checkout-Validierung. | Preflight-Kontrollen für Host-Control, Task-Root, Environment und descriptor-gebundenes Git. |
| Root-Launcher `S1066`, `S1192`, `S2737`, `S3776`, `S5754`, `S6353` | Candidate-Artefakte, Runtime-Pfade, numerische PIDs und Cleanup-Namen näherten sich privilegierten Sandbox-/Prozess-/Filesystem-Sinks. | Gehaltene vertrauenswürdige Deskriptoren, feste Sandbox-Pfade, PIDFD-gebundene Prozess-Ownership, identitätsgebundenes Cleanup und root-eigene begrenzte Evidence. | Launcher-Kontrollen für Artefakt-/FD-Replacement, PIDFD, Sandbox-Pfad, Timeout, Identität und Cleanup-Race. |
| Nur Test `S5778`, `S9073` | Breite Inline-Exception-Assertions verschleierten die getestete Fehlergrenze. | Benannte minimale fehlschlagende Operationen und direkte Exception-Assertions erhalten die Negativkontrolle. | Die oben genannten fokussierten Builder-, Dispatcher- und Launcher-Suiten. |

## Evidence-Checkliste

- [x] finaler lokaler Source-/Test-/Dokumentations-Diff geprüft und Checks bestanden;
- [x] normaler Base-Merge `acc0ca1d22fd8a452453e66f51115ce026517b52` ohne Rebase oder Force-Push erfolgt;
- [x] der Exact-Head-Read-back von `c8f1…` hat alle 20 verbleibenden Sonar-Issues einzeln offengelegt und zugeordnet;
- [ ] normaler Remediation-Successor gepusht, aus GitHub zurückgelesen und exakt abgeglichen;
- [ ] alle relevanten Checks und der vollständige Exact-Head-Runtime-Workflow erneut ausgeführt;
- [ ] Sonar-Issues einzeln triagiert, null neue Issues;
- [ ] externer Archivstatus bleibt `blocked_external_dependency`, bis der
      autoritative Plugin-Vertrag repariert ist.

Ausschließlich Vorbereitung — keine Merge-Autorisierung.
