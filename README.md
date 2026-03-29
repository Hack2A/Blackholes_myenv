# Blackholes_myenv

A production-grade OpenEnv environment that simulates multi-round technical interviews for evaluating AI agents on reasoning, memory, and decision-making.

## Overview

This environment presents an AI agent with a realistic interview scenario where it must:

1. Evaluate candidate answers with accurate scoring
2. Detect technical topics and identify weaknesses
3. Choose appropriate follow-up questions targeting gaps
4. Track performance across multiple rounds
5. Make a final hire/reject decision based on cumulative evidence

## Tasks

| Task | Rounds | Candidate | Focus |
|------|--------|-----------|-------|
| `easy` | 1 | Average | Single answer scoring and topic detection |
| `medium` | 2 | Average | Follow-up question selection targeting weak areas |
| `hard` | 4 | Weak | Memory, consistency, and final decision correctness |

## API Endpoints

### POST /reset

Initialize a new interview episode.

**Request:**
```json
{"task_id": "easy"}
```

**Response:** Observation with the first question and candidate answer.

### POST /step

Submit an evaluation action and advance the interview.

**Request:**
```json
{
  "action": {
    "evaluation_score": 7.0,
    "feedback": "Good understanding of fundamentals...",
    "detected_topics": ["python_basics"],
    "weak_topics": ["system_design"],
    "next_question": "How would you design a cache?",
    "final_decision": "continue"
  }
}
```

**Response:** StepResult with next observation, reward, done flag, and info.

### GET /state

Returns the current internal InterviewState.

### GET /tasks

Lists all available tasks with descriptions.

## Grading

Each task is graded on a 0.0-1.0 scale using deterministic graders:

- **Scoring accuracy**: Proximity of agent score to ground truth
- **Topic detection**: Jaccard similarity with expected topics
- **Follow-up relevance**: Whether follow-up targets identified weaknesses
- **Consistency**: Variance in scoring across rounds
- **Final decision**: Binary match with expected outcome

## Running Locally

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 7860
```

## Running Inference

```bash
export API_BASE_URL=http://localhost:7860
export MODEL_NAME=gpt-4o-mini
export OPENAI_API_KEY=your-key
python inference.py
```

## Docker

```bash
docker build -t blackholes_myenv .
docker run -p 7860:7860 blackholes_myenv
```

## Deployment

Deploy to Hugging Face Spaces as a Docker space with port 7860 exposed.
