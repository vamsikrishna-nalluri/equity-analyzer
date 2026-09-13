## 1. Zero-shot

### Prompt 1

**Prompt:**
```
You are a market expert, analyse the fundamental details provided for the stock and provide the recommendations.

Following are the details

Stock: LT.NS
Market Cap: ₹ 5,40,812 Cr.
Current Price: ₹ 3,931
High / Low: ₹ 4,440 / 3,288
Stock P/E: 30.7
Book Value: ₹ 794
Dividend Yield: 0.97 %
ROCE: 14.6 %
ROE: 15.9 %
Face Value: ₹ 2.00
Industry PE: 15.1
EPS: ₹ 121
Debt to equity: 1.15
No. Eq. Shares: 138
FII holding: 19.1 %
DII holding: 43.0 %
Avg Vol 1Yr: 24,51,385
Avg Vol 1Mth: 13,80,403
Avg Vol 1Wk: 17,81,261
Volume: 18,16,848
Price to book value: 4.95
Depreciation: ₹ 4,364 Cr.
Public holding: 37.6 %
Promoter holding: 0.00 %
Change in Prom Hold: 0.00 %
PB X PE: 152
EVEBITDA: 15.0

OUTPUT FORMAT : Stock - LT.NS, scrore - <score provided is here> , Reason - <provide your reasoning here>
```

**Answer:**
> Stock - LT.NS, Score - 6.5/10, Reason - L&T shows solid underlying business quality (ROE ~15.9%, ROCE ~14.6%, strong institutional confidence with DII holding at 43% and FII at 19.1%) and the unique structure of zero promoter holding (it's a professionally-managed, public-float company) removes governance/promoter-pledge risk that plagues many Indian large-caps. However, valuation is stretched: P/E of 30.7 is roughly 2x the industry average of 15.1, and P/B of 4.95 is rich for a company with debt/equity of 1.15 — the market is pricing in continued execution excellence and order-book growth rather than value. Dividend yield of 0.97% is modest, reflecting a growth/reinvestment orientation typical of a capital-goods and infra conglomerate rather than an income play. The stock trades meaningfully below its 52-week high (₹4,440) but well above its low (₹3,288), suggesting it's in a corrective/consolidation phase rather than a clear uptrend or downtrend. EV/EBITDA of 15.0 is reasonable for an infra/engineering major but not cheap.
>
> Net take: This is a fundamentally sound, well-managed business but not a "value buy" at current levels — it's priced for continued strong execution. Suitable for long-term investors comfortable paying a premium for quality and diversification (infra, defence, IT services, financial services arms), but not particularly attractive for value or high-dividend-seeking investors at this price point. A pullback toward the ₹3,400–3,600 zone would improve the risk-reward meaningfully.

**Observations:**
| | |
|---|---|
| **What's good** | The LLM is able to understand the stock details and provide the recommendation. It is given a score. |
| **What failed** | It measured the score for which not provided the details on what this core means? Also, the OUTPUT format is specified but Llm didn't't follow it. |
| **Why** | There is no strict instruction given to follow the output format. |

---

### Prompt 2 (refined)

**Prompt:**
```
You are a market expert, analyse the fundamental details provided for the stock and provide the recommendations.
Following are the details
Stock: LT.NS
Market Cap: ₹ 5,40,812 Cr.
Current Price: ₹ 3,931
High / Low: ₹ 4,440 / 3,288
Stock P/E: 30.7
Book Value: ₹ 794
Dividend Yield: 0.97 %
ROCE: 14.6 %
ROE: 15.9 %
Face Value: ₹ 2.00
Industry PE: 15.1
EPS: ₹ 121
Debt to equity: 1.15
No. Eq. Shares: 138
FII holding: 19.1 %
DII holding: 43.0 %
Avg Vol 1Yr: 24,51,385
Avg Vol 1Mth: 13,80,403
Avg Vol 1Wk: 17,81,261
Volume: 18,16,848
Price to book value: 4.95
Depreciation: ₹ 4,364 Cr.
Public holding: 37.6 %
Promoter holding: 0.00 %
Change in Prom Hold: 0.00 %
PB X PE: 152
EVEBITDA: 15.0

Follow the below mentioned output format provided while providing the recommendations. Make sure the reasoning don't include any financial numbers.

OUTPUT FORMAT : Stock - LT.NS, scrore - <score provided is here> , Reason - <provide your reasoning here>
```

**Response:**
> Stock - LT.NS, Score - 6.5/10, Reason - The company demonstrates solid operational efficiency and healthy returns on capital, backed by strong institutional confidence from both domestic and foreign investors. The absence of promoter holding reflects a professionally-managed corporate structure, which reduces governance-related risks such as pledging concerns. However, the stock currently trades at a premium compared to its sector peers, suggesting the market has already priced in expectations of continued strong execution and growth. The dividend payout is relatively modest, pointing to a growth-and-reinvestment orientation rather than an income-focused profile. The stock is trading well off its recent highs but comfortably above its lows, indicating a consolidation phase rather than a clear directional trend. Overall, this reflects a fundamentally sound and well-managed business, but one that is not particularly cheap at current levels — better suited to long-term, growth-oriented investors than to value or income seekers. A more attractive entry point would likely emerge on a meaningful price correction.

**Observations:**
| | |
|---|---|
| **What's good** | The LLM is able to understand the additional output format. It is given a score. |
| **What failed** | It measured the score for which not provided the details on what this core means? Also, the reason is too lengthy. |
| **Why** | There is no specific instrcution on score range and measurement of the score levels. Also, There is no instruction provided on length/brevity constraint. |

---