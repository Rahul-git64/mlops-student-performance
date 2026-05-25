# Submission & MLOps Execution Steps
### Course: Machine Learning System Design (MLSD)
**Author**: Rahul (MLOps Engineer)
**Target Pipeline**: Student Performance Prediction

---

## 🏆 Introduction
This submission document maps out the end-to-end execution, deployment, and verification stages of the **Student Performance Prediction MLOps Pipeline**. The project incorporates Git versioning, DVC remote S3 tracking, MLflow logging, Docker containerization, Kubernetes high-availability orchestration, and GitHub Actions CI/CD automation.

For each of the **12 granular steps**, an intro, a contextual mockup screenshot showing only the application itself, and a detailed technical breakdown are provided.

---

## STEP 1: Verify Raw Dataset Properties

### 📝 Intro
The first step of any Machine Learning System Design (MLSD) project is verifying the integrity and properties of the raw dataset. On Windows, we inspect the file properties of `student_dataset.csv` to ensure it is correctly formatted, has non-zero size, and is situated in the root folder before starting execution.

### 🖼️ Contextual Screenshot
![Windows File Properties for student_dataset.csv](screenshots/dataset_properties_mockup.png)

### 🛠️ Detail
#### 🖥️ Console Commands Required
On Windows, right-click `student_dataset.csv` in your file explorer and click **Properties** (or select the file and press `Alt + Enter`).

#### 🔍 Execution Mechanics & What Happens
* **File Properties Window**: Displays the standard Windows 11 General properties tab.
* **Integrity Validation**: Verifies that the file size is exactly **165 KB (169,805 bytes)**, confirming that the CSV has successfully downloaded and is not corrupted before pipeline execution.

---

## STEP 2: Pre-Initialization Environment Status Checks

### 📝 Intro
Before initializing Git source control and DVC data tracking in the workspace, we run empty status checks. This verifies that no pre-existing repositories exist in the folder and establishes a clean baseline.

### 🖼️ Contextual Screenshot
![Git Bash empty status checks before Git/DVC initialization](screenshots/git_dvc_status_mockup.png)

### 🛠️ Detail
#### 🖥️ Console Commands Required
Open **Git Bash** in the workspace folder and execute:
```bash
# 1. Check Git status on empty directory
git status

# 2. Check DVC status on empty directory
dvc status
```

#### 🔍 Execution Mechanics & What Happens
* **Git Output**: Displays `fatal: not a git repository (or any of the parent directories): .git`, proving the workspace is clean.
* **DVC Output**: Displays an error confirming you are not inside a DVC tracking directory.

---

## STEP 3: Setup Local Environment & Codebase Exploration

### 📝 Intro
Now, we provision our local Python virtual environment, install pinned MLOps library dependencies, and examine the core training scripts in VS Code (Visual Studio Code) to verify code structures.

### 🖼️ Contextual Screenshot
![VS Code Workspace Editor showing app.py and requirements.txt](screenshots/k8s_deployment_mockup.png)

### 🛠️ Detail
#### 🖥️ Console Commands Required
Run environment setup in **Git Bash** and open the project in VS Code:
```bash
# 1. Create a Python Virtual Environment
python -m venv venv

# 2. Activate the Virtual Environment
source venv/Scripts/activate

# 3. Upgrade pip and install package requirements
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4. Open the workspace in VS Code
code .
```

#### 🔍 Execution Mechanics & What Happens
* **Isolation**: The virtual environment (`venv/`) isolates package dependencies.
* **VS Code Editor**: Displays a clean dark-themed editor showing the file tree (`.github/`, `data/`, `k8s/`, `app.py`, `train.py`, `Dockerfile`, `params.yaml`, `requirements.txt`).

---

## STEP 4: Setup AWS S3 bucket IAM credentials (AWS Console)

### 📝 Intro
To connect DVC to remote AWS S3 data storage, we must create a dedicated IAM user (`s3-uploader`) with full read/write programmatic access to the S3 bucket. We inspect the AWS IAM console to confirm the credentials are active.

### 🖼️ Contextual Screenshot
![AWS IAM User Summary Console](screenshots/aws_iam_console_mockup.png)

