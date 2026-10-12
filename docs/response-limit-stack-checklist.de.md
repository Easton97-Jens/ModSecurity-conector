# Stackcheckliste für Request-/Response-Body-Limits

**Sprache:** [English](response-limit-stack-checklist.md) | Deutsch

## Stack und Abnahme

[PR #407](https://github.com/Easton97-Jens/ModSecurity-conector/pull/407) nutzt
`fix/engine-owned-response-limits-stack-20261011`, gestapelt auf #382-Branch
`fix/unified-native-results-events-20260921`. Basisupdates erfordern frische Prüfung;
normale Basis-Merges nach #407 erhalten die Historie. Kein Merge nach #382/master,
Force-Push oder History-Rewrite ist autorisiert. I09/#408 und I11/#406 sind integriert;
I10/#409 und I12/#410 bleiben getrennt.

Ready for review erfordert alle sieben Nutzer-Abnahmekriterien. Ready to merge
erfordert zusätzlich die geltende Integrations-/Sicherheits-/Hostabnahme.
Tatsächlichen Draft-/Head-/Basisstand und Exact-Head-Checks aus GitHub lesen; dieses
Quelldokument zertifiziert weder spätere Commits noch kodiert es veraltete Liefer-SHAs.

## Produktprüfungen

- [x] Common-/Adapter-/Service-Request-/Response-Größenpolicies, Defaults, Parser-/Merge-/Fallback-Gates und Connector-`body_limit_action` entfernen.
- [x] Entfernte Optionen ablehnen; native Direktiven wählen exklusiv Inspection-Limits und Reject/ProcessPartial.
- [x] Explizite richtungsbezogene Engine-Policies in Fixtures erhalten; keine versteckten Fixturedefaults.
- [x] Pointer-/Overflow-/Datei-/Descriptor-/Frame-/Nachrichten-/Header-/Event-/Timeoutprüfungen und begrenzte wiederverwendbare Buffer/private Spools erhalten.
- [x] Authorization-Samples unabhängig von Enginepolicy und vollständigem nativem Streaming klassifizieren; nicht unterstütztes Framing dokumentieren.
- [ ] Vollständige Request-/Response-Hostmatrizen aller aktiven Profile abschließen: unabhängige Host-/Samplegrenzen und I12-Fälle bleiben.

Die [Matrix der zehn Profile](body-inspection-review-matrix.de.md) liefert getrennte
Request-/Response-Pfade, tatsächliche Evidenzschichten, alle vier verbleibenden Limits
und dauerhafte Basis-Follow-ups. Sie erfasst Apache-Native-Reject bei Append/nach
Commit und SPOP-Vollständigkeitsprüfung vor Enginezulassung. Kategorie-4-Grenzen
werden niemals vollständig implementiert genannt.

## Review-Gates und erhaltene Nachweise

Die Matrix erfasst beobachtete Common-Native-, Apache-APR-/C17- und ausgewählte SPOP-/
kombinierte Hostresultate. Die korrigierte SPOP-Fixture besteht die frische 64-Test-Suite;
der frühere Fehler bleibt als überholte Evidenz erhalten.
Historische Quick-, Envoy- und CI-/Sonarerfolge belegen nur die jeweilige geprüfte
Revision; sie verifizieren keine neuen Reparaturen. Keine Scannerausnahmen oder
abgeschwächten Assertions sind erlaubt.

- Finale betroffene Tests/Builds, quick-check, Dokumentation/Generatoren und empfindliche Mutationskontrolle früherer Limits erfordern frische Run-Evidenz vor Ready.
- Finaler unabhängiger redigierter Secretscan erfordert eigenen Nachweis; der Master-only-Secretworkflow belegt diesen gestapelten PR nicht.
- Finale Exact-Head-GitHub-Checks und Sonar erfordern Quality Gate OK, null neue offene/akzeptierte Issues, Hotspots und Duplikation; erwartete Skips benötigen ausdrückliche Provenienz.
- GitHub-Ready-Umstellung und Readback erfordern alle sieben Kriterien; unveränderte Branchnamen und isDraft=false verifizieren.

Diese Regeln sind Abnahmeanforderungen, kein Remote-Statusfeed. Die
[Livechecks](https://github.com/Easton97-Jens/ModSecurity-conector/pull/407/checks)
und der finale Run-Readback bestimmen ihre Bewertung. Sonar ohne gemessene
Coverage ersetzt keine ausführbaren Tests.

## Verbleibende unabhängige Nachweise

Vollständige I12-/V08–V10-Hostabdeckung bleibt für alle zehn Profile not_run,
einschließlich ausgehandelter Protokolle, Ownership-/Commit-Timing und spätem Abort.
Ausgewählte Envoy-HTTP/1- und kombinierte HAProxy-Proben schließen sie nicht ab.
Foreign-UID-/Read-only-Mount-Spoolproben sind durch Root-only-UID-Maps/chown-EINVAL
und Namespace-EPERM blockiert; Compilation oder gecachte Binärdateien ersetzen sie nicht.

FU-COMMON-LOSSY-CONTRACT und FU-STOCK-RST-DELIVERY bleiben unabhängige Basisfehler
mit unveränderten Assertions und exakten Basis-/Aktuellvergleichen in der Matrix.
Vollständige Entfernung jeder aktiven Gesamtbodygrenze wird nicht behauptet:
Envoy ext_authz und Traefik forwardAuth bleiben Host-Vollsample-Routen, SPOP
bleibt eine begrenzte vollständige Nachricht, unabhängige Host-Requestgrößenkontrollen
bleiben. Natives ext_proc, natives Traefik-UDS und HTX sind ihre Streaming-Alternativen.
Der 32768-Byte-Authorization-Response-Schutz bleibt getrennt von Anwendungsresponse-
Inspection. Siehe [Ownership-Vertrag](phase4-mode-budget.de.md) und
[Change Record](../reports/audits/change-records/CR-20261011-response-limit-policy-removal.de.md).
