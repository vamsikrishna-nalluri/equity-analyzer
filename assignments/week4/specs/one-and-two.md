# Spec: Get Stock Fundamentals

**ID:** GET-STOCK-F-001

**Status**: Draft

## User Story
As a user, I want to get stock fundamentals so I can make better investment decisions.

## Scope
- In scope:
* Get fundamental details of a ticker

- Out of scope:
* Get technical details of a ticker.

* Get price details of a ticker

## Business Rules
- **BR-01:**
ticker name shall not be empty
- **BR-02:**
ticker name shall not allow `>` or `<`

## Example I/O
Input:
ticker Name: LT.NS

Ouput:
return {
    "price": info.get("regularMarketPrice"),
    "market_cap": info.get("marketCap"),
    "pe_ratio": info.get("trailingPE"),
    "eps": info.get("trailingEps"),
    "dividend_yield": info.get("dividendYield"),
    "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
    "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
}


## Scenarios

**Happy path:**
### Scenario 1: Successfully get the stock details
```
GIVEN the ticker a valid value
WHEN the user requests for fundamentals of a valid ticker.
THEN the system shall return the following fundamental details: price, market_cap, pe_ratio, eps, dividend_yield, fifty_two_week_high, fifty_two_week_low.
```

**Failure paths:**
### Scenario 2: Unable to get the fundamental details and market data provider is unvailable
```
GIVEN the ticker is a valid value and market data provide is unavailable
WHEN the user requests for fundamentals of a valid ticker.
THEN the system shall throw an exception `MarketDataUnavailableException` with message `Market data provider is temporarily unavailable.`
```

### Scenario 3: Unable to get the fundamental details and empty ticker
```
GIVEN the ticker is empty value or whitespaces
WHEN the user requests for fundamentals of the ticker.
THEN the system shall throw an exception `InValidTickerException` with message `Ticker should not be empty.`
```
### Scenario 4: Unable to get the fundamental details and invalid ticker
```
GIVEN the ticker is invalid value contains `>` or `<`
WHEN the user requests for fundamentals of the ticker.
THEN the system shall throw an exception `InValidTickerException` with message `Ticker must not contain '<' or '>' characters.`
```

## Non-Functional Requirements
- **NFR-01 (Performance):** get fundamentals of the stock, shall complete within 500ms on a standard broadband connection (>10 Mbps).

- **NFR-02 (Reliability):** get fundamentals of the stock, shall be available 99.9%  over 30 days.

## Tracebility Table
| Requirement ID | Description | Business Goal | Related Test(s) |
|---|---|---|---|
| GET-STOCK-F-001-BR-01 | empty ticker | BG-01: key stock fundamentals without manual research | GET-STOCK-F-001-TC-01 |
| GET-STOCK-F-001-BR-02 | No `<`/`>` chars in ticker | BG-01: key stock fundamentals without manual research | GET-STOCK-F-001-TC-02 |
| GET-STOCK-F-001-NFR-01 | Creation latency | BG-01: key stock fundamentals without manual research | GET-STOCK-F-001-TC-03 |
| GET-STOCK-F-001-NFR-02 | Reliability of service | BG-01: key stock fundamentals without manual research | GET-STOCK-F-001-TC-04 |
| GET-STOCK-F-001-FR-01 | get fundamentals with valid ticker | BG-01: key stock fundamentals without manual research | GET-STOCK-F-001-TC-05 |
| GET-STOCK-F-001-FR-02 | market data provider unavailable | BG-01: key stock fundamentals without manual research | GET-STOCK-F-001-TC-06 |
