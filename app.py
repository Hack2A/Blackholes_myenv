from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import ResetRequest, StepRequest, Observation, StepResult, InterviewState
from environment import InterviewEnvironment

app = FastAPI(
    title="Blackholes_myenv",
    description="Multi-round technical interview simulation environment following the OpenEnv specification.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

env = InterviewEnvironment()


@app.get("/")
def health_check():
    return {
        "status": "running",
        "environment": "Blackholes_myenv",
        "version": "1.0.0",
        "endpoints": ["/reset", "/step", "/state"],
    }


@app.post("/reset", response_model=Observation)
def reset_environment(request: ResetRequest = ResetRequest()):
    observation = env.reset(task_id=request.task_id)
    return observation


@app.post("/step", response_model=StepResult)
def step_environment(request: StepRequest):
    result = env.step(action=request.action)
    return result


@app.get("/state", response_model=InterviewState)
def get_state():
    return env.state()


@app.get("/tasks")
def list_available_tasks():
    from tasks import TASK_REGISTRY
    task_summaries = {}
    for tid, config in TASK_REGISTRY.items():
        task_summaries[tid] = {
            "description": config["description"],
            "max_rounds": config["max_rounds"],
            "candidate_strength": config["candidate_strength"],
        }
    return {"tasks": task_summaries}
