# Documentation style guide

**Language:** English | [Deutsch](documentation-style-guide.de.md)

This guide applies to repository-owned Markdown. It is a maintenance rule, not
a generator specification: do not manually rewrite generated documents.

## Required document shape

- Use exactly one H1, followed by a logical H2/H3 hierarchy.
- Place the language switch directly below the H1 in every English/German pair.
- Write short paragraphs and use a table only when readers must compare values.
- Give every code block an appropriate language tag such as <code>sh</code>,
  <code>make</code>, <code>json</code>, <code>yaml</code>, or <code>text</code>.
- Name the document’s purpose, currentness, source of truth, and claim boundary
  when they would otherwise be unclear.
- Prefer repository-relative links and explain what their starting directory is.

Use the checker before handing off a documentation change:

~~~sh
make check-bilingual-docs
~~~

This target checks required English/German companions and local Markdown links.
It does not certify the factual correctness of a runtime claim.

## English/German technical parity

English and German documents must contain the same technical facts. Keep
variable names, defaults, allowed values, paths, targets, IDs, status values,
rule IDs, case IDs, and integration-mode names identical. Translate prose, not
machine-readable values.

Create or update both files in one change. When a table exists in one language,
keep equivalent rows and values in the companion. A German link should use the
German companion target when one exists. Keep the standard headers exactly:

~~~text
Language line: English | German companion `file.de.md`
German line: English companion `file.md` | Deutsch
~~~

### Translation-exempt connector metadata

Only `connectors/**/ORIGIN.md` and `connectors/**/TODO.md` are exempt from
the companion-file rule. They are provenance or work-tracking metadata rather
than reader guides; their machine-oriented names and values remain
single-language. This exception does not cover connector READMEs, `docs/`,
`harness/`, `src/`, or PoC design notes: those reader-facing documents need a
German companion.

`docs/en/README.md` and `docs/de/README.md` are the one deliberate legacy
cross-directory language-index pair. They retain their stable navigation paths
instead of adding misleading `README.de.md` files. The bilingual checker
validates both the exception and their reciprocal language links.

## Variables and placeholders

Explain every user-adjustable value in the same document near its first use,
then link to the central [variable reference](../configuration/variables.md).
The local explanation answers:

1. What is the name and purpose?
2. What format and values are allowed?
3. Is it required or optional, and what is the actual default?
4. Who sets it, what scope does it affect, and what happens when it is wrong?
5. Is it secret-bearing or otherwise security-sensitive?
6. What realistic example can the reader adapt?

Use this pattern: introduce the variable in prose, then show the command.
For example, say that <code>BUILD_ROOT</code> is an optional absolute writable
build directory outside the checkout because the root Makefile derives a
default. Then show:

~~~sh
make quick-check BUILD_ROOT="/srv/modsecurity-work/build"
~~~

After the command, explain that <code>/srv/modsecurity-work/build</code> is an
example absolute runtime path, not the repository root or a system directory,
and link to the central
[variable reference](../configuration/variables.md#runtime-and-repository-paths).

Do not leave an executable placeholder unexplained. Immediately explain
<code>&lt;connector&gt;</code>, <code>&lt;path&gt;</code>,
<code>REPLACE_ME</code>, <code>CHANGE_ME</code>, <code>$VAR</code>, and
<code>$(MAKE_VAR)</code> with allowed values and an example. Explain example
YAML/JSON path, host, and port values as replaceable sample values even when
they are not syntactic variables.

For example, state that <code>&lt;connector&gt;</code> is one of
<code>apache</code>, <code>nginx</code>, <code>haproxy</code>,
<code>envoy</code>, <code>traefik</code>, or <code>lighttpd</code>, then give
the literal example <code>make build-nginx</code>.

Do not use unexplained ellipses in executable examples. If a focused
configuration omits standard directives, say so in prose and link to a
complete checked-in example.

## Paths, defaults, and secrets

Label the role of every meaningful path: repository-relative, absolute runtime,
host installation, generated, temporary, cache, or evidence. Do not publish
developer-specific paths such as a personal home directory or a local
workspace. Prefer a portable example such as
<code>/srv/modsecurity-work/build</code> and label it as an example.

Distinguish these terms exactly:

| Label | Meaning |
|---|---|
| Repository default | A value assigned by a checked-in Makefile or configuration |
| Host default | A value supplied by the installed host software |
| Example value | A readable value used only to illustrate format |
| Recommended local value | A suggested portable local choice, not an assigned default |
| CI value | A value derived or injected by CI |
| No default | The caller or target must provide the value |

Never put private keys, tokens, passwords, cookies, authorization headers, API
keys, client secrets, or real certificates in documentation. Use
<code>&lt;secret-from-secure-store&gt;</code>, say that it must not be committed
or copied into canonical evidence, and avoid command-line examples that expose
it in a process list.

## Commands, targets, status, and IDs

For each documented Make target, state its purpose, prerequisites, important
input variables, output/artifacts, exit-code behavior, and difference from a
nearby target. Explain target placeholders immediately.

Use the common status names precisely: <code>PASS</code>, <code>FAIL</code>,
<code>BLOCKED</code>, <code>NOT EXECUTED</code>, <code>NOT APPLICABLE</code>,
<code>UNSUPPORTED</code>, and historical <code>NOT_EXECUTABLE</code>. Explain
that process exit code <code>0</code> means the invoked process completed its
own technical contract; it does not mean every case in a catalog passed.

Give rule IDs, case IDs, message IDs, schema fields, and integration modes
context near their use. State whether an ID belongs to the repository’s
No-CRS baseline rather than OWASP CRS. Define non-obvious terms such as
<code>EOS</code>, <code>HTX</code>, <code>ext_proc</code>, or
<code>APXS</code> locally at first use and link to the
[glossary](../reference/glossary.md).

## Claims and evidence

Keep source, configuration, build, runtime, and canonical evidence claims
separate. State the selected host profile and the exact evidence boundary when
describing a result. Do not turn a capability declaration, a config-load
success, or a compatibility smoke into a broader assurance.

Do not claim production readiness, CRS verification/completeness, complete
HTTP/2 verification, complete HTTP/3 verification, a complete matrix, or
strict verification for all connectors. Use precise alternatives such as
“the selected HTTP/1.1 core route,” “run-scoped evidence,” or “not executed”
when that is what the artifacts support.

## Generated and historical documents

Recognize generated files from their generated notice, directory, or generator
contract. Update the generator/source of truth and regenerate instead of
editing output by hand. Preserve generated notices and machine-readable
values.

Historical reports retain their provenance. Mark a superseded report as
historical and link to the current replacement; do not silently rewrite
run IDs, commits, counts, or previous conclusions as current facts.

## Review checklist

- Both language files exist and have the standard headers.
- Local links resolve and German links point to German companions where present.
- Each new command has a purpose, prerequisite, input explanation, and outcome.
- Each variable/placeholder has a nearby explanation and realistic example.
- Path roles and defaults are labelled accurately.
- Secrets and sensitive data are absent.
- IDs, statuses, integration modes, and unusual abbreviations have context.
- Generated files were changed only through their generator.
- Claims remain within the recorded evidence boundary.
