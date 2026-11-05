"""Independent checks for a proposed PawPal care plan."""
from dataclasses import dataclass
from datetime import datetime


def minutes(hhmm: str) -> int:
    try:
        parsed = datetime.strptime(hhmm, '%H:%M')
        if len(hhmm) != 5:
            raise ValueError
    except (ValueError, TypeError):
        raise ValueError('Time must be HH:MM (24-hour).') from None
    return parsed.hour * 60 + parsed.minute


def clock(value: int) -> str:
    return f'{value // 60:02d}:{value % 60:02d}'


@dataclass(frozen=True)
class PlanCheck:
    passed: bool
    issues: tuple[str, ...]
    minutes_used: int


def evaluate_plan(owner, entries, day, window_start='08:00', window_end='20:00') -> PlanCheck:
    """Check all proposed entries, independently of the planning algorithm."""
    start, end = minutes(window_start), minutes(window_end)
    if end <= start:
        raise ValueError('Window end must be later than start.')
    issues = []
    intervals = []
    seen = set()
    total = 0
    for entry in entries:
        pet, task = entry.pet, entry.task
        key = id(task)
        if key in seen:
            issues.append(f'Duplicate task: {pet.name} / {task.description}')
        seen.add(key)
        if pet not in owner.pets or task not in pet.tasks:
            issues.append(f'Unknown task: {pet.name} / {task.description}')
        if task.completed or task.due_date > day:
            issues.append(f'Ineligible task: {pet.name} / {task.description}')
        if not isinstance(task.duration_minutes, int) or task.duration_minutes <= 0:
            issues.append(f'Invalid duration: {pet.name} / {task.description}')
            continue
        try:
            s = minutes(entry.start)
        except ValueError:
            issues.append(f'Invalid start: {pet.name} / {task.description}')
            continue
        e = s + task.duration_minutes
        if s < start or e > end:
            issues.append(f'Outside scheduling window: {pet.name} / {task.description}')
        if task.time is not None and task.time != entry.start:
            issues.append(f'Fixed time moved: {pet.name} / {task.description}')
        intervals.append((s, e, pet.name, task.description))
        total += task.duration_minutes
    intervals.sort()
    for i, (s, e, pet, name) in enumerate(intervals):
        for s2, e2, pet2, name2 in intervals[i + 1:]:
            if s2 >= e:
                break
            if s < e2:
                issues.append(f'Overlap: {pet} / {name} with {pet2} / {name2}')
    if total > owner.available_minutes:
        issues.append(f'Time budget exceeded: {total} > {owner.available_minutes} minutes')
    return PlanCheck(not issues, tuple(issues), total)
