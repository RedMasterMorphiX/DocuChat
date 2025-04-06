import os
import mysql.connector
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Load .env
load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Setup LLM
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model="llama3-70b-8192"
)

# Define a prompt template
template = """
You are a helpful assistant. Answer the following question:
Question: {question}
Answer:
"""
prompt = PromptTemplate(
    input_variables=["question"],
    template=template
)

chain = LLMChain(llm=llm, prompt=prompt)

# Ask a question
user_input = input("Enter your question: ")
response = chain.run(user_input)
print("Answer:", response)

# Save to MySQL
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="root",  # Change if needed
    database="langchain_data"
)

cursor = db.cursor()
cursor.execute("INSERT INTO responses (question, answer) VALUES (%s, %s)", (user_input, response))
db.commit()

cursor.close()
db.close()
