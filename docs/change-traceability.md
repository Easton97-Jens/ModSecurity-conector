# Change traceability policy

**Language:** English | [Deutsch](change-traceability.de.md)

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

Each record must use sections for Motivation, Acceptance criteria, Technical
decisions, Security impact, Changed files, Tests and actual results, Runtime
evidence, Checks not run, Known limitations, Residual risks, and Final review
status. A record is incomplete until its paired language version contains the
same facts.

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
