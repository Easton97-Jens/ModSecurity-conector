# Python Environment, Dependencies, and External CLI Policy

## Environment ownership

Parent and Framework Python dependency contracts are separate. For Parent imported-code/test/generator work, select the Parent repository virtual environment explicitly when it exists and matches the task's repository/CI compatibility contract.

Use:

- `PYTHONNOUSERSITE=1`
- `PIP_REQUIRE_VIRTUALENV=true`
- `PIP_DISABLE_PIP_VERSION_CHECK=1`

Never mutate system Python or the user site. Do not use bare `pip` for repository dependency changes.

A local `.venv` or `.python-version` is evidence of the current checkout/tool selection, not by itself a new compatibility claim beyond versioned repository/CI contracts.

## Framework

Framework work selects a Framework-owned interpreter/environment under Framework policy. Do not silently substitute the Parent `.venv` merely because imports happen to work. A shared environment requires a documented compatibility/lock contract.

## Repository dependency versus external CLI

Classify a Python package before installation:

- repository dependency: imported by product, versioned tests, versioned generator, or durable CI;
- external CLI: used only as a standalone analysis/test command;
- optional tool: helpful but not required by repository/task contract.

A new repository dependency requires explicit scope, owning repository, reproducible version/lock change, tests, supply-chain/license review, documentation/Change Record when applicable, and normal delivery.

## External CLI

A missing standalone CLI may use only the approved isolated external tool workflow when the current task needs it and all exact-version/source/storage/security predicates pass. Keep it outside Parent/Framework repository environments and outside MRTS.

Do not install from `latest`, ranges, VCS/local/editable/direct URLs, untrusted indexes, or source builds automatically. Do not use credentials in package URLs/logs/manifests.

A blocked required tool is a truthful blocker; do not replace it with system/user-site installation or silently skip the required check.

## Python quality

Syntax/import/Ruff/Pyright/pip-check/unit-test/dependency-audit results establish different facts. Report them separately and use the current repository contract to decide applicability.