### 🛠️ Detail
#### 🖥️ Console Commands Required
Log in to your **AWS Console** using a web browser and navigate to **IAM (Identity and Access Management)** -> **Users** -> **`s3-uploader`**.

#### 🔍 Execution Mechanics & What Happens
* **Access Credentials**: Displays the User ARN and active Access Key ID (**`AKIAVORO7DNXNBALEN7O`**) under a clean AWS console navigation bar, confirming programmatic API access is open.

---

## STEP 5: Provision Remote AWS S3 Storage Bucket

### 📝 Intro
Next, we provision a remote S3 data bucket (`mlops-student-performance`) in the **ap-south-1** region (Asia Pacific Mumbai). We enable bucket versioning to ensure dataset revisions can be fully tracked and recovered by DVC.

### 🖼️ Contextual Screenshot
![AWS S3 Buckets Dashboard](screenshots/aws_s3_buckets_mockup.png)

### 🛠️ Detail
#### 🖥️ Console Commands Required
Navigate to **Amazon S3** in your AWS browser console.

#### 🔍 Execution Mechanics & What Happens
* **Bucket Settings**: Verifies the creation of the bucket `mlops-student-performance` in the **ap-south-1** region with versioning active.

---

## STEP 6: Configure Local AWS CLI Session

### 🖥️ Intro
To authenticate our local computer session with the S3 bucket, we configure the AWS Command Line Interface (CLI) using the programmatic keys generated from the IAM console, and verify the connection.

### 🖼️ Contextual Screenshot
![AWS CLI configuration and S3 connection check in Git Bash](screenshots/aws_configure_terminal_mockup.png)

### 🛠️ Detail
#### 🖥️ Console Commands Required
Run AWS configuration inside your **Git Bash** shell:
```bash
# 1. Configure AWS CLI credentials
aws configure
# (Input keys, region as ap-south-1, format as json)

# 2. List S3 buckets to test connection
aws s3 ls
```

#### 🔍 Execution Mechanics & What Happens
* **Credentials Mapping**: Binds the programmatic keys locally under `~/.aws/credentials`.
* **Connection Verification**: Running `aws s3 ls` queries AWS and outputs `mlops-student-performance` with the timestamp, proving connection is successful!

---

## STEP 7: Local Data Versioning Setup (DVC)

### 📝 Intro
With DVC initialized, we set up data tracking for our dataset. This keeps our Git repository lightweight by excluding large data blobs from Git control and routing them directly to DVC instead.

### 🖼️ Contextual Screenshot
![DVC init and DVC push execution in Git Bash](screenshots/dvc_add_push_mockup.png)

### 🛠️ Detail
#### 🖥️ Console Commands Required
Initialize DVC and version-track your student dataset:
```bash
# 1. Initialize DVC in the workspace
dvc init --no-scm --force

# 2. Bind the AWS S3 bucket as DVC remote storage
dvc remote add -d s3remote s3://mlops-student-performance --force

# 3. Add the dataset to DVC tracking
dvc add data/student_dataset.csv

# 4. Push the tracked dataset blob up to AWS S3
dvc push
```

#### 🔍 Execution Mechanics & What Happens
* **DVC Indexing**: DVC indexes the raw dataset and replaces Git's tracking with a tiny pointer file `data/student_dataset.csv.dvc` containing a unique MD5 hash checksum.
* **Git Exclusion**: Appends the dataset path directly to `data/.gitignore` so Git ignores it.
* **Remote Storage Push**: `dvc push` uploads the 165 KB data blob directly to your S3 bucket.

---

## STEP 8: Verify Hashed Objects in S3 Bucket

### 📝 Intro
To prove that DVC successfully pushed the versioned dataset, we inspect the AWS S3 console in Chrome to confirm that the hashed binary files exist in the S3 bucket.

### 🖼️ Contextual Screenshot
![AWS S3 Bucket objects folder showing DVC files](screenshots/s3_uploaded_files_mockup.png)

### 🛠️ Detail
#### 🖥️ Console Commands Required
Open **Amazon S3** in your Chrome browser and click into the bucket **`mlops-student-performance`**.

#### 🔍 Execution Mechanics & What Happens
* **Object Indexing**: Shows S3 objects uploaded under the folder **`files/md5/`** inside a hashed folder like `84/` matching the DVC checksum, proving DVC dataset storage is active!

