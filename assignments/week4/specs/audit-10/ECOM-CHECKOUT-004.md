# Spec: Place Order (Checkout)
**ID:** ECOM-CHECKOUT-004
**Status:** Draft

## User Story
As a shopper, I want to place an order from my cart, so that I can purchase the items in it.

## Scope
- In scope: converting a validated cart into an order record, prior to payment processing.
- Out of scope: payment processing (see ECOM-PAYMENT-005), inventory reservation (see ECOM-INVENTORY-009).

## Business Rules
- **BR-01:** Cart shall contain at least 1 line item to be eligible for checkout.
- **BR-02:** Each SKU in the cart shall still exist in the catalog at the time of checkout.

## Example I/O
Input:
```json
{ "cart_id": "c-9821" }
```
Output (success, 201):
```json
{ "order_id": "o-4471", "status": "pending_payment", "total": 39.98 }
```

## Scenarios

### Happy path
**Scenario 1: Successfully placing an order**
```
GIVEN a cart with 1 or more valid line items
WHEN the shopper initiates checkout
THEN an order shall be created with status "pending_payment"
AND the cart shall be marked as converted
```

### Failure paths
**Scenario 2: Empty cart**
```
GIVEN a cart with 0 line items
WHEN the shopper initiates checkout
THEN the system shall return error "Cart is empty" with code 400
AND no order shall be created
```

**Scenario 3: A SKU was removed from the catalog after being added to the cart**
```
GIVEN a cart containing a SKU that no longer exists in the catalog
WHEN the shopper initiates checkout
THEN the system shall return error "One or more items are no longer available" with code 409
AND no order shall be created
```

### Boundary conditions
**Scenario 4: Cart with exactly 1 line item**
```
GIVEN a cart with exactly 1 line item
WHEN the shopper initiates checkout
THEN an order shall be created successfully
```

## Non-Functional Requirements
- **NFR-01 (Performance):** Checkout shall complete within 400ms at P95, under normal load (up to 200 concurrent users).

## Traceability Table
| Requirement ID | Description | Business Goal | Related Test(s) |
|---|---|---|---|
| ECOM-CHECKOUT-004-BR-01 | Cart must have >=1 item | BG-02: Reduce cart abandonment via fast, reliable cart operations | ECOM-CHECKOUT-004-TC-01 |
| ECOM-CHECKOUT-004-BR-02 | SKU still exists at checkout | BG-02: Reduce cart abandonment via fast, reliable cart operations | ECOM-CHECKOUT-004-TC-02 |
| ECOM-CHECKOUT-004-NFR-01 | Checkout latency | BG-02: Reduce cart abandonment via fast, reliable cart operations | ECOM-CHECKOUT-004-TC-03 |