# Atlas Workspace

Atlas is a bounded June-owned validation/sandbox executor. This workspace owns only local
validation artifacts and the canonical Atlas validation contract.

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
