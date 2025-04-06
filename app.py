import os
from dotenv import load_dotenv
from langchain_groq import Groq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from utils import extract_text_from_pdf, store_to_db

load_dotenv()

llm = Groq(api_key=os.getenv("GROQ_API_KEY"), model_name="mixtral-8x7b-32768")

prompt_template = PromptTemplate(
    input_variables=["text"],
    template="""
You are an expert resume parser. Extract the following information from the resume text below:

- Full Name
- Email
- Phone Number

Resume:
{text}

Return as JSON with keys: name, email, phone.
"""
)

chain = LLMChain(llm=llm, prompt=prompt_template)


def process_resume(file_path):
    raw_text = extract_text_from_pdf(file_path)
    if not raw_text.strip():
        print(f"No text found in {file_path}")
        return
    response = chain.run(raw_text)
    try:
        import json
        parsed = json.loads(response)
        name = parsed.get("name")
        email = parsed.get("email")
        phone = parsed.get("phone")
        print(f"✔ Extracted from {file_path}")
        store_to_db(name, email, phone, os.path.basename(file_path))
    except Exception as e:
        print(f"❌ Error parsing {file_path}: {e}\nRaw output: {response}")


def train_all_resumes(folder_path):
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            full_path = os.path.join(folder_path, file)
            process_resume(full_path)


def upload_new_resume(pdf_path):
    if os.path.exists(pdf_path) and pdf_path.endswith(".pdf"):
        process_resume(pdf_path)
    else:
        print("Invalid file path or format.")


if __name__ == "__main__":
    train_all_resumes(r"C:\Users\Soumy\PycharmProjects\Langchain\CVs1")

    # To process a new single resume, uncomment this line:
    # upload_new_resume(r"C:\Users\Soumy\Desktop\new_cv.pdf")

