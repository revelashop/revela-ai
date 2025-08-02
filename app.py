from flask import Flask, render_template, request
import requests

app = Flask(__name__)

COHERE_API_KEY = "J0haoqYmMhXnpywSfioaKe736XrLYtAyyqpA4mpk"
COHERE_API_URL = "https://api.cohere.ai/v1/chat/completions"

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
        "model": "command-xlarge",  # ou autre modèle disponible
        "messages": [
            {"role": "system", "content": "Tu es un assistant IA qui aide à créer des marques, projets et idées créatives."},
            {"role": "user", "content": user_input}
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }

    try:
        response = requests.post(COHERE_API_URL, headers=headers, json=data)
        response.raise_for_status()  # pour avoir l'erreur HTTP si besoin
        response_json = response.json()
        reply = response_json["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        reply = f"Erreur API (requête) : {e}"
    except KeyError:
        reply = f"Réponse API inattendue : {response.text}"

    return render_template("index.html", response=reply)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
