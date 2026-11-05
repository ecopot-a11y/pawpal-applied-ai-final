# PawPal AI — Intelligent Pet Care Planning and Reliability System

**Status:** In development — original PawPal+ application verified; AI planning extension pending implementation and evaluation.

## Project summary

PawPal AI is an extension of **PawPal+**, my Module 2 AI110 project. It aims to help pet owners coordinate care across multiple pets by proposing practical schedules, checking constraints, explaining scheduling decisions, and identifying tasks that need human attention.

The project emphasizes **reliable, explainable planning**: a proposed schedule should be checked before a pet owner relies on it. The intended AI extension uses a multi-step, rule-based planning agent with an evaluate-and-revise loop, rather than a hosted language model.

## Original project: PawPal+ (Module 2)

PawPal+ was a Python and Streamlit pet-care scheduling application designed to organize care tasks for multiple pets. It allowed owners to add pets and tasks, assign priorities and recurrence schedules, track completion, generate daily task lists within a time budget, detect overlapping tasks, and find available time slots. The original system warned about conflicts but did not automatically produce and validate a revised, conflict-free schedule.

Original project: [AI110 Module 2 PawPal starter](https://github.com/ecopot-a11y/ai110-module2show-pawpal-starter)

## What the final project adds

**Planned integrated extension (not yet implemented):**

1. **Planning agent:** Build a proposed timed care schedule from the owner's pets, tasks, priorities, available minutes, and scheduling window.
2. **Evaluate-and-revise loop:** Detect overlapping proposed tasks, time-budget violations, and unscheduled tasks; attempt a bounded revision when possible.
3. **Reliability guardrails:** Validate input and scheduling constraints; flag tasks that cannot be scheduled rather than silently omitting them or claiming success.
4. **Explainability and owner oversight:** Explain the resulting plan and unresolved trade-offs; present proposed changes for owner review before applying them.
5. **Scenario-based evaluation:** Test the integrated workflow with reproducible cases and record what passed or failed.

The extension must be integrated into the Streamlit application, not run only as a standalone demo.

## Architecture overview

Mermaid source: [`diagrams/architecture.mmd`](diagrams/architecture.mmd).

The **target architecture** follows this flow:

1. The pet owner enters tasks and planning preferences through Streamlit (`app.py`).
2. Input validation checks the request before planning.
3. The system retrieves the in-memory `Owner`, `Pet`, and `Task` records managed by `pawpal_system.py`.
4. A planning agent proposes task times.
5. An evaluator checks conflicts, time budget, and omissions; the planner revises fixable issues within a bounded loop.
6. The app displays an explanation, unresolved issues, and a proposed plan for human review.
7. Automated tests exercise validation, planning, and evaluation.

**Architecture status:** This describes the intended final design. Update the Mermaid source and this section to match the actual implementation before final submission.

## Technology

- Python 3.13 (tested locally with Python 3.13.7)
- Streamlit user interface
- Pytest automated testing
- Git and GitHub version control
- Mermaid architecture diagram

The planned planning agent is a **rule-based agentic workflow**, not a fine-tuned model or an LLM. It should not be described as providing veterinary diagnosis or medical advice.

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

### 4. Run the existing PawPal+ interface

```powershell
python -m streamlit run app.py
```

The interface currently supports pet/task management, recurrence, conflict warnings, and daily task selection. **The new AI planning interface will be documented here after implementation.**

### 5. Run the original command-line demonstration

```powershell
python main.py
```

### 6. Run automated tests

```powershell
python -m pytest -v
```

**Verified baseline:** 15 tests passed in 1.71 seconds on Windows with Python 3.13.7. This result covers the original project and does **not** verify the planned agent or evaluator.

## Sample interactions

The following are **planned acceptance scenarios**, not recorded outputs of a finished AI system. Replace each expected result with an actual captured run after implementing the extension.

### Scenario 1: Overlapping care tasks

**Input:** Two pending tasks are scheduled for 08:00, each requiring 15 minutes, with enough room later in the scheduling window.

**Expected behavior:** Identify the overlap, propose a non-overlapping alternative, recheck the schedule, and explain the change. If the time is fixed or no acceptable slot exists, flag the conflict for human review.

**Actual output:** _To be captured after implementation._

### Scenario 2: More tasks than the daily time budget

**Input:** An owner has 30 available minutes, but pending tasks require 50 minutes in total.

**Expected behavior:** Produce a plan that respects the 30-minute budget, explain task selection, and explicitly list tasks that could not fit.

**Actual output:** _To be captured after implementation._

### Scenario 3: No available slot

**Input:** A 20-minute task must fit inside a scheduling window with only 10 free minutes.

**Expected behavior:** Report that no suitable slot exists; do not claim the task was scheduled; request owner review.

**Actual output:** _To be captured after implementation._

## Design decisions and trade-offs

- **Reuse tested scheduling code:** Build around the existing `Scheduler` instead of replacing functioning recurrence, conflict detection, and task management.
- **Prefer reproducibility:** Use a deterministic, rule-based planning agent without requiring API keys, external services, or paid inference.
- **Separate planning from evaluation:** Check proposed results independently so planning mistakes are easier to detect and test.
- **Keep a human in control:** Present proposed changes for review rather than automatically changing medication or other care schedules.
- **Acknowledge limits:** Rule-based scheduling is explainable but cannot infer every real-world care requirement or medical urgency from a short task description.

## Reliability and testing

### Verified baseline

On the copied PawPal project, the following command completed successfully:

```powershell
python -m pytest -v
```

```text
collected 15 items
========================== 15 passed in 1.71s ==========================
```

The baseline tests cover recurrence, overlap detection, available-slot calculations, and basic task operations.

### Planned extension evaluation

Before final submission, add tests for:

- Detecting and revising fixable overlaps.
- Respecting the owner's daily time budget.
- Reporting tasks that cannot be scheduled.
- Rejecting invalid inputs without crashing.
- Producing consistent plans for identical inputs.
- Avoiding unintended changes to existing tasks before owner approval.

Record actual test results and at least two or three **real input/output examples** here. Report failures and unresolved edge cases honestly.

## Limitations and responsible use

PawPal AI is a planning aid, not a veterinary decision system. It must not recommend changing medication doses, prescribed timing, or treatment plans. Scheduling suggestions can be incomplete when the owner has not entered all constraints. Owners remain responsible for confirming care requirements and reviewing any proposed changes.

## Project reflection

Extending PawPal+ shows how a useful application can become more reliable by adding explicit planning, validation, evaluation, and explanations rather than relying on a plausible-looking output alone. The baseline testing also demonstrates the value of preserving working behavior before introducing more complex features.

**Graded AI collaboration and responsible-design reflection:** See [`model_card.md`](model_card.md) once it has been created and completed. That file will document AI-assisted development, an AI suggestion accepted, one revised or rejected, limitations, and future improvements.

## Development status and next steps

- [x] Copy the Module 2 PawPal project to a dedicated final-project repository.
- [x] Confirm the original 15 automated tests pass.
- [ ] Implement and integrate the planning agent.
- [ ] Implement independent evaluation and guardrails.
- [ ] Update `diagrams/architecture.mmd` to reflect the finished code.
- [ ] Capture three real end-to-end sample interactions.
- [ ] Run and document extension tests.
- [ ] Complete `model_card.md` and final portfolio review.
