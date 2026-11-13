# PawPal AI — Intelligent Pet Care Planning and Reliability System

## Project summary

PawPal AI is an extension of **PawPal+**, my Module 2 AI110 project. It helps pet owners coordinate care across multiple pets by proposing practical schedules, checking constraints, explaining scheduling decisions, and identifying tasks that need human attention.

The project emphasizes **reliable, explainable planning**: a proposed schedule should be checked before a pet owner relies on it. The implemented extension uses a multi-step, rule-based planning agent with a propose-and-check workflow with flexible-task placement followed by independent validation, rather than a hosted language model.

## Original project: PawPal+ (Module 2)

PawPal+ was a Python and Streamlit pet-care scheduling application designed to organize care tasks for multiple pets. It allowed owners to add pets and tasks, assign priorities and recurrence schedules, track completion, generate daily task lists within a time budget, detect overlapping tasks, and find available time slots. The original system warned about conflicts but did not automatically produce and validate a revised, conflict-free schedule.

Original project: [AI110 Module 2 PawPal starter](https://github.com/ecopot-a11y/ai110-module2show-pawpal-starter)

## What the final project adds

1. **Planning agent:** Builds a proposed timed care schedule from the owner's pets, tasks, priorities, available minutes, and scheduling window.
2. **Propose-and-check workflow:** Places flexible tasks around fixed appointments, checks the resulting proposal, and flags tasks that cannot be scheduled. If independent validation fails, the proposal is rejected.
3. **Reliability guardrails:** Validate input and scheduling constraints and flag tasks that cannot be scheduled rather than silently omitting them or claiming success.
4. **Explainability and owner oversight:** Explain the resulting plan and unresolved trade-offs; present proposed changes for owner review without automatically applying them.
5. **Scenario-based evaluation:** Tests the integrated workflow with reproducible cases and records what passed or failed.

The extension is integrated into section 6 of the Streamlit application. The app displays proposed schedules, independent validation results, unplanned tasks, and a decision log. It does not apply schedule changes automatically.

## Architecture overview

Mermaid source: [`diagrams/architecture.mmd`](diagrams/architecture.mmd).

The **implemented architecture** follows this flow:

1. The pet owner enters tasks and planning preferences through Streamlit (`app.py`).
2. Input validation checks the request before planning.
3. The system retrieves the in-memory `Owner`, `Pet`, and `Task` records managed by `pawpal_system.py`.
4. `ai_planner.py` proposes task times for flexible tasks and preserves fixed-time appointments.
5. `reliability.py` independently checks overlap, scheduling window, time budget, task eligibility, and fixed-time preservation. The planner places flexible tasks around occupied time and flags tasks it cannot schedule. This is a deterministic propose-and-check workflow, not an unrestricted iterative search.
6. The app displays an explanation, unresolved issues, and a **proposal only** for human review; the user must manually make any desired changes.
7. Automated tests exercise validation, planning, and evaluation.

**Architecture verification:** The Mermaid source should match the committed `ai_planner.py`, `reliability.py`, and `app.py`. In particular, it must not depict an implemented automatic approval/save action, since the UI currently presents proposals only.

## Technology

- Python 3.13 (tested locally with Python 3.13.7)
- Streamlit user interface
- Pytest automated testing
- Git and GitHub version control
- Mermaid architecture diagram

The implemented planner is a **deterministic, rule-based planning workflow with independent evaluation**, not a fine-tuned model or an LLM. It should not be described as providing veterinary diagnosis or medical advice.

## Setup and run

### 1. Clone the repository

```powershell
git clone https://github.com/ecopot-a11y/pawpal-applied-ai-final.git
cd pawpal-applied-ai-final
```

### 2. Create and activate a virtual environment (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run the following in the current terminal and then activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Run the PawPal AI Streamlit interface

```powershell
python -m streamlit run app.py
```

The interface supports pet/task management, recurrence, conflict warnings, daily task selection, and **section 6: AI-assisted care planning (proposal only)**. Add pets and tasks, choose a plan date, then click **Generate validated AI care plan**. Inspect the proposed schedule, independent validation, unplanned tasks, and decision log. The UI does not automatically save proposed times.

### 5. Run the original command-line demonstration

```powershell
python main.py
```

### 6. Run automated tests

```powershell
python -m pytest -v
```

The original command-line demonstration exercises the legacy scheduler. For reproducible **AI planning** examples, run the additional `demo_ai.py` file:

```powershell
python demo_ai.py
```

The following inputs and outputs were produced by running that script against the supplied `pawpal_system.py`, `ai_planner.py`, and `reliability.py` implementation with the fixed test date `2026-11-05`. 

## Sample interactions: actual inputs, outputs, and guardrails

```text
=== Flexible task avoids fixed appointment ===
Input: budget=60 min, window=08:00-20:00
  Mochi: Walk, 20 min, high, time=08:00
  Luna: Feed, 10 min, medium, time=flexible
Proposed plan:
  08:00 Mochi: Walk
  08:20 Luna: Feed
Validation: PASS; minutes=30/60; revisions=1
Unplanned:
  (none)
Decision log:
  Scheduled Mochi: Walk at 08:00 (high priority).
  Revised Luna: Feed to 08:20 to avoid occupied time.
  Scheduled Luna: Feed at 08:20 (medium priority).

=== Time budget omits a task ===
Input: budget=60 min, window=08:00-20:00
  Mochi: Walk, 40 min, high, time=flexible
  Luna: Feed, 20 min, high, time=flexible
  Luna: Play, 30 min, low, time=flexible
Proposed plan:
  08:00 Luna: Feed
  08:20 Mochi: Walk
Validation: PASS; minutes=60/60; revisions=1
Unplanned:
  Luna: Play — exceeds remaining time budget
Decision log:
  Scheduled Luna: Feed at 08:00 (high priority).
  Revised Mochi: Walk to 08:20 to avoid occupied time.
  Scheduled Mochi: Walk at 08:20 (high priority).

=== No free slot in planning window ===
Input: budget=100 min, window=08:00-09:00
  Mochi: Walk, 50 min, high, time=08:00
  Luna: Feed, 20 min, medium, time=flexible
Proposed plan:
  08:00 Mochi: Walk
Validation: PASS; minutes=50/100; revisions=0
Unplanned:
  Luna: Feed — no free slot; review manually
Decision log:
  Scheduled Mochi: Walk at 08:00 (high priority).

=== Conflicting fixed appointments ===
Input: budget=60 min, window=08:00-20:00
  Mochi: Walk, 20 min, high, time=08:00
  Luna: Feed, 10 min, medium, time=08:00
Proposed plan:
  08:00 Mochi: Walk
Validation: PASS; minutes=20/60; revisions=0
Unplanned:
  Luna: Feed — fixed-time conflict; review manually
Decision log:
  Scheduled Mochi: Walk at 08:00 (high priority).
```

**Interpretation:** `Validation: PASS` means the **selected proposed entries** satisfy the evaluator's constraints; it does **not** mean all requested tasks were scheduled. The `Unplanned` field must be reviewed separately. In the fixed-time conflict example, one appointment remains unplanned for human review.

## Design decisions and trade-offs

- **Reuse tested scheduling code:** Build around the existing `Scheduler` instead of replacing functioning recurrence, conflict detection, and task management.
- **Prefer reproducibility:** Use a deterministic, rule-based planning agent without requiring API keys, external services, or paid inference.
- **Separate planning from evaluation:** Check proposed results independently so planning mistakes are easier to detect and test.
- **Keep a human in control:** Present proposed changes for review rather than automatically changing medication or other care schedules.
- **Acknowledge limits:** Rule-based scheduling is explainable but cannot infer every real-world care requirement or medical urgency from a short task description.

## Reliability and testing

### Verified local automated test execution

The final-project test run used:

```powershell
python -m pytest -v
```

```text
collected 23 items
========================== 23 passed in 0.54s ==========================
```

This includes **15 original PawPal tests** and **8 new planning/evaluation tests**. All 23 passed (100% of the executed test cases); this is not a claim of 100% real-world scheduling accuracy.

| New automated scenario | Observed test result |
|---|---|
| Two fixed appointments conflict | PASS — conflict flagged; no silent move |
| Flexible task alongside fixed appointment | PASS — placed in nonoverlapping slot |
| Tasks exceed daily time budget | PASS — omission reported |
| No sufficiently long free slot | PASS — task flagged for manual review |
| Invalid time window | PASS — raises `ValueError` |
| Valid nonoverlapping fixed tasks | PASS — no unnecessary revision |
| Evaluator given overlapping, over-budget plan | PASS — both violations detected |
| Completed and future tasks | PASS — excluded from today's proposal |

### Reproducible scenario results

The four CLI scenarios above demonstrate actual planning outputs. In the first, a flexible feeding task is placed at 08:20 after an 08:00 walk. In the second, a 30-minute play task is omitted when the 60-minute budget is exhausted. In the third, an unavailable 20-minute slot is flagged. In the fourth, overlapping fixed appointments are **not** silently moved.

### What has not been established

- The 23 passing tests do not constitute full Streamlit UI automation or exhaustive edge-case coverage.
- A manual end-to-end Streamlit browser check is still recommended before submission.
- Medication timing, medical urgency, multiple caregivers, persistence, and overnight tasks are outside the tested scope.
- Application logging uses Python logging for selected warnings and errors; the on-screen decision log records planning choices. Persistent audit storage is not implemented.

## Limitations and responsible use

PawPal AI is a planning aid, not a veterinary decision system. It must not recommend changing medication doses, prescribed timing, or treatment plans. Scheduling suggestions can be incomplete when the owner has not entered all constraints. Owners remain responsible for confirming care requirements and reviewing any proposed changes.

## Project reflection

Extending PawPal+ shows how a useful application can become more reliable by adding explicit planning, validation, evaluation, and explanations rather than relying on a plausible-looking output alone. The final test run confirmed that the 15 original cases still pass alongside eight new planning and evaluation cases.

**Graded AI collaboration and responsible-design reflection:** See [`model_card.md`](model_card.md). That file documents AI-assisted development, an AI suggestion accepted, one revised or rejected, limitations, and future improvements.

## Optional video walkthrough

[Loom: PawPal AI end-to-end demonstration](https://www.loom.com/share/17127e5169b048a4b36e1a084dd54c52)

This walkthrough demonstrates the integrated Streamlit planner, three planning scenarios, and automated reliability results. Reproducible input/output evidence and test results are documented above; the video is supplemental.

## Development status and next steps

- [x] Copy the Module 2 PawPal project to a dedicated final-project repository.
- [x] Preserve the original scheduling code and pass its 15 baseline tests.
- [x] Implement the planning workflow and independent evaluator.
- [x] Integrate AI-assisted care planning into Streamlit section 6.
- [x] Record four reproducible CLI input/output examples.
- [x] Run the complete suite: 23 tests passed.
- [x] Prepare a separate graded responsible-AI reflection in `model_card.md`.
- [x] Manually verify the enhanced Streamlit UI and record any findings.
- [x] Confirm the Mermaid diagram matches the committed implementation (proposal-only, no automatic save).
- [x] Commit and push the final documentation and demo files.