# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

PawPal+ was originally designed to help pet owners manage daily care activities for multiple pets. It supported task scheduling, priorities, recurring activities, conflict detection, and time management.

For my final project, I extended PawPal+ by adding an AI-inspired, rule-based planning agent and a reliability evaluator. The enhanced system proposes care schedules, checks for conflicts, adjusts flexible tasks when possible, enforces available time limits, and explains scheduling decisions.

The system uses a deterministic planning workflow rather than a large language model.

**b. Limitations and Potential Biases**

One limitation of PawPal AI is that its recommendations depend on the information entered by the pet owner. If the owner provides inaccurate task durations, priorities, or scheduling requirements, the resulting plan may not reflect the pet's actual needs.

The system also relies on predefined scheduling rules rather than understanding each animal's individual health, behavior, or medical requirements. For example, it cannot determine whether a medication should be administered at a different time or whether a pet requires additional care based on its health condition.

Another potential bias comes from how tasks are prioritized. The scheduling algorithm gives preference to tasks marked as high priority and considers available time. This may disadvantage activities labeled as lower priority, even when those activities contribute to a pet's long-term well-being.

The system also assumes that the owner has a predictable daily schedule. Owners with irregular work hours, multiple caregivers, or unexpected responsibilities may find some recommendations less useful.

To address these limitations, PawPal AI explains its decisions, identifies tasks that cannot be scheduled, and allows the owner to review the proposed plan rather than treating the system's recommendations as automatically correct.

**c. Potential Misuse and Prevention**

PawPal AI could be misused if someone treated its scheduling recommendations as veterinary or medical advice.

For example, a pet owner might assume that an automatically generated schedule is appropriate for administering medication or managing a serious health condition. However, PawPal AI does not have the clinical knowledge necessary to make those decisions.

To reduce this risk, the system does not automatically move fixed-time appointments. It flags conflicts that require human attention instead of silently changing potentially important care times.

The application also uses input validation and an independent reliability evaluator to identify scheduling problems before presenting recommendations.

Another concern is that users might rely too heavily on the system and overlook tasks that could not fit within their available time. PawPal AI addresses this by reporting omitted or unresolved tasks rather than implying that every care requirement has been satisfied.

In future versions, I would add clearer medication-specific warnings, privacy protections for stored pet information, and additional checks for tasks that require professional veterinary guidance.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The daily scheduler considers whether a task is unfinished and due, its priority, its duration, and the owner's available minutes. It sorts eligible tasks by priority (high before medium before low), then by shorter duration within the same priority level, and selects tasks that fit the remaining budget. Separate methods sort tasks chronologically, filter them by pet or completion status, and identify overlapping timed activities. I prioritized completion status, due dates, and the owner's time limit so that the plan would be manageable rather than simply listing every task.

**b. Tradeoffs**

One tradeoff is that `Scheduler.find_conflicts()` warns about overlapping activities but does not automatically reschedule them. For example, a walk that starts at 8:00 AM and lasts 20 minutes conflicts with a feeding scheduled for 8:10 AM. The app displays a warning and leaves the decision to the owner. I chose this approach because some care activities, particularly medication and feeding, may have important timing requirements that an automatic change could overlook. It keeps the logic simpler and the owner in control. The priority-based daily planner also does not guarantee a conflict-free timetable; the conflict warnings are a separate check.

---

## 3. AI Collaboration

**a. How you used AI**

I used Claude as a development partner throughout the project, particularly for system design, code generation, debugging support, testing strategy, and documentation.

I began by providing the original PawPal Python files so the AI could examine the existing scheduling logic. This was important because I wanted the final project to extend the working application rather than replace it with an unrelated demonstration.

AI helped identify an opportunity to improve PawPal by introducing a planning workflow that could generate proposed schedules, evaluate constraints, and revise flexible tasks.

The AI also helped create the planning and reliability modules, develop additional automated tests, and organize the architecture diagram.

I then integrated the generated files into my local VS Code project and used pytest to verify the implementation. The complete suite passed all 23 tests, including the original 15 tests.

This collaboration demonstrated that AI can accelerate development, but the developer still needs to understand the code, evaluate its design, and independently verify its behavior.

