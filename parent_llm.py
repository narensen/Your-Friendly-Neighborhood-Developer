from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from config import *
import os

def parent_llm(json, plan, chain):
    prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """ You are the Parent LLM of an code builder you will be overseeing the code and make sure it 
                    is correct and goes as per the plan. You will be responsible for the code and the code builder.""",
                ),
                ("human", """ The code is {prompt} and the plan is {plan}"""),
            ]
        )
    
    response = chain.invoke({"prompt" : json, "plan" : plan}).content
    return response
