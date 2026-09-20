# Spec: Async Order Processing Pipeline
**ID:** ECOM-ORDER-011
**Version:** 1.1
**Status:** Draft
**Traces to:** BG-02 (Reduce cart abandonment via fast, reliable cart operations), BG-05 (Prevent overselling of limited stock)

## User Story
As a shopper, I want my order to be reliably processed end-to-end — inventory reserved, payment captured, and confirmation sent — even when individual services are slow or temporarily unavailable, so that I get a correct outcome (confirmed or clearly failed) rather than a silently stuck or duplicated order.

## Scope
- **In scope:** the asynchronous pipeline that runs after an order is created (`ECOM-CHECKOUT-004`) and before it reaches a terminal state (`confirmed`, `failed`, or `canceled`): inventory reservation, payment capture, and downstream notification triggering.
- **Out of scope:** the checkout API itself (`ECOM-CHECKOUT-004`), payment gateway integration details (`ECOM-PAYMENT-005`), notification content/channel (`ECOM-NOTIFICATION-010`), shipment/fulfillment after `confirmed`.

## System Context / Dependencies
This spec coordinates 4 independent services via an event/message queue:
- **Order Service** — owns order state; publishes and consumes order lifecycle events.
- **Inventory Service** — reserves/releases stock (`ECOM-INVENTORY-009`).
- **Payment Service** — authorizes/captures/refunds payment (`ECOM-PAYMENT-005`).
- **Notification Service** — triggered on terminal states (`ECOM-NOTIFICATION-010`).

All inter-service calls in this pipeline are **asynchronous** (queue-based) and subject to retry. Every event carries an **idempotency key** equal to the order ID.

## Business Rules
- **BR-01:** Processing an order-placed event more than once with the same order ID shall not result in more than one inventory reservation or more than one payment capture (idempotency).
- **BR-02:** An order shall reach a terminal state (`confirmed` or `failed`) within 5 minutes of creation, or be flagged for manual review.
- **BR-03:** If payment succeeds but inventory reservation subsequently fails (or vice versa), the succeeding step shall be automatically compensated (refunded / released) rather than left in an inconsistent state.
- **BR-04:** If a `PaymentCaptured` event is received for an order already in the `failed` state (i.e., a late arrival after reconciliation gave up and released inventory), the payment shall be automatically refunded and the order flagged for manual reconciliation review — the order shall NOT be automatically re-confirmed, since its reserved inventory may no longer be available.

## Order State Machine
Every transition is triggered by a named event. `InventoryReservationFailed` and `PaymentDeclined` are introduced here as the explicit failure counterparts to `InventoryReserved` and `PaymentCaptured` (implied by earlier scenarios but not previously named).

```
pending_payment --[OrderPlaced]--> reserving_inventory

reserving_inventory --[InventoryReserved]--> awaiting_payment
reserving_inventory --[InventoryReservationFailed]--> failed

awaiting_payment --[PaymentCaptured]--> confirmed
awaiting_payment --[PaymentDeclined]--> payment_failed
awaiting_payment --[no PaymentCaptured/PaymentDeclined within 8s]--> payment_uncertain

payment_failed --[InventoryReleased (compensating action)]--> failed

payment_uncertain --[reconciliation: PaymentCaptured found]--> confirmed
payment_uncertain --[reconciliation: PaymentDeclined found, or 3 attempts exhausted]--> failed

failed --[late PaymentCaptured received after failure — see Scenario 9]--> reconciliation_review
```
*(Note: a late `PaymentCaptured` arriving for an order already `confirmed` is the duplicate-delivery case, already covered by Scenario 5 and BR-01 — no new transition needed there.)*

## Async Flow — Happy Path (numbered steps)
```
1. Order Service publishes OrderPlaced{order_id, idempotency_key}
2. Inventory Service consumes OrderPlaced, reserves stock, publishes InventoryReserved{order_id}
3. Order Service consumes InventoryReserved, transitions order to "awaiting_payment", publishes PaymentRequested{order_id}
4. Payment Service consumes PaymentRequested, captures payment, publishes PaymentCaptured{order_id}
5. Order Service consumes PaymentCaptured, transitions order to "confirmed", publishes OrderConfirmed{order_id}
6. Notification Service consumes OrderConfirmed, sends confirmation to customer
```

## Scenarios

### Happy path

**Scenario 1: Order processes successfully end-to-end**
```
GIVEN a newly placed order with sufficient stock available
WHEN the async pipeline processes OrderPlaced
THEN inventory shall be reserved
AND payment shall be captured
AND the order status shall transition to "confirmed"
AND exactly one confirmation notification shall be triggered
```
*(Timing is governed by NFR-01, not restated here — see Non-Functional Requirements.)*

### Failure paths

**Scenario 2: Inventory reservation fails (insufficient stock)**
```
GIVEN a newly placed order for a SKU with 0 units available
WHEN the pipeline attempts to reserve inventory
THEN the order status shall transition to "failed" with reason "insufficient_stock"
AND no payment shall be requested
AND a failure notification shall be triggered
```

**Scenario 3: Payment fails after inventory was reserved (compensating action)**
```
GIVEN an order with inventory successfully reserved
WHEN payment capture is declined
THEN the order status shall transition to "payment_failed" then "failed"
AND the previously reserved inventory shall be released within 10 seconds (compensating action)
AND a failure notification shall be triggered
```

