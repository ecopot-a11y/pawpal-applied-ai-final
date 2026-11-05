"""Deterministic plan -> evaluate -> revise agent for PawPal.

No external LLM is used. Timed tasks are treated as fixed appointments and are
never moved automatically; flexible tasks can be placed into available gaps.
"""
from dataclasses import dataclass
from datetime import date
import logging

from pawpal_system import Scheduler
from reliability import clock, evaluate_plan, minutes, PlanCheck

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PlannedTask:
    pet: object
    task: object
    start: str


@dataclass(frozen=True)
class PlanningResult:
    entries: tuple[PlannedTask, ...]
    unplanned: tuple[str, ...]
    decisions: tuple[str, ...]
    check: PlanCheck
    revisions: int


def _free_slot(duration, occupied, start, end):
    cursor = start
    for left, right in sorted(occupied):
        if cursor + duration <= left:
            return cursor
        cursor = max(cursor, right)
    return cursor if cursor + duration <= end else None


def plan_care(owner, on_date=None, window_start='08:00', window_end='20:00') -> PlanningResult:
    """Plan care and verify every proposal before returning it.

    A fixed-time task that conflicts with another is flagged, not moved. Flexible
    tasks may be placed into free gaps. No original Task is modified.
    """
    day = on_date or date.today()
    begin, finish = minutes(window_start), minutes(window_end)
    if finish <= begin:
        raise ValueError('Window end must be later than start.')
    if owner.available_minutes < 0:
        raise ValueError('Available minutes cannot be negative.')
    candidates = [(pet, task) for pet, task in owner.get_all_tasks()
                  if not task.completed and task.due_date <= day]
    priority = Scheduler.PRIORITY_ORDER
    candidates.sort(key=lambda item: (priority[item[1].priority],
                                       item[1].time is None, item[1].duration_minutes))
    # Reserve all fixed appointments first, regardless of priority, to avoid
    # scheduling flexible tasks over fixed commitments.
    fixed = [(p, t) for p, t in candidates if t.time is not None]
    flexible = [(p, t) for p, t in candidates if t.time is None]
    entries, unplanned, decisions, occupied = [], [], [], []
    remaining = owner.available_minutes
    revisions = 0
    for pet, task in fixed + flexible:
        label = f'{pet.name}: {task.description}'
        duration = task.duration_minutes
        if duration <= 0:
            unplanned.append(f'{label} — invalid duration')
            continue
        if duration > remaining:
            unplanned.append(f'{label} — exceeds remaining time budget')
            logger.info('Unplanned %s: time budget', label)
            continue
        if task.time is not None:
            start = minutes(task.time)
            if start < begin or start + duration > finish:
                unplanned.append(f'{label} — fixed time outside planning window; review manually')
                continue
            if any(start < right and left < start + duration for left, right in occupied):
                unplanned.append(f'{label} — fixed-time conflict; review manually')
                logger.warning('Fixed-time conflict: %s', label)
                continue
        else:
            start = _free_slot(duration, occupied, begin, finish)
            if start is None:
                unplanned.append(f'{label} — no free slot; review manually')
                logger.warning('No free slot: %s', label)
                continue
            if start != begin:
                revisions += 1
                decisions.append(f'Revised {label} to {clock(start)} to avoid occupied time.')
        entries.append(PlannedTask(pet, task, clock(start)))
        occupied.append((start, start + duration))
        remaining -= duration
        decisions.append(f'Scheduled {label} at {clock(start)} ({task.priority} priority).')
    entries.sort(key=lambda e: e.start)
    check = evaluate_plan(owner, entries, day, window_start, window_end)
    if not check.passed:
        # Fail closed: do not present a plan that fails the independent evaluator.
        logger.error('Plan validation failed: %s', check.issues)
        unplanned.extend(f'Evaluator: {issue}' for issue in check.issues)
        entries = []
        check = evaluate_plan(owner, entries, day, window_start, window_end)
        decisions.append('Plan rejected by independent evaluator; human review required.')
    return PlanningResult(tuple(entries), tuple(unplanned), tuple(decisions), check, revisions)
