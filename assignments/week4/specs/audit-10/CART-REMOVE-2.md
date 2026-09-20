# Spec: Remove Item from Cart
**ID:** CART-REMOVE-2

## Requirements
- The system shall let the user remove an item from the cart.
- The system should handle cases where the item isn't there properly.
- Removal should update the cart total.

## Scenario
GIVEN a cart with items
WHEN the user removes an item
THEN the item shall be removed and the total updated