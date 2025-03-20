from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import math

app = FastAPI()

# Define the input model for calculator operations
class CalculatorInput(BaseModel):
    num1: float
    num2: float
    operation: str

class ScientificCalculatorInput(BaseModel):
    num1: float
    operation: str

# Define the API endpoint for calculator operations
@app.post("/calculate")
async def calculate(input: CalculatorInput):
    try:
        if input.operation == "add":
            result = input.num1 + input.num2
        elif input.operation == "subtract":
            result = input.num1 - input.num2
        elif input.operation == "multiply":
            result = input.num1 * input.num2
        elif input.operation == "divide":
            if input.num2 != 0:
                result = input.num1 / input.num2
            else:
                return JSONResponse(content={"error": "Cannot divide by zero"}, status_code=400)
        elif input.operation == "sqrt":
            if input.num1 >= 0:
                result = math.sqrt(input.num1)
            else:
                return JSONResponse(content={"error": "Cannot calculate square root of negative number"}, status_code=400)
        else:
            return JSONResponse(content={"error": "Invalid operation"}, status_code=400)

        return JSONResponse(content={"result": result}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Define the API endpoint for scientific calculator operations
@app.post("/scientific-calculate")
async def scientific_calculate(input: ScientificCalculatorInput):
    try:
        if input.operation == "sin":
            result = math.sin(math.radians(input.num1))
        elif input.operation == "cos":
            result = math.cos(math.radians(input.num1))
        elif input.operation == "tan":
            if math.cos(math.radians(input.num1)) != 0:
                result = math.tan(math.radians(input.num1))
            else:
                return JSONResponse(content={"error": "Cannot calculate tan of this number"}, status_code=400)
        elif input.operation == "log":
            if input.num1 > 0:
                result = math.log(input.num1)
            else:
                return JSONResponse(content={"error": "Cannot calculate log of non-positive number"}, status_code=400)
        elif input.operation == "exp":
            result = math.exp(input.num1)
        else:
            return JSONResponse(content={"error": "Invalid operation"}, status_code=400)

        return JSONResponse(content={"result": result}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Define the API endpoint for calculator history
calculator_history = []
@app.get("/history")
async def get_history():
    try:
        # Return calculator history
        return JSONResponse(content={"history": calculator_history}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Update the calculate function to store the history
@app.post("/calculate")
async def calculate(input: CalculatorInput):
    try:
        if input.operation == "add":
            result = input.num1 + input.num2
        elif input.operation == "subtract":
            result = input.num1 - input.num2
        elif input.operation == "multiply":
            result = input.num1 * input.num2
        elif input.operation == "divide":
            if input.num2 != 0:
                result = input.num1 / input.num2
            else:
                return JSONResponse(content={"error": "Cannot divide by zero"}, status_code=400)
        elif input.operation == "sqrt":
            if input.num1 >= 0:
                result = math.sqrt(input.num1)
            else:
                return JSONResponse(content={"error": "Cannot calculate square root of negative number"}, status_code=400)
        else:
            return JSONResponse(content={"error": "Invalid operation"}, status_code=400)

        calculator_history.append({
            "operation": input.operation,
            "num1": input.num1,
            "num2": input.num2,
            "result": result
        })

        return JSONResponse(content={"result": result}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Update the scientific_calculate function to store the history
@app.post("/scientific-calculate")
async def scientific_calculate(input: ScientificCalculatorInput):
    try:
        if input.operation == "sin":
            result = math.sin(math.radians(input.num1))
        elif input.operation == "cos":
            result = math.cos(math.radians(input.num1))
        elif input.operation == "tan":
            if math.cos(math.radians(input.num1)) != 0:
                result = math.tan(math.radians(input.num1))
            else:
                return JSONResponse(content={"error": "Cannot calculate tan of this number"}, status_code=400)
        elif input.operation == "log":
            if input.num1 > 0:
                result = math.log(input.num1)
            else:
                return JSONResponse(content={"error": "Cannot calculate log of non-positive number"}, status_code=400)
        elif input.operation == "exp":
            result = math.exp(input.num1)
        else:
            return JSONResponse(content={"error": "Invalid operation"}, status_code=400)

        calculator_history.append({
            "operation": input.operation,
            "num1": input.num1,
            "result": result
        })

        return JSONResponse(content={"result": result}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)