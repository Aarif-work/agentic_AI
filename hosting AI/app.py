import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)

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

# Configure Google AI
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    # Remove quotes if present in the API key
    api_key = api_key.strip('"').strip("'")
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        print(f"Error configuring model: {e}")
        model = None
else:
    model = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        if not request.json or 'message' not in request.json:
            return jsonify({"error": "Message is required"}), 400
            
        user_input = request.json['message']
        
        if not model:
            return jsonify({"response": "Please set your GOOGLE_API_KEY in the .env file to enable AI responses."})
        
        # Create prompt with portfolio context
        prompt = f"Answer briefly as Aarif based on this portfolio info:\n{portfolio_info}\n\nQuestion: {user_input}\nAnswer:"
        
        response = model.generate_content(prompt)
        return jsonify({"response": response.text})
        
    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)}")
        return jsonify({"error": "Failed to process request. Please check your API key."}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)