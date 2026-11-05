"""PawPal+ Streamlit interface backed by the real pet scheduler."""
from datetime import date, time

import streamlit as st
from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")
st.title("🐾 PawPal+ | Smarter Pet Scheduling")
st.caption("Plan care for multiple pets, review overlaps, and keep recurring tasks on track.")

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan", available_minutes=60)
owner = st.session_state.owner
scheduler = Scheduler(owner)

with st.sidebar:
    st.header("Owner settings")
    owner.name = st.text_input("Owner name", value=owner.name)
    owner.available_minutes = int(st.number_input(
        "Available care minutes per day", min_value=0, value=owner.available_minutes, step=5
    ))
    st.caption("Changes are kept for this browser session.")

st.subheader("1. Add a pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "bird", "other"])
    add_pet = st.form_submit_button("Add pet")
if add_pet:
    name = pet_name.strip()
    if not name:
        st.error("Enter a pet name.")
    elif any(p.name.casefold() == name.casefold() for p in owner.pets):
        st.warning("A pet with that name already exists.")
    else:
        owner.add_pet(Pet(name, species))
        st.success(f"Added {name}!")

st.subheader("2. Add a care task")
if not owner.pets:
    st.info("Add your first pet to begin scheduling tasks.")
else:
    with st.form("add_task_form", clear_on_submit=True):
        selected_pet = st.selectbox("Pet", [p.name for p in owner.pets])
        description = st.text_input("Task description", placeholder="Feed, walk, medication...")
        c1, c2, c3 = st.columns(3)
        with c1:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=1440, value=15)
            priority = st.selectbox("Priority", ["high", "medium", "low"])
        with c2:
            frequency = st.selectbox("Repeat", ["daily", "weekly", "once"])
            due_date = st.date_input("First due date", value=date.today())
        with c3:
            has_time = st.checkbox("Schedule a start time", value=True)
            start_time = st.time_input("Start time", value=time(8, 0))
        add_task = st.form_submit_button("Add task")
    if add_task:
        if not description.strip():
            st.error("Enter a task description.")
        else:
            pet = next(p for p in owner.pets if p.name == selected_pet)
            pet.add_task(Task(
                description, int(duration), frequency=frequency, priority=priority,
                time=start_time.strftime("%H:%M") if has_time else None,
                due_date=due_date,
            ))
            st.success(f"Added {description.strip()} for {pet.name}.")

st.divider()
st.subheader("3. Sorted and filtered tasks")
pet_options = ["All pets"] + [p.name for p in owner.pets]
c1, c2 = st.columns(2)
with c1:
    pet_filter = st.selectbox("Filter by pet", pet_options)
with c2:
    status_filter = st.selectbox("Filter by status", ["All", "Pending", "Completed"])

status_value = {"All": None, "Pending": False, "Completed": True}[status_filter]
matching = scheduler.filter_tasks(
    pet_name=None if pet_filter == "All pets" else pet_filter,
    completed=status_value,
)
# Preserve Scheduler.sort_by_time() ordering while applying selected filters.
matching_ids = {id(task) for _, task in matching}
sorted_filtered = [
    (pet, task) for pet, task in scheduler.sort_by_time()
    if id(task) in matching_ids
]
if sorted_filtered:
    st.table([{
        "Pet": pet.name,
        "Task": task.description,
        "Start": task.time or "Not set",
        "Minutes": task.duration_minutes,
        "Priority": task.priority,
        "Due": str(task.due_date),
        "Repeat": task.frequency,
        "Status": "Done" if task.completed else "Pending",
    } for pet, task in sorted_filtered])
else:
    st.info("No tasks match your filters.")

st.subheader("4. Complete a task")
pending = [(pet, task) for pet, task in scheduler.sort_by_time() if not task.completed]
if pending:
    # Index-based selection supports duplicate task descriptions.
    chosen = st.selectbox(
        "Select a pending task",
        range(len(pending)),
        format_func=lambda i: (
            f"{pending[i][0].name}: {pending[i][1].description} "
            f"({pending[i][1].due_date}, {pending[i][1].time or 'untimed'})"
        ),
    )
    if st.button("Mark complete"):
        pet, task = pending[chosen]
        next_task = scheduler.mark_task_complete(pet, task)
        if next_task:
            st.success(f"Completed! Next occurrence: {next_task.due_date}.")
        else:
            st.success("Task completed!")
        st.rerun()
else:
    st.info("No pending tasks to complete.")

st.divider()
st.subheader("5. Conflict warnings and daily plan")
plan_date = st.date_input("Plan date", value=date.today(), key="plan_date")
conflicts = scheduler.find_conflicts(on_date=plan_date)
if conflicts:
    st.warning(f"⚠️ {len(conflicts)} overlapping task pair(s) need your attention.")
    for warning in conflicts:
        st.warning(warning.removeprefix("WARNING: "))
    st.caption("Review the listed task times. PawPal+ does not automatically move tasks.")
else:
    st.success("No overlapping timed tasks detected for this plan date.")

if st.button("Generate daily plan", type="primary"):
    plan = scheduler.generate_schedule(on_date=plan_date)
    if not plan:
        st.info("No pending tasks fit the time budget for this date.")
    else:
        st.table([{
            "Pet": pet.name,
            "Task": task.description,
            "Start": task.time or "Not set",
            "Duration (min)": task.duration_minutes,
            "Priority": task.priority,
        } for pet, task in plan])
        st.success(f"Selected {len(plan)} task(s) using {sum(t.duration_minutes for _, t in plan)} of {owner.available_minutes} available minutes.")
        st.caption("The plan prioritizes importance and duration; it does not automatically resolve timed overlaps.")


st.divider()
st.subheader('6. AI-assisted care planning (proposal only)')
st.caption('Rule-based plan → evaluate → revise workflow. Fixed appointments are never moved automatically. Review all suggestions before editing tasks.')
from ai_planner import plan_care

if st.button('Generate validated AI care plan'):
    try:
        result = plan_care(owner, on_date=plan_date)
        if result.entries:
            st.table([{'Pet': e.pet.name, 'Task': e.task.description,
                       'Proposed start': e.start, 'Minutes': e.task.duration_minutes,
                       'Priority': e.task.priority} for e in result.entries])
        else:
            st.info('No tasks could be safely placed in the proposed plan.')
        if result.check.passed:
            st.success(f'Independent validation passed. {result.check.minutes_used} of {owner.available_minutes} minutes used; {result.revisions} scheduling revision(s).')
        if result.unplanned:
            st.warning('Unplanned tasks require owner review:')
            for note in result.unplanned:
                st.write(f'- {note}')
        with st.expander('Planning decision log'):
            for note in result.decisions:
                st.write(f'- {note}')
        st.info('This is a proposal, not an automatic update. Confirm changes yourself in the task scheduler. Do not change medication timing without veterinary guidance.')
    except ValueError as exc:
        st.error(f'Unable to plan: {exc}')
