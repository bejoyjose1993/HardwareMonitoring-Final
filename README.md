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
- **Deployment**: Azure VM instance
---


## 🧱 Architecture Overview

1] [ Angular App ] --> [ Spring Cloud Gateway ] --> [ Spring Boot Services ] | [ MySQL | Redis ]

2] [ Angular App ] --> [ Spring Cloud Gateway ] --> [ Pythod_Edge Monitor ]

3] [ Spring Boot Services ] --> [ Kafka ] --> [ Spring Notification Services ]

![Sysstem Architecture](Design%20Documents/System%20Architecture%20(2).jpg)


Each component is containerized using Docker and orchestrated via Docker Compose for local development and deployment on an Azure VM instance.

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
| Cloud Services         | Azure VM                                               |

---


## 🛠️ Prerequisites
- Docker & Docker Compose installed
- Open ports: `8080`, `8082`, `8083`, `4200`, `8000`
---


## 🚀 Getting Started (Installation and run instructions)
### 1. Clone the Repository

```bash
git clone https://github.com/bejoyjose1993/HardwareMonitoring-Final.git
cd HardwareMonitoring-Final
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


## Azure CICD Deployment using GitHub Actions 
A full-stack, containerized **Edge Monitor Application** deployed to an Azure VM instance using **GitHub Actions for automated CI/CD**, **Docker Compose**, and **Azure Container Registry**

Note:- Azure VM instance will only have the folder  /HardwareMonitoring-Final with below files
- docker-compose.yml (Make sure its upto date and latest pulled from repo)
- docker-compose.prod.yml (Make sure its upto date and latest pulled from repo)
- .evn.production
- /mysql/init/init.sql
- .git
- .gitignore
- ReadMe.md (Not Required)

### 🧱 Tech Stack
| Layer      | Technology                |
|------------|---------------------------|
| CI/CD      | GitHub Actions            |
| Deployment | Azure VM + Docker Compose |

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
3. **Tag** and **push** to Azure Container Registry.
4. **SSH into VM** using `appleboy/ssh-action`. Log into Azure Container Registry from VM.
5. **Pull latest containers** via Docker Compose.
6. **Removes all** currently running containers using Docker Compose.
7. **Restart containers** with new images via Docker Compose.
8. **Prune** unused Images.

### 📂 Workflow file: `.github/workflows/deploy.yml`
```bash
name: CI/CD Pipeline - Azure

on:
  push:
    branches: [ "main" ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Set up Docker
      uses: docker/setup-buildx-action@v3
      
    # Step 1 — Log in to Azure Container Registry (ACR)
    - name: Log in to Azure Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ secrets.AZURE_REGISTRY_NAME }}.azurecr.io
        username: ${{ secrets.AZURE_REGISTRY_USERNAME }}
        password: ${{ secrets.AZURE_REGISTRY_PASSWORD }}

    # Step 2 — Build and Push backend 
    - name: Build and push edgemonitor-backend image
      run: |
        docker build -t ${{ secrets.AZURE_REGISTRY_NAME }}.azurecr.io/edgemonitor_backend:latest ./edgemonitor-backend
        docker push ${{ secrets.AZURE_REGISTRY_NAME }}.azurecr.io/edgemonitor_backend:latest

    # Step 3 — Build and Push gateway
    - name: Build and push edgemonitor_gateway image
      run: |
        docker build -t ${{ secrets.AZURE_REGISTRY_NAME }}.azurecr.io/edgemonitor_gateway:latest ./edgemonitor-gateway
        docker push ${{ secrets.AZURE_REGISTRY_NAME }}.azurecr.io/edgemonitor_gateway:latest

    # Step 4 — Build and Push notification service
    - name: Build and push edgemonitor_notification service image
      run: |
        docker build -t ${{ secrets.AZURE_REGISTRY_NAME }}.azurecr.io/edgemonitor_notification:latest ./edgemonitor-notification
        docker push ${{ secrets.AZURE_REGISTRY_NAME }}.azurecr.io/edgemonitor_notification:latest

    # Step 5 — Build and Push Edge Monitor (Python)
    - name: Build and push edge_monitor service image
      run: |
        docker build -t ${{ secrets.AZURE_REGISTRY_NAME }}.azurecr.io/edge_monitor:latest ./edge_monitor
        docker push ${{ secrets.AZURE_REGISTRY_NAME }}.azurecr.io/edge_monitor:latest

    # Step 6 — Build and Push frontend (Angular)
    - name: Build and push edge_monitor_dashboard image
      run: |
        docker build \
          --build-arg BASE_API_URL=${{ secrets.BASE_API_URL }} \
          --build-arg FAST_BASE_API_URL=${{ secrets.FAST_BASE_API_URL }} \
          -t ${{ secrets.AZURE_REGISTRY_NAME }}.azurecr.io/edgemonitor_dashboard:latest ./edge_monitor_dashboard
        docker push ${{ secrets.AZURE_REGISTRY_NAME }}.azurecr.io/edgemonitor_dashboard:latest

    # Step 7 — Deploy to Azure VM (via SSH)
    - name: Deploy to Azure VM
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.AZURE_VM_HOST }}
        username: azureuser
        key: ${{ secrets.AZURE_VM_SSH_KEY }}
        script: |
          echo "Logging into Azure Container Registry..."
          docker login ${{ secrets.AZURE_REGISTRY_NAME }}.azurecr.io \
            -u ${{ secrets.AZURE_REGISTRY_USERNAME }} \
            -p ${{ secrets.AZURE_REGISTRY_PASSWORD }}

          cd ~/HardwareMonitoring-Final
          docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env.production pull
          docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env.production down
          docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env.production up -d
          docker image prune -a -f

