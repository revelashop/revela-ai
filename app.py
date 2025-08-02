from flask import Flask, render_template, request
import requests

app = Flask(__name__)

OPENROUTER_API_KEY = "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"  # Remplace par ta vraie clé
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form["user_input"]

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://revela-ai.onrender.com",  # à modifier si ton domaine change
        "X-Title": "Revela AI"
    }

    data = {
        "model": "mistralai/mixtral-8x7b-instruct",  # Ou un autre modèle compatible
        "messages": [
            {"role": "system", "content": "Tu es un assistant IA pour aider les projets créatifs."},
            {"role": "user", "content": user_input}
        ],
        "max_tokens": 800,
        "temperature": 0.7
    }

    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=data)
        response_json = response.json()
        reply = response_json["choices"][0]["message"]["content"]
    except Exception as e:
        reply = "Erreur API : " + str(e)

    return render_template("index.html", response=reply)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
