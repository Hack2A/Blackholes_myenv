"""
Inference Script for Blackholes_myenv
======================================
Multi-round technical interview simulation environment.

MANDATORY ENV VARS:
    API_BASE_URL   The API endpoint for the LLM.
    MODEL_NAME     The model identifier to use for inference.
    HF_TOKEN       Your Hugging Face / API key.

STDOUT FORMAT:
    [START] task=<task_name> env=<benchmark> model=<model_name>
    [STEP]  step=<n> action=<action_str> reward=<0.00> done=<true|false> error=<msg|null>
    [END]   success=<true|false> steps=<n> score=<score> rewards=<r1,r2,...,rn>
"""

import os
import json
import requests
from typing import List, Optional
from openai import OpenAI

# ── Mandatory env vars (LLM) ──────────────────────────────────────────────
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN") or os.getenv("API_KEY", "")

# ── Environment server URL (the HF Space running the FastAPI env) ─────────
ENV_URL = os.getenv("ENV_URL", "http://localhost:7860")

# ── Benchmark metadata ────────────────────────────────────────────────────
BENCHMARK = "Blackholes_myenv"
TASKS = ["easy", "medium", "hard"]

# ── OpenAI client pointed at the LLM endpoint ────────────────────────────
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN,
)

SYSTEM_PROMPT = """You are an expert technical interviewer AI agent. You are evaluating a software engineering candidate.

For each round, you will receive:
- The question asked to the candidate
- The candidate's answer
- The round number and total rounds
- History of previous rounds (if any)
- A task description explaining what you need to do

You must respond with a valid JSON object containing exactly these fields:
- "evaluation_score": a number between 0 and 10 rating the candidate's answer quality
- "feedback": a text explanation of your evaluation
- "detected_topics": a list of technical topics covered in the answer (use lowercase identifiers like "python_basics", "data_structures", "algorithms", "system_design", "oop_concepts", "databases")
- "weak_topics": a list of topics where the candidate showed weakness
- "next_question": a follow-up question string (required if the interview continues, should target weak areas)
- "final_decision": one of "hire", "reject", or "continue"

Rules:
- Score accurately based on depth, correctness, and keyword coverage
- Detect all relevant topics mentioned
- Identify weak areas where the candidate struggled
- Choose follow-up questions that probe identified weaknesses
- Only use "hire" or "reject" on the final round
- Use "continue" for all non-final rounds
- Be consistent in scoring across rounds

Respond ONLY with the JSON object, no other text."""


# ── Structured logging helpers ────────────────────────────────────────────

def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    done_str = str(done).lower()
    error_str = error if error else "null"
    # Sanitise action string: collapse to single line, cap length
    action_clean = action.replace("\n", " ").replace("\r", "")
    if len(action_clean) > 200:
        action_clean = action_clean[:200] + "..."
    print(
        f"[STEP] step={step} action={action_clean} reward={reward:.2f} done={done_str} error={error_str}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}",
        flush=True,
    )


# ── Agent logic ───────────────────────────────────────────────────────────

def call_llm(observation: dict) -> dict:
    """Ask the LLM to evaluate the current interview round."""
    user_message = json.dumps(
        {
            "round_number": observation["round_number"],
            "max_rounds": observation["max_rounds"],
            "question": observation["current_question"],
            "candidate_answer": observation["current_answer"],
            "history": observation.get("interview_history", []),
            "task_description": observation.get("task_description", ""),
            "candidate_hint": observation.get("candidate_profile_hint", ""),
        },
        indent=2,
    )

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=0.0,
        )
        response_text = (completion.choices[0].message.content or "").strip()

        # Strip markdown code fences if present
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            response_text = "\n".join(lines[1:-1])

        action = json.loads(response_text)
    except (json.JSONDecodeError, Exception):
        # Fallback action so the episode can continue
        action = {
            "evaluation_score": 5,
            "feedback": "Unable to parse LLM response.",
            "detected_topics": [],
            "weak_topics": [],
            "next_question": "",
            "final_decision": "continue",
        }

    # Clamp / fill defaults
    action["evaluation_score"] = max(0, min(10, float(action.get("evaluation_score", 5))))
    action.setdefault("final_decision", "continue")
    action.setdefault("feedback", "")
    action.setdefault("detected_topics", [])
    action.setdefault("weak_topics", [])
    action.setdefault("next_question", "")

    return action


def run_task(task_id: str) -> dict:
    """Run a single task episode, emitting structured logs to stdout."""
    rewards: List[float] = []
    steps = 0
    score = 0.0
    success = False

    log_start(task=task_id, env=BENCHMARK, model=MODEL_NAME)

    try:
        # ── Reset ─────────────────────────────────────────────────────
        reset_resp = requests.post(
            f"{ENV_URL}/reset",
            json={"task_id": task_id},
            timeout=30,
        )
        reset_resp.raise_for_status()
        observation = reset_resp.json()

        done = False

        while not done:
            # ── Ask the LLM ───────────────────────────────────────────
            action = call_llm(observation)

            # Build a short action summary for the log line
            action_summary = json.dumps(action, separators=(",", ":"))

            # ── Step ──────────────────────────────────────────────────
            step_resp = requests.post(
                f"{ENV_URL}/step",
                json={"action": action},
                timeout=30,
            )
            step_resp.raise_for_status()
            step_result = step_resp.json()

            observation = step_result["observation"]
            reward = float(step_result["reward"])
            done = bool(step_result["done"])
            info = step_result.get("info", {})
            error = info.get("error", None)

            rewards.append(reward)
            steps += 1

            log_step(
                step=steps,
                action=action_summary,
                reward=reward,
                done=done,
                error=error,
            )

        # ── Compute final score (clamped to [0, 1]) ──────────────────
        final_info = step_result.get("info", {})
        task_grade = final_info.get("task_grade", None)
        if task_grade is not None:
            score = float(task_grade)
        else:
            # Fallback: average of rewards
            score = sum(rewards) / len(rewards) if rewards else 0.0
        score = min(max(score, 0.0), 1.0)
        success = score > 0.0

    except Exception as exc:
        # On any error, still emit a STEP so the validator sees the triple
        if steps == 0:
            rewards.append(0.0)
            steps = 1
            log_step(step=1, action="error", reward=0.0, done=True, error=str(exc))
    finally:
        log_end(success=success, steps=steps, score=score, rewards=rewards)

    return {
        "task_id": task_id,
        "steps": steps,
        "score": round(score, 4),
        "success": success,
        "rewards": rewards,
    }


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    results = {}
    for task_id in TASKS:
        result = run_task(task_id)
        results[task_id] = result

    # Also dump a machine-readable summary
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
