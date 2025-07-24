# web_interface/Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install flask requests gunicorn google-cloud-pubsub google-cloud-firestore
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 app:app
