# Week 1 Prompt Library — Backend Development Track
**Project:** equity-analyzer
**Role track:** Backend Development
**Prompt types covered:** Zero-shot ×3, Few-shot ×1, Chain-of-thought ×1 (≥3 required ✅)

---

## Setup Checklist

- [x] Claude.ai access confirmed
- [x] Claude API key configured (environment variable, per project `README.md`)
- [x] Claude Code installed & verified — `claude --version` → `2.1.269 (Claude Code)`
- [x] Git repo `equity-analyzer` set up with layered architecture (`api` / `application` / `domain` / `infrastructure`)

---

## Prompt 1 — API Design Review

**Technique:** Zero-shot
**Quality rating:** 5/5

**Prompt:**
```
You are a senior API architect conducting a design review. Your goal is
to give a thorough, actionable review — not a rewrite and not vague praise.

<context>
- API type: REST
- All error code should be handled with proper HTTP response with errorcode, error description.
- For now, security aspect is ignored, will be implemented later.
- Thre is no support for internationalization.
</context>

<api_spec>
[OpenAPI 3.1 spec for GET /api/v1/stock/{ticker}, pasted as JSON]
</api_spec>

<review_dimensions>
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
## Summary
## Findings
- Severity | Location | Issue | Suggestion
## Assumptions Made
</output_format>
```

**Justification:** Run twice across two versions of the real OpenAPI spec (before and after exception handling was implemented in code). Both runs caught a genuine, non-obvious defect — spec/implementation drift, where the code returned `404`/`400`/`503` but the published OpenAPI contract only documented `200`/`422`. This is the kind of issue that's easy for a human reviewer to miss because the code "works," but breaks any client generating a typed SDK from the spec. The review correctly separated structural issues (missing error schema) from small fixes (adding a `pattern` to a path parameter), per instruction 4, and explicitly flagged its own assumptions rather than guessing. No hallucinated findings across either run.

---

## Prompt 2 — Code Explanation

**Technique:** Zero-shot
**Quality rating:** 5/5 (v2) — see v1→v2 comparison below

**Prompt (v2, final):**
```
You are an expert in understanding and explin the code in details. Your goal is
to read the code and provide clear explanation what the specific piece of code does.

<context>
Language : Python
framework : FastAPI
Libraries used: yfinance
The project has list of APIs, these fetch the infomratin from the yfinance API
and expose them to use the user or other systems.
</context>

<instructions>
1. Provide a summary of the complete functoinality.
2. Explain the code for each function, provide details of the input paremeters and return values.
3. If the code is complex, explain with additional details why it is so complex.
4. Always explain the code in the order of execution.
5. Explain the logic, if there are multiple nested loops or recusive logic
</instructions>

<ouput_format>
Summary:
Function summary: input parameters / return
Each line / complexity notes
</output_format>
```

