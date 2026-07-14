# Upstream provenance: `gh-fix-ci`

- Upstream owner and repository: OpenAI, [`openai/plugins`](https://github.com/openai/plugins)
- Immutable source commit: `11c74d6ba24d3a6d48f54a194cd00ef3beea18f9`
- Source path: `plugins/github/skills/gh-fix-ci/`
- Imported guidance source: [`SKILL.md`](https://raw.githubusercontent.com/openai/plugins/11c74d6ba24d3a6d48f54a194cd00ef3beea18f9/plugins/github/skills/gh-fix-ci/SKILL.md)
- License source: [`LICENSE.txt`](https://raw.githubusercontent.com/openai/plugins/11c74d6ba24d3a6d48f54a194cd00ef3beea18f9/plugins/github/skills/gh-fix-ci/LICENSE.txt)
- Upstream plugin version: `0.1.6`
- License: Apache-2.0
- Integration status: adapted and vendored at a fixed source commit.

## Local changes

The helper script `scripts/inspect_pr_checks.py` is not imported. It uses
authenticated GitHub reads and can retrieve check/job logs, which would expand
the repository's data surface. The local adapter requires exact-SHA evidence,
minimal log collection, local verification, and the repository delivery loop.

## Update procedure

Re-audit an immutable upstream revision, its path-level license, script
behavior, credentials/data handling, and the repository's delivery policy.
Update the lock manifest, this provenance file, tests, and bilingual
documentation together.
