from flask import Flask, request, jsonify
from google.cloud import firestore
import yfinance as yf
import pandas as pd
import os
import json
import base64

app = Flask(__name__)
db = firestore.Client()

def get_technical_indicators(ticker="AAPL"):
    df = yf.download(ticker, period="1mo", interval="1d")

    if df.empty or len(df) < 20:
        raise ValueError("Insufficient data to compute indicators.")

    df['SMA20'] = df['Close'].rolling(window=20).mean()
    df['RSI'] = 100 - (100 / (1 + df['Close'].pct_change().rolling(14).mean()))
    df.dropna(inplace=True)

    if df.empty:
        raise ValueError("Insufficient data after computing indicators.")

    latest = df.iloc[-1]

    # Safely extract scalar values
    close = latest['Close'].item() if hasattr(latest['Close'], 'item') else latest['Close']
    sma20 = latest['SMA20'].item() if hasattr(latest['SMA20'], 'item') else latest['SMA20']
    rsi = latest['RSI'].item() if hasattr(latest['RSI'], 'item') else latest['RSI']

    if pd.isna(close) or pd.isna(sma20) or pd.isna(rsi):
        raise ValueError("Indicator values are NaN")

    signal = "Buy" if close > sma20 and rsi < 70 else "Sell"

    return {
        "ticker": ticker,
        "Close": round(close, 2),
        "SMA20": round(sma20, 2),
        "RSI": round(rsi, 2),
        "signal": signal
    }

@app.route("/", methods=["GET"])
def home():
    return "Technical Agent is live!", 200

@app.route("/", methods=["POST"])
def handle_pubsub():
    try:
        envelope = request.get_json()
        print("Received envelope:", envelope)

        if not envelope or 'message' not in envelope:
            print("No Pub/Sub message in envelope.")
            return "Bad Request: No Pub/Sub message found", 400

        message = envelope['message']
        if 'data' not in message:
            print("No 'data' field in Pub/Sub message.")
            return "Bad Request: No data field", 400

        # Decode base64 data
        payload_json = base64.b64decode(message['data']).decode("utf-8")
        print("Decoded payload:", payload_json)

        payload = json.loads(payload_json)
        request_id = payload.get("request_id")
        ticker = payload.get("symbol", "AAPL")  # <-- Fix here: not price_data, it's just symbol

        if not request_id:
            print("Missing request_id.")
            return "Bad Request: request_id required", 400

        print(f"Running indicator analysis for: {ticker}")
        result = get_technical_indicators(ticker)
        print(f"Result: {result}")

        print(f"Writing to Firestore: agent_results/{request_id}")
        db.collection("agent_results").document(request_id).set({
            "technical": result
        }, merge=True)

        return "Processed", 200

    except Exception as e:
        print("Exception occurred:", str(e))
        return f"Internal Server Error: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
