---
name: port-endpoint
description: Porting an endpoint from the old Flask prototype (legacy/) to FastAPI while preserving behavior.
---

# Porting an endpoint

1. Find the endpoint in legacy/ and describe its behavior in docs/business-rules.md.
2. Write a characterization test that records the current response of the legacy version.
3. Implement the endpoint in apps/api by layers: router, service (path `/api/v1/...`).
4. Run the characterization test against the new implementation.
5. If the test fails, at most three fix attempts are allowed. After the third
   failure, stop, state a hypothesis about the cause and ask for a human decision.
6. Do not change the characterization test to make it pass.
