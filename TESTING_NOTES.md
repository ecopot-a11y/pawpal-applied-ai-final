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

## Required local verification

Run `python -m pytest -v` in the final project directory to verify the original 15 tests and the new 8 tests together. Record the actual count and results in README.md.

Run `python -m streamlit run app.py`, add sample pets/tasks, and click **Generate validated AI care plan**. Confirm the proposal and decision log appear. This UI check has not yet been performed here.

## Important limitations

- This is a deterministic, rule-based planning agent with evaluation and adjustment, not a generative language model or external LLM.
- Fixed-time appointments are never moved automatically. Conflicting fixed appointments are flagged for manual review.
- The plan is a proposal and does not modify existing tasks.
- The evaluator checks constraints on the proposed tasks; it does not establish that every real-world pet-care requirement is met.
- No veterinary or medication timing advice is provided.
