# PawPal AI — Evaluation Notes

## Verified in the development environment

Command: `python -m pytest -q tests/test_ai_planner.py`

Result: **8 passed**.

| Test input | Expected behavior | Result |
|---|---|---|
| Two fixed tasks at 08:00 | Flag the conflict without silently moving either appointment | Pass |
| Fixed walk at 08:00 and flexible feeding | Place feeding at 08:20 and explain adjustment | Pass |
| Tasks exceeding 60-minute budget | Keep selected work within budget; report omission | Pass |
| Only 10 minutes free for a 20-minute task | Flag no available slot | Pass |
| Window ending before it starts | Raise a clear validation error | Pass |
| Two non-overlapping fixed tasks | Accept without revisions | Pass |
| Manually supplied overlapping, over-budget plan | Independent evaluator rejects both violations | Pass |
| Completed and future tasks | Exclude from today's plan | Pass |

## Verified local combined suite

Command: `python -m pytest -v`

```text
collected 23 items
========================== 23 passed in 0.54s ==========================
```

The reported Windows run used Python 3.13.7 and pytest 9.2.0. All 15 original tests and eight new tests passed. See README.md and sample_output.txt for four CLI scenarios.

## UI verification

Run `python -m streamlit run app.py` to inspect the current build. The README links an optional Loom walkthrough. Automated end-to-end UI testing has not been demonstrated; the combined pytest result is not a browser test result.

## Important limitations

- This is a deterministic, rule-based planning agent with evaluation and adjustment, not a generative language model or external LLM.
- Fixed-time appointments are never moved automatically. Conflicting fixed appointments are flagged for manual review.
- The plan is a proposal and does not modify existing tasks.
- The evaluator checks constraints on the proposed tasks; it does not establish that every real-world pet-care requirement is met.
- No veterinary or medication timing advice is provided.
