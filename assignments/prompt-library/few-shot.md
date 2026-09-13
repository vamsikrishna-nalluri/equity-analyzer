## 2. Few-shot

### Prompt 1

**Prompt:**
```
you are a market expert, analyse fundamentals details of the stock and provide the recommendations. Given the details in a specific format, provide the output in defined format.

Here is some examples:
Example 1 :
input :
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

OUTPUT: Stock - LT.NS, score - 6, Reason - It's a construction company with Huge order book and strong institutional support.

Example 2:
input :
Stock: HDFCBANK.NS
Market Cap: ₹ 10,91,709 Cr.
Current Price: ₹ 708
High / Low: ₹ 1,020 / 682
Stock P/E: 13.8
Book Value: ₹ 390
Dividend Yield: 1.84 %
ROCE: 7.02 %
ROE: 13.6 %
Face Value: ₹ 1.00
Industry PE: 13.9
EPS: ₹ 51.4
Debt to equity: 6.21
No. Eq. Shares: 1,541
FII holding: 41.8 %
DII holding: 41.8 %
Avg Vol 1Yr: 3,31,20,954
Avg Vol 1Mth: 2,90,63,236
Avg Vol 1Wk: 2,79,98,724
Volume: 3,43,36,284
Price to book value: 1.81
Depreciation: ₹ 0.00 Cr.
Public holding: 16.3 %
Promoter holding: 0.00 %
Change in Prom Hold: 0.00 %
PB X PE: 25.0
EVEBITDA: 15.9

OUTPUT: Stock - HDFCBANK.NS, score - 3, Reason - Stock P/E is very High

Here are the details of the stock, provide your recommendation in the specified output format.
Market Cap: ₹ 9,90,020 Cr.
Current Price: ₹ 1,379
High / Low: ₹ 1,480 / 1,188
Stock P/E: 17.6
Book Value: ₹ 527
Dividend Yield: 0.87 %
ROCE: 7.18 %
ROE: 15.9 %
Face Value: ₹ 2.00
Industry PE: 13.9
EPS: ₹ 78.4
Debt to equity: 5.55
No. Eq. Shares: 718
FII holding: 33.8 %
DII holding: 42.3 %
Avg Vol 1Yr: 1,46,81,069
Avg Vol 1Mth: 93,25,572
Avg Vol 1Wk: 1,12,08,505
Volume: 73,00,481
Price to book value: 2.62
Depreciation: ₹ 0.00 Cr.
Public holding: 23.7 %
Promoter holding: 0.00 %
Change in Prom Hold: 0.00 %
PB X PE: 46.2
EVEBITDA: 18.0

the score 1 being strong fundamentals and 10 being worst fundamentals
If you are not sure , the score fill the score and reason with N/A
```

**Answer:**
> Stock - ICICIBANK.NS (based on data pattern), score - 4, Reason - P/E slightly above industry average and premium valuation (P/B 2.62), but healthy ROE (15.9%) and strong institutional holding (FII+DII ~76%) support fundamentals.

**Observations:**
| | |
|---|---|
| **What worked** | LLM is able to understand the example formats specified and the output format and the output format is correctly followed by LLM. |
| **What failed** | The stock symbol is hallusinated. |
| **Why** | The stock symbol is not provided and no specific provided about how LLM should behave in case of missing data. |

---

### Prompt 2 (refined)

**Prompt:**
```
you are a market expert, analyse fundamentals details of the stock and provide the recommendations. Given the details in a specific format, provide the output in defined format.
Here is some examples:
Example 1 :
input :
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
OUTPUT: Stock - LT.NS, score - 6, Reason - It's a construction company with Huge order book and strong institutional support.

Example 2:
input :
Stock: HDFCBANK.NS
Market Cap: ₹ 10,91,709 Cr.
Current Price: ₹ 708
High / Low: ₹ 1,020 / 682
Stock P/E: 13.8
Book Value: ₹ 390
Dividend Yield: 1.84 %
ROCE: 7.02 %
ROE: 13.6 %
Face Value: ₹ 1.00
Industry PE: 13.9
EPS: ₹ 51.4
Debt to equity: 6.21
No. Eq. Shares: 1,541
FII holding: 41.8 %
DII holding: 41.8 %
Avg Vol 1Yr: 3,31,20,954
Avg Vol 1Mth: 2,90,63,236
Avg Vol 1Wk: 2,79,98,724
Volume: 3,43,36,284
Price to book value: 1.81
Depreciation: ₹ 0.00 Cr.
Public holding: 16.3 %
Promoter holding: 0.00 %
Change in Prom Hold: 0.00 %
PB X PE: 25.0
EVEBITDA: 15.9
OUTPUT: Stock - HDFCBANK.NS, score - 3, Reason - Stock P/E is very High

Here are the details of the stock, provide your recommendation in the specified output format.
Market Cap: ₹ 9,90,020 Cr.
Current Price: ₹ 1,379
High / Low: ₹ 1,480 / 1,188
Stock P/E: 17.6
Book Value: ₹ 527
Dividend Yield: 0.87 %
ROCE: 7.18 %
ROE: 15.9 %
Face Value: ₹ 2.00
Industry PE: 13.9
EPS: ₹ 78.4
Debt to equity: 5.55
No. Eq. Shares: 718
FII holding: 33.8 %
DII holding: 42.3 %
Avg Vol 1Yr: 1,46,81,069
Avg Vol 1Mth: 93,25,572
Avg Vol 1Wk: 1,12,08,505
Volume: 73,00,481
Price to book value: 2.62
Depreciation: ₹ 0.00 Cr.
Public holding: 23.7 %
Promoter holding: 0.00 %
Change in Prom Hold: 0.00 %
PB X PE: 46.2
EVEBITDA: 18.0

If the stock symbol or any other parameters are missing. point out the issues and don't hallucinate .

the score 1 being strong fundamentals and 10 being worst fundamentals
If you are not sure , the score fill the score and reason with N/A
```

**Response:**
> Stock - N/A, score - N/A, Reason - N/A. The stock symbol/name is missing from the input, so I can't identify which company this is. All the financial metrics are provided, but without a ticker or company name I won't guess or assume the identity — please share the stock symbol to get a proper recommendation.

**Observations:**
| | |
|---|---|
| **What worked** | LLM is able to understand the instruction related to unavailbility of data and followed the specified output format specification. |
| **What failed** | No issues, we can reduce the reason length. |
| **Why** | No specific instruction on the lenght of the reason provided. |

---