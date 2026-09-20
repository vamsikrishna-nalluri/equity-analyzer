# Spec: Order Status Notification
**ID:** notif_order_status_v1

## Requirements
- The customer shall be notified when their order status changes.
- If an order is canceled, a refund shall be issued and shall not reduce the order total below zero.
- Notifications shall be sent in a timely manner.

## Scenario
GIVEN an order status changes
WHEN the change happens
THEN a notification shall be sent