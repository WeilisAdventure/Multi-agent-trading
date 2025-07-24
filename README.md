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

