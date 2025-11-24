import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)

prompt = ChatPromptTemplate.from_template(
    "Analyze this text and extract all relevant data into a suitable JSON format with appropriate keys:\n\n{text_input}"
)

chain = prompt | llm | StrOutputParser()

if __name__ == "__main__":
    input_text = "hope3 foundation have 25 students and 30 teachers and 2 classrooms."
    result = chain.invoke({"text_input": input_text})
    print(result)