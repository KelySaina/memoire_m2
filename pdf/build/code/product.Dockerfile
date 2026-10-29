FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
# Dockerfile
ARG VERSION
ARG BUILD_DATE

# Optional: write version info into a JSON file inside the image
RUN echo "{\"version\":\"${VERSION}\",\"date\":\"${BUILD_DATE}\"}" > /app/version.json

CMD ["python", "app.py"]