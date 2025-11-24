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

conversation_history = []

print("AI Chat - Type 'quit' to exit")

while True:
    user_input = input("\nYou: ")
    if user_input.lower() == 'quit':
        break
    
    context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history[-10:]])
    
    prompt = ChatPromptTemplate.from_template(
        "Previous conversation:\n{context}\n\nUser: {input}\n\nRemember any personal information the user shares and use it in future responses. Respond naturally:"
    )
    
    chain = prompt | llm | StrOutputParser()
    
    response = chain.invoke({"context": context, "input": user_input})
    
    conversation_history.append({"role": "User", "content": user_input})
    conversation_history.append({"role": "AI", "content": response})
    
    print(f"AI: {response}")

#I - chart ( stored the full conversation )