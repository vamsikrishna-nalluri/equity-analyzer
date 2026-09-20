# PR: Advanced-standard specs for Stock Fundamentals feature set

**Branch:** `specs/stock-fundamentals-advanced`
**Files changed:**
- `01-get-stock-fundamentals.md` (new)
- `02-handle-invalid-ticker-input.md` (new — marked superseded)
- `03-cache-stock-data.md` (new)
- `traceability-table.md` (new)

## Summary
Rewrites 3 under-specified drafts to advanced standard: full scenario coverage (happy/failure/boundary), measurable NFRs with percentiles, unique traceability IDs linked to BG-01, and AI-readable structure (Example I/O blocks, consistent terminology).

---

## Review Comments

### Comment 1 — RESOLVED
**File:** `03-cache-stock-data.md`, Scenario 5 (boundary)
**Reviewer comment:**
> Location: BR-01 vs. Scenario 5. Quality attribute: internal consistency / testability. BR-01 originally read "invalid if older than 5 minutes" (exclusive), but Scenario 5 treated an entry at exactly 5 minutes as expired — these contradict each other. Please make the rule text and the boundary scenario agree on whether 5:00 exactly is valid or expired.

**Resolution:** BR-01 updated to "5 minutes or older" (inclusive), and Scenario 5 confirmed to treat exactly-5-minute entries as expired. Rule and scenario now consistent.

---

### Comment 2 — RESOLVED
**File:** `01-get-stock-fundamentals.md`, Scenario 2 (originally)
**Reviewer comment:**
> Location: Scenario 2 GIVEN. Quality attribute: testability. GIVEN is identical to Scenario 1's GIVEN, but the two scenarios produce different outcomes (success vs. exception) with no distinguishing condition stated. Please add the condition that actually triggers the failure.

**Resolution:** Added `AND the market data provider is temporarily unavailable` to Scenario 2's GIVEN, disambiguating it from the happy path.

---

### Comment 3 — RESOLVED
**File:** `02-handle-invalid-ticker-input.md`
**Reviewer comment:**
> This spec's business rules (empty ticker, restricted characters) fully duplicate GET-STOCK-F-001-BR-01 and BR-02. Duplicated rules across specs risk drifting out of sync over time. Recommend merging or explicitly marking superseded.

**Resolution:** Spec marked `Status: Superseded`, with a review note explaining the decision and the condition under which it should be revisited (a second ticker-consuming operation being introduced).

---

## Outstanding Open Questions (not blocking merge)
- `CACHE-STOCK-F-001`: should API responses indicate data source (`cache` vs. `provider`)? Flagged for product/engineering discussion.

## Reviewer sign-off
All blocking comments resolved. Approved for merge.