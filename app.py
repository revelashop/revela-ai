from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

COHERE_API_KEY = "J0haoqYmMhXnpywSfioaKe736XrLYtAyyqpA4mpk"  # Remplace par ta clé réelle Cohere
COHERE_API_URL = "https://api.cohere.ai/v1/generate"

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form["user_input"]

    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "command-r-plus",  # ou "command-r" selon ton accès
        "chat_history": [],
        "message": user_input,
        "temperature": 0.7,
        "max_tokens": 500,
        "prompt_truncation": "AUTO",
        "preamble": "Tu es un assistant IA francophone qui aide à créer des marques, projets et idées créatives. Tu réponds toujours en français."
    }

    try:
        response = requests.post(COHERE_API_URL, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        reply = response_json["text"]
    except Exception as e:
        reply = f"Erreur API (requête) : {str(e)}"

    return render_template("index.html", response=reply)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