**Justification — v1 → v2 comparison:**
- **v1** (instruction #3: "explain with inline comments for each line") scored **4/5**. It produced a technically correct, well-ordered trace across 7 files, but the literal instruction — comment *every* line — was in tension with actual readability; I used judgment to group trivial lines (imports, blank lines) instead of following the instruction to the letter, which is a real gap between what was asked and what was delivered.
- **v2** (instruction #3 changed to: "explain with additional details why it is so complex") scored **5/5**. This is a clear demonstration of how a one-instruction edit measurably improved prompt quality: instead of mechanically annotating every line regardless of difficulty, the output correctly identified only the two genuinely complex pieces of logic in the codebase (the ticker-validation regex, and the three-layer exception translation chain) and explained *why* each is complex rather than just *what* it does. This resolved the v1 tension entirely.

---

## Prompt 3 — Unit Test Generation

**Technique:** Few-shot (the `<examples>` tag supplies a real test-naming example)
**Quality rating:** 5/5 — confirmed by an actual `pytest` run, not just review

**Prompt (v4, final):**
```
You are an expert in writing the unit tests based on the source code. Your goal
is to read the source code and understand before writing the unit tests.

<context>
Language : Python
framework : pytest
Source files : [stock_service.py, yfinance_provider.py]
</context>

<instructions>
1. Make sure not to change the source code to satisfy any tests.
2. There is no need to write the comments for the unit tests.
3. Make sure the test method always starts with `test_`
4. The test method should be self explanatory of the test senario.
5. When external parties needs to be called, mock the provider using unittest.mock or pytest-mock.
6. Make sure each tests only covers one test case, don't combine multiple tests.
7. Make sure to add negative tests and edge cases as well.
8. Make sure test package follows the same package structure as src package structure.
</instructions>

<examples>
example test method format : test_calculate_sma_with_insufficient_history_returns_none()
</examples>
```

**Justification:** This prompt went through 4 revision rounds before being run (fixing an example that pointed at the wrong architectural layer, adding a mandatory mocking requirement, and adding structure-mirroring) — each round is documented above as its own review pass. Once run, it generated 25 tests across 2 files. **All 25 passed on the first real execution** against the actual `equity-analyzer` codebase, with zero changes needed to the generated tests themselves (the only failure on first attempt was a project `pytest.ini` / `pythonpath` configuration gap, unrelated to the test content). It correctly covered success paths, exception propagation for both custom exception types, and non-obvious regex edge cases (leading/trailing/consecutive separators in ticker validation) that weren't explicitly listed in the prompt — inferred by actually reading the validation logic. Mocking was scoped correctly per instruction 5: only `yf.Ticker` was mocked, no real network calls.

---

## Prompt 4 — Bug Root Cause Analysis

**Technique:** Chain-of-thought (instructions 1→2→3 force a sequential understand → parse-logs → synthesize trace; the output format's `Reasoning` field explicitly demands the visible step-by-step trail)
**Quality rating:** 5/5

**Prompt:**
```
You are an expert in analysing the bugs by checking the logs, code. Your goal is
to understand the bug, read logs and start looking at the respective code to
analyse and list doewn the reasons(s).

<context>
<bug_detail>
- bug description: unable to fetch the market data
- Actual result: "Market data provider is temporarily unavailable."
- Expected result: the endpoint `v1/stock/TCS.NS` should return the stock details
- log file: [Python traceback — AttributeError: 'NoneType' object has no attribute 'get']
- suspected files : unknown
</bug_detail>
</context>

<instructions>
1. Analyse the existing code and make sure the existing code is understood clealy.
2. Analyse the log provided, makes sure to list down the errors and warnings.
3. if multiple reasons exists, list down each reason with detail explanation, don't force to a single answer.
4. log format is python logging
</instructions>

<output_format>
## Summary of bug
## Analysis
- Details / Solutions / Reasoning / Files Effected
</output_format>
```

**Justification:** Run twice — once with only the log and the last-known source file (no live access to the current repo state), once with the actual current file pasted in. **Run 1** correctly declined to force a single root cause when the evidence didn't support it (per instruction 3), presenting two honest, plausible hypotheses instead of fabricating confidence — the harder and more valuable behavior for an RCA tool. **Run 2**, given the real code, immediately pinpointed the exact defect (a one-character key typo, `regularMarketPrice1`) and explicitly retracted the earlier ticker-specific hypothesis rather than silently dropping it, correctly noting the bug would reproduce on any ticker, not just `TCS.NS`. It also surfaced a secondary, unrequested but genuinely useful observation (misleading code comments). The combination of calibrated uncertainty when warranted and precise diagnosis once evidence arrived is exactly the target behavior for a chain-of-thought debugging prompt.

---

## Prompt 5 — Legacy Code Refactoring

**Technique:** Zero-shot
**Quality rating:** 5/5

**Prompt:**
```
You are an experienced software engineer to do the refatoring of the code.
You goal to refactor the legacy code and re-write the code by following SOLID
principles, design patterns and coding guideline.

<context>
- New coding guidelines: coding_guildelines.md
- Legacy code: main_old.py
</context>

<instructions>
1. Make sure the refactor is not broken any existing functionality.
2. The plan is to do a progressive refactor. If any refator, which requires a
   major change, please list down, so that we can take neccessary steps.
3. All the tests should be re-written with complete coverage of new code.
4. Make sure the documentation is updated as per the new code.
5. When necessary, introduce an integration layer to ensure the existing code
   works seamlessly with the new implementation without disrupting current
   functionality.
</instructions>

<output_format>
Return:
1. A summary of what's being refactored and why?
2. The full refactored file(s), just list down the file names.
3. A list of any breaking/major changes requiring separate approval
4. updated tests, list down only the file names.
</output_format>
```

**Justification:** Run against the real, original single-file `main.py` and the project's actual `coding_guildelines.md`. Correctly identified genuine SOLID violations (Single Responsibility and Dependency Inversion — business logic was directly coupled to `yfinance`, making it untestable without network access) rather than generic textbook complaints. The proposed file breakdown matched the project's actual, independently-built layered architecture almost exactly, and the generated breaking-changes list correctly flagged a real behavioral regression risk (stricter ticker validation could reject previously-accepted inputs) that wasn't obvious from a surface read of the refactor. Output format constraints (file names only, not full rewritten content) were followed precisely.

---

## Sample Output — Demonstrating a Backend Use Case

The unit-test generation prompt (Prompt 3) produced real, executable pytest test files against the project's actual source code — this is the clearest concrete backend artifact in the library, since it was independently verified by running `pytest` and confirming all 25 tests passed:

- `tests/unit/application/test_stock_service.py` — 16 tests covering ticker validation (regex edge cases) and analysis orchestration (success paths, exception propagation)
- `tests/unit/infrastructure/market_data/test_yfinance_provider.py` — 9 tests covering yFinance adapter behavior with full network mocking

```
collected 25 items
...
================================================ 25 passed in 0.66s =
```

---

## Notes on Model Behavior Observed

- **Hallucination risk is low when the model has real code to check against**, and highest when working from a spec/log alone without source access (Prompt 4, Run 1) — in that case, the model correctly hedged rather than guessing, which is the desired behavior, not a failure.
- **Instruction ambiguity directly affects output quality**, demonstrated concretely by Prompt 2's v1→v2 rating change from a single instruction edit.
- **Weak examples actively mislead few-shot prompts** — Prompt 3's first draft included an example testing a scenario that could never occur in practice (null dependency injection), which had to be caught and replaced before the prompt was trustworthy to run.
