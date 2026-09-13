# Prompt Library — Equity Analyzer

A record of prompts tested for the equity-analyzer project, covering zero-shot, few-shot, and chain-of-thought techniques, with observations on what worked, what failed, and why.

# Fundamental Score:
* [zero-shot](zero-shot.md)
* [few-shot](few-shot.md)
* [chain-of-thought](chain-of-thought.md)


## Overall Model Behaviour Notes

**Hallucination**
When details are not provided to LLM, LLMs tend to hallucinate things. Which is what we have seen in few-shot prompt, where it hallucinated the Stock symbol.

**Context/format limits**
When writing prompts, it is important to provide a clear intent. If not, LLM will hallucinate and may produce wrong results. If we need precise output, better to specify the format very clear. The chain-of-thought consumed too many token as the LLM provided the reasoning as part of the LLM response.

**Quality differences**
We have explicitly given what should happen if data is not enough or not available. The response is very precise as we expected. So, it is important that, you prompt should have clear instructions for different situations.