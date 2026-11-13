# PawPal AI — Intelligent Pet Care Planning and Reliability System

**GitHub repository:** https://github.com/ecopot-a11y/pawpal-applied-ai-final

**Project overview:** PawPal AI extends my Python/Streamlit pet-care scheduler with a rule-based planning workflow and an independent reliability evaluator. It proposes care schedules across multiple pets, checks for conflicts and time-budget violations, explains scheduling decisions, and flags tasks requiring manual review. Recommendations are proposal-only; the system does not automatically change saved appointments.

**Tools and methods:** Python, Streamlit, pytest, Git/GitHub, Mermaid, deterministic planning, input validation, explainable decision logs, and automated reliability evaluation.

**Verified testing:** 23 of 23 automated tests passed in my local pytest run, including eight new planning and evaluation tests. This result covers the tested scenarios; it is not a claim of comprehensive real-world safety or veterinary expertise.

## What this project says about me as an AI engineer

This project shows that I approach AI engineering with an emphasis on **reliability, transparency, and human oversight**. Rather than replacing a working application or adding AI for its own sake, I extended PawPal+ with a practical planning workflow, separated decision-making from independent evaluation, and verified that the new features preserved existing behavior. I also made a deliberate trade-off: the system can recommend changes, but it does not automatically apply potentially sensitive pet-care scheduling decisions. Building PawPal AI strengthened my ability to collaborate with AI tools while critically evaluating their suggestions, testing actual behavior, and clearly communicating the system's limits.

**Supporting materials in the repository:** `README.md` (setup, demo inputs/outputs, testing), `model_card.md` (limitations, ethics, AI collaboration), `diagrams/architecture.mmd` (implemented architecture), `demo_ai.py` and `sample_output.txt` (reproducible scenarios), and `tests/test_ai_planner.py` (automated tests).
