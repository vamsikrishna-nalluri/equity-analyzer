# Spec: Cache Stock Data

**ID:** MKTDATA-CACHE-STOCK-F-001
**Status:** Draft
**Traces to:** BG-01

## User Story
As a user, I want stock fundamentals to be cached so that repeated requests are faster.

## Scope
- **In scope:**
  - Cache fundamental data retrieved from the market data provider
- **Out of scope:**
  - Cache technical details of a ticker
  - Cache price history details of a ticker

## Business Rules
- **BR-01:** Cache entries shall be considered invalid if 5 minutes or older.

## Example I/O

**Input:**
```json
{ "ticker": "LT.NS" }
```

**Output (success — served from cache or provider; see Open Questions re: source indicator):**
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

## Scenarios

### Happy path

**Scenario 1: Ticker details available in cache and valid**
```
GIVEN the ticker information is available in the cache and valid
WHEN the user requests fundamentals for the specified ticker
THEN the system shall return the details from the cache
```

**Scenario 2: Ticker details not available in cache**
```
GIVEN the ticker information is not available in the cache
WHEN the user requests fundamentals for the ticker
THEN the system shall get the data from the market data provider
AND update the cache with the retrieved data
```

**Scenario 3: Ticker cache available but expired**
```
GIVEN the ticker cache entry is available and expired
WHEN the user requests fundamental details for the ticker
THEN the system shall get the fundamentals from the market data provider
AND update the cache with the new fundamental details
```

### Failure paths

**Scenario 4: Cache miss and market data provider unavailable**
```
GIVEN the ticker is not present in the cache
AND the market data provider is temporarily unavailable
WHEN the user requests fundamentals for the ticker
THEN the system shall throw a MarketDataUnavailableException with message "Market data provider is temporarily unavailable."
AND the cache shall remain unchanged
```

### Boundary conditions

**Scenario 5: Cache entry exactly 5 minutes old**
```
GIVEN the ticker information is available in the cache and exactly 5 minutes old
WHEN the user requests fundamentals for the specified ticker
THEN the system shall treat the cache entry as expired
AND the system shall get the fundamentals from the market data provider
AND update the cache with the new fundamental details
```

## Non-Functional Requirements
- **NFR-01 (Performance):** Cache retrieval shall complete within 2ms at P50, 5ms at P95, and 15ms at P99, under normal load (up to 100 concurrent users).
- **NFR-02 (Reliability):** The cache shall be available 99.9% over 30 days.

## Traceability Table
| Requirement ID | Description | Business Goal | Related Test(s) |
|---|---|---|---|
| MKTDATA-CACHE-STOCK-F-001-FR-01 | Get fundamentals from cache | BG-01: Enable users to make faster, more informed investment decisions by providing key stock fundamentals without manual research across multiple sources | MKTDATA-CACHE-STOCK-F-001-TC-01 |
| MKTDATA-CACHE-STOCK-F-001-FR-02 | Get fundamentals when cache is not available | BG-01: Enable users to make faster, more informed investment decisions by providing key stock fundamentals without manual research across multiple sources | MKTDATA-CACHE-STOCK-F-001-TC-02 |
| MKTDATA-CACHE-STOCK-F-001-FR-03 | Get fundamentals when cache is expired | BG-01: Enable users to make faster, more informed investment decisions by providing key stock fundamentals without manual research across multiple sources | MKTDATA-CACHE-STOCK-F-001-TC-03 |
| MKTDATA-CACHE-STOCK-F-001-FR-04 | Get fundamentals when cache is empty and provider unavailable | BG-01: Enable users to make faster, more informed investment decisions by providing key stock fundamentals without manual research across multiple sources | MKTDATA-CACHE-STOCK-F-001-TC-04 |
| MKTDATA-CACHE-STOCK-F-001-BR-01 | Cache invalid at 5 minutes or older (boundary) | BG-01: Enable users to make faster, more informed investment decisions by providing key stock fundamentals without manual research across multiple sources | MKTDATA-CACHE-STOCK-F-001-TC-05 |
| MKTDATA-CACHE-STOCK-F-001-NFR-01 | Cache retrieval latency | BG-01: Enable users to make faster, more informed investment decisions by providing key stock fundamentals without manual research across multiple sources | MKTDATA-CACHE-STOCK-F-001-TC-06 |
| MKTDATA-CACHE-STOCK-F-001-NFR-02 | Cache availability/reliability | BG-01: Enable users to make faster, more informed investment decisions by providing key stock fundamentals without manual research across multiple sources | MKTDATA-CACHE-STOCK-F-001-TC-07 |

## Open Questions
- Should the response include an indicator of data source (e.g., `"source": "cache"` vs. `"source": "provider"`)? Not yet decided — flagged for product/engineering discussion before implementation.