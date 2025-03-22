from config import *
from models import *
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import os
import time
import threading

app = FastAPI()

# Ensure static and downloads directories exist
os.makedirs("static", exist_ok=True)
os.makedirs("downloads", exist_ok=True)

# CORS Middleware (Allow both local and deployed frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local frontend
        "https://your-friendly-neighborhood-developer.vercel.app",  # Deployed frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home():
    try:
        with open("static/index.html", "r") as f:
            content = f.read()
    except FileNotFoundError:
        content = "<h1>Index file not found</h1>"
    return HTMLResponse(content=content)

@app.get("/api")
def api_home():
    return {"message": "Hello World"}

@app.post("/generate")
async def main(request: PromptRequest):
    if request.fullstack:
        request.prompt = "Generate a FastAPI backend code only" + request.prompt

    generated_plan = generate_plan(request.prompt)
    generated_code = generate_code(request.prompt, generated_plan)
    debug_plan = generate_debug_plan(generated_code, generated_plan)
    backend_response = lexical_code_search(generated_code, debug_plan)
    backend_lines = backend_response.split("\n")
    backend_response_ = "\n".join(backend_lines[1:-1])

    frontend_response = None
    deployment_instructions = None

    if request.fullstack:
        frontend_response = generate_code(
            "Generate a frontend for the given code in a single file", backend_response
        )
        frontend_lines = frontend_response.split("\n")
        frontend_response = "\n".join(frontend_lines[1:-1])

        backend_response = generate_code(
            """Give me the backend code alone, nothing else—just code. 
            Connect the backend and frontend using static files.""",
            backend_response_,
        )
        
        backend_lines = backend_response.split("\n")
        backend_response = "\n".join(backend_lines[1:-1])

        # Save files temporarily in downloads/
        backend_file = "downloads/main.py"
        frontend_file = "downloads/index.html"

        with open(backend_file, "w") as f:
            f.write(backend_response)

        with open(frontend_file, "w") as f:
            f.write(frontend_response)

        deployment_instructions = generate_code(
            "Give me the instructions for how to run this code" + backend_response, 
            "Give me the instructions for how to run this code" + frontend_response
        )

    return {
        "backend_response": backend_response,
        "frontend_response": frontend_response,
        "deployment_instructions": deployment_instructions,
        "backend_download": f"/download/main.py",
        "frontend_download": f"/download/index.html",
    }

@app.get("/download/{filename}")
def download_file(filename: str):
    """Serve temporary files from the downloads directory."""
    file_path = f"downloads/{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename)
    return {"error": "File not found"}

def cleanup_old_files():
    """Auto-delete files older than 10 minutes."""
    while True:
        for file in os.listdir("downloads"):
            file_path = os.path.join("downloads", file)
            if os.path.isfile(file_path) and time.time() - os.path.getmtime(file_path) > 600:  # 10 min
                os.remove(file_path)
        time.sleep(600)  # Check every 10 minutes

# Start cleanup process in a background thread
threading.Thread(target=cleanup_old_files, daemon=True).start()
