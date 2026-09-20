# Spec: Cache Stock Data

**ID:** CACHE-STOCK-F-001

**Status**: Draft

## User Story
As a user, I want cache the stock fundamentals to make the system faster.

## Scope
- In scope:
* Cache the data from market data provider

- Out of scope:
* cache technical details of a ticker.
* cache price history details of a ticker.

## Business Rules
- **BR-01:**
cache shall be consider invalid if 5 minutes or older.

## Scenarios

**Happy path:**
### Scenario 1: The ticker details available in the cache and valid
```
GIVEN the ticker information is available in the cache and valid
WHEN the user looks into the cache for the specified ticker.
THEN the system will return the detail from the cache
```

### Scenario 2: The ticker details is not available in the cache
```
GIVEN the ticker information is not available in the cache and valid
WHEN the user requests for fundamentals of a ticker.
THEN the system gets the data from market data provider
AND updates the cache
```

### Scenario 3: The ticker cache is available but expired
```
GIVEN The ticker cache is available and expired
WHEN the user request for fundamental details of a ticker
THEN the system shall get the fundamentals from market data provider
AND update the cache with new fundamental details
```

**Failure paths:**
### Scenario 4: Cache miss and market data provider unavailable
```
GIVEN the ticker is not present in the cache
AND the market data provider is temporarily unavailable
WHEN the user requests fundamentals for the ticker
THEN the system shall throw a `MarketDataUnavailableException` with message "Market data provider is temporarily unavailable."
AND the cache shall remain unchanged
```

## Boundary conditions
### Scenario 5: The ticker details available in the cache and valid
```
GIVEN the ticker information is available in the cache and exactly 5 minutes back.
WHEN the user looks into the cache for the specified ticker.
THEN the system shall call the market data provider
AND updates the cache with new fundamental details
```

## Non-Functional Requirements
- **NFR-01 (Performance):** Cache retrieval shall complete within 2ms at P50, 5ms at P95, and 15ms at P99, under normal load (up to 100 concurrent users).

- **NFR-02 (Reliability):** the ticker cache, shall be available 99.9% over 30 days.

## Tracebility Table
| Requirement ID | Description | Business Goal | Related Test(s) |
|---|---|---|---|
| CACHE-STOCK-F-001-BR-01 | cache invalid after 5 minutes | BG-01: key stock fundamentals without manual research | CACHE-STOCK-F-001-TC-01 |
| CACHE-STOCK-F-001-NFR-01 | get cache latency | BG-01: key stock fundamentals without manual research | CACHE-STOCK-F-001-TC-02 |
| CACHE-STOCK-F-001-NFR-02 | cache retrival reliability | BG-01: key stock fundamentals without manual research | CACHE-STOCK-F-001-TC-08 |
| CACHE-STOCK-F-001-FR-01 | get ticker fundamental details from cache | BG-01: key stock fundamentals without manual research | CACHE-STOCK-F-001-TC-03 |
| CACHE-STOCK-F-001-FR-02 | get ticker fundamental details where cache is not available | BG-01: key stock fundamentals without manual research | CACHE-STOCK-F-001-TC-04 |
| CACHE-STOCK-F-001-FR-03 | get ticker fundamental details where cache is expired| BG-01: key stock fundamentals without manual research | CACHE-STOCK-F-001-TC-05|
| CACHE-STOCK-F-001-FR-04 | get ticker fundamental details cache is not available and market data provider is unavailable| BG-01: key stock fundamentals without manual research | CACHE-STOCK-F-001-TC-06|
| CACHE-STOCK-F-001-FR-05 | get ticker fundamental details from market data provide after exactly 5 minutes of cache entry| BG-01: key stock fundamentals without manual research | CACHE-STOCK-F-001-TC-07|

## Open Question:
* yet to be decided on wether the system should include the information about the source of the fundamental details like source: "cache" or source: "provider"

