# 🎓 Student Performance Prediction MLOps Pipeline

An end-to-end production-grade **Machine Learning System Design (MLSD)** and **MLOps** project designed for predicting student grades ("Fail", "Pass", "Distinction") using customer/student demographic and academic metrics.

This project implements a complete automated CI/CD pipeline, data version control, containerization, and orchestration, mimicking the architecture of the **MLSD Cryotherapy Project** from our clinical study blueprints.

---

## 🛠️ Technology Stack

* **Core Logic**: Python 3.9, Pandas, NumPy, Scikit-Learn
* **Experiment Tracking**: **MLflow** (metrics, parameters, model registry, artifact storage)
* **Data Versioning**: **DVC (Data Version Control)** integrated with **AWS S3**
* **Application Frontend**: **Streamlit** (interactive prediction dashboard with glassmorphism UI)
* **Containerization**: **Docker**
* **Orchestration**: **Kubernetes (k8s)** (Deployment with 2 pod replicas, exposing service via NodePort)
* **CI/CD Automation**: **GitHub Actions**

---

## 📂 Directory Layout

```text
mlops-student-performance/
├── .github/
│   └── workflows/
│       └── ml.yml                 # GitHub Actions CI/CD pipeline
├── data/
│   └── student_dataset.csv        # DVC-tracked cleaned dataset
├── k8s/
│   └── k8s-config.yaml            # Kubernetes service & pod orchestration manifest
├── models/                        # Serialized model pickles directory (git-ignored)
├── outputs/                       # Confusion matrix plot images (git-ignored)
├── .gitignore                     # Git tracking exclusions
├── app.py                         # Streamlit interactive prediction web application
├── Dockerfile                     # Streamlit container packaging instructions
├── dvc.yaml                       # DVC pipeline stage definition
├── params.yaml                    # ML parameters and directory paths config
├── requirements.txt               # Pinned library dependencies
└── README.md                      # Complete system documentation
```

---

## ⚙️ Initial Setup & Local Installation

### 1. Provision Virtual Environment
On Windows, open **Git Bash** (or PowerShell) in the project directory and run:
```bash
# Create environment
python -m venv venv

# Activate environment
source venv/Scripts/activate
```

### 2. Install Package Dependencies
Install all pinned libraries (NumPy, Scikit-Learn, Streamlit, MLflow, DVC with S3 support, etc.):
```bash
pip install -r requirements.txt
```

### 3. Initialize Git & Connect Remote Origin
```bash
git init
git remote add origin https://github.com/Rahul-git64/mlops-student-performance.git
git branch -M main
```

---

## 🚀 Pipeline Core Execution

### 1. Run Data Versioning (DVC)
To set up remote data storage backing your dataset to your AWS S3 bucket:
```bash
# Initialize DVC
dvc init

# Set AWS S3 remote storage location
dvc remote add -d s3remote s3://mlops-student-performance

# Push tracked data to remote bucket
dvc push
```

### 2. Run Training Pipeline & MLflow Logging
Execute the machine learning pipeline to preprocess features, train a Logistic Regression model, compute metrics, save pickles, and log run details to MLflow:
```bash
python train.py
```
*Outputs are saved under the `models/` directory, and the performance confusion matrix image is placed in `outputs/`.*

### 3. Run Streamlit Application locally
Start the interactive Streamlit user dashboard:
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser to interact with the input fields and trigger live grade classifications!

---

## 🐳 Containerization & Kubernetes Orchestration

### 1. Build Streamlit App Docker Image
Pack your Streamlit application and serialized pickles into a portable container:
```bash
docker build -t nathanirahul/student-performance-app:latest .
```

### 2. Run Docker Container Locally
Verify the containerized Streamlit app:
```bash
docker run -p 8501:8501 nathanirahul/student-performance-app:latest
```

### 3. Orchestrate with Kubernetes (Minikube setup)
Ensure Minikube is started:
```bash
# Start Kubernetes cluster
minikube start

# Load your local Docker image into Minikube's registry
minikube image load nathanirahul/student-performance-app:latest

# Deploy Streamlit pods and expose the NodePort service
kubectl apply -f k8s/k8s-config.yaml

# Check running pod and service status
kubectl get pods
kubectl get services

# Launch the browser service tunnel
minikube service student-app-service
```
*Your application will run on **2 high-availability pod replicas** and be accessible via NodePort **30001** (or the Minikube tunnel URL).*

---

## 🤖 CI/CD Automation (GitHub Actions)

When you push code updates to the `main` branch of your repository, GitHub Actions automatically handles environment provisioning, pulling DVC data from S3, retraining the model, logging registry updates, building the new Docker image, and pushing it to Docker Hub!

### Required GitHub Repository Secrets
Go to your repository at `https://github.com/Rahul-git64/mlops-student-performance.git` -> `Settings` -> `Secrets and variables` -> `Actions` -> `New repository secret`, and add the following:

| Secret Name | Value |
| :--- | :--- |
| **`AWS_ACCESS_KEY_ID`** | `YOUR_AWS_ACCESS_KEY_ID` (your AWS access key) |
| **`AWS_SECRET_ACCESS_KEY`** | `YOUR_AWS_SECRET_ACCESS_KEY` (your AWS secret key) |
| **`AWS_REGION`** | `ap-south-1` |
| **`DOCKER_ACCESS_KEY`** | *Your Docker Hub Personal Access Token (PAT): `YOUR_DOCKER_ACCESS_KEY`* |
| **`DOCKER_USERNAME`** | `nathanirahul` |

---

## 🏆 Project Author
* **Rahul** (MLOps Engineer)
* Based on system designs by Mulagondla Lakshmi Goutham Reddy.
