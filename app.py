from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

COHERE_API_KEY = "J0haoqYmMhXnpywSfioaKe736XrLYtAyyqpA4mpk"  # Colle ta vraie clé Cohere ici
COHERE_API_URL = "https://api.cohere.ai/generate"

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
        "model": "xlarge",  # modèle gratuit disponible
        "prompt": user_input,
        "max_tokens": 500,
        "temperature": 0.7
    }

    try:
        res = requests.post(COHERE_API_URL, headers=headers, json=data)
        res.raise_for_status()
        result = res.json()
        # Ici Cohere retourne un champ "generations" ou "text"
        # Exemple selon l’API :
        if "generations" in result:
            reply = result["generations"][0]["text"]
        else:
            reply = result.get("text", str(result))
    except requests.exceptions.RequestException as e:
        reply = f"Erreur API (requête) : {str(e)}"
    except Exception as e:
        reply = f"Erreur API inattendue : {str(e)}"

    return render_template("index.html", response=reply)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
