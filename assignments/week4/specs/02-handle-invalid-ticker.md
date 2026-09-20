# Spec: Handle Invalid Ticker Input

**ID:** INVALID-TICKER-002
**Status:** Superseded — merged into GET-STOCK-F-001

## Review Note
During peer review, this spec was found to be fully redundant with **GET-STOCK-F-001 (Get Stock Fundamentals)**:

- Ticker emptiness validation → covered by `GET-STOCK-F-001-BR-01` and Scenario 3
- Restricted-character validation → covered by `GET-STOCK-F-001-BR-02` and Scenario 4

**Decision:** Since ticker validation currently has only one consumer (the Get Stock Fundamentals operation), the business rules remain owned by `GET-STOCK-F-001` rather than being factored into a separate shared spec. This spec is retained only as a record of the review decision, and should not be implemented independently.

**Future trigger for revisiting this decision:** if a second ticker-consuming operation is introduced (e.g., Get Stock Price, Get Stock News), extract ticker validation into a standalone spec (e.g., `TICKER-VALID-001`) referenced by ID from every consuming spec, to avoid duplicated/drifting rule definitions.

## Traceability
| Requirement ID | Description | Business Goal | Status |
|---|---|---|---|
| INVALID-TICKER-002 | Ticker validation (empty, restricted chars) | BG-01 | Superseded by GET-STOCK-F-001-BR-01, GET-STOCK-F-001-BR-02 |