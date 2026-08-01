# FND-FRAMEWORK-0056 — Die PCRE2-Archiv-Digest-Regressionsfixture lässt das ModSecurity-v3-Provenance-Manifest aus

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-FRAMEWORK-0056 |
| Kategorie | test_failure |
| Repository / Ownership | framework / framework |
| Priorität / Schweregrad / Konfidenz | P1 / not_applicable / reproduced |
| Status / Machbarkeit | closed / feasible_now |
| Release-Blocker / sicherheitsrelevant | false / true |
| Betroffene Revision | `77d73decd094a8f289fbe0ef2582f12430923e24` |
| Parent/MRTS-Disposition | keine Parent-Gitlink- oder MRTS-Aktion; Framework bleibt unverändert |

## Zusammenfassung, beobachtetes und erwartetes Verhalten sowie Auswirkung

Die fokussierte PCRE2-Archiv-Digest-Fixture erzeugt `MODSECURITY_V3_SOURCE_DIR` nur mit `v3-source/.git`. Der aktuelle Framework-Provenance-Guard verlangt vor dem Apache-PCRE2-Setup zu Recht ein reguläres nicht-symlinked `.gitmodules`-Manifest. Daher prüfen alle vier ungültigen-Digest-Subcases den falschen Blocker, und die Matching-Digest-Legitimkontrolle beendet sich mit `77` vor ihrem PCRE2-tar-Marker.

Die Fixture muss stattdessen den kleinsten gültigen netzwerkfreien ModSecurity-v3-Source-Contract modellieren, den der aktuelle Provenance-Guard erfordert, und danach die Ablehnung ungültiger PCRE2-Digests vor der tar-Extraction sowie die Matching-Digest-Extraction-Kontrolle ausüben. Die Produktions-Provenance-Kontrolle darf weder abgeschwächt noch umgangen oder ausgestubbt werden.

Der reale V3-Guard bleibt fehlgeschlossen, aber dieser fokussierte Security-Regressionstest deckt seine beabsichtigten PCRE2-Archiv-Integritätskontrollen nicht mehr dynamisch ab. Dies ist kein Nachweis eines neuen Source-Provenance-Bypasses und blockiert die unabhängig erforderliche Hosted-Producer-Evidence von Parent PR #74 nicht.

## Betroffene Dateien, Symbole, Voraussetzungen und Reproduktion

Betroffene Framework-Dateien sind `tests/security_regression/test_pcre2_archive_digest.py`, `ci/lib/common.sh` und `ci/provisioning/prepare-apache-build.sh`. Relevante Symbole sind `Pcre2ArchiveDigestTests._run_case`, `ci_require_approved_modsecurity_v3_checkout` und `ensure_modsecurity_v3_source`.

An der aufgezeichneten Framework-Revision liefert die Fixture ein bestehendes V3-Source-Verzeichnis nur mit `.git`; der Apache-Builder ruft den aktuellen V3-Provenance-Guard auf, bevor er den PCRE2-Digest prüft. Reproduktion:

```sh
rtk env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest discover -s tests/security_regression -p test_pcre2_archive_digest.py -v
```

Der Lauf hat Exit-Status `1`: leere, Whitespace-, ungültige und nicht passende Digest-Subcases melden eine unfreigegebene V3-Source, und die Matching-Kontrolle beendet sich mit `77` mit dem fehlenden-`.gitmodules`-Blocker.

## Evidenz und Root Cause

Aufbewahrte Evidenz: `.codex/runs/20260726T084657Z-framework-pcre2-fixture-regression/evidence/framework-pcre2-fixture-failure.md` (SHA-256 `b11ecbb1a4a0f95a8c2427db3033e1a00d72ddc10ab5356dc27720111a657dac`).

