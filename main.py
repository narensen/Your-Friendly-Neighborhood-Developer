from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

app = FastAPI(title="Code Generation API", description="An API for generating code with LLM")

# CORS setup to allow frontend to call our API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
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

# Models for request/response
class PromptRequest(BaseModel):
    prompt: str

class PlanRequest(BaseModel):
    prompt: str
    plan: str

class CodeRequest(BaseModel):
    prompt: str
    code: str

# Initialize chain once for reuse
chain = chat_init()

@app.post("/api/generate-plan")
async def api_generate_plan(request: PromptRequest):
    try:
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an expert code planner (Planskill). Your task is to break down the request into a step-by-step implementation plan.
            **Always return output as JSON, nothing else.**"""),
            ("human", "The user wants: {original_prompt}"),
        ])
        
        messages = prompt_template.format_messages(original_prompt=request.prompt)
        response = chain.invoke(messages)
        
        return {"success": True, "data": response.content if response else "No response received."}
    except Exception as e:
        return {"success": False, "message": f"Error generating plan: {str(e)}"}

@app.post("/api/generate-code")
async def api_generate_code(request: PlanRequest):
    try:
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an expert code builder (Codeskill). Your job is to write efficient, structured, and well-documented code that follows the given plan."""),
            ("human", "The user wants: {original_prompt}\nHere is the plan:\n{plan}"),
        ])
        
        messages = prompt_template.format_messages(original_prompt=request.prompt, plan=request.plan)
        response = chain.invoke(messages)
        
        return {"success": True, "data": response.content if response else "No response received."}
    except Exception as e:
        return {"success": False, "message": f"Error generating code: {str(e)}"}

@app.post("/api/generate-full")
async def api_generate_full(request: PromptRequest):
    try:
        plan_response = await api_generate_plan(request)
        if not plan_response["success"]:
            return plan_response
        plan = plan_response["data"]
        
        code_request = PlanRequest(prompt=request.prompt, plan=plan)
        code_response = await api_generate_code(code_request)
        if not code_response["success"]:
            return code_response
        code = code_response["data"]
        
        return {"success": True, "data": {"plan": plan, "code": code}}
    except Exception as e:
        return {"success": False, "message": f"Error in full generation pipeline: {str(e)}"}

# Mount static files for frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