```

###  GitHub Secrets Required 
| Secret Name               | Description                                 |
| --------------------------| ------------------------------------------- |
| `AZURE_REGISTRY_NAME`     | Your Azure Registry name                    |
| `AZURE_REGISTRY_USERNAME` | Your Azure Container Registry username      |
| `AZURE_REGISTRY_PASSWORD` | Your Azure Container Registry password      |
| `AZURE_VM_HOST`           | Public IP or domain of your Azure VM        |
| `AZURE_VM_SSH_KEY`        | Your Azure private key (`.pem`) as a secret |
| `BASE_API_URL`            | http://xx.xx.xxx.xx:8082                    |
| `FAST_API_URL`            | http://xx.xx.xxx.xx:8000                    |

###  ✅ How to Deploy
Just push code to the main branch — that’s it!
git add .
git commit -m "Your changes"
git push origin main

GitHub Actions will:
-Build → Push → Deploy
-No manual steps required.

## If the Azure VM Ip changes
Note:- If you start and stop the Azure instance the public ip doestn't change unlike in EC2 W/O EIP 
Here if the VM ip changes we might require changing the EC2_HOST and BASE_API_URL to the latest URL and also manually update .env.production file in the VM instance.

1] Inside .env.production (Chnage following field values *APP_CORS_ALLOWED_ORIGINS Field change = Public IPv4 address and Public DNS) e.g. -> APP_CORS_ALLOWED_ORIGINS=http://xx.xx.xxx.xx,http://xx.xx.xxx.xx:4200.

2] Change EC2_HOST inside secrets (To Public IPv4 address) e.g. ->  xx.xx.xxx.xx

3] BASE_API_URL should be changed to Public IPv4 address:8082. e.g. For EC2 -> http://xx.xx.xxx.xx:8082

4] FAST_API_URL should be changed to Public IPv4 address:8000. e.g. For EC2 -> http://xx.xx.xxx.xx:8000

## Testing Endpoints
You can test backend APIs via(If rules are set correctly):

```bash
curl http://<ec2-public-ip>:8082/api/auth/hello
```
Use tools like Postman for more complex testing.


## Azure VM Manual Deployment Instructions
### 1. Use Azure Console (using Bastion) or SSH into VM

Authentication Type : SSH Private Key from Local File
Username: Your VM username
Local File: Your saved "*.pem" file

### 2. Install Docker & Docker Compose
```bash
# 1] Update Ubuntu packages
   sudo apt update
   sudo apt upgrade -y

# 2] Install Docker
   sudo apt install -y docker.io
   sudo systemctl start docker
   sudo systemctl enable docker
   sudo usermod -aG docker $USER
   
   # Log out and back in for the group change to take effect
   exit
   # Reconnect and check docker
   docker --version

# 3] Remove legacy Docker Compose packages
   sudo apt remove docker-compose python3-compose -y

# 4] Add Docker official repository (for Compose plugin)
   sudo apt install -y ca-certificates curl gnupg lsb-release
   sudo mkdir -p /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
   
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   sudo apt update

# 5] Install Docker Compose V2 plugin
   sudo apt install docker-compose-plugin -y
   docker compose version
```

### 3. Clone and Run

```bash
git clone https://github.com/bejoyjose1993/HardwareMonitoring-Final.git
cd HardwareMonitoring-Final
docker-compose --env-file .env.local up --build
```

### 5. Expose IP and Ports 

✅ Step-by-Step: Setting Inbound Rules on Azure Console
-  Log in to the Azure Console
-  Search Network security group
-  Identify the Security Group
-  Navigate to "*-nsg"
-  Open Setting tab > Inbound security rules
-  Click + ADD button
-  ADD Inbound Rules

| Type         | Protocol | Port Range | Priority   | Source               | Description                        |
| ------------ | -------- | ---------- | ---------- | -------------------- | ---------------------------------- |
| Custom TCP   | TCP      | 8080       | 1000       | Your IP              | Spring Backend                     |
| Custom TCP   | TCP      | 8082       | 1001       | Your IP              | Spring Gateway                     |
| Custom TCP   | TCP      | 8000       | 1003       | Your IP              | Python EdgeMonitor                 |
| Custom TCP   | TCP      | 4200       | 1002       | Your IP or 0.0.0.0/0 | Angular Dev Server                 |
| HTTP         | TCP      | 80         | 8082       | Anywhere (0.0.0.0/0) | For web traffic (if using port 80) |
| HTTPS        | TCP      | 443        | 8082       | Anywhere             | For HTTPS (optional)               |
| SSH          | TCP      | 22         | 8082       | Your IP              | SSH access                         |

 
 
