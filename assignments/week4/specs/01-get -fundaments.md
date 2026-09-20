# Spec: Get Stock Fundamentals

**ID:** GET-STOCK-F-001
**Status:** Draft
**Traces to:** BG-01

## User Story
As a user, I want to get stock fundamentals so I can make better investment decisions.

## Scope
- **In scope:**
  - Get fundamental details of a ticker
- **Out of scope:**
  - Get technical details of a ticker
  - Get price history details of a ticker

## Business Rules
- **BR-01:** Ticker shall not be empty or whitespace-only.
- **BR-02:** Ticker shall not contain `<` or `>` characters.

## Example I/O

**Input:**
```json
{ "ticker": "LT.NS" }
```

**Output (success):**
```json
{
  "price": 3500.25,
  "market_cap": 4850000000000,
  "pe_ratio": 28.4,
  "eps": 123.5,
  "dividend_yield": 0.012,
  "fifty_two_week_high": 3800.0,
  "fifty_two_week_low": 2900.0
}
```

**Output (failure — see Scenarios 2–4 for exact error shapes)**

## Scenarios

### Happy path

**Scenario 1: Successfully get the stock fundamentals**
```
GIVEN the ticker is a valid value
WHEN the user requests fundamentals for a valid ticker
THEN the system shall return the following fundamental details: price, market_cap, pe_ratio, eps, dividend_yield, fifty_two_week_high, fifty_two_week_low
```

### Failure paths

**Scenario 2: Market data provider unavailable**
```
GIVEN the ticker is a valid value
AND the market data provider is temporarily unavailable
WHEN the user requests fundamentals for a valid ticker
THEN the system shall throw a MarketDataUnavailableException with message "Market data provider is temporarily unavailable."
```

**Scenario 3: Empty ticker**
```
GIVEN the ticker is an empty value or whitespace
WHEN the user requests fundamentals for the ticker
THEN the system shall throw an InvalidTickerException with message "Ticker should not be empty."
```

**Scenario 4: Invalid ticker — contains restricted characters**
```
GIVEN the ticker contains "<" or ">"
WHEN the user requests fundamentals for the ticker
THEN the system shall throw an InvalidTickerException with message "Ticker must not contain '<' or '>' characters."
```

## Non-Functional Requirements
- **NFR-01 (Performance):** Get fundamentals shall complete within 500ms on a standard broadband connection (>10 Mbps).
- **NFR-02 (Reliability):** Get fundamentals shall be available 99.9% over 30 days.

## Traceability Table
| Requirement ID | Description | Business Goal | Related Test(s) |
|---|---|---|---|
| GET-STOCK-F-001-FR-01 | Get fundamentals with valid ticker | BG-01: Enable users to make faster, more informed investment decisions by providing key stock fundamentals without manual research across multiple sources | GET-STOCK-F-001-TC-01 |
| GET-STOCK-F-001-FR-02 | Market data provider unavailable | BG-01: Enable users to make faster, more informed investment decisions by providing key stock fundamentals without manual research across multiple sources | GET-STOCK-F-001-TC-02 |
| GET-STOCK-F-001-BR-01 | Empty ticker rejected | BG-01: Enable users to make faster, more informed investment decisions by providing key stock fundamentals without manual research across multiple sources | GET-STOCK-F-001-TC-03 |
| GET-STOCK-F-001-BR-02 | No `<`/`>` characters in ticker | BG-01: Enable users to make faster, more informed investment decisions by providing key stock fundamentals without manual research across multiple sources | GET-STOCK-F-001-TC-04 |
| GET-STOCK-F-001-NFR-01 | Fundamentals retrieval latency | BG-01: Enable users to make faster, more informed investment decisions by providing key stock fundamentals without manual research across multiple sources | GET-STOCK-F-001-TC-05 |
| GET-STOCK-F-001-NFR-02 | Fundamentals retrieval reliability | BG-01: Enable users to make faster, more informed investment decisions by providing key stock fundamentals without manual research across multiple sources | GET-STOCK-F-001-TC-06 |

## Open Questions
- None currently outstanding for this spec.