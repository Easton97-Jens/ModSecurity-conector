# Change traceability policy

**Language:** English | [Deutsch](change-traceability.de.md)

## Quick orientation

This policy keeps documentation and delivery facts reviewable. For a normal
non-trivial change, the practical rule is: update English and German together,
keep technical literals identical, record only checks that actually ran, do not
turn build/static results into runtime claims, and update generated material
through its generator. The pull-request description and any required Change
Record must match the final diff and observed results.

This policy makes bilingual maintenance part of the definition of done for
repository-owned, versioned, reader-facing content. It applies to every
feature, bug fix, security fix, and other non-trivial change.

## Scope and language model

English is the technical primary language. German is a complete companion
version, not a shortened summary. Every relevant versioned, reader-facing
document must be present and kept current in both languages, normally as
<code>name.md</code> and <code>name.de.md</code>.

## Required bilingual content

| Content type | Bilingual requirement |
| --- | --- |
| Repository and connector documentation | Keep READMEs, connector guides, installation, configuration, build, test, architecture, design, migration, and limitation documentation as English/German pairs. |
| Security and evidence material | Keep security documentation, audit and finding reports, Change Records, manually maintained reports, test results, runtime evidence, residual risks, and related warnings equivalent in both languages. |
| User-facing material | Keep examples, release notes, changelogs, issue templates, and other user-facing GitHub text bilingual; the pull-request template contains full English and German sections in one file. |
| New documentation | Create both language files in the same change and add reciprocal language switches. |

## Content parity

Both versions must communicate the same functions, prerequisites,
configuration, security warnings, examples, commands, supported and unsupported
scenarios, known limitations, test results, runtime evidence, residual risks,
links, and references. Keep heading and table structure aligned whenever the
repository check requires it. No language version may contain a material fact
that is missing from the other.

## Technical content that remains unchanged

Do not translate source code; variable, function, class, type, or API-field
names; protocol names; configuration keys; file names or paths; shell commands;
command-line options; code blocks; technically exact error messages; commit
hashes; run IDs; URLs; or machine-readable JSON, YAML, TOML, or XML. Keep
source-code comments in English. Translate reader-facing explanation around
those literals while preserving the literal itself.

## Local Codex files

The following local-only configuration does not need a German companion:
<code>AGENTS.md</code>, <code>AGENTS.override.md</code>, root Markdown control
files included from them using <code>@...</code>, and <code>.codex/</code>.
Never create a German companion for an active local control file. These local
instructions still require Codex to maintain all versioned, reader-facing
content under this policy.

## Change workflow

For every non-trivial change:

1. Identify affected English and German documents before editing.
2. Edit both versions together; create both files immediately for a new
   document.
3. Keep factual content, technical values, links, headings, tables, tests,
   evidence, limitations, and risks synchronized.
4. Prefer links to German companions from German documents when a companion
   exists.
5. Preserve commands and other technical literals unchanged in both versions.
6. Record both language paths in the Change Record.
7. Update generators or source data instead of editing generated output alone,
   and ensure the generator emits both language versions.
8. Run the bilingual documentation check before completing the work.

## Change Records

Store Change Record pairs under
<code>reports/audits/change-records/</code>. Name every pair
<code>&lt;change-id&gt;-&lt;name&gt;.md</code> and
<code>&lt;change-id&gt;-&lt;name&gt;.de.md</code>. The English and German
records must contain the same facts and actual values.

| Required metadata | Requirement |
| --- | --- |
| Change ID | Use the same stable identifier in both records. |
| Date and base revision | Record the same date and base revision in both records. |
| Motivation and acceptance criteria | Explain the same reason for the change and the same measurable completion conditions. |
| Technical and security decisions | Record the same technical decisions, security impact, and affected boundary. |
| Files and verification | List the same changed files, test commands, actual results, runtime evidence, and checks not run. |
| Remaining state | Record the same known limitations, residual risks, and final review status. |

The exact section names below are required, not synonyms. Their single
machine-readable owner is
<code>ci/checks/documentation/check-bilingual-docs.py</code>.
The regression test checks these tables against that owner.

