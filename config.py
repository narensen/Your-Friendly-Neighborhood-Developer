from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import json
import os

load_dotenv()
GROQ_API_KEY = os.environ["GROQ_API_KEY"]


def chat_init():
    llm = ChatGroq(
        model="llama-3.2-90b-vision-preview",
        temperature=0.7,
        api_key=GROQ_API_KEY,
        max_tokens=8192,
        max_retries=2,
    )
    return llm

chat = chat_init()

def generate_plan(prompt : str):
    
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """How to build backend of this code properly. THe most robust and efficient way
                """,
            ),
            ("human", """{prompt}"""),
        ]
    )
    
    chain = prompt | chat
    response = chain.invoke({"prompt" : prompt})

    return response.content

def generate_code(prompt_text : str, plan : str,):
    
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an ultimate code builder (you are packed with skills) Codeskill for writing code
                each function and class. You are allowed only to write code""",
            ),
            ("human", """{prompt} The Plan is {plan}"""),
        ]
    )
    
    chain = prompt | chat
    
    response = chain.invoke({"prompt" : prompt_text, "plan" : plan,}).content
    return response

def lexical_code_search(text : str, debug_plan : str,):
    
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """Provide only the code in output. Only the output code alone. You are an ultimate code debugger (you are packed with skills) Codeskill for searching code in natural language
                each function and class. make sure to always look at the code and functions that are making issues segregate them and fix them. Provide only the code nothing else""",
            ),
            ("human", """This is the debug plan {plan} and the code is {code}"""),
        ]
    )
    
    chain = prompt | chat
    
    response = chain.invoke({"plan" : debug_plan, "code" : text}).content
    return response

def generate_debug_plan(text : str, final_code : str):
    
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an ultimate code debugger you should give out a plan to
                generate the final code only the code alone generate the final code only the code alone
                debug the code and make sure it is correct and goes as per the flow.
                Check which functions are doing wrong and what mistakes are there and 
                generate the final code only the code alone.""",
            ),
            ("human", """{plan} {final_code}"""),
        ]
    )
    
    chain = prompt | chat
    response = chain.invoke({"plan" : text, "final_code" : final_code}).content
    return response
 
            