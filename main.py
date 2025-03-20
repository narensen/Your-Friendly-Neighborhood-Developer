from config import *
from models import *
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

# Create static directory if it doesn't exist
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
        request.prompt = "Generate a fastapi code " + request.prompt
    generated_plan = generate_plan(request.prompt)

    generated_code = generate_code(request.prompt, generated_plan)
    debug_plan = generate_debug_plan(generated_code, generated_plan)
    response = lexical_code_search(generated_code, debug_plan)

    with open("downloads/main.py", "w") as f:
        response = response.split("\n")
        modified_text = "\n".join(response[1:-1])
        f.write(modified_text)

    if request.fullstack:
        frontend_response = generate_code(
            "Generate a html css frontend for the given code in a single file", response
        )

        with open("downloads/index.html", "w") as f:
            response = frontend_response.split("\n")
            modified_text = "\n".join(response[1:-1])
            f.write(modified_text)

    else:
        frontend_response = None

    print(response)
    print(frontend_response)
    return {"response": response, "frontend_response": frontend_response}


if __name__ == "__main__":

    import uvicorn  
    uvicorn.run(app, host="0.0.0.0", port=8000)