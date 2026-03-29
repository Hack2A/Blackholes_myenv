from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class StrengthLevel(str, Enum):
    STRONG = "strong"
    AVERAGE = "average"
    WEAK = "weak"


class FinalDecision(str, Enum):
    HIRE = "hire"
    REJECT = "reject"
    CONTINUE = "continue"


class CandidateProfile(BaseModel):
    name: str
    strength_level: StrengthLevel
    strong_topics: list[str] = Field(default_factory=list)
    weak_topics: list[str] = Field(default_factory=list)


class RoundRecord(BaseModel):
    round_number: int
    question: str
    answer: str
    evaluation_score: float = 0.0
    feedback: str = ""
    detected_topics: list[str] = Field(default_factory=list)
    weak_topics: list[str] = Field(default_factory=list)


class InterviewState(BaseModel):
    episode_id: str
    task_id: str
    current_round: int = 1
    max_rounds: int = 1
    candidate: CandidateProfile
    history: list[RoundRecord] = Field(default_factory=list)
    current_question: str = ""
    current_answer: str = ""
    strong_topics_detected: list[str] = Field(default_factory=list)
    weak_topics_detected: list[str] = Field(default_factory=list)
    final_decision: Optional[str] = None
    done: bool = False
    step_count: int = 0
    action_history: list[dict] = Field(default_factory=list)


class Observation(BaseModel):
    current_question: str
    current_answer: str
    round_number: int
    max_rounds: int
    interview_history: list[dict] = Field(default_factory=list)
    task_description: str = ""
    candidate_profile_hint: str = ""


class Action(BaseModel):
    evaluation_score: float = Field(ge=0.0, le=10.0)
    feedback: str
    detected_topics: list[str] = Field(default_factory=list)
    weak_topics: list[str] = Field(default_factory=list)
    next_question: Optional[str] = None
    final_decision: str = Field(default="continue")


class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: dict = Field(default_factory=dict)


class ResetRequest(BaseModel):
    task_id: str = "easy"


class StepRequest(BaseModel):
    action: Action
