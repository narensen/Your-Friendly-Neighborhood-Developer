```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from math import sqrt, sin, cos, tan, log, exp
from enum import Enum

app = FastAPI()

class Operation(str, Enum):
    add = "add"
    subtract = "subtract"
    multiply = "multiply"
    divide = "divide"
    sqrt = "sqrt"
    sin = "sin"
    cos = "cos"
    tan = "tan"
    log = "log"
    exp = "exp"

class CalculatorInput(BaseModel):
    num1: float
    num2: Optional[float] = None
    operation: Operation

class CalculatorOutput(BaseModel):
    result: float

class TrigonometricInput(BaseModel):
    angle: float
    operation: Operation

class TrigonometricOutput(BaseModel):
    result: float

class LogarithmicInput(BaseModel):
    number: float
    operation: Operation

class LogarithmicOutput(BaseModel):
    result: float

class ExponentialInput(BaseModel):
    number: float
    operation: Operation

class ExponentialOutput(BaseModel):
    result: float

def calculate(num1: float, num2: Optional[float], operation: Operation):
    if operation == Operation.add:
        return num1 + num2
    elif operation == Operation.subtract:
        return num1 - num2
    elif operation == Operation.multiply:
        return num1 * num2
    elif operation == Operation.divide:
        if num2 == 0:
            raise HTTPException(status_code=400, detail="Cannot divide by zero")
        return num1 / num2
    elif operation == Operation.sqrt:
        if num1 < 0:
            raise HTTPException(status_code=400, detail="Cannot take square root of negative number")
        return sqrt(num1)
    else:
        raise HTTPException(status_code=400, detail="Invalid operation")

def trigonometric(angle: float, operation: Operation):
    if operation == Operation.sin:
        return sin(angle)
    elif operation == Operation.cos:
        return cos(angle)
    elif operation == Operation.tan:
        return tan(angle)
    else:
        raise HTTPException(status_code=400, detail="Invalid operation")

def logarithmic(number: float, operation: Operation):
    if operation == Operation.log:
        if number <= 0:
            raise HTTPException(status_code=400, detail="Cannot take logarithm of non-positive number")
        return log(number)
    elif operation == Operation.exp:
        return exp(number)
    else:
        raise HTTPException(status_code=400, detail="Invalid operation")

@app.post("/calculate", response_model=CalculatorOutput)
def calculate_endpoint(input: CalculatorInput):
    return CalculatorOutput(result=calculate(input.num1, input.num2, input.operation))

@app.post("/trigonometric", response_model=TrigonometricOutput)
def trigonometric_endpoint(input: TrigonometricInput):
    return TrigonometricOutput(result=trigonometric(input.angle, input.operation))

@app.post("/logarithmic", response_model=LogarithmicOutput)
def logarithmic_endpoint(input: LogarithmicInput):
    return LogarithmicOutput(result=logarithmic(input.number, input.operation))

@app.post("/exponential", response_model=ExponentialOutput)
def exponential_endpoint(input: ExponentialInput):
    return ExponentialOutput(result=logarithmic(input.number, input.operation))

from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")

from fastapi.responses import HTMLResponse
from pathlib import Path

@app.get("/index", response_class=HTMLResponse)
def read_index():
    return Path("index.html").read_text()
```