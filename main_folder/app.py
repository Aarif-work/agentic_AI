from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

app = Flask(__name__)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)

conversation_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    
    context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history[-20:]])
    
    prompt = ChatPromptTemplate.from_template(
        "Previous conversation:\n{context}\n\nUser: {input}\n\nRespond naturally:"
    )
    
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"context": context, "input": user_input})
    
    conversation_history.append({"role": "User", "content": user_input})
    conversation_history.append({"role": "AI", "content": response})
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)