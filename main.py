from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from fastapi.responses import JSONResponse

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
    if not GROQ_API_KEY:
        raise ValueError("Missing GROQ API Key. Set GROQ_API_KEY in environment variables.")
    
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

class ApiResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    data: Optional[dict] = None

# Initialize chain once for reuse
chain = chat_init()

@app.post("/api/generate-plan", response_model=ApiResponse)
async def api_generate_plan(request: PromptRequest):
    try:
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an expert code planner (Planskill). Your task is to break down the request into a step-by-step implementation plan.
            **Always return output as JSON, nothing else.**"""),
            ("human", "The user wants: {original_prompt}"),
        ])
        
        messages = prompt_template.format_messages(original_prompt=request.prompt)
        response = chain.invoke(messages)

        if not response or not hasattr(response, "content"):
            raise HTTPException(status_code=500, detail="Error: No response received from LLM.")
        
        return JSONResponse(
            content={
                "success": True,
                "data": {"plan": response.content if response else "No response received."}
            }
        )
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": f"Error generating plan: {str(e)}"},
            status_code=500
        )

@app.post("/api/generate-code", response_model=ApiResponse)
async def api_generate_code(request: PlanRequest):
    try:
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an expert code builder (Codeskill). Your job is to write efficient, structured, and well-documented code that follows the given plan."""),
            ("human", "The user wants: {original_prompt}\nHere is the plan:\n{plan}"),
        ])
        
        messages = prompt_template.format_messages(original_prompt=request.prompt, plan=request.plan)
        response = chain.invoke(messages)

        if not response or not hasattr(response, "content"):
            raise HTTPException(status_code=500, detail="Error: No response received from LLM.")
        
        return JSONResponse(
            content={
                "success": True,
                "data": {"code": response.content if response else "No response received."}
            }
        )
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": f"Error generating code: {str(e)}"},
            status_code=500
        )

@app.post("/api/debug-code", response_model=ApiResponse)
async def api_debug_code(request: CodeRequest):
    try:
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an expert code debugger (Debugskill). Your job is to find and fix errors in the given code."""),
            ("human", "The user wants: {original_prompt}\nHere is the generated code:\n{code}"),
        ])
        
        messages = prompt_template.format_messages(original_prompt=request.prompt, code=request.code)
        response = chain.invoke(messages)

        if not response or not hasattr(response, "content"):
            raise HTTPException(status_code=500, detail="Error: No response received from LLM.")
        
        return JSONResponse(
            content={
                "success": True,
                "data": {"debug_output": response.content if response else "No response received."}
            }
        )
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": f"Error debugging code: {str(e)}"},
            status_code=500
        )

@app.post("/api/generate-debug-plan", response_model=ApiResponse)
async def api_generate_debug_plan(request: CodeRequest):
    try:
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an expert code debugger. Your task is to generate a structured plan to debug the given code."""),
            ("human", "The user wants: {original_prompt}\nHere is the generated code:\n{code}"),
        ])
        
        messages = prompt_template.format_messages(original_prompt=request.prompt, code=request.code)
        response = chain.invoke(messages)

        if not response or not hasattr(response, "content"):
            raise HTTPException(status_code=500, detail="Error: No response received from LLM.")
        
        return JSONResponse(
            content={
                "success": True,
                "data": {"debug_plan": response.content if response else "No response received."}
            }
        )
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": f"Error generating debug plan: {str(e)}"},
            status_code=500
        )

@app.post("/api/parent-llm", response_model=ApiResponse)
async def api_parent_llm(request: CodeRequest):
    try:
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are the Parent LLM overseeing the entire code-building process. Your job is to validate whether the output meets the original request and plan."""),
            ("human", "The user wants: {original_prompt}\nHere is the final output:\n{json_response}"),
        ])
        
        messages = prompt_template.format_messages(original_prompt=request.prompt, json_response=request.code)
        response = chain.invoke(messages)

        if not response or not hasattr(response, "content"):
            raise HTTPException(status_code=500, detail="Error: No response received from LLM.")
        
        return JSONResponse(
            content={
                "success": True,
                "data": {"validation": response.content if response else "No response received."}
            }
        )
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": f"Error validating code: {str(e)}"},
            status_code=500
        )

# Full pipeline endpoint
@app.post("/api/generate-full", response_model=ApiResponse)
async def api_generate_full(request: PromptRequest):
    try:
        # Step 1: Generate plan
        plan_response = await api_generate_plan(request)
        plan_response_json = await plan_response.json()
        if not plan_response_json.get("success", False):
            return plan_response
        
        plan = plan_response_json["data"]["plan"]
        
        # Step 2: Generate code
        code_request = PlanRequest(prompt=request.prompt, plan=plan)
        code_response = await api_generate_code(code_request)
        code_response_json = await code_response.json()
        if not code_response_json.get("success", False):
            return code_response
        
        code = code_response_json["data"]["code"]
        
        # Step 3: Debug code
        debug_request = CodeRequest(prompt=request.prompt, code=code)
        debug_response = await api_debug_code(debug_request)
        debug_response_json = await debug_response.json()
        debug_output = debug_response_json["data"]["debug_output"] if debug_response_json.get("success") else None
        
        # Step 4: Generate debug plan
        debug_plan_response = await api_generate_debug_plan(debug_request)
        debug_plan_response_json = await debug_plan_response.json()
        debug_plan = debug_plan_response_json["data"]["debug_plan"] if debug_plan_response_json.get("success") else None
        
        # Step 5: Final validation
        validation_response = await api_parent_llm(debug_request)
        validation_response_json = await validation_response.json()
        validation = validation_response_json["data"]["validation"] if validation_response_json.get("success") else None
        
        return JSONResponse(
            content={
                "success": True,
                "data": {
                    "plan": plan,
                    "code": code,
                    "debug_output": debug_output,
                    "debug_plan": debug_plan,
                    "validation": validation
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": f"Error in full generation pipeline: {str(e)}"},
            status_code=500
        )

# Mount static files for frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
