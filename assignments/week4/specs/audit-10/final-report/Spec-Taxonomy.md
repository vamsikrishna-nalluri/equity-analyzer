# Spec Taxonomy — E-Commerce Platform

**Status:** Proposed
**Owner:** Spec Standards Working Group
**Motivation:** Corpus audit (see `audit-report.md`) found 3 cross-spec issues — inconsistent ID naming (3 of 10 specs), terminology drift ("SKU" vs. "Product ID"), and a domain-segment mismatch — none of which could have been caught by reviewing any single spec in isolation. This taxonomy exists to prevent recurrence.

---

## 1. Naming Convention

**Format:**
```
ECOM-<DOMAIN>-<NNN>
```
- `ECOM` — fixed top-level platform prefix (all specs in this corpus).
- `<DOMAIN>` — uppercase, single word or hyphenless compound, naming the **feature area**, not the parent business object. (This directly fixes the `07` finding, where `ORDER` was used for a shipping-address feature — the domain segment must match the feature itself, e.g. `SHIPPING`, not the object it happens to modify.)
- `<NNN>` — sequential, zero-padded to 3 digits. Never reused, even if a spec is retired/superseded.

**Approved domains for this platform:**
| Domain | Covers |
|---|---|
| `CART` | Cart contents: add, remove, update quantity |
| `PROMO` | Discounts, coupon codes |
| `CHECKOUT` | Cart-to-order conversion |
| `PAYMENT` | Payment authorization, capture, refund |
| `ORDER` | Order lifecycle state (status transitions, cancellation) |
| `SHIPPING` | Shipping address, delivery method, tracking |
| `SEARCH` | Product search and discovery |
| `INVENTORY` | Stock levels, reservation, restocking |
| `NOTIFICATION` | Customer-facing notifications (any channel) |

Requirement/test sub-IDs follow: `<SPEC-ID>-<TYPE>-<NN>`, where `<TYPE>` ∈ `{BR, FR, NFR, TC}` (established in Level 2). Example: `ECOM-SHIPPING-007-BR-01`.

**Remediation for existing corpus:**
| Current ID | Corrected ID |
|---|---|
| `CART-REMOVE-2` | `ECOM-CART-002` |
| `ORDER-CANCEL-06` | `ECOM-ORDER-006` |
| `notif_order_status_v1` | `ECOM-NOTIFICATION-010` |
| `ECOM-ORDER-007` (shipping address) | `ECOM-SHIPPING-007` |

---

## 2. Versioning Scheme

Every spec carries:
```markdown
**Version:** 1.0
**Status:** Draft | Approved | Implemented | Deprecated | Superseded
**Last Updated:** YYYY-MM-DD
```
- **Major version** (1.0 → 2.0): a breaking change to the contract (e.g., a business rule's threshold changes, a field is removed from the Example I/O).
- **Minor version** (1.0 → 1.1): a clarification or additive change that doesn't alter existing behavior (e.g., adding a boundary scenario that was previously an unstated gap).
- A **Changelog** section at the bottom of each spec records what changed and why, at each version bump.
- IDs are immutable regardless of version or status — a `Superseded` spec keeps its original ID permanently (as demonstrated with `INVALID-TICKER-002` in the prior corpus), so historical references never break.

---

## 3. Folder Hierarchy

```
/specs
  /cart
    ECOM-CART-001.md
    ECOM-CART-002.md
  /promo
    ECOM-PROMO-003.md
  /checkout
    ECOM-CHECKOUT-004.md
  /payment
    ECOM-PAYMENT-005.md
  /order
    ECOM-ORDER-006.md
  /shipping
    ECOM-SHIPPING-007.md
  /search
    ECOM-SEARCH-008.md
  /inventory
    ECOM-INVENTORY-009.md
  /notification
    ECOM-NOTIFICATION-010.md
  /shared
    /glossary
      glossary.md
    /validation
      (future shared-rule specs go here once a rule has 2+ consumers)
  /memory
    constitution.md
```

Folder names are lowercase versions of the domain segment, so navigation between the ID and the file path is always predictable without needing a lookup table.

---

## 4. Shared Glossary (resolves the SKU / Product ID drift)

A `glossary.md` file in `/shared/glossary/` is the single source of truth for terms used across specs. Every spec must use the glossary term verbatim — no synonyms.

| Canonical Term | Definition | Do not use instead |
|---|---|---|
| **SKU** | The unique catalog identifier for a purchasable product variant (e.g., size/color combination). | "Product ID", "item code", "product code" |
| **Order** | A confirmed, checked-out purchase, from checkout through delivery or cancellation. | "Purchase", "transaction" (reserve for payment-specific contexts only) |
| **Reservation** | A temporary hold on inventory tied to an order pending payment completion. | "Lock", "hold" |

**Remediation for existing corpus:** Specs `03` (`ECOM-PROMO-003`) and `09` (`ECOM-INVENTORY-009`) currently use "Product ID" — both should be updated to "SKU" to align with `01` and `04`, and the glossary entry above should be treated as binding going forward.

---

## 5. Enforcement

Per Level 3, Topic 5 — this taxonomy is only durable if it's enforced mechanically, not just documented:
- The naming-convention regex (`^ECOM-[A-Z]+-\d{3}$`) becomes a lint rule (see `lint-rules.md`), run against every new or modified spec before merge.
- The glossary becomes part of `memory/constitution.md`, so `/speckit-specify` generates new specs using canonical terms by default rather than requiring manual correction after the fact.