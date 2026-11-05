from datetime import date
from pawpal_system import Owner, Pet, Task
from ai_planner import plan_care
from reliability import evaluate_plan
import pytest

DAY = date(2026, 11, 5)


def make_owner(budget=60):
    owner = Owner('Jordan', budget)
    dog = Pet('Mochi', 'dog')
    cat = Pet('Luna', 'cat')
    owner.add_pet(dog)
    owner.add_pet(cat)
    return owner, dog, cat


def add(pet, description, duration, priority='medium', time=None):
    task = Task(description, duration, priority=priority, time=time, due_date=DAY)
    pet.add_task(task)
    return task


def test_two_fixed_appointments_conflict_and_are_flagged():
    owner, dog, cat = make_owner()
    add(dog, 'Walk', 20, time='08:00')
    add(cat, 'Feed', 10, time='08:00')
    result = plan_care(owner, DAY)
    assert result.check.passed
    assert len(result.entries) == 1
    assert any('fixed-time conflict' in s for s in result.unplanned)


def test_flexible_task_is_revised_around_fixed_appointment():
    owner, dog, cat = make_owner()
    add(dog, 'Walk', 20, time='08:00')
    add(cat, 'Feed', 10)
    result = plan_care(owner, DAY)
    assert result.check.passed
    assert [(e.task.description, e.start) for e in result.entries] == [('Walk', '08:00'), ('Feed', '08:20')]
    assert result.revisions == 1


def test_budget_is_enforced_and_omissions_reported():
    owner, dog, cat = make_owner(60)
    add(dog, 'Walk', 40, priority='high')
    add(cat, 'Play', 30, priority='low')
    add(cat, 'Feed', 20, priority='high')
    result = plan_care(owner, DAY)
    assert result.check.passed
    assert result.check.minutes_used == 60
    assert len(result.unplanned) == 1


def test_no_free_slot_is_reported():
    owner, dog, cat = make_owner(100)
    add(dog, 'Walk', 50, time='08:00')
    add(cat, 'Feed', 20)
    result = plan_care(owner, DAY, '08:00', '09:00')
    assert result.check.passed
    assert len(result.entries) == 1
    assert any('no free slot' in s for s in result.unplanned)


def test_invalid_window_rejected():
    owner, _, _ = make_owner()
    with pytest.raises(ValueError):
        plan_care(owner, DAY, '20:00', '08:00')


def test_clean_plan_requires_no_revision():
    owner, dog, cat = make_owner()
    add(dog, 'Walk', 20, time='08:00')
    add(cat, 'Feed', 10, time='09:00')
    result = plan_care(owner, DAY)
    assert result.check.passed and result.revisions == 0
    assert not result.unplanned


def test_evaluator_rejects_overlap_and_budget_overrun():
    from ai_planner import PlannedTask
    owner, dog, cat = make_owner(25)
    t1 = add(dog, 'Walk', 20)
    t2 = add(cat, 'Feed', 20)
    check = evaluate_plan(owner, [PlannedTask(dog, t1, '08:00'), PlannedTask(cat, t2, '08:10')], DAY)
    assert not check.passed
    assert any('Overlap' in issue for issue in check.issues)
    assert any('budget' in issue for issue in check.issues)


def test_future_and_completed_tasks_excluded():
    owner, dog, cat = make_owner()
    past = add(dog, 'Done', 10)
    past.mark_complete()
    cat.add_task(Task('Future', 10, due_date=date(2026, 11, 6)))
    result = plan_care(owner, DAY)
    assert not result.entries and result.check.passed
