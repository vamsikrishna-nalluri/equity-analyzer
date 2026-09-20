# Spec: Apply Discount Code
**ID:** ECOM-PROMO-003
**Status:** Draft

## User Story
As a shopper, I want to apply a discount code to my order so I can save money.

## Business Rules
- **BR-01:** Discount code must be valid and not expired.
- **BR-02:** Product ID must exist in the catalog for the discount to apply.
- **BR-03:** Discount code shall not reduce the order total below zero.

## Scenarios

### Happy path
**Scenario 1: Valid discount code applied**
```
GIVEN a cart with a subtotal of $100
WHEN the shopper applies discount code "SAVE10"
THEN the order total shall be reduced by 10%
```

### Failure paths
**Scenario 2: Expired discount code**
```
GIVEN a discount code that has expired
WHEN the shopper applies the code
THEN the system shall display "This discount code has expired"
AND the order total shall remain unchanged
```

## Traceability Table
| Requirement ID | Description | Business Goal | Related Test(s) |
|---|---|---|---|
| ECOM-PROMO-003-BR-01 | Code valid/not expired | BG-03 | TC-01 |
| ECOM-PROMO-003-BR-02 | Product ID exists | BG-03 | TC-01 |