"""Reproducible PawPal AI planning examples; run: python demo_ai.py."""
from datetime import date
from pawpal_system import Owner, Pet, Task
from ai_planner import plan_care

DAY = date(2026, 11, 5)

def scenario(title, budget, tasks, start='08:00', end='20:00'):
    owner = Owner('Jordan', budget)
    pets = {}
    for pet_name, species, description, duration, priority, when in tasks:
        if pet_name not in pets:
            pets[pet_name] = Pet(pet_name, species)
            owner.add_pet(pets[pet_name])
        pets[pet_name].add_task(Task(description, duration, priority=priority, time=when, due_date=DAY))
    result = plan_care(owner, DAY, start, end)
    print(f'=== {title} ===')
    print(f'Input: budget={budget} min, window={start}-{end}')
    for pet, task in owner.get_all_tasks():
        print(f'  {pet.name}: {task.description}, {task.duration_minutes} min, {task.priority}, time={task.time or "flexible"}')
    print('Proposed plan:')
    for entry in result.entries:
        print(f'  {entry.start} {entry.pet.name}: {entry.task.description}')
    if not result.entries:
        print('  (none)')
    print(f'Validation: {"PASS" if result.check.passed else "FAIL"}; minutes={result.check.minutes_used}/{budget}; revisions={result.revisions}')
    print('Unplanned:')
    for item in result.unplanned:
        print(f'  {item}')
    if not result.unplanned:
        print('  (none)')
    print('Decision log:')
    for item in result.decisions:
        print(f'  {item}')
    print()

if __name__ == '__main__':
    scenario('Flexible task avoids fixed appointment', 60, [
        ('Mochi', 'dog', 'Walk', 20, 'high', '08:00'),
        ('Luna', 'cat', 'Feed', 10, 'medium', None),
    ])
    scenario('Time budget omits a task', 60, [
        ('Mochi', 'dog', 'Walk', 40, 'high', None),
        ('Luna', 'cat', 'Feed', 20, 'high', None),
        ('Luna', 'cat', 'Play', 30, 'low', None),
    ])
    scenario('No free slot in planning window', 100, [
        ('Mochi', 'dog', 'Walk', 50, 'high', '08:00'),
        ('Luna', 'cat', 'Feed', 20, 'medium', None),
    ], '08:00', '09:00')
    scenario('Conflicting fixed appointments', 60, [
        ('Mochi', 'dog', 'Walk', 20, 'high', '08:00'),
        ('Luna', 'cat', 'Feed', 10, 'medium', '08:00'),
    ])
