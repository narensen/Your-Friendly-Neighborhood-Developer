from config import *
from fastapi import FastAPI, Request
from fastapi.middleware import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    
    prompt = "I want to build a js based calculator"
    response = generate_plan(prompt)
    print(response)
    
    code = generate_code(prompt, response)
    debug_plan = generate_debug_plan(code, response)
    print(debug_plan)
    response = lexical_code_search(code, debug_plan)
    print(response)
    