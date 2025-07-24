from flask import Flask, request, render_template, redirect, url_for
from google.cloud import firestore, pubsub_v1
import uuid
import json
import os

app = Flask(__name__)
db = firestore.Client()
publisher = pubsub_v1.PublisherClient()
PROJECT_ID = "augmented-atom-466412-s2"

TOPICS = {
    "tech": publisher.topic_path(PROJECT_ID, "tech-topic"),
    "risk": publisher.topic_path(PROJECT_ID, "risk-topic"),
    "news": publisher.topic_path(PROJECT_ID, "news-topic"),
}

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    request_id = request.args.get("request_id", "")
    if request.method == "POST":
        request_id = request.form.get("request_id", "").strip()
        return redirect(url_for("index", request_id=request_id))

    if request_id:
        doc = db.collection("agent_results").document(request_id).get()
        if doc.exists:
            result = doc.to_dict()

    return render_template("index.html", result=result, request_id=request_id)


@app.route("/submit", methods=["POST"])
def submit():
    symbol = request.form.get("symbol", "AAPL")
    risk = request.form.get("risk", "100000")
    news = request.form.get("news", "Apple just announced a new AI feature.")
    # print(news)
    request_id = str(uuid.uuid4())

    # Publish to tech agent
    publisher.publish(TOPICS["tech"], json.dumps({
        "request_id": request_id,
        "symbol": symbol
    }).encode("utf-8"))

    # Publish to risk agent
    publisher.publish(TOPICS["risk"], json.dumps({
        "request_id": request_id,
        "risk_data": {
            "position": float(risk)
        }
    }).encode("utf-8"))

    # Publish to news agent
    publisher.publish(TOPICS["news"], json.dumps({
        "request_id": request_id,
        "text": news
    }).encode("utf-8"))

    return redirect(f"/results/{request_id}?symbol={symbol}&risk={risk}&news={news}")

@app.route("/results/<request_id>")
def results(request_id):

    doc = db.collection("agent_results").document(request_id).get()

    result = doc.to_dict() if doc.exists else {}

    # Get query params to preserve submitted values
    symbol = request.args.get("symbol", "")
    risk = request.args.get("risk", "")
    news = request.args.get("news", "")

    return render_template("index.html", request_id=request_id, symbol=symbol, risk=risk, news=news, result=result)
