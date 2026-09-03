# Change Record

**Sprache:** [English](CR-20260825-trusted-lighttpd-runtime-supervisor-infrastructure.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260825-trusted-lighttpd-runtime-supervisor-infrastructure |
| Datum (UTC) | 2026-08-25 |
| Basis-Revision | `5d71be74369123257851eb5ec612d7523a6b061d` |
| Delivery-Status | Ein separater Parent-Draft-PR ist autorisiert. Dieser Record autorisiert weder Merge, Auto-Merge, direkten Default-Branch-Push, Framework-/MRTS-Änderung noch Gitlink-Update. |

## Motivation und Problemstellung

Der geschützte Lighttpd-Namespace-Dispatcher beweist derzeit nur seine
eingeschränkte Namespace-Fixture. Dieses Ergebnis darf nicht als Host-Runtime-
Evidence dargestellt werden; PR-beschreibbare Pläne, Ergebnisse, Events oder
Zusammenfassungen können keine reale Lighttpd-Runtime belegen. Es fehlt ein
von geschütztem `master` kontrollierter Supervisor, der die Runtime selbst
erzeugt und beobachtet.

## Akzeptanzkriterien

- Ein Standardbibliotheks-Supervisor akzeptiert ausschließlich einen
  geschlossenen, versiegelten Artefaktplan und bricht fail-closed vor einem
  Subprozessstart ab, wenn Identität, Pfad, Ownership, Digest, No-CRS- oder
  Privilegieninvariante fehlt.
- Der Supervisor startet die exakte versiegelte Lighttpd-Binary unter einer
  Non-root-Identität, beobachtet Executable, Connector-Modul und Loopback-
  Socket unabhängig, sendet feste Kontroll-/Detection-/Negativprobes und
  schreibt einen privaten Receipt.
- Die Dispatcher-Zusammenfassung ist nur an den geschützten Fixture-Step
  gebunden und erklärt ausdrücklich, dass weder Supervisor noch Runtime-
  Evidence ausgeführt wurden.
- Statische Mutationen verhindern, dass Zusammenfassung oder Status die
  Fixture als Lighttpd-Runtime-Ergebnis bezeichnen.
- Es sind keine Änderungen an NGINX, Framework, MRTS, Gitlink, Dependency,
  Lockfile, Toolchain oder PR #335 enthalten.

## Implementierungsentscheidung und Begründung

`trusted_lighttpd_runtime_supervisor.py` ist absichtlich ein Protected-
Runtime-Primitiv und kein PR-Workflow-Step. Es prüft ein vollständiges Digest-
Manifest für jede reguläre Datei im root-eigenen versiegelten Baum, weist
Zusatzdateien, Symlinks, veränderliche Ownership, Hardlinks, Linux-File-
Capabilities und Set-ID-Bits ab und verlangt einen getrennten privaten Receipt-
Root. Die generierte Konfiguration wird über denselben No-follow-Descriptor
gelesen, der auch für den Digest verwendet wird; CRS-Referenzen und Includes
werden abgewiesen. Jede `rules_file`- und `event_path`-Direktive wird
abgewiesen, bis ein separater kanonischer geschützter Rule-/Data-
Provenance-Vertrag existiert. Dieser statische Check wird getrennt von der
Runtime-Provenance ausgewiesen; der Supervisor blockiert, bevor er Lighttpd
starten oder einen `PASS`-Receipt ausgeben kann. Die Child-Umgebung setzt
`MSCONNECTOR_CRS_RUNTIME=0` sowie `MODSECURITY_RULESET=no-crs`.

Der später aktivierte Startpfad hat einen festen Argumentvektor und eine neue
Prozessgruppe. Er darf ausschließlich als PID 1 in seinem privaten PID-
Namespace starten, bindet die Child-PID an ein Startzeit-Token, prüft `/proc`
vor und nach den Probes auf versiegeltes Executable und gemapptes Modul,
verlangt genau einen dem Child gehörenden `127.0.0.1`-Listener, führt drei
feste `OPTIONS *`-Probes aus, fordert frische Host-Transaktions-IDs und prüft
beim Cleanup, dass kein Child im privaten Namespace verbleibt. Bis das
unabhängige Provenance-Gate existiert, stoppt die Ausführung vor diesem Pfad.
Ein Receipt wird genau einmal über einen root-eigenen Directory-Descriptor mit
atomarer Hardlink-Publikation geschrieben; die nicht verfügbare Voraussetzung
erzeugt ausschließlich `BLOCKED`, weist Runtime-No-CRS-Provenance als
`NOT_VERIFIED` und MRTS als `NOT_INVOKED` aus.

Der vorhandene geschützte Dispatcher bleibt Fixture-only. Seine neue Job-
Zusammenfassung kann den aufgelösten SHA und das Fixture-Ergebnis zeigen, liest
aber niemals PR-Source, erhält kein Write-Token und behauptet keine Runtime-
Evidence. Eine spätere Protected-master-Integration muss den Supervisor im
selben eingeschränkten Namespace aufrufen und die versiegelten Artefakte selbst
erzeugen; dieser Record behauptet diese künftige Runtime-Ausführung nicht.

## Geänderte Dateien

| Datei | Zweck |
| --- | --- |
| `ci/runtime/lifecycle/trusted_lighttpd_runtime_supervisor.py` | Neues geschütztes Runtime-Supervisor-Primitiv. |
| `tests/test_trusted_lighttpd_runtime_supervisor.py` | Fokussierte Verträge für Sealed-Plan, Prozess, Probes, Receipt und Cleanup. |
| `.github/workflows/run-trusted-lighttpd-namespace-dispatch.yml` | Begrenzte Fixture-only-GitHub-Zusammenfassung. |
| `tests/test_trusted_lighttpd_namespace_dispatch_workflow.py` | Fail-closed-Mutationsverträge für Zusammenfassung und Status. |
| Dieses gekoppelte Record-Paar und Archivindizes | Autorisierte zweisprachige Nachvollziehbarkeit. |

## Ausgeführte Befehle

- `rtk proxy python3 -m py_compile ci/runtime/lifecycle/trusted_lighttpd_runtime_supervisor.py` — bestanden.
- `rtk proxy python3 -m unittest -v tests.test_trusted_lighttpd_runtime_supervisor tests.test_trusted_lighttpd_namespace_dispatch_workflow` — bestanden (`16` fokussierte Tests).
- `rtk proxy make check-ci-security-contract` — bestanden.
- `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m pip check` — bestanden.
- Der gepinnte task-lokale `actionlint`-Aufruf für `.github/workflows/run-trusted-lighttpd-namespace-dispatch.yml` — bestanden.
- Der gepinnte task-lokale `zizmor`-Aufruf für `.github/workflows/run-trusted-lighttpd-namespace-dispatch.yml` — bestanden; der Offline-Modus meldete keine Befunde und drei bestehende Suppressions.
- `rtk proxy git diff --check` — bestanden.

## Security-Auswirkung

Der neue Code verengt die spätere Runtime-Trust-Boundary: PR-kontrollierter
Output kann weder Binary, Modul, Config, Port, Probe, Prozess noch Receipt-
Ergebnis auswählen. Er ergänzt keine PR-getriggerte privilegierte Ausführung
und ändert nicht die Least-Privilege-Token-Trennung des Dispatchers. Der
spätere geschützte Aufruf benötigt weiterhin unabhängiges Review, weil er die
versiegelten Artefakte erzeugt und diesen Supervisor als root vor dem Drop der
Lighttpd-Child-Identität ausführt.

## Runtime-Evidence

Es wurde keine Lighttpd-Runtime-Evidence erhoben oder beansprucht. Der aktuelle
Dispatcher führt weiterhin nur die geschützte Namespace-Fixture aus. Die
fokussierten Tests des Supervisors prüfen lokale Kontrolllogik und sind keine
Host-Runtime-Evidence für einen Pull Request.

## Bekannte Einschränkungen

Dieser PR bindet den Supervisor absichtlich nicht an den geschützten
Dispatcher an, erzeugt keinen versiegelten Artefaktsatz, erzeugt noch keinen
späteren kanonischen geschützten Rule-/Data-Provenance-Vertrag, aktiviert den
blockierten Startpfad nicht, dispatcht nicht gegen einen PR-SHA, führt kein
MRTS aus und schließt FND-PARENT-0303 nicht. Der vorhandene
Namespace muss der Ausführungsort bleiben; ein Host-seitiger Prozessbeobachter
kann ein Child in einem separaten PID-Namespace nicht ehrlich beobachten.

## Verbleibende Risiken

Die Protected-master-Integration steht noch aus. Ihre Eingaben müssen
master-eigene Literale oder unabhängig versiegelte Outputs bleiben und die hier
definierten exakten Prozess-, Listener-, Request-, Receipt- und Cleanup-
Beobachtungen beibehalten. Hosted-Exact-Head-Checks, SonarCloud und ein
manueller geschützter Runtime-Lauf stehen nach Öffnen des Draft-PR noch aus.

## Nicht ausgeführte Prüfungen mit Begründung

- Kein geschützter `workflow_dispatch`-Lauf: Der Workflow ist absichtlich an
  geschütztes `master` gebunden und kann von diesem ungemergten Draft-PR nicht
  ausgeführt werden.
- Kein echter Lighttpd-/MRTS-Lauf: Dieser Infrastruktur-PR erzeugt noch keine
  versiegelten Lighttpd-Artefakte und ruft den Supervisor nicht auf.
- Keine gehosteten PR-Checks oder SonarCloud-Analyse: Sie benötigen den späteren
  exakten Draft-PR-Head-SHA.
- `make check-bilingual-docs` ist durch den nicht initialisierten Framework-
  Gitlink in diesem separaten Worktree blockiert; dadurch entstehen bestehende
  fehlende lokale Linkziele unter `modules/ModSecurity-test-Framework/`. Diese
  Aufgabe initialisiert oder verändert dieses Repository nicht.
- Ruff ist in der bestehenden virtuellen Umgebung des Repositorys nicht
  installiert. Es wurde nicht allein für diese Aufgabe ergänzt, weil dies eine
  nicht autorisierte Dependency-/Tool-Änderung wäre.

## Finaler Diff- und Review-Status

Die lokalen Supervisor- und Dispatcher-Verträge bestanden die fokussierten
Tests, den CI-Security-Vertrag, Workflow-Linter und den finalen Whitespace-
Diff-Check. Ein unabhängiges finales Security-Diff-Review bestätigte, dass der
Supervisor vor jedem Runtime-Start blockiert, bis unabhängige Runtime-No-CRS-
Provenance existiert; es wurde kein verbleibender belegter High-/Critical-
Befund gemeldet. Exact-Head-Hosted-Checks, SonarCloud und eine geschützte
Runtime-Ausführung bleiben bis zur Delivery offen.
