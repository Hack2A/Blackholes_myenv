from tasks.graders import (
    grade_scoring_accuracy,
    grade_topic_detection,
    grade_follow_up_relevance,
    grade_weak_topic_detection,
)


def compute_step_reward(
    action: dict,
    ground_truth: dict,
    round_number: int,
    max_rounds: int,
    task_config: dict,
) -> float:
    reward = 0.0

    scoring_grade = grade_scoring_accuracy(
        action.get("evaluation_score", 0),
        ground_truth.get("quality_score", 5),
    )
    reward += 0.3 * scoring_grade

    expected_topics = [ground_truth.get("topic", "")]
    if expected_topics == [""]:
        expected_topics = []
    topic_grade = grade_topic_detection(
        action.get("detected_topics", []),
        expected_topics,
    )
    reward += 0.2 * topic_grade

    expected_weak = task_config.get("weak_topics", [])
    weak_grade = grade_weak_topic_detection(
        action.get("weak_topics", []),
        expected_weak,
    )
    reward += 0.1 * weak_grade

    if round_number < max_rounds:
        follow_up_grade = grade_follow_up_relevance(
            action.get("next_question", ""),
            action.get("weak_topics", expected_weak),
        )
        reward += 0.2 * follow_up_grade
    else:
        reward += 0.2 * 0.5

    feedback = action.get("feedback", "")
    if len(feedback) > 50:
        reward += 0.1
    elif len(feedback) > 20:
        reward += 0.05

    decision = action.get("final_decision", "continue")
    if round_number < max_rounds:
        if decision == "continue":
            reward += 0.1
        else:
            reward -= 0.1
    else:
        expected_decision = task_config.get("expected_final_decision", "continue")
        if decision == expected_decision:
            reward += 0.2
        else:
            reward -= 0.1

    return round(max(0.0, min(1.0, reward)), 4)


def compute_final_bonus(task_grade: float) -> float:
    return round(task_grade * 0.5, 4)
