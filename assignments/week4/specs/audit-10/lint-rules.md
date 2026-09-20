# Custom Lint Rules — E-Commerce Spec Corpus

Two rules, derived directly from anti-patterns found during this project's audits and reviews.
Format: rule name, machine-checkable condition (pattern or check), and the message shown to the author on violation.

---

## Rule 1: Traceability Table Required

```yaml
- rule: traceability-table-required
  applies_to: "every spec file (*.md) under /specs"
  check: "document must contain a '## Traceability Table' heading, and every BR/FR/NFR ID declared elsewhere in the document must appear as a row in that table"
  severity: error
  message: >
    Spec is missing a Traceability Table, or contains requirement IDs
    with no corresponding traceability row. Every requirement must trace
    to a business goal and a unique test ID (see spec-taxonomy.md).
  origin: >
    Found in spec 08 (Search Products) — no traceability table at all —
    and spec 10 (Order Status Notification) — same gap, more severe.
```

## Rule 2: No Vague Verbs in Requirements or Scenarios

```yaml
- rule: no-vague-verbs
  applies_to: "every spec file (*.md) under /specs"
  pattern: "\\b(handle|manage|process|support|optimize|improve)\\b|\\b(properly|appropriately|correctly)\\b"
  scope: "Business Rules, Functional Requirements, and Scenario GIVEN/WHEN/THEN lines"
  severity: error
  message: >
    Requirement or scenario contains a vague verb/adverb with no
    observable, testable outcome. Rewrite with a specific, measurable
    action (e.g., replace "handle errors properly" with the exact
    error condition and response).
  origin: >
    Found in spec 02 (Remove Item from Cart) — "handle cases... properly" —
    and spec 05 (Process Payment) — "Payment failures should be handled properly."
```

---

## Notes on Enforcement
Both rules are intended to run as part of a pre-merge check (e.g., a CI step invoked before a spec PR can be approved), and conceptually map to what a Spec-Kit `/speckit.checklist` pass would generate and verify automatically once the project's `memory/constitution.md` encodes these same standards (see spec-taxonomy.md, Section 5).

A third candidate rule — enforcing the `ECOM-<DOMAIN>-<NNN>` ID naming convention — is already defined in `spec-taxonomy.md` (Section 5) and is included there rather than duplicated here, to avoid the same duplicate-rule-across-documents anti-pattern this corpus's audit flagged elsewhere.