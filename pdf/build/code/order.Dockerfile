FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --production
COPY . .
# Dockerfile
ARG VERSION
ARG BUILD_DATE

# Optional: write version info into a JSON file inside the image
RUN echo "{\"version\":\"${VERSION}\",\"date\":\"${BUILD_DATE}\"}" > /app/version.json

CMD ["node", "index.js"]