import uuid
from models import InterviewState, Observation, RoundRecord, CandidateProfile, StrengthLevel
from tasks import get_task
from utils.simulator import CandidateSimulator


class StateManager:

    def __init__(self):
        self.state: InterviewState = None
        self.simulator: CandidateSimulator = None
        self.current_ground_truth: dict = {}

    def create(self, task_id: str) -> InterviewState:
        task_config = get_task(task_id)
        self.simulator = CandidateSimulator(task_config)
        self.state = InterviewState(
            episode_id=str(uuid.uuid4()),
            task_id=task_id,
            current_round=1,
            max_rounds=task_config["max_rounds"],
            candidate=self.simulator.profile,
            history=[],
            current_question="",
            current_answer="",
            strong_topics_detected=[],
            weak_topics_detected=[],
            final_decision=None,
            done=False,
            step_count=0,
            action_history=[],
        )
        question_data = self.simulator.get_question(1)
        answer_data = self.simulator.get_answer(question_data)
        self.state.current_question = question_data["question"]
        self.state.current_answer = answer_data["answer_text"]
        self.current_ground_truth = {
            "quality_score": answer_data["quality_score"],
            "keywords_present": answer_data["keywords_present"],
            "reasoning_quality": answer_data["reasoning_quality"],
            "topic": question_data["topic"],
            "expected_keywords": question_data["expected_keywords"],
        }
        return self.state

    def advance(self, action_dict: dict) -> InterviewState:
        record = RoundRecord(
            round_number=self.state.current_round,
            question=self.state.current_question,
            answer=self.state.current_answer,
            evaluation_score=action_dict.get("evaluation_score", 0),
            feedback=action_dict.get("feedback", ""),
            detected_topics=action_dict.get("detected_topics", []),
            weak_topics=action_dict.get("weak_topics", []),
        )
        self.state.history.append(record)
        self.state.action_history.append(action_dict)
        self.state.step_count += 1

        for t in action_dict.get("detected_topics", []):
            if t not in self.state.strong_topics_detected:
                self.state.strong_topics_detected.append(t)
        for t in action_dict.get("weak_topics", []):
            if t not in self.state.weak_topics_detected:
                self.state.weak_topics_detected.append(t)

        decision = action_dict.get("final_decision", "continue")
        if decision in ("hire", "reject") or self.state.current_round >= self.state.max_rounds:
            self.state.done = True
            self.state.final_decision = decision
            return self.state

        self.state.current_round += 1

        next_question_text = action_dict.get("next_question", "")
        if next_question_text:
            answer_data = self.simulator.get_answer_for_custom_question(next_question_text)
            self.state.current_question = next_question_text
            self.state.current_answer = answer_data["answer_text"]
            self.current_ground_truth = {
                "quality_score": answer_data["quality_score"],
                "keywords_present": answer_data.get("keywords_present", []),
                "reasoning_quality": answer_data.get("reasoning_quality", "partial"),
                "topic": "general",
                "expected_keywords": [],
            }
        else:
            question_data = self.simulator.get_question(self.state.current_round)
            answer_data = self.simulator.get_answer(question_data)
            self.state.current_question = question_data["question"]
            self.state.current_answer = answer_data["answer_text"]
            self.current_ground_truth = {
                "quality_score": answer_data["quality_score"],
                "keywords_present": answer_data["keywords_present"],
                "reasoning_quality": answer_data["reasoning_quality"],
                "topic": question_data["topic"],
                "expected_keywords": question_data["expected_keywords"],
            }

        return self.state

    def to_observation(self) -> Observation:
        task_config = get_task(self.state.task_id)
        history_dicts = []
        for record in self.state.history:
            history_dicts.append({
                "round": record.round_number,
                "question": record.question,
                "answer": record.answer,
                "score_given": record.evaluation_score,
                "feedback_given": record.feedback,
            })
        profile_hint = f"Candidate appears to have {self.state.candidate.strength_level.value} technical skills."
        if self.state.weak_topics_detected:
            profile_hint += f" Identified weak areas so far: {', '.join(self.state.weak_topics_detected)}."
        return Observation(
            current_question=self.state.current_question,
            current_answer=self.state.current_answer,
            round_number=self.state.current_round,
            max_rounds=self.state.max_rounds,
            interview_history=history_dicts,
            task_description=task_config["description"],
            candidate_profile_hint=profile_hint,
        )

    def is_done(self) -> bool:
        return self.state.done

    def get_ground_truth(self) -> dict:
        return self.current_ground_truth

    def get_task_config(self) -> dict:
        return get_task(self.state.task_id)
