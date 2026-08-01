# FND-PARENT-0069 — Apache mod_security3.c hat eine baseline-identische GCC-C17-Werror-Fehlergruppe

## Identität

- Kategorie: compiler_hardening_gap
- Repository / Ownership: parent / parent
- Priorität / Schweregrad / Konfidenz: P2 / not_applicable / reproduced
- Status / Machbarkeit: validated / feasible_now
- Release-Blocker / Candidate-Integration-Blocker / Sicherheitsrelevanz: false / false / true
- Scope: Master- und selektiver-#94A-Task-Kandidaten-Baselinevergleich

## Zusammenfassung

Der verpflichtende GCC-C17-Check mit -std=c17 -Wall -Wextra -Werror endet für
connectors/apache/src/mod_security3.c sowohl im zurückgehaltenen Master- als
auch im selektiven #94A-Kandidatenlauf mit Exit 1. Der Source ist bei SHA-256
8b21b64c95a1f1cb98ac05437e60e5d5ab8124e363cd2784b7c800e65449f8d7
byte-identisch, und die beiden 114-zeiligen stderr-Logs normalisieren zu
SHA-256 34b8bbdfcda5e8420a33ac99eaf57a1283388ec7f87d104b1ee36093744eacc6.

Dies ist eine validierte bereits bestehende Compiler-Hardening-Luecke, keine
durch selektives #94A verursachte Regression. Sie ist deshalb weder ein
Release-Blocker noch ein Candidate-Integration-Blocker für diesen Kandidaten.
Es wird kein Fix-, PR-, Merge-, Master-, Verified-, Closed- oder
Delivery-Claim erhoben.

## Beobachtetes Verhalten und Grenze

Der Header-Probe besteht, aber die getrennte Modul-Translation-Unit-Kompilierung
fehlschlägt in beiden zurückgehaltenen Verzeichnissen. Die Diagnosegruppe
enthält unbenutzte Parameter und Variablen, Pointer-Signedness an der
libModSecurity-Request-Header-API, einen fehlenden Apache-Module-Flags-
Initializer, statische msc_config.h-Deklarationen ohne Definition in dieser
Translation-Unit sowie einen Non-void-Cleanup-Pfad, der sein Ende erreicht.
Die Raw-Logs unterscheiden sich nur in absoluten Source- und Build-Präfixen;
der aufgezeichnete normalisierte Digest beweist dieselbe 114-zeilige Gruppe.

Dies ist eine Compiler-Hardening- und Assurance-Grenze, keine belegte
attacker-kontrollierte Runtime-Grenze. Sie darf nicht durch Warnunterdrückung,
-Wno-error, Entfernen aus der Source-Liste oder eine Scanner-/Gate-Ausnahme
aufgelöst werden.

## Evidence

| Artefakt | SHA-256 | Ergebnis |
| --- | --- | --- |
| Master-GCC-C17-stderr | 1d40b8f49f4d38f09f8cfce6266f59fc963cd64d2268dbefe3ce5e66f19f6cde | Zurückgehaltenes 114-zeiliges Log; aufgezeichneter Compiler-Exit 1. |
| Kandidaten-GCC-C17-stderr | 634475cf310eb274e3825549cdeed62bb58d865a3a2dd97444da7b354885196e | Zurückgehaltenes 114-zeiliges Log; aufgezeichneter Compiler-Exit 1. |
| Master- und Kandidaten-mod_security3.c | 8b21b64c95a1f1cb98ac05437e60e5d5ab8124e363cd2784b7c800e65449f8d7 | Byte-identischer Source, daher führte der Kandidat die Gruppe nicht ein. |
| Normalisierter zurückgehaltener stderr-Vergleich | 34b8bbdfcda5e8420a33ac99eaf57a1283388ec7f87d104b1ee36093744eacc6 | Parent-gelieferte Normalisierung nach Entfernung nur umgebungsspezifischer absoluter Pfadpräfixe. |

Die zurückgehaltenen Raw-Logs sind:

- /var/tmp/codex/ModSecurity-conector/runs/selective-apache-prs-master-20260729/validation/apache-c17-baseline-master/connectors_apache_src_mod_security3_c.c17.o.err
- /var/tmp/codex/ModSecurity-conector/runs/selective-apache-prs-master-20260729/validation/apache-c17-baseline-candidate/connectors_apache_src_mod_security3_c.c17.o.err

## Remediation-Richtung und Controls

Eine getrennte Parent-Source-Remediation verwenden. Jede Diagnose vor der
Korrektur klassifizieren: absichtlich unbenutzte Callback-Inputs, wirklich tote
Variablen, Header-Linkage, Cleanup-Return-Status, Apache-Module-ABI-
Initialisierung und semantisch geprüfte Unsigned-Byte-API-Konvertierung. Die
erforderlichen C17-Flags und das Source-Contract-Wiring bewahren.

Die Akzeptanz verlangt, dass der bestehende GCC-C17-Check ohne
Warnunterdrückung mit Exit 0 endet, fokussierte Apache/APXS/APR-Legitimate-
Controls für betroffene Semantik bestehen und ein frischer Source-/Log-
Vergleich vorliegt. Genehmigte Clang-C17-Controls als ergänzenden Check
ausführen, sobald verfügbar. Der selektive #94A-Kandidat wird weiterhin nur
gegen relevante change-introduced Findings bewertet.

## Deduplizierung und Restrisiko

Dies ist nicht FND-PARENT-0008: Dieser Record ist eine historische Clang-
Missing-Field-Initializer-Beobachtung in apache2/msc_config.c. Dies ist nicht
FND-PARENT-0043: Dieser Record besitzt Intervention-Buffer-Lifecycle und
Ownership-Sicherheit in mod_security3.c. Gemeinsames C17-Wiring oder ein
gemeinsamer Apache-Bereich sind keine gemeinsame Grundursache oder
Remediation-Grenze.

Die ungelöste Gruppe verhindert einen sauberen GCC-C17-Assurance-Claim für
diese Translation-Unit, etabliert aber keinen Remote- oder lokalen
attacker-kontrollierten Runtime-Exploit. Sie bleibt validated und feasible_now;
dieser lokale Finding-Task hat keine Source geändert.

## Historie

- 2026-07-29T10:13:10Z: Master- und selektive-Kandidaten-GCC-C17-Logs wurden
  als eine baseline-identische Compiler-Hardening-Gruppe unter einer neuen
  kanonischen ID erfasst.
