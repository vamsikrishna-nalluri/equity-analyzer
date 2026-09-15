# Prompt Library — Equity Analyzer

A record of prompts tested for the equity-analyzer project, covering zero-shot, few-shot, and chain-of-thought techniques, with observations on what worked, what failed, and why.

# Fundamental Score:
* [zero-shot](./prompt-library/zero-shot.md)
* [few-shot](./prompt-library/few-shot.md)
* [chain-of-thought](./prompt-library/chain-of-thought.md)


## Overall Model Behaviour Notes

**Hallucination**
When details are not provided to LLM, LLMs tend to hallucinate things. Which is what we have seen in few-shot prompt, where it hallucinated the Stock symbol.

**Context/format limits**
When writing prompts, it is important to provide a clear intent. If not, LLM will hallucinate and may produce wrong results. If we need precise output, better to specify the format very clear. The chain-of-thought consumed too many token as the LLM provided the reasoning as part of the LLM response.

**Quality differences**
We have explicitly given what should happen if data is not enough or not available. The response is very precise as we expected. So, it is important that, you prompt should have clear instructions for different situations.


# Risks and mitigation
[risks and mitigations](./risks/risks-and-mitigations.md)

# Prompts review
## [API design review](./week1/api_design_review.md)
### prompt summary:
* Technique - Zero-shot — no examples given, but heavily structured via XML tags, an explicit dimension checklist, and a strict output format
* Quality rating (1–5)	 - 5/5 — it caught a real, non-obvious bug (spec/implementation drift) rather than just restating surface issues, correctly distinguished "structural" vs. "small fix" per your instructions, and made no unsupported claims (flagged the freshness assumption explicitly)

## [code explanation](./week1/code_explanation.md)
### prompt summary:

* Prompt version - v2 — instruction #3 changed from line-by-line commenting to complexity justification
* Technique - Zero-shot
* Quality rating (1–5)	 - 5/5
* Justification	 - The revised instruction produces a more useful artifact — it forces genuine judgment about what counts as complex rather than mechanically annotating every line regardless of difficulty. This also resolves the tension I flagged in the v1 rating (literal line-by-line instruction vs. practical readability), so the score moves up from 4 to 5.


## [unit tests](./week1/unit-test-creation.md)

### prompt summary:
* Prompt	- Unit test generation (v4 — final)
* Technique	- Few-shot
* Quality rating (1–5)	- 5/5
* Justification	 - 25/25 tests passed against real code with zero modifications needed — the only issue was a project-config gap (pythonpath not set for the src/ layout), not a flaw in the generated tests. Correctly covered success paths, exception propagation, and non-obvious edge cases (consecutive separators, leading/trailing separators in the ticker regex) without being told those specific cases explicitly — it inferred them from reading the regex logic. Mocking was correctly scoped (only yf.Ticker and the port interfaces, never real network calls), honoring instruction #5.

## [bug fix](./week1/bug_root_cause_analysis.md)

### prompt summary:
* Prompt	- bug fix (v2 — final)
* Technique	 - Chain-of-thought
* Quality rating (1–5)	- 5/5 — first pass correctly identified the exact failure mechanism (None .get() chain) and correctly refused to guess the specific cause without seeing the code, flagging two honest hypotheses instead of fabricating confidence. Once given the real file, the diagnosis was immediate and precise (a one-character typo). That's the right behavior split: reason as far as the evidence allows, don't overreach, revise cleanly when more evidence arrives.
* Justification	- Split across the two runs to show the full arc: Run 1 (log-only, no source file) correctly traced the symptom back through the exception-handling layer — recognizing that the "unavailable" message was a translated error, not the real one — and then explicitly refused to collapse two plausible hypotheses (yFinance quirk vs. non-US ticker schema difference) into a false-confidence single answer, exactly per instruction 3. That's the harder, more valuable behavior for an RCA tool: knowing the limits of the available evidence instead of guessing plausibly. Run 2 (given the real file) immediately located the exact defect — a one-character key typo (regularMarketPrice1) — and, importantly, retracted the ticker-specific hypothesis from Run 1 rather than quietly ignoring it, noting the bug would reproduce on any ticker. It also caught a secondary, non-blocking issue (misleading "Trigger network request" comments) that wasn't asked for but adds real value. The combination — honest uncertainty when warranted, precise diagnosis when evidence allows, and self-correction across runs — is exactly what you want from a CoT-structured prompt, which is why this earns the full score rather than a "got lucky" 4.

## [refactor](./week1/legacy_code_refactoring.md)

### prompt summary:
* Prompt	- code refactor (v2 — final)
* Technique	- Zero-shot
* Quality rating (1–5)	- 5/5 — correctly identified real SOLID violations (not generic ones), the breaking-change list is genuinely accurate (the validation regression is a real behavior change worth flagging), and the output honored the "file names only" format constraint precisely.

