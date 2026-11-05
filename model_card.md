# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial UML design included four classes: `Owner`, `Pet`, `CareTask`, and `Scheduler`. The owner stored basic information and available care time, each pet held its own care tasks, and each task described an activity with a duration and priority. The scheduler was responsible for selecting tasks that fit the owner's time budget and explaining the resulting daily plan. This separation gave me a starting point for organizing the application.

**b. Design changes**

During implementation, `CareTask` became `Task` and gained a start time, due date, frequency, and completion status. I changed `Scheduler` to receive an `Owner` object and retrieve `(Pet, Task)` pairs through `Owner.get_all_tasks()`, allowing it to plan care for multiple pets. I also added sorting, filtering, overlapping-time conflict detection, and recurring-task methods. I revised the Mermaid UML diagram to reflect the final classes and their relationships.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The daily scheduler considers whether a task is unfinished and due, its priority, its duration, and the owner's available minutes. It sorts eligible tasks by priority (high before medium before low), then by shorter duration within the same priority level, and selects tasks that fit the remaining budget. Separate methods sort tasks chronologically, filter them by pet or completion status, and identify overlapping timed activities. I prioritized completion status, due dates, and the owner's time limit so that the plan would be manageable rather than simply listing every task.

**b. Tradeoffs**

One tradeoff is that `Scheduler.find_conflicts()` warns about overlapping activities but does not automatically reschedule them. For example, a walk that starts at 8:00 AM and lasts 20 minutes conflicts with a feeding scheduled for 8:10 AM. The app displays a warning and leaves the decision to the owner. I chose this approach because some care activities, particularly medication and feeding, may have important timing requirements that an automatic change could overlook. It keeps the logic simpler and the owner in control. The priority-based daily planner also does not guarantee a conflict-free timetable; the conflict warnings are a separate check.

---

## 3. AI Collaboration

**a. How you used AI**

I used Claude as a coding assistant for UML planning, drafting Python classes, building scheduler methods, adding docstrings, writing pytest tests, troubleshooting errors, and connecting the backend to Streamlit. The most useful features were generating small, targeted code changes, explaining how methods interact, and interpreting terminal output. Specific prompts such as “How could this algorithm be simplified for better readability or performance?” helped me evaluate the code instead of accepting it automatically. Keeping separate chat sessions or focused conversations for design, algorithms, testing, and UI work helped me keep each phase's requirements and decisions organized, although I still had to check that later changes matched the actual project files.

**b. Judgment and verification**

When reviewing the conflict detection algorithm, AI suggested that `itertools.combinations()` could shorten the code used to compare pairs of tasks. I chose to keep the existing sorted nested loops because they are easier for me to follow and can stop checking once later tasks start after the current task ends. I also learned to distinguish application bugs from setup problems: pytest initially reported an import-file mismatch because duplicate `test_pawpal.py` files existed in different folders. Removing the duplicate resolved the collection error without changing the scheduler logic. I verified the system through the CLI demonstration and automated tests rather than assuming that generated code was correct.

---

## 4. Testing and Verification

**a. What you tested**

I used `python -m pytest -v` to test basic task completion and addition, chronological sorting, daily and weekly recurrence, one-time tasks that should not recur, and several conflict-detection cases. The conflict tests covered tasks beginning at the same time, partially overlapping tasks, and situations that should not generate warnings, such as adjacent, completed, future-dated, or untimed tasks. These tests matter because they check both expected behavior and conditions that could produce confusing or incorrect schedules. My final shared terminal run reported **9 passed in 0.32 seconds**, with no failures or errors.

**b. Confidence**

My confidence level is **★★★★☆ (4 out of 5 stars)**. All nine automated tests passed, which gives me confidence in the main scheduling algorithms. I would not give five stars yet because I have not completed automated end-to-end tests of the Streamlit interface, and I would like to test more complex cases such as tasks that extend past midnight, a large number of overlapping activities, and how overdue recurring tasks should appear in a selected day's plan.

---

## 5. Reflection

**a. What went well**

I am most satisfied with turning a basic pet-task project into a multi-pet scheduling system with visible, useful features. The owner can add pets and tasks, choose start times and recurrence, view sorted or filtered tasks, and see conflict warnings in the Streamlit interface. The backend and UI now share the same `Owner`, `Pet`, `Task`, and `Scheduler` design, which makes the system easier to understand and maintain.

**b. What you would improve**

In another iteration, I would add an option to edit existing tasks directly in the UI, improve handling of overnight and overdue activities, and consider suggesting alternative times for conflicts without changing them automatically. I would also add more automated tests for the Streamlit workflow and save task data so it persists beyond the current browser session. These improvements would make the application more practical while keeping the scheduling rules understandable.

**c. Key takeaway**

My biggest lesson is that being the **lead architect** means I remain responsible for the system's design and behavior, even when AI can produce code quickly. AI was valuable for suggesting implementations, explaining errors, and accelerating documentation, but I still needed to decide which features belonged in the project, choose between alternative algorithms, and verify results. Good collaboration with AI means asking specific questions, checking the output against the requirements, and making deliberate design decisions rather than accepting every suggestion as-is.
