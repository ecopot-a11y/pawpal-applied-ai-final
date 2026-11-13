# PawPal AI — Final Project Presentation

**Target speaking time:** approximately 6 minutes (5–7 minutes including a brief live demonstration).  
**Project:** PawPal AI: Intelligent Pet Care Planning and Reliability System  
**Code:** https://github.com/ecopot-a11y/pawpal-applied-ai-final

## 0:00–0:45 — Introduction: The problem

Hello. My final project is **PawPal AI**, an intelligent pet-care planning and reliability system. Pet owners often have several responsibilities to manage: feeding, walking, medication reminders, grooming, and playtime. These tasks may overlap, and the owner may not have enough time to complete everything on a given day.

My goal was to create something more useful than a simple checklist: a system that proposes a realistic care schedule, explains its choices, and clearly identifies what it could not schedule.

## 0:45–1:35 — Starting point and what I built

I started with my earlier Module 2 project, **PawPal+**, built in Python and Streamlit. That version supported multiple pets, task priorities, recurring tasks, completion tracking, time budgets, conflict warnings, and finding open time slots. But it did not independently validate a newly proposed timetable.

For the final project, I extended the existing code rather than starting over. I added a rule-based planning agent in `ai_planner.py` and a separate evaluator in `reliability.py`. The Streamlit application now includes an AI-assisted planning section. The result is an integrated, deterministic planning workflow—not a chatbot, a generative language model, or a veterinary expert.

## 1:35–2:25 — How the system works

First, the owner enters pets and care tasks, including their durations, priorities, due dates, and optional fixed times. The planner considers the owner's available minutes and selected planning window.

It places eligible fixed-time tasks when possible, assigns flexible tasks to open slots, and records why tasks were scheduled or left out. The independent evaluator then checks the proposed schedule for overlapping appointments and time-budget violations. If the proposal fails validation, it is not presented as a valid plan.

The system is deliberately **proposal-only**. It displays recommendations and unresolved tasks, but does not automatically overwrite the original appointments. This is especially important because a fixed-time activity might be medically significant.

## 2:25–4:10 — Demonstration: Three real examples

**Demo setup:** Open the Streamlit interface with `python -m streamlit run app.py`, then show section **AI-assisted care planning**. Alternatively, run `python demo_ai.py` to reproduce the text-based scenarios in `sample_output.txt`. The outputs below are from the recorded demonstration, not invented examples.

**Example 1 — Avoiding an overlap.** With a 60-minute budget, Mochi has a 20-minute walk fixed at 08:00 and Luna has a flexible 10-minute feeding task. The planner schedules the walk at **08:00** and feeding at **08:20**. Validation passes, using **30 of 60 minutes**, and the decision log records one scheduling adjustment. This demonstrates how a flexible task can fit around a fixed commitment.

**Example 2 — Respecting a limited budget.** The owner has 60 minutes, but tasks require 90 minutes in total: a 40-minute walk, a 20-minute feeding, and 30 minutes of play. The proposed plan includes feeding at **08:00** and the walk at **08:20**, totaling **60 of 60 minutes**. Playtime is explicitly marked **unplanned because it exceeds the remaining time budget**. The evaluator passes the proposed schedule, but that does not mean every requested task was completed.

**Example 3 — Recognizing an unsolvable conflict.** Two fixed-time tasks both begin at **08:00**. The planner includes the 20-minute walk but flags the 10-minute feeding task as **a fixed-time conflict requiring manual review**. It does not quietly move the fixed appointment or claim that both tasks fit.

These examples show the system's most important behavior: it can say **no**, explain why, and leave the final decision to the owner.

## 4:10–5:05 — Reliability and evaluation

I tested the project with `python -m pytest -v`. My local terminal reported **23 tests passed in 0.54 seconds** using Python 3.13.7. That includes **15 existing tests** and **8 new tests** covering the planning and evaluation features.

The new tests check fixed-time conflicts, flexible-task adjustments, budget limits, unavailable slots, invalid planning windows, clean schedules, evaluator rejection of overlaps and budget overruns, and exclusion of completed or future tasks.

A lesson from this testing was that a schedule can look reasonable but still be wrong. A list of high-priority tasks might fit a time budget yet contain overlapping appointments. Separating plan generation from evaluation made these mistakes easier to detect. I also learned that a validation pass means the *proposed plan* satisfies the checked constraints; any unplanned tasks still require attention.

## 5:05–5:50 — Responsible AI and my engineering choices

The biggest limitation is that PawPal AI only knows the information entered by the owner. It cannot assess an animal's health, determine medication timing, or provide veterinary advice. Its priority rules can also favor some tasks over others, and a deterministic planner cannot anticipate every real-world interruption.

I used AI as a coding and design collaborator. One suggestion I **accepted** was separating the planner from an independent evaluator. One suggestion I **revised** was fully automatic conflict resolution and application of schedule changes. I kept fixed-time conflicts visible for human review and made the interface proposal-only, because convenience should not override safety or user control.

## 5:50–6:15 — Conclusion

PawPal AI shows how I approach AI engineering: build on working software, define the limits of automation, test the behavior, and make the system's decisions understandable. My proudest outcome is not just that the tests passed; it is that the application reports what it **cannot** safely schedule instead of presenting a misleadingly complete plan.

Thank you. The repository contains the source code, reproducible demonstrations, architecture diagram, reliability tests, README, and responsible-AI model card.

---

### Presenter checklist

- Open the repository and point to `app.py`, `ai_planner.py`, `reliability.py`, and `diagrams/architecture.mmd`.
- Run `python demo_ai.py` or show the Streamlit planning section.
- Highlight a scheduled task, an unplanned task, and the validation/decision log.
- Show the saved `python -m pytest -v` result: **23 passed in 0.54s**.
- Do **not** describe the application as automatically saving or approving proposed changes.
