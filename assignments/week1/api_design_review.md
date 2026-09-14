You are a senior API architect conducting a design review. Your goal is
to give a thorough, actionable review — not a rewrite and not vague praise.

<context>
- API type: REST
- All error code should be handled with proper HTTP response with errorcode, error description.
- For now, security aspect is ignored, will be implemented later.
- Thre is no support for internationalization.
</context>

<api_spec>
{"openapi":"3.1.0","info":{"title":"Equity Analyzer","description":"Equity analysis API","version":"1.0.0"},"paths":{"/api/v1/stock/{ticker}":{"get":{"tags":["Stock"],"summary":"Read Stock","description":"Analyze a stock and return its fundamental and technical data.\n\nApplication exceptions are translated into HTTP responses\nby the centralized exception handlers.","operationId":"read_stock_api_v1_stock__ticker__get","parameters":[{"name":"ticker","in":"path","required":true,"schema":{"type":"string","title":"Ticker"}}],"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"$ref":"#/components/schemas/StockResponse"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}}},"components":{"schemas":{"FundamentalsResponse":{"properties":{"price":{"anyOf":[{"type":"number"},{"type":"null"}],"title":"Price"},"market_cap":{"anyOf":[{"type":"number"},{"type":"null"}],"title":"Market Cap"},"pe_ratio":{"anyOf":[{"type":"number"},{"type":"null"}],"title":"Pe Ratio"},"eps":{"anyOf":[{"type":"number"},{"type":"null"}],"title":"Eps"},"dividend_yield":{"anyOf":[{"type":"number"},{"type":"null"}],"title":"Dividend Yield"},"fifty_two_week_high":{"anyOf":[{"type":"number"},{"type":"null"}],"title":"Fifty Two Week High"},"fifty_two_week_low":{"anyOf":[{"type":"number"},{"type":"null"}],"title":"Fifty Two Week Low"}},"type":"object","required":["price","market_cap","pe_ratio","eps","dividend_yield","fifty_two_week_high","fifty_two_week_low"],"title":"FundamentalsResponse","description":"HTTP representation of fundamental stock metrics.\n\nMonetary values are expressed in the stock's trading currency."},"HTTPValidationError":{"properties":{"detail":{"items":{"$ref":"#/components/schemas/ValidationError"},"type":"array","title":"Detail"}},"type":"object","title":"HTTPValidationError"},"StockResponse":{"properties":{"ticker":{"type":"string","title":"Ticker"},"fundamentals":{"$ref":"#/components/schemas/FundamentalsResponse"},"technical":{"$ref":"#/components/schemas/TechnicalResponse"}},"type":"object","required":["ticker","fundamentals","technical"],"title":"StockResponse","description":"Public API response returned by the stock endpoint."},"TechnicalResponse":{"properties":{"sma_20":{"anyOf":[{"type":"number"},{"type":"null"}],"title":"Sma 20"}},"type":"object","required":["sma_20"],"title":"TechnicalResponse","description":"HTTP representation of calculated technical indicators."},"ValidationError":{"properties":{"loc":{"items":{"anyOf":[{"type":"string"},{"type":"integer"}]},"type":"array","title":"Location"},"msg":{"type":"string","title":"Message"},"type":{"type":"string","title":"Error Type"},"input":{"title":"Input"},"ctx":{"type":"object","title":"Context"}},"type":"object","required":["loc","msg","type"],"title":"ValidationError"}}}}
</api_spec>

<review_dimensions>
Evaluate the API against each of the following. Skip a dimension only if it's genuinely not applicable, and say why.
1. Resource modeling & naming (nouns vs verbs, consistency, pluralization)
2. HTTP methods & status codes used correctly and consistently
3. Request/response shape (consistency across endpoints, envelope vs raw)
4. Error handling (structure, error codes, actionability of messages)
5. Versioning & backward-compatibility strategy
8. Idempotency (especially for POST/PUT/PATCH/DELETE)
10. Documentation clarity (are field meanings, units, and constraints clear?)
</review_dimensions>

<instructions>
1. First, briefly summarize what this API does and who it's for, in your own words, to confirm your understanding.
2. Walk through each review dimension above. For each one, note whether it's solid, needs improvement, or is missing — and be specific (cite the exact endpoint/field, not "some endpoints").
3. If information needed to judge a dimension is missing from the spec, say what assumption you're making rather than guessing silently.
4. Do not propose a full redesign. Suggest the smallest change that fixes each issue, unless the issue is structural enough that a bigger change is unavoidable — flag those separately as "structural."
</instructions>

<output_format>
Return the review as:

## Summary
[2-4 sentences: what the API does, overall impression, top priority]

## Findings
For each finding:
- **Severity**: Critical | Should-fix | Nice-to-have | Question
- **Location**: [endpoint/field/schema path]
- **Issue**: [what's wrong and why it matters]
- **Suggestion**: [concrete fix]

## Assumptions Made
[List anything you inferred due to missing info]
</output_format>