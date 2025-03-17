from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import json
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def chat_init():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        max_tokens=32768,
        max_retries=2,
    )
    return llm

chat = chat_init()

def generate_plan(prompt : str):
    
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an ultimate code builder (you are packed with skills) Planskill for
                planning in natural language each function and class. return the statement in a 
                list only a list eg, What functions classes are required in this why they are required
                [].
                """,
            ),
            ("human", """{prompt}"""),
        ]
    )
    
    chain = prompt | chat
    
    response = chain.invoke({"prompt" : prompt})
    data = response.content.encode('utf-8')
    parsed_data = json.loads(data)
    return parsed_data

def generate_code(text : str, plan : str, topic : str, code : str):
    
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an ultimate code builder (you are packed with skills) Codeskill for writing code
                each function and class. You are allowed only to write code""",
            ),
            ("human", """{prompt} The Plan is {plan} and the topic is you are gonna go onto is {topic} and the previous code is {code}"""),
        ]
    )
    
    chain = prompt | chat
    
    response = chain.invoke({"prompt" : text, "plan" : plan, "topic" : topic, "code" : code}).content
    return response

def lexical_code_search(text : str, debug_plan : str, chain):
    
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an ultimate code debugger (you are packed with skills) Codeskill for searching code in natural language
                each function and class. make sure to always look at the code and functions that are making issues segregate them and fix them.""",
            ),
            ("human", """This is the debug plan {plan} and the code is {code}"""),
        ]
    )
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
            ("human", """{code} {final_code}"""),
        ]
    )
    
    chain = prompt | chat
    response = chain.invoke({"code" : text, "final_code" : final_code}).content
    return response
 
            