`FND-FRAMEWORK-0030` härtete den V3-Topologie-Guard absichtlich so, dass er ein freigegebenes nicht-symlinked `.gitmodules`-Manifest verlangt. Die ältere PCRE2-Fixture repräsentiert eine Source-Root nur durch das Erzeugen von `.git` und erreicht daher den Archiv-Digest-Verifier nicht mehr. Der Produktions-Guard verhält sich wie vorgesehen; der Testfixture-Contract ist veraltet.

## Vorgeschlagene Remediation und Akzeptanzkriterien

In einer separat autorisierten Framework-Aufgabe ausschließlich die PCRE2-Testfixture so aktualisieren, dass sie die kleinste gültige freigegebene V3-Source-Topologie modelliert, die der aktuelle Guard verlangt. `ci_require_approved_modsecurity_v3_checkout` nicht ändern, abschwächen oder ausstuben.

1. Die Fixture enthält ein nicht-symlinked `.gitmodules`-Manifest und erforderliches gemocktes Topologie-/Git-Verhalten.
2. Jeder ungültige PCRE2-Digest beendet sich wieder wegen des Digest-Verifiers mit `77` und beweist, dass das Archiv tar nicht erreicht.
3. Die Matching-Digest-Kontrolle erreicht den lokalen PCRE2-Archiv-Extraction-Marker und vollendet ihren erwarteten Pfad.
4. Fokussierte PCRE2-Archiv-Digest- und V3-Provenance-Regressionen bestehen ohne Produktions-Guard-Regression.

## Validierung, Abhängigkeiten, Blocker und Restrisiko

Vor jeder Framework-Änderung die aktiven Framework-Instruktionen lesen und einen separaten Framework-Delivery-Plan anlegen. Dann `tests/security_regression/test_pcre2_archive_digest.py` und `tests/security_regression/test_modsecurity_v3_git_ref_provenance.py` ausführen, den exakten Framework-PR-Head prüfen und dessen geschützten Framework-Delivery-Lifecycle verwenden, falls der Nutzer einen PR autorisiert.

Abhängigkeiten sind `FND-FRAMEWORK-0030` und `FND-FRAMEWORK-0005`; verwandte Records sind diese beiden Befunde und `FND-PARENT-0053`. Dies ist kein Duplikat von `FND-FRAMEWORK-0030`, der die frühere False-Rejection der realen freigegebenen rekursiven Topologie durch den Produktions-Guard besitzt. Die aktuelle Korrektur ist aus dieser Parent-Aufgabe durch die nötige separate Framework-spezifische Autorisierung und Delivery-Lifecycle blockiert.

Der reale V3-Guard bleibt fehlgeschlossen. Das Restrisiko ist verlorene dynamische PCRE2-Regressionsabdeckung, bis eine separat autorisierte Fixture-Korrektur verifiziert ist; keine Risikoakzeptanz ist dokumentiert.

## Historie

- 2026-07-26 — Drei fokussierte Tests mit fünf Fehlern vor dem beabsichtigten Digest-Verifier reproduziert, weil der synthetischen V3-Source `.gitmodules` fehlt.
- 2026-07-26 — Von `FND-FRAMEWORK-0030` dedupliziert; dies ist ein separater veralteter Fixture-Contract, kein Grund, den Produktions-Topologie-Guard abzuschwächen.
- 2026-07-26 — `remediation_fixed` und `resulting_master_verified_and_closed`: Framework-PR #50 aktualisierte ausschließlich den PCRE2-Fixture-Contract. Exakter Framework-Master `de705a5efb872f95f010346fe2e6143c88876ad4` bestand alle 3 PCRE2-Archiv-Digest- und alle 18 V3-Provenance-Tests; der Produktions-Guard bleibt fehlgeschlossen. Receipt: `.codex/runs/20260726T160903Z-framework-pr50-pr51-master-verification/finding-closure-evidence.md` (SHA-256 `519b89ef349a2d1a66b8cf78a5f0056f2df1909df2f386e5e67b7742bf277a2d`).
