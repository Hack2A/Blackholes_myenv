from tasks.easy import EASY_TASK
from tasks.medium import MEDIUM_TASK
from tasks.hard import HARD_TASK

TASK_REGISTRY = {
    "easy": EASY_TASK,
    "medium": MEDIUM_TASK,
    "hard": HARD_TASK,
}


def get_task(task_id: str) -> dict:
    return TASK_REGISTRY.get(task_id, EASY_TASK)


def list_tasks() -> list[str]:
    return list(TASK_REGISTRY.keys())
