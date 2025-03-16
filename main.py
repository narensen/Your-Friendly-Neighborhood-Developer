from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import os
import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

app = FastAPI(title="Code Generation API", description="An API for generating code with LLM")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment setup
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("Warning: GROQ_API_KEY environment variable not set")

def chat_init():
    return ChatGroq(
        model="llama-3.2-90b-vision-preview",
        temperature=0.7,
        max_tokens=8192,
        api_key=GROQ_API_KEY,
        max_retries=2,
    )

# Models
class PromptRequest(BaseModel):
    prompt: str

class PlanRequest(BaseModel):
    prompt: str
    plan: str

class CodeRequest(BaseModel):
    prompt: str
    code: str

class ApiResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    data: Optional[dict] = None

# Initialize chain
chain = chat_init()

@app.post("/api/generate-plan", response_model=ApiResponse)
async def api_generate_plan(request: PromptRequest):
    try:
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an expert code planner. Break down the request into a step-by-step implementation plan.
            **Always return output as JSON, nothing else.**"""),
            ("human", "The user wants: {original_prompt}"),
        ])
        messages = prompt_template.format_messages(original_prompt=request.prompt)
        response = chain.invoke(messages)
        return ApiResponse(success=True, data={"plan": response.content if response else "No response received."})
    except Exception as e:
        return ApiResponse(success=False, message=f"Error generating plan: {str(e)}")

@app.post("/api/generate-code", response_model=ApiResponse)
async def api_generate_code(request: PlanRequest):
    try:
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are an expert code builder. Write efficient, structured, well-documented code following the plan."),
            ("human", "The user wants: {original_prompt}\nHere is the plan:\n{plan}"),
        ])
        messages = prompt_template.format_messages(original_prompt=request.prompt, plan=request.plan)
        response = chain.invoke(messages)
        return ApiResponse(success=True, data={"code": response.content if response else "No response received."})
    except Exception as e:
        return ApiResponse(success=False, message=f"Error generating code: {str(e)}")

@app.post("/api/debug-code", response_model=ApiResponse)
async def api_debug_code(request: CodeRequest):
    try:
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are an expert code debugger. Find and fix errors in the given code."),
            ("human", "The user wants: {original_prompt}\nHere is the generated code:\n{code}"),
        ])
        messages = prompt_template.format_messages(original_prompt=request.prompt, code=request.code)
        response = chain.invoke(messages)
        return ApiResponse(success=True, data={"debug_output": response.content if response else "No response received."})
    except Exception as e:
        return ApiResponse(success=False, message=f"Error debugging code: {str(e)}")

@app.post("/api/generate-full", response_model=ApiResponse)
async def api_generate_full(request: PromptRequest):
    try:
        plan_response = await api_generate_plan(request)
        plan_json = json.loads(plan_response.json())
        if not plan_json.get("success", False):
            return plan_response
        plan = plan_json["data"]["plan"]
        
        code_request = PlanRequest(prompt=request.prompt, plan=plan)
        code_response = await api_generate_code(code_request)
        code_json = json.loads(code_response.json())
        if not code_json.get("success", False):
            return code_response
        code = code_json["data"]["code"]
        
        debug_request = CodeRequest(prompt=request.prompt, code=code)
        debug_response = await api_debug_code(debug_request)
        debug_json = json.loads(debug_response.json())
        debug_output = debug_json["data"]["debug_output"] if debug_json.get("success", False) else None
        
        return ApiResponse(success=True, data={
            "plan": plan,
            "code": code,
            "debug_output": debug_output
        })
    except Exception as e:
        return ApiResponse(success=False, message=f"Error in full generation pipeline: {str(e)}")

# Serve frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