| English | Deutsch |
| --- | --- |
| <code>## Identity</code> | <code>## Identität</code> |
| <code>## Motivation and problem statement</code> | <code>## Motivation und Problemstellung</code> |
| <code>## Acceptance criteria</code> | <code>## Akzeptanzkriterien</code> |
| <code>## Implementation decision and rationale</code> | <code>## Implementierungsentscheidung und Begründung</code> |
| <code>## Changed files</code> | <code>## Geänderte Dateien</code> |
| <code>## Commands executed</code> | <code>## Ausgeführte Befehle</code> |
| <code>## Security impact</code> | <code>## Security-Auswirkung</code> |
| <code>## Runtime evidence</code> | <code>## Runtime-Evidence</code> |
| <code>## Known limitations</code> | <code>## Bekannte Einschränkungen</code> |
| <code>## Remaining risks</code> | <code>## Verbleibende Risiken</code> |
| <code>## Checks not run and rationale</code> | <code>## Nicht ausgeführte Prüfungen mit Begründung</code> |
| <code>## Final diff and review status</code> | <code>## Finaler Diff- und Review-Status</code> |

Use these exact identity-table labels, with identical values in both languages:

| English | Deutsch |
| --- | --- |
| <code>Change ID</code> | <code>Change-ID</code> |
| <code>Date (UTC)</code> | <code>Datum (UTC)</code> |
| <code>Base revision</code> | <code>Basis-Revision</code> |

Create both language scaffolds together with
<code>ci/tools/new-change-record.py</code> rather than inventing headings.
The tool imports the existing checker schema, validates the generated pair,
and writes only two new files under the existing Change Record archive.
It requires POSIX directory-descriptor support, rejects symlinked output
directories, and never overwrites an existing file. On an ordinary creation
failure it removes only newly created files whose identities still match;
the two-file operation is not crash-atomic.

Set <code>BASE_REVISION</code> to the actual full lowercase 40-character Git
commit SHA of the change's base. Replace <code>my-change</code> with a lowercase,
hyphen-separated name of at most 80 characters. The default date is the current
UTC date; <code>--date YYYY-MM-DD</code> allows an explicit valid date.
Run these native command payloads through any execution wrapper required
by the local working agreement:

~~~sh
python3 ci/tools/new-change-record.py create --name my-change --base-revision "$BASE_REVISION"
python3 ci/tools/new-change-record.py check
python3 -m unittest -v tests.test_change_record tests.test_prepare_reviewed_framework_handoff
~~~

Replace every pending paragraph and the scaffold notice with actual facts,
including actual checks not run and remaining risks. Keep the generated
headings and identity labels unchanged. These are editable scaffolds, not
generated evidence or proof that the change is complete.

The quick-framework CI workflow runs the archive-only check and its
regressions before framework setup. The early check reads only the record
archive and invokes no Git command. It also rejects orphan language files.
It does not replace <code>make check-bilingual-docs</code>,
<code>make check-doc-links</code>, manual bilingual-content review, or any
security/runtime checks. A structurally valid record can still contain
incomplete or inaccurate prose.

## Features and bug fixes

When behavior changes, review and update as applicable in both languages: the
main README, affected connector README, configuration documentation,
architecture or lifecycle documentation, examples, known limitations, and the
Change Record. A build or configuration result is not runtime evidence unless
the documented test layer says so.

## Security findings and fixes

For a security finding or fix, both versions must describe the affected
security boundary, attack preconditions, impact, technical cause, correction
strategy, regression test, verification of the original attack path, residual
risk, and any required migration or configuration guidance. Never put sensitive
payloads, tokens, cookies, bodies, or private environment values in either
version.

## Generated documentation

Do not update only a generated file. Change its generator or source data, make
the generator produce both language versions, and mark automatically translated
or manually maintained companions according to the repository's generated-file
rules.

## Pull requests and GitHub text

The pull-request template must retain full English and German sections. Each
section includes Summary, Motivation, Acceptance criteria, Key changes, Test
commands and actual results, Security impact, Documentation changes, Runtime
evidence, Known limitations, Checks not run, and a Change ID or Change Record
link. Maintain issue templates and other user-facing GitHub text as equivalent
English/German content.

## Completion check

Do not report the task complete when a required language version is missing or
stale. Run the following commands after the change:

~~~sh
make check-bilingual-docs
make check-doc-links
git diff --check
git status --short
~~~

Also manually confirm that no German companion was created for an active local
control file, new versioned policies and templates have
complete language coverage, both versions contain the same technical facts, and
unrelated changes were left untouched.
