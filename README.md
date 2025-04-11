# SwissHacks25-Priceless

This project is managed with Docker Compose. Below are the details of the services, their exposed ports, and how to run them.

## Available Commands

### Development Mode

docker compose -f compose.dev.yml up --build 

docker compose -f compose.dev.yml down --volumes


### Production Mode

docker compose -f compose.prod.yml up --build 

docker compose -f compose.prod.yml down --volumes


## Services Overview

### Frontend - Vue 3
- Repository: [https://github.com/HackathonCliTemplate/frontend-vue3-template.git](https://github.com/HackathonCliTemplate/frontend-vue3-template.git)
- Exposed Ports: `5173:5173`, `8080:8080`
- Depends on: `backend`

### Backend - FlaskAPI
- Repository: [https://github.com/HackathonCliTemplate/api-flask-static-template.git](https://github.com/HackathonCliTemplate/api-flask-static-template.git)
- Exposed Ports: `5000:5000`, `5000:5000`
- Volumes: `./backend:/app`

### Database - MongoDB
- Image: `mongo:latest`
- Exposed Ports: `27017:27017`, `27017:27017`

