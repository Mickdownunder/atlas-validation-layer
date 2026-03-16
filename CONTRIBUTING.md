# Contributing

## Scope

`atlas-validation-layer` is the bounded validation and sandbox layer.
Contributions should preserve these rules:

- ATLAS is not a global orchestrator.
- Operator owns project truth.
- ATLAS writes bounded local artifacts plus `atlas_validation.json`.
- Stdout envelope compatibility is part of the public contract.

## Local Checks

Run:

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

## Change Rules

- Do not add arbitrary shell execution paths.
- Prefer environment-variable configuration over hard-coded host paths.
- Keep validation-contract compatibility unless you intentionally version it.
- Add tests when changing runner guards, sandbox entrypoints, or contract logic.
