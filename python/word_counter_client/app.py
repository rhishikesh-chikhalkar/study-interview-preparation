import os
from flask import Flask, render_template, request, jsonify
import httpx

app = Flask(__name__)

# Configurable Go service URL
GO_SERVICE_URL = os.environ.get("GO_SERVICE_URL", "http://localhost:8081/count")


@app.route("/", methods=["GET", "POST"])
def index():
    word_count = None
    character_count = None
    error = None
    text_input = ""

    if request.method == "POST":
        text_input = request.form.get("text", "")
        if text_input:
            try:
                # Call Go service via HTTP POST
                with httpx.Client(timeout=5.0) as client:
                    response = client.post(GO_SERVICE_URL, json={"text": text_input})

                if response.status_code == 200:
                    data = response.json()
                    word_count = data.get("word_count", 0)
                    character_count = data.get("character_count", 0)
                else:
                    error = f"Go Service returned status code {response.status_code}: {response.text}"
            except Exception as e:
                error = f"Failed to connect to Go Service: {str(e)}"
        else:
            word_count = 0
            character_count = 0

    return render_template(
        "index.html",
        text_input=text_input,
        word_count=word_count,
        character_count=character_count,
        error=error,
    )


@app.route("/api/count", methods=["POST"])
def api_count():
    """API endpoint to forward count requests directly"""
    req_data = request.get_json() or {}
    text_input = req_data.get("text", "")

    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.post(GO_SERVICE_URL, json={"text": text_input})
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify(
                {"error": f"Go Service Error: {response.text}"}
            ), response.status_code
    except Exception as e:
        return jsonify({"error": f"Connection Error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(port=5001, debug=True)
