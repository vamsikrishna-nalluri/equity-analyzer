# Spec: Search Products
**ID:** ECOM-SEARCH-008
**Status:** Draft

## User Story
As a shopper, I want to search for products so I can find what I want to buy.

## Business Rules
- **BR-01:** Search query shall not exceed 100 characters.

## Scenarios

### Happy path
**Scenario 1: Search returns results**
```
GIVEN products exist matching the search term
WHEN the shopper searches for "blue shirt"
THEN matching products shall be returned
```

## Non-Functional Requirements
- **NFR-01 (Performance):** Search results should load quickly for a good user experience.