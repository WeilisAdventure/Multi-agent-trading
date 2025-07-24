# news_agent/Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install flask google-generativeai google-cloud-firestore
CMD ["python", "news_agent.py"]
