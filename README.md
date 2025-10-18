# 🚀 Full Stack Dockerized Application "# Edge-Monitor" 

This repository contains a **Dockerized Full-Stack Application** with the following tech stack:

- **Edge Monitor Backend**: Python  
- **Frontend**: Angular  
- **Backend**: Spring Boot  
- **API Gateway**: Spring Cloud Gateway
- **Mailing Micro-Service**: Spring Boot 
- **Database**: MySQL  
- **Caching**: Redis  
- **Queueing**: Kafka  
- **Deployment**: AWS EC2 instance
---

## 🧱 Architecture Overview

[ Angular App ] --> [ Spring Cloud Gateway ] --> [ Spring Boot Services ]
| [ MySQL | Redis ]

![Sysstem Architecture](Design%20Documents/System%20Architecture%20(2).png)


Each component is containerized using Docker and orchestrated via Docker Compose for local development and deployment on an AWS EC2 instance.

---

## ✅ Workflow

1. **EdgeMonitor** collects CPU, RAM, Disk, GPU, and temperature metrics every few seconds.  
2. Sends metrics via **HTTP POST** to the FastAPI `/ingest` endpoint.  
3. FastAPI stores the latest metrics in memory (`metrics_store`).  
4. Clients can query `/metrics` to get the most recent metrics.  
5. Both EdgeMonitor and FastAPI run **concurrently** using `asyncio`.  

## 📦 Tech Stack

| Layer                  | Technology                                             |
|------------------------|--------------------------------------------------------|
| Frontend               | Angular                                                |
| Edge Monitor Backend   | Python                                                 |
| Auth Backend           | Spring Boot                                            |
| API Gateway            | Spring Cloud Gateway                                   |
| Mailing Micro-Service  | Spring Boot                                            |
| Database               | MySQL                                                  |
| Caching                | Redis                                                  |
| Notification Queue     | Kafka                                                  |
| Deployment             | Docker, Docker Compose                                 |
| CICD                   | Git Actions                                            |
| AWS Services           | AWS EC2                                                |

---


## 🛠️ Prerequisites
- Docker & Docker Compose installed
- Open ports: `8080`, `8082`, `8083`, `4200`, `8000`
---


## 🚀 Getting Started (Installation and run instructions)
### 1. Clone the Repository

```bash
git clone https://github.com/bejoyjose1993/HardwareMonitoring.git
cd HardwareMonitoring
```


### 2. Create Enviornment Files (.env.local)
```bash
# .env — Deployment config
# API URL
BASE_API_URL=http://localhost:8082

# MySQL
DB_URL=jdbc:mysql://host.docker.internal:3306/your_db_name
DB_USERNAME=your_db_user_name
DB_PASSWORD=your_db_password
DB_DATABASE=your_db_name
DB_PORT=3306

# Redis
REDIS_HOST=host: host.docker.internal
REDIS_PORT=6379

# Zookeeper
ZOOKEEPER_PORT=2181

# Kafka
KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092
KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092
KAFKA_PORT=9092

# Backend
BACKEND_PORT=8080

# Gateway
GATEWAY_PORT=8082
GATEWAY_SERVICE_URI=http://host.docker.internal:8080
APP_CORS_ALLOWED_ORIGINS=http://localhost:4200

# Frontend
FRONTEND_PORT=4200

# Mailing (Notifiucation Service)
NOTIFICATION_PORT=8083
MAIL_USERNAME=your_own_emailId
MAIL_PASSWORD=your_own_generated_password_to_access_email_client
KAFKA_BOOTSTRAP_SERVER=kafka:9092

# Docker image tags (optional for versioning)
IMAGE_TAG=latest

# EDGE MONITOR
EDGE_MONITOR_PORT=8000
EDGE_MONITOR_TRANSPORT=http
EDGE_MONITOR_ENDPOINT=http://edge_monitor:8000/ingest
EDGE_MONITOR_INTERVAL=5
```

### 3. Build and Run with Docker Compose

```bash
docker-compose --env-file .env.local up --build
```

### 4. Access the Application

Frontend (Angular): http://localhost:4200

API Gateway: http://localhost:8082

MySQL: port 3306

Redis: port 6379

## 🚀 User Interface

### 1. Login Page

![Login Page](User%20Interface%20Images/Edge-Monitor%20LogIn%20Page.png)

### 2. SignIn Page

![SignUp Page](User%20Interface%20Images/Edge-Monitor%20SignUp%20Page.png)

### 3. Dashboard Page

![Dashboard Page](User%20Interface%20Images/Edge-Monitor%20Dashboard%20Page.png)


## Loom Video Link

https://www.loom.com/share/29842c0f5d9748e68b42c76efc74262e?sid=46512cf1-5cd0-49e8-98bb-5d59938567ae



## EC2 CICD Deployment using GitHub Actions 
A full-stack, containerized **Edge Monitor Application** deployed to an AWS EC2 instance using **GitHub Actions for automated CI/CD**, **Docker Compose**, and **Docker Hub**

Note:- EC2 instance will only have the folder  /HardwareMonitoring with below files
- docker-compose.yml (Make sure its upto date and latest pulled from repo)
- docker-compose.prod.yml (Make sure its upto date and latest pulled from repo)
- .evn.production
- /mysql/init/init.sql
- .git
- .gitignore
- ReadMe.md (Not Required)

