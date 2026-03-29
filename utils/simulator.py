from models import CandidateProfile, StrengthLevel
from tasks.dataset import get_question_for_round, get_candidate_answer, get_question_index_in_topic


class CandidateSimulator:

    def __init__(self, task_config: dict):
        self.task_config = task_config
        self.profile = CandidateProfile(
            name=task_config["candidate_name"],
            strength_level=StrengthLevel(task_config["candidate_strength"]),
            strong_topics=task_config.get("strong_topics", []),
            weak_topics=task_config.get("weak_topics", []),
        )

    def get_question(self, round_number: int) -> dict:
        return get_question_for_round(self.task_config["task_id"], round_number)

    def get_answer(self, question_data: dict) -> dict:
        topic = question_data["topic"]
        topic_questions = __import__("tasks.dataset", fromlist=["QUESTION_BANK"]).QUESTION_BANK.get(topic, [])
        q_index = 0
        for idx, q in enumerate(topic_questions):
            if q["question"] == question_data["question"]:
                q_index = idx
                break
        return get_candidate_answer(topic, q_index, self.profile.strength_level.value)

    def get_answer_for_custom_question(self, question_text: str) -> dict:
        topic, idx = get_question_index_in_topic(question_text)
        answer_data = get_candidate_answer(topic, idx, self.profile.strength_level.value)
        if answer_data["answer_text"] == "I am not sure about this topic.":
            fallback_answers = {
                "strong": {
                    "answer_text": "That is a good question. Based on my understanding of the fundamentals, I would approach this systematically by analyzing the core requirements and applying established patterns to find an optimal solution.",
                    "quality_score": 7,
                    "keywords_present": [],
                    "reasoning_quality": "good",
                },
                "average": {
                    "answer_text": "I have some familiarity with this area. I think the main idea involves breaking the problem down and applying standard approaches, though I may be missing some details.",
                    "quality_score": 4,
                    "keywords_present": [],
                    "reasoning_quality": "partial",
                },
                "weak": {
                    "answer_text": "I am not very confident about this topic. I have heard of the concept but I cannot explain it in detail right now.",
                    "quality_score": 2,
                    "keywords_present": [],
                    "reasoning_quality": "poor",
                },
            }
            return fallback_answers.get(self.profile.strength_level.value, fallback_answers["weak"])
        return answer_data
