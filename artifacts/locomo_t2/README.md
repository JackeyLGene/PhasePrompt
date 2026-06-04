# LoCoMo T2 Artifacts

This folder contains saved result artifacts for the PhasePrompt / LanguageWe
LoCoMo-MC pilot.

## Files

| File | Description |
|------|-------------|
| `t2_main_20260604_1224_manifest.json` | per-conversation run manifest |
| `t2_main_20260604_1224_summaries.jsonl` | summaries generated in the per-conversation run |
| `t2_main_20260604_1224_results.jsonl` | QA results for per-conversation run |
| `t2_stream_20260604_1318_results.jsonl` | QA results for continuous stream run |

## Verification

From the repository root:

```bash
python tools/verify_locomo_results.py artifacts/locomo_t2/t2_stream_20260604_1318_results.jsonl
python tools/verify_locomo_results.py artifacts/locomo_t2/t2_main_20260604_1224_results.jsonl --full
```

The stream run also shows lower answering-stage input tokens for SUM_LW:

| Condition | Total QA input tokens | Avg QA input tokens |
|-----------|----------------------:|--------------------:|
| SUM_REC | 400,200 | 805 |
| SUM_LW | 305,433 | 615 |

This is a 23.7% reduction in QA input tokens relative to SUM_REC.

## Notes

- The LoCoMo dataset is not redistributed here.
- The saved per-conversation summaries are LLM-generated derivatives of
  LoCoMo-MC conversation content.
- LoCoMo-MC is licensed CC BY-NC 4.0; these derived artifacts are for
  non-commercial research review only. See `../../THIRD_PARTY_NOTICES.md`.
- Stream summaries were not saved separately in the pilot run.
- These artifacts verify reported metrics, not the unpublished sidecar
  implementation.