### 🧱 Tech Stack
| Layer      | Technology               |
|------------|--------------------------|
| CI/CD      | GitHub Actions           |
| Deployment | AWS EC2 + Docker Compose |

## 🚀 Automated CI/CD Workflow
### ✅ Trigger:
> On every push to the `main` branch.

### 🛠️ GitHub Actions Flow:
1. **Build Docker images** for:
   - `edge_monitor`
   - `edgemonitor-backend`
   - `edgemonitor-gateway`
   - `edgemonitor-notification`
   - `edge_monitor_dashboard`
3. **Tag** and **push** to Docker Hub.
4. **SSH into EC2** using `appleboy/ssh-action`.
5. **Pull latest Docker images**.
6. **Restart containers** via Docker Compose.

### 📂 Workflow file: `.github/workflows/deploy.yml`
```bash
name: CI/CD Pipeline

on:
  push:
    branches: [ "main" ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Docker
      uses: docker/setup-buildx-action@v3
      
    - name: Log in to Docker Hub
      uses: docker/login-action@v3
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
        
    - name: Build and push edgemonitor-backend image
      run: |
        docker build -t bejoyjose/edgemonitor_backend ./edgemonitor-backend
        docker push bejoyjose/edgemonitor_backend:latest

    - name: Build and push edgemonitor_gateway image
      run: |
        docker build -t bejoyjose/edgemonitor_gateway ./edgemonitor-gateway
        docker push bejoyjose/edgemonitor_gateway:latest

    - name: Build and push edgemonitor_notification service image
      run: |
        docker build -t bejoyjose/edgemonitor_notification ./edgemonitor-notification
        docker push bejoyjose/edgemonitor_notification:latest

    - name: Build and push edge_monitor service image
      run: |
        docker build -t bejoyjose/edge_monitor ./edge_monitor
        docker push bejoyjose/edge_monitor:latest

    - name: Build and push edge_monitor_dashboard image
      run: |
        docker build \
          --build-arg BASE_API_URL=${{ secrets.BASE_API_URL }} \
          --build-arg FAST_BASE_API_URL=${{ secrets.FAST_BASE_API_URL }} \
          -t bejoyjose/edge_monitor_dashboard ./edge_monitor_dashboard
        docker push bejoyjose/edge_monitor_dashboard:latest

    - name: Deploy to EC2
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.EC2_HOST }}
        username: ec2-user
        key: ${{ secrets.EC2_SSH_KEY }}
        script: |
          docker pull bejoyjose/edgemonitor_backend:latest
          docker pull bejoyjose/edgemonitor_gateway:latest
          docker pull bejoyjose/edgemonitor_notification:latest
          docker pull bejoyjose/edge_monitor_dashboard:latest
          docker pull bejoyjose/edge_monitor:latest
          cd /home/ec2-user/HardwareMonitoring
          docker-compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env.production pull
          docker-compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env.production down
          docker-compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env.production up -d
          docker image prune -a -f
```

###  GitHub Secrets Required 
| Secret Name       | Description                               |
| ----------------- | ----------------------------------------- |
| `DOCKER_USERNAME` | Your Docker Hub username                  |
| `DOCKER_PASSWORD` | Your Docker Hub password/security token   |
| `EC2_HOST`        | Public IP or domain of your EC2           |
| `EC2_SSH_KEY`     | Your EC2 private key (`.pem`) as a secret |
| `BASE_API_URL`    | http://xx.xx.xxx.xx:8082                  |
| `FAST_API_URL`    | http://xx.xx.xxx.xx:8000                  |

###  ✅ How to Deploy
Just push code to the main branch — that’s it!
git add .
git commit -m "Your changes"
git push origin main

GitHub Actions will:
-Build → Push → Deploy
-No manual steps required.

## On Restart of EC2 (As EIP is not configured)
Note:- If you start and stop the EC2 instance the public ip will change and hence we might require changing the EC2_HOST and BASE_API_URL to the latest URL and also manually update .env.production file in the EC2 instance. This is because we aint using Elastic ip.

1] Inside .env.production (Chnage following field values *APP_CORS_ALLOWED_ORIGINS Field change = Public IPv4 address and Public DNS) e.g. -> APP_CORS_ALLOWED_ORIGINS=http://xx.xx.xxx.xx,http://ec2-xx-xx-xxx-xx.eu-north-1.compute.amazonaws.com

2] Change EC2_HOST inside secrets (To Public IPv4 address) e.g. ->  xx.xx.xxx.xx

3] BASE_API_URL should be changed to Public IPv4 address:8082. e.g. For EC2 -> http://xx.xx.xxx.xx:8082

4] FAST_API_URL should be changed to Public IPv4 address:8000. e.g. For EC2 -> http://xx.xx.xxx.xx:8000

Note:- Used Kafka Docker image, can also use MSK but its not available of free tire.

## Testing Endpoints
You can test backend APIs via(If rules are set correctly):

```bash
curl http://<ec2-public-ip>:8082/api/auth/hello
```
Use tools like Postman for more complex testing.

