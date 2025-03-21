from config import *
from models import *
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

os.makedirs("static", exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def home():
    # Return the index.html file
    with open("static/index.html", "r") as f:
        return HTMLResponse(content=f.read())


@app.get("/api")
def api_home():
    # Move the original home endpoint to /api
    return {"message": "Hello World"}


@app.post("/generate")
async def main(request: PromptRequest):
    if request.fullstack:
        request.prompt = "Generate a fastapi backend code only" + request.prompt

    generated_plan = generate_plan(request.prompt)
    generated_code = generate_code(request.prompt, generated_plan)
    debug_plan = generate_debug_plan(generated_code, generated_plan)
    backend_response = lexical_code_search(generated_code, debug_plan)
    backend_lines = backend_response.split("\n")
    backend_response_ = "\n".join(backend_lines[1:-1])

    frontend_response = None
    if request.fullstack:
        frontend_response = generate_code(
            "Generate a frontend for the given code in a single file", backend_response
        )

        backend_response = generate_code(
            """Give me the backend code alone nothing else just code not text anything. Give me the entire backend code alone I just want to copy paste Connect the backend and frontend using static files give me only the python code as you are working 
            on backend alone and return the backend code alone"""
            + backend_response_,
            frontend_response,
        )

        with open("downloads/main.py", "w") as f:
            backend_lines = backend_response.split("\n")
            backend_response = "\n".join(backend_lines[1:-1])
            f.write(backend_response)

        with open("downloads/index.html", "w") as f:
            frontend_lines = frontend_response.split("\n")
            modified_text = "\n".join(frontend_lines[1:-1])
            f.write(modified_text)
            
        deployment_instructions = generate_code(
            "Give me the deployment instructions for this code" + backend_response, 
            "Give me the deployment instructions for this code" + modified_text
        )
            
    return {"response": backend_response, "frontend_response": modified_text, "deployment_instructions": deployment_instructions}


if __name__ == "__main__":
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
