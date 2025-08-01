from flask import Flask, render_template, request
import requests

app = Flask(__name__)

TOGETHER_API_KEY = "8e022d58eaa0d0ba85379725aa47843333683ee521ee46cae23c5ffa00b29c9b"
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form["user_input"]

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "messages": [
            {"role": "system", "content": "Tu es un assistant qui aide à réaliser des projets créatifs."},
            {"role": "user", "content": user_input}
        ],
        "max_tokens": 200,
        "temperature": 0.7
    }

    try:
        response = requests.post(TOGETHER_API_URL, headers=headers, json=data)
        response_json = response.json()
        reply = response_json["choices"][0]["message"]["content"]
    except Exception as e:
        reply = "Une erreur est survenue lors de la réponse de l’IA. Détail : " + str(e)

    return render_template("index.html", response=reply)

if __name__ == "__main__":
    app.run(debug=True)
