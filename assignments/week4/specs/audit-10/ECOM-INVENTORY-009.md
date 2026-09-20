# Spec: Reserve Inventory
**ID:** ECOM-INVENTORY-009
**Status:** Draft

## User Story
As the system, I want to reserve inventory when an order is placed, so that the same stock isn't sold to two customers at once.

## Scope
- In scope: reserving stock quantity for each product ID in an order at checkout time.
- Out of scope: releasing reservations (see cancel/expiry flow), restocking.

## Business Rules
- **BR-01:** Available stock for a product ID shall not go below zero as a result of a reservation.
- **BR-02:** Reservations shall expire and release stock if payment is not completed within 15 minutes.

## Scenarios

### Happy path
**Scenario 1: Successfully reserving stock**
```
GIVEN a product ID with 10 units available
WHEN an order reserves 2 units
THEN available stock shall become 8
AND a reservation record shall be created with a 15-minute expiry
```

### Failure paths
**Scenario 2: Insufficient stock**
```
GIVEN a product ID with 1 unit available
WHEN an order attempts to reserve 2 units
THEN the system shall return error "Insufficient stock" with code 409
AND no reservation shall be created
```

**Scenario 3: Reservation expires unpaid**
```
GIVEN a reservation of 2 units created 15 minutes ago
AND the associated order has not completed payment
WHEN the expiry check runs
THEN the reservation shall be released
AND available stock shall increase by 2
```

## Non-Functional Requirements
- **NFR-01 (Performance):** Stock reservation shall complete within 150ms at P95, under normal load (up to 500 concurrent users).

## Traceability Table
| Requirement ID | Description | Business Goal | Related Test(s) |
|---|---|---|---|
| ECOM-INVENTORY-009-BR-01 | Stock cannot go below zero | BG-05: Prevent overselling of limited stock | ECOM-INVENTORY-009-TC-01 |
| ECOM-INVENTORY-009-BR-02 | 15-minute reservation expiry | BG-05: Prevent overselling of limited stock | ECOM-INVENTORY-009-TC-02 |
| ECOM-INVENTORY-009-NFR-01 | Reservation latency | BG-05: Prevent overselling of limited stock | ECOM-INVENTORY-009-TC-03 |