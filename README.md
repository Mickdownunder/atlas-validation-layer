# atlas-validation-layer

[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Stack Setup](https://img.shields.io/badge/docs-stack%20setup-black.svg)](https://github.com/Mickdownunder/operator-control-plane/blob/main/docs/STACK_SETUP.md)

Kurz auf Deutsch: `atlas-validation-layer` ist die begrenzte
Validierungs- und Sandbox-Schicht des Stacks. ATLAS prueft, validiert und
verifiziert Ergebnisse, ohne selbst zur Truth-, Planungs- oder
Orchestrierungsschicht zu werden.

`atlas-validation-layer` is the bounded validation layer of the public stack.
ATLAS exists to run checks that should not be silently folded into the execution
path: sandbox inspection, mini-audits, validation probes, and contract-shaped
verification attempts that feed back into Operator without becoming a second
planner.

## What ATLAS Actually Does

ATLAS exposes bounded validation entrypoints such as:

- `bin/atlas-sandbox-run`
- `bin/atlas-run-sandbox`

Those entrypoints:

- validate mission, dispatch, and optional project bindings
- acquire dispatch locks to avoid duplicate active validations
- run sandbox and health-oriented checks under explicit plans
- produce a canonical `atlas_validation.json` artifact
- return a structured recommendation rather than mutating project truth directly

## Why ATLAS Exists

Execution and validation should not be the same thing.

ATLAS provides a separate wall between:

- "the system ran"
- "the result should be trusted"

That separation matters because:

- Operator remains the only truth layer
- ARGUS can stay focused on bounded execution
- validation can fail, warn, or stop without becoming hidden execution detail
- sandbox-backed checks can be isolated from the control plane

## What Is In This Repository

- validation and sandbox entrypoints
- ATLAS validation contract logic
- mini-audit and stack-check behavior
- tests for the public validation surface

## Validation Contract

The main public output is `atlas_validation.json`.

That contract records things such as:

- mission and dispatch identity
- bound project identity when present
- attempt identity and run directory
- overall validation outcome
- recommendation and failure classification

See:

- `ATLAS_VALIDATION_CONTRACT.md`
- `lib/atlas_validation_contract.py`

## Configuration

Copy `.env.example` into your local environment management and set:

- `ATLAS_WORKSPACE_ROOT`
- `OPERATOR_ROOT`
- optionally `JUNE_WORKSPACE_ROOT`

## Test

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

## How It Fits Into The Stack

ATLAS is not meant to become a free-floating validator product inside this
stack. It is the bounded verification wall around Operator-driven work.

- Operator owns project truth and decisions about project state
- ARGUS executes bounded attempts
- ATLAS validates those attempts and emits structured outcomes

For cross-repo wiring and environment variables, see:
[operator-control-plane/docs/STACK_SETUP.md](https://github.com/Mickdownunder/operator-control-plane/blob/main/docs/STACK_SETUP.md)
