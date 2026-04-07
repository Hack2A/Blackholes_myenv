import os
import json
import requests
from openai import OpenAI

API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:7860")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.environ.get("HF_TOKEN", "")

client = OpenAI(
    api_key=HF_TOKEN if HF_TOKEN else os.environ.get("OPENAI_API_KEY", ""),
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


def run_agent_on_task(task_id: str) -> dict:
    # ---- [START] structured output for the validator ----
    print(f"[START] task={task_id}", flush=True)

    reset_response = requests.post(
        f"{API_BASE_URL}/reset",
        json={"task_id": task_id},
    )
    observation = reset_response.json()

    total_reward = 0.0
    steps = 0
    done = False

    while not done:
        user_message = json.dumps({
            "round_number": observation["round_number"],
            "max_rounds": observation["max_rounds"],
            "question": observation["current_question"],
            "candidate_answer": observation["current_answer"],
            "history": observation.get("interview_history", []),
            "task_description": observation.get("task_description", ""),
            "candidate_hint": observation.get("candidate_profile_hint", ""),
        }, indent=2)

        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=0.0,
        )

        response_text = completion.choices[0].message.content.strip()
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            response_text = "\n".join(lines[1:-1])

        try:
            action = json.loads(response_text)
        except json.JSONDecodeError:
            action = {
                "evaluation_score": 5,
                "feedback": "Unable to parse response properly.",
                "detected_topics": [],
                "weak_topics": [],
                "next_question": "",
                "final_decision": "continue",
            }

        action["evaluation_score"] = max(0, min(10, float(action.get("evaluation_score", 5))))
        if "final_decision" not in action:
            action["final_decision"] = "continue"
        if "feedback" not in action:
            action["feedback"] = ""
        if "detected_topics" not in action:
            action["detected_topics"] = []
        if "weak_topics" not in action:
            action["weak_topics"] = []
        if "next_question" not in action:
            action["next_question"] = ""

        step_response = requests.post(
            f"{API_BASE_URL}/step",
            json={"action": action},
        )
        step_result = step_response.json()

        observation = step_result["observation"]
        reward = step_result["reward"]
        done = step_result["done"]
        info = step_result.get("info", {})

        total_reward += reward
        steps += 1

        # ---- [STEP] structured output for the validator ----
        print(f"[STEP] step={steps} reward={reward}", flush=True)

    final_info = step_result.get("info", {})
    final_score = final_info.get("task_grade", round(total_reward, 4))

    # ---- [END] structured output for the validator ----
    print(f"[END] task={task_id} score={final_score} steps={steps}", flush=True)

    return {
        "task_id": task_id,
        "steps": steps,
        "total_reward": round(total_reward, 4),
        "task_grade": final_info.get("task_grade", 0.0),
        "final_bonus": final_info.get("final_bonus", 0.0),
        "final_decision": final_info.get("final_decision", "unknown"),
    }


def main():
    results = {}
    for task_id in ["easy", "medium", "hard"]:
        try:
            result = run_agent_on_task(task_id)
            results[task_id] = result
        except Exception as e:
            # Still emit structured output on error so the validator sees something
            print(f"[START] task={task_id}", flush=True)
            print(f"[STEP] step=1 reward=0.0", flush=True)
            print(f"[END] task={task_id} score=0.0 steps=0", flush=True)
            results[task_id] = {"error": str(e)}

    output_path = "results.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()

