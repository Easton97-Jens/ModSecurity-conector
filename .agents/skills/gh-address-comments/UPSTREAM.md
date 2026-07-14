# Upstream provenance: `gh-address-comments`

- Upstream owner and repository: OpenAI, [`openai/plugins`](https://github.com/openai/plugins)
- Immutable source commit: `11c74d6ba24d3a6d48f54a194cd00ef3beea18f9`
- Source path: `plugins/github/skills/gh-address-comments/`
- Imported guidance source: [`SKILL.md`](https://raw.githubusercontent.com/openai/plugins/11c74d6ba24d3a6d48f54a194cd00ef3beea18f9/plugins/github/skills/gh-address-comments/SKILL.md)
- License source: [`LICENSE.txt`](https://raw.githubusercontent.com/openai/plugins/11c74d6ba24d3a6d48f54a194cd00ef3beea18f9/plugins/github/skills/gh-address-comments/LICENSE.txt)
- Upstream plugin version: `0.1.6`
- License: Apache-2.0
- Integration status: adapted and vendored at a fixed source commit.

## Local changes

The helper `scripts/fetch_comments.py` is not imported. It performs
authenticated GraphQL reads and transfers review text into the session. The
local adapter adds strict task scope, evidence, privacy, and delivery controls.

## Update procedure

Re-audit a new immutable revision before use. Review license, helper behavior,
authentication/data handling, local-policy compatibility, and documentation;
then update the lock manifest and tests in the same reviewed change.
