# Spec: Add Item to Cart
**ID:** ECOM-CART-001
**Status:** Draft

## User Story
As a shopper, I want to add a product to my cart, so that I can purchase it later.

## Scope
- In scope: adding a product (by SKU) and quantity to the active cart.
- Out of scope: checkout, payment, inventory reservation.

## Business Rules
- **BR-01:** Quantity shall be a positive integer between 1 and 50 (inclusive).
- **BR-02:** SKU shall exist in the product catalog.

## Example I/O
Input:
```json
{ "sku": "TSHIRT-BLU-M", "quantity": 2 }
```
Output (success, 200):
```json
{ "cart_id": "c-9821", "sku": "TSHIRT-BLU-M", "quantity": 2, "line_total": 39.98 }
```
Output (failure, 400):
```json
{ "error": "quantity must be between 1 and 50", "code": 400 }
```

## Scenarios

### Happy path
**Scenario 1: Successfully adding an item**
```
GIVEN the cart is empty
WHEN the shopper adds SKU "TSHIRT-BLU-M" with quantity 2
THEN the cart shall contain 1 line item for "TSHIRT-BLU-M" with quantity 2
```

### Failure paths
**Scenario 2: SKU does not exist**
```
GIVEN a SKU "INVALID-SKU-999" that does not exist in the catalog
WHEN the shopper attempts to add it to the cart
THEN the system shall return error "SKU not found" with code 404
AND no line item shall be added
```

### Boundary conditions
**Scenario 3: Quantity at maximum (50)**
```
GIVEN a valid SKU
WHEN the shopper adds quantity 50
THEN the item shall be added successfully
```
**Scenario 4: Quantity above maximum (51)**
```
GIVEN a valid SKU
WHEN the shopper adds quantity 51
THEN the system shall return error "quantity must be between 1 and 50" with code 400
AND no line item shall be added
```

## Non-Functional Requirements
- **NFR-01 (Performance):** Add-to-cart shall complete within 200ms at P95, under normal load (up to 200 concurrent users).

## Traceability Table
| Requirement ID | Description | Business Goal | Related Test(s) |
|---|---|---|---|
| ECOM-CART-001-BR-01 | Quantity 1-50 | BG-02: Reduce cart abandonment via fast, reliable cart operations | ECOM-CART-001-TC-01 |
| ECOM-CART-001-BR-02 | SKU must exist | BG-02: Reduce cart abandonment via fast, reliable cart operations | ECOM-CART-001-TC-02 |
| ECOM-CART-001-NFR-01 | Add-to-cart latency | BG-02: Reduce cart abandonment via fast, reliable cart operations | ECOM-CART-001-TC-03 |