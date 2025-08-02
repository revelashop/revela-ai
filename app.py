from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# ✅ Ta clé API OpenRouter
OPENROUTER_API_KEY = "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"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form["user_input"]

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mixtral-8x7b-instruct",
        "messages": [
            {"role": "system", "content": "Tu es un assistant IA qui aide à créer des marques, projets et idées créatives."},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.7,
        "max_tokens": 500,
        "top_p": 1
    }

    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        reply = response_json["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        reply = f"Erreur API (requête) : {str(e)}"
    except KeyError:
        reply = f"Erreur API : Clé 'choices' introuvable. Réponse brute : {response.text}"
    except Exception as e:
        reply = f"Erreur inconnue : {str(e)}"

    return render_template("index.html", response=reply)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
