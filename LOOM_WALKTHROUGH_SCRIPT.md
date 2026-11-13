# PawPal AI — Loom Walkthrough Transcript

**Duration:** 4–5 minutes. 
**Format:** The CLI examples are from `demo_ai.py`

## 0:00–0:35 — Introduction

**Screen:** Streamlit PawPal+ application.

**Say:** “Hello. This is PawPal AI, my Applied AI final project. I extended my earlier PawPal+ pet-care scheduler into an intelligent planning and reliability system. The original app managed pets, care tasks, priorities, recurrence, and conflict warnings. The new feature proposes schedules, evaluates their constraints, and explains when tasks need human attention. It is a deterministic, rule-based planning agent—not a large language model or veterinary advice system.”

## 0:35–1:20 — Show the integrated application

**Screen:** Point to the owner settings, pet and task forms, and section 6, **AI-assisted care planning (proposal only)**. If the app is empty, add Mochi (dog) and Luna (cat).

**Say:** “The planning feature is integrated into the actual Streamlit application. I can add pets, assign care tasks, choose priorities and times, and set my available minutes per day. When I click ‘Generate validated AI care plan,’ the app uses the current pet and task records to produce a proposed schedule. It displays the proposed start times, independent validation, unplanned tasks, and a decision log. Importantly, this is a proposal only; the app does not automatically overwrite appointments.”

## 1:20–2:10 — Scenario 1: Avoid an overlap

**Screen:** In a fresh app session, set available minutes to 60. Add Mochi’s **Walk** for 20 minutes, high priority, at **08:00**, and Luna’s **Feed** for 10 minutes, medium priority, with **Schedule a start time** unchecked. Set due dates to the plan date. Click **Generate validated AI care plan** and expand **Planning decision log**.

**Say:** “My first example is a fixed walk at eight o’clock and a flexible feeding task. The agent keeps the walk at eight and proposes feeding at eight twenty. The independent check passes: thirty of sixty available minutes are used, and the planner records one scheduling adjustment. The decision log explains why the flexible task was placed after the walk. This demonstrates actual scheduling behavior, not just a list of tasks.”

## 2:10–2:55 — Scenario 2: Enforce the time budget

**Screen:** Show the `python demo_ai.py` terminal output for **Time budget omits a task**. This script creates a fresh scenario so earlier app tasks do not affect the results.

**Say:** “Next, the owner has sixty minutes available, but three tasks require ninety minutes: a forty-minute walk, a twenty-minute feeding, and thirty minutes of play. The agent schedules the two high-priority tasks, using all sixty minutes. It explicitly lists ‘Luna: Play — exceeds remaining time budget’ as unplanned. The evaluator passes the selected proposal, but that does not mean every requested task was completed. The owner still needs to review the omitted task.”

## 2:55–3:35 — Scenario 3: Fixed-time conflict guardrail

**Screen:** Show the `python demo_ai.py` output for **Conflicting fixed appointments**.

**Say:** “In the third case, Mochi’s twenty-minute walk and Luna’s ten-minute feeding are both fixed at eight o’clock. The planner does not silently move either fixed appointment. It includes the walk and flags the feeding as an unplanned fixed-time conflict requiring manual review. This is an important safety boundary, especially for care tasks where timing matters. The validation passes only for the selected proposal, while the unresolved conflict is clearly reported.”

## 3:35–4:15 — Automated reliability evidence

**Screen:** Show the saved pytest output or run `python -m pytest -v`.

**Say:** “I tested the original scheduling features and the new planning and evaluation behavior. My verified test run reported twenty-three tests passed in 0.54 seconds: fifteen original tests and eight new planning tests. The new tests cover fixed-time conflicts, flexible rescheduling, budget enforcement, unavailable slots, invalid windows, clean plans, evaluator detection of overlap and budget violations, and exclusion of completed or future tasks. Passing these tests supports reliability for the scenarios tested, but it does not prove that every real-world care situation is covered.”

## 4:15–4:55 — Ethics, learning, and close

**Screen:** Return to the Streamlit proposal-only section, then optionally show the README’s sample interaction and reliability table.

**Say:** “The most important lesson I learned is that a plausible schedule is not necessarily a valid schedule. Planning and independent evaluation should be separate. I accepted AI assistance with that separation, but revised the idea of automatic rescheduling so fixed-time commitments remain under human control. PawPal AI is not veterinary advice, and owners must review recommendations before making changes. My README includes the reproducible commands, input and output examples, and guardrail results used for grading. Thank you for watching.”

## Recording notes

- `demo_ai.py` produces four independent CLI scenarios and can be used to display examples 2 and 3 without resetting the app’s session state.
- For a current-day browser demo, choose the same **First due date** and **Plan date**; otherwise tasks may be filtered out.

## Add the Loom link to README.md after recording

```markdown
## Optional video walkthrough

[Loom: PawPal AI end-to-end demonstration](PASTE_YOUR_ACTUAL_LOOM_SHARE_URL_HERE)

This optional walkthrough demonstrates the integrated Streamlit planner, three planning scenarios, and automated reliability results. Reproducible input/output evidence and test results are documented above; the video is supplemental.
```
