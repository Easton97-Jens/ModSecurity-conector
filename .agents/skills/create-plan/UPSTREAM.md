# Upstream provenance: `create-plan`

- Upstream owner and repository: OpenAI, [`openai/skills`](https://github.com/openai/skills)
- Immutable source commit: `a5119697b819090e00e5d11ee1d86834d7c1043a`
- Source path: `skills/.experimental/create-plan/`
- Imported file: [`SKILL.md`](https://raw.githubusercontent.com/openai/skills/a5119697b819090e00e5d11ee1d86834d7c1043a/skills/.experimental/create-plan/SKILL.md)
- License source: [`LICENSE.txt`](https://raw.githubusercontent.com/openai/skills/a5119697b819090e00e5d11ee1d86834d7c1043a/skills/.experimental/create-plan/LICENSE.txt)
- License: Apache-2.0
- Integration status: adapted and vendored historical source; it was not
  retrieved from a moving branch.

## Local changes

The repository version replaces generic planning guidance with the mandatory
ModSecurity-conector workflow, Parent/Framework separation, explicit evidence,
and safe delivery boundaries. It imports no scripts, dependencies, network
configuration, credentials, or command automation.

## Update procedure

Do not overwrite this adapter from a moving upstream reference. Re-audit a
new immutable commit, license, behavior, and local-policy compatibility; update
`ci/tooling/codex-extensions.lock.yml`, this file, tests, and bilingual
documentation in the same reviewed change.
