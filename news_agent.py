from flask import Flask, request, jsonify
from google.cloud import firestore
import google.generativeai as genai
import os
import base64
import json
import re

app = Flask(__name__)
db = firestore.Client()

# Configure Gemini API key from environment variable
genai.configure(api_key="AIzaSyCeMBLHYdNSrJH9oCWY9x5lFv9M27BoQ40")

model = genai.GenerativeModel("gemini-2.0-flash-lite")

def analyze_sentiment(text):
    prompt = (
        f"Analyze the sentiment of this news: \"{text}\".\n"
        "Return output like:\n"
        "**Sentiment:** Positive\n"
        "**Confidence:** 92%\n"
        "**Summary:** Summary of the sentiment reasoning."
    )

    response = model.generate_content(prompt)
    raw = response.text.strip()

    # Use regex to extract sentiment, confidence, and summary
    sentiment_match = re.search(r"\*\*Sentiment:\*\*\s*(.+)", raw)
    confidence_match = re.search(r"\*\*Confidence:\*\*\s*(.+)", raw)
    summary_match = re.search(r"\*\*Summary:\*\*\s*(.+)", raw)

    return {
        "sentiment": sentiment_match.group(1).strip() if sentiment_match else "Unknown",
        "confidence": confidence_match.group(1).strip() if confidence_match else "Unknown",
        "summary": summary_match.group(1).strip() if summary_match else "No summary available.",
        # "raw_response": raw
    }


@app.route("/", methods=["POST"])
def handle_pubsub():

    try:
        envelope = request.get_json(force=True, silent=True)
        if not envelope or "message" not in envelope:
            return "Invalid Pub/Sub message", 400

        message = envelope["message"]

        if "data" not in message:
            return "Missing 'data' in Pub/Sub message", 400

        data = json.loads(base64.b64decode(message["data"]).decode("utf-8"))

        request_id = data.get("request_id")
        news_text = data.get("text", "")

        if not request_id:
            return "Missing request_id", 400

        result = analyze_sentiment(news_text)
        print("Writing to Firestore:", result)

        db.collection("agent_results").document(request_id).set({
            "news": result
        }, merge=True)

        return jsonify({"status": "News sentiment stored"}), 200
    except Exception as e:
        print("Error during processing:", e)
        return f"Error: {str(e)}", 500

@app.route("/", methods=["GET"])
def health_check():
    return "News Agent is running!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
