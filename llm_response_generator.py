# llm_response_generator.py

import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# GROQ API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Step 1: Initialize the model
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model="Gemma-7b-it"  # or "Gemma2-9b-it" if available in your API plan
)

# Step 2: Create a prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}")
])

# Step 3: Output parser
output_parser = StrOutputParser()

# Step 4: Combine into a chain
chain = prompt | llm | output_parser

# Step 5: Run the chain
def get_response(user_input):
    response = chain.invoke({"input": user_input})
    return response
