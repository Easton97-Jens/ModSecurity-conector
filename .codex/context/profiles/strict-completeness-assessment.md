# Strict Execution Completeness Overlay

## Purpose

Use only when the user explicitly requires that every applicable mandatory target be attempted to completion rather than closed with a normal `blocked` or `not_run` target status.

This overlay preserves safety and permission boundaries. It never authorizes bypassing them.

## Target-result model

A target test receives a final assessment result only when it was actually executed (`passed` or `failed`) or is technically proven `not_applicable`.

If an applicable target cannot be reached because a prerequisite/setup/access/environment check fails, record the prerequisite check result and leave the target as an explicit unresolved coverage gap. Do not invent a target result and do not remove it from completeness accounting.

## Required behavior

For each unresolved applicable target:

1. diagnose the first relevant prerequisite failure;
2. inspect existing local/repository-native prerequisites and setup paths;
3. establish missing task-local prerequisites when current authority permits;
4. rerun the original target after each meaningful setup correction;
5. continue all independent targets;
6. retain earlier failed attempts and the reached stage;
7. never weaken tests/security controls/quality gates to obtain execution.

## Completeness

A full strict assessment is complete only when every applicable mandatory target has a final executed result or justified `not_applicable`. Remaining unresolved target IDs make the assessment partial/failed according to the parent profile's completion model.

This overlay affects assessment completeness accounting only. Normal repository policies may still use `blocked`/`not_run` for their own checks and evidence.
