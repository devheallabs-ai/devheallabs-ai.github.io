# DH-ADOM Reference Implementation

This is a small, dependency-light reference implementation of the core DH-ADOM semantics.

It is intentionally not a production agent runtime. Its purpose is to make the normative model executable and testable.

Implemented reference behaviors:

- Agent registry
- Root → Feature routing
- Delegation contracts
- Scope validation
- Budget checks
- Specialist task execution
- Audit events
- Structured handoff
- State tracking

Run:

```bash
python -m unittest discover -s tests -v
python examples/demo.py
```
