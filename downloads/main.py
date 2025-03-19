from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

# Define the calculator model
class Calculator(BaseModel):
    num1: float
    num2: float
    operation: str

# Define the product model
class Product(BaseModel):
    name: str
    description: str
    requirements: str
    functionalities: str
    blueprint: str
    features: str
    roadmap: str
    deliverables: str
    timeline: str
    resources: str
    budget: str

# Create a dictionary to store products
products = {}

# Create a Jinja2 template engine
templates = Jinja2Templates(directory="templates")

# Define the calculator route
@app.get("/calculator")
async def get_calculator(request: Request):
    return templates.TemplateResponse("calculator.html", {"request": request})

# Define the calculator operation route
@app.post("/calculator/operation")
async def calculate(request: Request, num1: str = Form(...), num2: str = Form(...), operation: str = Form(...)):
    num1 = float(num1)
    num2 = float(num2)
    if operation == "add":
        return {"result": num1 + num2}
    elif operation == "subtract":
        return {"result": num1 - num2}
    elif operation == "multiply":
        return {"result": num1 * num2}
    elif operation == "divide":
        if num2 != 0:
            return {"result": num1 / num2}
        else:
            return {"error": "Cannot divide by zero"}

# Define the product creation route
@app.post("/product/create")
async def create_product(request: Request, name: str = Form(...), description: str = Form(...), requirements: str = Form(...), 
                          functionalities: str = Form(...), blueprint: str = Form(...), features: str = Form(...), 
                          roadmap: str = Form(...), deliverables: str = Form(...), timeline: str = Form(...), 
                          resources: str = Form(...), budget: str = Form(...)):
    products[name] = Product(name=name, description=description, requirements=requirements, functionalities=functionalities, 
                            blueprint=blueprint, features=features, roadmap=roadmap, deliverables=deliverables, 
                            timeline=timeline, resources=resources, budget=budget)
    return {"message": "Product created successfully"}

# Define the product requirements route
@app.get("/product/{product_name}/get_product_requirements")
async def get_product_requirements(product_name: str):
    if product_name in products:
        return {"requirements": products[product_name].requirements}
    else:
        return {"error": "Product not found"}

# Define the product functionalities route
@app.get("/product/{product_name}/get_functionalities")
async def get_functionalities(product_name: str):
    if product_name in products:
        return {"functionalities": products[product_name].functionalities}
    else:
        return {"error": "Product not found"}

# Define the product blueprint creation route
@app.post("/product/{product_name}/create_product_blueprint")
async def create_product_blueprint(product_name: str, blueprint: str = Form(...)):
    if product_name in products:
        products[product_name].blueprint = blueprint
        return {"message": "Product blueprint created successfully"}
    else:
        return {"error": "Product not found"}

# Define the product features definition route
@app.post("/product/{product_name}/define_product_features")
async def define_product_features(product_name: str, features: str = Form(...)):
    if product_name in products:
        products[product_name].features = features
        return {"message": "Product features defined successfully"}
    else:
        return {"error": "Product not found"}

# Define the product roadmap development route
@app.post("/product/{product_name}/develop_product_roadmap")
async def develop_product_roadmap(product_name: str, roadmap: str = Form(...)):
    if product_name in products:
        products[product_name].roadmap = roadmap
        return {"message": "Product roadmap developed successfully"}
    else:
        return {"error": "Product not found"}

# Define the product deliverables identification route
@app.post("/product/{product_name}/identify_product_deliverables")
async def identify_product_deliverables(product_name: str, deliverables: str = Form(...)):
    if product_name in products:
        products[product_name].deliverables = deliverables
        return {"message": "Product deliverables identified successfully"}
    else:
        return {"error": "Product not found"}

# Define the product timeline creation route
@app.post("/product/{product_name}/create_product_timeline")
async def create_product_timeline(product_name: str, timeline: str = Form(...)):
    if product_name in products:
        products[product_name].timeline = timeline
        return {"message": "Product timeline created successfully"}
    else:
        return {"error": "Product not found"}

# Define the product resources assignment route
@app.post("/product/{product_name}/assign_product_resources")
async def assign_product_resources(product_name: str, resources: str = Form(...)):
    if product_name in products:
        products[product_name].resources = resources
        return {"message": "Product resources assigned successfully"}
    else:
        return {"error": "Product not found"}

# Define the product budget establishment route
@app.post("/product/{product_name}/establish_product_budget")
async def establish_product_budget(product_name: str, budget: str = Form(...)):
    if product_name in products:
        products[product_name].budget = budget
        return {"message": "Product budget established successfully"}
    else:
        return {"error": "Product not found"}

# Define the product details route
@app.get("/product/{product_name}/details")
async def get_product_details(product_name: str):
    if product_name in products:
        return products[product_name]
    else:
        return {"error": "Product not found"}

# Define the product route
@app.get("/product")
async def get_product(request: Request):
    return templates.TemplateResponse("product.html", {"request": request})