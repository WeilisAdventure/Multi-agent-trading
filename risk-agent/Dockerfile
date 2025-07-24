# risk_agent/Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install flask numpy google-cloud-firestore
CMD ["python", "risk_agent.py"]
