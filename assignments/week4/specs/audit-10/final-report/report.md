# Spec Corpus Audit Report — E-Commerce Platform (10 specs)
**Auditor:** [Your name]
**Date:** 2026-09-20
**Scope:** Cart, Checkout, Payment, Inventory, Order, Search, Notification specs

---

## 1. Scoring Summary

Scale: 0 (absent) — 5 (fully meets advanced standard)

| # | Spec ID | Completeness | Testability | Traceability | AI-Parsability | Notes |
|---|---|---|---|---|---|---|
| 01 | ECOM-CART-001 | 5 | 5 | 5 | 5 | Meets advanced standard in full. |
| 02 | CART-REMOVE-2 | 1 | 1 | 0 | 0 | No scope, no BRs, no boundary/failure scenarios, no NFR, no traceability. |
| 03 | ECOM-PROMO-003 | 3 | 5 | 4 | 5 | No NFR section; traceability rows reuse the same test ID (TC-01) for two distinct rules. |
| 04 | ECOM-CHECKOUT-004 | 4 | 5 | 3 | 5 | Strong overall; traceability slightly under-detailed relative to scenario count. |
| 05 | ECOM-PAYMENT-005 | 2 | 1 | 0 | 3 | Only happy path present — no failure scenarios (declined card, double-charge, gateway timeout). NFR unmeasurable ("should be reliable"). Names a specific vendor (Stripe) — implementation leakage. |
| 06 | ORDER-CANCEL-06 | 2 | 1 | 0 | 1 | No user story, no scope, no NFR, no traceability. Actor missing in "Order canceled" scenario (who/what triggers cancellation is unstated). |
| 07 | ECOM-ORDER-007 | 4 | 4 | 5 | 4 | Solid; missing boundary scenarios; NFR lacks percentile/load condition; spec ID domain segment ("ORDER") doesn't reflect the feature ("shipping address"). |
| 08 | ECOM-SEARCH-008 | 3 | 4 | 0 | 4 | No scope, no failure paths, vague NFR ("should load quickly"), no traceability table at all. |
| 09 | ECOM-INVENTORY-009 | 4 | 5 | 5 | 5 | Strong overall; missing boundary scenarios (e.g., reserving exactly the last unit in stock). |
| 10 | notif_order_status_v1 | 0 | 0 | 0 | 0 | No scope, no BRs, no NFR, no traceability, no example I/O. Notification trigger/actor and delivery channel entirely unspecified. ID does not follow corpus convention. |

**Corpus average (out of 5):** Completeness 2.8 | Testability 3.1 | Traceability 2.2 | AI-Parsability 3.2

---

## 2. Per-Spec Findings

### 02 — Remove Item from Cart
- Vague verb: "handle cases... properly" (no observable outcome).
- No scenario categories beyond a single unlabeled happy path.
- No NFR, no traceability table, no Example I/O.

### 03 — Apply Discount Code
- Traceability rows for BR-01 and BR-02 both point to `TC-01` — duplicate test ID reuse; each rule needs its own test reference.
- No NFR section at all.

### 05 — Process Payment
- **Implementation leakage:** "shall charge the customer's card using Stripe" names a specific vendor; should state the business requirement (e.g., "shall charge the customer's payment method") independent of provider.
- **Missing failure paths:** no scenarios for declined payment, gateway timeout, or double-charge prevention — despite a requirement ("shall not double-charge") that has no corresponding test scenario at all.
- **Unmeasurable NFR:** "Payment processing should be reliable" has no percentile, threshold, or measurement window.

### 06 — Cancel Order
- Missing User Story and Scope sections entirely.
- **Missing actor:** "Order canceled" scenario's WHEN ("cancellation happens") doesn't state who/what triggers it — customer action, CS agent, automated timeout?
- No NFR, no traceability table.

### 07 — Update Shipping Address
- Spec ID domain segment is `ORDER` but the feature is specifically shipping-address management — inconsistent with the corpus's otherwise feature-specific domain naming (e.g., `CART`, `PROMO`, `SEARCH`).
- No boundary scenario (e.g., postal code at exact format-length limits).
- NFR-01 has no percentile breakdown or load condition, unlike comparable specs (01, 04, 09).

### 08 — Search Products
- Missing Scope section.
- No failure-path scenarios (e.g., query exceeding 100 characters, defined in BR-01 but never tested).
- Unmeasurable NFR: "should load quickly for a good user experience."
- No Traceability Table at all — BR-01 and NFR-01 are both untraced.

### 10 — Order Status Notification
- Most severe gaps in the corpus: no Scope, no Business Rules (beyond one misplaced rule — see cross-spec finding below), no NFR, no Traceability Table, no Example I/O.
- Scenario's WHEN ("the change happens") doesn't specify what triggers an order status change or who/what initiates it.
- No specification of notification channel (email? SMS? push?) or content — "a notification shall be sent" is untestable as written.

---

## 3. Cross-Spec Findings

| Finding | Type | Specs Affected |
|---|---|---|
| Inconsistent ID naming convention — `ECOM-<DOMAIN>-<NNN>` vs. ad hoc formats | Taxonomy | 02, 06, 10 (vs. the convention followed by 01, 03, 04, 07, 08, 09) |
| Terminology drift — "SKU" vs. "Product ID" used for the same catalog concept, never reconciled | AI-parsability / glossary gap | 01, 04 (SKU) vs. 03, 09 (Product ID) |
| Duplicate business rule text across unrelated specs — "Cancellation shall not reduce the order total below zero" appears verbatim in both the owning spec and an unrelated spec | Redundancy / ownership boundary | 06 (correct owner) and 10 (should not own this rule) |
| Domain-segment mismatch in spec ID vs. actual feature scope | Taxonomy | 07 (`ORDER` segment used for a shipping-address feature) |

---

## 4. Recommendations, Prioritized

1. **Urgent rework (blocking):** Specs `10` and `06` — both missing nearly every required section; `10` in particular cannot be implemented as written (notification channel and trigger are unspecified).
2. **High priority:** Spec `05` — remove vendor-specific implementation detail, add failure-path scenarios for the payment flow (this is a financial-transaction spec; missing failure coverage carries real production risk), and quantify the reliability NFR.
3. **Medium priority:** Spec `08` — add scope, failure paths, and a traceability table; spec `02` — full rewrite required (currently below minimum viable standard).
4. **Minor polish:** Specs `03`, `04`, `07`, `09` — each is fundamentally sound; fixes are localized (duplicate test IDs, missing boundary scenarios, NFR percentile detail).
5. **Org-level action (not spec-specific):** Publish a taxonomy/style guide (naming convention + shared glossary defining "SKU" as the single canonical term) so findings 1–3 in the cross-spec table don't recur in future specs. This is a process fix, not a per-spec fix — see accompanying Spec Taxonomy document.

---

## 5. Corpus-Wide Quality Verdict
3 of 10 specs (01, 04, 09) meet or nearly meet advanced standard. 4 of 10 (03, 07, 08, and marginally 05) are workable with targeted fixes. 3 of 10 (02, 06, 10) require substantial rework before implementation should begin. The corpus's most systemic issue is not any single spec's content, but the **lack of an enforced taxonomy and shared glossary**, which produced the naming and terminology drift found above — recommend addressing this at the process level before continuing to scale the corpus.