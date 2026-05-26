# AI-Powered Multi-Agent Workflow Orchestration Platform

An enterprise-style multi-agent orchestration platform built using LangGraph, FastAPI, LangSmith, and OpenTelemetry.

This system enables intelligent routing between specialized AI agents with workflow persistence, recovery handling, approval checkpoints, observability, and real-time updates.

---

# Features

## Multi-Agent Workflow System
- Supervisor Agent
- Researcher Agent
- Coder Agent
- Reviewer Agent
- Writer Agent

## Advanced Workflow Features
- Conditional Routing
- Error Recovery & Retry Logic
- Human Approval Checkpoints
- Real-Time Workflow Updates (WebSockets)

## Persistence & Observability
- SQLite Workflow Persistence
- LangSmith Tracing
- Prometheus Metrics
- OpenTelemetry Support

## API Layer
- FastAPI REST APIs
- Swagger Documentation
- WebSocket Support

---

# Architecture

```text
User
 ↓
FastAPI API Layer
 ↓
LangGraph Supervisor
 ├── Researcher Agent
 ├── Coder Agent
 ├── Reviewer Agent
 └── Writer Agent
 ↓
Recovery / Approval System
 ↓
Persistence Layer (SQLite)
 ↓
Observability
   ├── LangSmith
   └── Prometheus Metrics
```

---

# Tech Stack

- Python
- LangGraph
- LangChain
- FastAPI
- Groq LLM
- SQLite
- LangSmith
- Prometheus
- OpenTelemetry

---

# Project Structure

```text
project/
│
├── agents/
├── api/
├── core/
├── observability/
├── storage/
├── tests/
│
├── requirements.txt
├── README.md
└── .env.example
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <repo_url>
cd <project_name>
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Create Environment File

Copy:

```text
.env.example → .env
```

---

## 4. Add Environment Variables

```env
GROQ_API_KEY=your_groq_api_key
USE_REAL_LLM=true

LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=multi-agent-platform
```

---

# Run Application

```bash
uvicorn api.main:app --reload
```

---

# API Documentation

After server starts:

## Swagger UI

```text
http://127.0.0.1:8000/docs
```

---

# REST APIs

## Start Workflow

```http
POST /workflow/start
```

Example:

```json
{
  "query": "Write quicksort in python"
}
```

---

## Get Workflow Status

```http
GET /workflow/{request_id}
```

---

## Approve Workflow

```http
POST /workflow/{request_id}/approve
```

---

## Reject Workflow

```http
POST /workflow/{request_id}/reject
```

---

# WebSocket Endpoint

```text
ws://127.0.0.1:8000/ws/{request_id}
```

Provides real-time workflow updates.

---

# Metrics Endpoint

```text
http://127.0.0.1:8000/metrics
```

Tracks:
- workflow_success_total
- workflow_failure_total
- workflow_retry_total

---

# LangSmith Tracing

Workflow traces are available on:

```text
https://smith.langchain.com
```

Features:
- Agent execution traces
- Latency tracking
- Workflow debugging
- Input/output monitoring

---

# Testing

Run tests using:

```bash
pytest
```

---

# Implemented User Stories

- US-09 Conditional Routing Logic
- US-10 Error Recovery Subgraphs
- US-11 Approval Checkpoint System
- US-12 Approval UI/APIs
- US-13 Workflow State Persistence
- US-14 LangSmith Tracing
- US-15 OpenTelemetry Metrics

---

# Future Improvements

- Parallel Agent Execution
- Redis Persistence
- JWT Authentication
- React Dashboard
- Kubernetes Deployment
- CI/CD Pipeline

---

# Contributors

- Urvi Jain
- Shruti Mandal
- Srinidhi P Rao
