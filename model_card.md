# PawPal AI — Model Card and Responsible-AI Reflection

## 1. System Identification and Intended Use

**Final project:** PawPal AI — Intelligent Pet Care Planning and Reliability System  
**Base project:** PawPal+ (AI110 Module 2)  
**Approach:** Deterministic, rule-based scheduling workflow with independent evaluation; **not** a generative language model, fine-tuned model, or veterinary decision system.

The original PawPal+ helped owners manage multiple pets, recurring tasks, completion status, priorities, available care time, and scheduling conflicts. For the final project, I extended it with a planning component (`ai_planner.py`) and independent evaluator (`reliability.py`). The Streamlit app can display a proposed timed plan, explain scheduling choices, flag unplanned tasks, and report validation results. Proposed times are **not** automatically written back to pet-care tasks.

The intended user is a pet owner organizing routine activities. The system is **not intended** to determine medical urgency, medication doses, veterinary treatment, or whether prescribed care may safely be delayed.

## 2. What Are the Limitations or Biases in My System?

PawPal AI depends on the accuracy and completeness of owner-entered information. A missing appointment, inaccurate duration, or incorrect priority can lead to a plan that is technically valid but practically inappropriate. The system checks scheduling constraints, not the medical suitability of a care plan.

The planner prioritizes tasks using fixed rules. Higher-priority and fixed-time tasks can consume the available budget before lower-priority activities; even a low-priority task may be important to an animal's welfare. Within a priority group, shorter tasks may be favored. These design choices create a **priority and time-budget bias**, rather than a learned demographic bias. The system also assumes one owner, one daily budget, and a same-day scheduling window; it does not model travel time, multiple caregivers, emergencies, or overnight care.

A passing validation applies only to the **tasks included in the proposed plan**. Tasks left unplanned must be reviewed separately. A technically valid partial plan is not a guarantee that every pet-care need has been met.

## 3. Could My AI Be Misused, and How Would I Prevent That?

The most serious misuse would be treating PawPal's scheduling suggestions as veterinary guidance—for example, moving a prescribed medication time because a different slot appears available. Another risk is mistaking a validation `PASS` for proof that all tasks were completed or scheduled.

The current safeguards are deliberately limited and explainable:

- **Fixed-time tasks are not automatically moved.** Conflicts involving fixed appointments are flagged for owner review.
- **Flexible tasks can be placed in open slots**, but the app shows a proposal rather than silently editing the underlying records.
- **Independent checks** examine overlaps, time budget, task eligibility, scheduling window, and fixed-time preservation.
- **Unplanned tasks are displayed explicitly**, including budget and no-free-slot cases.
- **Input errors** such as invalid planning windows raise clear validation errors.

These controls reduce some scheduling risks but cannot recognize all medically sensitive tasks from a free-text description. A future version should provide explicit medication-specific warnings, privacy-conscious storage, and a clear escalation message for urgent veterinary concerns. Pet owners should confirm prescribed care requirements with a veterinarian.

## 4. What Surprised Me While Testing Reliability?

I learned that a schedule can fit within the total daily time budget and still contain overlapping appointments. That made it important to test the proposed **times**, not just the sum of task durations. I was also struck by the importance of the cases where the planner cannot find a solution: a useful system must say which task was omitted and why, rather than presenting an incomplete plan as complete.

I ran `python -m pytest -v` in my Windows virtual environment. The November 5, 2026 run reported **23 passed in 0.54 seconds**: the 15 original PawPal tests plus eight new planning/reliability tests. The new cases covered fixed-time conflicts, flexible rescheduling, budget enforcement, no free slot, invalid window, no unnecessary revision, evaluator rejection of invalid proposals, and exclusion of completed/future tasks.

All tests passing increased my confidence in these specific cases, but it does not establish perfect real-world reliability. In particular, a validated plan can still have unresolved tasks, and the Streamlit interface has not yet been documented with an automated end-to-end test.

## 5. How I Collaborated With AI During This Project

I used an AI assistant to review my original PawPal Python files, discuss a feasible final-project extension, draft modular planning and evaluation code, suggest automated scenarios, and improve the architecture and documentation. I integrated the files into VS Code and ran pytest myself to check whether the proposed changes worked with the original application.

The AI helped me move from a task-list scheduler to a proposal-and-validation workflow, but I remained responsible for choosing the scope, reviewing the design, and reporting only the test results I actually observed. I also learned to check generated documentation against the implementation: an early README still described the new agent as “pending” after the code had been implemented. I revised that description rather than leaving a misleading portfolio entry.

### AI Suggestion I Accepted — Separate Planning and Evaluation

I accepted the suggestion to keep `ai_planner.py` and `reliability.py` separate. The planner proposes times while the evaluator independently checks whether the selected entries violate constraints. This makes the code easier to inspect, test, and extend, and it prevents the planner from simply declaring its own output correct without a separate check.

### AI Suggestion I Revised — Do Not Automatically Apply Schedule Changes

I revised the broader suggestion that the system should automatically resolve conflicts and apply the revised schedule. Automatic changes could be inappropriate for fixed appointments or medication-related care. Instead, the implementation moves only **flexible tasks within a proposed plan**, flags fixed-time conflicts, and leaves changes to the owner. I also chose a deterministic workflow instead of introducing a hosted LLM, which would have increased setup cost and variability without being necessary for this assignment's scheduling goal.

This was a deliberate scope and safety decision, not evidence that all automated planning is unsafe. It made the final system easier to reproduce and aligned it with the information the application actually has.

## 6. Evaluation Summary

| Evaluation | Observed result | What it means |
|---|---|---|
| Original PawPal tests | 15/15 passed | Existing tested functionality preserved |
| New planning and reliability tests | 8/8 passed | Tested constraint-handling cases passed |
| Combined suite | 23/23 passed in 0.54 seconds | All executed automated cases passed |
| Reproducible CLI scenarios | 4 examples documented in README | Shows actual input, proposed plan, guardrail and decision output |
| Streamlit UI end-to-end automation | Not demonstrated | Requires further verification |

The evaluator's `PASS` result does not certify that omitted tasks are safe to ignore. See `README.md` for exact command examples and text-based scenario output.

## 7. Design Trade-offs and Future Improvements

The rule-based approach is transparent, reproducible, and does not require an API key, but it is less adaptable than a system with verified external care information or richer user preferences. It does not learn from outcomes or provide natural-language veterinary expertise.

Future improvements could include more explicit task constraints, multiple caregiver availability, a persistent audit log with privacy protections, UI-level automated tests, and a larger evaluation set covering edge cases. A retrieval component using vetted pet-care sources could support general informational explanations, but it should never substitute for professional veterinary guidance.

## 8. Personal Reflection

This project taught me that a useful AI-related workflow needs more than a plausible-looking recommendation. It must also check constraints, make limitations visible, and give people control over consequential decisions. The most valuable collaboration with AI was not simply generating code: it was using AI suggestions as starting points, then verifying, simplifying, and documenting the system's real behavior.
