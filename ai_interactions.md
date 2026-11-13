# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7) — historical Module 2 work

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked Claude to add a third, optional scheduling algorithm to PawPal+: find the earliest free start time for a task of a specified duration within a configurable daily window. I asked it to preserve existing sorting, filtering, conflict detection, recurrence, and scheduling behavior, and to add automated tests.

**What did the agent do?**

- Updated `pawpal_system.py` with `Scheduler.next_available_slot(duration_minutes, on_date, workday_start, workday_end)`.
- Created `tests/test_next_available_slot.py` with tests for an empty day, a gap between tasks, overlapping busy tasks, completed/future/untimed tasks, insufficient room, and invalid duration.
- Updated `ai_interactions.md` with this workflow record.
- The method sorts occupied time intervals, moves the proposed start past occupied intervals, and returns an `HH:MM` time or `None` when no slot fits.

**What did you have to verify or fix manually?**

The generated files were integrated locally and verified with pytest. The six available-slot tests passed in the final combined 23-test run. The method does not schedule across midnight, change existing task times, or reserve a slot automatically.

## Final project collaboration

For the final PawPal AI extension, I used ChatGPT to develop a separate planning agent and reliability evaluator, integrate the proposal-only workflow, and draft tests and documentation. I accepted separate planning and evaluation modules and narrowed automatic schedule changes to proposals requiring owner review. See [model_card.md](model_card.md) for the complete graded reflection. The final combined test run reported 23 passed in 0.54 seconds.
