# Change Record: <title>

**Language:** English | [Deutsch](TEMPLATE.de.md)

Copy this file and its German companion to
<code>&lt;change-id&gt;.md</code> and
<code>&lt;change-id&gt;.de.md</code>. Replace every placeholder. Do not commit
full logs, raw runtime data, secrets, complete environment variables, cookies,
tokens, bodies, private keys, caches, or build artifacts.

## Identity

| Field | Value |
| --- | --- |
| Title | &lt;short descriptive title&gt; |
| Change ID | CR-YYYYMMDD-short-slug |
| Date (UTC) | YYYY-MM-DDTHH:MM:SSZ |
| Author or executing agent | &lt;name or agent identity&gt; |
| Base revision | &lt;full commit ID before the change&gt; |
| Related issue or pull request | &lt;link or None&gt; |
| Final revision | &lt;commit ID or not committed&gt; |

## Motivation and problem statement

<Describe the task, impact, and why the change is needed.>

## Affected components and security boundaries

<List changed components, interfaces, trust/data boundaries, and local-only
configuration that is intentionally outside the versioned diff.>

## Acceptance criteria

| Criterion | Status | Evidence |
| --- | --- | --- |
| &lt;observable criterion&gt; | &lt;met / not met / deferred&gt; | &lt;test, review, or record section&gt; |

## Alternatives investigated

<Describe considered alternatives and why they were rejected or not selected.>

## Implementation decision and rationale

<Describe the chosen design, including security-relevant tradeoffs.>

## Changed files

<List the actual final versioned files. Separately identify any intentional
local, unversioned configuration without presenting it as part of the Git
diff.>

## Tests added or changed

<List tests added or changed, or state None.>

## Commands executed

| Exact command | Exit code or result | Sanitized relevant summary | Canonical evidence path | Run ID |
| --- | --- | --- | --- | --- |
| &lt;exact command&gt; | &lt;0 / PASS / other result&gt; | &lt;short factual summary&gt; | &lt;repo-relative path, portable placeholder, or None&gt; | &lt;run ID or None&gt; |

Record every command that actually ran. Do not paste full output. A planned,
skipped, or assumed command belongs in “Checks not run and rationale,” not as a
passing result.

## Security impact

<Describe the security effect, changed boundaries/defaults/validation/logging,
or state No security behavior change.>

## Documentation changes

<List updated documentation/examples and their language companions, or state
None.>

## Runtime evidence

<Provide the run ID, profile/scope, canonical sanitized evidence location, and
bounded observation; or state explicitly: “No runtime evidence was collected
or claimed for this change.” A build, lint, configuration check, unit test, or
smoke is not a runtime claim by itself.>

## Known limitations

<List known limitations or None.>

## Remaining risks

<List remaining risks, mitigations, or None.>

## Checks not run and rationale

<List each relevant check not run and why, or state None.>

## Final diff and review status

<State the final diff/whitespace review result, review status, whether the
record matches the actual final diff and real test outcomes, and the intended
commit or pull-request status.>
