from tasks.dataset import QUESTION_BANK, TOPIC_LIST


def grade_scoring_accuracy(agent_score: float, ground_truth_score: float) -> float:
    diff = abs(agent_score - ground_truth_score)
    if diff <= 1.0:
        return 1.0
    if diff <= 2.0:
        return 0.8
    if diff <= 3.0:
        return 0.5
    if diff <= 4.0:
        return 0.2
    return 0.0


def grade_topic_detection(detected: list[str], expected: list[str]) -> float:
    if not expected and not detected:
        return 1.0
    if not expected or not detected:
        return 0.0
    detected_set = set(t.lower().strip() for t in detected)
    expected_set = set(t.lower().strip() for t in expected)
    intersection = detected_set & expected_set
    union = detected_set | expected_set
    if not union:
        return 1.0
    return len(intersection) / len(union)


def grade_weak_topic_detection(detected_weak: list[str], expected_weak: list[str]) -> float:
    if not expected_weak and not detected_weak:
        return 1.0
    if not expected_weak:
        return 0.5
    if not detected_weak:
        return 0.0
    detected_set = set(t.lower().strip() for t in detected_weak)
    expected_set = set(t.lower().strip() for t in expected_weak)
    hits = len(detected_set & expected_set)
    return min(1.0, hits / len(expected_set))


def grade_follow_up_relevance(next_question: str, weak_topics: list[str]) -> float:
    if not next_question:
        return 0.0
    if not weak_topics:
        return 0.5
    next_q_lower = next_question.lower()
    topic_keywords = {
        "python_basics": ["python", "decorator", "list", "tuple", "generator", "lambda"],
        "data_structures": ["hash", "tree", "linked list", "stack", "queue", "array", "heap"],
        "algorithms": ["sort", "search", "bfs", "dfs", "dynamic programming", "recursion", "complexity"],
        "system_design": ["design", "scale", "cache", "load balancer", "microservice", "api", "database design"],
        "oop_concepts": ["class", "inheritance", "polymorphism", "encapsulation", "solid", "abstraction"],
        "databases": ["sql", "nosql", "index", "query", "normalization", "transaction", "join"],
    }
    relevance_score = 0.0
    for topic in weak_topics:
        topic_lower = topic.lower().strip()
        keywords = topic_keywords.get(topic_lower, [])
        for keyword in keywords:
            if keyword in next_q_lower:
                relevance_score = 1.0
                break
        if relevance_score == 1.0:
            break
    if relevance_score == 0.0:
        for topic_name, keywords in topic_keywords.items():
            for keyword in keywords:
                if keyword in next_q_lower:
                    relevance_score = 0.3
                    break
            if relevance_score > 0.0:
                break
    return relevance_score


def grade_consistency(scores: list[float], expected_trend: str = "stable") -> float:
    if len(scores) < 2:
        return 1.0
    variance = sum((s - sum(scores) / len(scores)) ** 2 for s in scores) / len(scores)
    if expected_trend == "stable":
        if variance <= 2.0:
            return 1.0
        if variance <= 4.0:
            return 0.7
        if variance <= 8.0:
            return 0.4
        return 0.1
    return max(0.0, 1.0 - variance / 20.0)


def grade_final_decision(agent_decision: str, expected_decision: str) -> float:
    if agent_decision.lower().strip() == expected_decision.lower().strip():
        return 1.0
    return 0.0


def grade_task(task_id: str, action_history: list[dict], task_config: dict) -> float:
    if not action_history:
        return 0.0

    if task_id == "easy":
        action = action_history[0]
        gt_score = 6
        scoring = grade_scoring_accuracy(action.get("evaluation_score", 0), gt_score)
        topics = grade_topic_detection(
            action.get("detected_topics", []),
            ["data_structures"]
        )
        return round(0.6 * scoring + 0.4 * topics, 4)

    if task_id == "medium":
        scores_list = [a.get("evaluation_score", 0) for a in action_history]
        gt_scores = [6, 6]
        scoring_grades = []
        for i, (agent_s, gt_s) in enumerate(zip(scores_list, gt_scores)):
            scoring_grades.append(grade_scoring_accuracy(agent_s, gt_s))
        avg_scoring = sum(scoring_grades) / max(len(scoring_grades), 1)
        all_detected = []
        for a in action_history:
            all_detected.extend(a.get("detected_topics", []))
        topics = grade_topic_detection(all_detected, ["data_structures", "algorithms"])
        follow_up = 0.0
        if len(action_history) >= 1:
            first_action = action_history[0]
            follow_up = grade_follow_up_relevance(
                first_action.get("next_question", ""),
                first_action.get("weak_topics", task_config.get("weak_topics", []))
            )
        return round(0.3 * avg_scoring + 0.3 * topics + 0.4 * follow_up, 4)

    if task_id == "hard":
        scores_list = [a.get("evaluation_score", 0) for a in action_history]
        gt_scores = [2, 2, 2, 1]
        scoring_grades = []
        for agent_s, gt_s in zip(scores_list, gt_scores):
            scoring_grades.append(grade_scoring_accuracy(agent_s, gt_s))
        avg_scoring = sum(scoring_grades) / max(len(scoring_grades), 1)
        all_detected = []
        for a in action_history:
            all_detected.extend(a.get("detected_topics", []))
        topics = grade_topic_detection(
            all_detected,
            ["python_basics", "data_structures", "system_design", "databases"]
        )
        follow_ups = []
        for a in action_history[:-1]:
            nq = a.get("next_question", "")
            wt = a.get("weak_topics", task_config.get("weak_topics", []))
            follow_ups.append(grade_follow_up_relevance(nq, wt))
        avg_follow_up = sum(follow_ups) / max(len(follow_ups), 1) if follow_ups else 0.0
        consistency = grade_consistency(scores_list, "stable")
        final_action = action_history[-1]
        decision = grade_final_decision(
            final_action.get("final_decision", "continue"),
            task_config.get("expected_final_decision", "reject")
        )
        return round(
            0.2 * avg_scoring
            + 0.2 * topics
            + 0.2 * avg_follow_up
            + 0.2 * consistency
            + 0.2 * decision,
            4,
        )

    return 0.0