---

## STEP 9: Model Training & Experiment Tracking (MLflow)

### 📝 Intro
Now, we run the Python training pipeline, which executes preprocessing, fits the Logistic Regression model, computes evaluation metrics, and logs them to the local MLflow dashboard.

### 🖼️ Contextual Screenshot
![MLflow Tracking experiment metrics run table](screenshots/mlflow_dashboard_mockup.png)

### 🛠️ Detail
#### 🖥️ Console Commands Required
Run the ML pipeline and start the MLflow server:
```bash
# 1. Execute the ML training pipeline
python train.py

# 2. Launch the MLflow UI dashboard server
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

#### 🔍 Execution Mechanics & What Happens
* **Experiment Logging**: Logs metrics (Accuracy: ~89.5%, AUC: ~0.91) and parameters (`test_size: 0.20`) to the SQLite backend (`mlflow.db`).
* **Evaluation Plotting**: Computes and saves a Confusion Matrix plot `confusion_matrix.png` to the `outputs/` folder.
* **Pickles Dump**: Serializes the trained model weights and categorical mapping encoders to the `models/` directory.

---

## STEP 10: Run Streamlit Web Application

### 📝 Intro
We launch the interactive Streamlit user dashboard, displaying an active grade prediction card and metric confidence meters, proving our serialization pipelines work.

### 🖼️ Contextual Screenshot
![Streamlit App student grade Pass prediction dashboard](screenshots/streamlit_app_mockup.png)

### 🛠️ Detail
#### 🖥️ Console Commands Required
Launch the user dashboard:
```bash
# Start Streamlit application
streamlit run app.py
```

#### 🔍 Execution Mechanics & What Happens
* **Dashboard Load**: Hosts the glassmorphism UI locally on Port `8501`.
* **Inference Card**: Takes weekly study hours, GPA, and test scores, loads the serialized pickles, runs real-time scaling, and renders a colored Distinction or Pass badge (success green/neon blue) alongside probability meters.

---

## STEP 11: Orchestrate Pods via Kubernetes (Minikube)

### 📝 Intro
For production orchestration, we deploy our containerized app to a local Kubernetes (Minikube) cluster, scaling it across 2 replica pods for failover.

### 🖼️ Contextual Screenshot
![Windows Git Bash - Kubernetes status and Minikube tunnel](screenshots/git_bash_k8s_mockup.png)

### 🛠️ Detail
#### 🖥️ Console Commands Required
Open your **Windows Git Bash** shell and run the deployment commands:
```bash
# 1. Start the local Kubernetes cluster
minikube start

# 2. Deploy Streamlit pods and NodePort service configuration
kubectl apply -f k8s/k8s-config.yaml

# 3. Check the running status of your pods
kubectl get pods

# 4. Launch the local web server tunnel in your browser
minikube service student-app-service
```

#### 🔍 Execution Mechanics & What Happens
* **Replica Pods**: Spawns 2 identical pod replicas (`student-app-deployment-5dbc48fddc-q8txq` and `student-app-deployment-5dbc48fddc-sp7v7`) running the Streamlit app.
* **Service Map**: Creates `student-app-service` mapping NodePort `30001` to Port `8501` in the containers, balancing traffic and tunneling user access directly to the browser.

---

## STEP 12: Verify GitHub Actions CI/CD Run

### 📝 Intro
We push our sanitised codebase to GitHub, triggering a fresh GitHub Actions workflow run. We inspect the runner dashboard to confirm that DVC data pulls, model retraining, and container pushes to Docker Hub have executed successfully.

### 🖼️ Contextual Screenshot
![GitHub Actions successful CI/CD runner steps execution](screenshots/github_actions_run_mockup.png)

### 🛠️ Detail
#### 🖥️ Console Commands Required
Push your code to trigger the GitHub Actions workflow automatically:
```bash
git add .
git commit -m "Optimize CI/CD runner build caching"
git push origin main
```

#### 🔍 Execution Mechanics & What Happens
* **Automated Runner**: GitHub Actions spins up an Ubuntu VM runner, installs `requirements.txt`, securely fetches S3 credentials, pulls S3 DVC data, executes DVC pipelines, compiles the Streamlit container, and successfully pushes it to your Docker Hub!
