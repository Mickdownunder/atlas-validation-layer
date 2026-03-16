# atlas-validation-layer

[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Stack Setup](https://img.shields.io/badge/docs-stack%20setup-black.svg)](https://github.com/Mickdownunder/operator-control-plane/blob/main/docs/STACK_SETUP.md)

`atlas-validation-layer` is the bounded validation layer of the Operator
research stack. ATLAS runs sandboxed checks, mini-audits, and contract-shaped
verification steps that feed back into Operator without becoming a second
planner.

## What This Repo Contains

- sandbox and mini-audit entrypoints
- Atlas validation contract logic
- validation knowledge maps and supporting docs
- tests for the public validation surface

## Canonical entrypoints
- `bin/atlas-sandbox-run`
- `bin/atlas-run-sandbox`

## Configuration

Copy `.env.example` into your local environment management and set:

- `ATLAS_WORKSPACE_ROOT`
- `OPERATOR_ROOT`
- optionally `JUNE_WORKSPACE_ROOT`

## Ownership boundaries
- June owns mission, dispatch, and escalation truth.
- Operator owns project truth.
- Atlas writes only bounded attempt artifacts and `atlas_validation.json`.

## Contracts
- `ATLAS_VALIDATION_CONTRACT.md`
- `lib/atlas_validation_contract.py`

## Tests
Run:

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

## Full-Stack Wiring

For cross-repo wiring and environment variables, see the Operator stack guide:
[operator-control-plane/docs/STACK_SETUP.md](https://github.com/Mickdownunder/operator-control-plane/blob/main/docs/STACK_SETUP.md)
