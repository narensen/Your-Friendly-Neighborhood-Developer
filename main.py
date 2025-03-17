from config import *

if __name__ == "__main__":
    
    prompt = "I want to build a js based calculator"
    response = generate_plan(prompt)
    
    final_code = []
    
    for i in range(len(response)):
        
        code = generate_code(prompt, response, response[i], final_code)
        final_code.append(code)
        
    debug_plan = generate_debug_plan(prompt, final_code)
    print(debug_plan)