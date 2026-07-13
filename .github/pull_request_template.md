## English

### Note
English is the technical primary language. Complete this section and the German
section with equivalent facts; German is not a shortened summary.

Use the [change traceability policy](../docs/change-traceability.md) and the
[Change Record index](../reports/audits/change-records/README.md) for every
non-trivial change.

### Summary
Describe the change briefly.

### Type of change
Please select all that apply:

- [ ] Bug fix
- [ ] Feature
- [ ] Documentation
- [ ] Refactoring
- [ ] Security / hardening
- [ ] CI / build

### Change Record

Change ID or Change Record link: <!-- CR-YYYYMMDD-short-slug or explain why a record is not required -->

### Motivation and context
Why is this change needed?

### Acceptance criteria

- [ ] <Observable criterion>
- [ ] <Observable criterion>

### Detailed changes
List the key changes made in this pull request.

### Tests and command results

List every command that actually ran. Do not paste complete logs or sensitive
raw data.

| Exact command | Exit code or result | Short sanitized summary | Canonical evidence path | Run ID |
| --- | --- | --- | --- | --- |
| <!-- command --> | <!-- result --> | <!-- summary --> | <!-- path or None --> | <!-- run ID or None --> |

### Runtime evidence

State the run ID, profile/scope, canonical sanitized evidence location, and
bounded observation. If none exists, state: “No runtime evidence was collected
or claimed.” Builds, configuration checks, lint, unit tests, and smoke results
are not runtime evidence by themselves.

### Security impact
Describe any security impact, including whether this change alters defaults, validation, logging, or threat exposure.

### Documentation status

List updated documentation and examples, including required language
companions, or state “No documentation update needed” with a reason.

### Known limitations

List known limitations and remaining risks, or state “None”.

### Checks not run

List each relevant check that was not run and why. Do not describe a planned or
assumed test as passed.

### Breaking changes
List any breaking changes. If none, state "None".

### Checklist

- [ ] I reviewed my own changes.
- [ ] I recorded exact commands and actual results, or explained checks not run.
- [ ] I updated documentation where needed.
- [ ] The Change Record, if required, matches the actual final diff and real test results.
- [ ] I did not add secrets, complete environment variables, cookies, tokens, bodies, private keys, caches, or sensitive raw data.
- [ ] I documented breaking changes if applicable.

---

## Deutsch

### Hinweis
Englisch ist die technische Primärsprache. Diesen und den deutschen Abschnitt
mit gleichwertigen Fakten ausfüllen; Deutsch ist keine Kurzfassung.

Für jede nicht triviale Änderung gelten die
[Richtlinie zur Nachvollziehbarkeit](../docs/change-traceability.de.md) und
der [Change-Record-Index](../reports/audits/change-records/README.de.md).

### Zusammenfassung
Beschreibe die Änderung kurz.

### Art der Änderung
Bitte alle zutreffenden Punkte auswählen:

- [ ] Bug fix
- [ ] Feature
- [ ] Documentation
- [ ] Refactoring
- [ ] Security / hardening
- [ ] CI / build

### Change Record

Change-ID oder Link zum Change Record: <!-- CR-YYYYMMDD-short-slug oder erklären, warum kein Record erforderlich ist -->

### Motivation und Kontext
Warum ist diese Änderung nötig?

### Akzeptanzkriterien

- [ ] <Beobachtbares Kriterium>
- [ ] <Beobachtbares Kriterium>

### Detaillierte Änderungen
Liste die wichtigsten Änderungen in diesem Pull Request auf.

### Tests und Befehlsergebnisse

Jeden tatsächlich ausgeführten Befehl aufführen. Keine vollständigen Logs oder
sensiblen Rohdaten einfügen.

| Exakter Befehl | Exit-Code oder Ergebnis | Kurze sanitisierte Zusammenfassung | Kanonischer Evidence-Pfad | Run-ID |
| --- | --- | --- | --- | --- |
| <!-- Befehl --> | <!-- Ergebnis --> | <!-- Zusammenfassung --> | <!-- Pfad oder None --> | <!-- Run-ID oder None --> |

### Runtime-Evidence

Run-ID, Profil/Scope, kanonischen sanitisierten Evidence-Ort und abgegrenzte
Beobachtung angeben. Falls keine vorliegt, schreiben: „Es wurde keine
Runtime-Evidence erhoben oder beansprucht.“ Builds, Konfigurationschecks,
Lint, Unit-Tests und Smoke-Ergebnisse sind für sich keine Runtime-Evidence.

### Sicherheitsauswirkung
Beschreibe alle Sicherheitsauswirkungen, einschließlich der Frage, ob diese Änderung Standardwerte, Validierung, Logging oder Threat Exposure verändert.

### Dokumentationsstatus

Aktualisierte Dokumentation und Beispiele einschließlich erforderlicher
Sprachbegleiter aufführen oder „Keine Dokumentationsaktualisierung nötig“ mit
Begründung schreiben.

### Bekannte Einschränkungen

Bekannte Einschränkungen und verbleibende Risiken aufführen oder „None“
schreiben.

### Nicht ausgeführte Prüfungen

Jede relevante nicht ausgeführte Prüfung und den Grund nennen. Einen geplanten
oder vermuteten Test nicht als bestanden beschreiben.

### Breaking Changes
Liste alle Breaking Changes auf. Falls es keine gibt, schreibe "None".

### Checkliste

- [ ] Ich habe meine eigenen Änderungen geprüft.
- [ ] Ich habe exakte Befehle und tatsächliche Ergebnisse dokumentiert oder nicht ausgeführte Prüfungen erklärt.
- [ ] Ich habe die Dokumentation bei Bedarf aktualisiert.
- [ ] Der erforderliche Change Record stimmt mit dem tatsächlichen finalen Diff und realen Testergebnissen überein.
- [ ] Ich habe keine Secrets, vollständigen Umgebungsvariablen, Cookies, Tokens, Bodies, privaten Schlüssel, Caches oder sensiblen Rohdaten hinzugefügt.
- [ ] Ich habe Breaking Changes dokumentiert, falls zutreffend.
