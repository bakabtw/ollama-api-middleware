from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
import asyncio
from typing import Dict
import uuid
import uvicorn
from ollama import Client
import os

app = FastAPI()

# Adding COSR middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_HOST = os.environ.get('OLLAMA_HOST', 'http://localhost:11434')  # API endpoint for Ollama
STEP1_MODEL = "generator"  # Step1 model name
STEP2_MODEL = "processor"  # Step2 model name
STEP1_PROMPT = ""  # SYSTEM prompt for step1 model
STEP2_PROMPT = ""  # SYSTEM prompt for step1 model

ollama = Client(host=OLLAMA_HOST)

# Queue for tasks and storage for results
task_queue = asyncio.Queue()
results: Dict[str, str] = {}

class RequestBody(BaseModel):
    input_text: str

# Sending request to Ollama
async def send_request_to_ollama(input_text: str, prompt: str = '', model: str = 'llama3.1') -> str:
    print("Sending request to ollama")
    response = ollama.chat(model=model, messages=[
        {
            'role': 'system',
            'content': prompt
        },
        {
            'role': 'user',
            'content': input_text,
        },
    ])
    print(response)

    return response['message']['content']

# Processing user input
async def process_input(input_text: str) -> list[str]:
    response1 = await send_request_to_ollama(input_text, prompt=STEP1_PROMPT, model=STEP1_MODEL)
    response2 = await send_request_to_ollama(response1, prompt=STEP2_PROMPT, model=STEP2_MODEL)

    return [response1, response2]

# Worker function to process queue requests in single-threaded manner
async def worker():
    while True:
        task_id, input_text = await task_queue.get()
        result = await process_input(input_text)
        results[task_id] = result
        task_queue.task_done()

# Background worker task
@app.on_event("startup")
async def start_worker():
    asyncio.create_task(worker())

@app.post("/request")
async def create_request(request_body: RequestBody):
    # Create a unique task ID
    task_id = str(uuid.uuid4())
    # Add the task to the queue
    await task_queue.put((task_id, request_body.input_text))
    # Return the task ID to the client
    return {"task_id": task_id}

@app.get("/result/{task_id}")
async def get_result(task_id: str):
    # Check if the result is ready
    if task_id in results:
        return {"status": "completed", "result": results[task_id]}
    else:
        return {"status": "pending"}

@app.get("/")
async def index_page():
    return FileResponse('index.html')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
