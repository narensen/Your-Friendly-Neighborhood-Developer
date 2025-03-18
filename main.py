from config import *
from models import *
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():
    return {"message": "Hello World"}

@app.post("/generate")
async def main(request : PromptRequest):
    
    generated_plan = generate_plan(request.prompt)
    generated_code = generate_code(request.prompt, generated_plan)
    debug_plan = generate_debug_plan(generated_code, generated_plan)
    response = lexical_code_search(generated_code, debug_plan)
    
    with open("calc.py ", "w") as f:
        f.write(response)
    
    if request.fullstack:
        frontend_response = generate_code("Generate a html css frontend for this code in a single file index.html", response)
        with open("index.html", "w") as f:
            f.write(frontend_response)
    
    else:
        frontend_response = None
    
    print(response)
    print(frontend_response)
    return {"response" : response, "frontend_response" : frontend_response}

if __name__ == "__main__":
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    