**b. Judgment and verification**

One AI suggestion I accepted was to separate the planning agent from the reliability evaluator.

Instead of relying on one function to generate a schedule and declare it correct, the system uses separate components to propose scheduling decisions and check whether those decisions satisfy important constraints.

I accepted this suggestion because it made the system more modular, easier to test, and more trustworthy.

It also supported the final project's requirement to demonstrate a meaningful AI feature integrated into the application's main workflow.

One suggestion I revised was the broader idea of allowing the planning agent to automatically resolve scheduling conflicts and apply the resulting changes.

Although fully automatic rescheduling could make the application more convenient, I decided that the system should distinguish flexible activities from fixed-time care requirements.

For example, moving a playtime activity may be reasonable, but automatically changing a medication-related appointment could create unnecessary risk.

I therefore limited the planning workflow to proposing adjustments for flexible tasks while flagging fixed-time conflicts for human review. I also kept the new workflow deterministic rather than introducing an external language-model API, which would have added cost, setup complexity, and less predictable behavior.

This decision made the project easier to reproduce and aligned its capabilities more closely with the needs of a responsible pet-care application.

---

## 4. Testing and Verification

**a. What you tested**

I used `python -m pytest -v` to test basic task completion and addition, chronological sorting, daily and weekly recurrence, one-time tasks that should not recur, and several conflict-detection cases. The conflict tests covered tasks beginning at the same time, partially overlapping tasks, and situations that should not generate warnings, such as adjacent, completed, future-dated, or untimed tasks. These tests matter because they check both expected behavior and conditions that could produce confusing or incorrect schedules. My final shared terminal run reported **9 passed in 0.32 seconds**, with no failures or errors.

**b. Confidence**

My confidence level is **★★★★☆ (4 out of 5 stars)**. All nine automated tests passed, which gives me confidence in the main scheduling algorithms. I would not give five stars yet because I have not completed automated end-to-end tests of the Streamlit interface, and I would like to test more complex cases such as tasks that extend past midnight, a large number of overlapping activities, and how overdue recurring tasks should appear in a selected day's plan.

---

## 5. Reflection

**a. What suprised you during testing**

One of the most interesting findings was that a scheduling system could produce a plan that appeared reasonable while still violating important constraints.

For example, simply selecting high-priority tasks does not guarantee that their scheduled times will avoid conflicts. A task list can fit within the owner's total available minutes while still containing overlapping appointments.

This helped me understand why generating a plan and validating that plan should be separate steps.

I was also surprised by the importance of testing situations where the system cannot find a satisfactory solution. Instead of forcing every task into the schedule, PawPal AI must recognize when no available time slot exists and report that limitation.

After integrating the new planning and reliability components, I ran the complete automated test suite. All 23 tests passed, including eight tests covering the new planning and validation functionality.

These tests verified conflict detection, flexible-task rescheduling, time-budget enforcement, unavailable scheduling slots, invalid scheduling windows, and independent evaluation of proposed schedules.

The results increased my confidence in the implementation, while also reminding me that passing automated tests does not guarantee that the system will handle every real-world situation correctly.

**b. What you would improve**

If I continued developing PawPal AI, I would focus on improving personalization and reliability.

Potential improvements include integrating verified pet-care reference information, supporting multiple caregivers, adding more flexible scheduling preferences, and evaluating the system against a larger collection of realistic scenarios.

I would also explore adding a retrieval-augmented assistant that could provide general pet-care information from reliable sources while clearly separating informational guidance from veterinary recommendations.

Before implementing such features, I would evaluate their accuracy, privacy implications, and potential risks.

**c. Key takeaway**

The most important lesson I learned from this project is that building a useful AI system requires more than generating an answer or recommendation.

A reliable system must also validate inputs, evaluate its decisions, communicate uncertainty or limitations, and give people appropriate control over the final outcome.

PawPal AI helped me connect the concepts from earlier course modules—including Python debugging, modular design, planning, testing, and responsible AI—into a working application.

The project also reinforced the importance of human oversight. AI can help generate and evaluate plans, but the final responsibility for pet-care decisions should remain with the owner and, when appropriate, a veterinary professional.
