import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

def get_portfolio_content():
    try:
        response = requests.get("https://aarif-work.github.io/html/", timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()
        return ' '.join(text.split())[:3000]
    except:
        return "Aarif - Full Stack Developer with skills in Python, JavaScript, React, Node.js"

portfolio_info = get_portfolio_content()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)

prompt = ChatPromptTemplate.from_template(
    "Answer briefly as Aarif:\n{portfolio_info}\n\nQ: {question}\nA:"
)

chain = prompt | llm | StrOutputParser()

def ask(question):
    return chain.invoke({"portfolio_info": portfolio_info, "question": question})

if __name__ == "__main__":
    while True:
        q = input("Q: ")
        if q.lower() == 'q': break
        print(ask(q))