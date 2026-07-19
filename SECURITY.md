# Security policy

**Language:** English | [Deutsch](SECURITY.de.md)

## Reporting a vulnerability

Please do not open a public issue or publish proof-of-concept details for a
suspected security vulnerability. Use
[GitHub Private Vulnerability Reporting](https://github.com/Easton97-Jens/ModSecurity-conector/security/advisories/new)
instead. This repository's private reporting feature is the intended
confidential channel.

Include a concise description, the affected version, commit, or branch when
known, safe reproduction steps, the expected and observed result, and a clear
assessment of the potential impact. Redact tokens, credentials, private data,
and exploit payloads from the report and any attachments.

## Supported versions

Security reports are assessed against the current `master` branch. No older
release line is currently declared as supported for security fixes. If you can
reproduce the issue only on an older revision, include that revision and check
whether it also affects current `master`.

## Scope and safe research

The report should concern this repository's versioned content or its published
GitHub Actions configuration. Do not test against systems you do not own or
have permission to assess, do not access other users' data, and avoid any
action that could disrupt services or create a privacy risk.

## What happens next

Maintainers will assess a private report, may request clarification, and will
coordinate a fix or mitigation when the report is confirmed. Disclosure timing
is coordinated with the reporter when practical. No response-time commitment
is made by this policy.

## Public channels are not confidential

GitHub issues, pull requests, discussions, and public comments are not
confidential reporting channels. Do not put secrets, personal data, or exploit
details in them. Use the private reporting channel above for security reports.
