# Spec: Update Shipping Address
**ID:** ECOM-ORDER-007
**Status:** Draft

## User Story
As a shopper, I want to update my shipping address before my order ships, so that my order arrives at the correct location.

## Scope
- In scope: updating the shipping address on an order that has not yet shipped.
- Out of scope: updating billing address, updating address after shipment.

## Business Rules
- **BR-01:** Shipping address shall only be editable while order status is "pending_payment" or "confirmed" (not "shipped" or "delivered").
- **BR-02:** Postal code shall match the format expected for the selected country.

## Scenarios

### Happy path
**Scenario 1: Successfully updating shipping address**
```
GIVEN an order with status "confirmed"
WHEN the shopper updates the shipping address with a valid address
THEN the order's shipping address shall be updated
```

### Failure paths
**Scenario 2: Attempting to update after shipment**
```
GIVEN an order with status "shipped"
WHEN the shopper attempts to update the shipping address
THEN the system shall return error "Address cannot be changed after shipment" with code 409
AND the address shall remain unchanged
```

## Non-Functional Requirements
- **NFR-01 (Performance):** Address update shall complete within 300ms at P95.

## Traceability Table
| Requirement ID | Description | Business Goal | Related Test(s) |
|---|---|---|---|
| ECOM-ORDER-007-BR-01 | Editable only pre-shipment | BG-04: Reduce failed deliveries due to incorrect addresses | ECOM-ORDER-007-TC-01 |
| ECOM-ORDER-007-BR-02 | Postal code format | BG-04: Reduce failed deliveries due to incorrect addresses | ECOM-ORDER-007-TC-02 |
| ECOM-ORDER-007-NFR-01 | Update latency | BG-04: Reduce failed deliveries due to incorrect addresses | ECOM-ORDER-007-TC-03 |