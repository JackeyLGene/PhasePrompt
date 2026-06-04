# LanguageWe + LoCoMo: Sidecar Value Validation

Date: 2026-06-04  
Status: research result concluded, engineering pilot complete.

## Core Claim

LanguageWe structural scoring added **+4.2pp net improvement** over a recency
baseline on DeepSeek-chat in a LoCoMo-MC pilot (497 QA items, 10 conversations).

The sidecar scoring layer itself uses:

- zero LLM calls;
- zero embeddings;
- zero training;
- zero query-time retrieval.

The full evaluation pipeline used DeepSeek-chat for compression generation and
QA answering.

## Experimental Setup

Dataset: LoCoMo-MC (`Percena/locomo-mc10`), 1986 multiple-choice questions
across 10 multi-session conversations. The pilot evaluates 497 stratified QA
items across the 10 conversations.

Reader/compressor:

- DeepSeek-chat;
- temperature 0;
- exact-match answer-letter scoring.

Sidecar configuration:

| Parameter | Value |
|-----------|-------|
| dim | 256 |
| kappa | 5.0 |
| sc_damping | enabled |
| pretrained corpus | NoLiMa book, 4898 sentences |

## Conditions

| ID | Description |
|----|-------------|
| NOCTX | Question and choices only |
| SUM_NONE | Model compresses conversation without hint |
| SUM_REC | Model compresses with recency hint |
| SUM_LW | Model compresses with LanguageWe structural hint |
| SUM_HYB | Model compresses with LW plus recency hints |
| FULL | Limited full-context reference, separate 50-QA sample |

FULL is not a strict upper bound because it uses a separate 50-QA sample and
conversation text is truncated.

## T2 Continuous Streaming Result

All 10 conversations were concatenated into one stream. A single LanguageWe
instance accumulated structure across 5882 messages. Its compact structural
hint was then used during query-agnostic conversation compression.

| Condition | Accuracy | vs REC |
|-----------|----------|--------|
| NOCTX | 37.8% | -15.5pp |
| SUM_NONE | 55.1% | +1.8pp |
| SUM_REC | 53.3% | baseline |
| **SUM_LW** | **57.5%** | **+4.2pp** |
| SUM_HYB | 53.7% | +0.4pp |

Answering-stage token use:

| Metric | SUM_REC | SUM_LW | Change |
|--------|---------|--------|--------|
| QA input tokens | 400,200 | 305,433 | **-23.7%** |
| Avg QA input tokens | 805 | 615 | **-190 tokens/question** |

The token saving is measured at QA time after summaries have been generated.
It should not be read as total end-to-end cost reduction for the whole
experiment, because the LW compression prompt includes a structural hint. It is
still practically important: the sidecar produced a compact memory that was
both more accurate and cheaper to reuse for later questions.

Paired vs REC:

| Condition | Wins | Losses | Ties | Net |
|-----------|------|--------|------|-----|
| SUM_NONE | 43 | 34 | 420 | +9 |
| **SUM_LW** | **65** | **44** | **388** | **+21** |
| SUM_HYB | 52 | 50 | 395 | +2 |

## By Question Type

| Type | n | SUM_REC | SUM_LW | Delta |
|------|---|---------|--------|-------|
| temporal_reasoning | 22 | 31.8% | 40.9% | +9.1pp |
| open_domain | 211 | 60.7% | 66.4% | +5.7pp |
| adversarial | 112 | 50.9% | 55.4% | +4.5pp |
| single_hop | 69 | 71.0% | 75.4% | +4.3pp |
| multi_hop | 83 | 28.9% | 27.7% | -1.2pp |

## Interpretation

The result supports a narrow but useful engineering claim:

> A structural sidecar can improve query-agnostic long-conversation compaction
> for a strong production LLM.

The result does not claim that PhasePrompt beats all memory systems, replaces
retrieval, or establishes a full autonomous memory architecture.

## Reproducibility Boundary

This repository includes saved result artifacts and a verification script. It
does not include the production LanguageWe implementation.

Current public artifacts support verification of the reported scores, paired
comparisons, and question-type breakdowns. A publication-grade run should add
stable qid sampling, tokenizer-based budget accounting, and saved stream
summaries.
