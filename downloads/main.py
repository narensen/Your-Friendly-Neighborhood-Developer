from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import re
from typing import Optional

# Initialize the FastAPI application
app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a model for calculator input
class CalculatorInput(BaseModel):
    num1: float
    num2: float
    operation: str

# Define a model for calculator output
class CalculatorOutput(BaseModel):
    result: float

# Define a dictionary for supported operations
SUPPORTED_OPERATIONS = {
    "add": "+",
    "subtract": "-",
    "multiply": "*",
    "divide": "/"
}

# Define a function to sanitize input values
def sanitize_input(input_value: str) -> str:
    return re.sub(r'[^0-9\.]+', '', input_value)

# Define a function to validate input types
def validate_input_types(num1: float, num2: float, operation: str) -> bool:
    if not isinstance(num1, (int, float)) or not isinstance(num2, (int, float)):
        return False
    if not isinstance(operation, str):
        return False
    return True

# Define a function to perform calculations
def perform_calculation(num1: float, num2: float, operation: str) -> float:
    try:
        if operation == "add":
            return num1 + num2
        elif operation == "subtract":
            return num1 - num2
        elif operation == "multiply":
            return num1 * num2
        elif operation == "divide":
            if num2 == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            return num1 / num2
        else:
            raise ValueError("Unsupported operation")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Define a route for calculator input
@app.post("/calculator", response_model=CalculatorOutput)
async def calculator(input_data: CalculatorInput) -> CalculatorOutput:
    try:
        num1 = float(sanitize_input(str(input_data.num1)))
        num2 = float(sanitize_input(str(input_data.num2)))

        if not validate_input_types(num1, num2, input_data.operation):
            raise TypeError("Invalid input types")

        result = perform_calculation(num1, num2, input_data.operation)

        logger.info(f"Calculation: {num1} {SUPPORTED_OPERATIONS.get(input_data.operation, '')} {num2} = {result}")

        return CalculatorOutput(result=result)
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Define a route for testing
@app.get("/test")
async def test() -> dict:
    return {"message": "Hello, World!"}

# Define a route for version
@app.get("/version")
async def version() -> dict:
    return {"version": "1.0.0"}

# Define a route for feedback
@app.post("/feedback")
async def feedback(feedback: str) -> dict:
    logger.info(f"Feedback: {feedback}")
    return {"message": "Thank you for your feedback!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)