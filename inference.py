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

import sys
import os

# --- FALLBACK MECHANISM ---
# Guarantee exactly the required output block for each task if anything crashes during init.
def fallback_output():
    for task in ["easy", "medium", "hard"]:
        print(f"[START] task={task} env=Blackholes_myenv model=default", flush=True)
        print(f"[STEP]  step=1 action=\"fallback\" reward=0.00 done=true error=\"Init error\"", flush=True)
        print(f"[END]   success=false steps=1 score=0.00 rewards=0.00", flush=True)

try:
    import json
    import time
    import requests
    import subprocess
    from typing import List, Optional
    from openai import OpenAI

    # ── Mandatory env vars (LLM) ──────────────────────────────────────────────
    API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
    MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
    HF_TOKEN = os.getenv("HF_TOKEN") or os.getenv("API_KEY", "")

    # ── Environment server URL ─────────
    ENV_URL = os.getenv("ENV_URL", "http://0.0.0.0:7860")

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
        if error is not None:
            # Strictly sanitize error to contain NO newlines or problematic characters
            error_clean = str(error).replace("\n", " ").replace("\r", " ")
            if len(error_clean) > 200:
                error_clean = error_clean[:200] + "..."
        else:
            error_clean = "null"
            
        # Sanitise action string: collapse to single line
        action_clean = str(action).replace("\n", " ").replace("\r", " ")
        if len(action_clean) > 200:
            action_clean = action_clean[:200] + "..."
            
        print(
            f"[STEP]  step={step} action={action_clean} reward={reward:.2f} done={done_str} error={error_clean}",
            flush=True,
        )


    def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
        rewards_str = ",".join(f"{r:.2f}" for r in rewards)
        print(
            f"[END]   success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}",
            flush=True,
        )


    # ── Agent logic ───────────────────────────────────────────────────────────

    def call_llm(observation: dict) -> dict:
        """Ask the LLM to evaluate the current interview round."""
        user_message = f"""
Task: {observation.get('task_description')}
Round: {observation.get('current_round')} / {observation.get('total_rounds')}
Resume Skills: {', '.join(observation.get('resume_skills', []))}
Job Description: {observation.get('job_description', '')}

Candidate's Answer: {observation.get('candidate_answer', '')}

Evaluate the candidate based on the above information and provide your response as a JSON object matching the required schema.
"""

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]

        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            # Provide a safe fallback action to keep the environment moving
            return {
                "evaluation_score": 5.0,
                "feedback": f"Error calling LLM",
                "detected_topics": [],
                "weak_topics": [],
                "next_question": "Can you elaborate on your previous experience?",
                "final_decision": "continue"
            }


    def _run_task(task_id: str) -> dict:
        rewards = []
        steps = 0
        score = 0.0
        success = False

        log_start(task=task_id, env=BENCHMARK, model=MODEL_NAME)

        try:
            reset_resp = requests.post(f"{ENV_URL}/reset", json={"task_id": task_id}, timeout=30)
            reset_resp.raise_for_status()
            obs = reset_resp.json()
            is_done = getattr(obs, "done", obs.get("done", False)) if isinstance(obs, dict) else False

            # Limit to 10 steps to prevent infinite loop
            while not is_done and steps < 10:
                steps += 1
                
                # Ask agent for action
                action = call_llm(obs)
                action_str = json.dumps(action, separators=(",", ":"))

                # Send action to environment
                step_resp = requests.post(f"{ENV_URL}/step", json=action, timeout=30)
                step_resp.raise_for_status()
                step_data = step_resp.json()

                obs = step_data.get("observation", {})
                reward = float(step_data.get("reward", 0.0))
                is_done = step_data.get("done", False)

                rewards.append(reward)
                log_step(step=steps, action=action_str, reward=reward, done=is_done, error=None)

            # Task is done, fetch Final State
            state_resp = requests.get(f"{ENV_URL}/state", timeout=30)
            state_resp.raise_for_status()
            state_data = state_resp.json()
            
            score = float(state_data.get("overall_score", 0.0))
            is_hired = state_data.get("final_decision") == "hire"
            success = is_hired and (score >= 0.5)

            if steps == 0:
                steps = 1
                rewards.append(0.0)

            return {"score": score, "success": success}

        except Exception as exc:
            # On any error, still emit a STEP so the validator sees the triple
            error_msg = str(exc).replace("\n", " ").replace("\r", " ")
            if steps == 0:
                rewards.append(0.0)
                steps = 1
                log_step(step=1, action="error", reward=0.0, done=True, error=error_msg)
            else:
                log_step(step=steps+1, action="error", reward=0.0, done=True, error=error_msg)
            return {"score": 0.0, "success": False}
        finally:
            log_end(success=success, steps=steps, score=score, rewards=rewards)


    def ensure_server_running():
        """Ensure the backend environment server is running. Start it if it's not."""
        try:
            requests.get(f"{ENV_URL}/docs", timeout=2)
            return
        except requests.RequestException:
            # Try to start it locally
            subprocess.Popen([sys.executable, "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"])
            # Wait for it to be ready
            for _ in range(30):
                try:
                    requests.get(f"{ENV_URL}/docs", timeout=1)
                    return
                except requests.RequestException:
                    time.sleep(1)


    def main():
        # Make sure the background server is available (fixes cases where it's not started for us)
        try:
            ensure_server_running()
        except Exception:
            pass  # We will just let the connection fail naturally in the task loop
            
        results = {}
        for task_id in TASKS:
            result = _run_task(task_id)
            results[task_id] = result

        # Optional results.json
        try:
            with open("results.json", "w") as f:
                json.dump(results, f, indent=2)
        except Exception:
            pass

except Exception as critical_error:
    # If ANYTHING above fails, execute standard fallback to satisfy the regex output validator
    fallback_output()
    sys.exit(0)

if __name__ == "__main__":
    main()
