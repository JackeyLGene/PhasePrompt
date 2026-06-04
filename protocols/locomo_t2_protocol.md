# LoCoMo T2 Protocol

Date: 2026-06-04  
Status: pilot protocol, not final industry benchmark.

## Question

Can a query-free structural sidecar improve a model's own conversation
compression quality?

This is the agent-relevant setting:

1. A long conversation has ended.
2. The system must compress it before knowing future questions.
3. Future QA uses the compressed memory.

## Dataset

LoCoMo-MC (`Percena/locomo-mc10`):

- 1986 multiple-choice QA items;
- 10 multi-session conversations;
- 10 choices per question;
- exact-match letter scoring.

The dataset itself is not redistributed in this repository.

## Main Conditions

| Condition | Meaning |
|-----------|---------|
| NOCTX | QA with question and choices only |
| SUM_NONE | LLM compresses conversation with no hint |
| SUM_REC | LLM compresses with recency hint |
| SUM_LW | LLM compresses with LanguageWe structural hint |
| SUM_HYB | LLM compresses with both LW and recency hints |
| FULL | Limited full-context reference, separate 50-QA sample |

## T2 Per-Conversation Run

Each conversation is processed independently by the sidecar.

Artifacts:

- `artifacts/locomo_t2/t2_main_20260604_1224_manifest.json`
- `artifacts/locomo_t2/t2_main_20260604_1224_summaries.jsonl`
- `artifacts/locomo_t2/t2_main_20260604_1224_results.jsonl`

Results:

| Condition | Accuracy |
|-----------|----------|
| NOCTX | 36.4% |
| SUM_NONE | 51.9% |
| SUM_REC | 51.3% |
| SUM_LW | 53.1% |
| SUM_HYB | 50.1% |
| FULL | 58.0% |

Paired vs REC:

| Condition | Net |
|-----------|-----|
| SUM_NONE | +3 |
| SUM_LW | +9 |
| SUM_HYB | -6 |

## T2 Continuous Stream Run

All 10 conversations are concatenated into one stream. A single sidecar instance
accumulates structure across all messages, then emits one compact hint used
during each conversation summary.

Artifact:

- `artifacts/locomo_t2/t2_stream_20260604_1318_results.jsonl`

Results:

| Condition | Accuracy |
|-----------|----------|
| NOCTX | 37.8% |
| SUM_NONE | 55.1% |
| SUM_REC | 53.3% |
| SUM_LW | 57.5% |
| SUM_HYB | 53.7% |

Answering-stage token use:

| Condition | Total QA input tokens | Avg QA input tokens |
|-----------|----------------------:|--------------------:|
| SUM_REC | 400,200 | 805 |
| SUM_LW | 305,433 | 615 |

SUM_LW used 23.7% fewer QA input tokens than SUM_REC while improving accuracy
by 4.2 percentage points.

Paired vs REC:

| Condition | Wins | Losses | Ties | Net |
|-----------|------|--------|------|-----|
| SUM_NONE | 43 | 34 | 420 | +9 |
| SUM_LW | 65 | 44 | 388 | +21 |
| SUM_HYB | 52 | 50 | 395 | +2 |

## Known Gaps

- Stream summaries and manifest were not saved separately.
- Sampling used Python `hash(qt)` in the pilot script; a follow-up protocol
  should use stable hashing and save qids.
- FULL uses a separate 50-QA sample and should not be read as a strict upper
  bound.
- Word budgets were approximate and should be replaced with tokenizer counts in
  a final benchmark run.

## Verification

Run:

```bash
python tools/verify_locomo_results.py artifacts/locomo_t2/t2_stream_20260604_1318_results.jsonl
python tools/verify_locomo_results.py artifacts/locomo_t2/t2_main_20260604_1224_results.jsonl --full
```
