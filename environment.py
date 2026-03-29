from models import Observation, Action, StepResult, InterviewState
from utils.state_manager import StateManager
from utils.reward import compute_step_reward, compute_final_bonus
from tasks.graders import grade_task
from tasks import get_task


class InterviewEnvironment:

    def __init__(self):
        self.state_manager = StateManager()
        self._cumulative_reward = 0.0

    def reset(self, task_id: str = "easy") -> Observation:
        self.state_manager.create(task_id)
        self._cumulative_reward = 0.0
        return self.state_manager.to_observation()

    def step(self, action: Action) -> StepResult:
        if self.state_manager.is_done():
            return StepResult(
                observation=self.state_manager.to_observation(),
                reward=0.0,
                done=True,
                info={"error": "Episode already finished. Call /reset to start a new episode."},
            )

        action_dict = action.model_dump()
        ground_truth = self.state_manager.get_ground_truth()
        task_config = self.state_manager.get_task_config()

        step_reward = compute_step_reward(
            action_dict,
            ground_truth,
            self.state_manager.state.current_round,
            self.state_manager.state.max_rounds,
            task_config,
        )

        self.state_manager.advance(action_dict)
        self._cumulative_reward += step_reward

        info = {
            "step_reward": step_reward,
            "cumulative_reward": round(self._cumulative_reward, 4),
            "round_completed": self.state_manager.state.current_round - 1 if not self.state_manager.is_done() else self.state_manager.state.current_round,
        }

        if self.state_manager.is_done():
            task_grade = grade_task(
                self.state_manager.state.task_id,
                self.state_manager.state.action_history,
                task_config,
            )
            final_bonus = compute_final_bonus(task_grade)
            self._cumulative_reward += final_bonus
            info["task_grade"] = task_grade
            info["final_bonus"] = final_bonus
            info["total_reward"] = round(self._cumulative_reward, 4)
            info["final_decision"] = self.state_manager.state.final_decision

        return StepResult(
            observation=self.state_manager.to_observation(),
            reward=step_reward,
            done=self.state_manager.is_done(),
            info=info,
        )

    def state(self) -> InterviewState:
        if self.state_manager.state is None:
            return InterviewState(
                episode_id="none",
                task_id="none",
                candidate={
                    "name": "none",
                    "strength_level": "average",
                    "strong_topics": [],
                    "weak_topics": [],
                },
            )
        return self.state_manager.state
