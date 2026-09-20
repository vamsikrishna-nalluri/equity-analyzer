# Spec: Cancel Order
**ID:** ORDER-CANCEL-06

## Business Rules
- BR-1: Order shall not be canceled if it has already shipped.
- BR-2: Cancellation shall not reduce the order total below zero.

## Scenarios

### Scenario: Order canceled
```
GIVEN an order exists
WHEN cancellation happens
THEN the order status shall be updated to "canceled"
AND a refund shall be issued
```

### Scenario: Already shipped
```
GIVEN an order has shipped
WHEN cancellation is attempted
THEN it shall not be allowed
```