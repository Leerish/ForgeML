---

# ForgeML — AI-Native MLOps Platform 🚀

ForgeML is an **end-to-end MLOps platform** designed to manage the complete lifecycle of machine learning systems — from dataset ingestion and validation to model training, experiment tracking, model promotion, and production inference.

The platform is built using **modern ML infrastructure tools** such as Prefect, MLflow, FastAPI, MinIO, Prometheus, Grafana, and Docker.

ForgeML demonstrates how production ML systems are structured in real-world AI platforms.

---

# Architecture

```
Raw Dataset
     │
     ▼
Prefect Ingestion Flow
     │
     ▼
Dataset Validation
     │
     ▼
Dataset Versioning (MinIO)
     │
     ▼
Training Pipeline
     │
     ▼
MLflow Experiment Tracking
     │
     ▼
Model Registry + Promotion Logic
     │
     ▼
Production Model
     │
     ▼
FastAPI Inference API
     │
     ▼
Prometheus + Grafana Monitoring
```

---

# Key Features

### Dataset Management

• Dataset ingestion pipelines
• Dataset validation checks
• Dataset versioning
• Object storage using MinIO

### Training Infrastructure

• Reproducible training pipelines
• Feature preprocessing pipelines
• Model evaluation metrics
• MLflow experiment tracking

### Model Management

• Lightweight model registry
• Automated model promotion logic
• Production model tracking

### Model Serving

• FastAPI inference service
• Production prediction endpoint
• Dockerized API deployment

### Observability

• Prometheus metrics
• Grafana dashboards
• API performance monitoring

### Infrastructure

• Fully containerized platform
• Multi-service architecture with Docker Compose

---

# Tech Stack

| Component              | Technology           |
| ---------------------- | -------------------- |
| Workflow Orchestration | Prefect              |
| Experiment Tracking    | MLflow               |
| Object Storage         | MinIO                |
| Model Serving          | FastAPI              |
| Monitoring             | Prometheus + Grafana |
| Infrastructure         | Docker               |
| Machine Learning       | Scikit-Learn         |
| Database               | PostgreSQL           |

---

# Project Structure

```
ForgeML
│
├── services
│   ├── api
│   │   ├── app
│   │   │   ├── main.py
│   │   │   ├── predict.py
│   │   │   ├── schemas.py
│   │   │   ├── model_loader.py
│   │   │   └── registry_reader.py
│   │   │
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── orchestrator
│   │   └── flows
│   │       ├── ingest.py
│   │       └── train.py
│   │
│   ├── training
│   │   └── train_model.py
│   │
│   └── monitoring
│       └── prometheus.yml
│
├── libs
│   └── features
│       └── feature_builder.py
│
├── artifacts
│   └── credit_model.joblib
│
├── registry
│   └── models.jsonl
│
├── data
│   └── credit.csv
│
├── docker-compose.yml
├── README.md
└── .env.example
```

---

# Running ForgeML

## Start Infrastructure

```
docker compose up -d
```

This launches the following services:

| Service       | URL                                            |
| ------------- | ---------------------------------------------- |
| MLflow        | [http://localhost:5000](http://localhost:5000) |
| Prefect       | [http://localhost:4200](http://localhost:4200) |
| MinIO Console | [http://localhost:9001](http://localhost:9001) |
| Grafana       | [http://localhost:3000](http://localhost:3000) |
| Prometheus    | [http://localhost:9090](http://localhost:9090) |
| Inference API | [http://localhost:8000](http://localhost:8000) |

---

# Train a Model

Run the training flow:

```
python -m services.orchestrator.flows.train credit_risk ./data/credit.csv
```

This will:

1. Load dataset
2. Prepare features
3. Train model
4. Log experiment to MLflow
5. Save model artifact
6. Compare with production model
7. Promote model if performance improves

---

# Inference API

Start the API:

```
uvicorn services.api.app.main:app --reload
```

Open Swagger UI:

```
http://localhost:8000/docs
```

---

# Prediction Example

Endpoint:

```
POST /predict
```

Example response:

```json
{
  "prediction": 1,
  "confidence": 0.99,
  "model_version": "v1"
}
```

---

# Monitoring

ForgeML includes full monitoring support.

### Prometheus Metrics

```
http://localhost:8000/metrics
```

Metrics include:

• Request latency
• Request count
• Error rate
• Response sizes

---

### Grafana Dashboards

```
http://localhost:3000
```

Default login:

```
admin / admin
```

---

# Model Promotion Logic

ForgeML automatically promotes models based on performance.

```
New Model Accuracy > Production Accuracy
           │
           ▼
      Promote Model
```

Otherwise:

```
Reject Candidate Model
```

The registry stores:

```
model_name
version
dataset_version
accuracy
stage
```

---

# Example MLflow Experiment

MLflow UI shows:

• model parameters
• metrics
• artifacts
• training runs

This allows full experiment reproducibility.

---

# Future Improvements

Potential extensions:

• Model drift detection
• Feature store integration
• Distributed training
• Kubernetes deployment
• Online model registry service

---

# Why ForgeML Matters

ForgeML demonstrates how modern machine learning systems are built in production environments.

It showcases concepts used in real AI platforms:

• reproducible ML pipelines
• model lifecycle management
• experiment tracking
• production inference systems
• observability and monitoring

---

# License

MIT License

