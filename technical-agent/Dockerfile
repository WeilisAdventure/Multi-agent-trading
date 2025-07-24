# technical_agent/Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install yfinance flask google-cloud-firestore
CMD ["python", "technical_agent.py"]
