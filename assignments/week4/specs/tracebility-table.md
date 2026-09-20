# Traceability Table — Stock Fundamentals Feature Set

**Business Goal**
**BG-01:** Enable users to make faster, more informed investment decisions by providing key stock fundamentals without manual research across multiple sources.

| Requirement ID | Description | Business Goal | Related Test(s) |
|---|---|---|---|
| GET-STOCK-F-001-FR-01 | Get fundamentals with valid ticker | BG-01 | GET-STOCK-F-001-TC-01 |
| GET-STOCK-F-001-FR-02 | Market data provider unavailable | BG-01 | GET-STOCK-F-001-TC-02 |
| GET-STOCK-F-001-BR-01 | Empty ticker rejected | BG-01 | GET-STOCK-F-001-TC-03 |
| GET-STOCK-F-001-BR-02 | No `<`/`>` characters in ticker | BG-01 | GET-STOCK-F-001-TC-04 |
| GET-STOCK-F-001-NFR-01 | Fundamentals retrieval latency | BG-01 | GET-STOCK-F-001-TC-05 |
| GET-STOCK-F-001-NFR-02 | Fundamentals retrieval reliability | BG-01 | GET-STOCK-F-001-TC-06 |
| INVALID-TICKER-002 | Superseded — see GET-STOCK-F-001-BR-01/BR-02 | BG-01 | N/A |
| CACHE-STOCK-F-001-FR-01 | Get fundamentals from cache | BG-01 | CACHE-STOCK-F-001-TC-01 |
| CACHE-STOCK-F-001-FR-02 | Get fundamentals when cache is not available | BG-01 | CACHE-STOCK-F-001-TC-02 |
| CACHE-STOCK-F-001-FR-03 | Get fundamentals when cache is expired | BG-01 | CACHE-STOCK-F-001-TC-03 |
| CACHE-STOCK-F-001-FR-04 | Get fundamentals when cache is empty and provider unavailable | BG-01 | CACHE-STOCK-F-001-TC-04 |
| CACHE-STOCK-F-001-BR-01 | Cache invalid at 5 minutes or older (boundary) | BG-01 | CACHE-STOCK-F-001-TC-05 |
| CACHE-STOCK-F-001-NFR-01 | Cache retrieval latency | BG-01 | CACHE-STOCK-F-001-TC-06 |
| CACHE-STOCK-F-001-NFR-02 | Cache availability/reliability | BG-01 | CACHE-STOCK-F-001-TC-07 |

**Coverage summary:** 13 active requirements (2 FR + 2 BR + 2 NFR for Get Stock Fundamentals; 4 FR + 1 BR + 2 NFR for Cache Stock Data), all tracing to BG-01, each with a unique test ID. 1 spec (INVALID-TICKER-002) marked superseded following peer review.