**Scenario 4: Payment gateway times out (uncertain outcome)**
```
GIVEN an order with inventory successfully reserved
AND the Payment Service does not respond within 8 seconds
WHEN the timeout elapses
THEN the order status shall transition to "payment_uncertain"
AND a reconciliation job shall query the payment gateway's actual status within 30 seconds
AND if the reconciliation confirms payment succeeded, the order shall transition to "confirmed"
AND if the reconciliation confirms payment failed or is still unresolved after 3 reconciliation attempts (90 seconds total), the order shall transition to "failed" and reserved inventory shall be released
```

**Scenario 5: Duplicate OrderPlaced event delivery**
```
GIVEN an OrderPlaced event for order "o-4471" has already been fully processed to "confirmed"
WHEN a duplicate OrderPlaced event for "o-4471" is delivered (e.g., due to consumer retry)
THEN the Inventory Service shall recognize the idempotency key and shall NOT create a second reservation
AND the Payment Service shall recognize the idempotency key and shall NOT capture payment a second time
AND the order status shall remain "confirmed"
```

**Scenario 6: Out-of-order event delivery**
```
GIVEN a PaymentCaptured event for order "o-4471" is delivered
AND the corresponding InventoryReserved event for the same order has not yet been processed
WHEN the Order Service consumes PaymentCaptured out of sequence
THEN the Order Service shall hold the PaymentCaptured event in a pending state
AND shall re-evaluate it once InventoryReserved is received
AND shall not transition the order to "confirmed" based on an incomplete sequence
```

### Boundary conditions

**Scenario 7: Order reaches exactly the 5-minute terminal-state deadline**
```
GIVEN an order has been in a non-terminal state for exactly 5 minutes
WHEN the deadline check runs
THEN the order shall be flagged for manual review
AND an alert shall be raised to the operations queue
```

**Scenario 8: Reconciliation reaches exactly its 3rd attempt with no resolution**
```
GIVEN a payment_uncertain order has completed 2 reconciliation attempts with no resolution
WHEN the 3rd reconciliation attempt also returns no resolution
THEN the order shall transition to "failed"
AND reserved inventory shall be released
AND no further reconciliation attempts shall be made
```

**Scenario 9: Late payment confirmation arrives after order already marked failed**
```
GIVEN an order transitioned to "failed" after reconciliation exhausted 3 attempts (Scenario 8)
AND its reserved inventory has already been released
WHEN a PaymentCaptured event for that order arrives after the order reached "failed"
THEN the order shall transition to "reconciliation_review" (not automatically back to "confirmed")
AND the system shall automatically issue a refund for the captured payment
AND the order shall be flagged for manual review with reason "late_payment_after_failure"
AND no automatic re-reservation of inventory shall be attempted
```

## Non-Functional Requirements
- **NFR-01 (Latency):** End-to-end pipeline completion (OrderPlaced → terminal state) shall complete within 15 seconds at P50, 60 seconds at P95, and 5 minutes at P99, under normal load (up to 500 concurrent orders).
- **NFR-02 (Consistency window):** During processing, order status reads may reflect an intermediate state (e.g., "reserving_inventory") but shall never reflect a state more than 1 step stale relative to the last successfully processed event, measured at read time.
- **NFR-03 (Reliability):** The pipeline shall successfully reach a terminal state (without manual review) for 99.5% of orders, measured over 30 days.

## Traceability Table
| Requirement ID | Description | Business Goal | Related Test(s) |
|---|---|---|---|
| ECOM-ORDER-011-BR-01 | Idempotent processing | BG-05: Prevent overselling of limited stock | ECOM-ORDER-011-TC-01 |
| ECOM-ORDER-011-BR-02 | 5-minute terminal-state SLA | BG-02: Reduce cart abandonment via fast, reliable cart operations | ECOM-ORDER-011-TC-02 |
| ECOM-ORDER-011-BR-03 | Automatic compensation on partial failure | BG-05: Prevent overselling of limited stock | ECOM-ORDER-011-TC-03 |
| ECOM-ORDER-011-BR-04 | Late payment confirmation after failure handled (refund + manual review) | BG-05: Prevent overselling of limited stock | ECOM-ORDER-011-TC-04 |
| ECOM-ORDER-011-NFR-01 | Pipeline latency | BG-02: Reduce cart abandonment via fast, reliable cart operations | ECOM-ORDER-011-TC-05 |
| ECOM-ORDER-011-NFR-02 | Consistency window bound | BG-05: Prevent overselling of limited stock | ECOM-ORDER-011-TC-06 |
| ECOM-ORDER-011-NFR-03 | Pipeline success rate | BG-02: Reduce cart abandonment via fast, reliable cart operations | ECOM-ORDER-011-TC-07 |

## Open Questions
- Should the customer see a live "processing" state in the UI during the pipeline window, or only the terminal outcome? Affects whether NFR-02's consistency window is user-visible or purely internal.
- Scenario 4/8: is 3 reconciliation attempts the right number, or should it scale with the payment gateway's own documented worst-case response time? Flagged for engineering input before implementation.
- BR-04/Scenario 9 resolves the late-payment-after-failure case by defaulting to refund + manual review rather than automatic re-confirmation, on the grounds that inventory may have already sold out. Is automatic refund the right default, or should high-value orders route to manual review *before* refunding, to give a human the option to manually re-reserve stock if still available? Flagged for product input.

## Changelog
- **v1.0:** Initial draft.
- **v1.1 (this revision):** Removed NFR timing duplicated inside Scenario 1; named all state-machine transition events explicitly (introducing `InventoryReservationFailed` and `PaymentDeclined`); added BR-04 and Scenario 9 to resolve the previously-unhandled late-payment-after-failure case.