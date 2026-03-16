# atlas-validation-layer

[![CI](https://github.com/Mickdownunder/atlas-validation-layer/actions/workflows/tests.yml/badge.svg)](https://github.com/Mickdownunder/atlas-validation-layer/actions/workflows/tests.yml)
[![Release](https://img.shields.io/github/v/tag/Mickdownunder/atlas-validation-layer?label=release)](https://github.com/Mickdownunder/atlas-validation-layer/releases)
[![License: Apache-2.0](https://img.shields.io/github/license/Mickdownunder/atlas-validation-layer)](LICENSE)
[![Stack Setup](https://img.shields.io/badge/docs-stack%20setup-black.svg)](https://github.com/Mickdownunder/operator-control-plane/blob/main/docs/STACK_SETUP.md)

`atlas-validation-layer` is the bounded validation layer in the
`operator-control-plane` stack. ATLAS runs validation and sandbox checks that
should stay independent from execution, then emits a canonical validation
artifact.

## What ATLAS Does

- Executes bounded validation plans through `bin/atlas-sandbox-run`
- Runs sandbox checks via `bin/atlas-run-sandbox`
- Enforces identity binding and duplicate-dispatch locks
- Emits canonical validation output (`atlas_validation.json`)

## What ATLAS Does Not Do

- Does not own project truth or state transitions (Operator does)
- Does not own execution authority (ARGUS does)
- Does not own orchestration or dispatch authority (June does)

## Quickstart

1. Configure environment from `.env.example`:

```bash
cp .env.example .env.local
# set ATLAS_WORKSPACE_ROOT, OPERATOR_ROOT, optional JUNE_WORKSPACE_ROOT
```

2. Run a bounded status validation path:

```bash
bin/atlas-sandbox-run status
```

3. Run tests:

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

## Public Contract

ATLAS publishes `atlas_validation.json` with mission/dispatch/project identity,
attempt metadata, overall outcome, recommendation, and failure classification.

- Contract spec: `ATLAS_VALIDATION_CONTRACT.md`
- Reference implementation: `lib/atlas_validation_contract.py`

## Stack Integration

- Operator: project truth and control-plane authority
- ARGUS: bounded execution attempts
- ATLAS: bounded validation outcomes for executed attempts

Cross-repo wiring and environment conventions:
[operator-control-plane/docs/STACK_SETUP.md](https://github.com/Mickdownunder/operator-control-plane/blob/main/docs/STACK_SETUP.md)

Runnable bounded public demo (2-5 min):
[operator-control-plane/docs/DEMO.md](https://github.com/Mickdownunder/operator-control-plane/blob/main/docs/DEMO.md)
