# Multi-agent-trading
# Cloud-Native Multi-Agent Trading Support System (GCP)

This project implements a cloud-native multi-agent trading support system on Google Cloud Platform (GCP). It uses:

- **Cloud Run** to deploy containerized agents
- **Pub/Sub** for agent communication
- **Firestore** for storing analysis results
- **Flask Web UI** for triggering requests and displaying results

## 📦 Docker Images (Hosted on Docker Hub and GCP Artifact)

All components are Dockerized and hosted on Docker Hub:

- [`technical-agent`](https://hub.docker.com/repository/docker/wwang9/myrep/general)
- [`risk-agent`](https://hub.docker.com/repository/docker/wwang9/myrep/general)
- [`news-agent`](https://hub.docker.com/repository/docker/wwang9/myrep/general)
- [`web-interface`](https://hub.docker.com/repository/docker/wwang9/myrep/general)

## 🧪 How to Consume the Service

### Option 1: Locally with Docker

```bash
docker pull wwang9/myrep/technical-agent
docker pull wwang9/myrep/risk-agent
docker pull wwang9/myrep/news-agent
docker pull wwang9/myrep/web-interface

docker run -p 8080:8080 wwang9/myrep/web-interface
Then go to: http://localhost:8080

### Option 2: Cloud-Hosted on GCP
Each agent is deployed on Cloud Run with public URLs.
[technical-agent](https://technical-agent-171318020464.us-central1.run.app)
[risk-agent](https://risk-agent-171318020464.us-central1.run.app)
[news-agent](https://news-agent-171318020464.us-central1.run.app)
[web-interface](https://web-interface-171318020464.us-central1.run.app)

Type the url https://web-interface-171318020464.us-central1.run.app and enter to run the app.

The Web UI lets users:
Enter a stock symbol and request analysis
Wait for background agents to complete processing
View results retrieved from Firestore

🔄 Agent Communication via Pub/Sub
Each agent listens to its own Pub/Sub topic:
technical-signals-topic
risk-analysis-topic
news-analysis-topic

The web UI publishes  messages like:
Ticker: AAPL
Closing Price: $213.76
RSI: 0.01
SMA20: $209.98
Signal: Buy

Firestore Result Schema
Results are stored under a results collection:
Document ID: request_id
Fields:
technical: ...
risk: ...
news: ...
Web UI polls this until all three are present.

Environment Setup
Enable these GCP services:
Cloud Run
Pub/Sub
Firestore
Artifact Registry (optional)

bash
gcloud services enable run.googleapis.com pubsub.googleapis.com firestore.googleapis.com
