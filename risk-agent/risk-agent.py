from flask import Flask, request, jsonify
from google.cloud import firestore
import os
import base64
import json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
db = firestore.Client()

def analyze_risk(risk_data):
    position = risk_data.get("position", 0)

    if position >= 200000:
        rating = "High"
    elif position >= 50000:
        rating = "Medium"
    else:
        rating = "Low"

    return {
        "position": position,
        "rating": rating,
        "analysis": f"Position of ${position} assessed as {rating} risk."
    }

@app.route("/", methods=["POST"])
def handle_pubsub():
    try:
        envelope = request.get_json()
        if not envelope or "message" not in envelope:
            return "Invalid Pub/Sub message", 400

        message = envelope["message"]
        decoded_data = base64.b64decode(message["data"]).decode("utf-8")
        data = json.loads(decoded_data)

        request_id = data.get("request_id")
        risk_data = data.get("risk_data", {})

        if not request_id:
            return "Missing request_id", 400

        result = analyze_risk(risk_data)
        print(f"Risk result for {request_id}: {result}")

        db.collection("agent_results").document(request_id).set({
            "risk": result
        }, merge=True)

        return jsonify({"status": "Risk analysis stored"}), 200

    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {str(e)}", 500

@app.route("/", methods=["GET"])
def health_check():
    return "Risk Agent is running!", 200

if __name__ == "__main__":
    port = int(os.environ.get("RISK_AGENT_PORT", 8080))
    app.run(host="0.0.0.0", port=port)
