from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv 
from waitress import serve

import logging
app = Flask(__name__)
CORS(app)
 

load_dotenv()

# 🔹 Set your Google Gemini API Key here
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")
print(model.generate_content("Hell!").text)



@app.route("/")
def index():
    return render_template("6.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        user_input = data.get("input")
        function = data.get("function")

        # Different prompts depending on function
        if function == "qna":
            prompt = f"Answer this factual question clearly: {user_input}"
        elif function == "summary":
            prompt = f"Summarize this text in simple words: {user_input}"
        elif function == "story":
            prompt = f"Write a short creative story about: {user_input}"
        elif function == "advice":
            prompt = f"Give helpful advice about: {user_input}"
        else:
            prompt = f"Respond to: {user_input}"

        # Call Google Gemini model
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        return jsonify({"response": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(debug=True, port=5000)
logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    print("🚀 Flask server starting...")
    serve(app, host="0.0.0.0", port=8080)
