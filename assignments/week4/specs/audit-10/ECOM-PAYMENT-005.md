# Spec: Process Payment
**ID:** ECOM-PAYMENT-005
**Status:** Draft

## User Story
As a shopper, I want my payment to be processed so my order can be confirmed.

## Requirements
- The system shall charge the customer's card using Stripe.
- Payment failures should be handled properly.
- The system shall not double-charge the customer.

## Scenarios

### Happy path
**Scenario 1: Payment succeeds**
```
GIVEN an order in status "pending_payment"
WHEN payment is processed
THEN the order status shall become "confirmed"
```

## NFR
- Payment processing should be reliable.