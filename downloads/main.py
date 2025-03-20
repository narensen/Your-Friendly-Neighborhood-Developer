from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import math

app = FastAPI()

class Calculation(BaseModel):
    operation: str
    num1: float
    num2: Optional[float] = None

class ScientificCalculator:
    def add(self, num1: float, num2: float):
        return num1 + num2

    def subtract(self, num1: float, num2: float):
        return num1 - num2

    def multiply(self, num1: float, num2: float):
        return num1 * num2

    def divide(self, num1: float, num2: float):
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        return num1 / num2

    def power(self, num1: float, num2: float):
        return num1 ** num2

    def sqrt(self, num1: float):
        if num1 < 0:
            raise ValueError("Cannot calculate square root of negative number")
        return num1 ** 0.5

    def log(self, num1: float):
        if num1 <= 0:
            raise ValueError("Cannot calculate logarithm of non-positive number")
        return math.log(num1)

    def sin(self, num1: float):
        return math.sin(num1)

    def cos(self, num1: float):
        return math.cos(num1)

    def tan(self, num1: float):
        return math.tan(num1)

calculator = ScientificCalculator()

@app.post("/calculate")
async def calculate(calculation: Calculation):
    operation = calculation.operation
    num1 = calculation.num1
    num2 = calculation.num2

    if operation == "add":
        if num2 is None:
            return {"error": "Two numbers are required for addition"}
        return {"result": calculator.add(num1, num2)}
    elif operation == "subtract":
        if num2 is None:
            return {"error": "Two numbers are required for subtraction"}
        return {"result": calculator.subtract(num1, num2)}
    elif operation == "multiply":
        if num2 is None:
            return {"error": "Two numbers are required for multiplication"}
        return {"result": calculator.multiply(num1, num2)}
    elif operation == "divide":
        if num2 is None:
            return {"error": "Two numbers are required for division"}
        try:
            return {"result": calculator.divide(num1, num2)}
        except ValueError as e:
            return {"error": str(e)}
    elif operation == "power":
        if num2 is None:
            return {"error": "Two numbers are required for power operation"}
        return {"result": calculator.power(num1, num2)}
    elif operation == "sqrt":
        if num2 is not None:
            return {"error": "Only one number is required for square root operation"}
        try:
            return {"result": calculator.sqrt(num1)}
        except ValueError as e:
            return {"error": str(e)}
    elif operation == "log":
        if num2 is not None:
            return {"error": "Only one number is required for logarithm operation"}
        try:
            return {"result": calculator.log(num1)}
        except ValueError as e:
            return {"error": str(e)}
    elif operation == "sin":
        if num2 is not None:
            return {"error": "Only one number is required for sine operation"}
        return {"result": calculator.sin(num1)}
    elif operation == "cos":
        if num2 is not None:
            return {"error": "Only one number is required for cosine operation"}
        return {"result": calculator.cos(num1)}
    elif operation == "tan":
        if num2 is not None:
            return {"error": "Only one number is required for tangent operation"}
        return {"result": calculator.tan(num1)}
    else:
        return {"error": "Invalid operation"}

@app.get("/operations")
async def get_operations():
    return {
        "operations": [
            "add",
            "subtract",
            "multiply",
            "divide",
            "power",
            "sqrt",
            "log",
            "sin",
            "cos",
            "tan"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)