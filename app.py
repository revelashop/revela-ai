from flask import Flask, render_template, request
import requests

app = Flask(__name__)

COHERE_API_KEY = "J0haoqYmMhXnpywSfioaKe736XrLYtAyyqpA4mpk"
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
        "model": "command-xlarge",
        "prompt": user_input,
        "max_tokens": 500,
        "temperature": 0.7,
        "k": 0,
        "p": 1,
        "stop_sequences": []
    }

    try:
        response = requests.post(COHERE_API_URL, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        # Cohere renvoie le texte dans 'generations' (liste) -> premier élément -> 'text'
        reply = response_json["generations"][0]["text"]
    except requests.exceptions.RequestException as e:
        reply = f"Erreur API (requête) : {e}"
    except KeyError:
        reply = f"Réponse API inattendue : {response.text}"

    return render_template("index.html", response=reply)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
